# Dynamic PSD fiber-scale maintenance has a direct-sum barrier

Status: Independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the compile-and-commit query theorem; deliberately limited QIPM scope

## Result

The [static implicit-recentering
theorem](2026-09-04-implicit-psd-fiber-recentering-access.md) has a genuine
dynamic direct sum, but only for a precise persistent-output contract.

Let \(b,T\geq1\) and \(s\geq2\) be integers. Let \(b\) source balls have
width \(s\), and let \(T\) online epochs apply fresh update batches. A
**compile-and-commit scale maintainer** must, after
epoch \(t\) and before the next epoch, produce either

1. all \(b\) scales as a classical record, or
2. a reusable complete unitary for their fixed-point values that makes no
   later call to the raw oracle for update batch \(t\). Here reusable means
   that an invocation and its inverse restore any backing workspace, so
   computational-basis values can be copied out without consuming the
   compiled object.

Require simultaneous relative error \(\delta<1/3\) and joint success at
least \(2/3\) over all epochs and sources. Even when every source update is
zero or one-sparse, any such maintainer uses

\[
       \Omega(Tb\sqrt s)\quad\text{quantum raw-update queries},
       \qquad
       \Omega(Tbs)\quad\text{randomized raw-update queries}.       \tag{1}
\]

There is also a margin-sensitive version. If \(k\mid s\),
\(1\leq k\leq s/2\), each nonzero update zeros a hidden block of \(k\)
replicated coordinates, and the smaller slack is \(\rho=k/s\), the tight
laws become

\[
       \Omega(Tb\sqrt{s/k})=\Omega(Tb\rho^{-1/2}),
       \qquad
       \Omega(Tb\,s/k)=\Omega(Tb\rho^{-1}).               \tag{1a}
\]

The one-sparse theorem (1) is the case \(k=1\).

More generally, suppose the scale service at epoch \(t\) must support
\(r_t\) arbitrary adaptive invocations before it may be discarded. On the
same promise family, the exact raw-query tradeoff is

\[
 \begin{aligned}
 Q&=\Theta\!\left(\sqrt s\sum_{t=1}^T\min\{r_t,b\}\right),\\
 R&=\Theta\!\left(s\sum_{t=1}^T\min\{r_t,b\}\right).
 \end{aligned}                                             \tag{1c}
\]

For the replicated-block family, replace \(\sqrt s\) and \(s\) by
\(\sqrt{s/k}=\rho^{-1/2}\) and \(s/k=\rho^{-1}\). Thus one online
evaluation has no \(b\) factor, whereas a reusable service with
\(r_t\geq b\) reaches the compile-and-commit law (1).

The quantum bound holds even in the stronger model that reveals every
epoch oracle at the start and permits queries in superposition over epoch,
source, and coordinate. Hence persistent quantum workspace and adaptive
cross-epoch scheduling do not remove it. Separate Grover searches match
the quantum order on the promise family.

This is not a bound for one online coherent scale evaluation. If the raw
update oracle remains callable, source-controlled Grover implements one
superposed evaluation over all \(b\) sources in \(O(\sqrt s)\) raw queries.
Nor is (1) automatically an end-to-end lower bound for a QIPM on one fixed
optimization instance: the hard updates below are fresh adversarial sparse
directions, not proved to be the Newton trajectory of one fixed conic
program. The theorem instead identifies the exact dynamic-access assumption
needed to treat a maintained scale oracle as free.

The lower bound is for hidden-support coordinate access. If an update is
instead delivered as an explicit sparse list, the exact identity
\[
 \rho_a(x+u)=\rho_a(x)-2x_a^Tu_a-\|u_a\|^2              \tag{1b}
\]
maintains the scale in work linear in the listed support. In particular,
explicit one-sparse updates cost \(O(b)\) arithmetic per epoch. Sparsity
alone is therefore not the hard resource; locating an unmaterialized
support is.

## 1. Online sparse-update family

For each source, use the public interior base point

\[
       \bar x={1\over\sqrt s}(0,1,\ldots,1),
       \qquad
       \bar\rho=1-\|\bar x\|^2={1\over s}.                 \tag{2}
\]

For every epoch--source pair \(q=(t,a)\), independently promise either

\[
 \begin{array}{ll}
 \mathcal P_0:&u_q=0,\\
 \mathcal P_j:&u_q=-e_j/\sqrt s\quad\text{for one }j\in\{2,\ldots,s\}.
 \end{array}                                                \tag{3}
\]

The update is zero or one-sparse. At epoch \(t\), apply the \(b\) updates
to independent source blocks, request the maintained scales, and then undo
them before epoch \(t+1\). Thus every queried point is strictly interior
and every epoch starts from the same public base point. The post-update
scale is

\[
       \rho_q=1-\|\bar x+u_q\|^2
       =\begin{cases}
          1/s,&\mathcal P_0,\\
          2/s,&\mathcal P_j.
        \end{cases}                                        \tag{4}
\]

For a column-packed PSD lift with \(h\) columns per source, the unique
fiber-centered diagonal is \(d_q=\rho_q/h\). Relative approximation of
\(d_q\) and of \(\rho_q\) are therefore equivalent. Since

\[
       {1+\delta\over s}<{2(1-\delta)\over s}
       \qquad(\delta<1/3),                                 \tag{5}
\]

the two valid output intervals are disjoint. Every correct scale record
reveals whether the corresponding search instance in (3) is marked.

The reset is only a device for making the updates sequential on the same
\(b\) source balls. It does not give the algorithm extra information: the
inverse update has the same raw oracle, and the scale must already have
been committed. Giving permanent access to all update oracles can only
make the task easier and is allowed in the lower-bound proof below.

For (1a), let \(k\mid s\) with \(1\leq k\leq s/2\), partition the
coordinates into \(s/k\) blocks of size \(k\), and let the public base
vanish on one whole block and equal \(1/\sqrt{s}\) elsewhere. A hidden
update is zero or \(-1/\sqrt{s}\) on every coordinate of one candidate
block. The two
slacks are \(k/s\) and \(2k/s\). A coordinate query is just a query to the
candidate-block mark bit, and there are \(N=s/k-1\) candidates. Replacing
the \((s-1)\)-leaf star below by an \(N\)-leaf star proves (1a); using one
fixed representative coordinate from each candidate block as the exact
Grover search domain gives the matching upper bound. The update is
\(k\)-sparse, while (1) retains the advertised one-sparse promise.

Under explicit sparse-list access, (1b) gives the complementary upper
bound \(O(\sum_a|\operatorname{supp}u_{t,a}|)\) arithmetic per epoch,
assuming queried coordinates of the current \(x\) are available. This
does not contradict (1): the hidden marked index in (3) has become part of
the input record rather than something the algorithm must discover.

## 2. Quantum direct-sum proof

Put \(m=Tb\) and index the \(m\) independent promise inputs by
\(q=(t,a)\). For one input, use labels
\(\{\varnothing\}\cup\{\{j\}:2\leq j\leq s\}\), where
\(\varnothing\) denotes no update and \(\{j\}\) the marked coordinate.
Let \(\Gamma_1\) be the adjacency matrix of the star centered at
\(\varnothing\). Then

\[
                  \|\Gamma_1\|=\sqrt{s-1},                \tag{6}
\]

and filtering by any one coordinate query leaves operator norm at most
one.

For the vector-valued \(m\)-fold promise-OR problem use the Kronecker sum

\[
 \Gamma_m=\sum_{q=1}^{m}
    I^{\otimes(q-1)}\otimes\Gamma_1\otimes I^{\otimes(m-q)}. \tag{7}
\]

All summands commute and have a common top tensor eigenvector, so

\[
                         \|\Gamma_m\|=m\sqrt{s-1}.         \tag{8}
\]

The matrix vanishes between inputs with the same full \(m\)-bit output.
Filtering by a queried triple \((t,a,j)\) kills all summands in (7) except
the one for \(q=(t,a)\), and the surviving filtered star has norm one.
The negative-weight adversary theorem therefore gives

\[
                  Q_{2/3}(\operatorname{PromiseOR}_{s-1}^{\otimes m})
                     =\Omega(m\sqrt{s-1})
                     =\Omega(Tb\sqrt s).                  \tag{9}
\]

An online maintainer is a special case of this simultaneous-oracle model:
simulate it while making all raw oracles available from the start and
record its committed outputs. Classical scale records directly give the
full presence/absence vector. For a committed quantum value oracle, query
the reusable unitary on every source label after each compile stage, copy
each fixed-point value in the computational basis, and invoke the inverse.
By the reusability contract this restores the backing workspace, so the
online simulation can continue without disturbance and without further
raw-input queries for that epoch. Comparing the copied value with any
threshold strictly between the two relative-error intervals gives the
same vector. Thus (9) proves the quantum part of (1).

The proof covers arbitrary retained quantum workspace. Its essential
output assumption is reusability. A one-shot state or an evaluator that
continues to call the raw update oracle is not a committed scale oracle.

### 2.1 Exact invocation--compilation tradeoff

Define an \(r_t\)-use service to implement the scale-value unitary for any
adaptive downstream client making at most \(r_t\) invocations, with joint
error probability at most \(1/3\). For the lower bound, choose a valid
client that queries \(\min\{r_t,b\}\) distinct source labels in the
computational basis and records their values. By (5), its transcript gives
that many independent search bits. Applying the same Kronecker-sum
adversary across all selected epoch--source pairs gives

\[
       \Omega\!\left(\sqrt s
          \sum_{t=1}^T\min\{r_t,b\}\right)                \tag{9a}
\]

quantum raw queries. The classical product-distribution argument gives the
second line of (1c).

For the upper bound, either implement every invocation by an exact
source-controlled Grover search, or search all \(b\) sources once and keep
their classical scale bits in QROM. Choosing the first strategy when
\(r_t<b\) and the second when \(r_t\geq b\) proves the matching quantum
upper bound. Scanning coordinates gives the analogous randomized upper.
This is a universal-service theorem: a particular downstream algorithm
whose query states have extra structure may define an easier task and does
not inherit (1c) automatically.

## 3. Randomized direct sum and matching upper bound

For one block, take the hard distribution that chooses \({\cal P}_0\) with
probability \(1/2\) and otherwise chooses the marked coordinate uniformly.
Distinguishing the cases with constant bias needs \(\Omega(s)\) expected
coordinate queries. Under the product distribution on the \(m\) blocks,
global success at least \(2/3\) implies constant marginal success for every
output bit. Queries to other independent blocks are only internal
randomness for that marginal task. Summing the expected queries assigned
to the blocks gives \(\Omega(ms)=\Omega(Tbs)\); Yao's principle gives the
worst-case randomized lower bound.

Conversely, scan every coordinate of every update classically. Quantumly,
run Grover search independently on its \(s-1\) candidate coordinates.
This gives

\[
          O(Tbs)\quad\text{classical},
          \qquad
          O(Tb\sqrt s)\quad\text{quantum}                 \tag{10}
\]

queries and writes the exact scale records. On the zero-or-one-mark
promise, exact amplitude amplification designed for the one-mark case,
followed by verification, distinguishes the two cases in \(O(\sqrt s)\)
queries per block with zero error: on a zero-mark input verification
rejects the arbitrary candidate returned. Thus no union-bound amplification is
needed and (1) is tight on this promise.

## 4. What this says about QIPM access

The implicit fiber-centered reduced Hessian uses

\[
       (H_0)_a={2h\over\rho_a}I
            +{4h\over\rho_a^2}x_ax_a^T.                  \tag{11}
\]

Consequently a QIPM that, after each arbitrary sparse update batch,
materializes a persistent QROM table of every \(\rho_a\) falls exactly
under (1). Calling that table in later Newton block encodings is cheap only
because its compilation has already paid the direct-sum cost.

There are three distinct contracts:

1. **Persistent compile-and-commit.** All \(b\) scales survive raw-oracle
   revocation. Equation (1) applies per \(T\) fresh batches.
2. **Online raw-backed evaluation.** One unitary evaluation may query the
   active raw update oracle in superposition over \(a\). Controlled Grover
   costs \(O(\sqrt s)\), not \(O(b\sqrt s)\), on (3); every later use pays
   again. For a universal \(r_t\)-use service, (1c) is the exact boundary
   between repeated evaluation and compilation.
3. **Correlated QIPM trajectory.** Scales can be updated through
   \(\rho_a(x+\alpha u)=\rho_a(x)-2\alpha x_a^Tu_a-
   \alpha^2\|u_a\|^2\), cached, or inferred from problem structure.
   Equation (1) applies only if the resulting access really satisfies the
   fresh compile-and-commit promise. No generic multiplication by the
   number of IPM iterations is justified.
4. **Explicit sparse-list update.** If every nonzero index and value is
   materialized, (1b) gives support-linear exact maintenance and the
   hidden-support search lower bound does not apply.

Thus the dynamic theorem closes a loophole in resource accounting rather
than proving a universal QIPM runtime lower bound. Any end-to-end speedup
claim using a maintained norm/scale oracle must state whether it pays the
compile-and-commit cost, retains a raw-backed evaluator and pays per use,
or exploits a proved correlation in the actual Newton path.

### Static-input noncomposition proposition

No factor \(T\) can be inferred by applying the one-snapshot search lower
bound separately to \(T\) rounds that query the same fixed problem oracle.
As a counterexample, let every round request the same scale bit
\(f(z)=\operatorname{OR}(z)\) from the same zero-or-one-mark input. Each
request considered in isolation has quantum query complexity
\(\Theta(\sqrt s)\), but an algorithm computes \(f(z)\) once, stores the
classical bit, and answers the entire \(T\)-round transcript with
\(O(\sqrt s)\) total queries.

More generally, an interleaved \(T\)-round algorithm for a fixed oracle is
just one query algorithm whose total query count is the sum of its actual
calls. Lower bounds for its individual subroutines do not compose unless
the required final transcript or output itself has a direct-product lower
bound. The fresh independent batches in Sections 1--3 provide exactly that
hypothesis. To turn (1) into a lower bound for one static conic program, one
would still have to embed \(T\) independent search outputs into its actual
Newton trajectory and prove that the QIPM output contract recovers all of
them. This note does not assume that missing theorem.

### Exact fixed-path caching corollary

The uncoupled linear product-ball path gives a positive static-input
example where no dynamic norm update is needed. For the marginal barrier
\[
             \bar F(x)=-h\sum_{a=1}^b\log(1-\|x_a\|^2)
\]
and objective \(\sum_a c_a^Tx_a\), stationarity at central multiplier
\(\eta\) is
\[
       {2h\over\rho_a}x_a+\eta c_a=0,
       \qquad \rho_a=1-\|x_a\|^2.                         \tag{12}
\]
Writing \(q_a=\|c_a\|\) and \(\tau_a=\eta q_a/h\), direct solution gives
\[
 \rho_a(\eta)={2\over1+\sqrt{1+\tau_a^2}},
 \qquad
 x_a(\eta)=-{\eta\rho_a(\eta)\over2h}c_a,               \tag{13}
\]
with the same formula at \(q_a=0\). Every centered PSD diagonal label
\(\gamma\) owned by source \(a\) is therefore
\(d_\gamma(\eta)=\rho_a(\eta)/h\), and the source block's
radial-to-tangential Hessian
condition is
\[
                    {2\over\rho_a(\eta)}-1
                       =\sqrt{1+\tau_a^2}.                \tag{14}
\]

Consequently, a reversible oracle for the fixed objective-block norms
\(q_a\), together with public \(h\) and \(\eta\), compiles any requested
central-path scale using one norm-oracle query plus charged reversible
scalar arithmetic. If the objective is explicit, all \(q_a\) can instead
be computed once in \(O(bs)\) arithmetic and reused at every path
parameter. Missing norm metadata may still have the static search cost,
but it is a one-time cost rather than a factor per central-path step.

This corollary is exact only for the uncoupled product-ball central path.
Additional affine constraints, inexact neighborhood iterates, or a generic
primal--dual SDP path destroy (12) and return to the access alternatives
above. Indeed, the closed form also makes this particular optimization
family directly solvable; it is an access-accounting witness, not a new
QIPM speedup.

## 5. Scope and novelty boundary

The construction is an access-layer dynamic lower bound for the explicit
column-packed Schur lift of product balls. It uses feasible projected
updates and the exact fiber-center map, but it does not realize the update
sequence as central or Newton iterates of one fixed conic optimization
instance. It gives no iteration lower bound and no lower bound for an
arbitrary quantum state output.

The proof is a direct application of the general adversary method to a
vector-valued search task; see Belovs,
[*Variations on Quantum Adversary*](https://arxiv.org/abs/1504.06943),
for the tight negative-weight framework and its extensions to general
input oracles and unitary implementation. The exact promise-search upper
uses the known-success-probability construction of Brassard, Hoyer, Mosca,
and Tapp,
[*Quantum Amplitude Amplification and
Estimation*](https://arxiv.org/abs/quant-ph/0005055). The new point here is
the compile-and-commit interpretation for dynamic PSD fiber recentering. A
targeted local and open-literature screen did not locate this exact access
theorem, but priority is not guaranteed without specialist review.
