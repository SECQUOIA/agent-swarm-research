# Newton RHS spectral alignment: on-path QIPM steps evade the two-cluster obstruction

Date: 2026-09-02
Status: proposition proved; independently referee-audited (verdict:
sound with one repair — the eigenspace-rotation bookkeeping needed the
Davis--Kahan patch, applied below; all algebra, numbers, and the
corollary mechanism verified). Empirics verified on two families; completes the two-cluster/Theorem Q story
(2026-09-02-two-cluster-central-hessian-benign-kappa.md) on the
positive side and connects it to the repository's face-leakage and
effective-spectral-dimension programs.

## Message

Theorem Q says two-cluster Newton systems cost
\(\widetilde\Theta(\kappa)\) quantumly (plain block-encoding) for
worst-case right-hand sides. This note shows the *path-following steps
themselves are not worst case*: at exact central points, the reduced
Newton RHS of both the centering and the affine-scaling step is one
universal vector whose bottom-cluster (weak-face) component is
\(O(\mu^2)\)-small — because the log-barrier path converges to the
analytic center of the optimal face, whose first-order condition
annihilates the leading weak-mode pairing. Consequently a top-window
solve satisfies any constant-relative-residual inexact-Newton contract,
at plain-block-encoding QSVT degree
\(O(\rho_2\log(\rho_2/\eta))\) — independent of \(\kappa\) — for
\(\mu=O(\sqrt\eta)\); in practice the weak-mode fraction is
\(\approx7\times10^{-4}\mu^2\) on afiro, so the \(\mu\)-range constraint
is vacuous at any practical depth. The \(\kappa\)-obstruction binds
off-path right-hand sides and output contracts, not the on-path
solves.

## Proposition R (universal RHS and its weak-mode fraction)

Setting of the two-cluster note (degenerate LP, log-barrier path,
reduced coordinates \(Z\) on \(\ker A\), clusters as in its Proposition
1). At the exact central point \(x=x(\mu)\):

1. **One RHS vector.** Centrality gives \(Z^\top(c-\mu X^{-1}\mathbf1)=0\),
   so the reduced RHS of the centering step to target
   \(\mu_2=\gamma\mu\) is
   \(r_c=-Z^\top(c-\mu_2X^{-1}\mathbf1)=-(1-\gamma)\mu\,Z^\top X^{-1}\mathbf1\)
   and the affine-scaling RHS is
   \(r_a=-Z^\top c=-\mu\,Z^\top X^{-1}\mathbf1\): both are scalar
   multiples of \(v_\mu=Z^\top X^{-1}\mathbf1\).
2. **Weak-mode fraction \(O(\mu^2)\).** Two ingredients (referee-patched
   bookkeeping):
   (i) *Eigenspace rotation is \(O(\mu^2)\), not \(O(\mu)\).* In the
   two-cluster note's split \(H_\mu=A_\mu+B_\mu\), the bottom eigenspace
   of \(A_\mu\) is exactly the face-tangent space \(\ker(P_NZ)\), the
   spectral gap is \(\Theta(1/\mu^2)\), and \(\|B_\mu\|\le\beta^{-2}=O(1)\);
   Davis--Kahan gives a bottom eigenspace of \(H_\mu\) within angle
   \(O(\mu^2)\) of the face-tangent space. Hence the \(N\)-coordinate
   contribution to a bottom-eigenvector pairing with
   \(X^{-1}\mathbf1\) is \(O(\mu^2)\cdot\Theta(1/\mu)=O(\mu)\).
   (ii) *Face-tangent pairing is \(O(\mu)\).* For face-tangent unit
   \(u\) (\(u_N=0\)), \(\langle u,X^{-1}\mathbf1\rangle=
   \sum_{j\in B}u_j/x_j(\mu)\); the path limit \(x^a\) is the analytic
   center of the primal optimal face (McLinden), maximizing
   \(\sum_{j\in B}\log x_j\) over the face, whose first-order condition
   is exactly \(\sum_{j\in B}u_j/x^a_j=0\); with the standard tail
   expansion \(x_B(\mu)=x^a_B+O(\mu)\) (strict complementarity), the
   pairing is \(O(\mu)\).
   Total bottom amplitude \(O(\mu)\), top amplitude \(\Theta(1/\mu)\)
   (inactive \(1/x_i=\Theta(1/\mu)\); nondegeneracy \(Z^\top c\ne0\),
   else the RHS vanishes identically): bottom \(\ell_2\)-fraction
   \(O(\mu^2)\). The empirical constant on afiro is
   \(6.4\text{--}6.7\times10^{-4}\), stable over four decades — a clean
   \(\mu^2\) law incompatible with a genuine \(O(\mu)\) term.
3. **Dropped-mode residual = bottom RHS fraction, exactly.** If
   \(d=H_\mu^{-1}r\) and the bottom-cluster component of \(d\) is
   dropped, the residual is \(H_\mu(d-d_{\rm bot})-r=-P_{\rm bot}r\), so
   the relative residual equals the bottom \(\ell_2\)-fraction of
   \(r\): \(O(\mu^2)\).

## Corollary (per-iteration quantum cost of on-path steps)

An inexact-Newton contract with relative residual \(\eta\) (constant
\(\eta\) suffices in standard inexact-feasible IPM analyses) is met, for
all \(\mu=O(\sqrt\eta)\), by inverting only on the top cluster: the
polynomial \(\approx1/x\) on \([1/\rho_2,1]\)-rescaled, bounded on
\([-1,1]\), has degree \(O(\rho_2\log(\rho_2/\eta))\) with \(\rho_2\) the
\(\mu\)-free top intra-cluster ratio — **implementable with a plain
block-encoding, \(\kappa\)-free**. Theorem Q is not contradicted: the
obstruction is real for worst-case RHS, and it also prices any *output*
contract that needs the weak-mode component to relative accuracy.

## Empirics

`notes/scripts/newton_rhs_cluster_alignment.py`. Degenerate \(n=40\) family and
Netlib afiro, \(\mu\) down to \(10^{-6}/10^{-5}\): RHS top-cluster mass
\(=1.0000\) for both step types at all depths; solution top mass
\(\ge0.9929\); dropped-bottom relative residual \(=6.7\times10^{-6},
6.4\times10^{-10},6.7\times10^{-14}\) at \(\mu=10^{-1},10^{-3},10^{-5}\)
on afiro — the \(O(\mu^2)\) law with instance constant
\(\approx7\times10^{-4}\), and machine-zero on the toy family.

## Scope, caveats, and connections

- Exact centrality is assumed; off-path iterates acquire weak-mode RHS
  components, and whether their accumulated neglect is safe is exactly
  the face-leakage/normalized-forcing summability question already
  settled conditionally in
  2026-09-02-projective-lazy-quantum-newton-refresh.md — the two-cluster
  spectral picture is the natural coordinate system for those
  conditions.
- The \(O(\mu^2)\) rate is a log-barrier statement (it uses the
  analytic-center limit and the \(X^{-2}\) cluster structure); for a
  general barrier an analogous mechanism via its own face-center
  gradient condition is *conjectured* (an \(O(\mu)\)-level fraction),
  but neither the cluster identification nor the path-limit facts are
  established there.
- Predictor--corrector variants, infeasible starts, and primal--dual
  (rather than reduced primal) systems are not analyzed here; the
  mechanism (path limit annihilates the weak-mode pairing of the
  path's own gradient) is expected to transfer but is unproved there.
- Connection to beyond-\(\kappa\) solvers: the RHS-visible spectral
  measure concentrated on the top cluster means instance-adaptive
  \(\kappa_{\rm eff}\) quantities (Dalzell--Li--Su-type; the
  repository's effective-spectral-dimension phase law) are \(O(1)\) for
  on-path steps — the two programs agree.

## Verification record

- Proposition R referee-audited: item 1 verified (and explains the
  empirically identical centering/affine columns); item 2's original
  draft proved only \(O(\mu)\) — the audit supplied the Davis--Kahan
  patch (gap \(\Theta(1/\mu^2)\), perturbation \(O(1)\) ⇒
  \(O(\mu^2)\) eigenspace rotation), applied above, and noted the
  toy family's machine-zero is an exact symmetry (uniform analytic
  center), so afiro is the substantive test; item 3 verified exact;
  corollary mechanism verified with the \(H\)-norm direction checked
  (\(O(\mu)\), better than the \(\ell_2\) fraction).
- Empirics: two families, two step types, three depths; the \(\mu^2\)
  scaling and the equality of the two step columns are both visible.
- All quoted numbers independently reproduced by the audit.

## End-to-end validation (added after the audit)

`notes/scripts/window_solve_ipm_run.py` runs a complete damped-Newton
path-following loop (shrink \(0.85\), up to four corrections per
\(\mu\), fraction-to-boundary steps) in two modes: exact reduced solves
versus **window-only solves that drop the bottom cluster whenever a
genuine spectral gap (\(>2\) decades) exists and fall back to full
solves otherwise**. Results, from \(\mu_0\) down nine to ten decades:

- degenerate toy family: identical trajectories, gap
  \(1.758\times10^{-8}\), 205 corrections in both modes;
- afiro: identical trajectories, relative gap \(7.4\times10^{-10}\),
  393 corrections in both modes.

An honest negative finding en route: a naive window rule (geometric-mean
threshold, no gap detection) *stalls* on afiro (final relative gap
\(0.98\)), because early in the run the spectrum is a continuum and the
threshold splits it arbitrarily — the adaptive rule "full solve until
the cluster gap opens, then drop the weak modes" is the correct
algorithmic translation of Proposition R, and cluster detection is
cheap. This validates, at whole-trajectory level and off the exact
path, that the \(\kappa\)-carrying subspace is never needed for the
path-following directions once the two-cluster structure exists.
