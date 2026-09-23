# Review of LB-ESH method note and prototype (2026-09-12)

**Historical review; corrections, 2026-09-19.** The
[new theory and proofs](lbesh-development-theory.md) correct two statements
in this review: every bounded convex subgradient satisfies the radial
separation argument (no special directional choice is required), and
individual disjunct Slater margins alone do not imply the objective-error
estimate suggested in S4 for intersected hulls. Current independent reviews
are linked in the [development log](lbesh-development-log.md). Findings below
describe the code inspected on the original review date.

Reviewed: [`lbesh-20260912-method.md`](lbesh-20260912-method.md) and
`code/minlp_solver_lab/lbesh/{structure,master,solver,nlfunc}.py`.
Reviewed code was not modified. Test scripts added under
`code/minlp_solver_lab/lbesh/tests/` (run from `code/minlp_solver_lab` with
`OMP_NUM_THREADS=1 PATH=/home/sgusev/miniconda3/envs/solvers/bin:$PATH uv run python lbesh/tests/<script>`):

| script | purpose |
|---|---|
| `review_compare_instances.py` | 8 small convex catalog instances x {hull/multi, hull/single, bigm/single, bigm/multi} vs BARON (`optcr=1e-6`, 60 s); output in `review_compare_instances.jsonl` / `.log` |
| `review_handmade.py` | A: OR-disjunction; B: integer variable inside a disjunct with an inequality-only nonlinear row; C: maximisation with nonlinear objective; D: variable names with spaces/commas |
| `review_fixed_var_row.py` | disjunct row whose variables are all fixed |
| `review_bigm_unbounded.py` | big-M cut whose M is infinite |

Summary: the mathematics is sound for XOR disjunctions with bounded boxes;
the note's proofs need small repairs (subgradient choice, OR disjunctions,
tolerance-level rigour of the bound). The prototype returns the BARON
optimum on all 8 catalog instances tested, but three code paths give wrong
answers or wrong statuses on simple hand-made models: OR (`xor=False`)
disjunctions in the hull master (wrong optimum reported as `optimal`), disjunct
rows whose variables are all fixed (disjunct silently forced off), and silently
dropped big-M cuts (status `optimal` with a large gap).

## Blocking

### B1. Hull master is not exact for OR disjunctions (`xor=False`)

`master.py:79` writes `sum_k lambda_ik >= 1` for `xor=False` while keeping
`x = sum_k nu_ik` and `lambda_ik x^L <= nu_ik <= lambda_ik x^U`. With two
selected disjuncts (`lambda = (1,1)`) the master allows `x = nu_1 + nu_2` with
`nu_1 in P_1`, `nu_2 in P_2`, i.e. the Minkowski sum, not `P_1 ∩ P_2`.
Lemma 1(a)'s "disaggregated form (`nu_ik = x` when `lambda_ik = 1`, else 0)"
is inconsistent with `x = sum nu` when two lambdas are 1. Consequences:

- the master is still a relaxation (any feasible point can be written with
  exactly one true disjunct), so the LB stays valid, but
- the `n == 0 => master point is GDP-feasible` shortcut (`solver.py:651` and
  the single-tree closing check at `solver.py:738-741`) accepts an infeasible
  point, and Gurobi's incumbent in the single tree is infeasible.

Reproduction (`review_handmade.py`, case A): `min x`, `x in [-2,0]`, two
disjuncts each with `x^2 <= 1`, `Disjunction(..., xor=False)`. True optimum
`-1` (BARON on big-M: `-1`). Result: hull/multi and hull/single return
`status optimal, obj -2.0, x = -2` (violates both disjuncts); big-M variants
return `-1` correctly. Pyomo's own `gdp.hull` refuses OR disjunctions
(`hull.py:598`: "Cannot do hull reformulation ... Must be an XOR!").

Fix: in `Master._add_disjunction`, raise for `xor=False` when
`formulation == "hull"` (mirroring Pyomo), or reformulate the OR as an XOR
over the non-empty subsets of disjuncts (each subset disjunct carries the
intersection of the constraint sets, plus `lambda_ik = OR of subset
indicators` links if lambda appears in the objective or logic rows). Update
the note's problem class ("or >= 1") and Lemma 1 accordingly.

### B2. Constraints whose variables are all fixed lose their constant

`structure.py:132-136`: when `generate_standard_repn` reports `is_fixed()`,
the constant `val` is checked for feasibility and the row is returned as
`LinRow(name, [], [], lb, ub)` with the *original* bounds instead of
`LinRow(name, [], [], lb - val, ub - val)` (the linear branch two lines
later does subtract the constant). In the hull the row becomes
`0 >= lb * lambda`, `0 <= ub * lambda`, in big-M `0 >= lb - M(1-lambda)`;
either forces `lambda = 0` whenever `lb > 0` (or `ub < 0`). For a global row
the master gets `0 >= lb` and is declared infeasible.

Reproduction (`review_fixed_var_row.py`): `p` fixed at 2, disjunct `d1` with
`p >= 1` and `x^2 <= 1`, disjunct `d2` with `x >= 3`, `min x`. Extracted
`d1.c = LinRow(vars=[], lb=1, ub=inf)`. hull/multi and bigm/multi report
`optimal, obj 3.0, d1 = 0`; BARON: `0`. Fixed variables are common in the
catalog builders (parameters modelled as fixed `Var`s), so this can silently
change optima.

Fix: return `LinRow(name, [], [], lb - val, ub - val)` and let the master skip
rows with no variables (they are then `0 <= ub - val` tautologies), or drop
such rows at extraction after the feasibility check; for an infeasible
constant row inside a disjunct, mark the disjunct infeasible (fix its
indicator to 0) instead of raising `StructureError` for the whole model.

### B3. Big-M cuts with infinite M are silently dropped; single tree then reports `optimal` with a wrong incumbent

`master.py:171` returns `(None, None)` when the interval bound of the cut's
left-hand side is infinite; `solver.py:358` skips the cut and does not count
it in `n`. In the single tree the MIPSOL callback then adds no lazy
constraint for a violated disjunct row, so Gurobi accepts the infeasible
master point as incumbent and prunes with it; `ObjBound` becomes the value
of that infeasible point. In the multi tree, `n == 0` with an NLP incumbent
that differs from the master value loops to `milp_max_iters` re-adding the
same cached cuts.

Reproduction (`review_bigm_unbounded.py`): `y >= 0` unbounded above (only
bounded through a global nonlinear row `y^2 <= 25`, which OBBT ignores),
`d1: exp(y) - x <= 0`, `d2: y^2 <= 1`, `min -y`; true optimum `-ln 10 =
-2.3026`. bigm/single: `status optimal, obj -2.3026, lb -5.0` (gap 2.7 but
status `optimal`; Gurobi's incumbent is `y = 5, d1 = 1`, infeasible);
bigm/multi: `status iteration_limit` after 50 identical iterations. The hull
raises `hull needs bounds on y` up front, which is the right behaviour.

Fix: treat a missing big-M bound for a cut as an error at cut time (or, at
`Master.__init__`, require finite bounds on every variable of a disjunct's
nonlinear rows, as the hull already does). Independently, the single-tree
final status should be `optimal` only if `ub - lb` is within tolerance.

## Should-fix

### S1. Lower bound taken from `ObjVal`, not `ObjBound`, in the multi tree

`solver.py:639`: `self.lb = max(self.lb, ObjVal)` at status `OPTIMAL`. Gurobi
stops at its default `MIPGap = 1e-4`, so `ObjVal` can exceed the master
optimum by `1e-4 |obj|`, which equals the solver's own `rel_tol`; the
returned "optimal" gap can thus be up to about `2e-4`. The theorem's "its
master value is a valid lower bound" holds only for the exact master optimum.
Evidence from the comparison run: `lb - obj = +1.2e-7` on FLay02 (hull/multi
and bigm/multi), `+8e-9` on basic_step and Circles2D3_modified, i.e. the LB
already exceeds the NLP upper bound (tolerance effects; the `ObjVal` path is
what allows it). Fix: use `ObjBound` (also for `OPTIMAL`) and/or set
`MIPGap` well below `rel_tol` (e.g. `rel_tol/10`) and `FeasibilityTol`
consistent with `cut_tol`. The single tree already uses `ObjBound`.

### S2. Reported objective ignores the sense for maximisation

`solver.py:569`: `stats.obj = self.ub` is the internal minimisation value.
Reproduction (`review_handmade.py`, case C): `max 10 - (x-2)^2 - 0.5x` with
optimum `8.5`; all variants report `stats.obj = -8.5`, `stats.lb = -8.5`
(the model's objective value after write-back is `8.5`, correct). Fix:
multiply `obj`, `lb`, `ub` by `prob.sense` before storing in `stats` (and
swap the roles of lb/ub for maximisation), or document that `stats` is in
min-form. All catalog instances are minimisations, so benchmarks are not
affected yet.

### S3. Note: Lemma 1 / theorem hypotheses to add

- Bounded box on every variable that appears in any disjunct (Lemma 1(a),
  "the bounds force `nu_ik = 0`", and the hull master's `nulb/nuub` rows). The
  theorem says "the box is bounded"; Lemma 1 should say so too, and B3 shows
  the big-M path needs the same for cut variables.
- XOR only (B1), or the OR-to-XOR reformulation.
- "Subgradients suffice": the proof uses that the right derivative of
  `phi` at `s` equals the directional derivative of an active row `j*`, and
  then cuts with `grad g_{j*}(z)`. With a nondifferentiable `g`, an arbitrary
  subgradient at `z` need not have directional derivative `>= delta` along
  `x_hat - xbar`; the argument needs the subgradient attaining the directional
  derivative (or the row to be differentiable, as the implementation assumes).
- The implementation bisects **per row** (`_esh_cuts`), not on
  `phi = max_j g_j` as in the proof. The proof adapts (apply it to each
  violated row `r` with `phi_r`); state it that way, or note the difference.
- The theorem's finite-termination conclusion should be stated relative to
  the code's termination tests: the loop also stops on `_converged()`
  (`ub - lb <= tol`), `CUTOFF`/infeasible master, or "stalled" (eps-feasible
  master point but the reduced NLP failed); the last returns no incumbent.
- Interior point: the note's step 1 includes `A x <= b`; validity of the
  cuts only needs `g(xbar) < 0`, so including the global linear rows can only
  make the Slater problem infeasible unnecessarily (then ECP is used). Say it
  is optional, or drop it.
- Integer variables inside disjuncts: the LP-phase point `p_ik = nu_ik /
  lambda_ik` is fractional; tangent cuts are valid for the continuous
  relaxation of `S_ik`, so validity holds; the packing argument is unaffected.
  Worth one sentence. Case B of `review_handmade.py` (integer `n` appearing
  only in a disjunct's nonlinear row, optimum inside that disjunct) agrees
  with BARON in all four variants (`2.6771242`).
- Big-M LP phase: the transformed cut `a^T x + c <= M (1 - lambda)` is
  violated at a fractional LP point by `eta - M(1 - lambda)`, which may be
  `<= 0`; the "LP phase terminates finitely for fixed `lambda_tol`" claim is
  for the hull master only (the code guards big-M with the iteration cap and
  the stall test).

### S4. Corollary on the hull-relaxation limit

As stated it is a conditional about a hypothetical dense cut set and says
nothing about the LP phase's actual output. What the LP phase delivers at
exit is a point `(x, nu, lambda)` with `g_ik(nu_ik/lambda_ik) <= eps` for
`lambda_ik >= lambda_tol` and `h(x) <= eps`, i.e. an approximately feasible
point of the (perspective) hull relaxation; with a Slater point of margin
`delta` the LP value is within `O(eps/delta + lambda_tol)` of the hull value
(the LP value is always a lower bound since `P_ik ⊇ S_ik`). Replace the
corollary by that statement, or keep the Hausdorff statement but add that
the LP-phase cut set is not dense and the corollary is not a property of
the algorithm.

### S5. `n == 0` incumbent acceptance restricted to hull, and NLP failures cached forever

`solver.py:651` only accepts the eps-feasible master point as incumbent for
the hull. For big-M with integral lambda the point is equally GDP-feasible
(big-M rows are exact at `lambda = 1`), so the same acceptance is valid; without
it a big-M multi-tree run where the NLP value differs from the master value by
more than `abs_tol` repeats identical iterations (see B3). Also,
`solve_reduced_nlp` caches `(None, None)` when Ipopt fails
(e.g. restoration failure on a feasible NLP); a later visit of the same
integer assignment never retries. Cache only successes, or retry once from a
different start.

### S6. Reduced NLP bookkeeping

- `solver.py:403` `v.fix(int(round(v.value)))` raises `TypeError` for an
  integer variable whose value is `None` (a variable in the model but in no
  row or objective is never set); guard or skip.
- `solver.py:425` maps the clone's solution by `v.name` with a silent
  fallback to the master point. Names with spaces and commas worked in case D,
  but a silent fallback would return an inconsistent incumbent (NLP objective
  with master values). Use `ComponentUID(v).find_component_on(m)` and treat a
  miss as an error.
- The eps-feasible master point accepted at `solver.py:651` (and at the end
  of the single tree) carries `t = ObjVal` for the epigraph variable while
  `f(x)` can be up to `cut_tol` larger; case D hull/single shows
  `stats.obj = 1.2499994` against the model objective `1.2500004` at the
  written-back point. This is the documented eps-feasibility, but the
  discrepancy should be reported (or the objective re-evaluated at the point).

## Minor

- `structure.py:135`: a constant-infeasible row inside a disjunct raises
  `StructureError` for the whole model; it only makes that disjunct
  infeasible.
- `_separate_point(..., add=False)` (`solver.py:319`, used at `solver.py:738`):
  `add` is unused; cuts are suppressed only because a no-op `lazy_cb` is
  passed, and they are still counted in `stats.cuts` and appended to
  `cut_log`.
- `_separate_point` with `lamtol = 1e-6` in MIPSOL: Gurobi's `IntFeasTol`
  (1e-5) allows `lambda = 1e-5` on an inactive disjunct; `nu/lambda` is then
  an arbitrary box point, producing wasted (valid) cuts and inflating
  `_max_viol`, which drives the `adaptive` NLP policy. Use `lamtol` of order
  `IntFeasTol` or round lambda in MIPSOL.
- `_cuts_at_solution` is called again with the cached NLP solution on every
  revisit, adding duplicate rows.
- `compute_interior_points` excludes the epigraph row from the global
  interior point, so the objective row always uses ECP cuts; an interior point
  for `t >= f(x)` is trivial (`t = f(xbar) + 1`) and would give ESH cuts there
  too.
- `disjunctive_bounds`/`tighten_bounds`/`_propagate_rows`/`_obbt_missing_bounds`
  were checked and are valid for every feasible point of the GDP: integer
  rounding uses floor/ceil of valid bounds (`Binary.is_integer()` is `True`
  in Pyomo 6.10.1, so binaries are rounded too); the disjunct's own indicator
  is fixed to 1 and skipped in the union, other indicators keep `[0,1]`
  (conservative); an infeasible disjunct contributes crossed bounds that only
  widen the min/max union; OR disjunctions are covered because a feasible
  point lies in at least one disjunct. Note that `extract` mutates the user's
  model (bounds tightened in place, `logical_to_linear` applied,
  `_lbesh_epigraph` added); document this or work on a clone.
- Big-M constants (`master.py:114-138, 160-173`) are valid: `M` is the
  interval maximum of the left-hand side over the current Pyomo bounds, which
  equal the Gurobi bounds since all tightening happens before `Master` is
  built; a cut coefficient on the disjunct's own indicator is bounded with
  `[0,1]`, conservative at `lambda = 0` and exact at `lambda = 1`. In the hull,
  the indicator coefficient is mapped to `c * lambda`, which is the correct
  transform of a row `g(x) + c*lambda <= 0` inside its own disjunct.
- Hull disaggregation (`master.py:80-113`): every variable of any disjunct's
  linear or nonlinear rows (including variables only in nonlinear rows and
  indicator variables of other disjunctions) is disaggregated with continuous
  `nu`; integer `x` stays integer on the aggregated variable. This is valid
  for integral lambda and matches Lemma 1.
- ESH cut validity (`_esh_cuts`): the bisection stops at `point(hi)` with
  `g(z) > 0` (tiny); the tangent at `z` is still valid since a tangent of a
  convex function underestimates it everywhere. Per-row bisection with the
  interior-point check `r.violation(interior) < -1e-9` and ECP fallback is
  fine.
- Single-tree callback: lazy cuts and user cuts are globally valid (tangent
  or supporting hyperplanes transformed by Lemma 1), `cbSetSolution` sets
  `nu = x` for the active disjunct and 0 otherwise, consistent with the NLP
  solution; `PreCrush = 1` is set for user cuts. Correct as far as reviewed
  (except B3).
- Epigraph (`structure.py:215-224`): `t >= sense * (f_nl(x) + lin + const)`,
  master minimises `t`, reduced NLP objective is `sense * value`; constant
  and sign are consistent between master and NLP (case C confirms the
  optimum), only the reporting is unsigned (S2).

## Run checks

`review_compare_instances.py` (2 threads, 60 s, BARON `optcr=1e-6` on the
big-M MINLP; FLay02/FLay03 BARON references failed on a `40/plot_width`
division by zero at initialisation, so the catalog LOA values
`37.94733180`/`48.98979471` were used):

| instance | BARON | hull/multi | hull/single | bigm/single | bigm/multi |
|---|---|---|---|---|---|
| Circles2D3 | 1.17157287 | 1.17157287 | 1.17157251 | 1.17157287 | 1.17157287 |
| Circles2D3_modified | 2.52786403 | 2.52786404 | 2.52786404 | 2.52786404 | 2.52786404 |
| Circles3D4 | 4.0 | 3.99999999 | 3.99999999 | 3.99999999 | 3.99999999 |
| FLay02 | (37.94733180) | 37.94733180 | 37.94733180 | 37.94733180 | 37.94733180 |
| FLay03 | (48.98979471) | 48.98979471 | 48.98979471 | 48.98979471 | 48.98979471 |
| ex1_Lee | 1.17157287 | 1.17157287 | 1.17157251 | 1.17157287 | 1.17157287 |
| basic_step | 2.99002479 | 2.99002487 | 2.99002487 | 2.99002487 | 2.99002487 |
| CLay0203.l1 | 41573.2625 | 41573.2625 | 41573.2625 | 41573.2625 | 41573.2625 |

All statuses `optimal`, all within `1e-6` relative of the reference, and the
written-back incumbents violate the original GDP constraints by at most
`3.6e-7`. Observed tolerance artefacts: `lb > obj` by up to `1.2e-7` in the
multi-tree runs (S1); hull/single `lb` is `4.06` below `obj` on CLay0203.l1
(Gurobi's `MIPGap = 1e-4` stop, gap `1e-4` relative, consistent with
`rel_tol`).

Hand-made GDPs (`review_handmade.py`): case A wrong in hull (B1); case B
(integer inside disjunct, optimum `2.6771242`) correct in all four variants;
case C correct optimum, sign-flipped report (S2); case D correct.
`review_fixed_var_row.py`: wrong optimum in hull and big-M (B2).
`review_bigm_unbounded.py`: wrong status in bigm/single, iteration limit in
bigm/multi (B3).
