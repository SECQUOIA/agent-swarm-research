# Facet-regular convex coupling cannot remove the box centrality tax

Status: Proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; priority not claimed

## Result

Let \(r\geq2\), \(K=(-1,1)^r\),

\[
 U(x)=-\sum_{i=1}^r\log(1-x_i^2),\qquad F=U+G,
 \tag{1}
\]

where \(G\in C^2(K)\) is convex and \(F\) is a standard
self-concordant barrier.  Suppose that, after permuting and changing signs
of coordinates if necessary, there are \(\delta\in(0,1)\) and finite
constants \(M,C\) such that on the full facet collar

\[
 \mathcal C_\delta=\{x\in K:x_1\geq1-\delta\}
 \tag{2}
\]

one has

\[
 \|\nabla G(x)\|_\infty\leq M,
 \qquad 0\preceq\nabla^2G(x)\preceq CI.
 \tag{3}
\]

Then the positive-objective central paths of \(F\) satisfy

\[
 \boxed{\displaystyle
 \sup_{w_i>0, s_0<s_1}
 {L_F(x_w|_{[s_0,s_1]})\over
   d_F(x_w(s_0),x_w(s_1))}
 \ \geq\ \Gamma_r,}
 \qquad
 \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2.
 \tag{4}
\]

Thus the ratio is at least \(\Theta(\sqrt{\log r})\).  The conclusion is
independent of the barrier parameter of \(F\).  It applies, in particular,
to every convex coupling whose gradient and Hessian are bounded on the
whole cube.

Within the class \(F=U+G\) with convex \(G\), eliminating this growing
worst-case tax therefore requires \(G\) to be derivative-singular on every
full signed facet collar: if even one collar satisfies (3), (4) follows.
This is a necessary condition, not a sufficient construction of a
tax-free barrier.

## 1. The path enters and stays in the regular collar

Put

\[
 u(t)=-\log(1-t^2),\qquad
 \alpha_i=\sqrt i-\sqrt{i-1},\qquad
 w_i(T)=e^{T\alpha_i}.
 \tag{5}
\]

Let \(x_T(s)\) be the central path

\[
 \nabla F(x_T(s))=z(s):=e^s w(T),\qquad s\leq0.
 \tag{6}
\]

Convexity of \(G\) and the collar bound imply, for fixed \(x_{-1}\),

\[
 x_1\leq1-\delta
 \quad\Longrightarrow\quad
 \partial_1G(x_1,x_{-1})
 \leq\partial_1G(1-\delta,x_{-1})\leq M.
 \tag{7}
\]

Choose \(Z>M+u'(1-\delta)\).  Stationarity in coordinate one gives

\[
 u'(x_{T,1})=z_1-\partial_1G(x_T).
 \tag{8}
\]

Consequently \(z_1\geq Z\) forces \(x_{T,1}>1-\delta\); otherwise
(7)--(8) would give \(u'(x_{T,1})>u'(1-\delta)\).  Since \(z_1(s)\) is
increasing, the path stays in \(\mathcal C_\delta\) after the activation
time

\[
 \tau_1=\log Z-T\alpha_1.
 \tag{9}
\]

This entry argument is why a full facet collar suffices.  No global bound
on \(G\) is needed away from the collar.

## 2. Central-arc lower bound

On the collar write

\[
 D=\nabla^2U(x_T(s)),\qquad H=\nabla^2F(x_T(s)).
\]

Differentiating (6) gives \(H\dot x_T=z\), hence

\[
 \|\dot x_T\|_{F,x_T}^2=z^TH^{-1}z.
 \tag{10}
\]

For a coordinate subset \(A\), restrict the variational formula for the
inverse quadratic form to vectors supported on \(A\).  Equations (3) and
inverse Loewner order give

\[
 z^TH^{-1}z
 \geq z_A^TH_{AA}^{-1}z_A
 \geq\sum_{i\in A}{z_i^2\over u''(x_{T,i})+C}.
 \tag{11}
\]

Within the collar, stationarity and (3) say

\[
 u'(x_{T,i})=z_i-(\nabla G(x_T))_i,
 \qquad |(\nabla G(x_T))_i|\leq M.
 \tag{12}
\]

Because

\[
 {u'(t)^2\over u''(t)}={2t^2\over1+t^2}\longrightarrow1
 \quad(t\uparrow1),
 \tag{13}
\]

after increasing the fixed \(Z\), for every prescribed
\(\varepsilon>0\),

\[
 z_i\geq Z
 \quad\Longrightarrow\quad
 {z_i^2\over u''(x_{T,i})+C}\geq1-\varepsilon.
 \tag{14}
\]

The activation times \(\tau_i=\log Z-T\alpha_i\) obey
\(\tau_1<\cdots<\tau_r<0\) for large \(T\).  Since the entire interval
\([\tau_1,0]\) lies in the collar, (10)--(14) apply on every successive
prefix interval.  Integration and summation by parts yield

\[
\begin{aligned}
 L_F(x_T|_{(-\infty,0]})
 &\geq\sqrt{1-\varepsilon}\left[
 \sum_{j=1}^{r-1}\sqrt j\,T(\alpha_j-\alpha_{j+1})
 +\sqrt r(T\alpha_r-\log Z)\right]\\
 &=\sqrt{1-\varepsilon}
   \left[T\Gamma_r^2-\sqrt r\log Z\right].
 \tag{15}
\end{aligned}
\]

## 3. Endpoint distance in the actual coupled metric

Let

\[
 \rho(t)=\int_0^t\sqrt{u''(a)}\,da,
 \qquad y_{T,i}=\rho(x_{T,i}(0)).
 \tag{16}
\]

At \(s=0\), the endpoint is in the collar and (12) applies.  The
standard interval endpoint asymptotic gives

\[
 y_{T,i}=T\alpha_i+O_{r,M}(1),
 \qquad \|y_T\|_2=T\Gamma_r+O_{r,M}(1).
 \tag{17}
\]

The strict convexity supplied by \(U\) gives \(F\) a unique analytic center
\(x_*\).  Fix any \(p\in\mathcal C_\delta\) with \(p_1=1-\delta/2\).
There is a fixed compact interior curve from \(x_*\) to \(p\), whose
\(F\)-length is a finite constant independent of \(T\).

Join \(p\) to \(x_T(0)\) by the coordinatewise \(U\)-geodesic

\[
 \rho(\gamma_i(q))=(1-q)\rho(p_i)+q y_{T,i},
 \qquad 0\leq q\leq1.
 \tag{18}
\]

For large \(T\), the first coordinate is monotone from
\(p_1>1-\delta\) to \(x_{T,1}(0)>p_1\), so this curve stays in the collar.
Its \(U\)-length is

\[
 \|y_T-\rho(p)\|_2=T\Gamma_r+O_{r,M,p}(1).
 \tag{19}
\]

Each coordinate of (18) is monotone.  Hence its Euclidean total variation
is at most \(2r\), and (3) gives

\[
 L_G(\gamma)
 :=\int_0^1\sqrt{\dot\gamma^T\nabla^2G(\gamma)\dot\gamma}\,dq
 \leq2r\sqrt C.
 \tag{20}
\]

Using \(\sqrt{a+b}\leq\sqrt a+\sqrt b\), the fixed entry curve and
(19)--(20) prove

\[
 d_F(x_*,x_T(0))\leq T\Gamma_r+O_{r,M,C,p,F}(1).
 \tag{21}
\]

Divide (15) by (21), send \(T\to\infty\), and then
\(\varepsilon\downarrow0\).  This proves (4).  The analytic-center start
is the limit \(s_0\to-\infty\); finite starts approximate the same ratio.

## 4. Why an almost-vertex neighborhood alone is not enough

The weaker condition that (3) hold only when
\(x_1,\ldots,x_{r-1}\) are all near \(1\), with \(x_r\) in a fixed compact
interval, does not support the preceding conclusion.  The logarithmic
growth in (15) is accumulated over the full flag

\[
 \{x_1=1\}\supset\{x_1=x_2=1\}\supset\cdots
 \supset\{x_1=\cdots=x_r=1\}.
 \tag{22}
\]

During the interval contributing the \(j\)-th prefix term, only the first
\(j\) coordinates are close to their endpoints.  A bound confined to the
last proper face controls only the final prefix interval, whose
contribution is \(O(T)\), not the harmonic sum
\(T\Gamma_r^2=\Theta(T\log r)\).  Thus a proof from only that local
hypothesis would need a different mechanism.  No all-barrier conclusion is
claimed here.

## Scope and novelty boundary

This is a continuous central-arc versus exact same-endpoint Hessian-distance
theorem.  It is not a distance-to-objective-accuracy, discrete-round,
finite-bit, or query lower bound.  The decomposition \(F=U+G\), convexity
of \(G\), and the full-collar derivative bounds are substantive hypotheses.
They do not cover an arbitrary \(O(r)\)-parameter barrier on the cube.

The candidate contribution is the stability principle: even a nonseparable
convex coupling cannot change the sharp asymptotic tax if it remains
second-order regular on one full facet collar.  No priority claim is made
without a dedicated literature search.

## Audit targets

1. Check the collar-entry implication (7)--(9), including dependence on
   the other coordinates.
2. Check that all staged activation intervals remain in the collar and
   that (11)--(15) retain the exact \(\Gamma_r\) constant.
3. Check analytic-center existence and the fixed entry path in Section 3.
4. Verify that the comparison path remains in the collar and that (20)
   bounds the added metric in the actual \(F\) geometry.
5. Check the scope distinction between a full facet collar and only an
   almost-vertex neighborhood.

## Independent hostile audit record

**PASS.**  For fixed transverse coordinates, convexity makes
\(\partial_1G\) nondecreasing in \(x_1\).  The derivative bound at the
collar entrance therefore proves (7), and stationarity forces entry whenever
\(z_1\geq Z\).  This is a pointwise implication, so increasing \(z_1(s)\)
keeps every later central point in the collar; no monotonicity of
\(x_{T,1}(s)\) was assumed.

Once inside, the collar bounds apply to every gradient component and the
entire Hessian.  Restricting the inverse-quadratic variational formula to an
active prefix proves the first inequality in (11), and inverse Loewner order
proves the second.  Bounded gradient perturbation plus
\(u'^2/u''\to1\) makes (14) uniform.  All staged prefix intervals start
after the first collar-entry time, and summation by parts gives exactly
\(T\Gamma_r^2-\sqrt r\log Z\).

The bounded-domain barrier has a unique analytic center because \(U\) is
strictly convex and supplies boundary blow-up.  A fixed interior entry curve
has finite fixed length.  For large \(T\), the chosen point \(p\) precedes
the terminal point in the first scalar metric coordinate, so the comparison
geodesic remains in the full collar.  Its \(U\)-length is the Euclidean
\(\rho\)-coordinate chord, while coordinatewise monotonicity limits ordinary
total variation to \(2r\); hence (20)--(21) are bounds in the actual
\(F\)-metric.

The theorem genuinely needs regularity on a full facet collar for this
proof.  An almost-vertex neighborhood misses the earlier prefix intervals
that generate the harmonic sum.  The statement correctly remains a
same-endpoint continuous theorem for barriers explicitly decomposed as
\(F=U+G\), not an all-barrier, accuracy-set, discrete-round, finite-bit, or
query lower bound.
