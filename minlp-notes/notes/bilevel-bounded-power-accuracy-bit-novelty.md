# Source assessment: bounded-power follower optimization in accuracy bits

Date: 2026-09-05. This is a bounded source audit of
`results/bilevel-bounded-power-accuracy-bit-algorithm.md`, not an independent
proof review. No matching theorem was identified in the checked sources.
That conclusion is provisional and is not a claim of exhaustive priority.

## Precise scope being compared

The reviewed result fixes the leader dimension and takes integer powers
at most `P` in separable strictly convex unit-box follower costs. Its upper objective is
an arbitrary signed affine function of the leader and follower response.
The leader domain is a rational polytope; no upper constraint depends on
the follower response. It returns a rational feasible leader and an
additive `2^(-B)` value guarantee in polynomial input size and **B**.
The final running time is polynomial in input bits, **B**, and the numerical
value **P**. Thus fixed powers and unary/dense growing powers are covered;
polynomial dependence on `log P` is not claimed. Numerical coefficient
magnitudes otherwise enter through their encoding lengths. This numerical-P
extension passed two independent proof reviews before promotion.

## Closest general optimization predecessor

Antoine Vigneron's *Geometric Optimization and Sums of Algebraic Functions*
(SODA 2010; ACM Transactions on Algorithms 10(1), Article 4, 2014,
[DOI](https://doi.org/10.1145/2532647)) is the closest predecessor.
The [author manuscript dated October 21, 2011](https://antoinevigneron.github.io/manuscripts/rational.pdf)
was retrieved and read directly; a local copy is
`literature/vigneron-2011-algebraic-sums-manuscript.pdf`.
Section 2.1 defines nonnegative, bounded, constant-description algebraic
terms and a constant-description semialgebraic domain. Theorem 6 gives
maximization and Theorem 9 gives minimization schemes, polynomial in
`1/epsilon`. Section 3.2 uses approximate sum evaluation to avoid exact
root-sum comparison. Section 2.3 states a real-RAM model with constant-cost
algebraic predicates, then explicitly says a bit-complexity model preserves
the FPTAS with a polynomial factor in coefficient bits, input size, and
`1/epsilon`.

Thus algebraic-sum approximation and its bit-model feasibility are prior
results. The candidate's distinction is the special clipped-root family,
signed affine objective, and polynomial dependence on **accuracy bits**,
with explicit rational feasible output. This is not a literal improvement
of the displayed real-RAM running-time bound in the same model. Shifting
signed terms to become nonnegative also does not change an FPTAS into an
accuracy-bit algorithm.

## Established ingredients and a different convex case

Sivan Toledo's [*Maximizing Non-Linear Concave Functions in Fixed Dimension*](https://www.tau.ac.il/~stoledo/Pubs/concave.pdf)
was read directly. Its abstract and Sections 1--2 assume a concave
piecewise-polynomial objective and a polynomial-sign evaluation/separation
algorithm, with fixed degree in the stated evaluator model. It develops
parametric search and real-algebraic tools, counting arithmetic operations.
The arbitrary signed clipped-root sum need not be concave or convex, so
that theorem does not directly settle the present model. The source is
nevertheless an antecedent for fixed-dimensional piecewise-polynomial
optimization, not evidence that this underlying method is new.

Binomial approximation on geometric intervals, sign-cell enumeration,
fixed-variable quantifier elimination, algebraic sampling, and rational
simplex rounding are established tools. The real-algebraic import should
retain its explicit bit-complexity qualification; see the checked
source discussion in `notes/bilevel-fixed-aggregate-response-novelty.md`
and its [Basu--Pollack--Roy manuscript](https://www.math.purdue.edu/~sbasu/jacm95.ps).
The new proof's elementary dyadic approximation is self-contained and
does not need an unqualified black-box algebraic-function oracle.

## Assessment and limits

The defensible contribution is an explicit accuracy-bit algorithm for
this restricted response family, including many follower coordinates and
rational feasible leader recovery. It is a combination theorem using
classical approximation and fixed-dimensional algebraic optimization.
It should be presented with Vigneron's more general FPTAS as the closest
comparison, rather than as the first optimization method for sums of
algebraic functions.

Exact root-sum threshold comparison remains outside the theorem. The
numerical-power dependence also matters to rational output size: the result's
growing-power example uses two different powers, `p` and `p/2`, and forces
an exponentially small positive rational leader at fixed additive
accuracy. It does not establish the same obstruction when all follower
powers are equal. No claim for response-dependent upper constraints or
variable leader dimension follows from this audit.

Queries included combinations of "sum of algebraic functions", "fixed
dimension", "approximation", "polynomial", "root", and "bilevel";
the Vigneron and Toledo primary manuscripts were the closest sources
found. Absence of a matching indexed theorem is only bounded evidence.
