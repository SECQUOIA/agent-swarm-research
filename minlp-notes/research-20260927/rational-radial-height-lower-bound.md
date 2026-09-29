# A quantitative lower bound for rational radial order

Date: 2026-09-28. Status: the height inequalities and inversion passed
fresh independent review. Publication priority is not established.

For the positive-integer scaling family
\[
 f_t(X)=t^{-2}F(tX),\qquad R(X)=1+\|X\|^2,
 \qquad t\in\mathbb Z_{>0},
\]
let \(\nu(t)\) be the least integer \(N\ge0\) for which
\(R^Nf_t\) is a sum of rational polynomial squares. Its finiteness
follows from the separately reviewed sphere corollary in
[the denominator frontier](rational-denominator-certificate-frontier.md).
Exact height tracking in
[the recursive separator construction](rational-radial-quantitative-separation.md)
proves
\[
 \boxed{\displaystyle
 \nu(t)=\Omega\!\left(\frac{\log\log t}{\log\log\log t}\right)
 \quad\text{as integer }t\to\infty.}
                                                        \tag{1}
\]
For this family's standard binary coefficient encoding, its input
length \(L(t)\) is \(\Theta(\log t)\). Thus (1) is equivalently
\(\nu(t)=\Omega(\log L/\log\log L)\). All members still have
an adaptive quadratic denominator and a certificate of size
\(O(L)\). This is an order lower bound for a prescribed radial
hierarchy, not a lower bound for all rational certificates or for
algorithm running time.

The proof gives a concrete, conservative threshold bound. If
\(\tau_N\) denotes the sufficient integer threshold constructed
in the companion note, then
\[
 \boxed{\displaystyle
 \tau_N\le
 2^{\,34\cdot64^N\left((N+2)!/2\right)^3}}
 \qquad(N\ge0).
                                                        \tag{2}
\]
In particular \(\tau_N\le\exp(\exp(O(N\log N)))\) as
\(N\to\infty\). The argument below tracks the exact denominators
that are needed for (2).

Retain the companion note's functionals \(\lambda_d\), nested
basis \(q_m=m-c_m\rho_r\) of \(I_d\), and correction
\(\lambda_d=\widehat\lambda_{d-1}+T_dM_d\). Put \(K=28450\).
Every monomial value of \(\lambda_d\) has denominator dividing
\(K\): this holds at the base step, and every subsequent correction
has integer monomial values. Define integer numerator heights and
augmented bit bounds by
\[
 H_d=\max\left\{1,\max_{\deg m\le2d}|K\lambda_d(m)|\right\},
 \qquad
 b_d=\max\{d+1,\lceil\log_2(H_d+1)\rceil\}.
                                                        \tag{3}
\]
The base values are \(H_2=113845\) and \(b_2=17\).
Old monomial values are preserved by each extension. Consequently
\(H_d\) is nondecreasing, and
\[
                         b_d\ge\max\{17,d+1\}.
                                                        \tag{4}
\]
The augmentation in (3) absorbs the heights of the basis coefficients;
it does not change the interpretation of \(b_d\) as a valid upper
bound on coefficient bit length, up to the fixed denominator's size.

Fix an extension step \(d\ge3\), and abbreviate
\[
 n=\dim I_{d-1}=\binom{d+2}{3}-5\le d^3,
 \qquad h=\binom{d+2}{2}\le2d^2.
\]
In the monomial reduction formula, every coefficient \(c_m=2^k\)
for a monomial of degree at most \(d\) satisfies
\(-d\le k\le d+1\). Each basis polynomial therefore has
denominator dividing \(2^{d+1}\) and coefficient \(\ell_1\)-norm
at most \(1+2^{d+1}\).

Write the raw square Gram matrix of
\(\widehat\lambda_{d-1}\) as
\(\left(\begin{smallmatrix}A&B\\B^{\mathsf T}&C\end{smallmatrix}\right)\),
where \(A\) indexes \(I_{d-1}\). Define
\[
 Q=K2^{2d+2},\qquad U=2^{4d+6}H_{d-1}.
                                                        \tag{5}
\]
All entries of the raw Gram matrix have denominators dividing \(Q\),
and multiplication by \(Q\) makes them integers of absolute value
at most \(U\). Indeed, before multiplication their absolute values
are at most
\[
 (1+2^{d+1})^2\frac{H_{d-1}}K
 \le2^{2d+4}\frac{H_{d-1}}K.
\]

Since \(QA\) is an integer positive definite matrix,
\(\det(QA)\ge1\). Each of its cofactors has absolute value at
most \((n-1)!U^{n-1}\), by the determinant expansion. Therefore
\[
 |(A^{-1})_{ij}|
 \le Q(n-1)!U^{n-1}
 \le Q(nU)^{n-1}.
                                                        \tag{6}
\]
For the Schur complement \(S=C-B^{\mathsf T}A^{-1}B\), this gives
\[
 |S_{ij}|\le\frac{2(nU)^{n+1}}Q,
 \qquad
 m_d:=\max_i\sum_j|S_{ij}|
       \le2h(nU)^{n+1}.
                                                        \tag{7}
\]
The determinant lower bound in (6) is the point where control of the
common rational denominator is essential.

The integer grid Gram matrix \(D\) in the new block has entries
bounded by
\[
 J_d=(d+1)^3d^{2d},\qquad
 \operatorname{tr}D\le W_d:=hJ_d.
                                                        \tag{8}
\]
Since \(D\) is positive definite and integer, \(\det D\ge1\).
For the companion note's
\(\beta_d=\det D/(\operatorname{tr}D)^{h-1}\), it follows that
\(\beta_d^{-1}\le W_d^{h-1}\). The integer ceiling in its choice
of \(T_d\) then satisfies
\[
 \begin{aligned}
 T_d
 &\le(m_d+1)W_d^{h-1}+1\\
 &\le4h(nU)^{n+1}W_d^{h-1}.
 \end{aligned}
                                                        \tag{9}
\]
The newly assigned monomial values are at most \(T_dJ_d\).
Combining (5), (8), and (9) gives the explicit height recursion
\[
 \boxed{\displaystyle
 H_d\le4K W_d^h
       \left(n2^{4d+6}H_{d-1}\right)^{n+1}.}
                                                        \tag{10}
\]
The right side also bounds the preserved old values. Although the
intermediate rational Schur complement may have large denominators,
the integer choice \(T_d\) preserves the fixed denominator bound
for the next functional. No running-time estimate for computing the
Schur complement is asserted.

For completeness, a uniform bit recurrence with simple constants is
\[
                    b_d\le32d^3
                       \bigl(b_{d-1}+\log_2(d+1)\bigr).
                                                        \tag{11}
\]
To verify this directly, put \(\ell=\log_2(d+1)\). For \(d\ge3\),
\[
 \log_2W_d\le5d\ell,\qquad
 \log_2n\le3\ell,\qquad n+1\le2d^3.
\]
Also \(b_{d-1}\ge d\), so \(4d+6\le6b_{d-1}\).
Taking logarithms in (10), allowing two bits for integer rounding,
and using \(\log_2K<15\), bounds the unaugmented bit length by
\[
 19+14d^3b_{d-1}+16d^3\ell.
\]
This is at most the right side of (11), which also exceeds \(d+1\).
Thus it bounds the augmented \(b_d\) as well. Since
\(\log_2(d+1)\le d\le b_{d-1}\), iteration gives
\[
 b_d\le64d^3b_{d-1}
 \le17\cdot64^{d-2}\left(d!/2\right)^3.
                                                        \tag{12}
\]
In particular, \(b_d\le\exp(O(d\log d))\).

It remains to connect functional heights to the threshold. Set
\(d=N+2\), \(s=x^2+y^2+z^2\), and use the companion note's
\[
 A_N=\sum_{k=1}^N
       \left|\binom Nk\lambda_d(s^kF)\right|,
 \qquad a_0=85351/28450>2.
\]
The fixed polynomial has 31 monomials and absolute coefficients at
most 448, so \(\|F\|_1\le13888\). For any polynomial of degree
at most \(2d\),
\( |\lambda_d(P)|\le2^{b_d}\|P\|_1\), and
\(\|s^k\|_1=3^k\). Hence
\[
 A_N\le13888\,2^{b_d}(4^N-1)
       \le13888\,2^{b_d+2N}.
                                                        \tag{13}
\]
The companion threshold formula and \(a_0>2\) imply
\[
 \tau_N\le2\sqrt{A_N+1},\qquad
 \log_2\tau_N\le\tfrac12b_d+N+8.5\le2b_d.
                                                        \tag{14}
\]
The final inequality uses both bounds in (4):
\(N\le b_d-3\) and \(b_d\ge17\). Substituting (12) in (14)
proves (2), including the case \(N=0\).

Here is an explicit inversion that also fixes the quantifiers. A loose
consequence of (2), using \(d!\le d^d\), is
\[
 \tau_N\le2^{\,2^{10(N+2)\log_2(N+3)}}.
                                                        \tag{15}
\]
For any positive integer \(t\) such that
\(u:=\log_2\log_2t\ge1024\), choose
\[
                  N=\left\lfloor\frac{u}{40\log_2u}\right\rfloor.
\]
In this range \(u/(40\log_2u)\ge2\), so
\(N+2\le u/(20\log_2u)\), and \(N+3\le u\). Therefore
\[
 10(N+2)\log_2(N+3)\le u/2,
 \qquad \tau_N\le2^{2^{u/2}}\le t.
\]
The separator excludes radial order \(N\) for every integer scale
at least \(\tau_N\). Because multiplication by the rational SOS
\(R\) preserves rational SOS, failure at \(N\) also excludes
all lower orders. Thus
\[
 \nu(t)\ge N+1>
 \frac{\log_2\log_2t}{40\log_2\log_2\log_2t}
 \qquad\text{whenever }\log_2\log_2t\ge1024.
                                                        \tag{16}
\]
This is an explicit sufficient range, chosen for simple inequalities.
No monotonicity of the actual thresholds or least orders is assumed.
The conclusion holds for every sufficiently large integer \(t\),
not merely along a selected subsequence.

Finally, the fixed support and coefficients
\([X^\alpha]f_t=[X^\alpha]F\,t^{|\alpha|-2}\) give an input
encoding of length \(O(1+\log t)\). The single coefficient
\([X_1^4]f_t=104t^2\) supplies the matching lower bound. Thus
\(L(t)=\Theta(\log t)\), proving the input-length form of (1).
This equivalence is asserted for the integer family. For arbitrary
rational parameters, denominator bit length need not be bounded by
\(\log t\).

A fresh reader checked the common denominators, adjugate bound,
Schur-complement bound, integer ceiling, height recurrence, and explicit
inversion. A further independent reader checked the final quantifiers.
Targeted inline Python calculations checked the base numerator heights
\(H_2=113845\), \(b_2=17\), and the polynomial's 31 terms,
maximum absolute coefficient 448, and exact coefficient norm 6637.
The independent reader also sampled a coarse logarithmic inequality
for \(d=3,\ldots,100\); these samples supplement the algebraic
bound and do not establish its universal quantifier. No larger
matrices, project-wide checks, or CI status were inspected for this
height analysis. The underlying separator's exact first-step
verification is recorded in the companion note.
