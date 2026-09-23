# Review: vertex binarization of separable nonconvex programs

Date: 2026-09-21. Independent adversarial review of
[the result note](../results/separable-vertex-binarization.md) and
[`code/vertex_binarization`](../code/vertex_binarization/README.md).
No existing file was modified.

## Verdict

**Not ready. The mathematics is sound; the computational section is not.**

- Theorem 1, Corollary 2, the exactness claim, and the implementation in
  `sob/model.py` are correct. I found no counterexample in brute-force checks
  on 23 tiny instances, including instances with side variables `y`.
- Theorem 3 is correct in substance but omits one step that the argument
  needs (bound tightening of `s_j` before the chord is rebuilt).
- Several sentences in "Summary" and "Computational evidence" contradict the
  stored data. The most serious: SCIP does **not** time out on the original
  lower-bound family; it solves every size in at most 1.3 s, through symmetry
  handling. The note never mentions this, and never mentions the asymmetric
  family `jeroslow_w` that was added to address it.
- Two solver wrong answers sit unreported in the stored results: Gurobi
  declares a wrong optimum on a reformulated quartic instance (reproduced),
  and BARON declares wrong optima on three original power-cost instances
  (reproduced; a real wrong answer, not an export artefact).
- Two computational claims have no stored data or code at all (BoxQP, explicit
  `x_i`), and the note links to an experiment record that does not exist.

Findings 1–6 are blocking. The rest are should-fix or minor.

## Findings

### 1. SCIP solves the original lower-bound family instantly; the note says it times out — blocking

Evidence. `results/jeroslow.jsonl` (via `summarize.py`): SCIP on the original
model is `optimal` at `n = 12, 18, 24, 30, 60, 120, 400` in 0.05–1.3 s.
The note says, in the Summary, "Gurobi 13 and SCIP 10 time out at `n = 24` on
the original model", and in finding 2, "Original model: all three solvers
reach the limit from `n = 24` with dual bound `0`". Both are false for SCIP.
Other deviations in the same paragraph:

- BARON reaches the limit on the original from `n = 18`, not 24.
- BARON on the reformulation solves `n = 12, 18` (0.8 s) and times out from
  `n = 24`, not "at `n = 60`". At `n = 18` BARON does benefit
  (121 s limit -> 0.8 s), so "none for BARON" is slightly too strong.
- Gurobi: limit from `n = 24` on the original, reformulation solved up to
  `n = 400` in 1.8 s. This part is supported.

Cause, verified: with `misc/usesymmetry = 0`, SCIP on the original `n = 30`
stops at the 20 s limit with dual bound `0` after 93 764 nodes; with the
default it needs 11 nodes. Symmetry handling is outside the box-branching
model of the lower-bound theorems
([separable note](../results/spatial-bb-exponential-lower-bound.md), Setting:
"Symmetry exploitation ... [is] outside the definition").

Correction. State the SCIP result and its cause. Report the asymmetric family
(finding 2) as the main experiment for SCIP. Rewrite the Summary bullet and
finding 2 from the data.

### 2. The asymmetric family `jeroslow_w` is in the code but absent from the note, the README, and the results — blocking

Evidence. `sob/instances.py` defines `jeroslow_weighted`
(`c_i x_i(1-x_i)`, `c_i = 1 + i/n`). No `results/jeroslow_w.jsonl` existed
when I finished. The note and the README do not mention the family. My small
runs (20–60 s limits):

| model | solver | result |
|---|---|---|
| `jeroslow_w-30` original | SCIP | limit 20 s, dual `-1e-9`, 94 862 nodes |
| `jeroslow_w-30` reformulated | SCIP | optimal, 0.5 s, 2 272 nodes |
| `jeroslow_w-400` reformulated | SCIP | **limit 60 s, dual 0** |
| `jeroslow_w-400` reformulated | Gurobi (2 threads) | optimal, 1.5 s |
| `jeroslow-400` reformulated | SCIP | optimal, 2.4 s, 17 nodes |

So the family is a sound replacement for showing that SCIP's success on the
original is a symmetry effect. It also shows that SCIP's `n = 400` success on
the symmetric reformulation probably depends on symmetry too (17 nodes
symmetric, time-out asymmetric). The claim "Gurobi and SCIP solve `n = 400`
in seconds" then holds for SCIP only on the symmetric family.

Are the lower-bound theorems valid for `jeroslow_w`? Not as stated; they are
proved for unit costs. But the separable theorem extends in two lines, and
the note should say so: chords of `x(1-x)` on subintervals of `[0,1]` are
nonnegative, so with `1 <= c_i <= 2` the weighted chord bound satisfies
`LB_w(B) <= 2 LB(B)`. A box pruned for the weighted problem at tolerance `ε`
has `LB(B) >= (1/4 - ε)/2 = 1/4 - ε'` with `ε' = 1/8 + ε/2 < 1/4`. The
optimal value is still `1/4` (`c_0 = 1`). Theorem 1 of the separable note
holds for every fixed `ε' < 1/4`, so the `2^Ω(n)` bound transfers with a
worse constant. The same sandwich works for SDP+RLT node relaxations because
`x_i - X_ii >= 0` is implied there; I did not check the SOS note's
hypotheses for this step.

Correction. Add the family, the extension remark, and the sweep to the note
and README; wait for the sweep to finish before quoting numbers.

### 3. Gurobi returns a wrong "optimal" value on a reformulated quartic instance; the quartic results are not mentioned at all — blocking

Evidence. `results/pilot_quartic.jsonl`, cell `quartic/10/3/1/sob/gurobi`:
status `optimal`, primal `-8.33636`, dual `-8.33719`. SCIP and BARON find
`-9.25012` in the same reformulated model, and all three solvers prove
`-9.25012` on the original. Reproduced deterministically with 4 threads
(40.8 s, same value). With 2 threads Gurobi finds `-9.25012` within 12 s.
Feeding that point as a MIP start to the 4-thread run gives "Loaded user MIP
start with objective -9.25012" and then `optimal` at `-9.25012`. So the point
is feasible in Gurobi's own model and the unaided run cut it off: a Gurobi
13.0.3 wrong answer, not a flaw in the reformulation. (Gurobi also prints
"small constant(s) (< 1e-13) in general constraint NL will be treated as
zero" for these models.)

The note never cites `pilot_quartic.jsonl`. Its content limits the claim
further: on quartics the reformulation is worse for SCIP and BARON
(e.g. `n = 10`: solved in 17–52 s originally, 26–180% gap reformulated) and
improves only Gurobi's gap (75–104% -> 6–19%), with the wrong answer above.

Correction. Report the quartic family, report the wrong answer explicitly,
and do not count that cell as solved. Add an objective cross-check to
`summarize.py` output in the note's tables (the `!` flag already detects it).

### 4. BARON's wrong optima on the power family are real, and the note counts them as solved — blocking

Evidence. `results/pilot.jsonl`: `power/25/{1,2,5}/1/orig/baron` report
`optimal`, 0 nodes, values `44.518`, `44.347`, `58.557`; every other
solver/form pair gives `38.3425`, `39.7778`, `42.3361`. I reran
`power-n25-m1-s1`:

| GAMS export variant | BARON result |
|---|---|
| as exported (`x**0.78`, `x.lo = 0`, start 5) | optimal, 0 nodes, 44.518 |
| `rpower(x, 0.78)` instead of `**` | optimal, 0 nodes, 44.518 |
| start point `x = 0` | optimal, 0 nodes, **53.512** |
| `x.lo = 1e-7` | optimal, 22 nodes, 38.351 (correct up to the perturbation) |

BARON reports a dual bound equal to a local solution that depends on the
start point. `**` versus `rpower` makes no difference, so this is not a GAMS
operator artefact. It is triggered by `x^p`, `0 < p < 1`, with lower bound
exactly `0`, where the derivative is infinite. Whether BARON or the GAMS link
is at fault I could not determine. The reformulated model has the same
expression with `s.lo = 0` and BARON answers correctly there.

The note's finding 1 says "all three solvers solve the original model in at
most 30 s". Three of the nine BARON power cells are wrong answers.

Correction. State this in the note. Exclude the three cells from the
"solved" count, or rerun BARON with `x.lo = 1e-7` and label the runs so.
A general rule for the tables: a run counts as solved only if its recomputed
objective matches the best known value.

### 5. Two computational claims have no data or code — blocking

- BoxQP sentence (finding 4: six `spar` instances, "less than 20%"). No
  result file, script, or instance list exists under
  `code/vertex_binarization`. `grep -i spar|boxqp` finds nothing.
- "A modelling detail that matters" (`n = 60` times out at bound `0` with
  explicit `x_i`, `0.1 s` after substitution). `binarized_ir` has no option
  to keep `x_i`, and no result is stored.

Also, the link to `notes/separable-vertex-binarization-experiments.md` is
dead, and `sob/model.py` cites a non-existent
`notes/vertex-binarization-theory.md`.

Correction. Store the scripts and JSON lines, or delete the sentences. Fix
both links.

### 6. Remaining sentences of "Computational evidence" checked against the data — blocking as a group, each small

- "hits the 60 s limit for `m = 5`, `n >= 50` with SCIP and BARON": also
  Gurobi at `n = 100` (both families); BARON already at `cknap n = 25, m = 5`;
  SCIP **solves** `power n = 50, m = 5` in 21.7 s.
- "SCIP and BARON improve from 40–46% to 3–11% gap": 40–46% is SCIP at
  `n = 25` only. SCIP original gaps are 42–75%; BARON original gaps are
  11–20%. Reformulated: BARON 3.3–3.8%, SCIP 3.6–11.4%. These gaps are
  measured against the best primal value found by any run, not proved
  optimal; say so.
- "Gurobi solves both forms in under a second": 1.2 s and 1.0 s at
  `n = 100, m = 5`. Minor.
- Every cell has one seed. Time limits differ (60 s pilot, 120 s lower-bound
  family). "Times include model construction" includes sympy work and, for
  BARON, GAMS start-up (about 0.3–0.5 s), which dominates many sub-second
  cells. State these.
- "in at most 30 s, usually under 1 s": supported for correct runs
  (maximum 28.2 s, BARON `cknap 100/5`).

### 7. Theorem 3 omits the bound-tightening step — should-fix

The relaxation uses the chord of `g_j` "on the current bounds of `s_j`". In
the node `t_j = 1` the bounds are `[0, 1]`, and the chord there is
identically `0`. The two Chvátal–Gomory cuts make the LP force `s_j = 1/2`,
but the LP objective is still `0` unless the variable bounds of `s_j` are
tightened to `[1/2, 1/2]` and the chord is rebuilt. The proof says "with
`s_j = 1/2` the chord ... on `[1/2, 1/2]` is `1/4`" without saying how the
bounds got there.

Correction. Add: "Feasibility-based bound tightening on the row with the two
cuts gives `s_j in [1/2, 1/2]`; the relaxation is rebuilt on these bounds."
Also state that pruning by bound uses the incumbent `1/4` (k ones and one
half), and that `0 <= k <= n-1`.

The rest checks: both rounding steps are valid Chvátal–Gomory cuts
(integer coefficients on binaries, right-hand sides derived from
`0 <= s_j <= 1`); in the last node both cuts give `k+1 <= sum u_i <= k`;
the tree has the root, `n` nodes `t_j = 1`, and `n` nodes `t_j = 0`,
so `2n + 1`.

### 8. The comparison with the lower bounds needs three qualifications — should-fix

1. The lower bounds cover box branching with specified node relaxations.
   They exclude symmetry handling (finding 1).
2. The repository already records that a known Boolean-quadric clique cut
   closes the root of the **original** model
   ([separable note](../results/spatial-bb-exponential-lower-bound.md),
   "Known global cut outside the model"). The family is an obstruction to a
   certificate system, not a hard problem. The note should cite this next to
   Theorem 3, because it means binaries are not the only way out.
3. Theorem 3 uses integer cutting planes and bound tightening. The
   separation is between "box branching + listed relaxations, no cuts" and
   "binary branching + CG cuts + bound tightening". The sentence "The
   separation is between two solution methods for the same problem" is
   right but too brief.

### 9. A piece can be tagged concave when it is not, and then the answer is wrong — should-fix

`_curvature_pieces` finds sign changes of `f''` on a 400-point grid and
confirms concavity on 21 sample points. A convex region narrower than a grid
cell and away from the samples is missed. Example (script below):
`f(x) = -x^2/2000 - 0.01 exp(-((x-0.49)/2e-4)^2)` on `[0,1]` gets one piece
tagged concave. For `n = 2`, `x_1 + x_2 = 0.98`, the original optimum is
`-0.02024` at `(0.49, 0.49)`; the reformulation returns `-0.00048` at
`(0.98, 0)` with status optimal (Gurobi and SCIP).

This is adversarial and does not affect the stored families (quadratics,
powers, logistic curves, quartics are tagged correctly; I checked one of
each, including a convex kink between two concave pieces). But the module
docstring says "certified-by-sampling" and that the margin ensures
root-finding error "cannot leak" non-concave points. Neither is a
certificate. The note's limitation bullet is closer to the truth but should
say plainly that concave tags are unverified heuristics.

Related defect: a linear `f` gets 400 pieces, 399 tagged concave (every grid
value of `f''` is exactly `0`, so every grid point becomes a "root"). The
result is valid but creates about 1 200 binaries for one linear term. A
constant `f` also breaks the Gurobi backend's degree `<= 2` branch (the
coefficient tuple has two entries, three are unpacked).

Correction. Reword the docstring; treat `f'' == 0` on a whole cell as "no
root"; for the stored families, tag analytically or verify the tags with
interval arithmetic.

### 10. Theorem 1: correct; small clarifications — minor

I checked the cases asked for.

- Rank argument. At the vertex `v`, active bounds are unit rows on `N \ P`.
  After removing them, the active rows `R` of `A` restricted to the columns
  in `P` must have rank `|P|`. Hence the columns `{A_i : i in P}` are
  independent. Inactive rows play no role. The sharper statement is
  `|P| <= rank((A_R)_P) <= number of active rows`; `|P| <= rank(A_C)` follows
  because `P` is a subset of `C`, and is what the reformulation can use
  without knowing `R`. Writing the sharper form in the proof would make the
  step "must come from rows of `A`" explicit.
- Ties. If `x*_i` is a breakpoint shared by two tagged pieces, either choice
  of `I_i` works; statement 2 says "a tagged piece that contains `x*_i`",
  which is right.
- Discontinuity. A concave function on a closed interval can jump down at an
  end point. The argument uses only `phi(sum λ_k v_k) >= sum λ_k phi(v_k)`,
  so it holds. Correct as written.
- `y` fixed, boundedness. `Q` is bounded because pieces are bounded. Fine.
- The Setting should say that the bounds `l, u` are finite and that the
  breakpoints are finitely many.

Remark (b) is imprecise. With `Y = {D y <= d}` the continuous `y` have
general constraints, not bounds, so "free continuous columns of `B`" is
undefined. The correct statement: at a vertex of the joint polyhedron, the
columns of the active rows of `[A B; 0 D]` indexed by `P` and by all
continuous `y_j` that are not at a simple bound are independent. The joint
polyhedron must be pointed (no line), and one needs that a concave function
bounded below on a pointed polyhedron attains its minimum at a vertex.

Remark (c) is correct, and I could not break it, but it is under-specified.
It needs: constraints of the form `sum_i h_ki(x_i) <= 0` with each `h_ki`
concave on the same tagged pieces; an iteration (while the face containing
the point has dimension above `r`, move along a direction in the face that
is orthogonal to the `r` supergradients; concavity of `h_k` keeps the whole
segment feasible, concavity of `phi` makes one end no worse, and the face
dimension drops); and the conclusion is only the count `|P| <= rank + r`,
not independence of columns. A grid check on 200 random instances
(`n = 3`, no linear rows, one reverse-convex ball constraint) found no case
where restricting to at most one interior variable lost value.

### 11. Corollary 2: correct — minor

`A_R d = 0` with `d` supported on strictly interior variables makes `±d`
feasible directions: active rows (equalities included) stay active,
inactive rows and bounds have slack. Then `g(t) = f(x* + t d)` has a local
minimum at `t = 0` on an open interval, so `g''(0) = d'Hd >= 0`, which
contradicts negative definiteness of `H_SS`. "Negative definite `H_SS`" is
sufficient; negative definiteness on the null space of `(A_R)_S` would be
enough. Say that `R` contains all equality rows. I could not verify the
attribution to Hager et al. against the source.

### 12. Reformulation code versus the note: they agree — minor

`binarized_ir` implements the stated formulation. Checked by reading and by
experiment:

- Tagged piece: `u + t <= d` (or `<= 1` for a single piece), `s <= L t`,
  `x = lo d + L u + s`, cost `f(lo) d + (f(hi) - f(lo)) u + g(s)`.
- Untagged piece: `h = f(lo + o)`, `o <= L d`; the constant `-f(lo)` plus
  `f(lo) d` gives `f(lo + o)` when on and `0` when off. For a single
  untagged piece the two constants cancel. Correct.
- `x` is substituted into the linking rows, with the constant moved to the
  right-hand side. Correct, including `>=` rows and `B y` terms.
- Budget is `rank` of the columns of variables that have a concave piece.
  `numpy.linalg.matrix_rank` can **under**-estimate the rank of nearly
  dependent real data, which would make the budget invalid. Use
  `min(m, number of such columns)` when in doubt, or document the tolerance.
- Side variables `y` are supported but untested in `test_sob.py`. My four
  random instances (`n = 4`, two rows `==` and `>=`, one binary, one
  continuous, one integer `y`) agree between forms and solvers to `2e-6`.

Brute-force comparison (grid search on the original): quartic `n = 3, m = 1`
(6 seeds), quartic `n = 4, m = 2` (5 seeds), sigmoid `n = 3`, `m = 1, 2`
(8 seeds), with Gurobi and SCIP on both forms. All agree with the grid value
to grid accuracy and with each other to `1e-5`.
`test_sob.py`: 14 passed.

### 13. Literature and priority wording — should-fix

- The note is properly modest about the structural theorem. Keep that.
- "first proved exponential separation between spatial branch-and-bound and
  such a reformulation" should carry the qualifications of finding 8 in the
  same sentence: the lower bound is for a restricted certificate system, a
  known cut already closes the original at the root, and the upper bound
  uses integer cuts and bound tightening. Otherwise it reads as a statement
  about solvers.
- "apparently new as a solver device" is acceptable with the stated caveat.
  The reformulation is a multiple-choice/incremental piecewise model with
  one extra cardinality row; the note should name that lineage, since the
  breakpoint state is what classical piecewise-linear models have.
- The status line says an independent review is "recorded". It should state
  the outcome: corrections required.

## What I ran

All from `code/vertex_binarization`, with
`uv run --project /home/sgusev/repo/minlp-notes/code/minlp_solver_lab python ...`
unless noted. Scratch scripts were in `/tmp/sobreview` (outside the
repository). Solver runs used at most 4 threads in total and limits of at
most 100 s. BARON ran only through `solve_baron`, which works in a temporary
directory and removes it; none remained afterwards.

```
python3 summarize.py results/jeroslow.jsonl
python3 summarize.py results/pilot.jsonl
python3 summarize.py results/pilot_quartic.jsonl
... python -m pytest -q test_sob.py -p no:cacheprovider          # 14 passed
... python /tmp/sobreview/brute.py quartic 3 1 "range(0,6)" gurobi,scip
... python /tmp/sobreview/brute.py quartic 4 2 "range(0,5)" gurobi,scip
... python /tmp/sobreview/brute.py sigmoid 3 {1,2} "range(0,4)" gurobi,scip
... python /tmp/sobreview/ytest.py      # side variables y, 4 seeds
... python /tmp/sobreview/func.py       # tagging: linear, constant, bump, kink, power, sigmoid, -x^4, x^3
... python /tmp/sobreview/dip.py        # mislabelled concave piece -> wrong optimum
... python run_one.py quartic 10 3 1 sob gurobi --tl 100 --threads 2 --log
... python run_one.py quartic 10 3 1 sob gurobi --tl 60  --threads 4 --log
... python /tmp/sobreview/gstart.py     # 2-thread point as MIP start for the 4-thread run
... python /tmp/sobreview/baron_pow.py  # power-n25-m1-s1 original: **, rpower, start 0, x.lo = 1e-7
... python /tmp/sobreview/sym.py        # SCIP misc/usesymmetry 0 vs default; jeroslow_w n = 30, 400
... python /tmp/sobreview/rc.py         # grid check of remark (c)
```

`brute.py` grids the free variables of the original problem (equality rows
are solved for the remaining variables) and compares with both forms under
Gurobi and SCIP at gap `1e-6`.

## What I could not check

- The literature (no sources were read); the attribution of Corollary 2 to
  Hager et al.; the novelty claims.
- Whether the SOS lower-bound note's hypotheses admit the weighted-cost
  extension of finding 2.
- The BoxQP and explicit-`x_i` claims (no code or data).
- `results/jeroslow_w.jsonl` did not exist when I finished. The
  `jeroslow.jsonl` sweep was still being written during part of the review;
  my statements use its final content (all seven sizes, three solvers).
- Whether the BARON wrong answer originates in BARON or in the GAMS link, and
  whether the Gurobi wrong answer persists under other parameter settings
  (I tried only 2 and 4 threads).
- Project-wide tests and CI were not run or inspected, as instructed.
