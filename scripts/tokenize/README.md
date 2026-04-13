# Tokenize Scripts

Tokenization scripts should compute token counts using the target training tokenizer.

Record:

- Target family, backend, model id, and processor revision
- Tokenizer name and version
- Context-length assumption and plain-text/chat-template tokenization mode
- Token count per document
- Token count per work
- Token count per author
- Token count per period
- Token count per language
- Token count per source
- Token count per quality tier

## Count Tokens

`count_tokens.py` reads normalized JSONL records and writes document-level token counts to `corpus/reports/token_counts.jsonl` by default. It also writes aggregate counts by author, period, language, source, and quality tier to `corpus/reports/token_counts_summary.json`.

The default target-tokenizer mode uses the Gemma 4 Hugging Face AutoProcessor from `google/gemma-4-E2B-it` and tokenizes plain normalized text with `add_special_tokens=False`:

```sh
python3 scripts/tokenize/count_tokens.py --dry-run
python3 scripts/tokenize/count_tokens.py --model-id google/gemma-4-E2B-it
```

Use a pinned or locally cached processor when needed:

```sh
python3 scripts/tokenize/count_tokens.py --revision <revision> --dry-run
python3 scripts/tokenize/count_tokens.py --local-files-only --dry-run
```

Skip the aggregate JSON summary only when another reporting step will compute it:

```sh
python3 scripts/tokenize/count_tokens.py --no-summary
```

For rough local smoke tests only, use the regex backend:

```sh
python3 scripts/tokenize/count_tokens.py --backend regex --limit 3 --output /tmp/token_counts_sample.jsonl --summary-output /tmp/token_counts_sample_summary.json
```

The legacy `tiktoken` backend is still available for comparison, but it is not the Gemma 4 target-tokenizer count:

```sh
python3 scripts/tokenize/count_tokens.py --backend tiktoken --tokenizer cl100k_base
```

Parquet output requires `pyarrow`:

```sh
python3 scripts/tokenize/count_tokens.py --write-parquet
```
