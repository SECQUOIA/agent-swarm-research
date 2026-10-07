# Independent verification: wave 2, small instances

Date: 2026-09-30. Reviewer: independent verifier (did not produce the results).
Claims under review: `open-instances-wave2/small/report.md` (the "report").
All code and logs for this review are in
`reviews/wave2-small-verification/`. I read the authors' code only after my own
numbers existed, to compare parameters (Section 8). I did not edit anything
under `open-instances-wave2/small/`, did not commit, and did not inspect CI.

## 1. Verdicts

| item | verdict | my rigorous numbers | report's numbers |
|---|---|---|---|
| 1. hvycrash | **verified** | objective ≡ −0.2185 on the feasible set; own exactly feasible point (c_k = 0.417, θ_50 = 4.2) | same identity; different point (c_k = 0.08, θ_50 = 3) |
| 2a. ex6_2_7 | **verified** (my bound is tighter) | dual bound −0.16084761546364904; own exact primal −0.16084761546360086; gap 4.8e-14 | −0.16084761549352554; gap 3.0e-11 |
| 2b. ex6_2_5 | **verified** (my bound is tighter) | dual bound −70.75207783344770758; own exact primal −70.75207783344770558; gap 2.0e-15 | −70.752077836333563; gap 2.9e-9 |
| 3. etamac | **verified** | dual bound −15.294675643368092; own **exactly** feasible primal −15.2946756433680896; gap 2.6e-15 | −15.294675643368096; primal has row violation 6.0e-14 |
| 4. pricing050 (max) | **verified** (my bound is tighter) | upper bound −1813.8290784519730577; own exact primal −1813.8290784519730578; gap 1.0e-17 | −1813.8290784519704; gap 2.7e-12 |
| 5. LINDO invalid (methanol50, rocket100/200/400) | **verified, now rigorous** (caveat on the size of the rocket violations, Section 6) | Krawczyk test proves an exactly feasible point with objective below LINDO's value for all four | numerical Newton polishing only |
| 6. status / novelty | **verified with caveats** | all five instances are not marked solved; prior literature exists for the Gibbs problems (Section 7) | report did not check literature |

"Rigorous" below means outward-rounded interval arithmetic (mpmath `iv`) or
exact rationals, starting from the exact OSIL decimals. Assumptions: mpmath
`iv` encloses `exp`, `log`, `cos`, `sqrt` correctly; for the Krawczyk tests,
numpy/BLAS double arithmetic is IEEE (the error bounds used hold for any
summation order, with or without FMA).

**OSIL reader.** I used `reviews/open-instances-verification/osilx.py` for
parsing only. It keeps decimals as strings, records `<obj constant=...>`, and
`ev_row` adds row constants. My `common.obj_value` adds the objective constant.
Among the nine instances only methanol50 has a constant: the file value is
`5.016256589999999` (the report writes 5.01625659; the 1e-15 difference is
immaterial). No row constants occur.

## 2. hvycrash (item 1): verified

Structure (`v_hvycrash.py`): all 150 rows match exact expression-tree
templates, and all 201 variables are accounted for. There are 50 stages
(θ_0 = x101, θ_50 = x50), and the objective is x152 = s_50. The acc and alg rows
use the identical D_k tree.

- **Identity.** alg_k reads −1/r − cos θ/(D r³) = 0. It is defined only for
  r ≠ 0. Multiplying by −r gives cos θ/(D r²) = −1, so every acc increment is
  exactly −4.37e-3. Hence x152 = −437/2000 = −0.2185 at every exactly
  feasible point.
- **Own feasible point** (different from the authors'). Set c_k = 0.417 and
  θ_50 = 4.2. Then define r_k = √(−cos θ_k/D_k) and
  θ_{k−1} = θ_k − 10(A_k − B_k), where A_k and B_k are the two dyn_k terms.
  The rows hold as real-number identities. Interval arithmetic (60 digits)
  proves:
  - cos θ_k ≤ −0.490 for every k;
  - every θ_k lies in [2.1653, 4.2], inside the bounds [0, 6.2831854];
  - r_k ∈ [2.21, 3.15];
  - the objective enclosure contains −0.2185, with width 5e-60.

  A 60-digit decimal version has objective −0.2185 and maximum row violation
  3.1e-60.
- **MINLPLib points** (my evaluation): the objectives and violations for p1, p2
  and p3 match the report's table, including r_50 = 2.47e7 and 1.58e9 for p1
  and p2, and max|cos/(Dr²) + 1| = 8.8e-13 for p3.
- **Tolerance remark.** I re-derived the report's bound −0.2185(1 + 7.86τ) − 50τ
  by hand and found it correct.
- **Not checked:** nothing material.

## 3. ex6_2_7 and ex6_2_5 (item 2): verified, with tighter bounds

**Structure** (`gibbs_sym.py`; sympy with exact rationals):

- The rows are Σ_p n_{p,i} = b_i, and the bounds are [1e-7, b_i].
- Every objective term uses one phase only.
- ex6_2_7 has three phases that are identical after renaming (26 terms each).
- ex6_2_5 has two identical 29-term liquid phases plus the ideal phase
  Σ n_i(ln(n_i/Σn) + 0.156969560191053).

**Scaling identity.** I derived R_p = t·d/dt[G_p(ty)/t] symbolically, checked
that it does not depend on t and is linear, and then checked
G_p(ty) − tG_p(y) − t ln t R_p(y) ≡ 0 symbolically. The results:

- ex6_2_7: R_p = (0, 0, 1/20000000000000), that is, 5e-14 on n3;
- ex6_2_5: R_p = 0.

Both match the report.

**Own multipliers** (`gibbs_kkt.py`; a different method from the authors'
multistart SLSQP):

1. Solve a tangent-plane LP on a simplex grid of 188k (ex6_2_7) and 376k
   (ex6_2_5) points: maximize λ·b subject to λ·y ≤ G(y) at each grid point.
2. Seed from the active points.
3. Refine with a 60-digit Newton solve of the 12×12 KKT system (residual below
   1e-59).

The LP finds the same three-phase splits as the report directly: ex6_2_7 at
t = 0.198, 0.485 and 0.317; ex6_2_5 at liquid t = 15.92 and 60.73 and ideal
t = 23.35. I used λ rounded to 20 digits. It agrees with the report's λ to all
11 printed digits.

**Own tangent-plane minimization** (`gibbs_bb.py`, a 2-D interval branch and
bound in mpmath `iv`). It differs from the authors' method in the arithmetic
(mpmath instead of numpy with `ilog`), the coordinates, the splitting rule and
the second-order rule:

- coordinates (y1, y2), with y3 clipped per box;
- lower bounds from the natural extension, the mean-value form, and an exact
  2×2 quadratic bound D(c) − ½ gᵀQ⁻¹g that uses the interval Hessian entries,
  not λ_min;
- geometric splitting in dilute coordinates;
- ymin = 0.99·1e-7/tmax, a superset of the feasible compositions.

For the ideal phase I used an exact argument instead of branch and bound:
min over the simplex of Σ y_i ln y_i − Σ y_i(λ_i − c) = −ln Σ exp(λ_i − c).
The result is +7.0e-22.

Results (`logs/*_bb_*.json`, `logs/*_bound.json`):

| | ex6_2_7 | ex6_2_5 |
|---|---|---|
| certified min of D | ≥ −6e-15 (42,111 boxes, 50 s, 6 processes) | liquid ≥ −1e-17 (131,111 boxes, 200 s, 8 processes); ideal ≥ +7.0e-22 |
| λ·b | −0.16084761546357586 | −70.75207783344770558 |
| **dual bound** λ·b + Σ_p[min(0, tmax·m_p) − max R_p/e] | **−0.16084761546364904** | **−70.75207783344770758** |
| own primal (phases 0 and 1 from KKT to 20 digits, phase 2 = b − others, exact rationals; objective enclosed) | −0.16084761546360086 | −70.75207783344770558 |
| gap | 4.8e-14 | 2.0e-15 |

Remarks:

- **The ex6_2_7 floor is real.** A run with τ = 1e-17 failed, as it should.
  With R ≠ 0, the tangent-plane function at the KKT phase with t = 0.485 equals
  −(1 + ln t)R(y) ≈ −4.2e-15, so no certificate can reach much below −4e-15
  there.
- **Sanity checks** (`gibbs_sanity.py`, not part of the proof):
  - on 300 random boxes, the certified bound never exceeded D at sampled
    points;
  - with λ_1 perturbed by 1e-3, the branch and bound fails, as expected.
- **Both report bounds are valid and lie below mine.** The MINLPLib p1 values
  match: −0.1608476154636001 and −70.7520778334477.
- **Not checked:** I did not re-run the authors' branch and bound.

## 4. etamac (item 3): verified

`v_etamac.py`:

- **Structure.** All 70 rows, 97 bounds and the objective match templates
  built from an explicit role map (K, KN, Y, YN, L, LN, E, EN, C, I, EC).
  β_t, a_t, c_L and c_E are all > 0.
- **Exponents** (exact rationals): p1·q = 0.27999999999999975 < 1, and
  s = (p2 + p3)q = 1 + 4.14e-16 > 1. So LN^{p2 q}EN^{p3 q} is not concave with
  the file's decimals, and the report's point about this is correct.
- **Relaxation validity.**
  - Changing YN_t = CES_t to YN_t ≤ CES~_t, and e43 to
    Y_1 − CES~_1 ≤ 3.4653339648, is a relaxation whenever CES ≤ CES~ at
    etamac-feasible points.
  - CES~ = M(u, κw) with w = LN^{p2/(p2+p3)}EN^{p3/(p2+p3)} (degree exactly 1,
    concave). M is a power mean with negative exponent, so it is concave and
    nondecreasing, and CES~ is concave.
  - CES = M(u, w^s) ≤ M(u, κw) holds whenever w ≤ W and κ ≥ W^{s−1}.
- **Box.** I derived the box from etamac's own rows, not from the relaxation,
  so it does not depend on κ:
  - Y_1 ≤ 3.4653339648 + c0^{−q};
  - I_t ≤ Y_t − C_lb − EC_lb, which gives KN_{t+1};
  - YN ≤ a^{−q}KN^{p1 q};
  - a forward recursion for Y, then bounds on C, EC, L, E, LN, EN and K.

  Results: largest upper bound 2062.83 (E_9, x61); Y_9 ≤ 26.73; Y_1 ≤ 4.959.
  These match the report.
- **Majorant constant.** My W = 1015.6 is the geometric-mean bound. The
  authors' W = 2022.06 is max(LN_ub, EN_ub), which is cruder but also valid.
  I get W^{s−1} ≤ 1 + 2.87e-15 and use κ = 1.000000000000004.
- **Bound.**
  - I solved the KKT system of the relaxation R itself: SLSQP start, then
    50-digit Newton, residual 2.7e-48.
  - Multipliers: min μ = 0.278 and μ70 = 0.363, the same as the report. No
    free variable is within 0.047 of a bound.
  - l is convex on the box, so l(x̂) + Σ_j min over the box of
    ∂_j l(x̂)(x_j − x̂_j) is a lower bound. The largest free gradient is
    4.9e-31, and ∂l/∂K_1 = 0.00496 multiplies a zero-width range.
  - **Dual bound: −15.294675643368092.** The report's −15.294675643368096 is
    valid and lies slightly below mine. The reason is that the authors took
    the KKT of the unrelaxed model, so their gradient is 1.1e-16.
- **Primal (improvement over the report).**
  - The report's primal has row violation 6.0e-14, so its "gap 6.6e-15"
    compares the bound with an inexact point.
  - I built an exactly feasible point. I fixed I_1..I_8, LN_t and EN_t at
    25-digit decimals and defined all other variables by the exact
    real-number recursions of the linear and CES rows, with I_9 := 0.07 K_9
    (so e70 is active).
  - Interval arithmetic confirms every bound with a margin of at least 0.047.
    The objective lies in [−15.29467564336808959198, same + 4e-45].
  - **Gap 2.6e-15.**
- **MINLPLib p1:** −15.2946756434628, violation 1.33e-10. This matches the
  report.

## 5. pricing050 (item 4): verified, with a tighter bound

`v_pricing050.py`:

- **Structure.** Template matching confirms that every term has the form
  a_ij x_j exp(g_ij x_j^p) with a < 0, g < 0 and p ∈ {1, 2, 3}, and that
  c_j ≥ 0. Row e5 lacks x21.
- **Own multipliers.**
  1. Nelder–Mead on the concave dual, with a 20,001-point grid for each min F_j.
  2. 50-digit refinement: solve rows e5 and e6 at the Lagrangian minimizers.

  Result: μ_e5 = 3.0489011208166370021 and μ_e6 = 2.1677509642745686136.
  The other multipliers are 0. This matches the report.
- **Own certified 1-D minima.** This method differs from the authors'
  natural/mean-value branch and bound: I used a monotonicity partition in
  mpmath `iv`. Each piece of [0, 10] is certified in one of four ways:
  - F′ > 0: the minimum is at the left end;
  - F′ < 0: the minimum is at the right end;
  - F″ < 0: the minimum is at one of the ends;
  - F″ > 0 on a piece of width below 1e-7: an exact quadratic bound.

  This used 2,406 pieces in total. The sum of the certified minima differs from
  the sum of F at the computed minimizers by only 7e-22.
- **Upper bound: −1813.8290784519730577.** The report's
  −1813.8290784519704 is valid and lies slightly above mine.
- **Own primal.** The KKT minimizers, rounded to 25 digits, are already exactly
  feasible: interval row slack ≥ 1.1e-18. The objective is
  −1813.8290784519730578, so the **gap is 1.0e-17**.
- **MINLPLib p1:** −1813.82907844984, violation 7.3e-10. This matches the
  report.

## 6. LINDO invalidity (item 5): verified rigorously

**Listed values.** The instance pages, fetched 2026-09-30, confirm LINDO's dual
bounds:

- methanol50: 0.00802826;
- rocket100: −1.0128319;
- rocket200: −1.01283563;
- rocket400: −1.01283634.

**Method** (`krawczyk.py`, `v_lindo.py`).

- Existence test: a midpoint–radius Krawczyk test on a square subsystem.
  - F(x̃) and J(X) are enclosed by interval forward-mode automatic
    differentiation at 40 digits, with outward conversion to doubles.
  - R = inv(Jc) in double.
  - The test is |RFc| + |R|Fr + |I − RJc|r + |R|Jr·r < r, with rigorous
    floating-point error bounds (γ_n) and a safety factor.
- After the test, I check all variable bounds on the whole box X and enclose
  the objective, including its constant, over X.
- **methanol50.**
  - Parameters x1502–x1506 are fixed at MINLPLib p4's decimals (the same values
    the authors held), and the three fixed initial values stay fixed.
  - The unknowns are the 1497 free, unbounded variables; the rows are all 1497
    rows.
  - Start: MINLPLib p4, with my own double-precision Newton polish.
- **rocketN.**
  - T is fixed at the authors' CONOPT values, taken from their polished files.
  - The mass rows are then linear in (step, m), so I computed step and
    m_1..m_{N−1} in exact rationals. All N mass rows hold exactly, and
    0.6 ≤ m_i ≤ 1 holds exactly; some masses equal 0.6 exactly.
  - D_0 = 0 and g_0 = 1 are exact.
  - The unknowns are v, h, g and D for i = 1..N (4N of them).

Results (radius r = 1e-12·max(1, |x̃|)):

| instance | n | Krawczyk β/r (max) | bounds on X | objective enclosure | LINDO | margin below LINDO |
|---|---|---|---|---|---|---|
| methanol50 | 1497 | 1.1e-4 | no finite bounds on unknowns | [0.00793021868, 0.00793021891] | 0.00802826 | 9.8e-5 (1.2%) |
| rocket100 | 400 | 1.1e-4 | ok (min margin 1.3e-9, D_N) | [−1.0128320069151, −1.0128320069130] | −1.0128319 | 1.07e-7 |
| rocket200 | 800 | 1.1e-4 | ok (min margin 2.0e-10, D_N) | [−1.0128356770698, −1.0128356770677] | −1.01283563 | 4.7e-8 |
| rocket400 | 1600 | 1.1e-4 | ok (min margin 6.4e-10, D_N) | [−1.0128365294842, −1.0128365294822] | −1.01283634 | 1.9e-7 |

Findings:

- **Each enclosure contains the report's value:** 0.0079302187922673,
  −1.0128320069141, −1.0128356770687 and −1.0128365294832.
- **Negative controls behave as expected** (`krawczyk_sanity.py`). A centre
  moved off the solution by 1e-8 fails with r = 1e-12 and passes with r = 1e-6.
- **Caveat on the rocket bounds.**
  - LINDO's rocket values are invalid as bounds, but only by about 1e-7
    relative. That is below the 1e-6 relative gap that MINLPLib uses for its
    "solved" status.
  - The rocket violations also survive rounding of the displayed values: the
    listed 8–9 significant digits allow at most ±5e-8 (rocket100) and ±5e-9
    (rocket200/400).
  - MINLPLib already treats all four instances as unsolved (Section 7), so the
    findings do not change any listed status. methanol50's 1.2% violation is
    large, and the page itself already lists p4 = 0.00793022 below LINDO's
    value.
- **Not checked:** the "no counterexample" claims for rocket50,
  methanol200/400, pinene100 and popdynm25; pindyck (Section 7 of the
  report); and whether GAMS/CONOPT reproduces the T values. I used the
  authors' T values; the proof does not depend on how they were obtained.

## 7. Status and novelty (item 6): verified with caveats

**Status.** From `instances.html`, the instance pages and `minlplib.solu`
(Last-Modified 2026-09-14), fetched 2026-09-30:

- None of hvycrash, ex6_2_7, ex6_2_5, etamac and pricing050 has the "solved"
  mark (column S). The .solu file lists `=best=`, not `=opt=`, for each.
- The same holds for methanol50 and rocket100/200/400: LINDO's single claim is
  not enough, because "solved" needs three solvers.

Best listed bounds (instance pages):

| instance | primal | best single-solver dual | .solu `=bestdual=` (third-best) |
|---|---|---|---|
| hvycrash | −0.2185 (p3) | −218500000 (SCIP, the only one) | none |
| ex6_2_7 | −0.16084762 | −1.06726714 (BARON) | −1.354737094 |
| ex6_2_5 | −70.75207783 | −111.4201713 (BARON) | −364.1162233 |
| etamac | −15.29467564 | −15.40567054 (SCIP) | −16.3990195 |
| pricing050 (max) | −1813.829078 | −1534.3281 (SCIP) | −1153.003281 |

The report's "best listed dual" is the best single-solver value. MINLPLib's own
`=bestdual=` is the third-best value, which is weaker.

**Novelty** (brief search only; see sources):

- **ex6_2_5 and ex6_2_7.** Prior global work exists.
  - The instances come from the Floudas et al. handbook (1999). The pages cite
    McDonald & Floudas, "GLOPEQ" (Comput. Chem. Eng. 21, 1997), a
    deterministic ε-global method (αBB/GOP) for these phase-equilibrium
    problems. I could not access the handbook text to confirm the global
    values it reports.
  - The Lagrangian-dual form of Gibbs minimization is the "dual extremum
    principle" of Mitsos & Barton (AIChE J. 2007).
  - Rigorous interval tangent-plane stability tests for excess-Gibbs models are
    established work (Stadtherr, Brennecke and coworkers, 1995–2000s).
  - So the method is not new, and the phase splits were very likely known to be
    ε-global. What appears new is a rigorous certificate closing these
    MINLPLib instances.
- **etamac.** The concavity of ETA-MACRO's CES production function is standard.
  The 4e-16 degree excess is an artifact of the file's decimals. I found no
  prior certificate.
- **pricing050.** Davarnia (Oper. Res. Lett. 2021, decision diagrams) reports
  gap closure on pricing instances, not optimality. I found no certificate.
- **hvycrash.** I found no prior discussion. The identity is elementary.

Sources:
- [MINLPLib ex6_2_7](https://www.minlplib.org/ex6_2_7.html)
- [MINLPLib ex6_2_5](https://www.minlplib.org/ex6_2_5.html)
- [GLOPEQ (MaRDI portal)](https://portal.mardi4nfdi.de/wiki/GLOPEQ)
- [Mitsos & Barton, A dual extremum principle in thermodynamics](https://yoric.mit.edu/?p=458)
- [Stadtherr group, reliable phase stability with interval analysis](https://www3.nd.edu/~markst/zm97a.pdf)
- [Davarnia, Strong relaxations for continuous NLPs based on decision diagrams](https://optimization-online.org/2020/03/7681/)

## 8. Comparison with the authors' code (read after my runs)

- The multipliers agree to all printed digits: Gibbs λ, etamac μ, and pricing
  μ.
- The etamac W differs: the authors use max(LN_ub, EN_ub) = 2022.06, I use
  the geometric-mean bound 1015.6. Both are valid.
- The authors' ex6_2_7 ymin (9.999999999999998e-08 < 1e-7) is safe.
- **No discrepancies that affect validity.** In every case my rigorous bound
  equals or improves the report's bound, and every report primal value lies
  inside or next to my enclosures.
- **One wording issue.** The report's etamac "gap 6.6e-15" is measured against
  a point with row violation 6e-14. With my exactly feasible point the claim
  holds anyway, and the gap is 2.6e-15.

## 9. Files and commands (targeted only; no project-wide checks, no CI)

Files, all in `reviews/wave2-small-verification/`:

- `common.py`: shared parsing and evaluation helpers.
- `ivgen.py`: compiles sympy expressions to mpmath `iv` functions.
- `v_hvycrash.py`
- `gibbs_sym.py`, `gibbs_kkt.py`, `gibbs_bb.py`, `gibbs_bound.py`,
  `gibbs_sanity.py`
- `v_etamac.py`
- `v_pricing050.py`
- `krawczyk.py`, `v_lindo.py`, `krawczyk_sanity.py`
- `logs/`: JSON results and logs.
- `sol/`: MINLPLib points I downloaded myself.
- `pages/`: the fetched instance pages, `instances.html`, `minlplib.solu` and
  `doc.html`.

Commands, run from that directory with OMP/OPENBLAS threads limited to 4:

```
curl (instance pages, instances.html, minlplib.solu, doc.html, .sol points)
python3 v_hvycrash.py
python3 gibbs_sym.py
python3 gibbs_kkt.py ex6_2_7 ex6_2_5
python3 gibbs_bb.py ex6_2_7 0 1e-14 6     # exploratory, 46 s
python3 gibbs_bb.py ex6_2_7 0 1e-17 6     # fails as expected (floor about -4.2e-15)
python3 gibbs_bb.py ex6_2_7 0 6e-15 6     # used, 50 s
python3 gibbs_bb.py ex6_2_5 0 1e-17 8     # used, 200 s
python3 gibbs_bound.py ex6_2_7 0=logs/ex6_2_7_bb_type0_tau6e-15.json
python3 gibbs_bound.py ex6_2_5 0=logs/ex6_2_5_bb_type0_tau1e-17.json
python3 gibbs_sanity.py ex6_2_7 ; python3 gibbs_sanity.py ex6_2_5
python3 v_etamac.py                       # 26 s
python3 v_pricing050.py                   # 20 s
python3 v_lindo.py {methanol50,rocket100,rocket200,rocket400} 1e-12   # < 3 s each
python3 krawczyk_sanity.py
```

An earlier ex6_2_7 run at τ = 1e-10 used λ converted through doubles. I
discarded it. A first Krawczyk run converted interval endpoints at 53 bits;
I fixed this to exact 300-bit copies and re-ran all four instances. The
results above are from the fixed code.
