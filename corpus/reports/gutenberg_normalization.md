# Project Gutenberg Normalization Report

Validation date: 2026-04-12

This report validates `corpus/normalized/jsonl/gutenberg.jsonl`, produced from raw Project Gutenberg text under `corpus/raw/gutenberg/`.

Normalization removed Project Gutenberg boilerplate and preserved manifest plus acquisition sidecar metadata. It did not segment works, deduplicate editions, reject documents, or edit raw files.

## Summary (Pass 2 — 2026-04-12)

- Expected high-confidence Project Gutenberg records: 89
- Accepted normalized docs: 89
- Failed docs: 0
- Unexpected extra normalized docs: 0
- Output path: `corpus/normalized/jsonl/gutenberg.jsonl`
- Output file size: 63 MB
- Output parses as valid JSONL.
- Required provenance fields are present for all accepted docs.
- Total normalized characters: 64,279,430

## Boilerplate Removal Notes

- Project Gutenberg `START` marker found: 89 docs
- Project Gutenberg `END` marker found: 89 docs
- Leading Project Gutenberg credit or warning notes removed: 33 docs
- No leading Project Gutenberg credit or warning notes found after the `START` marker: 56 docs
- Sentinel strings checked and not found in normalized `text`:
  - `START OF THE PROJECT GUTENBERG EBOOK`
  - `END OF THE PROJECT GUTENBERG EBOOK`
  - `This eBook is for the use of anyone anywhere in the United States`
  - `Project Gutenberg License`
  - `Full Project Gutenberg License`

The normalizer writes one full-text record per version with `normalization.segmentation` set to `full_text_only`. Work/book/section segmentation remains a future step.

## Failed Docs

None.

## Suspiciously Short Texts

Threshold used: fewer than 10,000 normalized characters.

No accepted docs were below this threshold. The shortest accepted docs are listed for review:

| Version ID | Title | Characters | Lines |
| --- | --- | ---: | ---: |
| `epictetus_enchiridion_higginson_pg_45109` | The Enchiridion | 69,831 | 1,283 |
| `marx_communist_manifesto_pg_61` | The Communist Manifesto | 72,883 | 1,381 |
| `marx_communist_manifesto_pg_31193` | Manifesto of the Communist Party | 92,494 | 1,786 |
| `spinoza_theologico_political_treatise_elwes_pg_991` | A Theological-Political Treatise [Part III] | 92,587 | 1,482 |
| `descartes_discourse_method_pg_25830` | A Discourse of a Method for the Well Guiding of Reason | 121,746 | 1,877 |
| `descartes_discourse_method_veitch_pg_59` | Discourse on the Method of Rightly Conducting One's Reason and of Seeking Truth in the Sciences | 128,430 | 1,976 |
| `spinoza_theologico_political_treatise_elwes_pg_992` | A Theological-Political Treatise [Part IV] | 160,651 | 2,546 |
| `mill_utilitarianism_pg_11224` | Utilitarianism | 161,096 | 2,493 |
| `machiavelli_prince_ricci_pg_57037` | The Prince | 172,815 | 2,769 |
| `spinoza_theologico_political_treatise_elwes_pg_989` | Theologico-Political Treatise - Part 1 | 176,274 | 2,803 |

## Text-Length Stats

Character counts:

- Total: 58,413,416
- Minimum: 69,831
- 25th percentile: 246,732
- Median: 514,904
- Mean: 789,370.49
- 75th percentile: 1,072,663.5
- Maximum: 4,115,353

Line counts:

- Total: 1,012,390
- Minimum: 1,283
- Median: 9,047.5
- Mean: 13,680.95
- Maximum: 79,466

Longest accepted docs:

| Version ID | Title | Characters | Lines |
| --- | --- | ---: | ---: |
| `aquinas_summa_theologica_secunda_secundae_pg_18755` | Summa Theologica, Part II-II (Secunda Secundae) | 4,115,353 | 79,466 |
| `montaigne_essays_complete_cotton_hazlitt_pg_3600` | Essays of Michel de Montaigne - Complete | 3,013,159 | 51,204 |
| `aquinas_summa_theologica_prima_pg_17611` | Summa Theologica, Part I (Prima Pars) | 2,837,997 | 53,900 |
| `aquinas_summa_theologica_prima_secundae_pg_17897` | Summa Theologica, Part I-II (Pars Prima Secundae) | 2,828,769 | 54,248 |
| `aquinas_summa_theologica_tertia_pg_19950` | Summa Theologica, Part III (Tertia Pars) | 2,686,481 | 51,043 |
| `mill_system_logic_pg_27942` | A System of Logic, Ratiocinative and Inductive | 2,447,118 | 37,826 |
| `santayana_life_reason_pg_15000` | The Life of Reason: The Phases of Human Progress | 1,940,143 | 31,695 |
| `maimonides_guide_perplexed_friedlander_pg_73584` | The guide for the perplexed | 1,554,907 | 24,623 |
| `augustine_city_of_god_dods_pg_45305` | The City of God, Volume II | 1,387,076 | 26,318 |
| `rousseau_emile_pg_5427` | Emile | 1,367,719 | 23,446 |

## Accepted Docs

| Version ID | Work ID | Characters | Lines | Title |
| --- | --- | ---: | ---: | --- |
| `aquinas_summa_theologica_prima_pg_17611` | `aquinas_summa_theologiae` | 2,837,997 | 53,900 | Summa Theologica, Part I (Prima Pars) |
| `aquinas_summa_theologica_prima_secundae_pg_17897` | `aquinas_summa_theologiae` | 2,828,769 | 54,248 | Summa Theologica, Part I-II (Pars Prima Secundae) |
| `aquinas_summa_theologica_secunda_secundae_pg_18755` | `aquinas_summa_theologiae` | 4,115,353 | 79,466 | Summa Theologica, Part II-II (Secunda Secundae) |
| `aquinas_summa_theologica_tertia_pg_19950` | `aquinas_summa_theologiae` | 2,686,481 | 51,043 | Summa Theologica, Part III (Tertia Pars) |
| `aristotle_politics_ellis_pg_6762` | `aristotle_politics` | 574,313 | 9,249 | Politics: A Treatise on Government |
| `augustine_city_of_god_dods_pg_45304` | `augustine_city_of_god` | 1,313,843 | 21,905 | The City of God, Volume I |
| `augustine_city_of_god_dods_pg_45305` | `augustine_city_of_god` | 1,387,076 | 26,318 | The City of God, Volume II |
| `augustine_confessions_pusey_pg_3296` | `augustine_confessions` | 602,908 | 9,281 | The Confessions of St. Augustine |
| `bacon_advancement_learning_morley_pg_5500` | `bacon_advancement_learning` | 487,468 | 7,625 | The Advancement of Learning |
| `bacon_novum_organum_devey_pg_45988` | `bacon_novum_organum` | 538,231 | 9,016 | Novum organum |
| `bergson_creative_evolution_mitchell_pg_26163` | `bergson_creative_evolution` | 833,645 | 14,899 | Creative Evolution |
| `berkeley_hylas_philonous_pg_4724` | `berkeley_hylas_philonous` | 205,692 | 4,147 | Three Dialogues Between Hylas and Philonous in Opposition to Sceptics and Atheists |
| `berkeley_principles_pg_4723` | `berkeley_principles` | 212,816 | 3,344 | A Treatise Concerning the Principles of Human Knowledge |
| `boethius_consolation_james_pg_14328` | `boethius_consolation` | 249,888 | 5,202 | The Consolation of Philosophy |
| `cicero_academic_questions_de_finibus_tusculan_yonge_pg_29247` | `cicero_academic_questions_de_finibus_tusculan` | 1,191,833 | 18,809 | The Academic Questions, Treatise De Finibus, and Tusculan Disputations, of M.T. Cicero |
| `descartes_discourse_method_pg_25830` | `descartes_discourse_method` | 121,746 | 1,877 | A Discourse of a Method for the Well Guiding of Reason |
| `descartes_discourse_method_veitch_pg_59` | `descartes_discourse_method` | 128,430 | 1,976 | Discourse on the Method of Rightly Conducting One's Reason and of Seeking Truth in the Sciences |
| `dewey_democracy_education_pg_852` | `dewey_democracy_education` | 829,436 | 12,762 | Democracy and Education |
| `epictetus_discourses_enchiridion_long_pg_10661` | `epictetus_discourses_enchiridion` | 325,670 | 5,247 | A Selection from the Discourses of Epictetus with the Encheiridion |
| `epictetus_enchiridion_higginson_pg_45109` | `epictetus_discourses_enchiridion` | 69,831 | 1,283 | The Enchiridion |
| `erasmus_praise_folly_holbein_pg_30201` | `erasmus_praise_folly` | 256,061 | 4,137 | In Praise of Folly |
| `erasmus_praise_folly_wilson_pg_9371` | `erasmus_praise_folly` | 202,791 | 3,035 | The Praise of Folly |
| `hegel_lectures_history_philosophy_haldane_pg_51635` | `hegel_lectures_history_philosophy` | 989,928 | 15,827 | Hegel's Lectures on the History of Philosophy: Volume 1 (of 3) |
| `hegel_philosophy_mind_wallace_pg_39064` | `hegel_philosophy_mind` | 705,822 | 11,562 | Hegel's Philosophy of Mind |
| `hobbes_leviathan_pg_3207` | `hobbes_leviathan` | 1,210,269 | 20,424 | Leviathan |
| `hume_enquiry_human_understanding_selby_bigge_pg_9662` | `hume_enquiry_human_understanding` | 347,043 | 6,049 | An Enquiry Concerning Human Understanding |
| `hume_enquiry_morals_pg_4320` | `hume_enquiry_morals` | 292,806 | 4,798 | An Enquiry Concerning the Principles of Morals |
| `hume_treatise_dialogues_green_grose_pg_62856` | `hume_treatise` | 991,848 | 17,106 | A Treatise of Human Nature |
| `hume_treatise_human_nature_pg_4705` | `hume_treatise` | 1,323,609 | 21,155 | A Treatise of Human Nature |
| `kant_critique_judgement_bernard_pg_48433` | `kant_critique_judgment` | 809,980 | 13,507 | Kant's Critique of Judgement |
| `kant_critique_practical_reason_abbott_pg_5683` | `kant_critique_practical_reason` | 370,955 | 6,112 | The Critique of Practical Reason |
| `kant_critique_pure_reason_meiklejohn_pg_4280` | `kant_critique_pure_reason` | 1,269,898 | 20,638 | The Critique of Pure Reason |
| `leibniz_theodicy_huggard_pg_17147` | `leibniz_theodicy` | 1,085,619 | 16,611 | Theodicy |
| `locke_essay_humane_understanding_pg_10615` | `locke_essay_human_understanding` | 833,904 | 14,166 | An Essay Concerning Humane Understanding, Volume 1 |
| `locke_essay_humane_understanding_pg_10616` | `locke_essay_human_understanding` | 705,123 | 11,721 | An Essay Concerning Humane Understanding, Volume 2 |
| `locke_second_treatise_government_pg_7370` | `locke_two_treatises` | 313,588 | 5,026 | Second Treatise of Government |
| `machiavelli_prince_marriott_pg_1232` | `machiavelli_prince` | 282,492 | 4,652 | The Prince |
| `machiavelli_prince_ricci_pg_57037` | `machiavelli_prince` | 172,815 | 2,769 | The Prince |
| `maimonides_guide_perplexed_friedlander_pg_73584` | `maimonides_guide_perplexed` | 1,554,907 | 24,623 | The guide for the perplexed |
| `marcus_aurelius_meditations_chrystal_pg_55317` | `marcus_aurelius_meditations` | 227,871 | 4,149 | The Meditations of the Emperor Marcus Aurelius Antoninus |
| `marcus_aurelius_meditations_pg_2680` | `marcus_aurelius_meditations` | 398,126 | 6,770 | Meditations |
| `marx_communist_manifesto_pg_31193` | `marx_communist_manifesto` | 92,494 | 1,786 | Manifesto of the Communist Party |
| `marx_communist_manifesto_pg_61` | `marx_communist_manifesto` | 72,883 | 1,381 | The Communist Manifesto |
| `mill_on_liberty_pg_34901` | `mill_liberty` | 306,413 | 4,655 | On Liberty |
| `mill_system_logic_pg_27942` | `mill_logic` | 2,447,118 | 37,826 | A System of Logic, Ratiocinative and Inductive |
| `mill_utilitarianism_pg_11224` | `mill_utilitarianism` | 161,096 | 2,493 | Utilitarianism |
| `montaigne_essays_complete_cotton_hazlitt_pg_3600` | `montaigne_essays` | 3,013,159 | 51,204 | Essays of Michel de Montaigne - Complete |
| `nietzsche_beyond_good_evil_zimmern_pg_4363` | `nietzsche_beyond_good_evil` | 382,799 | 6,064 | Beyond Good and Evil |
| `nietzsche_genealogy_morals_levy_pg_52319` | `nietzsche_genealogy_morals` | 332,649 | 5,338 | The Genealogy of Morals |
| `nietzsche_zarathustra_common_pg_1998` | `nietzsche_zarathustra` | 636,924 | 15,248 | Thus Spake Zarathustra: A Book for All and None |
| `plato_phaedo_jowett_pg_1658` | `plato_phaedo` | 232,870 | 4,392 | Phaedo |
| `plato_republic_jowett_pg_1497` | `plato_republic` | 1,194,387 | 24,478 | The Republic |
| `plato_republic_jowett_pg_150` | `plato_republic` | 678,813 | 16,496 | The Republic |
| `plato_symposium_jowett_pg_1600` | `plato_symposium` | 178,235 | 2,886 | Symposium |
| `rousseau_emile_pg_5427` | `rousseau_emile` | 1,367,719 | 23,446 | Emile |
| `rousseau_social_contract_discourses_cole_pg_46333` | `rousseau_social_contract` | 709,276 | 11,907 | The social contract & discourses |
| `russell_analysis_mind_pg_2529` | `russell_analysis_mind` | 520,792 | 8,506 | The Analysis of Mind |
| `russell_problems_philosophy_pg_5827` | `russell_problems_philosophy` | 245,680 | 3,936 | The Problems of Philosophy |
| `santayana_life_reason_pg_15000` | `santayana_life_reason` | 1,940,143 | 31,695 | The Life of Reason: The Phases of Human Progress |
| `schopenhauer_world_will_idea_haldane_kemp_pg_38427` | `schopenhauer_world_will_representation` | 1,115,482 | 16,450 | The World as Will and Idea (Vol. 1 of 3) |
| `schopenhauer_world_will_idea_haldane_kemp_pg_40097` | `schopenhauer_world_will_representation` | 1,000,627 | 14,895 | The World as Will and Idea (Vol. 2 of 3) |
| `schopenhauer_world_will_idea_haldane_kemp_pg_40868` | `schopenhauer_world_will_representation` | 1,033,797 | 16,932 | The World as Will and Idea (Vol. 3 of 3) |
| `smith_moral_sentiments_pg_67363` | `smith_moral_sentiments` | 691,433 | 10,919 | The Theory of Moral Sentiments |
| `spinoza_ethics_elwes_pg_3800` | `spinoza_ethics` | 501,985 | 9,666 | Ethics |
| `spinoza_theologico_political_treatise_elwes_pg_989` | `spinoza_theologico_political_treatise` | 176,274 | 2,803 | Theologico-Political Treatise - Part 1 |
| `spinoza_theologico_political_treatise_elwes_pg_990` | `spinoza_theologico_political_treatise` | 186,100 | 2,953 | Theologico-Political Treatise - Part 2 |
| `spinoza_theologico_political_treatise_elwes_pg_991` | `spinoza_theologico_political_treatise` | 92,587 | 1,482 | A Theological-Political Treatise [Part III] |
| `spinoza_theologico_political_treatise_elwes_pg_992` | `spinoza_theologico_political_treatise` | 160,651 | 2,546 | A Theological-Political Treatise [Part IV] |
| `thomas_more_utopia_pg_2130` | `thomas_more_utopia` | 237,296 | 3,611 | Utopia |
| `whitehead_science_modern_world_pg_68611` | `whitehead_science_modern_world` | 495,096 | 8,288 | Science and the modern world |
| `william_james_pragmatism_pg_5116` | `william_james_pragmatism` | 305,039 | 5,073 | Pragmatism: A New Name for Some Old Ways of Thinking |
| `william_james_varieties_religious_experience_pg_621` | `william_james_varieties_religious_experience` | 1,115,133 | 19,138 | The Varieties of Religious Experience: A Study in Human Nature |
| `wollstonecraft_vindication_woman_pg_3420` | `wollstonecraft_vindication_woman` | 509,016 | 9,079 | A Vindication of the Rights of Woman |
| `xenophon_memorabilia_dakyns_pg_1177` | `xenophon_memorabilia` | 392,569 | 8,384 | The Memorabilia |

## Next Checks

- Review composite and volume-based works before training, especially Aquinas, Augustine, Schopenhauer, Spinoza, and Locke multi-part records.
- Run a segmentation pass after deciding work-specific hierarchy rules.
- Run deduplication separately after segmentation, especially for duplicate or alternate Project Gutenberg editions.
