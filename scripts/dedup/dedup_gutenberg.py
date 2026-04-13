#!/usr/bin/env python3
"""Conservatively deduplicate normalized Project Gutenberg JSONL records.

This pass removes only exact full-text duplicates from the derived output.
Same-work clusters, alternate editions, translations, volumes, and canonical
whitespace/case matches are retained and reported for review.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_INPUT = Path("corpus/normalized/jsonl/gutenberg.jsonl")
DEFAULT_OUTPUT = Path("corpus/normalized/jsonl/gutenberg.deduped.jsonl")
DEFAULT_REPORT = Path("corpus/reports/gutenberg_dedup.md")
DEDUPER_ID = "scripts/dedup/dedup_gutenberg.py"
SPACE_RE = re.compile(r"\s+")
PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n+")
PART_OR_VOLUME_RE = re.compile(r"\b(?:vol\.?|volume|part|book)\b", re.IGNORECASE)
QUALITY_RANK = {
    "tier_1_canonical_primary": 0,
    "tier_2_major_primary": 1,
    "tier_3_secondary": 2,
    "tier_4_ocr_expansion": 3,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Deduplicate normalized Project Gutenberg JSONL conservatively, "
            "preserving the source normalized file."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Normalized JSONL input path. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Deduplicated JSONL output path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help=f"Markdown report output path. Default: {DEFAULT_REPORT}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze deduplication state without writing output or report files.",
    )
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"Input JSONL does not exist: {path}")

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
            if not record.get("version_id"):
                raise SystemExit(f"{path}:{line_number}: missing required version_id")
            if "text" not in record:
                raise SystemExit(f"{path}:{line_number}: missing required text")
            records.append(record)
    return records


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = SPACE_RE.sub(" ", text).strip()
    return text.casefold()


def paragraph_hashes(text: str) -> set[str]:
    hashes: set[str] = set()
    for paragraph in PARAGRAPH_SPLIT_RE.split(text):
        canonical = canonical_text(paragraph)
        if len(canonical) < 80:
            continue
        hashes.add(sha256_text(canonical))
    return hashes


def group_by_hash(records: Iterable[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record[key]].append(record)
    return [
        {"hash": digest, "records": sorted(items, key=record_sort_key)}
        for digest, items in sorted(grouped.items())
        if len(items) > 1
    ]


def record_sort_key(record: dict[str, Any]) -> tuple[int, str, str, str, str]:
    return (
        QUALITY_RANK.get(record.get("quality_tier"), 99),
        str(record.get("author") or ""),
        str(record.get("work_id") or ""),
        str(record.get("source_id") or ""),
        str(record.get("version_id") or ""),
    )


def build_exact_duplicate_decisions(
    exact_duplicate_groups: list[dict[str, Any]],
) -> tuple[dict[str, str], dict[str, list[str]]]:
    rejected_to_keeper: dict[str, str] = {}
    keeper_to_rejected: dict[str, list[str]] = {}
    for group in exact_duplicate_groups:
        keeper = group["records"][0]
        keeper_id = keeper["version_id"]
        rejected_ids = [record["version_id"] for record in group["records"][1:]]
        for rejected_id in rejected_ids:
            rejected_to_keeper[rejected_id] = keeper_id
        keeper_to_rejected[keeper_id] = rejected_ids
    return rejected_to_keeper, keeper_to_rejected


def same_work_clusters(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[(str(record.get("work_id") or ""), str(record.get("language") or ""))].append(record)

    clusters: list[dict[str, Any]] = []
    for (work_id, language), items in sorted(grouped.items()):
        if not work_id or len(items) < 2:
            continue
        sorted_items = sorted(items, key=record_sort_key)
        clusters.append(
            {
                "work_id": work_id,
                "language": language,
                "relation": classify_same_work_cluster(sorted_items),
                "records": sorted_items,
                "max_paragraph_containment": max_paragraph_containment(sorted_items),
            }
        )
    return clusters


def classify_same_work_cluster(records: list[dict[str, Any]]) -> str:
    titles = {canonical_title(record.get("title")) for record in records if record.get("title")}
    translators = {str(record.get("translator") or "") for record in records}
    has_part_or_volume = any(PART_OR_VOLUME_RE.search(str(record.get("title") or "")) for record in records)

    if has_part_or_volume and len(translators) <= 1:
        return "multi_part_or_volume_candidate"
    if has_part_or_volume:
        return "multi_part_or_volume_with_translator_variance"
    if len(translators) > 1:
        return "alternate_translation_or_scope_candidate"
    if len(titles) <= 1:
        return "alternate_edition_candidate"
    return "same_work_alternate_candidate"


def canonical_title(title: Any) -> str:
    return canonical_text(str(title or ""))


def max_paragraph_containment(records: list[dict[str, Any]]) -> float:
    paragraph_sets = [(record["version_id"], paragraph_hashes(record.get("text", ""))) for record in records]
    max_overlap = 0.0
    for index, (_, left) in enumerate(paragraph_sets):
        for _, right in paragraph_sets[index + 1 :]:
            smaller = min(len(left), len(right))
            if not smaller:
                continue
            max_overlap = max(max_overlap, len(left & right) / smaller)
    return max_overlap


def add_hashes(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    annotated: list[dict[str, Any]] = []
    for record in records:
        text = record.get("text", "")
        annotated_record = copy.deepcopy(record)
        annotated_record["_dedup_text_sha256"] = sha256_text(text)
        annotated_record["_dedup_canonical_sha256"] = sha256_text(canonical_text(text))
        annotated_record["_dedup_paragraph_hash_count"] = len(paragraph_hashes(text))
        annotated.append(annotated_record)
    return annotated


def deduplicate(records: list[dict[str, Any]], deduplicated_at_utc: str) -> dict[str, Any]:
    annotated = add_hashes(records)
    exact_groups = group_by_hash(annotated, "_dedup_text_sha256")
    canonical_groups = group_by_hash(annotated, "_dedup_canonical_sha256")
    rejected_to_keeper, keeper_to_rejected = build_exact_duplicate_decisions(exact_groups)
    kept_records = [
        record for record in annotated if record["version_id"] not in rejected_to_keeper
    ]
    clusters = same_work_clusters(kept_records)
    cluster_by_version_id: dict[str, dict[str, Any]] = {}
    for cluster in clusters:
        for record in cluster["records"]:
            cluster_by_version_id[record["version_id"]] = cluster

    output_records: list[dict[str, Any]] = []
    rejected_records: list[dict[str, Any]] = []
    for record in annotated:
        version_id = record["version_id"]
        if version_id in rejected_to_keeper:
            rejected_records.append(record)
            continue

        cluster = cluster_by_version_id.get(version_id)
        output_record = strip_internal_fields(copy.deepcopy(record))
        output_record["deduplication"] = {
            "deduplicated_at_utc": deduplicated_at_utc,
            "deduper": DEDUPER_ID,
            "status": (
                "accepted_exact_duplicate_keeper"
                if version_id in keeper_to_rejected
                else "accepted_unique"
            ),
            "text_sha256": record["_dedup_text_sha256"],
            "canonical_text_sha256": record["_dedup_canonical_sha256"],
            "paragraph_hash_count": record["_dedup_paragraph_hash_count"],
            "exact_duplicate_version_ids": keeper_to_rejected.get(version_id, []),
            "same_work_review": bool(cluster),
            "same_work_relation": cluster["relation"] if cluster else None,
            "same_work_cluster_size": len(cluster["records"]) if cluster else 1,
        }
        output_records.append(output_record)

    return {
        "annotated_records": annotated,
        "output_records": output_records,
        "rejected_records": rejected_records,
        "exact_duplicate_groups": exact_groups,
        "canonical_duplicate_groups": canonical_groups,
        "same_work_clusters": clusters,
        "rejected_to_keeper": rejected_to_keeper,
        "keeper_to_rejected": keeper_to_rejected,
    }


def strip_internal_fields(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if not key.startswith("_dedup_")}


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    temp_path.replace(path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(text, encoding="utf-8")
    temp_path.replace(path)


def validate_output(records: list[dict[str, Any]]) -> dict[str, Any]:
    doc_ids = [record.get("doc_id") for record in records]
    version_ids = [record.get("version_id") for record in records]
    text_hashes = [sha256_text(record.get("text", "")) for record in records]
    return {
        "records": len(records),
        "unique_doc_ids": len(set(doc_ids)),
        "unique_version_ids": len(set(version_ids)),
        "exact_duplicate_hash_groups": len(
            [items for items in group_counts(text_hashes).values() if items > 1]
        ),
        "records_with_dedup_metadata": sum(1 for record in records if "deduplication" in record),
    }


def group_counts(items: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for item in items:
        counts[item] += 1
    return counts


def render_report(
    input_path: Path,
    output_path: Path,
    records: list[dict[str, Any]],
    result: dict[str, Any],
    validation: dict[str, Any],
    generated_at_utc: str,
) -> str:
    output_records = result["output_records"]
    exact_groups = result["exact_duplicate_groups"]
    canonical_groups = result["canonical_duplicate_groups"]
    canonical_review_groups = [
        group
        for group in canonical_groups
        if len({record["_dedup_text_sha256"] for record in group["records"]}) > 1
    ]
    same_work = result["same_work_clusters"]

    lines = [
        "# Project Gutenberg Deduplication Report",
        "",
        f"Validation date: {generated_at_utc[:10]}",
        "",
        (
            "This report validates and records the conservative deduplication pass for "
            "`corpus/normalized/jsonl/gutenberg.jsonl`. The original normalized file was "
            "left unchanged."
        ),
        "",
        "## Summary",
        "",
        f"- Input path: `{input_path}`",
        f"- Deduped output path: `{output_path}`",
        f"- Input records: {len(records)}",
        f"- Output records: {len(output_records)}",
        f"- Exact full-text duplicate groups: {len(exact_groups)}",
        f"- Exact full-text duplicate records removed from derived output: {len(result['rejected_records'])}",
        f"- Canonical whitespace/case duplicate groups retained for review: {len(canonical_review_groups)}",
        f"- Same-work alternate or multi-record clusters retained for review: {len(same_work)}",
        "- Removal policy: only exact full-text duplicate records are excluded from the derived output.",
        "- Alternate editions, alternate translations, subsets, and multi-volume records are retained.",
        "",
        "## Output Validation",
        "",
        f"- Output JSONL records parsed: {validation['records']}",
        f"- Unique `doc_id` values: {validation['unique_doc_ids']}",
        f"- Unique `version_id` values: {validation['unique_version_ids']}",
        f"- Exact duplicate hash groups in output: {validation['exact_duplicate_hash_groups']}",
        f"- Records with `deduplication` metadata: {validation['records_with_dedup_metadata']}",
        "",
        "## Exact Full-Text Duplicates",
        "",
    ]

    if exact_groups:
        lines.extend(
            [
                "| Text SHA256 | Kept Version ID | Removed Version IDs | Work ID | Title |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for group in exact_groups:
            keeper = group["records"][0]
            removed = [record["version_id"] for record in group["records"][1:]]
            lines.append(
                "| "
                + " | ".join(
                    [
                        md(group["hash"][:16]),
                        code(keeper["version_id"]),
                        md(", ".join(code(record_id) for record_id in removed)),
                        code(keeper.get("work_id")),
                        md(keeper.get("title")),
                    ]
                )
                + " |"
            )
    else:
        lines.append("None. No exact normalized text duplicates were found.")

    lines.extend(["", "## Canonical Whitespace/Case Duplicate Review", ""])
    if canonical_review_groups:
        lines.extend(
            [
                "| Canonical SHA256 | Version IDs | Note |",
                "| --- | --- | --- |",
            ]
        )
        for group in canonical_review_groups:
            lines.append(
                "| "
                + " | ".join(
                    [
                        md(group["hash"][:16]),
                        md(", ".join(code(record["version_id"]) for record in group["records"])),
                        "Retained for manual review; not exact full-text duplicates.",
                    ]
                )
                + " |"
            )
    else:
        lines.append("None. No additional whitespace/case-only duplicate groups were found.")

    lines.extend(["", "## Same-Work Clusters Retained", ""])
    if same_work:
        lines.extend(
            [
                "| Work ID | Relation | Records | Max Paragraph Containment | Version IDs |",
                "| --- | --- | ---: | ---: | --- |",
            ]
        )
        for cluster in same_work:
            records_for_cluster = cluster["records"]
            version_list = "<br>".join(
                f"{code(record['version_id'])} ({md(record.get('title'))}, {len(record.get('text', '')):,} chars)"
                for record in records_for_cluster
            )
            lines.append(
                "| "
                + " | ".join(
                    [
                        code(cluster["work_id"]),
                        md(cluster["relation"]),
                        str(len(records_for_cluster)),
                        f"{cluster['max_paragraph_containment']:.3f}",
                        version_list,
                    ]
                )
                + " |"
            )
    else:
        lines.append("None.")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- The deduped file is a derived artifact; `corpus/normalized/jsonl/gutenberg.jsonl` remains the source of truth.",
            "- This pass does not normalize, segment, boilerplate-strip, or remove near-duplicates.",
            "- Same-work clusters should be reviewed before training weights are assigned, especially where Project Gutenberg records represent volumes, parts, selections, or alternate translations.",
            "",
        ]
    )
    return "\n".join(lines)


def code(value: Any) -> str:
    return f"`{md(value)}`"


def md(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def main() -> int:
    args = parse_args()
    if args.input.resolve() == args.output.resolve():
        raise SystemExit("--output must not overwrite --input")

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    records = load_jsonl(args.input)
    result = deduplicate(records, generated_at_utc)
    validation = validate_output(result["output_records"])
    report = render_report(
        args.input,
        args.output,
        records,
        result,
        validation,
        generated_at_utc,
    )

    if args.dry_run:
        print("Dry run only; no deduped JSONL or report files will be written.")
    else:
        write_jsonl(args.output, result["output_records"])
        write_text(args.report, report)

    print(f"Input records: {len(records)}")
    print(f"Output records: {len(result['output_records'])}")
    print(f"Exact full-text duplicate groups: {len(result['exact_duplicate_groups'])}")
    print(f"Exact duplicate records removed from derived output: {len(result['rejected_records'])}")
    print(f"Same-work clusters retained for review: {len(result['same_work_clusters'])}")
    if not args.dry_run:
        print(f"Wrote deduped JSONL to {args.output}.")
        print(f"Wrote report to {args.report}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
