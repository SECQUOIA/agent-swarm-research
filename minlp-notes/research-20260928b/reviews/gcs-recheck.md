# Recheck of the revised note on a priori gap bounds for GCS shortest paths

Date: 2026-09-29. Rechecked document:
[gcs/a-priori-gap-bounds.md](../gcs/a-priori-gap-bounds.md) (the "note"), as revised after
[the first review](gcs-review.md). Scripts and logs: [gcs-recheck/](gcs-recheck/). I had not
seen this material before. I did not edit the note, commit anything, or reuse the author's or
the first reviewer's code: `gcs-recheck/rc.py` is a new implementation written from the
note's definitions in §1.

## Verdict

All six revisions are correct. Theorem 1 also holds, re-derived from the definitions and
confirmed by exact enumeration of the rounding chain. No revised statement is false. What
remains is small:

- **Prop. B′ constant.** The ratio is exactly `1/2 + θ⁴/64 + O(θ⁶)` (series derivation and
  high-precision numerics). The note's "`c ≈ 0.016–0.018`" correctly describes 10°–30°.
  §11's "`c ≈ 0.017`" is a mid-range value, not the limit `1/64 ≈ 0.0156`.
- **Prop. 11 running time.** The Summary and §11 write it as
  `poly(|V|)·(1 + D√n/(εδ))^n`. Dijkstra on the product graph has `|E|·M²` arcs, where
  `M` is the net size, so the exponent is `2n`. The proposition's own wording ("polynomial
  in `|V|`, `|E|` and `(1 + D√n/(εδ))^n`") is correct.
- **Two wording and presentation points and one code defect** that affects no reported
  number: see "Remaining problems".

| Item | Verdict | Main evidence |
|---|---|---|
| (1) Corollary C exact form, `κ^sq_e ≥ κ_e²` | **Correct** | Proof checked step by step. On 415 random sets, the best-ball value and the best exactly evaluated mixture agree (relative gap ≤ 1.1e−7; ≤ 1.2e−5 on one ill-conditioned set). No bound is violated |
| (2) Prop. 12 stagger, disjointness, constant `tan²θ/(4N(m+1)²)`, `tan θ ≤ 3.3√N` | **Correct** | Reduction and arithmetic checked. The note's 2-CNF and a genuine unsatisfiable 3-CNF (`N = 3`, `m = 8`, 6561 paths) hold at 30°, 10°, 3° and at the boundary `tan θ = 3.3√N` |
| (3) Prop. 10 `sec θ_door = max(√5/2, √(1 + 1/(4H²)))` | **Correct** | Derived by hand; the numerical apertures match for 8 values of `H`. The door relaxation is exact for all of them |
| (4) Prop. B′ ratio `1/2 + cθ⁴` | **Correct, constant imprecise** | Exact formula and full `REL_H` solves agree. The limit is `c = 1/64` |
| (5) Prop. 11 as a `(1+ε)`-approximation; PTAS only for bounded `D/δ` | **Correct** | Proof checked; 30 grid runs all within `1 + ε`. Minor exponent slip in the Summary and §11 |
| (6) Rotated-cone formulation; did numbers change? | **Correct; no material change** | The cone is an exact epigraph. Every squared-length value the note reports reproduces under both formulations and both solvers |
| Theorem 1 | **Correct** | Independent proof check; 294 DAGs, 0 violations. This includes 74 instances with `OPT > REL_H` and 50 with nontrivial hull splitting |

## 1. Corollary C (exact squared-length constant)

**Proof check.** Every step holds.

- *Upper bound.* The affine function `α(w) = 2cᵀw + ρ² − d²` satisfies
  `α − q = ρ² − ‖w − c‖² ≥ 0` on `B(c, ρ)`, so `cav_D(q) ≤ α`. Maximizing `α/q` over the ball
  reduces to the axis: `h(r) = (2dr − (d² − ρ²))/r²` has its only critical point at
  `r = (d² − ρ²)/d`. This point lies in `[d − ρ, d + ρ]` and gives the value `d²/(d² − ρ²)`.
- *Reparametrization.* With `u = c/‖c‖²`, `‖w − c‖²/‖c‖² = f_w(u)` holds exactly. A convex
  function of `w` attains its maximum at extreme points. `τ* < 1` iff `0 ∉ D`: if `0 ∈ D`,
  then `f_0 ≡ 1`; if not, take `u = εa` with `a` strictly separating.
- *Lower bound.* `F` is coercive because `min_D ‖w‖ > 0`. Danskin and Carathéodory give
  weights `μ`. Then `Σμ_i ∇f_{w_i}(u*) = 0` gives `w̄ = Su*`, and averaging the active
  equalities gives `τ* = 1 − S‖u*‖²`. The mixture ratio is `1/(S‖u*‖²) = 1/(1 − τ*)`.
- *Supplement* (true, but not stated in the note). The note shows only
  `sup_{K_e} cav_e/ℓ_e ≤ κ^sq_e`, by push-forward. Equality also holds: any finite mixture on
  `D_e` lifts to `K_e` by choosing preimages `(x_i, x'_i)`, and the lifted means differ by
  `w̄`. So `κ^sq_e` is exactly the per-edge ratio on `K_e`, not only an upper bound for it.
- *Consequence 3.* A ball of angular radius `θ_B` lies in the cone of half-angle `θ_B`. Hence
  `θ_e ≤ θ*_e` and `κ^sq_e ≥ sec²θ_e = κ_e²`.
- *Consequence 4.* The product bound is valid by `‖EW‖ ≥ cos θ·E‖W‖` and Kantorovich. So it
  is never below the exact value, and for balls it equals `sec⁴θ`.

**Numerics (`k1_kappa_sq.py`).** I computed `κ^sq` in three independent ways:

- the best ball, via my own SOCP form `τ* = min_u max_i ‖ ‖w_i‖u − w_i/‖w_i‖ ‖²`, which is
  algebraically equal to the note's program;
- the note's linear-row form, whose duals give the Danskin weights;
- the true constant `sup_{p∈Δ} Σp_i‖w_i‖²/‖Σp_i w_i‖²`, computed both by a convex geo-mean
  program (the ratio is homogeneous of degree 0 in `p ≥ 0`) and by SLSQP. SLSQP is
  reliable here because the ratio is quasiconcave.

The comparison is a rigorous sandwich. The upper bound is `1/(1 − F(u))`, evaluated exactly
at the solver's `u`. The lower bound is the best exactly evaluated mixture.

| Sets | n | Max relative gap between upper and lower | Lower > upper | `κ^sq < sec²θ_e` | Product < `κ^sq` |
|---|---|---|---|---|---|
| Random polygons (2D) | 199 | 1.1e−7 | 0 | 0 | 0 |
| Arc-like polygons (2D) | 60 | 2.5e−8 | 0 | 0 | 0 |
| `X_v − X_u`, random polygons (2D) | 98 | 1.2e−5 (1 set with `κ ≈ 5374`; 1.4e−6 after polishing the centre) | 0 | 0 | 0 |
| `X_v − X_u`, random polytopes (3D) | 58 | 7.4e−9 | 0 | 0 | 0 |

- The best ball always contains `D` (to within 2e−14) and has `ρ < ‖c‖`.
- For 78 of the 415 sets, the optimal mixture needs three or more points, so a pairwise
  search would not suffice.
- Special sets:
  - Balls give `sec²θ`, not `sec⁴θ`.
  - A radial segment `[2, 8]` gives 1.5625, with the ball centred at 5.
  - A circular segment at `φ = 30°` gives 4/3, with the ball centred at `1/cos φ`. The
    product bound gives 1.340242 and the minimum-radius ball 1.5.

## 2. Proposition 12 (staggered hardness embedding)

**Proof check.**

- *Disjointness.* The heights `0`, `iL + jη` (`j ≤ 3`, `3η < L`) and `(m+1)L` are all
  distinct, so all sets are pairwise disjoint.
- *Apertures.* The smallest rise is `L − 3η = L_0`, on edges from literal 3 of the last
  layer into `t`. Every other rise is at least `L − 2η`. Lateral motion is at most `√N`, so
  `tan θ_e ≤ √N/L_0 ≤ tan θ`.
- *YES instances.* A constant satisfying assignment costs exactly the telescoped rise
  `(m+1)L`.
- *NO instances.* Take the sub-path between conflicting layers `i < i'`. It has
  `V ≤ (m−1)L + 2η ≤ mL` and lateral displacement at least 1. With
  `√(V² + 1) − V ≥ 1/(2V + 1)` this gives the absolute bound.
- *Ratio.* Since `L_0 ≥ √N/tan θ`, the condition `L ≥ 1/3` is equivalent to
  `tan θ ≤ 3.3√N`. Then `2mL + 1 ≤ 3(m+1)L`. From `L ≤ 1.1·1.01·√N/tan θ` we get
  `3L² ≤ 3.70·N/tan²θ ≤ 4N/tan²θ`.

**Numerics (`k2_hardness.py`).**

- *Algebra grid.* For `N, m ≤ 60`, `tan θ ≤ 3.3√N`, and rounding factor 1 or 1.01: 0
  violations. The minimum slack factor is 1.30, at the boundary. Beyond the hypothesis the
  written chain can fail (factor 0.997 at `N = m = 1`, `tan θ = 5`), so the hypothesis or
  padding is needed.
- *Instances.* Exact `OPT` by enumerating all literal paths (L-BFGS-B per path; the 5 best
  re-solved with Clarabel, agreeing to ≤ 1e−6):

| Instance | θ | Rounding | Disjoint | max `sec θ_e` ≤ `sec θ` | Relative excess of `OPT` | Claimed bound |
|---|---|---|---|---|---|---|
| Note's 2-CNF (`N = 2`, `m = 4`) | 30°, 10°, 3° | 1.00 | yes | yes | 6.83e−3, 6.42e−4, 5.67e−5 | 1.67e−3, 1.55e−4, 1.37e−5 |
| same | 30°, 10°, 3° | 1.01 | yes | yes | 6.70e−3, 6.29e−4, 5.56e−5 | same |
| same | 77.9° (`tan θ = 3.3√2`) | 1.00 / 1.01 | yes | yes | 0.321 / 0.316 | 0.109 |
| Unsatisfiable 3-CNF (`N = 3`, `m = 8`, 6561 paths) | 30°, 3°, 80.1° (boundary) | 1.01 | yes | yes | 1.25e−3, 1.03e−5, 0.109 | 3.43e−4, 2.83e−6, 3.36e−2 |

- All satisfiable subformulas give `OPT = (m+1)L` to about 1e−9.
- The 2-CNF values reproduce the note's t9 exactly: `OPT` = 13.564192, 44.140534 and
  148.424834.

## 3. Proposition 10 (door aperture on the ring)

**Derivation.**

- In region `T`, the displacement set `RT − LT = [2, 4] × [−1, 1]` has half-angle
  `arctan(1/2)`, so its secant is `√5/2`.
- In region `L`, the sets `LB − LT = [−1, 1] × [−2H−2, −2H]` and
  `LT − start = [−1/2, 1/2] × [H, H+1]` have half-angle `arctan(1/(2H))`.
- By symmetry the optimal axis is the obvious one in each case. So
  `sec θ_door = max(√5/2, √(1 + 1/(4H²)))`, with a tie at `H = 1`.

**Numerics (`k3_door.py`).** The apertures come from SOCPs over all vertex differences.

| `H` | 1/8 | 1/4 | 1/2 | 3/4 | 1 | 2 | 5 | 20 |
|---|---|---|---|---|---|---|---|---|
| Computed `sec θ_door` | 4.123106 | 2.236068 | 1.414214 | 1.201850 | 1.118034 | 1.118034 | 1.118034 | 1.118034 |
| Formula | same | same | same | same | same | same | same | same |

- For every `H`, door `REL = REL_H` (with and without degree constraints) `= OPT =
  2 + 2√(H² + 1/4)`, to within 1.5e−8 relative.
- The bound `OPT ≤ sec θ_door·REL_H` therefore holds with room to spare.

## 4. Proposition B′ (tangent family)

**Proof check.** The following all hold:

- the apertures, `|P_±| = D`, tangency at `T_±`, `OPT = 4√(D² − r²)`, the explicit point,
  and `cos θ/(1 + cos θ)`;
- the exact formula `REL_H = 2 min_{p∈A}(p_1 + D + ‖P_+ − p‖)`, by symmetrization, a
  canonical hull (in-degree 1 at `A`, out-degree 1 at `B`), and decoupling through the
  singleton `P_±`.

**Numerics (`k4_tangent.py`, `k4b_series.py`).**

- *Full solves.* The full cvxpy `REL_H` of the graph equals the formula to 1e−6 at 10°,
  20°, 23.578° and 30°, with or without degree constraints.
- *Exact ratios* (mpmath, 60 digits): 0.5000147 (10°), 0.5002455 (20°), 0.5004848
  (23.578°) and 0.5013356 (30°).
  - The note's table (0.500016, 0.500246, 0.500485, 0.501336) matches to ≤ 1.3e−6.
  - Rounded exactly, the last digits at 10° and 20° would be 0.500015 and 0.500245.
  - The column labelled "23.6°" is θ = 23.578°; at 23.6° exactly the ratio is 0.5004867.
- *Asymptotics.* A perturbation series gives ratio = `1/2 + θ⁴/64 + O(θ⁶)`.
  - Numerically, `(ratio − 1/2)/θ⁴` = 0.0156252 at θ = 0.005 rad.
  - The effective value over 10°–30° is 0.0158–0.0178.
  - The optimal relaxed arrival point in `A` sits at polar angle `π/2 + θ/2 + θ³/16`, halfway
    to the tangent point `π/2 + θ`. This is why the exact ratio exceeds `cos θ/(1 + cos θ)`.

## 5. Proposition 11 (fixed-dimension approximation)

**Proof check.** The proof is correct.

- A cell-centred grid of spacing `εδ/√n`, with `⌈D/s⌉ ≤ 1 + D√n/(εδ)` points per axis,
  followed by projection, which is nonexpansive and fixes set points, gives an `h`-net with
  `h = εδ/2`.
- Snapping costs at most `2hK`, and `OPT ≥ Kδ`.
- Shortcutting a Dijkstra walk is valid by the triangle inequality of the common norm.
- The PTAS label is now correctly restricted to bounded (or polynomially bounded) `D/δ`.

**Numerics (`k5_ptas.py`).** I ran 10 random cyclic 2D box instances with the direct
`s→t` edge excluded, each at `ε` = 1, 0.5 and 0.25 (30 runs):

- all net sizes are within the stated count;
- the sampled covering radius is at most `h`;
- every result is within `1 + ε` of the exact `OPT`, with worst `(ratio − 1)/ε = 0.078`.

**Imprecisions.** See "Remaining problems" 2 and 5.

## 6. Rotated-cone formulation for squared lengths

- **Correctness.** `SOC(t + y, [2(z′ − z), t − y])` means `4‖z′ − z‖² + (t − y)² ≤ (t + y)²`,
  that is, `‖z′ − z‖² ≤ t·y` with `t + y ≥ 0`. At `y = 0` it forces `z′ = z`. This is the
  exact epigraph of the perspective.
- **Reported squared-length values.** They reproduce under all four combinations: the
  explicit cone or `quad_over_lin`, each with Clarabel or SCS (`k6_cone.py`, `k4_tangent.py`).

  | Value | This recheck | Note / author output |
  |---|---|---|
  | Example C′: `REL`, `REL_H`, `OPT` | 12.25, 12.25, 12.375 | 12.25, 12.25, 12.375 |
  | Example C′: `κ^sq_max` | 1.8, since `(M+m)²/(4Mm) = 9/5` on `[0.5, 2.5]` | 1.8 |
  | C2 `REL_H` (with degree constraints), with the two-cycle cut | 1.5, 2 | 1.5, 2 |
  | C3 `REL_H`, with two-cycle cuts, with GSEC | 1.5, 1.5, 2 | 1.5, 1.5, 2 |
  | t3b_sq `REL_H` at 2.866°, 11.537°, 30° | 398.50077, 376.21515, 258.87505 | 398.500791, 376.215122, 258.875037 |

  The four combinations agree within 1e−5 relative.
- **Random instances.** On 60 random squared-length DAGs, no combination returned a
  non-optimal status. The maximum deviation from cone/Clarabel was 1e−7 with Clarabel and
  8e−6 with SCS. I therefore could not reproduce the first review's false-infeasibility
  failure; it appears to be instance-specific. The switch is correct either way.
- **Was every affected output regenerated?** File times show that `gcslib.py` changed at
  23:34 and every squared-length output was regenerated afterwards. Only `t8.out`, which
  uses no squared lengths, predates the change, as §11 says. The outputs contain no
  non-finite values, only a few "inaccurate solution" warnings.
- **Limit of this check.** The pre-revision outputs were overwritten, and `research-20260928b/`
  is untracked in git, so a before/after diff of the author's runs is impossible.
  However, every current value the note reports agrees with the independent computations
  here and with the first-version values the review quoted. **No reported number changed
  materially.**

## 7. Theorem 1 (re-derived from the definitions)

**Proof check.** No gap found.

- *Termination.* `λ_de ≤ y_e` and `Σ_f λ_ef = y_e`. A vertex `v ≠ t` without out-edges
  carries no flow.
- *Marginals.* By topological induction. The events `{e ∈ P}`, `e ∈ in(v)`, are disjoint
  because a DAG path enters `v` at most once. Column sums of (H2) then give `y_f`.
- *Conditional independence.* The Markov property.
- *Conditional means.* Row and column sums of (H2). `λ = 0` forces `w = 0` by the
  perspective, and the boundary conventions cover `s` and `t`.
- *Jensen step.* It needs only that `cav_e` is a supremum over finite mixtures in `K_e`,
  not convexity.
- *Derandomization.* The chain's support is exactly the set of source–sink paths of the
  pair graph, and these map to s–t paths of the DAG.
- *Bound (1).* `ℓ̃(0,0,0) = 0` and `y = 0 ⇒ z = 0`. The flow decomposes into s–t paths
  with no cycles, and `Δ ≥ 0`.
- (D) and `ℓ ≥ 0` are indeed never used.

**Numerics (`k7_theorem1.py`).** I enumerated every chain trajectory exactly, with its
probability.

- *Instances.* 294 random DAGs in dimensions 1–3, with points, segments, triangles and
  boxes. Lengths were Euclidean, squared, `ℓ1` and random affine (possibly negative).
  Degree constraints were on or off at random. Three families:
  - optimal points (94 instances);
  - random fractional feasible points, which test parts 1–3 for arbitrary feasible points
    (80 instances; 38 split flow at a vertex with in- and out-degree ≥ 2);
  - mirror-symmetric instances, whose symmetric optima are fractional (120 instances; 74
    with `OPT > REL_H`).
- *Identities.* `Pr(e ∈ P) = y_e`, `Pr(d, e consecutive) = λ_de`, the triple product form,
  the (unnormalized) conditional means and the closed form of `E[cost]` all hold to
  ≤ 1.3e−6.
- *Chain.* `REL ≤ REL_H ≤ OPT ≤ re-optimized ≤ pair-graph DP = best trajectory ≤ E ≤ Σ y cav
  ≤ REL_H + Σ yΔ ≤ REL_H + max_P ΣΔ` had 0 violations. For non-optimal points, the chain
  starts at `OPT` and uses the point's own cost in place of `REL_H`.

## Remaining problems

None of these affects a theorem.

1. **Prop. B′, §3.2 and §11 item 2.** Replace "`c ≈ 0.017`" (and optionally
   "`c ≈ 0.016–0.018`") with the exact expansion
   `(OPT/REL_H − 1)/(sec θ − 1) = 1/2 + θ⁴/64 + O(θ⁶)`. Keep the tested values as finite-θ
   data.
2. **Summary and §11 item 7, time of Prop. 11.** `poly(|V|)·(1 + D√n/(εδ))^n` should read
   `poly(|V|)·(1 + D√n/(εδ))^{2n}` (all pairs of net points per edge), or reuse the
   proposition's "polynomial in `|V|`, `|E|` and `(1 + D√n/(εδ))^n`".
3. **§3.3 Consequence 1.** "`κ^sq_e = sec²θ_e` exactly when `D_e` is a ball" can be read as
   "if and only if". Equality also holds for non-balls. Example: the chord between the two
   tangent points of a ball (`d = 1`, `ρ = 1/2`) gives `κ^sq = sec²θ_e = 4/3`. Suggested
   wording: "for balls, `κ^sq_e = sec²θ_e`".
4. **Code: `gcs/code/gcslib.kappa_sq`.** When `0` is a vertex of `D_e`, the function drops
   the zero row and returns a finite value, but the true value is `κ^sq_e = ∞` whenever
   `0 ∈ D_e`. For example, triangles `{(0,0),(1,0),(0,1)}` and `{(1,0),(2,0),(1,1)}` return
   7.04. The inline comment ("finite only if cone pointed") describes the Euclidean case.
   Only t10 reaches this branch, and it filters out `0 ∈ D`, so no reported number is
   affected. Fix: return `inf` when any difference is zero.
5. **Prop. 11 grid.** The stated point count assumes a cell-centred grid. A grid anchored at
   the box corner with `⌊D/s⌋ + 1` points can leave points at distance `s` rather than `s/2`
   in one coordinate. One phrase fixes this.
6. **Outside the revision, Prop. 5.2.** "`REL_H^{no deg} = 0.5`" is an infimum, not a
   minimum. Without degree constraints, an unbounded circulation on `1 → 2 → 1` drives the
   cycle cost to 0. The solvers return 0.5002–0.504 and flag the solution as inaccurate.
7. **Cosmetic, `t3b_sq.out`.** The squared-length rows print the Euclidean "explicit point"
   and "4·ell" values. The note does not use them.

## Computations (targeted local checks only)

- Python 3.13, cvxpy 1.9.3 (Clarabel; SCS for comparison), SciPy, mpmath, SymPy.
  `OMP_NUM_THREADS=1`, one process.
- The final full rerun of all scripts took 2 min 40 s of CPU.
- No project-wide checks were run, and no CI status or logs were inspected.

All commands were run from `research-20260928b/reviews/gcs-recheck/`:

```
python3 -W ignore k1_kappa_sq.py 200 100 60 0 > k1_kappa_sq.log      # Corollary C
python3 -W ignore k2_hardness.py all > k2_hardness.log               # Prop. 12
python3 -W ignore k3_door.py > k3_door.log                           # Prop. 10
python3 -W ignore k4_tangent.py > k4_tangent.log                     # Prop. B' (exact, cvxpy, squared)
python3 -W ignore k4b_series.py > k4b_series.log                     # Prop. B' series: 1/2 + t^4/64
python3 -W ignore k5_ptas.py > k5_ptas.log                           # Prop. 11
python3 -W ignore k6_cone.py 0 60 > k6_cone.log                      # rotated cone vs quad_over_lin
python3 -W ignore k7_theorem1.py 0 50 1.0 opt     >  k7_theorem1.log # Theorem 1 (appended runs:)
python3 -W ignore k7_theorem1.py 1 50 2.5 opt     >> k7_theorem1.log
python3 -W ignore k7_theorem1.py 2 40 1.0 random  >> k7_theorem1.log
python3 -W ignore k7_theorem1.py 3 40 2.5 random  >> k7_theorem1.log
python3 -W ignore k7_theorem1.py 4 60 1.5 sym     >> k7_theorem1.log
python3 -W ignore k7_theorem1.py 5 60 3.0 sym     >> k7_theorem1.log
```

I also ran two inline, read-only checks with no output files:

- polishing the ball centre on the single ill-conditioned set in item 1;
- calling `gcslib.kappa_sq` on the zero-vertex example of problem 4. This import created a
  `__pycache__` in `gcs/code/`, which I removed.

**Harness note.** An early version of my set projection minimized a *squared* distance. A
1e−8 objective tolerance then moved points by about 1e−4 and produced spurious 1e−4
"violations" of `Σ y cav ≤ REL_H + Σ yΔ`. The final harness minimizes the unsquared distance
and keeps points that are already inside the set. All logs above come from the final
version.

## Not checked

- The Bézier and corridor instances of t8 and Theorem 7 (not part of the revision).
- Open Questions 1–4 and scout Q2.
- The literature and novelty statements of §9.
- The random instances behind the author's t1, t2, t3 and t6 numbers. They cannot be
  regenerated independently; my own random families replace them.
