# Second wave, small instances: hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050, pindyck, methanol50 and LINDO-only closures

Date: 2026-09-30. Status: computational results with proofs in this file.
Independently verified (Section 11). pindyck, which this report does not
close, was closed later by
[`pindyck-extension.md`](pindyck-extension.md). Code, logs and downloaded MINLPLib points are in
`open-instances-wave2/small/` (file list in Section 10). All runs were
single-threaded and time-limited.

*Provenance note (root).* The agent that produced these results could not
write this file because its tool environment blocked report writes; the
root saved the agent's report text verbatim on 2026-09-30.

## 1. Summary

A "dual bound" below is a number L with L ≤ f(x) for every exactly feasible
x of the OSIL model (for maximization, an upper bound). Listed values come
from `open-instances-scout/fetched.csv` (MINLPLib pages fetched 2026-09-29).

| instance | listed primal | best listed dual (solver) | our rigorous dual bound | our primal (max violation) | gap after | method |
|---|---|---|---|---|---|---|
| hvycrash | −0.2185 (p3, viol. 1e-12) | −2.185e8 (SCIP) | **−0.2185 exactly** | −0.2185, 60-digit point (3.9e-62) | 0 | exact identity: the objective is constant on the feasible set; explicit feasible point |
| ex6_2_7 | −0.16084762 | −1.06726714 (BARON) | **−0.16084761549352554** | −0.16084761546360086 (6.7e-52; rows exact) | 3.0e-11 | Lagrangian over the 3 mass balances; tangent-plane test by rigorous 2-D interval branch and bound |
| ex6_2_5 | −70.75207783 | −111.4201713 (BARON) | **−70.752077836333563** | −70.752077833447706 (8.6e-50) | 2.9e-9 | same |
| etamac | −15.29467564 (p1, viol. 1.3e-10) | −15.40567054 (SCIP) | **−15.294675643368096** | −15.2946756433680896 (6.0e-14) | 6.6e-15 | convex relaxation (production equalities to ≤, concave majorant) + KKT tangent-plane certificate |
| pricing050 (max) | −1813.829078 (p1, viol. 7.3e-10) | −1534.3281 (SCIP) | **−1813.8290784519704** (upper bound) | −1813.8290784519731 (exactly feasible) | 2.7e-12 | Lagrangian over the 5 rows; 50 certified 1-D minimizations |
| pindyck | −1170.486285 | −1437.941134 (SCIP) | **none** (certificate failed; see [`pindyck-extension.md`](pindyck-extension.md), which closes it) | −1170.4862854360885621 (8.3e-28) | — | reduced-space concavity, certified only on the box p* ± 10 |

Findings on listed bounds (Section 8):

- **methanol50:** LINDO's listed dual bound 0.00802826 is invalid. MINLPLib
  point p4, re-solved (polished) to row violation 1.1e-26 with the kinetic
  parameters held, has objective 0.0079302187922673 (constant 5.01625659
  included). That is 1.2% below the "bound".
- **rocket100, rocket200, rocket400:** LINDO's listed dual bounds are also
  invalid, by small amounts. CONOPT local solves, polished to row violation
  1.5e-27 to 1.7e-27 with the thrust held, give:
  - rocket100: −1.0128320069141, below LINDO's −1.0128319 by 1.1e-7;
  - rocket200: −1.0128356770687, below −1.01283563 by 4.7e-8;
  - rocket400: −1.0128365294832, below −1.01283634 by 1.9e-7.

  These points also improve the listed primal values. For rocket200, LINDO
  is the only solver that "closes" the instance; the next listed bound is
  SCIP's −1.05708936.
- **methanol200/400, pinene100, popdynm25:** local solves reproduce the
  listed values. No counterexample to the LINDO bounds was found. This is
  weak evidence, not a certificate.

## 2. Conventions and common checks

- **OSIL reading.** `ev.py` uses the verifier's reader
  `reviews/open-instances-verification/osilx.py`. It keeps decimal strings
  and reads `<obj constant=...>` and row constants; `ev.evaluate` adds the
  objective constant. Every certificate script checks the row, bound and
  objective pattern it uses by exact string comparison against the parsed
  expression trees.
- **Point evaluation.** Points are evaluated in 50–60-digit mpmath arithmetic
  from their decimal values. The reported violations are exact violations of
  the stated decimal vectors. Variables missing from a `.sol` file are set
  to 0, and the bound check covers this.
- **Interval arithmetic.**
  - `ia.NI` does vectorized numpy intervals. Each `+ − × ÷ √` is computed in
    IEEE round-to-nearest and then widened by one `nextafter` step outward.
    Decimal constants are enclosed by the correctly rounded double ± 1 ulp.
  - `ia.ilog` is a rigorous log built only from these operations. It reduces
    x = m·2^e exactly and sums 2·atanh((m−1)/(m+1)) as a series with an
    explicit remainder bound (1e-19). Tested against mpmath at 8,109 points:
    every enclosure was correct, with relative width ≤ 4.3e-15. The scripts
    do not rely on libm `log` for rigor.
  - The remaining certificates (etamac, pricing050, hvycrash) use mpmath `iv`.
- **Targeted commands only.** No project-wide checks were run and no CI was
  inspected. Section 10 lists the commands.

## 3. hvycrash: optimum exactly −0.2185, feasible set nonempty (verified)

**Structure** (`hvycrash.py` checks all 150 rows, 201 bounds and the
objective). Stage k = 1..50 has:

- θ_k = x_k ∈ [0, 6.2831854];
- c_k = x_{50+k} ∈ [0.08, 0.417];
- r_k = x_{101+k}, free;
- θ_0 = x101 ∈ [0, 6.2831854];
- the accumulator s_k = x_{202−k}, free.

With D_k = 0.486237 c_k² + 0.0162079 > 0, each stage has three rows:

- acc_k: s_k = s_{k−1} + 4.37e-3 cos θ_k / (D_k r_k²), with s_0 := 0. The
  objective is s_50 = x152.
- alg_k: −1/r_k − cos θ_k / (D_k r_k³) = 0.
- dyn_k: 0.1 θ_{k−1} + 4.37e-3 c_k/((0.3 c_k² + 0.01) r_k²) −
  4.37e-3 cos θ_k/(D_k r_k⁴) − 0.1 θ_k = 0.

**Identity.** alg_k is defined only for r_k ≠ 0. Multiplying it by −r_k
gives cos θ_k/(D_k r_k²) = −1. So every accumulator increment is exactly
−4.37e-3, and x152 = −50 · 4.37e-3 = −0.2185 at every feasible point. This
was checked in Fraction arithmetic. The scout's claim is correct.

**A feasible point exists, so the optimum is −0.2185 and not +∞.** Construct
the point backwards:

- set c_k = 0.08 and θ_50 = 3;
- set r_k = √(−cos θ_k / D_k), which makes alg_k hold identically;
- solve dyn_k for θ_{k−1}; the row is linear in θ_{k−1} with coefficient
  0.1, so dyn_k holds identically;
- take s_k from acc_k.

Only the bounds remain to check. mpmath interval arithmetic (50 digits)
verifies:

- cos θ_k < 0 for k = 1..50, so every r_k is real and nonzero;
- all θ_k ∈ [0, 6.2831854]; θ_0 ≈ 2.6565 and θ_1 ≈ 2.6638.

A 60-digit version of this point has objective −0.2185 and row violation
3.9e-62 (`logs/hvycrash_point.txt`).

**MINLPLib points (50 digits).**

| point | objective | max row violation | comment |
|---|---|---|---|
| p3 | −0.218499999999997 | 1.02e-12 (e2) | max_k \|cos θ_k/(D_k r_k²) + 1\| = 8.8e-13 |
| p2 | −0.21412999999989 | 6.3e-10 (e149) | r_50 = 1.58e9 makes stage 50's increment ≈ 0: a tolerance artifact |
| p1 | −0.214129999501985 | 4.05e-8 (e149) | r_50 = 2.47e7: a tolerance artifact |

**Tolerance remark.** Suppose each row may be violated by at most τ
(absolute). Then alg_k gives cos θ_k/(D_k r_k²) = −1 − e_k r_k with
|e_k| ≤ τ. An increment below −4.37e-3 needs e_k r_k > 0. Because
|cos θ_k| ≤ 1, this forces r_k² < 1/D_k ≤ 1/0.0162079, that is,
|r_k| < 7.86. So x152 ≥ −0.2185·(1 + 7.86τ) − 50τ, which for τ = 1e-8 is
−0.2185 − 5.2e-7. The listed SCIP value, −2.185e8, is therefore far beyond
any tolerance effect.

## 4. ex6_2_7 and ex6_2_5 (Gibbs free energy): closed to 3.0e-11 and 2.9e-9

### 4.1 Structure (checked in `gibbs_model.py`)

- There are 9 variables n_{p,i} (phase p, component i) in [1e-7, b_i], and
  3 rows Σ_p n_{p,i} = b_i:
  - ex6_2_7: b = (0.4, 0.1, 0.5);
  - ex6_2_5: b = (40.30707, 5.14979, 54.54314).
- The objective is a sum of terms, and no term mixes phases, so
  f(n) = Σ_p G_p(n_p).
  - ex6_2_7 has three identical UNIQUAC-type phases (26 terms each; the
    expression trees are identical after renaming variables).
  - ex6_2_5 has two identical liquid phases (29 terms) and one ideal phase,
    Σ n_i (ln(n_i/Σn) + 0.156969560191053).
- **Scaling, exactly.** A rule-based analysis of the expression trees, in
  Fraction arithmetic, shows G_p(t n) = t G_p(n) + t ln t · R_p(n), where
  R_p is linear:
  - ex6_2_5: R_p = 0, so G_p is exactly homogeneous of degree 1;
  - ex6_2_7: R_p = (0, 0, 5e-14), because the n3 ln n3 coefficients do not
    cancel exactly (8.73945638067505 + 1.868 ≠ 10.607456380675).

### 4.2 Method and validity

For any λ ∈ R³ and every feasible n:

    f(n) = λ·b + Σ_p [G_p(n_p) − λ·n_p].

Write n_p = t y, where t = Σ_i n_{p,i} ∈ (0, tmax], tmax = Σ_i b_i, and y is
in the simplex. The variable box forces y_i ≥ ymin = 1e-7/tmax. Then

    G_p(n_p) − λ·n_p = t (G_p(y) − λ·y) + t ln t · R_p(y)
                     ≥ min(0, tmax · m_p) − max_i R_p,i / e,

where m_p is any lower bound of the tangent-plane function G_p(y) − λ·y over
{y ≥ ymin, Σy = 1}. The second term uses R_p ≥ 0 and t ln t ≥ −1/e. Summing
over phases gives the dual bound

    λ·b + Σ_p [min(0, tmax m_p) − max R_p/e].

The last term is 0 for ex6_2_5 and −1.84e-14 per phase for ex6_2_7.

**Choice of λ.** The primal was found by multistart SLSQP (200 starts). The
12-equation KKT system (equal chemical potentials in all three phases, plus
the mass balances) was then solved by Newton's method at 50 digits, to a
residual below 1e-48. λ is these chemical potentials rounded to doubles. Any
λ gives a valid bound.

**Computing m_p (2-D interval branch and bound, `gibbs.py`).** The two
coordinates are the components with the smaller amounts at the KKT point.
The third component is dependent; it is enclosed separately and clipped at
ymin. Each box gets the best of three lower bounds:

- the natural interval extension;
- the mean-value form with an interval gradient;
- a second-order form, f(c) + ∇f(c)·d + ½ λ_lo |d|². Here λ_lo ≤ λ_min of
  the interval Hessian (from nested interval automatic differentiation), and
  the 1-D quadratics are minimized exactly.

A box is fathomed when its lower bound is ≥ −τ, with τ = 1e-11. All
arithmetic is outward-rounded, including `ia.ilog`.

As a sanity check (not part of the proof), f was evaluated in 40 digits at 2
random points in each of 1,000 sampled leaves: the 200 leaves with the lowest
bounds plus 800 random ones. f was never below the leaf bound; the smallest
margin was +1.8e-12.

### 4.3 Results

| | ex6_2_7 | ex6_2_5 |
|---|---|---|
| λ | (−0.23993666802, −0.54068374801, −0.02160914691) | (−0.92114611232, −2.27778930378, −0.40139310691) |
| λ·b | −0.1608476154635759 | −70.7520778334477058 |
| branch and bound | 1 distinct phase: 488,064 boxes, certified min ≥ −9.96e-12, 44 s | liquid: 5.9M boxes, ≥ −9.97e-12, 566 s; ideal: 1,563 boxes, ≥ −8.9e-12 |
| **dual bound** | **−0.16084761549352554** | **−70.752077836333563** |
| primal | −0.16084761546360086 | −70.752077833447706 |
| gap | 3.0e-11 (= 3 tmax τ) | 2.9e-9 (= 3 tmax τ, tmax = 100) |

**Primal points** (`logs/ex6_2_*_primal.txt`). Two phases are rounded to 17
digits, and the third is set to b minus the other two in exact decimal
arithmetic. The rows therefore hold to the precision of the 50-digit
evaluation (6.7e-52 and 8.6e-50), and the bounds hold exactly.

The phase splits:

- ex6_2_7 has three distinct phases:
  - y = (0.0278, 0.0021, 0.9702), t = 0.317;
  - y = (0.6928, 0.0040, 0.3032), t = 0.485;
  - y = (0.2790, 0.4919, 0.2291), t = 0.198.
- ex6_2_5 has two distinct liquids and the ideal phase:
  - liquid, y = (0.0567, 6.0e-7, 0.9433), t = 15.92;
  - liquid, y = (0.5180, 0.0511, 0.4309), t = 60.73;
  - ideal phase, y = (0.3402, 0.0876, 0.5722), t = 23.35.

The MINLPLib p1 points have the same values (−0.1608476154636 and
−70.7520778334477). So the listed primal values are globally optimal to
within the gaps above. The Lagrangian dual has no duality gap: the tangent
planes support the Gibbs surfaces globally.

## 5. etamac: closed to 6.6e-15 (hidden convexity)

### 5.1 Structure (checked in `etamac.py`)

- 9 periods; objective min −Σ β_t ln C_t, with β_t > 0.
- Linear rows:
  - capital: KN_t = 4.91287681 I_{t−1} and K_{t+1} = 0.8153726976 K_t + KN_{t+1};
  - new labor LN and new energy EN;
  - output: Y_{t+1} = 0.8153726976 Y_t + YN_{t+1};
  - energy cost: EC_t = (c_L,t L_t + c_E,t E_t)/1000;
  - budget: Y_t = C_t + I_t + EC_t;
  - terminal row: 0.07 K_9 ≤ I_9.
- Nonlinear production rows, e9–e16: YN_t = CES_t =
  (a_t KN^−p1 + b LN^−p2 EN^−p3)^−q, with p1 = 0.342222222222222,
  p2 = 0.427777777777778, p3 = 0.794444444444445 and q = 0.818181818181818.
- Period 1 (e43): Y_1 − (b LN_1^−p2 EN_1^−p3 + c0)^−q = 3.4653339648.
- Bounds: K_1 is fixed, EC is free, and every other variable has only a
  positive lower bound.

### 5.2 Relaxation and validity

- **Relaxation R.** The production rows become YN_t − CES~_t ≤ 0 and
  Y_1 − CES~_1 ≤ 3.4653339648, where CES~ ≥ CES is defined below. Every
  etamac-feasible point is feasible for R.
- **Concavity, with the exact decimals.** Let r = 1/q, u = KN^(p1 q) and
  v = LN^(p2 q) EN^(p3 q). Then CES = (a u^−r + b v^−r)^(−1/r). This is a
  weighted power mean with a negative exponent, so it is concave and
  nondecreasing in (u, v).
  - u is concave, since p1 q = 0.27999999999999975.
  - v is not quite concave. With the file's decimals, s = (p2 + p3) q =
    1 + 4.14e-16, so v is a Cobb–Douglas function of degree slightly above 1.
    The scout's statement that the CES function is concave is therefore not
    exactly true.
- **Fix: a concave majorant.** Let w = LN^(p2 q/s) EN^(p3 q/s). It has degree
  exactly 1 and is concave. On the box below, w ≤ W = 2022.06, so
  v = w^s ≤ κ w with κ = W^(s−1) ≤ 1 + 3.2e-15. Define

      CES~ = (a KN^−p1 + b κ^−r LN^(−p2/s) EN^(−p3/s))^−q.

  CES~ is concave by the composition rule, and CES~ ≥ CES on the box.
- **Box.** These bounds hold on R's feasible set:
  - Y_1 ≤ 3.4653339648 + c0^−q;
  - YN_t ≤ a_t^−q KN_t^(p1 q), obtained by dropping the LN/EN term, which
    is ≥ 0;
  - KN_t = 4.91287681 I_{t−1}, with I_t ≤ Y_t − C_lb − EC_lb,t;
  - a forward recursion for Y, then bounds on C, EC, L, E, LN, EN and K from
    the linear rows.

  The largest upper bound is 2062.8 (on E_9), and the bound on Y_9 is 26.73.
- **Certificate.** Take the Lagrangian l = f + Σ ν h + Σ μ g~ + μ70 g70,
  where:
  - ν is free on the 60 linear equalities;
  - μ ≥ 0 on the 9 relaxed rows and μ70 ≥ 0 on e70.

  l is convex on the box. So l(x) ≥ l(x̂) + ∇l(x̂)·(x − x̂) for every x in the
  box, and the minimum of this linear bound over the box is a closed-form
  sum.
  - Evaluation: mpmath iv (40 digits), at a point x̂ and multipliers from a
    50-digit Newton solve of the KKT system (residual 2.7e-48).
  - Multipliers: all positive (min μ = 0.278, μ70 = 0.363). No variable is
    at a bound except the fixed K_1.
  - Gradient: the largest |∂l/∂x_j| over the free variables is 1.1e-16,
    which comes from CES~ − CES. ∂l/∂K_1 = 0.005, but it multiplies a
    zero-width range.

### 5.3 Results

- **Dual bound: −15.294675643368096.**
- **Primal:** the KKT point rounded to 17 digits. Objective
  −15.2946756433680896; max row violation 6.0e-14, caused by the 1e3
  coefficient in e60.
- **Gap: 6.6e-15.**
- MINLPLib p1 (−15.2946756434628, violation 1.3e-10) lies 9.5e-11 below the
  bound. Its violation allows this.
- The relaxation is tight, as expected. Raising YN_t to CES_t raises every
  later Y, and the gain can be passed on to C because β_t > 0. The
  certificate does not depend on this argument.

## 6. pricing050: closed to 2.7e-12

**Structure** (`pricing050_model.py`, checked):

- Objective: max −Σ c_j x_j, with c_j ∈ {0, 1, …, 20} and x ∈ [0,10]^50.
- 5 rows Σ_j a_ij x_j exp(g_ij x_j^p) ≤ r_i, with a_ij < 0, p ∈ {1, 2, 3} and
  g ∈ {−0.1, −1.0000000000000002e-2, −1.0000000000000002e-3}.
- Every term depends on a single variable.

**Method.** In minimization form, for μ ≥ 0:

    c·x ≥ −μ·r + Σ_j min_{[0,10]} F_j,   F_j(x) = c_j x + Σ_i μ_i a_ij x e^{g_ij x^p}.

- The multipliers came from Kelley cutting planes on a 20,001-point grid,
  followed by Newton's method (50 digits) on the KKT system of the
  Lagrangian minimizers.
- Only rows e5 and e6 have positive multipliers:
  μ = (0, 0, 0, 3.04890112081664, 2.16775096427457).
- Each min F_j is certified by a 1-D interval branch and bound in mpmath iv
  (natural extension plus mean-value form): 16,960 boxes in 5 s. The
  per-variable (upper − lower) widths sum to 3.2e-12.
- Each F_j has a single local minimum on [0, 10], so there is no Lagrangian
  duality gap.

**Results.**

- **Upper bound: −1813.8290784519704.**
- **Primal:** the KKT point rounded to 17 digits, with x11 raised by 1.3e-15
  to absorb the rounding. Objective −1813.8290784519731. The rows hold with
  slack ≥ 3.5e-15, so the point is exactly feasible.
- **Gap: 2.7e-12.**
- MINLPLib p1 (−1813.8290784498, violation 7.3e-10) lies 2.1e-9 above the
  bound. Its violation allows this.

## 7. pindyck: no global certificate (failure, with partial results)

*Superseded:* [`pindyck-extension.md`](pindyck-extension.md) closes pindyck
(concavity on a polytope containing the feasible set); verified in
[`../../reviews/pindyck-review.md`](../../reviews/pindyck-review.md).

**Structure** (checked in `pindyck.py`):

- prices p_t ≥ 0, t = 1..16;
- total demand: td_t = 0.87 td_{t−1} − 0.13 p_t + c_t;
- fringe supply: s_t = 0.75 s_{t−1} + 1.02^(−κ cs_t)(1.1 + 0.1 p_t), with
  cs_t = cs_{t−1} + s_t. The equation is implicit in s_t but has a unique
  root;
- OPEC demand and reserves: d_t = td_t − s_t ≥ 0 and R_t = R_{t−1} − d_t;
- objective: min −Σ δ_t d_t (p_t − 250/R_t).

Given p, every other variable is determined, so the problem is max J(p) over
16 prices.

**Primal.**

- Newton's method (50 digits) on ∇J = 0 gives J(p*) = 1170.4862854360885621.
- The full point, with states from the recursion, has row violation 8.3e-28,
  min d_t = 5.44 and min R_t = 350.3.
- 40 random L-BFGS-B starts all reach the same value, which matches
  MINLPLib p1.

**Attempted certificate: concavity in p.** The finite-difference Hessian of
J is negative definite at every sampled feasible point (largest eigenvalue
about −0.11). Feasibility implies two things:

- p lies in the box B = Π[0, p̄_t], where p̄_t = (td_t(0) − s_lb,t)/0.13
  ranges from about 100 to 202;
- p lies in the polytope P = {td_t(p) ≥ s_lb,t}.

If J is concave on the convex set B ∩ P, the tangent plane at p* bounds J
globally. The Hessian over B ∩ P was enclosed by interval second-order
forward automatic differentiation, using implicit differentiation for s_t.
Negative definiteness was then tested exactly: an LDLᵀ factorization in
rational arithmetic of −mid − ρ(radius) I, where ρ is bounded by the
Collatz–Wielandt formula.

| region | ρ(radius) bound | λ_max(mid) | negative definite? |
|---|---|---|---|
| B ∩ P (tightened s_lb) | 0.81 | −0.10 | no |
| p* ± 40 | 0.199 | −0.110 | no |
| p* ± 20 | 0.130 | −0.114 | no |
| p* ± 10 | 0.082 | −0.116 | **yes** |
| p* ± 5 / 2 / 1 | 0.037 / 0.015 / 0.007 | −0.116 | yes |

**Result.**

- J is certified concave on the box p* ± 10 in every price (intersected with
  B ∩ P). So p* is the unique maximizer there. This is a certified local
  statement only.
- **There is no global dual bound.** Over the full price range (0 to 200),
  the interval overestimation is about 8 times too large.
- Closing the gap would need one of these:
  - a branch and bound over the 16-D outer region, which is intractable with
    these bounds;
  - a different decomposition, such as dynamic programming or a Lagrangian
    over copied state variables (4-D state).
- The partial Lagrangian over the 16 periods that the scout proposed was not
  tried. The reason is an argument, not a computation: once the linear rows
  are dualized, d_t and p_t become independent within each period's block,
  and −δ d p is bilinear, so the block minima go to box corners.
- SCIP's −1437.94 remains the only listed bound.

## 8. methanol50 and instances closed only by LINDO

**methanol50.** 50-digit evaluation, with the objective constant 5.01625659
included:

| point | objective | max row violation |
|---|---|---|
| p1 | 0.009022286837986 | 1.3e-14 |
| p2 | 0.008031004666870 | 8.1e-12 |
| p3 | 0.008028255493908 | 1.2e-11 (equals LINDO's "bound" 0.00802826) |
| p4 | 0.007930218792267 | 8.5e-12 |

`polish.py` holds the 5 kinetic parameters (x1502–x1506) at p4's values. It
then runs Newton's method on the remaining square system (1,497 × 1,497),
using exact 60-digit residuals and a double-precision sparse Jacobian.

- The residuals fell 8.5e-12 → 9.5e-25 → 1.8e-38 → 2.9e-52, and the steps
  shrank quadratically.
- After rounding to 30 digits, the point has objective **0.0079302187922673**
  and violation 1.1e-26, with all bounds satisfied.
- So LINDO's 0.00802826 is not a valid bound: it lies 1.2% above a feasible
  value.
- This check is numerical. An interval Newton (Krawczyk) step would make the
  existence of the nearby exact solution rigorous.

The good methanol50/100 points seem to lie on a different solution branch of
the collocation equations:

- With the parameters fixed at methanol100 p2's values (objective
  0.0078281296, violation 2.8e-10), CONOPT finds states with objective
  0.0165, not 0.0078.
- methanol200 and methanol400 converge to 0.0090222898 from every start
  tried.

**LINDO-only closures named by the scout.** All local solves were
time-limited GAMS 54.3 runs with CONOPT and IPOPT (KNITRO was not licensed).

| instance | LINDO "bound" = listed primal | other listed bounds | what was found |
|---|---|---|---|
| rocket100 | −1.0128319 | COUENNE −1.01283202 | polished CONOPT point **−1.0128320069141** (viol. 1.5e-27). LINDO invalid by 1.1e-7; COUENNE consistent |
| rocket200 | −1.01283563 | SCIP −1.05708936, ANTIGONE −1.07333642 | polished CONOPT point **−1.0128356770687** (viol. 1.5e-27). LINDO invalid by 4.7e-8 |
| rocket400 | −1.01283634 | COUENNE −1.01283661 | polished CONOPT point **−1.0128365294832** (viol. 1.7e-27). LINDO invalid by 1.9e-7; COUENNE consistent |
| rocket50 | −1.0128171 | SCIP −1.01811726 | CONOPT −1.01281710382. The difference, 3.8e-9, is within the page's 8-digit rounding: inconclusive |
| methanol200 / 400 | 0.00902229 | 0 | 12 random-parameter starts plus 3 targeted starts all give 0.0090222898. No counterexample |
| pinene100 | 19.87217015 | GUROBI 0.042 | CONOPT and IPOPT from the default start give 19.8721701453–19.8721701457. No counterexample |
| popdynm25 | 19752.21542 | 0 | CONOPT and IPOPT give 19752.21541508–19752.21541516. No counterexample |

For the rocket instances, the thrust controls (x_{4N+7}..x_{5N+7}, bounds
[0, 3.5]) are held at CONOPT's values, and Newton's method solves the state
system (1,002 × 1,002 for N = 200). The final residuals are about 2e-51
before rounding to 30 digits.

The rocket discrepancies are small, about 1e-7 relative. They still show that
LINDO's rocket values are local solutions, not bounds. With methanol50, 4 of
the 9 LINDO values examined are not valid bounds.

## 9. What was checked, and caveats

- **Rigorous** (outward-rounded interval arithmetic or exact rationals,
  starting from the exact OSIL decimals):
  - the hvycrash identity and the existence of a feasible point;
  - the ex6_2_5 and ex6_2_7 bounds;
  - the etamac bound;
  - the pricing050 bound;
  - the local concavity result for pindyck.
- **Numerical, not interval-verified:**
  - the existence of exact solutions near the polished methanol50 and rocket
    points (Newton converges to about 1e-50);
  - the optimality of all primal points. Every primal point is a valid
    feasible point; any claim that one is globally optimal comes only from
    the matching bounds.
- **Assumptions:**
  - numpy `+ − × ÷ √` follow IEEE round-to-nearest;
  - mpmath iv's exp, log and cos are correct;
  - Python's `float(str)` is correctly rounded.

  No libm `log` or `exp` result is trusted in the numpy branch and bound.
- **Not checked:**
  - literature or novelty for any instance;
  - whether MINLPLib's gap tolerance would change rocket's "solved" status;
  - the Γ-domain question for quantum, which was out of scope.
- **The scout's claims:**
  - the hvycrash identity: confirmed;
  - "the etamac CES is concave": true only up to a degree excess of 4e-16,
    which the majorant handles;
  - the invalid LINDO bound on methanol50: confirmed, and the same problem
    found on rocket100/200/400.

## 10. Files and commands

All files are in `research-20260929/open-instances-wave2/small/`:

- `ev.py`: 50-digit evaluation of OSIL models and `.sol` points, including
  objective constants.
- `show.py`: readable dump of a model.
- `ia.py`: numpy interval arithmetic, the rigorous `ilog`, and interval
  automatic differentiation.
- `polish.py`: Newton polishing of a point to high-precision feasibility.
- `gdx2sol.py`: converts a GAMS GDX file to `.sol`.
- `hvycrash.py`; `gibbs_model.py` and `gibbs.py`; `etamac.py`;
  `pricing050_model.py` and `pricing050.py`; `pindyck.py`.
- `gms/run_methanol.sh`, `gms/ms.sh`, `gms/solve1.sh`: drivers for the GAMS
  local solves. They need the MINLPLib `.gms` files, which were deleted after
  the runs.
- `sol/`: the downloaded MINLPLib points, plus the extracted CONOPT and IPOPT
  rocket points.
- `logs/`: one log per script; the primal points (`*_primal.txt`,
  `*.polished.txt`, `hvycrash_point.txt`); `gams_runs.log`, a summary of all
  GAMS runs.

Commands run, from that directory (targeted only):

```
python3 ev.py hvycrash.p1 hvycrash.p2 hvycrash.p3 ex6_2_7.p1 ex6_2_5.p1 etamac.p1 pricing050.p1 pindyck.p1
python3 hvycrash.py
python3 gibbs_model.py
python3 gibbs.py ex6_2_7 1e-11          # 1.5 min
python3 gibbs.py ex6_2_5 1e-11          # 10 min
python3 etamac.py                       # 2 min
python3 pricing050.py                   # 1 min
python3 pindyck.py                      # 1 min
python3 ev.py methanol50.p1 methanol50.p2 methanol50.p3 methanol50.p4 methanol200.p1 methanol100.p2
python3 ev.py rocket200.p1 pinene100.p1 popdynm25.p1
python3 polish.py methanol50.p4 x1502 x1503 x1504 x1505 x1506
python3 polish.py rocket{100,200,400}.conopt <thrust variables>
gms/run_methanol.sh ..., gms/ms.sh ..., gms/solve1.sh ...   # GAMS CONOPT/IPOPT, reslim 120–300 s
```

Also run, not part of the results: a test of `ilog` against mpmath; grid and
multistart exploration for pricing050 and pindyck in `/tmp` (not kept); a
first ex6_2_7 run with a first-order-only branch and bound, which was
stopped.

## 11. Independent verification (added by the root, 2026-09-30)

An independent verifier rechecked every claim with its own code
([report](../../reviews/wave2-small-verification/verification-report.md)).
All results hold, with equal or tighter bounds:

| item | verdict | verifier's numbers |
|---|---|---|
| hvycrash | verified | objective −0.2185 at every feasible point; a different exactly feasible point (c_k = 0.417, θ_50 = 4.2) proved feasible in interval arithmetic |
| ex6_2_7 | verified | dual −0.16084761546364904; gap 4.8e-14 to an exactly feasible point |
| ex6_2_5 | verified | dual −70.75207783344770758; gap 2.0e-15 |
| etamac | verified | dual −15.294675643368092; gap 2.6e-15 to an exactly feasible point (this report's primal violates a row by 6e-14) |
| pricing050 | verified | upper bound −1813.8290784519730577; gap 1.0e-17 |
| LINDO bounds | verified, now rigorous | interval Krawczyk existence proofs around the claimed points: feasible values lie below LINDO's listed bounds by 9.8e-5 (methanol50, 1.2%), 1.07e-7, 4.7e-8, 1.9e-7 (rocket100/200/400) |

Qualifications from the verifier:

- The rocket discrepancies (about 1e-7 relative) are below MINLPLib's 1e-6
  "solved" tolerance, and MINLPLib already marks all four instances
  unsolved; the finding is that the listed LINDO values are not valid bounds,
  not that MINLPLib's status is wrong.
- The Gibbs instances ex6_2_5 and ex6_2_7 were very likely solved by an
  ε-global method in the literature (McDonald and Floudas, GLOPEQ, 1997;
  the verifier could not access the handbook to confirm the global
  values), and the
  tangent-plane duality method is known (Mitsos and Barton 2007; interval
  tangent-plane tests by Stadtherr's group). The contribution here is a
  rigorous high-precision closure of these MINLPLib instances, not the
  method. No prior certificate was found for hvycrash, etamac or pricing050
  (brief search).
- Not rechecked: pindyck (no certificate claimed), the "no counterexample"
  statements for rocket50, methanol200/400, pinene100 and popdynm25, and
  whether GAMS/CONOPT reproduces the rocket thrust values (the verifier used
  the authors' values).

*Root edit (2026-09-30, closing revision):* the header now says that the
report is independently verified (Section 11) and points to the pindyck
extension; the pindyck row of the Section 1 table and the heading of
Section 7 point to the extension that supersedes the failure; the Section 11
statement about prior ε-global solutions of ex6_2_5 and ex6_2_7 is
narrowed to what the verifier established.
