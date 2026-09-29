# Independent proof review of the quartic arithmetic reductions

Date: 2026-09-28. Status: proofs pass independent adversarial review.
The author added an explicit empty-list case and made the radius lemma's
smoothness assumption precise in response to this review. Both repairs
were independently rechecked.

This review covers [the arithmetic reduction](quartic-exact-arithmetic-reductions.md)
and, separately, Section 4 of the
[odd-radical complexity audit](odd-radical-sum-complexity-prior.md).
It treats the previously reviewed dense-input quartic realization and
rational Hessian-certificate construction as dependencies. It does not
repeat their full proofs or establish novelty, hardness, or completeness
of the literature search.

## Reduction, certificates, and input length

Let the input polynomials have degrees \(d_i\). The existing construction
produces a nonnegative quartic on \(d_i-1\) coordinates when \(d_i>1\),
with the required powers of the unique real root as its only zero.
For a rational root \(a\), the proposed block

\[
                  (u-a)^2+(u-a)^4
\]

has the asserted properties. Its Hessian Gram matrix on \((y,uy)\) is

\[
 \begin{pmatrix}2+12a^2&-12a\\-12a&12\end{pmatrix},
\]

whose determinant is \(24\); this supplies an explicit rational positive
definite certificate even for that branch.

On disjoint blocks, \(F=\sum_i F_i\) is nonnegative and vanishes exactly
at the product tuple. Thus the added affine inequality makes feasibility
equivalent to the original weak signed comparison, including equality.
The Hessian of \(F\) is block diagonal and at least the identity. Its
rational SOS identity and Hessian Gram certificate are obtained by
embedding the individual certificates in the selected block basis.

The full basis \((y,z\otimes y)\) generally cannot have a positive
definite Gram matrix. For different blocks, the coefficient of

\[
                         z_{i,r}^2y_{j,s}^2
\]

is zero. The only product of two full-basis monomials equal to this
monomial is the square of \(z_{i,r}y_{j,s}\), so its Gram diagonal must
be zero. This obstructs positive definiteness and is consistent with a
PSD Gram matrix obtained by embedding the block certificates. It does
not affect global strong convexity.

If \(L_i\) is the dense input length for block \(i\), all degrees and
coefficient lengths count toward \(L_i\). The sum of polynomial block
costs is polynomial in \(\sum_i L_i\). Fixed degree four also makes a
dense coefficient vector in the total number of variables polynomial
in that number. The reduction never expands the compositum or the
minimal polynomial of the sum. Its cost therefore does not assume that
their degrees are polynomially bounded.

The empty input list needs an explicit convention. Taking the empty
sum literally gives \(F=0\), contradicting the stated exact degree four.
A dummy block \(F(t)=t^2+t^4\) and affine function zero resolves this
without changing the comparison \(0\leq b\). Alternatively the source
can be explicitly restricted to nonempty lists. Perfect-cube terms can
be retained as rational blocks, so removing them need not create a
separate exception. The final note now includes the dummy-block case.

For the optimization version, global strong convexity makes \(F\)
coercive. A nonempty closed affine halfspace therefore has an attained
minimum; strict convexity makes it unique. The value is zero precisely
when the distinguished tuple satisfies the affine row. No positive
lower bound of inverse polynomial bit size follows merely from these
facts.

## Field closure and the scope of the obstruction

The signature arguments pass with the chosen fields viewed as subfields
of \(\mathbb R\). A real embedding of their compositum restricts to a
real embedding of every generating field. If every such field has one
real embedding, each restriction is its inclusion, so the compositum
embedding fixes every generator and is itself the inclusion.

If \(K\) has one real embedding and

\[
                  \beta^{2r+1}=a\in K,
\]

every real embedding of \(K(\beta)\) fixes \(K\) and must send
\(\beta\) to the unique real root of this equation. Therefore the
extension also has one real embedding. This proof does not require
\(T^{2r+1}-a\) to be irreducible over \(K\).

The passage to a subfield is slightly less immediate and is important.
A number field with one real embedding has odd degree. Hence for
\(L\subseteq K\), the degree \([K:L]\) is odd. Write \(K=L(\theta)\).
Under any real embedding of \(L\), the minimal polynomial of \(\theta\)
becomes an odd-degree real polynomial and has a real root. It extends
the embedding to a real embedding of \(K\). Since \(K\) has only one,
so does \(L\). Thus rational arithmetic and real odd-root adjunctions
preserve the required condition for the final output as well as the
field containing all intermediate values.

In particular, these fields cannot contain \(\sqrt2\), and cannot
contain any irrational totally real element. This excludes an exact
coordinate or rational-function realization of such an element. It
does not exclude transforming an instance into another number with the
same sign, and therefore does not exclude arbitrary decision reductions.

The nested cube-root example also passes: Eisenstein at two proves that
\(T^{3^m}-2\) is the minimal polynomial of \(2^{1/3^m}\). The dense
list has exponentially many coefficients, whereas the expression uses
only \(m\) nested root operations. This refutes the proposed inference
from qualitative field closure to a polynomial-time invocation of the
dense theorem. It does not prove that every other construction must
have exponential size.

## Radius and failed gate lifting

For a \(C^2\) function with Hessian at least the identity and minimizer
\(a\), strong monotonicity gives

\[
              -\nabla F(0)^{\mathsf T}a\geq\|a\|^2.
\]

Cauchy--Schwarz proves the stated radius bound, including \(a=0\).
For an explicit rational polynomial in \(N\) variables with coefficient
bit length at most \(B\), its linear coefficients give

\[
              \|a\|\leq\|\nabla F(0)\|\leq\sqrt N\,2^B.
\]

This prevents polynomial-size normalized constructions from preserving
the unscaled coordinate \(2^{2^m}\) produced by repeated squaring.
It does not prevent rescaling, reciprocal coordinates, or sign-only
encodings. The phrase “differentiable and with a global Hessian bound”
was replaced by “twice continuously differentiable” in the final note,
which makes the calculus assumptions explicit.

I also checked the cited
[Slot--Steurer--Wiedmer Theorem 1.1](https://arxiv.org/html/2511.03440v1)
in the primary text. Its minimizer-radius statement supports the
corresponding consequence for a single explicitly encoded rational
convex polynomial, including minimization over all of \(\mathbb R^N\).
It is not a radius assertion for arbitrary systems of several nonlinear
convex inequalities.

The gate counterexample is correct. For

\[
 H(x,y)=x^2+x^4+\varepsilon(y-x^2)^2,
\]

one has \(H_{xx}(0,y)=2-4\varepsilon y\), and this equals \(-2\)
at \(y=1/\varepsilon\). No positive residual weight makes this
polynomial globally convex. The underlying equations \(x=0\) and
\(y-x^2=0\) nevertheless have Jacobian equal to the identity at their
unique zero. Thus local nonsingularity does not rescue this naive
lifting argument.

## Separate review of the cube-sum upper bound

Section 4 of the odd-radical audit proves a many-one reduction to
PosSLP, not a hardness reduction from PosSLP. Its proof passes.

After integer normalization, the sum \(S\) is an algebraic integer in
a field \(K\) of degree \(D\leq3^m\). Every embedding sends each cube
root to a root of the same modulus, so every conjugate of \(S\) has
modulus below \(2^h\). For \(S\ne0\), its field norm is a nonzero
integer. Consequently

\[
 |S|\geq H^{-(D-1)}\geq2^{-h(D-1)}\geq2^{-h3^m}=\delta.
\]

Using a larger-than-necessary degree in this bound is harmless. No
primitive element or norm need be computed by the algorithm.

The Newton relative-error identity and its two bounds are exact:

\[
 e_{\rm new}=\frac{e^2(3+2e)}{3(1+e)^2}
             \leq\min\{2e/3,e^2\}\qquad(e\geq0).
\]

The warm-up count \(2b+2\) makes the error less than \(1/2\).
The further count in the audit is polynomial and makes the absolute
weighted-sum error less than \(\delta/8\). Therefore the offsets
\(\widehat S-\delta/2\) and \(\widehat S+\delta/2\) correctly
handle strict and weak comparison, including the case \(S=0\).

The crucial encoding step is valid. The exponent \(h3^m\) has polynomial
binary length, so a circuit constructs its power of two with polynomially
many gates. Newton iterates need not be expanded as binary rational
numbers. More explicitly, if \(x=P/Q>0\), the update is represented by

\[
           P'=2P^3+aQ^3,\qquad Q'=3P^2Q.
\]

Both integers stay positive. The weighted sum and the offset can then
be combined over a positive denominator; its integer numerator is the
PosSLP output. Shared gates keep the construction polynomial even when
expanded integers would have exponentially many bits. These observations
also explain why bounded-precision numerical sampling would not verify
the general reduction.

## Checks actually run and remaining scope

Three targeted inline `python - <<'PY'` commands used exact SymPy or
`fractions.Fraction` arithmetic. They passed:

- The gate Hessian identity and its negative-curvature specialization;
  absent cross-block Hessian monomials; rational-block affine evaluations.
- The sum of the repository's explicit cubic-root quartic and its
  reflected copy, evaluated modulo \(r^3-2\), with the affine boundary
  \(r+(-r)=0\) and thresholds \(0,1/100,-1/100\).
- The Newton error identity, both global error inequalities, 100 exact
  warm-up bounds, and 12 numerator/denominator recurrence updates.

These checks support specific identities and edge cases. General
convexity, the norm separation, input-size bounds, and field statements
are justified by the proofs above and their stated dependencies, not by
the finite probes. No Lean proof, project-wide tests, or CI inspection
was performed for this review.

A further inline standard-library Python check passed final-newline,
whitespace, control-character, math-delimiter, and local-link checks for
this review. It also checked the final main note for both requested
boundary and smoothness corrections.

The source problem's precise hardness remains unestablished here. The
reduction has a valid conditional algorithmic implication, but neither
an exact-solver lower bound nor a practical speedup has been proved.
