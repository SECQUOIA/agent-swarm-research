# Quantum winner search for the global-trace holonomy SDP

## Status and algorithmic classification

For a batch of \(G\) parity-holonomy SDP components coupled by one global trace
constraint, the exact optimum is the minimum component value.  Since each component has
one of two values separated by \(1/10\), the problem is
\(\mathrm{OR}_G\circ\mathrm{PARITY}_N\).  A clean coherent parity phase oracle costs
\(N\) raw sign queries, and quantum search uses \(O(\sqrt G)\) such calls.  The resulting
upper bound is
\[
O\!\left(N\sqrt G\log(1/\delta)\right) \tag{1}
\]
raw queries for failure probability \(\delta\), or \(O(N\sqrt G)\) at constant failure.
It returns the exact promised optimal value and a compact exact reduced/root optimizer description;
preparing the selected component in all original product-cone coordinates adds only
\(O(N)\) raw queries.

This is not a faster quantum interior-point iteration.  It is a quantum active-face or
crossover module that exploits separability plus a single resource constraint.  It can
select a winning component before a component QIPM is run, but the speedup comes from
Grover search, not from solving the Newton equations faster.

## 1. Winner-take-all lemma

Let \(\mathcal K_g\) be convex cones, let \(f_g\) and \(\ell_g\) be linear, and assume
\(\ell_g(X)\ge0\) on \(\mathcal K_g\).  Also assume either that
\(\ell_g(X)=0\) forces \(X=0\), or, more generally, that
\(f_g(X)\ge0\) on \(\mathcal K_g\cap\ker\ell_g\).  Define the normalized component value
\[
v_g=\inf\{f_g(X):X\in\mathcal K_g,\ \ell_g(X)=1\}. \tag{2}
\]
Consider
\[
\inf\left\{\sum_{g=1}^G f_g(X_g):
X_g\in\mathcal K_g,\ \sum_{g=1}^G\ell_g(X_g)=1\right\}. \tag{3}
\]
If every \(v_g\) is attained, then the value of (3) is
\[
\min_g v_g. \tag{4}
\]
Indeed, put \(t_g=\ell_g(X_g)\).  For \(t_g>0\), homogeneity gives
\(f_g(X_g)\ge t_gv_g\); the additional assumption gives the same inequality when
\(t_g=0\).  Hence the objective is at least
\(\sum_gt_gv_g\ge\min_gv_g\).  Equality is obtained by placing all trace mass on an
optimizer of a minimizing component and setting the other components to zero.

This elementary lemma is the source of the winner-take-all behavior.  It applies to
block-separable conic programs with one homogeneous resource constraint and is not
specific to interior-point methods.

## 2. The global-trace parity SDP

Component \(g\) contains \(P=33N\) blocks \(X_{g,i}\in S_+^3\) linked by the sparse
signed congruence path
\[
X_{g,i}=D_{\sigma_{g,j}}X_{g,i-1}D_{\sigma_{g,j}}^T,
\qquad D_\sigma=\operatorname{diag}(\sigma,1,1), \tag{5}
\]
on its \(N\) hidden edges, with the public identity plateaus and public costs from the
intrinsic signed-triangle construction.  Let
\[
h_g=\prod_{j=1}^N\sigma_{g,j}. \tag{6}
\]
After eliminating the path, normalized component \(g\) has root variable
\(Z_g\succeq0\), \(\operatorname{tr}Z_g=1\), and effective cost
\[
\overline C_{h_g}=3I+\frac1{10}
(H_{12}+H_{23}+h_gH_{13}). \tag{7}
\]
Its value and one public choice of optimizer are
\[
\begin{array}{c|c|c}
h_g&v_{h_g}&Z_{h_g}^*\\ \hline
+1&29/10&\frac12(I-r_+r_+^T),\quad r_+=(1,1,1)^T/\sqrt3,\\
-1&14/5&r_-r_-^T,\quad r_-=(1,-1,1)^T/\sqrt3.
\end{array} \tag{8}
\]

Replace the \(G\) separate trace constraints by the one public row
\[
\sum_{g=1}^G\operatorname{tr}X_{g,0}=1. \tag{9}
\]
The objective retains the within-component \(1/P\) averaging but has no \(1/G\)
average:
\[
\frac1P\sum_{g=1}^G\sum_{i=0}^{P-1}\langle C_{g,i},X_{g,i}\rangle. \tag{10}
\]
Applying (4) gives
\[
V=\begin{cases}
14/5,&\exists g:h_g=-1,\\
29/10,&\forall g:h_g=+1.
\end{cases} \tag{11}
\]
Thus additive error below \(1/20\) is exactly the decision problem “does some component
have negative parity?”  The scalar row and column incidence inside every component
remains constant; the one global trace row has \(3G\) nonzeros.  If constant scalar row
degree is required, introduce a binary summation tree whose \(3G\) leaves are the root
diagonal entries.  For every internal node add a free scalar accumulator \(t_v\)
and the public row
\[
t_v-t_{v_L}-t_{v_R}=0, \tag{11a}
\]
where a leaf symbol denotes its corresponding diagonal entry, and fix the top variable
to one.  These variables are uniquely determined and, on the PSD feasible set, equal
nonnegative partial traces.  Each new
row has at most three entries; every new scalar column occurs in at most two rows; and a
root diagonal column occurs in its first copy row and one summation row.  This extended
formulation projects exactly to (9), adds only \(O(G)\) public size, and does not change
(11) or any input-query count.  No separate \(\mathbb R_+\) constraint or scalar
log barrier is imposed on these free variables; adding one would change the Newton
geometry in the main theorem note.

## 3. Clean coherent parity marking

Use the standard bit-XOR sign oracle
\[
O_\sigma:\ |g,j,b\rangle\longmapsto
|g,j,b\mathbin\oplus z_{g,j}\rangle,
\qquad \sigma_{g,j}=(-1)^{z_{g,j}}. \tag{12}
\]
One call is simulated by one query to a canonical hidden coefficient on edge \((g,j)\)
of (5), and conversely the coefficient query used by the algorithm below is simulated by
one call to (12).  Public address arithmetic maps \((g,j)\) to that coefficient.

Here is the exact access statement used in the lower bound.  Work in the
fixed-position isometric-svec oracle: the position maps, coefficient
magnitudes, costs, and right-hand sides are public, and the value oracle
XORs the sign bit of the requested nonzero into a target bit.  Every hidden
slot is one of the two coefficients \(\pm\sigma_{g,j}\) in the \(12\) and
\(13\) copy rows of edge \((g,j)\).  A public reversible map sends a queried
row or column slot to \((g,j)\), or to a dummy address whose bit is zero.
One call to (12) then implements the coefficient-value query directly on
its sign target; no second query is needed to uncompute a stored answer.
The same construction works coherently in superposition and for inverse or
externally controlled calls.  Conversely, querying one fixed hidden copy
slot returns \(z_{g,j}\), so one coefficient query implements one call to
(12).  Thus the two query models have **exactly unit normalization** on the
hidden input.  The direct global trace row, or every row of the bounded-degree
cumulative formulation in the structural companion note, is public and
does not change this accounting.  Other value-loading conventions can cost
a factor two, as noted below, but do not change the theorem.

Prepare the answer qubit in \(|-\rangle=(|0\rangle-|1\rangle)/\sqrt2\).  For
\(j=1,\ldots,N\), query (12) with the same component register \(|g\rangle\) and the
public fixed edge index \(j\).  Phase kickback gives
\[
|g\rangle|-\rangle
\longmapsto
\left(\prod_{j=1}^N(-1)^{z_{g,j}}\right)|g\rangle|-\rangle
=h_g|g\rangle|-\rangle. \tag{13}
\]
The edge-index register is reset after each public address computation, and the answer
qubit remains exactly \(|-\rangle\).  Discarding this unchanged product factor, (13)
implements the clean phase oracle
\[
O_h|g\rangle=h_g|g\rangle. \tag{14}
\]
It marks precisely the winning components \(h_g=-1\), uses exactly \(N\) raw sign
queries, and leaves no parity or prefix garbage.  The construction works with \(g\) in
superposition.

If the available coefficient oracle loads a value into a zero register rather than
XORing a bit, compute--phase--uncompute uses at most \(2N\) coefficient-oracle calls.
This changes only the constant in (1).  Similarly, an exact \(N/2\)-query parity
*decision* circuit does not by itself give an \(N/2\)-query clean marking oracle:
amplitude amplification must uncompute its workspace, restoring an \(O(N)\) marking
cost.  The direct phase product (13) is the simplest clean implementation.

## 4. Search, verification, and value output

Apply any standard bounded-error quantum OR/search algorithm to (14).  With no promise
on the number of marked components, it uses
\[
O(\sqrt G\log(1/\delta)) \tag{15}
\]
marking-oracle calls to return either a marked index \(g_*\) or `NONE`, with failure at
most \(\delta\).  At constant \(\delta\), the logarithm is absent.  If an index is
returned, evaluate its parity once into a classical bit using \(N\) further raw queries;
this exactly verifies the candidate and is absorbed by (1).

Return
\[
\widehat V=\begin{cases}
14/5,&g_*\text{ was verified},\\
29/10,&\text{the search returned `NONE`}.
\end{cases} \tag{16}
\]
On the success event this is the exact optimum, not merely a constant-additive
estimate.  Therefore:

> **Theorem 1 (quantum global-trace value upper bound).**  From raw coherent sparse
> coefficient access, the global-trace SDP (9)--(10) can be solved to any fixed additive
> error smaller than \(1/20\), with constant success probability, using
> \(O(N\sqrt G)\) raw queries.  Failure probability \(\delta\) costs
> \(O(N\sqrt G\log(1/\delta))\) queries.

With straightforward reversible addressing, one parity marker uses
\(O(N\log(GP))\) elementary gates and
\(O(\log G+\log P)\) work qubits.  The total gate bound is therefore
\[
O\!\left(N\sqrt G\log(GP)\log(1/\delta)
+\operatorname{polylog}(G/\delta)\right), \tag{17}
\]
apart from the implementation cost of one raw coefficient query.  No QRAM or table of
the \(G N\) parities is assumed.

## 5. Finding and solving a winning component

The search produces more than the scalar value.  If it finds \(g_*\), an exact compact
optimizer of the eliminated root formulation is
\[
Z_{g_*}=Z_-^*,\qquad Z_g=0\quad(g\ne g_*). \tag{18}
\]
If there is no winner, choose the public component \(g_*=1\), set
\(Z_{g_*}=Z_+^*\), and set the others to zero.  Equations (8) and (18), together with
the classical label \(g_*\), are an \(O(\log G)\)-bit plus constant-matrix exact
root-optimizer description.  They are not by themselves a classical listing of the
input-dependent copied blocks in (20).  A purification of the selected root density matrix can be
prepared with a constant-size public circuit once the branch in (8) is known.

For an optimizer in the original copied coordinates, let
\[
R_{g_*,i}=D_{\tau_{g_*,i}},
\qquad
\tau_{g_*,i}=\prod_{j\le L(i)}\sigma_{g_*,j}. \tag{19}
\]
Then
\[
X_{g_*,i}=R_{g_*,i}Z_{h_{g_*}}^*R_{g_*,i}^T,
\qquad X_{g,i}=0\quad(g\ne g_*). \tag{20}
\]
After measuring the classical winning label, the prefix signs for just this component
can be streamed in \(N\) raw queries and \(O(N)\) classical work.  This yields all
nonzero blocks explicitly.  Alternatively, a uniform original-coordinate block-density
state
\[
\rho_{g_*}^{\mathrm{phys}}={1\over P}
\bigoplus_{i=0}^{P-1}R_{g_*,i}Z_{h_{g_*}}^*R_{g_*,i}^T \tag{21}
\]
can be prepared coherently with \(O(N)\) additional raw queries,
\(O(N\log P)\) reversible gates, and \(O(\log P)\) workspace by the standard threshold
prefix circuit.  The address \(g_*\) is now classical, so this stage does not touch any
other component.  Its cost is dominated by search for \(G\ge2\).

> **Theorem 2 (winner plus optimizer).**  The same
> \(O(N\sqrt G\log(1/\delta))\) query bound returns, with failure at most \(\delta\),
> a winning component and either a compact exact root optimizer or the physical optimizer
> state (21).  Explicitly listing the selected component's \(P=33N\) blocks costs the
> unavoidable additional \(\Theta(P)\) output work but no additional asymptotic query
> factor.

The theorem deliberately does not promise a dense classical list of all \(GP\) blocks.
All unselected blocks are zero and are represented by the compact label (18).

## 6. Matching lower bound: an explicit adversary

The required composition lower bound has a short direct proof, including on
the promise of either no winner or exactly one winner.  Let
\(E,O\subseteq\{0,1\}^N\) be the even- and odd-parity strings.  Define the
\(|E|\times|O|\) matrix
\[
 B_{xy}=\mathbf 1[|x-y|_1=1].                              \tag{22}
\]
It is the even-to-odd bipartite half of the \(N\)-cube.  Every row and
column has sum \(N\), and the uniform vectors attain this singular value,
so
\[
                              \|B\|=N.                     \tag{23}
\]
If \(\Delta_j(x,y)=\mathbf1[x_j\ne y_j]\), then
\(B\circ\Delta_j\) is the permutation matrix \(x\mapsto x\oplus e_j\).
Consequently
\[
                         \|B\circ\Delta_j\|=1.             \tag{24}
\]

Now restrict the block input to
\[
 \mathcal D_0=E^G,
 \qquad
 \mathcal D_1=\bigsqcup_{a=1}^G
 E^{a-1}\times O\times E^{G-a}.                            \tag{25}
\]
These are respectively all-even inputs and inputs with exactly one odd
block.  For the sector in which block \(a\) is odd, put
\[
 C_a=I_E^{\otimes(a-1)}\otimes B\otimes
       I_E^{\otimes(G-a)},
 \qquad C=[C_1\ C_2\ \cdots\ C_G],                         \tag{26}
\]
and use the symmetric adversary matrix
\[
                         \Gamma=\begin{pmatrix}0&C\\C^T&0\end{pmatrix}
\tag{27}
\]
indexed by \(\mathcal D_0\sqcup\mathcal D_1\).  Since the odd sectors are
disjoint,
\[
 CC^T=\sum_{a=1}^G
 I_E^{\otimes(a-1)}\otimes BB^T\otimes
 I_E^{\otimes(G-a)}.                                      \tag{28}
\]
The summands commute, each has norm \(N^2\), and their common uniform
tensor vector has eigenvalue \(N^2\) for every summand.  Therefore
\[
                         \|\Gamma\|=\|C\|=N\sqrt G.         \tag{29}
\]

Filter \(\Gamma\) by a query to raw bit \((a,j)\).  In every odd sector
other than \(a\), block \(a\) is connected through an identity factor, so
the filter annihilates that sector.  In sector \(a\), it replaces \(B\) by
the perfect matching \(B\circ\Delta_j\).  Equations (24) and (26) give
\[
                 \|\Gamma\circ\Delta_{a,j}\|=1             \tag{30}
\]
for every raw input position.  Thus the positive-weight adversary ratio is
exactly \(N\sqrt G\).  The standard adversary theorem implies
\[
 Q_{1/3}(\mathcal D_0\text{ versus }\mathcal D_1)
                         =\Omega(N\sqrt G).                 \tag{31}
\]
The upper bound from Sections 3--4 works without the one-winner promise, so
together these equations prove
\[
 Q_{1/3}(\mathrm{OR}_G\circ\mathrm{PARITY}_N)
                         =\Theta(N\sqrt G).                 \tag{32}
\]

On \(\mathcal D_0\), the SDP value is \(29/10\); on \(\mathcal D_1\), it
is \(14/5\).  For every fixed \(\epsilon<1/20\), the two correct-output
intervals are disjoint and thresholding at \(57/20\) decides (25) without
another query.  The unit-normalization simulation in Section 3 therefore
transfers (31) with no hidden oracle factor:

> **Theorem 3 (sharp winner-take-all query complexity).**  In the canonical
> fixed-position coefficient model, estimating the optimum of (9)--(10) to
> additive error \(\epsilon<1/20\), with failure probability at most
> \(1/3\), requires \(\Omega(N\sqrt G)\) coefficient queries, already under
> the all-even versus exactly-one-odd promise.  Theorem 1 gives the matching
> \(O(N\sqrt G)\) upper bound.  At the endpoint \(\epsilon=1/20\) under a
> non-strict error contract, the public midpoint \(57/20\) is a valid
> zero-query answer, so the accuracy threshold is sharp.

The same lower bound applies to any output from which the existence of a
winner can be recovered with constant bias, including the verified winning
label.

A randomized classical algorithm needs \(\Theta(GN)\) raw queries in the worst case,
already under the promise that either every block has even parity or exactly one block
has odd parity.  Here is a direct proof that allows arbitrary adaptive interleaving among
the blocks.  Let \(\mathcal D_0\) make the \(G\) blocks independent and uniform
conditional on even parity.  To obtain \(\mathcal D_1\), choose \(J\) uniformly from
\([G]\), independently of everything else, make block \(J\) uniform conditional on odd
parity, and keep every other block uniform conditional on even parity.

Couple an execution under the two distributions as follows.  In each block, give the
same independent fair answers to its first \(N-1\) distinct queried positions; on the
last unseen position, return the unique bit that realizes the required parity.  Repeated
queries return the stored answer.  This is exactly the appropriate conditional-uniform
distribution even under adaptive querying.  The two executions have identical
transcripts until the algorithm completes all \(N\) positions of block \(J\).

On the \(\mathcal D_0\) execution path of a \(q\)-query algorithm, let \(S\) be the set
of completed blocks.  Then \(|S|\le\lfloor q/N\rfloor\), while \(J\) is independent and
uniform.  The coupling therefore gives the explicit transcript bound
\[
 \operatorname{TV}\!\left(\mathsf{Tr}_{\mathcal D_0},
                           \mathsf{Tr}_{\mathcal D_1}\right)
 \le {\mathbb E|S|\over G}
 \le {\lfloor q/N\rfloor\over G}
 \le {q\over GN}.                                      \tag{32a}
\]
The same argument couples the internal seed of a randomized algorithm.  If the
algorithm is correct with probability at least \(2/3\) on every promised input, its
probability of answering that an odd block exists is at most \(1/3\) under
\(\mathcal D_0\) and at least \(2/3\) under \(\mathcal D_1\).  Hence the left side of
(32a) is at least \(1/3\), so \(q\ge GN/3\).  Reading all \(GN\) signs gives the
matching deterministic upper bound.  The unrestricted-OR problem inherits the same
lower bound by restriction to these zero- and one-winner inputs.

Thus the quantum speedup is a quadratic improvement in the number of components,
\(G\), while both algorithms retain linear dependence on the within-component path
length \(N\).

### 6.1 Exact-query scope and promise edge cases

The promise in (25) admits an exact algorithm with the same asymptotic query
cost as (32).  Run exact amplitude amplification configured for one marked
component.  If there is one, it returns that component with certainty; if
there is none, it may return an arbitrary candidate.  Evaluate the returned
component parity exactly and accept only if it is odd.  The verification takes
\(\lceil N/2\rceil\) raw queries and is absorbed by the
\(O(N\sqrt G)\) search cost.  Since exact algorithms are also bounded-error
algorithms, (31) gives

\[
 Q_E\bigl(\operatorname{OR}^{0,1}_G
       \circ\operatorname{PARITY}_N\bigr)
 =\Theta(N\sqrt G).
\tag{33}
\]

The implementation is still the clean, QRAM-free marker (13): it uses
exactly \(N\) raw queries per Grover call, and the entire exact search uses
\(O(N\sqrt G\log(GP))\) elementary routing gates and
\(O(\log G+\log P)\) work qubits, apart from its public one-qubit rotations.
For completeness, let \(\theta_0=\arcsin(1/\sqrt G)\), choose
\[
 m=\left\lceil {\pi\over4\theta_0}-{1\over2}\right\rceil,
 \qquad \theta_m={\pi\over4m+2},
 \qquad \gamma=G\sin^2\theta_m\le1,
\]
and append a public flag with amplitude \(\sqrt\gamma\) on \(|1\rangle\).
When there is one winner, declaring ``good'' to mean winner-and-flag-one
makes the initial good probability \(\sin^2\theta_m\).  Exactly \(m\)
ordinary Grover iterations then rotate it to probability one.  The good
reflection is (13) controlled by the flag and still costs exactly \(N\) raw
queries; the reflection about the initial state is public.  Thus exact
amplitude amplification needs no parity table.  Arbitrary public rotations
are free in the standard exact-query model, while finite-gate-set synthesis
adds the usual precision-dependent overhead.  The query-optimal
\(\lceil N/2\rceil\)-query parity *decision* algorithm cannot simply replace
this marker, because amplitude amplification needs a coherent phase oracle
with its work uncomputed.

If the promise says there is **exactly** one winner, the scalar decision is
constant and needs no query.  For \(G\ge2\), finding the winning label remains
\(\Theta(N\sqrt G)\), for bounded or exact algorithms: exact search is the
upper bound, and general-adversary composition with the unique-search
relation gives the lower bound.  For \(G=1\), the only possible winning label
is public and label recovery needs no query.

Without the promise (25), bounded error still costs \(\Theta(N\sqrt G)\),
but exact decision has the larger order

\[
 Q_E\bigl(\operatorname{OR}_G\circ\operatorname{PARITY}_N\bigr)
 =\Theta(NG).
\tag{34}
\]

Indeed, in sign variables \(\chi_g=\prod_j\sigma_{g,j}\), the unique
multilinear polynomial for the Boolean output is

\[
 1-2^{-G}\prod_{g=1}^G(1+\chi_g).
\]

Its top monomial has degree \(NG\), so the polynomial method gives an exact
query lower bound \(NG/2\).  Computing every component parity exactly uses
\(G\lceil N/2\rceil=O(NG)\) queries.  This unrestricted exact bound is a
scope clarification, not the winner-search headline.

The edge cases agree with these decision formulas.  For \(G=1\), the
zero-or-one decision task is parity and exact computation takes
\(\lceil N/2\rceil\) queries.  For \(N=1\), it
is ordinary OR: bounded error takes \(\Theta(\sqrt G)\), unrestricted exact
decision takes \(\Theta(G)\), and promised zero-or-one exact decision takes
\(\Theta(\sqrt G)\).  If \(N=0\) or \(G=0\), the function is public and no
query is needed.

## 7. Why this is a crossover/search module, not a new QIPM

At any positive log-barrier parameter, a strictly feasible central point assigns
positive trace to every component.  The winner-take-all face (18) appears only at the
optimization boundary.  Grover search bypasses this central trajectory by using the
promise that every normalized component has one of two analytically known values.
Nothing in the construction accelerates a generic SDP Newton solve.

The honest reusable algorithmic statement is the following.  For a block-separable
conic problem of form (3), suppose a coherent threshold test for component value costs
\(T_{\mathrm{check}}\), and solving one selected normalized component costs
\(T_{\mathrm{solve}}\).  Quantum minimum finding or threshold search gives the hybrid
bound
\[
\widetilde O(\sqrt G\,T_{\mathrm{check}})
+T_{\mathrm{solve}}+T_{\mathrm{recover}}, \tag{35}
\]
where \(T_{\mathrm{recover}}\) is charged according to the requested output.  In the
parity family,
\[
T_{\mathrm{check}}=\Theta(N),\qquad
T_{\mathrm{solve}}=O(1),\qquad
T_{\mathrm{recover}}=O(N), \tag{36}
\]
which gives Theorems 1--2.

If the component threshold test itself is implemented by a QIPM, then (35) is reasonably
called a **search-then-QIPM** or **quantum crossover** architecture.  It should not be
called a QIPM variation unless one also proves convergence and cost bounds for the
component solver.  For the present promise family, the local eigensolutions (8) are
explicit, so invoking an IPM at all would add machinery without changing the result.

## 8. Access-model caveats

1. A supplied oracle for \(h_g\) would reduce the search to \(O(\sqrt G)\) calls, but
   building that oracle from raw edge coefficients costs \(\Theta(GN)\) classical
   preprocessing or the on-demand \(\Theta(N)\) coherent work in (13).
2. A QRAM table containing all component parities has already paid the hard setup cost.
3. Parallel query ports may reduce depth, but not the \(\Theta(N\sqrt G)\) total-query
   bound.
4. The high-degree public trace row in (9) is not queried for hidden information.  A
   sparse public summation tree removes it if the chosen matrix-access model charges
   row degree.
5. The compact optimizer output is essential for the claimed end-to-end speedup.
   Materializing \(G\) dense component arrays would cost at least their output size even
   though all but one are zero.
6. Query preprocessing is not free.  If setup uses \(S\) raw queries and subsequent
   adaptive calls use \(q_t\), any procedure producing the value or a verified winner
   obeys \(S+\sum_tq_t=\Omega(N\sqrt G)\).  The raw-coefficient theorem does not
   cover an arbitrary input-dependent block-encoding completion supplied at unit cost;
   its construction, as well as any prefix, parity, nullspace, or eliminated-cost
   table, must be charged to setup.

## 9. Literature positioning

The quantum search step is standard amplitude amplification, and the matching lower
bound is the standard adversary composition for OR with parity.  The signed-triangle
component is documented separately in
`2026-09-02-intrinsic-spectrum-trace-normalized-s3-parity.md`.

Primary references for these algorithmic ingredients are:

* M. Boyer, G. Brassard, P. Høyer, and A. Tapp, *Tight bounds on quantum
  searching*, arXiv:quant-ph/9605034, including search with an unknown number of marked
  items.
* C. Dürr and P. Høyer, *A Quantum Algorithm for Finding the Minimum*,
  arXiv:quant-ph/9607014, for the more general minimum-finding formulation in (23).
* P. Høyer, T. Lee, and R. Špalek, *Tight adversary bounds for composite
  functions*, arXiv:quant-ph/0509067, for adversary composition.
* R. Beals, H. Buhrman, R. Cleve, M. Mosca, and R. de Wolf, *Quantum lower bounds by
  polynomials*, arXiv:quant-ph/9802049, for the parity query bound.

The potentially useful observation is the exact conic decomposition (4) together with
the end-to-end access and recovery accounting in Theorems 1--2.  A targeted literature
comparison is still needed before claiming novelty for the broader search-then-conic-
solver template.  The present note makes no claim that Grover search or winner-take-all
resource allocation is itself new.
