# Independent audit of rational witnesses and interior Gram output

Date: 2026-10-03. Verdict: the three stated results pass this audit under
their stated input and output conventions. No mathematical correction
is required. This is a fresh mathematical review, not a publication
priority determination or a formal proof.

The reviewed statements are:

- [Strictly feasible quartic witness lower bound](../../../research-20260927/strict-convex-quartic-rational-witness-lower-bound.md).
- [Positive definite ordinary Gram lower bound](../../../research-20260927/interior-gram-bit-lower-bound.md).
- [Singly exponential ordinary Gram upper bound](../../../research-20260927/interior-gram-single-exponential-upper.md).

I read these arguments directly. I also checked the needed parts of the
[signed root construction](../../../research-20260927/signed-odd-root-circuit-quartic.md),
the [strong convexity calculation](../../../research-20260927/general-strongly-convex-quartic-singleton.md),
and the [rational Hessian certificate construction](../../../research-20260927/sos-convex-quartic-realization.md).
The conclusions below do not rely on the verdicts in earlier review files.

## 1. Rational feasible coordinates

The small positive signal is encoded by a root circuit of length
\(k\), not by printing its digits. With \(M=1000^{k+3}\),
\[
\delta_0=M^{-1},\qquad
\delta_i=(1+3\delta_{i-1}^2)^{1/3}-1,
\]
positivity and the inequality \((1+t)^3\geq1+3t\) give
\(0<\delta_k\leq M^{-2^k}\). The supplied root intervals have
polynomial bit length. In particular, dependency-sensitive interval
evaluation of \(3\xi^2-6\xi+4\) on \([1-w,1+w]\) is contained
in \([1-13w,1+13w]\); the next interval has width \(1000w\).
Thus the certificate does not require resolving the tiny difference
\(\xi_k-1\) at input construction time.

For the cubic gates used here, the exposing identity can be checked
without the general odd-degree formulas. Writing \(\alpha^3=b(p)\),
the quadratic
\[
E=y^2-bx-\alpha(xy-b)+\alpha^2(x^2-y)
\]
vanishes at the retained powers \((\alpha,\alpha^2)\), even when
its two occurrences of \(\alpha\) are replaced consistently by a
rational approximation. Each of the rational relations
\(y^2-bx\), \(xy-b\), and \(x^2-y\) vanishes there separately.
At the exact coefficient value, its centered local quadratic part is
\[
\alpha^2 u^2-\alpha uv+v^2.
\]
Its matrix is at least \(I/2\) when \(\alpha\geq1\).
Signed affine predecessor terms add only cross terms. Geometrically
decreasing gate weights control those cross terms. The dependency's
small rational coefficient error then gives a positive quadratic part
and arbitrarily small gradient while preserving the zero exactly.

The subsequent square construction retains the negative Hessian
contributions of squared indefinite quadratics. Its Hessian Gram
proof establishes positivity on the full vector space of
\((v,X\otimes v)\), not only on vectors arising from evaluations of
monomials. Approximating and projecting this Gram onto its rational
coefficient equations is legitimate: those equations have mutually
orthogonal coefficient supports, and the explicitly bounded positive
margin exceeds the approximation error. This supplies the rational
positive definite \(M_0\) used in the witness theorem.

For a positive definite rational \(h\)-by-\(h\) matrix,
\[
\mu=\det(M_0)/(\operatorname{tr}M_0)^{h-1}
\]
is a positive rational lower bound on its smallest eigenvalue. Its
ordinary bit length is polynomial in the expanded matrix input.
Therefore \(\lambda=\lceil3/\mu\rceil\) is polynomial in bit
length, although its magnitude need not be polynomial. The rank-one
change \(\lambda M_0-2ee^{\mathsf T}\succeq I\) is valid on
the same full basis. This distinction between bit length and magnitude
is essential to the construction-size assertion.

At the algebraic zero \(p\) of the original SOS polynomial, put
\(u_*=\kappa\delta_k>0\). The perturbed quartic has value
\(-u_*^2\) and gradient norm \(2u_*\). Its strong convexity gives,
for every feasible point and \(r=\|X-p\|\),
\[
0\geq-u_*^2-2u_*r+r^2/2.
\]
Hence \(r\leq(2+\sqrt6)u_*<5\kappa M^{-2^k}\). The same
argument applies to boundary points. Strict feasibility, compactness,
and the constant coordinate bound all follow as stated.

The first coordinate \(\alpha=\kappa\xi_1\) is irrational of
degree three: \(M^{2/3}\) is an integer, and \(M^2+3\) lies
strictly between consecutive integer cubes. The displayed integers
\(A,B\), with \(\alpha^3=A/B\) and \(B<M^3\), need not be
coprime. For every rational coordinate \(a/b\), the nonzero integer
\(Ba^3-Ab^3\) still has absolute value at least one. The difference
of cubes and \(|a/b|,|\alpha|<3\) give
\[
b^{-3}\leq27B|a/b-\alpha|
 <270M^{3-2^k}.
\]
This proves the stated denominator lower bound without a Diophantine
approximation assumption. The asymptotic conclusion applies for
sufficiently large \(k\); a weak right-hand side for the first few
values does not affect it.

## 2. Positive definite polynomial Grams

For \(f_k=\lambda F+u^2\), the only zero of \(F\) is \(p\)
and \(u(p)>0\). Thus \(f_k\) is positive everywhere. Strong
convexity makes the minimum attained and positive. The small value
\(f_k(p)<4M^{-2^{k+1}}\) is an upper bound at a known algebraic
point; the argument does not assume that \(p\) minimizes \(f_k\).

The short rational PSD Gram follows directly from its weighted SOS
expression and has rank at most \(n+2<D=\binom{n+2}{2}\). Positive
rational weights can be expanded into ordinary rational squares with
polynomial total output size. Consequently this family cannot prove
an output lower bound for arbitrary PSD Grams or arbitrary rational
SOS certificates.

The existence of a positive definite rational Gram is also proved,
so the lower bound is nonvacuous. If the full Hessian Gram is at least
\(I\), choose a rational \(q\) near the minimizer with
\(c=f(q)-\|\nabla f(q)\|^2/2>0\). Taylor integration gives
\[
f=S_q+\tfrac12\|X-q+\nabla f(q)\|^2+c.
\]
After subtracting the constant Hessian block, the remaining Gram
dominates the identity on the full quadratic block. The integration
identity
\[
\int_0^1(1-t)(U+tV)^2dt
=\tfrac12(U+V/3)^2+V^2/36
\]
therefore supplies all quadratic factors \((X_i-q_i)(X_j-q_j)\).
Together with the affine factors and positive constant, they span
every polynomial of degree at most two. That full-span argument
establishes a positive definite ordinary Gram; mere positivity of
\(f\) would not suffice by itself.

The cube moment argument supplies a uniform norm bound for every PSD
Gram in the fixed full monomial basis. The centered-square moment
formula and the elementary inequality for the constant coefficient
give
\(\mathbb E[zz^{\mathsf T}]\succeq I/[15(n+1)]\).
Consequently \(\operatorname{tr}Q\leq15(n+1)\|f_k\|_1\).
This controls the other eigenvalues when the small Rayleigh quotient
at \(p\) bounds the smallest eigenvalue.

For \(Q\succ0\), these two facts give
\[
0<\det Q<4M^{-2^{k+1}}T_+^{D-1}.
\]
In a determinant permutation product, a symmetric off-diagonal entry
can occur at most twice. Therefore
\(\prod_{i\leq j}b_{ij}^2\) clears every denominator. The resulting
positive integer is at least one, proving the claimed lower bound on
the total denominator bits. Positive definiteness is indispensable:
the determinant of the short singular Gram is zero.

## 3. Singly exponential upper bound

I checked the primary rational-sampling statement directly in
[Basu, Pollack, and Roy, Theorem 4.1.2](../../../literature/papers/basu1996-on-the-combinatorial-and-algebraic/original.pdf),
printed pages 1031–1032. It gives coordinate numerator and denominator
bit bounds \(\tau d^{O(n)}\) in every component of a nonempty set
defined by strict integer polynomial inequalities.

For the supplied rational full Hessian Gram \(A\succ0\), the
determinant/trace bound \(\mu\) has polynomial bit length in the
combined input \(L\). The polynomial
\[
c(X)=f(X)-\|\nabla f(X)\|^2/(2\mu)
\]
has degree at most six and polynomial coefficient bit length after
clearing denominators. It is strictly positive at the minimizer.
The primary sampling theorem applies exactly to this nonempty open
set; no convexity of that set is required. It gives a rational center
with \(\operatorname{poly}(L)6^{O(n)}\) bits per coordinate.

The explicit Taylor Gram formula then uses matrices of polynomial
dimension and rational expressions of fixed degree in that center.
Its positive definiteness follows from the same quadratic, affine,
and constant spanning argument. Rational LDL factorization and binary
expansion of positive weights increase total encoding length only
polynomially. The resulting bound is
\(\operatorname{poly}(L)2^{O(n)}\), as stated.

This is an upper bound with the expanded rational Hessian Gram counted
in the input. It is not an upper bound for every strictly positive
SOS quartic, and it is not a polynomial-time construction in \(L\)
alone. The use of the original variable dimension \(n\), rather
than the ordinary Gram dimension \(D=\Theta(n^2)\), is justified
because the sampled open set lives in the original variables.

## 4. Claims that must remain separate

| Output or parameter | Supported conclusion |
| --- | --- |
| Expanded rational feasible coordinates | Some bounded strictly feasible bodies require \(\Omega(n2^{n/2})\) bits. |
| Expanded rational positive definite ordinary Gram | The lower family requires \(\Omega(n2^{n/2})\) total denominator bits. |
| Arbitrary rational PSD Gram or SOS certificate | The same family has a polynomial-size certificate. |
| Total constructed input length | The lower bounds are superpolynomial; \(2^{\Omega(L)}\) is not proved. |
| Supplied full positive definite Hessian Gram | Some interior ordinary Gram has \(\operatorname{poly}(L)2^{O(n)}\) expanded bits. |
| Compact arithmetic or algebraic descriptions | These encoding lower bounds do not rule them out. |
| Decision complexity or NP membership | Neither output lower bound settles it. |

The ordinary polynomial Gram and the Hessian Gram represent different
polynomials in different bases. A short well-conditioned Hessian Gram
does not imply a short interior ordinary Gram. A change of basis whose
own coefficients are long also cannot be ignored in an encoding claim.

The paired bounds make exponential dependence on dimension
qualitatively necessary and sufficient for interior Grams in the
supplied-Hessian class. They do not match exponent constants, resolve
the all-PSD frontier, or establish publication priority.

## 5. Targeted verification actually run

All commands below passed:

```text
python research-20261003-arithmetic/reviews/exact-core/check_witness_output_audit.py
python research-20260927/check_strict_quartic_witness_lower_bound.py
python research-20260927/check_interior_gram_bit_lower_bound_review.py
pdftotext -f 30 -l 31 -layout literature/papers/basu1996-on-the-combinatorial-and-algebraic/original.pdf -
```

The new diagnostic checks the cubic exposing identity, the Taylor
integration constants, and the full rational Taylor Gram on a
two-variable quartic with a nonzero rational center and nonzero
gradient. Exact rational LDL decompositions check positive
definiteness in that instance. The existing diagnostics check the
root-box arithmetic, localization constants, rank-one Gram changes,
and cube moments in small dimensions. These finite diagnostics do
not substitute for the general proofs reviewed above. No project-wide
verification or CI inspection was performed.
