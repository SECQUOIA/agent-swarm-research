# All rational quadratic relations at the cyclic singleton

Date: 2026-09-28. Status: uniform proof draft; fresh review pending.

For the [cyclic algebraic point](cyclic-quartic-exponential-degree.md)
in every dimension \(n\geq4\), the rational quadratic vanishing
space has dimension exactly \(n+1\). Its basis is the displayed
cyclic residual family. This proves one of the hypotheses of the
[descent criterion](convex-quartic-descent-criterion.md) uniformly.
It does not prove the remaining stationary-quartic product-span
hypothesis in all dimensions.

Put \(m=n+1\geq5\), \(B=-2\),
\(d=(2^m-(-1)^m)/3\), and
\(s_i=(B^i-1)/3\), for \(0\leq i<m\). Write
\(p_i=a^{s_i}\), where \(a^d=2\), and \(p_0=1\).
Homogenizing quadratics with the variable \(X_0\) identifies the
affine degree-at-most-two monomials with the homogeneous monomials
\(X_iX_j\), \(0\leq i\leq j<m\).

Their evaluations are rationally proportional exactly when
\(s_i+s_j\equiv s_k+s_\ell\pmod d\). This follows from
Eisenstein irreducibility of \(T^d-2\). Since both sides have two
terms, this is equivalent to

\[
             B^i+B^j\equiv B^k+B^\ell\pmod{B^m-1}.
 \tag{1}
\]

There are at most four indices in (1). Because \(m\geq5\),
there is an unused cyclic index. Rotate indices so that an unused index
is \(m-1\). Rotation preserves (1), since \(B^m\equiv1\)
and \(B\) is invertible modulo the odd integer \(B^m-1\).
All four indices now lie between zero and \(m-2\).

Among these powers, the largest positive and negative magnitudes are
\(2^{m-2}\) and \(2^{m-3}\), in one order or the other. Therefore
the absolute difference of the two sums in (1) is at most

\[
 2\cdot2^{m-2}+2\cdot2^{m-3}
       =3\cdot2^{m-2}<2^m-1\leq|B^m-1|.
\]

Consequently (1) is an ordinary integer equality after this rotation.
Its nontrivial solutions can be classified by the 2-adic valuation.

If both pairs contain distinct indices, the valuation of their sum is
the smaller index, because \(1+B^h\) is odd for \(h\geq1\).
The smaller indices are equal, and cancellation then makes the larger
indices equal. If both pairs are repeated indices, their valuations
likewise force the pairs to coincide. The remaining case is

\[
                    2B^r=B^u+B^v,\qquad u<v.
\]

Valuation gives \(u=r+1\). Dividing by \(B^r\) yields
\(2=-2+B^{v-r}\), so \(v=r+2\). Rotating back, every
nontrivial collision is exactly

\[
                 X_i^2\quad\hbox{with}\quad X_{i+1}X_{i+2},
 \tag{2}
\]

with indices modulo \(m\). Conversely every pair in (2) is a
collision, by the cyclic exponent identity.

The \(m\) pairs in (2) are disjoint as monomial pairs. Distinct
diagonal monomials cannot share an evaluation class, by the preceding
classification. Every remaining monomial has a class of its own.
Thus exactly \(m\) independent rational relations occur among the
homogeneous quadratic evaluations. Their rational coefficients are
fixed by the power-of-two factors in the evaluations; they are precisely
the cyclic quadrics

\[
 q_i=X_i^2-2^{k_i}X_{i+1}X_{i+2}
\]

from the family construction. This proves
\(\dim_{\mathbb Q}I_2(p)=m=n+1\).

Together with the rational convex SOS baseline and the product-independence
part of the descent criterion, it also gives
\(\dim W(p)=(n+1)(n+2)/2\) for every \(n\geq4\), subject
to that criterion's review. The unproved uniform issue is exactly whether
\(J_4(p)=W(p)\). The retained finite checker establishes that equality
only for the dimensions explicitly listed in the criterion note.

For \(n=3\), all four indices can be used, so the rotation step is
unavailable. That case has an additional independent quadratic relation
and dimension five, as the exact ternary construction shows. This is
a genuine boundary of this proof, rather than a discarded exception.
