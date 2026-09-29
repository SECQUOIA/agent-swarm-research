# A priori integrality-gap bounds for shortest paths in graphs of convex sets

Date: 2026-09-28; revised 2026-09-29. Status: research note with complete
proofs of the stated theorems and targeted numerical checks. It was revised
after the independent [review](../reviews/gcs-review.md) and the
[recheck](../reviews/gcs-recheck.md); §11 lists the changes. No
publication-priority claim is made; see the novelty caution in §9.

This note audits and extends the first-pass results of the scout report
[graphs-of-convex-sets](../scouting/graphs-of-convex-sets.md). Code and
outputs are in [`code/`](code/). Section numbers of the scout's statements
("scout Theorem 1", "scout Prop. 5", ...) refer to that report.

## Summary

**Proved (acyclic graphs, no edge constraints).**

- **Theorem 1.** For any feasible point of the relaxation `REL_H` (the
  perspective relaxation strengthened by vertex-local convex hulls), a Markov
  chain driven by the hull's edge-pair variables produces a random path whose
  expected cost is at most `Σ_e y_e cav_e(z̄_e, z̄'_e)`, where `cav_e` is the
  concave envelope of the edge length. A shortest path in the pair graph
  achieves this deterministically. Hence `OPT − REL_H ≤ max_P Σ_{e∈P} Δ_e`,
  where `Δ_e` is the maximal Jensen defect of edge `e`. This confirms scout
  Theorem 1.
- **Affine lengths:** `REL_H = OPT`. The basic relaxation `REL` can be `0`
  while `OPT = 2`, even with nonnegative affine lengths.
- **Sublinear lengths `g_e(x'−x)`:** `OPT ≤ κ_max·REL_H`, and for Euclidean
  lengths `κ_e = sec θ_e`, where `θ_e` is the aperture (half-angle of the
  narrowest circular cone) of `X_v − X_u`. The scout's finiteness condition
  was wrong in one direction and is corrected. An explicit family shows the
  excess constant is at least `1/2`; the exact constant is open.
- **Squared lengths:** the exact per-edge constant is
  `κ^sq_e = sec²θ*_e`, where `θ*_e` is the smallest angular radius (seen from
  the origin) of a ball containing `X_v − X_u`. It is computable by a convex
  program, and `κ^sq_e ≥ κ_e²`. The scout's Kantorovich bound is a valid upper
  bound on the same quantity, so it is never better; for balls it gives
  `sec⁴θ` against the exact `sec²θ`. This explains the Euclidean/squared
  difference: norm lengths lose only through angular dispersion, squared
  lengths lose its square plus radial (step-length) dispersion. Even 1D instances with disjoint intervals have
  gaps under squared lengths, but not under Euclidean lengths.
- **REL versus REL_H:** a `REL` point always extends to the hull at a vertex
  whose set is a simplex or whose in- or out-degree is one. For every
  non-simplex set, some configuration with enough edges does not extend.
  `REL` is first-order tight in set size over separation, `REL_H`
  second-order; closed forms confirm both orders on the scout's crossing
  family.

**Proved (extensions).**

- **Cyclic graphs (Theorem 5).** For any nonnegative convex lengths, the
  same chain gives an s–t *walk* with cost at most `Σ y cav`, without degree
  constraints. So `REL_H` bounds the shortest-walk problem from both sides.
  Paths follow when a common convex quasi-metric defines all lengths, such as
  a common norm. Without that, the path statement fails even with degree
  constraints and the hull: an explicit squared-length instance has
  `Σ y cav = 3/2 < OPT = 2`.
- **Edge constraints.**
  - *Negative (Prop. 6).* With translation constraints `x_v = x_u + c`, an
    acyclic 1D instance with pairwise-disjoint sets is infeasible, yet
    `REL = REL_H = 0` is attained. Set separation is therefore not the
    governing parameter.
  - *Positive (Theorem 7).* Identification-type constraints (continuity of
    Bézier control points, one-step-controllable linear dynamics) are removed
    exactly by a line-graph ("door") reformulation. The condition is that the
    entry and exit blocks of each vertex set be independent. Theorem 1 then
    applies. The basic relaxation of the reformulation dominates the original
    hull relaxation.
- **Overlapping covers.**
  - *Negative.* No multiplicative bound exists: `REL_H = 0 < OPT = 2` in 1D
    (Prop. 8). In the order-1 region formulation used for motion planning,
    `REL = REL_H = |goal − start| = 3` while `OPT = 2 + 2√(H² + 1/4)` on a
    ring around a wall of half-height `H` (Prop. 9). Two-cycle cuts and the
    region hull do not change this. The same holds numerically for cubic
    Bézier `C¹` segments.
  - *Checkable parameters that do give bounds.* Three are proved:
    - the additive Jensen/radius bound `OPT − REL_H ≤ Λ·max_P Σ (R_u + R_v)`
      on acyclic graphs;
    - the detour ratio `OPT/REL ≤ OPT/|goal − start|` for the region
      formulation, attained on the ring family;
    - the door aperture: `OPT ≤ sec θ_door · REL_H,door` for the door
      formulation. On the ring family `sec θ_door = 1.118` for every `H ≥ 1`
      (larger for `H < 1`), and the door relaxation is numerically exact
      there, while the region formulation is unbounded.
- **Hardness (§7).**
  - In fixed dimension, separated instances admit a `(1 + ε)`-approximation
    in time polynomial in `|V|`, `|E|` and `(1 + D√n/(εδ))^n`. The product
    graph has up to `|E|·M²` arcs for nets of size `M`, so the dependence is
    `(1 + D√n/(εδ))^{2n}`. This is a PTAS when the ratio of set diameter to
    separation, `D/δ`, is bounded.
  - In growing dimension, for every fixed aperture `θ`, approximating within
    `1 + tan²θ/(4N(m+1)²)` is NP-hard (3SAT with `N` variables, `m` clauses),
    with pairwise-disjoint polytopes.
  - Whether `1 + cθ²` is NP-hard (scout Q2) remains open. §7.3 identifies
    the obstacle: cheap spreading of state changes across layers.

**Open or conjectural (labelled in the text).**

- The exact worst-case constant in `OPT/REL_H − 1 ≲ c·(sec θ_max − 1)`; we
  show `1/2 ≤ c ≤ 1`.
- Whether generalized subtour cuts restore the path version on cyclic graphs.
- Boundedness of the region-formulation gap for simply connected planar
  covers.
- Underactuated dynamics.
- The `1 + cθ²` hardness threshold.

All numerical checks agree with the proofs: no stated inequality was
violated in several hundred checked instances or in a few thousand
adversarial evaluations (§8).

## 1. Setting and formulations

**Data.**

- A digraph `G = (V, E)` with distinct `s, t`, where `in(s) = out(t) = ∅`.
- For each `v`, a nonempty compact convex set `X_v ⊂ R^{n_v}`.
- For each `e = (u, v)`, a convex length `ℓ_e : K_e := X_u × X_v → R` that is
  bounded above on `K_e` (for example continuous).
- Optionally, a compact convex edge-constraint set `X_e ⊆ K_e`.

A path visits distinct vertices. `OPT` is the minimum of
`Σ_{e∈p} ℓ_e(x_u, x_v)` over s–t paths `p` and positions `x_v ∈ X_v` with
`(x_u, x_v) ∈ X_e`.

**Perspectives.** For compact convex `X`, let `X̃ := {(z, λ) : λ ≥ 0, z ∈ λX}`;
`λ = 0` forces `z = 0`. Define `ℓ̃_e(z, z', y) := y·ℓ_e(z/y, z'/y)` for `y > 0`
and `ℓ̃_e(0, 0, 0) := 0`. Boundedness of `ℓ_e` makes `ℓ̃_e` lower
semicontinuous at `y = 0`.

**REL** (SIOPT 2024 eq. (5.5); thesis (9.5)). Variables `y_e ≥ 0`, `z_e`,
`z'_e`:

```
(F)  Σ_{out(s)} y = 1 = Σ_{in(t)} y,   Σ_{in(v)} y = Σ_{out(v)} y   (v ≠ s, t)
(D)  Σ_{in(v)} y ≤ 1                                                  [degree; optional]
(P)  (z_e, y_e) ∈ X̃_u,  (z'_e, y_e) ∈ X̃_v,  (z_e, z'_e, y_e) ∈ X̃_e   [last only with edge constraints]
(C)  Σ_{in(v)} z'_e = Σ_{out(v)} z_f                                  (v ≠ s, t)
min  Σ_e ℓ̃_e(z_e, z'_e, y_e).
```

The lifted degree constraint `(x_v − z_v, 1 − y_v) ∈ X̃_v` with a free `x_v`
is vacuous, as thesis §9.3 notes.

**REL_H.** For every `v ∉ {s, t}` with `in(v), out(v) ≠ ∅`, add variables
`λ_ef ≥ 0` and `w_ef` for `e ∈ in(v)`, `f ∈ out(v)`:

```
(H1) (w_ef, λ_ef) ∈ X̃_v
(H2) Σ_f λ_ef = y_e,  Σ_f w_ef = z'_e   (e ∈ in(v));   Σ_e λ_ef = y_f,  Σ_e w_ef = z_f   (f ∈ out(v)).
```

The polytope `Y_v = {y ≥ 0 : Σ_in y = Σ_out y ≤ 1}` of flows through `v` has
vertices `0` and `1_e + 1_f`. So (H) is the projection of the disjunctive
convex hull of thesis Lemma 8.2 / SIOPT (7.4) at `v`. (H) implies (C) and the
vertex parts of (P). An s–t path gives a feasible point (`λ_ef = 1` on its
consecutive pairs, `w_ef = x_v`) of equal cost. Hence `REL ≤ REL_H ≤ OPT` in
every setting considered here.

**Notation.**

- Barycenters: `z̄_e = z_e/y_e`, `z̄'_e = z'_e/y_e`, `w̄_ef = w_ef/λ_ef` when
  the denominators are positive.
- **Concave envelope:** `cav_e(k) := sup{Σ_i p_i ℓ_e(k_i) : k_i ∈ K_e, p a
  probability vector, Σ_i p_i k_i = k}`.
- **Maximal Jensen defect:** `Δ_e := sup_{K_e}(cav_e − ℓ_e) ∈ [0, ∞)`.
- For a polytope `K_e` and convex `ℓ_e`, the supremum may be restricted to
  vertices of `K_e`. Then `cav_e(k)` is an LP, and `Δ_e` is a concave
  maximization over vertex weights. This is how both are computed in §8.
- **Boundary conventions.** For `e ∈ out(s)`, write the single "previous
  state" as `∗` with `λ_{∗e} := y_e`, `w̄_{∗e} := z̄_e`. For `e ∈ in(t)`, write
  `λ_{e∗} := y_e`, `w̄_{e∗} := z̄'_e`.

## 2. Theorem 1: Jensen-defect rounding on acyclic graphs

**Theorem 1.** Let `G` be acyclic without edge constraints. Let
`(y, z, z', λ, w)` be feasible for `REL_H`, with or without (D).

1. **Markov chain.** Choose the first edge `f ∈ out(s)` with probability
   `y_f`. After traversing `e = (u, v)` with `v ≠ t`, choose `f ∈ out(v)`
   with probability `λ_ef/y_e`. Place `s` at `z̄_f` (first edge `f`), each
   internal visited `v` at `w̄_ef` (entered by `e`, left by `f`), and `t` at
   `z̄'_e` (last edge `e`). This gives a random s–t path `P` with positions in
   the sets, and:
   - `Pr(e ∈ P) = y_e`;
   - `Pr(d, e consecutive in P) = λ_de`;
   - given `e ∈ P`, the previous and next edges are independent with laws
     `λ_de/y_e` and `λ_ef/y_e`;
   - `E[x_u | e ∈ P] = z̄_e` and `E[x_v | e ∈ P] = z̄'_e`.
2. **Expected cost.** The expected cost satisfies
   ```
   E[cost] = Σ_e Σ_{d,f} (λ_de λ_ef / y_e) · ℓ_e(w̄_de, w̄_ef)  ≤  Σ_{e: y_e>0} y_e · cav_e(z̄_e, z̄'_e).
   ```
3. **Deterministic rounding.** Build the *pair graph*:
   - nodes are the consecutive pairs `(d, e)` with `λ_de > 0` (including
     `(∗, e)` and `(e, ∗)`);
   - arcs join `(d, e) → (e, f)` with cost `ℓ_e(w̄_de, w̄_ef)`.

   Its shortest path from the `(∗, ·)` nodes to the `(·, ∗)` nodes is an s–t
   path of `G` with positions and cost at most `E[cost]`. The pair graph is
   acyclic and has at most `Σ_v |in(v)||out(v)| + |out(s)| + |in(t)|` nodes.

**Consequently**, at an optimal `REL_H` point,

```
OPT − REL_H ≤ Σ_e y_e (cav_e − ℓ_e)(z̄_e, z̄'_e) ≤ Σ_e y_e Δ_e ≤ max_{s–t paths P} Σ_{e∈P} Δ_e.     (1)
```

*Proof.*

- **Termination.** Every `e` chosen has `y_e > 0`, since `λ_de ≤ y_e` by (H2)
  and nonnegativity. If `v = head(e) ≠ t`, then `Σ_f λ_ef = y_e > 0`, so a
  next edge exists. Since `G` is acyclic, the walk never revisits a vertex and
  stops only at `t`.
- **Marginals.** Induct along a topological order. For `f ∈ out(s)`,
  `Pr(f ∈ P) = y_f`. For `f ∈ out(v)`, `v ≠ s`, the events `{e ∈ P}`,
  `e ∈ in(v)`, are disjoint because `v` is visited at most once. The next
  edge depends only on the entering edge. So
  `Pr(f ∈ P) = Σ_e Pr(e ∈ P) λ_ef/y_e = Σ_e λ_ef = y_f`, and similarly
  `Pr(d, e consecutive) = y_d · λ_de/y_d = λ_de`.
- **Conditional independence.** Given `e ∈ P`, the previous edge `d` has
  probability `λ_de/y_e`. By the Markov property, the next edge is
  independent of the past, with law `λ_ef/y_e`.
- **Conditional means.** By (H2) at `v = head(e)` and at `u = tail(e)`,
  `E[x_v | e ∈ P] = Σ_f λ_ef w̄_ef / y_e = z'_e/y_e` and
  `E[x_u | e ∈ P] = Σ_d λ_de w̄_de / y_e = z_e/y_e`. The boundary conventions
  cover `s` and `t`.
- **Jensen step.** Given `e ∈ P`, the pair `(x_u, x_v)` takes finitely many
  values in `K_e` with mean `(z̄_e, z̄'_e)`. By the definition of `cav_e`,
  `E[ℓ_e(x_u, x_v) | e ∈ P] ≤ cav_e(z̄_e, z̄'_e)`. Summing with weights
  `Pr(e ∈ P) = y_e` gives part 2.
- **Derandomization.** The chain's paths are paths of the pair graph, with
  pair-graph cost equal to the rounded cost. The minimum over pair-graph paths
  is at most the expectation. Re-optimizing positions on the chosen path can
  only lower the cost.
- **Consequences.** `REL_H = Σ_e y_e ℓ_e(z̄_e, z̄'_e)` at the optimal point
  gives (1). The last inequality of (1) follows because a unit s–t flow in a
  DAG decomposes into s–t paths, and `Δ_e ≥ 0`. ∎

**Remarks.**

- **Hypotheses.**
  - Acyclicity is used only for termination and the marginal identities
    (§4 treats cycles).
  - Degree constraints are not used, nor is `ℓ ≥ 0`.
  - Finiteness of `cav_e` needs `ℓ_e` bounded above on `K_e`; otherwise (1)
    is vacuous.
- **A posteriori version with edge constraints.** If a `REL_H` point
  satisfies `(w̄_de, w̄_ef) ∈ X_e` for all `d, f` with positive `λ`, every
  rounded pair is feasible, and Theorem 1 holds at that point. This can be
  checked after solving.
- **Vertex costs** charged per pair, `Σ f̃_v(w_ef, λ_ef)`, are paid exactly by
  the rounding and add no defect.
- **Where the hull is needed.** By Proposition 2, the hull variables are only
  needed at vertices whose set is not a simplex and that have in- and
  out-degree at least two in `supp y`. Elsewhere a `REL` point extends to
  `REL_H` at no cost. In particular, Theorem 1 applies verbatim to `REL` in
  one dimension.
- **Relation to the scout's statement.** Scout Theorem 1 is correct as
  stated for acyclic graphs. Two gaps in its sketch are filled here: the
  conditional-independence step behind the closed-form expectation, and the
  explicit pair-graph construction.

**Corollary 1.1 (additive a priori bound).** Under Theorem 1,
`OPT − REL_H ≤ max_P Σ_{e∈P} Δ_e`, computable by a longest-path DP on the DAG
from the `Δ_e`. Suppose `ℓ_e(x, x') = g_e(x' − x)` with a norm
`g_e ≤ Λ‖·‖₂`. Let `R_v` be the Euclidean circumradius of `X_v`. Then
`Δ_e ≤ Λ(R_u + R_v)`, so

```
OPT − REL_H ≤ Λ · max_P Σ_{e=(u,v)∈P} (R_u + R_v).     (2)
```

*Proof.* Let `(X, X')` have mean `(a, b)` in `K_e`. Then
`g(X' − X) ≤ g(b − a) + g(X' − b) + g(a − X)`. Also
`E‖X − a‖₂ ≤ (E‖X − a‖²)^{1/2} = (E‖X − c‖² − ‖a − c‖²)^{1/2} ≤ R_u` for the
circumcenter `c` of `X_u`, and similarly for `X'`. ∎

Bound (2) holds for arbitrarily overlapping sets. It is first order in set
size, and §6 shows that first order is unavoidable under overlap.

## 3. Corollaries and separations

### 3.1 Affine lengths

**Corollary A.** If `G` is acyclic and every `ℓ_e` is affine on `K_e`, then
`REL_H = OPT`. `OPT` is computable in polynomial time by a shortest path in
the pair graph, given support-function oracles for the sets.

*Proof.* `cav_e = ℓ_e`, so (1) gives `OPT ≤ REL_H`. Alternatively, write
`ℓ_e = c_e·x + d_e·x' + b_e`. Substituting (H2) turns the `REL_H` objective
into `Σ_{v,e,f} (d_e + c_f)·w_ef + Σ b_e y_e`. Minimizing over
`w_ef ∈ λ_ef X_v` gives `λ_ef·(−h_{X_v}(−(d_e + c_f)))`, where `h` is the
support function. What remains is the flow LP of a shortest path in the pair
graph, which is integral. ∎

**Proposition A′ (REL fails for affine lengths).**

- **Instance:**
  - Vertices `s, u1, u2, w1, w2, t`, each the point `{0}` in `R²`, and
    `X_v = [−1, 1]²`.
  - Edges `s→u_i`, `u_i→v`, `v→w_j`, `w_j→t`.
  - Nonnegative affine lengths `ℓ_{u1 v} = 2 − (x1 + x2)`,
    `ℓ_{u2 v} = 2 + x1 + x2`, `ℓ_{v w1} = 2 − (x1 − x2)`,
    `ℓ_{v w2} = 2 + x1 − x2`, and `0` on the other edges.
- **Values:** `REL = 0` and `REL_H = OPT = 2`.

*Proof.*

- *OPT.* Each of the four paths costs `4 ∓ 2x_1` or `4 ∓ 2x_2`, with minimum
  `2`.
- *REL.* The point `y ≡ 1/2` with `z̄'_{u1v} = (1,1)`, `z̄'_{u2v} = (−1,−1)`,
  `z̄_{vw1} = (1,−1)`, `z̄_{vw2} = (−1,1)` satisfies (C) (both sides are `0`)
  and costs `0`. Since the lengths are nonnegative, `REL ≥ 0`.
- *REL_H.* Corollary A gives `REL_H = 2`. ∎

The scout's Exp 14 had `REL = −4` against `OPT = −2`, an additive shift of
this instance; with nonnegative lengths the ratio is infinite.

**Novelty.** Corollary A is a straightforward consequence of network-flow
integrality once `w` is eliminated. It is in the spirit of dynamic-programming
extended formulations (Martin–Rardin–Campbell 1990) and of the Ceria–Soares
observation that hull relaxations are exact for linear objectives. It should
not be claimed as new.

### 3.2 Sublinear lengths and apertures

**Corollary B.** Let `ℓ_e(x, x') = g_e(x' − x)` with `g_e` sublinear, and let
`D_e := X_v − X_u`. Define

```
κ_e := inf{κ ≥ 1 : ∃ a ∈ ∂g_e(0) with g_e(w) ≤ κ·aᵀw for all w ∈ D_e}   (∞ if no such κ).
```

Then `cav_e(x, x') ≤ κ_e g_e(x' − x)` on `K_e`, and under Theorem 1, if every
`g_e ≥ 0` (for example norms),

```
OPT ≤ Σ_e κ_e · ℓ̃_e(z_e, z'_e, y_e) ≤ κ_max · REL_H.     (3)
```

*Proof.* For random `W ∈ D_e`,
`E g(W) ≤ κ aᵀ E W ≤ κ g(E W)`, since `a ∈ ∂g(0)` means `aᵀw ≤ g(w)`. This
passes to `κ_e` by compactness of `∂g(0)`. The first inequality of (3) then
follows from Theorem 1. The second needs `ℓ̃_e ≥ 0`: a linear `g_e` that is
negative on `D_e` has `κ_e = 1`, and an exact instance with `REL_H < 0` and
`κ_max > 1` would violate it. ∎

**Properties.**

1. **`κ_e = 1` implies affine.** If `κ_e = 1`, a limit point `a*` gives
   `g_e = a*ᵀ(·)` on `D_e`, so `ℓ_e` is affine on `K_e`. The `κ = 1` cases of
   (3) are thus covered by Corollary A. Examples:
   - `ℓ1` lengths when `D_e` lies in one closed orthant (take `a` = the sign
     vector), as the scout stated;
   - `α w⁺ + β w⁻` in 1D when `X_u ∩ X_v = ∅`.
2. **Euclidean norm.** `κ_e = sec θ_e`, where
   `θ_e := min_{‖a‖=1} max_{w∈D_e∖0} ∠(a, w)` is the aperture of `D_e`.
   - *Proof.* For a unit axis `a`, `aᵀw ≥ cos θ ‖w‖`. Conversely, any `a` with
     `‖a‖ ≤ 1` and `‖w‖ ≤ κ aᵀw` on `D_e` has its direction within
     `arccos(1/κ)` of every `w`.
   - *Correction to the scout.* `κ_e` is finite iff `θ_e < π/2`.
     `X_u ∩ X_v = ∅` suffices, since then `0 ∉ D_e` and compactness gives a
     separating direction. It is **not necessary**: for `X_u = {0}` and `X_v`
     a segment starting at `0`, `κ_e = 1`. The scout's "finite iff
     `X_u ∩ X_v = ∅`" is wrong in the "only if" direction.
3. **Balls.** For balls `X_u = B(c_u, r_u)` and `X_v = B(c_v, r_v)`,
   `D_e = B(c_v − c_u, r_u + r_v)` and `sin θ_e = (r_u + r_v)/‖c_v − c_u‖`.
   **The per-edge bound is sharp:** `sup_{K_e} cav_e/ℓ_e = sec θ_e`.
   - *Proof.* Mix the two tangent points of `D_e` seen from `0` with weights
     `1/2`. Each has norm `√(d² − ρ²)`, where `d = ‖c_v − c_u‖` and
     `ρ = r_u + r_v`. Their mean has norm `(d² − ρ²)/d`, and the ratio is
     `sec θ_e`.
   - Each boundary point of `D_e` with outer normal `ν` lifts uniquely to
     `(c_u − r_u ν, c_v + r_v ν) ∈ K_e`.

**Proposition B′ (lower-bound family; the constant is at least 1/2).**

- **Instance:** `A = B(0, r)` in `R²`, `s = (−D, 0)`, `sin θ = r/D`, and
  `u_± = (cos θ, ± sin θ)`. Set `P_± = s + 2√(D² − r²)·u_±`. Reflect `A` and
  `s` in the vertical line through `P_±` to obtain `B` and `t`. Edges are
  `s→A`, `A→P_±`, `P_±→B`, `B→t`.
- **Values:** every edge has aperture exactly `θ`, and
  ```
  OPT = 4√(D² − r²),   REL_H ≤ 2(D² − r²)/D + 2√(D² − r²),
  OPT/REL_H − 1 ≥ tan²(θ/2),   (OPT/REL_H − 1)/(sec θ − 1) ≥ cos θ/(1 + cos θ) → 1/2.
  ```

*Proof.*

- *Apertures.* Since `|P_± − 0|² = D² + 4(D² − r²) − 4√(D² − r²)·D cos θ = D²`,
  edges `A→P_±` have `sin θ_e = r/D`; the other edges follow by symmetry.
- *OPT.* The segment `s P_+` is tangent to `A` at `T_+ = s + √(D² − r²) u_+`,
  so the path through `x_A = T_+` and the mirror point is straight on each
  half. Any path costs at least `|sP| + |Pt|`.
- *REL_H.* At `A` (in-degree 1), take pair points `T_±` with weights `1/2`.
  The arrival mean lies on the axis at distance `(D² − r²)/D` from `s`, and
  `A→P_±` costs `√(D² − r²)`. The same holds mirrored at `B`. ∎

**Exact relaxation value of the family.** By the reflection symmetry
`x_2 ↦ −x_2` and convexity, some optimal `REL_H` point is symmetric. Since `A`
has in-degree 1 and `B` out-degree 1, the hull is canonical. Hence

```
REL_H = 2 · min_{p ∈ A} ( p_1 + D + ‖P_+ − p‖ ),
```

a two-dimensional minimization over the disk. Its value is below the explicit
point of the proof, so the ratio slightly exceeds `cos θ/(1 + cos θ)`.

**Series.** Scale to `D = 1`. Then `P_+ = (cos 2θ, sin 2θ)` and `A` is the disk
of radius `sin θ`. The minimand `p_1 + ‖P_+ − p‖` has no interior stationary
point, because `P_{+,2} = sin 2θ > sin θ`. So the minimum is on the circle,
`p = sin θ (cos φ, sin φ)`. Write `φ = π/2 + ψ`. Then

```
g(ψ) = −sin θ sin ψ + √(1 + sin²θ − 2 sin θ sin(2θ − ψ)).
```

- Expanding in `θ` with `ψ = a θ + O(θ³)`, the `θ⁴` coefficient
  `(4a² − 4a + 3)/8` is minimized at `a = 1/2`. The `θ³` term of `ψ` affects
  only order `θ⁸`.
- This gives `min g = 1 − 3θ²/2 + θ⁴/4 − 3θ⁶/320 + O(θ⁸)`, and hence
  ```
  (OPT/REL_H − 1)/(sec θ − 1) = 1/2 + θ⁴/64 + O(θ⁶),
  ```
  with `OPT = 4cos θ` and `REL_H = 2(1 + min g)`. The series was checked with
  SymPy; odd orders vanish by symmetry.
- The optimal relaxed pair point sits at polar angle
  `π/2 + θ/2 + θ³/16 + …`, halfway to the tangent point `π/2 + θ`.
- 60-digit evaluation of the exact formula gives
  `(ratio − 1/2)/θ⁴ = 0.0156250` at `θ = 0.0025` rad, against
  `1/64 = 0.015625`.

This expansion was first derived in the recheck
([reviews/gcs-recheck.md](../reviews/gcs-recheck.md) §4); the derivation above
is my own.

Exact values of the ratio at finite `θ` (from the formula; the full `REL_H`
solves in t3b agree to about `10⁻⁶`):

| `θ` | 10° | 20° | 23.578° | 30° |
|---|---|---|---|---|
| ratio | 0.5000147 | 0.5002455 | 0.5004848 | 0.5013356 |

Over `10°–30°` the effective value of `(ratio − 1/2)/θ⁴` is `0.0158–0.0178`.
For `θ ≤ 6°`, the t3b solves resolve the excess only to solver noise
(`≤ 4·10⁻⁶`).

Two errors of the first version are corrected here:

- It reported `0.5000` to four digits up to `23.6°`.
- Its script built the balls with radius `r + 10⁻³` and divided by a
  numerically computed `κ_max`.

The seeded local search (at `θ = 11.5°`, scored with numerical `κ_max`) found
no better perturbation. Random-start searches over four other templates found
at most `0.20` (t3). None of this affects `c* ≥ 1/2`, since `c*` is
asymptotic. The scout's `0.499` is this phenomenon.

**Open Question 1.** Let `c*` be the best constant in
`OPT/REL_H − 1 ≤ c*(sec θ_max − 1)(1 + o(1))` as `θ_max → 0`. We have
`1/2 ≤ c* ≤ 1`.

- Full loss on every edge would require the realized positions on every edge
  to sit at tangent points seen from both ends.
- In the configurations we analysed (a two-in, two-out ball vertex with far
  neighbours), these requirements conflict at small `θ`.

This suggests `c* < 1`. It is a heuristic, not a proof.

### 3.3 Squared lengths

Let `ℓ_e = ‖x' − x‖²`, `q := ‖·‖²`, and
`κ^sq_e := sup_{w∈D_e∖0} cav_{D_e}(q)(w)/q(w)`. Any measure on `K_e` pushes
forward to a measure on `D_e` with the corresponding mean. Hence
`cav_e(x, x') ≤ cav_{D_e}(q)(x' − x) ≤ κ^sq_e ‖x' − x‖²`, and
`OPT ≤ Σ κ^sq_e ℓ̃_e ≤ κ^sq_max REL_H`.

**Corollary C (exact squared-length constant).** Let `0 ∉ D_e`. Then

```
κ^sq_e = inf{ ‖c‖²/(‖c‖² − ρ²) : D_e ⊆ B(c, ρ), ρ < ‖c‖ } = sec²θ*_e = 1/(1 − τ*_e),
τ*_e  := min_u  max_{w ∈ ext D_e} ( ‖w‖²‖u‖² − 2wᵀu + 1 ).
```

Here `θ*_e` is the smallest angular radius, seen from the origin, of a ball
containing `D_e` (`sin θ_B := ρ/‖c‖`). The program for `τ*_e` is convex, a
finite maximum of convex quadratics when `X_u, X_v` are polytopes, since then
`ext D_e ⊆ ext X_v − ext X_u`. So `κ^sq_e` is computable in time polynomial
in the number of vertex pairs; for balls it has a closed form.

*Proof.*

- **Upper bound.** Let `B(c, ρ) ⊇ D_e` with `ρ < ‖c‖`, and put `d := ‖c‖`.
  - The affine function `α(w) := 2cᵀw + ρ² − d²` satisfies
    `α − q = ρ² − ‖w − c‖² ≥ 0` on the ball, with equality on the sphere. So
    `cav_{D_e}(q) ≤ α` on `D_e`.
  - For fixed `‖w‖`, `cᵀw` is largest on the axis, and every norm attained in
    the ball is attained on the axis. So `max_B α(w)/‖w‖²` is a
    one-dimensional maximum. It is attained at `t = (d² − ρ²)/d ∈ [d − ρ, d + ρ]`
    with value `d²/(d² − ρ²)`.
- **Reparametrization.** Substitute `u := c/‖c‖²`. Then
  `‖w − c‖²/‖c‖² = ‖w‖²‖u‖² − 2wᵀu + 1 =: f_w(u)`, so `D_e ⊆ B(c, ρ)` iff
  `max_{w∈D_e} f_w(u) ≤ ρ²/‖c‖²`.
  - For fixed `u`, `w ↦ f_w(u)` is convex, so the maximum is attained on
    `ext D_e`. Hence the infimum over balls equals `1/(1 − τ*_e)`.
  - `τ*_e < 1 = f_w(0)` iff `0 ∉ D_e`: take `u = εa` with `a` strictly
    separating `0` from `D_e`.
- **Lower bound.** `F(u) := max_{w∈cl ext D_e} f_w(u)` is convex and
  coercive, so it has a minimizer `u* ≠ 0`.
  - By Danskin's theorem and Carathéodory, there are active points `w_i`
    (`f_{w_i}(u*) = τ*`) and weights `μ_i ≥ 0` with `Σ μ_i = 1` and
    `Σ μ_i ∇f_{w_i}(u*) = 0`.
  - Since `∇f_w(u) = 2‖w‖²u − 2w`, this gives `w̄ := Σ μ_i w_i = S u*` with
    `S := Σ μ_i ‖w_i‖²`. Averaging the active equalities gives
    `τ* = S‖u*‖² − 2S‖u*‖² + 1 = 1 − S‖u*‖²`.
  - The mixture `Σ μ_i δ_{w_i}` lies in `D_e` with mean `w̄ ∈ D_e`, and
    `Σ μ_i q(w_i)/q(w̄) = S/(S²‖u*‖²) = 1/(1 − τ*)`. Hence
    `κ^sq_e ≥ 1/(1 − τ*)`. ∎

This strengthens the first version's enclosing-ball bound, which was stated
for a fixed ball, to an equality. The proof follows the review's §4; I
re-derived it and checked it numerically (t10).

**Consequences.**

1. **Balls.** For balls `D_e`, `κ^sq_e = sec²θ_e`; for balls `X_u, X_v`,
   `sin θ_e = (r_u + r_v)/‖c_v − c_u‖`.
   - This is not an "only if". The lower bound `κ^sq_e ≥ sec²θ_e`
     (Consequence 3) is attained by some non-balls too.
   - Example: the chord between the two tangent points of the ball with
     `d = 1`, `ρ = 1/2`. Its endpoints `(3/4, ±√3/4)` mix to `(3/4, 0)`, giving
     `κ^sq = 4/3 = sec²30°`.
2. **Radial segments.** For `D_e = {tu : m ≤ t ≤ M}`, `κ^sq_e = (M + m)²/(4Mm)`.
   The best ball has centre `(M + m)u/2` and radius `(M − m)/2`; the endpoint
   mixture with mean `2Mm/(M + m)·u` attains the value.
3. **Comparison with the norm case.** A ball of angular radius `θ_B` lies in
   the cone of half-angle `θ_B`, so `θ_e ≤ θ*_e` and `κ^sq_e ≥ sec²θ_e = κ_e²`.
4. **The scout's product bound** `sec²θ_e·(M_e + m_e)²/(4M_e m_e)` (with
   `m_e, M_e` the extreme norms on `D_e`) is a valid upper bound on `κ^sq_e`,
   by `‖EW‖ ≥ cos θ E‖W‖` and the Pólya–Szegő/Kantorovich inequality. It is
   therefore never better than the exact value, and for balls it gives
   `sec⁴θ`.
5. **Correction of the first version.** Its claims that "for thin arcs the
   scout's bound is better" and that "neither dominates" were false. They
   compared the product bound against a fixed ball: the minimum-radius ball in
   the text, and the vertex-centroid ball in the code.
   - For a circular segment of radius `m` and half-angle `φ`, the ball with
     centre at distance `m/cos φ` and radius `m tan φ` contains the segment.
     It gives `sec²φ`, which is exact (the endpoint mixture attains it).
   - At `φ = 30°` the values are: exact `4/3`, product bound `1.3402`,
     minimum-radius ball `1.5`, centroid ball `1.3955` (t10).

**Interpretation.** The norm case sees only the *cone* around `D_e`, that is,
angular dispersion. The squared case sees the *best enclosing ball* of `D_e`:
it pays at least the square of the angular factor, plus radial (step-length)
dispersion, which does not vanish when all directions agree. This is the
relaxation-level form of the Hamiltonian-path effect (mixing paths with
different step lengths).

**Example C′ (1D, disjoint intervals, squared lengths; t6).**

- **Instance:** `s = {0}`, `A = [1, 3]`, `P = {3.5}`, `Q = {4.5}`, `t = {6}`,
  with edges `s→A→{P, Q}→t`. Both routes cost `12.375`.
- **Squared lengths:** `REL = REL_H = 12.25 < OPT = 12.375`, a gap of 1.0%.
- **Euclidean lengths:** `REL = OPT = 6` (Corollary A).

On 46 random 1D instances with disjoint intervals no gap appeared: gaps need
nearly balanced alternatives.

### 3.4 REL versus REL_H

**Proposition 2.** Let `v ∉ {s, t}`, and fix a `REL`-feasible local
configuration at `v`. It consists of arrival points `a_e = z̄'_e` with weights
`y_e` and departure points `b_f = z̄_f` with weights `y_f`, satisfying (C).

1. If `v` has at most one in-edge or at most one out-edge in `supp y`, the
   configuration extends to (H) at `v` with the same `(y, z, z')`.
2. If `X_v` is a simplex, the configuration extends.
3. Conversely, suppose `X_v` is not a simplex. Then there is a configuration
   with enough in- and out-edges that does not extend. Sizes at most `n+2` in
   total suffice.

*Proof.*

1. With a single in-edge `e`, set `λ_ef = y_f` and `w_ef = z_f`. Then (H2)
   follows from flow conservation and (C). The single out-edge case is
   symmetric.
2. Let `q_0, …, q_n` be the vertices, and write `a_e = Σ_i α_{e,i} q_i` and
   `b_f = Σ_i β_{f,i} q_i` in barycentric coordinates.
   - By (C) and uniqueness of barycentric coordinates,
     `π_i := Σ_e y_e α_{e,i} = Σ_f y_f β_{f,i}`.
   - Put `λ_ef := Σ_{i: π_i>0} y_e α_{e,i} y_f β_{f,i}/π_i` and
     `w_ef := Σ_i (y_e α_{e,i} y_f β_{f,i}/π_i) q_i ∈ λ_ef X_v`.
   - Row sums: `Σ_f λ_ef = Σ_i y_e α_{e,i} = y_e` and `Σ_f w_ef = y_e a_e`.
     Column sums follow symmetrically.
   - This is conditionally independent gluing given the vertex label.
   - This is the standard fact that first-level RLT (here the Lemma 5.4-type
     relaxation) is exact when one factor is a simplex. Thesis Prop. 8.2 is its
     interval case.
3. Take an affine dependence among distinct extreme points,
   `Σ_{i∈I⁺} c_i p_i = Σ_{j∈I⁻} |c_j| p_j` with equal positive totals.
   - Let in-edges arrive at `p_i`, `i ∈ I⁺`, and out-edges depart from `p_j`,
     `j ∈ I⁻`, with weights proportional to `|c|`.
   - (C) holds. But an extreme point is not a nontrivial convex combination,
     so a hull extension needs `w̄_ij = p_i` and `w̄_ij = p_j` whenever
     `λ_ij > 0`. That is impossible. ∎

Consequences:

- In 1D, `REL = REL_H`, since intervals are simplices. With Corollary A, any
  acyclic 1D instance whose lengths are affine on each `K_e` has
  `REL = OPT`. This includes `α w⁺ + β w⁻` with disjoint intervals on every
  edge, and confirms the scout's claim with its exact hypothesis.
- Proposition A′ gives an objective-level separation at a square. The scout's
  diagonal crossing (Exp 3) is another.

**Proposition 3 (repair) and a first-order bound for REL.**

- **Repair.** Take a `REL` point. Let `μ_v^in`, `μ_v^out` be the arrival and
  departure point measures of mass `y_v` at `v`, and let `ℓ_f(·, x')` be
  `Λ`-Lipschitz for `f ∈ out(v)`. Then
  ```
  REL_H ≤ REL + Λ Σ_v W1(μ_v^in, μ_v^out).
  ```
- **First-order bound.** For norm lengths with `g_e ≤ Λ‖·‖` on an acyclic
  graph,
  ```
  OPT ≤ κ_max · (REL + Λ · max_P Σ_{v∈P∖{s,t}} diam X_v).     (4)
  ```
  For Euclidean lengths, `REL ≥ min_P Σ_{e∈P} dist(X_u, X_v)`. So the
  relative gap of `REL` is `O(size/separation)`, while that of `REL_H` is
  `O((size/separation)²)` by Corollary B.

*Proof.* Let `π` be an optimal coupling. Replace each departure point `b_f` by
the barycentric projection `b'_f := Σ_e π(e, f) a_e / y_f`, and set
`λ_ef := π(e, f)`, `w_ef := π(e, f) a_e`.

- (H) holds at `v`, and (C) is preserved.
- The changes at different vertices touch disjoint variables.
- The cost changes by at most `Λ Σ_f y_f ‖b'_f − b_f‖ ≤ Λ W1`.

Then use `W1 ≤ y_v diam X_v`, flow decomposition, and (3). ∎

**Proposition 4 (the scout's crossing family, closed forms; t4(e)).**

- **Instance:** `v = [−1, 1]² × {0}`; `u_{1,2} = ±(a, a, 0)`;
  `w_{1,2} = ±(a, −a, 0)` with `a = R/√2`; `s = (0, 0, −R)`; `t = (0, 0, R)`.
- **Values:**
  ```
  OPT = 2√2 R + 2√(R² − √2 R + 1),     REL ≤ 2√2 R + 2R − 2√2.
  ```
  Hence `OPT − REL ≥ √2 − o(1)` and `OPT/REL − 1 = Θ(1/R)` (lower bound from
  these formulas, upper bound from (4)). Corollary B gives
  `OPT/REL_H − 1 ≤ sec θ − 1 ≤ 1/(R² − 2)`, using `sin θ ≤ √2/R`.
- **Numerics:** `REL` equals the upper bound and `R²(OPT/REL_H − 1) → 0.104`.

*Proof of OPT.* The middle segment is symmetric under `x_2 ↦ −x_2`, so an
optimal `x_v` lies on `x_2 = 0`. The optimum over the segment is at `x_1 = 1`,
giving `2√((a − 1)² + a²)`. The `REL` point puts arrivals at the corners
`±(1, 1)` and departures at `±(1, −1)`. ∎

## 4. Cyclic graphs

**Theorem 5 (walk version).** Let `G` be any digraph with
`in(s) = out(t) = ∅`, no edge constraints, and `ℓ_e ≥ 0` on `K_e`. Take any
feasible point of `REL_H`, with or without (D), and run the chain of
Theorem 1. Then:

1. The chain is absorbed at `t` almost surely, with finite expected length.
2. Call an edge *good* if an edge into `t` is reachable from it in the
   transition graph; let `T` be the good edges. The expected number of
   traversals of `e` is `y_e` for `e ∈ T` and `0` otherwise.
3. The walk (positions per visit, as before) has expected cost at most
   `Σ_{e∈T} y_e cav_e(z̄_e, z̄'_e) ≤ Σ_e y_e cav_e(z̄_e, z̄'_e)`.
4. Dijkstra in the pair graph (nonnegative arc costs) returns, in polynomial
   time, an s–t walk with positions of at most that cost.

Hence `REL_H^{no deg} ≤ WALK* ≤ Σ_e y_e cav_e`, where `WALK*` is the
shortest-walk value of arXiv 2507.10878 (revisits allowed, one position per
visit).

*Proof.*

- **No entry into the bad set.** Let `U` be the set of edge-states (with
  `y > 0`) from which no edge into `t` is reachable in the transition graph.
  `U` is closed, and no edge of `U` enters `t`, so `Σ_f λ_ef = y_e` for
  `e ∈ U`. Sum (H2) over `f ∈ U`. For `f ∈ out(s)`, `y_f` is the initial
  mass; otherwise `y_f = Σ_e λ_ef`. This gives
  `Σ_U y_f = Σ_{f∈U∩out(s)} y_f + Σ_{e,f∈U} λ_ef + Σ_{e∉U, f∈U} λ_ef`, and
  closedness makes the middle term `Σ_{e∈U} y_e`. So the chain puts no initial
  mass on `U` and never enters it.
- **Absorption.** From every state of `T`, absorption is reachable. A finite
  chain then absorbs almost surely, with geometric tails.
- **Expected visits.** Restricted to `T`, `y_T = π_0 + y_T P_TT`, where
  `π_0` is the initial law. `P_TT` is substochastic with spectral radius below
  one, so `y_T = π_0 (I − P_TT)^{-1}`, which is the vector of expected visits.
  Predecessors `d` of `e ∈ T` with `λ_de > 0` lie in `T`, since `U` is
  closed.
- **Expected cost.** The expected number of consecutive triples `(d, e, f)`
  is `y_d (λ_de/y_d)(λ_ef/y_e) = λ_de λ_ef / y_e`. So the expected cost is
  `Σ_{e∈T} Σ_{d,f} (λ_de λ_ef/y_e) ℓ_e(w̄_de, w̄_ef)`, by Tonelli since
  `ℓ ≥ 0`. The weights `λ_de λ_ef/y_e²` form a probability law on `K_e` with
  mean `(z̄_e, z̄'_e)`, and Jensen as in Theorem 1 gives part 3.
- **Deterministic walk.** Walks of the chain are walks of the pair graph. ∎

The scout's step 7 said the expected number of traversals *equals* `y_f`.
That holds on `T`. Circulations in `U` are never entered and are charged
nothing, which is harmless because `cav ≥ ℓ ≥ 0`.

**Corollary 5.1 (paths under the shortcut property).** Suppose
`ℓ_e = d|_{K_e}` for one convex `d : R^n × R^n → [0, ∞)` satisfying the
triangle inequality; for example `d(x, x') = g(x' − x)` with `g ≥ 0`
sublinear, which is the scout's common-norm case. Then
`OPT ≤ Σ_e y_e cav_e(z̄_e, z̄'_e)` for every `REL_H` point, degree
constraints included or not. With Corollary B,
`OPT ≤ κ_max·REL_H^{no deg}`.

*Proof.* If a walk visits `v` at steps `i < j`, delete steps `i+1..j` and keep
the position `p_i`. The edge `(v, v_{j+1})` exists, and
`d(p_i, p_{j+1}) ≤ Σ_{k=i}^{j} d(p_k, p_{k+1})`. Since `s` has no in-edges
and `t` no out-edges, neither repeats. ∎

**Proposition 5.2 (the path version fails without the shortcut property).**
The base is SIOPT Example 5.10 (cyclic, squared lengths). There, degree
constraints restore exactness because the only relaxed solution uses the
cycle at full flow. Here `X_1` is shrunk to `[−1/2, 1/2]` and a parallel route
`s → 3 → t` is added, so that a half-flow cycle satisfies the degree
constraints. Take squared lengths and

- sets `X_s = {−1}`, `X_1 = [−1/2, 1/2]`, `X_2 = X_3 = {0}`, `X_t = {1}`;
- edges `(s,1), (1,2), (2,1), (1,t), (s,3), (3,t)` (instance C2).

The `REL_H` point with degree constraints is:

- `y ≡ 1/2`;
- `λ_{(s1),(12)} = λ_{(21),(1t)} = 1/2` with pair points `−1/2` and `+1/2`;
- all other pair variables zero.

It is feasible (`y_1 = 1`) and has value `3/2`. Because all positions are
extreme points of the edge domains, `Σ_e y_e cav_e = 3/2 < OPT = 2`.
Numerically (t5), `REL_H(deg) = 1.5` exactly and the shortest walk costs
`1`. Without degree constraints the value `1/2` is an infimum, not attained:
an unbounded circulation on `1 → 2 → 1` drives the cycle cost toward `0`.
With the circulation capped by `y_e ≤ K`, the value is `1/2 + 1/(2K)`
(`0.55`, `0.505`, `0.5005` for `K = 10, 100, 1000`). The uncapped solves
return `0.5001–0.5003`, flagged inaccurate.

- The two-cycle cut `y_12 + y_21 ≤ y_2` removes C2.
- The variant C3, with cycle `1→2→4→1` and `X_4 = {0}`, survives two-cycle
  cuts (`REL_H = 1.5`). The generalized subtour cut on `{1, 2, 4}` removes it
  (`REL_H = 2`).

This is in the spirit of Example 1 of arXiv 2507.10878 (walks beat paths), but
at the level of the relaxation with degree constraints.

**Open Question 2.** For nonnegative convex lengths on cyclic graphs, does
`OPT ≤ Σ y cav` hold for `REL_H` plus all generalized subtour-elimination
cuts? The flow polytope with these cuts is not integral for directed paths,
so the chain decomposition alone does not settle it.

## 5. Edge constraints

**Proposition 6 (no separation-based bound).**

- **Instance (1D, acyclic):**
  - sets `X_s = {0}`, `A = [9, 11]`, `P = {21}`, `M = {19}`, `B = [29, 31]`,
    `X_t = {40}`, which are pairwise disjoint;
  - edges `s→A→{P, M}→B→t`;
  - edge constraints `x_v = x_u + 10` and zero lengths.
- **Values:** the MICP is infeasible, but `REL = REL_H = 0`.
- **With a bypass:** adding a direct `s→t` edge of length `1` gives
  `OPT = 1` and `REL = REL_H = 0`.

*Proof.*

- *Infeasibility.* Via `P`: `x_A = 10` and `x_P = 20 ≠ 21`. Via `M`:
  `19 ≠ 20`.
- *Relaxation point.* `y = 1, 1/2, 1/2, 1/2, 1/2, 1`, with
  `z̄'_{sA} = 10` and `(z̄, z̄') = (11, 21)` on `A→P`, `(9, 19)` on `A→M`,
  `(21, 31)` on `P→B`, `(19, 29)` on `M→B`, `(30, 40)` on `B→t`.
- *Checks.* The perspective constraints `z' = z + 10y` hold; (C) holds at `A`
  (`10 = 5.5 + 4.5`) and at `B`. The hull is canonical because `A` has
  in-degree 1 and `B` out-degree 1. ∎

After translation this is the overlap instance of Proposition 8. The geometric
parameter must be measured *through* the constraint, for example on the
transported sets. Separation of the sets `X_v` themselves is not the governing
parameter.

**Theorem 7 (identification constraints: line-graph reformulation).**

*Hypotheses.* Let `G` be acyclic, with convex vertex costs `c_v` (path cost
`Σ_{v∈p} c_v(x_v)`, as in Science Robotics, where segment costs are charged on
out-edges). Suppose there are linear maps `Λ_v` (entry block) and `Γ_v` (exit
block) such that:

- the edge constraints are `X_e = {(x_u, x_v) ∈ K_e : Λ_v x_v = T_e Γ_u x_u + t_e}`;
- **entry–exit independence (H):** `(Λ_v, Γ_v)(X_v) = A_v × C_v` for each
  internal `v`.

*Construction of `L`.*

- **Vertices:** the edges `e = (u, v)` of `G`, with sets
  `Σ_e := {σ ∈ C_u : T_e σ + t_e ∈ A_v}`, plus dummy points `S'` and `T'`.
- **Edges:** `(e, f)` for consecutive `e = (u, v)`, `f = (v, w)`, with length
  ```
  ĉ_v(σ_e, σ_f) := min{c_v(x) : x ∈ X_v, Λ_v x = T_e σ_e + t_e, Γ_v x = σ_f}.
  ```
  Boundary edges `S'→e` and `e→T'` carry `ĉ_s` and `ĉ_t`.

*Conclusions.*

1. `ĉ_v` is convex and finite on `Σ_e × Σ_f` (by (H)). `L` is acyclic and has
   **no edge constraints**.
2. `OPT(L) = OPT(G)`.
3. `REL_H(G) ≤ REL(L) ≤ REL_H(L) ≤ OPT`, where `REL_H(G)` includes the edge
   constraints in perspective form.
4. Theorem 1 applies to `L`: `OPT − REL_H(L) ≤ max_P Σ Δ(ĉ)`.

*Proof.*

1. `ĉ_v` is a partial minimization of a convex function over a convex set.
   (H) makes it feasible, and `ĉ_v ≤ max_{X_v} c_v`.
2. Paths correspond one-to-one. For a fixed path, substituting
   `σ_e = Γ_u x_u` gives the same convex restriction.
3. Take a `REL(L)` point: flows `μ_ef` and copies `ζ^tail_(ef)`,
   `ζ^head_(ef)`, conserved at each `L`-vertex `e` with sum `Z_e`.
   - Let `x̄_ef` be a minimizer defining `ĉ_v` at the barycenters. Set
     `λ_ef := μ_ef`, `w_ef := μ_ef x̄_ef`, `z'_e := Σ_f w_ef`,
     `z_f := Σ_e w_ef`.
   - Then (H) holds, and
     `Λ_v z'_e = T_e Σ_f ζ^tail_(ef) + t_e y_e = T_e Z_e + t_e y_e`.
   - Also `Γ_u z_e = Σ_d ζ^head_(de) = Z_e`, so the perspective edge constraint
     holds.
   - Costs charged per out-edge satisfy
     `c̃_v(Σ_e w_ef, Σ_e λ_ef) ≤ Σ_e c̃_v(w_ef, λ_ef)`, by subadditivity of the
     perspective. ∎

**Scope in practice.**

- **Order-1 motion planning.** `x_v = (a_v, b_v) ∈ X_v²` and `b_u = a_v`; (H)
  holds. `L` is the directed door formulation, a GCS with a common Euclidean
  norm. For cyclic region graphs, Corollary 5.1 still applies to `L`, and
  `OPT(L) = OPT(G)` by the chord argument of Proposition 10.
- **Bézier curves with `C^η` continuity** (Science Robotics (8): the last
  `η+1` control points of `u` determine the first `η+1` of `v`). (H) holds
  when the region constraints are only control-point containment (7a) and the
  degree satisfies `d ≥ 2η + 1`. With absolute time scaling (7b)–(7d), the
  entry and exit times are coupled, so (H) fails. It can be restored with
  relative time (durations), with a total-time bound only in the objective.
  Velocity limits (7c) need (H) to be checked.
- **Linear dynamics** `s_w = A s_v + B a_v + c` with `x_v = (s_v, a_v) ∈ D_v`.
  Here the entry block is `s_v` and the exit block `A s_v + B a_v`. (H) is
  one-step controllability from every entry state to every exit state in
  `C_v`. It holds for fully actuated systems with large input sets and fails
  for underactuated ones. Proposition 6 is the drift-only extreme (`B = 0`).

**Numerical evidence (t8).**

- *Cubic Bézier `C¹` DAG corridors (9 instances).* `OPT_region = OPT_line`,
  and `REL_line ≥ REL_H,region` in every instance. For example, the
  two-lane instance has `REL_region = 5.000 = |goal − start|` and
  `REL_line = OPT = 5.023`.
- *Ring around a wall with `L→{T, B}→R` and cubic Bézier `C¹`.*
  `REL_region = REL_H,region = 3` for `H = 1, 5, 20`, while
  `REL_line = REL_H,line = OPT = 4.236, 12.050, 42.013`.

**Open Question 3.** For underactuated dynamics, or when (H) fails, which
geometric parameter controls the gap? Candidates are multi-step
controllability radii of the modes: grouping `k` steps into one vertex restores
(H) when the `k`-step reachable map is onto.

## 6. Overlapping convex covers

**Proposition 8 (no multiplicative bound under overlap; scout Prop. 5).**

- **Instance:** `s = {0} → A = [−1, 1] → {P = {1}, M = {−1}} → B = [−1, 1]
  → t = {δ}` with lengths `|x_v − x_u|`, for `0 ≤ δ ≤ 1`.
- **Values:** `REL = REL_H = δ` and `OPT = 2 − δ`. So `OPT/REL_H = ∞` at
  `δ = 0`.

*Proof.*

- *Lower bound.* `|w| ≥ w`, and (C) telescopes to
  `REL ≥ x_t − x_s = δ`.
- *Upper bound.* Take `y = 1/2` on the fork, departure points `±1` at `A`
  (mean `0` = arrival), arrival points `±1` at `B` (mean `0`), and edge `B→t`
  of cost `δ`. The hull is canonical at `A` and `B`.
- *OPT.* Via `P`: `|x_A| + |1 − x_A| + |x_B − 1| + |δ − x_B| ≥ 2 − δ`. Via
  `M` the cost is at least `2 + δ`. ∎

The additive bound is nearly tight here: `max_P Σ Δ_e = 2 − δ²` (computed
exactly), against the gap `2 − 2δ`. The circumradius bound (2) gives `4`.

**Corollary 8.1 (checkable parameter I: set radii).** Let all lengths be
`g(x' − x)` for one norm `g ≤ Λ‖·‖₂`. On an acyclic graph with arbitrary
overlaps,

```
OPT/REL_H ≤ 1 + Λ · max_P Σ_{e∈P} (R_u + R_v) / dist_g(X_s, X_t).
```

This follows from (2) and `REL ≥ dist_g(X_s, X_t)`, which holds on any
digraph. For the latter, take `a` in the dual unit ball of `g`, so
`ℓ̃_e ≥ aᵀ(z'_e − z_e)`. Then (C) telescopes to `aᵀ(x̄_t − x̄_s)` with
`x̄_s ∈ X_s`, `x̄_t ∈ X_t`, and minimax over the dual ball gives the claim.

**Proposition 9 (region formulation; checkable parameter II: detour).**
Consider the order-1 region formulation: `x_v = (a_v, b_v) ∈ X_v²`, continuity
`b_u = a_v`, cost `‖b_v − a_v‖` on out-edges.

1. `REL ≥ |goal − start|`. This holds with or without degree constraints,
   two-cycle cuts or the region hull, and on cyclic region graphs. Hence
   `OPT/REL ≤ OPT/|goal − start|`, the detour ratio of the optimal route.
2. For the ring around a wall of half-height `H`, the bound is attained and
   unbounded:
   - regions `L = [−2, −1] × [−H−1, H+1]`, `R = [1, 2] × [−H−1, H+1]`,
     `T = [−2, 2] × [H, H+1]`, `B = [−2, 2] × [−H−1, −H]`;
   - start `(−1.5, 0)`, goal `(1.5, 0)`;
   - values `REL = REL_H(region) = 3`, also with lifted two-cycle cuts, and
     `OPT = 2 + 2√(H² + 1/4)`.

*Proof.*

1. For a unit `u`, `‖zb_f − za_f‖ ≥ uᵀ(zb_f − za_f)`. Sum over out-edges of
   regions:
   - `a`-conservation and continuity give
     `Σ_{tail region} uᵀza_f = Σ_{head region} uᵀzb_e`;
   - region-to-region terms cancel;
   - what remains is `uᵀ goal − uᵀ start`.
2. Upper bound by an explicit point:
   - flows: `y = 1` on `s→L`, `1/2` on `L→T`, `L→B`, `T→R`, `B→R`, and `1`
     on `R→t`;
   - `L` exits at `(−1.5, ±H)` with zero-length segments (mean `=` start);
   - `T` and `B` run the segments `(−1.5, ±H) → (1.5, ±H)`, each costing
     `3/2`;
   - `R` enters at `(1.5, ±H)` with mean `=` goal and has a zero-length
     segment;
   - the free `b`-copies on in-edges are set to satisfy `b`-conservation.

   All degree constraints hold, and the lifted two-cycle cuts hold (for
   example, `start − ½(−1.5, H) ∈ ½L`). `L` has in-degree 1 and `R` out-degree
   1 in the support, so the region hull adds nothing. ∎

Numerically (t7(c), `H = 1, 2, 5, 10, 20`), all three relaxations equal
`3.00000` and `OPT` matches the closed form. So neither of the scout's fixes
(two-cycle cuts, region hull) helps, and the region formulation has no bound
independent of the detour. The scout's Exp 8 ring (29% gap) is `H = 1`.

**Proposition 10 (checkable parameter III: door aperture).** Consider the
door formulation: vertices are start, goal and the doors `X_u ∩ X_v`; edges
join two vertices lying in a common region; lengths are `‖x' − x‖`; no edge
constraints.

1. `OPT_door = OPT_region`.
2. For every `REL_H,door` point, with or without degree constraints,
   `OPT ≤ sec θ_door · REL_H,door`. Here `θ_door` is the maximum aperture of
   `D' − D` over regions and pairs of distinct doors (or start and goal)
   `D, D'` in the region. `θ_door` is finite, for example, when the doors of
   each region are pairwise disjoint and do not contain the start or goal.

*Proof.*

1. A door path is a polygonal path whose segments lie in regions. If a region
   repeats, replace the portion between its first and last use by a chord
   inside the region (convexity, triangle inequality). The result is a region
   path of no larger cost. The converse inclusion is immediate.
2. Corollary 5.1 (common norm) with Corollary B. ∎

**Door aperture on the ring family.** Two kinds of edge set the aperture.

- In region `T`, from door `L ∩ T` to door `R ∩ T`, the displacement set is
  `[2, 4] × [−1, 1]`, with half-angle `arctan(1/2)`.
- In region `L`, from door `L ∩ T` to `L ∩ B`, it is `[−1, 1] × [−2H−2, −2H]`,
  and from the start to `L ∩ T` it is `[−1/2, 1/2] × [H, H+1]`. Both have
  half-angle `arctan(1/(2H))`.

Hence

```
sec θ_door = max(√5/2, √(1 + 1/(4H²))).
```

This equals `√5/2 ≈ 1.118` for `H ≥ 1`, `√2 ≈ 1.414` at `H = 1/2` and
`√5 ≈ 2.236` at `H = 1/4`. The first version wrongly said "for every `H`".
Numerically (t7(c), `H ∈ {1/4, 1/2, 1, 2, 5, 10, 20}`), the computed
apertures match, the door relaxation is exact for every tested `H`, and the
region formulation's ratio is `14.0` at `H = 20`.

In the scout's corridors, doors of parallel lanes overlap and
`θ_door = π/2`. Consistently, the scout found the door formulation no better
there (Exp 12).

**Open Question 4 (simply connected covers).** For planar, simply connected
unions of convex regions, is the region-formulation ratio `OPT/REL` bounded
by an absolute constant?

- The ring mechanism needs a hole. A fork region whose exits lead to
  region-disjoint routes that rejoin encloses an obstacle.
- The scout's adversarial simply connected corridors reached 16%.
- We have neither a bound nor a family with growing ratio.

## 7. Hardness of approximation against aperture

### 7.1 Fixed dimension

**Proposition 11 (approximation in fixed dimension for separated instances).**
Take Euclidean lengths on any digraph. Let `δ := min_e dist(X_u, X_v) > 0` and
`D := max_v diam X_v`. A `(1 + ε)`-approximate path is computable in time
polynomial in `|V|`, `|E|` and `(1 + D√n/(εδ))^n`. This is a PTAS when `D/δ`
is bounded (or encoded in unary). In general the time is exponential in the
bit length of `D/δ`.

*Proof.*

- *Nets.* Build an `h`-net of each `X_v` with `h = εδ/2`.
  - Cover a bounding box of side `D` by cells of side `s = εδ/√n` and take the
    cell *centres*. There are `⌈D/s⌉ ≤ 1 + D√n/(εδ)` per axis, and every point
    of the box is within the half-diagonal `s√n/2 = h` of a centre. A grid
    anchored at a box corner would need one more point per axis for the same
    radius.
  - Project the centres onto `X_v`. Projection is nonexpansive and fixes
    points of `X_v`, so the projected points form an `h`-net with at most
    `M = (1 + D√n/(εδ))^n` points.
  - The product graph has at most `|V|·M` nodes and `|E|·M²` arcs.
- *Search.* Run Dijkstra on (vertex, net point) pairs, then shortcut
  repeated vertices by the triangle inequality.
- *Error.* Snapping an optimal path with `K` edges changes each edge length by
  at most `2h`. Since `OPT ≥ Kδ`, the snapped path costs at most
  `(1 + 2h/δ) OPT = (1 + ε) OPT`. ∎

This is routine grid discretization. So `1 + cθ²` hardness at fixed `θ` needs
growing dimension or growing `D/δ`. Exact solution is NP-hard already in 2D,
by the scout's Prop. 6(c) via polygon touring (not re-derived here).

### 7.2 Growing dimension: `1 + θ²/poly` hardness

**Proposition 12.** Fix `θ ∈ (0, π/2)`. Let a 3SAT instance have `N`
variables and `m` clauses, with `tan θ ≤ 3.3√N`. If this fails, add unused
variables; `N` below is the padded count.

In polynomial time one can build an SPP-in-GCS instance with:

- an acyclic layered graph;
- **pairwise-disjoint** polytopes (rational data);
- Euclidean lengths and all apertures at most `θ`;
- `OPT = (m+1)L` if the formula is satisfiable, and
  `OPT ≥ (m+1)L·(1 + tan²θ/(4N(m+1)²))` otherwise.

Hence approximating within `1 + tan²θ/(4N(m+1)²)` is NP-hard.

*Proof.* Use the thesis Thm 9.1 embedding with a time axis and a height
stagger inside each layer.

- *Construction.*
  - Let `L_0 := √N/tan θ`, rounded up to a rational within a factor `1.01`.
    Set `η := L_0/30` and `L := L_0 + 3η = 1.1 L_0`.
  - `X_s = [0,1]^N × {0}` and `X_t = [0,1]^N × {(m+1)L}`.
  - Literal `j ∈ {1, 2, 3}`, equal to `(k, a)`, of clause `i` gets the set
    `{x ∈ [0,1]^N : x_k = a} × {iL + jη}`.
  - Consecutive layers are fully connected.
- *Disjointness.* All heights are distinct, since `3η < L`. The first version
  put all literals of a layer at the same height, where their sets can meet,
  for example at `(1, 1)` for `x_1 = 1` and `x_2 = 1`.
- *Apertures.* Every edge rises by at least `L − 3η = L_0` vertically and
  moves at most `√N` laterally. So `tan θ_e ≤ √N/L_0 ≤ tan θ`.
- *Satisfiable instances.* Every path rises by exactly `(m+1)L`, and its cost
  is at least its total rise, with equality iff there is no lateral motion. A
  constant satisfying assignment gives `OPT = (m+1)L`.
- *Unsatisfiable instances.* Every choice of literals forces some variable to
  `a` on layer `i` and to `1 − a` on layer `i' > i`, with `i' − i ≤ m − 1`.
  - That sub-path rises by `V ≤ (m−1)L + 2η ≤ mL` and moves laterally by at
    least 1, so it costs at least `√(V² + 1)`.
  - The rest of the path costs at least its rise, `(m+1)L − V`.
  - Hence `OPT ≥ (m+1)L + √(V² + 1) − V ≥ (m+1)L + 1/(2mL + 1)`.
- *Ratio.* If `L ≥ 1/3`, which holds when `tan θ ≤ 3.3√N`, the ratio is at
  least `1 + 1/((m+1)L(2mL + 1)) ≥ 1 + 1/(3(m+1)²L²)`. Since
  `L ≤ 1.1·1.01·√N/tan θ`, this is at least `1 + tan²θ/(4N(m+1)²)`. ∎

Two notes:

- Euclidean lengths are irrational, so the statement is in the real-number
  model, or with lengths evaluated to polynomially many bits.
- This is a direct adaptation of thesis Theorem 9.1 with a standard gap
  argument, and the `1/poly` gap is modest.

**Consequence for relaxations.** `REL_H` is computable in polynomial time
to any fixed accuracy. Suppose that on all such instances `OPT/REL_H ≤ 1 + γ'`
for some `γ' < tan²θ/(4N(m+1)²)`. Then comparing `REL_H` with `(m+1)L` would
decide satisfiability. So unless P = NP, no such uniform bound holds, and the
second-order bound of Corollary B cannot be replaced by exactness.

Check (t9, rerun with the staggered construction). The test uses an
unsatisfiable 2-CNF with `N = 2`, `m = 4` and `θ = 30°, 10°, 3°`:

- all sets are pairwise disjoint and all apertures are at most `θ`;
- the computed `OPT` exceeds `(m+1)L + 1/(2mL + 1)`, with relative excess
  `6.8·10⁻³`, `6.4·10⁻⁴`, `5.7·10⁻⁵` against the bound
  `tan²θ/(4N(m+1)²) = 1.7·10⁻³`, `1.6·10⁻⁴`, `1.4·10⁻⁵`;
- the satisfiable subformula has `OPT = (m+1)L`.

### 7.3 The obstacle to `1 + cθ²` (scout Q2)

Along a layered embedding with spacing `L`, a path costs

```
Σ_k √(L² + ‖w_k‖²) = (m+1)L + Σ_k ‖w_k‖²/(2L) + O(Σ_k ‖w_k‖⁴/L³),
```

where `w_k` are the lateral displacements.

- **Cheap spreading.** A forced lateral change of size `Δ` between layers
  `i` and `i + M` can be spread evenly, at extra cost `Δ²/(2ML)`.
- **What a constant excess needs.** A relative excess `cθ²` (with
  `θ² ≈ max ‖w‖²/L²`) requires `Σ_k ‖w_k‖² ≥ c'·m·max_k ‖w_k‖²`. In NO
  instances, a constant fraction of steps would have to be forced to
  near-maximal lateral displacement, and no forced change could be spread.
- **Why the current sets fail.** The sets that carry assignment information
  across layers (faces of the cube) are exactly those that permit spreading.
  Heuristically, sets that forbid spreading make the lateral state nearly
  discrete. The problem then tends toward an ordinary shortest path over
  discrete states, which is polynomial. We have no theorem to this effect.

A proof of `1 + cθ²` hardness would need gadgets that carry information
through a continuous state while forbidding spreading, for example a
label-cover structure with geometric consistency gadgets. We could not
construct one. Also note:

- by Proposition 11, such gadgets need growing dimension;
- the gap between the known hardness `1 + θ²/poly(N, m)` and the algorithmic
  bound `sec θ = 1 + θ²/2 + O(θ⁴)` remains a factor `poly(N, m)` in the `θ²`
  coefficient.

**Q2 remains open.**

## 8. Computations

**Environment.**

- cvxpy 1.9.3 with Clarabel; `OMP_NUM_THREADS=1`; small instances.
- Exact `OPT` by enumerating simple paths and solving each convex
  restriction.
- After the review, the squared-length perspective in `relax` is an explicit
  rotated-cone epigraph `‖z' − z‖² ≤ t_e y_e` rather than cvxpy's
  `quad_over_lin`.
- Every run finished within minutes on one core. Commands were run from
  `research-20260928b/gcs/code/`, and outputs are the `*.out` files there.

All results are from targeted local checks. No project-wide checks were run,
and no CI status or logs were inspected. The table shows the final (post-review)
runs; §11 lists what was rerun and why.

| Command | What it checks | Result |
|---|---|---|
| `python3 t1_theorem1.py 0 40 1.0 > t1_seed0.out` | Theorem 1 chain `REL ≤ REL_H ≤ OPT ≤ reopt ≤ pairDP ≤ E[round] ≤ Σ y cav ≤ REL_H + Σ yΔ ≤ REL_H + max_P ΣΔ`; random DAGs, dims 1–3, boxes/points/triangles, mixed l2/sq/l1/affine lengths | 40 instances, 0 violations |
| `python3 t1_theorem1.py 1 40 2.5 > t1_seed1_big.out` | same, larger (overlapping) sets | 40 instances, 0 violations; 8 with `OPT > REL_H` |
| `python3 t2_kappa.py 0 30 > t2_seed0.out` | Cor. B (`sec θ`) and Cor. C (`sec²θ`, exact for balls) chains on random ball DAGs; `ℓ1` sign-monotone exactness | 30 + 30 + 15 instances, 0 violations |
| `python3 t3_adversarial.py sq 150 0 > t3_sq.out`, `python3 t3_adversarial.py l2 150 0 > t3_l2.out` | random-start local search maximizing `(OPT/REL_H − 1)/(κ_max − 1)` over 4 templates × 2 dims (instances with `κ_max − 1 < 10⁻⁴` skipped) | best 0.199 (l2), 0.099 (sq); never above 1 |
| `python3 t3b_tangent_family.py l2 200 0 > t3b_l2.out`, `python3 t3b_tangent_family.py sq 200 0 > t3b_sq.out` | Prop. B′ closed forms with exact radii and exact `κ_max`; seeded local search | l2 ratio 0.500016 (10°), 0.500246 (20°), 0.500485 (23.6°), 0.501336 (30°), matching the exact formula; sq ratio (vs `sec² − 1`) 0.4998 (2.9°) down to 0.4766 (30°) |
| `python3 t4_exactness.py 0 > t4.out` | (a) affine ⇒ `REL_H = OPT`; (b) Prop. A′; (c) 1D disjoint intervals ⇒ `REL = OPT` (acyclic, and cyclic with common `g` and no degree constraints); (d) triangles ⇒ `REL = REL_H`; (e) Prop. 4 closed forms; (f) Prop. 3 and bound (4) | (a) max error 3e−7 on 30; (b) `0 / 2 / 2`; (c) 0 exceptions; (d) max 4e−7; (e) matches to 1e−6; (f) 0 violations on 25 |
| `python3 t5_cyclic.py 0 30 > t5.out` | Thm 5 / Cor. 5.1 chain on random cyclic l2 instances without degree constraints; Prop. 5.2 (C2, C3), cuts | 30 instances, 0 violations; C2/C3: `REL_H(deg) = 1.5`, `Σ y cav = 1.5 < OPT = 2`; with GSEC: 2 |
| `python3 t6_squared1d.py 60 150 0 > t6.out` | Cor. C radial constant in 1D (squared); Example C′ | 46 random, 0 violations, 0 gaps; balanced fork gap 1.0% (REL 12.25, OPT 12.375), Euclidean exact |
| `python3 t7_overlap.py 0 > t7.out` | Prop. 8 exact values and `max_P ΣΔ = 2 − δ²`; bound (2) on 25 random overlapping DAGs; Prop. 9 ring-wall and Prop. 10 door relaxation for `H ∈ {1/4, 1/2, 1, 2, 5, 10, 20}`; `REL ≥ |goal − start|` on 15 random unions | all as stated; door apertures 2.236, 1.414, then 1.118 for `H ≥ 1`; 0 violations |
| `python3 t8_edge.py 0 8 > t8.out` | Prop. 6; Thm 7 on cubic Bézier `C¹` DAG corridors and ring-wall | as stated; 0 violations |
| `python3 t9_hardness.py > t9.out` | Prop. 12 staggered embedding on a tiny unsatisfiable 2-CNF | all sets pairwise disjoint; apertures ≤ θ; lower bound holds at 30°, 10°, 3° |
| `python3 t10_kappa_sq_exact.py 150 0 > t10.out` | Cor. C exact form: best-ball value vs mixture certificate on 150 random polygons; product and centroid-ball bounds; circular segment and radial segment | certificate = best ball to 6e−8; product and centroid bounds never below it; `κ^sq ≥ sec²θ`; segment `φ = 30°`: 4/3 exact |

The adversarial searches are small (hundreds of evaluations). They support,
but cannot establish, the conjectural statements. Solver tolerances are about
1e−7; checks use relative tolerance 1e−5.

## 9. Literature comparison and novelty caution

**Sources examined in this workstream.**

- **Local literature and scout downloads:**
  - Marcucci et al. SIOPT 2024 (`literature/papers/marcucci2024-shortest-paths-in-graphs-of/fulltext.md`):
    §§3, 5, 7, 9.4, including (5.5), Lemma 5.4, Prop. 7.1, (7.4), Lemma 7.4,
    Example 5.10 and §9.4.
  - Marcucci thesis (`../scouting/graphs-of-convex-sets/src/marcucci-thesis.txt`):
    Thm 8.1, Props 8.1–8.2, Lemmas 8.1–8.2, Thms 9.1–9.3, §§9.3–9.5.
  - Science Robotics / arXiv 2205.04422 (§5: the sets (7), edge constraints
    (8), costs (9)–(10)).
  - arXiv 2507.10878 (shortest walks, §II.C–D, §IV).
  - arXiv 2409.19543 (Lemma 1, affine versus quadratic cost-to-go).
  - arXiv 2510.20184 (Props 1–2, Theorem 1).
- **Repository literature summaries:** Balas 1985 and 1998, Ceria–Soares 1999,
  and Günlük–Linderoth 2010 (`literature/papers/*/paper.md`).
- **arXiv API queries run on 2026-09-28** (results listed by title):
  - `abs:"graph of convex sets" AND abs:"integrality gap"` — no hits;
  - `abs:"graphs of convex sets" AND abs:tightness`;
  - `abs:"perspective relaxation" AND abs:"shortest path"`;
  - `abs:"shortest path" AND abs:neighborhoods AND abs:approximation`;
  - `abs:"convex sets" AND abs:"shortest" AND abs:relaxation`;
  - `id_list=2305.01072,2407.08848,2410.08909` (abstracts).

  None states an a priori gap bound for GCS relaxations.
- **Recalled, not re-fetched:**
  - Martin–Rardin–Campbell, *Polyhedral characterization of discrete dynamic
    programming*, Oper. Res. 38 (1990): LPs over dynamic-programming
    hyperpaths are integral under a disjointness condition.
  - Björklund–Husfeldt–Khanna, ICALP 2004 (longest path inapproximability),
    already flagged by the scout.
  - The TSP-with-neighborhoods approximation literature under fatness or
    separation: Arkin–Hassin 1994 (cited in SIOPT), Dumitrescu–Mitchell,
    Mitchell.
- **Web search** was unavailable: the session's web-search budget was
  exhausted before this workstream started.

**Relation to known results** (revised after review; the review also scanned,
via OpenAlex, the 64 works citing SIOPT 2024 and found no gap bound).

- **Plausibly new as GCS statements, built from standard ingredients.**
  - *Theorem 1.* No GCS source examined states an a priori integrality-gap
    bound, a rounding guarantee or an approximation ratio. The ingredients are
    standard:
    - Markov-chain decomposition of a flow on the line graph;
    - Jensen and concave-envelope arguments for first-moment relaxations;
    - the disjunctive vertex hull, already written down in SIOPT (7.4).

    A referee may regard the theorem as elementary.
  - *Corollaries B and C.* The `sec θ` constants and the exact
    enclosing-ball characterization of `κ^sq_e` are plausibly new in this
    setting. The latter rests on the classical fact that `cav_D(‖·‖²)` is the
    lower envelope of the affine majorants coming from enclosing balls.
  - *Theorem 7.* The dominance `REL_H(G) ≤ REL(L)` and the independence
    criterion (H) are plausibly new. The line graph of region intersections
    itself appears as a heuristic search graph in "Fast path planning through
    large collections of safe boxes" (arXiv 2305.01072, IEEE T-RO 2024); only
    its abstract was checked.
  - *Propositions 9–10.* The ring family and the door-aperture bound are
    plausibly new examples and corollaries.
- **Known or routine.**
  - Corollary A: network-flow or DP-extended-formulation integrality after
    projection (Martin–Rardin–Campbell; Ceria–Soares for linear objectives).
    SIOPT §7.2 already derives the hull by disjunctive programming.
  - Proposition 2: (2) is the standard fact that RLT is exact on a simplex
    factor; (3) generalizes thesis Prop. 8.1; (1) is trivial.
  - Proposition 3: a standard optimal-transport repair.
  - Theorem 5 and Corollary 5.1: routine given Theorem 1. The walk/path
    distinction follows arXiv 2507.10878.
  - Proposition 5.2: a small variant of SIOPT Example 5.10.
  - Proposition 11: routine grid discretization, in the style of classical
    approximation schemes for geometric shortest paths.
  - Proposition 12: a direct adaptation of thesis Theorem 9.1 with a time axis
    and a standard gap argument.
- **Specific neighbours.**
  - Morozov et al. (2409.19543) and 2507.10878 build lower bounds with convex
    quadratic cost-to-go (SDP). This note gives upper bounds (rounding) for
    the first-moment relaxations, so the two are complementary.
  - arXiv 2507.19210 gives measure (moment) relaxations, again lower-bound
    machinery.

Unsuccessful searches do not establish novelty. Web search was unavailable to
both the author and the reviewer.

## 10. Status and corrections to the scout report

**Proved here:**

- Theorem 1 with Corollary 1.1;
- Corollaries A, B, C (C in the exact enclosing-ball form);
- Propositions A′, B′ (including the exact `REL_H` formula of the family and
  its series), 2, 3, 4, 5.2, 6, 8, 9, 10, 11, 12;
- Theorems 5 and 7;
- Corollaries 5.1 and 8.1.

**Numerical only:**

- the constant `0.104` in Prop. 4;
- `REL` of the Bézier ring-wall (t8(c));
- exactness of the door relaxation on the ring family (Prop. 10 proves only
  `≤ sec θ_door`, which is `1.118` for `H ≥ 1`);
- the finite-`θ` values of the Prop. B′ ratio (its series `1/2 + θ⁴/64` is
  derived, §3.2).

**Open:** Questions 1–4 and scout Q2 (§7.3).

**Corrections and sharpenings of the scout report.**

1. **Scout Theorem 1 (acyclic).** Correct. The proof now includes the
   conditional-independence step and an explicit pair-graph construction.
   Degree constraints and nonnegativity are not needed.
2. **Scout Theorem 1, cyclic step 7.** "Expected traversals equal `y_f`"
   holds only on the good set `T`. The conclusion survives because lengths are
   nonnegative. The statement generalizes to walks for any nonnegative convex
   lengths and to common convex quasi-metrics for paths. For general lengths
   the path version is false, even with degree constraints and the hull
   (Prop. 5.2).
3. **Scout Corollary B, finiteness.** "`κ_e` finite iff `X_u ∩ X_v = ∅`" is
   wrong in the "only if" direction. The correct condition is `θ_e < π/2`.
   Also, `κ_e = 1` only when `ℓ_e` is affine on `K_e`, so those cases are
   covered by Corollary A.
4. **Scout Corollary C.** The Kantorovich product is valid but loose (`sec⁴θ`
   for balls). The exact constant is `κ^sq_e = sec²θ*_e` with `θ*_e` the
   best enclosing-ball angular radius (Corollary C), so the product bound is
   never better.
5. **Scout Exp 14.** Strengthened to nonnegative affine lengths:
   `REL = 0 < REL_H = OPT = 2`.
6. **Scout Proposition 2(ii).** Proved by barycentric gluing, with a converse
   for non-simplex sets.
7. **Scout "sharpness 0.499".** Explained by the analytic tangent family of
   Prop. B′, which has limit ratio `1/2`.
8. **Scout's overlap regime.**
   - The negative results are made rigorous: 1D, and the region formulation
     with exact values and unbounded ratio despite two-cycle cuts and the
     region hull.
   - Three checkable parameters that do give bounds are identified: set radii
     (additive), detour ratio (region formulation, tight), and door aperture
     (door formulation).
   - The scout's remark that doors "help around a single obstacle but not in
     corridors" is explained by the door aperture being finite on the ring and
     infinite for overlapping lanes.

## 11. Revision after review

The [independent review](../reviews/gcs-review.md) (scripts in
[`reviews/gcs/`](../reviews/gcs/)) found every theorem correct and requested
nine corrections. I re-derived each one before changing the text.

1. **Corollary C is exact** (§3.3).
   - `κ^sq_e = inf_B sec²θ_B = 1/(1 − τ*)`, computable by a convex program.
     The proof uses ball-induced affine majorants for the upper bound and a
     Danskin–Carathéodory mixture for the lower bound.
   - The false claims that "thin arcs favour the scout's product bound" and
     that "neither bound dominates" are removed. They compared against a fixed
     ball: the minimum-radius ball in the text, the vertex-centroid ball in
     the code.
   - `gcslib.kappa_sq` now computes the exact value, and t10 verifies it.
2. **Prop. B′ numerics** (§3.2). The ratio is `1/2 + θ⁴/64 + O(θ⁶)`
   (0.5004848 at 23.578°), not "0.5000 up to 23.6°". The series was added
   after the recheck; the first revision said only "`c ≈ 0.017`", which is a
   mid-range value, not the limit. The exact relaxation value
   of the family, a two-dimensional minimization, is now stated. The first
   script inflated the radii by `10⁻³` and divided by a numerical `κ_max`.
3. **Bound (3)** now requires `g_e ≥ 0` for its second inequality, with the
   counterexample mechanism stated.
4. **Theorem 1(3).** The pair graph has *at most* the stated number of nodes.
5. **Prop. 5.2** now names SIOPT Example 5.10 as its base instance.
6. **Prop. 10.** `sec θ_door = max(√5/2, √(1 + 1/(4H²)))`, so `1.118` holds
   only for `H ≥ 1`. It is `1.414` at `H = 1/2` and `2.236` at `H = 1/4`
   (derived, and checked in t7).
7. **Prop. 11** is now stated as a `(1 + ε)`-approximation with running time
   polynomial in `|V|`, `|E|` and `(1 + D√n/(εδ))^n`, that is,
   `poly(|V|, |E|)·(1 + D√n/(εδ))^{2n}` counting the pairs of net points per
   edge: a PTAS only for bounded (or unary) `D/δ`. The first revision wrote
   the exponent `n` in the Summary and here, which the recheck corrected. The
   grid count assumes cell-centred points, which is now stated.
8. **Prop. 12.**
   - Same-layer literal sets intersected. Heights are now staggered within
     layers, so all sets are pairwise disjoint.
   - The constant becomes `tan²θ/(4N(m+1)²)`, under the hypothesis
     `tan θ ≤ 3.3√N` (pad `N` otherwise). The conflicting layers satisfy
     `i' − i ≤ m − 1`.
   - Checked in t9.
9. **Prop. 2(2)** is identified as the standard fact that RLT is exact on a
   simplex factor.

**Final fixes after the recheck** ([reviews/gcs-recheck.md](../reviews/gcs-recheck.md)).
The recheck confirmed all six revisions and Theorem 1. I made the following
minor fixes.

- **Prop. B′.** The ratio is now stated as exactly `1/2 + θ⁴/64 + O(θ⁶)`,
  with a series derivation (re-derived with SymPy) and 60-digit checks of the
  exact formula. The finite-`θ` table uses exact values at `θ = 23.578°`
  (see item 2 above).
- **Prop. 11.** In the Summary and item 7 above, the exponent is `2n`
  (pairs of net points per edge). The grid count now states that it assumes
  cell-centred points.
- **Corollary C, Consequence 1.** "Exactly when `D_e` is a ball" is reworded
  so that it is not an "iff". Equality with `sec²θ_e` also holds for the chord
  between two tangent points of a ball (`κ^sq = 4/3`).
- **Code (`gcslib.kappa_sq`).**
  - When `0` is a vertex of `D_e`, the function used to drop the zero
    difference and return a finite value (7.04 on the recheck's triangle
    example). The true value is `κ^sq_e = ∞` whenever `0 ∈ D_e`: mix `0` with
    any `w ≠ 0`.
  - It now returns `∞` in that case, and `1` when `D_e = {0}` (an identically
    zero length).
  - Only t10 reaches this branch, and t10 excludes sets with `0 ∈ D`, so no
    reported number changes. The rerun
    `python3 t10_kappa_sq_exact.py 150 0 > t10.out` reproduces its output
    exactly.
- **Prop. 5.2.** `REL_H^{no deg} = 1/2` is an infimum, not a minimum. A
  capped-circulation check gives `1/2 + 1/(2K)`. This was run inline, with no
  output file, from `gcs/code/`: `relax(..., degree=False, extra=y_e ≤ K)` for
  `K = 1, 10, 100, 1000`.

**Novelty (§9)** is revised as the review suggests.

- Theorem 1 and Corollaries B and C are plausibly new as GCS statements but
  built from standard ingredients.
- Corollary A, Prop. 2(2), Prop. 5.2, Prop. 11 and Prop. 12 are known or
  routine.
- The line graph of region intersections appears as a heuristic in arXiv
  2305.01072.

**Solver caution** (review §7: Clarabel can falsely report infeasibility on
cvxpy's `quad_over_lin` perspective).

- The first-version outputs contained no `inf` relaxation values. But t3,
  t3b and t6 skip non-finite relaxations silently, so an effect could not be
  ruled out from the outputs alone.
- I replaced the squared perspective with an explicit rotated-cone epigraph
  and reran every script that uses squared lengths: t1 (both seeds), t2, t3,
  t3b, t4, t5 and t6.
- Their summary results are unchanged: identical violation counts, gap
  counts and reported example values. Only noise-level quantities moved: the
  t4(d) maximum went from 8e−7 to 4e−7, and the t6 local search, whose scores
  are all zero up to solver noise, reports a different argmax.
- t3b changed only through the radius fix in item 2.
- An interrupted squared run of t3 showed a spurious score of 0.063 on an
  instance with `κ_max − 1 ≈ 10⁻⁸`. t3 now skips instances with
  `κ_max − 1 < 10⁻⁴`, and the rerun reproduces the earlier bests (0.199 l2,
  0.099 sq).

**Other code changes.**

- `poly_from_vertices2d` now takes the convex hull of its input. Earlier
  scripts passed only triangles and are unaffected; the non-convex input
  appeared first in the new t10.
- t7 now covers `H ∈ {1/4, 1/2}`; t9 uses the staggered construction.

**Targeted commands rerun after the review**, all from `gcs/code/` with
`OMP_NUM_THREADS=1`:

```
python3 t10_kappa_sq_exact.py 150 0 > t10.out
python3 t3b_tangent_family.py l2 200 0 > t3b_l2.out
python3 t3b_tangent_family.py sq 200 0 > t3b_sq.out
python3 t1_theorem1.py 0 40 1.0 > t1_seed0.out
python3 t1_theorem1.py 1 40 2.5 > t1_seed1_big.out
python3 t2_kappa.py 0 30 > t2_seed0.out
python3 t3_adversarial.py sq 150 0 > t3_sq.out
python3 t3_adversarial.py l2 150 0 > t3_l2.out
python3 t4_exactness.py 0 > t4.out
python3 t5_cyclic.py 0 30 > t5.out
python3 t6_squared1d.py 60 150 0 > t6.out
python3 t7_overlap.py 0 > t7.out
python3 t9_hardness.py > t9.out
```

`t8_edge.py` uses no squared lengths and was not rerun after the review. No
project-wide checks were run, and no CI was inspected.
