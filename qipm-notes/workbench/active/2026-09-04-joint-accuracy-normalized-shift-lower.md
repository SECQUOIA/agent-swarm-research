# Joint accuracy--gap lower bounds for unit-normalized shifts

Status: Proved; independently audited; targeted local literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the analytic inequality; moderate on novelty  

## Problem and notation

Fix \(\rho>1\) and \(0<\delta\leq1/(2\rho)\).  A coherent converter receives
controlled access to the
canonical scalar block encoding

\[
 U(t)=\begin{pmatrix}\sin t&\cos t\\ \cos t&-\sin t\end{pmatrix},
 \qquad x=\sin t,
\]

and makes \(T\) controlled queries to \(U(t)\) or its adjoint, interleaved
with arbitrary \(t\)-independent unitaries on any finite ancilla space.  Its
final circuit is a unitary, as required for a reusable block encoding.  Its
designated scalar
output block on this periodic oracle family is denoted by \(Q(t)\), and on
the principal branch put \(q(x)=Q(\arcsin x)\).  Unitarity gives
\(|Q(t)|\leq1\) for every real \(t\), whether or not \(\sin t\) is in the
correctness promise.  Suppose

\[
 \sup_{x\in[\delta,\rho\delta]}
 |q(x)-(1-x)|\leq K\delta.                                  \tag{1}
\]

Here \(K=K(\delta)\geq0\) may vanish jointly with \(\delta\).  The upper spectral
band is unnecessary for the lower bound.

As in the adaptive-hierarchy note, define

\[
 G_r(\rho)=
 \inf_{\substack{P\in\mathbb R[y],\ \deg P\leq2r\\
                  P(y)\geq0\ \forall y\in\mathbb R}}
 \max_{1\leq y\leq\rho}|P(y)-y|.                            \tag{2}
\]

The point of this note is to make the dependence on \(r\) explicit enough
to let \(r\) grow with \(\delta\).

## The uniform Fejer--Riesz jet inequality

### Theorem 1

There are constants \(c_\rho,C_\rho>0\) with the following property.  Let
\(r\geq1\), put \(s=r+1\), and assume

\[
 K<G_r(\rho),\qquad r\leq c_\rho\delta^{-1/2}.               \tag{3}
\]

Every converter satisfying (1) obeys

\[
 \boxed{
 T\geq c_\rho s\,
       \bigl(G_r(\rho)-K\bigr)^{1/s}
       \delta^{-1+1/(2s)}.}                                 \tag{4}
\]

Constants can be made numerical; their exact values are not important for
the joint asymptotics below.  Unlike the earlier compactness proof, (4) is a
single finite-\(\delta\) inequality with explicit \(r\)-dependence.

### Proof

Put

\[
 h(t)=1-\operatorname{Re}Q(t).
\]

A \(T\)-query circuit has matrix entries that are Laurent polynomials of
degree at most \(T\) in \(e^{it}\).  Thus \(h\) is a real trigonometric
polynomial of degree at most \(T\).  Also \(0\leq h\leq2\), since
\(|Q|\leq1\).  Fejer--Riesz factorization gives a polynomial \(A(z)\) of
degree at most \(T\) such that

\[
 h(t)=|A(e^{it})|^2,
 \qquad \max_{|z|=1}|A(z)|\leq\sqrt2.                       \tag{5}
\]

Define the analytic function

\[
 a(x)=A(e^{i\arcsin x}),\qquad |x|<1.
\]

Let \(B_r\) be its Taylor polynomial of degree \(r\) at zero.  Then

\[
 P_r(y)=\frac{|B_r(\delta y)|^2}{\delta}                    \tag{6}
\]

is a real polynomial of degree at most \(2r\) and is nonnegative for every
real \(y\).

We next bound the Taylor error uniformly in \(r\).  For \(|z|=R\leq1/4\),
the positive-coefficient series for \(\arcsin\) gives
\(|\operatorname{Im}\arcsin z|\leq2R\).  Bernstein--Walsh for the degree-
\(T\) polynomial \(A\), together with (5), therefore gives

\[
 |a(z)|\leq\sqrt2 e^{2TR}.                                  \tag{7}
\]

If \(T\rho\delta\geq s/8\), then already
\(T\geq s/(8\rho\delta)\), which is stronger than (4) after decreasing
\(c_\rho\).  Otherwise choose \(R=s/(4T)\).  The restriction in (3),
together with the following elementary two-point bound, lets us assume
\(s\leq T\), hence \(R\leq1/4\).  Namely, at the two endpoints (5) and (9)
give

\[
 |A(e^{i\arcsin(\rho\delta)})|
 -|A(e^{i\arcsin\delta})|
 \geq
 \{\sqrt{\rho-K}-\sqrt{1+K}\}\sqrt\delta.
\]

Because \(K<G_r(\rho)\leq G_1(\rho)<(\rho-1)/2\), the coefficient on the
right is bounded below by a positive constant depending only on \(\rho\).
Bernstein's inequality for \(A(e^{it})\), (5), and
\(\arcsin(\rho\delta)-\arcsin\delta=O_\rho(\delta)\) therefore imply
\(T\geq d_\rho\delta^{-1/2}\).  Taking \(c_\rho<d_\rho/2\) proves
\(s\leq T\) under (3).  Cauchy's coefficient estimate and a geometric tail
now yield, for \(1\leq y\leq\rho\),

\[
 e_r:=|a(\delta y)-B_r(\delta y)|
 \leq2\sqrt2
 \left(4\sqrt e\,\frac{T\rho\delta}{s}\right)^s.           \tag{8}
\]

On the promised interval, (1) implies

\[
 \left|\frac{|a(\delta y)|^2}{\delta}-y\right|\leq K,
 \qquad |a(\delta y)|\leq\sqrt{(\rho+K)\delta}.             \tag{9}
\]

Writing \(u=e_r/\sqrt\delta\), equations (6)--(9) give

\[
 \max_{[1,\rho]}|P_r(y)-y|
 \leq K+2\sqrt{\rho+K}\,u+u^2.                             \tag{10}
\]

Since \(P_r\) is globally nonnegative, (2) and (10) imply

\[
 u\geq
 \sqrt{\rho+G_r(\rho)}-\sqrt{\rho+K}
 \geq C_\rho\bigl(G_r(\rho)-K\bigr).                       \tag{11}
\]

Combining (8) and (11) and taking an \(s\)-th root proves (4).
\(\square\)

## An explicit threshold lower bound

Put

\[
 R_\rho=\frac{\sqrt\rho+1}{\sqrt\rho-1}>1.
\]

The exact Chebyshev formula in the staircase note implies the following
useful bound for every \(r\geq1\):

\[
 \boxed{
 G_r(\rho)\geq
 \frac{\sqrt\rho}{2er}R_\rho^{-2r}.}                       \tag{12}
\]

Indeed, write \(z_0=\cosh a\), where \(a=\log R_\rho\), in

\[
 G_r(\rho)=\frac{\rho-1}{2}
 \max_{z\geq z_0}\frac{z-z_0}{T_{2r}(z)}.
\]

Evaluate at \(z=\cosh(a+1/(2r))\).  Convexity gives
\(z-z_0\geq\sinh(a)/(2r)\), while
\(T_{2r}(z)=\cosh(2ra+1)\leq e^{2ra+1}\).  Finally
\((\rho-1)\sinh(a)/2=\sqrt\rho\), proving (12).

Combining (4) and (12) gives a clean two-parameter family.

### Corollary 2 (implicit joint law)

There are constants \(b_\rho,\delta_\rho>0\) such that, for every
\(0<\delta\leq\delta_\rho\) and every integer \(r\geq1\) satisfying

\[
 K\leq \frac{\sqrt\rho}{4er}R_\rho^{-2r},                  \tag{13}
\]

one has

\[
 \boxed{
 T\geq b_\rho r\,\delta^{-1+1/(2r+2)}.}                   \tag{14}
\]

The restriction on \(r\) in Theorem 1 is unnecessary here.  Indeed, if
\(T<s=r+1\), use the fixed Cauchy radius \(R=1/4\) in place of the radius in
(8).  For sufficiently small \(\delta\), uniformly for \(y\in[1,\rho]\),

\[
 e_r\leq2\sqrt2 e^{T/2}(4\rho\delta)^s
      \leq2\sqrt2 e^{s/2}(4\rho\delta)^s.                 \tag{15}
\]

On the other hand, (11)--(13) require

\[
 e_r\geq c_\rho\sqrt\delta\,r^{-1}R_\rho^{-2r}.
\]

The ratio of the upper bound to this lower bound is at most
\(C_\rho r\delta^{r+1/2}(4\rho\sqrt e\,R_\rho^2)^r\), which is less than
one simultaneously for every \(r\geq1\) once
\(\delta\leq\delta_\rho\).  Thus \(T<s\) is impossible.  If \(T\geq s\),
the proof of Theorem 1 applies without its auxiliary restriction on \(r\).
This proves (14) for every \(r\geq1\).

Thus a completely explicit joint lower bound is

\[
 T\geq b_\rho
 \max_{\substack{r\geq1\\
 K\leq \sqrt\rho R_\rho^{-2r}/(4er)}}
 r\,\delta^{-1+1/(2r+2)}.                                  \tag{16}
\]

To see the factor \(r\) in (14), retain the \(s\) factor in (4).
Equation (12) contributes
only the constant factor \(R_\rho^{-2r/(r+1)}\geq R_\rho^{-2}\) after the
\(s\)-th root.

## Joint-vanishing accuracy regimes

Let

\[
 L=\log(1/\delta),\qquad M=\log(1/K).
\]

Whenever \(M\to\infty\), condition (13) permits, up to additive
\(O_\rho(\log M)\),

\[
 r\simeq\frac{M}{2\log R_\rho}.
\]

Consequently (16) gives the useful heuristic form, made rigorous by taking
the largest integer satisfying (13),

\[
 T=\Omega_\rho\!\left(
 \frac{M}{\delta}
 \exp\!\left[-\frac{\log R_\rho\,L}{M-O_\rho(\log M)}\right]
 \right).                                                   \tag{17}
\]

A slightly less sharp but conventionally quantified version is often more
convenient: there are constants \(c_\rho,C_\rho,M_\rho>0\) such that, whenever
\(M\geq M_\rho\),

\[
 \boxed{
 T\geq c_\rho\frac{M}{\delta}
       \exp(-C_\rho L/M).}
\]

To prove it, take \(r=\lfloor\theta_\rho M\rfloor\), with
\(\theta_\rho>0\) small enough that \(2\theta_\rho\log R_\rho<1/2\).
For all sufficiently large \(M\), the remaining \(\log r\) term in (13)
is at most \(M/2\), so this \(r\) is admissible in (16).

Two consequences are especially clean.

1. If \(K=\delta^\beta\) for fixed \(\beta>0\), choose
   \(r=(\beta L-O_\rho(\log L))/(2\log R_\rho)\).  Then

   \[
    \boxed{T=\Omega_{\rho,\beta}(\delta^{-1}\log(1/\delta)).} \tag{18}
   \]

   Generic uniform singular-value amplification gives
   \(O(\delta^{-1}\log(1/(K\delta)))\), so (18) matches its order in this
   polynomial-accuracy regime.

2. More generally, if \(M/L\to\infty\), with no upper restriction on
   \(M\), the exponential factor in (17) tends to one:

   \[
    \boxed{T=\Omega_\rho(\delta^{-1}\log(1/K)).}             \tag{19}
   \]

   This again matches the precision-dependent part of the generic
   \(O(\delta^{-1}[L+M])\) amplification upper bound.

In fact the same comparison is tight throughout the whole high-accuracy
region: for every fixed \(\beta_0>0\), if \(M\geq\beta_0L\), then (17) gives

\[
 T=\Omega_{\rho,\beta_0}(\delta^{-1}M)
  =\Omega_{\rho,\beta_0}(\delta^{-1}[L+M]),                 \tag{20}
\]

which matches the generic upper bound.  Thus the joint query complexity is
settled up to constants whenever the relative error is at most a fixed
positive power of the spectral gap.

### Corollary 3 (tight high-accuracy complexity)

Let \(Q_{\rm comp}(\delta,\varepsilon)\) be the worst-case query complexity
of converting a plain normalized block encoding of any positive contraction

\[
 \delta I\preceq H\preceq I
\]

into a reusable unit-normalized block encoding of \(I-H\) with operator-norm
error at most \(\varepsilon\).  Fix \(\beta_0>0\).  Uniformly for
\(0<\varepsilon\leq\delta^{1+\beta_0}\),

\[
 \boxed{
 Q_{\rm comp}(\delta,\varepsilon)
 =\Theta_{\beta_0}\!\left(
   \delta^{-1}\log(1/\varepsilon)\right).}                 \tag{21}
\]

For the lower bound, restrict to the canonical scalar family with
\(x\in[\delta,\rho\delta]\), for any fixed \(\rho>1\), and set
\(K=\varepsilon/\delta\).  If \(E=\log(1/\varepsilon)\), then
\(M=E-L\geq\beta_0L\), so (20) is
\(\Omega_{\rho,\beta_0}(\delta^{-1}E)\).  This lower bound covers arbitrary
coherent converters.  The reverse inequality is the standard uniform
singular-value-amplification construction applied to the initial
two-normalized linear-combination encoding of \(I-H\).

For \(M=o(L)\), (17) is weaker by the factor
\(\exp[-\Theta_\rho(L/M)]\).  Determining whether that factor is inherent or
an artifact of the boundary-layer hierarchy remains open.

## Consequence for QIPM block-encoding pipelines

Suppose a sparse QIPM constructs a Newton or scaling operator through a
plain normalized block encoding of a positive contraction \(H\), and a later
stage needs a reusable unit-normalized encoding of \(I-H\).  If admissible
instances include an uncertain spectral interval
\([\delta,\rho\delta]\), and the required relative shift error obeys
\(K\leq\delta^{\beta_0}\), then even a fully coherent adaptive converter has
query cost

\[
 \Omega_{\rho,\beta_0}(\delta^{-1}\log(1/\delta)).
\]

This cost is dimension-independent and therefore survives sparsity.  It does
not apply when the lower cluster is known to consist of finitely many exact
eigenvalues, where low-degree interpolation can evade the interval lower
bound, or when the access model directly supplies the normalized complement.

## Scope and caveats

1. The lower bound applies to arbitrary coherent reusable block-encoding
   converters in the canonical plain-oracle family, not only fixed QSVT
   polynomials.  Deferred measurements and coherent adaptivity remain
   covered.  Free postselection is not a reusable unitary block encoding.
2. Theorem 1 permits an arbitrarily small margin \(G_r-K\), at the cost of
   the stated restriction on \(r\).  Corollary 2 removes that restriction
   under the explicit half-threshold condition (13), which is sufficient for
   all joint asymptotic consequences above.
3. The \(r\)-uniform Fejer--Riesz/Cauchy argument is the new ingredient over
   the compactness hierarchy.  Fejer--Riesz factorization, Bernstein--Walsh,
   Chebyshev exterior extremality, and QSVT query polynomials are classical or
   standard ingredients individually.
4. A targeted local search found no joint \((K,\delta)\) lower law of the
   form (16)--(19).  The closest local results are the fixed-\(K\) staircase
   and the endpoint-window constructions of
   [Orsucci--Dunjko](https://arxiv.org/abs/2101.11868).  The generic matching
   amplification upper bound is from
   [Gilyen--Su--Low--Wiebe](https://arxiv.org/abs/1806.01838).  Neither source
   states a joint arbitrary-converter lower bound.  A broader
   approximation-theory literature screen is still required before claiming
   priority.
5. The \(\delta^{-1}\log(1/\varepsilon)\) scaling in Corollary 3 resembles
   the classical optimal scaling of fixed-point amplitude amplification.  It
   should not be advertised as a new precision law in isolation.  The
   potentially new content is its derivation for unit-normalized complement
   conversion, the arbitrary-completion/coherent-converter access statement,
   and its embedding in the full joint threshold law (16).
