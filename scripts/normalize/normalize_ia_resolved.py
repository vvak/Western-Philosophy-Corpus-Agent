#!/usr/bin/env python3
"""Normalize IA-resolved texts into JSONL records."""

import argparse
import gzip
import json
import re
import unicodedata
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


DEFAULT_RAW_DIR = Path("corpus/raw/internet_archive_resolved")
DEFAULT_VERSIONS_MANIFEST = Path("corpus/manifests/versions.jsonl")
DEFAULT_OUTPUT = Path("corpus/normalized/jsonl/ia_resolved.jsonl")
DEFAULT_OCR_SCORES = Path("corpus/reports/ocr_quality_scores.jsonl")


def normalize_unicode(text: str) -> str:
    """Apply Unicode normalization (NFC)."""
    return unicodedata.normalize("NFC", text)


def clean_text(text: str) -> str:
    """Clean common OCR artifacts and boilerplate."""
    # Remove multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove page numbers (lines with just digits, possibly with punctuation)
    text = re.sub(r"^[ \t]*[\d\-—–]+[ \t]*$", "", text, flags=re.MULTILINE)

    # Fix spacing around punctuation
    text = re.sub(r"\s+([.,:;!?])", r"\1", text)
    text = re.sub(r"([.,:;!?])\s+", r"\1 ", text)

    # Normalize whitespace
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n +", "\n", text)

    return text.strip()


def _local_name(tag: str) -> str:
    """Strip an XML namespace from a tag, returning the local element name."""
    return tag.rsplit("}", 1)[-1]


def extract_abbyy_text(fileobj: Any) -> str:
    """Reconstruct plain text from an ABBYY FineReader XML stream.

    IA `_abbyy.gz` files hold layout XML, not text: each glyph is a
    ``<charParams>`` element grouped under ``<line>`` / ``<par>`` / ``<page>``,
    with word boundaries flagged by ``wordStart="true"`` (explicit space
    ``<charParams>`` may also appear). Emit one line break per ``<line>`` and a
    blank line between paragraphs. Parsed incrementally so multi-hundred-MB
    documents do not have to be held in memory.
    """
    paragraphs: list[str] = []
    lines: list[str] = []
    chars: list[str] = []

    def flush_line() -> None:
        if chars:
            lines.append("".join(chars))
            chars.clear()

    def flush_paragraph() -> None:
        flush_line()
        if lines:
            paragraphs.append("\n".join(lines))
            lines.clear()

    for _event, el in ET.iterparse(fileobj, events=("end",)):
        tag = _local_name(el.tag)
        if tag == "charParams":
            if el.get("wordStart") == "true" and chars and chars[-1] != " ":
                chars.append(" ")
            chars.append(el.text or "")
            el.clear()
        elif tag == "line":
            flush_line()
            el.clear()
        elif tag == "par":
            flush_paragraph()
            el.clear()
        elif tag == "page":
            flush_paragraph()
            el.clear()

    flush_paragraph()
    return "\n\n".join(par for par in paragraphs if par.strip())


def extract_text_from_file(file_path: Path) -> str:
    """Extract text from various formats."""
    if file_path.suffix == ".zip":
        # Try to extract _txt.zip
        try:
            with zipfile.ZipFile(file_path) as zf:
                # Find any .txt file inside
                txt_files = [f for f in zf.namelist() if f.endswith('.txt')]
                if txt_files:
                    return zf.read(txt_files[0]).decode('utf-8', errors='replace')
        except Exception:
            pass

    elif file_path.suffix == ".txt":
        # Plain text file
        try:
            with open(file_path, encoding='utf-8', errors='replace') as f:
                return f.read()
        except Exception:
            pass

    elif file_path.suffix == ".gz":
        # IA `_abbyy.gz` is FineReader layout XML, not plain text. Detect it and
        # reconstruct the text from <charParams>; only fall back to the raw
        # decompressed bytes when the payload is not ABBYY XML.
        try:
            with gzip.open(file_path, "rb") as f:
                head = f.read(4096)
            is_abbyy = b"FineReader" in head or b"<charParams" in head or b"<document" in head
            with gzip.open(file_path, "rb") as f:
                if is_abbyy:
                    return extract_abbyy_text(f)
                return f.read().decode("utf-8", errors="replace")
        except Exception:
            pass

    return ""


def load_versions(path: Path) -> dict[str, dict[str, Any]]:
    """Load version metadata, indexed by source_id."""
    versions = {}
    with open(path) as f:
        for line in f:
            obj = json.loads(line)
            if obj.get('source') == 'internet_archive' and \
               obj.get('acquisition_method') == 'internet_archive_api_discovery':
                versions[obj['source_id']] = obj
    return versions


def load_ocr_scores(path: Path) -> dict[str, dict[str, Any]]:
    """Load OCR scores indexed by source_id."""
    scores = {}
    if not path.exists():
        return scores
    with open(path) as f:
        for line in f:
            obj = json.loads(line)
            scores[obj["source_id"]] = obj
    return scores


def find_text_file(identifier: str, raw_dir: Path) -> Path | None:
    """Find the text file for a given IA identifier."""
    work_dir = raw_dir / identifier
    if not work_dir.exists():
        return None

    # Try different file patterns
    for pattern in [f"{identifier}_txt.zip", f"{identifier}_djvu.txt", f"{identifier}_abbyy.gz"]:
        candidate = work_dir / pattern
        if candidate.exists():
            return candidate

    # Fallback: any text-like file
    for f in work_dir.glob("*.txt"):
        return f
    for f in work_dir.glob("*.zip"):
        return f

    return None


def normalize_file(
    identifier: str,
    raw_dir: Path,
    version_metadata: dict,
    ocr_scores: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    """Normalize a single IA file."""
    ocr_score = ocr_scores.get(identifier)
    if ocr_score and ocr_score.get("ocr_quality_class") == "reject":
        return None

    text_path = find_text_file(identifier, raw_dir)
    if not text_path:
        return None

    text = extract_text_from_file(text_path)
    if not text or len(text) < 100:
        return None

    # Clean and normalize
    text = clean_text(text)
    text = normalize_unicode(text)

    # Create record
    work_id = version_metadata['work_id']
    version_id = version_metadata['version_id']

    ocr_class = ocr_score.get("ocr_quality_class") if ocr_score else None
    record = {
        'doc_id': f"{version_id}__full_text",
        'work_id': work_id,
        'version_id': version_id,
        'title': version_metadata['title'],
        'author': version_metadata['author'],
        'language': 'en',
        'source': 'internet_archive',
        'source_id': identifier,
        'source_url': version_metadata['source_url'],
        'license_status': 'public_domain',
        'quality_tier': 'tier_4_ocr_expansion' if ocr_class == 'ocr_bronze' else 'tier_1_canonical_primary',
        'ocr_quality_score': ocr_score.get("ocr_quality_score") if ocr_score else None,
        'ocr_quality_class': ocr_class,
        'training_eligibility': 'retrieval_only' if ocr_class == 'ocr_bronze' else 'training_candidate',
        'acquisition_method': 'internet_archive_api_discovery',
        'character_count': len(text),
        'text': text,
    }

    return record


def main():
    parser = argparse.ArgumentParser(description="Normalize IA-resolved texts to JSONL.")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help=f"Raw IA directory. Default: {DEFAULT_RAW_DIR}",
    )
    parser.add_argument(
        "--versions",
        type=Path,
        default=DEFAULT_VERSIONS_MANIFEST,
        help=f"Versions manifest. Default: {DEFAULT_VERSIONS_MANIFEST}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output JSONL. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--ocr-scores",
        type=Path,
        default=DEFAULT_OCR_SCORES,
        help=f"OCR quality scores JSONL. Default: {DEFAULT_OCR_SCORES}",
    )

    args = parser.parse_args()

    if not args.raw_dir.exists():
        print(f"Error: {args.raw_dir} not found")
        return 1

    # Load version metadata
    versions = load_versions(args.versions)
    ocr_scores = load_ocr_scores(args.ocr_scores)
    print(f"Loaded {len(versions)} version records for IA-resolved sources")
    print(f"Loaded {len(ocr_scores)} OCR quality scores")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    successful = 0
    skipped = 0

    with open(args.output, 'w') as out:
        for i, (source_id, version_meta) in enumerate(sorted(versions.items())):
            record = normalize_file(source_id, args.raw_dir, version_meta, ocr_scores)

            if record:
                out.write(json.dumps(record) + '\n')
                successful += 1
                if (i + 1) % 20 == 0:
                    print(f"  [{i+1}/{len(versions)}] ✓ {record['work_id']}")
            else:
                skipped += 1

    print(f"\nNormalization complete")
    print(f"  Successful: {successful}")
    print(f"  Skipped: {skipped}")
    print(f"  Output: {args.output}")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
