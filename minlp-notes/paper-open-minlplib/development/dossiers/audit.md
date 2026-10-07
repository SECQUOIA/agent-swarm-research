# Dossier: systematic audit of MINLPLib listed per-solver dual bounds (family key `audit`)

Prepared 2026-10-04 (second pass; it supersedes the first pass of the same
day, whose checks remain in `checks/audit/`). `R/` means `research-20260929/`.
The checks run for this pass are in `checks/audit-r2/` (scripts, logs and a
README with inputs and commands). Everything ran on copies in `/tmp`; nothing
was imported or executed inside `R/`, nothing under `R/` or `literature/` was
edited, and nothing was committed.

## 0. Summary

- **Population.** On 2026-09-30 the audit fetched all 1633 MINLPLib instance
  pages (site footer "Last updated 2026-09-14"). They display 2816 solution
  points and 11086 per-solver dual bounds (11031 finite) under 19 solver
  labels. A refresh on 2026-10-02 found the 69 relevant instances unchanged.
- **Screen.** In 158 (bound, point) pairs, on 46 instances, 56 points and 131
  (instance, solver) pairs, the displayed bound lies strictly beyond the
  displayed objective of a listed point with listed violation at most 1e-5.
  A further 3851 pairs (1133 instances) are display ties that the listing
  cannot decide.
- **Main result (class (i)).** For 19 per-solver bounds on 15 instances, an
  exactly feasible point of the instance (OSIL file, decimals read as exact
  rationals) has objective value better than the bound by at least 1.116
  units in the bound's last displayed digit. So neither the displayed number
  nor any number that rounds or truncates to it is a valid dual bound.
  - 11 margins exceed 1e-6·|d| ("gross"); 4 exceed 1e-2·|d|: glider100
    (COUENNE, LINDO), topopt-cantilever_60x40_50 (LINDO), methanol50 (LINDO).
  - 8 margins lie between 1.9e-9·|d| and 3.3e-7·|d| ("tolerance-scale").
  - Each of the 19 was confirmed by a second, independently written
    implementation (first verifier: 14 pairs; recheck: 5 pairs).
- **Outside the screen.** LINDO's bounds on rocket100/200/400 are invalid by
  at least 1.069e-7, 4.706e-8 and 1.894e-7 (1.06, 4.70 and 18.9 display
  units, rounded down). **New in this pass:** a second, independent rigorous
  implementation reproduces all three enclosures (Section 6,
  `checks/audit-r2/`).
- **Other results.** All 12 class (i-r) pairs (4 instances) were re-proved
  exactly; the spring global optimum is proved and its 8-decimal rounding is
  the five displayed bounds. For the four emfl SOCP instances every listed
  dual is proved valid, the optima are enclosed to within 3.4e-11, and the
  listed primal values lie below the exact optimum.
- **MINLPLib's aggregate dual is never invalidated beyond display rounding**
  in this family. Its `.solu` `=bestdual=` equals min(third-best per-solver
  bound, lowest listed point value) in 585 of 589 cases (a data-based
  reading, reproduced in both passes).
- **Model form, new in this pass.** An exact comparison shows that the
  `.gms` text and the OSIL file define the same model (every row, the
  objective, and every variable name, type and bound) for 14 of the 15 class
  (i) instances, for rocket100/200/400, for the four emfl instances and for
  the (i-r) instances spring and eniplac. methanol50 differs only in 360
  objective coefficients (relative change at most 2.38e-16), and its verdict
  was already proved on both forms.
- **Verdict.** I found nothing that invalidates a claimed result. The open
  points concern wording, two non-replayable certificate records, coverage,
  the novelty search, and an independent review of this pass's two new
  checks (Section 8).

## 1. Instances and models

### 1.1 Population and data

- **Pages.** `R/bound-audit/pages/` holds the 1633 instance pages (cut before
  the GAMS listing), `instances.html` and `minlplib.solu`, fetched
  sequentially on 2026-09-30. `R/bound-audit/pages.json` is the parse.
  - Senses: 1366 min, 264 max; camcns, gancns and korcns have no objective
    and are skipped.
  - `fct` has a page but no OSIL file; it is in no flagged pair.
  - The parse was re-done independently twice (audit-ir author and its
    reviewer): 0 differences over 2816 points, 11086 bounds and 11431
    listing fields.
- **Models.** The 1632 OSIL files in `~/.cache/minlplib/minlplib/osil`,
  byte-identical to the live files (checked by both verifiers and the status
  track). Every decimal constant is read as the exact rational it denotes.
- **Points.** The 56 screened points are the MINLPLib `.sol` files in
  `R/bound-audit/sol/`. As MINLPLib specifies, a variable missing from a
  `.sol` file is 0; the `objvar` entry is ignored when the OSIL form has
  eliminated the objective variable.
- **MINLPLib conventions** (stored `instances.html`, `doc.html`; literature
  slugs `vigerske2026-minlplib-a-library-of-mixed`,
  `vigerske2026-minlplib-documentation-database-snapshot-2026`):
  - feasibility tolerance 1e-8: points with violation at least 1e-8 are
    listed only under "Other points";
  - optimality tolerance 1e-9; gap tolerance 1e-6 ("dual bounds within 1e-06
    of primal bound indicate instance as solved");
  - S ("solved"): "for the best known feasible solution, at least 3 solvers
    claim global optimality (up to a relative optimal tolerance (gap) of
    10⁻⁶), or at least 3 solvers claim infeasibility";
  - "The 1st, 2nd, and 3rd best bound are in bold";
  - FAQ: the dual bounds "are just the best value as computed in some run
    with some option settings on some machine at some time in the past"; the
    primary format is GAMS; older GAMS versions used a default upper bound of
    100 for integer variables.
- **Display precision** (audit-ir and its review). No displayed value has
  more than 8 decimals. The rule "round to 10 significant digits, print with
  8 decimals, strip trailing zeros" reproduces 13,723 of the 13,847 finite
  displayed values exactly; 122 others differ only as "−0.", and two show
  more digits (evidence for Lemma 1 below).

### 1.2 Mathematical setting

An instance `P` in OSIL form is

    minimize   f(x) = c0 + f0(x)
    subject to l_i ≤ g_i(x) ≤ u_i      (i = 1..m)
               L_j ≤ x_j ≤ U_j         (j = 1..n; infinite bounds allowed)
               x_j ∈ Z                 (j ∈ I),

with rational data and expression trees built from +, −, ×, ÷, powers, exp,
log, sqrt and similar operators. Maximization is symmetric. Let `F(P)` be the
set of exactly feasible points (no tolerance) and
`v(P) = inf{ f(x) : x ∈ F(P) }`.

- **Validity.** A number `b` is a valid dual bound of a minimization
  instance if `b ≤ v(P)`.
- **Display unit.** For a displayed decimal string `s` with value
  `d(s) ≠ 0`, let `u(s)` be the unit of its last nonzero digit
  (`u("35.35267044") = 1e-8`, `u("−132117.") = 1`).
- **Audit slack.** `rho(s) = max(u(s)/2, ½·10^(⌊log10|d(s)|⌋ − 9))`, and
  `rho = 5e-9` for `d(s) = 0` (`audit.py: shown_slack`). The 10th-digit
  floor changes no screened pair.

### 1.3 The 15 class (i) instances

Sizes, types and S marks from `pages.json`; sources and references from the
stored instance pages.

| instance | source; application | type; vars/rows | S | structure that matters |
|---|---|---|---|---|
| glider100 | GAMS Model Library `glider` (COPS; Bulirsch, Nerz, Pesch, von Stryk 1993); hang-glider range maximization, 100 trapezoidal steps | NLP; 1315/1209 | – | `min −x102` (final range); free final time; 1209 equality rows; updraft terms `2.5(1 − r)e^(−r)`; exp and sqrt |
| topopt-cantilever_60x40_50 | QPLIB 5926 (J. Schelbert); topology optimization, 60×40 grid | MBQCP; 33600/14323 | – | `min Σ_e c_e`; cone rows `Σ_k w_{e,k}² − c_e y_e ≤ 0`, binary `y_e`; 4920 equality rows linear in the stresses `w`; 7003 rows in binaries only |
| methanol50 | GAMS Model Library `methanol` (COPS; Floudas et al. handbook; Tjoa–Biegler); methanol-to-hydrocarbons parameter estimation, 50 collocation elements | NLP; 1505/1497 | – | least squares, OSIL constant 5.016256589999999; 1497 rational equality rows; 5 kinetic parameters |
| sssd20-04, 22-08, 25-04, 25-08persp | Elhedhli 2006; Günlük–Linderoth perspective form; service system design with congestion | MBQCP; 108/52, 232/86, 128/57, 256/89 | S | customers assigned to servers, one capacity level per server; load rows `Σ_i a_i b_i = Σ_l c_l u_l`; `u_l ≤ b_l`; queue rows `u b + u q − q b ≤ 0`, i.e. `q ≥ u/(1 − u)` when `b = 1`; objective `Σ cost·b + 113818.9·Σ q` (sssd20-04) |
| ghg_3veh | Shiau–Michalek 2011; plug-in hybrid vehicle allocation minimizing greenhouse-gas emissions | MBNLP; 96/119 | – | exp terms and integer powers; 46 equalities plus 6 active inequalities form a 52×52 system after the binaries are fixed |
| nuclear14 | MacMINLP `c-reload` (Quist et al.); nuclear reactor core reload pattern | MBQCP; 1562/1226 | – | quadratic equalities; 434 rows remain after fixing integers and variables at bounds |
| nd_netgen-2000-3-4-b-a-ns_7 | QPLIB 4805 (A. Frangioni; Frangioni et al. 2011, 2016); network design | MBQCP; 10000/8074 | S | 2000 arcs `(b, f, u, s, t)`; rotated cones `c f² + s² − t² ≤ 0` with `s = (u − b)/2`, `t = (u + b)/2`, i.e. `c f² ≤ u b`; 74 flow-conservation rows; `f ≤ cap·b` |
| smallinvDAXr1b150-165, r2b150-165, r1b200-220, r2b200-220 | POLIP (portfolio, DAX30, small investor) | MIQCP (convex); 31/4 | S | `min objvar` with `xᵀQx − objvar ≤ 0`; three linear rows on 30 integer lots: return row e2 and budget rows e3, e4 (15000–16500 or 20000–22000); r1 and r2 differ only in e2 (every coefficient 1e-3 lower in r2), and one point proves both |
| watercontamination0303 | CMU-IBM MINLP project (Laird, Biegler, van Bloemen Waanders 2006); source inversion in a water network | MBQP (convex); 107222/108217 | S | all rows linear; quadratic objective with constant 9619.98394343983; 14 binaries; 1008 bounded source variables; 106200 free variables each fixed by a single-unknown equality |

### 1.4 Other instances in the family

- **Class (i-r):** eniplac (unit commitment; GAMS client; MBNLP 141/189; S),
  lop97icx (rail line optimization, Bussieck 1998; MIQCQP 986/87; S),
  spring (coil compression spring design, Sandgren 1990; modified MacMINLP;
  MINLP 17/8), stockcycle (cycle stock, Silver–Moon 1999; MBNLP 480/97,
  marked convex).
- **emfl050_3_3, 050_5_5, 100_3_3, 100_5_5** (GAMS Model Library `emfl`,
  after Vanderbei; facility location minimizing weighted Euclidean
  distances; QCP; 1611/1593, 5675/5625, 2961/2943, 9425/9375; S on 050_3_3
  and 100_5_5). Structure (asserted by `cert_socp.py` and by the recheck):
  base variables `z ≥ 0` (or free), each free `w` defined by one equality
  `w = a_wᵀz + e_w`, cones `t_k² − ‖w_k‖² ≥ 0` with `t_k ≥ 0`, objective
  `Σ_k c_k t_k` with `c_k ≥ 0` and no constant. The four OSIL files have no
  integer or binary variable (checked here).
- **rocket100/200/400** (GAMS Model Library `rocket`, Goddard rocket, COPS;
  Bryson 1999; NLP; `6N + 7` variables, `5N + 2` equality rows): one step
  variable, and velocity `v`, height `h`, gravity `g`, mass `m`, thrust `T`
  and drag `D` at `N + 1` nodes; `min −h_N`;
  `D_i = 310 v_i² exp(500(1 − h_i))`; `g_i = h_i^(−2)`; thrust in
  `[0, 3.5]`; mass in `[0.6, 1]` with `m_0 = 1`, `m_N = 0.6`.
- **oil** (pipeline design; MBNLP 1535/1546; S): class (iii), discussed in
  Section 8 (AUD-8).

### 1.5 Model provenance and model form

**History** (`R/publication/minlplib-status/report.md`, Table B1; review r1
confirmed the refresh; review r2: four minor issues, addressed).

- Unchanged on both sides of the bound dates, by archived copies:
  glider100 (since 2004), methanol50, nuclear14, nd_netgen, eniplac,
  lop97icx, spring, stockcycle, rocket100/200/400.
- topopt: complete identical listings of 2018-09-22 and 2020-01-11; the
  2022-05-22 copy (which already shows the LINDO bound) is cut at 1 MiB and
  matches today's first 23,479 lines; file dates (.gms 2020-12-11, OSIL
  2019-06-25) cover the rest.
- ghg_3veh: between 2017-11-23 and 2018-09-22, after both flagged bounds,
  three products of constants were replaced by rounded decimals (6 places in
  4 rows, relative change at most 1.84e-15). The refutation was re-proved on
  the old text with the audit's own `verify.py`, and independently by status
  review r1 (outward interval proof, objective 7.754006050100459 on the 2010
  text).
- sssd*persp, watercontamination0303 and smallinvDAX* were added a few days
  before their 2014 bounds. No copy covers March–December 2014; identity
  rests on the 2014-12-09 statistics page and the 2017-11-23 full copies.
  For smallinvDAX the old GAMS default integer bound 100 does not matter:
  the proving points use lots of at most 47 and 63.

**Model form (new exact check in this pass).** MINLPLib's primary format is
GAMS, while all certificates use the OSIL files. The status track compared
the two forms exactly only for methanol50, lop97icx, catmix and the controls
spring and nuclear14; the rest rested on GAMS conversion plus sample-point
evaluation. I ran the status track's exact comparison (`exact_forms.py`, on a
`/tmp` copy) for the other instances and added an exact comparison of
variable names, types and bounds (`checks/audit-r2/gms_osil_drive.py`). For
models with exp or sqrt, those functions were treated as opaque symbols whose
arguments are compared exactly (`gms_osil_drive_fn.py`).

| result | instances |
|---|---|
| every row (as an exact rational function), the objective, and every variable name, type and bound identical | glider100, topopt, sssd20-04/22-08/25-04/25-08persp, ghg_3veh, nuclear14, nd_netgen, smallinvDAX ×4, watercontamination0303 (14 class (i) instances); rocket100/200/400; emfl ×4; spring, eniplac |
| rows, bounds and types identical; 360 objective coefficients differ (constant, 104 linear, 255 quadratic; at most 2.38e-16 relative) | methanol50 (known; verdict proved on both forms by the status track) |

- Negative controls: changing one coefficient of sssd20-04persp row e30, the
  bound `x3.up` of spring, or one exp argument of ghg_3veh row e28, each by
  about 1e-13 relative, is detected (`gms_osil_negative_controls.log`).
- The `.gms` files contain only declarations, equations, bound and level
  assignments, `Model m / all /`, solve statements and output options
  (`m.limrow`, `m.limcol`, `m.tolproj`); none changes the model.
- Limits: one implementation (the status track's parser plus my bound
  comparison), not yet reviewed; stockcycle and lop97icx were not covered by
  this run (stockcycle has a rational objective that the parser rejects;
  lop97icx was compared by the status track).

## 2. Listed status

Pages of 2026-09-30, unchanged at the 2026-10-02 refresh. "Third-best" is
the third-best per-solver bound (MINLPLib bolds the three best). The `.solu`
column is the instance aggregate. Margins in the last column use the proven
exactly feasible objective `f` (Section 5) and are rounded to nearest.

| instance | S | flagged per-solver bounds (date) | best listed primal (point, date) | third-best bound | `.solu` | third − f; `.solu` − f |
|---|---|---|---|---|---|---|
| glider100 | – | COUENNE −1255.058601 (2015-06-25), LINDO −1255.058601 (2014-08-16) | −1255.058601 (p1, 2014-08-15); "other" p2 −983842.2578 (2022-03-16) | none (2 bounds) | `=best=` −1255.0586010 | no aggregate dual |
| topopt-cantilever_60x40_50 | – | LINDO 35.35267044 (2022-02-15) | 46.34312619 (p3, 2025-02-06); "other" p4 13.07748787, p5 10.33545826 | XPRESS 1.55311649 | `=bestdual=` 1.553116487 | −8.78; −8.78 |
| methanol50 | – | LINDO 0.00802826 (2022-02-15) | 0.00793022 (p4, 2022-03-16); p3 0.00802826 (2022-02-15) | GUROBI 0. | `=bestdual=` 0 | −0.0079; −0.0079 |
| sssd20-04persp | S | LINDO 347716.8909 (2014-03-02) | 347691.4105 (p3, 2015-03-06); p2 347716.8909 (2014-02-28) | ANTIGONE 347691.2933 | `=opt=` 347691.4105 | −0.117; +1.6e-5 (slack 5e-5) |
| sssd22-08persp | S | LINDO 508748.972 (2014-03-02) | 508713.731 (p4, 2017-09-13) | GUROBI 508713.6877 | `=opt=` 508713.731 | −0.043; −1.2e-5 |
| sssd25-04persp | S | LINDO 300186.8048 (2014-03-02) | 300176.5637 (p3, 2015-03-06) | GUROBI 300176.5511 | `=opt=` 300176.5637 | −0.013; +3.4e-5 (slack 5e-5) |
| sssd25-08persp | S | LINDO 472098.947 (2014-03-02) | 472093.078 (p4, 2017-09-13) | GUROBI 472092.8308 | `=opt=` 472093.078 | −0.25; +2.9e-5 (slack 5e-4) |
| ghg_3veh | – | ANTIGONE 7.7543245 (2013-09-26), BARON 7.7543245 (2014-08-16) | 7.75400605 (p2, 2015-03-06); p1 7.75432451 (2011-08-29) | GUROBI 6.39178216 | `=bestdual=` 6.391782164 | −1.36; −1.36 |
| nuclear14 | – | LINDO −1.12965944 (2022-02-15) | −1.12968744 (p3, 2025-06-18) | XPRESS −1000000. | `=bestdual=` −1e6 | −1e6; −1e6 |
| nd_netgen-2000-3-4-b-a-ns_7 | S | GUROBI 10729661.15, CPLEX 10729659.03 (both 2022-02-16) | 10729657.59 (p2, 2026-07-03); p1 10729661.15 (2018-08-18) | SCIP 10729656.76 | `=opt=` 10729657.59 | −0.83; +0.0047 (slack 0.005) |
| smallinvDAXr1b150-165, r2b150-165 | S | LINDO 88.1049355 (2014-02-28) | 88.10493476 (p2, 2015-03-06) | 88.10493476 (5 solvers) | `=opt=` 88.10493476 | −1e-11; −1e-11 |
| smallinvDAXr1b200-220, r2b200-220 | S | LINDO 156.604269 (2014-02-28) | 156.6042679 (p2, 2015-03-06) | 156.6042679 | `=opt=` 156.6042679 | +1.6e-8; +1.6e-8 (slack 5e-8) |
| watercontamination0303 | S | LINDO 207.9850353, BONMIN 207.9850352 (2014-02-28) | 207.9850348 (p2, 2014-02-28) | CPLEX 207.9850348 | `=opt=` 207.9850348 | −2.4e-9; −2.4e-9 |
| eniplac | S | COUENNE, LINDO, SCIP −132117. (2013-09-17) | −132117.083 (p2, 2004) | SCIP −132117. | `=opt=` −132117.083 | +0.083 (slack 0.5); +1.4e-5 (slack 5e-4) |
| lop97icx | S | ANTIGONE 4099.06 (2013-09-17) | 4099.059954 (p2, 2009) | LINDO 4099.059954 | `=opt=` 4099.059954 | +4.0e-7; +4.0e-7 (slack 5e-7) |
| spring | – | ANTIGONE, BARON, COUENNE, LINDO, SCIP 0.84624567 (2013-09-17) | 0.8462441 (p3, 2022) | COUENNE 0.84624567 | `=bestdual=` 0.8462206712 | +4.4e-9 (slack 5e-9); −2.5e-5 |
| stockcycle | – | ANTIGONE, BARON, COUENNE 119949. (2013-09-17) | 119948.6883 (p2, 2001) | COUENNE 119949. | `=opt=` 119948.6883 | +0.31 (slack 0.5); −3.3e-5 |
| rocket100 | – | LINDO −1.0128319 (2018-05-23) | −1.0128319 (p1, only point) | SCIP −1.0270225 | `=bestdual=` −1.027022503 | −0.014; −0.014 |
| rocket200 | – | LINDO −1.01283563 (2015-03-08) | −1.01283563 (p1) | ANTIGONE −1.07333642 | `=bestdual=` −1.073336422 | −0.061; −0.061 |
| rocket400 | – | LINDO −1.01283634 (2017-09-13) | −1.01283634 (p1) | ANTIGONE −9.30126526 | `=bestdual=` −9.301265255 | −8.3; −8.3 |

Source: `checks/audit-r2/agg.log` (and `checks/audit/third.log`).

**How MINLPLib aggregates (data-based reading, not a documented rule).** For
585 of the 589 instances with a `=bestdual=` entry, the value equals the
minimum of the third-best per-solver bound and the lowest listed point value
(other points included), up to 6e-9 relative. The four exceptions
(ball_mk4_15, chp_shorttermplan2c, nuclear10a, powerflow0057r) have no listed
point (`checks/audit-r2/solu.log`; same result in `checks/audit/solu.log`).
This matches the design stated in Vigerske's 2014 slides
(`vigerske2014-towards-minlplib-2-0`): "No way to verify correctness of
bound! … Conservative approach: Only trust a solver's dual bound claim if it
has been verified by at least 2 other solvers."

**Consequence.** In no instance of this family is the aggregate dual (the
third-best bound or the `.solu` value) larger than a proven exactly feasible
objective by more than display rounding. The safeguard worked. The refuted
entries matter for the per-solver data, for single-solver comparisons and
for users who read "the best listed dual" of an instance.

## 3. The certificates

### 3.1 Idea in plain words

A number is not a valid lower bound if a point that satisfies every
constraint exactly has a smaller objective value. The audit therefore looks
for listed points whose displayed objective lies below a displayed dual,
proves that an exactly feasible point exists at or near each such point,
and encloses that point's objective. Three kinds of existence proof are
used:

- the listed point is already exactly feasible;
- a nearby point is constructed and checked in exact rational arithmetic;
- a nearby point's existence is proved by a Krawczyk (interval Newton) test
  on a square subsystem, and every other constraint is checked over the
  proof box.

A conflict counts as an invalid bound only if it is larger than anything the
rounding of the displayed digits can explain. For the emfl instances, the
same exact machinery plus SOCP weak duality proves the opposite: every
listed dual is valid, and the listed primal values are tolerance artifacts.

### 3.2 Refutation under an explicit display hypothesis

**Hypothesis H (display).** For a listed bound `s` reported by a solver as
the number `b`, `|b − d(s)| < u(s)`.

**Lemma 1 (when H holds; supplied in this pass).**

- (a) Suppose the page shows exactly the stored decimal (trailing zeros
  stripped), and the stored decimal arose from `b` by one rounding (to
  nearest or directed) or truncation at some decimal position with unit
  `v`. Then H holds.
- (b) Suppose the stored value equals `b` up to binary64 conversion, and the
  page rounds it to nearest at 10 significant digits or 8 decimals and
  strips trailing zeros. Then H holds.
- (c) If `b` went through several roundings or truncations at successively
  coarser decimal positions before the page shows the result, then
  `|b − d(s)| < (10/9)·u(s)`; if the last step is the page's rounding to
  nearest, H holds.

*Proof.* (a) `d(s)` is an integer multiple of `v`, so its decimal expansion
has no nonzero digit finer than `v`; hence `u(s) ≥ v`. Rounding or
truncation at unit `v` moves the value by less than `v` (at most `v/2` for
rounding to nearest). So `|b − d(s)| < v ≤ u(s)`. (b) The page rounding at
unit `v'` gives `|b' − d(s)| ≤ v'/2` for the stored binary64 value `b'`, and
`u(s) ≥ v'` as in (a). The conversion error `|b − b'| ≤ 2^−53·|b|` is far
below `v'/2`, because the page unit is the coarser of the 10th significant
digit and the 8th decimal, so `v' ≥ 10^−10·|b|`. (c) Let the units be
`v_1 < … < v_k`. They are powers of 10, so `v_i ≤ 10^(i−k)·v_k`. Each step
moves the value by less than its unit, so the total is below
`v_k(1 + 1/10 + 1/100 + …) = (10/9)·v_k`. If the last step rounds to
nearest, the total is below `(1/2 + 1/9)·v_k` plus the conversion error. As
in (a), `u(s) ≥ v_k`. ∎

The display-rule test in Section 1.1 supports (b) for the pages.

**Proposition 1 (refutation).** Let `s` be a listed bound of a minimization
instance `P`. Let `x* ∈ F(P)` with `f(x*) ≤ φ`, where `φ` is rational.

- (i) If `d(s) − φ ≥ u(s)`, every `b` with `|b − d(s)| < u(s)` satisfies
  `b > v(P)`: under H, the solver's reported bound is invalid.
- (ii) If `d(s) − φ > rho(s)`, the same holds for every `b` within
  `rho(s)` of `d(s)` (round-to-nearest at the shown digits). This is the
  audit's class (i) rule.
- (iii) If `0 < d(s) − φ ≤ rho(s)`, the displayed number, read as a number,
  is not a valid bound, but a valid bound may display as `s` (class (i-r)).

*Proof.* `b > d(s) − u(s) ≥ φ ≥ f(x*) ≥ v(P)` for (i); (ii) and (iii) are
the same argument with `rho(s)` and with `b = d(s)`. ∎

All 19 class (i) pairs satisfy `(d − φ)/u ≥ 1.1158`. The minimum is
smallinvDAX*200-220: 1.1158 with the audit's enclosure, and exactly 1.116
with the point `objvar := xᵀQx` (margin 279/250000000). The rocket bounds
give 1.069, 4.71 and 18.9. So statement (i) applies to all 22 refuted
bounds. The 19 class (i) margins also exceed 10/9 units, so they survive
even a chain of truncations (Lemma 1(c)); rocket100 (1.069 units) is
covered by Lemma 1(a), (b), and (c) when the last step rounds to nearest.

**Corollary (tolerance independence).** Every tolerance-relaxed feasible set
contains `F(P)`, so its infimum is at most `v(P) ≤ f(x*) < b`. The
refutations hold for any feasibility tolerance of the solvers or of
MINLPLib. The converse fails: the emfl listed duals are valid for `F(P)`,
yet LINDO's and SCIP's 10.40173999 on emfl050_3_3 exceed the value of p2, a
primal-section point with listed violation 2e-10.

**Corollary (GAMS form).** For the 14 class (i) instances and
rocket100/200/400, which have exact form identity (Section 1.5), the
statements hold verbatim for the `.gms` model. For
methanol50 they hold on both forms (status track: the audit's `verify.py` on
GAMS 54.3's own OSIL rendering, which keeps the `.gms` objective exactly,
gives [0.007930218791205, 0.007930218793331]; and on the box p4 ± 1 the two
objectives differ by at most 3.2e-15, exactly).

### 3.3 Existence certificates

**(A) Exact rational certificates.** If a rational `x*` satisfies every
bound, integrality condition and row in exact arithmetic, then `x* ∈ F(P)`
and `f(x*)` is an exact rational. This covers rational-function models.

- Listed point exactly feasible as listed (route A): lop97icx p2, stockcycle
  p2, smallinvDAXr1b150-165 p2, smallinvDAXr2b150-165 p2.
- `cert_linear.py` (watercontamination0303): binaries rounded, the 1008
  bounded source variables keep their decimals, then 106200 single-unknown
  equality solves; every row and bound checked exactly.
- `cert_ndnetgen.py`: binaries kept; the 74 conservation rows are made exact
  by rational Gauss–Jordan elimination on interior flows (largest change
  2.1e-13; a row left without a pivot must already hold exactly, and the
  first verifier found rank 72 with two exactly consistent dependent rows);
  `u := max(u, c f²)`; `s, t` from their defining rows.
- Recheck `sssd_exact.py`: binaries kept, the load row fixes the single
  active utilization `u`, and `q := u/(1 − u)` (the least feasible value).
- Recheck `smallinv_exact.py`: integers kept, `objvar := xᵀQx`.
- audit-ir `check_ir.py`: all four (i-r) instances.

**(B) Krawczyk existence test.** Route B of `R/bound-audit/verify.py`
(route C first shifts the point into the interior along a direction from a
HiGHS LP, which is a heuristic only), the first verifier's `kraw.py`, the
wave-2 reviewer's `krawczyk.py`.

*Construction.* Integer variables are rounded and fixed; continuous
variables within 1e-7 (relative) of a bound are put on it; the active rows
`E` are all equalities plus the inequalities violated or within 1e-7 of a
side, held at that side; rows whose gradient vanishes move to the box check;
a basis `B` with `|B| = |E|` is chosen by QR with column pivoting; the other
variables `N` keep their exact decimals; Newton runs on
`F(x_B) = g_E(x_B, x_N) − t_E` with residuals at 40 digits.

**Proposition 2 (Krawczyk; Krawczyk 1969, Moore 1977, Rump 2010).** Let `F`
be continuously differentiable on an open set containing the box
`X = [x̃ − r, x̃ + r] ⊂ Rⁿ`, `r > 0`. Suppose
`F(x̃) ∈ [F_c − F_r, F_c + F_r]`, that for every `ξ ∈ X` and every row `i`
the gradient `∇F_i(ξ)` lies in row `i` of `[J_c − J_r, J_c + J_r]`, and let
`R` be any real matrix. If

    β := |R F_c| + |R| F_r + |I − R J_c| r + |R| J_r r  <  r   (componentwise),

then `F` has exactly one zero in `X`.

*Proof.*

1. Let `T(x) = x − R F(x)`. For `x ∈ X`, the mean value theorem applied row
   by row on the segment `[x̃, x] ⊂ X` gives `F(x) − F(x̃) = J̃(x − x̃)`, where
   row `i` of `J̃` is `∇F_i(ξ_i)`, so `|J̃ − J_c| ≤ J_r`.
2. Then `T(x) − x̃ = −R F(x̃) + (I − R J̃)(x − x̃)`, hence
   `|T(x) − x̃| ≤ |R F_c| + |R| F_r + (|I − R J_c| + |R| J_r) r = β < r`.
   So `T` maps `X` into its interior, and by Brouwer's theorem it has a
   fixed point `x*`.
3. For every `J̃` as in step 1, `M = |I − R J̃|` satisfies `M r ≤ β < r`.
   Hence `max_i (M r)_i / r_i < 1`, the spectral radius of `I − R J̃` is
   below 1, and `R J̃` is nonsingular. So `R` is nonsingular, and
   `R F(x*) = 0` gives `F(x*) = 0`.
4. If `x, y ∈ X` are zeros, `0 = F(x) − F(y) = J̃'(x − y)` with rows of `J̃'`
   taken at points of `[y, x] ⊂ X`; `J̃'` is nonsingular by step 3, so
   `x = y`. ∎

**Corollary (exactly feasible point).** If moreover (i) every row outside
`E` satisfies its bounds for all `ξ ∈ X` (interval enclosure), or is
constant in `x_B` and checked exactly; (ii) `L_B ≤ X ≤ U_B`; and (iii) the
fixed values `x_N` satisfy their bounds and integrality exactly, then
`x* = (x*_B, x_N) ∈ F(P)` and `f(x*)` lies in the interval enclosure of `f`
over `X × {x_N}`. An equality row outside `E` passes only if it vanishes
identically as a polynomial or its enclosure is the single point `[l, l]`;
a nonconstant enclosure of positive width can never pass, so no equality
can pass by accident (`verify.py: check_on_box`).

*What the computation checks, in which arithmetic.*

| item | audit `verify.py` | first verifier `kraw.py` (+ `ivl.py`) |
|---|---|---|
| `F(x̃)`, `J` over `X` | interval forward AD in mpmath `iv` at 40 digits from the exact decimals, converted outward to binary64 centre–radius pairs | interval forward AD with rational endpoints rounded outward to 200 bits; `+ − × ÷` and integer powers exact before rounding; sqrt via `isqrt`; exp/log by mpmath at 90 digits, widened by a relative 1e-60 |
| `R` | `inv(J(x̃))` in binary64 | `inv(J_c)` in binary64 |
| matrix products | a priori bound abs(fl(AB) − AB) ≤ γ_n·abs(A)·abs(B) entrywise, `γ_n = n·u/(1 − n·u)`, `u = 2⁻⁵³`; factor `(1 + 1e-6)²` for the remaining relative roundings (below `n·u ≈ 4.4e-13` for `n ≤ 4000`); `+1e-300` for underflow | same bound with a factor 2 and explicit underflow terms `k·2⁻¹⁰⁷⁴`; final factor `1 + 1e-12` |
| box `X` | `x̃ ± r` with endpoints moved outward by one ulp; inner and outer radii bounded at 200 bits | `x̃ ± r` with exact rational endpoints |
| box check | exact polynomial arithmetic in the basic variables where possible, interval evaluation otherwise | interval evaluation; exact for rows over fixed values |

*Trust base.* IEEE-754 binary64 arithmetic (any summation order, with or
without FMA) for the floating-point products; Python `Fraction` and integer
arithmetic; for the audit, correct outward rounding of mpmath `iv`
(conversion of decimals, `+ − × ÷`, powers, exp, log, sqrt); for the first
verifier, mpmath's exp/log accurate to far better than 1e-60 relative at 90
digits. I checked in `/tmp` that mpmath `iv` converts decimal strings and
large integers outward (for example `iv.mpf('0.1')` has positive width and
encloses 1/10). The class (i) and rocket OSIL files use only smooth
operators: `+ − ×`, divide, square, integer power, plus exp and sqrt
(glider100), exp (ghg_3veh, rocket). No abs, min, max or trigonometric
operator occurs (checked). Division and sqrt enclosures that touch 0 abort
the proof.

**(C) Dedicated certificates.**

- `cert_topopt.py` (audit) and `topopt_exact.py` (first verifier) for
  topopt p4 and p5. Binaries are kept; void-element stresses are exactly 0
  in the listed points (asserted) and stay 0, so their cone rows read
  `0 ≤ 0`. The 3162 (p5) or 3056 (p4) equality rows that involve
  solid-element stresses are linear.
  - Audit: a QR basis of solid-element `w`, Krawczyk on the linear system
    (worst ratio 0.011 at radius 1e-14 relative).
  - Verifier: `w = w₀ + A_sᵀy` with `G = A_s A_sᵀ` computed exactly,
    Krawczyk on `G y = r` (ratio 7.7e-6, p5).
  - In both, `c_e :=` the upper endpoint of an interval enclosure of
    `Σ_k W_{e,k}²` over the proof box, so every solid cone row holds at the
    unique solution in the box. The objective `Σ c_e` is then an exact
    rational upper bound for the proven point.

### 3.4 emfl: two-sided enclosure of the optimum

**Proposition 3.** Consider
`min Σ_k c_k t_k` s.t. `t_k² − ‖w_k‖² ≥ 0`, `t_k ≥ 0`,
`w_k = A_k z + e_k`, `z ≥ 0` (componentwise; free components allowed),
with rational data and `c_k ≥ 0`.

- (a) Upper bound. For rational `z̄` satisfying the bounds and rationals
  `τ_k ≥ 0` with `τ_k² ≥ ‖A_k z̄ + e_k‖²`, the point
  `(z̄, A z̄ + e, τ)` is exactly feasible, so `v ≤ Σ c_k τ_k`.
- (b) Lower bound. For rational `y_k` with `‖y_k‖² ≤ c_k²` and
  `g := Σ_k A_kᵀ y_k` with `g_j ≥ 0` for every sign-constrained `z_j` and
  `g_j = 0` for every free `z_j`, every feasible point satisfies
  `Σ c_k t_k ≥ Σ_k e_kᵀ y_k`.

*Proof of (b).* `t_k ≥ 0` and `t_k² ≥ ‖w_k‖²` give `t_k ≥ ‖w_k‖`. By
Cauchy–Schwarz, `c_k t_k ≥ c_k ‖w_k‖ ≥ ‖y_k‖ ‖w_k‖ ≥ y_kᵀ w_k`. Summing,
`Σ c_k t_k ≥ Σ y_kᵀ(A_k z + e_k) = gᵀz + Σ e_kᵀ y_k ≥ Σ e_kᵀ y_k`. ∎

*Computation.* `y` comes from a numerical dual SOCP (cvxpy/Clarabel), then
is made exactly admissible: the audit applies a rational least-norm
correction to `g = 0` and a global scale `s ≤ 1`; the recheck scales each
cone to radius `c_k(1 − η)`, corrects negative `g_j` with single-cone moves
and applies a final scale; the first verifier uses a least-norm correction of
negative `g_j` and `s = 1 − 2.2e-13`. Both conditions and `Σ e_kᵀ y_k` are
evaluated exactly; `τ_k` is a rational upper bound of the square root
(`isqrt`). Only `Fraction` and `isqrt` are trusted. `cert_socp.py` does not
check integrality, which is harmless here: the emfl files have no integer
variables.

### 3.5 spring: global optimum (explains the class (i-r) entries)

Model (from `spring.osil`; identical to the `.gms` text): `x1 ≥ 0.414`,
`x2 ≥ 0.207`, `x3 ∈ [λ, 0.02]` with `λ = 1.78571428571429e-3`, integer
`i4 ∈ [1, 100]`, `x5 ≥ 1.1`, free `x6`, binaries `b7..b17`;
`e2: x5 = x1/x2`; `e3: x6 = (4x5 − 1)/(4x5 − 4) + 0.615/x5`;
`e4: 2546.47908913782·x6·x5/x2² ≤ 189000`;
`e5: x3 = K·x5³·i4/x2` with `K = 6.95652173913044e-7`;
`e6: 2.1x2 + 1000x3 + 1.05·x2·i4 ≤ 14`; `e7: x1 + x2 ≤ 3`;
`e8: x2 = Σ_k c_k b_k` with
`c ∈ {.207, .225, .244, .263, .283, .307, .331, .362, .394, .4375, .5}`;
`e9: Σ b_k = 1`; objective `(a0 + a1·i4)·x1·x2²` with `a0 = 1.570796327`,
`a1 = 0.7853981635`.

**Proposition 4.** `v(spring) = f* := (a0 + 9a1)·0.283³·x5*` with
`x5* = (λ·0.283/(9K))^(1/3)`, i.e.
`f* = 0.84624566564315428125166463503714129527…`. It is attained at
`i4 = 9`, `x2 = 0.283` (`b11 = 1`), `x3 = λ`.

*Proof.*

1. *Reduction.* `e8`, `e9` and integrality give `x2 = c` for exactly one
   `c`. Fix `i4 = n` and `x2 = c`. Then `e2`, `e5`, `e3` determine
   `x1 = c·x5`, `x3 = K n x5³/c`, `x6 = W(x5)`, and the objective is
   `(a0 + a1 n) c³ x5`, increasing in `x5`.
2. *Each remaining condition is an interval in `x5 > 1`.*
   `x5 ≥ 1.1`; `x1 ≥ 0.414 ⇔ x5 ≥ 0.414/c`;
   `x3 ∈ [λ, 0.02] ⇔ (λc/(Kn))^(1/3) ≤ x5 ≤ (0.02c/(Kn))^(1/3)`;
   `e6 ⇔ x5³ ≤ (14 − 2.1c − 1.05cn)·c/(1000Kn)`; `e7 ⇔ x5 ≤ (3 − c)/c`;
   `e4 ⇔ h(x5) ≤ 189000c²/2546.47908913782 − 0.615`, where
   `h(x) = x(4x − 1)/(4(x − 1)) = (x − 1) + 7/4 + 3/(4(x − 1))`.
   Since `h''(x) = 3/(2(x − 1)³) > 0` on `(1, ∞)`, `h` is convex and its
   sublevel set is an interval. (The audit-ir reviewer used the same
   identity, with minimum `h + 0.615 = 2.365 + √3` at `x = 1 + √3/2`.)
3. So the feasible `x5` of each assignment form an interval `I(n, c)`
   (possibly empty), and `v = min_{n,c} (a0 + a1 n) c³ · min I(n, c)`.
4. At `(9, 0.283)`: the largest lower bound is `x5 ≥ x5* ≈ 4.32170`
   (from `x3 ≥ λ`; the others are 1.1 and 1.463). At `x5*`, `e4` gives
   187991.19 ≤ 189000, `e6` gives 5.054 ≤ 14, `e7` gives 1.506 ≤ 3, and
   `x3 = λ ≤ 0.02`. So `min I(9, 0.283) = x5*`, with value `f*`.
5. *Enumeration (computer-assisted, exact).* The audit-ir script
   `spring_global.py` enumerates all 1100 assignments with cube roots
   bracketed by rationals and checked by exact cubing: 890 are infeasible,
   210 feasible, and every other minimum exceeds `f*`; the runner-up is
   0.8592755352970280… at `(5, 0.307)`. Its independent reviewer
   (`step3_spring.py`) excludes 723 assignments by the bounds of `x3`, `e6`
   and `e7`, shows that no remaining assignment can reach the rational
   `T < f*` below, and encloses
   `f* ∈ [0.84624566564315428125166463503714129527532857794010,
   0.84624566564315428125166463503714129527534815925597]`. ∎

Checks here: my 60-digit scan reproduces 210 feasible assignments, `f*`,
the runner-up 0.859275535297028… and the third 0.891317680305808… at
`(10, 0.283)` (`checks/audit-r2/spring_scan.log`; evidence only).

**Consequences.** The five displayed bounds 0.84624567 exceed `f*` by
4.3568e-9 = 0.871·(5e-9) and equal `f*` rounded to 8 decimals. The bold
primal 0.8462441 (p3; `.solu` `=best=` 0.8462441005) lies 1.57e-6 below
`f*`, so no exactly feasible point attains it. `.solu` `=bestdual=`
0.8462206712 is valid. The underlying stored solver bounds are unknown.

### 3.6 Classification rule (minimization; maximization symmetric)

Let `[φ_lo, φ_hi]` enclose the objective of a proven exactly feasible point
near the flagged point (`audit.py classify`).

- (i): `d − φ_hi > rho(s)`; "gross" if `(d − φ_hi)/|d| > 1e-6`, otherwise
  "tolerance-scale". The 1e-6 threshold is a size label borrowed from
  MINLPLib's gap tolerance.
- (i-r): `0 < d − φ_hi ≤ rho(s)`.
- (ii) proven: `d ≤ L` for a rigorous lower bound `L ≤ v(P)`.
- (ii) repair: `φ_lo ≥ d`; evidence, not proof, that `d` is valid.
- (iii): no proof either way.

The class of an (instance, solver) pair is the strongest over its flagged
points. Margins are exact `Fraction`s compared with the binary64 value of
`rho(s)`; the closest ratios are 2.23 for (i) and 0.871 for (i-r), so no
decision is near a boundary.

## 4. Exactly feasible primal points

| instance (point) | construction | proof (arithmetic) | second implementation |
|---|---|---|---|
| glider100 (p2, "other", listed 3e-8; exact violation 1.2e-7) | route C: shift by `t = 1.75e-10`, Newton, Krawczyk on 1208 rows (ratio 1.0e-4, radius 1e-12) | interval (mpmath `iv`, exp, sqrt) | first verifier: own Krawczyk on 1209 rows with `y₁ = 0`, `cL₀ = 0` and 33 `cL = 0` fixed on bounds; ratio 0.133 at radius 1e-13 |
| topopt (p5, p4; "other", 1.2e-7 and 2.3e-8) | `cert_topopt.py` | linear Krawczyk + exact `c_e` | first verifier `topopt_exact.py` |
| methanol50 (p4, primal) | route B, n = 1497 (ratio 2e-3) | interval, rational model | first verifier (own Krawczyk); wave-2 reviewer (`krawczyk.py`) |
| nuclear14 (p3, primal) | route B, n = 434 | interval, quadratic model | first verifier |
| ghg_3veh (p2, primal; route A fails on e1 by 5e-14) | route B, n = 52 (ratio 7.3e-5) | interval (exp) | first verifier (ratio 9.1e-4 at radius 1e-13); status review r1 on the 2010 text |
| sssd20-04, 22-08, 25-04, 25-08persp (p3/p4, primal) | route B, "snap-first", n = 8 or 16 | interval | recheck: exact `q = u/(1 − u)` construction; first verifier: Krawczyk (sssd20-04, after snapping four 5e-15 values to 0); first dossier pass: own exact construction |
| smallinvDAXr{1,2}b150-165 (p2) | listed point exactly feasible (route A) | exact | verifier and recheck; with `objvar := xᵀQx`, exactly 88.10493476 = 2202623369/25000000 |
| smallinvDAXr{1,2}b200-220 (p2; e1 violated by exactly 5e-15 as listed) | route B (n = 1) | interval | `objvar := xᵀQx` = 156.604267884 = 39151066971/250000000 exactly (verifier, recheck, first dossier pass) |
| watercontamination0303 (p2) | `cert_linear.py` | exact | first verifier `water_exact.py` (1026-digit denominator) |
| nd_netgen (p2, primal; listed 1e-12, exact violation 1.70e-5) | `cert_ndnetgen.py` (`u = max(u, c f²)`) | exact | first verifier: minimal `u` (10729657.585117233…) and `max` variant |
| emfl ×4 | rational Clarabel `z`, exact `w`, rational `t ≥ ‖w‖` | exact | recheck (all four), first verifier (050_3_3) |
| (i-r): lop97icx p2, stockcycle p2 (exact as listed); eniplac (81 variables recomputed from linear equalities); spring (rational `x5` rounded up at 1e-30) | exact | exact | audit-ir author and reviewer |
| rocket100/200/400 (own CONOPT points) | thrust fixed at the authors' CONOPT values; step and masses exact (mass rows linear given thrust); Krawczyk on the 4N unknowns `(v, h, g, D)` | interval (exp) | wave-2 reviewer `krawczyk.py` (mpmath `iv`); **this pass:** `checks/audit-r2/rocket_kraw.py` with the first verifier's `ivl.py`/`kraw.py` |

**glider100 point (physical reading; both reviews).** Final time
62163.18 s, so the step is 621.63 s. The altitude starts at 1000 m, is exactly
0 at node 1 (on its bound; about 1e-10 m in the audit's route-C repair),
rises to about 64.6 km and ends at 900 m. The vertical acceleration changes
sign at every step with magnitude 7.8–9.8 m/s², so the trapezoidal averages
nearly cancel: a period-2 mode of the discretization at a huge step. The
range is 983,842 m against 1255 m at the physically meaningful local
solution. The point solves the discretized model as distributed, not the
continuous problem.

**rocket points (this pass).** The thrust is at a bound in 76/151/315 of the
101/201/401 nodes, and the mass equals its lower bound 0.6 exactly at
64/127/254 nodes; all such bounds are checked exactly. The Krawczyk ratio is
about 1.1e-4 at radius 1e-12·max(1, |x|) in both implementations.

## 5. Numbers

Display conventions: enclosures are rounded outward; margins `d − f`,
relative margins and "units" are computed from the upper end of the
enclosure and shown **rounded down** (safe "at least" displays,
`checks/audit-r2/safe_margins.log`); "units" means `(d − f)/u(s)`. A value
ending in "…" is an exact rational, truncated.

### 5.1 Class (i): 19 per-solver bounds on 15 instances

| instance | solver(s) | listed `d` | proven `f` (audit, outward) | second implementation | `d − f` ≥ | rel. ≥ | units ≥ | label |
|---|---|---|---|---|---|---|---|---|
| glider100 | COUENNE, LINDO | −1255.058601 | [−983842.2577737, −983842.2577716] | [−983842.2577883191, −983842.2577881224] | 982587.19 | 782.9 (`f/d` = 784) | 9.82e11 | gross |
| topopt-cantilever_60x40_50 | LINDO | 35.35267044 | p5 [10.33547432780, 10.33547432781]; p4 [13.07748199152, 13.07748199153] | p5 ≤ 10.335474275747004; p4 ≤ 13.077481991525133 | 25.01 | 0.7076 (`d/f` = 3.42) | 2.50e9 | gross |
| methanol50 | LINDO | 0.00802826 | [0.007930218684615, 0.007930218899920] | [0.0079302187853, 0.0079302187992]; [0.00793021868, 0.00793021891] | 9.804e-5 | 1.221e-2 | 9800 | gross |
| sssd20-04persp | LINDO | 347716.8909 | [347691.4104835, 347691.4104845] | [347691.4104839489, 347691.4104840173]; 347691.41048398308… | 25.48 | 7.327e-5 | 2.54e5 | gross |
| sssd22-08persp | LINDO | 508748.972 | p4 [508713.7310104, 508713.7310120] | 508713.73101118680506… | 35.24 | 6.926e-5 | 3.52e4 | gross |
| ghg_3veh | ANTIGONE, BARON | 7.7543245 | [7.754006050048, 7.754006050065] | [7.754006050055795, 7.754006050057346] | 3.184e-4 | 4.106e-5 | 3180 | gross |
| sssd25-04persp | LINDO | 300186.8048 | [300176.5636655, 300176.5636663] | 300176.56366586825118… | 10.24 | 3.411e-5 | 1.02e5 | gross |
| nuclear14 | LINDO | −1.12965944 | [−1.129687441173, −1.129687441170] | [−1.12968744117138, −1.12968744117116] | 2.800e-5 | 2.478e-5 | 2800 | gross |
| sssd25-08persp | LINDO | 472098.947 | p4 [472093.0779691, 472093.0779707] | 472093.07796988413312… | 5.869 | 1.243e-5 | 5860 | gross |
| nd_netgen-2000-3-4-b-a-ns_7 | GUROBI; CPLEX | 10729661.15; 10729659.03 | 10729657.585310911… (exact) | 10729657.585117233… (minimal `u`) | 3.564; 1.444 | 3.322e-7; 1.346e-7 | 356; 144 | tolerance |
| smallinvDAXr1b150-165, r2b150-165 | LINDO | 88.1049355 | 88.104934760000006 (listed point, exact) | 88.10493476 exactly (`objvar := xᵀQx`) | 7.399e-7 (7.4e-7 exactly for the `xᵀQx` point) | 8.399e-9 | 7.39 | tolerance |
| smallinvDAXr1b200-220, r2b200-220 | LINDO | 156.604269 | [156.60426788384, 156.60426788416] | 156.604267884 exactly | 1.115e-6 (279/250000000 = 1.116e-6 exactly for the `xᵀQx` point) | 7.125e-9 | 1.11 | tolerance |
| watercontamination0303 | LINDO; BONMIN | 207.9850353; 207.9850352 | 207.98503480238880… (exact) | 207.9850348023888… (exact) | 4.976e-7; 3.976e-7 | 2.392e-9; 1.911e-9 | 4.97; 3.97 | tolerance |

Sources: `R/bound-audit/audit-report.md` §1 and §4, `results.json`,
`logs/verify/*.json`, `logs/cert_*.json`; second implementations from
`R/reviews/bound-audit-verification/` (report table and logs),
`R/reviews/bound-audit-recheck.md` and `R/reviews/wave2-small-verification/`.
All margins agree with the summary and the audit report (no disagreement
found; `checks/audit-r2/margins.log`).

Distribution of `(d − f)/|d|`: [1e-9, 1e-7): 6; [1e-7, 1e-5): 2;
[1e-5, 1e-3): 7; [1e-3, 1e-1): 1; ≥ 0.1: 3.

By solver: LINDO 8 gross + 5 tolerance-scale (13 instances); ANTIGONE, BARON
and COUENNE 1 gross each; CPLEX, GUROBI and BONMIN 1 tolerance-scale each.
The 19 pairs are 15 distinct numerical conflicts: smallinvDAX r1/r2 share
the proving point value and LINDO value, and glider100 and ghg_3veh each
have two solvers with one displayed value.

### 5.2 Class (i-r): 12 pairs on 4 instances (all dated 2013-09-17)

| instance | solvers | listed `d` | exactly feasible `f` | `d − f` | rel. | /slack | /half unit at the page limit (10th digit or 8th decimal) | explanation |
|---|---|---|---|---|---|---|---|---|
| eniplac | COUENNE, LINDO, SCIP | −132117. | −132117.08301998871378… (from the listed point) | 0.0830 | 6.28e-7 | 0.166 | 1660 | consistent with earlier 6-digit rounding (evidence) |
| lop97icx | ANTIGONE | 4099.06 | 4099.059953600000099 (listed point) | 4.64e-5 | 1.13e-8 | 0.0093 | 92.8 | same |
| spring | ANTIGONE, BARON, COUENNE, LINDO, SCIP | 0.84624567 | `f*` = 0.84624566564315428125… (global optimum) | 4.3568e-9 | 5.15e-9 | 0.871 | 0.871 | 8-decimal rounding of `f*` (proved) |
| stockcycle | ANTIGONE, BARON, COUENNE | 119949. | 71969213/600 = 119948.68833… (listed point) | 187/600 | 2.60e-6 | 0.623 | 6233 | consistent with earlier 6-digit rounding (evidence) |

Source: `R/publication/audit-ir/report.md` and its review r1. The digit
histogram (59 six-digit and 2 seven-digit values among the 2013-09-17 dual
bounds) supports but does not prove the 6-digit explanation. Read as exact
numbers, the 7 non-spring entries would be class (i): eniplac and lop97icx
tolerance-scale, stockcycle gross (2.6e-6).

### 5.3 emfl: listed duals valid; listed primal values below the optimum

| instance | S | listed duals | best listed primal | exact optimum (recheck, outward) | audit enclosure | best listed primal below the optimum by ≥ |
|---|---|---|---|---|---|---|
| emfl050_3_3 | S | BARON 10.40173793; LINDO, SCIP 10.40173999; ANTIGONE 0.11605443; COUENNE 0.11888301 | 10.40173793 (p2, 2e-10) | [10.4017521318429, 10.4017521318448] | [10.4017521316, 10.4017521319] | 1.41e-5 (1.36e-6 rel.) |
| emfl050_5_5 | – | BARON, LINDO, SCIP 18.91340776; ANTIGONE 0.11665436; COUENNE 0.11671129 | 18.91165289 (p6, 1e-8) | [18.9136329557291, 18.9136329557624] | [18.9136329529, 18.9136329563] | 1.98e-3 |
| emfl100_3_3 | – | BARON, LINDO, SCIP 18.13262446; ANTIGONE 0.11740779; COUENNE 0.11813405 | 18.13236088 (p4, 1e-8) | [18.1326531242336, 18.1326531242359] | [18.1326531194, 18.1326531244] | 2.92e-4 |
| emfl100_5_5 | S | BARON, LINDO 32.63818348; SCIP 32.63818206; ANTIGONE 0.10044302; COUENNE 0 | 32.63818348 (p1, 1e-10) | [32.6381903545115, 32.6381903545301] | [32.6381903513, 32.6381903548] | 6.86e-6 (2.10e-7 rel.) |

- First verifier for emfl050_3_3: [10.40175213184103, 10.40175213184476];
  first dossier pass: own exact lower bound 10.401752116015716.
- The last column subtracts the displayed value plus half a unit in its last
  digit from the audit's exact lower bound
  (`checks/audit-r2/emfl_shortfalls.log`). Read literally, the displayed
  numbers lie 1.42016e-5 and 6.8713e-6 below, which supports the audit's
  "at least 1.42e-5" and "at least 6.87e-6"; both readings are true as
  stated, but only the widened values also cover the display rounding of the
  listed point values.
- Every listed point of emfl050_5_5, emfl100_3_3 and emfl100_5_5, and every
  listed point of emfl050_3_3 except p3 (at least 4.913e-5 above the proven
  upper bound), lies below the exact optimum. Largest shortfall: 8.12e-3
  (4.3e-4 relative; emfl050_5_5 p5, an "other" point).
- **emfl050_3_3 is marked S**, but its best listed dual 10.40173999 lies at
  least 1.213e-5 below the exact optimum, i.e. at least 1.166e-6 relative,
  just above the 1e-6 gap tolerance (widened by half a display unit; read
  literally, 1.2141e-5 and 1.1672e-6). The S mark is consistent with the
  listed primal 10.40173793, which no exactly feasible point attains. emfl100_5_5
  (S) is closed within tolerance also against the exact optimum (2.1e-7).
- `.solu` lists `=best=` (not `=opt=`) for all four, with `=bestdual=` equal
  to the lowest listed "other" point value (e.g. 10.40104178).

### 5.4 Outside the screen: LINDO on rocket

| instance | LINDO `d` (date) | proven enclosure (wave-2 reviewer) | proven enclosure (this pass, second implementation) | `d − f` ≥ | rel. ≥ | units ≥ |
|---|---|---|---|---|---|---|
| rocket100 | −1.0128319 (2018-05-23) | [−1.0128320069151, −1.0128320069130] | [−1.0128320069151, −1.0128320069130] | 1.069e-7 | 1.055e-7 | 1.06 |
| rocket200 | −1.01283563 (2015-03-08) | [−1.0128356770698, −1.0128356770677] | [−1.0128356770698, −1.0128356770677] | 4.706e-8 | 4.647e-8 | 4.70 |
| rocket400 | −1.01283634 (2017-09-13) | [−1.0128365294842, −1.0128365294822] | [−1.0128365294843, −1.0128365294821] | 1.894e-7 | 1.870e-7 | 18.9 |

Each LINDO value equals the only listed point p1 in every displayed digit (a
display tie the screen cannot see). The other rocket per-solver bounds are
consistent with these enclosures (COUENNE −1.01283202 lies 1.3e-8 below on
rocket100, and −1.01283661 lies 8.1e-8 below on rocket400). With rocket,
22 per-solver bounds on 18 instances are proven invalid; LINDO accounts for
16 instances.

### 5.5 Counts

| quantity | value | source |
|---|---|---|
| pages / OSIL files | 1633 / 1632 | `recount.log` |
| points / bounds (finite) / labels | 2816 / 11086 (11031) / 19 | `recount.log` |
| screened pairs / instances / points / (instance, solver) | 158 / 46 / 56 / 131; 110 pairs from "other points" | `recount.log` (exact decimal screen equals `screen.json`) |
| display ties / instances | 3851 / 1133 | `recount.log` |
| (instance, solver) pairs by class | (i) gross 11 (9 instances); (i) tolerance 8 (6); (i-r) 12 (4); (ii) proven 12 (4); (ii) repair 63 (11); (iii) 25 (12) | `class_recount.log`; recheck `consistency.log` |
| (ii)-repair instances | alkyl, elf, hybriddynamic_fixedcc, hybriddynamic_varcc, squfl010-040persp, squfl015-080persp, squfl020-040persp, squfl020-050persp, squfl025-040persp, squfl030-100persp, squfl030-150persp | `results.json` |
| (iii) instances | cecil_13, ex7_3_5, ex8_2_1b, hda, heatexch_spec2, oil, rsyn0815m04m, rsyn0820m03m, rsyn0830m03m, rsyn0830m04m, sepasequ_complex, sepasequ_convent | `results.json` |

**Disagreements found** (wording only; no number is wrong):

- The summary lists "an exact duality certificate" among the methods that
  prove the 19 bounds invalid; duality certificates prove validity (emfl).
- The summary gives the rocket100 margin as "1.1e-7"; the margin is at
  least 1.069e-7 (1.07e-7 as a rounded size; 1.06e-7 as a safe "at least"
  display at three digits).
- "Up to a factor of about 784" mixes `f/d = 784` with
  `(d − f)/|d| = 783`.

## 6. Verification record

| check | scope | independence | verdict |
|---|---|---|---|
| First verification (`R/reviews/bound-audit-verification/verification-report.md`, 2026-09-30) | 14 of 19 pairs; emfl050_3_3; nd_netgen exact violation | own OSIL reader (exact), own 200-bit rational interval arithmetic, own Krawczyk, own exact certificates; re-fetched data byte-identical | all confirmed; recommended the gross/tolerance split, margins relative to \|d\| and labelled inferences (adopted) |
| Recheck (`R/reviews/bound-audit-recheck.md`, 2026-09-30) | other 5 pairs; emfl050_5_5, 100_3_3, 100_5_5 (+ 050_3_3); all counts, margins, splits and histogram from the data files | own reader, exact only; negative controls | all confirmed; 9 text issues (one factual: ghg_3veh p2 is not exactly feasible as listed); no class change |
| Confirmations r1–r3 (`recheck-audit-confirm.md`, `audit-confirm-r1.md`, `audit-confirm-r2.md`) | fixes; outward display rounding; `check_display.py` with negative controls | own scripts | last verdict **verified**, no remaining problem |
| audit-ir + review r1 (`R/publication/audit-ir/report.md`, `R/publication/reviews/audit-ir-review-r1.md`) | all 12 (i-r) pairs; spring global optimum; full re-parse of 1633 pages; screen; digit statistics | author and reviewer wrote separate exact readers; SCIP cross-check as evidence | **verified, minor issues** (addressed) |
| Status/model history (`R/publication/minlplib-status/report.md`, reviews r1, r2) | refresh 2026-10-02; archived copies; exact comparisons for methanol50, lop97icx, catmix | r1 re-fetched with own code and gave an independent interval proof for ghg_3veh on the 2010 text | r1 confirmed; r2 **issues** (4 minor, addressed) |
| Wave-2 small verification §6 (`R/reviews/wave2-small-verification/verification-report.md`) | methanol50, rocket100/200/400 | reviewer's own Krawczyk (mpmath `iv`); the authors had numerical polishing only | **verified rigorously** |
| Integration reviews r1, r2 (`R/publication/reviews/integration-review-r*.md`) | audit counts, displays, wording in summary, audit and READINESS | independent | counts reproduce; wording fixed |
| First dossier pass (`checks/audit/`) | exact screen; aggregate dual; own exact sssd and smallinvDAX constructions; own emfl050_3_3 lower bound; spring scan | own code | consistent; not reviewed |
| This pass (`checks/audit-r2/`) | exact recount; margins; aggregate; spring scan; **exact `.gms`/OSIL identity (23 instances + controls)**; **second rocket proof** | own setup and drivers; reuses the status track's `.gms` parser and the first verifier's interval code | consistent; **not reviewed** |

**Remaining assumptions.**

- *Display hypothesis H* (Section 3.2). All 22 refutations need only H
  (less than one display unit), which covers rounding and truncation.
- *Model identity in time.* Archive gaps (Section 1.5): March–December 2014
  for nine instances; topopt 2020-01 to 2022-05 rests partly on file dates.
- *Arithmetic.* 12 of the 19 pairs (smallinvDAX ×4, sssd ×4, water ×2,
  nd_netgen ×2) have a proof in exact rational arithmetic only. The other 7
  (glider100 ×2, ghg_3veh ×2, methanol50, nuclear14, topopt) rest on
  Krawczyk tests in two implementations, both assuming IEEE binary64 for the
  matrix products. For methanol50, nuclear14 and topopt the first verifier's
  enclosures are rational (no transcendental function); exp enclosures are
  needed for glider100, ghg_3veh and rocket. The audit additionally assumes
  correct mpmath `iv`; the first verifier assumes mpmath's exp/log accurate
  to 1e-60 at 90 digits. The rocket proofs now have two implementations with
  these two different exp assumptions.
- *Inferences.* "A solver reported a local solution as its bound" is an
  inference from equal displayed values (glider100 p1, methanol50 p3,
  sssd p2, ghg_3veh p1, nd_netgen p1 for GUROBI, rocket p1), not verified.

## 7. Relation to prior work

Slugs refer to `literature/papers/`. No literature track searched
specifically for prior audits of benchmark bounds (AUD-2); the items below
come from the local knowledge base.

- **MINLPLib.** Bussieck, Drud, Meeraus 2003
  (`bussieck2003-minlpliba-collection-of-test-models`); site documentation
  and FAQ (`vigerske2026-minlplib-a-library-of-mixed`,
  `vigerske2026-minlplib-documentation-database-snapshot-2026`); Vigerske's
  MAGO 2014 slides (`vigerske2014-towards-minlplib-2-0`): dual bounds
  collected from ANTIGONE, BARON, Couenne, Lindo and SCIP, "No way to verify
  correctness of bound!", and the conservative rule to trust a bound only if
  verified by at least two other solvers. The audit supplies the
  verification that the slides call impossible from the listing alone, for
  the pairs a listed point decides, and shows that the conservative rule
  protected the aggregate.
- **Benchmark consistency checking.**
  - COCONUT: Neumaier, Shcherbina, Huyer, Vinkó 2005
    (`neumaier2005-a-comparison-of-complete-global`) count wrong global and
    infeasibility claims, check near-feasibility of the best points with
    solcheck at tolerance 1e-5, and state: "In a later stage of testing we
    intend to prove rigorously the existence of a nearby feasible point."
    Shcherbina et al. 2003
    (`shcherbina2003-benchmarking-global-optimization-and-constraint`)
    describe the benchmarking protocol with approximate and rigorous
    verification modes. The audit performs that rigorous step for listed
    MINLPLib points against listed bounds.
  - PAVER 2.0 (`bussieck2014-paver-2-0-an-open`): marks runs whose bounds
    contradict known bounds; the Examiner checks solutions against
    tolerances.
  - MIPLIB 2017 (`gleixner2021-miplib-2017-data-driven-compilation`):
    solution checker in GMP arithmetic but with tolerances; instances with
    primal/dual inconsistencies across solvers were removed from the
    benchmark set; exact objective values after fixing integers via SoPlex
    with iterative refinement.
  - QPLIB (`furini2018-qplib-a-library-of-quadratic`): distinguishes
    complete from rigorous solvers; none of its solvers is rigorous.
- **Wrong results of floating-point solvers and exact verification.**
  Neumaier–Shcherbina 2004 (`neumaier2004-safe-bounds-in-linear-and`);
  Jansson 2004 (`jansson2004-rigorous-lower-and-upper-bounds`); exact and
  certified MIP (`cook2013-a-hybrid-branch-and-bound`,
  `cheung2017-verifying-integer-programming-results`,
  `eifler2023-a-computational-status-update-for`,
  `wood2026-satisfiability-modulo-theories-for-verifying`); a posteriori
  analysis of SCIP's branch-and-bound decisions
  (`hoen2025-analyzing-the-numerical-correctness-of`).
- **Rigorous feasibility verification (basis of route B).** Krawczyk 1969
  (`krawczyk1969-newton-algorithmen-zur-bestimmung-von`), Moore 1977
  (`moore1977-a-test-for-existence-of`), Rump 2010
  (`rump2010-verification-methods-rigorous-results-using`), Hansen 2004
  (`hansen2004-global-optimization-using-interval-analysis`), Kearfott 1998
  (`kearfott1998-on-proving-existence-of-feasible`: square subsystems of
  underdetermined equality systems, perturbing points away from active
  bounds), Kearfott 1996
  (`kearfott1996-rigorous-global-search-continuous-problems`),
  Füllner, Kirst, Otto, Rebennack 2024
  (`fullner2024-feasibility-verification-and-upper-bound`: approximate
  active index sets for inequalities, as in route B's active-row
  selection). Route B and route C apply these classical tools; no
  methodological novelty should be claimed for them.
- **Instance sources:** COPS
  (`dolan2001-benchmarking-optimization-software-with-cops`,
  `dolan2004-benchmarking-optimization-software-with-cops`;
  `library2026-cops-and-gams-source-models`); perspective reformulations
  (`gunluk2010-perspective-reformulations-of-mixed-integer`,
  `frangioni2006-perspective-cuts-for-a-class`). Bulirsch et al. 1993,
  Elhedhli 2006, Shiau–Michalek 2011, Quist et al., Frangioni et al. 2011,
  Laird et al. 2006, Schelbert 2015, Sandgren 1990, Silver–Moon 1999 and
  Bryson 1999 are cited on the MINLPLib pages but are not in `literature/`.
- **Related findings of this project:** SCIP's wrong optimal values on
  waterno2 subproblems (separate family) are not visible in listed data.

## 8. Critical examination

### 8.1 What I re-derived and recomputed

- Proposition 1 and its corollaries; Lemma 1 (new) makes the display
  hypothesis explicit and shows that all 22 refutations need only "less than
  one unit".
- Proposition 2 (Krawczyk), including the step from `R F(x*) = 0` to
  `F(x*) = 0` and the box check's handling of equality rows. I read
  `verify.py` (`krawczyk`, `resid_jac`, `to_float_enclosure`,
  `check_on_box`, `polish_and_verify`) and the first verifier's `kraw.py`:
  - every term of the test is bounded with the γ_n analysis; the remaining
    relative roundings are covered by `(1 + 1e-6)²` (audit) or by factor 2
    and `1 + 1e-12` (verifier);
  - the audit's inner radius uses the smaller of the two one-ulp-widened
    distances, so `T(X)` lies inside the box actually used;
  - non-basic variables keep exact decimals or exact bounds; integer
    variables are rounded and then integral by construction; their bounds
    are checked exactly.
- `cert_socp.py`, `cert_topopt.py`, `cert_ndnetgen.py`, `cert_linear.py`
  and `audit.py classify`: the structure assertions match Proposition 3 and
  the constructions in Section 3.3; exact objectives are floored at 30
  decimals and the classification adds 1e-30 for the upper end.
- Proposition 4: the reduction, the convexity identity and the evaluation at
  `(9, 0.283)`.

Cheap checks run in this pass (`checks/audit-r2/`, all in seconds):

| check | result |
|---|---|
| exact-decimal recount and screen | 1633 / 2816 / 11086 (11031) / 19; 158 pairs (46, 56, 131), 110 "other"; 3851 ties (1133); no beyond-dual point skipped for infeasibility; pair set equals `screen.json` |
| margins of 31 (i)/(i-r) pairs | all agree with `results.json` and the reports; min units over (i) 1.1158; max units over (i-r) 0.435 |
| class recount | 11/8/12/12/63/25 pairs; instance lists as in Section 5.5 |
| aggregate dual | 585/589 rule; no family instance's aggregate beaten beyond rounding |
| spring scan (60 digits) | 210 feasible; `f*`, runner-up and third value reproduced |
| emfl displays | literal and widened shortfalls (Section 5.3) |
| `.gms` vs OSIL, exact | identical for 23 instances incl. 14 class (i); methanol50 objective only; three negative controls detected |
| rocket, second implementation | all three refutations reproduced (Section 5.4) |
| operators and integrality | no nonsmooth operator in the class (i) and rocket files; no integer variable in the emfl files |
| mpmath `iv` conversions | decimal strings and big integers enclosed outward |

**No finding invalidates a claimed result.**

### 8.2 Issues and proposed resolutions

**AUD-1 (minor; wording).**
- The summary lists "an exact duality certificate" among the proofs of
  invalidity; duality certificates prove validity (emfl).
- SYNTHESIS.md and closing-research-results.md speak of an audit of "all
  MINLPLib listed bounds"; the audit screens all listed bounds against all
  listed points and can refute only bounds that a listed point beats.
- The summary's rocket100 margin "1.1e-7" is a rounded-up size (1.069e-7).
*Resolution:* in the paper, "proved by exact rational arithmetic or an
interval Krawczyk existence test", "a screen of all 11,086 listed per-solver
bounds against all 2,816 listed points", and "at least 1.06·10⁻⁷".

**AUD-2 (major for novelty wording; does not affect results).** No
literature track searched for prior audits of MINLPLib bound data or for
earlier rigorous checks of published bounds. The knowledge base shows the
closest prior practice: COCONUT (tolerance-based near-feasibility, rigorous
existence announced as future work), MIPLIB 2017 (exact arithmetic with
tolerances; inconsistent instances removed), PAVER (tolerance-based
consistency checks).
*Resolution:* a targeted search (about 1–2 hours, no computation): "MINLPLib
dual bound wrong/verification", COCONUT follow-ups (Neumaier, Shcherbina,
Domes; GloptLab `domes2009-gloptlab-a-configurable-framework-for`),
Domes–Neumaier 2015 "Rigorous verification of feasibility" (not in the
knowledge base), MINLPLib/GAMS performance-world reports, QPLIB and MIPLIB
solution-checking follow-ups, Mittelmann's benchmark notes. Until then, phrase
any priority statement with its search scope.

**AUD-3 (minor; resolved here, needs review).** Exact `.gms`/OSIL identity
now covers 14 of 15 class (i) instances, rocket ×3 and emfl ×4 (Section
1.5); methanol50 was already handled.
*Resolution:* state that the certificates hold for both forms. Ask an
independent reviewer to rerun `gms_osil_drive.py` and `gms_osil_drive_fn.py`
on copies (under a minute) and, ideally, to compare with their own `.gms`
reader. lop97icx and stockcycle are (i-r) and need no change.

**AUD-4 (minor; resolved here, needs review).** The rocket refutations had
one rigorous implementation. `checks/audit-r2/rocket_kraw.py` adds a second
(the first verifier's rational interval arithmetic and Krawczyk code, own
setup). Both share the authors' thrust values and the decomposition idea,
which is the same level of independence as for the 19 pairs (shared listed
points).
*Resolution:* include it; ask a reviewer to rerun it (seconds per instance).

**AUD-5 (minor; replayability).**
- topopt p5: the committed certificate's basis is not saved, and the centre
  file prints basic values at 25 digits and `c_e` at 45 digits, so it is not
  an exact certificate. A one-thread regeneration selects another exactly
  feasible point (10.33547432783171797…; `check_display.py` then reports
  ok 80, failed 12). The first verifier's construction is deterministic up
  to the Krawczyk centre and gives ≤ 10.335474275747004.
- emfl: the rational dual vectors `y` are not saved (audit and recheck).
*Resolution:* in the paper, cite topopt as "objective ≤ 10.33548 (three
independent exactly feasible points)" or use the verifier's value. For the
release, regenerate the topopt certificate in a disposable copy with the
basis list and the exact `c_e` written out, and save rational `y` for emfl
(seconds to minutes each).

**AUD-6 (minor; trust base).** Seven class (i) pairs depend on Krawczyk
tests with IEEE and library assumptions. List them separately from the 12
exact-only pairs. *Optional:* an all-rational Krawczyk test for ghg_3veh
(n = 52; exp enclosed by a Taylor series with remainder bound; under an hour
of work, seconds to run) and nuclear14 (n = 434, sparse rational products;
minutes). Not needed for the claims.

**AUD-7 (minor; interpretation).** The audit compares gross margins with
"common 1e-4 relative gap tolerances". A dual bound computed as a minimum
over open nodes stays valid at any gap tolerance; a gap tolerance can make a
reported bound invalid only if the solver prunes within the tolerance or
reports an incumbent value as its bound.
*Resolution:* say the seven 1.2e-5–7.3e-5 cases are "consistent with pruning
or reporting at a 10⁻⁴ gap tolerance", and keep "local solution reported as
bound" labelled as an inference.

**AUD-8 (minor; coverage).** 19 (or 22) is a lower bound. Display ties
(3851) cannot be decided, and rocket shows that ties can hide invalid bounds.
Class (iii) contains a likely invalid case: oil, where ANTIGONE and LINDO
list −0.93249394 (equal to the 2001 point p1), p2 (−0.93250817, primal
section, violation 7.1e-11) lies 1.42e-5 lower, and GUROBI lists p2's value
as its bound. Its active system has 1408 rows of rank 1391.
*Resolution:* state coverage limits. Optional: identify the 17 dependent
rows; if they are functionally implied by the others (for example
identical parallel pipes made equal), drop them, prove existence for the
reduced system and verify the dropped rows identically. Estimate: several
hours of agent work, seconds of compute; result would add two class (i)
pairs (gross label, 1.5e-5 relative).

**AUD-9 (minor; counting).** The 19 pairs are 15 distinct numerical
conflicts (Section 5.1). *Resolution:* say so or footnote it.

**AUD-10 (minor; display hypothesis).** The audit's class (i) rule uses half
a unit, an implicit round-to-nearest assumption. *Resolution:* state
Hypothesis H and Lemma 1 (Section 3.2) in the paper; all 22 refutations
exceed one unit, and the 19 class (i) margins also exceed 10/9 units, which
covers chains of truncations.

**AUD-11 (minor; emfl displays).** "At least 1.42e-5" and "at least 6.87e-6"
are true for the displayed numbers, but cover the underlying point values
only as "at least 1.41e-5" and "at least 6.86e-6". *Resolution:* use the
widened values, or say "the displayed value".

**AUD-12 (minor; new observation, reproduced).** emfl050_3_3 is marked S,
yet its best listed dual is at least 1.166e-6 relative below the exact
optimum.
*Resolution:* state it as a consequence of the reviewed lower bound; no
claim that the S mark is wrong (it is defined with tolerance-feasible
points).

**AUD-13 (minor; framing).** Neither the audit nor the summary says that
MINLPLib's aggregate dual is untouched. *Resolution:* include the sentence
in Section 9; both dossier passes reproduce it from the data (seconds).

**AUD-14 (minor; data date).** MINLPLib is live. *Resolution:* date-stamp
every table ("pages of 2026-09-30, refreshed 2026-10-02") and archive the
pages with the release.

**AUD-15 (minor; process).** This pass's two new checks (AUD-3, AUD-4) and
the first pass's checks are not independently reviewed. Several earlier
reviews ran read-only display checkers inside `R/bound-audit`; that does not
affect results.

## 9. What the paper may and must not claim

**May claim** (suggested wording):

1. "We screened all 11,086 per-solver dual bounds displayed on the 1,633
   MINLPLib instance pages (fetched 2026-09-30) against the 2,816 listed
   solution points. In 158 (bound, point) pairs the displayed bound lies
   beyond the displayed objective value of the point."
2. "For 19 of these per-solver bounds, on 15 instances, we prove that the
   instance, with its decimal data read exactly, has an exactly feasible
   point whose objective value is better than the bound by more than one
   unit in the bound's last displayed digit. Hence no number that rounds or
   truncates to the displayed value is a valid dual bound. Each proof uses
   exact rational arithmetic or an interval Krawczyk existence test, and
   each was confirmed by a second, independently written implementation."
3. "Because exactly feasible points satisfy every feasibility tolerance,
   these conclusions do not depend on solver or library tolerances."
4. "Eleven of the 19 margins exceed 10⁻⁶·|d|. In four, the error exceeds 1%
   of |d|: COUENNE and LINDO on glider100 (the proven objective value is
   about 784 times the listed bound), LINDO on topopt-cantilever_60x40_50
   (3.4 times the objective of an exactly feasible point) and LINDO on
   methanol50 (1.2% of |d|; 9.8·10⁻⁵ absolute). The other eight lie between
   1.9·10⁻⁹ and 3.3·10⁻⁷ of |d|, below MINLPLib's gap tolerance of 10⁻⁶;
   they do not contradict any solved mark."
5. "The instances' GAMS and OSIL forms are the same model, exactly, for 14
   of the 15 instances; for methanol50 the forms differ only in rounded
   objective coefficients, and the conclusion holds for both." (after
   AUD-3 review)
6. "In none of these instances does an invalid entry change MINLPLib's
   aggregated dual bound (the third-best per-solver bound) beyond display
   rounding."
7. "glider100, as distributed, has an exactly feasible point with objective
   −983,842.26, against the best listed primal value −1,255.06. The point
   is a spurious period-2 solution of the discretization, not a physical
   trajectory."
8. "For the four emfl second-order-cone instances we prove that every listed
   dual bound is valid and enclose the optima to within 3.4·10⁻¹¹. All
   listed point values except one lie below the exact optimum, by up to
   4.3·10⁻⁴ relative; for the solved emfl050_3_3 the listed optimal value
   lies at least 1.36·10⁻⁶ relative below it."
9. "We prove the global optimum of spring, 0.846245665643154281…; the five
   displayed dual bounds 0.84624567 equal its eight-decimal rounding."
10. "Outside the screen, LINDO's bounds on rocket100, rocket200 and rocket400
    are invalid by at least 1.06·10⁻⁷, 4.7·10⁻⁸ and 1.89·10⁻⁷ (tolerance scale),
    shown with exactly feasible points near points we computed, in two
    independent implementations." (the second after AUD-4 review)
11. "According to archived copies, the models of the refuted entries are
    unchanged since the bound dates, except for the rounding of three
    constants in ghg_3veh, for which the refutation also holds on the old
    text; for nine instances added in February 2014 no copy covers
    March–December 2014."
12. A priority sentence such as "To the best of our knowledge, this is the
    first audit of MINLPLib's per-solver bounds that decides conflicts by
    proofs of exactly feasible points" only after AUD-2, with the search
    scope named.

**Must not claim:**

- that a solver (or its current version) has a bug, or that a particular
  mechanism produced a bound: versions, options and runs are unknown, and
  "reported a local solution as a bound" is an inference;
- that MINLPLib's aggregated dual bounds, solved marks or `.solu` values are
  invalid; only per-solver page entries are refuted, and emfl050_3_3's S
  mark is defined with tolerance-feasible points;
- that the 19 (or 22) are all invalid bounds in MINLPLib, or that any
  display tie, (ii)-repair or (iii) bound is valid or invalid;
- that the (i-r) solver bounds are invalid (only the displayed numbers are),
  or that the six-digit rounding explanation for eniplac, lop97icx and
  stockcycle is proved;
- anything about the continuous glider or rocket problems;
- that the tolerance-scale cases contradict solved marks;
- that route B, route C or the SOCP certificates are methodologically new.

## 10. Candidate figures and tables

1. **Pipeline figure.** 1633 pages → 11086 bounds × 2816 points → screen
   (158 pairs, 3851 ties) → exact evaluation of 56 points → existence proofs
   (route A exact, route B Krawczyk, route C shift, dedicated exact
   certificates) → classes (131 pairs), with counts at each stage.
2. **Margin scatter (main figure).** x: margin in display units (log); y:
   `(d − f)/|d|` (log); vertical lines at 0.5 (audit slack) and 1 unit
   (Hypothesis H); horizontal lines at 10⁻⁶ (MINLPLib gap tolerance) and
   10⁻⁴; 31 (i)/(i-r) pairs filled, rocket ×3 hollow; colour by solver.
   Data: `checks/audit-r2/margin_figure.csv`.
3. **Table:** the 19 class (i) pairs (Section 5.1) with the second
   implementation's value.
4. **Table:** (i-r) pairs and explanations (Section 5.2).
5. **Table:** emfl enclosures, listed duals and listed primal shortfalls
   (Section 5.3).
6. **Table:** model evidence per refuted instance: archived copies and
   exact `.gms`/OSIL identity (Section 1.5).
7. **Optional figure:** glider100 altitude and vertical acceleration against
   node for p1 and the proven p2 (period-2 oscillation, final time 62163 s),
   from `R/bound-audit/sol/glider100.p*.sol` and
   `logs/verify/glider100.p2.center.sol`.
8. **Appendix box:** Lemma 1, Propositions 1–4 with proofs, the Krawczyk
   floating-point terms and the trust base.

## 11. Commands run in this pass

All in `/tmp/audit-dossier2` on copies, one process,
`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`; each finished in seconds. Scripts
and logs are in `checks/audit-r2/` (README there).

```
python3 recount.py         # exact recount and screen
python3 margins.py         # margins of the 31 (i)/(i-r) pairs
python3 solu.py; python3 agg.py      # aggregate dual
python3 spring_scan.py     # 1100 assignments at 60 digits
python3 figdata.py; python3 safe_margins.py
cd xf; python3 drive.py <18 instances>; python3 drive_fn.py <6 instances>   # exact .gms vs OSIL
cd xf/ctl; python3 drive.py sssd20-04persp spring; python3 drive_fn.py ghg_3veh   # negative controls
cd rocket; python3 rocket_kraw.py 100; ... 200; ... 400   # second rocket proof
python3 class_recount.py; python3 emfl_shortfalls.py
# inline: operator grep, emfl integer-variable count,
#         mpmath iv outward-conversion test, Krawczyk parameters from logs/verify/*.json
```

Read-only inspection: `R/bound-audit/{audit.py, verify.py, cert_*.py,
results.json, logs/}`, the reviews and track reports named in Section 6, the
stored site pages, and the literature files cited in Section 7. These are
targeted checks, not project-wide verification, and not CI.
