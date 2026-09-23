# Stage 3 independent review 1

Reviewed `sections/06-restricted-barriers.tex` and
`sections/07-concrete-barriers.tex`, using the certificate and compression
theorems in Sections 1–5 as dependencies. I reconstructed the arguments rather
than treating workbench notes or the author audit as proof authority.

## Conclusion

**No major mathematical issue found.** One minor wording correction is needed.
The unresolved narrow-cap classification and intrinsic norm-tree optimum are
explicitly delimited open questions, not missing steps in the theorems asserted
here. I found no reason to reject the topic or any Stage 3 main theorem.

## Required minor correction

1. **Identify the compressed Slater endpoint precisely.** In
   `06-restricted-barriers.tex`, lines 90–92 of this review's version, the phrase
   “The compressed interior endpoints are positive definite in their respective
   faces” is ambiguous and, if read as referring to both endpoints, false:
   `P(f_i) bar X_i` can be singular, and its nullity is exactly what is being
   measured. Replace the sentence with: “The compressed Slater endpoint
   `P(f_i) X_i^circ` is positive definite in `V_i(f_i,1)` whenever this algebra
   has positive rank.” The subsequent derivative conclusion is correct and
   needs no mathematical change.

## Reconstruction of the principal arguments

- **Boundary order in all Euclidean Jordan algebras.** The quadratic
  representation sending the Slater point to the unit is invertible and
  rank-preserving. The remaining segment is diagonalizable in one frame, so
  the determinant has exactly the claimed integral vanishing order. The
  gradient quotient converges to the sum of nullities. This applies to every
  completion in a projected fiber, not merely a selected point.

- **Recession with derivative control.** With support idempotent `c` of the
  recession direction, the Peirce-1 component is positive definite after
  division by `t`, and its inverse is `O(1/t)`. The Jordan Schur correction in
  the complementary algebra is therefore `O(1/t)`. The determinant polynomial
  has a positive leading coefficient for each fixed interior `sigma`, which
  justifies differentiating the logarithmic asymptotic twice on compact
  interior `sigma` intervals. For the direction
  `H=t D+sigma(X^circ-bar X)`, the iterated limits of the numerator's linear
  term and denominator are respectively `-(r+z)` and `r+z`. No uniform
  interchange of the two limits is needed. The proof correctly avoids relying
  on an undifferentiated bounded remainder.

- **Primary-source check.** I independently opened the author-hosted published
  Gowda–Sznajder paper at
  <https://userpages.umbc.edu/~gowda/papers/GOW10-01.pdf>.
  Theorem 2(ii)(b), printed page 1557, gives the Jordan Schur determinant
  identity; the decomposition and inverse in the Peirce subalgebra are defined
  on printed page 1554. The paper expressly includes the exceptional algebra.
  This citation supports the manuscript's use; the recession derivative
  argument itself is supplied by the manuscript.

- **Unbounded lifts and genuine certificates.** A recession direction belongs
  to the slice tangent space and has zero projected component. The genuine
  whole-slice certificate identity therefore annihilates it. Positive
  orthogonality puts the certificate in the complementary face. Orthogonality
  to a supported primal point survives compression there, giving compressed
  nullity at least certificate rank. Thus the additional recession rank unit
  follows without a regular selection assumption.

- **One-channel rigidity.** The correct hypothetical threshold is strictly
  below two, as written. Integral boundary orders force all genuine
  certificates to have rank one. Convexity of the complete certificate fiber
  makes it one ray, and the affine slack identity fixes its scalar. Slater
  bounds yield uniform compactness and exclude zero. Closed graph then gives
  continuity, and connectedness fixes the active product label. Equality of
  projective rays forces equality of support directions by evaluating first
  at the ball center. The only primitive-ray manifolds homeomorphic to the
  required sphere are precisely the matching spin cases, including the
  order-two classical isomorphisms.

- **Sequential one-channel product argument.** The use of compressed images
  of the *original full fibers* is essential and correct. These images remain
  compact and convex, with a closed graph on the compact support sphere.
  They exclude zero by their row identity on the remaining contact cylinder.
  If all their ranks were at most one, the same ray-normalization and
  injectivity argument would work on that cylinder; it does not require that
  every certificate of the restricted lift extend to the original lift.
  Proper faces cannot introduce a primitive capacity equal to the original
  maximum. The join identity therefore supplies two new rank units per source,
  and the final rank statement holds for every positive aggregate of the
  chosen rows, exactly as asserted.

- **Wide-cap proof and collapse refinement.** The homogenization argument
  genuinely excludes negative and zero heights using boundedness and
  pointedness. The face-codimension inequality and integer nullity budget force
  constant total nullity under the stated width condition. A maximal chord in
  a nontrivial compact fiber must leave its minimal face's relative interior,
  contradicting that constancy. Generic curvature saturation then forces the
  full-order corank-one pattern; persistence of its zeros and constant total
  nullity prevent label changes. Equal kernel tuples force equal projected
  support points through a genuine certificate. The projective-product
  cohomology contradiction is therefore legitimate. In the narrow-cap
  refinement, the lower-dimensional collapse set only proves a fixed generic
  pattern when its codimension is at least two. The paper correctly does not
  infer extension of the projective map across exceptional fibers.

- **Concrete barriers.** The tree root Schur-complement calculation and its
  two limiting constructions are consistent. The polyhedral section really
  meets the domain interior and has the stated independent active facets, so
  its arbitrary-barrier lower bound is not inferred merely from determinant
  multiplicity. The grouped box section has the same property. For the
  bounded-fiber projection lemma, an unbounded sequence above bounded
  projected points would create a vertical recession direction by normalized
  convex interpolation; hence local uniform boundedness is proved rather
  than assumed. The Hessian Schur complement and differentiated stationarity
  give the required derivative identities. Column packing has bounded closed
  fibers and the claimed matrix-epigraph gradient norm, with no hidden
  restriction that the number of columns be at most the row dimension.

## Scope and originality

These sections carefully separate selected certificates, full certificate
fibers, every primal completion, a specified restricted standard barrier, and
optimization over arbitrary barriers. The explicit repeated-block and rotated
examples prevent the common invalid transfers among those quantities.

No priority claim in these sections exceeds the supplied evidence. The final
introduction should retain the author's recorded distinction that norm-tree
root calculations and grouped/packed constructions already occur in the
repository's `central-path-cost` manuscript. Their self-contained reuse is
appropriate, but it should not be counted as newly discovered repository
material. This is a final integration requirement already recorded in the
workflow, not an additional Stage 3 proof defect.
