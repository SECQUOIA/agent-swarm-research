# Source model and domain contract

The common importer now admits the seven application models refused by the
previous experiment. It preserves original rows and variable types. Baseline
and cut modes use the same importer. The additional variables are an objective
epigraph when needed and, only when necessary, witnesses for original function
domains. Nonlinear graph atoms are not duplicated.

The exact boundary is the submitted PySCIPOpt expression DAG and the real
interpretation of its binary64 coefficients. SCIP's internal expression
simplification, presolve, feasibility tolerances, and reported primal and dual
bounds remain numerical. Model admission is not a proof of a complete solve.

## Original coefficients and expression values

`solver/model.py` interprets each loaded finite binary64 leaf as its exact
rational value. Constant arithmetic is normalized only when its exact result is
binary64 representable. For each original row, the importer compares the exact
source value expression with the expression assembled for PySCIPOpt. The test
is exact symbolic subtraction and expansion, with no numerical tolerance.

Ordinary PySCIPOpt polynomial assembly can fold coefficient products in
binary64. For example, `(0.1*x)^2` has source coefficient
`Fraction(0.1)**2`, which differs from the rounded floating product. If ordinary
assembly changes a row, the importer constructs an explicit generic DAG with
separate constant children. The generic construction performs no arithmetic
on those coefficients. The equality check then runs again and fails closed.
This also retains nonrepresentable intermediate constant arithmetic.

Polynomial row constants require care because PySCIPOpt's `ExprCons` moves
them into the row sides using floating subtraction. Such constraint rows use a
generic DAG, which retains the constant in the expression. Original ranged
rows, including both sides of an equality, are submitted together.

## Exact bounds from original affine rows

`solver/bounds.py` applies exact rational interval propagation only to original
affine constraints: rows with no quadratic entries and no nonlinear tree.
It also applies the original binary and integer variable semantics. For
`sum a_i*x_i <= b`, a finite lower activity of all terms except `j` implies

\[
a_jx_j \le b-\sum_{i\ne j}\min(a_i l_i,a_i u_i).
\]

Dividing by `a_j` gives an upper or lower bound according to its sign. Lower
row sides use the same rule after negation. Every deduction records its row,
side, variable, previous bound, and exact new bound. Replay reconstructs the
premises from the supplied original instance and recomputes every step.
Finite work budgets can stop propagation; a valid prefix remains valid.

The exact inferred box contains every original feasible point. Exported
binary64 lower bounds are rounded down and upper bounds up. The solver keeps
the declared bounds and original rows; the deductions supply source-domain
proofs and conservative compact domains for support certificates. No
numerical presolve bound enters this proof.

For a domain argument that is affine, `model.py` additionally checks original
affine rows proportional to that argument. This proves, for example, that
`log(x-y)` has a positive argument when the original equality is `x-y=1`, even
if both coordinate bounds are unbounded. This direct argument check is
recomputed from the original rows; it does not assert finite coordinate bounds.

## Original partial-function domains

Domain traversal visits every original source node before algebraic
simplification. Zero products, cancelled divisions, and zero powers do not
erase their children's domains. Extended rational intervals retain finite
one-sided information: `x>=0` establishes `1+x>=1` even when `x` has no upper
bound. Finite elementary enclosures use the validated interval kernel.

When original affine constraints and interval bounds do not establish a
domain, the importer preserves it by an exact existential constraint:

| Original requirement | Added constraint |
|---|---|
| `d != 0`, including division and negative integer powers | `d*u = 1`, with free `u` |
| `d > 0`, including logarithms and negative fractional powers | `d*u = 1`, with `u >= 0` |
| `d >= 0`, including square roots and positive fractional powers | `d >= 0` |

These have exactly the required projections. If `d != 0`, choose `u=1/d`;
conversely, `d*u=1` excludes zero. If `u>=0`, that equality implies `u>0` and
`d>0`, and every positive `d` has the required witness. This preserves strict
domains without replacing them by an arbitrary epsilon. Witnesses can be
unbounded. Their numerical treatment remains part of SCIP's numerical solve.

The domain argument itself is compiled as a generic expression and compared
with its exact source value before the guard is submitted. The original row
is still submitted as well. Guards with the same exact value argument and
domain requirement can share a witness. Every original occurrence is visited,
so this sharing cannot remove a nested source restriction.

These witnesses also preserve deliberately cancelled domains, such as
`0*log(x)`, `sqrt(x)^2`, `x/x`, and `log(x)^0`. They do not provide extra affine
bounds to cut generation. A support routine that cannot safely cover a
partial-domain expression declines that cut; the common native model remains
available to solve the instance.

A strict domain can make an infimum unattained. Neither a numerical SCIP
status nor its small positive numerical domain tolerances prove existence of
an exact feasible minimizer. If a cancelled expression has a polynomial
extension outside its source domain, support over that larger box gives valid
cuts for the original feasible set. A closeness bound for the extended graph
does not establish membership in the original partial-function graph.

## Variable exponents

The supported variable-power rule is

\[
b(x)^{e(x)}=\exp(e(x)\log b(x)),\qquad b(x)>0.
\]

The importer first proves base positivity from the original affine rows and
declared or implied bounds. It then applies this identity at that source node
only. The generic logarithm node is retained, including `log(2)` for
`2^(x+y)`; no irrational coefficient is replaced by a floating approximation.
The transformed exact expression is compared with the submitted native DAG.

An unproved positive base gives `unsupported_variable_power_domain`. In
particular, the importer does not add a positive-base guard to a general
variable power: this could remove valid zero-base points or negative-base
points with integer exponents. Such a refusal is not an infeasibility claim.
Fixed power exponents are rational and must be exactly binary64 representable
in the native power node. Broader power semantics are explicitly unsupported.

## API, checks, and remaining limits

`build_model(instance)` returns a `BuiltModel` containing the common model,
original variables, objective variable if present, exact source row
expressions, exact implied bounds, outward binary64 bounds, and binding/domain
metadata. Expected refusals raise `ModelAdmissionError` with a status and
diagnostic. The metadata includes the replayable affine-bound certificate,
generic fallback rows, domain guard identities, and variable names. Each
domain guard records the interpreted submitted DAG, submitted and stored
constraint sides, named constraint, actual witness bounds, and SCIP infinity
sentinel. Replay must derive its expected guard from the original source; the
saved description is not itself proof of the projection identity.

Targeted checks cover one-sided unbounded domains, rational implications,
original equalities and integer semantics, cancelled domains, variable powers,
constant folding, row-side rounding, constant rows, malformed operators, and
corrupted bound certificates. Historical admission checks are recorded in
`numerics/model-admission.json`. Admission is separate from benchmark solve
performance and from validation of returned original-coordinate incumbents.

Targeted owner checks completed with 51 passing tests:

```sh
PYTHONPATH=research-20261003-convexification code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261003-convexification/solver/test_model.py research-20261003-convexification/solver/test_bounds.py
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/numerics/check_model_admission.py
```

The second command rebuilds the seven historical cases without optimization;
all seven were admitted. Independent model review added 31 passing tests,
including altered domain-guard metadata. The separate bound review includes
120 comparisons with exact polygon vertices. These are topic-specific local
checks, not project-wide or CI results.

The supported grammar is finite arithmetic, fixed rational powers, the
positive-base variable-power rule above, and the existing exp/log/sqrt/sin/cos/
absolute-value operators. General power domains, numerical SCIP correctness,
and arbitrary exact global domain inference are not claimed. The cuts rely
only on proved original-model implications and certified support domains.
