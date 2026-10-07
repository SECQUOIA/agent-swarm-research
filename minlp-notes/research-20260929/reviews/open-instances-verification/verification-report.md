# Independent verification of `open-instances/open-instances-report.md`

Date: 2026-09-29. Reviewer: independent verifier (did not produce the results).
Scope: the dual bounds, primal points, and camshape p2 claim for lnts50/100/200/400,
dtoc5, camshape100/200/400/800, optcdeg2, and lukvle10, plus a novelty check.

All computations use my own code in this directory. From the authors' material I
used only the report (for the mathematical argument), their stored numeric data as
inputs where the input only needs to be *some* value (the optcdeg2 multiplier
arrays; the primal vectors and MINLPLib `.sol` files that are being evaluated),
and their numbers for the final comparison. I did not run or import their code.

## 1. Verdicts

| instance | verdict | my rigorous dual bound | my primal (max abs. violation) | report's dual bound |
|---|---|---|---|---|
| lnts50 | verified | 0.5546687649381242 (margin 1e-12); 0.554668764883212 at the report's 1e-10 margin | 0.5546687649386789 (4.7e-15) | 0.554668764883212 |
| lnts100 | verified | 0.5545954011663565; 0.5545954011114516 at 1e-10 | 0.5545954011669111 (6.0e-15) | 0.554595401111452 |
| lnts200 | verified | 0.5545770161025290; 0.5545770160476259 at 1e-10 | 0.5545770161030836 (5.4e-15) | 0.5545770160476259 |
| lnts400 | verified | 0.5545724137001325; 0.5545724136452298 at 1e-10 | 0.5545724137006871 (6.7e-15) | 0.554572413645230 |
| dtoc5 | verified | 5.38967211918114046 | 5.3896721191811405 (1.8e-20) | 5.389672119181134 |
| camshape100 | verified (exact) | −4.2841471217467438034 | the same value, attained by an exactly feasible point | −4.284147121746744 |
| camshape200 | verified (exact) | −4.2785002329927222919 | the same, exactly feasible | −4.278500232992722 |
| camshape400 | verified (exact) | −4.2756884789255432152 | the same, exactly feasible | −4.275688478925543 |
| camshape800 | verified (exact) | −4.2742741419541941011 | the same, exactly feasible | −4.274274141954194 |
| optcdeg2 | verified with caveats | 293.8699938542 (m = 3080); 293.8700386118 (m = 3090) | 293.876075095886 (8.9e-16), the authors' control vector re-simulated | 293.86999385 |
| lukvle10 | verified | 352.2380254050785 (own multipliers, own B&B; gap 1.4e-9) | 352.2380254064961 (3.5e-15; MINLPLib p5) | 352.238025369202 |

The camshape400/800 claim about the MINLPLib p2 points is **verified**. p2 violates
convexity rows by 3.0e-10 and lies 8.15e-6 (n = 400) and 3.27e-5 (n = 800) below the
exact optimum. These points are within MINLPLib's 1e-8 feasibility tolerance, so the
claim concerns exact feasibility only, as the report says.

The novelty framing needs a correction (Section 8). The "MINLPLib dual" column in
the report is the metadata value, which is the bound "reported by at least 3
solvers". The MINLPLib instance pages list tighter single-solver bounds:

- camshape100: ANTIGONE −4.28415233, a gap of only 5.2e-6 (1.2e-6 relative).
- lnts50: GUROBI 0.55464755, a gap of 2.1e-5.
- optcdeg2: GUROBI 292.41713458.

No source I found certifies any of these optima to the report's accuracy, so the
closures are new. For camshape100, however, the improvement over the state of the
art is marginal.

## 2. Method and common checks

- **OSIL reading.** I wrote a new reader, `osilx.py`, which keeps every numeric
  constant as its decimal string. For each instance, the verification script
  compares every row, every bound, and the objective against the expected model by
  exact string equality (`check_structure`/`extract`). No file has `constant`
  attributes on rows or the objective. Default OSiL bounds (lb 0, ub INF) are
  handled; for example, lnts `x205`/`x255` with `ub="0"` are fixed at 0.
- **Hand cross-check.** Before writing the reader, I read rows e2, e102, and e152
  of lnts50, and the variable, objective, and qTerm sections of camshape100, directly
  from the XML.
- **Arithmetic.** Decimal constants are used exactly: as `Fraction` for camshape,
  lnts weights, and the dtoc5 step h = 1/50000, or as mpmath intervals that
  enclose the decimal (`iv.mpf('4e-4')` and similar).
- **Evaluating primal points.** Points are evaluated in 50–60-digit arithmetic, or
  in exact rational arithmetic (camshape). Values missing from a `.sol` file are set
  to 0. This concerned only variables whose bounds allow 0; the bound checks
  confirm it.
- **Targeted commands run** (all from this directory, `OMP_NUM_THREADS=1`):
  - `python3 v_lnts.py 50 100 200 400`
  - `python3 v_dtoc5.py`
  - `python3 v_camshape.py 100 200 400 800`
  - `python3 v_optcdeg2.py`
  - `python3 v_lukvle10_prep.py`
  - `python3 v_lukvle10_bnb.py 8`

  Outputs are in `logs/`. No CI or project-wide checks were run or inspected.

## 3. lnts50/100/200/400 — verified

**Structure.**

- The report's description matches the OSIL row for row:
  - θ at indices 0..N;
  - px, py, vx, vy chains;
  - h at index 5N+5;
  - objective `N·h`;
  - rows `p_{i+1} − p_i − .5·h·(v_i + v_{i+1})` and
    `v_{i+1} − v_i − .5·h·(100 cos/sin θ_i + 100 cos/sin θ_{i+1})`;
  - fixed values px_0 = py_0 = vx_0 = vy_0 = vy_N = 0, py_N = 5, vx_N = 45;
  - h ≥ 0.
- The θ bounds ±1.5707963267949 exceed π/2 by about 3e-15. This is irrelevant,
  because the certificate maximizes over all θ.

**Argument.**

- I checked the summation identities `vx_N = a h Σ w_j cos θ_j`,
  `vy_N = a h Σ w_j sin θ_j`, and `py_N = a h² Σ c_j sin θ_j` in exact rational
  arithmetic, with arbitrary rational values in place of sin and cos. The
  identities are linear in those values.
- The certificate (Section 3.3 of the report) is correct:
  - h = 0 is infeasible;
  - A(h) = 45/(100h) and B(h) = 5/(100h²) are decreasing;
  - with ν ≥ 0, every feasible h satisfies h > h2 whenever
    S(μ,ν) − νB(h2) < A(h2).
- The inequality directions are right for minimization.

**Recomputation.**

- (μ, ν, h*) come from Newton's method in 60 digits on the tangent-law system.
- The inequality is checked in `mpmath.iv` at 50 digits.
- At the report's margin h2 = h*(1 − 1e-10), my interval margins are
  −8.64e-9 (N = 50) to −6.91e-8 (N = 400), and the bounds equal the report's to
  all printed digits.
- A margin of 1e-12 also certifies, with interval margins −8.6e-11 to −6.9e-10.
  This gives the tighter bounds in the table and gaps of about 5.5e-13.

**Primal.**

- My own point (tangent-law controls rounded to double, states by forward
  recursion) and the authors' `lnts_*_primal.txt` vectors both evaluate to
  N·h* = 0.5546687649386789 / 0.5545954011669111 / 0.5545770161030836 /
  0.5545724137006871.
- Max row violation is 4.7e-15 to 6.7e-15 for my point and 5.3e-15 to 1.3e-14 for
  the authors' vectors. The report states 4.6e-15 to 6.9e-15; the difference is
  immaterial.
- MINLPLib lnts50 p1 evaluates to 0.55466876489565 with row violation 9.1e-10.

**Unchecked:** the cvxpy recheck and the SCIP baseline numbers (not needed).

## 4. dtoc5 — verified

**Structure.**

- u_t = x2..x50000 (indices 0..49998); y_t = indices 49999..99998, with y_0 fixed
  at 1 and all other variables free.
- Objective `2e-5 · Σ (u_t² + y_t²)` over u_0..u_{T−1} and y_0..y_{T−1}; y_T is
  absent.
- Rows `−2e-5 u_t + y_t − y_{t+1} + 8e-5 y_t² = 0`, T = 49999.
- 8e-5 = 4h exactly.

**Argument.**

- I re-derived the separable Lagrangian with multipliers λ_t on
  `y_{t+1} − y_t − 4h y_t² + h u_t`.
- The dual function in Section 4.3 of the report is correct. It requires
  λ_{T−1} = 0 (y_T is free and appears only linearly) and 1 − 4λ_t > 0 for
  t = 1..T−1. No condition on λ_0 is needed, because y_0 is fixed.
- No variable bounds are used, so weak duality needs nothing else.

**Recomputation.**

- Own primal: damped Newton on the reduced problem in y (tridiagonal Hessian), then
  three Newton steps in 40-digit mpmath. The final step has size 1e-33.
- λ_t = −2u_t, with λ_{T−1} = 0 set exactly; max λ = 0 < 1/4.
- d(λ) in `mpmath.iv` (30 digits, h = 1/50000 exactly) lies in
  [5.3896721191811404674, 5.3896721191811404675].
- My primal, controls computed from y in 50 digits and rounded, evaluates to
  5.3896721191811405 with max row violation 1.8e-20. The authors' `dtoc5_y.npy`,
  processed the same way, gives the same value.
- So the optimum is 5.38967211918114 to about 16 digits.
- The report's bound, 5.389672119181134, is 6.5e-15 below mine and therefore
  consistent.
- The report remarks that its dual "exceeds the primal by 1.6e-14". That comes from
  computing the controls in double precision. With accurate controls, the primal
  lies above both bounds.

## 5. camshape100/200/400/800 — verified exactly (stronger than claimed)

**Structure.**

- Rows and bounds are exactly as in Section 5.1 of the report. G_1 is row n−2,
  G_n is row n−1, E is row n, and the D_i rows follow. d_1 is free, and
  |d_i| ≤ α for i ≥ 2.
- c2 − 2c = −1.0e-14 for n = 400 and 0 for the other sizes, as the report says.

**Argument.** Each step checks out:

- the division by r_{j−1} r_j r_{j+1} > 0 that gives the rows linear in u = 1/r
  (including G_1 with u_0 = 1);
- the Green's-function representation with Chebyshev U_m(c/2);
- the fact that only rows G_1..G_{n−1} and r_1 ≤ ub_1 are used, so dropping G_n,
  E, and the lower bounds gives a relaxation;
- the min-plus envelope over slope-constrained pairs (2,3)..(n−1,n).

I read the authors' `camshape_bound.py` only to confirm that it excludes the pair
(1,2) (free d_1) in both passes. It does. Including that pair would not change the
numbers anyway.

**Recomputation, in exact rational arithmetic.**

- U_m(c/2) for m ≤ n−1 and S_j are computed with Python `Fraction` from the
  decimal constants. min U_m = 1, and min S_j = 0.3150 / 0.3120 / 0.3105 / 0.3098,
  so all are positive. (nθ/π = 0.39604 / 0.39801 / 0.39900 / 0.39950.)
- The envelope E is computed exactly. Its sum is enclosed in a 400-bit interval of
  width about 1e-118.
- **E is exactly feasible:**
  - every row, bound, and slope constraint holds in exact rational arithmetic, with
    63/127/255/512 convexity rows active (slack exactly 0);
  - its objective equals the bound exactly.
- So the optimum of each instance is exactly −c0·ΣE_j, not merely within 1e-15.
- My bounds agree with the report's to all 16 printed digits.
- The authors' `camshape*_envelope.npy` differ from my E by at most 1.1e-16.

**MINLPLib points** (exact evaluation of the decimal `.sol` values):

| n | point | objective | max violation | objective − optimum |
|---|---|---|---|---|
| 100 | p1 | −4.28414712174672 | 1.95e-14 | +2.4e-14 |
| 200 | p1 | −4.278500232993864 | 1.84e-14 | −1.14e-12 |
| 400 | p1 | −4.275688478934241 | 2.53e-14 | −8.7e-12 |
| 400 | p2 | −4.275696633420248 | 3.0e-10 | **−8.15e-6** |
| 800 | p1 | −4.274274141954209 | 3.91e-10 | −1.5e-14 |
| 800 | p2 | −4.27430686622631 | 3.0e-10 | **−3.27e-5** |

The p2 claim is confirmed. The p1 points of n = 200/400 also lie slightly below
the exact optimum (by 1e-12 and 9e-12). This is consistent with their 2e-14
violations and the ill-conditioning described in Section 5.5 of the report
(amplification 1/sin θ ≈ 80 to 640). The report's table shows these numbers but
does not comment on them.

**Unchecked:** the SCIP camshape100 incumbent claims, the SLSQP/LP rechecks, and
the cell-DP experiment (Section 8.1 of the report).

## 6. optcdeg2 — verified with caveats

**Structure.**

- N = 50000.
- Rows `y_{t+1} − y_t − 4e-4 v_t = 0` and
  `v_{t+1} − v_t − 4e-4 u_t + 8e-6 y_t + 8e-5 v_t² = 0`.
- Objective `2e-4 Σ_{t=0}^{N} y_t²`.
- Variable layout:
  - u_{N−1} = x50002;
  - v_N = x50001, fixed at 0;
  - v_0 fixed at 0;
  - v_1..v_{N−1} ≥ −1;
  - |u| ≤ .2;
  - y_0 = 10, other y free.
- The coefficients match h·0.02 = 8e-6 and h·0.2 = 8e-5. My code uses the decimal
  file constants directly.

**Argument.**

- I re-derived the Lagrangian L = f + Σ μ_t Y_t + Σ λ_t V_t. Its terms are:
  - y-terms: `2e-4 y² + (μ_{t−1} − μ_t + 8e-6 λ_t) y`;
  - u-terms: `−0.2·4e-4 |λ_t|`;
  - v-terms: `8e-5 λ_t v² + (λ_{t−1} − λ_t − 4e-4 μ_t) v`;
  - terminal: `2e-4 y_N² + μ_{N−1} y_N`.
- The head-block function Φ in Section 6.4 of the report is correct.
- The monotonicity argument is sound:
  - ∂J/∂u_k = 4e-4 · p_v(k+1);
  - the adjoint recursion is p_y(k) = 2·2e-4·y_k + p_y(k+1) − 8e-6 p_v(k+1) and
    p_v(k) = 4e-4 p_y(k+1) + (1 − 2·8e-5 v_k) p_v(k+1);
  - it is enclosed over forward-reachable intervals for the whole control box,
    without the v ≥ −1 intersection (correct, because the head minimum is taken
    over the whole box);
  - positivity of all p_v(k), k = 1..m, gives coordinatewise monotonicity along
    segments inside the box, so min J = J(−0.2, …, −0.2).
- State bounds for the rest terms use feasibility (v ≥ −1, v_N = 0), which is
  valid because those bounds apply only to feasible points.
- The g⁻¹ branch choice is valid because the forward bounds give v < 1.22 ≪ 6250.
  I used the cancellation-free form g⁻¹(w) = 2w/(1 + √(1 − 4·8e-5·w)).

**Recomputation** (own code, `mpmath.iv` at 100 bits):

- Multipliers: the authors' `optcdeg2_lam.npy` and `optcdeg2_mu.npy`, used as
  certificate data. Any multipliers give a valid bound.
- My forward/backward state bounds agree with the authors' stored bounds to
  1.1e-16.
- Full Lagrangian: **293.2500703422**, versus 293.2500703421716 in the report.
- Head block:

| m | monotone | min lower p_v | bound |
|---|---|---|---|
| 2800 | yes | 10.80 | 293.8412914624 |
| 3000 | yes | 3.371 | 293.8669756077 |
| 3080 | yes | 0.4477 | **293.8699938542** |
| 3090 | yes | 0.0843 | 293.8700386118 |
| 3100 | no | −0.279 | — |

  At m = 3080 this matches the report's mpmath recheck, 293.8699938542215, and is
  within 4e-9 of its `ivnp` value, 293.8699938501. m = 3090 also passes and gains
  4.5e-5; this is immaterial.

**Primal.**

- The authors' control vector `optcdeg2_primal_u.npy`, re-simulated in 40 digits
  with states rounded to double, gives objective 293.876075095886.
- Max row violation is 8.9e-16 (row e8900); the simulated v_N is −2.8e-16.
- There is one formal bound violation of 1.1e-17: the double 0.2 exceeds the
  decimal `.2`. The report says "no bound violation".
- MINLPLib p1: 293.876075102017, violation 1.25e-14.
- **Gap: 6.08e-3 absolute, 2.07e-5 relative, as claimed.**

**MINLPLib p2** (downloaded, evaluated, then deleted): objective 292.417134583025.
It violates 46,687 rows by more than 1e-8, with a maximum of 9.97e-7. Its value
equals GUROBI's listed dual bound, 292.41713458, which suggests that bound holds
only up to a 1e-6 feasibility tolerance.

**Caveats.**

- I used the authors' multipliers rather than computing my own adjoint. This does
  not affect validity.
- My implementation follows the method described in the report (forward/backward
  state propagation, natural interval adjoint), so it independently checks the
  arithmetic and code, not an alternative method.
- The primal was not re-optimized; I did not rescan the first switch.
- The failed block-DP and dual-optimization experiments were not checked.

## 7. lukvle10 — verified

**Structure.**

- 1000 free variables.
- Objective `Σ_{i<500} (x_{2i}²)^(x_{2i+1}²+1) + (x_{2i+1}²)^(x_{2i}²+1)`.
- Rows `−x_j + 3x_{j+1} − 2x_{j+2} − 2x_{j+1}² = −1`, j = 0..997.
- This matches Section 7.1 of the report. I also confirmed the dynamics claims:
  - fixed points ±1/√2;
  - at −1/√2, a saddle with eigenvalues 2.731 and 0.183;
  - at +1/√2, an attracting focus with |λ| = √0.5;
  - Jacobian determinant 1/2.

**Argument.**

- Partial Lagrangian with rows j < 994 dualized:
  - β_k = −λ_k + 3λ_{k−1} − 2λ_{k−2} and q_k = −2λ_{k−1};
  - for the tail entry: β_994 = 3λ_993 − 2λ_992, q_994 = −2λ_993,
    β_995 = −2λ_993, q_995 = 0;
  - x_996..x_999 carry no Lagrangian terms;
  - the constant is Σ_{j<994} λ_j.
- The kept rows 994–997 determine x_996..x_999 from (x_994, x_995), as the report
  says.
- The coercivity bound f(a,b) ≥ φ(a) + φ(b) is correct (base ≥ 1 and exponent
  ≥ 1 give (a²)^(b²+1) ≥ a²). It needs every q_k > −1; I checked min q = −0.8156.
- Dropping f(P s) ≥ 0 and f(P² s) ≥ 0 for the tail's box reduction is valid.

**Recomputation, all my own.**

- Multipliers:
  - least squares on the KKT system at MINLPLib p5, residual 4.6e-14 (same as the
    report);
  - entries j = 30..960, which agree to 2.4e-14, are replaced by the double
    λ_495 = 0.4077978179563417;
  - this gives 464 identical middle pairs (i = 16..479) and 34 distinct groups, as
    in the report.
- Box radii: my own coercivity bound, checked in intervals.
- Branch and bound (`v_lukvle10_bnb.py`):
  - best-first 2-D interval branch and bound in `mpmath.iv` (64-bit);
  - the power terms use an exact monotone range formula for base^e over
    base ≥ 0, e ≥ 1;
  - box bound: the maximum of the natural bound and a mean-value form with an
    interval gradient. For the tail, the gradient is computed by forward-mode
    differentiation through P and P²;
  - tolerance 1e-12 for pair problems and 1e-9 for the tail.
- Results:
  - pair groups: largest UB − LB is 1.0e-12; 2255–9471 boxes each;
  - middle group: LB −0.10848885472697, UB −0.10848885472614. The report's LB,
    −0.10848885473598, is looser but consistent;
  - tail: LB 1.1740123815543, UB 1.1740123825517 (92551 boxes). The report has
    LB 1.1740123815526 and UB 1.1740123825517;
  - Σλ = 405.03299763692109;
  - **rigorous dual bound 352.2380254050785**. The sum of the upper ends is
    352.2380254064956.
- Primal: MINLPLib p5 evaluates to 352.2380254064961 (violation 3.5e-15) and p1 to
  353.1224549165 (violation 1.1e-9).
- The remaining gap, 1.42e-9, equals the sum of my tolerances. This confirms the
  report's conclusion that the partial Lagrangian has no duality gap at these
  multipliers. The report's bound, 352.238025369202, is 3.6e-8 below mine and
  therefore consistent.
- Float sanity check (`v_lukvle10_sanity.py`, not a proof): 1201² grid sampling
  plus Nelder–Mead on each of the 35 problems. No value falls below its certified
  LB; the smallest margin is 8.4e-13.

**Caveats.**

- Rigor rests on mpmath's interval `exp`/`log`, the same library the authors use.
  My code is independent, but the library is a shared dependency.
- The primal is MINLPLib's p5. Like the authors, I did not compute a separate
  lukvle10 point.
- The full-Lagrangian estimate 352.152 in the report was not rechecked.

## 8. Novelty and status

**MINLPLib status.** I fetched the instance pages at
https://www.minlplib.org/<name>.html on 2026-09-29 (site "Last updated
2026-09-14, git 9472b011"). All 11 instances are open. Best single-solver dual
bounds listed:

| instance | best listed dual (solver) | listed primal | comment |
|---|---|---|---|
| lnts50 | 0.55464755 (GUROBI) | 0.55466876 | gap 2.1e-5; metadata uses 0.5258 |
| lnts100 | 0.55299042 (GUROBI) | 0.5545954 | |
| lnts200 | 0.55219867 (GUROBI) | 0.55457702 | |
| lnts400 | 0.55204395 (GUROBI) | 0.55457241 | |
| dtoc5 | 0.00243096 (BARON) | 5.38967212 | |
| camshape100 | **−4.28415233 (ANTIGONE)** | −4.28414712 | gap 5.2e-6 (1.2e-6 rel.) already |
| camshape200 | −4.63229055 (ANTIGONE) | −4.27850023 | |
| camshape400 | −4.97265746 (ANTIGONE) | −4.27569663 (p2) | |
| camshape800 | −5.12584096 (GUROBI) | −4.27430687 (p2) | |
| optcdeg2 | 292.41713458 (GUROBI) | 293.8760751 | equals the value of p2 (infeas. 1e-6) |
| lukvle10 | 351.223393 (SCIP) | 352.2380254 | |

**What this means for the report's framing.**

- The report's "MINLPLib dual" column and phrases such as "gap reduced from 98.5%"
  (optcdeg2) use the 3-solver metadata value. Measured against the best listed
  bound:
  - optcdeg2's starting gap was 0.50%;
  - lnts50's was 3.8e-5 relative;
  - camshape100's was 1.2e-6 relative.
- The new bounds still close or shrink every gap. For camshape100 the improvement
  is marginal.

**Consequence for MINLPLib.** The report's camshape400/800 bounds lie *above*
MINLPLib's listed primal values (the p2 points, accepted at MINLPLib's 1e-8
tolerance). Submitted as they are, they would look inconsistent with MINLPLib
unless the exact-versus-tolerance distinction is stated.

**Literature.** No certificate of global optimality was found for any of the 11
instances. Sources checked (partly by a delegated search, spot-checked by me):

- MINLPLib pages for all 11 instances, fetched by me with `curl`, plus
  `instances.html` and `bounddates.html`, which the delegated search reported on;
- COPS 2.0 (ANL/MCS-246, optimization-online 2000/11/237) and COPS 3.0
  (ANL/MCS-TM-273, mcs.anl.gov/~more/cops/cops3.pdf): camshape and lnts reference
  values from local solvers only, with no global claim;
- CUTEst SIF files DTOC5, OPTCDEG2, LUKVLE10 (bitbucket optrove/sif): local SOLTN
  values for other sizes;
- QPLIB 8585 and 8803 pages: solution values only;
- Mittelmann's MINLP benchmark (plato.asu.edu/ftp/minlp.html): camshape100 is
  unsolved by all solvers after 2 h (reported by the delegated search, not
  re-checked by me);
- GAMS model library pages for camshape and lnts;
- web searches for global optimality or solved status of camshape, lnts, dtoc5,
  optcdeg2, and lukvle10, 2024–2026: nothing found.

The continuous-time lnts problem has the analytic linear-tangent solution
(Bryson & Ho). That is consistent with the discrete optima but does not certify
them.

## 9. Summary of discrepancies found

1. **None affecting validity.** Every bound I recomputed is valid, and every
   reported number agrees with mine to the stated precision. For lukvle10 I
   certify a tighter bound (gap 1.4e-9 instead of 3.7e-8).
2. **Novelty framing** (Section 8). The "MINLPLib dual" column is the 3-solver
   metadata value. Tighter single-solver bounds exist on the instance pages,
   notably camshape100 (ANTIGONE, 1.2e-6 relative gap), lnts50 (GUROBI), and
   optcdeg2 (GUROBI 292.417, tolerance-feasible).
3. **Minor inaccuracies in the report.**
   - dtoc5: "dual exceeds primal by 1.6e-14" is an artifact of computing the
     controls in double precision.
   - optcdeg2: the primal violates the `.2` bounds by 1.1e-17 (float 0.2 > 0.2).
   - camshape200/400: the p1 points lie 1e-12 and 9e-12 below the exact optimum;
     not remarked on.
   - optcdeg2: the head check also passes at m = 3090.
4. **Stronger statement available for camshape.** The envelope is exactly
   feasible, so the reported bounds are the exact optima, not only closed to 1e-15.

## 10. Files

- `osilx.py`: own OSIL reader and evaluator (decimal strings kept).
- `v_lnts.py`, `v_dtoc5.py`, `v_camshape.py`, `v_optcdeg2.py`,
  `v_lukvle10_prep.py`, `v_lukvle10_bnb.py`: per-family verification.
- `logs/*.json`, `logs/*.log`: outputs. `logs/lukvle10_lam_kkt.npy` and
  `logs/lukvle10_x5.npy` hold my KKT multipliers and the p5 point.
