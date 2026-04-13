# Ingest Scripts

Source-specific ingestors belong here.

Start with:

1. Project Gutenberg catalog resolver
2. Standard Ebooks catalog resolver
3. Internet Archive metadata resolver
4. HathiTrust discovery resolver

Do not download bulk OCR until manifest and rejection reports are working.

## Project Gutenberg Acquisition

`acquire_gutenberg.py` downloads only high-confidence Project Gutenberg records from `corpus/manifests/versions.jsonl`. It preserves raw artifacts under `corpus/raw/gutenberg/` and writes a `metadata.json` sidecar per version in download mode.

Dry-run is the default:

```sh
python3 scripts/ingest/acquire_gutenberg.py
```

Download plain text and EPUB artifacts explicitly:

```sh
python3 scripts/ingest/acquire_gutenberg.py --download
```

Useful smoke-test options:

```sh
python3 scripts/ingest/acquire_gutenberg.py --limit 3
python3 scripts/ingest/acquire_gutenberg.py --download --limit 1 --formats txt
```
