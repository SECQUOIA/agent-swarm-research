# A condition--application dichotomy for parity LP normal equations

Date: 2026-09-02

Verification update: The fixed-preconditioner theorem below now uses the
stronger exact ramp bound obtained during Lean verification. The
[verification report](../../../formal/PRECONDITIONER.md) records the proved
scope. The data-dependent factors and quantum-query results later in this
note are separate results.

## Summary

The parity-amplified LP has condition-one reduced primal geometry, but its
original equality normal matrix is a signed, grounded-tree Laplacian with
condition number \(\Theta(N^2)\).  Two complementary results clarify what
preconditioning can and cannot do.

1. No input-independent SPD preconditioner improves the worst-case asymptotic
   condition number, even for the signed path subfamily.
2. A data-dependent perfect preconditioner is nevertheless trivial to
   construct locally: use the signed incidence factor itself.  For its natural
   signed-Cholesky congruence, applying the inverse factor to an actual Newton
   right-hand side takes \(\Omega(N)\) coefficient queries.  This is
   factor-specific: an input-dependent orthogonal rotation can make that
   transformed right-hand side easy, while moving the parity cost to applying
   the rotation or recovering the original Newton direction.
3. For an arbitrary data-dependent preconditioner, no individual phase is
   always hard.  The invariant statement is end to end: setup, transformed-RHS
   preparation, iterative oracle use, and original-variable recovery sum to
   \(\Omega(N)\) raw queries for the concrete Newton step constructed below.

Thus there is no lower bound on sparse preconditioner *construction* from this
family, and there is no factor-independent transformed-right-hand-side lower
bound.  The rigorous conclusion is an end-to-end accounting rule: good
conditioning, factor application, transformed-input preparation, and
original-coordinate recovery cannot all be treated as free.  The theorem below
isolates the cost for one canonical sparse factor.

## Normal matrix of the parity LP

Let \(T\) be the rooted chain-plus-copy tree in the parity-amplified LP.  Give
each edge \(e=(\pi(j),j)\) a sign \(\tau_j\), equal to the hidden sign on a
chain edge and \(+1\) on a copy edge.  Let \(D_\sigma\) be the square grounded
incidence matrix whose root row is \(e_0^\top\) and whose row for nonroot node
\(j\) is

\[
 e_j^\top-\tau_j e_{\pi(j)}^\top.
\tag{1}
\]

With pair variables \((u_j,v_j)\), the equality matrix is

\[
 A_\sigma=D_\sigma[I,-I].
\tag{2}
\]

At a central point all pair sums have the same value \(q\), while their
differences are signs.  If

\[
 H=\mu\operatorname{Diag}(x^{-2})
\]

is the primal logarithmic-barrier Hessian, then

\[
 A_\sigma H^{-1}A_\sigma^\top
 =\frac{w(q)}{\mu}D_\sigma D_\sigma^\top,
 \qquad
 w(q)=\frac{q^2+1}{2}.
\tag{3}
\]

Indeed, the contribution of pair \(j\) is
\(u_j^2+v_j^2=w(q)\), independent of which coordinate contains the
hidden sign.  The irrelevant scalar in (3) will be suppressed below.

Let \(p_0=1\) and \(p_j=\tau_jp_{\pi(j)}\), and put
\(R_\sigma=\operatorname{Diag}(p_j)\).  If \(D_+\) is the unsigned grounded
incidence matrix, then

\[
 D_\sigma R_\sigma=R_\sigma D_+,
 \qquad
 C_\sigma:=D_\sigma D_\sigma^\top
   =R_\sigma C_+R_\sigma.
\tag{4}
\]

Thus all sign instances are orthogonally similar and have the same
\(\Theta(N^2)\) condition number.  The gauge \(R_\sigma\), however, contains
all prefix products.

For completeness, this conditioning estimate follows directly from the tree.
The inverse of \(D_+\) has a \(1\) in position \((j,k)\) exactly when \(k\)
is an ancestor of \(j\).  Since the tree has \(\Theta(N)\) nodes and depth
\(\Theta(N)\),
\[
 \|D_+^{-1}\|_2^2\leq\|D_+^{-1}\|_F^2=O(N^2).
\]
Bounded degree gives \(\|D_+\|_2=O(1)\), hence
\(\kappa(C_+)=O(N^2)\).  Conversely, place the ramp
\((N+1,N,\ldots,1)\) on the spine rows and zero on the copy-tree rows.
Its squared norm is \(\Theta(N^3)\), while
\(\|D_+^\top r\|_2^2=\Theta(N)\).  Thus
\(\lambda_{\min}(C_+)=O(N^{-2})\); a constant diagonal entry gives
\(\lambda_{\max}(C_+)=\Omega(1)\).  Therefore
\(\kappa(C_\sigma)=\kappa(C_+)=\Theta(N^2)\).

## No input-independent SPD preconditioner

The obstruction already holds on a path of \(m\) nodes.  Let

\[
 B=
 \begin{pmatrix}
  1\\
  -1&1\\
    &-1&1\\
    &&\ddots&\ddots
 \end{pmatrix},
 \qquad C=BB^\top,
\tag{5}
\]

and let \(R=\operatorname{Diag}(1,-1,1,-1,\ldots)\).  Both \(C\) and
\(RCR\) are normal matrices of valid sign inputs.

### Theorem 1 (minimax fixed-preconditioner lower bound)

For every input-independent SPD matrix \(M\) and \(m\ge1\),

\[
 \max\left\{
 \kappa(M^{-1/2}CM^{-1/2}),
 \kappa(M^{-1/2}RCRM^{-1/2})
 \right\}
 \ge \frac{4m^2-1}{3}\ge m^2.
\tag{6}
\]

The identity gives condition number at most \(4m^2\) for both signings,
so it is minimax optimal in order. This theorem allows \(M\) to be dense
and unrestricted, and holds for every fixed invertible congruence factor
\(P\), with matrices \(P^\top CP\) and \(P^\top RCRP\).
The displayed constant is a witness lower bound, not the exact minimax
value. It strengthens the former \(m^2/4\) bound for \(m\ge4\).

### Proof

First use the following simultaneous-preconditioning lemma.  For SPD
\(A_0,A_1,M\),

\[
 \kappa(A_0^{-1/2}A_1A_0^{-1/2})
 \le
 \kappa(M^{-1/2}A_0M^{-1/2})
 \kappa(M^{-1/2}A_1M^{-1/2}).
\tag{7}
\]

To see this, bound the generalized Rayleigh quotient
\(x^\top A_1x/(x^\top A_0x)\) using the extremal eigenvalues of both
matrices in \(M\)-coordinates.  The independent overall scales cancel when
the ratio of the maximum and minimum generalized eigenvalues is taken.

For \(r=(m,m-1,\ldots,1)^\top\), the quadratic-form identity

\[
 x^\top Cx
 =\sum_{j=0}^{m-2}(x_j-x_{j+1})^2+x_{m-1}^2
\tag{8}
\]

gives \(r^\top Cr=m\). Summing the alternating witness exactly gives

\[
 r^\top RCRr
 =\sum_{j=0}^{m-2}(r_j+r_{j+1})^2+r_{m-1}^2
 =\sum_{k=1}^{m}(2k-1)^2
 =\frac{m(4m^2-1)}3.
\tag{9}
\]

Put \(t=(4m^2-1)/3\). The generalized Rayleigh quotient of \(RCR\)
relative to \(C\) is \(t\) at \(r\) and \(1/t\) at \(Rr\). Therefore

\[
 \kappa(C^{-1/2}RCRC^{-1/2})\ge t^2.
\tag{10}
\]

Equation (7) now implies that at least one of the two preconditioned condition
numbers is at least \(t\). Pulling the witnesses back through \(P^{-1}\)
gives the same proof for arbitrary invertible congruence factors.

For the identity upper bound, let \(d_i=x_i-x_{i+1}\) for \(i<m-1\)
and \(d_{m-1}=x_{m-1}\). Then \(x_i=\sum_{j=i}^{m-1}d_j\) and
\(x^\top Cx=\sum_jd_j^2\). Cauchy--Schwarz and
\((a-b)^2\le2a^2+2b^2\) give
\[
 \frac{\|x\|_2^2}{m^2}\le x^\top Cx\le4\|x\|_2^2.
\]
Thus \(\kappa(C)\le4m^2\). Orthogonal diagonal sign conjugation preserves
the condition number, so the upper bound applies to every signed path.
\(\square\)

The alternating input is a legal prefix-sign instance: choose every hidden
chain sign equal to \(-1\).  The conclusion is stronger than a locality
lower bound, but it applies only when the preconditioner is independent of
the hidden values.

## A perfect sparse local preconditioner exists

For a data-dependent preconditioner, construction itself is easy.  Take

\[
 C_\sigma=D_\sigma D_\sigma^\top
\tag{11}
\]

as the SPD preconditioner, or retain \(D_\sigma\) as its triangular factor.
Every row of \(D_\sigma\) has two nonzeros, and every entry uses only the sign
on its own edge.  The symmetrically preconditioned matrix is exactly the
identity:

\[
 D_\sigma^{-1}C_\sigma D_\sigma^{-\top}=I.
\tag{12}
\]

This invalidates any claim that constructing a sparse, locally queryable,
uniformly conditioning preconditioner must itself compute prefix parity.
The vacuous choice \(M_\sigma=C_\sigma\) already does so.  What is not free is
applying \(D_\sigma^{-1}\), applying \(C_\sigma^{-1}\), or loading the
transformed right-hand side.

For example,

\[
 D_\sigma^{-1}e_0=(p_j)_{j\in T}.
\tag{13}
\]

Sequential forward substitution computes all prefix products in linear work
and follows the tree height.  A parallel prefix scan can reduce circuit depth
to \(O(\log N)\) with all-to-all bounded-fan-in gates, but it still uses
\(\Theta(N)\) work and input queries.  Equation (13) is the exact location at
which the condition number disappears and the hidden global information
enters.

The same observation uniformly conditions the full saddle-point KKT matrix.
For

\[
 K=\begin{pmatrix}H&A_\sigma^\top\\A_\sigma&0\end{pmatrix},
 \qquad
 \mathcal S_\sigma=A_\sigma H^{-1}A_\sigma^\top,
\]

take the exact block-diagonal constraint preconditioner
\(\mathcal M=\operatorname{Diag}(H,\mathcal S_\sigma)\).  With
\[
 Q=\mathcal S_\sigma^{-1/2}A_\sigma H^{-1/2},
 \qquad QQ^\top=I,
\]
the symmetrically preconditioned KKT matrix is
\[
 \mathcal M^{-1/2}K\mathcal M^{-1/2}
 =\begin{pmatrix}I&Q^\top\\Q&0\end{pmatrix}.
\tag{14}
\]
Its eigenvalues are \(1\) on \(\ker Q\), and
\((1\pm\sqrt5)/2\) on each coupled two-dimensional subspace.  Its absolute
spectral condition number is therefore
\[
 \left(\frac{1+\sqrt5}{2}\right)^2,
\]
independent of \(N\) and the signs.  The Schur block construction is local
once the native KKT data are available: the \(H\) block is the native KKT
diagonal, while (3) constructs the Schur block from local edge signs and one
known scalar.  This statement assumes the native KKT oracle, including \(H\),
is already available; constructing that central-iterate oracle can itself
contain prefix parity.  Applying
\(\mathcal S_\sigma^{-1}\), which is a scalar multiple of
\(D_\sigma^{-\top}D_\sigma^{-1}\), carries the additional global cost.

### The hard transformed right-hand side is an actual Newton right-hand side

The vector \(e_0\) below is not an artificial adversarial solve.  Consider the
standard infeasible-start primal--dual Newton equations for the same LP at

\[
 x=\mathbf1,\qquad s=\mathbf1,\qquad y=0,\qquad \mu=1.
\tag{15}
\]

Here "the same LP" means the original pair LP with variables \((u,v)\),
objective \(c=\mathbf1\), and equality matrix (2).  It does **not** mean the
bounded-pair augmentation \(2u_j+2v_j+2t_j=3\); at (15), that augmentation
would have additional primal and dual residuals.

This point is strictly interior, exactly dual feasible, and exactly centered.
With the residual convention

\[
 r_p=b-A_\sigma x,\qquad
 r_d=c-A_\sigma^\top y-s,\qquad
 r_c=\mu\mathbf1-Xs,
\]

we have \(r_d=r_c=0\).  Since
\(A_\sigma\mathbf1=0\) and the LP right-hand side is \(b=e_0\), its only
residual is the primal residual \(e_0\).  For any centering target
\(\sigma_c\mu\), \(0<\sigma_c\leq1\), the standard infeasible primal--dual
Newton equations are

\[
 A_\sigma\Delta x=e_0,\qquad
 A_\sigma^\top\Delta y+\Delta s=0,\qquad
 \Delta x+\Delta s=(\sigma_c-1)\mathbf1.
\tag{16}
\]

Eliminating \(\Delta x,\Delta s\), and using
\(A_\sigma\mathbf1=0\), gives

\[
 A_\sigma A_\sigma^\top\Delta y=e_0,
 \qquad
 A_\sigma A_\sigma^\top=2D_\sigma D_\sigma^\top.
\tag{17}
\]

Under the signed-incidence factor congruence, the transformed Newton
right-hand side is \(D_\sigma^{-1}e_0\), up to the irrelevant factor \(2\).
Thus the state-loading lower bound in the next section applies to a concrete
QIPM Newton correction for every usual centering choice, not merely to an
adversarial linear-system right-hand side.  It does not assert that an
infeasible-start algorithm must take a full step from (15), only that this is
the exact Newton system it forms at that interior iterate.

## Quantum lower bound for the signed-incidence factor

For an amplitude-state theorem, one endpoint copy tree alone is insufficient:
a common sign on one large subspace can be a global phase.  Add a second,
input-independent copy tree rooted at node \(0\), isomorphic to the copy tree
rooted at node \(N\).  Let \(U_0,U_N\) denote their sets of new nodes.  Each
tree has \(M\) leaves and \(K=2M-2\) new nodes, where

\[
 M=2^{\lceil\log_2(16(N+1))\rceil}.
\]

All new edges have sign \(+1\).  The resulting tree still has
\(\Theta(N)\) nodes, bounded degree, constant row/column sparsity, and a
spine of length \(N\).  The pair-LP construction and the condition-one
reduced Hessian proof are unchanged.

### Theorem 2 (the signed-incidence factor maps the Newton RHS to a parity-hard state)

Let \(\widehat D_\sigma\) be the grounded signed incidence matrix of this
two-sided amplified tree and

\[
 |z_\sigma\rangle
 =\frac{\widehat D_\sigma^{-1}e_0}
        {\|\widehat D_\sigma^{-1}e_0\|_2}.
\tag{18}
\]

Any quantum algorithm whose unconditional output has trace distance at most
\(1/20\) from \(|z_\sigma\rangle\) for every sign input makes
\(\Omega(N)\) coefficient-oracle queries.

### Proof

The entries of \(\widehat D_\sigma^{-1}e_0\) are the root-to-node sign
products.  They equal \(+1\) on every node of \(U_0\) and \(p_N\) on every
node of \(U_N\).  Pair all corresponding new nodes of the two isomorphic
trees, not only their leaves.  A fixed unitary maps the pair label and the
choice \(U_0\) versus \(U_N\) to a label register and one side qubit.
Measuring that qubit in the \(X\) basis returns \(p_N\) exactly, conditional
on observing a paired copy-tree node.

If \(P\) is the total number of tree nodes and \(m=N+1\), then

\[
 \Pr[\text{paired copy node}]=\frac{2K}{P}
 =\frac{2K}{m+2K}
 >\frac{62}{63}.
\tag{19}
\]

The last inequality uses \(M\ge16m\), hence \(K=2M-2\ge31m\) for
\(m\ge2\).  On a spine outcome output a fair bit.  The ideal success
probability is greater than

\[
 \frac12+\frac{31}{63}=\frac{125}{126}.
\tag{20}
\]

Trace distance \(1/20\) leaves success above \(2/3\).  The fixed decoder
therefore turns the alleged state-preparation algorithm into a bounded-error
algorithm for parity of the \(N\) hidden signs.  Quantum parity needs
\(\Omega(N)\) sign queries, and every sparse matrix query exposes at most one
sign. \(\square\)

Combining (12) and (18), the perfectly preconditioned normal equation has
matrix \(I\), but its transformed right-hand-side state is parity-hard:

\[
 \widehat D_\sigma^{-1}
 (\widehat D_\sigma\widehat D_\sigma^\top)
 \widehat D_\sigma^{-\top}=I,
 \qquad
 \widehat D_\sigma^{-1}e_0
 \text{ is query-hard to prepare.}
\tag{21}
\]

This is a condition-versus-loading example with no condition-number loophole
for the specified signed-incidence factor.  It is not invariant under changing
the factor by an input-dependent orthogonal matrix.

Indeed, (4) gives \(D_\sigma=R_\sigma D_+R_\sigma\).  The equally perfect left
factor

\[
 P_\sigma=D_+^{-1}R_\sigma=R_\sigma D_\sigma^{-1}       \tag{21a}
\]

satisfies

\[
 P_\sigma C_\sigma P_\sigma^T=I,\qquad
 P_\sigma e_0=D_+^{-1}e_0=\mathbf1.                    \tag{21b}
\]

Thus the transformed right-hand side can be completely input independent.
The missing parity has not disappeared: recovering original coordinates uses
\(P_\sigma^T=R_\sigma D_+^{-T}\), so its cost has moved to factor application
or output recovery.  This explicit orthogonal-factor loophole rules out any
claim that *every* perfect preconditioner must have a hard transformed right-
hand side.

## Robust extension to nearby normal equations

The exact point (15) is not essential.  At an arbitrary positive primal-dual
point of the two-sided **pair** LP, interpret \(A_\sigma\) below as
\(\widehat D_\sigma[I,-I]\), and put

\[
 \Theta=XS^{-1},\qquad
 \omega_j=\frac{x_{u_j}}{s_{u_j}}+
           \frac{x_{v_j}}{s_{v_j}},\qquad
 \Omega=\operatorname{Diag}(\omega_j).
\tag{21c}
\]

For the pair LP,

\[
 A_\sigma\Theta A_\sigma^\top
 =\widehat D_\sigma\Omega\widehat D_\sigma^\top.
\tag{21d}
\]

With residual convention

\[
 r_p=b-Ax,\qquad r_d=c-A^Ty-s,\qquad
 r_c=\mu'\mathbf1-Xs,
\]

eliminating \(\Delta x,\Delta s\) from the primal-dual Newton equations gives

\[
 A_\sigma S^{-1}XA_\sigma^\top\Delta y=g,
 \qquad
 g=r_p-A_\sigma S^{-1}(r_c-Xr_d).
\tag{21e}
\]

Thus an exact local factor is

\[
 L_\sigma=\widehat D_\sigma\Omega^{1/2},
 \qquad
 L_\sigma^{-1}g=\Omega^{-1/2}\widehat D_\sigma^{-1}g.
\tag{21f}
\]

### Robust transformed-RHS theorem

Assume

\[
 \frac{\max_j\omega_j}{\min_j\omega_j}\le4,
 \qquad
 \lVert g-e_0\rVert_1\le\frac1{100}.
\tag{21g}
\]

Any quantum algorithm whose unconditional output is within trace distance
\(1/20\) of the normalized state proportional to

\[
 \Omega^{-1/2}\widehat D_\sigma^{-1}g
\tag{21h}
\]

for every sign input makes \(\Omega(N)\) raw coefficient queries.  Here
\(g,\Omega\) are either input-independent side data, or every raw query used
to construct and access input-dependent oracles for them is included in the
query total.  Free side oracles whose numerical values themselves encode
parity are outside the theorem.

To prove this, first set \(g=e_0\).  There are \(2K\) paired copy-tree nodes
and \(m=N+1\) unpaired spine nodes.  If
\(\Gamma=\max\omega/\min\omega\le4\), the paired nodes carry squared mass at
least

\[
 \alpha
 \ge\frac{2K}{2K+\Gamma m}
 \ge\frac{62}{66}=\frac{31}{33}.
\tag{21i}
\]

For one corresponding pair, the side-qubit amplitudes have the form \(a\)
and \(p_Nb\), where \(a,b>0\) and \(a/b\in[1/2,2]\).  An \(X\)-basis
measurement returns \(p_N\) with probability

\[
 \frac12+\frac{ab}{a^2+b^2}\ge\frac9{10}.
\tag{21j}
\]

Outputting a fair bit on the spine therefore succeeds on this ideal state
with probability at least

\[
 \frac12+\frac25\frac{31}{33}=\frac{289}{330}.
\tag{21k}
\]

Now let \(\delta=g-e_0\).  Every entry of
\(\widehat D_\sigma^{-1}\delta\) is a signed sum over an ancestor path, so

\[
 \lVert\widehat D_\sigma^{-1}\delta\rVert_2
 \le\sqrt P\lVert\delta\rVert_1.
\tag{21l}
\]

Consequently,

\[
 \frac{\lVert\Omega^{-1/2}\widehat D_\sigma^{-1}\delta\rVert_2}
      {\lVert\Omega^{-1/2}\widehat D_\sigma^{-1}e_0\rVert_2}
 \le\sqrt\Gamma\lVert\delta\rVert_1
 \le\frac1{50}.
\tag{21m}
\]

The Euclidean distance between the corresponding normalized pure states is
at most twice (21m), hence at most \(1/25\).  Including the promised output
trace error gives total measurement-probability error at most
\(1/25+1/20=9/100\).  Subtracting this from (21k) leaves success greater than
\(2/3\), and parity proves the claim.

For example, the weight-ratio condition follows from the concrete local
neighborhood \(4/5\le x_i,s_i\le6/5\): then each
\(x_i/s_i\in[2/3,3/2]\) and
\(\max\omega/\min\omega\le9/4\).  Condition (21g) on \(g\) is an aggregate
Newton-residual condition through (21e), not merely componentwise centrality.

### Why a constant \(\ell_2\) feasibility residual is not obtained

The proof above genuinely uses an \(\ell_1\) bound.  On the signed spine, set
\(\widetilde d_j=p_j(1-j/N)\), keep the node-0 copy tree at value one, and set
the entire node-\(N\) copy tree to zero.  Then

\[
 \lVert\widehat D_\sigma\widetilde d-e_0\rVert_2=N^{-1/2},
\]

because each spine-edge residual has magnitude \(1/N\), while every copy-edge
residual is zero.  Nevertheless, the amplified endpoint subtree has been
erased and \(\widetilde d\) is a constant relative distance from the exact
prefix vector.  Thus even a vanishing \(\ell_2\) feasibility residual does
not imply the state closeness used by this decoder.  This is an obstruction
to extending the present proof, not a counterexample to every possible
\(\ell_2\)-robust parity reduction.  The parallel-path construction in
Theorem 3 of `2026-09-02-parity-amplified-primal-state-lower-bound.md` obtains
constant relative \(\ell_2\) robustness by paying \(\Theta(N^2)\) LP size;
the separate connectivity construction is another robust-\(\ell_2\) fallback.

## General oracle accounting consequence

Suppose preprocessing makes \(q_{\rm set}\) raw coefficient queries and
produces a reusable resource implementing the inverse-factor state map in
(18).  If one use of that resource makes \(q_{\rm on}\) further raw queries,
the state-preparation procedure invokes it \(T\) times, and the rest of the
procedure makes \(q_{\rm other}\) raw coefficient queries, then Theorem 2 gives

\[
 q_{\rm set}+Tq_{\rm on}+q_{\rm other}=\Omega(N).
\tag{22}
\]

In particular, when \(q_{\rm other}=o(N)\), a polylogarithmic-use QLSA cannot
have both \(q_{\rm set}=o(N)\) and
\(q_{\rm on}=o(N/\operatorname{polylog}N)\).
Storing all prefix products during setup achieves \(q_{\rm set}=O(N)\) and
then makes every application local, so the tradeoff is tight in order.

The setup term may be charged only once if the resulting object is genuinely
reusable without consuming hidden-state advice.  If setup instead prepares
fresh quantum advice states that are consumed by applications, their repeated
preparation cost belongs to \(q_{\rm on}\) (or to \(q_{\rm other}\)); it cannot
be amortized by assuming cloning.

The theorem does not say that every entry of every good preconditioner reveals
parity, nor that applying a good preconditioner to every right-hand side is
hard.  Such claims are false or unsupported.  It states hardness for the
specific transformed right-hand side needed by the exact sparse factor, and
more generally charges any end-to-end solver whose promised output decodes
parity.

## Implications for sparse QIPMs

- Condition number of a reduced Hessian is not a complete access-cost
  parameter.  Reaching that reduced representation can require applying the
  parity gauge or an equivalent triangular inverse.
- Input-independent preconditioning provably cannot bridge the gap on the
  signed path.
- Data-dependent local construction can bridge the spectral gap perfectly,
  so a stronger construction lower bound is impossible without an
  efficient-inverse requirement.
- For the signed-incidence factor, the cost appears in inverse-factor
  application or transformed-RHS loading.  For the rotated factor (21a), that
  RHS is easy and the cost appears in recovery.  Only the total
  setup--RHS--solve--recovery statement is factor independent.

This complements the primal-state theorem: the latter lower-bounds the final
original-variable output regardless of the route taken, while Theorem 2 shows
where the same information appears inside the natural signed-factor version
of a condition-one preconditioned normal solve.

## Novelty and collision status

The ingredients are standard, and several collisions materially narrow the
novelty claim.

- Switching a balanced signed graph by a diagonal \(\{\pm1\}\) gauge and
  deriving combinatorial formulas for signed incidence/Laplacian inverses are
  established signed-graph facts; see Alazemi, Andelić, and Mallik, *Linear
  Algebra and its Applications* 694 (2024), 78--100,
  DOI `10.1016/j.laa.2024.04.012`, arXiv:2311.02792.  Thus (4) and the
  path-product content of (13) are not new linear algebra.
- The generalized-eigenvalue and product inequalities behind (7) belong to
  classical support theory.  Boman and Hendrickson explicitly formulate
  preconditioned condition numbers through matrix pencils and emphasize that
  useful preconditioners must be inexpensive both to compute and to apply;
  see *Support Theory for Preconditioning*, SIAM J. Matrix Anal. Appl. 25(3),
  694--717, DOI `10.1137/S0895479801390637`, Sections 1--3.  The exact
  two-signing minimax witness (6) was not found there, but it is an elementary
  corollary-style use of that framework rather than a new preconditioning
  theory.
- Orsucci and Dunjko already make the factor/RHS requirement explicit for
  quantum preconditioning: after an \(A=LL^\dagger\) decomposition, the
  classical stage must efficiently obtain a description of the transformed
  vector, and their positive result assumes sparse \(b\) and locally
  invertible blocks [[orsucci2021-on-solving-classes-of-positive]] p.5,
  p.21-26.  Theorem 2 supplies a QIPM instance on which this requirement is
  provably expensive for the natural signed factor; the general warning is
  prior art.
- Low and Su separately optimize and lower-bound calls to the initial-state
  oracle in QLS, making RHS preparation an explicit resource rather than a
  free operation [[guang2026-quantum-linear-system-algorithm-optimal]] p.1,
  p.42-45.  Lapworth and Sünderhauf likewise show that block-encoding
  normalization and forming/applying a preconditioner can erase a nominal
  condition-number gain [[leigh2025-preconditioned-block-encodings-quantum-linear]]
  p.1, p.9-15.  Neither source proves this coefficient-oracle parity example.
- Wu, Mohammadisiahroudi, and Terlaky give the directly matched 2026
  preconditioned infeasible-QIPM comparator.  Their Newton equations include
  the primal, dual, and complementarity residuals used in (16), but their
  resource model assumes QRAM and treats preparation of the changing
  right-hand-side state as polylogarithmic overhead
  [[zeguan2026-preconditioned-inexact-infeasible-quantum-interi]] p.6-8,
  p.17.  Equations (15)--(18) do not contradict that theorem: they show that
  building the assumed transformed-RHS access from the raw sparse LP oracle
  can require linear setup.

The closest current sparse-QLS lower-bound comparator is Mori, Kikuchi,
Benedetti, and Rosenkranz.  They prove
\(\Omega(\kappa\sqrt{s})\) sparse-oracle queries at constant error, using
PARITY composed with promise OR, and recover the known
\(\Omega(\kappa\log(1/\epsilon))\) dependence separately
[[mori2026-sparsity-dependent-complexity-lower-bound]] p.4-8.  Their model
treats preparation of the right-hand-side state as negligible
[[mori2026-sparsity-dependent-complexity-lower-bound]] p.2.  Theorem 2 is
complementary and factor-specific: its transformed matrix is the identity and
its charged object is the transformed RHS.  It neither improves nor
contradicts their general QLS lower bound.

After these collisions, the potentially new content is limited to the exact
combination of:

1. condition number after preconditioning;
2. local construction of the preconditioner factor; and
3. coefficient-query complexity of the natural factor on an exact
   infeasible-start LP Newton right-hand side.

No searched primary source states the explicit minimax lower bound (6) or the
signed-incidence/Newton-RHS realization (15)--(21).  Because (21a)--(21b)
removes RHS hardness by an orthogonal factor change, however, Theorem 2 should
be presented as a sharp example and accounting diagnostic, not as a universal
preconditioner lower bound.

Status: **proof complete in the stated factor-specific coefficient-query and
state-output models; apparent exact-example novelty, with substantial
conceptual prior art.**

## Follow-up: arbitrary data-dependent preconditioners

The exact-factor theorem extends to arbitrary preconditioners only as an
end-to-end oracle-accounting statement.  No theorem depending on the
preconditioned condition number alone is possible.

### One Newton step lands on the hard central state

Continue from the infeasible-start point (15) on the two-sided amplified
instance, now specializing (16) to the pure feasibility correction
\(\sigma_c=1\) and taking its full step.  Let
\[
 p=\widehat D_\sigma^{-1}e_0.
\]
The unique minimum-norm solution of
\(A_\sigma\Delta x=e_0\) is
\[
 \Delta x=\frac12(p,-p).
\tag{23}
\]
Indeed, (2) gives
\(A_\sigma\Delta x=\widehat D_\sigma p=e_0\), and (23) is
orthogonal to the null space spanned by the pair sums, so it belongs to
\(\operatorname{range}(A_\sigma^\top)\) and is the Newton solution from
(16).  Moreover,
\[
 \Delta s=-\Delta x.
\]
The full step is
\[
 x^+=\mathbf1+\Delta x,\qquad
 s^+=\mathbf1-\Delta x.
\tag{24}
\]
Every pair of \(x^+\) is \((3/2,1/2)\) or its swap, every pair sum is two,
and every pair difference is the required root-to-node sign.  Hence
\[
 A_\sigma x^+=e_0,\qquad
 X^+s^+=\frac34\mathbf1.
\tag{25}
\]
Together with the updated dual multiplier, (24) is exactly the feasible
central point at \(\mu=3/4\).  The second-order product
\((1+1/2)(1-1/2)=3/4\) explains why a feasibility correction linearized at
\(\mu=1\) lands on the lower-\(\mu\) center.

Let \(K_{\rm end}=2M-2\) be the number of nonroot nodes in the endpoint copy
tree and let
\[
 P=N+1+2K_{\rm end}=N+4M-3
\]
be the number of pairs.  All pairs of \(x^+\) have equal squared norm
\(5/2\), and
\[
 \frac{K_{\rm end}}{P}>\frac{15}{32}.
\tag{26}
\]
On an endpoint-copy pair, computational-basis measurement returns the
coordinate selected by \(p_N\) with probability \(9/10\).  On every other
outcome return a fair bit.  The ideal success probability for endpoint
parity is therefore greater than
\[
 \frac12+\frac25\frac{15}{32}=\frac{11}{16}.
\tag{27}
\]
Trace error \(1/100\) leaves success above \(2/3\).  Thus producing the
updated original-primal state after this single Newton correction requires
\(\Omega(N)\) raw coefficient queries.

### Theorem 3 (preconditioner-oracle accounting)

Consider any possibly data-dependent invertible factor preconditioner
\(P_\sigma\) for
the normal equation (17), and write
\[
 G_\sigma
 =P_\sigma(A_\sigma A_\sigma^\top)P_\sigma^\top,
 \qquad
 r_\sigma=P_\sigma e_0.
\tag{28}
\]
No sparsity, symmetry, or locality assumption on \(P_\sigma\) is needed.
Suppose an end-to-end quantum Newton procedure:

1. preprocesses the raw LP coefficient oracle;
2. prepares the transformed right-hand side \(r_\sigma\);
3. solves the \(G_\sigma\) system;
4. recovers \(\Delta y,\Delta x\) in the original variables and forms
   \(x^+\); and
5. outputs a density operator within trace distance \(1/100\) of
   \(|x^+/\|x^+\|_2\rangle\).

Partition its raw coefficient queries into setup, transformed-RHS,
iterative-solve, and recovery/update costs:
\[
 Q_{\rm set},\quad Q_{\rm rhs},\quad Q_{\rm solve},\quad Q_{\rm rec}.
\]
Then
\[
 \boxed{
 Q_{\rm set}+Q_{\rm rhs}+Q_{\rm solve}+Q_{\rm rec}
 =\Omega(N).
 }
\tag{29}
\]

#### Proof

The four phases together form one coefficient-query algorithm whose final
state satisfies the decoder in (26)--(27).  Composing the fixed decoder with
the procedure computes parity of the \(N\) hidden chain signs with bounded
error.  Each LP coefficient query is simulated by \(O(1)\) sign queries, so
the quantum parity lower bound proves (29). \(\square\)

The value of (29) is that it does not assume where a data-dependent
preconditioner hides its information.  Prefix parity may enter its setup
advice, the transformed RHS, an online inverse application, or the recovery
map; the total remains linear.

### Corollary with a condition-\(K\) block-encoded solve

Suppose
\[
 \kappa(G_\sigma)\le K,
\]
the iterative solver uses at most
\(T(K,\epsilon)\) calls to its preconditioned-matrix and preconditioner
oracles, and implementing one such call from the raw coefficient oracle costs
at most \(q_{\rm on}\) raw queries.  Absorb input-independent gates and
already charged setup advice into the other phases.  Then
\[
 Q_{\rm set}+Q_{\rm rhs}
 +T(K,\epsilon)q_{\rm on}+Q_{\rm rec}
 =\Omega(N).
\tag{30}
\]
For a QLSA with
\(T(K,\epsilon)=\widetilde O(K\log(1/\epsilon))\), this becomes
\[
 Q_{\rm set}+Q_{\rm rhs}+Q_{\rm rec}
 +\widetilde O\!\left(Kq_{\rm on}\log\frac1\epsilon\right)
 =\Omega(N).
\tag{31}
\]
Equivalently, if
\[
 Q_{\rm set}+Q_{\rm rhs}+Q_{\rm rec}\le Q
\]
and the hidden polylogarithmic factor in (31) is \(L(N,\epsilon)\), then
\[
 \boxed{Q+O(Kq_{\rm on}L(N,\epsilon))=\Omega(N).}
\tag{32}
\]
Consequently either the noniterative access phases cost \(\Omega(N)\), or
\[
 Kq_{\rm on}
 =\Omega\!\left(\frac{N}{L(N,\epsilon)}\right).
\tag{33}
\]
In particular, with \(O(1)\)-raw-query online oracle calls, a
polylogarithmically conditioned preconditioner forces a
\(\widetilde\Omega(N)\) setup, transformed-RHS, or recovery cost.

This is an accounting corollary, not a lower bound asserting that every QLSA
must use \(\Omega(K)\) calls on this family.  If setup, RHS preparation, and
recovery are all \(o(N)\), it forces the online implementation budget in
(30) to supply the remaining linear cost.  If \(K=O(1)\) and the number of
oracle calls is polylogarithmic, at least one access phase must therefore
cost \(\widetilde\Omega(N)\).

### Why no stronger black-box condition-number tradeoff exists

Condition number alone contains no information about the implementation cost
of a data-dependent preconditioner.

- Taking \(P_\sigma=(A_\sigma A_\sigma^\top)^{-1/2}\) gives
  \(G_\sigma=I\) and \(K=1\), but applying \(P_\sigma\) already performs the
  hard inverse square root.
- Taking the local factor \(P_\sigma=D_\sigma^{-1}\), up to a scalar, also
  gives \(G_\sigma=I\).  Its sparse factor is locally described, while
  \(P_\sigma e_0\) is the parity-hard state from Theorem 2.
- If a model grants a unit-cost oracle for either of these data-dependent
  inverse maps without charging its construction or reduction to the raw LP
  oracle, it has granted parity advice.  The resulting apparent violation of
  (29) is an oracle-model mismatch, not an algorithm.

Conversely, a preconditioner can arrange for \(r_\sigma\) to be easy while
moving the same difficulty into \(P_\sigma^\top\) during recovery.  Therefore
no universal lower bound on \(Q_{\rm rhs}\), \(Q_{\rm on}\), or
\(Q_{\rm rec}\) individually follows from \(K\).  Equation (29), together
with the fixed-preconditioner minimax theorem (6), is the strongest
black-box statement justified by this parity family:

- input-independent preconditioners retain \(\Omega(N^2)\) worst-case
  conditioning;
- arbitrary data-dependent preconditioners may achieve \(K=1\), but their
  complete setup--solve--recovery pipeline still costs \(\Omega(N)\) raw
  queries when it produces the original Newton update.

Status of follow-up: **universal end-to-end accounting theorem proved; a
stronger condition-only or phase-specific black-box tradeoff is false without
additional oracle-implementation assumptions.**

## Matched classical baseline and referee verdict

This family has a tight and very simple classical algorithm.  Read the
\(N\) hidden edge signs once, compute all prefix products, and store the gauge
\(R_\sigma\).  This costs \(\Theta(N)\) coefficient queries, work, and words.
Thereafter the signed tree is reduced to the fixed unsigned tree; forward and
back substitution, construction of the Newton update, and any explicit full
output each take \(\Theta(N)\) work.  If random access to the prefix table is
available, the gauge can be reused over later solves with the same sign
pattern.

The parallel baseline is also strong.  Prefix products form an associative
scan, so the classical Ladner--Fischer construction computes them with
\(O(N)\) work and \(O(\log N)\) bounded-fan-in depth; tree propagation and
subtree accumulation have the same work/depth scale.  See Ladner and Fischer,
*Parallel Prefix Computation*, JACM 27(4), 831--838 (1980),
DOI `10.1145/322217.322232`.  Consequently the quantum lower bound is not a
quantum-versus-classical separation: both require \(\Theta(N)\) raw queries
up to the known constant-factor quantum parity saving, and both admit
polylogarithmic parallel depth if linear total work/bandwidth is available.
Beals, Buhrman, Cleve, Mosca, and de Wolf supply the underlying tight parity
query bound, arXiv:quant-ph/9802049.

This also fixes the preprocessing interpretation.  An \(O(N)\) classical or
quantum setup can store all prefix signs and make later factor/RHS access
cheap.  Equation (22) is therefore tight and useful only when setup is
charged, or when a headline sublinear QIPM bound assumes the required QRAM
resource already exists.  It does not rule out amortization across many
Newton solves.  Huggins and McClean's precomputation framework gives the
appropriate general accounting language: offline preparation, storage, and
consumption remain resources even when online depth is reduced
[[william2024-accelerating-quantum-algorithms-precomputation]] p.1, p.9-16.

Referee assessment:

- Theorem 1 is a finite-dimensional minimax lower bound, but its proof is elementary
  support theory and its fixed-versus-data-dependent distinction is familiar.
- Theorem 2's useful new feature is the exact infeasible-start Newton RHS;
  factor rotation (21a) prevents advertising it as universal RHS hardness.
- Theorem 3 is factor independent but is a repackaging of the already proved
  hard original-primal output under a setup--solve--recovery ledger.  Its
  value is model hygiene, not a stronger complexity exponent.

The package is credible as a lemma/counterexample suite in a broader paper on
QIPM access costs.  By itself it is unlikely to support a paper claiming a
new asymptotic preconditioning lower bound or quantum advantage.  Its main
publishable message is narrower: for an actual sparse infeasible-start Newton
system, condition-one preconditioning can coexist with linear raw-input cost,
and changing the perfect factor only relocates that cost among setup, RHS
loading, and recovery.
