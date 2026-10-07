# Development inventory: smoothed exact global optimization beyond convexity

Date: 2026-10-05. Author: principal Opus writing agent. This record lists
the developments available for the manuscript, their exact models and
bounds, how they depend on one another, and what must be repaired or
cited. It is a working evidence file, not submission text.

All source paths are relative to the repository root. Unless stated
otherwise, `ND/` means `research-20261002/new-direction/`, `PA/` means
`research-20261002/prior-art/`, and `RV/` means `research-20261002/reviews/`.
Sibling manuscripts are `EA` = `paper-exact-arithmetic/`, `DA` =
`paper-decomposition-aware/`, and `SI` = `paper-sparse-indicator-quadratics/`.

## 0. What was read

Read in full: `research-20261002/README.md`, `SYNTHESIS.md`, `CLOSEOUT.md`,
`PROGRESS.md` (items 1-74); `EA/sections/10-recourse.tex` and the
finite-law lemmas and projected-growth tail of
`EA/appendices/I-recourse.tex`; `DA/sections/abstract.tex`, `DA/README.md`,
the introduction of `DA/sections/recourse.tex`, `DA` Theorem
`thm:cr-filter` and Proposition `prop:star`; the `SI` abstract and README.

`ND/` notes read in full (the theorem-bearing sources): proximal-growth-tail,
expected-smoothed-qp, smoothed-semiconcave-cells, smoothed-exact-cell-closure,
smoothed-ambient-cell-closure, smoothed-gaussian-cell-closure,
smoothed-miqp-cell-closure, smoothed-gaussian-miqp,
smoothed-mixed-separable-closure, anisotropic-gaussian-separable-closure,
smoothed-integer-low-rank, spectral-normalization, negative-inertia-qp,
negative-inertia-miqp, integer-label-isolation, sparse-bag-cell-smoothed-qp,
sparse-bag-cell-smoothed-miqp, smoothed-sparse-polynomial,
polynomial-finite-noise-tails, polynomial-exact-fallback,
convex-patch-evaluation, global-error-cell-barrier,
local-error-recourse-interface, sparse-smoothed-hardness-sanity,
smoothed-polynomial-graph-constraints, constrained-smoothing-barrier,
simplex-block-smoothed-extension, smoothed-implicit-graph-constraints,
smoothed-sparse-order-polynomial, order-polytope-cell-count,
smoothed-mixed-order-polynomial, smoothed-box-stable-recourse,
smoothed-polynomial-box-recourse, smoothed-native-integer-recourse,
native-integer-recourse-implicit-closure, smoothed-interior-core-flow,
core-only-flow-boundary-obstruction, smoothed-boundary-core-flow,
flow-optimal-face-certificate, smoothed-bilinear-core-flow,
smoothed-core-tu-recourse, core-only-noise-boundary-recourse,
core-noise-active-stratum-tube, small-residual-multiplier-curvature,
strong-field-component-qp, smoothed-sparse-polynomial-significance.

Read in part: order-polytope-face-closure (§1-4), core-only-noise-rotating-fiber
(§1-4), boundary-core-flow-significance (§1-4),
polynomial-component-primitive-limit (§1-7), strong-field-component-polynomial
(§1-2), ambient-local-count-barrier (§1, §5-8),
smoothed-polynomial-actuator-dynamics (§1), polynomial-recourse-rank-separation
(§1-2), polynomial-exact-fallback-construction (§1), screening-percolation
(statement), and the opening sections of core-only-noise-strong-recourse,
affine-convex-fiber-certificate, core-only-noise-exploration,
core-value-certified-recourse, continuous-core-noise-value-oracle,
implicit-graph-oracle-interface, implicit-convex-patch-certificate,
smoothed-linear-growth, summed-response-growth, tu-feasible-rounding,
tu-polyhedral-cell-count, polyhedral-chamber-count,
polynomial-growth-section-audit, polynomial-component-genericity-audit,
negative-curvature-sparse, unknown-growth-oracle-barrier,
nonconvex-certificate-barrier, modewise-growth-barrier. Not read:
convex-modulator-qp, the all-scale value and point-oracle notes (covered by
`EA`), deterministic grid notes (covered by `DA`). Review verdicts in `RV/`
were scanned for every theorem above; prior-art notes were read for their
claims and cited sources only. Partially read items must be read in full
by whoever writes their section.

The antecedent folders `research-20260922/` and `research-20260927/` were
checked through their READMEs; neither contains a smoothed development used
here (Section 8). No literature search, browsing, experiment, build, or
project-wide check was performed.

## 1. Disposition codes

| Code | Meaning |
| --- | --- |
| MAIN | Statement and full proof in the main text. |
| APP | Statement in the main text; full proof in an appendix. |
| LEM | Supporting lemma, stated once and reused across routes. |
| COR | Corollary or remark with a short complete proof. |
| LIM | Limitation or obstruction, stated and proved. |
| CITE | Belongs to a sibling manuscript; cited, not re-proved. |
| EXT | External published result used as a black box; citation must be confirmed by the Luna lead. |
| EXCL | Excluded: superseded, out of topic, or a non-theorem exploration. |
| OPEN | Incomplete development; may appear only as an open problem. |

"Reviewed" in the status column means the source records at least one
independent actual-file proof review that passed. Internal review is not
peer review, and every proof still needs the critical re-examination
required by the brief.

## 2. Inventory table

### 2.1 Framework and shared foundations (F)

| ID | Development | Source path(s) | Status | Disposition | Uses |
| --- | --- | --- | --- | --- | --- |
| F1 | Corrected-corner interpolation: mean-preserving endpoint rounding inside a cell and coordinate upper curvature `L` give `E F(Y) <= F(x) + (L/8) sum_i h_i^2`; sequential version for polynomials needs `partial_ii F <= L` on the continuous hull; correlated versions for simplex cells and common-threshold order rounding need a block or full Hessian bound | `ND/smoothed-semiconcave-cells.md` §3; `ND/smoothed-sparse-polynomial.md` §2; `ND/simplex-block-smoothed-extension.md` §2; `ND/smoothed-sparse-order-polynomial.md` §2; `ND/tu-feasible-rounding.md` | reviewed | LEM | - |
| F2 | Local-comparison counting lemma: each interior coordinate of a near-optimal grid node confines its independent linear coefficient to a fixed interval of length `<= L h + 2 delta / h`; product bound over coordinates; nested anisotropic power-of-two meshes give a level-independent expected count; finite-grid version adds `1/M` per interval and needs `M >= 2^J` | `ND/smoothed-semiconcave-cells.md` §1-2, §4 | reviewed | LEM | F1 |
| F3 | Continuous growth tail: for any continuous `f` on compact `X`, independent coefficients with densities `<= phi_i`, `Pr{g_* < eps} <= 2 eps sum_i phi_i w_i`; constant 2 sharp; proximal-map and area-formula proof; uniform-noise expanding-map proof | `ND/proximal-growth-tail.md` §1-7 | reviewed | APP | - |
| F4 | Finite-grid QP growth tail: scalar section of `{g_* < eps}` has at most `8(F+1)^2` components, `F` = number of (mixed) faces; transfer to the `M`-point grid with error `2nC/M`, uniform in the threshold | `ND/proximal-growth-tail.md` §8 | reviewed | APP | F3, F5 |
| F5 | Section-count transfer: if every axis section of an event has at most `C` interval components, uniform-grid and continuous-uniform probabilities differ by at most `2nC/M`; for laws within Kolmogorov distance `delta`, by `2nC delta` | `ND/proximal-growth-tail.md` §8; `ND/smoothed-ambient-cell-closure.md` §5; `ND/smoothed-gaussian-cell-closure.md` §6; same lemma in `EA/appendices/I-recourse.tex` (`lem:recourse-replacement`) | reviewed | LEM | - |
| F6 | Two-block quantifier-elimination section bound: an event defined by an existential and a universal block of `n` variables, one free noise scalar, fixed degree and `s` atoms (integer labels as finite disjunctions) has `2^{poly(I)}` section components, independent of coefficient heights and thresholds (Renegar 1992, Thm 1.1) | `ND/polynomial-finite-noise-tails.md` §2-3; audit `ND/polynomial-growth-section-audit.md`; same mechanism in `EA` `lem:recourse-sections` | reviewed | LEM | EXT Renegar |
| F7 | Active-margin tail: on the positive-growth event the optimizer is a nonsingular stationary root of its minimal face; isolated-root Bezout bound `D^k` roots per face; each active gradient (multiplier, exposure gap) has slope one in one free noise coordinate; union bound `K(tau/sigma + 1/M)` | `ND/polynomial-finite-noise-tails.md` §4; variants in `ND/sparse-bag-cell-smoothed-qp.md` §6, `ND/simplex-block-smoothed-extension.md` §5, `ND/order-polytope-face-closure.md` §2, `ND/smoothed-implicit-graph-constraints.md` §5 | reviewed | LEM | F3 |
| F8 | Integer-label isolation: for integer labels in `prod {L_i..U_i}` and any label costs, `Pr{two lowest label values within eps} <= sum_i (U_i-L_i)(eps/sigma + 1/N)`; Kolmogorov variant `G(eps/sigma + 2 delta)` | `ND/integer-label-isolation.md`; `ND/smoothed-gaussian-miqp.md` §3 | reviewed | LEM | - |
| F9 | Exact QP fallback by active-face enumeration: some global optimizer lies on a face whose tangent Hessian is positive definite or which is a vertex; `2^m` row subsets (polytopes) or `3^n prod N_j` faces (mixed boxes); exact rational output, ties and continua included | `ND/expected-smoothed-qp.md` §3; `ND/sparse-bag-cell-smoothed-miqp.md` §5 | reviewed | LEM | - |
| F10 | Lexicographic two-block fallback: the lexicographically first global optimizer of `F_gamma` on a compact domain has two-block singleton formulas for each coordinate and the value; Renegar plus univariate isolation gives work `B (I+b+q+1)^{c_d}`, `B = 2^{poly_d(I)}` base-only; feasible rational approximants with certified gap | `ND/polynomial-exact-fallback.md`; alternative proof `ND/polynomial-exact-fallback-construction.md`; same lemma in `EA` `lem:recourse-fallback` | reviewed | APP | EXT Renegar |
| F11 | Convex-patch evaluation: for a rational box (or relative polytope) with verified Hessian `>= tau I`, GLS weak optimization on the capped epigraph, homothety repair and rational clipping/projection give a feasible rational point within `2^{-q}` and a value interval of width `2^{-q}` in `poly(S+q)`, including boundary minimizers | `ND/convex-patch-evaluation.md`; relative-polytope and order versions in `ND/simplex-block-smoothed-extension.md` §6, `ND/smoothed-sparse-order-polynomial.md` §7 | reviewed | APP | EXT GLS |
| F12 | Localization on the good event: if every retained cell has a witness within `2E_j` of `f*` and point growth is `>= g_0`, every retained cell lies within coordinate distance `A h_j`, `A = 2 + nL/g_0`, of the unique optimizer | stated separately in each closure proof (e.g. `ND/sparse-bag-cell-smoothed-qp.md` §5) | reviewed | LEM | F1 |
| F13 | Algebraic tube with grid jitter: for a nonzero polynomial of degree `<= D` in `q` variables, `Pr_grid{dist(gamma, Z) <= delta} <= C(q,D)(delta/sigma + sqrt(q)/M)`, `C(q,D) = 16 q^{q+1} D (4D+2)^{q-1}` (Basu-Lerario 2023, Thm 1.1); atoms included | `ND/core-noise-active-stratum-tube.md` §5 | reviewed | LEM | EXT Basu-Lerario |
| F14 | Finite Gaussian-like law and weighted lattice count: bounded-time rational rejection sampler with Kolmogorov error `<= 2^{-b}` and support `[-(b+20)sigma,(b+20)sigma]`; Gaussian density majorant for dependent factor noise with frame `c I <= TT^T <= I`; capped lattice sum `<= CW phi_s(0) + 2C + 4` independent of the auxiliary box | `ND/smoothed-gaussian-cell-closure.md` §2-4 | reviewed | APP | - |
| F15 | Constant-base exact small-box polynomial solver: exact global optimizer and value of a fixed-degree rational polynomial on a rational `k`-box in `c_d^k poly_d(H)`; common-root output; ties and continua handled (pure-power deformation, moment-curve forms, characteristic-polynomial derivatives) | `ND/polynomial-component-primitive-limit.md`; review `RV/polynomial-component-primitive-limit-review.md` | reviewed; Sol re-audit passed; attribution open | APP (root decision 1: included with full constructive proof; no novelty claim for RUR/critical-point methods) | - |
| F16 | Budget order: choose the fallback budget `B` from base data, then `rho = 1/(4B)`, thresholds `g_0, tau` (and tube radius), then the cutoff `J`, then `M >= max{2^J, C_tail/rho, K/rho, ...}`; no precision circularity; expected work = search count + `(1/B) B poly` | pattern in every theorem note | reviewed | LEM (meta-theorem) | F2-F10 |
| F17 | Exact oracles used as black boxes: rational convex QP (Kozlov-Tarasov-Khachiyan 1980); FPT convex MIQP in integer dimension (Del Pia, arXiv 2311.00099, Thm 3); separable convex integer optimization over bounded TU systems (Hochbaum-Shanthikumar 1990, Thm 4.3/Alg. 4.2); exact rational forest box-QP (Del Pia-Khajavirad, treewidth paper); rational LP; GLS weak optimization | cited in `ND/negative-inertia-miqp.md`, `ND/smoothed-native-integer-recourse.md` §6, `ND/smoothed-box-stable-recourse.md` §6, `ND/convex-patch-evaluation.md` | source-checked in notes | EXT | - |
| F18 | Original-objective consequences: an exact sampled optimum has original regret `<= sigma W` (ambient noise) or `<= k sigma` (core-only noise on a unit core box); a sampled certificate plus `max_X gamma^T x` gives an original-objective interval of width `delta + sigma W` | `ND/smoothed-sparse-polynomial.md` §7; `ND/boundary-core-flow-significance.md` §3 | reviewed | COR (not for Route D; see §6 item 23) | - |

### 2.2 Route A: few negative directions and low-rank concavity (A)

Search space: auxiliary Fenchel coordinates `a in R^k`. Value function
`W(a) = min_x [F(x) + (alpha/2)||a - Tx||^2]`, which is `alpha`-semiconcave
and, under `ker(H + alpha T^T T) subseteq ker T`, continuously
differentiable with `grad W(a) = alpha(a - T x(a))`.

| ID | Development | Source path(s) | Status | Disposition | Uses |
| --- | --- | --- | --- | --- | --- |
| A0 | Fenchel lift, rational negative-space normalization (`nu <= beta < 2 nu`, `||U|| <= 1`, `H + 2 beta U U^T >= 0`, exact range projector; frame `TT^T >= 63/64 I`), growth transfer `g_W = g alpha/(2g + alpha||T||^2)`, and the deterministic conditioned theorem: exact QP/MIQP in `f(k, max(1,nu/g)) poly(I)` (resp. `f(n_Z, k, max(1,nu/g)) poly(I)`) with explicit retained-cell count `2^k (sqrt(k kappa) + 4)^k`, `kappa = alpha/g_W < 2 + 4nu/g` | `ND/spectral-normalization.md`; `ND/negative-inertia-qp.md`; `ND/negative-inertia-miqp.md`; frame bound in `ND/smoothed-ambient-cell-closure.md` §6; slab alternative `ND/convex-modulator-qp.md` (not needed) | reviewed | APP (foundation and contrast) | F17 |
| A1 | Growth-moment route for `k <= 2`: bounded polytope with `m` rows, ambient uniform grid with `M >= 2n D B`, `D = 8(2^m+1)^2`, `B = max(2, 2^m)`; interleave the conditioned solver with active-face enumeration; capped moment gives expected `(I+1)^K (1 + nu W/sigma)`; the argument fails for `k > 2` (term `r B^{1-1/p}`) | `ND/expected-smoothed-qp.md` | reviewed | APP (proposition) | A0, F4, F9 |
| A2 | Exact cell closure under aligned factor noise `T^T xi`, `xi in G_M(sigma)^k`; the source's `ker(H + alpha T^T T) subseteq ker T` hypothesis is unnecessary for supplied factors (attaining-witness inequality; root decision 4, Sol low-rank audit §3): critical-region extraction from an optimal-set vertex and nonnegative multipliers; base-only piece-Hessian bound `bar H = alpha(1 + n k (2n)! C_0^{2n})`; an unresolved retained cell forces `xi` within `sqrt(k)(alpha + bar H) h_j` of one of `K = 2^m(m+n+1)` fixed hyperplanes; expected `C^k (1 + Theta_al)(I+1)^C`, `Theta_al = prod_i [3 + (1+2k) alpha w_i/(2 sigma)]`, `w_i = range_P(Tx)_i + 2 sigma/alpha`; FPT in `(k, 1 + nu diam(P)/sigma)`; exact rational output every draw | `ND/smoothed-exact-cell-closure.md` | reviewed | MAIN | A0, F2, F9, F16 |
| A3 | Independent ambient uniform noise: complementary-minor volume lemma `Pr{d_i in I_i(eta), i in Q} <= prod sqrt(n) L_i/(2 sigma)` for dependent factor coordinates; scalar-section bound `C_sec = [2(2k+1)R+1](8k+2)`, `R = 2^m`; ambient hyperplane lifting `||L|| >= 1`; expected `C^k (1 + Theta_amb)(I+1)^C`, `Theta_amb <= [2 + (1+2k)(2n + 2 nu sqrt(n) diam(P)/sigma)]^k`; polynomial at fixed `k`, not FPT | `ND/smoothed-ambient-cell-closure.md` | reviewed | MAIN (part of Theorem A) | A2, F5 |
| A4 | Independent Gaussian-like ambient noise: `d` and residual noise independent under the Gaussian proxy; weighted count `Theta_G = prod_i [2 + c^{-1/2}(2C_k+4) + C_k alpha (u_i - l_i)/(sigma sqrt(2 pi))]`, `C_k = 1+2k`; base-only support/precision loop; expected `f(k, nu diam(P)/sigma) poly(I)` with absolute exponent | `ND/smoothed-gaussian-cell-closure.md` | reviewed | MAIN (part of Theorem A) | A2, A3, F14 |
| A5 | Mixed-integer QP on a bounded mixed polytope, uniform ambient noise: best-other-label gap by `2 n_Z` exclusion convex-MIQP solves; whole-cell test `C subseteq R_J` and `Delta(v) >= alpha k C_T h_j`; isolation bounds gap failures; section bound `[2(2k+1)R^2+1](8k+2)`, `R = N_Z 2^m` (`N_Z` integer label assignments in the LP range box); expected `f(n_Z) C^k (1 + Theta_amb) poly(I)` | `ND/smoothed-miqp-cell-closure.md` | reviewed | MAIN (part of Theorem A-MIQP) | A3, F8, F17 (Del Pia MIQP) |
| A6 | Mixed-integer QP, Gaussian-like noise: scalar isolation transfer without a factor `n`; support loop `J(t) <= J(0) + 2t`; expected `f(n_Z, k, 1 + nu diam(P)/sigma) poly(I)`, absolute exponent | `ND/smoothed-gaussian-miqp.md` | reviewed | MAIN (part of Theorem A-MIQP) | A4, A5 |
| A7 | Separable mixed recourse: `F = sum_i phi_i(x_i) - (alpha/2)||Tx||^2` on a mixed product box, `phi_i` convex piecewise quadratic with rational coefficients **and rational breakpoints**; scalar recourse by neighbor differences and derivative thresholds; global polyhedral regions; every active witness gives the upper model; aligned law: `C^k(1+Theta_al)(I+1)^C` (FPT); ambient uniform law: `C^k(1+Theta_amb) poly(I)`; integer dimension unrestricted | `ND/smoothed-mixed-separable-closure.md` | reviewed | MAIN (Theorem A-sep) | A2, A3 |
| A8 | Anisotropic Gaussian separable closure: exact rational row rotation and dyadic diagonal scaling (`UU^T >= I/16`, `L_max < 8 beta`), curvature-balanced meshes; expected `f(k, 1 + beta diam(X)/sigma) poly(I)`, `beta = alpha ||T||^2` (supplied concave curvature, not intrinsic); full row rank required; no conditioning parameter | `ND/anisotropic-gaussian-separable-closure.md` | reviewed | MAIN (part of Theorem A-sep) | A4, A7, A0 (Jacobi) |
| A9 | Integer low-rank lattice exactness: integer box, `g_j` convex quartic (degree `<= 4`) on each interval, minus `(alpha/2)||Tx||^2` (any rank `r`); per-row aligned noise `sigma_i`; `M >= max(2, r alpha s^2 D_0)`, `D_0 = 2 Q^3`; objective lattice `1/(D_0(M-1))` makes the terminal gap exact; **no fallback**; expected `8^r Theta_rat P(I)`; deterministic baselines for binary or listed labels | `ND/smoothed-integer-low-rank.md` | two reviews | MAIN (short theorem) | F2 |
| A10 | Approximate expected-cell search for a prescribed accuracy (law tuned to the accuracy) | `ND/smoothed-semiconcave-cells.md` §3-5 | reviewed | EXCL (superseded by A2; keep F2) | F2 |

### 2.3 Route B: sparse interactions on tree decompositions (B)

Search space: bag coordinates. Value function: the conditional value
`V_B(v) = min over outside coordinates on the original outside domain`,
which is independent of all bag noise and coordinatewise `L`-semiconcave.

| ID | Development | Source path(s) | Status | Disposition | Uses |
| --- | --- | --- | --- | --- | --- |
| B1 | Sparse bag-cell search: binarized decomposition; nested clipped grids; bag-cell whitelists; separator-key min-marginal DP over deduplicated corner rows; rounding preserves whitelists; global correction `E_j = n L h_j^2/8`; every optimizer retained; one globally consistent witness per retained cell; conditional count `Theta_B = prod_{i in B} [4 + (1 + n/2) L w_i/(2 sigma)]`; integer coordinates refine to unit spacing, then singletons | `ND/sparse-bag-cell-smoothed-qp.md` §2-4; `ND/sparse-bag-cell-smoothed-miqp.md` §2-3 | two reviews each | MAIN | F1, F2 |
| B2 | QP/MIQP closure: intersected coordinate hulls; exact affine gradient signs force original bounds (continuous only); integers fixed only from singleton hulls; PSD test on the remaining principal block, then exact convex QP on the original face; tail cutoff with `B = 3^{n_C} prod (w_i+1)`; expected `C_0^p [4 + (1+n/2) L w_max/(2 sigma)]^p (I+1)^C`; exact rational output | `ND/sparse-bag-cell-smoothed-qp.md` §5-7; `ND/sparse-bag-cell-smoothed-miqp.md` §4-6 | reviewed | MAIN (quadratic case of Theorem B) | B1, F4, F7, F9, F12 |
| B3 | Fixed-degree polynomial factors on a mixed box: sequential semiconcave rounding; midpoint gradient enclosure `M_2 r`; patch test `H_CC(c) - (M_3 r + g_0) I > 0`; `H_CC(a) >= 2 g_0 I` after active elimination; finite tail via F6, active margins via F7, fallback F10; expected `C_0^p [4 + (1+n/2) L w_max/(2 sigma)]^p poly_d(I)`; output = compact strongly convex patch (polynomial size) with `poly_d(I+q)` evaluation, or exact algebraic fallback; global pruning record has only an expected-size bound | `ND/smoothed-sparse-polynomial.md`; tails `ND/polynomial-finite-noise-tails.md`; fallback `ND/polynomial-exact-fallback.md`; evaluation `ND/convex-patch-evaluation.md`; significance `ND/smoothed-sparse-polynomial-significance.md` | reviewed (composition, adversarial, tail, fallback) | MAIN (Theorem B) | B1, F6, F7, F10, F11, F12 |
| B4 | Explicit polynomial graph constraints `z_j = P_j(t, z_<j)` (degree `e`, `<= k` parents, depth `D`): substitution keeps a decomposition of bag size `p' <= max(1,k^D) p`; condition on dependent-coordinate noise; pullback curvature `L'` uniform in that noise; expected `C_0^{p'}[4 + (1 + m/2) L' w_max/(2 sigma)]^{p'} poly(I)` | `ND/smoothed-polynomial-graph-constraints.md` | reviewed | COR (of Theorem B) | B3 |
| B5 | Implicit monotone graph constraints `q_j(t_{S_j}, y_j) = 0` with global brackets and derivative floors: certified approximate DP (`D_j = N delta_j <= E_j`, witnesses within `4E_j`); bordered-KKT nonsingular roots for the margin tail; expected `C_0^{p'}[4 + (1+n) L w_max/(2 sigma)]^{p'} poly(I)`, `p' <= p max(1,k)`; output = retained patch plus root equations; exact rational ambient feasibility not promised | `ND/smoothed-implicit-graph-constraints.md`; `ND/implicit-graph-oracle-interface.md` | four reviews | APP (Theorem B-domains, part) | B3, F6, F7, F10, F11 |
| B6 | Disjoint resource and probability simplex blocks plus native-integer intervals: clipped-cube cells are convex hulls of feasible corners; block Hessian bound `H_BB <= L I`; face-stratified count with anchor conditioning; derivative and derivative-difference face tests (no absolute-gradient tests on equality simplices); relative-polytope evaluator; expected `C_0^p [4 + (2 + n/2) L max(1, w_max)/(2 sigma)]^p poly_d(I)`; whole-block bags | `ND/simplex-block-smoothed-extension.md`; review `ND/simplex-block-noise-review.md`, `RV/simplex-block-closure-review.md` | two reviews | APP (Theorem B-domains, part) | B3, F11 |
| B7 | Continuous order polytopes `x_i <= x_j` (cycles allowed): common-threshold rounding with full Hessian bound `Lambda`; at most `b!` bag order chambers with affine copy maps of squared norm `<= n`; directional count `b!(b+1)[2 + (b n Lambda + 2 eta)/(2 sigma)]^b`; LP exposure-gap face certificate (sound without margins); paired-noise exposure tail; source bound `C_0^p p! (p+1) [2 + n Lambda (p+1)/(2 sigma)]^p poly_d(I)`, **superseded** by the B8 transport count specialized to `n_c = n`, `p_c = p`: `C_0^p p!(p+1)[2 + 3 n Lambda/(4 sigma)]^p poly_d(I)` (root decision 3); use the weighted Hessian test of `ND/order-polytope-face-closure.md` §3 | `ND/smoothed-sparse-order-polynomial.md`; `ND/order-polytope-cell-count.md`; `ND/order-polytope-face-closure.md`; review `ND/order-polytope-independent-review.md` | reviewed | APP (Theorem B-domains, part) | B3, F6, F7 |
| B8 | Binary order variables: endpoint-preserving transport gives feasible upper supports where projections are nonconvex; directional constant `n_c Lambda` (`n_c` continuous coordinates; source `N`); binary labels fixed before LP exposure (reverse order unsound); expected `C_0^p p_c!(p_c+1)[2 + 3 n_c Lambda/(4 sigma)]^{p_c} poly_d(I)`, `p_c` = continuous coordinates per bag (source: `q`) | `ND/smoothed-mixed-order-polynomial.md`; `RV/smoothed-mixed-order-review.md` | reviewed | APP (Theorem B-domains, part) | B7 |
| B9 | Affine-state polynomial-actuator dynamics: backward elimination keeps degree and factor scopes; corollary of B3 with conditioning on state noise | `ND/smoothed-polynomial-actuator-dynamics.md` | reviewed | COR (example) | B3 |
| B10 | Conditional-recourse count: if bag corner values `W_B(v)` are supplied with certified error `<= a e_B`, `e_B = |B| L h^2/8`, the expected tuple count becomes `prod [4 + (L w_i/(2 sigma))(1 + (1+a)p/2)]` (bag size instead of dimension); efficient recourse is not supplied | `ND/local-error-recourse-interface.md` §2-3; deterministic filter is `DA` Thm `thm:cr-filter` | reviewed | COR (bridge to Route C) | F2; CITE DA |

### 2.4 Route C: a small core with tractable conditional recourse (C)

Search space: core `v in [0,1]^k`. Value function
`V(v) = min_{z} F_gamma(v, z)` over a residual domain independent of `v`;
it is `L`-semiconcave in the core, and with residual noise conditioned it
receives an independent core tilt.

| ID | Development | Source path(s) | Status | Disposition | Uses |
| --- | --- | --- | --- | --- | --- |
| C1 | Core search with exact box-stable QP recourse (continuous unit box, ambient noise): exact recourse at dyadic core corners, correction `e_j = k L h_j^2/8`, count `[3 + (1+k/2) L/(2 sigma)]^k`; excluded-region certificate with `<= 2r` restricted recourse calls (`r` residual coordinates) and core Lipschitz bound `G` (`V_out(c) - V(c) > 2G diam D`); gradient-sign and constant-Hessian closure; expected `8^k [3 + (1+k/2) L/(2 sigma)]^k poly(I)`; exact rational output | `ND/smoothed-box-stable-recourse.md` | reviewed | MAIN (Theorem C1, part a) | F2, F4, F7, F9 |
| C2 | Feedback-vertex-set corollary: deleting the core leaves a forest; Del Pia-Khajavirad forest oracle supplies box-stable recourse; expected FPT in FVS size and `L/sigma` | `ND/smoothed-box-stable-recourse.md` §6 | reviewed | COR | C1, F17 |
| C3 | Certified approximate polynomial recourse (ambient noise): any box-stable oracle with certified lower value and feasible rational completion; residual convexity `H_RR >= 0` supplies it (GLS; tangent certificate (6a)); excluded slabs use certified lower values; nonlinear Hessian patch test; expected `8^k [3 + (1+k) L/(2 sigma)]^k poly_d(I)`; implicit patch output | `ND/smoothed-polynomial-box-recourse.md`; `RV/smoothed-polynomial-box-recourse-review.md` | reviewed | MAIN (Theorem C1, part b) | C1, F6, F7, F10, F11 |
| C4 | Rank separation: degree-five family with one core coordinate and dense convex quartic recourse; every fixed PSD quadratic convexifier has rank `>=` residual dimension; core curvature independent of coupling scale | `ND/polynomial-recourse-rank-separation.md` | checked | COR (example) | - |
| C5 | Native integer recourse: `X = [0,1]^k x Y`, `Y = {z in Z^r : Dz <= e, l <= z <= u}`, exact oracle stable under coordinate-bound tightening; competing-label certificate with `<= 2r` exclusion calls (`V_other(c) - V(c) > 2 G w`); whole-core exact algebraic completion; ambient noise; growth-only tail; label-enumeration fallback; expected `[8^k (3 + (1+k/2) L/(2 sigma))^k + c_d^k] poly_d(I)` with F15; integer label plus small-core shared-root algebraic output of size `c_d^k poly_d(I)` every draw; rational for quadratics | `ND/smoothed-native-integer-recourse.md`; `RV/smoothed-native-integer-recourse-review.md`; `RV/constant-base-core-transfer-review.md` | reviewed | MAIN (Theorem C2) | C1, F3/F6, F10, F15 |
| C6 | Implicit-output variant of C5: active-gradient and Hessian patch tests instead of algebraic completion; `8^k [...]^k poly_d(I)` with compact patch output | `ND/native-integer-recourse-implicit-closure.md` | reviewed | COR | C5, F7, F11 |
| C7 | TU and network oracles: Hochbaum-Shanthikumar exact separable convex integer optimization over bounded TU systems with endpoint tangent extensions; marginal-potential optimality certificate for flows | `ND/smoothed-native-integer-recourse.md` §6; `PA/integer-convex-flow-recourse-prior.md` | source-checked | EXT + COR | F17 |
| C8 | Core-only noise with uniformly strongly convex residual (`H_RR >= mu I`, verified): Lipschitz selector, projected-to-full growth lift `g_F = min{g_V/(1 + 2H^2), mu/4}`; three-block relative-boundary formula for residual active-pattern changes and algebraic tube (F13); small-multiplier release (`||grad lambda||^2 <= 2 K_3 lambda` on a two-sided ball; restored modulus `nu`); expected `8^k [3 + (1+k) L/(2 sigma)]^k poly_d(I)` with **only core noise**; implicit patch | `ND/core-only-noise-boundary-recourse.md`; `ND/core-noise-active-stratum-tube.md`; `ND/small-residual-multiplier-curvature.md`; antecedent lemmas in `ND/core-only-noise-strong-recourse.md`; reviews `ND/core-only-noise-boundary-recourse-independent-review.md`, `ND/core-noise-boundary-lemmas-independent-review.md` | reviewed | MAIN (Theorem C3) | C3, F13, F7, F11 |
| C9 | Interior uniform-flow certificate under core-only noise: shortest-path-tree polynomial potentials, exact non-strict reduced-cost sign tests on the hull, cross-label gradient images of chart zero sets, tube bound; premise: all optimal cores interior for every noise in the cube; `[8^k (...)^k + c_d^k] poly_d(I)` | `ND/smoothed-interior-core-flow.md`; `RV/smoothed-interior-core-flow-review.md` | reviewed | COR (variant of Theorem C4; network flows only) | C5, C7, F13 |
| C10 | Deterministic optimal-face certificate for flows: optimal-flow intervals `I_a` describe all tied flows; inward-derivative minimization over all tied flows is convex flow (two-point interpolation where needed); cycle proximity `||z - bar z||_1 <= r v_I(z)`; fixing test `mu >= r K T_1`, `beta - H R - (H/2) T_inf > 0` | `ND/flow-optimal-face-certificate.md`; `RV/flow-optimal-face-adversary.md` | reviewed | LEM (Route C) | C7 |
| C11 | Boundary core flows (core-only noise, any core face): facewise chart images, tube bound, normal-noise margins over all optimal flows, value margin `mu_0` via two-block elimination (`log(1/mu_0) <= f_d(k) poly_d(I)`); expected `f_d(k)[3 + (1+k/2) L/(2 sigma)]^k poly_d(I)` and sampling length `log M <= f_d(k) poly_d(I)` | `ND/smoothed-boundary-core-flow.md`; reviews `RV/smoothed-boundary-core-flow-adversary.md`, `RV/boundary-core-flow-bit-adversary.md`, `RV/flow-boundary-margin-review.md` | reviewed | APP (Theorem C4, part a) | C10, F13, F6, F10 |
| C12 | Bilinear coupling `phi(v) + sum psi_a(z_a) + v^T B z`: affine charts, elementary margin `|p(x)| >= b_min dist(x, Z)`; expected `[8^k (...)^k + c_d^k] poly_d(I)`, `log M = poly_d(I)`; `L` from `phi` only | `ND/smoothed-bilinear-core-flow.md`; `RV/smoothed-bilinear-core-flow-review.md` | reviewed | MAIN (Theorem C4, part b) | C11 |
| C13 | TU replacement: compact adjacent-slope dual from piecewise-linear interpolation and cellwise TU integrality; pointed dual with vertex bound `mV`; conformal unit-circuit proximity; inequality systems by explicitly bounded zero-cost slacks; both C11 and C12 bounds transfer | `ND/smoothed-core-tu-recourse.md`; `RV/smoothed-core-tu-recourse-review.md` | reviewed | MAIN (Theorem C4 stated for TU; networks as instance) | C10-C12 |

### 2.5 Strong noise without width (D)

| ID | Development | Source path(s) | Status | Disposition | Uses |
| --- | --- | --- | --- | --- | --- |
| D1 | Strong-field mixed box QP: coordinates whose noise lies outside the derivative range are pinned by strict monotonicity; bad sites are independent; components of the bad subgraph are solved by face/label enumeration; if `4 Delta beta < 1`, expected `poly(I + log M)[1 + sum_i a_i q_i/(1 - 4 Delta beta)]`, `a_i = 3` (continuous) or label count; sufficient `sigma >= 8 Delta max a_i R_i` | `ND/strong-field-component-qp.md`; `RV/strong-field-component-qp-review.md`; `PA/strong-field-component-qp-prior.md` | reviewed | APP (Theorem D) | F9 |
| D2 | Strong-field fixed-degree polynomials: same persistence, components solved by F15 with `a_i = c_d`; structured output (one algebraic representation per component; symbolic value sum); explicit conservative `c_d = 2^{10000 D}` | `ND/strong-field-component-polynomial.md`; two reviews | reviewed | APP (root decision 1: included) | D1, F15 |
| D3 | Random screening for indicator QPs (positive-definite `Q`, penalized indicators): screening lemma plus site percolation | `ND/screening-percolation.md` | checked; "modest" | EXCL (indicator/convex line; see `SI`) | - |

### 2.6 Limitations and obstructions (X)

| ID | Development | Source path(s) | Status | Disposition |
| --- | --- | --- | --- | --- |
| X1 | Global-error retention barrier: connected degree-four instances of treewidth `p-1`, `L = 2`, unit widths, `sigma = 1/100`; every bag cell survives until mesh `~ sqrt(p/n)`, giving `>= (5n/(6p))^{p/2}` retained cells on **every** draw; whole-hull closure cannot pass earlier; instances easy by endpoint DP | `ND/global-error-cell-barrier.md`; `RV/global-error-cell-barrier-review.md` | reviewed | LIM |
| X2 | Bag-local corrections are unsound with grid min-marginals (star, `m = 32`); positive-definite star with `d^2` leaves has error variation `(d-1)h^2` | `ND/local-error-recourse-interface.md` §1, §5 | reviewed | CITE (`DA` Prop. `prop:star` proves generalized versions); one-sentence remark |
| X3 | Ambient count surrogate barrier: QPs with `k` negative eigenvalues, perfectly conditioned factors and fixed projected widths have expected local and near-optimal counts `>= 128^{-k}(N/k)^{k/2}` and `>= 64^{-k}(N/k)^{k/4}`; rules out a dimension-free replacement for the A3 count, not for the solver | `ND/ambient-local-count-barrier.md`; three reviews | reviewed | LIM |
| X4 | Affine feasibility barrier: width-three affine equalities, bounded coefficients, always-feasible zero point; on every perturbation the optimum label solves SUBSET SUM (Las Vegas consequence); TU single-row example defeats coordinatewise counting (expected `>= (r-1)/4` locally minimal diagonal nodes) | `ND/constrained-smoothing-barrier.md` | reviewed | LIM |
| X5 | Parameterization obstructions: a determinant-one bounded linear inverse destroys conditional independence of retained noise; a bounded inverse can turn ambient cross-curvature into retained curvature `2H + 4 eps` | `ND/smoothed-polynomial-graph-constraints.md` §5 | reviewed | LIM (short) |
| X6 | Single-flow certificate fails at boundary core optima: two-arc example, event of probability exactly `1/16`, projected growth `>= 1`, no uniformly optimal flow on any origin box; chained version makes literal label enumeration cost `2^m` on that event | `ND/core-only-flow-boundary-obstruction.md`; review | reviewed | LIM |
| X7 | Core-only noise with merely convex residual: rotating fiber `(v - 1/2)^2 + (z_1 - v z_2)^2` has fixed projected growth and growth to the optimal set, yet no full-dimensional jointly convex patch; strictly convex variant with interior unique optimizer; both have short SOS certificates | `ND/core-only-noise-rotating-fiber.md` | checked | LIM |
| X8 | Compatibility with width-two hardness: Del Pia-Khajavirad NO family with gap `2^{-2r-4}`; inverse-polynomial noise crosses the threshold with probability `>= 1/2 - delta/(2 sigma) - 1/(2N)` | `ND/sparse-smoothed-hardness-sanity.md` | checked | LIM (remark) |
| X9 | Growth moment beyond two negative directions: the capped moment term is `r B^{1-1/p}` with `p = k/2 > 1` | `ND/expected-smoothed-qp.md` §6 | reviewed | LIM (remark in A1) |
| X10 | The fine law matters: endpoint atom `xi = 1` in `F(x,y) = xy - (x - y)/2` keeps a crossing cell unresolved at every level; only the same-draw fallback solves it | `ND/smoothed-exact-cell-closure.md` §6 (end) | reviewed | LIM (example) |
| X11 | Matching integer corner winners do not certify a cell (mixed QP and separable examples) | `ND/smoothed-miqp-cell-closure.md` §7; `ND/smoothed-mixed-separable-closure.md` §7 | reviewed | LIM (example) |
| X12 | Rational breakpoints are necessary for rational output: `max{0, x^2 - 2} - x` on `[0,2]` has optimum `sqrt 2` | `ND/smoothed-mixed-separable-closure.md` §8 | reviewed | LIM (footnote) |
| X13 | Exposure tests before fixing binaries are unsound: `0 <= x <= z`, `(x - 1/2)^2 + 10 z^2 - 11 z` | `ND/smoothed-mixed-order-polynomial.md` §5 | reviewed | LIM (example) |
| X14 | Two-sided balls are essential for small-multiplier release: `F = v^2/4 + v a + a^2/2` on `[0,1]^2`; weak multiplier `2v^2` example | `ND/small-residual-multiplier-curvature.md` §4; `ND/core-noise-active-stratum-tube.md` §6 | checked | LIM (example) |
| X15 | Residual point output under core noise: box-convex quartics encode Square Root Sum and PosSLP; regularization limits | `EA` Thm `thm:points-quartic-lower`, Prop. `prop:points-active`, Rem. `rem:recourse-quartic` | in `EA` | CITE |
| X16 | Deterministic baselines: binary and explicitly listed labels for A9 (zonotope vertex enumeration); deterministic core grid for flows with error `k L h^2/8` | `ND/smoothed-integer-low-rank.md` §7; `ND/boundary-core-flow-significance.md` §3 | reviewed | COR (discussion) |

### 2.7 Overlap with sibling manuscripts (O)

| ID | Development | Location | Disposition |
| --- | --- | --- | --- |
| O1 | Core-noise value oracle at all precisions, selected-core Cauchy name, coupled-polytope version, joint-convex coordinates | `EA/sections/10-recourse.tex` Thm `thm:recourse-core`, Cor. `cor:recourse-joint`; sources `ND/all-scale-core-value-oracle.md`, `ND/core-only-noise-core-oracle.md`, `ND/coupled-polytope-core-value-oracle.md`, `ND/joint-convex-core-point-oracle.md` | CITE (contrast: Cauchy names under merely convex residuals vs. exact output under structured recourse) |
| O2 | Exact QP output by Cauchy reconstruction in core-noise models | `EA` Cor. `cor:recourse-qp`; `ND/qp-core-cauchy-reconstruction.md` | CITE (contrast with A2-A4 and C1) |
| O3 | Full selected points under a convexifier; residual-convex cubics | `EA` Thm `thm:recourse-convexified`, Thm `thm:recourse-cubic` | CITE |
| O4 | Finite-law transfer, section counts, lexicographic fallback, projected-growth tail (uniform expanding-map proof) | `EA/appendices/I-recourse.tex` | re-proved here in greater generality (ambient noise, mixed and semialgebraic domains, Kolmogorov-close laws); overlap stated explicitly |
| O5 | Deterministic coordinate grids, `L_i w^2/8` corrections, min-marginal filtering, growth localization, deterministic exact output and implicit boundary output with a complementarity margin, conditional-recourse filter, TU coupling, structural limits | `DA` Sections 3-9 and Appendices (`thm:cr-filter`, `prop:star`, `thm:boundary`) | CITE as deterministic counterpart; F1 re-proved (short) |
| O6 | Smoothed penalty perturbations for sparse indicator quadratics (exact messages) | `SI` main theorem | CITE (sibling smoothed model) |
| O7 | Deterministic conditioned sparse polynomial pruning, exact implicit convex patch under a Hessian-at-optimum premise, deterministic boundary enclosures | `ND/polynomial-pruned-grid-extension.md`, `ND/implicit-convex-patch-certificate.md`, `ND/deterministic-boundary-output.md`; `DA` Section `sec:polynomial` and Appendix `app:boundary` | CITE (`DA`) |
| O8 | Rectangular active-sign precision and expanded algebraic output barriers | `EA` Props. `prop:points-rectangle`, `prop:points-algebraic-output` | CITE (explains implicit output contract) |

### 2.8 Excluded or superseded (E)

| ID | Development | Source path(s) | Reason |
| --- | --- | --- | --- |
| E1 | High-probability growth by maximal response slopes | `ND/smoothed-linear-growth.md` | superseded by F3/F4 |
| E2 | Summed-response refinement | `ND/summed-response-growth.md` | superseded by F3/F4 |
| E3 | Core-only noise with strongly convex **interior** residual | `ND/core-only-noise-strong-recourse.md` | superseded by C8 (keep its two lemmas inside C8) |
| E4 | One- and two-core value oracle; continuous-noise value comparator; integer value-oracle corollary | `ND/core-only-noise-value-oracle.md`, `ND/continuous-core-noise-value-oracle.md`, `ND/core-value-certified-recourse.md` | belong with O1; random-real input model out of scope |
| E5 | Affine optimal fibers and selector interface | `ND/affine-convex-fiber-certificate.md` | structural, no closure theorem |
| E6 | Core-noise exploration note | `ND/core-only-noise-exploration.md` | exploration, conclusions captured by X7 and C8 |
| E7 | TU feasible rounding, TU polyhedral count, fixed-polytope chamber count | `ND/tu-feasible-rounding.md`, `ND/tu-polyhedral-cell-count.md`, `ND/polyhedral-chamber-count.md` | supporting lemmas or scope boundary only at their proved scope (root decision 5); no smoothed TU optimization theorem |
| E8 | Random screening for indicator QPs | `ND/screening-percolation.md` | out of topic (D3) |
| E9 | Deterministic sparse and negative-curvature open targets | `ND/negative-curvature-sparse.md`, `ND/scalar-message-growth-obstruction.md`, `ND/psd-extraction-curvature-obstruction.md` | deterministic; open problems only |
| E10 | Genericity audit of Monte Carlo component solvers | `ND/polynomial-component-genericity-audit.md` | explains why F15 is needed; no theorem |

## 3. Supersession and specialization relationships

1. F3 (proximal tail) supersedes E1 and E2. F4 is its QP finite-law form;
   F6 gives the polynomial and semialgebraic finite-law form.
2. A2 (aligned closure) supersedes A10 for exact output. A3 and A4 change
   the noise model, not the closure: A2's extraction and fallback are reused
   unchanged. A4 removes A3's ambient dimension powers under a different
   law; A3 is not subsumed because its law is uniform.
3. A1 is not subsumed: for `k <= 2` and the uniform ambient law its
   numerical dependence `1 + nu W/sigma` is sharper than A3's
   `Theta_amb`. It is the growth-moment route whose failure for `k > 2`
   (X9) motivates closure.
4. A5 extends A3 to integers (label gap); A6 composes A4 and A5. A7 is the
   separable product-box case with unrestricted integer dimension; A8 is
   its anisotropic Gaussian form. A9 is a different exactness mechanism
   (objective lattice, no fallback) on pure-integer boxes.
5. B2 is the quadratic case of B3 with exact rational output and
   elementary tail constants. B4-B9 are domain extensions of B3; B8
   extends B7, and its transport count, specialized to continuous orders,
   supersedes B7's chamber count (root decision 3).
6. C3 generalizes C1's interface from exact to certified recourse; C1
   remains needed for nonconvex exact recourse (forests, C2) and rational
   output. C6 is an implicit-output variant of C5. C8 supersedes E3.
7. Network flows are TU, so C13 contains the flow cases of C11 and C12.
   C9 (interior, general convex arc costs, sharper bound) is not
   subsumed by C11 (which has the weaker `f_d(k)` factor); C12 recovers the
   sharper bound only for bilinear coupling.
8. D2 extends D1 and depends on F15.
9. Overlap: O1-O3 (exact-arithmetic) solve value/point Cauchy-name
   problems under weaker residual structure; this paper's Route C solves
   the sampled problem exactly under stronger recourse structure. O5 and
   O7 (decomposition-aware) are the deterministic, growth-conditioned
   counterparts of Route B and of the closure tests.

## 4. Precise models

### 4.1 Input model

Explicit rational data in binary; `I` = base input length, including the
noise scale `sigma`, every supplied curvature bound and the encoding of its
certificate, every supplied tree decomposition, factor `(T, alpha)` or core
partition. Certificate verification work belongs to the running time, not
to `I` (root model review, item 8). Sampled coefficients are not part of `I`; their bit length `b`
appears separately. Curvature bounds (`L`, block or full Hessian bounds,
`mu`) are promises unless derived by termwise monomial bounds, which have
polynomial encoding length at fixed degree. Convexity premises (residual
convexity, arc-cost convexity, TU) are promises or checkable certificates;
recognition is not claimed. Numerical ratios such as `L w_max/sigma`
enter the bounds numerically, not through their encoding lengths.

### 4.2 Noise laws

| Code | Law | Used by |
| --- | --- | --- |
| N1 | Ambient uniform grid: every original linear coefficient i.i.d. uniform on `G_M(sigma) = {-sigma + 2 sigma j/(M-1) : 0 <= j < M}`, `M` a power of two computed from base data before sampling, `log M = poly(I)` | A1, A3, A5, A7(b), B1-B9, C1, C3, C5 |
| N2 | Aligned factor noise: `xi in G_M(sigma)^k` i.i.d., perturbation `T^T xi` (correlated, low-dimensional support) | A2, A7(a), A9 (per-row `sigma_i`) |
| N3 | Core-only uniform grid: only core coefficients perturbed | C8, C9, C11-C13 (C11: `log M <= f_d(k) poly_d(I)`) |
| N4 | Finite Gaussian-like law: one scalar law (rejection sampler, Kolmogorov error `<= 2^{-b}`, support radius `(b+20)sigma`, `b` from a base-only support/precision loop), i.i.d. on all original coefficients | A4, A6, A8 |
| N5 | Strong-field grid: `G_M(sigma)` with `M >= 16 Delta max_i a_i` and large `sigma` | D1, D2 |
| N6 | Graph models: ambient noise on free and dependent coordinates; analysis conditions on dependent-coordinate noise | B4, B5, B9 |

Every theorem concerns the specific base-chosen law. Arbitrary coarser
atomic laws are not covered (X10). No draw is discarded or resampled;
correctness holds on every atom; only work is averaged.

### 4.3 Output contracts

| Code | Contract | Used by |
| --- | --- | --- |
| OC1 | Exact rational global optimizer and optimal value | A1-A9, B2, C1, C2, D1, quadratic cases of C5/C9/C12 |
| OC2 | Implicit convex patch: fixed integer labels and original bounds, a rational box or relative polytope containing every optimizer, a verified Hessian modulus; its unique minimizer is the optimizer. Compact descriptor of polynomial length; certified `2^{-q}` point and value in `poly_d(I+q)`; the global pruning record has only an expected-size bound | B3-B9, C3, C6, C8 |
| OC3 | Exact algebraic fallback output: lexicographically first optimizer, univariate defining polynomials and isolating intervals; size and refinement cost `B poly(I + b + q)`; expected cost polynomial | fallback branch of B3-B9, C3, C8 |
| OC4 | Integer label plus small-core common-root algebraic representation of size `c_d^k poly_d(I)` on **every** draw (`f_d(k) poly_d(I)` for C11) | C5, C9, C11-C13 |
| OC5 | Structured component output with symbolic value sum (no exact comparison of unrelated algebraic sums) | D2 |
| OC6 | Implicit graph point: rational retained coordinates plus scalar root equations (exact feasibility); rounded ambient coordinates are not claimed feasible | B5 |

Every route also yields F18's original-objective interval.

### 4.4 Parameters

`k` (search dimension: rows of the supplied factor, equal to the negative
inertia after normalization, or core size); `p` (largest bag size);
`n_Z` (integer dimension); `L` (coordinate upper curvature on the
continuous hull, core-only in Route C); `Lambda` (full Hessian upper bound,
order domains); `alpha` (factor curvature, `2 nu <= alpha < 4 nu` after
normalization); `nu = max(0, -lambda_min(H))`; `beta = alpha ||T||^2`;
`mu` (residual modulus); `Delta` (maximum primal degree, Route D);
`sigma`, coordinate widths `w_i`, `W = sum w_i`, `w_max`, `diam(P)`.
Bounds of the form `C_0^p [...]^p` with `n` inside the bracket are
fixed-width polynomial (XP), not FPT; Route A uniform-ambient bounds are
`n^{O(k)}`; Route A aligned and Gaussian-like bounds, A9 and Route C are
FPT in the stated parameters with absolute input exponents.

## 5. Proof dependencies the manuscript must supply or cite

### 5.1 Internal results to state once (currently repeated or delegated)

1. A general finite-law tail lemma for compact domains given by a
   quantifier-free formula with polynomial atoms and integer-label
   disjunctions: growth tail (F3 + F6) and active-margin tail (F7). The
   notes prove it for boxes and then adapt formulas for simplices
   (B6 §6 says the adaptation "requires explicit review"), order
   polytopes, graphs, implicit graphs and the integer polytope `Y` of C5.
2. A general lexicographic fallback lemma (F10) for the same class of
   domains; the QP active-face enumeration (F9) as the rational special
   case.
3. The localization lemma F12 and the budget order F16, currently
   re-derived inside each theorem.
4. The explicit retained-cell count and exact reconstruction rule of the
   conditioned negative-inertia solver (A0), which A1 uses by "unpacking"
   its proof.
5. The two lemmas C8 imports from the excluded antecedent E3: the growth
   lift `g_F = min{g_V/(1+2H^2), mu/4}` and the two-block projected-growth
   formula under core-only noise.
6. The core search of C5 (imported by C9 and C11-C13) and the deterministic
   face certificate C10.
7. The constant-base solver F15 with its full constructive proof (root
   decision 1); it serves C5, C9, C11-C13 and D2.

### 5.2 External results to cite (Luna to confirm exact statements)

Renegar 1992 (Thm 1.1: block-sensitive format and bit bounds); Basu-Lerario
2023 (Thm 1.1, tubes of singular algebraic sets); Grötschel-Lovász-Schrijver
1988 (Def. 2.1.10, Cor. 4.2.7, Sec. 1.2-1.3, 4.1); Kozlov-Tarasov-Khachiyan
1980 (exact convex QP); Del Pia 2023/2025 (arXiv 2311.00099, Thm 3,
"accurate" solution contract, FPT in integer dimension); Del Pia 2026
(rational Jacobi rotations, Thm 2-3); Del Pia-Khajavirad (treewidth paper:
strong NP-hardness at width two, exact rational forest oracle, Thm 1,
Lemmas 15-19, Thm 3); Hochbaum-Shanthikumar 1990 (Thm 4.3, Alg. 4.2);
isolated-root Bezout bound; semialgebraic dimension (Bochnak-Coste-Roy or
Basu-Pollack-Roy); Rockafellar 1970 and Evans-Gariepy 2015 (conjugates,
a.e. differentiability, area formula); univariate root isolation and
Cauchy bounds (Basu-Pollack-Roy); conformal decomposition and TU circuits
(Graver; proof is self-contained in C13).

## 6. Vulnerabilities and claims needing repair

These were found while reading; none defeats the subject. Items marked
"check" need fresh adversarial re-derivation before the TeX is final.

1. **Scope wording (repair).** Several summaries say "expected polynomial"
   without the numerical-ratio qualifier. Every theorem must state that
   the bound is polynomial in `I` and in the displayed numerical ratio
   for fixed structural parameters; Route B is XP in `p`; uniform-ambient
   Route A is `n^{O(k)}`.
2. **Non-box finite-law adaptations (repair).** See 5.1(1-2). B6 records
   that its formula adaptation "requires explicit review". One general
   lemma closes this for B4-B8 and C5.
3. **A1 depends on an unpacked exponent (repair).** The count
   `Z^{k/2}(1 + log Z)^d` must be derived explicitly from A0's
   `2^k (sqrt(k kappa) + 4)^k` cells per level and its exact-reconstruction
   depth `poly(I) + O(log kappa)`.
4. **F15 attribution (statement).** Root decision 1 includes the
   constant-base solver with a full proof. Its mechanisms (deformation,
   multiplication matrices, rational univariate representations) are
   classical; Luna must compare Rouillier and Basu-Pollack-Roy, and the
   paper must not claim a new general algebraic complexity result. D2 needs
   the constant base essentially; C5, C9, C12 use it for their additive
   `c_d^k` term. The stale symbol `A_d(k)` in
   `ND/native-integer-recourse-implicit-closure.md` must not be copied.
5. **C11 sampling length (statement).** The law itself has
   `log M <= f_d(k) poly_d(I)`; the theorem must not say "polynomial-bit
   law" in that case. C12/C13(b) restore polynomial sampling.
6. **C9 premise (statement).** Interiority must hold for every noise
   vector in the cube; it is a supplied promise with a checkable
   sufficient condition, not a property of the draw.
7. **Proof-record size (statement).** Only the compact patch descriptor
   has a per-draw polynomial bound; global pruning records, fallback
   representations and their evaluation have expected bounds only.
8. **Gaussian-like law (statement).** It is one specific finite law with
   base-chosen accuracy; no exact-real Gaussian input, and no claim for
   arbitrary coarse Gaussian approximations.
9. **Notation clashes (repair).** `p` is bag size in Route B but integer
   dimension in A5/A6 notes; `k` is factor rank and core size (kept, as the
   search dimension); `M` is grid size and a constraint matrix; `H` is a
   count factor, a Hessian, and a full-Hessian bound; `d` is degree and
   factor noise; `T` is a factor and a third-derivative bound; `q` is a
   precision, a per-bag continuous count, and a face dimension;
   `R` is a base count and the residual index set; `B` is a bag and the
   fallback work factor. The root's `notation.md` governs; `architecture.md`
   §7 lists additions and four requested clash resolutions (bags `B_t`,
   inequality rows `m`, continuous bag size `p_c`, third-derivative bound
   `M_3`).
10. **Check: ambient volume lemma (A3).** Projected-zonotope volume and
    the complementary-minor identity; Cauchy-Binet bound by `n^{t/2}`.
11. **Check: mixed section count (A5).** Fixed-label regions cover each
    noise line; the mixed value is a minimum of at most `R` quadratics,
    hence the `2R^2` breakpoint count.
12. **Check: Gaussian weighted sum (A4, A8).** The capped lattice sum
    constant and the majorant `c^{-t/2} prod phi_s` for frames with
    `c < 1/2` (A8 uses `c = 1/16`).
13. **Check: order chambers (B7) and binary transport (B8).** Closed-face
    representation by a fixed list of copy maps (limit argument) and the
    directional constant `n_c Lambda`.
14. **Check: simplex count (B6).** Anchor conditioning for tight-budget
    faces and the transformed-tuple multiplier bound without independence.
15. **Check: implicit DP error accounting (B5).** `D_j = N delta_j <= E_j`,
    witness gap `4E_j`, and nonsingularity of the bordered KKT root.
16. **Check: flow value margin (C11).** Two-block formula defining
    `(m^2, infinity)`, reciprocal Cauchy bound, and the identity argument
    for within-interval marginals.
17. **Check: TU compact dual (C13).** Cellwise integrality of the
    interpolated problem and the dual vertex bound `mV`.
18. **Check: three-block boundary formula and release constants (C8).**
19. **Check: F15 completeness.** Bounded-branch limits, moment-curve
    separation count `Q`, and the claim that spurious candidates are
    feasible.
20. **Check: F3 area-formula step.** `det DP = 0` a.e. on `E` and the
    trace inequality.
21. **Scope: C9 is proved for network flows only.** Its uniform-flow
    certificate uses shortest-path-tree potentials; the TU note (C13)
    transfers C11 and C12, not C9. Either prove the transfer with the
    compact-dual charts or keep part (c) of Theorem C4 network-only.
22. **Aligned noise does not isolate integer labels (scope).** Distinct
    labels can share a factor image and stay tied on every aligned draw
    (root finding: `-x^2` on `[-1,1]` plus a free binary `z` with
    `T = (1,0)`). A5/A6 need ambient noise on integer coefficients; A7
    (separable) uses scalar recourse and tolerates persistent ties.
23. **Regret endpoints (statement).** F18's interval has algebraic or
    implicit endpoints unless rational enclosures and a feasible rational
    point are used; finite-precision evaluation error must be charged to
    `delta`. Strong-field noise cannot be made small, so F18's calibration
    `sigma = epsilon/(2W)` excludes Route D; the Gaussian-like sampler's
    support radius `(b+20)sigma`, not `sigma`, enters the regret bound.
24. **Implicit graph outputs (statement).** A feasible graph can contain
    no rational point (`y^2 - 2 = 0`, `y in [1,2]`). B5 must use a charted
    descriptor: certified chart, unique reduced patch optimizer and exact
    lift; certificates for the original objective evaluate an exactly
    feasible lift. Explicit graphs (B4) map rational free points to
    rational feasible points.
25. **Fallback is not universal (statement).** A9 (objective lattice) and
    D1/D2 (exact component solves) need no rare fallback; the template
    theorem must allow this.
26. **Global certification needs the trace (statement).** A final
    whitelist alone does not certify global optimality; keep the pruning
    and DP record or permit recomputation (Sol sparse audit).
27. **Order closure test (repair).** Use the weighted Hessian test
    `B' Hess B - (T r + g_0) D_B > 0` of the face-closure lemma; it is
    sharper than the unweighted composition test.
28. **Selector promise (overlap).** `EA`'s core-noise outputs use the
    lexicographically least core and least residual norm; the exact
    results here return a deterministic optimizer, not that canonical
    selector, except in the lexicographic fallback.
29. **TU rounding scope (statement).** The rounding lemma needs `b/h`
    integral on every grid and a full Hessian bound (equality `x_1 = x_2`
    with objective `2 x_1 x_2` has positive rounding error despite zero
    diagonal curvature); it supplies neither an expected count nor closure.
30. **Instance-dependent finite law (statement).** No universal law for an
    input-length class is proved; keep the constructed-law contract.

## 7. Overlap summary for the manuscript

* With `EA`: the finite-law tools (F5, F6, F10) and a projected-growth
  tail appear in `EA` Appendix I for core noise. This paper needs them for
  ambient noise, mixed and semialgebraic domains, and Kolmogorov-close
  laws, so it states and proves its own versions and says that the
  core-noise versions appear in `EA`. The value/core/point theorems O1-O3
  are cited as a complementary output model. X15 is cited.
* With `DA`: F1 and B10's deterministic filter, X2, the deterministic
  growth-conditioned grids and the deterministic boundary output theorem
  are cited; this paper re-proves only F1 (short) because every count uses
  it.
* With `SI`: a sibling smoothed model (penalty noise for indicator
  quadratics) is cited in related work.

## 8. Antecedent folders

`research-20260922/` (ridge envelopes, benchmark bounds, OBBT and other
scouting) and `research-20260927/` (exact algebraic, PosSLP and
Hessian-span results, mostly convex) contain no development used by this
paper. `research-20260927/polynomial-nonlinear-dimension-optimization.md`
and `ordered-perturbation-optimizer.md` concern convex exact outputs and
belong with `EA`.

## 9. Literature requests for the root's Luna lead

Requests only; this agent did not search.

1. Confirm the exact statements in 5.2, especially Renegar's bit bound
   and format exponents, Basu-Lerario's constant, Del Pia's MIQP contract
   and exponent, Hochbaum-Shanthikumar's oracle model, and the
   Del Pia-Khajavirad forest oracle.
2. Closest prior work for smoothed or random-perturbation analyses of
   **exact** continuous or mixed global optimization (beyond Kelner-Nikolova
   2007, Beier-Vöcking 2004/2006, Röglin-Vöcking 2007, Röglin-Rösner 2017,
   Beier-Röglin-Rösner-Vöcking 2022/2023 Pareto counts), including any
   expected-complexity results for perturbed nonconvex QP.
3. Qualitative generic growth: Lee-Phạm 2016 (Thm 6.1) and 2017 (Thm A);
   Bonnans-Ioffe 1995; Drusvyatskiy-Lewis 2013; Azagra-Cappello-Hajłasz
   2023 (Alexandrov) - confirm statements used in comparisons.
4. Parametric QP and critical regions: Ding 1996 thesis (Thm 2.2.5, 2.3.1);
   Bemporad et al. 2002; Tøndel et al. 2003; Patrinos-Sarimveis 2011;
   Vavasis 1992; Luo et al. 2019 (spectral branch-and-bound); Del Pia 2023
   (approximation for indefinite MIQP).
5. Order and isotonic: Stanley 1986; Bach 2018 (nonconvex isotonic,
   common-quantile coupling).
6. Small-dimensional exact polynomial optimization with constant-base
   complexity (comparison for F15): Basu-Pollack-Roy critical-point
   methods, rational univariate representations, Gimenez-Matera 2016
   (Monte Carlo), and any deterministic `c_d^k` bound.
7. Random-field pinning and component counting for D1/D2: Gamarnik et al.
   2014; Helmuth et al. 2021.
8. Separable convex integer optimization and flows: Hochbaum-Shanthikumar
   1990; Végh 2016; Schöbel et al. 2014; Brand et al. 2024 (separable
   convex MIP).

## 10. Coverage count

In-scope developments: F1-F18 (18), A0-A9 (10; A10 excluded), B1-B10
(10), C1-C13 (13), D1-D2 (2; D3 excluded), X1-X16 (16): **69 in-scope
IDs**. By type: 27 theorem-level results (F3, F15, A0-A9, B2, B3, B5-B8,
C1, C3, C5, C8, C11-C13, D1, D2), 18 supporting lemmas, certificates or
cited oracles (F1, F2, F4-F14, F16, F17, B1, C7, C10), 8 corollaries or
examples (F18, B4, B9, B10, C2, C4, C6, C9) and 16 limitations. Root
decision 1 keeps F15 and D2. These 69 entries include lemmas, cited
oracles, examples and limitations; they are not 69 independent original
contributions. Overlap items O1-O8 are cited; E1-E10 are excluded, open,
or (E7) supporting at their proved scope.
