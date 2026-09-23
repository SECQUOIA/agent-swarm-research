# Lazy versus reusable central-path oracles on a fixed sparse LP

## Status

This note asks whether changing IPM diagonal weights force a large data-structure
update at every iteration.  The answer is negative without a materialization or
memory restriction: on the fixed sparse family below, all path-parameter dependence
is a single explicit scalar, so a structural oracle can be reused for the entire
trajectory.

There is nevertheless a rigorous preprocessing-versus-lookup boundary:

* an exact, reusable endpoint central-value oracle costs \(\Omega(N)\) raw input
  queries to construct;
* a completely lazy coherent endpoint lookup costs \(\Omega(L)\) raw queries when
  each independent sparse chain has length \(L\);
* a trajectory service that explicitly returns one endpoint from each of \(K\)
  independent chains costs \(\Omega(KL)=\Omega(N)\) total raw queries, regardless of
  how preprocessing and online queries are interleaved.

The last statement is a lower bound for an explicit-coordinate service contract.  A
generic QIPM is not automatically required to make those coordinate requests, so it
is not an unconditional per-iteration QIPM lower bound.

## 1. Fixed block-path LP

Let \(K,L\ge1\).  For every block \(a\in[K]\), let
\(\sigma_{a,1},\ldots,\sigma_{a,L}\in\{-1,+1\}\), and introduce

\[
 d_{a,i}=u_{a,i}-v_{a,i},\qquad u_{a,i},v_{a,i}\ge0
 \quad(0\le i\le L).
\]

For a fixed \(\alpha\in(0,1)\), take the direct product of \(K\) LPs

\[
\begin{aligned}
 \min\quad&
  \sum_{a=1}^K\left[
    \sum_{i=0}^L(u_{a,i}+v_{a,i})+\alpha(u_{a,L}-v_{a,L})
  \right],\\
 \text{s.t.}\quad&d_{a,0}=1 &&(a\in[K]),\\
 &d_{a,i}-\sigma_{a,i}d_{a,i-1}=0
   &&(a\in[K],\ 1\le i\le L).
\end{aligned}                                                    \tag{1}
\]

The constraint graph is a disjoint union of paths.  Rows and columns have constant
sparsity, all nonzero matrix entries have magnitude one, and the instance size is
\(\Theta(KL)\).  Write

\[
 p_{a,0}=1,\qquad p_{a,i}=\prod_{j=1}^i\sigma_{a,j},\qquad
 q_{a,i}=u_{a,i}+v_{a,i}.                                      \tag{2}
\]

Exactly as for one chain, feasibility gives

\[
 u_{a,i}=\frac{q_{a,i}+p_{a,i}}2,qquad
 v_{a,i}=\frac{q_{a,i}-p_{a,i}}2,qquad q_{a,i}\ge1.            \tag{3}
\]

The LP is strictly primal-dual feasible.  Its primal central path has

\[
 q_{a,i}(\mu)=q(\mu):=\mu+\sqrt{\mu^2+1}                       \tag{4}
\]

for every block and position.  In the fixed orthonormal null basis
\(V_{a,i}=(e_{u_{a,i}}+e_{v_{a,i}})/\sqrt2\), the reduced primal
barrier Hessian is

\[
 V^TH_xV=
 2\mu\left[(q(\mu)+1)^{-2}+(q(\mu)-1)^{-2}\right]I.            \tag{5}
\]

It therefore has condition number one along the whole trajectory.

Crucially, the trajectory factors as

\[
 (u_{a,i}(\mu),v_{a,i}(\mu))
 =\left(\frac{q(\mu)+p_{a,i}}2,
         \frac{q(\mu)-p_{a,i}}2\right).                        \tag{6}
\]

All changing numerical information is the known scalar \(q(\mu)\); all hidden
structural information is the time-independent prefix parity table \(p_{a,i}\).

## 2. Oracle model

Encode \(\sigma_{a,i}=(-1)^{b_{a,i}}\) and give standard reversible access

\[
 O_b\lvert a,i,z\rangle
 =\lvert a,i,z\oplus b_{a,i}\rangle.                            \tag{7}
\]

The endpoint parity is

\[
 P_a:=p_{a,L}=(-1)^{\oplus_{i=1}^L b_{a,i}}.                   \tag{8}
\]

An endpoint central oracle at parameter \(\mu\) returns the pair in (6) with
\(i=L\).  Exact return of that pair gives \(P_a\).  A classical pair with both
coordinate errors strictly below \(1/2\) also gives \(P_a\), by comparing the two
coordinates.  The same structural parity oracle works for every \(\mu\), because
\(q(\mu)\) is input independent.

## 3. Fully lazy lookup

### Theorem 1 (lazy coherent lookup cost)

Any quantum circuit that implements one endpoint central lookup for an arbitrary
block index, using only calls to \(O_b\) and input-independent gates, needs
\(\Omega(L)\) raw oracle queries in the worst case.  The statement holds both for an
exact coherent oracle and for a lookup whose decoded endpoint sign is correct with
probability at least \(2/3\).  It remains true if the block index may be in
superposition.

#### Proof

Fix the block-index register to a particular value \(a\), and fix every input bit
outside block \(a\).  Reading the returned central pair computes the parity of the
remaining \(L\) input bits.  Bounded-error quantum query complexity of parity is
\(\Omega(L)\), and exact parity requires \(\lceil L/2\rceil\) queries.  A coherent
implementation valid on superpositions must in particular work on this fixed basis
state, so superposition over blocks cannot reduce the lower bound. \(\square\)

The bound is tight up to constants.  Run the standard exact quantum parity algorithm
with the block index carried as a spectator, then reversibly combine \(P_a\) with the
classically known value \(q(\mu)\).  This evaluates every block coherently using
\(O(L)\) raw queries, not \(O(KL)\).

This upper bound is why a classical direct-sum argument cannot be applied to one
coherent block-encoding call: quantum superposition lets the same \(L\)-query circuit
handle every block index.

## 4. Reusable preprocessing

Call an input-dependent resource \(D_b\) an *exact reusable endpoint oracle* if,
after it is constructed, a fixed processor can invoke it at every block
\(a\in[K]\), with no further calls to \(O_b\), and obtain the exact central endpoint
value.  It is enough that the promised resource survive or otherwise support \(K\)
successive invocations; no assumption that it is a classical table is needed.

### Theorem 2 (reusable-oracle preprocessing cost)

Constructing an exact reusable endpoint oracle requires at least

\[
 P\ge \lceil KL/2\rceil                                      \tag{9}
\]

queries to \(O_b\).  The same \(\Omega(KL)\) conclusion holds for a bounded-error
resource if its \(K\) successive answers are jointly correct with constant
probability.

#### Proof

After preprocessing, invoke the resource on \(a=1,\ldots,K\), and decode
\(P_1,\ldots,P_K\).  Their product is

\[
 \prod_{a=1}^K P_a=(-1)^{\oplus_{a=1}^K\oplus_{i=1}^L b_{a,i}}, \tag{10}
\]

the parity of all \(KL\) raw input bits.  Thus the preprocessing algorithm, followed
only by input-free invocations of its resource, computes parity on \(KL\) bits.
Exact quantum parity needs \(\lceil KL/2\rceil\) queries.  The bounded-error
polynomial-method lower bound is also \(\Omega(KL)\), provided the joint service
guarantee lets the final product be recovered with constant success probability.
\(\square\)

This proof allows an arbitrary quantum program state, entanglement, or implicit
formula in \(D_b\).  It does not assume that QRAM cells are individually
materialized.  Reusability is the operative condition: the resource must answer all
\(K\) endpoint queries without returning to the raw input.

A classical or quantum preprocessing algorithm can match the asymptotic bound by
computing and storing the \(K\) endpoint parities once.  Changing \(\mu\) then costs
only the evaluation of (4) and simple reversible arithmetic.

## 5. An explicit trajectory service lower bound

Fix any path parameters \(\mu_1,\ldots,\mu_K>0\); they may in particular be a
strictly decreasing path-following schedule.  Consider a service that, at stage
\(a\), must return the classical endpoint central pair of block \(a\) at \(\mu_a\).
Preprocessing, persistent memory, lazy raw queries, and adaptive computation are all
allowed.

### Theorem 3 (total cost for distinct explicit cells)

If all \(K\) returned pairs have coordinate error below \(1/2\) with joint constant
success probability, the total number of raw input queries across preprocessing and
all stages is

\[
 \Omega(KL).                                                   \tag{11}
\]

Consequently the amortized cost over these \(K\) stages is \(\Omega(L)\).

#### Proof

Each returned pair reveals \(P_a\), independently of \(\mu_a\).  After the final
stage, multiply the decoded signs to obtain the parity of all \(KL\) raw bits.  The
bounded-error quantum parity lower bound gives (11). \(\square\)

The schedule is a fixed workload on one fixed sparse LP, not a sequence of changing
LP inputs.  Nevertheless, it is an explicit-coordinate service problem.  Standard
QIPM correctness does not require an algorithm to reveal a different chosen endpoint
at every iteration.  In particular, a QLSA may only prepare a normalized global
state, and a block encoding may use the structural oracle coherently without ever
classically returning the \(K\) signs.  Theorem 3 must not be advertised as an
unconditional QIPM iteration lower bound.

## 6. Why a generic per-iteration refresh lower bound fails

The factorization (6) exhibits the main obstacle to standard dynamic-data-structure
reductions.

1. **A fixed LP contains no fresh per-iteration information.**  Once its \(KL\)
   hidden bits have been processed, later central points cannot reveal more than the
   same finite input.  With unrestricted persistent memory, an \(\Omega(KL)\)
   preprocessing cost can be amortized over arbitrarily many IPM iterations.
2. **The path parameter can be low dimensional.**  Here every numerical update is
   generated by one scalar \(q(\mu)\).  A lazy oracle stores the structural parities
   once and performs \(O(1)\) extra arithmetic when \(\mu\) changes.  The fact that
   all \(2K(L+1)\) coordinates change does not imply that they require that many
   writes.
3. **Cell-probe lower bounds need a query contract.**  Dynamic predecessor, range
   counting, and related reductions assume adversarial update/query sequences.  An
   IPM follows an analytic trajectory chosen by its algorithm, not an adversarial
   coordinate workload.  Theorem 3 becomes applicable only after explicitly
   requiring the distinct coordinate answers.
4. **Coherent lookup defeats a naive block direct sum.**  A single lazy oracle circuit
   can compute the parity of the selected block in superposition in \(O(L)\) queries.
   One cannot multiply that cost by \(K\) unless the output contract forces recovery
   of \(K\) independent classical answers or the oracle is invoked in a way for which
   a suitable direct-product theorem applies.
5. **Normalized-state output is weaker than a data structure.**  A QLSA state need
   not support reusable random access to every coordinate.  Treating it as if it did
   silently adds tomography or QRAM construction to the model.

Therefore a true per-IPM-iteration dynamic lower bound needs at least one additional
ingredient: a persistent-memory cap, a mandatory explicit-coordinate monitoring
contract, a proof that the QIPM makes many independent oracle invocations that cannot
share coherent work, or a fixed LP whose successive Newton operators have a proven
online-hardness property beyond a low-dimensional analytic parameterization.  No
such ingredient follows from sparsity or diagonal-weight change alone.

## 7. Literature and novelty

The parity query lower bound is classical quantum-query theory, following the
polynomial method of Beals et al.,
[*Quantum Lower Bounds by Polynomials*](https://arxiv.org/abs/quant-ph/9802049).
The exact \(\lceil n/2\rceil\) parity complexity is also standard.  General quantum
direct-sum theorems are known; the proofs above avoid needing their full machinery by
reducing the recovered block parities to one parity of all raw bits.

Quantum cell-probe lower bounds are an established subject; see Sen and Venkatesh,
[*Lower Bounds in the Quantum Cell Probe Model*](https://arxiv.org/abs/quant-ph/0104100).
Those results study static predecessor and membership under particular storage and
probe models.  They do not directly give a lower bound for the analytic sequence of
IPM weights.

Targeted searches found no earlier QIPM formulation of the reusable-versus-lazy
parity-oracle boundary above.  The lower-bound technique is not new.  The useful
contribution is the exact fixed sparse LP trajectory showing both sides:
condition-one Newton geometry and analytic lazy updates, but a linear raw-input cost
for a reusable exact central oracle or for a trajectory contract that explicitly
extracts all independent endpoint cells.

## 8. Assessment

Theorems 1--3 are rigorous and may support an oracle-accounting section.  The most
important finding is also negative: they do not justify an \(\Omega(N)\) refresh cost
at every QIPM iteration.  Any such claim that merely counts changed weights is
defeated by lazy evaluation and preprocessing reuse on a fixed trajectory.
