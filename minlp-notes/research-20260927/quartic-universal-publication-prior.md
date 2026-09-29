# Publication audit of arithmetic realization by convex quartics

Date: 2026-09-28. Status: independent literature and significance audit;
publication priority is not established. The full construction and its
quantitative proof have separate reviews.

The strongest candidate contribution is an effective arithmetic
classification: every real algebraic number with exactly one real
conjugate can occur at rational minimum zero in a rational, globally
strongly convex quartic, with rational certificates of both
nonnegativity and SOS-convexity. Neither high algebraic degree alone nor
the existence of an irrational convex minimizer is a suitable novelty
claim. Several ingredients have close primary precedents, including an
arithmetic shortcut described below.

The theorem could support a substantial contribution to exact convex
polynomial optimization if its priority survives wider review. Its
current solver relevance is a limitation on exact witness formats and a
source of structured certification examples. It does not establish a
faster MINLP algorithm or a complexity lower bound for exact decision.

## Precise result and the useful comparison

The [quartic construction](general-strongly-convex-quartic-singleton.md)
and [Hessian certificate](sos-convex-quartic-realization.md) take a dense
irreducible polynomial \(p\in\mathbb Q[T]\), of degree \(d>1\), with
exactly one real root \(\alpha\). In polynomial bit time they produce a
quartic \(F\in\mathbb Q[x_1,\ldots,x_{d-1}]\) satisfying

\[
 F^{-1}(0)=\{(\alpha,\alpha^2,\ldots,\alpha^{d-1})\},
 \qquad \nabla^2F(x)\succeq I\quad(x\in\mathbb R^{d-1}).
\]

The output includes \(d\) rational quadratic squares summing to \(F\)
and a rational positive definite Gram matrix for its Hessian biform on
the basis \((y,x\otimes y)\). These are different certificates: the
polynomial itself cannot have a positive definite Gram matrix on a basis
containing the constant monomial because it has a real zero.

The field restriction is necessary even for unique minimizers of
rational convex polynomials without a rational minimum. Their real
critical set is the singleton minimizer. Every real embedding of its
coordinate field preserves the rational gradient equations, hence fixes
the full tuple. The field has one real embedding and odd degree. A
coordinate subfield also has one real embedding: each of its real
embeddings extends to a real embedding of the full field because the
relative degree is odd. The detailed argument appears in the
[singleton audit](singleton-field-characterization-prior.md).
The candidate supplies an effective converse at fixed degree four with
a rational zero level and certificates.

Degree four is minimal for an irrational unique minimizer among globally
convex rational polynomials. A globally convex polynomial of degree at
most three has degree at most two: its affine Hessian cannot remain
positive semidefinite on every line if its linear part is nonzero.
A quadratic with a unique unconstrained minimizer has an invertible
rational Hessian, so its minimizer is rational. This degree observation
is elementary and is not presented as new.

## Closest primary results

**Slot, Steurer, and Wiedmer, Hesse's Redemption (2025).** The inspected
November 5, 2025 version proves polynomial-time approximate convex
polynomial optimization over rational polyhedra. Table 1 leaves compact
rational witnesses for exact convex-quartic feasibility unresolved.
Appendix C gives an irrational quartic minimizer and a convex sextic
with rational minimum zero at an irrational point; Lemma C.3 excludes
the latter phenomenon for univariate quartics. The repository's
bivariate quartic already settles that particular rational-point
possibility negatively. The general construction adds arbitrary
admissible fields, uniform effective realization, strong convexity, and
certificates. The arXiv submission history inspected on the audit date
listed only v1; this does not exclude later results elsewhere.
[Primary text](https://arxiv.org/html/2511.03440v1),
[version record](https://arxiv.org/abs/2511.03440).

**Ahmadi, Chaudhry, and Zhang, Higher-Order Newton Methods with Polynomial
Work per Iteration (2023, v2 inspected).** Lemma 2 proves interior
SOS-convexity of \(\|x\|^2+\|x\|^{2k}\) with a positive definite
Hessian Gram matrix. Lemma 3 and Theorem 3 establish SOS-convex
regularization of Taylor models with a positive definite Hessian at the
center; cubic models receive a quartic regularizer. Their Schur-complement
and interiority arguments are direct technical predecessors. They do
not state arithmetic realization or preservation of an irrational zero
with rational coefficients. In particular, adding
\(t\|x-c\|^4\) at a rational center changes the gradient at a distinct
prescribed point. Centering it at that point generally loses rational
coefficients. [Primary text, Sections 2--4](https://arxiv.org/html/2311.06374v2).

**Krick, Mourrain, and Szanto, Univariate Rational Sums of Squares
(2023).** Section 2.1 uses Lagrange interpolation at real roots and
complex-conjugate pairs, then rational rounding and projection in a
Gram affine space. Proposition 2.2 and Corollary 2.4 require strict
positivity at the real roots. Their formulas also suggest the boundary
construction below, but that specialization is an inference, not a
stated application of those propositions. Their conclusion explicitly
leaves bit-complexity estimates for future work. The general quartic
construction should credit this arithmetic machinery and distinguish
its global convexification from it.
[Primary text](https://arxiv.org/pdf/2112.00490).

**Baldi, Krick, and Mourrain, An Effective Positivstellensatz over the
Rational Numbers for Finite Semialgebraic Sets (v2, August 28, 2025).**
This successor treats rational SOS representations modulo
zero-dimensional ideals, including nonnegative data under suitable
conditions. Sections 4--6 give height bounds, including Vandermonde
conditioning and rational projection; Section 7 gives an algorithm.
Relevant statements are Lemma 4.9, Corollary 4.13, Proposition 5.3,
and Appendix Lemma A.2.
It is stronger quantitative prior than the univariate paper alone.
These are certificates on a finite algebraic set, not globally convex
quartic realizations of that set. Existence of a bounded-height
certificate must not be silently identified with a polynomial-time
algorithm in the original defining-system size: quotient dimension can
be large. [Primary text](https://arxiv.org/pdf/2410.04845v2).

**Peyrl and Parrilo, Computing Sum of Squares Decompositions with Rational
Coefficients (2008).** Section 3, especially Proposition 8, gives exact
rational Gram certificates by rounding and orthogonal projection when
the positivity margin dominates the errors. This is direct prior for
the final rationalization of the Hessian Gram matrix. The candidate
must receive credit for its explicit matrix and polynomial precision
bound, not for rational Gram projection itself.
[Primary text](https://www.mit.edu/~parrilo/pubs/files/PeyrlParrilo-ComputingSumOfSquaresDecompositionsWithRationalCoefficients.pdf).

**Ahmadi and Hall, DC Decomposition of Nonconvex Polynomials with
Algebraic Techniques (2018).** Theorem 2 and Corollary 1 decompose every
polynomial of degree at most \(2k\) into a difference of two
SOS-convex polynomials of that degree, even with stronger diagonal
dominance certificates. Theorem 3 constructs an interior Hessian Gram
certificate. This is earlier degree-preserving convexification prior;
it does not require preservation of a prescribed zero or stationary
point. [Primary text, pages 13--14](https://www.princeton.edu/~aaa/Public/Publications/dcdv12.pdf).

**Nie and Ranestad, Algebraic Degree of Polynomial Optimization (2008).**
Section 3.1 gives the generic unconstrained degree \((D-1)^n\) for an
objective of degree \(D\); Example 3.1 has quartic degree 81 in four
variables. Its displayed polynomial is not convex. Generic complex
critical-point counts do not prescribe a coordinate field or a rational
minimum. Nevertheless, high algebraic degree in polynomial optimization
is established prior. [Primary text](https://arxiv.org/pdf/0802.1233).

**Lasserre, Convexity in Semialgebraic Geometry and Polynomial Optimization
(2009).** Theorem 2.6 proves Jensen's inequality for a normalized
functional positive on squares and an SOS-convex polynomial. Theorem 3.3
gives exactness of the first applicable moment relaxation and recovery
from its first moments under its hypotheses. Thus one SDP suffices for
SOS-convex optimization in this representational sense. It does not say
that the exact optimal moment vector is rational or polynomially
encodable in every format. The quartic construction is consistent with
this result. [Primary text](https://arxiv.org/pdf/0806.3784).

The [earlier scoped audit](general-quartic-realization-prior.md) also
compares Bienstock--Del Pia--Hildebrand's restricted-domain irrational
cubic zero, Kurdyka--Spodzieja's positive-polynomial convexification,
and Zhu--Cartis's regularized quartic SOS results. Those comparisons
remain relevant; this audit does not claim a fresh full reading of all
three papers. The primary Ahmadi--Hall 2026 critical-point paper was
checked for a later equivalent result. Its nonconvex hardness
constructions do not supply the present arithmetic realization.
[Ahmadi--Hall primary text](https://arxiv.org/html/2601.21917v1).

## An arithmetic shortcut identified during this audit

This is a proof simplification inferred from the interpolation machinery,
not a claim that the prior literature states the quartic theorem. Let
\(v(T)=(1,T,\ldots,T^{d-1})^{\mathsf T}\) and

\[
 \mathcal L=\{B=B^{\mathsf T}:v(T)^{\mathsf T}Bv(T)
                                      \equiv0\pmod p\}.
\]

The complex-pair Lagrange terms give a real \(R_*\in\mathcal L\)
with \(R_*\succeq0\) and kernel \(\mathbb Rv(\alpha)\).
Its restriction to \(z_0=0\) is positive definite. Approximate \(R_*\)
by rational \(B\in\mathcal L\), and set
\(G(x)=(1,x)^{\mathsf T}B(1,x)\). Then \(G(a)=0\), its quadratic
part remains positive definite, and \(\nabla G(a)\) tends to zero.
This supplies the qualitative input to the quartic proof without a
companion sandwich or a two-parameter pencil. Rational \(B\) need not be
positive semidefinite; demanding that would destroy the construction.

Here is the quantitative argument developed during this audit. It is
an assessed elementary corollary, **pending a fresh full proof review
before replacing the input lemma in the main construction**. The
global quartic convexification still uses the separate estimates in the
main notes.

Let \(R\geq1\) bound all root moduli and let \(\sigma>0\) be a
lower bound on distances between distinct roots. Write
\(u_\beta(T)=c_\beta^{\mathsf T}v(T)\) for the Lagrange polynomial
at root \(\beta\), and choose one root from each nonreal conjugate
pair. Define

\[
 R_*=2\sum_{\text{pairs }\beta}
 \bigl(\operatorname{Re}c_\beta
          (\operatorname{Re}c_\beta)^{\mathsf T}
       +\operatorname{Im}c_\beta
          (\operatorname{Im}c_\beta)^{\mathsf T}\bigr),
 \qquad K=dR^{d-1}.
\]

Products \(u_\beta u_{\bar\beta}\) vanish modulo \(p\), proving
the congruence defining \(\mathcal L\). The real matrix
\(W=[c_\alpha,\sqrt2\operatorname{Re}c_\beta,
\sqrt2\operatorname{Im}c_\beta]_{\text{pairs}}\) is obtained from
the inverse transpose of the complex evaluation Vandermonde matrix by
a unitary change of columns. The Vandermonde norm is at most \(K\),
so \(\sigma_{\min}(W)\geq K^{-1}\). Deleting its first column
does not decrease the least singular value of the resulting injective
matrix. Thus every nonzero eigenvalue of \(R_*\) is at least
\(K^{-2}\); its kernel is exactly \(\mathbb Rv(\alpha)\).

For \(z_0=0\), the squared distance of \(z\) from that kernel is
at least \(\|z\|^2/\|v(\alpha)\|^2\), since the first coordinate
of \(v(\alpha)\) is one. Consequently

\[
 R_*|_{\{z_0=0\}}\succeq K^{-4}I,
 \qquad
 \|R_*\|_2\leq
 d\left(\frac{1+R}{\sigma}\right)^{2d-2}.
\]

The second bound follows by expanding each numerator
\(\prod_{\gamma\ne\beta}(T-\gamma)\): its coefficient
one-norm is at most \((1+R)^{d-1}\), while the denominator
\(\prod_{\gamma\ne\beta}(\beta-\gamma)\) has modulus at least
\(\sigma^{d-1}\). Bounding the sum of the squared column norms
then bounds the Gram norm.

Take a rational symmetric approximation within Frobenius distance
\(\delta\) of \(R_*\), then project orthogonally onto
\(\mathcal L\). Projection is rational linear algebra, because
remainder modulo \(p\) gives rational linear equations; it is
nonexpansive and fixes \(R_*\). The resulting rational \(B\) has
the same error bound. In \(G(a+u)=\eta^{\mathsf T}u+u^{\mathsf T}Hu\),
this gives

\[
 H\succeq(K^{-4}-\delta)I,
 \quad
 \|H\|_2\leq d\left(\frac{1+R}{\sigma}\right)^{2d-2}+\delta,
 \quad \|\eta\|_2\leq2K\delta.
\]

Hence \(\delta\leq\min\{(2K^4)^{-1},\varepsilon/(2K)\}\)
suffices. Dense rational input permits root and separation bounds with
polynomial bit length. Certified complex-root approximation, evaluation
of the Lagrange coefficient formulas, and exact rational projection
then require polynomially many bits, including the requested
\(\log(1/\varepsilon)\). Denominators in those formulas stay bounded
away from zero by powers of \(\sigma\), so their precision loss has
polynomial bit length. No semidefinite oracle is needed. The BKM
conditioning and projection results cited above are close quantitative
precedents, not a substitute for checking this specific algorithm.

## What the theorem does and does not establish

The conjunction of fixed degree, rational zero level, arbitrary
admissible coordinate field, global strong convexity, and short rational
certificates is the plausible publication-level advance. It settles a
natural arithmetic classification within a regular and certifiably
convex class. A title or abstract should emphasize that conjunction.

The exact feasible set \(\{F\leq0\}\) has no rational point for
irrational \(\alpha\). Thus strong convexity and a short rational
Hessian certificate cannot justify an exact solver that always returns
a rational feasible point. This obstruction already occurs in the
explicit bivariate example. Universality shows it is not confined to
one cubic extension.

There is a precise moment consequence. Consider

\[
 \min\{L_y(F):y_0=1,\ M_2(y)\succeq0\}.
\]

The rational SOS expression proves its value is at least zero; the
Dirac moments at \(a\) attain zero. For every optimal \(y\), the
Jensen inequality cited above gives \(F(L_y(x))\leq L_y(F)=0\), hence
\(L_y(x)=a\). Therefore no rational optimal moment vector exists when
\(a\) is irrational, although the SOS lower-bound certificate and value
zero are rational. This is an immediate combination with established
moment theory, not a new SDP exactness theorem. It does not assert that
all optimal higher moments are unique.

The construction does not prove NP-hardness, failure of NP membership,
or superpolynomial complexity of exact decision. Its own zero has a
short algebraic description supplied by the input polynomial and power
coordinates. It does not rule out polynomial-size algebraic witnesses
for more general convex quartics. Approximate optimization remains
compatible with the theorem: a small positive objective tolerance permits
rational points near the zero.

The coefficients and certificates have polynomial bit length but need
not have small numerical magnitude or favorable condition numbers.
Normalizing the strong-convexity constant does not bound the Hessian
above. The zero level is also fragile under an arbitrary constant
perturbation: subtracting a positive constant gives a set with interior,
and adding one makes the zero sublevel empty. Convexity certification is
regular here; exact zero feasibility is still a boundary question.

## Dimension is a remaining limitation

An elementary degree bound gives useful context. Suppose
\(F=\sum_i q_i^2\), with rational polynomials \(q_i\) of degree at
most two, \(F(a)=0\), and \(\nabla^2F(a)\succ0\). Then

\[
 [\mathbb Q(a):\mathbb Q]\leq2^n.
\]

Indeed every \(q_i(a)=0\), and
\(\nabla^2F(a)=2\sum_i\nabla q_i(a)\nabla q_i(a)^{\mathsf T}\).
Choose \(n\) summands with independent gradients. Their Jacobian
determinant is nonzero at \(a\), and at every conjugate tuple, because
it is a nonzero element of \(\mathbb Q(a)\). These distinct tuples
are isolated simple complex zeros of \(n\) rational quadratics.
The isolated-root version of the affine Bezout bound gives at most
\(2^n\) such zeros, even if other components exist. Algebraicity follows
already from the nonsingular rational polynomial system. This is a
standard Jacobian-and-Bezout consequence; no novelty is claimed.
The relevant complex isolated-point bound is explicitly recalled in
[Barone--Basu, Section 1.3](https://www.math.purdue.edu/~sbasu/submission-12-july-2014.pdf).
Alternatively, a sufficiently small generic perturbation preserves all
these nonsingular zeros, and ordinary projective Bezout bounds the
perturbed system. The degree argument was independently checked by the
delegated arithmetic reviewer.

The construction uses \(n=d-1\), whereas the bound only forces
\(n\geq\lceil\log_2d\rceil\). It neither optimizes the dimension
nor shows that every field can attain this lower bound. Compressing
arbitrary field realization while retaining rational certificates is a
potentially stronger question. A lower bound alone is not evidence that
such compression is possible.

## Search record and review limits

The audit read both candidate notes, the earlier prior audit, the
explicit-example root audit, and the primary sections identified above.
An independently delegated arithmetic search identified the
Baldi--Krick--Mourrain successor and the interpolation shortcut.
Queries included combinations of `convex quartic`, `irrational
minimizer`, `rational minimum`, `unique zero`, `one real root`,
`one real embedding`, `prescribed minimizer`, `algebraic degree`,
`SOS-convex`, and `universality`. Citation following covered rational
SOS modulo ideals, rational Gram recovery, and exact moment extraction.
Results about convex algebraic regions, polytope realization spaces,
and homogeneous convex forms were not treated as equivalent statements
about globally convex nonhomogeneous polynomial functions.

No inspected primary theorem gives the entire construction. That is a
bounded search outcome, not a proof of novelty. The main remaining
publication tasks are an integrated proof using the simplest arithmetic
input, a careful attribution of the interpolation and regularization
ingredients, and wider expert or citation review of arithmetic
realization. The construction's proof review and exact calculations
remain necessary independently of this literature assessment.

Targeted verification for this audit: an inline `python - <<'PY'` check
verified final newline, whitespace, control characters, math-delimiter
balance, and relative Markdown links. This document audit is not a
verification of the universal quartic construction. No project-wide
verification or CI inspection was run.
