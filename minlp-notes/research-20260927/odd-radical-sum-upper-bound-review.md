# Independent review of the cube-root-sum circuit upper bound

Date: 2026-09-28. Scope: Section 4 of
[the odd-radical complexity audit](odd-radical-sum-complexity-prior.md).
The reviewer did not write that derivation. This is a proof review, not a
fresh literature search or a claim of originality.

The polynomial-time many-one reductions for both strict and weak signed
cube-root-sum comparison to PosSLP are correct as stated. They are upper
bounds on cube-root-sum comparison, not PosSLP-hardness statements.

## Arithmetic input normalization

For a positive rational radicand \(p/q\), with positive denominator,
\(\sqrt[3]{p/q}=\sqrt[3]{pq^2}/q\). Negative radicands can be
absorbed into signed coefficients. Multiplying by a positive product of
all coefficient denominators preserves strict and weak sign and has
polynomial bit cost. Thus the integer-coefficient, positive-integer-
radicand form used in Section 4 is obtained without integer factorization
or a common algebraic field representation.

## Separation

Let \(K=\mathbb Q(\sqrt[3]{a_1},\ldots,\sqrt[3]{a_m})\).
The tower law gives \([K:\mathbb Q]\leq3^m\), without independence
or irreducibility assumptions on the individual cubics. The weighted sum
\(S\) is an algebraic integer. If it is nonzero, its field norm is a
nonzero rational integer. Under any complex embedding, each cube root
has absolute value \(a_i^{1/3}\), hence every conjugate of \(S\)
is bounded by the audit's \(H<2^h\). Therefore

\[
 |S|>2^{-h([K:\mathbb Q]-1)}\geq2^{-h3^m}=\delta.
\]

The bound is conservative but sufficient. Neither \(K\), its degree,
nor the minimal polynomial of \(S\) must be computed.

## Newton circuit and sign offsets

With \(r=a_i^{1/3}\), the exact rational iteration
\(x'=(2x+a_i/x^2)/3\) has relative error

\[
 e'=\frac{e^2(3+2e)}{3(1+e)^2},\qquad e=x/r-1\geq0.
\]

Both bounds \(e'\leq2e/3\) and \(e'\leq e^2\) hold. The
initial \(x=2^b\) is above every root. After \(2b+2\) steps the
error is less than \(1/2\), because
\((2/3)^{2b+2}2^b=(4/9)(8/9)^b<1/2\).
After a further \(t\) steps its absolute error is at most
\(2^{b-2^t}\). The chosen inequality for \(2^t\) bounds the total
weighted error by less than \(\delta/8\).

Although \(\delta\) has an exponentially long expanded denominator,
the exponent \(h3^m\) has polynomial binary length. Repeated squaring
therefore constructs its denominator with polynomially many gates. The
number of Newton steps is also polynomial: the linear-convergence phase
uses \(O(b)\) steps and the quadratic phase uses
\(O(m+\log h+\log(b+\log(C+1)+1))\).

The shifts \(\widehat S-\delta/2\) and
\(\widehat S+\delta/2\) correctly handle equality without a separate
zero oracle. At \(S=0\), the first is negative and the second positive;
for nonzero \(S\), the norm gap determines their signs as claimed.

Every Newton denominator stays positive. More explicitly, if
\(x=P/Q\) with positive integers represented by shared circuits, then

\[
             x'=\frac{2P^3+a_iQ^3}{3P^2Q}.
\]

Maintaining numerator and denominator circuits therefore has constant
gate overhead per iteration and does not expand the integers. The final
comparison also has a positive denominator. Its numerator is a valid
division-free integer straight-line-program output, after constructing
the binary input constants from \(0,1\). This proves a many-one
reduction in the required Turing input model.

## Verification and limits

An independent inline SymPy command checked the Newton error identity,
both difference factorizations, and the numerator/denominator update.
A standard-library check verified this file's newline, whitespace,
control characters, mathematical delimiters, and local link. These
checks passed; the general precision and gate-size arguments were
reviewed mathematically above. No expanded exponential-precision Newton
trajectory was computed or needed. No project-wide checks or CI
inspection were used.

The review does not prove a polynomial bit-time algorithm for the
comparison: its arithmetic circuits may represent exponentially long
integers. It does not establish any hardness lower bound, and it does
not settle whether the source is a standard unresolved benchmark in
the latest literature.
