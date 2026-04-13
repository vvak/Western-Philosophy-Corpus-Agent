# Project Gutenberg Deduplication Report

Validation date: 2026-04-12

This report validates and records the conservative deduplication pass for `corpus/normalized/jsonl/gutenberg.jsonl`. The original normalized file was left unchanged.

## Summary

- Input path: `corpus/normalized/jsonl/gutenberg.jsonl`
- Deduped output path: `corpus/normalized/jsonl/gutenberg.deduped.jsonl`
- Input records: 89
- Output records: 89
- Exact full-text duplicate groups: 0
- Exact full-text duplicate records removed from derived output: 0
- Canonical whitespace/case duplicate groups retained for review: 0
- Same-work alternate or multi-record clusters retained for review: 14
- Removal policy: only exact full-text duplicate records are excluded from the derived output.
- Alternate editions, alternate translations, subsets, and multi-volume records are retained.

## Output Validation

- Output JSONL records parsed: 89
- Unique `doc_id` values: 89
- Unique `version_id` values: 89
- Exact duplicate hash groups in output: 0
- Records with `deduplication` metadata: 89

## Exact Full-Text Duplicates

None. No exact normalized text duplicates were found.

## Canonical Whitespace/Case Duplicate Review

None. No additional whitespace/case-only duplicate groups were found.

## Same-Work Clusters Retained

| Work ID | Relation | Records | Max Paragraph Containment | Version IDs |
| --- | --- | ---: | ---: | --- |
| `aquinas_summa_theologiae` | multi_part_or_volume_with_translator_variance | 4 | 0.002 | `aquinas_summa_theologica_prima_pg_17611` (Summa Theologica, Part I (Prima Pars), 2,837,997 chars)<br>`aquinas_summa_theologica_prima_secundae_pg_17897` (Summa Theologica, Part I-II (Pars Prima Secundae), 2,828,769 chars)<br>`aquinas_summa_theologica_secunda_secundae_pg_18755` (Summa Theologica, Part II-II (Secunda Secundae), 4,115,353 chars)<br>`aquinas_summa_theologica_tertia_pg_19950` (Summa Theologica, Part III (Tertia Pars), 2,686,481 chars) |
| `augustine_city_of_god` | multi_part_or_volume_candidate | 2 | 0.002 | `augustine_city_of_god_dods_pg_45304` (The City of God, Volume I, 1,313,843 chars)<br>`augustine_city_of_god_dods_pg_45305` (The City of God, Volume II, 1,387,076 chars) |
| `descartes_discourse_method` | alternate_translation_or_scope_candidate | 2 | 0.000 | `descartes_discourse_method_pg_25830` (A Discourse of a Method for the Well Guiding of Reason, 121,746 chars)<br>`descartes_discourse_method_veitch_pg_59` (Discourse on the Method of Rightly Conducting One's Reason and of Seeking Truth in the Sciences, 128,430 chars) |
| `epictetus_discourses_enchiridion` | alternate_translation_or_scope_candidate | 2 | 0.000 | `epictetus_discourses_enchiridion_long_pg_10661` (A Selection from the Discourses of Epictetus with the Encheiridion, 325,670 chars)<br>`epictetus_enchiridion_higginson_pg_45109` (The Enchiridion, 69,831 chars) |
| `erasmus_praise_folly` | alternate_translation_or_scope_candidate | 2 | 0.000 | `erasmus_praise_folly_holbein_pg_30201` (In Praise of Folly, 256,061 chars)<br>`erasmus_praise_folly_wilson_pg_9371` (The Praise of Folly, 202,791 chars) |
| `hume_treatise` | alternate_edition_candidate | 2 | 0.000 | `hume_treatise_human_nature_pg_4705` (A Treatise of Human Nature, 1,323,609 chars)<br>`hume_treatise_dialogues_green_grose_pg_62856` (A Treatise of Human Nature, 991,848 chars) |
| `locke_essay_human_understanding` | multi_part_or_volume_candidate | 2 | 0.000 | `locke_essay_humane_understanding_pg_10615` (An Essay Concerning Humane Understanding, Volume 1, 833,904 chars)<br>`locke_essay_humane_understanding_pg_10616` (An Essay Concerning Humane Understanding, Volume 2, 705,123 chars) |
| `machiavelli_prince` | alternate_translation_or_scope_candidate | 2 | 0.000 | `machiavelli_prince_marriott_pg_1232` (The Prince, 282,492 chars)<br>`machiavelli_prince_ricci_pg_57037` (The Prince, 172,815 chars) |
| `marcus_aurelius_meditations` | alternate_translation_or_scope_candidate | 2 | 0.000 | `marcus_aurelius_meditations_pg_2680` (Meditations, 398,126 chars)<br>`marcus_aurelius_meditations_chrystal_pg_55317` (The Meditations of the Emperor Marcus Aurelius Antoninus, 227,871 chars) |
| `marx_communist_manifesto` | same_work_alternate_candidate | 2 | 0.214 | `marx_communist_manifesto_pg_31193` (Manifesto of the Communist Party, 92,494 chars)<br>`marx_communist_manifesto_pg_61` (The Communist Manifesto, 72,883 chars) |
| `plato_phaedo` | alternate_translation_or_scope_candidate | 2 | 0.000 | `plato_apology_crito_phaedo_cary_pg_13726` (Apology, Crito, and Phaedo of Socrates, 285,115 chars)<br>`plato_phaedo_jowett_pg_1658` (Phaedo, 232,870 chars) |
| `plato_republic` | alternate_edition_candidate | 2 | 0.667 | `plato_republic_jowett_pg_1497` (The Republic, 1,194,387 chars)<br>`plato_republic_jowett_pg_150` (The Republic, 678,813 chars) |
| `schopenhauer_world_will_representation` | multi_part_or_volume_candidate | 3 | 0.000 | `schopenhauer_world_will_idea_haldane_kemp_pg_38427` (The World as Will and Idea (Vol. 1 of 3), 1,115,482 chars)<br>`schopenhauer_world_will_idea_haldane_kemp_pg_40097` (The World as Will and Idea (Vol. 2 of 3), 1,000,627 chars)<br>`schopenhauer_world_will_idea_haldane_kemp_pg_40868` (The World as Will and Idea (Vol. 3 of 3), 1,033,797 chars) |
| `spinoza_theologico_political_treatise` | multi_part_or_volume_candidate | 4 | 0.000 | `spinoza_theologico_political_treatise_elwes_pg_989` (Theologico-Political Treatise — Part 1, 176,274 chars)<br>`spinoza_theologico_political_treatise_elwes_pg_990` (Theologico-Political Treatise — Part 2, 186,100 chars)<br>`spinoza_theologico_political_treatise_elwes_pg_991` (A Theological-Political Treatise [Part III], 92,587 chars)<br>`spinoza_theologico_political_treatise_elwes_pg_992` (A Theological-Political Treatise [Part IV], 160,651 chars) |

## Notes

- The deduped file is a derived artifact; `corpus/normalized/jsonl/gutenberg.jsonl` remains the source of truth.
- This pass does not normalize, segment, boilerplate-strip, or remove near-duplicates.
- Same-work clusters should be reviewed before training weights are assigned, especially where Project Gutenberg records represent volumes, parts, selections, or alternate translations.
