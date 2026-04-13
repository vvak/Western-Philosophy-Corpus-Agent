# Normalize Scripts

Normalization scripts convert raw artifacts into structured JSONL while preserving provenance.

Required behavior:

- Normalize UTF-8 and Unicode
- Remove source boilerplate where appropriate
- Preserve translator/editor/source metadata
- Segment by work, book, chapter, section, or similar hierarchy
- Write normalized JSONL without overwriting raw text

## Project Gutenberg

`normalize_gutenberg.py` reads acquired text artifacts and metadata sidecars from `corpus/raw/gutenberg/`, removes Project Gutenberg header/footer boilerplate, and writes one full-text JSONL record per high-confidence Project Gutenberg version to `corpus/normalized/jsonl/gutenberg.jsonl`.

```sh
python3 scripts/normalize/normalize_gutenberg.py --dry-run
python3 scripts/normalize/normalize_gutenberg.py
```

Smoke-test a subset without replacing the full output:

```sh
python3 scripts/normalize/normalize_gutenberg.py --limit 3 --output /tmp/gutenberg_sample.jsonl
```
