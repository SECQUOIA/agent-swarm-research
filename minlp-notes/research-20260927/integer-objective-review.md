# Independent review of integer-only quadratic objectives

Date: 2026-09-27. Scope: the section **Convex quadratic objectives in the
integer variables** of [the unbounded integer frontier note](unbounded-integer-frontier.md).
This reviewer did not develop that corollary. The review treats the previously
reviewed feasibility theorem and its common-chart formula as dependencies;
it does not independently reprove those results.

**Finding.** No gap was found in the saved corollary. For fixed integer
dimension and continuous Hessian span, its reduction establishes exact
optimization of a rational convex quadratic depending only on the integer
coordinates, including infeasibility and unboundedness classification. The
output guarantee is an optimal integer assignment and a rational objective
value, with existence of an exactly feasible continuous fiber.

## Imported theorem checked

The reviewer inspected the original openly accessible
[Khachiyan--Porkolab paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
especially its formula definition and Theorem 1.1 on printed pages 207--208.
The theorem applies to a convex semialgebraic set given by a Boolean
first-order formula and bounds an optimal integer point when one exists.
The objective is its last integer coordinate. The coordinate-size bound
depends on coefficient size, degree, free dimension, and quantifier-block
sizes, and does not contain the number of atomic predicates. The theorem
does not require closedness or full dimension. These are exactly the
features used in this corollary.

## Adversarial checks

1. **Scaling and attainment.** Clearing all actual polynomial coefficient
   denominators, including the constant and any displayed factor of one
   half, gives a positive integer scale (L) and an integer-coefficient
   polynomial (p=Lf). The product of the input denominators already gives
   a scale with polynomial bit length. Therefore the attainable values of
   (p) form a subset of the integers. If that set is nonempty and bounded
   below, it has a least element achieved by a feasible assignment. No
   compactness or continuous minimizer assertion is being substituted for
   this argument.

2. **Epigraph equivalence.** The new inequality (p(z)-w\le0) has a PSD
   full Hessian because (f) is convex and (L>0). It has zero Hessian in
   the continuous coordinates. Its intersection with the original integer
   projection times the real line is convex. Every feasible integer (z)
   permits the integer value (w=p(z)); conversely (w\ge p(z)).
   Consequently the minimum of integer (w) equals the minimum of (p),
   and every optimal pair has (w=p(z)). Using an inequality instead of an
   equality is necessary for convexity and creates no relaxation gap here.

3. **Uniform bound.** Adding the epigraph predicate to the common-chart
   formula adds one free integer coordinate and no quantified coordinates.
   Its degree and coefficient lengths remain polynomial in the full input
   length, including the objective. The imported theorem therefore gives
   the asserted conservative bound (B=2^{N^{O((h+1)(k+2)^4)}}) whenever a
   finite optimum exists. Its constants depend on the theorem, not on
   whether the particular instance is bounded. Thus choosing (B) before
   the boundedness query is valid.

4. **Unboundedness test.** After original feasibility is established, an
   unbounded objective admits a point below every finite threshold. A
   bounded objective attains its minimum and the optimal-pair bound places
   that minimum at least at (-B). Hence feasibility at threshold
   (-B-1) is equivalent to unboundedness below. Testing emptiness first
   avoids confusing an empty instance with a finite optimum.

5. **Exact search and returned assignment.** In the finite case, (-B-1)
   is an infeasible threshold and (B) is a feasible threshold. Integer
   bisection ends at consecutive thresholds after (O(\log B)) queries.
   Every appended threshold row has zero continuous Hessian and is jointly
   convex. Each query has polynomial encoding length for fixed parameters.
   A feasible integer assignment at the final threshold must attain it;
   a strictly smaller integer value would contradict the preceding
   infeasible threshold. Dividing by (L) gives the exact rational optimum.

The epigraph coordinate is used only in the size-bound proof. The actual
queries retain the original number of integer coordinates and the original
continuous Hessian span. The existence of irrational continuous fibers does
not affect this output guarantee.

## Limits and verification record

The proof uses the rationality and integer-only dependence of the objective.
It does not establish attainment, recovery, or unboundedness classification
for an objective involving continuous coordinates. Convexity of the
integer-only quadratic is required both by the epigraph witness argument
and by the exact feasibility theorem used for threshold queries.

The epigraph conversion and discrete bisection are established techniques.
Any originality in this consequence depends on the preceding Hessian-span
projection and feasibility results; this review does not establish priority
for that larger package.

Verification was symbolic proof review and inspection of the primary source.
An inline `python` check of this review file passed its final-newline,
control-character, trailing-whitespace, and local-link checks. This is a
document check only.
No numerical experiment, Lean proof, project-wide check, or CI inspection
was used or is claimed to validate the general corollary.
