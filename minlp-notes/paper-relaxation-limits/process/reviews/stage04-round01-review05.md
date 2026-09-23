# Stage 4, round 1: independent review 05

**Verdict: PASS.** No major or minor manuscript defect found. The new coordinatewise graph-lift theorem and its global relative-tolerance extension have complete proofs under their stated oracle, degree and full-graph agreement assumptions. The endpoint count, arbitrary-cover formulation, charged reductions and exact upper-tree sizes are correct.

**Coverage.** I reviewed the frozen files in `process/snapshots/stage04-round01/`:

- `sections/09-cardinality-spatial.tex`, in full;
- `sections/10-cardinality-preordering.tex`, in full;
- `sections/11-coordinate-domains-lifts.tex`, in full;
- `sections/12-relative-blocks-cuts.tex`, in full;
- `sections/01-foundations.tex` and `macros.tex`, including the vertex representation and precise absolute/relative certificate conventions used here;
- the Stage 4 inputs in `main.tex`, the five Stage 4 bibliography entries in `references.bib`, the snapshot manifest, the frozen build report, and the frozen author's exact checker and result JSON.

There is no separate Stage 4 appendix. The Stage 4 arguments do not require an earlier specialized positive-gap or signed-gap theorem: the used earlier mathematical facts are the elementary multiaffine vertex property and certificate definitions. I verified the six foundation/Stage 4 source hashes against the snapshot manifest. I inspected rendered frozen PDF page 59, containing the graph-lift model, theorem and substitution; the text and equations are readable.

I read `process/review-protocol.md`, `process/stage-04-review-assignment.md`, `process/stage-04-author-assignment.md`, the complete `process/stage-04-author.md` ledger and validation record, all Stage 4 rows of `process/scope-proposal.md`, and `process/univariate-lift-refinement.md`. Every Stage 4 scope row is represented in the frozen manuscript, including the improved lift result, the weaker literal-substitution comparison, fixed-demand exact certification, tolerances, asymmetry modulo balances and escape certificates.

The canonical repository sources read in full were:

- `results/spatial-bb-exponential-lower-bound.md`;
- `results/spatial-bb-sdp-rlt-exponential-lower-bound.md`;
- `results/spatial-bb-higher-sos-exponential-lower-bound.md`;
- `results/spatial-bb-product-domain-exponential-lower-bound.md`;
- `results/spatial-bb-relative-gap-exponential-lower-bound.md`;
- `notes/spatial-bb-known-clique-cut.md`.

The correction and source-context notes read were `notes/review-spatial-bb-lower-bound.md`, `notes/review-spatial-bb-second.md`, `notes/review-spatial-bb-sdp-rlt.md`, `notes/review-spatial-bb-higher-sos.md`, `notes/review-spatial-bb-product-domain.md`, `notes/review-spatial-bb-relative-gap.md`, and `notes/spatial-bb-strengthening-novelty.md`. Their previous verdicts were not used as mathematical premises. I did not read another report from this review round or spawn agents.

I read `literature/AGENTS.md` before using local originals. The primary-source checks were:

- **Padberg (1989):** directly inspected the original PDF page 11, printed page 149, Lemma 2 and equation (17). The source states the clique inequality for integer `1 <= alpha <= |S|-1`. Setting `S=[n]`, `alpha=k`, and multiplying the rearranged inequality by two gives exactly `eq:clique-cut`. The manuscript independently supplies continuous validity and root exactness; it imports no facet assertion. This is a user-supplied original, and no source image is retained for redistribution.
- **Grigoriev (2001):** directly inspected original PDF page 7, the normalized falling-factorial functional and Lemmas 1.3–1.4. The cardinality identity and classical square-positivity provenance agree with the manuscript. I did not audit the subsequent full proof of the stronger classical positivity range. That is not an unproved mathematical dependency here, because the manuscript gives its own sufficient Gram and localizer proofs.
- **Potechin (2019):** read Theorem 1, Example 18, and the knapsack parts of Theorem 44 and Corollary 45, including the knapsack parameter calculation. Visually checked Example 18 on original page 61:8. Its binomial-ratio moments equal the displayed falling-factorial moments, and the source explicitly attributes the knapsack obstruction to Grigoriev. I did not audit the full general symmetry machinery, which is not imported by Stage 4.
- **Jarre (2018):** read the binary-fixing framework in Section 2 and the SDP comparison in Section 3, and visually checked original page 4. This confirms the limited predecessor description. I did not treat the predecessor's algorithmic counting argument as a premise of the manuscript's spatial proof.
- **Coniglio:** my own access to the [anonymous review PDF](https://openreview.net/pdf/369974754b073802afab412ee5f715561c39adbc.pdf) returned an OpenReview verification challenge. I did not bypass it or independently read Appendix C. I read the later access entry in `verification/primary-source-checks.md`, which records the coordinator's successful review-version reading. The manuscript explicitly identifies that version and does not claim its identity with the published version. This remains an external verification limit for the contextual comparison, not a missing premise of any Stage 4 theorem.

Original PDF hashes and visual locators are recorded in `verification/reviewer05/stage04-round01/source-checks.json`.

**Findings.** None. In particular, the historical incorrect maximum in the endpoint-cover bound, unrestricted tolerance slogan, omitted intermediate upper children, and uncharged objective deletions have not survived into this snapshot. No repair is requested.

**Independent verification.** I reconstructed the proofs rather than relying on the author or historical review conclusions.

1. **Optimum, domination, witness count and upper certificates.** The balance polytope has precisely the stated vertices, since two strictly fractional coordinates permit an opposite perturbation. Every vertex has penalty `1/4`. For each interval, convex endpoint interpolation bounds every convex underestimator by the chord; using an infimum for arbitrary underestimators correctly permits discontinuous endpoint values.

   For a product set, membership of a witness implies `Z ∩ A = H ∩ D = empty`. The two marginal avoidance probabilities need not be independent. The witness fraction is bounded above by the smaller marginal upper bound, and `|A|+|D| >= |R|` yields the **minimum** of the two reciprocal bases in `mathcal N(q)`. The union bound uses only cover membership, permitting overlap, arbitrary split positions, and disconnected or nonclosed coordinate sets. Zero endpoint classes produce base one, and `q=0` gives one region. The chord proof's strict inequality is justified because a positive target forces a nonempty contributing middle class.

   The positive-tolerance construction has one intermediate upper node in addition to each low, middle and high child. Direct recursion gives `2^(n+2)-3` nodes and `2^(n+1)-1` leaves. The exact midpoint stopping thresholds are `c=k+1` and `d=n-k`; their Pascal recurrence gives `binomial(n+1,k+1)` leaves and twice that minus one nodes. Thus the complementary fixed-demand exponent is correctly `n-k`, not `n-k+1`. The middle target can be increased slightly for strict pruning. The interval error is bounded by one quarter of the sum of squared widths; evaluating the true objective at a chord minimizer transfers that bound to node optima.

2. **Charged propagation and tolerance.** With at most `aN` certified discarded regions and at most `N` final regions, the augmented cover has at most `(a+1)N` members. Pure feasibility deletions remove no witness. The box proposition expressly assumes certification of a closed slab before charging that closed box; it does not infer certification from closure. The product-domain version instead uses the exact removed coordinate set. For `delta<1/2`, every allowed sum stays strictly between `k` and `k+1`, giving optimum `1/4-delta^2`; the exact-balance witnesses remain feasible and yield the weakened chord target. The hypotheses `epsilon+delta^2<1/4` and the failure of the formula after an integer sum becomes feasible are explicit.

3. **Full SDP–RLT and affine closure.** On the free coordinates, the covariance is exactly `t(s-t)/(s(s-1))` times `I-J/s`; deterministic rows have zero covariance. This certifies the full augmented PSD matrix by a Schur complement. The four distinct-index slack expectations are `d,c-d,c-d,(s-t)(s-t-1)/(s(s-1))`; repeated free indices give `c,0,0,1-c`. A restricted index supplies a nonnegative deterministic factor, including degenerate intervals. All row balances and the objective follow directly. The diagonal mixed slack is the chord secant bound. Affine Farkas representations include a nonnegative constant and an unrestricted balance multiple; expansion proves the stated original-coordinate affine closure without granting lifted clique cuts.

4. **Fractional moments and the exact order range.** For a squarefree multiplier of degree `a <= 2d-1 <= s-1`, the cardinality recurrence never requires a zero denominator. The homogeneous replacement has strictly positive denominator; its difference from the original monomial is the balance times a quotient of degree at most `d-1`. Multiplying by `P+H` consumes at most degree `2d-1` in the equality multiplier. Vandermonde gives the incidence-Gram decomposition as a polynomial identity, including when a numerator vanishes. Every coefficient is nonnegative under the stated sufficient hypotheses.

   Boolean reduction handles repeated and conflicting slack factors. The uncancelled indicator identity gives nonnegative weight through degree `2r`. If the original square multiplier is nonconstant, the assignment uses at most `2r-2` distinct coordinates, making its weight positive. Conditioning then leaves `s-v >= 2d` and both conditional cardinalities at least `2d-1`. Constant and fully assigned cases require no conditional denominator. This proves every allowed square, including globally coupled ones. The negative-indicator argument correctly distinguishes full-preordering positivity from a sharper moment-matrix theorem.

   Since the exclusion count is an integer, `|R|<k-2r+2` leaves at least `2r-1` unit witnesses, and likewise for zeros. The separate `r=1` dimension check is valid. The constructed penalty is strictly below the non-strict certification threshold, including `R=empty`. The exact formulas for `q_r`, the perturbed threshold, `r<=3t/8+1`, and `r<=13t/32+1` follow. The text distinguishes positive `q_r` from a linearly growing one and does not divide by a zero target.

5. **Arbitrary product domains and degree-free graph lifts.** A coordinate with both endpoints present reduces every valid local polynomial to a nonnegative combination of its two endpoint indicators. Each nonconstant coordinate in the product expansion consumes at least one original factor degree. Fixing restricted coordinates cannot increase the square multiplier's degree. Consequently every localizer remains in the assignment-indicator lemma's range, without a compactness or hull assumption.

   For graph lifts the same argument is valid in lifted degree because each lifted variable maps to an affine polynomial or a constant. Restricted auxiliary values are actual finite witness values, and endpoint auxiliary values are actual graph values. Original coordinates and affine balances are retained, so every allowed balance multiplier still has degree at most `2r-1`. A locally vanishing equality reduces to zero, including after every global multiplier. Full-graph identities also vanish at all substituted Boolean points. Full-graph objective agreement, rather than agreement only on the balance slice, permits the decisive Boolean comparison even at assignments that do not satisfy the balance. Uniqueness of multilinear reduction gives objective agreement under the functional. This is a valid moment construction and does not equate a nonlinear function with its chord on a continuous interval. Finite but discontinuous or unbounded auxiliary functions cause no problem because covers are defined by preimages of the original feasible set. Literal polynomial substitution gives the weaker `rD` bound with balance-product degree `1+D(2r-1) <= 2rD`.

6. **Relative tensor extension, uniqueness and escape cuts.** For every global preordering expression, each block localizing matrix on degree-at-most-`d` monomials is PSD. Tensoring them and retaining only tuples of total degree at most `d` gives exactly the required global localizing matrix. Entries discarded from the tensor are merely part of a Gram construction and need not be global moments. Equality products factor monomial by monomial. This proves the lemma for global squares and for lifted variables.

   Lightly restricted blocks use fractional moments; heavily restricted blocks use true witness evaluation. Both penalties are at most `|R_b|/(2q_0)`. Certification therefore forces total exclusions at least `2q_0 G tau`. Independent block witness sampling permits multiplication of block coverage bounds and gives the stated exponent. A written lifted objective may couple blocks: its Boolean reduction still agrees with the true objective after all block substitutions. The example gives `tau=17/128` and exponent `17n/384` exactly.

   Strict concavity and coefficient exchanges establish the unique vertex optimizer; the additional mass-transfer proof establishes its separate linear-cost minimum. First-moment bounds follow from the node constraints. For multiple balances, preservation of the normal row space forces whole-block permutations; the successive differences of squared-index coefficient lists exclude translations between distinct blocks. Distinctness alone would not suffice, and the manuscript does not use that invalid shortcut. Padberg's cut is continuously valid by multiaffinity and has Boolean value `(s-k)(s-k-1)`. Summing equality products gives the trace bound and penalty `1/4`; adding the attained linear-cost minimum proves the perturbed and increasing-cost assertions. PSD is unnecessary for this deduction. One cut per relative block or addition of separate component certificates avoids the obstruction, as stated.

The independent checker `verification/reviewer05/stage04-round01/check_independent.py` passed with **exact integer and rational arithmetic**:

| Check | Cases |
| --- | ---: |
| Arbitrary product membership patterns, including domains missing all witness values, `2 <= n <= 4` | 44,224 |
| Exact tree sizes and rational chord LP leaf bounds | 89 trees |
| Midpoint leaves checked, `2 <= n <= 10` | 4,070 |
| Positive-tolerance leaves checked, `2 <= n <= 8` | 7,133 |
| Tolerance slabs including the `delta=1/2` boundary and beyond | 162 |
| Tolerance vertex objective values | 2,724 |
| Integer order thresholds and strict objective estimates | 6,824 |

For the endpoint bound the checker compares the square of the rational witness fraction with the corresponding rational integer power, so no floating approximation to half-exponents is used. The chord LP checker solves its linear resource-allocation problem by exact sorted marginal costs. The tolerance checker enumerates all objective-value types of cube-edge/slab-boundary vertices, with cube vertices included when feasible. The results are in `verification/reviewer05/stage04-round01/independent-results.json`.

**Remaining limits.** The finite checks supplement the universal proofs and establish no unrestricted positivity or optimality theorem. I inspected the frozen author's checker and reported artifacts but did not rerun its scripts or rebuild the manuscript; the independent tests above and the frozen source/PDF inspection are my own verification. Coniglio's primary Appendix C remains independently inaccessible in this review, and published/review-version identity remains unverified. No exhaustive priority search, sharpness claim for alternative moment functionals, or result for coupled auxiliary functions, coupled valid cuts, nonlinear elimination of original coordinates, or component-additive certificates is certified here. Those exclusions are stated in the manuscript and do not undermine its specified cover lower bounds.
