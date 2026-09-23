# Verified continuation results: sparse QIPMs beyond the condition number

Date: 2026-09-02

This continuation produced three apparently new theorem packages, all different from
the earlier local results.

## 1. Stable active-subspace equilibration

See [stable-active-subspace-qipm.md](stable-active-subspace-qipm.md).

For strict-complementarity normal matrices
\[
 H_\mu=\mu^{-1}C_\mu+\mu D_\mu
\]
with active-range projector \(Q\), the directly assembled left-equilibrated operator
\[
 M_\mu
 =C_\mu+D_\mu-(1-\mu^2)QD_\mu
\]
is uniformly conditioned and satisfies
\[
 M_\mu^{-1}f=\mu^{-1}H_\mu^{-1}f
\quad(f\in\operatorname{range}Q).
\]
It therefore prepares exactly the original normalized Newton state, but removes the
\(\mu^{-2}\) DLS filtering penalty. An approximate \(Q\) needs only ordinary
\(O(\epsilon_{\rm QLS})\) accuracy. A separately encoded product \(P_\mu H_\mu\) does
not help because block-normalization overhead restores the penalty.

A constant-sparse bipartite-expander LP gives a genuine central-path witness:
unpreconditioned DLS filtering has \(\rho=\Theta(\mu^{-2})\), whereas direct split
assembly has \(O(1)\) conditioning and \(O(d)\) normalization.

## 2. Effective-spectral-dimension phase transition

See [effective-spectral-dimension-qipm.md](effective-spectral-dimension-qipm.md).

If the RHS spectral measure obeys
\[
 \nu_b([t,2t))=\Theta(t^{D/2}),
\]
then DLS effective truncation changes phase at \(D=4\), while filtering changes phase
at \(D=8\):
\[
 \kappa_{\rm eff}=
 \begin{cases}
 \Theta(\kappa),&D<4,\\
 \kappa^{1-\Theta(\epsilon^2)},&D=4,\\
 \Theta(\min\{\kappa,\epsilon^{-4/(D-4)}\}),&D>4,
 \end{cases}
\]
\[
 \rho=
 \begin{cases}
 \Theta(\kappa),&D<4,\\
 \Theta(\kappa/\sqrt{\log\kappa}),&D=4,\\
 \Theta(\kappa^{(8-D)/4}),&4<D<8,\\
 \Theta(\sqrt{\log\kappa}),&D=8,\\
 \Theta(1),&D>8.
 \end{cases}
\]
A positive full-step feasible QIPM corrector on a massive torus realizes
\(D=d+2\) for a conserved edge residual and quadratically improves its central
neighborhood. This gives a concrete solver-selection rule based on residual regularity,
not just sparsity and \(\kappa\).

## 3. Active/inactive coupling theorem

See [beyond-kappa-coupling-qipm.md](beyond-kappa-coupling-qipm.md).

For an exact feasible short-step RHS at a strictly complementary, primal-degenerate
limit, exact block elimination gives
\[
 \rho_\mu
 =\Theta\!\left(1+\frac{\lVert g_\mu\rVert}{\mu^2}\right),
\qquad
 g_\mu=E_\mu^{-1}F_\mu
 (C_\mu+\mu^2R_\mu)^{-1}b.
\]
Hence generic limiting coupling
\[
 E^{-1}FC^{-1}b\ne0
\]
forces the full \(\Theta(\mu^{-2})\) DLS filtering cost even though the usual
first-inverse measure is \(\Theta(1)\). The same coupling gives a fixed-accuracy DLS
truncation transition through constant slow-eigenspace solution mass. Coupled and
decoupled row-two LPs prove the result is sharp.

The note also records an exact-center realization of the known marked-diagonal QLS
search lower bound. Its QLS core is not new; the useful new part is its QIPM
normal-equation realization and the separation between first- and second-inverse
parameters.

## Verification and novelty boundary

The algebra, sparse witnesses, signs, neighborhood bounds, block-normalization
accounting, and output contracts were independently audited. Targeted searches through
2026-09-02 found no source that:

- applies the 2026 Dalzell--Li--Su solvers to IPM/QIPM Newton systems;
- derives the active/inactive second-inverse coupling law;
- gives the \(D=4\) versus \(D=8\) solver phase transition and QIPM realization; or
- gives the stable split operator with exact state preservation and
  \(\mu\)-independent projector accuracy.

The notes therefore use “apparently new,” not an absolute priority claim. Classical
active-set preconditioning, RHS-sensitive conditioning, Green-function moment
thresholds, and generic marked-diagonal QLS lower bounds are explicitly credited as
prior art.

None of the results alone proves an end-to-end LP speedup. Active-set discovery,
component block encodings, RHS preparation, norm estimation, tomography/classical
updates, and strong classical solvers such as Krylov methods or multigrid remain
chargeable. The positive result is strongest for state or few-observable output.
