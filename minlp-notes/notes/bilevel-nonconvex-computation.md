# Computation for the nonconvex scalar tariff specialization

Date: 2026-09-07. This is an independent computational check of
[the exact scalar algorithm](bilevel-nonconvex-scalar-algorithm.md), together with
small synthetic timing experiments. It implements the global nonconvex follower
step that the earlier convex tariff sweep did not cover. The experiments support
correctness and identify implementation costs; they do not establish an advantage
over a general global bilevel solver or performance on application data.

The implementation is [scalar_solver.py](../code/bilevel_nonconvex/scalar_solver.py).
The independent oracle and experiments are
[benchmarks.py](../code/bilevel_nonconvex/benchmarks.py), with
[raw results](../code/bilevel_nonconvex/benchmarks.json).

## Independent original-coordinate oracle

The oracle constructs the original Hessian
`Q = diag(d) - h*u*u.T` and enumerates the `3^n` choices of lower bound,
free variable, and upper bound. On each nonsingular free face, it solves the
original stationarity equations exactly. At a requested tariff it rejects
out-of-box candidates and compares their original objective values exactly.
It does not use the solver's fiber pieces, candidate construction, or envelope.
In particular, it never assumes that a KKT point is globally optimal.

Skipping singular free Hessians does not lose the global value. Choose a global
minimizer and its minimal box face. If its free Hessian is singular, stationarity
and positive semidefiniteness on this face imply that any nonzero null direction
preserves the objective. Follow that direction to the face boundary, obtaining a
global minimizer on a smaller face. Repetition reaches a nonsingular free face or
a vertex. This argument certifies the value oracle, not enumeration of an entire
flat minimizer set.

Eight cases cover flat follower intervals, distinct tied minimizers, a tariff
jump, signed and zero aggregate coefficients, fixed coordinates, and three
heterogeneous instances through four coordinates. Every atlas tariff point,
including quadratic irrational points, and a nine-point rational tariff grid
are queried. Every returned singleton response and every flat interval's two
endpoints and midpoint are checked against the original-space global value.
The final run passed 340 response checks at 136 tariff query entries; those
counts include repeated prices and duplicate endpoint representations. It also
checks attained optimistic and pessimistic optimizer witnesses against the
original-space oracle and the appropriate extreme revenue among its minimizers.
These finite checks supplement the independent proof reviews; they do not prove
that every response is present for every possible input.

## Exact behavior that matters for tariff design

The one-coordinate example
`f_x(z) = -z^2/2 + (x-1)*z`, `0 <= z <= 1`, `0 <= x <= 2`,
has follower response 1 below tariff `3/2`, response 0 above it, and both at the
switch. Its optimistic revenue maximum is `3/2`, attained at the switch.
Its pessimistic revenue supremum is also `3/2`, but is unattained. The solver
returns these different attainment flags explicitly.

The same distinction occurs with heterogeneous coupled followers. The two-variable
verification instance `family(2,3)` has revenue `34683/9440` and limiting tariff
`429/320`; the optimistic optimum is attained and the pessimistic supremum is not.
The three-variable instance `family(3,7)` has the exact optimal/limiting tariff

`111726/12485 - sqrt(35295210867)/24970`.

Its optimum revenue is

`-218891177/2197360 + 13627*sqrt(35295210867)/24445630`.

Again, optimistic attainment and pessimistic nonattainment differ. These are
implementation examples, not new claims that nonattainment is previously unknown.
The irrational switch makes exact algebraic output useful in this specialization.

A separate local-solver example uses `f(z)=z/4-z^2/2` on `[0,1]`. L-BFGS-B
started at 0 or 0.05 returns the nonglobal local minimum 0 with value 0;
starts at 0.5 or 1 return the global minimum 1 with value `-1/4`.
The exact result follows immediately from concavity and the endpoint values.
This illustrates why first-order KKT/local follower solutions cannot replace
global response selection here. It is not a broad comparison of local solvers.

## Repeated timings and an implementation improvement

The family uses heterogeneous positive rational diagonal costs, positive
aggregate coefficients, negative local linear costs, the unit box, and tariff
range `[0,5]`. It sets

`h * sum(u_i^2/d_i) = 7/5`.

Thus the follower Hessian is genuinely indefinite: diagonal congruence reduces
it to `I - h*v*v.T`, with one negative eigenvalue. Nonconvexity is not merely
permitted by the interface; every timing instance has it.

The first implementation inserted every pairwise branch crossing into the atlas,
including crossings above the global lower envelope. Those measurements are
retained in [benchmarks_pairwise_baseline.json](../code/bilevel_nonconvex/benchmarks_pairwise_baseline.json).
The revised implementation inserts branches into the current lower envelope and
retains contacts needed for exact isolated ties. Both runs use the same four
seed-17 instances. Entries are medians of three consecutive runs in one process;
SymPy caches and other concurrent work can affect these small timing measurements.
The baseline JSON records historical measurements before replacement of that
implementation; the current script reproduces the revised implementation.

| Variables | Fiber pieces | Old atlas points | New atlas points | Old build (s) | New build (s) | New upper optimization (s) |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 3 | 12 | 9 | 0.027 | 0.026 | 0.004 |
| 4 | 7 | 45 | 17 | 1.984 | 0.573 | 0.147 |
| 8 | 14 | 134 | 29 | 7.139 | 1.708 | 0.421 |
| 12 | 21 | 274 | 45 | 15.882 | 3.079 | 0.600 |

The exact optimum revenues agree between versions on all four instances.
A 24-variable scaling run has 38 fiber pieces and 79 atlas points, with
build median 5.427 seconds and upper optimization median 0.911 seconds.
At 48 variables, there are 66 fiber pieces and 135 atlas points; the corresponding
medians are 18.699 and 2.922 seconds. We stopped scaling here because exact
symbolic construction already takes roughly twenty seconds at this modest
number of distinct events.

Two additional eight-variable seeds give build medians 1.008 and 1.488 seconds,
and upper optimization medians 0.209 and 0.349 seconds. The raw JSON includes
all individual timings and exact revenue values.

The original-coordinate oracle is also timed at two and four variables.
At four variables, building its candidates and answering nine fixed-price
queries takes roughly 0.13 seconds in the revised run. That is a different,
smaller task than constructing the whole tariff reaction graph and optimizing
the leader over a continuous interval. It is reported as an independent
verification cost, not as a comparable competing bilevel solve. No speedup over
a general global bilevel solver is established.

## Population scaling with two coordinate types

A separate grouped family has `N=2m` coordinates: `m` copies of
`(d,c,u)=(1,-1,1)` and `m` copies of `(1,-1/2,1)`, all with bounds `[0,1]`.
It uses `h=3/(5m)`, tariff interval `[0,1]`, and upper capacity `W<=m`.
The Hessian is indefinite because `h*sum(u_i^2/d_i)=6/5`.
There are only three distinct fiber pieces and seven atlas points regardless of
population size. Thus this family tests population scaling with few coordinate
types, not growing numbers of distinct clipping events.

Within each type, strict convexity of the local quadratic makes the response
uniform at fixed type sum. Dividing the objective and aggregate by `m` reduces
this family exactly to the two-variable instance with `h=3/5`. The base-model
global responses at tariff `17/20` are `(3/8,0)` and `(1,5/8)`, both with
normalized follower value `-9/320` (population value `-9m/320`); the independent
original-space oracle verifies the base values.
Only the first satisfies capacity. The optimistic result is
`x=17/20`, `W=3m/8`, revenue `51m/160`; the pessimistic result is the same
unattained supremum. The script checks these exact formulas at every timing run.

| Variables | Build median (s) | Constrained upper optimization median (s) |
|---:|---:|---:|
| 20 | 0.080 | 0.029 |
| 200 | 0.127 | 0.267 |
| 1000 | 0.255 | 1.261 |

All medians use three runs. This is a useful positive case for a population
with a small number of response types. It does not remove the algebraic cost
seen when the number of distinct response events grows.

## Scope and reproducibility

Run from the repository root:

```sh
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/bilevel_nonconvex/benchmarks.py
```

The script needs SymPy and SciPy; the JSON records Python, SymPy, and platform
versions. Inputs are rational and timings use `time.perf_counter`.

This remains an exact prototype with limited evidence on heterogeneous instances. It addresses one scalar tariff
whose local linear perturbation is aligned with the aggregate, one concave
quadratic aggregate term, a diagonal positive local Hessian, and a box follower.
It does not implement the full fixed-dimensional theorem, arbitrary polynomial
aggregate costs, unaligned leader perturbations, or application data.
The experiments make the global nonconvex theorem more concrete, but do not yet
justify a claim of practical large-scale superiority. The retained negative
baseline shows why counting algebraic dimensions alone does not guarantee a
fast implementation.
