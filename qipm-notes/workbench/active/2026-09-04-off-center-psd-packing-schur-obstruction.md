# Off-center PSD packing: exact quotient Hessian, stability radius, and a sharp obstruction

Status: Proved; targeted literature screen completed; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated quotient-Hessian and conditional-oracle scope

## Result

The exact PSD--Lorentz reduced-oracle equivalence at auxiliary fiber
centers does **not** extend uniformly to arbitrary feasible packed-PSD
iterates.

For an arbitrary positive-definite Schur residual \(D_\ell\), exact
elimination of the PSD auxiliary directions gives the projected Hessian
quadratic

\[
 \boxed{
 Q_D(U)=
 2\sum_\ell\operatorname{tr}(D_\ell^{-1}U_\ell^TU_\ell)
   +4z(U)^TM(D)^{-1}z(U),}                                \tag{1}
\]

where

\[
 z_a(U)=\sum_\ell
   \operatorname{tr}(E_a^\ell W_\ell^TU_\ell),\qquad
 M_{ab}(D)=\sum_\ell
   \operatorname{tr}(E_a^\ell D_\ell E_b^\ell D_\ell).    \tag{2}
\]

Here \(E_a^\ell\) is the diagonal projector onto columns in block \(\ell\)
that belong to source ball \(a\). Formula (1) exposes two off-center
couplings absent from source-separated grouped Lorentz lifts:
\(D_\ell^{-1}\) couples column directions inside a packed block, and
\(M(D)^{-1}\) couples source allocation rows.

There is nevertheless a quantitative recovery theorem. Let \(D^0\) be
the diagonal fiber-center residual at the same projected point:

\[
 (D_\ell^0)_{\gamma\gamma}
    ={1-\|x_a\|^2\over h}
       \quad(\gamma\in\Gamma_a).                          \tag{3}
\]

If, blockwise,

\[
             \mu D_\ell^0\preceq D_\ell\preceq L D_\ell^0,
 \qquad 0<\mu\leq1\leq L,                                \tag{4}
\]

then the quotient Hessians satisfy

\[
 \boxed{
 {1\over L^2}H_0\preceq H_D\preceq{1\over\mu^2}H_0.}      \tag{5}
\]

Thus the fiber-centered grouped-Lorentz Hessian \(H_0\) is a preconditioner
with condition at most

\[
                         \boxed{(L/\mu)^2.}                \tag{6}
\]

The same comparison holds after restriction to a primal nullspace, and
the corresponding dual normal matrices have the reversed but equally
bounded comparison. Under matched block-encoding access and efficient
application of the centered preconditioner, a quantum linear solver
therefore loses at most a factor governed by \((L/\mu)^2\) in spectral
conditioning. Compiling \(D^{-1}\), \(M(D)^{-1}\), and the
preconditioner is a separate access cost and is not free.

No bound independent of \(L/\mu\) is possible. Already two balls packed
into one PSD block admit feasible iterates at projected point \(x=0\) for
which the grouped Lorentz Hessian has condition one while the packed-PSD
projected Hessian has condition

\[
                         {1+|\rho|\over1-|\rho|}\to\infty. \tag{7}
\]

For a fixed objective, the normalized projected Newton states stay a
constant trace distance apart as \(|\rho|\to1\). Hence there is no
packing-independent off-center oracle equivalence, condition comparison,
or state converter based only on the projected iterate and ball slacks.

Together with the centered equivalence theorem, this gives an exact
boundary:

- fiber correlations are invisible after exact auxiliary centering;
- bounded relative fiber eccentricity gives a \((L/\mu)^2\) transfer; and
- arbitrary off-center correlations can destroy both source separability
  and conditioning while the projected point remains fixed.

## 1. Setup

Use the column-packed lift of \(C=(B_2^s)^b\):

\[
 Z_\ell=
 \begin{pmatrix}S_\ell&W_\ell^T\\W_\ell&I_p\end{pmatrix}\succ0,
 \qquad
 D_\ell=S_\ell-W_\ell^TW_\ell\succ0,                      \tag{8}
\]

with source equations

\[
 \sum_\ell\langle E_a^\ell,S_\ell\rangle=1
 \qquad(a\in[b]).                                        \tag{9}
\]

Every column belongs to exactly one source, so the \(E_a^\ell\) are
pairwise orthogonal diagonal projectors whose nonzero sum is the identity
on the columns of block \(\ell\).

For a direction \((A_\ell,U_\ell)=(\delta S_\ell,\delta W_\ell)\), put

\[
                 B_\ell=A_\ell-W_\ell^TU_\ell-U_\ell^TW_\ell. \tag{10}
\]

The barrier Hessian is

\[
 {\cal Q}_D(B,U)=
 \sum_\ell\left[
  \operatorname{tr}(D_\ell^{-1}B_\ell D_\ell^{-1}B_\ell)
  +2\operatorname{tr}(D_\ell^{-1}U_\ell^TU_\ell)\right], \tag{11}
\]

and the affine tangent equations become

\[
 \sum_\ell\langle E_a^\ell,B_\ell\rangle=-2z_a(U).        \tag{12}
\]

The projected or quotient Hessian \(H_D\) is defined by minimizing (11)
over \(B\) subject to (12), for each fixed projected direction \(U\).

This is the correct second-order Schur elimination at an arbitrary
feasible lift point. It is distinct from partially minimizing the barrier
value over the whole auxiliary fiber, which would first replace \(D\) by
the diagonal center (3).

## 2. Exact auxiliary Schur complement

On the product space of symmetric \(B_\ell\)'s, define

\[
 \langle B,C\rangle_D
   =\sum_\ell\operatorname{tr}
      (D_\ell^{-1}B_\ell D_\ell^{-1}C_\ell).              \tag{13}
\]

The Riesz representative of the functional
\(B\mapsto\sum_\ell\langle E_a^\ell,B_\ell\rangle\) is

\[
                       G_a^\ell=D_\ell E_a^\ell D_\ell.   \tag{14}
\]

Its Gram matrix is exactly

\[
 \langle G_a,G_b\rangle_D
  =\sum_\ell\operatorname{tr}
       (E_a^\ell D_\ell E_b^\ell D_\ell)=M_{ab}(D).       \tag{15}
\]

The matrix \(M(D)\) is positive definite. Indeed, for
\(\theta\in\mathbb R^b\),

\[
 \theta^TM(D)\theta
 =\sum_\ell
   \left\|D_\ell^{1/2}
       \left(\sum_a\theta_aE_a^\ell\right)
       D_\ell^{1/2}\right\|_F^2,                          \tag{16}
\]

which vanishes only if every diagonal coefficient \(\theta_a\) on every
source column vanishes.

The minimum squared \(D\)-norm subject to (12) is therefore
\(4z^TM^{-1}z\). Adding the \(U\)-only term in (11) proves (1).

At the fiber center (3), every \(D_\ell^0\) is diagonal. The first term in
(1) becomes

\[
                  2\sum_\gamma{\|u_\gamma\|^2\over d_\gamma^0},
\]

while \(M(D^0)\) is diagonal with

\[
 M_{aa}(D^0)=h\left({1-\|x_a\|^2\over h}\right)^2.
\]

Substitution recovers

\[
 (H_0)_a={2h\over1-\|x_a\|^2}I
  +{4h\over(1-\|x_a\|^2)^2}x_ax_a^T,                     \tag{17}
\]

the grouped-Lorentz marginal Hessian.

## 3. Relative-eccentricity stability theorem

Vectorization turns the \(B\)-part of (11) into the positive quadratic
operator \(D_\ell^{-1}\otimes D_\ell^{-1}\), restricted to the symmetric
subspace. From (4),

\[
 {1\over L}(D_\ell^0)^{-1}
   \preceq D_\ell^{-1}
   \preceq {1\over\mu}(D_\ell^0)^{-1}.                    \tag{18}
\]

Tensor monotonicity and the analogous one-factor comparison for the
\(U\)-term give, for every \(B,U\),

\[
 {1\over L^2}{\cal Q}_{D^0}(B,U)
 \leq{\cal Q}_D(B,U)
 \leq{1\over\mu^2}{\cal Q}_{D^0}(B,U).                   \tag{19}
\]

The facts \(\mu\leq1\leq L\) make the squared constants valid
simultaneously for the \(B\)- and \(U\)-terms. They also follow
automatically for the extremal generalized eigenvalue bounds because
\(\operatorname{tr}D=\operatorname{tr}D^0\), unless \(D=D^0\).

The feasible affine set of \(B\)'s in (12) is the same for \(D\) and
\(D^0\). Taking its minimum on all three terms in (19) proves (5).

For any primal nullspace basis \(N\),

\[
 {1\over L^2}N^TH_0N
 \preceq N^TH_DN
 \preceq {1\over\mu^2}N^TH_0N.                           \tag{20}
\]

For a full-row-rank affine matrix \(A\), inversion of (5) gives

\[
 \mu^2 AH_0^{-1}A^T
 \preceq AH_D^{-1}A^T
 \preceq L^2 AH_0^{-1}A^T.                               \tag{21}
\]

Equations (20)--(21) prove the preconditioned condition bound (6) for the
standard primal-nullspace or dual-normal reductions.

A directly checkable sufficient condition is

\[
 \delta_{\rm fib}:=
 \max_\ell\left\|
   (D_\ell^0)^{-1/2}(D_\ell-D_\ell^0)(D_\ell^0)^{-1/2}
 \right\|_2<1.                                            \tag{21a}
\]

Then (4) holds with
\(\mu=1-\delta_{\rm fib}\) and \(L=1+\delta_{\rm fib}\), so

\[
 \kappa_{\rm prec}\leq
 \left({1+\delta_{\rm fib}\over1-\delta_{\rm fib}}\right)^2. \tag{21b}
\]

The stronger fiber Dikin bound obtained by replacing each spectral norm in
(21a) with the joint Frobenius norm also implies (21b). Thus a uniformly
small auxiliary-centering residual gives a dimension-independent spectral
transfer; ordinary projected centrality alone does not, as Section 4
shows.

In a block-encoding model, (6) is only the spectral part of a solver
ledger. Rescale the preconditioned SPD operator to spectrum contained in
\([( \mu/L)^2,1]\), and put
\(\gamma_{\rm BE}=\alpha_{\rm rel}/\|{\cal A}_{\rm rel}\|\geq1\) for any
additional block-encoding normalization overhead. A conditional
inverse-state bound has the schematic form

\[
 \widetilde O\!\left(
   \gamma_{\rm BE}\,(L/\mu)^2
   \log(1/\epsilon_{\rm lin})\right),                     \tag{22}
\]

where \(\alpha_{\rm rel}\) is the normalization of the chosen
preconditioned encoding. State preparation, application of
\(H_0^{-1/2}\), access to \(D^{-1}\), formation or inversion of the
\(b\times b\) matrix \(M(D)\), and output conversion remain charged.
Thus constant relative fiber eccentricity is a sufficient transfer
hypothesis, not by itself an end-to-end speedup theorem.

## 4. Exact two-ball obstruction

Take \(b=2\), one column per ball (\(h=1\)), and \(p=s\). Put

\[
 W=0,\qquad
 D=S=
 \begin{pmatrix}1&\rho\\ \rho&1\end{pmatrix},
 \qquad |\rho|<1.                                        \tag{23}
\]

This is a strictly feasible point of the one-factor
\(\mathbb S_+^{s+2}\) lift: both source equations fix the diagonal entries
to one, while the off-diagonal entry is free. Its projection is the
analytic center \(x_1=x_2=0\).

Because \(W=0\), the rank term in (1) vanishes. For
\(U=[u_1\ u_2]\),

\[
 Q_\rho(U)=
 {2\over1-\rho^2}
 \left(\|u_1\|^2+\|u_2\|^2-2\rho\,u_1^Tu_2\right).        \tag{24}
\]

The source-symmetric and source-antisymmetric subspaces have eigenvalues

\[
                         {2\over1+\rho},
 \qquad {2\over1-\rho},                                  \tag{25}
\]

with their order exchanged when \(\rho<0\). Hence

\[
                       \kappa(H_\rho)
                       ={1+|\rho|\over1-|\rho|}.           \tag{26}
\]

At the same projected point, the fiber-centered PSD and grouped Lorentz
Hessians are \(H_0=2I\), with condition one.

Choose a linear objective whose coefficient columns are
\(C=[v\ 0]\), with \(\|v\|=1\), and multiplier \(\eta>0\). The barrier
gradient in the \(U\)-variables vanishes at \(W=0\), and the auxiliary
\(B\)-system decouples. The projected Newton directions are therefore

\[
 \delta U_\rho=-{\eta\over2}[v\ \rho v],
 \qquad
 \delta U_0=-{\eta\over2}[v\ 0].                          \tag{27}
\]

Their normalized pure states have overlap
\(1/\sqrt{1+\rho^2}\), hence trace distance

\[
                         {|\rho|\over\sqrt{1+\rho^2}}
                         \longrightarrow {1\over\sqrt2}. \tag{28}
\]

The two states arising from the indistinguishable projected records
\(\rho\) and \(-\rho\) have trace distance
\[
                         {2|\rho|\over1+\rho^2}\longrightarrow1. \tag{28a}
\]

The projected data \(x\), ball slacks, objective, and source equations are
the same. Only the hidden auxiliary correlation differs. Therefore no
converter or oracle simulation using only projected data can recover the
off-center PSD Newton state uniformly: by (28a), error below \(1/2-o(1)\)
for both signs is impossible.

Here \(D^0=I\), \(\mu=1-|\rho|\), and \(L=1+|\rho|\). Thus the relative
eccentricity \(L/\mu\) equals the exact projected condition number (26).
At least linear dependence on relative fiber eccentricity is unavoidable;
the general squared upper bound (6) is not asserted sharp in its exponent.

The same example shows a structural obstruction. For every \(\rho\ne0\),
(24) has cross-source Hessian entries, whereas the source-separated
grouped Lorentz marginal Hessian is block diagonal. No
source-preserving permutation or diagonal rescaling can identify them.
This does not rule out representing one fixed SPD matrix by a more general
Lorentz system with new dense coupling data; such a representation would
already encode the auxiliary correlation and is not the centered
equivalence under study.

## 5. Algorithmic interpretation

The obstruction is avoidable for this explicit lift because the fiber
analytic center is known:

\[
 D_\ell\leftarrow D_\ell^0,\qquad
 S_\ell\leftarrow W_\ell^TW_\ell+D_\ell^0.                \tag{29}
\]

Exact recentering restores the PSD--Lorentz oracle identity before every
Newton call. But (29) is a nonlinear auxiliary update. Explicitly forming
its Gram matrices, maintaining them in finite precision, or coherently
compiling their ambient entry oracles must be charged.

The companion [implicit recentering and access
theorem](2026-09-04-implicit-psd-fiber-recentering-access.md) makes this
charge precise. It stores (29) as the factorized pair \((W,d)\), computes
the exact centered diagonal in \(O(bs)\) classical work, proves a certified
finite-precision version, and identifies radial scale access as the exact
extra resource needed by the reduced quantum compiler. It also proves
that normalized-state access alone is insufficient and gives a Grover
lower bound when the scales must instead be recovered from coordinate
queries.

There are therefore three defensible QIPM regimes.

1. **Implicit fiber-centered method.** Work directly with the marginal
   barrier. The exact PSD--Lorentz oracle equivalence applies.
2. **Approximately centered ambient method.** Certify (4), use the centered
   Lorentz Hessian as a preconditioner, and charge the \((L/\mu)^2\)
   spectral overhead together with oracle compilation.
3. **Unrestricted ambient method.** No packing-independent conditioning or
   state-generation comparison is possible, by (23)--(28).

No iteration lower bound follows from this trichotomy.

## 6. Scope and literature boundary

The exact quotient calculation is for the explicit column-packed Schur
lift and its restricted standard log-determinant. It permits arbitrary
strictly feasible auxiliary residuals \(D_\ell\), but the projected
objective and additional constraints must depend only on \(x\).

The stability theorem compares Hessian quadratic forms. Its quantum
corollary is conditional on matched block encodings and efficient
preconditioner access; it does not hide \(M(D)^{-1}\), data loading,
precision, or output costs. The counterexample concerns the projected
Newton state at one off-center feasible iterate, not convergence of a full
primal-dual SDP algorithm.

Targeted searches found the standard literature on log-determinant Schur
systems, sparse PSD barriers, and Hessian-barrier methods, including
Andersen, Dahl, and Vandenberghe,
[*Logarithmic barriers for sparse matrix
cones*](https://optimization-online.org/2012/03/3389/), and Srijuntongsiri
and Vavasis,
[*A Fully Sparse Implementation of a Primal-Dual Interior-Point Potential
Reduction Method for Semidefinite
Programming*](https://optimization-online.org/2004/12/1015/).
They did not reveal formula (1), the relative-eccentricity transfer
(5)--(6), or the fixed-projection obstruction (23)--(28). Novelty is
plausible subject to specialist review.
