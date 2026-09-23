# Gaussian-quadrature compression of signed exponential recourse

Status: Proved; independently audited; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the approximation and conic statements; moderate on novelty

## Result

Let \(w_i>0\), \(\lambda_i\in[-\Lambda,\Lambda]\), and

\[
 q(U,V)=\sum_{i=1}^N w_iV\exp(\lambda_iU/V)
 \tag{1}
\]

on the homogeneous two-sided sector

\[
 \mathcal S_L=\{(U,V):V\geq0,\ |U|\leq LV\}.
 \tag{2}
\]

At \(U=V=0\), use the closed-perspective value zero.  If \(\Lambda=0\), then
\(q=W_0V\) is linear, so below assume \(\Lambda>0\).  Put
\(W_0=\sum_iw_i\) and \(K=\Lambda L\).  The normalized slopes
\(x_i=\lambda_i/\Lambda\) and probabilities \(w_i/W_0\) define a probability
measure \(\mu\) on \([-1,1]\).

For every integer \(m\geq1\), there is a positive quadrature rule

\[
 Q_m f=\sum_{j=1}^s\omega_jf(\xi_j),
 \qquad
 s\leq\min\{m,N\},\quad
 \omega_j>0,\quad \sum_j\omega_j=1,\quad
 \xi_j\in[-1,1],
 \tag{3}
\]

that is exact for every polynomial of degree at most \(2m-1\).  The nodes lie
in the convex hull \([-1,1]\), not necessarily in the discrete source
support.  If the support of \(\mu\) has more than \(m\) points, this is its
ordinary \(m\)-node Gaussian quadrature rule.  If the support has at most
\(m\) points, take the support itself; then the rule is exact for every
function.

Define the compressed exponential recourse

\[
 q_m(U,V)
 =W_0V\sum_{j=1}^s\omega_j
   \exp(\Lambda\xi_jU/V).
 \tag{4}
\]

Then, uniformly on \(\mathcal S_L\),

\[
 \boxed{
 q_m(U,V)\leq q(U,V)\leq
 (1+\varepsilon_m)q_m(U,V),\qquad
 \varepsilon_m=
 \frac{4^{1-m}e^{2K}K^{2m}}{(2m)!}.}
 \tag{5}
\]

In particular, \(q_m\) is already a certified outer approximation, while
\((1+\varepsilon_m)q_m\) is a certified inner approximation.  No condition
\(\varepsilon_m<1\) is needed.  Thus a source formulation with \(N\)
exponential cones has certified inner and outer approximations using at most
\(m\) exponential cones.  This covers signed slopes and signed ratios, unlike
the positive Taylor-to-power-cone compiler.

## Proof

It is enough to treat the case where the support has more than \(m\) points;
otherwise (4) equals (1).  Write \(z=\Lambda U/V\), so \(|z|\leq K\), and let
\(\pi_m(x)=\prod_{j=1}^m(x-\xi_j)\) be the monic orthogonal polynomial whose
zeros are the Gaussian nodes.  Let \(H_z\) be the degree-\((2m-1)\) Hermite
interpolant to \(f_z(x)=e^{zx}\) at those nodes, matching both values and
first derivatives.  Pointwise Hermite remainder gives

\[
 f_z(x)-H_z(x)
 =\frac{f_z^{(2m)}(\zeta_x)}{(2m)!}\pi_m(x)^2
 \geq0,
 \tag{6}
\]

because \(f_z^{(2m)}(x)=z^{2m}e^{zx}\geq0\), even when \(z<0\).
The quadrature is exact on \(H_z\), and \(Q_mH_z=Q_mf_z\), so

\[
 0\leq
 \int f_z\,d\mu-Q_mf_z
 \leq
 \frac{e^KK^{2m}}{(2m)!}
 \int\pi_m(x)^2\,d\mu(x).
 \tag{7}
\]

The monic orthogonal polynomial minimizes the \(L_2(\mu)\) norm among monic
degree-\(m\) polynomials.  Comparing it to the monic Chebyshev polynomial
\(2^{1-m}T_m\) gives

\[
 \int\pi_m(x)^2\,d\mu(x)
 \leq\|2^{1-m}T_m\|_{\infty,[-1,1]}^2
 \leq4^{1-m}.
 \tag{8}
\]

Finally, both the source and quadrature measures are supported on
\([-1,1]\), so

\[
 \int e^{zx}\,d\mu(x)\geq e^{-K},
 \qquad
 Q_m(e^{z\cdot})\geq e^{-K}.
 \tag{9}
\]

Multiplying (7) by \(W_0V\), using (8), and dividing by the second lower
bound in (9) proves (5).  The case \(V=0\) follows from the declared
closed-perspective value.  When \(K=0\), the sector forces \(U=0\) and the
rule is exact.

Using \((2m)!\geq(2m/e)^{2m}\),

\[
 \varepsilon_m
 \leq4e^{2K}\left(\frac{eK}{4m}\right)^{2m}.
 \tag{10}
\]

For example, it suffices that

\[
 m\geq eK,\qquad
 m\geq\log_{16}(4e^{2K}/\epsilon)
 \tag{11}
\]

to ensure \(\varepsilon_m\leq\epsilon\).  Hence

\[
 m=O(K+\log(1/\epsilon))
 \tag{12}
\]

always suffices.  For fixed \(K>0\), Stirling inversion improves this to

\[
 m=O\!\left(
 \frac{\log(1/\epsilon)}{\log\log(1/\epsilon)}
 \right).
 \tag{13}
\]

The companion
[support lower bound](2026-09-04-exponential-mixture-support-lower-bound.md)
shows that this fixed-\(K\) order is worst-case optimal against every positive
atomic approximation whose nodes remain in the slope interval.  In fact the
minimax logarithmic error is

\[
 -\log \mathcal E_m(K)=2m\log m+O_K(m),
\]

so the leading inversion is
\((1/2+o(1))\log(1/\epsilon)/\log\log(1/\epsilon)\).
The same leading support law remains necessary even if a direct positive
mixture may use arbitrary real nodes; the audited lower bound then has the
slightly weaker remainder
\(-\log\mathcal E_m^{\mathbb R}(K)=2m\log m+O_K(m\log\log m)\).
For in-range nodes, more generally, if \(K=K_m\) and \(m/K_m\to\infty\),
the companion lower bound and the Gaussian rule together give

\[
 -\log\mathcal E_m(K_m)
 =2m\log(m/K_m)+O(m+K_m).
\]

Thus, writing \(L_\epsilon=\log(1/\epsilon)\), whenever
\(L_\epsilon/K\to\infty\) and
\(L_\epsilon/W(L_\epsilon/(2K))\to\infty\), the worst-case optimal support
size for a direct positive mixture is

\[
 m_*(\epsilon,K)
 =(1+o(1))
 \frac{L_\epsilon}{2W(L_\epsilon/(2K))}.
\]

## Conic and barrier consequences

Introduce \(h_j\) with

\[
 h_j\geq V\exp(\Lambda\xi_jU/V)
 \]

and aggregate \(t\geq W_0\sum_j\omega_jh_j\) through a partial-sum chain.
Each nonconstant local epigraph is one three-dimensional exponential cone;
a zero node contributes only a linear term.  The unscaled last inequality
gives the outer approximation in (5), and scaling it by
\(1+\varepsilon_m\) gives the inner approximation.
The epigraph containments are

\[
 \operatorname{epi}_{\mathcal S_L}
 \!\left((1+\varepsilon_m)q_m\right)
 \subseteq
 \operatorname{epi}_{\mathcal S_L}(q)
 \subseteq\operatorname{epi}_{\mathcal S_L}(q_m).
 \tag{14}
\]

For minimizing the epigraph coordinate over any common feasible set in
\(\mathcal S_L\), if \(\operatorname{OPT}_m\) denotes the optimum with
\(q_m\), then

\[
 \operatorname{OPT}_m\leq\operatorname{OPT}
 \leq(1+\varepsilon_m)\operatorname{OPT}_m.
\]

This is a relative statement when the optimum is positive.  A zero optimum
and objectives other than the epigraph coordinate require their own error
interpretation.

For the displayed product formulations, parameter-three exponential-cone
barriers give

\[
 \nu_{\rm source}=3N+O(1),\qquad
 \nu_{\rm quadrature}\leq3m+O(1).
 \tag{15}
\]

Under the initialization, neighborhood, and inexact-Newton hypotheses of a
generic nonsymmetric primal-barrier IPM, the outer-iteration estimate becomes

\[
 O\!\left(
 \sqrt{K+\log(1/\epsilon)}
 \log(1/\varepsilon_{\rm opt})
 \right)
 \tag{16}
\]

using the simple choice (12), with the sharper fixed-\(K\) value from (13).
This is a formulation-dependent iteration statement, not an intrinsic barrier
lower bound or an initialization-free runtime.

The copy-and-consensus path for \((U,V)\), aligned with the partial-sum chain,
has constant scalar incidence and scalar KKT treewidth \(O(1)\).  Subject to
stable bounded-treewidth factorization, a full classical Newton direction
therefore costs \(\widetilde O(m)\) arithmetic.  Full classical output already
costs \(\Omega(m)\), so this compression does not create a reason to use a
QLSA for the Newton stage.

## Exact construction and a robust approximate-moment variant

In exact arithmetic, the nodes and weights can be recovered from the moments

\[
 \int x^r\,d\mu(x),\qquad r=0,\ldots,2m-1,
 \tag{17}
\]

through the orthogonal-polynomial/Jacobi-matrix construction.  A singular
Hankel moment matrix corresponds to a smaller support and should be deflated,
not inverted.

This exact summary does not by itself give a sublinear source-query
algorithm.  At precision below \(1/(3N)\), its first moment already reveals
the exact Hamming weight on the subclass \(x_i\in\{0,1\}\), and parity gives
an \(\Omega(N)\) quantum-query lower bound.  Direct approximate
moment-to-node recovery also has no uniform condition bound: nearly
colliding support points make the Hankel/Jacobi reconstruction arbitrarily
ill-conditioned.

There is, however, a functionally robust alternative that does not try to
recover the true nodes.  Set \(D=2m-1\) and let

\[
 \mathcal H_D=
 \left\{y\in\mathbb R^{D+1}:
 y_r=\int_{-1}^1x^r\,d\nu(x),\
 \nu\ \hbox{a probability measure}\right\}
 \tag{18}
\]

be the truncated Hausdorff moment cone slice.  Estimate the source moments
\(M_r=\int x^r\,d\mu\) and obtain simultaneous intervals
\([c_r-\eta_r,c_r+\eta_r]\).  On their success event, the convex feasibility
problem

\[
 \widehat y\in\mathcal H_D,\qquad
 |\widehat y_r-c_r|\leq\eta_r,\qquad r=1,\ldots,D
 \tag{19}
\]

is nonempty because the true moment vector is feasible.  Choose any feasible
\(\widehat y\), any representing measure, and then its \(m\)-node Gaussian
rule.  The resulting positive atomic measure \(\widehat\nu\) has at most
\(m\) nodes and moments \(\widehat y_0,\ldots,\widehat y_D\).  Thus this
procedure never needs the approximate nodes to be close to the true
Gaussian nodes.

To allocate the source-query accuracy, put

\[
 a_r=\frac{K^r}{r!},\qquad
 S_D(K)=\sum_{r=1}^{D}\sqrt{a_r},\qquad
 \eta_r=\frac{\delta e^{-K}}
 {2S_D(K)\sqrt{a_r}}.
 \tag{20}
\]

When \(\eta_r\geq1\), use the trivial interval \([-1,1]\), drop that box
constraint from (19), and make no query.
Since both the true and chosen moments then lie in that interval, the bound
\(|M_r-\widehat y_r|\leq2\eta_r\) still holds.  For
\(|z|\leq K\), comparison through the degree-\(D\) Taylor polynomial gives

\[
\begin{aligned}
 \left|\int e^{zx}\,d\mu-\int e^{zx}\,d\widehat\nu\right|
 &\leq
 \sum_{r=1}^{D}\frac{K^r}{r!}|M_r-\widehat y_r|
 +\frac{2e^KK^{D+1}}{(D+1)!}\\
 &\leq
 \delta e^{-K}+\frac{2e^KK^{2m}}{(2m)!}.
\end{aligned}
\tag{21}
\]

Define

\[
 \rho_m=\delta+\frac{2e^{2K}K^{2m}}{(2m)!}.
 \tag{22}
\]

Since both the source and atomic moment-generating functions are at least
\(e^{-K}\), the atomic exponential recourse

\[
 \widehat q_m(U,V)
 =W_0V\int e^{\Lambda(U/V)x}\,d\widehat\nu(x)
\]

satisfies, on the simultaneous-success event,

\[
 |\widehat q_m-q|\leq\rho_m\min\{q,\widehat q_m\}.
 \tag{23}
\]

Certified conic models therefore follow directly from

\[
 \frac{\widehat q_m}{1+\rho_m}
 \leq q\leq
 (1+\rho_m)\widehat q_m.
 \tag{24}
\]

Thus \(\widehat q_m/(1+\rho_m)\) is the outer relaxation and
\((1+\rho_m)\widehat q_m\) is the inner restriction.  These certificates hold
with the declared simultaneous confidence probability; they are not
deterministic statements about a failed source-estimation event.

Assume \(W_0\) is known, a coherent weighted-sampling oracle prepares
probabilities \(w_i/W_0\), and a value oracle returns \(x_i\).  Estimating the
signed variable \(x^r\in[-1,1]\) by shifting it to \([0,1]\), amplitude
estimation and (20) use

\[
 \boxed{
 \widetilde O\!\left(
 \min\left\{N,\frac{e^KS_D(K)^2}{\delta}\right\}
 \right)}
 \tag{25}
\]

weighted source queries.  The \(N\) branch uses indexed access and explicit
summation.  Since

\[
 S_D(K)^2\leq S_\infty(K)^2
 =\Theta(e^K\sqrt K)\qquad(K\geq1),
\]

the second branch is
\(\widetilde O(e^{2K}\sqrt K/\delta)\), and for fixed \(K\) it is simply
\(\widetilde O(1/\delta)\), independent of \(m\).

The fixed-\(K\) dependence is optimal up to confidence logarithms for any
classical-output compiler that supplies an evaluable uniform relative
bracket.  On the subclass \(x_i\in\{0,1\}\), evaluation at \(U/V=L\) recovers
the bit mean from \(q/(W_0V)=1+(e^K-1)\mu\).  Approximate-counting lower bounds
therefore give

\[
 \Omega(\min\{N,1/\delta\})\ \hbox{quantum queries},\qquad
 \Omega(\min\{N,1/\delta^2\})\ \hbox{randomized queries}.
 \tag{26}
\]

For example, take fixed nonzero \(K\), choose both the moment and Taylor
widths as \(\Theta(N^{-1/2})\), and attach the recourse through
\((U,V,t)\) to a fixed-size or bounded-treewidth host model.  Then

\[
 m=O(\log N/\log\log N),
\]

the robust compiler uses \(\widetilde O(\sqrt N)\) quantum source queries,
and the compiled barrier has parameter \(O(\log N/\log\log N)\) rather than
\(\Theta(N)\).  Stable classical bounded-treewidth Newton solves add
\(\widetilde O(m^{3/2}\log(1/\varepsilon_{\rm opt}))\) arithmetic over the
generic IPM trajectory.  Whenever this last term is
\(\widetilde O(\sqrt N)\), (26) gives a quadratic oracle separation, up to
logarithms, between the hybrid quantum-preprocessing/classical-IPM pipeline
and any randomized certified source compiler.  This is not a QLSA
speedup.

This is a source-query statement in an exact-real/classical-postprocessing
model.  The truncated Hausdorff moment cone has standard Hankel
semidefinite descriptions, and an output atomic rule can be checked directly
for positive weights, nodes in \([-1,1]\), and its moment residuals.
Nevertheless, no strongly polynomial or uniform finite-bit bound for solving
(19) and extracting the atoms is claimed.  Any numerical residual must be
added to the weighted sum in (21).  Preparing the coherent sampling oracle,
bounded-value arithmetic, and outputting the \(O(m)\) classical nodes and
weights are not free.

Equations (5)--(16) give deterministic exact-moment compression; equations
(18)--(26) give the robust approximate-moment source-query variant.

## Novelty boundary

Gaussian quadrature, positive weights, \(2m-1\) polynomial exactness, and
one-sided error for functions with nonnegative \(2m\)-th derivative are
classical.  Discrete Gaussian summation is also established.  More
importantly, quadrature and moment-matching scenario compression are already
used in stochastic programming, with epi-convergence and smooth-integrand
rates.  The potentially new contribution here is therefore limited to the
specific homogeneous exponential-perspective sandwich (5), its exact
exponential-cone inner and outer models (14), and the barrier and sparse-KKT
ledger.  The confidence-box/Hausdorff-moment construction (18)--(25) also
appears to give a new robust quantum source compiler for signed slopes.  A
targeted search found no paper stating either full combination, but priority
is not guaranteed.

This result is distinct from:

- approximating each individual exponential cone by SOC or polyhedral lifts;
- the positive-slope Taylor compiler, which replaces the source by power
  cones and admits a source-query speedup; and
- exact finite source compilers, which are obstructed for unrestricted slope
  families.

Primary antecedents:

- [Monien, *Gaussian Summation: An Exponentially Converging Summation
  Scheme*](https://arxiv.org/abs/math/0611057), for Gaussian quadrature with
  respect to discrete measures.
- [Pennanen--Koivu, *Epi-convergent discretizations of stochastic programs
  via integration quadratures*](https://doi.org/10.1007/s00211-004-0571-4),
  for quadrature scenario approximations and epi-convergence in stochastic
  programming.
- [Mehrotra--Papp, *Generating Moment Matching Scenarios Using Optimization
  Techniques*](https://doi.org/10.1137/110858082), for moment-matching
  scenario compression, including rates for smooth integrands.
- [Dao--De Sa--Ré, *Gaussian Quadrature for Kernel
  Features*](https://arxiv.org/abs/1709.02605), for polynomially exact
  quadrature and exponential-integrand bounds in a different application.
- [Nayak--Wu, *The quantum query complexity of approximating the median and
  related statistics*](https://arxiv.org/abs/quant-ph/9804066), for the
  approximate-mean/counting lower bound in (26).
- [Brassard--Høyer--Mosca--Tapp, *Quantum Amplitude Amplification and
  Estimation*](https://arxiv.org/abs/quant-ph/0005055), for the amplitude
  estimation primitive used in (25).
- [Ye--Xie, *Second-Order Conic and Polyhedral Approximations of the
  Exponential Cone*](https://arxiv.org/abs/2106.09123), for approximation of
  individual exponential-cone constraints.
- [Papp--Varga, *Interior-point algorithms with full Newton steps for
  nonsymmetric convex conic optimization*](https://arxiv.org/abs/2502.16020),
  for the generic primal-barrier iteration framework used in (16).
