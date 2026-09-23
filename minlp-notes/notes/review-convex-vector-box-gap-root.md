# Independent root review: exact ternary-versus-binary convex graph counts

Date: 2026-09-05. Verdict: PASS for the degree-32 polynomial construction
and its exact product counts in
[the candidate](convex-vector-one-bit-box-gap-investigation.md).
This review concerns the final A=7/4, c=1/48 version. It does not certify
an unbounded gap at fixed input dimension.

Both Q_1=A(1-x)^32 and Q_2=A x^32 are convex on [0,1]. The three rational
boxes contain the graph on their designated intervals. The outer boxes
have component widths A-L<1 and d<1; the middle has widths L<1.
Their labeled convex hull has only integer slices z=0,1,2. At z=1 the
outer weights must be equal, say t<=1/2. Consolidating points within each
box is valid because the boxes are convex. The input minimum is
c+t(1-3c)>=c, and the maximum is at most 1-c. Each admitted output is
between zero and max(L,(A+d)/2)<1, while each true output is between zero
and L<1. This establishes both exact-graph containment and strict unit
accuracy for every point of the integer slice, not just its vertices.

The displayed rational thirds-combination errors are greater than one.
For every pair of the three contacts, one of the two weights 1/3 and 2/3
therefore violates the tube. In n coordinates, any pair of the 3^n
product contacts differs in at least one coordinate and inherits that
violation. Equal residues modulo three would make that chosen convex
combination integral, giving p_conv>=n. The product of the one-integer
MILPs supplies equality. A shared binary assignment admits every convex
weight, so all product contacts require distinct binary assignments;
the finite disjunction of the 3^n box products matches that lower bound.
Thus p_bin=ceil(n log2 3), with no restriction on the comparison lift's
continuous dimension or integer range.

The binary upper is stated only with unrestricted finite size; this is
sufficient for the exact count theorem. The one-general-integer lift per
coordinate has constant rational encoding, so its product is compact.
Both polynomial degree and all numerical data are fixed independently of
n. The linear gap is in growing input dimension, not in fixed one-input
output dimension. Positive affine changes of output do not alter the
counts or errors, so monotonicity refinements can be stated separately.

Independent exact checker:
[check_box_gap_root.py](../code/positive_vector_obstruction/check_box_gap_root.py).
It verifies the rational constants, all 72 candidate middle-slice
vertices, 2,048 additional exact integer-slice mixtures, and all 390 pairs
of product contacts for n=1,2,3. Every check passed. These diagnostics
support the explicit inequalities; the general proof above covers all n.

No publication-priority claim is established by this review. The
modulo-three convex-lift obstruction, bounded disjunction, and product
encoding are classical mechanisms; the precisely restricted polynomial
family and its exact count law require separate source positioning.
