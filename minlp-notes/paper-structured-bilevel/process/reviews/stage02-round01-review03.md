# Stage 2, round 1 — independent review 03

Reviewed snapshot: `process/snapshots/stage02-round01`.
SHA256 of `SHA256.json`: `b4c7f91913054ca4da83eac32ccaae2ac52412e605c468a63278172846d1f849`.
I independently verified the manifest digest and all seven listed file hashes.

**Recommendation: PASS. No major or minor correction requests.**

I read the entire frozen manuscript source, both sections, the fixed-core appendix, bibliography, README, and coverage inventory. I did not consult other stage 2 reports, delegate, change manuscript sources, or rely on historical PASS records. The later planned sections and final abstract are outside this gate and are not omissions in the current stage.

## Exact-response proof audit

### Local branches and global regimes

`sections/02-exact-responses.tex`, `lem:local-branches` and `lem:candidate-size`:

The local elimination is sound. For each fixed leader and compressed coordinate vector, the block objective is strictly convex; its gradient is the original follower gradient with shared multiplier contributions. Polyhedral first-order necessity supplies multipliers even on lower-dimensional feasible faces or with dependent rows. The quotient-space support reduction preserves nonnegative inequality multipliers, while equality multipliers absorb the projected dependence. Independent surviving normals make the enumerated KKT matrix nonsingular by positive definiteness.

Every validity predicate checks all original rows, including omitted equality rows, and the signs of the selected inequality multipliers. This prevents a candidate based on an incomplete equality basis from becoming a spurious feasible response. Squared determinants and the corresponding adjusted Cramer numerators give genuinely positive denominators on the declared regions.

The global regime selection does not take an exponential Cartesian product: every block's valid branches are fixed by a common realizable sign condition in fixed dimension. Agreement of valid branches follows from uniqueness of the effective local minimizer. Disconnected sign realizations require no additional component analysis because branch validity and ordering depend only on signs.

I checked the degree accounting: effective linear coefficients have degree `O(delta)` in compressed coordinates, fixed-size determinants have degree `O(d delta)`, and products over blocks grow only to `O((B+1)d delta)`. Expanding in fixed ambient dimension preserves polynomial monomial counts; the stated coefficient-product estimate controls bit lengths. Arbitrary explicitly encoded upper monomials remain manageable after substitution, with the stated `O((B+1)d delta^2)` bound.

### Global versus stationary responses and quantified selection

`eq:global-response-formula` at line 239, `eq:optimistic-compressed-relation` at line 257, and `eq:joint-optimum-formula` at line 269:

The global comparison has the correct quantifier order: it compares candidate values at the same leader. Every global minimum belongs to the comparison set, and every compared candidate is follower-feasible. Consequently, a candidate passing the universal comparison is global, and all global ties survive. The proof never treats KKT conditions alone as sufficient for a nonconvex follower.

The upper predicate uses the same regime decoding as the candidate formula. Its rows occur after the follower's globality test, so they cannot alter the follower problem. Quantifier elimination of the response predicate before further composition, or use of only a fixed number of renamed copies, keeps the number of real variables fixed. Growing regime counts and upper-row counts affect formula length rather than quantified dimension.

The empty-follower case is correctly excluded by the existential candidate part of the response formula. The universal comparison does not create a response through vacuous truth. Common-field sampling includes the leader, multipliers, aggregate, follower value, and upper value simultaneously; rational response evaluation then recovers all original coordinates without composing unrelated fields.

### Attainment and rank changes

`lem:closed-response` at line 284, `lem:moving-compression` at line 323, and `ex:moving-nonattainment` at line 360:

The fixed-normal compactness proof works without a promise that every leader admits a follower. Along a convergent sequence of response pairs, each nearby fiber is nonempty because it contains the corresponding response. Hoffman repair therefore approximates every limiting feasible competitor in those nearby fibers. Continuity yields limiting globality. Upper weak polynomial rows then preserve compactness of the optimistic feasible graph.

The moving-normal proof correctly enumerates every possible equality subset and uses determinant guards, including at rank changes. Soundness only needs sufficient local KKT conditions, so a selected equality subset need not span all original equality rows if the candidate passes those rows. Completeness selects a full equality basis pointwise and reduces the inequality support modulo that basis.

The example `xz=0` with follower objective `(z-1)^2` is valid both as a shared moving row and as a local rank-change example. At positive `x` the response is zero; at zero the response is one. The optimistic value `x+z` therefore has infimum zero without an optimizer. The empty local equality basis is necessary at zero, where the nonempty equality-active determinant vanishes.

### Pessimistic feasibility, worst values, and unattained infima

`thm:exact-semantics` at line 375, `eq:worst-value-formula` at line 413, and `eq:infimum-predicate` at line 429:

The domain includes existence of a true follower response and excludes any leader with a global response violating any upper row. The worst-value relation ranges over all global responses rather than a subset surviving the upper rows. Its fixed-leader maximum exists by compactness. The proof does not infer leader attainment from that fact.

The two parts of the infimum predicate express a lower bound and approximation from above for every positive tolerance. Applied after nonemptiness has been decided, they characterize the unique finite infimum. Endpoint membership decides attainment. The final joint sample requires both a worst value and a response attaining it, so the returned pessimistic witness has the promised meaning.

I independently checked the quartic counterexample at line 455. Its stationary points at `x=0` are `0,1/2,1`, with costs `0,1/16,0`. The global comparison rejects the middle point and retains both endpoint ties. The upper row `z<=1/2` is optimistically satisfiable at zero but pessimistically violated there. Without that row, the worst objective is `x` for `x>0` and one at zero, so the pessimistic infimum is not attained.

## New arithmetic refinement

`cor:constant-hessian-degree` at line 475:

I find the claimed constant algebraic-degree bound justified. With constant local Hessians and fixed normals, each KKT inverse is rational and independent of the compressed coordinates. Local responses are polynomial functions of those coordinates with degree controlled by the input degree. Summing over blocks enlarges coefficients and descriptions, but not degree. Upper substitution retains a degree bound depending only on the fixed structural dimensions and fixed input degree.

I checked the precise external ingredient against the primary source: `[[basu1996-on-the-combinatorial-and-algebraic]] p.3-4`, Theorem 1.3.1, bounds the output polynomial degrees in terms of input degree and quantified block dimensions independently of the number of input polynomials. The sampling construction at `p.27-28`, Section 3.1.3, likewise bounds each univariate representation's degree independently of that count. I visually checked the original PDF pages 4 and 27, not just the extracted formulas. These support the refinement after a fixed number of elimination/sampling steps. Polynomial evaluation of all decoded responses stays in the resulting field.

The corollary appropriately retains fixed normals and constant Hessians. The more general model's growing product-denominator degree is not silently covered by the constant bound. Bit length and total coordinate output are still allowed to grow polynomially.

## Fixed-core appendix and constructive recovery

`appendices/a-fixed-core.tex`, `thm:fixed-core`, `lem:core-support-membership`, and `lem:core-recovery`:

The local vertex argument covers lower-dimensional bounded polyhedra, singletons, duplicated rows, and empty blocks. At a vertex, the active normals must span the full ambient block space even if the feasible polyhedron has lower dimension; otherwise a two-sided feasible perturbation contradicts extremality. The determinant validity conditions therefore provide enough candidates.

The support predicate has the correct sign and quantification. Appending the objective as a measurement makes exact objective attainment equivalent to membership of the target in the Minkowski sum. Empty blocks make the predicate false for every support direction, including the zero direction. In the nonempty case, separation by a nearest point proves the converse support implication. The full original feasible set is closed and uniformly bounded even though its local normals move, so this single-level problem has an attained minimum when feasible.

The new recovery argument is complete. At the sampled core, every actual direction realizes some globally enumerated sign condition whose selected vertices jointly attain the Minkowski support. Those tuples all survive the denominator and feasibility filter. Extra feasible tuples from sign conditions that are not realized at that core can only add points already inside the same image. Hence the retained aggregates have exactly the image's support function and convex hull.

Carathéodory reduction gives an affinely independent support of at most `h+1=k+2` aggregate points. Enumerating those subsets is polynomial for fixed `h`. On an independent subset the weights are uniquely determined by a fixed-size linear system; if a real solution exists, its rational operations on coefficients and target in `K` put the weights in `K`. The subsequent zero and nonnegativity tests verify all equations and signs. Applying those same weights in every block preserves all local constraints and the complete aggregate target, including the objective coordinate. No growing-dimensional algebraic LP and no combination of nonconvex follower optima is used.

The extension from fixed degree to polynomial dependence on numerical degree is supported by the proof: local determinant and pair-comparison degrees grow polynomially in `delta`; global support products have degree `O((B+1)d delta)`; all expanded formulas remain in fixed dimension. Sampling and the fixed-size reconstruction have the required polynomial bit bounds.

## LP specialization, integration, and coverage

The supplied diagonal-plus-fixed-rank corollary at line 516 correctly relies on positive definiteness of the complete Hessian, without requiring the small coupling matrix to be positive semidefinite. The clipping formulas are affine on arrangement cells, agree on boundaries, and extend to cell closures. Intersecting each closure with aggregate consistency and upper rows gives a rational LP consisting only of true follower responses. Compact bounds on leader and aggregate variables ensure attained cell optima. The decomposition is explicitly supplied, and rational output is justified.

The coverage inventory assigns every current theorem and appendix component to explicit labels, including the two new developments. The scalar theorem is covered through the block proof and its explanatory scalar clipping formula. The prior stage's algorithm-scope and degree-output qualifications are preserved. The elementary curvature barriers now have an explicit later-stage assignment. No current obligation is replaced by an unsupported repository assertion, and the manuscript clearly separates the appendix's polyhedral convex combinations from nonconvex follower response semantics.

The exposition introduces geometry before multipliers and explains why each quantified construction is needed. The two counterexamples give concrete meanings to stationarity, ties, moving ranks, and universal feasibility. I found no prose or notation defect requiring correction for this stage.

## Verification artifacts and limits

All verification artifacts are under `verification/reviewer03/stage02-round01/`:

- `snapshot-check.json`: digest and seven file-hash checks.
- `check_stage02.py` and `checks.json`: independent exact diagnostics for changing rank, empty local fibers, lower-dimensional singletons with duplicate rows, KKT determinant failure, stationary/global separation, and universal upper-row semantics. The recovery diagnostic constructs six support tuples over `Q(sqrt(2))`, verifies that all eight Cartesian corner images belong to their convex hull, and recovers an algebraic target using three common-field weights and the same weights in all three blocks. It checks exact aggregate equality and local feasibility.
- `build/`, `build.log`, and `build-check.json`: fresh isolated latexmk build of the complete frozen source. It produces 17 pages. The final TeX log has no warnings, undefined citations/references, or overfull/underfull boxes. First-pass citation warnings in the combined transcript were resolved by subsequent passes.
- `bpr-page-4.png` and `bpr-page-27.png`: images of the primary PDF pages used to verify the degree formulas.

I compared the manuscript arguments with the actual canonical scalar/block, infimum/moving-normal, fixed-core, and supplied-low-rank source developments, while judging the proofs themselves. I did not rerun the author's diagnostic or use its success as independent evidence. I did not implement a general real quantifier-elimination algorithm, prove the cited algebraic tools from scratch, repeat a comprehensive publication-priority audit, inspect all 17 rendered pages visually, or test later computational stages. The finite checks supplement the proof audit and do not constitute an empirical test of the asymptotic algorithms.
