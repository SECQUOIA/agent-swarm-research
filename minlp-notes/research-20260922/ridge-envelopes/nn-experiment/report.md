# Neural-network global optimization with box-aware ridge cuts

Date: 2026-09-22/23. Author: experiment agent; written by the coordinator from
the agent's summary (the agent's harness blocked Markdown writes). Aggregate
tables: `results/summary_tables.md`; raw results as JSON/CSV in `results/`.

## Question

Do the cuts of [Theorem 1](../theory.md) (exact convex and concave envelopes of
`sigma(a^T y + b)` over the box of the previous layer's outputs) strengthen
relaxations and speed up global optimization over trained networks with
smooth activations, compared with the standard factorable relaxation (an
auxiliary pre-activation variable with interval bounds and the one-dimensional
envelope of `sigma`)?

## Setup

- 40 networks: 5 activations (tanh, sigmoid, SiLU, GELU, sin) × 8 architectures
  (input dimension 2, 3, 5; one to three hidden layers of width 8–32), trained
  in numpy with fixed seeds on standard test functions. Each network is
  minimized and maximized over its input box: 80 problems. A multistart local
  search value agreed with the best known value on all 80.
- R0: standard relaxation with iterative tangent cuts of the 1-D envelopes over
  neuron bounds from interval bound propagation (IBP) or OBBT. R1: R0 plus
  Theorem 1 cuts on each neuron as a function of the previous layer's outputs,
  both sides, separated at the LP point.
- Cut validity: every cut is repaired as required by the proof review (segment
  lines certified against `sigma` with analytic second-derivative bounds and
  shifted down; `psi` = minimum of the lines; cut uses `psi` at the nodes), with a
  1e-9 safety margin. Not an interval-arithmetic library.
- Global solve: a Python spatial branch and bound over the input box, 600 s CPU
  per run. SCIP 10 and Gurobi 13 on the same models as context (no GELU: neither
  offers `erf`). Times are process CPU times because other jobs shared the
  machine; Gurobi's limit is wall clock.

## Validity checks

- Against the verified envelope code (400 cases): the cut value never exceeds
  the verified value and is at most 1.0e-7 below it.
- All 40,805 root cuts evaluated at random points, random vertices and all
  vertices (n ≤ 10): the largest `cut - f` is -1.0e-9 (the safety margin). On
  average 78% of the sample points of a multi-dimensional cut lie outside the
  staircase simplex of its separation point, so validity was checked well away
  from the separation point.
- No lower bound from the Python B&B, SCIP or Gurobi exceeds a known feasible
  value; the optimal values agree. No safe-bound correction was applied to
  Gurobi LP optima.

## Results

Root gap closed, `(R1 - R0)/(best - R0)`:

| bounds | median | mean | max | problems >10% |
|---|---|---|---|---|
| IBP | 3.6% | 10.2% | 46% | 30 of 80 |
| OBBT | 2.2% | 3.7% | 21% | 8 of 80 |

- By activation (IBP, median): SiLU 20.3%, GELU 21.6%, sigmoid 4.3%, sin 0.7%,
  tanh 0.6%. The gain grows with depth (IBP median 0.8% with one hidden layer,
  4.3% with two, 13.5% with three).
- Single-hidden-layer networks gain little (median 0.8%), because the first
  layer's inputs are the original box coordinates and the relevant envelopes
  depend on few coordinates.
- Both relaxations are weak: the median R0 gap is 2.9 times the absolute best value.
- R1 with IBP bounds beats R0 with OBBT bounds on 24 of 80 problems.

Global solve (600 s CPU):

- R0 closed 59 of 80 runs, R1 closed 53; R1 closed none that R0 left open.
- On the 53 runs both closed, R1 used fewer nodes in all 53 (median ratio 0.68)
  but was slower in 47 (median time ratio 1.55). Over all 80 runs per
  relaxation, the unweighted mean of the per-run ratio `t_sep/time` is 91% (R0)
  and 98% (R1), and the unweighted mean of per-run `time/nodes` is 0.087 s (R0)
  and 0.31 s (R1); total CPU time divided by total nodes is 0.1034 s (R0) and
  0.3543 s (R1). Here `time` is the reported process CPU time of the run and
  `t_sep` the summed separation time. These shares are not reliable fractions
  of total CPU time: in 23 of the 160 saved records `t_sep` exceeds `time`
  (ratio up to 1.42449), which the nested `time.process_time()` intervals of
  the committed `bnb.py` and `relax.py` cannot produce; the saved data do not
  show which clock or code version caused this. Within the relaxation loop,
  where `t_sep` and `t_lp` are timed by the same clock in `relax.py`,
  separation takes on average 96% (R0) and 98% (R1) of the timed
  separation-plus-LP time, so it remains the dominant cost.
- At equal node counts, R1 had the smaller gap in 25 of the 27 runs not closed
  by both, never the larger. At the time limit R1 had the larger gap in all 21
  runs open in both, because it processed fewer nodes.
- Break-even would need R1 separation at about 1.5 times the cost of an R0 node
  instead of about 3 times.

Context: Gurobi 13 closed 53 of the 64 non-GELU runs (typical time 5.5 s), SCIP
10 closed 35 (24 s), and the Python B&B closed 48 with R0 and 44 with R1 on
the same runs.

## Assessment

Theorem 1 cuts are valid and give tighter bounds per node in almost all
comparisons (R1's root bound is at least R0's in 158 of 160 saved root
comparisons; for `sigmoid_d2_16_ackley` minimization, with both IBP and OBBT
bounds, R1 is lower by 1.46e-6, -2.212798522547568 against -2.21279706136749,
so R1 does not dominate R0 numerically in every case), with
the largest effect on non-monotone activations (SiLU, GELU) in deeper
networks. That is exactly the class that earlier closed forms do not cover.
In this implementation the per-node separation cost outweighs the node
savings, and commercial solvers already solve most of these small problems
quickly. The practical case therefore rests on a much cheaper separation
(for example, closed-form or warm-started solutions of (D), or separating
only at the root and at a few nodes), and on larger networks or embedded
models where bound strength matters more. This is recorded as a modest
positive result on bound strength and a negative result on solve time.

## Before publication: rerun the timing experiment

The node counts, closed-run counts and root-gap results above are sound. The
branch-and-bound timings are not clean enough for a paper: in 23 of the 160
saved records the separation time `t_sep` exceeds the total time `time`
(see Global solve). Before these timings are used in a paper:

1. Make `bnb.py` and `relax.py` report all times from one clock, and assert
   `t_sep + t_lp <= time` for each run.
2. Rerun the 160 branch-and-bound runs (40 networks, both senses, R0 and R1,
   600 s CPU limit). This takes about 10 CPU-hours. Run at most about four
   at once, one thread each, with no other load on the machine, so that the
   timings stay comparable.
3. Regenerate `results/summary_tables.md` and update the Global solve
   section, the break-even estimate and the summary in
   [`../../README.md`](../../README.md).

This rerun was deliberately deferred on 2026-09-25 (audit row m29 in
[`notes/audit-20260924-repository-issues.md`](../../../notes/audit-20260924-repository-issues.md)),
because no paper uses these results yet.

## Caveats

scipy 1.18.1 was installed into the `exact-quadratic-hull` environment (needed
by gurobipy's matrix API). A first B&B launch was stopped after 4 minutes
because of machine contention and its results were discarded.
