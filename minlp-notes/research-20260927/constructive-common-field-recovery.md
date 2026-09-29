# Constructing one field representation from algebraic approximations

Date: 2026-09-27. Status: complete proof;
[independent adversarial review](constructive-common-field-review.md) found
no substantive gap, conditional on the stated degree, height, and certified
approximation inputs. This is an algorithmic completion of the Hessian-span
recovery results, not a claim of a new primitive-element or univariate
representation method.

The exact coordinate recovery algorithm can be completed to return a single
real algebraic number and rational polynomials representing every coordinate.
The construction uses algebraic recognition, polynomial interpolation, and
rational linear algebra. It requires no factorization over a number field.
In particular, individual coordinate conjugates are never combined by an
uncontrolled product of their degrees.

## 1. General statement and input model

Let \(\beta=(\beta_1,\ldots,\beta_n)\in\mathbb R^n\), with
\(n\ge1\), and let

\[
 K=\mathbb Q(\beta_1,\ldots,\beta_n),\qquad
 d=[K:\mathbb Q]\le D,
\]

where \(D\ge1\) is a supplied bound. Suppose each coordinate has a
primitive integer minimal polynomial whose coefficient magnitudes are at most
\(2^H\), with a supplied \(H\ge1\). Suppose further that an oracle,
on input an accuracy integer \(p\ge1\), returns rational numbers
\(\widetilde\beta_j\), of bit length polynomial in \(n,D,H,p\),
satisfying

\[
               |\widetilde\beta_j-\beta_j|<2^{-p}
                    \quad(1\le j\le n).                    \tag{1}
\]

The oracle must approximate this one specified tuple. Separate minimal
polynomials without selected real embeddings would not supply this input.
Neither the coordinate minimal polynomials nor the exact degree \(d\)
need be given initially.

**Theorem.** There is a deterministic algorithm with polynomial overhead in
\(n,D,H\), making polynomially many calls to (1) at accuracy parameters
polynomial in \(n,D,H\), which returns:

- a primitive integer irreducible polynomial \(P\), of degree exactly
  \(d\), and a rational interval selecting one simple real root \(\alpha\);
- rational polynomials \(b_1,\ldots,b_n\), each of degree less than
  \(d\), such that \(\beta_j=b_j(\alpha)\) for every \(j\);
- integers \(c_1,\ldots,c_n\) such that
  \(\alpha=\sum_jc_j\beta_j\).

All output coefficient bit lengths are polynomial in \(n,D,H\). If the
oracle runs in time polynomial in these parameters and \(p\), so does
the complete algorithm. The empty tuple is a separate trivial case: use the
rational field, \(P(T)=T\), and no coordinate polynomials.

The only algebraic recognition theorem used is
Kannan--Lenstra--Lovász (1988), Theorem 1.19, as inspected and stated in
[the coordinate recovery note](algebraic-witness-recovery.md#4-turning-approximations-into-exact-coordinates).
It recovers a primitive integer minimal polynomial in polynomial time from
a degree bound, a coefficient-height bound, and sufficiently accurate rational
approximation. In particular, polynomial degree and coefficient-bit bounds
require only polynomially many accuracy bits. We do not replace its
certified precision requirements by a heuristic integer-relation search.

## 2. Uniform height bounds for the numbers to be recognized

First use recognition to recover the coordinate minimal polynomials. Let
\(a_j\ge1\) be the absolute value of the leading coefficient of the
\(j\)-th polynomial and put \(A=\prod_ja_j\). Then

\[
          \log_2 A\le nH,\qquad A\beta_j
                          \text{ is an algebraic integer}.   \tag{2}
\]

For the second assertion, if \(a_jT^r+\cdots+a_0\) vanishes at
\(\beta_j\), multiplying the substituted equation by \(a_j^{r-1}\)
gives a monic integer equation for \(a_j\beta_j\). Signs of leading
coefficients are immaterial. Multiplication by \(A/a_j\) preserves
integrality.

Every complex conjugate of \(\beta_j\) has modulus at most
\(1+2^H\le2^{H+1}\), by Cauchy's root bound. Consequently, for integers
\(c_j\) with \(|c_j|\le2^C\), let

\[
 \alpha=\sum_jc_j\beta_j,\qquad
 \gamma_s=\alpha+s\beta_i\quad(0\le s\le D).
\]

For every embedding of \(K\) into \(\mathbb C\),

\[
 |\sigma(\gamma_s)|\le M:=(n2^C+D)2^{H+1},\qquad
                         A\gamma_s\text{ is integral}.     \tag{3}
\]

If \(p_s(T)\in\mathbb Q[T]\) is the monic minimal polynomial of
\(\gamma_s\), of degree \(e_s\le D\), then
\(A^{e_s}p_s(T)\in\mathbb Z[T]\). Indeed, the monic minimal
polynomial of \(A\gamma_s\) is integral and equals
\(A^{e_s}p_s(T/A)\). Expanding the product over the conjugates of
\(\gamma_s\) therefore bounds the primitive integer minimal polynomial
by

\[
  \max|\text{coefficient}|
                \le A^{e_s}(1+M)^{e_s}.                    \tag{4}
\]

For clarity, the integral polynomial in this argument is
\(A^{e_s}p_s(T)\); it is obtained from the integral minimal polynomial
of \(A\gamma_s\) by substituting \(AT\), so all its coefficients
are integers. Thus an effective recognition height in bits is

\[
 H_{\rm rec}=
 D\left[nH+H+C+\lceil\log_2(n+D)\rceil+3\right].           \tag{5}
\]

This deliberately conservative bound also covers \(\alpha\) itself.
Dividing the integral polynomial by its content cannot increase its height.

An approximation to any of these linear forms with error below \(2^{-q}\)
is obtained from (1) using
\(p\ge q+\lceil\log_2(n2^C+D)\rceil+1\). Hence recognition precision
does not require operations in an unknown number field.

## 3. Finding a primitive element and the exact field degree

Use the finite family

\[
 \alpha_k=\sum_{j=1}^n k^{j-1}\beta_j,
 \qquad 0\le k\le L:=(n-1)D(D-1)/2,                         \tag{6}
\]

with \(k^0=1\), including at \(k=0\). This is the standard
separating-linear-form argument. The \(d\) embeddings of \(K\) are
distinct on the tuple generating \(K\). For each distinct pair of
embeddings, their difference on \(\alpha_k\) is a nonzero polynomial
in \(k\) of degree at most \(n-1\). At most
\((n-1)d(d-1)/2\) integer values fail to separate some pair. Thus at
least one candidate in (6) has \(d\) distinct conjugates and generates
\(K\).

The integers in (6) have bit length at most
\((n-1)\lceil\log_2\max(2,L)\rceil+1\). Apply Sections 1--2 to
recognize every candidate. The largest recognized degree is exactly \(d\),
and any candidate attaining it is primitive. Select one and retain its
integer coefficients \(c_j\). Let \(P\) be its primitive integer
minimal polynomial and \(p=P/\operatorname{lc}(P)\) its monic version.
The root-isolation step of the coordinate recovery note supplies an interval
selecting the intended \(\alpha\) from a sufficiently accurate linear-form
approximation. This uses only polynomially many bits in the degree and height.

There are \(L+1=O(nD^2)\) candidates. The coefficients, the height bound
(5), and the necessary precision are polynomial in \(n,D,H\). This
search also works when \(d=1\): every candidate is rational, and any
selected one generates \(\mathbb Q\). For \(n=1\), the sole candidate
is \(\beta_1\), already a primitive generator.

## 4. Interpolation remains valid when a sampled degree drops

Fix a coordinate \(\beta_i\). For every integer \(s=0,\ldots,d\),
recognize the monic minimal polynomial \(p_s(T)\) of
\(\gamma_s=\alpha+s\beta_i\). Write \(e_s=\deg p_s\). Since
\(\gamma_s\in K\), the tower law gives \(e_s\mid d\). Define

\[
                    C_s(T)=p_s(T)^{d/e_s}.                    \tag{7}
\]

Then

\[
 C_s(T)=\operatorname{Norm}_{K/\mathbb Q}(T-\gamma_s).
                                                               \tag{8}
\]

To see this without assuming that \(K\) is a normal extension, each
embedding of \(\mathbb Q(\gamma_s)\) into \(\mathbb C\) has
exactly \([K:\mathbb Q(\gamma_s)]=d/e_s\) extensions to \(K\),
because all extensions in characteristic zero are separable. Taking the
product of \(T-\sigma(\gamma_s)\) over the \(d\) embeddings proves
(8). Equivalently, use the tower property of the norm.

The polynomial

\[
 R_i(S,T)=\operatorname{Norm}_{K(S)/\mathbb Q(S)}
                            (T-\alpha-S\beta_i)
         =\prod_{\sigma:K\hookrightarrow\mathbb C}
                            (T-\sigma\alpha-S\sigma\beta_i)
                                                               \tag{9}
\]

belongs to \(\mathbb Q[S,T]\). This follows either from invariance of
the product or from the determinant of multiplication by
\(T-\alpha-S\beta_i\) on any rational basis of \(K\); that basis
is used only for this existence argument. The polynomial is monic of degree
\(d\) in \(T\) and has degree at most \(d\) in \(S\). Its
specialization at each sampled integer is exactly (7). Therefore ordinary
coefficientwise interpolation at \(0,\ldots,d\) constructs the entire
\(R_i\) using only rational arithmetic.

It would be wrong to interpolate the minimal polynomials \(p_s\) without
the exponent in (7). For example, take \(K=\mathbb Q(\sqrt2)\),
\(\alpha=\sqrt2\), and \(\beta_i=-\sqrt2\). At \(s=1\),
\(p_1(T)=T\) has degree one, whereas the required sample is
\(C_1(T)=T^2\). Formula (9) is
\(R_i(S,T)=T^2-2(1-S)^2\). No interpolation point has to be discarded,
and no promise that every sample is primitive is used.

## 5. Recovering the coordinate polynomials

Because \(\alpha\) is primitive,

\[
             R_i(0,T)=p(T),\qquad
             R_i(S,\alpha+S\beta_i)=0.                     \tag{10}
\]

The second identity holds in \(K[S]\), since the factor for the chosen
embedding in (9) vanishes. Differentiate it formally with respect to \(S\)
and set \(S=0\). This gives

\[
 (\partial_SR_i)(0,\alpha)+p'(\alpha)\beta_i=0,
 \qquad
 \beta_i=-\frac{(\partial_SR_i)(0,\alpha)}{p'(\alpha)}.     \tag{11}
\]

The denominator is nonzero because the characteristic is zero and \(p\)
is irreducible. Compute an inverse \(u(T)\) of \(p'(T)\) modulo
\(p(T)\) by extended Euclidean arithmetic over \(\mathbb Q\), and set

\[
 b_i(T)=\operatorname{rem}_p
                  \bigl(-u(T)(\partial_SR_i)(0,T)\bigr).    \tag{12}
\]

Then \(\deg b_i<d\) and \(\beta_i=b_i(\alpha)\). The inverse
\(u\) is common to all coordinates and exists by separability of the
minimal polynomial. Primitivity is used in (10): it makes \(R_i(0,T)=p(T)\)
rather than a power of that polynomial. No genericity condition on the other
sample values is required.
For \(d=1\), \(p'=1\), and the construction simply returns rational
constants.

## 6. Bit complexity after recognition

All remaining arithmetic has polynomial degree and coefficient size. Here
are explicit reasons; a count of arithmetic operations alone would be
insufficient.

1. Each primitive integer sample polynomial has degree at most \(d\) and
   coefficient bits at most (5). Dividing by its leading coefficient and
   raising it to power \(d/e_s\le d\) produces a polynomial of degree
   \(d\). The denominator is a power of that leading coefficient, and
   the numerator's coefficient norm grows by at most the same power of the
   original coefficient norm. Thus sample numerator and denominator bits
   are \(O(d(H_{\rm rec}+\log(d+1)))\).
2. For interpolation, use
   \[
    R_i(S,T)=\sum_{s=0}^d C_s(T)
                \frac{\prod_{0\le t\le d,\,t\ne s}(S-t)}
                     {\prod_{0\le t\le d,\,t\ne s}(s-t)}.
   \]
   The denominator has magnitude \(s!(d-s)!\le d!\), and the
   numerator has coefficient norm at most \((d+1)^d\). Clearing the
   at most \(d+1\) sample denominators therefore gives only polynomial
   bit growth. For example, coefficient bits
   \(O(d^2(H_{\rm rec}+\log(d+1)))\) suffice. Differentiation and
   evaluation at zero preserve a polynomial bound.
3. Modular inversion also has polynomial bit cost. One fully elementary
   implementation forms the \(d\)-by-\(d\) rational matrix for
   multiplication by \(p'\) in \(\mathbb Q[T]/(p)\). Reduction
   of powers up to \(2d-2\) uses only polynomially many rational
   operations and has polynomial bit growth, as is also seen from powers
   of the rational companion matrix of \(p\). This multiplication
   matrix is nonsingular. Clearing its entry denominators and applying
   determinant bounds to its linear system gives a polynomial bound for
   the inverse coefficients. Fraction-free rational elimination computes
   them in polynomial bit time. This supplies the same inverse as extended
   Euclid without relying on an uncontrolled intermediate expression size.
4. Products and remainders in (12) have degrees bounded by \(O(d)\)
   and the preceding coefficient bounds. Ordinary rational polynomial
   arithmetic again takes polynomial bit time and produces polynomial
   coefficient size.

There are at most \(n(d+1)\) sample recognitions after the primitive
search, and all use the approximation precision justified by (3)--(5).
No enumeration of a product of individual degrees occurs. No factorization
over \(K\), or construction of its full multiplication table before
recovery, is required.

## 7. Consequences for the Hessian-span results

For the canonical optimizer, use the joint-field degree bound in
[the multihomogeneous degree theorem](multihomogeneous-span-degree.md)
and the unchanged coordinate-height bound from
[ordered perturbations](ordered-perturbation-optimizer.md):

\[
 D=\mathcal B(n,h)
   :=\max_{0\le s\le\min(h,n)}2^s\binom ns,
 \qquad H=N^{O(h+1)}.
\]

The exact optimizer recovery algorithm supplies (1) with polynomial bit
cost for fixed \(h\). The present theorem then constructs a common
field representation in polynomial time for fixed \(h\). Its output
degree is the actual field degree, bounded by the displayed \(D\), and
its coefficient bits remain \(N^{O(h+1)}\). This conclusion about
output size does not sharpen the running-time exponent of the underlying
approximation oracle. The same conversion applies to canonical feasible
points from [the earlier recovery theorem](algebraic-witness-recovery.md).

The representation permits joint polynomial evaluation by substitution and
reduction modulo \(P\); it avoids the earlier ambiguity about combining
individually represented algebraic coordinates. For native affine and
quadratic rows, reduced degrees and coefficient sizes remain polynomial.
Their exact signs can be determined with polynomially many accuracy bits.
Here is an elementary reason. Clear positive rational denominators in a
reduced row to obtain \(v(T)\in\mathbb Z[T]\), of degree \(m<d\).
If \(v=0\), its value is zero. Otherwise irreducibility of the produced
\(P\) gives \(v(\alpha)\ne0\). Write \(a=\operatorname{lc}(P)\),
bound its coefficient magnitudes by \(2^{H_\alpha}\), and bound those
of \(v\) by \(2^{H_v}\). Put

\[
 R=1+2^{H_\alpha},\qquad U=(m+1)2^{H_v}R^m.
\]

All conjugate values of \(v(\alpha)\) have modulus at most \(U\).
The nonzero number \(a^mv(\alpha)\) is an algebraic integer, so its
norm is a nonzero integer. It follows that

\[
             |v(\alpha)|\ge |a|^{-md}U^{-(d-1)}.            \tag{13}
\]

The logarithm of the reciprocal bound is polynomial in the output size.
On \([-R-1,R+1]\), the derivative bound
\(\sum_{k=1}^m k|v_k|(R+1)^{k-1}\) also has polynomial bit length.
An approximation to \(\alpha\) accurate enough for the resulting
evaluation error to be less than half (13) determines the sign. Constants
are handled directly. Thus the construction itself needs no further
number-field operation for native constraint signs.

An independent verifier should not assume that a polynomial labeled
"minimal" is irreducible. It can first take its squarefree part and verify
the selected root, then use univariate sign determination, including gcd
computations for exact zeros. The primary RUR source below gives this
polynomial bit bound in Lemma 23. That lemma states a tighter endpoint-size
assumption than our deliberately conservative isolator: one may compute
fresh isolating intervals satisfying its assumption and identify the selected
root, or use the arbitrary rational-endpoint parameter in its proof's
Lemma 26. Both retain polynomial bit cost. This checks feasibility of a
supplied common-field point without trusting the construction or an
irreducibility label. A feasible point representation does not, by itself,
prove an optimization certificate or produce KKT multipliers when constraint
qualifications fail. Those require additional arguments.

The theorem also does not recover a field representation from a joint-degree
bound alone. A selected-point approximation procedure and effective height
bounds are substantive inputs. Nor does it assert that common-field output
is numerically better conditioned or faster in practical solvers.

## 8. Prior mechanisms and verification scope

The use of a separating linear form, its characteristic polynomial, and
coordinate numerators divided by a derivative belongs to the established
theory of rational univariate representations. The finite candidate family
(6) is the standard embedding-separation argument, already recorded in the
earlier local recovery note. The contribution of this note is a direct
completion of that note's input model using recognition and interpolation;
no priority is claimed for the algebraic mechanisms.

We inspected the primary preprint of Bouzidi, Lazard, Pouget, and Rouillier,
[*Rational Univariate Representations of Bivariate Systems and Applications*](https://arxiv.org/pdf/1303.5042),
Section 3.1, especially the parameterized product (4), Lemma 9, and
Proposition 7, and the sign-evaluation results in Lemmas 23 and 26.
It uses a product over algebraic solutions and derivatives
in the separating-form parameter to obtain coordinate representations.
Its input is a bivariate polynomial system and its algorithms use a
resultant; our input is an approximation oracle with degree and height
bounds. Thus the source is an antecedent for the representation mechanism,
not a direct theorem for this oracle model. Formula (11), including its
minus sign for the convention \(T-\alpha-S\beta_i\), is derived here
independently. We have not established novelty for the recognition and
interpolation combination.

The independent reviewer read the full proof, challenged the exceptional
sample cases and bit bounds, and rechecked the oracle-output condition and
the distinction between primitivity and separability after correction. The
reviewer suggested the elementary sign bound in Section 7; the author
independently rederived it, and the saved addition was reviewed again.

The reviewer ran the targeted command

```text
python research-20260927/check_constructive_common_field_review.py
```

The [exact symbolic checker](check_constructive_common_field_review.py)
passed three cases: a degree drop to the zero sample in
\(\mathbb Q(\sqrt2)\), a nonnormal cubic field, and a nonmonic integer
minimal polynomial with rational coordinate denominators. These checks
test norm reconstruction and the derivative formula after recognition;
they do not implement or test KLL.

The author ran a targeted inline Python check of this file: local links,
math delimiters, whitespace, control characters, and final newline passed.
The general theorem rests on the proof above and the cited recognition
theorem; symbolic examples cannot verify the universal degree, height, or
runtime claims. No project-wide checks, CI inspection, or Lean proof are
asserted.

The subsequent consolidation replaces the application degree bound by
\(\mathcal B(n,h)\) and links the earlier feasible-point note to this
completed conversion. A targeted inline Python document check passed for
both edited notes: 15 local links in total, math delimiters, whitespace,
control characters, final newlines, the displayed improved bound, and removal
of the obsolete statements that conversion remained open. No mathematical
test was rerun for these citation and consequence updates.
