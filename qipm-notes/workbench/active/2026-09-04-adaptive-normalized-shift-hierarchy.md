# Near-linear adaptive lower bounds for unit-normalized spectral shifts

Status: Proved; independently audited; literature screen preliminary  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate on apparent novelty  

## Result

Fix \(\rho>1\) and an integer \(r\geq0\).  Define the nonnegative
approximation threshold

\[
 G_r(\rho)=
 \inf_{\substack{P\in\mathbb R[y]\\
                  \deg P\leq2r,\;P(y)\geq0\ \forall y\in\mathbb R}}
 \max_{1\leq y\leq\rho}|P(y)-y|.
                                                               \tag{1}
\]

Then \(G_r(\rho)>0\).  Consider the canonical scalar block-encoding oracle

\[
 U(t)=
 \begin{pmatrix}
 \sin t&\cos t\\
 \cos t&-\sin t
 \end{pmatrix},
 \qquad x=\sin t,
\]

and any coherent converter whose designated output block is \(q_\delta(x)\).
If it makes \(T_\delta\) oracle calls and

\[
 \sup_{x\in[\delta,\rho\delta]}
 |q_\delta(x)-(1-x)|\leq K\delta,
 \qquad K<G_r(\rho),
                                                               \tag{2}
\]

then

\[
 \boxed{
 T_\delta=
 \Omega_{r,\rho,K}\!\left(
 \delta^{-(2r+1)/(2r+2)}
 \right).}                                                     \tag{3}
\]

The circuit may use arbitrary ancillas, controlled calls, deferred
measurements, and coherent adaptivity.  Thus (3) is not restricted to a
single QSVT polynomial.  Free postselection or nonlinear conditioning is
outside the reusable-unitary output model.

## Proof

A matrix element of a \(T_\delta\)-query circuit is a trigonometric polynomial
of degree at most \(T_\delta\) in \(t\) (some query-count conventions insert
an immaterial factor two).  Put, as a function of the encoded scalar,

\[
 g_\delta(x)=1-\operatorname{Re}q_\delta(x).
\]

Because the output circuit is unitary for every canonical oracle,
\[
 0\leq g_\delta(x)\leq2
\]
for every \(x\in[-1,1]\), including outside the correctness promise.  On the
promised
interval, (2) gives

\[
 \left|\frac{g_\delta(\delta y)}{\delta}-y\right|
 \leq K,\qquad 1\leq y\leq\rho.                               \tag{4}
\]

The composition \(g_\delta(\sin t)\) is a bounded trigonometric polynomial.
Interior trigonometric Bernstein inequalities and the chain rule give, for
each fixed \(j\),

\[
 \left|\frac{d^j}{dx^j}g_\delta(x)\right|
 \leq C_j(T_\delta+1)^j,\qquad |x|\leq1/2.                    \tag{5}
\]

Taylor-expand through order \(2r+1\), rescale \(x=\delta y\), and divide by
\(\delta\).  This gives a polynomial \(P_\delta(y)\) of degree at most
\(2r+1\) such that, on every fixed compact set,

\[
 \frac{g_\delta(\delta y)}{\delta}
 =P_\delta(y)+
 O_r\!\left(T_\delta^{2r+2}\delta^{2r+1}\right).              \tag{6}
\]

If (3) failed, some sequence would satisfy
\[
 T_\delta=o\!\left(\delta^{-(2r+1)/(2r+2)}\right),
\]
so the remainder in (6) would vanish.  Equation (4) bounds
\(P_\delta\) at \(2r+2\) fixed points of \((1,\rho)\).  Finite-dimensional
norm equivalence therefore bounds all coefficients, and a subsequence
converges coefficientwise to a polynomial \(P\) of degree at most \(2r+1\).

For every fixed real \(y\), eventually \(\delta y\in[-1,1]\), so (6) and
nonnegativity of \(g_\delta\) give \(P(y)\geq0\).  Only the limiting
polynomial is asserted to be globally
nonnegative; the finite Taylor polynomials need not be.  A nonzero globally
nonnegative real polynomial cannot have odd degree, hence
\(\deg P\leq2r\).  Finally (4) yields
\[
 \max_{[1,\rho]}|P(y)-y|\leq K,
\]
contradicting (1).  This proves (3).

The strict positivity of \(G_r(\rho)\) is also compactness.  If it vanished,
a coefficientwise limit of bounded degree would equal \(y\) on
\([1,\rho]\), hence everywhere, contradicting global nonnegativity.  Moreover
\(G_r(\rho)\to0\): square increasingly accurate degree-\(r\) polynomial
approximants to \(\sqrt y\) on the fixed interval.

## Explicit thresholds

For \(r=0\),

\[
 G_0(\rho)=\frac{\rho-1}{2},
\]

and (3) recovers the general \(\Omega(\delta^{-1/2})\) edge bound.

For \(r=1\), let

\[
 m=\frac{\rho+1}{2},\qquad h=\frac{\rho-1}{2},\qquad
 s=\sqrt{m^2-\frac{h^2}{2}}.
\]

Then

\[
 \boxed{
 G_1(\rho)=
 \frac{\rho+1-\sqrt{(\rho^2+6\rho+1)/2}}{4},}                 \tag{7}
\]

attained by the globally nonnegative quadratic

\[
 P_*(y)=\frac{(y+s)^2}{2(m+s)}.
\]

Its error equioscillates at \(1,m,\rho\).  For completeness, a lower bound
follows by evaluating quadratic Lagrange interpolation at \(z=-a<0\).  The
three interpolation weights have signs \(+,-,+\) and total absolute value

\[
 S(a)=2\left(\frac{m+a}{h}\right)^2-1.
\]

If a globally nonnegative quadratic has uniform error \(E\), its value at
\(-a\) gives \(E\geq a/S(a)\).  Maximizing at \(a=s\) gives (7).

For \(\rho=2\),

\[
 G_1(2)=\frac{3-\sqrt{17/2}}4=0.021131\ldots.
\]

Therefore every arbitrary coherent converter with relative error constant
below \(0.021131\ldots\) needs \(\Omega(\delta^{-3/4})\) queries.  This is
consistent with the \(\delta/16\) square-root upper bound: \(1/16\) lies above
this adaptive threshold.

## Near-linear high-accuracy corollary

If the requested relative error vanishes,

\[
 \frac{\eta(\delta)}{\delta}\longrightarrow0,
\]

then for every fixed \(\varepsilon>0\), choose \(r\) with
\((2r+2)^{-1}<\varepsilon\).  Eventually
\(\eta(\delta)/\delta<G_r(\rho)\), and (3) yields

\[
 \boxed{
 T_\delta=\Omega_{\rho,\varepsilon}
 \bigl(\delta^{-1+\varepsilon}\bigr)
 \quad\text{for every }\varepsilon>0.}                       \tag{8}
\]

Thus high-relative-accuracy unit-normalized shifting has an almost linear
all-algorithms lower-bound exponent.  Pairwise unitary discrimination alone
cannot prove more than the square-root scale; (8) uses unitarity over a
continuum through the global nonnegativity constraint.

At exact error, no finite-query converter exists even for a fixed nontrivial
interval \([\delta,\rho\delta]\).  Equality there would make the analytic
function \(q(x)\) equal \(1-x\) throughout \((-1,1)\), contradicting
\(|q(x)|\leq1\) as \(x\to-1\).

## Novelty and scope

The polynomial method, Bernstein inequalities, nonnegative approximation,
and the pairwise block-encoding lower bound are standard ingredients.  The
fixed-QSVT approximation thresholds in the companion note are different and
larger because even parity is imposed there.  A preliminary targeted search
found no continuum nonnegative-Taylor hierarchy for arbitrary reusable
block-encoding converters.  The defensible apparent novelty is (1)--(8), not
the individual tools.  A deeper approximation-theory search is still needed
before a priority claim.
