# Stage 2 independent review 4

Reviewed: `sections/03-products.tex`, `04-global-regularity.tex`, and `05-support-orbits.tex`, with the dictionary, minimum-fiber-rank, and Peirce-perspective results in Sections 1–2. I also checked the original joint-contact, switching, PSD2 product-rank, and Grassmannian source notes. I did not read other stage review reports.

## Verdict

**No major mathematical issue found.** The distinctions between full labelled rows, a joint weighted contact kernel, genuinely certified affine lifts, and prescribed globally smooth selections are maintained. The uniform simple-EJA selected-rank theorem and its sequential extension appear correct, including the Albert case. Two minor corrections would complete the presently claimed source coverage and remove an undefined edge case.

## Minor findings

1. **Preserve the exact PSD2 worst-certificate result and dual uniqueness from the source.** Locations: `03-products.tex:79–87`, `04-global-regularity.tex:244–264`, and `audit/source-map.md:374`. The source `selection-free-psd2-product-ball-exposed-rank.md` proves the exact value
   \[
   \inf_{\mathcal L}\sup_{u,\;Y^a\in\mathcal D_a(u_a)}
   \sum_i\operatorname{rank}\!\left(\sum_a\lambda_aY_i^a\right)
   =\sum_a(s_a-1)
   \]
   for real PSD2 lifts, for every fixed positive weight vector. This is a supremum over genuine **pure-row** certificate choices; it is not a minimum over the full aggregate-objective certificate fiber. The current source-map disposition warns against an “aggregate-fiber universal-minimum strengthening,” which is a different assertion and does not account for this valid exact source result. The manuscript gives its lower bound and explicit favorable norm-tree certificates, but does not prove uniqueness of the norm-tree dual certificate or state the resulting exact worst-certificate frontier. Its uniqueness claim currently concerns primal boundary fibers only.

   Fix: add a short dual coefficient-matching argument to the tree example (or a short adjacent corollary), state this exact PSD2 frontier, and correct the source-map disposition. In a binary tree, the leaf coefficients determine the corresponding signed dual coordinates; the coefficient of an internal primal variable equates its dual head with the negative parent coordinate; the root head equals one. Cone positivity forces every head to be at least the norm of its descendant support coordinates. The unit root norm forces equality down the tree, proving the displayed dual tuple is unique. On independent products, other-source factors of a pure-row certificate vanish by evaluating the zero slack while those factors are interior. Thus every pure-row aggregate has rank at most the number of tree factors, with generic equality. This is a small coverage completion, not a defect in the general dictionary existence theorem.

2. **State the nontrivial order cap in the private-curvature theorem.** Location: `03-products.tex:100–117`. The statement allows `R=1` syntactically but subsequently divides by `B=delta(R-1)`. Add `R>=2` to the theorem assumptions. Ray-only factors cannot satisfy the curved full-row identity, but the displayed ceiling is still undefined as currently written in that empty case.

## Checks supporting the verdict

- The joint two-ball construction has the correct constants: `c(x)c(z)||f(x)-f(z)||^2/2 = 1-<Z(x),Z(z)>`, and `<U(t),V(u)>=(t-u)^2/2`. Since the first block of `Z` has fixed norm `sqrt(lambda_1)<1`, the chosen stereographic pole is uniformly avoided. Thus the construction is global and smooth. Its `2s-1` factors match the phase-lift lower bound, whereas full labelled rows require `2s`.
- The general k-ball upper bound follows by normalizing the weights within each pair and scaling that pair's factorization by its total weight. A leftover source uses s coordinate-square factors. The manuscript explicitly leaves the k>=3 exact count unresolved rather than presenting the bounds as an equality.
- The hypersurface embedding assertion for sphere products is sound: an orientable Euclidean hypersurface has a trivial normal line, and adding p ambient directions makes the normal bundle trivial of rank p+1; its tubular boundary is the product with `S^p`.
- The switching argument uses a genuine product cylinder and disjoint phase patches. The dense-nonzero dual argument can be written as continuity of `X_i wedge D_b X_i=0`; the stated conclusion is valid. The flat smooth example refutes only an invalid continuation step and is explicitly not advertised as a full-slack construction.
- The norm-tree pairings telescope on the entire affine slice, even with free internal primal variables. The primal boundary-fiber uniqueness and codimension-two exceptional sets are correct. The local orthogonal projection decomposition is an exact linear-algebra consequence of rank saturation and does not imply global cone rigidity.
- In the selected-rank proof, equality forces q active rank-one dual factors with maximal per-rank capacity B and complementary primal rank r-1. Their primitive orbit maps yield the required covering. The real projective case is excluded by the affine-pencil kernel-injectivity lemma, and complex/quaternionic/Albert cases by their intermediate cohomology. The fixed-tail construction is valid in every EJA through the already established quadratic-representation identities.
- Under sequential compression, every proper non-ray face has strictly smaller per-rank capacity than its parent: lower matrix order classically, only rays in a spin factor, and the rank-two Albert face has capacity 8 rather than 16. A proper face therefore cannot create a new capacity-B matching-spin exception. The product lower bound applies to the chosen globally smooth pure-row sheets with the stated existential simultaneous-contact quantifier.
- I checked the stated Saint Raymond local-inversion hypothesis against the primary publisher abstract: everywhere differentiable maps with everywhere nonzero Jacobian are locally invertible in finite dimension. Source: https://www.cambridge.org/core/journals/mathematika/article/abs/local-inversion-for-differentiable-functions-and-the-darboux-property/5BE7FE09B3537A86F87FBF705E1B20D0 . Its use in the differentiability-only proposition is appropriate.
- Unique general-cone, product-orbit, residual-kernel, and projective-embedding content explicitly deferred to Stage 4 was not treated as missing Stage 2 content.
