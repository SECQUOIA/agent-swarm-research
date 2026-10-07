# Worst-case single-cut ratios for `w = xy`: vertex depth, SCIP's rule, and exactness at the contact point

Stream `ratio-bound`, research-20261001 (see [`../PROGRAM.md`](../PROGRAM.md)).
Dates: work began 2026-10-01; the first author session ended on 2026-10-02 at
about 04:27 UTC, when a usage limit interrupted it right after it wrote the
first version of this note. A second session on 2026-10-02 checked that
version, corrected it (Section 6.2), finished the open computation, and added
Theorems B2 and B3, Corollary A' and Proposition S3. A third session on
2026-10-02 revised the note after review round 1 (Section 6.3; checks in
Section 8.3). The 2026-10-03 revision after review round 2 applied its
optional fixes (Section 6.4); the coordinating agent checked them.
Code is in [`code/`](code/),
raw outputs in [`logs/`](logs/), and one downloaded source in
[`sources/`](sources/) (manifest in Section 7). This builds on the sfree note
[`../../research-20260928b/sfree/optimal-intersection-cuts.md`](../../research-20260928b/sfree/optimal-intersection-cuts.md)
(cited as "the sfree note"; its numbering is used for references to it).
Drafts from this stream were included in repository commits made outside the
stream; this research program itself makes no commits.

Final status (2026-10-04): reviewed in two rounds; r2 verified the revision;
its optional fixes were applied and checked by the coordinating agent; not refereed.

*Review status.* "Reviewed" means checked by another research agent, not
journal peer review. Review round 1 (2026-10-02,
[`reviews/review-r1.md`](reviews/review-r1.md)) re-derived the main proofs,
re-verified the box certificates independently, found no major issue and
three minor ones. Section 6.3 lists each issue and how it was handled.
Review round 2 (2026-10-03,
[`reviews/review-r2.md`](reviews/review-r2.md)) verified that revision, with no
major or minor issues and six optional wording fixes. Those fixes are applied
in this version (Section 6.4) and were checked by the coordinating agent.

## Summary

**Question** (open question of the sfree note). For a bilinear constraint
`w = xy`, is the worst-case ratio of the best single cut from the orbit family
(family (A) of sfree Section 8, or its maximal completions (B)) to the corner
bound `z_K` bounded away from 0 under a quantitative nondegeneracy condition?
The candidates were a grazing margin for the rays, a relative distance of the
LP vertex from `∂S`, and a bounded condition number of the ray matrix. The same
question for SCIP's fixed-`λ` rule; and whether a quantitative transversality
condition at the contact point makes the orbit family exact.

**Main answer.** Only the depth of the LP vertex matters for whether the ratio
is bounded away from 0. Depth is measured by the affinely invariant number

`D = sqrt( max_j |p~_jx| · max_j |p~_jy| / q(s̄) )`,

where `q = w − xy`, `s̄` is the LP vertex, `p~_j = (z_K/c_j) p_j` are the rays
scaled to the corner-bound level, and `c_j` are the reduced costs. The relative
depth is `δ = 1/D²`.

1. **Lower bound** (Theorem A, proved). For every corner (any number of rays,
   any costs), `z_B/z_K ≥ z_A/z_K ≥ 1/(1 + 2D²)` if `D ≤ 1` and
   `≥ 1/((1 + √2) D)` if `D ≥ 1`. A parabolic cylinder of the orbit family
   certifies the bound. No grazing margin and no conditioning is needed. A
   grazing margin `μ` improves only the constant, from `1/(1 + √2) ≈ 0.414` to
   at most 1 (Corollary A', proved).
2. **The order `1/D` is attained, for both families** (Theorems B, B2, B3).
   - Theorem B (proved): in the family `s̄ = (0, 0, ε)`, rays `(1, −1, 0)`,
     `(1, −2, 0)`, `(1, 1, 1)`, unit costs, every ray has an extreme relative
     discriminant (`−1, −1, +1`, so the grazing margin is maximal),
     `cond(P) = 12.01` for all `ε`, and `z_B/z_K → 0` as `ε → 0`.
   - Theorem B2 (computer-assisted proof, checked in exact rational
     arithmetic): in that family `z_A/z_K ≤ z_B/z_K ≤ 137 √ε / z_K < 193.8/D`
     for every `ε ∈ (0, 1)`, and `z_B/z_K ≥ 136.7 √ε / z_K` for
     `ε ≤ ε_1` (the exact threshold in Theorem B2(2)). Numerically
     `z_A/z_K ≈ 56.7 √ε` for small `ε`.
   - Theorem B3 (computer-assisted proof, exact): with two rays that pass
     close to `∂S` (relative discriminant `−0.001`) the constant drops:
     `z_A/z_K ≤ z_B/z_K ≤ 1.54/D` for every depth in the family. With
     relative discriminant `−0.01` (the 1% margin of the sfree adversarial
     search), `z_B/z_K ≤ 2.5/D`. Exact lower bounds from the best sets found
     show that these upper bounds are within 0.06–2.2% of the true (B) values
     on the families computed, for `L ≥ 3.4` (Theorem B3(5)).

   So for vertices close to `∂S` (large `D`) the worst-case ratio of both
   families lies between `0.414/D` and `1.54/D`. The constant of Theorem A is
   within a factor 3.72 of the truth.
3. **SCIP's fixed-`λ` rule** (Lemma S, Theorem S, Propositions S2 and S3,
   proved). SCIP's set is the orbit set `{4N² q(s) ≥ V(s − s̄)²}` (one
   component), with `N² = (x̄ − ȳ)² + (w̄ + 1)²` and the linear form
   `V(d) = (x̄ − ȳ) d_w − (w̄ + 1)(d_x − d_y)`. Its ratio satisfies
   `z_SCIP/z_K ≥ min(1/2, 1/(√6 κ D))`, where `κ = cond(P~)` (three rays).
   Proposition S3 shows that this is sharp up to a constant factor: for every
   `κ ≥ 1` and `D > 0` there is a corner with these values, all relative
   discriminants `+1`, an exact orbit family, and
   `z_SCIP/z_K = 2/(1 + sqrt(1 + κ²D²)) < 2/(κD)`. So SCIP's worst-case ratio
   is `Θ(min(1, 1/(κD)))`. The grazing margin plays no role. With `κ = 1`
   SCIP falls to `2/D` where the orbit family is exact; with `D = 1` it
   falls to about `2/κ`.
   *Scope.* This is SCIP's Case-4 rule for a constraint that SCIP sees
   exactly as `w − xy ≤ 0` (or the mirrored side `w ≥ xy`): SCIP's constant
   `κ_S = 0` (called `kappa` in the source; not the condition number `κ`),
   coefficient 1 on `w`, no linear terms in `x` and `y`, and no rescaling;
   `κ`, `D` and SCIP's set are all taken in the given coordinates. SCIP's
   rule changes if the constraint is rescaled or shifted (for example
   `2w = 2xy`, or `w = xy + c`, which gives `κ_S ≠ 0`), so Theorem S and
   Proposition S3 hold for that exact form only. The task refers to sfree
   Proposition 6, which is a two-variable example for SCIP's Case 2
   (`κ_S = 1`); that setting is not analysed here beyond a remark
   (Section 4).
4. **Exactness at the contact point** (Theorem C and Propositions C2, C3,
   proved). For a support-one minimizer `t*` with transversal edges, the orbit
   sets through `t*` form an explicit two-parameter family, and family (A)
   attains `z_K` if and only if, for some value of a parameter `α > 0`, the
   intervals `I_v(α)` of the other vertices have a common point in the
   interior of the interval `I_s̄(α)` of the LP vertex. If the closed
   intervals have no common point for any `α`, then `z_A < z_K`; the
   boundary case between these two conditions is left open. A sufficient
   quantitative transversality condition is
   `H_cyl := max_t min_v 4 h_v/(t u_vx + u_vy/t)² > 1`, where `u_v = v − t*`
   for the other vertices `v` of the optimal simplex and
   `h_v = ∇q(t*)^T u_v` is the height above the tangent plane. A cruder
   sufficient condition is `h_v > max|u_x| · max|u_y|` for all `v`. The
   constant 1 cannot be lowered: there are non-exact instances with
   `H_cyl ≥ 1 − η` for every `η > 0` (certified exactly for
   `H_cyl ≥ 0.96, 0.996, 0.9996`). No condition on the angles at `t*` alone
   suffices: the map `(x, y, w) → (kx, ky, k²w)` preserves `S`, the orbit
   family and all ratios, and sends the edges of the non-exact instance of
   sfree Proposition 16 to within any angle of the normal (certified exactly
   for `k = 10, 100`).

**Corrections.** To the sfree note (Section 6.1): the near-boundary
adversarial instance has `z_A/z_K ∈ [0.03052, 0.03056]` (both ends certified
exactly in this revision), not `0.0280`; the open question about an angle
threshold is answered by Proposition C2 (no angle threshold works). To the
first version of this note (Section 6.2): eight smaller errors and one code
defect in a heuristic search, none of which changes a main claim; the (B)
computation that was reported as unfinished had in fact finished. After
review round 1 (Section 6.3): a wrong explanation of three failed box searches
(the bounds tried there are false), three numerical values that were presented
as exact (two are now certified exactly, one is relabelled), and a missing
scope statement for the SCIP part. Theorem B2(2) was strengthened, Theorem
B3(5) was added, and Corollary A' was corrected to require `D ≥ 1`.

**Solver relevance.** Modest. Theorem A says that one cut from a parabolic
cylinder through the vertex (a closed form in one parameter `t`) already
gets within the factor `f(D)` of the best single-cut bound. Theorem S and
Proposition S3 say that SCIP's own set can be worse than the best orbit cut
by a factor of order `κD`, even on corners where the orbit family is exact.
In Proposition S3 the loss comes from SCIP's fixed constant `+1` in
`w̄ + 1`, which sets a length scale that the rule does not adapt to the
corner. Whether such corners occur on real instances was not tested here; the
`scip-rule-fidelity` and `scip-set-selection` streams cover SCIP itself.

## 1. Setting, invariance, and a description of the orbit family

Notation follows the sfree note, with one change: reduced costs are `c_j`
(the sfree note calls them `w`), because `w` is also a coordinate.
`S = {(x, y, w) : w ≤ xy}`, `q(s) = w − xy`, LP vertex `s̄` with
`q̄ = q(s̄) > 0`, rays `p_j` (columns of `P`), costs `c_j > 0`,
`z_K = min{c^T λ : λ ≥ 0, q(s̄ + Pλ) ≤ 0}`. `M(x, y, w; h) = [[w, x], [y, h]]`,
`det M(s, 1) = q(s)`. Family (A): `C_F = {s : sym(F^T M(s, 1)) ⪰ 0}`,
`det F > 0`; family (B): `cl(C_F + R_+ e_w)`. `z_A` and `z_B` are the best
single-cut bounds in each family (suprema over sets with `s̄` in the
interior); `z_A ≤ z_B ≤ z_K`. The side `w ≥ xy` is the image of this one under
`(x, y, w) → (x, −y, −w)`, so all results transfer.

*Scaled rays and the optimal simplex.* `p~_j = (z_K/c_j) p_j` and
`T* = conv{s̄, s̄ + p~_j}`; `T_r = conv{s̄, s̄ + r p~_j}`. A set of either
family gives the bound `z_K · min_j α~_j`, where `α~_j` is its step length
along `p~_j` from `s̄`. `X~ = max_j |p~_jx|`, `Y~ = max_j |p~_jy|`,
`D = sqrt(X~ Y~ / q̄)`, `δ = 1/D²`. The *relative discriminant* of a ray is
`(B² − 4A g0)/(B² + |4A g0|)` for the restriction `A s² + B s + g0` of `q` to
the ray; it lies in `[−1, 1]`, and 0 means grazing.

**Lemma N (symmetries and invariants).** The maps
`(x, y, w) → (αx + a, βy + b, αβ w + αb x + βa y + ab)` with `αβ > 0`, and the
swap `x ↔ y`, satisfy `q∘φ = αβ · q`. They map `S` onto `S`, orbit sets onto
orbit sets, (B) sets onto (B) sets, and corners to corners with the same
`z_K`, `z_A`, `z_B` (rays are mapped by the linear part, costs unchanged). The
number `D`, the relative discriminants of the rays, and all ratios `z/z_K` are
invariant. `cond(P~)` and Euclidean angles are not invariant, and neither is
SCIP's rule.

*Proof.* Direct substitution: `x'y' = αβ xy + αb x + βa y + ab`. In matrix
form the map is `M → A M B^T` with `A = [[α, a], [0, 1]]`,
`B = [[β, b], [0, 1]]` (it fixes the slice `h = 1` and multiplies `det` by
`αβ > 0`); so it maps `C_F` to `C_{F'}` and commutes with adding `R_+ e_w`
(the `w`-row has the positive factor `αβ`). The swap is `M → M^T`, which maps
`C_F` to `C_{F^{-1}}`. `X~` and `Y~` scale by `|α|` and `|β|`, `q̄` by `αβ`, so
`D` is invariant; translations and shears do not change the `x`, `y`
components of rays. The relative discriminant is invariant because the
restriction of `q` to a ray is multiplied by `αβ`. ∎

*Normalized frame.* Take `α = t/√q̄`, `β = 1/(t√q̄)`, `a = −αx̄`, `b = −βȳ`
(translate `(x̄, ȳ)` to the origin, then scale). The vertex goes to `(0, 0, 1)`
and a ray `p` becomes `(t p_x/√q̄, p_y/(t√q̄), ∇q(s̄)^T p / q̄)`. There
`M(s̄) = I`, and the orbit sets containing `s̄` in their interior are
`C_X = {sym(X M(s)) ⪰ 0}` with `sym(X) ≻ 0`. (Check: `code/rb.py:
to_normalized_X`, compared with the original-coordinate test on random
points; the step lengths of SCIP's set computed both ways agree,
`logs/check_scip_model.log`.)

**Lemma R (orbit sets are `q ≥ ℓ²` sets).** For `F^T = [[f1, f2], [f3, f4]]`
with `det F > 0`,

`C_F ∩ {h = 1} = {s : det(F) q(s) ≥ ℓ_F(s)²/4,  f1 w + f2 y + f3 x + f4 ≥ 0}`,
`ℓ_F(s) = f1 x − f4 y − f3 w + f2`.

Conversely every affine `ℓ = αx + βy + γw + δ` with `γδ − αβ > 0` arises
(`F^T = [[α, δ], [−γ, −β]]`, `det F = γδ − αβ`). So family (A) is the set of
convex components of `{s : (γδ − αβ) q(s) ≥ ℓ(s)²/4}`, a 3-parameter family
(`ℓ` up to scale).

*Proof.* For a 2×2 matrix `A`, `det sym(A) = det A − ((A12 − A21)/2)²`, and
`sym(A) ⪰ 0` iff `tr A ≥ 0` and `det sym(A) ≥ 0`. With `A = F^T M(s, 1)`:
`det A = det F · q(s)`, `A12 − A21 = ℓ_F(s)`, `tr A = f1 w + f2 y + f3 x + f4`. ∎

This is the 2×2 case of the identity behind Muñoz–Serrano's set
`{λ^T x ≥ ‖y‖}`: for `x ∈ R²`, `(λ^T x)² − ‖y‖² ≥ 0` reads
`‖x‖² − ‖y‖² ≥ ((λ^⊥)^T x)²`. It is elementary; it is used below because it
turns every step-length computation into a scalar quadratic. Numerical check:
0 mismatches in 20000 random `(F, s)` (`logs/check_thmA.log`).

*Parabolic cylinders.* For `t > 0` and a center `(x_c, y_c)`,

`C_t(x_c, y_c) = {s : q(s) ≥ (t(x − x_c) − (y − y_c)/t)²/4}`

is the image of `C_I ∩ {h = 1} = {w ≥ (x + y)²/4} = {q ≥ (x − y)²/4}` under the
map of Lemma N with `t = sqrt(β/α)`, `(x_c, y_c) = (a, b)`. It is the epigraph
`{w ≥ y_c x + x_c y − x_c y_c + (t(x − x_c) + (y − y_c)/t)²/4}`, so it is
convex, upward closed (it equals its own completion, so it lies in (A) and in
(B)), and its interior lies in `{q > 0}`. Along `s̄ + s p`, with center
`(x̄, ȳ)`,

`q(s̄ + sp) − s²(t p_x − p_y/t)²/4 = q̄ + s ∇q(s̄)^T p − s²(t p_x + p_y/t)²/4`

(the `−s² p_x p_y` term of `q` combines with the square). This is concave in
`s`, so the step length is

`α(t; p) = 2q̄ / ( sqrt((∇q(s̄)^T p)² + q̄ (t p_x + p_y/t)²) − ∇q(s̄)^T p )`
(`= ∞` if `t p_x + p_y/t = 0` and `∇q(s̄)^T p ≥ 0`). (1)

Checked against bisection on the definition: maximum relative difference
`1.4·10^-10` on 1200 rays (`logs/check_scip_model.log`).

*Membership in a (B) set* (used in Section 3.1; checked numerically against
the sfree code, 0 mismatches in 20000 random cases,
`logs/explore/test_closed.log`). Let `det X > 0`. Points of `C_X` have
`q ≥ 0` (Lemma R), so a point `s` with `q(s) ≥ 0` lies in
`B_X = cl(C_X + R_+ e_w)` iff `s − τ e_w ∈ C_X` for some `τ ∈ [0, q(s)]`. In
particular `C_X + R_+ e_w` is already closed.

## 2. A lower bound from the vertex depth

**Theorem A.** For every corner of a bilinear constraint with finite `z_K`
(any number `N` of rays, any costs `c > 0`, the cone need not be simplicial),
with `ρ_par := sup_{t>0} min_j α(t; p~_j)`,

`z_B/z_K ≥ z_A/z_K ≥ ρ_par ≥ f(D) := 1/(1 + 2D²)` for `D ≤ 1`, and
`f(D) := 1/((1 + √2) D)` for `D ≥ 1`.

In particular `f(D) ≥ min(1/3, 0.41/D) = min(1/3, 0.41 √δ)`, and
`f(D) → 1` as `D → 0`.

*Proof.* The cylinder `C_t(x̄, ȳ)` is in both families and contains `s̄` in
its interior, so `z_A/z_K ≥ min_j α(t; p~_j)` for every `t`. In the notation
of the normalized frame put `a_j = ∇q(s̄)^T p~_j / q̄` and
`b_j(t) = (t p~_jx + p~_jy/t)/√q̄`; then (1) reads
`α_j = 2/(sqrt(a_j² + b_j²) − a_j)`.

(i) With `t* = sqrt(Y~/X~)`, `|b_j(t*)| ≤ (t* X~ + Y~/t*)/√q̄ = 2D`. (If
`X~ Y~ = 0`, let `t → 0` or `∞`; then `b_j → 0` and the bounds below hold with
`D = 0`.)

(ii) Let `g_j(s) = q(s̄ + s p~_j)/q̄ = 1 + a_j s + c_j s²` with
`c_j = −p~_jx p~_jy/q̄ ∈ [−D², D²]`. Points `s̄ + s p~_j` with `s < 1` cost
`s z_K < z_K`, so they are not in `S`: `g_j > 0` on `[0, 1)` and
`g_j(1) ≥ 0`. Hence `a_j ≥ −1 − c_j ≥ −(1 + D²)`. Moreover
`a_j ≥ −max(2, 2D)`: if the ray meets `S`, its first root `s_1 ≥ 1` gives
`a_j = −(1/s_1 + 1/s_2) ≥ −2` when `c_j > 0` (both roots `≥ 1`) and
`a_j ≥ −1/s_1 ≥ −1` when `c_j ≤ 0`; if it misses `S`, then `c_j ≥ 0` and
`a_j² < 4c_j ≤ 4D²` or `a_j ≥ 0`.

(iii) If `a_j ≥ 0`, `α_j ≥ 2/|b_j| ≥ 1/D ≥ f(D)`. If `a_j < 0`, write
`A = −a_j`; the denominator is `sqrt(A² + b_j²) + A`.
For `D ≤ 1`, `A ≤ 1 + D²` and
`sqrt((1 + D²)² + 4D²) ≤ 1 + 3D²` (square both sides: the difference is
`8D⁴ ≥ 0`), so the denominator is at most `2 + 4D²` and
`α_j ≥ 1/(1 + 2D²)`. For `D ≥ 1`, `A ≤ 2D` and the denominator is at most
`(2√2 + 2) D`, so `α_j ≥ 1/((1 + √2) D)`. ∎

**Corollary A' (a grazing margin improves only the constant).** Consider a
corner as in Theorem A with depth `D ≥ 1`. Suppose every
ray that does not meet `S` and along which `q` initially decreases has
relative discriminant `≤ −μ`, for some `μ ∈ (0, 1]` (no condition on the
other rays). Put
`γ = sqrt((1 − μ)/(1 + μ))` and `γ_D = max(γ, 1/D)`. Then

`z_A/z_K ≥ ρ_par ≥ 1/( D (γ_D + sqrt(1 + γ_D²)) )`.

As `D → ∞` the constant tends to `1/(γ + sqrt(1 + γ²))`, which runs from
`1/(1 + √2)` (`μ → 0`) to 1 (`μ = 1`). (Proved.)

*Proof.* Only step (iii) changes. For a ray that misses `S` with `a_j < 0`
(so `q` initially decreases), the restriction of `q` is `q̄ g_j`, so its
relative discriminant is
`(a_j² − 4c_j)/(a_j² + 4c_j) ≤ −μ`, i.e. `|a_j| ≤ 2γ sqrt(c_j) ≤ 2γD`. For
a ray that meets `S`, `A ≤ 2` by (ii). So `A ≤ max(2, 2γD) = 2Dγ_D`, and the
denominator is at most `sqrt(4D²γ_D² + 4D²) + 2Dγ_D`. ∎

Theorems B and B3 below show that no margin keeps the ratio away from 0: in
Theorem B every relative discriminant is `±1`, and the ratio is still of
order `1/D`.

*Remarks.* (a) The grazing margin and the conditioning of `P` do not enter
Theorem A. Step (ii) uses only that `T*` lies outside `int S` up to its far
face. (b) `D` is affinely invariant (Lemma N), so the theorem holds with `D`
measured in any frame; Euclidean conditions imply it: since
`s̄ − q̄ e_w ∈ ∂S`, `dist(s̄, S) ≤ q̄`, hence
`δ ≥ dist(s̄, S)/(X~ Y~) ≥ dist(s̄, S)/diam(T*)²`. The sfree note's measure
`q(s̄)/max_j |p_j|²` (with `z_K = 1`, `c = 1`) is at most `δ`. So the
"relative distance of the LP vertex from `∂S`" asked about in the task is
the right parameter. (c) The best `t` is a one-dimensional maximization of a
minimum of unimodal functions; any `t` gives a valid bound (closed form (1)).

*Checks* (`code/check_thmA.py 21 60`, `logs/check_thmA.log`): on 60 random
corners (30 with `N = 3`, 30 with `N = 5`, random costs),
`f(D) ≤ ρ_par ≤ z_A` held in all; `z_A` is the normalized-frame SDP bisection,
and `ρ_par/z_A ≤ 1.000000`.

*The adversarial instances of the sfree note* (`code/check_adv_instances.py`,
`logs/check_adv_instances.log`; all have `z_K = 1`, `c = 1`):

| instance (sfree §8.6) | `D` | `f(D)` | `ρ_par` | `z_A` recomputed (normalized frame) | `D · z_A` |
|---|---|---|---|---|---|
| `_7` restart 1 (ray within `6.6·10^-7` of grazing) | 2.96 | 0.140 | 0.305 | 0.6106 | 1.80 |
| `_8` restart 1 (margin `10^-2`) | 8.94 | 0.046 | 0.292 | 0.6224 | 5.57 |
| `_8` restart 4 (the 0.45 instance) | 10.3 | 0.040 | 0.085 | 0.4526 | 4.68 |
| `_8` restart 3 (vertex near `∂S`) | 975.6 | 0.00042 | 0.0129 | 0.0306 (exact bracket `[0.03052, 0.03056]`, Section 6.1) | 29.9 |

The small ratios occur exactly where `D` is large, as Theorem A requires.

## 3. Depth is necessary, and the order `1/D` is attained

**Theorem B.** For `0 < ε < 1` let `s̄ = (0, 0, ε)`, `p_1 = (1, −1, 0)`,
`p_2 = (1, −2, 0)`, `p_3 = (1, 1, 1)`, `c = (1, 1, 1)`, `S = {w ≤ xy}`.

1. `z_K = z_0 := (1 + sqrt(1 + 4ε))/2 ∈ [1, 1 + ε]`, attained only at
   `λ = z_0 e_3`, where ray 3 crosses `∂S` transversally.
2. The relative discriminants of the three rays are `−1, −1, +1` (the extreme
   values; rays 1 and 2 never meet `S`), `cond(P) = 12.01` independently of
   `ε`, and `D = z_0 sqrt(2/ε)`.
3. (Lower bounds.) `z_B/z_K ≥ z_A/z_K ≥ f(D) ≥ √ε / ((1 + √2)√2 z_0)`.
   For `ε ≤ 4/9`, SCIP's set gives exactly `z_SCIP/z_K = 2√ε / z_0`.
4. (Family A, upper bound; superseded by Theorem B2.) For every
   `ε ≤ (160/(5·10^5))² = 1.024·10^-7`, `z_A/z_K ≤ 160 √ε / z_0`.
5. (Family B.) `z_B/z_K → 0` as `ε → 0`.

So neither a grazing margin nor a conditioning bound keeps the ratio away
from 0.

*Proof.* (1) With `λ ≥ 0`, expanding gives
`q(s̄ + Pλ) = ε + λ_3 − λ_3² + λ_2 λ_3 + (λ_1 + 2λ_2)(λ_1 + λ_2) ≥ ε + λ_3 − λ_3²`.
So `q ≤ 0` forces `λ_3 ≥ z_0`, and cost `z_0` needs `λ_1 = λ_2 = 0`. Along ray
3, `d/ds (ε + s − s²) = 1 − 2z_0 < 0` at `s = z_0`.

(2) Ray 1: `q = ε + s²` (`A = 1`, `B = 0`): relative discriminant `−1`; ray 2:
`q = ε + 2s²`, also `−1`; ray 3: `q = ε + s − s²`, `B² − 4A g0 = 1 + 4ε > 0`,
relative value `+1`. `X~ = z_0`, `Y~ = 2z_0`, `q̄ = ε`.

(3) Theorem A. SCIP: `x̄ = ȳ = 0`, so `θ = 0`, `R_θ = I` and SCIP's set is
`C_I ∩ H = {w ≥ (x + y)²/4}` (Lemma S below), which is upward closed. Ray 1
stays in it (`x + y = 0`), ray 2 leaves at `ε = s²/4`, i.e. `s = 2√ε`, ray 3 at
`s = z_0`. So `z_SCIP = min(2√ε, z_0)`, and `2√ε ≤ z_0` iff
`3ε ≤ z_0` iff `ε ≤ 4/9` (using `z_0² = z_0 + ε`).

(4) The automorphism `(x, y, w) → (x/√ε, y/√ε, w/ε)` (Lemma N with
`α = β = ε^{-1/2}`) sends `s̄` to `(0, 0, 1)` and the vertices of
`T_r` to `P_1 = (ρ, −ρ, 1)`, `P_2 = (ρ, −2ρ, 1)`, `P_3 = (ρ, ρ, 1 + H)` with
`ρ = r z_0/√ε`, `H = ρ/√ε`. An orbit set containing `s̄` in its interior is
`C_X` with `sym(X) ≻ 0`. If PSD matrices `Y_0 ≠ 0, Y_1, Y_2, Y_3` satisfy
`Y_0 + Σ_i M(P_i) Y_i = 0`, then for such `X`,
`0 = tr(X Σ_i M_i Y_i) = Σ_i ⟨sym(X M_i), Y_i⟩` (with `M_0 = I`) and the
`i = 0` term is positive, so some `P_i ∉ C_X`. `code/certify_sharpA.py`
builds, for `ρ = 160`, rational `Y_1, Y_2 ≻ 0` and, with `u = 1/H`,
`Y_3(u) = [[θu², σ(u) u], [σ(u) u, n]]`, `σ(u) = σ_∞ + ρθu²`, chosen so that
the sum is symmetric identically in `u`; `Y_0(u) = −(M(P_1)Y_1 + M(P_2)Y_2 +
M(P_3)Y_3(u))`. It verifies in exact arithmetic (sympy, root counting on
`[0, 1/H_0]`) that `Y_3(u) ⪰ 0` and `Y_0(u) ≻ 0` for all `0 < u ≤ 1/H_0`,
`H_0 = 5·10^5` (`logs/certify_sharpA.log`: ALL PASS; the certificate's
entries are printed there). So no orbit set contains `T_r` for
`r = 160√ε/z_0` once `160/√ε ≥ 5·10^5`; containing `T_r` is monotone in `r`.

(5) Fix `z ∈ (0, 1)` and suppose (B) sets `B_n ∋ s̄_n = (0, 0, ε_n)` (interior)
contain `T_n = conv{s̄_n, s̄_n + z p_j}` with `ε_n → 0`. Let `B_n` come from
`F_n` (`‖F_n‖ = 1`), `F_n → F`. Every vertex `v` of `T_n` has a lowered point
`v − τ e_w ∈ C_{F_n}` with `0 ≤ τ ≤ q(v)`; pass to limits.
*Case `det F > 0`.* The limits of the vertices lie in the (B) set of `F` (closed
conditions), so it contains `T_0 = conv{0, z p_j}`, which is full-dimensional.
The (B) set is S-free and contains `0 ∈ ∂S`. It lies in `{w ≥ 0}`: if `b` is
in it with `b_w < 0`, then `q(s b) = s b_w − s² b_x b_y < 0` for small
`s > 0`, and points of the open segment from an interior point of `T_0` to
`s b` close to `s b` are interior points in `int S`. A point of the (B) set
with `w = 0` is a limit of `c + τ e_w`, `c ∈ C_F ⊂ {w ≥ 0}`, so `τ → 0` and it
lies in `C_F`. Hence the triangle `conv{0, z p_1, z p_2} ⊂ {w = 0}` lies in an
exposed face of `C_F ∩ {h = 1}` of dimension 2. But `C_F ∩ {h = 1}` is the
preimage of the 2×2 PSD cone (a circular cone in `R³`) under the affine map
`s ↦ sym(F^T M(s, 1))`. Its linear part has rank 3 or 2: its kernel consists
of the `M(d; 0)` with `F^T M(d; 0) ∈ R J`, a space of dimension at most 1.
With rank 3 the set is an affine image of the cone, whose faces have
dimension 0, 1 or 3. With rank 2 the kernel is spanned by `F^{-T}J`, which
then has a zero `(2, 2)` entry, so the affine image plane does not pass
through the apex 0 (that would need `E_22 + N = c F^{-T} J` with `N` having
zero `(2, 2)` entry). The set is then empty or a cylinder over a conic
section, whose faces have dimension 1 or 3. Either way there is no
2-dimensional face. Contradiction.
*Case `det F = 0`.* Then `F^T = u v^T` and the limits of the lowered points
satisfy `M(l)^T v ∈ R_+ u`, a plane `Π` (the equation is nontrivial since
`F ≠ 0`). The lowered points `l_0 = 0` (`τ_0 ≤ ε_n → 0`),
`l_1 = (z, −z, −τ_1)`, `l_2 = (z, −2z, −τ_2)`, `l_3 = (z, z, z − τ_3)` with
`τ_1 ∈ [0, z²]`, `τ_2 ∈ [0, 2z²]`, `τ_3 ∈ [0, z − z²]` lie on `Π`; their
projections are not collinear, so `Π = {w = αx + βy}`. The set
`U = conv{l_i} + R_+ e_w` is a limit of subsets of the S-free sets `B_n`, hence
S-free, and `U = {(x, y) ∈ Δ, w ≥ αx + βy}` with
`Δ = conv{(0,0), (z,−z), (z,−2z), (z,z)}`. S-freeness means
`αx + βy ≥ xy` on `Δ`; near the vertex `(0, 0)` this forces `α − β ≥ 0` and
`α − 2β ≥ 0`. But `l_1, l_2 ∈ Π` give `α − β = −τ_1/z ≤ 0` and
`α − 2β = −τ_2/z ≤ 0`, so `α = β = 0`, and then `l_3 ∈ Π` gives `τ_3 = z`,
contradicting `τ_3 ≤ z − z²`. ∎

### 3.1 Family (B) is also of order `√ε` (Theorem B2)

**Theorem B2 (computer-assisted).** In the family of Theorem B:

1. For every `ε ∈ (0, 1)`: `z_A/z_K ≤ z_B/z_K ≤ 137 √ε / z_0`. In terms of
   the depth, `z_B/z_K ≤ 137 √2 / D < 193.8/D`.
2. For every `ε ≤ ε_1 := (1367/10)² / (h_0 − 1)² ≈ 1.8288·10^-5`, with
   `h_0 = 5417132036/169459`:
   `z_B/z_K ≥ (1367/10) √ε / z_0`, i.e. `≥ 193.32/D`. (The second session
   certified the weaker constant `273/2` for
   `ε ≤ 24336/1330717441 ≈ 1.8288·10^-5`, with the same `X`; that
   certificate is kept as a check, `logs/certify_zB_lower.log`.)

So `z_B/z_K = Θ(1/D)` on this family, with the constant in front of
`√ε / z_0` between 136.7 and 137 for small `ε` (both ends exact; the gap is
0.22%). This settles open question 2 of the first version of this note, and
part (1) extends Theorem B(4) to all `ε` with a better constant.

*Proof of (1).* In the normalized frame of Theorem B(4), `T_r` with
`r = ρ√ε/z_0` has the vertices `s̄ = (0, 0, 1)`, `P_1 = (ρ, −ρ, 1)`,
`P_2 = (ρ, −2ρ, 1)` and `P_3 = (ρ, ρ, 1 + ρ/√ε)`. The (B) sets are
`B_X = cl(C_X + R_+ e_w)` with `det X > 0` (`X = F^T`). If `B_X` contains
`T_r` with `s̄` in its interior, then the following seven conditions hold:

- (C0)–(C2) `s̄, P_1, P_2 ∈ B_X`;
- (C3)–(C5) the midpoints `m_01, m_02, m_12` of these three points lie in
  `B_X` (convexity);
- (L) `C_X` meets the vertical line `L = {(ρ, ρ, h) : h ∈ R}` (since
  `P_3 − τ e_w ∈ C_X` for some `τ ≥ 0`).

None of these conditions involves `ε`. So if no `X` with `det X > 0`
satisfies all seven for `ρ = 137`, then no (B) set contains `T_r` for
`r = 137√ε/z_0`, for any `ε`, and containment is monotone in `r`.

Three tests exclude a condition for a given `X` with `det X > 0`:

- *Point test.* If `v ∈ R²` satisfies `v^T X M(s) v < 0` and
  `v^T X M(s − q(s) e_w) v < 0`, then `s ∉ B_X`. Indeed `M(s − τ e_w)` is
  affine in `τ`, so `v^T X M(s − τ e_w) v < 0` for all `τ ∈ [0, q(s)]`, and
  `v^T X M v = v^T sym(XM) v`; then use the membership remark of Section 1.
- *Line tests.* The `(2, 2)` entry of `sym(X M(ρ, ρ, h))` is
  `ρ x21 + x22` for every `h`, so (L) needs `ρ x21 + x22 ≥ 0`. Also
  `det sym(X M(ρ, ρ, h)) = det X · (h − ρ²) − (c − x21 h)²/4` with
  `c = ρ x11 − ρ x22 + x12` (Lemma R); for `x21 ≠ 0` its maximum over `h` is
  `(det X / x21²) Ψ(X)` with
  `Ψ(X) = ρ x21 (x11 − x22) + x11 x22 − ρ² x21²`, and for `x21 = 0`,
  `Ψ = det X > 0`. So (L) needs `Ψ(X) ≥ 0`. (The formula for the maximum is
  checked numerically in `logs/explore/test_psi.log`, max relative error
  `1.4·10^-13`; it follows by completing the square.)

All conditions are invariant under `X → λX`, `λ > 0`, so it suffices to
consider the 8 facets `{x_ij = ±1, |other entries| ≤ 1}` of the cube
`max |x_ij| = 1`. `code/certify_zB.py` bisects each facet (3 free entries)
into boxes and, for each box, looks for one of four certificates valid on the
whole box:

- (a) `det X < 0` at all vertices of the box (`det` is multilinear in the free
  entries, so this excludes the whole box);
- (b) a rational `v` and one of the six test points such that both linear
  forms of the point test are negative on the box (a linear function on a
  box is maximal at a vertex);
- (c) an interval upper bound for `Ψ` that is negative;
- (d) `ρ x21 + x22 < 0` on the box.

The search uses floating point with a safety margin and stores each box as a
bisection path. `code/verify_zB.py` then re-derives every box from its path,
checks its certificate in exact rational arithmetic, and checks that the
paths of each facet are prefix-free with Kraft sum exactly 1, so that the
boxes cover the facet. For `ρ = 137` there are 28,699 boxes (8,664 of type
(b), 19,944 of type (c), 54 of type (a), 37 of type (d)); all verified, all 8
facets covered (`logs/zB_cert/verify_rho137.log`; the boxes are in
`logs/zB_cert/leaves_rho137.jsonl.gz`). The same was done for
`ρ = 138, 140, 160, 200`. ∎

The midpoint conditions matter. Without them the closed conditions are met
by rank-one limits `X = ab^T`: degenerate cones that lie in the plane tangent
to `∂S` along the ruling `x = ρ`, which contains lowered copies of `P_1`,
`P_2` and a point of `L`. The midpoints exclude these limits: the tangent
plane passes below the point of `∂S` under `m_01` and `m_02`, so no
admissible lowered point of them lies in the degenerate set
(`code/explore/rank1_midpoint.py`, `logs/explore/rank1_midpoint.log`: for
`X = (γ_0, −ρ)(1, −ρ)^T` and `ρ = 200` the conditions for `s̄`, `P_1`, `P_2`
and `L` hold with margin 0, those for `m_01`, `m_02` fail by about `10^6`).
Since the search only needs necessary conditions, adding the midpoints is
free.

*Proof of (2).* `code/certify_lower_found.py` takes the set found by the
heuristic (B) search, as printed in `logs/zB_extended.log`:
`X = [[1, −1678587/10^6], [1463/200000, 174583/250000]]`, and checks in exact
arithmetic that `sym(X) ≻ 0` (so `s̄ ∈ int C_X ⊂ int B_X`, and
`det X > 0`), that `sym(X M(P_1))` and `sym(X M(P_2))` are PSD for
`ρ = 1367/10` (so `P_1, P_2 ∈ C_X`, without lowering), and that
`sym(X M(ρ, ρ, h_0))` is PSD for `h_0 = 5417132036/169459 ≈ 31967.2`. Then
`P_3 = (ρ, ρ, 1 + ρ/√ε)` lies in `B_X` whenever `1 + ρ/√ε ≥ h_0`, i.e.
`ε ≤ (ρ/(h_0 − 1))² = 53661932375105209/2934348356061848092900`. By
convexity `B_X` then contains `T_r`, `r = ρ√ε/z_0`, so every step of `B_X`
along a scaled ray is at least `r` and `z_B/z_K ≥ r`
(`logs/rev1/certify_lower_found.log`: PASS). ∎ (The same `X` at
`ρ = 273/2`, `h_0 = 255361/8`: `code/certify_zB_lower.py`,
`logs/certify_zB_lower.log`, ALL PASS.)

*Independent sanity checks* (exploratory, `code/explore/`): on 2996 random
`X` with `det X > 0` (half of them near the best set), a direct membership
test (the sfree-based `rb.in_B_X` and a grid over `h`) found no `X` meeting
(C0)–(C2) and (L) at `ρ = 160`, and 46 such `X` at `ρ = 120`
(`logs/explore/sanity_zB_rho160.log`, `..._rho120.log`). A Nelder–Mead search
over the relaxed problem (C0)–(C2) and (L) found positive slack at
`ρ = 135` (`1.8·10^-5`) and negative slack from `ρ = 138` on
(`logs/explore/relaxB2_inf_*.log`), consistent with the certified bracket
`[136.7, 137]`.

*Why the (B) value is about 137, and where (B) gains over (A).* Let
`ρ_max(H)` be the largest `ρ` for which some orbit set `C_X` with `s̄` in its
interior contains `P_1`, `P_2` and `(ρ, ρ, 1 + H)` (Section 3.3). For
`ε ≤ (ρ/H)²` the point `(ρ, ρ, 1 + H)` lies below `P_3` on the vertical line,
so such a `C_X` gives a (B) set that contains `T_r`. Hence, for every `H`,
every `ρ < ρ_max(H)` and every `ε ≤ (ρ/H)²`, the constant of the (B) value
is at least `ρ` (proved, by this construction). The set of part (2) is of
this kind: it contains `P_1`, `P_2` and `(ρ, ρ, h_0)` in `C_X` itself, so
`ρ_max(31966.2) ≥ 136.7` (exact). With part (1), both the (B) constant for
`ε ≤ ε_1` and `sup_H ρ_max(H)` lie in `[136.7, 137]` (exact).
That they are equal, that is, that lowering `P_1` and `P_2` or using a (B)
set whose orbit set misses `s̄` gains nothing more, is numerical evidence
only: the extended (B) search, which allows both, found `136.707`
(Section 3.3), and for the found set the best lowering of `P_1` and `P_2`
is `τ = 0` (`logs/certify_zB_lower.log`, at `ρ = 136.5`). Family (A) must
contain `P_3` itself, at height `1 + ρ/√ε → ∞`, which pushes its constant
down to about 56.7 (numerical).

### 3.2 Nearly tangent rays: the constant of Theorem A is nearly right (Theorem B3)

Theorem B has maximal grazing margins, and its constant (`194/D` for (B),
about `80/D` for (A)) is far above the `0.414/D` of Theorem A. Rays that pass
close to `∂S` make the constant much smaller.

**Theorem B3 (computer-assisted).** For `η ∈ (0, 1)`, `k ≥ 1` with `√k`
rational, and `L > 0`, let `s̄ = (0, 0, 1)`,
`p_1 = (1, −1, −2(1 − η))`, `p_2 = (1, −k, −2√k(1 − η))`, `p_3 = (1, 1, L)`,
unit costs.

1. (Proved.) Rays 1 and 2 never meet `S`; along them `q` has minimum
   `2η − η²` and relative discriminant `((1 − η)² − 1)/((1 − η)² + 1)`
   (`−0.0010005` for `η = 1/1000`, `−0.01005` for `η = 1/100`). Ray 3 has
   relative discriminant `+1`. `L < z_K < L + 1/L`, and the depth is
   `D = √k z_K`.
2. (Computer-assisted, exact.) For `η = 1/1000`, `k = 4` and every `L > 0`:
   `z_A/z_K ≤ z_B/z_K ≤ (197/200)/z_K = 1.97/D`.
3. (Computer-assisted, exact.) For `η = 1/100`, `k = 4` and every `L > 0`:
   `z_B/z_K ≤ (5/4)/z_K = 2.5/D`.
4. (Computer-assisted, exact.) For `η = 1/1000` and every `L > 0`:
   `z_B/z_K ≤ (21/20)/z_K = 1.575/D` if `k = 9/4`, and
   `z_B/z_K ≤ (11/10)/z_K = 1.54/D` if `k = 49/25`.
5. (Exact lower bounds from explicit sets; added after review round 1.) In
   the four cases of parts 2–4 and for every `L ≥ 3.4`:
   `D · z_B/z_K ≥ 2461/1250 = 1.9688` (`η = 1/1000`, `k = 4`),
   `≥ 6117/2500 = 2.4468` (`η = 1/100`, `k = 4`),
   `≥ 15621/10000 = 1.5621` (`η = 1/1000`, `k = 9/4`) and
   `≥ 18851/12500 = 1.5081` (`η = 1/1000`, `k = 49/25`).

With Theorem A: for every `L > 0` the family of part 2 has a corner of depth
`D = 2z_K ∈ (2L, 2L + 2/L)` on which both families give at most `1.97/D`,
while Theorem A guarantees at least `1/((1 + √2)D) = 0.414/D` on every corner
of depth `D ≥ 1`. So the worst-case constant
`C* := lim_{D_0→∞} inf{ D · z_B/z_K : corners of depth D ≥ D_0 }` (and the
same for (A)) lies in `[0.414, 1.97]`; part 4 lowers the upper end to 1.54, so
Theorem A's constant is within a factor 3.72 of `C*`.

*Proof.* (1) Write `m = λ_1 + √k λ_2`. Expanding,
`q(s̄ + Pλ) = [1 − 2(1 − η)m + (λ_1 + λ_2)(λ_1 + kλ_2)] + Lλ_3 − λ_3² + (k − 1)λ_2λ_3`.
By Cauchy–Schwarz `(λ_1 + λ_2)(λ_1 + kλ_2) ≥ m²`, so the bracket is at least
`(m − (1 − η))² + 2η − η² ≥ 2η − η²`, and for `λ ≥ 0`,
`q ≥ 2η − η² + Lλ_3 − λ_3²`. So `q ≤ 0` forces `λ_3 > L`, hence `z_K > L`;
ray 3 alone reaches `∂S` at `(L + sqrt(L² + 4))/2 < L + 1/L`. The
restrictions are `q = 1 − 2(1 − η)s + s²`, `q = 1 − 2√k(1 − η)s + ks²` and
`q = 1 + Ls − s²`. `D`: `X~ = z_K`, `Y~ = k z_K`, `q̄ = 1`.
(2), (3) `s̄` is already in normalized position (`q̄ = 1`, `∇q(s̄) = e_w`).
With `ρ = r z_K`, the vertices of `T_r` are `s̄`,
`P_1 = (ρ, −ρ, 1 − 2ρ(1 − η))`, `P_2 = (ρ, −kρ, 1 − 2√kρ(1 − η))` and
`P_3 = (ρ, ρ, 1 + ρL)` on the vertical line over `(ρ, ρ)`. The proof of
Theorem B2(1) applies verbatim with these test points (none depends on `L`).
`code/certify_zB.py` with family `tan:1/1000:4` and `ρ = 197/200`: 11,132
boxes, all verified by `code/verify_zB.py` (`logs/zB_cert/verify_tan_eta1e-3_k4_rho197_200.log`);
with family `tan:1/100:4` and `ρ = 5/4`: 1,882 boxes, all verified
(`logs/zB_cert/verify_tan_eta1e-2_k4_rho5_4.log`). So `r z_K < ρ` for every
(B) set, and `z_B/z_K ≤ ρ/z_K = √k ρ/D`. For part 4: family `tan:1/1000:9/4`
with `ρ = 21/20` (10,705 boxes) and family `tan:1/1000:49/25` with
`ρ = 11/10` (11,943 boxes), all verified
(`logs/zB_cert/verify_tan_eta1e-3_k9_4_rho21_20.log`,
`logs/zB_cert/verify_tan_eta1e-3_k49_25_rho11_10.log`).
(5) `code/certify_lower_found.py` takes, for each case, the (B) set found by
the heuristic search (the matrix `XB` printed in the log of
`tangent_family.py`, read as an exact decimal) and checks in exact arithmetic
that `sym(X) ≻ 0` (so `s̄ ∈ int B_X` and `det X > 0`), that `sym(X M(P_1))`
and `sym(X M(P_2))` are PSD at `ρ = 2461/2500`, `6117/5000`, `5207/5000`,
`2693/2500` respectively (so `P_1, P_2 ∈ C_X`, without lowering), and that
`sym(X M(ρ, ρ, h_0))` is PSD for `h_0 = 1240951/370546`, `4011447/862162`,
`4025363/954377`, `412614/89749` (about 3.35, 4.65, 4.22, 4.60). Then
`P_3 = (ρ, ρ, 1 + ρL) ∈ B_X` whenever `1 + ρL ≥ h_0`, i.e. for
`L ≥ L_0 = (h_0 − 1)/ρ` (`L_0 = 2.386, 2.986, 3.090, 3.340`). By convexity
`B_X ⊇ T_r` with `r = ρ/z_K`, so `z_B/z_K ≥ ρ/z_K = √k ρ/D`
(`logs/rev1/certify_lower_found.log`: ALL PASS). ∎

*Numerics on this family* (`code/tangent_family.py ETA K B`, heuristic (B)
search whose set is re-checked by an independent membership test, and SDP
bisection for (A); `L = 10, 30, 100, 300, 1000`):

| `η`, `k` | `D · z_A/z_K` (SDP), by `L` | `D · z_B/z_K` found (all `L`) | certified `D · z_B/z_K ≥` (`L ≥ 3.4`) | certified `D · z_B/z_K ≤` (all `L`) | log |
|---|---|---|---|---|---|
| `10^-3`, 4 | 1.928, 1.888, 1.857, 1.840, 1.828 | 1.9689 | 1.9688 | 1.97 | `logs/tangent_family_eta0.001_k4.log` |
| `10^-2`, 4 | 2.278, 2.137, 2.059, 2.022, 2.000 | 2.4468 | 2.4468 | 2.5 | `logs/tangent_family_eta0.01_k4.log` |
| `10^-3`, 9/4 | 1.538, 1.514, 1.499, 1.492, 1.487 | 1.5622 | 1.5621 | 1.575 | `logs/tangent_family_eta0.001_k2.25.log` |
| `10^-3`, 49/25 | 1.449 (`L = 30` only) | 1.5082 (`L = 30` only) | 1.5081 | 1.54 | `logs/tangent_family_eta0.001_k1.96_L30.log` |

So for `L ≥ 3.4` the true (B) constant `D · z_B/z_K` on these families is
known to within 0.06% (`η = 10^-3`, `k = 4`), 2.2% (`η = 10^-2`), 0.8%
(`k = 9/4`) and 2.1% (`k = 49/25`); both ends of each bracket are exact
(Theorem B3(2)–(5)). The (A) values (numerical) are a few percent lower and
still decreasing slowly in `L`.
The cylinder bound gives `D · ρ_par ≈ 0.50`, close to the `0.414` of
Theorem A. Exploratory runs (`logs/explore/tangent_explore2.log`) with `k = 2`
gave `D · z_A ≈ 1.43` (`η = 10^-3`) and `1.39` (`η = 10^-4`) at `D = 424`, so
smaller margins lower the (A) constant a little further. I did not search
over more general configurations.

### 3.3 Numerical picture for the family of Theorem B

(`code/sharp_family.py 2`, `logs/sharp_family_k2.log`; `z_A` by bisection in
the normalized frame with Clarabel, "cert" is the exact bound of the returned
`X`; SCS agrees to 3–4 digits; (B) is a heuristic lower bound, taken from
`logs/sharp_family_k2.log` except at `ε = 10^-5`, where the extended search
of `logs/zB_extended.log` found `0.4323` and `sharp_family_k2.log` has
`0.4310`.)

| `ε` | `D` | `f(D)` | `ρ_par` | `z_A/z_K` (cert / SCS) | best (B) found | SCIP |
|---|---|---|---|---|---|---|
| `10^-1` | 4.9 | 0.085 | 0.982 | 1 / 1 | 1 | 0.579 |
| `10^-2` | 14.3 | 0.029 | 0.485 | 1 / 1 | 1 | 0.198 |
| `10^-3` | 44.8 | 0.0093 | 0.155 | 1 / 1 | 1 | 0.063 |
| `10^-4` | 141 | 0.0029 | 0.049 | 0.9805 / 0.9806 | 0.9805 | 0.020 |
| `10^-5` | 447 | 0.00093 | 0.0155 | 0.4207 / 0.4207 | 0.4323 | 0.0063 |
| `10^-6` | 1414 | 0.00029 | 0.0049 | 0.0994 / 0.0994 | 0.1367 | 0.0020 |
| `10^-7` | 4472 | 0.000093 | 0.0015 | 0.0247 / 0.0248 | 0.0432 | 0.00063 |
| `10^-8` | 14142 | 0.000029 | 0.00049 | 0.0068 / 0.0069 | 0.0137 | 0.00020 |

In the normalized frame the best (A) ratio is `ρ_max(H) √ε / z_0`, where
`ρ_max(H)` is the largest `ρ` for which some `C_X` contains `P_1, P_2, P_3`
(`code/rhomax.py`, `logs/rhomax.log`): `ρ_max = 31.6, 54.8, 98.9, 136.5,
99.1, 75.6, 65.6, 59.2, 57.5, 57.0` for `H = 10^3, 3·10^3, 10^4, 3·10^4, 10^5,
3·10^5, 10^6, 10^7, 10^8, 10^9` (for `H ≤ 3·10^3` it equals `√(1 + H)`,
i.e. `P_3` is on `∂S` and the orbit is exact). These are numerical values on
a coarse grid; the best height lies between grid points: the exact
certificate of Theorem B2(2) gives `ρ_max(31966.2) ≥ 136.7`. The limit problem `H = ∞` (`X` upper triangular, only `P_1`,
`P_2`) gives `ρ_max = 56.71` (SDP; a direct two-variable optimization gives
the same threshold between 56.70 and 56.75). One run at `H = 10^10` returned
35.7, below the limit; I treat it as a solver failure at that scaling. So
`z_A/z_K ≈ 56.7 √ε` for small `ε` (numerical), and at most `137 √ε`
(Theorem B2). The (B) value `136.71 √ε` found for `ε = 10^-5, 10^-6, 10^-8`
(floating-point evaluation) is attained by one fixed `X` with `sym(X) ≻ 0`;
for this `X` the value `136.7 √ε` is certified exactly (Theorem B2(2)). An extended search that also
allows (B) sets whose generating orbit set does not contain `s̄`
(`code/zB_extended.py`, `logs/zB_extended.log`) found the same value,
`136.705, 136.707, 136.707 √ε`, for all three `ε`.

The limit problem `H = ∞` of `rhomax.py` allows only `X` upper triangular,
i.e. `f3 = 0` in Lemma R. These are exactly the parabolic cylinders
`{q ≥ (t(x − x_c) − (y − y_c)/t)²/4}` with an arbitrary center
(`ℓ = f1 x − f4 y + f2` has no `w` term and `det F = f1 f4`). Centered
cylinders (Theorem A) reach only `ρ_par ≈ 4.9 √ε` (table above); moving the
center buys a factor of about 11.6 (numerical).

*Mechanism.* Near a vertex close to `∂S`, horizontal rays in two different
directions of the quadrant `{x > 0, y < 0}` can be accommodated only by cones
whose apex is near `s̄` (in the normalized frame `X ≈ I − A J`); such cones
cut the steep ray 3 after `O(√ε)`. Cylinders accommodate one horizontal
direction exactly (`t² = −p_y/p_x`) but not two. The certificate of
Theorem B(4) is the dual of this trade-off. In Theorem B3 the two nearly
tangent rays pass within `q = 2η` of `∂S` at distance about 1 from `s̄` in
the normalized frame; heuristically, this forces every orbit set to stay near
the tangent pencil of sfree Lemma 13 there.

## 4. SCIP's fixed-λ rule

SCIP's Case-4 set for `w ≤ xy` (Chmiela–Muñoz–Serrano, in the reimplementation
`ms_set` that the sfree note calls "SCIP's set") uses
`λ = x̂(s̄)/‖x̂(s̄)‖` with `x̂ = ((x − y)/2, (w + 1)/2)`. SCIP's
`nlhdlr_quadratic.c` uses the same `xextra = wzlp + kappa + sqrt(1 + kappa²)`
(read in the SCIP 10.0.3 source, lines 1665–1666 of
`scip/src/scip/nlhdlr_quadratic.c`), where SCIP's constant `kappa`, written
`κ_S` here, is 0 for our constraint. (`κ_S` is unrelated to the condition
number `κ = cond(P~)` used in Theorem S.) Write `(sin θ, cos θ) = λ`,
`N² = (x̄ − ȳ)² + (w̄ + 1)²` and `V(d) = (x̄ − ȳ) d_w − (w̄ + 1)(d_x − d_y)`.

*Scope of this section* (stated after review round 1). Everything below is
about SCIP's Case 4 for a constraint that SCIP sees exactly as
`w − xy ≤ 0` (or, mirrored, `w ≥ xy`): `κ_S = 0`, coefficient 1 on `w`, no
linear terms in `x` and `y`, no rescaling, and corners, `κ` and `D` taken in
the given coordinates. In SCIP 10.0.3, `κ_S` is the constant of the quadratic
written as `≤ 0` minus a term in the linear coefficients of the quadratic
variables (`intercutsComputeCommonQuantities`, lines 1151–1204), and
`w(z)` carries the coefficient of `w`. So writing the same constraint as
`2w = 2xy` doubles the eigenvalues and `w(z)` but leaves the `+1` in `x̂`;
this is SCIP's rule applied in the coordinates `(√2 x, √2 y, 2w)`, an
automorphism of Lemma N under which the rule is not invariant (the apex of
SCIP's uncompleted set, Lemma S below, lies on the plane `w = 1` of the
coordinates SCIP uses, which is the plane `w = 1/2` of the original ones).
Writing it as `w = xy + c` with `c ≠ 0` gives `κ_S ≠ 0`, which changes the
formula itself. These consequences were derived from reading the source, not tested
in SCIP. Theorem S and Proposition S3 hold for the exact form above only. The task's step 2 points to sfree Proposition 6, which is a
two-variable example (`S = {y² ≥ x² + 1}`) for SCIP's Case 2 with
`κ_S = 1`; it is not analysed here beyond the remark at the end of this
section.

**Lemma S.** SCIP's uncompleted set (the Muñoz–Serrano set
`{‖ŷ‖ ≤ λ^T x̂}`) is `C_F` with `F^T = R_θ = [[cos θ, −sin θ], [sin θ, cos θ]]`,
and

`C_SCIP = {s : 4N² q(s) ≥ V(s − s̄)²,  cos θ (w + 1) + sin θ (x − y) ≥ 0}`.

Its maximal completion (SCIP's actual Case-4 set) is its upward closure. Along
a ray `p` the step is the first `s > 0` with `4N² q(s̄ + sp) = s² V(p)²`.

*Proof.* With `Φ(x_1, x_2, y_1, y_2) = x_1 I + x_2 J + y_1 K + y_2 L` (sfree
Lemma 10), `M(x, y, w; h) = Φ((w + h)/2, (x − y)/2, (w − h)/2, (x + y)/2)`, so
SCIP's `(x̂, ŷ)` are the Sylvester coordinates and `{λ^T x̂ ≥ ‖ŷ‖}` is
`{sym(R_θ M) ⪰ 0}`: multiplying by `R_θ = cos θ I − sin θ J` rotates
`(x_1, x_2)` and rotates `(y_1, y_2)`. Lemma R with `(f1, f2, f3, f4) =
(cos θ, −sin θ, sin θ, cos θ)` gives `ℓ = cos θ (x − y) − sin θ (w + 1)`, which
vanishes at `s̄` and equals `−V(s − s̄)/N`; `det R_θ = 1`. The completion is
the upward closure by sfree Lemma 10(4). ∎

So SCIP's set is the orbit set of a rotation. This agrees with the
`intersection-literature` stream's Proposition B (Bienstock–Chen–Muñoz's
(14a) sets are exactly the orbit sets with `F^T` a rotation), and SCIP's `λ`
is BCM's choice in their Lemma 4.14 (arXiv v6; `λ ∝ (ā + d̄, b̄ − c̄)` with
`[[ā, b̄], [c̄, d̄]] = M(s̄)`). BCM remark after that lemma that this choice is
"'best' in a violation sense, and may not translate to finding the deepest
cut". Theorem S and Propositions S2, S3 measure how far from the deepest cut
it can be.

Numerical check (`code/check_scip_model.py`): on 1200 rays from 300 random
vertices the step lengths of `ms_set` agree with the upward closure of
`C_{R_θ}` (maximum relative difference `4.0·10^-6`, bisection tolerance), and
the plain Muñoz–Serrano set with `C_{R_θ}` (`9.3·10^-14`). The closed-form
step of Lemma S agrees with the PSD-based step on 600 random corners (maximum
relative difference `8.5·10^-13`, `logs/check_scip_bound.log`). The apex of
`C_{R_θ}` is `(−cot θ, cot θ, 1)`: always on the line `{(−u, u, 1)}`; SCIP's
set is a cylinder exactly when `x̄ = ȳ`.

**Theorem S.** For every corner with three rays (`κ = cond(P~)`),

`z_SCIP/z_K ≥ min( 1/2, 1/(2D), √q̄ / max_j ‖(p~_jx − p~_jy, p~_jw)‖ )
≥ min( 1/2, 1/(√6 κ D) )`,

for the uncompleted set and hence for SCIP's Case-4 set. (With `N` rays
replace `√6` by `sqrt(2N)`.)

*Proof.* Let `g_j(s) = q(s̄ + s p~_j)/q̄ = 1 + a_j s + c_j s²` as in Theorem A.
On `[0, s_0]`, `s_0 = min(1/2, 1/(2D))`, `g_j ≥ 1/4`: if `c_j ≤ 0`, `g_j` is
concave or linear with `g_j(0) = 1`, `g_j(1) ≥ 0`, so `g_j ≥ 1 − s`; if
`c_j > 0` and the ray meets `S`, both roots are `≥ 1` and
`g_j(s) = (1 − s/r_1)(1 − s/r_2) ≥ (1 − s)²`; if it misses `S`,
`a_j > −2√c_j` and `g_j(s) ≥ (1 − √c_j s)² ≥ (1 − Ds)²`. By Lemma S the step
along `p~_j` is at least `min(s_0, s')` where
`4N² q̄ · (1/4) = s'² V(p~_j)²`, i.e. `s' = N√q̄/|V(p~_j)|`, and
`|V(p)| ≤ N ‖(p_x − p_y, p_w)‖`. Below the first zero of the determinant the
matrix stays positive definite (it is at `s = 0`), so the trace condition
holds. For the second form, `‖(p_x − p_y, p_w)‖ ≤ √2 ‖p‖ ≤ √2 ‖P~‖ =
√2 κ σ_min(P~)` and `σ_min(P~) ≤ ‖row_x(P~)‖ ≤ √3 X~`, likewise `≤ √3 Y~`, so
`σ_min ≤ √3 sqrt(X~Y~) = √3 D √q̄`; also `1/(√6κD) ≤ 1/(2D)`. ∎

Checked on 600 random corners (three location regimes): no violation, and the
smallest ratio of the true SCIP value to the first bound is `1.038`, so the
first form is nearly tight on some corners (`logs/check_scip_bound.log`).

**Proposition S2 (without conditioning SCIP is arbitrarily bad, by a pure
rescaling).** Let `s̄ = (0, 0, 1)`, `p_1 = (L, −1/L, 0)`, `p_2 = (L, 1/L, 0)`,
`p_3 = (0, 0, 1)`, `c = 1`, `L ≥ 1`. Then `z_K = 1` (only at ray 2,
transversal crossing), `D = 1`, the relative discriminants are `−1, 1, 1`,
`cond(P~) = L²` for `L ≥ √2` (and `√2 L` for `1 ≤ L ≤ √2`), the orbit
cylinder with `t = 1/L` attains `z_K`, and SCIP's set gives
`z_SCIP = 2/(L + 1/L)`. The instance is the image of the case `L = 1` (where
SCIP is exact) under `(x, y, w) → (Lx, y/L, w)`.

*Proof.* `q(s̄ + Pλ) = 1 + λ_3 + λ_1² − λ_2²` on `λ ≥ 0` (expand), so
`z_K = 1` at `λ = e_2` only. SCIP: `x̄ = ȳ`, so its set is
`{w ≥ (x + y)²/4}`; ray 1 leaves at `s = 2/(L − 1/L)`, ray 2 at
`s = 2/(L + 1/L)`, ray 3 never. The cylinder
`{q ≥ (x/L − L y)²/4}`: along ray 1, `1 + s² ≥ s²`; along ray 2,
`1 − s² ≥ 0` up to `s = 1`; ray 3 stays in. The rows of `P` are orthogonal
with norms `√2 L`, `√2/L`, 1. ∎
(`code/scip_bad_family.py`, `logs/scip_bad_family.log`: `L = 2, 10, 100, 1000`
give SCIP `0.8, 0.198, 0.0200, 0.0020`, orbit `1`.)

**Proposition S3 (Theorem S is sharp in `κD`).** For `u > 1` and `D > 0` let
`v = sqrt(u² − 1)`, `s̄ = (u, −u, −1)`, `p_1 = (vD, 0, 0)`,
`p_2 = (0, −vD, 0)`, `p_3 = (0, 0, −v²)`, unit costs. Then:

1. `z_K = 1`, attained only at `λ = e_3`, where ray 3 crosses `∂S`
   transversally. All three relative discriminants are `+1`. The depth is
   `D`, and `P~ = P` has singular values `vD, vD, v²`, so
   `κ = max(v/D, D/v)`.
2. The orbit family is exact: in the coordinates
   `(x', y', w') = (x − u, y + u, w + ux − uy − u²)` centred at
   `t* = s̄ + p_3 = (u, −u, −u²)`, the orbit set
   `{4q ≥ (x' − y' − βw')², w' + βx' + 1 ≥ 0}` with `β = D/(uD + v)`
   contains `T*` and has `s̄` in its interior. So `z_A = z_B = z_K`, attained.
3. SCIP's Case-4 set and its uncompleted cone both give
   `z_SCIP/z_K = 2/(u + 1)`.

For `D ≤ v`, `κD = v`, so `z_SCIP/z_K = 2/(1 + sqrt(1 + κ²D²)) < 2/(κD)`.
Given any `κ ≥ 1` and `D > 0`, the choice `v = κD`, `u = sqrt(1 + v²)` gives
an instance with exactly these values. Together with Theorem S, SCIP's
worst-case ratio over corners with given `κ` and `D` lies between
`min(1/2, 0.408/(κD))` and `2/(1 + sqrt(1 + κ²D²)) ≤ min(1, 2/(κD))`.
(Proved.)

*Proof.* (1) Expanding with `u² − 1 = v²`:
`q(s̄ + Pλ) = v²(1 − λ_3) + uvD(λ_1 + λ_2) + v²D²λ_1λ_2`. With `λ ≥ 0`,
`q ≤ 0` forces `λ_3 ≥ 1`, and cost 1 needs `λ_1 = λ_2 = 0`;
`∂q/∂λ_3 = −v² ≠ 0`. The restrictions are `v² + uvDs` (rays 1, 2: `A = 0`,
`B > 0`) and `v²(1 − s)` (ray 3), so all relative discriminants are `+1`.
`X~ = Y~ = vD`, `q̄ = v²`.
(2) The map is Lemma N with `α = β = 1`. It sends `t*` to the origin and
`s̄`, `s̄ + p_1`, `s̄ + p_2` to `(0, 0, v²)`, `(vD, 0, v² + uvD)`,
`(0, −vD, v² + uvD)`. This is the set `C_{1,β}` of Theorem C(1). Its slack
`4q − (x' − y' − βw')²` is `v²(4 − β²v²) > 0` at `s̄` (`βv < 1` because
`Dv < uD + v`), `4(v² + uvD) > 0` at the other two vertices (there
`x' − y' − βw' = vD − βv(v + uD) = 0`), and 0 at `t*`; the trace
`w' + βx' + 1` is positive at all four. By convexity `C_{1,β} ⊇ T*`.
(3) Here `x̄ − ȳ = 2u` and `w̄ + 1 = 0`, so `λ = (1, 0)`, `N² = 4u²` and
`V(d) = 2u d_w`; Lemma S gives `C_SCIP = {4q ≥ (w + 1)², x ≥ y}`. Along ray 3,
`4v²(1 − s) ≥ s²v⁴` holds up to `s = 2(sqrt(1 + v²) − 1)/v² = 2/(u + 1)`.
Rays 1 and 2 keep `w = −1`, `q > 0` and `x > y`, so they never leave. For the
completion: the vertical line through `s̄` meets `C_SCIP` in
`w ∈ [1 − 2u, 1 + 2u]`, so along the downward ray 3 the upward closure also
ends at `w = 1 − 2u`, i.e. at `s = 2/(u + 1)`. ∎

`code/scip_kD_family.py` checks (1)–(3) symbolically in `u`, `D` (sympy;
`logs/scip_kD_family.log`: ALL PASS; the slacks of part 2 are printed there
as manifestly positive expressions) and against the Case-4 reimplementation:
for `(u, D) = (100, 1)`, `(100, 10)`, `(100, 99.995)`, `(1000, 30)`, SCIP
gives `0.019802, 0.019802, 0.019802, 0.001998` with `κ = 100.0, 10.0, 1.0,
33.3`, while `z_A = 1` (SDP).

The mechanism is SCIP's constant `+1` in `w̄ + 1`. When `w̄ + 1 = 0`,
SCIP's set is the cone `{4q ≥ (w + 1)², x ≥ y}` whatever the rays are; for
`q̄ ≫ 1` it is narrow (`β² = q̄/(1 + q̄)` below), because its width is set by
the constant 1 and not by the corner. In the normalized frame with
`t² = (1 + q̄ + ȳ²)/(1 + q̄ + x̄²)` SCIP's set is `C_X` with
`X ∝ [[1, β], [β, 1]]` and
`β² = (x̄ − ȳ)² q̄ / ((w̄ + 1)² + (x̄ − ȳ)²(1 + q̄))` (derived by hand and
checked numerically, `code/explore/check_scip_frame.py`, max deviation
`2·10^-15` on 200 vertices; not used in any proof). `β² → 1` is the
narrow-cone case; a mismatch between this `t` and the `t` that suits the rays
is the loss mechanism of Proposition S2.

So, to "does SCIP stay bad under the conditions": SCIP's ratio is bounded
below exactly when `κD` is bounded, with `κ` measured in the given
coordinates (SCIP's rule is not affinely invariant). The grazing margin
plays no role: all margins in Proposition S3 are extreme. With `κ = 1`
(`D = v`) SCIP falls to `2/(u + 1) ≈ 2/D` while the orbit family is exact;
with `D = 1` it falls to `≈ 2/κ`, faster than the `2/√κ` of Proposition S2.
*Remark on sfree Proposition 6.* That example (two variables,
`S = {y² ≥ x² + 1}`, SCIP's Case 2 with `κ_S = 1`) is outside the setting of
this section. It violates both the grazing margin and the conditioning: the
restriction of `x² + 1 − y²` to ray 1 is `(x_0 − s)² + 1`, whose relative
discriminant `−4/(8x_0² + 4)` tends to 0 (the ray becomes parallel to `∂S`),
and `P~` has columns of length `z_K/ε` and `z_K`. So it does not show whether
a margin or a conditioning bound alone would keep SCIP's Case-2 ratio away
from 0; I did not study that question.

*Numerical searches* (heuristic; from the first session). Nelder–Mead over
`(s̄, P)` minimizing SCIP's ratio (`code/scip_search.py`, 12 parameters,
6–12 restarts each): best `0.080` with `D ≤ 1` and no `κ` bound; `0.267` and
`0.238` with `κ ≤ 10` and `D ≤ 1` resp. `D ≤ 2`; `0.302` with `κ ≤ 3`,
`D ≤ 2`; `0.341`, `0.499` with `κ ≤ 10`, `D ≤ 1`, margin `0.1`. Random
sampling (`code/scip_random.py`, 15,731 corners in four location regimes;
minima recomputed by `code/scip_random_minima.py`,
`logs/rev1/scip_random_minima.log`): with `D ≤ 2` and no `κ` bound SCIP
reached `0.0140` (near the anti-diagonal, `κ = 434`); with `D ≤ 2`, `κ ≤ 10`
the minimum was `0.2397` for SCIP's Case-4 set (its completion) and `0.182`
for the uncompleted set. Proposition S3 shows
that these searches were far from the worst case: with `κ = 10`, `D = 1` it
gives `0.181`, and with `κ = 10`, `D = 2` it gives `0.095`. Its corners have
`w̄ = −1` exactly, which random sampling does not hit.

## 5. Exactness at the contact point

Let the corner minimizer `t*` be unique. Translate it to the origin with the
map of Lemma N (`α = β = 1`, `a = −x*`, `b = −y*`); then `∇q(t*) = e_w`, a
vertex `v` of `T*` becomes `(u_x, u_y, h)` with `u = v − t*` and
`h = ∇q(t*)^T u` (its height over the tangent plane), and `q(v) = h − u_x u_y`.

**Theorem C (orbit sets through the contact point; interval criterion).**

1. In these coordinates the orbit sets containing `t*` are exactly
   `C_{α,β} = {s : 4α q(s) ≥ (αx − y − βw)², αw + βx + 1 ≥ 0}` with `α > 0`,
   `β ∈ R` (`F^T = [[α, 0], [β, 1]]`). They are also the (B) sets containing
   `t*` before completion.
2. A point `(x, y, h)` with `h > 0` lies in `C_{α,β}` iff
   `β ∈ I(α) = [ (αx − y − 2√(αq))/h, (αx − y + 2√(αq))/h ]`, `q = h − xy`.
3. Suppose `t*` is a vertex of `T*` (support one) and every other vertex has
   `h_v > 0`. Then some orbit set with `s̄` in its interior contains `T*` (so
   (A) attains `z_K`) iff for some `α > 0` the intervals `I_v(α)` of the
   vertices `v ≠ t*` have a common point in the interior of `I_s̄(α)`. If for
   every `α > 0` the closed intervals have no common point, then
   `z_A < z_K`.
4. (Cylinder criterion; `β = 0`.) If for some `t > 0`,
   `4 h_v ≥ (t u_vx + u_vy/t)²` for all vertices `v ≠ t*` of `T*`, strictly
   for `s̄`, then the parabolic cylinder
   `{q ≥ (t(x − x*) − (y − y*)/t)²/4}` contains `T*` with `s̄` inside, and
   `z_A = z_B = z_K`, attained. In particular this holds if `H_cyl > 1`, and
   if `h_v ≥ max_v |u_vx| · max_v |u_vy|` for all `v ≠ t*` (strictly for
   `s̄`).
5. For a tangent edge (support two, edge direction `d` with
   `∇q(t*)^T d = 0`, `d_x d_y < 0`) the same holds with `α = −d_y/d_x` fixed;
   this is sfree Lemma 13 in these coordinates (`β` is its pencil parameter).

*Proof.* (1) `M(t*) = e_2 e_2^T`. A rank-one `ab^T` lies in `C_F` iff
`F^T a ∈ R_+ b` (sfree Lemma 10(3)), so `F^T e_2 = γ e_2`, `γ ≥ 0`, and
`γ > 0` since `det F ≠ 0`; scale `γ = 1`, then `det F = α > 0`. Lemma R gives
the formula. A (B) set containing `t*` contains a lowered point
`t* − τ e_w` with `τ ≤ q(t*) = 0`. (2) At `w = h` the inequality is
`h²β² − 2hβ(αx − y) + (αx + y)² − 4αh ≤ 0`, whose roots are as stated
because `(αx − y)² − (αx + y)² + 4αh = 4αq`. For the trace condition: the
matrix `F^T M = [[αh, αx], [βh + y, βx + 1]]` has `(1, 1)` entry `αh > 0`,
and `det sym ≥ 0` means `4αh(βx + 1) ≥ (αx + βh + y)²`, so `βx + 1 ≥ 0`.
(3) A set attaining `z_K` contains `T*`, hence `t*`; then use (1), (2) and
convexity (vertices suffice); `s̄` in the interior is `β ∈ int I_s̄(α)`. For
the last claim: if `z_A = z_K`, normalized `F_n` with
`C_{F_n} ⊇ T_{z_n}`, `z_n → 1`, have a limit `F` with `det F ≥ 0` (by
continuity, since `det F_n > 0`); if `det F > 0` then
`C_F ⊇ T*` (closed conditions) and `F` is some `(α, β)` with closed intervals
meeting; if `det F = 0`, `F` has rank one, so `C_F` lies in a plane and
cannot contain the full-dimensional `T*`. (4) `β = 0` is in `I_v(α)` iff
`(αx − y)² ≤ 4αq = 4αh − 4αxy`, i.e. `(αx + y)² ≤ 4αh`; put `α = t²`. The
cylinder is in both families (Section 1). If `H_cyl > 1`, some `t` gives
strict inequality at every vertex. With `t = sqrt(Y/X)`,
`(t u_x + u_y/t)² ≤ 4XY`. (5) Points `s d` of the edge have `w = 0`, so
`sym` has a zero diagonal entry and the off-diagonal entry `(αx + y)/2` must
vanish along `d`. ∎

The general form for (B) replaces `I_v(α)` by the union of the intervals of
the lowered points `(u_x, u_y, h')`, `max(u_x u_y, 0) < h' ≤ h` (and, if
`α u_x + u_y = 0`, the point at `h' = 0`).

*Check* (`code/check_exactness.py 3 150`, `logs/check_exactness.log`): on 150
random support-one corners with transversal edges the interval criterion and
the SDP bisection agree in every case (two cases where the criterion says
exact, with `H_cyl ≥ 1.7`, got `z_A = 0.99998` from the SDP; there the
cylinder proves exactness, so the SDP under-reports). 138 had `H_cyl ≥ 1`, all
exact; 2 were not exact, with `H_cyl ≤ 0.46`; the (B) intervals never gave a
worse answer than (A). The criterion reproduces the recheck's variant table of
sfree Proposition 16: gap `> 0` (not exact) for `v_2 = (6, −2, 1/4)`,
`(6, −2, 1)`, `(8, −3, 1/4)` and `< 0` (exact) for `(6, −2, 2)`,
`(6, −4, 1/4)`, with `H_cyl = 0.30, 0.48, 0.28, 0.66, 0.63`; so the cylinder
criterion is sufficient but not necessary.

**Proposition C2 (no condition on angles at `t*` suffices).** Let `I` be a
non-exact support-one instance with `t* = 0` and transversal edges, for
example sfree Proposition 16. For `k > 0`, the map
`φ_k(x, y, w) = (kx, ky, k²w)` sends `I` to an instance with the same `z_K`,
`z_A`, `z_B` (Lemma N with `α = β = k`), the same `D`, relative discriminants
and `H_cyl`, and its edges `u ↦ (k u_x, k u_y, k² h)` make angles with the
tangent plane `w = 0` whose sines `k²h/sqrt(k²(u_x² + u_y²) + k⁴h²)` tend to 1.
Hence for every angle `θ < 90°` there is a non-exact instance all of whose
edges at `t*` make an angle `≥ θ` with the tangent plane.

The positive definite certificate of sfree Proposition 16 transfers:
`M(φ_k v) = Δ M(v) Δ` with `Δ = diag(k, 1)`, so
`Y'_v = Δ^{-1} Y_v Δ^{-1}` satisfies `Σ_v M(φ_k v) Y'_v = 0`.
`code/certify_support_one.py` re-certifies the scaled instances from scratch
for `k = 1, 10, 100` (face enumeration, unique minimizer, rational positive
definite certificate; `logs/certify_support_one.log`: ALL PASS); for `k = 100`
the edge cosines with `∇q(t*)` are `0.99984, 0.96946, 0.99855`. The price is
conditioning: `cond(P)` grows like `k`. The invariant replacement for an angle
is the ratio of the height `h_v` to `|u_x| |u_y|`, as in Theorem C(4).

**Proposition C3 (the constant 1 in the cylinder criterion is best
possible).** For `d > 0` let `t* = 0`, `s̄ = (3/2, −1/2, 1/4 − d)`,
`v_2 = (1/2, 3/2, 1 − d)`, `v_3 = (3, 1, 4 − d)`, rays from `s̄` to
`t*, v_2, v_3`, unit costs. For all sufficiently small `d > 0`: `z_K = 1` with
the unique minimizer `t*` (support one), the edges at `t*` are transversal,
`H_cyl ≥ 1 − 4d`, and `z_A < z_K`. For `d = 1/100, 1/1000, 1/10000` this is
certified in exact arithmetic (`H_cyl ≥ 24/25, 249/250, 2499/2500`).

*Proof.* At `t = 1`, `4h_v/(u_x + u_y)² = 1 − 4d, 1 − d, 1 − d/4`. In the
centred coordinates of Theorem C,
`q(s̄) = 1 − d`, `q(v_2) = 1/4 − d`, `q(v_3) = 1 − d`, and with `α = t²`:
`left_s̄(t) = (3t²/2 + 1/2 − 2t sqrt(1 − d))/(1/4 − d)`,
`right_2(t) = (t²/2 − 3/2 + 2t sqrt(1/4 − d))/(1 − d)`,
`left_3(t) = (3t² − 1 − 2t sqrt(1 − d))/(4 − d)`.
For `0 < d ≤ 1/8` use `1 − sqrt(1 − d) ≥ d/2` and
`sqrt(1/4 − d) ≤ (1 − 2d)/2`. For `t ≥ 1`, the numerator of `left_s̄` is at
least `(3t − 1)(t − 1)/2 + td ≥ 0`, so `left_s̄ ≥ 2(3t − 1)(t − 1) + 4td`, and
`right_2 ≤ (8/7)(t + 3)(t − 1)/2`; hence
`left_s̄ − right_2 ≥ (t − 1)(38t − 26)/7 + 4dt > 0`. For `0 < t ≤ 1`, split
the numerator of `left_3` as `(3t + 1)(t − 1) + 2t(1 − sqrt(1 − d))`, a
nonpositive part plus a nonnegative part, so
`left_3 ≥ (8/31)(3t + 1)(t − 1) + td/4`; and the numerator of `right_2` is at
most `(t + 3)(t − 1)/2 − 2td ≤ 0`, so `right_2 ≤ (t + 3)(t − 1)/2 − 2td`.
Hence `left_3 − right_2 ≥ (1 − t)(77 − 17t)/62 + 2dt > 0`.
So for every `α` two of the closed intervals are disjoint, and Theorem C(3)
gives `z_A < z_K` once `T* ∩ S = {t*}`. At `d = 0` all three vertices lie on
the cylinder `{w ≥ (x + y)²/4}`, no two on a common ruling and none on its
contact curve `x = y` except `t*`, so `T* ∩ S = {t*}`; for small `d` this
persists by compactness (near `t*` because the heights are positive, away
from `t*` because `q > 0` on the compact rest). ∎
(`code/certify_support_one.py` verifies the three values of `d` from scratch,
including the face enumeration; `logs/certify_support_one.log`. The (B)
interval gap equals the (A) gap for `d = 10^-2, 10^-3` numerically, so these
instances are probably not (B)-exact either; this is not certified.)

So, to "does some quantitative transversality condition at the contact point
make the orbit family exact": yes. The condition must compare the height of
each vertex over the tangent plane at `t*` with the curvature term
`(t u_x + u_y/t)²/4` (Theorem C(4)), and the threshold 1 is sharp
(Proposition C3). A condition on angles alone cannot work (Proposition C2).
For support one, the one-parameter interval test of Theorem C(3) decides
whether family (A) attains `z_K`. It also proves `z_A < z_K` when the closed
intervals never meet. It leaves open one boundary case: the closed intervals
meet for some `α`, but never in the interior of `I_s̄(α)`. Then `z_K` is not
attained, and whether `z_A = z_K` holds as a supremum is undecided.

## 6. Corrections

### 6.1 Corrections and additions to the sfree note

- *Near-boundary adversarial instance* (sfree §8.6, last bullet; `_8` restart
  3). The sfree note reports `z_A = 0.0280` with "Clarabel ... reports
  infeasibility from 0.029 on". In the normalized frame Clarabel's bisection
  gives `0.030551` (lower and upper value agree), and an explicit rational `F`
  contains `s̄` in its interior and the simplex `T_r` with `r = 763/25000 =
  0.03052`, checked in exact arithmetic with the instance data taken as the
  exact binary floats (`code/recheck_adv3.py`, `logs/recheck_adv3.log`).
  In the revision after review round 1 the upper end is also certified
  exactly: a rational dual certificate (`code/certify_adv3_upper.py 191/6250`,
  `logs/rev1/certify_adv3_upper_191_6250.log`) shows that no orbit set with
  `s̄` in its interior contains `T_r` for `r = 191/6250 = 0.03056`. It is
  the argument of Theorem B(4): PSD matrices `Y_0 ≻ 0`, `Y_1`, `Y_2`, `Y_3`
  with `Σ_j M(v_j) Y_j = 0`, where `v_0 = s̄` and `v_1, v_2, v_3` are the
  other vertices of `T_r`, give `Σ_j ⟨sym(X M(v_j)), Y_j⟩ = 0`; for an `X`
  with `sym(X M(s̄)) ≻ 0` the `j = 0` term is positive, so some `v_j` is not
  in `C_X`. So
  `z_A/z_K ∈ [763/25000, 191/6250] = [0.03052, 0.03056]`, both ends exact
  (with the instance data and the scaled rays taken as the binary floats of
  the code; the float `z_K` is `1 + 6.7·10^-16`). The version of this
  note reviewed in round 1 wrote `[0.0305, 0.0306]` and labelled it as
  computed exactly, although its upper end was only Clarabel's bisection
  value (SCS gave `0.0337` as its upper value). The earlier infeasibility
  was caused by the scaling of the original-coordinate SDP
  (`q(s̄) = 5.3·10^-6`). The qualitative conclusion (the ratio tends to 0
  as the vertex approaches `∂S`) stands and is now proved (Theorems B, B2). Other restarts change slightly
  (`_7` restart 0: `0.375 → 0.404`; `_7` restart 3: `0.500 → 0.509`; `_8`
  restart 2: `0.9375 → 0.9985`); the values quoted in the sfree note
  (`0.6106`, `0.6224`, `0.4526`) are reproduced to all quoted digits
  (numerical).
- *(B) searches.* The sfree code evaluates (B) sets only after shifting `F` so
  that `s̄ ∈ C_F` (`interior_shift`), so its (B) search covers only
  completions whose orbit set contains `s̄`. The quoted (B) numbers remain
  valid lower bounds. On the Theorem B family the larger search found nothing
  better (numerical). Exactly: a set of the restricted kind (its orbit set
  contains `s̄`) attains `136.7 √ε/z_0` for `ε ≤ ε_1`
  (Theorem B2(2)), and no (B) set exceeds `137 √ε/z_0` (Theorem B2(1)), so
  there the restriction loses at most `137/136.7 − 1 < 0.22%`. (The version
  reviewed in round 1 gave the bracket `[136.707, 137]`; `136.707` is a
  floating-point evaluation of a heuristic set, not a certified value.)
- *Open question on angles* (end of sfree §8.6): "an angle threshold alone
  would have to exceed a cosine of about 0.16". Proposition C2 shows that no
  angle threshold works.
- *Open question on the worst-case ratio* (sfree Summary): answered by
  Theorems A, B, B2 and B3 (bounded below iff the depth `D` is bounded; order
  exactly `1/D`, constant between 0.414 and 1.54). The sfree note read the
  0.45 instance as "set by the margin" (two of its rays sit on the imposed 1%
  margin). With a 1% margin the ratio still tends to 0, like at most `2.5/D`
  (Theorem B3(3)); the margin changes the constant, not the order.

### 6.2 Corrections to the first version of this note (2026-10-02, first session)

Found in the second session by checking every proof and rerunning the exact
certificates (Section 8.2). None changes a main claim.

1. *The (B) run was not unfinished.* `logs/zB_extended.log` contains all three
   values (`136.7054, 136.7066, 136.7067 √ε` for `ε = 10^-5, 10^-6, 10^-8`);
   the run finished at 04:24 UTC, three minutes before the note was written.
2. *Normalized frame.* The translation parameters are `a = −αx̄`,
   `b = −βȳ`, not `a = −x̄`, `b = −ȳ` (the map translates first, then
   scales). The formulas for the transformed rays were right.
3. *Proposition S2.* `cond(P~) = L²` holds only for `L ≥ √2`; for
   `1 ≤ L ≤ √2` it is `√2 L` (the log shows `1.414` at `L = 1`).
4. *Theorem B(3).* SCIP's ratio is `min(2√ε, z_0)/z_0`; the formula
   `2√ε/z_0` needs `ε ≤ 4/9`.
5. *Theorem B(4)* claimed a strict inequality; the certificate gives `≤`
   (strictness needs an extra compactness step). It is now superseded by
   Theorem B2(1).
6. *Theorem B(5), case `det F > 0`.* The first version discussed a "dihedral
   wedge" case (a plane section through the apex of the cone). That case
   cannot occur: when the linear part of `s ↦ sym(F^T M(s, 1))` has rank 2,
   the image plane misses the apex. The proof above is corrected accordingly;
   the conclusion is unchanged.
7. *Summary item on transversality.* `H_cyl ≥ 1` is sufficient only with
   strict inequality at `s̄`; the summary now says `H_cyl > 1`.
8. *Proposition C3.* The proof said that for `t ≤ 1` the numerators of
   `left_3` and `right_2` are `≤ 0`; the numerator of `left_3` is slightly
   positive near `t = 1`. The estimate holds after splitting that numerator
   into a nonpositive and a nonnegative part, as now written.
9. *Code defect in the heuristic (B) search* (`rb.zB_heur`). Its
   parametrization can overflow (lowering parameter `τ_0 → 1`), and the step
   routines then return `∞` for a matrix with infinite entries, so the search
   can report a meaningless value (it reported `10^6` on one new instance in
   this session). The search now rejects non-finite matrices, and
   `tangent_family.py` re-checks the returned set with an independent
   membership test (`zB_check`). The (B) values of the first version are
   unaffected: their matrices are finite, and they lie below the certified
   upper bounds of Theorem B2.

The first version's open questions 2 (rate for family (B)) and 3 (exponent of
`κ` in Theorem S) are now answered by Theorem B2 and Proposition S3.

### 6.3 Revision after review round 1 (2026-10-02)

Review round 1 ([`reviews/review-r1.md`](reviews/review-r1.md), by another
research agent) found no major issue, three minor issues and seven optional
points. Each is listed here with what was done. Theorem B2(2) was strengthened,
Theorem B3(5) was added, and Corollary A' was corrected to require `D ≥ 1`.
Two numerical statements were replaced by exact ones, and one was relabelled.
The commands are in Section 8.3.

*Minor issue 1: wrong reason for three failed box searches.* The reviewed
version said that the box searches for `ρ = 6/5` (family `tan:1/100:4`) and
`ρ = 1, 19/20` (family `tan:1/1000:9/4`) stopped at maximum depth because the
closed relaxation (`s̄ ∈ B_X` instead of `s̄ ∈ int B_X`) is feasible on the
boundary, and that "the certified constants can be slightly above the true
ones". That was wrong: the bounds tried there are false.
- New Theorem B3(5) (`code/certify_lower_found.py`) gives exact (B) sets with
  `s̄` in the interior at `ρ = 6117/5000 = 1.2234` (`η = 1/100`, `k = 4`) and
  `ρ = 5207/5000 = 1.0414` (`k = 9/4`), for every `L ≥ 2.99` and `L ≥ 3.09`
  respectively. A set that contains `T_r` also contains every `T_r'` with
  `r' ≤ r`, so these sets are valid at `ρ = 6/5`, `1` and `19/20` too. The
  reviewer's own exact check (`reviews/r1-code/exact_feasible_below.py`,
  rerun here with identical output) gives sets at these three values for
  `L = 10, 30, 100, 300, 1000`.
- Hence `z_B/z_K ≤ ρ/z_K` is false at these `ρ`, and no method could certify
  it. A box that contains a feasible `X` can never be excluded; the search
  stopped near an `X` with `s̄` on the boundary of `B_X`, which is a boundary
  point of the feasible set. The three runs say nothing about the closed
  relaxation.
- Corrected in Section 8.2 (the three rows), Section 9 (the bullet on the
  closed relaxation). The general caveat remains: the
  seven conditions are only necessary, so a certified bound may lie above
  the true value; but no case was observed where the closed relaxation
  blocked a true bound.
- As the reviewer suggested, the best sets found are now certified exactly,
  so "within 0.06–2.2% of the best sets found" is now an exact bracket
  (Section 3.2 table).

*Minor issue 2: numerical values presented as exact or proved.*
- (a) "`z_A/z_K ∈ [0.0305, 0.0306]`, computed exactly" (Section 6.1): only the
  lower end was exact. The upper end is now certified exactly by a rational
  dual certificate (`code/certify_adv3_upper.py`): `z_A/z_K ∈
  [763/25000, 191/6250] = [0.03052, 0.03056]`.
- (b) "True constant in `[136.707, 137]`, within 0.22%" (Section 6.1): `136.707`
  was a floating-point value of a heuristic set. Theorem B2(2) now certifies
  `136.7` for the same `X` (with `h_0 = 5417132036/169459`, for
  `ε ≤ 1.8288·10^-5`), so the certified bracket is `[136.7, 137]` and the
  gap is below 0.22%. The earlier certificate at `273/2` is kept as a check.
- (c) "The (B) value is the (A) value at the best height" (Section 3.1): only
  "`≥`" follows from the construction. The paragraph now says this. Both
  values lie in `[136.7, 137]` (exact). Equality is labelled numerical
  evidence.

*Minor issue 3: scope of the SCIP part not stated.* Added to Summary item 3,
to the start of Section 4 and to Section 9. The analysis covers SCIP's Case 4
for a constraint seen exactly as `w − xy` (`κ_S = 0`, unit coefficient of
`w`, no linear terms in `x`, `y`, no rescaling), in the given coordinates.
Rescaling or shifting the constraint changes SCIP's set. The Case-2 example
of sfree Proposition 6 gets only a remark, which now states the relative
discriminant `−4/(8x_0² + 4)` that the reviewer computed.

*Optional points.*
- O1: the Section 3.3 caption now cites both logs for the (B) column.
- O2: "equals `√H`" corrected to `√(1 + H)`.
- O3: Section 4 now says 15,731 corners and gives the minimum `0.2397` for
  SCIP's Case-4 set with `D ≤ 2`, `κ ≤ 10`. It also gives `0.182` for the
  uncompleted set, which the reviewed version did not mention. Both are
  recomputed by the new `code/scip_random_minima.py`.
- O4: SCIP's constant is now written `κ_S`; `κ` is only `cond(P~)`.
- O5: the end of Section 5 and Summary item 4 now say that Theorem C(3)
  decides whether `z_K` is attained, and they name the open boundary case.
- O6: Corollary A' now has `D ≥ 1` in its hypothesis.
- O7: the box files for `ρ = 137, 138, 140, 160, 200` were written by an
  earlier version of `certify_zB.py`: their header stores `ρ` as a float
  and has no family key. Rerunning `certify_zB.py 137` with the current code
  reproduces exactly the same 28,699 leaves (same facets, paths, certificate
  types and certificate data), and `verify_zB.py` passes
  (`logs/rev1/`; Section 8.2 says so).

The reviewer also remarked that the appeal to sfree Proposition 12 in the
proof of Theorem C(3) is unnecessary. The proof now uses continuity of
`det` instead. The reviewer noted that the bound `+ 2dt` in Proposition C3
can be sharpened to `+ (9/4)dt`; it is valid as written and was left
unchanged.

### 6.4 Revision after review round 2 (2026-10-03)

Review round 2 ([`reviews/review-r2.md`](reviews/review-r2.md)) verified the
note with no major or minor issues. All six optional items are handled below;
these wording fixes have not been independently re-reviewed; they were checked by
the coordinating agent.

- N1: replaced `ε ≤ 1.83·10^-5` in all four places with `ε ≤ ε_1`, the
  exact threshold already certified in Theorem B2(2). No wider range is used.
- N2: changed Summary item 2 from `= 193.8/D` to `< 193.8/D`.
- N3: replaced both statements that no theorem changed with the actual
  changes: B2(2) was strengthened, B3(5) was added, and Corollary A' was
  corrected to require `D ≥ 1`.
- N4: removed both references to a results list absent from this note.
- N5: Section 8.3 now gives the dual margins separately: `1.9·10^-8` for
  `R = 153/5000` and `3.4·10^-9` for `R = 191/6250`, matching the stored logs.
- N6: replaced the claim that nothing was committed with the statement that
  drafts were included in repository commits made outside the stream; this
  research program itself makes no commits.

## 7. Relation to prior work, and novelty

Sources checked for this stream: the sfree note and its reviews; the
`intersection-literature` stream's note (read-only, for Bienstock–Chen–Muñoz
and the citing literature); the SCIP 10.0.3 source
(`scip/src/scip/nlhdlr_quadratic.c`, Case-4 restriction code, read-only); one
downloaded paper. Manifest of `sources/`:

| file | URL | accessed | version | sha256 |
|---|---|---|---|---|
| `bienstock-chen-munoz-1610.04604v6.pdf` | https://arxiv.org/pdf/1610.04604v6 | 2026-10-02 | arXiv v6 (2 June 2019) | `30e19c5538d58a944cb2f1f690dd7d6c4dc4ca8d4317b6a2c2c565e71447fe88` |

Web searches on 2026-10-02. First session: "intersection cuts maximal
quadratic-free sets bilinear strength approximation ratio corner relaxation",
"outer-product-free / quadratic-free sets ... distance to the boundary ...
strength bound", "worst-case strength of intersection cuts nonconvex
quadratic single cut". Second session: "intersection cuts bilinear
quadratic-free strength depth LP vertex distance boundary bound ratio corner
polyhedron nonconvex QCQP", "intersection cuts outer-product-free or
quadratic-free approximation guarantee single cut strength theorem
2023 2024 2025", "intersection cut strength arbitrarily weak or approximation
ratio bilinear S-free maximal set choice lambda Chmiela Muñoz Serrano", and
one on computer-assisted interval branch-and-bound proofs. They returned
Muñoz–Serrano (arXiv 1911.12341), Chmiela–Muñoz–Serrano (ZIB reports 20-29
and later versions), Bienstock–Chen–Muñoz (arXiv 1610.04604), Averkov–Basu–Paat
(arXiv 1705.02015) and a 2025 paper on monoidal strengthening for MIQCPs;
none gives a worst-case ratio for single quadratic intersection cuts or
compares the `λ` rule with the deepest cut quantitatively.

- *Bienstock–Chen–Muñoz* (Math. Program. 2020; arXiv v6 read in Sections 2
  and 4.2). Their oracle-based cuts use the S-free ball `B(x̄, d(x̄, S))` and
  separate over the whole polyhedron, with convergence of the closure. They
  give no single-cut ratio for the corner relaxation. Their Lemma 4.14 (Lemma
  24 in v7) is the `λ` rule that SCIP uses (Section 4), with the remark that it is best "in a
  violation sense, and may not translate to finding the deepest cut";
  Theorem S and Propositions S2 and S3 quantify that remark. Lemma R is the
  elementary reformulation of orbit sets as `det ≥ (linear)²`, which I did not
  find stated in this form, but it is immediate from the definitions.
- *Averkov–Basu–Paat* (SIOPT 2018; abstract only, through the sfree note)
  study constant-factor approximation of the corner polyhedron by closures of
  lattice-free families. Theorem A is a single-cut statement for one
  quadratic constraint with a depth-dependent factor, and Theorems B–B3 show
  that no constant factor holds for single cuts from the orbit family.
- *Muñoz–Serrano, Chmiela–Muñoz–Serrano.* Lemma S identifies SCIP's set as an
  explicit orbit set; the formula `4N²q ≥ V(s − s̄)²`, Theorem S and
  Proposition S3 are, as far as I found, not stated there.
- Theorem C refines sfree Lemma 13 (tangent edges) to support one and makes
  it a decision procedure; Proposition C3 answers the sfree open question.
- The computer-assisted proofs of Theorems B2 and B3 use only standard
  ingredients (homogeneity, multilinear and interval bounds on boxes, exact
  rational re-verification); I did not find them used for cut-strength
  questions, but did not search specifically.

Novelty is qualified: the searches were short (seven queries, one paper read
in part, plus the `intersection-literature` stream's audit), and the results
use only elementary tools once the orbit family is written as in Lemma R. An
unsuccessful search does not establish novelty.

## 8. Checks actually run

All commands were run from `research-20261001/ratio-bound/code/` (the
exploratory ones from `code/explore/`) with `OMP_NUM_THREADS=1`, at most four
processes at a time except for one brief exception noted under "Process
hygiene"; the machine was shared and heavily loaded. They are targeted local checks; no project-wide
verification was run and CI was not consulted. The library `code/rb.py`
imports `core.py` and `bilinear.py` from `research-20260928b/sfree/code`
read-only.

### 8.1 First session (2026-10-01/02)

| command | purpose | actual outcome (log in `logs/`) |
|---|---|---|
| `python3 check_scip_model.py` | SCIP's Case-4 set = upward closure of `C_{R_θ}`; plain set = `C_{R_θ}`; cylinder formula (1) | PASS at tolerance `1e-5`: max rel. diff `4.0e-6`, `9.3e-14`, `1.4e-10` on 1200 rays (`check_scip_model.log`) |
| `python3 check_stepB.py` | closed-form (B) step vs bisection | PASS, 3705 finite pairs, max rel. diff `4.7e-8` (`check_stepB.log`) |
| `python3 check_thmA.py 21 60` | Lemma R; Theorem A on 60 random corners (`N = 3, 5`) | Lemma R 0 mismatches / 20000; 0 violations of `f(D) ≤ ρ_par ≤ z_A` (`check_thmA.log`) |
| `python3 check_adv_instances.py` | `D`, `f(D)`, `ρ_par`, recomputed `z_A` on the sfree adversarial instances | table of Section 2 (`check_adv_instances.log`) |
| `python3 recheck_adv3.py` | near-boundary instance, normalized SDP, exact containment | Clarabel `0.030551/0.030551`, SCS `0.0117/0.0337`; exact check PASS at `r = 763/25000` (`recheck_adv3.log`) |
| `python3 sharp_family.py 2` | Theorem B family, `ε = 10^-1 … 10^-8` | table of Section 3.3 (`sharp_family_k2.log`) |
| `python3 certify_sharpA.py` | Theorem B(4), exact certificate | ALL PASS with `ρ = 160`, `H_0 = 5·10^5` (`certify_sharpA.log`) |
| `python3 rhomax.py` | `ρ_max(H)` and the `H = ∞` limit | values in Section 3.3; limit `56.714`; the `H = 10^10` value `35.7` is a solver failure (`rhomax.log`) |
| `python3 zB_extended.py` | (B) search with `s̄` only in the completion | `136.7054, 136.7066, 136.7067 √ε` for `ε = 10^-5, 10^-6, 10^-8` (`zB_extended.log`; complete, see Section 6.2) |
| `python3 scip_bad_family.py` | Proposition S2 | SCIP `1, 0.8, 0.19802, 0.019998, 0.0020` for `L = 1, 2, 10, 100, 1000`; orbit 1 (`scip_bad_family.log`) |
| `python3 check_scip_bound.py 5 600` | Lemma S closed form; Theorem S | max rel. diff `8.5e-13`; 0 violations; min ratio to bound `1.038` (`check_scip_bound.log`) |
| `python3 scip_search.py S R D0 K0 MU0` for `(1,6,1,0,0.01)`, `(2,6,1,10,0.01)`, `(3,6,1,10,0.1)`, `(4,12,2,10,0)`, `(5,12,2,3,0)`, `(6,12,1,10,0.1)` | adversarial SCIP search under constraints | best `0.080`, `0.267`, `0.499`, `0.238`, `0.302`, `0.341` (`scip_search_*.log`) |
| `python3 scip_random.py 11 4000 MODE`, MODE = origin, far, antidiag, axis | random SCIP sampling | 15,731 corners; minima quoted in Section 4 (`scip_random_*.log.gz`, compressed in the second session) |
| `python3 certify_support_one.py` | Propositions C2, C3: exact certificates | ALL PASS for `d = 1/100, 1/1000, 1/10000` and `k = 1, 10, 100` (`certify_support_one.log`) |
| `python3 check_exactness.py 3 150` | Theorem C vs SDP on 150 random support-one corners | 150 agree (2 borderline where the SDP under-reports); 138 with `H_cyl ≥ 1`, all exact; max `H_cyl` among non-exact `0.456` (`check_exactness.log`) |

The first session also ran exploratory one-off scripts from `/tmp`; every
number it reported was reproduced by a logged script, except the two-variable
check of the `H = ∞` threshold (56.70–56.75), a one-off Nelder–Mead run that
agrees with `rhomax.py`.

### 8.2 Second session (2026-10-02)

All box searches were run as
`timeout 2400 python3 certify_zB.py RHO OUTFILE 2300 DEPTH [FAMILY]` and all
verifications as `python3 verify_zB.py OUTFILE RHO [FAMILY]`.

| command | purpose | actual outcome |
|---|---|---|
| `timeout 900 python3 certify_sharpA.py`, `certify_support_one.py`, `scip_bad_family.py`, `check_scip_bound.py 5 600` | rerun of the first session's exact certificates and SCIP checks | output byte-identical to the logs in `logs/` (compared with `diff`) |
| `timeout 2400 python3 certify_zB.py RHO ../logs/zB_cert/leaves_rhoRHO.jsonl 2300 MAXDEPTH` for `RHO = 200, 160` (depth 70), `140, 138` (80), `137` (90) | Theorem B2(1): box search | all 8 facets done in 14–78 s; 4,349 / 6,113 / 15,226 / 20,147 / 28,699 boxes (`logs/zB_cert/search_rho*.log`) |
| `python3 verify_zB.py ../logs/zB_cert/leaves_rhoRHO.jsonl.gz RHO`, same five `RHO` | exact verification and coverage | ALL LEAVES VERIFIED, ALL 8 FACETS COVERED for each (`logs/zB_cert/verify_rho*.log`). These five box files were written by an earlier version of `certify_zB.py` (header with `ρ` as a float, no family key); the current code reproduces the same 28,699 leaves for `ρ = 137` (Section 8.3) |
| `python3 certify_zB_lower.py` | Theorem B2(2), exact | ALL PASS, valid for `ε ≤ 24336/1330717441` (`logs/certify_zB_lower.log`) |
| `certify_zB.py RHO ... tan:1/1000:4` for `RHO = 21/20, 1, 99/100, 197/200` (depth 90–100), then `verify_zB.py` | Theorem B3(2) | all done; 1,300 / 2,706 / 4,443 / 11,132 boxes; ALL VERIFIED for each (`logs/zB_cert/*tan_eta1e-3_k4*`) |
| `certify_zB.py RHO ... tan:1/100:4` for `RHO = 6/5` | Theorem B3(3), first try | stopped at depth 100 near an `X` with `s̄` on the boundary of `B_X`; kept as `logs/zB_cert/search_tan_eta1e-2_k4_rho6_5_MAXDEPTH.log`. *Corrected after review round 1:* the bound tried here is false (exact (B) sets exist at `ρ = 1.2234 > 6/5` for `L ≥ 2.99`, Theorem B3(5)), so no method could certify it; the reviewed version wrongly blamed the closed relaxation (Section 6.3) |
| same for `RHO = 3/2, 13/10, 5/4`, then `verify_zB.py` | Theorem B3(3) | 732 / 1,283 / 1,882 boxes; ALL VERIFIED for each |
| `certify_zB.py RHO ... tan:1/1000:9/4` for `RHO = 1, 19/20` | Theorem B3(4), first tries | stopped at depth 100 near `X` with `s̄` and `P_2` on the boundary of `B_X`; logs kept as `*_MAXDEPTH.log`. *Corrected after review round 1:* the bounds tried here are false (exact (B) sets exist at `ρ = 1.0414 > 1` for `L ≥ 3.09`, Theorem B3(5)); the reviewed version wrongly blamed the closed relaxation (Section 6.3) |
| same for `RHO = 6/5, 11/10, 21/20`, then `verify_zB.py` | Theorem B3(4), `k = 9/4` | 2,927 / 4,634 / 10,705 boxes; ALL VERIFIED for each |
| `certify_zB.py 11/10 ... tan:1/1000:49/25`, then `verify_zB.py` | Theorem B3(4), `k = 49/25` | 11,943 boxes; ALL VERIFIED |
| `verify_zB.py` on all 16 compressed box files (loop over the files and parameters listed in `logs/zB_cert/verify_all.log`) | final re-verification from the `.jsonl.gz` files | 16 of 16: ALL LEAVES VERIFIED, ALL 8 FACETS COVERED (`logs/zB_cert/verify_all.log`) |
| `timeout 900 python3 scip_kD_family.py` | Proposition S3 | ALL PASS (symbolic); float cross-check in Section 4 (`logs/scip_kD_family.log`) |
| `timeout 3600 python3 tangent_family.py ETA K B` for `(ETA, K) = (0.001, 4), (0.01, 4), (0.001, 2.25)`, and `timeout 1800 ... 0.001 1.96 B 30` | numerics for Theorem B3 (rerun after the guard of Section 6.2, item 9; the first runs gave identical numbers for `k = 4`, and a meaningless `10^6` for `k = 2.25`) | table of Section 3.2; every returned (B) set passed the membership check (`logs/tangent_family_eta*.log`) |
| `explore/test_closed.py` | closed-form (B) membership vs the sfree-based test | 0 mismatches in 20000 (`logs/explore/test_closed.log`) |
| `explore/test_psi.py` | `max_h det` formula behind certificate (c) | max rel. error `1.4e-13` (`logs/explore/test_psi.log`) |
| `explore/sanity_zB.py 160`, `explore/sanity_zB.py 120` | direct random test of the Theorem B2 conditions | 0 and 46 of 2996 random `X` meet all conditions (`logs/explore/sanity_zB_rho*.log`) |
| `explore/relaxB2.py inf 100 130 135 138 140` and `inf 150 200 400 1000` (run from `/tmp` with the same script; logs copied) | Nelder–Mead on the relaxed (B) problem | slack positive up to 135, negative from 138 (`logs/explore/relaxB2_inf_*.log`) |
| `explore/check_scip_frame.py` | SCIP's set in its balanced frame | max deviation `2.05e-15` (`logs/explore/check_scip_frame.log`) |
| `explore/rank1_midpoint.py` | why the midpoints are needed in Theorem B2 | margins of Section 3.1 (`logs/explore/rank1_midpoint.log`) |
| `explore/tangent_explore.py`, `explore/tangent_explore2.py` | first runs with nearly tangent rays | `D·z_A ≈ 2.2` (`η = 0.01`, `k = 2`), `1.43` (`η = 10^-3`), `1.39` (`η = 10^-4`) at `D = 424` (`logs/explore/tangent_explore*.log`) |

*Process hygiene.* Every long run had a `timeout` wall-clock limit, and the
box searches append each certified box to their output file (a rerun skips
finished facets). At most four of my processes ran at once, except for about
one minute in which six ran; I killed two of them (heuristic runs for
`k = 1.5625` and `k = 1.44`, not reported). One exploratory Nelder–Mead job
(`relax_tan.py`) was too slow and was killed; nothing from it is reported.
Before this note was finished, every background process started in this
stream had ended: `ps` showed no process from this stream, and the only
Python processes left had working directories in other streams
(`orbit-closure`, `scip-rule-fidelity`, `scip-set-selection`,
`split-practice`, `research-20260929`).

### 8.3 Revision after review round 1 (2026-10-02)

Run from `code/` unless noted, with `OMP_NUM_THREADS=1` where an SDP solver is
used. New outputs are in `logs/rev1/`. These are targeted local checks; no
project-wide verification was run and CI was not consulted.

| command | purpose | actual outcome |
|---|---|---|
| `timeout 600 python3 certify_lower_found.py` | Theorem B2(2) at `ρ = 1367/10`; Theorem B3(5) | all five cases PASS, ALL PASS (`logs/rev1/certify_lower_found.log`) |
| `timeout 600 python3 certify_adv3_upper.py` and `timeout 600 python3 certify_adv3_upper.py 191/6250` | exact upper end of `z_A/z_K` on the near-boundary instance (minor issue 2a) | ALL PASS for `R = 153/5000` and `R = 191/6250`; float dual margins in the normalized frame: `1.9·10^-8` for `R = 153/5000`, `3.4·10^-9` for `R = 191/6250` (`logs/rev1/certify_adv3_upper.log`, `..._191_6250.log`) |
| `timeout 2400 python3 certify_zB.py 137 ../logs/rev1/leaves_rho137_rerun.jsonl 2300 90`, then `timeout 1500 python3 verify_zB.py ../logs/rev1/leaves_rho137_rerun.jsonl 137` (file compressed afterwards) | optional point O7 | all 8 facets done in 78 s, 28,699 leaves; ALL LEAVES VERIFIED, ALL 8 FACETS COVERED (`logs/rev1/search_rho137_rerun.log`, `verify_rho137_rerun.log`) |
| `timeout 300 python3 compare_leaves.py ../logs/zB_cert/leaves_rho137.jsonl.gz ../logs/rev1/leaves_rho137_rerun.jsonl.gz` | same leaves as the stored file? | 28,699 vs 28,699; identical facets, paths, certificate types and certificate data; only the header differs (`logs/rev1/compare_leaves_rho137.log`) |
| `timeout 300 python3 scip_random_minima.py` | optional point O3 | 15,731 corners; minimum `0.0140` with `D ≤ 2`; with `D ≤ 2`, `κ ≤ 10`: `0.2397` (Case-4 set) and `0.1823` (uncompleted set) (`logs/rev1/scip_random_minima.log`) |
| `timeout 900 python3 recheck_adv3.py`; `timeout 900 python3 certify_zB_lower.py` | reruns of the checks touched by minor issue 2 | output identical to `logs/recheck_adv3.log` and `logs/certify_zB_lower.log` (`diff`) |
| from `reviews/r1-code/`: `timeout 600 python3 exact_feasible_below.py` (the reviewer's script, run unchanged) | the exact check behind minor issue 1 | output identical to `reviews/r1-logs/exact_feasible_below.log`: ALL VALID |
| read-only `sed -n 1060,1215p` and `sed -n 1560,1700p` of SCIP 10.0.3 `scip/src/scip/nlhdlr_quadratic.c`, and `grep -n kappa` | scope statement (minor issue 3) | `kappa` is computed at lines 1151–1204; `xextra = wzlp + kappa + norm` at lines 1665–1666 |
| a first attempt, discarded: an SDP search for lower-bound sets whose eigenvalue margins were scaled by the matrix norms (`certify_lower_sdp.py`, deleted) | — | the margins fell below Clarabel's tolerance (about `10^-9`), and its bisection under-reported `ρ` (136.51 where 136.7 is certified); replaced by the exact check of the found sets; nothing from it is reported |

*Process hygiene in the revision.* At most two of my processes ran at once,
each with a `timeout`. The only background job (the `ρ = 137` rerun and its
verification) finished with exit code 0 before this note was finished, and
no process from this stream was left running. Temporary files in `/tmp`
were deleted.

## 9. Limits

- Theorems B2 and B3 are computer-assisted. Their certificates are checked in
  exact rational arithmetic by `verify_zB.py`, but the reduction from
  "no set contains the simplex" to the seven box conditions is a hand proof
  (Section 3.1), and the box geometry (`box_of`) is shared between the search
  and the verifier. Review round 1 re-derived the reduction by hand and
  re-verified all 16 box files with an independently written exact verifier
  (`reviews/review-r1.md`).
- The constant of Theorem A is within a factor 3.72 of the worst case
  (Theorem B3), but the exact worst-case constant is not known; the (A)
  constant on the family of Theorem B3 is still decreasing at `D = 2000`, and
  only a two-parameter family of configurations was tried.
- Proposition C3's "all sufficiently small `d`" gives no explicit range;
  exact certificates cover three values. (Theorem B(5) has no rate, but
  Theorem B2(1) now gives one.)
- The box searches use only necessary conditions (the seven conditions of
  Section 3.1, with `s̄ ∈ B_X` instead of `s̄ ∈ int B_X`), so a certified
  upper bound can lie above the true value. On the families computed the
  gap is now bracketed exactly: at most 0.22% for Theorem B2 (small `ε`) and
  0.06–2.2% for Theorem B3 (`L ≥ 3.4`). No case was observed in which the
  relaxation blocked a true bound. (The reviewed version cited three failed
  searches as such cases; at those `ρ` the bounds are false, Section 6.3.)
  The lower bounds of Theorem B3(5) hold for `L ≥ 3.4` only, and those of
  Theorem B2(2) for `ε ≤ ε_1` only.
- Theorem S's `κ` is measured in the given coordinates, because SCIP's rule
  is not affinely invariant. Its constant `1/√6 ≈ 0.408` is within a factor
  `2√6 ≈ 4.9` of Proposition S3.
- Scope of the SCIP part: only SCIP's Case 4 for a constraint that SCIP sees
  exactly as `w − xy` (`κ_S = 0`, coefficient 1 on `w`, no linear terms in
  `x`, `y`, no rescaling). Rescaling or shifting the constraint changes
  SCIP's set (Section 4, from reading the source), and Theorem S and
  Proposition S3 then do not apply as stated. SCIP's Case 2, the setting of
  sfree Proposition 6 named in the task, is not analysed beyond a remark.
- "SCIP's set" is the reimplementation `ms_set`, checked against the Case-4
  formulas in the SCIP source by reading, not by extracting cuts from SCIP.
  Monoidal strengthening and SCIP's numerical safeguards are ignored. The
  corners of Proposition S3 have `w̄ = −1` exactly; how often SCIP meets
  nearby corners in practice was not tested.
- Theorem C covers support-one minimizers with transversal edges and, through
  sfree Lemma 13, tangent edges; degenerate contacts (an edge tangent at a
  support-one `t*`, ties) are not treated.
- Everything is single-cut and single-constraint; nothing here says how the
  rules compare after LP re-solves or over several rounds (see the
  `multiround` stream).

## 10. Open questions

1. The exact worst-case constant `C*` (Section 3.2), for (A) and for (B):
   now known to lie in `[0.414, 1.54]` (Theorems A, B3); numerically about
   1.4–1.5 for (A) with nearly tangent rays. Which configuration is worst,
   and does the limit problem have a closed form?
2. With a fixed grazing margin `μ`, Corollary A' gives the constant
   `1/(γ + sqrt(1 + γ²))`; the best upper bounds are 2.5 for `μ = 0.01`
   (Theorem B3) and about 194 for `μ = 1` (Theorem B2). What is the right
   dependence on `μ`?
3. Can SCIP's rule be repaired cheaply, for example by replacing the
   constant `+1` with a scale taken from the corner, or by choosing the
   rotation angle (the one free parameter of SCIP's family) by a
   one-dimensional search for the deepest cut? I did not check whether either
   removes the `κD` loss of Proposition S3; whether it would matter on real
   instances is a question for the `scip-set-selection` stream.
4. Is the interval test of Theorem C(3) also exact for family (B) with the
   lowered intervals, and is there a similar one-dimensional test for (B) at
   tangent edges? In the boundary case that Theorem C(3) leaves open (the
   closed intervals meet, but never in the interior of `I_s̄(α)`), is
   `z_A = z_K`?
5. Does a depth bound like Theorem A hold for the minor sets of signature
   `(2, 2)` used for implied minors (the `minor-sets` stream), where the slice
   `h = 1` is replaced by a homogeneous cone?
6. SCIP's Case 2 (the setting of sfree Proposition 6, `κ_S = 1`): does a
   grazing margin or a conditioning bound keep its single-cut ratio away
   from 0? Proposition 6 violates both conditions, so it does not decide
   this (Section 4). Relatedly, how much do rescaling or shifting the
   constraint change SCIP's Case-4 ratio on corners like those of
   Proposition S3?
