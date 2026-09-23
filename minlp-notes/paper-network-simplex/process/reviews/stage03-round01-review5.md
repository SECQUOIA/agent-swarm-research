# Stage 3, round 1 — independent review 5

## Verdict and findings

**No major or minor issues found.** I recommend accepting this stage. The original-coordinate descriptions, exact separation procedures, and constructive recovery arguments are complete for their stated graph classes. The change of signs between the theta coordinates and the parallel-path coordinates is explicit and consistent.

Enumerated findings: **none**.

## Mathematical review

1. **State domains and signs.** Checked that the three theta path deviations are `s,t,-s-t`, with the third sign absorbed into `sigma_e`, so the bounds and observations for `h=s+t` have the correct sign. The later parallel-path section deliberately returns to the original `epsilon_e` convention, where all path deviations sum to zero. The merged state has no observations; repeated observations on a path enter both endpoint lists and cannot silently disagree. Finite scaled bounds handle zero weights correctly.
2. **Theta feasibility and supports, Lemma 5.1.** Checked the five nonemptiness inequalities and all six tight support formulas by direct interval elimination. Every claimed support is attained, including collapsed intervals and segment or point domains.
3. **Planar sums, Lemma 5.2.** Checked the exposed-face argument for two-dimensional sums and its separate treatment of segments and points. An exposed edge of a two-dimensional sum cannot acquire a direction absent from all summands. The line-enforcing normals and remaining varying coordinate forms also suffice when the sum is one-dimensional. The caution that this reasoning does not generalize directly to higher-dimensional facets is appropriate.
4. **Cycle/theta hull and coefficient bounds, Theorem 5.3.** The local nonemptiness checks together with the aggregate supports exactly characterize the local Minkowski sums. The prior shared-simplex block theorem then gives the global result. Expanding convex lower branches and concave upper branches gives valid finite linear families. The distinct coordinate types and distinct state indices prevent repeated product coefficients; distinct representative arcs preserve the unit flow coefficients.
5. **Separation semantics.** Freezing an active affine branch of a violated convex left side produces a global inequality valid for the hull and with identical positive violation at the candidate. It is not merely a pointwise tangent or a heuristic. The original domains are included in the oracle checks. Tie choices are harmless.
6. **Constructive recovery, Proposition 5.4.** Checked the suffix-support intersection, the point-choice formula, and preservation of the remaining-sum invariant. The proof verifies all upper bounds of the chosen point, not only its lower bounds. The empty suffix forces the final remainder to zero. Normalizing explicit and merged states only at positive weights gives the desired global graph-point decomposition. The default-and-exception representation correctly avoids writing every dense flow vector during the stated linear arithmetic algorithm.
7. **Joint-state example, Example 5.5.** Each separate one-label decomposition sums to the stated aggregate flow and satisfies its two scaled state polytopes. The two labels together would require third-arc state flow `2/3` against an aggregate third-arc flow `1/3`. The displayed residual inequality has exact violation `1/3`. Use of `X_s,X_t` for actual aggregate flows distinguishes these from signed deviation coordinates.
8. **Parallel-path subset hull, Theorem 5.6.** Checked necessity, the lower-endpoint shift, nonnegativity of row targets derived from complementary subsets, agreement of total row and column targets, and the minimum cut calculation after fixing source-side rows. Adding back the lower endpoints gives exactly the stated subset inequality. The zero-total-target case is covered. Branch expansion again preserves the unit flow/product coefficient bound.
9. **Parallel-path oracle.** A negative shifted row target supplies the stated valid lower-bound cut. Otherwise a maximum flow either gives a feasible state matrix or a cut whose row subset violates the explicit description. Optimizing the column side choices can only decrease the cut capacity, so extracting only the source-side row set is sufficient. Active affine choices give a valid upper majorant of the concave subset right side, with the same candidate value.
10. **Complexity and scope.** Recomputed the transportation node and arc counts. The preprocessing and matrix storage bounds include `k_B(a_B+1)`, so no unwarranted linear-in-sparse-observations assertion is made for growing path counts. Shortest augmenting paths gives a capacity-independent polynomial iteration bound; clearing rational denominators has polynomial encoding length. The paper distinguishes rational arithmetic costs, bit costs, dense-output costs, and the generic known LP separation result. The exclusion of arbitrary nested series–parallel blocks is clear.

## Independent exact executable checks

I wrote `verification/reviewer5/stage03-round01/check_geometry.py` without importing any repository theorem implementation. It passed the following checks, retained in `check_geometry.json`:

- All **3,375** triples of intervals with endpoints in `{-2,-1,0,1,2}`, including singleton intervals: feasibility agrees with independent boundary-intersection enumeration; all six support formulas and the point-selection rule are correct on the **2,487** nonempty domains.
- **400 exact Minkowski-sum comparisons**, using independent convex hulls of sums of vertices versus polygons from the summed six supports. Rational arithmetic and exact planar orientation tests are used.
- **400 exact sequential recoveries** for families of one to nine state polygons. Every recovered point satisfies its own domain and the final aggregate remainder is zero.
- **500 parallel-path cases** with two to four paths and one to three states: all subset inequalities agree with exhaustive enumeration of bounded integer column vectors and their possible aggregate sums. In these integral transportation cases, integral vertices make the discrete feasibility comparison exact for the integral targets.

These checks supplement the general proofs. They do not constitute a check of the production graph-extraction or maximum-flow implementation.

## Coverage against the original result files

Read both `results/network-simplex-cycle-theta-hull.md` and `results/network-simplex-parallel-path-hull.md` in full. The stage includes their substantive mathematical developments:

- signed block coordinates and sparse local state grouping;
- exact state and aggregate conditions;
- unit flow/product coefficient descriptions;
- linear cycle/theta separation and compact constructive recovery;
- the joint-state obstruction example;
- arbitrary parallel-path transportation formulation and complete subset cuts;
- exact flow-based separation, state reconstruction, and the unbounded-path complexity qualification;
- the boundary between parallel-path blocks and general series–parallel blocks.

Prior disaggregation, block gluing, and model-transform limitations are already present in accepted foundations, so their reuse here is appropriate. Historical numerical verification counts, implementation comparisons, and the later bounded-rank or series–parallel results are not duplicated in this section; those belong to the scheduled later stages. I found no material mathematical omission from either original result file. Classical Minkowski-sum, flow, transportation, and network-Cayley ingredients are credited rather than presented as new general mechanisms.

## Build and visual presentation

Built a private frozen-snapshot copy using the documented LaTeX command. The final PDF has **20 pages**, and its final log contains no warnings, unresolved citations or references, or overfull/underfull boxes. The normal first-pass missing bibliography notice resolved during the build.

Visually inspected pages **15 and 16**, covering the full constructive recovery proof, the joint-state example, the sign transition to parallel paths, and the subset theorem. All displayed equations and theorem text fit within the margins and remain legible. The exposition gives sufficient intermediate explanations to follow both the recovery construction and the transportation reduction without consulting the research notes.

## Limitations and independence

This is a review of the frozen Stage 3 mathematics and integration, not a definitive novelty search, a publisher-metadata audit, or validation of future implementation and benchmark sections. I did not read other current-round reports, coordinate findings, spawn agents, edit manuscript sources, or build in the shared snapshot. Evidence is confined to the assigned reviewer verification directory.
