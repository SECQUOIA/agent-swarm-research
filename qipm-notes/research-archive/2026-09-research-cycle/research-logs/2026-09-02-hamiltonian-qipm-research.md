# Hamiltonian sparse-QIPM research log

**Date:** 2026-09-02  
**Final synthesis:** `notes/research-archive/2026-09-research-cycle/supporting-results/hamiltonian-qipm-sparse-obstructions.md`

## Scope exclusion

This research pass deliberately excluded the main results already recorded in
`notes/research-archive/2026-09-research-cycle/supporting-results/sparse-qipm-structural-results.md`: the complementarity support barrier, the
condition-one box-LP value family, the sparse-QLS-to-OSS embedding, the treewidth-two
KKT precision lower bound, and projective lazy diagonal maintenance.

## Search branches

Ten parallel branches examined end-to-end lower bounds, positive sparse algorithms,
trajectory costs, condition/sparsity interactions, output models, spectral sketches,
the current literature frontier, adversary reductions, classical baselines, and
unconventional constructions.

The candidates that survived internal proof checking were:

1. **QCPM simulation correction.** The global potential supremum is bounded below at
   the known initial center; the paper's state-concentration substitution is false.
   Its time-rescaling parameter is also time-dependent. The corrected integrated
   norm is
   \[
      (a\eta)^{-1}\int_0^1
      \sup_\Omega f_{\mu(t)}\,\mu(t)^{-3}dt,
   \]
   and the paper's schedule makes this
   \(\Omega(d/(a\eta\epsilon^3\log(1/\epsilon)))\).
2. **Ordered-simplex inverse metric.** A log barrier with two-sparse path constraints
   has a tridiagonal analytic-center Hessian but a fully dense inverse with
   \(\Theta(n^2)\) entries of order \(1/n\). This prevents sparse LP input from
   automatically yielding an entrywise sparse standard-coordinate Laplace--Beltrami
   coefficient tensor. The Green kernel is semiseparable and has an \(O(n)\) implicit
   apply, so this is a representation warning, not a simulation lower bound. The
   general oracle-construction concern is also recognized by Abe--Nagai (2026).
3. **Parity-complete original-form feasible start.** Hidden signs in a path constraint
   matrix force prefix parities into every feasible point. Value estimation,
   \(\ell_1\)-accurate original-form feasibility, and construction of the exact
   central-start value oracle are all \(\Omega(n)\)-query tasks, while every reduced
   primal-barrier Hessian is scalar. Homogeneous self-dual and infeasible-start methods
   are explicitly outside this lower bound.

All three are written with proofs and scope limits in the final synthesis.

## Verification record

- The QCPM equations were checked against the frozen local copy of
  `literature/papers/augustino2024-quantum-central-path-algorithm-linear/original.pdf`
  and the current public v2. Two independent referee passes confirmed the corrected
  clock, the exact norm identity, constants 128 and 64, and the global upper bound.
- Numerical quadrature for \(\epsilon=10^{-2},10^{-3},10^{-4}\) gave stabilized
  values of
  \(\epsilon^3\log(1/\epsilon)\int(1-\mu(t))^2\mu(t)^{-3}dt\), consistent with the
  proved lower-order scale. This was a sanity check, not part of the proof.
- The ordered-simplex inverse formula was checked against direct inversion for
  \(n=2,3,8,25\), and the arbitrary-slack Green formula was checked on random
  interiors through \(n=30\). A hostile review identified its semiseparable
  \(O(n)\)-apply structure, which is now explicit in the final note.
- Every sign instance of the original-form feasible-start LP was solved directly for
  \(N\le7\). The predicted value, full null basis, exact \(\mu=3/4\) center, and
  condition-one reduced Hessian all matched. An optimization referee separately
  checked the algebra and identified the homogeneous-self-dual escape route now stated
  in the theorem's scope.
- A final novelty referee searched current sources through 2026-09-02. It found no
  public source with the exact QCPM supremum/clock correction or the central-start
  oracle separation. It did find Abe--Nagai (2026), which partially anticipates the
  general inverse-metric access concern and is now cited.

## Other useful candidates retained for future work

These results were not promoted to the main note because the three items above form a
more coherent and impactful package. They remain potentially publishable.

- **Augmented spectral Newton sketch.** Spectrally sample the augmented regression
  matrix \([D^{1/2}A^T,v]\), not the Hessian and right-hand side separately. If the
  augmented Gram matrix has a \((1\pm\varepsilon)\) embedding, the sampled least-squares
  solution obeys
  \[
    \lVert B(\widetilde z-z^*)\rVert_2
    \le\frac{\varepsilon}{1-\varepsilon}
       \operatorname{dist}(v,\operatorname{col}B).
  \]
  The row-query cost is \(\widetilde O(\sqrt{nm}/\varepsilon)\), independent of a
  linear-system condition number. An end-to-end QIPM still needs a rigorous
  infeasible-step analysis and an implicit primal-update representation.
- **RHS-loading lower bound.** A diagonal, condition-one QP predictor can have its
  normalized Newton direction concentrated on a hidden \(k\)-subset. Preparing that
  state from coordinate-value access needs \(\Omega(\sqrt{N/k})\) queries, and explicit
  recovery under a block promise needs \(\Omega(\sqrt{Nk})\). The bound disappears if
  a support-list or state-preparation oracle is supplied; that access-model separation
  is the point.
- **Pattern-only value lower bound.** A fixed-data sparse LP or ridge QP can encode the
  2-to-1 versus almost-2-to-1 promise solely in the nonzero locations of a two-sparse
  constraint matrix. It has a constant scalar optimum gap and block-diagonal,
  uniformly conditioned central normal equations, yet needs \(\Omega(N)\) forward-row
  queries. A free transpose/preimage oracle is strictly stronger and can weaken the
  problem.
- **Connected output hierarchy.** A chain of diamond flow gadgets is planar,
  series-parallel, and has a condition-one sparse cycle Newton system. Exact central
  and optimal-flow states have one-query preparation, while an explicit
  constant-relative-error feasible flow, its support, or an explicit sampling table
  needs \(\Omega(N)\) queries on a code promise. The bare LP lower-bound exponent is
  known; the new part is the output-contract separation.
- **Strict-complementarity spectral split.** Along a nondegenerate central path,
  normal equations split into \(\Theta(\mu^{-1})\) active and \(\Theta(\mu)\) inactive
  eigenvalues. A feasible centering right-hand side can nevertheless have constant
  inverse-action norm, while an \(O(\eta\mu)\) inactive-subspace residual restores an
  \(O(\eta/\mu)\) penalty. Hostile review found that this does **not** imply a faster
  Dalzell--Li--Su filtering solve: for normalized \(\bar H=H/\lVert H\rVert\), that
  solver depends on
  \[
    \frac{\lVert H\rVert\,\lVert H^{-2}f\rVert}
         {\lVert H^{-1}f\rVert},
  \]
  not merely \(\lVert H\rVert\lVert H^{-1}f\rVert/\lVert f\rVert\). In the sparse
  witness the former remains \(\Theta(\mu^{-2})\). The safe contribution is a
  right-hand-side-sensitive structural identity, not an improved QLS complexity.
- **Trajectory transcription.** Materializing classical neighborhood iterates at
  \(T\) prescribed scales can encode \(T\) independent sparse-search instances and
  force \(\Omega(T\sqrt{Nk})\) cumulative queries. This is a classical-transcript
  theorem, not a lower bound for coherent time-labelled solution states; a block
  diagonal QLSA can prepare all such states in superposition.

## Rejected shortcuts and caveats

- Ground-state concentration does not control an operator supremum.
- A time-dependent kinetic coefficient cannot be removed by a constant linear clock.
- A sparse Hessian does not imply a sparse inverse metric.
- Exact inverse density alone is not a universal simulation lower bound; structured
  transforms or approximate inverses may help.
- A static sparse oracle contains only linearly many coefficients, so an iteration
  lower bound cannot exceed the cost of reading and caching the input without an
  online, memory, adaptive, or output restriction.
- Multiple hard Newton systems do not automatically add: controlled block-diagonal
  access can solve a time-labelled superposition at the maximum single-system cost.
- Sparse coefficient vectors are easy under a nonzero-location oracle and can be hard
  under coordinate-value access. Every lower bound must name which oracle is used.
- A quantum state, one coordinate sample, a random-access oracle, a scalar objective,
  and a materialized classical vector are inequivalent output contracts.

## Novelty standard

Searches covered local papers and open sources through 2026-09-02. Later papers already
criticize the broad real-space simulation and unbounded-adiabatic foundations of
Hamiltonian optimization. The final note therefore claims novelty only for the exact
global-supremum counterexample, corrected clock and norm formulas, ordered-simplex
inverse-metric specialization, and original-form parity-complete central-start
separation. No claim of priority is unconditional.
