# Independent separation review

This internal review covers `solver/separation.py`, `theory/separation.md`,
and the proof in `document/separation.tex`. It is separate from the implementation author's
review, but it is not external peer review or formal verification. The
generic quadratic polytope oracle has a separate mathematical review;
this review checks its use in separation and replay.

The inspected finite separation argument is sound under the stated rational
polynomial and compact rational polytope assumptions. The independent suite
passes **21 tests**. The review does not establish practical efficiency or
certify the complete numerical solver.

## Independent mathematical checks

For a nonempty compact rational polytope `P`, a continuous polynomial graph
`F`, and a query `q`, the distance in the L1 norm to `conv(F(P))` is

`max_{||c||_infinity <= 1} (min_{x in P} c.F(x) - c.q)`.

If `R >= sum_j max_{x in P} |F_j(x)-q_j|`, the expression inside this
maximum changes by at most `R * ||c-d||_infinity` when its normal changes
from `c` to `d`. Consequently a finite normal grid with covering radius
`rho`, and a support calculation with error at most `delta`, can certify
distance at most `delta + R*rho`. This statement requires coverage of the
whole normal box, including its boundary. Testing only its corners is not
sufficient.

A feasible graph point for each grid direction is enough to check the
upper support bound needed by a near-hull verdict. A separating cut needs a
lower support bound over the entire domain. These are different evidence
requirements. Neither a failed direction search nor a budget-exhausted
grid is a distance certificate.

A rational polytope is the convex hull of its vertices even when it is a
segment or singleton in its ambient space. Rational barycentric samples
can therefore cover a thin affine equality domain exactly. Filtering a
rectangular floating grid for approximate feasibility cannot replace this
argument.

For designated coordinates `J`, restricting normals to be nonnegative changes
the target set to `conv(F(P)) + cone{e_j: j in J}`. This sum is closed because
the hull is compact. Its finite lower support has precisely these normal
signs, so the same distance duality holds with the restricted normal box.
The primal distance contribution is `max(F_j-q_j,0)` on a cone coordinate,
rather than an absolute residual. The API and replay bind the chosen `J`.

An exact rational separating inequality need not survive binary64 export.
Coefficient changes require a correction using bounds on graph coordinates,
and the right-hand side must be rounded in the safe direction. If rounding
erases the violation, the algorithm can retain an exact rational cut, but
must not claim to have exported a solver cut that separates the query.

## Independent adversarial examples

- For `F(x)=(x,x^2)` on `[0,1]`, the query `(3/10,2/25)` has L1 distance
  exactly `1/100` from the graph hull. The tangent normal `(-3/5,1)` gives
  this lower bound; the feasible graph point `(3/10,9/100)` attains the
  matching distance. None of the nine normals with coordinates in
  `{-1,0,1}` separates this query. This detects corner-only enumeration.
- On `x+y=1/3`, `x,y in [0,1]`, the maximum of `xy` is exactly `1/36`.
  The query `(1/6,1/6,1/24)` violates this bound by `1/72`. This domain
  also tests exact equality handling without a feasible rectangular grid.
- A constant graph equal to the query has distance zero and `R=0`; a
  normal-grid resolution formula must not divide by zero.
- Contradictory affine inequalities describe an empty domain. This has an
  emptiness verdict, rather than finite distance to a nonempty graph hull.
- A positive rational gap smaller than the least positive binary64 value
  tests whether exact separation and exported numerical separation are
  distinguished.

## Findings resolved during review

1. The first source version called the quadratic replay API with arguments
   in the wrong order. The corrected call binds bounds, rows, coefficients,
   and certificate in the oracle's documented order.
2. Arbitrary-precision SymPy floating constants were narrowed through Python
   binary64 before conversion to rational coefficients. They now retain
   their exact supplied SymPy value.
3. Algebraic polynomial collection accepted an unevaluated expression
   `x * x**(-1)` as the constant one, losing its original domain restriction.
   Source syntax now admits only polynomial nodes before simplification;
   the singleton-domain regression at `x=0` requires refusal.
4. The original normal iterator materialized its entire coordinate mesh
   before a direction-budget check. A tiny tolerance could allocate an
   astronomical mesh even with zero permitted support calls. Coordinate
   generation is now lazy, with a bounded set of simple-priority normals.
   A tolerance `2^-200` with zero direction budget returns `unresolved`.
5. Recursive weak-composition and normal-grid iterators imposed an unstated
   Python stack-depth limit on vertex and feature counts. Both are now
   iterative. Independent checks exercise 1,200 components and verify
   the exact cardinality and uniqueness of smaller complete enumerations.
6. Malformed top-level certificates such as `None` raised an attribute error.
   Replay now rejects these inputs with `False`.

## Evidence and trust boundaries

The independent fixtures compute expected optima by completing squares,
one-dimensional stationary-point calculations, or elementary product bounds.
They do not obtain expected support values by calling the producer's oracle.
For nonbinary normals, the tests independently recompute the true quadratic
minimum using the actual exported binary64 coefficients. This verifies the
final row, including negative feature ranges, rather than only comparing
producer and checker output.

Mutation checks remove normal-grid evidence, replace directional witnesses,
put samples outside the domain, change support errors, alter convex weights,
change the expected query, domain, and tolerance, and forge an exported right
side. A graph cut with a negative cone coefficient is rejected even after its
untrusted problem header is changed to claim the cone model.

The polynomial lower bound uses the whole barycentric domain net and the
exact derivative-based error. A near-hull grid certificate instead checks
feasibility and an upper gap for each required normal. Replay need not trust
a point to be an optimizer when it is only being used as an upper witness.
The required grid is reconstructed, including its size and all coordinates.

The following boundaries remain part of the contract:

- `complete=True` gives a finite exact-arithmetic algorithm for a positive
  tolerance. It is not a polynomial-time or practical-runtime guarantee and
  does not decide exact hull membership.
- Direction and sample budgets are cardinality limits. They do not bound
  vertex/face enumeration, total arithmetic work, or wall-clock time. The
  practical solver uses a separate capped support wrapper.
- An incomplete search returns `unresolved` and supplies no geometric
  certificate. `within_tolerance` refers to L1 distance in the specified
  feature coordinates, and to the enlarged set when cone coordinates are
  requested. It is not automatically a distance in original model variables.
- A rational cut remains valid when binary64 export overflows or erases its
  strict violation. The export records availability and whether it separates;
  the caller must respect both fields.
- Replay shares exact polynomial and polytope routines with generation.
  Numerical LP proposals are rechecked, but Python, SymPy, and the shared
  rational arithmetic implementation remain trusted. This is not an
  independently implemented formal proof kernel.
- Source syntax validation cannot recover a domain restriction that was
  already removed before the caller constructed the supplied expression.

## Targeted verification

The independent command is:

```sh
/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/test_separation_review.py
```

It passes **21 tests**. The final captured output is in
`separation-review-checks.txt`. No project-wide verification or CI inspection
was performed.

The final reviewed SHA-256 values are:

| File | SHA-256 |
| --- | --- |
| `solver/separation.py` | `8869c1952a9b4b38fbc44352bb8119a9ffa6c721571bb112b7f3e428030aced9` |
| `theory/separation.md` | `dc647c1a0d61804ee78be31ba97bbf8988b0204ec4364818fc65db216f1cad5f` |
| `document/separation.tex` | `25c488d903a6a0c9fb87cdfcdb5498ba21953f06edc257b153012b07c8919205` |
| `theory/quadratic_polytope.py` (separation import and replay binding) | `4fffd2f5bb9b529e98b68ab1bd150083a24a9d5ee0c4fc122516bd82aab30a7b` |
| `reviews/test_separation_review.py` | `b6d3f9a4e843856a45ae9e74216082ccd54e5bf455e472613231c60ddb4eeb4d` |
