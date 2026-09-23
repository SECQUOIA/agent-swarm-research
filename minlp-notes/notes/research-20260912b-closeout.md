# Closeout of the 2026-09-12 evening continuation (solver algorithms and certificates)

**GDP update, 2026-09-19:** Sections 2 and 5.1 are historical. The
[LB-ESH development record](lbesh-development-log.md) documents further
correctness repairs, primary-source positioning, fresh independent reviews,
and a new witness-validating benchmark protocol. The old benchmark records
do not independently validate original GDP feasibility, and their original
scorer used an incorrect one-sided objective comparison. Their table is not
current validated performance evidence.

**Certification update, 2026-09-13:** the certified-MINLP claims and counts below are historical. A later audit reproduced false-bound acceptance and inconsistent expression semantics. The corrected implementation, complete proof replay, new experiments, and current claim boundaries are recorded in [the repair and replay note](certified-minlp-repair-and-replay.md). The GDP and HENS sections retain their separate scope.

Status: finished on 2026-09-13 at the user's request to complete and verify
the current ideas without starting new ones. "Independently reviewed" means a
separate research agent audited proofs and code; it is not journal peer
review. Every novelty statement rests on unsuccessful literature searches and
is qualified accordingly.

This continuation moved the repository from complexity theory towards
implemented methods with solver comparisons. Four pieces of work were
completed; their evidence, limits and verification are collected here. The
[research log](research-20260912b-log.md) preserves the chronology, including
the direction scouting reports.

## 1. Machine-checkable lower-bound certificates for convex MINLP

Method: [certified-bounds-20260912-method.md](certified-bounds-20260912-method.md).
Code: `code/minlp_solver_lab/certify/` (convexity certifier, safe rational
cuts, rational master writer, independent checker, SCIP-exact/VIPR runner,
re-check and summary scripts). Review:
[review-20260912-certified-bounds.md](review-20260912-certified-bounds.md)
(six blocking findings, all fixed; the reviewer's 36 adversarial tests pass).

What is established:

- A certificate format for a rational lower bound of a convex MINLP: exact
  convexity derivation of every nonlinear row, a rational box, a lemma file
  of safe rational cuts (linearization point clipped into the box, slopes
  rounded on the safe side, intercept a rigorous 200-bit interval bound
  rounded down), a rational master MILP, and a VIPR proof of the master's
  bound from SCIP 10 in exact mode.
- A soundness theorem (safe-cut lemma plus VIPR semantics) and an
  independent checker that re-derives convexity and bounds, re-verifies
  every cut with the given slopes, regenerates the master byte-for-byte,
  compares the VIPR problem section with the master up to positive row
  scaling, and requires the exact `viprchk` verdict.
- Tool findings recorded for reuse: `viprchk` compares GMP rationals
  without canonicalizing, so SCIP's `-5/10` style output must be rewritten
  in lowest terms; SCIP 10's certificates with cutting planes, presolving or
  propagation sometimes fail verification (a "safe" configuration without
  them is used as fallback); SCIP scales some input rows, which is why the
  checker compares rows up to positive scaling; dropping the SOL section is
  unsound because `{sol}` derivations then compare against a default value.

Results: see the table in section 5 (filled from the completed run of the
289 MINLPLib convex discrete instances whose convexity the rule set
certifies; 7 of the 299 fail to load for Python recursion reasons and 3 are
not certified convex).

## 2. Logic-based extended supporting hyperplane algorithm for convex GDP

Method and proofs: [lbesh-20260912-method.md](lbesh-20260912-method.md).
Code: `code/minlp_solver_lab/lbesh/` (hull and big-M masters in Gurobi,
multi-tree and single-tree variants, bound propagation, reduced NLPs).
Review: [review-20260912-lbesh.md](review-20260912-lbesh.md) (three
blocking defects and several should-fix items, all fixed).

What is established: validity of the master bound with exact affine
transformation of disjunct cuts (no ε-perspective), finite ε-convergence
under stated hypotheses, and a benchmark against GDPopt (LOA, LBB), MindtPy
(OA, ECP, LP/NLP-B&B) and six GAMS solvers on big-M and hull MINLPs over the
27 bounded convex GDP instances of the catalog
([gdp-instance-catalog-20260912.md](gdp-instance-catalog-20260912.md)),
120 s per run, 4 threads. Numbers are in section 5.

## 3. HENS: MINLPLib `heatexch_gen*` are ill-posed; the homogeneity lift does not help

Note: [hens-20260912-singularity-and-lift.md](hens-20260912-singularity-and-lift.md).
The guarded LMTD `(d1-d2)/log(d1/(d2+1e-6))` is unbounded above on the
feasible region of `heatexch_gen1/2/3`, so every process-exchanger area can
be driven to zero: explicit feasible points of `heatexch_gen1` with objective
`108999.78` (verified at 50 digits by the agent and re-derived independently
by the coordinator, section 8 of the note) lie far below the recorded primal
bound `154895.93`, and the infimum, bracketed in `[100500, 108846.94]`, is
not attained. The recorded 30 % gap is an artifact of the guard. On the
well-posed Yee–Grossmann example, the proposed lift `A·LMTD(dt) =
LMTD(A dt)` weakens the relaxation (root bound 49,214 versus 60,164) and is
recorded as a negative result.

## 4. Smaller findings

- LD-SDA and discrete convexity: a convex MINLP with two ordered integer
  variables whose ∞-neighbourhood local optimum is not global
  (`v(k) = (2k1-k2)^2 + |k|^2/100`, local minimum at `(1,2)`), answering the
  direction named in the LD-SDA paper's future work negatively for plain
  joint convexity ([log](research-20260912b-log.md)).
- Baseline of seven GAMS solvers on the 299 convex MINLPLib instances at
  60 s (`code/minlp_solver_lab/baseline/`): DICOPT returns "optimal" values
  far above the consensus on several instances (its stopping rule), SBB
  returns local values below the consensus (5075 on `clay0204m` against
  6545; 5370 on the GDP `CLay0204.l1`), and the certified bounds of section
  1 contradict such claims exactly.
- Pyomo tooling defects met on the way: GDPopt LBB crashes on
  `_get_final_results_object`; MindtPy ECP fails with `round(None)` on some
  instances; the GAMS plugin evaluates constraint bodies at the initial
  point and raises on `1/x` with `x = 0` (worked around by interior starting
  values); MINLPLib Pyomo files contain a stray indentation (`batch.py`) and
  deep recursion (`pedigree_*`).

## 5. Final numbers

### 5.1 Convex GDP comparison (27 instances, 120 s, 4 threads per run)

Instances: the 28 convex GDPs of the catalog minus `pyomo.batch_processing`
(111 variables without bounds inside disjunctions, which neither hull nor
big-M masters admit). "Solved" means an `optimal` status whose objective is
within `1e-4` of the consensus value (smallest value reproduced by at least
three methods) and, for methods that report a bound, a closed gap; GAMS
solvers that stopped before the time limit are accepted on their status
(their bound as read through Pyomo is unreliable, e.g. SHOT reports a root
bound). "Wrong" counts `optimal` claims above the consensus (DICOPT's
stopping rule) or below it (SBB's local solutions). Times are means over
solved instances and shifted geometric means (shift 10 s). Full table:
`code/minlp_solver_lab/results/gdp_final_summary.txt`; raw records
`results/gdp_final.jsonl`.

| method | solved | wrong | harness/tool errors | mean s | sh. geo. mean s |
|---|---:|---:|---:|---:|---:|
| LB-ESH hull single-tree | 25 | 0 | 0 | 5.5 | 3.5 |
| LB-ESH big-M single-tree | 25 | 0 | 0 | 4.7 | 3.2 |
| LB-ESH hull multi-tree | 24 | 0 | 0 | 7.1 | 4.4 |
| LB-ESH big-M multi-tree | 24 | 0 | 0 | 4.1 | 3.2 |
| GDPopt LOA (Ipopt/Gurobi) | 12 | 0 | 8 | 16.8 | 7.6 |
| GDPopt LBB (BARON) | 14 | 0 | 13 | 24.3 | 14.2 |
| MindtPy OA big-M / hull | 14 / 13 | 0 | 6 / 6 | 3.0 / 4.4 | 2.8 / 3.8 |
| MindtPy ECP big-M | 20 | 0 | 4 | 3.8 | 3.4 |
| MindtPy LP/NLP-B&B big-M | 18 | 0 | 6 | 4.2 | 3.4 |
| SHOT big-M / hull (GAMS) | 25 / 25 | 0 | 0 | 1.7 / 12.4 | 1.6 / 7.6 |
| BARON big-M / hull | 25 / 24 | 0 / 1 | 0 | 6.9 / 10.2 | 4.1 / 5.4 |
| Gurobi 13 big-M / hull | 26 / 26 | 0 | 0 | 5.8 / 10.7 | 3.3 / 5.9 |
| SCIP big-M / hull | 26 / 24 | 0 | 0 | 11.7 / 10.1 | 5.5 / 6.2 |
| DICOPT big-M / hull | 13 / 13 | 8 / 9 | 0 | 2.6 / 2.6 | 1.9 / 2.0 |
| SBB big-M / hull | 16 / 16 | 2 / 1 | 0 | 1.6 / 2.7 | 1.6 / 2.5 |

Reading: the LB-ESH prototype (Python, Gurobi master, Ipopt subproblems)
solves as many instances as BARON and SHOT and one fewer than Gurobi's and
SCIP's native MINLP on the big-M reformulation, with no wrong claims, and
clearly more than the existing Pyomo decomposition tools (GDPopt, MindtPy)
whose failures are partly tool errors (GDPopt LBB `_get_final_results_object`,
MindtPy `round(None)`, Ipopt exits on the `l2` layouts). SHOT on big-M is
the fastest; LB-ESH's per-instance times are within a factor of two to
three of it on the solved set. The unsolved instances for LB-ESH are
`gdplib.batch_processing` (hard master MILP; BARON needs 37 s, SHOT 6 s)
and `FLay06` (unsolved by every method within 120 s except DICOPT's
unverified claim). This is a competitive prototype, not a demonstrated
improvement over the best solvers; the exact-perspective advantage did not
translate into wins on this set, whose hull relaxations are handled well by
the MINLP solvers.

### 5.2 Certified lower bounds on the MINLPLib convex set

Run: `certify/run_all.py` over the 289 certified-convex instances, OA
(LB-ESH multi-tree) limited to 60 s, exact SCIP limited to 180 s for the
first 129 instances and 90 s for the rest (throughput), then `viprcomp`,
canonicalization, `viprchk`, and the independent checker; 4 to 10 workers.
Raw records `results/cert_all.jsonl`, summary `results/cert_all_summary.txt`,
artifacts (`master.lp`, `lemma.json`, `master_complete.vipr`, logs) under
`results/cert/<instance>/` (not committed; regenerable).

| quantity | count |
|---|---:|
| instances attempted (certified convex by the rule set) | 289 |
| fully verified certificates (`viprchk` verdict and independent checker) | 269 |
| of which exact SCIP solved the master to optimality / was interrupted at the limit | 152 / 117 |
| of which the certificate needed the "safe" SCIP configuration | 176 |
| not verified: `viprchk` failure in both SCIP configurations | 6 |
| not verified: pipeline crash or kill (OA or exact SCIP over the wall-clock cap) | 14 |
| certified bound within `1e-6` / `1e-4` / `1e-2` (relative) of MINLPLib's recorded primal bound | 115 / 127 / 159 |
| certified bound above MINLPLib's recorded primal bound (would indicate an error) | 0 |
| median / maximum wall time per verified instance | 152 s / 850 s |

Historical comparison: 127 accepted lower bounds were within `1e-4` relative of recorded MINLPLib primal values. Those reference values were not independently verified feasible witnesses, so this did not establish 127 optimality certificates. Larger recorded gaps reflected the particular relaxation and search budgets; they did not establish a limitation of certification in principle.

The old seven-solver comparison reported 35 discrepancies. That aggregate used historical certificate verdicts and is not a current solver-error count. The later [case-by-case audit](certified-minlp-solver-discrepancies.md) independently verifies that SBB's `clay0204m` returned point violates two constraints and that SHOT's `risk2bpb` point violates two fixed binary bounds. SBB's recorded status was Integer Solution, not Optimal. The audit also documents source-model equivalence and the distinction between an invalid returned point and attribution to an upstream solver implementation.

The historical run checked neither nonlinear primal feasibility nor the complete software soundness contract subsequently required. Its trusted base included the old `viprchk` and inconsistent extraction paths. The [repair and replay record](certified-minlp-repair-and-replay.md) replaces those certification claims and reports outcomes under the corrected checker, including conservative exclusions and resource limits.
