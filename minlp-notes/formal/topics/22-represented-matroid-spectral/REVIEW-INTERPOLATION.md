# Independent interpolation review

Date: 2026-09-22.

The reviewer read `Interpolation.lean`, `InterpolationExecution.lean`, and
`InterpolationTrace.lean`. The reviewer did not author those three modules.
This review covers exact coefficient reconstruction, the finite executable
calculation, and its recorded arithmetic. The reviewer authored
`InterpolationBits.lean` and `InterpolationTraceBits.lean`; those modules require
separate independent review.

The reviewed mathematical and executable interfaces are sound. The coordinate
nodes are the distinct rationals 1 through D+1. The one-variable Lagrange moment
identity is proved from the polynomial interpolation theorem. Factoring the
finite tensor sum gives the multivariate coefficient identity, with the required
coordinate degree bound explicitly stated. The proof uses coefficients of the
generating polynomial and therefore preserves the sum of contributions when
several bases share a profile. It does not incorrectly identify a profile with
one determinant term.

The zero-coordinate case is included: the function grid has one member, both
coordinate products equal one, and coefficient recovery returns the constant
polynomial's coefficient. D=0 is also included: the node list has one member,
its list of other nodes is empty, and its denominator product is one. The
executable coefficient query uses coordinates in `Fin (D+1)`, so every queried
coefficient lies inside the proved truncation range. No caller-supplied
interpolation oracle replaces the computation.

The numerator recurrence stores its previous row and computes the next row of
coefficients of a product of linear factors. Discarding coefficients above D is
valid: multiplying by a linear factor never makes a higher coefficient
contribute to a lower coefficient. The correctness theorem proves this directly
for every list of factors. The denominator is the product of differences from
all other nodes. Distinct nodes justify the Lagrange formula; rational totalized
division does not substitute for an unproved nonsingularity assumption.

The trace materializes numerator cells, coordinate weights, and grid terms.
The scalar product used by both a cell value and its subtraction event is now
explicitly cached as `product`. The traced value is proved equal to the
executable coefficient calculation. Its arithmetic-event count is exact,
including empty products and sums under the chosen expression evaluator.

The arithmetic trace intentionally excludes producing the supplied grid values,
constructing integer node literals, finite-list enumeration and sorting, and
list indexing. The assembled algorithm must account for those costs separately.
The trace module's own comment already separates grid-value production. This
review does not certify the whole algorithm's bit complexity or memory cost.

The targeted command
`lake build --wfail Formal.MatroidSpectral.ProfileGramExecution`
passed with the reviewed interpolation modules as dependencies, including the
explicit-product caching change. The final topic audit must include the resulting
sources. No project-wide or CI checks were run for this review.
