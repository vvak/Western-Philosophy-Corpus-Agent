# Internet Archive Tokenization Report

Validated: 2026-04-12 (Pass 3)

This report validates Gemma 4 token counts for `corpus/normalized/jsonl/internet_archive.deduped.jsonl`.

## Tokenizer

- Model: `google/gemma-4-E2B-it`
- Backend: `huggingface_auto_processor` (HuggingFace AutoProcessor)
- Tokenizer version: `5.5.3`
- `add_special_tokens`: `false`
- `plain_text_tokenization`: `true`
- `chat_template_applied`: `false`

Token counts file: `corpus/reports/internet_archive_token_counts.jsonl`
Summary file: `corpus/reports/internet_archive_token_counts_summary.json`

## Summary

| Metric | Value |
|---|---:|
| Documents | 13 |
| Total tokens | 2,496,817 |
| Total chars | 10,005,355 |
| Avg tokens/doc | 192,063 |

## Token Counts by Document

| Version ID | Author | Title | Period | Quality Tier | Tokens |
|---|---|---|---|---|---:|
| `marx_capital_vol1_ia_capitalcritiqueo00marx` | Karl Marx | Capital: A Critique of Political Economy, Vol. 1 | nineteenth_century | tier_1_canonical_primary | 548,316 |
| `leibniz_monadology_latta_ia_themonadology00leibuoft` | Gottfried Wilhelm Leibniz | The Monadology and Other Philosophical Writings | renaissance_early_modern | tier_1_canonical_primary | 254,267 |
| `pascal_pensees_trotter_ia_thoughtstrbywftr00pascuoft` | Blaise Pascal | Thoughts | renaissance_early_modern | tier_1_canonical_primary | 205,302 |
| `aristotle_metaphysics_ross_ia_workstranslatedi08aris` | Aristotle | The Works of Aristotle, Vol. VIII: Metaphysica | ancient | tier_1_canonical_primary | 204,949 |
| `hegel_phenomenology_spirit_vol1_baillie_ia_cu31924097557171` | Georg Wilhelm Friedrich Hegel | The Phenomenology of Mind, Vol. 1 | nineteenth_century | tier_1_canonical_primary | 189,563 |
| `hegel_philosophy_right_dyde_ia_cu31924014578979` | Georg Wilhelm Friedrich Hegel | Hegel's Philosophy of Right | nineteenth_century | tier_1_canonical_primary | 188,606 |
| `bentham_morals_legislation_ia_introductiontopr02bent` | Jeremy Bentham | An Introduction to the Principles of Morals and Legislation | nineteenth_century | tier_1_canonical_primary | 170,284 |
| `hegel_phenomenology_spirit_vol2_baillie_ia_phenomenologyofm02hege` | Georg Wilhelm Friedrich Hegel | The Phenomenology of Mind, Vol. 2 | nineteenth_century | tier_1_canonical_primary | 152,626 |
| `aquinas_summa_contra_gentiles_vol2_ia_summacontragenti02thomuoft` | Thomas Aquinas | Summa Contra Gentiles, Vol. 2 | medieval | tier_1_canonical_primary | 149,832 |
| `anselm_proslogion_deane_ia_proslogiummonol00deangoog` | Anselm | Proslogium; Monologium; An Appendix | medieval | tier_1_canonical_primary | 138,147 |
| `aquinas_summa_contra_gentiles_vol1_ia_summacontragenti01thomuoft` | Thomas Aquinas | Summa Contra Gentiles, Vol. 1 | medieval | tier_1_canonical_primary | 105,318 |
| `cicero_de_officiis_gardiner_ia_deofficiis00cice` | Cicero | De Officiis | ancient | tier_1_canonical_primary | 102,598 |
| `plotinus_enneads_vol1_mackenna_ia_theenneads01plot` | Plotinus | The Enneads, Vol. 1 (First Ennead) | ancient | tier_1_canonical_primary | 87,009 |
| **Total** | | | | | **2,496,817** |

## Token Counts by Author

| Author | Tokens |
|---|---:|
| Anselm | 138,147 |
| Aristotle | 204,949 |
| Blaise Pascal | 205,302 |
| Cicero | 102,598 |
| Georg Wilhelm Friedrich Hegel | 530,795 |
| Gottfried Wilhelm Leibniz | 254,267 |
| Jeremy Bentham | 170,284 |
| Karl Marx | 548,316 |
| Plotinus | 87,009 |
| Thomas Aquinas | 255,150 |

## Token Counts by Period

| Period | Tokens | % of IA Total |
|---|---:|---:|
| ancient | 394,556 | 15.8% |
| medieval | 393,297 | 15.8% |
| renaissance_early_modern | 459,569 | 18.4% |
| nineteenth_century | 1,249,395 | 50.0% |

## Combined Corpus Context

After Pass 3 (Gutenberg + Internet Archive):

| Period | Gutenberg Tokens | IA Tokens | Combined | % Combined |
|---|---:|---:|---:|---:|
| ancient | 2,537,678 | 394,556 | 2,932,234 | 16.6% |
| late_antique | 877,507 | — | 877,507 | 5.0% |
| medieval | 3,451,608 | 393,297 | 3,844,905 | 21.8% |
| renaissance_early_modern | 4,622,131 | 459,569 | 5,081,700 | 28.8% |
| nineteenth_century | 2,566,730 | 1,249,395 | 3,816,125 | 21.6% |
| early_20th_century_pd | 1,077,822 | — | 1,077,822 | 6.1% |
| **Total** | **15,133,476** | **2,496,817** | **17,630,293** | |

## Deduplication

- Input: 13 records
- Output: 13 records (0 exact duplicates removed)
- Same-work clusters retained for review: 2
  - `aquinas_summa_contra_gentiles` (vols 1 and 2 — multi-volume, expected)
  - `hegel_phenomenology_spirit` (vols 1 and 2 — multi-volume, expected)

## Notes

- **Leibniz volume** (254,267 tokens): The Latta 1898 edition contains Monadology, Discourse on Metaphysics, and Correspondence with Arnauld. Token count reflects the full volume; Monadology itself is a short text (~30 pages). A future segmentation pass could register Discourse on Metaphysics as a separate work entry.
- **Aristotle volume** (204,949 tokens): Oxford Works of Aristotle Vol. VIII contains primarily the Metaphysics plus shorter works (De Sensu, De Memoria, etc.). Full volume text is retained.
- **Pascal Pensées** (205,302 tokens): The Trotter 1910 Dent edition includes prefatory material and editorial apparatus. Token count reflects the full volume.
- **Marx Capital Vol. 1** (548,316 tokens): The largest single IA acquisition; the Moore/Aveling edition is the standard English version. Vols 2-3 (1907-09, also pre-1928) are next-priority acquisitions.
- **Hegel Philosophy of Right**: Dyde 1896 translation used. The standard Knox 1942 translation is not in public domain (enters PD 2038).
- **Plotinus**: Only First Ennead (1917) unambiguously PD. MacKenna vols II-VI (1921-1930) require US Copyright Office renewal check.
