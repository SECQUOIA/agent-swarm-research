# Rational minimizers of strongly SOS-convex quartics can require exponentially many bits

Date: 2026-09-28. Status: passed
[fresh independent adversarial review](rational-convex-quartic-minimizer-height-review.md).
Publication priority is unestablished.

A rational minimizer need not have a short ordinary binary description,
even for an unconstrained globally strongly convex rational quartic with
an explicit rational SOS expression and a supplied positive definite
rational Hessian Gram. The construction below keeps every minimizer
coordinate in the interval \([-1,1]\). Its large representation comes
entirely from denominators.

## Statement

**Theorem.** For every integer \(k\geq0\), there is a deterministic
polynomial-time construction of a rational quartic \(F_k\) in
\(N=2(k+1)\) variables, together with a sum of \(N+1\) rational
quadratic squares and a positive definite rational full Hessian Gram
on \((v,X\otimes v)\), such that:

1. \(\nabla^2F_k(X)\succeq I\) for every real \(X\).
2. \(\min F_k=0\), and its unique minimizer \(p\) is rational.
3. Every coordinate of \(p\) lies in \([-1,1]\). Each of the last
   two coordinates has reduced denominator exactly \(5^{2^k}\).
4. The expanded quartic, its rational square factors, and the Hessian
   Gram all have bit length polynomial in \(k\).

Consequently, writing the unique rational minimizer as ordinary reduced
fractions requires at least \(2^k\log_2 5\) bits in a single
coordinate. This is exponential in \(N\) and superpolynomial in the
constructed input length. No bound of the form
\(2^{\Omega(\text{total input bits})}\) is asserted.

The Hessian Gram may also be normalized to be at least the identity
by multiplying \(F_k\) by a rational integer square of polynomial
bit length. This does not change its minimizer or zero set.

## A rational chain on the unit circle

Let
\[
 z_0=(3+4\mathrm i)/5,\qquad z_j=z_{j-1}^2
       =a_j+\mathrm i b_j\quad(1\leq j\leq k).
 \tag{1}
\]
Every \(a_j,b_j\) is rational and \(a_j^2+b_j^2=1\).
Use variables \((x_j,y_j)\), \(0\leq j\leq k\), and define
\[
 \begin{aligned}
 r_0&=x_0-3/5,&s_0&=y_0-4/5,\\
 r_j&=x_j-x_{j-1}^2+y_{j-1}^2,&
 s_j&=y_j-2x_{j-1}y_{j-1}\quad(1\leq j\leq k),\\
 q_j&=x_j^2+y_j^2-1&& (0\leq j\leq k).
 \end{aligned}
 \tag{2}
\]
The \(N\) residuals \(r_j,s_j\) have the unique common real
zero \(p=(a_j,b_j)_{j=0}^k\). Their coefficients have constant
bit length. Every \(q_j\) also vanishes at \(p\).

Write
\[
 (3+4\mathrm i)^m=A_m+\mathrm i B_m\in\mathbb Z[\mathrm i].
\]
The element \(3+4\mathrm i\) is idempotent modulo five, since its
square is \(-7+24\mathrm i\), congruent to itself. Hence, for every
positive integer \(m\),
\[
 A_m\equiv3\pmod5,\qquad B_m\equiv4\pmod5.
 \tag{3}
\]
Taking \(m=2^j\) proves that both coordinates of \(z_j\) have
reduced denominator exactly \(5^{2^j}\). The numerator sizes need
not be bounded separately for the lower bound; their absolute values
are at most the denominator because \(|z_j|=1\).

## A positive exposing quadratic without expanding the chain

Set
\[
 E_0=(x_0-3/5)^2+(y_0-4/5)^2,
 \qquad
 E_j=q_j-2a_jr_j-2b_js_j-2q_{j-1}\quad(1\leq j\leq k).
 \tag{4}
\]
Each \(E_j\) vanishes at \(p\), and its full gradient vanishes
there. To check the predecessor block, let
\(\Phi(x,y)=(x^2-y^2,2xy)\). On the unit circle,
\[
 D\Phi(a_{j-1},b_{j-1})^{\mathsf T}(a_j,b_j)
                =2(a_{j-1},b_{j-1}).
 \tag{5}
\]
The gradient from \(-2a_jr_j-2b_js_j\) is therefore exactly
cancelled by that from \(-2q_{j-1}\). The current-coordinate
gradient cancels directly.

The quadratic part of \(E_j\) consists of the identity on its
current pair and the matrix
\[
 B_j=2\begin{pmatrix}a_j-1&b_j\\b_j&-a_j-1\end{pmatrix}
 \tag{6}
\]
on the predecessor pair. There are no cross terms between different
pairs. Since \(a_j^2+b_j^2=1\), the eigenvalues of \(B_j\) are
zero and minus four.

Let \(\omega_j=8^{-j}\), and define
\[
 E^*=\sum_{j=0}^k\omega_jE_j.
 \tag{7}
\]
Its quadratic-part matrix \(H_*\) is block diagonal. Block \(j<k\)
is \(\omega_jI+\omega_{j+1}B_{j+1}\), whose eigenvalues lie in
\([\omega_j/2,\omega_j]\). The last block is \(\omega_kI\).
Thus
\[
 E^*(p+u)=u^{\mathsf T}H_*u,
          \qquad \omega_kI\preceq H_*\preceq I.
 \tag{8}
\]
The exact coefficients \(a_j,b_j\) in (4) have huge expanded
size. They will only be approximated, while all basis quadratics in
(2) retain their exact small rational coefficients and their exact
zero at \(p\).

Choose rational approximations \(\widehat a_j,\widehat b_j\) with
coordinate error at most \(\eta\), replace those coefficients in
(4), and call the weighted sum \(G\). Then \(G(p)=0\) exactly.
Set \(V=4N\). Each residual gradient at \(p\) has norm at most
\(V\). Each predecessor-block error has norm at most \(4\eta\),
so
\[
 G(p+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,
 \quad \|H-H_*\|_2\leq4\eta,
 \quad \|\ell\|_2\leq4kV\eta.
 \tag{9}
\]
For \(k=0\), the approximation sum is empty and these errors are
zero. For any rational \(0<\varepsilon\leq1\), choose
\[
 \eta\leq\min\left\{1,\frac{\omega_k}{8},
                \frac{\varepsilon}{4(k+1)V}\right\}.
 \tag{10}
\]
Then, putting \(m=\omega_k/2\) and \(L=2\),
\[
 mI\preceq H\preceq LI,\qquad \|\ell\|_2\leq\varepsilon.
 \tag{11}
\]

The approximations in (10) can be computed without first writing any
large fraction in (1). Iterate \(\Phi\) with dyadic rounding. If a
current approximation is within Euclidean distance one of its true
unit-circle point, the map has error amplification at most three:
\[
 |\widehat z^2-z^2|
       \leq(|\widehat z|+|z|)|\widehat z-z|
       \leq3|\widehat z-z|.
\]
Round each new real and imaginary coordinate with absolute error at
most \(h\). The Euclidean error satisfies
\(e_j\leq3e_{j-1}+2h\), with \(e_0=0\), and consequently
\(e_j\leq h(3^j-1)\). Taking dyadic
\(h\leq\eta/(2\cdot3^k)\) proves inductively that all errors are
at most \(\eta/2\leq1\). The number of bits and rational arithmetic
operations is polynomial in \(k+\log(1/\eta)\).

## From the exposing quadratic to the quartic and its certificate

Here we use the general quantitative calculations in the reviewed
[strongly convex quartic realization](general-strongly-convex-quartic-singleton.md)
and its [rational Hessian certificate](sos-convex-quartic-realization.md).
Their estimates only use the translated residual bounds described
below; they do not require an irreducible univariate defining polynomial.

The Jacobian \(J\) of the \(N\) residuals in (2) is block lower
triangular with identity diagonal blocks. Thus \(\det J=1\).
Its Frobenius norm is at most \(4N=V\). The product of its singular
values gives
\[
 J^{\mathsf T}J\succeq\nu^2I,
                   \qquad \nu=V^{-(N-1)}.
 \tag{12}
\]
Each residual has the translated expansion
\(c_j^{\mathsf T}u+u^{\mathsf T}T_ju\), where
\(\|c_j\|_2\leq V\) and \(\|T_j\|_2\leq1\).
The base residuals are linear, which satisfies this bound with
\(T_j=0\). For a later real residual its quadratic part has entries
minus one and one on the predecessor diagonal; for an imaginary
residual its two off-diagonal entries are minus one.

Choose a square dyadic \(\varepsilon=t^2>0\) satisfying
\[
 \varepsilon\leq\min\left\{1,\frac{m^2}{2N},
       \frac{\nu^2m^2}{36N(L+NV)^2}\right\},
 \tag{13}
\]
then construct \(G\) with (10). Define
\[
 F_k=\left(\frac{G}{t\nu}\right)^2+
        \sum_{j=0}^k\left[
             \left(\frac{r_j}{\nu}\right)^2+
             \left(\frac{s_j}{\nu}\right)^2\right].
 \tag{14}
\]
The cited estimates give \(\nabla^2F_k\succeq(3/2)I\), as well
as a positive definite full Hessian Gram in coordinates centered at
\(p\). Translation back preserves positive definiteness.

For completeness, constructing a small rational Gram does not require
expanding \(p\). The Schur-complement margin and the translation
bound in the certificate proof are positive rationals of polynomial
bit length, using \(\|p\|\leq N\). Every entry of the translated
Gram is a polynomial of degree at most two in \(p\), with rational
coefficients of polynomial bit length. The dyadic iteration above
therefore computes a rational approximation within one quarter of a
known positive spectral margin using polynomially many bits. Orthogonal
projection onto the exact rational Hessian coefficient equations, as
specified in that certificate proof, is nonexpansive and preserves the
positive margin. It returns the required exact rational Gram in
polynomial time.

All logarithms of reciprocals in (10)--(13) are
\(O(N\log N+k)\), up to fixed constant factors and the precision
of the requested Gram approximation. The quartic, its \(N+1\)
factors, and the \((N+N^2)\)-dimensional Gram have polynomially many
coefficients, each of polynomial bit length. The quartic degree is
exactly four because \(G\) has a positive definite quadratic part.
Every factor in (14) vanishes at \(p\); thus \(F_k(p)=0\).
The residual equations already force \(p\), and strong convexity
also proves uniqueness.

If the Gram is denoted by \(M\), its computable rational spectral
lower bound
\(\rho=\det M/(\operatorname{tr}M)^{N+N^2-1}>0\) has
polynomial bit length. Choose an integer \(c\geq1\) with
\(c^2\rho\geq1\). Multiplying the quartic by \(c^2\), and all
its square factors by \(c\), normalizes the full Gram to be at least
identity with the same bit-size guarantees.

## Consequences and limits

This example answers the rational-minimizer-height question negatively
under a strong, efficiently checkable convexity promise. It also gives
a singleton \(\{X:F_k(X)\leq0\}\) containing a rational point,
but no rational point of polynomial expanded bit length.

The example has a small rational SOS certificate and a small rational
Hessian certificate. Thus a large rational optimizer does not by itself
force a large nonnegativity certificate or a large Gram. In this family,
the optimizer also has a short exact arithmetic circuit, namely (1).
No complexity-class separation or lower bound for all possible exact
representations is claimed. Approximation to any prescribed precision
remains efficient.

The long-witness result for a
[strictly feasible quartic body](strict-convex-quartic-rational-witness-lower-bound.md)
uses proximity to an irrational coordinate. Here the minimizer itself
is rational, and the feasible set at level zero is a singleton. Neither
result implies the other.

The [primary comparison](rational-minimizer-height-prior.md) distinguishes
norm and approximation bounds, exact optimization with a supplied
denominator bound, and earlier exponential witnesses from nonconvex
optimization and convex quadratic systems. The proposed contribution
is the combination of a bounded rational minimizer, a single globally
strongly SOS-convex quartic, and short rational certificates. An
unsuccessful literature search does not establish novelty.

The construction also forces large rational entries in every
maximal-rank optimal Gram and every matrix exposing its optimal Gram
face. The [separate consequence note](rational-circle-optimal-gram-height.md)
states the precise rank restriction and its review status. The supplied
short SOS Gram has smaller rank.

## Verification

The fresh reviewer independently reconstructed the proof and checked
the imported quartic estimates through their abstract hypotheses. No
substantive correction was needed. The review also supplies an explicit
polynomial precision bound for constructing the rational Hessian Gram
without expanding the optimizer.

The reviewer wrote and ran the exact checker below; the author then
ran the same checker independently, with the same passing result:

```text
python research-20260927/check_rational_circle_minimizer_review.py
```

It checks the symbolic circle identity, reduced denominators, rounded
exposer values, curvature margins, and Jacobians for \(k=0,\ldots,8\).
At \(k=1\), it verifies an exact positive definite Hessian Gram,
its polynomial identity, translation, and rational coefficient
projection. These finite checks support the algebra; the uniform
inequalities and polynomial bit bounds rely on the proofs. No Lean,
project-wide verification, or CI inspection is claimed.
