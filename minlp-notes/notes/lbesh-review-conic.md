# Independent review of the quadratic conic baseline

Review date: 2026-09-19. This review was performed by a fresh agent that did
not implement `lbesh_research/conic.py`. Scope was the implementation, its
10 author tests, and `notes/lbesh-development-conic.md`. The reviewer added
11 analytic and refusal regressions in
`code/minlp_solver_lab/lbesh_research/tests/test_independent_conic.py`.

The reviewed baseline is suitable for controlled numerical comparisons within
its stated domain after the repairs below. This is a review verdict, not a
formal proof of the Python implementation or a guarantee of solver accuracy.
The conic reformulation is exact as a mathematical statement; objectives,
primal witnesses, solver-reported bounds, and termination statuses use floating
point arithmetic and require the separate experiment harness's validation.

## Defects found and repaired

1. **Disjunct indicators in disjunct rows broke the claimed continuous hull.**
   The original implementation disaggregated these indicators as ordinary
   variables, without requiring their branch copies to agree with the selected
   alternative. For `d0: x >= y0`, `d1: x >= 2*y1`, `0 <= x <= 3`, the
   alternatives require `x >= 1` and `x >= 2`. At weights `(0.5, 0.5)` their
   hull requires `x >= 1.5`. The implementation returned zero. The author
   repaired this by explicitly rejecting active disjunct-indicator references
   in disjunct rows, a conservative scope restriction. The regression verifies
   rejection. Global indicator constraints and objective terms remain allowed.
2. **Active SOS constraints were silently omitted.** For two `[0,1]` variables,
   an SOS1 constraint and a maximization of their sum, the implementation
   returned two although the true optimum is one. The author added an active
   component type whitelist; SOS and other unsupported component types now
   cause `UnsupportedConic`. The independent SOS regression passes.
3. **Active objectives inside disjuncts were silently omitted.** A model with
   a global objective and an additional objective inside a disjunct returned
   `optimal`. Objective enumeration now traverses disjuncts, requires exactly
   one active objective, and rejects a disjunct ancestor. The regression passes.

All three failures were reproduced before repair. The independent reviewer
reported them to the author and parent agent; the author changed the module,
and the reviewer reran the targeted tests after those changes.

## Mathematical and numerical checks

For bounded alternatives, scaled variable bounds force every disaggregated
copy to zero at zero weight. For positive weight, dividing the perspective
quadratic row by that weight recovers the original row at the divided copy.
These observations establish both directions of the individual-disjunction
convex-hull formulation in exact arithmetic, including empty alternatives.
The implementation correctly retains constants inside affine squares as
`A*nu + b*lambda`, rather than `A*nu + b`. A fractional shifted-interval test
has analytically known optimum `-2`; a separate fractional quadratic test
from the author has optimum `2`.

Expanded quadratic coefficients are checked using rational Schur complements
of the actual stored binary floating point coefficients. This is conservative
and does not clip a small negative eigenvalue. The independent tests reject
a matrix whose off-diagonal term makes it indefinite by approximately
`1e-12`. Explicit nonnegative affine squares preserve their PSD structure
without expanding those squares first. Model construction and subsequent
optimization still use floating point arithmetic.

Global norm epigraphs have a nonnegative radius. Reciprocal epigraphs have
nonnegative factors; a positive numerator forces a strictly positive
denominator. They are used in monotone upper constraints or minimized convex
expressions. Lower bounds on convex quadratics and reciprocals with a declared
domain crossing zero are refused. Some algebraically admissible expression
syntax is also conservatively refused: maximization of `-1/(x+1)` currently
produces an unsupported double-negation expression. This limits scope, without
silently changing a model.

The tests check maximization bound orientation, the absence of a witness after
infeasibility, an empty quadratic branch at zero weight, original Pyomo
expression evaluation at an integer witness, and a rank-deficient expanded
quadratic with a cross term. The author tests additionally check that the
source model is unchanged, fixed variables and inactive disjuncts, explicit
norm and reciprocal optimal values, missing bounds, and nonexclusive
alternatives. Multiple individual hulls intersected with global constraints
are not claimed to give the complete GDP convex hull.

## Verification record

The final targeted command, from `code/minlp_solver_lab`, was:

```
.venv/bin/python -m unittest lbesh_research.tests.test_conic lbesh_research.tests.test_independent_conic -v
```

All 21 tests passed in approximately 0.3 seconds. Independent solver calls used
one thread and a 15-second limit per instance; every case finished promptly.
Development reproductions used `.venv/bin/python -` for the three defects
above. The Gurobi runtime reported version 13.0.3 and successfully solved these
small licensed instances. No broad benchmark, project-wide verification, or CI
status/log inspection was performed during this review. The evidence supports
using this baseline for numerical experiments, not a runtime superiority claim
or a mathematical certificate from solver output.
