# Standard Ebooks Tokenization Report

**Source file:** `corpus/normalized/jsonl/standard_ebooks.deduped.jsonl`
**Token counts:** `corpus/reports/standard_ebooks_token_counts.jsonl`
**Summary:** `corpus/reports/standard_ebooks_token_counts_summary.json`
**Most recent run:** 2026-04-12 (Pass 4 — 21 documents)

---

## Validation Summary

| Check | Result |
|---|---|
| `standard_ebooks_token_counts.jsonl` exists and parses cleanly | PASS |
| `standard_ebooks_token_counts_summary.json` exists and parses cleanly | PASS |
| All 21 records have required schema fields | PASS |
| All doc_ids match between deduped JSONL and token counts | PASS (21/21) |
| `total_tokens` in summary matches sum of records | PASS (4,208,070) |
| `documents` count in summary matches record count | PASS (21) |
| Tokenizer metadata present on every record | PASS |
| `model_id` is `google/gemma-4-E2B-it` on all records | PASS |

No parse errors, no doc_id mismatches, no missing fields.

---

## Tokenizer Metadata

| Field | Value |
|---|---|
| `target_family` | `gemma4` |
| `backend` | `huggingface_auto_processor` |
| `model_id` | `google/gemma-4-E2B-it` |
| `tokenizer` | `huggingface_auto_processor:google/gemma-4-E2B-it` |
| `tokenizer_version` | `5.5.3` (transformers library version) |
| `processor_revision` | `null` |
| `plain_text_tokenization` | `true` |
| `add_special_tokens` | `false` |
| `chat_template_applied` | `false` |
| `enable_thinking` | `null` |
| `context_length` | `null` (no truncation applied) |

**Note:** AutoProcessor could not be loaded (requires PyTorch/Torchvision). AutoTokenizer fallback was used. For plain-text tokenization (`add_special_tokens=False`), the tokenizer and processor produce identical token counts; the fallback does not affect correctness.

Tokenization method: plain normalized text passed to `tokenizer(text, add_special_tokens=False)`, as specified in the agent operating spec.

---

## Totals

| Metric | Value |
|---|---|
| Documents | 21 |
| Distinct works | 20 (plato_dialogues is a collection) |
| Distinct authors | 15 |
| Total tokens | **4,208,070** |
| Language | `en` |
| Source | Standard Ebooks |

---

## Tokens by Quality Tier

| Tier | Tokens | Share |
|---|---|---|
| `tier_1_canonical_primary` | 3,971,422 | 94.4% |
| `tier_2_major_primary` | 236,648 | 5.6% |

---

## Tokens by Period

| Period | Tokens | Share |
|---|---|---|
| `ancient` | 1,815,472 | 43.1% |
| `late_antique` | 645,256 | 15.3% |
| `renaissance_early_modern` | 867,950 | 20.6% |
| `nineteenth_century` | 669,233 | 15.9% |
| `early_twentieth_public_domain_candidates` | 210,159 | 5.0% |

The `ancient` period dominates due to `plato_dialogues_jowett_se` (1,623,059 tokens — the full Jowett Dialogues collection).

---

## Tokens by Document

| Version ID | Author | Tokens | Quality Tier | Period |
|---|---|---:|---|---|
| `plato_dialogues_jowett_se` | Plato | 1,623,059 | tier_1_canonical_primary | ancient |
| `augustine_city_of_god_dods_wilson_smith_se` | Augustine | 586,661 | tier_1_canonical_primary | late_antique |
| `hobbes_leviathan_se` | Thomas Hobbes | 261,210 | tier_1_canonical_primary | renaissance_early_modern |
| `william_james_varieties_religious_experience_se` | William James | 236,648 | tier_2_major_primary | early_twentieth_public_domain_candidates |
| `smith_moral_sentiments_se` | Adam Smith | 194,055 | tier_1_canonical_primary | renaissance_early_modern |
| `dewey_democracy_education_se` | John Dewey | 159,107 | tier_1_canonical_primary | early_twentieth_public_domain_candidates |
| `nietzsche_zarathustra_common_se` | Friedrich Nietzsche | 136,370 | tier_1_canonical_primary | nineteenth_century |
| `aristotle_nicomachean_ethics_peters_se` | Aristotle | 129,845 | tier_1_canonical_primary | ancient |
| `locke_two_treatises_se` | John Locke | 125,781 | tier_1_canonical_primary | renaissance_early_modern |
| `wollstonecraft_vindication_woman_se` | Mary Wollstonecraft | 104,292 | tier_1_canonical_primary | nineteenth_century |
| `nietzsche_beyond_good_evil_zimmern_se` | Friedrich Nietzsche | 85,148 | tier_1_canonical_primary | nineteenth_century |
| `rousseau_social_contract_cole_se` | Jean-Jacques Rousseau | 72,791 | tier_1_canonical_primary | renaissance_early_modern |
| `nietzsche_genealogy_morals_samuel_se` | Friedrich Nietzsche | 67,697 | tier_1_canonical_primary | nineteenth_century |
| `william_james_pragmatism_se` | William James | 64,530 | tier_1_canonical_primary | early_twentieth_public_domain_candidates |
| `hume_enquiry_human_understanding_se` | David Hume | 64,331 | tier_1_canonical_primary | renaissance_early_modern |
| `marcus_aurelius_meditations_long_se` | Marcus Aurelius | 62,568 | tier_1_canonical_primary | ancient |
| `mill_on_liberty_se` | John Stuart Mill | 61,342 | tier_1_canonical_primary | nineteenth_century |
| `boethius_consolation_james_se` | Boethius | 58,595 | tier_1_canonical_primary | late_antique |
| `russell_problems_philosophy_se` | Bertrand Russell | 51,052 | tier_1_canonical_primary | early_twentieth_public_domain_candidates |
| `machiavelli_prince_marriott_se` | Niccolo Machiavelli | 45,490 | tier_1_canonical_primary | renaissance_early_modern |
| `marx_communist_manifesto_moore_se` | Karl Marx and Friedrich Engels | 17,498 | tier_1_canonical_primary | nineteenth_century |

---

## Combined Corpus After Pass 4 (Gutenberg + Internet Archive + Standard Ebooks)

| Source | Docs | Tokens | % Combined |
|---|---:|---:|---:|
| Project Gutenberg | 89 | 15,133,476 | 69.3% |
| Internet Archive | 13 | 2,496,817 | 11.4% |
| Standard Ebooks | 21 | 4,208,070 | 19.3% |
| **Combined** | **123** | **21,838,363** | |

### Combined Tokens by Period

| Period | PG Tokens | IA Tokens | SE Tokens | Combined | % Combined |
|---|---:|---:|---:|---:|---:|
| `ancient` | 2,537,678 | 394,556 | 1,815,472 | 4,747,706 | 21.7% |
| `late_antique` | 877,507 | — | 645,256 | 1,522,763 | 7.0% |
| `medieval` | 3,451,608 | 393,297 | — | 3,844,905 | 17.6% |
| `renaissance_early_modern` | 4,622,131 | 459,569 | 867,950 | 5,949,650 | 27.2% |
| `nineteenth_century` | 2,566,730 | 1,249,395 | 669,233 | 4,485,358 | 20.5% |
| `early_20th_public_domain` | 1,077,822 | — | 210,159 | 1,287,981 | 5.9% |
| **Total** | **15,133,476** | **2,496,817** | **4,208,070** | **21,838,363** | |

---

## Notes and Observations

**`plato_dialogues_jowett_se` dominates the SE batch.** At 1,623,059 tokens it represents 38.6% of all SE tokens. It also overlaps substantially with individual Gutenberg Plato dialog records. Training data preparation must resolve this redundancy.

**`augustine_city_of_god_dods_wilson_smith_se` (586,661 tokens)** is the complete City of God in one SE volume. Gutenberg has the same Dods translation in two volumes (668,795 tokens combined). These are near-duplicate editions from the same translator.

**Same-work cross-source pairs flagged for training review:**

| Work | Gutenberg | SE | Same translator? |
|---|---|---|---|
| City of God | pg_45304 + pg_45305 (Dods) | augustine_city_of_god_dods_wilson_smith_se (Dods/Wilson/Smith) | Yes |
| Leviathan | hobbes_leviathan_pg_3207 | hobbes_leviathan_se | Yes (original English) |
| Two Treatises | locke_second_treatise_government_pg_7370 (only 2nd Treatise) | locke_two_treatises_se (both treatises) | Yes (original English) |
| Enquiry HU | hume_enquiry_human_understanding_selby_bigge_pg_9662 | hume_enquiry_human_understanding_se | Same work, different editions |
| Social Contract | rousseau_social_contract_discourses_cole_pg_46333 | rousseau_social_contract_cole_se | Cole translation |
| Theory of Moral Sentiments | smith_moral_sentiments_pg_67363 | smith_moral_sentiments_se | Original English |
| Vindication | wollstonecraft_vindication_woman_pg_3420 | wollstonecraft_vindication_woman_se | Original English |
| Communist Manifesto | marx_communist_manifesto_pg_61/pg_31193 | marx_communist_manifesto_moore_se (Moore) | Moore translation |
| On Liberty | mill_on_liberty_pg_34901 | mill_on_liberty_se | Original English |
| Beyond Good and Evil | nietzsche_beyond_good_evil_zimmern_pg_4363 | nietzsche_beyond_good_evil_zimmern_se | Zimmern translation |
| Thus Spake Zarathustra | nietzsche_zarathustra_common_pg_1998 | nietzsche_zarathustra_common_se | Common translation |
| Genealogy of Morals | nietzsche_genealogy_morals_levy_pg_52319 | nietzsche_genealogy_morals_samuel_se | Different translators (Levy vs Samuel) |
| Pragmatism | william_james_pragmatism_pg_5116 | william_james_pragmatism_se | Original English |
| Varieties of Religious Experience | william_james_varieties_religious_experience_pg_621 | william_james_varieties_religious_experience_se | Original English |
| Problems of Philosophy | russell_problems_philosophy_pg_5827 | russell_problems_philosophy_se | Original English |
| Democracy and Education | dewey_democracy_education_pg_852 | dewey_democracy_education_se | Original English |

SE editions are expected to differ from Gutenberg in minor ways: Standard Ebooks performs careful proofreading against physical originals, corrects OCR errors, and applies consistent typographic conventions. These are not exact duplicates but are near-duplicates with shared content and potentially more consistent quality in the SE edition.

**Scale.** At 21.8M tokens, the combined corpus remains a pilot relative to the 10B-token target. The next expansion steps are HathiTrust/Internet Archive OCR for tier_3/4 content and additional Internet Archive acquisitions (Plotinus Enneads II-VI, Marx Capital vols 2-3, medieval gap sources).
