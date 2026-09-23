# A noncommuting sparse block-SDP central-state parity lower bound

Date: 2026-09-02

## Main result

There is a linear-size family of product-cone SDPs with \(3\times3\) blocks
whose exact central density matrices and normalized full primal--dual vectors
encode parity with constant bias.  The
family has constant `svec` sparsity, one input-dependent coefficient position
per hidden bit, constant coefficient magnitude, a public right-hand side of
constant norm, bounded primal/slack/multiplier coordinates, and reduced
log-det Hessian condition number exactly one.  Preparing the normalized primal
density matrix or full central state to trace distance \(1/100\)
requires
\(\Omega(P)=\Omega(N)\) raw coefficient queries.  The same lower bound holds
for calls to an explicit canonical exact block encoding of the `svec`
measurement operator with normalization two.

Unlike the \(2\times2\) candidate in
[2026-09-02-two-by-two-block-sdp-parity-audit.md](2026-09-02-two-by-two-block-sdp-parity-audit.md),
each block's feasible slice is not an LP interval.  It is affinely isomorphic
to \(\mathbb S_+^2\), hence to a three-dimensional Lorentz cone, and is
nonpolyhedral; the full slice is their product.  Moreover, the central blocks
for opposite parities do not commute at any positive central parameter.

The remaining limitations are explicit.  This is a block-SDP/SOCP phenomenon,
not irreducible higher-dimensional SDP geometry.  The hard signs are loaded
through affine feasibility constraints into the requested state, and bounded
dual coordinates require the inverse scale \(\mu_0=1/P\).

## 1. Fixed `svec` convention and sparse constraints

For \(X\in\mathbb S^3\), use the Frobenius isometry

\[
 \operatorname{svec}(X)
 =(X_{11},\sqrt2X_{12},\sqrt2X_{13},
   X_{22},\sqrt2X_{23},X_{33}).
\tag{1}
\]

Let

\[
 G_{13}=\frac{E_{13}+E_{31}}{\sqrt2},
 \qquad
 G_{23}=\frac{E_{23}+E_{32}}{\sqrt2}.
\tag{2}
\]

Thus \(\langle G_{13},X\rangle=\sqrt2X_{13}\) and similarly for
\(G_{23}\).  Let \(N\ge2\), \(K=16N\), and

\[
                         P=N+K+1=17N+1,
                  \qquad \mu_0=\frac1P.
\tag{3}
\]

Put

\[
 a_i=\begin{cases}
       \sigma_i,&1\le i\le N,\\
       1,&N<i<P,
     \end{cases}
 \qquad
 \tau_0=1,
 \qquad
 \tau_i=\prod_{j=1}^ia_j.
\tag{4}
\]

The primal variable is
\(X=(X_0,\ldots,X_{P-1})\in(\mathbb S_+^3)^P\).  Use three independent
rooted chains of constraints:

\[
\begin{aligned}
 \langle E_{33},X_0\rangle&=1,&
 \langle E_{33},X_i\rangle-\langle E_{33},X_{i-1}\rangle&=0,\\
 \langle G_{13},X_0\rangle&=\sqrt2,&
 \langle G_{13},X_i\rangle-a_i\langle G_{13},X_{i-1}\rangle&=0,\\
 \langle G_{23},X_0\rangle&=0,&
 \langle G_{23},X_i\rangle-\langle G_{23},X_{i-1}\rangle&=0,
 \qquad 1\le i<P.
\end{aligned}
\tag{5}
\]

They fix \(X_{i,33}=1\), \(X_{i,13}=\tau_i\), and \(X_{i,23}=0\), while
leaving the top \(2\times2\) principal block free.  Use the public cost

\[
                       C_i=\mu_0\operatorname{Diag}(1,1,2).
\tag{6}
\]

In the fixed `svec` coordinates, every row of (5) has at most two nonzeros,
every constrained column occurs in at most two rows, and all coefficients
have magnitude one.  The maximum absolute row and column sums are two.  The
support is public, and exactly one `svec` coefficient position depends on
each \(\sigma_i\).  If a raw oracle instead exposes both symmetric matrix
entries before `svec`, an input sign occupies two positions; this changes only
an absolute constant.

The three chain matrices act on disjoint `svec` coordinates and are invertible
lower bidiagonal matrices.  Hence the \(3P\) constraints are linearly
independent in the \(6P\)-dimensional vectorization.  Only the two root
right-hand sides are nonzero, so

\[
                              \|b\|_2=\sqrt3.
\tag{7}
\]

## 2. Exact central path and bounded multipliers

For \(0<\mu\le\mu_0\), put \(t=\mu/\mu_0\in(0,1]\) and define

\[
 X_i(t)=
 \begin{pmatrix}
  1+t&0&\tau_i\\
  0&t&0\\
  \tau_i&0&1
 \end{pmatrix}.
\tag{8}
\]

Its inverse is

\[
 X_i(t)^{-1}=
 \begin{pmatrix}
  t^{-1}&0&-\tau_it^{-1}\\
  0&t^{-1}&0\\
  -\tau_it^{-1}&0&1+t^{-1}
 \end{pmatrix}.
\tag{9}
\]

Thus the central slack is

\[
 S_i(t)=\mu X_i(t)^{-1}
 =\begin{pmatrix}
  \mu_0&0&-\mu_0\tau_i\\
  0&\mu_0&0\\
  -\mu_0\tau_i&0&\mu+\mu_0
 \end{pmatrix}.
\tag{10}
\]

Both matrices are positive definite and satisfy

\[
                             X_i(t)S_i(t)=\mu I_3.
\tag{11}
\]

Let \(\gamma\), \(\alpha\), and \(\delta\) be the multipliers of the
\(33\), signed \(13\), and public \(23\) chains, respectively.  With the
primal--dual convention

\[
                       \mathcal A_\sigma^*y+S=C,
\tag{12}
\]

take

\[
\begin{aligned}
 \alpha_j&=\sqrt2\mu_0\tau_j(P-j),\\
 \gamma_j&=(\mu_0-\mu)(P-j),\\
 \delta_j&=0.
\end{aligned}
\tag{13}
\]

To verify every `svec` factor, stationarity on the constrained coordinates is

\[
 B_\sigma^T\alpha=\sqrt2\mu_0\tau,
 \qquad
 B_+^T\gamma=(\mu_0-\mu)\mathbf1,
 \qquad
 B_+^T\delta=0.
\tag{14}
\]

Backward substitution gives (13).  On the three free top-block coordinates,
the slack already equals the cost:
\(S_{11}=S_{22}=\mu_0\), \(S_{12}=0\).  This proves exact dual stationarity.
As a sign and normalization check,
\[
 \langle C,X(t)\rangle=3+2t,
 \qquad b^Ty(t)=\gamma_0+\sqrt2\alpha_0=3-t,
 \qquad \langle C,X(t)\rangle-b^Ty(t)=3t=3P\mu,
\tag{14a}
\]
which is the exact primal--dual gap for \(P\) blocks of order three.

All central coordinates are uniformly bounded on the whole tail
\(0<\mu\le\mu_0\):

\[
 \|X(t)\|_{\max}\le2,
 \qquad \|S(t)\|_{\max}\le\frac2P,
 \qquad \|\alpha\|_\infty\le\sqrt2,
 \qquad \|\gamma\|_\infty\le1.
\tag{15}
\]

The \(1/P\) scale is necessary in this representation.  Replacing \(\mu_0\)
by a constant in (6) and following the same constant-ratio path makes
\(|\alpha_0|=\sqrt2\mu_0P=\Theta(P)\).

## 3. Unique strictly complementary optimum

Write a feasible block as

\[
 X_i=\begin{pmatrix}A_i&b_i\\b_i^T&1\end{pmatrix},
 \qquad b_i=(\tau_i,0)^T.
\tag{16}
\]

The Schur complement gives

\[
                         X_i\succeq0
 \quad\Longleftrightarrow\quad
                         Z_i:=A_i-b_ib_i^T\succeq0.
\tag{17}
\]

Up to the fixed contribution of the constrained last coordinate and
\(b_ib_i^T\), the objective is

\[
                         \mu_0\sum_i\operatorname{Tr}Z_i.
\tag{18}
\]

It has the unique minimizer \(Z_i=0\).  Hence the unique primal optimum is

\[
 X_i^*=
 \begin{pmatrix}1&0&\tau_i\\0&0&0\\\tau_i&0&1\end{pmatrix},
 \qquad \operatorname{rank}X_i^*=1.
\tag{19}
\]

Taking \(\mu\downarrow0\) in (10),(13) gives a dual optimum with

\[
 S_i^*=\mu_0
 \begin{pmatrix}1&0&-\tau_i\\0&1&0\\-\tau_i&0&1\end{pmatrix},
 \qquad \operatorname{rank}S_i^*=2,
 \qquad X_i^*S_i^*=0.
\tag{20}
\]

Thus every block is strictly complementary, with
\(\operatorname{rank}X_i^*+\operatorname{rank}S_i^*=3\).  The limiting
multipliers remain bounded by (15).  The dual slack is also unique: the free
top-block stationarity coordinates force
\(S_{11}=S_{22}=\mu_0,S_{12}=0\), and \(S_iX_i^*=0\) then forces
\(S_{13}=-\mu_0\tau_i,S_{23}=0,S_{33}=\mu_0\).  Full row rank of the
measurement map makes its multiplier unique.

The barrier characterization also proves uniqueness of the central path.
Since \(\det X_i=\det Z_i\), the reduced barrier objective is

\[
              \mu_0\operatorname{Tr}Z_i-\mu\log\det Z_i,
\tag{21}
\]

whose unique minimizer is \(Z_i=(\mu/\mu_0)I_2=tI_2\).  Substitution in
(16) is exactly (8).

## 4. Condition-one reduced log-det Hessian

The tangent space consists of arbitrary symmetric perturbations \(H_i\) in
the free top \(2\times2\) block.  Under the Schur-complement coordinate
\(Z_i\), the same perturbation is applied to \(Z_i=tI_2\).  For every such
perturbation,

\[
 D^2[-\mu\log\det Z_i][H_i,H_i]
 =\mu\operatorname{Tr}(Z_i^{-1}H_iZ_i^{-1}H_i)
 =\frac\mu{t^2}\|H_i\|_F^2.
\tag{22}
\]

Using any Frobenius-orthonormal `svec` basis of \(\mathbb S^2\) in each block,
the complete \(3P\)-dimensional reduced Hessian is

\[
 H_{\rm red}(\mu)=\frac\mu{t^2}I_{3P}
 =\frac{\mu_0^2}{\mu}I_{3P},
 \qquad
 \kappa(H_{\rm red})=1.
\tag{23}
\]

At \(\mu=\mu_0\), its absolute eigenvalue is \(1/P\); it grows rather than
shrinks farther down the central tail.

## 5. Noncommuting parity centers

Let \(X_+(t)\) and \(X_-(t)\) denote (8) with \(\tau=+1\) and \(-1\).
Their commutator is

\[
 [X_+(t),X_-(t)]
 =\begin{pmatrix}
    0&0&-2t\\
    0&0&0\\
    2t&0&0
   \end{pmatrix}\ne0
 \qquad(t>0).
\tag{24}
\]

Thus no input-independent orthogonal basis diagonalizes both positive central
blocks.  At the limiting optimum \(t=0\), the two rank-one matrices happen to
commute because their supports are orthogonal; noncommutativity is a genuine
interior-path property here.  Quantitatively,
\(\|[X_+(t),X_-(t)]\|_{\rm op}=2t\), so it is not bounded away from zero
uniformly as \(\mu\downarrow0\).

Each block's feasible slice is also genuinely nonpolyhedral.  Equation (17)
is an affine isomorphism from that slice to \(\mathbb S_+^2\), which is
linearly isomorphic to the three-dimensional Lorentz cone; the full feasible
slice is \((\mathbb S_+^2)^P\).  Since a linear image of a polyhedron is
polyhedral, this slice has no finite exact LP extended formulation.  It is
still SOCP-representable, so the result should not be advertised as
irreducible higher-order semidefinite hardness.

There is a stronger reduction caveat.  Since
\(b_ib_i^T=\operatorname{Diag}(1,0)\) for both signs, the reduced variable
\(Z_i\), its cone, the objective (18), and the barrier (21) are all completely
input-independent.  The signs occur only in affine-fixed entries discarded
by the Schur-complement reduction.  Thus (24) is genuine noncommutation in the
reported original matrices, but not evidence of an input-dependent
noncommutative Newton solve.  Indeed, with
\(Q=\operatorname{Diag}(-1,1,1)\), one has
\(X_-(t)=QX_+(t)Q\) and \(S_-(t)=QS_+(t)Q\): the two signs are related by a
hidden orthogonal congruence, even though no single public basis diagonalizes
both.

## 6. Density-state parity decoder

Let \(O=\{N+1,\ldots,N+K\}\) be the public copy suffix.  On it,
\(\tau_i=p_N:=\prod_{j=1}^N\sigma_j\).  Normalize the block direct sum to a
density operator:

\[
 \rho_\sigma(t)
 =\frac{\bigoplus_{i=0}^{P-1}X_i(t)}{2P(1+t)}.
\tag{25}
\]

Define a fixed contraction that is zero off the suffix and swaps basis states
one and three on each suffix block:

\[
 \mathcal O=\bigoplus_iO_i,
 \qquad
 O_i=\begin{cases}
       E_{13}+E_{31},&i\in O,\\
       0,&i\notin O.
      \end{cases}
\tag{26}
\]

Then \(\|\mathcal O\|=1\) and

\[
 \operatorname{Tr}[\mathcal O\rho_\sigma(t)]
 =p_N\frac{K}{P(1+t)}.
\tag{27}
\]

Uniformly for \(0<t\le1\),

\[
                  \frac{K}{P(1+t)}
                  \ge\frac{K}{2P}
                  \ge\frac{16}{35}.
\tag{28}
\]

The binary POVM \((I\pm\mathcal O)/2\) therefore reports parity with
constant bias from one copy of the density state.

### 6.1 Normalized full primal--dual state

The parity signal is not diluted if the requested amplitude state contains
the complete central vector.  Let
\[
 v_\sigma(t)=
 \bigl(\operatorname{svec}X(t),\,y(t),\,
       \operatorname{svec}S(t)\bigr),
 \qquad
 |v_\sigma(t)\rangle=\frac{v_\sigma(t)}{\|v_\sigma(t)\|_2},
\tag{28a}
\]
where \(y=(\gamma,\alpha,\delta)\) is ordered as in Section 2.  Directly from
(8), (10), and (13),
\[
\begin{aligned}
 \|X(t)\|_F^2&=P(2t^2+2t+4),\\
 \|y(t)\|_2^2
 &=\bigl(2+(1-t)^2\bigr)
   \frac{(P+1)(2P+1)}{6P},\\
 \|S(t)\|_F^2&=\frac{t^2+2t+5}{P}.
\end{aligned}
\tag{28b}
\]
For \(P\ge3\) and \(0<t\le1\), these imply
\[
                         \|v_\sigma(t)\|_2^2\le11P.
\tag{28c}
\]

On each suffix block, let a fixed symmetric contraction swap the primal
`svec` coordinate \(X_{33}=1\) with the coordinate
\(\sqrt2X_{13}=\sqrt2p_N\), and let it be zero on every other primal, dual,
and slack coordinate.  Its expectation in (28a) is
\[
 p_N\frac{2\sqrt2K}{\|v_\sigma(t)\|_2^2},
 \qquad
 \left|\frac{2\sqrt2K}{\|v_\sigma(t)\|_2^2}\right|
 \ge\frac{2\sqrt2K}{11P}.
\tag{28d}
\]
Since \(K/P\ge32/35\) for \(N\ge2\), this is a uniform constant bias.
Thus one fixed binary POVM decodes parity from the normalized complete
central amplitude state throughout the late tail.

## 7. Raw-query lower bound

Give an algorithm coherent sparse position/value access to the fixed `svec`
measurement matrix of (5), with \(b,C,\mu\) and the block layout public.
Count all coefficient queries used in preprocessing, advice, or output-state
preparation.  A matrix value query is simulated with at most one query to the
corresponding \(\sigma_i\).

If an algorithm outputs either a density operator within trace distance
\(1/100\) of \(\rho_\sigma(t)\), or a state within trace distance \(1/100\)
of (28a), for any fixed public \(t\in(0,1]\), the corresponding fixed POVM in
Section 6 computes parity with bounded error.  The polynomial method therefore
gives

\[
                         q\ge\frac N2=\Omega(P)
\tag{29}
\]

raw coefficient queries.  Querying all signs and preparing either target
state shows tightness up to a constant factor in this query model.

The theorem is uniform over the whole central tail in the sense that the same
lower bound and decoder work for every fixed public \(t\in(0,1]\).  It does
not mean that one algorithm must output all tail points simultaneously.

## 8. Canonical block-encoding query lower bound

The raw-query theorem transfers to a completely specified block-encoding
interface.  Let \(A_\sigma\in\mathbb R^{3P\times6P}\) be the `svec`
measurement matrix in (5).  Its support and entry magnitudes are public, every
nonzero magnitude is one, and

\[
             \max_r\|(A_\sigma)_{r,*}\|_1
             =\max_c\|(A_\sigma)_{*,c}\|_1=2.
\tag{BE1}
\]

For every potential nonzero position \((r,c)\), introduce a distinct public
label \(|e_{rc}\rangle\), together with mutually orthogonal row-failure labels
\(|L_r\rangle\) and column-failure labels \(|R_c\rangle\).  Define

\[
\begin{aligned}
 |\chi_r\rangle
 &=\sum_{c:(r,c)\in\operatorname{supp}A}
   \sqrt{\frac{|A_{rc}|}{2}}\,|e_{rc}\rangle
   +\sqrt{1-\frac{\|(A_\sigma)_{r,*}\|_1}{2}}\,|L_r\rangle,\\
 |\phi_c^\sigma\rangle
 &=\sum_{r:(r,c)\in\operatorname{supp}A}
   \operatorname{sgn}(A_{rc}^\sigma)
   \sqrt{\frac{|A_{rc}|}{2}}\,|e_{rc}\rangle
   +\sqrt{1-\frac{\|(A_\sigma)_{*,c}\|_1}{2}}\,|R_c\rangle.
\end{aligned}
\tag{BE2}
\]

The row states are an orthonormal family because different rows have disjoint
entry and failure labels.  The column states are orthonormal for the analogous
reason.  Free top-block `svec` columns have column sum zero and are represented
entirely by their failure label.  Root rows and terminal chain columns have
sum one and hence failure amplitude \(1/\sqrt2\); internal chain rows and
columns have sum two and no failure amplitude.  Most importantly,

\[
                         \langle\chi_r|\phi_c^\sigma\rangle
                         =\frac{(A_\sigma)_{rc}}2.
\tag{BE3}
\]

Choose public unitary completions

\[
 L|0,r\rangle=|\chi_r\rangle,
 \qquad
 R_0|0,c\rangle=|\phi_c^0\rangle,
\tag{BE4}
\]

where \(R_0\) includes every public sign, including the public minus on a
predecessor entry, but omits the hidden factor \(\sigma_i\).  All support,
one- or two-term superpositions, failure arms, invalid-index behavior, and
unitary completions are fixed independently of the input.

A concrete public completion uses a two-slot register.  For a degree-two row
or column, apply a Hadamard and reversibly map its two slots to its two entry
labels.  For degree one, map the second slot to the corresponding failure
label.  For a free degree-zero column, map directly to its failure label.
Padded invalid addresses map bijectively to distinct invalid labels.  The
inverse reversible maps and the same controlled Hadamards define the inverse
circuits on these subspaces; complete the remaining public basis states by a
fixed lexicographic bijection.  Thus neither the state preparation nor its
junk action makes an uncharged input query.

On an entry label, reversibly compute whether it is the predecessor entry of
the signed \(13\)-transition row \(i\le N\), and compute that \(i\) when it
is.  Let \(S_\sigma\) multiply such a label by \(\sigma_i\), and act as the
identity on every public-entry, failure, and invalid label.  With the standard
phase-oracle extension \(\sigma_0=1\), this uses exactly one coherent hidden
sign query on an arbitrary superposition.  Then

\[
 R_\sigma=S_\sigma R_0,
 \qquad
 U_A=L^\dagger R_\sigma
\tag{BE5}
\]

is an exact rectangular projected-unitary encoding of \(A_\sigma/2\): after
padding row and column address spaces to one public common dimension,

\[
 \langle0,r|U_A|0,c\rangle=\frac{(A_\sigma)_{rc}}2.
\tag{BE6}
\]

Thus the normalization is exactly

\[
                              \alpha_A=2.
\tag{BE7}
\]

Each call to \(U_A\), \(U_A^\dagger\), or a controlled version uses exactly
one sign query.  If a square Hermitian block encoding is preferred, apply the
same state-pair construction directly to the public-support dilation

\[
 \mathscr A_\sigma=
 \begin{pmatrix}0&A_\sigma\\A_\sigma^T&0\end{pmatrix}
 \in\mathbb R^{9P\times9P}.
\tag{BE8}
\]

Its maximum absolute row and column sums are also two.  Each hidden dilation
entry and its transpose compute the same local bit index, so placing its sign
in the column-state phase again gives an exact normalization-two block
encoding with one sign query per call, adjoint call, or controlled call.

The right-hand side \(b\), the cost \(C\), the public parameter \(t\), and the
block/output layouts contain no hidden signs.  Their state-preparation and
arithmetic circuits may be called without hidden-input queries.  Therefore an
algorithm using either canonical encoding above, its adjoint, arbitrary
input-independent gates, and unlimited public-data preparation that outputs
either target state of Sections 6--6.1 to trace distance \(1/100\) must use

\[
                          q_{\rm BE}\ge\frac N2=\Omega(P)
\tag{BE9}
\]

block-encoding calls.  The proof replaces every block-encoding call by its
one-query sign-oracle implementation and then applies the parity lower bound
from Section 7.

This statement is deliberately about the displayed canonical unitary and its
fully specified junk action.  It is not a theorem relative to an arbitrary
input-dependent unitary completion supplied for free.  Such a completion can
store prefix products or parity in its nonprincipal blocks even though its
encoded top-left matrix is still \(A_\sigma/2\).  Any preprocessing used to
construct a different completion must be charged to the raw input queries for
the lower bound to apply.

## 9. Scope and literature calibration

The result strengthens the \(2\times2\) audit in three ways: the feasible
slice is nonpolyhedral, the exact centers for opposite parity do not commute,
and the public right-hand side has constant rather than \(\Theta(\sqrt P)\)
norm.  It also retains exact centrality, strict complementarity, bounded
coordinates, constant sparsity, and condition-one reduced geometry.

It establishes both a raw coefficient-oracle theorem and a theorem for the
canonical block encoding in Section 8, but not for an arbitrary supplied
unitary completion.  Nor does it establish hardness of a robust
approximate-feasibility contract.  Because the fixed affine constraints
directly load prefix parity into
\(X_{13}\), it is best interpreted as an output-synthesis obstruction for
sparse QIPMs rather than a lower bound on the arithmetic cost of the reduced
Newton solve.

The linear-size formulation uses the standard product cone
\((\mathbb S_+^3)^P\), equivalently an SDP language with an explicit list of
constant-size PSD blocks.  If the input format instead permits only one
unrestricted \(3P\times3P\) PSD variable, enforcing all off-block entries to
zero explicitly takes \(\Theta(P^2)\) scalar equalities.  Thus the linear
dimension and sparsity claim must not be transferred to that single-cone
format without granting block-diagonal structure as part of the
representation.

Finally, the Schur-complement reduction is more revealing than the bare SOCP
equivalence: because \(b_ib_i^T\) is independent of \(\tau_i\), the entire
reduced conic optimization and every reduced Newton system are public.  The
raw-query lower bound is for synthesizing the affine offset in the requested
original-coordinate output.  It is not evidence that solving the scalar
condition-one reduced Hessian consumes parity queries.

The cone slice is a Lorentz cone.  For the standard fact that
\(\mathbb S_+^2\) is linearly isomorphic to the three-dimensional second-order
cone, see Fawzi,
[*On representing the positive semidefinite cone using the second-order
cone*](https://doi.org/10.1007/s10107-018-1233-0).  Existing quantum QIPM work,
including Augustino et al.,
[*Quantum Interior Point Methods for Semidefinite Optimization*](https://arxiv.org/abs/2112.06025),
analyzes algorithmic upper bounds and condition/precision dependence rather
than this exact central density-output query contract.  General quantum SDP
oracle lower bounds such as van Apeldoorn et al.,
[*Quantum SDP-Solvers: Better upper and lower bounds*](https://arxiv.org/abs/1705.01843),
use different feasibility/value-estimation output models.

A targeted search did not locate this particular conjunction of a locally
signed sparse block-SDP, a noncommuting exact central family, condition-one
reduced log-det geometry, bounded central coordinates, and a density-output
parity reduction.  This is evidence rather than proof of priority.  The
SOCP equivalence and affine output-loading mechanism should remain prominent
in any novelty claim.

As a numerical audit, dense `svec` systems for \(N=2,5,17\) were checked at
\(t=1,0.37,0.01\).  Primal residuals were zero, dual residuals were below
floating-point roundoff, complementarity held blockwise, every reduced
Hessian eigenvalue equaled \(\mu_0^2/\mu\), and the density expectation
matched (27).
