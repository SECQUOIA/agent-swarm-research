# Optimal intersection cuts from maximal quadratic-free sets

Workstream note, research-20260928b. Scout report:
[s-free-intersection-cuts.md](../scouting/s-free-intersection-cuts.md).
Code, logs and certificates: [code/](code/) and [logs/](logs/).
Date: 2026-09-28; revised 2026-09-29 after the independent review
[`../reviews/sfree-review.md`](../reviews/sfree-review.md) (see Section 12).
Nothing here has been committed.

## Summary

**Question.** For a nonconvex quadratic constraint and a simplicial LP cone,
which maximal quadratic-free set gives the best intersection cut, and is a
low-dimensional search over the Muñoz–Serrano "transformations" enough?

**Proved here** (full proofs below; numbers refer to sections).

1. *Single cut = corner bound* (Theorem 1). With strictly positive reduced
   costs `w`, the best bound from one intersection cut, over all S-free sets
   containing the LP vertex in their interior, equals the corner bound
   `z_K(w) = min{w^T λ : λ ≥ 0, x̄ + Rλ ∈ S}` for every closed `S`. The
   supremum is attained when every corner minimizer is a regular KKT point;
   it can fail to be attained otherwise, and the equality can fail when `w`
   has zero entries (Proposition 2).
2. *Few rays suffice* (Lemma 3, Theorem 4). A corner minimizer uses at most
   `rank P ≤ k` rays, and, for `S = {q ≤ 0}`, at most
   `ρ(q) = n_+(Q) + n_0(Q) + 1 − [b ∉ range Q]` rays. For bilinear
   constraints `ρ = 2`; for strictly concave `q`, `ρ = 1`.
3. *Complexity* (Theorem 5). For fixed `min(k, ρ)`, `z_K` is computable in
   polynomial time; with `rank P = k` only `O(N^{⌊k/2⌋})` `k`-ray
   subproblems are needed. Each subproblem has a closed form for generic
   data and for at most two rays in all cases. Computing `z_K` (equivalently
   the best single-cut bound) is NP-hard when `k` is part of the input, and
   NP-hard to approximate within relative error `1/(5k^2)` (Motzkin–Straus).
4. *SCIP's set can be arbitrarily bad* (Proposition 6). SCIP's
   (Chmiela–Muñoz–Serrano) set can give a bound `ε(x_0 + 1/x_0)` while
   another Muñoz–Serrano set of the same constant-`λ` family gives `1`.
5. *The Lorentz orbit reaches all maximal sets in signature `(n,1)` and
   `(1,m)`* (Theorem 8). If the homogenized quadratic form has one negative
   (or one positive) eigenvalue, every full-dimensional maximal
   quadratic-free set is an image of the Muñoz–Serrano set under the
   automorphism group of the form (sliced at `t = 1` in the inhomogeneous
   case), provided the direction `λ` is free (equivalently, the whole orbit
   is used). This covers every indefinite quadratic in two variables and
   answers which sets Muñoz–Serrano's transformations can reach. With their
   (and SCIP's) rule `λ = x̂(Ts̄)/‖x̂(Ts̄)‖`, the sets reachable at a fixed
   `s̄` form only a one-parameter family. It misses `z_K` on 13 of 36
   random two-variable corners with finite `z_K`, also when Muñoz–Serrano's
   full construction (their enlargement of some members) is modelled
   (numerical evidence, from the recheck; Section 6.1).
6. *Rank-1 closure ≠ hull* (Proposition 9). In the plane, for a triangle and
   the complement of the unit disk, the closure of all LP-basis intersection
   cuts is strictly larger than the convex hull; the second round closes it.
7. *Bilinear constraints: the transformation search is not exact*
   (Section 8). For `w = xy`, the orbit of the Muñoz–Serrano sets is the
   3-parameter family `C_F = {sym(F^T M) ⪰ 0}` of 2×2 matrices, the maximal
   completion used by SCIP (Case 4) is its upward closure along `w`, and the
   best orbit cut is a quasiconvex problem (bisection over 2×2 LMIs). But
   both families **fail to attain the corner bound**: when the corner
   minimizer lies on a tangent edge, any orbit set containing the optimal
   simplex must belong to a one-parameter pencil, and an exact rational
   instance (Theorem 14) has no member of the pencil containing it. The gap
   is strict (proved); numerically it is about 2.5% on that instance, 16.5%
   on a second rational instance (strictness proved for the orbit family).
   A support-one minimizer with all edges transversal does not save family
   (A) either (Proposition 16, certified exactly after the review refuted
   the former Conjecture 16; for (B) only numerically).
   For family (A), an adversarial search found gaps up to 55% (checked with
   two SDP solvers; that instance sits on the imposed 1% grazing margin)
   and 97% when the LP vertex nearly lies on `∂S`; for family (B) the
   corresponding numbers are heuristic lower bounds of the same order. The
   corner bound itself is computed exactly with `O(N^2)` closed-form two-ray
   problems (Theorem 11), so the best single-cut bound is cheap even where
   no transformation finds a set attaining it.

**Computations** (Section 9; all targeted, commands in Section 11).
- *Validation.* The exact corner bound matches SCIP global solves on 77
  random instances (max. relative difference `2.8·10^-6`); the
  counterexamples of Theorem 14 (both families), the second rational
  instance (family A) and Proposition 16 (family A) are certified in exact
  arithmetic; the orbit bound of Theorem 8 is confirmed on 24 random
  2-variable corners (ratio `1.00000000`).
- *One cut at a McCormick LP vertex* (random bilinear programs, n = 47 and
  73). Fraction of the single-constraint gap closed on the corner: SCIP's
  set 0.70 / 0.59 (mean), best orbit set 0.755 / 0.648 (it attains `z_K` in
  all 120 corners). After re-solving the full LP with the cut: SCIP
  0.895 / 0.870, orbit 0.929 / 0.907, while the objective-parallel
  corner-optimal cut `w^T λ ≥ z_K` gives only 0.755 / 0.648.
- *Prototype separator* (root loop, HiGHS): the orbit rule closes the gap
  faster on small instances (0.998 vs 0.963 after 3 rounds, fewer cuts) but
  ends behind SCIP's rule on the 6×8 instances (0.887 vs 0.931 after 10
  rounds, n = 10). The corner-optimal cut stalls after one round.
- *Adversarial search:* single-cut ratios of family (A) down to 0.45 with
  rays 1% from grazing (two solvers agree) and 0.028 when the vertex nearly
  lies on `∂S` (Clarabel); family (B) values are heuristic lower bounds.
- A solver bug (dropped double roots) produced spurious gaps and was
  fixed; near-grazing adversarial corners are numerically ill-posed and
  were excluded (Section 9.1).

**Open.** Whether some quantitative transversality condition at the
contact point makes the orbit exact (the former Conjecture 16, "support one
suffices", is false); the worst-case single-cut ratio of the orbit family
for bilinear constraints (0.45 with rays 1% from grazing, 0.028 near `∂S`;
is it bounded away from 0 under a nondegeneracy condition?); whether the
*closure* of the orbit family is exact (an Averkov–Basu–Paat-type question
that the single-cut obstruction does not settle); loop convergence (OQ3 of
the scout).

**Status of the scout's first-pass claims.**

| Scout claim | Status here |
|---|---|
| Lemma 1: single cut = corner bound for `w > 0` | Proved (Theorem 1), with an attainment criterion; fails for `w` with zero entries (Proposition 2) |
| Closure at `x̄` equals `cl(conv X + R^N_+)` | Proved for every closed `S` (Theorem 1(5)); folklore |
| Lemma 2: `≤ rank P` rays | Proved (Lemma 3); sharpened to `ρ(q)` (Theorem 4) |
| Prop 3: `O(N^{⌊k/2⌋})` closed-form subproblems; `2N − 4` for `k = 3` | Correct with `rank P = k` and a triangulated normal fan; the closed forms are generic, exact for `≤ 2` rays; the rigorous polynomial bound uses Renegar (Theorem 5) |
| Prop 3: efficacy-optimal cuts polynomial for fixed `k` | Correct up to `ε` via the ellipsoid method (remark after Theorem 5) |
| Prop 4: NP-hard via Motzkin–Straus | Correct; decision version with rational threshold and `1/(5k^2)` inapproximability added (Theorem 5(4)) |
| Prop 5: SCIP's `λ` arbitrarily bad | Correct; needs `x_0 ≥ ε/√(1 − ε^2)` for the stated `z_K` (Proposition 6) |
| Prop 6: constant-`Γ` closure factor → 0 | Correct in the limit `r_2 → −r_1`; for a pointed cone the perturbation must be small relative to `1/a` (`η = a^{-1}` gives `z_K ≈ 0.51`; `η = a^{-3}` works) (Remark 7) |
| Prop 7: Lorentz orbit = all maximal sets, signature `(n, 1)` | Proved with `λ` free, and extended to the inhomogeneous case (Theorem 8); with the Muñoz–Serrano point rule the reachable family is one-parameter and its plain sets miss `z_K` (Section 6.1) |
| exp11: rank-1 closure ≠ hull (triangle, disk) | Proved exactly (Proposition 9) |
| OQ1(a): orbit sufficiency for `(2, 2)`; "equivalently" closure = dominant | **False** for single cuts, also for the maximal completion (Theorem 14), and also when the minimizer has support one (Proposition 16); the claimed equivalence holds in one direction only |
| E3: best cut closes median 1.00 of the single-constraint gap on the corner | Reproduced (0.755 mean / 1.00 median, n = 47); but re-solving the full LP changes the picture (Section 9.2) |

---

## 1. Setting and notation

LP relaxation in `R^d` with an optimal basic solution `x̄`. The basis cone
is `K = x̄ + R·R^N_+`, where the columns `r_1, …, r_N` of `R ∈ R^{d×N}` are
the extreme rays (for an LP basis `R` has full column rank; we do not need
this except where stated). The objective is `c^T x`; the reduced costs are
`w = R^T c ≥ 0` (dual feasibility). `S ⊂ R^d` is closed, `x̄ ∉ S`.

- *Corner set and bound.* `X = {λ ∈ R^N_+ : x̄ + Rλ ∈ S}` and
  `z_K(w) = inf{w^T λ : λ ∈ X}` (`+∞` if `X = ∅`). The corner relaxation
  `min{c^T x : x ∈ K ∩ S}` has value `c^T x̄ + z_K(w)`.
- *Intersection cut.* For a closed convex `C` with `x̄ ∈ int C` and
  `int C ∩ S = ∅` ("S-free"), let `α_j(C) = sup{t ≥ 0 : x̄ + t r_j ∈ C}`
  `∈ (0, ∞]`. The cut is `Σ_j λ_j/α_j ≥ 1` (with `1/∞ = 0`).
- *One-cut bound.* `z_C(w) = min{w^T λ : λ ≥ 0, Σ_j λ_j/α_j ≥ 1}`
  `= min_{j : α_j < ∞} w_j α_j` (LP duality; `+∞` if all `α_j = ∞`).

*Validity* (standard). If `λ ≥ 0` and `θ := 1 − Σ λ_j/α_j > 0`, then with
`J = {j : α_j < ∞}`,
`x̄ + Rλ = θ x̄ + Σ_{j∈J} (λ_j/α_j)(x̄ + α_j r_j) + Σ_{j∉J} λ_j r_j`.
The points `x̄ + α_j r_j` lie in `C` (closed), the `r_j` with `j ∉ J` are
recession directions of `C`, and `x̄ ∈ int C` has weight `θ > 0`, so the
point lies in `int C` and not in `S`.

*Quadratic sets.* `S = {s : q(s) ≤ 0}` with `q(s) = s^T Q s + b^T s + c`.
If `q` depends only on the coordinates `s = E x ∈ R^k`, we write
`s̄ = E x̄`, `P = E R ∈ R^{k×N}` (projected rays, columns `p_j`), and
`X = {λ ≥ 0 : q(s̄ + Pλ) ≤ 0}`. Inertia of `Q`: `n_+, n_−, n_0`.

## 2. The best single cut is the corner bound

**Theorem 1.** Let `S` be closed, `x̄ ∉ S`, and `w ∈ R^N_{>0}`.

1. If `X ≠ ∅`, `z_K(w)` is attained.
2. `z_C(w) ≤ z_K(w)` for every S-free `C` with `x̄ ∈ int C`, and
   `sup_C z_C(w) = z_K(w)` (including the case `+∞ = +∞`).
3. The supremum may be taken over maximal S-free sets.
4. (Attainment.) Let `S = {q ≤ 0}` with `q ∈ C^1`, `z = z_K(w) < ∞`, and
   suppose every minimizer `λ*` with `t* = x̄ + Rλ*` satisfies
   `∇q(t*)^T (x̄ − t*) > 0`. Then for small `δ > 0` the set
   `C_δ = conv(T* ∪ B(x̄, δ))`, `T* = conv{x̄, x̄ + (z/w_j) r_j : j}`, is
   S-free with `x̄ ∈ int C_δ` and `z_{C_δ}(w) = z`; so is every maximal
   S-free set containing it.
5. (Closure.) For every closed `S`,
   `∩_C {λ ≥ 0 : Σ_j λ_j/α_j(C) ≥ 1} = cl(conv X + R^N_+)`.

*Proof.* (1) `X` is closed and `{λ ≥ 0 : w^T λ ≤ t}` is compact for
`w > 0`.

(2) `≤` is validity: the cut halfspace contains `X`. For `≥`, let
`z = z_K(w)`, fix `ε ∈ (0, 1)` (or any `M > 0` if `z = ∞`) and put
`T_ε = x̄ + R{λ ≥ 0 : w^T λ ≤ (1 − ε) z}`. It is a compact polytope and,
by definition of `z`, disjoint from `S`; let `δ < dist(T_ε, S)`. Then
`C_ε = T_ε + δB` is closed, convex, disjoint from `S`, contains `x̄` in its
interior, and `α_j(C_ε) ≥ (1 − ε) z / w_j`. Hence
`z_{C_ε}(w) ≥ (1 − ε) z`.

(3) Every S-free closed convex set lies in a maximal one (Zorn: the closure
of a nested union of S-free convex sets is convex, and its interior is the
union of the interiors, so it is S-free), and enlarging `C` can only
increase every `α_j`.

(4) Points of `T*` in `S` are exactly the points `t*` of minimizers (their
`w`-value is `≤ z`, hence `= z`), so `M* := T* ∩ S` is compact and lies in
the far face `{w^T λ = z}`. Also `T* ∩ int S = ∅`: if a far-face point `p`
were in `int S`, the points `x̄ + (1 − η)(p − x̄)` would lie in `S` with
cost `(1 − η) z < z`. By continuity there are `η > 0` and a neighbourhood
`U` of `M*` with `∇q(t)^T (x̄' − t) ≥ η` for `t ∈ U` and `x̄'` near `x̄`.

*Claim: for small `δ`, `q ≥ 0` on `C_δ` and `q > 0` on `C_δ \ M*`.*
Otherwise there are `δ_n → 0` and `p_n = θ_n s_n + (1 − θ_n) t_n` with
`s_n ∈ B(x̄, δ_n)`, `t_n ∈ T*`, `θ_n ∈ [0, 1]`, `q(p_n) ≤ 0`,
`p_n ∉ M*`. A subsequence converges to `p = θx̄ + (1 − θ)t ∈ T* ∩ S = M*`.
Since `p` is on the far face and `x̄` is not, `θ = 0`; so `θ_n → 0` and
`t_n → p`. If `θ_n = 0` then `p_n = t_n ∈ T*` with `q(p_n) ≤ 0`, so
`p_n ∈ M*` (as `T* ∩ int S = ∅`), a contradiction. If `θ_n > 0`, the mean
value theorem gives `q(p_n) = q(t_n) + θ_n ∇q(ξ_n)^T (s_n − t_n) ≥ θ_n η/2 > 0`
for large `n`, since `q(t_n) ≥ 0`. Contradiction.

By the claim `int C_δ ∩ S ⊆ M*`. A point `m ∈ M* ∩ int C_δ` would be an
interior local minimum of `q` (value 0), so `∇q(m) = 0`, contradicting
`∇q(m)^T(x̄ − m) > 0`. So `C_δ` is S-free; it contains `T*`, hence
`α_j ≥ z/w_j` and `z_{C_δ}(w) = z` by (2).

(5) The cut halfspaces are closed, convex and upward closed and contain
`X`, so they contain `D := cl(conv X + R^N_+)`. Conversely, let `λ̂ ∉ D`.
`D` is closed, convex, with recession cone `⊇ R^N_+`, so a separating
vector `u` satisfies `u ≥ 0` and `u^T λ̂ < inf_D u^T λ = z_K(u)` (if
`D = ∅`, take `u = 1`). Replacing `u` by `u + ε1` with small `ε > 0` keeps
the strict inequality, since `z_K(u + ε1) ≥ z_K(u)`. By (2) applied to
`u + ε1 > 0` there is `C` with `z_C(u + ε1) > (u + ε1)^T λ̂`; as
`z_C` is the minimum of `(u + ε1)^T λ` over the cut halfspace, `λ̂`
violates the cut of `C`. ∎

*Remarks.* (i) Nothing requires `K` to be full-dimensional or `R` to have
full column rank. (ii) Part (5) is the finite-ray, closed-`S` form of the
sufficiency of S-free sets (Balas; Conforti–Cornuéjols–Daniilidis–
Lemaréchal–Malick, MOR 2015; Cornuéjols–Wolsey–Yıldız, Math. Program. 2015)
and is folklore; the proof is included for completeness. (iii) The KKT
condition in (4) holds whenever the Fritz John multiplier of the objective
is positive: if `σ_0 w + σ R^T ∇q(t*) − ν = 0` with `ν^T λ* = 0`, then
`σ ∇q(t*)^T (x̄ − t*) = σ_0 z`. For bilinear `q` it fails only when a single
ray grazes `∂S` at its first contact (Section 8.2).

**Proposition 2 (hypotheses are needed).**

- *(Zero reduced cost.)* `S = {(x, y) : (x + 1) y + 1 ≤ 0}`, `x̄ = 0`, rays
  `e_1, e_2`, `w = (0, 1)`. On `R^2_+` we have `q = xy + y + 1 ≥ 1`, so
  `X = ∅` and `z_K = +∞`. Every S-free `C ∋ 0` in its interior contains a
  ball `B(0, δ)`; if `α_1 = ∞` it contains `(t, −δ/2)` for all `t ≥ 0` in
  its interior, and `(2/δ, −δ/2) ∈ int S`. So `α_1 < ∞` and
  `z_C = w_1 α_1 = 0`. Hence `sup_C z_C = 0 < z_K = ∞`.
- *(Non-attainment, `w > 0`.)*
  `q(λ) = λ_1 − λ_1^2 + (1 − λ_2)^2`, `x̄ = 0`, rays `e_1, e_2`,
  `w = (1, 1)`. Then `z_K = 1`, attained only at `(0, 1)` (for
  `0 < λ_1 < 1`, `q > 0`; for `λ_1 ≥ 1` the cost is at least the golden
  ratio). If `C` is S-free with `0 ∈ int C ⊇ B(0, δ)` and `α_2 ≥ 1`, then
  `(0, 1) ∈ C`, so `C` contains `(0, 1) + s((−s, 0) − (0, 1)) = (−s^2, 1 − s)`
  in its interior for `0 < s < δ`; but `q(−s^2, 1 − s) = −s^4 < 0`. So
  `z_C < 1` for every `C`, while `sup_C z_C = 1`. Here
  `∇q(0,1)^T((0,0) − (0,1)) = 0`: the ray `e_2` is tangent to `∂S`.

Checked in exact arithmetic by `code/verify_props.py`.

## 3. Few rays suffice

**Lemma 3 (rank).** Let `T ⊂ R^k` be closed,
`X = {λ ≥ 0 : s̄ + Pλ ∈ T}`, `r = rank P`, `X_J = X ∩ {λ_{J^c} = 0}`. Then
`conv X = conv(∪_{|J| ≤ r, P_J injective} X_J) + {δ ≥ 0 : Pδ = 0}`, and for
`w ≥ 0`, `z_K(w) = min_{|J| ≤ r} inf_{X_J} w^T λ`; if the minimum is
attained, it is attained with support `J` such that `P_J` has linearly
independent columns.

*Proof.* For `λ ∈ X` the polyhedron `Π(λ) = {μ ≥ 0 : Pμ = Pλ}` lies in `X`.
It is pointed, so `Π(λ) = conv(vertices) + {δ ≥ 0 : Pδ = 0}`, and each
vertex is a basic solution, with support `J` such that `P_J` has linearly
independent columns. Also `X + {δ ≥ 0 : Pδ = 0} = X`. The LP
`min{w^T μ : μ ∈ Π(λ*)}` has a vertex solution. ∎

The refinement below uses second-order conditions. It says that the number
of rays is controlled by the *nonnegative* part of the inertia of `Q`.

**Theorem 4 (inertia bound).** Let `S = {q ≤ 0}` with
`q(s) = s^T Q s + b^T s + c`, `q(s̄) > 0`, `w > 0`, and let
`ρ(q) = n_+(Q) + n_0(Q) + 1 − [b ∉ range Q]`. Every minimizer `λ*` of
`z_K(w)` whose support `J` has `P_J` injective satisfies `|J| ≤ ρ(q)`.
Consequently some minimizer uses at most `min(rank P, ρ(q))` rays.

*Proof.* Put `t* = s̄ + P_J μ*` (`μ* > 0`) and
`g(μ) = q(s̄ + P_J μ) = μ^T G μ + 2 m^T μ + g_0` with `G = P_J^T Q P_J`.
On the open face `μ > 0`, `μ*` is a local minimizer of `w_J^T μ` subject
to `g(μ) ≤ 0`, and the constraint is active (otherwise decrease a
coordinate).

*Case `P_J^T ∇q(t*) ≠ 0`* (LICQ). There is `σ > 0` with
`w_J = −σ ∇g(μ*)`, and the second-order necessary condition gives
`d^T G d ≥ 0` for all `d` with `w_J^T d = 0`. So `Q ⪰ 0` on
`V = P_J{d : w_J^T d = 0}`, a subspace of dimension `|J| − 1` contained in
the tangent hyperplane `T = ∇q(t*)^⊥`. If `v ∈ V ∩ ker Q`, then
`0 = ∇q(t*)^T v = 2 (Q t*)^T v + b^T v = b^T v`; so
`V ∩ ker Q ⊆ ker Q ∩ b^⊥`, which has dimension `n_0 − [b ∉ range Q]`. The
image of `V` in `R^k / ker Q` is a subspace on which the nondegenerate form
induced by `Q` is PSD, hence has dimension `≤ n_+` (it meets the
`n_−`-dimensional negative definite part only in 0). So
`|J| − 1 ≤ n_+ + n_0 − [b ∉ range Q]`.

*Case `P_J^T ∇q(t*) = 0`.* Then `g(μ* + d) = d^T G d`. If `d^T G d < 0`
for some `d`, the open double cone `{d^T G d < 0}` contains `d` and `−d`,
and `w_J^T d ≠ 0` for some such `d` (the cone is open); moving along `±d`
stays feasible and decreases the cost. So `G ⪰ 0`, `Q ⪰ 0` on
`span P_J` (dimension `|J|`), and as above
`|J| ≤ n_+ + n_0 − [b ∉ range Q] < ρ(q)`. ∎

*Corollaries and remarks.*

- *Reverse convex.* If `cl(R^k \ S)` is convex, it is the unique maximal
  S-free set: every S-free `C` has `int C ⊆ R^k \ S`, hence
  `C ⊆ cl(R^k \ S)`. So its cut (the Tuy/concavity cut) has
  `z_C = sup_C z_C = z_K` for every `w > 0` by Theorem 1(2)–(3). This needs
  neither Theorem 4 nor a quadratic `S` (revised after the review, which
  pointed this out). What Theorem 4 adds for `Q ≺ 0` (`ρ = 1`) is that the
  minimum is the first hit of a single ray, the quadratic case of the
  classical vertex property of concave minimization.
- *Bilinear* `q = ±(w − xy)` on `(x, y, w)`: `n_+ = n_0 = 1` and
  `b ∉ range Q`, so `ρ = 2`: two rays suffice (used in Section 8).
- *2-variable quadratics:* `min(k, ρ) = 2`, no gain over Lemma 3. (`ρ`
  itself can be 3, e.g. `q = x^2 − 1` on `R^2`, where `n_0 = 1`; the
  earlier claim `ρ ≤ 2` was wrong.)

In 888 random bilinear corners with `N ∈ {3, 6, 10}` rays, the minimizer
had support 1 in 749 cases, 2 in 139, and never 3
(`code/support_stats.py`).

## 4. Complexity

**Theorem 5.** Let `r = min(k, ρ(q))`.

1. *(Fixed `r` is polynomial.)* Given rational data and a rational `t`, one
   can decide `z_K(w) ≤ t` (`w > 0`) in time polynomial in the input size
   for every fixed `r`; hence `z_K` can be approximated to relative
   accuracy `ε` in time polynomial in the input size and `log(1/ε)`.
2. *(Normal-fan pieces.)* If `rank P = k`, only `O(N^{⌊k/2⌋})` supports of
   size `k` (and their subsets of size `≤ r`) are needed: the maximal cones
   of a triangulation refining the normal fan of
   `D_w = {y ∈ R^k : P^T y ≤ w}`. For `k = 3` there are at most `2N − 4`
   cells and at most `3N − 6` two-ray edges.
3. *(Closed forms.)* A support-`J` subproblem
   `min{w_J^T μ : μ ≥ 0, g(μ) ≤ 0}` is solved by enumerating the `2^{|J|}`
   faces; on a face `F` with nonsingular `G_F` the KKT point is
   `μ_F = −G_F^{-1}(m_F + τ w_F)`,
   `τ^2 = (m_F^T G_F^{-1} m_F − g_0)/(w_F^T G_F^{-1} w_F)`. For `|J| ≤ 2`
   every case (including singular `G_F`) is handled exactly by maximizing
   `u_+(θ)`, the larger root of `g_0 u^2 + b(θ) u + a(θ)`, over
   `θ ∈ [0, 1]`; the candidates are the endpoints and the real roots of
   three explicit quadratics (`code/core.py: two_ray`).
4. *(Hardness.)* Computing `z_K` is NP-hard when `k` is part of the input,
   even for `K = R^k_+`, `s̄ = 0`, `w = 1`, `q = μ − s^T A_G s`. Deciding
   `z_K ≤ t` for rational `t` is NP-hard, and approximating `z_K` within
   relative error `1/(5k^2)` is NP-hard.

*Proof.* (1) By Theorem 1(1) the minimum is attained, and by Lemma 3 and
Theorem 4 at a support of size `≤ r`. So `z_K ≤ t` iff for some `J` with
`|J| ≤ r` the sentence `∃μ ∈ R^J : μ ≥ 0, w_J^T μ ≤ t, g_J(μ) ≤ 0` holds.
There are `O(N^r)` such `J`; each sentence has `≤ r` variables and
`r + 2` polynomials of degree `≤ 2`, so Renegar's algorithm (1992) decides
it in time polynomial in the bit size for fixed `r`. Bisection gives the
approximation.

(2) For `z ∈ cone P`, `φ(z) := min{w^T λ : λ ≥ 0, Pλ = z} = max{y^T z : y ∈ D_w}`
by LP duality, so `z_K = min{φ(z) : s̄ + z ∈ S, z ∈ cone P}`. `D_w` is
pointed (`rank P = k`) and `φ(z) = y_v^T z` on the normal cone
`N_v = cone{p_j : p_j^T y_v = w_j}` of each vertex `y_v`. Perturb `w`
lexicographically; the perturbed polyhedron is simple, has at most
`O(N^{⌊k/2⌋})` vertices by the upper bound theorem (bound an unbounded
`D_w` by one extra facet), and its normal cones triangulate the `N_v`. On a
cell `σ = cone P_J ⊆ N_v`, `y_v^T P_J μ = w_J^T μ`, so the cell problem is
the `J`-subproblem, and its minimizer has support `≤ r` (Theorem 4). For
`k = 3`, a simple 3-polyhedron with `N` facets has at most `2N − 4`
vertices, and a triangulated sphere or disk with `≤ N` vertices has at most
`3N − 6` edges.

(3) For fixed `θ`, `ν(θ) = (θ/w_i, (1 − θ)/w_j)` and
`g(τ ν) = a(θ) τ^2 + b(θ) τ + g_0`, `g_0 > 0`. The smallest feasible `τ` is
`1/u_+(θ)`, and `u_+` is continuous where the discriminant
`D = b^2 − 4 g_0 a ≥ 0`. Its maximum over `[0, 1]` is at an endpoint, at a
zero of `D`, or where `D' = 2 b' √D`, which after squaring is the quadratic
`D'^2 = 4 b'^2 D`; if that identity holds identically, `√D` is linear and
`u_+` is piecewise linear with kinks at zeros of `D`, and if `b' = 0` the
condition is `D' = 0`.

(4) By Motzkin–Straus, `max_{ν ∈ Δ} ν^T A_G ν = 1 − 1/ω(G)`. With
`λ = τ ν`, `q(λ) ≤ 0` iff `τ ≥ (μ/ν^T A_G ν)^{1/2}`, so
`z_K = (μ ω/(ω − 1))^{1/2}` (for `ω ≥ 2`). With `μ = ω_0(ω_0 − 1)`,
`z_K ≤ ω_0` iff `ω(G) ≥ ω_0`. With `μ = 1`, consecutive values satisfy
`f(ω)/f(ω + 1) = (1 − 1/ω^2)^{−1/2} ≥ 1 + 1/(2k^2)`, and for
`δ = 1/(5k^2)`, `(1 + δ)/(1 − δ) < 1 + 1/(2k^2)`, so a `δ`-approximation
determines `ω(G)`. `Q = −A_G` is indefinite whenever `G` has an edge. ∎

By Theorem 1(2), (4) also says that the best single-cut bound over all
maximal quadratic-free sets is NP-hard to compute or approximate. The
hardness uses `ρ(q) = n_−(A_G) + n_0(A_G) + 1`, which is unbounded over the
graphs in the reduction; by Theorem 5(1), unless P = NP, hardness needs both
`k` and `ρ` unbounded.

*Remark (efficacy).* The set of cut vectors `{a ≥ 0 : a^T λ ≥ 1 on X}` is
convex, and `z_K(a) ≥ 1` is its membership test. With the oracle of
Theorem 5(1), the ellipsoid method optimizes convex criteria (e.g.
Euclidean efficacy) over valid cut vectors in polynomial time for fixed `r`,
up to `ε`. This is the scout's claim, restated with its hypothesis.

*Checks.* `code/verify_props.py` confirms `z_K = ω_0` (with
`μ = ω_0(ω_0 − 1)`) on `C_5` and six random graphs.
`code/validate_corner.py` compares the support-enumeration `z_K` with SCIP
global solves on 77 random instances (bilinear, `k = 2`, `k = 3`,
`N ≤ 6`): no mismatch, maximum relative difference `2.8·10^-6`.

## 5. The implemented set can be arbitrarily bad

SCIP's quadratic intersection cuts (Chmiela–Muñoz–Serrano, Math. Program.
197, 2023; `nlhdlr/quadratic/useintersectioncuts`, off by default in SCIP
10) use one Muñoz–Serrano set per cut, `{‖y‖ ≤ λ^T x̂}` in eigen-coordinates
with the fixed direction `λ = x̂(s̄)/‖x̂(s̄)‖`.

**Proposition 6.** Let `S = {(x, y) : y^2 ≥ x^2 + 1}`, `x̄ = (x_0, 0)` with
`x_0 > 0`, rays `r_1 = (−1, 0)`, `r_2 = (0, 1)`, and `w = (ε, 1)` with
`0 < ε < 1` and `x_0 ≥ ε/√(1 − ε^2)`. (This is the corner of
`min{−εx + y : y^2 ≥ x^2 + 1, x ≤ x_0, y ≥ 0}` at `(x_0, 0)`.)

- SCIP's set (Chmiela Case 2, `κ = 1`) is
  `{|y| ≤ (x_0 x + 1)/√(1 + x_0^2)}` and gives
  `z_SCIP = min{ε(x_0 + 1/x_0), √(1 + x_0^2)}`.
- The strip `{|y| ≤ 1}` is the Muñoz–Serrano set of the same family with
  `λ = (0, 1)`; it is maximal S-free and gives `z = 1`.
- `z_K = ε x_0 + √(1 − ε^2)`.

With `ε = x_0^{-2}`, `z_SCIP/z_K → 0` as `x_0 → ∞`, while the strip attains
`z/z_K → 1`.

*Proof.* Along `r_1`, `(x_0 − t, 0)` stays in SCIP's set iff
`x_0(x_0 − t) + 1 ≥ 0`, so `α_1 = x_0 + 1/x_0`; along `r_2`,
`α_2 = √(1 + x_0^2)`. For the strip, `α_1 = ∞`, `α_2 = 1`. The strip is
S-free (`y^2 < 1 ≤ x^2 + 1`) and maximal: adding a point with `|y| > 1`
brings a band `1 < y < 1 + η` (all `x`) into the interior, and it contains
`(0, 1 + η/2) ∈ S`. For `z_K`, minimize `ελ_1 + √((x_0 − λ_1)^2 + 1)`; the
stationary point `x_0 − λ_1 = ε/√(1 − ε^2)` is feasible by assumption and
gives the value. ∎

Numerically (`code/verify_props.py`, reimplementation of the Chmiela
formulas in `code/scout_sfree.py`): `x_0 = 10^3`, `ε = 10^{-6}` gives
`z_SCIP = 0.001`, strip `1`, `z_K = 1.001`.

*Remark 7 (the whole constant-`λ` family).* The scout's Proposition 6 goes
further. Take `S` as above, `x̄ = 0`, `w = (1, 1)`, `r_1 = (a, r)` with
`r = √(1 + a^2)`, and `r_2 = −r_1 + η n` with `n ∝ (r, −a)` a unit vector.
The constant-`λ` sets containing `0` in their interior are
`{|y| ≤ (ux + 1)/s_u}`, `s_u = √(1 + u^2)`, with cut coefficients
`a_j(u) = max(0, |r_{j,y}| s_u − u r_{j,x})`. For `η = 0` these are
`(r s_u − ua, r s_u + ua)`, so `(1/(2r), 1/(2r))` satisfies every such cut
and the closure of the whole family gives at most `1/r`. The oblique split
`{|ry − ax| ≤ 1}` is S-free (on `S`, `y = ρ cosh φ`, `x = ρ sinh φ` with
`|ρ| ≥ 1`, and `|ry − ax| = |ρ| cosh(φ − θ) ≥ 1` with `cosh θ = r`) and exits
both rays at their first S-points. For a pointed cone, `η` must be small:
with `η = a^{-1}`, `z_K ≈ 0.51`. With `η = a^{-3}` (`code/remark7.py`, the
closure bound certified by the point `c(1, 1)`, `c = 1/min_u(a_1 + a_2)`,
a convex 1-D minimization):

| `a` | `z_K` | oblique split | closure of all constant-`λ` sets `≤` |
|---|---|---|---|
| 10 | 0.98612 | 0.98602 | 0.09950 |
| 100 | 0.99986 | 0.99986 | 0.0100 |
| 1000 | 0.999999 | 0.999999 | 0.0010 |

So even the closure of the implemented family can be arbitrarily worse than
one cut from a Lorentz-boosted set (the split is the image of the strip
`{|y| ≤ 1}` under a boost), which is the mechanism behind Theorem 8.

## 6. Transformations and signature `(n, 1)`

Muñoz–Serrano (Math. Program. 192, 2022, §6, arXiv:1911.12341) show that
the maximal set their construction produces "heavily depends on the choice
of `T`", the linear map bringing the (homogenized) quadratic to the form
`{‖x‖ ≤ ‖y‖}` (sliced by a hyperplane `H` in the inhomogeneous case), and
leave "the role of different transformations" open (§7). The admissible `T`
are the isometries of the homogenized form, i.e. `O(n, m)` up to scaling.

Notation (Muñoz–Paat–Serrano, "MPS"): `Q_h = {(x, y) ∈ R^n × R^m : ‖x‖ ≤ ‖y‖}`,
`C_Γ = {(x, y) : Γ(β)^T x ≥ β^T y ∀β ∈ D^m}` for `Γ : D^m → D^n` (unit
spheres). The Muñoz–Serrano set is `C_λ` (constant `Γ ≡ λ`).

**Theorem 8.** Let the homogenized form have signature `(n, m)` on its
nondegenerate part.

1. *(Homogeneous, `m = 1`, `n ≥ 2`.)* Every full-dimensional maximal
   `Q_h`-free set equals `L(C_λ)` for some `L ∈ SO^+(n, 1)` (and any fixed
   `λ`).
2. *(Homogeneous, `n = 1`, any `m ≥ 1`.)* The full-dimensional maximal
   `Q_h`-free sets are exactly the two sets `{±x ≥ ‖y‖}`, i.e. `C_λ` with
   `λ = ±1`.
3. *(Inhomogeneous.)* Let `S = {s ∈ R^k : q(s) ≤ 0}` with homogenized form of
   signature `(n, 1)` or `(1, m)` (plus possibly zero eigenvalues). Every
   full-dimensional maximal S-free set is the slice at `t = 1` (times the
   lineality space of the zero-eigenvalue coordinates) of `L(C_λ)` for some
   automorphism `L` of the form. In words: the Muñoz–Serrano set with a
   *free* direction `λ`, under all admissible transformations, reaches every
   maximal S-free set. (With `λ` tied to the point, as in Muñoz–Serrano and
   SCIP, it does not; Section 6.1.)

*Proof.* (1) By MPS Theorems 1.1–1.2 (arXiv:2211.05185), a full-dimensional
maximal set is `C_Γ` with `Γ` non-expansive and
`0 ∉ conv{(Γ(β), −β)}`. For `m = 1`, `D^1 = {±1}`, non-expansiveness is
automatic, and the second condition says `γ_1 := Γ(1) ≠ −Γ(−1) =: −γ_2`.
So `C = {γ_1^T x ≥ y, γ_2^T x ≥ −y}`, the intersection of two halfspaces
whose normals `(γ_1, −1)` and `(γ_2, 1)` are null vectors of the dual
Lorentz form. Represent such a halfspace pair by the two points
`ξ_1 = γ_1`, `ξ_2 = −γ_2` of the celestial sphere `S^{n−1}` (the future
null directions `(ξ, 1)` of `J·normal`, `J = diag(I_n, −1)`); they are
distinct exactly by the maximality condition, and `C_λ` corresponds to the
antipodal pair `(λ, −λ)`. An `L ∈ SO^+(n, 1)` maps the halfspace with
normal `ν` to the one with normal `J L J ν` and preserves time orientation,
so it acts on the pair by the induced Möbius transformation of `S^{n−1}`,
sending normals to positive multiples. The orientation-preserving Möbius
group (`PSL_2(R)` for `n = 2`) is transitive on ordered pairs of distinct
points, so some `L` maps `(λ, −λ)` to `(ξ_1, ξ_2)`.

(2) If `n = 1`, `Γ` takes values in `{±1}`. For `m ≥ 2`, non-expansiveness
with `‖Γ(β) − Γ(β')‖ = 2` forces `β' = −β`, so a non-constant `Γ` would
have `D^m = {β, −β}`, impossible. For `m = 1` the condition
`0 ∉ conv{(Γ(1), −1), (Γ(−1), 1)}` forces `Γ(1) = Γ(−1)`.

(3) By MPS 2026 (arXiv:2605.30602), §2.1, after homogenization and
diagonalization `S` becomes `Q'_g = {‖x‖ ≤ ‖y‖, a^T x + d^T y + h^T z = −1}`
inside the hyperplane `H'` given by the linear equation.

*Lineality.* If `S' ⊆ R^p` satisfies `S' + V = S'` for a subspace `V`, every
*full-dimensional* maximal S'-free set `C` satisfies `C + V = C`: for convex
`C` with `int C ≠ ∅`, `int cl(C + V) = int(C + V) = int C + V`, which misses
`S'` (if `c + v ∈ S'` then `c ∈ S' − v = S'`), so `cl(C + V)` is S'-free and
contains `C`. Full dimension is needed (recheck): in `R^2`,
`S' = V = R × {0}` and `C = {0} × R` is maximal S'-free (any convex
enlargement contains a strip whose interior meets the `x`-axis), yet
`C + V = R^2`. Only full-dimensional sets are used below.

*Case `h ≠ 0`.* The map `(x, y, z) ↦ (x, y, z − (h^T z/‖h‖^2) h)` is an
affine bijection of `H'` onto `R^{n+m} × h^⊥` (the removed component is
recovered from the equation), and it sends `Q'_g` onto `Q_h × h^⊥`. By
lineality every maximal set there is `C × h^⊥` with `C` maximal `Q_h`-free
(a larger `Q_h`-free set would give a larger product). Pulled back, the
maximal S-free sets are the slices of `C × R^ℓ`. Muñoz–Serrano (§4, after
Remark 5) state only the converse direction ("`C × R^ℓ` is maximal"); this
two-line argument, from the review, supplies the direction used here.

*Case `h = 0`.* Then `Q'_g = Q_g × R^ℓ`, and by lineality the maximal sets
are (maximal `Q_g`-free) `× R^ℓ`. MPS 2026, Lemma 1: every
full-dimensional maximal `Q_g`-free set is `C_Γ ∩ H` with `C_Γ` a maximal
`Q_h`-free set (its proof: `cone(K)` is `Q_h`-free, extend it by Zorn,
slice back, use maximality of `K`).

In both cases `C_Γ` (resp. `C`) is maximal `Q_h`-free, so by (1)–(2) it is
`L(C_λ)`. ∎

*Consequences.*

- Every *indefinite* quadratic in two variables has a 3×3 homogenized form
  with at least one eigenvalue of each sign (its 2×2 part is indefinite),
  so it has signature `(2, 1)`, `(1, 2)`, or `(1, 1)` plus a zero
  eigenvalue. So for `k = 2` the orbit family (with `λ` free) is complete,
  and by Theorem 1 the best orbit cut equals `z_K`. (Convex and
  reverse-convex quadratics are classical; degenerate forms such as `x^2`
  are not covered by the statement.)
- In signature `(n, 1)` the orbit sets are
  `{γ_1^T x ≥ y, γ_2^T x ≥ −y}`; relaxing `‖γ_i‖ = 1` to `‖γ_i‖ ≤ 1` keeps
  them `Q_h`-free, so the best orbit cut for a target `z` is two independent
  SOCP feasibility problems and bisection on `z`. For `(1, m)` there are
  only two candidate sets.
- Chmiela et al.'s Cases 1–3 are slices of `C_λ` in eigen-coordinates.
  With `λ` free, "SCIP's sets under all transformations" form the orbit
  family; with SCIP's rule for `λ` they form the smaller point-rule family
  of Section 6.1.
- Muñoz–Serrano conjectured (§7) that their method "produces all maximal
  quadratic-free sets in 3 dimensions". If "3 dimensions" refers to the
  homogenized space (`n + m = 3`, i.e. quadratics in two variables and
  homogeneous quadratics in three), Theorem 8 proves this, in the stronger
  form that one fixed set and its orbit suffice. If it refers to `S ⊂ R^3`,
  it is false already for `S = {w ≤ xy}` (Remark 15), and Theorem 14 shows
  that the missing sets matter for cut strength.
- The case `h ≠ 0` is now proved in full (lineality argument above).

*Check* (`code/orbit_n1.py`): 24 random 2-variable corners (13 of signature
`(2, 1)`, 11 of `(1, 2)`, 2–5 rays); the best orbit bound (SOCP bisection)
divided by `z_K` is `1.00000000` in every case. This checks Theorem 1
together with the MPS parametrization of the `(n, 1)` sets; the Lorentz
transitivity itself is group theory and needs no numerical check.

### 6.1 The point rule for `λ` is not enough

Muñoz–Serrano (Theorem 7, Example 9) and Chmiela et al. (Cases 1–4) take
`λ = x̂(Ts̄)/‖x̂(Ts̄)‖`, where `Ts̄ = (x̂, ŷ)` in the transformed coordinates.
Then `Ts̄ = ((‖x̂‖) λ, ŷ)` lies in the plane spanned by the two tangency null
lines `(λ, 1)` and `(λ, −1)` of `C_λ` (for `m = 1`). This property is
invariant under automorphisms. So for signature `(n, 1)`, every set the rule
produces under any transformation is `{γ_1^T x ≥ y, γ_2^T x ≥ −y}` with the
homogenized `s̄` in the span of its tangency lines `(γ_1, 1)` and
`(γ_2, −1)`:
`u_s = (x̂, ŷ) = a(γ_1, 1) + b(γ_2, −1)` with `a, b > 0` (positivity is
equivalent to `s̄ ∈ int C`, since `γ_1^T x̂ − ŷ = b(1 + γ_1^T γ_2)` and
`γ_2^T x̂ + ŷ = a(1 + γ_1^T γ_2)`). Conversely every such pair arises, by
2-transitivity. For `n = 2`, `γ_1 = (cos θ, sin θ)` determines
`a = (‖x̂‖^2 − ŷ^2)/(2(γ_1^T x̂ − ŷ))`, `b = a − ŷ`, `γ_2 = (x̂ − aγ_1)/b`:
a **one-parameter** family, while the maximal sets containing `s̄` form a
two-parameter family (pairs of distinct points of the circle).

The rule therefore reaches at most a one-parameter family of sets at a
fixed `s̄` (one set per pair, i.e. per `θ`), also after any enlargement
applied to each member, whereas the maximal sets containing `s̄` form a
two-parameter family. *Slice picture* (from the recheck): when both
tangency points lie on the slice side, `u_s = a t_1 P_1 + b t_2 P_2` is a
convex combination of the tangency points `P_i ∈ H`, so the rule at `s̄`
produces exactly the maximal sets whose two tangency points lie on a chord
through `s̄`.

*Enlargement.* In Case 2 (`‖d‖ < ‖a‖`) MPS 2026 Theorem 5 allows no dropped
inequality, but Muñoz–Serrano's §5.2 construction still *enlarges* a
member whose tangency point lies on the wrong side of `H`: it replaces that
inequality `−λ^T x + β^T y ≤ 0` by `−λ^T x + ∇φ_λ(β)^T y ≤ r(β)`. This new
inequality vanishes on the null vector `(x_β, β)`, where `x_β` solves their
problem (11), so `λ^T x_β = φ_λ(β)` and `a^T x_β + d^T β = 0`. Its tangency
line therefore lies in `H_0 = {h = 0}`, i.e. it is one of the (at most two)
asymptotic null halfspaces. So each set Muñoz–Serrano can return is either
a plain member or its kept halfspace intersected with one of two explicit
asymptotic halfspaces.

*Check.* Commands: `code/point_rule_check.py 0 40`,
`code/point_rule_crosscheck.py`, `code/point_rule_refine.py` and
`code/ms_asymptote_check.py`. The generator yields 40 random two-variable
corners with `κ > 0` (Chmiela Case 2) and 2–4 rays; 4 of them have
`z_K = ∞` (no ray combination meets `S`) and are skipped, leaving 36. `θ` is
scanned on 20001 (or `10^5`) points with local refinement.

- The full orbit (`λ` free) attains `z_K` in all 36. The SOCP bisection was
  run on the 13 misses (`z_K` confirmed there by SCIP); for the other 23
  this follows because the point-rule family is contained in the orbit.
- The plain point-rule sets `C_λ ∩ H` miss `z_K` in 13 of the 36, with
  ratios 0.119, 0.217, 0.242, 0.302, 0.484, 0.526, 0.546, 0.629, 0.674,
  0.707, 0.966, 0.967, 0.967. SCIP's own set, which is one member (in
  Chmiela's coordinates `d = 0` and `λ^T a < 0`, so nothing is enlarged), is
  never better than the family optimum, as it must be.
- **Muñoz–Serrano's full construction also misses `z_K` on all 13** (numerical
  evidence). This result is the recheck's (`../reviews/sfree-recheck.md` §2).
  It implemented `φ_λ` and `r(β)` literally under every transformation,
  after reproducing their Example 8. I reproduced it independently with the
  transformation-free upper bound above (`ms_asymptote_check.py`: best of
  the plain member and the two asymptotic replacements for every `θ`,
  `10^5` points with refinement). Only corners 9 and 31 improve, from 0.674
  to 0.689 and from 0.217 to 0.249; the largest ratio is 0.9669. My earlier
  "generous relaxation" (any null halfspace as replacement) reached `z_K`
  only because it ignored that Muñoz–Serrano use one of the two asymptotes;
  it is kept in `point_rule_refine.py` for the record.

So with `λ` tied to the point, Muñoz–Serrano's construction under all
transformations is not enough on these corners (numerically), while letting
`λ` vary (the whole orbit) is (Theorem 8). The reviewer, using another
generator, found 2 misses in 24 corners (0.989, 0.944) for the plain sets.

*On Muñoz–Serrano's conjecture* (§6 above). Their "method" uses the point
rule. For `n + m = 3` the conjecture also holds with the point rule if `s̄`
may vary: every maximal set is produced from any `s̄` on the open chord
between its two tangency points (recheck, §2). It fails at a fixed `s̄`.

## 7. The rank-1 closure is not the convex hull

The scout checked that the *non-local* S-free closure of a polytope `P`
(all S-free sets, not tied to a vertex) equals `conv(P ∩ S)` for every
closed `S`: if `a^T x ≥ b` is valid for `P ∩ S` and violated at `p`, then
`(P ∩ {a^T x ≤ b'}) + εB` is S-free for `a^T p < b' < b` and small `ε`.
Intersection cuts in solvers are tied to LP bases, and then one round is not
enough, even in the plane and even for reverse-convex `S`.

**Proposition 9.** Let `P = conv{(0, 2), (−1/2, 0), (1/2, 0)}` and
`S = {x : ‖x‖ ≥ 1}`, so the closed unit disk `D` is the unique maximal
S-free set. The rank-1 closure (all intersection cuts from all bases of
`P`) is `conv{(0, 2), p_1, X, p_2}`, where `p_{1,2} = (∓(1 − t)/2, 2t)` with
`t = (1 + 2√13)/17` are the exits of the slanted edges from `D`, and
`X = (0, (1 + √13)/6) ≈ (0, 0.7676)`. Since `conv(P ∩ S) = conv{(0, 2), p_1, p_2}`
has lowest point at height `2t ≈ 0.9660`, the rank-1 closure is strictly
larger than the hull. A second round (the basis at `X`) gives the chord
`p_1 p_2` and closes the gap.

*Proof.* The vertex `(0, 2)` lies in `S` and gives no cut. At
`u = (−1/2, 0)` the basis rays point to `(0, 2)` and to `(1/2, 0)`; they
leave `D` at `p_1 = u + t((0, 2) − u)` (solve `‖u + t((0,2) − u)‖ = 1`, i.e.
`17t^2 − 2t − 3 = 0`) and at `e_1 = (1, 0)`. Every S-free set is contained in
`D`, so the disk cut (the line through `p_1` and `e_1`) is the strongest
cut at `u`; symmetrically at `(1/2, 0)`. The two lines meet on the axis at
height `2t/(3/2 − t/2) = (1 + √13)/6 < 2t`. At `X` the tight constraints
are the two cuts, whose rays point to `p_1` and `p_2` on `∂D`, so the next
cut is the chord. ∎

Checked in exact arithmetic (`code/verify_props.py`, part F). So the loop
"vertex → strongest intersection cut" needs several rounds even when every
single cut is optimal; this is the practical counterpart of Theorem 1(5),
which describes the closure at *one* vertex.

## 8. Bilinear constraints

*Which rank-2 quadratics.* Let `Q` have rank 2 and signature `(1, 1)`, so
`q(s) = (u^T s)(v^T s) + b^T s + c`. If `b ∈ range Q = span{u, v}`, then `q`
depends on two coordinates, its homogenized form has signature `(2, 1)`,
`(1, 2)` or `(1, 1)` plus a zero eigenvalue, and Theorem 8 applies: the
transformation family is complete and attains `z_K` (with `ρ ≤ 2`). If
`b ∉ range Q`, an affine change of coordinates maps `S` to `{w ≤ xy}` or
`{w ≥ xy}` (times free coordinates), whose homogenized form has signature
`(2, 2)`. This section treats that case; the obstruction of Section 8.5
shows that for such `q` the transformation family is not exact.

### 8.1 The determinant model and the two families

Let `S = {(x, y, w) : w ≤ xy}` ("side +", violated when `w̄ > x̄ȳ`); the
side `w ≥ xy` is symmetric (below). Put
`M(x, y, w; h) = [[w, x], [y, h]]`, so `det M(s, 1) = w − xy = q(s)` and
the homogenized form is `det`, of signature `(2, 2)`. (For `w ≥ xy` use
`M = [[x, w], [h, y]]`, `det = xy − wh`.) `H = {h = 1}`.

**Lemma 10.**

1. The automorphism group of `det` on `R^{2×2}` is
   `{M ↦ AMB^T, M ↦ AM^TB^T : det A · det B = 1}`.
2. In suitable Sylvester coordinates the Muñoz–Serrano set `C_λ` is
   `C_I = {M : sym(M) ⪰ 0}`, and its orbit is
   `{C_F : det F > 0}`, `C_F = {M : sym(F^T M) ⪰ 0}` (`C_{cF} = C_F` for
   `c > 0`: 3 parameters).
3. For invertible `F`, `C_F` is full-dimensional, and it is `Q_h`-free iff
   `det F > 0`; its boundary touches the null cone
   along the rank-one matrices `F^{-T} bb^T`, which in the slice is the curve
   `{(x, φ(x), xφ(x))}` with `φ` the increasing Möbius map induced by
   `F^T`.
4. (Maximal completion.) The inequality of `C_F` indexed by `v ∈ R^2` is
   `⟨F vv^T, M⟩ ≥ 0`; MPS 2026 keeps it iff its tangency point
   `F^{-T}(Jv)(Jv)^T` (`J = [[0, 1], [−1, 0]]`) has `h ≥ 0`. For `det F > 0`
   this is equivalent to `⟨F vv^T, E⟩ ≥ 0` with `E = M(e_w; 0) = e_1 e_1^T`,
   and
   `C_F^G := {M : ⟨F vv^T, M⟩ ≥ 0 for all kept v} = cl(C_F + R_+ E)`.
   In the slice: `C_F^G ∩ H = cl((C_F ∩ H) + R_+ e_w)`, the upward closure.
   (Side `w ≥ xy`: `E = e_1 e_2^T`, kept iff `⟨F vv^T, −E⟩ ≥ 0`, downward
   closure.)

*Proof.* (1) Standard (`SO^+(2,2) ≅ (SL_2 × SL_2)/±1`; the determinant is
preserved by `M ↦ AMB^T` with `det A det B = 1` and by transposition).

(2) With `Φ(x_1, x_2, y_1, y_2) = x_1 I + x_2 J + y_1 K + y_2 L`
(`K = diag(1, −1)`, `L = [[0, 1], [1, 0]]`),
`det Φ = x_1^2 + x_2^2 − y_1^2 − y_2^2`, and
`sym(Φ) = [[x_1 + y_1, y_2], [y_2, x_1 − y_1]]` has eigenvalues
`x_1 ± ‖y‖`; so `Φ(C_{e_1}) = C_I`. Any two Sylvester coordinate systems
differ by an automorphism, so the orbits agree. Under `M ↦ AMB^T`,
`C_I ↦ {M : sym(BA^{-1} M) ⪰ 0}` (substitute `v = B^T u` in
`v^T A^{-1} M B^{-T} v ≥ 0`), i.e. `C_F` with `F^T = BA^{-1}` and
`det F = 1/(det A)^2 > 0`; transposition fixes `C_I`. Conversely `C_F` is
the image under `A = aI`, `B = aF^T`, `a^4 det F = 1`.

(3) `C_F ⊇ F^{-T}·{PD matrices}` is full-dimensional. If `sym(F^T M) ≻ 0`,
the real parts of the eigenvalues of `F^T M` are positive, so
`det(F^T M) > 0` and `det M` has the sign of `det F`. A
rank-one `M = ab^T` lies in `C_F` iff `sym((F^T a) b^T) ⪰ 0` iff
`F^T a ∈ R_+ b`.

(4) `adj(F^T) = JFJ^T` gives `F^{-T} = JFJ^T/det F`, and a direct
computation gives `h(F^{-T}(Jv)(Jv)^T) = (Fv)_1 v_1 / det F` while
`⟨Fvv^T, e_1e_1^T⟩ = (Fv)_1 v_1`. Next, `C_F = (F·PSD)^*`, so
`C_F^* = F·PSD` and `(C_F + R_+E)^* = {FY : Y ⪰ 0, ⟨Y, Z⟩ ≥ 0}` with
`Z = sym(F^T E)`. *2×2 rank-one decomposition:* if `Y = LL^T ⪰ 0` and
`⟨Y, Z⟩ ≥ 0`, let `φ(θ) = (Lu_θ)^T Z (Lu_θ)`; then
`φ(θ) + φ(θ + π/2) = ⟨Y, Z⟩` and `φ(θ + π/2) − φ(θ)` changes sign over
`[0, π/2]`, so some `θ` has `φ(θ) = φ(θ + π/2) ≥ 0` and
`Y = Lu_θ u_θ^T L^T + Lu_{θ+π/2} u_{θ+π/2}^T L^T` with both terms kept
(this is the 2×2 case of Sturm–Zhang, MOR 2003). Hence
`(C_F + R_+E)^* = cone{Fvv^T : v kept}` and, by the bipolar theorem,
`C_F^G = cl(C_F + R_+E)`. Slicing commutes because `E` has `h = 0` and
`int C_F^G` meets `H`. ∎

So there are two natural "transformation families" for `w ≤ xy`:

- **(A) sliced orbit sets** `C_F ∩ H`: the Muñoz–Serrano homogeneous set
  under every admissible transformation, sliced at `h = 1` (the scout's
  experiment E12; S-free, not always maximal);
- **(B) maximal completions** `C_F^{G_F} ∩ H = cl((C_F ∩ H) + R_+ e_w)`:
  MPS 2026 Theorem 4 (here `‖a‖ = ‖d‖` because `H` is a null hyperplane for
  `det`) says these are maximal (away from one exceptional `F`). SCIP's Case
  4 set is the member with constant `Γ ≡ λ` in Chmiela's coordinates: their
  `φ_λ(y)` equals `max_{β ∈ G} β^T y` over the spherical cap
  `G = {β : β_{last} ≤ λ_{p_+ + 1}}`. So (B) is "SCIP's construction under
  every transformation and every `λ`".

A point `s` lies in a (B) set iff `s − τ e_w ∈ C_F` for some
`0 ≤ τ ≤ q(s)` (below that the point is in `int S`), i.e. iff the 2×2
pencil `sym(F^T M(s)) − τ sym(F^T E)` is PSD for some `τ ≥ 0`
(`code/bilinear.py: in_B`). By the S-lemma this is the same as the
kept-inequality description; `code/test_B_identity.py` confirms the
identity numerically on 9998 of 10000 random (F, point) pairs, the two
disagreements being boundary cases of the angular grid used for the kept
inequalities.

### 8.2 Exact corner bound and attainment

**Theorem 11.** For a bilinear constraint (either side) and `w > 0`:

1. `z_K(w) = min(min_j w_j t_j, min_{i<j} z_{ij})`, where `t_j` is the first
   hit of ray `j` and `z_{ij}` the closed-form two-ray value of Theorem
   5(3). This is `O(N^2)` closed forms; with the normal fan of Theorem 5(2),
   `O(N log N)` time (3-D convex hull) plus at most `4N − 6` closed forms.
2. The supremum of Theorem 1 is attained (by a set containing
   `conv(T* ∪ B(s̄, δ))`) unless some minimizer is the first contact of a
   single ray that is tangent to `∂S` there.

*Proof.* (1) Theorem 4 with `ρ = 2`, and Theorem 5(2)–(3). (2) `∇q ≠ 0`
everywhere (`∂q/∂w = ±1`). In Theorem 1(4) the condition fails only if the
Fritz John multiplier of the objective vanishes, i.e.
`P_J^T ∇q(t*) = 0`; by the second case of the proof of Theorem 4 this
forces `Q ⪰ 0` on `span P_J`, of dimension
`≤ n_+ + n_0 − 1 = 1`, so `|J| = 1` and the ray is tangent at its contact
point. ∎

So the *best single-cut bound* is cheap. The corner-optimal cut
`w^T λ ≥ z_K` is its limit and is itself valid. Section 9 shows that this
objective-parallel cut is a poor practical choice; what matters is a
maximal set whose cut dominates it.

### 8.3 The best orbit cut is a quasiconvex problem

**Proposition 12.** For fixed `z`, the set of `F` with
`sym(F^T M(s̄)) ≻ 0` and `sym(F^T M(s̄ + (z/w_j) p_j)) ⪰ 0` for all `j` is a
convex cone, and it shrinks as `z` grows. Hence
`z_A := sup{z_{C_F}(w) : F}` is found by bisection on `z`, each step an SDP
with `N + 1` blocks of size 2 in 4 variables; the returned `F` certifies a
lower bound (`code/core.py: best_orbit_bound`). `z_A ≤ z_B ≤ z_K`, where
`z_B` is the supremum over family (B); the (B) problem is bilinear in
`(F, τ)` and is solved here by Nelder–Mead from the (A) optimum and random
starts.

*Proof.* `C_F ⊇ T_z` iff it contains the vertices of `T_z`, and each vertex
condition is a linear matrix inequality in `F`. The strict condition at `s̄`
already forces `det F > 0`: `sym(F^T M(s̄)) ≻ 0` gives `det(F^T M(s̄)) > 0`,
and `det M(s̄) = q(s̄) > 0`. ∎

This replaces the scout's 7-parameter Nelder–Mead search by an exact
convex computation.

### 8.4 Tangent edges are rigid

Let `t*` be the unique corner minimizer and suppose its support is two rays
`{i, j}` (a *tangent edge*): `t* = s̄ + Pλ*` lies in the relative interior of
the edge `e = [v_i, v_j]` of `T*` (`v_l = s̄ + (z/w_l) p_l`), and
`d = v_i − v_j` satisfies `∇q(t*)^T d = 0` (KKT) and `det M(d; 0) > 0`
(second order; `= 0` means `e` lies on a ruling of `∂S`). Write
`M_0 = M(t*) = a_0 b_0^T` (rank one).

**Lemma 13.** If `F` is invertible and the (B) set of `F` contains `e` (in
particular if `C_F ∩ H ⊇ e`), then
`F^T = θ J adj(M(d; 0) + κ M_0)` for some `θ > 0`, `κ ∈ R`. The pencil
`G_0 + κ G_1`, `G_0 = J adj(M(d; 0))`, `G_1 = J adj(M_0)`, satisfies
`det(G_0 + κG_1) = det M(d; 0) > 0` and `sym(G_1 M_0) = 0`. If `e` lies on a
ruling (`det M(d; 0) = 0`), no invertible `F` qualifies.

*Proof.* `t*` is in the (B) set and `q(t*) = 0`, so the lowering `τ` is 0
and `t* ∈ C_F`: `F^T a_0 = c b_0`, `c > 0`. For `|s|` small,
`t* + sd − τ(s) e_w ∈ C_F` with `0 ≤ τ(s) ≤ s^2 det M(d)`. Let
`X(s) = c b_0 b_0^T + sY − τ(s) Z ⪰ 0` with `Y = sym(F^T M(d))`,
`Z = sym(F^T E)`, and `u = Jb_0`. The inequality of `C_F` touching at `t*`
is indexed by `u` and is strictly kept (its tangency point `t*` has
`h = 1`), so `u^T Z u > 0`. From
`u^T X(s) u = s u^T Y u − τ(s) u^T Z u ≥ 0` for both signs of `s` we get
`u^T Y u = 0` and `τ ≡ 0`. Then `X(s)` is PSD with a zero
`(u, u)`-entry, so its `(b_0, u)`-entry `s Y_{b_0 u}` vanishes and
`Y = μ b_0 b_0^T`. Hence `sym(F^T(M(d) − (μ/c) M_0)) = 0`, i.e.
`F^T(M(d) + κM_0) = θ' J` with `κ = −μ/c`. Since
`det(M(d) + κM_0) = det M(d) + κ ∇q(t*)^T d + κ^2 q(t*) = det M(d)`, the
matrix is invertible when `det M(d) > 0` and `F^T = θ' J (M(d) + κM_0)^{-1}`
`= (θ'/det M(d)) J adj(M(d) + κM_0)`; the sign is fixed by `c > 0`. If
`det M(d) = 0`, `θ' J` would be singular, so `θ' = 0` and `F` is singular.
∎

So a tangent edge leaves a **one-parameter pencil** of candidate orbit sets
(the quadric cones with apex on the line of `e`, and the cylinder
`κ = 0`); each remaining vertex `v` restricts `κ` to the set
`K_A(v) = {κ : sym((G_0 + κG_1) M(v)) ⪰ 0}` (an interval) for (A), or
`K_B(v) ⊇ K_A(v)` for (B). If the sets of `s̄` and the other vertices do not
intersect, no set of the family contains `T*`.

### 8.5 The obstruction

**Theorem 14.** Let `S = {w ≤ xy}`, `s̄ = (−9/2, 0, 3/2)`, and rays
`p_j = v_j − s̄` to `v_1 = (−1, −6, 18)`, `v_2 = (−5, 6, −18)`,
`v_3 = (0, 5/2, 5/2)`, with `w = (1, 1, 1)`. Then:

1. `z_K = 1`, attained only at `t* = (−3, 0, 0) = (v_1 + v_2)/2`, which lies
   in the relative interior of the tangent edge `[v_1, v_2]`
   (`d = (4, −12, 36)`, `det M(d) = 48`).
2. No set of family (A) or family (B) contains `T* = conv{s̄, v_1, v_2, v_3}`.
3. `z_A ≤ z_B < z_K`. Numerically `z_A = 0.97539` (certified lower bound
   from an explicit `F`; bisection upper value agrees to `10^-10`) and the
   best (B) value found is `0.97539`.
4. The same holds for all corners in a neighbourhood of this one.

*Proof.* (1) On `T*`, `q = w − xy` is a quadratic in the barycentric
coordinates; enumerating the 15 faces and their stationary points in exact
rational arithmetic shows `min_{T*} q = 0`, attained only at `t*`. So
`T* ∩ int S = ∅`, `q > 0` on `T* \ {t*}`, and `t*` has cost 1.

(2) By Lemma 13, a candidate `F` is `θ(G_0 + κG_1)^T` with the sign fixed
by the lemma's criterion `F^T a_0 = c b_0`, `c > 0`: here `M(t*) = a_0 b_0^T`
with `a_0 = (x_0, 1)`, `b_0 = (y_0, 1)`, `G_1 a_0 = 0` and `G_0 a_0 = 4 b_0`,
so `θ > 0` (the script now checks exactly this; an earlier version chose
the sign by `tr sym(G_0 M(t*))`, which gives the same answer here). Exact
computation (`code/certify_counterexample.py`, sympy):

- `K_A(s̄) = [12 − 8√2, 12 + 8√2]`, `K_A(v_1) = (−∞, 2]`,
  `K_A(v_2) = [−2, ∞)`, `K_A(v_3) = [−13/5 − 2√30/5, −13/5 + 2√30/5]`;
  `K_A(s̄) ∩ K_A(v_3) = ∅` (`−13/5 + 2√30/5 ≈ −0.409 < 0.686 ≈ 12 − 8√2`).
- For family (B), fix `u_s = (1 − √2/3, 1)` and
  `u_3 = (−3/10 + √30/60, 1)`. With `A_v(κ) = sym((G_0 + κG_1)M(v))` and
  `Z(κ) = sym((G_0 + κG_1)E)`:
  `u_s^T A_{s̄} u_s = (√2/2)(κ − κ_s)`, `κ_s = 12 − 8√2`, and
  `u_s^T Z u_s = −(1 − √2/3)κ + 44/3 − 8√2`, which is positive for
  `κ ≤ κ_s`. So for `κ < κ_s` and every `τ ≥ 0`,
  `u_s^T(A_{s̄} − τZ)u_s < 0`: `s̄` is in no (B) set of the pencil. Likewise
  `u_3^T A_{v_3} u_3 = −(√30/6)(κ − κ_3)` with `κ_3 = −13/5 + 2√30/5`, and
  `u_3^T Z u_3 = (3/10 − √30/60)κ + 59/50 − 3√30/25 > 0` for `κ ≥ κ_3`, so
  `v_3` is in no (B) set for `κ > κ_3`. Since `κ_3 < κ_s`, every `κ` is
  excluded.

(3) Suppose `z_B = z_K`. Take `F_n` with `‖F_n‖ = 1` and (B) sets containing
`T_{z_n}`, `z_n → 1`, with lowering parameters
`τ_{v,n} ∈ [0, q(v_n)]` at the vertices (bounded). Pass to limits
`F_n → F`, `τ_{v,n} → τ_v`. Then `sym(F^T M(v − τ_v e_w)) ⪰ 0` at the
vertices `v` of `T*`. If `det F > 0`, `T*` lies in the (B) set of `F`,
contradicting (2). If `F` has rank one, `F^T = qp^T`, the condition says
`M(s)^T p ∈ R_+ q`, which confines the lowered vertices to a plane `Σ`. The
lowered edge point below `t*` is a limit of points of S-free sets, hence
not in `int S`, so `τ_{v_1} = τ_{v_2} = 0` and `t* ∈ Σ`. If `Σ` is vertical,
`T* ⊆ Σ + R_+ e_w = Σ`, impossible. Otherwise `Σ = {w = ℓ(x, y)}` and the
Kuratowski limit of the (B) sets contains
`U = conv(lowered vertices) + R_+ e_w = {(x, y) ∈ proj T*, w ≥ ℓ(x, y)}`
and is S-free, so `ℓ ≥ xy` on `int proj T*`, with equality at `(x_0, y_0)`.
Since `(x_0, y_0) = (−3, 0)` is interior to `proj T*` (checked exactly),
`ℓ` is the tangent plane of `xy` there, and `ℓ − xy = −(x+3)y` is negative
nearby. Contradiction. The argument for (A) is the same with `τ ≡ 0`, and a
rank-one limit then puts `T*` in a plane.

(4) *Sketch, not verified in detail.* It suffices that, under small
perturbations of `(s̄, P, w)`, the minimizer stays unique and on the
tangent edge, and the certificates of (2) and the interior condition of (3)
persist. The first needs strict complementarity for ray 3 and second-order
nondegeneracy along the edge; both hold here exactly: the KKT multiplier of
ray 3 is `20/3 > 0` (with `σ = 2/3`, since `∇q(t*) = (0, 3, 1)` and
`P^T ∇q(t*) = (−3/2, −3/2, 17/2)`), and `det M(d) = 48 > 0`. The rest are
strict inequalities (`κ_3 < κ_s`, nonzero slopes, positive `u^T Z u` at
the endpoints, interior distance of `(x_0, y_0)`) in quantities that depend
continuously on the data near a nondegenerate minimizer. ∎

*A larger gap for family (A).* For `s̄ = (−1/2, 1/2, 1)`,
`v_1 = (1/2, −4, −1/2)`, `v_2 = (−10, 3, 24)`, `v_3 = (9/2, 1/2, 15/2)`,
`w = 1`, the same script proves `z_K = 1` at `t* = (−1, −3, 3)` and
`K_A(s̄) = [133/12 − 7√30/6, 133/12 + 7√30/6] ≈ [4.69, 17.47]` disjoint from
`K_A(v_3) ≈ [−1.67, 1.53]`, so `z_A < z_K`; numerically `z_A = 0.83477`.
The (B) certificate above does not apply here (and `(x_0, y_0)` is on the
boundary of `proj T*`); Nelder–Mead finds no (B) set better than `0.83477`.

*Remark 15 (what the obstruction means).*

- The scout's conjecture OQ1(a) ("orbit sufficiency" for signature
  `(2, 2)`) is false, both for the sliced orbit and for SCIP's maximal
  completions.
- Every maximal S-free set containing `conv(T* ∪ B(s̄, δ))` (which exists
  by Theorem 1(4)) is outside family (B). So Muñoz–Serrano's construction
  under all transformations and all `λ` does not produce all maximal
  quadratic-free sets for `S = {w ≤ xy} ⊂ R^3`, and the missing ones matter
  for cut strength. (That (B) misses *some* maximal sets is easier. The
  McCormick-type wedge `W = {x ≥ a, y ≤ b, w ≥ bx + ay − ab}` is S-free,
  since `bx + ay − ab − xy = (x − a)(b − y) > 0` inside, and maximal: a
  point with `x < a` (or `y > b`) added to `W` puts points of `int S` near the
  ruling `{x = a, y → −∞}` (or `{y = b, x → ∞}`) into the interior of the
  hull; and inside the quadrant the lower boundary `g` of a larger S-free
  set would satisfy `xy ≤ g ≤ ` plane with equality on both boundary rays,
  so `plane − g` is concave, nonnegative, `O(ε^2)` along every ray from
  `(a, b)`, hence zero. This maximality argument is a sketch. `W` is
  polyhedral, while (B) sets have curved boundaries, since `C_F ∩ H` is an
  affine image of the 2×2 PSD cone or a cylinder over a conic section.)
- The mechanism is local: a tangent edge forces an orbit set to contain a
  line through `t*` in its boundary, which fixes the set up to one
  parameter. Sets whose boundary is flat near `t*` (for example polyhedral
  sets, characterized by MPS Theorem 1.3 through isometric covers, with a
  sharp ridge along `e`) are not subject to it.
- *Ruling ties.* If `T*` touches `S` at two points on a common ruling
  (`x_1 = x_2` or `y_1 = y_2`), then `F^T a ∈ R_+ b_1 ∩ R_+ b_2 = {0}`, so no
  invertible `F` works in (A) or (B). This happens only for ties in `w`, but
  shows the obstruction also in the simplest configuration.

### 8.6 How often, and how large

- *Random corners* (`code/explore_supp2.py`, `code/screen2.py`): of 25
  random bilinear corners with `N = 3` whose minimizer has support 2, family
  (A) attained `z_K` in 22; the three failures had `z_A/z_K = 0.99992`,
  `0.8632` and `0.99905`, and family (B) attained `z_K` in two of them
  (`0.8632` remained). All failures had empty `K_A`-intersections, as Lemma
  13 predicts. On support-1 corners (the majority) the orbit attained `z_K`
  in every tested case (20 random corners here, after rescaling costs so
  that `z_K = 1`; consistent with the scout's E12c/d).
- *Adversarial search* (`code/adversarial_ratio.py`: Nelder–Mead over
  11-parameter tangent-edge configurations with `N = 3`, `w = 1`, exact
  `z_K` and LMI bisection; `code/verify_adversarial.py`,
  `code/verify_adv2.py`: SCIP, Clarabel and SCS cross-checks). The search
  drives one ray towards grazing `∂S`; instances within relative
  discriminant `10^-8` of grazing are numerically ill-posed and excluded
  (Section 9.1). Among verified instances:
  - a ray missing `∂S` by relative discriminant `−6.6·10^-7`:
    `z_K = 1` (SCIP `0.9999992`), `z_A = 0.6106` (Clarabel and SCS agree
    at `0.60` feasible / `0.62` infeasible), best (B) found `0.6131`;
  - with every ray at relative discriminant at least `10^-2` away from
    grazing: `z_K = 1` (SCIP agrees), `z_A = 0.6224` (both solvers), best
    (B) found `0.7078`;
  - with rays at least `10^-2` from grazing and a vertex violation
    `q(s̄)/max|P|^2 ≈ 9·10^-4`: `z_A = 0.4526` (Clarabel and SCS agree),
    best (B) found `0.4526`. Two of its three rays sit exactly on the
    imposed margin (relative discriminants `−0.0100`, `−0.0101`), so this
    ratio is set by the margin: read "non-degenerate" as "rays 1% from
    grazing";
  - with rays at least `10^-2` from grazing but the vertex almost on `∂S`
    (`q(s̄)/max|P|^2 ≈ 10^-7`): `z_K = 1` (SCIP `0.999998`), and Clarabel
    finds an `F` whose exact bound is `0.0280` and reports infeasibility from
    `0.029` on (SCS is unreliable on this instance, returning "feasible"
    points with negative eigenvalues); best (B) found `0.031`.

  So the single-cut ratio of family (A) can be far below 1 on corners whose
  rays stay 1% from grazing, and the last instance suggests that it tends
  to 0 as the LP vertex approaches `∂S`, i.e. that no constant
  approximation factor holds for single cuts. This is numerical evidence
  only. For family (B) the values quoted are heuristic lower bounds on `z_B`
  (Nelder–Mead), and (B)-strictness on these instances rests on a `κ`-grid,
  not a proof. The review reproduced `z_K` and `z_A` for the 0.4526 and
  0.6224 instances with its own code.

**Proposition 16 (support one is not enough).** *(Replaces the former
Conjecture 16, which the review refuted numerically; certified here.)* Let
`S = {w ≤ xy}`, `s̄ = (−2, 3, 2)`, and rays `p_j = v_j − s̄` to
`v_1 = t* = (0, 0, 0)`, `v_2 = (6, −2, 1/4)`, `v_3 = (1, −5/2, 1/2)`, with
`w = (1, 1, 1)`. Then:

1. `z_K = 1`, attained only at `t* = v_1` (support one). Every edge of `T*`
   at `t*` is transversal to `∂S`: `∇q(t*) = (0, 0, 1)` and
   `∇q(t*)^T(v − t*) = 2, 1/4, 1/2` for `v = s̄, v_2, v_3`. The KKT
   multipliers of rays 2 and 3 are `1/8` and `1/4` (strict complementarity).
2. No nonzero `F` satisfies `sym(F^T M(v)) ⪰ 0` at all four vertices of
   `T*`. Hence `z_A < z_K`.

Numerically `z_A = 0.98385` (Clarabel and SCS are both infeasible at
`0.984`; Clarabel's `F` at `0.980` has exact bound `0.98000`, and bisection
gives the certified lower bound `0.983847`), the best (B) value found is
`0.98385`, and SCIP's own set gives only `0.318`.

*Proof* (`code/certify_supp1.py`, exact arithmetic). (1) Face enumeration
of `min_{T*} q` as in Theorem 14; the multipliers come from
`w + σ P^T ∇q(t*) − ν = 0` with `σ = 1/2`. (2) There are rational
positive definite matrices `Y_v` with `Σ_v M(v) Y_v = 0` exactly (found by an
SDP whose optimal minimum eigenvalue is `1.7·10^-3`, then rounded and
projected exactly onto the four linear equations; positive definiteness
checked exactly). For every `F`,
`Σ_v ⟨sym(F^T M(v)), Y_v⟩ = tr(F^T Σ_v M(v) Y_v) = 0`, so if all four
matrices are PSD they are all zero, and the linear system
`sym(F^T M(v)) = 0` (all `v`) has only `F = 0`. The compactness argument of
Theorem 14(3) (a normalized limit `F ≠ 0` would satisfy the closed
conditions) gives `z_A < 1`. ∎

A hand-checkable integer certificate (from the recheck, verified here):
`Y_{s̄} = [[92, −75], [−75, 64]]`, `Y_{v_1} = [[726, 89], [89, 12]]`,
`Y_{v_2} = [[96, −64], [−64, 45]]`, `Y_{v_3} = [[20, 16], [16, 16]]`; all have
positive `(1,1)` entry and determinant (263, 791, 224, 64), and the products
`M(v) Y_v` are `[[334, −278], [201, −161]]`, `[[0, 0], [89, 12]]`,
`[[−360, 254], [−256, 173]]`, `[[26, 24], [−34, −24]]`, which sum to zero. The
recheck also brackets `0.9838 ≤ z_A ≤ 0.9839` exactly.

*Why.* In the proof of Lemma 13, a one-sided or nearly tangent edge at the
contact point gives only an inequality `u^T Y u ≥ 0` instead of an
equality, but the edge must still lie in the orbit set to second order.
That curvature condition can conflict with containing `s̄` and the other
vertices. The review found the effect numerically by tilting a tangent edge
outward: cosines `10^-3`, `10^-2`, `3·10^-2`, `10^-1` with `∇q(t*)` give
`z_A = 0.9974`, `0.99973`, `0.999992`, `1` (`../reviews/sfree/rv_conj16_tilt*.log`).
But the angle at `t*` is not the only factor. In Proposition 16 the far face
also nearly touches `∂S`: on the edge `[s̄, v_2]`, `q` falls to
`31/2560 ≈ 0.012` at `s̄ + (143/320)(v_2 − s̄)` (checked exactly). In the
recheck's variants of this instance (`../reviews/sfree-recheck/prop16_variants.log`;
three rows reproduced in `logs/prop16_variants_spotcheck.log`):

| `v_2` | edge cosine at `t*` | min `q` on far face | `z_A` |
|---|---|---|---|
| `(6, −2, 1/4)` (Prop. 16) | 0.0395 | 0.012 | 0.98385 |
| `(6, −2, 1)` | 0.156 | 0.34 | 0.99923 |
| `(6, −2, 2)` | 0.30 | 0.78 | 1 |
| `(6, −4, 1/4)` | 0.035 | 0.95 | 1 |
| `(8, −3, 1/4)` | 0.029 | 0.025 | 0.98765 |

So a cosine of 0.156 still fails while 0.035 succeeds: the gap depends on how
close the whole far face comes to `∂S`, not on the angle at `t*` alone. A
search over rational support-one corners with nearly tangent edges
(`code/search_supp1_cex.py 1 6000`) found 6 with `z_A < 0.9995`
(`logs/search_supp1_cex.log`).

*Open question* (replacing the conjecture). Which nondegeneracy condition
on the optimal simplex (in these examples, a lower bound on `q` over the far
face away from `t*` together with the angles at `t*`) makes the orbit attain
`z_K`? In the family above, an angle threshold alone would have to exceed a
cosine of about 0.16. My earlier adversarial search (`adversarial_supp1.py`,
margin `10^-2`) found no support-one failure because it did not target
these configurations; it is not evidence for any such condition.

## 9. Computations on McCormick relaxations

All values below are targeted local checks (Section 11), not CI results.

### 9.1 Validation and corrected errors

`code/validate_corner.py` compares `z_K` from `code/core.py` (supports of
size 1 and 2 exactly, size 3 by the generic KKT formula) with SCIP global
solves: 77 random instances (bilinear, general `k = 2, 3`, `N ≤ 6`), no
mismatch, maximum relative difference `2.8·10^-6`.

Errors found and fixed during this work, all in degenerate
cases:

- the first version of `two_ray` dropped double roots of the stationarity
  equation (floating-point imaginary parts `~10^-8`). It overestimated `z_K`
  on rational instances with `b' = 0` and produced spurious "orbit
  failures"; all rational screens were rerun after the fix;
- `one_ray` treated an exactly-zero discriminant computed as `−10^-16` as a
  miss; it now treats relative discriminants above `−10^-12` as tangential
  contact. Relatedly, the first adversarial search drove a ray to within
  relative discriminant `10^-8`–`10^-11` of grazing `∂S` in four of six
  restarts. There the exact answer is a miss (`z_K = 1`), but SCIP's
  feasibility tolerance reports the near-touch (`z_K ≈ 0.39`–`0.62`), so
  `z_K` is numerically ill-posed; those instances are excluded, and the
  second search imposes a margin `10^-2`.
- a later tolerance change in `two_ray` (relative to the sum of the
  polynomial coefficients) was too loose for badly scaled costs
  (`w_1 = 10^-8`) and was reverted; all reported runs were repeated or
  checked with the final code.

Every instance quoted as a counterexample was re-checked: `z_K` against
SCIP, the orbit value with two SDP solvers (Clarabel, SCS) where relevant,
and the two rational instances in exact arithmetic.

### 9.2 One cut at an LP vertex

Generator of the scout's E3: random bilinear programs with McCormick
envelopes and a few random rows, HiGHS optimal basis, the most violated
term `w_e = x_i x_j`, reference `z_1 = min{c^T x : x ∈ P, w_e = x_i x_j}`
(SCIP). Fractions of the single-constraint gap `z_1 − z_LP`:

| Rule | 4 vars, 4 products (n = 47) | 6 vars, 8 products (n = 73) |
|---|---|---|
| Corner increment `z_C/gap`, SCIP's set | mean 0.700, median 0.839 | mean 0.591, median 0.634 |
| Corner increment, best orbit set (= corner bound) | mean 0.755, median 1.000 | mean 0.648, median 0.795 |
| LP re-solve with the cut, SCIP's set | mean 0.895, median 0.957 | mean 0.870, median 0.934 |
| LP re-solve, best orbit set | mean 0.929, median 1.000 | mean 0.907, median 0.999 |
| LP re-solve, corner-optimal cut `w^T λ ≥ z_K` | mean 0.755, median 1.000 | mean 0.648, median 0.795 |

- The best orbit set attained `z_K` in all 120 LP corners up to the
  bisection resolution (worst ratio `0.9999695`). A single `0.999` in the first 6×8 run was a scaling artifact of
  the bisection, gone after normalizing by `z_K`
  (`exp_mccormick_12_big_final.json`). SCIP's set reached below `0.9 z_K` in
  26 of 120 corners and below `0.5 z_K` in 3.
- Re-solving the LP matters. The corner-optimal cut is parallel to the
  objective and gains exactly `z_K`; SCIP's cut and the orbit cut are
  tilted and gain much more from the other LP rows. The objective-parallel
  cut was worse than SCIP's cut by more than 0.01 of the gap in 58 of 120
  instances. So "bound-optimal on the corner" is the right criterion for
  choosing *among maximal sets that attain it*, not a reason to use the
  bound cut itself.
- The orbit cut beat SCIP's cut by more than 0.01 of the gap in 60 of 120
  instances and lost by more than 0.01 in 26; mean gain 0.03–0.04.

### 9.3 Prototype separator (root cutting loop)

`code/exp_loop.py`: each round solves the LP, takes the optimal basis, and
adds one cut per violated bilinear term, with the set chosen by the rule.
Fraction of the root gap `z_bil − z_LP` closed (mean over instances;
`z_bil` from SCIP):

| Rule | 4×4, n = 12: rounds 1 / 2 / 3 / 8 | cuts | 6×8, n = 10: rounds 1 / 2 / 3 / 10 | cuts |
|---|---|---|---|---|
| SCIP's set | 0.828 / 0.940 / 0.963 / 1.000 | 7.2 | 0.686 / 0.820 / 0.861 / 0.931 | 32.6 |
| best orbit set | 0.863 / 0.967 / 0.998 / 1.000 | 5.2 | 0.701 / 0.796 / 0.832 / 0.887 | 33.2 |
| its completion (B) | 0.863 / 0.967 / 0.998 / 1.000 | 5.2 | 0.701 / 0.796 / 0.832 / 0.881 | 33.3 |
| corner-optimal cut | 0.722 / 0.796 / 0.796 / 0.796 | 16.1 | 0.584 / 0.584 / 0.584 / 0.584 | 42.2 |

- On the small instances the orbit rule closes the gap faster (8 of 12
  instances better by more than 0.01 after round 1, 1 worse) with fewer cuts.
- On the 6×8 instances it wins the first round on average but loses later:
  after 10 rounds SCIP's rule is ahead by more than 0.01 in 5 of 10
  instances and behind in none. Choosing the bound-optimal set for the
  *current* objective direction in every round is therefore not a better
  multi-round strategy in general; n = 10 is small, and I did not
  investigate the cause.
- No LP re-solve failed in the final runs. (An earlier version returned an
  infinite coefficient when the SDP solver put `s̄` on the boundary of
  `C_F`; fixed by shifting `F` by a small multiple of `M(s̄)^{-T}`, which
  keeps it in the orbit.)

The objective-parallel corner cut stalls after one round: the next vertex is
dual degenerate (zero reduced costs along the cut face), so `z_K = 0` there.
The completion (B) of the chosen orbit set rarely matters: in a separate
check on 42 corners of the 6×8 generator it lengthened 11 of 588 steps (in
4 corners), and `e_w` was never a recession direction of the chosen `C_F`.
Cut density is the same for all rules (the cuts are dense, as in SCIP).

### 9.4 What the numbers say about OQ1

- On LP-derived corners the transformation (orbit) search is essentially
  exact: it attained `z_K` in all 120 corners.
- On random corners, 3 of 25 tangent-edge instances fail, one by 13.7%.
- Adversarially the gap is large (Section 8.6): single-cut ratios down to
  0.45–0.62 on corners with a clear violation, and 0.028 when the LP vertex
  violates the constraint only slightly.
- For one cut, the orbit bisection is a strict improvement over SCIP's
  fixed set (it attains the corner bound in all 120 LP corners and
  gains 0.03–0.04 of the gap on average after re-solving the LP). Over
  several rounds the evidence is mixed (Section 9.3), so I would not claim a
  solver-level benefit without MINLPLib/QPLIB experiments inside SCIP.

## 10. Literature and novelty

### 10.1 Sources examined

| Source | What was checked |
|---|---|
| Muñoz–Serrano, Math. Program. 192 (2022), arXiv:1911.12341 (`../scouting/s-free-intersection-cuts/sources/1911.plain.txt`) | §3 (the set `C_λ`, Theorem 7), §4 opening (Remark 5, reduction with `h`), §6 (transformations, Example 9), §7 (future work; the 3-dimension conjecture) |
| Muñoz–Paat–Serrano, Math. Program. 210 (2025), arXiv:2211.05185 | §1 (Theorems 1.1–1.4, Corollary 1.1), §8 (future work) |
| Muñoz–Paat–Serrano, arXiv:2605.30602 (May 2026) | §1 (Theorems 1–5), §2.1 (reduction), Lemmas 1–3, Remark 1, end of §5–6, references |
| Chmiela–Muñoz–Serrano, ZIB Report 20-29 (Math. Program. 197, 2023) | §3 (Cases 1–4, Remarks 2–3, Lemma 3, implied quadratics) |
| SCIP 10 via PySCIPOpt 6.2.1 | `nlhdlr/quadratic/*` parameter names (checked); I did not extract SCIP's own cuts |
| Local KB `renegar1992-on-the-computational-complexity-and` | used for Theorem 5(1) (fixed number of variables) |
| Local KB `bienstock2020-outer-product-free-sets-for`, `kazachkov2025-monoidal-strengthening-of-simple-v`, `andersen2013-intersection-cuts-for-mixed-integer` | index entries and summaries only |
| arXiv abstracts: 1705.02015 (Averkov–Basu–Paat), 1901.02112 (Towle–Luedtke), 2302.14020 (Xu–Liberti) | abstracts via the arXiv API |
| arXiv API searches (2026-09-28) | `abs:"quadratic-free"`, `abs:"S-free" AND abs:quadratic`, `abs:"maximal S-free"`, `abs:"intersection cut" AND abs:bilinear`, `abs:"intersection cuts" AND abs:"quadratically constrained"`, `abs:"outer-product-free"`, `abs:"intersection cut" AND abs:"strongest"`, `abs:"cut selection" AND abs:"intersection cuts"`, `abs:"quadratic intersection cuts"`, `abs:"concavity cut"`, `abs:"intersection cuts" AND abs:"reverse convex"`, `au:Averkov AND au:Paat` |
| Semantic Scholar citation lists | papers citing arXiv:2211.05185 (only 2605.30602) and arXiv:1911.12341 (16 titles; none about choosing among maximal sets); citations of Chmiela et al. not retrieved (API rate limit) |

Not re-read (cited from memory or through the papers above): Balas (1971),
Tuy (1964), Conforti–Cornuéjols–Zambelli, *Integer Programming* (2014)
Ch. 6, Conforti–Cornuéjols–Daniilidis–Lemaréchal–Malick (MOR 2015),
Cornuéjols–Wolsey–Yıldız (Math. Program. 2015), Motzkin–Straus (1965),
Sturm–Zhang (MOR 2003), Porembski (JOGO 2001, 2004), Chmiela–Muñoz–Serrano
monoidal strengthening (Math. Program. B 210, 2025; abstract only, via the
scout). The shared web-search budget was exhausted before this workstream
started, so no general web search was possible. An unsuccessful search does
not establish novelty.

### 10.2 Relation to prior work and novelty assessment

- *Theorem 1* (1)–(3), (5) and *Lemma 3* are the finite-ray, closed-`S`
  forms of classical facts: intersection cuts from S-free sets suffice for
  the corner relaxation (Balas; CCDLM 2015; CWY 2015), and corner-polyhedron
  vertices use at most (number of rows) rays. The attainment criterion (4)
  and the examples of Proposition 2 are elementary; I did not find them
  stated.
- *Theorem 4* (the inertia bound `ρ(q)`) is, as far as I found, new as a
  statement about corner relaxations with one quadratic constraint, but its
  technique is standard: second-order necessary conditions plus inertia
  counting, as in the support (sparsity) bounds for local minimizers of
  standard quadratic programs (Bomze and coauthors; Chen–Peng–Zhang). Those
  references are cited from the reviewer's memory and were not re-read. The
  reverse-convex statement (the Tuy cut attains `z_K`) is classical and
  follows from Theorem 1 plus uniqueness of the maximal S-free set (Section
  3); the bilinear case of Theorem 4 is what makes Theorem 11 simple.
- *Theorem 5*: polynomiality for fixed dimension is routine given Lemma 3;
  the hardness is the standard-quadratic-program reduction
  (Motzkin–Straus). The content is the statement about best intersection
  cuts and the parameter `ρ`.
- *Proposition 6* and Remark 7 come from the scout and are checked here;
  they answer negatively whether SCIP's fixed `λ` is a safe default.
- *Theorem 8* combines MPS's characterizations (2025, 2026 Lemma 1) with the
  2-transitivity of the Möbius group. It answers which sets the
  transformations reach for signatures `(n, 1)` and `(1, m)` (all
  indefinite 2-variable quadratics), *when `λ` is free*; with Muñoz–Serrano's
  point rule the reachable family is smaller and not exact (Section 6.1). I
  found no statement of it.
- *Section 8*: the explicit parametrization of the orbit as
  `{sym(F^T M) ⪰ 0}`, the identification of SCIP's Case-4 completion with
  the upward closure (via the 2×2 rank-one decomposition), the quasiconvex
  best-orbit computation, the tangent-edge rigidity lemma and the certified
  obstruction are, as far as I found, new. The homogeneous sets `C_F`
  are related to the outer-product-free sets of Bienstock–Chen–Muñoz (Math.
  Program. 183, 2020), which Chmiela et al. identify with their sets for the
  implied minor equations `X_{i1j1}X_{i2j2} = X_{i1j2}X_{i2j1}` (their Case
  1, a homogeneous form of signature `(2, 2)`); whether the tangent-edge
  obstruction also occurs there was not checked.
- *Averkov–Basu–Paat* (SIOPT 2018) classify families of lattice-free sets
  that approximate the corner polyhedron up to a constant factor by their
  *closures*. The results here concern the best *single* cut. The scout's
  OQ1(a) states that single-cut exactness for all `w` is "equivalent" to the
  family's closure being the corner-hull dominant; only one direction holds
  (single-cut exactness for all `w` implies closure exactness, by the
  argument of Theorem 1(5)). Whether the closure of the orbit family is
  exact for bilinear constraints is open.
- *Monoidal strengthening* (Chmiela–Muñoz–Serrano 2025) acts on integer
  nonbasic variables and is complementary; not examined.
- *Deeper cuts for concave and bilinear programs* are an older line of work
  on the same question (which convex set, which cut) in special cases:
  Glover, "Convexity cuts and cut search" (Oper. Res. 1973); Konno, "A
  cutting plane algorithm for solving bilinear programs" (Math. Program.
  1976); Sherali–Shetty, polar and disjunctive face cuts for bilinear
  programs (Math. Program. 1980); Porembski, "How to extend the concept of
  convexity cuts to derive deeper cutting planes" (JOGO 1999); and
  Balas–Margot, generalized intersection cuts (Math. Program. 2013), which
  optimize the cut over a relaxation. These are cited from the reviewer's
  memory and were not re-read by me; they do not concern maximal
  quadratic-free sets or the orbit results, but they are the precedents for
  selecting deeper intersection cuts.
- *Risk.* The MPS group calls the characterization "a new avenue" for cut
  generation; concurrent work on set selection is plausible.

## 11. Reproducibility

Environment: Python 3.13, numpy 2.5.1, scipy 1.18.0, cvxpy 1.9.3 with
Clarabel 0.11.1 and SCS 3.3.1, sympy 1.14.0, highspy, PySCIPOpt 6.2.1 (SCIP
10). All commands run from `research-20260928b/sfree/code/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`. These are targeted checks only;
no project-wide checks were run and CI was not consulted.

| Command | Checks | Output (in `../logs/`) |
|---|---|---|
| `python3 verify_props.py` | Prop. 2, 6, 9 and the Motzkin–Straus formula (exact / high precision) | `verify_props.log` (ALL PASS) |
| `python3 validate_corner.py 0 90` | `z_K` vs SCIP, 77 instances | `validate_corner.log` (0 mismatches, max rel. diff `2.8e-6`) |
| `python3 support_stats.py 0` | support sizes of bilinear minimizers (888 corners) | `support_stats.log` (749 / 139 / 0) |
| `python3 orbit_n1.py 0 40` | Theorem 8 on 24 two-variable corners | `orbit_n1.log` (ratio `1.00000000`) |
| `python3 remark7.py` | Remark 7 table | `remark7.log` |
| `python3 test_B_identity.py` | Lemma 10(4): MPS completion = upward closure | `test_B_identity.log` (9998 / 10000) |
| `python3 certify_counterexample.py` | Theorem 14, exact arithmetic | `certify_8459.log` (ALL PASS) |
| `python3 certify_counterexample.py '{"sbar":["-1/2","1/2","1"],"v1":["1/2","-4","-1/2"],"v2":["-10","3","24"],"v3":["9/2","1/2","15/2"],"t0":["-1","-3","3"]}'` | second rational instance, family (A) | `certify_bigA.log` ((1)–(4A) pass; (4), (5) fail as expected) |
| `python3 explore_supp2.py 0 3 25`; `python3 dump_supp2.py`; `python3 screen2.py` | random tangent-edge corners, (A) and (B) | `explore_supp2.log`, `supp2_instances.json`, `screen2_supp2.log` |
| `python3 explore_orbit.py 1 3 20`; `python3 recheck_supp1.py` | random (support-1) corners; rescaled recheck of the one near-miss | console; `recheck_supp1.log` |
| `python3 rational_kappa.py`; `python3 rational_kappa_B.py`; `python3 screen_rational2.py` | kappa-sets of rational instances; numeric `z_A`, `z_B` | `rational_kappa.log`, `rational_kappa_B.log`, `screen_rational2.log` |
| `python3 find_rational_cex.py`; `python3 search_big_gap.py S 40000` (S = 1, 2, 3; stopped early) | rational tangent-edge searches (the log is the rerun after the `two_ray` fix, stopped early; exact kappa-sets recomputed in `rational_kappa.log`) | `find_rational_cex.log`, `search_big_gap_*.jsonl` |
| `python3 adversarial_ratio.py 7 10` (old code; crashed after 6 restarts); `python3 verify_adversarial.py …_7.log`; `python3 verify_adv2.py ../logs/adversarial_ratio_7.log 1,5` | adversarial search; SCIP and two-solver checks | `adversarial_ratio_7.log`, `verify_adv_7.log` |
| `python3 adversarial_ratio.py 8 10 0.01` (stopped after 5 restarts); `python3 verify_adv2.py ../logs/adversarial_ratio_8_margin.log 1,2,3,4`; `python3 inspect_adv3.py` | adversarial search with non-degeneracy margin; checks | `adversarial_ratio_8_margin.log`, `verify_adv_8_margin.log`, `inspect_adv3.log`, `adversarial_summary.log` |
| `python3 adversarial_supp1.py 3 8 0.01` | support-one stress test (did not target nearly tangent edges) | `adversarial_supp1.log` (all 8 restarts: ratio 1) |
| `python3 search_supp1_cex.py 1 6000` | rational support-one corners with nearly tangent edges | `search_supp1_cex.log` (6 with `z_A < 0.9995`) |
| `python3 certify_supp1.py` | Proposition 16, exact certificate | `certify_supp1.log` (ALL PASS) |
| `python3 supp1_numeric.py` (run inline with identical code) | Proposition 16 numerics: SCIP `z_K`, SCIP's set, two SDP solvers, (B) | `supp1_cex_numeric.log` |
| `python3 point_rule_check.py 0 40`; `python3 point_rule_crosscheck.py` (run inline with identical code); `python3 point_rule_refine.py` | Section 6.1: point rule vs full orbit | `point_rule_check.log`, `point_rule_crosscheck.log`, `point_rule_refine.log` |
| `python3 ms_asymptote_check.py` | Section 6.1: upper bound for Muñoz–Serrano's full construction (point rule) | `ms_asymptote_check.log` (13 misses remain; max 0.966934) |
| `python3 prop16_integer_cert.py` | Proposition 16: integer certificate and far-face near-contact `31/2560` | `prop16_integer_cert.log` (ALL PASS) |
| inline variant spot check | Proposition 16 variants (three rows of the recheck's table) | `prop16_variants_spotcheck.log` |
| `python3 exp_mccormick.py 11 150 ../logs/exp_mccormick_11.json` (rerun with final code: `…_11_final.json`, identical) | one cut, 4×4 instances | n = 47 |
| `python3 exp_mccormick.py 12 200 ../logs/exp_mccormick_12_big.json 6 8 4` (rerun with final code: `…_12_big_final.json`, same up to the orbit bisection resolution) | one cut, 6×8 instances | n = 73 |
| `python3 check_B_steps.py` | effect of the completion (B) on step lengths | `check_B_steps.log` |
| `python3 exp_loop.py 21 30 8 ../logs/exp_loop_small.json` | loop, 4×4 | n = 12 |
| `python3 exp_loop.py 22 30 10 ../logs/exp_loop_big.json 6 8 4` | loop, 6×8 | n = 10 (earlier crashed attempts: `exp_loop_big_crashed*.log`) |

`code/scout_sfree.py` is the scout's implementation of the
Chmiela–Muñoz–Serrano sets (`ms_set`) and of `corner_bound_scip`; "SCIP's
set" in this note means that reimplementation with the default `λ`, not
cuts extracted from SCIP.

## 12. Revision after review

The independent review [`../reviews/sfree-review.md`](../reviews/sfree-review.md)
(scripts in `../reviews/sfree/`) confirmed Theorems 1, 4, 5, 11, Lemmas
3, 10, 13, Propositions 2, 6, 9, 12, Remark 7, and re-certified Theorem
14(1)–(3) in exact arithmetic with its own code. It found one false claim,
several overstatements and some missing references. I re-derived each point
before changing the note.

| # | Review finding | Re-derivation here | Change |
|---|---|---|---|
| 1 | Conjecture 16 numerically false (support-one corners with a nearly tangent edge, `z_A ≈ 0.9974`) | Built my own rational instance and **certified** `z_A < z_K` exactly with a positive definite dual certificate (`certify_supp1.py`); numerics: `z_A = 0.98385`, SCIP's set `0.318` | Conjecture withdrawn; Proposition 16 added; open question restated with a transversality condition; `adversarial_supp1.py` described as not targeting this case |
| 2 | Theorem 8 glosses overclaim: with the point rule `λ = x̂(Ts̄)/‖x̂(Ts̄)‖` the family is one-parameter and misses `z_K` (2 of 24) | Derived the span property and the parametrization; `point_rule_check.py`: plain point-rule sets miss `z_K` in 13 of the 36 Case-2 corners with finite `z_K` (down to 0.119), full orbit 36 of 36. Found a further caveat: Muñoz–Serrano's §5.2 enlarges members with a wrong-side tangency point (settled in the second round below) | Theorem 8(3), the Summary, §6 consequences and §10 now say "`λ` free"; new §6.1 |
| 2′ | The `h ≠ 0` step cited a remark stating only the converse | Wrote out the affine bijection `H' → R^{n+m} × h^⊥` and the lineality lemma | Proof of Theorem 8(3) completed; the "not re-derived" caveat removed |
| 3 | `ρ ≤ 2` for 2-variable quadratics false; Tuy optimality does not need Theorem 4 | `q = x^2 − 1`: `n_+ = n_0 = 1`, `b = 0`, so `ρ = 3`; the unique maximal S-free set contains every S-free set, so Theorem 1 gives `z_{C*} = z_K` | §3 corollaries and §10.2 corrected |
| 4 | The pencil sign was chosen by a trace heuristic; Theorem 14(4) is a sketch | `G_1 a_0 = 0` and `G_0 a_0 = c_0 b_0` with `c_0 = 4` (Theorem 14) and `21/2` (second instance, with my scaling of `d`); the scripts now use this criterion and give identical results; the KKT multiplier `20/3` of ray 3 is now checked exactly | `certify_counterexample.py`, `bilinear.kappa_pencil` changed; Theorem 14(4) labelled a sketch with its conditions |
| 5 | The 0.45 instance sits on the 1% margin; "(both families) verified" too strong | Confirmed from `verify_adv_8_margin.log` (relative discriminants `−0.0100`, `−0.0101`) | §8.6 and the Summary say "rays 1% from grazing"; (B) values called heuristic lower bounds |
| 6 | Older deeper-cut work not cited; Theorem 4's technique is standard | Not re-read (web-search budget exhausted); added as cited from the reviewer's memory | §10.2 |
| — | Minor: strict LMI at `s̄` forces `det F > 0`; "every *indefinite* quadratic"; worst orbit/`z_K` is `0.9999695`; the wedge maximality is a sketch | Checked (`det(F^T M(s̄)) > 0` and `det M(s̄) = q(s̄) > 0`) | Proposition 12, §6, §9.2, Remark 15 |

What the revision does not change: the counterexample of Theorem 14, the
computations of §9 (the review recomputed all statistics from the JSON
records), and Theorems 1, 4, 5, 11.

Commands rerun or added for the revision (all from `sfree/code/`, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`; targeted checks only, no
project-wide checks, CI not consulted):

- `python3 certify_counterexample.py` and the second-instance call
  (pencil sign by `c > 0`, KKT check added): `logs/certify_8459.log` ALL
  PASS (`c_0 = 4`, `σ = 2/3`, `ν_3 = 20/3`); `logs/certify_bigA.log`
  (A)-certificate passes (`c_0 = 21/2`);
- `python3 rational_kappa.py`: kappa-sets unchanged after the sign change
  (`diff` against the previous log is empty);
- `python3 search_supp1_cex.py 1 6000`, `python3 certify_supp1.py`,
  `python3 supp1_numeric.py` (`logs/supp1_cex_numeric.log`);
- `python3 orbit_n1.py 0 40` (main guard added; same result, ratio
  `1.00000000` on 24 corners);
- `python3 point_rule_check.py 0 40`, `python3 point_rule_crosscheck.py`
  (`logs/point_rule_crosscheck.log`), `python3 point_rule_refine.py`.

### Second round: recheck of the revision

A fresh recheck [`../reviews/sfree-recheck.md`](../reviews/sfree-recheck.md)
(scripts in `../reviews/sfree-recheck/`) confirmed Proposition 16 (with an
independent proof of part (1), a hand-checkable integer certificate and the
exact bracket `0.9838 ≤ z_A ≤ 0.9839`), the one-parameter claim of §6.1
(two parametrizations agree to `6·10^-8`) and the `h ≠ 0` step of Theorem 8.
It requested five changes, each re-derived here:

| # | Recheck finding | Re-derivation here | Change |
|---|---|---|---|
| 1 | 4 of the 40 generated corners of §6.1 have `z_K = ∞` and were skipped silently: the counts are 13 of 36 and all 36 | `logs/point_rule_check.log` has 36 instance lines; the rerun now reports the 4 skipped corners | Summary item 5, §6.1, §12 row 2 |
| 2 | Muñoz–Serrano's full construction (`φ_λ`, `r(β)`), modelled under every transformation, still misses `z_K` on all 13 (max 0.967; 0.674 → 0.689, 0.217 → 0.249); the earlier relaxation reached `z_K` only by allowing any halfspace | Re-derived from their §5.2 that each replaced inequality vanishes on the null vector `(x_β, β)` with `a^T x_β + d^T β = 0`, so its tangency line is one of the two asymptotes in `H_0`; `ms_asymptote_check.py` (transformation-free upper bound) reproduces all 13 values | §6.1 rewritten (credited, labelled numerical); Summary item 5 |
| 3 | The lineality lemma needs "full-dimensional" | Checked the counterexample `S' = V = R × {0}`, `C = {0} × R` in `R^2` | Theorem 8(3) proof |
| 4 | The gap in Proposition 16 does not follow the angle at `t*` alone; the far face nearly touches `∂S` (`q = 31/2560`) | Verified `31/2560` at `s = 143/320` exactly; reproduced three variant rows (`logs/prop16_variants_spotcheck.log`) and the integer certificate | "Why" paragraph and open question rewritten; certificate added |
| 5 | Stale docstring and log label in `point_rule_check.py` | — | Docstrings and labels of `point_rule_check.py` and `point_rule_refine.py` corrected; both rerun |

Commands for this round (from `sfree/code/`, `OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`; targeted only, no
project-wide checks, CI not consulted):

- `python3 ms_asymptote_check.py` → `logs/ms_asymptote_check.log` (13 misses,
  0 reach `z_K`, max 0.966934);
- `python3 point_rule_check.py 0 40` and `python3 point_rule_refine.py`
  (relabelled; rerun) → `logs/point_rule_check.log`,
  `logs/point_rule_refine.log`;
- `python3 prop16_integer_cert.py` → `logs/prop16_integer_cert.log` (integer
  certificate and `min q = 31/2560` on `[s̄, v_2]`, ALL PASS); the inline
  variant spot check → `logs/prop16_variants_spotcheck.log`.

