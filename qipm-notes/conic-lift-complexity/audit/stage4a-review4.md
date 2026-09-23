# Stage 4A independent review 4

Reviewer focus: restricted kernels, projective phase embeddings, near-saturation counts, and the column-rank nullity criterion. I read the author report, all five Stage 4A sections, and the relevant earlier contact-rank, joint-kernel, and real order-three exclusion arguments. I did not read other reviewer reports or modify the manuscript.

## Verdict

No major or minor correction identified. The statements I checked have the hypotheses their proofs require. In particular, the new column-rank strengthening is valid; it does not need continuity, and its stronger squared-kernel corollary follows with the stated strict inequality. The manuscript appropriately distinguishes restricted kernels from complete labelled slack factorizations.

## Restricted-kernel verification

- Projective phase embedding: nonzero complementary Lorentz factors give globally defined positive scales and circle phases. Finite fundamental group, rather than mod-two first cohomology, permits real angle lifts. The mixed metric proves immersion; the strict diagonal proves injectivity. Compactness supplies an embedding. The inverse Stiefel--Whitney calculation has the correct maximal degree `2^ceil(log2(r))-r`, including power-of-two values of `r`. Its product monomial gives the stated codimension bound. The separate orientability argument is needed and correctly supplied for the projective plane.
- The normalized Veronese factor, stereographic denominator, and scalar chord maps have consistent scales: the Lorentz pairing is half the squared scalar difference, so multiplying both factors by the displayed positive denominators gives the desired projective kernel. The upper construction is nowhere zero and uses exactly the claimed number of channels.
- Local chart saturation covers every finite set of sample pairs and their jets by choosing poles outside both projected sample sets. The inference concerns the kernel's locally selected factors and does not make the false assertion that a prescribed finite list of factor values extends globally.
- Partition separation legitimately isolates a group by freezing the others at diagonal contacts. Functional inertia is justified by one finite evaluation matrix of full feature rank; each common-scale term has at most one extra negative direction, and a cospherical term has none. The overlapping block-additive count uses `I >= k` and `t <= floor(I/2)` correctly. Exact paired optimality is explicitly confined to that smaller class.
- The all-source-dependent construction has a pole strictly outside the weighted product image. Its tangent variation establishes actual dependence of a selected channel on every source; it does not rely on an unproved locality assumption.
- In the Rado argument, independent choices from the union of matrix ranges would lie in a common primal kernel at the corresponding product contact. The subspace induction and exterior-product reduction handle infinite generating sets. Crucially, the deficient range span really is the direct sum of the block range spans because the matrices are block diagonal. Thus its matrix-space dimension is at most `(R+1)(|J|-1)/2`.
- Cylindrical column spaces have relation dimension at most `|J|-1`, even if some of them do not contain constants. This gives the exact expression used in the strict criterion. The uniform endpoint calculation is correct and includes `b=1` without an order restriction.
- Antipodal separation gives a continuous coefficient map separating antipodal points, so Borsuk--Ulam yields column rank at least `s`. For squared slack, odd columns span all linear coordinates, and even columns span all homogeneous quadratic forms on the sphere. The exact rank is therefore `s(s+3)/2`, not merely a lower bound. Constants occur in each column space, giving the exact labelled rank `1+b(rho-1)` and the stated matrix-dimension and factor-count consequences.
- The barrier consequence has the necessary extra relative-Slater affine-slice hypothesis. The final positive-splitting example does not promote its factor penalty to an unrestricted full-slack lower bound.

## Checks across the rest of the stage

The normalized-base argument extracts genuine embedded charts from constant rank and invariance of domain before treating the initially nonsmooth boundary as a smooth sphere. Joint injectivity follows from contact nondegeneracy. The covering theorem does not assert that the cone is Lorentz or that a product covering splits coordinatewise.

The product-orbit proof retains finite coverings in the presence of scalar rays. The real order-four ruling argument uses both assigned sphere factors; the real order-three argument first isolates its row and then invokes the full mixed rank to obtain the local diffeomorphism required by the earlier exclusion. I found no missing implication in these reductions.

The full-fiber theorem uses compactness to obtain connectedness and support descent. Upper semicontinuous integer nullities with constant total are locally constant individually. Equality in the Peirce/dimension chain forces full-size rank-two factors of corank one; the entire-fiber hypothesis is not silently replaced by a chosen section. The accessibility corollary uses upper semicontinuity in the correct direction.

The topology appendix distinguishes individual submersions from joint saturation. Its clutching argument proves existence of a frame without asserting triviality of the original plane field. The rational formal-dimension calculation has the appropriate simply connected fiber for target dimension at least three, and the target-two argument explicitly uses a fiber model instead of assuming simple connectivity. The balanced real order-five exclusion uses the integral relation `x^2=2y`, which supplies the required mod-two contradiction.

## Literature and attribution checks

I independently inspected the primary author-uploaded text of Browder's 1962 note, Theorem 1, at <https://www.researchgate.net/publication/251964661_Fiberings_of_spheres_and_H-spaces_which_are_rational_homology_spheres>. Its connected-fiber sphere conclusion supports the uses in the topology appendix.

I also inspected the primary text of *Positive Semidefinite Rank* at <https://arxiv.org/html/1407.4095> and the publisher article for Fawzi's SOC nonrepresentability result at <https://link.springer.com/article/10.1007/s10107-018-1233-0>. The manuscript correctly attributes ordinary PSD-rank bounds to prior work and keeps full-cone SOC nonrepresentability separate from its finite restricted-projective-kernel construction. The Rado ingredient is proved in the manuscript, so its use does not depend on access to the original paywalled article.

No literature-wide firstness claim is made in the reviewed restricted-kernel section. The stated additional steps are specific mathematical implications rather than claims that the underlying topology or ordinary-rank machinery is new.
