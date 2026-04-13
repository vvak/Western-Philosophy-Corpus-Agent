# End-to-End Process

This file documents how to run the Western Philosophy Corpus Agent and how the corpus-building process should work from start to finish.

## How To Run The Agent

The current agent is an operating spec, not a standalone executable program.

Start a Codex or LLM-agent session in the project directory:

```bash
cd /Users/vlad/projects/western-philosophy-corpus
```

Then give the agent this instruction:

```text
Use agents/western-philosophy-corpus-agent.md as your operating spec.

Start with the current manifests and scripts. Validate the Project Gutenberg acquisition results under corpus/raw/gutenberg/. Count downloaded, skipped, and failed artifacts; verify every high-confidence Project Gutenberg record has expected raw files and metadata.json sidecars; then write corpus/reports/gutenberg_acquisition.md. Do not normalize, deduplicate, or remove boilerplate yet.
```

For the next implementation step after acquisition validation, use a narrower prompt:

```text
Use agents/western-philosophy-corpus-agent.md as your operating spec.

Implement a Project Gutenberg normalizer for raw files under corpus/raw/gutenberg/. Preserve raw files exactly as downloaded, remove Project Gutenberg boilerplate only in normalized outputs, keep metadata from each metadata.json sidecar, and write normalized JSONL under corpus/normalized/jsonl/. Start with a small smoke test and write corpus/reports/gutenberg_normalization.md. Do not deduplicate yet.
```

The mental model is:

- `agents/western-philosophy-corpus-agent.md` is the agent's operating constitution.
- `corpus/manifests/` is the agent's working memory.
- `corpus/reports/` is the audit trail.
- `scripts/` is where repeatable commands should be added as the workflow matures.

## Current Project State

The project currently has:

- A main README describing the corpus goal and manifest-first design.
- An agent spec in `agents/western-philosophy-corpus-agent.md`.
- A source policy in `corpus/manifests/sources.yaml`.
- A license policy in `corpus/manifests/licenses.yaml`.
- A period-grouped author seed in `corpus/manifests/authors.yaml`.
- A work manifest in `corpus/manifests/works.jsonl`.
- A version manifest in `corpus/manifests/versions.jsonl`.
- Report templates and source-resolution notes in `corpus/reports/`.

**Current corpus size: 123 documents, 21.8M Gemma 4 tokens (Pass 4, 2026-04-12).**

Sources acquired:
- `corpus/raw/gutenberg/`: 89 high-confidence PG records
- `corpus/raw/internet_archive/`: 13 high-confidence IA records
- `corpus/raw/standard_ebooks/`: 21 high-confidence SE records

Normalized outputs:
- `corpus/normalized/jsonl/gutenberg.jsonl` → `gutenberg.deduped.jsonl` (89 docs)
- `corpus/normalized/jsonl/internet_archive.jsonl` → `internet_archive.deduped.jsonl` (13 docs)
- `corpus/normalized/jsonl/standard_ebooks.jsonl` → `standard_ebooks.deduped.jsonl` (21 docs)

Token count outputs:
- `corpus/reports/token_counts.jsonl` and `token_counts_summary.json` (Gutenberg)
- `corpus/reports/internet_archive_token_counts.jsonl` and `internet_archive_token_counts_summary.json` (IA)
- `corpus/reports/standard_ebooks_token_counts.jsonl` and `standard_ebooks_token_counts_summary.json` (SE)

Reports:
- `corpus/reports/gutenberg_acquisition.md`
- `corpus/reports/gutenberg_normalization.md`
- `corpus/reports/gutenberg_dedup.md`
- `corpus/reports/gutenberg_tokenization.md`
- `corpus/reports/internet_archive_acquisition.md`
- `corpus/reports/internet_archive_dedup.md`
- `corpus/reports/internet_archive_tokenization.md`
- `corpus/reports/standard_ebooks_acquisition.md`
- `corpus/reports/standard_ebooks_normalization.md`
- `corpus/reports/standard_ebooks_dedup.md`
- `corpus/reports/standard_ebooks_tokenization.md`
- `corpus/reports/coverage_gaps.md`
- `corpus/reports/source_resolution.md`

Scripts:
- `scripts/ingest/acquire_gutenberg.py`
- `scripts/ingest/acquire_internet_archive.py`
- `scripts/ingest/acquire_standard_ebooks.py`
- `scripts/normalize/normalize_gutenberg.py`
- `scripts/normalize/normalize_internet_archive.py`
- `scripts/normalize/normalize_standard_ebooks.py`
- `scripts/dedup/dedup_gutenberg.py`
- `scripts/dedup/dedup_standard_ebooks.py`
- `scripts/tokenize/count_tokens.py`

Important caveat: Project Gutenberg catalog release dates are ebook release dates, not original print publication dates. The version records therefore keep edition review in the license rationale instead of treating catalog dates as final legal clearance.

Standard Ebooks EPUB download requires `?source=download` appended to the URL; without it the server returns an HTML redirect page instead of the binary EPUB.

## Done So Far

1. Created the project scaffold in `/Users/vlad/projects/western-philosophy-corpus`.

2. Added the main project documentation:

- `README.md`
- `PROCESS.md`
- `agents/western-philosophy-corpus-agent.md`

3. Defined the corpus scope:

- Western philosophy only for the first build.
- Public-domain-first source policy.
- Modern copyrighted works excluded unless separately licensed or reviewed.
- Wikipedia timeline used only as an author discovery index, not as corpus text.

4. Added the working project structure:

```text
corpus/
  raw/
  normalized/
  rejected/
  manifests/
  reports/
scripts/
  ingest/
  normalize/
  dedup/
  tokenize/
  audit/
agents/
```

5. Added source and license policy manifests:

- `corpus/manifests/sources.yaml`
- `corpus/manifests/licenses.yaml`

6. Added initial discovery manifests:

- `corpus/manifests/authors.yaml`, with 137 philosophers grouped by period.
- `corpus/manifests/works.jsonl`, initially seeded with high-priority Western philosophy works.

7. Performed the first Project Gutenberg source-resolution pass:

- Used Project Gutenberg's official CSV catalog rather than crawling pages.
- Resolved high-confidence Project Gutenberg records.
- Split adjacent Cicero and Hegel discoveries into their own work IDs.
- Updated `corpus/manifests/works.jsonl` to 83 work records.
- Replaced the placeholder `corpus/manifests/versions.jsonl` with 77 Project Gutenberg version records.
- Added `corpus/reports/source_resolution.md`.

8. Added report placeholders:

- `corpus/reports/coverage_gaps.md`
- `corpus/reports/license_summary.md`
- `corpus/reports/source_quality.md`
- `corpus/reports/token_counts.parquet.README.md`

9. Added script placeholders:

- `scripts/ingest/README.md`
- `scripts/normalize/README.md`
- `scripts/dedup/README.md`
- `scripts/tokenize/README.md`
- `scripts/audit/README.md`

10. Implemented the first runnable acquisition script:

- `scripts/ingest/acquire_gutenberg.py`
- Default mode: dry-run.
- Real acquisition mode: `--download`.
- Supported formats: TXT and EPUB.
- Output path: `corpus/raw/gutenberg/`.
- Metadata sidecars: one `metadata.json` per downloaded Gutenberg version.
- Scope: high-confidence Project Gutenberg version records only.

11. Smoke-tested the acquisition script in dry-run mode:

```bash
cd /Users/vlad/projects/western-philosophy-corpus
python3 scripts/ingest/acquire_gutenberg.py --dry-run --limit 3
```

The dry-run selected three Project Gutenberg records and planned six raw artifacts: TXT and EPUB for each selected version.

12. Completed Pass 1 and Pass 2 Gutenberg acquisitions (89 records), normalization, deduplication, and tokenization. Reports: `gutenberg_acquisition.md`, `gutenberg_normalization.md`, `gutenberg_dedup.md`, `gutenberg_tokenization.md`. Token total: 15.1M.

13. Completed Pass 3 Internet Archive acquisitions (13 records), normalization, deduplication, and tokenization. Script: `scripts/ingest/acquire_internet_archive.py`, `scripts/normalize/normalize_internet_archive.py`. Reports: `internet_archive_acquisition.md`, `internet_archive_dedup.md`, `internet_archive_tokenization.md`. Token total: 2.5M.

14. Completed Pass 4 Standard Ebooks acquisitions (21 records), normalization, deduplication, and tokenization:

- `scripts/ingest/acquire_standard_ebooks.py` — downloads EPUB for each high-confidence SE record using `?source=download` query parameter.
- `scripts/normalize/normalize_standard_ebooks.py` — extracts text from EPUB spine (skipping titlepage, imprint, halftitlepage, colophon, uncopyright).
- `scripts/dedup/dedup_standard_ebooks.py` — conservative dedup; 0 exact duplicates; cross-source overlaps flagged in report.
- Token count script (`count_tokens.py`) updated with AutoTokenizer fallback when AutoProcessor requires PyTorch.
- Reports: `standard_ebooks_acquisition.md`, `standard_ebooks_normalization.md`, `standard_ebooks_dedup.md`, `standard_ebooks_tokenization.md`.
- SE token total: 4.2M. Combined corpus after Pass 4: 123 docs, 21.8M tokens.

## End-to-End Workflow

### 1. Discovery

Build a candidate list of Western philosophers and works.

Inputs:

- `corpus/manifests/authors.yaml`
- `corpus/manifests/works.jsonl`
- The Wikipedia timeline of Western philosophers as a discovery index only

Rules:

- Do not use Wikipedia text as corpus content.
- Do not add a work without enough information to search for source-specific versions.
- Keep primary works and secondary/commentarial works distinct.

### 2. Source Resolution

Resolve abstract works into concrete versions.

Example:

```text
Work: Plato, The Republic
Version: Project Gutenberg ebook 1497, Jowett translation
```

Required fields for a version:

- `version_id`
- `work_id`
- `source`
- `source_id`
- `source_url`
- `title`
- `author_metadata`
- `translator`
- `language`
- `license_status`
- `license_rationale`
- `acquisition_method`
- `resolution_confidence`

Current source-resolution order:

1. Project Gutenberg
2. Standard Ebooks
3. Internet Archive
4. HathiTrust
5. Perseus or other classical repositories with clear licensing

Status:

- Project Gutenberg pass is complete for the current seed set.
- Standard Ebooks resolution is the next clean-source pass.
- Internet Archive, HathiTrust, and Perseus should come after clean ebook sources.

### 3. Acquisition Planning

Use `versions.jsonl` as the download plan.

Before writing an acquisition script, decide:

- Which source it handles.
- Whether it supports dry-run mode.
- Where raw files are stored.
- How it logs success/failure.
- Whether it should skip already-downloaded files.

For Project Gutenberg, raw files should go under:

```text
corpus/raw/gutenberg/
```

Do not download OCR-heavy sources until the rejection and quality reports exist.

### 4. Raw Acquisition

Download raw artifacts only for version records that pass the license/source gate.

Rules:

- Preserve raw files exactly as downloaded.
- Do not edit raw files in place.
- Keep source IDs in filenames or adjacent metadata.
- Log failed downloads.
- Avoid re-downloading files that already exist unless explicitly requested.

### 5. Normalization

Convert raw artifacts into normalized text records.

Inputs may include:

- TXT
- EPUB
- HTML
- XML
- OCR text

Outputs should go under:

```text
corpus/normalized/jsonl/
corpus/normalized/text/
```

Normalization should:

- Convert to UTF-8.
- Normalize Unicode.
- Remove source boilerplate where appropriate.
- Preserve author, translator, editor, source, and license metadata.
- Segment by work, book, chapter, section, or other meaningful hierarchy.
- Avoid mixing different translations or editions.

### 6. Deduplication And Rejection

Run deduplication and quality checks after normalization.

Use:

- Exact file/document hashes.
- Paragraph-level hashes.
- Near-duplicate methods such as SimHash or MinHash.
- OCR quality checks for scanned sources.

Rejected or down-ranked texts should go under explicit folders:

```text
corpus/rejected/license_unclear/
corpus/rejected/modern_copyright/
corpus/rejected/low_quality_ocr/
corpus/rejected/duplicate/
```

Do not silently delete rejected material unless the user asks for cleanup.

### 7. Tokenization

Tokenize normalized text with the target model tokenizer.

Record:

- Tokenizer name and version.
- Token counts by document.
- Token counts by work.
- Token counts by author.
- Token counts by period.
- Token counts by source.
- Token counts by quality tier.

The future generated output should be:

```text
corpus/reports/token_counts.parquet
```

### 8. Reporting

Keep reports human-readable and machine-checkable where possible.

Required reports:

- `corpus/reports/source_resolution.md`
- `corpus/reports/license_summary.md`
- `corpus/reports/source_quality.md`
- `corpus/reports/coverage_gaps.md`
- Duplicate cluster report
- OCR rejection report
- Token count report

Reports should answer:

- What was accepted?
- What was rejected?
- Why was it rejected?
- Which authors and periods are undercovered?
- Which sources have the highest quality?
- Which works need manual review?

### 9. Training Preparation

Do not flatten the corpus into one uniform text pile.

Preserve quality tiers:

- `tier_1_canonical_primary`
- `tier_2_major_primary`
- `tier_3_secondary`
- `tier_4_ocr_expansion`

Training should use sampling weights, with high-quality canonical primary texts weighted more heavily than OCR expansion material.

Canonical primary works alone probably produce hundreds of millions of tokens, not 10B tokens. To approach 10B tokens, the project must expand into public-domain commentaries, histories, journals, collected works, and large public-domain OCR sources after the clean-source workflow is stable.
