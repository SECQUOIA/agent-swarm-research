# Proximal and residual-certified reuse for feasible OSS QIPMs

Date: 2026-09-02

Verification correction, 2026-09-20: the pathwise refresh bound is now
formalized in [the Lean verification report](../../../formal/REFRESH.md).
Part 3 of Theorem 1 below requires an exact test or a certified rejection
condition, in addition to safe acceptance. Safe acceptance alone does not
bound the number of solves. Only the pathwise theorem is formalized; the
OSS convergence, proximal analysis, and quantum ledgers in this note are not.

## Summary

Checkpoint reuse can be made into a convergent feasible-OSS algorithm by a
simple rule: scalar-rescale the cached classical coefficient vector, compute
its current OSS residual, and reuse it only when the residual satisfies the
same inexactness contract as the underlying feasible IPM.  Every accepted
direction is exactly primal--dual feasible, and the published short-step
convergence proof applies without change. Conditional on the directed
cross-gain bound, checkpoint accuracy, and the exact residual test specified
below, the number of QLS/tomography refreshes is bounded by projective variation.

This does not automatically give a sublinear sparse algorithm.  An exact
classical residual test costs one OSS matrix--vector product per IPM round.  A
quantum residual test has an explicit amplitude factor and can be as hard as
state verification.  It replaces the classical scan only in an access model
where the tested residual has a well-normalized coherent value or state oracle.

Tikhonov/proximal selection prevents the particular arbitrary rotating choice
at one solve, but the row-3-sparse witness shows that continuity of the
coefficient ray is not the same as contraction of the primal iterate.  It does
not give a generic conditioning improvement under the residual contract.
A regularization large enough to improve the OSS condition can retain too much
of an invalid checkpoint direction.  Choosing it small enough to guarantee the
required residual leaves the original \(1/\mu\) singular-value scale.  Thus
proximal regularization is useful after residual certification or with an
additional spectral error promise; it is not a replacement for certification.

## 1. Feasible OSS and access model

Let \(A\in\mathbb R^{m\times n}\) have full row rank.  At a primal--dual
feasible LP point, let \(V\in\mathbb R^{n\times(n-m)}\) be a fixed
full-column-rank basis of \(\ker A\).  The orthogonal-subspaces system is

\[
 \mathcal M_t z_t=f_t,
 \qquad
 \mathcal M_t=[-X_tA^T\ \ S_tV],
 \qquad
 z_t=(\Delta y_t,\lambda_t),
\tag{1}
\]

with

\[
 f_t=\beta\mu_t e-X_ts_t,
 \qquad
 \Delta x_t=V\lambda_t,
 \qquad
 \Delta s_t=-A^T\Delta y_t.
\tag{2}
\]

For every coefficient vector, exact or approximate,

\[
 A\Delta x_t=0,
 \qquad A^T\Delta y_t+\Delta s_t=0.
\tag{3}
\]

Assume block encodings of \(A^T/\alpha_A\) and \(V/\alpha_V\), coherent
value access to \(x_t,s_t\), and known bounds

\[
 R_x\ge\|x_t\|_\infty,
 \qquad R_s\ge\|s_t\|_\infty.
\]

Value-to-amplitude diagonal encodings followed by products and LCU give a
block encoding of (1) with normalization

\[
 \boxed{\alpha_{\mathcal M,t}=R_x\alpha_A+R_s\alpha_V.}
\tag{4}
\]

The effective QLS parameter is

\[
 \mathcal K_t=\alpha_{\mathcal M,t}\|\mathcal M_t^{-1}\|.
\tag{5}
\]

For RHS preparation, a coherent coordinate circuit computes
\((f_t)_i=\beta\mu_t-x_{t,i}s_{t,i}\).  Uniform-index controlled rotation has
amplification factor

\[
 \Gamma_{f,t}
 =\frac{\sqrt n\,F_{\infty,t}}{\|f_t\|_2},
 \qquad F_{\infty,t}\ge\|f_t\|_\infty.
\tag{6}
\]

For the usual \(N_2(\theta)\) neighborhood and
\(\beta=1-a_0/\sqrt n\), the vectors \(e\) and
\(X_ts_t-\mu_te\) are orthogonal because
\(e^T(X_ts_t-\mu_te)=0\).  Consequently

\[
 \|f_t\|^2
 =a_0^2\mu_t^2+\|X_ts_t-\mu_te\|^2,
 \qquad
 a_0\mu_t\le\|f_t\|\le\sqrt{a_0^2+\theta^2}\,\mu_t.
\tag{6a}
\]

Thus the relative contract used below is equivalent, up to explicit fixed
constants, to the published feasible-IF-IPM contract stated as an absolute
multiple of \(\mu_t\).

Thus one normalized OSS solution-state preparation by a conventional QLS
routine costs, up to logarithms and block-encoding error budgets,

\[
 Q_{\rm state,t}
 =\widetilde O(\Gamma_{f,t}\mathcal K_t).
\tag{7}
\]

Coherent \(\ell_2\) tomography of the \(n\)-dimensional coefficient state to
normalized error \(\xi_t\) uses
\(\widetilde O(n/\xi_t)\) controlled state-preparation/inverse calls.  Norm
recovery and the sign convention are additional charged operations.  Sparse
tomography may improve this only under a separate threshold/tail promise.
Normalized-state error is not yet OSS residual error.  Define the
RHS-specific output amplification

\[
 \rho_t
 =\frac{\alpha_{\mathcal M,t}\|z_t\|}{\|f_t\|}
 \le \mathcal K_t.
\tag{7a}
\]

If the normalized direction and its norm are recovered to errors \(\xi_t\)
and relative \(\chi_t\), respectively, then, up to the product term,

\[
 \frac{\|\mathcal M_t\widehat z_t-f_t\|}{\|f_t\|}
 \le \rho_t(\xi_t+\chi_t+\xi_t\chi_t)
       +\epsilon_{{\rm QLS-res},t}.
\tag{7b}
\]

Here \(\epsilon_{{\rm QLS-res},t}\) denotes the QLS approximation's
contribution measured directly in relative OSS residual; a normalized QLS
state error \(\zeta_t\) bounds it only by \(\rho_t\zeta_t\).  Thus a
worst-case residual target \(\epsilon\) requires
\(\xi_t,\chi_t,\zeta_t=O(\epsilon/\rho_t)\).  One dense
coherent-tomography refresh consequently costs

\[
 \widetilde O\!\left(
   \Gamma_{f,t}\mathcal K_t\frac{n\rho_t}{\epsilon}
 \right)
\tag{7c}
\]

oracle calls, with logarithmic QLS-precision factors suppressed.  Norm
estimation costs \(\widetilde O(\rho_t/\epsilon)\) additional coherent calls
and is dominated by (7c) for dense output.  A posteriori classical residual
testing can certify a more accurate instance, but cannot remove this
worst-case conversion factor.
Storing the resulting dense checkpoint in a standard binary-tree QRAM costs
\(O(n)\) classical writes and memory at that refresh; thereafter it provides
coherent coordinate and normalized-state access in polylogarithmic time,
assuming coherent reads.  Without such a data structure, preparation of
\(|\widehat z_s\rangle\) must be charged explicitly and may cost \(\Theta(n)\)
per use.

## 2. Residual-certified checkpoint algorithm

At refresh \(s\), store a classical vector \(\widehat z_s\) satisfying

\[
 \|\mathcal M_s\widehat z_s-f_s\|
 \le\epsilon\|f_s\|.
\]

At a later iteration \(t\), compute

\[
 h_t=\mathcal M_t\widehat z_s,
 \qquad
 a_t=\frac{\operatorname{Re}\langle h_t,f_t\rangle}
           {\|h_t\|^2},
\tag{8}
\]

where \(a_t=0\) if \(h_t=0\).  Accept \(a_t\widehat z_s\) when

\[
 \|a_th_t-f_t\|\le\eta_t\|f_t\|;
\tag{9}
\]

otherwise run QLS plus tomography and replace the checkpoint.

### Theorem 1 (feasible convergence and conditional refresh bound)

Suppose the underlying feasible OSS short-step theorem permits any coefficient
vector whose residual obeys

\[
 \|\mathcal M_t\widehat z_t-f_t\|
 \le\eta_t\|f_t\|
\tag{10}
\]

and suppose the implementation of (8)--(9) has enough safety margin that every
accepted or newly refreshed vector really obeys (10). In particular, the
checkpoint accuracy used as a step must satisfy \(\epsilon\le\eta_s\)
at each refresh. Then:

1. every reconstructed step is exactly primal--dual feasible by (3);
2. the neighborhood preservation, gap reduction, and
   \(O(\sqrt n\log(\mu_0/\epsilon_{\rm opt}))\) iteration bound of the
   underlying inexact feasible IPM apply unchanged;
3. if \(\eta_t\equiv\eta>0\), \(G>0\), all right-hand sides are nonzero,
   checkpoint tomography has \(0\le\epsilon\le\eta/(2G)\), and the
   directed cross-gain bound holds from the current checkpoint through every
   test, including failed tests, then the exact scalar minimization and
   threshold test (8)--(9) give the following number of checkpoint solves,
   including the initial solve:

\[
 R\le1+\frac{2GV_{\rm proj}}{\eta}.
\tag{11}
\]

#### Proof

The least-squares scalar (8) minimizes the residual over the cached ray.
Accepted and newly refreshed vectors satisfy the residual assumption of the published
outer theorem, while (3) supplies exact feasibility.  Thus its proof applies
iteration by iteration.  The refresh count is the projective lazy-refresh
theorem applied to the exact minimization and threshold policy in part 3.
An approximate implementation needs a rejection certificate that the true
minimum residual exceeds the threshold used in the variation argument.
Safe acceptance by itself permits rejecting every candidate: for a constant
identity system with one fixed nonzero right-hand side and exact checkpoints,
the projective variation is zero, but that policy performs a solve at every
iteration. Thus the original acceptance-only safety condition does not
establish (11).

This is an IPM convergence theorem, but (11) remains conditional on the
realized projective variation.  Feasibility and a standard neighborhood alone
do not bound that variation.

For \(T\) IPM iterations and \(R\) refreshes, the fully explicit hybrid ledger
is therefore

\[
 O(T\operatorname{nnz}\mathcal M)
 +\sum_{s\in\mathcal R}\widetilde O\!\left(
   \Gamma_{f,s}\mathcal K_s\frac{n\rho_s}{\epsilon}
 \right)
\tag{11a}
\]

operations/oracle calls, plus \(O(nR)\) QRAM writes and memory traffic.  Under
the hypotheses of (11), \(R\le1+2GV_{\rm proj}/\eta\); the first term still
runs for all \(T\) rounds.

### Classical residual-test cost

If \(\mathcal M_t\) is row sparse and the iterate is explicit, (8)--(9) cost

\[
 O(\operatorname{nnz}\mathcal M_t)
\tag{12}
\]

arithmetic per IPM iteration.  This gives a fully implementable hybrid
algorithm but retains the full sparse classical scan over all \(T\) rounds.

### Quantum residual-test cost

Prepare \(|\widehat z_s\rangle\), apply the block encoding of
\(\mathcal M_t/\alpha_{\mathcal M,t}\), and estimate its success probability
and its overlap with \(|f_t\rangle\).  Define

\[
 \Lambda_{t,s}
 =\frac{\alpha_{\mathcal M,t}\|\widehat z_s\|}
        {\|\mathcal M_t\widehat z_s\|}.
\tag{13}
\]

With coherent preparation and inverse access for both normalized states,
distinguishing residual at most \(\eta_t/2\) from residual at least
\(\eta_t\) costs

\[
 \widetilde O\!\left(
   \frac{\Lambda_{t,s}+\Gamma_{f,t}}{\eta_t}
 \right)
\tag{14}
\]

block-encoding/value-oracle calls.  Here the \(\Gamma_f\) term is omitted if a
unit-cost RHS-state oracle is supplied; otherwise it charges amplitude
amplification from the value oracle.  Formula (14) uses coherent amplitude
estimation, including inverses, and a promised gap; copy-only testing generally
loses the quadratic improvement in \(1/\eta_t\).  It also assumes that the
cached-vector state preparer has already been built at its \(O(n)\) refresh
cost.  Formula (14) is an upper-bound ledger, not a claim that the test is
always cheap.  Near a small singular direction,
\(\Lambda_{t,s}\) can diverge even when the candidate's relative residual is
acceptable.  Quantum state-verification lower bounds independently rule out a
parameter-free generic black-box test; (13) is the explicit amplification cost
of this block-encoding construction, not a matching lower bound for every
possible tester.

## 3. Proximal OSS selection

Given a checkpoint \(z_0\), define the proximal direction

\[
 z_\lambda
 =\arg\min_z
 \left\{\|\mathcal Mz-f\|^2+\lambda\|z-z_0\|^2\right\}.
\tag{15}
\]

It obeys

\[
 (\mathcal M^T\mathcal M+\lambda I)z_\lambda
 =\mathcal M^Tf+\lambda z_0.
\tag{16}
\]

Let \(z_* =\mathcal M^{-1}f\) and \(e=z_0-z_*\).  Then exactly

\[
 z_\lambda-z_*
 =\lambda(\mathcal M^T\mathcal M+\lambda I)^{-1}e,
\tag{17}
\]

and

\[
 \mathcal Mz_\lambda-f
 =\mathcal M\lambda(\mathcal M^T\mathcal M+\lambda I)^{-1}e.
\tag{18}
\]

### Exact block encoding and RHS ledger

Products and LCU give a block encoding of
\(G_\lambda=\mathcal M^T\mathcal M+\lambda I\) with normalization

\[
 \alpha_{G,\lambda}=\alpha_{\mathcal M}^2+\lambda.
\tag{19}
\]

Its effective inverse parameter is

\[
 \mathcal K_{G,\lambda}
 =\frac{\alpha_{\mathcal M}^2+\lambda}
        {\sigma_{\min}(\mathcal M)^2+\lambda}.
\tag{20}
\]

The RHS is prepared by an LCU of
\(\mathcal M^Tf\) and \(\lambda z_0\).  In an ideal norm-normalized input
model its amplification factor is at least accounted for by

\[
 \Gamma_{\rm prox}
 =\frac{\alpha_{\mathcal M}\|f\|+\lambda\|z_0\|}
        {\|\mathcal M^Tf+\lambda z_0\|},
\tag{21}
\]

with the actual normalizations of the \(|f\rangle\) and \(|z_0\rangle\)
preparers substituted when larger.  Cancellation can make (21) large.

One may instead solve the augmented least-squares system

\[
 \begin{bmatrix}\mathcal M\\ \sqrt\lambda I\end{bmatrix}z
 \approx
 \begin{bmatrix}f\\ \sqrt\lambda z_0\end{bmatrix},
\tag{22}
\]

whose singular condition is

\[
 \sqrt{\frac{\sigma_{\max}(\mathcal M)^2+\lambda}
              {\sigma_{\min}(\mathcal M)^2+\lambda}}.
\tag{23}
\]

This avoids presenting the squared condition as intrinsic, but preparation of
the augmented RHS and extraction of a classical coefficient vector remain
charged.

### Theorem 2 (worst-case regularization--residual tradeoff)

For every invertible \(\mathcal M\), checkpoint error \(e\), and
\(\lambda>0\),

\[
 \|\mathcal Mz_\lambda-f\|
 \le\frac{\sqrt\lambda}{2}\|e\|.
\tag{24}
\]

The constant \(1/2\) is sharp.  Therefore a sufficient uniform choice for
the relative residual contract \(\eta\) is

\[
 \lambda
 \le\frac{4\eta^2\|f\|^2}{\|e\|^2}.
\tag{25}
\]

If \(\|f\|=\Theta(\mu)\), \(\|e\|=\Theta(1)\),
\(\sigma_{\min}(\mathcal M)=\Theta(\mu)\), and both
\(\alpha_{\mathcal M}\) and \(\sigma_{\max}(\mathcal M)\) are
\(\Theta(1)\), (25) gives
\(\lambda=O(\eta^2\mu^2)\).  Equations (20)--(23) then retain respectively
the \(\Theta(\mu^{-2})\) normal-equation scale and the
\(\Theta(\mu^{-1})\) augmented-system scale.  Hence proximal regularization
does not improve the worst-case OSS condition while guaranteeing the standard
residual contract.

#### Proof

In a singular-vector coordinate of value \(\sigma\), the residual multiplier
in (18) is

\[
 \frac{\sigma\lambda}{\sigma^2+\lambda}.
\]

Its maximum over \(\sigma\ge0\) is \(\sqrt\lambda/2\), attained at
\(\sigma=\sqrt\lambda\).  Summing orthogonal coordinates proves (24), and
(25) follows.  Substitution gives the final asymptotics.

Larger \(\lambda\) can be effective when \(e\) is known to lie only in small
singular directions.  That is an additional spectral promise, not a
consequence of overlap with \(z_0\).

## 4. Overlap maximization is insufficient without residual control

Maximizing \(|\langle z,z_0\rangle|/(\|z\|\|z_0\|)\) favors continuity but
does not control \(\|\mathcal Mz-f\|\).  A small component of
\(z-z_*\) in a large-singular-value direction can have negligible effect on
state overlap and an arbitrarily large effect on residual.  Conversely, a
large change in a small-singular-value direction can have poor overlap but an
acceptable residual.  Therefore overlap can break ties only *inside* a
certified residual ball.  It cannot replace (9), (24), or an equivalent
spectral promise.

The proximal solution (15) is the continuous version of this principle: it
chooses a vector near \(z_0\) while penalizing residual.  Theorem 2 gives the
cost of making that penalty safe uniformly.

## 5. Test on the row-3-sparse cycling witness

For the LP

\[
 \min\sum_{j=4}^n x_j,
 \qquad x_1+x_2+x_3=1,
 \qquad x\ge0,
\tag{26}
\]

the standard inexact residual contract permits a trajectory whose optimal-face
component rotates through three projective lines.  Its face displacement is
\(d=\Theta(1/\sqrt n)\), its OSS RHS has norm \(\Theta(\mu_t)\), and the
cycling complementarity residual is \(O(d\mu_t)\).

The idealized policy with an exact solve on every failed test cannot follow
this particular three-phase trajectory:

1. if the cached rescaled direction satisfies (9), it is reused, so the
   output coefficient ray cannot switch among the three displayed rays;
2. if it fails, the unique exact centering direction at (29) is (35), which
   contracts the current face displacement when applied at that point rather
   than rotating it.

This is only a rejection of the displayed cycle, not a proof that the reuse
trajectory has finite projective variation.  Repeatedly applying a stale
face-tangent coefficient can drift across the optimal face until its residual
test fails.  Moreover, a practical QLS/tomography refresh is only approximate;
residual accuracy alone still permits a large coefficient error in the
\(\Theta(\mu_t)\) singular subspace.  Suppression of the exact cycle therefore
requires the stated exact-solve idealization, or a coefficient/state-accuracy
guarantee strong enough to choose the exact centering ray.  The outer
convergence theorem needs neither condition, but the conditional refresh bound
still needs finite \(V_{\rm proj}\).

It does expose the implementation cost.  The face-tangent singular values of
\(\mathcal M_t\) are \(\Theta(\mu_t)\).  A proximal parameter
\(\lambda\gg\mu_t^2\) retains the old tangent coefficient and prevents an
arbitrary switch to the next displayed ray at that solve.  It does not itself
contract the primal face displacement: the retained coefficient is a step and
can instead cause drift.  Nor does it have a uniform residual guarantee
outside this witness.  The safe choice from (25) is
\(O(\eta^2\mu_t^2)\) and gives no asymptotic conditioning gain.

For a normalized cached coefficient dominated by the face tangent,

\[
 \Lambda_{t,s}
 =\frac{\alpha_{\mathcal M,t}\|z_s\|}
        {\|\mathcal M_tz_s\|}
 =\Omega(1/\mu_t)
\tag{27}
\]

under the ordinary OSS encoding.  Thus a generic amplitude-based quantum
residual test at every short-step iteration can be precision-dependent even
though a sparse classical residual test is straightforward.

## 6. Final status

The residual-certified algorithm and Theorem 1 give an implementable feasible
QIPM with a genuine outer convergence theorem.  On a realized finite-
projective-variation tail it reduces QLS/tomography refreshes, but its residual
testing work must still be charged at every iteration.

Theorem 2 is a no-go result for unconditional proximal acceleration of OSS
checkpoint solves.  Proximal or overlap-maximizing selection is safe and useful
only after residual certification, or under a structured promise placing the
checkpoint error in small-singular-value face directions.  On the row-3-sparse
witness, deterministic exact-refresh reuse rejects the exhibited three-ray
cycle, but neither proximality nor residual certification proves finite
variation.  The witness also shows why generic quantum-only certification need
not be cheap.

Relevant prior work includes Kim, Chia, and Kyrillidis, *A catalyst framework
for the quantum linear system problem via the proximal point algorithm* (AAAI
2026), classical Krylov recycling, Somma--Subasi quantum state verification,
and the feasible OSS convergence theorem of Mohammadisiahroudi, Fakhimi, Wu,
and Terlaky.  None of these by itself supplies the sequence-level certified
reuse theorem or removes the residual-test ledger above.
