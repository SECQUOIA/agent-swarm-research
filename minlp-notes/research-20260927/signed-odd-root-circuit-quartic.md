# Quartic realization of signed odd-root circuits with certified intervals

Date: 2026-09-28. Status: quantitative construction independently
checked in [the adversarial review](signed-odd-root-circuit-review.md).
Publication priority is unestablished.

The [reviewed cube-root construction](monotone-cube-root-circuit-quartic.md)
extends to odd roots and signed coefficients if the input gives rational
intervals that certify the roots stay away from zero. The intervals are
checked by rational arithmetic. The construction allows cancellation
inside a radicand without expanding a common minimal polynomial.

## Input, theorem, and scope

Let a circuit have \(k\geq1\) gates in topological order. Gate \(i\)
has an odd degree \(d_i=2n_i-1\geq3\), encoded in unary, and defines

\[
 \xi_i^{d_i}=c_i+
   \sum_{j<i}\sum_{e=1}^{n_j}a_{ije}\xi_j^e,
 \qquad c_i,a_{ije}\in\mathbb Q.
 \tag{1}
\]

Signed coefficients are allowed. Along with the circuit, the input gives
rational intervals \([L_i,U_i]\) not containing zero. The interval
evaluation of the right side of (1), using the interval powers of the
earlier boxes, must lie inside \([L_i^{d_i},U_i^{d_i}]\). All powers
and endpoint comparisons in this condition are exact rational
operations. Induction proves that every real gate value lies in its
box. Every gate has exactly one real root.

Put \(N=\sum_i n_i\). There is a deterministic algorithm, polynomial
in the binary input length and the unary degrees, that constructs a
rational quartic in \(N\) variables with the following properties:

1. Its Hessian is at least \(I\) everywhere.
2. Its zero set is the singleton consisting of the normalized gate
   powers described below; an explicit rational diagonal map recovers
   \((\xi_i^e)_{i,e}\).
3. It is a sum of \(N+1\) rational quadratic squares.
4. It has a positive definite rational Hessian Gram matrix on the full
   basis \((v,X\otimes v)\).

Every output has polynomial bit length. This is a construction under a
checkable input condition, not a polynomial-time procedure for finding
such boxes for an arbitrary circuit. The condition rules out roots
equal to zero and includes the encoded distance from zero in the input
size. General multiplication of independent gate values is not part of
(1). Products implicit in a single retained gate power are allowed.

For example, \(\xi_1=\sqrt[3]2\) and
\(\xi_2=(6-\xi_1^2)^{1/5}\) have the valid boxes
\([1,3/2]\) for both gates. The second radicand interval is
\([15/4,5]\), contained in \([1,(3/2)^5]\).

## Normalization and bounds

Let \(\sigma_i\in\{-1,1\}\) be the sign of the box, and choose

\[
 \kappa=\max\left\{1,
      \max_i\frac1{\min(|L_i|,|U_i|)}\right\}.
\]

Set \(\alpha_i=\sigma_i\kappa\xi_i\). Its transformed box is
positive with lower endpoint at least one. The transformed coefficients
in (1) are

\[
 c_i'=\sigma_i\kappa^{d_i}c_i,\qquad
 a_{ije}'=\sigma_i\sigma_j^e\kappa^{d_i-e}a_{ije}.
 \tag{2}
\]

The degrees are odd, so these are the exact transformed equations.
Negative exponents in (2) mean reciprocal rational powers. Their
absolute exponents are at most \(2N\), so all transformed coefficients
have polynomial bit length. Interval containment is preserved by the
sign changes and scaling. In the rest of the proof suppress primes,
and let \(U_i\) denote the positive transformed upper endpoints.
Define

\[
 A=3+\sum_iU_i+\sum_i|c_i|+\sum_{i,j,e}|a_{ije}|.
 \tag{3}
\]

Then \(1\leq\alpha_i\leq A\), every retained power is at most
\(A^N\), and the total absolute coefficient sum is at most \(A\).
Although \(A\) can be large, its logarithm has polynomial bit length.

Use variables \(X_{i,e}\), \(1\leq e\leq n_i\), and set

\[
 b_i(X)=c_i+\sum_{j<i}\sum_{e=1}^{n_j}a_{ije}X_{j,e}.
\]

There are exactly \(N\) residuals:

\[
 \begin{aligned}
 r_{i,j}&=X_{i,1}X_{i,j}-X_{i,j+1}
                  &&(1\leq j<n_i),\\
 r_{i,n_i}&=X_{i,n_i-1}X_{i,n_i}-b_i(X).
 \end{aligned}
 \tag{4}
\]

They have the unique real common zero
\(p=(\alpha_i^e)_{i,e}\): the chain gives powers of the first
coordinate, and the terminal equation gives its unique odd root.
Their quadratic parts have norm at most one. Their Jacobian at \(p\)
is block lower triangular with local determinant
\(d_i\alpha_i^{d_i-1}\). This follows by differentiating along the
power chain, or by eliminating its first \(n_i-1\) rows. Thus its
determinant has magnitude at least one. The bounds

\[
 V=4NA^N,\qquad \nu=V^{-(N-1)}
 \tag{5}
\]

give gradient norms at most \(V\) and
\(J^{\mathsf T}J\succeq\nu^2I\). All their logarithms have
polynomial length.

## An explicit exposing quadratic for one odd root

Temporarily fix a gate and write \(d=2n-1\), \(\alpha=\alpha_i\),
and \(X_j=X_{i,j}\), with \(X_0=1\). Define

\[
 \ell_j=X_{j+1}-\alpha X_j\quad(0\leq j<n).
\]

Let \(T_\alpha\) be the symmetric tridiagonal \(n\)-by-\(n\)
matrix

\[
 (T_\alpha)_{jj}=\alpha^{d-1-2j},\qquad
 (T_\alpha)_{j,j+1}=\tfrac12\alpha^{d-2-2j}.
 \tag{6}
\]

It equals \(D T_0D\), where
\(D=\operatorname{diag}(\alpha^{n-1-j})\) and \(T_0\) has
diagonal one and neighboring entries \(1/2\). The matrix \(T_0\) has
smallest eigenvalue \(1-\cos(\pi/(n+1))\geq1/(n+1)^2\).
Since \(\alpha\geq1\),
\(T_\alpha\succeq(N+1)^{-2}I\).

Put \(P_\alpha(X)=\ell^{\mathsf T}T_\alpha\ell\). On the power
curve \(X_j=t^j\),

\[
 P_\alpha(t,\ldots,t^n)
  =(t-\alpha)^2\sum_{h=0}^{d-1}\alpha^{d-1-h}t^h
  =(t-\alpha)(t^d-\alpha^d).
 \tag{7}
\]

In centered coordinates \(u_j=X_j-\alpha^j\), this is
\(u^{\mathsf T}H_i u\). The difference matrix has diagonal one
and lower diagonal \(-\alpha\); its inverse has norm at most
\(nA^{n-1}\). The following common bounds suffice:

\[
 h_0=\frac1{N^2(N+1)^2A^{2N}},\qquad
 L_0=8A^{2N+2},\qquad h_0I\preceq H_i\preceq L_0I.
 \tag{8}
\]

The upper bound follows from
\(\|T_\alpha\|\leq2A^{d-1}\) and the difference-matrix norm
at most \(1+A\).

Now restore the affine predecessor radicand and define

\[
 E_i^*(X)=P_{\alpha_i}(X_i)
               +(\alpha_i-X_{i,1})(b_i(X)-\alpha_i^{d_i}).
 \tag{9}
\]

At \(p\), this polynomial and its full gradient vanish. If
\(u=X-p\), its exact centered expression is

\[
 E_i^*(p+u)=u_i^{\mathsf T}H_i u_i
                 -u_{i,1}\sum_{j<i,e}a_{ije}u_{j,e}.
 \tag{10}
\]

Thus signed coefficients introduce only quadratic cross terms, not
uncontrolled linear terms.

## Rational combinations preserve the exact zero

Although (9) uses \(\alpha_i\), its rational approximation must
preserve zero exactly. Here is an explicit basis for doing so.
For local weighted degree \(h\), define the quadratic representative

\[
 m_h(X)=\begin{cases}
  1&h=0,\\
  X_h&1\leq h\leq n,\\
  X_nX_{h-n}&n<h\leq2n.
 \end{cases}
\]

For each ordinary monomial \(M\) of degree at most two in the local
variables, let \(w(M)\) be its power-curve degree and put
\(R_M=M-m_{w(M)}\). These are rational quadratics that vanish on
the whole power curve; zero relations may be omitted. Write

\[
 P_\alpha=\sum_M\beta_M(\alpha)M,
 \qquad
 S_i=X_{i,n_i}^2-b_iX_{i,1},\quad
 T_i=X_{i,n_i-1}X_{i,n_i}-b_i.
\]

Equation (7), compared coefficient by coefficient, gives the identity

\[
 E_i^*=S_i-\alpha_iT_i+
                 \sum_M\beta_M(\alpha_i)R_M.
 \tag{11}
\]

Each polynomial \(S_i,T_i,R_M\) is rational, of degree at most two,
and vanishes at \(p\). In particular, evaluating the coefficients
of (11) at a rational approximation to \(\alpha_i\) preserves its
zero exactly.

Expanding (6) shows that the sum of the absolute coefficients of all
univariate polynomials \(\beta_M\) is at most \(8n_i\), and their
degrees are at most \(2n_i\). For root error \(\theta\leq1\),
the total polynomial coefficient error in (11) is therefore at most
\(B_0\theta\), where

\[
 B_0=A+1+32N^2(A+1)^{2N}.
 \tag{12}
\]

Indeed the sum of derivative bounds for the \(\beta_M\) is at
most \(16N^2(A+1)^{2N}\); each \(R_M\) has coefficient norm at
most two; and \(T_i\) has coefficient norm at most \(A+1\).

## A positive quadratic part for the whole circuit

Define

\[
 \rho=\left(\frac{h_0}{2NA}\right)^2,
 \quad \omega_i=\rho^{i-1},
 \quad \gamma=\frac{h_0\rho^{k-1}}2,
 \quad W=kL_0+A+1.
 \tag{13}
\]

The exposing sum \(E^*=\sum_i\omega_i E_i^*\) has zero gradient
at \(p\). Scale the local centered coordinates by \(\sqrt{\omega_i}\).
Its diagonal blocks are \(H_i\succeq h_0I\). Every cross entry
has magnitude at most \(A\sqrt\rho/2\), since it joins an earlier
gate to a later one. Each row has at most \(N\) such entries, so
the cross-part norm is at most \(NA\sqrt\rho/2=h_0/4\).
Scaling back proves that its quadratic part satisfies

\[
                    H^*\succeq\gamma I,
                    \qquad \|H^*\|\leq W.
 \tag{14}
\]

The norm bound follows by summing the local bounds and the absolute
cross coefficients, using \(\omega_i\leq1\).

Let \(m=\gamma/2\) and \(L=W+1\). Choose a dyadic rational square
\(\varepsilon=t^2>0\) with

\[
 \varepsilon\leq
 \min\left\{1,\frac{m^2}{2N},
       \frac{\nu^2m^2}{36N(L+NV)^2}\right\}.
 \tag{15}
\]

Approximate every normalized root to error

\[
 \theta\leq\min\left\{1,
     \frac\gamma{4kB_0},
     \frac\varepsilon{4A^NkB_0}\right\}.
 \tag{16}
\]

Evaluate (11) at these rational approximations and form the weighted
sum \(G\). It is rational and \(G(p)=0\). Equations (12) and (16)
bound its coefficient error by \(kB_0\theta\). For a quadratic,
that bounds the norm of its quadratic-part error, while its gradient
error at \(p\) is at most \(2A^NkB_0\theta\). Therefore

\[
 G(p+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,
 \qquad mI\preceq H\preceq LI,
 \qquad\|\ell\|\leq\varepsilon.
 \tag{17}
\]

## Certified approximation and output complexity

The rational interval certificate makes root approximation explicit.
Maintain subintervals of the supplied boxes that contain the preceding
roots. Each retained power \(x^e\) on \([1,A]\) has derivative at
most \(eA^{e-1}\). Hence an affine radicand interval has width at
most \(C\) times the largest predecessor root-interval width, where
\(C=NA^N\). The certified radicand interval stays at least one.
The derivative of its odd root is at most one, so rounding each root
endpoint outward to accuracy \(\eta\) gives the width recurrence

\[
 D_i\leq C\max_{j<i}D_j+2\eta.
\]

Intersecting with the given gate box only improves the bound. To obtain
root error at most a specified dyadic \(2^{-P}\), take
\(\eta=2^{-P}/[4k(C+1)^k]\). Bisection of the increasing function
\(x^{d_i}\), using exact rational comparisons and the supplied box,
produces these endpoint intervals in polynomial time. The number of
bits is polynomial in the input length and \(P\). This includes the
precision required by (16). For an arbitrary rational requested
tolerance, its encoding length must also be counted.

Apply the
[reviewed quartic construction](general-strongly-convex-quartic-singleton.md)
and its [Hessian certificate](sos-convex-quartic-realization.md) to (4),
(5), and (17). The result is

\[
 F(X)=\left(\frac{G(X)}{t\nu}\right)^2+
                     \sum_{i,j}\left(\frac{r_{i,j}(X)}\nu\right)^2.
 \tag{18}
\]

Their estimates give \(\nabla^2F\succeq(3/2)I\). Its rational
SOS expression has \(N+1\) squares, and its zero is exactly \(p\).
Its degree is exactly four because \(H\succ0\).

For completeness, constructing the rational Hessian Gram does not
require the exponentially large common number field. Once the rational
quadratics in (18) are fixed, the centered Gram, translated back to
the uncentered normalized \(X\) variables, has entries of degree at most two in the
formal center coordinates. The reviewed Schur-complement proof gives
a positive rational lower bound \(\mu\) for its eigenvalues with
polynomially many bits. Here \(\|p\|\leq NA^N\). A rational bound
on the coefficient norms of these degree-two entries bounds their
derivatives, so polynomially many further center bits approximate the
Gram to Frobenius error less than \(\mu/4\). Root accuracy controls
all retained powers by the derivative bound
\(N(A+1)^N\). The exact rational coefficient projection from the
certificate note then preserves the Hessian identity and positive
definiteness. All steps use rational linear algebra in polynomial
dimension.

The logarithms of \(h_0^{-1},\rho^{-1},\gamma^{-1},V,\nu^{-1},
B_0\), and the required precision are polynomial in the input length.
The number of local power relations is at most quadratic in \(N\).
The dense quartic and its full Hessian Gram each have polynomially
many entries. Unary degree encoding is essential to this stated
output-size bound.

## Consequences, checks, and remaining limits

Exact affine comparison of the retained gate powers reduces to adding
that rational affine inequality to \(F\leq0\). The original input boxes can be imposed through the rational maps
\(\xi_i=\sigma_iX_{i,1}/\kappa\) if an explicit compact feasible
description is wanted.
No decision-complexity hardness follows from this reduction. Independent
prime cube-root gates already show that the joint field can have
exponential degree, so a dense common defining polynomial would be
an inappropriate intermediate representation.

The [reviewed optimizer baseline](signed-root-convex-optimizer-baseline.md)
already represents this circuit class as the unique optimizer of a compact
convex polynomial program, with an explicit polynomial-bit linear
objective. The result here adds the unique feasible zero, fixed quartic
degree, global curvature, and rational certificates.

The extension adds signed radicands with certified separation, odd
degrees, and affine access to predecessor powers. The previous theorem
automatically supplies the needed separation from its positive
coefficients; this theorem instead includes a verifiable certificate
in the input. It makes no claim that cancellation with an exponentially
small, uncertified radicand can be handled at polynomial cost. An
unsuccessful prior search would not establish novelty, and the new
circuit model still needs a scoped literature comparison.

The [targeted exact check](check_signed_odd_root_exposing.py) was run as

```text
python research-20260927/check_signed_odd_root_exposing.py
```

For degrees 3, 5, 7, 9, and 11 it passed the exposing identity (11),
the translated identity (10), the coefficient-norm bound, and the local
Jacobian determinant. Exact rational LDL checks at roots 1, 3/2, and
2 passed the proposed local spectral margins. These finite checks
support the algebra and indexing; they do not verify the general
spectral estimates, approximation algorithm, or bit-complexity claim.
No project-wide or CI checks were run. The independent review also
checked an exact coupled two-gate instance with negative and positive
original roots, degrees three and five, and signed predecessor terms.
