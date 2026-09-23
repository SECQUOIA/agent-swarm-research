# A bounded-degree treewidth-one simplex central path with a Grover-hard coordinate

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the construction and query bounds; moderate on novelty

## Main point

Low treewidth dequantizes a Newton solve once its current numerical entries and
right-hand side are available.  It does **not** by itself dequantize a compressed
central-path or optimizer output, because constructing the current iterate
interface may already contain an unstructured-search problem.

For every power of two \(N\geq4\), the family below is an extended
formulation of a simplex LP with:

- \(O(N)\) nonzeros and coefficients in \(\{-1,0,1\}\);
- a public strictly feasible analytic center;
- a standard logarithmic-barrier KKT graph that is itself a tree, with every
  row and column incident to at most three nonzeros;
- a unique optimizer whose leaf vector \(x^*=e_j\) is one-sparse; and
- one bounded central-path coordinate whose matched-access query complexity is

\[
 \boxed{Q=\Theta(\sqrt N),\qquad R=\Theta(N).}             \tag{1}
\]

The bounds survive canonical full sample-and-query access to the hidden
objective: its norm and squared-coordinate distribution are public, and its
state-preparation oracle is just one use of the usual phase oracle.  The same
bounds hold for compiling an offline exact SQ interface to the selected
central point.  This is a sharp counterexample to the claim that low latent
treewidth and linear total sparsity alone imply dimension-independent
classical query complexity for a compressed central-path or optimizer target.
Equivalently, it obstructs any structural QIPM-dequantization argument based
only on those two graph parameters.

For the displayed logarithmic barrier \(\nu=N\), so (1) is equivalently the
sharp law \(Q=\Theta(\sqrt\nu)\), \(R=\Theta(\nu)\) for this one
constant-accuracy path coordinate.  This is a total-query statement; it does
not assign one independent query instance to each short step.

The construction gives only Grover's quadratic query separation, not a new
quantum path-following algorithm.  A full dense classical iterate still costs
\(\Theta(N)\) writes, and classical low-treewidth elimination solves each
Newton system in \(O(N)\) arithmetic.  The novelty candidate is the exact
central-path, treewidth, full-SQ, and dynamic-interface combination.

## LP and access model

Let \(H\subset[N]\) be the public left half of the leaves of a balanced
binary tree, and let \(j\in[N]\) be the unique hidden marked index.  Put

\[
 c_i^{(j)}=1-2\mathbf 1\{i=j\},\qquad
 h_i=\mathbf 1\{i\in H\}.                                \tag{2}
\]

Introduce one variable \(s_v\) at every internal node of the tree, put
\(s_i=x_i\) at a leaf, and impose the public three-sparse summation equations

\[
 s_v=s_{v_L}+s_{v_R}                                      \tag{3a}
\]

at all internal nodes, together with \(s_{\rm root}=1\).  Designate the
left child of the root as

\[
 p=s_{{\rm root},L}.                                      \tag{3b}
\]

The LP is

\[
 \begin{array}{ll}
 \text{minimize}   & (c^{(j)})^Tx\\
 \text{subject to} & \text{the tree equations (3a),}\quad
                     s_{\rm root}=1,\quad x\geq0.
 \end{array}                                                \tag{3}
\]

The internal variables are free equality variables and are uniquely
determined as subtree sums.  Hence this formulation projects exactly onto
\(\mathbf1^Tx=1,x\geq0\), and \(p=h^Tx\in[0,1]\) is now a literal scalar
coordinate rather than a dense output functional.  The point \(x_i=1/N\),
with the corresponding public subtree sums and \(p=1/2\), is strictly
feasible in the relative interior.  The unique optimizer is

\[
 x^*=e_j,\qquad p^*=h_j\in\{0,1\}.                       \tag{4}
\]

The internal variables at the optimizer are the zero--one indicators of
subtrees containing \(j\).  Thus the full lifted optimizer has
\(O(\log N)\) nonzeros, and \(j\) compactly specifies all of them.

The raw input oracle is the usual marked-item oracle, equivalently coordinate
queries to \(c^{(j)}\).  We also allow canonical full SQ access to the
objective:

1. \(\|c^{(j)}\|_2=\sqrt N\) is public;
2. squared-coordinate sampling is public uniform sampling; and
3. canonical coherent preparation produces

\[
 |c^{(j)}\rangle={1\over\sqrt N}\sum_i c_i^{(j)}|i\rangle.
                                                               \tag{5}
\]

Preparation of (5), and its inverse, use one marked-item phase query and
public Hadamards.  Thus every allowed full-SQ call is simulated by \(O(1)\)
ordinary search queries.  The constraint matrix, \(h\), all dimensions, and
all norms and sampling distributions are public.  An arbitrary unitary
completion that hides extra information outside the specified preparation
subspace is not part of the interface.

## Exact logarithmic central path

For objective multiplier \(\eta>0\), minimize

\[
 \eta(c^{(j)})^Tx-\sum_{i=1}^N\log x_i
 \quad\text{over}\quad \mathbf1^Tx=1.                    \tag{6}
\]

By symmetry, write the marked coordinate as \(a\) and every unmarked
coordinate as \(b\).  The KKT equations give, for a scalar \(\lambda\),

\[
 a={1\over\lambda-\eta},\qquad
 b={1\over\lambda+\eta},\qquad a+(N-1)b=1.              \tag{7}
\]

More generally, prescribe any marked mass
\(\theta\in(1/N,1)\).  Equations (7) are solved by

\[
 a=\theta,\qquad b={1-\theta\over N-1},\qquad
 \eta(\theta)={N\theta-1\over2\theta(1-\theta)}.          \tag{7a}
\]

At this point the ordinary primal objective gap and readout are exactly

\[
 (c^{(j)})^Tx(\eta(\theta))+1=2(1-\theta),
 \qquad
 p_j(\eta(\theta))={1\over2}\mathbin\pm
 {N\theta-1\over2(N-1)},                                  \tag{7b}
\]

where the plus sign holds for \(j\in H\).  Thus every fixed
\(\theta\in(0,1)\), for all sufficiently large \(N\), gives a constant
readout gap while still lying at a constant additive objective-accuracy
scale.  The particularly simple choice below fixes \(\theta=1/2\).

At the public path parameter

\[
 \eta_0=N-2                                                   \tag{8}
\]

one has \(\lambda=N\) and therefore

\[
 \boxed{a={1\over2},\qquad b={1\over2(N-1)}.}             \tag{9}
\]

Consequently the designated coordinate at this *one fixed path point* is

\[
 p_j(\eta_0)=
 \begin{cases}
 \displaystyle {3N-4\over4(N-1)},&j\in H,\\[4pt]
 \displaystyle {N\over4(N-1)},&j\notin H.
 \end{cases}                                                \tag{10}
\]

The two values lie symmetrically around \(1/2\), at distance

\[
 \Delta_N={N-2\over4(N-1)}\geq{1\over6}.                 \tag{11}
\]

Thus additive error at most \(1/8\) in one bounded central-path coordinate
decides whether the marked index lies in the public half \(H\).

This remains true for a feasible conventional local-norm approximate center,
whose lifted coordinates obey the tree equations.  At (9), let

\[
 D=\nabla^2\!\left(-\sum_i\log x_i\right)
   =\operatorname{diag}(x_i^{-2}).                         \tag{12}
\]

If \(\|\widetilde x-x(\eta_0)\|_D\leq1/8\), then

\[
 |h^T(\widetilde x-x)|
 \leq {1\over8}\sqrt{h^TD^{-1}h}
 \leq {1\over8}\|x\|_2
 = {1\over16}\sqrt{N\over N-1}< {3\over40}.             \tag{13}
\]

Combining (11)--(13), thresholding \(h^T\widetilde x\) at \(1/2\) still
recovers the correct half.  Constants are deliberately loose.

Consequently every path-following implementation which reaches this
\(1/8\)-local neighborhood and exposes the literal coordinate \(p\) obeys
the same total raw-query lower bounds below.  This is a whole-run lower
bound, not a claim that separate Newton iterations contain independent
hidden inputs.

## Query theorem

### Theorem 1

Under the raw coefficient oracle or the canonical full-SQ interface above,
estimating either \(p_j(\eta_0)\) to additive error \(1/8\), or \(p^*\) to
additive error less than \(1/3\), has bounded-error query complexities

\[
 Q=\Theta(\sqrt N),\qquad R=\Theta(N).                    \tag{14}
\]

The same lower bounds apply to returning an exactly feasible
\(\widehat x\) with objective gap less than \(1/2\), under an output contract
from which the half containing its heavy leaf can be recovered without
further hidden-input queries.  This includes an explicit classical leaf
vector or its heavy-coordinate sparse description.  Indeed,

\[
 (c^{(j)})^T\widehat x-(c^{(j)})^Tx^*
 =2(1-\widehat x_j)<{1\over2}                             \tag{15}
\]

implies \(\widehat x_j>3/4\).  Hence
\(h^T\widehat x>3/4\) when \(j\in H\), whereas
\(h^T\widehat x<1/4\) when \(j\notin H\).

#### Proof

Every stated output distinguishes the partial Boolean function

\[
 f(j)=\mathbf1\{j\in H\}                                  \tag{16}
\]

on unique-mark search inputs.  A classical randomized algorithm needs
\(\Omega(N)\) queries.  For example, under the uniform distribution on
\(j\), until a query hits \(j\) all answers are identical; querying \(q\)
locations can improve success over the best half-guess by at most \(q/N\).
Constant advantage therefore requires \(q=\Omega(N)\).

The quantum lower bound is \(\Omega(\sqrt N)\).  One may apply the standard
adversary relation joining every marked location in \(H\) to every marked
location outside \(H\).  Each related input pair differs in two oracle
positions; the all-ones relation has norm \(N/2\), while restricting it to
one queried position gives norm \(\sqrt{N/2}\).  The adversary ratio is
\(\Omega(\sqrt N)\).  This is the usual unique-search lower bound with only
the half-membership of the marked location requested.

Grover search finds \(j\) in \(O(\sqrt N)\) queries, after which (10) or
(4) is returned exactly.  A classical scan gives the \(O(N)\) upper bound.
The full-SQ simulation following (5) transfers both lower bounds to the
stronger matched interface.  This proves (14). \(\square\)

### Corollary 1A (free-linear-algebra QIPM query lower bound)

In the raw coefficient-query model, Theorem 1 is an unconditional total-query
lower bound for every algorithm which exposes the stated path coordinate,
including a QIPM.  It remains valid if the width-one tree decomposition is
supplied and all inter-query computation, exact arithmetic, and exact solution
of every *explicitly and fully numerically instantiated* Newton
matrix--right-hand-side pair are free.  Every raw query used to instantiate a
hidden entry remains charged; a solver that itself accepts a lazy objective
oracle would be a different access model.  Query complexity already grants
arbitrary input-independent computation between oracle calls, so these
additions cannot weaken the search reduction.

What cannot be supplied for free without changing the input model is an
oracle for the hidden numerical center, its Hessian/scaling, or a
mark-adapted preconditioner.  At (9), any of these interfaces may itself
reveal \(j\), as the current-iterate section below makes explicit.

Since the displayed barrier has \(\nu=N\), constant-accuracy evaluation of
this one central-path coordinate requires

\[
 \boxed{\Omega(\sqrt\nu)\ \text{quantum raw queries},\qquad
        \Omega(\nu)\ \text{randomized raw queries}.}      \tag{14a}
\]

The Grover upper bound makes (14a) tight for the abstract coordinate task.
Its \(\sqrt\nu\) dependence matches the characteristic square-root barrier
factor in standard short-step outer bounds, up to their separate logarithmic
progress factor.  This is **not** an iteration lower bound: one query can be
used coherently across all coordinates, iterations need not carry independent
inputs, and no \(O(\sqrt\nu)\)-query QIPM is constructed here.

### Corollary 2 (no width-and-degree-only scalar dequantization)

There is no generic classical algorithm for a constant-accuracy central-path
coordinate whose coefficient-query complexity is
\(\operatorname{poly}(\tau,d,\log N)\), where \(\tau\) is the treewidth and
\(d\) is the maximum off-diagonal degree of the structural augmented KKT
graph (equivalently here, the maximum matrix row/column sparsity), even with
a supplied tree decomposition and full SQ access to every raw input vector.
The family above has \((\tau,d)=(1,3)\) and needs \(\Omega(N)\)
classical queries.  A valid positive theorem cannot omit every
conditioning, numerical-dynamic-range, raw-input-aggregation, and
current-iterate-oracle construction term.

## The current-iterate oracle is exactly where the hardness moves

At (9),

\[
 \|x(\eta_0)\|_2^2={N\over4(N-1)},
 \qquad
 \Pr_{I\sim |x_i|^2/\|x\|^2}[I=j]={N-1\over N}.           \tag{17}
\]

Therefore one squared-coordinate sample from an already constructed exact
\(SQ(x(\eta_0))\) interface reveals the marked index with probability
\(1-1/N\).  Here an **offline exact SQ compiler** must return an interface
whose later norm, coordinate, sample, and state-preparation calls make no
further raw marked-item queries; equivalently, one may charge compilation
together with its first downstream interface use.  Without this convention,
a zero-query lazy wrapper makes a preprocessing-only claim vacuous.  Under
this convention, appending one sample proves that compilation needs
\(\Omega(\sqrt N)\) quantum or \(\Omega(N)\) randomized input queries.

The bounds are tight.  Grover search or a classical scan first finds \(j\);
then the public values in (9) give an exact constant-size description of
every coordinate and of the squared-coordinate distribution, with no further
raw queries.  Exact offline SQ compilation therefore also has complexities
\(\Theta(\sqrt N)\) and \(\Theta(N)\).  No approximate-interface claim is
made without a total-variation or trace-distance contract.
The conclusion is even more immediate for an SQ/coordinate interface to the
full extended iterate: one query to its literal coordinate \(p\), at constant
precision, decides (16).

This gives a precise access-fairness warning.  Granting the QLSA or a
quantum IPM a free oracle for the current nonlinear iterate erases the cost
that carries all the hardness on this family.  Low-treewidth elimination
only applies after those numerical entries have been formed.

The statement also separates output contracts:

- the endpoint leaf optimizer has the one-word sparse description \((j,1)\),
  and \(j\) also specifies its \(O(\log N)\) nonzero lifted subtree sums, so
  compact output itself does not force \(\Omega(N)\) quantum work;
- a dense length-\(N\) iterate has an \(\Omega(N)\) write floor and the usual
  full-output no-advantage theorem applies; and
- the one scalar \(p\) retains exactly the Grover separation.

## Treewidth and Newton structure

The scalar log-barrier Hessian is diagonal on the leaf variables \(x_i\) and
zero on the internal free equality variables.  Make one KKT vertex for every
primal variable and one for every tree equation.  An internal-equation vertex
is adjacent only to its parent variable and two child variables.  An internal
variable is adjacent only to the equation in which it is a parent and the
equation in which it is a child; a leaf is adjacent only to its parent
equation.  The root-fixing equation is one additional leaf.

The resulting incidence/KKT graph is connected and has

\[
 (2N-1)+N=3N-1\quad\text{vertices},\qquad
 3(N-1)+1=3N-2\quad\text{edges}.                          \tag{18}
\]

It is acyclic by the parent--child orientation, hence it is exactly a tree.
The diagonal Hessian entries add no graph edges.  Thus the actual augmented
Newton graph has treewidth one, maximum degree three, and \(O(N)\) nonzeros,
including the literal readout coordinate \(p\).

The equation matrix has full row rank.  In a linear dependence among its
rows, each leaf column first forces the coefficient of its parent equation
to vanish; induction toward the root kills every tree-equation coefficient,
and the root column then kills the root-fixing coefficient.  Moreover the
barrier Hessian is positive on the equality nullspace: if all leaf
components vanish, the homogeneous tree equations force every internal
component to vanish.  Hence the equality KKT matrix is nonsingular despite
the zero Hessian on the free internal variables.

A supplied width-one decomposition therefore gives an \(O(N)\)-arithmetic
exact Newton solve by low-treewidth Gaussian elimination.  Here treewidth one
refers to the ordinary structural graph of the symmetric KKT matrix.  The
row--column bipartite graph used by the exact elimination theorem is obtained
by doubling every bag, so it also has constant width and linear size.  This is
fully consistent with Theorem 1: linear work is optimal classically for discovering
the hidden coefficient, while quantum search uses \(\Theta(\sqrt N)\)
queries for the compressed task.  The hard operation is not numerical fill;
it is constructing the input-dependent current iterate or its scalar output.

At the analytic center \(x_i=1/N\), the positive leaf Hessian block is
\(N^2I\) and hence has condition number one after public scaling.  At the
revealing point (9), this leaf block has diagonal condition number
\((N-1)^2\).  After eliminating the tree variables, the feasible leaf
tangent is \(S=\mathbf1^\perp\), and the reduced Hessian has condition
exactly \(N-1\).  In fact this growth cannot be removed uniformly by any
public input-independent congruence preconditioner.

### Theorem 3 (input-oblivious two-sided preconditioning is insufficient)

Let \(G_j\) be the barrier Hessian at (9), restricted to \(S\), with an
irrelevant factor four removed.  For every pair of invertible maps
\(L,R:S\to S\) that is common to all marked indices,

\[
 n=N-1,\qquad
 t_N=n+{2n-1\over n^3},\qquad
 \tau_N={t_N+\sqrt{t_N^2-4}\over2}.                       \tag{19a}
\]

Then

\[
 \boxed{\max_j\kappa_2(LG_jR)\geq\tau_N\geq N/2.}        \tag{19}
\]

Here \(\kappa_2\) is the singular-value condition number.  Taking
\(L=R=I\) gives \(\kappa_2(G_j)=N-1\), so the minimax order
\(\Theta(N)\) is sharp.

#### Proof

Put \(\rho=(N-1)^2=n^2\), let \(\Pi_S\) be orthogonal projection onto \(S\), and
write

\[
 u_j=\Pi_Se_j=e_j-{1\over N}\mathbf1,qquad
 \|u_j\|^2={N-1\over N}.
\]

As an operator on \(S\),

\[
 G_j=\rho I_S-(\rho-1)u_ju_j^T.                            \tag{20}
\]

It has eigenvalue \(n=N-1\) along \(u_j\) and eigenvalue \(\rho=n^2\) on
\(u_j^\perp\cap S\), proving \(\kappa(G_j)=N-1\).

For \(j\ne k\), the subspace \(u_j^\perp\cap u_k^\perp\cap S\) has
dimension \(n-2\), and \(G_kG_j^{-1}\) is the identity there.  The two
remaining eigenvalues have product one because \(\det G_j=\det G_k\).
Using

\[
 G_j^{-1}={1\over n^2}I_S+
 \left({1\over n}-{1\over n^2}\right)
 {u_ju_j^T\over\|u_j\|^2},
\]

and \(u_j^Tu_k=-1/N\), direct tracing gives

\[
 \operatorname{tr}(G_kG_j^{-1})
 =2n-2+{2n-1\over n^3}.                                   \tag{21}
\]

After subtracting the \(n-2\) unit eigenvalues, the last two therefore have
sum \(t_N\) and product one.  They are exactly
\(\tau_N,\tau_N^{-1}\), so the positive generalized eigenvalues of the pair
have modulus ratio \(\tau_N^2\).

Put \(A_\ell=LG_\ell R\).  Then
\[
 A_kA_j^{-1}=L(G_kG_j^{-1})L^{-1},
\]
so its eigenvalues are those generalized eigenvalues.  For every invertible,
possibly nonsymmetric matrix \(M\),
\[
 \kappa_2(M)\geq
 {\max_\lambda|\lambda(M)|\over\min_\lambda|\lambda(M)|};
\]
indeed, evaluate \(\|Mv\|\) on normalized eigenvectors for the largest and
smallest eigenvalue moduli.  Therefore
\[
 \tau_N^2\leq\kappa_2(A_kA_j^{-1})
 \leq\kappa_2(A_k)\kappa_2(A_j).
\]
At least one of these two conditions is at least
\(\tau_N\).  Finally \(\tau_N\geq N/2\) follows, for example, from its
generalized Rayleigh quotient at \(u_j\), which is
\((N-1)-(N-2)/(N-1)^2\geq N/2\).  This proves (19). \(\square\)

Theorem 3 does not say that an input-dependent preconditioner is impossible,
or that a useful one must identify \(j\) exactly.  It says that no single
input-oblivious square invertible two-sided linear preconditioner uniformly
removes the reduced-SPD conditioning in Euclidean norm.  It does not cover
\(j\)-dependent or adaptive maps, nonlinear or rectangular
preconditioning, deflation, a variable metric, or the full indefinite KKT
system.  Theorem 1 separately charges the raw queries needed to extract the
requested central scalar or build its iterate interface.  The full primal
Hessian is singular on the free internal variables; no full-KKT condition
number is claimed.  The standard product log barrier has parameter \(N\).

Because \(L,R\) are arbitrary common invertible maps, (19) is stronger than
a failure of diagonal scaling or SPD congruence: it rules out every square
input-independent two-sided linear preconditioner on the feasible tangent.
This is the simultaneous, access-normalized statement that a raw condition
number alone normally lacks.  Input-dependent whitening remains possible,
but its construction is not free.

### Theorem 4 (adaptive preconditioner construction is search-complete)

Fix any target

\[
 1\leq K<\tau_N.                                         \tag{22}
\]

Suppose an algorithm, from raw or canonical
full-SQ access to \(c^{(j)}\), outputs with probability at least \(2/3\) a
self-contained effective classical description of invertible maps
\(L,R:S\to S\) satisfying

\[
 \kappa_2(LG_jR)\leq K.                                   \tag{23}
\]

Even if output length and all exact postprocessing are free, its query
complexity is

\[
 \boxed{Q=\Theta(\sqrt N),\qquad R=\Theta(N).}             \tag{24}
\]

In particular, constructing any input-adaptive preconditioner with condition
\(o(N)\), or with any fixed-factor improvement over \(N-1\), within this
reduced-SPD square two-sided class is as hard as finding the hidden marked
coefficient.  By contrast, the input-oblivious choice \(L=R=I\) uses zero
queries and attains condition \(N-1\).  Thus the only unresolved threshold
window in this exact family is
\([\tau_N,N-1)\), whose width is \(\Theta(1/N)\): expanding (19a) gives
\(\tau_N=n-n^{-1}+O(n^{-2})\).

#### Proof

The pairwise proof of Theorem 3 gives, for every \(j\ne k\) and every fixed
pair \(L,R\),

\[
 \kappa_2(LG_jR)\,\kappa_2(LG_kR)\geq\tau_N^2.            \tag{25}
\]

Therefore when \(K<\tau_N\), one fixed output pair \((L,R)\) can satisfy (23)
for at most one index \(j\).  Given its self-contained description, an
unbounded decoder enumerates the public matrices \(G_1,\ldots,G_N\), computes
their preconditioned singular-value conditions, and returns their unique
minimum.  No exact threshold comparison is needed: on a successful input
\(j\), (25) gives for every \(k\ne j\)
\[
 \kappa_2(LG_kR)\geq{\tau_N^2\over\kappa_2(LG_jR)}
 \geq{\tau_N^2\over K}>K.
\]
Thus the true condition is separated from every other condition by at least
the public positive gap \(\tau_N^2/K-K\).  Approximating all conditions to
less than one quarter of this gap recovers \(j\).  Unique search therefore
gives the \(\Omega(\sqrt N)\) quantum and \(\Omega(N)\) randomized lower
bounds, including under canonical full SQ by the simulation in (5).

For the matching upper bounds, Grover search or a classical scan finds \(j\).
Then output the public rank-one formula for \(L=G_j^{-1}\), \(R=I\), which
makes \(LG_jR=I\).  The index \(j\) is an \(O(\log N)\)-bit succinct
description of this preconditioner.  Explicitly, with
\(\rho=(N-1)^2\),
\[
 G_j^{-1}=\rho^{-1}I_S+
 {N(\rho-1)\over\rho(\rho+N-1)}u_ju_j^T.
\]
\(\square\)

The effective-output contract means a finite representation from which the
actions or entries of \(L,R\), and the resulting singular values, can be
approximated to arbitrary precision without further raw queries.  Rational
or algebraic matrices and certified evaluable circuits suffice.  The theorem
does not cover a quantum state encoding a preconditioner, an oracle whose
later uses continue to query the raw input, uncertified floating-point
descriptions, nonlinear or rectangular preconditioners, or a preconditioner
tailored only to one right-hand side rather than the operator condition in
(23).  No bit-complexity theorem is claimed.  A finite-precision extension
would require a certified condition bound or explicit representation,
scaling, norm, and error controls for \(L,R\), in addition to a threshold
margin.

### Theorem 5 (accuracy--conditioning frontier)

The search obstruction does not require a poorly conditioned reduced Newton
system.  Fix a target readout offset \(\delta\in(0,1/2)\), and choose the
central-path point (7a) with

\[
 \theta_\delta={1+2\delta(N-1)\over N},\qquad
 b_\delta={1-2\delta\over N},\qquad
 \eta_\delta={\delta N^2\over
 (1+2\delta(N-1))(1-2\delta)}.                          \tag{26}
\]

Then the literal coordinate is exactly
\(p_j=1/2\pm\delta\).  Put

\[
 \rho_\delta=\left({1+2\delta(N-1)\over1-2\delta}\right)^2.
                                                               \tag{27}
\]

After removing a common positive scale, the barrier Hessian restricted to
\(S=\mathbf1^\perp\) is

\[
 G_j(\delta)=\rho_\delta I_S-
             (\rho_\delta-1)u_ju_j^T.                    \tag{28}
\]

Its condition number is

\[
 C_N(\delta)={N\rho_\delta\over\rho_\delta+N-1}.         \tag{29}
\]

Write \(n=N-1\) and define the exact pairwise generalized eigenvalue

\[
 t_N(\delta)=2+{(\rho_\delta-1)^2(n-1)
                    \over\rho_\delta(\rho_\delta+n)},qquad
 \tau_N(\delta)={t_N(\delta)+\sqrt{t_N(\delta)^2-4}\over2}.
                                                               \tag{29a}
\]

Moreover, over all common square invertible two-sided maps,

\[
 \tau_N(\delta)\ \leq\
 \inf_{L,R}\max_j\kappa_2\!\left(LG_j(\delta)R\right)
 \ \leq C_N(\delta),                                     \tag{30}
\]

where

\[
 r_N(\delta)=C_N(\delta)-
 {\rho_\delta-1\over
 (N-1)(\rho_\delta+N-1)},
 \qquad \tau_N(\delta)\geq r_N(\delta),\qquad
 0\leq C_N(\delta)-\tau_N(\delta)<{1\over N-1}.         \tag{31}
\]

Thus the identity preconditioner is within an additive \(1/(N-1)\) of the
best possible worst-case common two-sided preconditioner.  At the same time,
estimating \(p_j\) with bounded success probability to additive error at most
\(c\delta\), for any fixed \(c<1\), still has matched query complexity

\[
 Q=\Theta(\sqrt N),\qquad R_{\rm rand}=\Theta(N).         \tag{32}
\]

The same matched law holds for constructing a self-contained effective
classical pair \(L,R\) with
\(\kappa_2(LG_j(\delta)R)\leq K\) for any public
\(1\leq K<\tau_N(\delta)\).  This threshold is exact for the pairwise
separation argument.

For \(\delta=\Theta(N^{-\alpha})\), the condition frontier is

\[
 C_N(\delta)=
 \begin{cases}
  1+\Theta(N^{1-\alpha}),&\alpha>1,\\
  \Theta(1),&\alpha=1,\\
  \Theta(N^{2-2\alpha}),&1/2<\alpha<1,\\
  \Theta(N),&0\leq\alpha\leq1/2,
 \end{cases}
\]

with constants understood so that \(\delta<1/2\).  In particular,
\(\delta=\Theta(1/N)\) gives a Grover-hard central coordinate even though
the reduced Newton condition number and the optimal common-preconditioned
worst-case condition are both \(\Theta(1)\).  The price is inverse-linear
output accuracy, not bad reduced conditioning.  More strongly, if
\(\delta=o(1/N)\), the reduced condition tends to one while the matched
query law (32) is unchanged at error proportional to \(\delta\).

#### Proof

Solving (7b) for a prescribed offset \(\delta\), and then substituting into
(7a), gives (26), while
\(\theta_\delta/b_\delta=\sqrt{\rho_\delta}\).  Multiplying the diagonal
leaf Hessian by the irrelevant common factor
\(\rho_\delta b_\delta^2\), and restricting it to \(S\), gives (28).
Because \(\|u_j\|^2=(N-1)/N\), its eigenvalue is
\((\rho_\delta+N-1)/N\) along \(u_j\) and \(\rho_\delta\) on
\(u_j^\perp\cap S\), proving (29) and the upper bound in (30).

For distinct \(j,k\), the relative operator is the identity on the
\((n-2)\)-dimensional common orthogonal complement of \(u_j,u_k\).  A
Sherman--Morrison inverse and \(u_j^Tu_k=-1/N\) give
\[
 \operatorname{tr}(G_k(\delta)G_j(\delta)^{-1})
 =n+{(\rho_\delta-1)^2(n-1)
          \over\rho_\delta(\rho_\delta+n)}.
\]
The two remaining generalized eigenvalues have product one, because all
\(G_j(\delta)\) have the same determinant.  They are therefore exactly
\(\tau_N(\delta)\) and \(\tau_N(\delta)^{-1}\).  The similarity and
singular-condition argument in Theorem 3 implies that at least one of
\(LG_j(\delta)R\) and \(LG_k(\delta)R\) has condition at least
\(\tau_N(\delta)\), proving the lower bound in (30).

The generalized Rayleigh quotient of the same pair at \(u_j\) is exactly
\(r_N(\delta)\), so \(\tau_N(\delta)\geq r_N(\delta)\).  Direct subtraction
gives
\(C_N(\delta)-r_N(\delta)=
(\rho_\delta-1)/[(N-1)(\rho_\delta+N-1)]<1/(N-1)\),
which proves (31).

An estimate within \(c\delta\), \(c<1\), can be thresholded at \(1/2\) to
decide which public half contains the marked item.  The adversary and Yao
arguments of Theorem 1 give the lower bounds in (32); Grover search and a
classical scan give the matching upper bounds.  For the preconditioner-output
claim, the pairwise product inequality shows that one fixed output can serve
at most one marked index when \(K<\tau_N(\delta)\).  The effective decoder
and rank-one inverse construction from Theorem 4 then give the same lower and
upper bounds.  Finally, substituting
\(\delta=\Theta(N^{-\alpha})\) into (27)--(29) gives the displayed regimes.
\(\square\)

This is a real-arithmetic, query-only tradeoff.  It does not make the
\(\Theta(1/N)\)-accurate answer free: writing or certifying that precision,
choosing the path parameter to adequate precision, and finite-precision
linear-system stability must be charged in a bit or gate model.  Nor does
(30) cover input-dependent, nonlinear, rectangular, or full-KKT
preconditioning.

## Literature screen and novelty boundary

The repository's earlier
[`winner-central-path-condensation`](../../research-archive/2026-09-research-cycle/supporting-results/2026-09-02-winner-central-path-condensation.md)
already proves the broader mechanism that a central state with constant mass
on one hidden winning SDP block is search-hard to construct and becomes
ill-conditioned.  It also uses a public bounded-degree summation tree.  The
present result must not claim that mechanism as new.  Its added value is a
minimal LP witness where the *entire numerical KKT graph* is a degree-three
tree, the hard output is one literal scalar coordinate at a closed-form path
point, canonical objective SQ is fully matched, and the uniform
preconditioning obstruction (19) is explicit and sharp in order.

The ingredients are known.  Boyer, Brassard, Høyer, and Tapp prove the tight
\(\Theta(\sqrt N)\) quantum complexity of unique search:
[*Tight bounds on quantum searching*](https://arxiv.org/abs/quant-ph/9605034).
Apers and Gribling already use sign matrices whose magnitude-based SQ data
are public to transfer search lower bounds to LP spectral approximation, and
their LP paper also records general search-based LP lower bounds:
[*Quantum Speedups for Linear Programming via Interior Point Methods*](https://doi.org/10.1137/23M1625951).
Fürer, Hoppen, and Trevisan give the sharp linear-time fixed-treewidth exact
linear-system theorem:
[*Fast Gaussian Elimination for Low Treewidth Matrices*](https://doi.org/10.4230/LIPIcs.ESA.2025.116).
Augustino, Leng, Nannicini, Terlaky, and Wu study a different quantum model
that simulates the central path from a potential oracle:
[*A quantum central path algorithm for linear optimization*](https://arxiv.org/abs/2311.03977).
Tong, An, Wiebe, and Lin analyze how a *supplied* preconditioner changes QLSA
complexity, rather than the raw-query cost of constructing an
instance-adaptive one:
[*Fast inversion, preconditioned quantum linear system solvers, and fast
evaluation of matrix functions*](https://doi.org/10.1103/PhysRevA.104.032422).
Recent sparsity-sensitive QLSA lower bounds likewise concern applying the
given matrix oracle, not outputting a preconditioner:
[*Sparsity-dependent Complexity Lower Bound of Quantum Linear System
Solvers*](https://arxiv.org/abs/2601.16697).

Targeted searches for combinations of `simplex central path marked item`,
`treewidth quantum linear programming search`, `central-path coordinate
query lower bound`, and `central path output accuracy conditioning lower
bound` found no source stating (9)--(21) or (26)--(32), the bounded-degree
treewidth-one dynamic
iterate-oracle lower bound, the adaptive-preconditioner threshold
(22)--(25), or the three-way output-contract boundary.  The
underlying search reduction is elementary and closely adjacent to known LP
query lower bounds, so this should be presented as an apparently new sharp
boundary theorem, not as a new quantum lower-bound technique.  Literature
search cannot establish priority.

## What the theorem does and does not say

It proves that the following proposed implication is false for classical
query complexity of the stated compressed task:

> linear total sparsity + constant latent treewidth + classical scalar output
> implies dimension-independent classical dequantization.

It does not contradict dimension-independent sparse-SQ inverse algorithms.
Those theorems assume a uniformly conditioned invertible sparse matrix (or an
SPD matrix) and a supplied right-hand-side SQ interface.  The present Newton
matrix is an indefinite equality KKT system; its revealing barrier weights
have polynomial dynamic range, and constructing the *current* iterate or
scaling interface is the hard operation.  Bounded degree and treewidth do not
replace the missing conditioning/access hypotheses.

It does not by itself prove that an actual scalar-output QIPM has been
classically dequantized or separated; it is an obstruction to deriving such a
claim from sparsity and treewidth alone.  It also does not establish a
quantum-IPM runtime of \(O(\sqrt N)\).  Grover search is a task-level upper
bound.  Any claimed QIPM realization must charge the barrier parameter \(N\),
the polynomial leaf-Hessian dynamic range at the revealing point, the
indefinite KKT conditioning, and construction of all dynamic oracles.

## Audit record

An independent hostile audit rechecked the exact multiplier, the general
\(\theta\) formula, (9)--(13), the objective-gap transfer, and the
half-membership adversary matrix.  It verified
\(\|\Gamma\|=N/2\) and
\(\|\Gamma\circ\Delta_i\|=\sqrt{N/2}\), the classical Yao bound, and the
constant-query simulation of every canonical objective-SQ call.  It also
recounted the extended KKT graph, including the root-fixing row and literal
readout variable, and confirmed that it is a maximum-degree-three tree.
The reduced-Hessian audit separately verified (19)--(21), the similarity
invariance of the relative spectrum, the eigenvalue-to-singular-value
inequality for nonsymmetric matrices, and the sharp \(\Theta(N)\) minimax
order against every common square invertible two-sided preconditioner.
The follow-up audit also recomputed the exact trace and nontrivial relative
eigenvalues in (19a)--(21), verified
\(\tau_N=n-n^{-1}+2n^{-2}+O(n^{-3})\), and checked the adaptive decoder's
strict public gap \(\tau_N^2/K-K>0\).  It confirmed the tight
search-completeness result (22)--(25) under the stated self-contained
classical-output contract and the free-linear-algebra scope of Corollary 1A.
It also verified the exact generalized-eigenvalue threshold \(\tau_N\),
Corollary 1A's explicitly instantiated free-solve model, and Theorem 4's
search-complete adaptive-preconditioner construction under the effective
classical-output contract.  The strict inequality \(K<\tau_N\), public
decoder gap, succinct rank-one inverse upper bound, and finite-precision
caveats are all necessary and are incorporated above.

A further independent algebra audit checked Theorem 5 for arbitrary
\(\delta\): it recomputed the central mass and unmarked mass in (26), the
rank-one reduced Hessian (28), both of its eigenvalues, the condition in
(29), the exact relative trace and eigenvalue in (29a), and the generalized
Rayleigh quotient in (31).  It also verified that the pairwise determinant
argument yields both the common-preconditioner lower bound and the adaptive
threshold, that the upper and lower bounds differ by less than \(1/(N-1)\), and
that all four \(\delta=\Theta(N^{-\alpha})\) regimes are correct.  The
audit retained the inverse-accuracy and finite-precision caveat; the
\(\delta=\Theta(1/N)\) statement is a query-model separation, not a bit-cost
or end-to-end QIPM theorem.

The audit required the operational offline-SQ convention, explicit output
scope for the objective-gap reduction, KKT nonsingularity, the
symmetric-versus-bipartite treewidth convention, and the distinction between
a task-level Grover upper bound and a QIPM implementation.  All corrections
are incorporated above.  No algebraic or query-complexity defect remains.
