# Stage 4A independent review 3

Recommendation: accept this stage. I found no major issue and no remaining minor correction that I consider necessary. This review does not assert that a finite review can exclude all possible errors.

## Scope

I read `stage4a-author.md`, all five new sections (`08a`, `08b`, `08c`, `08d`, `08e`), and the relevant prior reduction, selection, mixed-Peirce, and boundary-order lemmas. I did not read the other reviewers' reports or edit the manuscript. My principal focus was the full-fiber theorem and its barrier consequence.

## Entire boundary fibers and accessibility

Theorem `full-fiber-rigidity` has the needed hypotheses and its proof is sound.

- The set called `E` is the preimage of the product of sphere boundaries, rather than the entire topological boundary of the product body. Its projection fibers are convex. Compactness makes the separation argument for connectedness valid: the images of the two proposed clopen pieces are disjoint compact sets because each fiber is connected.
- Rank is lower semicontinuous on a symmetric cone, so nullity is upper semicontinuous. Integer values and a constant total nullity force each individual nullity to be locally constant. Connectedness then fixes each block's rank throughout `E`.
- Taking the midpoint within an individual projection fiber is legitimate. The support-join identity and equality of ranks imply equality of supports throughout that fiber. Continuity on a fixed-rank stratum and the compact quotient property then give an intrinsic continuous support map on the base. No continuous section is assumed or extracted.
- The curvature inequality is used only on a common regular semialgebraic set. Genuine pure-row certificates can be selected independently on their individual support spheres, while the primal selection is on the product. The mixed-Peirce lemma needs only first derivatives and does not require strict complementarity.
- Every step in `full-fiber-chain` has the correct direction. In particular, primal rank zero gives zero mixed contribution, ray nullities are retained in the final total, and the positive gap `m-2-a(r-1)` for rank greater than two rules out all such active factors at equality. Equality forces exactly `L` full-dimensional rank-two factors of primal and dual rank one. It cannot leave a vertex factor or a null ray.
- Interior inactive blocks have zero dual coordinate for every certificate of a row supporting the corresponding contact, not merely for the selected certificates used in the curvature argument. This justifies the subsequent injectivity proof.
- Equal active primal support rays annihilate a genuine certificate at the other primal tuple. Applying the whole-slice certificate identities to every pure row forces equality of all base coordinates. Invariance of domain and compactness then give a homeomorphism. The mod-two cohomological indecomposable quotient correctly recovers the multiset of sphere dimensions, including circles.
- The separate Lorentz lift attains the stated profile with compact singleton fibers.

Corollary `accessible-fibers` is also valid. The boundary-order lemma bounds nullity from above at **every** tuple. Accessibility supplies approximating regular tuples at which the local curvature bound gives the reverse inequality. Upper semicontinuity has exactly the needed direction at the limit. The text explicitly avoids deriving accessibility from a barrier bound or replacing every-tuple accessibility by a single selected sheet. It does not close the earlier unconditional barrier brackets.

## Other stage results

I also checked the following points without finding an error:

- In `general-joint-cover`, initially nonsmooth cone-base boundaries become smooth only after constant-rank transversal patches and invariance of domain establish relatively open image patches. Compactness then supplies surjectivity. The common-kernel argument does not differentiate the contact correspondence. The proper-cone ambient barrier lower bound uses interior-crossing two-dimensional linear sections; it is not incorrectly transferred to an affine feasible slice.
- In `product-orbit-saturation`, complementary aggregate ranks and capacity equality produce the finite support covering. The universal-cover square and torsion obstructions exclude the stated Grassmannians and the Albert orbit. The real order-five rational degree-two argument is sufficient without assuming its mod-two square relation. The real order-four cylinder argument uses its two separately assigned sphere rulings, and the order-three reduction preserves the finite scalar-ray terms. Assigning spin factors using cohomological indecomposables or circle windings does not presume that the covering splits as a product.
- In `projective-phase`, finite fundamental group permits global real angles; immersion follows from the mixed metric, and strict-diagonal vanishing gives injectivity. The inverse Stiefel--Whitney bound, projective-plane orientability refinement, stereographic constants, and finite smooth upper construction agree.
- The local chart and partition constructions use the declared factorization classes. The functional-inertia calculation correctly permits one additional negative direction for each noncospherical summand. Paired optimality is confined to positive block-additive summands, and the all-source-dependent example prevents an unsupported locality assumption.
- The Rado argument works for arbitrary index sets: multilinearity reduces independent subspace choices to independent members of the generating sets. The deficient span is the direct sum of its block spans because each block-diagonal range contains its block-supported vectors. The cylindrical column-space bound and uniform-cap algebra are correct. The exact squared-kernel rank includes independent linear and homogeneous-quadratic restrictions. The conversion to a barrier bound retains the affine-slice hypothesis.
- The abstract plane-field proof only concludes existence of a frame, not triviality of the originally supplied small summand. The midpoint-rank case is separately excluded by Euler class. The sphere-product submersion calculation treats the potentially non-simply-connected fiber over `S^2` separately, using an explicit acyclic path model. The balanced real-orbit argument treats positive-dimensional fibers and covering maps separately.

## Primary literature spot checks

- I opened Aubrun--La Piana--Müller-Hermes, [arXiv:2606.27825v1](https://arxiv.org/html/2606.27825v1), and checked the introduction and Theorem 1. The manuscript accurately distinguishes their quantifier over every positive linear map from the present single smooth slack factorization.
- I checked the primary author lecture notes by Kathryn Hess, [*Rational Homotopy Theory*](https://homepages.math.uic.edu/~bshipley/Hess.Chicago.pdf), Theorem 2.2.1 and the following fiber-square discussion, together with Theorem 2.4.3. The simply connected base hypothesis supports the fiber-model argument even though the fiber over `S^2` need not itself be simply connected. The formal-dimension identity matches the manuscript's parity calculation.
- I checked the search-accessible primary author-uploaded Browder article record and theorem text concerning a connected polyhedral fiber of a sphere-total-space bundle. The use is consistent with the cited sphere-fibering theorem; the manuscript also supplies the subsequent spectral-sequence reasoning rather than attributing all of its product consequences to Browder.

The existing build log has no undefined-reference, citation, or overfull-box messages. I did not rerun the unchanged build because the stage author had already supplied the integrated clean build.
