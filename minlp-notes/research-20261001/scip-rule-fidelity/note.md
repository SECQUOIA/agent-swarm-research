# Does the "SCIP's set" model match SCIP 10.0.3, and how far are SCIP's cuts from the corner bound?

Stream `scip-rule-fidelity`, research-20261001 (program:
[`../PROGRAM.md`](../PROGRAM.md)). Work began 2026-10-01 and continued
2026-10-02. A first author agent built the instrumented SCIP, ran all SCIP
jobs and analysed the generator dumps, then stopped at a usage limit
without writing a note. This note was written in the continuation, which
re-checked that work, completed the MINLPLib analysis and wrote up the
results. The repository later included this stream in commits made outside
this program. This revision makes no commits and does not change the
index, branch or HEAD.
**Final status (2026-10-04): reviewed in two rounds; r2 minor fixes applied;
the last revision's fixes checked by the coordinating agent; not refereed.**
The coordinating agent checked the numbers log and SCIP source for the ray-scaling claim.
The independent research-agent review in round 2 confirmed all round-1
fixes and gave "minor fixes": one minor issue, one optional item and two
nits. "Reviewed" means
checked by another research agent, not journal peer review. See
[`reviews/review-r1.md`](reviews/review-r1.md),
[`reviews/review-r2.md`](reviews/review-r2.md) and the revision sections below.

Code: [`code/`](code/). Raw outputs: [`logs/`](logs/). Instrumentation
patch: [`patch/nlhdlr_quadratic_dump.diff`](patch/nlhdlr_quadratic_dump.diff).
Earlier note: [`../../research-20260928b/sfree/optimal-intersection-cuts.md`](../../research-20260928b/sfree/optimal-intersection-cuts.md)
(cited as "the sfree note").

## Summary

**Main answer.** The sfree note's Python model of "SCIP's set" matches the
intersection cuts SCIP 10.0.3 actually computes, and the gap that SCIP's
single cuts leave below the corner bound is small in the median on the
McCormick generator but large on the MINLPLib corners where the corner bound is
positive. On most MINLPLib corners the corner bound is 0, so no single cut
can improve it.

1. *What SCIP builds* (Section 1, from the source): the Chmiela–Muñoz–Serrano
   Cases 1–4 with the point rule `λ = x̂(s̄)/‖x̂(s̄)‖`, tableau rays of all
   nonbasic columns and row slacks projected on the constraint variables,
   steps from a closed-form root with a bisection fallback. Notable details
   that are not in the documentation: the cut limit is a per-expression
   count of *generated* cuts, reset at restarts (20 checked at the root,
   2 in the tree), and the parameters `ignorebadrayrestriction` and `ignorenhighre`
   do the opposite of what their descriptions say (both TRUE by default,
   both enable rejection tests). (Read from the source; the limit and the
   range/efficacy rejection are confirmed in the dumps.)
2. *Fidelity* (Section 4; computed from instrumented-SCIP dumps). On
   610,193 rays of 7,945 attempts (all generator attempts, 4,578 sampled
   MINLPLib attempts), the model reproduces SCIP's step lengths except on
   1,211 rays (0.2%). All 1,211 are classified: steps beyond `10^12`
   (819), SCIP reporting `∞` for steps beyond `8.6·10^9` (31), SCIP's
   conservative bisection fallback (307; SCIP's step shorter by at most
   `5.9·10^-4` in this sample; larger losses occur in the sibling stream),
   and rounding at huge steps or in the root formula (54).
   The case agrees in all 7,945 records, `κ` to relative `1.4·10^-13`, and
   the cut coefficients equal `1/t`. The
   earlier model's Case 4 is wrong for `κ ≠ 0` (a transcription slip in
   `scout_sfree.ms_set`, Section 7.2). It disagrees with SCIP on 91% of
   such rays, but no earlier result used that case.
3. *How far below the corner bound* (Section 5; numerical evidence with
   validated codes, floating-point `z_K` or solver-reported Gurobi values;
   exact checks are identified in Sections 5 and 7.1). On the
   generator, `z_C/z_K` of SCIP's actual sets has median 0.976 (mc11) and
   0.992 (mc12) over all attempts. It is below 0.9 in 35% and 25% of
   attempts and below 0.5 in 11% and 7%; instance-weighted, below 0.9 in
   23% and 20%. Redoing the sfree note's statistic: SCIP's set is below
   `0.9 z_K` in 27 of the note's 120 corners and below `0.5 z_K` in 3 (26
   and 3 before the correction below); on SCIP's own first-LP corners the
   counts are 28 and 4. On MINLPLib, 73% of the sampled corners are
   degenerate (a zero-cost face meets `S`, so `z_K = 0`) and 4% have all
   rates zero. On the remaining 1,067 corners (26 instances, classified
   by the reduced-space numerical test), the median
   ratio is 0.923 per corner and 0.818 instance-weighted; 48% (54%
   instance-weighted) are below 0.9 and 35% (43%) below 0.5, while 29% equal
   1. In 187 of the 371 low-ratio records (half), SCIP's set exits a
   zero-rate ray at a finite step. No intersection with `S` is found along
   183 of those rays; four reach `S` in the dumped data through tiny
   drift lost in the reduced-space test.
4. *Failures and rejections* (Section 6; computed exactly from the dumps).
   On MINLPLib only 37.7% of 76,914 attempts produce a cut. 49.5% abort on
   the dynamism test, and 12.7% abort on a free nonbasic variable. Every
   dynamism abort meets the coefficient-ratio threshold by definition.
   Among 1,799 sampled first-piece aborts, `min/max |A,B,C|` has median
   `4.6·10^-18`; 493 (27.4%) are below `10^-25`. A rounding diagnostic
   finds 36 of 138 first-piece aborts (26.1%) consistent with zero at its
   tolerance. Only `A` is tiny in 1,270/1,799 sampled first-piece aborts
   (70.6%) and 28,071/34,834 in all dumps (80.6%); in 1,209 of the 1,270,
   it exceeds the `64u` rounded-zero diagnostic threshold (`u = 2^-53`).
   SCIP does not normalise rays, and its test depends on ray length,
   although rescaling the ray and converting the coefficient back leaves
   the cut unchanged in exact arithmetic. Rescaling would make the
   first-piece test pass for
   1,728/1,799 sampled aborts (96.1%) and 31,926/34,834 in all dumps
   (91.7%). Whether the short ray components are LP noise and whether
   these cuts would be safe remain open. Of the generated cuts, 14.3% are
   rejected by clean-up or the range/efficacy test. Of the
   checkable cuts handed to SCIP, at least 14% (MINLPLib) and 28–39%
   (generator) are later observed in the LP. These are lower bounds
   on entry rates; cuts can enter and leave between observations. On the
   generator
   only 2 of 3,367 attempts fail and 5 generated cuts are rejected.
5. *Correction to the sfree note* (Section 7.1; certified in exact
   arithmetic). Ten of its 120 stored corner bounds in Section 9.2 were too
   small, because `core.two_ray` fails on antiparallel scaled rays. The
   corrected means of the corner increment are 0.724/0.616 (SCIP's set) and
   0.783/0.675 (orbit = corner bound), instead of 0.700/0.591 and
   0.755/0.648. "The orbit set attains `z_K` in all 120 corners" still
   holds. The loop experiments of its Section 9.3 change in the orbit and
   corner columns but not in their conclusion.

**Solver relevance.** These are measurements of SCIP's existing cuts
(intersection cuts are off by default). They suggest where a better choice
of set could matter: non-degenerate corners with cheap rays. They also show
that on MINLPLib the dynamism abort, degeneracy and cut selection limit the
effect of any set choice. The abort counts do not establish that rounding
noise is the main cause, or that relaxing the test would be safe. They do
not show that a different set would speed up SCIP; no solver-level
experiment was run.

Background processes: every process started by this stream has finished
(checked with `ps` before writing this note); none is running.

---

## 1. What SCIP 10.0.3 builds

Source: `scip/src/scip/nlhdlr_quadratic.c` of SCIP 10.0.3 (read in the
read-only tree `/workspace/local-home/build-scip/scipoptsuite-10.0.3`), and
Chmiela–Muñoz–Serrano, "On the implementation and strengthening of
intersection cuts for QCQPs" (ZIB report 20-29; Math. Program. 197, 2023),
pp. 11–14 of the report (copy in
`research-20260928b/scouting/s-free-intersection-cuts/sources/`). Function
names below are those of `nlhdlr_quadratic.c`.

### 1.1 Which expressions get cuts, and when

*Detection* (`nlhdlrDetectQuadratic`). The handler looks at expressions
that are sums of at least two terms and quadratic (`SCIPcheckExprQuadratic`).
It takes the separation role for the lower (upper) side only if no other
nonlinear handler already enforces that side, the eigendecomposition is
available, and the quadratic is not convex (not concave). Intersection cuts
are switched off in sub-SCIPs. The detection priority is 1, low, so the
higher-priority handlers (for example the second-order cone, convex and
concave handlers) take their expressions first. The eigendecomposition
exists only if SCIP was built with LAPACK or Ipopt
(`SCIPcomputeExprQuadraticCurvature`); with `LAPACK=OFF` and `IPOPT=OFF`
the handler never generates an intersection cut (confirmed in Section 2).

*Enforcement* (`nlhdlrEnfoQuadratic`). A cut is attempted for an expression
and a violated side only if all of the following hold:

1. intersection cuts are on (`useintersectioncuts`, default FALSE in 10.0);
2. the side to separate is not the convex one (for `q ≤ rhs`, `q` is not
   convex; for `q ≥ lhs`, not concave);
3. the point is the current LP solution (`sol == NULL`), the LP is solved to
   optimality and the solution is basic;
4. the node depth `d` satisfies `d mod atwhichnodes = 0` (default 1: every
   node; `−1`: root only);
5. a per-expression counter is below the limit: at the root,
   fewer than `ncutslimitroot = 20` cuts generated so far for this
   expression; at depth `> 0`, fewer than `ncutslimit = 2`. The counter
   (`nlhdlrexprdata->ncutsadded`) counts *generated* cuts (incremented
   before the clean-up test) and is not reset between nodes. A restart
   frees and re-detects the expression data, resetting the counter to 0.
   Within each solve run between restarts, an expression that received two
   or more cuts at the root gets no further cut in the tree, and every
   expression gets at most two in the tree. In `ex1264`, new expression
   addresses at LP 113 have counter 0 after the root restart; before it,
   LPs 1–77 used counters up to 18. The
   parameter description ("limit for number of cuts generated
   consecutively") does not say this; a node-based limit is present but
   commented out;
6. the violation is at least `minviolation = 1e-4` (absolute violation
   `|auxvalue − aux|` for a subexpression, `max(lhs − q, q − rhs)` for a
   constraint);
7. the expression is not both the root of one constraint and a
   subexpression of another;
8. for a constraint root, the violation is at least the feasibility
   tolerance.

When the quadratic is a subexpression with an auxiliary variable `z_a`, the
handler separates `q(z) − z_a ≤ 0` (or `≥ 0`); when it is the root of a
constraint, it separates `q(z) ≤ rhs` or `q(z) ≥ lhs` directly. In both
cases the violated side is rewritten as `q(s) ≤ 0` in the space of the
constraint variables `s = [quadratic variables, linear variables,
auxiliary variable]`, multiplying by `−1` for the `≥` side ("sidefactor").

### 1.2 Rays

`createAndStoreSparseRays`: one ray per nonbasic LP column and per nonbasic
row slack, read from the simplex tableau rows of the basic constraint
variables. The ray is the direction in which the nonbasic variable moves
away from its active bound by one unit (for a row: the row activity moves
away from its active side by one unit). Only the components on the
constraint variables are kept, entries with `|·| ≤ 10^-9` (`SCIPisZero`)
are dropped, and rays that are zero on the constraint variables are not
stored. If a constraint variable or a nonbasic column with a nonzero ray is
nonbasic free ("basis status ZERO"), the attempt is aborted.

With `useboundsasrays = TRUE` (default FALSE) the rays are instead the
coordinate directions from the nearest box vertex, which must itself
violate the constraint; this variant is not used for subexpressions.

### 1.3 The set

`intercutsComputeCommonQuantities`. Let `Q = Σ_i θ_i v_i v_i^T` on the
quadratic variables (signs already flipped for the `≥` side), `b` the
linear coefficients, and `I_+, I_−, I_0` the indices of positive, negative
and zero eigenvalues (zero means `|θ_i| ≤ 10^-9`). With
`x_i(s) = √θ_i (v_i^T s + v_i^T b/(2θ_i))` (`i ∈ I_+`),
`y_i(s) = √(−θ_i) (v_i^T s + v_i^T b/(2θ_i))` (`i ∈ I_−`),
`κ = c − ¼ Σ_{i ∈ I_+ ∪ I_−} (v_i^T b)^2/θ_i` (set to 0 if `|κ| ≤ 10^-9`)
and `w(s) = Σ_{i ∈ I_0} (v_i^T b)(v_i^T s) + b_l^T s_l − s_a` (the linear
variables and, if present, the auxiliary variable with coefficient `−1`),
the violated side is `‖x(s)‖^2 − ‖y(s)‖^2 + w(s) + κ ≤ 0`. Case 4 is
declared whenever there are linear variables, an auxiliary variable, or a
nonzero quadratic-variable coefficient of `w` (an exact `!= 0.0` test).
With `s̄` the LP point:

| Case | Condition | Set `C` | `λ` |
|---|---|---|---|
| 1 | `w ≡ 0`, `κ = 0` | `‖y(s)‖ ≤ λ^T x(s)` | `x(s̄)/‖x(s̄)‖` |
| 2 | `w ≡ 0`, `κ > 0` | `‖y(s)‖ ≤ λ^T (x(s), √κ)` | `(x(s̄), √κ)/‖·‖` |
| 3 | `w ≡ 0`, `κ < 0` | `‖(y(s), √−κ)‖ ≤ λ^T x(s)` | `x(s̄)/‖x(s̄)‖` |
| 4 | `w ≢ 0` | `φ_λ(ŷ(s)) ≤ λ^T x̂(s)` | `x̂(s̄)/‖x̂(s̄)‖` |

In Case 4, with `r = √(1 + κ^2)`,
`x̂(s) = (x(s), (w(s) + κ + r)/(2√r))`, `ŷ(s) = (y(s), (w(s) + κ − r)/(2√r))`,
so that `‖x̂‖^2 − ‖ŷ‖^2 = ‖x‖^2 − ‖y‖^2 + w + κ`, and, writing `λ_e` for the
last entry of `λ` and `ŷ_e` for the last entry of `ŷ`,
`φ_λ(ŷ) = ‖ŷ‖` if `ŷ_e ≤ λ_e ‖ŷ‖`, and
`φ_λ(ŷ) = √((1 − λ_e^2)(‖ŷ‖^2 − ŷ_e^2)) + λ_e ŷ_e` otherwise
(`computeRestrictionToRay`: pieces "4a" and "4b"). These are the
Muñoz–Serrano sets with the "point rule" `λ = x̂(s̄)/‖x̂(s̄)‖`, i.e. exactly
the sets the sfree note calls "SCIP's set" (sfree note, Sections 5 and 6.1).
The ZIB report (p. 13) writes `x̂, ŷ` with an extra overall factor
`(1 + κ^2)^{-1/4}`; this rescales `(x̂, ŷ)` by a positive constant and
gives the same set.

### 1.4 Step lengths and the cut

For each ray `r_j`, `computeRestrictionToRay` writes the gauge-like
function along `s̄ + t r_j` as `√(A t^2 + B t + C) − (D t + E)` (two such
pieces in Case 4), and `computeIntersectionPoint` returns its smallest
positive root `t_j` from the quadratic `(A − D^2)t^2 + (B − 2DE)t + (C − E^2)`
(interval arithmetic, `SCIPintervalSolveUnivariateQuadExpressionPositiveAllScalar`),
followed by a bisection if the root has `φ > 10^-10`. `t_j = ∞` if
`√A ≤ D`. In Case 4 the 4a root is used if it satisfies the 4a condition,
otherwise `max(t_4a, t_4b)`. The cut is `Σ_j λ_j / t_j ≥ 1` in the
nonbasic space (`1/∞ = 0`), translated to the structural variables with
the LP rows of the nonbasic slacks (`addColToCut`, `addRowToCut`).

### 1.5 Strengthening variants and their effect on the single-cut bound

The single-cut bound of a cut `Σ_j a_j λ_j ≥ 1` on the corner is
`z_C = min{w^T λ : λ ≥ 0, Σ a_j λ_j ≥ 1} = min_{j : a_j > 0} w_j / a_j`
(`w_j ≥ 0`: objective rate of ray `j`). Coefficients `a_j ≤ 0` do not
enter it.

- *Negative edge extension* (`usestrengthening`, default FALSE;
  `computeStrengthenedIntercut`, `findRho`): rays with `t_j = ∞` get a
  coefficient `1/ρ_j < 0`. No effect on `z_C`.
- *Minimal representation* (`useminrep`, default TRUE, Case 2 only): rays
  with `t_j = ∞` get a negative coefficient from the restriction to a line
  through the apex. No effect on `z_C`.
- *Monoidal strengthening* (`usemonoidal`, default TRUE, Case 2 only, rays
  of integer columns or integral rows): the coefficient comes from a
  quadratic root (`computeMonoidalStrengthCoef`) and can be smaller than
  `1/t_j`. This uses integrality, so the resulting `z_C` can exceed the
  continuous corner bound `z_K`. Records with monoidal coefficients are
  reported separately.

So with the default parameters the cut SCIP adds is the plain intersection
cut of the set in Section 1.3, except in Case 2 (monoidal coefficients on
integer rays, negative coefficients on rays that do not meet the
boundary).

### 1.6 Where an attempt can fail or be rejected

1. *Zero basis status* (free nonbasic variable with a nonzero ray): abort.
2. *`φ(0) ≥ 0`* (`computeRestrictionToRay` in Cases 1–3,
   `areCoefsNumericsGood` in all cases): the LP point is not strictly
   inside the computed set (numerically); abort the whole cut.
3. *Dynamism* (`areCoefsNumericsGood`): for some ray,
   `max(|A|, |B|, |C|)/min_{≠0}(|A|, |B|, |C|) ≥ 10^15`
   (`SCIPisHugeValue`), also for the 4b piece: abort the whole cut. This
   test runs only when `ignorebadrayrestriction = TRUE`, which is the
   default. The parameter description ("should cut be generated even with
   bad numerics when restricting to ray?") states the opposite of what the
   code does.
4. *Row not nonbasic enough* (`addRowToCut`): a nonbasic row whose activity
   is not at its side within the feasibility tolerance: abort.
5. *Clean-up* (`SCIPcleanupRowprep` with `mincutviolation = 1e-4`): the cut
   is scaled and cleaned (coefficient and side modifications); it is
   rejected if it is not violated by at least `1e-4` afterwards.
6. *Range/efficacy*: the cut is rejected if
   `max|coef|/min|coef|/efficacy ≥ 10^9`. The test is applied when
   `ignorenhighre = TRUE` (the default; code: `if( !ignorehighre || ratio < 1e9 )
   add`), and skipped when it is FALSE. Again the parameter description
   ("should cut be added even when range / efficacy is large?") states the
   opposite. The dumps confirm the default behaviour: 2889 MINLPLib cuts
   were rejected by this test (Section 6).

### 1.7 Parameters (`nlhdlr/quadratic/...`) and defaults

| Parameter | Default | Effect |
|---|---|---|
| `useintersectioncuts` | FALSE | master switch |
| `usestrengthening` | FALSE | negative edge extension (Section 1.5) |
| `usemonoidal` | TRUE | monoidal coefficients, Case 2, integer rays |
| `useminrep` | TRUE | minimal-representation coefficients, Case 2 |
| `useboundsasrays` | FALSE | box-vertex rays instead of tableau rays |
| `ncutslimit` | 2 | per-expression limit between restarts, checked at depth `> 0` (item 5 of 1.1) |
| `ncutslimitroot` | 20 | per-expression limit between restarts, checked at the root |
| `maxrank` | `INT_MAX` | declared, not used in the code |
| `mincutviolation` | `1e-4` | clean-up threshold |
| `minviolation` | `1e-4` | violation needed to attempt a cut |
| `atwhichnodes` | 1 | depths at which cuts are attempted |
| `nstrengthlimit` | `INT_MAX` | rays strengthened per cut |
| `sparsifycuts` | FALSE | replace nonbasic variables by bounds |
| `ignorebadrayrestriction` | TRUE | enables the dynamism abort (item 3 of 1.6) |
| `ignorenhighre` | TRUE | enables the range/efficacy rejection (item 6 of 1.6) |
| `trackmore` | FALSE | statistics only |

(`maxrank` appears only in the parameter definition; `grep` finds no other
use.)

## 2. Instrumentation and build

*Patch* ([`patch/nlhdlr_quadratic_dump.diff`](patch/nlhdlr_quadratic_dump.diff),
794 lines, `nlhdlr_quadratic.c` only; the diff of the copy against the
read-only source tree shows no other changed file). If the environment
variable `SCIP_INTERCUT_DUMP` names a file, every attempt of the main SCIP
(not of sub-SCIPs) that reaches `generateIntercut` writes one JSON line:

- LP count, node number and depth, constraint name, expression address,
  side (`over`), whether the expression is a constraint root, violation,
  LP objective value, the expression's cut counter;
- the quadratic as SCIP stores it (square, bilinear and linear
  coefficients, constant, sides), SCIP's own eigenvalues and eigenvectors,
  the LP values, local bounds and integrality of the constraint variables;
- every ray: sparse entries on the constraint variables exactly as stored
  by SCIP, LP position, basis status, reduced cost or row dual, column or
  row width (to recognise fixed columns and equality rows), name;
- the common quantities `vb, vzlp, wcoefs, w(zlp), κ`, the Case-4 flag,
  the side factor, the Case-2 flag, the apex and the monoidal flag;
- for every ray: step length `t`, cut coefficient, monoidal flag, and the
  restriction coefficients `A, …, E` of both pieces and the Case-4
  condition;
- the outcome: generated or not and why (zero basis status, `φ(0) ≥ 0`,
  dynamism, minimal-representation failures, row not nonbasic enough), the
  nlhdlr failure counters before and after, the raw and cleaned row,
  clean-up result and violation, efficacy and range/efficacy ratio,
  added or rejected;
- the names (LP numbers) of this expression's intersection cuts that are
  in the current LP.

At exit a counter line records how often each early return of
`nlhdlrEnfoQuadratic` (Section 1.1) was taken, plus the nlhdlr statistics.

*Build.* A copy of the SCIP 10.0.3 suite in `/workspace/local-home/build-scip/fidelity/src`
(the original tree and `build-suite` were not touched), built in
`/workspace/local-home/build-scip/fidelity/build`: Release, SoPlex 8.0.3, GMP on,
`IPOPT=off`, `PAPILO=off`, `LAPACK=on` with the system
`liblapack.so.3`/`libblas.so.3` (3.12.0) and `libgfortran.so.5` linked
through symlinks in `/workspace/local-home/build-scip/fidelity/lapacklib`, gcc
16.2.0. The first build had `LAPACK=off` like `build-suite`; it never
detected a quadratic for intersection cuts (0 detections on a `w = xy`
instance) because no eigendecomposition is computed. With LAPACK the same
instance gives 4 detections and 3 cuts, matching PySCIPOpt 6.2.1's bundled
SCIP (first author agent's checks, transcript; not repeated). Every run
below was made with the final binary (built 2026-10-01 23:43 EDT, before
all runs), and the first record of every one of the 168 dumps has the
`raywidth` field added in the final patch (or is a zero-basis-status abort,
which stops before the rays are written).

## 3. Runs

All runs: the instrumented binary with SCIP defaults except
`nlhdlr/quadratic/useintersectioncuts = TRUE`
([`code/intercuts_on.set`](code/intercuts_on.set)), via
[`code/run_scip.sh`](code/run_scip.sh) (time limit 60 s for the
generator, 120 s for MINLPLib; at most 7 parallel runs). Raw logs and dumps:
`logs/runs_mc11/`, `logs/runs_mc12/`, `logs/runs_minlplib/` (gzipped JSON
lines; 6.4 MB, 13 MB and 2.1 GB).

- *Generator.* [`code/gen_mccormick_cip.py`](code/gen_mccormick_cip.py)
  writes the random bilinear programs of `research-20260928b/sfree/code/exp_mccormick.py`
  as `.cip` files with the same seeding: seed 11, 4 variables, 4 products,
  3 random rows, trials 0–149 (`instances/mc11/`), and seed 12, 6 variables,
  8 products, 4 rows, trials 0–199 (`instances/mc12/`). Each product is a
  nonlinear equality `w_e = x_i x_j`; the McCormick rows are explicit
  linear rows, as in the earlier LPs. All 350 runs solved to optimality.
  SCIP attempted intersection cuts in exactly the 47 (seed 11) and 73
  (seed 12) instances that form the sfree note's Section 9.2 samples (I did
  not check why the others had no attempt). Attempts: 898 and
  2469; 97–99% at the root.
- *MINLPLib.* [`code/select_minlplib.py`](code/select_minlplib.py) with seed
  20261001 drew 64 of the 394 instances in
  [`sources/minlplib_instancedata.csv`](sources/manifest.txt) that have a
  quadratic constraint, constraint curvature not linear, convex or concave,
  no general nonlinear, polynomial or signomial constraints, at most 1000
  variables, and an OSiL file ([`instances/minlplib_sample.txt`](instances/minlplib_sample.txt)).
  30 runs finished, 34 hit the time limit. In 16 instances the handler's
  enforcement callback was never called (no dump is written then); the
  other 48 made 76,914 attempts.

## 4. Fidelity: recomputing SCIP's cuts

*Method* (`code/analyze.py`, `code/dumpio.py`, `code/model_vec.py`). For
every analysed attempt, the violated side `q(s) ≤ 0`, the LP point `s̄` and
SCIP's rays are rebuilt from the dump in SCIP's variable order. The Python
model computes its own eigendecomposition (NumPy), `κ`, the case, `λ` by the
point rule and the step length along every ray by bisection on the gauge
(200 iterations; no exit before `10^12` counts as `∞`). Two models are
compared with SCIP's dumped steps ray by ray (match = relative difference
`≤ 10^-6`, or both `∞`):

- **fixed**: the formulas of Section 1.3 (SCIP's code);
- **note**: the sfree note's `scout_sfree.ms_set` (Case 4 as in Section 7.2;
  Cases 1–3 identical to "fixed").

Records analysed: all 898 (mc11) and 2,469 (mc12) attempts; for MINLPLib a
uniform sample of 50 attempts per instance (seed 12345; all attempts if
fewer) plus, for the 26 instances with non-degenerate corners in that
sample, 150 further attempts (seed 54321, disjoint): 4,578 records with
rays, from all 48 instances. The two samples contain 4,785 records in
total, including 207 zero-basis-status aborts without rays (59 in the
first sample and 148 in the second, all 148 from `space25a`).
Rays of failed attempts after the failing ray have no SCIP step and are not
compared.

**Claim 4.1 (computed exactly from the dumps; floating-point
comparison).** On all compared rays, the "fixed" model reproduces SCIP's
step lengths: 7,532 of 7,533 rays (mc11), 36,263 of 36,263 (mc12) and
565,187 of 566,397 (MINLPLib, 0.21% mismatches), in all four cases,
including Cases 2, 3 and 4 with `κ ≠ 0`. SCIP's case equals the model's
case in all 7,945 records. Every one of the 1,211 mismatching rays (1 on mc11,
1,210 on MINLPLib) falls in
one of the classes below (`code/explain_mismatch.py`, which replays SCIP's
`computeIntersectionPoint` from the dumped coefficients; log
`logs/explain_mismatch.log`):

| Class | Rays | What happens |
|---|---|---|
| beyond the model's cutoff | 819 | SCIP's step is finite but `≥ 1.15·10^12`; the model reports `∞` (coefficient `≤ 9·10^-13`) |
| SCIP `∞`, true step huge | 31 | SCIP's test `√A ≤ D` says "no intersection" where the model finds a step `≥ 8.6·10^9` |
| bisection fallback, replayed exactly | 200 | the quadratic's root fails (typically a negative discriminant when the ray passes through the apex of the cone, where `φ` has a kink), SCIP bisects and stops at `|φ| ≤ 10^-6`; its step is shorter by at most `5.9·10^-4` (relative, in this sample) |
| bisection fallback, not replayed exactly | 107 | same mechanism (SCIP's step shorter in all 107, by at most `4.9·10^-4` in this sample); my replay cannot reproduce the outward rounding of SCIP's interval root, which decides whether the bisection runs |
| huge steps | 21 | steps `≥ 10^8`; both formulas lose accuracy there (largest relative difference 18.6, at steps of `8.5·10^11` vs `1.7·10^13`) |
| root formula rounding | 33 | no bisection; my replay reproduces SCIP's step, which differs from the model by at most `2.1·10^-5` |

So there is **no mismatch in the construction of the set**: the case
distinction (all 7,945 records), `κ` (largest
`|Δκ|/max(1,|κ|) = 2.8·10^-14`, absolute when `|κ| ≤ 1`;
largest relative difference `1.4·10^-13`, after SCIP's zeroing of
`|κ| ≤ 10^-9`), the point rule for `λ`, the Case-4 scaling and the
two-piece function all agree. The differences are in SCIP's root finder:
it is conservative (shorter step, hence a valid but weaker cut) when it
falls back to bisection. The small bisection losses above are
sample-specific: the sibling [`scip-set-selection` note, Section 4.3](../scip-set-selection/note.md#43-scips-own-root-finder-can-halve-a-step-observation)
shows the same fallback halving a step in `ex8_3_2`. SCIP also treats steps beyond
about `10^10` as `∞` or computes them with large relative error. The
latter could make a coefficient too small (`0` instead of about `10^-10`),
which is invalid in exact arithmetic, but only for points `10^10` units
along the ray. Matching rays agree closely: in records without any `diff`
ray the largest relative difference is `1.3·10^-10` (mc11), `2.4·10^-11`
(mc12) and `9.8·10^-7` (MINLPLib).

**The earlier model.** "note" agrees with "fixed" wherever `κ = 0` or the
case is 1–3, and therefore reproduces SCIP on all generator rays. On
MINLPLib Case-4 rays with `κ ≠ 0` it disagrees with SCIP on 17,584 of
19,376 compared rays (Section 7.2).

**Coefficients.** For every ray without a monoidal coefficient and with a
finite step, SCIP's cut coefficient is exactly `1/t` (largest relative
difference 0, all 7,619 analysed records with coefficient data). Of the
23,949 MINLPLib rays with `t = ∞`, 21,512 have coefficient 0 and 2,437 a
negative minimal-representation coefficient (Case 2); none is positive.
Monoidal coefficients occur in 140 of the 916 analysed Case-2 records.

**Claim 4.2 (computed from the dumps, floating-point check; end-to-end
check of the objective rates).** For every added cut that is later found in an LP of
the same node (via `lpcuts`), that LP's value is at least
`lpobj_L + z_cut`, where `z_cut = min_{a_j > 0} w_j/a_j` uses the dumped
coefficients and the rates (reduced costs, row duals) as signed in
`dumpio.rays`: 296 of 296 cuts (mc11), 595 of 595 (mc12) and 314 of 316
(MINLPLib; all 95 with non-negligible `z_cut`, i.e. `z_cut > 10^-6 max(1, |lpobj|)`), with tolerance
`10^-6 z_cut + 10^-7 max(1, |lpobj|)` (`code/check_rates.py`, log
`logs/check_rates.log`). The two MINLPLib exceptions are degenerate
corners (Section 5) with `z_cut ≈ 2·10^-7`, which comes only from the floor
`10^-9 max w` on zero rates; the LP gained `10^-13`. On the generator the minimum of
`(lpobj_next − lpobj_L)/z_cut` is exactly 1.000: the bound is often
attained, which a wrong sign or scale of `w` could not produce
systematically. An earlier version of this check, which did not test
whether the cut was in the LP, reported 121 and 258 violations; they came
from cuts that SCIP's cut selection never applied (Section 6).

## 5. Single-cut bound of SCIP's actual sets

*Definitions.* For an attempt with corner `(s̄, P, w)` (rays of fixed
columns and equality rows dropped, since their `λ_j` is 0 on the LP;
rates floored at `10^-9 max w`, as in the sfree note):

- `z_C = min_j w_j t_j` over SCIP's own steps `t_j` when the cut was
  generated (745 MINLPLib records and all generator records but 2), else
  over the steps of the validated "fixed" model (failed attempts, rays with
  monoidal coefficients; 322 MINLPLib records). This is the single-cut
  bound of SCIP's *set*. For rays with monoidal coefficients the actual cut
  can do better, but it is then valid only because of integrality; this
  concerns 12 ratio records.
- `z_K` = corner bound, by `code/zk_fast.py` in the reduced space of
  `rank Q + [b ∉ range Q]` coordinates: exact (up to floating point) for
  `ρ = n_+ + 1 ≤ 2` (Theorem 4 of the sfree note); for `ρ = 3`, the
  minimum of the two-ray value and a generic 3-ray KKT enumeration; for
  `ρ ≥ 4`, the smaller of the two-ray value and Gurobi's incumbent, with
  Gurobi's best bound as a solver-reported lower estimate
  (`code/gurobi_zk.py`, 120 s per record; 232 records, 175 reported
  optimal, 47 time limits, 10 reported infeasible). These statuses and
  bounds are numerical solver reports, not certificates.
- Classes: *degenerate* if the face of zero-rate rays meets `S` (then
  `z_K = z_C = 0` for every S-free set and the ratio is undefined; for
  `ρ ≥ 3` only faces reached with at most two rays are detected);
  *all rates zero*; otherwise the ratio `z_C/z_K` is reported. These
  classes use the reduced-space numerical test. Four records lose tiny
  full-space drift under that reduction (Section 5.2), so their class
  does not establish non-degeneracy in exact arithmetic on the dumped data.

*Validation of `z_K`.* `code/test_zk_fast.py 0 900` (Section 7.1); Gurobi
on 40 random records with exact or 3-ray `z_K` (38 reported optimal: largest
relative difference `3.6·10^-3`, median `10^-9`; 2 reported infeasible by
Gurobi, a numerical artifact since our point is verified feasible) and on 20
records with ratio below 0.1 (16 reported optimal, 4 time limits). Among
the 16 optimal reports, the median relative difference is
`6.8·10^-10`, but the largest is `8.9·10^-5`: Gurobi reports a lower value
for `pooling_digabel18` k=351, a `kkt3` record. Three time-limited
incumbents (`blend029` k=22 and `pooling_sppa0tp` k=1143 and k=1640)
agree with the stream's values within `10^-7` relative;
`blend029` k=15 has no incumbent.
Finally, 189 MINLPLib
records whose violated side has `n_+ = 0`, where `cl(R^k \ S)` is convex
and therefore `z_C = z_K` must hold: all 189 give ratio 1 to within `10^-6`.

**Claim 5.1 (numerical evidence; floating-point computations with the
validated codes and solver-reported values, subject to the caveats below).**
Distribution of `z_C/z_K` for SCIP's actual sets
(`code/summarize.py`, log `logs/summary.log`). Quartiles; fractions
below 0.9 and 0.5; fraction equal to 1 (`≥ 1 − 10^-6`). No ratio exceeds
`1 + 10^-6`.

| Corners | n | mean | q25 | median | q75 | `< 0.9` | `< 0.5` | `= 1` |
|---|---|---|---|---|---|---|---|---|
| mc11, all attempts | 898 | 0.849 | 0.769 | 0.976 | 0.999 | 35.4% | 11.0% | 1.2% |
| mc11, instance-weighted (47) | 898 | 0.912 | 0.927 | 0.994 | 1.000 | 23.0% | 5.0% | 1.0% |
| mc12, all attempts | 2469 | 0.897 | 0.905 | 0.992 | 1.000 | 24.5% | 6.8% | 2.3% |
| mc12, instance-weighted (73) | 2469 | 0.920 | 0.940 | 0.996 | 1.000 | 19.5% | 4.2% | 3.2% |
| mc11, first LP, most violated product | 47 | 0.929 | 0.866 | 0.974 | 0.998 | 13/47 | 1/47 | 0 |
| mc12, first LP, most violated product | 73 | 0.924 | 0.917 | 0.978 | 0.998 | 15/73 | 3/73 | 1/73 |
| MINLPLib, sampled corners classified non-degenerate | 1067 | 0.648 | 0.190 | 0.923 | 1.000 | 48.3% | 34.8% | 29.3% |
| MINLPLib, instance-weighted (26) | 1067 | 0.586 | 0.036 | 0.818 | 1.000 | 54.4% | 42.6% | 18.4% |
| MINLPLib, generated cuts only | 755 | 0.649 | 0.181 | 0.956 | 1.000 | 47.3% | 35.5% | 29.4% |
| MINLPLib, failed attempts (model `z_C`) | 312 | 0.645 | 0.253 | 0.890 | 1.000 | 50.6% | 33.0% | 29.2% |

For 46 MINLPLib ratio records the table uses a solver-reported bracket
for `z_K`. The corresponding ratio upper estimates are all below 0.1
(maximum `0.09847245955656159`). For 10 more, Gurobi reported
infeasibility and supplied no positive lower estimate of `z_K`; the
reported ratio uses the stream's two-ray value. Conditional on the
solver-reported brackets being valid, those 46 records are all below 0.5
and 0.9. The other 10 use upper bounds on `z_K`, so their ratios can
only move up: uncertainty in them can only lower the fractions below
0.5 and 0.9, by at most `10/1067 ≈ 0.94` percentage points. Under the
same condition, moving the 46 ratios to their upper estimates changes
the per-corner mean by `0.000580` and leaves
the quartiles unchanged. These are sensitivity calculations, not
certified bounds on the true distribution.

The reviewer observed inconsistent Gurobi optimality reports on badly
scaled full-space models. For `waterund25` k=410, Gurobi reported
objective = bound = `0.1635207364437` with a cost cap of `2·z_K`, and
`0.2398457846693` with a cap of `4·z_K`. Both exceed the stream's
single-ray value `0.15618498137992684`. Exact rational arithmetic on the
dumped quadratic and ray brackets that ray's boundary cost near
`0.15618498137992642` and verifies a feasible point at cost
`0.1561849815361114`. This confirms a feasible upper bound near
`0.156185`, not global optimality of the full corner. The reviewer also
found inconsistent reports on `waterund32` k=1250 and `blend480` k=365;
independent, numerically checked support-2 points reproduce the stream's
lower values there. These examples rule out treating solver statuses as
certificates. Exact lower and upper certificates exist for the ten
generator corrections in Section 7.1; the other `z_K` values here are
floating-point results. Evidence: `reviews/r1-logs/gurobi_fullspace_summary.log`,
`gurobi_relaxed.log`, `pairs_upper.log`, and
`logs/check_revision_r1.log` (the exact single-ray check repeated here).

### 5.1 Generator

- *Comparison with the sfree note.* On the earlier note's own corners
  (HiGHS basis at the LP vertex, most violated product), SCIP's set is
  below `0.9 z_K` in 27 of 120 corners and below `0.5 z_K` in 3 (Section
  7.1, after the `z_K` correction; the note said 26 and 3). On SCIP's own
  first-LP corners for the same products (`code/compare_first_lp.py`, logs
  `compare_first_lp_1{1,2}.log`) the counts are 28 and 4. In all 120
  instances SCIP's first LP has the same point on `(x_i, x_j, w_e)` as
  HiGHS (difference `≤ 10^-7`), and the ratio agrees to `10^-6` in 113;
  the other 7 differ because SCIP's LP has a different basis at the same
  vertex (and contains SCIP's own initial estimators), so the cone differs.
- *Over all attempts* the ratio is lower: below 0.5 in 11.0% (mc11) and
  6.8% (mc12) of attempts against 2–4% at the first LP; most attempts come
  from later root rounds.
  In the attempts with ratio below 0.5 the ray that determines `z_C` has a
  small positive rate (`≤ 10^-3 max w`) in 58 of 99 (mc11) and 120 of 167
  (mc12) cases (`code/low_ratio_mechanism.py`, log
  `low_ratio_mechanism_generator.log`): SCIP's set leaves such a cheap ray
  early, while the optimal set would exit it late or not at all; this is
  the mechanism of the sfree note's Proposition 6.
- No generator corner is degenerate (no zero rates), and the few attempts
  in the tree (26 and 28) have higher ratios (means 0.946 and 0.990).

### 5.2 MINLPLib

- *Most corners are degenerate.* Of the 4,578 analysed MINLPLib attempts,
  3,347 (73.1%) have a zero-cost face that meets `S`, so `z_K = 0` and no
  single intersection cut, from any S-free set, can raise the bound of the
  corner relaxation, although the cut does cut off the LP point. Another
  164 (3.6%) have all rates zero. Only 1,067 (23.3%), from 26 of the 48
  instances, have `0 < z_K`; in the other 22 instances every analysed
  corner is degenerate or has zero rates under the numerical class test.
  In all 115 degenerate corners with `ρ ≤ 2` in the reviewer's sample,
  one zero-rate ray alone reaches `S`; the median share of zero-rate rays
  is 60% (56 witnesses are columns outside the constraint, 33 are
  constraint-variable columns and 26 are row slacks). This points to
  heavy dual degeneracy of the LPs, consistent with the sibling
  [`scip-set-selection` note, Section 8.1](../scip-set-selection/note.md#81-scips-root-corners-are-mostly-dual-degenerate).
  The calculation was repeated in `code/check_revision_r1.py`, with
  `logs/check_revision_r1.log`. (The first sample alone, 50 per
  instance, gives 74% degenerate and 7% zero-rate corners.)
- *Where the bound is defined, SCIP's set is often far from it.* The
  distribution is bimodal: 29% of the corners have ratio 1, a third have
  ratio below 0.5, and the instance-weighted median is 0.82. Instances
  differ strongly: ratio 1 on all 170 analysed corners of `elec25` (Case 2
  with `n_+ = 0`, where the complement of `S` is convex) and on the
  circle-packing corners; median 0.97–1.00 on `crudeoil_li03`, `ex3_1_2`,
  `ex7_3_3`, `nvs14`, `pooling_adhya1tp`, `sssd22-08persp`; median below
  0.05 on `blend029`, `genpooling_meyer04`, `pooling_digabel18`,
  `pooling_sppa0tp`, `tln12`, `waterund32`, `waterund36`.
- *Mechanism of the low ratios* (`code/low_ratio_mechanism.py 0.5`, log
  `logs/low_ratio_mechanism_after_r1.log`). The revised script uses
  `summarize.ratio_of`, so it covers the same 371 records below 0.5 as the
  table. The old 359-record selection omitted 14 `nvs23` records with
  infinite two-ray values and included two others (k=25 and k=31), because
  it ignored Gurobi's incumbents. Of the 371 records, 187 (50.4%) have the
  `z_C`-determining ray at zero rate under the floor convention; in 183
  (49.3% of 371) the full-space one-ray check finds no intersection with
  `S`. SCIP's set exits these rays at a finite step, giving a negligible
  bound with floored rates and zero gain with exactly zero rates.
  Another 99 have a rate below `10^-3 max w` on that ray; 85 have neither.

  The four apparent class contradictions are `waterund32` k=651, 715,
  1138 and 1292. Their determining rays have raw rate 0. A full-space
  boundary check accepts the one-ray candidates; adding that check alone
  does not resolve the contradiction. Exact rational restriction of the
  dumped quadratic gives `A = 0` and negative linear drift between
  `−2.5792121992851563·10^-14` and `−7.737636597855469·10^-15`, so each ray
  reaches `S` in that exact dumped-data model, at a step between
  approximately `2.10·10^18` and `6.85·10^18`. The spectral
  reduction loses this drift and reports no intersection. In each record
  the ray moves `t_x612` down from its upper bound 1425. Its bilinear
  partner (`t_x245`, `t_x261` or `t_x252`) has a dumped LP value of about
  `10^-14`; the bilinear coefficient is 1, so the negative drift equals
  minus that partner value, without cancellation. Rounding of about
  `u·10^3 ≈ 10^-13` in the spectral coordinate `Vrᵀ s̄` exceeds the drift.
  The drift is present in the dumped LP values; whether those values
  reflect nonzero values in the true LP corner remains undetermined.
  This explains their class in the table. Thus only 183 of the 187 support the
  no-intersection mechanism. The four remain in the numerical table;
  they do not establish `z_K > 0` for the full-space corner with exactly
  zero rates. Their enormous one-ray costs with floored rates do not
  improve the reported `z_K` values.

  With the floored rates, Theorem 1 of the sfree note
  guarantees S-free sets whose bound approaches `z_K`; with exactly zero
  rates the supremum can fall short (its Proposition 2), so how much an
  optimal set gains here is not settled by this measurement.
- *Failed attempts.* The model's single-cut bound on the attempts that
  SCIP aborted has a similar distribution to that of the generated cuts
  (last two rows of the table): the aborts do not select particularly good
  or bad corners.

**Answer to the stream's question.** The sfree note's model of "SCIP's
set" matches SCIP 10.0.3 (Claim 4.1). SCIP's actual single cuts leave a
median of 1–3% of the corner bound on the generator and, on the
quarter of MINLPLib corners where the corner bound is positive, a median
of 8% (per corner) or 18% (instance-weighted), with a third of these
corners below half of `z_K`. On three quarters of the MINLPLib corners the
question is void because `z_K = 0`.

## 6. How often generation fails or cuts are rejected

All attempts, from the complete dumps (`code/index_dumps.py` via
`code/run_index.sh`, then `code/outcomes.py`, log `logs/outcomes.log`;
**computed exactly** from the dumps; the counter lines of every run agree
with the record counts).

| | mc11 | mc12 | MINLPLib (48 instances) |
|---|---|---|---|
| enforcement calls | 3,307 | 6,943 | 13,828,959 |
| skipped: per-expression cut limit | 2,167 | 3,938 | 13,749,250 |
| skipped: violation < `minviolation` | 215 | 530 | 2,362 |
| skipped: LP not optimal/basic | 27 | 6 | 433 |
| attempts (reach `generateIntercut`) | 898 | 2,469 | 76,914 |
| abort: zero basis status | 0 | 0 | 9,784 (12.7%) |
| abort: dynamism test | 0 | 2 | 38,105 (49.5%) |
| abort: `φ(0) ≥ 0` | 0 | 0 | 0 |
| abort: minimal representation | 0 | 0 | 3 |
| generated | 898 | 2,467 | 29,022 (37.7%) |
| rejected by clean-up | 0 | 0 | 1,265 |
| rejected by range/efficacy test | 1 | 4 | 2,889 |
| added to the separation storage | 897 | 2,463 | 24,868 (32.3%) |
| attempts at depth > 0 | 26 | 28 | 17,346 |

- *The dynamism test is the main failure.* It removes half of all MINLPLib
  attempts (more than half of the attempts in 17 of the 48 instances; by
  case: 46% of Case-1, 55% of Case-2, 89% of Case-3 and 57% of Case-4
  attempts). By definition, every abort has
  `min_{≠0}/max |A,B,C| ≤ 10^-15` on a checked piece. The 1,799 / 1,974
  split (91.1%) identifies failures on the first piece (Cases 1–3 or 4a);
  the remaining 175 fail on 4b. It provides no evidence about rounding.
  Recomputing the coefficients' ratios from the raw sampled dumps gives:

  | Failing piece | n | 10th percentile | median | 90th percentile | `< 10^-25` |
  |---|---|---|---|---|---|
  | Cases 1–3 / 4a | 1799 | `2.98645758·10^-34` | `4.61594214·10^-18` | `4.55819518·10^-16` | 493/1799 (27.4%) |
  | 4b | 175 | `1.08080140·10^-20` | `4.32021883·10^-17` | `7.96814357·10^-16` | 4/175 (2.3%) |

  The dumps identify the immediate mechanism for most first-piece
  aborts: only `A` lies below `10^-15 max |A,B,C|`. This occurs in
  1,270/1,799 sampled aborts (70.6%) and 28,071/34,834 first-piece aborts
  in all dumps (80.6%). In Cases 1–3,
  `A = Σ_{θ_i < 0} |θ_i|(v_iᵀr)^2`; Case 4a also adds
  `w(r)^2/(4√(1+κ²))`. These are sums of nonnegative terms. An independent
  evaluation on the dumped inputs finds that in 1,209 of the 1,270
  sampled tiny-`A` cases, `A` exceeds `64u` times the absolute evaluation
  of its formula (`u = 2^-53`); it is not consistent with a rounded zero
  under that diagnostic. The small value usually reflects a short ray
  component in the negative eigenspace (and small `w(r)` in Case 4a)
  relative to the LP-point terms in `B,C`.

  The dynamism test is not invariant under ray scaling. For `α > 0`,
  replacing `r` by `αr` maps `(A,B,C)` to `(α²A,αB,C)`. The step becomes
  `t/α`; dividing the resulting cut coefficient by `α` recovers `1/t`,
  so the cut is unchanged in exact arithmetic. In SCIP 10.0.3,
  `createAndStoreSparseRays` and `insertRayEntries` store signed tableau
  entries without normalising the rays; they drop entries at
  `SCIPisZero` (`|·| ≤ 10^-9`). A TODO at `nlhdlr_quadratic.c:819`
  suggests scaling the entries and converting the cut coefficient back.
  `computeRestrictionToRay` (lines 1622–1624 and 1700–1702) has the
  scaling above, while `areCoefsNumericsGood` (lines 2076–2092) compares
  the unscaled coefficient ratio. An analytic optimisation over `α`
  shows that rescaling would make the first-piece test pass for
  1,728/1,799 sampled aborts (96.1%) and 31,926/34,834 in all dumps
  (91.7%); the median best `min/max` ratio is about 0.5. These figures
  concern the first piece on the failing ray, not successful generation
  of the whole cut: 4b and other rays or checks could still fail.
  The median largest quadratic-variable ray entry is `1.9·10^-5` in
  the sample and `10^-6` in all first-piece aborts. Whether the short
  components are themselves LP noise, and whether computing these cuts
  after rescaling would be safe, remain open. Script:
  [`code/check_revision_r2.py`](code/check_revision_r2.py); log:
  [`logs/check_revision_r2.log`](logs/check_revision_r2.log).

  An adapted version of the reviewer's diagnostic uses SCIP's dumped
  eigenvectors and the failing ray. It tests whether all negative-eigenspace
  dot products and, in Case 4, the whole `w(ray)` are within
  `10^-12` of the sum of absolute evaluation terms. In the reviewer's
  saved sample, 36 of 138 first-piece aborts (26.1%) have `A,B` consistent
  with zero at that tolerance; 102 have a component above it, with median
  coefficient ratio `7.59782506·10^-18`. Twelve 4b aborts are excluded
  from this diagnostic. This is a heuristic consistency test, not an exact
  zero test, and that sample is not a representative estimate of all
  aborts. It does not support rounding noise as the cause of most aborts
  and does not test the safety of cuts computed after ray rescaling.
  Script: [`code/dynamism_after_r1.py`](code/dynamism_after_r1.py), adapting
  `reviews/r1-code/dyn_noise.py`; log:
  [`logs/dynamism_after_r1.log`](logs/dynamism_after_r1.log). Had SCIP
  generated these cuts, their single-cut bounds (computed with the
  validated model) would be distributed similarly to those of the
  generated cuts (Section 5, last two rows of the table).
- *Zero basis status* aborts are concentrated in `space25a` (8,638) and
  `lukvle10` (1,146): free nonbasic variables.
- *The per-expression limit* (Section 1.1) rejects 99.4% of all MINLPLib
  enforcement calls. In the tree it allows at most two cuts per
  expression within a solve run between restarts, and none for expressions
  that already have two cuts from that run's root. Two of the 64 runs
  restarted: `ex1264` and `squfl010-040persp`.
- *Most checkable added cuts are never observed in the LP.* `SCIPaddRow` only stores the cut;
  SCIP's cut selection decides what enters the LP. Using the `lpcuts`
  field (this expression's intersection cuts in the LP at its next
  attempt at the same node), `code/lp_entry.py` (log `logs/lp_entry.log`)
  finds the cut in a later LP for 296 of 767 checkable added cuts on mc11
  (38.6%), 595 of 2,155 on mc12 (27.6%) and 3,152 of 21,886 on MINLPLib
  (14.4%). The rest were never seen in the LP (a cut that entered and left
  between two attempts would be counted as "never seen", so these are
  lower bounds); 130, 308 and 2,982 added cuts had no later attempt of
  their expression at the same node and cannot be checked.

## 7. Corrections to the sfree note

### 7.1 Ten stored corner bounds in Section 9.2 were wrong (`core.two_ray`)

**Claim 7.1 (computed exactly).** In the sfree note's Section 9.2 runs,
the stored corner bound `z_K` is wrong for 3 of the 47 corners of
`exp_mccormick_11_final.json` (trials 3, 110, 122) and for 7 of the 73
corners of `exp_mccormick_12_big_final.json` (trials 14, 28, 71, 115, 140,
142, 174). All 10 stored values are below an exactly certified lower bound
on the true `z_K`.

*Certificate* (`code/certify_two_ray.py`, logs `certify_two_ray_1{1,2}.log`).
Each corner is regenerated exactly as `exp_mccormick.py` does it (the
regenerated `core.corner_bound` value equals the stored value in all 120
corners). Its floating-point data `(s̄, P, w)` are converted exactly to
rationals. Upper bound: a rational point `λ ≥ 0` with
`q(s̄ + Pλ) ≤ 0` (checked exactly) and `w^T λ = z_up`. Lower bound
`z_low = 0.999 · z_up`: for every single ray and every pair of rays, `q > 0`
on the triangle `{μ ≥ 0, w_J^T μ ≤ z_low}` (vertices, edges and the
interior stationary point checked exactly). For bilinear `q`, `ρ = 2`, so
by Theorem 4 and Lemma 3 of the sfree note some minimizer uses at most two
rays, hence `z_K ≥ z_low`.

| seed | trial | stored `z_K` | certified `z_low` | `z_up` | `z_C/z_K` of SCIP's set (corrected) |
|---|---|---|---|---|---|
| 11 | 3 | 8.1e-9 | 0.04880 | 0.04885 | 0.967 |
| 11 | 110 | 0.1035 | 0.13367 | 0.13380 | 0.776 |
| 11 | 122 | 0.0156 | 0.03294 | 0.03297 | 0.998 |
| 12 | 14 | 0.0625 | 0.19874 | 0.19894 | 0.989 |
| 12 | 28 | 0.125 | 0.13711 | 0.13725 | 0.990 |
| 12 | 71 | 0.0313 | 0.04923 | 0.04928 | 1.000 |
| 12 | 115 | 0.0039 | 0.02768 | 0.02771 | 0.917 |
| 12 | 140 | 0.0039 | 0.04075 | 0.04080 | 0.993 |
| 12 | 142 | 0.125 | 0.19662 | 0.19682 | 0.944 |
| 12 | 174 | 0.0078 | 0.07195 | 0.07202 | 1.000 |

*Cause.* `core.two_ray` parametrizes a pair of rays by
`ν(θ) = (θ/w_i, (1 − θ)/w_j)` and takes the larger root
`u_+ = −2a/(bb + √D)` of `g_0 u^2 + bb u + a = 0`. When the two scaled rays
are antiparallel (`P ν(θ*) = 0` for some `θ*`), `a(θ*)` and `bb(θ*)` are
both rounding noise and the formula returns an arbitrary `u_+`. In all 10
corners the pair that `core.corner_bound` picks has cosine `−1.000` between
its rays, and the returned "minimizer" has `q = 0.33`–`0.67 > 0` exactly,
i.e. it is infeasible. Antiparallel projected rays are common in these LP
corners (38 of 47 and 66 of 73 corners have at least one pair); the error
shows only when the noise wins. The golden-section safety net in `two_ray`
does not catch it, because the spurious value sits at an isolated `θ`.
The stream's own `zk_fast.zK_upto2` had the same flaw in its first version
and a second instance of it (two rays that are both null directions of `q`,
found on an `sssd22-08persp` corner, where it produced `z_C/z_K > 1`). The final version accepts a
candidate only if `q`, recomputed from scratch at the candidate point, is
about 0 (`_on_boundary`). The test `code/test_zk_fast.py 0 900` refereed
with a brute-force `θ` grid: 868 of 873 finite cases agree with
`core.corner_bound` to `4·10^-10`; in the other 5, `zk_fast` agrees with
the brute force (relative `1.6·10^-9`) and `core.corner_bound` is too
small; in 8 cases `core.corner_bound` returns a huge finite value
(`3·10^12`–`2·10^18`) where the brute force finds no intersection (or
`1.3·10^13`).

*Effect on the sfree note's Section 9.2* (`code/recheck_note_affected.py`,
logs `recheck_note_affected_1{1,2}.log`; only the 10 corners change). The
stored increments of all three rules were capped at the wrong `z_K`:

| Quantity (n = 47 / n = 73) | stored | corrected |
|---|---|---|
| corner increment, SCIP's set, mean (median) | 0.700 (0.839) / 0.591 (0.634) | 0.724 (0.864) / 0.616 (0.647) |
| corner increment, best orbit set = corner bound | 0.755 (1.000) / 0.648 (0.795) | 0.783 (1.000) / 0.675 (0.800) |
| LP re-solve, SCIP's set | 0.895 (0.957) / 0.870 (0.934) | unchanged |
| LP re-solve, best orbit set | 0.929 (1.000) / 0.907 (0.999) | 0.931 (1.000) / 0.910 (1.000) |
| LP re-solve, corner-optimal cut | 0.755 (1.000) / 0.648 (0.795) | 0.783 (1.000) / 0.675 (0.800) |
| SCIP's set below 0.9 `z_K` / below 0.5 `z_K` | 26 / 3 of 120 | 27 / 3 of 120 |

The statement "the best orbit set attained `z_K` in all 120 LP corners"
survives: with the corrected `z_K` as bisection scale the worst orbit ratio
is 0.99997.

*Effect on Section 9.3* (`code/exp_loop_fixedzk.py`, which runs the
unchanged `exp_loop.py` with `core.corner_bound` replaced by `zk_fast`; the
orbit rule uses `z_K` as its bisection cap and the corner-optimal cut uses
it directly; SCIP's rule does not use `z_K`; logs `exp_loop_{small,big}_fixedzk.{json,log}`;
fraction of the root gap closed, mean over instances):

| Rule | 4×4, n = 12, rounds 1 / 2 / 3 / 8, stored → corrected | 6×8, n = 10, rounds 1 / 2 / 3 / 10, stored → corrected |
|---|---|---|
| SCIP's set | 0.828 / 0.940 / 0.963 / 1.000 (unchanged) | 0.686 / 0.820 / 0.861 / 0.931 (unchanged) |
| best orbit set | 0.863 / 0.967 / 0.998 / 1.000 → 0.891 / 0.967 / 0.998 / 1.000 | 0.701 / 0.796 / 0.832 / 0.887 → 0.701 / 0.799 / 0.828 / 0.901 |
| its completion (B) | 0.863 / … / 1.000 → 0.891 / 0.967 / 0.998 / 1.000 | 0.701 / 0.796 / 0.832 / 0.881 → 0.701 / 0.799 / 0.828 / 0.904 |
| corner-optimal cut | 0.722 / 0.796 / 0.796 / 0.796 → 0.781 / 0.854 / 0.854 / 0.854 | 0.584 (all rounds) → 0.613 (all rounds) |

The conclusions of Section 9.3 stand: the orbit rule is ahead after round 1
on the small instances (now 9 of 12 better by more than 0.01, none worse)
and behind SCIP's rule after 10 rounds on the 6×8 instances (better in 1,
worse in 4 of 10); the corner-optimal cut stalls. The rerun agrees exactly
with the first author agent's rerun made before the second `zk_fast` fix.

Section 9.1's validation against SCIP global solves (77 random instances)
is probably not affected, since random rays are almost surely not
antiparallel; I did not recheck it.

### 7.2 Case 4 of the earlier model (`scout_sfree.ms_set`) is wrong for κ ≠ 0

**Claim 7.2 (proved; numerical confirmation).** For Case 4 with `κ ≠ 0`,
`ms_set` builds `x̂ = (x/r^{1/2}, (w + κ + r)/(2 r^{1/2}))`,
`ŷ = (y/r^{1/2}, (w + κ − r)/(2 r^{1/2}))`, `r = √(1 + κ^2)`. Then
`‖x̂‖^2 − ‖ŷ‖^2 = (‖x‖^2 − ‖y‖^2)/r + w + κ`, which is not a positive multiple
of `q = ‖x‖^2 − ‖y‖^2 + w + κ` unless `r = 1`, i.e. `κ = 0`. So the modelled
set is in general not S-free, and the LP point need not lie in its interior.
The ZIB report's formula (an overall factor `r^{-1/2}` on both blocks, with
the extra coordinate divided by `2 r^{1/2}` inside) and SCIP's code (no
factor) both give `‖x̂‖^2 − ‖ŷ‖^2 ∝ q` and the same set; `ms_set` is a
transcription slip. *Proof:* the identity
`((A + r)^2 − (A − r)^2)/(4r) = A` with `A = w + κ`. *Numerically*
(`code/test_model_vec.py 0 200`, log `test_model_vec.log`; the first author
agent's run, repeated in this continuation with identical output): on 50
random Case-4 corners, 8 had `s̄` outside the interior of the
`ms_set` set, and 956 of 96,508 sampled interior points of the `ms_set`
sets with `|κ| > 0.1` lie in `int S`; for SCIP's formula, 0 of 113,049. On
SCIP's own MINLPLib cuts (Section 4) `ms_set` disagrees with SCIP on
17,584 of 19,376 compared Case-4 rays with `κ ≠ 0`; elsewhere it uses the
same formulas as the "fixed" model and differs only through its smaller
cutoff (`10^7` instead of `10^12`).

*Effect on the sfree note:* none found. Its bilinear constraints have
`κ = 0`; Proposition 6 and Section 6.1 use Case 2. The first author agent's
docstrings in `code/scip_rule.py` and `code/model_vec.py` attributed the
slip to the ZIB report; they were corrected in this continuation.

## 8. Comparison with the earlier notes and prior work

- *sfree note.* Its "SCIP's set" (Sections 5, 6.1, 8, 9) is the set SCIP
  10.0.3 builds, case by case and with the same point rule; the only
  modelling error (Case 4 with `κ ≠ 0`, Section 7.2) never entered its
  results. Its Section 9.2 statistic "SCIP's set below 0.9 `z_K` in 26 of
  120 corners, below 0.5 in 3" becomes 27 and 3 after the `z_K` correction
  (Section 7.1), and 28 and 4 on SCIP's own first-LP corners (Section 5.1).
  It said that SCIP's own cuts were never extracted; this stream extracted
  them, and they behave as modelled. Its remark that a solver-level benefit
  would need experiments inside SCIP is reinforced: on MINLPLib the
  single-cut bound is often irrelevant because the corner is degenerate,
  half of the attempts abort, and most checkable added cuts are never
  observed in the LP.
- *Chmiela–Muñoz–Serrano* (ZIB report 20-29; Math. Program. 197, 2023)
  describe the construction implemented in `nlhdlr_quadratic.c` and report
  root-node gap closed on 587 MINLPLib instances (about 8% more gap closed
  on average with their cuts). They do not compare single cuts with the
  corner bound, and they report no statistics on aborted attempts, the
  dynamism test or cut selection. Their printed Case-4 formula is correct
  (Section 1.3).
- *Muñoz–Serrano* (Math. Program. 192, 2022) and Muñoz–Paat–Serrano give
  the maximal quadratic-free sets; the point rule `λ = x̂(s̄)/‖x̂(s̄)‖` is
  theirs. The sfree note showed that this rule can miss `z_K` (Section 6.1
  there); Section 5 here measures by how much in SCIP's corners.
- *SCIP documentation and release reports* (SCIP 8.0 and 9.0 reports,
  found by a web search on 2026-10-02) mention the parameter, that it is off
  by default, monoidal strengthening (SCIP 9.0) and in source comments the
  numerical risks of the root computation. I found no measurement of the
  single-cut bound of SCIP's cuts against the corner bound, nor of the
  abort rates. The search was short (one web query plus the sources already
  collected by the scout), so this does not establish novelty; the
  measurements are routine once the instrumentation exists.

## Revision after review round 1

Revised 2026-10-03 in response to
[`reviews/review-r1.md`](reviews/review-r1.md). Round 2 independently
confirmed these fixes. Only this stream's note, analysis code and logs
were edited; review artifacts were preserved. No SCIP rebuild, benchmark
rerun, solver rerun, commit or change to the git index, branch or HEAD was made.

| Issue | Change and evidence |
|---|---|
| M1 | Removed "probably rounding noise" as the explanation for most aborts. The 91.1% figure is now only the split between checked pieces. Recomputed both ratio distributions from 1,974 sampled abort records in raw dumps and repeated the heuristic diagnostic: 36/138 consistent with zero, 102 above tolerance. Summary, Section 6, Solver relevance and Open question 1 now state what remains undetermined. `logs/dynamism_after_r1.log`. |
| m1 | Replaced Gurobi certification and "175 closed" with solver-reported statuses. Made bracket and sensitivity claims conditional; corrected the largest ratio upper estimate from "below 0.03" to `0.09847245955656159` (below 0.1). Repeated the exact rational feasible-point check for `waterund25` k=410 and separated it from a global optimum certificate. Exact two-sided certificates apply to the ten Section 7.1 generator corrections. `logs/check_revision_r1.log` and the review's Gurobi logs. |
| m2 | Corrected 18 optimal / 2 time limits to 16 / 4; replaced `~10^-6` agreement with median `6.8·10^-10`, maximum `8.9·10^-5` relative, lower on `pooling_digabel18` k=351. Three time-limited incumbents agree within `10^-7`; one has none. `logs/check_revision_r1.log`. |
| m3 | Defined `|Δκ|/max(1,|κ|) = 2.8·10^-14` as absolute for `|κ| ≤ 1`; true relative maximum is `1.4·10^-13`. `logs/check_revision_r1.log`. |
| m4 | Replaced 59 no-ray records with 207 of 4,785 (59 first sample, 148 second sample). `logs/check_revision_r1.log`. |
| m5 | Mechanism script now selects the table's 371 records, instead of 359: 187 zero-rate, 99 small-rate, 85 other. It adds boundary and exact restriction checks. The four `waterund32` contradictions have tiny drift present in the dumped LP values, lost under spectral reduction; a boundary check alone does not remove them. Qualified the numerical classes and the mechanism: 183/371 show no one-ray intersection, while 187/371 have a zero-rate determining ray. `logs/low_ratio_mechanism_after_r1.log`. |
| m6 | Replaced "cut selection drops the rest" with lower bounds on LP entry among checkable cuts; acknowledged cuts that enter and leave between observations and 2,982 uncheckable MINLPLib cuts. `logs/lp_entry_after_r1.log`. |
| m7 | Qualified both bisection-loss maxima as sample-specific and cited the sibling note's Section 4.3, where SCIP halves a step. Removed "slightly" from the general statement. Saved `logs/explain_mismatch.log` and the matching reviewer log support the sample figures; this revision's full replay timed out at 120 s. |
| m8 | Added that dump-writing overhead changes which attempts occur in the 34 time-limited MINLPLib runs; counts describe the instrumented binary. `logs/check_revision_r1.log`. |
| m9 | Replaced "never reset" / "lifetime" throughout with limits between restarts. Checked new expression addresses and counter 0 at LP 113 of `ex1264`, after counters up to 18 at LPs 1–77. `logs/check_revision_r1.log`; source lifecycle read in `cons_nonlinear.c`. |
| o1 | Changed the generator gap description to "small in the median". The distribution table is unchanged. `logs/summary_after_r1.log`. |
| o2 | Added the explanation from the reviewer's sample: 115/115 degenerate corners have a single zero-rate ray reaching `S`, median zero-rate ray share 60%; cited sibling Section 8.1. Repeated the calculation in `logs/check_revision_r1.log`. |
| o3 | Added the full-space formulation as possible future work in Open question 6, subject to independent verification of solver reports. No new solve was run. |
| Header | Replaced "Nothing here has been committed" with the repository's outside-program commit history and the current revision status: revised after r1, not re-reviewed. |

## Revision after review round 2

Revised 2026-10-03 in response to
[`reviews/review-r2.md`](reviews/review-r2.md), which confirmed all round-1
fixes. This round-2 revision has not been independently re-reviewed.
Only this stream's note, new checking script and logs were edited;
review files were preserved. No SCIP rebuild, benchmark run, solver run,
commit or change to the git index, branch or HEAD was made.

| Issue | Change and evidence |
|---|---|
| N1 | Replaced "causes of most aborts remain undetermined" with the observed mechanism and the questions that remain open. Independent raw-dump counts give tiny `A` alone in 1,270/1,799 sampled first-piece aborts (70.6%) and 28,071/34,834 in all dumps (80.6%); 1,209/1,270 sampled tiny-`A` values exceed the `64u` rounded-zero diagnostic threshold. An analytic rescaling calculation gives 1,728/1,799 (96.1%) and 31,926/34,834 (91.7%) first-piece passes. Source inspection confirms that rays are not normalised and that the test depends on their length. Summary and Section 6 state the mechanism; Open question 1 includes ray scaling as a candidate change requiring safety checks. Whether short ray components are LP noise and whether those cuts are safe remain open. `code/check_revision_r2.py`, `logs/check_revision_r2.log`. |
| N2 | Replaced "real tiny drift" with drift "present in the dumped LP values". Summary and Section 5.2 now say the four rays reach `S` in the dumped data. Exact rational restrictions independently confirm that each drift is minus the approximately `10^-14` LP value of the bilinear partner of `t_x612`, below approximately `10^-13` rounding in the spectral reduction. The true LP-corner values remain undetermined. `logs/check_revision_r2.log`. |
| N3 | Replaced "the ray's linear component" with "the whole `w(ray)`" in the Section 6 diagnostic description. The diagnostic includes zero-eigenvalue, linear-variable and auxiliary-variable terms. |
| N4 | Replaced Summary item 3's "exact certificates" with "exact checks". Section 5 now says the 10 uncertain ratios can only move up, so their uncertainty can only lower the fractions below 0.5 and 0.9 by at most `10/1067 ≈ 0.94` percentage points. The exact feasible-point check in Section 5 remains distinct from the two-sided certificates in Section 7.1. `logs/check_revision_r2.log`. |
| Header | Updated status to "revised after review round 2; not re-reviewed" and linked the round-2 review. |

## Checks actually run

All targeted, local, in `code/` unless stated; no project-wide verification
and no CI. Outcomes are the actual results.

*Runs by the first author agent, re-checked and reused (not repeated):*
the patched build (`/workspace/local-home/build-scip/fidelity/build`; checked here:
binary built 2026-10-01 23:43 EDT, before all runs, links LAPACK 3.12.0,
patch file identical to the source diff); `run_scip.sh` on
`instances/mc11` (150), `instances/mc12` (200) and the 64 MINLPLib
instances (all exit code 0; every dump has the final `raywidth` field;
attempts in exactly the 47 + 73 instances of the sfree note's samples);
`recheck_note_affected.py 11 150 …` and `12 200 … 6 8 4` (its inputs, the
corrected `z_K` values, were re-derived here and are identical, so its
outputs are kept).

*Commands run in this continuation:*

| Command | Outcome |
|---|---|
| `./run_index.sh` (twice; the second after adding `lpcuts`) | 168 index files, 80,617 lines; every run's counter line agrees with its record count |
| `python3 outcomes.py` | `logs/outcomes.log`; per-expression limit check: 0 attempts at depth > 0 with 2 or more earlier cuts |
| `python3 certify_two_ray.py 11 150 <sfree>/logs/exp_mccormick_11_final.json`; `… 12 200 …12_big_final.json 6 8 4` | 3 + 7 wrong stored `z_K` certified (exact lower and upper bounds); `logs/certify_two_ray_1{1,2}.log` |
| `PYTHONPATH=<sfree>/code python3 test_zk_fast.py 0 900` | 868/873 agree with `core.corner_bound` (`4·10^-10`); 5 disagreements, `zk_fast` = brute force (`1.6·10^-9`); 8 infinite mismatches, brute force `∞` or `1.3·10^13`; `logs/test_zk_fast.log` |
| `python3 test_model_vec.py 0 200` | identical to the first author agent's log |
| `./run_all_analysis.sh` (8 processes, 3 h limit per job); mc12 chunks and `analyze.py --max-records 50 … bayes2_30` run by hand after a runner bug (Limits) | `logs/an_mc11.jsonl`, `an_mc12.jsonl`, `an_minlplib/` (48), `an_minlplib2/` (26); all jobs completed |
| `python3 explain_mismatch.py ../logs/an_mc11.jsonl ../logs/an_mc12.jsonl ../logs/an_minlplib/*.jsonl ../logs/an_minlplib2/*.jsonl` | 1,211 mismatching rays, all classified (Section 4) |
| `python3 check_rates.py mc11 …`, `mc12 …`, `minlplib …` | 296/296, 595/595, 314/316 (2 floor artifacts on degenerate corners) |
| `python3 lp_entry.py mc11 mc12 minlplib` | seen in LP: 38.6%, 27.6%, 14.4% of checkable added cuts |
| `python3 recheck_note_zK.py 11 150 …`; `… 12 200 … 6 8 4` | identical to the first author agent's output (same 10 corners) |
| `./run_loops.sh` (`exp_loop_fixedzk.py 21 30 8 …`, `22 30 10 … 6 8 4`) | identical to the first author agent's rerun; table in Section 7.1 |
| `python3 compare_first_lp.py 11 150 … mc11`; `… 12 200 … mc12 6 8 4` | same LP point in 120/120 instances, same ratio in 113/120 |
| `./run_gurobi.sh`, `./run_gurobi_tln.sh` (Gurobi 13.0.2, 1 thread, 120 s) | 232 records with `ρ ≥ 4`: 175 reported optimal, 47 time limits, 10 reported "infeasible" (numerical); solver reports, not certificates |
| `python3 gurobi_zk.py ../logs/gurobi_zk_validate.jsonl 60 validate:40 …`; `… gurobi_zk_lowratio.jsonl 60 lowratio:20 …` | 38/40 reported optimal, max relative difference `3.6·10^-3`; low-ratio check: 16 reported optimal, 4 time limits, max relative difference `8.9·10^-5`. Solver reports, not certificates |
| `python3 low_ratio_mechanism.py 0.5 ../logs/an_minlplib/*.jsonl ../logs/an_minlplib2/*.jsonl`; same with `../logs/an_mc11.jsonl`, `../logs/an_mc12.jsonl` | Section 5.2 / 5.1 |
| `python3 summarize.py` | `logs/summary.log` (all tables of Sections 4–5, including the `n_+ = 0` check: 189/189) |

*Commands run for the round-1 revision:* all from `code/`, prefixed with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`, with `python3 -B` to avoid
changing bytecode caches. At most four processes ran at once. No
project-wide checks or CI were run.

| Command | Outcome |
|---|---|
| `timeout 600s python3 -B dynamism_after_r1.py` | Exit 0; `logs/dynamism_after_r1.log`. Re-read failing coefficients from all 1,974 sampled raw dump records; ratio distribution and 36/138 rounding diagnostic reproduced. |
| `timeout 600s python3 -B low_ratio_mechanism.py 0.5 ../logs/an_minlplib/*.jsonl ../logs/an_minlplib2/*.jsonl` | Exit 0; `logs/low_ratio_mechanism_after_r1.log`. 371 records, 187/99/85 mechanism classes; exact restriction explains all four class contradictions. Rerun after adding diagnostics and formatting; no benchmarks rerun. |
| `timeout 120s python3 -B low_ratio_mechanism.py 0.5 ../logs/an_mc11.jsonl`; same with `../logs/an_mc12.jsonl` | Both exit 0; `logs/low_ratio_mechanism_mc{11,12}_after_r1.log`. Generator mechanism counts unchanged: 58/99 and 120/167 small-rate determining rays. |
| `timeout 120s python3 -B check_revision_r1.py` | Exit 0; `logs/check_revision_r1.log`. Status counts, relative differences, κ scale, sample counts, selection differences, bracket sensitivity, 34/30 run statuses, restart counters, degeneracy witnesses and exact rational feasible point checked. Review artifact hashes recorded. |
| `timeout 120s python3 -B summarize.py` | Exit 0; `logs/summary_after_r1.log`, byte-identical to `logs/summary.log`. |
| `timeout 120s python3 -B outcomes.py` | Exit 0; `logs/outcomes_after_r1.log`, byte-identical to `logs/outcomes.log`. |
| `timeout 120s python3 -B lp_entry.py mc11 mc12 minlplib` | Exit 0; `logs/lp_entry_after_r1.log`, byte-identical to `logs/lp_entry.log`. |
| `timeout 120s python3 -B explain_mismatch.py ../logs/an_mc11.jsonl ../logs/an_mc12.jsonl ../logs/an_minlplib/*.jsonl ../logs/an_minlplib2/*.jsonl` | Exit 124 (timeout), no completed output; `logs/explain_mismatch_after_r1.log`. The unchanged sample figures were checked against the saved author and reviewer logs, not claimed as a successful rerun. |
| `timeout 120s python3 -B -` (final artifact audit); `git diff --check -- research-20261001/scip-rule-fidelity/` | Exit 0; `logs/final_revision_r1.log`. Changed Python files parse, all review artifact hashes are unchanged, mechanism counts and four floored-cost comparisons agree, saved/rerun summaries match, and no analysis process is left. Diff whitespace check passed. |

*Commands run for the round-2 revision (from the repository root):*
All used `OMP_NUM_THREADS=1`; the numerical script used one process.

| Command | Outcome |
|---|---|
| `timeout 300s python3 -B research-20261001/scip-rule-fidelity/code/check_revision_r2.py` | Initial run exited 1 at the separate N4 table-selection assertion after reproducing all N1 and N2 numbers: the checking script omitted stored Gurobi incumbents when selecting records with infinite two-ray values. Corrected that selection and repeated the command; exit 0, all assertions passed. `logs/check_revision_r2_initial.log` preserves the initial outcome; `logs/check_revision_r2.log` contains the successful run. No solver was run. |
| `rg -n 'SCIP_VERSION_(MAJOR\|MINOR\|PATCH\|SUB)\|VERSION 10' <SCIP>/scip/CMakeLists.txt <SCIP>/scip/src/scip/scip.h <SCIP>/scip/src/scip/def.h`; targeted `sed` reads of `nlhdlr_quadratic.c` | Exit 0. Version 10.0.3; signed tableau entries without ray normalisation, scaling TODO at line 819, non-invariant `(A,B,C)` comparison and coefficient conversion confirmed. Source excerpts are in `logs/check_revision_r2.log` and `logs/final_revision_r2.log`; the former also records the source SHA-256. |
| `timeout 30s python3 -B -` (read review data) | Exit 0. Read all 38,105 records in `reviews/r2-logs/dyn_recompute.jsonl.gz` and all 371 records in `zero_rate_exact.jsonl`; review scripts and text logs were also read. |
| `timeout 30s python3 -B -` (final artifact audit) | Final run exited 0: script parses; analytic rescaling handles zero coefficients and changes of initial ray scale; status, body wording, artifact links and numerical log agree; source version and cited formulas checked; no revision-checking or aborted audit process remains. `logs/final_revision_r2.log`. An initial malformed shell invocation was stopped (exit 143; empty `logs/final_revision_r2_initial.log`); the next run exited 1 because its wording check also matched quoted old wording in the revision history (`logs/final_revision_r2_wording.log`). Scoped that check to the note's body and repeated it successfully. |
| `timeout 30s git diff --check -- research-20261001/scip-rule-fidelity/note.md research-20261001/scip-rule-fidelity/code/check_revision_r2.py` | Exit 0; no whitespace errors. Read-only check; no git state changes. |

Superseded outputs: the first author agent's loop and recheck logs are kept
in `logs/superseded_first_agent/` for the comparison above; analysis
outputs computed before the second `zk_fast` fix were deleted (the
generator values were identical; MINLPLib values changed, e.g. two spurious
ratios above 1).

## Limits

- *Samples.* One SCIP run per instance (default seed), 60 s / 120 s time
  limits, 64 MINLPLib instances drawn from 394 (16 never called the
  handler's enforcement), and at most 50 + 150 sampled attempts per
  instance. The MINLPLib ratio statistics rest on 1,067 corners from 26
  instances; a few instances dominate the per-corner numbers, hence the
  instance-weighted rows. In the 34 of 64 MINLPLib runs that hit the
  120 s time limit, machine speed and the overhead of writing 2.1 GB of
  gzipped dumps change which attempts are reached. Thus the Section 6
  counts and the samples describe the instrumented binary's runs;
  they need not match an unpatched SCIP run with the same time limit.
  The instrumentation preserves the algorithm's behavior per attempt.
- *What is measured.* `z_C/z_K` is the single-cut bound on the corner
  relaxation. It ignores the other LP rows (the sfree note's Section 9.2
  shows that LP re-solves change the picture), cut selection, and
  branch-and-bound effects. Rates are floored at `10^-9 max w`; ratios of
  essentially 0 on zero-rate rays depend on this convention only in that
  they would be exactly 0.
- *`z_K`.* Exact for `ρ ≤ 2` and by a generic 3-ray KKT enumeration for
  `ρ = 3` (can miss degenerate minimizers; Gurobi found a 0.06% lower value
  in one validated case); for `ρ ≥ 4` from the smaller of the two-ray
  value and Gurobi's incumbent. The 56 loose or missing solver-reported
  brackets are not the only uncertainty: even "optimal" statuses and
  tight reported gaps do not certify bounds on badly scaled corners
  (Section 5). The degeneracy test detects a zero-cost face
  meeting `S` only through at most two rays when `ρ ≥ 3`. All in floating
  point; four reduced-space classes lose exact dumped-data linear drift
  along zero-rate rays (Section 5.2). The candidate check accepts points
  with `q ≤ 10^-3 q(s̄)`, which
  can make `z_K` slightly too small (worst validated case 0.36%).
- *Fidelity.* SCIP's rays and LP point are taken from the dump, not
  recomputed from the LP; the end-to-end rate check covers only cuts that
  reached the LP. My replay of SCIP's root finder cannot reproduce the
  interval rounding (107 rays). Monoidal coefficients (Case 2, integer
  rays) were checked only for their presence.
- *Earlier notes.* For the `two_ray` error I rechecked Sections 9.2 and
  9.3 of the sfree note, not its other uses of `core.corner_bound`
  (validation, adversarial and random corners), where antiparallel scaled
  rays are unlikely but were not excluded.
- *Process slips.* Two runner bugs (an `xargs -L` line continuation
  merged job lines; two `pkill` patterns matched my own shell) forced
  reruns. All reported outputs come from completed jobs, checked as
  described.
- *Data volume.* `logs/runs_minlplib/` holds 48 gzipped dump files
  (2.20 GB) preserved in the `scip-fidelity-traces` evidence package.
  Restore that package using [the archive instructions](../../artifacts/README.md)
  before checks that read the original dumps. The 64 solver logs and compact
  analyses remain in Git. `logs/index/` is 38 MB and can be regenerated with
  `run_index.sh` in about two minutes. Regenerating the dumps needs the
  patched build and roughly 20–30 minutes on seven cores.

## Open questions

1. Are the short ray components behind most first-piece dynamism aborts
   themselves LP noise, and would the resulting cuts be safe? The test
   depends on ray length, and rescaling would make 96.1% of sampled and
   91.7% of all first-piece aborts pass it (Section 6). Ray scaling, with
   cut coefficients converted back to the original nonbasic coordinates,
   is a candidate change whose safety needs exact or high-precision
   testing, including 4b and the other numerical checks. Such checks
   should also distinguish rounded zero coefficients from nonzero small
   coefficients and ill-conditioned restrictions before any solver-level
   test of whether scaling or a different numerical rule closes more gap.
2. On degenerate corners (`z_K = 0`, three quarters of MINLPLib) the
   single-cut bound cannot guide the choice of set. What should replace
   it: a perturbed objective, the next LP's objective, or depth in the
   cone?
3. Zero-cost rays that never meet `S`: SCIP's set gives `z_C = 0` there
   although `z_K > 0`. How much can a set with such a ray in its recession
   cone gain, and is there a
   cheap rule (for example a constrained point rule or an orbit member) that
   does this, given that the sfree note's Proposition 2 shows that the
   supremum can fail with zero rates?
4. Why are most checkable intersection cuts never observed in an LP
   (density, parallelism, efficacy), and is the per-expression limit
   between restarts intended?
5. Does the stronger single cut of the orbit rule (sfree note) survive
   SCIP's numerics tests and cut selection inside SCIP?
6. Could the reviewer's full-space formulation improve the unresolved
   `ρ ≥ 4` estimates? It reported optimality within 60 s on all 35
   `upper`-kind records tried, including `tln12` records, but the
   inconsistencies in Section 5 require independent verification before
   those reports can support stronger conclusions. This is future work;
   no solver reruns were made for this revision.
