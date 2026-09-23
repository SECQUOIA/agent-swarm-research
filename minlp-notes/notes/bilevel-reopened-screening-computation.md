# Exact screened recovery compared with a dense KKT MILP

Date: 2026-09-06. Status: completed independent computational comparison.

The current exact screening prototype was slower than a conventional numerical
KKT MILP on all four synthetic cases tested. It returned exact rational
solutions with verified follower KKT conditions and upper feasibility. The MILP
reported global optimality on every case. Three default-tolerance objective
values agreed with the exact result within `1.4e-15`; the remaining discrepancy
disappeared in a bounded follow-up with tighter feasibility tolerances.

This adds a modern global-solver comparison to the
[surrogate-screening result](bilevel-reopened-approximate-structure.md).
The earlier `3^N` full-enumeration counts are not used as a performance baseline.

## Reproduction and experimental scope

- [Independent comparison driver](../code/bilevel_reopened/screening_milp_comparison.py).
- [Saved results, including all solver statuses and timing components](../code/bilevel_reopened/screening_milp_comparison.json).
- [Original instance generator and exact screened implementation](../code/bilevel_reopened/approximate_structure_checks.py).

Run from the repository root:

```
python code/bilevel_reopened/screening_milp_comparison.py
```

The comparison uses the existing dense family with seed `101` and perturbation
scale `10000`, at `N=8,12,20`, plus one larger case at `N=40`. The surrogate is
the identity; the true Hessian is a symmetric dense perturbation with verified
strict diagonal dominance. The leader lies in `[0,1]`, minimizes the existing
signed affine response objective, and must satisfy the existing signed affine
response constraint. The saved file records the objective and constraint rows.

The comparison model was written by an agent independent of the screened
implementation. It reuses the input generator and calls the screened method,
but does not reuse its screening, active-pattern recovery, or interval formulas
to construct the numerical comparison. It separately verifies each exact
returned solution by direct dense matrix arithmetic.

These are uncalibrated synthetic models, single runs in a shared environment.
The recorded software versions are Python `3.13.11`, NumPy `2.5.1`, SciPy
`1.18.0`, and SymPy `1.14.0`. Timings are descriptive, without repetition,
hardware isolation, or statistical uncertainty estimates.

## Independent comparison formulation

Write `g=Qz+c+Cx`. The MILP has continuous variables `(x,z)` and two binary
variables `l_i,u_i` per follower coordinate. It imposes

```
0 <= x <= 1,  0 <= z_i <= 1,
z_i+l_i <= 1,  z_i-u_i >= 0,  l_i+u_i <= 1,
-M_i*u_i <= g_i <= M_i*l_i.
```

The exact rational row bound is

```
M_i = 1 + |c_i| + |C_i| max(|lo|,|hi|) + sum_j |Q_ij|.
```

Thus `M_i` is a valid gradient bound throughout the leader and follower boxes.
The unit slack also prevents ordinary floating conversion from rounding the
bound inward on these bounded inputs. The driver records every rational `M_i`.

If both binaries are zero, the gradient is zero. If `l_i=1`, the coordinate is
at its lower bound and its gradient is nonnegative. If `u_i=1`, the coordinate
is at its upper bound and its gradient is nonpositive. Conversely every box
KKT point admits these binaries, including degenerate zero-gradient bounds.
Positive definiteness makes these KKT conditions equivalent to unique global
follower optimality. The original affine objective and upper constraint are
then added directly. This is the conventional global KKT MILP reformulation.

SciPy calls HiGHS with a 30-second limit and requested relative MIP gap zero.
The numerical primal and dual values remain floating-point solver reports,
not rational lower/upper certificates. All statuses and discrepancies are
retained rather than dropping unfavorable or unsuccessful comparisons.

## Recorded results

The exact solver time below includes dense inversion, screening, and recovery.
The screening and recovery columns split out those two components; the small
remaining difference is inverse computation and other solver overhead. Input
generation, surrogate-cover construction, and final exact verification are
recorded separately in the JSON. MILP formulation is separate from MILP solve.

| `N` | Cells | Maximum ambiguous | Completed cell/status assignments | Exact solver seconds | Screening seconds | Recovery seconds | MILP solve seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 13 | 2 | 105 | 0.0984 | 0.0418 | 0.0549 | 0.0243 |
| 12 | 20 | 2 | 168 | 0.2962 | 0.1374 | 0.1537 | 0.0382 |
| 20 | 33 | 2 | 285 | 0.9332 | 0.4714 | 0.4500 | 0.1560 |
| 40 | 36 | 4 | 2304 | 17.5689 | 2.1285 | 15.2902 | 0.4041 |

MILP formulation took approximately `0.0011`, `0.0018`, `0.0048`, and `0.0133`
seconds, respectively. Including these times does not reverse the comparison.
The MILP reported status `0` and relative gap zero on every case; its branch
node counts were `1,1,1,21`. No time limit or solver error occurred.

Every screened solution passed exact rational checks of leader and follower
bounds, complete dense follower KKT conditions, upper constraints, and the
objective evaluation. The exact screening method's global completeness rests
on its separately reviewed theorem; checking the returned point alone would
not establish global optimality.

The larger case illustrates why the actual ambiguity distribution matters.
At `N=40`, 27 of 36 cells have four ambiguous coordinates; the other cells have
two or three. Recovery accounts for about 15.3 seconds of the 17.6-second exact
solve. The increase cannot be attributed to dimension alone: this generated
case also has different breakpoint coincidences and a larger ambiguity
parameter than the smaller cases.

## Numerical tolerance discrepancy and follow-up

For `N=8`, the exact optimal value is

```
4810519997 / 235205877942.
```

The default MILP reported a primal objective and dual bound both approximately
`3.3703e-7` below that exact value. Its returned point violated a modeled linear
constraint by approximately `3.5387e-7`, while its binaries were integral.
Consequently the driver records that the default result fails the `1e-7`
objective-agreement check. A zero reported MIP gap did not make this an exact
feasible global solution.

Only this discrepant MILP was rerun, requesting both HiGHS MIP and primal
feasibility tolerances of `1e-9`. The installed SciPy wrapper forwards these
solver-specific settings to HiGHS and issues a warning; that warning is saved.
The follow-up reported optimality in `0.0141` seconds, with objective difference
`3.82e-17` and maximum linear violation `1.11e-16`. Its timing is a follow-up
observation and is not substituted into the original timing table.

The default objective differences at `N=12,20,40` were approximately
`2.86e-16`, `1.33e-15`, and `1.11e-16`. These agreements support the independent
comparison; they do not turn HiGHS's numerical bounds into exact certificates.

## Consequence for the practical claim

These experiments support exact global recovery on dense inputs with small
certified ambiguity. They do not support a speed advantage for the current
SymPy implementation. On this family the conventional numerical MILP was
already easy, and exact screening plus rational recovery added substantial
cost. The `N=40` case makes recovery the principal implementation bottleneck.

The present value of the result is its exact guarantee and verified structural
parameter, with numerical evidence that the method works. Application-level
performance claims still require representative models, a stronger rational
linear-algebra implementation, and comparisons across perturbation sizes and
surrogate choices. None of those unperformed experiments is treated as a
completed result here.
