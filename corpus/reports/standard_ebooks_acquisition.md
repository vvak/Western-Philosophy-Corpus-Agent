# Standard Ebooks Acquisition Report

Most recent update: 2026-04-12 (Pass 4 — Standard Ebooks)

This report validates the raw Standard Ebooks acquisition results under `corpus/raw/standard_ebooks/` against the high-confidence Standard Ebooks records in `corpus/manifests/versions.jsonl`.

No normalization, deduplication, segmentation, or boilerplate removal was performed during acquisition.

## Summary

- Manifest records (standard_ebooks, high-confidence): 21
- Raw Standard Ebooks record directories created: 21
- Metadata sidecars created: 21
- EPUB files downloaded: 21
- Failed downloads: 0
- Total raw EPUB bytes: 16,872,592

## Artifact Status Counts

- `downloaded`: 21
- `skipped_existing`: 0
- `failed`: 0

## Download URL Pattern

Standard Ebooks serves EPUB files at:

```
https://standardebooks.org/ebooks/{source_id}/downloads/{slug}.epub?source=download
```

where `{slug}` is `{source_id}` with `/` replaced by `_`. The `?source=download` query parameter is required: without it, the server returns an HTML "Your Download Has Started!" page with a `<meta http-equiv="refresh">` redirect, not the binary EPUB.

## Byte Counts by Record

| Version ID | EPUB Bytes |
|---|---:|
| `plato_dialogues_jowett_se` | 2,900,347 |
| `augustine_city_of_god_dods_wilson_smith_se` | 1,498,639 |
| `hobbes_leviathan_se` | 1,048,387 |
| `boethius_consolation_james_se` | 1,020,830 |
| `william_james_varieties_religious_experience_se` | 877,017 |
| `smith_moral_sentiments_se` | 767,924 |
| `aristotle_nicomachean_ethics_peters_se` | 784,895 |
| `dewey_democracy_education_se` | 738,427 |
| `marcus_aurelius_meditations_long_se` | 643,395 |
| `william_james_pragmatism_se` | 661,195 |
| `locke_two_treatises_se` | 655,054 |
| `hume_enquiry_human_understanding_se` | 590,174 |
| `nietzsche_beyond_good_evil_zimmern_se` | 608,262 |
| `nietzsche_zarathustra_common_se` | 592,625 |
| `nietzsche_genealogy_morals_samuel_se` | 550,921 |
| `wollstonecraft_vindication_woman_se` | 492,255 |
| `rousseau_social_contract_cole_se` | 504,466 |
| `russell_problems_philosophy_se` | 501,284 |
| `mill_on_liberty_se` | 528,397 |
| `marx_communist_manifesto_moore_se` | 530,958 |
| `machiavelli_prince_marriott_se` | 377,140 |
| **Total** | **16,872,592** |

## Pass 4 Acquisitions (2026-04-12)

All 21 records are new Standard Ebooks acquisitions:

| Version ID | Work | Translator(s) | Source ID | SE Release |
|---|---|---|---|---|
| `plato_dialogues_jowett_se` | Plato: Dialogues (collection) | Benjamin Jowett | plato/dialogues/benjamin-jowett | 2022-06-25 |
| `aristotle_nicomachean_ethics_peters_se` | Aristotle: Nicomachean Ethics | F. H. Peters | aristotle/nicomachean-ethics/f-h-peters | 2018-12-03 |
| `marcus_aurelius_meditations_long_se` | Marcus Aurelius: Meditations | George Long | marcus-aurelius/meditations/george-long | 2014-05-25 |
| `augustine_city_of_god_dods_wilson_smith_se` | Augustine: The City of God | Marcus Dods, George Wilson, J. J. Smith | augustine-of-hippo/the-city-of-god/marcus-dods_george-wilson_j-j-smith | — |
| `boethius_consolation_james_se` | Boethius: The Consolation of Philosophy | H. R. James | boethius/the-consolation-of-philosophy/h-r-james | — |
| `machiavelli_prince_marriott_se` | Machiavelli: The Prince | W. K. Marriott | niccolo-machiavelli/the-prince/w-k-marriott | — |
| `hobbes_leviathan_se` | Hobbes: Leviathan | — (original) | thomas-hobbes/leviathan | — |
| `locke_two_treatises_se` | Locke: Two Treatises of Government | — (original) | john-locke/two-treatises-of-government | — |
| `hume_enquiry_human_understanding_se` | Hume: Enquiry Concerning Human Understanding | — (original) | david-hume/an-enquiry-concerning-human-understanding | — |
| `rousseau_social_contract_cole_se` | Rousseau: The Social Contract | G. D. H. Cole | jean-jacques-rousseau/the-social-contract/g-d-h-cole | — |
| `smith_moral_sentiments_se` | Adam Smith: Theory of Moral Sentiments | — (original) | adam-smith/the-theory-of-moral-sentiments | — |
| `wollstonecraft_vindication_woman_se` | Wollstonecraft: A Vindication of the Rights of Woman | — (original) | mary-wollstonecraft/a-vindication-of-the-rights-of-woman | — |
| `marx_communist_manifesto_moore_se` | Marx & Engels: The Communist Manifesto | Samuel Moore | karl-marx_friedrich-engels/the-communist-manifesto/samuel-moore | — |
| `mill_on_liberty_se` | Mill: On Liberty | — (original) | john-stuart-mill/on-liberty | — |
| `nietzsche_beyond_good_evil_zimmern_se` | Nietzsche: Beyond Good and Evil | Helen Zimmern | friedrich-nietzsche/beyond-good-and-evil/helen-zimmern | — |
| `nietzsche_zarathustra_common_se` | Nietzsche: Thus Spake Zarathustra | Thomas Common | friedrich-nietzsche/thus-spake-zarathustra/thomas-common | — |
| `nietzsche_genealogy_morals_samuel_se` | Nietzsche: The Genealogy of Morals | Horace B. Samuel | friedrich-nietzsche/the-genealogy-of-morals/horace-b-samuel | — |
| `william_james_pragmatism_se` | William James: Pragmatism | — (original) | william-james/pragmatism | — |
| `william_james_varieties_religious_experience_se` | William James: The Varieties of Religious Experience | — (original) | william-james/the-varieties-of-religious-experience | — |
| `russell_problems_philosophy_se` | Russell: The Problems of Philosophy | — (original) | bertrand-russell/the-problems-of-philosophy | — |
| `dewey_democracy_education_se` | Dewey: Democracy and Education | — (original) | john-dewey/democracy-and-education | — |

## License Basis

All Standard Ebooks releases used here:
- Source texts are US public domain (published before 1928 or otherwise verified).
- SE editorial contributions are dedicated to the public domain via CC0 1.0.
- Rights statements are published on each SE ebook page.

## Metadata Coverage

Every Standard Ebooks manifest record has:
- A record directory named `se_{source_id_slug}_{version_id}`
- A `metadata.json` sidecar
- A raw `{version_id}.epub` file

## Validation Result

All 21 high-confidence Standard Ebooks manifest records acquired. No failed artifacts. No missing files or metadata sidecars.
