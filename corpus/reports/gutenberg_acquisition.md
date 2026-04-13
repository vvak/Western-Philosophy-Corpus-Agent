# Project Gutenberg Acquisition Report

Most recent update: 2026-04-12 (Pass 2 — 15 new records added)

This report validates the raw Project Gutenberg acquisition results under `corpus/raw/gutenberg/` against the high-confidence Project Gutenberg records in `corpus/manifests/versions.jsonl`.

No normalization, deduplication, segmentation, or Project Gutenberg boilerplate removal was performed during acquisition.

## Summary

- Manifest records total: 118
- High-confidence Project Gutenberg records acquired: 89
- Raw Project Gutenberg record directories found: 89
- Metadata sidecars found: 89
- Text files found: 89
- EPUB files found: 89
- Missing expected files or sidecars: 0
- Malformed metadata sidecars: 0
- Failed downloads: 0

## Artifact Status Counts

- `downloaded`: 30 (Pass 2 new acquisitions)
- `skipped_existing`: 148 (Pass 1 artifacts unchanged)
- `failed`: 0

## Byte Counts

- Raw text bytes: 67,376,778
- Raw EPUB bytes: 32,706,540
- Total raw artifact bytes: 100,083,318

## Pass 2 Additions (2026-04-12)

15 new high-confidence records upgraded or added:

**Upgraded from medium to high confidence:**
- `plato_apology_crito_phaedo_cary_pg_13726` — Henry Cary translation
- `aristotle_ethics_pg_8438` — Nicomachean Ethics
- `descartes_six_metaphysical_meditations_pg_70091` — William Molyneux 1680 translation

**New acquisitions:**
- `lucretius_de_rerum_natura_leonard_pg_785` — On the Nature of Things (Leonard)
- `aristotle_poetics_butcher_pg_1974` — Poetics (S.H. Butcher)
- `aristotle_categories_edghill_pg_2412` — Categories (E.M. Edghill)
- `seneca_morals_lestrange_pg_56075` — Morals (Sir Roger L'Estrange)
- `kierkegaard_selections_hollander_pg_60333` — Selections (Lee M. Hollander)
- `plato_phaedrus_jowett_pg_1636`
- `plato_gorgias_jowett_pg_1672`
- `plato_timaeus_jowett_pg_1572`
- `plato_laws_jowett_pg_1750`
- `plato_theaetetus_jowett_pg_1726`
- `plato_protagoras_jowett_pg_1591`
- `plato_parmenides_jowett_pg_1687`

## Metadata Coverage

Every high-confidence Project Gutenberg manifest record has:

- A record directory named `pg_<source_id>_<version_id>`
- A `metadata.json` sidecar
- A raw `<version_id>.txt` file
- A raw `<version_id>.epub` file
- Sidecar `version_id`, `source_id`, `source_url`, `license_rationale`, and manifest record metadata
- Artifact entries for both `txt` and `epub`

## Validation Result

Acquisition is complete for all 89 current high-confidence Project Gutenberg manifest records. No failed artifacts. No missing files or metadata sidecars.
