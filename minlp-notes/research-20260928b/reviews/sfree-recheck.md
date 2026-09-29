# Recheck: optimal intersection cuts from maximal quadratic-free sets (revision of 2026-09-29)

Target: `research-20260928b/sfree/optimal-intersection-cuts.md`, as revised after
[`sfree-review.md`](sfree-review.md) (its §12 lists the changes). Scope, as requested:

1. the new Proposition 16, which replaces the refuted Conjecture 16;
2. the revised §6.1: the point rule for `λ` compared with the full orbit, and the Muñoz–Serrano (MS)
   enlargement subtlety;
3. the `h ≠ 0` step of Theorem 8(3), now written out in full.

I am a fresh reviewer. I re-derived the definitions from the note and the sources in
`scouting/s-free-intersection-cuts/sources/`, and I wrote my own scripts in
[`sfree-recheck/`](sfree-recheck/). The only thing I took from the author's code is the instance
generator `case2_instance` of `sfree/code/point_rule_check.py`, so that §6.1 is rechecked on the same 40
corners. I did not edit the note and did not commit.

## Verdict summary

| Item | Verdict | Main point |
|---|---|---|
| Prop. 16(1): `z_K = 1`, unique support-one minimizer `t* = v_1`, transversal edges, multipliers `1/8`, `1/4` | **correct** | Re-proved exactly by a different argument (radial reduction to the far face instead of face enumeration). |
| Prop. 16(2): exact dual certificate, so no nonzero `F` works and `z_A < z_K` | **correct** | New certificate built independently. A small integer version is given below. The compactness step is sound. Extra: exact bracket `0.9838 ≤ z_A ≤ 0.9839`. |
| Prop. 16, numbers (`z_A = 0.98385`) and "(B) only numerically" | **consistent** | `z_A = 0.98385` reproduced. My dual check also excludes (B) numerically for every lowering. A simple exact (B) certificate does not exist. |
| §6.1: span property, one-parameter family | **correct** | The θ-formula family and an independent scan over `SO⁺(2,1)` agree to `6·10⁻⁸`. |
| §6.1: "13 of 40 miss `z_K`", "full orbit reaches it in all 40" | **numbers right, count wrong** | 4 of the 40 generated corners have `z_K = ∞` and are skipped by the note's own script. It should read **13 of 36** and **all 36**. The 13 ratios reproduce exactly. |
| §6.1: MS §5.2 enlarges members whose tangency point is on the wrong side of `H`; MPS 2026 Thm 5 allows no dropped inequality | **correct reading of the sources** | Checked against the MS text (§5.2, eq. (12), Lemma 2, Theorems 9–10, Example 8) and MPS 2026 Theorem 5. |
| §6.1: "whether MS's full construction with the point rule attains `z_K` is not settled" | **can now be settled for these instances (numerically)** | I implemented the full MS §5.2 construction (`φ_λ` and `r(β)`) under every transformation. It still misses `z_K` on **all 13** corners. It improves only two of them, 0.674 → 0.689 and 0.217 → 0.249. |
| Theorem 8(3), `h ≠ 0` step | **correct** | Affine bijection and lineality argument verified, and the attribution to MS checked. Minor: the lineality lemma needs "full-dimensional". |

No mathematical error was found in the three items. The problems are:
- a wrong count in §6.1;
- an open question that my computation answers on the note's own instances;
- two small wording points;
- a stale docstring.

## 1. Proposition 16

### Definitions re-derived from the note

- **Set and matrix.** `S = {w ≤ xy}`, `q = w − xy`, and `M(x, y, w) = [[w, x], [y, 1]]`, so `det M = q` on the
  slice `h = 1`.
- **Corner bound.** `z_K = min{Σλ_j : λ ≥ 0, q(s̄ + Pλ) ≤ 0}`, with `p_j = v_j − s̄` and `w = 1`.
- **Family (A), the orbit family.** The sets are `C_F ∩ H` with `C_F = {M : sym(F^T M) ⪰ 0}` and `det F > 0`.
  - The one-cut bound is `z_{C_F} = min_j w_j α_j`.
  - `z_{C_F} ≥ z` holds iff `sym(F^T M(v)) ⪰ 0` at the vertices `v` of `T_z = conv{s̄, s̄ + z p_j}`, with strict
    inequality at `s̄`.
  - `z_A = sup_F z_{C_F}`.

### Part (1), re-proved by a different method (`prop16_exact.py`)

- `det P = 67/2`, `q(s̄) = 8`, `q(t*) = 0`.
- **Radial reduction.** `t* = 0`, so every point of `T* \ {t*}` is `r f` with `f` in the far face
  `F* = conv{s̄, v_2, v_3}` and `r ∈ (0, 1]`. Then `q(r f) = r (f_w − r f_x f_y)`.
  - `f_w ≥ 1/4 > 0` on `F*`, because its vertex values are 2, 1/4 and 1/2.
  - So `q > 0` on `T* \ {t*}` iff `q > 0` on `F*`.
- **Exact minimum over `F*`.** Candidates: vertices 8, 49/4, 3; edge stationary points 31/2560 and 263/264;
  the interior stationary point is a saddle, since the Hessian `[[80, 59], [59, 33]]` is indefinite.
  - So `min_{F*} q = 31/2560 > 0`.
  - Hence `T* ∩ S = {t*}`, `z_K = 1`, and the minimizer `λ = e_1` is unique (`P` is invertible).
- **Transversality.** `∇q(t*) = (0, 0, 1)` and `∇q(t*)^T (v − t*) = 2, 1/4, 1/2`. All three edges at `t*` are
  transversal.
- **KKT.** `w + σ P^T ∇q(t*) − ν = 0` with `P^T ∇q(t*) = (−2, −7/4, −3/2)` gives `σ = 1/2` and `ν = (0, 1/8, 1/4)`.
  The Theorem 1(4) condition `∇q(t*)^T (s̄ − t*) = 2 > 0` also holds.

### Part (2), with an independent certificate

- I built the certificate from an exact rational basis of the kernel of `(Y_v) ↦ Σ_v M(v) Y_v`, which has
  dimension 8. The note's script instead solves for pivot unknowns.
- I took an SDP centre, rounded it in that basis, and checked positive definiteness exactly.
- The SDP margin is `1.7109·10⁻³`, the same as the note's `1.7·10⁻³`.
- A hand-checkable integer certificate (`prop16_small_cert.py`):

  | `v` | `M(v)` | `Y_v` | `Y_11`, `det Y_v` |
  |---|---|---|---|
  | `s̄` | `[[2, −2], [3, 1]]` | `[[92, −75], [−75, 64]]` | 92, 263 |
  | `v_1 = t*` | `[[0, 0], [0, 1]]` | `[[726, 89], [89, 12]]` | 726, 791 |
  | `v_2` | `[[1/4, 6], [−2, 1]]` | `[[96, −64], [−64, 45]]` | 96, 224 |
  | `v_3` | `[[1/2, 1], [−5/2, 1]]` | `[[20, 16], [16, 16]]` | 20, 64 |

  The products `M(v) Y_v` are `[[334, −278], [201, −161]]`, `[[0, 0], [89, 12]]`, `[[−360, 254], [−256, 173]]`
  and `[[26, 24], [−34, −24]]`. They sum to zero; I checked this by hand and by script.
- The identity `Σ_v ⟨sym(F^T M(v)), Y_v⟩ = tr(F^T Σ_v M(v) Y_v)` was checked symbolically.
- The system `sym(F^T M(v)) = 0` for all four `v` has rank 4. This is also clear from the structure: the four
  `M(v)` span all 2×2 matrices because the vertices are affinely independent.
- So no nonzero `F`, including a rank-one `F`, has `C_F ⊇ T*`.
- **Compactness.** Normalize `‖F_n‖ = 1` and let the vertices of `T_{z_n}` tend to those of `T*`. A limit
  `F ≠ 0` would satisfy the closed conditions, so `z_A < 1`. Because the certificate excludes rank-one `F`
  too, the separate rank-one case of Theorem 14(3) is not needed. The note says this correctly.

### Numbers

- **Exact bracket for `z_A` (extra).**
  - Lower bound: rational `F` with `det F > 0`, PD at `s̄` and PSD at the vertices of `T_z` for
    `z = 49/50`, `983/1000` and `4919/5000`.
  - Upper bound: exact PD certificates at `T_z` for `z = 99/100`, `197/200` and `9839/10000`.
  - Hence `0.9838 ≤ z_A ≤ 0.9839`, consistent with the note's `0.98385`.
- **Family (B).** This is numerical only, as the note says.
  - For fixed lowerings `τ_v ∈ [0, q(v)]`, a PD certificate `Σ_v (M(v) − τ_v E) Y_v = 0` excludes every
    nonzero `F`.
  - The best certificate margin over the `τ`-box (9³ grid and Nelder–Mead) is `1.71·10⁻³`, attained at `τ = 0`.
    Lowering only increases it. So (B) also misses `T*` numerically.
  - I also looked for an exact certificate affine in `τ`: `Y_v(τ)` PD at the 8 box corners with the identity
    holding in `τ`. It does not exist (SDP margin 0). An exact (B) proof would need another argument.
  - Caution for anyone rerunning (B) checks: the primal test `max_{‖F‖ ≤ 1} min_v λ_min` is vacuous here.
    `F = 0` gives value 0, and the rank-one vertex `t*` caps the value at 0. My first attempt made this mistake.
- **Not rechecked:** "SCIP's own set gives only 0.318" (it depends on the scout's Case 4 implementation).

### An observation on the "Why" paragraph and the open question

The far face has a second near-contact with `∂S`. On the edge `[s̄, v_2]`, `q` falls to `31/2560 ≈ 0.012` (at
`s̄ + (143/320)(v_2 − s̄)`), against `q(s̄) = 8`.

In a small exploratory family (`prop16_variants.py`, numerical: Clarabel bisection plus the certificate margin
at `z = 1`), the gap does not follow the angle at `t*` alone:

| `v_2` | edge cosine at `t*` | min `q` on far face | `z_A` |
|---|---|---|---|
| `(6, −2, 1/4)` (Prop. 16) | 0.0395 | 0.012 | 0.98385 |
| `(6, −2, 1)` | 0.156 | 0.34 | 0.99923 |
| `(6, −2, 2)` | 0.30 | 0.78 | 1 |
| `(6, −4, 1/4)` | 0.035 | 0.95 | 1 |
| `(8, −3, 1/4)` | 0.029 | 0.025 | 0.98765 |

This does not contradict the note's open question, which asks for some angle threshold `δ`. But it shows that
in this family any such `δ` must exceed a cosine of about 0.16. It also shows that nearly tangent edges at `t*`
are not the only factor. The "Why" paragraph could say that the far face also nearly touches `∂S`.

## 2. Section 6.1: point rule versus full orbit

### The derivation

- **Span property.** With `λ = x̂/‖x̂‖`, `Ts̄ = ((a + b)λ, a − b) = a(λ, 1) + b(λ, −1)`. Here `a, b > 0` iff
  `‖x̂‖ > |ŷ|`, i.e. `s̄ ∉ S`.
- **Invariance.** The property is invariant under automorphisms. The identities `γ_1^T x̂ − ŷ = b(1 + γ_1^T γ_2)`
  and `γ_2^T x̂ + ŷ = a(1 + γ_1^T γ_2)` hold.
- **The θ-formula.** It follows from `‖x̂ − aγ_1‖ = b = a − ŷ`.
- **Converse.** It follows by 2-transitivity: map the ordered pair `(λ, −λ)` of celestial points to
  `(γ_1, −γ_2)` with an orthochronous map. It sends `(λ, ±1)` to positive multiples of `(γ_1, 1)` and
  `(γ_2, −1)`, so the rule then picks `λ`.
- **A slice picture** the author may want to add. When both tangency points lie on the slice side (always the
  case for maximal sets in Case 2, by MPS 2026 Thm 5), the rule at `s̄` produces exactly the maximal sets whose
  two tangency points lie on a chord through `s̄`. The reason is that `u_s = a t_1 P_1 + b t_2 P_2` is a
  convex combination of the tangency points `P_i` in `H`.

### The numbers (`point_rule_recheck.py`, own code)

- **Setup.** Own `z_K` (exact one-ray roots, two-ray direction scan with refinement), own Sylvester form, own
  full-orbit scan over `(γ_1, γ_2) ∈ S¹ × S¹` with refinement.
- **Two independent parametrizations** of the point-rule family:
  - the note's θ-formula, 2·10⁵ points with refinement;
  - a scan over transformations `L = B(η) R(φ) ∈ SO⁺(2,1)` (601 × 721 grid, `|η| ≤ 7`, refinement), applying the
    rule in the `L`-coordinates.
  - They agree to `6·10⁻⁸` on every corner. This numerically confirms the one-parameter claim.
- **Count.** Of the 40 generated corners, **4 have `z_K = ∞`** (instances 3, 13, 18, 37: no ray combination meets
  `S`). The note's `point_rule_check.py` skips them silently, and its log has 36 lines. My `z_K` values equal the
  note's on all 36 corners to the printed 6 decimals.
- **Full orbit** attains `z_K` in 36 of 36. The note's cross-check ran the SOCP only on the 13 misses. For the
  other 23 corners the claim follows by inclusion.
- **Plain point-rule sets** miss `z_K` in 13 of 36, with exactly the note's ratios 0.119, 0.217, 0.242, 0.302,
  0.484, 0.526, 0.546, 0.629, 0.674, 0.707, 0.966, 0.967, 0.967.
- **SCIP's set.** "SCIP's own set, which is one member" is right for Case 2. In Chmiela's coordinates `d = 0` and
  `λ^T a < 0` (ZIB 20-29, Case 2), so MS's construction returns `C_λ ∩ H` unchanged.

### The MS enlargement, checked against the text and then modelled

**The text** (`1911.plain.txt`, §5.2; `2605.30602.plain.txt`, Theorem 5) says the following.
- In Case 2 (`‖d‖ < ‖a‖ = 1`), MS replace the inequality `−λ^T x + β^T y ≤ 0` of `C_λ` whenever
  `λ^T a + d^T β > 0`, i.e. when its exposing point `(λ, β)` does not scale onto `H`.
- The replacement is `−λ^T x + ∇φ_λ(β)^T y ≤ r(β)`, with `φ_λ` from eq. (12) and `r(β)` from Lemma 2
  (Theorems 9–10: S-free and maximal).
- Inequalities with `λ^T a + d^T β ≤ 0` are kept (`r = 0`, `φ_λ = ‖·‖` there).
- MPS 2026 Theorem 5 says that in this case `C_Γ^G ∩ H` is maximal only if `G = D^m`, so no completion by
  dropping inequalities exists.

The note's description is therefore accurate: "their `φ_λ` and tilting", members with both tangency points on
the slice side returned unchanged, and the reviewer's "no completion" remark applying to dropping only. So is
MS §6/Example 9: one transformation gives a set with an asymptote, the other does not.

**Modelled** (`point_rule_recheck.py`, `ms_asymptote_bound.py`, `ms_fiber_check.py`). For `m = 1` I implemented
the MS construction literally, under every transformation `L`:
- `φ(β) = √((1 − d²)(1 − (λ^T a)²)) − dβ λ^T a`;
- `∇φ(β) = β φ(β)`;
- `r(β) = (dβ + λ^T a φ)/(φ + dβ λ^T a)`;
- homogenized on `H` as `(−λ + r a)^T x + (βφ + r d) y ≤ 0`.

Checks of the implementation:
- **MS Example 8 reproduced.** `β = −1` is kept; for `β = +1`, `φ = 1/√2` and `r = 1`.
- **On 300 random `L` per corner:**
  - every modified normal is null (relative error below 10⁻¹⁵);
  - its tangency line lies in `H_0 = {t = 0}` (relative error below 10⁻¹⁵);
  - the MS set contains the plain member;
  - sampled points of `S` never lie in its interior;
  - `s̄` is interior.
- **Why the tangency line lies in `H_0`.** MS show `(x_β, β) ∈ H_0` with `λ^T x_β = φ(β)` and `‖x_β‖ = 1`, so the
  modified inequality vanishes on the null vector `(x_β, β)`. The set is maximal (MS Thm 10), so its homogenized
  normals are null (MPS 2026 Lemma 1), and a null halfspace meets the cone only along its tangency line. So each
  set MS can return is either a plain member, or its kept halfspace intersected with the tangent halfspace along
  one of the **two** null lines of `H_0`.
- **Fibre check.** Along the boosts that fix a member (123 fibres), MS's modified halfspace does not change. So
  "one set per θ, also after the enlargement" holds for MS's construction as well.

Results. The `L`-scan and an `L`-independent upper bound (best of the two asymptote choices for every θ,
10⁵ points with refinement) agree:

| Corner | 1 | 5 | 6 | 9 | 15 | 19 | 21 | 22 | 23 | 24 | 27 | 31 | 39 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| plain point rule / `z_K` | .9657 | .3015 | .6287 | .6736 | .4840 | .9669 | .9669 | .1186 | .2424 | .5264 | .7069 | .2167 | .5462 |
| MS full construction / `z_K` | .9657 | .3015 | .6287 | **.6891** | .4840 | .9669 | .9669 | .1186 | .2424 | .5264 | .7069 | **.2487** | .5462 |

So on all 13 corners, MS's full construction with the point rule misses `z_K` under every transformation. The
largest ratio is 0.9669. The note's "generous relaxation" reached `z_K` because it allowed any null halfspace,
whereas MS only ever use one of the two asymptotes. This is numerical: it rests on a dense one-parameter scan
and on the tangency fact above, not on exact arithmetic.

### A related minor point on the §6 gloss about MS's conjecture

MS's "our method" uses the point rule. For `n + m = 3` their conjecture holds with the point rule too, provided
`s̄` may vary. Every maximal set `K` is produced from any `s̄` on the open chord between its two tangency
points. It fails at a fixed `s̄` (§6.1). The gloss "Theorem 8 proves this, in the stronger form that one fixed
set and its orbit suffice" is about `λ` free. One sentence would connect it to MS's actual method.

## 3. Theorem 8(3), the `h ≠ 0` step

- **Setting.** MPS 2026 §2.1 gives `Q′_g = {‖x‖ ≤ ‖y‖, a^T x + d^T y + h^T z = −1}`, as the note states. MS §4,
  after Remark 5, states only that `C × R^ℓ` is maximal for maximal `C`. The attribution in the note is accurate.
  MPS cite it as "[25, Remark 3.2]" with the converse wording.
- **The map.** `(x, y, z) ↦ (x, y, z − (h^T z/‖h‖²) h)` restricted to `H′` is an affine bijection onto
  `R^{n+m} × h^⊥`.
  - The inverse restores `z = z′ + c h` with `c = (−1 − a^T x − d^T y)/‖h‖²`.
  - The image of `Q′_g` is all of `Q_h × h^⊥`, with no constraint left on `(x, y)`.
  - `L ⊕ id` is an automorphism of the degenerate form.
- **Lineality lemma.** It is correct for **full-dimensional** `C`: for convex `C` with `int C ≠ ∅`,
  `int(C + V) = int C + V` and `int cl(C + V) = int(C + V)`.
  - As stated ("every maximal S′-free set"), it is false for lower-dimensional sets. Counterexample:
    `S′ = V = R × {0}` in `R²`, `C = {0} × R`. `C` is maximal S′-free (any convex enlargement contains a strip
    whose interior meets the x-axis), yet `C + V = R²`.
  - The application concerns full-dimensional sets only, so the proof stands. Add "full-dimensional" to the lemma.
- **The rest.**
  - A full-dimensional maximal set in the product is `C × h^⊥` with `C` full-dimensional and maximal `Q_h`-free.
  - Pulling back gives the slices `(C × R^ℓ) ∩ H′`.
  - (1)–(2) then give `C = L(C_λ)`.
  - The `h = 0` case and MPS Lemma 1 (full-dimensional `C_Γ`) are used correctly.

## Requested changes (the note was not edited)

1. **Count in §6.1, the Summary (item 5) and §12 (row 2).** Replace "13 of 40" and "all 40" with "13 of the 36
   corners with finite `z_K`", and say that 4 of the 40 generated corners have `z_K = ∞`. Note that "`z_K`
   confirmed by SCIP" refers to the 13 misses.
2. **§6.1 and Summary item 5.** The question "whether MS's enlargement repairs this" can be answered for these
   instances. With the MS §5.2 construction modelled exactly (`φ_λ`, `r(β)`, all transformations), it still
   misses `z_K` on all 13 (ratios as above, max 0.967; numerical). Optionally add the tangency-chord description
   of the point-rule family.
3. **Theorem 8(3), lineality lemma.** Say "every full-dimensional maximal S′-free set".
4. **Proposition 16.** Optionally state the integer certificate above, which can be checked by hand. Mention the
   far-face near-contact (`min q = 31/2560` on `[s̄, v_2]`) in the "Why" paragraph.
5. **Stale code text** (minor):
   - the docstring of `code/point_rule_check.py` still says the point-rule sets "are exactly the
     Muñoz–Serrano/SCIP sets under all transformations", which §6.1 now corrects;
   - its log labels the generous relaxation "MS-construction upper bound".

## What was not checked

- "SCIP's own set gives only 0.318" (Prop. 16 numerics) and the best (B) value 0.98385.
- An exact proof that family (B) misses `T*`. Only the numerical dual check above; the affine-in-`τ` certificate
  does not exist.
- The rest of the note, which the earlier review covered, and the `n ≥ 2` Möbius argument of Theorem 8(1).
- §6.1 beyond the note's 40 generated corners. The MS result is numerical, not exact.

## Commands run (targeted checks only)

All from `research-20260928b/reviews/sfree-recheck/` with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`. No
project-wide checks were run and CI was not consulted. The first test run of `point_rule_recheck.py` wrote a
`__pycache__` into `sfree/code/`. I deleted it, and the scripts now disable bytecode writing.

| Command | Result (log) |
|---|---|
| `python3 prop16_exact.py` | ALL PASS: (1) exact, certificate, rank 4, bracket `[0.9838, 0.9839]` (`prop16_exact.log`) |
| `python3 prop16_small_cert.py` | integer certificate, exact (`prop16_small_cert.log`) |
| `python3 prop16_familyB.py` | min certificate margin over the `τ`-box `1.71e-3 > 0` (`prop16_familyB.log`) |
| `python3 prop16_familyB_exact.py` | no affine-in-`τ` exact certificate (margin ≈ 0) (`prop16_familyB_exact.log`) |
| `python3 prop16_variants.py` | exploratory variants, `z_A = 0.98385` reproduced (`prop16_variants.log`) |
| `python3 point_rule_recheck.py 40` | 36 finite, orbit 36/36, plain misses 13 (note's ratios), θ vs `L` scan `6e-8`, MS full construction misses 13; about 2 min (`point_rule_recheck.log`) |
| `python3 ms_asymptote_bound.py` | `L`-independent upper bound for MS: 0 of 13 reach `z_K`, max 0.966934 (`ms_asymptote_bound.log`) |
| `python3 ms_fiber_check.py` | MS output constant along member-fixing boosts, 123 fibres (`ms_fiber_check.log`) |
