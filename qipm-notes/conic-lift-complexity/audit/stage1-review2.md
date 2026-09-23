# Stage 1 independent review 2

Reviewed `main.tex`, `macros.tex`, `sections/01-foundations.tex`, `sections/02-certificate-rank.tex`, and `bibliography.bib` independently, without reading other reviewers' reports or workbench audit conclusions. Primary emphasis: all-Euclidean-Jordan-algebra calculations and exceptional-cone attainment.

## Verdict

No major mathematical issue found in Stage 1. The selection-free certificate-rank theorem, including the Albert case, is supported by the stated arguments. Two minor terminology/definition issues should be corrected. This verdict concerns the material currently present, not the later barrier results or completeness of the final paper's literature review.

## Minor findings requiring correction

1. **Use “trace-inner-product norm,” not “trace norm.”** In `sections/02-certificate-rank.tex:80`, the norm defined by `||w||^2 = <w,w> = tr(w^2)` is the Euclidean/Frobenius norm associated with the trace inner product. “Trace norm” conventionally denotes `tr(|w|)`, a different norm. The constants in the displayed perspective and completion identities are correct for the stated inner-product norm. Replace the phrase with “the norm induced by the trace inner product.” No formula needs to change.

2. **Define the polar body and Lorentz-cone notation before first use.** `C^\circ` first occurs at `sections/01-foundations.tex:66`, without a definition, and `Q_m` first occurs in the norm-tree proof near the end of that file, also without a definition. These are familiar but central conventions in a standalone paper. Add `C^\circ={v:<x,v> <= 1 for all x in C}` after the assumptions on C, and define `Q_m={(t,u) in R x R^{m-1}:t >= ||u||_2}` before the norm-tree construction. This also makes unambiguous that m is total cone-space dimension.

## Calculation audit

### Mixed Peirce channels

At a complementary contact, positive X and Y admit a common Jordan frame, with disjoint positive supports I and J. For every positive z supported on I-complement, the scalar function `<X(th),z>` has a two-sided minimum at zero. Its first derivative vanishes. Since that face cone spans the corresponding Peirce-one subalgebra, DX has no components with both endpoints outside I. The same argument applies to DY with J. Therefore their common Peirce components are exactly I-by-J blocks, irrespective of any zero-zero support or changes of rank nearby.

Differentiating `X circ Y=0` gives, in a block V_ij, `(mu_j DX_ij + lambda_i DY_ij)/2=0`. Hence

`-<DX[h],DY[l]> = sum_(i in I,j in J) (mu_j/lambda_i)<DX_ij[h],DX_ij[l]>`.

The manuscript's sign, coefficient, positive semidefiniteness, symmetry, and rank bound apq are all correct. The proposed derivations also have the claimed normalization: `4[L_z,L_ci]ci=z` and `4[L_z,L_ci]cj=-z`. Exponentiating a linear combination of these derivations simultaneously realizes all the channels to first order.

### Quadratic representation and primitive perspective

The approximation argument for `rank_J P(x)c <= 1` is valid in every EJA: invertible elements are dense, invertible quadratic representations are cone automorphisms, these preserve extreme rays, and the nonnegative rank-at-most-one locus is closed. It does not use an associative matrix representation.

For w in V(c,1/2), write `w^2=t c+u`. Associativity of the trace inner product yields `t=||w||^2/2`; Peirce multiplication gives `P(w)c=u`, and `tr u=t`. For w nonzero, u is therefore `t k` for a primitive idempotent k orthogonal to c. The supports of w and w^2 agree spectrally, so w lies in V(c+k,1), and `k circ w=w/2`. The span of c,k,w has multiplication table

`c^2=c, k^2=k, c circ k=0, c circ w=k circ w=w/2, w^2=t(c+k)`.

Thus the relevant two eigenvalues have sum delta+z and product `delta*z-2t`; all remaining r-2 eigenvalues are z. This proves the determinant and positivity assertions, including zero endpoints and r=2. No exceptional-case obstruction appears: the rank-two face inside the Albert algebra is a spin algebra, and the proof only uses EJA identities.

Expanding `A P(c-g/(sqrt(2)A))c` gives precisely `A c-g/sqrt(2)+P(g)c/(2A)`. Its tail trace is `||g||^2/(4A)`. In particular the factors of two in the manuscript are consistent with the trace-inner-product normalization.

### Exact lift, coefficient constraints, and all support cases

The proposed affine slice is injectively parametrized by the displayed ball coordinates and auxiliary z variables; output x is an affine function of the cone coordinates. Cone positivity gives each z nonnegative, b at most one, and `sum ||w_G||^2 <= (1-b)(1+b)`. Conversely, the stated surplus allocation gives feasible z whenever b<1, including the south pole, and b=1 is handled separately. At x=0, z=1/q gives strict positivity in every full dictionary factor, including incomplete coordinate groups.

For arbitrary certificate blocks the whole-slice pairing is

`(1-b) sum A_G + sqrt(2) sum <w_G,u_G> + sum z_G tr H_G`.

Zero-sum z variations force a common tail trace gamma. Comparing the constant and b terms yields `sum A_G+gamma=1` and `-sum A_G+gamma=-eta`, so gamma=(1-eta)/2 and sum A=(1+eta)/2. These comparisons also remain valid when q=1.

For eta<1, each nonzero group g_G has the stated positive A_G and a rank-one completion with tail trace gamma. A zero group has A_G=0 and may use gamma times any primitive tail idempotent. The sums are correct because `sum ||g_G||^2=1-eta^2`. Every block of every certificate must be nonzero when gamma>0, proving the lower bound q even when some or all groups vanish. At eta=1, every tail block vanishes and positivity removes all half-Peirce components; one head coefficient gives rank one. At eta=-1, all heads vanish and all q tail certificates remain rank one. Extra orthogonal half-Peirce coordinates in an incomplete group cannot defeat the positive-tail-trace lower bound.

### Remaining Stage 1 reasoning

The minimum-rank fiber is semialgebraically selectable even though it need not be closed. The draft correctly uses general semialgebraic choice rather than minimum-norm selection for that fiber. Minimum norms are used only for convex closed fibers. Finite stratification yields the common dense open regular set; applying the rank bound to a rank-minimizing certificate there proves the assertion for all certificates in each such fiber. Rank extrema exist because the attainable ranks lie in a finite integer range.

The universal dimension-minus-two argument is valid. Minimal-face reduction and free-variable elimination preserve exactness; certificate normalization is supplied by Slater duality on the reduced cone. The dimension-capped tree construction has exactly s leaves, uses q factors of total dimension s-1+2q, and is relatively strictly feasible. Decomposing symmetric factors to obtain the ambient-rank lower bound is legitimate under a per-factor dimension cap.

## Literature check within this review's scope

The draft appropriately attributes the lift/factorization equivalence and ordinary Jordan algebra machinery, and qualifies the precise minimax novelty claim. I found no contrary result in targeted searches for curvature-based conic-lift lower bounds. That is not an exhaustive novelty certification. The primary-author publication list confirms the exact Gowda--Sznajder paper title, authors, volume, and pages used in the bibliography: https://userpages.umbc.edu/~gowda/papers/papers.html (entry 61). Its role here is background; the manuscript supplies its own proof of the specialized primitive perspective.

For the eventual full literature discussion, the distinction from Hamza Fawzi's *Limitations on the Expressive Power of Convex Cones without Long Chains of Faces* (SIAM J. Optimization, DOI 10.1137/19M1245670) would be useful context: it concerns obstructions to product-cone lifts from facial structure, whereas the current result extracts quantitative differential capacity and certificate rank at positively curved contacts. This is a contextual suggestion, not a mathematical defect in Stage 1.
