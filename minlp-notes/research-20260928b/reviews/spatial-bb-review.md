# Adversarial review: spatial branch-and-bound theory, scout Section 3

Date: 2026-09-28. Scope: Section 3 of
[`../scouting/spatial-bb-theory.md`](../scouting/spatial-bb-theory.md). This
covers the model and Lemma 0 (3.1), Theorem B and its remarks (3.2), Theorem D,
its corollary and the stratum integrals (3.3), Theorem A and its tightness
example (3.4), Theorem C and the (QD) remark (3.5), the rate table (3.6) and the
McCormick example (3.7). The reviewer did not write the scout report and did not
edit it. Reviewer scripts and logs are in [`spatial-bb/`](spatial-bb/). They
do not reuse the scout's code.

## Verdict

The four main inequalities hold. After the fixes below, the proofs of Lemma 0
and Theorems A–D are complete. No counterexample to any of them was found, and
independent code reproduces the scout's 1D numbers exactly. The errors are in
side claims:

- the sufficient condition for (QD) is false as stated;
- the claim that the three quantities agree "up to `e^{O(n)}`" hides
  instance constants;
- Lemma 0's per-node piece count is wrong for iterated reduction;
- two rows of the rate table overstate what is proved.

The novelty assessment is in Section 9. In short, Theorems A–D are short
transfers of known Lipschitz and bandit arguments to a relaxation-gap model:
per-cell covering, packing, and level-by-level counting. The cluster
literature is not free of lower counts. Neumaier (2004, Section 15) gives a
heuristic lower count for boxes of fixed width, and it already contains the
`(const^n/det G)^(1/2)` prefactor and the dimension drop under active
constraints. What was not found in the sources checked:

- a rigorous version for adaptive trees with arbitrary box shapes;
- the per-box AM–GM and arcsine computation;
- the vertex-localization steps;
- Lemma 0;
- the vertex-exact examples.

The absence of a log factor in Theorem B is not special to the quadratic
gap. The same covering argument appears to remove the log factor from the
Lipschitz lower bound of Bachoc et al. as well (Section 9.3).

| Claim | Verdict | Main point |
|---|---|---|
| 3.1 model, (G_alpha), alpha-valid family | correct, clarify | (G_alpha) is used only at feasible points; state it for the projected relaxation value |
| Lemma 0 | correct with fixes | decompose frames per reduction round, not per node; bounds taken from sub-boxes; scope of "FBBT" |
| Theorem B | correct | constant sharp for `n = 1`; the AM–GM step loses about `0.81^n` per cube |
| Remark: anisotropic alpha | correct | |
| Remark: low-rank | correct as a lower bound | the 3.6 row also claims an unproved upper bound |
| Remark: exact finite certificates | correct | necessary condition only |
| Theorem D | correct | |
| Corollary (bound tightening) | correct within its model | excludes objective-cutoff propagation, which escapes the bound on the scout's own instance |
| 3.3 stratum integral, axis-aligned strata | correct | |
| 3.3 stratum integral, bounded aspect ratio | correct, but not a bound on `N_opt` | restricts the family, not the problem |
| Theorem A | correct | `F = X0` is essential; constant depends on `kappa` |
| Theorem A tightness example | correct | |
| Theorem C (proof) | correct | |
| (QD) sufficient condition, `K = max(2, M)` | false | norm factor `n` and neighbourhood size; corrected statement below |
| "all three quantities agree up to `e^{O(n)}`" | false as stated | ratio depends on `K`, `kappa` and `K/alpha` |
| 3.6 rate table | mostly correct | sharp row: "avoids dyadic points" is false; low-rank row: upper side unproved |
| 3.7 McCormick example | correct | `Omega(eps^(-1/2))` for widest-side bisection is proved; the matching upper bound is numerical |

## 1. Model and Lemma 0

### 1.1 Hypotheses

- **Where (G_alpha) is used.** Every proof uses (G_alpha) only at feasible
  points `y in F ∩ B`. For relaxations in lifted variables, the relevant
  function is the projected value `f_B(y) = inf{t : (y,w,t) in R_B}`. Stating
  (G_alpha) for this function on `F ∩ B` is what the proofs need. It is weaker
  than the stated hypothesis.
- **Tolerance.** "Pruned at tolerance `eps`" means `LB(C) >= UBD - eps` with
  `UBD >= f*`. Relative gaps reduce to this. If a node is pruned when
  `LB >= UBD - max(eps_abs, eps_rel |UBD|)` with `eps_rel <= 1`, then
  `LB >= f* - max(eps_abs, eps_rel |f*|)` for every `UBD >= f*`. The three sign
  cases of `f*` and `UBD` each give this directly. So the theorems apply with
  `eps := max(eps_abs, eps_rel |f*|)`. Termination by a global gap is the same
  test applied to the open nodes. Incumbents accepted within a feasibility
  tolerance can have `UBD < f*`; then `f*` must be read as the optimal value of
  the tolerance-relaxed problem.
- **Pruning by infeasibility.** A valid relaxation satisfies `R_B ⊇ F ∩ B`. An
  infeasible relaxation therefore proves that `B` contains no feasible point,
  and (V) holds vacuously. A box whose relaxation is infeasible but which
  contains feasible points cannot occur in exact arithmetic. Floating-point
  infeasibility verdicts are outside the model.
- **Inherited bounds.** A node bound `max(own bound, parent bound)` is covered,
  because `S ⊆ B` implies `q_S <= q_B` on `S`.
- **Bounds taken from sub-boxes.** Strong branching and probing can set a
  parent's bound to the minimum of its children's bounds. If the parent is
  then recorded as the pruned leaf, (V) holds only with the children's `q`,
  which is smaller than the parent's. The children must be recorded as the
  leaves. Their relaxations were solved, so the relaxation count is unchanged.

### 1.2 Leaves and pieces form a covering

Children of an axis-parallel split are closed boxes that share a face. Leaves
and removed pieces together cover `X0`, with disjoint interiors. Theorems A, B
and D use only the covering property: the integral in B and the Hausdorff
measure in D are subadditive, and A needs only that every `y` lies in some
`C`. Shared faces and degenerate pieces are therefore harmless.

### 1.3 The removed region

The region removed by one reduction is a frame `B \ int(B')` for a sub-box
`B' ⊆ B`. It is L-shaped only when `B'` shares a vertex with `B`. The slab
decomposition splits any such frame into at most `2n` boxes inside `B`: for
`i = 1..n`, take `y_j in [l'_j,u'_j]` for `j < i`, `y_i in [l_i,l'_i]` or
`[u'_i,u_i]`, and `y_j in [l_j,u_j]` for `j > i`. That part of the lemma is
right.

**Fix 1: decompose per reduction round.** The proof needs every piece `S` to lie
inside the box `B_k` whose relaxation excluded its feasible points, so that
`q_S <= q_{B_k}`. Iterated OBBT removes points from `B_k` using `f_{B_k}` for
`k = 0, 1, ...`, and the scout's `obbt_1d.py` runs up to 20 rounds per node.
Splitting the merged frame `B_0 \ B_final` into `2n` boxes can break (V). In
[`spatial-bb/obbt_2d.py`](spatial-bb/obbt_2d.py) (2D, separable exact alphaBB,
iterated OBBT), merged-frame pieces violate (V) in every run: 15 of 40, 37 of
82, 60 of 119, 10 of 42, 68 of 180 and 151 of 683. With one frame per round,
all leaves and pieces satisfy (V), the areas sum to 1, and `|P|` exceeds the
Theorem B bound in every run.

Consequently, "each processed node yields at most `2n` pieces" is false for
iterated reduction. The correct count is at most `2n` pieces per reduction
round. The relaxation count still holds, with this accounting:

- each bounding solve yields at most one leaf;
- each objective-based round (OBBT solves `2n` LPs per round; reduced-cost
  tightening uses the LP solution of the current box) yields at most `2n`
  pieces that can contain feasible points;
- consecutive rounds of purely feasibility-based reduction can be merged into
  one frame, because their pieces contain no feasible points.

Pieces without feasible points contribute nothing in Theorem D, and in
Theorem B (`F = X0`) feasibility-based reduction removes nothing. So the
number of relaxations solved is at least `#{C in P : C ∩ F ≠ ∅}/(2n+1)`, which
is what the corollary uses. Reusing the duals from `B_k` on `B_{k+1}` is also
fine, since the pieces of `B_{k+1} \ B_{k+2}` lie in `B_k`.

**Fix 2: scope of "feasibility-based reduction".** Solvers propagate the
objective cutoff `f(y) <= UBD` (or `UBD - eps`) through the expression graph
with interval arithmetic. This removes feasible points using information other
than (G_alpha). It is therefore not "feasibility-based reduction that removes
only infeasible points", and the pieces it removes need not satisfy (V). The
scout's last sentence under the corollary excludes it, but the bold claim "bound
tightening cannot change the `eps`-exponent" invites a wider reading. On the
scout's own instance `nondeg1` (`t^2 - 2t^4`, alpha = 13/3),
[`spatial-bb/fbbt_cutoff_1d.py`](spatial-bb/fbbt_cutoff_1d.py) shows:

| eps | Theorem B bound without cutoff propagation | cutoff `f <= UBD - eps` | cutoff `f <= UBD` |
|---|---|---|---|
| 1e-2 | 3.25 leaves | root emptied after 4 FBBT rounds, 0 relaxations | 1 node, 1 relaxation |
| 1e-5 | 7.86 leaves | root emptied after 6 rounds, 0 relaxations | 1 node, 1 relaxation |
| 1e-8 | 12.44 leaves | root emptied after 7 rounds, 0 relaxations | 1 node, 1 relaxation |

The `log(1/eps)` lower bound thus describes the (G_alpha) bounding mechanism,
not the problem. The same happens whenever the expression makes
`f >= f* - eps` evident to interval arithmetic, for example the ring
`(|t|^2 - r^2)^2 <= -eps`, which is empty at once. The bold sentence in 3.3
should say "same-relaxation bound tightening"; Section 4 of the scout report
already does.

**Lemma 0 verdict: correct with fixes.** Replace "L-shaped region" by "frame",
decompose per reduction round, record children as leaves when a parent bound
comes from its children, and state the relaxation count for boxes that meet
`F`.

## 2. Theorem B

**Correct.** Each step checks:

- (V) gives `(f-f*+eps)^(-n/2) <= (alpha q_C)^(-n/2)` on `C` (this needs
  `eps > 0`; the case `eps = 0` is the remark on exact certificates);
- AM–GM gives `q_C^(-n/2) <= n^(-n/2) prod_i a_i^(-1/2)`;
- `integral_l^u ((t-l)(u-t))^(-1/2) dt = pi` for every interval;
- only covering is used when summing.

**The constant.** It is sharp for `n = 1`. Take the sawtooth
`f = alpha (y-kh)((k+1)h-y)` on each of `N` cells of width `h = 1/N`. The grid
is valid for every `eps >= 0`, and the bound tends to `N` as `eps -> 0`.
[`spatial-bb/thm_b_1d.log`](spatial-bb/thm_b_1d.log) gives `N_opt = N` and
ratio `N_opt/bound = 1.000` at `eps = 1e-9` and `1e-12` for `N = 3` and `N = 7`.

For `n >= 2` the AM–GM step loses a factor on every box. With the substitution
`y_i = l_i + w_i sin^2(theta_i)`, the ratio of the true per-box integral to
`pi^n n^(-n/2)` is an average of `prod(x_i)/(mean x_i^2)^(n/2)`. Monte Carlo
estimates for cubes ([`spatial-bb/amgm_constants.log`](spatial-bb/amgm_constants.log))
are 0.742 (`n = 2`), 0.580 (`n = 3`), 0.189 (`n = 8`) and 0.033 (`n = 16`),
about `0.81^n`. Elongated boxes lose more (0.045 at aspect ratio 100 in 2D).
Whether `N_opt` itself loses this factor on some instance is not known.

**Independent 1D checks.** [`spatial-bb/thm_b_1d.py`](spatial-bb/thm_b_1d.py)
decides validity exactly from critical points and computes the minimum
certificate by the greedy cover. For exact alphaBB a box is prunable exactly
when (V) holds on it, so this minimum equals `N_opt`. The script reproduces the
scout's values exactly: `N_opt` = 6/13/21, 3/18/101 and 2/2/2, with bounds
3.255/7.859/12.437, 1.318/10.73/63.56 and 0.598/0.658/0.659. On 40 random
degree-6 polynomials with random `alpha` and random `eps` in
`[1e-9, 1e-1]`, the smallest ratio `N_opt/bound` was 1.47.

**Remarks.**

- *Anisotropic alpha*: correct. AM–GM applied to `alpha_i a_i` gives the
  stated constant.
- *Low-rank*: correct as a lower bound. For each `z`, the boxes of `P` that
  contain `z` give at most `|P|` boxes in the `k` branched coordinates. They
  satisfy (V) for `y -> f(y,z)` with the same constant `f*`, and Theorem B's
  proof uses only that. If only `K` is branched, (V) on `C_Y x Z0` is
  equivalent to (V) for `v(y) = min_z f(y,z)`, so "reduces exactly" is correct
  for the validity condition. That condition is necessary, not sufficient, for
  pruning, so no upper bound follows. See the table row in Section 6.
- *Exact finite certificates*: correct. A certificate at `eps = 0` is valid for
  every `eps > 0`, and monotone convergence gives the condition. The integral
  is finite at sharp minima (`|t|^(-n/2)` is integrable in `n` dimensions) and
  infinite at nondegenerate ones (`|t|^(-n)` is not). This holds only under
  (G_alpha). alphaBB with box-dependent alpha, which vanishes on locally convex
  boxes, and interval-Hessian methods terminate finitely at nondegenerate
  minima (Dym, Section 2; Neumaier, Section 15).

## 3. Theorem D and Section 3.3

**Theorem D: correct.** For `y in S ∩ C`, (V) and `f(y) <= f* + eta` give
`alpha a_i(y) <= eps + eta` for every `i`. Also `a_i >= d_i^2`. Choosing in each
coordinate the endpoint nearest `y_i` gives a vertex `v` with
`|y - v|_inf <= r`, so the vertex claim follows. The points of `C` within sup-distance `r` of `v` lie in a cube of
side `2r <= l0`. Summing uses only covering and subadditivity. Written out, the
bound is `|P| >= H^p(S) alpha^(p/2) / (2^(n+p) c_S (eps+eta)^(p/2))`, the same
as stated. The factor `2^(-n)` from the vertices makes the bound weak for large
`n` at fixed `p`.

A constrained check is in
[`spatial-bb/thm_d_constrained.py`](spatial-bb/thm_d_constrained.py). The
instance minimizes `f = 0` written as `(x^2+y^2) - x^2 - y^2` subject to
`x + y = 1` on `[0,1]^2`. The DC-secant scheme has gap exactly `q_B`, and every
feasible point is optimal (`p = 1`, `c_S = sqrt 2`), so the bound on boxes
meeting `S` is `1/(8 sqrt(eps))`.

| eps | Theorem D bound | explicit certificate (anti-diagonal squares) | widest-side bisection leaves meeting `S` |
|---|---|---|---|
| 1e-2 | 1.2 | 8 | 22 |
| 1e-4 | 12.5 | 71 | 254 |
| 1e-6 | 125.0 | 708 | 3070 |
| 1e-8 | 1250.0 | 7072 | 24574 |

The bound holds, and the certificate is within a constant factor of it
(about 5.7).

**Corollary (bound tightening): correct within its model,** with the Lemma 0
fixes and the scope caveat of Section 1.3. A stronger statement also follows:
in the unconstrained case, Theorem A applies to the family produced by any
run with same-relaxation OBBT. So plain bisection is within a factor
`(2n+1) C_n J_eps` of that run's relaxation count. Same-relaxation OBBT can
therefore save at most a `log(1/eps)` factor. The scout's sharp 1D data (4
versus 27) shows that it can save that much.

**Stratum integrals.**

- *Axis-aligned strata: correct.* On `S ∩ C`, (V) gives
  `f - f* + eps >= alpha sum over free i of a_i`. AM–GM over the `d` free
  coordinates, and covering of `S` by the slices, give the stated constant.
- *Bounded aspect ratio: correct, but not a bound on `N_opt`.* The inequality
  `q_C >= (s_min/2) dist_1(y, vertices of C)` holds because
  `a_i >= d_i (w_i - d_i) >= d_i w_i/2`. With the density bound
  `H^d(S ∩ B(v,t)) <= c_S t^d`, the layer-cake formula gives
  `integral_{S∩C} |y-v|^(-d/2) dσ <= 2 c_S diam(C)^(d/2)`. This yields a
  constant depending on `n`, `d`, `rho`, `c_S` and `alpha`. The hypothesis
  restricts the *family*, for example to bisection trees, so the result is not
  a lower bound on `N_opt`. The text says "cubes of bounded aspect ratio",
  which should read "boxes"; it should also say that this case bounds only such
  families. The scout correctly lists the general case as open.

## 4. Theorem A

**Correct.**

- *Levels.* A non-pruned level-`j` cube contains `y` with
  `m(y) + eps < alpha' q_D(y) <= alpha' n s_j^2/4`. So `2^j` is below
  `s0 (alpha' n/(4 eps))^(1/2)`, which allows at most `J_eps` levels. If
  `J_eps = 0`, the root is pruned and `|T_bis| = 1`.
- *Neighbourhood count.* `y` is within sup-distance `s_j (kappa n)^(1/2)/2` of
  a vertex of the certificate box `C` containing it. The level-`j` cube lies in
  a cube of half-width `R = s_j((kappa n)^(1/2)/2 + 1)`. At most
  `floor((kappa n)^(1/2) + 2)` grid cells per coordinate fit inside it. The
  stated `(sqrt(kappa n)+4)^n`, and `(sqrt(kappa n)+3)^n`, are both valid but
  loose.
- *Charging.* Charge each non-pruned cube to (certificate box, vertex, level).
  There are `2^n |P|` pairs, at most `J_eps` levels, and at most `2^n` children
  per processed node. This gives the stated bound.

Hypotheses:

- `F = X0` is essential. The witness `y` of a non-pruned cube is only
  relaxed-feasible, and (V) is needed at `y`.
- The upper gap `alpha'` is needed only for the bisection relaxation. `P` can
  be any alpha-valid family.
- `C_n = 4^n (sqrt(kappa n)+4)^n` depends on `kappa`.
- The theorem is stated for `2^n`-ary refinement. The same charging works for
  binary widest-side bisection with different constants, because intermediate
  boxes also satisfy `q <= n s_j^2/4`. The scout does not claim more than this.

**Tightness example: correct.** On any `[l,u]` containing `a`,
`f_B = 2|y-a| + (2a-l-u) y + lu - a^2`. This is convex piecewise linear with
slope below `-1` on the left of `a` and at least `1` on the right, so
`LB = -(a-l)(u-a)`. A cell that does not contain `a` has linear `f_B` that is
nonnegative at both ends, so it is pruned. Hence
`|T_bis| = 1 + 2 #{j : 2 (2^(-j))^2 / 9 > eps}`. This matches the scout's
7/9/13/17/19/23/27 and the reviewer's run. `[0,a], [a,1]` has bounds 0.

Numerics ([`spatial-bb/bisection_checks.log`](spatial-bb/bisection_checks.log)):
`T_bis/(J_eps N_opt)` is about 1.03–1.17 on the sharp instance, where the log
factor is attained. It falls from 0.54 to 0.16 on `nondeg1` and from 0.83 to
0.18 on `quartic1`, where it is not attained.

## 5. Theorem C and (QD)

**Proof: correct.**

- *Step 1.* `m(y) + eps < alpha' Q_j`, and (QD) with `|x-y|_inf <= s_j` gives
  `m(x) + eps <= K(alpha' Q_j + s_j^2) + alpha' Q_j = Lambda s_j^2`. The last
  `alpha' n/4` in `Lambda` can be dropped by using `m(y) < alpha' Q_j - eps` and
  `K >= 1`.
- *Steps 2–3.* The sum `sum_j s_j^(-n) V(Lambda s_j^2)` equals
  `integral sum over {j : s_j >= theta(x)} of s_j^(-n) dx`, with
  `theta(x) = ((m+eps)/Lambda)^(1/2)`. The inner geometric sum is at most
  `2 theta^(-n)`.

Numerically, `T_bis` is below the Theorem C bound on every (QD) instance
tried. `T_bis` divided by the integral is stable: 2.6–3.2 for `nondeg1`,
0.66–0.89 for `quartic1`, about 7.1–7.4 for separable 2D `nondeg` and
4.2–4.3 for separable 2D `mixed`. On the sharp instance, the grid estimate of
`K` doubles with every grid refinement (24.5, 49, 98), as expected when (QD)
fails.

**The sufficient condition "(QD) holds with `K = max(2, M)`" is false as
stated.** It has two independent defects.

1. *Norm factor.* Take `m = |x|^2/2` on `[-1,1]^n`, whose gradient is
   1-Lipschitz in the Euclidean norm. With `y = 0` and `x = (t,...,t)`,
   `m(x)/(m(y) + |x-y|_inf^2) = n/2`, which exceeds `max(2, M) = 2` for
   `n >= 5`.
2. *Size of the neighbourhood.* The inequality `|grad m(y)|^2 <= 2 M m(y)`
   needs `m >= 0` and an `M`-Lipschitz gradient on the segment from `y` to
   `y - grad m(y)/M`. A thin neighbourhood of `X0` is not enough. Take
   `m_rho(t) = 4(t-1/2)^2 (t+rho)(1+rho-t)` on `X0 = [0,1]`. It satisfies
   `m >= 0` on `[-rho, 1+rho]`, and its second derivative there is bounded by
   `M ≈ 10` for all small `rho`. But `m(0) ≈ rho` and `m'(0) ≈ 1`, and the
   (QD) constant is at least 3.8, 14.1 and 48.1 for `rho` = 1e-2, 1e-3 and
   1e-4. It grows like `1/(2 sqrt(rho))`.

*Corrected statement.* Let `G = sup over X0 of |grad m|_2`. Suppose `m`
extends to a set `U ⊇ X0 + B_2(0, G/M)` on which `m >= 0` and `grad m` is
`M`-Lipschitz in the Euclidean norm. Then (QD) holds with `K = max(2, nM)`.
*Proof:* `m(x) <= m(y) + |grad m(y)|_2 |x-y|_2 + (M/2)|x-y|_2^2`, which is at
most `2 m(y) + M |x-y|_2^2` by `|grad m(y)|^2 <= 2 M m(y)` and
`2ab <= a^2 + b^2`. Finally `|x-y|_2^2 <= n |x-y|_inf^2`. For growth
`sum_i |t_i|^(q_i)` with `q_i >= 2` on a bounded box, (QD) can be checked
directly: `|x_i|^q <= 2^(q-1)(|y_i|^q + D^(q-2)|x_i-y_i|^2)`, where `D` is the
box diameter.

**The claim "`N_opt ≍ |T_bis| ≍ integral`, with hidden constants `e^{O(n)}`" is
false as stated.** Dividing the Theorem C upper bound by the Theorem B lower
bound gives `2 (4 pi^2 Lambda/(alpha n))^(n/2)`. For exact alphaBB
(`alpha = alpha'`) this is `2 (pi^2 (K+1) + 4 pi^2 K/(alpha n))^(n/2)`. (QD)
adds `m(y)` and `|x-y|^2`, which have different units. Written as
`m(x) <= K1 m(y) + K2 |x-y|_inf^2`, the ratio is
`2 (pi^2 (K1+1) kappa + 4 pi^2 K2/(alpha n))^(n/2)`. At a nondegenerate
minimizer with `m ≈ gamma |t|_2^2`, taking `x - y` along a diagonal forces
`K2 >= gamma n`, so the two bounds differ by at least a factor of order
`(gamma/alpha)^(n/2)`. The constants are independent of `eps`, which is the
main point. They are `e^{O(n)}` only when `K1`, `K2/alpha`
and `kappa` are bounded. The first row of the 3.6 table already shows a factor
`(alpha/gamma)^(n/2)`; the summary and Section 3.5 should say the same.

## 6. Rate table (3.6)

- **Nondegenerate minima: correct.** Recomputing with `m ≈ gamma |t|^2` gives a
  lower bound of about
  `(2 e alpha/(pi gamma))^(n/2) (n/(4 pi))^(1/2) log(1/eps)` per minimizer. So
  `c = 2e/pi ≈ 1.73`, and the bound is exponential in `n` once
  `alpha/gamma > pi/(2e) ≈ 0.58`. The upper bound needs (QD) with the
  corrected constant. The row, and the summary's "`log(1/eps)` at
  nondegenerate minima", hold only for (G_alpha) schemes. Box-dependent alphaBB
  and interval-Hessian methods certify such minima with finitely many boxes
  (Section 2, last remark).
- **Morse–Bott and growth exponents: correct.** Quasi-homogeneous scaling
  `t_i = eps^(1/q_i) u_i` gives the exponent `n/2 - sum_i 1/q_i`. The
  rescaled integral converges exactly when `sum_i 1/q_i < n/2`. With `q_i >= 2`
  the only exception is all `q_i = 2`, which is the log case.
- **Sharp minimum.** The certificate bound is correct. Cells that have the
  minimizer as a vertex satisfy `q <= s |t|_1 <= (c/alpha)|t|_1`. Every other
  cell has some `|t_i| >= s`, so `m >= c s >= alpha n s^2/4 >= alpha q`.
  Clipping cells to `X0` keeps both properties. **But "bisection needs
  `Theta(log(1/eps))` when the minimizer avoids dyadic points" is false.** Take
  `f = 2|y-z| - (y-z)^2` with `z = sum_k 2^(-2^(2^k))` (binary digits 1 at
  positions 2, 4, 16, 256, 65536, ...). The bound of the dyadic cell `[l,u]`
  containing `z` is exactly `-(z-l)(u-z)`. Exact rational arithmetic
  ([`spatial-bb/bisection_checks.log`](spatial-bb/bisection_checks.log)) gives
  511, 513 and 513 nodes at `eps = 2^-511, 2^-600, 2^-1000`, against 511, 599
  and 999 for `z = 1/3`. The count stays at 513 until `eps` is about
  `2^-65792`, so `liminf |T_bis|/log(1/eps) = 0`. The correct condition: the
  lower bound `Omega(log(1/eps))` holds when, at a positive fraction of levels,
  some coordinate of the minimizer lies in the middle part `[delta, 1-delta]`
  of its dyadic cell. Examples are a rational coordinate with an odd
  denominator greater than 1, or almost every minimizer, since almost every
  number is normal. The upper bound `O(log(1/eps))` holds for every minimizer
  by Theorem A.
- **Low-rank row: only the lower bound is proved.** The cell "N_opt and
  bisection = the `k`-dimensional integral of `v`" also asserts an upper bound.
  That would need two-sided gaps, (QD) for `v`, and a node bound controlled by
  `v` on boxes `C_Y x Z0`. None of this is shown. Also, the value-function
  bound applies only when the other coordinates are never branched. Otherwise
  only the weaker slice bound `sup_z` holds.

## 7. McCormick example (3.7)

**Correct**, with one wording fix.
[`spatial-bb/mccormick_check.py`](spatial-bb/mccormick_check.py) uses its own
LP.

- On a 1201^2 grid, `f >= 0` and `min f/|x-a| = 1.4142 = 2 - max(b, 1-b)`, so
  the optimal set is the segment `x = a`.
- Both boxes of the 2-leaf certificate have bound exactly 0.
- At the point `X = 0`, `Y = ` midpoint, the McCormick envelope equals
  `-(w_y/2) min(X_u, |X_l|)`. With `a` at relative position 1/3 or 2/3, this is
  `-w_x w_y/6`. The script asserts `LP bound <= -w_x w_y/6` for every
  straddling box that widest-side bisection generates; all assertions pass.
- Node counts match the scout: 21, 61, 253, 765 and 2045 for
  `eps = 1e-2 ... 1e-6`. Counting only the boxes in the column that contains
  `x = a` gives a proved lower bound of 10, 30, 94, 382 and 1022, about
  `eps^(-1/2)`.

The lower bound `Omega(eps^(-1/2))` and the `O(1)` certificate are proved. The
matching upper bound `O(eps^(-1/2))` for widest-side bisection is numerical
only (`nodes * eps^(1/2)` is 1.9–2.5). The same holds for `Theta(log(1/eps))`
with branching on `x` only: the lower bound follows from the same envelope
evaluation, while the upper bound is numerical. Q2's "This is proved by the
example in Section 3.7 for `p = 1`" should say which parts are proved.

## 8. Computations

Commands run from `research-20260928b/reviews/spatial-bb/`, each logged next to
its script:

- `python3 thm_b_1d.py 40`: exact 1D minimum certificates against Theorem B,
  including the sawtooth and 40 random instances.
- `python3 amgm_constants.py`: AM–GM loss per box.
- `python3 bisection_checks.py`: Theorems A and C in 1D and on separable 2D
  instances, the (QD) counterexamples and the sparse-digit count.
- `python3 mccormick_check.py`: Section 3.7.
- `python3 obbt_2d.py`: Lemma 0 with iterated OBBT in 2D, per-round versus
  merged frames.
- `python3 fbbt_cutoff_1d.py`: objective-cutoff propagation on `nondeg1`.
- `python3 thm_d_constrained.py`: Theorem D on an equality-constrained
  instance.

These are floating-point illustrations. Only the sparse-digit count uses exact
arithmetic. They are not certified. No project-wide checks were run and CI was
not inspected.

## 9. Novelty assessment

### 9.1 Sources and access

The reviewer read the local full texts of Neumaier (2004) and Wechsung et al.
(2014). A delegated search covered the rest, and the reviewer spot-checked its
key quotations. WebSearch was out of quota. The arXiv API (16 queries) and
direct fetches of arXiv and NeurIPS pages worked. Several publishers blocked
access.

| Source | Access | Relevant content |
|---|---|---|
| Neumaier, Acta Numerica 13 (2004), Section 15 | local full text, read by reviewer | Heuristic **lower** count for fixed-width covers. "any covering by boxes of diameter ε contains at least const √((2∆)^n)/(ε^n √det G) boxes", with bounding accuracy `∆ = K eps^(s+1)`. For `s = 1` the count is independent of `eps` but "may still grow exponentially with the dimension". Under active constraints "n must be replaced by n − a". On non-isolated solution sets "some clustering seems unavoidable". |
| Wechsung, Schaber, Barton, JOGO (2014) | local full text, read by reviewer | Section 2.1 refines Neumaier's argument and says it bounds the number of boxes "from below". The count is for fixed width `delta`, assumes a sharp bounding error, and places the minimizer at a box centre. Its covering results are upper bounds. |
| Du–Kearfott (1994); Kannan–Barton (2017, 2018) | local full texts (agent) | Upper or conservative worst-case counts only. Du–Kearfott Remark 1: "an upper bound, and not a precise value". |
| Hansen, Jaumard, Lu, Math. Oper. Res. 16 (1991) | abstract only | In 1D and Lipschitz, Piyavskii's algorithm satisfies `n_P <= 2 n_B + 1` (sharp) against the best possible certificate `n_B`. "Lower and upper bounds on n_B are obtained as functions of f(x), ε, L0, and L1." The form of the lower bound was not seen. |
| Bachoc, Cesari, Gerchinovitz, NeurIPS 2021, arXiv:2102.01977 v5 | full text (agent) | Lipschitz and black box. The certified sample complexity is within constants and logs of `integral (f(x*) - f(x) + eps)^(-d)`. The upper bound comes from c.DOO and packing layers (Proposition 1, Theorem 1). The lower bound (Theorem 2) uses a local adversary and loses `1/(1 + m_eps)`, a log factor. Theorem 3 compares c.DOO with the best algorithm. Nothing on second-order smoothness, relaxations, constraints or branch-and-bound. |
| Bouttier, Cesari, Ducoffe, Gerchinovitz, arXiv:2002.02390 | full text (agent) | Packing bounds for Piyavskii–Shubert. It reports that Perevozchikov (1990) proved a DOO-like branch-and-bound bound under a volume assumption on the near-optimal sets. |
| de Montbrun, Gerchinovitz, arXiv:2308.00978 (JUQ 2024) | full text (agent) | Multi-fidelity version of Bachoc's lower bound, keeping the log factor. Tailoring to smooth functions is left "for future work". |
| Munos, NIPS 2011 | full text (agent) | Near-optimality dimension and the DOO level-by-level count under a semi-metric `‖x-y‖^beta`. With `beta = 2`, the example `1 - ‖x‖_inf^alpha` gives the exponent `n/2 - n/alpha`, as in the growth row of 3.6. No certificates and no lower bounds. |
| Dym, arXiv:2005.13728 | full text (agent) | No iteration counts and no lower bounds. Notes finite termination of alphaBB with box-dependent alpha at nondegenerate minima. |
| Cartis, Fowkes, Gould, JOGO 61 (2015) | preprint full text (agent) | No node counts. |
| Schöbel, Scholz, JOGO 48 (2010); Csendes, Ratz (1997) | abstract only | No counts in the abstracts. Secondary sources describe Schöbel–Scholz as a very conservative upper bound. |

### 9.2 Corrections to the scout's framing

- "The cluster literature gives only upper estimates" and the repository
  screen's "No lower bounds on node counts exist in this literature" are
  inaccurate. Neumaier gives a heuristic lower count, and Wechsung et al. call
  it one. The defensible claim is narrower: no *rigorous* lower bound was found
  for *adaptive* trees with arbitrary box shapes summed over all scales.
- Row 1 of the 3.6 table is the rigorous, all-scales form of Neumaier's
  heuristic. His `(const^n/det G)^(1/2)` prefactor at `s = 1` is the
  `(c alpha/gamma)^(n/2)` factor. Neumaier's `n - a` remark anticipates the
  dimension drop in Theorem D.
- Hansen–Jaumard–Lu are not "known only through Bachoc". Their abstract
  already compares an algorithm with the best possible certificate and bounds
  that certificate below, in 1D.
- The report presents Bachoc et al.'s log loss as a contrast with Theorem B.
  Section 9.3 shows that this contrast comes from the proof method, not from
  the setting.

### 9.3 A log-free Lipschitz lower bound by the same covering argument

The delegated search proposed the following derivation. The reviewer checked
each step. It was not compared against the full text of Hansen–Jaumard–Lu or
any later paper.

1. Take the maximization setting of Bachoc et al.
   - A deterministic algorithm must output a certificate `xi_n` that holds
     for every `L`-Lipschitz function consistent with its observations.
   - Suppose it stops with `xi_n <= eps` after queries `x_1..x_n` and
     recommendation `x_hat`.
2. The upper envelope `U(x) = min_i (f(x_i) + L|x-x_i|)` is `L`-Lipschitz and
   consistent with the observations. So is
   `g = min(U, D + L|x - x_hat|)`, where `D` is the lower envelope at `x_hat`.
   Validity for `g` gives the following for every `x`:
   - either `|x - x_hat| <= eps/L`;
   - or there is an `i` with `|x - x_i| <= r_i := (f* + eps - f(x_i))/L`.
3. On `B(x_i, r_i)`, the Lipschitz bound on `f` gives
   `f* - f + eps >= (L - Lip f) r_i`. The same holds on `B(x_hat, eps/L)`,
   with `eps/L` in place of `r_i`.
4. So each of the `n+1` balls contributes at most
   `vol(B_1)/(L - Lip f)^d` to `integral (f* - f + eps)^(-d)`.

**Result:**
`n + 1 >= (L - Lip f)^d / vol(B_1) * integral_X (f* - f + eps)^(-d) dx`.
There is no log factor and no assumption on `X`. The factor
`(1 - Lip f/L)^d` matches theirs.

If this is right, two things follow. First, the scout's Theorem B is the same
per-cell covering argument, with an axis-parallel box and the gap
`alpha q_C` in place of a ball and a Lipschitz cone. Second, the absence of a
log factor is not an advantage of the quadratic-gap setting. What is specific
is the per-box constant. `alpha q_C` vanishes on the whole boundary of `C`, so
bounding the per-box integral uniformly over all box shapes needs the AM–GM
and arcsine computation.

### 9.4 Assessment by claim

- **Theorem B.** Per-cell covering, as in the Lipschitz certificate
  literature (Hansen–Jaumard–Lu in 1D; Section 9.3), plus a new per-box
  computation. Neumaier's heuristic is the closest MINLP precedent. No
  rigorous statement for relaxation-based spatial branch-and-bound was found.
  Originality: modest; the transfer is natural.
- **Theorem D.** A standard packing lower bound. The specific step is that
  near-optimal points must sit near box vertices. Neumaier notes the dimension
  drop heuristically. Originality: low to modest.
- **Theorem A.** The same form as Hansen–Jaumard–Lu's `n_P <= 2 n_B + 1` and
  Bachoc et al.'s Theorem 3: a fixed partition rule against the best
  certificate. The vertex-charging proof and the attained log factor under a
  vertex-exact relaxation were not found elsewhere. Bachoc et al.'s
  Proposition 3 (Piyavskii–Shubert certifies `L‖x‖` in 2 queries) is a related
  sharp-minimum phenomenon. Originality: modest.
- **Theorem C.** The Perevozchikov and Munos level-by-level count, converted to
  an integral as in Bachoc et al.'s Theorem 1. (QD) plays the role that the
  Lipschitz condition plays there. Originality: low.
- **Lemma 0 and the bound-tightening corollary.** No precedent was found; the
  cluster papers and Puranik–Sahinidis have no theorem relating tightening to
  node counts. The argument is short and, as Section 1.3 shows, limited to
  same-relaxation tightening. Originality: modest.
- **Vertex-exact examples (3.4 tightness, 3.7).** No precedent was found. They
  are a useful counterpoint to the view of Wechsung et al. and Kannan–Barton
  that vertex placement of a minimizer is the bad case.

Overall, this supports the scout's own "moderate originality" risk, but on the
low side for Theorems C and D. The claim "the first lower bounds on total tree
size for adaptive spatial branch-and-bound" should read "the first rigorous
lower bounds for relaxation-based spatial branch-and-bound with adaptive trees,
as far as the bounded search found". It should cite Neumaier as the heuristic
precedent and Hansen–Jaumard–Lu and Bachoc et al. as the Lipschitz precedents.

### 9.5 Not checked

- The full texts of Hansen–Jaumard–Lu (the form of their lower bound on
  `n_B`) and Schöbel–Scholz.
- Ratschek–Rokne, Kearfott (1996), Kearfott–Du (1993, univariate), Munos
  (2014), Danilin (1971), Perevozchikov (1990) and Sukharev.
- Whether any paper after 2021 already removes the log factor from Bachoc et
  al.'s lower bound.
- General web search was unavailable. An unsuccessful search does not
  establish novelty. The interval-analysis box-count literature remains the
  most likely place for close prior work.

## 10. What remains unchecked

- The constant of the bounded-aspect-ratio stratum case was not computed
  explicitly.
- The scout's 2D non-separable runs (ring, 2D nondegenerate) were not re-run.
  Separable 2D instances were re-run with independent code and show the same
  behaviour.
- Whether `N_opt` loses the AM–GM factor for `n >= 2` on some instance.
- The open questions Q1–Q3 and the conjectures under Q2 were not reviewed.
- Literature items that could not be accessed are listed in Section 9.
