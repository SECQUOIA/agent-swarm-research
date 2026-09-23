# Nullspace geometry does not supply the affine feasible offset

## Purpose and status

This note isolates the access-model consequence of the robust parallel-path LP in
Theorem 3 of `2026-09-02-parity-amplified-primal-state-lower-bound.md`.  For that
family, the nullspace, the complete reduced barrier problem, the reduced central
point, and the reduced central Hessian are all independent of the hidden input.
Nevertheless, preparing an original-primal approximate-feasible state requires
\(\Omega(\sqrt P)\) raw coefficient queries.

The query lower bound below is a formal corollary of that theorem, not a new
asymptotic bound.  Its useful extra content is an oracle-interface separation: it
identifies the missing object as the input-dependent **affine feasible offset**.
Thus a nullspace/reduced-Hessian QIPM cannot count only reduced Newton-solve access
if its output contract is an original-variable state.  The result does not apply
if a feasible-offset oracle, an equivalent original-coordinate loading oracle, or
a global batch oracle is supplied for free.

The gain--plateau extension is in
`2026-09-02-gain-plateau-affine-offset-oracle-separation.md`.  It strengthens the
dimension dependence to \(\Omega(P)\) on a late central tail with reduced
condition number below \(7/6\), at the cost of \(\Theta(\sqrt P)\) primal dynamic
range and loss of the exact scalar-identity geometry.

## The parallel-path family

Let \(N\) be a power of two.  The tree and LP are those of Theorem 3 in the source
note.  There are

\[
 P=33N^2-1
\]

tree vertices and \(4P\) nonnegative variables
\((u_j,v_j,h_j,t_j)\).  Write \(d_j=u_j-v_j\) and
\(q_j=u_j+v_j\).  The equalities are

\[
\begin{aligned}
 d_r&=1, &d_k-a_{jk}d_j&=0 &&((j,k)\in E(T)),\\
 h_r&=1, &h_k-h_j&=0 &&((j,k)\in E(T)),\\
 q_j+t_j-2h_j&=0 &&(j\in V(T)).
\end{aligned}                                                    \tag{1}
\]

On edge \(i\) of each of the \(N\) parallel length-\(N\) paths,
\(a_{jk}=\sigma_i\in\{-1,1\}\); all other labels are one.  The support pattern,
right-hand side, objective, and tree are input-independent.  Let

\[
 \tau_r=1,\qquad \tau_k=a_{jk}\tau_j.                            \tag{2}
\]

Thus \(\tau_j\) is a prefix product on a long path and equals the full parity
\(p_N=\prod_{i=1}^N\sigma_i\) on all \(16N^2\) designated output leaves.

## Exact decomposition of the hidden affine space

Define the input-independent orthonormal columns

\[
 W_j=\sqrt{\frac23}\left(\frac12e_{u_j}+\frac12e_{v_j}-e_{t_j}\right),
 \qquad W=(W_j)_{j\in V(T)}.                                    \tag{3}
\]

For every hidden string \(\sigma\), these columns form a complete basis of
\(\ker A_\sigma\).  Indeed, each column preserves \(d\) and \(h\), changes
\(q\) by \(\sqrt{2/3}\), and makes the opposite change in \(t\), so it satisfies
all three groups in (1).  There are \(P\) columns, while the \(3P\) rows of
\(A_\sigma\in\mathbb R^{3P\times4P}\) are independent.

Every exact feasible point has the unique form

\[
 x_\sigma(q)_j=
 \left(\frac{q_j+\tau_j}{2},
       \frac{q_j-\tau_j}{2},1,2-q_j\right),                    \tag{4}
\]

and it is nonnegative exactly when \(1\le q_j\le2\).  In particular, set

\[
 x_\sigma^{\rm off}:=x_\sigma(\mathbf1),\qquad
 (x_\sigma^{\rm off})_j=
 \left(\frac{1+\tau_j}{2},\frac{1-\tau_j}{2},1,1\right).       \tag{5}
\]

Then the whole affine equality space is

\[
 \{x:A_\sigma x=b\}
 =x_\sigma^{\rm off}+\operatorname{range}(W),                  \tag{6}
\]

and, more precisely,

\[
 x_\sigma(q)=x_\sigma^{\rm off}+Wz,
 \qquad z_j=\sqrt{\frac32}(q_j-1).                             \tag{7}
\]

Equation (5) is the only input-dependent part of this nullspace
parameterization.  It records, at every node, which member of the \((u_j,v_j)\)
pair is selected.  On every output leaf that choice is the full parity.  The
tangent subspace \(\operatorname{range}(W)\) changes the two pair members equally,
so no nullspace motion can create or reveal their fixed difference \(\tau_j\).

Even the canonical least-Euclidean-norm particular solution is hidden.  For a
point in (4), the squared norm of the four coordinates at node \(j\) is

\[
 \frac{q_j^2+1}{2}+1+(2-q_j)^2,
\]

which is uniquely minimized at \(q_j=4/3\).  Hence

\[
 A_\sigma^\dagger b=x_\sigma\!\left(\frac43\mathbf1\right).  \tag{7a}
\]

Although the orthogonal null projector \(WW^T\), and therefore the row-space
projector \(I-WW^T\), are public, the vector (7a) is not: its pair differences
are still \(\tau_j\).  Computing the usual initializer
\(A_\sigma^T(A_\sigma A_\sigma^T)^{-1}b\) is therefore part of the charged
coefficient processing in this family.

This also shows why a feasible-offset oracle cannot be included among the free
oracles.  Two random-access queries to the \(u_j,v_j\) coordinates of (5) at one
known output leaf reveal \(p_N\).  Even a state-preparation oracle for
\(x_\sigma^{\rm off}/\|x_\sigma^{\rm off}\|\) reveals it with constant bias:
\(\|x_\sigma^{\rm off}\|^2=3P\), and the selected pair coordinates on the
\(16N^2\) output leaves have constant total measurement probability.

## Everything intrinsic to the reduced barrier is public

The primal objective restricted to (4) is

\[
 c^Tx_\sigma(q)=\sum_j(q_j+3),                                \tag{8}
\]

and the logarithmic-barrier objective, up to an irrelevant constant, is

\[
 \Phi_\mu(q)=\sum_j\left[
 q_j+3-\mu\log\left(\frac{q_j^2-1}{4}(2-q_j)\right)
 \right].                                                     \tag{9}
\]

Both are exactly independent of \(\sigma\).  Consequently, so are all value,
gradient, Hessian, and higher-derivative oracles for the reduced problem.  Its
central point has

\[
 q_j=q(\mu)\in(1,2)\quad\hbox{for all }j,                      \tag{10}
\]

where \(q(\mu)\) is the unique root in \((1,2)\) of

\[
 1-\mu\left(\frac{2q}{q^2-1}-\frac1{2-q}\right)=0.            \tag{11}
\]

Let \(F_\mu(x)=c^Tx-\mu\sum_i\log x_i\) be the original primal
barrier objective.  At the central point, its Hessian reduced in the orthonormal
coordinates (3) is

\[
 W^T\nabla_x^2F_\mu(x_{\sigma,\mu})W=\lambda(\mu)I_P,          \tag{12}
\]

with

\[
 \lambda(\mu)=\frac{2\mu}{3}\left[
 \frac{2(q(\mu)^2+1)}{(q(\mu)^2-1)^2}
 +\frac1{(2-q(\mu))^2}\right]>0.                              \tag{13}
\]

Thus one may grant, at zero query cost, the clean sparse access circuits for
\(W,W^T\), the projectors \(WW^T\) and \(I-WW^T\), exact evaluation of (8)--(9)
and all their derivatives, exact inversion or block encoding of (12), the scalar
\(q(\mu)\), and preparation of the uniform reduced central vector.  These objects
are the same oracle or circuit for every hidden string.  What they do not provide
is the translation (5), the particular solution (7a), or an operation implementing
the embedding (7) in original coordinates.

## Oracle-separation theorem

**Theorem (reduced geometry versus original-coordinate loading).**  Consider the
family (1) in the coherent fixed-position sparse row/value oracle model, or the
analogous fixed-position column model.  Let an algorithm receive, for free and
with unlimited precision and unlimited calls, arbitrary quantum circuits, advice,
and clean oracles that are functions only of

\[
 (N,\mu,T,W,c,b,\Phi_\mu,q(\mu),\lambda(\mu))                  \tag{14}
\]

and hence are identical for every \(\sigma\).  In particular, the grant may
include the complete reduced optimization problem, its exact reduced central
solution and central Hessian inverse, and arbitrary input-independent
preprocessing of these data.

Suppose that, for every \(\sigma\), the algorithm outputs an unconditional density
operator \(\rho_\sigma\) for which there is a nonzero \(x_\sigma\ge0\) satisfying

\[
 \frac{\|A_\sigma x_\sigma-b\|_2}{\|b\|_2}\le\frac1{200},     \tag{15}
\]

and

\[
 D_{\rm tr}\left(\rho_\sigma,
 |x_\sigma/\|x_\sigma\|\rangle
 \langle x_\sigma/\|x_\sigma\||\right)\le\frac1{100}.       \tag{16}
\]

Then it makes \(\Omega(N)=\Omega(\sqrt P)\) queries to the raw coefficient
oracle for \(A_\sigma\).  The same statement holds for a constant-success
heralded output when the repetitions needed to obtain successful copies are
charged.  It remains true after adding any primal centrality-neighborhood,
objective-accuracy, or exact-central-point requirement, because those conditions
only restrict the set already quantified over in (15).

In particular, even when \(q(\mu)\), (12), and the exact reduced central vector
are free, preparing a state close to the original-variable exact central point

\[
 x_{\sigma,\mu}=x_\sigma^{\rm off}
 +W\left[\sqrt{\frac32}(q(\mu)-1)\mathbf1\right]              \tag{17}
\]

requires \(\Omega(\sqrt P)\) raw coefficient queries for every prescribed
\(\mu>0\), including an \(N\)-dependent choice.  For this exact-central-point
specialization, (16) can be weakened to trace distance at most \(1/20\).

### Proof

All free objects in (14), including all allowed oracle unitaries and their
garbage conventions, are fixed independently of \(\sigma\).  They can therefore
be hardwired as free gates in a quantum query algorithm for parity.

A coherent query to a nonzero position in a row or column of \(A_\sigma\) exposes
at most one hidden sign \(\sigma_i\).  Its row, column, repeated-path index, and
the corresponding \(i\) are determined by the public tree.  Hence one raw
coefficient query can be simulated reversibly with at most one standard sign
query, including on a superposition of positions.  Input-independent free
oracles do not require sign queries.

The stability lemma and decoder in Theorem 3 of the source note apply to every
nonnegative vector satisfying (15), without using centrality or objective
accuracy.  A fixed measurement of a constant number of independent copies of
\(\rho_\sigma\) recovers \(p_N\) with bounded error.  The trace error in (16)
preserves a positive constant bias.  Thus an algorithm making \(Q\) raw
coefficient queries would give a bounded-error parity algorithm using \(O(Q)\)
sign queries.  Quantum parity has bounded-error query complexity \(\Omega(N)\),
so \(Q=\Omega(N)=\Omega(\sqrt P)\).

For (17), equations (4), (10), and (7) prove the displayed identity, and exact
feasibility makes (15) automatic.  It remains to verify the stronger trace-error
constant.  Let

\[
 O_S=\sum_{j\in S}
 (|u_j\rangle\langle u_j|-|v_j\rangle\langle v_j|).
\]

For \(q=q(\mu)\), the squared central-vector norm per node is

\[
 G(q)=\frac{q^2+1}{2}+1+(2-q)^2.
\]

Every output leaf has \(\tau_j=p_N\), so the normalized central state obeys

\[
 p_N\langle O_S\rangle
 =\frac{|S|q}{PG(q)}.
\]

For \(1\le q\le2\), the inequality \(q/G(q)\ge1/3\) is equivalent to
\(3q^2-14q+11\le0\), whose roots are \(1\) and \(11/3\).  Since
\(|S|/P>16/33\), the displayed expectation has magnitude greater than
\(16/99\).  Trace distance \(1/20\) changes the expectation of this norm-one
observable by at most \(1/10\), leaving a fixed nonzero bias.  A constant number
of measurements therefore recovers parity.  The same oracle reduction gives
\(\Omega(N)\) raw queries with this larger central-state error tolerance.
This proves the central-point specialization.
\(\square\)

## Exact access boundary and interpretation

The theorem remains valid under any extra free access whose channel is identical
for all hidden strings, even if that access gives unbounded computational power on
the reduced coordinates.  It does **not** remain a coefficient-query theorem if
one also grants any of the following input-dependent resources:

1. a particular feasible solution or affine offset such as (5), in random-access
   or constant-success amplitude-state form;
2. a loading isometry that maps a reduced vector \(z\) to the normalized
   original vector \(x_\sigma^{\rm off}+Wz\);
3. a QRAM table of the propagated signs \(\tau_j\), or a global/batch matrix oracle
   that aggregates the repeated occurrences of the same coefficient.

Each of these resources can already contain the endpoint parity.  Charging only
queries to a scalar-identity reduced Hessian after granting such a resource would
move the hard work into uncharged input loading.

This is therefore best described as an **access-model separation** or an
**original-coordinate loading lower bound**, not as a stronger numerical query
lower bound than the robust parallel-path theorem.  Formally it is a corollary,
because all newly granted reduced oracles are input-independent.  Conceptually it
sharpens the theorem's scope: condition-one reduced Newton geometry, even together
with the exact reduced central trajectory, contains no information about the
affine translation needed to realize that trajectory in the original variables.

For nullspace-QIPM accounting, the separation is stark: \(W\) has three nonzeros
per column, its central reduced Hessian has condition number one, and the reduced
central solution is the known scalar vector \(q(\mu)\mathbf1\).  The reduced solve
therefore needs no input queries at all in this family.  The
\(\Omega(\sqrt P)\) cost lies entirely in constructing a feasible particular
solution or loading the reduced answer into original coordinates.  A complexity
bound that assumes either operation as a free state-preparation oracle has assumed
away precisely the hard stage exhibited here.

The result does not say that every nullspace QIPM pays this cost, that constructing
an arbitrary feasible offset always has parity complexity, or that a conventional
KKT matrix is well conditioned.  It is a worst-case separation in the standard
local coefficient-oracle model.  Its residual is the global right-hand-side
relative residual in (15), with \(\|b\|_2=\sqrt2\); it is not a row-normalized RMS
residual or a scale-invariant backward error.  It also lower-bounds a primal
amplitude-state output, not scalar objective estimation or a reduced Newton-state
output.
