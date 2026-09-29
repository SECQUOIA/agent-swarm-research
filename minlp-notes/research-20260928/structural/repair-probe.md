# Exact transfer of deterministic repair bounds to local probability laws

Date: 2026-09-28. Status: supporting theorem and sharp limitations, independently
checked in an adversarial proof review. This is a synthesis of classical tree
gluing, transport, and deterministic error bounds. No substantial novelty claim
is made. The exact equality of the best constants is the useful formulation.

The theorem handles hard local constraints and integer coordinates without a
separate rounding argument. Its substantive premise is a deterministic bound
for repairing inconsistent local records. Probability measures neither improve
nor worsen the best universal Hölder constant on a tree. Computing a useful
deterministic bound and an efficient repair remains a separate problem.

## 1. Setting

Let \(T=(V,E)\) be a finite tree. For each vertex \(v\), let \(K_v\) be a
nonempty compact metric space with metric \(d_v\). For each edge \(e=vw\),
let \((S_e,d_e)\) be a metric space and let
\(p_{ve}:K_v\to S_e\), \(p_{we}:K_w\to S_e\) be continuous maps. The
union of their images is compact, so every Wasserstein distance below is finite
and attained.

For a tree decomposition, \(K_v\) is the feasible set for bag \(v\), and
the maps project onto its separator with the adjacent bag. Bounded integer
coordinates are allowed, with their usual metric or a chosen discrete metric.
The running-intersection property makes agreement on these edges equivalent
to a single assignment of all original coordinates. In the abstract statement,
edge agreement itself defines feasibility; no coordinate interpretation is
needed.

Set
\[
 K=\prod_{v\in V}K_v,\qquad
 D(z,y)=\sum_vd_v(z_v,y_v),\qquad
 r(z)=\sum_{e=vw}d_e(p_{ve}z_v,p_{we}z_w),
\]
and assume that the compact set
\[
 F=\{z\in K:r(z)=0\}
\]
is nonempty. It includes every hard local constraint through the sets \(K_v\).
Write \(h(z)=\operatorname{dist}_D(z,F)\).

For arbitrary actual probability measures \(\mu_v\in\mathcal P(K_v)\),
define the separator residual and the optimal repair distance by
\[
 R(\mu)=\sum_{e=vw}W_{1,d_e}((p_{ve})_\#\mu_v,(p_{we})_\#\mu_w),
 \tag{1}
\]
\[
 H(\mu)=\min_{\nu\in\mathcal P(F)}
       \sum_vW_{1,d_v}(\mu_v,(\operatorname{pr}_v)_\#\nu).
 \tag{2}
\]
The minimum in (2) exists: \(\mathcal P(F)\) is weakly compact and the
objective is continuous for weak convergence on compact metric spaces.
The repaired law need not preserve the original integer or action marginals.
It is supported on exactly feasible integer/continuous assignments.

## 2. Sharp lifting theorem

**Theorem 1.** Fix \(0<\alpha\le1\) and \(C\ge0\). The following are
equivalent, with exactly the same constant \(C\):
\[
 h(z)\le C r(z)^\alpha\quad\text{for all }z\in K; \tag{3}
\]
\[
 H(\mu)\le C R(\mu)^\alpha
 \quad\text{for all }(\mu_v)_{v\in V}. \tag{4}
\]
Consequently the infimal valid constants in (3) and (4) agree, including the
possibility that both are infinite.

**Proof of (3) implies (4).** For each edge choose an optimal coupling of its
two separator marginals. Disintegrate the two bag laws over their respective
separator maps. Integrating the product of these two conditional bag laws
against the chosen separator coupling produces a probability law
\(\gamma_e\) on \(K_v\times K_w\). Its bag marginals are
\(\mu_v,\mu_w\), and its expected edge discrepancy is that edge's term
in (1).

These pair laws have consistent bag marginals and can all be realized by one
joint law \(\pi\) on \(K\). To see this explicitly, root the tree, draw
the root bag with its law, and draw each child conditionally on its parent
using a disintegration of \(\gamma_e\) on the parent coordinate. Induction
gives every bag marginal and every edge pair marginal as specified. Different
children may be conditionally independent; uniqueness of this joint law is
neither required nor asserted. Thus
\[
 \pi\in\Pi((\mu_v)_v),\qquad \int r\,d\pi=R(\mu). \tag{5}
\]

For \(\varepsilon>0\), take a finite \(\varepsilon\)-net in \(F\) for
the metric \(D\). Map each \(z\) to the first nearest net point
\(P_\varepsilon(z)\). This is a Borel map and
\[
 D(z,P_\varepsilon(z))\le h(z)+\varepsilon.
\]
Use the law of \(P_\varepsilon(Z)\), for \(Z\sim\pi\), as a candidate
in (2). Each pair \((Z_v,(P_\varepsilon Z)_v)\) is a valid transport
coupling. Summing costs, using (3), and using concavity of \(t^\alpha\),
\[
 H(\mu)\le\int h\,d\pi+\varepsilon
 \le C\int r^\alpha\,d\pi+\varepsilon
 \le C R(\mu)^\alpha+\varepsilon.
\]
Let \(\varepsilon\downarrow0\). This finite-net argument avoids needing
an exact measurable nearest-point selection theorem.

**Proof of the converse.** For a fixed \(z\in K\), take
\(\mu_v=\delta_{z_v}\). Then \(R(\mu)=r(z)\), and transport from a
Dirac measure is unique, so
\[
 H(\mu)=\min_{\nu\in\mathcal P(F)}\int_FD(z,y)\,d\nu(y)
       =\min_{y\in F}D(z,y)=h(z).
\]
Equation (4) therefore implies (3). ∎

The same proof works with \(C t^\alpha\) replaced by any continuous
concave nonnegative function \(\omega\) with \(\omega(0)=0\). Fixed
positive weights on the bag distances and on the edge residuals are also
allowed, provided the same weights are used on both sides of the equivalence.

### Two exact transport identities

The proof can be separated into two identities. For any finite graph, retaining
the same compactness and nonempty \(F\),
\[
 H(\mu)=\min_{\pi\in\Pi((\mu_v)_v)}\int h(z)\,d\pi(z). \tag{6}
\]
For a tree,
\[
 R(\mu)=\min_{\pi\in\Pi((\mu_v)_v)}\int r(z)\,d\pi(z). \tag{7}
\]
All minima exist by compactness. For (6), projecting an arbitrary \(\pi\)
to a finite net of \(F\) proves the inequality \(H\le\min\int h\).
Conversely, fix a law \(\nu\) on \(F\) and optimal couplings between
each \(\mu_v\) and \(\nu_v\). Disintegrate those couplings on their
\(\nu_v\) coordinates. First draw \(Y\sim\nu\); then draw the
\(Z_v\) conditionally on \(Y_v\) using those kernels. The resulting
\(Z\) has bag marginals \(\mu_v\), and
\[
 \int h\,d\mathcal L(Z)\le\mathbb E D(Z,Y)
 =\sum_v W_1(\mu_v,\nu_v).
\]
Minimizing over \(\nu\) proves the other inequality. For (7), every joint
law has expected edge discrepancies at least the corresponding optimal
transport costs; (5) attains their sum. The special role of the tree is
precisely (7).

## 3. Why the assumptions matter

**Cycles.** The following equal/equal/unequal marginal example is classical;
it appears in the introduction of Vorob'ev's 1962 paper cited below. The
explicit distances here explain its consequence for the proposed quantitative
extension. Consider the three binary pair bags \(12,23,13\), each with
the full local set \(\{0,1\}^2\) and the Hamming metric. Match the two
copies of each variable around the triangle with the absolute-value metric.
For every deterministic tuple, its distance to consistency equals the number
of disagreeing variable copies, which is exactly \(r\). Hence (3) holds
with \(\alpha=C=1\).

Give bags \(12\) and \(23\) the uniform law on \(\{00,11\}\), and bag
\(13\) the uniform law on \(\{01,10\}\). All separator marginals are
uniform, so \(R=0\). No global law realizes all three pair laws: the first
two force all three variables equal almost surely, contradicting the third.
In fact \(H=1\). For a lower bound, any tuple in the product support has
at least one inconsistent variable copy and thus \(h\ge1\); use (6).
For attainment, use the global uniform law on \(000,111\): the first two
bag laws agree exactly, and changing one bit transports the third bag law
at cost one. Thus the tree hypothesis cannot simply be dropped, even for
unconstrained finite bag sets with a perfect deterministic error bound.

**Exponents greater than one.** Take one edge with \(K_1=K_2=\{0,1\}\)
and equality as consistency. Pointwise \(h=r\in\{0,1\}\), so (3) holds
with \(C=1\) for every \(\alpha>0\). For
\(\mu_1=\delta_0\) and
\(\mu_2=(1-\varepsilon)\delta_0+\varepsilon\delta_1\), however,
\(H=R=\varepsilon\). No finite constant in (4) works for \(\alpha>1\).
This proves that the exponent restriction is material, not just a proof
artifact.

**Original local fibers versus viable fibers.** A forward fiber map can be
Lipschitz on its own projection domain while repaired inputs leave a child's
projection domain. Hard terminal constraints cause exactly this problem.
Backward pruning to globally extendable local sets addresses the domain issue,
but changes the fibers and can be as difficult as the underlying feasibility
problem. Assuming those viable fibers are Lipschitz must not be treated as a
consequence of Lipschitz dynamics.

## 4. Contractive dynamics can have exponentially bad terminal repair

Fix a rational \(0<a<1/2\), put \(f(x)=a x^2\), and consider
\[
 x_{j+1}=f(x_j)\quad(0\le j<m),\qquad
 0\le x_j\le1,\qquad x_m=0,
 \qquad \min -x_0. \tag{8}
\]
The initial state is free. Every forward transition is \(2a\)-Lipschitz,
with \(2a<1\). The only feasible trajectory is zero, and the true optimum
is zero.

Let \(\mu_j\in\mathcal P([0,1])\), \(0\le j<m\), be arbitrary
transition input laws; the local transition law is supported on the exact graph
of \(f\). Set \(\mu_m=\delta_0\), define
\[
 r_j=W_1(f_\#\mu_j,\mu_{j+1}),\quad
 R=\sum_{j=0}^{m-1}r_j,\quad d=2^m,\quad A=a^{d-1}.
\]
Transport contraction and the triangle inequality give
\[
 A\int x^d\,d\mu_0
 =W_1((f^m)_\#\mu_0,\delta_0)
 \le\sum_{j=0}^{m-1}(2a)^{m-1-j}r_j\le R.
\]
Jensen's inequality then proves the root-cost repair bound
\[
 \int x\,d\mu_0\le a^{-1+2^{-m}}R^{2^{-m}}. \tag{9}
\]
Both its exponent and its displayed constant are sharp. Start the local
trajectory at \(t\in(0,1]\), use Dirac laws at its successive states,
and retain the separate terminal law \(\delta_0\). Only the terminal
separator is inconsistent, with
\[
 R=A t^d,\qquad \text{root-cost repair loss}=t.
\]
Equality holds in (9). For fixed \(a,m\), every proposed bound
\(C R^\beta\) with \(\beta>2^{-m}\) fails as \(t\downarrow0\).
This remains true with an arbitrarily small common forward contraction factor.

A fixed initial state can be added by fixing an irrelevant initial state to
zero and selecting a first-stage action \(u\in[0,1]\), with cost \(-u\)
and first output \(a u^2\). Follow this by \(m-1\) copies of \(f\) and
the same terminal constraint. The same formula holds with root decision \(u\).

This is an approximate-consistency obstruction, **not** a lower bound for
exact moment matching. In this example, exact matching of first separator
moments with the terminal zero forces the preceding nonnegative square to
have expectation zero. For actual local measures this propagates backward
using only first separator moments. No truncated-moment extraction claim
is made by that observation.
The repeated-squaring mechanism is classical; see the prior comparisons in
[`equality-frontier.md`](../../research-20260927/equality-frontier.md).
The distinct point here is that strong forward contraction does not control
hard-terminal feasible repair.

## 5. Consequences and limits for MINLP relaxations

If the local objectives \(c_v\) are \(L\)-Lipschitz for the bag metrics,
the theorem gives a law on exactly feasible global assignments satisfying
\[
 \mathbb E\sum_vc_v(Y_v)
 \le\sum_v\int c_v\,d\mu_v+LC R(\mu)^\alpha. \tag{10}
\]
Some deterministic feasible assignment attains a cost no greater than this
expectation. Different cost Lipschitz constants can be incorporated as bag
weights. The mathematical existence guarantee does not supply an efficient
method for sampling or projecting onto \(F\).

Standard deterministic error-bound theorems can therefore be used without a
separate probabilistic regularity assumption. For example, a known Hoffman
bound for the product local polyhedron intersected with consistency equalities
immediately gives \(\alpha=1\). The same is true for finite unions of
compact polyhedra with linear separator maps: use Hoffman on each product
piece that intersects \(F\); on each remaining compact piece, \(r\) has
a strictly positive minimum, and the bounded distance to nonempty \(F\)
gives a linear bound. Finitely many pieces give a common constant. This covers
bounded MILP bag sets, without giving a small constant or preserving the
original integer marginal distributions.

Compact semialgebraic sets, with semialgebraic separator maps and metrics
(including coordinate projections and the usual Euclidean or sum metrics),
admit some Hölder error bound because \(h\) and \(r\) are continuous
semialgebraic functions with the same zero set; the theorem transfers that
bound. No useful
dimension-independent exponent follows, as Section 4 demonstrates.

If separator feature matching separately implies \(R(\mu)\le\eta_k\),
then (10) gives an objective gap at most \(LC\eta_k^\alpha\). This is a
conditional quantitative extension of exact gluing to hard constraints.
It concerns actual locally feasible measures. Positive semidefinite truncated
moment sequences need not represent such measures, so this is not a finite
SOS extraction theorem. Exact local optimization, representation, and efficient
global repair remain separate requirements.

The companion [penalty and dual-message note](penalty-messages.md) gives an
exact Wasserstein-penalty formulation and identifies the deterministic
linear repair constant with the smallest universal Lipschitz bound on
dual separator potentials for 1-Lipschitz local costs.

## 6. Sources, novelty assessment, and verification

The proof uses classical ingredients. The following primary sources or local
audits were examined or identified on 2026-09-28; the
[companion source audit](source-audit.md) records the broader search and
the [targeted finite LP check](check_repair_transfer.py).

- Vorob'ev, *Consistent families of measures and their extensions* (1962),
  [open primary scan](https://www.panix.com/~jays/vorob.pdf): classical exact
  extension of consistent marginal families. This source was identified by
  the parent investigator; it is prior to any claim about tree gluing here.
- Haasler, Ringh, Chen, Karlsson, *Multimarginal Optimal Transport with a
  Tree-Structured Cost and the Schrödinger Bridge Problem* (2021),
  [open primary manuscript](https://arxiv.org/abs/2004.06909) and
  [published-paper copy](https://par.nsf.gov/servlets/purl/10282851): tree
  pairwise cost structure and transport decomposition are established.
  The abstract and the tree-cost setup in Section 3 were examined; a theorem-
  by-theorem exclusion of an equivalent sharp repair statement is unfinished.
- Fan, Haasler, Karlsson, Chen, *On the complexity of the optimal transport
  problem with graph-structured cost* (2022),
  [primary paper](https://proceedings.mlr.press/v151/fan22a/fan22a.pdf):
  established junction-tree transport algorithms and complexity bounds. The
  abstract was examined. No new transport algorithm is claimed here.
- Kollár, *An Effective Łojasiewicz Inequality for Real Polynomials* (1999),
  [primary manuscript](https://arxiv.org/abs/math/9904161), together with the
  closer local audit in
  [`equality-frontier.md`](../../research-20260927/equality-frontier.md):
  exponential power-chain error-bound exponents are classical. Section 4 is
  a terminal-feasibility interpretation with a sharp measure-level root-cost
  formula, not discovery of the underlying conditioning phenomenon.

Searches for combinations of marginal consistency, Wasserstein error bounds,
Hoffman bounds, and tree gluing did not identify an explicit statement of
Theorem 1 with equality of optimal constants. This unsuccessful search does
not establish novelty. The theorem is short enough, and its ingredients
standard enough, that it should currently be treated as a supporting lemma
rather than a substantial independent theoretical advance.

An independent reviewer checked the contraction obstruction, proved (9) for
arbitrary measures, and checked the lifting theorem and its Dirac converse.
The reviewer also supplied the finite-net proof that avoids exact measurable
projection machinery. This is proof review, not formal verification. No Lean
proof was attempted. Targeted finite transport computations and source review
are maintained by the parent structural investigation; this note does not
claim any project-wide check or CI result.
