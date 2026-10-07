# Independent mathematical review: representability and sparse graphs

Reviewed files:

- `sections/02-setting.tex`
- `sections/06-representability.tex`
- `sections/07-graphs.tex`
- `appendices/C-representability.tex`

This review reconstructed the proofs from their stated hypotheses. It did not conduct literature research or rerun archived optimization experiments. The Bodirsky–Kummer–Thom external inputs were treated as contracts verified by the separate literature review; their internal use was checked here.

## Conclusion

No substantive mathematical error or missing prerequisite was found. The sharp four-variable obstruction, its geometric extension, the proper-face result, the positive-induced graph minor obstruction, and the small-positive-component formulation follow from the stated external inputs. There is one minor formulation clarification listed below.

## Checked arguments

1. **Closed homogenization and duality.** For compact `K` and closed polyhedral `D`, the cone `hat(K+D)` is closed, with the complete height-zero section `D`. A homogenized arbitrary lift may omit recession directions but cannot add any direction outside `D`; adding the explicitly representable height-zero cone fills the omitted directions without changing a positive-height section. This avoids an unjustified assumption about lifting all recession directions. The constant coordinate and diagonal slack give the claimed dual cones.

2. **Positive side of the dimension threshold.** The order-simplex construction uses DNN blocks of order at most four. A completely positive decomposition turns each nonzero rank-one term into a simplex atom with mass `(1^T v)^2`; normalization and the moment maps are correct. An intrinsic affine coordinate change extends the construction to arbitrary polytopes of dimension at most three.

3. **Real closed field obstruction.** The coefficient map fixes real constants because it is unital and `F`-linear. Therefore entrywise complete positivity preserves the affine LMI and the auxiliary witness of a lift. The Horn quadratic is nonnegative over the extended box. With first-coordinate-most-significant lexicographic order, every exponent `2e_1-2e_{k+1}` is positive, making the evaluation point lie strictly between zero and one. All five rescaled variables evaluate to `epsilon^(2e_1)`, so the mapped polynomial has value `epsilon^(4e_1) eta < 0`. Its original square coefficients are positive, so the same obstruction applies to both square-sign cones. The higher-dimensional section and the passage to normalized moment sets are valid.

4. **Simple-ray geometry.** At a simple ray, the `m-1` incident facet forms have common kernel equal to the ray span. Adding a strictly positive cone form gives an invertible coordinate map. The stated bound on each nonincident facet is uniform for the required thin five-dimensional orthant; setting unused transverse coordinates to zero is legitimate in dimension above five. Height zero gives only the origin. The cone over a polytope carries the asserted homogeneous quadratic correspondence in intrinsic coordinates.

5. **Every proper face of the four-variable compact hull.** The zero set on a cube face containing a relative-interior zero is an affine kernel section of that face. There are finitely many such polytopes, each of dimension at most three, including the full-cube case when the quadratic has a nonzero PSD quadratic part. Their compact moment hulls and their finite convex hull have finite lifts. For a nonexposed face, the supporting-hyperplane construction in successive affine hulls decreases the containing face dimension until it equals the target face. The argument does not incorrectly include the improper face.

6. **`K_4` minors and minor closure.** Each tree-edge squared-difference expression is nonnegative only because both endpoints have positive loops. Equality forces branchwise equal atom coordinates and zero slack on all nonsingleton branch vertices. The projection is exactly the four-variable compact hull plus singleton diagonal slack, and adding the remaining diagonal rays gives the obstructed positive-loop hull. The single-edge contraction proof correctly restores the merged diagonal ray after projection. Deletion is a coordinate projection.

7. **Signed sparse lift with at most three positive vertices per component.** Independent Bernoulli rounding outside the positive set preserves every recorded cross moment and first moment. A negative diagonal is recovered by downward slack; an absent diagonal imposes no condition. Consistent bag tables produce a joint binary law, including zero-probability separator states. Conditional DNN simplex blocks at each boundary assignment have no residual moments at zero mass. Sampling distinct continuous components conditionally independently realizes every retained edge, since no edge joins two distinct positive components. The count is valid because component orders are bounded by three; it explicitly does not claim original-graph treewidth controls torso width or count every linear-map nonzero.

8. **Forest reduction.** Complementations preserve all square coefficients and the cross-support graph. Choosing vertex signs recursively on a forest maps each sparse quadratic to the nonpositive-cross-coefficient cone. A finite union of these cone images lies in their finite Minkowski sum, and the reverse containment follows from convex-cone closure under addition, proving the asserted equality. Linear sign restrictions provide the converse representability implication. The open path/star cases are not used as theorem premises elsewhere.

## Minor clarification

In the small-component lift, explicitly allow a single empty bag when `R` is empty. Its unique table entry has mass one; then the empty boundary assignment for an isolated positive component has marginal probability one. This makes the construction literal in the all-positive disconnected case. It is a notation/convention clarification and does not affect the theorem or proof strategy.

No numerical checks or project-wide checks were run for this review.
