# Standard Ebooks Deduplication Report

Validation date: 2026-04-12

This report validates and records the conservative deduplication pass for `corpus/normalized/jsonl/standard_ebooks.jsonl`. The original normalized file was left unchanged.

## Summary

- Input path: `corpus/normalized/jsonl/standard_ebooks.jsonl`
- Deduped output path: `corpus/normalized/jsonl/standard_ebooks.deduped.jsonl`
- Input records: 21
- Output records: 21
- Exact full-text duplicate groups: 0
- Exact full-text duplicate records removed from derived output: 0
- Canonical whitespace/case duplicate groups retained for review: 0
- Same-work alternate or multi-record clusters retained for review: 0
- Removal policy: only exact full-text duplicate records are excluded from the derived output.
- Alternate editions, alternate translations, subsets, and multi-volume records are retained.

## Output Validation

- Output JSONL records parsed: 21
- Unique `doc_id` values: 21
- Unique `version_id` values: 21
- Exact duplicate hash groups in output: 0
- Records with `deduplication` metadata: 21

## Exact Full-Text Duplicates

None. No exact normalized text duplicates were found.

## Canonical Whitespace/Case Duplicate Review

None. No additional whitespace/case-only duplicate groups were found.

## Same-Work Clusters Retained

None.

## Cross-Source Notes

Several Standard Ebooks versions share work_ids with existing Project Gutenberg records. These are not flagged as exact duplicates here because they were normalized from different source files and the text may differ (different typo corrections, metadata normalization, etc.). Training data preparation should apply version selection or down-weighting for same-work cross-source records.

The `plato_dialogues_jowett_se` record is a large collection that contains the full text of many dialogs also present individually in Gutenberg records. This collection record should be treated as a superset and weighted carefully relative to individual dialog records.

## Notes

- The deduped file is a derived artifact; `corpus/normalized/jsonl/standard_ebooks.jsonl` remains the source of truth.
- This pass does not normalize, segment, boilerplate-strip, or remove near-duplicates.
- Same-work clusters should be reviewed before training weights are assigned.
