# Exact reference checkers for optimization outputs

This small standard-library Python implementation demonstrates the difference
between a certified objective gap, distance to the optimizer set, and distance
to one fixed optimizer. It checks supplied rational witnesses. It does not
search for witnesses or implement the paper's optimization algorithms.

## Supported input and guarantees

`output_contracts.py` represents explicitly expanded sparse polynomials with
`fractions.Fraction` coefficients. A supported instance supplies a rational
bounding box, optional rational linear inequalities, and an identity

```text
f(x) = a'x + b + sum_j w_j (u_j'x + v_j)^(2 d_j),
w_j >= 0, d_j >= 1.
```

The checker expands the right-hand side and compares coefficients exactly
with the supplied objective. This identity certifies global convexity.
Weighted affine squares include factored positive semidefinite quadratics;
the implementation does not find a factorization or recognize general convex
polynomials. Expansion can be expensive even when a factored description is
short. No polynomial running-time guarantee in that factored description is
claimed.

Every witness contains a candidate point and a tangent anchor. The checker
checks the candidate's box and linear constraints exactly. Its feasibility
also witnesses that the domain is nonempty. It computes a supporting tangent
at the anchor and minimizes that affine function over the box. This gives a
valid lower bound for the possibly smaller polyhedral domain. It accepts no
asserted optimal value or arbitrary lower bound. The tangent anchor may lie
outside the domain because global convexity is independently certified.

The three checking functions have distinct contracts:

| Function | Certified output |
| --- | --- |
| `verify_value_gap` | The feasible candidate has objective gap at most the requested tolerance. |
| `verify_distance_to_set` | The feasible candidate lies within the requested Euclidean distance of some optimizer. |
| `verify_minimum_norm` | The feasible candidate lies within the requested distance of the fixed minimum-Euclidean-norm optimizer. |

The point checks recompute an effective error-bound constant from the checked
polynomial and domain. They use the constants in the
[sparse coefficient extension](../global-point/sparse-coefficient-degree-extension.md).
They do not accept a user-supplied error-bound constant. The minimum-norm
check constructs the Tikhonov objective `f + tau ||x||^2` and uses the schedule
in [the original point theorem, Section 6](../../research-20261002/new-direction/globally-convex-polynomial-point-oracle.md#6-deterministic-point-and-fixed-selector-evaluation).
Its witness anchor and returned value report concern this regularized
objective. The output point remains a point in the original domain.

The constants are deliberately coarse. A witness can be rejected even when
its true error is below the request. In particular, a box tangent can be too
weak for a constrained optimum because it ignores additional inequalities.
Failure means that this particular certificate is insufficient; it does not
prove that the candidate is inaccurate. The checker is sound for its supported
certificates, not complete for all valid output points.

The implementation also extracts the coefficient matrix of the gradient,
computes its exact rational rank and kernel, and illustrates the translation
invariance of the objective. Keeping the constant-gradient row prevents an
affine slope from being mistaken for an invariant direction.

## Reproduce the diagnostics

From the repository root:

```sh
python -m unittest discover -s research-20261003-arithmetic/implementation -p 'test_*.py' -v
python research-20261003-arithmetic/implementation/demo.py
```

There are no third-party dependencies. The tests cover nonunique optima,
small objective gaps with large coordinate errors, nonzero minimum-norm
selection with an exact rational rounding budget, lower-dimensional domains,
affine and constant objectives, false convexity decompositions, infeasible
candidates, and nonfeasible tangent anchors. They check behavior and rejected
false premises, not just arithmetic agreement between two copies of the same
formula. Finite tests do not establish the universal mathematical error-bound
theorem; that theorem requires its separate proof and review.

`demo.py` prints deterministic JSON for the first two distinctions and a
repeated-squaring example. Twelve squarings from `1/2` use thirteen recurrence
nodes but produce an expanded denominator of 4,097 bits. This illustrates
compact exact versus expanded rational output. It does not turn the checker
into an arithmetic-circuit comparison algorithm or establish a hardness
classification.

## Deliberate limits

The implementation does not optimize general convex polynomials, check
arbitrary convexity promises, construct an unbounded-domain radius, recover a
small-core residual optimizer, decide exact irrational equality, solve
PosSLP, implement an exact quartic active-set algorithm, or produce full
nonconvex MINLP certificates. It supports positive ambient dimension and point
tolerances in `(0,1]`. It uses exact rational arithmetic throughout and rejects
floating-point inputs. It is a small research reference, with no hostile-input
resource limits or production API stability guarantee.
