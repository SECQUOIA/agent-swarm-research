# Whole-manuscript review: root assessment

Reviewed version: `process/snapshots/stage08-round01`, 31 files, manifest
SHA-256 `d487e138b70585e03d5affa52a23e03631a30a45165651ddbe9d286162643231`.

All five independent reviewers completed a reading of every section, appendix,
proof and example. Root read all five final reports in full and assessed them
against the source and the independent checks recorded in
`stage08-root-reading.md`. Reviewers 01, 02 and 04 identified no required
corrections. Reviewers 03 and 05 each identified one minor issue. No reviewer
identified a major issue, and root identified no additional major issue.

## Accepted findings

1. **S8-1, minor, reviewer 03 R3-1: computational export dependencies.**
   Accept. The manuscript's LaTeX inputs are standalone, but the computational
   drivers import sibling repository modules and read historical data outside
   the paper folder. An exported supplement must contain the complete closure
   of the commands it documents, including measured source versions and their
   provenance. Create and test a self-contained computational ZIP that preserves
   these relative paths. Include the supporting historical records. Do not
   replace the reported timings or label them as new measurements.
2. **S8-2, minor, reviewer 05 R05-1: signed sparse-power objective.**
   Accept. In Example `ex:sparse-power-output`, replace the ambiguous phrase
   "Their difference" with the explicit upper objective
   `x^{2/p}-x^{1/p}` (equivalently `z_2-z_1`). The completed square already
   specifies this sign and the proof is correct for it. This is a local
   clarification, not a change of theorem or output lower bound.
3. **S8-3, minor, root literature follow-up: pessimistic coupling constraints.**
   Reviewer 01 surfaced an inaccessible publisher result without relying on it.
   Root subsequently read the accessible primary manuscript and the published
   article: Henke, Lefebvre, Schmidt and Thürauf, *On Coupling Constraints in
   Pessimistic Linear Bilevel Optimization*, JOTA 210, article 25 (2026),
   DOI `10.1007/s10957-026-03026-x`, published July 13, 2026. Section 2 uses
   nonempty follower responses and universal upper-row feasibility, matching
   the convention relevant here. Section 3 proves polynomial-size reformulations
   between the linear model variants with preservation of projected global
   optimizers under its standing assumptions. Theorem 3.3 explicitly introduces
   the full vector `bar y` among the leader variables, so this route does not
   preserve a fixed leader dimension as follower dimension grows. Add a concise
   comparison after the Ketkov--Prokopyev paragraph and its verified citation.
   This credits an additional related reformulation; it changes no theorem,
   novelty claim or proof and is minor.

No findings are rejected or deferred. All three accepted findings must be closed
by a separate correction agent before final acceptance. Since these corrections
do not change the scientific arguments, no further five-reviewer round is required by the
user's major-issue rule unless the correction or verification reveals a major
issue.

## Delivery and verification requirements

The correction agent will also prepare the final PDF and a clean LaTeX source
ZIP, with blank authors and no internal development records or literature
originals in either submission archive. The computational archive must contain
its own concise README, actual dependencies, raw records and measured-version
mapping. Document precisely which computations it reproduces. Update the paper
README to describe the deliverables, leaving root acceptance pending until root
checks the correction report and artifacts.

Root will inspect every changed manuscript line, verify preservation of all
other scientific sources and raw records, extract both archives outside the
repository, build the actual source export, run the complete diagnostic driver,
regenerate the three tables byte-for-byte, and check the measured-source
mapping. Root owns final acceptance, status and the accepted snapshot. A clean
review is evidence of diligence, not a guarantee of exhaustive priority or
journal acceptance.

## Correction verification and acceptance

Root read the complete separate correction report `process/stage08-corrections.md`,
its command outcomes and manifest, and the exact difference against the reviewed
snapshot. Only the two specified prose passages and the new citation change the
scientific inputs. The other 27 of the 31 reviewed files are unchanged; the fourth
changed file is the delivery README. Root later updated only acceptance records
and the coverage inventory. All proofs, computational sources, figure/table
inputs and measured data are preserved.

Root independently extracted both actual ZIPs into
`/tmp/bilevel-final-root-exdokm8y`, removed `PYTHONPATH`, verified their complete
file inventories and hashes, and confirmed that no process or literature tree
is exported. The source archive builds cleanly to 78 pages with blank authors;
its extracted PDF text is identical to the delivered `paper.pdf`. The final
LaTeX log has no warnings, undefined references, overfull or underfull boxes.
Root visually inspected the changed comparison, example and citation on pages
3, 28 and 76. The 54-entry bibliography resolves.

The extracted supplement passes its integrity verifier and all 11 measured
input mappings. Root separately checked the 60 distinct successful worker keys,
the unchanged raw-record hash, all five diagnostic families, and byte-identical
regeneration of the three tables. The correction agent independently exercised
every other documented non-timing command, including eight boundary scripts
and figure generation. Their complete outcomes were inspected. The source and
archive hashes remained unchanged throughout root verification. No new timing
campaign was needed or represented as completed.

Root's executable check and full outcomes are in
`verification/stage08-root/verify_final.py` and `manifest.json`. The final
delivery identities are recorded in `delivery/final-artifacts.json`.

**Decision: accept stage 8 and the complete manuscript.** All three accepted
minor issues are closed. There is no identified unresolved major or minor
issue and no missing in-scope development or proof obligation. The corrections
did not reveal a major issue, so the user's required review cycle is complete
without another five-reviewer round. The manuscript is ready for submission
as a complete theoretical optimization paper with computational supplements.
This assessment does not assert that future research or journal referees can
never suggest improvements.

Final accepted snapshot: `process/snapshots/stage08-accepted`, 39 files,
manifest SHA-256
`22466375e8acb78cd06879ba48b5051efbe9bdef2939e668c715252431cc5327`.
The snapshot includes the PDF and final archive-identity manifests; the ZIPs
remain the separately hashed submission artifacts. Acceptance-only README and
coverage updates occurred after the recorded root archive verification and
did not change any exported byte.
