# Source assessment: the vector-power refinement obstruction

Date: 2026-09-05. Status: bounded primary-source audit; two mathematical
reviews were active when this note was written.

The [candidate](positive-polynomial-vector-refinement-obstruction.md) is a
useful boundary for the repository's scalar proofs. I did not locate its
combined example and conclusions in the checked primary literature. The
appropriate claim is an explicit separation between three complexity tests,
not a general failure of vector approximation or scalarization.

For `F_j(x)=(7/4)x^(128*1024^(j-1))`, `j=1,...,M`, on `[0,1]` with unit
componentwise error, every exact-graph midpoint is admissible, and each
fixed normalized linear scalarization has a finite formulation with at most
one binary variable. Nevertheless the joint graph needs at least
`ceil(log_3 M)` general integer coordinates and `ceil(log2 M)` binaries.
A finite binary upper bound is `ceil(log2(M+1))`. Common chord partitions
also satisfy `N_F(2)=1` and `N_F(1)>=M`.

The example therefore rules out an output-independent bound based only on
the maximum of the separate scalarized integer minima, and rules out a
constant-piece vector version of the scalar error-halving lemma. It does
**not** prove that `p_bin-p_conv` is unbounded.

## Established mechanisms

**Residue classes and convex combinations.**
[Lubin, Vielma, and Zadik, Mixed-integer convex representability](https://optimization-online.org/wp-content/uploads/2017/06/6082.pdf),
Lemma 4.1, give a finite quantitative midpoint obstruction through parity
of integer lifts. Their Section 4.1 also characterizes binary convex
representability through finite unions of projected convex sets. These are
the direct conceptual predecessors. Replacing parity by congruence modulo
three and using the weights `1/3,2/3` is an elementary variant of the same
argument; no new general residue-class technique should be claimed.
Their Section 7 asks about sufficiency of the midpoint condition for exact
representability. The present example does not answer that question: it
has finite formulations, concerns an approximation sandwich, and checks
midpoints of exact-graph contacts rather than all points of an exact target
set.

**Midpoint versus full chord error.**
[Simchowitz, Jamieson, Suchow, and Griffiths (2018)](https://arxiv.org/pdf/1808.04523),
Lemma 2.1, give the factor-two comparison between midpoint and maximum
chord error for scalar convex functions. Thus a midpoint error below one
does not already promise a full chord error below one. The candidate makes
that familiar constant-factor distinction accumulate across separated
boundary layers of different output powers. Its stronger conclusion is
that a single coarse vector chord cannot be refined to unit accuracy using
a number of pieces bounded independently of the output count. Scalar
three-piece refinement remains valid; simultaneous refinement can require
the union of many different output breakpoints.

**Finite disjunction encoding.**
The upper bound is a finite union of rectangles indexed by the half-height
points of the monotone outputs. Binary coding of a finite union is standard.
The real algebraic endpoints are allowed by the finite-count model; this
upper bound alone is not a polynomial rational construction theorem. The
[compiler audit](compiled-rational-knot-formulations-novelty.md) records
the broader established formulation machinery, but the obstruction does
not need that compiler.

## Simultaneous polynomial approximation and scalarization

A recent nearby source is
[Bernasconi, Castiglioni, Celli, and Farina (July 2026)](https://arxiv.org/pdf/2607.25693),
*A Unifying Framework for Quasi-Polynomial Optimization of Fixed-degree
Polynomials*. Theorems 1.1--1.3, with full versions later in the paper,
construct simultaneous covers of joint polynomial value sets. Their
guarantees use fixed degree and bounded range on an enclosing simplex or
nonnegative `l_1` ball, and explicitly account for the number of polynomials.
This is relevant current work on genuinely simultaneous approximation.
It does not establish a common chord-refinement bound or a lower bound
on convex graph-lift integer dimension. The present family has growing
degrees, and preserving a whole input-output graph under convex lifted
combinations is a different requirement from covering a value set by
representative values. There is no contradiction with their results.

The scalarization statement needs careful quantifiers. It says

```
for each lambda with ||lambda||_1=1,
there exists a small formulation for lambda^T F,
```

while no uniformly bounded integer count suffices for a joint formulation
of `F`. Each scalarization may choose its own split point and its own
formulation. This is not a claim that the collection of scalarized functions
fails to determine the vector function, or that scalarization cannot certify
membership in a convex error body. In particular, `||v||_infinity` is exactly
the supremum of `lambda^T v` over `||lambda||_1<=1`. The candidate uses the
correct induced unit tolerance; the loss occurs when separate formulation
minima are used as the joint complexity statistic. It does not rule out
methods using several scalarizations together, adaptive scalarizations,
or common partitions chosen from full vector information.

Searches for simultaneous convex interpolation, vector-valued piecewise
linear approximation, common knots, and MICP residue obstructions produced
no direct matching statement. Much of the literature using "simultaneous
approximation" instead concerns interpolation together with derivative
approximation, common approximation spaces, or Pareto sets. Those results
should not be treated as matching common-input graph approximation without
checking their definitions.

## Recommended use and remaining limits

This is best retained as a supporting counterexample explaining why the
scalar-sum and independent-output arguments do not automatically extend
to arbitrarily many nonlinear outputs sharing an input. Its strength is
the simultaneous failure of all exact-graph midpoint tests and all separate
normalized linear-scalarization integer-count tests, witnessed by positive
monomials and a simple non-midpoint residue argument.

The example does not establish hardness of computing the best formulation,
does not resolve an additive binary-versus-general-integer gap, and does
not preclude an algorithm within a constant of the true joint minimum.
Its upper formulation may use real coefficients. Degree and output count
both grow; there is no fixed-degree or fixed-output impossibility claim.
The sparse encoding is much shorter than the dense encoding, so any later
running-time interpretation must state its encoding separately. A bounded
source search supports a qualified novelty assessment, not a priority claim.
