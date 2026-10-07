# Independent review of the polynomial pruned-grid extension

Date: 2026-10-02. Status: passed mathematical and input/bit review. Reviewed
the complete [extension](../new-direction/polynomial-pruned-grid-extension.md)
against Sections 2--7 of the actual
[pruned-grid theorem](../new-direction/pruned-coordinate-grid.md). This is
a review of the stated algorithmic corollary, not an implementation test
or a priority assessment.

**Verdict.** No substantive gap was found. Explicit fixed-degree rational
polynomial factors admit the same certified mixed-box approximation bound.
On native integer boxes, the original objective's value lattice converts
that approximation into exact optimizer discovery. Both running-time
claims require the stated point quadratic growth and use the curvature
bound actually verified on the continuous box hull.

## Arithmetic proof and domain filtering

The predecessor already states its arithmetic extension to exactly
evaluable coordinate-semiconcave factors. Its key inequality remains valid
for polynomial interactions: condition successively on the independent
coordinate roundings and apply the one-dimensional upper-curvature bound.
The resulting expected increase is at most one half of `L` times the sum
of coordinate variances. Each endpoint's unary correction covers its
interval's contribution. Unit integer intervals need no correction because
their feasible points are already endpoints.

The same argument gives each interval's conditional lower bound from its
two endpoint min-marginals. It does not require the remaining coordinates
to interact quadratically. Consequently filtering preserves every optimizer,
the incumbent, and the next center. The complete successful trial's
filtering history is necessary: the last restricted-box DP alone would
not certify the original domain. The extension retains this history and
uses the nonincreasing incumbent correctly.

The contraction and retained-domain calculations use only this lower
bound, the geometric mesh inequality, and point growth. No quadratic
identity is hidden in their reuse. In particular, the additional unit
radius for retained integer intervals is present. The unknown-growth
algorithm caps coordinate grids before allocating tables, so unsuccessful
trials cannot introduce an accuracy exponent depending on bag size.

## Exact arithmetic and integer output

I checked the inherited common-denominator induction. Within a trial,
old centers and clipped endpoints have denominators dividing the next
stage's `A_j`; the explicit geometric displacement has the same property.
Degree changes the evaluation denominator from a square to `A_j^d`,
not the grid denominator itself. All polynomial factor values and unary
corrections therefore share the displayed `8 D A_j^max(d,2)` denominator.
DP messages sum and select these quantities, so tree depth does not
multiply unrelated denominators. Explicit fixed degree makes the value
heights and evaluation work fit the claimed parameterized bit bound.

For a wholly native-integer input, the original coefficient denominator
`Q` satisfies `Q F(x)` integral at every feasible point. An incumbent
with certified gap strictly below `1/Q` is consequently exactly optimal,
regardless of uniqueness or growth. The latter assumptions are used only
to bound the discovery work. The choice
`q = 1 + ceil(log2 Q)` supplies a strict gap using only input-polynomial
accuracy bits. Neither refined grid denominators nor a rational-height
bound for optimizers enters this exactness argument.

The result is an actual discovery algorithm: a proposed optimizer is not
part of its input. With ties the acceptance rule remains valid, but the
point-growth parameter bound is not available. The extension also correctly
omits continuous exact output; a cubic with optimizer `sqrt(2)` already
prevents direct reuse of rational-QP reconstruction.

## Material scope and significance

The curvature inequality must hold between lattice labels, on the full
continuous hull. The explicit monomial interval verifier is a sufficient
polynomial-time certificate, although it can overestimate curvature and
worsen the parameter. Alternative certificate data and polynomial
verification work must be counted. Factor scopes, rather than sparsity
of a Hessian evaluated at one point, determine the supplied decomposition.

The native-integer scope is deliberate. Rescaling unequal physical lattice
steps can worsen the curvature/growth ratio; preserving that ratio needs
the separate grid and denominator audit listed in the extension. This
review does not silently establish that further result. Binary-encoded
unbounded exponents and arbitrary arithmetic circuits are also outside
the displayed bit claim.

This is a finite-bit and exact-integer consequence of the local pruned-grid
theorem's already stated semiconcave arithmetic generality. It adds a
deterministic nonlinear optimization consequence beyond quadratic input,
but introduces no new filtering or rounding algorithm. It should be
presented at that level rather than as an independent mechanism.

## Verification record

This review checked the actual mathematical files and their displayed
constants and denominator formulas. A scoped Python document check verified
local links, trailing whitespace, and paired display-math delimiters in
this review and the extension. No additional optimization executable,
project-wide check, CI inspection, external search, or index edit was run
for this review. The separately reviewed nonlinear shell checker exercises
higher-degree factor evaluation and rounding, but is not a test of this
pruned-grid optimizer.
