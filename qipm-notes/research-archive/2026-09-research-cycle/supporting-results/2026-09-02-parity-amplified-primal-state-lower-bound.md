# Parity-amplified primal-state lower bound for sparse QIPMs

Date: 2026-09-02

## Result

This note strengthens the existing parity-complete feasible-start construction in
`hamiltonian-qipm-sparse-obstructions.md`.  A bounded-degree copy tree amplifies the
endpoint parity into a constant fraction of the coordinates.  Consequently, the
lower bound applies even when the requested optimization output is only one
amplitude-encoded quantum state, rather than a classical vector, a value oracle, or
the scalar optimal value.  A bounded local slack extension strengthens this further:
the amplitude state of every exactly feasible point is hard, so no small
objective-gap assumption is needed.

Let hidden signs

\[
 \sigma_1,\ldots,\sigma_N\in\{-1,+1\},
 \qquad
 p_0=1,\quad p_i=\prod_{h=1}^i\sigma_h.
\]

Every node below is represented by a nonnegative pair \((u_j,v_j)\) and its
difference \(d_j=u_j-v_j\).  There are two stages of nodes.

1. There are chain nodes \(0,\ldots,N\), with constraints
   \[
      d_0=1,\qquad d_i-\sigma_i d_{i-1}=0\quad(1\le i\le N).
   \tag{1}
   \]
2. Root a complete binary copy tree at chain node \(N\).  Every new tree node
   \(j\), with parent \(\pi(j)\), has the constraint
   \[
      d_j-d_{\pi(j)}=0.
   \tag{2}
   \]
   Choose the number of leaves to be
   \[
      M=2^{\lceil\log_2(8(N+1))\rceil}.
   \]
   Thus the number of new copy nodes is \(K=2M-2=\Theta(N)\).

Let \(P=N+1+K\) be the total number of pairs.  Consider the standard-form LP

\[
  \min_{x\ge0}\ \mathbf 1^Tx
  \quad\text{subject to (1)--(2)}.
\tag{3}
\]

The oracle model is coherent fixed-position sparse access to \(A,b,c\).  The
support pattern is known.  A row query, column query, or sparse-value query exposes
at most one hidden sign, so it is simulable with \(O(1)\) standard sign-oracle
queries.  The same conclusion holds for a whole sparse row or whole sparse column.

### Theorem 1 (near-optimal primal-state output is parity-hard)

The family (3) has the following properties.

1. It has \(2P=\Theta(N)\) variables and \(P=\Theta(N)\) equalities.  Every
   coefficient belongs to \(\{-1,0,1\}\), each row has at most four nonzeros, and
   each column has at most three nonzeros.  The support pattern, right-hand side,
   and objective are input-independent.
2. It is strictly primal-dual feasible and has a unique nondegenerate strictly
   complementary optimum.  Its reduced logarithmic-barrier Hessian in an explicit,
   input-independent orthonormal null basis has spectral condition number one at
   every point of the central path.
3. Suppose a quantum query algorithm has final output density operator \(\rho\),
   with no additional unheralded failure event, and there exists an exactly feasible
   \(x\ge0\) satisfying
   \[
       \mathbf1^Tx-\operatorname{OPT}\le1
   \tag{4}
   \]
   and
   \[
       D_{\rm tr}\!\left(\rho,
          |x/\lVert x\rVert_2\rangle\langle x/\lVert x\rVert_2|
       \right)\le\frac1{10}.
   \tag{5}
   \]
   Then the algorithm makes \(\Omega(N)\) coefficient-oracle queries.
4. The same \(\Omega(N)\) lower bound holds when the final output density operator
   is within trace distance \(1/10\) of the normalized exact primal central point at
   the fixed barrier parameter \(\mu=3/4\).

The output in item 3 is only one amplitude-encoded state.  No coordinate-query
oracle, tomography, or classical vector is requested.

## Proof

### Sparsity and rank

Equation (1) has row sparsity two for \(d_0=1\) and four for every chain
transition.  Equation (2) has row sparsity four.  A chain pair occurs in at most
its incoming and outgoing chain equations, except node \(N\), which occurs in its
incoming equation and two copy-child equations.  A copy pair occurs in its parent
equation and at most two child equations.  Hence column sparsity is at most three.

In the difference variables, (1)--(2) are triangular when the chain and then the
tree are ordered away from their roots.  They fix

\[
    d_i=p_i\quad(0\le i\le N),
    \qquad d_j=p_N\quad(j\text{ a copy node}).
\tag{6}
\]

Thus the equality matrix has full row rank.  Its null space has the explicit
orthonormal basis

\[
   V_j=\frac{e_{u_j}+e_{v_j}}{\sqrt2},\qquad j\in[P],
\tag{7}
\]

which is independent of the hidden signs.

### Oracle simulation audit

Use the standard coherent sign oracle

\[
 O_\sigma:|i,z\rangle\longmapsto|i,z\oplus\operatorname{enc}(\sigma_i)\rangle.
\]

The locations of all nonzeros are fixed.  A chain-transition row contains only
the hidden value \(-\sigma_i\); every other value in that row is fixed.  A column
of a chain pair contains at most the one hidden value from its outgoing
transition.  Tree rows, bounding rows, \(b\), and \(c\) are input-independent.
Therefore a coherent sparse-position, sparse-value, whole-row, or whole-column
query is implemented reversibly with at most one call to \(O_\sigma\), including
when the row or column index is in superposition.  Uncomputation uses at most one
inverse call.  The added variables and equations in Theorem 2 introduce no new
hidden values, so the same simulation applies unchanged.

This audit is for the stated coefficient-access model.  A separately granted
global state-preparation oracle for all of \(A\), an input-dependent feasible
offset, or preprocessing advice is a stronger interface and is not simulated by
this argument.

### Optimum, strict feasibility, and central conditioning

Write \(q_j=u_j+v_j\).  Feasibility is equivalent to

\[
 u_j=\frac{q_j+d_j}{2},\qquad
 v_j=\frac{q_j-d_j}{2},\qquad q_j\ge1.
\tag{8}
\]

The objective is \(\sum_jq_j\).  Hence \(\operatorname{OPT}=P\), and the unique
optimum has every \(q_j=1\).  Taking every \(q_j=2\) gives strict primal
feasibility.  Taking equality multiplier \(y=0\) and slack \(s=\mathbf1\) gives
strict dual feasibility.

At the optimum, the positive coordinate of each pair has dual slack zero and the
zero coordinate can be assigned dual slack two.  The resulting vector
\(c-s\) is a linear combination of the pair differences.  Full row rank and (7)
therefore imply an equality multiplier.  The \(P\) columns belonging to the
positive coordinates differ, up to column signs, from the triangular full-rank
matrix on the difference variables.  They form a nonsingular basis, and all of
its basic variables equal one, proving primal nondegeneracy.  Complementarity
forces zero slack on these columns at every dual optimum, so the basis equations
uniquely determine the equality multiplier.  The remaining slacks equal two.
Thus the dual optimum is unique, dual nondegenerate, and strictly complementary.

On the feasible affine space, the primal logarithmic-barrier objective is a sum of
identical scalar functions,

\[
  \Phi_\mu(q)=\sum_{j=1}^P
  \left[q_j-\mu\log\frac{q_j^2-1}{4}\right].
\tag{9}
\]

Every central coordinate is

\[
  q(\mu)=\mu+\sqrt{\mu^2+1},
\tag{10}
\]

and the reduced Hessian in basis (7) is a positive scalar multiple of the identity:

\[
 V^T H_x V
 =2\mu\left[(q(\mu)+1)^{-2}+(q(\mu)-1)^{-2}\right]I.
\tag{11}
\]

Its condition number is exactly one for every \(\mu>0\).

### Decoding parity from any near-optimal primal state

For any feasible \(x\), let \(\delta_j=q_j-1\ge0\).  Condition (4) is exactly
\(\sum_j\delta_j\le1\), so every \(q_j\le2\).  The squared norm contributed by
pair \(j\) is

\[
 w_j=u_j^2+v_j^2=\frac{q_j^2+1}{2}.
\tag{12}
\]

Since \(q_j^2-1\le3(q_j-1)\) on \([1,2]\),

\[
 W:=\lVert x\rVert_2^2=\sum_jw_j\le P+\frac32.
\tag{13}
\]

Assume \(N\ge2\), which is immaterial for the asymptotic lower bound.  Every
copy pair has difference \(p_N\).  If a computational-basis measurement
lands on a copy pair, call its coordinate *correct* when it is the plus coordinate
for \(p_N=+1\) and the minus coordinate for \(p_N=-1\).  Within each copy pair,

\[
 \frac{\text{correct squared mass}}{w_j}
 =\frac{(q_j+1)^2}{2(q_j^2+1)}\ge\frac9{10}.
\tag{14}
\]

The total copy-pair squared mass is at least \(K\).  Our choice of \(M\) gives
\(K\ge16(N+1)-2\), while \(P=N+1+K\).  Therefore

\[
 \beta:=\Pr[\text{measurement lands on a copy pair}]
 \ge \frac{K}{P+3/2}>\frac9{10}.
\tag{15}
\]

Use the following fixed decoder: on a copy coordinate output the sign encoded by
plus versus minus; on any chain coordinate output a fair random bit.  Its success
probability on the ideal state is at least

\[
  \frac12+\frac25\beta>\frac{43}{50}.
\tag{16}
\]

Trace distance changes every measurement success probability by at most the trace
distance.  Under (5), the same decoder succeeds with probability greater than
\(19/25>2/3\).  Composing it with the alleged state-preparation algorithm computes
\(p_N\), the parity of the \(N\) hidden signs.  Bounded-error quantum parity has
query complexity \(\Omega(N)\).  Since every LP query is simulated with \(O(1)\)
sign queries, item 3 follows.

This treats \(\rho\) as the algorithm's unconditional final density operator, as is
standard for a state-generation query problem.  A general CPTP implementation may
contain arbitrary discarded work and classical randomness; \(\rho\) is simply its
reduced output state.  If an implementation instead has a heralded failure flag,
condition (5) is imposed on the success branch and the success probability must be
a fixed constant.  A fixed constant number of repetitions, using the first
successful branch and guessing randomly if all fail, gives bounded overall error
with only a constant-factor worst-case query overhead.

There is also a limited unheralded extension.  Suppose a classical internal event
of probability at least \(2/3\) has a conditional output satisfying (5), while the
remaining branch is arbitrary and the event is not revealed.  The fixed decoder's
unconditional success is at least

\[
 \frac23\frac{19}{25}=\frac{38}{75}>\frac12.
\]

Repeating the entire algorithm and taking a majority therefore computes parity with
bounded error using only a constant-factor query overhead.  Merely saying that an
unheralded mixed state is ``good with probability \(2/3\)'' without specifying such
a physical ensemble is not an invariant density-operator contract and is not used.

### Exact central state

At \(\mu=3/4\), equation (10) gives \(q=2\).  Every pair is therefore
\((3/2,1/2)\) or its swap.  All pairs have equal squared norm, a copy pair is
measured with probability \(K/P>9/10\), and the coordinate within a copy pair has
the correct sign with probability \(9/10\).  The same decoder and trace-distance
argument prove item 4.

## Bounded-pair strengthening: arbitrary feasible-state output is hard

The absolute gap in Theorem 1 prevents a small number of large \(q_j\)'s from
dominating the amplitude normalization.  A local upper bound removes the need for
that gap assumption without sacrificing constant sparsity or the condition-one
reduced geometry.

For every pair, add a nonnegative variable \(t_j\) and the input-independent
equality

\[
   2u_j+2v_j+2t_j=3,
\tag{17}
\]

and give \(t_j\) objective coefficient zero.  Keep (1)--(2) and minimize
\(\sum_j(u_j+v_j)\).  Call the resulting LP \(\overline{\mathrm{LP}}_\sigma\).

### Theorem 2 (constant-relative-gap and feasibility-state lower bound)

The LP \(\overline{\mathrm{LP}}_\sigma\) has \(3P=\Theta(N)\) variables and
\(2P=\Theta(N)\) equalities.  Matrix and objective coefficients have magnitude at
most two, the right-hand side has magnitude at most three, and maximum row and
column sparsity are four.  It is strictly primal-dual
feasible and has a unique nondegenerate strictly complementary optimum.  In an
explicit input-independent orthonormal null basis, its reduced logarithmic-barrier
Hessian has condition number one at every point on the central path.

Let \(\rho\) be the unconditional final density operator of a quantum query
algorithm.  If there exists **any** exactly feasible point \(x\) of
\(\overline{\mathrm{LP}}_\sigma\) such that

\[
 D_{\rm tr}\!\left(\rho,
 |x/\lVert x\rVert_2\rangle\langle x/\lVert x\rVert_2|
 \right)\le\frac1{10},
\tag{18}
\]

then the algorithm makes \(\Omega(N)\) coefficient-oracle queries.  In particular,
this holds under every constant-relative objective-gap promise, and it holds for
the normalized exact primal central point at every fixed \(\mu>0\).

The same conclusion holds if exact feasibility is replaced by

\[
 x\geq0,
 \qquad
 \|\overline A x-\overline b\|_1\leq\frac1{50},
\tag{19}
\]

while retaining trace-distance error at most \(1/10\).

#### Proof

Feasibility now gives, for each pair,

\[
  1\le q_j=u_j+v_j\le\frac32,
  \qquad
  t_j=\frac32-q_j.
\tag{20}
\]

Choosing \(q_j=5/4\) makes \(u_j,v_j,t_j\) strictly positive.  For strict dual
feasibility, set every difference-equation multiplier to zero and every multiplier
of (17) to \(-1/4\).  Under the convention \(A^Ty+s=c\), this gives
\(s_{u_j}=s_{v_j}=3/2\) and \(s_{t_j}=1/2\).

The unique optimum again has \(q_j=1\), now with \(t_j=1/2\).  Per pair, exactly
the sign-selected member of \((u_j,v_j)\) and \(t_j\) are positive.  These \(2P\)
positive columns form a nonsingular basis: the \(t\)-columns give a diagonal block
on (17), and eliminating that block leaves, up to column signs, the triangular
difference matrix from (1)--(2).  In particular, the full \(2P\)-row equality
matrix has rank \(2P\).  At the optimum set the dual slack of each positive variable
to zero and the slack of the zero member of each \((u_j,v_j)\) pair to two.
As in Theorem 1, \(c-s\) is in the difference-row space.  This proves
strict complementarity.  All \(2P\) basic variables are positive.  Moreover,
complementarity forces zero slack on their columns at every dual optimum, and
the nonsingular basis then uniquely fixes the equality multiplier; every
remaining slack is two.  Hence the primal and dual optima are nondegenerate and
the dual optimum is unique.

The null space has one local direction per pair,

\[
  \overline V_j
  =\frac{e_{u_j}+e_{v_j}-2e_{t_j}}{\sqrt6}.
\tag{21}
\]

These vectors are orthonormal and input-independent.  On the feasible affine
space, the barrier is

\[
 \overline\Phi_\mu(q)=\sum_j\left[
 q_j-\mu\log\frac{q_j^2-1}{4}
     -\mu\log\left(\frac32-q_j\right)
 \right].
\tag{22}
\]

Every central coordinate is the same scalar \(q(\mu)\in(1,3/2)\).  Therefore
the sign only swaps the two pair entries, and a direct calculation gives

\[
 \overline V^TH_x\overline V
 =\frac{2\mu}{3}\left[
   (q(\mu)+1)^{-2}+(q(\mu)-1)^{-2}
   +(3/2-q(\mu))^{-2}
 \right]I.
\tag{21a}
\]

It is a positive scalar multiple of the identity and has condition number one.

It remains to decode parity.  The squared norm of one full triple is

\[
 \overline w(q)
 =u^2+v^2+t^2
 =\frac{q^2+1}{2}+\left(\frac32-q\right)^2.
\tag{23}
\]

For \(q\in[1,3/2]\),

\[
  \frac54\le\overline w(q)\le\frac{13}{8}.
\tag{24}
\]

The copy triples therefore carry a fraction

\[
 \overline\beta
 \ge
 \frac{(5/4)K}{(5/4)K+(13/8)(N+1)}
 =\frac{10K}{10K+13(N+1)}
 >\frac9{10}
\tag{25}
\]

of the total squared mass.  On a copy triple, measure in the computational basis;
the plus/minus coordinate encodes \(p_N\), while on the \(t\)-coordinate output a
fair random bit.  The success probability conditional on that triple is

\[
 \frac12+\frac{u^2-v^2}{2\overline w(q)}
 =\frac12+\frac{q}{2\overline w(q)}
 \ge\frac9{10}.
\tag{26}
\]

On a chain triple output a fair random bit.  The ideal-state success probability is
at least

\[
 \frac12+\frac25\overline\beta>\frac{43}{50}.
\tag{27}
\]

Trace error \(1/10\) leaves success greater than \(19/25>2/3\).  The parity lower
bound proves the theorem.  Notice that no objective-gap inequality entered the
decoder; (17) alone prevents normalization from hiding the copied sign. \(\square\)

#### Robustness to small \(\ell_1\) feasibility residual

It remains to justify the approximate-feasibility extension (19).  Put

\[
 \varepsilon=\frac1{50},
 \qquad d_*=1-\varepsilon=\frac{49}{50},
 \qquad C=\frac32+\frac\varepsilon2=\frac{151}{100}.
\]

Write the residual of each difference equation as \(r_j\).  Multiplying the
chain equations by the corresponding prefix signs makes them telescope.  The
same is true down every copy-tree path.  Since the sum of the absolute residuals
of *all* equations is at most \(\varepsilon\), every copy node obeys

\[
 p_Nd_j\ge d_*.
\tag{28}
\]

For a bounding equation write
\(h_j=2(q_j+t_j)-3\).  Nonnegativity and \(|h_j|\le\varepsilon\) give

\[
 q_j\ge|d_j|\ge d_*,
 \qquad q_j+t_j\le C.
\tag{29}
\]

Consequently every copy triple has squared norm at least \(d_*^2\), while every
triple has squared norm at most \((q_j+t_j)^2\le C^2\).  With
\(L=N+1\), \(N\ge2\), and \(K/L\ge46/3\), the copy mass fraction satisfies

\[
 \beta_\varepsilon
 \ge\frac{Kd_*^2}{Kd_*^2+LC^2}
 >\frac{43}{50}.
\tag{30}
\]

For a copy triple let \(d'=p_Nd_j\).  Its signed decoder observable has
conditional expectation

\[
 \frac{p_N(u_j^2-v_j^2)}{u_j^2+v_j^2+t_j^2}
 =\frac{d'q_j}{(q_j^2+d'^2)/2+t_j^2}.
\]

Using \(d'\ge d_*\), \(d'\le q_j\le C\), and
\(t_j\le C-q_j\), its reciprocal is at most

\[
 \frac{C}{2d_*}+\frac12+\frac{(C-d_*)^2}{d_*^2}
 =\frac{7505}{4802}<\frac{100}{63}.
\tag{31}
\]

Thus the ideal approximate-feasible amplitude state has signed decoder
expectation greater than

\[
 \frac{43}{50}\frac{63}{100}=\frac{2709}{5000}.
\tag{32}
\]

For the norm-one diagonal decoder observable, trace distance \(1/10\) changes
its expectation by at most \(1/5\).  The output expectation therefore retains
the correct sign with magnitude greater than

\[
 \frac{2709}{5000}-\frac15
 =\frac{1709}{5000}>\frac13.
\]

The associated randomized binary decoder succeeds with probability greater
than \(2/3\), proving (19).

The linear exponent is tight in the coefficient-query model: query all \(N\)
hidden signs, compute their prefixes classically, and prepare any chosen feasible
point or central point from its explicit coordinate formula.  The theorem therefore
identifies an exact \(\Theta(N)\) input-query boundary for this output contract.

## Weaker output contracts

The trace-distance state guarantee is stronger than the proof needs.  Define the
fixed, input-independent, norm-one diagonal observable

\[
 O_{\rm copy}
 =\sum_{j\ {\rm copy}}
   \left(|u_j\rangle\!\langle u_j|-|v_j\rangle\!\langle v_j|\right),
\tag{33}
\]

with eigenvalue zero on every chain and \(t\) coordinate.  For every exactly
feasible bounded-pair point,

\[
 p_N\left\langle O_{\rm copy}\right\rangle
 =\frac{\sum_{j\ {\rm copy}}q_j}{\|x\|_2^2}
 >\frac9{10}\frac45=\frac{18}{25}.
\tag{34}
\]

For every point satisfying (19), the proof of (32) gives instead

\[
 p_N\left\langle O_{\rm copy}\right\rangle
 >\frac{2709}{5000}>\frac12.
\tag{35}
\]

Consequently, even a classical estimate of this one selected expectation value
to additive error \(1/2\), with bounded success probability, determines the sign
of the parity and needs \(\Omega(N)\) coefficient queries.  Producing a quantum
state is unnecessary for this weaker-output corollary.  This does not say that
*every* observable is hard; the objective value, for example, is known.

The state theorem also has an immediate fidelity formulation.  For a pure target,

\[
 \langle x/\|x\||\rho|x/\|x\|\rangle\ge\frac{99}{100}
\tag{36}
\]

implies trace distance at most \(1/10\).  Thus Theorems 1--2 hold under squared
fidelity at least \(99/100\), or root fidelity at least \(\sqrt{99/100}\), with
the convention stated explicitly.  The output \(\rho\) may be mixed.

### Why the one-path construction does not tolerate constant \(\ell_2\) error

The robust version of Theorem 2 uses a global \(\ell_1\) residual.  It implies an
\(\ell_2\)-residual version only at the dimension-dependent scale

\[
 \|\overline A x-\overline b\|_2
 \le\frac1{50\sqrt{2P}}.
\]

There is a concrete obstruction to the same decoder at constant \(\ell_2\)
error.  In sign-corrected chain coordinates set

\[
 p_i d_i=1-\frac{i}{N},
 \qquad 0\le i\le N,
\]

put every copy difference equal to \(d_N=0\), and take \(q_j=1,t_j=1/2\)
everywhere.  The bounding and copy equations are exact, nonnegativity holds, and
the \(N\) chain residuals all have magnitude \(1/N\).  Hence the total residual
has \(\ell_2\) norm \(1/\sqrt N\), but the amplified copy coordinates contain no
parity signal at all.  This does not by itself give an easy state-generation
algorithm, because the chain coordinates still contain hidden prefixes.  It does
prove that one-path copy-tree amplification and its fixed decoder cannot
establish a constant-\(\ell_2\)-residual theorem.  The parallel-path construction
in Theorem 3 below supplies the required robust gadget, at a quadratic cost in
dimension.

## What this does and does not establish

The theorem is end-to-end in the coefficient-query model: it lower-bounds the
production of the requested original-primal solution state, irrespective of QLSA,
preconditioning, scaling, or the route taken through an infeasible-start or
homogeneous self-dual embedding.  Those transformations cannot remove information
that is recoverable by a fixed measurement of the promised final state.

It is stronger than an output-length or tomography bound.  The output contains only
\(O(\log N)\) qubits, and one measurement already decodes parity with constant bias.
The optimum value is the known constant \(P\), so the hardness genuinely belongs to
the primal-output contract rather than value estimation.

The state here is the QLS-style amplitude encoding of the original primal vector.
It is not the same object as the coordinate-basis wavefunction used by the
Hamiltonian quantum central-path method of Augustino et al.  The theorem applies to
that method only if its output is additionally converted to the amplitude-encoded
contract in Theorem 1 or 2.

The condition-one statements concern the reduced primal-barrier Hessians in the
explicit null bases (7) and (20).  The original equality normal matrices contain the
chain and tree incidence geometry and are not uniformly conditioned.  Thus this is
not a theorem that every conventional KKT representation is well conditioned.  Supplying
a feasible offset containing all prefix products would trivialize the hard input
processing; constructing that advice is exactly what the parity reduction charges.

Theorem 1 uses exact feasibility.  The bounded-pair Theorem 2 now tolerates the
explicit global \(\ell_1\) residual \(1/50\), with the same trace-distance
constant.  The counterexample following (36) shows why this amplified decoder
does not extend to constant \(\ell_2\) residual.  The parallel-path construction
in Theorem 3 supplies such robustness at the price of quadratic LP dimension;
the separate degree-two connectivity construction remains another fallback.

## Referee verdict

**Verdict: correct in the stated fixed-pattern coefficient-query model after the
repairs above.**  The sparse-oracle simulation uses at most one hidden-sign query,
including coherent whole-row and whole-column access.  Both equality matrices have
full row rank; the displayed positive-column bases prove primal nondegeneracy and
uniqueness of the dual multipliers; and the reduced Hessian calculations are scalar
identities in the claimed input-independent orthonormal bases.  The decoder works
uniformly for every admissible feasible point and for arbitrary mixed CPTP output,
not only for the optimum or a pure algorithm output.

The audit strengthened the copy-mass constant from \(4/5\) to \(9/10\), made the
heralded and physically meaningful unheralded contracts explicit, added fidelity
and one-observable corollaries, and proved robustness to global \(\ell_1\)
feasibility residual \(1/50\).  It also found the exact limitation of the proposed
robustness: an \(O(N^{-1/2})\) \(\ell_2\) residual can erase the endpoint signal by
drifting gradually along the chain.  Therefore no constant-\(\ell_2\) claim should
be attached to this single-chain copy-tree decoder.  The parallel-path extension
below obtains constant relative \(\ell_2\) robustness by increasing the LP size to
\(\Theta(N^2)\).

The remaining qualifications are substantive but already explicit: the theorem
does not cover a stronger input-dependent feasible-offset or global matrix-state
oracle, does not assert conditioning of conventional KKT systems, and does not
apply directly to a coordinate-basis central-path wavefunction without conversion
to the amplitude-encoded primal contract.

## Collision and novelty audit

The parity query lower bound and prefix-product gadget are standard.  The earlier
local theorem already used the chain to lower-bound scalar value estimation,
classical feasible output, and preprocessing of a random-access central-point
oracle.  The apparent new ingredient here is an **LP-native bounded-degree
realization** of endpoint amplification that makes a single amplitude-encoded
original-primal state itself parity-hard without tomography or coordinate access.
Endpoint padding and amplification in QLS history states are established prior art,
as detailed below.

Targeted searches through 2026-09-02 found general quantum state-conversion
adversary bounds, quantum LP value lower bounds, QLS solution-state generation and
verification lower bounds, and QIPM tomography/output discussions.  None of those
results makes the theorem above a formal corollary.  No searched source stated a
sparse strictly feasible LP whose arbitrary feasible primal amplitude state and every
fixed-parameter central-path amplitude state both have linear quantum input-query
complexity while the reduced barrier Hessians have condition number one.  This is
evidence of apparent novelty, not proof of priority.

The calibrated claim is therefore about the **LP embedding and output interface**,
not a new generic state-generation lower-bound method.  Lee et al. characterize
input-dependent state conversion by a filtered adversary norm, and Ambainis et al.
give additive and multiplicative adversary methods for state generation.  The proof
here uses the simpler fact that one fixed measurement of every admissible output
state evaluates parity.  Even the linear exponent is already attained by
Apers--Gribling on square constant-sparse LPs, although for optimal-value output.
The novelty candidate is the conjunction of an original-primal **any-feasible-state**
contract, a fixed known optimum value, fixed support with bounded row and column
degree, exact central-state hardness, strict LP regularity, and an
input-independent reduced log-barrier Hessian that is a scalar identity.

Nor is endpoint amplification in a linear-system solution state new.  The HHL
computational-history construction pads the completed computation over a constant
fraction of its clock, and the 2026 QLS lower bound of Mori et al. places repeated
endpoint parity in the middle third of a sparse inverse state.  The binary tree above
is an LP-native, bounded-column-degree realization of that established amplification
principle; the principle itself should not be claimed as novel.

Primary comparators include:

- Apers and Gribling, *Quantum Speedups for Linear Programming via Interior Point
  Methods*, SIAM Journal on Computing (2026), Theorem 8.4.  Their hard LP computes
  a hidden Boolean function in the optimal value and gives an
  \(\Omega(\sqrt{nd}\,r)\) row-query bound for constant-additive value accuracy.
  Here the optimum value is known, and the hidden parity is instead recoverable from
  one measurement of the requested primal state;
- J. van Apeldoorn, A. Gilyen, S. Gribling, and R. de Wolf,
  [*Quantum SDP-solvers: Better upper and lower
  bounds*](https://arxiv.org/abs/1705.01843), Theorem 30 and Corollary 31.  Their
  coefficient-query LP family also hides a Boolean function in two possible integral
  optimum values.  It gives stronger dense square-instance exponents, but does not
  address a primal output state, a fixed known optimum, central points, bounded row
  and column degree, or reduced barrier conditioning;
- T. Lee, R. Mittal, B. Reichardt, R. Spalek, and M. Szegedy,
  [*Quantum query complexity of state
  conversion*](https://arxiv.org/abs/1011.3020), especially Theorem 4.9's general
  bounded-error characterization by filtered \(\gamma_2\).  This subsumes the
  general task of preparing input-dependent target states, but does not supply the
  sparse-LP construction or its condition-one geometry;
- A. Ambainis, L. Magnin, M. Roetteler, and J. Roland,
  [*Symmetry-assisted adversaries for quantum state
  generation*](https://arxiv.org/abs/1012.2112), for general state-generation
  adversary methods.  Again, it does not give the LP embedding;
- Kerenidis and Prakash, *A Quantum Interior Point Method for LPs and SDPs*,
  arXiv:1808.09266, for QIPM solution-state and tomography interfaces;
- Augustino et al., *A Quantum Central Path Algorithm for Linear Optimization*,
  arXiv:2311.03977, for a central-path state-based optimization model;
- Somma and Subasi, *Complexity of Quantum State Verification in the Quantum Linear
  Systems Problem*, arXiv:2007.15698, for a QLS solution-state verification lower
  bound.  Their Theorems 1 and 3 require, respectively,
  \(\Omega(\kappa/\|A^{-1}|b\rangle\|)\) calls to the right-hand-side preparation
  unitary or its square in copies of \(|b\rangle\), with constant probability.  This
  is verification of a supplied candidate under right-hand-side access, whereas
  Theorems 1--2 lower-bound generation from the LP coefficient oracle;
- D. Orsucci and V. Dunjko,
  [*On solving classes of positive-definite quantum linear systems with
  quadratically improved runtime in the condition
  number*](https://arxiv.org/abs/2101.11868), Propositions 6 and 17.  They prove
  \(\Omega(\min\{\kappa,N\})\) constant-error PD-QLS solution-state query lower
  bounds for right-hand-side preparation, normalized block-encoding, and
  constant-sparse matrix access.  This is the closest output-state lower bound, but
  it does **not** subsume the LP theorem: it is a supplied square invertible system
  with one inverse state, while the bounded-pair LP is an underdetermined affine
  feasibility problem and permits any feasible target.  Applying their result to the
  explicit reduced barrier Hessian gives only \(\Omega(1)\), since that Hessian has
  \(\kappa=1\).  A square feasibility or KKT representation can be ill-conditioned,
  but it is a different operator and generally requires a hidden-information-bearing
  feasible offset or right-hand side;
- A. Harrow, A. Hassidim, and S. Lloyd,
  [*Quantum algorithm for linear systems of
  equations*](https://arxiv.org/abs/0811.3171), Section III.  Their sparse QLS
  computational-history construction repeats the final computation throughout the
  middle third of a clock, so a measurement of one normalized solution state reveals
  the answer with constant probability.  This is direct prior art for endpoint
  padding, but its hard inverse system has condition number growing with the clock
  length and is not an LP central-path construction;
- Q. Wang and Z. Zhang,
  [*Tight Quantum Depth Lower Bound for Solving Systems of Linear
  Equations*](https://arxiv.org/abs/2407.06012), Theorem 2 and Corollary 2.  A
  2-sparse permutation-chain inverse state reveals the chain endpoint with constant
  probability, yielding \(\Omega(\kappa)\) query depth and total-query lower bounds.
  This is another close state-output precedent whose hardness is carried by the
  encoded QLS condition number;
- G. H. Low and Y. Su,
  [*Quantum linear system algorithm with optimal queries to initial state
  preparation*](https://arxiv.org/abs/2410.18178), Theorem 3, for a Grover-based
  lower bound in the inverse success amplitude of one supplied QLS instance.  It
  concerns right-hand-side preparation, not coefficient-query hardness at
  condition one;
- S. Mori et al.,
  [*Sparsity-dependent Complexity Lower Bound of Quantum Linear System
  Solvers*](https://arxiv.org/abs/2601.16697), Theorems 1--2.  Their Theorem 1 is
  especially close at proof level: a constant-sparse clocked inverse state contains
  prefix parities, a full block of repeated endpoint parity, and reverse prefixes, so
  a fixed measurement of one approximate output state computes parity.  It gives
  \(\Omega(\kappa\log(1/\epsilon))\) at constant sparsity and
  \(\Omega(\kappa\sqrt{s})\) at constant error.  These bounds become constant in
  the present reduced-Hessian regime \(\kappa=s=O(1)\), and their clocked square
  QLS construction is not an arbitrary-feasible-state LP construction;
- Beals et al., *Quantum Lower Bounds by Polynomials*,
  arXiv:quant-ph/9802049, for the parity query lower bound.

Status: **proof complete in the fixed-pattern coefficient-query model; apparently new
as an LP/output-interface embedding after the targeted search.  The underlying parity
and state-generation lower-bound methodology is not new.**

---

## Robust extension: parallel parity paths

The exact-feasibility qualification in Theorem 1 can be removed, at a quadratic
cost in LP dimension. One parity chain has resistance \(N\): in prefix-product
coordinates, a linear drift from \(+1\) to \(-1\) has residual norm
\(2/\sqrt N\). Copying its endpoint cannot repair this defect. Placing \(N\)
length-\(N\) chains in parallel gives constant effective conductance without
increasing row or column sparsity.

### Construction

Let \(N\) be a power of two and set \(R=N\), \(L=16N\). Form a rooted tree \(T\):

1. Start with a complete binary fanout tree with \(R\) leaves.
2. Append a path of length \(N\) to each leaf. Edge \(i\) on every path is labelled
   by the same hidden sign \(\sigma_i\).
3. At every path endpoint, attach a complete binary tree with \(L\) leaves. All
   remaining edges have label \(+1\).

Write \(r\) for the fanout root, \(V(T)\) for the vertices, and \(S\) for the \(RL\)
leaves in the endpoint trees. Then

\[
 P:=|V(T)|=(2R-1)+RN+R(2L-2)=33N^2-1,
 \qquad |S|=16N^2.                                      \tag{R1}
\]

For each vertex \(j\), introduce nonnegative variables

\[
 (u_j,v_j,h_j,t_j),\qquad d_j=u_j-v_j,\quad q_j=u_j+v_j.
\]

The equalities are

\[
\begin{aligned}
 d_r&=1,& d_k-a_{jk}d_j&=0 &&((j,k)\in E(T)),\\
 h_r&=1,& h_k-h_j&=0 &&((j,k)\in E(T)),\\
 q_j+t_j-2h_j&=0 &&(j\in V(T)),
\end{aligned}                                             \tag{R2}
\]

where \(a_{jk}=\sigma_i\) on the \(i\)-th edge of every long path and
\(a_{jk}=1\) otherwise. The standard-form LP is

\[
 \min_{x\ge0} c^Tx,\qquad
 c_{u_j}=c_{v_j}=2,\quad c_{h_j}=c_{t_j}=1,
 \quad\text{subject to (R2).}                              \tag{R3}
\]

### Theorem 3 (constant-relative-residual state output is parity-hard)

In the coherent fixed-position sparse coefficient-oracle model, (R3) has
\(4P=\Theta(N^2)\) variables and \(3P=\Theta(N^2)\) full-row-rank equalities.
Every coefficient belongs to \(\{-2,-1,0,1,2\}\), and every row and column has at
most four nonzeros. The support pattern, \(b\), and \(c\) are input-independent.

Suppose a quantum query algorithm outputs a density operator \(\rho\) for which
there is a nonzero \(x\ge0\) satisfying

\[
 \frac{\|Ax-b\|_2}{\|b\|_2}\le\frac1{200},                \tag{R4}
\]

and

\[
 D_{\rm tr}\!\left(\rho,
 |x/\|x\|_2\rangle\langle x/\|x\|_2|\right)\le\frac1{100}.
                                                               \tag{R5}
\]

Here \(\rho\) denotes the unconditional output state. Equivalently, the statement
may be applied to a heralded success branch of constant success probability, with
the constant repetitions needed to obtain that branch charged to the query count.

Then the algorithm makes \(\Omega(N)=\Omega(\sqrt P)\) coefficient-oracle
queries. The conclusion remains true if the output contract additionally requires

\[
 \left|c^Tx-\operatorname{OPT}\right|
 \le\frac1{10}\operatorname{OPT}.                         \tag{R6}
\]

In fact, the proof does not use (R6). Thus it applies to every nonnegative point
with the stated constant relative \(\ell_2\) feasibility residual, and a fortiori
when the contract also requires two-sided objective accuracy. The absolute value
in (R6) matters: for an infeasible point, the one-sided quantity
\(c^Tx-\operatorname{OPT}\) can be negative and is not an optimality gap. The
theorem also immediately lower-bounds preparation of the normalized exact primal
central point at every fixed \(\mu>0\), since that point has zero residual.

The LP is bounded and strictly primal-dual feasible, has a unique nondegenerate
strictly complementary optimum, and has condition-one reduced primal-barrier
Hessian in an explicit input-independent null basis at every point of its central
path.

### Proof

#### Rank, sparsity, and oracle simulation

In coordinates \((d,q,h,t)\), the first group of (R2) is a pinned tree incidence
system and is nonsingular on \(d\). The second group is the same system on \(h\).
After those blocks, every cap row has its own private \(t_j\) coefficient. Hence
all \(3P\) rows are independent.

A difference coordinate occurs in at most three tree-edge rows and one cap row.
The root occurs in two child rows, its anchor row, and its cap row. The same count
applies to \(h\), while \(t_j\) occurs only in its cap row. This proves the sparsity
bounds.

Only long-path coefficients depend on the input. A sparse position or row query
exposes at most one \(\sigma_i\), and a whole sparse column also exposes at most one
sign: a path vertex has a hidden coefficient only in its outgoing long-path row.
Thus every coherent LP-oracle query is simulated reversibly by one standard
sign-oracle query plus input-independent computation, also on a superposition of
the \(R\) repeated occurrences of a sign.

#### Feasible set, optimum, and central conditioning

Let \(\tau_r=1\) and propagate \(\tau_k=a_{jk}\tau_j\). Exact feasibility fixes
\(d_j=\tau_j\), \(h_j=1\), and \(\tau_j=p_N\) on \(S\). The local constraints give

\[
 u_j=\frac{q_j+\tau_j}{2},\qquad
 v_j=\frac{q_j-\tau_j}{2},\qquad
 t_j=2-q_j,\qquad 1\le q_j\le2.             \tag{R7}
\]

The feasible polytope is a product of \(P\) compact intervals. Taking \(q_j=3/2\)
is strictly primal feasible; \(y=0,s=c\) is strictly dual feasible. On the feasible
affine space,

\[
 c^Tx=\sum_j(2q_j+h_j+t_j)=\sum_j(q_j+3).    \tag{R8}
\]

Therefore \(\operatorname{OPT}=4P\), uniquely attained at \(q_j=1\). At the
optimum, the coordinate in each pair selected by \(\tau_j\), as well as \(h_j,t_j\),
is positive, and the opposite pair coordinate is zero. The positive columns form a
nonsingular basis after the triangular coordinate change above, proving primal
nondegeneracy.

Strict complementarity can be checked explicitly. Let \(B_a\) be the nonsingular
pinned labelled-incidence matrix in the \(d\) equations and \(B_1\) its unsigned
counterpart. Give the difference, reference, and cap rows dual multipliers
\(\alpha,\beta,\gamma\), chosen by

\[
 B_a^T\alpha=\tau,\qquad B_1^T\beta=3\mathbf1,\qquad
 \gamma=\mathbf1.
\]

Under the convention \(A^Ty+s=c\), these choices give

\[
\begin{aligned}
 s_u&=2\mathbf1-B_a^T\alpha-\gamma=\mathbf1-\tau,\\
 s_v&=2\mathbf1+B_a^T\alpha-\gamma=\mathbf1+\tau,\\
 s_h&=\mathbf1-B_1^T\beta+2\gamma=0,\qquad
 s_t=\mathbf1-\gamma=0.
\end{aligned}
\]

Thus the selected member of every \((u_j,v_j)\) pair, and every \(h_j,t_j\), has
zero slack, while the zero member of each pair has slack two. The dual multiplier
is unique because the positive primal columns form a basis, so the optimum is also
dual nondegenerate.

The null space has the input-independent orthonormal basis

\[
 W_j=\sqrt{\frac23}\left(\frac12e_{u_j}+\frac12e_{v_j}-e_{t_j}\right).
                                                               \tag{R9}
\]

At a primal central point every \(q_j\) is the same scalar \(q(\mu)\in(1,2)\),
because after eliminating the equalities each local barrier summand is

\[
 q-\mu\log\!\left(\frac{q^2-1}{4}(2-q)\right).              \tag{R10}
\]

Changing \(\tau_j\) only swaps \(u_j,v_j\). Hence the reduced Hessian of (R10),
including the normalization in (R9), is the same positive scalar at every node:
\(W^TH_xW=\lambda(\mu)I\), where

\[
 \lambda(\mu)=\frac{2\mu}{3}
 \left(\frac{2(q(\mu)^2+1)}{(q(\mu)^2-1)^2}
       +\frac1{(2-q(\mu))^2}\right)>0.                  \tag{R10a}
\]

Its condition number is one for every \(\mu>0\).

#### Stability lemma

Let \(D_a z=(z_k-a_{jk}z_j)_{(j,k)\in E(T)}\). For this tree, every
\(z\in\mathbb R^P\) obeys

\[
 \frac{\|\operatorname{Diag}(\tau)z-\mathbf1\|_2}{\sqrt P}
 \le12\,\|(z_r-1,D_az)\|_2,                                \tag{R11}
\]

and

\[
 \frac{\|\operatorname{Diag}(\tau_S)z_S-\mathbf1\|_2}{\sqrt{|S|}}
 \le12\,\|(z_r-1,D_az)\|_2.                               \tag{R12}
\]

The unsigned version has every \(\tau_j=1\). To prove these estimates,
gauge-transform \(z_j\mapsto\tau_jz_j\), which turns every labelled edge residual
into an ordinary difference without changing its norm. A vertex error is the root
error plus the sum of edge residuals on its root-to-vertex path.

For a complete binary tree, the contribution of level \(\ell\) to the normalized
leaf norm has operator norm \(2^{-\ell/2}\), so

\[
 \sum_{\ell\ge1}2^{-\ell/2}=1+\sqrt2<\frac52.              \tag{R13}
\]

For all tree vertices the analogous level sum is below \(7/2\). The fanout and
endpoint trees therefore contribute universal constants. On the \(R\) long paths,
Cauchy--Schwarz gives

\[
 \left(\frac1R\sum_{r=1}^R
       \left|\sum_{i=1}^N e_{r,i}\right|^2\right)^{1/2}
 \le\sqrt{\frac NR}\,\|e\|_2=\|e\|_2.                    \tag{R14}
\]

For internal path vertices, the prefix-sum matrix has norm at most \(N\), while
\(\sqrt P>N\). More explicitly, after normalization, the root, fanout, long-path,
and endpoint-tree contributions are bounded respectively by \(1,4,2,4\) for the
all-vertex norm and by \(1,5/2,1,5/2\) for the output-leaf norm. The triangle
inequality therefore gives a constant below 12 in both normalized norms. This proves
(R11)--(R12). With only one long path, the factor in (R14) would be \(\sqrt N\).

For completeness, these four constants follow directly by descendant counting.
At binary-tree level \(k\), the descendant supports of distinct edge residuals are
disjoint and each occupies at most a \(2^{-k}\) fraction of the relevant terminal
blocks; summing the operator norms over levels gives the geometric sum in (R13)
(the slack to 4 also covers the fanout vertices themselves). For the long paths,
the internal-prefix contribution is at most \(N\|e_{\rm path}\|_2/\sqrt P<
\|e_{\rm path}\|_2\), while replicating each terminal path sum over at most \(2L\)
endpoint-tree vertices contributes at most
\(\sqrt{2LN/P}\|e_{\rm path}\|_2\le\|e_{\rm path}\|_2\), since
\(2LN=32N^2\le P\). For output leaves, (R14) gives the displayed constant one
exactly. Thus the claimed bounds 2 and 1 for the long-path block, and the looser
binary-tree bounds 4 and \(5/2\), hold uniformly in \(N\).

#### State decoder

Split the residual of (R2) into its three blocks and put

\[
 E=\|Ax-b\|_2\le\frac{\sqrt2}{200},                        \tag{R15}
\]

since \(b\) has two unit entries. Apply (R11) to the unsigned \(h\) system and (R12)
to \(d\). For \(e_j=\tau_jd_j-1\) on \(S\),

\[
 \|h-\mathbf1\|_2\le12E\sqrt P,
 \qquad \|e\|_2\le12E\sqrt{|S|}.                          \tag{R16}
\]

Let \(a_j=q_j+t_j-2h_j\) be the cap residual. Nonnegativity gives

\[
 q_j\le2h_j+|a_j|,\qquad t_j\le2h_j+|a_j|.                \tag{R17}
\]

Using \(u_j^2+v_j^2\le q_j^2\), (R15)--(R17) imply

\[
 \|x\|_2^2\le\|q\|_2^2+\|h\|_2^2+\|t\|_2^2<11P.           \tag{R18}
\]

For the numerical bound, \(\|a\|_2\le E\) and

\[
 \|h\|_2\le(1+12E)\sqrt P<1.09\sqrt P,\qquad
 \|q\|_2,\|t\|_2\le2\|h\|_2+E<2.18\sqrt P.
\]

Thus the left side of (R18) is less than
\((2(2.18)^2+1.09^2)P<11P\).

Also \(q_j\ge|d_j|\). Therefore

\[
\begin{aligned}
 \sum_{j\in S}\tau_jd_jq_j
 &=\sum_{j\in S}(1+e_j)q_j\\
 &\ge |S|-\sqrt{|S|}\,\|e\|_2-\|e\|_2\|q_S\|_2
 >\frac35|S|.
\end{aligned}                                               \tag{R19}
\]

Indeed, the two loss terms in (R19), divided by \(|S|\), are at most

\[
 12E\left(1+2.18\sqrt{P/|S|}\right)
 <\frac{12\sqrt2}{200}
   \left(1+2.18\sqrt{33/16}\right)<\frac25,               \tag{R19a}
\]

where we used (R18) and \(P/|S|<33/16\).

Measure the ideal amplitude state in the computational basis. On an output pair
\(j\in S\), report \(+1\) on \(u_j\) and \(-1\) on \(v_j\); elsewhere report a fair
random sign. Its bias toward \(p_N\) is

\[
 \frac1{2\|x\|_2^2}\sum_{j\in S}\tau_jd_jq_j
 >\frac{(3/5)\cdot16}{2\cdot11\cdot33}
 =\frac8{605}>\frac1{80}.                                \tag{R20}
\]

Trace distance \(1/100\) reduces the bias by at most \(1/100\), leaving bias
greater than \(1/400\). A fixed number of repetitions therefore computes parity
with bounded error. Quantum parity requires \(\Omega(N)\) sign queries, and the
oracle simulation completes the proof.

#### Output-contract corollaries and quantifiers

The state quantifier above is for the unconditional reduced output of an arbitrary
CPTP algorithm; \(\rho\) may be mixed. It is not restricted to a pure algorithmic
branch. A heralded version with input-independent success probability at least a
constant \(p_0>0\) has the same lower bound: run a fixed constant number of trials,
retain the successful flags, and apply the decoder to a fixed constant number of
successful copies. This gives bounded error and constant worst-case query overhead.
By contrast, saying only that an unheralded internal branch is good with constant
probability is insufficient here: the decoder bias in (R20) is a small constant,
so arbitrary bad branches could cancel it. The unconditional density-operator or
explicit heralded contract is therefore essential.

The result also holds for a weaker, one-observable output contract. Define the
fixed input-independent diagonal observable

\[
 O_S=\sum_{j\in S}
 \left(|u_j\rangle\langle u_j|-|v_j\rangle\langle v_j|\right),
 \qquad \|O_S\|=1.                                      \tag{R20a}
\]

For every \(x\) satisfying (R4), (R19) gives

\[
 p_N\langle x/\|x\||O_S|x/\|x\|\rangle
 =\frac{\sum_{j\in S}\tau_jd_jq_j}{\|x\|_2^2}
 >\frac{(3/5)\cdot16}{11\cdot33}>\frac1{40}.           \tag{R20b}
\]

Consequently, producing a classical additive-\(1/100\) estimate of this single
selected expectation already requires \(\Omega(N)\) coefficient queries. If the
estimate is instead taken on a state \(\rho\) satisfying (R5), its expectation
changes by at most \(2D_{\rm tr}\|O_S\|=1/50\) and therefore retains magnitude
greater than \(1/200\). An additive-\(1/1000\) estimate on \(\rho\) has the same
lower bound. This does not claim hardness for the objective observable, which is
input-independent and has known optimum.

Finally, under the squared-fidelity convention
\(F(\rho,|\psi\rangle)=\langle\psi|\rho|\psi\rangle\), the trace-distance premise
(R5) can be replaced by

\[
 F(\rho,|x/\|x\|\rangle)\ge1-\frac1{100^2}
 =\frac{9999}{10000},                                    \tag{R20c}
\]

by the Fuchs--van de Graaf inequality. Under the root-fidelity convention, take
the square root of the right-hand side.

### Why the original copy-only amplifier cannot have this robustness

In the original single-chain construction, gauge-transform to \(z_i=p_id_i\), set

\[
 z_i=1-\frac{2i}{N}\quad(0\le i\le N),
\]

and set every copied descendant equal to \(z_N=-1\). The anchor and all copy-edge
residuals vanish, while each chain-edge residual has magnitude \(2/N\). Thus every
amplified output encodes the wrong parity with total residual

\[
 \sqrt{N(2/N)^2}=\frac2{\sqrt N}.                          \tag{R21}
\]

No analysis of that one-path LP can make its decoder robust to fixed relative
\(\ell_2\) residual. Theorem 3 pays \(N\) parallel paths, hence
\(\Theta(N^2)\) variables, precisely to remove this drift. Proposition 5 below
shows that a linear-size bounded-degree real-linear gadget can have a comparable
constant soundness gap by using constant gain at every step. That escape incurs
exponential dynamic range and conditioning, so it does not yield a well-scaled
QIPM instance. The dedicated plateau note linked below replaces the long gain
chain by a short gain prefix and obtains polynomial range together with a
uniformly conditioned reduced barrier Hessian.

### Quadratic volume is necessary for signed-edge propagation gadgets

The quadratic size is optimal within a class that includes chains, copy trees,
arbitrary bounded-degree fanout networks, and expanderized signed-edge variants.

**Proposition 4 (effective-resistance volume bound).** Let \(G=(V,E)\) be connected,
have maximum degree \(\Delta\), pinned root \(r\), and nonempty output set \(S\).
Every edge constraint has the form

\[
 d_v-a_{uv}(\sigma)d_u=0,
\]

where, for a fixed set \(T_{uv}\subseteq[N]\) of size at most \(k\),
\(a_{uv}:\{\pm1\}^{T_{uv}}\to\{\pm1\}\) may be an arbitrary Boolean function.
Suppose the constraints are consistent for every \(\sigma\), with \(\tau_r=1\),
and every output label is

\[
 \tau_s=\prod_{i=1}^N\sigma_i\qquad(s\in S).
\]

Then there is a real vector \(d\), with \(d_r=1\) and \(d_s=-\tau_s\) for every
\(s\in S\), whose signed-edge residual satisfies

\[
 \left(\sum_{(u,v)\in E}|d_v-a_{uv}d_u|^2\right)^{1/2}
 \le \frac{k\sqrt{2\Delta |V|}}{N}.                        \tag{Q1}
\]

Consequently, if a fixed threshold \(\eta>0\) must exclude every vector whose
whole output set has the wrong parity, then

\[
 |V|>\frac{\eta^2}{2\Delta k^2}N^2.                        \tag{Q2}
\]

Every root-to-output path has length at least \(N/k\). Consistency makes the
product of its edge-label functions equal \(\prod_i\sigma_i\). In the unique
multilinear Fourier representation on the Boolean cube, each edge function has
degree at most \(k\), and degree is subadditive under products. A path of length
\(\ell\) therefore produces a function of degree at most \(k\ell\). Parity has
degree exactly \(N\), so \(\ell\ge N/k\).

Gauge-transform \(w_v=\tau_vd_v\), making every residual \(w_v-w_u\), and wire
the vertices in \(S\) together. Remove circulations from any unit flow without
increasing its energy, and decompose the resulting acyclic flow into
root-to-\(S\) paths. The distance bound then gives
\(\sum_e|f_e|\ge N/k\).
Cauchy--Schwarz and Thomson's principle imply

\[
 R_{\rm eff}(r,S)=\min_f\sum_e f_e^2
 \ge\frac{N^2}{k^2|E|},\qquad
 C_{\rm eff}(r,S)\le\frac{k^2|E|}{N^2}
 \le\frac{\Delta k^2|V|}{2N^2}.                           \tag{Q3}
\]

By the Dirichlet principle, the minimum edge energy with \(w_r=1\) and
\(w_s=-1\) on \(S\) is \(4C_{\rm eff}(r,S)\). The harmonic minimizer lies in
\([-1,1]\) by the maximum principle. This proves (Q1), and (Q2) follows.

The obstruction is LP-native. Add the same nonnegative pair and cap variables as
in (R2), take \(h_j=q_j=t_j=1\), and set
\(u_j=(1+d_j)/2\), \(v_j=(1-d_j)/2\). All reference and cap residuals vanish, the
point has exact optimal objective \(4|V|\), and every output pair encodes the wrong
parity. If \(|S|\ge\theta|V|\), as in a constant-mass output amplifier, the total
squared norm is at most \(3|V|\) and the fixed plus/minus output decoder has bias
at least \(\theta/6\) toward the *wrong* parity. This makes the output-boundary
condition explicit.

Thus a near-linear expander cannot repair this model: constant conductance
and \(k\)-local Boolean edge coefficients require \(\Omega(N^2/k^2)\)
bounded-degree volume. For constant \(k\), this is still quadratic. Proposition 4
does not cover higher-arity real-linear constraints or non-Boolean coefficient
functions. In the capped LP, \(\|b\|_2=\sqrt2\), so absolute and relative constant
residual thresholds differ only by this fixed factor.

### Referee audit of Proposition 4

The proposition is correct as stated, with the usual convention that every
undirected edge has unit conductance and is counted once.  The proof has four
independent steps, all of which survive multiedges when degree counts
multiplicity.

1. Consistency supplies vertex gauges \(\tau_v\in\{\pm1\}\) with
   \(\tau_v=a_{uv}\tau_u\).  Hence the product of the edge functions on every
   root-to-output path is parity.  An edge function depending on at most \(k\)
   bits has multilinear Fourier degree at most \(k\); subadditivity of degree
   under products gives path length at least \(N/k\).
2. Contracting \(S\) to one terminal is only notation for the usual
   root-to-set resistance.  Removing signed-flow cycles cannot increase
   energy.  Every path in an acyclic unit-flow decomposition ends at an output,
   so its length is at least \(N/k\).  Therefore
   \(\sum_e|f_e|\geq N/k\).
3. Cauchy--Schwarz gives
   \(\sum_e f_e^2\geq N^2/(k^2|E|)\).  Thomson's principle and
   \(|E|\leq\Delta|V|/2\) give (Q3).
4. For a voltage difference two, Dirichlet energy is four times effective
   conductance.  The maximum principle keeps the minimizer in \([-1,1]\), and
   the gauge identity
   \(d_v-a_{uv}d_u=\tau_v(w_v-w_u)\) transfers its energy back without a
   missing factor.  Taking square roots gives exactly (Q1).

Thus there is no hidden factor-of-two, connectivity, flow-cancellation, or
Fourier-degree gap in (Q1)--(Q3).  The unit-modulus gauge identity in step 4 is
the essential structural assumption.

### Proposition 5 (bounded-gain real propagation defeats the quadratic bound)

The analogous claim for arbitrary bounded-coefficient real-linear propagation
gadgets is false.  Fix the constant gain \(B=2\).  For
\(i=0,\ldots,N\), introduce nonnegative variables

\[
 (u_i,v_i,h_i,t_i),
 \qquad d_i=u_i-v_i,
 \qquad q_i=u_i+v_i.
\]

Impose

\[
 \begin{aligned}
 d_0&=1,& d_i-2\sigma_i d_{i-1}&=0 &&(1\leq i\leq N),\\
 h_0&=1,& h_i-2h_{i-1}&=0 &&(1\leq i\leq N),\\
 &&q_i+t_i-2h_i&=0 &&(0\leq i\leq N),
 \end{aligned}                                             \tag{G1}
\]

and minimize

\[
 \sum_{i=0}^N(2u_i+2v_i+h_i+t_i).                         \tag{G2}
\]

This LP has \(4(N+1)\) variables and \(3(N+1)\) full-row-rank equalities.
Every row and column has at most four nonzeros, every coefficient has magnitude
at most two, and each row or column depends on at most one hidden input bit.
The support, right-hand side, and objective are input-independent.

Its unique optimum is

\[
 h_i=q_i=t_i=2^i,
 \qquad d_i=2^ip_i,
 \qquad p_i=\prod_{j=1}^i\sigma_j,                        \tag{G3}
\]

so exactly one of \(u_i,v_i\) equals \(2^i\).  It is strictly
primal-dual feasible, nondegenerate, and strictly complementary.  Moreover,
there are absolute constants \(\epsilon_0,c_0>0\) with the following robust
property.  If \(x\geq0\) satisfies

\[
 \|Ax-b\|_2\leq\epsilon_0,                               \tag{G4}
\]

then a fixed measurement of \(|x/\|x\|\rangle\) returns the parity \(p_N\)
with probability at least \(1/2+c_0\).  Consequently, producing a state within
trace distance \(10^{-2}\) of any such normalized point requires
\(\Omega(N)\) coefficient queries, even though the LP volume is only linear.

#### Proof

The first two equation families in (G1) are triangular and fix
\(h_i=2^i\), \(d_i=2^ip_i\) exactly.  Nonnegativity gives
\(q_i\geq|d_i|=h_i\), while the cap gives \(q_i+t_i=2h_i\).  The objective
contribution at vertex \(i\) is

\[
 2q_i+h_i+t_i=q_i+3h_i,
\]

so its unique minimum has \(q_i=t_i=h_i\), proving (G3).  Choosing
\(q_i=3h_i/2\), \(t_i=h_i/2\) gives strict primal feasibility.  Strict dual
feasibility follows already from equality multiplier zero because every
objective coefficient is positive.  At the optimum, the sign-selected member
of \((u_i,v_i)\), together with \(h_i,t_i\), gives exactly
\(3(N+1)\) positive columns.  The gain, reference, and cap equations make
this column basis block triangular and nonsingular. The opposite pair member
has reduced cost two: increasing it by \(\delta\), while preserving the fixed
value of \(d_i\), increases both members of the pair by \(\delta\), decreases
\(t_i\) by \(2\delta\), and raises (G2) by \(2\delta\). The dual basic solution
therefore has zero slack on every positive basic variable and slack two on every
nonbasic pair member. This proves nondegeneracy and strict complementarity.

It remains to prove robustness.  Let \(E=\|Ax-b\|_2\), and denote the gain-row
residuals by \(e_i\), including the root anchor as \(e_0=d_0-1\).  Gauge and
rescale:

\[
 a_i=2^{-i}p_id_i.
\]

Then

\[
 a_0-1=e_0,
 \qquad
 a_i-a_{i-1}=2^{-i}p_ie_i,
\]

and therefore

\[
 |a_i-1|
 \leq\left(1+\sqrt{\sum_{j\geq1}4^{-j}}\right)E
 =\left(1+{1\over\sqrt3}\right)E.                       \tag{G5}
\]

The same argument for the reference rows, with
\(b_i^{\rm ref}=2^{-i}h_i\), gives the identical bound.  Put
\(K=1+1/\sqrt3\).  For \(E\leq10^{-2}\),

\[
 p_id_i\geq(1-KE)2^i,
 \qquad
 0\leq h_i\leq(1+KE)2^i.                                \tag{G6}
\]

Let \(c_i=q_i+t_i-2h_i\) be the cap residual.  Since \(q_i,t_i\geq0\),

\[
 q_i,t_i\leq2h_i+|c_i|.
\]

Also
\(u_i^2+v_i^2=(q_i^2+d_i^2)/2\leq q_i^2\).  Hence

\[
 \begin{aligned}
 \|x\|_2^2
 &\leq\sum_i\left[(q_i+t_i)^2+h_i^2\right]\\
 &\leq9\sum_i h_i^2+2\sum_i c_i^2\\
 &\leq12(1+KE)^2\,4^N+2E^2.                             \tag{G7}
 \end{aligned}
\]

At the endpoint, the coordinate selected by \(p_N\) has value

\[
 {q_N+|d_N|\over2}\geq|d_N|\geq(1-KE)2^N.              \tag{G8}
\]

Equations (G7)--(G8) put a fixed positive fraction of the normalized squared
mass on the correct endpoint coordinate.  The decoder outputs its plus/minus
label there and a fair bit elsewhere.  At \(E=10^{-2}\), its ideal bias is
greater than \(3/100\); trace distance \(10^{-2}\) leaves positive constant
bias.  Constant repetition gives bounded error.

Every sparse row, column, or value query to (G1) is simulated with at most one
query to the corresponding \(\sigma_i\).  The quantum parity lower bound now
proves the final assertion.

The scalar core makes the escape from Proposition 4 transparent.  With
\(z_i=p_id_i\) and \(w_i=2^{-i}z_i\),

\[
 d_i-2\sigma_i d_{i-1}=p_i2^i(w_i-w_{i-1}).              \tag{G9}
\]

The effective resistance from \(w_0\) to \(w_N\) is

\[
 \sum_{i=1}^N4^{-i}<\frac13,
\]

so reversing the normalized endpoint costs constant energy on one path.  In
the unit-modulus signed-edge model every conductance is one and the resistance
is instead \(N\).

The displayed chain has exponential solution range and conditioning. That is not
essential to the counterexample: the next refinement has only polynomial range
and conditioning. Thus no general \(\Omega(N^2/k^2)\) volume theorem follows from
bounded row/column degree, bounded coefficient magnitude, \(O(1)\)-bit
coefficient locality, and polynomial numeric bounds alone. A valid positive
extension needs a genuinely uniform energy-conservation, bounded-gain-product,
or constant scaled-Hoffman hypothesis.

### Linear-size polynomial-range upgrade

A stronger plateau-gain construction is proved in
[2026-09-02-linear-size-robust-gain-parity-lp.md](2026-09-02-linear-size-robust-gain-parity-lp.md).
It has \(\Theta(N)\) variables, an \(\Omega(N)\) coefficient-query lower bound,
right-hand-side-relative residual and trace-distance thresholds \(1/100\), maximum
primal scale \(\Theta(\sqrt N)\), and reduced central-tail condition number below
\(7/6\). That note also proves the sharp path-bundle frontier
\(PH^2=\Omega(N^2)\), unifying the bounded-scale quadratic construction here with
the linear-size plateau construction.

The Thomson and Dirichlet principles, and bounds obtained from flow
decompositions, are standard electrical-network tools; see, for example,
[Aldous and Fill, Chapter 3.7](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S7.html).
They are not novelty claims. The apparent new observation is their use to prove
quadratic volume necessity for a locally queryable parity-propagation LP gadget.

### Scope and novelty audit

Theorem 3 is an end-to-end coefficient-oracle lower bound for the original primal
state. Row or column scaling, preconditioning, an OSS formulation, or an
infeasible-start implementation cannot change the fixed decoder (R20) promised at
the output. Unlike the earlier normal-equation and multiplier-state examples in
this repository, its hardness is not caused by a poorly conditioned reduced Newton
system.

The residual convention in (R4) is important. It is the standard right-hand-side
relative residual

\[
 \|Ax-b\|_2/\|b\|_2,
\]

and here \(\|b\|_2=\sqrt2\). Thus the theorem permits a fixed global residual
\(\sqrt2/200\), independent of \(P\). It does **not** claim robustness for a
row-normalized root-mean-square residual, nor for the scale-invariant backward
error \(\|Ax-b\|/(\|A\|\|x\|+\|b\|)\). Since there are \(3P\) rows, a fixed
global residual corresponds to an average residual of order \(P^{-1/2}\) per row.
This normalization should be stated whenever the result is quoted. Likewise,
``any \(x\)'' means any **nonzero** nonnegative \(x\) satisfying (R4), because its
amplitude state otherwise is undefined.

The coefficient-oracle qualification is also substantive. It covers the usual
coherent fixed-position sparse row/value oracle and the analogous column oracle:
the queried row or column contains only constantly many entries, and one LP query
is simulated by one query to the hidden-sign oracle even though a sign
is repeated on \(R\) paths. It does not cover a stronger, separately supplied
global amplitude-state or batch oracle that aggregates all repeated occurrences
of a coefficient in one call.

The unconditional-state convention in Theorem 3 avoids an otherwise real
ambiguity about probabilistic output guarantees. A claim that (R5) holds merely
with probability \(2/3\) over an **unflagged** classical branch is not enough for
the decoder: an adversarial failure branch could overwhelm the small constant bias
in (R20). The usual heralded state-preparation contract is covered, because one can
repeat until a success flag is seen and then take the fixed number of successful
samples used by the parity decoder. An unheralded high-probability contract would
need a stronger success probability or an additional argument.

The theorem does not lower-bound a Newton-direction state, and it does not apply to
a QIPM whose only output is the scalar objective. Although (R3) has a unique
optimum, even the two-sided objective-accuracy condition (R6) is only an optional
simultaneous promise, not an independent objective-output lower bound. The hardness
comes entirely from the approximate-feasibility and state-output contract. A
one-sided inequality would be weaker still and would not be meaningful as a gap for
an infeasible point, because an input-independent vector can lie below the feasible
optimum.
Moreover, the feasible reduced Newton direction changes \(u_j,v_j\) equally and
therefore does not itself encode \(\tau_j\); turning this construction into a
Newton-direction lower bound would require a different gadget.

#### Collision audit through 2026-09-02

Several ingredients have close precedents, so they should not be presented as new:

- Parallel paths and the \(N/R\) effective-resistance calculation are standard
  electrical-network facts. In quantum query complexity, effective resistance is
  also the exact positive-witness quantity for the \(st\)-connectivity span
  program; see Belovs and Reichardt,
  [*Span programs and quantum algorithms for st-connectivity and claw
  detection*](https://arxiv.org/abs/1203.2603), and Jarret et al.,
  [*Quantum Algorithms for Connectivity and Related
  Problems*](https://arxiv.org/abs/1804.10591). The contribution here is the
  bounded-degree LP use of \(N\) parallel parity paths to obtain a constant
  residual-decoding gap, not the circuit law itself.
- Padding a clock by repeated final configurations is standard in
  Feynman--Kitaev/HHL-style constructions, and Mori et al.
  [arXiv:2601.16697](https://arxiv.org/abs/2601.16697), Theorem 1, use a full
  repeated endpoint-parity block in a sparse QLS lower bound. Their output promise
  is Euclidean closeness to one designated normalized inverse state. It does not
  say that every vector of small equation residual is decodable.
- Robust computation encodings also occur in Hamiltonian complexity. Nirkhe,
  Vazirani, and Yuen,
  [*Approximate low-weight check codes and circuit lower bounds for noisy ground
  states*](https://arxiv.org/abs/1802.07419), use a Feynman--Kitaev construction
  to embed code spaces robustly under their noisy-ground-state model. Anshu,
  Breuckmann, and Nguyen,
  [*Circuit-to-Hamiltonian from tensor networks and fault
  tolerance*](https://arxiv.org/abs/2309.16475), show that sufficiently low-energy
  states in a fault-tolerant circuit encoding retain a noisy computation. These
  are important conceptual comparators for the ``all approximate objects decode''
  idea, but they concern local-Hamiltonian energy/noise and circuit complexity,
  not nonnegative LP vectors, right-hand-side residual, or coefficient queries.
- Recent robust or instance-dependent QLS algorithms do not collide with the
  quantifiers in Theorem 3. Dalzell, Li, and Su,
  [*Faster quantum linear system solver beyond the condition
  number*](https://arxiv.org/abs/2607.07691), approximate a designated normalized
  solution after spectral truncation or filtering. Li,
  [*A Residual-Based Quantum Linear System Algorithm with Dynamic Stopping and
  Applications to Elliptic PDEs*](https://arxiv.org/abs/2605.06414), introduces a
  residual register as an a posteriori stopping signal. Neither proves a
  coefficient-query lower bound for every state represented by every vector in a
  fixed residual tube.
- Apers and Gribling,
  [*Quantum speedups for linear programming via interior point
  methods*](https://arxiv.org/abs/2311.03215), explicitly return a feasible
  near-optimal classical point and prove an LP **value** query lower bound in
  Theorem 8.4. Van Apeldoorn et al.
  [arXiv:1705.01843](https://arxiv.org/abs/1705.01843), Theorem 30 and Corollary
  31, likewise give LP/SDP value lower bounds. Neither result is an
  approximate-feasible amplitude-state lower bound.

The QLS output-state lower bounds cited above this extension are not black-box
proofs of Theorem 3. They supply a square linear system and single out its inverse
state (or minimum-norm state). Here \(A\) is rectangular and underdetermined and
the algorithm may choose **any** nonnegative approximate feasible vector. Reduced
barrier conditioning \(W^TH_xW=\lambda I\) does not assert that the feasibility
operator \(A\), or a chosen square basis of it, has condition one. The new work is
therefore precisely (R11)--(R20), which makes the whole admissible residual tube
decode parity.

No primary source located in the targeted search gives all of the following in one
result: a fixed-pattern bounded-row-and-column-degree LP; a standard
right-hand-side-relative \(\ell_2\) residual promise; quantification over every
nonnegative vector satisfying that promise; a coefficient-query lower bound for
its primal amplitude state; and an input-independent scalar reduced central-path
Hessian. The defensible status is therefore: **apparently new LP-native robust
state-output theorem, built from standard parity, padding, and effective-resistance
ingredients**. It proves \(\Omega(\sqrt P)\), not a linear lower bound in LP
dimension; the quadratic size is exactly the cost paid for constant residual
soundness. This is evidence of novelty, not proof of priority.

### Referee verdict on Theorem 3

**Verdict: correct in the stated coefficient-oracle and residual normalization,
after the repairs recorded above.** Equations (R1)--(R21) have been checked with
their displayed constants. In particular, the two anchors give
\(\|b\|_2=\sqrt2\); the stability estimates imply the explicit norm bound
\(\|x\|_2^2<11P\); and the total loss in (R19) is below \(2|S|/5\), leaving decoder
bias greater than \(1/80-1/100=1/400\) after trace error. The reduction quantifies over
every nonzero nonnegative vector in the residual tube and over arbitrary mixed
unconditional CPTP output. The fixed-success heralded and selected-observable
variants above are also valid; an unspecified unheralded good branch is not.

The structural claims also survive audit. The pinned labelled-incidence,
unsigned-incidence, and private-cap blocks give full row rank. The positive primal
columns form a basis, the displayed dual solution has slack two exactly on the
zero pair member, and uniqueness of the basis multipliers gives dual
nondegeneracy. The basis (R9) is orthonormal and input-independent, and the reduced
central Hessian is a positive scalar identity. A coherent sparse row, entry, or
column query needs only one hidden-sign query even though each sign is repeated on
all \(R\) paths.

The main correction was to replace the former one-sided objective clause by the
two-sided accuracy condition (R6). For an infeasible point, a one-sided expression
relative to the feasible optimum is not an optimality gap. The proof deliberately
does not use objective accuracy, so Theorem 3 is a robust primal-state/output
lower bound, not a value-estimation lower bound. Its \(\Omega(\sqrt P)\) scaling
and its dependence on the standard global right-hand-side-relative residual must
remain explicit when the result is stated.
