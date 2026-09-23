# A bounded-incidence SDP whose free \(S_+^3\) central Hessian encodes parity

## Status and main point

This note gives a companion to the Schur-block parity construction.  After all equality
constraints are eliminated in one fixed public root coordinate, the optimization problem
is genuinely over one free matrix \(Z\in S_+^3\), and the hidden parity changes, by a
constant amount,

1. the effective objective on \(Z\);
2. the exact central point \(Z(\mu)\); and
3. the reduced log-barrier Hessian on the six-dimensional free tangent space.

The reduced Hessian has condition number less than \(5\), all scalar constraint rows
have two nonzeros of magnitude one, every hidden bit changes only two coefficient
values, and all cost matrices have eigenvalues in \([1/2,3/2]\).  Nevertheless,
preparing even the normalized density matrix of the free central variable to constant
trace distance requires \(\Omega(N)\) raw input queries.  The lower bound is tight in
the raw-query model.

The reduced Hessian itself cannot be synthesized cheaply from the local coefficients.
At \(\mu=1\), any raw-query circuit implementing a constant-normalization block
encoding of that six-dimensional operator to unscaled error at most \(1/8\) uses
\(\Omega(N)=\Omega(P)\) queries, including its setup.  This operator-synthesis
statement is separate from the central-state and Newton-direction lower bounds.

There is a sharper Newton statement at a completely public feasible point.  At
\(X_i^0=I_3\), barrier parameter \(\mu=1\), the complete reduced Newton Hessian is
exactly the \(6\times6\) identity and the unreduced Newton right-hand sides are
public.  Yet the exact free-root primal direction is

\[
                  \Delta Z=-a(H_{12}+pH_{13}).
\]

A fixed swap of its isometric-svec \(12\) and \(13\) coordinates has expectation
exactly \(p\).  The same is true for the normalized global primal-direction state.
Preparing either direction state therefore has the same
\(\Omega(N)=\Omega(P)\) raw-query lower bound.

There is an essential gauge caveat.  The two reduced objectives are related by the
parity-dependent orthogonal congruence \(U_p=\operatorname{diag}(1,1,p)\).  In that hidden
coordinate the reduced objective, center, Hessian, and Newton direction are public.  The
theorem is therefore about the cost of learning and applying this gauge from raw matrix
coefficients, not a lower bound after an input-dependent data structure has already been
built.  In particular, an oracle or QRAM that stores prefix products or parity has
already paid linear classical input work.

## 1. Construction

Let \(N\ge 1\), set
\[
K=16N,\qquad P=2K+N=33N,
\]
and let the input be signs \(\sigma_1,\ldots,\sigma_N\in\{-1,+1\}\).  Write
\[
p=\prod_{j=1}^N\sigma_j,
\qquad
D_\sigma=\operatorname{diag}(\sigma,1,1).
\]
There are \(P\) primal blocks \(X_0,\ldots,X_{P-1}\in S_+^3\), divided into a
pre-input group of \(K\) nodes, an input group of \(N\) nodes, and a post-input group
of \(K\) nodes.  Consecutive blocks obey
\[
X_i=G_iX_{i-1}G_i^T. \tag{1}
\]
The first \(K-1\) edges and the final \(K\) edges have \(G_i=I_3\).  The \(N\)
intervening edges, in order, have \(G_i=D_{\sigma_j}\).
These counts sum to \((K-1)+N+K=2K+N-1=P-1\) edges.

Let
\[
H_{12}=E_{12}+E_{21},\qquad H_{13}=E_{13}+E_{31}.
\]
The public cost matrices are
\[
C_i=\begin{cases}
I_3+\frac12H_{12},&0\le i<K,\\
I_3,&K\le i<K+N,\\
I_3+\frac12H_{13},&K+N\le i<P.
\end{cases} \tag{2}
\]
Consider the homogeneous SDP
\[
\begin{aligned}
\text{minimize}\quad &\sum_{i=0}^{P-1}\langle C_i,X_i\rangle,\\
\text{subject to}\quad &(1),\\
&X_i\succeq0\quad(0\le i<P).
\end{aligned} \tag{3}
\]
Every \(C_i\) is positive definite, with spectrum contained in
\([1/2,3/2]\).

## 2. Exact elimination and sparsity

Define accumulated congruences
\[
R_0=I_3,\qquad R_i=G_iG_{i-1}\cdots G_1.
\]
Then every feasible point, and only every feasible point, has the form
\[
X_i=R_iZR_i^T,\qquad Z\in S_+^3. \tag{4}
\]
The matrices \(R_i\) equal \(I_3\) throughout the pre-input group, equal
\(D_{\sigma_1\cdots\sigma_j}\) at the \(j\)-th input node, and equal \(D_p\)
throughout the post-input group.  Thus the feasible cone is linearly isomorphic to
\(S_+^3\), rather than to a second-order-cone-representable slice.

For an explicit scalar encoding, use the Frobenius-isometric coordinates
\[
\operatorname{svec}(X)=
(X_{11},\sqrt2X_{12},\sqrt2X_{13},X_{22},\sqrt2X_{23},X_{33}).
\]
Congruence by \(D_\sigma\) acts as
\[
Q_\sigma=\operatorname{diag}(1,\sigma,\sigma,1,1,1). \tag{5}
\]
Consequently each edge contributes six scalar equations
\[
x_{i,\ell}-q_{i,\ell}x_{i-1,\ell}=0. \tag{6}
\]
Every row has exactly two nonzeros of magnitude one.  Every scalar block-coordinate
occurs in at most two rows.  A hidden sign changes exactly two public-support
coefficient values, those for the \((1,2)\) and \((1,3)\) coordinates of its edge.
The right-hand side is identically zero.  The block lower-bidiagonal constraint matrix
has full row rank \(6(P-1)\), leaving tangent dimension six.

## 3. The hidden parity enters the free optimization problem

Substituting (4) into the objective gives
\[
\langle C_{\mathrm{eff}}(p),Z\rangle,
\qquad
C_{\mathrm{eff}}(p)=\sum_{i=0}^{P-1}R_i^TC_iR_i. \tag{7}
\]
The input-group costs are isotropic.  Since \(D_pH_{13}D_p=pH_{13}\),
\[
C_{\mathrm{eff}}(p)
=P\overline C_p,
\qquad
\overline C_p=I_3+aH_{12}+paH_{13},
\qquad
a=\frac{K}{2P}=\frac8{33}. \tag{8}
\]
Thus (3) reduces exactly to
\[
\min_{Z\succeq0}P\langle\overline C_p,Z\rangle. \tag{9}
\]
The three eigenvalues of \(\overline C_p\) are
\[
1-r,\ 1,\ 1+r,
\qquad r=\sqrt2a=\frac{8\sqrt2}{33}<\frac12. \tag{10}
\]
The optimum is uniquely \(Z^*=0\).  Strict primal feasibility is witnessed by
\(Z=I_3\).  Moreover, the two parity-dependent free cost matrices do not commute:
\[
[\overline C_+,\overline C_-]
=-2a^2[H_{12},H_{13}]\ne0. \tag{11}
\]
Thus no one input-independent orthogonal basis diagonalizes both objectives.  They are,
however, equivalent under an input-dependent basis.  For
\[
 U_p=\operatorname{diag}(1,1,p)
 \tag{11a}
\]
one has
\[
                         U_p^T\overline C_pU_p=\overline C_+.
\tag{11b}
\]
Consequently, writing \(\widetilde Z=U_p^TZU_p\) turns (9) into the same public
reduced optimization for both parities.  Computing the required gauge is exactly the
parity task, so this equivalence does not weaken the raw-query lower bounds below.

In fact, the gauge observation applies to the whole product-cone formulation, not only
to its reduction.  Set \(T_i=R_iU_p\) and
\(\widetilde X_i=T_i^TX_iT_i\).  Then every edge equation becomes
\(\widetilde X_i=\widetilde X_{i-1}\).  The transformed costs are also completely
public: on the pre-input blocks \(U_p\) fixes \(H_{12}\), on input blocks the cost is
isotropic, and on post-input blocks \(R_i=U_p\), hence \(T_i=I\).  Thus all input
instances lie in one orbit under an input-dependent block-diagonal orthogonal change
of variables.  Preparing the original-coordinate output still requires discovering
this change of variables; a formulation that grants the \(T_i\)'s for free has already
removed the query obstruction.

## 4. Exact central path, dual feasibility, and reduced Hessian

Use the product log-det barrier.  Orthogonal sign congruences preserve determinant, so
on the feasible cone
\[
-\mu\sum_{i=0}^{P-1}\log\det X_i=-\mu P\log\det Z. \tag{12}
\]
The exact central point is therefore
\[
Z_p(\mu)=\mu\overline C_p^{-1},
\qquad
X_i(\mu)=R_iZ_p(\mu)R_i^T. \tag{13}
\]
The associated block slacks are
\[
S_i(\mu)=\mu X_i(\mu)^{-1}
=R_i\overline C_pR_i^T, \tag{14}
\]
which are independent of \(\mu\) and have eigenvalues in \([1-r,1+r]\).

These slacks are exactly dual feasible.  Indeed, for every feasible tangent
\((R_iYR_i^T)_i\),
\[
\begin{aligned}
\sum_i\langle C_i-S_i,R_iYR_i^T\rangle
&=\left\langle C_{\mathrm{eff}}-
\sum_iR_i^TS_iR_i,Y\right\rangle\\
&=\langle P\overline C_p-P\overline C_p,Y\rangle=0.
\end{aligned} \tag{15}
\]
Because the equality matrix has full row rank, the orthogonal complement of its
kernel is the range of its adjoint.  Hence some equality multiplier \(y\) satisfies
\(A^*y+S=C\).  Equations (13)--(14) also give \(X_iS_i=\mu I_3\) blockwise.

To state conditioning in an orthonormal free coordinate, define
\[
\mathcal W_\sigma(Y)=\frac1{\sqrt P}
(R_0YR_0^T,\ldots,R_{P-1}YR_{P-1}^T). \tag{16}
\]
All \(R_i\) are orthogonal, so \(\mathcal W_\sigma\) is an isometry in Frobenius
norm.  If \(F_\mu(X)=-\mu\sum_i\log\det X_i\), then at (13)
\[
\mathcal W_\sigma^*\nabla^2F_\mu(X(\mu))\mathcal W_\sigma[Y]
=\frac1\mu\overline C_pY\overline C_p. \tag{17}
\]
The eigenvalues of the symmetric-space operator in (17) are pairwise products of
the eigenvalues in (10).  Its condition number is therefore
\[
\kappa_{\mathrm{red}}
=\left(\frac{1+r}{1-r}\right)^2<5, \tag{18}
\]
uniformly in \(N\), the input, and \(\mu\).  The irrelevant common factor \(1/\mu\)
does not affect condition number.  At \(\mu=1\), primal, slack, objective, and reduced
Hessian scales are all bounded above and below by absolute constants.

The reduced Hessians for the two parities are distinct.  Their defining matrices are
noncommuting by (11), and hence so are the two free central matrices
\(Z_+(\mu)\) and \(Z_-(\mu)\).  They are nevertheless gauge-equivalent:
\(U_p^TZ_p(\mu)U_p=Z_+(\mu)\), and conjugating the symmetric-space Hessian by
\(Y\mapsto U_p^TYU_p\) changes (17) to the public \(p=+1\) operator.

### 4.1 Exact condition-one Newton system at a public start

The preceding central Hessian has constant condition number.  A stronger
condition-one statement holds for a Newton correction from a public feasible point.
Take

\[
                         X_i^0=I_3\quad(0\le i<P),\qquad \mu=1.
\tag{18a}
\]

This point is feasible for every input because
\(D_{\sigma_i}I_3D_{\sigma_i}=I_3\).  For the barrier objective

\[
 \Phi(X)=\sum_i\langle C_i,X_i\rangle-\sum_i\log\det X_i,
\]

the block gradients and Hessians at (18a) are

\[
                         g_i=C_i-I_3,\qquad
 \nabla^2\Phi(X^0)=I
\tag{18b}
\]

in Frobenius-isometric svec coordinates.  In particular, every \(g_i\) is public
and independent of the hidden signs.

The feasible Newton correction is the unique minimizer

\[
 \min_{\Delta X\in\ker A_\sigma}
 \left\{\langle g,\Delta X\rangle+\frac12\|\Delta X\|_F^2\right\}.
\tag{18c}
\]

Equivalently, for a suitable equality multiplier \(\Delta y\), it solves the
unreduced KKT equations

\[
 A_\sigma\Delta X=0,\qquad
 \Delta X-A_\sigma^*\Delta y=I-C.
\tag{18d}
\]

Both displayed right-hand sides are public: zero for primal feasibility and the
blockwise matrices \(I-C_i\) for stationarity.  All input dependence is confined to
the two signed coefficient values per hidden edge in \(A_\sigma\).

The tangent isometry (16) gives

\[
 \boxed{
 \mathcal W_\sigma^*\nabla^2\Phi(X^0)\mathcal W_\sigma=I_{\mathbb S^3}.}
\tag{18e}
\]

Thus the complete reduced Newton Hessian is exactly identity, not merely
well-conditioned.  The reduced gradient is

\[
 \begin{aligned}
 \mathcal W_\sigma^*g
 &=\frac1{\sqrt P}\sum_iR_i^T(C_i-I)R_i\\
 &=\sqrt P\,a(H_{12}+pH_{13}).
 \end{aligned}
\tag{18f}
\]

The reduced-coordinate direction is therefore
\(-\sqrt P\,a(H_{12}+pH_{13})\).  Since a tangent represented by \(Y\) in
(16) has root block \(Y/\sqrt P\), the physical free-root direction is exactly

\[
 \boxed{\Delta Z=-a(H_{12}+pH_{13}).}
\tag{18g}
\]

Every physical block direction is
\[
                  \Delta X_i=R_i\Delta ZR_i^T.
\tag{18h}
\]

This is a full feasible step: the eigenvalues of \(\Delta Z\) are
\(-r,0,r\), where \(r=\sqrt2a<1/2\), so
\[
                         I_3+\Delta Z\succ0.
\tag{18i}
\]
Orthogonal congruence then gives
\(I_3+\Delta X_i=R_i(I_3+\Delta Z)R_i^T\succ0\) for every physical block,
so ``full feasible step'' here applies to the original product-cone SDP, not
only to its eliminated root coordinate.

The sign and normalization in (18g) can be checked without solving for
\(\Delta y\): substituting (18f) into the identity reduced system (18e) gives it
directly.

### 4.2 Exact parity in the primal Newton-direction states

Let \(\lvert12\rangle,\lvert13\rangle\) denote the two off-diagonal
isometric-svec coordinate basis states.  Since
\(\|\Delta Z\|_F=2a\), its normalized amplitude state is, up to a global sign,

\[
 \lvert\delta z_p\rangle
 =\frac{\lvert12\rangle+p\lvert13\rangle}{\sqrt2}.
\tag{18j}
\]

The fixed swap

\[
 T=\lvert12\rangle\langle13\rvert+
   \lvert13\rangle\langle12\rvert
\tag{18k}
\]

has

\[
                         \boxed{\langle\delta z_p|T|\delta z_p\rangle=p.}
\tag{18l}
\]

There is no small-root-amplitude issue for the global primal direction.  Congruence
by each \(R_i\) multiplies both the \(12\) and \(13\) direction coordinates by the
same sign.  Hence the direct sum of the swap (18k) on all \(P\) primal blocks is a
fixed Hermitian contraction \(T_{\rm glob}\), and

\[
 \boxed{
 \left\langle
 \frac{\Delta X}{\|\Delta X\|_F},
 T_{\rm glob}
 \frac{\Delta X}{\|\Delta X\|_F}
 \right\rangle=p.}
\tag{18m}
\]

The ideal swap measurement recovers parity with certainty.  Trace-distance error
\(1/100\) leaves success probability at least \(99/100\).  Because one raw
coefficient query is simulated by at most one input-bit query, quantum parity gives
an \(\Omega(N)=\Omega(P)\) lower bound for preparing either the normalized root
direction state (18j) or the normalized global primal-direction state in (18m).
The bound is tight after explicitly reading all \(N\) signs.

> **Theorem 1 (public-RHS condition-one Newton-direction hardness).**
> For the SDP family (3), consider the equality-constrained primal
> logarithmic-barrier Newton correction at the public feasible point (18a).
> Its complete reduced Hessian is exactly identity, both unreduced KKT
> right-hand sides in (18d) are public, all scalar equality rows and columns
> have incidence at most two, and the feasible cone is linearly isomorphic to
> the non-SOCP cone \(\mathbb S_+^3\).  Nevertheless, any bounded-error
> quantum algorithm that prepares either normalized primal direction state
> (18j) or (18m), to trace distance at most \(1/100\), uses
> \(\Omega(N)=\Omega(P)\) raw coefficient queries.

This theorem does not concern the amplitude state of the complete
\((\Delta X,\Delta y)\) KKT solution.  Chain multipliers can dominate that
normalization, and extracting the primal sector would require its success probability
to be charged.

### 4.3 Raw-query cost of a reduced-Hessian block encoding

The parity obstruction is already present in coherent access to the reduced
central Hessian.  At \(\mu=1\), omit the irrelevant scalar factor in (17) and
write the six-dimensional symmetric-space operator as

\[
                    \mathcal L_p(Y)=\overline C_pY\overline C_p.
\tag{HBE1}
\]

Its spectral condition number is the quantity in (18), namely

\[
 \kappa_2(\mathcal L_p)
 =\left(\frac{1+8\sqrt2/33}{1-8\sqrt2/33}\right)^2
 <4.18<5,
\tag{HBE2}
\]

and \(\|\mathcal L_p\|=(1+8\sqrt2/33)^2<1.81\).  Thus neither
conditioning nor operator scale grows with \(P\).

Let \(\lvert33\rangle\) be the isometric-svec basis vector for \(E_{33}\).
Since the third column of \(\overline C_p\) is
\((pa,0,1)^T\), direct multiplication gives

\[
 \mathcal L_p(E_{33})
 =\begin{pmatrix}a^2&0&pa\\0&0&0\\pa&0&1\end{pmatrix},
 \qquad
 \operatorname{svec}(\mathcal L_p(E_{33}))
 =(a^2,0,\sqrt2pa,0,0,1)^T.
\tag{HBE3}
\]

Let \(\ell_p\) denote the svec vector displayed in (HBE3).  It has norm
\(1+a^2\).  Therefore the public swap

\[
 T_H=\lvert13\rangle\langle33\rvert+
     \lvert33\rangle\langle13\rvert
\tag{HBE4}
\]

has expectation

\[
 \left\langle {\ell_p\over1+a^2},
 T_H{\ell_p\over1+a^2}\right\rangle
 ={2\sqrt2pa\over(1+a^2)^2},
 \qquad
 {2\sqrt2a\over(1+a^2)^2}>0.61.
\tag{HBE5}
\]

This yields a block-encoding synthesis lower bound without postselection.
Use the standard unscaled-error convention: a unitary \(U_\sigma\), with
signal projector
\(\Pi=\lvert0^{a_{\rm anc}}\rangle\langle0^{a_{\rm anc}}\rvert\otimes I_6\),
is an \((\alpha,a_{\rm anc},\varepsilon)\) block encoding when

\[
 B_\sigma=\Pi U_\sigma\Pi\big|_{\operatorname{ran}\Pi},
 \qquad
 \|\mathcal L_p-\alpha B_\sigma\|\le\varepsilon.
\tag{HBE6}
\]

Assume the normalization \(\alpha\) is a fixed public number with
\(0<\alpha\le A\), where \(A\) is an absolute constant, and take
\(\varepsilon\le1/8\).  Apply \(U_\sigma\) once to
\(\lvert0^{a_{\rm anc}}\rangle\lvert33\rangle\), then measure the observable equal to
\(T_H\) on the signal subspace and zero on its orthogonal complement.  Put

\[
 e_p=\alpha B_\sigma\lvert33\rangle-\ell_p.
\]

Equation (HBE6) gives \(\|e_p\|\le\varepsilon\).  Since
\(\|\ell_p\|=1+a^2\) and \(\|T_H\|=1\), the signed measurement expectation
obeys

\[
\begin{aligned}
 p\,\langle T_H\rangle
 &\ge {1\over\alpha^2}
 \left(2\sqrt2a-2(1+a^2)\varepsilon-\varepsilon^2\right)\\
 &\ge {\gamma\over A^2},\\
 \gamma
 &:=\frac{16\sqrt2}{33}-\frac{1+a^2}{4}-\frac1{64}
 >0.405.
\end{aligned}
\tag{HBE7}
\]

The zero eigenspace of the measured observable can be assigned an independent
fair output sign.  The resulting binary output equals parity with probability
at least \(1/2+\gamma/(2A^2)\), a fixed advantage.  One call to the proposed
block encoding therefore gives a parity algorithm.

> **Theorem 2 (reduced-Hessian oracle-synthesis hardness).**  Let a uniform
> quantum circuit use coherent raw access to the local equality coefficients
> in (6) and implement an
> \((\alpha,a_{\rm anc},\varepsilon)\) block encoding of the
> reduced Hessian \(\mathcal L_p\), where \(\alpha\le A=O(1)\) is public and
> \(\varepsilon\le1/8\) uses the convention (HBE6), for every input
> \(\sigma\).  Then the circuit uses at least
> \(N/2=\Omega(P)\) raw coefficient-oracle queries.

Indeed, the preceding single-call decoder has the correct sign with uniform
positive bias.  Its acceptance probability is a polynomial of degree at most
twice the raw query count; the sign degree of parity is \(N\).  The exact
\(N/2\) statement is not obtained by amplification and does not hide a
constant depending on \(A\).

All input-dependent work must be counted.  If a setup stage makes
\(q_{\rm setup}\) queries to produce classical data, gates, or coherent
workspace and a subsequent first usable call makes \(q_{\rm call}\) further
queries, then the proof gives

\[
                     q_{\rm setup}+q_{\rm call}\ge N/2.
\tag{HBE8}
\]

After an \(\Omega(N)\)-query setup, the marginal cost of later calls may of
course be small; the theorem is a synthesis cost, not an amortized per-call
lower bound.  The proof only measures the principal block, so it permits any
unitary completion that the counted raw-query circuit actually constructs.
It does not apply when an arbitrary input-dependent completion, a reduced
Hessian oracle, the parity, or the prefix gauges are supplied for free.  Such
an interface has already performed the global aggregation that the theorem
lower-bounds.  Likewise, the claim is not a block-encoding-call lower bound:
once a valid reduced-Hessian oracle is supplied, one call suffices to reveal
parity by (HBE7).

## 5. Linear raw-query lower bound for the free central state

The raw oracle is the standard coherent value oracle for the displayed scalar
constraint matrix: on a requested row and one of its two public nonzero slots, it
returns the exact value in \(\{-1,+1\}\).  Row supports, all right-hand sides, and all
cost matrices are public.  Equivalently, encode
\(\sigma_j=(-1)^{z_j}\) and use the standard bit oracle
\(|j,b\rangle\mapsto|j,b\mathbin\oplus z_j\rangle\).  Because the requested row
identifies its edge and svec coordinate, one constraint-value query is simulated
coherently using at most one call to this bit oracle.  This statement includes queries
made in superposition.

Normalize the free central variable to a density matrix:
\[
\rho_p=\frac{Z_p(\mu)}{\operatorname{tr}Z_p(\mu)}
=\frac{\overline C_p^{-1}}{\operatorname{tr}\overline C_p^{-1}}. \tag{19}
\]
The state is independent of \(\mu\).  Direct inversion, or diagonalization in the
span of \(e_1\) and \((e_2+pe_3)/\sqrt2\), gives
\[
\operatorname{tr}(H_{13}\rho_p)
=-p\frac{2a}{3-2a^2}
=-p\frac{528}{3139}. \tag{20}
\]
Since \(\|H_{13}\|=1\), the trace distance obeys
\[
D(\rho_+,\rho_-)
=\frac12\|\rho_+-\rho_-\|_1
\ge \frac{528}{3139}>\frac16. \tag{21}
\]
Thus a fixed two-outcome postprocessing of a measurement of \(H_{13}\), or the
Helstrom measurement, recovers parity with constant bias.  If a preparation algorithm
outputs a state within trace distance \(1/100\) of the correct \(\rho_p\), the same
measurement still has constant bias.

In the raw sparse-coefficient oracle model, one coefficient query can be simulated with
at most one query to the corresponding sign \(\sigma_j\): only the two locations in
(5) depend on that sign.  A \(q\)-query state-preparation algorithm followed by the
measurement above would therefore give a \(q\)-query bounded-error quantum algorithm
for parity.  The quantum query complexity of parity is \(\Omega(N)\).  Hence:

> **Theorem 3 (free-cone central-state hardness).**  For the SDP family (3), any
> bounded-error quantum algorithm that, from raw coherent sparse coefficient access,
> prepares a state within trace distance \(1/100\) of the normalized free central
> state (19) uses \(\Omega(N)=\Omega(P)\) input queries.  This remains true at
> \(\mu=1\), where all primal/slack scales and the reduced Hessian condition number
> are absolute constants.

The raw-query bound is tight: read the \(N\) signs, compute their parity, and prepare
the constant-dimensional state (19).  This costs \(O(N)\) raw queries plus only
constant-dimensional state synthesis.

## 6. The same lower bound for the physical product-cone state

Let
\[
\rho_p^{\mathrm{glob}}
=\frac{\bigoplus_{i=0}^{P-1}X_i(\mu)}
{\sum_i\operatorname{tr}X_i(\mu)}. \tag{22}
\]
Every sign congruence preserves trace.  On the first \(K\) blocks, \(R_i=I\), so
the public block-diagonal observable that equals \(H_{13}\) on those blocks and zero
elsewhere has norm one and expectation
\[
\frac KP\operatorname{tr}(H_{13}\rho_p)
=-p\frac{16}{33}\frac{528}{3139}. \tag{23}
\]
The two global states consequently have constant trace distance.  Even after trace
error \(1/100\), (23) gives a constant-bias parity decoder.  Therefore Theorem 3 also
holds when the requested output is the normalized physical product-cone central state,
not merely the root coordinate.

## 7. What the theorem does and does not say

The construction separates several explanations that are often conflated:

* The hardness is not caused by poor reduced conditioning: (18) is below five.
* It is not caused by high row or column degree: scalar incidence is at most two.
* It is not caused by large or vanishing data: constraint coefficients have magnitude
  one and public costs lie between \(1/2\) and \(3/2\).
* It is not enough to observe that the reduced Hessian is a constant-dimensional,
  well-conditioned operator.  Theorem 2 shows that synthesizing even a
  constant-normalization approximate block encoding of that operator from the local
  coefficients costs \(\Omega(P)\) raw queries.  Once that oracle is supplied, one
  call reveals parity; this is a synthesis lower bound, not a call lower bound.
* For the Newton theorem, it is not hidden in the right-hand side: (18d) has public
  primal and stationarity right-hand sides, while the complete reduced Hessian at the
  public start is exactly identity.
* In the fixed public root coordinate, equations (8), (13), and (17) show constant
  parity dependence in the free objective, central point, and Hessian.  This is not
  an intrinsic separation modulo input-dependent coordinates: (11a)--(11b) turn all
  three into public objects.  The hard operation is recovering and applying that
  hidden gauge, or producing the answer in the requested public coordinate.
* It is not a dimension-output lower bound.  The free output is a single qutrit density
  matrix.  The obstruction is the raw work required to aggregate globally distributed
  coefficient information.

The theorem does not preclude a fast solver under a stronger oracle that returns the
prefix products or parity directly.  Such an oracle has changed the input model.  A
classical preprocessing pass that builds it costs \(\Theta(N)\) on this family.  Nor
does the theorem claim a gate lower bound once that preprocessing is supplied for free.

The equality multipliers need not remain bounded: dual flow along the chain may
accumulate.  The result deliberately concerns the free primal central state and reduced
Hessian, for which all relevant scales are constant.  Any theorem additionally
requiring a bounded complete primal-dual Newton direction must separately charge this
dual-flow issue.

The exact identity claim (18e) is for the equality-constrained primal
logarithmic-barrier Newton system.  It is not a condition-one claim for the full saddle
matrix in (18d), nor automatically for every symmetrized primal-dual SDP Newton
formulation.  The reduced gradient (18f) already contains parity; an oracle that
supplies that reduced right-hand side, or the elimination isometry
\(\mathcal W_\sigma\), for unit cost has supplied the hard global composition.
Finally, Theorem 1 targets the normalized primal direction, not the complete
primal--dual direction state.

## 8. Structural lesson

Orthogonal congruence chains can hide a global group product while preserving an
isometric feasible tangent space.  Repeating two different public anisotropic costs on
opposite sides of the hidden chain makes that group product act on the reduced free
objective.  This yields the general template
\[
\overline C_g=C_0+U_g^TC_1U_g, \tag{24}
\]
where \(g\) is a hard accumulated group element.  Conditioning can remain constant if
the anisotropic perturbations are bounded away from the PSD boundary.  In the present
\(\mathbb Z_2\) example, the fixed-coordinate matrices for the two parities do not
commute, but they lie in one orbit under the hidden congruence \(U_p\).  Thus the two
anisotropic anchors expose the accumulated group element in a public coordinate; they
do not make the reduced optimization inequivalent modulo input-dependent congruence.
An intrinsically different reduced problem would require a congruence invariant, such
as the spectrum, to depend on \(g\).  The present construction instead isolates the
raw cost of finding the coordinate transformation itself on the smallest non-SOCP cone
\(S_+^3\).

This template suggests a broad access lower-bound frontier for sparse conic IPMs:
bounded local incidence and a well-conditioned reduced Hessian do not imply cheap
coherent access to that Hessian or its central state.  One must also account for the
cost of composing the local congruences that define the reduced operator.

## 9. Literature check and novelty status

Several ingredients have clear classical precedents and should not be presented as
new.  Accumulating local orthogonal group labels into a global gauge or holonomy is a
standard synchronization motif; see T. Gao, J. Brodzki, and S. Mukherjee,
[*The Geometry of Synchronization Problems and Learning Group Actions*](https://arxiv.org/abs/1610.09051).
Representation-theoretic block diagonalization and restriction to invariant
Jordan-algebra ranges are established SDP dimension-reduction methods; see F. Vallentin,
[*Symmetry in semidefinite programs*](https://arxiv.org/abs/0706.4233), and
F. Permenter and P. A. Parrilo,
[*Dimension reduction for semidefinite programs via Jordan algebras*](https://arxiv.org/abs/1608.02090).
These works support the gauge/elimination interpretation of (4), but they do not give
an IPM central-state query lower bound.  The log-det central equation and Hessian
pullback are standard barrier calculations.  The parity lower bound is the polynomial
method of R. Beals et al.,
[*Quantum lower bounds by polynomials*](https://arxiv.org/abs/quant-ph/9802049), and
the fact that \(S_+^3\) has no finite second-order-cone representation is due to
H. Fawzi,
[*On representing the positive semidefinite cone using the second-order cone*](https://arxiv.org/abs/1610.04901).

The generic quantum SDP lower bounds do **not** subsume Theorem 1 as stated.
J. van Apeldoorn, A. Gily\'en, S. Gribling, and R. de Wolf,
[*Quantum SDP-solvers: Better upper and lower bounds*](https://arxiv.org/abs/1705.01843),
lower-bound approximate optimization interfaces, including objective-value recovery,
by LP embeddings.  Here the optimum is exactly zero for both parities, so an
optimal-value oracle has no parity information; the requested output is instead one
specified interior central state.  This makes the contracts incomparable rather than
making the present theorem a uniformly stronger SDP lower bound.  Moreover, quantum
row-query lower bounds with a linear exponent are already possible in other sparse
optimization regimes: Theorem 8.4 of S. Apers and S. Gribling,
[*Quantum speedups for linear programming via interior point methods*](https://arxiv.org/abs/2311.03215v3),
gives an \(\Omega(\sqrt{ndr})\) lower bound for additive LP optimal-value estimation.
That theorem neither requests nor identifies a central density, so the linear exponent
itself is not the novelty claimed here.  Quantum
SDP/IPM upper bounds such as I. Kerenidis and A. Prakash,
[*A Quantum Interior Point Method for LPs and SDPs*](https://arxiv.org/abs/1808.09266),
and B. Augustino et al.,
[*Quantum Interior Point Methods for Semidefinite Optimization*](https://arxiv.org/abs/2112.06025),
analyze approximate solutions or Newton directions under their own matrix-access and
output models.  B. Augustino et al.,
[*A quantum central path algorithm for linear optimization*](https://arxiv.org/abs/2311.03977),
uses a potential-evaluation oracle to simulate an LP central path and is not a raw
sparse-coefficient lower bound for an SDP central density.

Nor is Theorem 1 a disguised condition-number lower bound for a supplied quantum
linear system.  No square linear system and prepared right-hand-side state are part of
the theorem's input; its reduced Hessian is only six-dimensional and uniformly
well-conditioned.  General query state conversion, characterized by T. Lee et al.,
[*Quantum query complexity of state conversion*](https://arxiv.org/abs/1011.3020),
is an abstract framework capable of expressing this input-to-state task, but does not
provide the sparse SDP construction or its central-path interpretation.

A targeted primary-source search through September 2, 2026 found no theorem with the
specific conjunction proved here: bounded-degree local congruence constraints; a free,
non-SOCP \(S_+^3\) reduction; a bounded parity-dependent central Hessian; and
\(\Omega(P)\) raw coefficient queries for a constant-dimensional central density (or
the physical product-cone central state), together with the raw-query lower bound for
synthesizing a bounded-normalization block encoding of that six-dimensional Hessian.
The defensible novelty claim is this conjunction, not the congruence-chain,
symmetry-reduction, parity, log-det, or linear query-exponent ingredients separately.
Here ``parity-dependent'' is explicitly a fixed-public-coordinate statement:
(11a)--(11b) show that the two reduced problems are equivalent under a
parity-dependent orthogonal gauge.  The construction therefore does not establish
inequivalence under arbitrary input-dependent reparameterization.  This search is
evidence against an obvious collision, not proof of bibliographic priority.
