# Bounded-treewidth full-output QIPMs: a trajectory replacement theorem

Status: Supporting synthesis; independently audited; mostly collides locally  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High under the stated numerical and output assumptions  
Question: When does bounded treewidth rule out a total-work advantage from
replacing classical Newton solves by a QLSA?

## Scope and relation to existing local results

The archived
[sparse-QIPM structural note](../../research-archive/2026-09-research-cycle/supporting-results/sparse-qipm-structural-results.md)
already proves the one-system ceiling

\[
 O(D\tau^2)\quad\hbox{classical factorization}
 \qquad\hbox{versus}\qquad
 \Omega(D)\quad\hbox{dense output}.
\]

The result below does not claim that ceiling as new.  It strengthens and
qualifies it in three ways:

1. it gives a replacement theorem for an entire adaptive IPM trajectory;
2. it separates reusable symbolic structure from generally nonreusable
   numerical factors and changing quantum value oracles; and
3. it gives a direct \(\Omega(D)\) quantum query lower bound for a genuine
   condition-one, treewidth-zero Newton direction under constant relative
   \(\ell_2\) error, without relying only on a word-output count or a
   tomography convention.

This is a theorem about hybrid QIPMs that materialize classical directions or
iterates.  It is not an impossibility theorem for quantum-state output,
observable estimation, or a fully coherent nonlinear path-following method.

## Model

At outer iteration \(t\), let the algorithm solve \(q_t\) systems

\[
 K_t d_{t,j}=r_{t,j},\qquad j=1,\ldots,q_t,
\]

where \(K_t\in\mathbb R^{D_t\times D_t}\).  Assume:

- **Uniform numerical graph.** Along every legal trajectory accepted by the
  robust outer theorem, the graph of the actual scalar matrix \(K_t\), not
  merely the aggregate graph of the original conic data, is contained in a
  fixed enumerable supergraph with one supplied chordal completion and
  elimination order of width at most \(\tau\).
- **Eligible factorization.** Either \(K_t\) is SPD, or it is a regularized
  symmetric quasi-definite matrix for which the supplied symmetric order has
  a numerically stable pivot-free \(LDL^T\) factorization.  For a general
  indefinite KKT matrix this assumption must not be inferred from treewidth.
- **Matched entry access.** Given the current explicit iterate, every current
  matrix and right-hand-side entry is classically evaluable at the same
  precision charged to the quantum value oracle.  There is no quantum-only
  input oracle.  Enumerating all structural entries and forming the right-hand
  sides costs \(O(D_t\tau+q_tD_t)\).
- **Robust outer contract.** The convergence proof accepts every direction
  satisfying

  \[
   \|K_t\widehat d_{t,j}-r_{t,j}\|_2
   \leq \eta_{t,j}\|r_{t,j}\|_2.                         \tag{1}
  \]

- **Full classical update.** The hybrid algorithm materializes the dense
  classical direction or updated iterate as \(\Theta(D_t)\) machine words
  before it constructs the next nonlinear Newton system.

The last condition captures the usual QLSA--tomography--classical-update
architecture.  Keeping a solution state coherent does not satisfy it.

## The trajectory replacement theorem

### Theorem 1

Under the model above, there is a classical implementation with the same
outer iteration guarantee and real-arithmetic work

\[
 \boxed{
 \sum_{t=1}^T
 O\!\left(D_t\tau_t^2+q_tD_t\tau_t\right)
 }
                                                               \tag{2}
\]

and peak factor storage

\[
 O\!\left(\max_t D_t\tau_t\right).                            \tag{3}
\]

Symbolic analysis is performed once for the common supergraph and order.  A numerical
factorization is performed once per outer iteration and is reused for all
predictor, corrector, or refinement right-hand sides having the same
\(K_t\) exactly.

Consequently, if \(D_t=\Theta(D)\), \(q_t=O(1)\), and
\(\tau_t\leq\tau\), a full-output hybrid QIPM has a dimension-only total-work
speedup ceiling

\[
 \widetilde O(\tau^2).                                       \tag{4}
\]

For \(\tau=D^{o(1)}\), this excludes a polynomial speedup in \(D\).  For
constant \(\tau\), classical factorization and the classical-output floor are
both linear per materialized Newton update.

### Proof

In an elimination order of width \(\tau_t\), each eliminated scalar has at
most \(\tau_t\) later neighbors.  Its numerical update changes a dense
\(\tau_t\)-by-\(\tau_t\) frontal block, so summing over the \(D_t\) columns
costs \(O(D_t\tau_t^2)\) arithmetic.  The factor contains
\(O(D_t\tau_t)\) scalars.  Forward and backward substitution therefore cost
\(O(D_t\tau_t)\) per right-hand side.

The graph and order depend only on the symbolic support and can be cached.
The pivots and Schur-complement entries depend on the current barrier scaling,
so the numerical factor cannot in general be cached across iterations.  It
can be reused inside one predictor--corrector iteration when the matrix is
unchanged.

Solve each right-hand side until (1) holds and feed that direction to the
outer update.  The classical directions can generate a different adaptive
trajectory from the quantum approximations.  The uniform graph, access,
factorization, and outer-iteration hypotheses above therefore apply to every
legal trajectory, not merely the matrices realized on one quantum run.  The
robust outer contract then gives the same iteration bound even though the
classical direction need not equal the random tomographic output.
This proves (2)--(3).

Materializing a dense \(D_t\)-word update costs \(\Omega(D_t)\) word writes.
Summing this cost over the same trajectory and comparing with (2) gives (4).
This is an output-contract lower bound, not a claim that \(T\) unrelated
oracle strings occur in one fixed optimization instance.  In particular, it
does not preclude numerical factor updates when only a small local part of
\(K_t\) changes. ∎

## Arithmetic count versus bit complexity

Theorem 1 counts real arithmetic.  Suppose the factorization and triangular
solves have normwise backward error
\(\beta_tu\|K_t\|_2\), where \(\beta_t\) includes dimension, scaling, and
growth factors.  Choosing unit roundoff

\[
 u=O\!\left(\frac{\eta_{t,j}}
 {\beta_t\kappa_2(K_t)}\right)                              \tag{5}
\]

suffices for (1), up to an absolute implementation constant and ordinary
scaling assumptions.  Thus

\[
 B_t=O\!\left(L_t+\log\beta_t+\log\kappa_2(K_t)
                  +\log(1/\eta_{t,j})\right)                \tag{6}
\]

working bits suffice when input entries have \(L_t\) bits.  For well-scaled
SPD Cholesky, standard bounds give \(\beta_t=\operatorname{poly}(D_t)\).
Residual recomputation or iterative refinement adds \(O(D_t\tau)\) work per
round.  Bit work is (2) multiplied by the cost of \(B_t\)-bit arithmetic;
storage is (3) times \(B_t\).  Equation (6) is not a
strong-polynomiality claim.

Symmetric quasi-definiteness guarantees existence of pivot-free \(LDL^T\)
under symmetric permutations, but existence alone is not a numerical
stability theorem.  The indefinite extension of Theorem 1 therefore retains
the explicit stable-order or bounded-growth hypothesis.  This distinction is
consistent with the classical theory of
[symmetric quasi-definite matrices](https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/1993/93-72.html).

## An unconditional query lower bound at treewidth zero

The word-output argument can be strengthened to an oracle-query lower bound.

### Theorem 2

There is a strictly feasible separable box LP whose first Newton step has
an input-independent condition-one, treewidth-zero Hessian, but producing a
constant-relative-\(\ell_2\) classical approximation to that Newton direction
requires \(\Omega(D)\) bounded-error quantum coefficient queries.

### Proof

Fix a public constant \(0<\alpha\leq1/4\).  For
\(z\in\{0,1\}^D\), put

\[
 b_z=D^{-1/2}\big((-1)^{z_1},\ldots,(-1)^{z_D}\big)
\]

and consider

\[
 \min\ \alpha b_z^Tx\qquad\text{subject to}\qquad 0\leq x\leq2e \tag{7}
\]

with logarithmic barrier

\[
 \Phi(x)=-\sum_{i=1}^D[\log x_i+\log(2-x_i)].              \tag{8}
\]

At the public analytic center \(x^0=e\),

\[
 \nabla\Phi(x^0)=0,\qquad \nabla^2\Phi(x^0)=2I,
\]

and the Newton direction for \(b_z^Tx+\Phi(x)\) is

\[
 \Delta_z=-\frac\alpha2 b_z.                               \tag{9}
\]

The matrix has treewidth zero and condition number one.  Moreover,

\[
 \|\Delta_z\|_{\nabla^2\Phi(x^0)}^2=\frac{\alpha^2}{2},
\]

so the start lies comfortably in conventional short-step neighborhoods.  The
constant scaling does not change the normalized direction or the relative
output lower bound.

Suppose a quantum algorithm outputs a classical \(\widehat\Delta\) with

\[
 \|\widehat\Delta-\Delta_z\|_2
 \leq\epsilon\|\Delta_z\|_2.                              \tag{10}
\]

Every coordinate whose sign is rounded incorrectly contributes at least
\(\alpha^2/(4D)\) to the squared error.  Hence sign rounding makes at most
\(\epsilon^2D\) bit errors.

For completeness, the standard oracle-interrogation lower bound can be seen
from the polynomial/Fourier method.  After \(Q\) phase queries, the family of
final states lies in the span of Boolean Fourier characters of degree at most
\(Q\), of dimension

\[
 M_Q=\sum_{j=0}^Q {D\choose j}.                             \tag{11}
\]

Choose an exponentially large code in \(\{0,1\}^D\) with relative distance
greater than \(2\epsilon^2\).  The successful rounded-output regions for its
codewords are disjoint.  A dimension/packing bound then requires \(M_Q\) to
be exponential in \(D\).  The binomial entropy bound implies \(Q=\Omega(D)\)
for every sufficiently small fixed \(\epsilon\).  This is the approximate
oracle-interrogation phenomenon studied by
[van Dam](https://arxiv.org/abs/quant-ph/9805006).

Thus (10) requires \(\Omega(D)\) coefficient queries, even if access to the
Newton matrix is free. ∎

The normalized state \(|\Delta_z\rangle\) is easy to prepare from a uniform
superposition and one phase query.  Theorem 2 therefore isolates the missing
resource exactly: converting that state into a useful dense classical IPM
update, not solving the condition-one diagonal system.

The older local box-LP theorem is stronger for scalar output at high absolute
precision: additive objective error below \(1/2\) computes the hidden Hamming
weight or parity information with \(\Omega(D)\) queries.  Theorem 2 instead
uses constant relative vector error and makes the state-versus-classical
direction boundary explicit.

## Parallel-depth corollary

Suppose additionally that an SPD system is supplied with a balanced
multifrontal tree of height \(h\) and front width \(O(\tau)\).  Independent
fronts at one level can be processed simultaneously.  A direct dense
implementation inside each front gives

\[
 \begin{array}{ll}
 \text{factorization work:} & O(D\tau^2),\\
 \text{factorization depth:} & O(h\tau^3),\\
 \text{triangular-solve depth:} & O(h\tau^2).
 \end{array}                                                \tag{12}
\]

Balanced-separator recursion for a width-\(\tau\) graph yields
\(h=O(\log D)\) and width \(O(\tau)\); the constant hidden in the width may
increase.  A constructive statement with width at most \(6\tau+5\) is given
by [Jain and Tewari](https://www.cse.iitk.ac.in/users/rtewari/papers/tree_decomp.pdf),
Theorem 3.  Hence constant-treewidth SPD Newton solves have linear classical
work and logarithmic-depth arithmetic circuits.  If, in addition, the
nonlinear iterate update, line search, coefficient refresh, and stopping
test at each of an inherently sequential \(T\)-step trajectory all have
polylogarithmic depth, then the complete classical trajectory has depth
\(O(T\,\operatorname{polylog}D)\).  Equation (12) alone establishes only
the Newton-solve part of that statement.  Under the extra refresh
hypothesis this rules out an exponential parallel-depth separation for the
same full-output trajectory, but it does not compare against a quantum
algorithm with a different global iteration scheme.

The depth statement is deliberately conditional on a balanced elimination
tree.  An arbitrary supplied width-\(\tau\) ordering can have height
\(\Theta(D)\).

## Conic and chordal consequences

For products of bounded-order LP, SOC, rotated-SOC, or fixed-size PSD blocks,
a bounded-width factor graph gives a bounded-width augmented Newton graph
only when the local scaling blocks and equality rows fit in the stated bags.
Large Lorentz or PSD blocks can create large dense fronts despite sparse
external incidence.

For sparse SDP, treewidth of the original aggregate graph is not the right
hypothesis.  Zhang gives aggregate-treewidth-zero examples whose chordal
conversion still requires cubic per-iteration work.  The sufficient object is
an extended aggregate graph that makes every constraint support a clique;
bounded width there gives linear work per IPM iteration
[[zhang2024-complexity-of-chordal-conversion-for]].  The dualized clique-tree
conversion gives the same linear-per-iteration conclusion for its covered
constant-clique families
[[zhang2020-sparse-semidefinite-programs-with-guaranteed]].

Consequently, on these covered chordal SDP families, a tomography-based QIPM
that follows the same IPM schedule and materializes \(\Theta(m+n)\) Newton
coordinates per iteration cannot improve the asymptotic per-step work.  This
does not contradict chordal-conversion degeneracy: clique conversion can
introduce nonunique multipliers and worsening Schur conditioning
[[raghunathan2016-degeneracy-in-maximal-clique-decomposition]].

## Oracle construction and refresh closure

Treewidth is a sparsity statement, not an access primitive.

For one Newton step, the relevant comparison is the complete ledger

| Stage | Hybrid quantum route | Matched classical route |
|---|---|---|
| current entries and RHS | coherent value-oracle construction or refresh | direct local evaluation |
| linear solve | QLSA state preparation, with normalization, condition, and precision costs | \(O(D\tau^2)\) factorization and \(O(D\tau)\) per RHS |
| update output | coherent tomography or another classical extraction method | triangular solve already returns the classical vector |
| next system | explicit update of the iterate-dependent values, or a proved coherent nonlinear refresh | direct evaluation from the explicit iterate |

No stage in the first column is free merely because the support has small
treewidth.

- It does not bound maximum degree: a star has treewidth one and degree
  \(D-1\).
- Constructing a coherent lookup table from explicit sparse entries costs at
  least the source writes needed to load those entries.
- If all local barrier weights change after a materialized update, rebuilding
  or updating their explicit value table costs \(\Omega(D)\) source writes at
  constant treewidth.
- If the algorithm is instead supplied a persistent coherent oracle that
  evaluates the new entries from an implicit quantum iterate, this loading
  lower bound does not apply.  Such an oracle is an additional algorithmic
  resource and lies outside Theorem 1's explicit-update model.

End-to-end QIPM resource analyses already emphasize QRAM construction,
changing matrix data, and tomography
[[dalzell2023-end-end-resource-analysis-quantum]].  The new point here is the
closed dichotomy: either the next iterate is explicit, in which case
low-width classical elimination matches its output cost up to
\(\widetilde O(\tau^2)\), or it remains implicit, in which case the algorithm
must supply and analyze a coherent nonlinear iterate-to-Newton-oracle update.

## Limits and novelty boundary

The theorem does not cover:

- quantum-state, sampling, scalar-value, or few-observable output;
- a quantum-only coefficient oracle;
- a fully coherent sequence with no classical iterate materialization;
- arbitrary indefinite KKT systems without controlled pivoting and growth;
- raw aggregate treewidth when cone scaling or chordal conversion enlarges
  the actual Newton graph;
- large cone blocks hidden behind a single factor-graph vertex; or
- algorithms using a different barrier, iteration schedule, or non-IPM
  global evolution.

Sparse Cholesky, quasi-definite \(LDL^T\), multifrontal parallelism, oracle
interrogation, chordal conversion, and output lower bounds are prior art.  A
targeted search found no source stating the combined adaptive-trajectory
replacement theorem with its residual contract, exact numerical-graph
hypothesis, symbolic-versus-numeric reuse rule, and explicit-or-coherent
refresh dichotomy.  That synthesis, plus the treewidth-zero Newton
oracle-interrogation witness, is the defensible apparent novelty; priority is
not guaranteed.
