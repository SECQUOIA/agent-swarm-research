# Independent Stage 5c review — reviewer 3

Overall verdict: **accept the frozen Stage 5c section**. I found no major or minor issue requiring a repair. The proofs support the stated accuracy-bit complexity and original-parameter recovery guarantees. This verdict covers every new result, including the growing dense-degree approximation lemma and polynomial-law corollary, both coefficient-uncertainty models, and the several-parameter hybrid theorem.

I first read `completion-s5c-review-instructions.md`. I did not read author reports, lead notes, historical reviews, adjudications, or peer reports, did not coordinate with other reviewers, and did not use subagents. This report is my only repository edit. I made no commit.

The initial SHA256 of `complexity/sections/10-weighted-blocks.tex` was `fdb90d578a0a915b66fb443dcc530731d1f2647da6e437a3a0e1ebe093cebdb1`, matching the supplied freeze. The final verification returned the same hash.

## Explicit result verdicts

All locations below refer to `complexity/sections/10-weighted-blocks.tex` unless another file is named.

| Result | Verdict | Main reason |
|---|---|---|
| `lem:a-wblk-local`, Conditional block values | Accept | Exact block aggregation and independent coefficient boxes justify separation. Fixed-dimensional zonotope projection eliminates all coefficient variables and permits exact recovery. |
| `lem:a-wblk-univariate`, Uniform rational approximation on an interval | Accept | The annihilator, exceptional set, short bands, analytic disks, and rational interpolation have adequate polynomial degree and bit bounds. |
| `cor:a-wblk-scalar-sum`, Sums of scalar semialgebraic responses | Accept | Rational common panels avoid exact algebraic-sum comparison; additive errors and rational-argument recovery are correctly bounded. |
| `thm:a-wblk-line`, Weighted bounded blocks on an affine nomination line | Accept in all three coefficient models | The scalar corollary applies to the conditional block maxima, and the global coefficient-continuity estimate justifies independent rational rounding. |
| `cor:a-wblk-line-polynomial`, Fixed dense piecewise-polynomial laws | Accept | Fixed dimension permits growing dense degree. Strict monotonicity, continuity, and polynomial-bit derivative bounds provide the required local Lipschitz data. |
| `thm:a-wblk-hybrid`, Fixed total rank in the noncactus blocks | Accept in all three coefficient models | There are exactly `d + kappa + 1` retained optimization variables; the exceptional coefficient projection is exact and cactus surrogates compose with it. |
| `cor:a-wblk-hybrid-box`, Balanced boxes with fixed support and exceptional rank | Accept | The coefficient-independent face reduction preserves the needed rank bound, and interval/scenario selection plus rational disaggregation preserve the guarantee. |
| Several-parameter discussion and literature comparison | Accept | It distinguishes the proved interfaces from the unresolved algorithmic case without asserting hardness or impossibility. The cited statements support the comparisons. |

## Mathematical audit

### Block decomposition and exact conditional values

I checked lines 25–101 against the existence, block-incidence, block-decomposition, continuity, and computation results in `01-preliminaries.tex`; the box-LP proof in `03-block-rank.tex:395–524`; and the objective and continuity identities in `07-weighted-cactus.tex`.

Deleting a block's edges partitions the original vertices into components with exactly one block vertex each. Consequently each effective nomination is a sum of original nominations, independent of every circulation and coefficient elsewhere in the network. The reconstruction proof in `lem:a-pre-block` checks conservation at articulation vertices and shifts local potential gauges along the incidence tree. It therefore justifies combining independently optimized blocks, rather than merely establishing a necessary restriction property. The spanning-tree routing of `c` yields `W = sum_e w_e g_e(x_e)` with rational, polynomial-bit weights and does not introduce coefficient dependence into those weights.

The physical flow bound follows from orientation along strictly decreasing potential and source-to-sink path decomposition. This also holds inside an aggregated block because aggregation cannot increase total positive nomination. Chord flows are the fundamental circulation coordinates when the particular tree flow has zero chord entries. Thus the retained circulation box contains every physical state.

The box-LP lemma is applicable with `r_B` linking equations and one weighted-value row. Its proof does not enumerate all coefficient corners: it enumerates realizable signs of `eta^T W_e(z)` in fixed dimension, expresses the support inequalities, and eliminates only the fixed-dimensional support vector. This produces exact zonotope membership. The degree bound stays fixed independently of the number of edges and intervals. Subsequent circulation elimination and maximality quantification still involve a fixed number of variables. Compact fibers and uniqueness ensure that the maximality formula describes an attained, single-valued graph.

The recovery argument also covers a lower-dimensional or singleton zonotope. Every exposed vertex is obtained from a full-dimensional central-arrangement cell after discarding zero columns; at most `r_B + 2` image vertices suffice to represent any feasible image. Fixed-size determinant calculations and polynomially many field operations recover the original interval coordinates. No exponential corner search is hidden in this step.

For symmetric uncertainty there is one coordinate per edge throughout. For directional uncertainty the selected flow sign determines the active interval; the other coefficient is free to take an allowed value. At zero flow the active contribution is zero for either choice, so closed sign-cell overlaps do not relax the original law. Positive endpoints and compact boxes are inherited from the expressly referenced model.

The constants are consistent: difference flows satisfy `||x-x'||_infinity <= ||b-b'||_1/2`, while quadratic edge laws have Lipschitz constant `2 beta_U B_0`. Multiplying these and the affine-nomination and objective-weight bounds gives exactly the stated `K_B`; the direct edge-drop bound gives `M_B`. Maximizing over a common coefficient box preserves the fixed-profile Lipschitz bound. Neither argument requires a nonzero flow or derivative lower bound.

### Scalar approximation and summation

I checked the entire proof of `lem:a-wblk-univariate`, including the numerical constants, rather than treating the approximation statement as a black box.

For an explicit graph formula in two variables, at a generic graph point some value-dependent polynomial must vanish: otherwise continuity of all signs would give an open two-dimensional set of solutions. Content removal and squarefree reduction discard only finitely many exceptional parameter specializations. Continuity of the function extends the annihilating identity across those specializations. Products, subresultants, primitive parts, and exact quotients have polynomial total degree and coefficient size in the dense two-variable input. Irreducibility is unnecessary.

The leading coefficient times the resultant is nonzero over `Q[t]`. Its roots include degree drops and collisions of every algebraic branch. Real quantifier elimination of the real and imaginary equations computes the real parts of the complex roots in fixed dimension, including the roots that do not lie on the real axis. This is a finite set of at most `E` values, not a real-discriminant-only construction.

The padded bands have total length at most `4(E+1) rho <= eta/(16K)`. A midpoint value computed to `eta/8` therefore gives the advertised constant-piece error, even when several bands merge. Endpoint bands handle 0 and 1. Exceptional real parts outside `[-1,2]` cannot intrude into the disk-distance estimate; those retained but outside the parameter interval are also separated by the endpoint padding and the definition of the nearest gap boundary.

On each complementary gap the geometric panel rule gives `h <= d(tau)/64` and `R = d(tau)/4`. Each closed disk therefore avoids every exceptional root by at least `3 rho/4`. With a nonvanishing leading coefficient and simple roots, analytic continuation on a simply connected disk supplies the desired branch. Continuity of the selected real root forbids an undetected branch switch on the panel. Singular and switching parameters are already inside the short bands.

The bound on the leading coefficient is valid by its complex factorization. Since the disks have `|t| < 2`, coefficient sums give the stated rational `T`, and the Cauchy root bound gives `M`. Although `M` can be large, its logarithm and rational encoding length are polynomial: the exponent is the polynomially bounded degree of the leading coefficient, and `log(1/rho)` is polynomial in input and accuracy bits.

The contour formula yields the displayed interpolation remainder. The ratio `2h/(R-h)` is at most `2/15`, and the stated bound by `M 2^{-q}` is valid for `q >= 1`. For equally spaced nodes the product denominator of the j-th Lagrange basis is `(2h/q)^q j!(q-j)!`, yielding the given amplification bound. The chosen rational node precision controls that amplification and requires only `O(log(1/eta)+q log(q+1))` bits. Node spacings, including the final truncated panel, remain rationals of polynomial encoding length; expanding the interpolants therefore does not hide an exponential coefficient representation. This proves uniform error throughout each panel, not merely at sampled points.

For sums, the union of rational endpoints produces a polynomial number of common intervals. Each chosen local polynomial is valid on the entire selected closed interval, and alternative endpoint values cause no problem because both satisfy the same uniform error bound. Summing rational coefficients avoids composita of algebraic fields and remains stable under cancellation. The enclosure has width at most `eps/4`; the sample loss is at most `5 eps/16`; rational rounding loses at most `eps/4`. Negation handles minima, and the empty sum and constant cases are covered.

### Network recovery and dense polynomial laws

The affine-line theorem uses a rational affine normalization with polynomial encoding, and the singleton case can be handled by separately refined local value intervals. At the selected rational nomination, exact local coefficient optimizers are independent and globally compatible. Rounding each original uncertain coordinate inside its interval changes its coordinate by at most the isolation width. The coefficient-continuity bound uses the sum of these changes, so `||c||_1 B_0^2 k delta` is sufficient. Fixed coordinates remain rational; symmetric coordinates are rounded once; directional coordinates are separate. The output is an admissible original parameter scenario, not a rounded state asserted to satisfy the equations.

The fixed-law polynomial corollary uses only laws from `04-laws.tex:15–39`: rational breakpoints, dense polynomial pieces, continuity on the real line, vanishing at zero, and strict increase. Partitioning affine flow coordinates by every breakpoint needs polynomially many realizable cells in fixed dimension. Expanding a univariate degree-D polynomial of an affine form costs polynomial size for fixed dimension. Elimination has polynomial complexity in numerical degree, which dense encoding controls.

The coefficient-sum bounds on the pieces and their derivatives over `[-B_0,B_0]` have polynomial bit length even when degree grows. Continuity joins the piecewise derivative bounds into a whole-law Lipschitz constant. The acyclic difference-flow argument requires strict monotonicity, not a positive minimum derivative, so derivative zeros and nonsmooth breakpoints are covered. No coefficient rounding is needed in this corollary, and the exclusion of sparse binary exponents is appropriate.

### Hybrid theorem and face composition

In lines 408–510, the exceptional circulations number exactly `kappa`. All exceptional cycle equations and one total weighted-value row are projected together; hence the image dimension is `kappa + 1`, not the number of exceptional edges or objective-support vertices. The box projection is performed on degree-two data before substituting the growing-degree cactus approximants. The optimization variables are `z`, exceptional `q`, and one `v`.

The remaining cycle and bridge effective nominations depend only on `z`. I checked the earlier fixed-law charts, root selectors, threshold lemma, complete boundary/stationary/flat candidate construction, radical panels, and common sign-part construction in `07-weighted-cactus.tex:277–650`. Those arguments are local to a cycle and its nomination and objective weights; they do not require an ambient cactus. Comparisons are between surrogate candidates within a cycle, so a common sign decomposition avoids a Cartesian product of candidate choices. Both needed estimates hold: the surrogate is within `a` of the conditional maximum and within `a` of the recovered selected scenario.

Exceptional feasibility remains exact. Open sign parts are optimized through supremum threshold tests; a strictly lower sample threshold avoids assuming attainment there. For a selected feasible exceptional core, recovered coefficients need only represent its prescribed image. The zonotope recovery proof establishes exactly this stronger fact, although its lemma statement emphasizes optimization. At most `kappa + 2` image vertices suffice, and all exceptional arithmetic stays in the one sampled core field. Each ordinary cycle needs only its own extension of the common nomination field. Their fields need not be joined.

The physical objective upper bound and the `a = eps/16` approximation budget imply the stated enclosure and `5 eps/16` scenario loss. Rational LP in the isolating box intersected with `P` is valid for a lower-dimensional rational polytope and yields polynomial-bit rational parameters. The global joint-continuity estimate controls simultaneous nomination and coefficient rounding, even when it changes a flow sign, branch, or surrogate denominator condition. The remaining loss is at most `eps/4`.

For the balanced-box corollary I read the full face-reduction proof, including pruning, zero-objective block contraction, the two smoothing/perturbation stages, the coefficient-independent endpoint patterns, and greedy rational disaggregation. Surviving blocks do not acquire additional rank; deleting blocks cannot increase `kappa`. The number of free nomination coordinates on a face is fixed for fixed support and exceptional rank. Selecting the scenario with the largest certified lower endpoint loses at most one interval width in addition to its local scenario tolerance. The stated `eps/8` calls leave ample margin. The minimum follows by applying the argument to `-c`; support size and the structural reductions remain within the same bounds.

## Literature evidence actually inspected

- **Vigneron, October 21, 2011 author manuscript:** I read the local original PDF through a fresh `pdftotext -layout` extraction, specifically Section 2.1 (definition of nonnegative nice functions and constant description complexity), Section 2.3 (bit-model extension), Theorem 6, and Section 3.2 (approximate summation and avoiding exact radical-sum comparison), printed pp. 5–10. These support the multiplicative, polynomial-in-`1/eps` comparison. The current section does not claim approximate summation as a new principle.
- **Borcea–Bøgvad–Shapiro:** I inspected [arXiv:math/0409353v2](https://arxiv.org/pdf/math/0409353v2), Definitions 2–6 and Theorems 2–3, printed pp. 2–4. Their rational recurrence approximants converge to a dominant branch off the specified exceptional locus, with an exponential estimate away from that locus. The manuscript accurately distinguishes this from its uniform original-coordinate bit guarantee across exceptional parameters.
- **Yomdin:** I inspected [arXiv:1406.1719v2](https://arxiv.org/pdf/1406.1719v2), Definitions 5.1–5.2 and Theorem 5.6 with its proof, printed pp. 22–24. The complexity is a sum of degree powers for polynomial maps approximating a parametrization. The planar logarithmic-cubed estimate is accurately described as degree-based parametric approximation, not as a coefficient-bit algorithm in a prescribed coordinate.
- **Binyamini–Novikov:** I inspected [arXiv:1802.07577v2](https://arxiv.org/pdf/1802.07577v2), Section 1.1.1 and Theorem 1, Section 1.5 on polynomial-bound notation, and Section 2.2.3 on algebraic degree/complexity. The polynomial chart-count and complexity statements support the comparison. They do not themselves assert the rational coefficient-bit shared-coordinate summation interface used here.
- **Petras:** I inspected the [publisher abstract](https://www.sciencedirect.com/science/article/pii/S0377042701005866), obtained through the search tool after direct opens failed. It expressly concerns verified enclosure of a function or integral under representation assumptions. This supports the modest attribution; I did not inspect or rely on a detailed Petras rate theorem.
- **Real algebraic primitives:** I inspected the local original Basu survey PDF, Section 2.2.2/Definition 2.13, Theorem 2.16, Section 2.5.2/Theorem 2.27 and its coefficient-bit bound, and Section 2.6's dense-encoding convention, using a fresh PDF text extraction. I also inspected the locally stored text of Renegar Part III, Proposition 2.3 (restating Part I, Proposition 4.1), printed p. 332. These support fixed-dimensional sign enumeration and elimination with polynomial dependence on dense numerical degree and coefficient length. I did not independently reread the full BPR book; its algorithmic principles are also explained in the manuscript and the inspected survey.

The final discussion states an unresolved case of the present algorithms, not a universal limitation on approximation theory. It acknowledges that another optimization method might avoid the proposed surrogate representation. I found no unsupported novelty, impossibility, or hardness assertion.

## Diagnostics and their limits

I inspected `completion-s5c-build.json`, `completion-s5c-checks.json`, the full new diagnostic script, `complexity/main.tex`, and the new bibliography entries. The new section is included before the conclusion. The build record reports return code 0, a PDF, no unresolved references or citations, no duplicate labels, and no overfull boxes. I independently checked all **17** build-manifest source hashes against current files; all matched. I did not rerun the LaTeX build.

I reran `/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-potential-flow/verification/check_s5c_scalar_approximation.py`; it exited 0 and reported `passed: true`. Its SHA256 matched the record: `ae633732ca9ea4f47986eb2d46ab0c35590f0bc8fdbfad5767a8d2d11ca4985e`. The record also contains a successful `python -O` run; I inspected that record rather than rerunning it. The script uses explicit `require` checks, so its checks are not removed by Python optimization.

The four fixtures cover an implicit quintic, a real branch switch, nearby nonreal branch points, and a nearby exterior pole. They checked all 3,826 constructed panel geometries, interpolated 35 selected panels, and made 595 certified sample comparisons plus 33 band checks. The script verifies the quintic resultant and a repeated-factor/content-removal identity. Its exact rational calculations reproduce the manuscript's panel and interpolation constants.

These are finite diagnostics. The exceptional parameters and function-value oracles are supplied for the fixtures, interpolation is performed only on selected panels, and sample comparisons alone do not prove uniform error. There is no general graph-to-annihilator or quantifier-elimination implementation, no growing-degree performance experiment, and no full network optimizer test. Those limitations are correctly disclosed in the code and records. Acceptance rests on the proofs and inspected computation bounds, with diagnostics providing supplementary arithmetic checks.

## Findings and remaining uncertainty

**Major findings: none. Minor findings: none. Required repairs: none.** I have no separate optional suggestion necessary for this stage. I cannot establish exhaustive novelty across all approximation literature, and the diagnostic code is not an implementation of the general polynomial-time algorithms; neither limitation contradicts the section's claims.

Final source hash: `fdb90d578a0a915b66fb443dcc530731d1f2647da6e437a3a0e1ebe093cebdb1`.
