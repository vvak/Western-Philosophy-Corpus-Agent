# Coverage Gaps

Updated: 2026-04-12 (Pass 4 — Standard Ebooks acquisition)

This report tracks known gaps in corpus coverage after the fourth acquisition pass.

## Current State

- 123 documents acquired, normalized, and tokenized (89 Gutenberg + 13 Internet Archive + 21 Standard Ebooks)
- Gutenberg: 89 documents, 15.1M Gemma 4 tokens
- Internet Archive: 13 documents, 2.5M Gemma 4 tokens
- Standard Ebooks: 21 documents, 4.2M Gemma 4 tokens
- **Combined: 123 documents, 21.8M tokens**
- HathiTrust: no acquisitions yet

## Tier 1 Works — Pass 4 Status

| Work ID | Author | Status | Source |
|---|---|---|---|
| `anselm_proslogion` | Anselm | **ACQUIRED** | IA `proslogiummonol00deangoog` (Deane 1903) |
| `aquinas_summa_contra_gentiles` | Thomas Aquinas | **ACQUIRED** (2 vols) | IA `summacontragenti01/02thomuoft` (Dominican Fathers 1923/24) |
| `aristotle_metaphysics` | Aristotle | **ACQUIRED** | IA `workstranslatedi08aris` (Ross 1908) |
| `bentham_morals_legislation` | Jeremy Bentham | **ACQUIRED** | IA `introductiontopr02bent` (1823 orig.) |
| `cicero_de_officiis` | Cicero | **ACQUIRED** | IA `deofficiis00cice` (Gardiner 1899) |
| `epicurus_letters_principal_doctrines` | Epicurus | No confirmed PD English translation on IA or PG | — |
| `hegel_phenomenology_spirit` | Georg W. F. Hegel | **ACQUIRED** (2 vols) | IA `cu31924097557171` + `phenomenologyofm02hege` (Baillie 1910) |
| `hegel_philosophy_right` | Georg W. F. Hegel | **ACQUIRED** | IA `cu31924014578979` (Dyde 1896) |
| `kierkegaard_either_or` | Soren Kierkegaard | No complete PD English translation confirmed | — |
| `leibniz_monadology` | Gottfried W. Leibniz | **ACQUIRED** | IA `themonadology00leibuoft` (Latta 1898; includes Discourse on Metaphysics) |
| `lucretius_de_rerum_natura` | Lucretius | **ACQUIRED** | PG 785 (Leonard 1921) |
| `marx_capital` | Karl Marx | **ACQUIRED** (Vol. 1) | IA `capitalcritiqueo00marx` (Moore/Aveling 1906) |
| `nicholas_cusa_learned_ignorance` | Nicholas of Cusa | **No PD English translation available** | All known English translations post-1928 |
| `pascal_pensees` | Blaise Pascal | **ACQUIRED** | IA `thoughtstrbywftr00pascuoft` (Trotter ca. 1910) |
| `plato_dialogues` | Plato | **ACQUIRED** as collection | SE `plato/dialogues/benjamin-jowett` (Jowett; includes all major dialogues) |
| `plotinus_enneads` | Plotinus | **ACQUIRED** (Ennead I only) | IA `theenneads01plot` (MacKenna 1917) |
| `seneca_letters` | Seneca | L'Estrange adaptation acquired as `seneca_morals` | PG 56075 |
| `sextus_empiricus_outlines_pyrrhonism` | Sextus Empiricus | **No PD English translation available** | Bury Loeb (1933) has uncertain renewal status; no pre-1928 complete translation |

## Tier 2 Works With No Acquired Text

| Work ID | Author | Note |
|---|---|---|
| `abelard_sic_et_non` | Peter Abelard | Not on Gutenberg; IA sources need license review |
| `anselm_monologion` | Anselm | **Resolved**: included in `anselm_proslogion` IA acquisition (Deane 1903 vol contains both) |
| `averroes_commentaries` | Averroes | No confirmed PD English translation |
| `bonaventure_mind_journey_god` | Bonaventure | Not on Gutenberg; IA sources need license review |
| `ockham_philosophical_writings` | William of Ockham | Not on Gutenberg; IA sources need license review |
| `pseudo_dionysius_works` | Pseudo-Dionysius | Not on Gutenberg; IA sources need license review |

## Still-Missing Tier 1 Works

2 works definitively unresolvable for this corpus:

- **`nicholas_cusa_learned_ignorance`** — All English translations by Heron (1954) and Hopkins are post-1928 and under copyright. No pre-1928 English translation exists in accessible form.
- **`sextus_empiricus_outlines_pyrrhonism`** — The standard English translation (Bury Loeb 1933) was published after the 1928 cutoff with uncertain copyright renewal status. No pre-1928 complete English translation confirmed.

3 works with no confirmed PD source yet:

- **`epicurus_letters_principal_doctrines`** — Primary text scattered across doxographic sources. No standalone pre-1928 English translation confirmed. Bailey's edition (Oxford 1926) may be eligible — requires detailed copyright check.
- **`kierkegaard_either_or`** — No complete pre-1928 English translation. Hollander selections (PG 60333) acquired but incomplete.
- **`plotinus_enneads`** (partial) — Only First Ennead (1917 MacKenna) unambiguously PD. Enneads II-VI published 1921-1930 by MacKenna; copyright renewal status for vols published 1921-1930 requires US Copyright Office check.

## Next Acquisition Priority

1. **Plotinus Enneads II-VI** — Check US Copyright Office renewal records for MacKenna vols published 1921-1930. If not renewed, all 6 Enneads are PD and can be acquired from IA (~800K estimated tokens).

2. **Marx Capital Vol. 2 and 3** — Moore/Aveling/Engels translations available on IA (vols 2-3 published 1907-09, pre-1928); would complete the Capital set.

3. **Medieval gap** — Abelard, Averroes, Bonaventure, Ockham, Pseudo-Dionysius. Require careful license review on available translation editions.

4. **Epicurus Bailey edition (Oxford 1926)** — Pre-1928; copyright renewal check needed before acquisition.

5. **HathiTrust expansion** — For works where IA full-view access is unavailable or where HathiTrust has better OCR.

## Underrepresented Areas

- Presocratic fragments and doxography (Diels-Kranz; no PD English edition)
- Hellenistic schools beyond Stoicism (Epicurus, Skeptics)
- Late antique Neoplatonism — Plotinus partially acquired; Porphyry, Iamblichus, Proclus still absent
- Medieval Jewish and Islamic philosophy (Avicenna, Averroes beyond partial; Ibn Gabirol)
- Renaissance Platonism (Ficino, Pico)
- German idealism beyond Hegel (Fichte, Schelling)
- Kierkegaard primary works
- Early analytic philosophy before 1931 (Frege, early Wittgenstein — limited PD English)
- Women philosophers in public-domain editions (Mary Wollstonecraft acquired; Harriet Taylor needs review)
- Original-language editions (Greek, Latin, German, French) for cross-lingual corpus use

## Cross-Source Duplicate Pairs Pending Training-Time Resolution

Several work_ids now have multiple editions from different sources. These are not exact duplicates but contain the same philosophical text and must be weighted or deduplicated before training:

| Work | Gutenberg Record | SE Record | Same translator? |
|---|---|---|---|
| City of God | pg_45304 + pg_45305 (Dods) | augustine_city_of_god_dods_wilson_smith_se | Yes (Dods) |
| Leviathan | hobbes_leviathan_pg_3207 | hobbes_leviathan_se | Yes (original English) |
| Two Treatises | locke_second_treatise_government_pg_7370 | locke_two_treatises_se | Yes (original; PG only has 2nd Treatise) |
| Enquiry HU | hume_enquiry_human_understanding_selby_bigge_pg_9662 | hume_enquiry_human_understanding_se | Yes (same work, different typesetting) |
| Social Contract | rousseau_social_contract_discourses_cole_pg_46333 | rousseau_social_contract_cole_se | Yes (Cole translation) |
| Theory of Moral Sentiments | smith_moral_sentiments_pg_67363 | smith_moral_sentiments_se | Yes (original English) |
| Vindication of the Rights of Woman | wollstonecraft_vindication_woman_pg_3420 | wollstonecraft_vindication_woman_se | Yes (original English) |
| Communist Manifesto | marx_communist_manifesto_pg_61/pg_31193 | marx_communist_manifesto_moore_se | Yes (Moore) |
| On Liberty | mill_on_liberty_pg_34901 | mill_on_liberty_se | Yes (original English) |
| Beyond Good and Evil | nietzsche_beyond_good_evil_zimmern_pg_4363 | nietzsche_beyond_good_evil_zimmern_se | Yes (Zimmern) |
| Thus Spake Zarathustra | nietzsche_zarathustra_common_pg_1998 | nietzsche_zarathustra_common_se | Yes (Common) |
| Pragmatism | william_james_pragmatism_pg_5116 | william_james_pragmatism_se | Yes (original English) |
| Varieties of Religious Experience | william_james_varieties_religious_experience_pg_621 | william_james_varieties_religious_experience_se | Yes (original English) |
| Problems of Philosophy | russell_problems_philosophy_pg_5827 | russell_problems_philosophy_se | Yes (original English) |
| Democracy and Education | dewey_democracy_education_pg_852 | dewey_democracy_education_se | Yes (original English) |

## Token Balance Notes

- **Ancient period** now: Gutenberg (2.54M) + IA Aristotle + Cicero (307K) + SE Plato collection + SE Aristotle (1.95M) = **4.75M tokens, 21.7% of combined corpus**. Plato alone contributes ~2.0M tokens across PG+SE editions. Per-dialog weights should be computed before training.
- **Renaissance/early modern** remains the largest period at 5.95M tokens (27.2%). Hobbes, Locke, Spinoza, Bacon, Descartes, Hobbes well-covered.
- **Medieval** at 3.84M is second-largest but mostly Aquinas. Medieval breadth remains thin.
- **19th century** grew to 4.49M. Marx Capital vol 1 (548K) + Bentham + Hegel IA + Nietzsche/Mill/Marx SE add substantial content.
- **Late antique** at 1.52M is now better represented thanks to SE Augustine (586K) + PG Augustine + Boethius.
- **Combined: 21.8M tokens, 123 documents, 42+ authors, all English.**
