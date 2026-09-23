# Stage 5 author report: integrated manuscript and source delivery

Author: `/root/formal_author`; completed 2026-09-14. This is the Stage 5 author
handoff, not stage acceptance or the final whole-manuscript review. Five
independent Stage 5 reviewers are the coordinator's next step.

## Manuscript changes

- Completed the abstract with the actual integration, focused formal result,
  historical and primary outcomes, exact primal cases, and catalogue scope.
- Rewrote the contribution statement around exact model/cut/master/proof
  integration, machine-checked mathematical interfaces, and reproducible
  reliability evidence. No broad or qualified priority claim was introduced.
- Integrated Jansson (2004, 2009), Messine–Trombettoni (2019), and Elloumi et al.
  (2025), with publisher-deposited metadata independently checked and saved in
  `stage05-literature-metadata.json`. Read the relevant author manuscripts for
  the latter three; Jansson 2004 uses institutional abstract/metadata only.
  The QIBEX-R comparison describes its reported method and does not validate its
  implementation or assert absence of proof export. Correctly uses the 2025
  journal issue year despite 2024 online publication.
- Clarified that Baes et al.'s Theorems 1 and 3 bound the number of certificate
  points, not the bit length of their real data; rechecked the local full text.
- Added attribution next to the finite-box correction. No accepted mathematical
  statement or proof changed. The correction remains an application of support
  minimization, with explicit replay-specific enclosure/domain obligations.
- Added a compact TikZ architecture diagram in Section 4. It distinguishes
  saved evidence, complete replay, and objective-preserving transfer without
  suggesting an executable Lean connection. Rendered and visually inspected
  its PDF page (page 13); text and arrows fit and are legible.
- Completed Section 7 with practical consequences, the preserved versioned
  failure evidence, proof-size/domain/coverage limits, and formal/software trust
  distinctions. Removed an optional-extension list following root feedback;
  the conclusion focuses on the completed scoped contribution.
- Added Appendix A with paper, Lean, checker-only core, bulk, version-restoration,
  and generation instructions; actual byte counts and honest data availability.
  No public upload, DOI, author identity, affiliation, or solver license was
  invented. Anonymous review author attribution remains.
- Replaced conditional section inputs with mandatory inputs, so missing required
  sections fail the build. Added TikZ dependencies to the preamble.
- Updated current repository/literature evidence maps to the final actual state,
  preserving all dated process reports and accepted source snapshots.

The final scientific distinctions are preserved: historical replay 188/92/9;
frozen primary V1 replay 203/19/67; separate V2 twelve/twelve and V3 two tls12
proof checks; the expected full V3 primary count 204/18/67 is explicitly an
expectation, not an unperformed new full replay; catalogue 222 matching-model
entries from 405 accepted records; final current tests 161. Reference metrics
remain unverified-reference differences, exact original-model primal witnesses
remain separate, and no solver speed or universal coverage superiority is claimed.

## Portable source delivery

Added:

- `README.md`: concise deliverable map and build/reproduction instructions.
- `scripts/build-paper.sh`: compiles only current required sources in a fresh
  temporary directory, then copies the final PDF/bibliography to the paper root.
  This avoids the known stale root auxiliary/bibliography issue.
- `scripts/package-source.py`: deterministic explicitly inventoried source
  packaging, excluding experimental archives and all dependency/build caches.
- `certified-minlp-paper-source.tar.gz`: **476,878 bytes**, SHA-256
  `11e566f2d7aa8e4ca589928635034bc3914625afa5c3d4f76ca81a5f0e4f08d8`.
  Its 49 entries include all source sections/tables/bibliography, reproduction
  scripts and current maps, and the complete focused formal sources, exact
  pins, audit scripts, coverage, and saved verification records.
- `PAPER-SHA256SUMS`: file-level hashes included inside that archive.
- `paper-source-archive.json`: external source-archive index.

The source archive includes neither `main.pdf` nor a stale `.bbl`; it rebuilds
its PDF and bibliography from sources. The current root `main.pdf` and
`main.bbl` are both replaced by the clean integrated build. Core and bulk stay
separate. The archive contains no `.lake`, duplicate build tree, user literature
PDF, installed dependency or experimental proof archive.

## Validation

1. Fresh source build passes with no LaTeX warning, undefined citation/reference,
   overfull or underfull box. Delivered PDF is **32 pages, 522,212 bytes**.
   Logs: `build/current-build.log`, `build/current-main.log`; extracted PDF
   text: `build/current-main.txt`.
2. Extracted the final source archive into a new temporary directory and verified
   all `PAPER-SHA256SUMS` entries. Also verified all accepted focused formal
   hashes using `formal/verification/SHA256SUMS`. No formal source or pinned
   dependency changed, so no redundant Lean rebuild was run.
3. Compiled the extracted archive with its documented plain latexmk command.
   No warnings; its bibliography bytes and PDF extracted text exactly match
   the delivered root build. The archive has no missing required resource or
   private repository dependency for compilation. Details and path are in
   `stage05-source-extraction.json`; command logs are `stage05-extracted-1.log`,
   `stage05-extracted-2.log`, `stage05-extracted-3.log`.
4. Repeated source packaging without source edits and obtained the identical
   compressed hash, confirming the deterministic packaging claim.
5. Checked current core digest and core/bulk sizes against `supplement/archives.json`.
   Core remains **6,478,558 bytes**, SHA-256
   `80ef5d50faefc97e01832f06b1f730a3a906b7d5b2ca9d8609453df9561f1fc6`.
   Bulk remains **30,664,561,063 bytes** with the previously accepted digest
   `88c23497c2d20c76b3ac25cfc2c60a529aecb35da98e8de00213f4513ed314d4`.
   Bulk contents were not read or rebuilt. No experimental campaign, proof
   replay, checker test or mathematical implementation was rerun or changed.

All sources, final PDF/bibliography, source archive/index, and relevant validation
records are frozen by `stage05-author-manifest.json` for the required review.
