# Exponential matched-access separation for a one-cone SOCP Newton state

Status: Proved; independently audited and targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate on apparent novelty of the transfer  

## Main theorem

Fix a sufficiently large constant \(k\).  There is a family of dimension-\(N\)
SOCPs with one Lorentz cone, a three-sparse data matrix
\(M\in\mathbb R^{N\times N}\), and \(\kappa_2(M)=O(\log N)\), for which:

\[
 \boxed{\text{quantum }\operatorname{polylog}N
 \quad\text{versus}\quad
 \text{classical SQ }\Omega(N^{1-1/k})}
\]

queries suffice or are necessary to sample from a constant-relative-error
optimizer.  The same hard state is exactly the first reduced
Lorentz-barrier Newton direction from a public analytic center.  The reduced
Newton matrix is nine-sparse and has condition \(O(\log^2N)\).

This is an unconditional separation in the matched coherent-data/SQ model.
It is a compressed optimizer-sampling theorem, not a value-only or
explicit-vector theorem.

A cyclic-clock refinement below gives a full parameterized frontier.  For
condition \(K\), sparsity \(s\), and relative precision \(\zeta\), the
classical query exponent is
\(\Theta(K\log s\log(1/\zeta))\) on the explicit family, while the exact
optimizer state is also the first legal Newton state and has a structured
constant-hidden-query quantum preparation.

## Access-preserving Lorentz lift

Take a real symmetric invertible hard matrix \(M\) from
[Grønlund--Larsen](https://arxiv.org/abs/2411.02087), with a public rescaling
such that
\[
 \|M\|_2\leq1,\qquad \sigma_{\min}(M)\geq1/K,\qquad K=O(\log N),
\]
and consider

\[
 \begin{aligned}
 \max_{x,u}\quad &2e_1^Tu\\
 \text{s.t.}\quad &u=Mx,\\
 &(1,u)\in Q_{N+1},
 \end{aligned}                                      \tag{1}
\]

where \(Q_{N+1}=\{(t,u):t\geq\|u\|_2\}\).  Eliminating \(u\) gives

\[
 \max_x 2e_1^TMx\qquad\text{s.t.}\qquad \|Mx\|_2\leq1. \tag{2}
\]

Putting \(y=Mx\), the unique optimum is

\[
 y^*=e_1,\qquad x^*=M^{-1}e_1,\qquad \operatorname{OPT}=2.
\]

Each equality row \([M_i,-e_i]\) in (1) has at most four nonzeros and each
\(x\)-column has at most three.  The explicit Grønlund--Larsen Forrelation
family has equal row and column norms, so SQ access to this augmented
standard-form data is simulated from \(SQ(M)\) with constant overhead.

## Exact first-Newton identity

The pulled-back Lorentz barrier is

\[
 \phi(x)=-\log(1-\|Mx\|_2^2).
\]

It is an exact parameter-one self-concordant barrier after the displayed
elimination (the canonical logarithmically homogeneous barrier on the
unreduced Lorentz cone has parameter two).  For objective multiplier
\(\eta>0\), define

\[
 F_\eta(x)=\phi(x)-2\eta e_1^TMx.
\]

At the public analytic center \(x_0=0\),

\[
 \nabla F_\eta(0)=-2\eta Me_1,\qquad
 \nabla^2F_\eta(0)=2M^2.
\]

The first reduced Newton direction is therefore

\[
 \boxed{d_\eta=\eta M^{-1}e_1=\eta x^*.}              \tag{3}
\]

Its decrement and post-step slack are

\[
 \lambda_\eta^2=2\eta^2,\qquad
 1-\|Md_\eta\|^2=1-\eta^2.
\]

Thus, for example, \(\eta\leq1/(4\sqrt2)\) gives
\(\lambda_\eta\leq1/4\) and a strictly feasible full Newton step.  Equation
(3) implies exact equality of normalized states:

\[
 |d_\eta\rangle=|x^*\rangle.
\]

The whole exact central path stays on the same ray:

\[
 x(\eta)=\alpha(\eta)M^{-1}e_1,\qquad
 \frac{\alpha}{1-\alpha^2}=\eta,\qquad
 \alpha(\eta)=\frac{\sqrt{1+4\eta^2}-1}{2\eta}.
\]

Consequently every nonzero central point and path direction has the same
normalized high-dimensional state.  Once (3) is prepared, continuation to
objective gap \(\tau\) requires only scalar updates; a standard geometric
schedule takes \(O(\log(1/\tau))\) updates.

## Accuracy transfer

Let \(\widehat x\) be feasible for (2), and suppose its maximization gap is at
most \(\tau\):

\[
 2-2e_1^TM\widehat x\leq\tau.
\]

Since \(\|M\widehat x\|\leq1\),

\[
 \|M\widehat x-e_1\|_2^2
 \leq2-2e_1^TM\widehat x\leq\tau.
\]

Using \(\|M^{-1}e_1\|\geq1\),

\[
 \boxed{
 \frac{\|\widehat x-x^*\|_2}{\|x^*\|_2}
 \leq K\sqrt{\tau}.}                                  \tag{4}
\]

Thus objective gap
\(\tau\leq\epsilon^2/K^2\) forces the
relative-\(\epsilon\) vector guarantee in the hard linear-system problem.
For the family here this is only inverse-polylogarithmic objective accuracy.

## Quantum upper and classical lower bounds

Theorem 1 of Grønlund--Larsen gives, for fixed sufficiently large \(k\) and a
corresponding constant \(\epsilon>0\), an
\(\Omega(N^{1-1/k})\) classical-query lower bound even with the strong
\(SQ(M)\) interface: entry queries, row and column \(\ell_2\)-sampling, and
norm queries.  The required output is only one sample from the squared
coordinates of a relative-\(\epsilon\) approximate solution of
\(Mx=e_1\).  Equations (1)--(4) transfer this lower bound with constant oracle
overhead to optimizer sampling for the SOCP and to sampling the first Newton
direction.

Quantumly, a sparse QLSA prepares \(|M^{-1}e_1\rangle\) in
\(\operatorname{polylog}N\) queries on this family.  Interpreted literally as
the first Newton solve, its Hessian \(2M^2\) has at most nine nonzeros per row
and column and

\[
 \kappa_2(2M^2)=\kappa_2(M)^2=O(\log^2N).
\]

A factor-aware implementation solves \(Md=e_1\) directly and retains the
better \(O(\kappa(M))\) condition dependence.  Both use the same coherent
data structure whose classical version supplies \(SQ(M)\).

The first-step sparsity is special.  Away from the exact central ray, the
rank-one term in the Lorentz-barrier Hessian can be dense.  The theorem does
not grant a free \(SQ(M^2)\) or Hessian oracle: every Newton-oracle use is
simulated from the original \(M\) access.

For the cyclic-clock refinement below, this last qualification can be
removed at the first step.  If \(M\) is its normalized symmetric dilation,
then

\[
 H_0=\nabla^2\phi(0)=2M^2,
 \qquad \kappa(H_0)=K^2,
 \qquad s(H_0)\leq 2q+1.                                  \tag{5a}
\]

Each diagonal block of \(M^2\) is a public multiple of

\[
 (1+\gamma^2)I-\gamma(U+U^T).
\]

The diagonal, forward-clock, and reverse-clock supports are disjoint.  Their
row and column norms are public, and sampling inside a transition block is
either uniform on a \(q\)-point Hadamard row or deterministic on a hidden
sign.  Consequently full \(SQ(H_0)\), as well as SQ access to the first
Newton right-hand side \(2\eta Me\), is simulated with only constant hidden
Forrelation-query overhead.  The parameterized lower bound therefore holds
even when the classical algorithm is handed the reduced Newton system
directly, rather than only the conic data.  Writing \(\kappa_H=\kappa(H_0)\)
and \(s_H=s(H_0)\), at fixed relative direction error it reads

\[
 \boxed{Q_{\rm SQ}(H_0^{-1}Me)
 =\exp\!\bigl(\Omega(\sqrt{\kappa_H}\log s_H)\bigr).}       \tag{5b}
\]

Under the exact-distribution or flagged-output contract stated below, its
precision-sensitive form is

\[
 Q_{\rm SQ}
 =\exp\!\left(\Omega\!\left(
 \sqrt{\kappa_H}\log s_H\log(1/\zeta)
 \right)\right)                                           \tag{5c}
\]

whenever \(\sqrt{\kappa_H}\log s_H\) exceeds a universal
constant, up to the explicit prefactor and polynomial denominator below.
Thus the lower bound is a direct sparse SPD Newton-direction sampling
theorem; it does not arise merely from an access gap between \(M\) and
\(M^2\).

## Parameterized cyclic-clock refinement

The joint lower family in the sparse-SQ frontier yields a stronger
conditioning--sparsity--precision version of the same SOCP theorem.  Let
\(K\geq3\), \(q=2^r\), and

\[
 \alpha_K=\log\frac{K+1}{K-1},\qquad
 \ell=\frac{\log(1/\zeta)}{6\alpha_K}+O(1).
\]

Use the cyclic-clock symmetric dilation \(M\), which has

\[
 \|M\|=1,qquad \kappa(M)=K,qquad
 s(M)\leq q+1,qquad N=\Theta(Tq^\ell).
\]

Its full SQ interface is simulated with constant hidden Forrelation-query
overhead because every row and column norm is public.  Applying (1) with the
public clock-basis vector \(e\), let \(L_c=3T\) be the clock period,
\(\gamma=(K-1)/(K+1)\), and \(z_0=\gamma^{L_c}\).  The optimizer norm is

\[
 R=\|M^{-1}e\|
 =\sqrt{K\frac{1+z_0}{1-z_0}},
\]

so its effective inverse sensitivity is

\[
 K_{\rm eff}=\frac{\|M^{-1}\|}{R}
 =\sqrt{K\frac{1-z_0}{1+z_0}}=\Theta(\sqrt K).              \tag{5}
\]

The last equality holds for the chosen clock, where \(z_0\) is bounded away
from one.  Hence any classical SQ algorithm that outputs an
\(x\)-coordinate sample from an exactly feasible point of gap

\[
 \tau\leq\zeta^2/K                                         \tag{6}
\]

must use

\[
 \boxed{
 Q=\Omega\!\left(\frac{\zeta q^{\ell/2}}{r\ell}\right).}    \tag{7}
\]

The augmented equality matrix \([M,-I]\) has row/column sparsity
\(\Theta(q)\), and its SQ interface is a public mixture of the \(M\) and
identity parts.  Equation (4), sharpened by (5), proves the reduction from
(6) to a
relative-\(\zeta\) inverse-state sampler.  Equivalently, at fixed
sufficiently small \(\zeta\),

\[
 Q=\exp(\Omega(K\log s)).                                   \tag{8}
\]

There is also a stronger ambient-dimension form at fixed precision.  Replace
2-Forrelation by \(k\)-Forrelation for any fixed admissible constant \(k\),
and decompose each global Hadamard into the same \(r\)-qubit blocks.  The
forward circuit then has \(T=\Theta(k\ell)\) layers, while its randomized
query lower bound is

\[
 \Omega\!\left(
   \left(\frac{q^\ell}{r\ell}\right)^{1-1/k}
 \right).
\]

Choosing the damping so that the final plateau has constant mass and
\(K=\Theta(T)\) gives a one-cone first-Newton family with

\[
 N=\Theta(Kq^\ell),\qquad
 Q=\widetilde\Omega_k(N^{1-1/k})
   =\exp(\Omega_k(K\log s)).                                \tag{8a}
\]

All matrix-SQ, Hessian-SQ, and Newton-right-hand-side simulations above
remain constant-query reductions.  Thus the joint conditioning--sparsity
lower exponent is compatible with a classical lower bound arbitrarily close
to linear in the ambient dimension (choose a large fixed \(k\)); the constant
hidden in \(\Omega_k\) deteriorates with \(k\), and the required fixed output
accuracy is correspondingly \(2^{-O(k)}\).

For the precision-sensitive construction, whenever \(K\log s\) exceeds a
universal constant,

\[
 Q=\exp\!\left(
 \Omega(K\log s\log(1/\zeta))
 \right),                                                   \tag{9}
\]

up to the explicit prefactor and polynomial denominator in (7).

The rare-event precision bound inherits the same output contract as the
linear-system theorem: each invocation's overall law must satisfy the
relative-solution guarantee, or failure must be flagged or
\(O(\zeta)\).  Unflagged constant failure can swamp the
\(\Theta(\zeta)\)-mass history plateau.  If a whole-variable sample is
returned, conditioning on the \(x\) block costs only a constant factor for
\(\zeta<1/2\).

For this explicit cyclic family, the lower exponent is tight even for exact
optimizer sampling.  Query the two hidden sign tables, each of size
\(q^\ell\), apply the \(O(\ell)\) block-Walsh--Hadamard layers to the full
amplitude vector, sample the public geometric clock, and sample the required
prefix-state distribution.  This uses

\[
 q^\ell\operatorname{poly}(\ell,r)
 =\exp\!\left(O(K\log s\log(1/\zeta))\right)                \tag{10}
\]

queries and arithmetic and produces the exact distribution of
\(x^*=M^{-1}e\), hence an exact feasible optimum.  Together with (7), this
proves

\[
 \log Q_{\rm classical}
 =\Theta(K\log s\log(1/\zeta))                              \tag{11}
\]

whenever the exponent dominates the explicit prefactors, including
\(\log Q=\Theta(K\log s)\) at fixed precision.

This exhaustive upper is specific to the constructed sign-oracle family.
On this family, a sign query is recovered from a designated sparse-\(M\)
entry query and full \(SQ(M)\) is simulated by a constant number of sign
queries, so the two source interfaces are constant-query equivalent.  It is
not an upper bound for arbitrary matrices supplied only through an unrelated
SQ data structure.

There is also a generic dimension-independent feasible-point upper envelope.
Construct a sparse polynomial inverse \(z=p(M)e\) with
\(\|Mz-e\|\leq\eta\), and normalize

\[
 x=z/\|Mz\|,\qquad u=Mz/\|Mz\|.
\]

This is exactly feasible, its \(x\)-sampling law is unchanged by the unknown
global normalization, and its angular objective gap is \(O(\eta^2)\).
Taking \(\eta=\Theta(\zeta/\sqrt K)\), the general sparse-SQ construction
costs

\[
 \exp\!\left(O(K\log s\log(\sqrt K/\zeta))\right)           \tag{12}
\]

at the certified accuracy (6).

Quantumly, the exact first Newton state remains \(|M^{-1}e\rangle\): it costs
\(\widetilde O(K)\) queries given a unit-normalized block encoding of the
cyclic factor, or \(\widetilde O(sK)\) under a generic sparse-value-to-block
encoding.  Hence the family gives a parameterized one-cone QIPM separation,
not only the fixed-sparsity \(K=\Theta(\log N)\) point furnished by the
Grønlund--Larsen instance.

In the native Forrelation realization, one can do better than generic QLSA
query complexity: prepare the public geometric clock and apply every circuit
gate controlled on whether the clock has passed it.  The two hidden diagonal
oracles occur once forward and once in reverse, so this uses \(O(1)\) hidden
source queries and \(\widetilde O(Tr)\) public gates, including geometric-clock
amplitude preparation and comparator overhead.  This uses the structured
sign-oracle realization, which is
constant-overhead equivalent to the constructed coherent sparse-\(M\) oracle;
it is not a generic conversion from a classical SQ interface to quantum
state access.

## Scope and prior-art boundary

The optimal value in (1) is the public constant two.  Hence the theorem says
nothing about value-only optimization.  Explicit construction of the
\(\Theta(N)\)-entry sparse table or QRAM, and explicit output of all
coordinates of \(x^*\), each costs \(\Omega(N)\).  Conventional hybrid QIPMs
that tomograph every direction do not inherit the separation.  The result is
for a specialized implicit/state-output primal-barrier IPM, and it uses one
high-dimensional Lorentz block rather than a product of bounded-size blocks.

The least-squares and ellipsoid-to-SOCP reductions are standard.
[Mande--Shao](https://quantum-journal.org/papers/q-2025-01-14-1593/) already
give SQ lower bounds for linear regression, and
[Apers--Gribling](https://doi.org/10.1137/25M1736098) give SQ lower bounds for
spectral approximation and LP value approximation.  Thus this is not the
first SQ lower bound for optimization or for a conic-representable task.
Existing quantum SOCP IPMs, including
[Kerenidis--Prakash--Szilágyi](https://quantum-journal.org/papers/q-2021-04-08-427/),
use QLSAs for Newton systems but output classical directions.

A targeted primary-source search found no prior work that transfers the
near-linear Grønlund--Larsen SQ lower bound to a one-cone SOCP or realizes its
hard inverse state as an exact public-start Lorentz-barrier Newton direction.
That exact access-preserving wrapper is the defensible apparent novelty;
priority is not guaranteed by a negative search.

The companion
[sparse-SQ conditioning frontier](2026-09-04-sparse-sq-conditioning-frontier.md)
shows that the logarithmic condition growth here is necessary for any
dimension-polynomial sparse/SQ sampling separation.  Squaring the hard
linear system gives a five-sparse SPD version at the tight
\(\Theta(\log^2N)\) SPD threshold.
