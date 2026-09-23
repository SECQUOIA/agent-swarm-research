# Quantum barrier compilation for a sparse tree SOCP

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate-to-high on novelty of the conjunction  
Question: Can quantum preprocessing remove both scenario-count barrier growth
and recursive-output overhead on an explicit sparse conic family?

## Sparse SOCP family

Let \(r_i=2-b_i\), where \(b\in\{0,1\}^N\) has Hamming weight zero or one.
For fixed \(d\), consider

\[
 \begin{aligned}
 \max\quad &e_1^Tz_1\\
 \text{s.t.}\quad &(t_i,z_i)\in\mathcal Q_{d+1},\\
 &t_i=r_i,\qquad z_i=z_{i+1}\quad(i<N).
 \end{aligned}
\]

The constraint matrix is public and has entries in \(\{0,\pm1\}\); only the
bounded RHS values \(r_i\) are queried. The block factor graph is a path,
scalar incidence is constant, and the numerical primal-barrier KKT graph is a
forest along the central path. Slater holds: \((t_i,z_i)=(r_i,0)\) is strictly
primal feasible, and setting the fixed-\(t_i\) dual multipliers to two and the
consensus multipliers to zero gives cone slacks \((2,-e_1)\) at the root and
\((2,0)\) elsewhere.

Consensus makes every \(z_i=z\), so the exact projection is

\[
 \|z\|_2\leq r_*:=\min_i r_i,
 \qquad \operatorname{OPT}=r_*.
\]

## Compiled QIPM and tight query complexity

Quantum minimum finding computes \(r_*\) using \(\Theta(\sqrt N)\) coherent
RHS queries. It thereby certifies the exact projected barrier

\[
 \phi_{r_*}(z)=-\log(r_*^2-\|z\|_2^2),
\]

whose self-concordant parameter is at most two (indeed one under the sharp ball
normalization). Short-step path following then uses

\[
 O(\log(1/\epsilon))
\]

Newton steps, each costing \(\operatorname{poly}(d)\), with no more input
queries. The output is an explicit \(d\)-vector plus the public implicit lift
\(z_i=z\). A classical coordinate oracle answers any original coordinate in
constant time. Coherently, the lift is the public isometry

\[
 |z\rangle\mapsto |u_N\rangle|z\rangle,
\]

which costs polylogarithmically many gates for standard uniform-state
preparation and uses no input-dependent reconstruction.

The query bound is optimal. Additive error below \(1/3\) distinguishes
\(r_*=2\) from \(r_*=1\), i.e. zero versus one marked bit. Hence

\[
 Q=\Theta(\sqrt N),\qquad R=\Theta(N).
\]

A classical structure-aware solver matches the randomized bound by scanning
the radii, compiling the same ball, and solving the fixed-dimensional problem.

## A genuine barrier-path separation

Ordinary equality elimination leaves the replicated product barrier

\[
 \Phi(z)=-\sum_{i=1}^N\log(r_i^2-\|z\|_2^2).
\]

On the all-\(r_i=2\) branch, \(\Phi=N\phi_2\), so its parameter is
\(\Theta(N)\). Along the radial exact central path \(z=\alpha e_1\),

\[
 \phi_2''(\alpha)=\frac{2(4+\alpha^2)}{(4-\alpha^2)^2}.
\]

The \(N\phi_2\)-metric length from \(\alpha=1\) to
\(\alpha=2-\epsilon\) is

\[
 \Omega(\sqrt N\log(1/\epsilon)).
\]

If consecutive exact centers have Dikin distance at most a fixed
\(\rho<1\), self-concordance bounds the integrated length of one move by
\(-\log(1-\rho)\). Every such local exact-central schedule therefore needs

\[
 \Omega_\rho(\sqrt N\log(1/\epsilon))
\]

moves. The compiled one-ball barrier removes the \(\sqrt N\) factor.

Blind division by \(N\) is not a uniform fix. On the one-mark branch,
\(N^{-1}[\phi_1+(N-1)\phi_2]\) approaches the \(r=1\) boundary with the
singular term dominating; the standard third-derivative self-concordance ratio
is multiplied by \(\sqrt N\). The minimum certificate is what licenses
replacement of the whole sum by the exact-domain barrier.

## Treewidth, conditioning, and barrier parameter separate

At the analytic center, one coordinate of the lifted consensus KKT system is

\[
 K=\begin{bmatrix}D&A^T\\A&0\end{bmatrix},
\]

where \(A\) is path incidence and \(D\) has diagonal entries in
\([1/2,2]\). Consequently,

\[
 \kappa(AD^{-1}A^T)=\Theta(N^2),\qquad
 \kappa(K)=\Theta(N^2),
\]

despite forest support, bounded coefficients, and strict feasibility. Public
consensus elimination removes this artificial lifted-system condition factor;
quantum active-cone compilation then removes the independent \(N\)-fold
barrier multiplicity. No claim is made that a QLSA must pay \(N^2\), because
the public elimination is an explicit preconditioner.

## Homothetic-cone generalization

Let \(C\subset\mathbb R^d\) be a public compact convex body containing zero
and having a \(\nu\)-self-concordant barrier \(f\). Put copies \(x_i\) on a
bounded-degree public tree, impose consensus, and require \(x_i\in r_iC\).
Nestedness gives

\[
 \bigcap_i r_iC=r_*C,qquad r_*=\min_i r_i.
\]

Quantum minimum finding compiles a \(\nu\)-barrier for the exact projection in
\(\Theta(\sqrt N)\) key queries, instead of following the natural
\(N\nu\)-scale product barrier. Any constant-size conic representation of
\(C\) preserves bounded incidence and constant block treewidth.

## Width-\(k\) chain-cover / Pareto compiler

The one-chain theorem extends sharply. Suppose \(N\) local conic constraints
are partitioned into \(k\) supplied chains under reverse inclusion. Chain
\(j\) contains \(n_j\) constraints with an ordered key, and its retained
constraint has a \(\nu_j\)-barrier once the extremal key is known. Constraints
from different chains may be incomparable. Then

\[
 \bigcap_{j,\ell}C_{j,\ell}
 =\bigcap_{j=1}^k C_{j,*}.
\]

Quantum minimum finding in each chain uses

\[
 \widetilde O\!\left(\sum_j\sqrt{n_j}\right)
 \leq\widetilde O(\sqrt{Nk})
\]

queries. The compiled barrier has parameter
\(\nu_0+\sum_j\nu_j\), with no remaining dependence on \(N\), and the
postproblem can remain a genuinely coupled \(k\)-dimensional conic program.

The exponent is tight. Take \(n_j=m=N/k\) Lorentz interval constraints
\(|z_j|<2-b_{j,\ell}\), with each chain containing zero or one marked bit.
Returning the optimizer of \(\max\sum_jz_j\) to \(\ell_\infty\) error below
\(1/3\) returns all \(k\) OR values. The direct-sum adversary formed from \(k\)
star matrices has norm \(k\sqrt m=\sqrt{Nk}\), while each coordinate query
filters it to norm one. Hence

\[
 Q=\Theta(\sqrt{Nk}),\qquad R=\Theta(N).
\]

The quantum/classical ratio \(\sqrt{N/k}\) vanishes exactly when the poset
width reaches \(N\).

On the all-radius-two input, the natural replicated barrier is

\[
 \Phi_N(z)=m\sum_{j=1}^k\phi_2(z_j)
\]

with parameter \(N\) and radial central-path length
\(\Omega(\sqrt N\log(1/\epsilon))\). The compiled \(k\)-box barrier has
parameter \(k\), path length \(\Theta(\sqrt k\log(1/\epsilon))\), and the
standard matching short-step upper bound. Thus the path compression factor
\(\sqrt{N/k}\) equals the query-advantage factor. Dividing the original
barrier by \(m\) is not uniformly self-concordant when a chain has one tighter
constraint; the extremal-key certificate is essential.

A sparse lift uses \(k\) consensus paths coupled only at their roots, has
\(\Theta(N)\) size, constant local incidence, and block treewidth \(O(k)\).
After compilation, all original coordinates have a public chain-copy
reconstruction. Adding a public ellipsoid
\(z^THz<R^2\) and a generic objective produces a genuinely coupled dense
\(k\)-dimensional postsolve without changing preprocessing.

For explicit bounded-fan-in input, the \(k\) readable outputs require
\(\Omega(N)\) gates and depth \(\Omega(\log_g(N/k))\); parallel classical
reductions match both. The poset-width theorem therefore preserves the same
honest oracle-versus-loading boundary as the one-chain case.

## Explicit-input closure

The advantage is oracle-dependent. If the \(N\) bits are explicit input wires
and gates have fan-in at most \(g\), a constant-size readable output that is
sensitive to every unique-search bit requires \(\Omega(N)\) gates in its
backward light cone and depth \(\Omega(\log_gN)\). A classical balanced
minimum tree matches these bounds. Requiring a materialized \(Nd\)-vector also
costs \(\Omega(Nd)\). Thus the theorem gives a tight query advantage with a
supplied coherent radius oracle, not a gate-work or parallel-depth advantage
after loading explicit input.

## Novelty boundary

Classical build-up barriers, redundant-constraint removal, quantum violated-
constraint search, minimum finding, and small-treewidth solvers are prior art.
A targeted search found no source combining the exact homothetic/tree
compilation, an \(N\)-to-one barrier and path-length reduction, forest-KKT
conditioning separation, tight quantum/randomized bounds, public coherent
reconstruction, and the explicit-loading closure. That conjunction is the
defensible apparent novelty. The family becomes elementary after \(r_*\) is
known; this limitation should be stated prominently.
