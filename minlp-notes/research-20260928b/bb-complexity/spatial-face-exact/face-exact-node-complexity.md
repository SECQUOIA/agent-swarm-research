# Node complexity of spatial branch-and-bound with face-exact relaxations

Workstream `spatial-face-exact/` of the
[branch-and-bound complexity program](../PROGRAM.md). Date: 2026-09-28.
Status: first-pass results, not independently reviewed. Scripts and logs are
in this directory. Starting points: Q2 and Section 3.7 of the
[spatial scout report](../../scouting/spatial-bb-theory.md) and the
[spatial review](../../reviews/spatial-bb-review.md).

## Summary

*Revised 2026-09-29 after an independent review
([`../../reviews/face-exact-review.md`](../../reviews/face-exact-review.md)),
and again after a recheck
([`../../reviews/face-exact-recheck.md`](../../reviews/face-exact-recheck.md)).
Section 11 lists every change.*

The scout's lower bounds for spatial branch-and-bound assume an alphaBB-type
gap, `gap >= alpha * sum_i (y_i - l_i)(u_i - y_i)`, which vanishes only at box
vertices. McCormick envelopes of bilinear terms, and vertex-polyhedral
envelopes of multilinear terms, vanish on whole box faces. This note develops
a node-count theory for these relaxations. The three questions have the
following answers.

**Q1 (lower bounds and the right invariant).**

- The relevant geometry is the zero set of the gap. For termwise McCormick it
  is the set of box faces on which the fixed coordinates form a vertex cover of
  the bilinear interaction graph `G` (Lemma 2.2).
- A stratum of near-optimal points is *transversal* if no tangent vector lies
  in a coordinate subspace `span(e_I)` with `I` independent in `G`
  (Definition 2.7). This refines the scout's "transversal to all coordinate
  hyperplanes".
- Transversal `p`-dimensional strata force `Omega(eps^(-p/2))` leaves
  (Theorems 3.6 and 3.8). This proves the scout's conjecture in the refined
  form. For flat strata the constant is explicit, and on the tilted-stratum
  instance it is sharp: `N_opt = (1/2) sqrt(theta/eps) + O(1)`
  (Proposition 3.13).
- For flat strata a weaker sufficient condition is a constant
  `tau(V, G) > 0` (gap-nondegeneracy, Definition 2.8). Transversality implies
  it, and for `p = 1` the two coincide. A non-transversal optimal plane with
  `tau = 1/sqrt(2)` costs `Theta(1/eps)` leaves (Proposition 4.7).
- `tau` does not decide the exponent. Aligned strata (`tau = 0`) cost `O(1)`
  in Theorem 4.4 but `Theta(eps^(-1/2))` in Example 3.12(b).
- Curved, non-transversal near-optimal surfaces escape all of these tools. In
  the recheck's example (Proposition 3.14), a row-slice argument gives
  `N_cov >= 0.307/(eps (1 + ln(1/(2 eps))))`, while Theorems 3.4, 3.6 and 3.8
  and Proposition 3.10 give only `O(eps^(-3/4))`. So no characterization by
  those bounds holds: Conjectures 7.1 and 7.1' are withdrawn.
- The alphaBB certificate integral fails for McCormick. The per-box integral
  of `gap^(-s)` is finite only for `s < 1`, where it equals
  `|c|^(-s) (w_x w_y)^(1-s) * 2 Gamma(1-s)^2 / Gamma(3-2s)` (Lemma 3.1). The
  resulting "McCormick certificate integral" (Theorem 3.2) has exponent
  `s < k` for a matching of size `k`. It is within `log^(2k)(1/eps)` of the
  natural exponent `k`. On sharp instances one log factor of loss is
  unavoidable.
- Concave directions of the bilinear part carry alphaBB-type chord gaps
  (Lemma 2.4). Slices along matched concave directions give integral lower
  bounds, including `Omega(log(1/eps))` at every smooth interior minimizer
  with an active bilinear term (Theorem 3.4, Corollary 3.5).
- A cube of side `W` on which `m <= eta` costs at least
  `(alpha W^2/(4(eps + eta)))^(tau*(G))` leaves, where `tau*` is the fractional
  vertex cover number (Proposition 3.10, Corollary 3.11). The exponent is
  attained. For alphaBB it is `n/2`. `tau*(G) <= n/2`, with equality iff `G`
  has a fractional perfect matching.
- **Structure of optimal sets (Section 4).** Take `f = g + phi` with `g`
  convex and `phi` bilinear. A convex function that is affine on a segment has
  constant directional derivatives along it (Lemma 4.1, a standard fact).
  Consequences:
  - Optimal segments lie in concave-or-flat directions of `phi`
    (Theorem 4.2).
  - For smooth `g`, interior optimal strata are transversal under a rank
    condition (Corollary 4.3).
  - Along an aligned stratum the transverse growth rates are affine. In 2D,
    a full aligned optimal segment always admits an exact 2-box certificate,
    for every convex `g`, because sharpness is forced (Theorem 4.4).
  - The same holds in `n` dimensions when the fixed coordinates form an
    independent vertex cover in which each other variable has at most one
    neighbour (Theorem 4.5). This condition cannot be dropped
    (Proposition 4.7).
  - In three or more dimensions an aligned stratum can have quadratic
    transverse growth and cost `Omega(eps^(-1/2))`, even with box constraints
    only (Example 3.12(b), found by the review).
  - For `F = X0`, an exact finite certificate exists iff `N_opt` stays
    bounded. No such certificate exists at any minimizer where `m` grows
    sublinearly along a feasible concave direction (Proposition 4.6).

  So the scout's "axis-aligned strata have `O(1)` certificates" is true in 2D,
  where the needed sharpness comes for free. It is false in general.

**Q2 (branching points and rules).**

- *Bisection.* For any second-order scheme, widest-side bisection is
  `O(integral (m+eps)^(-n/2))` under quadratic doubling. It is
  `O(eps^(-p/2))` at sharp `p`-dimensional strata (Theorem 5.1). The same
  holds within constants for every balanced widest-side rule
  (Proposition 5.2). So on smooth instances whose optimal sets are
  transversal Morse–Bott strata, bisection is within a constant factor of
  optimal.
- *Oblivious rules.* The loss is polynomial for every oblivious rule, that is,
  every rule whose split tree does not depend on the instance. On the
  aligned-kink family, where `N_opt = 2`, the expected counts over a random
  vertical kink and a random horizontal kink sum to at least
  `beta sqrt(|c|/(8 eps))` (Theorem 5.3).
- *Rules that use the relaxation solution or the incumbent* (Section 5.3).
  - Splitting exactly at the relaxation point, with no clamp, takes 3 nodes
    on the kink family (Proposition 5.4(b)).
  - Practical codes keep the split point away from the bounds. With SCIP's
    clamp 0.2 (SCIP with `branching/midpull = 0`) the count is bounded for
    every `a` outside a Cantor set of measure zero, but it is unbounded near
    that set (Proposition 5.4(c)). On the set the split never reaches the
    optimal face. For `a = 1/6` widest-side selection then needs at least
    `0.0745 eps^(-1/2)` nodes (Proposition 5.5, from the review).
  - Branching at an optimal incumbent places the face exactly. On the kink
    family it takes 3 nodes with width ties broken toward `x`
    (Proposition 5.4(d)). This is the finite branching scheme of
    Shectman–Sahinidis, which BARON adopts, and it is the solver mechanism
    that realizes the `O(1)` certificates there. It places the face only in
    nodes that contain the incumbent, so the tie rule and the incumbent's
    position matter (remark after Proposition 5.4).
  - A fixed midpoint weight `alpha < 1`, such as Couenne's documented 0.25,
    splits at the optimal face for at most countably many `a`
    (Proposition 5.6). The count is then `O(log(1/eps))` if the right variable
    is always chosen, and about `eps^(-1/2)` with widest-side selection.
  - SCIP 10's default weight depends on the box (midpull 0.75, scaled below
    relative width 0.5). Proposition 5.6 does not cover it. Numerically it
    lies between the two regimes.
  - Strong branching with the min-child score and Couenne-type points
    provably needs at least `0.0287/eps - 1` nodes on the scout's instance,
    which is worse than bisection, while `N_opt = 2` (Proposition 5.7). The
    product score avoids this.
- *Open.*
  - No rule is known to be within `polylog(1/eps)` of `N_opt` on all
    instances.
  - Conjecture 5.8, which proposed the clamped relaxation point with
    widest-side selection, is false (Proposition 5.5).
  - The relaxation point with product-score strong branching stayed within a
    factor 2.6 of `N_opt` on all tilted instances and was logarithmic for
    `a = 1/6` (Question 5.9).

**Q3 (convergence order).** McCormick and alphaBB both have second-order
pointwise convergence (Bompadre–Mitsos), and in the kink example they have the
same prefactor. On that instance, `N_opt` is 2 for McCormick and
`Theta(eps^(-1/2))` for alphaBB. A *first-order* face-exact scheme also has
`N_opt = 2` (Theorem 6.1). That first-order schemes can suffice at
nondifferentiable minimizers was already observed in Wechsung's thesis, as
Kannan–Barton report. The new part is the comparison at equal order and
prefactor. Convergence order controls only the upper bound (Theorem 5.1).
Lower bounds are set by where the gap vanishes relative to the near-optimal
set, together with the transverse growth of `m`.

**Computations.** A toy branch-and-bound with exact LP/QP node bounds (HiGHS,
with a Clarabel fallback) tests every claim on 2D/3D face-exact instances,
Haverly pooling problems and random box QPs. They support every proved bound
and rate, and they are commands and logs, not certified counts (Section 8).
The revision reruns are recorded in Section 8.4.

## 1. Model

### 1.1 Problems and relaxations

- Root box `X0 = prod_i [L_i, U_i]`. For a box `B = prod_i [l_i, u_i]` and
  `x in B`, write:
  - `delta_i^-(x) = x_i - l_i` and `delta_i^+(x) = u_i - x_i`;
  - `d_i(x) = min(delta_i^-, delta_i^+)` and `w_i = u_i - l_i`;
  - `a_i = delta_i^- delta_i^+` and `q_B = sum_i a_i`.
- Problem `(P)`: minimize `f = g + phi` over `F = X0 ∩ Q`, where:
  - `g` is convex and continuous on `X0`;
  - `phi` is multilinear, `phi(x) = sum_S c_S prod_{i in S} x_i`;
  - `Q` is a polyhedron in `x`-space.

  So only the objective is nonconvex. `f*` is the optimal value and
  `m = f - f*`.
- The main case is bilinear: `phi = sum_{i<j} c_ij x_i x_j`, with
  interaction graph `G = {ij : c_ij != 0}` and Hessian `C = grad^2 phi`.
  Concave diagonal terms relaxed by secants behave like alphaBB terms in their
  own coordinate and are not the subject here.
- Node relaxation on `B`: `f_B = g + psi_B`, where either:
  - **(T)** termwise: `psi_B = sum_S vex_B(c_S x^S)` (for bilinear terms this
    is McCormick, which is the convex envelope of `c_ij x_i x_j` on the
    `(i,j)` face box); or
  - **(J)** joint: `psi_B = vex_B(phi)`.

  In both cases `psi_B <= phi` on `B`.
- The gap is `Gamma_B = f - f_B = phi - psi_B >= 0`. Termwise gaps dominate
  joint ones: `Gamma^T_B >= Gamma^J_B`, because a sum of envelopes lies below
  the envelope of the sum.
- Node bound: `LB(B) = min {f_B(x) : x in B ∩ Q}`. In lifted form this is the
  LP or convex program with one variable `w_S` per term, constrained to the
  convex hull of the term's graph over `B`. The projection onto `x` gives
  `f_B`: minimizing `c_S w_S` over the hull fiber gives `vex_B(c_S x^S)`.
- **Monotonicity.** If `B' ⊆ B`, then `psi_B <= psi_B'` on `B'`. So
  `Gamma_B' <= Gamma_B` on `B'` and `LB(B) <= LB(B')`.

### 1.2 Trees, certificates and the pruning criterion

A branch-and-bound run:

- splits boxes by axis-parallel hyperplanes at arbitrary points;
- processes nodes in any order;
- uses an incumbent `UBD >= f*`;
- prunes `B` when `LB(B) >= UBD - eps`, or when `B ∩ Q` is empty.

Relative gaps reduce to this form (spatial review, Section 1.1). A box `C` is
**valid** at tolerance `eps` if `Gamma_C(x) <= m(x) + eps` for all
`x in C ∩ F`. A **valid cover** is a finite family of valid boxes covering
`X0`.

- `N_opt(eps)` is the minimum number of leaves of a tree whose leaves are all
  pruned with `UBD = f*`. Equivalently, it is the minimum size of a guillotine
  partition of `X0` into valid boxes.
- `N_cov(eps) <= N_opt(eps)` is the minimum size of an arbitrary valid cover.
- All lower bounds below bound `N_cov`, so they bound `N_opt` and every tree.
  A binary tree with `N` leaves has `2N - 1` nodes.

**Lemma 1.1 (pruning criterion).** With `UBD = f*`, a box `C` is pruned iff it
is valid. For any `UBD >= f*`, pruned boxes are valid.

*Proof.* `LB(C) = min_{C ∩ F} (f - Gamma_C)`. So
`LB(C) >= f* - eps` iff `Gamma_C <= m + eps` on `C ∩ F`. If `UBD >= f*`, then
`LB >= UBD - eps` implies `LB >= f* - eps`. □

**Lemma 1.2 (which bound tightening the lower bounds cover).** Consider a run
that also uses:

- (i) reduction that removes only points outside `Q`, such as FBBT on the
  linear constraints; and
- (ii) OBBT or reduced-cost tightening computed from the node relaxation
  `f_B` with cutoff `UBD` or `UBD - eps`.

Decompose each reduction *round* into at most `2n` boxes (spatial review,
Fix 1). Then the leaves together with the removed pieces form a valid cover.

*Proof.*

- A piece of type (i) contains no point of `F`, so it is valid vacuously.
- Let `S` be a piece of type (ii), removed from box `B_k` in round `k`, and
  let `x in S ∩ F`. Then `f_{B_k}(x) > UBD - eps >= f* - eps`, so
  `Gamma_{B_k}(x) < m(x) + eps`.
- Since `S ⊆ B_k`, monotonicity gives `Gamma_S(x) <= Gamma_{B_k}(x)`. □

*Also covered:* any node relaxation that lies pointwise below termwise
McCormick on the node box. Examples are gradient outer approximation of `g`
and McCormick cuts inherited from ancestors without re-separation. Such a
relaxation has a larger gap, so validity is harder and every lower bound
still holds.

*Not covered:*

- objective-cutoff propagation, that is, interval FBBT of `f <= UBD - eps` on
  the expression graph. It uses information other than the relaxation and can
  empty whole boxes (spatial review, Fix 2);
- cutting planes beyond the envelopes (RLT, SDP, and so on). These matter:
  one RLT product removes Example 3.12(a) at the root;
- relaxations that are pointwise stronger than termwise McCormick;
- constraints that involve lifted variables, such as the pooling bilinear
  equalities. There, validity at feasible points is not necessary for
  pruning, because the envelope point `(x, w)` may violate the relaxed
  constraints;
- bounds taken from children. When strong branching or probing assigns a
  parent the minimum of its children's bounds, the children must be counted
  as the leaves;
- branching on auxiliary (lifted) variables;
- incumbents accepted within a feasibility tolerance, which can have
  `UBD < f*`. Then `f*` must be read as the optimal value of the
  tolerance-relaxed problem.

The pooling runs in Section 8 are therefore illustrations only.

## 2. Gap geometry

**Lemma 2.1 (McCormick gap).** Let `phi = c x_i x_j` on a box `B`.

- (a) Exact gap. If `c > 0`, then
  `Gamma = c min(delta_i^- delta_j^-, delta_i^+ delta_j^+)`. If `c < 0`, then
  `Gamma = |c| min(delta_i^- delta_j^+, delta_i^+ delta_j^-)`.
- (b) `Gamma(x) = 0` iff `x_i in {l_i, u_i}` or `x_j in {l_j, u_j}`.
- (c) `|c| d_i d_j <= Gamma <= |c| min(d_i w_j, d_j w_i)`.
- (d) `Gamma <= (|c|/2)(a_i + a_j)`, and `sup_B Gamma = |c| w_i w_j / 4`,
  attained at the center.

*Proof.*

- (a) The convex envelope of `x_i x_j` on a rectangle is the maximum of the
  two McCormick underestimators, and the concave envelope is the minimum of
  the two overestimators (McCormick 1976; Al-Khayyal–Falk 1983). The gap
  formulas follow from
  `x_i x_j - (l_j x_i + l_i x_j - l_i l_j) = delta_i^- delta_j^-` and its
  three analogues.
- (b) This is read off from (a).
- (c) Each `delta >= d`, which gives the lower bound. For the upper bound in
  case `c > 0`: if `d_i = delta_i^-`, then
  `Gamma <= c delta_i^- delta_j^- <= c d_i w_j`; if `d_i = delta_i^+`, use the
  second product. The case `c < 0` is the same.
- (d) `min(p, q) <= (pq)^(1/2)`. The product of the two terms in (a) is
  `a_i a_j`, and `(a_i a_j)^(1/2) <= (a_i + a_j)/2`. Each term is maximized at
  the center. □

**Lemma 2.2 (faces and zero sets).**

- (a) For a polytope `B`, a face `Fc` of `B`, and continuous `phi`:
  `vex_B(phi)|_Fc = vex_Fc(phi|_Fc)`. Hence `Gamma^J_B ≡ 0` on `Fc` iff
  `phi|_Fc` is convex. For multilinear `phi` this holds iff `phi|_Fc` is
  affine, that is, iff `∂_ij phi ≡ 0` on `Fc` for every pair `i, j` of free
  coordinates of `Fc`.
- (b) For termwise bilinear relaxations, `Gamma^T_B(x) = 0` iff
  `{i : x_i in {l_i, u_i}}` is a vertex cover of `G`.

*Proof.*

- (a) The envelope is the infimum of `sum lambda_k phi(x_k)` over
  representations `x = sum lambda_k x_k` with `x_k in B` and `lambda_k > 0`.
  If `x in Fc`, every such `x_k` lies in `Fc`, by the definition of a face.
- A multilinear function whose restriction to the `(i,j)` coordinate plane
  has a nonzero coefficient on `x_i x_j` is not convex along `e_i ± e_j`.
- (b) Sum Lemma 2.1(b) over the edges. □

**Lemma 2.3 (mixed-partial lower bound).** Let `phi` be multilinear, `B` a
box and `x in B`. For all `i != j`,
`vex_B(phi)(x) <= phi(x) - |∂_ij phi(x)| d_i(x) d_j(x)`. Hence
`Gamma^J_B(x) >= max_{i<j} |∂_ij phi(x)| d_i d_j`. For termwise relaxations
the corresponding sum over monomials holds.

*Proof.*

- Let `D = ∂_ij phi(x)` and `s = sign(D)`. With the other coordinates fixed,
  `phi(x + t_i e_i + t_j e_j) = phi(x) + beta_i t_i + beta_j t_j + D t_i t_j`,
  because `phi` is affine in each of `x_i`, `x_j`, and `D` does not depend on
  them.
- The points `x ± (d_i e_i - s d_j e_j)` lie in `B` and average to `x`.
- Averaged over the two points, `phi` equals `phi(x) - |D| d_i d_j`.
- Convexity and `vex <= phi` give
  `vex_B(phi)(x) <= average of vex_B(phi) <= average of phi`. □

**Lemma 2.4 (chord bound).** Let `x in B` and a direction `v`, and let the
chord be `B ∩ (x + R v) = {x + t v : t in [t_-, t_+]}` with `t_- <= 0 <= t_+`.

- `vex_B(phi)(x)` is at most the envelope of `t -> phi(x + t v)` over
  `[t_-, t_+]`, evaluated at `0`.
- If `phi(x + t v) = phi(x) + beta t - kappa t^2` with `kappa > 0`, then
  `Gamma^J_B(x) >= kappa (-t_-) t_+`.
- For multilinear `phi` and `v = e_i - s e_j` with
  `s = sign(∂_ij phi(x))`, this holds with `kappa = |∂_ij phi(x)|`, and
  `kappa` is constant along the whole line.
- For a bilinear term `c x_i x_j` and any direction with `c v_i v_j < 0`, the
  term alone satisfies this with `kappa = |c v_i v_j|`. Hence the termwise gap
  obeys the same bound.

*Proof.* The chord lies in `B`, so combinations along the chord are allowed
in the envelope. A concave quadratic on an interval has as its envelope the
chord, and the chord gap at `0` is `kappa (-t_-) t_+`. Along `e_i - s e_j` the
multilinear `phi` is exactly quadratic with leading coefficient
`-s ∂_ij phi = -|∂_ij phi|`, and `∂_ij phi` does not depend on `x_i, x_j`. □

So in concave directions McCormick gaps are alphaBB gaps along chords. In
directions with `c v_i v_j > 0` only `min(t, L-t)^2` remains, which follows
from Lemma 2.1(c) along the chord.

**Lemma 2.5 (upper bounds; second-order convergence).**

- Termwise bilinear: `Gamma^T_B <= alpha'_T q_B` with
  `alpha'_T = max_i sum_{j ~ i} |c_ij|/2`, and
  `sup_B Gamma^T_B = sum_{ij in G} |c_ij| w_i w_j / 4`.
- Joint envelope of a `C^2` function `phi`: `Gamma^J_B <= alpha' q_B` with
  `alpha' = max(0, -min_B lambda_min(grad^2 phi))/2`.

*Proof.* The first claim is Lemma 2.1(d) summed over edges. For the second,
the alphaBB function `phi - alpha' q_B` is a convex underestimator, so it lies
below the envelope. □

So both relaxations satisfy the upper gap hypothesis of the scout's
Theorems A and C and are second-order convergent in the Bompadre–Mitsos
sense. They fail the *lower* hypothesis `(G_alpha)`.

**Definition 2.6 (gap graph).** For a set `S` and `alpha > 0`, let
`E_alpha(S)` be the set of pairs `ij` with `|∂_ij phi| >= alpha` on `S` for
(J), or `|c_ij| >= alpha` for (T). By Lemmas 2.1 and 2.3, on every box `C`
and at every `x in S ∩ C`:

```
Gamma_C(x) >= alpha * max_{ij in E_alpha} d_i^C(x) d_j^C(x).          (2.1)
```

**Definition 2.7 (transversality).** A subspace `T` is *transversal* for a
graph `E` if `T ∩ span{e_i : i in I} = {0}` for every set `I` that is
independent in `E`. Equivalently, for every vertex cover `K`, the coordinate
projection `pi_K` is injective on `T`. A stratum is transversal if its tangent
spaces are. A stratum is *aligned* if its tangent spaces meet some
`span(e_I)` with `I` independent.

- For a single edge `{x, y}` in `R^2`, the independent sets are `{x}` and
  `{y}`. Transversal therefore means "not axis-parallel".
- With an isolated coordinate `z`, a direction along `e_z` is aligned, even
  though it is transversal to the hyperplanes `x = const` and `y = const`.
  This is why the scout's notion "transversal to all coordinate hyperplanes"
  has to be refined.

**Definition 2.8 (gap-nondegenerate flats).** A `p`-dimensional subspace
`span(V)` is *gap-nondegenerate* for `E` if the constant `tau(V, E)` of
Theorem 3.6 is positive.

- Transversal subspaces are gap-nondegenerate (Lemma 3.7(a,b)).
- For `p = 1` the two notions coincide.
- For `p >= 2`, gap-nondegeneracy is strictly weaker. This matters: the
  non-transversal but gap-nondegenerate plane of Proposition 4.7 costs
  `Theta(1/eps)` leaves.

## 3. Lower bounds

### 3.1 The certificate integral for product-form gaps

The scout's Theorem B bounds `integral_C q_C^(-n/2)` by a constant that does
not depend on the box `C`, using AM–GM and the arcsine integral. The analogue
for a McCormick gap behaves differently.

**Lemma 3.1 (per-box integral).** Let `c x_i x_j` be a bilinear term on a box
`R = [l_i, u_i] x [l_j, u_j]` with gap `Gamma` (Lemma 2.1(a)), and let
`sigma > 0`. Then

```
integral_R Gamma^(-sigma) = |c|^(-sigma) (w_i w_j)^(1 - sigma) J(sigma),
J(sigma) = 2 Gamma(1-sigma)^2 / Gamma(3 - 2 sigma)   for sigma < 1,
```

and the integral is infinite for `sigma >= 1`. In particular:

- `J(1/2) = 2 pi`;
- `J(sigma) <= 2.3/(1-sigma)^2`;
- `J(sigma) ~ 2/(1-sigma)^2` as `sigma -> 1`.

*Proof.*

1. Take `c > 0`; for `c < 0` reflect one coordinate. Substitute
   `x_i = l_i + w_i xi` and `x_j = l_j + w_j eta`. Then
   `Gamma = c w_i w_j min(xi eta, (1-xi)(1-eta))`.
2. The two products are exchanged by `(xi, eta) -> (1-xi, 1-eta)`.
3. `xi eta <= (1-xi)(1-eta)` iff `xi + eta <= 1`. Hence
   `J(sigma) = 2 integral_{xi+eta<=1} (xi eta)^(-sigma)`, a Dirichlet integral
   equal to `2 Gamma(1-sigma)^2/Gamma(3-2sigma)` for `sigma < 1`.
4. For `sigma >= 1` the integral diverges at `xi = 0`.
5. Bounds: `Gamma(1-sigma) = Gamma(2-sigma)/(1-sigma)` with
   `Gamma(2-sigma) <= 1`, and `Gamma(3-2sigma) >= 0.8856` on `[1, 3]`. □

The scale-free exponent is `sigma = 1`. There the integral diverges
logarithmically near the "second-order" corners, where the gap is the product
`delta delta`. So no box-independent constant exists. The fix is to use
exponents below the natural one:

**Theorem 3.2 (McCormick certificate integral).** Assume a termwise bilinear
relaxation. Let `M = {e_1, ..., e_k}` be a matching in `G`, with
`e_r = {i_r, j_r}` and coefficients `c_r`. Let `V_M` be its `2k` coordinates
and `Z` the remaining coordinates. Fix `z` in the projection of `X0` onto `Z`,
and write `W_r = (U_{i_r} - L_{i_r})(U_{j_r} - L_{j_r})`. Then for every
`s in (0, k)`,

```
N_cov(eps) >= k^s (prod_r |c_r|)^(s/k) J(s/k)^(-k) (prod_r W_r)^(-(1 - s/k))
              * integral_{F_z} (m + eps)^(-s) dx_{V_M},
```

where `F_z = {x_{V_M} : (x_{V_M}, z) in F}`.

*Proof.*

1. Let `C` be in a valid cover. At `x in C ∩ F` with `x_Z = z`,
   `m + eps >= Gamma_C >= sum_r Gamma_r`. Here `Gamma_r` is the gap of term
   `e_r`, which depends only on `(x_{i_r}, x_{j_r})` and the bounds of `C` in
   these coordinates.
2. AM–GM gives `sum_r Gamma_r >= k (prod_r Gamma_r)^(1/k)`, so
   `(m + eps)^(-s) <= k^(-s) prod_r Gamma_r^(-s/k)`.
3. The slice of `C` is a product of the `k` rectangles `R_r`. By Lemma 3.1,
   the integral of the right side over the slice is
   `k^(-s) prod_r |c_r|^(-s/k) (w w)_r^(1 - s/k) J(s/k)`.
4. Bound `(w w)_r` by `W_r` and sum over `C`. The slices of the cover boxes
   cover `F_z`. □

**Corollary 3.3.**

- (a) For `eps <= e^(-2)` and `s = k(1 - 1/log(1/eps))`,
  `N_cov >= c * log(1/eps)^(-2k) * integral_{F_z} (m+eps)^(-k)`. The constant
  `c > 0` depends only on `k`, the `|c_r|` and the `W_r`. So the natural
  integral with exponent `k` (which is `n/2` for a perfect matching) is a
  lower bound up to `log^(2k)`.

  *Derivation.* Use `(m + eps)^(k/log(1/eps)) >= eps^(k/log(1/eps)) = e^(-k)`
  and `J(1 - 1/log(1/eps)) <= 2.3 log(1/eps)^2`.
- (b) Some loss is unavoidable in general. On the scout's kink instance,
  Section 3.7 of the scout report,
  `f = 2|x-a| - (x-a)(y-b)` on `[0,1]^2` with `a = 1/3` and
  `b = sqrt(2) - 1`. Here `N_opt = 2` for all `eps` (Theorem 4.4), while
  `integral (m + eps)^(-1) >= (2/2.6) log(1/eps) - O(1)`, because
  `m <= 2.6|x - a|`.

  This example is sharp, so it violates the quadratic-doubling condition
  (QD) of Theorem 5.1(a). Two questions are open:
  - whether any log loss is needed for (QD) instances, where Theorem 5.1(a)
    gives an upper bound of the same integral form;
  - the gap between the proved loss `log^(2k)` and the one log shown
    necessary.

### 3.2 Concave slices

**Theorem 3.4 (matching slices).** Assume a termwise bilinear relaxation and
a matching `M` as in Theorem 3.2. Let `v_r = e_{i_r} - sign(c_r) e_{j_r}`, and
for `z in R^n` let `V t = sum_r t_r v_r`. Then

```
N_cov(eps) >= (k/pi^2)^(k/2) (prod_r |c_r|)^(1/2)
              * integral_{T_z} (m(z + V t) + eps)^(-k/2) dt,
T_z = {t : z + V t in F}.
```

For a joint multilinear envelope the case `k = 1` holds along any line
`z + t(e_i - s e_j)` on which `s ∂_ij phi = kappa > 0`. The quantity
`∂_ij phi` is constant on such a line.

*Proof.*

1. For a box `C`, the set `C_z = {t : z + V t in C}` is a box
   `prod_r [alpha_r, beta_r]`. Each coordinate constraint involves at most one
   `t_r`, because the matched pairs are disjoint and the other coordinates are
   fixed.
2. For `t in C_z ∩ T_z`, the chord of `C` through `z + V t` in direction
   `v_r` is exactly `{t_r in [alpha_r, beta_r]}`.
3. Lemma 2.4, applied to term `e_r` alone and summed over `r`, gives
   `m + eps >= Gamma_C >= sum_r |c_r| (t_r - alpha_r)(beta_r - t_r)`.
4. Anisotropic Theorem B: for any box `D` in `R^k`,
   `integral_D (sum_r kappa_r a_r)^(-k/2) <= (pi^2/k)^(k/2) prod_r kappa_r^(-1/2)`.
   This follows from AM–GM, `sum kappa_r a_r >= k (prod kappa_r a_r)^(1/k)`,
   and the arcsine integral `integral_alpha^beta ((t-alpha)(beta-t))^(-1/2) = pi`.
5. Summing over `C` gives the bound. For the joint multilinear line, use
   Lemma 2.4 with constant `kappa`. □

**Corollary 3.5 (logarithmic cost at smooth minimizers).** Let `y*` be a
global minimizer, and let `c_ij != 0` and `v = e_i - sign(c_ij) e_j`. Suppose
`y* + t v in F` for `|t| <= t0` and `m(y* + t v) <= M t^2` there (for example
`m` is `C^{1,1}` and `y*` is interior). Then

```
N_cov(eps) >= (2/pi) sqrt(|c_ij|/M) arsinh(t0 sqrt(M/eps))
           >= (1/pi) sqrt(|c_ij|/M) log(1/eps) - O(1).
```

The same holds for joint multilinear envelopes with `|c_ij|` replaced by
`|∂_ij phi(y*)|`.

*Proof.* Take `k = 1` in Theorem 3.4 with `z = y*`, and use
`integral_{-t0}^{t0} (M t^2 + eps)^(-1/2) dt = (2/sqrt(M)) arsinh(t0 sqrt(M/eps))`. □

So a nondegenerate interior minimizer with an active bilinear term costs
`Theta(log(1/eps))`, as under alphaBB. The upper bound is Theorem 5.1.

### 3.3 Transversal strata

**Theorem 3.6 (flat strata).** Let `A = z0 + span(V)` be a `p`-flat, with
`V` an `n x p` matrix with orthonormal columns and rows `v^i` in `R^p`. Let
`S ⊆ A ∩ F` be convex (relative to `A`) with `m <= eta` on `S`. Let `E` and
`alpha` satisfy (2.1) on `S`. For a convex body `K` in `R^p`, let
`W_i(K) = max_K v^i.t - min_K v^i.t`, and define

```
tau(V, E) = inf_K (max_{ij in E} W_i(K) W_j(K))^(p/2) / vol_p(K).
```

Then

```
N_cov(eps) >= tau(V, E) * (alpha / ((p+1)^2 (eps + eta)))^(p/2) * H^p(S).
```

*Proof.*

1. For `C` in a valid cover, `K = S ∩ C` is convex. If it has empty relative
   interior it has zero measure; otherwise let `g` be its centroid, so
   `g in S ∩ C`.
2. By the Minkowski–Radon theorem the centroid of a convex body in `R^p` lies
   at distance at least `1/(p+1)` of the width from each supporting
   hyperplane. Applied to the linear function `x_i` on `K ⊆ C`, this gives
   `d_i^C(g) >= W_i(K)/(p+1)`.
3. Validity at `g` and (2.1) give
   `alpha max_E W_i W_j/(p+1)^2 <= m(g) + eps <= eta + eps`.
4. By the definition of `tau`,
   `vol_p(K) <= ((p+1)^2 (eta + eps)/alpha)^(p/2)/tau`.
5. Sum over the cover. □

**Lemma 3.7 (the constant `tau`).**

- (a) `tau(V, E) >= delta(V, E)`, where
  `delta = min over vertex covers K of E of max_{J ⊆ K, |J| = p} |det V_J|`
  and `V_J` is the `p x p` submatrix with rows `J`.
- (b) `delta > 0` iff `span(V)` is transversal for `E` (Definition 2.7).
- (c) For `p = 1` with unit direction `v`,
  `tau = max_{ij in E} |v_i v_j|^(1/2)`, so `tau > 0` iff `v` is transversal.
- (d) For `p >= 2`, `tau > 0` does not imply transversality. Example:
  `p = n = 2` with a single edge. Then `tau = 1`, because
  `W_x W_y >= vol(K)` for every convex `K`, but the plane contains `e_x`.

*Proof.*

- (a) Let `eta = max_E W_i W_j`. Then `K* = {i : W_i <= sqrt(eta)}` is a
  vertex cover, since each edge has `min(W_i, W_j) <= sqrt(W_i W_j)`. Choose
  `J ⊆ K*` with `|det V_J|` maximal, which is `>= delta`. The body `K` lies in
  the parallelepiped `{t : v^j.t in [min_K, max_K], j in J}`, whose volume is
  `prod_{j in J} W_j / |det V_J| <= eta^(p/2)/delta`.
- (b) `V u in span(e_I)` iff `v^i.u = 0` for all `i` in the complement of
  `I`. So transversality fails iff the rows of some vertex cover fail to span
  `R^p`.
- (c) For a segment of length `l`, `W_i = |v_i| l`.
- (d) Stated. □

For a straight segment in the plane at angle `theta` from a coordinate axis,
`tau` is proportional to `sqrt(theta)`, not to `theta`. The cruder
vertex-cover argument below gives `theta`. The sharper dependence is attained
(Proposition 3.13).

**Theorem 3.8 (curved strata).** Let `S ⊆ F` with `m <= eta` on `S`, and let
`E` and `alpha` satisfy (2.1) on `S`. Assume:

- **(H)** for every vertex cover `K` of `E`, every `r in (0, r0]` and every
  `xi in R^K`, `H^p(S ∩ {x : |x_K - xi|_inf <= r}) <= c_S r^p`.

Then for `eps + eta <= alpha r0^2`,

```
N_cov(eps) >= H^p(S) (alpha/(eps + eta))^(p/2) / (c_S sum_{K minimal} 2^|K|).
```

*Proof.*

1. Let `x in S ∩ C` and `rho = ((eps + eta)/alpha)^(1/2)`. By (2.1),
   `d_i d_j <= rho^2` on every edge, so `{i : d_i <= rho}` is a vertex cover.
   It contains a minimal cover `K`.
2. Then `x_K` is within `rho` in the sup norm of one of the `2^|K|` points
   whose coordinates are `l_i` or `u_i` (`i in K`).
3. Hence `H^p(S ∩ C) <= c_S rho^p sum_{K minimal} 2^|K|`. Sum over the
   cover. □

**Lemma 3.9 (C^1 criterion for (H)).** Let `S` be a compact subset of an
embedded `C^1` `p`-manifold `Mf`, with `T_x Mf` transversal for `E` at every
`x in S`. Then (H) holds.

*Proof.*

1. Fix a vertex cover `K`. The complement of `K` is independent, so
   `ker pi_K ∩ T_x Mf = {0}`. At `x0 in S` choose `J ⊆ K` with `|J| = p` such
   that `pi_J` is invertible on `T_{x0} Mf`.
2. By the inverse function theorem, `pi_J` restricted to `Mf` near `x0` is a
   `C^1` diffeomorphism onto an open set, with inverse `psi_{x0}`. Shrink to a
   compact neighborhood on which `||D psi_{x0}|| <= Lambda`.
3. For a cube `Q` of side `2r` in `R^K`, `pi_J` maps the part of `Mf` in that
   neighborhood and in `pi_K^(-1)(Q)` into a cube of side `2r` in `R^J`. The
   area formula gives measure at most `Lambda^p (2r)^p`.
4. Finitely many such neighborhoods cover `S` (compactness), and there are
   finitely many covers `K`. □

**The scout's conjecture, refined.** Consider a `p`-dimensional near-optimal
stratum.

- If it is flat and gap-nondegenerate (Definition 2.8), or curved and
  transversal (Definition 2.7), it forces `N_opt = Omega(eps^(-p/2))`, by
  Theorems 3.6 and 3.8 with `eta = 0`.
- The correct hypothesis concerns the independent coordinate subspaces of
  the gap graph, not the coordinate hyperplanes.
- For `p = 1` transversality and `tau > 0` coincide.
- For `p >= 2`, `tau > 0` is a weaker sufficient condition. Proposition 4.7
  gives a plane that is not transversal but has `tau > 0` and costs
  `Theta(1/eps)`.
- Neither condition is necessary for polynomial cost. The aligned segments of
  Example 3.12 have `tau = 0` and still cost `Omega(eps^(-1/2))`, because a
  2-dimensional *near-optimal* region around them has `tau > 0`.
- A curved version of Theorem 3.8 under a uniform lower bound on `tau` of the
  tangent spaces is expected but not proved.

### 3.4 Near-optimal boxes and the fractional vertex cover number

**Proposition 3.10 (box regions).** Let `R ⊆ F` be a box with widths `W_i`
and `m <= eta` on `R`, and let `E` and `alpha` satisfy (2.1) on `R`. Set
`rho^2 = 4(eps + eta)/alpha` and

```
nu = max { prod_i w_i : 0 < w_i <= W_i,  w_i w_j <= rho^2  (ij in E) }.
```

Then `N_cov(eps) >= vol(R)/nu`.

*Proof.* `C ∩ R` is a box with widths `w'_i`, and its center `z` lies in
`C ∩ F`. Since `C ∩ R ⊆ C`, `d_i^C(z) >= w'_i/2`. Validity at `z` and (2.1)
give `alpha w'_i w'_j/4 <= eta + eps` on every edge. So
`vol(C ∩ R) <= nu`. □

**Corollary 3.11 (exponent `tau*`).** If `R` is a cube of side `W >= rho`,
then

```
nu = rho^n (W/rho)^(n - 2 tau*(E)),     N_cov(eps) >= (alpha W^2 / (4 (eps + eta)))^(tau*(E)).
```

Here `tau*(E) = min {sum_i z_i : z_i + z_j >= 1 (ij in E), z >= 0}` is the
fractional vertex cover number. Conversely, suppose `sum_E |c_e| rho'^2/4 <= eps`.
Boxes of widths `W`, `rho'` or `rho'^2/W`, according to a half-integral
optimal `z` taking the values 0, 1/2 or 1, are valid on any region. About
`(W/rho')^(2 tau*)` of them cover `R`. So the exponent `tau*` is attained.

*Proof.*

1. Take logarithms: `log w_i = log rho + x_i log(W/rho)`. The program becomes
   the LP `max sum x_i` subject to `x_i <= 1` and `x_i + x_j <= 0`.
2. With `z = (1 - x)/2`, this LP is `n - 2 min {sum z : z_i + z_j >= 1, z >= 0}`.
3. The fractional vertex cover LP has half-integral optimal vertices.
4. Validity of the covering boxes follows from `sup Gamma <= eps`
   (Lemma 2.5). □

Comparison with alphaBB, whose exponent is `n/2`:

- `tau*(G) <= n/2`, with equality iff `G` has a fractional perfect matching
  (Tutte, as a 2-matching).
- A dense bipartite bilinear program `x^T A y`, with `x in R^a` and
  `y in R^b`, has `tau* = min(a, b)`. This matches the classical fact that
  branching on the smaller side suffices.
- A star `x_0 sum_k c_k y_k` has `tau* = 1`.
- A matching (`n/2` disjoint products) has `tau* = n/2`.

At fixed `eta` and `eps -> 0` the bound is bounded. It matters for thin
regions (Example 3.12) and for dimension dependence at fixed tolerance. It
complements the repository's `2^Omega(n)` results.

**Example 3.12 (aligned strata with quadratic growth).**

*(a) Via a constraint.*

- Instance `aligned_quad`, on `[0,1]^3`:
  `f = gamma (x-a)^2 + c (x-a)(y-z)` with the linear constraint `y = z`.
- On `F`, `f = gamma (x-a)^2`, and the optimal set
  `S = {x = a, y = z}` is aligned: its tangent `(0, 1, 1)` lies in
  `span(e_y, e_z)`, and `{y, z}` is independent. So Theorems 3.6 and 3.8 do
  not apply.

Apply Proposition 3.10 inside the plane `y = z`, with
`R' = [a-h, a+h] x [0, 1]`.

- A leaf `C` meets the plane in a box `C'` in the `(x, y)` coordinates. At
  the center of `C' ∩ R'`, the two McCormick terms give
  `Gamma >= |c| d_x (d_y + d_z) >= |c| w'_x w'_y/2`.
- Hence `N_cov >= |c| h/(gamma h^2 + eps)`. With `h = sqrt(eps/gamma)`, this
  is `|c|/(2 sqrt(gamma eps))`.

*RLT caveat.* This cost is an artifact of the missing constraint products.
Multiplying the equality `y - z = 0` by `x` gives the RLT row
`w_xy - w_xz = 0`, and together with `y = z` the lifted objective then equals
`gamma (x-a)^2 >= 0 = f*`. So one RLT product prunes the root. BARON,
ANTIGONE and SCIP's RLT separator generate such products. Lemma 1.2 does not
cover them.

*(b) With box constraints only (counterexample A of the review).* Consider
`f = (x-a)^2 + (x-a)(y-z) + (y-z)^2` on `F = X0 = [0,1]^3`, with
`a in (0,1)`.

- Take `g = (x-a)^2 + (y-z)^2` plus linear terms, which is convex, and
  `phi = xy - xz`, relaxed by termwise McCormick. The interaction graph is
  `G = {xy, xz}`.
- Write `X = x - a` and `D = y - z`. Then `f = (X + D/2)^2 + 3D^2/4`, so
  `argmin f = {x = a, y = z}`, a segment.
- Its tangent `(0, 1, 1)` lies in `span(e_y, e_z)` with `{y, z}` independent,
  and in `ker C`. The segment is therefore aligned, with `tau = 0`, and the
  rank condition (R) of Corollary 4.3 fails.
- The transverse growth `f(a + t, y, y) = t^2` is quadratic.

**Claim.** `N_cov(eps) >= 1/(2 sqrt(eps))` for `eps <= min(a, 1-a)^2`.

*Proof.* This is the argument of part (a) with `gamma = |c| = 1`. The
constraint was used there only to restrict attention to the plane `y = z`, and
here that plane lies in `F` anyway.

1. On `R' = {(x, y, y) : |x - a| <= h, y in [0,1]}`, `m = (x-a)^2 <= h^2`.
2. A leaf `C` meets the plane in a box `C'` of `(x, y)` coordinates, with
   `y` in `[l_y, u_y] ∩ [l_z, u_z]`. The center `(x_c, y_c, y_c)` of
   `C' ∩ R'` lies in `C`.
3. There `d_x >= w'_x/2`, and both `d_y` and `d_z` are at least `w'_y/2`.
   Lemma 2.1(c) for the terms `xy` and `-xz` gives
   `Gamma_C >= w'_x w'_y/2`.
4. Validity gives `area(C' ∩ R') <= 2(h^2 + eps)`, and `area(R') = 2h`. Take
   `h = sqrt(eps)`. □

*Upper bound.* For this smooth instance `N_opt = Theta(eps^(-1/2))`, as the
recheck noted.

- `m = X^2 + X D + D^2` is a positive semidefinite quadratic form in the
  coordinates, so (QD) holds. Writing `m = |M(x - x*)|^2`,
  `m(x) <= 2 m(y) + 6 ||M||^2 |x - y|_inf^2`.
- `m` depends only on `(X, D)`, with eigenvalues `1/2` and `3/2`, so
  `integral (m + eps)^(-3/2) = O(eps^(-1/2))`.
- Theorem 5.1(a) then bounds bisection by `O(eps^(-1/2))`.

This smooth instance is convex as a whole, so a solver that detects convexity
would not branch. The variant `f = (x-a)^2 + (x-a)(y-z) + K|y-z|` with
`K = 2` is nonconvex. It satisfies `f >= X^2 + (K-1)|D|`, has the same optimal
segment and the same bound, and involves no constraints on which RLT products
could act.

Computations (`rules_table_i.jsonl`, Section 8.4) grow like `eps^(-1/2)` under
every rule tried:

- bisection takes 69, 301, 1227, 3699 and 12115 nodes for
  `eps = 10^-2, ..., 10^-6`, against the bound of 500 leaves at `10^-6`;
- the relaxation point `LP(1,.2)` takes 12389 nodes at `10^-6`;
- SCIP's default rule takes 12455;
- product-score strong branching takes 3939;
- incumbent branching takes 15213;
- the `K = 2` variant takes 6645 nodes with bisection and 4265 with
  product-score strong branching.

The `K = 2` counts are close to those of part (a). For bisection and
product-score strong branching they are equal, and they differ in the other
rules (9921 against 9919 for `LP(1,.2)`). We have not checked why.

**Consequence.** Aligned strata do not automatically have linear transverse
growth when `n >= 3`. Section 4 proves automatic linear growth in 2D
(Theorem 4.4), where the bilinear Hessian is nonsingular, and for the face
structure of Theorem 4.5. Part (b) is a box-constrained aligned stratum with
quadratic growth. Its cost comes from a 2-dimensional *near-optimal* strip
`{y = z, |x - a| <= sqrt(eps)}`, whose plane has `tau = 1/sqrt(2) > 0`. The
optimal set alone does not determine the exponent (Section 7).

### 3.5 Sharpness of the transversal bound

**Proposition 3.13 (tilted stratum).** Let `theta in (0, 1]` and
`eps <= theta/16`. Consider
`f = 2|U| + U Y` on `[0,1]^2` with `U = (x - 1/2) + theta (y - 1/2)` and
`Y = y - 1/2` (instance `tilt(theta)`).

- Here `U Y = (x - 1/2)(y - 1/2) + theta (y - 1/2)^2`. The bilinear part is
  relaxed by McCormick with `c = 1`, and the convex square is kept exact.
- The optimal set is the line `U = 0`, which is transversal and lies along a
  concave direction of `xy`.

Then

```
(1/2) sqrt(theta/eps) <= N_opt(eps) <= 2 ceil((1/4) sqrt(theta/eps)) <= (1/2) sqrt(theta/eps) + 2.
```

*Proof of the lower bound.* Apply Theorem 3.6 with `p = 1`, `alpha = 1`,
`eta = 0` and `v = (-theta, 1)/sqrt(1 + theta^2)`. Then
`tau = (theta/(1+theta^2))^(1/2)` and `H^1(S) = (1 + theta^2)^(1/2)`.

*Proof of the upper bound.*

1. Cut `[0,1]` in `y` into `K = ceil(1/h)` strips of height at most
   `h = 4 sqrt(eps/theta) <= 1`. In each strip, split `x` at the point `x_m`
   where the optimal line crosses mid-height `y_mid`.
2. On the right box `[x_m, 1] x [y0, y0 + h']`, write `s = x - x_m >= 0` and
   `t = y - y0`. Then `U = s + theta(t - h'/2)`.
3. Lemma 2.1 gives `Gamma <= s t`. Also `m = 2|U| + U Y >= 1.5 |U|`, since
   `|Y| <= 1/2`.
4. If `t >= h'/2`, then `U >= s`, and `s t <= 1.5 s` because `h' <= 1`.
5. If `t < h'/2`, let `D = theta(h'/2 - t)`. The concave function
   `s -> s t - 1.5 |s - D|` has slopes `t ± 1.5`, so it is maximized at
   `s = D`. The maximum is `theta (h'/2 - t) t <= theta h^2/16 <= eps`.
6. The left box is symmetric. □

The scan in `tilt_certificate.log` finds the smallest valid strip count with
exact node bounds. It agrees with `2 ceil(sqrt(theta/eps)/4)`, and the ratio
to the lower bound falls from 1.15 to 1.00 as `eps` decreases. So the constant
of Theorem 3.6 is exact here.

- As `theta -> 0`, `N_opt` falls to 2 for `eps >= theta/16`. This matches the
  aligned case (Theorem 4.4).
- Widest-side bisection needs about `1900 ~ eps^(-1/2)` nodes at
  `eps = 10^-6` for `theta = 0.3` (Section 8). Its count does not improve as
  `theta` decreases.

### 3.6 Curved non-transversal surfaces (row slices)

Theorem 3.6 handles flat near-optimal pieces, and Theorem 3.8 handles
transversal curved ones. A curved, non-transversal surface escapes both. The
following example and its row-slice argument are due to the recheck of this
note (`../../reviews/face-exact-recheck.md`, Section 6.3). I re-derived the
proof and checked the example with my own code (`curved_check.log`).

**Proposition 3.14 (curved version of Proposition 4.7).** Let
`psi(s) = -s - s^2/2`, `c0 = 3/4`, `D = x1 - x2 - c0`, and on `[0,1]^3`

```
f = max_{s in [-1,2]} (D - psi(s)) (y - s)  =  G(D, y) + D y,
G(D, y) = max_{s in [-1,2]} [ -s D - psi(s) y + psi(s) s ].
```

- `g = G(x1 - x2 - c0, y)` is convex, as a maximum of affine functions.
  `phi = D y = x1 y - x2 y - c0 y` is bilinear plus linear, on the path
  `x1 - y - x2`, and is relaxed by termwise McCormick.
- (a) `f >= 0`, and `f = 0` on the surface `Sigma = {D = psi(y)}`, so
  `f* = 0`. Moreover `m = f >= (D - psi(y))^2/12`.
- (b) `Sigma` is curved (`psi'' = -1`) and not transversal: its tangent
  planes contain `(1,1,0)`, which lies in `span(e_x1, e_x2)`.
- (c) For `eps < 1/2`,
  `N_cov(eps) >= A/(2 eps (1 + ln(1/(2 eps))))`, with
  `A = integral_0^1 (1 - |psi(y) + c0|) dy = 0.6148`.
- (d) The bound of Theorem 3.6 with `p = 2`, applied to convex pieces of
  near-optimal sets `{m <= eta}` with any `eta >= 0`, is at most
  `0.471 eps^(-3/4)`.

*Proof.*

- (a)
  1. Taking `s = y` gives `f >= 0`.
  2. `psi` is decreasing on `[-1, 2]`. So on `Sigma`, `(psi(y) - psi(s))` and
     `(y - s)` have opposite signs for every `s`, and `f = 0`.
  3. For the growth bound, let `delta = D - psi(y)` and take
     `s = y - delta/8`, which lies in `[-1, 2]` because `|delta| <= 1.75`.
  4. Then `psi(y) - psi(s) = psi'(xi) delta/8` with `|psi'(xi)| <= 2.22`. So
     `(D - psi(s))(y - s) >= (1 - 2.22/8) delta^2/8 >= delta^2/12`.
- (b) The normal of `Sigma` is `(1, -1, -psi'(y))`, which is orthogonal to
  `(1,1,0)`.
- (c) Parametrize `Sigma` by `(t, y)`, with `x2 = t` and
  `x1 = t + psi(y) + c0`. Take a box `C` of a valid cover and `y` in its
  `y`-range.
  1. The row `{t : (t + psi(y) + c0, t, y) in C}` is an interval of some
     length `ell <= 1`.
  2. Its midpoint `p` lies on `Sigma`, so `m(p) = 0`. Moving `t` by
     `± ell/2` keeps both `x1` and `x2` inside `C`, so
     `d_x1(p), d_x2(p) >= ell/2`.
  3. Lemma 2.1(c) for `x1 y` and `-x2 y` gives
     `Gamma_C(p) >= ell d_y(y)`, where `d_y` is the distance of `y` to the
     `y`-faces of `C`. Validity at `p` gives `ell <= eps/d_y(y)`.
  4. Hence the `(t, y)`-area of `Sigma ∩ C` is at most
     `2 integral_0^(w_y/2) min(1, eps/d) dd <= 2 eps (1 + ln(1/(2 eps)))`.
  5. The `(t, y)`-area of `Sigma ∩ [0,1]^3` is `A`, since for each `y` the
     row has length `1 - |psi(y) + c0|`.
  6. Sum over the cover.
- (d)
  1. Let `S` be a convex piece of a plane, contained in `{m <= eta}`.
     Taking `K = S` in the definition of `tau` gives
     `tau H^2(S) <= max_E W_i W_j (S)`.
  2. The pair `{x1, x2}` carries no bilinear term, so it cannot satisfy
     (2.1). Hence `E ⊆ {x1 y, x2 y}` and `alpha <= 1`, and the bound is at
     most `W_y(S)/(9 (eps + eta))`.
  3. By (a), `S` lies in the band `|D - psi(y)| <= w = sqrt(12 eta)`, and
     its image in the `(D, y)` plane is convex.
  4. Take two points at `y`-distance `W_y` and their midpoint. Since
     `psi'' = -1`, `psi` at the midpoint exceeds the average of the endpoint
     values by `W_y^2/8`. So `W_y^2/8 <= 2w`, that is, `W_y <= 4 sqrt(w)`.
  5. The resulting bound `4 (12 eta)^(1/4)/(9 (eps + eta))` is largest at
     `eta = eps/3`, where it equals `0.471 eps^(-3/4)`. □

**The other tools.** The recheck also bounds:

- Theorem 3.6 with `p = 1`, Theorem 3.8 and Theorem 3.4, each by
  `O(eps^(-1/2))`;
- Theorem 3.6 with `p = 3` (`tau = 0`) and Proposition 3.10, by `O(1)`.

The integral bound of Theorem 3.2 also gives only `eps^(-1/2)` up to logs,
since `m` grows quadratically across `Sigma`. So every lower-bound tool of
Sections 3.1–3.4 gives `O(eps^(-3/4))`, while `N_cov` is of order at least
`1/(eps log(1/eps))`.

The row-slice argument in (c) is a lower-bound tool in its own right. It
applies to segments of the near-optimal set in a direction `u` with
`supp(u)` independent in `E`. The gap at each segment's midpoint is weighted
by the distance to the faces in the coordinates that stay fixed along the
segment, and the bound follows by integrating over the family of segments.

An upper bound on `N_opt` for this instance is not known.

Numerical checks (`curved_check.log`):

- the closed-form maximization over `s` agrees with a grid to `1e-8`;
- `min f = 1.8e-11` on 20000 points;
- `f = 0` on `Sigma` to `1e-31`;
- `min f/(D - psi(y))^2 = 0.123`;
- no convexity violations of `G` in 20000 midpoint tests;
- the row-slice inequality holds on 16209 random boxes (minimum ratio
  1.0000);
- the lower bound overtakes `0.471 eps^(-3/4)` from `eps = 10^-6` on, by
  factors 1.46, 8.8 and 176 at `10^-6`, `10^-10` and `10^-16`.

## 4. Structure of optimal sets and bounded certificates

Section 3 shows that transversal strata are expensive. This section shows
when aligned strata are cheap.

- In 2D box-constrained problems, aligned strata automatically have the
  linear transverse growth that makes them cheap (Theorem 4.4).
- The same holds for faces whose fixed coordinates have the structure of
  Theorem 4.5.
- In three or more dimensions this fails in general (Example 3.12(b)).

Lemma 4.1 is a standard fact of convex analysis. The graph of `g` over the
segment lies in the relative interior of one face of the epigraph, and the
normal cone, hence the subdifferential, is constant there (Rockafellar,
*Convex Analysis*). The short proof is included for completeness.

**Lemma 4.1.** Let `g` be convex and finite on a convex set `D`, and affine on
a relatively open segment `sigma ⊆ D`. Let `u` satisfy `q + t u in D` for all
`q in sigma` and `t in [0, t0]`. Then the directional derivative
`g'(q; u) = lim_{t↓0} (g(q + t u) - g(q))/t`, which lies in `[-inf, inf)`, is
the same at every `q in sigma`.

*Proof.*

1. Let `p, p0 in sigma` and `h = g'(p0; .)`. On the cone of feasible
   directions at `p0`, `h` is positively homogeneous and convex, so
   `h(a + b) >= h(a) - h(-b)`.
2. Convexity gives `g(p0 + d) >= g(p0) + h(d)` for feasible `d`.
3. Since `g` is affine on `sigma` and `p0` is relatively interior,
   `h(p0 - p) = g(p0) - g(p)`.
4. Hence
   `g(p + t u) >= g(p0) + h((p - p0) + t u) >= g(p0) + t h(u) - g(p0) + g(p)`.
   So `g'(p; u) >= g'(p0; u)`.
5. Exchanging `p` and `p0` gives equality. □

**Theorem 4.2 (structure of optimal segments).** Let `f = g + phi` with `g`
convex and continuous on `X0`, and `phi` quadratic with Hessian `C` (bilinear,
possibly with square terms). Let
`sigma = {p0 + s v : |s| < s0} ⊆ argmin_F f`.

- (i) `v^T C v <= 0`: optimal segments point in concave or flat directions of
  `phi`.
- (ii) Suppose `v^T C v = 0` and `sigma + [0, t0] u ⊆ F`. Then for `|s| < s0`,

  ```
  m'(p0 + s v; u) = m'(p0; u) + s u^T C v.
  ```

  The one-sided transverse growth rate of `m` is affine along the segment,
  with slope `u^T C v`.

*Proof.*

- (i) On `sigma`, `g = f* - phi`, and `s -> -phi(p0 + s v)` has second
  derivative `-v^T C v`. Convexity of `g` forces this to be `>= 0`.
- (ii) Now `phi` is affine on `sigma`, so `g` is affine there. By Lemma 4.1,
  `g'(.; u)` is constant on `sigma`. Also
  `m'(p; u) = g'(p; u) + grad phi(p).u`, and
  `grad phi(p0 + s v).u = grad phi(p0).u + s v^T C u`. □

**Corollary 4.3.**

- (a) Suppose `g` is differentiable on `sigma ⊂ int F`. Then either
  `v^T C v < 0` or `C v = 0`.
- (b) Suppose `g` is `C^2` near a `C^2` curve `gamma` of interior minimizers.
  Then at each point either `gamma'^T C gamma' < 0` or `C gamma' = 0`.
- (c) Assume the **rank condition (R)**: `C v != 0` for every nonzero
  `v in span(e_I)` with `I` independent in `G`. If `g` is `C^2`, every
  interior optimal `C^2` stratum is transversal. Theorems 3.6 and 3.8 then
  give `N_opt = Omega(eps^(-p/2))`.

  (R) holds for:
  - one edge;
  - a perfect matching (an isolated coordinate `i` has `C e_i = 0`, so any
    unmatched vertex breaks (R));
  - the complete graph `K_n`;
  - dense bipartite programs `x^T A y` iff `A` is square and nonsingular.

  If (R) fails, (b) still forces aligned tangent directions into `ker C`.
  Along such a direction `phi` is affine with constant slope.
- (d) For an axis-parallel optimal segment in direction `e_k` of a bilinear
  `phi`, and `u = ±e_i`, the rate `m'(.; ±e_i)` changes linearly along the
  segment with slope `±c_ik`. So if `c_ik != 0`, it vanishes at most at one
  point.

*Proof.*

- (a) At interior points `m'(p; ±u) = ±grad m(p).u = 0` for all `u`. By
  Theorem 4.2(ii), `s u^T C v = 0` for all `s` and `u`.
- (b) At an interior minimizer, `grad f = 0` and `grad^2 f` is positive
  semidefinite (PSD). From `f(gamma(t)) = f*`,
  `gamma'^T grad^2 f gamma' = 0`, hence `grad^2 f gamma' = 0`. Therefore
  `gamma'^T grad^2 g gamma' = -gamma'^T C gamma' >= 0`. If this vanishes, then
  `grad^2 g gamma' = 0` (PSD), and so `C gamma' = 0`.
- (c) For `v in span(e_I)`, `v^T C v = sum_{i,j in I} C_ij v_i v_j = 0`, so
  (b) would force `C v = 0`.
- (d) This is Theorem 4.2(ii) with `v = e_k`. □

So in smooth problems aligned interior strata cannot occur when (R) holds.
Aligned strata come from:

- nonsmooth convex terms, such as the kink in the scout's example;
- optimal sets on the boundary of `X0`;
- constraints, as in Example 3.12;
- kernel directions of `C`.

**Theorem 4.4 (2D: a full aligned optimal segment gives a 2-box
certificate).** Let `n = 2`, `F = X0 = [L_x, U_x] x [L_y, U_y]`, and
`f = g + c x y` (plus linear terms), with `g` convex and continuous and
`c != 0`. Suppose `{a} x [L_y, U_y] ⊆ argmin f` with `L_x < a < U_x`. Then
`{x <= a}` and `{x >= a}` are valid at `eps = 0`. Hence `N_opt(eps) <= 2` for
every `eps >= 0`. If `a in {L_x, U_x}`, the root box itself is valid.

*Proof.*

1. For `y` in `(L_y, U_y)`, let `r_±(y) = m'((a, y); ±e_x)`. These are `>= 0`
   by optimality.
2. By Theorem 4.2(ii) with `v = e_y`, `r_+(y) = r_+(y0) + c(y - y0)` and
   `r_-(y) = r_-(y0) - c(y - y0)`.
3. `t -> m(a ± t, y)` is convex, since `phi` is affine in `x`. Hence
   `m(a ± t, y) >= t r_±(y)`.
4. Case `c > 0`. Letting `y0 -> L_y` in the first formula gives
   `r_+(y) >= c(y - L_y)`. Letting `y0 -> U_y` in the second gives
   `r_-(y) >= c(U_y - y)`.
   - Right box: by Lemma 2.1(a),
     `Gamma = c min((x-a)(y-L_y), (U_x-x)(U_y-y)) <= c(x-a)(y-L_y) <= m`.
   - Left box: `Gamma = c min((x-L_x)(y-L_y), (a-x)(U_y-y)) <= c(a-x)(U_y-y) <= m`.
5. Case `c < 0`. Now `r_+(y) >= |c|(U_y - y)` and `r_-(y) >= |c|(y - L_y)`.
   These match the corners in `Gamma = |c| min(delta_x^- delta_y^+, delta_x^+ delta_y^-)`.
6. Continuity extends the inequality to the closed boxes. □

The sign of `c` fixes both which corners of the McCormick gap are
second-order and which way the rates slope. These always match. The scout's
instance, `g = 2|x - a|` with `c = -1`, is one case. Every convex `g` works:
the sharpness needed is supplied by Theorem 4.2.

**Theorem 4.5 (faces that fix star centres).** Let `F = X0`, with termwise
bilinear `phi`. Suppose `K` is an independent vertex cover of `G` in which
every vertex outside `K` has at most one neighbour. Equivalently, `G` is a
disjoint union of stars and isolated vertices, and `K` is exactly the set of
centres. The hypothesis is about the pair `(G, K)`, that is, about which
coordinates the optimal face fixes. Let `I` be the complement of `K`. Suppose the face `Phi = {x in X0 : x_K = a_K}`, with every `a_k` interior
to its range, lies in `argmin f`. Then the `2^|K|` orthant boxes
`{sigma_k (x_k - a_k) >= 0, k in K}` form a certificate at `eps = 0`.

*Proof.*

1. Fix an orthant `sigma`, a point `x_I` in the open box of the
   `I`-coordinates, and `tau = sigma ∘ t` with `t >= 0`. Let `p = (a_K, x_I)`.
2. Along the direction `(tau, 0)` the curvature of `phi` is
   `tau^T C_KK tau = 0`: no edges join centers, and there are no squares. So
   `m` is convex along it, and `m(a_K + tau, x_I) >= rho(x_I; tau)`, where
   `rho(x_I; tau) = m'(p; (tau, 0))`.
3. Theorem 4.2(ii) applies to segments inside `Phi` in directions
   `v in span(e_I)`, for which `v^T C v = 0`. It shows that
   `rho(x_I; tau) = rho(x_I^0; tau) + (x_I - x_I^0)^T C_IK tau` is affine in
   `x_I`.
4. An affine function that is `>= 0` on a box is at least
   `sum_i |slope_i| dist(x_i, argmin side)`. Here `slope_i = c_{i k(i)} tau_{k(i)}`
   for a leaf `i` with center `k(i)`, and `0` for isolated `i`.
5. On the orthant box, the McCormick gap of term `(k, i)` is at most
   `|c_ki| t_k (x_i - L_i)` if `c_ki sigma_k > 0`, and at most
   `|c_ki| t_k (U_i - x_i)` otherwise, by Lemma 2.1(a). This is the same side
   on which the `i`-th slope term is minimized.
6. Summing, `Gamma <= rho <= m`. □

If a vertex outside `K` has two neighbours in `K`, the slopes
`c_ik tau_k + c_ik' tau_k'` can cancel. The conclusion then fails:

**Proposition 4.7 (the condition on the fixed coordinates cannot be
dropped).** Let `f = |X1 - X2| + (X1 - X2) y` on `[0,1]^3`, with
`X_k = x_k - a_k`, `a_k in (0,1)` and `D = X1 - X2`, and termwise McCormick on
`x1 y` and `-x2 y`.

- The interaction graph is the path `x1 - y - x2`, which is itself a star
  with centre `y`.
- The optimal face `Phi = {x1 = a1, x2 = a2}` fixes the vertex cover
  `K = {x1, x2}`, in which `y` has two neighbours. So Theorem 4.5 does not
  apply.

Then:

- (a) No exact certificate exists.
- (b) `tau H^2(S)/(9 eps) <= N_cov(eps) <= N_opt(eps) <= 1 + 18/eps`, where
  `S = {X1 = X2}` intersected with the box and `tau = 1/sqrt(2)`. For
  `a1 = 1/3` and `a2 = sqrt(2) - 1` the lower bound is `0.102/eps`. So
  `N_opt = Theta(1/eps)`.
- (c) The plane `S` is not transversal: it contains `(1,1,0)`, which lies in
  `span(e_x1, e_x2)`, and `{x1, x2}` is independent. It is nonetheless
  gap-nondegenerate.
- (d) `argmin f = S ∪ {y = 1, X1 <= X2}`.

*Proof.*

1. `f = |D| + D y >= 0` for `y in [0,1]`, with equality iff `D = 0`, or
   `D < 0` and `y = 1`. This gives (d), and `S` is an optimal flat stratum
   with `p = 2`.
2. In the orthonormal basis `(1,1,0)/sqrt(2)`, `e_y` of the plane, the rows
   are `v^x1 = v^x2 = (1/sqrt(2), 0)` and `v^y = (0, 1)`.
3. For convex `K`, `max_E W_i W_j = W_{t1} W_{t2}/sqrt(2) >= vol(K)/sqrt(2)`,
   so `tau >= 1/sqrt(2)`.
4. Theorem 3.6 with `alpha = 1` (Lemma 2.1(c)) gives the lower bound in (b),
   and the lower bound gives (a).
5. *Upper bound.* The construction is due to the face-exact review; it is
   re-derived here. Use a quadtree in `(x1, x2)` in which every box keeps the
   full `y`-range `[0,1]`. A square `Q` of side `h` is a leaf if
   `h <= 2 eps` or `min_Q |D| >= 2h`.
   - If `h <= 2 eps`, then `sup Gamma <= h/4 + h/4 <= eps` by Lemma 2.1(d),
     since `w_y = 1`.
   - If `min_Q |D| >= 2h` and `D < 0` on `Q`, then `m = |D|(1 - y)`. The
     gaps of `x1 y` and `-x2 y` are at most `delta_x1^+ delta_y^+ <= h(1-y)`
     and `delta_x2^- delta_y^+ <= h(1-y)` (Lemma 2.1(a)). So
     `Gamma <= 2h(1-y) <= m`.
   - If `min_Q |D| >= 2h` and `D > 0` on `Q`, then `m = D(1 + y)`. The gaps
     are at most `delta_x1^- delta_y^- <= h y` and
     `delta_x2^+ delta_y^- <= h y`. So `Gamma <= 2hy <= m`.
   - On a square of side `h`, `D` ranges over an interval of length `2h`.
     So a refined square satisfies `|i1 - i2 - (a1 - a2)/h| < 3` in grid
     indices, and there are at most `6/h` of them at side `h`.
   - Summing over dyadic `h > 2 eps` gives at most `6/eps` refinements, each
     of which adds 3 leaves.
6. (c) was checked in the statement.
7. Remark (from the review): (a) also follows from Proposition 4.6(b). The
   direction `(1, 1, -1)` is concave for the `x1 y` term, and `m ≡ 0` along it
   inside `S`. □

Computations:

- In `path3_check.log`, two of the four orthant boxes around `(a1, a2)` have
  negative bounds (`-0.18` and `-0.31`). Bisection needs 241, 2353 and 24497
  nodes at `eps = 10^-2, 10^-3, 10^-4`, and the LP-point rules show the same
  `1/eps` growth.
- In `path3_quadtree.log`, every quadtree leaf has an LP bound `>= -eps`,
  and leaves times `eps` stays between 6.1 and 13.0 for
  `eps = 10^-1, ..., 10^-3`.
- The recheck certified every quadtree leaf in exact rational arithmetic,
  for three rational `(a1, a2)` and `eps = 1/10, ..., 1/300`. It also
  confirmed `tau H^2(S)/9 = 0.10212`, and that the leaf counts stay within
  `1 + 18/eps` (`../../reviews/face-exact-recheck.md`, Section 5).

So the condition of Theorem 4.5 on the fixed coordinates cannot be dropped.
Transversality is also not necessary for polynomial cost when `p >= 2`.

**Proposition 4.6 (bounded counts and exact certificates).** Assume a
termwise bilinear relaxation.

- (a) Let `F = X0`. Then `N_opt(eps)` is bounded as `eps -> 0` iff an exact
  certificate exists, and then `N_opt(0) <= liminf N_opt(eps)`.

  With a polyhedral `Q` the closure step of the proof fails. A limit box can
  meet `F` only on a proper face, where its approximating boxes may miss `F`
  and the gap is not controlled. The statement is then open (review,
  Section 7.4).
- (b) Suppose, for some minimizer `y*`, some `c_ij != 0` and some direction
  `v` with `c_ij v_i v_j < 0` and `y* + t v in F` for `t in [0, t0]`, that
  `liminf_{t↓0} m(y* + t v)/t = 0`. Then no exact certificate exists, and
  `N_opt(eps) -> infinity`. In particular this holds at every interior
  minimizer where `m` is differentiable and some bilinear term is present.
  With `C^{1,1}` growth, the rate is `Omega(log(1/eps))` (Corollary 3.5).

*Proof.*

- (a) Take certificates with at most `N` boxes for `eps_k -> 0`. Pass to a
  subsequence with a fixed tree shape and convergent split points, using
  compactness. The limit guillotine partition covers `X0`.
  - A point `x` interior to a limit box lies in the approximating boxes for
    large `k`.
  - `Gamma_B(x)` depends continuously on the bounds (Lemma 2.1), so
    `Gamma <= m` on the interior. By continuity this extends to the closure.
  - Degenerate limit boxes have measure zero and can be dropped.
- (b)
  1. The leaves are closed and convex and finite in number, so one leaf `C`
     contains `[y*, y* + t1 v]` for some `t1 > 0`.
  2. For `0 < t < t1`, the chord of `C` through `y* + t v` extends at least
     `t` backward and `t1 - t` forward. Lemma 2.4 for the single term gives
     `Gamma_C(y* + t v) >= |c_ij v_i v_j| t (t1 - t)`.
  3. Validity at `eps = 0` then gives
     `m(y* + t v)/t >= |c_ij v_i v_j| (t1 - t)`, which contradicts the
     hypothesis. □

So finite termination at `eps = 0` with McCormick requires linear growth of
`m` along every feasible concave direction at every minimizer. The
qualitative finite-termination theorems for branching at relaxation solutions
(Al-Khayyal–Sherali 2000; Shectman–Sahinidis 1998, known here only from
metadata) must therefore rest on settings with this kind of growth. The exact
correspondence with their hypotheses has not been checked.

### 4.7 The two-dimensional picture

For `n = 2`, `f = g + c x y` with `g` convex, and `F = X0`, the results give
the following. The last column says which parts are proved.

| Optimal-set piece | Growth | `N_opt(eps)` | Status |
|---|---|---|---|
| Full axis-parallel segment | automatic, linear except at one point (Thm 4.2) | 2 | proved (Thm 4.4) |
| Segment at angle `theta` (necessarily along a concave direction, Thm 4.2(i)) | sharp | `(1/2) sqrt(theta c/eps) + O(1)` | proved for `tilt` (Prop 3.13) |
| Transversal `C^1` curve | any | `Omega(eps^(-1/2))` | proved (Thm 3.8); `O(eps^(-1/2))` under (QD) or sharpness (Thm 5.1) |
| Interior point, `C^{1,1}` | quadratic | `Omega(log(1/eps))`, no exact certificate | proved (Cor 3.5, Prop 4.6); `O(log)` under (QD) |
| Point with linear growth in all concave directions | sharp | `O(1)` in the tested instance (`sharp_pt`: 3 nodes) | conjectured in general |

Two dimensions are special here. The bilinear Hessian `[[0, c], [c, 0]]` is
nonsingular, so Theorem 4.2 forces linear growth along aligned segments. In
three dimensions this fails (Example 3.12(b)).

**Conjecture 4.8 (2D dichotomy).** Let `n = 2` and `F = X0`, and let the
optimal set be a finite union of points and `C^2` arcs. Then
`N_opt(eps) = O(log(1/eps))` if every arc is an axis-parallel segment, and
`N_opt(eps) = Theta(eps^(-1/2))` otherwise.

- The lower bound in the second case is proved (Theorem 3.8).
- The upper bounds are proved only for single-piece instances under (QD) or
  sharpness (Theorem 5.1), and for full segments (Theorem 4.4).
- A segment that ends inside the box needs extra boxes near its endpoint.
  There, `m(a, y) > 0` and the transverse rate is no longer controlled by
  Theorem 4.2.

## 5. Branching rules

Throughout this section, the *kink family* is

```
f_{a,b}(x, y) = L|x - a| + c (x - a)(y - b)   on [0,1]^2,   L > |c| max(b, 1 - b),
```

with termwise McCormick. Its optimal set is `{a} x [0,1]`, so
`N_opt(eps) = 2` for all `eps` by Theorem 4.4. The *mirrored family*
`f'_{a,b} = L|y - b| + c (x - a)(y - b)` has optimal set `[0,1] x {b}`. The
scout's instance is `f_{1/3, sqrt(2)-1}` with `L = 2` and `c = -1`.

### 5.1 Upper bounds for bisection and balanced rules

**Theorem 5.1 (bisection under second-order schemes).** Let `X0` be a cube of
side `s0` and `F = X0`. Suppose the relaxation satisfies
`sup_D Gamma_D <= tau s(D)^2` for every box `D` with longest side `s(D)`.
By Lemma 2.5 this holds for McCormick with `tau = sum_E |c_e|/4`, and for
every second-order scheme. Consider dyadic bisection, either `2^n`-ary or
binary widest-side. The intermediate boxes of the binary version satisfy the
same bound and lie within the cubes counted below, so the counts change only
by a factor of at most `2^n`.

- (a) Assume **(QD)**: `m(x) <= K (m(y) + |x - y|_inf^2)`. Then
  `|T_bis| <= 1 + 2^(n+1) Lambda^(n/2) integral_{X0} (m + eps)^(-n/2)` with
  `Lambda = K(tau + 1) + tau`.
- (b) Assume `m >= mu dist_inf(., S)`, where `S` has covering numbers
  `N_inf(S, r) <= c_S r^(-p)` by sup-norm balls of radius `r <= s0`. Then for
  `p >= 1`,
  `|T_bis| <= C0 + 2^(n+2) 7^n c_S (tau/eps)^(p/2)`, where `C0` depends only
  on `n`, `s0` and `tau/mu`. For `p = 0` the bound is `O(log(1/eps))`.

*Proof.*

- (a) This is the scout's Theorem C with `alpha' n/4` replaced by `tau`. Its
  proof uses only the upper gap on non-pruned cubes. The spatial review
  (Section 5) checked the proof and corrected the sufficient condition for
  (QD).
- (b)
  1. A non-pruned level-`j` cube `D` of side `s_j` contains `y` with
     `mu dist(y, S) <= m(y) < tau s_j^2`. So `s_j^2 > eps/tau` and
     `dist(D, S) < tau s_j^2/mu`.
  2. For `s_j <= mu/tau`, `D` lies within sup distance `2 s_j` of `S`.
     Covering `S` by `N_inf(S, s_j)` balls, each of whose enlargements meets at
     most `7^n` level-`j` cubes, bounds the level count by
     `7^n c_S s_j^(-p)`.
  3. Levels with `s_j > mu/tau` contribute a constant.
  4. Sum the geometric series down to `s_j = (eps/tau)^(1/2)`. □

**Proposition 5.2 (balanced widest-side rules).** Let `X0 = [0,1]^n`. Take any
rule that selects the widest side (relative to the root) and splits it at a
point of `[l + beta w, u - beta w]`, with `beta in (0, 1/2]`. This includes
`R(alpha, beta)` with effective `beta' = max(beta, (1 - alpha)/2)`. Under the
hypotheses of Theorem 5.1(a),

```
|T| <= 1 + 4 G (2/beta)^n Lambda^(n/2) integral_{X0} (m + eps)^(-n/2),
G = ceil(n log(2/beta) / log(1/(1-beta))) + 1.
```

*Proof.*

1. **Aspect ratio.** Every box has `max width / min width <= 1/beta`. When
   the widest side `w_max` is split, the new sides are at least `beta w_max`.
2. **Chains.** Group the non-pruned boxes by the dyadic band `(s/2, s]` of
   their largest width. Volumes in a band lie in `((beta s/2)^n, s^n]`, and
   each split reduces the volume by a factor at most `1 - beta`. So a
   root-to-leaf path contains at most `G` boxes of the band.
3. **Antichains.** By Mirsky's theorem, the band splits into `G` antichains.
   Each antichain consists of interior-disjoint boxes.
4. **Location.** As in Theorem C, a non-pruned box of the band lies in
   `{m + eps <= Lambda s^2}`.
5. Hence the band holds at most `G vol{m + eps <= Lambda s^2}/(beta s/2)^n`
   boxes. Summing over bands as in the proof of Theorem C gives the bound. □

**Consequence.** In the smooth regime the rule does not matter beyond
constants. Take (QD) together with an optimal set that is a finite union of
transversal Morse–Bott strata, or of nondegenerate minimizers with an active
bilinear term. The integral is then `Theta(eps^(-p/2))`, or
`Theta(log(1/eps))` for points. This matches the lower bounds of Theorems 3.6
and 3.8 and of Corollary 3.5. So bisection and every balanced widest-side
rule are within constant factors of `N_opt`. The constants depend on the
instance: `K`, `tau`, the conditioning of the strata and `alpha`.

### 5.2 Oblivious rules lose a polynomial factor

A rule is *oblivious* if its split tree is fixed in advance. At each node it
chooses a coordinate and a split ratio in `[beta, 1 - beta]` as a function of
the node's position in the tree, not of the instance. Uniform bisection,
fixed-ratio splitting and cyclic coordinate choice are examples.

**Theorem 5.3.** Let `c != 0`, `L >= 2|c|`, and `b0, a0` fixed. For every
oblivious rule with ratios in `[beta, 1 - beta]` and every
`eps <= beta^2 |c|/8`,

```
E_{a ~ U[0,1]} N(f_{a,b0}, eps) + E_{b ~ U[0,1]} N(f'_{a0,b}, eps) >= beta sqrt(|c| / (8 eps)).
```

Every instance in both families has `N_opt = 2`. So for some instance in one
of the two families, the rule needs at least `(beta/2) sqrt(|c|/(8 eps))`
nodes.

*Proof.*

1. **A straddling box stays open.** Let `B` be a box with
   `a in (l_x, u_x)`. At the point `(a, midpoint of y)`, the kink term
   vanishes, and the McCormick envelope equals `-(|c| w_y/2) D_x`, where
   `D_x = min(a - l_x, u_x - a)`. So `LB(B) <= -(|c| w_y/2) D_x`.
2. **Ancestors stay open.** By monotonicity (Section 1.1),
   `LB(ancestor) <= LB(B)`. So every box with `LB < -eps` is processed.
3. **A partition of comparable boxes.** Let `A = 8 eps/(|c| beta) <= 1`, and
   let `P_A` be the set of boxes of the (infinite) split tree with area at
   most `A` whose parent has area greater than `A`. `P_A` is a finite
   partition of `[0,1]^2`, its areas lie in `[beta A, A]`, and
   `|P_A| >= 1/A`.
4. **Expected processed boxes for `f_{a,b0}`.** For `B in P_A` and `a`
   uniform, `P(D_x > 2 eps/(|c| w_y)) = (w_x - 4 eps/(|c| w_y))^+`, which is
   at least `w_x/2` because `w_x w_y >= beta A = 8 eps/|c|`. So the expected
   number of processed boxes of `P_A` is at least `sum_{P_A} w_x/2`.
   Similarly, for `f'_{a0,b}` it is at least `sum_{P_A} w_y/2`.
5. **Combine.** The total is at least
   `sum_{P_A} sqrt(w_x w_y) >= |P_A| sqrt(beta A) >= sqrt(beta/A)`. □

The rule cannot tell `a` from `b` in advance. It must refine thin boxes in
both directions, and AM–GM turns this into the `eps^(-1/2)` loss. The theorem
covers widest-side bisection (`beta = 1/2`), whose `Theta(eps^(-1/2))` count
on the scout's instance is now proved in both directions (Theorem 5.1(b) with
`p = 1`, and the spatial review's column bound). In `oblivious.log`
(40 values each of `a` and `b`, four oblivious rules), the sum times
`sqrt(eps)` stays between 4.0 and 6.8 from `eps = 10^-3` to `10^-6`. That is
23–73 times the proved bound, with a stable ratio for each rule.

### 5.3 Rules that use the relaxation solution or the incumbent

The practical point rule, in Speakman–Lee's parametrization, is

```
R(alpha, beta):  split at  clamp(alpha xhat_i + (1 - alpha) mid_i, [l_i + beta w_i, u_i - beta w_i]).
```

Speakman–Lee's Table 1 lists `(1, 0.2)` for SCIP, `(0.75, 0.1)` for
ANTIGONE, `(0.7, 0.01)` for BARON and `(0.25, 0.2)` for Couenne. These values
are not a faithful model of the solvers' current behaviour. The first version
of this note relied on them, and the review corrected this.

- **SCIP 10.** Checked here with PySCIPOpt 6.2.1 `getParam`: the defaults are
  `branching/midpull = 0.75`, `branching/midpullreldomtrig = 0.5` and
  `branching/clamp = 0.2`. The library's parameter text for `midpullreldomtrig`
  reads "multiply midpull by relative domain width if the latter is below
  this value".
  - The branching point is `midpull_B mid + (1 - midpull_B) xhat`, clamped to
    the middle 60%. Here `midpull_B = 0.75` on nodes whose relative width
    `r_B` is at least 0.5, and `0.75 r_B` below that.
  - So SCIP's weight on the relaxation point is `alpha_B = 0.25` on wide
    nodes and `1 - 0.75 r_B` on narrow ones. We call this rule `SCIPdef`.
  - The rule `R(1, 0.2)` is SCIP with `branching/midpull = 0`. It was labelled
    "SCIP(1,.2)" in the first version and is labelled `LP(1,.2)` from now on.
- **BARON.** BARON adopts the finite branching scheme of Shectman–Sahinidis.
  The branching point comes from an exhaustive rule such as bisection, "with
  the modification that the branching point is set to the incumbent whenever
  the latter lies in the current subdomain and is not one of the end-points
  of the interval of the selected branching variable. This renders the
  incumbent gapless"
  [[tawarmalani2002-convexification-and-global-optimization-in]] p.243.
  - We call this rule `INC`. In the fixed-incumbent model the incumbent is an
    optimal point. The implementation in `face_bb.py` tests only whether the
    incumbent's coordinate lies inside the interval, not whether the
    incumbent point lies in the node (remark after Proposition 5.4).
  - `R(0.7, 0.01)` models at most BARON's convex-combination formula
    [[tawarmalani2002-convexification-and-global-optimization-in]] p.215, not
    its incumbent rule.
- **Couenne.** `(0.25, 0.2)` is documented in
  [[belotti2009-branching-and-bounds-tightening-techniques]] p.18.
- **ANTIGONE.** The value `(0.75, 0.1)` comes only from Speakman–Lee and was
  not checked.

**Labels.**

- `LP(1, beta)` is the relaxation point with clamp `beta`.
- `R(alpha, beta)` has a fixed weight `alpha < 1`.
- `SCIPdef` is SCIP 10's box-dependent rule.
- `INC` is incumbent branching on top of bisection.

**Proposition 5.4 (exact face placement).** Consider the kink family
`f_{a,b}` of Section 5.

- (a) Every minimizer of the node relaxation over a box with
  `a in (l_x, u_x)` has `xhat = a`.
- (b) *Unclamped relaxation point.* `LP(1, 0)` with widest-side selection
  (ties to `x`) processes exactly 3 nodes, for every `a in (0,1)` and every
  `eps < |LB(root)|`.
- (c) *Clamped relaxation point.* Let `beta in (0, 1/2)`. The straddling
  `x`-intervals do not depend on `eps` or on the selection rule. Let `k0(a)` be
  the number of clamped `x` splits before the split lands at `a`, and let
  `K_beta` be the set of `a` for which this never happens (Proposition 5.5).
  For `a` not in `K_beta`, `LP(1, beta)` with widest-side selection (ties to
  `x`) processes at most `1 + 4 beta^(-(k0(a)+1))/(1 - beta)` nodes, for every
  `eps`. The count `k0(a)` is finite exactly off `K_beta`, and it is
  unbounded as `a` approaches `K_beta` or a clamp point.
- (d) *Incumbent branching.* `INC` with widest-side selection, ties broken
  toward `x`, and an optimal incumbent `(a, y*)`, processes exactly 3 nodes,
  for every `a in (0,1)` and every `eps < |LB(root)|`.

*Proof.*

- (a) For fixed `y`, the envelope is a maximum of two affine functions of `x`
  with slopes of absolute value at most `|c| max(b, 1 - b) < L`. So
  `f_B(., y)` is strictly decreasing for `x < a` and strictly increasing for
  `x > a`.
- (b) Boxes not straddling `a` are sub-boxes of the certificate of
  Theorem 4.4, hence valid and pruned. The root is a square, so `x` is split,
  at `xhat = a` by (a). Both children are pruned.
- (c)
  1. Since `xhat = a`, the `x` split point depends only on the current
     `x`-interval `I_k` and on `a`, and `y` splits do not change `I_k`.
  2. A clamped split replaces `I_k` by its outer part, of width `beta |I_k|`,
     that contains `a`. So `|I_k| = beta^k` for `k <= k0`, and the relative
     position `rho_k` of `a` in `I_k` evolves by
     `T(rho) = rho/beta` if `rho < beta` and `T(rho) = (rho - 1 + beta)/beta`
     if `rho > 1 - beta`. At `k0`, `rho_k0 in [beta, 1 - beta]`, the split is
     at `a`, and both children are pruned.
  3. This corrects the first version, which claimed that a clamped split
     keeps `D = min(a - l_x, u_x - a)`. In fact `D = beta^k min(rho_k, 1-rho_k)`
     can shrink much faster than `w_x`.
  4. At `x`-level `k`, widest-side selection splits `y` while
     `w_y > beta^k`. The `y` split point is at relative position
     `clamp(rho_k, [beta, 1-beta])` if `c < 0`, and
     `clamp(1 - rho_k, [beta, 1-beta])` if `c > 0`. Either way each child
     keeps at least `beta` of its parent's width. Boxes arriving from level `k - 1` have
     `w_y > beta^k`. Hence the level-`k` boxes that are split in `x` have
     `w_y in (beta^(k+1), beta^k]`.
  5. These boxes partition `[0,1]` in `y`, so there are at most
     `beta^(-(k+1))` of them. The `y`-split nodes at level `k` are internal
     nodes of binary trees whose leaves are these boxes, so there are fewer of
     them.
  6. Summing over `k <= k0`, there are at most
     `2 beta^(-(k0+1))/(1 - beta)` straddling nodes. All internal nodes of
     the tree are straddling, and a binary tree with `I` internal nodes has
     `1 + 2I` nodes, which gives the bound. (The first revision said that each
     straddling node has at most one non-straddling child. The final `x` splits
     at `a` have two, which is why the node identity is used instead.)
- (d) The root is a square and ties go to `x`, so `x` is selected. The
  incumbent coordinate `a` lies strictly inside `(0, 1)`, so the split is at
  `a`, and both children are pruned as in (b). □

*Remark on (d)* (from the recheck, confirmed in exact arithmetic in
`kink_exact_runs.log`). The counts below are for `a = 1/3`, and they are
identical for `a = 1/6` (`kink_exact_inc_a.log`).

- The tie rule matters. With ties toward `y` the root is split in `y`
  first. The count is then 7 when `y*` is interior. This needs
  `eps < min(y*, 1-y*) a(1-a)`, which holds for every tested `eps`.
- The quoted rule sets the branching point to the incumbent only when the
  incumbent *point* lies in the node. With ties toward `y` and `y* = 0` (an
  endpoint), the root is bisected in `y`. The child `[0,1] x [1/2,1]` then
  does not contain the incumbent and is bisected forever: 17, 49, 193, 513
  and 1537 nodes for `eps = 10^-2, ..., 10^-6`.
- So incumbent branching places the face only in nodes that contain the
  incumbent.
- The code's `INC` rule (`face_bb.py`) tests only whether the incumbent's
  *coordinate* lies strictly inside the interval. On `(a, 0)` with ties to
  `y` that version takes 7 nodes. The two tests agree on every run reported
  in Section 8.
- The `O(1)` statement is proved only for the kink family. For the faces of
  Theorem 4.5 a similar argument is plausible but not given.

*Remark (general 2D aligned segments).* Part (a) extends to the setting of
Theorem 4.4. Take `c > 0` and a box `B` with `a in (l_x, u_x)`.

- For fixed `y`, `x -> m(x, y)` is convex, and `x -> Gamma_B(x, y)`, a
  minimum of linear functions of `x`, is concave. So `m - Gamma_B` is convex
  in `x`.
- Its right derivative at `a` is at least
  `r_+(y) - c(y - l_y) >= c(l_y - L_y) >= 0`, by Theorem 4.4's bound on `r_+`.
- Its left derivative in the direction `-e_x` is at least
  `r_-(y) - c(u_y - y) >= 0`.

So `x = a` minimizes `f_B(., y)` for every `y`, and it does so uniquely when
these inequalities are strict. The case `c < 0` is symmetric. The relaxation
minimizer therefore lies on the optimal face. As Proposition 5.5 shows, it is
the clamp, not the minimizer, that can move the split off the face.

**Proposition 5.5 (clamping misses the face on a Cantor set).** This
counterexample is due to the face-exact review (Section 8.2); the proof is
re-derived here. Let `beta in (0, 1/2)`, and let `T` be the map of
Proposition 5.4(c).

- (i) Let `K_beta` be the set of `a in (0,1)` whose orbit under `T` stays in
  `[0, beta) ∪ (1 - beta, 1]` forever. For `a` in `K_beta`, `LP(1, beta)`
  never splits `x` at `a`, whatever the selection rule.
  - `K_beta` is uncountable and Lebesgue-null.
  - Its closure is the self-similar Cantor set of two maps of ratio `beta`,
    of Hausdorff dimension `log 2/log(1/beta)` (0.43 for `beta = 1/5`).
  - It contains rationals: `beta/(1 + beta)` is a point of period 2
    (`1/6 -> 5/6 -> 1/6` for `beta = 1/5`).
- (ii) Take `a = 1/6`, `beta = 1/5`, `c = -1`, `L = 2` and
  `b = sqrt(2) - 1`, and widest-side selection with ties to `x`. Then for
  `eps <= 1/7.2`, `LP(1, 1/5)` processes at least `0.0745 eps^(-1/2)` nodes,
  while `N_opt = 2`.

*Proof.*

- (i)
  1. The split is at `a` iff `rho_k in [beta, 1 - beta]`.
  2. The set of `a` that survive `k` clamped steps is a union of `2^k`
     intervals of length `beta^k`. Its measure `(2 beta)^k` tends to 0.
  3. The left branch of `T` maps `[0, beta)` onto `[0, 1)`, and the right
     branch maps `(1 - beta, 1]` onto `(0, 1]`; both are affine. Because the
     outer parts are half-open, an itinerary that ends in a constant run gives
     no point of `(0,1)`. Every other infinite sequence of choices (left or
     right outer part) gives a point, and distinct sequences give distinct
     points. There are uncountably many sequences that are not eventually
     constant. (Corrected after the recheck: the first revision said both
     branches map onto `[0,1)`.)
  4. The dimension is that of the attractor of two similarities of ratio
     `beta` under the open set condition.
  5. `T(1/6) = 5/6` and `T(5/6) = (5/6 - 4/5) 5 = 1/6`.
- (ii)
  1. From (i), the straddling intervals `I_k` have width `5^(-k)`, and
     `rho_k` alternates between `1/6` and `5/6`. All `x` splits are clamped.
  2. As in Proposition 5.7, the node bound of a straddling box is
     `-w_y (a - l_x)(u_x - a)/w_x = -(5/36) w_x w_y`. The relaxation
     minimizer has `yhat` at relative position `rho_k`, so `y` splits are
     clamped to relative position `1/5` or `4/5`.
  3. Let `k` be the largest integer with `5^(-2k) >= 7.2 eps`. At every
     level `k' < k`, the boxes with `w_y > w_x` are split in `y`. Their
     children have `w_y > (1/5) 5^(-k')` and bound magnitude above
     `(5/36)(1/5) 5^(-2k') >= 5 eps`, so they are processed.
  4. The level-`k'` boxes with `w_y <= w_x` also have `w_y > (1/5) w_x`. They
     are processed and split in `x`. Their straddling children at level
     `k' + 1` have bound magnitude above `(5/36) 5^(-2(k'+1)) >= eps`, so they
     are processed too.
  5. By induction, processed straddling boxes at level `k` cover `[0,1]`
     in `y`. There, boxes with `w_y > 5^(-k)` have bound magnitude above
     `(5/36) 5^(-2k) >= eps` and are split in `y`.
  6. Every child of a non-pruned node is processed. The level-`k` boxes with
     `w_y <= 5^(-k)` partition `[0,1]` in `y`, so at least `5^k` nodes are
     processed.
  7. Finally `5^k > (1/5)(7.2 eps)^(-1/2) = 0.0745 eps^(-1/2)`. □

*Remark (rate on the rest of `K_beta`; from the recheck).* The
`eps^(-1/2)` rate in (ii) uses the fact that the orbit of `1/6` stays at
relative positions `1/6` and `5/6`, bounded away from 0 and 1.

- Other points of `K_beta` can have long runs in one outer part. During such
  a run, every straddling box has a small bound, and for a range of `eps` the
  tree stops early.
- The recheck's exact counts for a run of 8 left steps show
  `N sqrt(eps)` as small as 0.0028.
- For itineraries with runs of unbounded length, `liminf N(eps) sqrt(eps) = 0`.
- What holds on all of `K_beta` is `N(eps) -> infinity`. The reason is the
  same as in step 4 of the proof of Proposition 5.6(a): some straddling box
  with a negative bound survives at every depth.

**Computations.**

- `kink_exact_runs.log` replays the rules in exact rational arithmetic.
- `clamp_cantor.log` replays twelve straddling intervals for `a = 1/6`
  exactly: every split is clamped. Its node counts come from a
  floating-point runner that agrees with the HiGHS-based `face_bb.py` on 45
  runs.

Node counts at `eps = 10^-2, ..., 10^-8` for `a = 1/6`:

| rule | nodes | arithmetic |
|---|---|---|
| `LP(1,.2)`, widest side, ties to `x` | 13, 39, 167, 547, 1513, 4917, 19537 (bound 0.7 ... 745) | exact |
| `LP(1,.2)`, widest side, ties to `y` | 15, 43, 173, 553, 1521, 4927 (to `10^-7`) | exact |
| `LP(1,.2)`, `x` only | 5, 9, 11, 13, 17, 19, 23 | exact |
| `LP(1,.2)`, product-score strong branching | 5, 9, 11, 13, 17, 19, 23 | floating point; reproduced exactly by the closing audit |
| `LP(1,0)`, `LP(1,.1)`, `INC` | 3 at every `eps` (`1/6` is not in `K_0.1`) | floating point |
| `SCIPdef`, widest side | 17, 47, 215, 215, 757, 4943, 15327 | floating point |
| bisection | 21, 61, 253, 765, 2045, 8189, 24573 | floating point |

The recheck reproduced the floating-point rows other than product-score
strong branching exactly in rational arithmetic. The closing audit reproduced
all rows, including that one, exactly in `Q(sqrt 2)`.

The first revision printed floating-point counts for the first row (13, 39,
169, 549, 1515, 4921, 19541). They exceed the exact ones because rounding
breaks some width ties `w_x = w_y` toward `y`.

Near clamp points the bound of Proposition 5.4(c) is finite but large. For
`a = 0.1999` (`k0 = 5`), `LP(1,.2)` needs 3, 527 and 19307 nodes (exact) at
`10^-4, 10^-6, 10^-8`.

**Proposition 5.6 (a fixed midpoint weight misses the face).** Let
`alpha < 1` be fixed, independent of the box.

- (a) For all but countably many `a`, and any selection rule, `R(alpha, beta)`
  never splits `x` exactly at `a`. So `N(f_{a,b}, eps) -> infinity` as
  `eps -> 0`.
- (b) If the selection always picks `x` at straddling nodes, then
  `N <= 1 + 2 ceil(log(|c|/(4 eps)) / log(1/(1 - beta')))`, where
  `beta' = max(beta, (1-alpha)/2)`.

*Proof.*

- (a)
  1. By Proposition 5.4(a), `xhat = a` at straddling nodes. So along any
     fixed sequence of decisions (variable, child, clamp case), every
     `x`-endpoint is an affine function `lambda a + mu` of `a` with
     `lambda in [0, 1)`.
  2. By induction: the root has `lambda = 0`. An unclamped split point has
     `lambda = alpha + (1 - alpha)(lambda_l + lambda_u)/2 < 1`. A clamped one
     has `lambda = (1 - beta) lambda_l + beta lambda_u < 1`.
  3. So "split point `= a`" has at most one solution per decision sequence.
     There are countably many sequences.
  4. Outside this set, some straddling box survives at every depth, and its
     bound is negative (step 1 of the proof of Theorem 5.3).
  5. The argument needs `alpha` constant. SCIP's default weight
     `alpha_B = 1 - midpull_B` depends on the relative width, so the endpoints
     become polynomials in `a` and step 1 no longer applies. Whether the
     countable-exception statement extends to `SCIPdef` is open.
- (b) `w_x` shrinks by a factor at most `1 - beta'` per `x` split, and a
  straddling box is pruned once `|c| w_x/4 <= eps`. The exact bound of a
  straddling box is `-|c| w_y (a - l_x)(u_x - a)/w_x`; see the proof of
  Proposition 5.7. □

Widest-side selection interleaves `y` splits, which double the straddling
column. In the computations on the scout's instance (`a = 1/3`), the
fixed-weight points `R(.75,.1)`, `R(.7,.01)` and `R(.25,.2)` with widest-side
selection grow like bisection, about `eps^(-1/2)`: 1581, 1983 and 2439 nodes
at `10^-6`. The relaxation point `LP(1,.2)` takes 3 nodes.

SCIP 10's default rule `SCIPdef` sits in between, since `alpha_B` rises to 1
as boxes shrink. It takes 15, 51, 167, 723 and 913 nodes at
`eps = 10^-2, ..., 10^-6` with widest-side selection, and 7, 11, 11, 11 and 19
with `x`-only selection (`rules_table_j.jsonl`). These match the review's
independent emulation. A real SCIP 10 run in the review took 5, 11 and 35
nodes at gaps `10^-5, 10^-6, 10^-7`, with its root propagation active.

**Proposition 5.7 (strong branching with the min score can be worse than
bisection).**

- Instance: the scout's `f_{1/3, sqrt(2)-1}` (`L = 2`, `c = -1`).
- Rule: Couenne's point `R(1/4, 1/5)`, with the branching variable chosen to
  maximize the smaller of the two child bounds.

For `eps < D = 45/3136`, the number of processed nodes is at least
`2D/eps - 1 = 0.0287/eps - 1`. This compares with `N_opt = 2` and with
`Theta(eps^(-1/2))` for bisection.

*Proof.*

1. **Bound of a straddling box.** For a straddling box,
   `LB = -w_y (a - l_x)(u_x - a)/w_x`. By Proposition 5.4(a),
   `xhat = a`. At `X = 0` the envelope is
   `max(-X_u (Y - Y_l), |X_l| (Y - Y_u))`. It is minimized at
   `Y - Y_l = rho w_y`, where `rho = (a - l_x)/w_x`, with value
   `-X_u |X_l| w_y/w_x`. So `yhat` has relative position `rho` in its range.
2. **The choice depends only on `rho`.** Both candidate split points have the
   relative position `pi = clamp(rho/4 + 3/8, [1/5, 4/5])`.
   - An `x` split leaves one pruned child and one straddling child with bound
     `-w_y w_x rho(pi - rho)/pi` (if `rho < pi`) or
     `-w_y w_x (rho - pi)(1 - rho)/(1 - pi)` (if `rho > pi`).
   - A `y` split gives two children with bounds `-r w_y w_x rho(1 - rho)`,
     for `r = pi` and `r = 1 - pi`.

   All four quantities scale with `w_y`. So the comparison depends only on
   `rho`, and a `y` split does not change `rho`.
3. **The path.** Exact rational arithmetic (`q3_order.log`, part B) gives the
   straddling sequence `rho = 1/3, 8/11, 5/13, 40/49`. Here `x` wins at the
   first three nodes. At `rho = 40/49` the `y` split wins:
   `-0.008310 w_y` against `-0.009908 w_y`.
4. **The column.** From the box `[49/192, 539/1536] x [0,1]` on, only `y` is
   split. Every descendant has bound `-w_y D` with `D = 45/3136`, so the
   column's leaves have `w_y <= eps/D`. There are at least `D/eps` of them,
   hence at least `2D/eps - 1` nodes. □

In the computations:

- this rule used 44965 nodes at `10^-6` on the scout's instance (bound
  28699);
- on the smooth transversal `diag` instance it grew like `eps^(-1)`
  (599, 3855, 32651);
- on a random 4-variable box QP with an interior minimizer (`boxqp4s2c`) it
  exceeded 20000 nodes at `10^-3`.

With the product score `max(Delta_1, 10^-9) max(Delta_2, 10^-9)`, the same
point rule grows only logarithmically (9, 15, 21, 27, 33 nodes on the scout's
instance). *Relaxation-point selection without a width safeguard* also failed
on `boxqp4s2c`. There the "most central `xhat`" selection exceeded 60000
nodes at `10^-3`, while widest-side and product-score selections stayed below
2100 nodes at `10^-6`. The score and the selection matter polynomially, not
just the point.

### 5.4 Answer to Q2

- **Bisection against optimal.**
  - The loss is a constant factor in the smooth transversal regime
    (Section 5.1).
  - It is `Theta(eps^(-p/2))` for aligned sharp `p`-strata. For `p = 1`:
    about `2000` nodes against 2 leaves at `10^-6`.
  - For strata at angle `theta` it is at most `O(theta^(-1/2))`. The upper
    bound follows from Theorem 5.1(b) and Proposition 3.13. The matching
    behaviour of bisection is observed numerically in Section 8, not proved.
- **Practical point rules.**
  - The *unclamped* relaxation point locates aligned strata in the kink
    family exactly (Proposition 5.4(b)).
  - With a clamp (`LP(1, beta)`, `beta > 0`) the count stays bounded except
    on a Lebesgue-null Cantor set of instances, and the bound blows up near
    that set (Propositions 5.4(c) and 5.5). On the set the count tends to
    infinity.
    - For `a = 1/6` it grows at least like `eps^(-1/2)` with widest-side
      selection.
    - No uniform rate holds on the set. Points whose orbit has arbitrarily
      long runs in one outer part have `liminf N(eps) sqrt(eps) = 0`
      (recheck, Section 2).
  - A fixed midpoint weight (`alpha < 1`) misses the face for all but
    countably many instances (Proposition 5.6). The loss is then
    `log(1/eps)` or about `eps^(-1/2)`, depending on the selection.
  - SCIP's default, box-dependent weight is not covered by these results.
    Numerically it lies between the two regimes.
  - Min-score strong branching combined with a biased point loses at least a
    factor of order `1/eps` against `N_opt = 2` (Proposition 5.7).
- **The solver mechanism that realizes the `O(1)` certificates** on the
  kink family is branching at the incumbent, the finite branching scheme of
  Shectman–Sahinidis adopted in BARON (Proposition 5.4(d)).
  - Once an optimal incumbent is known, the split lands on the optimal face
    in every node that contains the incumbent, with no clamp.
  - This takes 3 nodes on `kink` and 7 on `kinkT` (Section 8.4), with ties to
    `x`.
  - The `INC` counts on `tilt(0.03)` and `diag` equal bisection's exactly
    (1747 and 4091 at `10^-6`). The reason is that the incumbent used there,
    `(1/2, 1/2)`, is the root centre, so every incumbent split is also a
    bisection split. Other incumbents were not tested. At a transversal
    stratum, an incumbent fixes only the face positions through one point, so
    no large gain is expected.
- **Is some rule within a constant or log factor of optimal?**
  - For oblivious rules, no (Theorem 5.3).
  - For the clamped relaxation point with widest-side selection, no:
    Conjecture 5.8 below is false (Proposition 5.5). It is also far from
    `N_opt` on nearly aligned strata: 694, 384 and 782 leaves on
    `tilt(theta)` at `10^-6` for `theta = 0.3, 0.03, 0.003`, against
    `N_opt = 274, 88, 28`.
  - Relaxation-point splitting with product-score strong branching stayed
    within a factor 2.6 of `N_opt` on the three `tilt` instances, was
    logarithmic on `a = 1/6`, and took 3 nodes on `kink`. Whether it is
    uniformly competitive is Question 5.9.

**Conjecture 5.8 (withdrawn: false).** The first version conjectured that
`R(1, beta)` (`beta > 0`) with widest-side selection has
`|T| <= C(instance) log(1/eps) N_opt(eps)` on box-constrained bilinear
problems. Proposition 5.5(ii) refutes it: for `a = 1/6` and `beta = 1/5`,
`|T| >= 0.0745 eps^(-1/2)` while `N_opt = 2`.

**Question 5.9.** Is there a rule that is uniformly competitive, with
`|T| <= C(n, coefficient bounds) polylog(1/eps) N_opt(eps)`? The candidate
suggested by the computations is relaxation-point splitting with
product-score strong branching, possibly combined with incumbent branching.

The scout's conjecture was that no node-local rule is within
`polylog(1/eps)` of `N_opt`.

- It is proved for oblivious rules (Theorem 5.3).
- It is proved for the clamped relaxation point with widest-side selection
  (Proposition 5.5).
- It is proved for min-score strong branching with Couenne points
  (Proposition 5.7, loss at least of order `1/eps`).
- It holds numerically for fixed-weight points with widest-side selection on
  the kink (growth about `eps^(-1/2)`), and for widest-side selection of any
  point on the near-aligned family `tilt(theta)`, `theta -> 0`.
- It is open for relaxation-point splitting with product-score strong
  branching (Question 5.9).

## 6. Convergence order does not determine node counts

Bompadre and Mitsos call a scheme of relaxations *pointwise convergent of
order `beta`* if `sup_{x in B} (f - f_B) <= tau w(B)^beta` for boxes of
width `w(B)`. They show that McCormick relaxations and alphaBB are second
order. The cluster-problem analyses (Du–Kearfott, Wechsung et al.,
Kannan–Barton) turn order and prefactor into *upper* estimates of the number
of boxes near a minimizer.

**Theorem 6.1.**

- (a) **Order gives upper bounds.** Theorem 5.1 and Proposition 5.2 use only
  the second-order condition. So every second-order scheme has bisection
  counts `O(integral (m+eps)^(-n/2))` under (QD), and `O(eps^(-p/2))` at
  sharp `p`-strata. The same proof gives
  `O(integral (m + eps)^(-n/beta))` for order `beta` under the analogue of
  (QD) with `|x - y|^beta`.
- (b) **Order and prefactor do not give lower bounds.** On the scout's
  instance `f = 2|x - a| - (x - a)(y - b)`, with `a = 1/3` and
  `b = sqrt(2) - 1`:
  - Termwise McCormick is order 2, with `sup_D Gamma = s^2/4` on squares of
    side `s`. `N_opt(eps) = 2` for all `eps >= 0` (Theorem 4.4).
  - alphaBB with `alpha = 1/2`, the smallest uniform value that convexifies
    `-(x-a)(y-b)`, is order 2 with the *same* prefactor:
    `sup_D alpha q_D = s^2/4`. Yet
    `N_opt(eps) = Theta(eps^(-1/2))`.
  - The scheme `McCormick - kappa min(x - l_x, u_x - x)` with `kappa = 0.2` is
    only *first*-order: its gap is at least `kappa w_x/2` at the center. Yet
    `N_opt(eps) = 2`.
- (c) **When order does predict.** Consider a transversal Morse–Bott stratum
  of dimension `p` with (QD). McCormick has
  `N_opt = Theta(eps^(-p/2))` by Theorems 3.6, 3.8 and 5.1. alphaBB has the
  same by the scout's Theorems D and C. So the two second-order schemes agree.

*Proof of (b).*

- McCormick: Theorem 4.4.
- alphaBB:
  - The lower bound is the scout's Theorem D, which the spatial review found
    correct. Take `S = {a} x [0,1]`, `p = 1`, `eta = 0`, `c_S = 1`,
    `n = 2`. Then `N_cov >= (1/2)(alpha/(4 eps))^(1/2) / 4 = 0.088/sqrt(eps)`.
  - The upper bound is Theorem 5.1(b) with `m >= 1.41 |x - a|`.
- First-order scheme:
  - It is convex, because it adds `max(-kappa(x - l_x), -kappa(u_x - x))` to
    a convex function. It lies below `f`, and its gap vanishes on the faces
    `x = l_x` and `x = u_x`.
  - On `{x >= a}`, its gap is at most `(x - a)(1 - y) + 0.2 (x - a)`. This
    is at most `(2 - (y - b))(x - a) = m` whenever `1.2 <= 2 + b`. The left
    box is symmetric.
  - A grid check (`q3_order.log`, part A) confirms that `gap - m <= 0` on
    both boxes for both face-exact schemes. □

The computations agree. Splitting at the relaxation solution with McCormick
takes 3 nodes at every `eps`. The same rule with alphaBB takes 19, 91, 315,
699 and 3003 nodes for `eps = 10^-2, ..., 10^-6`. Widest-side bisection takes
the same counts for both schemes (21, ..., 2045). Bisection cannot exploit
face exactness, because it never places a face at `x = a`.

**Why order does not suffice.** Order is a sup-norm statement over boxes
shrinking around a point. Node counts depend on *where* the gap vanishes: on
faces for McCormick, at vertices for alphaBB. They also depend on how the
near-optimal set sits relative to that zero set (transversal or aligned), and
on the growth of `m` across it. Section 3 bounds counts below through
transversal strata, concave slices and near-optimal boxes. Section 4 shows
that alignment plus the automatic linear growth gives bounded counts.
Kannan–Barton already observed that first-order schemes can avoid clustering
in constrained problems when `f` grows linearly. They also report that
Wechsung's thesis (Section 2.3) shows first-order convergence "may be
sufficient to mitigate the cluster problem in unconstrained optimization when
the optimizer sits at a point of nondifferentiability of the objective
function" [[kannan2017-the-cluster-problem-in-constrained]] p.2.

The kink minimizers are such points, so the first-order part of
Theorem 6.1(b) is anticipated there. What is new is the comparison: two
schemes with the same order and the same prefactor differ polynomially in
`N_opt`, because they have different gap-zero sets.

## 7. Conjectures and open problems

- **Conjecture 7.1 (withdrawn: false).** The first version conjectured
  `N_opt(eps) = Theta~(eps^(-p*/2))` for box-constrained bilinear problems.
  Here `p*` was the largest dimension of a `tau`-nondegenerate `C^1`
  submanifold of the *optimal set*. Example 3.12(b) refutes this. Its optimal
  set is one aligned segment, so `p* = 0` and the prediction is
  `O(log(1/eps))`, yet `N_opt >= 1/(2 sqrt(eps))`. An earlier draft that used
  the largest *transversal* dimension had already been refuted by
  Proposition 4.7.
- **Conjecture 7.1' (withdrawn: false).** The first revision conjectured
  `N_opt(eps) <= C polylog(1/eps) L(eps)`, where `L(eps)` is the best lower
  bound from Theorems 3.4, 3.6 and 3.8 and Proposition 3.10 applied to the
  near-optimal sets `{m <= eta}`. Proposition 3.14, due to the recheck,
  refutes it. That instance has `L(eps) = O(eps^(-3/4))`, yet
  `N_cov >= 0.307/(eps (1 + ln(1/(2 eps))))`.
- **Question 7.1'' (open).** Add row-slice bounds (Proposition 3.14(c)), or
  a curved version of Theorem 3.6, to `L`. Is `N_opt` then within
  `C polylog(1/eps)` of `L`, with `C` and the polylog degree depending on the
  instance and termwise McCormick relaxations?
  - The only evidence is the examples of this note. No upper bound is known
    for the instance of Proposition 3.14.
  - The lesson of Example 3.12 and Proposition 3.14 is that the exponent is
    set by near-optimal sets at scale `eps`, including curved,
    non-transversal ones, and not by the optimal set.
- **Open 7.2 (beyond Theorem 4.5).** Suppose the optimal set near a face
  `{x_K = a_K}` equals that face, with `K` a vertex cover that does not
  satisfy the single-neighbour condition. Does an `O_n(1)` certificate exist?
  - Proposition 4.7 does not decide this, because its optimal set is larger
    than the face.
  - Example 3.12(b) shows that a proper subset of a vertex-cover face
    (`K = {x}`) can be expensive.
- **Open 7.3 (multilinear degree `>= 3`).** The lower bounds hold for joint
  vertex-polyhedral envelopes through Lemmas 2.3 and 2.4 (Theorems 3.4 with
  `k = 1`, 3.6 and 3.8). The structure results (Theorem 4.2) need `phi`
  affine along the stratum. Multilinear `phi` is affine along axis
  directions, so Lemma 4.1 still gives constant `g'`. The rate is then
  `grad phi.u`, which is affine in the axis coordinate. An analogue of
  Theorem 4.4 for a trilinear term is plausible but not checked.
- **Open 7.4 (constraints with lifted variables).** In pooling, validity at
  feasible points is not necessary for pruning (Lemma 1.2). A lower-bound
  theory needs a certificate notion that accounts for relaxed feasibility.
  The Haverly instances run here are all solved in at most 9 nodes by every
  rule, so they do not discriminate between rules.
- **Open 7.5 (competitive rules).** Question 5.9.
  - Conjecture 5.8 is false (Proposition 5.5).
  - The first version claimed that a counterexample to Conjecture 5.8 was
    impossible in 2D for full segments. That was wrong: the relaxation
    minimizer does lie on the face (remark after Proposition 5.4), but the
    clamp moves the split off it.
  - Incumbent branching and product-score strong branching are the remaining
    candidates.
- **Open 7.6 (gaps left by the review).**
  - Proposition 4.6(a) for polyhedral `Q`.
  - Whether Proposition 5.6(a) extends to SCIP's box-dependent weight.
  - A matching `O(eps^(-1/2))` upper bound in Proposition 5.5(ii). The counts
    suggest `Theta`.
  - Whether a log loss is needed in Corollary 3.3 under (QD).

## 8. Computations

### 8.1 Setup

The code lives in this directory:

- `face_bb.py` is the branch-and-bound;
- `instances.py` defines the instances;
- `rules_table.py`, `rules_table2.py`, `rules_sp.py` and `tilt_focus.py` are
  the drivers.

Node model:

- The lifted relaxation of Section 1.1 is solved exactly as an LP or convex
  QP with HiGHS 1.15. It runs single-threaded with tolerances `10^-10`,
  retries at `10^-8` and `10^-7`, and a 5-second limit per solve. If HiGHS
  fails, Clarabel via cvxpy is used; it agrees with HiGHS to `1.0e-11` on 120
  random QP boxes (`crosscheck.log`). One Clarabel solve in the box-QP run
  returned "optimal_inaccurate" and was accepted (`rules_table_e.err`).
- The `tilt` family uses an exact closed-form bound: golden section on the six
  segments that carry the minimum. It agrees with the QP to `1.2e-13` on 450
  boxes. It replaced the QP after HiGHS stalled on some tiny `tilt` boxes.
- `oblivious.py` uses a closed-form bound for the kink family. It agrees with
  the LP to `2.2e-16` on 600 boxes.

Run model:

- The incumbent is fixed at `f*`, so the processed set does not depend on
  node order.
- A node counts as processed when its relaxation is solved.
- Counts are floating-point illustrations, not certified counts.
- For rules that use `xhat`, counts can depend on which relaxation minimizer
  the solver returns when it is not unique. For example, `LP(1,.2)c` on
  `tilt(0.3)` at `10^-6` gave 1699 nodes with the QP solver and 1737 with the
  exact bound.

The code reproduces the scout's counts on the kink instance:

- widest-side bisection: 21, 61, 253, 765, 2045;
- `x`-only bisection: 11, 17, 25, 31, 37;
- relaxation point: 3.

Rules:

- `bisect`: widest side relative to the root, at the midpoint.
- `xonly`: bisect `x` only.
- `R(alpha, beta)` with the Speakman–Lee point, for `(alpha, beta)` in
  `(1, .2)`, `(.75, .1)`, `(.7, .01)` and `(.25, .2)`.
  - `(1, beta)` is written `LP(1, beta)`: the relaxation point with clamp
    `beta`. `LP(1,.2)` is SCIP with `branching/midpull = 0`, not default
    SCIP.
  - The fixed weights are the Speakman–Lee table values. They do not model
    the ANTIGONE or BARON solvers (Section 5.3).
  - The first version's labels `SCIP(1,.2)`, `ANTIG(.75,.1)`,
    `BARON(.7,.01)` and `COUEN(.25,.2)` are kept as keys in the `.jsonl`
    files. `make_tables.py` and `make_condensed.py` print the new labels.
- `SCIPdef`: SCIP 10's default point rule (midpull 0.75, multiplied by the
  relative width below 0.5, clamp 0.2).
- `INC`: incumbent branching (Shectman–Sahinidis), which bisects unless the
  optimal incumbent's coordinate is strictly inside the interval. The code
  applies this *coordinate* test. The quoted rule also requires the
  incumbent point to lie in the node; the two tests agree on every reported
  run (remark after Proposition 5.4).
- The branching variable is chosen among the variables of violated terms by
  one of:
  - `w`: widest;
  - `x`: always `x`;
  - `c`: most central `xhat`;
  - `s`: strong branching maximizing the smaller child bound;
  - `sp`: strong branching maximizing the product of the two bound gains.

### 8.2 Condensed results

Processed nodes at `eps = 10^-4 / 10^-6` (relative `eps` for the box QP and
pooling instances). "LB" is the proved lower bound on the number of leaves;
any tree has at least `2 LB - 1` nodes. Full tables are in
`rules_tables.log`.

The lower bounds come from:

- `kink`, `kinkT`: `N_opt = 2`, exactly (Theorem 4.4);
- `tilt`: Proposition 3.13;
- `diag`: Theorem 3.6;
- `iso`: Theorem 3.4 with `k = 1`;
- `aligned_quad`: Example 3.12.

| instance | LB leaves 1e-4 / 1e-6 | bisect | LP(1,.2)w | LP(1,.2)sp | R(.75,.1)w | R(.7,.01)w | R(.25,.2)w | R(.25,.2)sp | R(.25,.2)s |
|---|---|---|---|---|---|---|---|---|---|
| kink | 2.0 / 2.0 | 253 / 2045 | 3 / 3 | 3 / 3 | 89 / 1581 | 75 / 1983 | 199 / 2439 | 21 / 33 | 407 / 44965 |
| kinkT | 2.0 / 2.0 | 251 / 1019 | 7 / 7 | 3 / 3 | 167 / 1235 | 201 / 1499 | 223 / 1015 | 15 / 31 | 1601 / cap |
| sharp_pt | – / – | 21 / 29 | 3 / 3 | 3 / 3 | 11 / 19 | 11 / 19 | 19 / 27 | 19 / 25 | 19 / 31 |
| iso | 2.7 / 4.2 | 29 / 49 | 21 / 37 | 19 / 33 | 21 / 39 | 21 / 41 | 29 / 45 | 25 / 49 | 71 / 789 |
| diag | 70.7 / 707.1 | 507 / 4091 | 391 / 4035 | 391 / 4035 | 451 / 4379 | 459 / 4551 | 491 / 4971 | 491 / 5095 | 599 / 32651 |
| tilt(0.3) | 27.4 / 273.9 | 195 / 1887 | 119 / 1387 | 127 / 1251 | 107 / 1311 | 155 / 1443 | 207 / 1799 | 139 / 1583 | - / - |
| tilt(0.03) | 8.7 / 86.6 | 195 / 1747 | 131 / 767 | 55 / 383 | 131 / 1419 | 147 / 1479 | 187 / 2071 | 51 / 471 | - / - |
| tilt(0.003) | 2.7 / 27.4 | 31 / 1775 | 35 / 1563 | 23 / 143 | 43 / 1471 | 39 / 1715 | 31 / 1923 | 35 / 179 | - / - |
| aligned_quad | 50.0 / 500.0 | 757 / 6645 | 985 / 9919 | 463 / 4265 | 865 / 9299 | 879 / 9285 | 891 / 9995 | 463 / 4265 | 463 / 4265 |
| boxqp4s1c | – / – | 57 / 89 | 31 / 37 | 33 / 37 | 29 / 39 | 29 / 39 | 37 / 53 | 27 / 45 | 39 / 175 |
| boxqp4s2c | – / – | 1093 / 2039 | 865 / 1651 | 609 / 1207 | 931 / 1753 | 879 / 1639 | 845 / 1633 | 847 / 1725 | - / - |
| haverly3q | – / – | 9 / 9 | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 |

**What the computations support.**

- **Proved bounds are respected.** Every count satisfies
  `nodes >= 2 LB - 1`.
- **Rates.**
  - `diag` and `aligned_quad` grow by a factor of 2.7–3.2 per decade under
    every balanced rule (`eps^(-1/2)` would give 3.16).
  - `iso` and `sharp_pt` grow additively (`log(1/eps)`) or are constant.
  - On `kink` and `kinkT` (`a = 1/3`), the relaxation point `LP(1,.2)` stays
    at 3 to 7 nodes, while bisection and the fixed-weight points grow like
    `eps^(-1/2)`. For `a = 1/6`, `LP(1,.2)` grows too (Proposition 5.5,
    Section 8.4).
- **Smooth regime.** The balanced rules (bisection, and `w` or `sp`
  selection with any point) are within a factor 1.5 of each other on `iso`
  and `diag`. On the box QPs they are within a factor 3, with bisection the
  slowest. This is consistent with Proposition 5.2.
- **Near-alignment.** For `theta = 0.3, 0.03, 0.003`, `N_opt` at `10^-6` is
  274, 88 and 28 leaves (Proposition 3.13).
  - Bisection does not benefit: 1887, 1747 and 1775 nodes.
  - Neither does any point rule with widest-side selection: `LP(1,.2)w`
    takes 1387, 767 and 1563 nodes.
  - Relaxation-point splitting with product-score strong branching takes
    1251, 383 and 143 nodes, that is 2.3, 2.2 and 2.6 times `N_opt` in
    leaves.
  - So the loss of bisection and of widest-side rules grows as `theta -> 0`
    (Section 5.4).
- **Strong branching.**
  - With the min score and Couenne's point `R(.25,.2)` it is the outlier
    everywhere:
    `kink` 44965 nodes (Proposition 5.7 bound 28699), `diag` 32651, `iso`
    789, `boxqp4s2c` more than 20000 at `10^-3`.
  - With the min score and the relaxation point `LP(1,.2)` it also grows like
    `1/eps` on
    `tilt(0.03)` (283 nodes at `10^-4`, 2915 at `10^-5`).
  - With the product score it stays within a factor 1.25 of bisection
    everywhere. It is the best rule on `aligned_quad` (4265 against 6645 for
    bisection) and on all `tilt` instances.
- **Theorem 4.5 and Proposition 4.7.**
  - In 300 random *tight* star instances (3D single star and 4D double star,
    with rates vanishing at box corners), the orthant certificate's node
    bounds are at least `-4.4e-16` (`star_check.log`).
  - The two-center instance `path3` grows like `1/eps`: 241, 2353 and 24497
    bisection nodes, against the proved `0.102/eps`
    (`path3_check.log`).
- **Selection without a width safeguard.** The central-`xhat` selection `c`
  exceeded 60000 nodes at `10^-3` on `boxqp4s2c`, although it was harmless on
  the 2D instances.
- **Pooling and bilinear box QPs.** Haverly 1–3, the two-pool Haverly variant
  (`f* = -500`) and the zero-diagonal random box QPs are solved in at most 9
  nodes by every rule. These instances do not discriminate between rules.
  - The bilinear box QPs are pruned at the root. Their optima are vertices,
    where McCormick is exact.
  - In `haverly3q` the pool quality upper bound is raised to 3.3, so the
    optimal quality 1.5 is no longer a dyadic point. There bisection needs 9
    nodes against 3 for every `R(alpha, beta)` rule.

### 8.3 Commands

All commands were run from this directory, `research-20260928b/bb-complexity/spatial-face-exact/`,
with Python 3.13, HiGHS 1.15.1 and SciPy 1.18.0.

| Command | Output | Checks |
|---|---|---|
| `python3 gap_checks.py` | `gap_checks.log` | Lemma 2.1 formula against the vertex-LP envelope (max error `2.9e-13`, 2000 boxes). Bounds of Lemma 2.1(c,d). Lemmas 2.3 and 2.4 on 400 random multilinear functions (`n = 4`, degree `<= 3`; zero violations; min ratios 1.09 and 1.07). Termwise gap `>=` joint gap. `J(s)` closed form against quadrature (Lemma 3.1). |
| `python3 rules_table.py kink kinkT sharp_pt iso` | `rules_table_a.jsonl` | Rules on aligned, sharp and isolated instances |
| `python3 rules_table.py diag aligned_quad` | `rules_table_c.jsonl` | `diag` complete. `aligned_quad` stopped at `LP(1,.2)w`, `10^-6`, on a HiGHS QP failure, before the fallback existed |
| `python3 rules_table.py aligned_quad` | `rules_table_d.jsonl` | `aligned_quad`, all rules (rerun) |
| `python3 tilt_focus.py 0.3`; `python3 tilt_focus.py 0.03 0.003` | `rules_table_b.jsonl`, `rules_table_f.jsonl` | `tilt` with the exact bound. Both runs were stopped during min-score strong branching at `10^-6`, which is slow; `theta = 0.003` was not reached |
| `python3 tilt_focus.py 0.003 --no-minscore` | `rules_table_h.jsonl` | `tilt(0.003)`, all rules except min-score strong branching |
| `python3 rules_table2.py haverly1 haverly2 haverly3 haverly3q haverly1_2pool boxqp5s0b boxqp5s1b boxqp4s0c boxqp4s1c boxqp4s2c` | `rules_table_e.jsonl` | Pooling and box QPs |
| `python3 rules_sp.py` | `rules_table_g.jsonl` | Product-score strong branching on the 2D instances |
| `python3 oblivious.py 40` | `oblivious.log` | Theorem 5.3 and the closed-form bound cross-check |
| `python3 tilt_certificate.py` | `tilt_certificate.log` | Proposition 3.13, upper construction |
| `python3 q3_order.py` | `q3_order.log` | Theorem 6.1(b) and the exact path of Proposition 5.7 |
| `python3 integral_bound.py` | `integral_bound.log` | Theorem 3.2 on `diag`: valid but weak, at most 9 leaves against the Theorem 3.6 bound 707 and 2018 leaves found |
| `python3 crosscheck.py` | `crosscheck.log` | Solver cross-checks |
| `python3 star_check.py` | `star_check.log` | Theorem 4.5 in tight 3D/4D star instances, and a control showing that the root alone is not valid |
| `python3 path3_check.py` | `path3_check.log` | Proposition 4.7: invalid orthant boxes and `1/eps` growth |
| `python3 make_tables.py > rules_tables.log`; `python3 make_condensed.py` | `rules_tables.log`, Section 8.2 | Tables |

In the table, "-" means not run. Min-score strong branching was not run on
`tilt` at `10^-6`, nor with the point `R(.25,.2)` on `tilt`, and it was stopped after
the cap on `kinkT` and `boxqp4s2c`.

**Superseded runs.** The first `tilt` runs used the HiGHS QP. They stalled on
some tiny boxes and were stopped, and their output was overwritten by the
exact-bound runs. Two short exploratory commands, a trace of the
strong-branching decisions and a timing probe, are not recorded as logs.
Their content is reproduced by `q3_order.py` (part B) and by the table
runs.

### 8.4 Revision reruns (2026-09-29)

These runs were added after the review. They use the same code, with three
new point rules in `face_bb.py` (`SCIPdef`, `INC` and the `x`-only
selection). The rules and results of the earlier runs are unchanged.

| instance | LB leaves 1e-4 / 1e-6 | bisect | LP(1,.2)w | LP(1,.2)sp | SCIPdef w | INC w | LP(1,0)w |
|---|---|---|---|---|---|---|---|
| kink | 2.0 / 2.0 | 253 / 2045 | 3 / 3 | 3 / 3 | 167 / 913 | 3 / 3 | 3 / 3 |
| kinkT | 2.0 / 2.0 | 251 / 1019 | 7 / 7 | 3 / 3 | 59 / 371 | 7 / 7 | 7 / 7 |
| tilt(0.03) | 8.7 / 86.6 | 195 / 1747 | 131 / 767 | 55 / 383 | 151 / 1027 | 195 / 1747 | - / - |
| iso | 2.7 / 4.2 | 29 / 49 | 21 / 37 | 19 / 33 | 21 / 41 | 41 / 69 | - / - |
| diag | 70.7 / 707.1 | 507 / 4091 | 391 / 4035 | 391 / 4035 | 427 / 4099 | 507 / 4091 | - / - |
| aligned_quad | 50.0 / 500.0 | 757 / 6645 | 985 / 9919 | 463 / 4265 | 923 / 9883 | 875 / 7147 | - / - |
| box_aligned | 50.0 / 500.0 | 1227 / 12115 | 1199 / 12389 | 531 / 3939 | 1177 / 12455 | 1309 / 15213 | - / - |
| box_alignedK2 | 50.0 / 500.0 | 757 / 6645 | 985 / 9921 | 463 / 4265 | 913 / 9821 | 875 / 7147 | - / - |

What the reruns support:

- **Counterexample A** (`box_aligned` and `box_alignedK2`, Example 3.12(b)).
  Every rule grows like `eps^(-1/2)` and stays above the proved
  `1/(2 sqrt(eps))` leaves. The bisection counts 69, 301 and 1227 at
  `10^-2 ... 10^-4` equal the review's independent Clarabel runs.
- **SCIP 10's default point** (`SCIPdef`).
  - On `kink` it takes 15, 51, 167, 723 and 913 nodes, equal to the review's
    emulation. That is between `LP(1,.2)` (3) and fixed `alpha = 0.25`
    (2439 at `10^-6`).
  - On `tilt(0.03)`, `diag`, `iso` and `aligned_quad` it is within a factor
    1.4 of `LP(1,.2)`.
- **Incumbent branching** (`INC`).
  - It takes 3 nodes on `kink` and 7 on `kinkT`, at every `eps`.
  - On `tilt(0.03)` and `diag` it matches bisection exactly. The incumbent
    used, `(1/2, 1/2)`, is the root centre, so every incumbent split is a
    bisection split.
  - On `iso`, `aligned_quad` and `box_aligned` it is up to 1.4 times worse
    than bisection.
- **Clamped relaxation point** (`clamp_cantor.log` and `kink_exact_runs.log`,
  Proposition 5.5):
  - `a = 1/6` is replayed exactly;
  - `LP(1,.2)w` stays above `0.0745 eps^(-1/2)` at every `eps` down to
    `10^-8`;
  - the floating-point runner agrees with `face_bb.py` on all 45 runs;
  - the exact rational counts equal the recheck's (13, 39, 167, 547, 1513,
    4917, 19537).
- **Proposition 4.7, upper bound** (`path3_quadtree.log`). Every quadtree
  leaf has an LP bound `>= -eps`, and leaves times `eps` stays between 6.1
  and 13.0. The recheck certified every leaf in exact arithmetic and confirmed
  the constant 0.10212 and the count `<= 1 + 18/eps`.
- **Second revision** (after the recheck):
  - `curved_check.log` verifies the curved counterexample of
    Proposition 3.14: closed-form maximization, `f >= 0`, `f = 0` on the
    surface, growth ratio 0.123 against the required 1/12, convexity of `G`,
    the row-slice inequality on 16209 boxes, `A = 0.6148`, and the lower bound
    against the Theorem 3.6 (`p = 2`) bound.
  - `kink_exact_runs.log` gives the exact counts and the incumbent tie-rule
    tests.

Commands, run from this directory:

| Command | Output | Checks |
|---|---|---|
| `python3 -c "import pyscipopt; m = pyscipopt.Model(); print([m.getParam(p) for p in ('branching/midpull', 'branching/midpullreldomtrig', 'branching/clamp')])"`, and `strings` on `libscip` for the parameter text | console | SCIP 10.0 defaults 0.75, 0.5, 0.2, and the documented meaning of `midpullreldomtrig` |
| `python3 clamp_cantor.py` | `clamp_cantor.log` | Propositions 5.4(c) and 5.5: exact replay for `a = 1/6`, runner cross-check, counts, `k0(a)` near clamp points |
| `python3 revision_runs.py A` | `rules_table_i.jsonl` | Example 3.12(b) (counterexample A), both variants |
| `python3 revision_runs.py B` | `rules_table_j.jsonl` | `SCIPdef`, `LP(1,0)` and `INC` on the Section 8 instances |
| `python3 path3_quadtree.py` | `path3_quadtree.log` | Proposition 4.7(b) upper bound and (d) optimal set |
| `python3 curved_check.py` | `curved_check.log` | Proposition 3.14 (counterexample to Conjecture 7.1'), second revision |
| `python3 kink_exact_runs.py` | `kink_exact_runs.log` | Exact rational counts for `a = 1/6` and `a = 0.1999`; incumbent branching with both tie rules and both tests, second revision |
| `python3 make_tables.py > rules_tables.log`; `python3 make_condensed.py rev` | `rules_tables.log`, the table above | Tables with the new labels |

## 9. Literature comparison

Only sources in the local library were read for this note. No web search was
done in this workstream. **An unsuccessful search does not establish
novelty.** The interval-analysis literature on box counts (Ratschek–Rokne,
Csendes, Neumaier 2004 Section 15) and the branching-point literature before
2009 (Liu–Sahinidis–Shectman 1996, the omega rule) were not examined.

- **Bompadre–Mitsos 2012** ("Convergence rate of McCormick relaxations"; not
  in the local library).
  - Known here through the summary in Kannan–Barton: second-order pointwise
    convergence of convex and concave envelopes of `C^2` functions and of
    alphaBB, and propagation rules for McCormick composition
    [[kannan2017-the-cluster-problem-in-constrained]] p.2.
  - Relation: Lemma 2.5 is the trivial bilinear case. Theorem 6.1 shows that
    their order, even with the prefactor, determines only upper bounds on node
    counts.
- **Kannan–Barton 2017.**
  - They define convergence orders for lower-bounding schemes in constrained
    problems [[kannan2017-the-cluster-problem-in-constrained]] p.5.
  - They show that first-order schemes can remove clustering when `f` grows
    linearly [[kannan2017-the-cluster-problem-in-constrained]] p.41. They
    derive upper estimates of box counts from order and prefactor.
  - Our results add lower bounds and identify the missing parameter: the gap's
    zero set and the transverse growth.
  - Theorem 4.2 explains when linear growth is automatic along aligned
    optimal strata: in 2D (Theorem 4.4) and at faces fixing star centres
    (Theorem 4.5), but not in general (Example 3.12(b)).
  - They also report Wechsung's thesis result that first-order schemes may
    suffice at nondifferentiable unconstrained minimizers
    [[kannan2017-the-cluster-problem-in-constrained]] p.2. This anticipates the
    first-order part of Theorem 6.1(b). The new part there is the comparison
    at equal order and prefactor.
- **Wechsung–Schaber–Barton 2014; Du–Kearfott 1994.**
  - Wechsung et al. assume the minimizer sits at a box center, and note that
    if it coincides with a vertex, "an exponential number of boxes will
    contain this minimizer" [[wechsung2014-the-cluster-problem-revisited]] p.2.
  - For face-exact relaxations the opposite holds. Placing the near-optimal
    set on gap-free faces is what makes certificates small (Theorems 4.4, 4.5;
    Propositions 3.13, 5.4). Placement relative to the relaxation's zero set,
    not order or prefactor, decides whether clustering occurs.
- **Speakman–Lee 2018.**
  - They parametrize practical branching points as
    `clamp(alpha xhat + (1-alpha) mid, [a + beta w, b - beta w])` and tabulate
    reported defaults: SCIP `(1, .2)`, ANTIGONE `(.75, .1)`, BARON
    `(.7, .01)`, Couenne `(.25, .2)`
    [[speakman2018-on-branching-point-selection-for]] p.2-3.
  - They qualify the table themselves. SCIP "(mostly)" uses the relaxation
    point, and "especially in BARON" other factors, including available
    incumbents, supersede the formula
    [[speakman2018-on-branching-point-selection-for]] p.3.
  - The first version of this note used the table as a model of the
    solvers. That was wrong for SCIP 10 (Section 5.3: midpull 0.75, scaled
    below relative width 0.5) and for BARON (incumbent branching).
  - They choose points for one trilinear monomial by the volume of the child
    hulls, and note that this is a local proxy with no node-count guarantee
    [[speakman2018-on-branching-point-selection-for]] p.22-23.
  - Relation: Propositions 5.4–5.7 are, as far as we found, the first
    node-count statements about these parameters:
    - the unclamped relaxation point places faces on aligned strata exactly;
    - with a clamp it misses them on a Lebesgue-null Cantor set of instances;
    - a fixed weight `alpha < 1` misses them for all but countably many
      instances.

    Theorem 5.3 bounds oblivious rules. Volume criteria cannot see these
    effects, since they ignore where the near-optimal set lies.
- **Belotti et al. 2009 (Couenne).**
  - Couenne uses the LP-midpoint combination with `alpha = 0.25` and
    `beta = 0.2` to balance subproblem difficulty
    [[belotti2009-branching-and-bounds-tightening-techniques]] p.18.
  - Their experiments conclude that no single strategy dominates, that "the
    LP point should always be taken into account", and that points should
    stay away from the bounds
    [[belotti2009-branching-and-bounds-tightening-techniques]] p.29-30.
  - Propositions 5.4–5.7 give a mechanism for the first conclusion and show
    that the weight on the LP point matters polynomially on aligned instances.
  - They also describe branching at a known local optimum, following
    Shectman–Sahinidis, with a convexification "exact at the new bounds"
    [[belotti2009-branching-and-bounds-tightening-techniques]] p.18. This is
    the mechanism of Proposition 5.4(d).
  - They also report that setting product branching points to 0 when near 0
    helps. This places a face at a special value. By Lemma 2.1 it makes the
    gap vanish on `{x_i = 0}`, which helps when near-optimal points lie
    there.
- **Tawarmalani–Sahinidis 2002** (book).
  - BARON branches at a convex combination of the relaxation solution (omega
    rule) and the midpoint, "to induce exhaustiveness", because branching at
    the relaxation solution alone is not exhaustive
    [[tawarmalani2002-convexification-and-global-optimization-in]] p.215.
  - They also state that BARON adopts the finite branching scheme of
    Shectman–Sahinidis: "the branching point is set to the incumbent whenever
    the latter lies in the current subdomain and is not one of the end-points
    ... This renders the incumbent gapless"
    [[tawarmalani2002-convexification-and-global-optimization-in]] p.243.
  - This incumbent rule is exactly the "put a face on the optimum" mechanism,
    and Proposition 5.4(d) turns it into a node count: 3 nodes on the kink
    family. The first version of this note claimed that BARON's default
    misses the optimal face. That claim is withdrawn.
  - What our results do show concerns the convex-combination part alone. A
    fixed midpoint weight gives up exact face placement for all but countably
    many instances (Proposition 5.6). A clamp on the relaxation point gives it
    up on a Cantor set of instances (Proposition 5.5).
- **Tawarmalani–Sahinidis 2004; Rikun 1997.**
  - Convex envelopes of multilinear functions on boxes are vertex polyhedral
    [[rikun1997-a-convex-envelope-formula-for]] p.1.
  - Rikun also gives an example where the termwise ("standard")
    linearization error grows like `(n^2 - n)/8` while the joint envelope error
    is `(n - 1)/8` [[rikun1997-a-convex-envelope-formula-for]] p.1.
  - Our lower bounds hold for both the joint and the termwise envelopes. The
    joint versions use the weaker Lemma 2.3.
- **Al-Khayyal–Sherali 2000; Shectman–Sahinidis 1998** (finite termination
  when branching at relaxation solutions or incumbents).
  - The papers were not examined. Shectman–Sahinidis's scheme is known here
    through Tawarmalani–Sahinidis p.243 and Belotti et al. p.18. Branching at
    the incumbent so that it becomes gapless is their mechanism. Proposition
    5.4(d) adds only a node count for it on the kink family, and
    Propositions 5.5 and 5.6 show what happens without it.
  - Proposition 4.6(b) gives a necessary condition for any finite McCormick
    certificate: linear growth along every feasible concave direction at every
    minimizer.
  - Theorems 4.4 and 4.5 give sufficient conditions of a different kind. The
    comparison with their hypotheses is open.
- **Standard ingredients.**
  - Lemma 4.1 is the fact that normal cones, hence subdifferentials, are
    constant on the relative interior of a face of `epi g` (Rockafellar,
    *Convex Analysis*; not in the library).
  - The Minkowski–Radon centroid bound and the Dirichlet integral of
    Lemma 3.1 are classical.
- **SCIP 10 documentation.** The parameters `branching/midpull`,
  `branching/midpullreldomtrig` and `branching/clamp` and their descriptions
  were read from PySCIPOpt 6.2.1 and the SCIP 10.0 library (Section 5.3).
- **Al-Khayyal–Falk 1983; McCormick 1976.**
  - The McCormick inequalities, and the fact that they give the convex
    envelope of a bilinear term on a rectangle, are used in Lemma 2.1.
  - Al-Khayyal–Falk was not examined.
    [[mccormick1976-computability-of-global-solutions-to]] is in the library.
- **Leads not examined.**
  - Epperly–Pistikopoulos 1997 (reduced-space branching), related to the
    vertex-cover view and `tau*`.
  - Schöbel–Scholz 2010 and Scholz 2012 (convergence rates of geometric
    branch-and-bound).
  - Falk–Soland 1969.
  - Tuy 1991 and Horst–Tuy (omega-subdivision versus bisection in concave
    minimization, the older form of the branching-point question).
- **Dey–Santana–Wang 2019.** They propose non-axis ("hyperbola/parabola")
  branching for bipartite bilinear programs
  [[dey2019-new-socp-relaxation-and-branching]] p.1-3. Our theory is for
  axis-parallel branching. Transversality is defined relative to coordinate
  subspaces, so non-axis branching changes the invariant.
- **Closest known mechanisms** (as the program requires).
  - Bachoc–Cesari–Gerchinovitz (arXiv:2102.01977; via the scout):
    Lipschitz certificate integrals, with a `1/(1+log)` loss in the lower
    bound. Theorem 3.2 is the McCormick analogue. Its per-box integral is
    finite only below the natural exponent, and the loss is `log^(2k)`, of
    which one log is necessary (Corollary 3.3(b)).
  - Dey–Dubey–Molinaro: lower bounds on general branch-and-bound trees by
    adversarial families [[dey2023-lower-bounds-on-the-size]] p.1-7.
    Theorem 5.3 uses an averaging argument over an instance family of the
    same general kind, for a much narrower rule class (oblivious rules).
  - Cheng–Basu 2026 (misleading local scores in MILP; via the scout, not
    examined). Proposition 5.7 is a spatial example of a score that locks into
    the wrong variable.

**Known or anticipated, and credited above:**

- the McCormick gap formulas (Lemma 2.1);
- Lemma 4.1;
- the branch-at-the-optimum mechanism (Shectman–Sahinidis, BARON);
- first-order sufficiency at nondifferentiable minimizers (Wechsung's
  thesis);
- the row-slice bound and the curved example of Proposition 3.14 (the
  recheck of this note).

**What appears new, subject to the incomplete search:**

- the vertex-cover and independent-set description of McCormick gap-zero
  sets used for node counts;
- transversality and gap-nondegeneracy as sufficient conditions for lower
  bounds (Theorems 3.6 and 3.8, Proposition 4.7), with a sharp constant on
  one example;
- the product-form certificate integral (Lemma 3.1, Theorem 3.2);
- the fractional vertex cover exponent (Corollary 3.11);
- the aligned-segment certificates, with sharpness automatic in 2D
  (Theorems 4.2, 4.4 and 4.5);
- node-count statements for practical branching-point rules
  (Theorem 5.3, Propositions 5.4–5.7);
- the separation of convergence order from node counts at equal order and
  prefactor (Theorem 6.1(b)).

These are transfers of the scout's covering arguments, which the spatial
review classified as transfers of Lipschitz and bandit arguments. The new
ingredient is the independent-set and vertex-cover geometry.

## 10. Checks run

All checks are targeted. They are listed with their outputs in Section 8.3.

- Lemma checks: `python3 gap_checks.py`.
- Branch-and-bound tables:
  - `python3 rules_table.py ...`, `python3 rules_table2.py ...`,
    `python3 rules_sp.py` and `python3 tilt_focus.py ...`;
  - summarized with `python3 make_tables.py` and `python3 make_condensed.py`.
- Theorem-specific checks: `python3 oblivious.py 40`,
  `python3 tilt_certificate.py`, `python3 q3_order.py`,
  `python3 integral_bound.py`, `python3 star_check.py` and
  `python3 path3_check.py`.
- Solver cross-checks: `python3 crosscheck.py`.
- Second revision (after the recheck): `python3 curved_check.py` and
  `python3 kink_exact_runs.py`.
- Revision after review (2026-09-29): `python3 clamp_cantor.py`,
  `python3 revision_runs.py A`, `python3 revision_runs.py B`,
  `python3 path3_quadtree.py`, the SCIP parameter query, and
  `python3 make_tables.py > rules_tables.log` (Section 8.4).

These are floating-point computations, not certified proofs. The only
exact-arithmetic checks are:

- the rational replays in `q3_order.py` (part B) and `clamp_cantor.py`
  (part A);
- the rational branch-and-bound in `kink_exact_runs.py`.

No project-wide checks were run, CI was not inspected, and nothing was
committed. Other workstreams' files were not modified.

## 11. Revision after review

The independent review
([`../../reviews/face-exact-review.md`](../../reviews/face-exact-review.md),
scripts in `../../reviews/face-exact/`) confirmed the gap lemmas, the lower
bounds, the tilted-stratum constant, the structure theorems, the
oblivious-rule bound and the strong-branching bound. It found the errors
below. Each fix was re-derived here, not copied, and the affected
computations were rerun with this directory's own code (Section 8.4).

1. **Proposition 5.4(b) was false, and Conjecture 5.8 (formerly 5.7) is
   false.**
   - The old proof claimed that a clamped split keeps `D`. It does not:
     `D = beta^k min(rho_k, 1 - rho_k)`.
   - Proposition 5.4 is restated:
     - (b) the unclamped relaxation point takes 3 nodes;
     - (c) with a clamp the count is bounded by
       `1 + 4 beta^(-(k0+1))/(1-beta)` off the Cantor set `K_beta`, and this
       bound blows up near it;
     - (d) incumbent branching takes 3 nodes.
   - The clamped counterexample (`a = 1/6`, `beta = 1/5`, at least
     `0.0745 eps^(-1/2)` nodes, `N_opt = 2`) is the new Proposition 5.5, with
     credit to the review. The old Open 7.5 claim that such a counterexample
     is impossible in 2D is withdrawn.
   - Propositions 5.5 and 5.6, Conjecture 5.7 and Question 5.8 of the first
     version are now numbered 5.6, 5.7, 5.8 and 5.9.
2. **Conjecture 7.1 is false.** Example 3.12(b) is the review's
   counterexample A: a box-constrained aligned segment with quadratic growth
   and `N_opt >= 1/(2 sqrt(eps))`. Two claims are restricted accordingly:
   "aligned strata in box-constrained problems automatically have linear
   growth" now holds for `n = 2` and for faces fixing star centres, and
   "quadratic growth needs constraints" is withdrawn. Conjecture 7.1'
   measured exponents on near-optimal sets at scale `eps`. It was itself
   withdrawn in the second revision (below).
3. **Solver defaults.**
   - SCIP 10 uses `midpull = 0.75`, scaled by the relative width below 0.5,
     and `clamp = 0.2`. This was verified here with PySCIPOpt and the library
     parameter text.
   - The rule `R(1, 0.2)` is SCIP with `midpull = 0`. It is relabelled
     `LP(1,.2)` throughout, and SCIP's default rule is added as `SCIPdef`.
     Proposition 5.6 is stated for fixed weights only.
   - BARON branches at the incumbent when it lies inside the domain
     (Tawarmalani–Sahinidis p.243, Shectman–Sahinidis). The claim that
     BARON's default misses the optimal face is withdrawn. Incumbent
     branching is now discussed as the solver mechanism that realizes the
     `O(1)` certificates (Proposition 5.4(d), `INC` runs).
4. **Smaller fixes.**
   - Proposition 4.6(a) is restricted to `F = X0`.
   - Proposition 4.7 now records the full optimal set, includes the review's
     `O(1/eps)` quadtree construction (re-derived and checked, with credit),
     and states `Theta(1/eps)`. Its wording now says that the condition of
     Theorem 4.5 concerns the fixed coordinates. The path `x1 - y - x2` is
     itself a star.
   - `tau` is no longer called the exact invariant.
   - Example 3.12(a) now notes that one RLT product prunes it at the root.
   - "(R) holds for a matching" now reads "perfect matching".
   - Corollary 3.3(b) now notes that its example violates (QD).
   - Lemma 1.2 lists the pointwise-weaker relaxations it covers, and the
     child bounds, auxiliary-variable branching and tolerance-accepted
     incumbents it does not.
5. **Novelty.** Section 9 credits:
   - Lemma 4.1 as standard convex analysis;
   - the branch-at-the-optimum mechanism to Shectman–Sahinidis;
   - the first-order observation of Theorem 6.1(b) to Wechsung's thesis, as
     reported by Kannan–Barton p.2.

   The novelty list was narrowed.

**Not changed** (confirmed by the review): Lemmas 2.1–2.5, Theorems 3.2, 3.4,
3.6 and 3.8, Lemmas 3.7 and 3.9, Proposition 3.10, Corollaries 3.3(a), 3.5
and 3.11, Proposition 3.13, Theorems 4.2, 4.4 and 4.5, Corollary 4.3 (apart
from the matching fix), Theorems 5.1 and 5.3, Proposition 5.2 and Theorem 6.1.

### Second revision (after the recheck)

The recheck
([`../../reviews/face-exact-recheck.md`](../../reviews/face-exact-recheck.md),
scripts in `../../reviews/face-exact-recheck/`) confirmed:

- the revised Propositions 5.4(a)–(c) and 5.5;
- Example 3.12(b);
- Proposition 4.7, with every quadtree leaf certified in exact arithmetic.

It found the following, all fixed here:

1. **Conjecture 7.1' is false.** Its curved variant of Proposition 4.7 is
   now Proposition 3.14, with credit.
   - I re-derived the proof, including the growth constant and the `p = 2`
     bound.
   - I checked it numerically with my own code (`curved_check.log`).
   - Conjecture 7.1' is withdrawn. Question 7.1'' asks whether adding
     row-slice bounds restores a characterization.
2. **Proposition 5.4(c), proof.** The final `x` splits have two
   non-straddling children. The count now uses `nodes = 1 + 2 * internal`.
   The `y` split sits at relative position `1 - rho` when `c > 0`.
3. **Proposition 5.5(i), step 3.** The right branch maps onto `(0, 1]`, and
   the proof now uses itineraries that are not eventually constant.
4. **Exact counts.**
   - The first-revision `LP(1,.2)` counts were floating-point; width ties
     were broken by rounding. The exact counts, 13, 39, 167, 547, 1513, 4917
     and 19537, and 19307 for `a = 0.1999`, were reproduced independently in
     `kink_exact_runs.log`, and the table is labelled by arithmetic.
   - Section 5.4 no longer claims an `eps^(-1/2)` rate on all of `K_beta`.
     That rate is proved for `a = 1/6`. On the whole set the proved statement
     is `N -> infinity`, and `liminf N sqrt(eps) = 0` for suitable points
     (remark after Proposition 5.5).
5. **Proposition 5.4(d).**
   - It now states the tie rule (ties to `x`).
   - A remark covers the difference between the coordinate test and the
     point test, with exact counts (7 nodes with ties to `y`; 17, 49, 193,
     513, 1537 with ties to `y`, incumbent `(a, 0)` and the point test).
   - The equality of `INC` and bisection on `tilt(0.03)` and `diag` is now
     attributed to the centre incumbent.
   - The `O(1)` claim is limited to the kink family.
6. **Example 3.12(b)** is now stated as `Theta(eps^(-1/2))`, with the upper
   bound from Theorem 5.1(a). Proposition 4.7 cites the recheck's exact
   certification.

Commands added in this revision: `python3 curved_check.py` and
`python3 kink_exact_runs.py` (Section 8.4). No other reruns were needed.

### Closing audit

The closing audit
([`../../reviews/closing-audit-b.md`](../../reviews/closing-audit-b.md),
item 3) found the second revision correct. It confirmed:

- Proposition 3.14, with `A = 0.614769` in closed form;
- every exact kink count, including the product-score strong-branching row,
  which it reproduced exactly in `Q(sqrt 2)`.

It suggested two optional edits, both made:

- The remark on Proposition 5.4(d) now states that its counts are for
  `a = 1/3`. It also gives the condition `eps < min(y*, 1-y*) a(1-a)` for the
  count 7.
- The strong-branching row cites the audit's exact reproduction.

I confirmed that the incumbent counts are identical at `a = 1/6`:
`python3 -c "... kink_exact_runs.run ..."` for `a = 1/3` and `1/6`, both tie
rules, both incumbents and both tests, logged in `kink_exact_inc_a.log`.
