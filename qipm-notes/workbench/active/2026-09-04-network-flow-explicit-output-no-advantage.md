# Sparse network-flow QIPMs: an explicit-output no-advantage theorem

Status: Supporting synthesis; independently audited; core diamond idea
collides with a preliminary local lead  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the constructions and model separation; not a new
standalone theorem relative to the local archive

## Result and boundary

Sparse network-flow LPs support a rigorous no-quantum-advantage statement,
but only after the output contract is fixed.  There are two complementary
results.

1. A planar, bounded-degree, treewidth-two minimum-cost-flow family requires
   \(\Omega(m)\) bounded-error quantum queries to return an explicit feasible
   near-optimal edge-flow.  The same lower bound holds with canonical full
   sample-and-query access, and a classical algorithm matches it in
   \(\Theta(m)\) time.  Its first box-barrier Newton matrix in the public
   orthonormal cycle/tangent basis is condition one, yet returning the full
   classical Newton direction still takes \(\Omega(m)\) quantum queries.
2. On every incidence LP, each primal--dual normal equation is a weighted
   graph Laplacian.  A classical nearly-linear Laplacian solve gives exactly
   the natural scaled Newton-error certificate, without a condition-number
   conversion.  Therefore any \(T\)-round hybrid QIPM which explicitly
   materializes all \(m\) edge variables every round has classical work
   \(\widetilde O(mT)\) and an \(\Omega(mT)\) word-write floor.

Neither result rules out a quantum advantage for an objective value, one
coordinate, a sample, a quantum state, or an edge-queryable implicit flow.
Nor does the second result prove \(\Omega(mT)\) independent input queries:
the same hidden data may be reused at all iterations.

## Access and output model

An instance has a public directed graph, incidence matrix, demands, and
capacities.  Edge costs are accessed through any combination of the
following canonical oracles:

- an entry oracle \(|e,b\rangle\mapsto|e,b\oplus c_e\rangle\);
- the public norm \(\|c\|_2\);
- an independent sample \(e\) with probability \(c_e^2/\|c\|_2^2\); and
- a canonical coherent preparation of
  \(\|c\|_2^{-1}\sum_e c_e|e\rangle\).

This is called full SQ access below.  An arbitrary unitary completion is not
allowed to hide extra input information off the specified preparation
subspace.

The **explicit-flow contract** requires a self-contained classical array (or
a sparse list) from which every edge-flow can be read without further access
to the input oracle.  Oracle calls, ordinary word operations, and output
writes are all charged.  A persistent wrapper which answers an edge query by
calling the original input oracle is an implicit output and does not satisfy
this contract.

## A bounded-degree full-flow query lower bound

### The series-diamond family

For \(M\geq1\), form a directed chain of \(M\) diamonds.  Gadget \(j\) has
the four arcs

\[
 v_{j-1}\longrightarrow u_{j,a}\longrightarrow v_j,
 \qquad a\in\{0,1\}.
 \tag{1}
\]

All arcs have capacity one, and one unit must flow from \(v_0\) to \(v_M\).
For a hidden string \(z\in\{0,1\}^M\), only the first arc of each branch may
have nonzero cost:

\[
 c_{j,a}=a\mathbin\oplus z_j.
 \tag{2}
\]

The second arc of every branch has cost zero.  The graph is a planar DAG,
has \(m=4M\) arcs, maximum undirected degree four, and treewidth at most two.
All data are integral and in \(\{0,1\}\), and the all-one-half flow is a
public strictly feasible point.

Every feasible flow is described by branch masses
\(x_{j,0}+x_{j,1}=1\), independently in each gadget.  Hence

\[
 c_z^Tx=\sum_{j=1}^M x_{j,1-z_j}.
 \tag{3}
\]

The unique optimum uses branch \(z_j\) in every gadget.  Its value is zero
and its support contains exactly \(2M\) arcs.

### Theorem 1 (explicit near-optimal flow)

Fix \(0<\delta<1/8\).  Every bounded-error quantum algorithm which, on the
series-diamond family, returns a classical feasible flow satisfying

\[
 c_z^T x\leq\delta M                                      \tag{4}
\]

uses \(\Omega(M)=\Omega(m)\) cost-oracle queries.  This remains true under
the full SQ access above.  A classical algorithm matches the bound in
\(\Theta(m)\) time.

Exact feasibility is part of the main output contract.  A limited
\(\ell_1\)-conservation extension is given after the proof; no extension to
an arbitrary Euclidean or energy-norm residual is claimed.

#### Proof

Decode \(\widehat z_j\) as a branch carrying at least one half unit in
gadget \(j\), breaking ties by a public rule.  If
\(\widehat z_j\neq z_j\), the wrong branch contributes at least one half to
(3).  Thus every output satisfying (4) obeys

\[
 d_H(\widehat z,z)\leq2\delta M.                           \tag{5}
\]

For completeness, choose by the Gilbert--Varshamov bound a code
\({\cal C}\subseteq\{0,1\}^M\) of size \(2^{\Omega(M)}\) and minimum
distance greater than \(4\delta M\).  The Hamming balls allowed by (5) are
disjoint on this code.  After \(Q\) standard quantum bit queries, the final
state family has an expansion

\[
 |\psi_z\rangle
 =\sum_{S\subseteq[M],\ |S|\leq Q}(-1)^{\sum_{j\in S}z_j}|v_S\rangle,
 \tag{6}
\]

so its span has dimension at most

\[
 D_Q=\sum_{k=0}^Q{M\choose k}.                             \tag{7}
\]

Successful approximate recovery identifies the codeword with constant
probability.  Fano's inequality and the Holevo dimension bound give
\(\log D_Q=\Omega(M)\).  The binomial entropy bound then forces
\(Q=\Omega(M)\).  Bit and phase queries are equivalent up to a constant.

It remains to check the stronger access model.  The cost vector has exactly
one unit entry per gadget, so its norm and support size are public.  An entry
query uses one query to \(z_j\).  A squared-coordinate sample is generated
by choosing public uniform \(j\) and querying whether the supported branch
is \(1-z_j\).  Likewise, a uniform superposition over \(j\), one coherent
query to \(z_j\), and public index arithmetic prepare the canonical cost
state.  Thus each allowed SQ call is simulated by \(O(1)\) bit queries, and
the lower bound transfers.

Finally, querying every bit and writing the two used arcs in every gadget
constructs the exact optimum in \(\Theta(M)\) work.  Its support is
\(2M\), so both a dense array and a sparse nonzero list take \(\Omega(M)\)
words. \(\square\)

The same argument is representation-independent under a source-erasing
contract.  Suppose a quantum preprocessor outputs a self-contained classical
string \(R_z\) from which an oracle-free decoder produces a feasible flow
satisfying (4) with constant probability.  Composing the two procedures
gives Theorem 1, so preprocessing needs \(\Omega(M)\) queries.  On the code
promise used in the proof, Fano's inequality also gives
\(I(z;R_z)=\Omega(M)\), and hence \(|R_z|=\Omega(M)\) bits.  This does not
apply when the decoder retains the original cost oracle.

The approximation scale in (4) is a constant average cost per gadget.  In
particular, the theorem contains exact optimization as a special case.  It
does not claim a multiplicative approximation to the zero optimum.

There is a robust but norm-specific extension.  Let \(r=Bf-b\) be the
demand residual of a nonnegative edge vector, with the source--sink demand
normalized to one.  If \(\|r\|_1\leq\rho<1\), summing conservation residuals
over the prefix cut before gadget \(j\) shows that the total flow \(F_j\) on
its two first arcs obeys \(|F_j-1|\leq\rho\).  Decode the larger of those two
flows.  A wrong decision puts at least \((1-\rho)/2\) on the costly arc, so

\[
 d_H(\widehat z,z)\leq {2c_z^Tf\over1-\rho}.
\]

Theorem 1 therefore also holds when \(c_z^Tf\leq\delta M\) and
\(\|Bf-b\|_1\leq\rho\), provided \(\delta<(1-\rho)/8\).  A relative
Euclidean or \(L^\dagger\)-norm Newton residual does not by itself imply this
dimension-independent \(\ell_1\) condition.

The family is two-terminal series-parallel, for which Booth and Tarjan
already give an \(O(m\log m)\)-time specialized classical minimum-cost
maximum-flow algorithm
[[Booth--Tarjan 1993](https://doi.org/10.1006/jagm.1993.1048)].

## A condition-one Newton-direction lower bound

At the public feasible point \(x^0_e=1/2\), use the box barrier

\[
 \Phi(x)=-\sum_e\bigl(\log x_e+\log(1-x_e)\bigr).
 \tag{8}
\]

Then \(\nabla\Phi(x^0)=0\) and \(\nabla^2\Phi(x^0)=8I\).  On gadget \(j\),
let

\[
 w_j=(1,1,-1,-1)^T,\qquad q_j=w_j/2,                      \tag{9}
\]

where the positive coordinates are branch zero.  The disjoint vectors
\(q_j\) are an orthonormal basis of the feasible tangent space.  For
objective multiplier \(\tau>0\), the constrained Newton direction is

\[
 \Delta_z=-{\tau\over32}\sum_{j=1}^M(2z_j-1)w_j.          \tag{10}
\]

Indeed, the reduced Hessian is \(Q^T(8I)Q=8I_M\), while
\(q_j^Tc_z=(2z_j-1)/2\).  Its Newton decrement satisfies

\[
 \|\Delta_z\|_{\nabla^2\Phi(x^0)}^2={\tau^2M\over32}.     \tag{11}
\]

Taking \(\tau=M^{-1/2}\) makes the decrement a fixed small constant.

### Theorem 2 (classical direction readout)

For every sufficiently small fixed \(\epsilon>0\), returning a classical
tangent direction \(\widehat\Delta\) with

\[
 \|\widehat\Delta-\Delta_z\|_2
 \leq\epsilon\|\Delta_z\|_2                              \tag{12}
\]

requires \(\Omega(m)\) bounded-error quantum cost queries, even though the
reduced Newton matrix is public and has condition number one.  The same is
true if (12) is replaced by the corresponding relative residual guarantee
in reduced coordinates.

#### Proof

In reduced coordinate \(j\), the true value has magnitude \(\tau/16\)
and sign determined by \(z_j\).  Every incorrectly rounded sign contributes
at least \((\tau/16)^2\) to squared error, whereas the true reduced vector
has squared norm \(M(\tau/16)^2\).  Thus sign rounding makes at most
\(\epsilon^2M\) errors.  The approximate-interrogation proof of Theorem 1
applies.  Because the reduced matrix is \(8I\), relative residual and
relative solution error are identical. \(\square\)

One coherent query nevertheless prepares the normalized state proportional
to (10).  As a ray, this state also loses the global sign distinguishing
\(z\) from its complement; a public anchor gadget can fix that phase if
desired.  This family isolates classical readout, not condition number or
quantum state preparation.

Condition one refers only to the cycle/tangent reduction.  The grounded
vertex-potential normal matrix is ((1/8)BB^T) at this point and has
condition number (Theta(M^2)) on the diamond chain.  The public cycle
basis removes that graph-conditioning artifact exactly; no condition-one
claim is made for the multiplier Laplacian or the full KKT matrix.

## Laplacian normal equations match the classical Newton norm

Let \(B\in\mathbb R^{(n-1)\times m}\) be a reduced incidence matrix of a
connected graph.  For the standard-form incidence LP

\[
 \min c^Tx\quad\text{subject to}\quad Bx=b,\quad x\geq0,
 \tag{13}
\]

write the primal--dual Newton residual equations as

\[
 B\Delta x=r_p,\qquad
 B^T\Delta y+\Delta s=r_d,\qquad
 S\Delta x+X\Delta s=r_c.                                 \tag{14}
\]

With \(D=XS^{-1}>0\), elimination gives

\[
 L\Delta y=h,\qquad L=BDB^T,                              \tag{15}
\]

where

\[
 h=r_p-BS^{-1}(r_c-Xr_d),                                 \tag{16}
\]

followed by

\[
 \Delta s=r_d-B^T\Delta y,qquad
 \Delta x=S^{-1}(r_c-Xr_d)+DB^T\Delta y.                 \tag{17}
\]

The grounded matrix \(L\) is an SPD weighted graph Laplacian.  If
\(e=\widehat y-\Delta y\), recovery from \(\widehat y\) gives

\[
 \delta s=-B^Te,qquad \delta x=DB^Te,                    \tag{18}
\]

and therefore the exact identities

\[
 \|D^{-1/2}\delta x\|_2=\|e\|_L,
 \qquad
 \|L\widehat y-h\|_{L^{-1}}=\|e\|_L.                    \tag{19}
\]

Thus an energy-norm Laplacian solve directly supplies the scaled primal
Newton error and dual-residual certificate; no \(\sqrt\kappa(L)\) loss is
needed.  The same conclusion follows for a primal log-barrier formulation,
where the inverse diagonal barrier Hessian supplies the edge weights.

Spielman and Teng give a randomized solver producing relative energy-norm
error \(\eta\) in
\(\widetilde O(m\log(1/\eta))\) expected time
[[Spielman--Teng 2014](https://epubs.siam.org/doi/10.1137/090771430)].
This is a real-arithmetic statement; bit complexity also depends
polylogarithmically on input precision and the weight range.

For comparison, Apers and de Wolf give a quantum algorithm which outputs an
explicit classical Laplacian solution with relative energy-norm error
\(\eta\) in \(\widetilde O(\sqrt{mn}/\eta)\) time under their
adjacency-list/QRAM model
[[Apers--de Wolf 2022](https://arxiv.org/abs/1911.07306)].  On bounded-degree
graphs, \(m=\Theta(n)\), this is already
\(\widetilde O(m/\eta)\), so at constant forcing tolerance it offers no
polynomial dimension gain over classical nearly-linear solution.  On dense
graphs the single-solve bound can be sublinear in \(m\); an explicit
edge-variable IPM still separately pays for whatever \(m\)-coordinate
recovery and update its contract requires.

### Theorem 3 (matched explicit-iterate trajectory)

Consider a common \(T\)-round incidence-LP path-following schedule whose
outer proof accepts

\[
 \|L_t\widehat y_t-h_t\|_{L_t^{-1}}
 \leq\eta_t\|h_t\|_{L_t^{-1}}.                            \tag{20}
\]

Assume the current edge weights and residuals can be evaluated classically
from an explicit iterate with the same precision charged to their quantum
oracles.  Then a classical implementation has work

\[
 \widetilde O\left(
   \sum_{t=1}^T m\log(1/\eta_t)
 \right),                                                  \tag{21}
\]

including \(O(m)\) recovery and update per round.  Any hybrid quantum
implementation of the same schedule which materializes all \(m\) primal or
slack coordinates before each next round uses \(\Omega(mT)\) sequential
word operations.  At constant forcing tolerances, the classical upper and
hybrid output floor match up to polylogarithmic factors.

This is a conditional replacement theorem for a specified robust schedule,
not a claim that a nearly-linear Laplacian solve by itself preserves exact
feasibility or proves IPM convergence.  In (20), a nonzero residual is an
equality-constraint residual; a feasible-IPM application needs precisely the
assumed inexact-path-following theorem or a separately proved repair.  It is
not an
iteration lower bound against every quantum optimization algorithm.  It
also proves only an \(mT\) word-write floor.  Theorem 2 supplies a direct
\(\Omega(m)\) input-query lower bound for one genuine Newton direction, but
the same hidden \(M\) bits can be learned once and reused; multiplying that
query lower bound by \(T\) would be invalid.

## Centrality does not control normal-equation condition

The classical conclusion above does not need a polynomial dependence on
\(\kappa(L)\).  In contrast, sparse exact centrality alone does not justify
dismissing that dependence from a direct QLSA ledger.

Use vertices \(\{g,1,2\}\), ground \(g\), and arcs
\(g\to1,1\to2,2\to1\), with

\[
 B=\begin{bmatrix}1&-1&1\\0&1&-1\end{bmatrix},\quad
 b=(1,0)^T,\quad c=(0,1,1)^T.                              \tag{22}
\]

For every \(\mu>0\), the fixed LP has the exact central point

\[
 x=(1,\mu,\mu),\quad y=(-\mu,-\mu),\quad s=(\mu,1,1),     \tag{23}
\]

so \(D=XS^{-1}=\operatorname{diag}(\mu^{-1},\mu,\mu)\) and

\[
 L=\begin{bmatrix}
 \mu^{-1}+2\mu&-2\mu\\-2\mu&2\mu
 \end{bmatrix}.                                           \tag{24}
\]

Here \(\det L=2\) and \(\operatorname{tr}L=\mu^{-1}+4\mu\), hence
\(\kappa_2(L)=\Theta(\mu^{-2})\) for \(0<\mu\leq1/2\).
Taking \(k\) copies joined only at \(g\) gives \(m=3k=\Theta(n)\), a
block-diagonal grounded Laplacian of constant row sparsity, and duality gap
\(3k\mu\).  At target gap \(\varepsilon\), its condition number is

\[
 \kappa_2(L)=\Theta\bigl((m/\varepsilon)^2\bigr).          \tag{25}
\]

This is a warning about an unpreconditioned normal-matrix QLSA bound, not a
quantum lower bound: the displayed \(2\)-by-\(2\) blocks admit an obvious
preconditioner, and an augmented formulation can avoid squaring the scaled
incidence condition.

## Why there is no output-independent no-advantage theorem

The series-diamond family sharply separates contracts.

| Requested output | Cost on this family |
|---|---|
| Dense edge-flow array | \(\Omega(m)\) queries and writes |
| Sparse nonzero list | \(\Omega(m)\); the optimum has \(2M\) nonzeros |
| Full classical first Newton direction | \(\Omega(m)\) queries |
| Objective value only | zero queries; the optimum value is public zero |
| One squared-coordinate flow sample | one hidden-bit query |
| Amplitude-encoded optimum or Newton direction | one coherent query |
| Input-retaining edge-coordinate wrapper | constant description size |

The last line is not merely formal.  Recent flow algorithms explicitly use
edge-queryable data structures or emit each coordinate when the edge is
seen in the last stream pass, thereby avoiding the requirement that one
self-contained object store every coordinate
[[van den Brand--Song--Weng 2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2026.46)].
Any quantum/classical comparison must give both sides the same output and
input-retention contract.

There can also be a genuine quantum query advantage for scalar flow values.
With \(m\) parallel unit-capacity arcs and costs \(c_i\in\{-1,+1\}\), the
unit-flow optimum is \(\min_i c_i\).  Distinguishing all-plus-one costs from
one minus-one cost takes \(\Theta(m)\) randomized queries and
\(\Theta(\sqrt m)\) quantum queries by unstructured search.  This separation
survives full SQ access: the norm and squared-coordinate sampling
distribution are identical under the promise, while the entry oracle gives
Grover search.  Therefore
Laplacian normal-equation structure and full-flow readout cannot support a
blanket no-quantum-advantage theorem for value-only algorithms.

## End-to-end comparison with specialized classical flow algorithms

Chen, Kyng, Liu, Peng, Probst Gutenberg, and Sachdeva compute exact maximum
flows and minimum-cost flows with polynomially bounded integral data in
\(m^{1+o(1)}\) time
[[Chen et al. 2022](https://arxiv.org/abs/2203.00671)].  Combining that
all-instance upper bound with Theorem 1 gives the following precise
worst-case conclusion:

> Under the explicit classical full-flow contract, no bounded-error quantum
> algorithm for exact directed minimum-cost flow can improve the polynomial
> exponent in \(m\) over the best known classical algorithm.  The quantum
> worst-case cost is \(\Omega(m)\), while the classical cost is
> \(m^{1+o(1)}\) for polynomially bounded integral data.

This conclusion is stronger than a comparison of one classical and one
quantum linear solver, but narrower in output and data type.  It does not
cover real-valued general convex flows, objective-only output, implicit
flows, or possible improvements inside the remaining \(m^{o(1)}\) factor.
A deterministic \(m^{1+o(1)}\) exact algorithm is also known
[[van den Brand et al. 2023](https://arxiv.org/abs/2309.16629)], so the
conclusion is not an artifact of randomization in the classical upper bound.

## Novelty and collision assessment

The nearly-linear classical algorithms, energy-norm Laplacian solvers,
oracle-interrogation method, and output-representation distinction are
known.  More importantly, the local
[Hamiltonian QIPM research log](../../research-archive/2026-09-research-cycle/research-logs/2026-09-02-hamiltonian-qipm-research.md)
already records the central idea of a planar diamond chain with a
condition-one cycle Newton system, one-query state preparation, and a
linear explicit-output query lower bound.  Theorems 1--2 supply a complete
proof, exact constants, and canonical full-SQ accounting for that preliminary
lead; they must not be presented as a fresh discovery relative to this
repository.

The useful additions are the exact energy-norm recovery identities (19),
the matched explicit-trajectory statement, the fixed-LP central-path
condition witness, and the clean corollary comparing the \(\Omega(m)\)
explicit-output floor with the \(m^{1+o(1)}\) exact classical flow upper.
These are best framed as a rigorous boundary and synthesis, not as a new
standalone lower-bound technique.  The external screen found no paper that
states the exact combined theorem, but priority remains subject to broader
expert review.
