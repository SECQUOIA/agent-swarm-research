# A trajectory-level direct-sum lower bound for a sparse box LP

Status: Proved; independently audited; quantum upper corrected for joint success
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the stated checkpoint-increment contract; moderate on novelty

## Result

The scalar-inequality LP in the
[parameterized scalar-frontier note](2026-09-04-parameterized-one-cone-scalar-frontier.md)
can multiplex \(B\) independent Forrelation instances along one central
path. This gives a genuine trajectory statement rather than repeating one
diagnostic at one point.

For each block \(i\in[B]\), let \(M_i,e,a_i\) be an independent copy of the
cyclic inverse-history construction, with the same public parameters
\(K,q,r,\ell,\delta\). Thus

\[
 \|M_i\|=1,\qquad \sigma_{\min}(M_i)=K^{-1},\qquad
 a_i^TM_i^{-1}e=h\Phi_i,\qquad h=\sqrt p=\Theta(\delta),       \tag{1}
\]

where \(\Phi_i\) is the hidden Forrelation amplitude and every \(a_i\) is a
public clock-supported vector. Fix the public constant \(\Gamma=2^{20}\),
put

\[
 \theta_i=\Gamma^{-i},\qquad
 \eta_j=\Gamma^{j+1/2},\qquad 0\leq j\leq B,                \tag{2}
\]

and consider the single block-diagonal LP

\[
 \boxed{
 \begin{aligned}
  \max_{x_1,\ldots,x_B}\quad &
       2\sum_{i=1}^B\theta_i e^TM_ix_i,\\
  \text{subject to}\quad &-\mathbf1\leq M_ix_i\leq\mathbf1
       \quad(i\in[B]).
 \end{aligned}}                                             \tag{3}
\]

Append one free accumulator coordinate, using a public three-sparse partial-
sum chain, so that

\[
 w=\sum_{i=1}^B a_i^Tx_i.                                  \tag{4}
\]

Let \(w(\eta)\) denote this coordinate at the exact logarithmic central point
with objective multiplier \(\eta\), and define its selected path increments

\[
 D_j=w(\eta_j)-w(\eta_{j-1}),\qquad j\in[B].               \tag{5}
\]

There is a universal \(c>0\) such that the following checkpoint-increment
problem has bounded-error classical full-SQ query complexity

\[
 \boxed{
 R_{\rm SQ}^{\rm traj}(B)
 =\Omega\!\left(
   B\frac{q^{\ell/2}}{r\ell}
  \right).}                                                \tag{6}
\]

The problem is to return all \(B\) numbers \(D_j\) to additive error at most
\(ch\), with joint success probability at least \(2/3\), under the independent
promises

\[
 |\Phi_i|\leq\alpha=1/100
 \quad\hbox{or}\quad
 \Phi_i\geq\beta=3/5.                                    \tag{7}
\]

The same lower bound applies if an algorithm instead returns the accumulator
coordinate of every checkpoint to error \(ch/2\), since differencing those
outputs solves (5). It also applies to any stronger contract returning full
classical central points with that coordinatewise accuracy.

For fixed \(k\)-Forrelation, choose the promise constants
\(\alpha_k<\beta_k\), a public

\[
 \Gamma_k\geq
 \left(\frac{12}{\beta_k-\alpha_k}\right)^2,
\]

and an output constant \(c_k=2^{-O(k)}\) below one quarter of the resulting
increment gap.  The same construction then gives

\[
 R_{\rm SQ}^{\rm traj}(B)
 =\widetilde\Omega_k\!\left(BN_0^{\,1-1/k}\right),          \tag{8}
\]

where \(N_0\) is one block's ambient dimension. The total LP dimension is
\(\mathcal N=\Theta(BN_0)\), so (8) is equivalently
\(\widetilde\Omega_k(B^{1/k}\mathcal N^{1-1/k})\), for returning every
increment to additive error \(c_kh\).  The fixed value
\(\Gamma=2^{20}\) and universal \(c=0.21\) above are only for the
2-Forrelation promise (7).

For 2-Forrelation, the structured quantum source algorithm returns the whole
increment trace with joint success at least \(2/3\) using \(O(B)\) hidden
queries at the displayed \(c=0.21\) accuracy.  It robustly recovers all
promise bits and outputs a fixed representative for the corresponding low or
high amplitude interval.  Direct numerical amplitude estimation gives the
stronger \(c=1/100\) accuracy in \(O(B\log B)\) queries.  For signed fixed
\(k\)-Forrelation, the audited generic upper remains
\(2^{O(k)}B\log B\), since the Boolean promise bit alone does not determine
the sign of the numerical increment.  These quantum uppers are for the
source-equivalent cyclic realization, not for a generic QIPM given arbitrary
sparse matrices.

## Exact central path and the almost-diagonal increment kernel

Use coordinates \(u_i=M_ix_i\). The barrier subproblem for (3) is

\[
 F_\eta(u)=
 -\sum_{i=1}^B\sum_t\log(1-u_{i,t}^2)
 -2\eta\sum_{i=1}^B\theta_i e^Tu_i.                       \tag{9}
\]

It is separable and strictly convex. If

\[
 \rho(z)=\frac{\sqrt{1+4z^2}-1}{2z}
        =\frac{2z}{1+\sqrt{1+4z^2}},\qquad \rho(0)=0,      \tag{10}
\]

then \(\rho/(1-\rho^2)=z\), and the exact path is

\[
 u_i(\eta)=\rho(\eta\theta_i)e,\qquad
 x_i(\eta)=\rho(\eta\theta_i)M_i^{-1}e.                  \tag{11}
\]

Equations (1), (4), and (11) give

\[
 \frac{D_j}{h}
 =\sum_{i=1}^B
 \left[\rho(\Gamma^{j-i+1/2})
       -\rho(\Gamma^{j-i-1/2})\right]\Phi_i.             \tag{12}
\]

Define the nonnegative convolution kernel

\[
 d_m=\rho(\Gamma^{m+1/2})-\rho(\Gamma^{m-1/2}),
 \qquad m\in\mathbb Z.                                   \tag{13}
\]

It telescopes to

\[
 \sum_{m\in\mathbb Z}d_m=1,                              \tag{14}
\]

because \(\rho(0)=0\) and \(\rho(+\infty)=1\). Moreover,

\[
 \rho(z)\leq z,\qquad
 1-\rho(z)=\frac{\rho(z)}{z(1+\rho(z))}\leq\frac1{2z}.
                                                                    \tag{15}
\]

Consequently the main coefficient and the total off-diagonal leakage obey

\[
 d_0\geq1-\frac{3}{2\sqrt\Gamma},\qquad
 \sum_{m\ne0}d_m=1-d_0\leq\frac{3}{2\sqrt\Gamma}.        \tag{16}
\]

Truncating the infinite sum to the \(B\) actual blocks can only reduce the
leakage. Since every real Forrelation amplitude has absolute value at most
one, (12) therefore implies

\[
 \left|\frac{D_j}{h}-d_0\Phi_j\right|
 \leq \tau_\Gamma:=1-d_0.                                \tag{17}
\]

For the weaker choice \(\Gamma=256\), already \(d_0\geq29/32\) and
\(\tau_\Gamma\leq3/32\), so the choice \(\Gamma=2^{20}\) used in the theorem
has still more slack. A low instance satisfies

\[
 |D_j|/h\leq d_0\alpha+\tau_\Gamma,
\]

whereas a high instance satisfies

\[
 D_j/h\geq d_0\beta-\tau_\Gamma.
\]

The gap between these two intervals is at least

\[
 g_\Gamma=d_0(\beta-\alpha)-2\tau_\Gamma>0.34.           \tag{18}
\]

Hence any \(c<g_\Gamma/2\) lets one
recover all \(B\) promise bits from the increment trace.

This is the reason for placing the checkpoints halfway between consecutive
objective scales. Over its assigned multiplicative interval, block \(j\)
moves from \(O(\Gamma^{-1/2})\) to \(1-O(\Gamma^{-1/2})\), while the total
movement of every other block is only \(O(\Gamma^{-1/2})\), independently of
\(B\).

## Approximate-centering corollary

The exact-checkpoint statement is stable under a standard barrier-subproblem
gap. Let \(u(\eta)\) be the minimizer in (9), and suppose a returned point
\(\widehat u(\eta)\) is exactly feasible and satisfies

\[
 F_\eta(\widehat u(\eta))-F_\eta(u(\eta))\leq\zeta.        \tag{19}
\]

Every scalar interval barrier has second derivative

\[
 \frac{2(1+u^2)}{(1-u^2)^2}\geq2.
\]

Therefore strong convexity gives

\[
 \|\widehat u(\eta)-u(\eta)\|_2\leq\sqrt\zeta.             \tag{20}
\]

Write \(b_i=M_i^{-T}a_i\). The one-block construction gives
\(\|b_i\|\leq K_{\rm eff}\leq\sqrt K\), so the error in the shared
accumulator is at most

\[
 |\widehat w(\eta)-w(\eta)|
 \leq\left(\sum_{i=1}^B\|b_i\|^2\right)^{1/2}
       \|\widehat u(\eta)-u(\eta)\|
 \leq\sqrt{BK\zeta}.                                      \tag{21}
\]

Consequently, returning such a point at every selected checkpoint with

\[
 \boxed{\quad \zeta\leq \frac{c^2h^2}{16BK}
       =\Theta\!\left(\frac{\delta^2}{BK}\right) \quad}    \tag{22}
\]

lets one difference consecutive accumulator coordinates with total error at
most \(ch/2\). The direct-sum lower bound (6) therefore also holds for this
approximate-centering trajectory contract. The accumulator equality (4) must
be enforced exactly, or the scalar must be evaluated directly from the
returned \(x_i\)'s. An approximate equality residual requires its own error
budget.

## Direct-sum query proof

Let

\[
 L_0=\Omega\!\left(\frac{q^{\ell/2}}{r\ell}\right)       \tag{23}
\]

be the randomized query lower bound for one 2-Forrelation promise bit, at
any fixed error strictly below \(1/2\). The standard minimax theorem supplies
a hard distribution \(\mu\) over one promised instance. This is the
[Aaronson--Ambainis Forrelation lower bound](https://doi.org/10.1137/15M1050902);
the fixed-\(k\) replacement is due to
[Bansal--Sinha](https://arxiv.org/abs/2008.07003).

Suppose a randomized classical full-SQ algorithm \(A\) solves the \(B\)-block
increment problem using \(Q\) queries and joint success probability at least
\(2/3\) on every promised input. Draw \(B\) independent inputs from \(\mu\),
put a target input in a uniformly random block \(I\), and simulate all other
blocks for free. In the query model the simulator may sample and store the
filler truth tables without charge; only queries to the target oracle are
counted. A sparse-value or sparse-location query names one block. A global
SQ sample returns one sampled block and one entry. Public row norms, column
norms, mixture weights, objective scales, and accumulator coefficients need
no hidden query. Therefore the expected number of target queries is at most
\(Q/B\), even for an adaptive algorithm.  For a global SQ sample, the key
point is that the assembled input is distributed as \(\mu^B\) and is
independent of the uniformly hidden target location \(I\): the target and
all fillers have the same law.  Every named query or returned sample touches
only one block, so averaging its block indicator against this independent
\(I\) gives \(1/B\), regardless of public nonuniform block-sampling weights.

Whenever \(A\) gets the whole trace right, (18) makes its decoded target bit
right. Abort the simulation if it uses more than \(12Q/B\) target queries.
Markov's inequality loses at most \(1/12\) success probability, leaving a
constant bias above \(1/2\). Constantly many repetitions amplify that bias
to \(2/3\). Equation (23) then implies \(Q/B=\Omega(L_0)\), proving (6).

The argument is a direct-sum theorem for classical randomized SQ access. It
does not assume that the algorithm queries the blocks in advance or follows
the displayed checkpoints sequentially. It does rely on the ordinary
classical interface in which one query returns one sampled or addressed data
item; it is not a quantum direct-sum lower bound for a coherent superposition
over block indices.

The fixed-\(k\) statement follows identically from the distributional
\(k\)-Forrelation lower bound used in the base construction, after replacing
\(\Gamma,c,\alpha,\beta\) by the \(k\)-dependent constants specified below
(8).  If the high promise is \(|\Phi_i|\geq\beta_k\), decode by thresholding
\(|D_j|\); the same leakage calculation applies.

## Access, sparsity, and path length

The inequality matrix of (3) is the stack of the block-diagonal matrices
\(M_i\) and \(-M_i\). Its row and column sparsity remains
\(s=\Theta(q)\). Each accumulator coefficient in (4) is public, and a
three-sparse chain over all \(O(BT)\) supported accumulator terms keeps the
augmented row and column sparsity \(\Theta(q)\); in particular, (4) is not
retained as one dense row.  Since one block already has
\(N_0=\Theta(Tq^\ell)\) coordinates, these auxiliaries preserve total
dimension \(\Theta(BN_0)\). The objective has public geometric block weights. Its SQ
mixture weights are also public, and an entry query has constant hidden-sign
overhead. Thus one full-SQ query to the multiplexed LP costs at most a
constant number of indexed source queries.

The selected multiplier range is

\[
 \log(\eta_B/\eta_0)=B\log\Gamma.                         \tag{24}
\]

Thus the number \(B\) of independently hard increments is proportional to
the logarithmic length of the prescribed multiplier interval. A conventional
short-step method may insert intermediate centers between the selected
checkpoints; returning the selected increment trace remains a consequence of
returning that finer classical trajectory.
For the fixed-\(k\) extension, replace \(\Gamma\) by \(\Gamma_k\); then the
range is \(B\log\Gamma_k=O_k(B)\), so the fixed-\(k\) dimension and
trajectory-length scalings are unchanged.

At the public analytic center the reduced Hessian is block diagonal with
blocks \(2M_i^TM_i\), hence has condition number \(K^2\). No uniform
condition-number claim is made over the geometrically scaled trajectory:
old blocks approach the box boundary and their barrier curvature grows.
Likewise, the standard box barrier has parameter \(BN_0\). The result is an
output/access lower bound for a specified sparse LP central-path trace, not a
claim that every optimization method must execute \(B\) path-following steps
or that a generic QLSA enjoys the structured quantum upper bound.

## Quantum comparison

For increment \(j\), estimate \(\Phi_j\) to a sufficiently small constant
additive error with the source Forrelation circuit and output

\[
 \widehat D_j=h d_0\widehat\Phi_j.                        \tag{25}
\]

By (17), the omitted contribution of all other blocks is at most
\(h\tau_\Gamma\). For \(\Gamma=2^{20}\), this is less than \(0.0015h\);
estimating \(\Phi_j\) to error \(0.005\) makes the total error less than
\(0.007h<ch\) for \(c=1/100\).  To meet the joint-success contract for all
\(B\) increments, set each estimate's failure probability to \(O(1/B)\).
Standard repetition and a median use \(O(\log B)\) hidden queries for
2-Forrelation, or \(2^{O(k)}\log B\) for fixed \(k\)-Forrelation, per
increment.  This proves the total \(O(B\log B)\) and
\(2^{O(k)}B\log B\) upper bounds stated above.

Estimating every amplitude only to constant individual success would use
\(O(B)\) queries but would not establish joint success probability \(2/3\).
The needed collective argument is supplied by Corollary 3 of
Buhrman--Newman--Roehrig--de Wolf's *Robust Polynomials and Quantum
Algorithms*: \(B\) bounded-error Boolean subroutines can have all their
output bits recovered jointly with probability at least \(2/3\) using
\(O(BT)\) coherent invocations when one subroutine costs \(T\).  The theorem
treats the subroutines as black-box unitaries, so it applies to valid promised
Forrelation inputs.  Controlled block selection uses the indexed source
oracle, and the public Forrelation circuit supplies the required inverses.

Run this recovery algorithm on the \(B\) low/high promise bits.  If block
\(j\) is low, output \(0\); if it is high, output \(0.8h d_0\).  In the low
case, (17) bounds the error by
\((0.01d_0+\tau_\Gamma)h<0.012h\).  In the high case, the midpoint of
\([0.6d_0, d_0]\) has intrinsic error at most \(0.2d_0h\), so leakage makes
the total less than \(0.202h\).  Both are below \(0.21h\).  Meanwhile the
low/high increment intervals are separated by more than \(0.586h\) for
\(\Gamma=2^{20}\), so an additive \(0.21h\) output still implies the
classical decoding lower bound.  This proves the joint-success \(O(B)\)
upper stated above.  It uses the positive high-amplitude promise of
2-Forrelation and does not extend verbatim to a signed high case.

These near-linear quantum comparisons apply to the increment trace. Returning every
absolute checkpoint value \(w(\eta_j)\) to \(O(h)\) error is a stronger
numerical task because it includes a growing prefix sum of the actual
amplitudes. The elementary quantum procedure for that stronger task can
cost \(O(B^2\log B)\) hidden queries under a joint-success contract. The
lower bound (6) still applies, but no matching near-linear quantum upper bound
is claimed for absolute checkpoint values.

## Novelty and limitation

The ingredients are elementary: block-diagonal direct sums, geometric
objective scaling, and the scalar box central path. The potentially useful
new point is their combination into one sparse LP whose *successive path
increments* carry independent hard query problems with only constant total
cross-talk. This converts the earlier one-checkpoint diagnostic into a
trajectory lower bound linear in the number of selected logarithmic path
intervals while preserving sparsity and constant hidden-query overhead.

The contract is intentionally path-following-specific. It does not lower-
bound algorithms asked only for an optimal value or one final optimizer, and
it does not prove that the same direct sum is necessary if a solver may return
an unrelated compressed certificate. A single absolute checkpoint is not
being advertised as containing \(B\) independently recoverable answers at
the stated precision; the information is isolated by the sequence of
increments.

The decision-tree direct-sum step itself is standard; see, for example,
[Blais--Brody](https://arxiv.org/abs/1908.01020) and the earlier results
cited there.
[Buhrman--Newman--Roehrig--de Wolf](https://arxiv.org/abs/quant-ph/0309220)
prove the robust quantum direct-sum recovery theorem used for the
joint-success \(O(B)\) upper. Apers--Gribling also use independent OR blocks and a direct
product/direct-sum theorem for a matrix spectral-approximation lower bound in
their [LP IPM work](https://arxiv.org/abs/2311.03215). A targeted search found
no result that geometrically multiplexes independent query problems into
successive scalar increments of one LP logarithmic central path. Accordingly,
the novelty claim is only for that access-preserving path wrapper and its
leakage analysis, not for the direct-sum lemma or the box path in isolation.
