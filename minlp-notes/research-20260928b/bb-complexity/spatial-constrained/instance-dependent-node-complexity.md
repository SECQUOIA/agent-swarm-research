# Instance-dependent node complexity of spatial branch-and-bound with constraints

Date: 2026-09-28. Workstream `spatial-constrained/` of the
[program](../PROGRAM.md). Status: first draft. It consolidates the scout's
Lemma 0 and Theorems A–D
([scout report](../../scouting/spatial-bb-theory.md), Sections 2–3) with the
corrections of the [independent review](../../reviews/spatial-bb-review.md),
and adds a constrained theory. The new results (Sections 4–8) were reviewed
in [`reviews/spatial-constrained-review.md`](../../reviews/spatial-constrained-review.md).
That review found no counterexample and listed 17 corrections. All are made,
and Section 13 lists them. A
[recheck](../../reviews/spatial-constrained-recheck.md) found the six
substantive revisions correct and listed five minor points, fixed in Section
13.1. Those last edits have not been rechecked. Computations are floating-point illustrations, not certified
counts. Scripts and logs are in this directory.

## Summary

The question is how many leaves a spatial branch-and-bound tree needs to
certify an `eps`-optimal value, as a function of `eps` and of the instance,
when node bounds come from convex relaxations. The answer below is stated for
relaxation schemes whose gap at feasible points is at least `alpha q_B`, where
`q_B(y) = sum_i (y_i-l_i)(u_i-y_i)`. That class includes uniform alphaBB and
secant relaxations of separable concave terms. The upper bounds need only
standard second-order pointwise convergence.

Proved here (complete proofs, unreviewed unless stated):

1. **Corrected unconstrained package (Sections 2–3).** Lemma 0 and Theorems
   A–D of the scout, with the review's fixes. Reduction pieces are split per
   round. The corollary is restricted to same-relaxation tightening. The (QD)
   sufficient condition is corrected, and the constants in the comparison
   between bisection and the optimum are stated honestly.
2. **Key lemma (Lemma 4.1).** For every box `B` and every `d`-dimensional
   `C^1` submanifold `S`,
   `integral_{S∩B} q_B^(-d/2) dσ <= (pi^2/d)^(d/2) binom(n,d)^(1/2) sum_I M^I(S)`.
   Here `M^I(S)` is a coordinate multiplicity: the largest number of points of
   `S` on one coordinate `(n-d)`-flat, counting only points where the flat is
   transversal. The tools (Cauchy–Binet, the area formula with multiplicity,
   Federer's reach inequality) are standard geometric measure theory. The new
   part is the per-box arcsine bound. Bounded curvature alone does **not**
   suffice: a flat comb with infinitely many components, and also a connected
   spiral of bounded curvature, have an unbounded integral (Proposition 4.4).
   The right hypothesis is positive reach, which makes the multiplicity 1 at
   scale `~ reach` (Lemma 4.2).
3. **Stratified lower bounds (Theorems 4.5, 4.6).** They hold for every
   adaptive tree, any node order and any valid incumbent, with constraints.
   - Integral form: for every feasible stratum `S` of dimension `d`,
     `N_opt(eps) >= c(n,d,S) alpha^(d/2) integral_S (f-f*+eps)^(-d/2) dσ`.
   - Covering form: `N_opt(eps) >= 2^(-n) N_inf(E(eta), 2 sqrt((eps+eta)/alpha))`,
     where `E(eta)` is the set of `eta`-optimal feasible points.
4. **Constraint-gap schemes (Section 5).** Relaxations whose only gap comes
   from loosened nonconvex constraints obey a tube dichotomy. It produces lower
   bounds from slightly infeasible points whose objective value is below
   `f* - eps`.
   - An isotropic loosening forces `Theta(eps^(-1/2))` leaves on a flat optimal
     segment. An anisotropic loosening of the same constraint has a 3-leaf
     certificate for every `eps`.
   - Under an outward-descent condition, a constraint gap `beta` gives the
     same covering lower bounds as an objective gap
     `alpha_eff = mu_0 beta/(12 c_1)` (Theorem 5.4). This is a one-directional
     transfer of lower bounds, not an equivalence of the two gaps.
   - Kannan–Barton (2017, Section 3.2) already identified clustering on nearly
     feasible infeasible points as a mechanism, with upper estimates. The
     lower-bound form here is new as far as the bounded search found.
   - At a KKT point with a relaxed active constraint and an active stratum of
     dimension `d >= 1`, constraint-gap schemes need `Omega(log(1/eps))`
     leaves, even with the objective relaxed exactly (Theorem 5.7).
5. **Upper bounds and characterization (Section 6).** Assume second-order
   pointwise convergence, an error bound for the constraints and a Lipschitz
   objective. Then uniform bisection processes at most
   `C_0 + C_1 sum_j N_j(E(Lambda s_j^2))` nodes. Combined with item 3:
   - `N_opt(eps)` and bisection are within `C log(1/eps)` of
     `Phi_alpha(eps) = sup_{eta >= 0} N_inf(E(eta), 2 sqrt((eps+eta)/alpha))`
     (Theorem 6.3). Here `E(eta)` is the set of `eta`-optimal feasible points.
     Within a factor `2^n`, `Phi_alpha(eps)` is the **running supremum over
     `eta >= eps`** of the parabolic covering numbers
     `N_inf(E(eta), 2 sqrt(eta/alpha))`. Up to constants, these form Munos's
     near-optimality profile for the semi-metric `alpha |x-y|_inf^2`.
   - The supremum over coarser levels is necessary. Covering the
     `eps`-optimal set at scale `sqrt(eps)` alone does not determine `N_opt`
     with uniform constants: `K` separated near-optimal local minima force
     `N_opt >= K/2^n`, while that single-scale covering number stays `O(1)`
     (Remark 6.3a).
   - Under stratified regularity,
     `N_opt(eps) ≍ |T_bis| ≍ sum_S integral_S (f-f*+eps)^(-dim S/2) dσ`
     (Theorem 6.7).
6. **Regular instances (Section 7).**
   - Finitely many nondegenerate KKT minimizers (LICQ, SC, SOSC) whose active
     strata have dimension `d >= 1`: `N_opt ≍ |T_bis| ≍ log(1/eps)`, with
     lower-bound prefactor `(alpha/M_L)^(d/2)`. This is a rigorous form of Neumaier's heuristic
     "`n` replaced by `n-a`".
   - Unique vertex minimizer (`d = 0`): `N_opt = O(1)` for every `eps >= 0`, while
     bisection needs `Theta(log(1/eps))` for generic positions.
   - Morse–Bott optimal manifold of dimension `p`: `Theta(eps^(-p/2))`.
7. **Consequences (Section 8).**
   - The `eps`-exponent is half the box-counting dimension of the optimal set.
   - Active constraints matter through the stratum that carries the optimal
     set. The full-dimensional integral can predict the wrong exponent.
   - Same-relaxation bound tightening saves at most a `log(1/eps)` factor.
   - First-order gaps give exponent `(n+p)/2` instead of `p/2`. This includes
     an `eps^(-n/2)` lower bound for the cluster effect at nondegenerate
     minima, valid for every adaptive tree.

Computations (Section 9) with a toy spatial branch-and-bound on circle, sphere
and ball constrained problems confirm the exponents `0` (logarithmic), `1/4`,
`1/2` and `1`. The ratio of bisection leaves to the proved lower bound is
stable across `eps` (about 30–45 in 2D and 100–120 in 3D). The ball instances
follow the boundary-stratum prediction, not the full-dimensional integral.

Open (Section 11):
- the log factor between `N_opt` and bisection for a *local* branching rule
  (workstream `branching-competitiveness/`);
- whether bisection's prefactor depends on the stratum dimension `d` rather
  than `n` (a conjecture);
- whether constraint propagation removes the constraint-gap lower bounds on
  curved strata;
- Lemma 5.5 for nonlinear exactly kept constraints (sketched only);
- face-exact relaxations (workstream `spatial-face-exact/`).

**Novelty (Section 10).** As the review found, Theorems B, D, A and C transfer
known Lipschitz and bandit arguments to a relaxation-gap model.
- The Lipschitz precedents are Hansen–Jaumard–Lu (1991), Perevozchikov (1990),
  Munos (2011) and Bachoc–Cesari–Gerchinovitz (2021).
- Neumaier (2004, Section 15) gives the heuristic MINLP precedent.
The claim defended here is narrower: rigorous lower bounds for
relaxation-based spatial branch-and-bound with adaptive trees and constraints.
It includes:
- the per-box arcsine bound and its stratified form (Lemma 4.1, which
  otherwise uses standard geometric-measure-theory tools);
- the covering characterization up to `log(1/eps)` for constrained problems;
- the lower-bound form of the tube dichotomy for constraint-gap schemes.
  Kannan–Barton (2017, Section 3.2) is the precedent for clustering on nearly
  feasible points, with upper estimates.
These were not found in the sources checked. An unsuccessful search does not
establish novelty.

### Result status

| Item | Content | Status |
|---|---|---|
| Lemma 2.1 | leaves and removed pieces form a valid family | proved (corrected per review) |
| Theorems 3.1–3.5 | scout's B, D, A, C (unconstrained) | proved; review confirmed B, D, A, C proofs |
| Lemma 3.6 | corrected (QD) sufficient condition | proved (review's statement) |
| Lemma 4.1 | key lemma (multiplicity form) | proved |
| Lemmas 4.2–4.3 | reach or graph bound gives local multiplicity 1 | proved |
| Proposition 4.4 | multiplicity cannot be dropped; curvature is not enough | proved |
| Theorem 4.5 | stratified integral lower bound | proved |
| Theorem 4.6 | covering lower bound | proved |
| Lemma 5.1, Theorem 5.2 | tube dichotomy; infeasible-side lower bound | proved |
| Example 5.3 | isotropic vs anisotropic flat constraint gap | proved; numerics agree |
| Theorem 5.4, Lemma 5.5, Proposition 5.6 | Lagrangian transfer (covering form; (OD) near KKT points with `P_ex` polyhedral; integral form with a shift map) | proved; the extension to nonlinear exact constraints is sketched only |
| Theorem 5.7 | `log(1/eps)` lower bound at KKT points for constraint-gap schemes | proved |
| Lemma 6.1, Theorems 6.2–6.4, 6.6–6.7, Corollary 6.5, Remark 6.3a | bisection upper bounds; covering and integral characterizations; running-supremum form and failure of a single-scale version; dimension formula | proved |
| Proposition 6.8 | `O(1)` certificate at a sharp constrained minimizer | proved |
| Theorems 7.1–7.2 | KKT and Morse–Bott rates | proved |
| Corollary 8.1, Theorem 8.2 | bound tightening; first-order relaxations | proved, (d) written out in the revision (the integral form in 8.2(e) has a log loss) |
| Section 11, item 2 | bisection prefactor depends on `d`, not `n` | conjecture |

## 1. Model

### 1.1 Problem and notation

- Root box `X0 = prod_i [L_i, U_i] subset R^n`; `s0 = max_i (U_i - L_i)`.
- Problem `min f(y)` subject to `y in F`, where
  `F = {y in X0 ∩ P_ex : g_j(y) <= 0 (j <= m), h_k(y) = 0 (k <= r)}`.
  `P_ex` is a closed set of constraints that every node relaxation keeps
  exactly (for example linear constraints, or none: `P_ex = R^n`). The
  functions `f, g_j, h_k` are continuous on `X0`. `F` is compact and nonempty,
  and `f* = min_F f`.
- Optimality gap `m(y) = f(y) - f*`, so `m >= 0` on `F`. Sublevel sets
  `E(eta) = {y in F : m(y) <= eta}` for `eta >= 0`. Optimal set
  `M = E(0) = argmin_F f`.
- Violation `v(z) = max(0, max_j g_j(z), max_k |h_k(z)|)` for
  `z in X0 ∩ P_ex`. So `F = {z in X0 ∩ P_ex : v(z) = 0}`.
- For a box `B = prod_i [l_i, u_i] subset X0`:
  `a_i(y) = (y_i - l_i)(u_i - y_i)`, `q_B(y) = sum_i a_i(y)`, width
  `w(B) = max_i (u_i - l_i)`. `d_i(y) = min(y_i - l_i, u_i - y_i)` is the
  distance to the nearer endpoint in coordinate `i`. Two facts are used
  throughout:
  - `a_i(y) >= d_i(y)^2`;
  - `a_i(y) <= d_i(y) (u_i - l_i)`.
- `Q(x, r) = {y : |y - x|_inf <= r}` is the closed sup-norm ball: a cube of
  side `2r`. `N_inf(A, delta)` is the least number of closed cubes of side
  `delta` covering `A`. `H^d` is `d`-dimensional Hausdorff measure, and `dσ`
  is its restriction to a `d`-dimensional set.

### 1.2 Node model

A node is a box `B subset X0`. Its relaxation consists of:

- a set `R_B` with `R_B ⊇ F ∩ B`, contained in `B ∩ P_ex` (validity);
- a function `f_B` on `R_B` with `f_B <= f` on `F ∩ B`.

The node bound is `LB(B) = inf_{R_B} f_B`, with `LB(B) = +inf` if `R_B` is
empty. For relaxations in lifted variables, `f_B(y)` means the projected value
`inf{t : (y, w, t) in lifted relaxation}`.

- **Incumbent and tolerance.** Branch-and-bound keeps an incumbent value
  `UBD >= f*` and prunes `B` when `LB(B) >= UBD - eps`, with `eps >= 0`.
  Pruning by infeasibility is the case `LB(B) = +inf`. A relative tolerance
  reduces to this: pruning when
  `LB >= UBD - max(eps_abs, eps_rel |UBD|)`, with `eps_rel <= 1`, implies
  `LB >= f* - max(eps_abs, eps_rel |f*|)` (review, Section 1.1). The
  theorems then apply with `eps := max(eps_abs, eps_rel |f*|)`. Incumbents
  accepted within a feasibility tolerance can give `UBD < f*`; then `f*` must
  be read as the optimal value of the tolerance-relaxed problem.
- **Exact arithmetic** is assumed; floating-point infeasibility verdicts are
  outside the model.

### 1.3 Certificates

A **certificate at tolerance `eps`** is a finite family `P` of boxes with
pairwise disjoint interiors covering `X0` such that every `C in P` has
`LB(C) >= f* - eps`. Pruning with any incumbent `UBD >= f*` implies this.
`N_opt(eps)` is the least size of a certificate. It is at most the number of
leaves of any terminated branch-and-bound tree without bound tightening, for
any branching rule, split points, node order and valid incumbent. Lemma 2.1
extends the comparison to trees with bound tightening.

A family `P` of boxes with disjoint interiors covering a set `A` is
**`alpha`-valid on `A`** if

```
(V)   m(y) + eps >= alpha q_C(y)    for every C in P and every y in C ∩ A ∩ F.
```

For `A = X0`, this is the scout's definition.

### 1.4 Gap hypotheses

Lower bounds use one of the following three conditions.

- **(G^pt_alpha)**, objective gap at feasible points: for every box `B` and
  every `y in F ∩ B`, `f_B(y) <= f(y) - alpha q_B(y)`.
- **(G^LB_alpha)**, bound form: for every box `B` and every `y in F ∩ B`,
  `LB(B) <= f(y) - alpha q_B(y)`. Since `y in R_B`, (G^pt) implies (G^LB).
- **(T_{alpha,beta})**, tube form, for gaps coming from constraint
  relaxations: for every box `B` and every `z in B ∩ P_ex` with
  `v(z) <= beta q_B(z)`, we have `z in R_B` and
  `f_B(z) <= f(z) - alpha q_B(z)`. Here `alpha >= 0` and `beta >= 0`. With
  `beta = 0` the tube is `F ∩ B`, and (T) reduces to (G^pt).

Upper bounds use:

- **(U_tau)**, second-order pointwise convergence (Bompadre–Mitsos;
  Kannan–Barton 2018, Definition 13): for every box `B` and every
  `z in R_B`, `f_B(z) >= f(z) - tau w(B)^2` and `v(z) <= tau w(B)^2`.
- **(U^q_{alpha'})**, vertex-vanishing form: for every box `B` and every
  `z in R_B`, `f_B(z) >= f(z) - alpha' q_B(z)` and `v(z) <= alpha' q_B(z)`.
  Since `q_B <= n w(B)^2/4`, (U^q_{alpha'}) implies (U_tau) with
  `tau = alpha' n/4`.
- **(EB)**, error bound: `dist_2(z, F) <= kappa v(z)` for all
  `z in X0 ∩ P_ex` with `v(z) <= v_0`.
- **(Lip)**: `f` is `L`-Lipschitz on `X0` in the Euclidean norm.

(EB) holds when the Mangasarian–Fromovitz condition (MFCQ) holds at every
point of `F`, the box constraints of `X0` and `P_ex` included, and the data
are `C^1`. Robinson's stability theorem (Robinson 1976; Bonnans–Shapiro 2000,
Theorem 2.87) gives a local error bound at each feasible point. A compactness
argument makes it uniform for `v(z) <= v_0`: a sequence with `v(z_k) -> 0`
and `dist(z_k, F)/v(z_k) -> inf` has a limit point in `F`, where the local
bound fails.

### 1.5 Which relaxations satisfy what

- **Uniform alphaBB of the objective**, `f_B = f - alpha q_B` with `alpha` at
  least half the most negative Hessian eigenvalue on `X0`, and any valid
  relaxation of the constraints: (G^pt_alpha) and, for the objective part,
  (U^q_alpha).
- **Secant relaxation of separable concave terms** `-sum_i c_i y_i^2`, with
  `c_i >= alpha`: gap `sum_i c_i a_i`, so (G^pt_alpha) and
  (U^q_{max c_i}).
- **alphaBB relaxation of a nonconvex constraint** `g <= 0` by
  `g - beta q_B <= 0`, and of an equality `h = 0` by
  `h - beta q_B <= 0 <= h + beta q_B`: the relaxed set is exactly the tube
  `{v <= beta q_B}`. With the objective exact this gives (T_{0,beta}) and the
  constraint part of (U^q_beta).
- **McCormick envelopes of bilinear terms** satisfy the upper hypothesis but
  not the lower one (Lemma 1.1). Interval-Hessian alphaBB with a
  box-dependent `alpha_B -> 0` satisfies neither lower hypothesis uniformly.

**Lemma 1.1 (McCormick gap of a bilinear term).** Let `B = [l_1,u_1] x
[l_2,u_2]`, and let `psi` and `Psi` be the McCormick convex and concave
envelopes of `xy` on `B`. Then on `B`

```
0 <= xy - psi(x,y) <= q_B(x,y)/2,       0 <= Psi(x,y) - xy <= q_B(x,y)/2,
```

and both gaps vanish on every edge of `B`.

*Proof.* Write `p = x - l_1`, `p' = u_1 - x`, `r = y - l_2`, `r' = u_2 - y`.
All four are nonnegative on `B`.
- The two underestimators are `l_2 x + l_1 y - l_1 l_2` and
  `u_2 x + u_1 y - u_1 u_2`. The corresponding differences are
  `xy - (l_2 x + l_1 y - l_1 l_2) = p r` and
  `xy - (u_2 x + u_1 y - u_1 u_2) = p' r'`.
- Hence `xy - psi = min(p r, p' r')`, and
  `min(p r, p' r') <= sqrt(p r p' r') = sqrt(p p') sqrt(r r') <= (p p' + r r')/2 = q_B/2`.
- The concave case is the same with `min(p r', p' r)`.
- On an edge one of `p, p', r, r'` is 0. □

So McCormick bilinear relaxations satisfy (U^q_{|coef|/2}). They violate
(G^pt_alpha) for every `alpha > 0`, because the pointwise gap is 0 on edges
where `q_B > 0`.

(G^LB_alpha) bounds only `LB(B)`, which can be lower elsewhere in `B`, so a
zero pointwise gap does not by itself contradict it. It does fail on the
scout's face-exact example (review, Section 7):
- there a 2-leaf certificate exists for every `eps`, while the optimal set is
  a segment;
- under (G^LB_alpha), Theorem 4.6 with `eta = 0` would force
  `N_opt(eps) >= 2^(-2) N_inf(segment, 2 sqrt(eps/alpha)) -> inf`.

The upper bounds of Section 6 therefore apply to McCormick relaxations, and
the lower bounds of Sections 3–5 do not. In that example widest-side
bisection needs `Omega(eps^(-1/2))` nodes.

## 2. Leaves, reduction pieces and validity (Lemma 0, corrected)

Two kinds of domain reduction are distinguished. Each is applied in rounds to
the current box `B_k` of a node and returns a box `B_{k+1} ⊆ B_k`.

- **(R-inf) Feasibility-based reduction.** It removes only points outside
  `F`. Examples are exact constraint propagation on the original constraints
  and interval FBBT without the objective cutoff.
- **(R-rel) Same-relaxation reduction.** It removes only points
  `z in B_k` with `z notin R_{B_k}` or `f_{B_k}(z) > UBD - eps`. Examples:
  - OBBT over `{z in R_{B_k} : f_{B_k}(z) <= UBD}` or with cutoff
    `UBD - eps`;
  - reduced-cost or marginal tightening from a dual solution of the
    relaxation on `B_k`;
  - propagation of the relaxation's own convex constraints.

Objective-cutoff propagation (FBBT of `f(z) <= UBD` or `f <= UBD - eps`
through the expression of `f`) is **neither**. It removes feasible points using
information other than the relaxation. The review shows that on the scout's
instance `t^2 - 2t^4` it empties the root with no relaxation solved
(review, Section 1.3). Every lower bound below excludes it.

**Frame decomposition.** For boxes `B' = prod [l'_i,u'_i] ⊆ B = prod [l_i,u_i]`,
the frame `B \ int B'` is covered, with disjoint interiors, by the at most `2n`
nondegenerate boxes

```
S_i^- = prod_{j<i} [l'_j,u'_j] x [l_i, l'_i] x prod_{j>i} [l_j,u_j],
S_i^+ = prod_{j<i} [l'_j,u'_j] x [u'_i, u_i] x prod_{j>i} [l_j,u_j],   i = 1..n.
```

Proof: if `y in B \ int B'`, let `i` be the least index with
`y_i notin (l'_i, u'_i)`; then `y in S_i^-` or `y in S_i^+`. Pieces with
different `i` have disjoint interiors, because `S_i` forces `y_i` outside
`(l'_i,u'_i)` while `S_{i'}`, `i' > i`, forces `y_i in [l'_i,u'_i]`. All pieces
lie in `B`.

**Lemma 2.1 (leaves and pieces).** Consider any branch-and-bound run that
terminates at tolerance `eps >= 0`. It may use axis-parallel splits at
arbitrary points, any node order, any incumbent values `UBD >= f*` (changing
over time), pruning by bound or infeasibility, bounds inherited from ancestors,
and reduction rounds of types (R-inf) and (R-rel). Record the pruned nodes as
leaves. When a node's bound is set to the minimum of its children's bounds
(strong branching or probing), record the children, not the node. Decompose the
frame removed in **each reduction round** into at most `2n` pieces as above.
Let `P` be the family of leaves and pieces. Then:

(a) `P` consists of boxes with pairwise disjoint interiors covering `X0`.

(b) Under (G^pt_alpha), `P` is `alpha`-valid on `X0`: (V) holds at every
feasible point of every member. If the run uses no (R-rel) round, (G^LB_alpha)
suffices.

(c) Under (T_{alpha,beta}), if the run uses no (R-inf) round, then for every
`C in P` and every `z in C ∩ P_ex`:

```
(D)   either   v(z) > beta q_C(z)   or   f(z) - alpha q_C(z) >= f* - eps.
```

(d) Let `P_F = {C in P : C ∩ F ≠ ∅}`. Then
`|P_F| <= #leaves + 2n #(R-rel rounds)` and
`|P| <= #leaves + 2n #(all reduction rounds)`.

*Proof.*

(a) By induction over processed nodes. A split partitions a box into children.
A reduction round partitions `B_k` into `B_{k+1}` and the frame pieces.

(b) Let `C` be a leaf pruned by a bound `LB(A) >= UBD - eps >= f* - eps`,
where `A = C` or `A` is an ancestor with `A ⊇ C` (inherited bound).
- Take `y in F ∩ C`. Then (G^LB) on `A` gives
  `f(y) - alpha q_A(y) >= LB(A) >= f* - eps`.
- `q_C(y) <= q_A(y)`, because `(y_i-l_i^C)(u_i^C-y_i) <= (y_i-l_i^A)(u_i^A-y_i)`
  when `[l^C,u^C] ⊆ [l^A,u^A]`. This gives (V).

The other members satisfy (V) as follows.
- Leaves pruned by infeasibility and (R-inf) pieces contain no feasible point,
  so (V) holds vacuously.
- Let `S ⊆ B_k` be an (R-rel) piece and `y in S ∩ F`. Then `y in R_{B_k}`, so
  `y` was removed because `f_{B_k}(y) > UBD - eps >= f* - eps`. By (G^pt),
  `f(y) - alpha q_S(y) >= f(y) - alpha q_{B_k}(y) >= f_{B_k}(y) > f* - eps`.

(c) Take a leaf `C` with bound from `A ⊇ C` as in (b), and
`z in C ∩ P_ex` with `v(z) <= beta q_C(z)`.
- Since `q_C(z) <= q_A(z)`, the point `z` is in the tube of `A`. So
  `z in R_A`, and `f(z) - alpha q_C(z) >= f(z) - alpha q_A(z) >= f_A(z) >= LB(A) >= f* - eps`.
- If `C` was pruned as infeasible, `R_C` is empty. So no point of `C` is in its
  tube, and the first alternative of (D) holds for all `z`.
- For an (R-rel) piece `S ⊆ B_k` and `z in S ∩ P_ex` with
  `v(z) <= beta q_S(z) <= beta q_{B_k}(z)`, `z` is in the tube of `B_k`. So
  `z in R_{B_k}`, and `z` was removed because `f_{B_k}(z) > UBD - eps`. As
  before, `f(z) - alpha q_S(z) > f* - eps`.

(d) Each leaf is one member. Each round contributes at most `2n` pieces.
(R-inf) pieces do not meet `F`. □

**Remarks.**

- *Why per round.* Splitting the merged frame `B_0 \ B_final` of several
  rounds can violate (V), because a merged piece need not lie in the box
  `B_k` whose relaxation removed its points. The review's 2D test with
  iterated OBBT found 10 to 151 such violations per run, and none with
  per-round frames (review, Section 1.3, `reviews/spatial-bb/obbt_2d.py`).
- *Counting relaxations.* If every (R-rel) round solves at least one
  relaxation, as OBBT does, then `|P_F| <= (2n+1)` times the number of
  relaxations solved plus leaves pruned by an inherited bound without their
  own solve. Every lower bound on `|P_F|` below is therefore a lower bound on
  the work of such runs, up to the factor `2n+1`.
- *Why (c) excludes (R-inf).* Exact propagation of the original constraints
  may remove tube points. These are infeasible points with small objective
  value, and they carry the lower bound of Section 5. Example 5.3 shows that
  this can collapse the tree.

## 3. The unconstrained package (scout's Theorems B, D, A, C), corrected

In this section `F = X0` (no constraints), so `v ≡ 0`. The review checked each
proof below. The fixes are in the statements of Theorem 3.5, Lemma 3.6,
Remark 3.7 and Section 3.8.

**Theorem 3.1 (integral lower bound; scout's Theorem B).** Let `F = X0` and
`eps > 0`. Every `alpha`-valid family `P` satisfies

```
|P| >= (alpha n / pi^2)^(n/2) integral_{X0} (m(y) + eps)^(-n/2) dy.
```

*Proof.*
1. On `C in P`, (V) gives `(m + eps)^(-n/2) <= (alpha q_C)^(-n/2)`.
2. By AM–GM, `q_C >= n (prod_i a_i)^(1/n)`, so
   `q_C^(-n/2) <= n^(-n/2) prod_i a_i(y_i)^(-1/2)`.
3. The arcsine integral does not depend on the interval. With
   `t = l + (u-l) sin^2 theta`,
   `integral_l^u ((t-l)(u-t))^(-1/2) dt = integral_0^(pi/2) 2 dtheta = pi`.
4. Hence `integral_C (m+eps)^(-n/2) <= (pi^2/(alpha n))^(n/2)` for every box
   `C`, whatever its shape.
5. Summing over the cover `P` gives the claim. □

Remarks (from the review, Section 2).

- The constant is sharp for `n = 1`. For the sawtooth
  `f = alpha (y - kh)((k+1)h - y)` on `N` cells of width `h`, `N_opt = N` and
  the bound tends to `N`.
- For `n >= 2` the AM–GM step loses about `0.81^n` per cube, and more on
  elongated boxes. Whether `N_opt` loses this factor on some instance is open.
- *Anisotropic gap* `sum_i alpha_i a_i`: the constant becomes
  `(n/pi^2)^(n/2) prod_i alpha_i^(1/2)`. If some `alpha_i = 0`, no bound
  follows; Example 5.3 shows this is genuine.
- *Low rank* (gap only in coordinates `K`, `|K| = k`): slicing gives
  `|P| >= (alpha k/pi^2)^(k/2) sup_z integral (f(y,z)-f*+eps)^(-k/2) dy`.
  This is a lower bound only.
- *Exact certificates* (`eps = 0`) require
  `integral (f-f*)^(-n/2) < inf`, by monotone convergence. This is a
  necessary condition only.

**Theorem 3.2 (near-optimal sets; scout's Theorem D).** Let `S subset F` with
`m <= eta` on `S`. Assume `H^p(S ∩ Q) <= c_S l^p` for every cube `Q` of side
`l <= l0`. If `eps + eta <= alpha l0^2/4`, every family that is
`alpha`-valid on `S` satisfies

```
|P| >= H^p(S) (alpha/(4(eps+eta)))^(p/2) / (2^n c_S).
```

*Proof.* Let `r = ((eps+eta)/alpha)^(1/2)`.
1. For `y in S ∩ C`, (V) gives `alpha d_i(y)^2 <= alpha a_i(y) <= eps + eta`
   for every `i`. So `y in Q(v, r)` for the vertex `v` of `C` nearest in each
   coordinate.
2. Hence `H^p(S ∩ C) <= 2^n c_S (2r)^p`.
3. Subadditivity over the cover gives the claim. □

Theorem 4.6 below is the covering form of this argument and implies it. The
constrained case needs no change, since only points of `F` are used.

**Theorem 3.3 (bisection is within a log factor of optimal; scout's Theorem
A).** Assume:
- `X0` is a cube of side `s0`, and `F = X0`;
- two-sided gaps `alpha q_B <= f - f_B <= alpha' q_B` on every box, with
  `kappa = alpha'/alpha`;
- `T_bis` is the uniform `2^n`-ary dyadic refinement with `UBD = f*`. Level-`j`
  cubes have side `s_j = s0 2^(-j)`, and the children of a cube not pruned at
  tolerance `eps` are processed.

Then for every `alpha`-valid family `P`,

```
|T_bis| <= 1 + 4^n (sqrt(kappa n) + 2)^n J_eps |P|,     J_eps = max(0, ceil(log2(s0 sqrt(alpha' n/(4 eps))))).
```

*Proof.*
1. *Levels.* Let `Q_j = n s_j^2/4`, and let `D` be a non-pruned level-`j`
   cube. Some `y in D` has `f_D(y) < f* - eps`. Then
   `f(y) - alpha' q_D(y) <= f_D(y)`, so `m(y) + eps < alpha' q_D(y) <= alpha' Q_j`.
   As `m >= 0`, `s_j > 2 (eps/(alpha' n))^(1/2)`. At most `J_eps` levels can
   contain non-pruned cubes.
2. *Vertex proximity.* Let `C in P` contain `y`. By (V),
   `alpha a_i^C(y) <= alpha q_C(y) <= m(y) + eps < alpha' Q_j`. So
   `d_i^C(y) < s_j (kappa n)^(1/2)/2` for all `i`. Then
   `y in Q(v, s_j (kappa n)^(1/2)/2)` for a vertex `v` of `C`, and
   `D ⊆ Q(v, s_j((kappa n)^(1/2)/2 + 1))`.
3. *Counting.* A cube of side `s_j(sqrt(kappa n) + 2)` contains at most
   `(sqrt(kappa n) + 2)^n` level-`j` cubes. Charge `D` to the triple
   (`C`, `v`, `j`). There are `2^n |P| J_eps` triples.
4. Each non-pruned cube has `2^n` processed children, and the root is
   processed. □

The hypothesis `F = X0` is used in step 2: the witness `y` is only
relaxed-feasible, and (V) is needed at `y`. Theorem 6.2 removes it with an
error bound. The upper gap is used only for the bisection tree. `P` may come
from any run covered by Lemma 2.1.

**Example 3.4 (the log factor is attained).** Take `f(y) = 2|y-a| - (y-a)^2`
on `[0,1]` with `a = 1/3`, and exact alphaBB with `alpha = alpha' = 1`.
- On any `[l,u]` containing `a`, `f_B = 2|y-a| + (2a-l-u)y + lu - a^2`. This
  is convex piecewise linear with slope below `-1` left of `a` and at least
  `1` right of it, so `LB = -(a-l)(u-a)`.
- On a cell not containing `a`, `f_B` is linear and nonnegative at both
  endpoints, so the cell is pruned.
- So `{[0,a],[a,1]}` is a certificate for every `eps >= 0`, while
  `|T_bis| = 1 + 2 #{j >= 0 : 2 (2^(-j))^2/9 > eps}` (review, Section 4).

**Correction (review, Section 6).** Bisection does *not* need
`Theta(log(1/eps))` whenever the minimizer avoids dyadic points. For
`z = sum_k 2^(-2^(2^k))`, `liminf |T_bis|/log(1/eps) = 0`. The lower bound
`Omega(log(1/eps))` holds when a positive fraction of the levels have some
coordinate of the minimizer in the middle part `[delta, 1-delta]` of its dyadic
cell (Remark 6.9). The upper bound `O(log(1/eps))` always holds.

**Theorem 3.5 (bisection matches the integral; scout's Theorem C).** Assume
the setting of Theorem 3.3, and

```
(QD)   m(x) <= K (m(y) + |x - y|_inf^2)   for all x, y in X0,   with K >= 1.
```

Then, with `Lambda = K(alpha' n/4 + 1)`,

```
|T_bis| <= 1 + 2^(n+1) Lambda^(n/2) integral_{X0} (m + eps)^(-n/2) dy.
```

*Proof.*
1. Let `D` be non-pruned at level `j`. As in Theorem 3.3, some `y in D` has
   `m(y) < alpha' Q_j - eps`.
2. For `x in D`, `|x - y|_inf <= s_j`, so by (QD)
   `m(x) + eps <= K(alpha' Q_j - eps + s_j^2) + eps <= Lambda s_j^2`, using
   `K >= 1`. Hence `D ⊆ {m + eps <= Lambda s_j^2}`, and the number of such
   `D` is at most `V(Lambda s_j^2)/s_j^n`, where
   `V(t) = vol{x in X0 : m(x) + eps <= t}`.
3. Summing over `j`,
   `sum_j s_j^(-n) V(Lambda s_j^2) = integral_{X0} sum_{j : s_j >= theta(x)} s_j^(-n) dx`,
   where `theta(x) = ((m(x)+eps)/Lambda)^(1/2)`.
4. The inner geometric sum is at most `theta^(-n)/(1 - 2^(-n)) <= 2 theta^(-n)`.
5. Finally `|T_bis| = 1 + 2^n #(non-pruned cubes)`. □

(The scout's `Lambda` had an extra `+ alpha' n/4`; the review shows it can be
dropped, as done here.)

**Lemma 3.6 (a sufficient condition for (QD); corrected, from the review).**
Let `G = sup_{X0} |grad m|_2`. Suppose `m` extends to a convex set
`U ⊇ X0 + B_2(0, G/M)` on which `m >= 0` and `grad m` is `M`-Lipschitz in the
Euclidean norm. Then (QD) holds with `K = max(2, nM)`.

*Proof.*
1. For `y in X0`, the point `y - grad m(y)/M` lies in `U`. The descent lemma
   gives `0 <= m(y - grad m(y)/M) <= m(y) - |grad m(y)|^2/(2M)`. Hence
   `|grad m(y)|^2 <= 2 M m(y)`.
2. For `x in X0`, the descent lemma along `[y, x]` and `2ab <= a^2 + b^2` give
   `m(x) <= m(y) + |grad m(y)| |x-y| + (M/2)|x-y|^2 <= 2 m(y) + M |x-y|_2^2 <= 2 m(y) + nM |x-y|_inf^2`. □

The scout's `K = max(2, M)` is false for two reasons (review, Section 5).
- The norm factor `n` is missing. Take `m = |x|^2/2` with `x = (t, ..., t)`.
- A thin neighbourhood of `X0` does not suffice. The review's `m_rho` has a
  (QD) constant growing like `rho^(-1/2)`.

For growth `sum_i |t_i|^(q_i)` with `q_i >= 2` on a box of diameter `D`,
(QD) follows from `|x_i|^q <= 2^(q-1)(|y_i|^q + D^(q-2)|x_i - y_i|^2)`.
(QD) fails at sharp minima.

**Remark 3.7 (what "bisection matches the optimum" means).** For (QD)
instances, Theorems 3.1 and 3.5 give

```
(alpha n/pi^2)^(n/2) I(eps) <= N_opt(eps) <= |T_bis| <= 1 + 2^(n+1) Lambda^(n/2) I(eps),
I(eps) = integral (m+eps)^(-n/2).
```

The ratio of the constants is
`2^(n+1) Lambda^(n/2) (pi^2/(alpha n))^(n/2) = 2 (4 pi^2 Lambda/(alpha n))^(n/2)`.
With `Lambda = K(alpha' n/4 + 1)` this equals
`2 (pi^2 K (kappa + 4/(alpha n)))^(n/2)`. It is independent of `eps` but
depends on `K`, `kappa` and `K/alpha`. (The first version of this note
dropped a factor `2^n` here.)

The scout's claim that the three quantities agree "up to `e^{O(n)}`" is false
as stated. Written as `m(x) <= K_1 m(y) + K_2 |x-y|^2`, the ratio grows like
`(K_2/alpha)^(n/2)`, and `K_2` is at least the curvature of `m`
(review, Section 5).

### 3.8 Rate table, corrected

`I(eps)` is evaluated near the near-optimal set; unconstrained, and (QD) where
an upper bound is claimed.

| Structure near the optimum | `N_opt` | bisection | proved where |
|---|---|---|---|
| `r` isolated nondegenerate minimizers, Hessian `~ gamma I` | `Theta(log(1/eps))`, lower bound `≈ r (2e alpha/(pi gamma))^(n/2) (n/(4 pi))^(1/2) log(1/eps)` (review) | `Theta(log(1/eps))` | Theorems 3.1, 3.5 |
| `p`-dimensional Morse–Bott manifold of minimizers | `Theta(eps^(-p/2))` | same | Theorems 3.1, 3.5; with constraints Theorem 7.2 |
| growth `sum_i |t_i|^(q_i)`, `q_i >= 2` | `Theta(eps^(-(n/2 - sum 1/q_i)))`, or `log` if all `q_i = 2` | same | Theorems 3.1, 3.5 |
| sharp minimum, `m >= c|t|` | `O(1)` for all `eps >= 0` (Proposition 6.8) | `O(log(1/eps))`; `Omega(log)` only under the middle-part condition | Theorem 3.3, Remark 6.9 |
| gap in `k` coordinates only | lower bound by the `k`-dimensional slice integral | upper bound **not** proved | Theorem 3.1, remark |

## 4. Stratified lower bounds with constraints

Under (G^LB_alpha), every certificate at tolerance `eps` is `alpha`-valid on
`F`. For `C` with `LB(C) >= f* - eps` and `y in F ∩ C`,
`f(y) - alpha q_C(y) >= LB(C) >= f* - eps`. By Lemma 2.1, the same holds for
the leaf-and-piece family of any run with the allowed reductions. The theorems
below are stated for `alpha`-valid families, so they bound `N_opt(eps)` and
the size of every such run from below.

### 4.1 Coordinate multiplicity and the key lemma

Let `1 <= d <= n` and let `S subset R^n` be a `d`-dimensional embedded `C^1`
submanifold, not necessarily closed.

- For `y in S`, let `U(y)` be an `n x d` matrix with orthonormal columns
  spanning `T_y S`.
- For `I subset {1..n}` with `|I| = d`, let `J_I(y) = |det U_I(y)|`, where
  `U_I` keeps the rows in `I`. This is the Jacobian of the coordinate
  projection `pi_I` restricted to `T_y S`.
- By the Cauchy–Binet formula, `sum_I J_I(y)^2 = det(U^T U) = 1`. So the
  lexicographically first maximizer `I(y)` has
  `J_{I(y)}(y) >= binom(n,d)^(-1/2)`.
- Put `S^I = {y in S : I(y) = I}`, a Borel partition of `S`.

For `A subset R^n`, define

```
M^I(S; A) = sup_{x in R^I} #(S^I ∩ A ∩ pi_I^(-1)(x)),   M^I(S) = M^I(S; R^n),   M(S) = sum_I M^I(S).
```

`M^I(S; A)` is the largest number of points of `S ∩ A` on one coordinate
`(n-d)`-flat `{y_I = x}`, counting only points where that flat is the most
transversal coordinate flat. For `d = n` (an open subset of `R^n`), `M = 1`.

**Lemma 4.1 (key lemma).** For every box `B` and every Borel set `A`,

```
integral_{S ∩ B ∩ A} q_B(y)^(-d/2) dσ(y) <= C_{n,d} sum_I M^I(S; A ∩ B),     C_{n,d} = (pi^2/d)^(d/2) binom(n,d)^(1/2).
```

In particular, `sup_B integral_{S∩B} q_B^(-d/2) dσ <= C_{n,d} M(S)`.

*Proof.* Fix `I`.
1. For `y in S^I ∩ B`, AM–GM over the coordinates in `I` gives
   `q_B(y) >= sum_{i in I} a_i(y) >= d (prod_{i in I} a_i(y))^(1/d)`. So
   `q_B^(-d/2) <= d^(-d/2) prod_{i in I} a_i(y_i)^(-1/2)` in `[0, inf]`.
2. Since `J_I >= binom(n,d)^(-1/2)` on `S^I`,
   `integral_{S^I∩B∩A} prod_{i in I} a_i^(-1/2) dσ <= binom(n,d)^(1/2) integral_{S^I∩B∩A} prod_{i in I} a_i(y_i)^(-1/2) J_I(y) dσ(y)`.
3. By the area formula for the linear map `pi_I` on the `d`-rectifiable set
   `E = S^I ∩ B ∩ A` (Federer 3.2.20; Evans–Gariepy, Theorem 3.9), the last
   integral equals
   `integral_{prod_{i in I}[l_i,u_i]} prod_{i in I} a_i(x_i)^(-1/2) #(E ∩ pi_I^(-1)(x)) dx`.
4. The multiplicity is at most `M^I(S; A ∩ B)`, and by the arcsine integral the
   remaining integral is `pi^d`.
5. Summing over `I` gives `d^(-d/2) binom(n,d)^(1/2) pi^d sum_I M^I`. □

For `d = n` this is steps 2–4 of Theorem 3.1.

**Lemma 4.2 (local multiplicity one).** Suppose `S` has a *two-point
constant* `tau in (0, inf]`:

```
dist(z - y, T_y S) <= |z - y|^2/(2 tau)    for all y, z in S.
```

Put `rho_* = 2 tau/(1 + binom(n,d)^(1/2))`. If `y, z in S^I`,
`pi_I(y) = pi_I(z)` and `|z - y| < rho_*`, then `y = z`. Consequently:

- `M^I(S; A) <= 1` for every set `A` of Euclidean diameter `< rho_*`;
- if `S subset X0` and `d < n`, then
  `M^I(S) <= (floor(s0 sqrt(n-d)/rho_*) + 1)^(n-d)`.

*Proof.*
1. Write `z - y = t + nu` with `t in T_y S` and `nu ⊥ T_y S`. Then
   `|nu| <= |z-y|^2/(2 tau)`, and `pi_I t = -pi_I nu`.
2. The restriction of `pi_I` to `T_y S` has singular values
   `sigma_1 >= ... >= sigma_d`, all at most 1 because `pi_I` is an orthogonal
   projection. So `J_I(y) = prod sigma_k <= sigma_d`, and
   `|t| <= |pi_I t|/sigma_d <= |nu|/J_I(y) <= binom(n,d)^(1/2) |nu|`.
3. Hence `|z - y| <= |t| + |nu| <= (1 + binom(n,d)^(1/2)) |z-y|^2/(2 tau)`.
   This forces `z = y` or `|z - y| >= rho_*`.
4. For the global count, partition the fibre `pi_I^(-1)(x) ∩ X0`, a box in
   the `n-d` coordinates outside `I` with sides at most `s0`, into `k^(n-d)`
   boxes of side `s0/k` with `k = floor(s0 sqrt(n-d)/rho_*) + 1`. Each has
   diameter `< rho_*`. □

By Federer's theorem on sets of positive reach (Federer 1959, Theorem
4.18(2)), every **relatively open** subset `S` of a `d`-dimensional `C^1`
submanifold `Sigma` with `reach(Sigma) >= tau` has two-point constant `tau`.
Federer's theorem gives the inequality with `2r` for every `r < reach`, and
letting `r -> reach` gives `tau`. Relative openness makes `T_y S = T_y Sigma`.
Examples:
- a sphere of radius `R` has `tau = R`, with equality in the defining
  inequality;
- an affine subspace has `tau = inf` and `M(S) = 1`;
- a compact `C^2` submanifold without boundary has `tau > 0`.

The following local version is the one used near a point.

**Lemma 4.3 (graphs).** Let `T` be a `d`-dimensional subspace, `U subset T`
convex, and `phi : U -> T^⊥` of class `C^2` with `||D^2 phi|| <= K_2` on `U`.
Then `S = {x + phi(x) : x in U}` has two-point constant `tau >= 1/K_2`
(`tau = inf` if `K_2 = 0`).

*Proof.* Let `y = x + phi(x)` and `z = x' + phi(x')`, and set `h = x' - x`.
1. `h + D phi(x) h in T_y S`, so
   `dist(z - y, T_y S) <= |phi(x') - phi(x) - D phi(x) h| <= (K_2/2)|h|^2`
   by Taylor's theorem on the segment `[x, x'] subset U`.
2. `|h| <= |z - y|`, because `h` is the `T`-component of `z - y`. □

**Proposition 4.4 (the multiplicity factor is necessary; curvature is not
enough).**

(a) Let `S_k` be the union of `k` parallel segments `(0,1) x {h_j}`,
`h_j = (j - 1/2)/k`, in `R^2`. It has zero curvature and `M(S_k) = k`. For
`B = [0,1]^2`,

```
integral_{S_k ∩ B} q_B^(-1/2) ds = sum_j 2 arcsin((1 + 4 h_j(1-h_j))^(-1/2)) >= (pi/2) k,
```

while Lemma 4.1 gives at most `pi sqrt(2) k`.

(b) Let `S_∞` be the union of the segments `(0,1) x {2^(-j)}`, `j >= 1`. It is
an embedded one-dimensional `C^∞` submanifold with infinitely many
components, zero curvature and reach 0. Then
`integral_{S_∞ ∩ [0,1]^2} q^(-1/2) ds = inf`.

(c) A connected example: the spiral
`c(t) = rho(t)(cos t, sin t)`, `rho(t) = r(1 + 1/(1+t))`, `t in (0, inf)`, is
an embedded `C^∞` curve with curvature at most `10/r` and reach 0. For
`B = [-2r, 2r]^2`, `integral_{S ∩ B} q_B^(-1/2) ds = inf`.

So no bound `C(n, d, curvature)` can hold for all boxes, even for connected
strata.

*Proof.*
- (a), (b): On the segment at height `h`,
  `q_B = (1/4 + h(1-h)) - (x - 1/2)^2`. With `c^2 = 1/4 + h(1-h)`, the integral
  `integral_0^1 (c^2 - (x-1/2)^2)^(-1/2) dx = 2 arcsin(1/(2c))`. Since
  `4h(1-h) <= 1`, each term is at least `2 arcsin(2^(-1/2)) = pi/2`.
- (c), embedding: `|c(t)| = rho(t)` is continuous and strictly decreasing.
  So `c` is injective, and `c^(-1) = rho^(-1)(|·|)` is continuous on the
  image. Hence `c` is an embedding. (The limit points not on the curve are
  the circle of radius `r` and the point `(2r, 0)`.)
- (c), reach 0: compare `y = c(t)` and `z = c(t + 2 pi)`, which lie at the same
  angle.
  - The chord is `z - y = -Delta e_r` with `Delta = rho(t) - rho(t + 2 pi) -> 0`,
    where `e_r` is the radial unit vector.
  - The unit tangent at `y` is `(rho' e_r + rho e_theta)/sqrt(rho^2 + rho'^2)`,
    so `dist(z - y, T_y) = Delta rho/sqrt(rho^2 + rho'^2)`.
  - A two-point constant `tau` would need
    `Delta rho/sqrt(rho^2 + rho'^2) <= Delta^2/(2 tau)`, that is,
    `tau <= Delta sqrt(rho^2 + rho'^2)/(2 rho) -> 0` as `t -> inf`.
  - By Federer's theorem, a set of positive reach has two-point constant equal
    to its reach, so the reach is 0.
- (c), curvature: `r < rho < 2r`, `|rho'| <= r` and `|rho''| <= 2r`. The polar
  curvature formula `|rho^2 + 2 rho'^2 - rho rho''|/(rho^2 + rho'^2)^(3/2)`
  gives at most `10 r^2/r^3`.
- (c), divergence: the length is at least `integral r dt = inf`. The curve lies
  in the disc of radius `2r`, which is inside `B`, where
  `q_B <= 2 (2r)^2 = 8 r^2`. So the integral is at least
  `length/(2 sqrt(2) r) = inf`. □

**Numerics** ([`key_lemma_check.py`](key_lemma_check.py),
[`logs/key_lemma_check.log`](logs/key_lemma_check.log)).
- *Comb.* The ratio `(integral)/k` tends to `1.8403`. So the lemma's
  multiplicity factor is sharp up to a factor `pi sqrt 2 / 1.84 ≈ 2.4`.
- *Circle.* The largest value found is `2 pi`, attained by the bounding
  square. Nelder–Mead started there stays at `2 pi`. The lemma's bound is
  `pi sqrt(2) · 4 = 17.77`.
- *Spiral.* For the spiral with `r = 1`, the integral over `t in (0, T]` is
  4.98, 40.0 and 381 for `T = 10, 100, 1000`, which is linear in `T`.
- *Review stress test* (`reviews/spatial-constrained/key_lemma_stress.py`,
  not re-run here). The integral divided by the bound with the local
  multiplicity is at most 0.709 for curves (lines, circle, ellipse, helices)
  and 0.43 for surfaces (sphere, ellipsoid, planes). A segment on a box edge
  attains `1/sqrt 2`, so for multiplicity 1 the constant is sharp to within
  `sqrt 2` when `d = 1`.

### 4.2 The stratified integral lower bound

**Theorem 4.5 (stratified integral lower bound).** Let `S subset F` be a
`d`-dimensional embedded `C^1` submanifold, `1 <= d <= n`, let `eps > 0`, and
let `P` be `alpha`-valid on `S` (for example, a certificate under
(G^LB_alpha)).

(i) Global form:

```
|P| >= alpha^(d/2) integral_S (m + eps)^(-d/2) dσ / (C_{n,d} M(S)).
```

(ii) Local form. Assume `d < n` and that `S` has two-point constant `tau > 0`.
Let `r_* = rho_*/(2 sqrt(n-d))` and
`S_♭ = {y in S : m(y) + eps < alpha r_*^2}`. Then

```
|P| >= alpha^(d/2) integral_{S_♭} (m + eps)^(-d/2) dσ / (2^(n-d) binom(n,d) C_{n,d}).
```

(iii) For `d = n` and `S` open in `R^n`,
`|P| >= (alpha n/pi^2)^(n/2) integral_S (m+eps)^(-n/2)`.

*Proof.*

(i) For `C in P` and `y in S ∩ C`, (V) gives
`(m(y)+eps)^(-d/2) <= alpha^(-d/2) q_C(y)^(-d/2)`. Lemma 4.1 bounds
`integral_{S∩C} q_C^(-d/2)` by `C_{n,d} M(S)`. Sum over the cover `P` of
`S`.

(ii) Let `C in P` and `y in S_♭ ∩ C`.
1. (V) gives `alpha d_i(y)^2 <= alpha q_C(y) < alpha r_*^2`, so `y` lies in
   `A_C := union over vertices v of C of {z : |z - v|_inf < r_*}`.
2. We claim `M^I(S; A_C ∩ C) <= 2^(n-d)`. Take points of `S^I ∩ A_C ∩ C` on
   one fibre `{y_I = x}`. Label each point `y` by the vector
   `sigma(y) in {-,+}^(I^c)` that records, for `i notin I`, whether `y_i` is
   within `r_*` of `l_i` (label `-`, preferred in ties) or of `u_i`.
3. Two points `y, z` with the same label agree on `I` and satisfy
   `|y_i - z_i| < 2 r_*` for `i notin I`. So
   `|y - z| < 2 r_* sqrt(n-d) = rho_*`, and Lemma 4.2 gives `y = z`.
4. Lemma 4.1 with `A = A_C` gives
   `integral_{S_♭∩C} (m+eps)^(-d/2) <= alpha^(-d/2) C_{n,d} binom(n,d) 2^(n-d)`.
   Sum over `C`.

(iii) is Theorem 3.1 restricted to `S`. □

**Remarks.**

- *Which form to use.* Form (i) is exact for affine strata, where `M(S) = 1`
  and only one `I` occurs, so the constant is `C_{n,d}`. Form (ii) has
  constants that depend only on local geometry. For the comb `S_k` of
  Proposition 4.4 with `eps -> 0`, the true count is `~ k eps^(-1/2)`. Form (i)
  loses the factor `k`; form (ii) keeps it once `eps < alpha r_*^2`, with
  `r_* ~ 1/k`.
- *What is integrated.* The integrand `(m+eps)^(-d/2)` uses the dimension of
  the stratum, not `n`. For a full-dimensional `F` whose optimum lies on a
  boundary stratum, the boundary stratum can give a larger exponent than the
  `n`-dimensional integral (Section 8.2 and Section 9).
- *Constraints enter only through `S subset F`.* The constraint relaxations
  can be arbitrary under (G^LB). Section 5 treats schemes whose gap comes from
  the constraints.

### 4.3 The covering lower bound

**Theorem 4.6 (covering lower bound).** If `P` is `alpha`-valid on `E(eta)`,
then

```
|P| >= 2^(-n) N_inf(E(eta), 2 sqrt((eps + eta)/alpha))      for every eta >= 0.
```

*Proof.* Let `r = ((eps+eta)/alpha)^(1/2)`, and take `y in E(eta) ∩ C` with
`C in P`. Then `alpha d_i(y)^2 <= alpha q_C(y) <= m(y) + eps <= eta + eps`, so
`y in Q(v, r)` for a vertex `v` of `C`. The `2^n |P|` cubes `Q(v, r)` of side
`2r` cover `E(eta)`. □

Theorem 3.2 follows: if `2r <= l0`, then
`H^p(S) <= c_S (2r)^p N_inf(S, 2r)`. Theorem 4.6 needs no regularity and no
dimension. Theorem 4.5 is its integral, multi-scale refinement.

**Corollary 4.7.**

(a) *Sum over strata.* If `S_1, ..., S_{K_S} subset F` each satisfy the
hypotheses of Theorem 4.5(i) or (ii) with constants `c_k`, then
`N_opt(eps) >= (1/K_S) sum_k c_k alpha^(d_k/2) integral_{S_k (♭)} (m+eps)^(-d_k/2) dσ`.

(b) *Dimension.* Let `dim_low(M)` be the lower box-counting dimension of the
optimal set `M`, measured with sup-norm cubes. Then

```
liminf_{eps -> 0} log N_opt(eps) / log(1/eps) >= dim_low(M)/2.
```

*Proof.* (a) Take the maximum of the `K_S` bounds. (b) Apply Theorem 4.6 with
`eta = 0`: `N_opt(eps) >= 2^(-n) N_inf(M, delta)` with
`delta = 2 (eps/alpha)^(1/2)`, and
`log(1/delta) = (1/2) log(1/eps) + O(1)`. □

## 5. Constraint-gap schemes

Many relaxations keep a convex objective exact and put all the gap into
relaxed nonconvex constraints. Then (G^LB) can fail completely. A trivial
example is minimizing a linear function over a sphere with the convex side
`|y|^2 <= 1` kept exactly: the root bound is already `f*`. Pruning then
depends on how the relaxation treats **infeasible** points. This section uses
the tube hypothesis (T_{alpha,beta}) of Section 1.4.

*Modelling convention.* Constraints that the relaxation keeps exactly, in
particular convex constraints such as `|y|^2 <= 1`, must be placed in `P_ex`.
Otherwise, tube points that violate them are not in `R_B`, and (T) fails.
With this convention, the secant relaxation of a reverse-convex constraint
such as `|y|^2 >= 1` is a natural (T_{0,1}) scheme: its margin is exactly
`q_B`.

**Lemma 5.1 (tube dichotomy).** Under (T_{alpha,beta}), every certificate at
tolerance `eps` satisfies (D) of Lemma 2.1: for every `C` and every
`z in C ∩ P_ex`, either `v(z) > beta q_C(z)` or
`f(z) - alpha q_C(z) >= f* - eps`. The same holds for the leaf-and-piece
family of any run without (R-inf) rounds (Lemma 2.1(c)).

*Proof.* If `v(z) <= beta q_C(z)`, then `z in R_C` and
`f(z) - alpha q_C(z) >= f_C(z) >= LB(C) >= f* - eps`. □

For feasible `z` (`v = 0`) the first alternative is impossible, and (D) is
(V). For **super-optimal** points, those with `f(z) < f* - eps`, the second
alternative is impossible (`alpha q_C >= 0`). Such points must satisfy
`beta q_C(z) < v(z)`: they must lie near a vertex of their box, at the
parabolic scale of their violation.

**Theorem 5.2 (infeasible-side covering bound).** Let `P` satisfy (D) with
`beta > 0`. For `nu > 0` put
`W(eps, nu) = {z in X0 ∩ P_ex : v(z) <= nu, f(z) < f* - eps}`. Then

```
|P| >= 2^(-n) N_inf(W(eps, nu), 2 sqrt(nu/beta)).
```

If also `alpha > 0`, Theorem 4.6 holds as well, and `|P|` is at least the
larger of the two bounds.

*Proof.* For `z in W ∩ C`, (D) gives `beta d_i(z)^2 <= beta q_C(z) < v(z) <= nu`.
So `z` lies in a sup-ball of radius `sqrt(nu/beta)` around a vertex of `C`.
Conclude as in Theorem 4.6. □

**Example 5.3 (flat optimal segment; isotropic versus anisotropic loosening).**
Let `X0 = [-1.2, 1.3]^2`, `f(z) = z_2` (kept exact, `alpha = 0`), and one
constraint `g(z) = -z_2 <= 0`. Then `f* = 0` and `M = [-1.2,1.3] x {0}`. The
constraint is deliberately *not* kept exactly (`P_ex = R^2`). It is loosened
with `beta = 1` in one of two ways:

- *isotropic*: `R_B = {z in B : -z_2 <= q_B(z)}`, which satisfies
  (T_{0,1}) and (U^q_1);
- *anisotropic*: `R_B = {z in B : -z_2 <= a_2(z_2)}`, which satisfies (T)
  only with the anisotropic `q = a_2`.

Claims:

(a) *Anisotropic*: `N_opt(eps) <= 3` for every `eps >= 0`, while widest-side
bisection grows like `eps^(-1/2)` (numerically) and `z_2`-only bisection like
`log(1/eps)`.

(b) *Isotropic*: `N_opt(eps) >= (5/16) (2 eps)^(-1/2)` for `eps < 1/2`, and
`z_2`-only bisection does not terminate for `eps < 1.2`. Widest-side
bisection needs `O(eps^(-1/2))` nodes by Theorem 6.4, so
`N_opt = Theta(eps^(-1/2))`.

(c) Exact propagation of the original constraint (an (R-inf) round) sets
`l_2 = 0` at the root. The root relaxation then has bound `0 = f*`, so one
node suffices for every `eps >= 0`.

*Proof.*

(a) Consider the slabs `[-1.2,1.3] x [-1.2,-0.6]`, `x [-0.6, 0]` and
`x [0, 1.3]`.
- On `[l_2, 0]`, a point with `z_2 < 0` is relaxed-feasible iff
  `1 <= z_2 - l_2`. This is impossible when `|l_2| < 1`. So the relaxed set
  of the middle slab is `{z_2 = 0}`, with bound 0.
- On `[-1.2, -0.6]`, `-z_2 >= 0.6 > 0.09 >= a_2(z_2)`, so the relaxation is
  empty.
- On `[0, 1.3]`, the bound is 0.

(b) *Lower bound.* The strip `[-1.2,1.3] x [-2eps, -eps)` is contained in
`W(eps, 2eps)`, and its projection onto `z_1` has length 2.5. By Theorem 5.2,
`N_opt >= 2^(-2) · 2.5/(2 sqrt(2 eps))`.

*Non-termination of `z_2`-only bisection.* Every box
`[-1.2,1.3] x [l_2,u_2]` with `u_2 < -eps` contains the point `(0.05, u_2)`.
There `a_1 = 1.5625 > 1.2 >= -u_2`, so the point is relaxed-feasible, and
`LB <= u_2 < -eps`. Such boxes are never pruned, and splitting `z_2` keeps
producing them.

*Upper bound.* (U^q_1), (EB) with `kappa = 1` (`dist(z, F) = v(z)`) and
(Lip) with `L = 1` hold. `m(y) = y_2 >= dist(y, M)` on `F`, so (QG) of
Theorem 6.4 holds with `c_g = 1/s0`, since
`y_2 >= y_2^2/s0 = dist(y, M)^2/s0`. `N_inf(M, s) ~ 2.5/s`.

(c) After `l_2 = 0`, every point of the root box satisfies `-z_2 <= 0`. □

Numerics ([`flat_constraint_gap.py`](flat_constraint_gap.py),
[`logs/flat_constraint_gap.log`](logs/flat_constraint_gap.log)):

| eps | aniso widest | aniso `z_2`-only | iso widest | iso `z_2`-only | iso lower bound (leaves) |
|---|---|---|---|---|---|
| 1e-1 | 9 | 5 | 29 | > 2·10^6 | 0.75 |
| 1e-3 | 189 | 13 | 253 | > 2·10^6 | 7.0 |
| 1e-5 | 1533 | 19 | 3069 | > 2·10^6 | 70 |
| 1e-7 | 6141 | 23 | 32765 | > 2·10^6 | 699 |

The anisotropic widest-side count has plateaus. At some levels the dyadic
position of `z_2 = 0` in its cell is near an end (relative positions cycle
with period 20), so straddling cells are pruned early. This is the phenomenon
noted for Example 3.4.

Example 5.3 shows three things.
- An isotropic constraint gap forces the same `eps^(-p/2)` exponent as an
  objective gap.
- A gap that vanishes in the directions along the optimal set does not.
- Constraint propagation that uses information outside the relaxation can
  remove the whole effect.

The next results make the first point general.

**Theorem 5.4 (Lagrangian transfer, covering form).** Let `P` satisfy (D)
with `beta > 0` (any `alpha >= 0`). Let `eta >= 0` and `Y subset E(eta)`.
Assume the **outward descent** condition (OD): every `y in Y` has a unit
vector `e(y)` such that, for `t in [0, t_1]`,

```
y + t e in X0 ∩ P_ex,    v(y + t e) <= c_1 t,    f(y + t e) <= f(y) - mu_0 t + C_2 t^2.
```

If `0 < eta + eps <= min(mu_0^2/(9 C_2), mu_0 t_1/3, c_1 mu_0/(3 beta))`, then

```
|P| >= 2^(-n) N_inf(Y, 2 sqrt((eta + eps)/alpha_eff)),       alpha_eff = mu_0 beta/(12 c_1).
```

*Proof.* Let `t_* = 3(eta+eps)/mu_0 <= t_1` and `z = y + t_* e(y)`.
1. `f(z) <= f* + eta - 3(eta+eps) + 9 C_2 (eta+eps)^2/mu_0^2 <= f* - eps - (eta+eps) < f* - eps`.
2. `v(z) <= c_1 t_* =: nu`. By (D) and step 1, `beta q_C(z) < nu` for the box
   `C` containing `z`. So `z in Q(v, r)` for a vertex `v` of `C`, with
   `r = (nu/beta)^(1/2) = (3 c_1 (eta+eps)/(mu_0 beta))^(1/2)`.
3. The last condition on `eta + eps` gives `t_* <= r`. Hence
   `y in Q(v, 2r)`, and `Y` is covered by `2^n |P|` cubes of side
   `4r = 2 ((eta+eps)/alpha_eff)^(1/2)`. □

Theorem 5.4 transfers lower bounds only. A constraint gap yields the covering
lower bounds of an objective gap `alpha_eff`. The two gaps are not equivalent:
nothing here gives upper bounds from `alpha_eff`.

**Lemma 5.5 ((OD) near KKT points).** Let `z*` be a KKT point with
multipliers `(mu*, lambda*)` and LICQ, with `f, g, h` of class `C^2` near
`z*`. Assume that `P_ex` is polyhedral near `z*`: on some ball `B(z*, rho_ex)`
it is defined by finitely many affine inequalities. Let `A` be the active inequalities, including active box bounds and
active constraints of `P_ex`. Let `A'` be the set of active inequalities that
are not exact and have `mu*_j > 0`, together with the non-exact equalities
that have `lambda*_k ≠ 0`. Suppose `A'` is nonempty. Then there are a unit
vector `e` and constants `rho, t_1, mu_0, c_1, C_2 > 0` such that (OD) holds
with `e(y) = e` for every `y in F ∩ B(z*, rho)`.

*Proof.* By LICQ, choose `ê` with the following properties:
- `grad g_j(z*)·ê = 1` for the inequalities in `A'`;
- `grad h_k(z*)·ê = sign(lambda*_k)` for the equalities in `A'`;
- `grad·ê = 0` for all other active constraints, including box bounds and
  exact constraints.

Put `e = ê/|ê|`. Then:

- *Descent.* By KKT,
  `grad f(z*)·e = -(sum_{A'} mu*_j + sum_{A'} |lambda*_k|)/|ê| =: -2 mu_0 < 0`.
  With `M` a bound on the Hessians near `z*`, for `|y - z*| <= rho` with
  `M rho <= mu_0` we get
  `f(y + te) <= f(y) + t grad f(y)·e + M t^2/2 <= f(y) - mu_0 t + (M/2) t^2`.
- *Violation.* For every active constraint,
  `g_j(y+te) <= g_j(y) + t(grad g_j(z*)·e + M rho) + M t^2/2` and similarly
  for `|h_k|`. So `v(y + te) <= c_1 t` with
  `c_1 = max(|grad·e| over active constraints) + M rho + M t_1/2`.
- *Inactive constraints.* Inactive inequalities and inactive box bounds have
  slack bounded below near `z*`. They stay satisfied for `t <= t_1` small.
- *Exact constraints.* Active box bounds and active exact constraints have
  `grad·e = 0`. These constraints are affine near `z*` (box bounds, and
  `P_ex` by hypothesis), so their values are constant along `y + te` and stay
  satisfied. Inactive affine constraints of `P_ex` keep their slack for small
  `t`. □

*Nonlinear exact constraints.* The polyhedrality hypothesis can be removed.
Replace the ray `y + te` by a `C^1` curve with initial velocity `e` that keeps
the active exact constraints at their values at `y`. LICQ and the implicit
function theorem give such curves uniformly for `y` near `z*`, and Theorem 5.4
then holds with changed constants. This extension is sketched only (review,
Section 3) and is not used below.

With `Y = M` a Morse–Bott optimal manifold along which (OD) holds uniformly,
Theorem 5.4 gives `N_opt >= c eps^(-p/2)` for constraint-gap schemes. A
covering bound at a single scale gives only `O(1)` at an isolated KKT point.
The multi-scale integral version follows.

**Proposition 5.6 (integral form via a shift).** Let `P` satisfy (D) with
`beta > 0`. Let `S subset F` be a `d`-dimensional embedded `C^1`
submanifold. Let `Z : S -> X0 ∩ P_ex` be an injective `C^1` map whose image
`S'` is an embedded `C^1` submanifold, with Jacobian `J_Z >= j_0 > 0`, such
that for all `y in S`:

- `f(Z(y)) < f* - eps`;
- `v(Z(y)) <= A_1 (m(y) + eps)`.

Then

```
|P| >= (beta/A_1)^(d/2) j_0 integral_S (m + eps)^(-d/2) dσ / (C_{n,d} M(S')).
```

*Proof.*
1. Let `y in S` and `C in P` with `Z(y) in C`. By (D) and the first
   condition, `beta q_C(Z(y)) < v(Z(y)) <= A_1(m(y)+eps)`. So
   `(m(y)+eps)^(-d/2) <= (A_1/beta)^(d/2) q_C(Z(y))^(-d/2)`.
2. By the area formula for the injective map `Z`,
   `integral_{Z^(-1)(C)} q_C(Z(y))^(-d/2) J_Z(y) dσ(y) = integral_{S'∩C} q_C^(-d/2) dσ'`.
   Lemma 4.1 bounds the right side by `C_{n,d} M(S')`.
3. Hence
   `integral_{Z^(-1)(C)} (m+eps)^(-d/2) dσ <= (A_1/beta)^(d/2) C_{n,d} M(S')/j_0`.
4. The sets `Z^(-1)(C)`, `C in P`, cover `S`. Sum over `C`. □

**Theorem 5.7 (constraint-gap schemes at KKT points).** Let `z*` be a global
minimizer (`m(z*) = 0`) satisfying the hypotheses of Lemma 5.5. These include
LICQ, `P_ex` polyhedral near `z*`, and some active non-exact constraint with a
nonzero multiplier. Let `f, g, h` be `C^2` near `z*`. Let
`S_loc = {y : |y - z*| < rho, g_j(y) = 0 (j in A), h(y) = 0}`, which is a
`d`-dimensional `C^2` manifold, and assume `d >= 1`. Let `P` satisfy (D) with
`beta > 0`. Then there are `c, eps_0 > 0` such that, for `0 < eps <= eps_0`,

```
|P| >= c log(1/eps).
```

SOSC is not needed. In particular, under (T_{0,beta}), `N_opt(eps)` grows at
least logarithmically even though the objective is relaxed exactly.

*Proof.*

1. *Graph.* By LICQ and the implicit function theorem, for small `rho`,
   `S_loc ∩ B(z*, rho) = {z* + x + phi(x) : x in U}`. Here `T = T_{z*} S_loc`,
   `U subset T` is a neighbourhood of 0, `phi : U -> T^⊥` is `C^2`, and
   `phi(0) = 0`, `D phi(0) = 0`. Shrinking `rho`, the inactive constraints
   have negative values and `S_loc subset F`.

2. *Shift.* Let `e`, `mu_0`, `c_1`, `C_2`, `t_1` be as in Lemma 5.5, and
   define `Z_eps(y) = y + 3(m(y) + eps) e/mu_0 = Z_0(y) + (3 eps/mu_0) e`.
   - So `Z_eps` is `Z_0` followed by a translation. This does not change
     Jacobians, injectivity, two-point constants or multiplicities.
   - In graph coordinates,
     `Z_0(z* + x + phi(x)) = z* + psi(x) + phi(x) + (3/mu_0) m~(x) e_N`,
     where `m~(x) = m(z* + x + phi(x))`, `e = e_T + e_N` is split along
     `T ⊕ T^⊥`, and `psi(x) = x + (3/mu_0) m~(x) e_T`.
   - Since `z*` minimizes `m >= 0` on `S_loc subset F`, we have
     `m~(0) = 0` and `grad m~(0) = 0`. So `D psi(0) = I`.
   - Shrink `U` so that `||D psi - I|| <= 1/2` on `U`. Then `psi` is a `C^2`
     diffeomorphism onto its image, and the image contains a ball `V_0`.
     Restrict `S` to `S = {z* + x + phi(x) : psi(x) in V_0}`.
   - Then `Z_0(S) = {z* + x' + phi'(x') : x' in V_0}`, where
     `phi' = (phi + (3/mu_0) m~ e_N) ∘ psi^(-1)` is `C^2` with Hessian bounded
     by some `K_2'` on the convex set `V_0`.
   - By Lemma 4.3, `Z_0(S)` has two-point constant `1/K_2'`. Shrinking `V_0`
     so that `diam Z_0(S) < rho_*`, Lemma 4.2 gives
     `M(Z_eps(S)) <= binom(n,d)`.
   - The Jacobian of `Z_0` is at least
     `j_0 = 2^(-d) (1 + sup||D phi||^2)^(-d/2) > 0`: the area factors of the
     two graphs lie in `[1, (1 + ||D.||^2)^(d/2)]`, and `psi` has Jacobian at
     least `2^(-d)`.

3. *Conditions of Proposition 5.6.* For `y in S` with `m(y) + eps` small
   enough, the computation in the proof of Theorem 5.4 with
   `t_* = 3(m(y)+eps)/mu_0` and (OD) from Lemma 5.5 gives two facts.
   - `f(Z_eps(y)) < f* - eps`.
   - `v(Z_eps(y)) <= A_1 (m(y) + eps)` with `A_1 = 3 c_1/mu_0`.
   Shrink `S` and `eps_0` so that this holds for all `y in S`: `m <= M_L rho^2/2`
   on `S`.

4. *The integral.* On `S_loc`, `m = L - f*`, where `L` is the Lagrangian with
   the KKT multipliers. By Taylor's theorem, `m(y) <= (M_L/2)|y - z*|^2`, with
   `M_L` a bound on `||grad^2 L||` near `z*`. The graph over the ball of radius
   `r/(1 + sup||D phi||)` in `T` lies in `B(z*, r)`. Hence
   `V(r) := H^d(S ∩ B(z*, r)) >= omega_d (r/(1+sup||D phi||))^d =: theta_0 r^d`
   for `r <= r_1`.
   With `phi_eps(r) = ((M_L/2) r^2 + eps)^(-d/2)`, decreasing in `r`, the
   layer-cake formula gives
   `integral_S (m+eps)^(-d/2) dσ >= integral_0^{r_1} V(r) (-phi_eps'(r)) dr`.
   On `r >= (2 eps/M_L)^(1/2)`, `(M_L/2) r^2 + eps <= M_L r^2`, so
   `-phi_eps'(r) >= (d M_L/2) r (M_L r^2)^(-d/2-1)`. Therefore

   ```
   integral_S (m+eps)^(-d/2) dσ >= theta_0 (d/2) M_L^(-d/2) integral_{(2eps/M_L)^(1/2)}^{r_1} dr/r
                                 = theta_0 (d/4) M_L^(-d/2) log(M_L r_1^2/(2 eps)).
   ```

5. Proposition 5.6 gives
   `|P| >= (beta mu_0/(3 c_1))^(d/2) j_0 theta_0 (d/4) M_L^(-d/2) log(M_L r_1^2/(2eps)) / (C_{n,d} binom(n,d))`. □

*A natural instance.* The review checked Theorem 5.7 on
`min |y - c|^2` subject to `|y| >= 1`, with the secant relaxation of the
reverse-convex constraint (a genuine (T_{0,1}) scheme, `d = 1`). Widest-side
bisection counts grow logarithmically (19 to 159 nodes for
`eps = 1e-1 … 1e-9`), and (D) holds on every leaf
(`reviews/spatial-constrained/reverse_convex_tube.py`; not re-run here).

The prefactor is `(beta mu_0/(c_1 M_L))^(d/2)`. The effective objective gap is
`beta mu_0/c_1`: the constraint gap times the multiplier, divided by the
violation rate. This is the same Lagrangian mechanism as in the cluster-free
theorem ([results note](../../../results/cluster-free-branch-and-bound-constrained-minima.md),
Theorem 1), run in the opposite direction.

**Remark 5.8 (what the constraint-gap lower bounds exclude).** Lemma 2.1(c)
and Example 5.3(c) show that the bounds of this section hold only for runs
whose reductions use the relaxation itself. Exact propagation of the original
constraints can remove the super-optimal infeasible points that carry the
bound.
- For flat, axis-aligned strata it removes the whole effect.
- For curved strata, interval propagation replaces a box `B` by the hull of
  `B ∩ F`. That hull still contains infeasible points near the curved
  boundary.

Whether the exponent survives propagation for strictly curved strata is open
(Section 11).

## 6. Upper bounds for bisection with constraints

**Model.** `X0` is a cube of side `s0`. `T_bis` is the uniform `2^n`-ary
dyadic refinement with `UBD = f*`, as in Theorem 3.3. Level-`j` cells are the
closed dyadic cubes of side `s_j = s0 2^(-j)`. `N_j(A)` is the number of
closed level-`j` cells meeting `A`. The leaves of `T_bis` form a certificate,
so `N_opt(eps) <= |T_bis|`. Constants:

```
Lambda = tau (1 + L kappa),     j_0 = min{ j >= 0 : tau s_j^2 <= v_0 and kappa tau s_j <= 1 },
J = #{ j >= 0 : Lambda s_j^2 > eps } = max(0, ceil(log2(s0 sqrt(Lambda/eps)))).
```

**Lemma 6.1 (localization).** Assume (U_tau), (EB) and (Lip). Let `D` be a
level-`j` cube with `j >= j_0` that is not pruned at tolerance `eps`. Then
`eps < Lambda s_j^2`, and some `y in E(Lambda s_j^2 - eps)` has
`dist_inf(y, D) <= kappa tau s_j^2 <= s_j`. Consequently

```
|T_bis| <= 1 + 2^n [ 2^(n j_0) + 5^n sum_{j >= j_0, Lambda s_j^2 > eps} N_j(E(Lambda s_j^2 - eps)) ].
```

*Proof.*
1. `LB(D) < f* - eps`, so some `z in R_D` has `f_D(z) < f* - eps`. By
   (U_tau), `f(z) < f* - eps + tau s_j^2` and `v(z) <= tau s_j^2 <= v_0`.
2. By (EB), some `y in F` has `|y - z|_2 <= kappa tau s_j^2`. By (Lip),
   `f(y) <= f(z) + L kappa tau s_j^2 < f* - eps + Lambda s_j^2`. So
   `0 <= m(y) < Lambda s_j^2 - eps`, and `dist_inf(y, D) <= |y - z|_inf <= s_j`.
3. If `y` lies in the closed cell `G`, every cell `D` with
   `dist_inf(y, D) <= s_j` is within index distance 2 of `G` in each
   coordinate: `D_i = [delta, delta + s]` with `delta > g + s` forces
   `delta - y_i <= s`, hence `delta <= g + 2s`. So at most `5^n` cubes `D`
   are charged to each cell meeting `E(Lambda s_j^2 - eps)`.
4. Levels `j < j_0` contain at most `2^(nj)` cubes, and
   `sum_{j < j_0} 2^(nj) <= 2^(n j_0)`. Each non-pruned cube has `2^n`
   children, and the root is processed. □

**Theorem 6.2 (constrained version of Theorem 3.3).** Assume (U_tau), (EB)
and (Lip). Let `P` be any family that is `alpha`-valid on `F`: a
certificate under (G^LB_alpha), or the leaf-and-piece family of any run in
Lemma 2.1. Then

```
|T_bis| <= 1 + 2^n [ 2^(n j_0) + 10^n (2 sqrt(Lambda/alpha) + 2)^n J |P| ].
```

*Proof.* Let `y in E(Lambda s_j^2 - eps) ∩ C` with `C in P`. By (V),
`alpha d_i(y)^2 <= alpha q_C(y) <= m(y) + eps <= Lambda s_j^2`, so
`y in Q(v, sqrt(Lambda/alpha) s_j)` for a vertex `v` of `C`. A closed interval
of length `2r` meets at most `2r/s + 2` closed cells of length `s`. So
`N_j(E(Lambda s_j^2 - eps)) <= 2^n (2 sqrt(Lambda/alpha) + 2)^n |P|`. Insert
this into Lemma 6.1. □

Only members of `P` that meet `F` are used, so `|P|` may be replaced by
`|P_F| = #{C in P : C ∩ F ≠ ∅}`. The tightening statement below relies on
this.

In the unconstrained case, `kappa = 0`, `j_0 = 0` and `tau = alpha' n/4`. Then
Theorem 6.2 is Theorem 3.3 with slightly different constants. The hypothesis
`F = X0` is replaced by the error bound. By Lemma 2.1(d), for any run with
same-relaxation reductions,

```
|T_bis| <= C_0 + C_1 log(1/eps) (#leaves + 2n #(R-rel rounds)).
```

So such tightening can save at most a factor `O(log(1/eps))` against plain
bisection. The scout's sharp 1D data show that it can save that much
(review, Section 3).

### 6.1 The covering characterization

Define the **parabolic covering profile**

```
Phi_alpha(eps) = sup_{eta >= 0} N_inf( E(eta), 2 sqrt((eps + eta)/alpha) ).
```

**Theorem 6.3 (N_opt and bisection within a log factor of `Phi_alpha`).**
Assume (G^LB_alpha), (U_tau), (EB) and (Lip). For every `eps > 0`,

```
2^(-n) Phi_alpha(eps) <= N_opt(eps) <= |T_bis| <= 1 + 2^n [ 2^(n j_0) + 15^n max(1, ceil(2 sqrt(Lambda/alpha)))^n J Phi_alpha(eps) ].
```

*Proof.*
- *Lower bound.* Apply Theorem 4.6 for every `eta`.
- *Upper bound.* Let `t = Lambda s_j^2 - eps >= 0`.
  - A closed cube of side `s_j` meets at most `3^n` closed level-`j` cells,
    so `N_j(E(t)) <= 3^n N_inf(E(t), s_j)`.
  - Covering by cubes of side `s_j` needs at most `max(1, ceil(a))^n` times
    as many cubes as covering by side `a s_j`. With
    `a s_j = 2 sqrt(Lambda/alpha) s_j = 2 sqrt((eps + t)/alpha)`, this gives
    `N_inf(E(t), s_j) <= max(1, ceil(2 sqrt(Lambda/alpha)))^n Phi_alpha(eps)`.
  - Insert into Lemma 6.1. There are at most `J` levels. □

**Remark 6.3a (what `Phi_alpha` measures; the supremum is needed).**

(i) *Running supremum.* Let `psi_alpha(eta) = N_inf(E(eta), 2 sqrt(eta/alpha))`.
A cube of side `2 sqrt(eta/alpha)` is a ball of radius `eta` for the
semi-metric `ell(x,y) = alpha |x - y|_inf^2`. So `psi_alpha` is a Munos-type
covering profile of the near-optimal sets. Munos (2011) defines the
near-optimality dimension with packings by `ell`-balls of radius `nu eta`,
where `nu` is a free constant, so the identification holds up to constants.
Its growth exponent as `eta -> 0` is the near-optimality dimension. Then

```
2^(-n) sup_{eta >= eps} psi_alpha(eta)  <=  Phi_alpha(eps)  <=  sup_{eta >= eps} psi_alpha(eta).
```

*Proof.* Covering by cubes of side `s` needs at most `ceil(a)^n` times as many
cubes as covering by cubes of side `a s`.
- For `eta >= eps`, the scale `2 sqrt((eps+eta)/alpha)` lies between
  `2 sqrt(eta/alpha)` and `2 sqrt(2 eta/alpha)`, and `ceil(sqrt 2) = 2`. So
  the `eta`-term of `Phi_alpha` lies between `2^(-n) psi_alpha(eta)` and
  `psi_alpha(eta)`.
- For `eta < eps`, `E(eta) subset E(eps)` and the scale is at least
  `2 sqrt(eps/alpha)`. So the term is at most `psi_alpha(eps)`. □

So `Phi_alpha(eps)` is, within a factor `2^n`, the **running supremum** over
`eta >= eps` of the Munos-type profile, not the profile at `eta = eps`. The
review's exact 1D computation found `sup psi` between `Phi` and `2 Phi`
(`reviews/spatial-constrained-recheck/remark63a_family.log`).

(ii) *A single-scale version fails with uniform constants.* No bound
`N_opt(eps) <= C log(1/eps) N_inf(E(eps), c sqrt(eps))` holds with `C, c`
depending only on `n` and the scheme constants. Take `n = 1`, `X0 = F = [0,1]`
and

```
f_K(y) = K^(-2) (1 - cos(2 pi K t)) + K^(-2) (1 - exp(-K^2 t^2)),   t = y - 1/2,
```

with exact alphaBB and `alpha = alpha' = 32`.

- *The scheme and the role of `alpha`.*
  - Exact alphaBB, `f_B = f - alpha q_B`, satisfies (G^pt_alpha) and
    (U^q_alpha) with equality for **every** `alpha`. The lower bound needs
    nothing about `f`.
  - The real requirement on `alpha` is that `f_B` be a convex underestimator
    (Section 1.5): `alpha >= -min f_K''/2`. Termwise
    `f_K'' = 4 pi^2 cos(2 pi K t) + (2 - 4u^2) e^(-u^2)` with `u = K t`. The
    second term is at least `-4 e^(-3/2)`, its minimum at `u^2 = 3/2`. So
    `alpha >= 20.19` suffices; the review found `-min f_K''/2 ≈ 20.11`
    numerically.
  - The covering step below needs only `alpha > 8`.
  - So `alpha = 32` works for every `K`, and all scheme constants are uniform
    in `K`.
- *Minimizer and growth.* `f* = 0` at `t = 0`. For `|t| <= 1/(2K)`,
  `1 - cos x >= 2x^2/pi^2` gives `m >= 8 t^2`. For `|t| >= 1/(2K)`, the second
  term gives `m >= K^(-2)(1 - e^(-1/4)) > 0.22 K^(-2)`.
- *The single-scale profile is bounded.* For `eps < 0.22 K^(-2)`,
  `E(eps) subset {|t| <= (eps/8)^(1/2)}`. So
  `N_inf(E(eps), c sqrt(eps)) <= 1/(sqrt(2) c) + 2`, independent of `K`.
- *`N_opt` is large.* The points `t_k = k/K`, `|k| <= K/2` (including
  `t_0 = 0`), number `2 floor(K/2) + 1 >= K`, and they have
  `m(t_k) = K^(-2)(1 - e^(-k^2)) <= K^(-2)`.
  - Apply Theorem 4.6 with `eta = K^(-2)` and `eps < K^(-2)`.
  - The cubes have side
    `2 ((eps + eta)/alpha)^(1/2) < 2 (2/(alpha K^2))^(1/2)`. This is less than
    the spacing `1/K` iff `alpha > 8`, and equals `1/(2K)` at `alpha = 32`.
  - So each cube contains at most one `t_k`, and `N_opt(eps) >= K/2`.
- *Conclusion.* At `eps = 0.2 K^(-2)`, `N_opt >= K/2`, while
  `C log(1/eps) N_inf(E(eps), c sqrt(eps)) = O(log K)`. □

**Interpretation.** Theorem 6.3 says:

- under a two-sided second-order relaxation scheme, the running supremum of a
  Munos-type near-optimality profile for the semi-metric `alpha |x - y|_inf^2`
  is, up to a factor `4^(-n)`, a **lower** bound for every branch-and-bound
  certificate, with constraints;
- uniform bisection attains it within `C log(1/eps)`.

In the Lipschitz setting, the analogous two-sided statement is
Bachoc–Cesari–Gerchinovitz (2021), with semi-metric `|x - y|`. The log factor
cannot be removed for bisection (Example 3.4, Remark 6.9). It can be removed
when the profile grows geometrically along dyadic scales, as in Theorems 6.4
and 6.6.

**Theorem 6.4 (quadratic growth to the optimal set).** Assume (G^LB_alpha),
(U_tau), (EB), (Lip) and

```
(QG)   m(y) >= c_g dist_inf(y, M)^2    for all y in F.
```

Then for `eps > 0`, with `J' = {j >= j_0 : Lambda s_j^2 > eps}`,

```
2^(-n) N_inf(M, 2 sqrt(eps/alpha)) <= N_opt(eps) <= |T_bis| <= 1 + 2^n [ 2^(n j_0) + 5^n (2 sqrt(Lambda/c_g) + 3)^n sum_{j in J'} N_j(M) ].
```

*Proof.*
- *Lower bound.* Theorem 4.6 with `eta = 0`.
- *Upper bound.* By (QG), `E(Lambda s_j^2) subset {y : dist_inf(y, M) <= r}`
  with `r = sqrt(Lambda/c_g) s_j`. A closed cell `G` meeting `Q(x, r)`, for
  `x in M` lying in a closed cell `G'`, has index offset at most
  `r/s_j + 1` from `G'` in each coordinate. That gives at most `2r/s_j + 3`
  values per coordinate. So `N_j(E(Lambda s_j^2)) <= (2 sqrt(Lambda/c_g) + 3)^n N_j(M)`.
  Insert into Lemma 6.1. □

The upper bound uses only (U_tau), (EB), (Lip) and (QG), not (G^LB_alpha).

**Corollary 6.5 (the exponent is half the dimension of the optimal set).**
Under the hypotheses of Theorem 6.4:

(a) `liminf log N_opt(eps)/log(1/eps) >= dim_low(M)/2`, and
`limsup log |T_bis|/log(1/eps) <= dim_up(M)/2` when `dim_up(M) > 0`. Here
`dim_low` and `dim_up` are the lower and upper box-counting dimensions.

(b) If `M` has box-counting dimension `p > 0`, both exponents equal `p/2`. If
`M` is finite, `1 <= N_opt(eps) <= |T_bis| <= C_0 + 20^n (2 sqrt(Lambda/c_g) + 3)^n |M| J`.
Here `C_0 = 1 + 2^(n(j_0+1))`.

*Proof.*
- (a) The lower half is Corollary 4.7(b).
- (a), upper half. `N_j(M) <= 3^n N_inf(M, s_j) <= 3^n s_j^(-dim_up(M) - delta)`
  for any `delta > 0` and all small `s_j`. Summing over
  `s_j >= (eps/Lambda)^(1/2)` gives `O(eps^(-(dim_up(M)+delta)/2))`.
- (b) For finite `M`, a point meets at most `2^n` closed cells, so
  `N_j(M) <= 2^n |M|`. □

### 6.2 Integral form under stratified regularity

**Hypothesis (R).** Strata `S_1, ..., S_{K_S} subset F` are given. Each `S_k` is a
`d_k`-dimensional embedded `C^1` submanifold (`d_k >= 1`) or a finite set
(`d_k = 0`). There are constants `t_0, r_0, theta > 0` and `K_R, K >= 1` such
that:

- **(R1) parabolic proximity:** for `t <= t_0`, every `y in E(t)` has some
  `k` and `y' in S_k` with `|y - y'|_inf <= sqrt(K_R t)` and
  `m(y') <= K_R t`;
- **(R2) quadratic doubling along strata:** for `x, z in S_k` with
  `m(z) <= K_R t_0` and `|x - z|_inf <= r_0`,
  `m(x) <= K (m(z) + |x - z|_inf^2)`;
- **(R3) lower density:** for `z in S_k` with `m(z) <= K_R t_0` and
  `r <= r_0`, `H^(d_k)(S_k ∩ Q(z, r)) >= theta r^(d_k)`.

Condition (R1) says that the near-optimal feasible set lies within parabolic
distance of the strata. Points of `F` whose `m` grows linearly away from a
stratum, such as the interior of `F` near an active constraint with a positive
multiplier, need no stratum of their own.

**Theorem 6.6 (integral upper bound).** Assume (U_tau), (EB), (Lip) and (R).
Put:

```
rho = sqrt(K_R Lambda),   Lambda' = K (K_R Lambda + 1/4) + Lambda,
j_1 = min{ j >= j_0 : Lambda s_j^2 <= t_0, s_j <= 2 r_0 },
I_k(eps) = integral_{S_k} (m + eps)^(-d_k/2) dσ   (d_k >= 1).
```

Then

```
|T_bis| <= 1 + 2^n [ 2^(n j_1) + (2 rho + 6)^n ( sum_{k : d_k >= 1} (2^(d_k + 1)/theta) Lambda'^(d_k/2) I_k(eps) + J sum_{k : d_k = 0} #S_k ) ].
```

*Proof.* Let `j >= j_1` with `Lambda s_j^2 > eps`, and let `D` be a
non-pruned level-`j` cube.

1. By Lemma 6.1, some `y in E(Lambda s_j^2)` has `dist_inf(y, D) <= s_j`.
   By (R1) with `t = Lambda s_j^2 <= t_0`, some `y' in S_k` has
   `|y - y'|_inf <= rho s_j` and `m(y') <= K_R Lambda s_j^2`.
2. Let `Z_k` be a maximal subset of `Y_k = {y' in S_k : m(y') <= K_R Lambda s_j^2}`
   with pairwise sup-distances `> s_j`. Some `z in Z_k` has
   `|y' - z|_inf <= s_j`, so `dist_inf(z, D) <= (rho + 2) s_j`.
3. A closed level-`j` cell `D` with `dist_inf(z, D) <= R s_j` has its lower
   corner in an interval of length `(2R + 1) s_j` in each coordinate. So at
   most `(2R + 2)^n = (2 rho + 6)^n` cells are charged to each `z`.
4. For `d_k = 0`, `|Z_k| <= #S_k`.
5. For `d_k >= 1`, the cubes `Q(z, s_j/2)`, `z in Z_k`, are pairwise
   disjoint.
   - For `x in S_k ∩ Q(z, s_j/2)`, (R2) (with `s_j/2 <= r_0` and
     `m(z) <= K_R t_0`) and `eps < Lambda s_j^2` give
     `m(x) + eps <= K(K_R Lambda + 1/4) s_j^2 + Lambda s_j^2 = Lambda' s_j^2`.
   - (R3) gives `|Z_k| theta (s_j/2)^(d_k) <= V_k(Lambda' s_j^2)`, where
     `V_k(t) = H^(d_k)(S_k ∩ {m + eps <= t})`.
6. Summing over `j`:
   `sum_j s_j^(-d) V_k(Lambda' s_j^2) = integral_{S_k} sum_{j : s_j >= theta(x)} s_j^(-d) dσ(x)`,
   with `theta(x) = ((m(x)+eps)/Lambda')^(1/2)`. The inner geometric sum is at
   most `2 theta(x)^(-d)` for `d >= 1`.
7. Levels `j < j_1` contribute at most `2^(n j_1)` cubes. □

**Theorem 6.7 (two-sided integral characterization).** Assume (G^LB_alpha),
(U_tau), (EB), (Lip) and (R) with all `d_k >= 1`, and `M(S_k) < inf` for each
`k`. The last condition holds, for example, if `S_k subset X0` has a positive
two-point constant (Lemma 4.2). Then for every `eps > 0`,

```
c_low sum_k I_k(eps) <= N_opt(eps) <= |T_bis| <= C_0 + C_up sum_k I_k(eps),
c_low = (1/K_S) min_k alpha^(d_k/2)/(C_{n,d_k} M(S_k)),
C_up  = 2^n (2 rho + 6)^n max_k 2^(d_k+1) Lambda'^(d_k/2)/theta,
C_0   = 1 + 2^(n (j_1 + 1)).
```

If some strata are finite sets, the upper bound gains
`2^n (2 rho + 6)^n J #(points)`. The lower bound keeps the strata of positive
dimension; points contribute `N_opt >= 1`.

*Proof.* The lower bound is Theorem 4.5(i) with Corollary 4.7(a). The upper
bound is Theorem 6.6. □

**Where the constants come from.**
- `alpha^(d/2)` in the lower bound: the objective gap.
- `Lambda'^(d/2)`, with `Lambda' ~ K K_R tau (1 + L kappa)`, in the upper
  bound: the relaxation error, the error bound and the growth and doubling of
  `m` along the strata.
- The multiplicity `M(S_k)` and the density `theta`: the global and local
  geometry of the strata. By Lemma 4.2, `M(S_k)` is controlled by the reach.
- `C_{n,d}` and `(2 rho + 6)^n`: dimension.

Both constants are independent of `eps`. Their ratio is not `e^{O(n)}` in
general (Remark 3.7).

### 6.3 Sharp minimizers and the log factor

**Proposition 6.8 (an `O(1)` certificate at a sharp minimizer).** Assume
(U^q_{alpha'}), (EB), (Lip) and sharp growth `m(y) >= c |y - z*|_2` on `F`
for some `z* in F`. Let `K' = (1 + L kappa + c kappa) alpha'` and

```
s_V = min( c/(K' sqrt(n)), 4c/(K' n), 2 sqrt(v_0/(n alpha')) ).
```

For every `s in (0, s_V]`, the grid of side `s` with `z*` as a grid point,
clipped to `X0`, is a certificate for every `eps >= 0`. Hence
`N_opt(eps) <= (s0/s_V + 2)^n` for all `eps >= 0`, including `eps = 0`.

*Proof.* Let `C` be a clipped cell and `z in R_C`.
1. `v(z) <= alpha' q_C(z) <= alpha' n s^2/4 <= v_0`. Let `y` be a nearest
   point of `F`, so `|y - z| <= kappa alpha' q_C(z)`.
2. Then
   `f_C(z) >= f(z) - alpha' q_C(z) >= f(y) - (1 + L kappa) alpha' q_C(z) >= f* + c|y - z*| - (1 + L kappa) alpha' q_C(z)`,
   and so `f_C(z) - f* >= c |z - z*| - K' q_C(z)`.
3. *Cells with vertex `z*`.* Clipping keeps `z*` a vertex. In each
   coordinate one factor of `a_i(z)` is `|z_i - z*_i|` and the other is at
   most `s`. So `q_C(z) <= s |z - z*|_1 <= s sqrt(n) |z - z*|`, and
   `f_C(z) - f* >= |z - z*| (c - K' s sqrt n) >= 0`.
4. *Other cells.* `z*` is a grid point, so `|z - z*| >= |z - z*|_inf >= s`,
   and `q_C <= n s^2/4`. Hence `f_C(z) - f* >= c s - K' n s^2/4 >= 0`.
5. So every cell has `LB(C) >= f*` or an empty relaxation. The count is at
   most `prod_i (ceil((U_i - L_i)/s) + 1)`. □

For unconstrained problems (`kappa = 0`, `L` irrelevant), this is the scout's
sharp-minimum row. It needs the **vertex-vanishing** upper gap (U^q). Under
(U_tau) alone, a relaxation error `tau w^2` that is positive at the vertex
`z*` prevents pruning for `eps < tau s^2`.

**Remark 6.9 (bisection at a vertex minimizer).** Assume (G^LB_alpha). Let
`z* in M` lie in the level-`j` cell `D`, with some coordinate satisfying
`z*_i in [l_i + delta s_j, u_i - delta s_j]`. Then
`LB(D) <= f* - alpha q_D(z*) <= f* - alpha delta(1-delta) s_j^2`, so `D` is
not pruned when `alpha delta (1-delta) s_j^2 > eps`.
- If some `(z*_i - L_i)/s0` is rational with odd denominator `q > 1`, the
  relative position of `z*_i` in every dyadic cell is a fraction with
  denominator `q`. The condition then holds at every level with
  `delta = 1/q`, so `|T_bis| >= log2(s0 (alpha (q-1)/(q^2 eps))^(1/2)) - 1`.
- The upper bound `O(log(1/eps))` always holds (Corollary 6.5(b)).

So at sharp minimizers, bisection loses exactly a `log(1/eps)` factor against
`N_opt` for such positions, and less for positions with sparse binary digits
(review, Section 6).

**Remark 6.10 (binary widest-side bisection).** Binary widest-side bisection
from a cube produces, at depth `nj + r` (`0 <= r < n`), boxes of width `s_j`
contained in level-`j` cubes. Lemma 6.1 applies with `w = s_j`, and each
level-`j` cube contains `2^r` boxes of depth `nj + r`. So the number of
non-pruned boxes with depth in `[nj, nj + n)` is at most
`(2^n - 1) 5^n N_j(E(Lambda s_j^2 - eps))`. Since `|T_bin| = 1 + 2 #(non-pruned)`,
all bounds of this section hold for binary bisection with the factor `2^n`
replaced by 2 and an extra factor `2^n` inside.

## 7. Regular instances

### 7.1 Nondegenerate KKT points

**Theorem 7.1.** Let the set of global minimizers be finite,
`M = {z*_1, ..., z*_N}`. Parts (a) and (c) allow `N >= 1`; part (b) assumes
`N = 1`. Assume that `f, g, h` are `C^2` near each `z* in M`, and that each
`z*` satisfies (KKT), (LICQ), (SC) and (SOSC) with constant `gamma`, as in the
[cluster-free note](../../../results/cluster-free-branch-and-bound-constrained-minima.md)
(Section 1). Active bounds of `X0` and active constraints of `P_ex` are
counted among the `g_j`. For a minimizer `z*`, let `a = |A| + r` be the number
of active constraints, and `d = n - a` the dimension of the active stratum
`S_loc = {y near z* : g_A(y) = 0, h(y) = 0}`. Let `M_L` bound
`||grad^2 L||` near `z*`, where `L` is the Lagrangian with the KKT
multipliers. Assume (U_tau), (EB) and (Lip).

*Which description.* In (a) and (b), the conditions (KKT)–(SOSC), the stratum
`S_loc` and `M_L` may be taken in **any** `C^2` description of
`F ∩ B(z*, rho)` by finitely many constraints. It need not be the description
used by the relaxation and in (U_tau) and (EB). The proofs use these
conditions only to obtain (QG), sharp growth in (b), and the local graph
structure of `S_loc`, which depend only on `F` near `z*`. Under LICQ, `S_loc`
is the stratum of `F` through `z*`, so `d` does not depend on the description.
Part (c) uses the relaxation's own constraints, because Lemma 5.5 refers to
them.

(a) If `d >= 1` at some `z* in M` and (G^LB_alpha) holds, there are
`c_a, C_a, eps_0 > 0` such that for `0 < eps <= eps_0`

```
c_a (alpha/M_L)^(d/2) log(1/eps) <= N_opt(eps) <= |T_bis| <= C_a log(1/eps).
```

Here `c_a` depends only on `n`, `d` and the graph constants of `S_loc`
near that `z*`. `(alpha/M_L)^(d/2)` is the lower-bound prefactor; the upper
constant `C_a` has a different form (Section 11, item 2).

(b) If `N = 1` and `d = 0`, then under (U^q_{alpha'}), `N_opt(eps) <= C_b` for every
`eps >= 0`, while `|T_bis| <= C_a log(1/eps)`. Under (G^LB_alpha),
`|T_bis| = Omega(log(1/eps))` whenever `z*` satisfies the middle-part
condition of Remark 6.9, for example with a rational coordinate of odd
denominator.

(c) Assume (T_{0,beta}) instead of (G^LB), and at some `z* in M` with
`d >= 1`: some active non-exact constraint has a nonzero multiplier, and
`P_ex` is polyhedral near `z*` (the hypotheses of Lemma 5.5). Then Theorem 5.7
gives `N_opt(eps) >= c log(1/eps)`. Under (SC) a nonzero multiplier is
automatic for active inequalities, but not for equalities. The upper bound of
(a) holds unchanged.

*Proof.*

*Quadratic growth.* By the cluster-free note, Theorem 1 applied to degenerate
boxes `Z = {y}` with an exact relaxation (`w(Z) = 0`), and by the classical
second-order sufficient condition, `m(y) >= (gamma/4)|y - z*|^2` for
`y in F ∩ B(z*, rho)`, for each `z* in M`, with `rho` smaller than half the
least distance between minimizers. `F` is compact and `M` is the whole
optimal set, so `m >= c' > 0` on `F` minus the union of these balls. Hence
(QG) holds with `c_g = min(gamma/4, c'/(n s0^2))`.

(a) *Upper bound.* Corollary 6.5(b) with `|M| = N`.

(a) *Lower bound.* Apply the following at one minimizer `z*` with `d >= 1`.
1. By LICQ and the implicit function theorem, `S_loc` near `z*` is a graph
   `{z* + x + phi(x)}` over `T = T_{z*} S_loc`, with `D phi(0) = 0`, as in
   the proof of Theorem 5.7.
2. By Lemma 4.3 it has a positive two-point constant on a small convex piece
   `S`. `S subset F` once `rho` is small, since inactive constraints stay
   negative.
3. On `S`, `m = L - f*`. Since `grad L(z*) = 0`, Taylor's theorem gives
   `m(y) <= (M_L/2)|y - z*|^2`.
4. Step 4 of the proof of Theorem 5.7 gives
   `integral_{S ∩ B(z*, r_1)} (m+eps)^(-d/2) dσ >= theta_0 (d/4) M_L^(-d/2) log(M_L r_1^2/(2 eps))`.
5. Choose `r_1` so small that `M_L r_1^2/2 < alpha r_*^2/2`. Then for
   `eps < alpha r_*^2/2`, `S ∩ B(z*, r_1) subset S_♭`, and Theorem 4.5(ii)
   applies. (For `d = n` use Theorem 4.5(iii).)

(b) *Sharp growth.* Let `delta = y - z*` for `y in F` near `z*`, and let
`mu_min = min_{j in A} mu*_j > 0`.
1. On `F`, `h(y) = 0` and `g_j(y) <= 0`, so
   `m(y) = L(y) - f* + sum_{j in A} mu*_j (-g_j(y)) >= -(M_L/2)|delta|^2 + mu_min sum_A (-g_j(y))`.
2. The `n` active gradients are linearly independent. So
   `|delta| <= kappa_0 (sum_A |grad g_j(z*)·delta| + sum_k |grad h_k(z*)·delta|)`.
3. By Taylor's theorem with a Hessian bound `M`,
   `|grad h_k(z*)·delta| <= (M/2)|delta|^2`.
4. Also `|grad g_j(z*)·delta| <= -g_j(y) + (M/2)|delta|^2`: the upper side
   uses `g_j(y) <= 0`, and the lower side uses Taylor directly.
5. Hence `sum_A (-g_j(y)) >= |delta|/kappa_0 - n (M/2)|delta|^2`, and
   `m(y) >= (mu_min/(2 kappa_0)) |delta|` for `|delta| <= rho` small.
6. Uniqueness and compactness extend this to all of `F`, with a smaller
   constant. Proposition 6.8 gives `N_opt <= C_b`.

The bisection statements are Corollary 6.5(b) and Remark 6.9.

(c) Theorem 5.7 at that minimizer, and the upper bound of (a). □

**Comparison with Neumaier's heuristic.** Neumaier (2004, Section 15) argues
heuristically as follows. Covering by boxes of diameter `eps` needs at least
`const √((2Δ)^n)/(eps^n √det G)` boxes, and under `a` active constraints
"`n` must be replaced by `n - a`". Theorem 7.1(a) is a rigorous, all-scales
version for adaptive trees:
- the lower-bound prefactor is `(alpha/M_L)^(d/2)` with `d = n - a`;
- the total count is `Theta(log(1/eps))`;
- when `n - a = 0`, the count is `O(1)` for the best certificate, but not for
  bisection.

This agrees with Kannan–Barton (2017): at points where the objective grows
linearly along feasible directions (trivial critical cone, `d = 0` here),
weaker convergence suffices.

### 7.2 Morse–Bott optimal manifolds

**Theorem 7.2.** Suppose the optimal set `M` is a compact embedded `C^2`
submanifold of dimension `p >= 1`, without boundary, with reach
`tau_M > 0`. Assume (QG), (G^LB_alpha), (U_tau), (EB) and (Lip). Put
`rho_* = 2 tau_M/(1 + binom(n,p)^(1/2))`, `r_* = rho_*/(2 sqrt(n-p))` and
`theta_M = (3/4)^(p/2) omega_p`, where `omega_p` is the volume of the unit
`p`-ball. For `0 < eps < alpha r_*^2`,

```
alpha^(p/2) H^p(M) eps^(-p/2) / (2^(n-p) binom(n,p) C_{n,p})  <=  N_opt(eps)  <=  |T_bis|
     <=  C_0 + 2^n 5^n 4^n (2 sqrt(Lambda/c_g) + 3)^n (2^(p+1)/theta_M) H^p(M) (Lambda/eps)^(p/2).
```

*Proof.*
- *Lower bound.* Theorem 4.5(ii) with `S = M`, where `m = 0` and
  `S_♭ = M`. By Federer's theorem, `M` has two-point constant `tau_M`.
- *Upper bound.* Use Theorem 6.4 and bound `N_j(M)` for `s_j <= 2 tau_M`.
  1. Let `Z subset M` be maximal with pairwise sup-distances `> s_j`. Then
     `M subset union_{z in Z} Q(z, s_j)`, and each `Q(z, s_j)` meets at most
     `4^n` closed cells. So `N_j(M) <= 4^n |Z|`.
  2. The sets `M ∩ Q(z, s_j/2)` are disjoint. Each contains
     `M ∩ B_2(z, s_j/2)`, whose `H^p`-measure is at least
     `theta_M (s_j/2)^p` for `s_j/2 <= tau_M`. This is the volume bound of
     Niyogi, Smale and Weinberger (2008, Lemma 5.3):
     `vol(M ∩ B(z, r)) >= (1 - r^2/(4 tau^2))^(p/2) omega_p r^p`.
  3. Hence `|Z| <= 2^p H^p(M)/(theta_M s_j^p)`.
  4. Sum over `s_j >= (eps/Lambda)^(1/2)`. The finitely many levels with
     `s_j > 2 tau_M` go into `C_0`. □

Both sides are `Theta(H^p(M) eps^(-p/2))`. The ratio of the constants is of
order `C^n (Lambda/c_g)^(n/2) (Lambda/alpha)^(p/2)/theta_M`. The dimension
`n` enters the upper bound only through the transversal factor
`(Lambda/c_g)^(n/2)`.

**Example 7.3 (quadratic forms on spheres and balls; the computations of
Section 9).**

*Setting.* Let `f(y) = -sum_i c_i y_i^2` with
`c_1 = ... = c_k > c_{k+1} >= ...`. The feasible set is
`F = {|y| = 1}` (sphere) or `F = {|y| <= 1}` (ball), inside a cube `X0`
containing the unit ball. The relaxation is:
- alphaBB of the objective with `alpha >= c_1`;
- `|y|^2 <= 1` kept exactly;
- for the sphere, the secant relaxation of `|y|^2 >= 1`, whose margin is
  exactly `q_B`.

*Hypotheses.* The exactly kept constraint `|y|^2 <= 1` is placed in `P_ex`
(the convention of Section 5). Then (G^pt_alpha) and (U^q_{max(alpha,1)})
hold. (EB) holds with `kappa = 1`, since
`dist(z, sphere) = 1 - |z| <= 1 - |z|^2 = v(z)` for `|z| <= 1`.

*Optimal set.* `M` is the unit sphere of the top eigenspace, so `p = k - 1`.

*(QG) on the sphere.* `m(y) = sum_i (c_1 - c_i) y_i^2 >= (c_1 - c_{k+1}) |y_{>k}|^2`.
Also `dist(y, M)^2 <= |y_{>k}|^2 + (1 - |y_{<=k}|)^2 <= 2 |y_{>k}|^2`,
because `1 - |y_{<=k}| <= 1 - |y_{<=k}|^2 = |y_{>k}|^2`. So (QG) holds with
`c_g = (c_1 - c_{k+1})/2` in the Euclidean norm.

*(QG) on the ball.* `m(y) >= c_1 (1 - |y|^2) + (c_1 - c_{k+1}) |y_{>k}|^2`,
and (QG) follows similarly near `M`, and by compactness away from it.

*Predictions.* Theorem 7.2 predicts `Theta(eps^(-(k-1)/2))` for `k >= 2`, and
Theorem 7.1(a) predicts `Theta(log(1/eps))` for `k = 1` (`d = n - 1 >= 1`),
on both the sphere and the ball.

*Checking Theorem 7.1's hypotheses for `k = 1`.*
- *Sphere.* In the relaxation's description, `|y|^2 <= 1` (in `P_ex`) and
  `1 - |y|^2 <= 0` are both active at `±e_1`, with gradients `±2 e_1`, so
  LICQ fails there. Theorem 7.1 allows any `C^2` description of `F` near
  `z*`. Describe the sphere by the equality `h = |y|^2 - 1 = 0`. Then LICQ
  holds, (SC) is vacuous, and (SOSC) holds on the tangent space: the Lagrangian
  Hessian is `2 diag(c_1 - c_i)`, which is positive definite on `e_1^⊥`
  because `c_1 > c_2`. The minimizers `±e_1` are two nondegenerate KKT points
  with `d = n - 1`.
- *Ball.* Only `|y|^2 <= 1` is active, with multiplier `c_1 > 0`. LICQ, (SC)
  and (SOSC) hold with the same Hessian.

*Ball versus the naive integral.* For the ball, the minimizers lie on the
boundary stratum `{|y| = 1}`, where `m` grows linearly into the interior. The
full-dimensional integral `integral_F (m+eps)^(-n/2)` then grows only like
`eps^(-(p-1)/2)` for `p >= 2`, or `log(1/eps)` for `p = 1`: half an order
less. The count follows the boundary stratum (Section 9, Table 9.1).

*A degenerate example.* Let `f = -|y|^2 + y_2^4` on the unit circle. Then
`m = sin^4 theta` along the circle, and Theorem 6.7 applies with `S = circle`:
- (R1) is trivial, since `E(t) subset circle`;
- (R2) is (QD) for `sin^4` on the circle;
- (R3) holds with `theta = 1` for `r <= 1/2`.

So `N_opt ≍ integral (sin^4 theta + eps)^(-1/2) dtheta ≍ eps^(-1/4)`. This is
the constrained analogue of the quartic rows of Section 3.8, for a genuine
(G^pt) scheme.

## 8. Consequences

### 8.1 The exponent is half the dimension of the optimal set

By Corollaries 4.7(b) and 6.5, under (G^LB), (U), (EB), (Lip) and (QG):

```
lim_{eps -> 0} log N_opt(eps) / log(1/eps) = lim log |T_bis| / log(1/eps) = dim_box(M)/2,
```

whenever the box-counting dimension `dim_box(M) > 0` exists. For finite `M`,
`N_opt` is between 1 and `O(log(1/eps))`; Theorem 7.1 decides which. The
lower half needs neither (QG) nor any regularity of `M`. Without (QG),
degenerate growth adds to the exponent: in the quartic example
`M` is two points and the exponent is `1/4` (Section 3.8, Example 7.3).

*Symmetric problems.* Suppose a compact connected Lie group `G` acts
smoothly on `R^n`, preserves `F` and `f`. Then `M` is a union of orbits, and
each orbit `G·y` is a compact embedded submanifold. So

```
dim_box(M) >= dim(G·y)    for every y in M.
```

The maximum orbit dimension over all of `F` is **not** a lower bound. For
`SO(2)` acting on the unit disc with `f = |y|^2`, `M = {0}` is a fixed point,
although generic orbits are circles. So each continuous symmetry direction
that acts nontrivially **on `M`** costs a factor `eps^(-1/2)` in the lower
bound. Within (G^LB) schemes, no branching rule, node order or
same-relaxation tightening avoids it.

*Symmetry breaking.* Add constraints that cut `M` to a lower-dimensional set
`M'` and keep `f*`, and keep them exact in the relaxation.
- This preserves (G^pt), because a feasible `y` stays in the smaller `R_B`.
  It need not preserve (G^LB): shrinking `R_B` can raise `LB(B)`.
- (EB) and (QG) must be re-checked for the new `F`.
- When they hold, the exponent drops to `dim M'/2`, by Corollary 6.5 for the
  upper bound and Corollary 4.7(b) for the lower bound. The latter uses
  (G^LB), which follows from (G^pt).

For example, take Example 7.3 on the sphere with `n = 3` and
`c = (1, 1, 1/2)`. Then `M` is the great circle in the `(y_1, y_2)`-plane,
and the count is `Theta(eps^(-1/2))`. The rotation in that plane is a
symmetry. The exact constraints `y_2 = 0` and `y_1 >= 0` pick one point of
each orbit. Then `F` becomes a half circle, `M' = {(1,0,0)}` is a
nondegenerate minimizer on a 1-dimensional stratum, and the count drops to
`Theta(log(1/eps))` (Theorem 7.1(a)). Here the objective relaxation is
unchanged, so (G^pt) holds.
- *KKT conditions.* In the equality description
  `{|y|^2 = 1, y_2 = 0, y_1 >= 0}`, allowed by Theorem 7.1, the active
  gradients at `(1,0,0)` are `2 e_1` and `e_2`. So LICQ holds, and (SOSC) holds
  with `c_1 > c_3`.
- *(EB)* holds with `kappa = 1` directly: for `z` in the exact part
  `{|y| <= 1, y_2 = 0, y_1 >= 0}`, the radial projection `z/|z|` lies in `F`,
  and `1 - |z| <= 1 - |z|^2 = v(z)`.
- *(QG)* follows from the nondegenerate minimum. So the scout's suggestion that symmetry
breaking has a quantitative payoff is a theorem for this class. The gain in
practice depends on how solvers handle symmetric continuous problems, which is
not examined here.

### 8.2 Active constraints

Three effects follow.
- The stratum that carries the optimal set decides the exponent, not the
  dimension of `F`. At a nondegenerate KKT point with `a` active
  constraints, the count is `Theta(log(1/eps))` with lower-bound prefactor
  `(alpha/M_L)^((n-a)/2)` if `a < n`, and `O(1)` for the best certificate if
  `a = n` and the minimizer is unique (Theorem 7.1(b)).
- The `n`-dimensional integral of Theorem 3.1, applied to a full-dimensional
  `F`, is still a valid lower bound. But when the optimum lies on a boundary
  stratum with a positive multiplier, it predicts an exponent half an order
  too small. In Example 7.3 on the ball with `p = 2`, it grows like
  `eps^(-1/2)`, while the count and Theorem 4.5 on the boundary sphere grow
  like `eps^(-1)` (Table 9.2).
- When the stratified form is needed:
  - For `p >= 1`, the covering bound (Theorem 4.6 with `eta = 0`) already
    gives the right exponent `p/2`.
  - The stratified integral is needed for **isolated** minimizers on a
    boundary stratum (`p = 0`). In Example 7.3 on the ball with `k = 1`
    (`B3_iso`), near `e_1` we have `m ≈ 2 c_1 s + gamma |t|^2`, where `s` is
    the depth and `t in R^2` is tangential. Integrating out `s` leaves
    `integral (gamma |t|^2 + eps)^(-1/2) d^2 t`, which is bounded as
    `eps -> 0`. So the full-dimensional integral stays bounded, and so does
    the covering bound (two points). Numerically, the full-dimensional bound
    is 2.60, 2.69, 2.72 and 2.72 leaves at `eps = 1e-3 … 1e-6`
    ([`logs/analyze_sweep.log`](logs/analyze_sweep.log)). Over the same range
    the stratified bound on the boundary sphere grows from 1.71 to 3.24 and the
    count from 415 to 753 nodes, like `log(1/eps)` (Table 9.1).
- For constraint-gap schemes, the active constraints are also what creates
  the gap (Section 5). The effective objective gap is `beta mu_0/c_1`: the
  constraint gap times the multiplier, divided by the violation rate.

### 8.3 Bound tightening

**Corollary 8.1.**

(a) *Same-relaxation tightening cannot change the exponent.* For any run of
Lemma 2.1 under (G^pt_alpha), `#leaves + 2n #(R-rel rounds)` obeys every
lower bound of Sections 3–4 and 7. This includes runs with (R-inf) rounds,
because (R-inf) pieces do not meet `F`. Under (T_{alpha,beta}), runs without
(R-inf) rounds obey the bounds of Section 5.

(b) *It can save at most a log factor.* Under (U_tau), (EB) and (Lip),
`|T_bis| <= C_0 + C_1 log(1/eps) (#leaves + 2n #(R-rel rounds))` for every
such run (Theorem 6.2 with `|P_F|`). The constants are exponential in `n` and
depend on `Lambda/alpha`: `C_1 = 20^n (2 sqrt(Lambda/alpha) + 2)^n` up to the
conversion from `J` to `log(1/eps)`.

(c) *Tightening with other information is outside the model and can change
everything.*
- Objective-cutoff propagation empties the root of `t^2 - 2t^4` with no
  relaxation solved (review, Section 1.3).
- Exact propagation of a loosened linear constraint reduces Example 5.3 to one
  node.

Case (c) is not a defect of the proofs. Cutoff propagation uses the
expression of `f` through interval evaluation and backward propagation, so it
is effectively a *different* relaxation. The theory applies to a combined
scheme exactly when that scheme still satisfies a gap hypothesis.

*Heuristic explanation (not proved).* Interval evaluation and backward
propagation are exact, or nearly so, on boxes for monotone or separable
expressions such as `t^2 - 2t^4` near its minimizer, and for a single linear
constraint. There no gap hypothesis holds, which is consistent with both
examples. A quantitative theory of such hybrid schemes is open.

These statements are consistent with the repository's iterated-OBBT
experiment, where OBBT did not pay off on MINLPLib QCQPs. They do not explain
it, since those runs used McCormick-type relaxations, which lie outside (G).

### 8.4 First-order relaxations

Replace the quadratic gap by a first-order one:

```
(G^1_alpha)   LB(B) <= f(y) - alpha delta_B(y)   for y in F ∩ B,   delta_B(y) = max_i d_i(y) = dist_inf(y, vertices of B),
(U^1_tau)     f_B >= f - tau w(B)  and  v <= tau w(B)  on R_B.
```

An example is the vertex-evaluation Lipschitz bound
`f_B(y) = max_v (f(v) - L_B |y - v|_inf)` with `L_B > Lip_inf(f)`. For the
maximizing vertex `v`,
`f(y) - f_B(y) >= (L_B - Lip_inf f) |y - v|_inf >= (L_B - Lip_inf f) delta_B(y)`.
The node model does not require `f_B` to be convex.

Parts (a) and (e) of the next theorem are the known Lipschitz covering
argument and the Bachoc et al. integral, written for boxes (see the Section 9.3
derivation of the [scout review](../../reviews/spatial-bb-review.md)).

**Theorem 8.2 (first-order gaps).** Let `Lambda_1 = tau(1 + L kappa)`.

(a) Under (G^1_alpha),
`N_opt(eps) >= 2^(-n) N_inf(E(eta), 2(eps + eta)/alpha)` for every
`eta >= 0`.

(b) Under (U^1_tau), (EB) and (Lip), with
`j_0' = min{j : tau s_j <= v_0}`,

```
|T_bis| <= 1 + 2^n [ 2^(n j_0') + (3 + 2 ceil(kappa tau))^n sum_{j >= j_0', Lambda_1 s_j > eps} N_j(E(Lambda_1 s_j - eps)) ].
```

(c) *Nondegenerate minimum.* Let `F = X0`, and let `z*` be an interior unique
minimizer with `m(y) <= (M_f/2)|y - z*|^2` near `z*` and
`m >= c_g |y - z*|^2` on `X0`. Then

```
2^(-n) omega_n (alpha^2/(8 M_f eps))^(n/2) <= N_opt(eps) <= |T_bis| <= C (Lambda_1^2/(c_g eps))^(n/2).
```

This is the cluster effect as a **lower** bound for every adaptive tree under
first-order schemes, with Du–Kearfott's `eps^(-n/2)` rate.

(d) *Morse–Bott manifold of dimension `p >= 1`.* Assume:
- `F = X0`, and `M = argmin f` is a compact embedded `C^2` submanifold of
  dimension `p`, without boundary, with reach `tau_M > 0`;
- `dist(M, ∂X0) >= r_0 > 0`;
- `m <= (M_f/2) dist(y, M)^2` when `dist(y, M) <= r_0`, and
  `m >= c_g dist(y, M)^2` on `X0` (Euclidean distance);
- (G^1_alpha), (U^1_tau) and (Lip).

Then there are `eps_1 > 0` and `C_0` such that for `0 < eps <= eps_1`

```
2^(-n-p) 2^((n-p)/2) 4^(-n) omega_(n-p) H^p(M) alpha^n M_f^(-(n-p)/2) eps^(-(n+p)/2)  <=  N_opt(eps)  <=  |T_bis|
      <=  C_0 + 2^(n+1) 3^n (3/2)^p 2^(n-p) omega_(n-p) H^p(M) (Lambda_1/c_g)^((n-p)/2) (Lambda_1/eps)^((n+p)/2).
```

So both are `Theta(eps^(-(n+p)/2))`, instead of the second-order
`Theta(eps^(-p/2))`.

(e) *Integral form* (`F = X0`):
`|P| >= alpha^n integral_{X0} (m + eps)^(-n) dy / (2^n [1 + n log(alpha s0/(2 eps))])`
for every certificate `P`.

*Proof.*

(a) For `y in E(eta) ∩ C`,
`alpha delta_C(y) <= m(y) + eps <= eta + eps`. So `y in Q(v, (eps+eta)/alpha)`
for a vertex `v`, and we conclude as in Theorem 4.6.

(b) As in Lemma 6.1. A witness `z in R_D` has `f(z) < f* - eps + tau s_j`
and `v(z) <= tau s_j <= v_0`. A nearest feasible `y` has
`|y - z| <= kappa tau s_j` and `m(y) < Lambda_1 s_j - eps`. So `D` is within
index distance `1 + ceil(kappa tau)` of a cell meeting
`E(Lambda_1 s_j - eps)`.

(c) *Lower bound.* For small `eps`, `E(eps) ⊇ B_2(z*, (2 eps/M_f)^(1/2))`. A
set of volume `V` needs at least `V/delta^n` cubes of side `delta`. Apply (a)
with `eta = eps`, `delta = 4 eps/alpha` and `V = omega_n (2 eps/M_f)^(n/2)`.

*Upper bound.* `E(t) subset B(z*, (t/c_g)^(1/2))`, so
`N_j(E(Lambda_1 s_j)) <= (2 (Lambda_1/(c_g s_j))^(1/2) + 3)^n`. The sum over
`s_j >= eps/Lambda_1` is dominated by its last term, which is
`O((Lambda_1^2/(c_g eps))^(n/2))`.

(d) *Tube volumes.* Let `N_R(M) = {x : dist(x, M) < R}` with
`0 < R < tau_M`.
- `(y, nu) -> y + nu` maps the open normal disc bundle of radius `R`
  bijectively onto `N_R(M)`.
  - Injectivity: for `nu ⊥ T_y M` with `|nu| < reach(M)`, the nearest point of
    `M` to `y + nu` is `y` (Federer 1959, Theorem 4.8(12)).
  - Surjectivity: nearest points exist because `M` is compact, and
    `x - pi_M(x)` is normal at `pi_M(x)`.
- Its Jacobian at `(y, nu)` is `det(I_p - A_nu)`, where `A_nu` is the shape
  operator of `M` in the normal direction `nu` (the tube computation of Weyl
  1939; Gray, *Tubes*, 2004, Chapter 3).
- The second fundamental form satisfies `|II(u,u)| <= 1/tau_M` for unit
  `u in T_y M`. This follows from the two-point inequality (the remark after
  Lemma 4.2, which applies since `M` is closed with reach `tau_M`).
  - Take a `C^2` curve `gamma` in `M` with `gamma(0) = y` and `gamma'(0) = u`.
    The normal part of `gamma''(0)` is `II(u,u)`, so
    `dist(gamma(t) - y, T_y M) = (t^2/2)|II(u,u)| + o(t^2)`, while
    `|gamma(t) - y|^2 = t^2 + o(t^2)`.
  - The inequality `dist <= |gamma(t) - y|^2/(2 tau_M)` gives the claim as
    `t -> 0`.

  (Niyogi–Smale–Weinberger 2008, Proposition 6.1, state this for smooth
  manifolds.) Since `A_nu` is symmetric with `<A_nu u, u> = <II(u,u), nu>`,
  its eigenvalues lie in `[-|nu|/tau_M, |nu|/tau_M]`.
- The area formula then gives

  ```
  (1 - R/tau_M)^p omega_(n-p) R^(n-p) H^p(M) <= vol N_R(M) <= (1 + R/tau_M)^p omega_(n-p) R^(n-p) H^p(M),
  ```

  and for `R <= tau_M/2` the factors are at least `2^(-p)` and at most
  `(3/2)^p`.

*Lower bound.* Let `R = (2 eps/M_f)^(1/2) <= min(r_0, tau_M/2)`. Then
`m <= eps` on `N_R(M)`, so `E(eps) ⊇ N_R(M)`. A set of volume `V` needs at
least `V/delta^n` cubes of side `delta`. Part (a) with `eta = eps` and
`delta = 4 eps/alpha` gives
`N_opt >= 2^(-n) 2^(-p) omega_(n-p) R^(n-p) H^p(M) (alpha/(4 eps))^n`, which
is the stated bound.

*Upper bound.* Here `kappa = 0` and `v ≡ 0`, so `j_0' = 0`, and part (b) gives
`|T_bis| <= 1 + 2^n 3^n sum_{j : Lambda_1 s_j > eps} N_j(E(Lambda_1 s_j))`.
1. By (QG), `E(t) subset closure N_{r(t)}(M)` with `r(t) = (t/c_g)^(1/2)`.
2. Closed level-`j` cells meeting `closure N_r(M)` lie in
   `closure N_{r + sqrt(n) s_j}(M)` and have disjoint interiors, so
   `N_j <= vol N_{r + sqrt(n) s_j}(M)/s_j^n`.
3. With `r_j = (Lambda_1 s_j/c_g)^(1/2)`, consider the levels with
   `sqrt(n) s_j <= r_j` and `2 r_j <= tau_M/2`, that is,
   `s_j <= s_* = min(Lambda_1/(n c_g), c_g tau_M^2/(16 Lambda_1))`. On these,
   `N_j <= (3/2)^p omega_(n-p) (2 r_j)^(n-p) H^p(M)/s_j^n = (3/2)^p 2^(n-p) omega_(n-p) H^p(M) (Lambda_1/c_g)^((n-p)/2) s_j^(-(n+p)/2)`.
4. Summing over `s_j > eps/Lambda_1` with `(n+p)/2 >= 1` gives at most
   `2 (Lambda_1/eps)^((n+p)/2)` times this constant.
5. The levels with `s_j > s_*` contain at most `2^(n j_*)` cubes, with
   `j_* = ceil(log2(s0/s_*))`. They go into `C_0 = 1 + 2^n 2^(n j_*)`.

(e) On `C`, `m + eps >= max(eps, alpha delta_C)`. Split `C` into the `2^n`
parts nearest to each vertex. On the part of vertex `v`,
`delta_C(y) = |y - v|_inf`, and the part lies in an orthant of `Q(v, s0/2)`.
Then
`integral max(eps, alpha |y-v|_inf)^(-n) dy <= alpha^(-n) [1 + n integral_{eps/alpha}^{s0/2} dr/r]`. □

**Remarks.**
- *Where the exponents come from.* At a Morse–Bott set of dimension `p`, the
  exponents are `p/2` under a second-order gap and `(n+p)/2` under a
  first-order gap.
  - Along `M`, each direction contributes `1/2` under a second-order gap and
    `1` under a first-order gap.
  - Transversal directions contribute `0` under a second-order gap and `1/2`
    each under a first-order gap.

  In both regimes the `eps`-optimal set is a tube of width `~ eps^(1/2)` around
  `M`. What changes is the cell side a certificate can use near `M`:
  `~ eps^(1/2)` under a second-order gap, `~ eps` under a first-order gap. In
  integral form, `integral (m+eps)^(-n)` replaces `integral (m+eps)^(-n/2)`.
  This matches the Lipschitz theory of Bachoc et al. (2021), whose integral has
  exponent `d`.
- The review observed that a ball-based Lipschitz argument gives the integral
  form **without** the log factor (review, Section 9.3). For boxes of
  arbitrary shape, whether the log in (e) is needed is open. The covering
  forms (a)–(d) have no log.
- A second-order gap removes the transversal loss entirely, not just the log.
  This is the precise sense in which second-order schemes avoid the cluster
  effect: `log(1/eps)` versus `eps^(-n/2)` at nondegenerate minima, with
  matching lower bounds for both.

## 9. Computations

All runs use exact-alphaBB-type relaxations with the incumbent fixed at `f*`,
binary widest-side bisection, and pruning when the bound is at least
`f* - eps`. They are floating-point illustrations, not certified counts.

**Toy B&B ([`sbb_sphere.py`](sbb_sphere.py)).** Instances are those of
Example 7.3: `f = -sum_i c_i y_i^2 (+ y_2^4)` on the unit circle, sphere or
ball, with `X0 = [-1.2, 1.3]^n`. The offset root keeps the coordinate
hyperplanes `y_i = 0` away from dyadic points. The relaxation is:
- the objective `f - alpha q_B` with `alpha = 1.1 max c`;
- `|y|^2 <= 1` kept exactly;
- for the sphere, the secant cut `sum_i ((l_i+u_i) y_i - l_i u_i) >= 1`.

The node problem is separable given two multipliers. The bound is the
Lagrangian dual maximized by L-BFGS-B, which is valid for any multipliers.

**Validation ([`check_dual_bounds.py`](check_dual_bounds.py),
[`logs/check_dual_bounds.log`](logs/check_dual_bounds.log)).** On 582 random
boxes, the dual bound never exceeds the best SLSQP primal value by more than
`3.4e-13`, and it is never more than `1e-6` below it. So the bounds are valid
and tight up to rounding.

**Table 9.1 (bisection nodes; [`logs/analyze_sweep.log`](logs/analyze_sweep.log)).**
"LB" is the Theorem 4.5(i) lower bound on the leaves of *any* certificate. It
is computed on the unit sphere or circle stratum (`d = n-1`, `M(S) <= 2n`)
and, for `S3_circ`, also on the optimal circle (`d = 1`, `M <= 4`); the larger
value is used. Bisection leaves are `(nodes+1)/2`.

| instance | `n` | `p` | prediction | nodes at eps = 1e-2 / 1e-4 / 1e-6 | local exponent, last three decades | leaves/LB |
|---|---|---|---|---|---|---|
| `S2_iso` circle, `c = (1, .5)` | 2 | 0 | `log` | 77 / 135 / 187 | additive: +34, +28, +24 nodes per decade | 34–36 |
| `S2_circ` circle, `c = (1,1)` | 2 | 1 | `eps^(-1/2)` | 273 / 3359 / 29465 | 0.57, 0.45, 0.49 | 32–45 |
| `S3_iso` sphere, `c = (1,.5,.25)` | 3 | 0 | `log` | 299 / 535 / 753 | additive: +120, +112, +106 | 113–125 |
| `S3_circ` sphere, `c = (1,1,.5)` | 3 | 1 | `eps^(-1/2)` | 1191 / 14037 / 130237 | 0.56, 0.49, 0.48 | 105–118 |
| `S3_all` sphere, `c = (1,1,1)` | 3 | 2 | `eps^(-1)` | 6023 / 588281 (1e-4) | per half-decade: 0.88, 1.02, 1.07 | 99–121 |
| `S2_quart` circle, `-|y|^2 + y_2^4` | 2 | 0, quartic | `eps^(-1/4)` | 89 / 317 / 895 (2595 at 1e-8) | 0.20, 0.25, 0.26, 0.20 | 30–36 |
| `B2_circ`, `B3_iso`, `B3_circ`, `B3_all` (ball) | | | as the sphere | identical to the sphere runs within 2 nodes | | |

The ball runs match the sphere runs because the objective pushes outward. The
secant cut matters only in boxes inside the ball, which the bound prunes
anyway.

**Table 9.2 (active constraint: stratified versus full-dimensional bound, ball
instances).** "Full-dim" is `(alpha n/pi^2)^(n/2) integral_F (m+eps)^(-n/2)`,
Theorem 3.1 restricted to `F`. It is valid but has the wrong exponent.

| eps | `B3_circ` leaves | Thm 4.5 (boundary sphere) | full-dim | `B3_all` leaves | Thm 4.5 | full-dim |
|---|---|---|---|---|---|---|
| 1e-2 | 596 | 5.45 | 6.44 | 3011 | 26.95 | 20.72 |
| 1e-3 | 1933 | 18.40 | 10.36 | 26649 | 269.5 | 73.09 |
| 1e-4 | 7019 | 59.34 | 14.32 | 294141 | 2695 | 239.2 |
| 1e-6 | 65119 | 598.2 | 22.23 | – | – | – |

The full-dimensional bound grows by about 3.95 per decade for `B3_circ`
(`log`) and by about `sqrt 10` per decade for `B3_all` (`eps^(-1/2)`). The
counts grow like `eps^(-1/2)` and `eps^(-1)`, as the boundary stratum
predicts.

**Other computations.**
- Constraint-gap example: Example 5.3, [`flat_constraint_gap.py`](flat_constraint_gap.py).
  The node bound is in closed form.
- Key lemma: Proposition 4.4, [`key_lemma_check.py`](key_lemma_check.py).

**What the computations establish.**
- The exponents `0, 1/4, 1/2, 1` predicted by Theorems 7.1, 7.2 and 6.7
  appear in bisection counts over 4–6 decades of `eps`.
- The ratio of bisection leaves to the proved lower bound is roughly constant
  in `eps` (30–45 in 2D, 100–125 in 3D). This agrees with Theorem 6.7's
  `eps`-independent constants.
- The boundary stratum, not the full-dimensional integral, predicts the ball
  exponents.

They do not certify any count, and they do not measure `N_opt` itself in 2D or
3D.

## 10. Literature comparison and novelty

No new literature search was run for this note. The comparison relies on:
- the scout's Section 1;
- Section 9 of the scout review: local full texts of Neumaier (2004) and
  Wechsung et al. (2014); a delegated search with spot-checked quotations for
  the other sources; no general web search;
- Section 9 of the [review of this note](../../reviews/spatial-constrained-review.md),
  which read Kannan–Barton (2017) Sections 2–3 locally;
- the repository's cluster-free note.

| Source | What it gives | Relation to this note |
|---|---|---|
| Du, Kearfott, JOGO 5 (1994) | upper estimates on the boxes left, for interval extensions of order `alpha`; "an upper bound, and not a precise value" | Theorem 8.2(c) is a matching **lower** bound for first-order gaps (`eps^(-n/2)`) for adaptive trees; Theorem 7.1 gives the second-order counterpart `Theta(log(1/eps))` |
| Wechsung, Schaber, Barton, JOGO 58 (2014) | fixed-width covering estimates; refine Neumaier's lower count; minimizer at box centre; prefactor threshold | the prefactor `(alpha/gamma)^(n/2)` multiplies `log(1/eps)` for every tree (Section 3.8); for vertex-exact relaxations, vertex placement is optimal (Example 3.4, Proposition 6.8) |
| Neumaier, Acta Numerica 13 (2004), Section 15 | heuristic lower count `const √((2Δ)^n)/(eps^n √det G)`; "`n` replaced by `n - a`" under active constraints; clustering "seems unavoidable" on non-isolated solution sets | Theorems 7.1 and 7.2 are rigorous all-scales versions: lower-bound prefactor `(alpha/M_L)^((n-a)/2)`, `O(1)` for the best certificate when `a = n` and the minimizer is unique, and `eps^(-p/2)` on `p`-dimensional solution sets. **This is the closest MINLP precedent.** |
| Kannan, Barton, JOGO 69 (2017), 71 (2018) | constrained cluster analysis with worst-case, fixed-width **upper** estimates; first order suffices with a trivial critical cone. **Section 3.2 and Lemmas 2–3 of the 2017 paper** treat the region `X_3` of infeasible points with violation at most `eps^f` and objective at most `f* + eps^o`; the abstract says "clustering can occur both on nearly-optimal and nearly-feasible regions" | **precedent for the infeasible-side mechanism of Section 5.** New here: the lower-bound form for adaptive trees, the tube hypothesis (T), the isotropic/anisotropic contrast, the Lagrangian transfer and Theorem 5.7. Also Theorem 7.1(b): `d = 0` gives `O(1)` certificates. Lemma 1.1 shows McCormick satisfies the upper hypothesis |
| Cluster-free note (repository; Anitescu 2005; Bonnans–Shapiro) | `L(Z) >= f* + c_1 dist^2 - c_2 w^2`, `O(1)` boxes per scale | used for (QG) in Theorem 7.1; Theorem 5.7 runs the same Lagrangian mechanism in reverse to get lower bounds from constraint gaps |
| Hansen, Jaumard, Lu, MOR 16 (1991) | 1D Lipschitz: Piyavskii within `2 n_B + 1` of the best certificate; bounds on `n_B` | Theorems 3.3 and 6.2 are multivariate, relaxation-based, constrained analogues, with a log factor that is attained |
| Perevozchikov (1990), via Bouttier et al. (arXiv:2002.02390); Munos (NIPS 2011) | level-by-level branch-and-bound or DOO counts under volume or near-optimality-dimension assumptions (upper bounds) | Lemma 6.1 and Theorems 6.2–6.4 are this level-by-level count plus an error bound. Theorem 6.3: the running supremum of the near-optimality profile for `|x-y|^2` is also a **lower** bound for every certificate, and bisection attains it within `log(1/eps)` (Remark 6.3a) |
| Bachoc, Cesari, Gerchinovitz, NeurIPS 2021 (arXiv:2102.01977) | Lipschitz black box: certified sample complexity `≍ integral (f*-f+eps)^(-d)` up to logs | second-order white-box analogue `integral (m+eps)^(-n/2)`, with constraints and strata. Theorem 8.2(a) and (e) are the known Lipschitz covering argument (scout review, Section 9.3) and their integral, written for boxes |
| Dey, Dubey, Molinaro (midpoint/cross-polytope) | integer-branching lower bounds | credited by the program as the closest integer mechanism; not used here |
| Federer (1959); Niyogi, Smale, Weinberger (2008); Weyl (1939); Gray, *Tubes* (2004); Robinson (1976); Evans–Gariepy | reach and the two-point inequality; volume of small balls on manifolds and the bound `1/tau` on the second fundamental form; tube volumes; error bounds under MFCQ; area formula with multiplicity (Banach indicatrix) | tools. Lemma 4.1 combines standard geometric-measure-theory tools: a coordinate projection with Jacobian at least `binom(n,d)^(-1/2)` via Cauchy–Binet, the area formula with multiplicity, and reach-based multiplicity bounds. Its new part is the per-box arcsine bound |

**What is claimed as new, as far as the bounded search found.** Rigorous
lower bounds on the tree size of relaxation-based spatial branch-and-bound
that hold for adaptive trees, any node order and same-relaxation tightening,
with constraints. Specifically:
- Lemma 2.1, corrected;
- the per-box arcsine bound for `q_B^(-d/2)` on strata (Lemma 4.1; the
  surrounding tools are standard), and the necessity of the multiplicity
  (Proposition 4.4);
- the stratified integral bound (Theorem 4.5);
- the lower-bound form of the infeasible-side mechanism: the tube dichotomy,
  the Lagrangian transfer and Theorem 5.7 (Section 5). Kannan–Barton (2017,
  Section 3.2) is the precedent for the mechanism, with upper estimates;
- the covering characterization of `N_opt` and bisection within `log(1/eps)`
  for constrained problems (Theorem 6.3), and its integral form (Theorem 6.7).

The unconstrained Theorems 3.1–3.5 are, per the review, short transfers of
Lipschitz and bandit arguments. Their originality is modest to low.

The review of this note rated originality by part:
- Section 5: modest to moderate, the most original part;
- Lemma 4.1, Theorem 4.5 and Section 7: modest;
- Theorem 4.6, Section 6 and Section 8: low to modest.

**Not examined:**
- the interval-analysis box-count literature (Ratschek–Rokne; Csendes–Ratz;
  Kearfott 1996; Schöbel–Scholz 2010), which is the most likely place for
  close prior work;
- the full text of Hansen–Jaumard–Lu;
- post-2021 work on Bachoc et al.'s log factor.

An unsuccessful search does not establish novelty.

## 11. Open problems and conjectures

1. **Local rules (Q1b).** Is there a node-local branching rule within
   `C_n N_opt(eps)` on every (G) instance? Bisection loses exactly
   `log(1/eps)`, and only at sharp or vertex minimizers (Remark 6.9). This is
   the subject of `branching-competitiveness/`.
2. **Upper-bound prefactor.** Theorems 7.1 and 7.2 have lower prefactor
   `(alpha/M_L)^(d/2)` and upper prefactor `C^n (Lambda/c_g)^(n/2) Lambda'^(d/2)`.
   *Conjecture:* at a nondegenerate KKT point with SC, bisection's prefactor
   is `C^n (Lambda/gamma)^(d/2)`. Here `d` is the stratum dimension, not `n`,
   because the near-optimal set has width `O(t)` normal to the active
   constraints (linear growth under SC). A proof would use (R1) with linear
   normal displacement in Theorem 6.6.
3. **Propagation and constraint gaps.** Does exact interval propagation of
   the original constraints preserve the `eps^(-p/2)` exponent for
   constraint-gap schemes when the optimal stratum is strictly curved?
   Example 5.3(c) shows it can remove the effect on flat, axis-aligned strata.
4. **Hybrid schemes.** Give a quantitative theory for relaxations combined
   with objective-cutoff interval propagation (Corollary 8.1(c)).
5. **Singular strata.** Theorem 4.5 needs `C^1` strata with a positive
   two-point constant. Optimal sets with cusps or other non-manifold points
   are covered only by the covering bound (Theorem 4.6). The right integral
   form there is open.
6. **Box-dependent `alpha_B`** (interval-Hessian alphaBB) and **face-exact
   relaxations** (McCormick, multilinear): the upper bounds of Section 6
   apply (Lemma 1.1), the lower bounds do not. See `spatial-face-exact/`.
7. **Constants.** Is the AM–GM loss (`~0.81^n` per cube) attained by
   `N_opt`? Is the factor `binom(n,d)^(3/2)` in Lemma 4.1 necessary? Is the
   log factor in Theorem 8.2(e) necessary for boxes of unbounded aspect ratio?
8. **Incumbent.** All upper bounds fix `UBD = f*`. With certified upper
   bounding (Füllner–Kirst–Stein), finding the incumbent adds a separate cost
   that is not analysed here.
9. **Nonlinear exact constraints.** Lemma 5.5, and hence Theorems 5.7 and
   7.1(c), assume `P_ex` polyhedral near `z*`. The extension by
   constraint-preserving curves is sketched after Lemma 5.5 but not written
   out.

## 12. Checks run

Targeted commands, all run from
`research-20260928b/bb-complexity/spatial-constrained/`, with outputs in
`logs/`:

- `./run_sweep.sh`: runs `python3 sbb_sphere.py INST EPS` for the nine
  sphere and ball instances. `eps = 1e-1 ... 1e-6`, or down to `1e-4` for
  `p = 2`, 30 processes in parallel, output `logs/sweep_sphere.jsonl`.
- `python3 sbb_sphere.py S2_quart EPS` for `EPS = 1e-1 ... 1e-8`, output
  `logs/sweep_quartic.jsonl`.
- `python3 analyze_sweep.py > logs/analyze_sweep.log` and
  `python3 analyze_quartic.py > logs/analyze_quartic.log`: exponents,
  Theorem 4.5 lower bounds and full-dimensional bounds (Tables 9.1, 9.2).
- `python3 check_dual_bounds.py > logs/check_dual_bounds.log`: validity and
  tightness of the node bounds on 582 random boxes.
- `python3 flat_constraint_gap.py > logs/flat_constraint_gap.log`: Example
  5.3, with closed-form node bounds.
- `python3 key_lemma_check.py > logs/key_lemma_check.log`, filtering SciPy
  warning lines: Proposition 4.4 (comb and spiral) and the circle constant of
  Lemma 4.1. Re-run in the revision after extending the script.

Re-run in the revision (Section 13):
- `key_lemma_check.py`, extended with the bounding-square start and the
  spiral;
- `analyze_sweep.py`, extended with a second, closed-form-radial computation
  of the full-dimensional ball integral, including `B3_iso`.

The other checks test statements that the revision did not change. They were
not re-run.

These checks test the numbered statements they cite. They are floating-point
illustrations and certify nothing. Every theorem rests on its written proof.
The review's own scripts are in `reviews/spatial-constrained/` and were not
re-run here. No project-wide checks were run, CI was not inspected, and
nothing was committed.

## 13. Revision after review

The [review](../../reviews/spatial-constrained-review.md) found no
counterexample to any numbered result and listed 17 corrections (its Section
10). Each was re-derived before it was made.

1. **Remark 3.7.** The ratio is `2 (4 pi^2 Lambda/(alpha n))^(n/2) = 2 (pi^2 K (kappa + 4/(alpha n)))^(n/2)`.
   The first version dropped `2^n`.
2. **After Lemma 1.1.** McCormick violates (G^pt), not (G^LB) as such. The
   failure of (G^LB) is now derived from the face-exact example and Theorem
   4.6.
3. **Remark after Lemma 4.2.** It now says "relatively open subset of a
   `d`-dimensional `C^1` submanifold", and explains the limit `r -> reach` in
   Federer's Theorem 4.18(2).
4. **Proposition 4.4.**
   - `S_∞` is now called a submanifold with infinitely many components.
   - Part (c) adds a connected spiral with curvature at most `10/r` and an
     infinite integral, with proof.
   - The comb, circle and spiral numerics were re-run.
5. **Lemma 5.5.** The hypothesis "`P_ex` polyhedral near `z*`" is now in the
   statement. It is carried into Theorems 5.7 and 7.1(c), and into Open problem
   9. The curve extension is described as a sketch only.
6. **Theorem 5.4 and the Summary.** The result is described as a
   one-directional transfer of lower bounds. Summary item 4 now says "has a
   3-leaf certificate".
7. **Theorem 6.2.** `|P|` may be replaced by `|P_F|`; Corollary 8.1(b) uses
   this.
8. **Theorem 6.3.**
   - Remark 6.3a(i) proves that `Phi_alpha` is, within a factor `2^n`, the
     running supremum over `eta >= eps` of a Munos-type profile. (The
     constants were tightened after the recheck; see below.)
   - Remark 6.3a(ii) proves that a single-scale version fails with uniform
     constants. The explicit family is
     `f_K = K^(-2)(1 - cos 2 pi K t) + K^(-2)(1 - exp(-K^2 t^2))` with
     `alpha = 32`, giving `N_opt >= K/2` against an `O(1)` single-scale
     covering number. (The recheck's count includes `t_0`.)
   - The Summary and the interpretation are restated accordingly.
9. **Corollary 6.5(b).** The constant is `20^n`, not `10^n`.
10. **Theorem 6.7 and hypothesis (R).** The number of strata is renamed
    `K_S`, which removes the clash with the doubling constant `K`. The
    restriction `eps <= t_0` is dropped; neither inequality needs it.
11. **Theorem 7.1.**
    - Parts (a) and (c) now allow finitely many nondegenerate minimizers. This
      covers Example 7.3 with `k = 1` (`±e_1`). Part (b) keeps a unique
      minimizer.
    - Part (c) requires a nonzero multiplier and the polyhedral `P_ex`.
    - "Lower-bound prefactor" is used in 7.1, 8.2 and the Neumaier comparison.
12. **Section 8.1.**
    - The orbit dimension is now taken at points of `M` (the `SO(2)`-on-disc
      counterexample is included), for compact connected Lie groups.
    - Adding exact constraints preserves (G^pt), not (G^LB); (EB) and (QG) must
      be re-checked, and are checked in the worked example.
13. **Section 8.2.** "Necessary" is restricted to isolated minimizers on a
    boundary stratum. For `p >= 1` the covering bound already gives the
    exponent. New numerics for `B3_iso`: the full-dimensional bound stays near
    2.72, while the count and the stratified bound grow like `log(1/eps)`.
14. **Theorem 8.2(d).** Written out with hypotheses and explicit constants.
    It uses tube-volume bounds from the normal-bundle parametrization and the
    second-fundamental-form bound `1/tau_M`.
15. **First remark after Theorem 8.2.** Reworded. Along `M`, each direction
    contributes 1/2 (second order) or 1 (first order); transversal directions
    contribute 0 or 1/2. The tube width `eps^(1/2)` is common to both regimes;
    the admissible cell side differs.
16. **Section 8.3.** The interval-evaluation explanation is labelled
    heuristic and mentions backward propagation. Corollary 8.1 now states that
    (R-inf) rounds are covered under (G^pt), and that the constants are
    exponential in `n` and depend on `Lambda/alpha`.
17. **Section 10 and the Summary.**
    - Kannan–Barton (2017, Section 3.2, region `X_3`) is cited as the
      precedent for the infeasible-side mechanism of Section 5.
    - Lemma 4.1 is described as standard geometric-measure-theory tools plus
      the new per-box arcsine bound.
    - Theorem 8.2(a) and (e) are described as the known Lipschitz covering
      argument in box form.
    - The review's originality ratings by part are recorded.

Further changes suggested in the review's body text:
- the modelling convention that exactly kept convex constraints belong to
  `P_ex` (Section 5 and Example 7.3, whose (EB) derivation now uses it);
- the review's reverse-convex instance, as a natural example for Theorem 5.7;
- the review's key-lemma stress-test results, in Section 4.1.

Checks re-run for this revision, from this directory:
- `python3 key_lemma_check.py > logs/key_lemma_check.log` (SciPy warning lines
  filtered). Result: circle maximum `2 pi`; comb limit 1.8403; spiral integral
  4.98, 40.0 and 381 for `T = 10, 100, 1000`.
- `python3 analyze_sweep.py > logs/analyze_sweep.log` (SciPy warning lines
  filtered). Result: the second method reproduces the earlier full-dimensional
  values exactly for `B3_circ` and `B3_all`; the `B3_iso` values are
  1.57 … 2.72, bounded.

No other computation depends on a changed statement.

### 13.1 Second round, after the recheck

A [recheck](../../reviews/spatial-constrained-recheck.md) of the six
substantive revisions found them correct. It listed five minor points, which
are fixed as follows after re-deriving each.

1. **Description-independence in Theorem 7.1.** Under the `P_ex` convention,
   `|y|^2 <= 1` and `1 - |y|^2 <= 0` are both active at `±e_1` on the sphere,
   so LICQ fails in that description.
   - Theorem 7.1 now states that in (a) and (b) the conditions (KKT)–(SOSC),
     `S_loc` and `M_L` may be taken in any `C^2` description of `F` near `z*`.
     The proof uses them only for (QG), sharp growth and the graph structure of
     `S_loc`. Part (c) still uses the relaxation's constraints.
   - This is applied in Example 7.3 (the sphere as `|y|^2 = 1`; LICQ, SOSC via
     `2 diag(c_1 - c_i)` on `e_1^⊥`) and in the Section 8.1 half-circle example
     (description `{|y|^2 = 1, y_2 = 0, y_1 >= 0}`; (EB) checked directly by
     radial projection).
2. **Remark 6.3a.**
   - Cubes of side `2 sqrt(eta/alpha)` are balls of radius `eta` for
     `ell = alpha |x - y|_inf^2`. The Munos identification is stated up to
     constants.
   - The upper factor in (i) is 1, since both proof steps already gave factor
     1. So `2^(-n) sup psi <= Phi <= sup psi`.
   - In (ii): exact alphaBB meets (G^pt) and (U^q) for every `alpha`. The real
     requirement is convexity, `alpha >= -min f_K''/2`: at most 20.19 by the
     termwise bound `-4 pi^2 - 4 e^(-3/2)`, and about 20.11 numerically per the
     recheck. The covering step needs only `alpha > 8`.
   - Counting `t_0` gives `N_opt >= K/2`.
   - The Summary and the Interpretation were adjusted.
3. **Theorem 8.2(d) citations.**
   - Injectivity of `(y, nu) -> y + nu` now cites Federer 1959, Theorem
     4.8(12).
   - The bound `|II| <= 1/tau_M` is derived for `C^2` manifolds from the
     two-point inequality along a curve in `M`, instead of citing a
     smooth-manifold source.
4. **Proposition 4.4(c).**
   - The embedding argument now uses `|c(t)| = rho(t)` strictly decreasing, and
     it names both limit sets not on the curve: the circle of radius `r` and
     `(2r, 0)`.
   - A proof of reach 0 is added: same-angle points on consecutive turns force
     `tau <= Delta sqrt(rho^2 + rho'^2)/(2 rho) -> 0`.
5. **Wording.** The Section 10 Neumaier row now says "lower-bound prefactor"
   and "`O(1)` … when `a = n` and the minimizer is unique". Section 8.2 now
   says the same and cites Theorem 7.1(b).

No computation depends on these changes, so no script was re-run in this
round. The recheck's own scripts are in `reviews/spatial-constrained-recheck/`
and were not re-run here. Nothing was committed.
