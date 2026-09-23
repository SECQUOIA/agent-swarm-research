# Exact conic quadratic hull comparison

`code/minlp_solver_lab/lbesh_research/conic.py` implements an independent
comparison method for convex quadratic disjunct constraints. It uses Pyomo
expressions and Gurobi directly; it does not call LB-ESH extraction,
linearization, bound propagation, or NLP code. This comparison measures the
cost of solving the conic hull directly when that representation is available.
It is an established reformulation, not a new theoretical contribution.

## Mathematical formulation and scope

For one XOR disjunction, write the bounded continuous alternatives as

\[
 C_j=\{x:L\le x\le U,\ q_{jr}(x)\le0\ \forall r\}.
\]

The implementation introduces nonnegative indicators \(\lambda_j\), copies
\(\nu_j\), \(\sum_j\lambda_j=1\), \(x=\sum_j\nu_j\), and
\(L\lambda_j\le\nu_j\le U\lambda_j\). Every variable occurring in any
alternative of the disjunction gets a copy for every alternative, even when
it does not occur in that alternative's constraints. Variables appearing only
in global rows or the objective do not require copies. Finite declared bounds
are required only for variables that are copied. Fixed variables are substituted.

For a convex quadratic row
\(q(x)=x^TQx+a^Tx+c\le0\), \(Q\succeq0\), the row is represented by

\[
 \nu^TQ\nu\le s\lambda,\qquad
 s=-a^T\nu-c\lambda,\qquad s\ge0.
\]

For \(\lambda>0\), division by \(\lambda\) gives
\(\lambda q(\nu/\lambda)\le0\). For \(\lambda=0\), the finite scaled
bounds imply \(\nu=0\), and the equations permit \(s=0\). Thus the formulation
is the closed bounded perspective without an epsilon parameter. Each conic
inequality is convex because \(Q\) is PSD and both product factors are
nonnegative. With integral indicators the projected constraints are exactly the
original disjunction. With continuous indicators the projection is the convex
hull of the continuous bounded alternatives: positive-weight copies divide
to feasible points in their alternatives, and conversely any convex combination
lifts by multiplying its points by their weights. Empty alternatives cannot
receive positive weight.

For multiple disjunctions the formulation intersects their individual hull
relaxations and the unchanged global constraints. **It is not generally the
convex hull of the complete GDP.** Original integer variables retain integrality
in the integer solve; relaxing them gives the hull of the continuous
alternatives, not the integer hull of each alternative.

The implementation preferentially preserves explicit sums of nonnegative
weighted affine squares. For
\(q(x)=\sum_k w_k(A_kx+b_k)^2+a^Tx+c\), it introduces
\(z_k=A_k\nu+b_k\lambda\) and imposes
\(\sum_k w_kz_k^2\le s\lambda\). This prevents polynomial-expansion roundoff
from turning a rank-deficient PSD matrix into an indefinite matrix. General
expanded quadratic expressions use an exact rational PSD check on their
binary floating point coefficients, via Schur complements. No eigenvalues are
clipped and no regularization changes a row. A quadratic that fails this
conservative check is unsupported; an intended PSD expression can therefore
need explicit affine-square syntax. Constants and coefficients are otherwise
passed through ordinary floating point model construction. “Exact” refers to
the mathematical conic reformulation, not exact-arithmetic solver output.

Supported additional global expressions are nonnegative weighted sums of
explicit Euclidean norms and positive constant divided by a nonnegative
affine expression. A norm gets its standard SOC epigraph. A reciprocal
\(a/d(x)\), \(a>0\), gets \(a\le t d\), \(t,d\ge0\), and an affine
definition of \(d\). The product inequality itself forces \(d>0\), even if
its declared lower bound is zero. A zero numerator requires a strictly positive
declared lower bound to preserve the original domain. Norm/reciprocal epigraphs
are used only in convex, monotone positions. Unsupported nonquadratic
disjunct rows, nonexclusive disjunctions, nesting, reused/orphan disjuncts,
nonconvex quadratics, and missing copied-variable bounds fail explicitly.
Objectives inside disjuncts and multiple active objectives also fail explicitly.
Nonlinear equalities fail unless their two required inequalities are both
supported convex rows. Logical constraints use Pyomo's standard
`core.logical_to_linear` transform on a clone of the source model.

Gurobi documents automatic recognition of PSD quadratic constraints and rotated
second-order cones with nonnegative product factors in its
[quadratic constraint documentation](https://docs.gurobi.com/projects/optimizer/en/current/concepts/modeling/constraints.html#quadratic-constraints).
The baseline fixes `NonConvex=0` to reject accidental nonconvex models. This
implementation is independent of the custom cone transformations in the
[conic GDP reformulation literature](https://arxiv.org/abs/2508.16093).

## Interface and evidence

`conic.solve(model, time_limit=300, threads=1, mip_gap=1e-4,
abs_gap=1e-6, relax_integrality=False)` returns a JSONable result. `witness`
maps original variable names to primal values; `obj` evaluates the original
objective at that witness. `lb` is the solver-reported numerical dual bound in the original
objective sense (an upper bound for maximization). Missing dual bounds remain
missing; primal objectives are never substituted for them. The input model is
unchanged. `time` includes clone and formulation construction; `solver_runtime`
is Gurobi's reported solve time. `TimeLimit` limits optimization, not construction.
Raw solver status and numerical options are retained. Original-model witness
validation belongs to the independent benchmark harness.

On 2026-09-19, the targeted command

```
cd code/minlp_solver_lab
.venv/bin/python -m unittest lbesh_research.tests.test_conic -v
```

passed 10 tests. Analytic cases cover a shifted disk union, a fractional
perspective whose optimum is 2, a zero-weight infeasible alternative,
cross terms and a global quadratic objective, norm and reciprocal epigraphs,
decimal rank-deficient affine squares, maximization bound orientation, fixed
variables and inactive alternatives, and explicit rejection of unsupported
rows, missing bounds, and OR disjunctions. Integral solutions are checked by
evaluating original Pyomo constraints and variable bounds, separately from the
conic translation.

Fresh independent review identified two additional scope checks before the
comparison was released: a disjunct row referencing a nonfixed GDP indicator
needs special handling to preserve the tagged hull; unknown active component
types such as SOS cannot be silently ignored. The implementation now rejects
both explicitly. Indicators in the global objective and global logical
constraints remain supported. Empty component declarations impose no rows and
are accepted. The comparison does not support global exponential functions;
legacy models containing them must be reported as outside its scope.

Targeted `.venv/bin/python -` smoke solves also checked
`pyomo.circles.Circles2D3`, `pyomo.constrained_layout.CLay0203.l2`,
`pyomo.farm_layout.FLay02`, and `pyomo.farm_layout.FLay03` with one Gurobi
thread and five-second solve limits. Their original objective values were
approximately 1.17157304, 31030.37726, 37.94733262, and 48.98979546,
respectively. These were development smoke checks, not performance evidence.

The generated pilot `lbesh.quadratic.small.s104729` was also checked in both
continuous and integer modes, with one thread, a 20-second limit, relative gap
`1e-7`, and absolute gap `1e-8`. The continuous objective was 1.89737968118 with
dual bound 1.89737900426; the integral objective and dual bound were both
1.90624962339. Original-expression witness checks passed for the integral
solution. These checks verify the interface on the generated quadratic family;
they do not replace the benchmark harness or its validation.

Runtime dependencies used here are Python from the existing project `.venv`,
Pyomo 6.10.1, and gurobipy/Gurobi 13.0.3. The licensed Gurobi runtime solved all
analytic and smoke examples. No new dependency was added. Solver arithmetic
and certificates remain numerical; independent primal checks and reported gaps
are required for publication results. No project-wide verification or CI
inspection was performed for this module.
