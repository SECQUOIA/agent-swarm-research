# Audit of the gain--plateau linear-size robust parity LP

Date: 2026-09-02

## Verdict

The gain--plateau construction gives a valid linear-size strengthening of the
parallel-path parity LP. With \(P=17N+1\) nodes, constant row and column sparsity,
and coefficients of magnitude at most two, preparing one amplitude encoding of
any nonnegative point with constant relative \(\ell_2\) feasibility residual
requires \(\Omega(N)=\Omega(P)\) coefficient queries. The proof does not need an
objective-gap assumption.

The construction avoids the quadratic replicated-path cost by growing the exact
signal to height

\[
 H=\Theta(\sqrt N)
\]

using only \(O(\log N)\) gain-two edges, and then carrying that signal along a
length-\(\Theta(N)\) gain-one plateau. Thus the relevant tradeoff is paid in
solution dynamic range rather than matrix coefficient magnitude. Its reduced
barrier Hessian is not condition one on the entire central path. It does, however,
have condition number below \(7/6\), uniformly in \(N\), throughout the late path
\(0<\mu\le1/16\).

## Construction

Let \(N\ge2\),

\[
 T=\left\lceil\frac12\log_2N\right\rceil,
 \qquad K=16N,\qquad P=N+K+1=17N+1,
\]

and index nodes by \(0,\ldots,N+K\). Define deterministic heights and local gains

\[
 H_i=2^{\min\{i,T\}},qquad
 g_i=\frac{H_i}{H_{i-1}}\in\{1,2\},qquad H=2^T.
\]

Then \(\sqrt N\le H<2\sqrt N\). For hidden signs
\(\sigma_1,\ldots,\sigma_N\), put

\[
 a_i=\begin{cases}
      \sigma_i,&1\le i\le N,\\
      1,&N<i\le N+K,
     \end{cases}
 \qquad
 \tau_0=1,\qquad \tau_i=\prod_{j=1}^ia_j.
\]

At each node introduce nonnegative variables \((u_i,v_i,h_i,t_i)\), and write
\(d_i=u_i-v_i\), \(q_i=u_i+v_i\). The equalities are

\[
\begin{aligned}
 d_0&=1,&d_i-g_ia_id_{i-1}&=0,\\
 h_0&=1,&h_i-g_ih_{i-1}&=0,\\
 &&q_i+t_i-2h_i&=0,
\end{aligned}                                                   \tag{1}
\]

with one transition row of each type for every \(i\ge1\), and one cap row for
every node. The objective is

\[
 \min\sum_{i=0}^{N+K}(2u_i+2v_i+h_i+t_i).                 \tag{2}
\]

Only one coefficient in a signed transition depends on the input. The support,
\(b\), and \(c\) are fixed; \(\|b\|_2=\sqrt2\).

## The robust state theorem

### Theorem 1

Suppose a coefficient-query algorithm outputs a density operator \(\rho\) for
which there is a nonzero \(x\ge0\) satisfying

\[
 \frac{\|Ax-b\|_2}{\|b\|_2}\le\frac1{100},
 \qquad
 D_{\rm tr}\!\left(
   \rho,|x/\|x\|_2\rangle\!\langle x/\|x\|_2|
 \right)\le\frac1{100}.                                  \tag{3}
\]

Then the algorithm makes \(\Omega(N)=\Omega(P)\) coherent sparse coefficient
queries. The conclusion is unchanged if the contract also imposes any objective
accuracy condition.

The LP has \(4P\) variables and \(3P\) full-row-rank equalities. Every row and
column has at most four nonzeros and every coefficient of \(A,b,c\) has magnitude
at most two. It is bounded and strictly primal-dual feasible and has a unique
nondegenerate strictly complementary optimum.

### Stability proof

Let the residuals in the signed transitions be \(e_i\), including the root
residual \(e_0=d_0-1\). Gauge and scale by

\[
 z_i=\frac{\tau_i d_i}{H_i}.
\]

Then

\[
 e_i=\tau_iH_i(z_i-z_{i-1})\quad(i\ge1).
\]

The effective series resistance is constant:

\[
 \sum_{i=1}^{N+K}H_i^{-2}
 <\frac13+\frac{17N}{H^2}\le\frac{52}{3}.                \tag{4}
\]

Therefore Cauchy--Schwarz gives, simultaneously at every node,

\[
 |z_i-1|
 \le |e_0|+
      \left(\sum_{j=1}^iH_j^{-2}\right)^{1/2}
      \left(\sum_{j=1}^ie_j^2\right)^{1/2}
 \le\left(1+\sqrt{52/3}\right)E,                         \tag{5}
\]

where \(E=\|Ax-b\|_2\le\sqrt2/100\). The right side is below \(3/40\).
Applying the same argument to the unsigned reference transitions gives

\[
 \left|\frac{h_i}{H_i}-1\right|<\frac3{40}.              \tag{6}
\]

Let \(c_i=q_i+t_i-2h_i\) be a cap residual. Nonnegativity and (6) imply

\[
 q_i,t_i\le2h_i+|c_i|<2.165H_i.                          \tag{7}
\]

There is no fractional-point loophole here: \(u_i,v_i\ge0\) always gives
\(q_i\ge|d_i|\), independently of the cap or objective. Also

\[
 u_i^2+v_i^2=\frac{q_i^2+d_i^2}{2}\le q_i^2.
\]

Consequently,

\[
 \|x\|_2^2
 \le\sum_i(q_i^2+h_i^2+t_i^2)
 <11\sum_iH_i^2.                                         \tag{8}
\]

The geometric ramp and plateau obey

\[
 \sum_iH_i^2
 <\left(17N+\frac43\right)H^2
 <\frac{53}{3}NH^2.                                      \tag{9}
\]

On the output set \(S=\{N+1,\ldots,N+K\}\), \(\tau_i=p_N\), where
\(p_N=\prod_{j=1}^N\sigma_j\). Equations (5) and \(q_i\ge|d_i|\) give

\[
 p_Nd_iq_i>\left(\frac{37}{40}\right)^2H^2.             \tag{10}
\]

Measure the normalized ideal state in the coordinate basis, reporting \(+1\) on
an output \(u_i\), \(-1\) on an output \(v_i\), and a fair bit elsewhere. Its
bias toward \(p_N\) is greater than

\[
 \frac{K(37/40)^2H^2}{2\|x\|_2^2}
 >\frac{16(37/40)^2}{2\cdot11\cdot(53/3)}
 >\frac1{30}.                                             \tag{11}
\]

Trace distance \(1/100\) leaves bias greater than \(7/300\). Constant
repetition therefore computes parity. One coherent sparse row or column query to
(1) reveals at most one \(\sigma_i\) and is simulated by one sign-oracle query.
Quantum parity needs \(\Omega(N)\) queries, proving the theorem.

## LP regularity

In \((d,h,q,t)\) coordinates, the signed \(d\) block and unsigned \(h\) block are
nonsingular lower bidiagonal matrices; after them, every cap row has a private
\(t_i\) coefficient. Hence the \(3P\) rows are independent.

Exact feasibility fixes

\[
 h_i=H_i,qquad d_i=\tau_iH_i,qquad H_i\le q_i\le2H_i,
 \qquad t_i=2H_i-q_i.                                    \tag{12}
\]

Thus the feasible set is compact. Taking \(q_i=3H_i/2\) makes every primal
variable positive. Taking equality multipliers zero gives the positive dual slack
\(s=c\), proving strict primal-dual feasibility.

On the feasible affine space, the local objective is

\[
 2q_i+H_i+t_i=q_i+3H_i.
\]

The unique optimum has \(q_i=t_i=H_i\), so

\[
 \operatorname{OPT}=4\sum_iH_i=\Theta(N^{3/2}).          \tag{13}
\]

At the optimum, select \(u_i\) if \(\tau_i=+1\), and \(v_i\) if
\(\tau_i=-1\). The selected pair column, together with the \(h_i,t_i\) columns,
forms a nonsingular \(3P\)-column basis: pivot first on the signed difference
block, then the unsigned reference block, then the private cap columns. All basic
variables are positive.

For an explicit strict-complementarity certificate, let \(B_a\) and \(B_g\) be
the signed and unsigned lower-bidiagonal matrices in (1). Choose dual multipliers
\(\alpha,\beta,\gamma\) satisfying

\[
 B_a^T\alpha=\tau,qquad B_g^T\beta=3\mathbf1,qquad
 \gamma=\mathbf1.                                        \tag{14}
\]

Under the convention \(A^Ty+s=c\), this gives

\[
 s_u=\mathbf1-\tau,qquad s_v=\mathbf1+\tau,qquad
 s_h=s_t=0.                                               \tag{15}
\]

The zero member of every pair has slack two and every positive variable has zero
slack. The positive-column basis also makes the multiplier unique, proving the
claimed nondegeneracy and strict complementarity.

## Reduced central-path geometry

The null space has the input-independent orthonormal basis

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right).
                                                               \tag{16}
\]

At node height \(h=H_i\), write the central coordinate as
\(q=h+z\), with \(0<z<h\). The local barrier stationarity equation is

\[
 1=\mu\left[
   \frac1{2h+z}+\frac1z-\frac1{h-z}
 \right].                                                  \tag{17}
\]

The bracket is strictly decreasing from \(+\infty\) to \(-\infty\), so this
defines one central coordinate. The sum of its two \(h\)-dependent terms is
negative, so \(z<\mu\). If \(0<\mu\le1/16\) and \(h\ge1\), that sum is at
least \(-16/15\), and hence

\[
 \frac{15}{16}\mu\le z<\mu.                              \tag{18}
\]

The scalar Hessian in the \(q\) coordinate is

\[
 f_h''(q)=\mu\left[
  \frac1{(2h+z)^2}+\frac1{z^2}+\frac1{(h-z)^2}
 \right].                                                  \tag{19}
\]

Equations (18)--(19) imply

\[
 \frac1\mu<f_h''(q)<\frac7{6\mu}.                        \tag{20}
\]

Because \(dq/dW_i=\sqrt{2/3}\), the actual reduced eigenvalue in the
orthonormal basis (16) is \((2/3)f_h''(q)\). Hence

\[
 \frac2{3\mu}<\lambda_i<\frac7{9\mu},
 \qquad
 \kappa(W^TH_xW)<\frac76                                 \tag{21}
\]

throughout the full late central-path tail \(\mu\le1/16\), independently of
\(N\). Omitting the factor \(2/3\) in the absolute eigenvalue interval would be
a normalization error, although it would not affect the condition ratio.

Combining (21) with Theorem 1 gives the central-path corollary most directly
relevant to QIPMs:

> **Corollary 2 (linear central-state lower bound at constant reduced
> condition).** For every prescribed \(0<\mu\le1/16\), preparing a state within
> trace distance \(1/100\) of the normalized exact primal central point requires
> \(\Omega(P)\) coefficient queries, although the input has constant row and
> column sparsity, coefficients bounded by two, and reduced primal-barrier Hessian
> condition number below \(7/6\) at that point and throughout the remaining path
> to the optimum.

The lower bound therefore cannot be charged to the condition number of the
reduced Newton solve on the late central-path tail. It is an end-to-end cost of
loading the hidden affine translation into original primal coordinates.

This does not extend uniformly to the whole central path. For
\(\mu/H\to\infty\), setting \(r=q/H\) in (17) shows that \(r\) approaches an
\(H\)-independent analytic-center constant, while (19) scales as
\(\mu/H^2\). Across heights from one to \(H=\Theta(\sqrt N)\), the reduced
condition number can therefore approach \(\Theta(H^2)=\Theta(N)\). The proper
claim is a uniformly conditioned late tail, not condition one everywhere.

## Why this evades the replication barrier

For a unit-height signed path, changing the normalized endpoint by a constant has
energy \(\Theta(1/N)\), so bounded-coefficient parallel-path amplification needs
\(\Theta(N)\) copies. Here the raw coefficients remain at most two, but after the
change of variables \(d_i=\tau_iH_iz_i\), the residual on edge \(i\) is weighted
by \(H_i\). The effective resistance becomes the summable series (4). The
endpoint amplitude is simultaneously raised to \(H=\Theta(\sqrt N)\), so
\(\Theta(N)\) plateau copies carry total squared mass \(\Theta(NH^2)=\Theta(N^2)\)
inside a state whose total squared norm has the same order.

Thus this construction does not contradict the earlier
\(RB^2=\Omega(\eta^2N)\) result for replicated **unit-height** paths. It exits that
model through accumulated signal gain, paying

\[
 \max_i H_i=\Theta(\sqrt N),\qquad
 \operatorname{OPT}=\Theta(N^{3/2}),qquad
 \|x^*\|_2=\Theta(N).                                    \tag{22}
\]

All of these scales are polynomial and are created from constant local
coefficients.

## Balanced XOR/PCP route: why it is unnecessary here

A balanced XOR circuit does not immediately give the same theorem.

1. The standard convex-hull XOR inequalities have the four Boolean truth-table
   points as boundary vertices. Turning their inequalities into standard-form
   slack equalities therefore prevents strict primal feasibility when the input
   wires are fixed exactly. Thickening the truth-table polytopes restores an
   interior but introduces fractional assignments and accumulated gate error.
2. If every fixed constant is placed in \(b\), then \(\|b\|_2=\Theta(\sqrt P)\).
   A constant relative residual can corrupt a constant fraction of all rows, and
   in particular can corrupt the small cut above the root while an output-copy
   gadget propagates the wrong value exactly.
3. Homogenizing constants through one reference anchor repairs the normalization,
   but an ordinary depth-\(\Theta(\log N)\) formula still has a single root-to-leaf
   channel. A unit output change can be spread across that channel with
   \(\ell_2\) violation \(O(1/\sqrt{\log N})\). Robust PCP-style wire blocks would
   need to eliminate this fractional drift while preserving bounded degree,
   coefficient-query locality, and a strictly feasible LP relaxation.

These points are not a general impossibility theorem for fault-tolerant LP circuit
encodings. They show that the naive balanced XOR formulation does not close the
robustness gap. Since the gain--plateau path already obtains \(P=\Theta(N)\) with
a simpler proof and stronger sparsity, the XOR/PCP route is no longer needed for
the present coefficient-query lower bound.

## Audit status

The dimension, rank, sparsity, oracle reduction, feasibility, compactness,
nondegeneracy, strict complementarity, stability constants, state norm, decoder,
and late-tail reduced-conditioning bounds above have been checked independently.
The main qualifications are the \(\Theta(\sqrt N)\) primal dynamic range and the
absence of a dimension-independent reduced-conditioning claim for the early
central path.

A targeted open-literature search on 2026-09-02 found sparse LP optimal-value
lower bounds and clock/endpoint-padding lower bounds for quantum linear systems,
but no matching gain--plateau LP construction. The closest proof pattern is the
repeated endpoint region in Mori et al.,
[*Sparsity-dependent Complexity Lower Bound of Quantum Linear System
Solvers*](https://arxiv.org/abs/2601.16697), whose hardness is stated for a square
QLS instance and parameterized by its condition number and sparsity. Apers and
Gribling,
[*Quantum Speedups for Linear Programming via Interior Point
Methods*](https://doi.org/10.1137/23M1608569), prove stronger generic dimension
dependence for additive optimal-value estimation, but do not give this
approximate-feasible original-primal state contract or late-tail reduced geometry.
This search is evidence of apparent novelty, not a proof of priority; the parity
adversary and endpoint-padding principles themselves are established prior art.
