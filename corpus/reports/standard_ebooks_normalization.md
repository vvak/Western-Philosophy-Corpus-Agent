# Standard Ebooks Normalization Report

Validation date: 2026-04-12

This report validates `corpus/normalized/jsonl/standard_ebooks.jsonl`, produced from raw Standard Ebooks EPUB files under `corpus/raw/standard_ebooks/`.

Normalization extracted text from EPUB spine items, removed Standard Ebooks boilerplate pages, applied Unicode NFC normalization, and preserved manifest and acquisition sidecar metadata. It did not segment works, deduplicate editions, reject documents, or edit raw files.

## Summary

- Expected high-confidence Standard Ebooks records: 21
- Accepted normalized docs: 21
- Failed docs: 0
- Unexpected extra normalized docs: 0
- Output path: `corpus/normalized/jsonl/standard_ebooks.jsonl`
- Output file size: ~165 MB
- Output parses as valid JSONL.
- Required provenance fields are present for all accepted docs.
- Total normalized characters: 18,625,090

## EPUB Extraction Notes

**Normalizer:** `scripts/normalize/normalize_standard_ebooks.py`

**EPUB structure used:**
- `META-INF/container.xml` → OPF path
- OPF manifest + spine → reading order
- Spine items in `epub/text/*.xhtml` extracted in order

**Boilerplate items skipped (SE infrastructure, not philosophical content):**
- `titlepage.xhtml`
- `imprint.xhtml`
- `halftitlepage.xhtml`
- `colophon.xhtml`
- `uncopyright.xhtml`

**Items kept:** prefaces, introductions, chapters, appendices, endnotes, dedication pages, bibliographical notes, and all other content not matching the skip list.

**Text extraction method:** XML ElementTree parse of XHTML body element with block-level paragraph markers; Unicode NFC normalization; horizontal whitespace collapsed; runs of 3+ newlines reduced to 2.

## Failed Docs

None.

## Suspiciously Short Texts

Threshold: fewer than 50,000 normalized characters.

No accepted docs were below this threshold.

## Text-Length Stats

Character counts (18,625,090 total):

| Version ID | Title | Characters | Lines |
|---|---|---:|---:|
| `plato_dialogues_jowett_se` | Dialogues | 6,854,092 | ~120,000 est. |
| `augustine_city_of_god_dods_wilson_smith_se` | The City of God | 2,553,354 | — |
| `hobbes_leviathan_se` | Leviathan | 1,168,400 | — |
| `william_james_varieties_religious_experience_se` | The Varieties of Religious Experience | 1,070,709 | — |
| `smith_moral_sentiments_se` | The Theory of Moral Sentiments | 954,942 | — |
| `dewey_democracy_education_se` | Democracy and Education | 832,472 | — |
| `locke_two_treatises_se` | Two Treatises of Government | 572,005 | — |
| `aristotle_nicomachean_ethics_peters_se` | Nicomachean Ethics | 565,618 | — |
| `nietzsche_zarathustra_common_se` | Thus Spake Zarathustra | 525,806 | — |
| `wollstonecraft_vindication_woman_se` | A Vindication of the Rights of Woman | 498,539 | — |

## Accepted Docs

| Version ID | Work ID | Characters | Author |
|---|---|---:|---|
| `plato_dialogues_jowett_se` | `plato_dialogues` | 6,854,092 | Plato |
| `augustine_city_of_god_dods_wilson_smith_se` | `augustine_city_of_god` | 2,553,354 | Augustine |
| `hobbes_leviathan_se` | `hobbes_leviathan` | 1,168,400 | Thomas Hobbes |
| `william_james_varieties_religious_experience_se` | `william_james_varieties_religious_experience` | 1,070,709 | William James |
| `smith_moral_sentiments_se` | `smith_moral_sentiments` | 954,942 | Adam Smith |
| `dewey_democracy_education_se` | `dewey_democracy_education` | 832,472 | John Dewey |
| `locke_two_treatises_se` | `locke_two_treatises` | 572,005 | John Locke |
| `aristotle_nicomachean_ethics_peters_se` | `aristotle_nicomachean_ethics` | 565,618 | Aristotle |
| `nietzsche_zarathustra_common_se` | `nietzsche_zarathustra` | 525,806 | Friedrich Nietzsche |
| `wollstonecraft_vindication_woman_se` | `wollstonecraft_vindication_woman` | 498,539 | Mary Wollstonecraft |
| `nietzsche_beyond_good_evil_zimmern_se` | `nietzsche_beyond_good_evil` | 384,593 | Friedrich Nietzsche |
| `rousseau_social_contract_cole_se` | `rousseau_social_contract` | 346,137 | Jean-Jacques Rousseau |
| `hume_enquiry_human_understanding_se` | `hume_enquiry_human_understanding` | 317,474 | David Hume |
| `nietzsche_genealogy_morals_samuel_se` | `nietzsche_genealogy_morals` | 312,144 | Friedrich Nietzsche |
| `william_james_pragmatism_se` | `william_james_pragmatism` | 302,213 | William James |
| `mill_on_liberty_se` | `mill_liberty` | 305,962 | John Stuart Mill |
| `marcus_aurelius_meditations_long_se` | `marcus_aurelius_meditations` | 274,027 | Marcus Aurelius |
| `boethius_consolation_james_se` | `boethius_consolation` | 245,648 | Boethius |
| `russell_problems_philosophy_se` | `russell_problems_philosophy` | 245,995 | Bertrand Russell |
| `machiavelli_prince_marriott_se` | `machiavelli_prince` | 207,827 | Niccolo Machiavelli |
| `marx_communist_manifesto_moore_se` | `marx_communist_manifesto` | 87,133 | Karl Marx and Friedrich Engels |

## Notes on Large Records

**`plato_dialogues_jowett_se` (6,854,092 chars, 1,623,059 tokens):** This is the complete Standard Ebooks Jowett Plato Dialogues collection, which includes Apology, Charmides, Crito, Euthyphro, Gorgias, Ion, Laches, Laws, Lysis, Meno, Parmenides, Phaedo, Phaedrus, Philebus, Protagoras, Republic, Sophist, Statesman, Symposium, Theaetetus, Timaeus, and Critias — all in a single EPUB. This record has substantial overlap with individual Gutenberg Plato records (Republic ×2, Phaedo ×2, Gorgias, Laws, Theaetetus, Phaedrus, Protagoras, Parmenides, Symposium, Timaeus — see Gutenberg dedup report). Training data preparation must apply version selection or down-weighting to avoid Plato overrepresentation.

**`augustine_city_of_god_dods_wilson_smith_se` (2,553,354 chars, 586,661 tokens):** The complete City of God in a single SE volume (Dods/Wilson/Smith translation). Gutenberg has this as two volumes (pg_45304, pg_45305). The translator combination is the same source text; minor typographic differences are expected between editions.

## Next Checks

- Apply version selection or down-weighting for same-work cross-source records before training.
- Run a segmentation pass after deciding work-specific hierarchy rules, particularly for `plato_dialogues_jowett_se` (individual dialog boundaries).
- Run cross-source deduplication after all source acquisitions are complete.
