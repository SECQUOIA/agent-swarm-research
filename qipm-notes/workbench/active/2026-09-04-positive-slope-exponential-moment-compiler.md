# A moment-to-power-cone compiler for positive-slope exponential recourse

Status: Proved; independently audited; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the mathematics; moderate on novelty and impact

## Setting

Let \(w_i>0\), \(0\leq\lambda_i\leq\Lambda\), and consider the homogeneous
exponential-recourse function

\[
 q(U,V)=\sum_{i=1}^N w_iV\exp(\lambda_iU/V).
 \tag{1}
\]

Restrict the common features to the declared conic sector

\[
 \mathcal S_L=\{(U,V):V\geq0,\ 0\leq U\leq LV\}.
 \tag{2}
\]

At the only point of this sector with \(V=0\), namely \(U=V=0\), define
both \(q\) and \(q_R\) by their closed-perspective value zero.

The ratio restriction is essential.  It is a homogeneous linear restriction,
not a compactness assumption on the scale of \((U,V)\).  Put \(K=\Lambda L\).
If \(K=0\), because either \(\Lambda=0\) or \(L=0\), then \(q=W_0V\) on the
declared sector and is already linear; below assume \(K>0\).

The usual formulation of \(t\geq q(U,V)\) has one exponential-cone factor per
scenario.  The result below replaces those \(N\) factors by a number of
three-dimensional power cones depending on \(K\) and the requested relative
accuracy, but not on \(N\).

## Certified Taylor-moment sandwich

For an integer \(R\geq2\), define the source moments

\[
 W_p=\sum_{i=1}^Nw_i\lambda_i^p,
 \qquad p=0,\ldots,R-1,
 \tag{3}
\]

and the homogeneous truncated-moment function

\[
 q_R(U,V)
 =\sum_{p=0}^{R-1}\frac{W_p}{p!}U^pV^{1-p}.
 \tag{4}
\]

For \(z\geq0\), write \(P_{R-1}(z)=\sum_{p=0}^{R-1}z^p/p!\).  The exact
identity

\[
 e^{-z}P_{R-1}(z)=\Pr\{X_z\leq R-1\},
 \qquad X_z\sim\operatorname{Poisson}(z),
\]

and the Chernoff bound, for \(R\geq z\), give

\[
 0\leq1-e^{-z}P_{R-1}(z)
 =\Pr\{X_z\geq R\}
 \leq \left(\frac{ez}{R}\right)^R.
 \tag{5}
\]

Consequently, for \(0<\epsilon<1\), it suffices to take any \(R\geq K\)
satisfying

\[
 \left(\frac{eK}{R}\right)^R\leq\epsilon.
 \tag{6}
\]

For example, the fully explicit choice

\[
 R\geq
 \max\left\{2eK,\ \log_2(1/\epsilon)\right\}
\]

ensures

\[
 (1-\epsilon)e^z\leq P_{R-1}(z)\leq e^z
 \qquad(0\leq z\leq K).
\]

Applying this term by term to (1) yields the global-on-\(\mathcal S_L\)
multiplicative sandwich

\[
 \boxed{(1-\epsilon)q(U,V)\leq q_R(U,V)\leq q(U,V).}
 \tag{7}
\]

Equivalently, with

\[
 q_-(U,V)=q_R(U,V),\qquad
 q_+(U,V)=\frac{q_R(U,V)}{1-\epsilon},
\]

the epigraphs satisfy

\[
 \boxed{
 \operatorname{epi}_{\mathcal S_L}(q_+)
 \subseteq
 \operatorname{epi}_{\mathcal S_L}(q)
 \subseteq
 \operatorname{epi}_{\mathcal S_L}(q_-).}
 \tag{8}
\]

Thus \(q_+\) gives a certified inner restriction and \(q_-\) a certified outer
relaxation.  Both use the same \(R\) source moments.  For fixed \(K\), the
least \(R\) satisfying (6) is
\[
 O\!\left(\frac{\log(1/\epsilon)}
                 {\log\log(1/\epsilon)}\right)
\]
as \(\epsilon\to0\).  The simpler uniform choice displayed above gives

\[
 R=O(K+\log(1/\epsilon))
 \tag{9}
\]

in general.  Sharper Poisson-tail inversion can improve constants and the
transition regime but is not needed for the theorem.

For the displayed Taylor-moment construction this fixed-\(K\) order is
asymptotically tight.  At the single endpoint \(z=K>0\), its relative error
is a Poisson tail and is at least its first omitted mass,

\[
 1-e^{-K}P_{R-1}(K)\geq e^{-K}\frac{K^R}{R!}
 \geq e^{-K}\left(\frac KR\right)^R.
\]

Therefore error at most \(\epsilon\) requires
\(R\log(R/K)\geq\log(1/\epsilon)-K\), which for fixed \(K\) implies
\(R=\Omega(\log(1/\epsilon)/\log\log(1/\epsilon))\).  Together with (5),
this matches the stated upper order.  This is not a lower bound against
arbitrary rational or non-moment conic approximations.

For the pure problem of minimizing the epigraph coordinate over any common
feasible set contained in \(\mathcal S_L\), (7) gives the optimal-value
sandwich

\[
 (1-\epsilon)\operatorname{OPT}
 \leq\operatorname{OPT}_-
 \leq\operatorname{OPT}
 \leq\operatorname{OPT}_+
 \leq\frac{\operatorname{OPT}}{1-\epsilon}.
\]

More general objectives need their own error transfer.
When the optimum is positive this is a relative guarantee; for a zero optimum
the displayed multiplicative inequalities remain true but do not provide a
meaningful relative-error certificate.

## Exact power-cone representation of the approximants

The terms with \(p=0,1\) in (4) are linear.  For every \(p\geq2\), introduce
\(s_p\) and impose

\[
 s_p\geq\frac{U^p}{V^{p-1}}.
 \tag{10}
\]

This is exactly one ordinary three-dimensional power-cone constraint:

\[
 (s_p,V,U)\in K_{1/p}
 :=\{(a,b,c):a,b\geq0,\ a^{1/p}b^{1-1/p}\geq|c|\},
 \tag{11}
\]

together with \(U\geq0\).  Since every coefficient \(W_p/p!\) is
nonnegative, projection of

\[
 t\geq W_0V+W_1U+
 \sum_{p=2}^{R-1}\frac{W_p}{p!}s_p
 \tag{12}
\]

and (10) is precisely \(t\geq q_R(U,V)\).  Scaling the right-hand side of
(12) by \(1/(1-\epsilon)\) represents the inner approximation.

Hence (8) replaces \(N\) exponential cones by \(R-2\) power cones and a
constant number of linear inequalities.  Using the parameter-three
Roy--Xiao barrier

\[
 -\log(x^{2\alpha}y^{2(1-\alpha)}-z^2)
 -(1-\alpha)\log x-\alpha\log y
\]

for each three-dimensional power cone gives the explicit
comparison

\[
 \nu_{\rm original}=3N+O(1),\qquad
 \nu_{\rm compiled}\leq3R+O(1)
 =O(K+\log(1/\epsilon)).
 \tag{13}
\]

These are parameters of the displayed product formulations, not intrinsic
lower bounds on all barriers for their low-dimensional projections.  Generic
primal-barrier nonsymmetric IPMs therefore reduce the outer-iteration bound
of this explicit formulation from
\(O(\sqrt N\log(1/\varepsilon_{\rm opt}))\) to

\[
 O\!\left(
 \sqrt{K+\log(1/\epsilon)}
 \log(1/\varepsilon_{\rm opt})
 \right),
 \tag{14}
\]

in addition to the controlled modeling error \(\epsilon\).
This uses the feasibility, initialization, neighborhood, and inexact-Newton
conditions of the chosen generic nonsymmetric IPM; (14) is not an
initialization-free end-to-end runtime.

Equation (14) is only an iteration statement.  The smallest power exponent in
the compiled lift is \(1/(R-1)\), and coefficient dynamic range and the
assembled KKT condition number are not controlled by the barrier parameter.
The small exponent alone does not force bad local conditioning: at normalized
coordinates \(x=y=1\) and normalized power-cone slack
\(|z|\leq\theta<1\), the standard barrier Hessian depends continuously on
\(\alpha\in[0,1]\) and remains positive definite even at the limiting
\(\alpha=0,1\) product cones, so its spectrum lies in
\([c_\theta,C_\theta]\) uniformly in \(\alpha\).  There is no corresponding
global bound when coordinate ratios or boundary proximity are unrestricted.
Any QLS-based runtime must therefore retain the actual assembled condition
number and the arithmetic precision needed for \(W_p/p!\).

There is also an exact metric statement for these explicit barriers.  Every
\(\nu\)-logarithmically homogeneous barrier satisfies
\(z^\top\nabla^2F(z)z=\nu\).  Therefore a strict radial segment between
scales \(a_0,a_1\) has length

\[
 \sqrt\nu\,|\log(a_1/a_0)|.
\]

For the displayed natural and compiled lifts the radial-length ratio is
\(\Theta(\sqrt{N/R})\).  This is a property of these barriers, not a lower
bound on the central path or on arbitrary IPMs.

## Sparsity and Newton structure

A path of copies of \((U,V)\), with two-sparse consensus equalities, and a
matching partial-sum chain for (12) make both the original \(N\)-factor lift
and the compiled \(R\)-factor lift have constant scalar incidence and scalar
KKT treewidth \(O(1)\).  Align the two chains so that a constant-size
tree-decomposition bag contains each stage's copy, partial-sum variable, and
adjacent consensus multipliers.  In particular, the final epigraph sum is not
left as one dense row.  The compilation therefore reduces the linear-system
dimension and number of local barrier blocks without hiding a dense star in
the lift.

This structure points to a classical, not quantum, Newton solve after the
quantum source compilation.  Under stable bounded-treewidth factorization and
the usual bounded-precision assumptions, a full Newton direction for the
compiled chain costs \(\widetilde O(R)\) classical arithmetic per iteration.
Writing all lift coordinates already costs \(\Omega(R)\).  Thus a QLSA does
not improve the full-classical-output Newton stage of this formulation.  The
[bounded-treewidth no-advantage note](2026-09-04-bounded-treewidth-full-output-no-advantage.md)
states the general sequence-level version and its numerical hypotheses.

There is also an exact projected Hessian identity.  Since
\(q_R(U,V)=VP_{R-1}^{W}(U/V)\) is a scalar perspective, putting \(r=U/V\)
gives

\[
 \nabla^2q_R(U,V)
 =\frac{(P_{R-1}^{W})''(r)}{V}
 \begin{pmatrix}1\\-r\end{pmatrix}
 \begin{pmatrix}1&-r\end{pmatrix},
 \tag{15}
\]

where

\[
 P_{R-1}^{W}(r)=\sum_{p=0}^{R-1}\frac{W_p}{p!}r^p.
\]

Thus the projected recourse Hessian has rank at most one, and its coefficient
is evaluated from the cached moments in \(O(R)\) arithmetic.  This rank-one
fact is elementary for any twice differentiable one-homogeneous function of
two variables; it is not claimed as a new power-cone Hessian result.

## Source-query ledger and safe approximate moments

Exact moments still require reading the source in the worst case.  For
example, take uniform weights and \(\lambda_i=z_i\in\{0,1\}\).  Then
\(W_1/W_0=|z|/N\), so error below \(1/(3N)\) recovers the exact Hamming weight
by rounding and hence computes parity.  Bounded-error quantum compilation at
that precision needs \(\Omega(N)\) source queries.  Barrier compression is
not free data loading.

Approximate moments are nevertheless safe in this positive regime.  Suppose
coherent estimation returns simultaneous confidence intervals

\[
 W_p^-\leq W_p\leq W_p^+.
\]

Replace a negative reported lower endpoint by
\(\max\{0,W_p^-\}\).  All monomials in (4) are nonnegative on
\(\mathcal S_L\), so these clipped lower endpoints give a certified outer
epigraph relaxation.  Upper endpoints, followed by the factor
\(1/(1-\epsilon)\) accounting for Taylor truncation, give a certified inner
restriction.  There is no cancellation or exponent-estimation crossing.

More precisely, fix \(0<\delta<1\), assume \(W_0=\sum_iw_i\) is known, and
assume the coherent sampling
oracle prepares indices with probabilities \(w_i/W_0\).  The normalized
quantities to estimate are

\[
 M_p=\frac{W_p}{W_0\Lambda^p}
 =\mathbb E\!\left[(\lambda/\Lambda)^p\right]\in[0,1].
\]

There is no need to pay uniformly for moments whose Taylor coefficients are
tiny.  Put

\[
 a_p=\frac{K^p}{p!},\qquad
 S_R(K)=\sum_{p=1}^{R-1}\sqrt{a_p}.
 \tag{16}
\]

For a requested normalized half-width \(\delta\), estimate \(M_p\) to

\[
 \eta_p=\frac{\delta}{S_R(K)\sqrt{a_p}}.
 \tag{17}
\]

If \(\eta_p\geq1\), use the trivial interval \([0,1]\) and make no query.
Otherwise use amplitude estimation, with the failure probability divided
among the active moments.  On the simultaneous-success event,

\[
 \sum_{p=1}^{R-1}a_p\eta_p\leq\delta.
 \tag{18}
\]

Indeed, at \(y=\Lambda U/V\in[0,K]\), the normalized polynomial is
\(q_R/(W_0V)=\sum_p M_py^p/p!\), so (18) bounds the error of either endpoint
by \(\delta\).  Since \(q\geq W_0V\), before applying the Taylor safety
factor this is also an additional relative endpoint error of at most
\(\delta\).  Combining it with (7), if
\(\widehat q_R^-\leq q_R\leq\widehat q_R^+\) are the moment endpoint
polynomials, then

\[
 q-\widehat q_R^-\leq(\epsilon+\delta)q,
\]

while the certified inner function obeys

\[
 q\leq\frac{\widehat q_R^+}{1-\epsilon}
 \leq\frac{1+\delta}{1-\epsilon}q.
\]

Thus its relative excess is at most
\((\epsilon+\delta)/(1-\epsilon)\).  Choosing both the Taylor and moment
tolerances of the same order gives a total relative bracket of that order.
The total number of weighted source queries is

\[
 \boxed{
 \widetilde O\!\left(
 \min\left\{N,\ \frac{S_R(K)^2}{\delta}\right\}
 \right).}
 \tag{19}
\]

The logarithm hidden here is only the confidence amplification needed to
output all active classical intervals.  To verify (19), sum the safe
\(O(1/\eta_p)\) amplitude-estimation costs:

\[
 \sum_{p:\eta_p<1}\frac1{\eta_p}
 \leq \frac{S_R(K)}{\delta}\sum_{p=1}^{R-1}\sqrt{a_p}
 =\frac{S_R(K)^2}{\delta}.
\]

For every fixed \(K\),

\[
 S_R(K)\leq S_\infty(K)
 =\sum_{p\geq1}\sqrt{K^p/p!}<\infty,
\]

so the query count is \(\widetilde O(\min\{N,1/\delta\})\), independent of
the truncation degree.  The dependence on a growing sector width is also
explicit:

\[
 S_\infty(K)^2=\Theta(e^K\sqrt K)\qquad(K\geq1).
 \tag{19a}
\]

One short proof writes \(K^p/p!=e^K\pi_p\), where \(\pi\) is the
\(\operatorname{Poisson}(K)\) mass function.  With
\(b_p=1+(p-K)^2/K\), Cauchy--Schwarz gives

\[
 \left(\sum_p\sqrt{\pi_p}\right)^2
 \leq\left(\sum_p\pi_pb_p\right)\left(\sum_p b_p^{-1}\right)
 =O(\sqrt K).
\]

Conversely,
\((\sum_p\sqrt{\pi_p})^2\geq1/\max_p\pi_p=\Omega(\sqrt K)\)
by the standard Stirling bound on the largest Poisson mass.  Omitting the
\(p=0\) term does not change this order for \(K\geq1\).

This improvement uses separate amplitude estimates
with optimized accuracies; it does not require a joint multivariate mean
estimator.  The \(N\) branch assumes indexed source-query access and explicit
summation, not sampling access alone.  A classical sample reveals all powers
of one sampled slope, so the matched randomized baseline must reuse samples
across moments rather than pay \(R\) independent times.  Full explicit source
loading remains \(\Theta(N)\).

For example, take fixed nonzero \(K=O(1)\), set both the Taylor and moment
tolerances to \(\Theta(N^{-1/2})\), and hence request total modeling width
\(\Theta(N^{-1/2})\).  Then one may take
\(R=O(\log N/\log\log N)\), the optimized source-query upper bound is
\(\widetilde O(\sqrt N)\), and the explicit compiled barrier
has parameter \(O(\log N/\log\log N)\), versus parameter \(\Theta(N)\) for
the source formulation.  Approximate-mean lower bounds already give
\(\Omega(\sqrt N)\) quantum and \(\Omega(N)\) randomized queries from the
first moment.  Thus the source-query dependence is optimal up to confidence
logarithms in this regime.  More generally, on the binary-slope subclass
\(\lambda_i\in\{0,\Lambda\}\), evaluation at \(U/V=L\) gives

\[
 \frac{q(U,V)}{W_0V}=1+(e^K-1)\mu,
 \qquad
 \mu=\frac{1}{N}\sum_i\mathbf 1\{\lambda_i=\Lambda\}.
 \tag{20}
\]

Consequently, any compiler that outputs an evaluable uniform relative
bracket of width \(O_K(\delta)\) also estimates the mean of \(N\) bits to
additive error \(O_K(\delta)\).  Standard approximate-counting lower bounds
give

\[
 \Omega\!\left(\min\{N,1/\delta\}\right)
 \quad\hbox{quantum queries},
 \qquad
 \Omega\!\left(\min\{N,1/\delta^2\}\right)
 \quad\hbox{randomized queries}.
 \tag{21}
\]

For fixed nonzero \(K\), (19) therefore has optimal \(N,\delta\) dependence,
up to confidence logarithms, among such classical-output certified
compilers.  This corollary concerns source queries and explicit barrier
parameters; it does not make linear solves, iterate output, or QRAM loading
free.

Combining the two ledgers gives a clean hybrid regime.  Take fixed nonzero
\(K\), Taylor and moment widths both \(\Theta(N^{-1/2})\), and a fixed-size or
bounded-treewidth host model attached through \((U,V,t)\).  Then

\[
 R=O(\log N/\log\log N),
\]

quantum preprocessing uses \(\widetilde O(\sqrt N)\) source queries, and a
classical sparse IPM uses

\[
 \widetilde O\!\left(
 R^{3/2}\log(1/\varepsilon_{\rm opt})
 \right)
\]

post-compilation arithmetic under the assumptions above.  The corresponding
certified source summary requires \(\Omega(N)\) randomized source queries by
(21).  Hence, whenever
\(R^{3/2}\log(1/\varepsilon_{\rm opt})=\widetilde O(\sqrt N)\), the compiler
yields a quadratic oracle separation, up to logarithms, for the whole hybrid
pipeline.  This is a quantum data-reduction advantage
followed by a classical IPM, not evidence for a quantum Newton-system
advantage.

The assumptions behind (19) are substantive: the algorithm needs coherent
weighted sampling, bounded-value arithmetic for \(\lambda_i\), and classical
output of the \(R\) confidence intervals.  Preparing that oracle or writing a
dense source table is not free.

## Scope and novelty boundary

The positivity assumptions \(U/V\geq0\) and \(\lambda_i\geq0\) make every
Taylor coefficient and monomial nonnegative.  With signed slopes or ratios,
a Taylor truncation can lose both one-sidedness and the simple convex
power-cone representation.  Without the sector bound, no finite truncation
is uniformly relatively accurate.  The result is therefore aimed at
positive-slope posynomial, risk, and exponential-recourse models, not at all
exponential-cone programs.

Taylor and repeated-squaring approximations of a single exponential cone are
established.  In particular, Ye and Xie give SOC and polyhedral approximations
of individual exponential cones, including Taylor-based constructions.
Polynomial approximation of sums of exponentials is also classical.  The
[dilation-rank note](2026-09-04-dilation-rank-perspective-compilers.md)
proves that arbitrary exponential slopes have no fixed-dimensional *exact*
continuous source summary.

A targeted search found no source that combines the cross-scenario moment
summary (3), the exact power-cone representation (10)--(12), the certified
conic sandwich (8), and the barrier/source-query ledger (13)--(21).  That
combination is the apparent novelty; priority is not guaranteed.  This is an
approximate compiler theorem, not a new approximation of the scalar
exponential function itself.

Primary antecedents:

- [Ye--Xie, *Second-Order Conic and Polyhedral Approximations of the
  Exponential Cone*](https://arxiv.org/abs/2106.09123).
- [Fawzi--Saunderson, *Optimal self-concordant barriers for quantum relative
  entropies*](https://arxiv.org/abs/2205.04581), for the broader perspective
  barrier context rather than this approximation.
- [Papp--Varga, *Interior-point algorithms with full Newton steps for
  nonsymmetric convex conic optimization*](https://arxiv.org/abs/2502.16020),
  for the generic \(O(\sqrt\nu\log(1/\varepsilon))\) primal-barrier
  iteration framework used in (14).
- [Roy--Xiao, *On self-concordant barriers for generalized power
  cones*](https://www.microsoft.com/en-us/research/wp-content/uploads/2018/01/powercones-5a71024933c4b.pdf),
  for the parameter-three barrier used for every three-dimensional power
  factor.  A more familiar natural barrier has parameter four, so the choice
  matters in the constant in (13).
- [Nayak--Wu, *The quantum query complexity of approximating the median and
  related statistics*](https://arxiv.org/abs/quant-ph/9804066), for the
  quantum approximate-mean/counting lower bound used in (21).  The randomized
  branch is the standard Bernoulli mean-estimation lower bound (or its
  finite-population version via Yao's principle).
- [Brassard--Høyer--Mosca--Tapp, *Quantum Amplitude Amplification and
  Estimation*](https://arxiv.org/abs/quant-ph/0005055), for the amplitude
  estimation primitive and approximate-counting upper bounds.
