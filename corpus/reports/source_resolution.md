# Source Resolution Report

Source resolution has now covered the initial Project Gutenberg CSV pass and a metadata-only Standard Ebooks pass. No raw or bulk text was downloaded in the Standard Ebooks pass.

Project Gutenberg's offline catalog page says its machine-readable XML/RDF/CSV metadata should be used instead of crawling the website. The catalog also notes that Project Gutenberg release metadata does not include original print publication dates and that some ebooks come from multiple print editions. Because of that, the first pass records `source_release_date` and keeps edition review in the license rationale.

For Standard Ebooks, only finished catalog pages with a `read-free` section were added to `versions.jsonl`. Search hits that resolved to `ebook-placeholder` sponsor pages were treated as deferred and were not added as downloadable versions.

## Summary

- Seed works in `works.jsonl`: 83
- Version records in `versions.jsonl`: 106
- Project Gutenberg version records: 77
- Standard Ebooks version records: 29
- Standard Ebooks unique source slugs: 25
- Standard Ebooks work IDs covered: 28
- Status: usable as a first download plan, but not final legal/edition clearance

## Project Gutenberg Pass

Strong Project Gutenberg matches were found for major works by Plato, Aristotle, Xenophon, Epictetus, Marcus Aurelius, Augustine, Boethius, Maimonides, Aquinas, Machiavelli, Erasmus, Thomas More, Montaigne, Bacon, Hobbes, Descartes, Spinoza, Locke, Leibniz, Berkeley, Hume, Rousseau, Adam Smith, Kant, Wollstonecraft, Schopenhauer, Marx/Engels, Mill, Nietzsche, William James, Bergson, Russell, Dewey, Santayana, and Whitehead.

The Project Gutenberg pass found useful adjacent Cicero and Hegel works that were not exact matches for the original seed IDs. They have been split into their own `work_id` records:

- `cicero_academic_questions_de_finibus_tusculan`
- `hegel_philosophy_mind`
- `hegel_lectures_history_philosophy`

## Standard Ebooks High-Confidence Resolutions

High-confidence Standard Ebooks records were added where the finished catalog page is an exact or near-exact match for the manifest work:

- `plato_dialogues` -> `plato/dialogues/benjamin-jowett`
- `aristotle_nicomachean_ethics` -> `aristotle/nicomachean-ethics/f-h-peters`
- `marcus_aurelius_meditations` -> `marcus-aurelius/meditations/george-long`
- `augustine_city_of_god` -> `augustine-of-hippo/the-city-of-god/marcus-dods_george-wilson_j-j-smith`
- `boethius_consolation` -> `boethius/the-consolation-of-philosophy/h-r-james`
- `machiavelli_prince` -> `niccolo-machiavelli/the-prince/w-k-marriott`
- `hobbes_leviathan` -> `thomas-hobbes/leviathan`
- `locke_two_treatises` -> `john-locke/two-treatises-of-government`
- `hume_enquiry_human_understanding` -> `david-hume/an-enquiry-concerning-human-understanding`
- `rousseau_social_contract` -> `jean-jacques-rousseau/the-social-contract/g-d-h-cole`
- `smith_moral_sentiments` -> `adam-smith/the-theory-of-moral-sentiments`
- `wollstonecraft_vindication_woman` -> `mary-wollstonecraft/a-vindication-of-the-rights-of-woman`
- `marx_communist_manifesto` -> `karl-marx_friedrich-engels/the-communist-manifesto/samuel-moore`
- `mill_liberty` -> `john-stuart-mill/on-liberty`
- `nietzsche_beyond_good_evil` -> `friedrich-nietzsche/beyond-good-and-evil/helen-zimmern`
- `nietzsche_zarathustra` -> `friedrich-nietzsche/thus-spake-zarathustra/thomas-common`
- `nietzsche_genealogy_morals` -> `friedrich-nietzsche/the-genealogy-of-morals/horace-b-samuel`
- `william_james_pragmatism` -> `william-james/pragmatism`
- `william_james_varieties_religious_experience` -> `william-james/the-varieties-of-religious-experience`
- `russell_problems_philosophy` -> `bertrand-russell/the-problems-of-philosophy`
- `dewey_democracy_education` -> `john-dewey/democracy-and-education`

## Standard Ebooks Medium-Confidence Resolutions

Medium-confidence records were added where the Standard Ebooks slug is a finished catalog page but the manifest mapping needs segmentation, pairing, or partial-coverage review:

- `plato_republic`, `plato_symposium`, and `plato_phaedo` map to the Jowett `plato/dialogues/benjamin-jowett` collection. Deduplicate the shared `source_url` before download and segment the component works before training.
- `cicero_academic_questions_de_finibus_tusculan` maps partially to `cicero/tusculan-disputations/c-d-yonge`. This covers Tusculan Disputations only, not Academic Questions or De Finibus.
- `epictetus_discourses_enchiridion` maps to both `epictetus/discourses/george-long` and `epictetus/short-works/george-long`. The second source covers the Enchiridion and fragments; pair both records before treating the composite work as complete.
- `descartes_discourse_method` and `descartes_meditations` map to `rene-descartes/philosophical-works/john-veitch`, which includes Discourse on the Method, Meditations on First Philosophy, and selections from Principles of Philosophy. Segment before training.

## Standard Ebooks Deferred Or Not Added

The following Standard Ebooks search hits were not added because they were placeholder pages, had no finished catalog page, or were not an exact match for a manifest work:

- `epicurus_letters_principal_doctrines`
- `lucretius_de_rerum_natura`
- `cicero_de_officiis`
- `seneca_letters`
- `plotinus_enneads`
- `augustine_confessions`
- `aquinas_summa_theologiae`
- `leibniz_theodicy`
- `erasmus_praise_folly`
- `thomas_more_utopia`
- `montaigne_essays`
- `pascal_pensees`
- `spinoza_ethics`
- `locke_essay_human_understanding`
- `berkeley_principles`
- `berkeley_hylas_philonous`
- `hume_treatise`
- `hume_enquiry_morals`
- `kant_critique_pure_reason`
- `kant_critique_practical_reason`
- `kant_critique_judgment`
- `hegel_philosophy_right`
- `schopenhauer_world_will_representation`
- `marx_capital`
- `mill_utilitarianism`
- `bergson_creative_evolution`
- `russell_analysis_mind`
- `santayana_life_reason`
- `whitehead_science_modern_world`

## Unresolved Or Deferred From Project Gutenberg

No sufficiently strong Project Gutenberg match was accepted for:

- `epicurus_letters_principal_doctrines`
- `lucretius_de_rerum_natura`
- `seneca_letters`
- `sextus_empiricus_outlines_pyrrhonism`
- `plotinus_enneads`
- `pseudo_dionysius_works`
- `anselm_proslogion`
- `anselm_monologion`
- `abelard_sic_et_non`
- `averroes_commentaries`
- `aquinas_summa_contra_gentiles`
- `bonaventure_mind_journey_god`
- `ockham_philosophical_writings`
- `nicholas_cusa_learned_ignorance`
- `pascal_pensees`
- `leibniz_monadology`
- `bentham_morals_legislation`
- `hegel_phenomenology_spirit`
- `kierkegaard_either_or`
- `marx_capital`

These should be resolved next through Internet Archive, HathiTrust, Perseus, or another clear-license source.

## Next Steps

1. Resolve Internet Archive metadata for the unresolved/deferred list.
2. Resolve HathiTrust full-view/public-domain candidates for works still unresolved after Internet Archive.
3. Add a JSONL validator that checks required fields and flags `resolution_confidence=low`.
4. Before Standard Ebooks acquisition, deduplicate records that share the same `source_url` and download each slug at most once.
