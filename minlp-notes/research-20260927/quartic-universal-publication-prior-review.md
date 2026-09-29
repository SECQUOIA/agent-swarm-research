# Review of the universal convex-quartic publication audit

Date: 2026-09-28. Scope: novelty framing, significance, the moment
consequence, the degree bound, and the qualitative interpolation shortcut
in [the publication audit](quartic-universal-publication-prior.md).

No required mathematical correction was found in this scope. The
consequences follow from the stated hypotheses, and the publication
assessment distinguishes a candidate contribution from established
priority. This conclusion is conditional on the separately stated
quartic and Hessian-certificate theorems. This review does not certify
their full constructions or the newly added quantitative shortcut.
Earlier positive reviews were not used as evidence of correctness.

## Moment consequence

The displayed relaxation uses a truncated vector indexed by monomials
of degree at most four. Positive semidefiniteness of its order-two
moment matrix makes its functional nonnegative on every square of a
quadratic polynomial. Thus the supplied SOS identity gives a lower
bound of zero, and the Dirac vector at the prescribed zero attains it.

The exact hypotheses of Lasserre's Theorem 2.6 are an SOS-convex
polynomial of degree at most \(2r\), a normalized truncated functional,
and \(M_r(y)\succeq0\). No representing measure or flatness assumption
is required. Setting \(r=2\) gives the inequality used in the audit.
Its Theorem 3.3 additionally assumes attainment, Slater's condition,
and SOS-convexity of the objective and the negatives of the constraint
polynomials; the unconstrained application here has no constraint
qualification problem. [Primary text, Theorems 2.6 and 3.3](https://arxiv.org/pdf/0806.3784).

Consequently, every optimal vector has first moments equal to the
unique zero \(a\). If any coordinate of \(a\) is irrational, the
whole optimal moment vector cannot be rational. This conclusion does
not depend on uniqueness of higher moments. The audit correctly
separates rational optimal value and rational SOS certificate from
rationality of the primal optimizer. It also correctly avoids turning
this observation into a complexity lower bound.

An optional clarity edit is to state explicitly that \(y\) contains
moments through degree four. Another is to identify Lasserre's
relaxation as the simplified relaxation (3.3), rather than only the
first applicable relaxation. Neither changes the argument.

## Degree bound

The bound \([\mathbb Q(a):\mathbb Q]\leq2^n\) is valid with all
the hypotheses currently stated: rational quadratic SOS summands,
a real zero, and a positive definite Hessian there.

At that zero, the Hessian is twice the Gram matrix of the summand
gradients. Positive definiteness therefore supplies \(n\) rational
quadratics whose gradients are independent at \(a\). Their common
zero is nonsingular and isolated over \(\mathbb C\), so its
coordinates are algebraic. Every embedding of the coordinate field
gives another nonsingular zero of the same selected equations: the
Jacobian determinant is a nonzero field element and remains nonzero
under each embedding. Distinct embeddings give distinct tuples because
the coordinates generate the field.

Counting only isolated zeros is essential; the selected system need
not be globally zero-dimensional. The affine isolated-point bound
applies nevertheless. The cited Barone--Basu Section 1.3 explicitly
recalls the complex bound by the product of the equation degrees.
Here that product is at most \(2^n\). [Primary text, Section 1.3](https://www.math.purdue.edu/~sbasu/submission-12-july-2014.pdf).

This is a bound for rational quadratic SOS zeros with the Hessian
assumption, not an unrestricted arithmetic-degree theorem for every
convex quartic. The audit retains this distinction. The logarithmic
dimension lower bound does not imply that arbitrary permitted fields
have realizations attaining it.

## Qualitative interpolation shortcut

The shortcut is valid and correctly identified as an inference from
the literature. For a squarefree polynomial, KMS equation (4) makes
distinct Lagrange idempotents have product zero modulo the polynomial.
Specializing the expression in equation (6) to zero target and positive
complex-pair weights gives a real positive semidefinite Gram matrix.
With one real root, the real and imaginary coefficient vectors of the
nonreal Lagrange polynomials span a space of dimension \(d-1\), so its
kernel is exactly the real root evaluation vector. Proposition 2.2
and Corollary 2.4 assume strict positivity at real roots; they must not
be invoked directly at zero target. The audit makes that distinction.
[Primary text, Section 2.1, equations (4), (6)](https://arxiv.org/pdf/2112.00490).

The congruence-zero space is defined by rational linear equations.
Its rational points are dense, so approximation inside that space
preserves the zero exactly while preserving the positive definite
quadratic block and making the gradient small. Requiring the rational
approximant itself to be positive semidefinite would force it to be
zero: positive semidefiniteness implies that it kills \(v(\alpha)\),
and each rational row must then vanish by power-basis independence.

The final note now includes quantitative Vandermonde and projection
bounds and explicitly marks replacement of the construction lemma as
pending a fresh full proof review. Those bounds and the full bit-time
algorithm are outside this review's approval. Their appearance in the
audit must not be cited as independently verified here.

## Prior art and significance

The inspected version of *Hesse's Redemption* distinguishes irrational
quartic minimizers from the stronger absence of any rational zero-level
witness. Table 1 and Appendix C leave the latter quartic possibility
open; its degree-six example does not settle it at degree four. The
audit's comparison targets the right issue. The arXiv record inspected
again on this review date lists only the November 5, 2025 version.
[Primary text, Table 1 and Appendix C](https://arxiv.org/html/2511.03440v1#A3),
[version record](https://arxiv.org/abs/2511.03440).

The other principal comparisons also preserve their assumptions:

- Ahmadi--Chaudhry--Zhang Lemma 2 constructs an interior Hessian Gram
  certificate; Lemma 3 and Theorem 3 justify regularization of Taylor
  models. These results do not preserve a prescribed irrational zero
  over the rationals. [Primary text](https://arxiv.org/html/2311.06374v2).
- BKM's nonnegative case uses \(1\in(I:f)+(f)\); its height analysis
  in Sections 4--6 assumes a radical ideal. The audit's qualified
  description is accurate, and it does not infer polynomial time in
  arbitrary defining-system size from the height bounds.
  [Primary text, Section 1.3](https://arxiv.org/pdf/2410.04845v2).
- Peyrl--Parrilo Proposition 8 controls positivity after rational
  rounding and orthogonal projection. Crediting that method separately
  from the candidate's explicit Hessian matrix and precision bound is
  appropriate. [Primary text, Section 3](https://www.mit.edu/~parrilo/pubs/files/PeyrlParrilo-ComputingSumOfSquaresDecompositionsWithRationalCoefficients.pdf).
- Ahmadi--Hall Theorems 2--3 supply degree-preserving DC decomposition
  and interior Hessian certificates, without requiring preservation of
  a zero. Nie--Ranestad's generic critical-point degree counts likewise
  do not prescribe the field and minimum level. Their Example 3.1 is
  nonconvex, as its second derivative in the first coordinate at the
  origin is \(-26\).
  [Ahmadi--Hall primary text](https://www.princeton.edu/~aaa/Public/Publications/dcdv12.pdf),
  [Nie--Ranestad primary text, Section 3.1](https://arxiv.org/pdf/0802.1233).

The combined fixed-degree arithmetic realization is a reasonable
candidate for further publication assessment. The present review
establishes neither priority nor publication venue suitability. The
note appropriately limits solver implications to exact representation
and certification, and it avoids claims of a faster MINLP algorithm,
NP-hardness, or failure of NP membership.

## Verification record

I read the repository `AGENTS.md`, the main audit, its two construction
statements, and the linked field-necessity argument. Primary sources
were reopened at the specific results listed above. A separate
reviewer checked the moment and degree arguments independently.

Targeted local checks: `test ! -e` confirmed that this review filename
was unused before creation. An inline `python - <<'PY'` command checked
this review's final newline, trailing whitespace, control characters,
math delimiters, and local Markdown links. No project-wide verification
or CI inspection was run. The main audit was not edited by this reviewer.
