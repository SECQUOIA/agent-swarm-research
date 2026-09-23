# Stage 4 independent review 4

Reviewed 2026-09-14. Focus: Section 6, its generated tables, frozen protocols, archive documentation and portable entry points, model attribution, source-version/timing labels, and the scientific scope of the reported evidence. I did not read peer reviews, rerun numerical generation, hash the bulk archive, or duplicate the separately assigned core execution review.

## Verdict

**No major Stage 4 issue found. One minor scientific-wording correction is requested.** The experimental design, retained denominators, separate repair cohorts, and distinction between proof acceptance and producer success are sufficiently explicit. The core/bulk packaging and portable instructions address the previous artifact-access limitation for a distributed submission supplement.

## Valid minor correction

**Avoid asserting the cause of the small `risk2bpb` reference discrepancy.** In `sections/06-experiments.tex`, subsection “What rejected proof steps reveal,” the sentence “The library string ... lies slightly beyond it because the strings have different precision” states a causal explanation stronger than the evidence supplied by a certified bound and an unverified reference string. Different displayed precisions make rounding a plausible explanation, but do not establish the provenance or feasibility of the reference value. Replace this with, for example: “The library string ... lies slightly beyond this bound; the difference is consistent with rounding at the reference's displayed precision.” This matches the appropriately qualified interpretation already used in the bound-quality subsection. It requires no new experiment.

## Scientific and numerical presentation

- Section 6 clearly preserves 299 selected names, the ten pre-attempt exclusions, and the 289 attempted denominator. It does not identify this frozen selection with all current MINLPLib models.
- The historical 81 revoked acceptances and 92 total rejections are correctly distinguished: eleven proof failures were already historical crashes. The section does not present all historical rejections as newly discovered false bounds.
- Primary production counts (198/67/8/4/12) sum to 289 and are kept separate from primary replay counts (203/19/67). The explicit treatment of completed files surviving timeouts or worker errors avoids inflating completed production. Canonical/fallback/default selection is fixed independently of bound quality.
- The V1 primary results remain preserved after V2 producer normalization and V3 report conversion repairs. The paper explicitly states that only one additional primary bundle is accepted by the corrected reporting layer, and the portable README states the expected 204/18/67 outcome using V3 rather than promising reproduction of V1 counts with changed code.
- The 405-record, 222-model catalog is labeled a union of accepted evidence, requires model hash/sense agreement, retains candidates and proof provenance, and is not attributed to the uniform search budget. This is an appropriate use of merged results.
- Historical accepted checking time, all-record checking time, and campaign elapsed time are separately labeled. Primary generation phase sums cover observed ended calls, distinguish incomplete observations, and are not confused with elapsed or pure-kernel time. The manuscript discloses six workers, shared-machine timing, WSL2, requested one-thread search, and proof-completion defaults.
- Signed exact reference discrepancies are not called optimality gaps. Negative discrepancies, failed sufficient nonlinear checks, locally invalid discrete inferences, and original primal infeasibility have distinct interpretations. The mixed-direction and gapped-split findings concern supplied rule justifications, with no unwarranted inference of false final objective bounds.
- The two printed-point audits are scoped to source formulas and saved points. The stated robust row-error bounds, 0.00265 and 0.0044, equal the respective coefficient absolute sums times 0.00005 and are much smaller than the reported violations. GAMS compilation and historical in-memory models are explicitly outside the source-equivalence claim. The exact 6545 optimum relies on a newly checked witness and matching bound, not a vendor status.

## Artifact and documentation inspection

I read the outer supplement README/index and, directly from the core tarball, the standalone README, attribution notice, source-version README, portable `reproduce.py`, and archived quadratic README. I also inspected the frozen uniform/replay-selection protocols and generated campaign, phase, repair, and catalog tables.

- The outer README correctly identifies both actual archive filenames, their exact byte counts and SHA-256 values, approximately 93.7 GB extracted bulk regular-file size, and the core-first path.
- The inner README distinguishes checker-only reproduction, optional tests, optional full replay, and licensed numerical generation. The broader original `uv.lock` is expressly provenance, not a portable installation recipe. The generator-specific package and executable requirements are separately stated.
- Full-replay paths resolve relative to the extracted layout; historical absolute paths are described as provenance. Both archives extract into the same `minlp-certified-evidence` tree. The bulk archive is optional for core examples, saved-record summaries, local failure extracts, and catalog regeneration.
- The core documents expected V3 acceptance differences and how to recover V1/V2 in a separate tree without corrupting the core manifest. It also distinguishes actual timed wrappers from later portable path corrections and preserves the frozen wrappers by hash.
- `reproduce.py small` invokes full checks for four bundles, uses the separate source/primal evaluator, and recomputes twelve historical plus three new local failed-step extracts. Its reports go to a new output directory. The historical extract script's default mode verifies supplied extracts without rewriting them.
- The preserved quadratic README has an explicit portable-supplement notice directing readers away from its original repository-relative commands and notes links. Consequently those archival links do not leave the advertised portable workflow dependent on missing repository notes.
- `ATTRIBUTION.md` identifies MINLPLib, maintainers/contributors, source/download URLs, CC-BY 4.0, unchanged frozen inputs, and the in-memory dedenting convention. It states that source snapshots need not match future downloads. Literature PDFs, vendor binaries/licenses, and proof-assistant caches are excluded.

## Boundaries of this review

The author record reports full bulk-member readback, extraction checks, and 161 tests. I inspected those documented scopes but did not independently repeat those resource-intensive checks; core execution is assigned to another reviewer. I found no documentary contradiction requiring a new bulk replay or generation campaign. Final manuscript integration and the additional literature stage are pending by design and are not treated as Stage 4 defects.
