#!/usr/bin/env python3
"""Acquire raw Internet Archive DjVu plain-text artifacts listed in the version manifest.

This script downloads the plain-text DjVu output (_djvu.txt) produced by
Internet Archive's OCR pipeline for each high-confidence internet_archive
record in the version manifest.

Download pattern:
  https://archive.org/download/{source_id}/{source_id}_djvu.txt

This script is intentionally source-specific and acquisition-only. It does not
normalize, segment, deduplicate, or perform any text cleaning.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST = Path("corpus/manifests/versions.jsonl")
DEFAULT_OUTPUT_DIR = Path("corpus/raw/internet_archive")
USER_AGENT = "western-philosophy-corpus/0.1 (metadata-preserving corpus build)"


@dataclass(frozen=True)
class DownloadCandidate:
    format_name: str
    url: str
    filename: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download raw Internet Archive DjVu plain-text artifacts for "
            "high-confidence internet_archive records in corpus/manifests/versions.jsonl."
        )
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=f"Path to versions JSONL manifest. Default: {DEFAULT_MANIFEST}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Raw Internet Archive output directory. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of selected manifest records, useful for smoke tests.",
    )
    parser.add_argument(
        "--version-id",
        action="append",
        default=None,
        help="Acquire only a specific version_id. May be passed multiple times.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing raw artifact files. Existing files are skipped by default.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Network timeout in seconds for each download request. Default: 120.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=1.0,
        help="Delay in seconds between network requests. Default: 1.0.",
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        default=True,
        help="Print the acquisition plan without writing files. This is the default.",
    )
    mode.add_argument(
        "--download",
        dest="dry_run",
        action="store_false",
        help="Perform downloads and write raw artifacts plus metadata sidecars.",
    )

    return parser.parse_args()


def load_manifest(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            records.append(record)
    return records


def select_records(
    records: list[dict[str, Any]], version_ids: set[str] | None, limit: int | None
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for record in records:
        if record.get("source") != "internet_archive":
            continue
        if record.get("resolution_confidence") != "high":
            continue
        if version_ids is not None and record.get("version_id") not in version_ids:
            continue
        require_manifest_field(record, "version_id")
        require_manifest_field(record, "source_id")
        require_manifest_field(record, "source_url")
        require_manifest_field(record, "license_rationale")
        selected.append(record)

    if limit is not None:
        if limit < 0:
            raise SystemExit("--limit must be non-negative")
        selected = selected[:limit]

    if version_ids is not None:
        found = {record["version_id"] for record in selected}
        missing = sorted(version_ids - found)
        if missing:
            raise SystemExit(
                "Requested version_id values are missing or not high-confidence "
                f"Internet Archive records: {', '.join(missing)}"
            )

    return selected


def require_manifest_field(record: dict[str, Any], field: str) -> None:
    if not record.get(field):
        version_id = record.get("version_id", "<unknown>")
        raise SystemExit(f"{version_id}: missing required manifest field {field!r}")


def djvu_txt_url(source_id: str) -> str:
    return f"https://archive.org/download/{source_id}/{source_id}_djvu.txt"


def candidate_for_record(record: dict[str, Any]) -> DownloadCandidate:
    source_id = str(record["source_id"])
    version_id = str(record["version_id"])
    return DownloadCandidate(
        format_name="djvu_txt",
        url=djvu_txt_url(source_id),
        filename=f"{version_id}.txt",
    )


def raw_dir_for_record(output_dir: Path, record: dict[str, Any]) -> Path:
    source_id = str(record["source_id"])
    version_id = str(record["version_id"])
    return output_dir / f"ia_{source_id}_{version_id}"


def dry_run(records: list[dict[str, Any]], output_dir: Path) -> int:
    print("Dry run only; no files will be written.")
    print(f"Selected high-confidence Internet Archive records: {len(records)}")
    print(f"Output directory: {output_dir}")

    for record in records:
        record_dir = raw_dir_for_record(output_dir, record)
        candidate = candidate_for_record(record)
        print(f"\n{record['version_id']} -> {record_dir}")
        print(f"  [{candidate.format_name}] {candidate.url} -> {candidate.filename}")

    print(f"\nPlanned artifacts: {len(records)}")
    return 0


def download(records: list[dict[str, Any]], args: argparse.Namespace) -> int:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    downloaded = 0
    skipped = 0

    for record in records:
        record_dir = raw_dir_for_record(args.output_dir, record)
        record_dir.mkdir(parents=True, exist_ok=True)
        metadata: dict[str, Any] = {
            "version_id": record["version_id"],
            "work_id": record.get("work_id"),
            "source": record.get("source"),
            "source_id": record["source_id"],
            "source_url": record["source_url"],
            "license_status": record.get("license_status"),
            "license_rationale": record["license_rationale"],
            "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
            "manifest_record": record,
            "artifacts": [],
        }

        candidate = candidate_for_record(record)
        destination = record_dir / candidate.filename
        artifact_metadata: dict[str, Any] = {
            "format": candidate.format_name,
            "source_url": candidate.url,
            "raw_path": str(destination),
        }

        if destination.exists() and not args.overwrite:
            artifact_metadata["status"] = "skipped_existing"
            artifact_metadata.update(file_fingerprint(destination))
            skipped += 1
            metadata["artifacts"].append(artifact_metadata)
            print(f"SKIP existing {destination}")
        else:
            try:
                response_metadata = fetch(candidate.url, destination, args.timeout)
            except urllib.error.HTTPError as exc:
                artifact_metadata["status"] = "failed"
                artifact_metadata["error"] = f"HTTP {exc.code}: {exc.reason}"
                failures += 1
                print(f"FAIL {candidate.url}: HTTP {exc.code} {exc.reason}", file=sys.stderr)
            except urllib.error.URLError as exc:
                artifact_metadata["status"] = "failed"
                artifact_metadata["error"] = f"URL error: {exc.reason}"
                failures += 1
                print(f"FAIL {candidate.url}: {exc.reason}", file=sys.stderr)
            else:
                artifact_metadata["status"] = "downloaded"
                artifact_metadata.update(response_metadata)
                artifact_metadata.update(file_fingerprint(destination))
                downloaded += 1
                print(f"OK {candidate.url} -> {destination}")

            metadata["artifacts"].append(artifact_metadata)
            if args.sleep > 0:
                time.sleep(args.sleep)

        metadata_path = record_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        f"Completed Internet Archive acquisition: {downloaded} downloaded, "
        f"{skipped} skipped, {failures} failed."
    )
    return 1 if failures else 0


def fetch(url: str, destination: Path, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()

    destination.write_bytes(data)
    return {
        "http_status": getattr(response, "status", None),
        "content_type": response.headers.get("Content-Type"),
        "content_length_header": response.headers.get("Content-Length"),
    }


def file_fingerprint(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return {"byte_count": size, "sha256": digest.hexdigest()}


def main() -> int:
    args = parse_args()
    records = load_manifest(args.manifest)
    version_ids = set(args.version_id) if args.version_id else None
    selected = select_records(records, version_ids, args.limit)

    if args.dry_run:
        return dry_run(selected, args.output_dir)
    return download(selected, args)


if __name__ == "__main__":
    raise SystemExit(main())
