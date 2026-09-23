# Source Quality

## Normalized Sources

- gutenberg: 309 deduped records, 32,636,281 tokens
- gutenberg quality tiers: tier_1_canonical_primary=103, tier_2_major_primary=165, tier_3_secondary=41
- standard_ebooks: 27 deduped records, 4,633,200 tokens
- standard_ebooks quality tiers: tier_1_canonical_primary=23, tier_2_major_primary=3, tier_3_secondary=1
- internet_archive: 31 deduped records, 6,146,869 tokens
- internet_archive quality tiers: tier_1_canonical_primary=20, tier_2_major_primary=6, tier_3_secondary=5
- ia_resolved: 80 deduped records, 14,594,429 tokens
- ia_resolved quality tiers: tier_1_canonical_primary=76, tier_4_ocr_expansion=4
- ia_resolved training eligibility: retrieval_only=4, training_candidate=76
- lane_b: 148 deduped records, 20,236,252 tokens
- lane_b quality tiers: tier_3_secondary=148
- lane_b training eligibility: training_candidate=148

Total reported tokens: 78,247,031

## OCR Quality Gate

- ocr_bronze: 14
- ocr_gold: 481
- ocr_silver: 27
- reject: 7

- `reject` OCR is skipped by IA-resolved and Lane B normalizers.
- `ocr_bronze` is retained as `retrieval_only` and assigned `tier_4_ocr_expansion`.
