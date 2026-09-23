# A direct-sum trajectory lower bound for standard SOCP Newton decrements

Status: Proved; independently audited; iterate-access scope and quantum upper corrected
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the theorem; moderate on novelty

## Main theorem

There is a single sparse SOCP whose ordinary predictor Newton decrements at
\(B\) specified central-path checkpoints encode \(B\) independent
Forrelation instances.

For every block \(i\in[B]\), take an independent copy of the cyclic family
from the
[parameterized scalar-frontier note](2026-09-04-parameterized-one-cone-scalar-frontier.md).
It supplies \(M_i,e,a_i\) and public numbers \(h,G,\lambda_{\rm n}\) such
that

\[
 \|M_i\|=1,\qquad \sigma_{\min}(M_i)=K^{-1},\qquad
 g_i=M_i^{-T}a_i,\qquad \lambda_{\rm n}=\frac1{2G},        \tag{1}
\]

\[
 \|e+\lambda_{\rm n}g_i\|^2
 =C+\epsilon\Phi_i,\qquad
 C=\frac54,\qquad \epsilon=\frac hG
 =\Theta\!\left(\frac{\delta}{\sqrt K}\right).             \tag{2}
\]

Here \(\Phi_i\) is the hidden Forrelation amplitude, while \(h,G\), and
\(\lambda_{\rm n}\) are exactly public. Reduce the universal upper bound on
\(\delta\), if needed, so that

\[
 \xi:=\epsilon/C\leq\frac14.                              \tag{3}
\]

Fix a public constant \(\Gamma\geq256\), and set

\[
 \theta_i=\frac{\Gamma^{-i}}{\sqrt C},\qquad
 \eta_j=\Gamma^j,\qquad j\in[B].                          \tag{4}
\]

The multiplexed SOCP is

\[
 \boxed{
 \begin{aligned}
 \max\quad&
 2\sum_{i=1}^B\theta_i(e^Tu_i+\lambda_{\rm n}a_i^Tx_i),\\
 \text{subject to}\quad&
 u_i=M_ix_i,\qquad
 (1,u_i)\in Q_{N_0+1}\quad(i\in[B]).
 \end{aligned}}                                           \tag{5}
\]

The vectors \(a_i\) are public and sparse, so no accumulator variable is
needed. Let \(z(\eta)\) be the exact logarithmic central point of (5). At
\(z(\eta_j)\), propose the public relative multiplier update

\[
 \eta_j\longmapsto(1+\sigma)\eta_j,\qquad
 \sigma=\frac{\sigma_0}{\sqrt B},                         \tag{6}
\]

where \(\sigma_0>0\) is a sufficiently small constant. Denote the ordinary
squared Newton decrement of this predictor correction by
\(\Lambda_j^2\).

From full-SQ access to the SOCP formulation data, with the checkpoints defined
implicitly by the exact central-path equations, returning all \(B\) values
\(\Lambda_j^2\) to additive accuracy

\[
 c\sigma^2\xi
 =\Theta\!\left(\frac{\delta}{BK^{1/2}}\right)             \tag{7}
\]

with joint success probability at least \(2/3\) requires

\[
 \boxed{
 Q_{\rm classical}
 =\Omega\!\left(
 B\frac{q^{\ell/2}}{r\ell}
 \right)}                                                 \tag{8}
\]

classical full-SQ queries. For fixed \(k\)-Forrelation, define

\[
 \Delta_k=\frac{2\beta_k}{6^{3/2}}-\frac{\alpha_k}{4}>0
\]

for the standard promise constants, choose
\(\Gamma_k\geq1+1.6/\Delta_k\), and replace \(c\) by any
\(c_k<\Delta_k/8=2^{-O(k)}\).  The result then becomes

\[
 \boxed{
 Q_{\rm classical}
 =\widetilde\Omega_k\!\left(BN_0^{\,1-1/k}\right)
 =\widetilde\Omega_k\!\left(
 B^{1/k}\mathcal N^{\,1-1/k}\right),}                     \tag{9}
\]

where \(\mathcal N=\Theta(BN_0)\) is the total dimension.
The fixed value \(\Gamma\geq256\) and universal accuracy constant in (7)
apply only to the 2-Forrelation promise (20).

For 2-Forrelation there is also a joint-success linear-query point: specialize
to \(\Gamma=2^{20}\) and take \(c=0.036\) in (7).  The structured
source-equivalent quantum algorithm then returns the whole decrement trace
with joint success at least \(2/3\) using \(O(B)\) hidden queries.  At the
stricter \(c=1/100\), direct independent numerical estimation gives
\(O(B\log B)\).  For fixed \(k\), the audited generic bound remains
\(2^{O(k)}B\log B\). The product Lorentz
barrier has parameter \(2B\), and (6) makes every proposed predictor
decrement \(O(1)\). Thus the diagnostic is at the natural short-step scale;
it is not an artificially large jump between the geometrically separated
reporting checkpoints.

Equivalently, define the publicly normalized diagnostic
\(P_j=\Lambda_j^2/\sigma^2\). Its required accuracy is
\(\Theta(\delta/\sqrt K)\), independent of \(B\).

This is not a local-diagnostic lower bound when an exact SQ oracle for the
central iterate is supplied as an additional input. Such an oracle normally
reveals block norms, while

\[
 \|u_j(\eta_j)\|
 =\rho\!\left(\sqrt{1+\xi\Phi_j}\right),
\]

which directly exposes the target amplitude. The theorem charges the
queries needed to obtain the trajectory diagnostic from the formulation
data; it does not assume free iterate-SQ access.

This observation also gives a dynamic-access corollary rather than merely a
caveat. At checkpoint \(j\), the active block has

\[
 r_j:=\|u_j(\eta_j)\|
 =\rho\!\left(\sqrt{1+\xi\Phi_j}\right).
\]

For \(\xi\leq1/4\) and \(|\Phi_j|\leq1\), its argument lies in
\([\sqrt{3/4},\sqrt{5/4}]\). On this interval
\(\rho<2/3\), because \((2/3)/(1-(2/3)^2)=6/5>\sqrt{5/4}\), and implicit
differentiation gives

\[
 \rho'(z)=\frac{(1-\rho(z)^2)^2}{1+\rho(z)^2}
 \geq\frac{25}{117}.
\]

Therefore

\[
 \frac{d r_j}{d\Phi_j}
 =\rho'\!\left(\sqrt{1+\xi\Phi_j}\right)
   \frac{\xi}{2\sqrt{1+\xi\Phi_j}}
 \geq\frac{25}{117\sqrt5}\,\xi.
\]

The low and high 2-Forrelation block-norm intervals are consequently
separated by more than \(0.056\xi\). Constructing, from formulation access,
a trajectory SQ interface that reports every active cone-block norm to
additive error \(\xi/50\) therefore also requires the classical direct-sum
cost (8). Thus an assumption of free exact checkpoint-iterate SQ access does
not refute the lower bound; it places the hard work in dynamic data-structure
construction. This corollary is only for interfaces exposing conditional
cone-block norms, not for a normalized quantum state with its norm withheld.

## Exact decrement formula

Use \(x_i=M_i^{-1}u_i\), and write

\[
 v_i=e+\lambda_{\rm n}g_i,\qquad s_i=\|v_i\|
 =\sqrt{C+\epsilon\Phi_i}.
\]

The barrier on block \(i\) is

\[
 \phi_i(u_i)=-\log(1-\|u_i\|^2).
\]

Rotational symmetry makes its central point radial:

\[
 u_i(\eta)=\rho(\eta\theta_i s_i)\frac{v_i}{s_i},\qquad
 \frac{\rho(z)}{1-\rho(z)^2}=z.                           \tag{10}
\]

At \(u=r\,v_i/s_i\), the radial eigenvalue of the barrier Hessian is

\[
 H_{\rm rad}(r)=\frac{2(1+r^2)}{(1-r^2)^2}.               \tag{11}
\]

Changing the multiplier by \(\sigma\eta\) leaves the point fixed and creates
the block residual \(2\sigma\eta\theta_i v_i\). Its squared Newton decrement
is therefore

\[
 \begin{aligned}
 \Lambda_i^2(\eta)
 &=4\sigma^2\eta^2\theta_i^2s_i^2
   \frac{(1-r_i^2)^2}{2(1+r_i^2)}\\
 &=\sigma^2 f(\eta\theta_i s_i),
 \end{aligned}                                            \tag{12}
\]

where

\[
 f(z)=\frac{2\rho(z)^2}{1+\rho(z)^2}
 =1-\frac1{\sqrt{1+4z^2}}.                               \tag{13}
\]

The blocks are independent, so the exact total diagnostic at checkpoint
\(j\) is

\[
 \boxed{
 \frac{\Lambda_j^2}{\sigma^2}
 =\sum_{i=1}^B
 f\!\left(\Gamma^{j-i}\sqrt{1+\xi\Phi_i}\right).}         \tag{14}
\]

In particular \(0\leq\Lambda_j^2\leq B\sigma^2=\sigma_0^2\), proving the
short-step-scale assertion.

## A diagonal sensitivity kernel

Subtract the public all-zero baseline

\[
 P_j^0=\sum_{i=1}^B f(\Gamma^{j-i}),\qquad
 E_j=\frac{\Lambda_j^2}{\sigma^2}-P_j^0.                  \tag{15}
\]

For a scale \(z>0\), define

\[
 \psi_z(x)=f(z\sqrt{1+\xi x})-f(z).
\]

Direct differentiation gives the exact formula

\[
 \psi_z'(x)
 =\frac{2\xi z^2}
 {\left(1+4z^2(1+\xi x)\right)^{3/2}}.                   \tag{16}
\]

Since \(|x|\leq1\) and \(\xi\leq1/4\), at the main scale \(z=1\),

\[
 \frac{2\xi}{6^{3/2}}
 \leq\psi_1'(x)\leq\frac{\xi}{4}.                         \tag{17}
\]

For every scale,

\[
 0\leq\psi_z'(x)
 \leq\frac{2\xi z^2}{(1+3z^2)^{3/2}}.                    \tag{18}
\]

Hence all off-diagonal blocks at checkpoint \(j\) contribute at most

\[
 \begin{aligned}
 T_\Gamma
 &:=\sum_{i\ne j}|\psi_{\Gamma^{j-i}}(\Phi_i)|\\
 &\leq\xi\left[
 \frac{2}{3^{3/2}}\frac{\Gamma^{-1}}{1-\Gamma^{-1}}
 +2\frac{\Gamma^{-2}}{1-\Gamma^{-2}}
 \right]
 \leq\frac{0.4\xi}{\Gamma-1}.                            \tag{19}
 \end{aligned}
\]

The first series bounds already activated blocks \(i<j\), using
\((1+3z^2)^{3/2}\geq3^{3/2}z^3\); the second bounds not-yet-activated blocks
\(i>j\), using the denominator lower bound one. Boundary truncation only
decreases both sums.

Under the 2-Forrelation promise

\[
 |\Phi_i|\leq\alpha=1/100
 \quad\text{or}\quad
 \Phi_i\geq\beta=3/5,                                    \tag{20}
\]

a low instance at position \(j\) satisfies

\[
 |E_j|\leq\frac{\xi\alpha}{4}+T_\Gamma,                  \tag{21}
\]

whereas a high instance satisfies

\[
 E_j\geq\frac{2\xi\beta}{6^{3/2}}-T_\Gamma.              \tag{22}
\]

For \(\Gamma\geq256\), the normalized gap between (21) and (22) is more than
\(0.075\xi\). Therefore an additive \(c\xi\) approximation to
\(\Lambda_j^2/\sigma^2\), for example with \(c=1/100\), recovers the \(j\)th
promise bit. For the signed fixed-\(k\) promise, use the absolute deviation
\(|E_j|\). Monotonicity and (17), together with the choice
\(\Gamma_k\geq1+1.6/\Delta_k\), leave a gap at least
\(\Delta_k\xi/2=2^{-O(k)}\xi\).

Unlike the shared-accumulator LP construction, each reporting checkpoint now
uses one standard scalar diagnostic. The localization comes from the
band-pass sensitivity of the decrement function \(f\), not from differencing
two custom path observables.

## Classical direct sum and quantum upper bound

The direct-sum reduction is the same elementary random-embedding argument as
in the
[multiplexed LP note](2026-09-04-multiplexed-lp-central-path-direct-sum.md).
Choose the hard distribution for one Forrelation instance, place a target in
a uniformly random block, and sample all other blocks as free fillers. A
classical sparse or SQ query returns information from at most one indexed
hidden instance. Thus an algorithm making \(Q\) queries uses \(Q/B\) target
queries on average.  This remains true for global SQ sampling: because the
target and fillers are i.i.d. from the same hard distribution, the assembled
input is independent of the hidden uniform target location, and every
returned sample belongs to only one block. Public block-mixture weights do
not change the \(1/B\) average over that hidden location.  Truncate the
simulator after \(12Q/B\) target queries.  Markov's inequality costs at most
\(1/12\) success probability, so joint success at least \(2/3\) leaves
target success at least \(7/12>1/2\).  Constant repetition and majority vote
give a bounded-error one-instance algorithm with \(O(Q/B)\) queries, proving
(8). The fixed-\(k\) lower
bound follows from
[Bansal--Sinha](https://arxiv.org/abs/2008.07003).

One direct quantum method estimates only \(\Phi_j\) to constant accuracy and
outputs

\[
 \widehat P_j
 =P_j^0+\psi_1(\widehat\Phi_j).                           \tag{23}
\]

Equation (19) bounds the omitted blocks by \(O(\xi/\Gamma)\), while (17)
makes constant amplitude accuracy contribute \(O(\xi)\). One source
Forrelation estimator per checkpoint, amplified to failure probability
\(O(1/B)\), therefore gives the claimed \(O(B\log B)\), or
\(2^{O(k)}B\log B\), hidden-query bound.  Constant individual success would
use \(O(B)\) queries but would not meet the joint-success requirement.  No
collective \(O(B)\)-query numerical-estimation argument follows from this
method alone.

For 2-Forrelation, the logarithm can in fact be removed at a slightly looser
numerical accuracy.  Buhrman--Newman--Roehrig--de Wolf's robust input-recovery
theorem, Corollary 3 in *Robust Polynomials and Quantum Algorithms*, says
that \(B\) bounded-error Boolean subroutines can have all \(B\) output bits
recovered jointly with probability at least \(2/3\) using \(O(BT)\)
invocations when one subroutine costs \(T\).  The recovery procedure treats
the subroutines as coherent unitaries and therefore also applies on promised
Forrelation inputs.  A controlled choice of block is implemented by the
indexed source oracle, and the public circuit supplies the inverses required
by the recovery algorithm.

After recovering the promise bit, do not estimate \(\Phi_j\).  For a low bit,
output the midpoint of \(\psi_1([-\alpha,\alpha])\); for a high bit, output
the midpoint of \(\psi_1([\beta,1])\), in each case adding \(P_j^0\).  Uniformly
for \(\xi\leq1/4\), the two intrinsic midpoint errors are at most
\[
 0.001795\xi
 \quad\text{and}\quad
 0.035778\xi,
\]
respectively.  With \(\Gamma=2^{20}\), (19) is below
\(4\cdot10^{-7}\xi\).  Thus every reconstructed \(P_j\) has error below
\(0.036\xi\), jointly, using \(O(B)\) source queries.  The separation between
the low and high numerical intervals exceeds \(0.079\xi\) at this \(\Gamma\),
so the same relaxed accuracy still implies the classical direct-sum lower
bound.  This Boolean-representative argument uses the one-sided high promise
of 2-Forrelation; it does not by itself give the signed fixed-\(k\) numerical
upper.

## Access and scope

The SOCP has \(B\) Lorentz blocks. Its equality matrix is block diagonal, so
row and column sparsity remains \(\Theta(q)\). The vectors \(a_i\), geometric
objective weights, and all SQ mixture probabilities are public.  In fact,
the two pieces of objective block \(i\) occupy disjoint \(u_i\)- and
\(x_i\)-registers and have squared norm
\[
 4\theta_i^2\bigl(1+\lambda_{\rm n}^2\|a_i\|^2\bigr),
\]
where \(\|a_i\|=1/R\) is public.  Exact objective norms and global or
conditional squared-coordinate sampling therefore reveal no \(\Phi_i\).
Every data query is simulated with constant indexed hidden-sign overhead,
exactly as in the one-block theorem.  The current formulation writes
\(\lambda_{\rm n}a_i^Tx_i\) directly in the objective and therefore needs no
accumulator equality.  If designated \(w_i\) coordinates are retained, each
must instead use the base construction's \(O(T)\)-row three-sparse chain;
this adds \(O(BT)\) public rows but preserves sparsity and total dimension
\(\Theta(BN_0)\).

The lower bound starts from full-SQ access to the conic formulation, not from
an exact SQ oracle for the checkpoint central iterate or Newton residual.
This distinction is essential: standard SQ access reports vector norms, and
at the main block
\(\|u_j(\eta_j)\|=\rho(\sqrt{1+\xi\Phi_j})\), which already reveals the
answer. Likewise, supplying the residual together with its exact
normalization supplies the hard decrement by definition. Entry/location
access to a checkpoint system might still be simulable, but any such local
diagnostic lower bound needs a separately specified nonleaking access model
and is not proved here.

The selected path range has

\[
 \log(\eta_B/\eta_1)=(B-1)\log\Gamma.                     \tag{24}
\]

The lower bound is therefore linear both in the number of reported
checkpoints and in this logarithmic multiplier range. Conventional
path-following may insert the required intermediate short steps; (6) is the
local update used at each selected reporting point.

The ideal-real oracle statement treats the public coefficients
\(\Gamma^{-i}\) exactly.  A finite-bit implementation needs
\(O(B\log\Gamma+\log(1/\xi))\) coefficient bits to preserve the smallest
objective weight and the requested additive accuracy; no bit-complexity
claim is made here.
For fixed \(k\), replace \(\Gamma\) by \(\Gamma_k\); then the range is
\((B-1)\log\Gamma_k=O_k(B)\).

No uniform condition-number bound is claimed along the full scaled
trajectory. Earlier blocks approach their cone boundaries, and the reduced
barrier Hessian can become ill-conditioned across blocks. Nor is (8) a lower
bound for algorithms asked only for the final optimal value. It is a
trajectory-level lower bound for returning a standard path-following
diagnostic at prescribed central points from formulation access. It does not
survive free exact norm-reporting SQ access to those iterates. The structured
quantum upper bound uses the source-equivalent cyclic representation and is
not a generic QLSA upper bound.

The high-dimensional Lorentz blocks give barrier parameter \(2B\),
independent of \(N_0\). Replacing them by exact bounded-dimension norm trees
would increase the standard product-barrier parameter to
\(\Theta(BN_0)\), as explained in the
[SOC granularity note](2026-09-04-soc-granularity-barrier-tradeoff.md).

## Novelty screen

The Forrelation lower bounds and randomized direct-sum step are established
ingredients: see
[Aaronson--Ambainis](https://doi.org/10.1137/15M1050902),
[Bansal--Sinha](https://arxiv.org/abs/2008.07003), and
[Blais--Brody](https://arxiv.org/abs/1908.01020).
[Buhrman--Newman--Roehrig--de Wolf](https://arxiv.org/abs/quant-ph/0309220)
prove the robust quantum input-recovery/direct-sum theorem used for the
joint-success \(O(B)\) upper; that recovery theorem is prior work.
Apers--Gribling use independent OR blocks for a matrix
spectral-approximation lower bound in their
[quantum LP IPM paper](https://arxiv.org/abs/2311.03215).
A targeted search found no prior theorem embedding a classical direct sum
into the sequence of standard Newton decrements along one conic central path.
The apparent new content is the radial decrement identity (14), geometric
sensitivity localization (16)--(19), and its access-preserving sparse SOCP
wrapper. Priority is not established.
