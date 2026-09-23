# A fixed sparse KKT ray collapses repeated QLS query costs

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the algebra and noncomposition theorem; moderate on the
novelty of the conic wrapper

## Main result

Let \(M_\theta\in\mathbb R^{n\times n}\) be an invertible matrix selected by
a hidden input \(\theta\), with at most \(s\) nonzeros per row and column.
Assume bidirectional sparse-location/value access: both \(M_\theta\) and
\(M_\theta^T\) have their row oracles. Let \(e\) be a public unit basis
vector. Consider the one-cone SOCP

\[
 \begin{aligned}
  \operatorname*{maximize}_{x,u}\quad&2e^Tu,\\
  \text{subject to}\quad&u=M_\theta x,\\
  &(1,u)\in Q_{n+1}.
 \end{aligned}                                                    \tag{1}
\]

Use the fixed-scale Lorentz barrier

\[
                  \phi(u)=-\log(1-\|u\|^2).                       \tag{2}
\]

Then all exact central predictors of (1), at every central multiplier,
have the same normalized augmented-KKT solution state. Writing

\[
                         v_\theta=M_\theta^{-1}e,                  \tag{3}
\]

that state is

\[
 {(|u\rangle,|x\rangle,|\lambda\rangle)\text{-amplitudes}
  \over\text{normalization}}
       ={(e,v_\theta,0)\over\sqrt{1+\|v_\theta\|^2}},              \tag{4}
\]

independently of the path parameter. The augmented KKT matrix is only
\((s+2)\)-sparse and every one of its hidden entries comes from \(M_\theta\).

At the same time, starting at the analytic center, reaching any feasible
point of objective gap at most \(0<\epsilon\leq1\) requires

\[
 T\ \geq\
       {\log(1/\epsilon)
       \over m\log(1/(1-R))}                                      \tag{5}
\]

rounds if a round contains at most \(m\) chords of starting Dikin norm at
most \(R<1\). The movement lower bound can therefore be made arbitrarily
large by requesting high optimization accuracy, while the normalized KKT
target never changes.

This gives a fixed-instance noncomposition theorem. If preparing
\(|v_\theta\rangle\) once has sparse-oracle query lower bound \(q\), then
each checkpoint KKT solve, considered in isolation, inherits that lower
bound. It is nevertheless invalid to conclude a total lower bound \(Tq\):
the hidden input can be learned once, or \(v_\theta\) can be materialized
once, and every later center and direction is obtained by public scalar
rescaling. An elementary four-sparse signed-tree family already gives a
one-shot lower bound and matching classical solve cost
\[
                         q=\Theta(L)=\Theta(\kappa)
\]
at constant state error. For the precision-sensitive constant-sparsity
parity-clock family of Mori et al., in their stated regime
\(0<\delta\leq1/11\),
the one-shot lower and the cost of reading the whole hidden input are both

\[
             \Theta\!\bigl(\kappa\log(1/\delta)\bigr),             \tag{6}
\]

where \(\delta\) is the QLS state error and
\(\kappa=\kappa_2(M_\theta)\). The total raw-query cost for any number of
central checkpoints remains of this order in Mori et al.'s canonical
source-bit oracle model, not this order times (5).

The theorem is a decisive obstruction to multiplying a worst-case
**one-shot** QLS lower bound by an IPM movement count. It does not rule out
a different fixed program whose required final output has a genuine
direct-product query lower bound.

## 1. Exact central ray

Eliminate the equality in (1), but retain \(u\) to display the sparse KKT
system. At objective multiplier \(\eta\geq0\), the centering problem is

\[
   \min_{u=M_\theta x,\ \|u\|<1}
       \phi(u)-2\eta e^Tu.                                        \tag{7}
\]

Since \(M_\theta\) is invertible, stationarity in \(x\) forces the equality
multiplier to vanish. Stationarity in \(u\) then gives

\[
              {u\over1-\|u\|^2}=\eta e.
\]

Consequently there is a unique \(a=a(\eta)\in[0,1)\) satisfying

\[
              {a\over1-a^2}=\eta,
 \qquad u(\eta)=ae,
 \qquad x(\eta)=av_\theta.                                      \tag{8}
\]

Thus the entire central path lies on one hidden ray. Differentiating the
first identity in (8) gives

\[
              a'(\eta)={(1-a^2)^2\over1+a^2}.                     \tag{9}
\]

## 2. The sparse augmented KKT solve is identical at every checkpoint

Put \(q_a=1-a^2\). At \(u=ae\), the barrier Hessian is

\[
 D_a=\nabla^2\phi(ae)
       ={2\over q_a}I+{4a^2\over q_a^2}ee^T.                      \tag{10}
\]

The exact predictor equations obtained by differentiating (7) are

\[
 \underbrace{
 \begin{pmatrix}
   D_a&0&I\\
   0&0&-M_\theta^T\\
   I&-M_\theta&0
 \end{pmatrix}}_{K_a}
 \begin{pmatrix}\dot u\\\dot x\\\dot\lambda\end{pmatrix}
 =
 \begin{pmatrix}2e\\0\\0\end{pmatrix}.                            \tag{11}
\]

The second block row and invertibility of \(M_\theta\) give
\(\dot\lambda=0\); the third gives \(\dot u=M_\theta\dot x\). The
\(e\)-eigenvalue of \(D_a\) is

\[
              {2(1+a^2)\over q_a^2}.
\]

Therefore the unique solution of (11) is

\[
       (\dot u,\dot x,\dot\lambda)
          ={q_a^2\over1+a^2}(e,v_\theta,0)
          =a'(\eta)(e,v_\theta,0),                                \tag{12}
\]

which proves (4).

Matrix (11) has row and column sparsity at most \(s+2\). Its diagonal
block \(D_a\), its identity blocks, and its right-hand side are public;
one sparse-location or sparse-value query to \(K_a\) is simulated with at
most one query to \(M_\theta\) or \(M_\theta^T\), up to a public constant
number of routing queries. There is no dense normal-matrix oracle hidden
in this statement. Row/column sparsity by itself does not construct a
transpose row oracle from a standard one-direction row oracle; the
bidirectional access assumption above is part of the theorem.

Assume the public normalization \(\|M_\theta\|\leq1\). Then
\(\|v_\theta\|\geq1\), so the \(x\) register in (4) has probability at
least \(1/2\). Measuring that register and postselecting yields exactly
\(|v_\theta\rangle\). The same reduction is robust to sufficiently small
constant Euclidean state error. Hence any sparse-access lower bound for
preparing \(|M_\theta^{-1}e\rangle\) transfers, with constant loss, to the
literal augmented KKT state (4) at **every** checkpoint.

This is a state-output statement. A scalar expectation, one sample from
the squared-coordinate distribution, an SQ oracle for the direction, a
classical vector, and a reusable state-preparation unitary are different
contracts and do not automatically inherit the same lower bound.

## 3. Movement lower bound on the same fixed program

The equality \(u=M_\theta x\) makes the feasible affine slice isomorphic to
the unit ball. Pullback by \(M_\theta\) is an isometry between its barrier
metric and that of (2). For \(r=\|u\|\), direct inversion of (10) gives

\[
       \|\nabla\phi(u)\|_{u,*}^2
          ={2r^2\over1+r^2}\leq1.                                 \tag{13}
\]

If a feasible point has maximization gap at most \(\epsilon\), then

\[
 2-2e^Tu\leq\epsilon
 \quad\Longrightarrow\quad
 r\geq e^Tu\geq1-\epsilon/2
 \quad\Longrightarrow\quad
 1-r^2\leq\epsilon.                                                \tag{14}
\]

Thus \(\phi(u)-\phi(0)\geq\log(1/\epsilon)\). Equation (13) and the
fundamental theorem of calculus show that every interior path from the
analytic center to the feasible \(\epsilon\)-accurate set has barrier-metric
length at least this amount. A chord of starting Dikin norm at most
\(R<1\) has length at most \(\log(1/(1-R))\) by Hessian comparison.
Allowing at most \(m\) such chords per round proves (5). Intermediate
points need only remain in the interior of the affine slice.

Equation (5) is for the explicit primal barrier (2). It is not the
arbitrary-LHSC primal--dual Nesterov--Todd theorem, and it does not apply
to unbounded local-norm jumps.

## 4. Elementary four-sparse parity witness

The one-shot hardness in the main result has a self-contained bounded-error
witness with a linear classical solve. Fix \(L\geq2\), hidden signs
\(\sigma_1,\ldots,\sigma_L\), and
\[
                         H=\prod_{i=1}^L\sigma_i.                 \tag{15a}
\]
Let \(h=2^{\lceil\log_2L\rceil}\). Form a rooted dependency tree with:

1. a path \(p_0,p_1,\ldots,p_L\), whose edge into \(p_i\) has sign
   \(\sigma_i\);
2. a complete public binary tree with \(h\) leaves rooted at \(p_0\);
3. a disjoint complete hidden binary tree with \(h\) leaves rooted at
   \(p_L\).

For the root use the equation \(y_{p_0}=1\). For every other node \(z\)
with parent \(\pi(z)\), use
\[
                 y_z-s_z y_{\pi(z)}=0,                           \tag{15b}
\]
where \(s_z=\sigma_i\) on path edge \(p_{i-1}p_i\) and \(s_z=1\) on
the two copy trees. These equations define a square triangular matrix
\(A_\sigma\) and public basis right-hand side \(e_0\). Every row has at
most two nonzeros and every column at most four. Put
\[
                    M_\sigma={A_\sigma\over\sqrt8}.               \tag{15c}
\]
The row/column norm bound gives \(\|M_\sigma\|\leq1\).

The exact solution of \(A_\sigma y=e_0\) is \(+1\) on every public-tree
node and \(H\) on every hidden-tree node; the path nodes contain the prefix
parities. The total number of variables is
\[
                         N_L=L+4h-3=\Theta(L).                    \tag{15d}
\]
Let \(|P\rangle\) and \(|H_{\rm leaf}\rangle\) be the public uniform
superpositions over the two sets of \(h\) leaves. Measuring the normalized
solution in the two public directions
\[
              {|P\rangle+|H_{\rm leaf}\rangle\over\sqrt2},
        \qquad
              {|P\rangle-|H_{\rm leaf}\rangle\over\sqrt2}          \tag{15e}
\]
reveals \(H\) whenever the leaf subspace is hit. Its probability is
\(2h/N_L\geq2/5\). A constant number of preparations and majority
amplification therefore computes parity with bounded error. Preparing
\(|M_\sigma^{-1}e_0\rangle\), or the augmented KKT state (4), to a
sufficiently small constant Euclidean error needs \(\Omega(L)\) sign
queries. Reading all signs gives the matching \(O(L)\) upper bound.

The condition number is \(\Theta(L)\). Indeed,
\(\|A_\sigma\|=O(1)\); its inverse has row and column sums \(O(L)\), so
\(\|A_\sigma^{-1}\|=O(L)\). The signed path principal subproblem is,
after diagonal sign changes, the \(L\times L\) cumulative-sum matrix,
whose norm is \(\Omega(L)\). Scaling in (15c) does not change the
condition number. The dependency graph is a tree, and (11) has a
constant-width decomposition with bags
\(\{\lambda_z,x_z,x_{\pi(z)},u_z\}\). Forward substitution solves
\(M_\sigma v=e_0\) in \(O(L)\) arithmetic.

Thus every checkpoint KKT state is separately
\(\Theta(L)=\Theta(\kappa)\)-query hard, on a constant-width system with a
linear-time classical solve. Nevertheless, after one \(O(L)\)-query solve,
the same stored vector serves every checkpoint. This is already enough to
refute a generic multiplication by (5).

## 5. Exact temporal collapse and the classical reuse baseline

Once \(v_\theta\) is known, equations (8), (9), and (12) generate every
exact center and predictor using only public scalar arithmetic. In
particular, an implicit classical iterate needs only the pair
\((a,v_\theta)\). A factorization or solve for \(M_\theta v=e\) is paid
once. It is not paid once per central multiplier.

For a generic sparse matrix, LSQR applied once to \(M_\theta v=e\) costs

\[
 O\!\left(\operatorname{nnz}(M_\theta)\,
          \kappa_2(M_\theta)\log(1/\zeta)\right)                   \tag{15}
\]

arithmetic in exact-arithmetic convergence accounting, for a matched
residual tolerance \(\zeta\). Later implicit centers and predictors cost
\(O(1)\) scalar work; materializing each dense vector costs \(O(n)\) writes,
but still no new input queries. A supplied sparse factorization or narrow
elimination ordering can improve the one-time solve further.

The parity-clock matrices used for the fixed-sparsity QLS lower bound have
more structure. They have the form
\(M_\theta=c(I-\gamma U_\theta)\) for a public \(c>0\), where a clock step
applies one hidden bit gate.
After reading the \(N_{\rm bit}\) hidden bits once, the inverse history

\[
 M_\theta^{-1}e
   ={c^{-1}\over1-\gamma^L}
        \sum_{j=0}^{L-1}\gamma^jU_\theta^je                       \tag{16}
\]

is classically generated in support-linear time. Mori et al.'s parameter
choice has

\[
 N_{\rm bit}=\Theta\!\bigl(\kappa\log(1/\delta)\bigr),             \tag{17}
\]

matching their one-shot quantum query lower bound up to constants. Reading
those bits, constructing (16), and retaining it therefore answers any
number of requests for (4) with the query cost (6). Quantum gates, memory,
and repeated dense output are not free in an end-to-end ledger; the point
is specifically that raw-input queries do not acquire a factor (5).
This matching upper bound uses the canonical source-bit realization, in
which each hidden bit controls a designated clock transition. Under a
generic sparse-coefficient oracle, the unconditional fallback is to read
all addressable coefficient words as in the next section.

## 6. General fixed-oracle information cap

The example illustrates a model-independent cap. Suppose a fixed problem
instance is described by \(B\) addressable coefficient words and one query
returns one whole word. With arbitrary computation and storage, reading
all \(B\) words once gives

\[
                 Q_{\rm total}\leq B                               \tag{18}
\]

for every later trajectory computation and output relation. Therefore a
claimed fixed-instance lower bound \(Tq\) must at least satisfy
\(Tq\leq B\), and it still needs a single adversary or hybrid argument for
the required final transcript. Applying a one-shot lower bound separately
to \(T\) calls is never such an argument.

For an \(n\)-dimensional row-and-column-\(s\)-sparse matrix with independently
addressable nonzeros, \(B=O(ns)\). A lower bound larger than this cannot be
an ordinary coefficient-query theorem, regardless of the number of IPM
rounds. Row queries that return an entire sparse row only reduce the cap.
This observation concerns word queries; bit complexity can be larger when
one coefficient word contains many bits.

A genuine fixed-instance product theorem needs at least one additional
ingredient:

1. the final scalar or classical solution itself computes a function with
   direct-product complexity;
2. a required online transcript exposes independent outputs before later
   computation;
3. a compile-and-commit contract revokes the raw oracle and demands a
   reusable service; or
4. a proved memory bound prevents caching enough information.

Without one of these, “fresh along the central path” is geometry, not an
oracle lower-bound premise.

## 7. What is and is not new

The reduced central-ray identity for this SOCP also appears in the local
[parameterized one-cone scalar
frontier](2026-09-04-parameterized-one-cone-scalar-frontier.md). The new
step here is to retain the equality variables and prove the exact sparse
augmented-KKT identity at every central multiplier.

The sparse QLS lower bound used in (6) is prior work:

- R. Mori, Y. Kikuchi, M. Benedetti, and M. Rosenkranz,
  [*Sparsity-dependent complexity lower bound of quantum linear system
  solvers*](https://arxiv.org/abs/2601.16697).

Reuse and low-rank updating across sequences of IPM KKT systems are also a
classical theme; for example:

- S. Bellavia, V. De Simone, D. di Serafino, and B. Morini,
  [*On the update of constraint preconditioners for regularized KKT
  systems*](https://doi.org/10.1137/130947155).
- D. Ek and A. Forsgren,
  [*A structured modified Newton approach for solving systems of nonlinear
  equations arising in interior-point methods for quadratic
  programming*](https://optimization-online.org/2020/09/8030/).

The Lorentz SOCP itself is elementary. The apparently new contribution is
the exact sparse augmented-KKT identity (11)--(12), which places a literal
one-shot QLS-hard state unchanged at every point of an arbitrarily long
bounded-Dikin trajectory, together with the fixed-oracle cap (18). A
targeted search found work on reusing or updating KKT factorizations and
preconditioners, but no prior theorem using one conic instance to disprove
the multiplication of QLS query lower bounds by IPM movement lower bounds.
Priority requires specialist review.

## 8. Consequence for the current frontier

The existing one-sharing-cone theorem gives simultaneous readout and
movement lower bounds on one instance. This note explains why they are
correctly combined by a maximum. Even the stronger premise that every
individual checkpoint contains a QLS-hard sparse KKT system is insufficient
for multiplication: on (1), all of those systems ask for the same hidden
state.

The strongest safe fixed-instance conclusion presently available is
therefore

\[
       Q_{\rm total}=\Omega(q),\qquad T=\Omega(\log(1/\epsilon)),
       \qquad\text{with no inferred }\Omega(qT).                    \tag{19}
\]

Any future positive composition theorem must make the final-output,
online-transcript, oracle-revocation, or memory hypothesis explicit and
must prove a joint adversary bound.

## Independent hostile audit

The audit rederived the exact central ray, predictor derivative, augmented
KKT signs and solution, and the constant-one barrier-gradient bound behind
(5). It verified the postselection reduction to
\(|M_\theta^{-1}e\rangle\), Mori et al.'s
\(\Theta(\kappa\log(1/\delta))\) clock parameter count, and the finite-cycle
inverse (16). It also caught and repaired the need to assume sparse row
access to both \(M_\theta\) and \(M_\theta^T\).

For the elementary witness, the audit independently checked \(N_L=L+4h-3\),
row sparsity two, column sparsity four, the \(2h/N_L\geq2/5\) parity
measurement, \(\kappa=\Theta(L)\), width-three KKT bags, and the linear
forward solve. It found no product lower bound: the read-once upper and the
fixed-word cap remain valid for arbitrarily many checkpoints.
