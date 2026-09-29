# Independent review of constructive common-field recovery

Date: 2026-09-27. Status: the complete saved
[construction](constructive-common-field-recovery.md) passes the independent
review below, including its subsequent input-model and sign-verification
clarifications. This review is conditional on the existing degree, height, and certified
approximation guarantees; it does not reprove the convex optimization
theorem supplying those guarantees.

## Input assumptions and primitive-element search

Let the intended real coordinates be \(\beta_1,\ldots,\beta_n\), and
let \(K=\mathbb Q(\beta_1,\ldots,\beta_n)\). The input guarantees must
include a bound \(\overline D\) on the **joint** degree \([K:\mathbb Q]\),
a bound \(H\) on the coefficient bit lengths of the primitive integer
minimal polynomials of the coordinates, and certified simultaneous
rational approximation of the intended coordinates to arbitrary
polynomially specified precision. Bounds on individual degrees alone do
not replace the joint-degree guarantee.

The approximation oracle must also return rationals of polynomial encoding
length. Otherwise merely reading arbitrarily padded outputs need not fit
the claimed overhead. The author added this condition after review; it
already follows from the polynomial-time oracle used in the optimization
application.

The [canonical-point construction](algebraic-witness-recovery.md)
supplies the joint bound through a uniform bound on the degree of every
rational linear form, not by multiplying or identifying individual
coordinate degrees. That distinction is essential.

For

\[
\alpha_k=\sum_{j=1}^n k^{j-1}\beta_j,
\qquad 0\le k\le (n-1)\overline D(\overline D-1)/2,
\]

with \(k^0=1\), the usual embedding-separation argument is valid.
Every pair of distinct embeddings gives a nonzero polynomial in \(k\)
of degree at most \(n-1\). The candidate list has more entries than
the resulting bound on bad integers. Recovering each candidate's minimal
polynomial and choosing one of largest degree therefore gives a primitive
element \(\alpha\), and determines the actual field degree
\(d=[K:\mathbb Q]\). The cases \(n=1\), \(d=1\), and rational or zero
coordinates cause no exception.

The coefficients \(k^{j-1}\) can be large in value, but their bit lengths
are \(O(n\log(n\overline D+2))\). Candidate count, coefficient encoding,
and the precision needed to form a linear combination are polynomial in
the stated parameters. The approximation error is amplified by at most
the sum of absolute coefficients, so adding the logarithm of that sum
to the requested coordinate precision is sufficient.

## Uniform height bound for recognized numbers

Write \(a_j>0\) for the absolute leading coefficient of the primitive
integer minimal polynomial of \(\beta_j\), and put
\(A=\prod_j a_j\). Then \(\log_2 A\le nH\), and every
\(A\beta_j\) is an algebraic integer. Cauchy's bound gives
\(|\sigma(\beta_j)|\le 1+2^H\le2^{H+1}\) for every embedding.

Suppose \(\alpha=\sum_j c_j\beta_j\), with integer
\(|c_j|\le2^C\). For every coordinate \(\beta\) and integer
\(0\le s\le d\), the number \(\gamma_s=\alpha+s\beta\) satisfies

\[
A\gamma_s\text{ is integral},\qquad
|\sigma(\gamma_s)|\le M:=(n2^C+d)2^{H+1}.
\]

If its monic minimal polynomial is \(p_s\) of degree \(e_s\), then
\(A^{e_s}p_s\in\mathbb Z[T]\), and its coefficients are bounded by
\(A^{e_s}(1+M)^{e_s}\). Passing to a primitive integer polynomial
does not increase that bound. Thus a uniform recognition-height bound
has polynomial bit length. The same argument covers the primitive-element
candidate search.

The existing Kannan–Lenstra–Lovász recognition theorem now applies with
known degree and height bounds. It requires a proved approximation error
at the prescribed precision, rather than numerical evidence that an
integer relation has stabilized. The construction inherits this guarantee
from the certified approximation procedure. This review relies on the
separate [recognition-source review](algebraic-recognition-source-review.md)
for the exact theorem and its bit-model assumptions.

## Exceptional sample values and interpolation

For a fixed coordinate \(\beta\), define

\[
R(s,T)=\operatorname{Norm}_{K/\mathbb Q}(T-\alpha-s\beta)
      =\prod_{\sigma:K\hookrightarrow\mathbb C}
          (T-\sigma(\alpha)-s\sigma(\beta)).
\]

Its coefficients lie in \(\mathbb Q[s]\), and each has degree at most
\(d\) in \(s\). At an integer sample, tower multiplicativity of the
norm gives

\[
R(s,T)=p_s(T)^{d/e_s},\qquad e_s=\deg p_s.
\]

The exponent is an integer because \(\mathbb Q(\gamma_s)\subseteq K\).
This identity remains true when \(\gamma_s\) fails to generate \(K\),
including \(\gamma_s=0\), whose minimal polynomial is \(T\) but whose
norm polynomial is \(T^d\). Interpolating the minimal polynomials
themselves would be incorrect.

The degree in this exponent must be the actual recovered degree \(d\),
not merely an upper bound \(\overline D\). The normalized polynomials
must be monic: primitive integer representatives can have unrelated
leading coefficients at different samples.

Values at \(s=0,\ldots,d\) determine \(R\) coefficientwise. Rational
sample coefficients and their powers have polynomial bit length.
For these integer nodes, each Lagrange denominator divides
\(i!(d-i)!\), and the numerator coefficient sizes are bounded by a
polynomial in \(d\) bits. Combining \(d+1\) rational samples therefore
keeps polynomial bit length. This establishes Turing-model interpolation
complexity, not only a bound on arithmetic operations.

## Derivative recovery and power-basis encoding

Since \(\alpha\) generates \(K\), its conjugates are distinct, and
\(R(0,T)=p_\alpha(T)\), the monic minimal polynomial. Differentiate
the product for \(R\), then substitute \(s=0,T=\alpha\). Every term
except the one associated with the distinguished embedding vanishes:

\[
R_s(0,\alpha)=-\beta\,p_\alpha'(\alpha).
\]

Characteristic zero ensures \(p_\alpha'(\alpha)\ne0\). Therefore

\[
g_\beta(T)\equiv
 -R_s(0,T)\bigl(p_\alpha'(T)\bigr)^{-1}
 \pmod {p_\alpha(T)},\qquad \deg g_\beta<d,
\]

satisfies \(g_\beta(\alpha)=\beta\). The minus sign is essential.
This derives the correct formula independently of any source convention.

Multiplication by \(p_\alpha'\) on
\(\mathbb Q[T]/(p_\alpha)\) is an invertible rational linear map.
Its matrix has polynomial dimension and coefficient bit length.
Rational Gaussian elimination, or determinant bounds followed by a
polynomial-time linear-system algorithm, gives its inverse action with
polynomial bit length. This is a direct encoding argument; a statement
that an inverse merely exists would not suffice.

No factorization over \(K\) is used. For each coordinate there are
\(d+1\) recognition calls, polynomial-size interpolation, and rational
linear algebra. Together with the primitive-element search, this is
polynomial in \(n,\overline D,H\) and the cost of obtaining the required
certified approximations.

## Sign certification and independent checking

After substitution \(x_j=g_j(\alpha)\), each rational quadratic
constraint becomes a rational polynomial evaluated at \(\alpha\).
Reduction modulo \(p_\alpha\), followed by clearing a positive common
denominator, yields an integer polynomial \(q\) of degree below \(d\)
and polynomial coefficient bit length. A zero remainder proves equality.
Under the construction's minimal-polynomial guarantee, a nonzero
remainder cannot vanish at \(\alpha\).

There is an elementary polynomial precision bound for its sign. Let
\(p\) be the primitive integer minimal polynomial, with leading
coefficient \(a\ne0\) and coefficient magnitudes at most \(2^B\).
For nonzero \(q\in\mathbb Z[T]\) with degree \(m<d\) and height
at most \(2^L\), put

\[
R_0=1+2^B,\qquad U=(m+1)2^L R_0^m.
\]

The number \(a^m q(\alpha)\) is a nonzero algebraic integer. Its norm
is a nonzero integer, and its other conjugates have bounded magnitude.
Consequently

\[
|q(\alpha)|\ge |a|^{-md}U^{-(d-1)}.
\]

The logarithm of the reciprocal is polynomial. A derivative bound for
\(q\) on \([-R_0-1,R_0+1]\) then shows that polynomially many additional
bits of \(\alpha\) determine the sign by rational evaluation. Degree
zero is immediate.

A certificate verifier must not simply trust an input label saying
“minimal polynomial.” It can use standard univariate sign determination:
check squarefreeness and that the rational interval isolates one root,
then evaluate signs there. Polynomial gcds handle the possibility that
the query vanishes at that root. This requires neither a numerical
optimizer nor factorization over a number field. The constructed output
does have a minimal polynomial, but sound verification need not assume
that fact without checking it.

## Prior results and significance

Derivative coordinate recovery belongs to classical rational univariate
representation (RUR) methods. Bouzidi, Lazard, Pouget, and Rouillier's
2013 [Section 3.1, Proposition 7 and Lemma 9](https://arxiv.org/html/1303.5042#S3.SS1)
use derivatives of a sheared resultant for coordinate representation;
the section explicitly attributes that principle to earlier work.
Their [Lemma 23](https://arxiv.org/html/1303.5042#S4.SS2)
provides polynomial bit complexity for the sign of a univariate
polynomial at an isolated real algebraic root. Its endpoint-size assumption
is sharper than the local conservative isolator; the arbitrary-endpoint
bound in Lemma 26, also inspected, removes that mismatch. These are primary-source
comparisons, not novelty conclusions from an unsuccessful search.

The inspected version's derivative formula appears to omit a minus sign
for the convention \(T-X-SY\). The present review uses the direct product
calculation above, not that displayed sign. This does not affect the
prior-art observation that the derivative representation principle is
established.

The useful role here is to finish the exact-output and verification
guarantee of the Hessian-span program. It converts a proved polynomial
joint-degree and height bound into an explicit common-field encoding.
The algebraic conversion mechanism itself should be presented as
supporting machinery, not as the main original contribution. Practical
efficiency of high-precision recognition or interpolation has not been
established by this complexity argument.

## Verification record and limitations

This review checked the primitive search, height bounds, exact norm
multiplicities, interpolation encoding, derivative identity, modular
inverse, and sign bounds symbolically. The cited RUR statements were
inspected in the primary HTML and PDF versions. The full saved note was
then read, and the corrected oracle-output condition, separation of
primitivity from separability, and added sign-verification section were
rechecked independently.

The targeted command

```text
python research-20260927/check_constructive_common_field_review.py
```

passed three exact stress cases:

- \(\alpha=\sqrt2,\beta=-\sqrt2\): sample degrees \(2,1,2\),
  with the exceptional zero sample correctly raised from \(T\) to
  \(T^2\), and recovered coordinate \(-T\).
- \(t^3=2,\alpha=t,\beta=t^2\): the nonnormal cubic field gives
  \(R(S,T)=T^3-6ST-2-4S^3\), and recovered coordinate \(T^2\).
- \(\alpha=t/2,\beta=t^2/3\): the primitive integer polynomial is
  \(4T^3-1\), while the monic norm polynomial is
  \(R(S,T)=T^3-ST-1/4-4S^3/27\); recovery gives \(4T^2/3\).

The script uses exact symbolic minimal polynomials as inputs to the
interpolation stage. It does not implement KLL, validate its numerical
precision theorem, or prove the universal complexity bounds. The tests
specifically challenge degree drops, the absence of normality, and
nonmonic integer representations. No project-wide tests, CI inspection,
or Lean verification were performed.

Subsequent consolidation review: Section 7 of the construction now uses
\(\mathcal B(n,h)=\max_{0\le s\le\min(h,n)}2^s\binom ns\).
The linked multihomogeneous theorem explicitly bounds the joint field of
the minimum-norm optimizer, so this replacement matches the required input.
The height bound and approximation assumptions are unchanged, and the
general conversion theorem is untouched. The two updated paragraphs in
the earlier witness note accurately link coordinate conversion and
polynomial-time feasibility checking for its quadratic systems. These
narrow edits were checked by reading the changed passages and the linked
theorem statement; no computational or project-wide checks were needed.
