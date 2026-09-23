# Source audit: fixed aggregate response dimension in bilevel optimization

Date: 2026-09-05. Bounded primary-source audit of
[the candidate](bilevel-fixed-aggregate-response-investigation.md).
The mathematical proof is being reviewed separately.

No matching exact polynomial-time theorem was found for the complete
candidate class: fixed leader, resource, and aggregate dimensions;
unboundedly many box-bounded follower coordinates with positive diagonal
quadratic local costs; a possibly nonconvex polynomial aggregate follower
cost; and explicitly encoded polynomial upper constraints and objective.
The author subsequently extended the model to polynomial `U(x)` and
polynomial box endpoints, and to growing polynomial degrees under dense
or unary-exponent encodings. The fixed resource matrices and box normal
directions remain unchanged. This is a qualified novelty assessment, not
certification of first publication.

The best contribution claim is **compression of the global follower
reaction graph** to fixed dimension, followed by exact optimistic bilevel
optimization. KKT necessity, scalar clipping, multiplier-based dimension
reduction, arrangements, quantifier elimination, and Hoffman continuity
are established tools. In particular, low-dimensional dual arrangements
for separable quadratic resource allocation predate this work by decades.

## Closest resource-allocation antecedent

**Megiddo and Tamir (1993), Linear time algorithms for some separable
quadratic programming problems**, ORL 13(4), 203–211, treats separable
convex quadratic programs with a fixed number of resource equalities
and related transportation structures. Their algorithm works with
piecewise quadratic functions in a fixed-dimensional multiplier space
and identifies cells using critical hyperplanes. The author manuscript's
Sections 2–4 give explicit local minimizer formulas and cell searches.
This is a direct antecedent for eliminating many local quadratic
variables through a few multiplier coordinates.
[Author-hosted primary manuscript](https://theory.stanford.edu/~megiddo/pdf/qtranrev.pdf),
[publication](https://doi.org/10.1016/0167-6377(93)90041-E).

That paper solves a convex, single-level problem. The candidate uses
related elimination inside a nonconvex follower, adds aggregate values
and leader coordinates, and compares all compressed KKT values to
retain global responses. It must not claim that the low-dimensional
multiplier representation or clipped quadratic response is new.

## Exact comparison with Ketkov and Prokopyev (2026)

**Ketkov and Prokopyev, On the Complexity of Bilevel Linear and Quadratic
Programs in Fixed Dimensions**, arXiv:2511.15592v2, revised June 10,
2026, is the closest current bilevel classification.
Theorem 4 gives polynomial solvability for optimistic bilevel convex
quadratic programs with a fixed number of follower variables.
Theorem 6 proves hardness with an indefinite follower objective even
when follower variable and constraint counts are fixed. Its reduction
allows the leader dimension to grow. Theorem 5 concerns pessimistic
semantics with fixed follower constraint count. Their convex optimistic
case with fixed follower constraint count is left open.
[Primary full text](https://arxiv.org/html/2511.15592v2), Table 2 and
Theorems 4–6.

The candidate fixes leader dimension and structural resource/aggregate
counts while allowing follower dimension and its box inequalities to
grow. It therefore neither contradicts their hardness results nor
resolves their general fixed-follower-constraint open case. Its
nonconvex aggregate term is structurally restricted, while its upper
polynomials are more general than their convex quadratic upper model.
These are different parameterizations; describe them explicitly rather
than implying that one theorem subsumes the other.

## Parametric QP and solution-path methods

Parametric quadratic programming already uses active-set regions and
explicit formulas for local or global solution maps. A fixed number
of parameters alone does not make arbitrary active-set enumeration
polynomial. A checked primary example is **Ghaffari-Hadigheh, Romanko,
and Terlaky, Bi-Parametric Convex Quadratic Optimization**, Lehigh
report 09T-007: its
discussion of convex quadratic optimization explicitly distinguishes
output-size enumeration from input-polynomial complexity because the
number of optimal partitions can grow exponentially.
[Primary institutional manuscript](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/09/09t_007.pdf).
This audit uses that discussion only for the stated distinction; it
does not import a theorem about the candidate's structured class.

The candidate's polynomial regime bound comes from something stronger
than ordinary parametric QP notation: all clipping tests are polynomials
of controlled degree in a fixed number of leader, aggregate, and resource
multiplier coordinates. Their realizable sign conditions are polynomial
in the number of tests and their actual degree. That reduction makes the existing
real-algebraic tools applicable.

**Provably Data-driven Multiple Hyper-parameter Tuning with Structured
Loss Function (2026)** is a further methodological neighbor. Section 6
encodes bi-level validation using first-order polynomial formulas;
Section 7 assumes a piecewise rational solution path and exploits its
description. Its target is pseudo-dimension and statistical sample
complexity, rather than exact bit-complexity of global bilevel
optimization. It shows that neither quantified descriptions of
bi-level optimality nor rational solution-path analysis is a new
general idea.
[Primary paper](https://arxiv.org/html/2602.02406), Sections 6–7.

## Fixed-rank quadratic optimization is not the same restriction

**Hladík, Černý, and Rada (2021)** solve box-constrained quadratic
optimization when the rank of the **whole** quadratic matrix is fixed,
using a zonotope of fixed dimension. In the candidate, even a quadratic
aggregate term yields a follower Hessian of the form
`diag(a_i(x))+U^T M(x) U`; its total rank may grow with the number of
followers. Their theorem therefore does not directly apply.
[Primary preprint](https://arxiv.org/abs/1911.10877),
[author's publication record](https://kam.mff.cuni.cz/~hladik/publ/b2hd-HlaCer2021c.html).

**Cen and Xia (2021)** give global branch-and-bound algorithms for
quadratic programs with a fixed small number of negative eigenvalues,
including an approximation iteration bound for one negative eigenvalue.
They explicitly note hardness under general convex constraints even
with one negative eigenvalue. These methods do not supply the
candidate's exact polynomial theorem for its box-plus-fixed-resources
geometry or its bilevel reaction graph.
[Primary publisher article](https://pubsonline.informs.org/doi/10.1287/ijoc.2020.1017),
abstract and contribution statement checked.

Thus the result should not be characterized as tractability from
low-rank nonconvexity alone. Positive separable local curvature,
the original box structure, and the fixed resource and leader dimensions
are essential stated restrictions.

## Established algebraic and continuity ingredients

The sign-condition enumeration and fixed-total-variable quantifier
elimination are standard real-algebraic algorithms. The candidate
correctly gives its own encoding argument: multiplying the positive
denominators increases degrees with `N`, but fixed ambient dimension
keeps the expanded polynomial list polynomial in size. This is an
application of established algorithms, not a new quantifier-elimination
method.
[Basu–Pollack–Roy primary manuscript](https://www.math.purdue.edu/~sbasu/jacm95.ps).

Comparing KKT values is valid only because every global follower optimum
is represented and every represented point is follower-feasible. The
second quantified KKT copy is a compact way of expressing that comparison;
it does not turn KKT conditions alone into a sufficient nonconvex
optimality condition.

The fixed follower constraint normals also matter for attainment.
Hoffman's bound supplies continuity of feasible fibers along feasible
right-hand-side perturbations. The candidate does not assert such a
uniform argument for arbitrary leader-dependent resource matrices.
Polynomial box endpoints only change right-hand sides, while a
polynomial aggregate map `U(x)` changes the objective representation
without changing the follower's resource normals.
[Hoffman's original paper](https://upload.wikimedia.org/wikipedia/commons/0/07/On_approximate_solutions_of_systems_of_linear_inequalities_%28IA_jresv49n4p263%29.pdf).

## Recommended claim and remaining limits

After mathematical acceptance, claim an exact polynomial-bit algorithm
for this explicit fixed-aggregate response class with unbounded follower
dimension. Attribute the multiplier clipping and cell machinery to
separable resource-allocation and parametric programming, and the final
logical processing to real algebraic geometry.

Do not claim an algorithm for unrestricted nonconvex bilevel programs,
for low-rank perturbations of arbitrary convex follower objectives,
for fixed leader dimension alone, or for unrestricted integer followers.
Polynomial time here has an exponent depending on the fixed dimensions;
actual degrees may grow in the stated dense/unary encoding. This is
not a fixed-parameter running-time claim of the form
`f(parameter)*input_size^constant`.

Searches combined fixed leader/follower dimensions, fixed resource
counts, separable quadratic allocation, diagonal plus low rank,
nonconvex aggregate costs, parametric quadratic solution paths, and
bilevel quantifier elimination, including 2026 work. No matching complete
theorem was found. This was a bounded search, and the broad parametric
programming literature has not received an exhaustive forward-citation
audit.
