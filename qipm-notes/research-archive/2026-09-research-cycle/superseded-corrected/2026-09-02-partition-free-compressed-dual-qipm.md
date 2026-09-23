# Partition-free stable dual QIPM with compressed output

Date: 2026-09-02

## Summary

The partition-free active-range construction composes end to end with a dual
logarithmic-barrier QIPM if the output is an explicit low-dimensional dual
certificate plus coherent coordinate access to the primal/slack vectors.
Only the \(m\)-dimensional dual Newton direction is materialized.  Every one
of the \(n\) slacks, the current active selector, and the split stable normal
matrix is regenerated from the static sparse columns and the current dual
iterate.

The composition introduces one essential parameter that a state-only theorem
does not see.  If \(P_\mu=\mu Q+\mu^{-1}(I-Q)\) is the stable left
equilibration and \(g\) is the Newton forcing, define

\[
 J_\mu={\|P_\mu^{-1}\|\,\|P_\mu g\|\over\|g\|}.
\]

An inexact residual for the equilibrated system is amplified by at most
\(J_\mu\) when transferred back to the original Newton equation.  This factor
is \(O(1)\) precisely when the inactive forcing is
\(O(\mu^2)\) relative to the active forcing, but can be
\(\Theta(\mu^{-2})\).  Thus stable conditioning alone is insufficient; stable
forcing is also necessary.

Under bounded \(J_\mu\), bounded RHS preparation, and the active spectral-gap
promises, the theorem below gives a complete compressed-output path ledger
with no \(n\)-coordinate iterate refresh and no polynomial \(1/\mu\) factor.
A separate theorem shows why applying the face repair with a full classical
correction at every iteration loses this gain: its required
\(O(\tau\mu)\) absolute accuracy makes coherent tomography cost
\(\widetilde\Omega(d/(\tau\mu))\), while the same uniformly conditioned sparse
repair can be computed classically in nearly linear time with only logarithmic
precision dependence.

## 1. Dual barrier and compressed access model

Consider

\[
 \min\{c^Tx:Ax=b,\ x\ge0\},
 \qquad
 \max\{b^Ty:A^Ty+s=c,\ s\ge0\},
\tag{1}
\]

where \(A\in\mathbb R^{m\times n}\) has full row rank and at most \(d_c\)
nonzeros per column.  Assume:

1. coherent sparse-column access to \(A\), a static block encoding
   \(A/\alpha_A\) of query cost \(C_A\), and value access to \(b,c\);
2. the current \(B_t\)-bit vector \(y_t\in\mathbb R^m\) is stored in coherent
   memory, with polylogarithmic read cost and \(\widetilde O(mB_t)\) load/update
   work;
3. a strict-complementarity tail with partition \(B\dot\cup N\), constants
   \(\underline x,\overline x,\underline s,\overline s\), and central
   neighborhood bounds as in the partition-free face-repair note;
4. known lower bounds for
   \(\sigma_B=\sigma_{\min}^+(A_B)\) and
   \(\sigma_N=\sigma_{\min}(A_N^T|_{\ker A_B^T})\);
5. an underlying inexact dual-barrier theorem accepting relative Newton
   residual \(\eta\) and taking
   \(T=O(\sqrt n\log(n\mu_0/\epsilon_{\rm opt}))\) tail iterations.

The coherent slack oracle evaluates

\[
 s_i(y_t)=c_i-a_i^Ty_t
\tag{2}
\]

using \(d_c\) column/value accesses and
\(\widetilde O(d_cB_t)\) arithmetic gates.  Define the implicit barrier primal
coordinate \(x_i^b=\mu_t/s_i(y_t)\).  Once the tail separation holds, the
selector

\[
 E_t=\operatorname{Diag}({\bf1}\{x_i^b\ge s_i\})
     =\operatorname{Diag}({\bf1}\{s_i^2\le\mu_t\})
\tag{3}
\]

equals the unknown optimal selector \(P_B\).  It is computed coherently from
(2), not loaded as an \(n\)-bit active set.  The comparison has a constant gap
when performed as \(x_i^b\) versus \(s_i\); evaluating the reciprocal requires
only \(O(\log(1/\mu_t))\) value bits.

The algorithm's primary output is

\[
 \mathcal O_{\rm comp}
 =\bigl(y_T,\mu_T,O_{s,T},O_{x,T}\bigr),
\tag{4}
\]

where \(y_T\) is an explicit dual certificate, \(O_{s,T}\) evaluates (2), and
\(O_{x,T}\) evaluates the minimum-residual primal coordinate used by the dual
method,

\[
 x_i(y_T,\mu_T)
 =\frac{\mu_T}{s_i(y_T)}
  +\frac{\mu_T}{s_i(y_T)^2}a_i^T\Delta y_T.
\tag{5}
\]

The final \(m\)-vector \(\Delta y_T\) is stored with \(y_T\).  Any requested
coordinate costs \(O(d_c)\) coherent sparse accesses.  Enumerating all primal
coordinates remains a separately charged \(\Theta(nd_c)\) output operation.

## 2. Direct partition-free stable Newton system

The dual Newton equation can be scaled as

\[
 G_t\Delta y_t=g_t,
 \qquad
 G_t=\mu_tAS_t^{-2}A^T,
 \qquad
 g_t=b-\mu_tAS_t^{-1}e.
\tag{6}
\]

Put \(E=E_t\), \(F=I-E\), and define

\[
 C_t=\mu_t^2AES_t^{-2}EA^T,
 \qquad
 D_t=AFS_t^{-2}FA^T,
 \qquad
 Q_t=\Pi_{\operatorname{range}(AE)},
 \qquad R_t=I-Q_t.
\tag{7}
\]

Then

\[
 G_t=\mu_t^{-1}C_t+\mu_tD_t.
\tag{8}
\]

The current-value selector and QSVT construct \(Q_t\) without a supplied
partition, in

\[
 \chi_{Q,t}
 =O\!\left({\alpha_A\over\sigma_B}\log(1/\delta_Q)\right)
\tag{9}
\]

sparse/block-encoding queries.  With

\[
 R_{E,t}=\max_{i\in B}s_i^{-1},
 \qquad R_{N,t}=\max_{i\in N}s_i^{-1},
\]

direct product encodings have normalizations

\[
 \alpha_{C,t}=\alpha_A^2\mu_t^2R_{E,t}^2=O(\alpha_A^2),
 \qquad
 \alpha_{D,t}=\alpha_A^2R_{N,t}^2=O(\alpha_A^2),
\tag{10}
\]

where the hidden constants are the strict-complementarity margins.  Assemble

\[
 M_t=C_t+D_t-(1-\mu_t^2)Q_tD_t.
\tag{11}
\]

For the exact projector,

\[
 M_t=P_tG_t,
 \qquad
 P_t=\mu_tQ_t+\mu_t^{-1}R_t.
\tag{12}
\]

The stable active-subspace theorem gives

\[
 \alpha_{M,t}\le
 \alpha_{C,t}+(2-\mu_t^2)\alpha_{D,t},
 \qquad
 \mathcal K_{M,t}:=\alpha_{M,t}\|M_t^{-1}\|=O(1)
\tag{13}
\]

with respect to \(\mu_t\).  Dependence on \(\alpha_A,\sigma_B,\sigma_N\) and
the tail margins remains explicit or hidden only inside the fixed constants.
An operator error \(\delta_Q\) perturbs (11) by \(O(\alpha_D\delta_Q)\), so
the required projector accuracy is the requested solve accuracy, not a power
of \(\mu_t\).

## 3. Direct transformed RHS and the forcing-transfer factor

Strict complementarity implies \(b\in\operatorname{range}A_B\): any optimal
primal point obeys \(b=A_Bx_B^*\).  Therefore \(R_tb=0\).  Instead of applying
the badly normalized \(P_t\) to a prepared \(|g_t\rangle\), assemble its
action algebraically:

\[
 \begin{split}
 \widetilde g_t=P_tg_t
 &=\mu_tb-\mu_t^2AES_t^{-1}Ee\\
 &\quad-\mu_t^2Q_tAFS_t^{-1}Fe
       -R_tAFS_t^{-1}Fe.
 \end{split}
\tag{14}
\]

Every diagonal coefficient in (14) is bounded on the tail.  If \(b\) has
state-preparation normalization \(\alpha_b\), a safe LCU numerator is

\[
 \alpha_{g,t}
 =\mu_t\alpha_b
  +\mu_t^2\alpha_AR_{E,t}\sqrt n
  +(1+\mu_t^2)\alpha_AR_{N,t}\sqrt n.
\tag{15}
\]

Define and charge the actual cancellation/amplification factor

\[
 \Gamma_{g,t}={\alpha_{g,t}\over\|\widetilde g_t\|}.
\tag{16}
\]

A structured RHS oracle may make \(\Gamma_{g,t}=O(1)\); generic uniform-index
LCU need not.  Formula (16) explicitly retains the cancellation that occurs
near a centered point.

The transformed and original residuals are not interchangeable.  If

\[
 \|M_t\widehat z_t-\widetilde g_t\|
 \le\epsilon_{M,t}\|\widetilde g_t\|,
\]

then (12) gives

\[
 {\|G_t\widehat z_t-g_t\|\over\|g_t\|}
 \le J_t\epsilon_{M,t},
 \qquad
 \boxed{
 J_t={\|P_t^{-1}\|\,\|P_tg_t\|\over\|g_t\|}.
 }
\tag{17}
\]

These definitions apply when \(g_t\ne0\).  If \(g_t=0\), the Newton correction
is zero and the solve is skipped; set \(J_t=1\) by convention.

Writing \(u_t=\|Q_tg_t\|\) and \(v_t=\|R_tg_t\|\), the factor is exactly

\[
 J_t=
 {\sqrt{u_t^2+\mu_t^{-4}v_t^2}
  \over\sqrt{u_t^2+v_t^2}}.
\tag{18}
\]

Thus

\[
 \|R_tg_t\|\le C\mu_t^2\|Q_tg_t\|
 \quad\Longrightarrow\quad
 J_t\le\sqrt{1+C^2},
\tag{19}
\]

whereas a nonzero purely inactive forcing has \(J_t=\mu_t^{-2}\).  Equation
(18) is a sharp forcing dichotomy: uniform matrix conditioning removes no
precision dependence unless the realized Newton RHS is also active-aligned.

## 4. End-to-end compressed-output theorem

Define the RHS-specific output amplification

\[
 \rho_t={\alpha_{M,t}\|\Delta y_t\|
               \over\|\widetilde g_t\|}
 \le\mathcal K_{M,t}.
\tag{20}
\]

To meet the original relative residual target \(\eta\), take transformed
residual error \(\epsilon_{M,t}=\Theta(\eta/J_t)\).  Tomography of the
normalized direction and its norm must then have errors

\[
 \xi_t,\chi_t
 =O\!\left({\eta\over J_t\rho_t}\right).
\tag{21}
\]

### Theorem 1 (partition-free compressed dual QIPM)

Under the access and outer-method assumptions in Section 1, the algorithm
(2)--(3), (7)--(16), followed by coherent \(\ell_2\) tomography of
\(\Delta y_t\), produces the compressed output (4).  Its directions satisfy
the original Newton residual contract, so the underlying positivity,
neighborhood, and
\(T=O(\sqrt n\log(n\mu_0/\epsilon_{\rm opt}))\) convergence guarantees apply.

The total number of sparse/block-encoding and RHS-oracle calls is

\[
 \boxed{
 Q_{\rm path}
 =\widetilde O\!\left(
  \sum_{t<T}
  {mJ_t\rho_t\over\eta}\,
  \Gamma_{g,t}\mathcal K_{M,t}\chi_{Q,t}
 \right).
 }
\tag{22}
\]

The gate and data-movement ledger is

\[
 \begin{split}
 G_{\rm path}
 =C_{\rm build}(A)
 +\widetilde O\!\sum_{t<T}\bigg[&
 {mJ_t\rho_t\over\eta}
 \Gamma_{g,t}\mathcal K_{M,t}\chi_{Q,t}
 (C_A+d_cB_t)\\
 &+mB_t\bigg].
 \end{split}
\tag{23}
\]

There is no \(nT\) iterate-write term.  Sufficient arithmetic precision is

\[
 B_t=O\!\left(
 L+\log{J_t\mathcal K_{M,t}\over\eta\mu_t}
 \right),
\tag{24}
\]

because active slacks are \(\Theta(\mu_t)\) and an absolute slack error
\(O(\eta\mu_t/(J_t\mathcal K_{M,t}))\) is a safe bound keeping the active
matrix perturbation below the transformed residual budget.  Fixed
normalization and tail-margin constants are suppressed in (24).

In the favorable promised regime

\[
 J_t,\rho_t,\Gamma_{g,t},\mathcal K_{M,t},
 \chi_{Q,t}=O(1),
 \qquad \eta=\Theta(1),
\tag{25}
\]

the tail complexity simplifies to

\[
 Q_{\rm path}=\widetilde O(Tm),
 \qquad
 G_{\rm path}=C_{\rm build}(A)+
 \widetilde O(Tm(C_A+d_cB_t)).
\tag{26}
\]

This is independent of \(n\) except through the outer iteration count and
static-oracle construction.  It is an end-to-end theorem in the compressed
output model (4), not a claim that arbitrary sparse LPs satisfy (25).

#### Proof

The affine slack identity makes every diagonal and selector query depend only
on the current explicit \(y_t\), so updating the representation costs
\(\widetilde O(mB_t)\).  Equations (7)--(13) give a uniformly normalized,
uniformly conditioned partition-free block encoding.  Equation (14) prepares
the correctly transformed RHS without composing block encodings of \(P_t\)
and \(G_t\).  Equations (17) and (21) make every reconstructed direction obey
the original residual contract.  Tight coherent pure-state tomography uses
\(\widetilde O(m/\xi_t)=\widetilde O(mJ_t\rho_t/\eta)\) state-preparation and
inverse calls.  Multiplying by the QLS, RHS, projector, and oracle costs gives
(22)--(23).  The outer theorem then applies unchanged.

## 5. Classical comparator

The same selector and split are available classically.  One application of
the matrix-free stable operator scans the sparse columns and costs
\(\Theta(nd_c)\) arithmetic in the unstructured column-oracle model.  With
the uniform condition promise, a Krylov solve costs

\[
 \widetilde O\!\left(
 nd_c\log(J_t/\eta)
 \right)
\tag{27}
\]

per direction.  Ignoring the different query/gate units, a necessary regime
for the QLS/tomography route to improve this comparator is

\[
 {mJ_t\rho_t\Gamma_{g,t}\mathcal K_{M,t}\chi_{Q,t}\over\eta}
 =o(nd_c).
\tag{28}
\]

Classical randomized matrix sketches can beat (27) when the column
contributions have bounded leverage or form a bounded average.  Consequently
(28) is a conditional oracle-model comparison, not a universal classical
lower bound.  Static input loading \(C_{\rm build}(A)=\Omega(nd_cB)\) also
removes a sublinear wall-clock claim when the input is supplied as an explicit
file rather than a reusable oracle or formula.

## 6. Sharp boundary for full classical face-repair output

The compressed dual output avoids materializing the \(n\)-dimensional primal
repair.  Requiring that repair as a classical vector at every iteration has a
different complexity.

### Theorem 2 (tomography-based full-repair no-go)

Suppose a repaired lazy trajectory enforces

\[
 \ell_t^+\le K(\mu_t-\mu_{t+1})=\Theta(\tau\mu_t),
\tag{29}
\]

and suppose a face correction of norm \(\Theta(1)\) in dimension \(d\) is
available only through controlled state preparation and its inverse.  Any
generic coherent-tomography implementation that returns the correction as a
classical vector with the worst-case accuracy required by (29) uses

\[
 \boxed{
 \widetilde\Omega\!\left({d\over\tau\mu_t}\right)
 }
\tag{30}
\]

state-oracle calls at iteration \(t\).  Copy-only readout needs quadratic
inverse-accuracy dependence.

In contrast, under the same bounded active gaps, the basis-free filtered
repair systems are uniformly conditioned and have sparse matrix-vector
products.  Classical LSQR/CG computes the full correction to this absolute
accuracy in

\[
 \widetilde O\!\left(
  \operatorname{nnz}(A)\,
  \operatorname{poly}(\chi_p,\chi_d)
  \log{1\over\tau\mu_t}
 \right)
\tag{31}
\]

arithmetic operations.  For constant row/column sparsity and bounded gaps,
(30) is polynomially worse in final central precision than (31), and at fixed
accuracy it cannot asymptotically beat the linear output-size comparator.

#### Proof

An additive error \(u_t\) lying in a primal or dual face subspace survives the
repair projector exactly as leakage of norm \(\|u_t\|\).  Hence the worst-case
contract (29) requires absolute \(\ell_2\) output error
\(O(\tau\mu_t)\).  For a constant-norm state this is normalized-state error
\(O(\tau\mu_t)\).  The tight coherent pure-state tomography lower bound is
\(\widetilde\Omega(d/\epsilon)\), which gives (30).  Uniform condition and
geometric Krylov convergence give (31).

The theorem is scoped to an amplitude-state followed by generic classical
readout.  It does not rule out a concise analytic correction, sparse-support
output, or the affine compressed representation (4).  Those are exactly the
structures needed to escape it.

## 7. Status and novelty boundary

The new positive result is the complete composition of four pieces:

1. current-value recovery of the active partition;
2. direct stable split assembly without a supplied projector;
3. algebraically transformed RHS preparation rather than a separately encoded
   ill-normalized left preconditioner; and
4. an explicit residual-transfer factor \(J_t\) connecting the stable solve to
   the original dual-barrier convergence theorem.

The dual logarithmic-barrier method, affine slack access, active-set prediction,
QSVT projectors, and coherent tomography are established ingredients.  The
combination (14)--(26), especially the sharp forcing dichotomy (18)--(19), was
not found in the reviewed literature.  Theorem 2 records the complementary
full-output boundary and prevents the compressed theorem from being read as a
generic full-vector speedup.

Primary comparators are Wu, Sampourmahani, Mohammadisiahroudi, and Terlaky,
[*A Quantum Dual Logarithmic Barrier Method for Linear
Optimization*](https://arxiv.org/abs/2412.15977), for the outer method, and van
Apeldoorn, Cornelissen, Gily\'en, and Nannicini,
[*Quantum tomography using state-preparation
unitaries*](https://arxiv.org/abs/2207.08800), for the tight coherent readout
bound.

Status: **conditional end-to-end compressed-output theorem, with every
conditioning, forcing, RHS, precision, data-access, and output factor charged;
sharp no-go for generic tomography-based full face-repair output.**
