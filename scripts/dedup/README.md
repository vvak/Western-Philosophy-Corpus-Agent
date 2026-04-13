# Dedup Scripts

Deduplication scripts should run after normalization.

Use:

- Exact hashes for full documents
- Paragraph hashes
- Near-duplicate methods such as SimHash or MinHash

Never silently delete duplicates. Mark them in reports and move rejected records into `corpus/rejected/duplicate/` when appropriate.

## Project Gutenberg

`dedup_gutenberg.py` reads `corpus/normalized/jsonl/gutenberg.jsonl`, writes the derived deduplicated file to `corpus/normalized/jsonl/gutenberg.deduped.jsonl`, and writes the audit report to `corpus/reports/gutenberg_dedup.md`.

The pass is conservative: it removes only exact full-text duplicate records from the derived output. Same-work clusters, alternate editions, translations, selections, and multi-volume records are retained and reported for manual review.

```sh
python3 scripts/dedup/dedup_gutenberg.py --dry-run
python3 scripts/dedup/dedup_gutenberg.py
```
