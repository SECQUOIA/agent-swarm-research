# Prior-art comparison: strong point approximation for convex optimization

Date: 2026-10-02. This note compares the candidate in
[`convex-point-radical-comparison.md`](../new-direction/convex-point-radical-comparison.md)
with primary sources already read in the local literature KB. It is a scoped
comparison, not publication-priority clearance. The source note's independent
proof review has passed; this audit does not make a publication-priority
claim.

## Candidate and strongest precedent

The candidate gives a polynomial reduction from positive-integer
Square Root Sum (SRS) to finding a point within distance `1/4` of the
optimizer of a rational, jointly convex quartic over a rational box. On
instances where equality has been handled, the optimizer is unique. The
degree is four, coefficients and coordinate widths are bounded by absolute
constants, and the primal interaction graph has treewidth at most two. Thresholding one
coordinate of any such approximate point decides the SRS instance. Therefore
a deterministic polynomial-time point-output algorithm for this class would
put SRS in P; an always-correct expected-polynomial-time point algorithm
would yield a zero-error randomized expected-polynomial-time SRS algorithm.
These are conditional implications, not hardness or class-separation
results. The candidate's exact dimensions, construction, and limitations are
in its Sections 1–5.

The closest conceptual predecessor is Etessami and Yannakakis's distinction
between *weak* and *strong* approximation of fixed points. Their strong
approximation task asks for a point near an actual solution, while a weak
approximation may only have a small residual. Their Theorem 4 proves that SRS
reduces in polynomial time to constant-gap approximation of a distinguished
coordinate of a Nash equilibrium, even for unique equilibria: for four
players the coordinate is exactly 0 or 1, and for three players the gap is
0 versus greater than `1-ε` for any fixed positive `ε` (indeed also for
exponentially small `ε`). This is a very close precedent for the *output
contract and reduction pattern*. It does not subsume the candidate's
optimization class: Nash equilibria are solutions of a nonlinear fixed-point
or complementarity system, not minimizers of an explicit convex polynomial
with a bounded-width primal interaction graph. See Etessami–Yannakakis, “On the Complexity
of Nash Equilibria and Other Fixed Points,” [DOI
10.1137/080720826](https://doi.org/10.1137/080720826), the weak/strong
distinction in §1, printed pp.2–4, and Theorem 4, printed pp.21–24
([[etessami2010-on-the-complexity-of-nash]] p.2-4, p.21-24).

This precedent means that the general claim “constant-accuracy output of an
actual solution can be harder than a residual or value approximation” is
established. The candidate's scoped comparison is the transfer of that
phenomenon to a particularly structured convex polynomial minimizer, with
fixed treewidth and bounded numerical data. The project’s earlier cubic
construction only encoded SRS into *exact active-bound recognition*; the
quartic candidate strengthens that output implication to constant-distance
approximation of the entire optimizer.

## Weak objective approximation is a different contract

The classical ellipsoid-oracle framework explicitly separates these tasks.
Grötschel, Lovász, and Schrijver define weak optimization of a convex body as
returning a rational point that is nearly feasible and nearly maximizes the
specified linear functional (Problem 2.1.10, printed p.50). Their weak
constrained convex-function minimization problem returns an almost-feasible
point whose function value is within the requested tolerance of the minimum
on an eroded domain (Problem 2.1.22, printed p.56). Theorem 4.3.13 gives an
oracle-polynomial algorithm under weak-membership and function-value-oracle
hypotheses (printed p.114). For the candidate's rational box and explicitly
computable convex polynomial, the box and exact rational gradients supply
the usual separation/value oracles; applying this theorem is an inference
from its hypotheses, not a theorem about the candidate stated in the book.
These weak guarantees control objective value, not Euclidean distance to a
minimizer. See [*Geometric Algorithms and Combinatorial
Optimization*](https://doi.org/10.1007/978-3-642-97881-4), Problems 2.1.10
and 2.1.22 and Theorem 4.3.13 ([[groetschel1988-geometric-algorithms-and-combinatorial-optimization]]
p.50, p.56, p.114).

For a feasible point and a known quadratic-growth modulus `g>0`, an objective
gap `δ` does imply distance at most `sqrt(δ/g)` from a unique minimizer. The
candidate deliberately has no input-uniform growth guarantee: at the
optimizer, the `y` curvature is
`2η((t_+*)²+(t_-*)²)` and may be very small (candidate Eq. (10)). Thus
ordinary polynomial-precision value optimization does not supply the
constant-accuracy point required by the reduction. This distinction is
consistent with the usual SRS gap issue: precise value or coordinate
comparison can require more precision than a polynomial-time objective
approximation promises. The 2024 Subspace Theorem bound improves separation
for a fixed radicand set but has a nonexplicit constant, and does not give an
effective polynomial-bit separation guarantee for general binary instances
(Eisenbrand, Haeberle, and Singer, “An Improved Bound on Sums of Square Roots
via the Subspace Theorem,” [DOI 10.4230/LIPIcs.SoCG.2024.54](https://doi.org/10.4230/LIPIcs.SoCG.2024.54),
abstract and §1, [[eisenbrand2024-an-improved-bound-on-sums]] p.1-2).

The phrase “strong optimization” should be used carefully here. In GLS,
*strong optimization* means exact linear optimization over a represented
convex body; it does not mean the strong, metric approximation of an actual
solution used by Etessami–Yannakakis or by this candidate. State the output
contract explicitly: value-gap approximation, point-distance approximation,
exact coordinate/active-set decision, and compact implicit representation
are distinct tasks.

## Exact and algebraic point output

General real-algebraic methods give a baseline when dimension is fixed, not
when the number of variables grows and only treewidth is fixed. Renegar's
quantifier-elimination theorem has a complexity bound exponential in the
quantified dimension (and doubly exponential in the number of quantifier
blocks); it provides exact sign/feasibility descriptions but does not imply
polynomial-time coordinate recovery for the candidate's variable-dimensional
instances ([[renegar1992-on-the-computational-complexity-and]] p.1-5,
p.20-24). This is an algorithmic upper-bound comparison, not an obstruction
for convexity or bounded treewidth.

Bienstock, Del Pia, and Hildebrand study polynomial-bit rational witnesses
and near-feasible certificates for polynomial optimization. Their negative
results concern whether rational feasible points of reasonable encoding
size exist or can be recognized, while their positive algorithms are
dimension-sensitive. They do not assert hardness of constant-distance
approximation to the unique minimizer of a convex polynomial, nor do they
establish an exact algebraic optimizer-output algorithm for variable
dimension ([[bienstock2023-complexity-exactness-and-rationality-in]]
p.1-4, p.16-19). They are relevant background on bit-model output
contracts, but are not a direct predecessor to this reduction.

Etessami and Yannakakis also show that Nash is FIXP-complete for exact,
decision, strong-approximation, and partial-computation variants (Theorem
18). This broad solution-representation framework contextualizes the
coordinate-output task, but no cited FIXP theorem specializes to convex
polynomial minimization over boxes or to bounded treewidth
([[etessami2010-on-the-complexity-of-nash]] p.38-43).

## SRS source boundary

SRS itself remains the established arithmetic comparison problem: given
positive binary integers `a_i` and an integer `B`, decide whether
`Σ_i sqrt(a_i) ≤ B`. The project’s existing source audit covers its
relationship to exact geometric length comparison, the counting-hierarchy
upper bound, zero testing, and known separation-bound methods
([`convex-active-set-radical-prior.md`](convex-active-set-radical-prior.md)).
Those results support the source problem and its unresolved bit-complexity
boundary; they do not give the convex-quartic reduction. The new candidate
handles equality by integer-square tests, so its point-output reduction does
not assume a signed-sum-to-threshold equivalence.

The strongest source-level novelty boundary supported here is therefore:

- **Established:** SRS-hardness of constant-accuracy strong approximation to
  an actual solution coordinate in nonlinear fixed-point/equilibrium
  problems; polynomial-time weak optimization of convex objectives under
  standard oracle hypotheses; exact real-algebraic algorithms with
  dimension-sensitive complexity.
- **Not supplied by those sources:** the same SRS reduction to a constant
  point-distance approximation of the unique global minimizer of a jointly
  convex, bounded-width rational polynomial over a box.
- **Not concluded:** NP-hardness, impossibility of polynomial-time
  optimization, hardness of objective-value approximation, or a lower bound
  on the compact representation of the optimum. Any point-oracle consequence
  remains conditional on the open complexity of SRS.

No new source or KB ingestion was needed; all cited primary texts above are
already available and marked read in the local literature KB.
