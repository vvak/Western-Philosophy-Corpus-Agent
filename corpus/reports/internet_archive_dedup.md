# Project Gutenberg Deduplication Report

Validation date: 2026-04-12

This report validates and records the conservative deduplication pass for `corpus/normalized/jsonl/gutenberg.jsonl`. The original normalized file was left unchanged.

## Summary

- Input path: `corpus/normalized/jsonl/internet_archive.jsonl`
- Deduped output path: `corpus/normalized/jsonl/internet_archive.deduped.jsonl`
- Input records: 13
- Output records: 13
- Exact full-text duplicate groups: 0
- Exact full-text duplicate records removed from derived output: 0
- Canonical whitespace/case duplicate groups retained for review: 0
- Same-work alternate or multi-record clusters retained for review: 2
- Removal policy: only exact full-text duplicate records are excluded from the derived output.
- Alternate editions, alternate translations, subsets, and multi-volume records are retained.

## Output Validation

- Output JSONL records parsed: 13
- Unique `doc_id` values: 13
- Unique `version_id` values: 13
- Exact duplicate hash groups in output: 0
- Records with `deduplication` metadata: 13

## Exact Full-Text Duplicates

None. No exact normalized text duplicates were found.

## Canonical Whitespace/Case Duplicate Review

None. No additional whitespace/case-only duplicate groups were found.

## Same-Work Clusters Retained

| Work ID | Relation | Records | Max Paragraph Containment | Version IDs |
| --- | --- | ---: | ---: | --- |
| `aquinas_summa_contra_gentiles` | multi_part_or_volume_candidate | 2 | 0.000 | `aquinas_summa_contra_gentiles_vol1_ia_summacontragenti01thomuoft` (Summa Contra Gentiles, Vol. 1, 429,679 chars)<br>`aquinas_summa_contra_gentiles_vol2_ia_summacontragenti02thomuoft` (Summa Contra Gentiles, Vol. 2, 629,543 chars) |
| `hegel_phenomenology_spirit` | multi_part_or_volume_candidate | 2 | 0.001 | `hegel_phenomenology_spirit_vol1_baillie_ia_cu31924097557171` (The Phenomenology of Mind, Vol. 1, 818,873 chars)<br>`hegel_phenomenology_spirit_vol2_baillie_ia_phenomenologyofm02hege` (The Phenomenology of Mind, Vol. 2, 680,610 chars) |

## Notes

- The deduped file is a derived artifact; `corpus/normalized/jsonl/gutenberg.jsonl` remains the source of truth.
- This pass does not normalize, segment, boilerplate-strip, or remove near-duplicates.
- Same-work clusters should be reviewed before training weights are assigned, especially where Project Gutenberg records represent volumes, parts, selections, or alternate translations.
