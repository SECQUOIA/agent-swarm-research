# Gaussian separable mixed closure without a conditioned factor

Date: 2026-10-02. Status: complete proof that passed
[independent review](../reviews/anisotropic-gaussian-separable-closure-review.md).
No priority claim is made.

An exactly rational row rotation and diagonal scaling can normalize the
supplied concave factor without changing the separable convex residual.
The price is diagonal, rather than scalar, auxiliary curvature. A grid
balanced by that curvature keeps small singular values out of the
expected cell count: they affect only bit precision and the refinement
cutoff.

## 1. Model and conclusion

Use the product domains and explicit convex univariate piecewise quadratic
functions of the reviewed
[separable mixed theorem](smoothed-mixed-separable-closure.md). In particular,
every interval endpoint, listed breakpoint, and polynomial coefficient is
rational; integer intervals have binary-encoded endpoints. First round
integer endpoints inward, reject empty domains, and eliminate fixed
coordinates, absorbing their affine and constant contributions into the
residual. If no variables remain, solve the instance directly. The full-row-rank
promise below is on the supplied factor after this scalar-domain preprocessing.
Consider

\[
 F(x)=\sum_{j=1}^n\phi_j(x_j)-\frac\alpha2\|Tx\|^2,
 \qquad \alpha>0,
 \quad T\in\mathbb Q^{k\times n}\text{ of full row rank}.
                                                               \tag{1}
\]

For \(k=0\), the objective separates and is solved directly; below
\(k\ge1\). The number of integer coordinates is unrestricted. The supplied factor
need not satisfy a norm or smallest-singular-value bound. Write

\[
 \beta=\alpha\|T\|_2^2
\]

for the curvature of this supplied concave term. It is not the negative
curvature of the full objective. The row number \(k\) is retained:
this note does not remove dependent rows or identify a minimum-rank
representation of the objective.

For any rational noise scale \(\sigma>0\), the algorithm constructs a
finite scalar rational Gaussian-like law before sampling and independently
perturbs every original linear coefficient with that law. It returns the
exact optimum and a rational optimizer of the sampled objective on every
draw, with expected bit work

\[
 f\!\left(k,1+\frac{\beta\operatorname{diam}(X)}\sigma\right)
 \operatorname{poly}(I),                                \tag{2}
\]

where the polynomial exponent is absolute and \(I\) is the original
rational input length, including \(\sigma\). There is no integer-dimension
parameter. The scalar recourse, critical-region closure, and exact fallback
are those of the separable theorem. The probability argument extends the
[Gaussian cell-count theorem](smoothed-gaussian-cell-closure.md).

## 2. Exact rational row normalization

Set \(\Gamma=TT^T\succ0\). Let \(H\ge\|\Gamma\|_2\) be a
positive rational row-sum bound. If \(D_0\) clears all denominators
of \(\Gamma\), then

\[
 \mu=D_0^{-k}H^{-(k-1)}\le\lambda_{\min}(\Gamma).
\]

This follows from the nonzero integer determinant of \(D_0\Gamma\)
and the upper bound \(H\) on the other eigenvalues. The logarithms of
\(H,\mu\) have polynomial input length. The rational orthogonal
Jacobi construction in the
[normalization note](spectral-normalization.md), with operator-norm residual
target \(\mu/64\) and per-entry threshold \(\mu/(64k)\), computes in polynomial bit time an exactly orthogonal
rational \(Q\) with

\[
 Q\Gamma Q^T=\operatorname{diag}(a_1,\ldots,a_k)+E,
 \qquad E_{ii}=0,\quad\|E\|_2\le\mu/64.
\]

Every \(a_i\) is a Rayleigh quotient and satisfies
\(\mu\le a_i\le\|\Gamma\|_2\). Choose a dyadic positive
number \(d_i\) with

\[
 2a_i\le d_i^2<8a_i.
\]

Consecutive squared powers of two differ by four, so rational comparisons
find such a number in polynomial bit time, including when it is below 1.
Define

\[
 D=\operatorname{diag}(d_i),\qquad
 U=D^{-1}QT,\qquad L=\operatorname{diag}(L_i),
 \quad L_i=\alpha d_i^2>0.
\]

The transformed frame obeys

\[
 \frac1{16}I_k\preceq UU^T\preceq I_k,
 \qquad L_{\max}<8\beta.                               \tag{3}
\]

Indeed the diagonal of \(D^{-1}\operatorname{diag}(a_i)D^{-1}\)
lies in \((1/8,1/2]\), while
\(\|D^{-1}ED^{-1}\|\le(\mu/64)/(2\mu)=1/128\).
Also \(d_i^2<8a_i\le8\|T\|^2\). Most importantly,

\[
 \alpha\|Tx\|^2=(Ux)^TL(Ux)                            \tag{4}
\]

holds exactly because \(Q\) is exactly orthogonal. The small Jacobi
residual is not discarded or added to the convex residual. Consequently
every \(\phi_j\) stays unchanged and separability is preserved.
All transformed data have polynomial encoding length. Small singular
values determine the requested Jacobi accuracy through its logarithm;
they are not numerical parameters in (2).

## 3. Anisotropic recourse and curvature-balanced grids

Let \(u_j\) denote column \(j\) of \(U\). Decompose an ambient
perturbation using

\[
 A_U=(UU^T)^{-1}U,\quad d=A_U\gamma,\quad
 r=(I-U^TA_U)\gamma,
 \qquad\gamma=U^Td+r.
\]

The auxiliary value is

\[
 \begin{aligned}
 W_r(a)&=\min_{x\in X}[F(x)+r^Tx+\tfrac12(a-Ux)^TL(a-Ux)]\\
 &=\tfrac12a^TLa+
 \sum_j\min_{x_j\in X_j}
       [\phi_j(x_j)-(u_j^TLa-r_j)x_j],
 \qquad V(a)=W_r(a)+d^Ta.
 \end{aligned}                                         \tag{5}
\]

Thus precisely the existing scalar difference/derivative tests apply,
with changed linear tilts. They return exact values, witnesses, and global
critical regions. Square completion gives

\[
 V(a)=\min_{x\in X}[F(x)+\gamma^Tx+
  \tfrac12(a-Ux+L^{-1}d)^TL(a-Ux+L^{-1}d)]
       -\tfrac12d^TL^{-1}d.                             \tag{6}
\]

An auxiliary optimizer lies in the coordinate range of \(UX-L^{-1}d\).
An inner witness transfers its auxiliary gap to the original problem
without increasing it, exactly as in scalar-curvature closure.

Choose dyadic positive mesh scales \(\rho_i\) with

\[
 1\le L_i\rho_i^2<4.                                   \tag{7}
\]

For a fixed auxiliary box with coordinate widths \(w_i>0\), put
\(S=\max_i w_i/\rho_i\), \(h_j=S2^{-j}\). In coordinate \(i\),
use the least power-of-two number of equal subdivisions that makes the
actual step \(h_{ij}\le\rho_i h_j\). These grids are nested,
have at most \(2^j\) subdivisions per coordinate, and each refined
coordinate satisfies

\[
 \rho_i h_j/2<h_{ij}\le\rho_i h_j.
\]

Unrefined coordinates have only their two endpoints. Every cell's
corrected-corner error is

\[
 B_j=\frac18\sum_iL_i h_{ij}^2\le\frac k2h_j^2.          \tag{8}
\]

For local neighboring comparisons at an interior grid coordinate,
coordinate curvature \(L_i\) gives an allowed factor-noise interval
of length at most

\[
 L_i h_{ij}+4B_j/h_{ij}\le C_kL_i h_{ij},
 \qquad C_k=1+8k.                                      \tag{9}
\]

The last inequality uses \(L_i h_{ij}^2>h_j^2/4\).
Unrefined coordinates require no interval estimate. This is where an
unbalanced isotropic mesh would incorrectly introduce curvature ratios.

## 4. Gaussian weighted local counts

Every attaining witness at \(v\) gives the global upper model

\[
 W_r(v+z)\le W_r(v)+(L(v-Ux_v))^Tz+\tfrac12z^TLz.
                                                               \tag{10}
\]

Let \([\ell_i,u_i]\) be the coordinate range of \(UX\), computed
from product-box endpoints. Combining the local neighboring comparisons
with (10) places each allowed coefficient in

\[
 L_i[\ell_i-v_i,u_i-v_i]
      +[-C_kL_i h_{ij}/2,C_kL_i h_{ij}/2].               \tag{11}
\]

For the Gaussian proxy \(\gamma\sim N(0,\sigma^2I_n)\), factor
noise \(d\) and residual noise \(r\) are independent. The factor
covariance is \(\sigma^2(UU^T)^{-1}\), with eigenvalues between
\(\sigma^2\) and \(16\sigma^2\). The Gaussian density majorant
and capped weighted lattice sum apply coordinatewise with spacing
\(\Delta_i=L_i h_{ij}\), core width \(L_i(u_i-\ell_i)\),
and frame constant \(c=1/16\). The proof of that majorant works
for every \(c\in(0,1]\), not just the \(c\ge1/2\) used in the
earlier statement. It yields, on every level and every fixed auxiliary box,

\[
 \sum_v\Pr(E_v)\le H_L,
 \qquad H_L=\prod_i\left[
 2+4(2C_k+4)+\frac{C_kL_i(u_i-\ell_i)}{\sigma\sqrt{2\pi}}
 \right].                                               \tag{12}
\]

No auxiliary-box width or ratio \(L_{\max}/L_{\min}\) occurs.
Since \(\|U\|\le1\), each original projection width is at most
\(\operatorname{diam}(X)\). Equations (3) and (12) give the numerical
parameter dependence in (2). The count does not require smoothness of the
mixed envelope.

## 5. Exact closure and rare unresolved cells

Keep the separable theorem's state count \(R\), hyperplane count
\(K=R(2n+1)\), exact fallback multiplier \(B\), and scalar-section
bound

\[
 C_{\rm sec}=[2(2k+1)R+1](8k+2).
\]

They are unchanged by the tilts in (5), and their logarithms have
polynomial input length. For any selected continuous free states,

\[
 H_J=L-\sum_{j\in\mathcal F_J}
          \frac{(Lu_j)(Lu_j)^T}{p_{j,J}},\qquad
 \nabla q_J(a;r)=L(a-Ux_J(a,r)).                         \tag{13}
\]

This algebraic identity remains valid at lower-dimensional regions and
ties. If \(r_j^+\) is the largest reciprocal of a positive listed
continuous curvature, with zero when no such curvature occurs, set

\[
 H_0=L_{\max}+\sum_{j\text{ continuous}}r_j^+\|Lu_j\|^2.
\]

It is a rational upper bound for \(\|H_J\|\), independent of all
sampled coefficients. Exact cell containment and quadratic minimization
on its \(3^k\) faces work unchanged on the resulting rectangular cells.

For every active witness, (10) and minimization of its upper quadratic give

\[
 g^TL^{-1}g\le2[V(v)-\min V],\qquad
 g=L(v-Ux_v)+d.
\]

A retained unresolved cell has a corner with gap at most \(2B_j\).
Thus

\[
 \|g\|\le\sqrt{2kL_{\max}}\,h_j,
 \qquad\operatorname{diam}(\text{cell})
 \le h_j\sum_i\rho_i.
\]

The existing facet-image argument for an invertible \(H_J\), or the
proper gradient image for a singular \(H_J\), therefore places the
noise in a tube about one of \(K\) fixed ambient hyperplanes. A safe
rational tube coefficient is

\[
 C_{\rm tube}=k(1+L_{\max})+H_0\sum_i\rho_i,
 \qquad\tau_j=C_{\rm tube}h_j.                         \tag{14}
\]

The pulled-back normal has norm at least one because its factor normal
\(u\), normalized to length one, and ambient normal \(v\) satisfy
\(Uv=u\). The Hessians and region normals are fixed, and their offsets
are affine in residual noise, as required for fixed ambient hyperplanes.
Under the Gaussian proxy one tube has probability at most
\(\tau_j/\sigma\). Under independent scalar laws with Kolmogorov
error \(\delta\), it has probability at most
\(\tau_j/\sigma+2n\delta\).

Tiny \(L_i\) can enlarge \(\rho_i\) and (14). These quantities
have polynomial bit length and enter the cutoff only through logarithms.
They do not enter (12).

## 6. One fixed rational product law and expected bit work

For trial support multiplier \(R_s=2^t\), take the fixed auxiliary box

\[
 A_{R_s}=\prod_i[\ell_i-s_i,u_i+s_i],\qquad
 s_i=\frac{R_s\sigma\|(A_U)_{i,:}\|_1}{L_i}.
\]

This contains an auxiliary optimizer for every ambient draw with
\(\|\gamma\|_\infty\le R_s\sigma\). Form its scaled largest
width \(S=\max_i(u_i-\ell_i+2s_i)/\rho_i\), and choose the
least \(J\ge0\) satisfying

\[
 S2^{-J}\le\frac{\sigma}{4KB C_{\rm tube}}.
\]

Put \(Q_{\rm all}=(J+1)(2^J+1)^k\). Choose the least positive
integer accuracy \(b\) with

\[
 2^b\ge\max\{8nKB,\ 2nC_{\rm sec}Q_{\rm all}\}.
\]

Increase \(t\) from zero until \(2^t\ge b+20\), then fix these
budgets and use the Gaussian theorem's bounded polynomial-time rational
sampler independently in every original coordinate at accuracy \(b\)
and scale \(\sigma\). Its support is inside
\([-\sigma(b+20),\sigma(b+20)]\).

This loop is noncircular: \(S(t)\le2^tS(0)\), while
\(C_{\rm tube}\) is support-independent, so
\(J(t)\le J(0)+t\). The required \(b\) grows only linearly
in \(kt\), up to logarithms and polynomial base-input terms. The
successful \(t,J,b\) are polynomially bounded in the original input
length. Normalization increased that length only polynomially. The scalar
sampler operates on radius \(b+20\), not on an exponentially enumerated
support. All draws occur after the budgets are fixed.

The uniform scalar-section argument and product-law replacement give
local-event discrepancy at most \(2nC_{\rm sec}2^{-b}\) per
deterministic node. Summing all grids through \(J\) gives expected
local-event count at most \((J+1)H_L+1\). Corner incidence, child
counts, exact recourse, and local quadratic closure therefore cost
\(C_0^k(1+H_L)\operatorname{poly}(I)\) in expectation.

At level \(J\), the probability of any retained unresolved cell is at
most

\[
 K C_{\rm tube}S2^{-J}/\sigma+2nK2^{-b}\le1/(2B).
\]

The separable theorem's exact same-draw fallback costs
\(B\operatorname{poly}(I+b)\); its expected contribution is polynomial.
Every sampled atom is solved correctly, including ties, because closure
and fallback are deterministic exact certificates. This proves (2).

## 7. Scope and verification

The new result removes only the numerical conditioning assumption on a
supplied full-row-rank factor. It preserves the supplied separable convex
residual exactly. It does not claim that arbitrary nonconvex piecewise
quadratics admit such a decomposition, or that \(k\) and \(\beta\)
are intrinsic negative-inertia parameters of the final objective.
Dependent-row elimination is not included.

As before, the target is the perturbed objective under the specifically
constructed independent finite Gaussian-like law. The argument does not
give exact-real Gaussian input to a Turing machine or cover every coarse
Gaussian approximation. No growth or uniqueness condition is required.

The parent researcher independently read the complete proof and found no
substantive gap. The
[fresh independent review](../reviews/anisotropic-gaussian-separable-closure-review.md)
also passed; a separate reader approved its normalization, mesh, and
bit-complexity claims.

The targeted command

```sh
python research-20261002/new-direction/check_anisotropic_gaussian.py
```

passed four exact normalization fixtures with four rational Jacobi
rotations, including a badly conditioned oblique factor; the largest
frame entry used 280 bits. It checked exact frame inequalities, the
operator-norm residual bound, and preservation of the full quadratic
penalty. It also checked 120 anisotropic grid levels, 169 interior-coordinate
interval bounds, and 91 inactive-coordinate cases, including a 200-bit
curvature ratio. The diagnostic uses small-matrix principal minors solely
for verification, not as the polynomial normalization algorithm. It is
not a general solver implementation or an empirical expectation bound.
No project-wide checks or CI inspection were performed.
