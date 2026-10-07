# Parametric flow recourse can have many value-function pieces

Date: 2026-10-02. This focused note records the strongest verified lower
bound relevant to scalar parametric integer-flow recourse. It concerns the
number of regions in a complete parametric value function. It does not show
that evaluating the recourse value at one parameter, or optimizing the
reduced value with a convex core term, is hard.

## Verified shortest-path lower bound

Gajjar and Radhakrishnan's primary paper [“Parametric Shortest Paths in
Planar Graphs”](https://eccc.weizmann.ac.il/report/2018/211/download) gives a
particularly strong, precisely scoped result. Their model is a directed
acyclic graph with source `s`, sink `t`, and affine edge weights
`w_e(lambda)=m_e lambda+c_e`. The shortest-path value is the lower envelope
of the affine costs of all `s`–`t` paths. Their Theorem 1 states that even
for planar graphs, the envelope can have `n^{Omega(log n)}` breakpoints when
the integer edge coefficients have only `O(log^3 n)` bits. The result counts
changes of the optimal path / pieces of the value function over the real
parameter line. The same paper's Theorem 3 gives the corresponding
unbounded-fan-in PRAM lower bound; that computation-model result is not
needed for the breakpoint comparison here.

This covers the acyclic, polynomial-bit setting, rather than relying on
large or arbitrary real coefficients. An `s`–`t` shortest-path instance is
also a unit-flow min-cost-flow instance on the same acyclic network, so the
breakpoint lower bound applies to that special case of integer recourse.
Adding the same convex function of `lambda` to every path cost leaves all
path-switching breakpoints unchanged. Thus a convex core penalty does not
remove the large number of branches in this construction.

The affine edge-cost construction is posed for all real `lambda`. Its finite
set of breakpoints can be enclosed in a rational interval and mapped
affinely to `[0,1]`; path costs remain affine with polynomial-bit rational
coefficients. This is a reparameterization of the breakpoint example, not a
claim about the candidate theorem's noise distribution or normalized
curvature-to-noise parameter.

## Carstensen and the bounded-coefficient refinement

The same primary paper reports the earlier general-graph history: Carstensen
proved an `n^{Omega(log n)}` breakpoint lower bound without a coefficient
bound, and Mulmuley and Shah proved the same order with coefficient bit
length `O(log^3 n)`. This is consistent with their own primary paper,
[Mulmuley and Shah, “A Lower Bound for the Shortest Path Problem”](https://doi.org/10.1006/jcss.2001.1766),
whose Theorem 1.3 is reported in the paper's available text as an explicit
`n`-vertex family with `2^{Omega(log^2 n)}` breakpoints and `O(log^3 n)`-bit
edge-cost coefficients. The two expressions are equivalent up to constants
in the exponent.

Carstensen's separate network-programming paper, [“Complexity of Some
Parametric Integer and Network Programming Problems”](https://doi.org/10.1007/BF02591893),
has an official Springer abstract stating that its network-programming
example has a number of optimal-cost breakpoints exponential in the square
root of the number of variables. The full article was not available in the
source route checked for this audit, so this note does not infer its exact
network restrictions, coefficient sizes, or a unit-flow formulation from
the abstract alone. The shortest-path result above is the primary-text
comparison used here.

## What this establishes for recourse methods

The shortest-path value can be evaluated at a fixed rational `lambda` by
ordinary shortest-path algorithms, and the corresponding unit-flow
recourse has an exact polynomial-time oracle. Yet its complete parametric
message can have a superpolynomial number of pieces. Therefore a solver
that explicitly stores every label/flow regime in a symbolic message can
incur superpolynomial work even with one continuous core coordinate. This
is a warning against deriving polynomial complexity from parameter
dimension alone.

It does not imply hardness of minimizing a convex core penalty plus that
message, expected work under independent random perturbations, or the
point-query / pruning algorithm in
[the native-integer recourse theorem](../new-direction/smoothed-native-integer-recourse.md).
That algorithm queries an exact conditional oracle at selected core points
and tests competing labels; it does not enumerate all parametric flow
regions. The lower bound is thus a baseline for approaches based on full
parametric-message enumeration, not an obstruction to the theorem's stated
oracle interface.

## Access and remaining source gap

- Gajjar and Radhakrishnan (2019), ECCC TR18-211, revised 2019: primary PDF
  open and read; Theorem 1 gives the planar `n^{Omega(log n)}` lower bound
  with `O(log^3 n)`-bit integer coefficients, and Section 1 defines the
  directed-acyclic affine-weight model.
- Mulmuley and Shah (2001), *Journal of Computer and System Sciences*
  63(2), 253–267, DOI `10.1006/jcss.2001.1766`: primary article identity
  and Theorem 1.3 statement checked in the author's indexed text; the
  publisher page is abstract-only in the route used here. Gajjar and
  Radhakrishnan independently state the bounded-coefficient predecessor
  result in their primary paper.
- Carstensen (1983), *Mathematical Programming* 26, 64–75, DOI
  `10.1007/BF02591893`: official publisher abstract only. The exact network
  construction and coefficient restrictions remain unverified here.

The last two primary full texts should be checked by the sole literature
ingester before this audit makes any more detailed claim about their exact
network-flow variants.
