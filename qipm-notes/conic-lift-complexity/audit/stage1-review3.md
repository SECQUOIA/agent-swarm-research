# Stage 1 independent review 3

Scope: `main.tex`, `sections/01-foundations.tex`, and `sections/02-certificate-rank.tex`, with emphasis on counterexamples, hypotheses, facial reduction, and exact resource counts. I did not read other review reports or change the manuscript.

## Overall verdict

**No major mathematical issue identified.** The universal bound, the dimension-capped resource formulas, and the selection-free certificate-rank theorem survive the counterexample and boundary-case checks below. Two minor presentation corrections are needed.

## Findings requiring correction

1. **Minor — barrier-parameter wording is too categorical.** Location: `sections/01-foundations.tex:325–328`, especially “It is not the parameter of that restriction.” Restricting a standard product barrier to an affine slice preserves the ambient parameter as a valid upper bound; in some slices the optimal parameter also equals that ambient value. Thus ambient rank is not generally *different* from the restricted parameter. Proposed correction: say that total ambient Jordan rank is the standard ambient parameter and remains a valid parameter after restriction, but need not be the *least* parameter of the restricted barrier, and does not imply an intrinsic lower bound for the projected body. A later precise definition of the least restricted parameter should use this same terminology.

2. **Minor — define two basic symbols for a standalone paper.** Locations: first use of `C^\circ` at `sections/01-foundations.tex:66`, and `Q_{b_i+2}` at line 317. State `C^\circ={v:<x,v> <= 1 for every x in C}` and `Q_m={(t,z) in R x R^{m-1}:t >= ||z||_2}` before their first use. Their intended meanings are clear, so this does not affect any proof.

## Independent checks and attempted failure modes

- **Dimension minus two.** The local proof needs only two-sided differentiability, pointedness, and complementarity. For nonzero contact elements `a,b`, the derivative ranges lie in `b^perp` and `a^perp`. The restricted pairing has exactly the one-dimensional radial kernel spanned by `a`, giving rank `m-2`. At a zero contact element, a two-sided derivative lies in both the cone and its negative, hence vanishes. This also handles rays and two-dimensional proper cones. No hidden smoothness of the cone boundary is being assumed.

- **Arbitrary definable cones and regularity.** Exact projection of a definable cone slice makes the body definable. On a smooth boundary patch one may use a definable graph chart, and the normalized normal map is then definable. Minimum-norm choices in the nonempty closed convex primal and dual fibers are definable; alternatively definable choice suffices. Refining the finitely many relevant maps into differentiability strata supplies a dense regular locus meeting the open set of positive curvature. The proof does not improperly assume global regularity or a compact lifted feasible set.

- **Free variables.** A free-variable null direction preserving all equalities at fixed cone coordinates is feasible in both signs. Its output must vanish because the projected body is compact. Since this nullspace is independent of the particular feasible point, affine elimination yields a well-defined affine output map on the projected affine slice. There is no hidden cone-factor cost in that elimination.

- **Facial reduction.** Choosing a relative-interior feasible point puts every feasible point in its minimal face. The reduced lift is proper, and dual attainment then yields certificates valid on every point of the reduced affine slice. The manuscript explicitly evaluates certificate ranks after reduction, so it does not incorrectly assume an ambient positive extension of a reduced certificate. Faces of the relevant simple symmetric cones retain no larger capacity; rank-one and zero faces cannot supply curvature.

- **Reducible factors and resource counts.** Splitting a reducible symmetric factor preserves total Jordan rank and does not increase any irreducible component's dimension. Each curvature-contributing irreducible component has rank at least two and capacity at most `d-2`. Thus the lower bound `2 ceil((s-1)/(d-2))` remains valid even when the original presentation packages components into reducible factors. For arbitrary cones, summing `m_i-2` over factors of dimension at least two gives the claimed dimension lower bound, with ray dimensions accounted for separately. Zero-dimensional factors can simply be removed and cannot defeat the factor-count bound.

- **Norm-tree sharpness.** The chain tree has `sum b_i+1=s` leaves, each factor contains `b_i+1` child values and one epigraph value, and hence each factor has dimension `b_i+2`. Eliminating the nonnegative internal epigraph values gives exactly the Euclidean norm inequality. Positive, decreasing internal values give strict feasibility at the zero output. This checks factor count, total dimension, rank, and endpoint case `k=1` simultaneously.

- **Peirce bound with changing ranks.** The derivative of the primal element vanishes on the complementary support subalgebra, and the dual derivative obeys the corresponding restriction. The only overlap is the primal–dual off-diagonal Peirce space. Differentiating Jordan complementarity gives the stated positive Gram weights. The reasoning does not need local rank constancy or strict complementarity; common zero eigenspaces add no mixed channels.

- **Rank-minimizing selection.** Jordan-rank level sets are semialgebraic. Selecting from the least attainable level at each support and restricting to its dense open regular locus is legitimate even for unbounded fibers. At every regular support, the differential lower bound applies to a rank-minimizing certificate, which is precisely why it bounds every certificate in that fiber. The dense-open and essential-infimum conclusions use the quantifiers correctly.

- **Uniform attainment, including the exceptional cone.** The rank-one property of `P(x)c` follows from approximation by invertible elements and closedness of the positive rank-at-most-one set. For a half-Peirce element `w`, `P(w)c` is a positive rank-one element with trace `||w||^2/2`; this yields the rank-two subalgebra and determinant formula without associative matrix multiplication. The normalization factors `sqrt(2)` and `1/(2A)` in the completion are consistent with the trace inner product.

- **Whole-fiber obstruction and degenerate supports.** Comparing affine-slice coefficients forces every tail trace to `(1-eta)/2`. Away from the north pole this is positive even if an individual objective block vanishes, so every certificate block is nonzero. The supplied construction realizes rank one in each block, including zero objective blocks and the south pole. At the north pole, the certificate concentrates in a single head idempotent. Partial coordinate groups do not create a lower-rank loophole: unconstrained half-Peirce components cannot cancel a positive tail trace. For `q=1`, both generic and pole ranks are one, consistent with the theorem. The separately discussed interval case correctly avoids the zero value of the ceiling formula.

These checks support proceeding after the minor wording and notation fixes. They are a correctness review of the presented Stage 1 arguments, not an exhaustive novelty certification.
