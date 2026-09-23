# Stage 4C independent review 1

Decision: **no major issues and no minor issues identified**. Stage 4C is acceptable on the scope reviewed below. This decision does not replace the later whole-manuscript review.

I personally read all seven new sections, `10a` through `10g`, and `audit/stage4c-author.md`. I did not read another review, delegate the review, or edit the manuscript. I examined the nonsymmetric-barrier author audit after reading the manuscript, and the projected-compiler audit to check the distinction between published and preprint theorem numbering. I read the necessary earlier curvature, reduction, partial-minimization, minimum-dimension, norm-ball, and sphere-submersion results. The following records substantive verification, rather than a list of suggested changes.

## Nonsymmetric barriers

- The root equation defining `h(p)` is strictly monotone for the stated non-Euclidean range, and the algebraic excess formula is correct. The logarithmic-homogeneity restriction is retained in the actual theorem and its dictionary consequences.
- I checked Hildebrand's primary full text, Theorem 5.4 and Sections 7.1–7.2. The cross-ratio convention agrees with the manuscript. Norm-cone configurations for `p < 2` use the branch whose sums exceed two; those for `p > 2` do not. Dualizing the entire product before using the product lemma is therefore necessary and correctly done. The scalar power-cone configuration uses the positive branch after exchanging the axial coordinates when appropriate.
- The product lemma is sound: on the ray from an embedded vertex through the product interior point and onward, the other blocks remain strictly positive multiples of their local interior points. Projectivizing the chosen block maps the opposite contact and the missing-basis hyperplane to their local counterparts. Thus the local cross-ratios survive, including their sum, without imposing separability of the barrier.
- I independently computed the perspective conjugate, dual cone, and axial/diagonal map to the conjugate-exponent cone. The section `u=v=t` and the scalar-output sections meet the cone interiors. The upper bounds use dimension-parameter existence separately from the more expensive scalar-power oracle construction.
- For the characteristic integral, the change of variables has Jacobian `alpha s^(r+1)`. Integrating the positive residual and radial variables yields the displayed exponent `r+1`. Near the unique minimizer the anisotropic volume exponent is `1/2+(r-1)/q`, giving blow-up exponent `3/2+(r-1)/p`. The local dominator is integrable, and the outside tails remain bounded for derivative orders zero through three. The rising-factorial derivative coefficients follow from the homogeneous model integral. The norm-cone transverse-volume calculation independently gives exponent `1+(r-1)/p`. These differentiated estimates justify the self-concordance inequality; an undifferentiated asymptotic alone would not have sufficed.
- The characteristic-family strict-gap proof has the correct signs. The derivative of its cubic numerator is negative on the required interval, and its endpoint is zero. The separate statement for `p < 2` correctly names the dual-characteristic family rather than identifying it with the characteristic family.
- The two-LHSC classification argument works: the two test directions force the tangent cubic to vanish, and homogeneity removes every radial component of the third derivative of `exp(-F)`. Its quadratic form has Lorentz signature. The manuscript correctly distinguishes this nonattainment argument from a strict lower bound on the infimum.
- I checked the failed defining-log and nested-log formulas, including the nonzero coefficient causing loss of third differentiability and the diverging transverse third derivative when `p > 3`. Their claims apply to the specified formulas and bounded corrections, not arbitrary barriers.
- The endpoint expansions agree with direct expansion of `a^s(1+s(a+1))=1`. I additionally checked the displayed asymptotic errors numerically using Python's standard-library `decimal` arithmetic at 60-digit precision in the required qipm environment. No package was installed. These numerical checks supplement, rather than replace, the algebraic verification.

## Entropy aggregation

- The orthant-input recession certificate has feasible simultaneous subtraction and the stated noninterior thresholds, including `n=1`. Its tensorization is a lower-bound argument valid for coupled, nonhomogeneous barriers.
- The explicit linear isomorphism between the dual and primal exponential cones has the correct signs and boundary face. Thus the product optimum `3R+P` is justified for either convention.
- I recalculated the entropy second and third directional derivatives and the geometric-mean compatibility identity. The resulting compatibility constants are sufficient for the cited theorem.
- The zero-column distinction is correct and substantive. Every active entropy term is bounded above along a convergent image sequence because it appears with a positive coefficient in some row and every other term has a uniform lower bound. Lower semicontinuity gives the necessary closed inequalities. Replacing zero coordinates by positive epsilon supplies the converse, including an active pair `(0,0)`. Inactive pairs can have positive first input and zero second input and must therefore use rays rather than an unused exponential cone.
- The parameter counts `2N+B`, `2N+n_++B`, and `3N` for a nonempty partition use different precise representations and are correctly distinguished. The Hessian factorization gives the asserted arithmetic solve count without claiming an equally cheap affine-constrained Newton solve.

## Approximation, topology, and conditioning

- The finite-sample mixed difference is `-h^2 I-tau^2 11^T`; the four entrywise errors give the stated operator bound. The two normal projections and the singular value of size gamma justify the block approximation, including dimensions one and two, parallel vectors, and a zero selected factor.
- In the smooth theorem the mixed slack derivative remains exact despite the support-function error. The finite-radius interpolation formula handles zero curvature bound. The sharper error omits a genuinely unnecessary term. The definable local selections do not silently assert uniform chart or derivative bounds.
- The global robust splitting uses continuous canonical projectors, not arbitrary pointwise truncations. The invertible sum and saturated rank budget imply constant full channel ranks and a direct sum of images. Adams and Euler-class consequences agree with the earlier statements.
- The phase-critical-point argument correctly uses the total diagonal defect derivative, whereas the higher-rank argument correctly requires the one-sided derivative. The latter distinction is not lost in the corollaries. I checked the cited sphere-submersion dependency and the Hopf exceptions.
- The gauge-infimum obstruction is invariant under fixed blockwise changes of coordinates, and its limitations are stated. The Lorentz boost preserves the Schur matrix but not the raw augmented spectrum. Both the oscillating radial and rotating phase examples have the displayed derivatives and bounded pointwise geometry. The final condition-number and bit-count consequences are explicitly conditional.

## Exact and projected compilers

- The translate criterion is the classical finite-dimensional vector-lattice result with a valid elementary proof. The Lorentz arc example only obstructs the specified same-space translate representation. The query discussion includes joint success amplification and distinguishes physical from transformed entry access.
- The continuous-summary lower bounds use injectivity and invariance of domain under the needed continuous-encoder hypothesis; decoder continuity is unnecessary. The finite dilation-rank classification is attributed to the classical translation-space theorem. Both relative-entropy conventions have the correct scalar scaling terms.
- The binomial three-cone construction exactly represents the whole epigraph despite unbounded signed-feature rank. For product cosh, retaining the epigraph coordinate gives an `r`-dimensional positive-curvature patch after compact truncation, so the strengthened lower bound `R >= r` follows from the earlier curvature theorem. The artificial truncation ray is correctly excluded from the original ambient barrier charge.
- Farkas compilation retains the orthogonal compatibility equalities. The extreme-ray count uses effective rank. The canonical recourse rule requires a strictly positive feasible point and has an invertible reduced KKT derivative.
- The scalar and matrix quadratic barriers have the stated derivatives and exact parameters after quotienting flat directions. The Loewner inflation is in the safe direction. The quantum LP and spectral-approximation reductions retain their access, precision, initialization, output, and objective-scope qualifications.
- The convolution-normalization obstruction uses the stated degenerate-block family. The reusable boundary-oracle lower bound has an operational joint reuse contract and a correct Fourier-span dimension argument. The additive-log lower bound uses individually exposed arcs and does not conflict with the dimension-two existential barrier.

## Primary literature checks

The local Lee–Yue literature entry and the manuscript's earlier cited dependencies were consulted read-only. Online checks included:

- [Hildebrand, primary full preprint](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf): cross-ratio convention, Theorem 5.4, both norm-cone branches, power-cone branch, and the account of Chares's numerical conjecture.
- [Chares, full thesis](https://perso.uclouvain.be/francois.glineur/files/theses/Chares-PhD-thesis-2007.pdf): scalar power-barrier theorem and the distinction from higher-dimensional conjectures.
- [Fawzi–Saunderson, primary full text](https://arxiv.org/html/2205.04581v3): compatibility and recession lower-bound framework.
- [Hildebrand, canonical-barrier publisher record](https://pubsonline.informs.org/doi/10.1287/moor.2013.0640): dimension-parameter existence and the distinction from the characteristic barrier.
- [Apers–Gribling, primary full text](https://arxiv.org/html/2311.03215v2): spectral approximation and row-access scope; the author audit explains the published theorem numbering used in the manuscript.

Targeted literature searches did not identify a contradictory prior statement of the displayed higher-dimensional characteristic necessary scales. That negative search is not proof of priority. The manuscript's qualified formulation is appropriate. Classical constructions and unresolved optimal-barrier questions are clearly separated from the precise developments claimed here.

No correction request results from this review.
