# Partition-free spectral active-range construction and face-leakage repair

Date: 2026-09-02

## Result in one sentence

On a strictly complementary LP tail, the optimal partition and the bases
\(Z,Y\) in the exact face-leakage repair need not be supplied: the classical
\(x_i\)-versus-\(s_i\) active-set rule has a constant value margin, so a coherent
implementation of that rule and QSVT can construct the two required nullspace
projectors with no polynomial dependence on \(1/\mu\).  This gives a
partition-free *operator implementation*, not a new active-set identification
rule.  It also removes the supplied-active-projector assumption from the
stable normal-equation state solver by directly assembling all split blocks
from \(A,X,S\), with \(\mu\)-independent normalization and condition factors.
It does not by itself give a precision-independent end-to-end full-output
QIPM: materializing an unstructured repaired direction accurately enough for
the summable-leakage ledger by generic tomography costs
\(\widetilde\Theta(d/(\tau\mu))\) coherent queries in dimension \(d\), and
using the untruncated global
weighted projector instead recovers the original \(1/\mu\)-conditioned solve.
The tomography scaling quoted here is a boundary for the generic tomography
route; an LP-specific \(\Omega(d/(\tau\mu))\) output lower bound is not proved.

## 1. Assumptions and automatic partition recovery

Let \(A\in\mathbb R^{m\times n}\) have full row rank.  Suppose a feasible
strict-complementarity tail has the fixed optimal partition \(B\dot\cup N\)
and satisfies

\[
 \underline x\le x_i\le\overline x\quad(i\in B),
 \qquad
 \underline s\le s_i\le\overline s\quad(i\in N),
\tag{1}
\]

and

\[
 (1-\theta)\mu\le x_is_i\le(1+\theta)\mu.
\tag{2}
\]

Assume coherent fixed-point value oracles for \(x_i,s_i\), a sparse/block
encoding of \(A/\alpha_A\), and enough bits to represent the current values
with error below one quarter of the promised comparison margin.
Known lower bounds on the nonzero active singular gaps are also required to
set the QSVT thresholds; all such gaps are displayed below.  Without them, an
adaptive singular-value search must be charged.
Under the usual polynomial LP bit-complexity bounds (or when \(L\) includes
the bit size of the promised tail constants), the number of value bits is
\(O(\operatorname{poly}(L)+\log(1/\mu))\);
coherent arithmetic is polynomial in this bit count, not in \(1/\mu\).
The oracle model charges a query after the current QRAM/value structure exists.
Loading or rewriting a dense explicit iterate costs \(\Theta(n)\) classical
writes per round and is not hidden in the selector cost.

Define the current selector

\[
 E=\operatorname{Diag}({\bf1}\{x_i\ge s_i\}),
 \qquad F=I-E.
\tag{3}
\]

### Lemma 1 (constant-margin form of a classical tail-identification rule)

If

\[
 \mu\le {1\over2(1+\theta)}
       \min\{\underline x^2,\underline s^2\},
\tag{4}
\]

then \(E=P_B\), the coordinate projector onto \(B\), and every comparison in
(3) has absolute margin at least
\(\frac12\min\{\underline x,\underline s\}\).

#### Proof

For \(i\in B\), (1)--(2) give
\(s_i\le(1+\theta)\mu/\underline x\le\underline x/2\le x_i/2\).
For \(i\in N\), they give
\(x_i\le(1+\theta)\mu/\underline s\le\underline s/2\le s_i/2\).
Thus the current values identify the limiting partition with a constant
absolute gap.  A reversible comparator uses two value queries and
\(\operatorname{poly}(L+\log(1/\mu))\) gates when \(L\) denotes the stored
input/tail bit bound.  It does not scan all
coordinates and does not use amplitude estimation.

This lemma is an oracle statement.  If the iterates are available only as
amplitude-encoded states, constructing the coordinate selector is subject to
the separate state-to-diagonal query--normalization obstruction.
It is also a tail theorem: an implementation must know a safe bound implying
(4), or run the ordinary method until a separate strict-complementarity
separation certificate succeeds.  The theorem does not infer the unknown
constants \(\underline x,\underline s\) for free.
The comparison itself is not new: Mehrotra--Ye already proposed comparing
primal variables with dual slacks to identify the optimal face.  The content
used below is the explicit constant-margin consequence of (1)--(4), together
with its coherent-query implementation.
The test \(x_i\ge s_i\) is not invariant under diagonal rescaling of the primal
variables: the reciprocal rescaling of \(x_i\) and \(s_i\) changes the constants
in (1) and hence the safe tail threshold (4).  All margin and bit-complexity
claims are therefore for the fixed input scaling; they are not uniform over
affinely equivalent formulations.

### Theorem 1a (automatic stable active-range equilibration)

The same selector removes the supplied-active-projector assumption from the
stable normal-equation construction.  Define, directly from current data,

\[
 C_\mu=\mu AEXS^{-1}EA^T,
 \qquad
 D_\mu=\mu^{-1}AFXS^{-1}FA^T,
 \qquad
 Q_U=\Pi_{\operatorname{range}(AE)}.
\tag{4a}
\]

Then the ordinary normal matrix is exactly

\[
 H_\mu=AXS^{-1}A^T=\mu^{-1}C_\mu+\mu D_\mu.
\tag{4b}
\]

Moreover, direct diagonal/product encodings have the \(\mu\)-independent
normalizations

\[
 \alpha_C\le
 \alpha_A^2{\overline x^2\over1-\theta},
 \qquad
 \alpha_D\le
 \alpha_A^2{1+\theta\over\underline s^2}.
\tag{4c}
\]

Given \(\sigma_B=\sigma_{\min}^+(A_B)>0\), QSVT constructs \(Q_U\) from the
block encoding of \(AE/\alpha_A\) using

\[
 O\!\left({\alpha_A\over\sigma_B}\log(1/\delta)\right)
\tag{4d}
\]

queries.  Therefore the directly assembled operator

\[
 M_\mu=C_\mu+D_\mu-(1-\mu^2)Q_UD_\mu
\tag{4e}
\]

has normalization at most
\(\Gamma_M=\alpha_C+(2-\mu^2)\alpha_D\).  To make the conditioning claim
precise, assume for constants independent of \(\mu\) that

\[
 \|C_\mu\|,\|D_\mu\|\le L,\qquad
 C_\mu|_U\succeq cI_U,\qquad
 (I-Q_U)D_\mu(I-Q_U)|_{U^\perp}\succeq dI_{U^\perp},
\tag{4e'}
\]

where \(U=\operatorname{range}(AE)\) and \(c,d>0\).  These are not mysterious
extra LP assumptions: (1)--(2) imply
\[
 C_\mu|_U\succeq
 {\underline x^2\over1+\theta}\sigma_B^2 I_U,\qquad
 (I-Q_U)D_\mu(I-Q_U)|_{U^\perp}\succeq
 {1-\theta\over\overline s^2}
 \sigma_{\min}(A_N^T|_{U^\perp})^2 I_{U^\perp},
\tag{4e''}
\]
while (4c) bounds \(L\).  Full row rank makes the second restricted singular
value positive, although its numerical size must still be charged.  Then
\(M_\mu\), which is
generally nonsymmetric, has bounded largest singular value and bounded inverse
norm (for the sufficiently small tail under discussion), with constants
depending only on \(L,c,d\).  Consequently constant operator error in \(Q_U\),
chosen below the resulting singular-value margin, suffices for constant
solution-state error.  If the normal-equation RHS \(f\) lies in
\(\operatorname{range}(AE)\), then

\[
 M_\mu^{-1}f=\mu^{-1}H_\mu^{-1}f,
\tag{4f}
\]

so the normalized Newton state is unchanged.  With RHS-preparation factor
\(\Gamma_f\), its state-preparation query ledger is conservatively

\[
 \widetilde O\!\left(
  \Gamma_f\Gamma_M\|M_\mu^{-1}\|
  {\alpha_A\over\sigma_B}
 \right),
\tag{4g}
\]

where all displayed factors are independent of \(\mu\); logarithmic solver
and projector errors are suppressed.  A supplied \(Q_U\) removes the final
gap factor.  Equation (4g) charges the coherent selector and current diagonal
arithmetic as constant-query, polylogarithmic-bit operations.

#### Proof

Equations (4a)--(4b) are the selected-column decomposition.  On \(B\),
\(\mu x_i/s_i=\mu x_i^2/(x_is_i)\le\overline x^2/(1-\theta)\); on \(N\),
\(\mu^{-1}x_i/s_i=(x_is_i)/(\mu s_i^2)\le(1+\theta)/\underline s^2\).
This proves (4c).  QSVT applied to \(AE\) gives (4d).  With
\(P_\mu=\mu Q_U+\mu^{-1}(I-Q_U)\), direct multiplication gives
\(M_\mu=P_\mu H_\mu\), which proves (4e)--(4f).  In the decomposition
\(U\oplus U^\perp\), (4e') makes the diagonal blocks uniformly invertible and
the upper off-diagonal block is \(O(\mu^2)\); a Schur-complement bound gives the
stated singular-value conditioning.  This is the stable active-subspace
equilibration argument, now with every input operator constructed from
\(A,X,S,\mu\).  Multiplying
the direct-encoding, QLS, RHS, and projector-query costs gives (4g).

This is strictly stronger in access assumptions than the earlier
supplied-active-projector result.  It is still a tail and state-output theorem:
it assumes the separation promise (4), the active singular gap, the stable
block bounds, and an RHS in the active range.  It does not supply a classical
next iterate without readout.  A generic feasible- or infeasible-start Newton
RHS need not lie exactly in that range; for such an RHS one must either retain
the complementary component or prove that discarding it is below the required
step tolerance.  Equation (4f) is not an unconditional identity for every IPM
Newton step.

## 2. Basis-free exact formulas

Write all diagonal matrices below as zero outside their selected support and
define

\[
 T=E\sqrt{XS^{-1}}E,
 \qquad B_r=E(XS)^{-1/2}E,
 \qquad K=AT.
\tag{5}
\]

Let \(\Pi_p\) be the Euclidean projector onto \(\ker K\), and let

\[
 Q=\Pi_{\ker K^T}=\Pi_{\ker(AE)^T}.
\tag{6}
\]

The equality of the left kernels follows because \(T\) is invertible on
\(B\).  Thus \(Q=I-Q_U\) once Lemma 1 applies.  Notice that \(T\) is zero on
\(N\), so \(\ker K\) also contains the whole \(N\)-coordinate subspace; the
selected factors in (8) annihilate this harmless extra summand.  For the
inactive block put

\[
 D_N=FXS^{-1}F,
 \qquad H_N=AD_NA^T,
 \qquad c_N(r)=QAFS^{-1}Fr.
\tag{7}
\]

### Theorem 2 (partition- and basis-free face repair)

Under (1)--(4), the two dangerous errors in equations (66)--(70) of the
lazy-refresh note equal

\[
 \boxed{
 p_F(r)=T\Pi_pB_rr,
 \qquad
 q_F(r)=-(QH_NQ)^+c_N(r).
 }
\tag{8}
\]

Consequently

\[
 \widehat{\Delta x}^{+}=\widehat{\Delta x}-p_F(r),
 \quad
 \widehat{\Delta y}^{+}=\widehat{\Delta y}-q_F(r),
 \quad
 \widehat{\Delta s}^{+}=\widehat{\Delta s}+A^Tq_F(r)
\tag{8a}
\]

is exactly repair (78), without being given \(B,N,Z\), or \(Y\).

#### Proof

On \(B\), put \(W=X_B^{-1}S_B\).  If \(Z\) spans \(\ker A_B\), then
\(W^{1/2}Z\) spans
\(\ker(A_BW^{-1/2})=\ker K\) inside the \(B\)-coordinate subspace.  Hence

\[
 \Pi_p
 =W^{1/2}Z(Z^TWZ)^{-1}Z^TW^{1/2}
\tag{9}
\]

on the \(B\)-coordinate subspace.  On the full space its kernel projector also
has the direct summand \(F\), but both \(B_r r\) and the final multiplication
by \(T\) are \(B\)-supported.  Since
\(W^{-1/2}X_B^{-1}=(X_BS_B)^{-1/2}\), sandwiching (9) as in (8) gives
\(Z(Z^TWZ)^{-1}Z^TX_B^{-1}r_B\), exactly \(p_F(r)\).

The range of \(Q\) is \(\ker A_B^T\).  Restricted to this range, \(H_N\)
is positive definite because \(A\) has full row rank.  Therefore
\((QH_NQ)^+Q\) is the coordinate-free inverse of the \(H_N\) bilinear form
on \(\ker A_B^T\).  Expressing it in any basis \(Y\) of that space gives
\(Y(Y^TH_NY)^{-1}Y^T\), which turns the second formula in (8) into (67).

## 3. Quantum construction and all condition parameters

From (1)--(2),

\[
 {\underline x\over\sqrt{(1+\theta)\mu}}
 \le T_{ii}\le
 {\overline x\over\sqrt{(1-\theta)\mu}}
 \quad(i\in B).
\tag{10}
\]

A diagonal block encoding of \(T/R_T\) may therefore use

\[
 R_T={\overline x\over\sqrt{(1-\theta)\mu}},
 \qquad
 \alpha_K=\alpha_AR_T.
\tag{11}
\]

Let \(\sigma_B=\sigma_{\min}^+(A_B)\).  Since
\(K K^T=A_BT_B^2A_B^T\) and
\(T_B^2\succeq t_-^2I\),

\[
 \sigma_{\min}^+(K)\ge
 {\underline x\over\sqrt{(1+\theta)\mu}}\sigma_B.
\tag{12}
\]

Thus QSVT implements both projectors in (6), to operator error \(\delta\),
using

\[
 \boxed{
 O\!\left(\chi_p\log(1/\delta)\right),
 \qquad
 \chi_p\le
 {\alpha_A\over\sigma_B}
 {\overline x\over\underline x}
 \sqrt{{1+\theta\over1-\theta}}
 }
\tag{13}
\]

queries.  The active-submatrix conditioning is charged, but there is no
polynomial \(1/\mu\) factor.  The block encoding of the complete primal
correction map in (8) has normalization

\[
 \alpha_p=R_T R_B,
 \qquad R_B={1\over\sqrt{(1-\theta)\mu}},
 \qquad \alpha_p=O(1/\mu).
\tag{14}
\]

When \(\ker A_B\ne\{0\}\), the face-error map has
\(\Theta(1/\mu)\) norm under the fixed tail constants, so this scaling is not
merely a block-encoding artifact.  If \(\ker A_B=\{0\}\), the primal repair map
is zero and no such lower statement applies.  Applied to an \(O(\mu)\) residual
aligned with a nonzero dangerous face, it has constant state-preparation
success.  For a general residual the exact RHS-specific amplification is

\[
 \Gamma_p(r)={\alpha_p\|Er\|\over\|p_F(r)\|},
\tag{15}
\]

in addition to the cost of preparing \(|Er\rangle\).  It can be large when
the leakage is tiny; in that regime an implementation should certify that the
correction is below its target rather than prepare its normalized state.

For the dual correction, (1)--(2) give

\[
 { (1-\theta)\mu\over\overline s^2}F
 \preceq D_N\preceq
 { (1+\theta)\mu\over\underline s^2}F.
\tag{16}
\]

Let
\(\sigma_N=\sigma_{\min}(A_N^T|_{\ker A_B^T})>0\).  A product block encoding
of \(H_N\) has normalization

\[
 \alpha_H=\alpha_A^2{(1+\theta)\mu\over\underline s^2},
\tag{17}
\]

while the smallest eigenvalue of \(QH_NQ\) on \(\operatorname{range}Q\) is
at least \((1-\theta)\mu\sigma_N^2/\overline s^2\).  Its effective inverse
parameter is therefore

\[
 \boxed{
 \chi_d\le
 {\alpha_A^2\over\sigma_N^2}
 {1+\theta\over1-\theta}
 {\overline s^2\over\underline s^2},
 }
\tag{18}
\]

again independent of \(\mu\).  Preparing \(c_N(r)\) by applying the encoded
\(QAFS^{-1}F\) has the additional factor

\[
 \Gamma_d(r)=
 {\alpha_A\underline s^{-1}\|Fr\|\over\|c_N(r)\|},
\tag{19}
\]

with the supplied upper bound on \(S_N^{-1}\) substituted if larger.  Norm
recovery for \(q_F\) has RHS-specific factor
\(\rho_d=\alpha_H\|q_F\|/\|c_N(r)\|\le\chi_d\).

For completeness, let \(\Gamma_{r,B}\) and \(\Gamma_{r,N}\) denote the costs
of preparing the normalized selected residuals from their value oracle.  In
units of sparse-\(A\) and current-value queries, normalized correction-state
preparation has the conservative ledgers

\[
 Q_p=\widetilde O(\Gamma_{r,B}\Gamma_p\chi_p),
 \qquad
 Q_d=\widetilde O(\Gamma_{r,N}\Gamma_d\chi_p\chi_d),
\tag{19a}
\]

where logarithms in projector, QLS, and arithmetic precision are suppressed.
The \(\chi_p\) in \(Q_d\) charges construction of \(Q\); two uses of \(Q\) per
block encoding change only constants.  If an implementation supplies selected
residual states or the range projector directly, the corresponding factor is
removed.  Classical norm output adds amplitude-estimation dependence through
\(\rho_d\) and the analogous primal success amplitude; full vector output is
charged in Section 6.

Equations (13)--(19) are the promised full operator ledger.  They improve on
the supplied-active-projector theorem: neither the optimal partition nor a
block encoding of \(A_B\), \(Z\), or \(Y\) is an input.  They do not remove
the input-dependent gaps \(\sigma_B,\sigma_N\), RHS preparation, or output.

## 4. A genuinely spectral alternative for the dual range

The active range can also be obtained without the coordinate comparator.
Form the current scaled normal matrix

\[
 \mathcal C_\mu=\mu AXS^{-1}A^T=C_B+E_N.
\tag{20}
\]

Here \(\operatorname{range}C_B=\operatorname{range}A_B=:U\), its smallest
positive eigenvalue is at least

\[
 c_U={\underline x^2\over1+\theta}\sigma_B^2,
\tag{21}
\]

and

\[
 \|E_N\|\le
 {1+\theta\over\underline s^2}\mu^2\|A_N\|^2.
\tag{22}
\]

For sufficiently small \(\mu\), QSVT filtering at threshold \(c_U/2\)
constructs the high-eigenvalue projector \(\widetilde Q_U\).  Davis--Kahan
perturbation and polynomial approximation give

\[
 \|\widetilde Q_U-Q_U\|
 =O(\mu^2\|A_N\|^2/c_U)+\delta.
\tag{23}
\]

The direct block encoding of (20) has bounded normalization
\(\alpha_C=O(\alpha_A^2)\), so the filter degree is

\[
 O\!\left({\alpha_C\over c_U}\log(1/\delta)\right),
\tag{24}
\]

with no polynomial \(1/\mu\) dependence.  Taking
\(\delta=O(\tau\mu)\) makes the *projector* error compatible with the pointwise
leakage budget once \(\mu=O(\tau)\), provided the downstream restricted inverse
has the uniform stability in (18).  The natural \(O(\mu^2)\) subspace bias is
then small enough.  This statement must not be read as applying an approximate
projector to the unscaled ill-conditioned normal equations, where leakage can
be amplified.  The construction removes the hard coordinate decision only for
the dual range \(Q=I-Q_U\): the formula for \(H_N\) and \(c_N\) in (7) still
uses \(F\), so the complete dual repair is not selector-free without an
additional way to construct those inactive blocks.  The primal repair still
needs either the
coordinate selector (3) or an equivalent support filter to keep its correction
on the optimal face.

## 5. Why the untruncated partition-free projector fails

There is a tempting formula using no active filter.  Put

\[
 W=X^{-1}S,
 \quad T_{\rm all}=W^{-1/2},
 \quad K_{\rm all}=AT_{\rm all}.
\tag{25}
\]

Projecting the full residual onto \(\ker K_{\rm all}\) gives

\[
 T_{\rm all}\Pi_{\ker K_{\rm all}}
 T_{\rm all}X^{-1}r=e_x,
\tag{26}
\]

the entire primal Newton error, not only its face leakage.  Likewise the full
dual formula uses
\((AXS^{-1}A^T)^{-1}AS^{-1}r\).  Thus exact global weighted repair is simply
another representation of solving the original Newton error equation.

This equivalence has a constant-row-sparse sharp witness.  Let

\[
 A=\begin{bmatrix}1&1&0&0\\0&0&1&-1\end{bmatrix},
 \quad b=(1,0),
 \quad c=(0,0,1,1),
\tag{27}
\]

and consider its exact central path

\[
 x=(1/2,1/2,\mu,\mu),
 \quad y=(-2\mu,0),
 \quad s=(2\mu,2\mu,1,1).
\tag{28}
\]

Then \(B=\{1,2\}\), \(N=\{3,4\}\), and

\[
 K_{\rm all}K_{\rm all}^T
 =\operatorname{Diag}((2\mu)^{-1},2\mu),
 \qquad
 \kappa(K_{\rm all})={1\over2\mu},
\tag{29}
\]

while

\[
 AXS^{-1}A^T
 =\operatorname{Diag}((2\mu)^{-1},2\mu),
 \qquad
 \kappa(AXS^{-1}A^T)={1\over4\mu^2}.
\tag{30}
\]

Both primal and dual face corrections can have constant norm for an
\(O(\mu)\) residual: use respectively
\(r=2\mu d(1,-1,0,0)\) or
\(r=\mu d(0,0,-1,1)\).  Hence the bad scales in (29)--(30) are relevant, not
unused worst-direction singular values.

A Tikhonov kernel filter does not evade the same witness.  For

\[
 P_\lambda=\lambda(K_{\rm all}^TK_{\rm all}+\lambda I)^{-1},
\tag{30a}
\]

the multiplier on the smallest positive singular direction is
\(\lambda/(2\mu+\lambda)\).  Approximating the true kernel projector to error
at most \(\delta<1/2\) therefore forces

\[
 \lambda\le {2\delta\over1-\delta}\mu.
\tag{30b}
\]

Because the matrix in (30a) also has exact-kernel eigenvalue \(\lambda\) and
largest eigenvalue \(\Theta(1/\mu)\), its condition number is then

\[
 \Omega(1/(\delta\mu^2)).
\tag{30c}
\]

Direct QSVT filtering of \(K_{\rm all}\) has the same qualitative obstruction:
after normalization by \(\|K_{\rm all}\|=\Theta(\mu^{-1/2})\), its smallest
positive singular value is \(\Theta(\mu)\), so a uniform step filter has
degree \(\Omega(1/\mu)\).  Regularization only moves the active-cluster
resolution cost into the shifted inverse.

Equations (26)--(30) prove the dichotomy: an exact partition-free *unfiltered*
projector can reintroduce \(1/\mu\) (or \(1/\mu^2\) in normal equations).
Avoiding it requires resolving the active/inactive spectral clusters.  On the
strictly complementary tail that resolution is cheap by (3), (13), or
(20)--(24), but it is logically equivalent to learning the active range.

## 6. Output and iteration-composition barrier

Suppose the repaired lazy trajectory is required to satisfy the pointwise
ledger

\[
 \ell_t^+\le C(\mu_t-\mu_{t+1})=\Theta(\tau\mu_t).
\tag{31}
\]

An additive implementation error \(u_t\) in either face correction can produce
face leakage \(\Theta(\|u_t\|)\): if \(u_t\) lies in the corresponding face
subspace, the weighted face projection of the corrected direction retains
\(u_t\) exactly (up to the sign convention).  Therefore a uniform worst-case
implementation must output the relevant corrections to absolute
\(\ell_2\) error

\[
 \delta_t=O(\tau\mu_t).
\tag{32}
\]

For a generic unknown correction state of constant norm in dimension \(d\)
(\(d=n\) for the primal correction and \(d=m\) for the dual correction),
coherent pure-state tomography with a state-preparation unitary and its inverse
has tight (up to logarithms) query complexity

\[
 \widetilde\Theta(d/\delta_t)
 =\widetilde\Theta\!\left({d\over\tau\mu_t}\right)
\tag{33}
\]

state-preparation/inverse calls; standard copy-only tomography is quadratic in
\(1/\delta_t\).  Recovering an actual real Newton vector additionally requires
its norm and a reference that fixes the state's otherwise unobservable global
phase/sign.  Providing those does not weaken the tomography lower bound and
may add cost.  The sparse witness (27)--(30) realizes the constant correction
norm and the required absolute-error scale, but, being four-dimensional, it
does **not** establish the \(d\)-dependent tomography lower bound for the family
of LP corrections.  Thus (33) cannot be omitted when the chosen implementation
literally uses generic tomography to obtain an unstructured classical
correction; no LP-specific \(\Omega(d/\delta_t)\) output lower bound is claimed,
and a problem-specific classical formula could evade it.  Estimating
whether a correction is below \(\delta_t\) also
has inverse-signal dependence when the leakage is near the threshold.

Keeping the correction only as an amplitude state avoids (33) for state or a
few observables, but does not give the coherent coordinate values of the next
\(x,s\).  Those values are needed by (3), by the changing diagonal block
encodings, and by the next complementarity residual.  A generic conversion
from a state-preparation oracle to a well-normalized diagonal/value oracle obeys
the separate query--normalization product lower bound.  An implicit-coordinate
QIPM can escape only when problem structure supplies those coordinate values
directly; that is an additional oracle promise, not a consequence of the
spectral filter.

The final algorithmic conclusion is therefore two-sided:

1. **Positive primitive.** With coherent current-coordinate access, the exact
   face-repair operators are constructible without a supplied optimal
   partition or bases, and their projector gaps and restricted-inverse
   condition parameters are independent of \(\mu\).  The primal map still has
   the genuine \(O(1/\mu)\) normalization and RHS-specific amplification in
   (14)--(15).  The same selector makes the stable active-range Newton-state
   solver fully constructible from current data.  Only logarithmic precision
   dependence enters projector construction.
2. **End-to-end boundary.** In a hybrid QIPM that materializes each repaired
   iterate by generic coherent tomography, enforcing the summable-leakage
   accuracy restores an inverse-\(\mu\) output cost.  This is a limitation of
   that extraction route, not an LP-specific output lower bound.  Without
   filtering, the inverse-\(\mu\) cost already appears in conditioning.  Thus
   the new construction improves the
   supplied-projector assumption but does not establish a full-output quantum
   speedup.

## 7. Classical comparison and literature boundary

With explicit iterates, a classical implementation identifies (3) in
\(O(n)\), applies every sparse matrix in \(O(\operatorname{nnz}A)\), and then
uses a rank-revealing factorization or Krylov solve whose cost depends on
\(\sigma_B,\sigma_N\).  The quantum primitive replaces the scan and explicit
bases by coherent comparison and spectral filters, so it is meaningful for
state/few-observable output.  It does not beat the classical full-vector
baseline after (33) is charged.

Classical identification of the optimal face from an IPM tail is old.  In
particular, Mehrotra and Ye,
[*Finding an interior point in the optimal face of linear programs*](https://doi.org/10.1007/BF01585180),
proposed comparing primal variables with dual slacks.  Cartis and Yan,
[*Active-set prediction for interior point methods using controlled
perturbations*](https://doi.org/10.1007/s10589-015-9791-z), review this and
other cutoff rules and prove later active-set predictions.  Thus Lemma 1's
rule and the general idea of switching to an identified face are not novel.
The weighted projectors in (8) are also standard linear-algebraic projector
and Schur-complement identities; their value here is the exact translation of
the previously defined face-leakage repair, not a new projector identity.
Classical active-partition preconditioning is likewise established.  Chai and
Toh,
[*Preconditioning and iterative solution of symmetric indefinite linear
systems arising from interior point methods for linear
programming*](https://doi.org/10.1007/s10589-006-9006-8), transform and
precondition a reduced augmented IPM system using a predicted partition.

On the quantum side, singular-value threshold projectors and pseudoinverses are
standard consequences of Gilyén, Su, Low, and Wiebe,
[*Quantum singular value transformation and beyond*](https://arxiv.org/abs/1806.01838).
Quantum preconditioning also predates this note; see Tong, An, Wiebe, and Lin,
[*Fast inversion, preconditioned quantum linear system solvers, and fast
evaluation of matrix functions*](https://arxiv.org/abs/2008.13295).
Lapworth and Sünderhauf,
[*Preconditioned Block Encodings for Quantum Linear Systems*](https://arxiv.org/abs/2502.20908),
show why block-encoding subnormalization can erase a nominal conditioning gain.
That makes the direct bounded normalizations (4c), rather than the abstract
left preconditioner alone, the material part of Theorem 1a.  Finally, the
\(\widetilde\Theta(d/\epsilon)\) coherent tomography statement is due to van
Apeldoorn, Cornelissen, Gilyén, and Nannicini,
[*Quantum tomography using state-preparation unitaries*](https://arxiv.org/abs/2207.08800),
not a new lower bound here.

The closest QIPM collision is Wu, Yang, and Terlaky,
[*A preconditioned inexact infeasible quantum interior point method for linear
optimization*](https://doi.org/10.1007/s10589-025-00750-4).  It already builds
a quantum IPM preconditioner from an estimated optimal partition, adapting the
Chai--Toh construction, and proves an improvement from
\(O(\mu^{-2})\) to \(O(\mu^{-1})\) conditioning before charging tomography and
classical updates.  Therefore neither “partition-estimated QIPM
preconditioning” nor “better tail conditioning” is new here.  The narrower
distinction of (4a)--(4g) is an exact active-range left equilibration for an
active-range RHS, with a directly assembled block encoding whose
normalization and singular conditioning are both \(O(1)\) in \(\mu\) under
(4e').  It is a stronger tail promise and a state-output contract, not a
replacement end-to-end infeasible QIPM.
Recent almost-exact/iterative-refinement proposals also explicitly target the
precision and readout bottleneck; for example Mohammadisiahroudi et al.,
[*Optimal Scaling Quantum Interior Point Method for Linear
Optimization*](https://arxiv.org/abs/2512.04510), claim logarithmic
\(1/\epsilon\) dependence by combining quantum Newton solves with classical
updates and refinement.  Whatever the final status of that preprint, it is
another reason to read Section 6 only as a lower bound on repeatedly applying
generic tomography at the raw target accuracy, not as a universal QIPM
precision lower bound.

The most defensible apparently new content is the combination of (i) coherent
construction, from current LP coordinates, of the exact previously defined
face-leakage maps, (ii) direct split block encodings whose normalization and
singular-value parameters are independent of \(\mu\) under the explicit tail
gaps, and (iii) the sparse witness showing why the unfiltered weighted
projector loses that property.  Equations (13)--(19) give a useful complete
oracle ledger.  No reviewed source was found with this exact combination, but
the individual active-set, weighted-projector, QSVT, preconditioning, and
tomography ingredients are established prior art.

Status: **proved operator-level lemma suite and a generic-tomography
composition warning; not a matched LP output lower bound or an end-to-end
full-output QIPM speedup.**
