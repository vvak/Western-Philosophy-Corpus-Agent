#!/usr/bin/env python3
"""Score raw OCR text files before promotion into training data."""

import argparse
import gzip
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

DEFAULT_ROOTS = [
    Path("corpus/raw/internet_archive_resolved"),
    Path("corpus/raw/lane_b_pilot"),
    Path("corpus/raw/lane_b_cleaned"),
    Path("corpus/raw/lane_b_recovered"),
]
DEFAULT_OUTPUT = Path("corpus/reports/ocr_quality_scores.jsonl")
DEFAULT_SUMMARY = Path("corpus/reports/ocr_quality_scores.md")

COMMON_WORDS = {
    "the", "and", "of", "to", "in", "that", "is", "it", "for", "as", "with",
    "was", "not", "be", "by", "on", "this", "which", "or", "from", "are",
    "his", "have", "at", "but", "all", "one", "their", "more", "an", "he",
    "were", "we", "has", "there", "can", "what", "when", "so", "if",
}


def iter_text_files(roots: list[Path]) -> list[Path]:
    files = []
    for root in roots:
        if not root.exists():
            continue
        txt = [
            p for p in root.rglob("*")
            if p.is_file() and (p.suffix == ".txt" or p.name.endswith("_text.txt"))
        ]
        # IA items sometimes ship only `_abbyy.gz` (FineReader XML) with no plain
        # text. Score those too, but only when the directory has no .txt sibling,
        # so a single work is never scored twice.
        txt_dirs = {p.parent for p in txt}
        abbyy = [
            p for p in root.rglob("*_abbyy.gz")
            if p.is_file() and p.parent not in txt_dirs
        ]
        files.extend(txt)
        files.extend(abbyy)
    return sorted(files)


def _local_name(tag: str) -> str:
    """Strip an XML namespace, returning the local element name."""
    return tag.rsplit("}", 1)[-1]


def extract_abbyy_text(fileobj) -> str:
    """Reconstruct plain text from an ABBYY FineReader XML stream.

    Mirrors the extractor in ``scripts/normalize/normalize_ia_resolved.py`` so
    the gate scores the same text that normalization will emit: one glyph per
    ``<charParams>``, grouped by ``<line>`` / ``<par>`` / ``<page>``, with word
    breaks flagged by ``wordStart``.
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
        elif tag in ("par", "page"):
            flush_paragraph()
            el.clear()

    flush_paragraph()
    return "\n\n".join(par for par in paragraphs if par.strip())


def read_document_text(path: Path) -> str:
    """Read a file for scoring, extracting text from ABBYY `_abbyy.gz` payloads."""
    if path.suffix == ".gz":
        try:
            with gzip.open(path, "rb") as handle:
                head = handle.read(4096)
            is_abbyy = b"FineReader" in head or b"<charParams" in head or b"<document" in head
            with gzip.open(path, "rb") as handle:
                if is_abbyy:
                    return extract_abbyy_text(handle)
                return handle.read().decode("utf-8", errors="replace")
        except Exception:
            return ""
    return path.read_text(encoding="utf-8", errors="replace")


def score_text(text: str) -> dict:
    sample = text[:250_000]
    chars = len(text)
    printable = sum(1 for c in sample if c.isprintable() or c in "\n\t\r")
    alpha = sum(1 for c in sample if c.isalpha())
    weird = sum(1 for c in sample if not (c.isalnum() or c.isspace() or c in ".,;:'\"!?()-[]{}_/&%$#@*+=<>"))
    tokens = re.findall(r"[A-Za-z]{2,}", sample.lower())
    long_tokens = sum(1 for t in tokens if len(t) > 24)
    common_hits = sum(1 for t in tokens if t in COMMON_WORDS)
    hyphen_breaks = len(re.findall(r"[A-Za-z]-\n[A-Za-z]", sample))
    line_count = max(1, sample.count("\n") + 1)
    short_lines = sum(1 for line in sample.splitlines() if 0 < len(line.strip()) < 4)

    printable_ratio = printable / max(1, len(sample))
    alpha_ratio = alpha / max(1, len(sample))
    weird_ratio = weird / max(1, len(sample))
    long_token_ratio = long_tokens / max(1, len(tokens))
    common_word_ratio = common_hits / max(1, len(tokens))
    hyphen_break_rate = hyphen_breaks / max(1, line_count)
    short_line_ratio = short_lines / line_count

    raw = 100
    raw -= max(0, 0.97 - printable_ratio) * 160
    raw -= max(0, 0.45 - alpha_ratio) * 120
    raw -= weird_ratio * 500
    raw -= long_token_ratio * 400
    raw -= max(0, 0.08 - common_word_ratio) * 250
    raw -= hyphen_break_rate * 60
    raw -= short_line_ratio * 40
    raw -= 25 if chars < 5_000 else 0
    score = max(0, min(100, round(raw, 2)))

    if score >= 85:
        label = "ocr_gold"
    elif score >= 70:
        label = "ocr_silver"
    elif score >= 50:
        label = "ocr_bronze"
    else:
        label = "reject"

    return {
        "char_count": chars,
        "sample_char_count": len(sample),
        "printable_ratio": round(printable_ratio, 4),
        "alpha_ratio": round(alpha_ratio, 4),
        "weird_char_ratio": round(weird_ratio, 4),
        "long_token_ratio": round(long_token_ratio, 4),
        "common_word_ratio": round(common_word_ratio, 4),
        "hyphen_break_rate": round(hyphen_break_rate, 4),
        "short_line_ratio": round(short_line_ratio, 4),
        "ocr_quality_score": score,
        "ocr_quality_class": label,
    }


def write_summary(path: Path, records: list[dict]) -> None:
    counts = Counter(r["ocr_quality_class"] for r in records)
    lines = [
        "# OCR Quality Scores",
        "",
        f"- Scored files: {len(records)}",
        f"- ocr_gold: {counts.get('ocr_gold', 0)}",
        f"- ocr_silver: {counts.get('ocr_silver', 0)}",
        f"- ocr_bronze: {counts.get('ocr_bronze', 0)}",
        f"- reject: {counts.get('reject', 0)}",
        "",
        "Generated by `scripts/audit/ocr_quality_score.py`.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("roots", nargs="*", type=Path)
    args = parser.parse_args()

    roots = args.roots or DEFAULT_ROOTS
    records = []
    scored_at = datetime.now(timezone.utc).isoformat()
    for path in iter_text_files(roots):
        text = read_document_text(path)
        rec = {
            "path": str(path),
            "source_id": path.parent.name,
            "scored_at_utc": scored_at,
            **score_text(text),
        }
        records.append(rec)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(json.dumps(r, sort_keys=True) for r in records) + ("\n" if records else ""), encoding="utf-8")
    write_summary(args.summary, records)
    print(json.dumps({"scored": len(records), "output": str(args.output), "summary": str(args.summary)}))


if __name__ == "__main__":
    main()
