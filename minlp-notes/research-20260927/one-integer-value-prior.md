# Prior-art audit: one unbounded integer variable

Date: 2026-09-28. Scope: exact feasibility and finite-infimum recovery for
rational quadratic systems with one integer variable, arbitrary continuous
dimension, and fixed span dimension of the continuous constraint Hessians.
The corresponding explicit rational MISOCP case is also considered.

No equivalent published theorem was identified in the sources examined.
This search does not establish priority. The one-dimensional tail argument
uses classical semialgebraic geometry. The candidate contribution is the
quantitative combination: small individual projection polynomials despite
arbitrary affine rows and continuous dimension, then exact optimization
with an unbounded integer variable, including finite infima that are not
attained. The relevant proof review is
[one-integer-value-review.md](one-integer-value-review.md).

## Closest results and precise differences

### Grigoriev--Pasechnik: sampling and announced optimization

[Grigoriev and Pasechnik, *Polynomial-time computing over quadratic maps I:
sampling in real algebraic sets*](https://arxiv.org/pdf/cs/0403008),
Theorem 1.2, computes samples meeting every connected component of
\(Z(p(Q(x)))\), where \(Q\) has \(k\) quadratic components. Degrees
and integer coefficient bits are controlled by \((dn)^{O(k)}\), with
the coefficient bound multiplied by input bit size. Theorem 1.5 states
exact minimization, minimizer computation, and computation of an
unattained infimum for an objective in the same quadratic map; its proof
is deferred to a continuation.

These are substantial precedents. Neither statement permits an arbitrary
number of additional affine inequalities without accounting for them.
Introducing a separate square slack or map coordinate for each affine
row destroys a fixed-map-count argument. The
[existing minimum-face audit](nonconvex-hessian-span-prior-audit.md)
already derives fixed-Hessian-span feasible certificates from Theorem 1.2.
Thus that continuous certificate result should not be counted again as
an original part of the one-integer extension. The source does not state
the one-integer theorem considered here.

### A recent explicit precedent for compressed formulas with parameters

[Kamminga and Rudolph, *The Pure-State Consistency of Local Density
Matrices Problem*, ITCS 2026](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.83/LIPIcs.ITCS.2026.83.pdf),
Theorem 5.2 and equations (24)--(26), express Grigoriev--Pasechnik critical
pieces and limiting feasibility using few quantified variables.
Remark 5.3 explicitly allows coefficients in \(\mathbb Z[C]\), treating
\(O(k)\) real parameters symbolically. Hence neither reduction to few
variables nor symbolic parameter treatment is new in itself.

Definition 1.14 and Theorem 1.15 give parallel approximation of a minimum
and an optimizer for a bounded quadratic-map zero set. Immediately after
Theorem 1.15, the authors say that a proof of the unbounded optimization
statement in Grigoriev--Pasechnik is not available to their knowledge.
Their result is not a theorem for arbitrary affine rows and one unbounded
integer variable. Its parameterized formulas are nevertheless an important
comparison for the present compression argument. This audit did not
independently verify all details of their limit construction.

### Basu--Pollack--Roy: degree and height versus formula size

[Basu, *Algorithms in real algebraic geometry: a survey*, Theorem 2.27,
printed page 16](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf)
states the block-sensitive quantifier-elimination bound used here. For
block sizes \(k_1,\ldots,k_\omega\), input degree \(d\), and
coefficient bits \(\tau\), individual output degrees are bounded by
\(d^{O(k_\omega)\cdots O(k_1)}\). Output coefficient bits are
bounded by the same type of factor, including free-variable dimension,
times \(\tau\). Neither bound contains the input predicate count.
The formula size and construction time do depend on that count.

This separation is established machinery. It is exactly why an
exponentially large compressed Boolean matrix can still establish small
individual boundary polynomials. It does not license constructing that
matrix or its quantifier-free equivalent in polynomial time. The
optimization algorithm must use the bounds with its separate feasibility
oracle. Applying general elimination directly to all original continuous
variables would instead retain an ambient-dimension exponent.

### Khachiyan--Porkolab: convex integer optimization

[Khachiyan and Porkolab, *Integer Optimization on Convex Semialgebraic
Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Theorems 1.1--1.2, allow a convex set given by a quantified real formula.
Theorem 1.1 bounds the binary length of an optimal integer vector when
an optimum exists. Theorem 1.2 gives polynomial time when the total
number of free and quantified variables is fixed; its formula-size
dependence remains material.

The problem they optimize has an integer objective coordinate. An affine
objective involving continuous variables cannot be made such a coordinate
while preserving its exact real infimum. A finite infimum may be irrational
or unattained. Their theorem therefore does not directly settle the
present value problem. It is a major ingredient of the separately proved
MISOCP feasibility oracle. In the nonconvex one-integer case, univariate
root bounds provide small feasible integer coordinates without a convex
projection assumption; this is a classical one-dimensional simplification,
not an extension of their theorem to arbitrary nonconvex sets.

### Earlier algorithms specifically for one integer variable

[Baes, Oertel, Wagner, and Weismantel, *Mirror-Descent Methods in
Mixed-Integer Convex Optimization*](https://arxiv.org/pdf/1209.0686),
Section 4.1 and Proposition 4, give approximate bisection for the convex
function obtained by minimizing over the continuous variables. In the
arXiv v1 text, Remark 4 on printed page 27 applies this to mixed-integer
optimization assuming a known bounded interval for the integer variable,
finite objective spread, and an oracle approximating each continuous
slice to accuracy \(\gamma\). The resulting improvement oracle has an
additive error proportional to \(\gamma\). The preceding discussion
also assumes exact identification of the feasible interval when needed.

This source establishes the general strategy of optimizing a univariate
convex value function through slice oracles. It does not provide a bit
bound on a truncation for an unbounded integer variable, an algebraic
finite-infimum bound, or exact recovery of an unattained value. Those
are the relevant differences, rather than the use of bisection itself.

### Projection topology is a related but different guarantee

[Basu and Zell, *On Projections of Semi-algebraic Sets Defined by Few
Quadratic Inequalities*](https://arxiv.org/pdf/math/0602398),
Theorem 1.2 and the following algorithmic result, bound and compute the
first few Betti numbers of projections of compact sets defined by a fixed
number of quadratic inequalities. The introduction and conclusion
explicitly distinguish this from constructing a quantifier-free
description of the projection.

Their results do not give the coefficient-height or finite-value bound
needed here. Conversely, an individual-polynomial bound proved using an
exponentially large formula does not solve the efficient explicit
projection-description problem discussed there. The historical open
question in that paper is not asserted here to remain open today.

### Strict subclasses and practical exact algorithms

[Del Pia, *Convex quadratic sets and the complexity of mixed integer
convex quadratic programming*](https://arxiv.org/abs/2311.00099),
Theorem 3, gives fixed-parameter tractability in the integer dimension
for a convex quadratic objective over a mixed-integer rational polyhedron.
The continuous dimension need not be fixed. Its linear constraints are
a strict restriction relative to general MISOCP or nonconvex quadratic
constraints. This is stronger prior algorithmic work for that subclass,
not an equivalent general result.

[Coey, Lubin, and Vielma, *Outer Approximation With Conic Certificates
For Mixed-Integer Convex Problems*](https://arxiv.org/abs/1808.05290),
Sections 2.1 and 2.3, establish a conic outer-approximation framework under
assumptions including finite integer bounds and well-posed primal-dual
subproblems. Its finite-termination theorem does not cover the unbounded
integer/nonattainment cases at issue here. A future practical algorithm
could combine certified truncation or value bounds with such methods;
the current theory alone does not establish a speed improvement.

## How the contribution should be described

For a semialgebraic epigraph in the \((z,t)\)-plane, eventual monotonicity
of a finite endpoint branch is classical; see the monotonicity theorem in
[van den Dries, *O-minimal Structures and Real Analytic Geometry*,
printed page 116](https://archive.intlpress.com/site/pub/files/_fulltext/journals/cdm/1998/1998/0001/CDM-1998-1998-0001-a004.pdf).
Consequently, sufficiently far
out on either integer tail, its infimum agrees with the corresponding
continuous-tail infimum. Finite limits of rational algebraic branches are
algebraic. None of these qualitative facts should be claimed as a new
discovery.

What needs a proof specific to this problem class is a truncation and a
finite-value degree/height bound polynomial in the original input for
fixed continuous Hessian span, without expanding all affine cases or
assuming an attained fiber minimum. The argument must keep open fibers,
empty fibers, and fibers with infimum minus infinity distinct. It must
also bound each exceptional polynomial separately, since multiplying the
entire exceptional family could lose the desired coefficient bound.

The nonconvex complexity claim is NP feasibility and exact value recovery
with an NP oracle, not deterministic polynomial time. Even with an unused
integer variable, Hessian span one includes the known Boolean-forcing
nonconvex feasibility construction. Deterministic polynomial-time claims
here require the explicit convex conic representation and its separately
proved exact feasibility oracle.

The best-supported current description is a quantitative extension and
combination of established algebraic and optimization tools. A claim of
priority for the combined theorem remains provisional; no identified
source states the same assumptions and conclusion.

## Search and verification record

The audit inspected the source statements above, the local
Grigoriev--Pasechnik text, the local Khachiyan--Porkolab full text, and the
existing Hessian-span prior audits. Web searches included the phrases
“one integer variable” with convex optimization, polynomial time,
unboundedness, and quadratic programming; one-integer semialgebraic
optimization; parametric quadratic maps; and projection or quantifier
elimination for few quadratic inequalities. A 2003 Pasechnik slide deck
on parametric quadratic solving was located, but its full text was not
retrieved successfully and no theorem is attributed to it here.

A separate subagent checked the one-integer oracle source and the Del Pia
and conic outer-approximation comparisons. The search found no equivalent
theorem; this is limited negative evidence, not a novelty certificate.
The targeted document check verified local links, math delimiter counts,
whitespace, control characters, and the final newline. No project-wide
verification or CI inspection was performed. This audit is not a proof
verification of the new theorem.
