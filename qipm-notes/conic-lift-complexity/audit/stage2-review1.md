# Stage 2 independent review 1

Scope: `sections/03-products.tex`, the selected-rank and successive-compression arguments in `sections/05-support-orbits.tex`, and their dependence on the Stage 1 foundations. I reconstructed these arguments rather than relying on workbench status labels. I did not inspect the other five-review reports.

## Assessment

No major mathematical issue found. The all-EJA compression argument is valid, including the Albert algebra. The product existence theorem preserves the materially important original-certificate quantifier. The stronger smooth-product statement also follows, because passage to a proper face cannot create a new capacity-B spin exception. Two small proof-presentation corrections below should be made before closing the stage.

## Valid minor corrections

1. **Make the affine-face intersection explicit before calling compressed certificates genuine.** In `03-products.tex`, lines 49–60, cylindrical complementarity establishes that every *feasible* point of the restricted affine slice belongs to the complementary face. It does not put every infeasible point of that affine slice in the face. Consequently the sentence at lines 56–57 that compression preserves pairing with “every tuple on this slice” is literally justified only after replacing the affine slice by its intersection with `prod_i V_i(f_i,1)`. Add this intersection explicitly immediately after the cylindrical-complementarity sentence (it preserves the feasible set and exact projection). Then both that sentence and the later minimal-face certificate assertion hold on the entire stated affine slice. This is local bookkeeping, not a gap in the lower bound: the final minimal-face slice already has the needed intersection under the conventions of Lemma 1.1.

2. **Use rank, not dimension, for the join increment.** In `03-products.tex`, lines 65–68, replace “dimension increment of a support join” with “Jordan-rank increment of a support join.” The invariant in the displayed lemma is Jordan rank; the real vector-space dimension of an EJA face is generally different. The subsequent face-lattice rank inequality is correct.

## Detailed proof checks

### All-EJA support joins and compression

For `f=e-c`, `t=supp(P(f)y)`, the positive element y is orthogonal to the idempotent `f-t`, since the quadratic compression is self-adjoint and fixes that idempotent. Thus `supp y <= c+t`. Conversely the complement k of `c join supp y` lies below f and is orthogonal to y, hence to `P(f)y`; it is therefore orthogonal to t. This puts `c+t <= e-k`, proving equality. The argument uses EJA face orthogonality and quadratic projections only, with no associative matrix multiplication. It applies to Albert factors. Orthogonality against a positive sum is equivalent to orthogonality against each positive summand, giving the support-join formula for all positive weights.

Compression does not increase Jordan rank. This can be seen by spectrally decomposing y into primitive positive summands: their quadratic images have rank at most one, and rank is subadditive on the positive cone. Equivalently it is the standard face-lattice rank inequality. In particular `rank(P(k)y) <= rank(P(f)y)` when `k<=f`; the nested Peirce projections satisfy `P(k)P(f)=P(k)`.

### Original certificates and successive rows

The restricted projection is exactly the next ball: every point in that ball, together with fixed earlier contacts and fixed later interior coordinates, belongs to the original product and has a feasible lift. Original whole-slice pure-row certificates exist by original-slice Slater duality. After the explicit face intersection requested above, their compressions are genuine certificates on the restricted slice. Its minimal-face reduction has no greater capacity B. The generic *all-certificate* lower bound from Theorem 3.1 can therefore be applied before choosing any original certificate at the resulting support. Its further compression has rank at least `q_B(s_a)`, so the first compression does too. The support-join lemma then adds these increments. Every final primal tuple is complementary to the chosen positive aggregate, proving the every-primal-fiber nullity assertion.

The statement does not mistakenly claim that all aggregate certificates, or the minimum rank in the aggregate objective fiber, obey the additive bound. The paragraph following the theorem explicitly keeps these quantifiers separate.

### Private Hermitian curvature

At a contact, take the decomposition `Ran X_i direct-sum ker X_i`. A two-sided PSD derivative has zero kernel-to-kernel block. In the row-a mixed pairing, the derivative of Y has its kernel-side endpoint in `U_ia`. Cylindrical complementarity implies the source-a derivative of X annihilates `U_i,-a`. Hence the relevant off-diagonal map factors through `U_ia/(U_ia intersect U_i,-a)`, and its real target-space dimension is `delta p_i d_ia`. This proves the mixed-rank estimate over real, complex, and quaternionic Hermitian matrices. The complements E_ia are jointly independent by the stated elementary argument; their sum dimension is at most the rank of the positive aggregate. The integer rounding is performed source by source before summing, which is necessary and correct.

The column-packing construction has Schur complement `S-W*W`. Its diagonal is nonnegative precisely at feasible projected points; the given choice supplies the converse. At a product extreme this PSD Schur complement has zero diagonal, hence vanishes. The block matrix then has rank p and nullity h. Each displayed certificate gives the pure-row slack on the entire affine slice and has rank one. Their leading e_a coordinates establish independence over each stated field.

### Selected ranks and successive smooth compression

In the one-ball equality case `s-1=qB`, the mixed-rank chain forces exactly q nonzero dual factors, each of rank one, full parent capacity B, and complementary primal rank r-1. Lower semicontinuity plus constant total rank makes the factor ranks constant. The support differential identifies a covering by the sphere onto the product of primitive-idempotent orbits. For q>1, the circle fundamental-group obstruction or the intermediate cohomology of the product of compact universal covers rules it out. For q=1, only a matching spin survives: the real projective alternatives are ruled out by the affine-kernel lemma after the other dual factors vanish. That affine pencil follows by evaluating the full slack against a matrix basis drawn from the rank-one dual sheet. The fixed-tail construction has nonzero rank-one duals even for zero coordinate groups, so it attains the claimed selected rank everywhere.

For products, fixing the earlier contact coordinates puts the primal sheet in the complementary face. Fixing the later coordinates on their spheres leaves a globally C1 two-point next-row factorization, and linear quadratic compression preserves C1 regularity. A proper classical face lowers the order, a proper spin face is a ray, and the Albert rank-two face has capacity 8 rather than 16. Thus any saturation at the original B comes from unreduced original factors; compression cannot create a new matching spin exception at B. Applying the one-ball proof to each remaining face system gives the stated incremental kappa bound. Positive-weight aggregate ranks are join ranks, so the chosen simultaneous contact works for every positive weight vector. The separated fixed-tail/direct-spin constructions attain both aggregate rank and nullity.

The adaptive finite-capacity envelope is also consistent: the concavity of `q(R-q)` makes an equalized integer allocation maximize capacity at fixed total rank. This is a lower bound, not an asserted exact additional frontier.
