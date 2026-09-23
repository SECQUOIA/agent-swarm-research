# Linear-size robust gain-parity LP

Date: 2026-09-02

## Main result

A short constant-gain prefix followed by a polynomial plateau gives a
constant-sparse LP with all of the following properties:

- linear input size and an \(\Omega(n)\) standard coefficient-query lower bound;
- robustness to a fixed right-hand-side-relative \(\ell_2\) feasibility residual;
- one amplitude-encoded original-primal output state, with no tomography;
- coefficients of magnitude at most two and polynomial solution range;
- a uniformly conditioned reduced primal-barrier Hessian on the late central path.

The construction also gives a sharp size--dynamic-range frontier for path-bundle
parity gadgets. Bounded solution scale forces the earlier quadratic-volume
construction, while linear volume requires scale \(\Omega(\sqrt N)\). The LP below
attains the latter endpoint.

### Construction

Let hidden signs be

\[
 \sigma_1,\ldots,\sigma_N\in\{-1,+1\},\qquad
 p_i=\prod_{j=1}^i\sigma_j,
\]

and assume \(N\ge2\). Set

\[
 T=\left\lceil\frac12\log_2N\right\rceil,\qquad
 K=16N,\qquad P=N+K+1=17N+1.
\]

There are nodes \(i=0,\ldots,N+K\). Define

\[
 H_i=2^{\min\{i,T\}},\qquad
 g_i=\frac{H_i}{H_{i-1}}\in\{1,2\}\quad(i\ge1).
\]

The first \(N\) edges carry the input signs, and the remaining \(K\) edges copy
the final parity:

\[
 a_i=\begin{cases}\sigma_i,&1\le i\le N,\\1,&N<i\le N+K.\end{cases}
\]

At every node introduce \(u_i,v_i,h_i,t_i\ge0\), with
\(d_i=u_i-v_i\) and \(q_i=u_i+v_i\). The equalities are

\[
\begin{aligned}
 d_0&=1,&d_i-g_ia_id_{i-1}&=0&&(1\le i\le N+K),\\
 h_0&=1,&h_i-g_ih_{i-1}&=0&&(1\le i\le N+K),\\
 &&q_i+t_i-2h_i&=0&&(0\le i\le N+K).
\end{aligned}                                             \tag{1}
\]

The objective is

\[
 \min\sum_{i=0}^{N+K}(2u_i+2v_i+h_i+t_i).                \tag{2}
\]

We use coherent fixed-position sparse access to \(A,b,c\). A value, whole-row,
or whole sparse-column query reveals at most one hidden sign: a path variable has
an input-dependent coefficient only in its outgoing transition row. Thus every
LP-oracle query is simulated coherently by one standard sign-oracle query plus
input-independent computation. Repeated occurrences do not provide a batch
oracle.

### Theorem 1 (linear-size robust primal-state lower bound)

The LP (1)--(2) has \(4P=\Theta(N)\) variables and
\(3P=\Theta(N)\) full-row-rank equalities. Every row has at most four nonzeros,
every column has at most three, and every input coefficient has magnitude at most
two. The support pattern, \(b\), and \(c\) are input-independent.

It is bounded and strictly primal-dual feasible and has a unique nondegenerate
strictly complementary optimum. Its largest optimal coordinate is
\(\Theta(\sqrt N)\), its optimal value is \(\Theta(N^{3/2})\), and its optimal
Euclidean radius is \(\Theta(N)\).

Suppose a quantum query algorithm outputs an unconditional density operator
\(\rho\). If there is a nonzero \(x\ge0\) such that

\[
 \frac{\|Ax-b\|_2}{\|b\|_2}\le\frac1{100}                 \tag{3}
\]

and

\[
 D_{\rm tr}\!\left(\rho,
 |x/\|x\|_2\rangle\langle x/\|x\|_2|\right)\le\frac1{100},
                                                               \tag{4}
\]

then the algorithm makes \(\Omega(N)=\Omega(P)\) coefficient-oracle queries.
The conclusion remains true under any additional fixed two-sided relative
objective-accuracy requirement.

The same result holds for a heralded success branch whose success probability is
bounded below by an input-independent constant, with repetition overhead charged
to the query count. An unspecified unheralded good branch is not claimed.

In the explicit input-independent orthonormal null basis

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right),      \tag{5}
\]

the reduced primal-barrier Hessian has spectral condition number below \(7/6\)
at every central point with \(0<\mu\le1/16\), independently of \(N\).

## Proof

### Rank, regularity, and exact optimum

Let \(B_{ga}\) be the pinned lower-bidiagonal matrix for the first row family in
(1), and \(B_g\) its unsigned counterpart. Both are nonsingular. In
\((d,q,h,t)\) coordinates, the first two row blocks uniquely fix \(d,h\), and
each cap row has a private \(t_i\) coefficient. Hence all \(3P\) rows are
independent.

Define \(\tau_i=p_i\) through node \(N\), and \(\tau_i=p_N\) afterward. Exact
feasibility fixes

\[
 h_i=H_i,\qquad d_i=H_i\tau_i.
\]

The cap and nonnegativity give

\[
 H_i\le q_i\le2H_i,\qquad t_i=2H_i-q_i.                  \tag{6}
\]

The local objective contribution is \(q_i+3H_i\). Therefore the unique optimum is

\[
 q_i=t_i=h_i=H_i,\qquad d_i=H_i\tau_i.                   \tag{7}
\]

Taking \(q_i=3H_i/2\) is strictly primal feasible. Equality multiplier zero gives
slack \(s=c>0\), so the LP is strictly dual feasible. The sign-selected member of
each \((u_i,v_i)\) pair, together with \(h_i,t_i\), gives a triangular basis.
This proves primal nondegeneracy.

Strict complementarity is explicit. Give the difference, reference, and cap rows
multipliers \(\alpha,\beta,\gamma\) satisfying

\[
 B_{ga}^T\alpha=\tau,\qquad B_g^T\beta=3\mathbf1,\qquad
 \gamma=\mathbf1.
\]

Under \(A^Ty+s=c\),

\[
 s_u=\mathbf1-\tau,\qquad s_v=\mathbf1+\tau,\qquad
 s_h=s_t=0.
\]

Thus every positive primal coordinate has zero slack, while the zero member of
each pair has slack two. The positive-column basis makes the dual multiplier
unique.

Let \(H=2^T\in[\sqrt N,2\sqrt N)\). There are \(\Theta(N)\) plateau nodes, so

\[
 \sum_iH_i=\Theta(NH)=\Theta(N^{3/2}),\qquad
 \sum_iH_i^2=\Theta(NH^2)=\Theta(N^2).
\]

Equation (7) gives the stated value, coordinate, and radius bounds.

### Uniform conditioning on the late central path

The vectors (5) are orthonormal, input-independent, and span the null space.
Write a central coordinate as \(q_i=H_i+z_i\), with \(0<z_i<H_i\). After
eliminating the equalities, the nonconstant part of the local barrier objective is

\[
 z-\mu\log\!\left[(H_i+z/2)(z/2)(H_i-z)\right].
\]

Stationarity gives

\[
 \frac1\mu=\frac1{2H_i+z_i}+\frac1{z_i}-\frac1{H_i-z_i}. \tag{8}
\]

The two \(H_i\)-dependent terms have negative sum, so \(z_i<\mu\). For
\(H_i\ge1\) and \(0<\mu\le1/16\),

\[
 -\frac{16}{15}
 \le\frac1{2H_i+z_i}-\frac1{H_i-z_i}<0.
\]

Using (8),

\[
 \frac{15}{16}\mu\le z_i<\mu.                            \tag{9}
\]

The scalar second derivative is

\[
 f_i''(z_i)=
 \mu\left[(2H_i+z_i)^{-2}+z_i^{-2}+(H_i-z_i)^{-2}\right].
\]

Equations (9), \(H_i\ge1\), and \(\mu\le1/16\) imply

\[
 \frac1\mu<f_i''(z_i)
 <\frac1\mu\left(\frac{256}{225}+\frac1{1024}+\frac1{225}\right)
 <\frac7{6\mu}.                                          \tag{10}
\]

Changing from \(z_i\) to \(W_i\) multiplies every diagonal entry by \(2/3\).
The reduced Hessian is diagonal, so (10) proves the condition-number claim.

Consequently, for every prescribed \(0<\mu\le1/16\), preparing the normalized
exact primal central state to trace distance \(1/100\) requires
\(\Omega(P)\) coefficient queries even though the reduced primal-barrier Hessian
at that point, and throughout the remaining path to the optimum, has condition
number below \(7/6\).

All reduced geometry is public on this family. The basis \(W\), the reduced
objective and barrier, every reduced derivative, and each central scalar \(z_i\)
depend only on the deterministic heights \(H_i\), not on \(\sigma\). The hidden
object is the affine feasible translation \(d_i=H_i\tau_i\). Thus even granting
exact reduced solves and their state preparation for free does not remove the
lower bound for loading the answer into original primal coordinates.

### Robust state decoder

Put

\[
 E=\|Ax-b\|_2\le\frac{\sqrt2}{100},
\]

because \(b\) has exactly two unit anchors. Let \(e_i\) denote the
difference-row residuals, including \(e_0=d_0-1\), and define
\(z_i^{(d)}=\tau_id_i/H_i\). Then

\[
 z_0^{(d)}-1=e_0,\qquad
 z_i^{(d)}-z_{i-1}^{(d)}=\frac{\tau_ie_i}{H_i}.
\]

The gain prefix and plateau satisfy

\[
 \sum_{i=1}^{N+K}H_i^{-2}
 <\frac13+\frac{17N}{H^2}\le\frac{52}{3}.                \tag{11}
\]

Cauchy--Schwarz gives, simultaneously for every node,

\[
 \left|z_i^{(d)}-1\right|
 \le\left(1+\sqrt{52/3}\right)E<\frac3{40}.              \tag{12}
\]

The identical argument for the reference rows gives

\[
 \left|\frac{h_i}{H_i}-1\right|<\frac3{40}.              \tag{13}
\]

For cap residual \(c_i=q_i+t_i-2h_i\), nonnegativity implies

\[
 q_i,t_i\le2h_i+|c_i|<2.165H_i.                          \tag{14}
\]

Using \(u_i^2+v_i^2\le q_i^2\),

\[
\begin{aligned}
 \|x\|_2^2
 &\le\sum_i(q_i^2+h_i^2+t_i^2)
 <11\sum_iH_i^2\\
 &<11\left(17N+\frac43\right)H^2
 \le\frac{583}{3}NH^2.                                  \tag{15}
\end{aligned}
\]

Let \(S=\{N+1,\ldots,N+K\}\). These are \(16N\) plateau-scale copies of the
final parity. Equations (12) and \(q_i\ge|d_i|\) give

\[
 \sum_{i\in S}\tau_id_iq_i
 \ge16N\left(\frac{37}{40}\right)^2H^2.                  \tag{16}
\]

Use the fixed measurement that reports \(+1\) on \(u_i\), \(-1\) on \(v_i\) for
\(i\in S\), and a fair sign elsewhere. Its ideal bias toward \(p_N\) is greater
than

\[
 \frac{16(37/40)^2}{2(583/3)}>\frac1{30}.                \tag{17}
\]

Trace distance \(1/100\) leaves bias greater than \(7/300\). A fixed number of
repetitions computes parity with bounded error. Quantum parity needs
\(\Omega(N)\) sign queries, while every LP query is simulated with \(O(1)\) sign
queries. This proves Theorem 1.

The exponent is tight: query all \(N\) signs, compute their prefixes classically,
and prepare the explicit optimum or any desired central point using \(O(N)\)
input queries.

## Adaptive preprocessing and trajectory accounting

The one-output theorem already gives a tight amortized statement for an entire
QIPM trajectory. It is important that the conclusion is linear **in total**, not
linear per Newton iteration.

### Corollary 1.1 (adaptive end-to-end trajectory lower bound)

Use the standard sign oracle

\[
 O_\sigma|i,z\rangle=|i,z\mathbin\oplus\sigma_i\rangle
\]

(with any fixed reversible encoding of \(\pm1\)), or the coherently simulated
fixed-position sparse LP oracle described above. Consider any interactive quantum
algorithm with the following freedoms. Calls to the oracle or its inverse count
equally, and the query terms below are worst-case query counts.

1. it starts with arbitrary \(\sigma\)-independent classical or quantum advice;
2. it performs arbitrary data-dependent preprocessing, intermediate measurements,
   and adaptive classical control;
3. it retains unlimited persistent classical and quantum workspace through an
   arbitrary number \(R\) of Newton, correction, refinement, or preconditioning
   phases; and
4. every input-dependent primitive used by those phases is implemented from the
   raw oracle, and every such raw call is charged.

Partition the raw coefficient queries in any way as

\[
 Q_{\rm prep}+\sum_{t=1}^R
 (Q_{{\rm form},t}+Q_{{\rm solve},t}+Q_{{\rm recover},t})+Q_{\rm out}.       \tag{A1}
\]

If the final unconditional state obeys (3)--(4), then

\[
 Q_{\rm prep}+\sum_{t=1}^R
 (Q_{{\rm form},t}+Q_{{\rm solve},t}+Q_{{\rm recover},t})+Q_{\rm out}
 =\Omega(N)=\Omega(P).                                                        \tag{A2}
\]

The same conclusion holds if the final state is the normalized original-primal
central point for any adaptively selected \(0<\mu\le1/16\). More generally, it is
enough that any caller-accessible committed output state in the transcript
satisfies (3)--(4).

#### Proof

Regard the preprocessing, all persistent advice, all adaptive phases, and the
output routine as one quantum query algorithm. Intermediate measurements and
classical control do not change the query model; equivalently, they may be
purified and deferred. Compose its final channel with the fixed measurement in
(17). This computes parity with a fixed positive bias. Every sparse LP query is
simulated by at most one call to \(O_\sigma\). The quantum parity lower bound
therefore applies after constant repetition, which changes (A1) by only a constant
factor, proving (A2). An exact central point is
feasible, so it is a special case of (3). No independence between rounds and no
assumption about where the algorithm stores the prefixes is used. \(\square\)

This ledger covers a data-dependent preconditioner or compiled Newton oracle. If
setup constructs a reusable classical table or persistent quantum resource, its
raw queries belong to \(Q_{\rm prep}\). If a resource is consumed, all queries
needed to prepare the consumed copies are charged in setup or in the phase using
them. Treating a separately supplied input-dependent resource as free changes the
input model and invalidates the conclusion: one free advice bit containing
\(p_N\), or a free original-primal central-state oracle, defeats the reduction.

### Proposition 1.2 (static-oracle amortization ceiling)

For the same fixed LP instance, all coefficient dependence can be cached with
exactly \(N\) raw sign queries. After this setup, every later sparse coefficient
query, reduced Newton solve, and original-coordinate recovery can be simulated
without further raw queries. Consequently, for any finite or adaptive number of
iterations,

\[
 Q_{\rm total}=O(N)=O(P).                                                       \tag{A3}
\]

Indeed, query every \(\sigma_i\), store the signs and their prefix products, and
then answer all coefficient lookups locally. The deterministic heights \(H_i\),
the null basis (5), and the central scalars obtained from (8) are public. Unlimited
computation is free in the query model, so this cached description suffices to
prepare every requested central point or to simulate the full QIPM trajectory.

Corollary 1.1 and Proposition 1.2 give a tight \(\Theta(P)\) total raw-query law.
They also rule out a stronger fixed-instance iteration multiplier in this model.
In particular, no \(\Omega(RP)\) trajectory lower bound is possible for this
family: the hidden input is static and contains only \(N=\Theta(P)\) bits. Such an
additive per-round result requires fresh online input after each committed output,
a memory restriction that prevents caching, or a different charged resource such
as gates, communication, QRAM writes, or copies of consumable advice.
Equivalently, the only unconditional average implied over \(R\) phases is
\(\Omega(P/R)\) raw queries per phase after charging setup once.

Finally, the output contract is essential. All reduced geometry of this family is
input-independent, so an algorithm asked only for reduced Newton directions,
reduced central coordinates, or the known scalar objective can answer without
learning parity. The lower bound attaches to forming an original-primal state (or
another output with the fixed parity decoder), not to the mere act of making
multiple Newton calls.

## Sharp size--dynamic-range frontier

### Proposition 2 (path-bundle frontier)

Consider \(R\) internally disjoint parity-propagation paths, each containing all
\(N\) sign layers. Let the exact positive reference scale on every path be at most
\(H\), with gain constraint

\[
 d_i-\frac{h_i}{h_{i-1}}a_id_{i-1}=0.
\]

If a fixed absolute residual threshold \(\eta>0\) must exclude a point whose root
is exact and whose \(R\) endpoints all have the wrong normalized sign, then

\[
 RH^2>\frac{\eta^2}{4}N.                                 \tag{18}
\]

If the paths occupy \(P=\Theta(RN)\) nodes, then

\[
 PH^2=\Omega(N^2).                                       \tag{19}
\]

After writing \(d_i=\tau_ih_iw_i\), residual energy on one path is
\(\sum_i h_i^2(w_i-w_{i-1})^2\). Its effective resistance is
\(\mathcal R=\sum_i h_i^{-2}\ge N/H^2\). The minimum energy for voltage
difference two is \(4/\mathcal R\le4H^2/N\). Taking the harmonic minimizer on all
\(R\) paths gives total residual squared at most \(4RH^2/N\). The maximum
principle keeps \(w_i\in[-1,1]\), so the vector is nonnegative and exactly
objective-optimal with \(q_i=t_i=h_i\). This proves (18)--(19).

The bounded-scale parallel construction in
2026-09-02-parity-amplified-primal-state-lower-bound.md has
\(R=\Theta(N)\), \(H=\Theta(1)\), and \(P=\Theta(N^2)\). Theorem 1 here has
\(R=1\), \(H=\Theta(\sqrt N)\), and \(P=\Theta(N)\). Both saturate (19). Thus
linear volume requires \(H=\Omega(\sqrt N)\) in this path-bundle model, and the
plateau construction uses the minimum possible polynomial range.

## Scope, comparison, and novelty

This is an end-to-end coefficient-query lower bound for an original-primal
amplitude state. Internal row scaling, preconditioning, an OSS formulation, or an
infeasible-start embedding cannot change the fixed final-state decoder.

The residual in (3) is the standard right-hand-side-relative residual. Here
\(\|b\|_2=\sqrt2\), so it is a fixed global residual, not a row-normalized
root-mean-square error or scale-invariant backward error. The theorem quantifies
over every nonzero nonnegative vector in this residual tube. The objective promise
is optional and two-sided; no scalar-objective lower bound is claimed.

Compared with the quadratic bounded-scale theorem, this improves the query lower
bound from \(\Omega(\sqrt P)\) to the optimal \(\Omega(P)\), while retaining a
constant reduced-Hessian condition number on \(0<\mu\le1/16\). The tradeoff is
that the exact primal range grows as \(\Theta(\sqrt N)\), and the reduced Hessian
is bounded-condition rather than an exact scalar identity for every \(\mu\).

The parity lower bound, endpoint padding, weighted-path resistance, and
state-measurement reduction are established techniques. Nearby primary sources
include:

- Beals et al., [*Quantum Lower Bounds by
  Polynomials*](https://arxiv.org/abs/quant-ph/9802049), for parity;
- Harrow, Hassidim, and Lloyd,
  [*Quantum algorithm for linear systems of
  equations*](https://arxiv.org/abs/0811.3171), for padded computation-history
  solution states;
- Caha, Landau, and Nagaj,
  [*The Feynman-Kitaev computer's clock: bias, gaps, idling, and pulse
  tuning*](https://arxiv.org/abs/1712.07395), equations (18)--(19), for constant
  local gains producing geometrically biased clock amplitudes;
- Bausch and Crosson,
  [*Analysis and limitations of modified circuit-to-Hamiltonian
  constructions*](https://arxiv.org/abs/1609.08571), Lemma 4, for weighted
  linear clocks realizing prescribed time distributions;
- Mori et al.,
  [*Sparsity-dependent Complexity Lower Bound of Quantum Linear System
  Solvers*](https://arxiv.org/abs/2601.16697), for repeated endpoint parity in a
  sparse QLS state;
- Wang and Zhang,
  [*Tight Quantum Depth Lower Bound for Solving Systems of Linear
  Equations*](https://arxiv.org/abs/2407.06012), for a sparse weighted inverse
  clock whose output state reveals a chain endpoint;
- Apers and Gribling,
  [*Quantum speedups for linear programming via interior point
  methods*](https://arxiv.org/abs/2311.03215), for sparse-LP value query lower
  bounds and a QIPM returning a feasible near-optimal point.

No primary source found in the targeted search gives this conjunction: a
fixed-pattern bounded-degree LP; constant relative \(\ell_2\) feasibility
residual; quantification over every nonnegative vector in that tube; one
original-primal amplitude state; an \(\Omega(P)\) coefficient-query lower bound;
polynomial solution range; and a uniformly conditioned reduced central tail. This
is evidence of apparent novelty, not proof of priority.

The gain-and-plateau amplification principle itself is therefore not new. The
LP-native contribution is the quantifier over **every** nonnegative vector in
the residual tube, together with strict LP regularity and the public,
uniformly conditioned reduced central tail. The pinned propagation block has
\(\kappa=\Theta(N)\), and its normal equations have condition
\(\Theta(N^2)\), so the linear exponent is consistent with known
\(\Omega(\kappa)\) QLS lower bounds. Those bounds do not formally imply the
present underdetermined any-feasible-state LP theorem.

Corollary 1.1 is an oracle-accounting consequence of the state decoder, not a
new quantum direct-product theorem. Proposition 1.2 is the matching obstruction:
static-input caching prevents any honest multiplication by the IPM iteration
count. The trajectory-level novelty remains the LP family and its robust final
state contract, rather than the composition argument itself.

For completeness, the bidiagonal propagation block has norm \(\Theta(1)\).
Its inverse maps the root vector to the height profile, whose norm is
\(\Theta(H\sqrt N)=\Theta(N)\), while the ancestor-product formula bounds the
inverse Frobenius norm by \(O(N)\). Hence its condition is indeed
\(\Theta(N)\).

Status: **proof complete in the stated coefficient-oracle and output model;
apparently new after the targeted search.**
