# Stage 1 independent review 03, round 01

Reviewer: `/root/reviewer03`. Date: 19 September 2026.

## Verdict

Proceed after two minor wording corrections. I found no major issue in the authored Stage 1 content. The empirical scope is appropriately narrow, its central numbers agree with independent queries of the raw results, and the contribution does not depend on an unsupported priority claim. Empty later-stage sections were treated as reserved inputs, not defects. I did not read other current reviews or edit manuscript sources.

## Major issues

None identified in this stage.

## Minor actionable issues

1. **Name the timing statistic and the averaging qualification in the introductory results.** `sections/introduction.tex:12` says “timing averages” and “ESH uses fewer cuts and LP iterations on the matched cohorts.” Change the first to “shifted geometric mean wall times” and the second to “ESH has lower mean cut counts and LP iterations on the matched cohorts” (or equivalent). The independent computation supports the stated approximately 4–6% gain, but the current wording leaves readers to infer an unspecified statistic and can suggest an instancewise work reduction. The reported work comparison is an arithmetic cohort mean. The later planned results will explain this in detail, but the introduction can be precise at negligible length cost.

2. **Limit disaggregation to the hull variant.** `sections/related-work.tex:17` says “The present implementation instead maintains disaggregated variables” while the introduction explicitly includes big-M masters. Say “Our hull variant instead maintains disaggregated variables” and then explain that the radial tangent generation is shared with the big-M variant if useful. This keeps the distinction from Kronqvist–Misener accurate without suggesting the big-M master has hull variables.

## Verification and evidence

I independently read `main.tex`, `references.bib`, `README.md`, both authored section files, the evidence maps, and the Stage 1 author record. I compared the coverage map and prose against `notes/lbesh-study-results.md` and inspected the schemas and contents of the final analysis and derived artifacts.

A read-only inline Python query loaded the original JSONL records, used their saved numerical `assessment.solved` values, constructed common-solved cohorts, and independently recomputed the following. This checks arithmetic and correspondence with retained outcomes; it is not a new original-model witness audit.

- Generated controls: 51 distinct instances, including 33 held out and 18 pilot.
- Held-out single-tree accepted solves in all three schedules: ESH 33/33 with each formulation; ECP hull 32/33 and big-M 31/33. Common-solved cohort sizes are 32 and 31.
- Independently computed percentage reductions in the one-second-shifted geometric mean wall time: hull 5.941%, 4.941%, 5.946%; big-M 4.257%, 5.397%, 6.235%. “Approximately 4–6%” is supported.
- Primary matched mean cut counts: hull single 877.94/940.00, hull multi 477.93/507.63, big-M single 1268.26/1419.68, big-M multi 632.69/773.59 for ESH/ECP. The LP-iteration means are also lower for ESH in all four cohorts. The recorded cut-generation times are higher in every cohort, consistent with the introduction.
- External inputs: all 27 models; equal accepted solve counts for ESH/ECP within each pair (19 hull single and 20 in each remaining configuration).
- Default single-tree pilot accepted results total 69/72. In the corresponding no-integer-NLP ablation only ESH hull has one accepted result; the other three variants have none. The introduction correctly says integer-point recovery rather than claiming no NLP work.
- Quadratic conic run: all nine results accepted. All-nine shifted mean wall time 0.454825 seconds versus 2.280492 seconds for ESH hull single, a ratio of 5.013997. The Stage 1 prose correctly describes a strong available alternative without a universal performance claim.
- The eight declared benchmark files contain 663, 132, 132, 9, 351, 144, 9, and 24 records, totaling 1,464 exactly, matching `evidence/coverage.md:15`.

The first version of the read-only Python query assumed every baseline row contained `instance_metadata` and exited with `KeyError`; I corrected it by mapping metadata by instance from records that contain it. The corrected complete query finished successfully. No data files were changed.

Primary literature spot checks used `web.run` to open and inspect:

- [Gusev–Bernal Neira v2](https://arxiv.org/html/2508.16093v2): version/date, section 3.2 and the lifted CEHR equations. The equation and bounded zero-weight interpretation in `related-work.tex` agree with the source. The manuscript does not misrepresent this as a different limiting hull.
- [Kronqvist–Misener author manuscript](https://optimization-online.org/wp-content/uploads/2020/08/7957.pdf): its explanation of independent convex subproblems per disjunction term and avoidance of the perspective formulation supports the stated procedural distinction.
- [Nguyen–Pulsipher](https://arxiv.org/abs/2608.27707): its abstract explicitly generalizes logic-based OA and cutting-plane methods to infinite-dimensional GDP, supporting the restrained adjacent-work sentence.

The affine perspective identity in `related-work.tex:7–12` is algebraically correct: differentiating the perspective at any positive-weight point with ratio `z` gives the stated homogeneous tangent coefficients. The quadratic lifted constraints similarly imply the perspective row for positive weight and force the auxiliary variable to zero at zero weight under scaled bounds.

No LaTeX build, optimizer run, project-wide check, CI inspection, or independent revalidation of stored witnesses was performed. Those were unnecessary for these two minor prose corrections and are not claimed here.
