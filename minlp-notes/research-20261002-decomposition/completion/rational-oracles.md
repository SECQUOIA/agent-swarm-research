# Reusable rational optimization oracles

The new [rational_optimization.py](../solver/rational_optimization.py) implements
exact LP and convex box-QP backends using Python's standard library. They accept
the supplied optimization problem; neither requires a known optimal point. Every
conclusive optimization result contains a witness checked with exact rational
arithmetic before return. The independent verification functions never call an
optimizer.

This completes the missing numerical backend for affine-response recognition,
stationary recovery, and convex recourse factors. These are implementations of
classical optimization and certificate conditions, not new complexity results.
The exact simplex and active-face implementations do **not** establish
polynomial running time.

## API

All objectives are minimized. Exact coefficients may be integers, Fraction
objects, or rational strings; floats and booleans are rejected as input data.

```python
from rational_optimization import (
    solve_lp, verify_lp_result,
    solve_convex_box_qp, verify_convex_box_qp_result, is_psd, solve_nonsingular,
)

lp = solve_lp(
    c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None,
    max_pivots=10000, check=None,
)
qp = solve_convex_box_qp(
    H, c, bounds, constant=0, max_faces=10000, max_pivots=10000,
    check=None,
)
```

The LP is `min c'x` subject to `A_ub x <= b_ub`, `A_eq x = b_eq`, and
coordinate bounds. Missing bounds mean unrestricted variables. A bound endpoint
may be `None`. Bounds are compiled as inequality rows after the supplied
inequalities, in coordinate order, lower then upper when present. Contradictory
bounds produce an infeasibility certificate.

The QP is `min x'Hx/2 + c'x + constant` over a finite rational box. `H` must be
symmetric; its positive semidefiniteness is checked exactly, allowing singular
matrices. Fixed coordinates and the zero-dimensional problem are supported.

`solve_nonsingular(matrix, rhs, check=None)` also solves square rational linear
systems by exact elimination. It returns `None` for any singular coefficient
matrix, whether the right-hand side is consistent or inconsistent; rectangular
systems are rejected. Use LP feasibility for bounded singular systems.

Results expose `status`, `x`, `value`, `certificate`, `pivots`, and `reason`;
QP results also expose `faces`. Points and multipliers are tuples of Fractions.

| Backend | Conclusive statuses | Inconclusive status |
|---|---|---|
| LP | `optimal`, `infeasible`, `unbounded` | `limit` |
| Convex box-QP | `optimal`; `not_convex` means the supplied Hessian failed the exact PSD test | `limit` |

`max_pivots` caps total simplex pivots, including phase I and artificial-variable
cleanup. For QP, that cap is shared among all LPs attempted during the call.
`max_faces` caps distinct active faces. A cap is never interpreted as
infeasibility. A caller can supply `check()` to enforce its shared budget; the
callback runs at simplex iterations and pivots, QP faces, and Schur/Gaussian
elimination steps. Its exceptions propagate to the caller. These checks are
cooperative: one exact arithmetic step and the final certificate replay can
finish before the next callback. Pivot/face caps alone are not wall-time,
coefficient-bit-size, or memory limits.

## LP certificates and correctness

Write all inequalities, including bounds, as `Gx <= h`, and equalities as
`Ex = f`.

For an optimal result the certificate stores `inequality_multipliers = lambda`
and `equality_multipliers = mu`. The verifier checks

\[
Gx\le h,\quad Ex=f,\quad \lambda\ge0,\quad
c+G^T\lambda+E^T\mu=0,\quad
c^Tx=-\lambda^Th-\mu^Tf.
\]

For every feasible `z`, stationarity and `lambda >= 0` give
`c'z >= -lambda'h - mu'f`. Equality at `x` proves optimality.

For infeasibility, the same multiplier fields satisfy

\[
\lambda\ge0,\qquad G^T\lambda+E^T\mu=0,\qquad
\lambda^Th+\mu^Tf<0.
\]

A feasible point would make the left side of the weighted constraints zero and
at most a negative number, a contradiction. Thus this status has a Farkas
witness even with redundant equations or inconsistent bound pairs.

For unboundedness the result supplies a feasible point `x` and a ray `d` with

\[
Gd\le0,\qquad Ed=0,\qquad c^Td<0.
\]

Then `x+td` is feasible for every nonnegative `t` and the objective tends to
negative infinity. The stored objective is the value at the feasible ray
origin, not a finite optimal value.

The implementation splits each unrestricted variable into two nonnegative
variables, introduces slack variables, and solves phase I with artificial
variables. It uses Bland's entering and ratio-tie rules. Exact row
transformations recover dual multipliers, including after deletion of redundant
rows. At zero phase-I value, artificial basic variables are pivoted out or their
redundant zero row is removed. The second phase minimizes the original
objective. With caps removed, the finite simplex argument applies. The verifier
uses only the displayed certificate equations and inequalities, so its soundness
does not depend on pivot choices.

## Convex QP certificates and completeness

The certificate stores nonnegative lower and upper multipliers `l` and `u`.
The verifier recomputes PSD, box feasibility, the objective, and

\[
Hx+c=l-u,\qquad
l_i(x_i-a_i)=0,\qquad u_i(b_i-x_i)=0.
\]

These conditions imply, for any other feasible `z`,

\[
F(z)-F(x)
=(Hx+c)^T(z-x)+\tfrac12(z-x)^TH(z-x)\ge0.
\]

The solver first uses bounded floating-point coordinate descent to propose
active faces. These proposals supply no certificate and may be omitted; all
acceptance conditions are exact. It then enumerates remaining lower/free/upper
faces. On a face it solves free-coordinate stationarity directly when the free
Hessian is nonsingular. When singular, an exact LP finds free coordinates
satisfying stationarity, the box bounds, and the active-coordinate gradient
signs. Fixed coordinates impose no gradient-sign restriction.

A convex differentiable function on a compact box has a minimizer satisfying
these KKT conditions. The enumeration includes that minimizer's face, and the
stationarity LP on that face is feasible. Thus removing both finite caps makes
the search complete. Its worst-case face count is exponential; singular faces
can require multiple exact LPs. This implementation claim must remain separate
from the polynomial-time convex-optimization oracle used in theoretical
complexity bounds elsewhere in the report.

## Verification performed

Targeted command from the repository root:

```sh
python3 -m unittest discover -s research-20261002-decomposition/solver -p 'test_rational_optimization.py' -v
```

Result: **17 tests passed**. These cover the classical cycling example,
contradictory and redundant constraints, rational negative right-hand sides,
unrestricted unbounded problems, empty dimensions, resource caps, callback
propagation, singular convex QPs, exact boundary multipliers, iterable input
normalization, forced exhaustive fallback without numerical proposals,
malformed/tampered certificates, and 32 seeded PSD problems with independently
constructed KKT optima. The tests verify that certificate replay does not call
an optimizer.

An [independent review](rational-oracles-review.md) additionally compared 1,600
small LPs with SciPy and checked 320 PSD QPs. It found an exhausted-input-iterator
bug in QP self-verification; that defect was fixed and covered by a regression.
These are local backend checks, not project-wide or CI verification, and they do
not establish performance on large LPs or QPs.
