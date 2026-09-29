# Compressing the cyclic construction to (n+1) integer squares

Date: 2026-09-28. Status: the rational identity, precision choice, and
cyclic quantitative bounds were independently checked. This note reviews
a refinement proposed after the verified
[cyclic construction](cyclic-quartic-exponential-degree.md). The original
\(n+2\)-square construction remains valid independently of this refinement.
The full refinement is stated in
[One fewer rational square](cyclic-quartic-square-compression.md).
That note has an additional independent review and exact output checks;
the alternative precision recipe below checks the same identity and
coefficient bounds from a different rational bisection construction.

## A rational square root after choosing the regularization parameter

Let \(g\in\mathbb Q^m\setminus\{0\}\), put
\(R=g^{\mathsf T}g\), and choose a rational
\(r\) with \(0<r<\sqrt R\). Define

\[
 t=\frac{R-r^2}{2r},\qquad
 s=\frac{R+r^2}{2r},\qquad
 L=tI+\frac{r}{R}gg^{\mathsf T}.
\]

These are rational, \(t>0\), \(s-t=r\), and \(s+t=R/r\).
Since \((gg^{\mathsf T})^2=Rgg^{\mathsf T}\), direct multiplication
gives

\[
 L^2=t^2I+
      \frac{2tr+r^2}{R}gg^{\mathsf T}
    =t^2I+gg^{\mathsf T}.
\]

The eigenvalue of \(L\) along \(g\) is \(s\); all orthogonal
directions have eigenvalue \(t\). In particular, \(L\) is positive
definite. For any vector of rational quadratic polynomials \(q\),

\[
              (g^{\mathsf T}q)^2+t^2\sum_iq_i^2
                         =\sum_i(Lq)_i^2.                 \tag{1}
\]

The parameter \(t\) is chosen with this identity. It would be incorrect
to claim that every previously fixed rational \(t>0\) allows the same
rational matrix square root: \(R+t^2\) need not be a rational square.

## Choosing (t) in the required range

Use the cyclic construction's rounded weights \(g_i=z_i/Q\), with
\(m=n+1\), \(M=10^6n^5\), and \(Q=32mM^2\). Its bounds imply
\(1/8<g_i<5\), so \(1/8<\sqrt R<5m\).

Compute a rational approximation \(u\) to \(\sqrt R\) with
\(|u-\sqrt R|\le1/(16M)\), and put

\[
                         r=u-\frac5{4M}.
\]

Rational bisection on \([0,5m]\) uses \(O(\log(mM))\) steps.
Each comparison is between rational squares and \(R\). Thus its
numerators and denominators have polynomial magnitude in \(n\), not
merely polynomial bit length.

For \(\delta=\sqrt R-r\),

\[
 \frac{19}{16M}\le\delta\le\frac{21}{16M},\qquad
 r\ge\frac1{16}>0,
\]

where the second inequality uses \(M\ge32\). Moreover,

\[
 t=\delta\left(1+\frac{\delta}{2r}\right),\qquad
                         \frac1M\le t\le\frac2M.
\]

For the upper bound, \(\delta/(2r)\le8\delta\le21/(2M)\),
so \(t\le(21/16)(1+21/64)/M<2/M\). The lower bound follows from
\(t\ge\delta>1/M\).

## The curvature and certificate estimates survive

Keep the same rounded exposing quadratic \(G=g^{\mathsf T}q\).
Replace the previous parameter \(M^{-2}\) by
\(\varepsilon'=t^2\in[M^{-2},4M^{-2}]\). The previously established
gradient error obeys
\(\|\ell\|\le1/(4M^2)\le\varepsilon'/4\); the matrix bounds
on \(G\) are unchanged.

With \(\mu=1/(16n^2)\), \(\nu=1/(8n)\),
\(L=9\), and \(D_0=L+8m\le17n\), the required inequalities are

\[
 \varepsilon'\le1,\qquad
 \varepsilon'\le\frac{\mu^2}{2m},\qquad
 \varepsilon'\le\frac{\nu^2\mu^2}{36nD_0^2}.
\]

All hold even at \(\varepsilon'=4/M^2\). For example the last
right-hand side is at least \(1/(170459136n^9)\), whereas
\(4/M^2=4/(10^{12}n^{10})\). The constants leave ample slack for
every \(n\ge2\). The complete strong-convexity and rational positive
definite Hessian Gram proofs therefore apply unchanged to
\(\Phi'=G^2+t^2\sum_iq_i^2\). Equation (1) expresses this polynomial
as exactly \(m=n+1\) rational quadratic squares.

## Explicit common denominator and integer output

Write \(r=a/b\) with positive integers \(a,b\), and put
\(S=\sum_i z_i^2\), so \(R=S/Q^2\). An explicit common
denominator is

\[
                        D=2abQ^2S.
\]

The integer matrix \(P=DL\) has entries

\[
 P_{ij}=S(Sb^2-a^2Q^2)\,\mathbf1_{i=j}
                         +2a^2Q^2z_i z_j.                \tag{2}
\]

Since \(2q_i\) has integer coefficients, every polynomial
\(2(Pq)_i\) is an integer quadratic, and

\[
                    F'=\sum_{i=1}^{m}[2(Pq)_i]^2
                                      =4D^2\Phi'.         \tag{3}
\]

All of \(a,b,Q,S,D\) have polynomial magnitude in \(n\). Thus the
coefficients of the integer square factors have \(O(\log(n+1))\)
bits. Every factor lies in the span of the same \(O(n)\) monomials
appearing in the residuals, so the union of their square supports has
\(O(n^2)\) monomials. Summing polynomially many terms preserves the
coefficient-bit bound.

The unscaled curvature lower bound is
\((3/2)t^2\nu^2\). Consequently (3) has Hessian at least
\(3D^2/(32M^2n^2)\) times the identity. The explicit denominator
satisfies \(D\ge2Q^2\), so this quantity exceeds one for the chosen
parameters. The field degree, exact zero, and rational Hessian certificate
are preserved. Rational translation of a coordinate preserves the number
of integer squares as well.

## Scope

This is an exact rational factorization, not numerical square-root
rounding. It reduces the displayed square count by selecting a nearby
regularization parameter before applying the existing curvature proof.
It does not by itself prove that \(n+1\) squares are necessary. Any
minimality theorem needs its own argument, especially when a quartic has
flat directions in its leading homogeneous part.

The rank-one identity and denominator formula were checked algebraically.
Their role in the cyclic estimates was checked separately from the original
\(n+2\)-square proof. The main refinement's more general bisection of
\(R-r^2-3\tau r\) was also checked: the derivative lower bound gives
the stated \(4\Delta\) endpoint margin for the exact center root,
and a \(\Delta/2\)-accurate rational midpoint stays in the allowed
interval.

A targeted `python -` check using `fractions.Fraction` also verified the
complete matrix identity for rational examples of sizes \(1,2,3,5\);
all passed. These examples support the arithmetic and do not replace the
general proof. The same targeted command checked this file's local links,
delimiters, final newline, and trailing whitespace. No project-wide checks,
CI inspection, or Lean formalization of this refinement are claimed.
