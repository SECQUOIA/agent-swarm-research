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
  but was slower in 47 (median time ratio 1.55). Separation takes 91% (R0) and
  98% (R1) of node time; a node costs 0.087 s with R0 and 0.31 s with R1.
- At equal node counts, R1 had the smaller gap in 25 of the 27 runs not closed
  by both, never the larger. At the time limit R1 had the larger gap in all 21
  runs open in both, because it processed fewer nodes.
- Break-even would need R1 separation at about 1.5 times the cost of an R0 node
  instead of about 3 times.

Context: Gurobi 13 closed 53 of the 64 non-GELU runs (typical time 5.5 s), SCIP
10 closed 35 (24 s), and the Python B&B closed 48 with R0 and 44 with R1 on
the same runs.

## Assessment

Theorem 1 cuts are valid and give consistently tighter bounds per node, with
the largest effect on non-monotone activations (SiLU, GELU) in deeper
networks. That is exactly the class that earlier closed forms do not cover.
In this implementation the per-node separation cost outweighs the node
savings, and commercial solvers already solve most of these small problems
quickly. The practical case therefore rests on a much cheaper separation
(for example, closed-form or warm-started solutions of (D), or separating
only at the root and at a few nodes), and on larger networks or embedded
models where bound strength matters more. This is recorded as a modest
positive result on bound strength and a negative result on solve time.

## Caveats

scipy 1.18.1 was installed into the `exact-quadratic-hull` environment (needed
by gurobipy's matrix API). A first B&B launch was stopped after 4 minutes
because of machine contention and its results were discarded.
