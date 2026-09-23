# Collision lower bounds for symmetric block-resource states

Date: 2026-09-02

Status: proof-complete standalone interface theorem.  Its strongest version is
also incorporated into 2026-09-02-general-block-logdet-condensation.md.

## Main theorem

This note isolates the state-output argument behind the winner-take-all
central-path example.  There are \(G\) independently queried input blocks.
Each block has a Boolean winner predicate \(f\), and the input is promised to
have either no winner or exactly one winner.  Suppose a target density state
has a public component register with these properties:

1. on a no-winner input, the component marginal is uniform;
2. on a unique-winner input, the winning component has probability at least
   \(p\).

No symmetry among the losing components is required.  Two independent
component measurements collide with probabilities \(c_0,c_1\) satisfying

\[
 c_0={1\over G},\qquad
 c_1\ge p^2+{(1-p)^2\over G-1},qquad
 c_1-c_0\ge{(Gp-1)^2\over G(G-1)}.                         \tag{1}
\]

If each prepared state has trace error at most \(\epsilon\), the observable
gap is at least the last quantity in (1) minus \(4\epsilon\).  Therefore,
whenever \(p\ge p_0>0\), \(G\ge2/p_0\), and
\(\epsilon<p_0^2/16\), a constant number of state preparations decides the
zero-versus-one-winner promise.

Let \(A=\operatorname{Adv}^{\pm}(f)\) in the same block-local raw query
model.  An explicit adversary construction gives

\[
 \operatorname{Adv}^{\pm}(\operatorname{UOR}_G\circ f^G)
                         \ge A\sqrt G.                     \tag{2}
\]

Consequently any state-preparation algorithm satisfying the two marginal
conditions and the fixed trace-error bound above uses

\[
                              \boxed{\Omega(A\sqrt G)}      \tag{3}
\]
raw queries.  Since the general adversary bound characterizes bounded-error
quantum query complexity, this is equivalently
\(\Omega(Q(f)\sqrt G)\) up to universal constants.  For
\(f=\operatorname{PARITY}_N\), it becomes \(\Omega(N\sqrt G)\).

The theorem needs neither a candidate-verification query nor access to a
coherent inverse of the state-preparation circuit.  It applies to arbitrary
mixed outputs, and to purification outputs whose reduced system states satisfy
the trace-error contract, because the decoder reads only two reduced component
registers.

## 1. Minimal state assumptions

Let \(\mathcal X_0=f^{-1}(0)\) and \(\mathcal X_1=f^{-1}(1)\).  The raw
input is

\[
 x=(x_1,\ldots,x_G)\in\mathcal X^G,
 \qquad x_g\in\mathcal X_0\cup\mathcal X_1,                 \tag{4}
\]

with the promise

\[
 \mathcal P_0=\mathcal X_0^G,
 \qquad
 \mathcal P_1=\bigsqcup_{a=1}^G
 \mathcal X_0^{a-1}\times\mathcal X_1\times
 \mathcal X_0^{G-a}.                                      \tag{5}
\]

For each valid input, let \(\rho_x\) be the target state.  Assume there are
public orthogonal projectors \(\Pi_1,\ldots,\Pi_G\), summing to the identity
on a component register, and write

\[
                              w_g(x)=\operatorname{Tr}(\Pi_g\rho_x).     \tag{6}
\]

The state theorem uses only

\[
 x\in\mathcal P_0\Longrightarrow w_g(x)=1/G,
 \qquad
 x\in\mathcal P_1\text{ with winner }a
       \Longrightarrow w_a(x)\ge p.                       \tag{7}
\]

The first implication usually follows from block-permutation symmetry and
uniqueness of the regularized optimizer or central point.  The second is a
problem-specific mass estimate.  The internal conditional states, phases,
purifying registers, and losing probabilities may otherwise depend
arbitrarily on the input.

A still weaker formulation suffices.  If the no-winner target has component
collision probability at most \(b\), replace \(1/G\) below by \(b\).  Thus
exact uniformity is a convenient symmetry certificate, not logically
necessary; the minimal output assumption is a separated collision statistic.

## 2. Collision lemma

Prepare two independent copies of \(\rho_x\), measure their component
registers, and accept when the two labels agree.  The acceptance probability
is

\[
                              c(x)=\sum_{g=1}^G w_g(x)^2.    \tag{8}
\]

On \(\mathcal P_0\), (7) gives \(c_0=1/G\).  On
\(\mathcal P_1\), fix the winning mass \(w_a=q\ge p\).  Cauchy--Schwarz on
the other \(G-1\) entries gives

\[
 \sum_{g\ne a}w_g^2\ge{(1-q)^2\over G-1}.                  \tag{9}
\]

The right side of
\(q^2+(1-q)^2/(G-1)\) is increasing for \(q\ge1/G\).  Hence, provided
\(p\ge1/G\),

\[
 c_1\ge p^2+{(1-p)^2\over G-1},
 \qquad
 c_1-c_0\ge{(Gp-1)^2\over G(G-1)}.                         \tag{10}
\]

Equality holds when all losing probabilities are equal.  Thus (10) is both
the exact symmetric formula and the worst-case bound without loser symmetry.

If \(p\ge p_0\) and \(G\ge2/p_0\), then
\(Gp-1\ge Gp_0/2\), and (10) implies

\[
                              c_1-c_0\ge{p_0^2\over4}.       \tag{11}
\]

This shows why constant winner mass, rather than detailed conditional-state
geometry, is enough for a constant decoder.

## 3. Trace-error robustness

Suppose a preparation circuit outputs \(\widetilde\rho_x\) with

\[
             D_{\rm tr}(\widetilde\rho_x,\rho_x)\le\epsilon             \tag{12}
\]

on every promised input, using the convention
\(D_{\rm tr}(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1\).
Subadditivity under tensor products gives

\[
 D_{\rm tr}(\widetilde\rho_x^{\otimes2},\rho_x^{\otimes2})
                              \le2\epsilon.                 \tag{13}
\]

Therefore the collision probability moves by at most \(2\epsilon\) under
each promise.  If the ideal collision gap is \(d\), the implemented gap is
at least

\[
                              \Delta=d-4\epsilon.            \tag{14}
\]

When \(\Delta>0\), \(O(\Delta^{-2}\log(1/\delta))\) independent collision
experiments using fresh preparations distinguish the promises with failure
probability \(\delta\).
For fixed \(p_0\) and any fixed \(\epsilon<p_0^2/16\), equations
(11)--(14) require only a constant number of state preparations.  More
quantitatively, if one preparation costs \(q\) raw queries and the decision
problem in (5) costs \(L\), then

\[
                              q=\Omega(L\Delta^2)            \tag{15}
\]

up to an absolute constant.  The useful regime in this note is constant
\(\Delta\), where (15) simply says \(q=\Omega(L)\).

The factor \(4\epsilon\) is a safe worst-case bound: two copies cost
\(2\epsilon\) under each of the two promises.  It makes no assumption about
how the output error is distributed among components.

## 4. Explicit block-composition adversary

The state reduction can use any lower bound \(L\) for (5).  For completeness,
the standard \(\sqrt G\) composition factor has a direct witness.  Let
\(B\) be the rectangular zero-to-one block of any feasible general-adversary
matrix for \(f\), normalized so that

\[
 \|B\|=A,
 \qquad
 \max_j\|B\circ\Delta_j\|\le1.                            \tag{16}
\]

Here \(\Delta_j[x,y]=1\) exactly when the answer to inner query \(j\)
differs between \(x\in\mathcal X_0\) and \(y\in\mathcal X_1\).  For the
sector of \(\mathcal P_1\) whose winner is block \(a\), define

\[
 C_a=I_0^{\otimes(a-1)}\otimes B\otimes I_0^{\otimes(G-a)},
 \qquad C=[C_1\ C_2\ \cdots\ C_G],                         \tag{17}
\]

where \(I_0\) is the identity on inputs in \(\mathcal X_0\).  Set

\[
                              \Gamma=\begin{pmatrix}0&C\\C^*&0\end{pmatrix}.
\tag{18}
\]

The unique-winner sectors are disjoint, so

\[
 CC^*=\sum_{a=1}^G I_0^{\otimes(a-1)}\otimes BB^*\otimes
                         I_0^{\otimes(G-a)}.                \tag{19}
\]

The summands commute.  A top eigenvector of \(BB^*\), tensored \(G\)
times, is a common eigenvector with eigenvalue \(A^2\) for every summand.
The triangle inequality gives the matching upper bound, and hence

\[
                              \|\Gamma\|=A\sqrt G.           \tag{20}
\]

Filter by raw query \((a,j)\).  Every unique-winner sector other than \(a\)
has an identity in block \(a\), so that sector vanishes under the filter.
In sector \(a\), (16) gives

\[
                              \|\Gamma\circ\Delta_{a,j}\|\le1.          \tag{21}
\]

Thus \(\Gamma\) is feasible with adversary value at least \(A\sqrt G\),
proving (2).  This proof permits signed or complex adversary weights and
partial inner predicates.  It requires only the Cartesian block-local query
model in (4)--(5).

By tightness of the general adversary bound,
\(A=\Theta(Q(f))\) for bounded-error quantum query complexity.  Combining
(15) and (20)--(21) proves the main theorem.

## 5. Minimal oracle-hardness assumptions

The precise assumptions needed for the \(\Omega(Q(f)\sqrt G)\) conclusion
are:

1. **Independent input blocks.**  All tensor-product inputs in (5) are valid.
2. **Block-local queries.**  One raw query addresses one coordinate of one
   block, coherently over addresses.  It does not return an aggregate of
   several blocks.
3. **A hard local predicate.**  Both fibers of \(f\) are nonempty and
   \(\operatorname{Adv}^{\pm}(f)=A\).  The predicate may be partial.
4. **A public component measurement.**  The projectors in (6) do not depend
   on the hidden input.
5. **Separated target marginals.**  The no-winner collision is small and the
   unique winner receives enough target mass to make (14) positive after
   output error.

No clean coherent evaluator for \(f\) is needed for the lower bound.  Such
an evaluator is relevant only to a matching Grover upper bound.  No promise
is needed about the target state's internal block matrices or about equal
loser masses.  No inverse state-preparation oracle, postselection, or
candidate verification is used.

For an optimization coefficient oracle, one must additionally state its
simulation cost in the raw block oracle.  If one coefficient query is
simulated by at most \(s\) raw queries, (3) becomes
\(\Omega(A\sqrt G/s)\) coefficient queries.  In the fixed-position XOR
access of the holonomy SDP, \(s=1\), including inverse and controlled calls.
Supplying the winner bits, a winner phase oracle, or an input-dependent
component projector at unit cost changes the model and removes the inner
factor \(A\).

## 6. Optimization corollary

Consider any block-symmetric resource problem with one public budget, for
example

\[
 \min\left\{\sum_g F_{x_g}(Z_g): Z_g\in\mathcal K,
                         \sum_g\ell(Z_g)=1\right\},          \tag{22}
\]

and let \(\rho_x(\tau)\) be a regularized optimizer, barrier center, or other
canonical primal density.  Suppose uniqueness plus symmetry makes its
no-winner resource marginal uniform, while a unique lower-cost block has
mass at least \(p_0\) at the parameter \(\tau\).  Then any fixed-error
preparation of \(\rho_x(\tau)\), with error below \(p_0^2/16\), has raw
query complexity

\[
                              \Omega(Q(f)\sqrt G).           \tag{23}
\]

This conclusion is independent of the Hessian condition number.  A separate
problem-specific analysis is needed to prove winner mass, conditioning, and
the coefficient-to-raw access normalization.

For the global-trace holonomy SDP, \(f=\operatorname{PARITY}_N\),
\(Q(f)=\Theta(N)\), and the exact resolvent calculation gives winner mass at
least \(3/4\) when \(\tau\le1/(90G)\).  Taking \(p_0=3/4\) yields trace
tolerance below \(1/32\) and the \(\Omega(N\sqrt G)\) theorem.  Moving to
\(\tau\le1/(135G)\) gives \(p_0=5/6\), for which trace error \(1/20\)
still leaves a collision gap \(1/45\).

## 7. Scope and novelty

The collision identity is the classical second moment of a categorical
distribution, and the adversary construction is the standard unique-search
composition mechanism.  Neither is new.  The useful contribution is a
compact interface theorem: a problem-specific winner-mass estimate plus a
local-predicate adversary bound automatically yields a trace-robust quantum
state-preparation lower bound, without inspecting the conditional state or
paying to verify a sampled winner.

The theorem does not say that every symmetric optimization problem has a
condensed regularized state.  It also does not provide a lower bound when
the target error is comparable to the winner mass, when the no-winner
marginal is already concentrated, or when queries aggregate many blocks.
Those are failures of the stated reduction, not evidence that preparation is
easy.

The general adversary bound and its tightness are prior work; relevant
primary sources are Høyer, Lee, and Špalek,
[*Negative weights make adversaries stronger*](https://arxiv.org/abs/quant-ph/0611054),
and Reichardt,
[*Reflections for quantum query algorithms*](https://arxiv.org/abs/1005.1601).
The exact holonomy instantiation and its condensation law are in
`2026-09-02-winner-central-path-condensation.md`.
