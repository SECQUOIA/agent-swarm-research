# Independent review of the strict-Hessian descent lemmas

Date: 2026-09-28. Scope: Lemmas 1–2, the SDP comparison, and the scope statements in
[the literature note](rational-sos-convex-descent-prior.md).
Both lemmas are correct. This review reconstructs their arguments; it
does not independently audit all the cited papers or the later
counterexample construction.

For Lemma 1, Taylor's integral has the correct weight and no missing
factor. At a minimizer the linear Taylor term vanishes. For every
$0<t<1$, the map

\[
 T_t(b,c)=(b,a\otimes b+tEc)
\]

is injective: its first block determines $b$, and with $b=0$ its second
block determines $c$ because $E$ is injective. Therefore integrating
$(1-t)T_t^{\mathsf T}MT_t$ gives a positive definite matrix on all
linear and distinct quadratic monomials in $x-a$. If $a$ is rational,
the integral is rational because its entries are integrals of rational
polynomials in $t$. Rational $LDL^{\mathsf T}$ and the four-square
theorem then give rational polynomial squares.

The positive-minimum branch also holds. Adjoining the constant yields
$\operatorname{diag}(m,J)\succ0$, and translation gives a positive
definite Gram matrix in the ordinary monomial basis. The coefficient
equations for that Gram matrix are rational linear equations. Their
nonempty real affine solution space has a rational parametrization and
dense rational points, so it contains a rational positive definite
matrix. This proves the descent step directly, without assuming either
$a$ or $m$ rational or independently auditing Hillar's proof.

For Lemma 2, the bottom principal block of $M$ is positive definite.
Comparing the quadratic terms in $x$ and using Euler's identity gives
$12F_4(x)>0$ for $x\ne0$. The full Hessian certificate also gives
$\nabla^2F(x)\succeq\lambda_{\min}(M)I$, so the affine zero is unique.
The homogenization is nonnegative and has exactly that one real
projective zero, since $F_4$ excludes zeros at infinity.

I checked the published statement of
[Scheiderer's Theorem 4.1, journal page 1507](https://ems.press/content/serial-article-files/32129),
and the paper's definition of general position. I did not independently
reprove the classification. Its application here is valid: a
nonnegative quartic with four distinct complex line factors in general
position has no real line factor, since a simple real factor changes
sign away from the other lines. Conjugation therefore pairs the lines
into two pairs. Each pair intersects in a real projective point, and
general position makes the points distinct. This contradicts the
unique-zero conclusion. Dehomogenization preserves rational SOS.

The added comparison with older non-descent examples is also correct.
Let a rational form $p$ be real SOS but not rational SOS, let $v$ be the
vector of monomials of half its degree, and put $R=v^{\mathsf T}v$.
The SDP minimizing $t$ subject to
$p+tR=v^{\mathsf T}Qv$, $Q\succeq0$, and $t\ge0$ has attained real
optimum zero. For any rational $t>0$, a real Gram matrix $Q_0$ for $p$
gives the strictly positive definite Gram matrix $Q_0+tI$ for $p+tR$.
Rational affine-space density gives a rational positive definite Gram
matrix for the same polynomial. Thus the SDP has rational Slater
points with objective arbitrarily close to zero, but no rational
optimizer: one would be a rational SOS Gram matrix for $p$. These
features alone therefore follow from older non-descent examples. This
comparison does not verify the later quartic construction or its
claimed additional structure.

Two minor wording corrections were requested in the reviewed draft:

- The opening annihilation claim must refer to every **positive
  semidefinite** Gram matrix. An arbitrary indefinite Gram matrix can
  have zero quadratic value at the evaluation vector without
  annihilating it.
- Lemma 1 should explicitly relax the opening minimum-zero assumption
  when introducing $m=F(a)$, so its positive-minimum branch is not
  apparently vacuous.

The warning about an irrational minimizer is correct: the hyperplane
of quadratics vanishing at $a$ has evaluation normal
$(1,a_i,a_ia_j)$ and need not be defined over $\mathbb Q$. Positive
definiteness in that translated space alone does not justify rational
descent. It also does not exclude a rational Gram matrix of smaller
rank. Lemma 2 uses a dimension-specific classification and makes no
higher-dimensional claim.

The initial draft's unresolved-case language must be limited to the
outcome of its literature search and updated to cross-reference the
separately reviewed construction reported during this review. Neither
these lemmas nor an unsuccessful search establishes novelty. The later
construction, its checker, the other source theorems, and the reported
Laplagne identity and Hessian calculations are outside this review's
independent verification.

Targeted verification consisted of reading the note, reconstructing
the two proofs and the SDP comparison, checking the stated Scheiderer
result, and an inline `python -` command checking this review's link,
display delimiters, newline,
whitespace, and control characters. The local check passed. No
project-wide checks or CI inspection were performed.
