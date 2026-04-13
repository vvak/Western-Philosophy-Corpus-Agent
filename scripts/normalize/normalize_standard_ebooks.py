#!/usr/bin/env python3
"""Normalize raw Standard Ebooks EPUB artifacts into JSONL records.

This script extracts text from Standard Ebooks EPUBs, removes SE boilerplate
(titlepage, imprint, halftitlepage, colophon, uncopyright), and produces
normalized JSONL records preserving all provenance metadata.

It does not segment by work/chapter, deduplicate, or edit raw files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_RAW_DIR = Path("corpus/raw/standard_ebooks")
DEFAULT_VERSIONS_MANIFEST = Path("corpus/manifests/versions.jsonl")
DEFAULT_WORKS_MANIFEST = Path("corpus/manifests/works.jsonl")
DEFAULT_OUTPUT = Path("corpus/normalized/jsonl/standard_ebooks.jsonl")

# Standard Ebooks boilerplate files to exclude from text extraction.
# These are SE infrastructure pages, not philosophical content.
SE_SKIP_FILENAMES = frozenset(
    {
        "titlepage.xhtml",
        "imprint.xhtml",
        "halftitlepage.xhtml",
        "colophon.xhtml",
        "uncopyright.xhtml",
    }
)

# HTML tags treated as block-level elements. Text before and after these
# elements receives paragraph separator treatment (double newline).
BLOCK_TAGS = frozenset(
    {
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
        "li",
        "dt",
        "dd",
        "pre",
        "section",
        "article",
        "hgroup",
        "figcaption",
        "th",
        "td",
        "caption",
        "header",
        "footer",
        "div",
        "nav",
    }
)

# HTML tags whose entire subtree should be omitted from text output.
SKIP_TAGS = frozenset({"script", "style", "head"})

MULTIPLE_BLANK_LINES_RE = re.compile(r"\n{3,}")
HORIZONTAL_SPACE_RE = re.compile(r"[ \t]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract text from Standard Ebooks EPUB artifacts and write "
            "normalized JSONL to corpus/normalized/jsonl/standard_ebooks.jsonl."
        )
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help=f"Raw Standard Ebooks directory. Default: {DEFAULT_RAW_DIR}",
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
        if record.get("source") != "standard_ebooks":
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
                f"Standard Ebooks records: {', '.join(missing)}"
            )

    return selected


def require_field(record: dict[str, Any], field: str) -> None:
    if not record.get(field):
        version_id = record.get("version_id", "<unknown>")
        raise SystemExit(f"{version_id}: missing required field {field!r}")


def epub_slug(source_id: str) -> str:
    return source_id.replace("/", "_")


def raw_dir_for_record(raw_dir: Path, record: dict[str, Any]) -> Path:
    source_id = str(record["source_id"])
    version_id = str(record["version_id"])
    slug = epub_slug(source_id)
    return raw_dir / f"se_{slug}_{version_id}"


def epub_path_for_record(raw_dir: Path, record: dict[str, Any]) -> Path:
    record_dir = raw_dir_for_record(raw_dir, record)
    version_id = str(record["version_id"])
    return record_dir / f"{version_id}.epub"


def metadata_path(raw_dir: Path, record: dict[str, Any]) -> Path:
    return raw_dir_for_record(raw_dir, record) / "metadata.json"


def load_sidecar(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc


def validate_inputs(records: list[dict[str, Any]], raw_dir: Path) -> None:
    missing: list[str] = []
    for record in records:
        ep = epub_path_for_record(raw_dir, record)
        sidecar = metadata_path(raw_dir, record)
        if not ep.is_file():
            missing.append(str(ep))
        if not sidecar.is_file():
            missing.append(str(sidecar))
    if missing:
        raise SystemExit("Missing required raw inputs:\n" + "\n".join(missing))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_text(elem: ET.Element, out: list[str]) -> None:
    """Recursively collect text from an XML element tree.

    Block-level elements contribute double newlines before and after their
    content. SKIP_TAGS elements (script, style, head) are omitted entirely.
    <br> produces a single newline.
    """
    tag = elem.tag.split("}")[1] if "}" in elem.tag else elem.tag

    if tag in SKIP_TAGS:
        # Omit entire subtree. Tail text (after this element's closing tag)
        # is handled by the caller.
        return

    if tag == "br":
        out.append("\n")
        # Tail is handled by caller.
        return

    is_block = tag in BLOCK_TAGS
    if is_block:
        out.append("\n\n")

    if elem.text:
        out.append(elem.text)

    for child in elem:
        collect_text(child, out)
        if child.tail:
            out.append(child.tail)

    if is_block:
        out.append("\n\n")


def xhtml_body_text(xhtml_content: str) -> str:
    """Extract readable text from an XHTML file's body element."""
    # Parse as XML. Standard Ebooks produces clean, namespace-declared XHTML.
    try:
        root = ET.fromstring(xhtml_content)
    except ET.ParseError as exc:
        # Fall back: strip all tags with regex.
        text = re.sub(r"<[^>]+>", " ", xhtml_content)
        text = re.sub(r"&[a-zA-Z0-9#]+;", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    # Locate the body element (with or without namespace).
    xhtml_ns = "http://www.w3.org/1999/xhtml"
    body_ns = root.find(f"{{{xhtml_ns}}}body")
    body = body_ns if body_ns is not None else root.find("body")
    if body is None:
        body = root

    parts: list[str] = []
    collect_text(body, parts)
    raw = "".join(parts)

    # Normalize whitespace: collapse runs of spaces/tabs, then collapse
    # runs of 3+ newlines to 2.
    raw = HORIZONTAL_SPACE_RE.sub(" ", raw)
    raw = MULTIPLE_BLANK_LINES_RE.sub("\n\n", raw)
    return raw.strip()


def extract_text_from_epub(
    epub_path: Path,
) -> tuple[str, dict[str, Any]]:
    """Extract main text from a Standard Ebooks EPUB.

    Returns (normalized_text, extraction_metadata).

    The extraction:
    - Follows container.xml → OPF → spine order.
    - Skips SE boilerplate files (titlepage, imprint, colophon, etc.).
    - Keeps prefaces, introductions, chapters, endnotes, appendices.
    - Joins content files with double newlines.
    - Applies Unicode NFC normalization.
    """
    with zipfile.ZipFile(epub_path) as zf:
        # 1. Read container.xml to find OPF path.
        container_xml = zf.read("META-INF/container.xml").decode("utf-8")
        container_root = ET.fromstring(container_xml)
        opf_path: str | None = None
        for elem in container_root.iter():
            local = elem.tag.split("}")[1] if "}" in elem.tag else elem.tag
            if local == "rootfile":
                opf_path = elem.get("full-path")
                break
        if not opf_path:
            raise ValueError(f"{epub_path}: no OPF rootfile found in container.xml")

        opf_dir = opf_path.rsplit("/", 1)[0] if "/" in opf_path else ""

        # 2. Parse OPF to get manifest and spine.
        opf_xml = zf.read(opf_path).decode("utf-8")
        opf_root = ET.fromstring(opf_xml)

        # Build manifest: item-id → href (relative to OPF dir).
        manifest: dict[str, str] = {}
        for elem in opf_root.iter():
            local = elem.tag.split("}")[1] if "}" in elem.tag else elem.tag
            if local == "item":
                item_id = elem.get("id")
                href = elem.get("href")
                if item_id and href:
                    manifest[item_id] = href

        # Get spine reading order.
        spine_hrefs: list[str] = []
        for elem in opf_root.iter():
            local = elem.tag.split("}")[1] if "}" in elem.tag else elem.tag
            if local == "itemref":
                ref_id = elem.get("idref")
                if ref_id and ref_id in manifest:
                    spine_hrefs.append(manifest[ref_id])

        # 3. Extract text from each spine item in order.
        text_parts: list[str] = []
        items_accepted = 0
        items_skipped = 0
        items_failed = 0
        skipped_filenames: list[str] = []

        for href in spine_hrefs:
            filename = href.rsplit("/", 1)[-1] if "/" in href else href
            if filename in SE_SKIP_FILENAMES:
                items_skipped += 1
                skipped_filenames.append(filename)
                continue

            # Construct full path within the ZIP.
            full_path = f"{opf_dir}/{href}" if opf_dir else href

            try:
                raw = zf.read(full_path).decode("utf-8")
            except KeyError:
                try:
                    raw = zf.read(href).decode("utf-8")
                except KeyError:
                    items_failed += 1
                    continue

            body_text = xhtml_body_text(raw)
            if body_text.strip():
                text_parts.append(body_text)
                items_accepted += 1

        full_text = "\n\n".join(text_parts)
        full_text = unicodedata.normalize("NFC", full_text)
        full_text = MULTIPLE_BLANK_LINES_RE.sub("\n\n", full_text).strip()

    return full_text, {
        "spine_items_total": items_accepted + items_skipped + items_failed,
        "spine_items_accepted": items_accepted,
        "spine_items_skipped": items_skipped,
        "spine_items_failed": items_failed,
        "skipped_filenames": skipped_filenames,
    }


def build_record(
    version_record: dict[str, Any],
    work_record: dict[str, Any] | None,
    acquisition_metadata: dict[str, Any],
    epub_path: Path,
    text: str,
    extraction_metadata: dict[str, Any],
    normalized_at_utc: str,
) -> dict[str, Any]:
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
            "raw_path": str(epub_path),
            "raw_sha256": sha256_file(epub_path),
            "source_artifact_url": acquisition_metadata.get("artifacts", [{}])[0].get("source_url"),
            "acquired_at_utc": acquisition_metadata.get("acquired_at_utc"),
        },
        "normalization": {
            **extraction_metadata,
            "normalized_at_utc": normalized_at_utc,
            "normalizer": "scripts/normalize/normalize_standard_ebooks.py",
            "unicode_normalization": "NFC",
            "segmentation": "full_text_only",
            "se_skip_filenames": sorted(SE_SKIP_FILENAMES),
            "text_char_count": len(text),
            "text_line_count": text.count("\n") + 1 if text else 0,
        },
        "manifest_record": version_record,
        "acquisition_metadata": acquisition_metadata,
        "text": text,
    }


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
    failures: list[str] = []

    with temp_output.open("w", encoding="utf-8") as handle:
        for version_record in records:
            ep = epub_path_for_record(raw_dir, version_record)
            sidecar_path = metadata_path(raw_dir, version_record)
            acquisition_metadata = load_sidecar(sidecar_path)

            try:
                text, extraction_metadata = extract_text_from_epub(ep)
            except Exception as exc:
                version_id = version_record.get("version_id", "<unknown>")
                failures.append(f"{version_id}: {exc}")
                print(f"FAIL {version_id}: {exc}")
                continue

            work_record = works_by_id.get(str(version_record.get("work_id")))
            record = build_record(
                version_record=version_record,
                work_record=work_record,
                acquisition_metadata=acquisition_metadata,
                epub_path=ep,
                text=text,
                extraction_metadata=extraction_metadata,
                normalized_at_utc=normalized_at_utc,
            )
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
            total_chars += len(text)
            version_id = version_record.get("version_id", "<unknown>")
            chars = len(text)
            print(f"OK {version_id}: {chars:,} chars")

    temp_output.replace(output)
    return {
        "records_written": count,
        "failures": failures,
        "output": str(output),
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
        print(f"Selected high-confidence Standard Ebooks records: {len(records)}")
        print(f"Raw directory: {args.raw_dir}")
        print(f"Output path: {args.output}")
        return 0

    summary = normalize_records(records, works_by_id, args.raw_dir, args.output)
    print(
        f"\nWrote {summary['records_written']} records to {summary['output']} "
        f"({summary['total_text_chars']:,} normalized characters)."
    )
    if summary["failures"]:
        print(f"Failures ({len(summary['failures'])}):")
        for f in summary["failures"]:
            print(f"  {f}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
