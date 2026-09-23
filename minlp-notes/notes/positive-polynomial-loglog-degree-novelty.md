# Source audit: double-logarithmic degree overhead for positive polynomial graphs

Date: 2026-09-05. Bounded primary-source audit of
[the positive-polynomial candidate](positive-polynomial-loglog-degree-precision.md).
The complete draft was read. Independent agents are responsible for its
mathematical verification.

No matching theorem was found giving a compact rational MILP within
`O(r+sum_i log log(D_i+2))` integer coordinates of every convex lift of the
same graph approximation. The candidate's two useful additions are an
allocation-dependent change of coordinates for the universal lower bound,
and a polynomial-size endpoint-layer construction for the upper bound.
Neither convex optimality, log-utility allocation, nor dyadic approximation
or binary product linearization should be claimed as new.

## What the supporting scalarization adds

Kelly, Maulloo, and Tan,
[Rate control for communication networks: shadow prices, proportional fairness and stability](https://web.stanford.edu/class/cs244/papers/ShadowPricesFairnessStability.pdf)
(1998), printed page 239, equations (1)–(4), develops weighted logarithmic
resource allocation and its shadow-price characterization. Massoulié,
[Structural properties of proportional fairness: stability and insensitivity](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2005-102.pdf),
Sections 1–2, explicitly treats convex downward-closed capacity regions and
characterizes log-optimal allocations using convex duality. These are
direct precedents for the allocation framework, beyond linear capacity
constraints.

At a positive maximizer, replacing a convex feasible body by its supporting
halfspace in the objective-gradient direction preserves the optimum by
the first-order inequality for a concave objective. The candidate's
normal-cone calculation applies this standard fact while retaining the
coordinate caps. Its nonnegative supporting output weights then combine
all powers of each coordinate into one normalized polynomial. This is
the relevant new use: the scalarization is selected by the allocation,
and its square-root coordinate maps permit a degree-independent
parity-volume bound without losing the allocation optimum.

The convexity of `sqrt(sum_k d_k x^k)` for nonnegative `d_k` and `k>=2`
follows directly by viewing it as the Euclidean norm of nonnegative
convex components `sqrt(d_k)x^(k/2)`. The draft proves this elementary
composition step; it need not be advertised as a new general convexity
theorem. Likewise, the midpoint-parity obstruction must credit Lubin,
Zadik, and Vielma,
[Mixed-integer convex representability](https://arxiv.org/abs/1706.05135),
Lemma 4.1 in the checked local full text. Its use after an allocation-chosen
coordinate transformation is the proposed bridge.

The multipliers are existential lower-bound tools. The rational algorithm
does not need to compute them or a rational version of the coordinate
homeomorphisms. This distinction is important when comparing the proof
to parametric optimization algorithms.

## Adaptive layers and existing piecewise-linear approximation

Rote's [1992 Sandwich-algorithm paper](https://page.mi.fu-berlin.de/rote/Papers/pdf/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.pdf)
already gives adaptive chord/tangent approximation of convex functions
with optimal-order quadratic decay in the number of pieces. The
[finite pure-power audit](pure-power-degree-independent-count-novelty.md)
records further direct power-interpolation precedents, including Wei et
al. (2019) and Lee, Skipper, Speakman, and Xu. Those works do not supply
the candidate's universal minimum-integer comparison.

Magnanti and Stratila,
[Separable Concave Optimization Approximately Equals Piecewise-Linear Optimization](https://optimization-online.org/wp-content/uploads/2012/01/3316.pdf)
(2012 full manuscript following their 2004 extended abstract), Section 2,
uses geometrically spaced tangent points and bounds piece counts for
relative-error approximation. Theorem 2 also gives a piece-count lower
bound for the square root on a positive interval. It is relevant prior
for geometric grids and optimization-oriented approximation complexity.
Its concave objectives, relative-error criterion, and prescribed
piecewise-linear approximants differ from convex polynomial whole-graph
outer approximations with arbitrary convex integer lifts. Its lower
bound cannot simply be transferred to the present integer-count model.

The candidate uses only `O(log D)` endpoint layers because a layer's
squared width times `k(k-1)x^(k-2)` is uniformly bounded for every
`2<=k<=D`. Encoding the layer index then costs `O(log log D)` bits.
This is an elementary geometric-layer application; the impact lies in
its simultaneous validity for all positive coefficient mixtures and in
the total formulation guarantee. No claim that geometric layers themselves
were introduced here is warranted.

## Compact formulations and attribution

Vielma,
[Embedding Formulations and Complexity for Unions of Polyhedra](https://arxiv.org/pdf/1506.01417),
Proposition 1 and Corollary 1, explicitly encode a union of `N` polyhedra
using `ceil(log2 N)` bits. Thus logarithmic layer selection is prior art.
Continuous selectors forced to zero or one by the code do not create
additional integer coordinates; their bounded-product linearization is
a standard extended-formulation device.

Teles, Castro, and Matos's polynomial parameterization papers and
Kolodziej, Castro, and Grossmann's bilinear disaggregation paper are the
closest established polynomial MILP construction methods. Their checked
primary sources and access limits are recorded in the
[positive-polynomial audit](positive-separable-polynomial-precision-novelty.md).
Exact power recurrences using shared digit variables should be credited
to this methodology. The candidate adds local endpoint normalization and
uses its uniform curvature bound to control the entire admitted error
rectangle, while comparing the resulting integer count to all convex
lifts rather than just other discretization formulations.

## Scope and recommended claim

The theorem concerns nonnegative coefficients in the original coordinate
monomial basis, not all polynomials that happen to be positive on the box.
The whole output error body is unconditional, not merely centrally
symmetric. Degrees may grow under dense encoding; the exact recurrences
do not establish polynomial complexity for huge binary-encoded sparse
exponents.

The lower bound is degree-independent. The double-logarithmic degree term
is the current upper construction's overhead, not a proven necessary or
sharp dependence. The separate pure-power result already achieves a
degree-independent comparison for that subclass. No claim that mixtures
must incur this overhead follows from the present proof.

A defensible contribution is a compact rational approximation of positive
separable polynomial vector graphs whose integer dimension exceeds the
minimum among all convex lifts by at most
`O(r+sum_i log log(D_i+2))`, together with a degree-independent lower
benchmark obtained through supporting scalarization. No exact match was
found in this bounded source search; this is not a proof of worldwide
publication priority.
