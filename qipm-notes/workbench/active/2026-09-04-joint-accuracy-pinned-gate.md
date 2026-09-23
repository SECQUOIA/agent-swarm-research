# A uniform pinned-gate upper bound at shrinking accuracy

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem

## Theorem

Fix \(\rho>1\) and \(c\in(0,1]\).  Let \(\delta\downarrow0\) and
\(K(\delta)\downarrow0\), and define

\[
 r=r(\delta):=\min\{j\geq1:G_j(\rho)\leq K\}.
\]

If

\[
 r\longrightarrow\infty,
 \qquad r=o(\log(1/\delta)),                                 \tag{1}
\]

then the unit-normalized two-band shift has a reusable converter with

\[
 \boxed{
 Q=O_{\rho,c}\!\left(
 r^3\delta^{-1+1/(2r)}+\log(1/\delta)
 \right).}                                                   \tag{2}
\]

The hidden constant is independent of the growing threshold index.  The
converter has error at most \(G_r\delta\leq K\delta\) on
\([\delta,\rho\delta]\) and at most \(K\delta\) on \([c,1]\).

Since \(K\to0\), the existing adaptive lower theorem gives, for every
fixed \(\varepsilon>0\),

\[
 Q=\Omega_{\rho,\varepsilon}(\delta^{-1+\varepsilon}).       \tag{3}
\]

Thus, throughout (1),

\[
 \frac{\log Q}{\log(1/\delta)}\longrightarrow1.             \tag{4}
\]

This does not match the subpolynomial factor in (2).

## Exact extremizer and contacts

Put

\[
 n=2r,\quad m_0=(\rho+1)/2,\quad h=(\rho-1)/2,
 \quad R_0=\frac{\sqrt\rho+1}{\sqrt\rho-1}.
\]

The exact threshold extremizer is

\[
 P_r(y)=y+G_rT_n((y-m_0)/h),                                \tag{5}
\]

and fixed \(\rho\)-dependent constants bound

\[
 a_\rho r^{-1}R_0^{-2r}
 \leq G_r\leq A_\rho r^{-1}R_0^{-2r}.                       \tag{6}
\]

The positive-error contacts are

\[
 y_j=m_0+h\cos(2\pi j/n),\qquad 0\leq j\leq r.              \tag{7}
\]

Indeed, writing \(\xi=(y-m_0)/h=\cos\phi\), one has
\(T_n(\xi)=\cos(n\phi)\).  Its value is one precisely at
\(\phi_j=2\pi j/n\), \(0\leq j\leq r\), so there are exactly \(r+1\)
positive contacts.  Moreover,

\[
 |y_{j+1}-y_j|\leq h|\phi_{j+1}-\phi_j|
 =\frac{2\pi h}{n},
\]

so they form an \(O_\rho(1/r)\)-net of \([1,\rho]\).

## Pinned polynomial gate

Choose an odd integer

\[
 k=\Theta_\rho(\delta^{-1+1/(2r)}),                         \tag{8}
\]

with a sufficiently large fixed leading constant.  For
\(\theta=\arcsin x\), \(a_j=\arcsin(\delta y_j)\), let

\[
 D_{k,a}(\theta)=\frac{\sin(k(\theta-a))}{k\sin(\theta-a)}.
\]

With \(p=r+2\) and \(s=r+1\), define

\[
 Z(\theta)=\prod_{j=0}^{r}\prod_{\sigma=\pm1}
 \left(1-D_{k,\sigma a_j}(\theta)^{2p}\right)^s,
 \qquad W=1-Z.                                               \tag{9}
\]

Then \(0\leq W\leq1\) and \(W(\delta y_j)=1\).  Odd \(k\)
makes every kernel use only even trigonometric frequencies.  Pairing the
centers \(a_j,-a_j\) makes (9) even in \(\theta\), so \(W\) is a real
polynomial in \(\cos(2\theta)=1-2x^2\).  Direct degree counting gives

\[
 \deg W=O(r^3k).                                             \tag{10}
\]

## Uniform low-band estimate

For \(y\in[1,\rho]\), choose the contact whose angle \(\phi_j\) is
nearest to \(\phi\), and put \(d(y)=|y-y_j|\).  Then
\(d(y)\leq C_\rho/r\).  Assumption (1) gives

\[
 k\delta=\Theta_\rho(\delta^{1/(2r)})=o(1).
\]

The nearest-contact factor in (9) therefore gives

\[
 \lambda(y):=1-W(\delta y)
 \leq[C_\rho r(k\delta)^2d(y)^2]^{r+1}.                     \tag{11}
\]

For \(\Delta=|\phi-\phi_j|\leq\pi/n\), the inequalities
\(1-\cos u\geq2u^2/\pi^2\) for \(|u|\leq\pi\) and
\(|\cos\phi-\cos\phi_j|\leq\Delta\) give the explicit angular slack

\[
 \begin{aligned}
 G_r-[P_r(y)-y]
 &=G_r[1-\cos(n\phi)]\\
 &\geq \frac{2G_rn^2}{\pi^2}\Delta^2
 \geq \frac{2G_rn^2}{\pi^2h^2}d(y)^2
 \geq c_\rho G_rr^2d(y)^2.                                \tag{12}
 \end{aligned}
\]

Write the leading constant in (8) as \(A\), so
\(k\delta=A\delta^{1/(2r)}(1+o(1))\).  Using (6) and
\(d(y)\leq C_\rho/r\), and absorbing the fixed powers of \(A\) into
\(C_{\rho,A}\),

\[
 \frac{\lambda(y)}
 {\delta\{G_r-[P_r(y)-y]\}}
 \leq
 C_{\rho,A} e^{-\log(1/\delta)/r}
 \left(\frac{C_{\rho,A}R_0^2}{r}\right)^r=o(1).            \tag{13}
\]

The ratio is interpreted by continuity at a contact, where
\(\lambda=0\).  Uniformly on the low band, for small enough \(\delta\),

\[
 \lambda(y)\leq
 \tfrac12W(\delta y)\delta\{G_r-[P_r(y)-y]\}.               \tag{14}
\]

Let \(S_N(x^2)\) be the positive truncated expansion used in the fixed
staircase construction, so \(0\leq S_N(x^2)\leq1-x\) for positive
\(x\), and put

\[
 q(x)=W(x)[1-\delta P_r(x/\delta)]+[1-W(x)]S_N(x^2).         \tag{15}
\]

If \(e=P_r-y\) and \(d_N=(1-\delta y)-S_N(\delta^2y^2)\),
then target minus output equals

\[
 (1-x)-q(x)=W\delta e+\lambda d_N,
 \qquad 0\leq d_N\leq1.                                    \tag{16}
\]

Its lower bound by \(-G_r\delta\) is immediate from \(e\geq-G_r\).
Equation (14) is exactly what is needed for the upper bound by
\(G_r\delta\).  Thus (15) meets the threshold without an asymptotic
overshoot.

## High band and contractivity

On \([c,1]\), the shifted kernels satisfy

\[
 W(x)\leq C_{\rho,c}r^2k^{-2(r+2)}.                         \tag{17}
\]

The exterior Chebyshev bound and (6) give

\[
 |P_r(y)|\leq |y|+
 C_\rho r^{-1}R_0^{-2r}[C_\rho(1+|y|)]^{2r}.                \tag{18}
\]

Write \(k=A\delta^{-1+1/n}\), up to odd-integer rounding, and choose the
fixed \(A=A_\rho\) larger than the constant in (18).  Split
\([-1,1]\) into

\[
 |x|\leq4\rho\delta,
 \qquad 4\rho\delta\leq|x|\leq1/k,
 \qquad |x|\geq1/k.                                        \tag{19}
\]

The middle interval is omitted if empty.  In the first region, (18) on
the fixed scaled interval \(|y|\leq4\rho\) gives, for a fixed
\(\Lambda_\rho>1\),

\[
 \delta P_r(x/\delta)
 =O_\rho(\delta\Lambda_\rho^{2r}/r)=o(1)                    \tag{20}
\]

by (1).  In the middle region, (18) is maximized at its outer scale.  Its
linear term contributes at most \(1/k=o(1)\), and its Chebyshev term is
at most

\[
 \frac{C_\rho}{r}\delta R_0^{-n}
 \left[\frac{C_\rho}{k\delta}\right]^n
 \leq\frac{C_\rho}{r}
 \left[\frac{C_\rho}{AR_0}\right]^n=o(1),                 \tag{21}
\]

where \((k\delta)^n=A^n\delta(1+o(1))\).  To justify the last factor
under odd-integer rounding, let
\(k_0=A\delta^{-1+1/n}\).  Then \(k=k_0+O(1)\), and

\[
 (k/k_0)^n=1+o(1)
\]

because \(n/k_0=o(1)\): condition (1) gives \(n=o(\log(1/\delta))\),
whereas \(k_0\) grows exponentially in \(\log(1/\delta)\).
Finally, for
\(|x|\geq1/k\), the pointwise kernel estimate gives

\[
 W(x)\leq C_\rho r^2(k|x|)^{-n-4}.                          \tag{22}
\]

The linear term in (18), after multiplication by \(\delta W\), is at
most \(C_\rho r^2/k=o(1)\).  Since the remaining power of \(|x|\) is
\(n-(n+4)=-4\), the Chebyshev term is also maximized at \(|x|=1/k\)
and is at most

\[
 C_\rho r\left[\frac{C_\rho}{AR_0}\right]^n=o(1).           \tag{23}
\]

Increasing \(A_\rho\) once more makes the sum at most one, proving

\[
 \sup_{|x|\leq1}\delta P_r(x/\delta)W(x)\leq1.              \tag{24}
\]

Since \(P_r\geq0\), writing (15) as

\[
 q=B-\delta P_r(x/\delta)W,
 \qquad B=W+(1-W)S_N(x^2)\in[0,1],
\]

proves \(|q|\leq1\) globally.  On \([c,1]\), (17)--(18) and
\(2(r+2)=n+4\) give, after division by \(G_r\delta\),

\[
 \frac{W\delta|P_r(x/\delta)|}{G_r\delta}
 \leq C_{\rho,c}r^2(C_{\rho,c}/A)^n
 \delta^{3-4/n}+o(1)=o(1),                                \tag{25}
\]

Here the conclusion holds even if \(C_{\rho,c}/A>1\), because the
logarithm of the non-\(\delta\) factor is \(O_{\rho,c}(n)=o(\log(1/\delta))\),
whereas \((3-4/n)\log\delta=-(3-o(1))\log(1/\delta)\).
The linear term satisfies the still smaller bound

\[
 \frac{W|x|}{G_r\delta}
 \leq C_{\rho,c}r^3R_0^n A^{-n-4}
 \delta^{n+2-4/n}=o(1).
\]

Thus the gate error is \(o(G_r\delta)\), and hence is at most
\(K\delta/2\) for all sufficiently small \(\delta\).  For \(c<1\), take

\[
 N+1\geq
 \frac{\log(2/(K\delta))}{-\log(1-c^2)}.
\]

Then the positive-series truncation obeys, uniformly on \([c,1]\),

\[
 |S_N(x^2)-(1-x)|
 \leq(1-x^2)^{N+1}\leq K\delta/2.
\]

For \(c=1\) this tail vanishes at the only high-band point.  Thus in all
cases one may take

\[
 N=O_c(\log(1/(K\delta)))=O_{\rho,c}(\log(1/\delta))         \tag{26}
\]

handles the truncation tail, where the last equality follows from (1) and
(6).  Combining (8), (10), and (26) proves (2).  Generalized QSP
implements the resulting mixed-parity polynomial with constant query
overhead.

## Scope

Condition (1) is sufficient, not claimed necessary.  It makes
\(k\delta\to0\) and controls the reflected contacts in (20).  A regime
\(r=\Theta(\log(1/\delta))\) may be accessible after tracking the
proportionality constant, but is not asserted here.
