# Independent LB-ESH solver review, 2026-09-19

The reviewed solver is suitable for the scoped numerical experiments after the
repairs below. I found no remaining correctness blocker in the checked flat,
bounded, smooth convex XOR-GDP scope. This is a targeted independent code
review and regression exercise, not a proof of the implementation, an exact
certificate, or a verdict on publication novelty or experimental breadth.

The reviewer did not author changes to `solver.py`, `master.py`, `structure.py`,
or `nlfunc.py`. I read those modules and the author's publication-contract
tests, constructed separate adversarial examples, reported failures to the
implementation author, and reran checks after correction. My independent
tests are in
`code/minlp_solver_lab/lbesh/tests/test_independent_solver_review.py`.

## Findings resolved during review

1. **Reduced NLP initialization changed fixed original values.** For
   `min x + f`, `f.fix(1)`, and `x >= 1` XOR `x >= 3`, a supplied NLP seed with
   `x=1, f=2` changed the original fixed value to 2. With a stubbed successful
   NLP return, the validator accepted objective 3, even though extracted
   constants still described `f=1`. The author now preserves fixed variables
   during initialization and normalizes accepted tolerance-sized fixed-value
   deviations before validation. The independent regression passes.

2. **Indicator references could invalidate the exact individual hull claim.**
   Let `x` lie in `[0,2]`; choose `d0: x >= 1` or
   `d1: x >= 1-y0`, with XOR indicators `y0,y1`. Both branches imply `x>=1`.
   The former relaxed hull master attained 0.5 by assigning both indicators
   weight 0.5 and allocating the copy of `y0` to branch 1. This was a weaker
   relaxation, although the integer solutions remained correct. The author
   chose the simple, explicit scope restriction: nonfixed GDP indicators
   inside disjunct constraint bodies are refused, including own-indicator
   references. Global logic on indicators remains supported. Independent
   own- and cross-indicator refusal checks pass.

3. **Time accounting needed qualification and enforcement.** The original
   construction/NLP path did not consistently pass remaining time to solvers,
   and single-tree optimization forced an extra second after exhaustion.
   The repaired zero-budget single-tree test returns `time_limit` with no
   callbacks or reduced NLP solves. The author passes remaining time to
   OBBT/Gurobi and a remaining CPU-time limit to default Ipopt. This is not
   hard wall-clock process preemption; other NLP plugins lack a portable
   generic timeout. The implementation note states that limitation.

## Independent checks

The 13 independent test methods cover:

- The previously reported big-M single-tree failure with reduced NLPs disabled:
  the known objective 1 is now returned with `optimal` numerical status.
- Fixed Boolean branch selection in all four formulation/tree combinations,
  deactivated branches, and global logical selection.
- Preservation of original fixed variables during reduced NLP initialization.
- Explicit refusal of unsupported own/cross-indicator rows, nested or repeated
  disjunct membership, and big-M rows lacking a required finite bound.
- ESH and ECP tangent validity at independently known feasible points for
  `exp(-x) <= exp(-1)`, with positive separation at `x=0`.
- Actual Ipopt reduced NLP solves for the exponential branches `x>=1` and
  `x>=3`, represented nonlinearly, in all four formulation/tree combinations.
  All return the analytic optimum 1 within `1e-4` and a checked selected-row
  residual at most `1e-6`.
- Zero-budget handling, original-sense LP-bound reporting for maximization,
  and a positive weighted perspective residual at lambda `1e-8`, below the
  current separation cutoff.
- Amplified-coefficient binary projection: a raw binary value `1-5e-7` in
  `x = 1e9*(1-y0)` satisfies the raw row at approximately `x=500`, but rounding
  makes that point violate the row by approximately 500. The solver rejects
  it. With `x=0`, the projected point is valid, and the stored incumbent,
  recomputed objective, reported objective, and final model writeback all use
  the same exact projected binary values. The original supplied dictionary
  remains unchanged.

I also reran the author's 12 test methods, including their eight real-Ipopt
nonquadratic ESH/ECP cases, callback exception injection, finite-cut checks,
recomputed nonlinear maximization objectives, primal rejection tests, gap
requirements, constant infeasible branches, and bound-propagation regressions.

Final targeted commands, from `code/minlp_solver_lab`:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
PATH=/home/sgusev/miniconda3/envs/solvers/bin:$PATH \
.venv/bin/python -m unittest discover -s lbesh/tests \
  -p test_independent_solver_review.py -v

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
PATH=/home/sgusev/miniconda3/envs/solvers/bin:$PATH \
.venv/bin/python -m unittest discover -s lbesh/tests \
  -p test_publication_contracts.py -v
```

The independent command passed all 13 methods and the author command passed
all 12 methods, with no skips (25 methods total). They
used one solver thread and the existing project environment. Gurobi's
available academic license worked. The independent suite finished in about
0.7 seconds on its final run; the author's suite finished in about 1.1 seconds. An earlier
invocation without the solver path skipped the author's Ipopt method; that
invocation is not the final verification. A transient failure of the original
own-indicator acceptance test reflected the intentional new refusal contract;
the test was updated to verify the narrowed contract explicitly.

From the repository root, `git diff --check -- code/minlp_solver_lab/lbesh`
also passed. No project-wide verification, CI inspection, broad benchmark,
or certification run was performed for this review. Reproduction versions
are recorded in `notes/lbesh-development-implementation.md` and the research
environment manifest.

The binary-projection test was added in a focused follow-up after a separate
review found raw-witness mutation in the experiment harness. That harness
issue does not reproduce in LB-ESH's internal validator: it constructs an
explicit projected `clean` dictionary, checks every relevant row after
projection, reevaluates the objective there, and stores that dictionary as the
incumbent. No solver-module change was needed for this follow-up.

## Limits that must remain visible

Convexity, differentiability, and usable nonlinear expression domains remain
input assumptions. Floating-point propagation, tangents, master bounds, and
primal tests do not establish rigorous interval bounds. `optimal` means an
accepted numerical incumbent and finite master bound meet the documented
objective-gap tolerance; `rigorous_certificate` is false. A feasible NLP
termination code alone is not accepted as a primal certificate.

The LP lambda cutoff is still heuristic. The new residual diagnostic includes
positive weights below that cutoff, but a no-cut or stalled LP exit does not
certify nonlinear perspective feasibility. Callback evaluation failures stop
the solve with a numerical error; failures outside callbacks can raise. These
behaviors are appropriate for failing closed and must not be silently counted
as successful experiment records.
