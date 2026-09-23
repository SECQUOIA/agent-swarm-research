# A joint gap--accuracy law for unit-normalized spectral shifts

Status: Proved; independently audited twice; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate-to-high on apparent novelty  

## Result

Fix \(\rho>1\) and \(c\in(0,1]\).  There are constants
\(\delta_0(\rho),K_0(\rho)>0\).  Let
\(0<\delta<\min\{c/\rho,\delta_0\}\) and \(0<K<K_0\), where \(K\) may depend on
\(\delta\).  A reusable
unit-normalized converter must output a block approximating \(I-H\) to
absolute error \(K\delta\) whenever

\[
 \operatorname{spec}(H)\subseteq
 [\delta,\rho\delta]\cup[c,1].                              \tag{1}
\]

For every integer \(n\geq2\), define the exterior threshold

\[
 H_n(\rho)=h\max_{z\geq z_0}\frac{z-z_0}{T_n(z)},
 \qquad
 h=\frac{\rho-1}{2},\qquad z_0=\frac{\rho+1}{\rho-1}.       \tag{2}
\]

Let \(n=n(K)\) be the largest odd integer for which
\(H_n(\rho)\geq8K\).  For all sufficiently small \(K\), this is well
defined: \(T_{n+1}(z)>T_n(z)\) for \(z>1\), so \(H_n\) strictly
decreases to zero.  Moreover,

\[
 n(K)=\frac{\log(1/K)-\log\log(1/K)+O_\rho(1)}
 {\log R_0},
 \qquad
 R_0=\frac{\sqrt\rho+1}{\sqrt\rho-1}.                       \tag{3}
\]

The quantum query complexity satisfies the quantitative lower and upper
bounds

\[
 \boxed{
 \Omega_\rho\!\left(
 n K^{1/(n+1)}\delta^{-n/(n+1)}
 \right)
 \leq Q_{\rm shift}(\delta,K)
 \leq
 O\!\left(\delta^{-1}\log\frac1{K\delta}\right).}          \tag{4}
\]

Because \(K^{1/(n+1)}=\Theta_\rho(1)\), the lower bound can also be
written

\[
 Q_{\rm shift}
 =\Omega_\rho\!\left(
 \delta^{-1}\log\frac1K\,
 \exp\!\left[-\Theta_\rho\!\left(
 \frac{\log(1/\delta)}{\log(1/K)}\right)\right]
 \right).                                                   \tag{5}
\]

In the polynomially accurate and higher-accuracy regime, (4) closes:
for every fixed \(\beta>0\), uniformly over \(0<K\leq\delta^\beta\),

\[
 \boxed{
 Q_{\rm shift}(\delta,K)
 =\Theta_{\rho,\beta}\!\left(
 \frac1\delta\log\frac1K\right).}                         \tag{6}
\]

The lower bound uses only the low continuum \([\delta,\rho\delta]\), so
the fixed high band in (1) is irrelevant to the impossibility result.  The
upper construction is accurate on the larger interval \([\delta,1]\).

### Operational block-encoding corollary

Let \(Q_{\rm comp}(\delta,\epsilon)\) be the worst-case number of queries
needed to convert a plain normalized block encoding of an arbitrary positive
contraction

\[
 \delta I\preceq H\preceq I
\]

into a reusable unit-normalized block encoding of \(I-H\) with norm error
\(\epsilon\).  For every fixed \(\beta_0>0\), uniformly when
\(0<\epsilon\leq\delta^{1+\beta_0}\), (6) gives

\[
 \boxed{
 Q_{\rm comp}(\delta,\epsilon)
 =\Theta_{\beta_0}\!\left(
 \frac1\delta\log\frac1\epsilon\right).}                  \tag{6a}
\]

For the lower bound, restrict to the canonical scalar family on
\([\delta,\rho\delta]\) and set \(K=\epsilon/\delta\).  If
\(E=\log(1/\epsilon)\) and \(D=\log(1/\delta)\), then
\(\log(1/K)=E-D\geq\beta_0D\), so (6) is
\(\Omega_{\beta_0}(\delta^{-1}E)\).  The upper bound follows either from
the integrated-sign polynomial below or by exactly block encoding
\((I-H)/2\) with LCU and applying standard uniform singular-value
amplification across its \(\Theta(\delta)\) headroom.

## Exterior-threshold asymptotic

Writing \(z_0=\cosh a_0\), with \(a_0=\log R_0\), and setting
\(z=\cosh(a_0+s/n)\) gives

\[
 H_n(\rho)=
 \frac{2\sqrt\rho}{e\,n}R_0^{-n}
 \left(1+O_\rho(n^{-1})\right).                             \tag{7}
\]

The maximizing \(s\) is \(1+O_\rho(1/n)\).  Equation (3) and the fact
that \(K^{1/(n+1)}\) stays between positive \(\rho\)-dependent constants
follow at once.  Restricting to odd indices changes \(n\) by at most two,
and maximality gives \(H_{n+2}<8K\).

## Quantitative all-circuit lower bound

It suffices to use the canonical scalar oracle

\[
 U(t)=\begin{pmatrix}\sin t&\cos t\\
 \cos t&-\sin t\end{pmatrix}.
\]

Let \(Q_{\rm out}(t)\) be a designated matrix element of a \(Q\)-query
coherent converter on this canonical oracle and put

\[
 F(t)=1-\operatorname{Re}Q_{\rm out}(t).
\]

Then \(F\) is a real trigonometric polynomial of degree at most \(C_0Q\)
for a convention-dependent absolute constant \(C_0\), and unitarity gives
\(0\leq F\leq2\) for every real \(t\).  Correctness on the low band gives

\[
 |F(\arcsin(\delta y))-\delta y|\leq K\delta,
 \qquad 1\leq y\leq\rho.                                  \tag{8}
\]

The global output need not be a function of \(\sin t\) alone, because an
arbitrary converter may inspect the completion carrying \(\cos t\).  The
proof uses the periodic function \(Q_{\rm out}(t)\) globally and invokes the
block-encoding contract only on the principal-branch points in (8).

Use the affine local coordinate that maps the promised interval exactly:

\[
 t_1=\arcsin\delta,\qquad t_\rho=\arcsin(\rho\delta),
 \qquad b_\delta=\frac{t_\rho-t_1}{\rho-1},
 \qquad a_\delta=t_1-b_\delta,                             \tag{9}
\]

so \(t=a_\delta+b_\delta y\) maps \([1,\rho]\) onto
\([t_1,t_\rho]\).  The ratio \(\arcsin x/x\) is strictly increasing,
which gives \(b_\delta>t_1>\delta\) and \(a_\delta<0\), while
\(b_\delta=\delta(1+O_\rho(\delta^2))\).  Retain the sine
target, rather than replacing it by its linear term, because \(K\) may be
much smaller than \(\delta^2\).  Let

\[
 P_n(y)=\frac1\delta\sum_{j=0}^n
 \frac{F^{(j)}(a_\delta)}{j!}(b_\delta y)^j,
 \qquad
 S_{n,\delta}(y)=\frac1\delta\sum_{j=0}^n
 \frac{\sin^{(j)}(a_\delta)}{j!}(b_\delta y)^j.             \tag{10}
\]

The trigonometric Bernstein inequality
\(\|F^{(j)}\|_\infty\leq(C_0Q)^j\|F\|_\infty\) and Taylor's theorem
show, with the fixed choice \(A=\rho+1\), that

\[
 |F(a_\delta+b_\delta y)/\delta-P_n(y)|
 \leq
 u_Q:=\frac{2(C_\rho C_0AQ)^{n+1}\delta^n}{(n+1)!},        \tag{11}
\]

and

\[
 |\sin(a_\delta+b_\delta y)/\delta-S_{n,\delta}(y)|
 \leq
 u_s:=\frac{(C_\rho A)^{n+1}\delta^n}{(n+1)!}.            \tag{12}
\]

Here \(b_\delta\leq C_\rho\delta\), and the fixed
\(\rho\)-dependent factor is kept inside the growing power.  For
\(t=a_\delta+b_\delta y\), the encoded value \(\sin t\) ranges exactly
over \([\delta,\rho\delta]\).  Thus (8), reparameterized by this affine
coordinate, and the two Taylor bounds give

\[
 \|P_n-S_{n,\delta}\|_{[1,\rho]}
 \leq K+u_Q+u_s.                                           \tag{13}
\]

Let \(a_n=h(z_n-z_0)\) correspond to a maximizer in (2).  The hyperbolic
form in the proof of (7) gives \(a_n=\Theta_\rho(1/n)\), so it lies in the
fixed interval used above.  Nonnegativity of
\(F(a_\delta-b_\delta a_n)\) gives

\[
 P_n(-a_n)\geq-u_Q.                                        \tag{14}
\]

There is also an exact useful sign.  Put
\(f(y)=\arcsin(\delta y)\).  For \(0<a_n\leq1\), monotonicity of
\(f(y)/y\) on the positive half-line gives

\[
 \frac{f(1)-f(-a_n)}{1+a_n}\leq f(1)
 <\frac{f(\rho)-f(1)}{\rho-1}=b_\delta.
\]

Thus the secant through \(1,\rho\), extended to \(-a_n\), lies below
the graph even though \(f\) changes convexity at zero:

\[
 a_\delta-b_\delta a_n\leq-\arcsin(\delta a_n).
\]

For small \(\delta\) both sides lie in \((-\pi/2,0)\), so
\(\sin(a_\delta-b_\delta a_n)/\delta\leq-a_n\).  Taylor's
remainder hence gives

\[
 S_{n,\delta}(-a_n)\leq-a_n+u_s.                           \tag{15}
\]

Apply exterior Chebyshev extremality to the degree-\(n\) polynomial
\(P_n-S_{n,\delta}\).  Equations (13)--(15) imply

\[
 H_n(\rho)\leq K+2u_Q+2u_s.                                \tag{16}
\]

For the chosen \(n\), the left side is at least \(8K\).  To make the
remaining uniformity explicit, maximality and the lower half of (7) give

\[
 K>\frac18H_{n+2}
 \geq c_\rho(n+2)^{-1}R_0^{-(n+2)}.
\]

Consequently

\[
 \frac{u_s}{K}
 \leq C_\rho n\,
 \frac{(C_\rho A R_0\delta)^n}{(n+1)!}=o(1),               \tag{16a}
\]

uniformly over growing \(n=n(K)\) once \(\delta<\delta_0(\rho)\).
Consequently \(u_Q=\Omega(K)\), and solving (11) for \(Q\), then using
Stirling's inequality, proves

\[
 Q=\Omega_\rho\!\left(
 nK^{1/(n+1)}\delta^{-n/(n+1)}
 \right).                                                   \tag{17}
\]

This argument applies to arbitrary coherent converters, including controlled
queries, ancillas, and coherent adaptivity.  It does not apply to free
postselection or another nonlinear output model.

## Contractive upper bound by integrating a sign approximant

Set \(\epsilon=2K\delta<1/2\) and use the standard bounded
sign-approximation lemma: there is an odd real polynomial \(s\) of degree

\[
 d=O\!\left(\delta^{-1}\log(1/\epsilon)\right)             \tag{18}
\]

such that \(|s(x)|\leq1\) on \([-1,1]\) and
\(|s(x)-\operatorname{sign}(x)|\leq\epsilon\) for
\(|x|\geq\delta\).  Define

\[
 p(x)=\int_{-1}^x\frac{1+s(t)}2\,dt,
 \qquad q(x)=1-p(x).                                       \tag{19}
\]

Oddness gives \(p(1)=1\), while \(0\leq p'(x)\leq1\).
Therefore \(0\leq p,q\leq1\) on all of \([-1,1]\): (19) is already
unit-normalized, with no rescaling loss.  For every \(x\geq\delta\),

\[
 q(x)-(1-x)
 =\frac12\int_x^1(s(t)-1)\,dt,
 \qquad
 |q(x)-(1-x)|\leq\epsilon/2.                               \tag{20}
\]

This proves the upper half of (4).  The polynomial
has mixed parity, but generalized QSP implements it at unit normalization
with \(O(d)\) controlled walk calls by the centered Laurent construction in
the companion staircase note.

## Matched polynomial-accuracy regime

Put \(D=\log(1/\delta)\) and \(L=\log(1/K)\).  From (3),
\(n=\Theta_\rho(L)\), and

\[
 \delta^{-n/(n+1)}
 =\delta^{-1}\exp[-D/(n+1)].                               \tag{21}
\]

If \(K\leq\delta^\beta\), then \(L\geq\beta D\), so the exponential
factor in (21) is bounded below by a positive constant depending only on
\(\rho,\beta\).  The lower bound is therefore
\(\Omega_{\rho,\beta}(\delta^{-1}L)\).  Conversely,
\(D+L\leq(1+1/\beta)L\), so (18)--(20) give the matching upper bound.

## Relation to the fixed-accuracy staircase

For fixed \(K\), choosing any fixed odd \(n=2r+1\) with \(H_n> K\)
recovers the exponent \(\delta^{-(2r+1)/(2r+2)}\) from the adaptive
Taylor-jet lower hierarchy.  The new content is quantitative uniformity when
the truncation order grows with \(K^{-1}\), plus the matching law (6).
The sharper fixed-\(K\) phase diagram uses global nonnegative limits and the
even-degree thresholds \(G_r\); the exterior thresholds \(H_n\) here are a
finite-order quantitative surrogate and should not be conflated with
\(G_r\).  The companion
[uniform Fejér--Riesz jet bound](2026-09-04-joint-accuracy-normalized-shift-lower.md)
gives an independent lower-bound route through a globally nonnegative square.
Its fixed-radius branch removes any growth restriction on
\(\log(1/K)\) and independently proves the full matched high-accuracy law.
The two proofs use different finite-order obstructions, \(G_r\) and \(H_n\),
and therefore provide a useful cross-check rather than a circular derivation.

## Novelty boundary

Trigonometric polynomial query representations, Bernstein inequalities,
Chebyshev exterior extremality, and bounded polynomial approximations to the
sign function are prior art.  The apparent novelty is their growing-order
combination in (4), the monotone integral construction (19) for a
unit-normalized shift, and the closed joint law (6).  A targeted literature
screen found no matching gap--accuracy lower law or contractive integrated-sign
shift construction.  Dong--Larsen--Lin--Sarkar's very recent
[constrained-minimax QSP work](https://arxiv.org/abs/2608.30937) develops
numerical Remez and Fourier-retraction methods for general bounded QSP design,
but does not state this shift problem, its query lower bound, or (6).
Gilyén--Su--Low--Wiebe's
[QSVT work](https://arxiv.org/abs/1806.01838) supplies the bounded sign
approximant and synthesis ingredients.  The
\(\delta^{-1}\log(1/\epsilon)\) form also parallels known optimal fixed-point
amplitude amplification and is not claimed novel in isolation.  The
defensible new claim is the arbitrary-completion coherent-converter lower and
the full joint threshold law in this normalized-complement problem.  Apparent
novelty is not a guarantee against an unlocated approximation-theory
antecedent.

The theorem concerns a reusable coherent unitary output.  It does not cover
postselected renormalization or stochastic branch-dependent output channels,
whose amplitudes need not obey the same bounded trigonometric-polynomial
representation.

See [the fixed-accuracy staircase](2026-09-04-normalized-shift-staircase.md)
and [the adaptive lower hierarchy](2026-09-04-adaptive-normalized-shift-hierarchy.md).
