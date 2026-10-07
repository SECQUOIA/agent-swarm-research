# Exact screening and percolation: quantitative review

This note establishes an exact algorithm when the entire potentially active set is sparse. It does not establish an algorithm for a broad penalty law centered near zero or near the activation thresholds. In those regimes, many forced-active variables can remain, and eliminating them can create a dense Schur complement.

The positive result is screening followed by site percolation and component enumeration. Its useful feature is that the original graph can have unbounded treewidth. Its mathematical novelty appears modest; it should not be presented as resolving the stronger influence-decay proposal.

## Model and a safe screen

Consider

\[
 \min_{x\in\mathbb R^n,\ z\in\{0,1\}^n}
 x^TQx-2b^Tx+\sum_i\lambda_i z_i,
 \qquad x_i(1-z_i)=0,
\]

where \(Q\) is symmetric positive definite. Put an edge \(ij\) in \(G\) exactly when \(Q_{ij}\ne0\), and assume maximum degree at most \(\Delta\).

Suppose a deterministic nonnegative vector \(r\) satisfies

\[
 |(Q_{SS}^{-1}b_S)_i|\le r_i
 \quad\text{for every }S\subseteq[n]\text{ and }i\in S.
\]

Then every optimal selected set is contained in

\[
 U=\{i:\lambda_i\le T_i\},\qquad T_i=Q_{ii}r_i^2.
\]

To prove the claim, fix any global optimizer with selected set \(S\). Its continuous coordinates satisfy \(Q_{SS}x_S=b_S\). If \(i\in S\), setting both \(x_i\) and \(z_i\) to zero while keeping the other coordinates unchanged changes the objective by

\[
 Q_{ii}x_i^2-\lambda_i.
\]

Optimality implies \(\lambda_i\le Q_{ii}x_i^2\le T_i\). The screen therefore excludes only \(\lambda_i>T_i\). It must retain equality. Negative penalties are allowed in this proof; they are necessarily retained. A selected variable with \(x_i=0\) also causes no difficulty.

Two constructions of \(r\) are useful.

1. If \(Q_{ii}-\sum_{j\ne i}|Q_{ij}|\ge\delta>0\) and \(\|b\|_\infty\le B\), take \(r_i=B/\delta\). To see the bound for every principal system, apply the row equation at a coordinate of maximum absolute value. This gives the simple threshold \(T_i=Q_{ii}B^2/\delta^2\).
2. More generally, let \(M=\operatorname{diag}(Q)-|\operatorname{offdiag}(Q)|\) be a nonsingular M-matrix and take \(r=M^{-1}|b|\). Principal comparison gives \(|Q_{SS}^{-1}b_S|\le M_{SS}^{-1}|b_S|\). Also \(M_{SS}r_S=|b_S|+|Q_{S,S^c}|r_{S^c}\ge|b_S|\), so \(M_{SS}^{-1}|b_S|\le r_S\). Computing this sharper vector may require polynomial preprocessing; the first construction requires only the stated bounds.

For arbitrary positive definite \(Q\), a less local bound is also available:

\[
 r_i^2=(Q^{-1})_{ii}\,b^TQ^{-1}b.
\]

Indeed, Cauchy–Schwarz in the \(Q_{SS}^{-1}\) inner product gives \(|(Q_{SS}^{-1}b_S)_i|^2\le(Q_{SS}^{-1})_{ii}b_S^TQ_{SS}^{-1}b_S\). Both factors are at most their full-matrix counterparts, by the variational characterization of the inverse quadratic form. This extends the screening theorem to every positive definite matrix, but \(b^TQ^{-1}b\) can grow proportionally to \(n\) even with bounded data, so the sufficient disorder width can grow with \(n\).

## Exact component algorithm

Independently retain vertex \(i\) precisely when \(\lambda_i\le T_i\). Set \(z_i=x_i=0\) outside \(U\), form the connected components of \(G[U]\), and solve each component independently. For a component \(C\), enumerate every \(S\subseteq C\) and evaluate

\[
 \sum_{i\in S}\lambda_i-b_S^TQ_{SS}^{-1}b_S,
\]

with value zero for the empty set. Return a minimizing support and its continuous minimizer. A direct implementation costs \(O(k^3 2^k)\) arithmetic operations on a component of size \(k\).

This decomposition is exact. It retains both ambiguous and forced-active vertices. Distinct components have zero direct coupling, and every vertex outside them is fixed at zero. No elimination of a connecting active region is used. In particular, Schur-complement fill does not invalidate the decomposition.

The argument needs independent retention events with

\[
 \Pr(\lambda_i\le T_i)\le p.
\]

Identical distributions, a continuous law, and anti-concentration are unnecessary for this particular theorem. The relevant distributional property is the lower-tail probability at the deterministic screening thresholds.

## Expected work: the exact branching-process constant

Assume first \(\Delta\ge3\) and put \(d=\Delta-1\). Conditional on a vertex being retained, its component exploration is stochastically dominated by a rooted branching process whose root has \(\operatorname{Bin}(\Delta,p)\) children and whose other vertices have \(\operatorname{Bin}(d,p)\) children. Breadth-first exposure and independent Bernoulli domination prove this even when the underlying graph contains cycles or the retention probabilities vary by vertex. Repeatedly encountered vertices only reduce the actual exploration.

Let \(H(s)\) be the probability generating function for the total progeny of the process started at a non-root vertex. Its finite value is the least nonnegative solution of

\[
 H=s(1-p+pH)^d.
\]

For \(0<p<1/d\), the radius on the positive real axis is

\[
 s_c=\frac{(d-1)^{d-1}}{p\,d^d(1-p)^{d-1}}.
\]

Indeed, solving for \(s\) gives \(s(H)=H/(1-p+pH)^d\). This function reaches its maximum at

\[
 H_* = \frac{1-p}{p(d-1)},
\]

which gives the displayed \(s_c\). Truncating the branching process at depth \(h\) and iterating its generating function shows that the least fixed point is the actual moment. The root generating function is

\[
 R(s)=s(1-p+pH(s))^\Delta,
\]

so the extra root neighbor does not change the moment radius.

Define \(p_*(d)\) as the unique solution in \((0,1/d)\) of

\[
 2p_*(1-p_*)^{d-1}=\frac{(d-1)^{d-1}}{d^d}.
\]

For \(p<p_*(d)\), choose a fixed \(s\in(2,s_c)\). Then \(k^2 2^k\le A_s s^k\) for a finite constant \(A_s\). Charging component work equally to its \(k\) vertices gives

\[
 \mathbb E\!\left[\sum_C |C|^3 2^{|C|}\right]
 =\sum_i\mathbb E\!\left[\mathbf1_{\{i\in U\}}|C(i)|^2 2^{|C(i)|}\right]
 \le n p A_s R(s).
\]

Thus the expected enumeration work is \(O(n)\) arithmetic operations, with a constant depending on \(\Delta\) and the strict gap between \(p\) and \(p_*(d)\). Reading the bounded-degree graph and finding its components also take \(O(n)\) work. Include any separate cost of constructing the screening bounds.

At \(p=p_*(d)\), \(H(2)=H_*\) and \(R(2)<\infty\). The strict gap is therefore unnecessary for expected polynomial time: using \(|C|\le n\) in the same charge yields expected \(O(n^3)\) arithmetic work for the direct implementation. The uniform infinite-tree moments with polynomial factors in \(|C|\) need not be finite at this endpoint, so the preceding expected-linear argument does require a strict gap.

For \(\Delta=2\), the descendant process has one possible child and

\[
 H(s)=\frac{s(1-p)}{1-sp}.
\]

Consequently \(p<1/2\) gives expected linear enumeration work. At \(p=1/2\), a direct count of runs in paths and cycles gives expected polynomial work, with \(O(n^5)\) sufficient for the \(k^3 2^k\) implementation. For \(\Delta\le1\), every component has size at most two and no probability restriction is needed. The case \(p=0\) is immediate.

Some strict expected-linear thresholds are:

| Maximum degree \(\Delta\) | \(p_*\) | \(1/p_*\) |
| --- | ---: | ---: |
| 2 | 0.5000000000 | 2.000000 |
| 3 | 0.1464466094 | 6.828427 |
| 4 | 0.0893163975 | 11.196152 |
| 5 | 0.0643882836 | 15.530776 |
| 6 | 0.0503656269 | 19.854811 |

## Why ordinary subcriticality is insufficient

The condition \(p<1/(\Delta-1)\) implies exponentially decaying component-size tails and components of size \(O(\log n)\) with high probability. It therefore gives polynomial enumeration time with high probability, with a degree depending on the tail constant. It does not by itself give expected polynomial enumeration time.

This distinction is sharp for the stated exhaustive enumeration algorithm. Fix \(d\ge2\) and \(p>p_*(d)\). Consider the complete rooted \(d\)-ary tree of height \(h\), of maximum degree \(d+1\) and size \(n_h=(d^{h+1}-1)/(d-1)\). Conditional on its root being retained, the generating function at 2 obeys

\[
 H_0=2,\qquad H_{h+1}=2(1-p+pH_h)^d.
\]

For \(p>p_*(d)\), this iteration has no fixed point at or above 2, so it grows without bound. For \(p<1/d\), this follows from \(s_c<2\). For \(p\ge1/d\), the maximum of \(H/(1-p+pH)^d\) over \(H\ge2\) is also less than 2: its unconstrained maximizer is at most 1, and its value at 2 is \(2/(1+p)^d<2\).

Once \(H_h\) is large enough, the inequality

\[
 H_{h+1}\ge 2p^d H_h^d
\]

implies \(\log H_h\ge c d^h\) for some \(c>0\). Hence \(\mathbb E[2^{|C(\mathrm{root})|}\mid\mathrm{root}\in U]=\exp(\Omega(n_h))\). Even the number of enumerated subsets has exponential expectation. For \(\Delta=2\) and \(p>1/2\), the all-retained event on a path gives the same conclusion from \((2p)^n\).

These examples concern the runtime of this enumeration algorithm, not an impossibility result for other algorithms. The trees themselves have treewidth one. In particular, the examples do not prove hardness of the underlying optimization problem in the intermediate subcritical regime.

## Continuous and finite-precision perturbation laws

Let \(T=\max_i T_i\). If \(\lambda_i=\bar\lambda_i+\eta_i\), where the deterministic baseline satisfies \(\bar\lambda_i\ge0\) and the \(\eta_i\) are independent uniform variables on \([0,W]\), then

\[
 \Pr(\lambda_i\le T_i)\le \min\{1,T/W\}.
\]

Thus \(W>T/p_*(\Delta-1)\) is a sufficient expected-linear condition for \(\Delta\ge3\). Equality gives the weaker expected-polynomial bound above. For \(\Delta=2\), use \(W>2T\). A continuous density upper bound \(1/W\) on the nonnegative half-line gives the same estimate when the penalty distribution has no negative mass.

An exact rational-input version avoids the representation issue of continuously distributed real numbers. Take

\[
 \eta_i\ \text{uniform on}\ \{W/m,2W/m,\ldots,W\},
\]

for rational \(W>0\) and positive integer \(m\). For any nonnegative baseline,

\[
 \Pr(\bar\lambda_i+\eta_i\le T_i)
 \le \frac{\min\{m,\max\{0,\lfloor mT_i/W\rfloor\}\}}{m}
 \le \min\{1,T_i/W\}.
\]

Ties need no isolation argument: keep screening equality and choose any minimizing support. Exact rational linear algebra evaluates each support in bit complexity polynomial in its size and the input bit length. Under a strict moment gap, any fixed polynomial size factor is absorbed by \(s^{|C|}\), giving an expected bound of the form \(n\operatorname{poly}(L)\), apart from optional screening preprocessing, where \(L\) bounds the bit length of each input number. This is a discrete perturbation theorem, not literally a continuous smoothed-analysis model.

The lower-tail hypothesis is material. For example, \(\lambda_i\) uniform on \([-W,W]\) gives retention probability approaching \(1/2\) as \(W\to\infty\), rather than approaching zero. The theorem above therefore does not cover the desired broad centered high-disorder regime in general. A density upper bound alone also does not control the retained fraction if substantial mass lies below zero. Arbitrary negative baseline shifts similarly invalidate the uniform estimate \(T/W\).

## Assessment of the influence-decay extension

Exponential decay of the inverse of a diagonally dominant matrix bounds the effect of distant active variables, but a nonzero effect can still reverse a sufficiently small support gap. Continuous perturbations make exact ties unlikely; they do not create a deterministic minimum gap. Truncation plus a global isolation bound can give a small error probability, but invoking an exponential fallback on that event does not yield an expected polynomial algorithm without a sufficiently strong runtime-tail analysis.

Likewise, connecting all ambiguous sites within radius \(r\) becomes less useful as \(r\) grows: its potential degree grows roughly as \((\Delta-1)^r\). An argument that takes \(r=\Theta(\log n)\) for numerical accuracy must account for this growth. A valid extension would need a multiscale certificate that reduces the unresolved-site probability faster than the interaction neighborhoods expand, together with a proof controlling the dependencies between the resulting random events. No such proof is supplied here.

## Checks performed

Two targeted commands used `python - <<'PY'`: one bisected the displayed \(p_*\) equation for \(\Delta=2,\ldots,10\), and one checked this file for trailing whitespace, a final newline, and balanced display-math delimiter counts. Both completed successfully; the table reports the first five numerical thresholds. No project-wide verification, CI inspection, external search, or knowledge-base lookup was performed.
