# Western Philosophy Corpus Agent

This project defines an agent for building a high-quality, public-domain-first corpus of Western philosophy texts for domain-adaptive LLM training and retrieval.

The goal is not to scrape "everything" at once. The agent should first create a clean, auditable seed corpus from canonical philosophers and public-domain editions, then expand into commentaries, histories, journals, and OCR material only after the metadata and license gates are stable.

## Agent

Primary agent spec:

- [agents/western-philosophy-corpus-agent.md](agents/western-philosophy-corpus-agent.md)

Use that file as the operating prompt for a corpus-building agent. It defines scope, source priority, legal constraints, metadata schema, quality tiers, and the phased acquisition workflow.

Full operating process:

- [PROCESS.md](PROCESS.md)

## Scope

Version 1 focuses on Western philosophy only:

- Ancient Greek and Roman philosophy
- Late antique and medieval Christian, Jewish, and Islamic philosophy where part of the Western philosophical tradition
- Renaissance and early modern philosophy
- German idealism and 19th-century philosophy
- Early 20th-century works that are public domain in the United States
- Public-domain histories, commentaries, lecture series, encyclopedias, and journals as an expansion layer

The Wikipedia page [Timeline of Western philosophers](https://en.wikipedia.org/wiki/Timeline_of_Western_philosophers) should be used as a discovery index for candidate authors, not as a corpus source.

## Source Priority

Start with clean structured or semi-structured sources:

1. Project Gutenberg
2. Standard Ebooks
3. Internet Archive public-domain scans and derived text
4. HathiTrust full-view/public-domain records
5. Perseus or university classics repositories, only where licensing is clear

Modern open-access scholarship is out of scope for the first public-domain corpus unless a later legal review explicitly allows it.

## Public Domain Rule Of Thumb

As of 2026 in the United States, works published in 1930 or earlier are generally public domain. This is only a starting rule. The agent must still track edition, translator, publication year, source terms, and license status per text version.

Translations and editorial apparatus are especially important. A public-domain ancient source text can have a copyrighted modern translation or introduction.

## Suggested Repository Layout

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
agents/
  western-philosophy-corpus-agent.md
```

## First Milestone

Build a seed manifest before downloading at scale:

- 100-300 philosophers or authors
- 500-1,500 candidate public-domain works or editions
- Source URL for each candidate
- Edition and translator metadata where available
- Publication year and public-domain rationale
- Quality tier
- Acquisition method
- Initial token-count estimate

Only after that manifest exists should the agent implement source-specific ingestors.

## How This Works

This project is organized around a manifest-first corpus pipeline.

The agent starts with a discovery list of philosophers and candidate works, then resolves those candidates into specific text versions from approved sources. A "work" is the abstract title, such as Plato's `The Republic`; a "version" is a concrete edition or translation from a particular source, such as a Jowett translation from Project Gutenberg.

This separation matters because philosophy corpora are edition-sensitive. The same work can appear in different translations, revised editions, collected volumes, abridgments, or OCR scans. The corpus should preserve those differences instead of flattening them into one undifferentiated text pile.

The pipeline has six stages:

1. **Discovery**
   Build a candidate list of authors and works from trusted indexes, starting with the Western philosophy timeline as a discovery aid.

2. **Source Resolution**
   Match each candidate work to source-specific versions from Project Gutenberg, Standard Ebooks, Internet Archive, HathiTrust, Perseus, or another approved source. Record translator, editor, publication year, source URL, and license/public-domain rationale.

3. **Acquisition**
   Download raw files only after a version record exists. Raw files stay in `corpus/raw/` and should not be edited directly.

4. **Normalization**
   Convert raw EPUB, TXT, HTML, XML, or OCR text into normalized UTF-8 JSONL. Remove boilerplate where appropriate, preserve metadata, and segment texts by book, chapter, section, or similar structure.

5. **Deduplication And Rejection**
   Run exact and near-duplicate checks. Reject or down-rank unclear licenses, modern copyrighted translations, low-quality OCR, and duplicate editions. Rejections should be explicit and auditable.

6. **Reporting**
   Generate token counts, license summaries, source quality summaries, duplicate clusters, OCR rejection reports, and coverage gaps.

The output should always be traceable. Every normalized text record should point back to a version record, and every version record should point back to a source URL and license rationale.

## Training Corpus Expectation

Canonical primary works alone are unlikely to reach 10B tokens. A realistic staged target is:

- Canonical primary works: tens to hundreds of millions of tokens
- Expanded primary works and multiple languages: hundreds of millions of tokens
- Primary works plus public-domain commentaries and histories: up to low billions of tokens
- Library-scale OCR expansion from public-domain scans: potentially multiple billions of tokens

The corpus should be sampled by quality tier rather than treated as a flat pile of text.
