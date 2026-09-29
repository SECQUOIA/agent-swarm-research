# An explicit recursive separator for rational radial SOS

Date: 2026-09-28. Status: the construction passed a fresh independent
mathematical review; its first extension step passed exact rational
checks by two readers. The subsequent
[height analysis](rational-radial-height-lower-bound.md) proves an
asymptotic radial-order lower bound. Publication priority is not
established.

The radial nonmembership proof can be made effective using rational
matrix arithmetic and finite grids. For every integer \(N\ge0\), the
recursion below produces an explicit integer \(\tau_N\) such that
\[
 (1+\|X\|^2)^N t^{-2}F(tX)\notin\Sigma\mathbb Q[X]^2
 \qquad(t\in\mathbb Z,\ t\ge\tau_N).
\]
Here \(F\) is the fixed quartic in
[the radial-exponent manuscript](rational-radial-exponent-obstruction.md).
For example, the displayed recursion certifies the sufficient threshold
\[
                         \tau_1=711859414639.
\]
This threshold is deliberately conservative. It is not the least scale
where radial order one fails. The recursion gives a finite effective
threshold for each order. Its growth in \(N\) and the resulting
asymptotic lower bound are analyzed in the separate height note.

Write \(p=(a^4/2,a,a^2/2)\), where \(a^5=2\) and \(a>0\).
Let \(I_d\) be the rational polynomials of total degree at most
\(d\) vanishing at \(p\), and let \(V_d\) be their real span.
The fixed rational coefficient functional
\[
 L(P)=2[z]P+4[y^2]P
\]
satisfies \(L(F)=-4\) and \(L(q^2)\ge0\) for \(q\in V_2\).
These inputs were independently checked in
[the fresh certificate review](rational-denominator-certificate-fresh-review.md).
The construction will give rational linear functionals \(\lambda_d\)
on \(\mathbb R[x,y,z]_{\le2d}\) such that
\[
 \lambda_d(q^2)>0\quad(0\ne q\in V_d),\qquad
 \lambda_d(F)=-a_0,\quad a_0=\frac{85351}{28450}>0.
                                                        \tag{1}
\]
Positivity here is restricted to \(V_d\); it is not positivity on
all real polynomial squares.

Use the five representative monomials
\[
 (\rho_0,\rho_1,\rho_2,\rho_3,\rho_4)=(1,y,z,yz,x).
\]
Their values at \(p\) are respectively
\(1,a,a^2/2,a^3/2,a^4/2\), a rational basis of \(\mathbb Q(a)\).
For any monomial \(m=x^iy^jz^k\), put
\[
 e=4i+j+2k,\qquad r=e\bmod5,\qquad
 c_m=2^{\lfloor e/5\rfloor-i-k+\mathbf1_{r\ge2}}.
                                                        \tag{2}
\]
Then \(m(p)=c_m\rho_r(p)\). For each monomial of degree at most
\(d\) other than the five representatives, define
\[
                              q_m=m-c_m\rho_r.
                                                        \tag{3}
\]
For \(d\ge2\), these polynomials form a basis of \(I_d\).
Indeed, reducing every monomial by (3) leaves a unique linear
combination of the five representatives. Its value at \(p\) can
vanish only when all five rational coefficients vanish. Each
nonrepresentative monomial occurs with coefficient one in its own
basis element and with coefficient zero in every other basis element.

Order monomials first by total degree and then lexicographically by
their exponent triples \((i,j,k)\), with smaller entries first.
The bases (3) are nested in this order. For \(d\ge3\), each newly
added basis element has leading homogeneous part exactly its degree-
\(d\) monomial, because its subtracted representative has degree at
most two. Thus
\[
 \dim I_d=\binom{d+3}{3}-5,\qquad
 h_d:=\dim I_d-\dim I_{d-1}=\binom{d+2}{2}\quad(d\ge3).
                                                        \tag{4}
\]
No numerical approximation of \(a\) is involved in (2) or (3).

For the base separator, define the rational evaluation functional
\[
 E(P)=\sum_{u\in\{0,1,2\}^3}P(u),\qquad
 \lambda_2=L+\frac1{28450}E
 \quad\text{on polynomials of degree at most four.}
                                                        \tag{5}
\]
The tensor grid is unisolvent for polynomials whose degree in each
variable is at most two: successive use of the univariate root bound
shows that a polynomial vanishing on the grid must be zero. Hence
\(E(q^2)>0\) for every nonzero real quadratic-or-lower polynomial
\(q\). Since \(L(q^2)\ge0\) on \(V_2\), (5) is strictly
positive on its nonzero squares. Direct integer evaluation of the
fixed \(F\) gives
\[
 E(F)=28449,\qquad
 \lambda_2(F)=-4+\frac{28449}{28450}
             =-\frac{85351}{28450}=-a_0.
                                                        \tag{6}
\]

Now suppose \(\lambda_{d-1}\) has been constructed, where
\(d\ge3\). Extend it to degrees at most \(2d\) by assigning
zero to all monomials of degrees \(2d-1\) and \(2d\). Call this
extension \(\widehat\lambda_{d-1}\). On the nested basis of
\(I_d\), write its square Gram matrix in blocks as
\[
 \bigl(\widehat\lambda_{d-1}(q_iq_j)\bigr)_{i,j}
       =\begin{pmatrix}A&B\\B^{\mathsf T}&C\end{pmatrix},
                                                        \tag{7}
\]
where the first block indexes \(I_{d-1}\). By induction \(A\)
is positive definite, so its rational inverse exists.

If \(P_{2d}\) denotes the homogeneous component of degree \(2d\),
define
\[
 M_d(P)=\sum_{u\in\{0,1,\ldots,d\}^3}P_{2d}(u).
                                                        \tag{8}
\]
Old–old and old–new products have degree below \(2d\), so this
functional changes neither the upper-left block nor the off-diagonal
blocks of (7). On the new basis elements it gives the integer matrix
\[
 D_{mn}=\prod_{v=1}^3\left(\sum_{j=0}^{d}
                j^{\,\alpha_v(m)+\alpha_v(n)}\right),
                                                        \tag{9}
\]
where \(\alpha(m)\) is the exponent triple of the corresponding
degree-\(d\) monomial. The convention \(j^0=1\) includes \(j=0\).
The matrix \(D\) is positive definite. For any nonzero vector of
coefficients, the associated degree-\(d\) homogeneous form is
nonzero and has coordinate degrees at most \(d\). The grid in (8)
is unisolvent for those coordinate degrees, so the sum of its squared
values is positive. In particular, \(\det D\) is a positive integer.

All remaining choices are explicit. Set
\[
 \begin{aligned}
 S&=C-B^{\mathsf T}A^{-1}B,\\
 m_d&=\max_i\sum_j|S_{ij}|,\\
 \beta_d&=\frac{\det D}{(\operatorname{tr}D)^{h_d-1}},\\
 T_d&=\left\lceil\frac{m_d+1}{\beta_d}\right\rceil,\\
 \lambda_d&=\widehat\lambda_{d-1}+T_dM_d.
 \end{aligned}                                           \tag{10}
\]
These are rational arithmetic operations, followed by one integer
ceiling. To verify the bound, symmetry gives \(S\succeq-m_dI\).
Also, if the eigenvalues of \(D\) are positive, their product is
at most its smallest eigenvalue times
\((\operatorname{tr}D)^{h_d-1}\). Thus
\(D\succeq\beta_dI\), and
\[
                         S+T_dD\succeq I.
                                                        \tag{11}
\]
The Schur complement criterion applied to (7) proves that
\(\lambda_d\) is strictly positive on every nonzero square from
\(V_d\). Since \(\deg F=4<2d-1\), its value on \(F\)
remains \(-a_0\). This proves the induction and (1).
All monomial values of every \(\lambda_d\) have denominators
dividing 28450: (5) has this property, and each new contribution in
(10) has integer coefficients. This denominator statement does not
bound the growth of their numerators.

Here is the resulting radial threshold. For a chosen \(N\ge0\),
construct \(\lambda_{N+2}\), write \(s=x^2+y^2+z^2\), and compute
\[
 c_{N,k}=\binom Nk\lambda_{N+2}(s^kF),\qquad
 A_N=\sum_{k=1}^{N}|c_{N,k}|,
 \qquad A_0=0.
                                                        \tag{12}
\]
Define
\[
 \boxed{\displaystyle
 \tau_N=\left\lceil
       \sqrt{\max\left\{1,\frac{2(A_N+1)}{a_0}\right\}}
                       \right\rceil .}
                                                        \tag{13}
\]
The square-root ceiling can be computed by integer comparisons on
the numerator and denominator, without a floating-point operation.
For \(0\le\varepsilon\le1\),
\[
 \lambda_{N+2}((1+\varepsilon s)^NF)
 =-a_0+\sum_{k=1}^N c_{N,k}\varepsilon^k
 \le-a_0+\varepsilon A_N.
\]
If \(t\ge\tau_N\), then \(\varepsilon=t^{-2}\) also satisfies
\(\varepsilon\le a_0/(2(A_N+1))\). Therefore the last expression
is strictly less than \(-a_0/2\). On the other hand, a rational
SOS of this polynomial would have factors of degree at most \(N+2\)
vanishing at \(p\), and (1) would make its value under
\(\lambda_{N+2}\) nonnegative. This contradiction excludes such an
SOS. Rational substitution \(X=x/t\) then proves the assertion at
the start of the note. The case \(N=0\) is included and gives
\(\tau_0=1\).

Let \(\nu(t)\) be the least radial order certifying
\(t^{-2}F(tX)\); its finiteness is established in the companion note.
The bound is fully recursive and effective. Thresholds need not be
claimed monotone or optimal; replacing \(\tau_N\) by
\(\max_{0\le j\le N}\tau_j\) gives a nondecreasing sequence if
needed. Together with upward closure of the radial SOS hierarchy, any
computed threshold yields a certified lower bound \(\nu(t)>N\)
for all integer \(t\ge\tau_N\). The separate height analysis bounds
the growth of (10) and obtains
\(\nu(t)=\Omega(\log\log t/\log\log\log t)\), equivalently
\(\Omega(\log L/\log\log L)\) for this integer family's binary
input length \(L=\Theta(\log t)\).

At the first extension, \(d=3\), the exact constants in the stated
basis order are
\[
 \begin{aligned}
 \det D&=5226018400740990389182812651520,\\
 \operatorname{tr}D&=73784,\\
 m_3&=\frac{9404050821622998287}{1365315554567100},\\
 \beta_3&=\frac{38936871295727717795840}
                  {482891852308771687305501478648808263},\\
 T_3&=85434602576348679,\\
 A_1&=\frac{21625546155409857068677729019}{28450}.
 \end{aligned}
\]
These give (13)'s integer threshold \(711859414639\). Thus an
explicit separator for this instance is (5) on degrees at most four,
zero on degree five, and \(T_3\) times the grid functional (8) on
degree six. Its square Gram matrix on \(I_3\) is positive definite.

The [targeted exact checker](check_rational_radial_quantitative_separation.py)
reconstructs \(F\), the nested bases, and the functionals. It checks
the five positive leading principal minors of the base Gram matrix,
the ten positive leading principal minors of \(D\), the exact block
update, \(T_3\beta_3-m_3\ge1\), all fifteen positive leading
principal minors of the updated Gram matrix, the preserved value on
\(F\), and strict negativity at the stated threshold. The command
actually run was

```text
python3 research-20260927/check_rational_radial_quantitative_separation.py
```

It passed. A temporary prototype first needed its polynomial domain
changed from integers to rationals before evaluating the rational
perturbation; the saved checker uses \(\mathbb Q\) throughout. A
fresh independent reader reconstructed the first step with separate
code and matched \(E(F)\), \(\lambda_2(F)\), \(\det D\),
\(\operatorname{tr}D\), and \(T_3\), while also checking the
\(N=1\) negativity estimate. A further reader checked the basis
and threshold formulas. Those checks cover the first
extension; the proof by induction covers arbitrary \(N\). No
project-wide checks, numerical optimization, or CI inspection were
performed.
