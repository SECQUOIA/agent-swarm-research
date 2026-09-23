# Tight coordinate recovery for the non-SOCP block-tree parity SDP

Date: 2026-09-02

## Result

The non-SOCP Schur-block family in
`2026-09-02-nonsoc-schur-block-sdp-parity.md` has an output lower bound, but
that lower bound also has a matching constructive upper bound.  For fixed
block order, its free-coordinate central solve is public and block diagonal;
all input dependence enters only when the free solution is embedded back into
the requested original matrix coordinates.  That embedding can be carried out
with linear work and logarithmic workspace, and it cannot be carried out with
sublinear raw-oracle work.

More precisely, let

\[
 P=17N+1,\qquad \tau_i=\prod_{j=1}^{\min\{i,N\}}\sigma_j,
 \qquad \sigma_j\in\{\pm1\},
\]

and let \(k=3\), the smallest genuinely non-SOCP case.  (The constructive
upper bounds below hold for every fixed \(k\); fixing \(k=3\) lets us invoke
the existing lower bound with the stated numerical error \(1/100\).)  Let

\[
 X_{\tau_i}^{(k)}(t)=
 \begin{pmatrix}
  tI_k+e_1e_1^T&\tau_i e_1\\
  \tau_i e_1^T&1
 \end{pmatrix},
 \qquad 0<t\leq1.
 \tag{1}
\]

These are the exact primal central blocks at the public parameter
\(\mu=t/P\).  In the coherent fixed-position sparse-coefficient oracle model,
the following bounds hold.

1. Any one requested hidden coordinate
   \((X_i)_{1,k+1}=\tau_i\) can be recovered with
   \(L_i=\min\{i,N\}\) sign queries and constant workspace.  Conversely,
   bounded-error recovery requires at least \(L_i/2\) raw coefficient
   queries.  Thus a tail coordinate has query complexity \(\Theta(N)\).
2. All \(P\) central blocks can be streamed classically with exactly \(N\)
   sign queries, \(O(Pk^2)\) arithmetic/output operations in the
   real-arithmetic model, and constant extra workspace beyond the output.
   For fixed \(k\), this is linear.
3. The trace-normalized block-diagonal central matrix

   \[
   \rho_\sigma(t)=
   \frac{\bigoplus_{i=0}^{P-1}X_{\tau_i}^{(k)}(t)}{P(kt+2)}
   \tag{2}
   \]

   has a purification that can be prepared with at most \(2N\) sign-oracle
   queries, \(O(N\log P+\operatorname{polylog}(1/\epsilon))\) elementary
   gates, and \(O(\log P+\log(1/\epsilon))\) work qubits to trace-distance
   error \(\epsilon\).  The previously proved parity decoder gives a lower
   bound of \(N/2\) raw coefficient queries when \(\epsilon\leq1/100\).
   Hence one-copy density-state preparation has tight raw-query complexity
   \(\Theta(N)=\Theta(P)\).

The upper bound in item 3 does **not** require materializing a length-\(P\)
prefix table or assuming QRAM.  It is a direct coherent prefix-phase circuit.
Thus the lower bound is genuinely a data-query/work bottleneck, not a linear
quantum-memory lower bound.

## 1. Coordinate recovery is exactly prefix parity

Every entry of (1) is public except

\[
 (X_i)_{1,k+1}=(X_i)_{k+1,1}=\tau_i.
 \tag{3}
\]

Query \(\sigma_1,\ldots,\sigma_{L_i}\) and maintain their product in one bit.
This proves the upper bound in item 1.  For the lower bound, an algorithm
estimating (3) with constant success probability, say at least \(2/3\),
computes parity
of the first \(L_i\) input signs.  The bounded-error quantum query complexity
of parity is at least \(L_i/2\).  A raw query to the sole input-dependent
coefficient \(-\sigma_jF_1\) and a sign-oracle query simulate one another with
constant overhead, because the support position and coefficient magnitude are
public.

For a list of requested coordinates, put \(L\) equal to the largest prefix
length among its hidden off-diagonal entries.  Querying the first \(L\) signs
once, scanning their prefixes, and emitting the requested entries costs
\(O(L+q)\) time for \(q\) outputs.  If the list contains the hidden coordinate
of a block with prefix length \(L\), the same parity reduction gives an
\(L/2\) quantum-query lower bound.  This is an output-sensitive description:
public entries are free, while the cost of a hidden coordinate is controlled
by the deepest tree path on which it lies.

For all blocks, a single left-to-right scan computes every \(\tau_i\).  Each
constant-size block is then emitted from (1).  This proves item 2.  The scan
uses constant extra workspace if output is written sequentially.

## 2. An explicit constant-rank local purification

Write \(w_\tau=\tau e_1+e_{k+1}\).  Equation (1) has the exact Gram
decomposition

\[
 X_\tau^{(k)}(t)
 =t\sum_{j=1}^k e_je_j^T+w_\tau w_\tau^T,
 \qquad \operatorname{tr}X_\tau^{(k)}(t)=kt+2.
 \tag{4}
\]

Let the environment labels \(0,1,\ldots,k\) be orthogonal.  A purification of
the trace-normalized local block is

\[
 |\phi_\tau(t)\rangle
 =\frac{1}{\sqrt{kt+2}}
 \left[
   \sqrt t\sum_{j=1}^k|j\rangle_S|j\rangle_E
   +(\tau|1\rangle_S+|k+1\rangle_S)|0\rangle_E
 \right].
 \tag{5}
\]

Tracing out the second register gives \(X_\tau^{(k)}(t)/(kt+2)\).  Therefore

\[
 |\Phi_\sigma(t)\rangle
 =\frac1{\sqrt P}\sum_{i=0}^{P-1}
 |i\rangle_S|i\rangle_E|\phi_{\tau_i}(t)\rangle
 \tag{6}
\]

purifies (2).

## 3. Direct coherent preparation without a prefix table

First prepare the public state obtained from (6) by replacing every
\(\tau_i\) by \(+1\).  Uniform superposition over the public range
\(\{0,\ldots,P-1\}\) and the fixed-dimensional state (5) require only public
rotations.  They can be synthesized to total error \(\epsilon\) with
\(\operatorname{polylog}(1/\epsilon)\) overhead; fixed \(k\) is important
here.

It remains to put the phase \(\tau_i\) only on the component

\[
 |i\rangle_S|i\rangle_E|1\rangle_S|0\rangle_E.
 \tag{7}
\]

For each \(j=1,\ldots,N\), do the following.

1. Query \(\sigma_j\) into one work qubit.
2. Apply a phase \(-1\) to (7) iff \(i\geq j\) and \(\sigma_j=-1\).
3. Unquery the work qubit.

For a fixed address \(i\), the accumulated phase is

\[
 \prod_{j=1}^N \sigma_j^{[i\geq j]}
 =\prod_{j=1}^{\min\{i,N\}}\sigma_j=\tau_i.
 \tag{8}
\]

Thus the final state is (6).  There are two oracle calls per input sign.  A
comparison of a \(\lceil\log P\rceil\)-qubit address with a fixed classical
threshold costs \(O(\log P)\) elementary reversible gates and logarithmic
workspace, proving item 3.  If \(N\) clean input bits are retained instead of
unqueried, one query per sign suffices, at the price of \(O(N)\) workspace.

This preparation is exact in the real-rotation idealization.  In a discrete
fault-tolerant gate set, only the public uniform-state and constant-dimensional
local rotations are approximate; the input-dependent prefix phases are exact.
The claimed \(\epsilon\) dependence should be read in that standard synthesis
model.

### 3.1 The complete central-triple amplitude state is also tight

The same circuit closes the upper bound for the complete
primal--multiplier--slack amplitude state defined in the source note.  From
its explicit formulas, the only input-dependent signs are:

- the primal off-diagonal coordinates, proportional to \(\tau_i\);
- the dual-slack off-diagonal coordinates, proportional to \(-\tau_i\); and
- the signed-chain multiplier \(\alpha_i\), proportional to \(\tau_i\).

Every magnitude and every remaining sign is public as a function of \(i,t\),
and \(P\).  First prepare the amplitude encoding of this public unsigned
vector.  A standard binary-tree rotation circuit uses \(O(P)\) ideal
arbitrary-angle gates for fixed \(k\).  Then run the coherent prefix-phase
loop of Section 3, with an additional public predicate selecting precisely the
three coordinate classes above.  It supplies the factor \(\tau_i\); a public
phase supplies the minus sign in the slack class.  This uses \(2N\) raw sign
queries and \(O(P+N\log P)\) ideal gates, without QRAM.  Synthesizing the
\(O(P)\) public rotations separately gives the conservative fault-tolerant
bound \(O(P\log(P/\epsilon)+N\log P)\).

The source note proves an \(N/2\)-query lower bound for trace-distance error
\(1/100\), uniformly for \(0<t\leq1\).  Thus full central-triple amplitude
preparation, like density-state preparation, has tight raw-query complexity
\(\Theta(P)\).  The density purification is more structured and avoids the
linear list of rotation angles; the query conclusion is the same.

## 4. Why bounded block treewidth does not remove the cost

At the supernode level, the equality-factor graph consists of \(k+1\) rooted
paths and constant-size local PSD blocks.  A tree decomposition can keep two
adjacent block supernodes and their incident chain rows in a bag, so its width
is bounded by a constant depending only on \(k\).  This also has a direct
scalar KKT statement.  Put

\[
 q=\frac{(k+1)(k+2)}2,
\]

the number of svec coordinates per primal block.  In the condensed primal
Newton KKT graph \([H\ A^T;A\ 0]\), the barrier Hessian makes each block's
\(q\) coordinates a clique, while a transition row touches only its two
adjacent block cliques.  A path bag containing the coordinates of blocks
\(i-1,i\) and the \(k+1\) transition-row vertices at index \(i\) contains
every graph edge and has the running-intersection property.  Hence

\[
 \operatorname{tw}(K_{\rm KKT})\leq2q+k,
 \tag{9}
\]

which is an absolute constant for \(k=3\).  Root rows fit in the first bag.
After the public Schur
change of variables

\[
 Z_i=A_i-e_1e_1^T,
 \tag{10}
\]

the feasible tangent space is a product of independent \(\mathbb S^k\)
blocks, the center is simply \(Z_i=tI_k\), and the reduced barrier Hessian is
\((P^{-2}/\mu)I\).  Hence no difficult linear solve remains: even a perfect
bounded-treewidth Newton solver returns a public free-coordinate answer.

The map back to original coordinates still needs the labels \(\tau_i\).  The
theorem above pins its complexity down exactly:

\[
 \underbrace{\text{free central solve}}_{0\text{ input queries}}
 \quad\longrightarrow\quad
 \underbrace{\text{original-coordinate recovery/state loading}}
 _{\Theta(P)\text{ raw queries}}.
 \tag{11}
\]

Thus bounded treewidth, chordal decomposition, and condition-one reduced
geometry can make reconstruction the only input-dependent stage, but they do
not make that stage sublinear.  Conversely, the coherent construction shows
that reconstruction does not hide any additional superlinear cost.

In the unit-cost exact-arithmetic model, a generic symmetric system with a
supplied elimination ordering of scalar width \(w\) admits an
\(LDL^T\) factorization in \(O(Dw^2)\) arithmetic operations and
\(O(Dw)\) storage, followed by \(O(Dw)\) triangular solves.  For constant
\(w\), this gives the familiar linear classical comparator.  This standard
fact is only contextual here: the present family is stronger because its
free-coordinate solve is already explicit.  No numerical-stability or
bit-complexity conclusion is inferred from treewidth alone.

## 5. Abstract tree-holonomy loading theorem

The same upper/lower match is not specific to the entries in (1).  The
following formulation isolates the reusable mechanism.

Let \(T=(V,E)\) be a public rooted tree.  Every input edge has a sign
\(\sigma_e\in\{\pm1\}\), and each vertex has the transported label

\[
 \tau_v=\prod_{e\in\operatorname{path}(r,v)}\sigma_e.
 \tag{12}
\]

Let \(B_+,B_-\succeq0\) be two public constant-dimensional matrices with
the same trace \(T_0>0\), and put

\[
 \rho_\sigma=\frac1{|V|T_0}\bigoplus_{v\in V}B_{\tau_v}.
 \tag{13}
\]

Assume public constant-size circuits prepare purifications of
\(B_+/T_0\) and \(B_-/T_0\).  Then:

1. A purification of (13) can be prepared, without QRAM, using at most
   \(4|E|\) sign queries,
   \(O(|E|\log|V|+\operatorname{polylog}(1/\epsilon))\) gates, and
   \(O(\log|V|+\log(1/\epsilon))\) work qubits, up to error \(\epsilon\).
2. All labels and blocks can be streamed classically in
   \(O(|E|+|V|)\) time, one query per input edge, and space equal to the tree
   depth (or constant extra space on a path).  For a selected vertex set
   \(Q\), it suffices to query the edges in the union of its root paths.
3. Suppose the tree contains an unknown-sign path of length \(N\), followed
   by a public all-\(+1\) subtree of \(K=\Theta(N)\) output vertices, and all
   other vertices number \(O(N)\).  If

   \[
   d=\frac12\left\|\frac{B_+}{T_0}-\frac{B_-}{T_0}\right\|_1>0,
 \tag{14}
   \]

   then preparation of (13) to any fixed trace-distance error smaller than
   a sufficiently small constant depending only on \(d\) and \(K/|V|\)
   requires \(N/2\) input-edge queries.  Consequently its raw-query
   complexity is \(\Theta(N)\).

### Proof of the upper bound

Give the rooted tree a public depth-first-search order.  For an edge
\(e=(u,w)\), the predicate that \(e\) lies on the root-to-\(v\) path is
equivalent to \(v\) lying in the public preorder interval of the subtree
rooted at \(w\).  It can therefore be evaluated with two comparisons on
\(O(\log|V|)\)-bit addresses.

Prepare a uniform entangled vertex address
\(|V|^{-1/2}\sum_v|v\rangle_S|v\rangle_E\).  Loop over the edges.  Query the
current sign, toggle a label qubit iff the sign is negative and \(v\) lies in
the child subtree, and unquery the sign.  After the loop, the label qubit is
\(\tau_v\).  Use it to select the public local purification, then reverse the
loop to erase the label.  The forward and reverse loops use four queries per
edge and the stated gate and workspace bounds.  On the path instance, the
special phase relation in (5) removes the compute--uncompute pair and improves
four queries per unknown edge to the two queries used in Section 3.

The classical statement is the usual rooted-tree scan.  Restricting the scan
to the union of root paths proves the selected-output upper bound.

### Proof of the lower bound

All \(K\) public descendants of the unknown path endpoint have label equal to
the parity of the \(N\) unknown signs.  First project (13) onto these tail
blocks.  This event has the public constant probability
\(\alpha=K/|V|\).  Conditional on it, the normalized local state is either
\(B_+/T_0\) or \(B_-/T_0\).  Their Helstrom measurement has success
probability \((1+d)/2\).  Guessing randomly off the tail gives total parity
success probability

\[
 \frac12+\frac{\alpha d}{2}.
 \tag{15}
\]

A trace-distance preparation error \(\epsilon\) changes this success
probability by at most \(\epsilon\).  Taking
\(\epsilon<\alpha d/4\) leaves constant advantage, so the parity query lower
bound gives at least \(N/2\) edge-sign queries.  The preparation above gives
the matching linear upper bound.

This theorem applies to any fixed-size conic block family in which local
constraints transport a two-valued frame along a tree and the requested
original-coordinate block is \(B_{\tau_v}\).  Such a constraint-factor graph
has bounded block treewidth.  The theorem says that bounded treewidth makes
the transport computable in linear work; it does not make a global transported
label locally queryable.  The plateau is needed only to give the global label
constant weight in the normalized state.

## 6. Reuse, preprocessing, and what is not proved

- If the signs are read once and all prefixes are cached, later central states
  at different public values of \(t\) need no new raw input queries.  The
  lower bound applies to the first preparation from the sparse-coefficient
  oracle, not separately to every IPM iteration after charged preprocessing.
- A QRAM containing the prefix table can reduce online lookup depth, but
  building or refreshing its \(\Theta(P)\) input-dependent contents already
  pays the matching setup cost.  The direct circuit above avoids assuming
  such a memory.
- The result is a total-query/work statement.  With parallel input ports, a
  prefix network may reduce depth while still using linear total queries and
  work.
- Bounded treewidth alone does not imply a parity lower bound.  The lower
  bound uses the signed path holonomy in the reconstruction map.  Other
  bounded-treewidth instances can have completely public or locally
  recoverable embeddings.
- This does not prove a lower bound for returning only the public reduced
  variables \(Z_i\), an objective value, or another invariant summary.  It is
  tight specifically for original-coordinate recovery and the density-state
  interface (2).

## Assessment

The new content is a matching, QRAM-free coherent upper bound and an exact
coordinate-recovery characterization for the existing non-SOCP lower-bound
family.  The construction is elementary but closes an important logical gap:
the linear lower bound is neither an artifact of an inefficient output
routine nor evidence of a larger hidden memory cost.  It certifies a tight
separation between a trivial bounded-treewidth central solve and linear
original-coordinate state loading.  The targeted audit summarized below
found no exact collision, but this supports only an “apparently new”
output-interface conjunction, not an unconditional priority claim.

## Literature positioning

Zhang's chordal-conversion theorem gives linear classical IPM iterations under
bounded treewidth of the appropriate extended aggregate graph
[[zhang2024-complexity-of-chordal-conversion-for]].  It does not analyze the
raw-oracle cost of reconstructing a quantum state in the original coordinates.
The SDP QIPMs of Augustino--Nannicini--Terlaky--Zuluaga analyze quantum Newton
solves and direction recovery under QRAM/block-encoding access
[[augustino2023-quantum-interior-point-methods-semidefinite]], but do not give
this tree-holonomy loading separation.  The \(N/2\) parity bound and rooted-tree
scan used in the proof are standard ingredients.  Targeted searches on
treewidth/chordal QIPMs and parity-based state generation did not locate the
combined tight theorem above.  Accordingly, the potentially new claim is the
QIPM output-interface composition and its matching QRAM-free construction,
not either ingredient in isolation.
