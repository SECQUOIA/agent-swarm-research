# Rational SOS certificates need not preserve block separation

Date: 2026-09-28. Status: construction and encoding consequences passed
a [fresh independent review](rational-block-sos-splitting-obstruction-review.md).
Publication priority remains unestablished.

A rational quartic of the form \(f(x)+g(y,z)\) can have a short
rational SOS certificate while neither a rational constant shift nor
a different rational Gram permits an SOS certificate separated between
the two variable blocks. The obstruction already occurs with both
block minima equal to zero.

A separate, strictly positive family has rational certificates of
both kinds. Its joint rational SOS remains short, while every
certificate respecting the prescribed two blocks needs exponentially
many denominator bits. This is a cost of imposing separation, not a
lower bound for unrestricted rational SOS or PSD Gram certificates.

## 1. A rational quartic lifting lemma

Let \(f\in\mathbb Q[x_1,\ldots,x_n]\), \(n\ge1\), be a
quartic with minimum zero at \(p\). Suppose a rational positive
definite full Hessian Gram \(A\) is supplied:
\[
 u^{\mathsf T}\nabla^2 f(x)u
       =(u,x\otimes u)^{\mathsf T}A(u,x\otimes u).
                                                        \tag{1}
\]
The point \(p\) need not be supplied or rational. Set
\[
 h=n+n^2,\qquad
 \rho=\frac{\det A}{(\operatorname{tr}A)^{h-1}}>0,
 \qquad \mu=\rho/2.
                                                        \tag{2}
\]
Thus \(A\succeq\rho I\). All constructions below use rational
arithmetic and have polynomial size in the expanded input \((f,A)\).

Take another \(n\)-tuple \(y\), and introduce
\(m=n(n+1)/2\) variables \(z_{ij}\), \(i\le j\). Write
\[
                   r_{ij}=y_iy_j-z_{ij}.
                                                        \tag{3}
\]
In each cubic monomial of \(\nabla f(y)\), replace a selected
product \(y_iy_j\) by \(z_{ij}\). For example, choose the first
two indices in the sorted index list of that monomial. Leave gradient
terms of degree at most two unchanged. This gives a rational vector
\(a(y,z)\) of degree at most two with
\[
 a(y,(y_iy_j)_{i\le j})=\nabla f(y),\qquad
 e(y,z):=\nabla f(y)-a(y,z)=E(y)r,
                                                        \tag{4}
\]
where \(E(y)\) is a rational matrix of homogeneous linear
polynomials. No cubic factor will need to be squared in the final
certificate.

We will choose a positive rational \(\lambda\) and define
\[
 g(y,z)=\frac{\|a(y,z)\|^2}{2\mu}-f(y)
                                      +\lambda\|r(y,z)\|^2.
                                                        \tag{5}
\]
This polynomial has degree at most four.

**Lifting lemma.** A suitable \(\lambda\) and a rational SOS
certificate for \(f(x)+g(y,z)\) can be constructed in deterministic
polynomial time with polynomial bit length. Every square factor has
degree at most two. Moreover,
\[
 g\ge0,\qquad g(p,(p_ip_j)_{i\le j})=0.
                                                        \tag{6}
\]

## 2. A positive Taylor Gram absorbs the lifting error

Put \(d=x-y\), and use the polynomial list
\[
                  w=(d,y\otimes d,d\otimes d).
                                                        \tag{7}
\]
Its length is \(b=n+2n^2\), and its entries have degree at most
two. The Taylor remainder is
\[
 T_f(x,y)=f(x)-f(y)-\nabla f(y)^{\mathsf T}d
       =\int_0^1(1-t)
       (d,(y+td)\otimes d)^{\mathsf T}
       A(d,(y+td)\otimes d)\,dt.
                                                        \tag{8}
\]
Partition \(A\) according to its constant and tensor blocks.
An exact rational Gram for (8) on \(w\) is
\[
 M=\begin{pmatrix}
 A_{00}/2&A_{01}/2&A_{01}/6\\
 A_{10}/2&A_{11}/2&A_{11}/6\\
 A_{10}/6&A_{11}/6&A_{11}/12
 \end{pmatrix}.
                                                        \tag{9}
\]
Since \(A\succeq\rho I\),
\[
 M\succeq\rho\left[
 \frac12I_n\ \oplus\
 \left(\begin{pmatrix}1/2&1/6\\1/6&1/12\end{pmatrix}
                                    \otimes I_{n^2}\right)\right].
                                                        \tag{10}
\]
The small block has positive diagonal and determinant \(1/72\).
Consequently
\[
 N=M-\frac\mu2\operatorname{diag}(I_n,0,0)\succ0:
                                                        \tag{11}
\]
its lower bound in (10) retains the first block \(\rho I_n/4\)
and the same positive tensor block. This is a statement about the
ordinary matrix; redundant entries in \(w\) cause no difficulty.

By (4), a rational matrix \(D\) satisfies
\[
                    e(y,z)^{\mathsf T}d=r^{\mathsf T}Dw.
                                                        \tag{12}
\]
Only the \(y\otimes d\) columns are needed. Define
\[
 \delta=\frac{\det N}{(\operatorname{tr}N)^{b-1}}>0,
 \qquad
 \lambda=\left\lceil1+\frac{\|D\|_F^2}{4\delta}\right\rceil.
                                                        \tag{13}
\]
Because \(N\succeq\delta I\), the Schur complement proves
\[
 K=\begin{pmatrix}N&D^{\mathsf T}/2\\D/2&\lambda I_m\end{pmatrix}
 \succ0.
                                                        \tag{14}
\]
Explicitly, its Schur complement after eliminating \(N\) satisfies
\[
                 \lambda I_m-\frac14DN^{-1}D^{\mathsf T}\succeq I_m.
\]
The required polynomial identity is now
\[
 \boxed{
 f(x)+g(y,z)=
 \begin{pmatrix}w\\r\end{pmatrix}^{\mathsf T}
 K\begin{pmatrix}w\\r\end{pmatrix}
       +\frac\mu2\|d+a(y,z)/\mu\|^2.}
                                                        \tag{15}
\]
To check the signs, the first term equals
\(T_f-\mu\|d\|^2/2+e^{\mathsf T}d+\lambda\|r\|^2\).
The completed square adds
\(\mu\|d\|^2/2+a^{\mathsf T}d+\|a\|^2/(2\mu)\).
Since \(e+a=\nabla f(y)\), (8) gives exactly (5) and (15).

Both parts of (15) have rational positive semidefinite coefficient
matrices. Rational LDL factorization and binary expansion of positive
rational weights produce an unweighted rational SOS. Matrix dimensions,
coefficient matching, determinants, trace powers, and the ceiling in
(13) all have polynomial bit complexity. The degree-two factors have
polynomial total encoding length. This procedure never computes the
algebraic zero \(p\).

At \((y,z)=(p,(p_ip_j))\), both \(r\) and \(a=\nabla f(p)\)
vanish, and \(f(p)=0\), proving the equality in (6). For arbitrary
\((y,z)\), substitute \(x=p\) into the real nonnegative SOS
identity (15). This proves \(g(y,z)\ge0\). These steps complete
the lifting lemma.

## 3. Rational block separation can fail to exist

Choose the fixed three-variable \(k=1\) member of the reviewed
[quintic-tower construction](exponential-least-sos-field.md).
It has minimum zero at \(p=(a,a^2,a^3)\), where \(a=2^{1/5}\),
a supplied rational positive definite full Hessian Gram, and no
rational SOS or rational PSD polynomial Gram. Denote it by \(f\),
and apply the lifting lemma to obtain \(g\).

There are three \(x\) variables and nine \((y,z)\) variables.
The rational quartic
\[
                          P(x,y,z)=f(x)+g(y,z)
                                                        \tag{16}
\]
has a rational SOS with quadratic factors by (15).

If rational block-separated squares existed, comparison of the two
independent blocks would give a rational constant \(t\) such that
\[
 f(x)+t=\sum_i u_i(x)^2,\qquad
 g(y,z)-t=\sum_j v_j(y,z)^2.
                                                        \tag{17}
\]
The zero minimum of \(f\) forces \(t\ge0\), and the zero
minimum of \(g\) forces \(t\le0\). Thus \(t=0\), which
would make \(f\) rational SOS, a contradiction. The same proof
excludes separated rational PSD Grams.

This disproves rational block splitting for quartics, even without
an encoding restriction. It does not disprove real block splitting:
\(f\) is real SOS by its Taylor certificate at its zero, and
\(g=P(p,y,z)\) is real SOS by (15).

## 4. Separation alone can force an algebraic coefficient field

The lifting lemma also applies to the reviewed
[quintic-tower quartics](exponential-least-sos-field.md). Write their
polynomials as \(f_k\), their unique zeros as \(p_k\), and their
distinguished field elements as \(a_k=2^{1/5^k}\). Apply the lift
to obtain \(g_k\) and
\[
                         J_k(x,y,z)=f_k(x)+g_k(y,z).
                                                        \tag{18}
\]
The quartic and an unrestricted rational SOS have polynomial size in
\(k\). The total number of variables is \(O(k^2)\).

For every real field \(E\), a block-separated SOS over \(E\)
exists if and only if \(a_k\in E\). Necessity follows as in
(17): both block minima are zero, so the constant shift vanishes and
the first block is an SOS of \(f_k\) over \(E\). The imported
field theorem then forces \(a_k\in E\).

Conversely, if \(a_k\in E\), the tower theorem supplies an SOS
of \(f_k\) over \(E\), and \(p_k\in E^{3k}\). Substitution
of \(x=p_k\) in the rational SOS for \(J_k\) gives an SOS of
\(g_k\) over \(E\). The same equivalence holds for separated
PSD polynomial Grams.

Thus the least real coefficient field for the separated certificates
is exactly \(\mathbb Q(a_k)\), while the joint certificate is
rational. For certificates with algebraic coefficients, the reviewed
[individual-coefficient lemma](exponential-sos-individual-coefficient-degree.md)
implies that at least one separated coefficient has degree at least
\(5^k\). This is exponential in tower depth \(k\); after the
quadratic lifting, it is \(5^{\Theta(\sqrt{N})}\) in the total
variable count \(N\), not \(5^{\Theta(N)}\). It does not exclude
short root-circuit descriptions of those algebraic coefficients.

## 5. Strict positivity gives existence with a large rational cost

Return to the fixed three-variable \(f\) and its fixed lift \(g\)
from Section 3. In an independent \(2k\)-variable block \(\xi\),
take the strictly positive quartic \(h_k\) from the reviewed
[interior-Gram lower-bound construction](interior-gram-bit-lower-bound.md).
It has polynomial input size, a short rational SOS, a rational positive
definite full Hessian Gram, and a positive attained minimum \(m_k\)
satisfying
\[
 0<m_k<4M_k^{-2^{k+1}},\qquad M_k=1000^{k+3}.
                                                        \tag{19}
\]
Only those properties of \(h_k\) are used here.

Set
\[
 G_k(y,z,\xi)=g(y,z)+h_k(\xi),\qquad
 P_k(x,y,z,\xi)=f(x)+G_k(y,z,\xi).
                                                        \tag{20}
\]
The polynomial \(P_k\) is strictly positive, has \(2k+12\)
variables, and has a polynomial-size rational SOS obtained by adding
the certificates for (16) and \(h_k\). Also \(\min G_k=m_k\).

Rational certificates separated between \(x\) and \((y,z,\xi)\)
do exist. Choose rational \(t\) with \(0<t<m_k\). The strictly
positive polynomial \(f+t\) has a rational positive definite Gram
by the reviewed
[rational-center Taylor lemma](interior-gram-single-exponential-upper.md#2-an-explicit-rational-polynomial-gram).
Choose a rational point \(q\) sufficiently close to the zero of
\(f\) that \(s=f(q)<m_k-t\). Restricting (15) at \(x=q\)
gives a rational SOS for \(g+s\). The polynomial
\(h_k-(t+s)\) is strictly positive with the same strict rational
Hessian Gram as \(h_k\), so the same lemma gives a rational SOS.
Their sum is
\[
                 G_k-t=(g+s)+(h_k-t-s).
                                                        \tag{21}
\]
No short-bit claim is made for this choice of \(t\), \(q\), or
these separated certificates.

Every rational separated certificate, however, is long. Its constant
shift \(t\) satisfies
\[
                              0<t\le m_k.
                                                        \tag{22}
\]
Nonnegativity gives \(t\ge0\) and \(t\le\min G_k\);
equality \(t=0\) would make \(f\) rational SOS or give it a
rational PSD Gram. Writing \(t=a/b\) in lowest terms with
\(a,b>0\), equations (19)--(22) give
\[
                        \log_2 b>2^{k+1}\log_2M_k-2.
                                                        \tag{23}
\]

This scalar is determined by the certificate, even if the output does
not list it. Let \(\nu\) be the fixed denominator of \(f(0)\).
A separated Gram certificate here means two local rational PSD
matrices, one for \(f+t\) and one for \(G_k-t\), each on its
ordinary monomial basis with its own constant entry. The first local
matrix therefore has \(Q_{00}=f(0)+t\). Thus
\[
 \log_2\operatorname{den}(Q_{00})
       \ge\log_2 b-\log_2\nu.
                                                        \tag{24}
\]
One Gram entry already requires \(\Omega(k2^k)\) denominator bits.

For an unweighted separated SOS, let \(c_i=u_i(0)\). Then
\(t=\sum_i c_i^2-f(0)\), whose denominator divides
\(\nu\prod_i\operatorname{den}(c_i)^2\). Consequently
\[
 \sum_i\log_2\operatorname{den}(c_i)
   >2^k\log_2M_k-1-\tfrac12\log_2\nu.
                                                        \tag{25}
\]
This proves an \(\Omega(k2^k)\) lower bound for the total
ordinary rational coefficient length of every separated SOS. It is
an actual certificate-size bound, not a requirement to print an
otherwise optional shift. The bound is exponential in the total
variable count of this positive family and superpolynomial in its
polynomially bounded input size. It is not stated as
\(2^{\Omega(\text{total input bits})}\).

## Scope and review status

The zero-minimum example shows failure of rational separated existence.
The strictly positive family shows exponential growth for existing
rational separated certificates. Both have short unrestricted rational
SOS certificates. These are different conclusions, and neither is an
unrestricted PSD Gram or SOS lower bound.

The base lift here makes no convexity assertion for \(g\) or the
joint polynomials. A [separate reviewed supplement](strongly-sos-convex-block-splitting-obstruction.md)
makes the fixed-field example and the positive certificate-size family
strongly SOS-convex. The [reviewed quadratic graph theorem](quadratic-graph-quartic-realization.md)
also upgrades the growing-field example with polynomial-size data.
A nontrivial block-separable polynomial
cannot have a positive definite Gram on the full joint Hessian vector
\((u,X\otimes u)\): holding one block and a direction in that
block fixed while sending another block to infinity contradicts the
uniform positive matrix margin. The present construction therefore
does not extend the earlier result within its strict full-Hessian
class.

The question of real block separation is an established one.
[Kojima, Kim, and Waki](https://www.researchgate.net/publication/2477507_Sparsity_in_Sums_of_Squares_of_Polynomials)
discuss it in *Sparsity in Sums of Squares of Polynomials*, and report
the zero-minimum case in their concluding discussion. The obstruction
here concerns rational coefficients; the zero-minimum blocks above
do have real SOS decompositions. This comparison does not establish
publication priority for the rational construction or its quantitative
consequences. The [scoped primary-source audit](rational-block-sos-splitting-prior.md)
compares the precise real and rational conclusions and explains why
known rational-preserving support projections do not contradict them.

The author and the root independently reconstructed the lifting
identity and its positive Gram construction. A reviewer who did not
contribute to the lift checked the full proof and final mathematical
revision. A further fresh reader checked the denominator extraction
and its encoding scope. The review records the source hashes, exact
checks, explicit Schur complement, and two-local-Gram convention.
No finite computation is claimed to establish the universal statements.
No project-wide verification, CI inspection, or Lean formalization was
performed for this note.

A targeted inline Python document check passed five local links,
balanced math delimiters, whitespace, control characters, and the final
newline. This formatting check is separate from mathematical review.
