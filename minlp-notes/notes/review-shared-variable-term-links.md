# Review: shared-variable term links (results note, code, bilinear pilot)

**Later corrective audit (2026-09-22).** The
[ten-agent audit](review-minlp-developments-20260922.md) corrects the blanket
claim about joint epigraphs, supplies the nonnegative factors in the displayed
moment-cone formulation, and distinguishes tolerance feasibility from exact
feasibility of the saved rational point. The historical empirical findings
below retain their stated numerical scope.

Date: 2026-09-21. Independent adversarial review of
[results/shared-variable-term-links.md](../results/shared-variable-term-links.md),
`code/shared_variable_terms/`, and, briefly,
[notes/row-hull-bilinear-items-pilot.md](row-hull-bilinear-items-pilot.md) with
`code/row_hull_bilinear/`. No existing file was edited. Review scripts and raw
outputs are in `code/shared_variable_terms/review/` (listed at the end).
Machine: 36 cores; all review runs used `nice`, at most 6 threads in total, no
run longer than 15 minutes.

## Most important findings

1. **The "failed variant" section and the README misreport an invalid bound.**
   `pricing050` is a *maximization* problem (OSiL `maxOrMin="max"`;
   `instancedata.csv` objsense `max`, primal -1813.83, dual -1153.00). A SCIP
   dual bound of -145 (my rerun: -187.05 after 60 s) is an upper bound and is
   valid, only very weak. The "best known value below -1895" is the *worse*
   incumbent -1895.72 that SCIP found in the linked pilot, not the best known
   value. Nothing in the record shows an invalid bound. Fix: rewrite lines
   152-158 of the note and the README line for `moment_pilot.py` ("failed
   variant, invalid bound observed") to: the cone form gave a much weaker bound
   (-187 against -1465 linked and -1487 native, maximization) and no solution.
   The same sign error affects the 60 s table (see finding 5).
2. **The headline claim on `waterno2_06/09/12/18` holds as far as it can be
   checked.** The MINLPLib page values quoted in the note were re-fetched today
   and match exactly (best dual 165.19 SCIP / 273.90 SCIP / 479.51 Gurobi /
   770.74 SCIP; primal 282.888 / 922.595 / 2263.36 / 5269.64; `ghg_2veh`
   7.4335 SCIP / 7.7709). My own 870 s, 4-thread run of the linked model on
   `waterno2_18` (reviewer's reader and builder, `review/run_linked_point.py`)
   gives dual 2442.70 and primal 5151.90; the primal point, evaluated in the
   NATIVE model with a plain-float evaluator of the OSiL trees, has maximum
   constraint violation 9.9e-7 (absolute and relative), bound violation 1e-16,
   integrality violation 0. So a point below MINLPLib's 5269.64 exists at
   Gurobi's 1e-6 tolerance; it does not meet MINLPLib's 1e-8 standard, and the
   note's own 5138.30 point was never saved and cannot be checked. Every dual
   bound in all three jsonl files is below the best primal value known for its
   instance. The bounds remain uncertified floating-point output.
3. **Validity of the reformulation: no error found.** At native Gurobi
   incumbents of 18 instances (`review/validity_check.jsonl`) every link
   constraint and every `t_k` bound holds to at most 1.8e-15 relative. The
   note's Gurobi translation (`gurobi_link.py`, executed as is with variables
   fixed) accepts the native incumbent with the same objective as my evaluator
   on 12 of 13 instances; on `ex8_4_7` both reject it because the point is
   infeasible by 8.7e-4 in exact arithmetic (Gurobi tolerance artefact), which
   also means Gurobi's "optimal" 28.931 on `ex8_4_7` (below MINLPLib's primal
   29.047) is uncertified.
4. **SCIP error confirmed** with SCIP's own OSiL reader on `waterno2_02` and
   `waterno2_03`: `checkSol` (default tolerances and `completely=True`)
   accepts Gurobi's points 39.5714 and 115.0072 while SCIP reports "optimal"
   42.3436 and 130.8405. The result is setting-dependent: with
   `numerics/feastol 1e-7` SCIP returns 46.149 on `_02` but the correct
   115.0045 on `_03`; with presolving off 42.3435 and 117.579.
5. **Numbers.** Two quoted numbers are wrong: the term-by-term volume for
   `(x^2, x^3)` on `[1,2]` is exactly `3/20 = 0.1500` (Ballerstein's value is
   exact, the note's 0.1497 is an integration error); the 60 s table is headed
   "(minimization)" but contains `pricing050` (maximization), where the linked
   bound -1290 is *weaker* than the native -1331. Everything else recomputes
   (details below). `scan_candidates.txt` is referenced by the README and
   `run_links.sh` but does not exist, so the SCIP pilot cannot be reproduced as
   written; the `lnts_soc.py` numbers (0.5423 vs 0.5522) have no raw record.
6. **Bilinear pilot.** The 6n-variable state form is exact: on 60 random
   instances (n <= 5, random widths and residuals, random linear objectives in
   `(x, y, t)`) its LP value equals the global minimum of the nonconvex
   problem solved by Gurobi to gap 1e-9 (max difference 1.8e-15). Caveat:
   `proto.py`'s `exact()` is not a brute force over the true set; it enumerates
   the row vertices with `y in {0,1}`, which presupposes the concavity argument
   it is meant to confirm. The argument is correct, but the note's "brute-force
   hull value" should say "vertex enumeration".

## Task 1: validity of the reformulation

Files: `link_detect.py` (rules), `link_pilot.py` lines 43-62 (same rules,
duplicated), `gurobi_link.py`.

Detection rules, checked case by case:

- Negative exponent with `lb = 0`: excluded by `link_detect.py:27`
  (`min(p) > 0 or inst.var_lb[v] > 0`). Correct. With `lb > 0` the `t` bounds
  `sorted((lo**p, hi**p))` are correct for negative `p` (the sort handles the
  reversal). With `lo = 0` and `p > 0`, `0.0**p = 0.0`. Correct.
- `times` nodes: `x*x*y` is read as exponent 2 of `x` (count of bare `var`
  children); constants and other factors do not matter. A product whose
  repeated factor carries a coefficient (`("times", ("num", c), ("var", i))`
  from the reader) is not counted, which misses a term but never adds a wrong
  exponent. Instances where this rule fires: `nvs05`, `nvs22`, `primary`.
- `divide(num, var)` -> exponent -1: correct, the model contains `1/x`.
- Squares from the quadratic section: `(i, i, c)` -> exponent 2. Correct.
- Infinite upper bound: excluded (`math.isfinite(inst.var_ub[v])`). Integer or
  binary variables (`nvs05/16/21/22` have integer `x` with `ub = 200`): the
  identity `t_k = x^{p_k}` holds regardless of type; `t` bounds up to
  `200^4 = 1.6e9` (`nvs21`) and `2^50 = 1.1e15` (`ex4_1_2`, 49 exponents) are
  valid but numerically poor. Not an error, but worth a cap.
- Exponent sets after removing 0 and 1: correct; all sets found are listed in
  `review/detect_audit.py` output (e.g. `(-0.36, -0.075)`, `(-1.5935, -1, 2.4242)`,
  `(0.5, 2, 3)`, `(0.06, 0.71)`). Reference exponent = smallest magnitude; the
  link `t_p = t_ref^{p/ref}` is valid in every sign combination because a
  negative exponent forces `x >= lb > 0`, so `t_ref > 0`.
- `sin`/`cos` only of a bare variable: valid for any bounds (`lnts*`,
  `inscribedsquare*`).

Independent test at feasible points (`review/validity_check.py`, 2 threads,
120 s per native solve, reviewer's OSiL reader and Gurobi builder):
`waterno2_02/03/04`, `ghg_1veh`, `ghg_2veh`, `lnts50`, `pricing050`
(incumbent -1813.83, equal to the known primal), `ex8_4_7`, `wastepaper4`,
`ex4_1_2`, `nvs05`, `nvs22`, `launch`, `cvxnonsep_psig40`, `ex8_3_13`,
`ortez`, `otpop`, `ex1226`. Maximum violation of any link constraint or
`t` bound: 1.8e-15 relative (`ex4_1_2`, exponent 49). All pass 1e-7.

Translation in `gurobi_link.py` (`expr`, lines 118-136): `sum` and `times`
are folded n-ary; `negate` is `-1.0 * k`; `divide` and `power` map to
gurobipy operators (all `power` nodes in the 46 instances have a numeric
exponent; bases are `var`, `sum`, `times`, `divide`; exponents are
non-integer in 15 instances — fine for gurobipy's `NLExpr ** float`, and every
non-integer power in these files has a base with `lb >= 0`, so Gurobi's
domain convention for `x**p` does not bite). Objective constant and sense
(lines 153-154) are handled; `pricing050` and `inscribedsquare*` are
maximizations and are built as such. Ranged rows would be split into two
constraints (lines 155-158); none occur in the 46 instances. OSiL objective
`weight` is ignored; it is 1 everywhere in the set. End-to-end check
(`review/note_model_point_check.py`): the note's model, built by executing
`gurobi_link.py` with `optimize()` removed and all original variables fixed to
my native incumbent, reports the same objective as the plain-float evaluator on
`waterno2_02/03`, `ghg_1veh`, `lnts50`, `wastepaper4`, `launch`,
`cvxnonsep_psig40`, `ex4_1_2`, `nvs05`, `ex8_3_13`, `ortez`, `pricing050`,
native and linked. On `ex8_4_7` both the native and linked note models declare
the fixed point infeasible; my evaluator gives row violation 8.7e-4 for that
point (row 26), so the point Gurobi returned as optimal (28.922 in my run,
28.931 in the note's) is infeasible in exact arithmetic. This is a Gurobi
tolerance issue on a badly scaled instance, not a translation error, but the
note should not count 28.931 as a solve that agrees with MINLPLib's 29.047.

Agreement of optimal values (`review/recompute_numbers.py`): Gurobi native vs
linked agree on all 23 instances solved by both. SCIP native vs linked disagree
on `waterno2_03` (130.84 vs 130.75, both wrong). Cross-solver, both "solved":
only `waterno2_02/03/04` disagree (the SCIP error). SCIP's "optimal" 1.20585 on
`ex7_3_5` (native and linked) is below MINLPLib's listed dual bound 1.206653 by
7e-4 relative; not investigated.

Verdict: valid on every instance where the links are applied; translation
faithful on the instances tested.

## Task 2: the headline claim

(a) Dual bound vs best primal: for every record in `results_gurobi_60.jsonl`,
`results_gurobi_1800.jsonl` and `results_links.jsonl`, the dual bound is on the
correct side of the best primal value (own runs and `instancedata.csv`) except
the three SCIP `waterno2` errors already reported in the note. Note that the
repository's `instancedata.csv` (12 Sep 2026) lists dual bounds 108.40,
134.22, 280.55, 383.66 for `waterno2_06/09/12/18` (the Xpress/Antigone
values), lower than the page values used in the note; the note should say which
source it compares against (it does: the page, verified today).

(b) Own run: `review/run_linked_point.py waterno2_18 870 4` (linked model from
the reviewer's reader, links from `link_detect.detect`): status time limit,
dual 2442.70, primal 5151.90, 279,540 nodes. The point (saved in
`review/point_waterno2_18_linked.json`) evaluated in the native model with
`review/osil_eval.py`: objective 5151.8978, max row violation 9.87e-7 (row
3514, a `t = x^3` equation), bound violation 1.1e-16, integrality violation 0
(all 162 binaries integral). So a point better than MINLPLib's 5269.64 exists
at 1e-6 tolerance; MINLPLib's pages list points with infeasibility 1e-8 to
1e-13, so this point would need polishing before submission. The note's
5138.30 point was not saved by `gurobi_link.py` (it writes no solution file)
and cannot be checked.

(c) Structure of `waterno2_*` (`review/waterno2_structure.py`): every
nonlinear row is exactly `-t + x^3 = 0` and every diagonal quadratic row is
`-s + x^2 = 0`, both equalities; 234 flow variables of `waterno2_18` carry
both, with bounds `[0, 0.5..0.8]` or `[0.6..0.85, 1]`, all continuous. With
`x >= 0`, `t3 = t2^1.5` is an identity on the feasible set; `t` bounds
`[lo^2, hi^2]`, `[lo^3, hi^3]` are correct. 54 further variables have only a
square and get no link. Valid.

(d) Uncertified: the dual bounds are single floating-point Gurobi runs (no
certificate, no second solver — SCIP is unusable on this family); the four
1800 s runs were done once, ten processes at a time on a 36-core machine
(30 threads), so timings and node counts are not reproducible; the primal
points are checked only to 1e-6; and the comparison with the MINLPLib page
mixes unknown solver versions, options and time limits, as the note says.
What is established: with the links, Gurobi 13 reports a bound above the
listed best dual on all four instances in one run each, and I reproduced the
effect on `waterno2_18` in an independent implementation.

## Task 3: the SCIP error

`review/scip_check.py` (Gurobi 1 thread, tolerances 1e-9; SCIP reads the
OSiL file itself, 120 s limit, gap 1e-4):

| instance | Gurobi point (evaluator viol.) | SCIP `checkSol` | SCIP default | presolve off | feastol 1e-7 | both |
|---|---|---|---|---|---|---|
| `waterno2_02` | 39.57142 (1.0e-9) | accepted (also `completely=True`) | optimal 42.3436 | gaplimit 42.3435 | optimal 46.1490 | optimal 55.4031 |
| `waterno2_03` | 115.00725 (9.7e-10) | accepted | optimal 130.8405 | optimal 117.5788 | optimal 115.0045 | time limit, dual 122.61 |

Confirmed: SCIP 10 with default settings declares optimal a value above a
point its own checker accepts on the original problem, with SCIP's own reader
(so the note's builder is not the cause). The wrong value changes with
presolving and tolerance settings, in both directions (tighter `feastol` makes
`_02` worse and `_03` right), which points to invalid domain reductions or
cuts rather than a tolerance choice. The note's sentence "the listed SCIP
bounds for this family are doubtful" is justified. The note's numbers
(42.343, 130.8, 161.1) recompute from `results_links.jsonl`; the SCIP "native
and linked alike" on `waterno2_03` is 130.84 vs 130.75.

Code remarks: `check_scip_waterno2.py:14` is a no-op assertion
(`... or True`); the script leaves Gurobi at its default thread count (all 36
cores) — set `Threads`.

## Task 4: numbers

Recomputed with `review/recompute_numbers.py`, `review/scip_counts.py`,
`review/volume.py`, `review/volume_fine.py`. Matches unless noted.

- Scan: 1,625 records, 31 parse errors, 1,594 parsed, 189 with a variable
  carrying >= 2 distinct univariate terms. Matches. (1,632 OSiL files in the
  cache; 7 are absent from `scan.jsonl`, immaterial.) 48 instances with links:
  matches `link_instances.txt`.
- Gurobi 60 s: 46 instances; solved (status 2) 25 native, 24 linked; only
  native `ex8_4_7`, `lnts50`; only linked `wastepaper4`; shifted geometric
  mean (shift 1 s, unsolved at 60 s) 8.18 vs 8.39; linked faster on 9 of 23.
  All match. Table: all entries match the jsonl; `waterno2_03` 12.1 -> 3.5 s,
  `waterno2_04` 47.7 -> 34.6 s, `lnts50` native 24.1 s match. **Error:** the
  table is headed "(minimization)" and lists `pricing050`, a maximization; there
  the linked bound -1290.3 is weaker than the native -1331.0, and the text
  gives no sign that this row is a loss. Fix: mark the sense or move the row to
  the list of negative cases.
- Gurobi 1800 s table: all ten dual and primal values match to the printed
  digits; MINLPLib page values verified today (see finding 2).
- SCIP 60 s: "24 native and 25 linked of 48" holds only if `gaplimit` counts as
  solved (optimal alone: 15 vs 14) and it includes the wrong "optimal"
  161.135 of `waterno2_04` linked; without that solve it is 24 vs 24. Mean time
  (shift 1, unsolved at 60) 10.4 vs 10.9 s: "unchanged" is fair. The note
  should say "solved to gap 1e-4" and exclude the erroneous `waterno2` solves.
- `lnts50` 1800 s: linked dual 0.55432 vs native 0.51168, optimum 0.55467;
  `lnts100` 0.54560 vs 0.53974. Match. The `lnts_soc.py` claim (0.5423 after
  300 s against 0.5522) has no raw output file; unverifiable.
- Volumes for `(x^2, x^3)` on `[1,2]`: term-by-term
  `int_1^2 (3x-2-x^2)(7x-6-x^3) dx = 3/20 = 0.1500` exactly (sympy and a
  200,000-point midpoint rule agree); **the note's 0.1497 is wrong** and the
  parenthetical "(his 0.1500)" should be dropped. With the link, taking the
  relaxation of `t3 = t2^1.5` on `t2 in [1,4]` as the region between the curve
  and its chord, the volume is 0.0730 (two grid resolutions agree to 5
  digits); the note's 0.0729 is consistent to the precision of its method.
  The note should state what relaxation of the link it integrated.

## Task 5: overclaiming and fairness

- Summary bullet 3 ("the links raise Gurobi's dual bound ... All four exceed
  the best dual bounds listed") is supported by the record and by my
  reproduction, with the qualifications the note already gives. It should add
  that the improvement on the 60 s runs of the same family is also present
  (150/464/1110/2236 vs 96/175/352/606), which is stronger evidence than a
  single 1800 s run, and that the primal side improved on three of four.
- "SCIP 10 returns a wrong optimum on `waterno2_02`" is confirmed; the
  stronger sentence "its dual bounds there ... prove nothing" is fair.
- Comparison with MINLPLib page values is fairly qualified (solver version and
  time unknown). The repository CSV disagrees with the page; say so.
- Single runs, 8 x 4 = 32 and 10 x 3 = 30 threads on 36 cores: the machine
  was near saturation but not oversubscribed; timing comparisons (8.2 vs 8.4 s,
  "faster on 9 of 23") are within run-to-run noise and the note does not claim
  a timing win, which is right.
- Negative cases are reported (`lnts*` under Gurobi, `ex8_4_7`, `ghg_2veh` at
  60 s, `waterx`, `pricing050` once the sense is fixed). "Results are mixed on
  small instances and large on one family" is an accurate summary.
- Overclaim in the "failed variant" section (invalid bound): see finding 1.
- Minor: the `ex8_4_7` native "solve" at 28.931 is a tolerance artefact and
  should not be listed as solved without a remark; `ex7_3_5` SCIP value below
  MINLPLib's dual bound is unremarked.

What the evidence supports: the links are valid; on the `waterno2` family
they make Gurobi's root and tree bounds much stronger in every run recorded
(60 s and 1800 s, four instances each), and the resulting bounds are above the
best listed on MINLPLib; elsewhere the effect is small or negative; no claim
about SCIP on this family can be made; the cone variant on `pricing050` is
weak, not invalid.

## Task 6: bilinear pilot note

`review/bilinear_bruteforce.py`: 60 random instances, `n in {2,...,5}`,
`k in {1,...,n-1}`, `w in [0.5, 2]`, `r in (0.05w, 0.95w)`, Gaussian
objectives in `(x, y, t)`. The state-form LP value equals the global optimum of
`min c.(x,y,xy)` over `{sum x = kw + r, 0 <= x <= w, 0 <= y <= 1}` solved by
Gurobi as a nonconvex QCP to gap 1e-9, max difference 1.8e-15. The exactness
claim holds. The total-unimodularity argument in the note is right (each state
column has one entry in its item row and at most one in the two cardinality
rows: a bipartite incidence structure), and the concavity argument for vertex
generators is right (`min_y (c_y + c_t x) y = min(0, c_y + c_t x)` is concave
in `x`). Two wording points: `proto.py`'s "exact" value is vertex enumeration
that assumes the concavity argument, so "equals the brute-force hull value"
overstates the check; and the note should say the row polytope's vertices have
that form only for `0 < r < w`, which `blend.py`/`pool.py` already guard with
`if r < 1e-6 or w - r < 1e-6: continue`. The negative pilot is described
without overclaim; the sentences "root gap 0 on 3 of 4" and "0–0.24%" were not
rerun.

## Concrete fixes (file: line)

- `results/shared-variable-term-links.md:32` — replace "0.1497 term by term
  (his 0.1500)" by "0.1500 term by term (exact, 3/20)".
- `results/shared-variable-term-links.md:90-98` — the table is not all
  minimization; mark `pricing050` as maximization (linked bound weaker) or
  move it to line 106-108 with the negative cases.
- `results/shared-variable-term-links.md:147-158` and
  `code/shared_variable_terms/README.md:12` — `pricing050` is a maximization;
  the -145 bound is valid; replace "invalid bound" by "much weaker bound and no
  solution"; the "-1895" is a worse incumbent, the best known value is
  -1813.83.
- `results/shared-variable-term-links.md:130` — say "solved to gap 1e-4
  (optimal or gap limit)" and note that the linked count includes the wrong
  `waterno2_04` solve.
- `results/shared-variable-term-links.md:87` — flag `ex8_4_7` native 28.931
  as below MINLPLib's primal and infeasible at 1e-4 in exact arithmetic.
- `results/shared-variable-term-links.md:121-122` — may now cite: an
  independent linked run found 5151.90 feasible in the native model to 9.9e-7
  (this review); still not to MINLPLib's 1e-8.
- `code/shared_variable_terms/README.md:5`, `run_links.sh:5` — restore or
  regenerate `scan_candidates.txt` (the SCIP pilot ran on 180 instances; the
  list is recoverable from `results_links.jsonl`).
- `code/shared_variable_terms/check_scip_waterno2.py:14` — delete the no-op
  assert; line 15 — set `m.Params.Threads`.
- `code/shared_variable_terms/link_pilot.py:43-79` duplicates
  `link_detect.py`; import it instead (as `gurobi_link.py` does).
- `notes/row-hull-bilinear-items-pilot.md:36-37` — "brute-force hull value"
  -> "value over the row vertices with `y in {0,1}` (`proto.py`)".

## Review scripts and outputs (`code/shared_variable_terms/review/`)

- `osil_eval.py` — independent OSiL reader and plain-float evaluator/checker.
- `gmodel.py` — reviewer's Gurobi builder from that reader (links via
  `link_detect.detect`).
- `validity_check.py`, `validity_check.jsonl` — task 1 point test (18 instances).
- `note_model_point_check.py`, `note_model_point_check.jsonl` — the note's
  own model with variables fixed to native incumbents.
- `detect_audit.py`, `tree_ops.py`, `waterno2_structure.py` — detection and
  expression-shape audits.
- `run_linked_point.py`, `run_waterno2_18_linked.jsonl`,
  `point_waterno2_18_linked.json` — task 2(b).
- `scip_check.py`, `scip_check_waterno2_02.txt`, `scip_check_waterno2_03.txt` — task 3.
- `recompute_numbers.py`, `scip_counts.py`, `volume.py`, `volume_fine.py` — task 4.
- `bilinear_bruteforce.py` — task 6.

Commands run (targeted, local): the scripts above via
`uv run --project code/minlp_solver_lab python`, plus
`moment_pilot.py pricing050 {moment,linked} 60`. No project-wide checks and no
CI inspection.
