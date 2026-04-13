#!/usr/bin/env python3
"""Normalize raw Internet Archive DjVu plain-text files into JSONL records.

DjVu plain text from Internet Archive OCR has specific artifacts:
  - Google Books digitization notice (for Google-scanned items)
  - Cornell University / HathiTrust header (for Cornell-digitized items)
  - Multiple internal spaces between words (OCR column layout artifact)
  - Short running header/footer lines with page numbers
  - No form-feed page break markers (IA strips those in _djvu.txt)

This script applies source-specific cleaning without removing philosophical content.
It does not segment, deduplicate, or tokenize.
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


DEFAULT_RAW_DIR = Path("corpus/raw/internet_archive")
DEFAULT_VERSIONS_MANIFEST = Path("corpus/manifests/versions.jsonl")
DEFAULT_WORKS_MANIFEST = Path("corpus/manifests/works.jsonl")
DEFAULT_OUTPUT = Path("corpus/normalized/jsonl/internet_archive.jsonl")

# Google Books digitization notice: begins at line 1, ends with Google Book
# Search URL or "at http://books.google.com". The notice spans ~45-55 lines.
GOOGLE_BOOKS_NOTICE_RE = re.compile(
    r"(?s)\A\s*This is a digital copy of a book.*?"
    r"(?:at\s+j?https?://(?:books\s*\.\s*google|www\s*\.\s*google).*?\n"
    r"|at\s+j?http\s*:\s*//books\s*\.\s*qoo[a-z]*\s*\..*?\n)"
    r"\s*"
)

# Cornell/Internet Archive header: "The original of this book is in the Cornell
# University Library. There are no known copyright restrictions..."
CORNELL_HEADER_RE = re.compile(
    r"(?s)\A\s*The original of (?:this|tli[ei]s) book.*?"
    r"https?://www\.archive\.org/details/\S+\s*\n"
    r"\s*"
)

MULTIPLE_SPACES_RE = re.compile(r"  +")
MULTIPLE_BLANK_LINES_RE = re.compile(r"\n{3,}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Remove Internet Archive DjVu boilerplate and normalize raw text "
            "files to corpus/normalized/jsonl/internet_archive.jsonl."
        )
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help=f"Raw Internet Archive directory. Default: {DEFAULT_RAW_DIR}",
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
        help="Normalize only the first N records, useful for smoke tests.",
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
        help="Validate inputs and print the plan without writing JSONL.",
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
        if record.get("source") != "internet_archive":
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
                f"Internet Archive records: {', '.join(missing)}"
            )

    return selected


def require_field(record: dict[str, Any], field: str) -> None:
    if not record.get(field):
        version_id = record.get("version_id", "<unknown>")
        raise SystemExit(f"{version_id}: missing required field {field!r}")


def raw_dir_for_record(raw_dir: Path, record: dict[str, Any]) -> Path:
    source_id = str(record["source_id"])
    version_id = str(record["version_id"])
    return raw_dir / f"ia_{source_id}_{version_id}"


def raw_text_path(raw_dir: Path, record: dict[str, Any]) -> Path:
    return raw_dir_for_record(raw_dir, record) / f"{record['version_id']}.txt"


def metadata_path(raw_dir: Path, record: dict[str, Any]) -> Path:
    return raw_dir_for_record(raw_dir, record) / "metadata.json"


def load_sidecar(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc


def strip_ia_boilerplate(raw_text: str) -> tuple[str, dict[str, Any]]:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n").replace("\ufeff", "")
    google_notice_removed = False
    cornell_notice_removed = False

    match = GOOGLE_BOOKS_NOTICE_RE.match(text)
    if match:
        text = text[match.end():]
        google_notice_removed = True

    match = CORNELL_HEADER_RE.match(text)
    if match:
        text = text[match.end():]
        cornell_notice_removed = True

    text = normalize_ia_text(text)
    return text, {
        "boilerplate_removed": google_notice_removed or cornell_notice_removed,
        "google_books_notice_removed": google_notice_removed,
        "cornell_header_removed": cornell_notice_removed,
    }


def normalize_ia_text(text: str) -> str:
    text = text.replace("\f", "\n")
    text = unicodedata.normalize("NFC", text)
    # Collapse multiple spaces within lines (OCR artifact from column formatting)
    lines = []
    for line in text.split("\n"):
        line = line.rstrip()
        line = MULTIPLE_SPACES_RE.sub(" ", line)
        lines.append(line)
    text = "\n".join(lines).strip()
    text = MULTIPLE_BLANK_LINES_RE.sub("\n\n", text)
    return text


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
            if artifact.get("format") == "djvu_txt"
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
            "normalizer": "scripts/normalize/normalize_internet_archive.py",
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
    total_chars = 0
    boilerplate_removed = 0

    with temp_output.open("w", encoding="utf-8") as handle:
        for version_record in records:
            txt_path = raw_text_path(raw_dir, version_record)
            sidecar_path = metadata_path(raw_dir, version_record)
            acquisition_metadata = load_sidecar(sidecar_path)
            raw_text = txt_path.read_text(encoding="utf-8-sig", errors="replace")
            text, normalization_metadata = strip_ia_boilerplate(raw_text)

            if normalization_metadata["boilerplate_removed"]:
                boilerplate_removed += 1

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
        "boilerplate_removed": boilerplate_removed,
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
        print(f"Selected high-confidence Internet Archive records: {len(records)}")
        print(f"Raw directory: {args.raw_dir}")
        print(f"Output path: {args.output}")
        return 0

    summary = normalize_records(records, works_by_id, args.raw_dir, args.output)
    print(
        f"Wrote {summary['records_written']} records to {summary['output']} "
        f"({summary['total_text_chars']} normalized characters)."
    )
    print(f"Boilerplate removed from {summary['boilerplate_removed']} records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
