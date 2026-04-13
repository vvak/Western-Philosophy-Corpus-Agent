# Gutenberg Tokenization Report

**Source file:** `corpus/normalized/jsonl/gutenberg.deduped.jsonl`  
**Token counts:** `corpus/reports/token_counts.jsonl`  
**Summary:** `corpus/reports/token_counts_summary.json`  
**Most recent run:** 2026-04-12 (Pass 2 — 89 documents)

---

## Validation Summary

| Check | Result |
|---|---|
| `token_counts.jsonl` exists and parses cleanly | PASS |
| `token_counts_summary.json` exists and parses cleanly | PASS |
| All 89 records have required schema fields | PASS |
| All doc_ids match between deduped JSONL and token counts | PASS (89/89) |
| `total_tokens` in summary matches sum of records | PASS (15,133,476) |
| `documents` count in summary matches record count | PASS (89) |
| Tokenizer metadata present on every record | PASS |
| `model_id` is `google/gemma-4-E2B-it` on all records | PASS |

No parse errors, no doc_id mismatches, no missing fields.

---

## Tokenizer Metadata

These fields appear on every record in `token_counts.jsonl` and are reproduced in `token_counts_summary.json`:

| Field | Value |
|---|---|
| `target_family` | `gemma4` |
| `backend` | `huggingface_auto_processor` |
| `model_id` | `google/gemma-4-E2B-it` |
| `tokenizer` | `huggingface_auto_processor:google/gemma-4-E2B-it` |
| `tokenizer_version` | `5.5.3` (transformers library version) |
| `processor_revision` | `null` (default HEAD at download time) |
| `plain_text_tokenization` | `true` |
| `add_special_tokens` | `false` |
| `chat_template_applied` | `false` |
| `enable_thinking` | `null` |
| `context_length` | `null` (no truncation applied) |

Tokenization method: plain normalized text passed to `processor.tokenizer(text, add_special_tokens=False)`, as specified in the agent operating spec. Chat template was not applied; these are corpus token counts, not SFT examples.

---

## Totals

| Metric | Pass 1 (2026-04-12) | Pass 2 (2026-04-12) | Delta |
|---|---|---|---|
| Documents | 74 | 89 | +15 |
| Distinct works | 56 | 70 | +14 |
| Distinct authors | 37 | 40 | +3 |
| Total tokens | 13,733,654 | **15,133,476** | +1,399,822 |
| Language | `en` | `en` | — |
| Source | Project Gutenberg | Project Gutenberg | — |

---

## Tokens by Quality Tier

| Tier | Tokens | Share |
|---|---|---|
| `tier_1_canonical_primary` | 11,911,711 | 78.7% |
| `tier_2_major_primary` | 3,221,765 | 21.3% |

No tier_3, tier_4, or rejected records appear in the deduped JSONL.

---

## Tokens by Period

| Period | Tokens | Share |
|---|---|---|
| `ancient` | 2,537,678 | 16.8% |
| `late_antique` | 877,507 | 5.8% |
| `medieval` | 3,451,608 | 22.8% |
| `nineteenth_century` | 2,566,730 | 17.0% |
| `renaissance_early_modern` | 4,622,131 | 30.5% |
| `early_twentieth_public_domain_candidates` | 1,077,822 | 7.1% |

Ancient period grew from 9.5% to 16.8% due to new Plato dialogues (Laws, Timaeus, Theaetetus, Gorgias, Phaedrus, Protagoras, Parmenides), Aristotle's Nicomachean Ethics and Poetics, Lucretius, and Seneca. Renaissance/early modern remains the largest period. Medieval is dominated by Aquinas.

---

## Tokens by Author

| Author | Tokens | Share |
|---|---|---|
| Thomas Aquinas | 3,083,657 | 20.4% |
| Plato | 1,321,395 | 8.7% |
| Augustine | 816,760 | 5.4% |
| Arthur Schopenhauer | 728,532 | 4.8% |
| Michel de Montaigne | 726,385 | 4.8% |
| David Hume | 661,785 | 4.4% |
| John Stuart Mill | 635,572 | 4.2% |
| Immanuel Kant | 530,290 | 3.5% |
| Jean-Jacques Rousseau | 474,645 | 3.1% |
| John Locke | 427,454 | 2.8% |
| George Santayana | 414,710 | 2.7% |
| Georg Wilhelm Friedrich Hegel | 389,191 | 2.6% |
| Maimonides | 367,951 | 2.4% |
| William James | 334,611 | 2.2% |
| Friedrich Nietzsche | 329,482 | 2.2% |
| Aristotle | 321,440 | 2.1% |
| Thomas Hobbes | 301,408 | 2.0% |
| Cicero | 282,105 | 1.9% |
| Baruch Spinoza | 269,641 | 1.8% |
| Gottfried Wilhelm Leibniz | 252,597 | 1.7% |
| Francis Bacon | 235,279 | 1.6% |
| Henri Bergson | 217,148 | 1.4% |
| John Dewey | 170,018 | 1.1% |
| Bertrand Russell | 169,589 | 1.1% |
| Marcus Aurelius | 151,005 | 1.0% |
| Adam Smith | 151,398 | 1.0% |
| Aristotle (nicomachean ethics) | — | — |
| Seneca | 147,931 | 1.0% |
| Lucretius | 113,996 | 0.8% |
| Soren Kierkegaard | 113,898 | 0.8% |
| Mary Wollstonecraft | 115,846 | 0.8% |
| Erasmus | 108,592 | 0.7% |
| Rene Descartes | 109,403 | 0.7% |
| Alfred North Whitehead | 106,357 | 0.7% |
| Niccolo Machiavelli | 104,783 | 0.7% |
| Xenophon | 103,253 | 0.7% |
| George Berkeley | 97,828 | 0.6% |
| Epictetus | 96,553 | 0.6% |
| Boethius | 60,747 | 0.4% |
| Thomas More | 54,797 | 0.4% |
| Karl Marx and Friedrich Engels | 35,444 | 0.2% |

---

## Tokens by Work

70 distinct works. Multi-document works are aggregated.

| Author | Work | Quality Tier | Docs | Tokens |
|---|---|---|---|---|
| Thomas Aquinas | Summa Theologica (all parts) | tier_1_canonical_primary | 4 | 3,083,657 |
| Arthur Schopenhauer | The World as Will and Idea | tier_1_canonical_primary | 3 | 728,532 |
| Michel de Montaigne | Essays — Complete | tier_1_canonical_primary | 1 | 726,385 |
| Augustine | The City of God | tier_1_canonical_primary | 2 | 668,795 |
| John Stuart Mill | A System of Logic | tier_2_major_primary | 1 | 533,984 |
| David Hume | A Treatise of Human Nature | tier_1_canonical_primary | 2 | 518,331 |
| Plato | The Republic | tier_1_canonical_primary | 2 | 441,349 |
| George Santayana | The Life of Reason | tier_1_canonical_primary | 1 | 414,710 |
| Maimonides | The Guide for the Perplexed | tier_1_canonical_primary | 1 | 367,951 |
| John Locke | An Essay Concerning Human Understanding | tier_1_canonical_primary | 2 | 353,246 |
| Plato | Laws | tier_2_major_primary | 1 | 309,120 |
| Jean-Jacques Rousseau | Emile | tier_2_major_primary | 1 | 316,177 |
| Thomas Hobbes | Leviathan | tier_1_canonical_primary | 1 | 301,408 |
| Cicero | Academic Questions, De Finibus, Tusculan Disputations | tier_2_major_primary | 1 | 282,105 |
| Immanuel Kant | Critique of Pure Reason | tier_1_canonical_primary | 1 | 270,211 |
| William James | The Varieties of Religious Experience | tier_2_major_primary | 1 | 265,230 |
| Gottfried Wilhelm Leibniz | Theodicy | tier_2_major_primary | 1 | 252,597 |
| Georg Wilhelm Friedrich Hegel | Lectures on the History of Philosophy | tier_2_major_primary | 1 | 228,234 |
| Henri Bergson | Creative Evolution | tier_1_canonical_primary | 1 | 217,148 |
| Immanuel Kant | Critique of Judgement | tier_1_canonical_primary | 1 | 179,704 |
| John Dewey | Democracy and Education | tier_1_canonical_primary | 1 | 170,018 |
| Friedrich Nietzsche | Thus Spake Zarathustra | tier_1_canonical_primary | 1 | 162,708 |
| Georg Wilhelm Friedrich Hegel | Philosophy of Mind | tier_2_major_primary | 1 | 160,957 |
| Jean-Jacques Rousseau | The Social Contract & Discourses | tier_1_canonical_primary | 1 | 158,468 |
| Aristotle | Nicomachean Ethics | tier_1_canonical_primary | 1 | 149,483 |
| Adam Smith | The Theory of Moral Sentiments | tier_1_canonical_primary | 1 | 151,398 |
| Seneca | Morals of a Happy Life, Benefits, Anger and Clemency | tier_2_major_primary | 1 | 147,931 |
| Marcus Aurelius | Meditations | tier_1_canonical_primary | 2 | 151,005 |
| Baruch Spinoza | Theologico-Political Treatise | tier_1_canonical_primary | 4 | 148,315 |
| Augustine | Confessions | tier_1_canonical_primary | 1 | 147,965 |
| Aristotle | Politics | tier_1_canonical_primary | 1 | 132,641 |
| Baruch Spinoza | Ethics | tier_1_canonical_primary | 1 | 121,326 |
| Lucretius | On the Nature of Things | tier_1_canonical_primary | 1 | 113,996 |
| Soren Kierkegaard | Selections from the Writings of Kierkegaard | tier_2_major_primary | 1 | 113,898 |
| Francis Bacon | Novum Organum | tier_1_canonical_primary | 1 | 120,044 |
| Mary Wollstonecraft | A Vindication of the Rights of Woman | tier_1_canonical_primary | 1 | 115,846 |
| Francis Bacon | The Advancement of Learning | tier_1_canonical_primary | 1 | 115,235 |
| Bertrand Russell | The Analysis of Mind | tier_1_canonical_primary | 1 | 114,892 |
| Plato | Timaeus | tier_2_major_primary | 1 | 99,788 |
| Erasmus | The Praise of Folly | tier_2_major_primary | 2 | 108,592 |
| Rene Descartes | Discourse on the Method | tier_1_canonical_primary | 2 | 56,803 |
| Rene Descartes | Six Metaphysical Meditations (Molyneux 1680) | tier_1_canonical_primary | 1 | 52,600 |
| Alfred North Whitehead | Science and the Modern World | tier_2_major_primary | 1 | 106,357 |
| Niccolo Machiavelli | The Prince | tier_1_canonical_primary | 2 | 104,783 |
| Xenophon | The Memorabilia | tier_2_major_primary | 1 | 103,253 |
| Plato | Theaetetus | tier_2_major_primary | 1 | 88,896 |
| Epictetus | Discourses and Enchiridion | tier_1_canonical_primary | 2 | 96,553 |
| Friedrich Nietzsche | Beyond Good and Evil | tier_1_canonical_primary | 1 | 88,891 |
| Immanuel Kant | Critique of Practical Reason | tier_1_canonical_primary | 1 | 80,375 |
| Plato | Gorgias | tier_1_canonical_primary | 1 | 79,987 |
| David Hume | An Enquiry Concerning Human Understanding | tier_1_canonical_primary | 1 | 78,441 |
| Friedrich Nietzsche | The Genealogy of Morals | tier_1_canonical_primary | 1 | 77,883 |
| John Locke | Second Treatise of Government | tier_1_canonical_primary | 1 | 74,208 |
| Plato | Apology, Crito, and Phaedo (Henry Cary) | tier_1_canonical_primary | 1 | 70,636 |
| William James | Pragmatism | tier_1_canonical_primary | 1 | 69,381 |
| John Stuart Mill | On Liberty | tier_1_canonical_primary | 1 | 66,517 |
| David Hume | An Enquiry Concerning the Principles of Morals | tier_1_canonical_primary | 1 | 65,013 |
| Boethius | The Consolation of Philosophy | tier_1_canonical_primary | 1 | 60,747 |
| Plato | Phaedo (Jowett) | tier_1_canonical_primary | 1 | 54,885 |
| Thomas More | Utopia | tier_1_canonical_primary | 1 | 54,797 |
| Bertrand Russell | The Problems of Philosophy | tier_1_canonical_primary | 1 | 54,697 |
| Plato | Phaedrus | tier_1_canonical_primary | 1 | 50,082 |
| George Berkeley | Three Dialogues Between Hylas and Philonous | tier_1_canonical_primary | 1 | 49,349 |
| George Berkeley | A Treatise Concerning the Principles of Human Knowledge | tier_1_canonical_primary | 1 | 48,479 |
| Plato | Parmenides | tier_2_major_primary | 1 | 47,248 |
| Plato | Symposium | tier_1_canonical_primary | 1 | 42,563 |
| Plato | Protagoras | tier_2_major_primary | 1 | 36,841 |
| Karl Marx and Friedrich Engels | The Communist Manifesto | tier_1_canonical_primary | 2 | 35,444 |
| John Stuart Mill | Utilitarianism | tier_1_canonical_primary | 1 | 35,071 |
| Aristotle | Poetics (S.H. Butcher) | tier_2_major_primary | 1 | 20,557 |
| Aristotle | Categories (E.M. Edghill) | tier_1_canonical_primary | 1 | 18,759 |

---

## Top 10 Works by Token Count

| Rank | Work ID | Tokens |
|---|---|---|
| 1 | `aquinas_summa_theologiae` | 3,083,657 |
| 2 | `schopenhauer_world_will_representation` | 728,532 |
| 3 | `montaigne_essays` | 726,385 |
| 4 | `augustine_city_of_god` | 668,795 |
| 5 | `mill_logic` | 533,984 |
| 6 | `hume_treatise` | 518,331 |
| 7 | `plato_republic` | 441,349 |
| 8 | `santayana_life_reason` | 414,710 |
| 9 | `maimonides_guide_perplexed` | 367,951 |
| 10 | `locke_essay_human_understanding` | 353,246 |

---

## Pass 2 New Works (+1,399,822 tokens)

| Work | Tokens | Notes |
|---|---|---|
| Plato — Laws | 309,120 | Longest new addition |
| Aristotle — Nicomachean Ethics | 149,483 | Translator unclear in PG front matter |
| Seneca — Morals (L'Estrange) | 147,931 | Adapted/condensed, not literal translation |
| Lucretius — On the Nature of Things | 113,996 | Leonard 1921 |
| Kierkegaard — Selections | 113,898 | Anthology 1923 Hollander, not Either/Or |
| Plato — Timaeus | 99,788 | |
| Plato — Theaetetus | 88,896 | |
| Plato — Gorgias | 79,987 | |
| Plato — Apology/Crito/Phaedo (Henry Cary) | 70,636 | Multi-dialog; requires segmentation before training |
| Descartes — Six Metaphysical Meditations | 52,600 | Molyneux 1680; archaic English |
| Plato — Phaedrus | 50,082 | |
| Plato — Parmenides | 47,248 | |
| Plato — Protagoras | 36,841 | |
| Aristotle — Poetics | 20,557 | |
| Aristotle — Categories | 18,759 | |

---

## Notes and Observations

**Aquinas still dominates.** The Summa Theologica contributes 20.4% of all tokens — down from 22.5% as the corpus has grown. Still the single largest concentration risk for period balance in training data.

**Plato is now the second-largest author.** New Jowett dialogues (Laws, Timaeus, Theaetetus, Gorgias, Phaedrus, Protagoras, Parmenides) plus the Cary multi-dialog work add ~783K tokens to bring Plato's total to 1.32M tokens across 13 documents. The Plato corpus is now broadly representative of the dialogues available in public-domain English.

**Multi-edition works retained.** Several works have multiple documents from different editions (Republic ×2, Phaedo ×2, Discourse on Method ×2, etc.). Token counts include all editions. Training data preparation should apply version selection or down-weighting for near-duplicate content.

**Seneca L'Estrange adaptation flagged.** PG 56075 is a condensed/adapted paraphrase, not a direct translation. It is useful as philosophical secondary content but should be weighted accordingly. No strict primary-text Seneca Letters (Epistulae Morales) is available on Project Gutenberg; this remains a gap.

**Descartes Meditations is the 1680 Molyneux translation.** The English is archaic. The Standard Ebooks collection `rene-descartes/philosophical-works/john-veitch` (medium confidence, not yet acquired) contains the more standard Veitch Meditations and should be considered for acquisition.

**Kierkegaard gap remains.** PG 60333 is a 1923 selections anthology. No complete major Kierkegaard work (Either/Or, Concluding Unscientific Postscript) is available on Project Gutenberg in English.

**`processor_revision` is null.** The tokenizer was loaded without pinning a specific HuggingFace revision. Future runs should capture and record the processor revision hash for reproducibility.

**Context length not applied.** No truncation was applied during token counting. Documents longer than the model's context window will need chunking before SFT or retrieval use.

**Scale.** At 15.1M tokens, this corpus is still a small pilot relative to the 10B-token target in the agent spec. Remaining Gutenberg gaps, Standard Ebooks acquisition, and HathiTrust/Internet Archive OCR expansion are required to reach training-scale volume.

---

## Remaining Gutenberg Gaps (Tier 1 Works Not Found)

These tier_1_canonical_primary works in the manifest have no available English Gutenberg source:

| Work | Reason |
|---|---|
| Aristotle — Metaphysics | No English edition found on Gutenberg |
| Anselm — Proslogion | No English edition found on Gutenberg |
| Aquinas — Summa Contra Gentiles | Not found on Gutenberg |
| Bentham — Introduction to Principles of Morals and Legislation | Not found on Gutenberg |
| Cicero — De Officiis | Only Latin (PG 47001); no English |
| Hegel — Phenomenology of Spirit | Not found on Gutenberg |
| Hegel — Philosophy of Right | Not found on Gutenberg |
| Leibniz — Monadology | Only German and French editions on Gutenberg |
| Marx — Capital | Only Spanish and Greek on Gutenberg |
| Nicholas of Cusa — De Docta Ignorantia | Not found on Gutenberg |
| Pascal — Pensées | Not found on Gutenberg |
| Plotinus — Enneads | Not found on Gutenberg |
| Sextus Empiricus — Outlines of Pyrrhonism | Not found on Gutenberg |

These should be sourced from Standard Ebooks, Internet Archive, HathiTrust, or Perseus in a future acquisition pass.
