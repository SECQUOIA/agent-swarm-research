# Referee report: "Exponential lower bounds for single-tree spatial branch-and-bound with face-exact relaxations on a path"

Date: 2026-09-29. Note under review:
`research-20260929/theory-face-exact/face-exact-exponential.md` (cited below as
"the note", with line numbers of the version dated 2026-09-29 22:26). The
referee did not write the note. Referee scripts and logs are in
`research-20260929/reviews/face-exact-review-checks/`. Only targeted checks were
run; no project-wide verification and no CI (AGENTS.md).

## Verdict in brief

- **The mathematics is correct.** Lemma 2.1, Lemma 3.1 and Theorem 1 (both
  parts) are proved correctly. I could not break them, either on paper or by
  an adversarial search for large valid boxes. Lemma 4.1, Theorem 2,
  Propositions 5.1, 5.2, 5.3, 5.5 and 6.1 are also correct. A few need small
  wording fixes (listed below).
- **Two computational interpretations are wrong and must be revised.**
  1. `bb_path.py` sometimes returns node bounds above the exact QP optimum,
     by up to 1.5e-4. This happens on the instance `kappa = 0`, `c = 0`. At
     `eps <= 1e-5` the toy B&B then prunes boxes that are not valid, so it
     undercounts by 5–25% (at `n = 8`, `eps = 1e-6`: 29,282 instead of
     37,500). The claim in Section 7.5 that "the slope falls at
     small `eps`" when `x*` is on the dyadic grid is an artifact of this
     error. The grid-DP optimum at `n = 2`, `eps = 1e-6` is 12, not 10. The
     bisection count there is 38, not 32.
  2. SCIP's default settings are outside hypothesis (M_b). With SCIP's
     *minor* separator (PSD cuts on 2x2 principal minors) turned off:
     - the `kappa = 0` root solve disappears: 21 nodes at `n = 4` and
       14,011 at `n = 8`, against 1 and 21;
     - on the PROGRAM family, node counts rise by factors of 2.4–8 at
       `n = 4..8`;
     - SCIP's growth rate rises from about 2.1–2.3 to about 2.9–3.5 per
       variable.

     Section 8's statement that SCIP's relaxation "should satisfy (M_b)" is
     therefore false for default SCIP. So is the statement that the SCIP
     `kappa = 0` data "fit Theorem 1".
- **Significance.** The bound is a statement about the *relaxation class*,
  not about single-tree search as such.
  - Theorem 1 holds for a convex QP (`kappa = 0`). SDP-type cuts avoid it, and
    SCIP adds such cuts by default.
  - Theorem 2 depends on the factorization. If each `g_i` is split evenly
    between the two neighbouring factors, every factor is convex on
    `|x|_inf <= 0.577`. For `kappa = 0` every factor is convex everywhere.
    The Theorem 2 mechanism near `x*` then disappears.
  - The title, the Summary and Section 8 should say this.
  - The ingredients are known: a center-of-box witness (face-exact note,
    Proposition 3.10) and the cluster-problem prediction of
    exponential-in-`n` clusters. Their combination into a rigorous lower bound
    for every certificate, with the edge gaps summed and `m` evaluated at the
    witness, appears new relative to the repository and to the program's
    literature audit.

## 1. Theorem 1 (termwise McCormick)

### 1.1 Lemma 2.1 (center of `C ∩ R`): correct

I checked every step (note lines 224–233).

- `C ∩ R = prod [z_i - h_i, z_i + h_i]` is contained in `C`. So
  `d_i^C(z) >= h_i` whether or not `C` extends beyond `R` and whether or not
  `x* in C`. Every face of `C ∩ R` is a face of `C` or lies inside `C`.
- `[z_i - h_i, z_i + h_i] ⊆ [x*_i - r, x*_i + r]` gives
  `|z_i - x*_i| <= r - h_i`.
- The certifying box `A ⊇ C` has `d^A(z) >= d^C(z)`. Only monotonicity of `L`
  is needed, not monotonicity of the relaxation.
- The volume identity is `vol(C ∩ R)/vol(R) = prod(1 - s_i)`. The covering
  step `1 <= sum vol(C ∩ R)/vol(R)` does not need disjoint interiors.
- **Mixed signs.** The McCormick gap of `b_i x_i x_{i+1}` is
  `|b_i| min(...)` for either sign (face-exact Lemma 2.1(a)), so it is at
  least `|b_i| d_i d_{i+1}`. The model `U` uses `|y|`, so the sign pattern
  enters nowhere else. `U` is nondecreasing because `D > 0`, which is forced
  by `D I + B ⪰ 0`.

### 1.2 Lemma 3.1 and the width optimization: correct

- I rederived `k'(s0) = 0`, `rho s0^2 + 2 s0 = 1`, the equivalence
  `k''(s0) <= 0` iff `S <= 2`, and the convex/concave split at `s1`.
- I rederived `F'(S) = (S^2 - 3S - 2)/(2 S^3 (S+1))`, which is negative on
  `[1, 3.56)`. `F` is also negative for large `S` (`F ~ -1/(2S)`), so
  `F >= 0` exactly on `[1, S_max]`.
- Numerically (`constants.py`):
  - `S_max = 1.729321` and `rho_max = 1.990553`;
  - `max_s k(s) - k(s0) <= 2.8e-16` over 800 values of `rho`, on a grid that
    includes points up to `1 - 1e-12`.
- Steps 2–5 of the proof of Theorem 1 are correct:
  - `(1-s_i)(1-s_{i+1}) - s_i s_{i+1} = 1 - s_i - s_{i+1}`;
  - the degree-2 step loses only at the two ends;
  - the Lagrangian step in (b) and `Psi <= -mu` for `mu (rho+2) <= 1` are
    right.
- **The constant is nearly the best this lemma allows.** I maximized
  `prod(1 - s_i)` over admissible `s` directly (SLSQP, before applying
  Lemma 3.1). This gives `1/nu` = 37.9, 290.6, 2236.7 and 132,884 at
  `n` = 8, 12, 16, 24, against 34.2, 263.6, 2033.6 and 121,078 from the
  closed form. So Lemma 3.1 loses only about 10%.

Values I reproduced: `theta = 3/5` and `lambda = 5/9`; bounds 4.427, 94.88,
2033.6 and 15,692 at `n` = 4, 10, 16, 20; Lagrangian 4.503, 95.58 and 15,747;
the factor 0.5736 for `r >= 1/2`; the factor 0.3292 for `r = sqrt(eps/b)`.

**Minor fix (line 330).** The Lagrangian form improves the closed form by
3.1% at `n = 2` and 1.7% at `n = 4`. "Less than 1%" holds only for `n >= 8`.

### 1.3 Coverage: any rule, split points, order, incumbent, tightening

The coverage claim is correct. The mechanism is Lemma 1.2 of the note, which
restates Lemma 2.1 of the constrained note.

- **Bound tightening does not break the center argument.** A round that
  shrinks `B_k` to `B_{k+1}` contributes at most `2n` frame pieces. Each piece
  `S ⊆ B_k` is certified by `B_k`, because `f_{B_k} > UBD - eps` on `S`.
  Lemma 2.1 applies to `S` like any other member. The frames must be taken
  per round, and the note does this.
- **The price is counting.** The bound is on *leaves + 2n × (tightening
  rounds)*, not on leaves alone. With OBBT at every node, the node lower bound
  is Theorem 1 divided by `2n + 1`. It is still exponential.
  - *Fix (Summary lines 19–21 and 24–25).* The Summary says every certificate
    "has at least ... leaves". It should say "leaves plus `2n` per tightening
    round", as Lemma 1.2 does.
- **Inherited cuts (lines 161–163).** The note says (M_b) holds for any
  relaxation "that lies pointwise below such a relaxation, for example cuts
  inherited from ancestors". Adding cuts raises a relaxation; it does not lower
  it. The conclusion is still right, for a different reason.
  - Ancestor McCormick cuts are dominated by the node's own envelope, because
    `vex_A <= vex_C` on `C ⊆ A`.
  - Inherited univariate cuts are valid convex underestimators of `g_i`, which
    (M_b) already allows.
  - *Fix.* Say "termwise cuts inherited from ancestors are dominated by, or
    allowed in, the termwise relaxation". Aggregated inherited cuts (cuts on
    `sum t_i`) are not covered.
- **Exclusions.** The Section 1.3 list of exclusions is appropriate. One
  precision: level-1 RLT for these terms *is* McCormick plus secants/tangents
  of `x_i^2`, so it satisfies (M_b). SDP or PSD-minor cuts are what escape
  the bound (Section 5 below). Listing "RLT" among the escapes is harmless
  but imprecise.

### 1.4 "No nonconvexity or uniqueness needed", and the role of `r`: correct

- The proof uses only (Q_D) at an interior global minimizer. For `kappa = 0`
  the objective is a strictly convex QP, and the bound holds there.
- `r` enters only through `eps'' = eps/(b r^2)`. The bound therefore holds for
  every cube `R ⊆ X0` around `x*` with `eps <~ b r^2 n`.
- The "Other graphs" sketch (line 350) is right, with `rho = D/(Delta b)` and
  with `eps''` replaced by `2 eps''/Delta` and no `-1` offset.

A useful fact the note could add: `x*` is a minimizer with `g'' <= D`, so
`D I + B ⪰ 0`. On a path this forces `rho >= cos(pi/(n+1))`, so the proved
base is at most `1 + 1/sqrt(2) = 1.707`. The value 5/3 for the PROGRAM family
is close to that ceiling.

### 1.5 Adversarial numerical test

Theorem 1 is equivalent to a per-box statement: every valid box `C` has
`vol(C ∩ R)/vol(R) <= nu`. I tested exactly that, with an independent
implementation.

**Setup** (`adversarial_boxes.py`, `adversarial_large.py`):
- relaxation: `x^2` exact, secant of `-kappa x^4`, McCormick for each
  `b_i x_i x_{i+1}` with arbitrary signs, solved by Clarabel directly;
- validity: `LB(C) >= f* - eps`;
- search: greedy maximal face extension by bisection, then face-exchange
  moves, from 40 starts per case. The starts include all `2^n` orthant boxes
  with vertex `x*` (boxes aligned to `x*`), tiny cubes at `x*`, alternating
  slabs, and random points.

By monotonicity of this relaxation, a valid `C` implies a valid `C ∩ R`. So
boxes reaching outside `R` cannot do better, and searching inside `R` covers
them.

**Cases:**
- A: `kappa = 0`, `c = 0`, `b = +0.8`, `r = 1`;
- B: as A, but with alternating signs of `b_i`;
- C: as A, but with small `R` (`r = 0.1` inside `X0 = [-1,1]^n`);
- D: `kappa = 0.1`, seed 0, so `x* != 0`, secant relaxation, `r = 0.5`;
- E: as A, but with `eps = 0.05`.

All cases use `eps = 1e-4` except E.

| n | best valid box, `fraction^(1/n)` (A / B / C / D / E) | exact `nu^(1/n)` (A) | Theorem 1 `^(1/n)` (A) | `1/best` (A) vs Theorem 1 |
|---|---|---|---|---|
| 2 | 0.629 / 0.629 / 0.634 / 0.613 / 0.655 | 0.652 | 0.792 | 2.53 vs 1.59 |
| 3 | 0.655 / 0.655 / 0.658 / 0.632 / 0.670 | 0.672 | 0.722 | 3.56 vs 2.66 |
| 4 | 0.648 / 0.648 / 0.651 / 0.633 / 0.659 | 0.666 | 0.689 | 5.66 vs 4.43 |
| 5 | 0.613 / 0.603 / 0.607 / 0.589 / 0.620 | 0.655 | 0.671 | 11.6 vs 7.4 |
| 6 (A only) | 0.610 | 0.646 | 0.658 | 19.5 vs 12.3 |
| 8 (A only) | 0.582 | 0.635 | 0.643 | 75.5 vs 34.2 |

- **No violations.** In every case the best valid box lies below the exact
  `nu` and below the closed form.
- The center inequality of Lemma 2.1 holds at every box found. The largest
  slack is -4.5e-4, in case C.
- Mixed signs (B) give essentially the same values as uniform signs (A), as
  the gauge symmetry of a path predicts. The small difference at `n = 5` is
  search noise.
- The McCormick bound used here agrees with a third solver (cvxpy + Clarabel)
  to 8e-12 on 600 random boxes.

**Consequence for the remark "Where the constant is lost" (lines 354–360).**
- A valid box with volume fraction `0.5824^8` exists at `n = 8`. So *any*
  lower bound that comes from the largest single-box volume is at most 75.5 at
  `n = 8`. Theorem 1 gives 34.2 and exact `nu` gives 37.9. The one-witness
  step therefore loses at most a factor of about 2.2 here, whatever witnesses
  are used, sign-aware ones included.
- The gap to the observed counts (10^4 or more at `n = 8`) lies in the
  covering step: large valid boxes cannot tile `R`.
- *Fix.* The remark should say this. It should also say that Conjecture 5.4's
  `c 2^n` cannot be reached by a per-box volume argument while valid boxes
  with volume fraction above `2^-n` exist. At `n = 8`, `0.582 > 0.5`.

## 2. Theorem 2 (per-factor convex envelopes)

**Lemma 4.1 is correct.**
- The points `p ± v` lie in `A`.
- `q'' = h'' sigma^2 d_1^2 - 2|beta| sigma d_1 d_2 <= -2 k0`.
- The chord argument gives the gap bound.
- Monotonicity and 2-homogeneity follow from the substitution `t = sigma d_1`.

**The reduction in the proof of Theorem 2 is correct.**
- The expansion and the bound
  `b(1-sigma) s_i s_{i+1} <= b(1-sigma)(s_i^2 + s_{i+1}^2)/2` need
  `sigma <= 1`, which holds.
- The degree-2 step and the Lagrange step are right.

**The base, recomputed independently** (`constants.py`):
- The supremum over `s` switches from the interior local maximum to `s = 0`
  at the optimum. The optimal `(sigma, mu)` sits on this kink:
  `sigma = 0.400`, `mu = 1.165`, with `exp(-Psi_J) = 1.2050`.
- The note's 1.2021 is the value at `n = 200`, including the
  `mu b sigma / n` term (see `bounds.py`, `best_env(D, b, 200, 0)`). So it is
  slightly conservative. "`c 1.20^n`" is correct.
- Per-`n` values: 1.45, 4.44 and 28.7 at `n` = 4, 10, 20 with fixed
  parameters, against the note's per-`n`-optimized 1.53, 4.50 and 28.65.

**Significance gap: Theorem 2 depends on the factorization.** (E_D) attaches
all of `g_i` to the factor containing `x_i x_{i+1}` (lines 164–167). This is
the PROGRAM's formulation, and the note says "for this factorization". But
the same objective can be written with balanced factors
`f_i = g_i(x_i)/2 + b x_i x_{i+1} + g_{i+1}(x_{i+1})/2`, with the end factors
taking the whole `g_1` and `g_n`.

- For `kappa = 0` each factor has Hessian `[[1, 0.8], [0.8, 1]]`, which is
  positive definite. So every factor is convex, the per-factor envelopes are
  exact, and the root is pruned.
- For `kappa = 0.1` a factor is convex wherever `g''(x_i) g''(x_{i+1}) >= 2.56`.
  This holds on `|x|_inf <= 0.577`. So the whole cube around `x*` is one valid
  box.
- In both cases the mechanism of Theorem 2 near `x*` disappears.
- *Fix.* The Summary (item 2), Section 4 and Section 10 should say that
  Theorem 2 is a property of the given factorization. PROGRAM.md calls
  per-factor envelopes "the strongest factorable relaxation"; that should also
  be qualified by the factorization.
- Theorem 1 does not have this problem, because the bilinear term is relaxed
  by McCormick under any split of `g_i`.

## 3. Propositions 5.1–5.5 and Conjecture 5.4

- **Proposition 5.1: correct.** Part (a) follows from (V) at `x*` and
  `b d_i d_{i+1} <= eps` on each edge. Part (b) follows from
  `sup Gamma = b w_i w_j/4` per edge.
- **Proposition 5.2 (orthant validity): correct.**
  - The translation identity is correct, with `grad f(x*) = 0`.
  - An unfrustrated term has McCormick underestimator 0 from the lower
    corner.
  - The frustrated envelope is `-|b| min(W_{j+1} u_j, W_j u_{j+1})`. The
    minimization over `tau` gives `-b^2 W_j^2 W_{j+1}^2 /(2D(W_j^2 + W_{j+1}^2))`,
    with `tau <= |b|/(2D) <= 1`.
  - `checks.log` agrees: `-0.08` for `W = 1` and `-0.02` for `W = 0.5`.
  - The claim `G <= (D/2)|y|^2` needs `W_j <= r` (or `g'' <= D` on the
    segment). This holds for the family.
- **Proposition 5.3 (log factor, base 1.072): correct with a wording fix.**
  - The slice algebra is right: `e_r = -sign(b_{2r}) sign(b_{2r-1})`, the
    sign flips preserve the cube, and `M = 2(D-b)I - bA` needs `D > 2b`.
  - `lambda_geo(M) = 2.0944` (2.0953 from the spectrum at `k = 400`); the
    base is 1.0723.
  - The ellipsoid-restricted values are valid lower bounds. My full-cube
    quadrature gives 2.801 (`n = 2`), 4.291 (`n = 4`) and 1.606
    (`n = 2`, `eps = 1e-2`), against the note's 2.80, 4.05 and 1.61.
  - *Fix (lines 516–517).* The proof of face-exact Theorem 3.4 needs the
    *chord* gap along `e_i - sign(b) e_j`. That is a property of the McCormick
    gap. It does not follow from the inequality (M_b) as defined on line 154:
    the chord product `min(δ_i^-, δ_j^+) min(δ_i^+, δ_j^-)` and `d_i d_j` are
    not comparable. State the hypothesis as "gap at least the termwise
    McCormick gap", which the note's prose already describes.
- **Conjecture 5.4: the evidence needs recalibration.**
  1. Grid-restricted optima are *upper* bounds on `N_cert`. That they are at
     least `2^n` is weak evidence for a lower bound.
  2. At `n = 2`, `eps = 1e-6`, the grid optimum is **12**, not 10. The
     independent-bound rerun (`grid_dp_check.py`) reproduces 4 (`1e-2`) and 8
     (`1e-4`) at `n = 2`, and 10 (`1e-2`) and 16 (`1e-3`) at `n = 3`. The
     corrected sequence 4, 8, 12 is linear in `log(1/eps)`, which supports the
     `log(1/eps)` half of the conjecture more cleanly.
  3. Section 1.5 above shows that the `2^n` half needs an argument beyond
     single-box volume.
- **Proposition 5.5: correct.** The per-variable factors 16.53 and 19.95 are
  reproduced.
  - *Fix (lines 602–604 and Summary item 5).* The justification for binary
    bisection, "changes the count by at most a factor `2^n`", would give
    `(2C)^n`, not the `C^n` stated for "uniform bisection" in the Summary.
  - The correct and simpler argument is that validity is monotone under
    inclusion. Then each binary leaf inside a level-`j` cube `Q` either equals
    `Q`, a dyadic leaf, or contains a valid level-`(j+1)` subcube, and the
    subcubes of distinct binary leaves are distinct. So widest-side binary
    bisection has *at most* as many leaves as the dyadic scheme.

## 4. Section 6 (per-factor alphaBB): correct

Recomputed independently:
- `alpha_f` = 0.1403 (`h'' = 2`) and 0.2472 (`h'' = 0.8`);
- `lambda_geo(2I + 0.8A)` = 1.6 (1.6012 from the spectrum at `n = 400`);
- repository Theorem 3.1 bases 0.7791 and 1.0342, with the threshold
  `pi/(4e) = 0.2889`;
- center-volume bases 1.3351 and 1.5149, against the note's 1.3338 and 1.5160.
  The differences are grid resolution in `mu`.

Proposition 6.1 is correct. The base-above-1 argument
(`mu K <= 1/2`, `mu alpha <= 1/4`) checks out.

The table uses the anisotropic form of Theorem 3.1 (`prod alpha_i^(1/2)`,
with `alpha_f` at the two end variables). This is not literally the
repository statement, which uses one `alpha`. It is a valid generalization
(AM–GM, as in face-exact Theorem 3.4, step 4), and the note should say so.

## 5. Section 7 numerics

### 5.1 Reproduced

- **`bb_path.py` toy B&B, `eps = 1e-4`.** Bisection counts match with an
  independent bound:
  - `mc`, `kappa = 0`, `c = 0`: 24, 100, 320, 962, 2780 (note 2778), 7976
    (note 7962);
  - seed 0: 20, 80, 249, 738, 2254;
  - `kappa = 0.1`, `c = 0`: 28, 110, 342, 1014, 2974 (note 2972);
  - alphaBB bisection: 32, 114, 316, 804, 1992, 4828, exact.
  - `mcx`, `kappa = 0`, gives 320 and 962, which confirms "mc = mcx for
    `kappa = 0`" (line 685). That run is not in the logs; add it.
  - The growth factors 2.7–3.1 per variable (Section 7.3) stand.
- **Leaf locations.** 82% of leaves at sup-distance below 0.3 and 46% below
  0.1 (`n = 8`); 1604 of 1698 added leaves within 0.03 (`n = 6`). Correct from
  `leaves_a.log` and `leaves_c.log`.
- **The `log(1/eps)` slopes for seed 0.** 60, 560 and 5000 per decade
  (bisection); 46, 390 and 3250 (`vw`). Correct from the logs. Seed-0
  instances show no bound discrepancy above 1e-8 at `eps = 1e-4` or `1e-6`
  (`bb_crosscheck_seed0*.log`).
- **SCIP, one data point.** Seed 0, `n = 4`, `absgap = 1e-4`: 217 nodes.
  - The incumbent value is **2.51e-6 below** the true `f* = -0.033795168`.
    Each `t_i` sits 7–9e-7 below its expression.
  - The incumbent's true `f` is 6.1e-7 above `f*`.
  - So the note's explanation (line 804–807) is confirmed. The quoted
    "2.3e-6" and "3.6e-6" are from the no-propagation runs; the default runs
    give 2.5e-6 and 3.5e-6.

### 5.2 Wrong or unsupported

**(a) `bb_path.py` bound errors on the degenerate instance.** For
`kappa = 0`, `c = 0` (`x* = 0` on the dyadic grid), HiGHS's QP sometimes
returns an objective up to 1.5e-4 *above* the exact QP optimum. Clarabel
direct and cvxpy + Clarabel agree with each other to 1e-11.

The run's "ok" check tests only that `f(x_hat) >= f* - 1e-9`. It cannot detect
an overestimated bound.

Effect on bisection counts (`bb_crosscheck.py`, pruning by the exact bound):

| `eps` | `n` | note (`bb_path`) | exact bound | flipped pruning decisions |
|---|---|---|---|---|
| `1e-2`, `1e-3` | 2–8 | — | equal (±3) | 0–3 |
| `1e-4` | 6 / 7 | 2778 / 7962 | 2780 / 7976 | 2 / 10 |
| `1e-5` | 4 / 5 / 6 | 400 / 1184 / 3378 | 422 / 1264 / 3636 | 6 / 16 / 44 |
| `1e-6` | 2 / 3 / 4 / 5 / 6 / 7 | 32 / 140 / 448 / 1298 / 3654 / 10182 | 38 / 162 / 522 / 1562 / 4474 / 12758 | 2 / 4 / 8 / 24 / 58 / 162 |

At `n = 8`, `eps = 1e-5` and `1e-6`, the note reports 27,888 and 29,282. The
exact bound gives 30,474 and 37,500, with 402 and 498 flipped decisions. The
corrected `n = 8` row is 9508, 16534, about 23500, 30474 and 37500, with
per-decade increments of about 7000 at every step.

Consequences:
- Section 7.5, lines 841–843, says "With `x* = 0` on the dyadic grid ... the
  slope falls at small `eps` ... the unfrustrated orthants become exact". This
  is **an artifact**. With exact bounds the per-decade increments are
  constant:
  - `n = 4`: 100, 88, 102, 100;
  - `n = 6`: 832, 826, 856, 838;
  - `n = 8`: 7026, 6954, 6986, 7026.
- The `kappa = 0` row of the Section 7.5 table must be recomputed.
- In the Section 7.6 table, `n = 2`, `eps = 1e-6`: bisection has 38 leaves and
  the grid optimum is 12.
- Fix the tool: verify every bound with a second solver or with HiGHS's dual
  bound, or use the LP (`mcx`) relaxation for `kappa = 0`.
- The trees reported at `eps <= 1e-5` for this instance are not certificates,
  because some pruned boxes are invalid.
- The Section 7.3 conclusions at `eps = 1e-4` are unaffected (errors of 0.2%
  or less).

**(b) SCIP runs are outside (M_b).** SCIP 10 separates PSD minor cuts by
default (`separating/minor/freq = 10`). Its RLT separator runs at the root
(`separating/rlt/freq = 0`) but had no effect here. Evidence from
`scip_probe.py` and `scip_minor.py`, `absgap = 1e-4`:

| instance | `n` | default nodes | minor separator off | RLT off |
|---|---|---|---|---|
| `kappa = 0`, `c = 0` | 4 | 1 | 21 | 1 |
| `kappa = 0`, `c = 0` | 8 | 21 | 14,011 | 21 |
| seed 0 (PROGRAM) | 4 / 6 / 8 | 217 / 1055 / 4447 | 529 / 4367 / 36,081 | — |
| `kappa = 0.1`, `c = 0` | 4 / 6 / 8 | 81 / 1116 / 6410 | 134 / 1841 / 19,781 | — |

With the minor separator off:
- SCIP's growth on seed 0 is about 2.9 per variable (`n = 4 → 8`), in the
  toy B&B range. On `c = 0` it is about 3.3–3.5.
- So the minor (PSD) cuts are "the component" that the note could not
  identify (line 816–817). They also explain most of the gap between SCIP's
  2.1–2.3 and the toy's 2.7–3.1.

These statements must be revised:
- lines 814–815: "This fits Theorem 1, which does not depend on convexity";
- line 891–893: "SCIP's node relaxation ... should satisfy (M_b)";
- the use of SCIP's default runs as support for the mechanism in Section 8.

The PROGRAM correction (PROGRAM.md lines 57–63) reports correct measurements.
But the `kappa = 0` counts reflect how SCIP schedules minor cuts, not the
(M_b) mechanism.

**(c) SCIP tolerance: the explanation is incomplete** (lines 802–809). In
SCIP, `limits/absgap` is a global stopping criterion. Nodes are cut off when
`LB >= primal bound`, with no `absgap` slack. That is why counts do not change
for `absgap = 1e-4..1e-6`, and why the runs end with `dual = primal`
("optimal"). The incumbent lying 2.5–4.4e-6 below `f*` then sets the
effective per-node tolerance.

If pruning used `UBD - absgap`, an incumbent a few 1e-6 low would *not* make
the counts insensitive to `absgap`. The conclusion "compare with our
`eps = 1e-6`" still stands. This relies on SCIP's documented meaning of
`limits/absgap`; I did not read SCIP's source code.

**(d) Small inconsistencies.**
- Summary lines 89–90 say "All counts are above Theorem 1's bound ... by
  factors of about 10–2000".
  - The grid optima are only 2.5–7 times the bound: `4/1.58` and `32/4.40`.
  - SCIP counts at `n = 2` (1 node, against 1.59) and at `kappa = 0`, `n = 4`
    (1 node, against 4.4) are *below* it, because they are outside the model.
- The oracle rule changes counts by between +55% and -17% on seed 0
  (`mc`, `n = 10`: 164,774 against 198,363). The -18% is seed 1.
- Summary line 93 says the root solve holds "only for `n <= 4`". PROGRAM.md
  now says "up to `n = 5`".
- Summary item 7 says every rule grows 2.7–3.1 "except one rule that stalls".
  alphaBB bisection grows 2.39. That is a different relaxation, but say so.

## 6. Significance, novelty and the meaning of "single-tree"

**Definition.** "Single-tree" is made precise by the certified cover (Section
1.3) and Lemma 1.2. The statement is meaningful and not vacuous *for the
declared relaxation class*. The bound is really about that class:
- It holds for a convex QP (`kappa = 0`), so it is not about nonconvexity or
  search structure.
- Relaxations outside the class avoid it near `x*`:
  - PSD-minor or SDP cuts. SCIP adds these by default, and they collapse the
    `kappa = 0` case at `n <= 8` (Section 5.2(b) above).
  - Convexity detection on the aggregated sum.
  - For Theorem 2, simply a different factorization (Section 2 above).
- Level-1 RLT does not avoid it, because it equals McCormick here.

**For the program.** A single-tree versus decomposition separation must fix
the relaxation class on both sides. The decomposition certificate in
PROGRAM.md uses child minorants of subtree value functions, which are stronger
objects than termwise McCormick. Otherwise the separation measures relaxation
strength, not search structure.

The title, Summary and Section 8 should put "termwise McCormick" (and "for the
given factorization" for Theorem 2) up front, and should drop the SCIP-default
attribution.

**Novelty.** I checked the repository and the program's literature audit
(`research-20260929/literature/decomposition-bb-prior.md`, C1). I did not run
a new web search.

- **Same witness.** The face-exact note's Proposition 3.10 uses the same
  witness, the center of `C ∩ R`, with the gap of one edge and a uniform
  bound `m <= eta`. It gives `O(1)` near an isolated minimizer. The note
  explains this correctly (lines 235–244).
- **Cluster problem.** Neumaier 2004 (Section 15) and Wechsung–Schaber–Barton
  2014 predict, as *estimates* for specific box sizes and schemes, clusters
  exponential in `n` for second-order relaxations whose prefactor is above
  about `9 lambda_1/4`. Termwise McCormick has prefactor growing like `n`.
  Theorem 1 is a rigorous every-certificate version of that prediction.
- **MILP.** Exponential lower bounds for B&B (Basu et al.; Dey–Shah;
  Dey–Dubey–Molinaro) use different instances, with many optima, and
  different mechanisms.
- **Assessment.** I found no prior rigorous statement of Theorem 1's form. The
  covering-by-volume technique itself is standard, including the repository's
  own Theorem 3.1.
- *Fix (lines 961–962).* "We did not search the literature" should be replaced
  by a pointer to the audit's C1 entry and the cluster-problem sources.

## 7. Per-claim verdicts

| Claim | Location | Verdict | Fix |
|---|---|---|---|
| Lemma 1.1 | l. 124–142 | correct | — |
| Lemma 1.2 (runs give certified covers) | l. 178–193 | correct | Summary: say "leaves + 2n per tightening round" |
| (M_b) for inherited cuts | l. 161–163 | correct with fix | inherited termwise cuts are dominated, not "pointwise below" |
| Lemma 2.1 | l. 212–233 | correct | — |
| Lemma 3.1 | l. 252–276 | correct | — |
| Theorem 1(a), (b) | l. 278–314 | correct | — |
| Corollary 1.3 | l. 316–331 | correct | "less than 1%" only for `n >= 8` |
| Remark "Where the constant is lost" | l. 354–360 | gap | single-box volume is nearly exhausted (Section 1.5 above); the loss is in covering |
| Remark "Other graphs" | l. 350–353 | correct (sketch) | replace `eps''` by `2 eps''/Delta` |
| Lemma 4.1 | l. 364–391 | correct | — |
| Theorem 2 | l. 393–421 | correct, significance gap | base about 1.205 (1.2021 conservative); state factorization dependence and the balanced-factor counterexample |
| Proposition 5.1 | l. 427–441 | correct | — |
| Proposition 5.2 | l. 451–487 | correct | note that the quadratic upper bound on `G` needs `W <= r` |
| Proposition 5.3 | l. 500–534 | correct with fix | hypothesis is the McCormick chord gap, not (M_b) |
| Conjecture 5.4 evidence | l. 536–548 | gap | grid optima are upper bounds; `n = 2`, `1e-6` is 12; `2^n` is out of reach of volume arguments |
| Proposition 5.5 | l. 574–605 | correct with fix | binary bisection <= dyadic by monotonicity, not "factor `2^n`" |
| Proposition 6.1, Section 6 table | l. 620–642 | correct | mention the anisotropic form of Theorem 3.1 |
| Section 7.3 counts | l. 742–776 | correct (±0.2%) | log the `mcx`, `kappa = 0` runs |
| Section 7.5 `kappa = 0` row; "slope falls" | l. 831–843 | false | recompute with verified bounds; slope is constant |
| Section 7.6, `n = 2`, `1e-6` | l. 857 | false | 38 bisection leaves, grid optimum 12 |
| Section 7.4 SCIP incumbents below `f*` | l. 802–811 | correct, explanation incomplete | add that node cutoff ignores `absgap` |
| Section 7.4 / 8: SCIP satisfies (M_b); `kappa = 0` "fits Theorem 1" | l. 812–817, 890–898 | false | SCIP's minor (PSD) separator is outside (M_b) and explains the root solves and the lower growth |
| Summary 7: "all counts above ... by 10–2000" | l. 89–90 | false as stated | grid optima 2.5–7 times the bound; SCIP counts below it |
| Literature statement | l. 961–962 | gap | cite the audit C1 and the cluster-problem literature |

## 8. What I verified myself, and commands run

All commands were run from `research-20260929/reviews/face-exact-review-checks/`
unless stated otherwise. Logs are in `logs/`. These are targeted local checks,
not CI.

- **By hand.** Every step of Lemmas 2.1, 3.1 and 4.1, Theorems 1 and 2, and
  Propositions 5.1, 5.2, 5.3, 5.5 and 6.1. The McCormick gap for both signs.
  The Theorem 3.1 base formula against the constrained note's statement. The
  face-exact Proposition 3.10 comparison.
- `python3 constants.py > logs/constants.log`: `S_max`, `rho_max`, Lemma 3.1
  on a grid, Theorem 1 values and Lagrangian, Theorem 2 base, alphaBB
  constants and bases, `lambda_geo`, Proposition 5.3 base and full-cube
  quadrature, Proposition 5.5 factors.
- `python3 adversarial_boxes.py [quick]` (`logs/adversarial_full.log`,
  `logs/adversarial_quick.log`) and `python3 adversarial_large.py`
  (`logs/adversarial_large.log`): largest valid boxes against the exact `nu`
  and the closed form, for cases A–E, `n = 2..8`.
- An inline cross-check of the independent bound against `bb_path.relax` and
  cvxpy on 600 random boxes. The one discrepancy was 5.75e-5, in HiGHS.
- `python3 bb_crosscheck.py KAPPA CMODE EPS n...` for:
  - `kappa = 0`, `c = 0` at `eps` = 1e-2, 1e-3, 1e-4, 1e-5, 1e-6;
  - seed 0 at 1e-4 and 1e-6;
  - `kappa = 0.1`, `c = 0` at 1e-4.

  Logs: `logs/bb_crosscheck_*.log`.
- `python3 abb_crosscheck.py 1e-4 2 3 4 5 6 7` (`logs/abb_crosscheck.log`).
- `python3 grid_dp_check.py` for `(n, K, eps)` = (2, 4, 1e-2), (2, 7, 1e-4),
  (2, 10, 1e-6), (3, 4, 1e-2) and (3, 5, 1e-3) (`logs/grid_dp_check_*.log`).
- `python3 ../../theory-face-exact/bb_path.py mcx bisect 0.0 zero 1e-4 4 5`
  (`logs/mcx_k0.log`).
- `python3 scip_probe.py` (`logs/scip_probe.log`) and
  `python3 scip_minor.py {zero,seed0} 1e-4 4 6 8`
  (`logs/scip_minor_*.log`). SCIP 10.0 via PySCIPOpt 6.2.1, one thread.
- **Read, not rerun.** The note's `bounds.log`, `checks.log`, `summary.log`,
  `scip_runs.log`, `scip_noprop_*.log`, `leaves_*.log` and `grid_dp*.log`. I
  checked the derived numbers in the note against them.
