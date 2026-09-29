# One fewer rational square in the cyclic quartic construction

Date: 2026-09-28. Status: proof written by the root investigator and
checked in an [independent review](cyclic-quartic-rank-one-compression-review.md).
This supplements the verified
[cyclic quartic family](cyclic-quartic-exponential-degree.md).
The original construction remains valid.

The cyclic family can use \(n+1\) integer quadratic squares instead
of \(n+2\), while preserving its field degree, short coefficients,
global strong convexity, and rational positive definite Hessian Gram
certificate. The adjustment changes the small rational regularization
coefficient before taking a rational matrix square root. It does not
claim that an arbitrary rational positive definite matrix has a
rational square root.

## A rational rank-one square root

Let \(g\in\mathbb Q^m\) be nonzero and put \(R=g^{\mathsf T}g\).
Choose a positive rational \(r<\sqrt R\), and define

\[
 t=\frac{R-r^2}{2r},\qquad
 s=\frac{R+r^2}{2r},\qquad
 L=tI+\frac{gg^{\mathsf T}}{s+t}
   =tI+\frac rRgg^{\mathsf T}.
 \tag{1}
\]

Then \(t>0\), \(s^2=t^2+R\), and direct multiplication proves

\[
                         L^2=t^2I+gg^{\mathsf T}.
 \tag{2}
\]

Indeed the coefficient of \(gg^{\mathsf T}\) is
\((2tr+r^2)/R=1\). All entries of \(L\) are rational.
Its eigenvalues are \(t\) on \(g^\perp\) and \(s\) on
\(\mathbb Rg\). For any vector of rational polynomials \(q\),

\[
 (g^{\mathsf T}q)^2+t^2\sum_iq_i^2
                              =\sum_i(Lq)_i^2.
 \tag{3}
\]

The formulas are elementary rational parametrization and a rank-one
matrix identity. The contribution here is their compatible use in the
quartic construction, not a new matrix-square-root principle.

## Choosing the regularization size without irrational arithmetic

For any positive rational \(\tau\), a rational \(r\) with
\(t\in[\tau,2\tau]\) can be found with polynomial bit complexity
in the encoding of \(R,\tau\). The function

\[
 r(t)=\sqrt{R+t^2}-t
\]

is strictly decreasing and satisfies
\[
 |r'(t)|=\frac{R}{\sqrt{R+t^2}(\sqrt{R+t^2}+t)}
              \ge\frac{R}{2(R+4\tau^2)}
 \quad(\tau\le t\le2\tau).
\]

The point corresponding to \(t=3\tau/2\) is the unique positive
root of the rational quadratic
\[
                         R-r^2-3\tau r=0.
\]

Use exact rational bisection between zero and the integer
\(U=\lceil R\rceil+1\). Stop with interval width at most
\[
                    \Delta=\frac{R\tau}{16(R+4\tau^2)}.
\]

The midpoint is within \(\Delta/2\) of that root. By the derivative
bound, the exact root has distance at least \(4\Delta\) from either
endpoint of the interval corresponding to \([\tau,2\tau]\).
Thus the midpoint remains at least \(7\Delta/2\) from either
endpoint and gives the desired \(r\). An exact rational
root encountered during bisection can be used immediately.
All sign tests are rational quadratic evaluations.

For the cyclic data, \(R\) has polynomial magnitude and a common
denominator of polynomial magnitude, and \(\tau=1/M\), with
\(M=10^6n^5\). Here \(R\) is also bounded below by a positive
inverse polynomial. The bisection uses \(O(\log(n+1))\) steps
and gives \(r=a/b\) with positive integers \(a,b\) of polynomial
magnitude. No degree-\(d_n\) algebraic computation occurs.

## Applying the identity to the cyclic quadratics

Retain the main construction's \(m=n+1\) quadratics \(q_i\),
integer weights \(z_i\), and
\[
 M=10^6n^5,\qquad Q=32mM^2,\qquad
                g_i=z_i/Q,\qquad G=g^{\mathsf T}q.
\]

The weight approximation still gives, at the prescribed zero \(p\),
\[
 G(p+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,\quad
 \|\ell\|\le\frac1{4M^2},\quad
 H\succeq\mu I,\quad \|H\|\le9,
 \quad\mu=\frac1{16n^2}.
\]

The residual Jacobian has smallest singular value at least
\(\nu=1/(8n)\), every quadratic part has norm at most one,
and every residual gradient has norm at most eight.
Choose \(r\) by the preceding procedure with \(\tau=1/M\),
and let \(\varepsilon=t^2\). Then
\[
 \frac1{M^2}\le\varepsilon\le\frac4{M^2},
                        \qquad \|\ell\|\le\varepsilon/4.
\]

All previously used Gram and curvature inequalities remain valid.
In detail, \(D=9+8m\le17n\) and it suffices that
\[
 \varepsilon\le
 \min\left\{1,\frac{\mu^2}{2m},
          \frac{\nu^2\mu^2}{36nD^2}\right\}.
\]
The last right-hand side is at least
\(1/(170459136n^9)\); even \(4/M^2=4/(10^{12}n^{10})\)
is smaller for every \(n\ge2\). The other two inequalities
also follow directly. Consequently
\[
 \Phi=G^2+t^2\sum_iq_i^2=\sum_i(Lq)_i^2,\qquad
              \nabla^2\Phi\succeq\frac32t^2\nu^2I.
 \tag{4}
\]

The Gram Schur complement keeps the same positive lower estimate,
so the original rational Hessian-certificate construction still
applies. Its required precision remains polynomial.

For explicit integer output, put \(S=\sum_i z_i^2>0\).
Since \(R=S/Q^2\) and \(r=a/b\), equation (1) becomes
\[
 L=tI+\frac{a}{bS}zz^{\mathsf T},\qquad
 t=\frac{Sb^2-Q^2a^2}{2abQ^2}.
\]

The integer \(D_0=2abQ^2S\) clears all entries of \(L\).
The quadratics \(q_i\) have denominators at most two, so
\[
 D=32MnD_0,\qquad
                         \widetilde F_n=\sum_{i=0}^{m-1}(D(Lq)_i)^2
 \tag{5}
\]
is a sum of exactly \(m=n+1\) integer quadratic squares.
The scaling clears those remaining halves, and (4) gives
\(\nabla^2\widetilde F_n\succeq I\).
Indeed \(D\ge32Mn\) and \(t\ge1/M\), so the lower bound
is at least \(24I\).

Every integer appearing in (5) has polynomial magnitude in \(n\).
Thus its square factors have \(O(\log(n+1))\) coefficient bits.
Although their expanded individual supports may be larger, equality
with \(D^2(G^2+t^2\sum_iq_i^2)\) shows that the resulting quartic
still has only \(O(n^2)\) monomials, with the same coefficient-bit
order. It can be expanded through that expression to avoid redundant
intermediate products.

The zero set remains the original singleton, because \(t>0\)
and (3) vanishes exactly when all \(q_i\) vanish. The joint field
degree, first-coordinate degree, local conditioning order, and
translated ordinary sparse-output obstruction therefore remain
unchanged. Scaling preserves the positive definite rational Hessian
Gram certificate.

This note does not itself establish a lower bound on the number of
squares. A separate topological argument is under review. Optimality
of \(n+1\) squares must be linked to that result only after its
assumptions and proof have been checked.
