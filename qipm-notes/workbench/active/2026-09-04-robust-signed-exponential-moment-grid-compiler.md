# A robust moment-grid compiler for signed exponential recourse

Status: Quantum compilers and classical sampling corollary independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result and the important correction

Let \(w_i>0\), \(\lambda_i\in[-\Lambda,\Lambda]\), and

\[
 q(U,V)=\sum_{i=1}^Nw_iV\exp(\lambda_iU/V)
 \tag{1}
\]

on

\[
 \mathcal S_L=\{(U,V):V\geq0, |U|\leq LV\}.
 \tag{2}
\]

Use the closed-perspective value zero at \(U=V=0\), put
\(W_0=\sum_iw_i\) and \(K=\Lambda L\).  If \(K=0\),
then \(q=W_0V\) on the sector and no source query or exponential cone is
needed.  Below assume \(K>0\), which implies \(\Lambda,L>0\), and let the
normalized slopes \(x_i=\lambda_i/\Lambda\) have probabilities \(w_i/W_0\).

There is a root-recovery-free, confidence-certified compiler which:

1. rounds the slopes to a fixed public grid;
2. estimates finitely many signed moments, without recovering roots of a
   Hankel matrix;
3. solves a linear feasibility problem over nonnegative grid weights; and
4. returns a positive atomic measure on at most \(d+1\) grid points.

For \(0<\epsilon\leq1/2\), it suffices to take an integer \(d\geq1\) with

\[
 d=O\bigl(K+\log(1/\epsilon)\bigr),
 \tag{3}
\]

and, for fixed \(K>0\),

\[
 d=O_K\!\left(
 \frac{\log(1/\epsilon)}{\log\log(1/\epsilon)}
 \right).
 \tag{4}
\]

With failure probability at most \(\alpha\), the output is an at-most-
\((d+1)\)-term exponential sum \(\widetilde q\) and explicit numbers
\(0<L_*\leq U_*\) such that

\[
 L_*q\leq\widetilde q\leq U_*q,
 \qquad
 1-\epsilon\leq L_*\leq U_*\leq1+\epsilon
 \tag{5}
\]

uniformly on \(\mathcal S_L\).  Consequently

\[
 \operatorname{epi}(\widetilde q/L_*)
 \subseteq \operatorname{epi}(q)
 \subseteq \operatorname{epi}(\widetilde q/U_*),
 \tag{6}
\]

and both bounding epigraphs have exact formulations using at most \(d+1\)
three-dimensional exponential cones.

The robust construction removes the ill-conditioned node-recovery step in
the exact Gaussian-quadrature compiler.  It also exposes a correction to a
tempting source-query claim.  Independent signed-moment estimates with
rectangular confidence boxes give

\[
 \widetilde O\!\left(
 \min\left\{N,\frac{e^{2K}\sqrt K}{\epsilon}\right\}
 \right)
 \tag{7}
\]

queries for \(K\geq1\), not
\(\widetilde O(e^K\sqrt K/\epsilon)\).  The missing factor \(e^K\) is real
in this proof: a signed exponential average can be as small as \(e^{-K}\),
so an absolute Taylor-moment error must be \(O(\epsilon e^{-K})\).
Equation (7) is \(\widetilde O(\min\{N,1/\epsilon\})\) for every fixed
nonzero \(K\).  A lower bound below matches its \(N,\epsilon\) dependence
for fixed \(K\), and gives \(\Omega(e^K/\epsilon)\) in a natural growing-
\(K\) regime.  The new tilted-jet construction below closes that large-\(N\)
growing-sector gap: it uses

\[
 \widetilde O\!\left(\min\{N,e^K/\epsilon\}\right)
 \tag{7a}
\]

queries and still returns only \(O(K+\log(1/\epsilon))\) positive atoms.
Its temporary feasibility LP has more rows, but a final exact moment
compression removes them from the conic formulation.  A simpler value-grid
construction is retained below because its certificate uses only function
values; it uses \(\widetilde O(\min\{N,e^K/\epsilon^2\})\) queries and
\(O(K/\epsilon)\) output cones.

The quantum branch assumes known \(W_0\), coherent weighted sampling with
probabilities \(w_i/W_0\), and coherent slope-value access.  The \(N\)
branch in every displayed minimum additionally assumes indexed access to
both weights and slopes, so the source can be read explicitly once.

## Public grid and rounded source

Let \(G_h\subset[-1,1]\) be a rational grid and let \(r_h(x)\) be a
deterministic nearest-grid map satisfying

\[
 |r_h(x)-x|\leq h.
 \tag{8}
\]

There are \(O(1+1/h)\) grid points.  Define \(Y=r_h(X)\), where \(X\) has the
source distribution, and let

\[
 \overline M_p=\mathbb E[Y^p],\qquad p=1,\ldots,d.
 \tag{9}
\]

It is important to estimate the moments of the *rounded* value \(Y\), not
the moments of \(X\) and then widen every box by a Lipschitz bound.  The
rounding is public reversible arithmetic after one call to the value oracle
and costs no additional source query.

Let

\[
 f(z)=\mathbb E[e^{zX}],\qquad
 \overline f(z)=\mathbb E[e^{zY}].
\]

Termwise comparison gives the multiplicative rounding certificate

\[
 e^{-Kh}f(z)\leq\overline f(z)\leq e^{Kh}f(z)
 \qquad(|z|\leq K).
 \tag{10}
\]

For example, \(h=\epsilon/[16(K+\epsilon)]\) is sufficient, and the public
grid needs only \(O(1+K/\epsilon)\) points.  This is stronger than the
looser \(O(1+Ke^K/\epsilon)\) grid-size target.

## Signed amplitude estimation and the moment polytope

Assume a coherent weighted-sampling oracle prepares the source index with
probability \(w_i/W_0\), and a value oracle returns \(x_i\).  Reversible
arithmetic computes \(Y^p\in[-1,1]\).  To estimate this signed mean, rotate
an ancilla with success probability

\[
 \frac{1+Y^p}{2}.
\]

Amplitude estimation to probability error \(\eta_p/2\) therefore gives a
number \(\widehat M_p\) satisfying

\[
 |\widehat M_p-\overline M_p|\leq\eta_p
 \tag{11}
\]

at cost \(O(1/\eta_p)\), up to confidence amplification.  This factor of two
is needed for a signed observable.  Split total failure probability among
the active moments.

Write the grid points as \(g_1,\ldots,g_G\).  Solve the linear feasibility
problem

\[
 \theta_j\geq0,\qquad
 \sum_j\theta_j=1,\qquad
 \left|\sum_j\theta_jg_j^p-\widehat M_p\right|\leq\eta_p
 \quad(1\leq p\leq d).
 \tag{12}
\]

On the simultaneous-success event, the rounded source histogram is feasible.
Hence (12) cannot fail on that event.  If \(M_p^\theta=\sum_j\theta_jg_j^p\),
then every feasible solution obeys

\[
 |M_p^\theta-\overline M_p|\leq2\eta_p.
 \tag{13}
\]

The factor two in (13) is the diameter of a confidence box, rather than its
radius.

The moment vector \(M^\theta\in\mathbb R^d\) lies in the convex hull of the
grid moment-curve points
\((g_j,g_j^2,\ldots,g_j^d)\).  Caratheodory's theorem therefore replaces
\(\theta\), while preserving its moment vector exactly, by a nonnegative
vector supported on at most \(d+1\) grid points.  Equivalently, one may take
a basic feasible solution after fixing the attained moment vector.  The
number of active box inequalities does not increase this support bound.

## Uniform error certificate

Let

\[
 a_p=\frac{K^p}{p!},\qquad
 S_d(K)=\sum_{p=1}^d\sqrt{a_p},
 \tag{14}
\]

and choose a moment budget \(\delta>0\).  Set

\[
 \eta_p=\min\left\{1,\frac{\delta}{S_d(K)\sqrt{a_p}}\right\}.
 \tag{15}
\]

If \(\eta_p=1\), the trivial estimate \(\widehat M_p=0\) and interval
\([-1,1]\) require no query.  In all cases,

\[
 \sum_{p=1}^da_p\eta_p\leq\delta.
 \tag{16}
\]

Indeed, \(a_p\eta_p\leq\delta\sqrt{a_p}/S_d(K)\) term by term.

Let

\[
 g_\theta(z)=\sum_j\theta_je^{zg_j}.
\]

Taylor's theorem and (13) give, uniformly for \(|z|\leq K\),

\[
 \left|g_\theta(z)-\overline f(z)\right|
 \leq
 2e^K\frac{K^{d+1}}{(d+1)!}
 +2\sum_{p=1}^da_p\eta_p
 \leq A_d,
 \tag{17}
\]

where

\[
 A_d=2e^K\frac{K^{d+1}}{(d+1)!}+2\delta.
 \tag{18}
\]

The two Taylor remainders in (17), one for each probability measure, explain
the first factor two.  Since \(f(z)\geq e^{-K}\), (10) and (17) imply

\[
 \bigl(e^{-Kh}-e^KA_d\bigr)f(z)
 \leq g_\theta(z)\leq
 \bigl(e^{Kh}+e^KA_d\bigr)f(z).
 \tag{19}
\]

Thus one can take

\[
 L_*=e^{-Kh}-e^KA_d,\qquad
 U_*=e^{Kh}+e^KA_d.
 \tag{20}
\]

For example, choose

\[
 h\leq\min\left\{1,\frac{\epsilon}{16K}\right\},\qquad
 \delta\leq\frac{\epsilon e^{-K}}{32},\qquad
 e^{2K}\frac{K^{d+1}}{(d+1)!}\leq\frac{\epsilon}{32}.
 \tag{21}
\]

These choices give \(e^KA_d\leq\epsilon/8\).  Also
\(e^{-Kh}\geq1-\epsilon/16\), while
\(e^{Kh}\leq1+2Kh\leq1+\epsilon/8\).  Hence
\(L_*\geq1-3\epsilon/16\), \(U_*\leq1+\epsilon/4\), and (5) holds with
the displayed constants.  The factorial bound \(n!\geq(n/e)^n\) proves
(3), while the
usual Stirling inversion proves (4).

Finally define

\[
 \widetilde q(U,V)=W_0Vg_\theta(\Lambda U/V).
 \tag{22}
\]

Each term in (22) is represented by one exponential cone.  Scaling the last
aggregation inequality by the explicit constants \(L_*,U_*\) proves (6).
For the standard parameter-three exponential-cone barrier, the displayed
moment-grid formulation has
\(\nu\leq3(d+1)+O(1)\), rather than the source formulation's
\(3N+O(1)\).  Copies of \((U,V)\) and a partial-sum aggregation chain give
constant scalar incidence and scalar KKT treewidth.  As usual, translating
this barrier reduction into an end-to-end IPM bound still requires
initialization, neighborhood, and inexact-Newton hypotheses.

## Source-query ledger

For every active moment, signed amplitude estimation costs
\(\widetilde O(1/\eta_p)\).  Therefore

\[
 \sum_{p:\eta_p<1}\frac1{\eta_p}
 \leq\frac{S_d(K)^2}{\delta}.
 \tag{23}
\]

As in the positive-slope compiler,

\[
 S_d(K)^2\leq S_\infty(K)^2
 =\Theta(e^K\sqrt K)\qquad(K\geq1).
 \tag{24}
\]

The relative-error choice \(\delta=\Theta(\epsilon e^{-K})\) in (21) gives
(7).  The \(N\) branch reads each indexed source item once and computes all
rounded powers classically; it uses \(O(N)\) value queries but may use
\(O(Nd)\) arithmetic.  A sampling oracle alone does not supply this branch.

The often-suggested target

\[
 \widetilde O(e^K\sqrt K/\epsilon)
 \tag{25}
\]

would follow from putting \(\delta=\Theta(\epsilon)\) in (23).  That only
certifies normalized *absolute* error.  For signed slopes, the example
\(X\equiv-1,z=K\) has \(f(z)=e^{-K}\), so it does not certify uniform
relative error.  Within the independent rectangular-moment-box proof,
Cauchy--Schwarz shows that (23) is already the optimal allocation of the
widths subject to \(\sum_pa_p\eta_p\leq\delta\).  Hence (25) needs a
different source summary or a correlated, distribution-sensitive confidence
region; it is not obtained by retuning the \(\eta_p\)'s.

## Tilted local jets close the growing-sector query gap

The extra factor \(e^K\sqrt K\) is not information-theoretic.  It can be
removed by estimating moments after several local exponential tilts, and
then compressing only after the confidence LP has been solved.

**Theorem (tilted-jet compiler).**  Suppose \(K\geq1\) and
\(0<\epsilon\leq1/2\).  Under coherent weighted-sampling and coherent value
access, a positive atomic measure \(\psi\) can be produced, with failure
probability at most \(\alpha\), such that

\[
 (1-\epsilon)f(z)\leq g_\psi(z)\leq(1+\epsilon)f(z)
 \qquad(-K\leq z\leq K).
 \tag{TJ1}
\]

The measure has at most

\[
 d+1=O\bigl(K+\log(1/\epsilon)\bigr)
 \tag{TJ2}
\]

atoms on the public rounded-slope grid, and the source-query cost is

\[
 \widetilde O\!\left(
 \min\left\{N,{e^K\over\epsilon}\right\}
 \log {1\over\alpha}
 \right).
 \tag{TJ3}
\]

Here and below the tilde hides logarithms in the displayed parameters and
reversible-arithmetic precision.  The \(O(N)\) arm in (TJ3) additionally
requires indexed weight-and-value access; with only the two coherent
oracles, the \(e^K/\epsilon\) arm is the claim.  For fixed \(K\), the same final Taylor
compression gives the sharper atom count
\(O_K(\log(1/\epsilon)/\log\log(1/\epsilon))\).

To prove the theorem, fix a numerical constant \(0<\tau<1/2\), and choose
a public set of centers \(z_j\) which covers \([-K,K]\) with radius
\(\tau\), has constant separation, and includes centers within \(\tau\) of
the endpoints.  Thus

\[
 J=O(K),\qquad
 \sum_j e^{|z_j|}=O(e^K).
 \tag{TJ4}
\]

At center \(z_j\), put

\[
 W_j(y)=e^{z_jy-|z_j|}\in[0,1],\quad
 b_j=\mathbb E[W_j(Y)],\quad
 B_{j,p}=\mathbb E[W_j(Y)Y^p].
 \tag{TJ5}
\]

The elementary but decisive bound is

\[
 b_j\geq e^{-2|z_j|}.
 \tag{TJ6}
\]

Let \(a_p=\tau^p/p!\),
\(S_r=\sum_{p=0}^r\sqrt{a_p}\), and choose

\[
 \xi_p=\min\left\{1,
 {c\epsilon\over S_r\sqrt{a_p}}\right\},
 \tag{TJ7}
\]

where \(c>0\) is a sufficiently small numerical constant.  Estimate only
the active features with \(\xi_p<1\), to additive accuracy
\(\Theta(b_j\xi_p)\).  The unknown scale \(b_j\) causes no circularity.  Use
a median-amplified geometric relative-mean routine, capped at the public
lower bound (TJ6).  On its success event it returns
\(\widetilde b_j\in[b_j/2,2b_j]\), with
\(O(b_j^{-1/2}\log(1/\alpha_j))\) queries.  The geometric sum has that same
order, and the cap bounds even a failure path by
\(O(e^{|z_j|}\log(1/\alpha_j))\).  This supplies the proxy used to fix the
absolute confidence radii.  The \(p=0\) feature is active and is re-estimated
to its final requested accuracy.  Split \(\alpha\) over the \(O(Kr)\)
pilot and feature-estimation calls.

For completeness, the query bound follows directly from the
distribution-sensitive error term in amplitude estimation.  Encode the two
nonnegative random variables

\[
 {W_j(Y)(1+Y^p)\over2},\qquad
 {W_j(Y)(1-Y^p)\over2}.
 \tag{TJ8}
\]

Each has mean at most \(b_j\).  The Brassard--Hoyer--Mosca--Tapp estimate
after \(M\) Grover iterates has error
\(O(\sqrt a/M+1/M^2)\) for a success probability \(a\).  Consequently an
additive \(\Theta(b_j\xi_p)\) estimate costs

\[
 O\left({1\over\xi_p\sqrt{b_j}}\right)
 \tag{TJ9}
\]

queries; the \(M^{-2}\) term is smaller because \(0<\xi_p\leq1\).
Confidence amplification contributes only a logarithm.  Moreover,

\[
 \sum_{p:\xi_p<1}{1\over\xi_p}
 \leq {S_r^2\over c\epsilon}=O(1/\epsilon),
 \tag{TJ10}
\]

because \(S_r\leq\sum_{p\geq0}\sqrt{\tau^p/p!}=O_\tau(1)\).
Equations (TJ4), (TJ6), and (TJ9)--(TJ10) give

\[
 \widetilde O\left({1\over\epsilon}
 \sum_jb_j^{-1/2}\right)
 =\widetilde O(e^K/\epsilon).
 \tag{TJ11}
\]

Now solve a nonnegative grid-weight LP containing the confidence interval
for every active \(B_{j,p}\), together with normalization.  The rounded
source histogram is feasible on the simultaneous-success event.  If
\(\theta\) is any feasible solution, the diameter of the confidence
intervals and the accurate \(p=0\) row imply, after changing only numerical
constants,

\[
 |B_{j,p}^{\theta}-B_{j,p}|
 \leq Cb_j\xi_p\qquad(0\leq p\leq r).
 \tag{TJ12}
\]

For an inactive row, (TJ12) means the trivial bound with \(\xi_p=1\): the
\(p=0\) row gives \(b_j^\theta\leq2b_j\), so
\(|B_{j,p}^{\theta}-B_{j,p}|\leq b_j^\theta+b_j\leq3b_j\).

Take \(z=z_j+t\), \(|t|\leq\tau\).  After multiplying the MGF by
\(e^{-|z_j|}\), its local Taylor coefficients are exactly (TJ5):

\[
 e^{-|z_j|}\overline f(z_j+t)
 =\sum_{p=0}^r{t^p\over p!}B_{j,p}+R_j(t).
 \tag{TJ13}
\]

The source remainder is at most
\(b_je^\tau\tau^{r+1}/(r+1)!\); the feasible measure has the same bound
with \(b_j^\theta\leq2b_j\).  Also the left side of (TJ13) is at least
\(e^{-\tau}b_j\).  Therefore (TJ7), (TJ12), and
\(\sum_pa_p\xi_p\leq c\epsilon\) give

\[
 \sup_{|t|\leq\tau}
 \left|{g_\theta(z_j+t)\over\overline f(z_j+t)}-1\right|
 \leq C_1c\epsilon+
 {C_2e^{2\tau}\tau^{r+1}\over(r+1)!}.
 \tag{TJ14}
\]

Choose \(c\) small enough and

\[
 r=O\left({\log(1/\epsilon)\over
                 \log\log(1/\epsilon)}\right)
 \tag{TJ15}
\]

(with a constant fallback for nonasymptotic \(\epsilon\)) so that (TJ14)
is at most a chosen constant fraction of \(\epsilon\).  The centers cover
the whole interval, proving a uniform relative certificate for \(\theta\).
Notice that the confidence LP has \(O(Kr)\) rows; this is not the final
number of atoms or cones.

For the last step, choose \(d\) so that

\[
 2e^{2K}{K^{d+1}\over(d+1)!}\leq c'\epsilon.
 \tag{TJ16}
\]

Caratheodory compression of the first \(d\) ordinary moments of \(\theta\)
produces a positive measure \(\psi\), supported on at most \(d+1\) points
of the same public slope grid.  Taylor's theorem gives

\[
 |g_\psi(z)-g_\theta(z)|
 \leq2e^K{K^{d+1}\over(d+1)!}
 \leq c'\epsilon e^{-K}
 \leq c'\epsilon f(z).
 \tag{TJ17}
\]

Thus compression does not need to preserve any tilted constraint.  Finally,
take \(Kh=O(\epsilon)\) in the public rounding step and combine (10),
(TJ14), and (TJ17).  Keeping the three error budgets explicit gives
computable factors, for example

\[
 L_*=e^{-Kh}(1-\epsilon_{\rm jet})-\epsilon_{\rm cmp},
 \qquad
 U_*=e^{Kh}(1+\epsilon_{\rm jet})+\epsilon_{\rm cmp},
 \tag{TJ18}
\]

with each budget chosen so that
\(1-\epsilon\leq L_*\leq U_*\leq1+\epsilon\).  Applying the perspective and
the same scaling argument as in (22) proves the certified epigraph bracket
using only the \(d+1\) atoms in \(\psi\).  The indexed \(O(N)\) branch reads
the source histogram exactly and performs only the last compression.

This proof explains why local tilting is essential.  At center \(z_j\),
relative feature accuracy costs \(b_j^{-1/2}\), not \(b_j^{-1}\); constant
spacing makes the sum of these costs geometric.  Estimating independent
ordinary moments at the origin instead pays for the global coefficient
envelope and the worst relative denominator simultaneously.

### Matched classical sampling law and quadratic separation

The same construction also identifies the classical sampling boundary.
One classical draw of \(Y\) supplies every center and every feature in
(TJ8); their correlation is harmless because the guarantee is simultaneous,
not an independence claim.  Put

\[
 S_{2/3}=\sum_{p=0}^r a_p^{2/3},\qquad
 \xi_p=\min\left\{1,
 {c\epsilon\,a_p^{-1/3}\over S_{2/3}}\right\}.
\]

Then \(\sum_pa_p\xi_p\leq c\epsilon\).  Indeed, the active terms give this
bound directly, while for an inactive term
\(a_p^{1/3}\leq c\epsilon/S_{2/3}\), so
\(a_p\leq(c\epsilon/S_{2/3})a_p^{2/3}\).  Moreover,

Also \(\sum_{p\geq0}(\tau^p/p!)^{2/3}<\infty\).

For
\(Z_{j,p}^{\pm}=W_j(Y)(1\pm Y^p)/2\), one has
\(0\leq Z_{j,p}^{\pm}\leq1\) and
\(\operatorname{Var}(Z_{j,p}^{\pm})\leq
\mathbb E Z_{j,p}^{\pm}\leq b_j\).
Bernstein's inequality and \(b_j\geq e^{-2|z_j|}\) therefore show that

\[
 n_{\rm samp}=O\left({e^{2K}\over\epsilon^2}
          \log {Kr\over\alpha}\right)
 \tag{TJ19}
\]

i.i.d. weighted-source samples suffice for every confidence width in
(TJ12), because

\[
 \sum_{p:\xi_p<1}{1\over\xi_p^2}
 \leq {S_{2/3}^3\over c^2\epsilon^2}
 =O_\tau(1/\epsilon^2).
 \tag{TJ20}
\]

An empirical-Bernstein interval, or a sample-split constant-factor
pilot followed by an ordinary Bernstein interval, makes the unknown
\(b_j\) implementable; its radius is \(O(b_j\xi_p)\) on the simultaneous
success event.  A union bound over the \(O(Kr)\) center-feature pairs gives
the logarithm in (TJ19).  There is no multiplicative sum over centers or
features in the sample count because every observed \(Y\) evaluates all of
them; the classical arithmetic per sample can nevertheless be \(O(Kr)\).
The same LP and post hoc compression then return the identical type of
certified \(O(K+\log(1/\epsilon))\)-atom output.

This dependence is necessary in the weighted-sampling oracle model.  In the
binary family \(X\in\{-1,+1\}\), take
\(p=\Pr[X=+1]=\Theta(e^{-2K})\) and compare it with
\(p'=p(1+\Theta(\epsilon))\).  Equation (27) shows that the two MGFs at
\(z=K\) differ by relative \(\Theta(\epsilon)\).  Their one-sample
Bernoulli Kullback--Leibler divergence is
\(\Theta(p\epsilon^2)\), so classical hypothesis testing requires

\[
 \Omega(e^{2K}/\epsilon^2)
 \tag{TJ21}
\]

independent samples for constant success probability.  This statement
requires only a sampler returning a binary value with the stated
probability; its cost does not truncate at \(N\).  In particular, it remains
valid for a two-item source with arbitrary hidden sampling weights.  It
does not apply if an indexed oracle directly reveals those two weights.

With indexed weight-and-value access, reading the source gives a second
\(O(N)\) branch.  The resulting query law is

\[
 \widetilde\Theta\left(
 \min\left\{N,{e^{2K}\over\epsilon^2}\right\}\right)
 \tag{TJ21a}
\]

for the worst case, up to confidence logarithms and the usual constant
ranges \(K\geq1\), \(0<\epsilon\leq\epsilon_0\).  A finite-population lower
bound follows already with public equal weights and hidden binary values.
If \(N\lesssim e^{2K}/\epsilon\), distinguish Hamming weights zero and one;
their MGF relative gap is \(\Omega(e^{2K}/N)\), and randomized search costs
\(\Omega(N)\).  If \(N\gtrsim e^{2K}/\epsilon\), take a base weight
\(\Theta(Ne^{-2K})\) and a separation
\(\Theta(\epsilon Ne^{-2K})\).  The standard hypergeometric two-weight
bound is

\[
 \Omega\left(
 \min\left\{N,
 {\Theta(e^{-2K})\over
  \Theta(\epsilon e^{-2K})^2}\right\}\right)
 =
 \Omega\left(\min\left\{N,{e^{2K}\over\epsilon^2}\right\}\right).
\]

For a short justification, apply Yao's principle after uniformly permuting
each fixed-weight input.  Any adaptive algorithm then sees sampling without
replacement.  For \(q\leq cN\), the chain rule bounds the transcript
KL divergence by
\(O(q\,\Delta_p^2/p)\), where \(p\) is the base fraction and
\(\Delta_p\) is the difference of the two fractions.  Pinsker's inequality
therefore forces
\(q=\Omega(\min\{N,p/\Delta_p^2\})\), which is the displayed bound.
Rounding the two weights only changes constants once their separation is at
least one; the zero-versus-one construction covers the smaller-\(N\)
regime.  Thus (TJ21a) includes the finite-population and integrality
qualifications that are absent from the pure sampling statement (TJ21).

Under coherent weighted-sampling access, the corresponding two-Bernoulli
amplitude-estimation lower bound is
\(\Omega(e^K/\epsilon)\), matching (TJ3); for public equal weights the same
large-source conclusion is (28).  Thus the sampling-only laws are
quadratically separated:
\(\widetilde\Theta(e^{2K}/\epsilon^2)\) classically versus
\(\widetilde\Theta(e^K/\epsilon)\) quantumly.  This comparison deliberately
contrasts classical samples with coherent access to the same sampling
distribution.  With indexed access, the full quadratic relation requires
the genuinely large-source regime
\(N=\Omega(e^{2K}/\epsilon^2)\); for
\(e^{2K}/\epsilon\lesssim N\lesssim e^{2K}/\epsilon^2\), the classical
law saturates at \(N\) while the quantum law has already saturated at
\(e^K/\epsilon\).  The separation concerns source queries/samples and
preserves a classical list of positive atoms; it does not claim an
exponential end-to-end runtime separation after solving the explicit
feasibility LP.

## A complementary value-grid compiler

There is also a simpler construction which uses only function values.  It
is now dominated in query and output-cone complexity by the tilted-jet
compiler, but it remains useful as a short independent certificate.

Keep the same rounded slope grid.  Choose public evaluation points
\(\mathcal Z\subset[-K,K]\) with covering radius \(s\), and for each
\(z_j\in\mathcal Z\) estimate the nonnegative normalized mean

\[
 b_j=\mathbb E[e^{z_jY-|z_j|}].
 \tag{25a}
\]

The summand is in \([0,1]\) and \(b_j\geq e^{-2|z_j|}\).  Relative amplitude
estimation with relative error \(\gamma\) therefore uses

\[
 \widetilde O\!\left(\frac{e^{|z_j|}}{\gamma}\right)
 \tag{25b}
\]

source queries.  If the relative estimate is \(\widehat b_j\), use the
specific confidence interval

\[
 [\ell_j,u_j]
 =
 \left[
 \frac{\widehat b_j}{1+\gamma},
 \frac{\widehat b_j}{1-\gamma}
 \right].
\]

Then solve the positive grid-weight LP

\[
 \theta\geq0,\qquad {\bf1}^{\mathsf T}\theta=1,\qquad
 \ell_j\leq
 \sum_g\theta_g e^{z_jg-|z_j|}
 \leq u_j
 \quad(z_j\in\mathcal Z).
 \tag{25c}
\]

The rounded source histogram certifies feasibility.  If both it and a
feasible \(\theta\) lie in an interval obtained from a relative-\(\gamma\)
estimate, then at every evaluation node

\[
 \left|\log\frac{g_\theta(z_j)}{\overline f(z_j)}\right|
 \leq\log\frac{1+\gamma}{1-\gamma}.
 \tag{25d}
\]

For any positive measure on \([-1,1]\), the logarithmic derivative of its
moment-generating function is a tilted mean in \([-1,1]\).  Hence

\[
 \left|\frac{d}{dz}\log
 \frac{g_\theta(z)}{\overline f(z)}\right|\leq2.
\]

At an arbitrary \(z\), comparison with the nearest evaluation node and then
with the unrounded source gives the completely multiplicative certificate

\[
 \left|\log\frac{g_\theta(z)}{f(z)}\right|
 \leq
 Kh+\log\frac{1+\gamma}{1-\gamma}+2s.
 \tag{25e}
\]

Taking \(Kh,\gamma,s=\Theta(\epsilon)\) proves a uniform
\((1\pm\epsilon)\) bracket.  There are
\(J=O(1+K/\epsilon)\) evaluation points, and Caratheodory compression in
\(\mathbb R^J\) leaves at most \(J+1\) positive slope-grid atoms.  Summing
(25b) over a uniform evaluation grid gives

\[
 \widetilde O\!\left(
 \min\left\{N,\frac{e^K}{\epsilon^2}\right\}
 \right)
 \tag{25f}
\]

source queries.  The \(N\) branch again reuses one explicit read of each
source value.  Together with the tilted-jet theorem, the public-grid
compilers give

\[
 \widetilde O\!\left(
 \min\left\{N,\frac{e^K}{\epsilon}\right\}\right).
 \tag{25g}
\]

The value-grid method has \(O(1+K/\epsilon)\), rather than
\(O(K+\log(1/\epsilon))\), output cones.  For a
rational implementation, approximate each feature coefficient
\(c_{jg}=e^{z_jg-|z_j|}\) by \(\widetilde c_{jg}\) with
\[
 |\widetilde c_{jg}-c_{jg}|\leq\rho_j,
 \qquad
 \rho_j=O(\gamma e^{-2|z_j|}).
\]
Enlarge the LP confidence interval by \(\rho_j\), which makes the rounded
source feasible.  Interpreting a feasible rational solution with the true
coefficients incurs at most one further \(\rho_j\), still only a relative
\(O(\gamma)\) perturbation because \(b_j\geq e^{-2|z_j|}\).  Resolving these
features costs \(O(K+\log(1/\epsilon))\) bits and gives the same explicit
finite-bit LP conclusion as the moment-grid construction.
Its displayed product formulation has barrier parameter
\(3(J+1)+O(1)=O(1+K/\epsilon)\).

## Why estimating unrounded moments is worse

Suppose instead that one estimates \(M_p=\mathbb E[X^p]\).  Because

\[
 |Y^p-X^p|\leq ph,
\]

the confidence box in (12) must have half-width at least
\(\eta_p+ph\) for the rounded histogram to certify feasibility.  An arbitrary
feasible solution can then differ from the source moment by
\(2\eta_p+ph\), and the rounding part of the Taylor certificate is

\[
 h\sum_{p=1}^dpa_p\leq hKe^K.
\]

After division by the worst-case value \(e^{-K}\), this becomes
\(hKe^{2K}\).  Thus the naive widened-box proof needs
\(h=O(\epsilon e^{-2K}/K)\), not \(O(\epsilon e^{-K}/K)\).  Estimating the
rounded moments directly and using (10) avoids this artificial loss.

## Lower bounds and what remains

For every fixed \(K>0\), the binary subclass \(X\in\{0,1\}\) reduces a
uniform relative bracket to approximate counting.  Standard quantum
approximate-counting lower bounds give

\[
 \Omega_K\bigl(\min\{N,1/\epsilon\}\bigr)
 \tag{26}
\]

source queries.  Hence (7) has optimal \(N,\epsilon\) dependence, up to
confidence logarithms, for fixed nonzero \(K\).

There is also an exponential lower bound when \(K\) grows.  On
\(X\in\{-1,+1\}\), if \(p=\Pr[X=+1]\), then

\[
 f(K)=e^{-K}+(e^K-e^{-K})p.
 \tag{27}
\]

Around \(p=\Theta(e^{-2K})\), a relative-\(\epsilon\) bracket determines
\(p\) to additive error \(O(\epsilon e^{-2K})\).  Whenever the corresponding
Hamming weights and their separation are at least constant (for example
\(N=\Omega(e^{2K}/\epsilon)\)), the approximate-counting lower bound yields

\[
 \Omega(e^K/\epsilon)
 \tag{28}
\]

quantum queries.  More generally, for \(K\geq1\), the adjacent-weight and
approximate-weight regimes give the conservative envelope

\[
 \Omega\!\left(
 \min\left\{N,\sqrt{N/\epsilon},e^K/\epsilon\right\}
 \right)
 \tag{29}
\]

up to absolute constants and ordinary integrality qualifications.  One way
to see the three regimes is to distinguish adjacent weights near \(N/2\)
when \(N=O(1/\epsilon)\), adjacent weights near
\(\Theta(1/\epsilon)\) when
\(1/\epsilon\lesssim N\lesssim e^{2K}/\epsilon\), and weights near
\(Ne^{-2K}\) separated by
\(\Theta(\epsilon Ne^{-2K})\) above that range.  The standard
two-weight approximate-counting bound gives respectively
\(N\), \(\sqrt{N/\epsilon}\), and \(e^K/\epsilon\).  The tilted-jet upper
bound (TJ3) matches (28), up to confidence logarithms, whenever
\(N=\Omega(e^{2K}/\epsilon)\).  It also recovers the fixed-\(K\)
\(\widetilde\Theta(1/\epsilon)\) frontier.  In the intermediate indexed-
source regime, the present upper \(\min\{N,e^K/\epsilon\}\) and lower
envelope (29) need not match; closing that finite-population interpolation
is the remaining query question.

## Finite arithmetic and scope

Assume here that \(\Lambda,W_0\) and the requested sector bound are rational
or otherwise supplied with certified finite-bit enclosures.  Choose a
rational grid and finite-bit amplitude-estimation outputs.  Reserve a
constant fraction of every analytic width in (15), round the implemented
width down, and round the reported confidence endpoints outwards within the
reserved slack.  This preserves source feasibility and keeps the total
diameter in (13) within its stated analytic budget.

Then (12) is a rational LP.  Its
coefficient bit length includes \(O(d\log G)\) bits for powers of rational
grid points.  Standard rational LP theory returns a rational basic feasible
solution with bit length polynomial in the explicit LP dimensions and input
bit length; the determinant bound gives the same conclusion directly.  At
an extreme point, the normalization row and at most \(d\) independent active
moment rows imply support at most \(d+1\).  A lower rational enclosure for
\(L_*\) and an upper rational enclosure for \(U_*\) preserve (5)--(6).
Thus the public-grid construction closes the finite-bit
atom-extraction caveat of the free-node Hausdorff-moment construction.

For the tilted-jet LP, outward-approximate each coefficient
\(e^{z_jg-|z_j|}g^p\) within a reserved constant fraction of its row's
confidence radius.  The smallest necessary absolute radius is
\(e^{-O(K)}\epsilon^{O(1)}\), so
\(O(K+\log(1/\epsilon)+\log r)\) coefficient bits suffice.  The same precision
also suffices for reversible evaluation of \(W_j(Y)Y^p\) and its controlled
rotation: since \(b_j\geq e^{-2K}\) and (TJ7) gives
\(\xi_p=\Omega_\tau(\epsilon)\), their additive arithmetic errors can be
charged to the reserved \(O(b_j\xi_p)\) confidence slack.  The resulting
rational feasible \(\theta\) is then compressed by a second rational LP
which preserves its first \(d\) ordinary grid moments.  That LP has only
the rational powers \(g^p\), and a basic solution has support at most
\(d+1\).  Hence neither the \(O(Kr)\) tilted rows nor their transcendental
coefficients appear in the delivered conic formulation.

This is polynomial time in the *explicit* LP size
\(G=O(1+K/\epsilon)\), \(d\), and coefficient bit length.  It can therefore be
polynomial in \(1/\epsilon\), not in \(\log(1/\epsilon)\), and is not a
strongly polynomial result.  Near degeneracy can still make floating-point
basis recovery ill-conditioned, so a numerical implementation must return a
rational feasibility certificate or add its residual to (17).

This compiler is distinct from the exact Gaussian-quadrature compiler.  The
Gaussian rule uses at most \(m\) free nodes and exactly matches \(2m-1\)
moments, but stable recovery of those nodes requires a separation condition.
The present rule uses at most \(d+1\) nodes from a public finite grid, only
matches confidence boxes, and stays feasible even when source atoms collide.
Caratheodory/Tchakaloff compression, Taylor approximation, exponential
tilting, and amplitude estimation are established tools.  The potentially
new point is their combination into a robust signed exponential-cone source
compiler with an explicit confidence, support, epigraph, and query ledger.

## Targeted literature screen

A targeted search on 2026-09-04 checked combinations of *tilted moments*,
*Esscher transform*, *Laplace/MGF approximation*, *positive quadrature*,
and *quantum mean estimation*.  The closest ingredients found were:

- [Brassard--Hoyer--Mosca--Tapp](https://arxiv.org/abs/quant-ph/0005055),
  whose amplitude-estimation error bound supplies (TJ9);
- [Curto--Fialkow's duality proof of Tchakaloff's
  theorem](https://arxiv.org/abs/math/0207065), which supplies positive
  finite-moment compression;
- [Montanaro's quantum Monte Carlo
  framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC4614442/), which
  treats quantum mean estimation and relative-variance bounds; and
- the [Quantum Esscher Transform](https://arxiv.org/abs/2401.07561), which
  prepares an exponentially tilted quantum state in a different input and
  output model.

No source found states a classical-output positive atomic compiler with a
uniform relative MGF/epigraph certificate, the local tilted-jet confidence
LP, the post hoc \(O(K+\log(1/\epsilon))\)-atom compression, or the matched
\(\widetilde O(e^K/\epsilon)\) query ledger.  This is evidence against an
obvious collision, not a priority claim; a broader expert literature audit
is still required.

Primary antecedents are the same as in the
[Gaussian-quadrature compiler](2026-09-04-gaussian-quadrature-exponential-cone-compiler.md),
together with Nayak--Wu for approximate-counting lower bounds and the standard
Caratheodory/Tchakaloff finite-moment representation theorem.
