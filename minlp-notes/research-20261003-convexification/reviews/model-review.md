# Independent model and domain review

Status: the model, bound, and saved-metadata checks below pass. No unresolved
model-admission finding remains for the source hashes recorded below. Campaign
clearance additionally requires the separation, row, and experiment reviews.

The review covers the boundary between the original expression model and its
native SCIP representation. A valid support inequality for a different
expression or a smaller, unjustified domain is insufficient.

The checks target four contracts:

1. Original affine rows used to justify domains must be interpreted exactly
   and checked against their complete native rows before they become premises.
2. Source domain restrictions must be visited before cancellation, constant
   folding, or variable-power rewriting. A zero coefficient does not establish
   that a source logarithm or reciprocal is defined.
3. An inferred bound must follow from the original bounds and affine rows.
   Exporting a rational bound to binary64 must enlarge the certified interval.
4. The actual native expression must agree with the admitted source function
   on the certified domain, including coefficient accumulation in full rows.

## Findings and resolutions

The first proposed variable-power guard would have restricted every base to
positive values. That is not equivalent to an unrestricted source power: a
negative base with an integer exponent can be valid. Variable powers now
require independently proved positive bases. Otherwise admission reports
`unsupported_variable_power_domain`. In particular, a negative base is not
reported as proof that the original model is infeasible.

Other partial functions use exact domain witnesses where interval or affine
proofs are insufficient. For a real argument `d`, `d*u = 1` with a free `u`
projects to `d != 0`. Requiring `u >= 0` instead projects to `d > 0`. A square
root requires `d >= 0`. The source traversal records these restrictions even
inside zero products or zero powers. These are exact statements over the
reals; SCIP still evaluates numerical feasibility with its own tolerances.

Pure constant rows initially reached `addCons` as Python Boolean values.
Construction now uses constant expression objects. Feasible empty and
nonlinear constant equality rows are covered by independent solve tests.

The implementation also avoids moving a polynomial row constant to its side
through binary64 subtraction. The review checks an equality containing `0.01`
and a `0.1` side, whose exact difference is not the stored binary64 subtraction.
Its submitted generic expression keeps the original side.

## Independent checks

The command below passed **31 tests**:

```text
PYTHONPATH=research-20261003-convexification code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261003-convexification/reviews/test_model_review.py
```

The checks include:

- Exact `1/3` equality deductions and outward binary64 conversion on both
  sides; negative unbounded implications; integer rounding after propagation;
  and every prefix of a bounded deduction chain.
- An independent exact intersection enumeration for 120 deterministic
  two-dimensional polygons. Every feasible vertex remains inside the inferred
  box; no nonempty enumerated polygon is reported infeasible.
- Rejection of changed original premises, changed deductions, reordered
  dependencies, inward float bounds, and malformed certificates.
- An unbounded `x-y=1` domain proof for `log(x-y)`, canceled square-root,
  logarithm, and reciprocal domains, variable powers, and negative integer
  powers on negative intervals.
- Full-row coefficient cancellation and nested binary64 coefficient products,
  checked against exact source expressions.
- Cancellation of undefined constant expressions, which must not make their
  source domains feasible.

The model-binding boundary is the **submitted PySCIPOpt expression DAG**.
This review does not prove SCIP's later simplification, presolve, floating
point feasibility decisions, or final primal and dual bounds. The generic
expression fallback preserves the submitted real expression; it is not an
exact arithmetic SCIP implementation.

## Saved-model metadata audit

`model_binding_audit.py` accepts the independently decoded original instance
and its saved metadata. It replays the affine-bound certificate, reconstructs
requirements from raw original expression trees, and derives each guard's
expected equation from the projection identities above. It checks the recorded
submitted expression, constraint name, submitted and stored sides, actual
witness bounds, and native variable names. It also reconstructs the original
native model without solving to check the remaining deterministic metadata.
Saved expression strings are compared as data, never parsed or evaluated.

The domain walker and native model builder are shared reviewed primitives.
The audit independently reconstructs the original input and the expected
guard equations; it is not a separately implemented symbolic engine or a
proof of SCIP's internal representation. The tests cover all three guard
kinds, JSON path conversion, changed original affine premises and domains,
and more than 20 changes to saved equations, sides, names, bounds, and metadata.

No project-wide verification or CI inspection was performed. Reviewed SHA256
values are:

| File | SHA256 |
| --- | --- |
| `solver/model.py` | `e4b13e50e0104ed2351b51840ac2a5c0154ad64a864ea257a91336af05638cbe` |
| `solver/bounds.py` | `51136605f4d26cb70b1d27348423a2a05fc26368e2a7b69e151598a70a4c3b35` |
| `reviews/test_model_review.py` | `3eff5c35871749756d57cd3b60098375086bc80100fc8eaec25cd6ce8cf91066` |
| `reviews/model_binding_audit.py` | `00e601bb928fdf8f4905c4ce60a37f383bd802cbe46c74ee82b54762d06d7e6e` |
