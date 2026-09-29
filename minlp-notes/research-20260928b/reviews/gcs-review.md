# Review: a priori integrality-gap bounds for shortest paths in graphs of convex sets

Date: 2026-09-28. Reviewed document:
[gcs/a-priori-gap-bounds.md](../gcs/a-priori-gap-bounds.md) (the "note"). Reviewer code
and logs: [reviews/gcs/](gcs/). The reviewer did not write the note and did not edit it.

## Verdict

The note is mathematically sound. Every theorem and proposition survives, and every
explicit example reproduces with independent code. Four statements need corrections, and
none of them changes a main result:

1. **Corollary C (squared lengths) is stronger than stated.** Optimized over enclosing
   balls, the enclosing-ball bound is *exact*: `κ^sq_e = inf_B sec²θ_B`, and this value
   is computable by a convex program (proof in §4). So the scout's Kantorovich product
   bound is never better. The note's claims "for thin arcs the scout's bound is better"
   and "neither dominates in general" are false. They hold only against a fixed ball,
   such as the minimum-radius ball or the centroid-centred ball the author's code uses.
2. **Prop. 12 construction.** The sets are not pairwise disjoint. Literal sets in the
   same layer intersect. Sets on adjacent layers are disjoint, and a height stagger
   repairs the claim.
3. **Prop. 11 label.** The algorithm is a PTAS only when `D/δ` is bounded (or given in
   unary). The stated running time itself is correct.
4. **Minor numerical and scope statements:**
   - In Prop. B′, the ratio is `1/2 + O(θ⁴)`. It exceeds `0.5000` at `23.6°`
     according to the author's own output.
   - In Prop. 10, `sec θ_door = 1.118` holds for `H ≥ 1`, not for every `H`.
   - Bound (3) needs `g_e ≥ 0` for its second inequality.
   - In Theorem 1, the pair-graph node count is an upper bound, not an equality.

**Novelty.** The results are plausibly new as statements about GCS relaxations. No GCS
source that could be checked states an a priori gap bound. The ingredients, however, are
standard, and several items are known or routine:

- Corollary A;
- Prop. 2(2), which is the RLT-on-a-simplex fact;
- Prop. 5.2, a small variant of SIOPT Example 5.10;
- Prop. 11;
- Prop. 12.

## Per-claim verdicts

Legend: **C** correct, **CF** correct with fixes, **G** gap, **F** false.

| Claim | Verdict | Evidence / note |
|---|---|---|
| §1 definition of `REL` vs SIOPT (5.5) and thesis (9.5) | C | See §1 of this review |
| §1 `REL_H` = projection of SIOPT (7.4) / thesis Lemma 8.2 | C | With (D), the `ŷ = 0` term absorbs `x_v`. Without (D), `REL_H` is the conic analogue |
| `REL ≤ REL_H ≤ OPT` | C | Checked by proof and on all instances |
| Theorem 1 (chain, marginals, conditional independence, means, Jensen, derandomization, bound (1)) | C | Minor: the pair graph has *at most* the stated number of nodes. Exact enumeration on 120 DAGs, 0 violations (r2) |
| Theorem 1 remarks (no need for `ℓ ≥ 0` or (D); a posteriori edge-constraint version; vertex costs) | C | Includes negative affine lengths (r2) |
| Corollary 1.1, bound (2) | C | Variance identity and triangle inequality |
| Corollary A (affine ⇒ `REL_H = OPT`) | C | Not new; see Novelty |
| Prop. A′ (`REL = 0`, `REL_H = OPT = 2`) | C | Reproduced exactly (r1) |
| Corollary B, inequality (3) | CF | The second inequality `Σ κ_e ℓ̃_e ≤ κ_max REL_H` needs `ℓ̃_e ≥ 0`, which fails for a linear, negative `g_e` with `κ_e = 1`. State (3) for `g_e ≥ 0`, e.g. norms |
| Cor. B properties 1–3 (`κ = 1` ⇒ affine; `κ = sec θ`; finiteness iff `θ < π/2`; balls sharp) | C | The correction to the scout's "iff disjoint" is right |
| Prop. B′ (tangent family, `c* ≥ 1/2`) | C (analytic) / CF (numerics) | "0.5000 to four digits for θ from 2.9° to 23.6°" is wrong. The author's t3b gives 0.5005 at 23.578°; exact values are 0.500015 (10°), 0.500245 (20°), 0.50134 (30°). The limit `1/2` is unaffected |
| Open Question 1 (`1/2 ≤ c* ≤ 1`) | C | The heuristic for `c* < 1` is correctly labelled as a heuristic |
| Cor. C.1 enclosing-ball bound; equality for balls | C, and strengthened | Optimized over balls, it equals `κ^sq_e` exactly (§4) |
| Cor. C.2 radial segments | C | Reproduced (1.125, 1.8) |
| Cor. C.3 product bound valid | C | — |
| Cor. C.3 / Summary: "neither dominates"; "thin arcs: scout's bound is better" | **F** | The best ball always equals the true `κ^sq`. 0 of 210 polygons favour the product bound (r4, r4b) |
| Example C′ (1D, squared: 12.25 vs 12.375; Euclidean exact) | C | Reproduced |
| Prop. 2 (1)–(3) | C | (2) is the classical RLT/simplex fact. REL = REL_H to 1e−10 on triangles and intervals (r9) |
| Prop. 3 and bound (4) | C | 25 DAGs, 0 violations (r8) |
| Prop. 4 (crossing family) | C | Formulas reproduced. `R²(OPT/REL_H − 1)` → about 0.1036, consistent with "0.104" (r1b) |
| Theorem 5 (walks on cyclic graphs) | C | 90 cyclic rows plus 33 injected circulations, 0 violations (r3) |
| Corollary 5.1 (common quasi-metric ⇒ paths) | C | Holds on all common-norm cyclic rows |
| Prop. 5.2 (C2, C3) | C | 1.5 / 0.5 / walk 1 / cuts give 2, reproduced. Cite SIOPT Ex. 5.10 as the base |
| Open Question 2 | — | Not attempted |
| Prop. 6 (translation constraints) | C | Reproduced: infeasible, `REL = REL_H = 0`; with bypass `OPT = 1` |
| Theorem 7 (line-graph reformulation) | C | Algebra checked. 70 random region DAGs (9 with gaps), `REL_H(G) ≤ REL(L)` always (r5b, r5c) |
| Thm. 7 scope (order-1, Bézier `d ≥ 2η+1`, time-scaling coupling, dynamics) | C | Checked against Science Robotics (7)–(10) |
| t8 Bézier ring numbers | C | Reproduced independently (r7) |
| Prop. 8 and `max_P ΣΔ = 2 − δ²` | C | Reproduced |
| Corollary 8.1 | C | — |
| Prop. 9 (region formulation, `REL ≥ |goal − start|`, ring values) | C | Reproduced with lifted two-cycle cuts (Science Robotics A.1 + SIOPT Lemma 5.4) and the region hull |
| Prop. 10 (door formulation) | CF | The proof is correct. "`sec θ_door = 1.118` for every `H`" holds for `H ≥ 1`: at `H = 0.5` it is 1.414 and at `H = 0.25` it is 2.236 (r8) |
| Open Question 4 | — | Not attempted |
| Prop. 11 (fixed dimension) | CF | The error analysis and running time are correct. Call it a PTAS only for bounded `D/δ` |
| Prop. 12 (`1 + tan²θ/(3N(m+1)²)` hardness) | CF | The reduction and arithmetic are correct. "Pairwise-disjoint polytopes" is false as constructed. Also needs `tan θ ≤ 3√N` for `L ≥ 1/3` (pad `N`) |
| Consequence for relaxations (§7.2) | C | — |
| §7.3 obstacle discussion | — | Heuristic, correctly labelled |
| §9 novelty caution | C, with additions | See Novelty |

## 1. Definitions against the sources

I read SIOPT (5.1)–(5.6), Lemma 5.4, Remark 7.2, (7.4) and Lemma 7.4 in the PDF
(`literature/papers/marcucci2024-shortest-paths-in-graphs-of/original.pdf`). The
markdown full text omits the displayed equations. I also read thesis (8.1)–(8.5),
Lemma 8.2, Prop. 8.2, §8.5 and §9.3.

- **Degree constraint.** SIOPT (5.5c) is `Σ_{out(v)} y ≤ 1`. The note writes the in-edge
  form, which is equivalent under conservation. The thesis (9.5c) writes both sides. The
  thesis §9.3.3 and the SIOPT text after Example 5.10 say (D) is redundant on DAGs. The
  note uses it the same way.
- **Position conservation.** SIOPT (5.5d) conserves the pair `(z′, y)` at internal
  vertices only. So the source and target positions may differ between first edges and
  between last edges. The lifted constraints (5.6) are redundant. The note's (F), (C) and
  (P) match this, including its boundary conventions for `s` and `t`. The edge
  perspective (P) with `X̃_e` matches thesis (9.5f). SIOPT encodes edge constraints
  through `ℓ_e = +∞`; the note keeps them separate and assumes `ℓ_e` finite on `K_e`.
- **Hull.** `Y_v = {y ≥ 0 : Σ_in y = Σ_out y ≤ 1}` has vertices `0` and `1_e + 1_f`, and
  `Y_v` is a scaled product of two simplices. In the SIOPT (7.4) hull, the copy for
  `ŷ = 0` carries `x_0 ∈ λ_0 X_v` and appears only in `x_v`. Projecting out `x_v` gives
  (H1)–(H2) plus `Σ λ_ef ≤ 1`, which is (D). Without (D), `REL_H` is the homogeneous
  version. At `s` and `t` the hull reduces to (P). The claims that (H) implies (C) and
  the vertex part of (P) are correct.

## 2. Theorem 1, step by step

- **Termination.** Correct. Every chosen edge has `y > 0`, since `λ_de ≤ y_e`.
  Conservation excludes dead ends carrying flow.
- **Marginals.** Correct. On a DAG, `v` is visited at most once, so the events
  `{e ∈ P}`, `e ∈ in(v)`, are disjoint. The column sums of (H2) give `y_f`.
- **Conditional independence.**
  - *Correct.* The edge `e` occurs at most once, so `{e ∈ P}` is a disjoint union over
    times `k` of `{X_k = e}`. For each `k`, the Markov property gives
    `P(X_{k−1} = d, X_{k+1} = f | X_k = e) = P(X_{k−1} = d | X_k = e)·λ_ef/y_e`.
  - *The law of the next edge does not depend on `k`.* Summing over `k` gives
    `P(d, e, f consecutive) = λ_de λ_ef / y_e`. Exact enumeration confirms this to 4e−7
    (r2).
  - *Where it is used.* Conditional independence is needed only for the closed-form
    `E[cost]`. The Jensen bound uses only the two conditional marginals, whose means are
    `z̄_e` and `z̄′_e` by (H2).
- **Jensen step.** Correct, and it does not need convexity: `cav_e` is defined as a
  supremum over finite mixtures. Convexity is used only for `REL_H ≤ OPT`.
- **Derandomization.** Correct. The chain's trajectories are exactly the source–sink
  paths of the pair graph, so the minimum is at most the average. The pair graph has *at
  most* `Σ_v |in(v)||out(v)| + |out(s)| + |in(t)|` nodes.
- **Last inequality of (1).** Correct. A unit flow on a DAG decomposes into s–t paths,
  and `Δ_e ≥ 0`.
- **Cycles.** Correctly deferred to Theorem 5. Acyclicity is used only for termination
  and for the disjointness in the marginal and independence steps.

**Numerical audit (r2).** The audit used 120 random layered DAGs:

- dimensions 1–3;
- sets: points, boxes, segments, triangles;
- lengths: Euclidean, squared, `ℓ1`, and random affine lengths that may be negative;
- degree constraints on or off;
- small and large (overlapping) sets.

For each instance, every chain trajectory was enumerated with its probability. I checked
`Pr(e ∈ P) = y_e`, `Pr(d, e consecutive) = λ_de`, the product form, the conditional
means, the closed form, and the chain

`REL ≤ REL_H ≤ OPT ≤ min pair-graph path ≤ E ≤ Σ y cav ≤ REL_H + Σ yΔ ≤ REL_H + max_P ΣΔ`.

There were 0 violations, and 10 instances had `OPT > REL_H`.

## 3. Corollaries and extensions

- **Corollary 1.1.** The step `E‖X − a‖ ≤ (E‖X − c‖² − ‖a − c‖²)^{1/2} ≤ R_u` is right.
  The symmetric use of `g` needs `g(w) ≤ Λ‖w‖` for all `w`, which holds for norms.
- **Corollary A.**
  - Both proofs are right.
  - The second proof reduces to the flow LP on the line graph. (D) is redundant there on
    DAGs because each path visits `v` once.
  - Reconstructing positions needs linear-optimization oracles; values alone need only
    support-function oracles.
- **Corollary B.**
  - The proof is right.
  - *Fix.* (3) combines `OPT ≤ Σ κ_e ℓ̃_e` with `≤ κ_max Σ ℓ̃_e`. The second step needs
    `ℓ̃_e ≥ 0`. If `κ_e > 1`, then `g_e ≥ aᵀw ≥ 0` on `D_e` holds automatically.
  - *Failure without it.* If `κ_e = 1`, `g_e` can be linear and negative on `D_e`. Then
    any exact instance with `REL_H < 0` violates `OPT ≤ κ_max REL_H` whenever
    `κ_max > 1`.
  - *Recommendation.* State (3) for nonnegative `g_e`.
- **Properties 1–3 of Cor. B.**
  - `κ = sec θ` follows from `‖a‖ ≤ 1`, which gives `cos∠(a, w) ≥ 1/κ`.
  - The counterexample to the scout's "only if" is valid: `X_u = {0}` and a segment
    starting at `0` give `κ = 1`.
  - The ball sharpness computation is right. The tangent points have norm
    `√(d² − ρ²)` and their mean has norm `(d² − ρ²)/d`.
- **Prop. B′.**
  - `|P_±| = D` checks out.
  - The segment `sP_+` is tangent to `A` at `T_+`, so OPT is `4√(D² − r²)`.
  - The explicit `REL_H` point is valid. `A` has in-degree 1 and `B` out-degree 1, so the
    hull is canonical and `REL = REL_H`.
  - The bound `cos θ/(1 + cos θ) → 1/2` is right.
  - Numerically, the ratio exceeds `1/2` at finite `θ` by about `θ⁴`: `score − 1/2` is
    1.5e−5 at 10°, 2.5e−4 at 20° and 1.3e−3 at 30° (r1b).
  - The note's "0.5000 to four digits up to 23.6°" contradicts `gcs/code/t3b_l2.out`,
    which prints 0.5005 at 23.578°. The note's local search also divided by a numerically
    computed `κ_max` slightly above `sec θ`, which deflates its scores. None of this
    affects `c* ≥ 1/2`, since `c*` is asymptotic.
- **Corollary C.** See §4. C.1, C.2 and the validity of C.3 are correct. The comparison
  statements are false.
- **Example C′.** Both routes cost 12.375. `REL = REL_H = 12.25`, with departures at
  1.5 and 2.5. The Euclidean relaxation is exact. All reproduced.
- **Prop. 2.**
  - (1) is correct.
  - (2) is correct. The barycentric gluing is fine. This is the standard fact that
    first-level RLT, or here the Lemma 5.4 relaxation, equals `conv S` when one factor is
    a simplex: the RLT rows give `Z_i ∈ x_i P`.
  - (3) is correct. A non-simplex compact convex set has affinely dependent extreme
    points; Radon gives size `n + 2`; and extreme points force `w̄_ij = p_i = p_j`.
  - The 1D consequences, including cyclic 1D with Euclidean lengths via Cor. 5.1, are
    correct.
- **Prop. 3 / bound (4).**
  - The repair moves only tail copies `z_f` of out-edges of `v`.
  - Arrival copies `z′` are untouched, so repairs at different vertices do not interact.
  - Each edge's cost changes through its tail only.
  - Flow decomposition then gives (4).
  - 25 DAGs (6 with gaps), 0 violations (r8).
- **Prop. 4.**
  - The formulas reproduce (r1).
  - `OPT − REL` equals 1.530, 1.468, 1.440, 1.427 and 1.421 for `R` = 5, 10, 20, 40
    and 80, tending to `√2`.
  - `R²(OPT/REL_H − 1)` equals 0.1089, 0.1062, 0.1049, 0.1042 and 0.1039 for `R` = 20,
    40, 80, 160 and 320. The limit extrapolates to about 0.1036.
  - `sec θ − 1 ≤ 1/(R² − 2)` is right, since `sec θ − 1 = (sec²θ − 1)/(sec θ + 1)`.
- **Theorem 5.**
  - The closed-set argument for `U` is right. Summing the column identities over `U`
    forces zero initial mass on `U` and zero inflow into `U`.
  - `y_T = π_0(I − P_TT)^{-1}` holds, because predecessors of `T` lie in `T`.
  - The expected triple counts `λ_de λ_ef / y_e` are right.
  - `WALK*` is the infimum over `K` in arXiv 2507.10878 (2). The inequality
    `REL_H^{no deg} ≤ WALK*` holds because each finite walk yields a `REL_H^{no deg}`
    point of no larger cost (Jensen on repeated traversals).
  - Numerical check (r3): 48 random cyclic instances × {deg, no deg}, with lengths
    Euclidean, squared, or Euclidean with a different weight per edge:
    - 0 violations; 10 rows had `REL_H < OPT`, and 3 had a walk shorter than `OPT`;
    - the closed form matched Monte Carlo;
    - injecting a circulation into `U` gave no inflow, and the expected visits equalled
      `y` on `T` to 5e−11.
- **Corollary 5.1.** Correct. The shortcut uses the edge `(v, v_{j+1})` of the walk and
  only the triangle inequality of the common `d`.
- **Prop. 5.2.**
  - Reproduced: `REL_H(deg) = 1.5`, `REL_H(no deg) = 0.500`, shortest walk 1, and
    two-cycle cut 2.0.
  - For C3: 1.5, still 1.5 with two-cycle cuts, and 2.0 with the GSEC on `{1, 2, 4}`.
  - The instance is SIOPT Example 5.10 with `X_1` shrunk to `[−1/2, 1/2]` and a parallel
    route `s→3→t` added. The note should cite Example 5.10 as the base.
- **Prop. 6.** Correct and reproduced.
- **Theorem 7.**
  - *Claim 1* follows from (H) and partial minimization.
  - *Claim 2* holds by the substitution `σ_e = Γ_u x_u`.
  - *Claim 3.* The constructed point satisfies (H) and the perspective edge equality
    `Λ_v z′_e = T_e Γ_u z_e + t_e y_e`. The vertex-cost step is subadditivity of the
    perspective, and the source and target boundary cases work.
  - *Claim 4* is immediate.
  - *Numerical check (r5b, r5c).* On 70 random acyclic region DAGs, 9 of which had
    region-formulation gaps up to 9.8%:
    - `REL_H(G) ≤ REL(L)` to 2e−7;
    - `OPT(G) = OPT(L)`;
    - the line graph closed 8 of the 9 gaps fully and reduced the ninth to 0.01%.
  - *Bézier ring (r7).* `REL_region = REL_H,region = 3` and
    `REL_line = REL_H,line = OPT` = 4.23607, 12.04988, 42.01250 for `H` = 1, 5, 20.
    These match the note's t8.
- **Scope bullets (Science Robotics (7)–(10)).**
  - With only (7a) and `d ≥ 2η + 1`, the entry block `r_{0..η}` and exit block
    `r_{d−η..d}` are disjoint, so (H) holds.
  - With the absolute time scaling `h`, (7b)/(7d) couple the entry and exit times
    (monotonicity), so (H) fails, as stated.
  - With `d = 2η + 1`, (7c) links `r_η` and `r_{η+1}`. So "velocity limits need (H) to
    be checked" is right.
- **Prop. 8, Cor. 8.1.** Correct. `max_P ΣΔ = 2 − δ²` is confirmed with an exact `Δ`
  computation.
- **Prop. 9.**
  - The telescoping in (1) needs only conservation and continuity, so it holds with
    cuts, the hull and cycles.
  - For (2), my implementation of the lifted two-cycle cuts reproduces
    `REL = REL_H = REL + cuts = REL_H + cuts = 3` and the closed-form OPT for
    `H` = 1, 2, 5, 20. The ratio is 14.004 at `H = 20`.
- **Prop. 10.**
  - The chord argument (1) and the reduction (2) to Cor. 5.1 plus Cor. B are right.
  - The door relaxation is numerically exact for all tested `H`.
  - The aperture value 1.118 is correct for `H ≥ 1`. For `H < 1`, the doors `L∩T` and
    `L∩B` in region `L` give `tan θ = 1/(2H)`.
- **Prop. 11.**
  - Correct as a statement about running time. The grid count can be tightened to
    `(1 + D√n/(εδ))^n`.
  - The time is exponential in the bit size of `D/δ`, so "PTAS" should read "PTAS for
    bounded (or unary) `D/δ`". The note's own consequence sentence, "needs growing
    dimension or growing `D/δ`", is consistent with that.
- **Prop. 12.**
  - The reduction, the triangle-inequality bound with `M ≤ m − 1`, and the ratio
    arithmetic are right.
  - Check (r6) on the unsatisfiable 2-CNF (`N = 2`, `m = 4`): `OPT − (m+1)L` is 0.101,
    0.0311 and 0.00926 at 30°, 10° and 3°. These exceed the note's lower bounds 0.049,
    0.015 and 0.0046. The satisfiable subformula has `OPT = (m+1)L`.
  - *Fix.* Literal sets in the same layer intersect: `{x_1 = 1} ∩ {x_2 = 1} = {(1,1)}`
    at the same height. So "pairwise-disjoint polytopes" is false. Two repairs are
    possible:
    - claim only that adjacent sets are disjoint; or
    - put literal `j` of layer `i` at height `iL + jη` with `0 < η ≪ L`. The YES value
      is unchanged, because the vertical displacements telescope to `(m+1)L` and the cost
      is at least the total vertical displacement, with equality iff there is no lateral
      motion. The NO bound changes by `O(η)`, and `L` must grow slightly to keep
      apertures at most `θ`.
  - *Hypothesis.* `L ≥ 1/3` requires `tan θ ≤ 3√N`; pad `N` if needed.
  - On this tiny instance `REL = REL_H = OPT`.

## 4. Correction to Corollary C: the enclosing-ball bound is exact

**Claim.** Let `D` be compact and convex with `0 ∉ D`, and let `q = ‖·‖²`. Then

```
κ^sq(D) := sup_{w∈D} cav_D(q)(w)/q(w)
         = inf{ ‖c‖²/(‖c‖² − ρ²) : D ⊆ B(c, ρ), ρ < ‖c‖ }
         = 1/(1 − τ*),   τ* := min_u max_{w∈ext D} ( ‖w‖²‖u‖² − 2wᵀu + 1 ).
```

**Proof.**

- *Upper bound.* The first `≤` is the note's C.1.
- *Convex form.* Substitute `u = c/‖c‖²`. Then `‖w − c‖²/‖c‖² = f_w(u)`, where
  `f_w(u) := ‖w‖²‖u‖² − 2wᵀu + 1`. The largest radius needed is attained at extreme
  points, so the infimum over balls equals `1/(1 − τ*)`. Each `f_w` is convex, so `τ*`
  is a convex (SOCP/QP) problem. For polytopes, `ext D` is finite; for `D_e` it consists
  of differences of vertices of `X_v` and `X_u`.
- *`u* ≠ 0`.* Since `0 ∉ D`, some ball contains `D` but not `0`, so `τ* < 1 = f_w(0)`.
- *Optimality condition.* At the minimizer, there are active points `w_i` with
  `f_{w_i}(u*) = τ*` and weights `μ_i ≥ 0` summing to 1 such that
  `Σ μ_i ∇f_{w_i}(u*) = 0` (Danskin). Since `∇f_w(u) = 2‖w‖²u − 2w`, this gives
  `w̄ := Σ μ_i w_i = S u*` with `S := Σ μ_i ‖w_i‖²`.
- *Value of the mixture.* Averaging the active equalities gives `τ* = 1 − S‖u*‖²`. Hence
  `Σ μ_i q(w_i)/q(w̄) = 1/(S‖u*‖²) = 1/(1 − τ*)`.
- *Lower bound.* `w̄ ∈ D` is a mixture of points of `D`, so
  `κ^sq ≥ cav_D(q)(w̄)/q(w̄) ≥ 1/(1 − τ*)`.
- *General `D`.* For general compact `D`, approximate from inside by polytopes `P`.
  `κ^sq` is monotone under inclusion, and `τ*` is continuous in the Hausdorff metric. ∎

**Consequences for the note.**

- `κ^sq_e` is exactly `sec²θ*_B`, where `θ*_B` is the smallest angular radius, seen from
  the origin, of a ball containing `D_e`. It is computable in polynomial time.
- The Kantorovich product bound is another upper bound on the same quantity, so it is
  never better. The recommendation "use the minimum of the two" should become "compute
  the best ball".
- A ball of angular radius `θ_B` lies in the cone of half-angle `θ_B`. Hence
  `κ^sq_e ≥ κ_e²`. This makes the note's interpretation exact: the squared case loses
  the square of the angular factor, plus radial dispersion.

**Numerical confirmation (r4, r4b).** `κ^sq` was computed by bisection with a concave
inner problem.

| Set | True `κ^sq` | Best ball | Other bounds |
|---|---|---|---|
| Balls | `sec²θ` (1.0101, 1.0989, 1.5625) | equal | product bound gives `sec⁴θ` |
| Circular segment, `φ = 30°` | 1.33333 | 1.33333 | product 1.34024, minimum-radius ball 1.5 |
| 150 random polygons (r4b) | — | equal to `κ^sq` (max relative difference 5e−8) | product bound never strictly better |
| 60 more random polygons (r4) | — | never worse than the product bound | product bound never strictly better; no bound violated |

The note's thin-arc remark compares against a fixed ball. The author's `gcslib.circ()`
uses the vertex centroid as the centre, which is neither optimal nor minimum-radius.

## 5. Novelty assessment

**Searched.**

- Local sources:
  - SIOPT 2024 (PDF, §§2, 5, 7);
  - the Marcucci thesis (Ch. 8, §§9.3–9.5);
  - Science Robotics (arXiv 2205.04422, §5 and App. A);
  - arXiv 2507.10878, 2409.19543 and 2507.19210;
  - Tawarmalani et al., Math. Program. 2026 (local full text; it cites GCS only as an
    application).
- The arXiv API: all 41 abstracts matching "graph(s) of convex sets", plus five keyword
  queries on integrality, rounding, perspective with shortest path, concave envelope and
  approximation.
- OpenAlex: all 64 works citing SIOPT 2024 (titles, and abstracts for five candidates).
- Unavailable: web search (session quota exhausted), and Semantic Scholar and OpenAlex
  full-text search (rate-limited).

**Finding.** No GCS source states an a priori integrality-gap bound, a rounding
guarantee, or an approximation ratio. The SIOPT paper and the thesis give only the
arbitrarily loose §9.4 example and empirical statistics. The thesis §9.5 rounding has no
cost guarantee. 2507.19210 and 2409.19543 give lower-bound machinery (measures,
quadratic cost-to-go), not gap bounds.

**Per item.**

- **Theorem 1.** Plausibly new as a GCS statement; a referee may see it as elementary.
  Its ingredients are:
  - flow decomposition of pair (line-graph) flows by a Markov chain;
  - Jensen's inequality and concave envelopes for first-moment relaxations;
  - the disjunctive hull, which SIOPT (7.4) already writes down.
- **Corollaries B and C.**
  - The `sec θ` and ball constants are plausibly new.
  - The exact characterization of §4 is a small addition. It rests on the classical fact
    that `cav_D(‖·‖²)` is the lower envelope of the affine majorants coming from
    enclosing balls.
- **Corollary A.** Not new: it is network-flow or DP-extended-formulation integrality
  after projection. SIOPT §7.2 already notes the hull via disjunctive programming. The
  note says this itself.
- **Prop. 2.**
  - (2) is the known fact that RLT is exact on a simplex factor.
  - (3) generalizes thesis Prop. 8.1 (the square example).
  - (1) is trivial.
- **Prop. 3.** A standard optimal-transport repair.
- **Theorem 5 and Cor. 5.1.** Routine given Theorem 1. The walk/path distinction follows
  2507.10878.
- **Prop. 5.2.** A small variant of SIOPT Example 5.10.
- **Theorem 7.**
  - The line graph of region intersections is used as a heuristic search graph in "Fast
    path planning through large collections of safe boxes" (arXiv 2305.01072, IEEE T-RO
    2024). OpenAlex lists it among the works citing SIOPT; its full text was not checked.
  - The dominance statement `REL_H(G) ≤ REL(L)` and the (H) criterion are plausibly new.
- **Props. 9–10.** The ring family and the door-aperture bound are plausibly new
  examples and corollaries.
- **Prop. 11.** Routine grid discretization, in the style of classical approximation
  schemes for geometric shortest paths.
- **Prop. 12.** A direct adaptation of thesis Theorem 9.1, adding a time axis and a
  standard gap argument. The resulting `1/poly` gap is modest.

## 6. Required corrections (precise list)

1. **Summary, §3.3 C.3 and §10 item 4.** Replace "for thin arcs the scout's bound is
   better … neither dominates in general" with the exact characterization of §4:
   `κ^sq_e = inf_B sec²θ_B = 1/(1 − τ*)`. The product bound is valid but never better.
2. **§3.2, sentence after Prop. B′.** Replace "0.5000 to four digits for θ from 2.9° to
   23.6°" with: "0.50000 at 2.9°, 0.5005 at 23.6°; the ratio is `1/2 + O(θ⁴)`." Qualify
   "local search did not exceed 0.5000", which was seeded at `θ = 11.5°` and scored with
   a numerical `κ_max > sec θ`.
3. **Corollary B, (3).** Add "`g_e ≥ 0`", or state the second inequality only when all
   `ℓ̃_e ≥ 0`.
4. **Theorem 1(3).** Replace "has … nodes" with "has at most … nodes".
5. **Prop. 5.2.** Cite SIOPT Example 5.10 as the base instance.
6. **Prop. 10 and Summary.** Replace "1.118 for every `H`" with "for every `H ≥ 1`".
7. **Prop. 11 and Summary.** Replace "PTAS" with "(1+ε)-approximation in time
   `poly(|V|)·(1 + D√n/(εδ))^n`; a PTAS for bounded `D/δ`".
8. **Prop. 12.** Drop "pairwise-disjoint" or add the height stagger. Add
   `tan θ ≤ 3√N` (or padding) for `L ≥ 1/3`.
9. **Prop. 2(2).** Note that it is the standard fact that RLT (Lemma 5.4-type) is exact
   when one factor is a simplex.

## 7. What remains unchecked

- **Recalled sources, not fetched:**
  - Martin–Rardin–Campbell (1990);
  - the Ceria–Soares and Günlük–Linderoth texts (local summaries not reopened);
  - the exact reference for the RLT/simplex exactness fact;
  - classical discretization schemes for geometric shortest paths;
  - Arkin–Hassin and the approximation literature on TSP with neighbourhoods;
  - the full text of arXiv 2305.01072.
- **Touring polygons.** The Dror–Efrat–Lubiw–Mitchell NP-hardness wording behind "exact
  solution is NP-hard in 2D" was taken from the scout and was not re-derived.
- **Unavailable searches.** Web search was not available (quota exhausted). Semantic
  Scholar and OpenAlex full-text search were rate-limited. Unsuccessful searches do not
  establish novelty.
- **Not rerun.** The note's t8 Bézier corridor instances beyond the ring, its t3
  adversarial templates (best 0.2), and its t2 / t6 runs. My own checks replace them
  where noted.
- **Open questions 1–4 and scout Q2** were not attempted. For Q1, I only reasoned
  briefly about binary fork trees. There is a tension between grazing (maximal Jensen
  loss) and bouncing (path optimality), which is consistent with the note's heuristic
  for `c* < 1`.
- **The author's code** was not audited line by line. Two observations:
  - `circ()` uses a centroid-centred ball (see §4).
  - The squared-length perspective uses cvxpy's `quad_over_lin(·, y)`. In my runs,
    Clarabel falsely reported this construct *infeasible* on several random instances
    until I replaced it with an explicit rotated-cone epigraph. The author's `relax`
    returns `inf` in that case. Their `.out` files show no `inf` rows or violations, so
    their reported runs appear unaffected, but future runs should use the explicit cone.

## 8. Computations (targeted local checks only)

- **Environment and scope.**
  - Python 3.13, cvxpy 1.9.3 with Clarabel (tight tolerances) and SCS as a fallback.
  - `OMP_NUM_THREADS=1`; every run took minutes on one core.
  - All commands ran in `research-20260928b/reviews/gcs/`. They use only the reviewer's
    `rgcs.py` (REL, REL_H, degree/two-cycle/GSEC/lifted cuts, exact OPT by simple-path
    enumeration, chain and pair-graph tools, `cav`/`Δ` by LPs over vertices).
  - No project-wide checks were run, and no CI status or logs were inspected.
- **Harness fixes during the review.** The results below come from the final version of
  the harness.
  - The squared-length perspective was changed to an explicit cone.
  - Pair points with `λ < 1e−6` are dropped and barycentres are projected onto their
    sets. Without this, solver noise gave spurious out-of-set positions.

| Command | Checks | Result |
|---|---|---|
| `python3 r1_examples.py` | Props A′, B′, C′, 4, 5.2 (C2, C3), 6, 8 | All values as in the note (see §§2–3) |
| `python3 r1b_prop4_limit.py` | Prop. 4 limit; B′ score vs θ | 0.1089 → 0.1039 (`R` up to 320); score `1/2 + O(θ⁴)` |
| `python3 r2_theorem1.py 0 30 1.0`, `… 1 30 2.5`, `… 2 30 1.5 hard`, `… 3 30 2.0 hard` | Theorem 1 by exact chain enumeration | 120 DAGs, 0 violations, 10 with gaps |
| `python3 r3_cyclic.py 0 24`, `… 1 24` | Theorem 5, Cor. 5.1, bad-set handling | 90 rows plus 33 circulations, 0 violations |
| `python3 r4_squared.py`, `python3 r4b_ball_exact.py` | Cor. C bounds vs true `κ^sq` | Best ball = `κ^sq` on 150 random polygons (5e−8) and on all special sets; product bound never better on 210 polygons |
| `python3 r5_ring_door.py` | Props. 9–10 on the ring | As in the note; `sec θ_door = 1.11803` |
| `python3 r5b_thm7_corridors.py`, `python3 r5c_thm7_gaps.py` | Theorem 7 claim 3 | 70 DAGs, 0 violations |
| `python3 r6_hardness.py` | Prop. 12 | Bounds hold; same-layer sets intersect |
| `python3 r7_bezier.py` | Bézier C¹ ring (t8) | Reproduced |
| `python3 r8_repair_door.py` | Prop. 3 / (4); door aperture for `H < 1` | 0 violations; 2.236 / 1.414 / 1.118 / 1.118 |
| `python3 r9_simplex.py` | Prop. 2(2) | `REL = REL_H` to 2e−10 on triangles and intervals |
