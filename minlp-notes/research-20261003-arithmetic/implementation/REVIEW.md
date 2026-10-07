# Independent review of the exact output checker

This review covers `output_contracts.py`, `test_output_contracts.py`, and the
implementation claims in `README.md`. It compares the constants with the
[sparse coefficient extension](../global-point/sparse-coefficient-degree-extension.md)
and the selector schedule with Section 6 of the
[original point theorem](../../research-20261002/new-direction/globally-convex-polynomial-point-oracle.md).
No unresolved soundness defect was found within the documented input model.
This is a review of a reference witness checker, not a validation of a
general optimization algorithm or a hostile-code execution boundary.

## Findings

- The convexity certificate is checked by exact equality of canonical
  polynomial coefficients. Each nonlinear summand has a checked nonnegative
  weight and positive even exponent. The affine term is unrestricted, as it
  should be. Candidate feasibility is checked against the supplied box and
  every extra inequality.
- The value lower bound is recomputed from the supplied objective and a
  supporting tangent. The anchor need not be feasible because the certificate
  establishes global convexity. Neither an asserted optimum nor an asserted
  lower bound enters the calculation.
- The gradient coefficient rows include the constant gradient row. The
  denominator and integer-height calculations use these actual rows and
  the supplied constraint normals. Omitting right-hand sides from the
  Hoffman constant is justified by its uniformity in those right-hand sides.
- The implementation's `degree`, `c_star`, `coefficient_interpolation`, and
  `gamma` agree with `D`, `C_*`, `B_(D-1)`, and equation (9) of the sparse
  coefficient extension. The box radius is a valid infinity-norm bound.
  Its separately computed sum of coordinate bounds is a valid Euclidean-norm
  bound for the selector schedule.
- The minimum-norm routine uses the original Euclidean norm, the stated
  `tau` and `eta`, and a freshly checked regularized objective. The theorem
  allocates half the requested distance to selection bias and half to solve
  error. The returned value report concerns that regularized objective, as
  documented.

The initial test run exposed the known constant-objective empty-row `max`
error. The author corrected it before the successful final test run below.

## Checks performed

The targeted command

```sh
python3 -B -m unittest discover -s research-20261003-arithmetic/implementation -p test_output_contracts.py -v
```

passed all ten tests after that correction and the addition of the constrained
tangent regression described below. No project-wide verification or
CI inspection was performed.

A separate in-memory exact-rational diagnostic passed 630 checks. It used
one-dimensional convex quadratics with analytic constrained optimizers,
rational linear constraints, and both feasible and infeasible tangent
anchors. It checked tangent lower bounds, objective-gap arithmetic, the
effective distance inequality when the true gap is at most one, and the
Tikhonov selection bias. It also rejected altered constant, linear, cubic,
and quartic coefficients against an unchanged convexity certificate and
rejected a witness for an inconsistent domain. These finite checks supplement
the formula review; they do not prove the general error-bound theorem.

## Material limits

The box tangent can fail to certify even an exact constrained optimizer.
For example, with `f(x,y)=x+y`, box `[-1,1]^2`, and constraint `x+y>=1`,
the optimum is one but every tangent lower bound computed by this checker
is minus two. Thus no anchor certifies a gap smaller than three. The
independent diagnostic reproduced this example, and a checked-in regression
now covers it. The README correctly explains that rejection does not establish
inaccuracy.

Exact expansion can be large relative to a factored certificate. The
checker has no hostile-input resource limits, accepts only a restricted
certificate class, and neither generates witnesses nor supplies a complete
certificate method for arbitrary polyhedra. These limits are disclosed in
the README. They do not invalidate accepted certificates.
