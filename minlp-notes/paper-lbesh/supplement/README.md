# Frozen research supplement

`publication_bundle_v1.tar.gz` is copied byte-for-byte from the completed research record. Its SHA-256 is `f0399194ca1c9c57421965e236302c62e10eb72846ab807f936f18d9927d4b26` and its size is 38,086,636 bytes. It contains 9,076 payload files plus the embedded publication manifest. Paths are relative to the original repository root (`code/`, `notes/`, `README.md`, `AGENTS.md`).

The archive preserves the original executable source freeze (`source_v1.tar.gz`, SHA-256 `6c9eaf9898f04d08a12381879ab9bae79f83b800f0db9e4cc696ccbff6be84ad`), plans, all 1,464 benchmark records and native logs, 420 cone-reference calls, final analysis, model sources/licenses and pinned environment declarations. Historical intermediate material is provenance; use `analysis_v1` for final aggregates and retain repeats and follow-ups separately.

The adjacent manifest, checksum and original verification JSON are unchanged copies from the research record. `publication_bundle_verification_v1.json` records the original verification; the manuscript's fresh relocation audit is a distinct check. The paper's `scripts/verify_supplement.py` verifies every member and safely extracts to a new or empty directory. See the main README for complete commands.

The source archive intentionally omits this large `.tar.gz`. When using an extracted paper-source package, copy this separately delivered file into its `supplement/` directory. Model copyrights and license files remain as archived. No new blanket license is asserted for third-party sources.
