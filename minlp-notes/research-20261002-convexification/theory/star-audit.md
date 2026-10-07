# Independent audit of constrained quadratic star support

The constrained-star argument and its implementation passed an independent
exact audit. No mathematical correctness defect was found. This audit covers
continuous quadratic support with finite rational bounds and rows involving
the center and at most one leaf. It does not establish a runtime improvement
inside a MINLP solver or a priority claim for the theorem.

The reviewed implementation is [quadratic_star.py](quadratic_star.py), together
with its polygon projection routine in
[quadratic_polygon.py](quadratic_polygon.py). The proof and interface claims
appear in [theory/README.md](README.md).

## Independent global-minimum check

[check_star_audit.py](check_star_audit.py) independently enumerates stationary
points on all possible faces of the full feasible polytope. Its own rational
Gaussian elimination solves the equality-constrained stationarity system for
each subset of at most `n` active rows, including the original variable bounds.
It keeps feasible solutions and evaluates the original polynomial directly.
It does not use the producer's polygon vertices, center projection, envelope
construction, breakpoint construction, or conditional minimization routines.

This candidate enumeration is complete for bounded quadratic minimization.
A minimizer exists on a nonempty bounded polytope. In the relative interior
of its minimal face, the gradient restricted to the face vanishes and the
restricted Hessian is positive semidefinite. If that Hessian is singular, a
nonzero tangent null direction preserves the objective until reaching a
smaller face. Repeating this step produces a minimizer on a face whose
restricted Hessian is positive definite, or a vertex. An independent set of
active normals for that face gives a nonsingular stationarity system among
the enumerated systems. Every nonempty bounded polytope also has a vertex,
so an empty candidate set certifies emptiness. This algorithm is exponential
in the dimension and is used only as a small-instance audit oracle.

The seeded cases include two or three leaves, all possible center positions,
rational affine rows, positive, zero, and negative leaf curvature, and
occasional fixed variables and equality rows. For every nonempty case, the
audit compares the exact attained bound against the independent oracle and
checks the reported minimizer against the original bounds, rows, and
polynomial. It also evaluates every returned affine rule at both interval
ends and three interior points. Those sampled checks supplement the global
oracle; they are not a proof of correctness throughout each interval.

One separately specified four-variable example combines crossing lower and
upper envelopes, mixed leaf curvature, and a center at index `1`. Its exact
minimum is `-1993/912`, attained at
`(-25/114, -25/76, 51/76, -51/76)`. The producer emits seven center pieces.
The audit also rejects five certificate mutations and two changes to the
trusted original problem.

Executed from the repository root:

```sh
python research-20261002-convexification/theory/check_star_audit.py
```

Output, preserved in [star-audit-results.txt](star-audit-results.txt):

```text
155 random constrained stars: 76 feasible, 79 empty; 298 returned pieces checked at both ends and three interior points
Designed crossing-envelope mixed-curvature star: -1993/912 ['-25/114', '-25/76', '51/76', '-51/76'] 7 pieces
7 certificate/trusted-input tampering checks rejected
```

The command exited successfully. This is a targeted local audit. No
project-wide verification was run and no CI status or logs were inspected.

## Proof and complexity assessment

The projection step is sound: each bounded center–leaf polygon projects to a
closed interval, and their intersection is exactly the feasible center set.
Once the center is fixed in that intersection, the leaves are independent.
The statement includes singleton projections and fixed leaf variables.

All possible active-envelope changes are included among pairwise line
intersections. For a convex leaf, clipping its free affine minimizer adds only
affine intersections. For a concave or linear leaf, subtracting the endpoint
values gives the interval width times an affine expression on each envelope
piece. Since the width is nonnegative, the affine factor determines endpoint
selection. Zero width and identically tied endpoints need no extra roots.
Conditional minima are continuous, so a rule selected inside a regime gives
the correct value at either endpoint, even when the minimizing leaf value
has a jump there.

The conservative `O((k+m+1)^3)` rational-operation bound is supported by the
implementation. If leaf `i` has `s_i` bound lines, projection costs
`O((s_i+1)^3)`, its line intersections produce `O(s_i^2)` pieces, and selecting
active lines across them costs `O(s_i^3)`. The combined partition has
`O(sum_i s_i^2)` pieces. Computing all leaf rules and the objective on every
combined piece costs `O((sum_i s_i) sum_i s_i^2)`. Sorting, center-only rows,
dense row normalization, and output construction fit the stated cubic bound.
With no added rows, there are `O(k)` regimes and the implementation's direct
reevaluation of all leaves costs `O((k+1)^2)` operations.

The bit-complexity qualification is also supported. Breakpoints solve affine
equations in rational input data. Piece coefficients are sums of rational
expressions of bounded algebraic depth, and candidate centers solve linear
stationarity equations. Numerator and denominator lengths grow polynomially
with input length. The operation bound alone is not a claim about constant
cost rational arithmetic or practical wall-clock performance.

## Certificate boundary

Replay recomputes the same canonical mathematical result from trusted inputs
and compares the complete output. This binds the normalized rational box,
rows, polynomial, center index, partition, attained values, and minimizers.
It detects omitted pieces and the tested input and certificate changes.
Binding is mathematical, not lexical: equal rational scalar representations
normalize identically, and zero objective terms are omitted. Row order is
retained. The certificate does not preserve an original expression tree.

The producer and replay checker share the exact algorithms. They therefore
share possible implementation defects; replay is not an independently
implemented proof checker. The independent audit reduces that testing gap on
the exercised cases but does not replace a general proof or formal
verification. A solver must additionally bind any emitted floating-point cut
to the certified rational inequality. Exact support for a selected direction
does not prove complete separation or the solver's final global bound.

Reviewed source SHA-256 values:

```text
669aefecc4cc4470f12552a835956337ad6536f6189ef0cebee6542c94398fde  quadratic_star.py
7172e3c900631068198580608c2dcf01678d65379b007d36d28fa55ecad1e31b  quadratic_polygon.py
e4561dcd123de5bd3a83be6c5a0198ece800767b7320bed09babc005a3f7d4a7  check_star_audit.py
```
