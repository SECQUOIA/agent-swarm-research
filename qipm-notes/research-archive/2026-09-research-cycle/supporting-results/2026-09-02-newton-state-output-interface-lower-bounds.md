# Newton-state output-interface lower bounds

Date: 2026-09-02

## Summary

A quantum state proportional to a Newton direction is not generically a cheap,
reusable iterate oracle.  The theorem below makes the tradeoff sharp: converting
a state-preparation circuit into a diagonal block encoding must pay through
either the number of state-oracle queries or the block-encoding normalization.
The product is \(\Omega(\sqrt n)\), and the known amplitude-to-diagonal
construction saturates it.

The proof uses standard hybrid and amplitude-estimation arguments.  The
apparently new content is the normalization--query interface theorem and its
central-path consequences, not a new adversary technique.

A stronger compositional theorem below does not assume that the algorithm
actually constructs a block encoding: turning the normalized iterate state
into the solution state of a subsequent one-sparse, condition-below-two
diagonal system already takes \(\Omega(\sqrt n)\) coherent queries.  These
costs add to \(\Omega(T\sqrt n)\) in an explicitly defined online
fresh-oracle interface, including one-time compiler setup.  They do not yet
give an unconditional \(T\)-factor for a QIPM on one fixed LP; the exact
freshness, atomic-query, oracle-extension, and trajectory-embedding
obstructions are recorded below.

The centrality pair also admits an input-generated version: two one-sparse LPs
with equal-norm objective-state oracles are
\(\Theta(\mu/\sqrt n)\)-close, their scalar optimum values can differ by
\(\Theta(n\mu)\), and a common primal--dual pair is centered for one input but
far outside the \(N_2\) neighborhood for the other.  This gives an end-to-end
\(\Omega(\sqrt n/\mu)\) lower bound in the state-only objective-data model.
The same construction explicitly fails for binary coefficient-value or freely
supplied Newton-block-encoding access, which fixes the theorem's oracle
boundary.

## Oracle model

Let \(v\in\mathbb R_{>0}^n\), let \(\nu=\|v\|_2\) be known, and suppose that
controlled access is given to a state-preparation circuit and its inverse:

\[
 U_v|0\rangle=|\widehat v\rangle
 =\frac1\nu\sum_{j=1}^n v_j|j\rangle.
\]

The circuit fixes a consistent real phase.  This is stronger than copy access:
an ordinary quantum state only defines a ray and cannot specify the sign of a
Newton update.  Take \(n\) to be a power of two, or pad the vectors by identical
positive coordinates to the next qubit-register dimension.

## Normalization--query product theorem

Suppose a controlled invocation of a circuit \(W_v\), using \(q\) calls to
\(U_v,U_v^\dagger\), is an \((\alpha,a,1/8)\)-block encoding of
\(\operatorname{Diag}(v)\).  Suppose its reported normalization obeys
\(\alpha\leq A\), where \(A\geq1\) is a uniform known bound.  Then, in the
worst case,

\[
 \boxed{qA=\Omega(\sqrt n).}
\tag{1}
\]

### Proof

For \(n\geq10\), consider the positive equal-norm pair

\[
 v^{(0)}=(1,\ldots,1),
 \qquad
 v^{(1)}=(2,\beta,\ldots,\beta),
 \qquad
 \beta=\sqrt{\frac{n-4}{n-1}}.
\tag{2}
\]

Both norms are \(\sqrt n\), and

\[
 \frac1{\sqrt n}
 \leq
 \left\|
   \frac{v^{(0)}}{\sqrt n}-
   \frac{v^{(1)}}{\sqrt n}
 \right\|_2
 \leq \sqrt{\frac2n}.
\tag{3}
\]

Choose extensions \(U_0,U_1\) related by the minimum planar rotation that maps
one prepared state to the other.  Then

\[
 \|U_0-U_1\|=\Theta(n^{-1/2}),
\]

and the standard hybrid argument says that any constant-bias distinguisher
needs \(\Omega(\sqrt n)\) total calls to these oracles and their inverses.

On the other hand, \(O(A)\) controlled calls to \(W_v\) suffice to distinguish
the pair.  Estimate

\[
 \operatorname{Re}
 \langle0^a,1|W_v|0^a,1\rangle
\]

to additive error \(1/(16A)\), and multiply by the reported \(\alpha\).  The
estimation error is at most \(1/16\), and the block-encoding error contributes
at most \(1/8\), so the first diagonal entry is recovered within \(1/4\).  This
separates one from two.  The complete distinguisher uses \(O(qA)\) calls to the
original state oracle, which proves (1).

### Worst-case tightness on the near-uniform family

Rattew and Rebentrost's Theorem 2 gives, from \(U_v\), an exact constant-query
block encoding of

\[
 \operatorname{Diag}(v/\nu).
\]

Viewed as an encoding of \(\operatorname{Diag}(v)\), its normalization is
\(\alpha=\nu\).  For the near-uniform hard pair, \(q\alpha=\Theta(\sqrt n)\),
so the worst-case bound (1) is tight up to constants on this family.  It is not
a per-vector lower bound for every structured preparation circuit.

Consequently, a generic QLS Newton state cannot be converted into an
\(O(\|v\|_\infty)\)-normalized diagonal iterate oracle with polylogarithmic
dimension dependence.  Moving cost from oracle construction into
subnormalization does not evade the product bound.

If only independent copies of \(|\widehat v\rangle\) are provided, the same
pair needs \(\Omega(n)\) copies: its overlap is \(1-\Theta(1/n)\), so the trace
distance of \(k\) copies is constant only for \(k=\Omega(n)\).

## Strict-complementarity centrality barrier

The generic \(\sqrt n\) result becomes worse near a strictly complementary
endpoint, even if state access is supplied for the full feasible primal--dual
triple.  Let \(n=2m\), \(m\geq5\), \(0<\mu\leq1\), and define

\[
 \beta=\sqrt{\frac{m-4}{m-1}},
 \qquad
 v=(2,\beta\mathbf1_{m-1}),
 \qquad
 r=(m-1)(1-\beta)=\frac3{1+\beta},
 \qquad
 z=2(r,\mathbf1_{m-1}).
\]

Then \(\|v\|_2=\|\mathbf1_m\|_2\) and
\(z^\top(v-\mathbf1_m)=0\).  Consider the fixed one-sparse LP

\[
 A=[I_m\;0],
 \qquad b=\mathbf1_m,
 \qquad c=(z,\mathbf1_m).
\tag{4}
\]

Use the common primal point and the two dual--slack pairs

\[
 x=(\mathbf1_m,\mu\mathbf1_m),
\tag{5}
\]

\[
 s^{(0)}=(\mu\mathbf1_m,\mathbf1_m),
 \qquad
 y^{(0)}=z-\mu\mathbf1_m,
\]

\[
 s^{(1)}=(\mu v,\mathbf1_m),
 \qquad
 y^{(1)}=z-\mu v.
\tag{6}
\]

Both triples are primal--dual feasible for (4).  The slack norms agree because
\(\|v\|=\|\mathbf1\|\), and the dual norms agree because
\(z^\top(v-\mathbf1)=0\):

\[
 \|s^{(0)}\|_2=\|s^{(1)}\|_2,
 \qquad
 \|y^{(0)}\|_2=\|y^{(1)}\|_2.
\]

The YES triple is exactly centered, with \(\bar\mu_0=\mu\).  For the NO
triple, \(\bar\mu_1<\mu\), while its first complementarity product is
\(2\mu\).  Hence

\[
 \|Xs^{(1)}-\bar\mu_1\mathbf1_n\|_2>\mu>\bar\mu_1.
\tag{7}
\]

The slack-state distance is \(\Theta(\mu/\sqrt n)\).  The dual vectors differ
by the same unnormalized vector \(\mu(v-\mathbf1)\), while their common norm is
\(\Omega(\sqrt m)\); hence their normalized-state distance is also
\(O(\mu/\sqrt n)\).  Choose clean close extensions for both state-preparation
oracles.  A hybrid argument over queries to either oracle gives

\[
 \boxed{
 Q_{N_2}=\Omega(\sqrt n/\mu)
 }
\tag{8}
\]

total controlled state-preparation queries to distinguish

\[
 \|Xs-\bar\mu\mathbf1\|_2\leq\bar\mu/4
 \quad\text{from}\quad
 \|Xs-\bar\mu\mathbf1\|_2\geq3\bar\mu/4.
\]

With copy-only access the bound is \(\Omega(n/\mu^2)\).  This lower bound
already grants the fixed LP data, the common \(x\), all three norms, positivity,
and consistent real phases.  Both triples approach the same strictly
complementary optimum

\[
 (x^*,y^*,s^*)=((\mathbf1_m,0),z,(0,\mathbf1_m)).
\]

Thus even full feasible-triple amplitude-state access does not supply a
dimension-polylogarithmic replacement for a coordinate-sensitive \(N_2\)
neighborhood test.  A coordinate-value oracle still defeats the construction,
so (8) is an interface lower bound, not an input-query lower bound for every
QIPM representation.

## Input-generated one-sparse LP lower bound

The preceding feasible triples need not be supplied as exogenous iterate
states.  They can be generated by the objective oracle of an actual sparse LP,
and the same close-oracle pair then gives a scalar, end-to-end optimization
lower bound.  This strengthens the state-only interpretation of (8), but it
does **not** turn it into a lower bound for the usual binary coefficient-value
oracle.

Retain \(n=2m\), \(v,\beta,r\) from above, and put

\[
 d=v-\mathbf1_m,
 \qquad z_0=2(r,\mathbf1_{m-1}),
 \qquad z_\mu=z_0-\frac\mu2d.
\]

The identities

\[
 z_0^Td=0,
 \qquad \mathbf1^Td=1-r,
 \qquad 1\leq\|d\|_2^2\leq2
\tag{9}
\]

follow directly from \((m-1)(1-\beta)=r\).  Consider the two LPs

\[
 \min\{(c^{(b)})^Tx:Ax=\mathbf1_m,\ x\geq0\},
 \qquad A=[I_m\;0],
\tag{10}
\]

with

\[
 c^{(0)}=(z_\mu,\mathbf1_m),
 \qquad
 c^{(1)}=(z_\mu+\mu d,\mathbf1_m).
\tag{11}
\]

All entries are positive for \(0<\mu\leq1\), the constraint matrix has full row
rank and row and column sparsity at most one, and both LPs are strictly
primal--dual feasible with an attained finite optimum.  Also
\(AA^T=I_m\), so the unweighted constraint matrix has condition number one.
Crucially, the two
objective norms agree exactly:

\[
 \|c^{(1)}\|_2^2-\|c^{(0)}\|_2^2
 =2\mu z_\mu^Td+\mu^2\|d\|_2^2=0.
\tag{12}
\]

Let the only input-dependent access be a controlled clean preparation oracle
for \(|c^{(b)}\rangle=c^{(b)}/\|c^{(b)}\|_2\), together with its inverse.  The
common norm, \(A\), and the right-hand side are free.  Since
\(\|c^{(b)}\|_2=\Theta(\sqrt n)\), (9)--(12) give

\[
 \bigl\||c^{(1)}\rangle-|c^{(0)}\rangle\bigr\|_2
 =\frac{\mu\|d\|_2}{\|c^{(0)}\|_2}
 =\Theta\!\left(\frac\mu{\sqrt n}\right).
\tag{13}
\]

Choose the two valid unitary completions to differ only by the minimum planar
rotation between these states.  The hybrid argument then proves that
distinguishing the two sparse-LP inputs takes

\[
 \Omega(\sqrt n/\mu)
\tag{14}
\]

controlled objective-state queries.

With independent copies instead of controlled preparation/inverse access, the
same pair requires \(\Omega(n/\mu^2)\) copies, because its squared state
distance is \(\Theta(\mu^2/n)\).
Conversely, amplitude estimation of the known first objective amplitude to
additive accuracy \(\Theta(\mu/\sqrt n)\) distinguishes the pair using
\(O(\sqrt n/\mu)\) controlled queries.  Thus the state-query exponent is tight
for this promise family.

This is simultaneously an update/certification lower bound and an end-to-end
value lower bound.  Give the algorithm the common primal--dual pair

\[
 x=(\mathbf1_m,\mu\mathbf1_m),
 \qquad y=z_\mu-\mu\mathbf1_m.
\tag{15}
\]

The induced slack is \((\mu\mathbf1_m,\mathbf1_m)\) for input zero and
\((\mu v,\mathbf1_m)\) for input one.  Thus the first input is exactly centered,
whereas the second is outside every fixed \(N_2\) neighborhood with radius
less than one, exactly as in (7).  The iterate is now generated from the LP
objective and the common pair (15), rather than supplied by a separate slack
oracle.

For the scalar claim, every feasible point has first block \(\mathbf1_m\), and
the positive-cost second block is zero at the optimum.  Hence

\[
 \operatorname{OPT}_1-\operatorname{OPT}_0
 =\mu\mathbf1^Td=\mu(1-r),
 \qquad
 |\operatorname{OPT}_1-\operatorname{OPT}_0|\geq\frac\mu2.
\tag{16}
\]

An algorithm estimating the optimum to additive error at most \(\mu/8\), or
returning enough information to certify which side of the known midpoint it
lies on, distinguishes the clean objective oracles.  It therefore also needs
the query lower bound (14).  This is a scalar-output lower bound, not a cost of
writing an \(n\)-coordinate solution.

The value gap can be put at the natural IPM duality-gap scale without changing
the oracle distance.  Let \(L=6\), replace the objectives by

\[
 \widetilde c^{(0)}=
 n(z_0-\tfrac\mu2d,\mathbf1_m),
 \qquad
 \widetilde c^{(1)}=
 n(z_0+\tfrac\mu2d,\mathbf1_m),
\]

and replace the right-hand side by \(b=L^{-1}\mathbf1_m\).  Multiplying both
objectives by the same scalar leaves their normalized state oracles unchanged,
so (13)--(14) still apply.  Use the common point

\[
 \widetilde x=(L^{-1}\mathbf1_m,(\mu/n)\mathbf1_m),
 \qquad
 \widetilde y=n(z_0-\tfrac\mu2d)-L\mu\mathbf1_m.
\]

For input zero its slack is
\((L\mu\mathbf1_m,n\mathbf1_m)\), so every complementarity product is
exactly \(\mu\).  For input one the first slack block is
\(\mu(L\mathbf1_m+nd)\), which remains positive: for \(m\geq5\),
\(n(1-\beta)\leq5<L\).  Its first product is
\(\mu(1+n/L)\), so it is far outside a fixed \(N_2\) neighborhood.  Finally,

\[
 |\widetilde{\operatorname{OPT}}_1-
   \widetilde{\operatorname{OPT}}_0|
 =\frac{n\mu}{L}(r-1)\geq\frac{n\mu}{12}.
\]

The YES point has total duality gap \(\widetilde x^T\widetilde s=n\mu\).
Therefore additive optimum accuracy \(n\mu/48\), a fixed fraction of the
ordinary centered duality-gap scale, already inherits the
\(\Omega(\sqrt n/\mu)\) state-query lower bound.  The scalar theorem is not an
artifact of demanding accuracy \(n\) times finer than the usual IPM stopping
scale.

### Why the result does not lift to stronger input oracles

The access qualification in (14) is essential.

1. A standard sparse coefficient-value oracle writes a binary approximation of
   \(c_i\) into a value register.  In (11), querying the known first coordinate
   reveals values separated by \(\mu\) in one query, provided the oracle exposes
   the requested precision.  Hiding the exceptional coordinate restores an
   unstructured-search \(\Omega(\sqrt n)\) bound, but not the additional
   \(1/\mu\) factor.  Distinct computational-basis value strings do not give
   close unitary completions merely because their represented real numbers are
   numerically close.
2. A freely supplied block encoding of the Newton normal matrix is also a
   stronger oracle.  At (15), the first input has
   \(H_0=\mu^{-1}I_m\), whereas the second has
   \(H_1=\mu^{-1}\operatorname{Diag}(v^{-1})\).  After the natural
   \(\mu^{-1}\) normalization, their known first diagonal entries are one and
   one half.  Constantly many controlled block-encoding queries distinguish
   them.  The cost (14) can instead reside in *constructing* that Newton oracle
   from the objective-state input; it cannot be charged again after the block
   encoding is granted for free.
3. The LP family therefore proves an end-to-end lower bound for a state-only
   data/update interface.  It is not representation invariant and does not
   lower-bound QIPMs supplied with entry-value QRAM, a precomputed Newton-system
   oracle, or any other input that exposes the changed coordinate directly.

This boundary is also a no-go for obtaining a \(\sqrt n/\mu\) lower bound in
the standard exact-value sparse-oracle model by merely replacing an exogenous
hard iterate with a small coefficient perturbation.  One needs either a weak
analog/phase oracle with an explicitly charged precision, a hidden-coordinate
adversary giving only the search factor, or a different global LP property.

The same example gives a tight state-accuracy requirement.  If
\(\||\widetilde s\rangle-|s/\|s\|\rangle\|_2\leq\xi\), then

\[
 \|x\circ(\widetilde s-s)\|_2
 \leq \|x\|_\infty\|s\|_2\xi.
\]

Since \(\|s\|_2=\Theta(\sqrt n)\), centrality error \(O(\mu)\) requires

\[
 \xi=O(\mu/\sqrt n),
\]

and (4)--(7) show this scaling is necessary.

## Fraction-to-boundary barrier

Even line search cannot generically be driven from a direction state at
polylogarithmic dimension cost.  Let \(x=\mathbf1_n\) and compare equal-norm
directions

\[
 \delta^{(0)}=-\tfrac12\mathbf1_n,
 \qquad
 \delta^{(1)}=(-1,-\gamma,\ldots,-\gamma),
 \quad
 \gamma=\tfrac12\sqrt{\frac{n-4}{n-1}}.
\]

Their maximal positive steps are two and one, while their normalized states are
\(\Theta(n^{-1/2})\) apart.  Any state-only rule that never returns a step
larger than one on the second input, but returns at least \(3/2\) on the first,
needs \(\Omega(\sqrt n)\) controlled state-preparation calls.

## A state-to-next-solve lower bound

The normalization--query theorem concerns a particular compiler.  The next
result rules out a more general bypass: on a hard family, an algorithm cannot
use the iterate state to prepare the solution of the next diagonal system
without ever constructing a diagonal block encoding.

Fix \(0<\eta\leq1/4\) and define

\[
 v^{(0)}=\mathbf1_n,
 \qquad
 v^{(1)}=(1+\eta,\beta_\eta,\ldots,\beta_\eta),
 \qquad
 \beta_\eta=
 \sqrt{1-\frac{2\eta+\eta^2}{n-1}}.
\tag{17}
\]

Both vectors have norm \(\sqrt n\).  For \(n\geq4\), their normalized-state
distance \(d_\eta\) satisfies

\[
 \frac{\eta}{\sqrt n}
 \leq d_\eta
 =\frac1{\sqrt n}
   \sqrt{\eta^2+(n-1)(1-\beta_\eta)^2}
 \leq\frac{2\eta}{\sqrt n}.
\tag{18}
\]

Let

\[
 D_b=\operatorname{Diag}(v^{(b)}),
 \qquad
 r=\frac{e_1+e_2}{\sqrt2},
 \qquad
 |z_b\rangle=\frac{D_b^{-1}r}{\|D_b^{-1}r\|_2}.
\tag{19}
\]

These are one-sparse diagonal systems, and

\[
 \kappa(D_b)\leq\frac{1+\eta}{\beta_\eta}<2.
\tag{20}
\]

The solution states are separated by \(\Omega(\eta)\).  One direct way to see
this is to measure in the computational basis.  For \(b=0\), the probability
of outcome one is \(1/2\).  For \(b=1\), put
\(q=\beta_\eta/(1+\eta)\).  That probability is
\(q^2/(1+q^2)\), and \(q\leq1/(1+\eta)\), so

\[
 \frac12-\frac{q^2}{1+q^2}
 \geq
 \frac12-\frac1{1+(1+\eta)^2}
 =\frac{2\eta+\eta^2}{2(2+2\eta+\eta^2)}
 \geq \frac{\eta}{3}.
\tag{21}
\]

### Theorem 1 (one-transition lower bound)

Give an algorithm controlled access to \(U_b,U_b^\dagger\), where
\(U_b|0\rangle=|v^{(b)}\rangle/\sqrt n\), and choose the two extensions by the
minimum rotation as in the normalization--query theorem.  If the algorithm
prepares a state \(\rho_b\) satisfying

\[
 D_{\rm tr}(\rho_b,|z_b\rangle\!\langle z_b|)\leq\eta/12
\tag{22}
\]

for both \(b\), it needs \(\Omega(\sqrt n)\) calls to
\(U_b,U_b^\dagger\).

In particular, taking the fixed short-step size \(\eta=1/4\) makes (22) a
constant-accuracy QLS output requirement; no inverse-precision factor is being
hidden in the \(\Omega(\sqrt n)\) conclusion.

#### Proof

Equation (21), contractivity of trace distance under measurement, and (22)
imply that the two algorithm outputs have trace distance at least \(\eta/6\).
A \(Q\)-query hybrid has trace distance at most

\[
 Q\|U_0-U_1\|=Qd_\eta\leq\frac{2Q\eta}{\sqrt n}.
\]

Consequently \(Q\geq\sqrt n/12\).  The same bound holds with controlled
queries because the controlled-oracle difference has the same operator norm.
\(\square\)

With copy-only iterate access, the same transition needs \(\Omega(n)\) copies.
For \(k\) copies the input trace distance is at most
\(\sqrt{k}\,d_\eta=O(\sqrt{k}\eta/\sqrt n)\), which must reach
\(\Omega(\eta)\) to produce outputs satisfying (22).

The conclusion is independent of block-encoding normalization and applies to
any circuit that produces the next solution state.  The Hermitian embedding

\[
 H_b=\begin{pmatrix}0&D_b\\D_b&0\end{pmatrix}
\tag{23}
\]

has the same condition number and row sparsity one, so the result is also a
standard Hermitian QLS lower bound with state-oracle access to the changing
diagonal: the right-hand side \((0,r)\) has solution \((D_b^{-1}r,0)\).
The symbol \(v\) can represent either a primal or a slack iterate.  Fixing
\(s=\mathbf1\) makes \(D_b=\operatorname{Diag}(x/s)\), while fixing
\(x=\mathbf1\) makes \(D_b=\operatorname{Diag}(s/x)\).  Thus the same
reduction covers diagonal primal, diagonal slack, and either ratio compiler
interface.

This theorem does not contradict a polylogarithmic-in-\(n\) QLS algorithm:
such an algorithm assumes an already usable matrix oracle.  The theorem lower
bounds constructing or bypassing that oracle from the normalized iterate
state.

## When per-iteration costs add

The single-transition theorem has a clean direct-sum consequence in an online
interface.  Stating the causality assumptions is essential.

### Online fresh-oracle interface

For rounds \(t=1,\ldots,T\):

1. After all outputs from earlier rounds have been committed, an adversary
   chooses a fresh bit \(b_t\), independent of the algorithm's current
   workspace.
2. The algorithm receives controlled black-box access to a new pair
   \(U_{t,b_t},U_{t,b_t}^\dagger\).  Its prepared state is the corresponding
   vector in (17), and its off-zero action is the close minimum-rotation
   extension.  Future round oracles are unavailable.
3. Before round \(t+1\), the algorithm must either:
   - prepare a state satisfying (22) for the system (19); or
   - after \(S_t\) one-time setup queries, expose a reusable controlled
     \((\alpha_t,a,\eta/8)\)-block encoding of \(D_{b_t}\), with a reported
     bound \(\alpha_t\leq A_t\).  One invocation of the resulting circuit may
     make another \(q_t\) calls to the state oracle.

Arbitrary persistent quantum memory, prior measurement results, and classical
randomness are allowed.  They are independent of the newly selected bit.

### Theorem 2 (online additive lower bound)

If the per-round trace-distance or block-encoding guarantee above holds for
the output channel, every fixed worst-case round-query budget satisfies

\[
 \sum_{t=1}^T Q_t=\Omega(T\sqrt n)
\tag{24}
\]

for next-solution-state output.  For the reusable diagonal compiler,

\[
 \sum_{t=1}^T (\eta S_t+q_tA_t)=\Omega(T\sqrt n).
\tag{25}
\]

The setup may produce classical data or persistent quantum advice.  If the
advice is consumed by an invocation, the cost of preparing enough copies is
part of \(S_t\).  A consumer resolving the \(\eta\)-sized diagonal difference
makes \(\Theta(A_t/\eta)\) controlled calls, so its total state-oracle cost is

\[
 S_t+\Theta(q_tA_t/\eta).
\]

For a fixed short-step constant \(\eta\), (25) is equivalently
\(\sum_t(S_t+q_tA_t)=\Omega(T\sqrt n)\).

#### Proof

Condition on the complete workspace and transcript at the start of round
\(t\).  By the fresh-bit condition this side information is independent of
\(b_t\), so it can be included as a fixed ancilla in the proof of Theorem 1.
That theorem gives \(Q_t=\Omega(\sqrt n)\).  The scaled version of the
normalization--query proof, using (17) and block error \(\eta/8\), gives
\(\eta S_t+q_tA_t=\Omega(\sqrt n)\): run the setup once, then estimate the
first encoded entry to \(O(\eta/A_t)\) using \(O(A_t/\eta)\) block-encoding
calls.  This distinguisher makes
\(S_t+O(q_tA_t/\eta)\) state-oracle calls, whereas the close oracles require
\(\Omega(\sqrt n/\eta)\).  Summing the conditional round bounds proves
(24)--(25).  \(\square\)

A heralded probabilistic compiler obeys the same conclusion after conditioning
on a success flag whose probability is bounded below, with the query cost
charged per successful invocation.  An unheralded constant failure probability
is not covered when \(\eta\) tends to zero, because it can exceed the
\(\Theta(\eta)\) separation of the target states.

The oracle ledger for (24)--(25) is as follows.

- The atomic charged operations are controlled calls to the current
  \(U_{t,b_t}\) and its inverse.  Gate complexity is not lower-bounded.
- The common norm \(\sqrt n\), the two possible vector formulas, \(r\), and the
  round number are free.  The hidden information is only \(b_t\).
- No coordinate-value, QRAM, objective-coefficient, or already compiled matrix
  oracle is available.  Any one of these can reveal the known exceptional
  coordinate in one query.
- The full off-zero action is part of the oracle promise: the adversary may use
  the close minimum-rotation completions.  Merely specifying
  \(U|0\rangle\) would not be enough for a query lower bound.
- One-time compiler setup, including reusable advice, is charged through
  \(S_t\); per-invocation oracle use is charged through \(q_t\).  Omitting
  either term creates an immediate amortization loophole.
- The output is required before access to the next fresh oracle.  This is the
  causality assumption that makes the conditional per-round bounds additive.

The hard iterate stream is compatible with positivity, equal norms, and a
coordinatewise short-update promise.  Indeed, for any two consecutive choices
in (17),

\[
 |v^{(b_{t+1})}_i-v^{(b_t)}_i|
 \leq\eta v^{(b_t)}_i
 \qquad\text{for every }i.
\]

For the first coordinate this is immediate.  For the other coordinates, it
follows from \(\beta_\eta\geq1/(1+\eta)\), which holds for \(n\geq4\).
Therefore positivity and short relative motion alone do not invalidate the
online direct sum.

### Exact obstruction to a fixed-instance QIPM lower bound

Theorem 2 is a rigorous iterative-interface theorem, but it is not yet an
end-to-end lower bound for solving one fixed LP.  The missing step is not a
minor technicality:

1. **Freshness is stronger than a fixed optimization instance.**  In a QIPM,
   every iterate and Newton circuit is ultimately determined by one static
   input oracle and the preceding computation.  A new independent oracle is
   not supplied after each committed output.
2. **The one-vector theorem is worst-case, not automatically direct-sum.**  If
   all iterates depend on one hidden bit, the algorithm can learn it once and
   hard-code every later diagonal.  Reapplying the single-step theorem would
   double-count the same information.
3. **Circuit generation must be expanded to atomic queries.**  A circuit for
   \(U_{x_{t+1}}\) may call \(U_{x_t}\), which itself contains the entire prior
   history.  Treating each as a unit-cost primitive hides multiplicative
   inlining; charging both as independent primitives double-counts it.
4. **Off-zero leakage is model dependent.**  The lower bounds choose clean,
   close extensions adversarially.  An actual QLS implementation may expose
   coordinate values or trajectory information in its action away from
   \(|0\rangle\).  A fixed-input theorem must specify the complete solver
   oracle, not only its prepared state.
5. **All-round coherent access changes the direct-sum problem.**  If every
   time-indexed oracle is available through one multiplexed query, the causal
   proof of (24) fails.  A separate adversary/direct-sum theorem would be
   required, and still would not show that such an oracle family is generated
   by a sparse LP trajectory.
6. **The QIPM equations may permit a bypass.**  Equations (19)--(23) prove
   hardness for a changing sparse diagonal solve, but not that these systems
   occur as consecutive Newton systems of one fixed sparse LP.  Algebraic
   cancellation, a scale-free formulation, or a direct history-state
   algorithm could avoid separately compiling \(X_t,S_t\), or \(X_tS_t^{-1}\).
7. **The output contract matters.**  The theorem applies to an architecture
   that exposes a reusable diagonal or a next Newton solution state every
   round.  An algorithm that analytically guarantees a fixed step and only
   emits one final observable need not satisfy this interface.

Consequently, a genuine fixed-LP \(\Omega(T\sqrt n)\) theorem needs an explicit
family with \(T\) independent hard pieces embedded in one sparse instance, a
proof that its prescribed IPM trajectory reveals one piece per round, and a
direct-sum lower bound against queries to the *static input oracle*.  No such
embedding is proved here.  Claiming an unconditional iteration multiplier
from (1) alone would be incorrect.

## Error ledger for coherent diagonal updates

Suppose

\[
 \||\widetilde v\rangle-|v/\nu\rangle\|_2\leq\xi,
 \qquad
 |\widetilde\nu-\nu|\leq\delta_\nu.
\]

The amplitude-to-diagonal lifting has absolute operator error at most

\[
 \delta_\nu+\widetilde\nu\xi.
\]

For coherent LCU updates \(X_{t+1}=X_t+h_t\Delta_t\), absolute errors satisfy

\[
 E_T\leq E_0+
 \sum_{t<T}|h_t|
 \bigl(\delta_{\nu,t}+\widetilde\nu_t\xi_t\bigr).
\tag{26}
\]

Thus late-path positivity or centrality forces the cumulative weighted
state-preparation error, not merely each local error, below the final
\(O(\mu_T)\) margin.

Literal circuit reuse also nests.  If preparing the next direction takes
\(Q_t\) calls to the current-iterate circuit, then direct inlining yields
\(C_{t+1}=\Theta((1+Q_t)C_t)\).  This is an accounting statement for the
literal composition model, not a universal lower bound; structured direct
oracles and history-state methods lie outside it.

## Literature boundary

- Rattew and Rebentrost, *Non-Linear Transformations of Quantum Amplitudes*,
  arXiv:2309.09839, Theorem 2, prove the matching amplitude-diagonal upper
  construction: https://arxiv.org/abs/2309.09839
- Mitarai, Kitagawa, and Fujii, *Quantum Analog-Digital Conversion*,
  arXiv:1805.11250, gives related inverse-precision analog-to-digital methods:
  https://arxiv.org/abs/1805.11250
- Guo, Mitarai, and Fujii, *Nonlinear transformation of complex amplitudes via
  quantum singular value transformation*, arXiv:2107.10764, is an earlier
  state-amplitude block-encoding construction:
  https://arxiv.org/abs/2107.10764
- Ozols, Roetteler, and Roland, *Quantum rejection sampling*,
  arXiv:1103.2774, gives tight bounds for a different amplitude-rescaling task:
  https://arxiv.org/abs/1103.2774
- Arihara and Murao, *Sample-Query Interconversion of Block Encoding of Unknown
  Quantum States*, arXiv:2608.22470, Theorem 3 proves an
  \(\Omega(1/\epsilon)\) copy lower bound for implementing one use of an
  unknown density matrix's block-encoding channel.  Theorem 4 proves that
  recovering a rank-\(r\), \(d\)-dimensional state from an
  \((\alpha,a,0)\) block encoding takes
  \(\Omega((\alpha/\lambda_{\max})\sqrt{d/r})\) queries.  These are the
  copy-to-density-block-encoding and block-encoding-to-state directions, not
  the coherent amplitude-to-diagonal conversion studied here:
  https://arxiv.org/abs/2608.22470
- Rempfer, Kuklinski, Elenewski, and Obenland, *Harmonic sequence
  state-preparation*, arXiv:2602.23664, build a diagonal harmonic block
  encoding from an analytic circuit.  Their comparison notes the poor
  subnormalization obtained by a generic direct state-to-diagonal route, but
  gives no worst-case query--normalization lower bound:
  https://arxiv.org/abs/2602.23664
- Tang, Wright, and Zhandry, *Conjugate queries can help*, arXiv:2510.07622,
  show that \(q\) forward/inverse state-preparation queries can generally be
  simulated with \(O(q^2/\epsilon)\) copies.  This explains the quadratic
  query-versus-copy boundary but does not state (1) or (8):
  https://arxiv.org/abs/2510.07622
- Wang and Zhang, *Quantum Lower Bounds by Sample-to-Query Lifting*,
  arXiv:2308.01794, and Chen, Wang, and Zhang's 2025 follow-up compile the
  general quadratic sample/query lifting technique used by many property-test
  lower bounds.  They do not contain the compiler tradeoff or the
  strict-complementary LP embedding:
  https://arxiv.org/abs/2308.01794
  and https://arxiv.org/abs/2512.01971
- Lee, Mittal, Reichardt, Spalek, and Szegedy, *Quantum query complexity of
  state conversion*, arXiv:1011.3020, gives the general adversary framework
  for converting input-dependent state families.  Theorem 1 above is a simple
  two-input hybrid specialization with a QIPM diagonal-solve target:
  https://arxiv.org/abs/1011.3020
- Suruga, *Direct sum theorems beyond query complexity*, arXiv:2408.15570,
  studies general amortized/direct-sum questions, but its advertised quantum
  result restricts each oracle access to be classical.  It therefore does not
  supply the missing direct sum for coherent multiplexed time-indexed iterate
  oracles: https://arxiv.org/abs/2408.15570
- Apers and Gribling, *Quantum Speedups for Linear Programming via Interior
  Point Methods*, prove LP lower bounds in coefficient row-query and
  sampling-and-query models.  Those results use constant-gap discrete inputs;
  they do not state the equal-norm objective-state, inverse-\(\mu\) precision
  lower bound (14)--(16):
  https://doi.org/10.1137/25M1736098
- Kerenidis and Prakash, arXiv:1808.09266, and Augustino, Nannicini, Terlaky,
  and Zuluaga, arXiv:2112.06025, reconstruct classical SDP directions from
  QLS states and analyze inexact-IPM convergence.  They do not prove a lower
  bound for reusing a Newton state as a coordinate-sensitive iterate oracle:
  https://arxiv.org/abs/1808.09266
  and https://arxiv.org/abs/2112.06025

No primary source found in searches through 2026-09-02 states the product
lower bound (1), the strict-complementarity consequence (8), the
input-generated scalar-value
version (14)--(16), the fraction-to-boundary corollary, or the QIPM
state-to-next-solve and online compiler statements (17)--(25).  The theorems
are scoped to generic state-preparation access; a structured circuit or
stronger coefficient/Newton oracle may expose coordinate values by other
means.

Status: **proof complete in the stated oracle model and apparently new after a
targeted open-literature audit.**
