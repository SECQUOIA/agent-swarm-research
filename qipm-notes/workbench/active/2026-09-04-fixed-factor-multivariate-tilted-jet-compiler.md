# Fixed-factor multivariate tilted-jet scenario compression

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the fixed-factor theorem, source-query ledger, support
bound, and lower-bound oracle separations

Update: the later
[growing-factor refinement](2026-09-04-growing-factor-tilted-jet-refinement.md)
removes the \((Cr)^r\) query prefactor below, replacing it by \(C_0^r\) for
constant-or-larger coordinate width \(K\).  At bounded dual width
\(B=rK\), its empirical-process arm is dimension-free in source queries
and direct positive-atom count, and its cube-section lower bound forces
\(R=\Omega(B^2/\epsilon)\) in the stated growing-r accuracy regime.  The
present theorem remains a valid independently audited baseline.

## Convention and result

Let \(X\) be a source distribution on \([-1,1]^r\), available through
coherent weighted sampling and a coherent vector-value oracle, and define

\[
 f(z)=\mathbb E[e^{\langle z,X\rangle}],
 \qquad z\in[-K,K]^r.
 \tag{1}
\]

The coordinatewise sector is important: throughout this note

\[
 B:=\sup_{z\in[-K,K]^r,\,x\in[-1,1]^r}
 |\langle z,x\rangle|=rK.
 \tag{2}
\]

If the exposure domain were instead \(\|z\|_1\leq K\), every occurrence of
\(B=rK\) below would become \(K\).  This distinction prevents hiding an
exponential factor in the norm convention.

For \(K\geq1/r\), \(0<\epsilon\leq1/2\), and fixed factor dimension \(r\),
there is a confidence-certified compiler which, with failure probability at
most \(\alpha\), returns a classical positive atomic measure

\[
 \psi=\sum_{\ell=1}^R\theta_\ell\delta_{\widehat x_\ell},
 \qquad \widehat x_\ell\in[-1,1]^r,
 \tag{3}
\]

on a public rational grid such that

\[
 (1-\epsilon)f(z)\leq
 g_\psi(z):=\sum_{\ell=1}^R\theta_\ell
 e^{\langle z,\widehat x_\ell\rangle}
 \leq(1+\epsilon)f(z)
 \quad\text{for every }z\in[-K,K]^r.
 \tag{4}
\]

One may take

\[
 d=O\bigl(B+\log(1/\epsilon)\bigr),\qquad
 R\leq {r+d\choose r},
 \tag{5}
\]

and the quantum source-query cost is

\[
 \widetilde O\left(
 {A_r (C r)^r e^{B}\over\epsilon}
 \log{1\over\alpha}\right),
 \qquad
 A_r\leq e^{C\sqrt r}.
 \tag{6}
\]

Here \(C\) is numerical and the tilde hides confidence and arithmetic
logarithms.  Thus, for every fixed \(r\),

\[
 Q=\widetilde O_r(e^{rK}/\epsilon),\qquad
 R=O_r\bigl((rK+\log(1/\epsilon))^r\bigr).
 \tag{7}
\]

If indexed access to all source weights and vectors is also available, the
query bound in (6) can be replaced by its minimum with \(N\).  The
dependence exponential in \(r\), the degree-\(r\) support polynomial, and
the explicit-grid size below are genuine fixed-factor qualifications, not
suppressed polynomial factors.

## Public rounding

Round every coordinate of \(X\) to a public rational grid with
\(\|Y-X\|_\infty\leq h\).  Since

\[
 |\langle z,Y-X\rangle|\leq rKh=Bh,
\]

the rounded MGF \(\overline f(z)=\mathbb E[e^{\langle z,Y\rangle}]\)
satisfies

\[
 e^{-Bh}f(z)\leq\overline f(z)\leq e^{Bh}f(z).
 \tag{8}
\]

Taking \(h=\Theta(\epsilon/B)\) consumes only a constant fraction of the
relative-error budget.  The full public slope grid has

\[
 G=O\left((1+B/\epsilon)^r\right)
 \tag{9}
\]

points.  This grid is used to make atom extraction a finite rational
feasibility problem; the final support is much smaller than \(G\).

## Constant-radius tilt cover

Fix \(\tau=1/4\) and put \(a=\tau/r\).  Take a tensor grid of centers
\(\mathcal Z\subset[-K,K]^r\) with one-dimensional spacing \(2a\), adjusted
at the endpoints.  Every \(z\) has a center \(z_j\) satisfying

\[
 \|z-z_j\|_\infty\leq a,\qquad
 \|z-z_j\|_1\leq\tau.
 \tag{10}
\]

The center count and the weighted center count are

\[
 J=O((1+rK)^r),\qquad
 \sum_{z_j\in\mathcal Z}e^{\|z_j\|_1}
 =O((C r e^K)^r).
 \tag{11}
\]

To verify the second identity, the one-dimensional geometric sum on a grid
of spacing \(\Theta(1/r)\) is \(O(r e^K)\), and the tensor sum factorizes
into the product of \(r\) such sums.  This is the precise covering-number
cost.

At center \(z_j\), define

\[
 W_j(y)=e^{\langle z_j,y\rangle-\|z_j\|_1}\in[0,1],
 \quad b_j=\mathbb E[W_j(Y)],
 \quad B_{j,\nu}=\mathbb E[W_j(Y)Y^\nu],
 \tag{12}
\]

for multi-indices \(\nu\in\mathbb N^r\).  The tilted mass obeys

\[
 b_j\geq e^{-2\|z_j\|_1}.
 \tag{13}
\]

## Multivariate local jets

Choose a local total degree \(m\), write
\(\nu!=\prod_k\nu_k!\), and set

\[
 c_\nu={a^{|\nu|}\over\nu!},\qquad
 S_{r,m}=\sum_{|\nu|\leq m}\sqrt{c_\nu}.
 \tag{14}
\]

The tensor-product majorant gives

\[
 S_{r,m}\leq
 \left(\sum_{q=0}^\infty{a^{q/2}\over\sqrt{q!}}\right)^r,
 \qquad
 A_r:=\left(\sum_{q=0}^\infty
                 {a^{q/2}\over\sqrt{q!}}\right)^{2r}
 \leq e^{C\sqrt r}.
 \tag{15}
\]

For the last inequality, \(a=\Theta(1/r)\) and
\(\log(1+O(\sqrt a))=O(\sqrt a)\).

Use feature tolerances

\[
 \xi_\nu=\min\left\{1,
 {c\epsilon\over S_{r,m}\sqrt{c_\nu}}\right\}.
 \tag{16}
\]

For every active feature \(\xi_\nu<1\), estimate
\(B_{j,\nu}\) to additive accuracy \(\Theta(b_j\xi_\nu)\).
As in the scalar compiler, encode the two nonnegative means

\[
 \mathbb E\left[{W_j(Y)(1+Y^\nu)\over2}\right],
 \qquad
 \mathbb E\left[{W_j(Y)(1-Y^\nu)\over2}\right].
 \tag{17}
\]

Both are at most \(b_j\).  The distribution-sensitive
\(O(\sqrt q/M+1/M^2)\) amplitude-estimation error therefore gives feature
cost

\[
 O\left({1\over\xi_\nu\sqrt{b_j}}\right).
 \tag{18}
\]

A constant-relative pilot for \(b_j\), capped using (13), makes the
confidence widths implementable without knowing \(b_j\).  Moreover,

\[
 \sum_{\nu:\xi_\nu<1}{1\over\xi_\nu}
 \leq {S_{r,m}^2\over c\epsilon}
 \leq {A_r\over c\epsilon}.
 \tag{19}
\]

Combining (11), (13), and (18)--(19) proves (6).

Solve a positive grid-weight LP imposing all active confidence intervals
and normalization.  The rounded source histogram is feasible on the joint
success event.  For any feasible \(\theta\), the interval diameter, the
accurate \(\nu=0\) row, and the trivial inactive-feature bound give

\[
 |B_{j,\nu}^{\theta}-B_{j,\nu}|
 \leq Cb_j\xi_\nu
 \qquad(|\nu|\leq m).
 \tag{20}
\]

Let \(z=z_j+t\), so \(\|t\|_1\leq\tau\).  The total-degree Taylor expansion
is

\[
 e^{-\|z_j\|_1}\overline f(z_j+t)
 =\sum_{|\nu|\leq m}{t^\nu\over\nu!}B_{j,\nu}
  +R_j(t).
 \tag{21}
\]

Because \(|\langle t,Y\rangle|\leq\tau\), its remainder is at most

\[
 |R_j(t)|\leq
 b_je^\tau{\tau^{m+1}\over(m+1)!}.
 \tag{22}
\]

The feasible measure has the same bound with
\(b_j^\theta\leq2b_j\), and the left side of (21) is at least
\(e^{-\tau}b_j\).  Finally,

\[
 \sum_{|\nu|\leq m}{|t^\nu|\over\nu!}\xi_\nu
 \leq\sum_{|\nu|\leq m}c_\nu\xi_\nu
 \leq 2c\epsilon.
 \tag{23}
\]

Indeed, the active features contribute at most \(c\epsilon\), while for an
inactive feature the definition of \(\xi_\nu\) gives
\(c_\nu\leq(c\epsilon/S_{r,m})\sqrt{c_\nu}\), so all inactive features
together contribute at most another \(c\epsilon\).  This harmless factor
is absorbed by the numerical choice of \(c\).

Choosing \(c\) small and

\[
 m=O\left(1+{\log(1/\epsilon)\over
                 \log(2+\log(1/\epsilon))}\right)
 \tag{24}
\]

gives a uniform relative approximation of \(\overline f\) by the feasible
histogram.  The temporary confidence LP has

\[
 O\left((1+rK)^r {r+m\choose r}\right)
 \tag{25}
\]

rows.  This large row count is part of the honest fixed-factor classical
postprocessing cost, but it will not be the number of output atoms.

## Post hoc multivariate moment compression

Choose \(d\) so that

\[
 2e^{2B}{B^{d+1}\over(d+1)!}\leq c'\epsilon.
 \tag{26}
\]

This is possible with \(d=O(B+\log(1/\epsilon))\).  Preserve exactly every
ordinary grid moment \(Y^\nu\) with \(|\nu|\leq d\).  The moment-vector
dimension, including the constant moment, is

\[
 D={r+d\choose r}.
 \tag{27}
\]

Caratheodory--Tchakaloff compression therefore produces a positive measure
\(\psi\) on at most \(D\) points of the same public grid.  For
\(\|z\|_\infty\leq K\), \(|\langle z,Y\rangle|\leq B\); the matched
total-degree Taylor polynomial and two remainders give

\[
 |g_\psi(z)-g_\theta(z)|
 \leq2e^B{B^{d+1}\over(d+1)!}
 \leq c'\epsilon e^{-B}
 \leq c'\epsilon f(z).
 \tag{28}
\]

Combining (8), the local-jet certificate, and (28) proves (4)--(5).
Rational outward approximation of the tilted LP coefficients and
reversible rotations needs
\[
 O\left(B+\log{1\over\epsilon}+\log{1\over\alpha}
          +\log J+\log {r+m\choose r}\right)
 \tag{28a}
\]
bits under a direct union-bound implementation; their error is charged to
reserved confidence slack.  (More economical confidence bookkeeping can
reduce these logarithmic terms.)  The final compression LP contains only
rational public-grid monomials.

## Classical and quantum lower bounds

The exponent \(B=rK\) is forced by the coordinatewise cube, not by an
upper-bound artifact.  Consider the two source atoms

\[
 x^-:=(-1,\ldots,-1),\qquad x^+:=(1,\ldots,1),
\]

and evaluate at \(z^*:=(K,\ldots,K)\).  If
\(p=\Pr[X=x^+]\), then

\[
 f(z^*)=e^{-B}+(e^B-e^{-B})p.
 \tag{29}
\]

Around \(p=\Theta(e^{-2B})\), a uniform relative-\(\epsilon\) certificate
determines \(p\) to additive \(O(\epsilon e^{-2B})\).  In the hidden
weighted-sampling model, the standard two-amplitude lower bound gives

\[
 Q_{\rm quantum}=\Omega(e^B/\epsilon)
 =\Omega(e^{rK}/\epsilon).
 \tag{30}
\]

This oracle prepares the source distribution but does not explicitly reveal
its two probabilities.  For uniform scenarios under indexed vector-value
access, the same approximate-counting pair realizes (30) whenever
\[
 N=\Omega(e^{2B}/\epsilon),
 \tag{30a}
\]
which ensures that both the rare Hamming weight and its requested
separation are at least constant.

The corresponding Bernoulli KL calculation for i.i.d. classical samples
from the hidden weighted source gives

\[
 Q_{\rm classical}=\Omega(e^{2B}/\epsilon^2)
 =\Omega(e^{2rK}/\epsilon^2)
 \tag{31}
\]

for i.i.d. classical weighted-source samples.  Conversely, applying
Bernstein confidence intervals to the same tilted features gives
\(\widetilde O(A_r e^{2B}/\epsilon^2)\) classical samples, since a single
sample can be reused for every center and multi-index.  Thus, for fixed
\(r\), (6), (30), and (31) match the exponential-sector and accuracy
dependence and exhibit the full quadratic source-access separation.
With indexed uniform scenarios, the classical law instead saturates as
\[
 \widetilde\Theta\left(\min\{N,e^{2B}/\epsilon^2\}\right),
 \tag{31a}
\]
so the fully unsaturated quadratic comparison requires
\(N=\Omega(e^{2B}/\epsilon^2)\).

This hard family changes all \(r\) coordinates and is queried at the
opposite cube corners, so it genuinely realizes the width \(rK\).  It is
not the weaker embedding which varies one coordinate and yields only
\(e^K\).  The lower bound does not force the covering prefactor
\((Cr)^r\) or the support count (27); those may be improvable when \(r\)
grows.

## Low-factor entropic-risk application

Let scenario loadings
\(\lambda_i\in[-\Lambda,\Lambda]^r\), affine factor exposures
\(U(x)\in\mathbb R^r\), and a scale \(V(x)\) obey

\[
 0\leq V(x)\leq V_{\max},\qquad
 \|U(x)\|_\infty\leq LV(x).
 \tag{32}
\]

For \(\beta>0\), define

\[
 {\cal R}_\beta(U,V)
 ={V\over\beta}\log\sum_i p_i
 \exp\left({\beta\langle\lambda_i,U\rangle\over V}\right).
 \tag{33}
\]

This formula is for \(V>0\); on the sector (32), set
\({\cal R}_\beta(0,0)=0\), its continuous limiting value.

After normalizing each loading coordinate by \(\Lambda\), its MGF exposure
lies in the cube with \(K=\beta\Lambda L\) and \(B=rK\).  Replacing the
source by (3), with
\(\widehat\lambda_\ell:=\Lambda\widehat x_\ell\), gives a compressed
entropic-risk function
\(\widetilde{\cal R}_\beta\).  If the compiler returns factors
\(L_*,U_*\), then

\[
 \widetilde{\cal R}_\beta-{V\over\beta}\log U_*
 \leq{\cal R}_\beta\leq
 \widetilde{\cal R}_\beta-{V\over\beta}\log L_*.
 \tag{34}
\]

Therefore the inner/outer optimal-value and feasible-solution guarantees in
[the scalar application theorem](2026-09-04-tilted-jet-entropic-risk-ecp.md)
hold verbatim, with error

\[
 {\gamma V_{\max}\over\beta}\log{U_*\over L_*}.
 \tag{35}
\]

Each output atom requires one three-dimensional exponential cone:

\[
 (\beta\langle\widehat\lambda_\ell,U\rangle-t,\ V,\ q_\ell)
 \in K_{\exp},\qquad
 \sum_\ell\theta_\ell q_\ell\leq V.
 \tag{36}
\]

Thus a base conic lift with barrier parameter \(\nu_0\) becomes a sparse
fixed-factor lift with

\[
 \nu\leq\nu_0+3{r+d\choose r}+O(1).
 \tag{37}
\]

Balanced copy and aggregation trees give \(O(r)\) row incidence at each
cone leaf and constant incidence elsewhere.  At target additive
optimization error \(\tau\), use
\(\epsilon=\Theta(\min\{1,\beta\tau/(\gamma V_{\max})\})\) in
(5)--(7), assuming \(\gamma V_{\max}>0\); otherwise the scenario term is
irrelevant.  Explicitly, the coherent source cost is

\[
 \widetilde O\left(
 A_r(Cr)^r e^{rK}
 \max\left\{1,{\gamma V_{\max}\over\beta\tau}\right\}
 \right),
 \tag{38}
\]

and

\[
 d=O\left(rK+
 \log_+{\gamma V_{\max}\over\beta\tau}\right),\qquad
 R\leq{r+d\choose r}.
 \tag{39}
\]

Here \(\log_+x:=\max\{0,\log x\}\) for \(x>0\).

The original \(N\)-scenario formulation has \(N\) exponential cones; the
compiled formulation has the support count (39), independent of \(N\).

## Independent audit scope

The audit checked the tensor cover in the \(\ell_\infty\) metric and its
\(\ell_1\)-radius \(\tau\), including the factorized weighted sum in (11).
It also checked the worst-case tilt mass (13), the active-feature query sum
(19), the inactive-feature contribution made explicit in (23), and both
local Taylor remainders.  The post hoc moment space has exactly
\({r+d\choose r}\) coordinates including the constant, so its normalized
affine slice needs no extra Caratheodory atom.

For the lower bounds, taking two Bernoulli probabilities separated by
\(\Theta(\epsilon e^{-2B})\) gives state-preparation angle separation
\(\Theta(\epsilon e^{-B})\) and one-sample KL divergence
\(\Theta(\epsilon^2e^{-2B})\).  The indexed version is the corresponding
approximate-counting pair, subject to the integer-weight condition (30a).
Thus the quantum and classical exponents in (30)--(31) use the full cube
width \(B=rK\).  This audit does not claim that the growing-\(r\) cover
factor \((Cr)^r\), the support count, or their dependence on \(r\) is
optimal.

## Literature and scope

Multivariate Tchakaloff compression, exponential tilting, local Taylor
models, and quantum amplitude estimation are individually standard.
[Curto--Fialkow](https://arxiv.org/abs/math/0207065) is a primary antecedent
for positive finite-moment compression.
[Campbell--Beronov](https://arxiv.org/abs/1906.03329) constructs Bayesian
coresets using sparse variational inference in an exponential-family
viewpoint, but targets posterior KL quality rather than a uniform
partition-function bracket on a parameter cube.
[Wainwright--Jaakkola--Willsky](https://arxiv.org/abs/1301.0610) develops
variational log-partition upper bounds for graphical models, not positive
atomic source compression.

A targeted search on 2026-09-04 used combinations of *multivariate MGF*,
*Laplace-transform quadrature*, *positive atomic measure*, *log-partition
coreset*, *low-rank scenario reduction*, and *quantum entropic risk*.  It
found no theorem with the local tilted multi-jet confidence construction,
post hoc multivariate moment compression, a uniform relative certificate
on a continuum of exposures, and the query laws (6), (30), and (31).
This is evidence against an immediate collision, not a priority claim.

The result is useful specifically when \(r\) is a small fixed factor rank:
it replaces \(N\) scenarios by a classical positive atomic summary while
retaining a uniform certificate over a continuum of factor exposures.  It
is not efficient in unrestricted dimension, and equations (6), (9), (25),
and (27) state the associated covering and support curses explicitly.
