# Exact normalized shift for two-point spectra

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated; implies a correction to the access-model discussion  
Confidence: High on mathematics; moderate on apparent novelty  
Question: Must plain block access pay condition-number-scale uniform amplification
to obtain a unit-normalized encoding of \(I-H\)?

## Access model

The input is an exact controlled \((1,a_0,0)\) block encoding \(U_H\) and its
adjoint for an unknown PSD contraction \(0\preceq H\preceq I\). A converter is
an oracle-independent circuit that must output a \((1,b,\eta)\) block encoding
of \(I-H\) for every matrix in the stated promise.

## Exact two-query escape

Let \(0<a<b\leq1\) be known and assume

\[
 (1-a)(1-b)\leq a+b;
\]

in particular, \(b\geq1/2\) suffices. Define the even quadratic

\[
 p_{a,b}(x)=1-\frac{ab}{a+b}-\frac{x^2}{a+b}.
\]

It obeys \(|p_{a,b}(x)|\leq1\) on \([-1,1]\): it decreases with \(x^2\),
its value at zero is below one, and

\[
 p_{a,b}(\pm1)=-\frac{(1-a)(1-b)}{a+b}\geq-1.
\]

Standard QSVT therefore implements a unit-normalized block encoding of
\(p_{a,b}(H)\) using exactly two queries. Moreover,

\[
 \boxed{
 p_{a,b}(H)-(I-H)=-\frac{(H-aI)(H-bI)}{a+b}.
 }
\]

If \(\operatorname{spec}(H)\subseteq\{a,b\}\), the encoding is exact. For
clustered spectra its operator error is exactly

\[
 \max_{\lambda\in\operatorname{spec}(H)}
 \frac{|(\lambda-a)(\lambda-b)|}{a+b}.
\]

In the important edge case \(b=1\), the polynomial is

\[
 p_{a,1}(x)=\frac{1-x^2}{1+a}.
\]

Thus a two-point spectrum \(\{a,1\}\) admits an exact unit-normalized shift in
two queries even as \(1/a\to\infty\). Any shift-conversion lower bound based
only on condition number is false.

## Interval-promise lower bound

The escape is promise-sensitive. Let \(0<\Delta\leq1/4\) and
\(\eta\leq\Delta/16\). Any converter valid for both

\[
 H_\Delta=\operatorname{diag}(\Delta,1),\qquad
 H_{2\Delta}=\operatorname{diag}(2\Delta,1)
\]

requires

\[
 \boxed{
 T\geq\frac{\sqrt3-\sqrt2}{2\sqrt\Delta}
 =\Omega(\Delta^{-1/2}).
 }
\]

This follows by specializing the arbitrary-algorithm polynomial lower bound in
Theorem 73 of Gilyén--Su--Low--Wiebe to \(f(x)=1-x\), at
\(x=\Delta,y=2\Delta\). The complementary-amplitude numerator is at least

\[
 \sqrt{4\Delta-4\Delta^2}-\sqrt{2\Delta-\Delta^2}
 \geq(\sqrt3-\sqrt2)\sqrt\Delta,
\]

while the denominator is \(2\Delta\). The result holds for adaptive coherent
algorithms and arbitrary input-block completions, not only fixed QSVT
polynomials. If zero is allowed and exact error is required, taking the scalar
pair toward zero rules out every finite-query universal converter.

More generally, suppose an exact converter outputs a
\((\nu,b,0)\) encoding of \(I-H\). For a continuum promise near the scalar
point \(x=\Delta\), the same hybrid bound, differentiated at that point,
gives

\[
 \boxed{
 T\geq
 \frac{(1-\Delta)\sqrt{1-\Delta^2}}
 {\nu\sqrt{\nu^2-(1-\Delta)^2}}.
 }
\]

Indeed the target amplitude is \(f_\nu(x)=(1-x)/\nu\), whose complementary
amplitude has derivative
\((1-x)/(\nu\sqrt{\nu^2-(1-x)^2})\), whereas the canonical scalar input
block encoding changes at rate \(1/\sqrt{1-x^2}\). Writing \(\nu=1+s\), for
small \(\Delta,s\) this is \(\Omega((\Delta+s)^{-1/2})\). Thus the edge cost
is sharply tied to demanded normalization: unit normalization forces a
square-root cost, while constant slack can permit constant cost.

## Dichotomy and QIPM implication

For a known exact two-point support, two queries suffice. For an interval
promise broad enough to contain \(\Delta\) and \(2\Delta\), accuracy
\(O(\Delta)\) needs \(\Omega(\Delta^{-1/2})\) queries. Generic uniform
singular-value amplification gives \(O(\Delta^{-1}\log(1/\eta))\). The gap is
real for an unrestricted interval touching the spectral edge, but the
separated two-band promise below admits a matching square-root construction.
A sharper treatment for an arbitrary fixed ratio \(\rho\), including the
exact first-order accuracy threshold, is recorded in
[the companion interval note](2026-09-04-two-cluster-interval-shift-upper.md).

If a symmetric-cone Newton operator has exact Peirce/two-eigenvalue form
\(H=aP+b(I-P)\), plain block access already supplies the normalized shift in
two queries. Approximate two-band structure incurs precisely the factorized
error above. This does not produce a generic condition-number-free QLS:
inverse-output normalization and right-hand-side overlap remain separate
obstructions.

## Tight interval construction

**Status:** proved and independently audited.

Fix a constant \(c\in(0,1]\), take
\(0<\Delta\leq\min\{1/256,c/8\}\), and promise

\[
 \operatorname{spec}(H)\subseteq[\Delta,2\Delta]\cup[c,1].
\]

For all sufficiently small \(\Delta\), there is an even polynomial \(p\) with

\[
 0\leq p(x)\leq1\quad(x\in[-1,1]),
\]

\[
 \max_{x\in[\Delta,2\Delta]\cup[c,1]}
 |p(x)-(1-x)|\leq\Delta/16,
\]

and

\[
 \deg p=O_c(\Delta^{-1/2}+\log(1/\Delta)).
\]

Definite-parity QSVT would therefore give a unit-normalized
\(\Delta/16\)-approximate encoding of \(I-H\) with
\(\widetilde O(\Delta^{-1/2})\) queries. Together with the lower bound above,
this closes the two-band shifted-edge complexity at
\(\Theta_c(\Delta^{-1/2})\) for error \(\Delta/16\). The additive logarithm
is asymptotically smaller.

### Polynomial construction

Use the explicit monotone sign polynomial

\[
 S_k(x)=\frac{\int_0^x(1-t^2)^kdt}{\int_0^1(1-t^2)^kdt}.
\]

It is odd of degree \(2k+1\), sign-preserving, bounded by one, and for fixed
\(c>0\),

\[
 1-S_k(x)\leq C\sqrt{k}(1-c^2)^k\qquad(x\geq c).
\]

Thus

\[
 p_{\rm hi}(x)=1-xS_k(x)
\]

is even, globally in \([0,1]\), and approximates \(1-x\) on \([c,1]\)
with exponentially small error.

For the lower band, let \(d\) be the least even integer at least
\(2/\sqrt\Delta\), put \(s=(-1)^{d/2}\), and define

\[
 D_d(x)=1-sT_d(x)=1-\cos(d\arcsin x),
\]

\[
 C_d(x)=\frac{17\Delta}{24}
 +\frac{2D_d(x)}{3\Delta d^2},
 \qquad p_{\rm lo}(x)=1-C_d(x).
\]

Since \(0\leq D_d\leq2\) and \(\Delta d^2\geq4\), one has
\(0<p_{\rm lo}<1\) globally for small \(\Delta\). Uniformly on
\([\Delta,2\Delta]\),

\[
 \frac{2D_d(x)}{3\Delta d^2}
 =\frac{x^2}{3\Delta}+O(\Delta^2).
\]

The quadratic
\(17\Delta/24+x^2/(3\Delta)\) approximates \(x\) on that interval with
exact minimax error \(\Delta/24\).

Finally put \(\ell=c^2/16\), \(h=c^2\),
\(\theta=(\ell+h)/2\), \(L=\max\{\theta,1-\theta\}\), and
\(u(x)=(x^2-\theta)/L\). Then \(u([-1,1])\subseteq[-1,1]\), and the low and
high regions are separated from zero by the constant
\((h-\ell)/(2L)\). Use another \(S_k\) and set
\(F=(1-S_k(u))/2\) to form an even
selector \(F\in[0,1]\) satisfying

\[
 F\geq1-\varepsilon\quad(|x|\leq c/4),\qquad
 F\leq\varepsilon\quad(|x|\geq c),
\]

with degree \(O_c(\log(1/\varepsilon))\). The convex polynomial blend

\[
 p=Fp_{\rm lo}+(1-F)p_{\rm hi}
\]

stays in \([0,1]\) on the entire QSVT domain. Taking
\(\varepsilon=\Delta/256\) proves the approximation and degree claims.

This particular square-root construction is scoped to the ratio-two lower
band and error \(\Delta/16\).  The
[companion interval theorem](2026-09-04-two-cluster-interval-shift-upper.md)
handles arbitrary fixed band ratio above its affine threshold, while the
[sharp staircase theorem](2026-09-04-normalized-shift-staircase.md) handles
every strict adaptive threshold band, including successively higher relative
accuracies.

## Accuracy-dependent obstruction

The square-root construction has a genuine relative-accuracy threshold; it
cannot extend to arbitrarily small error merely by paying logarithmic factors.
For \(r\geq0\), define the fixed-interval approximation number

\[
 E_r(\rho)=\inf_{A\in\mathbb R_r[u]}
 \max_{1\leq u\leq\rho}|u-A(u^2)|.
\]

Suppose an even degree-\(d\) polynomial \(p\), bounded by one on \([-1,1]\),
approximates \(1-x\) on \([\Delta,\rho\Delta]\) to error \(K\Delta\), where
\(K<E_r(\rho)\). Then

\[
 \boxed{
 d=\Omega_{r,\rho,K}\!\left(
 \Delta^{-1+1/(2r+2)}
 \right).
 }                                                     \tag{3}
\]

To prove this, Taylor-expand \(p\) at zero through degree \(2r\). Evenness
removes the odd powers. After substituting \(x=\Delta u\) and dividing by
\(\Delta\), the function \((1-p(\Delta u))/\Delta\) differs from a
degree-\(r\) polynomial in \(u^2\) by at most

\[
 C_{r,\rho}d^{2r+2}\Delta^{2r+1}.
\]

The derivative estimate follows from the interior Bernstein inequality for
algebraic polynomials: on (say) \([-1/2,1/2]\),
\(\|p^{(j)}\|_\infty\leq C_jd^j\|p\|_\infty\). It can also be obtained by
applying trigonometric Bernstein to \(p(\cos\theta)\) and using the chain rule
away from \(\theta=0,\pi\). The definition of \(E_r\) therefore implies

\[
 E_r(\rho)\leq K+C_{r,\rho}d^{2r+2}\Delta^{2r+1},
\]

which rearranges to (3).

The first nontrivial threshold is explicit:

\[
 E_1(\rho)=\frac{(\rho-1)^2}{8(\rho+1)}.
\]

Indeed this is half the maximum gap between \(\sqrt v\) and its secant on
\(v\in[1,\rho^2]\). Thus relative error below \(E_1(\rho)\) already forces
\(d=\Omega(\Delta^{-3/4})\). Crossing successive fixed-degree approximation
floors pushes the exponent in (3) toward one. In particular, a uniform
\(O(\Delta^{-1/2}\operatorname{polylog}(1/\eta))\) construction for
arbitrarily small \(\eta/\Delta\) is impossible.

This is consistent with the tight construction above: for \(\rho=2\),
\(E_1(2)=1/24<1/16\), so error \(\Delta/16\) lies on the attainable side of
the affine threshold.

## Prior art and correction boundary

Orsucci--Dunjko, *Quantum* 5, 573 (2021), leave the generic normalized
\(I-\eta A\) construction open and invoke the lower-bound machinery of
Gilyén--Su--Low--Wiebe. The latter source already supplies both the general
lower-bound method and uniform-amplification upper bounds. A targeted search
found no statement of the quadratic \(p_{a,b}\) or the exact-support versus
interval-promise dichotomy.

The defensible novelty claim is the elementary two-query construction and its
promise dichotomy, together with the explicit two-band construction, not a new
QSVT or lower-bound technique. The current paper must not claim that faithful
edge amplification intrinsically costs \(\Theta(1/\Delta)\): exact two-point
spectra take two queries, and the fixed-gap two-band promise at error
\(\Delta/16\) has the tight complexity \(\Theta_c(\Delta^{-1/2})\).
