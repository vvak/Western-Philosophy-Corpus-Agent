#!/usr/bin/env python3
"""Normalize raw Project Gutenberg text into JSONL records.

This script removes Project Gutenberg boilerplate and preserves acquisition
metadata. It does not segment, deduplicate, or edit raw files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_RAW_DIR = Path("corpus/raw/gutenberg")
DEFAULT_VERSIONS_MANIFEST = Path("corpus/manifests/versions.jsonl")
DEFAULT_WORKS_MANIFEST = Path("corpus/manifests/works.jsonl")
DEFAULT_OUTPUT = Path("corpus/normalized/jsonl/gutenberg.jsonl")

START_MARKER_RE = re.compile(
    r"(?im)^\s*\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*\s*$"
)
END_MARKER_RE = re.compile(
    r"(?im)^\s*\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*\s*$"
)
MULTIPLE_BLANK_LINES_RE = re.compile(r"\n{3,}")
LEADING_CREDIT_RE = re.compile(
    r"(?is)\A\s*(?:Produced by|E-text prepared by|This etext was produced by)\b.*?(?:\n\s*\n)+"
)
LEADING_ASTERISK_NOTICE_RE = re.compile(r"(?s)\A\s*\*{20,}\s*\n.*?\n\s*\*{20,}\s*(?:\n\s*)*")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Remove Project Gutenberg boilerplate from raw .txt artifacts and "
            "write normalized JSONL to corpus/normalized/jsonl/gutenberg.jsonl."
        )
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help=f"Raw Project Gutenberg directory. Default: {DEFAULT_RAW_DIR}",
    )
    parser.add_argument(
        "--versions-manifest",
        type=Path,
        default=DEFAULT_VERSIONS_MANIFEST,
        help=f"Version manifest path. Default: {DEFAULT_VERSIONS_MANIFEST}",
    )
    parser.add_argument(
        "--works-manifest",
        type=Path,
        default=DEFAULT_WORKS_MANIFEST,
        help=f"Work manifest path. Default: {DEFAULT_WORKS_MANIFEST}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output JSONL path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Normalize only the first N selected records, useful for smoke tests.",
    )
    parser.add_argument(
        "--version-id",
        action="append",
        default=None,
        help="Normalize only a specific version_id. May be passed multiple times.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print the normalization plan without writing JSONL.",
    )
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSON: {exc}") from exc
    return rows


def select_records(
    versions: list[dict[str, Any]], version_ids: set[str] | None, limit: int | None
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for record in versions:
        if record.get("source") != "project_gutenberg":
            continue
        if record.get("resolution_confidence") != "high":
            continue
        if version_ids is not None and record.get("version_id") not in version_ids:
            continue
        require_field(record, "version_id")
        require_field(record, "source_id")
        require_field(record, "source_url")
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
                f"Project Gutenberg records: {', '.join(missing)}"
            )

    return selected


def require_field(record: dict[str, Any], field: str) -> None:
    if not record.get(field):
        version_id = record.get("version_id", "<unknown>")
        raise SystemExit(f"{version_id}: missing required field {field!r}")


def record_dir(raw_dir: Path, record: dict[str, Any]) -> Path:
    return raw_dir / f"pg_{record['source_id']}_{record['version_id']}"


def raw_text_path(raw_dir: Path, record: dict[str, Any]) -> Path:
    return record_dir(raw_dir, record) / f"{record['version_id']}.txt"


def metadata_path(raw_dir: Path, record: dict[str, Any]) -> Path:
    return record_dir(raw_dir, record) / "metadata.json"


def load_sidecar(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc


def strip_gutenberg_boilerplate(raw_text: str) -> tuple[str, dict[str, Any]]:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n").replace("\ufeff", "")
    start_match = START_MARKER_RE.search(text)
    if not start_match:
        raise ValueError("missing Project Gutenberg START marker")

    content_start = start_match.end()
    end_match = END_MARKER_RE.search(text, content_start)
    content_end = end_match.start() if end_match else len(text)

    body = text[content_start:content_end]
    body, leading_notes_removed = strip_leading_project_gutenberg_notes(body)
    body = normalize_text(body)
    return body, {
        "boilerplate_removed": True,
        "start_marker_found": True,
        "end_marker_found": bool(end_match),
        "leading_project_gutenberg_notes_removed": leading_notes_removed,
        "start_marker_line": line_number_for_offset(text, start_match.start()),
        "end_marker_line": line_number_for_offset(text, end_match.start()) if end_match else None,
    }


def strip_leading_project_gutenberg_notes(text: str) -> tuple[str, int]:
    removed = 0
    while True:
        for pattern in (LEADING_ASTERISK_NOTICE_RE, LEADING_CREDIT_RE):
            match = pattern.match(text)
            if match:
                text = text[match.end() :]
                removed += 1
                break
        else:
            return text, removed


def normalize_text(text: str) -> str:
    text = text.replace("\f", "\n")
    text = unicodedata.normalize("NFC", text)
    lines = [line.rstrip() for line in text.split("\n")]
    text = "\n".join(lines).strip()
    text = MULTIPLE_BLANK_LINES_RE.sub("\n\n", text)
    return text


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_record(
    version_record: dict[str, Any],
    work_record: dict[str, Any] | None,
    acquisition_metadata: dict[str, Any],
    raw_path: Path,
    text: str,
    normalization_metadata: dict[str, Any],
    normalized_at_utc: str,
) -> dict[str, Any]:
    raw_artifact = next(
        (
            artifact
            for artifact in acquisition_metadata.get("artifacts", [])
            if artifact.get("format") == "txt"
        ),
        {},
    )
    title = version_record.get("title") or (work_record or {}).get("title")

    return {
        "doc_id": f"{version_record['version_id']}__full_text",
        "work_id": version_record.get("work_id"),
        "version_id": version_record.get("version_id"),
        "title": title,
        "author": (work_record or {}).get("author"),
        "author_metadata": version_record.get("author_metadata"),
        "translator": version_record.get("translator"),
        "editor": version_record.get("editor"),
        "language": version_record.get("language"),
        "source": version_record.get("source"),
        "source_id": version_record.get("source_id"),
        "source_url": version_record.get("source_url"),
        "source_release_date": version_record.get("source_release_date"),
        "license_status": version_record.get("license_status"),
        "license_rationale": version_record.get("license_rationale"),
        "quality_tier": (work_record or {}).get("quality_tier"),
        "period": (work_record or {}).get("period"),
        "resolution_confidence": version_record.get("resolution_confidence"),
        "acquisition_method": version_record.get("acquisition_method"),
        "hierarchy": {
            "work": title,
            "book": None,
            "section": None,
        },
        "raw": {
            "raw_path": str(raw_path),
            "raw_sha256": sha256_file(raw_path),
            "source_artifact_url": raw_artifact.get("source_url"),
            "acquired_at_utc": acquisition_metadata.get("acquired_at_utc"),
        },
        "normalization": {
            **normalization_metadata,
            "normalized_at_utc": normalized_at_utc,
            "normalizer": "scripts/normalize/normalize_gutenberg.py",
            "unicode_normalization": "NFC",
            "segmentation": "full_text_only",
            "text_char_count": len(text),
            "text_line_count": text.count("\n") + 1 if text else 0,
        },
        "manifest_record": version_record,
        "acquisition_metadata": acquisition_metadata,
        "text": text,
    }


def validate_inputs(records: list[dict[str, Any]], raw_dir: Path) -> None:
    missing: list[str] = []
    for record in records:
        txt_path = raw_text_path(raw_dir, record)
        sidecar_path = metadata_path(raw_dir, record)
        if not txt_path.is_file():
            missing.append(str(txt_path))
        if not sidecar_path.is_file():
            missing.append(str(sidecar_path))
    if missing:
        raise SystemExit("Missing required raw inputs:\n" + "\n".join(missing))


def normalize_records(
    records: list[dict[str, Any]],
    works_by_id: dict[str, dict[str, Any]],
    raw_dir: Path,
    output: Path,
) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_output = output.with_suffix(output.suffix + ".tmp")
    normalized_at_utc = datetime.now(timezone.utc).isoformat()
    count = 0
    missing_end_markers = 0
    total_chars = 0

    with temp_output.open("w", encoding="utf-8") as handle:
        for version_record in records:
            txt_path = raw_text_path(raw_dir, version_record)
            sidecar_path = metadata_path(raw_dir, version_record)
            acquisition_metadata = load_sidecar(sidecar_path)
            raw_text = txt_path.read_text(encoding="utf-8-sig", errors="replace")
            text, normalization_metadata = strip_gutenberg_boilerplate(raw_text)

            if not normalization_metadata["end_marker_found"]:
                missing_end_markers += 1

            work_record = works_by_id.get(str(version_record.get("work_id")))
            record = build_record(
                version_record=version_record,
                work_record=work_record,
                acquisition_metadata=acquisition_metadata,
                raw_path=txt_path,
                text=text,
                normalization_metadata=normalization_metadata,
                normalized_at_utc=normalized_at_utc,
            )
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
            total_chars += len(text)

    temp_output.replace(output)
    return {
        "records_written": count,
        "output": str(output),
        "missing_end_markers": missing_end_markers,
        "total_text_chars": total_chars,
    }


def main() -> int:
    args = parse_args()
    versions = load_jsonl(args.versions_manifest)
    works = load_jsonl(args.works_manifest)
    works_by_id = {str(record.get("work_id")): record for record in works}
    version_ids = set(args.version_id) if args.version_id else None
    records = select_records(versions, version_ids, args.limit)
    validate_inputs(records, args.raw_dir)

    if args.dry_run:
        print("Dry run only; no JSONL will be written.")
        print(f"Selected high-confidence Project Gutenberg records: {len(records)}")
        print(f"Raw directory: {args.raw_dir}")
        print(f"Output path: {args.output}")
        return 0

    summary = normalize_records(records, works_by_id, args.raw_dir, args.output)
    print(
        f"Wrote {summary['records_written']} records to {summary['output']} "
        f"({summary['total_text_chars']} normalized characters)."
    )
    if summary["missing_end_markers"]:
        print(
            "Warning: "
            f"{summary['missing_end_markers']} record(s) had no Project Gutenberg END marker."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
