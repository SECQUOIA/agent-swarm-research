# Frozen research supplement

`publication_bundle_v1.tar.gz` is the public export of the completed research record. Its current SHA-256 is `96c50c412dbea4386d530419570c0215685a40c43a96aac4a6b9c9c4aca8131e` and its size is 37,540,096 bytes. It contains 9,076 payload files plus the embedded publication manifest. Paths are relative to the original repository root (`code/`, `notes/`, `README.md`, `AGENTS.md`).

The archive preserves the exported executable source freeze (`source_v1.tar.gz`, current SHA-256 `06251680ac06cdb94b1ccfaca06191b38e0048a649a7746e6cb6a6535c5d17a9`), plans, all 1,464 benchmark records and native logs, 420 cone-reference calls, final analysis, model sources/licenses and pinned environment declarations. Historical intermediate material is provenance; use `analysis_v1` for final aggregates and retain repeats and follow-ups separately.

The adjacent manifest, checksum and original verification JSON are unchanged copies from the research record. `publication_bundle_verification_v1.json` records the original verification; the manuscript's fresh relocation audit is a distinct check. The paper's `scripts/verify_supplement.py` verifies every member and safely extracts to a new or empty directory. See the main README for complete commands.

The source archive intentionally omits this large `.tar.gz`. When using an extracted paper-source package, copy this separately delivered file into its `supplement/` directory. Model copyrights and license files remain as archived. No new blanket license is asserted for third-party sources.

Current manifests bind the exported bytes. Original source fingerprints identify the versions used by the recorded workers; the source audit checks those historical bindings separately from every current source-archive payload hash. Scientific results and historical verification receipts were retained.
