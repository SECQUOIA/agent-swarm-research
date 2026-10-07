# Audit: MINLPLib per-solver dual bounds versus exactly feasible points

Updated 2026-10-03: publication integration adds independent class (i-r)
proofs and page parsing, the model-history/status refresh, the SCIP finding,
and reproduction limits. The original computational audit is dated
2026-09-30. Its results were checked
twice with separate code. A third check confirmed the fixes made after the
second and found eight text problems, fixed in Section 10.2. A fourth check
confirmed those eight fixes and found two wording problems, fixed in
Section 10.3. A fifth check confirmed those two fixes and found no remaining
problem.

| check | report | confirmed |
|---|---|---|
| first verification | `research-20260929/reviews/bound-audit-verification/verification-report.md` | 14 of the 19 class (i) pairs; the emfl050_3_3 bounds |
| recheck | `research-20260929/reviews/bound-audit-recheck.md` | the other 5 class (i) pairs; the bounds of emfl050_5_5, emfl100_3_3 and emfl100_5_5; the counts in this report, recomputed from the data files |
| confirmation, round 1 | `research-20260929/reviews/recheck-audit-confirm.md` | the nine fixes made after the recheck; every displayed enclosure and bound of this audit's own results (with a stricter display check). It found eight remaining text problems, fixed in Section 10.2 |
| confirmation, round 2 | `research-20260929/reviews/audit-confirm-r1.md` (titled "round 2") | the eight fixes of Section 10.2, recomputed from the data files; the stricter `check_display.py`, with negative controls. It found two wording problems, fixed in Section 10.3 |
| confirmation, round 3 | `research-20260929/reviews/audit-confirm-r2.md` | the two fixes of Section 10.3; no remaining problem |

All 19 class (i) pairs, all 12 class (i-r) pairs and all four (ii)-proven
emfl instances are confirmed independently. The publication tracks also
checked page parsing and model histories (Section 8.4). Class (ii)-repair
and (iii) did not acquire independent validity proofs. The original audit
code, data and logs are in
`research-20260929/bound-audit/`. Nothing was committed. No solver developer
or MINLPLib maintainer was contacted.

Revised after the first verification:
- class (i) is split into gross errors and tolerance-scale violations;
- margins are given in absolute terms and relative to |d|;
- inferences about solver behaviour are labelled as such;
- the verifier's description of the glider100 point is added.

Revised after the recheck: see Section 10.1. No class, count or verdict
changed. Displayed enclosures and bounds are now rounded outward, and several
statements are corrected.

Revised after confirmation round 1: see Section 10.2. No class, count,
margin or verdict changed. The text and `check_display.py` were corrected.

Revised after confirmation round 2: see Section 10.3. Two wording fixes
only; no number, class or verdict changed, and no code or data file changed.

A *dual bound* d for a minimization instance is valid if d ≤ f(x) for every
exactly feasible point x of the instance (the OSIL model as distributed by
MINLPLib, with exact decimal data). For maximization, the inequality is
reversed. Below, "beyond the dual" means below d for minimization and above d
for maximization.

## 1. Summary

**Scope.** I fetched the instance page of every instance in the MINLPLib
listing (1633 pages, 2026-09-30). The pages list 2816 points and 11086
per-solver dual bounds (11031 of them finite).

**Screen.** In 158 (dual bound, listed point) pairs, the displayed dual lies
strictly beyond the displayed objective of a point whose listed violation is
at most 1e-5. These pairs cover 46 instances and 56 points. I downloaded and
evaluated all 56 points in 40-digit arithmetic. All 56 have a violation of at
most 1e-6 by my measure, or MINLPLib lists them as feasible, so all 158 pairs
are flagged.

A further 3851 pairs (1133 instances) have a dual bound equal to a point's
objective in every displayed digit. The listed data cannot decide these pairs,
because the displayed dual may be a rounding of a valid bound.

**Classification** of the 131 distinct (instance, solver) pairs, using the
strongest result over the flagged points:

| class | meaning | pairs | instances |
|---|---|---|---|
| (i) proven invalid, gross | an exactly feasible point is proven to exist with objective beyond d by more than the rounding slack of d's shown digits, and by more than 1e-6 of \|d\| | 11 | 9 |
| (i) proven invalid, tolerance-scale | same proof, but the margin is at most 1e-6 of \|d\| (here 1.9e-9 to 3.3e-7): below MINLPLib's 1e-6 relative gap convention, and of the size of typical solver tolerances | 8 | 6 |
| (i-r) invalid as listed | same proof, but the margin is within the rounding slack, so rounding in the listing can explain it | 12 | 4 |
| (ii) proven | the flagged point is only tolerance feasible, and a rigorous bound proves that d is valid | 12 | 4 |
| (ii) repair | the flagged point is only tolerance feasible; an exactly feasible point near it is proven to exist, but its objective is not beyond d (evidence, not a proof, that d is valid) | 63 | 11 |
| (iii) undecided | no proof either way | 25 | 12 |

Margins are given two ways: the absolute margin d − f, and the margin
relative to the listed dual, (d − f)/|d|. Here f is the upper end of the
proven objective enclosure (minimization). An earlier version of this report
used (d − f)/max(1, |d|), which understates cases with |d| < 1. For
methanol50 it gave 9.8e-5, while the error is 1.2% of |d|.

**How numbers are displayed.** Proven enclosures [lo, hi] and proven bounds
are rounded outward at the digits shown: lower ends down, upper ends up. A
value ending in "…" is an exact rational, truncated. Margins, ratios, point
values and violations are rounded to nearest; they are sizes, not bounds.
Every class decision uses the exact endpoints, not the displayed ones.

**Class (i), gross errors** (11 pairs, 9 instances; (d − f)/|d| from 1.2e-5
to 783):

| instance | solver | listed dual d | proven exactly feasible objective f | d − f | (d − f)/\|d\| |
|---|---|---|---|---|---|
| glider100 | COUENNE, LINDO | −1255.058601 | [−983842.2577737, −983842.2577716] | 982587.2 | 783 (f/d = 784) |
| topopt-cantilever_60x40_50 | LINDO | 35.35267044 | [10.33547432780, 10.33547432781] (p5); [13.07748199152, 13.07748199153] (p4) | 25.02 | 0.71 (d/f = 3.4) |
| methanol50 | LINDO | 0.00802826 | [0.007930218684615, 0.007930218899920] | 9.80e-5 | 1.2e-2 |
| sssd20-04persp | LINDO | 347716.8909 | [347691.4104835, 347691.4104845] | 25.48 | 7.3e-5 |
| sssd22-08persp | LINDO | 508748.972 | [508713.7310104, 508713.7310120] | 35.24 | 6.9e-5 |
| ghg_3veh | ANTIGONE, BARON | 7.7543245 | [7.754006050048, 7.754006050065] | 3.18e-4 | 4.1e-5 |
| sssd25-04persp | LINDO | 300186.8048 | [300176.5636655, 300176.5636663] | 10.24 | 3.4e-5 |
| nuclear14 | LINDO | −1.12965944 | [−1.129687441173, −1.129687441170] | 2.80e-5 | 2.5e-5 |
| sssd25-08persp | LINDO | 472098.947 | [472093.0779691, 472093.0779707] | 5.87 | 1.2e-5 |

"Gross" is a size label: the margin exceeds 1e-6 of |d|. It does not mean
that every such bound is far outside what solvers tolerate.
- Four pairs (three instances) are clear errors under relative gap
  tolerances measured against |d|: glider100 (COUENNE and LINDO, a factor
  of 784), topopt-cantilever_60x40_50 (3.4 times the proven point) and
  methanol50 (1.2% of |d|).
  - glider100 and topopt also have large absolute margins (982587 and
    25.02).
  - methanol50 does not. Its |d| is 0.008 and its absolute margin is
    9.8e-5. Relative to max(1, |d|), the margin is also 9.8e-5, just below
    1e-4. Whether methanol50 exceeds a common tolerance therefore depends on
    how the gap is measured.
- The other seven gross pairs (sssd ×4, nuclear14, ghg_3veh ×2) have
  margins from 1.2e-5 to 7.3e-5 of |d|. These exceed MINLPLib's 1e-6
  convention, but they are below common relative gap tolerances of 1e-4.

**Class (i), tolerance-scale violations** (8 pairs, 6 instances; (d − f)/|d|
from 1.9e-9 to 3.3e-7):

| instance | solver | listed dual d | proven exactly feasible objective f | d − f | (d − f)/\|d\| |
|---|---|---|---|---|---|
| nd_netgen-2000-3-4-b-a-ns_7 | GUROBI | 10729661.15 | 10729657.585310911… (exact rational) | 3.56 | 3.3e-7 |
| nd_netgen-2000-3-4-b-a-ns_7 | CPLEX | 10729659.03 | same | 1.44 | 1.3e-7 |
| smallinvDAXr1b150-165, smallinvDAXr2b150-165 | LINDO | 88.1049355 | 88.104934760000006 exactly (the listed point, exactly feasible as listed) | 7.4e-7 | 8.4e-9 |
| smallinvDAXr1b200-220, smallinvDAXr2b200-220 | LINDO | 156.604269 | [156.60426788384, 156.60426788416] | 1.12e-6 | 7.1e-9 |
| watercontamination0303 | LINDO | 207.9850353 | 207.98503480238880… (exact rational) | 4.98e-7 | 2.4e-9 |
| watercontamination0303 | BONMIN | 207.9850352 | same | 3.98e-7 | 1.9e-9 |

- The tolerance-scale violations are proven exactly. They exceed the
  display slack, so the listed numbers are invalid as bounds.
- They are below MINLPLib's 1e-6 relative gap convention: by a factor of 3
  for nd_netgen GUROBI, 7 for nd_netgen CPLEX, and more than 100 for the
  others. They are of the size of typical feasibility and optimality
  tolerances. The solver settings of these runs are not known, so I cannot
  say whether each lies within the tolerance its run used.
- *Judgment, not proven:* I read them as tolerance-level effects, not as
  solver errors of the kind shown by the four clear gross pairs.
- The gross errors, above all the four clear pairs, are the substantive
  findings.

**By solver:**
- LINDO: 8 gross, 5 tolerance-scale.
- ANTIGONE and BARON: 1 gross each (ghg_3veh).
- COUENNE: 1 gross (glider100).
- CPLEX and GUROBI: 1 tolerance-scale each (nd_netgen).
- BONMIN: 1 tolerance-scale (watercontamination0303).

**Distribution of (d − f)/|d| over the 19 pairs:**

| (d − f)/\|d\| | pairs |
|---|---|
| [1e-9, 1e-7) | 6 (tolerance-scale) |
| [1e-7, 1e-5) | 2 (tolerance-scale: nd_netgen) |
| [1e-5, 1e-3) | 7 (gross: sssd ×4, ghg_3veh ×2, nuclear14) |
| [1e-3, 1e-1) | 1 (gross: methanol50) |
| ≥ 0.1 | 3 (gross: glider100 ×2, topopt-cantilever_60x40_50) |

**Solved instances whose closing bound is proven invalid.** MINLPLib marks
each of these instances as solved (S). In each, the listed bound lies within
MINLPLib's 1e-6 relative gap of the best listed primal, so I count it as one
of the bounds that close the instance. The S mark itself rests on solver
claims, which the pages do not show.

| instance | solver | listed dual d | exactly feasible objective f (proven) | d − f | (d − f)/\|d\| |
|---|---|---|---|---|---|
| nd_netgen-2000-3-4-b-a-ns_7 | CPLEX | 10729659.03 | 10729657.585310911… | 1.44 | 1.3e-7 |
| nd_netgen-2000-3-4-b-a-ns_7 | GUROBI | 10729661.15 | same | 3.56 | 3.3e-7 |
| watercontamination0303 | BONMIN | 207.9850352 | 207.98503480238880… | 4.0e-7 | 1.9e-9 |
| watercontamination0303 | LINDO | 207.9850353 | same | 5.0e-7 | 2.4e-9 |
| smallinvDAXr1b150-165, smallinvDAXr2b150-165 | LINDO | 88.1049355 | 88.104934760000006 exactly (the listed point is exactly feasible) | 7.4e-7 | 8.4e-9 |
| smallinvDAXr1b200-220, smallinvDAXr2b200-220 | LINDO | 156.604269 | [156.60426788384, 156.60426788416] | 1.1e-6 | 7.1e-9 |

All of these are tolerance-scale violations, smaller than 1e-6 relative.
They therefore do not contradict the S mark, which allows a relative gap of
1e-6.

LINDO's bounds on the four solved sssd*persp instances are proven invalid by
gross margins (Section 4), but they are not closing bounds. Within rounding
(class (i-r)), the closing bounds of eniplac (COUENNE, LINDO, SCIP; listed
−132117.) and lop97icx (ANTIGONE; listed 4099.06) are also invalid as
listed.

**Largest findings: glider100 and topopt-cantilever_60x40_50.** In both,
MINLPLib lists the decisive point only under "other points", because its
violation exceeds 1e-8, but the point repairs to an exactly feasible point.

- **glider100.**
  - Point p2 (infeas 3e-8) has objective −983842.2578.
  - It repairs to an exactly feasible point with objective in
    [−983842.2577737, −983842.2577716].
  - COUENNE and LINDO list −1255.058601 as their dual bound, which equals
    the objective of point p1. That both solvers reported a local optimum
    as a bound is an inference from this equality. It is not verified.
  - Consequence: the discretized glider model, as distributed, has optimum
    at most −983842.2577. Its listed primal bound (−1255.06) is off by a
    factor of 784.
  - The exactly feasible point is a spurious solution of the discretization.
    The independent verification describes it (Section 8):
    - the final time is tf = 62163 s, so the time step is h = 621.6 s;
    - the altitude first drops from 1000 m to 0 at node 1, then rises to
      about 64.6 km and returns to 900 m at the final node. The value at
      node 1 is exactly 0 in the listed point and in the verifier's repair,
      where the variable sits on its bound 0. In this audit's repair it is
      about 1e-10 m, because route C moved it off the bound;
    - the vertical acceleration changes sign from node to node (magnitude
      about 7.8–9.8 m/s²), so the trapezoidal averages nearly cancel. This
      is a period-2 mode of the discretization at a huge step.

    The listed bounds are therefore invalid for the model as written,
    although the point is physically meaningless. The finding concerns the
    instance, not the continuous glider problem.
- **topopt-cantilever_60x40_50.**
  - Points p4 and p5 (violations 2.3e-8 and 1.2e-7, in linear equilibrium
    rows) repair to exactly feasible points with objectives in
    [13.07748199152, 13.07748199153] and [10.33547432780, 10.33547432781].
  - LINDO's listed dual 35.35267044 is invalid. GUROBI's listed 8.88779974
    is consistent with both points.
  - The listed primal bound (46.34, point p3) is 4.5 times the proven
    10.3355.

**Tolerance effects are common.** Examples:
- In 110 of the 158 pairs, the point comes from the "other points" section.
- The emfl facility-location instances are second-order cone programs. For
  all four, I proved two-sided bounds on the exact optimum with gaps of at
  most 5e-9 (Section 3.2). Every listed dual is valid.
- Every listed point of emfl050_5_5, emfl100_3_3 and emfl100_5_5, and all
  listed points of emfl050_3_3 except p3, have values below the exact
  optimum. This includes primal-section points with listed violation 4e-11
  to 8e-10; for example, emfl050_5_5 p3 (4e-11) lies 1.2e-4 below, and
  emfl050_5_5 p2 (8e-10) lies 2.25e-4 below. (The recheck found this; I
  confirmed it against the lower bounds proven here.)
  The largest gaps are about 1e-4 relative for points with violation 1e-8,
  and 4.3e-4 relative for "other" points. The listed primal bound itself is
  below the exact optimum in all four:
  - emfl050_5_5: listed 18.91165289; exact optimum ≥ 18.9136329529.
  - emfl100_3_3: listed 18.13236088; exact optimum ≥ 18.1326531194.
  - emfl050_3_3 (solved): the listed optimal value 10.40173793 is below the
    exact optimum by at least 1.42e-5 (relative 1.36e-6).
  - emfl100_5_5 (solved): the listed optimal value 32.63818348 is below the
    exact optimum by at least 6.87e-6.

**Rigor.** Every class (i), (i-r) and (ii)-proven result rests on one of
these:
- exact rational arithmetic;
- a Krawczyk existence test in outward-rounded interval arithmetic;
- an exact weak-duality certificate.

Each route starts from the exact OSIL decimals. The assumptions are in
Section 7. Class (ii)-repair is evidence only. Class (iii) says nothing.

Independent code (Section 8) has confirmed all 19 class (i) pairs and the
(ii)-proven bounds of all four emfl instances. The later publication
[audit-ir track](../publication/audit-ir/report.md) independently re-proved
all 12 class (i-r) pairs (Section 8.4).

## 2. Data collection

- `fetch_pages.py` fetched `instances.html`, `minlplib.solu` and all 1633
  instance pages.
  - Requests were sequential with a 1 s delay.
  - Each page is cached in `pages/`, truncated before the GAMS listing.
- `parse_pages.py` wrote `pages.json`. For each instance it records:
  - the listing's type, convexity mark, S mark and listing bounds;
  - the objective sense;
  - every listed point: displayed value, displayed infeas, and section
    (primal: infeas ≤ 1e-8; other: larger infeas);
  - every per-solver dual bound, with its date.

  Numbers are kept as the displayed strings.
- **Display precision.** Values are shown with at most 8 decimals; there is
  no 10-significant-digit limit. Counts refer to displayed entries, not
  distinct numbers: 35 entries (18 distinct strings) with a nonempty
  fractional part have 11–17 digits from the first through last nonzero
  digit; dropping the fractional-part filter gives 38 entries with 11–19
  digits; counting trailing integer zeros as significant gives 46 entries
  with 11–20 digits (for example −10000000000.). Trailing fractional zeros
  are dropped. Some entries carry
  only 6 significant digits, for example "−132117." and "119949.". Every
  such entry involved in this audit is dated 17 or 26 Sep 2013. I cannot
  tell whether a displayed dual was rounded, and how, before it was
  stored.
  - For each listed dual, the **slack** is half a unit in its last shown
    digit, but never less than half a unit in the 10th significant digit.
    This floor is an explicit conservative choice, not a consequence of a
    display limit. It changes the slack of 0 of the 158 screened pairs and
    therefore changes no screened-pair class. It changes 17 display-tie
    pairs on three instances: fac1, fac2 and waternd_fosspoly0.
    For the value 0, the slack is 5e-9.
  - A proven violation larger than the slack cannot come from rounding the
    dual to its shown digits. That is class (i).
  - A proven violation no larger than the slack is class (i-r).
- **Screen** (`audit.py screen`).
  - A pair (solver dual d, point p) is kept when the displayed values satisfy
    d > p (min) or d < p (max).
  - Points with listed infeas above 1e-5 are skipped. No such point lies
    beyond any listed dual.
  - Three instances have no objective sense (camcns, gancns, korcns: pure
    feasibility problems) and are skipped.
- **Points.** `audit.py download` fetched the 56 screened points from
  `https://www.minlplib.org/sol/<name>.<pk>.sol`, sequentially with a 1 s
  delay.

## 3. Evaluation and verification methods

### 3.1 High-precision evaluation (`audit_eval.py`)

**Parser.** The parser is `reviews/open-instances-verification/osilx.py`
(the verifier's reader). I checked the points that matter for this audit:

- It keeps every constant as its decimal string.
- It reads `<obj constant>`; row constants are added in `ev_row`.
- It expands `mult`/`incr`. In all 1632 OSIL files, `incr` occurs only in
  index arrays, which is the only case the reader handles.
- It asserts that `<number>` has type real.
- It parses the objective weight, which I assert is 1.

**Operators.** The operators used in the library are sum, product, negate,
divide, square, power, ln, log10, exp, sqrt, sin, cos, abs, signpower, tanh,
erf, min and gammaFn. I added the missing ones in `audit_eval.FNS`, with
domain checks.

**Not handled.**
- `osilx.py` ignores SOS constraints (6 water* instances). None of them is
  flagged.
- No instance has semicontinuous variables.

**What is computed.** Points are evaluated with mpmath at 40 digits from
their decimal strings. Variables missing from a `.sol` file are 0, and the
`objvar` entry, which the OSIL model does not contain, is ignored. The
output is:

- the objective, including its constant;
- the largest absolute violation of rows, bounds and integrality.

**Agreement with the listing.** All 56 objectives agree with the displayed
values to the displayed precision. The violations agree with the listed
infeas within a factor of about 10, or both are below 3e-10. Differences at
that level come from the 16–17-digit decimals in the `.sol` files. There are
two exceptions:

- **nd_netgen-2000-3-4-b-a-ns_7 p2.** Exact violation 1.7e-5, listed 1e-12.
  The row is c f² + s² − t² ≤ 0 with c = 5482.675589 and s, t ≈ 1.45e6. The
  double-precision value of s² − t² loses all its digits to
  cancellation.
- **glider100 p2.** Exact violation 1.2e-7, listed 3e-8.

**Flag rule.** A pair is flagged if the exact objective is beyond d and
either my violation or the listed infeas is at most 1e-6. All 158 pairs pass.

### 3.2 Existence of an exactly feasible point nearby (`verify.py`, `verify_one.py`)

- **Route A: the listed point as it is.**
  - Polynomial rows are evaluated in exact rational arithmetic; the others
    in mpmath interval arithmetic.
  - Equality rows need exact arithmetic.
  - Bounds and integrality are checked exactly.
  - Result: 4 points are exactly feasible as listed (lop97icx, stockcycle,
    smallinvDAXr1b150-165, smallinvDAXr2b150-165).
- **Route B: polish and Krawczyk.** This generalizes
  `open-instances-wave2/small/polish.py` and
  `reviews/wave2-small-verification/krawczyk.py`.
  1. Integer variables are rounded.
  2. The active rows are the equalities plus the inequalities that are
     violated or within 1e-7 (relative) of a side.
  3. From the continuous variables in active rows, a basis of |active rows|
     variables is chosen by QR with column pivoting. The weights favour
     variables away from their bounds.
  4. The non-basic variables keep their exact decimals, or are put exactly
     on a bound if they lie within 1e-7 of it.
  5. Newton runs on the square system, with residuals at 40 digits.
  6. A midpoint–radius Krawczyk test runs on a box X of relative radius
     1e-12, 1e-10 or 1e-8 around the Newton point. It uses the same operator
     and the same floating-point error terms (γ_n, safety factor) as the
     reviewed `krawczyk.py`. It proves that X contains exactly one solution
     of the square system.
  7. On X, every other row is enclosed: exactly (rational polynomial in the
     basic variables) where possible, otherwise by interval arithmetic. The
     bounds of the basic variables are also enclosed. Every non-basic value
     is checked exactly against its bounds and integrality.
  8. The objective, including its constant, is enclosed over X.

  If a basic variable ends up on a bound, it is fixed there and the attempt
  is repeated (up to 3 rounds), followed by a "snap all near-bound variables
  first" variant.
- **Route C: shift into the interior.** This route is for degenerate
  mixed-integer points.
  1. Continuous variables fixed exactly by a row that is linear in its only
     free variable are fixed, repeatedly. Rows that become constant are
     decided exactly.
  2. A direction LP (HiGHS) finds a step that keeps the linearized
     equalities and strictly improves as many active inequalities and bounds
     as possible. A second LP minimizes the objective change on that set.
  3. Constraints that cannot be improved are kept as equalities (rows) or
     fixed at the bound (variables).
  4. The route steps a distance t along the direction, then applies route B's
     Newton, Krawczyk and box checks. t grows by factors of 10 from 3 times
     the violation.

  The repaired point can therefore lie farther from the listed point. Its
  objective is still rigorously enclosed.
- **Dedicated certificates**, for the four structures that the generic
  routes could not handle. The first two finish with an exact rational check
  of every row and bound of the OSIL model. `cert_socp.py` checks its point
  and its dual exactly. `cert_topopt.py` ends with route B's box check.
  - `cert_linear.py` (watercontamination0303).
    - All rows are linear and the objective is quadratic.
    - Binaries are rounded, and the 1008 bounded source variables keep their
      decimals.
    - Every other variable is computed exactly by propagation through
      equality rows with one unknown: 106200 rows, all variables determined.
    - Result: exactly feasible, and the objective is an exact rational.
  - `cert_ndnetgen.py` (nd_netgen p2).
    - Binaries are rounded.
    - The 74 flow-conservation rows are made to hold exactly by rational
      Gauss–Jordan elimination on flows strictly inside their bounds. The
      largest flow change is 2.1e-13.
    - Then u := max(u, c f²) and s, t follow from their defining rows, so
      each cone row c f² ≤ u·b holds exactly.
  - `cert_socp.py` (emfl050_3_3, emfl050_5_5, emfl100_3_3, emfl100_5_5).
    - The script asserts from the OSIL file that the instance is
      min Σ c_k t_k with t_k ≥ ‖A_k x + e_k‖, where each w-variable is
      defined by one linear equality and the base variables are free or
      ≥ 0.
    - **Upper bound.** Any base point, completed with
      t_k = sqrt(Σ w²) rounded up to a rational, is exactly feasible.
    - **Lower bound (weak duality).** For y_k with ‖y_k‖ ≤ c_k and
      Σ A_kᵀ y_k = 0, the value Σ y_k·e_k is a lower bound. y comes from the
      numerical dual SOCP (cvxpy/Clarabel). It is corrected exactly by a
      rational least-norm step, then scaled by a rational s ≤ 1 so that
      every norm condition holds. Both conditions are checked in exact
      arithmetic.
  - `cert_topopt.py` (topopt-cantilever_60x40_50 p4 and p5).
    - The script asserts that the cone rows are Σ w² ≤ c_e·y_e, that the
      equality rows are linear in the stress variables w only, and that the
      objective is Σ c_e.
    - Binaries are rounded. In void elements (y_e = 0), all w are exactly 0
      in the listed point (asserted) and stay 0.
    - Of the 4920 equality rows, 3056 (p4) or 3162 (p5) involve free w. For
      them, a basis of solid-element w is chosen by QR. Newton (the system is
      linear) and the Krawczyk test then prove a solution in a box X, with
      worst ratio 0.011 at radius 1e-14.
    - c_e is set to the exact upper endpoint of the interval enclosure of
      Σ w² over X, so every cone row holds.
    - Route B's box check then verifies every other row, all bounds and
      integrality, and encloses the objective.

### 3.3 Classification (`audit.py classify`, `summarize.py`)

For a flagged pair with a proven exactly feasible point of objective
enclosure [lo, hi] (minimization):

- d − hi > slack: **(i)**. It is **gross** if d − hi > 1e-6·|d|, and
  **tolerance-scale** otherwise.
- 0 < d − hi ≤ slack: **(i-r)**.
- lo ≥ d: **(ii) repair**.
- otherwise: **(iii)**.

In addition:

- If a rigorous lower bound L on the exact optimum satisfies d ≤ L:
  **(ii) proven**.
- If verification failed: **(iii)**.

Maximization is symmetric. The per-(instance, solver) summary keeps the
strongest class over that solver's flagged points.

### 3.4 Negative controls (`sanity.py`, log `logs/sanity.log`)

1. ghg_3veh p2 verifies through route B (positive control).
2. Krawczyk on methanol50:
   - the centre moved by 1e-11 (relative) with radius 1e-12 fails, as it
     should;
   - the same centre with radius 1e-11, which contains the solution, passes;
   - the unperturbed centre passes.
3. The box check passes on a 1e-12 box around the ghg_3veh proof centre. It
   fails, naming the right row, once an inactive row is tightened by 1e-9
   below its value.
4. Route A rejects a point once a bound cuts off one of its values.

**Numerical cross-check.** The centre of every proof box was re-evaluated
with the independent evaluator (`audit_eval.py`). Row residuals are at the
double-rounding level (up to 1.4e-8 for glider100, whose values reach 1e8;
1.8e-17 for the topopt centres), and the objectives lie inside the
enclosures.

## 4. Full classified table

One line per (instance, point, class), with all listed duals of that group.

- S: solved mark in the listing.
- f(point): the listed point's exact objective.
- viol.: its largest absolute violation.
- Exact point / bound: the enclosure of the proven exactly feasible point's
  objective, or the rigorous lower bound on the optimum. Both are rounded
  outward at 13 significant digits.
- f(point), viol., margins and the repaired values in the note column are
  rounded to nearest.
- Slack: rounding slack of the listed dual.
- Margins of class (i) and (i-r) rows are given as absolute d − f and as a
  fraction of |d|.

The per-pair data (158 rows) are in `results.csv` and `results.json`.

| instance | S | point (section) | f(point) | viol. | solvers: listed dual | class | exact point / bound | note |
|---|---|---|---|---|---|---|---|---|
| alkyl | yes | p2 (other) | -1.7650249825 | 7.9e-07 | ANTIGONE -1.76500127; BARON -1.76500008; COUENNE -1.76501147; LINDO -1.76499965; SCIP -1.7650056 | (ii) repair | [-1.764999645645, -1.764999645587] | exact repair not beyond the dual |
| cecil_13 | yes | p2 (primal) | -115656.49968 | 4.5e-12 | ANTIGONE -115656. | (iii) |  | active Jacobian rank 567 < 627 rows; margin at the listed point 0.5..0.5 vs slack 0.5: at most (i-r) |
| elf | yes | p2 (other) | 0.19155509427 | 5.6e-07 | ANTIGONE 0.19166667; BARON 0.19166667; COUENNE 0.19166667; GUROBI 0.19163215; LINDO 0.19166667; SCIP 0.19166667; SHOT 0.19166667 | (ii) repair | [0.1932226208163, 0.1932226208164] | exact repair not beyond the dual |
| emfl050_3_3 | yes | p2 (primal) | 10.401737935 | 2e-10 | LINDO 10.40173999; SCIP 10.40173999 | (ii) proven | opt >= 10.40175213162 | dual <= rigorous lower bound on the optimum; point repaired to 10.401754821 |
| emfl050_3_3 | yes | p5 (other) | 10.401041779 | 5.7e-07 | BARON 10.40173793; LINDO 10.40173999; SCIP 10.40173999 | (ii) proven | opt >= 10.40175213162 | dual <= rigorous lower bound on the optimum; point repaired to 10.401952458 |
| emfl050_3_3 | yes | p4 (other) | 10.40129699 | 1e-07 | BARON 10.40173793; LINDO 10.40173999; SCIP 10.40173999 | (ii) proven | opt >= 10.40175213162 | dual <= rigorous lower bound on the optimum; point repaired to 10.401949864 |
| emfl050_5_5 |  | p6 (primal) | 18.911652893 | 1e-08 | BARON 18.91340776; LINDO 18.91340776; SCIP 18.91340776 | (ii) proven | opt >= 18.91363295294 | dual <= rigorous lower bound on the optimum; point repaired to 18.914568775 |
| emfl050_5_5 |  | p5 (other) | 18.905509152 | 8.6e-07 | BARON 18.91340776; LINDO 18.91340776; SCIP 18.91340776 | (ii) proven | opt >= 18.91363295294 | dual <= rigorous lower bound on the optimum; point repaired to 18.918613211 |
| emfl050_5_5 |  | p4 (other) | 18.909192084 | 5e-08 | BARON 18.91340776; LINDO 18.91340776; SCIP 18.91340776 | (ii) proven | opt >= 18.91363295294 | dual <= rigorous lower bound on the optimum; point repaired to 18.915772054 |
| emfl100_3_3 |  | p4 (primal) | 18.132360875 | 1e-08 | BARON 18.13262446; LINDO 18.13262446; SCIP 18.13262446 | (ii) proven | opt >= 18.13265311948 | dual <= rigorous lower bound on the optimum; point repaired to 18.132747657 |
| emfl100_3_3 |  | p3 (other) | 18.131982441 | 9.4e-08 | BARON 18.13262446; LINDO 18.13262446; SCIP 18.13262446 | (ii) proven | opt >= 18.13265311948 | dual <= rigorous lower bound on the optimum; point repaired to 18.132866209 |
| emfl100_5_5 | yes | p2 (other) | 32.637836047 | 2.8e-07 | BARON 32.63818348; LINDO 32.63818348; SCIP 32.63818206 | (ii) proven | opt >= 32.63819035137 | dual <= rigorous lower bound on the optimum; point repaired to 32.638346899 |
| eniplac | yes | p2 (primal) | -132117.08302 | 2.5e-10 | COUENNE -132117.; LINDO -132117.; SCIP -132117. | (i-r) | [-132117.0830149, -132117.0830141] | margin COUENNE 0.083 (6.3e-07 of \|d\|), LINDO 0.083 (6.3e-07 of \|d\|), SCIP 0.083 (6.3e-07 of \|d\|); slack 0.5 |
| ex7_3_5 |  | p5 (other) | 1.2054531574 | 9.8e-07 | ANTIGONE 1.20687143; BARON 1.20665305; COUENNE 1.20652509; LINDO 1.20669187; SCIP 1.20569526 | (iii) |  | Newton did not converge; margin at the listed point 0.00024..0.0014 vs slack 5e-09: (i) if an exact point exists near it |
| ex7_3_5 |  | p4 (other) | 1.2055104971 | 9.1e-07 | ANTIGONE 1.20687143; BARON 1.20665305; COUENNE 1.20652509; LINDO 1.20669187; SCIP 1.20569526 | (iii) |  | Newton did not converge; margin at the listed point 0.00018..0.0014 vs slack 5e-09: (i) if an exact point exists near it |
| ex8_2_1b | yes | p2 (other) | -979.19130677 | 8.3e-07 | ANTIGONE -979.1782748; BARON -979.1782756; COUENNE -979.1782738; LINDO -979.1782738; SCIP -979.1791064 | (iii) |  | rows/bounds not verified on X: row e12; margin at the listed point 0.012..0.013 vs slack 5e-08: (i) if an exact point exists near it |
| ghg_3veh |  | p2 (primal) | 7.7540060501 | 5.5e-13 | ANTIGONE 7.7543245; BARON 7.7543245 | (i) gross | [7.754006050048, 7.754006050065] | margin ANTIGONE 0.000318 (4.1e-05 of \|d\|), BARON 0.000318 (4.1e-05 of \|d\|); slack 5e-08 |
| glider100 |  | p2 (other) | -983842.25779 | 1.2e-07 | COUENNE -1255.058601; LINDO -1255.058601 | (i) gross | [-983842.2577737, -983842.2577716] | margin COUENNE 9.83e+05 (7.8e+02 of \|d\|), LINDO 9.83e+05 (7.8e+02 of \|d\|); slack 5e-07 |
| hda | yes | p2 (primal) | -5964.5340835 | 1e-10 | ANTIGONE -5964.53; LINDO -5964.53 | (iii) |  | nonpolynomial active row e68 over fixed variables not verifi; margin at the listed point 0.0041..0.0041 vs slack 0.005: at most (i-r) |
| heatexch_spec2 | yes | p2 (primal) | 634977.82837 | 1.3e-11 | BARON 634978. | (iii) |  | overdetermined: 63 active rows, 48 candidates; margin at the listed point 0.17..0.17 vs slack 0.5: at most (i-r) |
| hybriddynamic_fixedcc | yes | p2 (other) | 1.4735037636 | 7e-08 | ANTIGONE 1.47377775; BARON 1.47377778; COUENNE 1.47377778; CPLEX 1.47377778; GUROBI 1.47377776; LINDO 1.47377778; SCIP 1.47377778 | (ii) repair | [1.479131862450, 1.479131893270] | exact repair not beyond the dual |
| hybriddynamic_varcc | yes | p3 (other) | 1.5359426714 | 3e-08 | ANTIGONE 1.53641516; BARON 1.53641516; COUENNE 1.53641516; LINDO 1.53641516; SCIP 1.53641405 | (ii) repair | [1.539421798927, 1.539421851044] | exact repair not beyond the dual |
| lop97icx | yes | p2 (primal) | 4099.0599536 | 0 | ANTIGONE 4099.06 | (i-r) | [4099.059953600, 4099.059953601] | margin ANTIGONE 4.64e-05 (1.1e-08 of \|d\|); slack 0.005 |
| methanol50 |  | p4 (primal) | 0.0079302187923 | 8.5e-12 | LINDO 0.00802826 | (i) gross | [0.007930218684615, 0.007930218899920] | margin LINDO 9.8e-05 (0.012 of \|d\|); slack 5e-09 |
| nd_netgen-2000-3-4-b-a-ns_7 | yes | p2 (primal) | 10729657.585 | 1.7e-05 | CPLEX 10729659.03; GUROBI 10729661.15 | (i) tolerance-scale | [10729657.58531, 10729657.58532] | margin CPLEX 1.44 (1.3e-07 of \|d\|), GUROBI 3.56 (3.3e-07 of \|d\|); slack 0.005 |
| nuclear14 |  | p3 (primal) | -1.1296874412 | 2.7e-11 | LINDO -1.12965944 | (i) gross | [-1.129687441173, -1.129687441170] | margin LINDO 2.8e-05 (2.5e-05 of \|d\|); slack 5e-09 |
| oil | yes | p2 (primal) | -0.93250816631 | 7.1e-11 | ANTIGONE -0.93249394; LINDO -0.93249394 | (iii) |  | active Jacobian rank 1391 < 1408 rows; margin at the listed point 1.4e-05..1.4e-05 vs slack 5e-09: (i) if an exact point exists near it |
| rsyn0815m04m | yes | p1 (primal) | 3410.854344 | 1.8e-11 | AOA 3410.8543 | (iii) |  | overdetermined: 802 active rows, 564 candidates; margin at the listed point 4.4e-05..4.4e-05 vs slack 5e-05: at most (i-r) |
| rsyn0820m03m | yes | p1 (primal) | 2028.8119408 | 8e-14 | AOA 2028.8119 | (iii) |  | overdetermined: 651 active rows, 453 candidates; margin at the listed point 4.1e-05..4.1e-05 vs slack 5e-05: at most (i-r) |
| rsyn0830m03m | yes | p1 (primal) | 1543.0593216 | 8.1e-14 | AOA 1543.0593 | (iii) |  | overdetermined: 768 active rows, 558 candidates; margin at the listed point 2.2e-05..2.2e-05 vs slack 5e-05: at most (i-r) |
| rsyn0830m04m | yes | p1 (primal) | 2529.0734109 | 8e-14 | AOA 2529.0734 | (iii) |  | overdetermined: 1029 active rows, 744 candidates; margin at the listed point 1.1e-05..1.1e-05 vs slack 5e-05: at most (i-r) |
| sepasequ_complex |  | p4 (other) | 368.76108835 | 2.9e-07 | ANTIGONE 368.7616151 | (iii) |  | overdetermined: 572 active rows, 435 candidates; margin at the listed point 0.00053..0.00053 vs slack 5e-08: (i) if an exact point exists near it |
| sepasequ_convent | yes | p2 (other) | 481.12033263 | 1.6e-08 | ANTIGONE 482.4997966; BARON 482.4997952; LINDO 482.4997971; SCIP 482.4996585 | (iii) |  | overdetermined: 801 active rows, 573 candidates; margin at the listed point 1.4..1.4 vs slack 5e-08: (i) if an exact point exists near it |
| smallinvDAXr1b150-165 | yes | p2 (primal) | 88.10493476 | 0 | LINDO 88.1049355 | (i) tolerance-scale | [88.10493476000, 88.10493476001] | margin LINDO 7.4e-07 (8.4e-09 of \|d\|); slack 5e-08 |
| smallinvDAXr1b200-220 | yes | p2 (primal) | 156.60426788 | 5e-15 | LINDO 156.604269 | (i) tolerance-scale | [156.6042678838, 156.6042678842] | margin LINDO 1.12e-06 (7.1e-09 of \|d\|); slack 5e-07 |
| smallinvDAXr2b150-165 | yes | p2 (primal) | 88.10493476 | 0 | LINDO 88.1049355 | (i) tolerance-scale | [88.10493476000, 88.10493476001] | margin LINDO 7.4e-07 (8.4e-09 of \|d\|); slack 5e-08 |
| smallinvDAXr2b200-220 | yes | p2 (primal) | 156.60426788 | 5e-15 | LINDO 156.604269 | (i) tolerance-scale | [156.6042678838, 156.6042678842] | margin LINDO 1.12e-06 (7.1e-09 of \|d\|); slack 5e-07 |
| spring |  | p3 (primal) | 0.84624410052 | 9.9e-09 | ANTIGONE 0.84624567; BARON 0.84624567; COUENNE 0.84624567; LINDO 0.84624567; SCIP 0.84624567 | (i-r) | [0.8462456656363, 0.8462456656500] | margin ANTIGONE 4.35e-09 (5.1e-09 of \|d\|), BARON 4.35e-09 (5.1e-09 of \|d\|), COUENNE 4.35e-09 (5.1e-09 of \|d\|), LINDO 4.35e-09 (5.1e-09 of \|d\|), SCIP 4.35e-09 (5.1 |
| spring |  | p2 (other) | 0.84622067122 | 4.9e-07 | ANTIGONE 0.84624567; BARON 0.84624567; COUENNE 0.84624567; LINDO 0.84624567; SCIP 0.84624567 | (i-r) | [0.8462456656363, 0.8462456656500] | margin ANTIGONE 4.35e-09 (5.1e-09 of \|d\|), BARON 4.35e-09 (5.1e-09 of \|d\|), COUENNE 4.35e-09 (5.1e-09 of \|d\|), LINDO 4.35e-09 (5.1e-09 of \|d\|), SCIP 4.35e-09 (5.1 |
| squfl010-040persp | yes | p2 (other) | 240.59672093 | 9e-07 | BARON 240.5985259; COUENNE 240.5983438; CPLEX 240.5985262; GUROBI 240.5985262; LINDO 240.5985262; SCIP 240.5970973 | (ii) repair | [240.5991756613, 240.5991756725] | exact repair not beyond the dual |
| squfl015-080persp | yes | p2 (other) | 402.4844708 | 9.8e-07 | BARON 402.4885296; COUENNE 402.4880496; CPLEX 402.48853; GUROBI 402.48853; LINDO 402.48853; SCIP 402.4848764 | (ii) repair | [402.4903506829, 402.4903507060] | exact repair not beyond the dual |
| squfl020-040persp | yes | p2 (other) | 209.25278479 | 9.6e-07 | BARON 209.2548899; COUENNE 209.2547119; CPLEX 209.2548902; GUROBI 209.2531361; LINDO 209.2548902; SCIP 209.2534062 | (ii) repair | [209.2557413515, 209.2557413615] | exact repair not beyond the dual |
| squfl020-050persp | yes | p2 (other) | 230.19860595 | 9.9e-07 | BARON 230.2021493; COUENNE 230.2018279; CPLEX 230.2021495; GUROBI 230.2021495; LINDO 230.2021495; SCIP 230.1992312 | (ii) repair | [230.2040215935, 230.2040216114] | exact repair not beyond the dual |
| squfl025-040persp | yes | p2 (other) | 197.33166003 | 1e-06 | BARON 197.333881; COUENNE 197.3336792; CPLEX 197.3338812; GUROBI 197.3317961; LINDO 197.3338812; SCIP 197.3319942 | (ii) repair | [197.3349298745, 197.3349298867] | exact repair not beyond the dual |
| squfl030-100persp | yes | p3 (other) | 363.08020962 | 9.5e-07 | BARON 363.093848; CPLEX 363.0938483; GUROBI 363.0938483; LINDO 363.0938483; SCIP 363.0855772 | (ii) repair | [363.0999757089, 363.0999757561] | exact repair not beyond the dual |
| squfl030-150persp | yes | p3 (other) | 430.56040493 | 1e-06 | CPLEX 430.5765549; GUROBI 430.5765549; LINDO 430.5765524; SCIP 430.5628306 | (ii) repair | [430.5842000868, 430.5842001648] | exact repair not beyond the dual |
| sssd20-04persp | yes | p3 (primal) | 347691.41048 | 5.2e-15 | LINDO 347716.8909 | (i) gross | [347691.4104835, 347691.4104845] | margin LINDO 25.5 (7.3e-05 of \|d\|); slack 5e-05 |
| sssd22-08persp | yes | p4 (primal) | 508713.73101 | 2.8e-15 | LINDO 508748.972 | (i) gross | [508713.7310104, 508713.7310120] | margin LINDO 35.2 (6.9e-05 of \|d\|); slack 0.0005 |
| sssd22-08persp | yes | p3 (primal) | 508719.49127 | 4e-12 | LINDO 508748.972 | (i) gross | [508719.4912727, 508719.4912742] | margin LINDO 29.5 (5.8e-05 of \|d\|); slack 0.0005 |
| sssd25-04persp | yes | p3 (primal) | 300176.56367 | 6.5e-15 | LINDO 300186.8048 | (i) gross | [300176.5636655, 300176.5636663] | margin LINDO 10.2 (3.4e-05 of \|d\|); slack 5e-05 |
| sssd25-08persp | yes | p4 (primal) | 472093.07797 | 7.2e-15 | LINDO 472098.947 | (i) gross | [472093.0779691, 472093.0779707] | margin LINDO 5.87 (1.2e-05 of \|d\|); slack 0.0005 |
| sssd25-08persp | yes | p3 (primal) | 472094.42418 | 9.4e-15 | LINDO 472098.947 | (i) gross | [472094.4241784, 472094.4241801] | margin LINDO 4.52 (9.6e-06 of \|d\|); slack 0.0005 |
| stockcycle |  | p2 (primal) | 119948.68833 | 0 | ANTIGONE 119949.; BARON 119949.; COUENNE 119949. | (i-r) | [119948.6883333, 119948.6883334] | margin ANTIGONE 0.312 (2.6e-06 of \|d\|), BARON 0.312 (2.6e-06 of \|d\|), COUENNE 0.312 (2.6e-06 of \|d\|); slack 0.5 |
| topopt-cantilever_60x40_50 |  | p5 (other) | 10.335458257 | 1.2e-07 | LINDO 35.35267044 | (i) gross | [10.33547432780, 10.33547432781] | margin LINDO 25 (0.71 of \|d\|); slack 5e-09 |
| topopt-cantilever_60x40_50 |  | p4 (other) | 13.077487872 | 2.3e-08 | LINDO 35.35267044 | (i) gross | [13.07748199152, 13.07748199153] | margin LINDO 22.3 (0.63 of \|d\|); slack 5e-09 |
| watercontamination0303 | yes | p2 (primal) | 207.9850348 | 5.2e-14 | BONMIN 207.9850352; LINDO 207.9850353 | (i) tolerance-scale | [207.9850348023, 207.9850348024] | margin BONMIN 3.98e-07 (1.9e-09 of \|d\|), LINDO 4.98e-07 (2.4e-09 of \|d\|); slack 5e-08 |

Notes on the (iii) rows:

- **Rounding-limited.** For cecil_13, hda, heatexch_spec2 and the four rsyn
  instances (AOA), the listed margin itself is within the rounding slack.
  These could at best become (i-r). They fail in the verifier because of
  degenerate active sets (more active rows than free variables, or dependent
  rows), or, for hda, a nonpolynomial active row over fixed variables that
  cannot be decided.
- **oil p2** (ANTIGONE and LINDO, −0.93249394; margin 1.4e-5).
  - The point is a primal-section point with violation 7e-11, and GUROBI
    lists exactly its value as its own dual bound.
  - It is very probably exactly repairable, which would give class (i).
  - The active equality system is rank deficient: 10 dependent equality rows
    after all reductions, most likely redundant pressure-drop relations of
    parallel identical pipes, since many pipe-speed variables share the value
    1.350091307554050. Krawczyk cannot handle dependent equalities.
- **ex7_3_5, ex8_2_1b, sepasequ_complex, sepasequ_convent.**
  - These are "other" points with violations 1.6e-8 to 1e-6.
  - ex7_3_5 is not solved; its five listed duals range from 1.20569526 to
    1.20687143. For ex8_2_1b, four solvers agree to 2e-6 and SCIP is lower.
    sepasequ_complex has only ANTIGONE's listed dual. For sepasequ_convent,
    ANTIGONE, BARON and LINDO agree to about 2e-6, and SCIP is lower by
    1.4e-4.
  - Newton did not converge (ex7_3_5), or the active set is degenerate
    (sepasequ). For ex8_2_1b, route C found a repaired point at −969.98,
    far above all duals, but could not verify one row.
  - These are probably tolerance effects, but unproven.

## 5. Per-solver summary

Counts are distinct (instance, solver) pairs with at least one flagged point.
The last column lists the class (i) results with their absolute margin d − f
and, in parentheses, (d − f)/|d|.

For scale, the pages list 11086 dual bounds under 19 solver labels. The
ten solvers with flagged pairs have: SCIP 1565, LINDO 1564, BARON 1485,
COUENNE 1451, ANTIGONE 1424, GUROBI 1073, SHOT 1011, CPLEX 389, BONMIN 348
and AOA 11. The other nine labels have no flagged pair: ALPHAECP 358,
XPRESS 316, PQCR 43, and six small labels with 48 dual bounds in total
(DynamicProgramming 21, Sven Mallach 17, Peter Hahn et.al. 7, Pajarito 1,
TRIVIAL 1, and a Gurobi run on a MISOCP reformulation, 1).

| solver | pairs | (i) gross | (i) tolerance-scale | (i-r) | (ii) proven | (ii) repair | (iii) | margins of (i): absolute (relative to \|d\|) |
|---|---|---|---|---|---|---|---|---|
| ANTIGONE | 15 | 1 | 0 | 3 | 0 | 4 | 7 | ghg_3veh 0.000318 (4.1e-05) |
| AOA | 4 | 0 | 0 | 0 | 0 | 0 | 4 |  |
| BARON | 21 | 1 | 0 | 2 | 4 | 10 | 4 | ghg_3veh 0.000318 (4.1e-05) |
| BONMIN | 1 | 0 | 1 | 0 | 0 | 0 | 0 | watercontamination0303 3.98e-07 (1.9e-09) |
| COUENNE | 15 | 1 | 0 | 3 | 0 | 9 | 2 | glider100 9.83e+05 (7.8e+02) |
| CPLEX | 9 | 0 | 1 | 0 | 0 | 8 | 0 | nd_netgen-2000-3-4-b-a-ns_7 1.44 (1.3e-07) |
| GUROBI | 10 | 0 | 1 | 0 | 0 | 9 | 0 | nd_netgen-2000-3-4-b-a-ns_7 3.56 (3.3e-07) |
| LINDO | 35 | 8 | 5 | 2 | 4 | 11 | 5 | glider100 9.83e+05 (7.8e+02); topopt-cantilever_60x40_50 25 (0.71); methanol50 9.8e-05 (0.012); sssd20-04persp 25.5 (7.3e-05); sssd22-08persp 35.2 (6.9e-05); sssd25-04persp 10.2 (3.4e-05); nuclear14 2.8e-05 (2.5e-05); sssd25-08persp 5.87 (1.2e-05); smallinvDAXr2b150-165 7.4e-07 (8.4e-09); smallinvDAXr1b150-165 7.4e-07 (8.4e-09); smallinvDAXr2b200-220 1.12e-06 (7.1e-09); smallinvDAXr1b200-220 1.12e-06 (7.1e-09); watercontamination0303 4.98e-07 (2.4e-09) |
| SCIP | 20 | 0 | 0 | 2 | 4 | 11 | 3 |  |
| SHOT | 1 | 0 | 0 | 0 | 0 | 1 | 0 |  |

What the numbers mean:

- **LINDO** has the most proven invalid bounds: 13 instances.
  - 8 are gross: glider100, topopt-cantilever_60x40_50, methanol50, four
    sssd*persp and nuclear14. Their margins run from 1.2e-5 of |d| up to a
    factor of 784. The margins of the four sssd*persp instances and of
    nuclear14 (1.2e-5 to 7.3e-5 of |d|) are below common relative gap
    tolerances of 1e-4 (Section 1).
  - 5 are tolerance-scale (four smallinvDAX, watercontamination0303), with
    margins of 2.4e-9 to 8.4e-9 of |d|.
  - In 6 of the 13, the listed dual equals, to all shown digits, the
    objective of a listed point: glider100 (p1), methanol50 (p3), and the
    four sssd*persp instances (p2). Each of these points is dated before
    LINDO's dual (by one day for glider100, two days for sssd*persp), except
    methanol50 p3, which has the same date as the dual (15 Feb 2022).
    *Inference, not verified:* LINDO reported a local solution as a dual
    bound. This agrees with the earlier diagnosis for methanol50.
  - In topopt-cantilever_60x40_50, the dual (2022) is 3.4 times the proven
    point, which comes from a 2025 listed point.
  - Together with rocket100/200/400
    (`reviews/wave2-small-verification/verification-report.md`), LINDO
    bounds on 16 instances are now proven invalid. The rocket cases are
    tolerance-scale, at about 1e-7.
- **ANTIGONE and BARON** (ghg_3veh, 2013/2014): both list 7.7543245, which
  is the objective of point p1 (7.75432451). *Inference, not verified:* both
  reported p1's value as a bound.
  - Point p2, added in 2015, is not exactly feasible as listed: route A
    finds row e1 off by 5e-14. It repairs (route B, Krawczyk) to an exactly
    feasible point with objective in [7.754006050048, 7.754006050065].
  - Both bounds are invalid by 3.18e-4, which is 4.1e-5 of |d|.
  - This is gross by this report's 1e-6 threshold, but below common relative
    gap tolerances of 1e-4, as the verifier notes. The same holds for the
    sssd*persp and nuclear14 pairs (Section 1).
  - The instance is not marked solved.
- **CPLEX and GUROBI** (nd_netgen, 2022): the bounds are invalid by 1.44
  and 3.56, which is 1.3e-7 and 3.3e-7 of |d| (tolerance-scale). GUROBI's
  bound equals the objective of point p1 (added 2018). The better point p2
  was added in July 2026.
- **COUENNE** (glider100): −1255.058601, which is p1's value. The same
  inference applies as for LINDO.
- **BONMIN** (watercontamination0303): invalid by 3.98e-7, which is 1.9e-9
  of |d| (tolerance-scale).
- **SCIP**: no class (i) results. Its two (i-r) results come from entries
  dated 17 Sep 2013: eniplac (a 6-digit value) and spring (8 digits).
  The five spring (i-r) solver-point pairs need not be solver errors:
  display rounding explains their listed conflict, while the underlying
  stored solver bounds are unknown. In the separate audit-ir recheck,
  SCIP 10 evaluated the spring proof point using bisection at its
  feasibility tolerance. The resulting objective difference is a numerical
  evaluation effect, not a conflict with the exact proof.
  - The SCIP 10.0.2 errors on waterno2 subproblems
    (`reviews/waterno2-verification/`) are not visible in the listed data.
  - MINLPLib's SCIP entries are for other versions and settings.
- **Tolerance effects** (class ii) involve eight of the ten solvers with
  flagged pairs; AOA and BONMIN have no class (ii) pair. The flagged
  conflicts are not evidence of solver errors, but the validity of the duals
  is proven only for emfl* (class (ii) proven, 12 pairs).
  - For the 63 (ii)-repair pairs (squfl*persp, hybriddynamic_*, alkyl, elf),
    an exactly feasible point near the flagged point is proven to exist, and
    its objective is not beyond any flagged dual. This is evidence, not
    proof, that those duals are valid.
  - The flagged points violate the constraints by 2e-10 (emfl050_3_3 p2)
    to 1e-6.
  - Examples of what such violations buy:
    - squfl*persp: 1e-6 in perspective constraints lowers the objective by
      1e-5 to 5.5e-5 relative to the exactly feasible repair;
    - emfl*: 1e-8 at cone apexes lowers it by up to about 1e-4 relative to
      the exact optimum.

## 6. Instances marked solved

- **Closing bounds proven invalid:** see the table in Section 1
  (nd_netgen-2000-3-4-b-a-ns_7, watercontamination0303, and the four
  smallinvDAX instances). All of them are tolerance-scale.
- **Within rounding:** eniplac (COUENNE, LINDO, SCIP; listed −132117.; an
  exactly feasible point has objective in [−132117.0830149, −132117.0830141])
  and lop97icx (ANTIGONE; listed 4099.06; the listed point, with objective
  in [4099.059953600, 4099.059953601], is exactly feasible as listed).
- **Solved with a listed optimal value below the exact optimum:**
  - emfl050_3_3: listed 10.40173793, exact optimum in
    [10.4017521316, 10.4017521319];
  - emfl100_5_5: listed 32.63818348, exact optimum in
    [32.6381903513, 32.6381903548].

  In both, every listed dual is valid. Only the listed primal value is not
  attained by any exactly feasible point. This is the same pattern as the
  earlier finding for camshape400/800.
- **Invalid but not closing:** sssd20-04persp, sssd22-08persp,
  sssd25-04persp and sssd25-08persp are solved. LINDO's bounds on them are
  invalid by gross margins of 5.87 to 35.2 (1.2e-5 to 7.3e-5 of |d|, below
  common relative gap tolerances of 1e-4). They are not closing bounds.

## 7. Caveats: what is proven and what is numerical

- **Proven** (under the assumptions below):
  - every class (i) and (i-r) result: the existence of an exactly feasible
    point with objective in the stated enclosure. "Gross" and
    "tolerance-scale" are size labels only; both kinds are proven;
  - the emfl lower and upper bounds;
  - the invalidity of each class (i) listed number;
  - the validity of each emfl listed dual.

  Independent code has confirmed all class (i) and (i-r) results and the
  emfl bounds (Section 8). Displayed enclosures and bounds are
  rounded outward (Section 1).
- **Assumptions:**
  - mpmath `iv` encloses exp, log, sqrt, sin, cos and integer powers
    correctly, and outward-rounds decimal strings;
  - numpy/BLAS double arithmetic is IEEE (the Krawczyk error terms hold for
    any summation order);
  - the exact-arithmetic scripts (`cert_*.py`, route A, the polynomial box
    checks) use Python `Fraction`.
- **Numerical, not proven:**
  - class (ii) repair: the repaired point is proven feasible, but that
    another exactly feasible point does not beat d is not proven;
  - every statement that a solver reported a local optimum, or a point's
    value, as a bound. These are inferences from equal listed numbers and
    are marked *Inference, not verified*;
  - the diagnoses for the (iii) cases.
- **Model identity.** The audit tests bounds against the current OSIL files
  in `~/.cache/minlplib/minlplib/osil`. A bound computed years ago on a
  different version of an instance (for example, before a reformulation)
  would show up here as invalid. The later
  [model-history check](../publication/minlplib-status/report.md) examined
  those histories. It found no substantive model change explaining the
  audited conflicts. Only three ghg_3veh constants changed by rounding;
  the old-text contradiction was re-proved.
  - The glider100 and ghg_3veh bounds date from 2013 to 2015. Their listed
    points date from 2011 (ghg_3veh p1) to 2022 (glider100 p2). The decisive
    points date from 2015 (ghg_3veh p2) and 2022 (glider100 p2).
  - The topopt LINDO bound dates from 2022, and its decisive points (p4, p5)
    from 2025.
  - Evidence, not proof, of an unchanged model: the older points behind the
    glider100 and ghg_3veh bounds satisfy the current files to about 1e-11
    (first verification), and the sssd*persp p2 points repair on the current
    files to objectives within the display slack of LINDO's numbers
    (recheck).
- **Rounding of listed duals.** Class (i) needs the margin to exceed the
  slack of the shown digits. If MINLPLib stored some bounds with fewer
  digits than it shows, the slack would be larger. The (i) margins are at
  least 7.9 times the slack in all cases but one (smallinvDAX*200-220:
  margin 1.1e-6, slack 5e-7, a factor of 2.2). The recheck found that all
  19 class (i) margins also exceed a full unit in the last shown digit (the
  smallest is 1.116 units, for smallinvDAX*200-220). So truncation instead
  of rounding would change no verdict.
- **Coverage.** Only pairs where a listed point beats a listed dual on the
  display are audited. Bounds that no listed point beats cannot be refuted
  from listed data. This includes all 3851 display ties, the single-solver
  closures of 186 unsolved instances, and rocket100/200/400, whose LINDO
  bounds were refuted with better points found by CONOPT. Finding such
  cases needs new primal points, which is outside this audit.
- **Degeneracy.** The generic verifier fails on degenerate mixed-integer
  points (dependent or too many active constraints). Class (iii) therefore
  mixes a likely-invalid bound (oil) with likely tolerance effects and with
  rounding-limited cases.
- **Size of class (i).** The 8 tolerance-scale pairs (1.9e-9 to 3.3e-7 of
  |d|) are exact-arithmetic violations below MINLPLib's 1e-6 relative gap
  convention (by a factor of 3 for nd_netgen GUROBI), and of the size of
  typical solver tolerances. The settings of these runs are not known. Seven
  of the 11 gross pairs (1.2e-5 to 7.3e-5 of |d|) are below common relative
  gap tolerances of 1e-4. Only the four pairs of glider100, topopt and
  methanol50 exceed such tolerances when the gap is measured against |d|.
  glider100 and topopt also have large absolute margins. methanol50 does
  not: its absolute margin is 9.8e-5, which is also its margin relative to
  max(1, |d|), just below 1e-4 (Section 1). *Judgment:* the tolerance-scale
  pairs should not be read as solver bugs of the same kind as those four.
- **glider100** is invalid for the discretized model as written. The
  exactly feasible point is physically spurious (Section 1).

## 8. Independent verification

The first two checks used code separate from this audit's. Neither changed
a class or a verdict. Later publication checks are in Section 8.4.

### 8.1 First verification

Report: `research-20260929/reviews/bound-audit-verification/verification-report.md`
(2026-09-30).

**Independence.** The verifier used separate code throughout:
- its own OSIL reader, with exact Fractions;
- its own interval arithmetic, with rational endpoints rounded outward to
  200 bits;
- its own Krawczyk test and its own exact certificates.

It re-fetched the OSIL files and points, which are byte-identical to the
ones used here.

**Checked and confirmed:**
- 14 of the 19 class (i) pairs:
  - ghg_3veh (ANTIGONE, BARON);
  - nd_netgen-2000-3-4-b-a-ns_7 (CPLEX, GUROBI);
  - watercontamination0303 (BONMIN, LINDO);
  - glider100 (COUENNE, LINDO);
  - topopt-cantilever_60x40_50 (LINDO);
  - methanol50, nuclear14, sssd20-04persp, smallinvDAXr1b150-165 and
    smallinvDAXr1b200-220 (all LINDO).
- The (ii)-proven claim for emfl050_3_3. Its optimum lies in
  [10.40175213184103, 10.40175213184476], inside the enclosure given in
  Section 6.
- The exact violation 1.70e-5 of nd_netgen p2, against the listed 1e-12.

**Differences, all consistent.** The verifier's repaired points differ from
the ones here; both are valid.
- nd_netgen: 10729657.585117233… with minimal u, against
  10729657.585310911… here.
- topopt p5: 10.335474275747004, against [10.33547432780, 10.33547432781]
  here.
- glider100: [−983842.2577883191, −983842.2577881224], against
  [−983842.2577737, −983842.2577716] here. The verifier fixed the altitude
  at node 1 at its bound 0; this audit's route C moved it to about 1e-10 m
  (Section 1).

**Recommendations adopted after this check:**
- report gross errors and tolerance-scale violations separately;
- give margins relative to |d| as well as absolute;
- label inferences about solver behaviour;
- add the characterization of the glider100 point.

The verifier also suggested the more neutral label "consistent with
rounding" for class (i-r). The label is kept here, and its meaning is stated
in Section 3.3.

### 8.2 Recheck

Report: `research-20260929/reviews/bound-audit-recheck.md` (2026-09-30), with
code, data and logs in `research-20260929/reviews/bound-audit-recheck/`.

**Independence.** The recheck used its own OSiL reader and exact evaluator
(Python Fractions). It did not use this audit's code or `osilx.py`, the
reader this audit uses. It used the first verifier's reader only as a
cross-check. All its certificates are exact rational checks of every row,
bound and integrality condition; it needed no interval arithmetic. Its
fetched OSIL files and points are byte-identical to the ones used here.

**Checked and confirmed:**
- The other 5 class (i) pairs (7 points), all LINDO: sssd22-08persp (p3,
  p4), sssd25-04persp (p3) and sssd25-08persp (p3, p4), which are gross,
  and smallinvDAXr2b150-165 and smallinvDAXr2b200-220, which are
  tolerance-scale. Each exactly feasible objective it built lies inside the
  enclosure given here, and the gross / tolerance-scale labels hold.
- The two-sided bounds of emfl050_5_5, emfl100_3_3 and emfl100_5_5, with
  emfl050_3_3 as a control. Each of its intervals lies inside this audit's
  enclosure of the optimum (from `logs/cert_socp_*.json`, rounded outward):
  - emfl050_5_5: [18.9136329557291, 18.9136329557624], inside
    [18.9136329529, 18.9136329563];
  - emfl100_3_3: [18.1326531242336, 18.1326531242359], inside
    [18.1326531194, 18.1326531244];
  - emfl100_5_5: [32.6381903545115, 32.6381903545301], inside
    [32.6381903513, 32.6381903548] (Section 6).

  So every emfl listed dual is valid, and all 12 (ii)-proven pairs hold.
- The numbers of this report, recomputed with its own scripts from
  `results.json`, `results.csv` and `pages.json`: the class counts, margins,
  split rules, histogram, per-solver table, closing flags and screen counts.
  It found no numerical mismatch.

**Additional finding.** In emfl050_5_5, emfl100_3_3 and emfl100_5_5, every
listed point lies below the exact optimum, and in emfl050_3_3 every listed
point except p3 does. I confirmed this against the lower bounds proven here
and added it to Section 1.

**Text problems.** The recheck reported nine problems in the text, none of
which changes a class or verdict. Section 10 lists how each was handled.

### 8.3 Scope left by the first two reviews (historical)

The following gaps describe those reviews at their dates. Section 8.4
supersedes the (i-r), parsing and model-history gaps.

- The class (i-r), (ii)-repair and (iii) rows. The (i-r) results rest on
  this audit's code only.
- The parsing of the 1633 pages. The recheck recomputed the counts from
  `pages.json` and compared the nine pages it fetched, but did not re-parse
  the pages.
- Instance change histories (Section 7, Model identity).

### 8.4 Publication checks integrated on 2026-10-03

The [audit-ir report](../publication/audit-ir/report.md), checked by an
[independent reviewer, round 1](../publication/reviews/audit-ir-review-r1.md),
re-proves all 12 class (i-r) pairs with exact rational arithmetic. It also
re-parses the stored pages and independently reproduces the screen and ties.
The four instances are eniplac (three solvers), lop97icx (one), spring
(five) and stockcycle (three). Spring's exact global optimum rounds to all
five listed duals, so display rounding explains the listed conflicts; the
underlying solver bounds remain unknown. The other seven entries could
reflect earlier rounding to six significant digits, but that is evidence,
not a proved account of the solver computations. No classification changes.

The [status/model-history report](../publication/minlplib-status/report.md)
and [round-2 review](../publication/reviews/minlplib-status-review-r2.md)
find the relevant bounds, points, solved marks and OSIL files unchanged at
the 2026-10-02 refresh. Archived listings support model identity for the
audited past bounds. The old ghg_3veh model differs in three rounded
constants; the invalidity proof holds there too. glider100 is unchanged;
complete pre-bound copies support topopt identity, while its later archived
copy is truncated. Some earlier archive windows are absent, so model
history is not established by a continuous chain of archived copies.
The certificates use exact OSIL coefficients; small GAMS/OSIL differences
are recorded in the report. Its current Table B1 supersedes the older
Table B1 in its data/tables.md.

The [SCIP finding](../publication/scip-bug/report.md), independently
[verified in round 1](../publication/reviews/scip-bug-review-r1.md), supplies
exactly feasible witnesses against wrong optimality claims on the waterno2
period and cell-pair models. In instrumented wrong runs, fixed-bound cubic
equalities suffer a binary64 residual and the default nonlinear handler's
reverse propagation cuts off the feasible witness. The trace supports that
mechanism on those runs; it does not diagnose unrelated historical bounds.
The upstream report and minimized reproducer are prepared. **The report
is drafted and has NOT been submitted; filing remains the user's decision.**

The [reproduction guide](../publication/reproduction/README.md) and
[package report](../publication/reproduction/report.md) map each audit
classification to scripts and saved evidence. The topopt p5 objective
numbers in this report use the committed certificate. Regeneration with
one BLAS thread selects a different exactly feasible point because the
pivoted QR basis depends on numerical settings; the guide explains the
resulting display-check differences. This is a replay/regeneration limit
and changes no classification or invalidity conclusion.

The latest review verdicts, responses and limits are recorded in
[publication/READINESS.md](../publication/READINESS.md). Older revision
records below describe the verification status at their own dates.

## 9. Files, commands and run status

**Data:**

| file | content |
|---|---|
| `pages/` | instance pages, `instances.html` and `minlplib.solu` (fetched 2026-09-30) |
| `pages.json` | parsed pages |
| `sol/` | the 56 downloaded points |
| `screen.json` | the 158 flagged pairs and the 3851 display ties |
| `logs/eval/*.json` | high-precision evaluations |
| `logs/verify/*.json` | verification results |
| `logs/verify/*.center.sol` | proof-box centres |
| `logs/cert_*.json` | dedicated certificates |
| `results.json`, `results.csv` | the classified pairs |
| `summary.json`, `logs/summary.txt`, `logs/tables.md` | summaries |
| `logs/verify_run1*`, `logs/verify_run2*`, `logs/verify_run3*` | earlier verifier runs, superseded; the results agree with the final run |
| `logs/verify_big/` | topopt logs |

**Code:**

| file | role |
|---|---|
| `fetch_pages.py`, `parse_pages.py` | data collection |
| `audit.py` | screen, download, evaluate, verify, classify |
| `audit_eval.py` | 40-digit evaluator |
| `verify.py`, `verify_one.py` | routes A, B and C |
| `cert_linear.py`, `cert_ndnetgen.py`, `cert_socp.py`, `cert_topopt.py` | dedicated certificates |
| `summarize.py`, `make_tables.py` | summaries and tables |
| `check_display.py` | checks the rigorous displays in this report against the exact values: each "[lo, hi]" must enclose its intended quantity (nearest lower end), each "…" value must be a truncation of an exact value, each emfl "opt >=" or "≥" bound must hold, and so must the two emfl "at least" differences (Section 10.2) |
| `sanity.py` | negative controls |

**Commands** (targeted checks only; no project-wide verification, no CI):

```
python3 fetch_pages.py                 # 1633 pages, sequential, 1 s delay (53 min)
python3 parse_pages.py
python3 audit.py screen
python3 audit.py download              # 56 points, sequential, 1 s delay
python3 audit.py evaluate --jobs 3
python3 audit.py verify --jobs 2       # timeout 3600 s per point (final run; earlier runs used 3 jobs)
python3 cert_linear.py watercontamination0303.p2
python3 cert_ndnetgen.py nd_netgen-2000-3-4-b-a-ns_7.p2
python3 cert_socp.py emfl050_3_3 emfl050_3_3.p2 emfl050_3_3.p4 emfl050_3_3.p5
python3 cert_socp.py emfl050_5_5 emfl050_5_5.p4 emfl050_5_5.p5 emfl050_5_5.p6
python3 cert_socp.py emfl100_3_3 emfl100_3_3.p3 emfl100_3_3.p4
python3 cert_socp.py emfl100_5_5 emfl100_5_5.p2
python3 cert_topopt.py topopt-cantilever_60x40_50.p4   # about 90 s each
python3 cert_topopt.py topopt-cantilever_60x40_50.p5
python3 sanity.py
python3 audit.py classify && python3 summarize.py > logs/summary.txt && python3 make_tables.py > logs/tables.md
python3 check_display.py               # after editing this report
```

**Run status.**

- All runs finished.
- The final verification run reproduced the statuses and enclosures of the
  earlier runs to 1e-9 relative. The earlier runs are kept in
  `logs/verify_run1*`, `logs/verify_run2*` and `logs/verify_run3*`.
- A generic route-C run on topopt (`verify_one.py
  topopt-cantilever_60x40_50.p4 --max-n 8000 --route-c-only`) was stopped
  after about an hour. Its direction LP (HiGHS, 31200 variables) did not
  finish on the loaded machine. `cert_topopt.py` replaced it.
- Limits and load: 3600 s per point in `audit.py verify` and 5400 s for the
  topopt certificates. Jobs ran at nice 5 or with at most 3 processes.
- After the recheck, only the classification and tables were rerun
  (Section 10.1). After confirmation rounds 1 and 2, only
  `check_display.py` was rerun (Sections 10.2 and 10.3). No verification or
  certificate was rerun.

## 10. Revision after review

### 10.1 Recheck (2026-09-30)

Check report: `research-20260929/reviews/bound-audit-recheck.md`, verdict
"fixes needed". I verified each issue myself before changing the text. All
nine were correct. No class, count, margin or verdict changed.

1. **ghg_3veh p2 called "exactly feasible" (Section 5).**
   - Verified: `logs/verify/ghg_3veh.p2.json` records route A failing on row
     e1 by 5e-14. The result is proved by route B, with enclosure
     [7.75400605004881, 7.75400605006433] (rounded outward at 14
     decimals).
   - Change: Section 5 now says that p2 is not exactly feasible as listed
     and that it repairs to an exactly feasible point.
   - The recheck's suggested interval, [7.754006050049, 7.754006050064], is
     itself rounded inward. The text uses the outward-rounded
     [7.754006050048, 7.754006050065].
   - Section 3.4 now says the control verifies "through route B".
2. **"Tolerance effects (class ii) involve every solver, and they are not
   errors" (Section 5).**
   - Verified from `summary.json`: class (ii) pairs occur for ANTIGONE,
     BARON, COUENNE, CPLEX, GUROBI, LINDO, SCIP and SHOT. AOA and BONMIN
     have none.
   - Change: the bullet now says eight of ten solvers (made precise in
     Section 10.2, item 2). It says that the conflicts are not evidence of
     errors, that validity is proven only for emfl*, and that (ii)-repair is
     evidence only.
   - Found while checking (from `results.json`): the stated violation range
     "1e-8 to 1e-6" was wrong. The (ii) points have violations from 2e-10
     (emfl050_3_3 p2) to 1e-6.
   - Also found: the squfl*persp drop "about 1e-5 relative" is 1e-5 to
     5.5e-5 relative to the repaired point. Both are corrected.
3. **methanol50 p3 called an "earlier" point (Section 5, LINDO).**
   - Verified in `pages.json`: p3 and LINDO's dual are both dated 15 Feb
     2022. The other five points are earlier:
     - glider100 p1: 15 Aug 2014, against LINDO's 16 Aug 2014;
     - sssd*persp p2: 28 Feb 2014, against 02 Mar 2014.
   - Change: the text now says "a listed point" and gives the dates.
4. **Point dates in Section 7.**
   - Verified in `pages.json`:
     - ghg_3veh p1: 29 Aug 2011; p2: 06 Mar 2015;
     - glider100 p1: 15 Aug 2014; p2: 16 Mar 2022;
     - the bounds date from 26 Sep 2013 to 25 Jun 2015.
   - Change: the text now says "listed points 2011–2022; decisive points
     2015 and 2022".
5. **Displayed enclosures rounded to nearest, not outward.**
   - Verified: at 13 significant digits, round-to-nearest moved upper ends
     inward by up to 9.1e-7 (nd_netgen), and some lower ends inward too.
     Section 6 showed emfl100_5_5 as [32.6381903514, 32.6381903547] against
     the proven [32.638190351378666…, 32.63819035472937] (upper end to
     double precision). The Section 1 value
     88.10493476 for smallinvDAX*150-165 was 6e-15 below the listed point's
     exact objective, 88.104934760000006.
   - Found while checking: `results.json` stored `rigorous_opt_lower` as
     `float(L)`, which rounds to nearest. For emfl100_3_3 and emfl100_5_5
     that float is 1.1e-15 and 3.9e-15 above the exact bound. Classification
     already used the exact rational, so no class depended on it.
   - Changes:
     - `audit.py classify` now stores the exact bound rounded down at 30
       decimals.
     - `make_tables.py` rounds enclosure ends and bounds outward.
     - I reran `audit.py classify`, `summarize.py` and `make_tables.py`,
       and replaced the Section 4 table with the new `logs/tables.md`.
     - I set the displays in Sections 1, 5, 6 and 8 by hand. The two
       emfl differences now read "at least 1.42e-5" and "at least
       6.87e-6".
     - Section 1 states the display convention. Margins, ratios and point
       values stay rounded to nearest as sizes.
   - Checks:
     - Compared with the previous outputs (kept in `/tmp` during the run),
       only `rigorous_opt_lower` changed in `results.json`.
     - `results.csv`, `summary.json` and `logs/summary.txt` are
       byte-identical.
     - `logs/tables.md` differs only in the rounding direction of enclosure
       ends and bounds.
     - The first version of `check_display.py` tested each "[lo, hi]" and
       each emfl "opt >=" or "≥" bound shown in this report. All 68 displays
       of this audit's own enclosures and bounds passed. The script listed
       seven intervals as not enclosing, and each is a quotation:
       - five come from the reviews: the reviews' tighter emfl intervals,
         which lie inside the ones here, and the verifier's different
         glider100 repair;
       - two are old inward-rounded displays: the ghg_3veh interval quoted
         in item 1 (also the recheck's suggestion) and the emfl100_5_5
         interval quoted in this item.
     - That version was weaker than first described here: it accepted an
       interval that enclosed any audit quantity, not only the intended
       one, and it did not test "…" values or "at least" statements.
       Section 10.2, item 4, replaces it with a stricter version.
6. **The ghg_3veh caveat applies to seven gross pairs.**
   - Verified from `results.json`: sssd ×4, nuclear14 and ghg_3veh ×2 have
     (d − f)/|d| from 1.2e-5 to 7.3e-5, all below 1e-4.
   - Change: the caveat is now stated in Section 1 (after the gross table),
     Section 5 (LINDO; ANTIGONE and BARON), Section 6 and Section 7.
     Section 1 names the four pairs with the largest margins relative to
     |d|: glider100 ×2, topopt-cantilever_60x40_50 and methanol50. (The
     wording "errors by any common tolerance" used here was too strong for
     methanol50; see Section 10.2, item 1.)
7. **"Far below MINLPLib's 1e-6 … below the tolerances with which solvers
   compute bounds" (Section 1).**
   - Verified: 1e-6 is 3.0 times the nd_netgen GUROBI margin (3.3e-7 of
     |d|), 7.4 times the CPLEX margin, and at least 119 times each of the
     others. The solver settings are not on the pages.
   - Change: the Section 1 table row, the bullets below the
     tolerance-scale table, and Section 7 now say "below the 1e-6
     convention, and of the size of typical solver tolerances". They give
     the factors and state that the settings are unknown. Reading these
     pairs as non-errors is labelled as a judgment.
8. **glider100 altitude (Section 1).**
   - Verified from `sol/glider100.p2.sol` and the OSIL file:
     - x103 is fixed at 1000;
     - x104 is absent from the point, so it is 0, on its default lower
       bound 0;
     - x105 = 1719.5;
     - the block reaches 64580 m at node 55 and ends at x203 = 900.
   - This audit's own proof-box centre has x104 = 1.0e-10. Route C shifted
     the point by t = 1.75e-10 (`logs/verify/glider100.p2.json`).
   - Change: Section 1 now says that the altitude first drops to 0 at node
     1. It states the value at node 1 in the listed point, in the verifier's
     repair, and in this audit's repair. Section 8.1 adds the same note.
9. **Header, Section 1 (Rigor) and Section 8 out of date.**
   - Change:
     - The header now has a status table for both checks.
     - Rigor states that all 19 class (i) pairs and the four emfl
       (ii)-proven results are confirmed independently, and that (i-r) is
       not.
     - Section 8 is split into the first verification (8.1), the recheck
       (8.2) and what neither covered (8.3).
     - Section 7 uses the recheck's result that all 19 margins exceed a
       full display unit, and its sssd p2 evidence on model identity.

**Added from the recheck, after my own check.** In emfl050_5_5, emfl100_3_3
and emfl100_5_5, every listed point value lies below the exact optimum. In
emfl050_3_3, every listed point except p3 does. I confirmed this by
comparing each displayed value, plus half a unit in its last digit, with the
exact lower bounds in `logs/cert_socp_*.json`. It is now in Section 1.

**Targeted commands run for this revision** (single-threaded,
OMP_NUM_THREADS=1; each finished in seconds). No project-wide verification
was run, and CI was not inspected.

```
python3 audit.py classify
python3 summarize.py > logs/summary.txt
python3 make_tables.py > logs/tables.md
python3 check_display.py
# plus read-only inspection of pages.json, results.json, summary.json,
# logs/verify/{ghg_3veh,glider100}.p2.json, logs/cert_socp_*.json,
# sol/glider100.p2.sol and logs/verify/glider100.p2.center.sol
```

No verification route, certificate or download was rerun. The recheck's own
certificates were not rerun here; their results are cited from its report.

### 10.2 Confirmation check, round 1 (2026-09-30)

Check report: `research-20260929/reviews/recheck-audit-confirm.md`. It found
the nine fixes of Section 10.1 correct and listed eight remaining text
problems. I verified each one myself before changing the text. All eight
were correct. No class, count, margin or verdict changed, and no data file
changed.

1. **"Clear errors by any common tolerance" (Sections 1 and 7).**
   - Verified from `results.json` with exact fractions: for methanol50,
     d − f = 9.804e-5, (d − f)/|d| = 1.22e-2, and (d − f)/max(1, |d|) =
     9.804e-5, below 1e-4. glider100 (d − f = 982587) and topopt (25.02)
     have large margins by every measure.
   - Change: Section 1 now calls the four pairs clear errors under relative
     gap tolerances measured against |d|. It gives methanol50's absolute
     margin and its margin relative to max(1, |d|). Section 7 says the same,
     and Section 10.1, item 6, marks the old wording.
2. **"Eight of the ten solvers" and the "For scale" line (Section 5).**
   - Verified from `pages.json`: 11086 dual bounds under 19 solver labels.
     The ten labels with flagged pairs (the solvers in `results.json`) hold
     10321. The other nine labels hold 765: ALPHAECP 358, XPRESS 316, PQCR
     43, and six small labels with 48 in total. None of the nine has a
     flagged pair.
   - Change: Section 5 now says "eight of the ten solvers with flagged
     pairs", and the "For scale" line lists all 19 labels.
3. **Two "…" values were rounded, not truncated.**
   - Verified: the ghg_3veh upper end in `logs/verify/ghg_3veh.p2.json`
     begins 7.7540060500643257, so the old display (ending 433) was rounded
     up. The first verifier's nd_netgen value is the fraction in
     `reviews/bound-audit-verification/logs/nd_netgen_exact.log`. Its
     decimal expansion begins 10729657.585117233985, so the old display
     (ending 234) was rounded too.
   - Change: Section 8.1 now shows the verifier's value truncated. Section
     10.1, item 1, now shows the ghg_3veh enclosure rounded outward, without
     "…", like the other enclosures in this report:
     [7.75400605004881, 7.75400605006433]. I did not use the suggested
     truncation 7.75400605006432…, because a truncated upper end of an
     enclosure lies below the exact end.
   - The new `check_display.py` (item 4) tests every "…" value in this
     report. It found no other rounded one.
4. **`check_display.py` was weaker than described (Sections 9 and 10.1,
   item 5).**
   - Verified by reading and running the script. It accepted an interval
     that enclosed any audit quantity, not only the intended one. It did not
     test "…" values or "at least" statements. For the last histogram row
     of Section 1, it printed a "lower bound not matched" line, which the
     report did not mention.
   - Change: I made the script stricter, so that its description is true:
     - each "[lo, hi]" must enclose its intended quantity, the exact
       enclosure whose lower end is nearest to lo;
     - each value ending in "…" must be a truncation of an exact audit
       value;
     - the two emfl "at least" differences are checked against the exact
       lower bounds;
     - that histogram row is reported as skipped.

     Section 9 and Section 10.1, item 5, now say what the new and the first
     version check. Margins, ratios and other "at least" statements are
     sizes and are still not checked by the script.
   - Checks:
     - On the report before this revision, the new version passes the same
       68 displays as the first version and fails the same seven
       quotations. It also passes 7 "…" values and both "at least"
       differences, and it flags exactly the two rounded values of item 3.
     - Negative control, on a modified copy of the report in `/tmp`: an
       sssd22-08persp p4 interval widened to enclose p3 but not p4 fails,
       and so does a false "at least 1.43e-5" for emfl050_3_3. The first
       version accepted both.
     - On this revised report: ok 84, failed 8, skipped 1. The eight
       failures are quotations: the seven intervals listed in Section 10.1,
       item 5, and the first verifier's nd_netgen value in Section 8.1,
       which is not an audit value. I checked that value by hand (item 3).
     - The confirmation's own script
       (`reviews/recheck-audit-confirm-checks/check_displays_indep.py`, run
       read-only with its output in `/tmp`) also passes every display of
       this audit's own results. Its failures are the same quotations, plus
       the Section 10.1, item 5, quotation of the emfl100_5_5 bounds, whose
       upper end is labelled as given to double precision.
5. **Primal-section violation range (Section 1, emfl bullet).**
   - Verified from `pages.json` and `logs/cert_socp_*.json`: the emfl
     primal-section points with listed violation below 1e-8 that lie below
     the exact optimum have listed violations from 4e-11 to 8e-10.
     (emfl050_3_3 p3, a primal-section point listed at 3e-11, lies above
     the proven upper bound, so it is not in this range.) emfl050_5_5 p2
     (listed 8e-10) lies at least 2.25e-4 below the exact lower bound, even
     after adding half a unit in its last displayed digit. The qualifier
     "that lie below the exact optimum" was added after confirmation round
     2 (Section 10.3, item 2).
   - Change: the range is now 4e-11 to 8e-10, with emfl050_5_5 p2 as a
     second example.
6. **"The five sssd*persp and nuclear14 margins" (Section 5, LINDO).**
   - Verified from `results.json`: four sssd*persp instances (sssd20-04,
     sssd22-08, sssd25-04, sssd25-08) plus nuclear14 give five margins, from
     1.2e-5 to 7.3e-5 of |d|.
   - Change: the text now says "the margins of the four sssd*persp
     instances and of nuclear14".
7. **Section 8.2, "inside the enclosure given here".**
   - Verified: the report showed only lower bounds for emfl050_5_5 and
     emfl100_3_3. From `logs/cert_socp_*.json`, the outward-rounded
     enclosures are [18.9136329529, 18.9136329563] and
     [18.1326531194, 18.1326531244]. The stored upper bounds are doubles
     (`cert_socp.py` writes `float(ub)`), within 2e-15 of the exact values,
     so the rounded-up tenth decimals hold. The recheck's intervals lie
     inside both.
   - Change: Section 8.2 now cites the logs and shows all three enclosures
     next to the recheck's intervals. Section 8.1 now points to Section 6
     for the emfl050_3_3 enclosure.
8. **"Quoted in this item" (Section 10.1, item 5).**
   - Verified: the old ghg_3veh display is quoted in item 1, where it is
     also the recheck's suggestion. Only the emfl100_5_5 display is quoted
     in item 5.
   - Change: item 5 now names both displays and where each is quoted.

The header now has a status row for this check, and Section 9 records that
only `check_display.py` was rerun.

**Targeted commands run for this revision** (single-threaded,
OMP_NUM_THREADS=1; each finished in seconds). No project-wide verification
was run, and CI was not inspected.

```
python3 check_display.py        # before and after the text changes
python3 ../reviews/recheck-audit-confirm-checks/check_displays_indep.py > /tmp/bound-audit-round1/indep.log
# negative control: new and first check_display.py on a modified copy of this report in /tmp
# plus read-only inspection, with short exact-fraction snippets, of pages.json,
# results.json, logs/verify/ghg_3veh.p2.json, logs/cert_socp_*.json, cert_socp.py
# and reviews/bound-audit-verification/logs/nd_netgen_exact.log
```

No classification, table, verification route, certificate or download was
rerun, because no data changed.

### 10.3 Confirmation check, round 2 (2026-09-30)

Check report: `research-20260929/reviews/audit-confirm-r1.md` (titled
"Confirmation check, round 2"). It found the eight fixes of Section 10.2
correct and listed two wording problems. I verified both myself before
changing the text. Both were correct. No number, class, count, margin or
verdict changed, and no code or data file changed.

1. **The status line overstated the third check (header).**
   - Verified: the header said "a third check confirmed the revised text",
     but `reviews/recheck-audit-confirm.md` gives the verdict "fixes needed".
     It confirmed the nine fixes of Section 10.1 and the outward rounding of
     the displays, and it listed eight text problems (Section 10.2). The
     status table row already said this.
   - Change: the status line now says that the third check confirmed the
     fixes made after the second and found eight text problems, fixed in
     Section 10.2. It also records this fourth check and its two problems.
     The status table has a row for this check, and Section 9 records that
     only `check_display.py` was rerun.
2. **The violation range in Section 10.2, item 5, lacked its qualifier.**
   - Verified from `pages.json` and `logs/cert_socp_*.json`, adding or
     subtracting half a unit in the last shown digit of each listed value:
     the emfl primal-section points with listed violation below 1e-8 are
     emfl050_3_3 p1 (1e-10), p2 (2e-10) and p3 (3e-11); emfl050_5_5 p1
     (1e-10), p2 (8e-10) and p3 (4e-11); emfl100_3_3 p1 (1e-10) and p2
     (2e-10); and emfl100_5_5 p1 (1e-10). All lie below the exact lower
     bound except emfl050_3_3 p3, which lies at least 4.9e-5 above the
     proven upper bound. So the range is 3e-11 to 8e-10 over all of them,
     and 4e-11 to 8e-10 over those below the exact optimum.
   - Section 1 was already correct: its range follows "This includes", so
     it refers to the points below the exact optimum.
   - Change: Section 10.2, item 5, now says "that lie below the exact
     optimum" and names emfl050_3_3 p3 as the exception.

**Targeted commands run for this revision** (single-threaded,
OMP_NUM_THREADS=1; each finished in seconds). No project-wide verification
was run, and CI was not inspected.

```
python3 check_display.py        # before and after the text changes: ok 84, failed 8, skipped 1
# plus a short read-only script comparing each emfl listed point in pages.json
# (value ± half a unit in its last shown digit) with the exact L and U in
# logs/cert_socp_*.json
```

No classification, table, verification route, certificate or download was
rerun, because no data changed.

*Root edit (2026-09-30, closing revision):* the header and its table now
record the round-3 confirmation (`reviews/audit-confirm-r2.md`, verdict
"verified", no remaining problem). No other text changed.

### 10.4 Publication integration (2026-10-03)

Applied the owned exact replacements from the minor-fixes integration list:
page precision and entry-count definitions, the conservative slack floor,
and the spring rounding qualifier. Corrected the emfl050_3_3 relative
"at least" display by exact rational arithmetic. Added the independent
(i-r) proofs, parsing and screening checks, status/model-history refresh,
SCIP bug evidence and committed-certificate reproduction limit. No data,
classification, margin or solver result was regenerated.

Targeted integration commands and their results are recorded in
[../publication/integration/commands.md](../publication/integration/commands.md).
The exact checks read saved data without importing scientific scripts.
No project-wide verification or CI inspection was performed; no commit,
push or outside contact was made.
