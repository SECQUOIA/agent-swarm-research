# Stage 1 independent review — reviewer 5

Reviewed the scope/literature record, bibliography, scaffold, original conditioning and spectral material, the degenerate-LP development, and targeted active-file/literature searches. This is a planning review; candidate theorems have not yet been submitted with full proofs.

## Overall assessment

The proposed fixed-metric, equal-primal-gap scope is coherent. The explicit separation from preconditioned systems and iteration complexity is necessary and well handled. Inclusion of the degenerate LP endpoint resolves a real inconsistency in the source manuscript. Xiong–Freund is correctly recognized as a direct antecedent. I independently inspected its primary PDF, Fact 5.2 and Remark 5.1 (PDF pp. 32–33), and verified the July 15, 2024 arXiv version. The novelty language is appropriately provisional.

I found one major literature-review omission and two minor planning corrections. I found no mathematical counterexample to the proposed stronger geometric theorem.

## MAJOR 1 — add the omitted classical literature on central-path matrix conditioning and objective-gap parameterization

The audit overlooks Javier Peña, *Two properties of condition numbers for convex programs via implicitly defined barrier functions*, Mathematical Programming 93 (2002), 55–75, DOI 10.1007/s101070200294. This is directly relevant prior work, not merely a paper sharing the word “conditioning.” The author-posted abstract explicitly identifies growth of the condition numbers of linear equations in interior-point algorithms as one of its two main subjects. The publisher and author's publication list verify the metadata:

- https://optimization-online.org/2001/01/250/
- https://link.springer.com/article/10.1007/s101070200294
- https://www.andrew.cmu.edu/user/jfp/papers.html

The indexed author manuscript additionally exposes an objective-value parameterization in Section 3.1, Proposition 3.2, and the same standard containment facts in Proposition 2.7. Those locations are retrieval leads rather than a completed primary-PDF audit: direct access to the indexed ResearchGate copy failed with HTTP 429 in this review. Do not assert theorem equivalence from that excerpt alone. It appears to treat Schur systems rather than the proposed equality-reduced primal Hessian, so this finding does not establish that the proposed theorem is already known.

Two connected works also require screening before the final prior-work positioning is settled:

- Peña (2001), *Conditioning of Convex Programs from a Primal-Dual Perspective*, Mathematics of Operations Research 26(2), 206–220, DOI 10.1287/moor.26.2.206.10551. Publisher primary abstract: https://pubsonline.informs.org/doi/10.1287/moor.26.2.206.10551 . Its abstract concerns the conditioning of primal-dual constraint systems, so distinguish that condition notion from spectral condition numbers rather than assuming identity.
- Renegar (1996), *Condition Numbers, the Barrier Method, and the Conjugate-Gradient Method*, SIAM Journal on Optimization 6(4), 879–912, DOI 10.1137/S105262349427532X. Primary publisher page: https://epubs.siam.org/doi/10.1137/S105262349427532X . It explicitly bounds the conditioning of interior-point linear equations using an inequality-system condition measure and analyzes approximate CG solves. This belongs in the classical algorithmic context alongside Axelsson and Wright.

**Required correction:** add these sources to the scope audit and bibliography, state verified abstract-level scope honestly, and add a concrete Stage 2 obligation to compare Peña's objective-value parameterization and matrix-conditioning conclusions with the new theorems. Obtain/read the relevant primary text before assigning novelty to the gap reparameterization or general matrix-conditioning upper bounds. The final contribution should remain the precise difference-body/equal-gap comparison and consequences if those survive this comparison. I classify this as major because the user's central publication requirement is a careful novelty audit and the omitted 2002 paper directly combines the two proposed headline subjects.

More specifically, compare the following four claims, rather than merely adding citations: (i) the use of primal objective gap as a central-path parameter, which is plainly an older idea; (ii) the proposed all-barrier O(g^{-2}) upper spectral edge, because older self-concordant conditioning bounds may already imply it or its Schur analogue; (iii) the *matching* D(g)-dependent law, where a diameter-sensitive lower edge and two-sided conditioning conclusion may be the actual advance; and (iv) the Loewner comparison of two distinct barriers at the same gap, which is stronger than a scalar condition bound and should be checked against the older implicit-barrier machinery. There is currently no evidence from this review that (iii) or (iv) is already stated in Peña; they remain plausible contributions, with the uncompleted comparison disclosed.

## MINOR 1 — correct the oscillatory witness's Hessian notation

The added refinement says “H/4 has entries H11/4=2, ...”. This mixes the name of the matrix with its rescaled entries and risks a factor-four error downstream. Write either `H=F''; H11=8, H12=4 epsilon/y, H22=4(y^{-2}+(1-y)^{-2})`, or define `B=H/4` and give the entries of B. The candidate itself is consistent at x=0 and sin(log y)=0; it still needs the complete self-concordance audit already required by the plan.

## MINOR 2 — cite the classical Riemannian geometry comparator where the metric/path-length boundary is discussed

Nesterov–Todd, *On the Riemannian Geometry Defined by Self-Concordant Barriers and Interior-Point Methods*, Foundations of Computational Mathematics 2 (2002), 333–361, DOI 10.1007/s102080010032, is absent. The author-hosted primary manuscript is available at https://people.orie.cornell.edu/miketodd/NTRiemann.pdf and the Cornell repository at https://ecommons.cornell.edu/bitstreams/7802e4b8-9203-4dd6-890e-106c4b6e08e5/download . Its stated subject is the Hessian Riemannian metric, geodesics, and path-following efficiency. Add it to the scope-boundary literature map so the paper's “geometry” terminology is situated against both Euclidean sublevel geometry and intrinsic barrier geometry. No extensive treatment is needed.

## Independent mathematical checks to retain for Stage 2

The difference-body sandwich has a short plausible proof. For a centered Dikin displacement v, either x+v or x−v lies in the objective sublevel; taking its difference with x places v in L(g)−L(g). The reverse inclusion follows by subtracting two points each in the translated asymmetric-containment ellipsoid. Closure handles the unit boundary. This supports the candidate, provided the ellipsoid and subtraction both live in the same affine tangent space.

For the upper edge, homothetically contracting an interior Euclidean ball toward an optimum by g/Delta produces a ball of radius rg/Delta in L(g), for 0<g<=Delta. Its difference body contains a centered ball of twice that radius. Combined with L(g)−L(g) contained in 2C times the Dikin ellipsoid, this gives the proposed lambda_max upper bound. The objective projection must remain nonzero; the common equal-gap path interval must be stated.

For the approximate-gap claim, D(tg)<=tD(g) follows by contracting both endpoints of a diameter chord toward one common optimum, when the sublevels are defined in the same P. The objective displacement estimate follows by optimizing the linear objective over the closed Dikin ellipsoid and using feasibility. These refinements appear suitable for development.

The all-barrier O(g) weak-mode estimate also has a viable route: the canonical hard-range quadratic lower bound transfers by Loewner comparison, hence every unit vector in the weak spectral subspace has O(g) projection onto the orthogonal complement of the face tangent. Since c annihilates that tangent, the weak projection of c is O(g). Do not infer the sharper canonical O(g^2) rate from Loewner comparison alone.

## Coverage and scaffold

No additional mandatory repository theorem was identified beyond the inventory. Excluding the detailed QSVT/access and iteration-distance packages is a sound topical choice, provided their boundary implications are retained as planned. The scaffold clearly labels itself incomplete, so its empty author and absent bibliography rendering are appropriate at this stage. The original source's nondegeneracy restriction and numerical-only four-window claim must not survive unchanged; both are already explicit development obligations.
