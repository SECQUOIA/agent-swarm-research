# Stage 5c independent review — R2

Overall verdict: the seven new results are mathematically sound, subject to the minor precision-choice correction below. I found no major issue in the frozen section or its material dependencies. In particular, the scalar approximation proof supplies the required uniform rational output and polynomial bit bounds; the hybrid proof retains a fixed number of variables and recovers original coefficients without combining the independent block fields.

I read the review instructions first, reviewed independently, did not read author, lead, historical, or other reviewer reports, and did not communicate with other reviewers or use subagents. I changed only this report. References to manuscript lines below are to `paper-potential-flow/complexity/sections/10-weighted-blocks.tex` unless another file is named.

Initial source SHA256: `fdb90d578a0a915b66fb443dcc530731d1f2647da6e437a3a0e1ebe093cebdb1`.

Final source SHA256: `fdb90d578a0a915b66fb443dcc530731d1f2647da6e437a3a0e1ebe093cebdb1`.

## Result-by-result verdicts

| Result | Verdict | Reasons |
| --- | --- | --- |
| Conditional block values, `lem:a-wblk-local`, lines 25–101 | Accept | The block aggregation, fixed-dimensional box projection, maximum-graph formula, bounds, and separate local recovery are valid. No exponential coefficient-corner enumeration is hidden. |
| Uniform rational approximation, `lem:a-wblk-univariate`, lines 111–280 | Accept with minor wording correction M1 | The annihilator, finite complex exceptional set, short bands, analytic disks, contour estimate, rational interpolation, and dense bit bounds work together. M1 makes the stated choice of the band width well-defined. |
| Sums of scalar semialgebraic responses, `cor:a-wblk-scalar-sum`, lines 282–311 | Accept | Common rational interval refinement and univariate optimization avoid exact sum comparison. The enclosure and rational-argument error budgets are sufficient. |
| Weighted bounded blocks on an affine nomination line, `thm:a-wblk-line`, lines 315–355 | Accept | Conditional maxima separate over blocks; the scalar corollary supplies the shared rational parameter; independent coefficient recovery and original-box rounding complete the scenario guarantee. All three coefficient models are covered. |
| Fixed dense piecewise-polynomial laws, `cor:a-wblk-line-polynomial`, lines 362–395 | Accept | Breakpoint cells have fixed dimension, degrees and dense encodings remain polynomial, and derivative/value bounds give the needed Lipschitz and absolute bounds. Strict monotonicity, rather than a positive derivative lower bound, suffices for flow sensitivity. |
| Fixed total noncactus rank, `thm:a-wblk-hybrid`, lines 410–510 | Accept | There are exactly `d + kappa + 1` retained optimization coordinates. One exceptional value row and the established cactus common partition preserve this bound; arbitrary feasible exceptional-core recovery is justified by the box lemma's proof. |
| Balanced boxes with fixed support and exceptional rank, `cor:a-wblk-hybrid-box`, lines 512–533 | Accept | The earlier resistance-independent face theorem applies with fixed maximum block rank, reductions cannot increase exceptional rank, and face selection plus rational disaggregation preserves the guarantee. |

The closing several-parameter discussion, lines 535–600, is also acceptable. It identifies an interface the present algorithms do not provide and does not assert an impossibility theorem, a new hardness classification, or the necessity of exact SRS comparison.

## Findings

### M1 — Minor: specify a power of two when choosing the band width

Location: lines 173–178, the instruction to choose a positive dyadic `rho` with the largest possible value satisfying the displayed inequality.

Under the usual meaning of a dyadic rational, this largest value need not exist. For example, take the graph `f(t)=t`, `K=M_0=1`, and `eta=1/3`. The construction can use `F=y-t`, so `H_*=1` and `E=0`. The upper bound on `rho` is then `1/192`, which is not a dyadic rational. Dyadic rationals are dense below this bound, so there is no largest admissible one.

Concrete repair: replace “a positive dyadic” by “a power of two `rho=2^{-s}`, with the smallest integer `s>=0` satisfying the inequality,” or equivalently choose the largest admissible member of `{1, 1/2, 1/4, ...}`. This is precisely what the diagnostic's `dyadic_below` routine does. It gives `A/2 < rho <= A` for the positive upper bound `A`, establishing the polynomial encoding and logarithmic panel-count claims. No other proof or constant needs to change.

This is a minor formulation issue, not a counterexample to the approximation lemma. The intended construction is clear and its repair is local.

No major findings. No further minor findings.

## Mathematical checks

### Local graphs and coefficient elimination

I checked the block-incidence and aggregation proofs in `01-preliminaries.tex`, including reconstruction at cut vertices and shifts of local potentials. They justify both coefficient independence conditional on the original nominations and the assembly of independently selected local states. A spanning-tree flow `Aw=c` gives the weighted edge-drop identity for arbitrary balanced rational `c`; no bound on objective support is used in the local or affine-family algorithms.

The parametric box lemma in `03-block-rank.tex` has the interface used here. For fixed core and image dimensions its support-function formula uses sign tests in the core and support-vector coordinates, rather than one quantified coefficient coordinate per edge. Enumerating realizable signs is polynomial in fixed dimension. The universal support inequalities characterize the entire zonotope, including lower-dimensional images, zero columns, and singleton intervals. The subsequent coefficient recovery enumerates polynomially many exposed image vertices and fixed-size affine combinations. It does not enumerate all original box corners. The same recovery works at any attainable prescribed image, which is exactly the stronger use required in the hybrid proof.

The local formula includes the compact nomination domain and a circulation box containing every physical state. Projection followed by exclusion of a larger attainable value therefore describes the maximum graph exactly. Compactness and state continuity supply attained, nonempty fibers. At a rational parameter, sampling a maximizing local core and lifting its zonotope image supplies algebraic coefficients of polynomial representation size.

For the stated constants, the local nomination change obeys `||Delta b^B||_1 <= T_B ||Delta z||_infinity`. The acyclic difference-flow argument gives the factor `1/2`, and the quadratic edge-law Lipschitz constant is `2 beta_U B_0`. Their product is the displayed `K_B`. Maximizing over a common coefficient box preserves this Lipschitz bound by evaluating the same optimizing profile at the other nomination. Absolute bounds follow directly from the flow bound and the weighted edge-drop formula.

The directional model selects the active coefficient on each closed sign cell. At zero flow, both branch contributions vanish, so the two closed-cell formulas agree even when the directional intervals differ. An unused directional coefficient can be chosen independently. The symmetric model retains its single original edge coefficient and rounds it once. These distinctions remain correct in both the line and hybrid theorems.

### Annihilator, complex exceptional parameters, and coverage

For interior parameters outside finitely many roots of the parameter-only tests and contents, some value-dependent graph polynomial must vanish: otherwise all tests are locally constant and the formula includes an open neighborhood in the plane. Removing content and repeated factors preserves the needed roots at generic parameters. Continuity then extends `F(t,f(t))=0` to the omitted parameters and both endpoints. This includes a reducible graph and continuous switches between algebraic branches. There is no unsupported irreducibility assumption.

Dense products in two variables have polynomial degree and coefficient length. Subresultants over `Q[t]` yield the required primitive squarefree part with polynomial degrees and heights. The nonzero polynomial `a_D Res_y(F,F_y)` contains every leading-coefficient zero and every finite root collision. Its complex roots have at most `E` distinct real parts. Real elimination of `Re H_*(u+iv)=Im H_*(u+iv)=0` is in two variables of polynomial numerical degree. Exact real projection, sorting, and isolation therefore give the finite set of real parts in polynomial bit time. Here “eliminate” must mean the exact real projection already specified by the section's algebraic-computation conventions; a bare resultant with no real feasibility filtering would not be an equivalent replacement.

Padding each retained real-part enclosure by `rho` ensures that every complex exceptional root is at least `d(t)` from a real point in a complementary gap, using its real part alone. Roots whose real parts are outside `[-1,2]` are farther than one from the relevant real interval and do not invalidate the estimate. Merging overlapping padded intervals preserves it. Their total real length is at most `4(E+1)rho`; the constant approximation on each component has error less than `eta/4`. Endpoint bands cover both endpoints. A constant `H_*` yields an empty root list and still leaves the endpoint-band construction valid.

On a panel, `h <= d(tau)/64` and `R=d(tau)/4`, hence `h <= R/16`. Every point of the closed disk remains at distance at least `3d(tau)/4` from the exceptional roots. The polynomial has fixed positive degree in its value variable and simple roots on a slightly larger disk. Local implicit branches, boundedness of roots over compact subsets, and the simply connected disk give a single holomorphic branch. The continuous real graph follows that branch throughout the panel because distinct roots cannot be exchanged continuously without a collision. Branch switches inside the discarded bands need no analytic treatment.

The lower bound on the leading coefficient is valid by its factorization: every factor has distance at least `3rho/4`, so `|a_D(t)| >= |lambda|(3rho/4)^{k_0}`. Also `|t|<2` on the disks. The coefficient sum bound and the Cauchy polynomial-root bound therefore give the displayed rational `M`. The numerical size of `M` can be large, but its logarithm and rational encoding are polynomial: raising a polynomial-bit rational to a polynomial degree still has polynomial encoding. The argument does not assume a lower bound on the imaginary distance of a singularity to the real axis.

### Interpolation, dense output, and summation

I independently checked the contour estimate and both error allocations. For `q+1` nodes the numerator product contributes at most `(2h)^{q+1}`, each contour denominator factor contributes at least `R-h`, and the additional Cauchy denominator contributes the factor `R/(R-h)`. Thus the displayed error is at most `(16M/15)(2/15)^{q+1} <= M 2^{-q}` for `q>=1`.

For equally spaced nodes, `|L_j(x)| <= q^q/[j!(q-j)!]` on the real panel. Summing gives at most `(2q)^q/q! <= (2q)^q`. Node rounding to `eta/[8(2q)^q]` therefore adds at most `eta/8`. Together with interpolation error this is at most `eta/4`. Computing each node value independently avoids a common algebraic field. Rational node spacings may be very small, but their encodings remain polynomial; products, exact divisions, and dense expansion of the degree-`q` Lagrange polynomials retain polynomial bit length.

The scalar-sum corollary refines only rational endpoints, so it produces polynomially many common intervals. At shared endpoints either valid local polynomial satisfies the same error guarantee. Optimizing each rational sum polynomial requires only endpoints and derivative roots, including constant polynomials. The combined enclosure width is at most `eps/4`, the algebraic sample loss is at most `5eps/16`, and rational argument rounding adds at most `eps/4`. The rounding can leave a chosen surrogate panel because the loss is controlled by the true sum's global Lipschitz constant. This also explains why cancellation between large signed summands is harmless for additive accuracy. The empty sum and constant functions are covered explicitly; `K_i>=1` prevents a zero denominator in the nonempty-sum rounding expression.

### Network output and the polynomial-law extension

The line theorem's nondegenerate interval is mapped rationally to `[0,1]`, with polynomial encoding. A singleton rational interval has a rational parameter already and reduces to separate local optimization and value refinement; the subsequent coefficient-rounding argument still applies. At the recovered rational parameter the independently optimized block coefficients assemble into a global scenario by the block-decomposition proof. Rounding inside each original rational coefficient interval preserves feasibility, and the all-graph continuity estimate bounds the total loss. Inactive directional coordinates, fixed coefficients, and singleton intervals do not require a nonzero-flow or interior-point assumption.

For fixed dense polynomial laws, all breakpoint hyperplanes are affine in a fixed number of flow coordinates. Enumerating their realizable cells gives polynomially many polynomial systems. Substitution of affine flows into a dense univariate polynomial of growing degree has polynomial dense size in fixed dimension. Fixed-dimensional elimination remains polynomial in numerical degree, so it is applicable here. The explicit value and derivative coefficient sums have polynomial bit length, and continuity joins the derivative-based Lipschitz bounds across breakpoints. Strict monotonicity gives the same acyclic difference-flow proof even where a derivative is zero. The corollary correctly restricts this extension to fixed laws and does not silently extend it to growing-degree uncertain coefficient families or sparse binary exponents.

### Hybrid algorithm, recovery, and face composition

All exceptional circulation coordinates together number `kappa`; the one value coordinate represents their total weighted contribution. Applying the box lemma before introducing growing-degree surrogates respects its fixed-degree hypotheses. The cactus and bridge through-nominations are functions of `z` alone by aggregation. The earlier candidate construction uses only local affine nominations and weights, so the presence of an exceptional block elsewhere does not change it.

I checked the fixed-law chart, square-root panel, threshold-with-ties, and complete-candidate proofs in `07-weighted-cactus.tex`. Their common sign partition includes eligibility, denominators, and same-cycle surrogate comparisons, so a selected feasible local scenario and the local maximum both stay within their allocated error of the summed surrogate. The fixed-variable optimization of `v+S(z)` is consequently valid. Open sign parts require supremum tests and a sample at a strictly smaller threshold, as the proof states. Compactness of the exact core and bounded physical values provide the finite search bound even when surrogate denominators approach zero.

The exceptional coefficients are recovered in the common ordered field of the sampled core; their image dimension is `kappa+1`, so at most `kappa+2` exposed image vertices suffice. Each other cycle is recovered in its own extension of the nomination field. There is no requirement to compare or join all cycle fields. The coefficient-continuity proof is valid at zero flow because the smoothed directional laws are jointly continuously differentiable there and the electrical terminal adjoint currents have magnitude at most one.

Rational linear feasibility in `P` intersected with rational coordinate enclosures returns a feasible rational nomination even if `P` has lower dimension or is a singleton. The coefficient rounding stays within the original independent intervals. The global bound `K_b H_1 h + ||c||_1 B_0^2 k delta` controls the final loss even if the rounded physical state changes signs, branches, or circulation. Zero multipliers can simply be omitted from the precision requirement. A graph with no exceptional blocks uses `v=0`; a one-vertex graph has no block contributions and zero balanced weighted objective.

Finally, I checked the earlier small-face proof: pruning, zero-objective block contraction, the ordered ordinary chains, the two-stage smoothing/perturbation, and rational disaggregation. Surviving blocks do not acquire identified distinct vertices under these contractions, so their ranks are unchanged; removed blocks cannot increase `kappa`. Fixed support and fixed exceptional rank therefore yield finitely many fixed-dimensional nomination problems in polynomial count. Selecting the largest certified face lower endpoint loses at most a local interval width, in addition to that face's scenario tolerance, well within the stated budget.

## Primary-source and integration evidence

- **Vigneron:** inspected the local original `literature/vigneron-2011-algebraic-sums-manuscript.pdf` through a fresh text extraction: Section 2.1 (printed p. 5), Section 2.3 (p. 7), Theorem 6 and its proof (pp. 8–9), and Section 3.2 (pp. 9–10). The manuscript defines nonnegative nice functions with constant description complexity, gives a multiplicative scheme, and explicitly states a bit-model extension polynomial in `1/eps`. Its approximate summation and common-arrangement mechanisms support the attribution and the stated distinction.
- **Borcea–Bøgvad–Shapiro:** inspected Definitions 2–6 and Theorems 2–3, printed pp. 2–3 of [arXiv:math/0409353v2](https://arxiv.org/pdf/math/0409353v2). The approximation concerns the dominant branch outside the equimodular, pole, and slow-growth loci; Theorem 3 gives exponential convergence away from them. This supports the manuscript's comparison, without supplying its uniform bit-algorithm interface across exceptional parameters.
- **Yomdin:** inspected Definitions 5.1–5.2 and Theorem 5.6 with its proof, printed pp. 22–24 of [arXiv:1406.1719v2](https://arxiv.org/pdf/1406.1719v2). The complexity counts degrees of polynomial maps approximating a parametrization. The logarithmic-cubed planar bound is accurately cited, and it is correctly distinguished from approximation in a prescribed common argument.
- **Binyamini–Novikov:** inspected the preceding algebraic lemma and Theorem 1, printed p. 2; Section 1.5, pp. 12–13; and Section 2.2.3, p. 15 of [arXiv:1802.07577v2](https://arxiv.org/pdf/1802.07577v2). The smooth chart bounds and degree-based complexity notions are geometric. The manuscript correctly avoids treating them as a supplied rational-coefficient Turing algorithm for adding many independently parameterized graphs.
- **Petras:** inspected the publisher's indexed abstract for [Self-validating integration and approximation of piecewise analytic functions](https://www.sciencedirect.com/science/article/pii/S0377042701005866), JCAM 145(2), 345–359. Direct page-opening attempts failed, but the publisher result returned the complete abstract. It explicitly concerns validated enclosures under representation assumptions. The modest attribution in the manuscript is supported; I did not inspect a full Petras proof or use any detailed rate from it.
- **Algebraic computation:** inspected the original local Basu survey PDF, `literature/papers/basu2014-algorithms-in-real-algebraic-geometry/original.pdf`, especially Definition 2.13, Theorem 2.16, and Theorem 2.27/Section 2.5.2, printed pp. 10–12 and 16. The theorem's operation, degree, formula-size, and integer-bit bounds match the fixed-dimensional uses in the preliminaries. I did not rely on the corrupted extraction of the local 2006 book as source evidence.

I also inspected `main.tex`, the new bibliography entries and the existing Vigneron entry, and the concluding integration. The new section is included once after the prior mathematical sections. The bibliography gives the original-manuscript locator for Vigneron and the v2 locator for Borcea–Bøgvad–Shapiro. The section expressly acknowledges classical root isolation, complex branch continuation, and interpolation, and I found no material novelty overstatement in its comparisons. This source check is not a claim of an exhaustive literature priority search.

## Diagnostic and build evidence

I read `completion-s5c-build.json` and `completion-s5c-checks.json`. The build manifest reports a successful forced `latexmk` build, no undefined references/citations, no duplicate labels, and no overfull boxes. I independently recomputed every source hash listed in that build manifest; all match the current files. I did not rerun the build, because this review permits writing only the assigned report.

I read the entire new diagnostic script and independently reran it with optimization enabled:

```text
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python -O paper-potential-flow/verification/check_s5c_scalar_approximation.py
```

It exited successfully. Its four fixtures constructed and checked respectively 988, 896, 904, and 1038 panel geometries; interpolated 10, 10, 10, and 5 selected panels; and performed 170, 170, 170, and 85 certified sample comparisons. They cover an implicit quintic, a real branch switch, nearby nonreal branch points, and an external pole. The independently recomputed script hash is `ae633732ca9ea4f47986eb2d46ab0c35590f0bc8fdbfad5767a8d2d11ca4985e`, matching the checks manifest. The explicit `require` checks remain active under `-O`.

These are exact finite diagnostics, with `Fraction` arithmetic and symbolic resultant identities. They do not implement general graph-formula elimination, general complex-root projection, a general network optimizer, or a proof of uniform error by sampling. They interpolate only selected panels; the contour proof supplies uniform analytic-panel validity. The reported large rational coefficients are compatible with polynomial asymptotic encoding bounds. My acceptance of the theorems rests on the proofs and inspected algebraic-computation bounds, with the fixtures serving as supplementary checks.

The final manuscript hash matches the initial frozen hash stated above. No manuscript, bibliography, diagnostic, managed literature, or Paper B file was edited, and no commit was made.
