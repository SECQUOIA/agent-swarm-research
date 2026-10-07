# Independent review of the direct-row theorem

Date: 2026-10-03. Reviewed
[`theory/row-aggregation.md`](../theory/row-aggregation.md), SHA-256
`fb6758fc222ab0f458dc1e7df2184e66e8883a7f6d1e41d7cdcaeef9667e66d8`.
This review checks the mathematical arguments in §§1–4. It does not verify
their integration code, certificates, performance, or the separate finite-net
claim mentioned in §5.

**Conclusion:** the principal theorem and rounding argument are correct.
The earlier clarification is resolved: the equality extension now explicitly
assumes continuity of `h`, so both `g` and `h` are continuous on compact `D`
and their joint graph is compact. The text also explicitly explains shared
coordinates through duplication and linear identification. I inspected both
corrections in the version identified above. No unresolved proof finding
remains in the reviewed scope.

## Validity and original-variable elimination

The source-row orientation and signs in (2) and (3) are correct. The lower
support bound is combined with an upper bound on the weighted nonlinear
sum. Inequality multipliers are nonnegative; equality multipliers are free.
Neither optimal multipliers nor a tight support value is required. The
objective epigraph and hypograph signs, including the objective constants,
are also correct.

Shared occurrences of a variable cause no mathematical difficulty if all
linear coefficients are collected once before export. The theorem's `(x,z)`
notation can accommodate §1's overlapping block/model coordinates by
temporarily duplicating `x`, then intersecting the result with
`x = selection(v)`. No independence of the actual model variables is needed.

## Completeness of the projected graph relaxation

I checked both inclusions independently. Compactness and continuity make the
graph compact; its finite-dimensional convex hull `K` is compact. Adding the
closed nonnegative cone preserves closedness because every convergent
sequence of sums has a subsequence whose `K` components converge, and the
remaining cone components then converge. Convexity and nonemptiness also
hold.

For a proposed point `p = (x,b-Lz)`, membership in `K + cone` is precisely
the existence of a graph-hull coordinate `y <= b-Lz`. Every finite lower
support of this sum has nonnegative coefficients on the cone coordinates.
Conversely, separation of an exterior point from a nonempty closed convex
set supplies a strict separating lower support with finite infimum, so it
necessarily has those signs. Minimizing its linear function over the graph
hull is equivalent to minimizing over the original graph. Substitution
therefore gives exactly (4), with no lost directions.

The zero multiplier vector is included. Consequently the family also imposes
membership of `x` in `conv(D)`, even if the graph hull has empty interior or
`D` is nonconvex. Unbounded `z` is harmless: the set in the theorem is the
inverse image of a closed set under a continuous affine map. No general
claim that arbitrary linear projections of closed convex sets are closed is
being used.

For equalities, the cone is zero on their graph coordinates; hence their
support coefficients are unrestricted. The proof carries over under the
now explicit joint graph compactness assumptions. Additional
linear restrictions can be intersected after this characterization. Doing
so characterizes the stated relaxation; it does not interchange
convexification and intersection with nonlinear constraints. The
`x^2 = 1/4` example correctly demonstrates that latter distinction.

## Floating-point correction

The error is `Delta = exported - exact`, so a lower row needs a lower bound
on `Delta^T v`. Formula (5) has the correct sign, and the right-hand side
must be rounded downward. Positive `Delta_j` requires only the lower
variable bound; negative `Delta_j` requires only the upper bound. A zero
delta requires neither bound. Thus an unbounded auxiliary coordinate is
admissible when its exported coefficient is exact.

The final documentation now distinguishes that mathematical sufficient
condition from the exporter's admission rule. I inspected the focused
coefficient-error branch in `solver/row_certificate.py`: zero error skips
correction, while nonzero error requires both bounds to be finite. This
conservative refusal is consistent with the theorem and is not a validity
bug. The additional documentation does not change the mathematical argument;
the earlier rounding diagnostics were therefore not rerun. This focused
inspection does not enlarge the review into a complete code audit.

The text correctly refuses a coefficient change when its needed bound is
missing, and correctly requires another correction after later coefficient
changes. These facts address coefficient rounding; they do not establish
the validity of unrecorded solver transformations or the solver's final
optimality claim.

As a diagnostic beyond the proof, a targeted Python `fractions.Fraction`
calculation checked 1,224 coefficient perturbations and rational points:
positive and negative `1/10`, `1/3`, and `1/7`, nearest and adjacent binary64
coefficients, four signed/degenerate intervals, and 17 points per interval.
It also checked both one-sided unbounded sign cases at finite points. All
checks passed. These finite calculations illustrate the formula; the
algebraic proof establishes it for all points.

No project-wide verification or CI inspection was performed.
