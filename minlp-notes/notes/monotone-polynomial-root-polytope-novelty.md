# Monotone polynomial roots over polytopes: source assessment

Date: 2026-09-05. Focused primary-source assessment by
`joint_flow_novelty` of the complete
[candidate theorem](monotone-polynomial-root-polytope-optimization.md).
Mathematical audits are separate.

No exact matching theorem was found for the stated combination: a dense
univariate polynomial affine in unrestricted-dimensional polytope data,
a promised unique strictly increasing root on a supplied bracket, and
polynomial-bit recovery of both a rational optimizing vertex and its exact
real-algebraic root. This is a bounded search finding, not established
priority. The result should be presented as an explicit arithmetic refinement
of classical quasilinear optimization and decision-to-optimization methods.
Its standalone novelty is plausibly modest.

## Quasilinear structure explains the elementary mechanisms

Our direct comparison identifies the root map as quasilinear. For every
threshold `z` in the supplied bracket,

```
{theta in P: q(theta)<=z} = {theta in P: H(z,theta)>=0},
{theta in P: q(theta)>=z} = {theta in P: H(z,theta)<=0}.
```

Both are affine halfspace intersections with `P`. Thus both quasiconvexity
and quasiconcavity hold. Their standard convex-combination inequalities
already imply that a point's root lies between the minimum and maximum
vertex roots. Neither vertex attainment nor scalar LP threshold tests are
new consequences to advertise separately.

Akshay Agrawal and Stephen Boyd,
*Disciplined quasiconvex programming*, Optimization Letters 14 (2020),
1643–1657, [primary author copy](https://web.stanford.edu/~boyd/papers/pdf/dqcp.pdf),
Section 2.1 records the quasiconvex and quasiconcave convex-combination
inequalities. Section 3, printed p.1649/PDF p.7, reduces a quasiconvex
problem with a known value bracket to convex feasibility bisection, stopping
at a requested additive error. These sections and the linear-fractional
example in Section 2.3 were read. The paper itself credits older
quasiconvexity and fractional-programming literature.

Comparison: its method gives the candidate's threshold-bisection framework,
but the inspected statement does not supply exact algebraic output or the
finite precision at which an exact rational vertex can be recovered. The
candidate's root map need not be differentiable: `H(q,theta)=q^3-theta`
already gives a cube-root map. It is therefore safer to use the established
term *quasilinear* than silently invoke a differentiable pseudolinear theorem
whose assumptions may fail.

## Fractional programming and parametric search are close predecessors

Nimrod Megiddo, *Combinatorial Optimization with Rational Objective
Functions*, Mathematics of Operations Research 4 (1979), 414–424,
[primary author copy](https://theory.stanford.edu/~megiddo/pdf/rational.pdf),
Section 2, printed pp.415–417/PDF pp.2–4, gives a decision-to-optimum
algorithm for an affine ratio using an algorithm for linear optimization.
Its theorem assumes a bounded number of additions and comparisons. The proof
simulates those comparisons parametrically, identifies the relevant parameter
interval, then solves an equation for the optimal value and recovers an
optimizer. That complete theorem and proof were read.

Comparison: degree one in the candidate is ordinary linear-fractional
programming, since strict increase makes the affine coefficient of `q`
positive. The general idea of recovering an exact optimum from parametric
linear optimization is also old. Megiddo's specific theorem does not directly
state the dense variable-degree root result for an arbitrary rational
H-polytope and a generic bit-polynomial LP algorithm. In particular, invoking
its arithmetic-operation hypothesis for any polynomial-time LP algorithm
without checking the operations would be unjustified. The candidate instead
uses ordinary rational bisection plus a uniform algebraic separation bound.

This difference does not by itself establish a novel paradigm; it explains
why the short explicit recovery argument is useful. The 2025 survey of
linear-parametric optimization was used only to locate primary references,
not as authority for a blanket parametric-search theorem.

## Real interval roots and the complex-root Edge Theorem

Eldon R. Hansen and G. William Walster, *Sharp Bounds on Interval Polynomial
Roots*, Reliable Computing 8 (2002), 115–122, develops sharp real-root
enclosures for independent interval coefficients. The introduction and
Section 3, printed pp.121–122, were read in the openly displayed
[primary article text](https://www.researchgate.net/publication/220252983_Sharp_Bounds_on_Interval_Polynomial_Roots).
Section 3 reduces interval-root endpoints to roots of four endpoint-coefficient
polynomials, separating positive and negative arguments. The quadratic
discussion also explicitly uses coefficient monotonicity in applicable cases.
Some overbar notation is degraded in the displayed extraction; no detailed
formula was imported from that extraction.

Comparison: sharp endpoint roots under interval uncertainty are known.
Independent monomial coefficients permit especially simple envelope
polynomials. The candidate allows arbitrary correlated polyhedral data and
affine combinations of dense polynomials. Its LP envelope can change active
vertices as the root parameter varies. The checked interval source does not
give the unrestricted-polytope exact optimizer bit guarantee.

A. C. Bartlett, C. V. Hollot, and Huang Lin,
*Root locations of an entire polytope of polynomials: It suffices to check
the edges*, Mathematics of Control, Signals and Systems 1 (1988), 61–71,
[primary publisher page](https://link.springer.com/article/10.1007/BF02551236),
describes exposed-edge testing for root locations of a polynomial polytope.
Only the publisher abstract was accessible in this audit; the full article
was subscription content and was not bypassed.

Comparison: that general root-location problem concerns the complex roots
of a family. The candidate selects a single monotone real branch in a
common bracket. Its vertex argument neither replaces nor strengthens the
general Edge Theorem. Also, existence of an edge or vertex criterion does
not itself give polynomial runtime for an H-polytope with exponentially many
edges or vertices. No claim about the original article's precise runtime
model is made without its full text.

## Exact recovery: useful bookkeeping using classical algebra

The candidate's essential extra step is this: all vertex polynomials have
uniformly bounded degree and coefficient height, even though their number
can be exponential. A lower bound on the distance between distinct roots
of any pair therefore has polynomial encoding length. Once LP bisection
narrows the optimal-root bracket below that bound, a vertex optimizing the
appropriate rational endpoint LP must have exactly the optimal root.
Ordinary root isolation of this one vertex polynomial finishes the task.
No derivative lower bound or exact LP at an unknown algebraic parameter is
required.

This is our reading of the candidate, not a theorem attributed to a new
source. Its ingredients are established. Theorem 1.2 in the primary paper
[*A new bound on cofactors of sparse polynomials*](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/new-bound-on-cofactors-of-sparse-polynomials/2CADDB77D2E5CBFB7B803CCCAC49D2FD)
explicitly reproduces Mignotte's integer-factor bound and attributes it to
his 1974 Theorem 2; that statement was checked, but the original Mignotte
proof was not read here. Sagraloff and Mehlhorn,
[*Computing Real Roots of Real Polynomials*](https://arxiv.org/pdf/1308.4088),
Theorem 3/36, provides polynomial-bit isolation and refinement for integer
polynomials after squarefree preprocessing, as already checked in the
repository's scalar precision source assessments and reopened here.

Keep the result's promises explicit: bounded nonempty rational polytope,
supplied bracket, uniform strict increase and bracketing signs, dense degree
encoding, and one branch. It does not validate monotonicity, handle arbitrary
complex roots, or give a strongly polynomial algorithm. Piecewise-polynomial
flow laws need their own breakpoint argument.

Recommended positioning: “A classical quasilinear LP-bisection reduction,
together with uniform algebraic separation, gives an explicit polynomial-bit
method returning an exact rational optimizing vertex and its algebraic root.
We did not locate this precise arithmetic statement in the primary sources
checked.” It is appropriate as a supporting theorem for correlated passive
flow design; a broad abstract novelty claim remains unwarranted.
