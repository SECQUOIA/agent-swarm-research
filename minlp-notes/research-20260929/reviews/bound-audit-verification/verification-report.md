# Independent verification of the MINLPLib bound audit

Date: 2026-09-30. Reviewed: `research-20260929/bound-audit/audit-report.md`
and `results.csv`. Nothing was committed. No solver developer or MINLPLib
maintainer was contacted.

## 1. Summary

I checked 14 of the audit's 19 "proven invalid" (class (i)) pairs, plus one
emfl instance, with my own code. The audit's code and its OSIL reader
(`osilx.py`) were not used. Every class (i) claim I checked holds: in each
case an exactly feasible point exists whose objective is beyond the listed
dual bound by more than the display-rounding slack. My objective values agree
with the audit's to the precision that matters. Where they differ slightly,
it is because my repaired point differs from the audit's; both are valid.

| instance | solver: listed dual (date) | my exactly feasible objective | margin (rel. to max(1,\|d\|)) | verdict |
|---|---|---|---|---|
| ghg_3veh | ANTIGONE, BARON: 7.7543245 (2013, 2014) | [7.754006050055795, 7.754006050057346] | 3.18e-4 (4.1e-5) | confirmed with caveats (model history) |
| nd_netgen-2000-3-4-b-a-ns_7 | CPLEX 10729659.03, GUROBI 10729661.15 (2022) | 10729657.585310902 (exact rational; 10729657.585117234 with minimal u) | 1.44 (1.35e-7), 3.56 (3.32e-7) | confirmed; tolerance-level size |
| watercontamination0303 | BONMIN 207.9850352, LINDO 207.9850353 (2014) | 207.9850348023888 (exact rational) | 3.98e-7 (1.9e-9), 4.98e-7 (2.4e-9) | confirmed; tolerance-level size |
| glider100 | COUENNE, LINDO: −1255.058601 (2015, 2014) | [−983842.2577883191, −983842.2577881224] | 9.83e5 (objective ratio 784) | confirmed (exact, not a tolerance or scaling artifact; see 3.4) |
| topopt-cantilever_60x40_50 | LINDO 35.35267044 (2022) | 10.335474275747004 (p5), 13.077481991525133 (p4), exact rationals | 25.02 (0.71) | confirmed |
| methanol50 | LINDO 0.00802826 (2022) | [0.0079302187853, 0.0079302187992] | 9.8e-5 (1.2% of \|d\|) | confirmed |
| nuclear14 | LINDO −1.12965944 (2022) | [−1.12968744117138, −1.12968744117116] | 2.80e-5 | confirmed |
| sssd20-04persp | LINDO 347716.8909 (2014) | [347691.4104839489, 347691.4104840173] | 25.48 (7.3e-5) | confirmed |
| smallinvDAXr1b150-165 | LINDO 88.1049355 (2014) | 88.10493476 exactly (listed point is exactly feasible) | 7.4e-7 (8.4e-9) | confirmed |
| smallinvDAXr1b200-220 | LINDO 156.604269 (2014) | 156.604267884 exactly (integers kept, objvar := xᵀQx) | 1.116e-6 (7.1e-9) | confirmed; tightest case, see 5 |
| emfl050_3_3 | all duals valid; listed optimum 10.40173793 | optimum in [10.40175213184103, 10.40175213184476] | listed optimum is 1.42e-5 below the proven lower bound | confirmed |

All instances have objective sense min, and every bound above is listed under
"Dual Bounds" on the instance page.

Not checked: 5 class (i) pairs, all LINDO (sssd22-08persp, sssd25-04persp,
sssd25-08persp, smallinvDAXr2b150-165, smallinvDAXr2b200-220). Also not
checked: the other three emfl instances, all (i-r), (ii) and (iii) rows, the
1633-page screen and its counts, and instance change histories.

## 2. Data and independence

- **Fetch.** `fetch.py` downloaded the instance pages, current OSIL files and
  the relevant `.sol` points from minlplib.org: 41 files in `data/` (40 MB),
  sequential, 2 s delay.
  - The fetched OSIL files are byte-identical to `~/.cache/minlplib`, which
    holds the audit's model files.
  - The fetched points are byte-identical to the audit's `sol/` files.
  - The listed values and dates quoted above come from my fetch, not from the
    audit's `pages.json`. They agree with the audit report.
- **Own code** (all in this directory):
  - `osil.py`: OSIL reader. It keeps all data as exact Fractions and handles
    `mult`/`incr` arrays, row and objective constants, quadratic terms and
    OSnL trees. A variable missing from a `.sol` file is set to 0, and every
    such 0 is checked against its bounds.
  - `ivl.py`: interval arithmetic with rational endpoints, rounded outward to
    200-bit dyadics.
    - +, −, ×, ÷ and integer powers are exact before rounding. sqrt is exact
      via `isqrt`.
    - exp and ln use mpmath at 90 digits, padded by a relative 1e-60. exp
      of arguments ≤ −5000 is enclosed by [0, 2⁻⁷⁰⁰⁰].
    - mpmath matters only for glider100 and ghg_3veh (exp). The other
      instances are algebraic.
  - `ad.py`: forward-mode differentiation over floats or intervals.
  - `kraw.py`, `run_kraw.py`: my own Krawczyk test.
    - Integers are fixed. Variables exactly on a bound are fixed (optional
      snapping). The system is the equality rows plus the active inequalities
      with a nonzero gradient.
    - The basis comes from QR with column pivoting. The centre comes from
      Newton with exact residuals.
    - The test is K(X) ⊂ int X with an interval Jacobian over X. Float matrix
      products carry the a-priori bound |fl(AB) − AB| ≤ γ_k|A||B|, with a
      factor 2 and underflow terms.
    - A box check then covers every other row, every bound and integrality,
      and encloses the objective (constant included).
  - Dedicated exact certificates: `nd_netgen_exact.py`, `water_exact.py`,
    `topopt_exact.py` and `emfl_cert.py` (Section 3).
- **Negative controls** (`sanity.py`, `logs/sanity.log`), on ghg_3veh p2 and
  glider100 p2. All behave as expected:
  - the unperturbed test passes;
  - moving the centre by 1e-9 (relative) with radius 1e-13 fails (ratio 1e4);
  - shifting the right-hand side of one system row by 1e-8 fails;
  - lowering a basic variable's upper bound to its centre value makes the box
    check fail and name that variable.
- **Listed points in exact arithmetic** (`evalpt.py`, `logs/evalpt.log`). My
  worst violations agree with the audit's:
  - glider100 p2: 1.18e-7;
  - nd_netgen p2: 1.70e-5 in cone row e6873, where the site lists 1e-12. The
    listed point really violates this row in exact arithmetic, as the audit
    says.
  - The listed objectives match the pages.

## 3. Per-case details

### 3.1 ghg_3veh (ANTIGONE, BARON: 7.7543245)

- **Method.** Krawczyk on p2 (`logs/kraw_ghg_3veh.p2.log`).
  - Binaries are fixed at their exact 0/1 values.
  - The square system has 52 rows (46 equalities and 6 active inequalities
    held at their bounds) in 52 basic variables.
  - Rows such as b1·x49 ≤ 0 with b1 = 0 are constant once the binaries are
    fixed. They are decided exactly in the box check.
- **Result.** At radius 1e-13 the Krawczyk ratio is 9.1e-4, and the box check
  passes. The objective x46 + x64 + x82 (no constant) lies in
  [7.754006050055795, 7.754006050057346].
- **Margin.** 3.18e-4 against a slack of 5e-8.
- **Version evidence.** Both duals equal the objective of p1 (added 2011),
  7.75432450745. p1 still satisfies the current file to 4.9e-13. This fits an
  unchanged model, but does not prove it.
- **Caveat.** The relative margin, 4.1e-5, is below common relative gap
  tolerances (1e-4). A reported dual bound must still be valid, but the error
  is of tolerance scale.

### 3.2 nd_netgen-2000-3-4-b-a-ns_7 (CPLEX 10729659.03, GUROBI 10729661.15)

- **Structure** (asserted in the script):
  - objective: min Σ c_b·b + Σ c_f·f + Σ u, no constant;
  - capacity rows f ≤ cap·b;
  - 74 flow-conservation rows with integer data;
  - defining rows s = (u − b)/2 and t = (u + b)/2;
  - cone rows c f² + s² − t² ≤ 0, which is c f² ≤ u·b;
  - b binary, 0 ≤ f ≤ cap, u ≥ 0, s and t free.
- **Exact repair** (`logs/nd_netgen_exact.log`):
  1. The binaries are already exactly 0/1. The 1280 closed arcs already have
     flow exactly 0.
  2. Conservation is restored by exact Gauss–Jordan elimination on 72
     interior open arcs. The 74 rows have rank 72, and the two dependent rows
     are consistent exactly. The largest flow change is 1.2e-13.
  3. u is set to c f² on open arcs and to 0 on closed arcs (variant A), or to
     max(listed u, c f²) (variant B). s and t follow from their rows.
  4. Every row, bound and integrality condition holds exactly.
- **Result.** The objective is 10729657.585117234 (A) or 10729657.585310902
  (B). The audit's 10729657.585310911 corresponds to B.
- **Margins.** CPLEX 1.445 (1.35e-7); GUROBI 3.565 (3.32e-7).
- **Size.** Both are proven, but they are of tolerance size: below MINLPLib's
  1e-6 gap and below MIQCP feasibility tolerances.

### 3.3 watercontamination0303 (BONMIN 207.9850352, LINDO 207.9850353)

- **Structure.** All rows are linear, and the objective is quadratic with
  constant 9619.98394343983.
- **Method** (`water_exact.py`, `logs/water_exact.log`).
  - The listed decimals are kept for the 1022 bounded variables. The 14
    binaries are exactly 0/1.
  - The 106200 free variables are determined by 106200 single-unknown
    solves on equality rows.
  - Every row and bound holds exactly.
  - This is the same idea as the audit's `cert_linear.py`, implemented
    independently.
- **Result.** The objective is 207.9850348023888. It is an exact rational
  whose denominator has 1026 digits.
- **Margins.** BONMIN 3.98e-7; LINDO 4.98e-7. The slack is 5e-8.
- **Other duals.** BARON, CPLEX, GUROBI, SHOT and SCIP are all at or below
  the proven objective.

### 3.4 glider100 (COUENNE, LINDO: −1255.058601)

- **Method.** Krawczyk on all 1209 equality rows (`logs/kraw_glider100.p2.log`).
  - 42 variables are fixed. 7 are fixed by the model. 35 lie exactly on a
    bound: y₁ = 0, cL₀ = 0 and 33 other cL = 0.
  - 1209 basic variables are chosen from 1273 candidates.
  - Radius 1e-13 (relative); Krawczyk ratio 0.133.
  - The box check passes all bounds: vr ≥ 0.01, x, y, vx, r, h ≥ 0 and
    cL ∈ [0, 1.4].
- **Result.** The objective lies in [−983842.2577883191, −983842.2577881224].
  The listed p2 value, −983842.257788221, lies inside.
- **Objective check.** The OSIL objective is min −x102, the final range, with
  no constant. It matches GAMS row e810 (−x102 − objvar = 0).
- **Missing variables.** The 104 variables missing from p2's `.sol` file are
  the updraft terms ua = 2.5(1 − r)e^(−r) with r ≈ 1e8, plus x2, x104, x406
  and x1012.
  - At the listed zeros, the ua rows have residuals of about e^(−1e8), not
    exactly zero. The ua are basic, so the Krawczyk box covers their exact
    values.
  - The other four are genuine zeros.
- **Not an artifact.** The proof is exact, so the point is not a tolerance,
  scaling or objective misreading effect. It is an exact solution of the
  discretized equations as distributed. It is physically spurious:
  - tf = 62163 s, so the step is h = 621.6 s;
  - the altitude rises from 1000 m to about 64.6 km and ends at 900 m;
  - the vertical acceleration changes sign from node to node, with magnitude
    about 7.8 to 9.8 m/s², so the trapezoidal averages nearly cancel. This is a
    period-2 mode of the discretization at a huge step.
  - The claim concerns the instance, not the continuous glider problem.
- **Version evidence.** p1 (added 2014) satisfies the current file to
  1.1e-11, and its objective equals both duals.

### 3.5 topopt-cantilever_60x40_50 (LINDO 35.35267044)

- **Structure** (asserted in the script): min Σ c_e with c_e ≥ 0;
  Σ_k w²_{e,k} − c_e·b_e ≤ 0; 4920 equality rows linear in w only; the other
  rows involve binaries only.
- **Method** (`topopt_exact.py`, `logs/topopt_exact.log`). The construction
  differs from the audit's QR-basis approach.
  1. Keep b, which is exactly 0/1. All 7003 binary rows hold exactly.
  2. Set void-element w to 0. Their listed values are already exactly 0.
  3. Write w = w₀ + A_sᵀy, with G = A_sA_sᵀ computed in exact rationals.
  4. Krawczyk on Gy = r proves a solution in the box: n = 3162 for p5
     (ratio 7.7e-6) and n = 3056 for p4.
  5. Set c_e to the rational upper bound of Σ W². Every cone row then holds.
- **Result.** The exactly feasible objectives are 10.335474275747004 (p5) and
  13.077481991525133 (p4).
- **Margins.** LINDO 25.02 (from p5) and 22.28 (from p4).
- **Other duals.** GUROBI's 8.88779974 is consistent with both points. The
  audit's p5 value, 10.3354743278, comes from a different repair; both are
  valid.

### 3.6 emfl050_3_3 (tolerance-effect claim)

- **Structure** (asserted in the script):
  - min Σ c_k t_k, where only 180 of the 531 cones have c_k > 0;
  - t_k² ≥ ‖w_k‖² with t_k ≥ 0;
  - each w is defined by one equality, w = A_k z + e_k;
  - 18 base variables z ≥ 0.
- **Upper bound.** Take the numerical z from Clarabel, rounded to rationals.
  Compute w exactly, and set t := rational ceiling of ‖w‖. The whole OSIL
  model then holds exactly.
- **Lower bound** (my own derivation). Take y_k with ‖y_k‖ ≤ c_k and
  g = Σ A_kᵀy_k ≥ 0. Because z ≥ 0,

  Σ c_k t_k ≥ Σ y_k·w_k = g·z + Σ y_k·e_k ≥ Σ y_k·e_k.

  - y comes from the SOC duals.
  - Its negative g components are corrected exactly by a least-norm step,
    and y is then scaled by s = 1 − 2.2e-13.
- **Result** (`logs/emfl050_3_3.log`). The optimum lies in
  [10.40175213184103, 10.40175213184476], a gap of 3.7e-12. This is inside
  the audit's [10.4017521316, 10.4017521319].
- **Listed primal values below the optimum.**
  - The listed optimal value p2, 10.40173793 (primal section, infeas 2e-10),
    is 1.42e-5 below the lower bound, relative 1.37e-6.
  - p1, 10.40173999, is also 1.21e-5 below it.
  - No exactly feasible point attains either value.
- **Listed duals.** All are valid: BARON 10.40173793, LINDO/SCIP 10.40173999,
  ANTIGONE 0.116 and COUENNE 0.119.

### 3.7 LINDO spot checks

- **methanol50** (dual 0.00802826, equal to p3).
  - Krawczyk on p4: 1497 rows, algebraic, ratio 1.1e-3.
  - The objective, including the constant 5.01625659, lies in
    [0.0079302187853, 0.0079302187992].
  - Confirmed.
- **nuclear14** (dual −1.12965944).
  - Krawczyk on p3: 434 rows after 1128 variables are fixed at bounds or
    integer values.
  - The objective lies in [−1.12968744117138, −1.12968744117116].
  - Confirmed.
- **sssd20-04persp** (dual 347716.8909, equal to p2).
  - Krawczyk on p3 needs four listed values of 5e-15 snapped to 0 (x97,
    x100, x103, x106). Without the snap, the active rows x97 ≤ b81 and
    x97·x93 ≤ 0 are dependent and the Jacobian is singular.
  - The objective lies in [347691.4104839489, 347691.4104840173].
  - Confirmed.
- **smallinvDAXr1b150-165** (dual 88.1049355). The listed p2 is exactly
  feasible as listed, with objective exactly 88.10493476. Confirmed.
- **smallinvDAXr1b200-220** (dual 156.604269).
  - The integer point is kept, and objvar := xᵀQx = 156.604267884 exactly.
    The point is then exactly feasible.
  - The margin, 1.116e-6, is 2.2 times the audit's slack of 5e-7. It is also
    larger than a full unit in the last shown digit (1e-6), so it survives
    even if the site truncates instead of rounding.
  - Confirmed.

## 4. Assessment of the audit's classification rules

- **Class (i) is sound under two assumptions.**
  - The model is the current OSIL file.
  - A listed value differs from the solver's number by at most half a unit in
    its last shown digit.

  The slack rule is conservative for that display format. Every class (i)
  margin I checked also exceeds a full unit in the last digit, so truncation
  instead of rounding would change no verdict.
- **Class (i) mixes two different things.**
  - Gross errors: glider100 (objective ratio 784), topopt (3.4×), methanol50 (1.2%),
    the sssd instances, nuclear14 and ghg_3veh (1e-5 to 1e-4).
  - Exact-arithmetic violations at 1e-9 to 3e-7 relative: nd_netgen,
    watercontamination0303 and smallinvDAX. These lie within the solvers'
    own feasibility and gap tolerances and within MINLPLib's 1e-6
    convention.

  I recommend reporting the two groups separately.
- **The margin normalization (d − f)/max(1, |d|) understates small-magnitude
  cases.** For methanol50 the audit reports "9.8e-5", but the error is 1.2%
  of |d|.
- **(i-r) "invalid as listed"** cannot be decided from the listing.
  "Consistent with rounding" would be a more neutral label. The audit already
  keeps it separate from (i).
- **(ii) proven** is sound. I confirmed it for emfl050_3_3.
- **(ii) repair** is correctly described as evidence only.
- **(iii)** is honestly described as a mixed class.
- **Inference stated as fact.** Section 1 says both glider100 solvers
  "reported a local optimum as a bound". This is an inference; the audit
  labels such statements as unproven only in Section 7.
- **Model identity** remains the main unverifiable assumption. For glider100
  and ghg_3veh, the older points behind the bounds remain feasible on the
  current file at the 1e-11 level. This supports an unchanged model.

## 5. Residual assumptions

- mpmath's exp and log at 90 digits are accurate to far better than the
  1e-60 padding. This matters for glider100 and ghg_3veh only.
- IEEE double arithmetic holds in numpy/BLAS. The γ_k bounds hold for any
  summation order.
- Python Fraction and integer arithmetic are exact.
- The numerical SOCP solver (Clarabel) and the Newton steps are heuristics
  only. Every certificate is checked exactly or by interval arithmetic.

## 6. Commands run (targeted only; no project-wide checks, no CI)

```
python3 fetch.py ghg_3veh:p1,p2 nd_netgen-2000-3-4-b-a-ns_7:p1,p2 watercontamination0303:p1,p2 \
  glider100:p1,p2 topopt-cantilever_60x40_50:p4,p5 emfl050_3_3:p1,p2
python3 fetch.py methanol50:p3,p4 nuclear14:p3 sssd20-04persp:p2,p3 smallinvDAXr1b150-165:p2
python3 fetch.py smallinvDAXr1b200-220:p2
python3 evalpt.py <points>                                  # logs/evalpt.log
python3 run_kraw.py ghg_3veh.p2 | glider100.p2 | methanol50.p4 | nuclear14.p3 | smallinvDAXr1b200-220.p2
python3 run_kraw.py sssd20-04persp.p3 --snap 1e-12
python3 nd_netgen_exact.py p2
python3 water_exact.py p2
python3 topopt_exact.py p5 p4                               # about 35 s each
python3 emfl_cert.py emfl050_3_3 "" p2=10.40173793 p1=10.40173999 p3=10.40180127 BARON=10.40173793 LINDO=10.40173999 SCIP=10.40173999
python3 sanity.py                                           # negative controls
```

All of these runs finished. The results in the logs match the numbers
reported here.
