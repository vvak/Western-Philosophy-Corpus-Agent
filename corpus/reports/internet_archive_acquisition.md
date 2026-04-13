# Internet Archive Acquisition Report

Most recent update: 2026-04-12 (Pass 3)

This report documents the Internet Archive acquisition pass targeting Tier 1 canonical works absent from Project Gutenberg.

## Summary

- Manifest records (internet_archive, high-confidence): 13
- Raw artifact directories created: 13
- Metadata sidecars created: 13
- DjVu plain-text files downloaded: 13
- Failed downloads: 0
- Total raw text bytes: 11,576,792

## Artifact Status

All 13 records: `downloaded` (Pass 3)

## Byte Counts

| Version ID | Bytes |
|---|---:|
| `plotinus_enneads_vol1_mackenna_ia_theenneads01plot` | 357,144 |
| `cicero_de_officiis_gardiner_ia_deofficiis00cice` | 473,390 |
| `aquinas_summa_contra_gentiles_vol1_ia_summacontragenti01thomuoft` | 511,000 |
| `anselm_proslogion_deane_ia_proslogiummonol00deangoog` | 557,588 |
| `aquinas_summa_contra_gentiles_vol2_ia_summacontragenti02thomuoft` | 746,103 |
| `hegel_phenomenology_spirit_vol2_baillie_ia_phenomenologyofm02hege` | 794,849 |
| `hegel_philosophy_right_dyde_ia_cu31924014578979` | 797,551 |
| `bentham_morals_legislation_ia_introductiontopr02bent` | 803,506 |
| `aristotle_metaphysics_ross_ia_workstranslatedi08aris` | 891,324 |
| `hegel_phenomenology_spirit_vol1_baillie_ia_cu31924097557171` | 960,229 |
| `pascal_pensees_trotter_ia_thoughtstrbywftr00pascuoft` | 984,452 |
| `leibniz_monadology_latta_ia_themonadology00leibuoft` | 1,170,479 |
| `marx_capital_vol1_ia_capitalcritiqueo00marx` | 2,529,177 |
| **Total** | **11,576,792** |

## Pass 3 Acquisitions (2026-04-12)

All 13 records are new Internet Archive acquisitions targeting Tier 1 canonical primary works with no Project Gutenberg source:

| Version ID | Work | Translator | IA Identifier | Year |
|---|---|---|---|---|
| `anselm_proslogion_deane_ia_proslogiummonol00deangoog` | Anselm Proslogion + Monologion | S.N. Deane | proslogiummonol00deangoog | 1903 |
| `aquinas_summa_contra_gentiles_vol1_ia_summacontragenti01thomuoft` | Aquinas SCG Vol. 1 | Dominican Fathers | summacontragenti01thomuoft | 1923 |
| `aquinas_summa_contra_gentiles_vol2_ia_summacontragenti02thomuoft` | Aquinas SCG Vol. 2 | Dominican Fathers | summacontragenti02thomuoft | 1924 |
| `aristotle_metaphysics_ross_ia_workstranslatedi08aris` | Aristotle Metaphysics | W.D. Ross | workstranslatedi08aris | 1908 |
| `bentham_morals_legislation_ia_introductiontopr02bent` | Bentham Introduction | — (orig.) | introductiontopr02bent | 1823 |
| `cicero_de_officiis_gardiner_ia_deofficiis00cice` | Cicero De Officiis | G.B. Gardiner | deofficiis00cice | 1899 |
| `hegel_phenomenology_spirit_vol1_baillie_ia_cu31924097557171` | Hegel Phenomenology Vol. 1 | J.B. Baillie | cu31924097557171 | 1910 |
| `hegel_phenomenology_spirit_vol2_baillie_ia_phenomenologyofm02hege` | Hegel Phenomenology Vol. 2 | J.B. Baillie | phenomenologyofm02hege | 1910 |
| `hegel_philosophy_right_dyde_ia_cu31924014578979` | Hegel Philosophy of Right | S.W. Dyde | cu31924014578979 | 1896 |
| `leibniz_monadology_latta_ia_themonadology00leibuoft` | Leibniz Monadology + Discourse | Robert Latta | themonadology00leibuoft | 1898 |
| `marx_capital_vol1_ia_capitalcritiqueo00marx` | Marx Capital Vol. 1 | Moore/Aveling | capitalcritiqueo00marx | 1906 |
| `pascal_pensees_trotter_ia_thoughtstrbywftr00pascuoft` | Pascal Pensées | W.F. Trotter | thoughtstrbywftr00pascuoft | 1910 |
| `plotinus_enneads_vol1_mackenna_ia_theenneads01plot` | Plotinus Enneads Vol. 1 | S. MacKenna | theenneads01plot | 1917 |

## License Basis

All acquisitions are US public domain, established by publication date:
- All source texts published before 1928 (US public domain cutoff as of January 1, 2026)
- Internet Archive rights statements: NOT_IN_COPYRIGHT (Google Books items) or Cornell University Library public domain declaration
- Hegel Philosophy of Right: Dyde 1896 used in place of T.M. Knox 1942 (Knox translation copyrighted through 2038)

## Metadata Coverage

Every Internet Archive manifest record has:
- A record directory named `ia_{source_id}_{version_id}`
- A `metadata.json` sidecar
- A raw `{version_id}.txt` file (DjVu plain text)

## Acquisition Script

`scripts/ingest/acquire_internet_archive.py`
- Downloads `{source_id}_djvu.txt` from `https://archive.org/download/{source_id}/`
- Selects `source=="internet_archive"` AND `resolution_confidence=="high"` manifest records
- Writes to `corpus/raw/internet_archive/ia_{source_id}_{version_id}/`
- Writes `metadata.json` sidecar per record

## Normalization Notes

`scripts/normalize/normalize_internet_archive.py`
- Strips Google Books digitization notice (where present; detected in 1/13 records)
- Collapses multiple internal spaces (OCR column-layout artifact)
- NFC Unicode normalization
- No segmentation; full text per version record
- Output: `corpus/normalized/jsonl/internet_archive.jsonl` (13 records, ~10.0M chars)
- Deduped: `corpus/normalized/jsonl/internet_archive.deduped.jsonl` (13 records; 0 exact duplicates removed)

## Validation Result

All 13 high-confidence Internet Archive records acquired. No failed artifacts. No missing files or metadata sidecars.
