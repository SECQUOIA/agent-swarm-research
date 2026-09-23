# Pathwise residual-certified refresh

Source: the theorem “Pathwise residual-certified refresh” in
[`paper/sections/13-positive-modules.tex`](../paper/sections/13-positive-modules.tex),
label `thm:positive-lazy-refresh`. The Lean sources are in
[`QipmFormal/Refresh/`](QipmFormal/Refresh/).

The development proves the bound for the actual scalar least-squares test
and sequential checkpoint procedure. It derives the residual estimate from
the original systems, rather than assuming that estimate or the disjointness
of failed intervals.

## Verified statement

For a finite realized sequence `H_t z_t = f_t`, `t = 0, ..., T`, set

\[
q_t=\|z_t\|,\qquad \psi_t=z_t/q_t,\qquad
M_t=(q_t/\|f_t\|)H_t,\qquad
\delta_j=\|M_{j+1}(\psi_{j+1}-\psi_j)\|.
\]

Each `H_t` is invertible and every `f_t` in the finite horizon is nonzero.
At each checkpoint `s`, the stored vector has relative residual at most
`epsilon`. At each test, minimize the current relative residual over scalar
multiples of the stored vector. Reuse at residual at most `eta`; refresh
only when that minimum exceeds `eta`.

If `G > 0`, `eta > 0`, `epsilon ≤ eta/(2G)`, and for each actual test at
time `t` with current checkpoint `s`,

\[
\|M_tM_j^{-1}\|\le G\quad(s\le j\le t),
\]

then `paper_refresh_bound` proves

\[
R\le 1+\frac{2G}{\eta}\sum_{j=0}^{T-1}\delta_j.
\]

`R` counts the initial solve at time zero as well as every later refresh.
The gain assumption includes the endpoint of a failed test, before the
checkpoint is replaced. Accuracy is assumed only at realized checkpoints,
including the last one. The paper explicitly states `epsilon ≥ 0`; Lean
does not need it as an extra assumption, because initial checkpoint accuracy
already implies it.

## Representation and manuscript correspondence

- `E` is a real inner-product space. For the manuscript's Euclidean
  coordinates use `EuclideanSpace ℝ (Fin n)`, with its Euclidean norm;
  an unadorned function space's default sup norm is not substituted for it.
- `H : ℕ → E ≃L[ℝ] E` represents bounded invertible linear operators with
  bounded inverses. In finite dimension these are the nonsingular systems.
  The theorem also applies in the more general inner-product-space setting.
- `solution H f t` is the actual inverse applied to `f t`, and
  `solution_equation` proves its defining system equation. `solutionNorm`,
  `ray`, and `normalizedOperator` are exactly the quantities above.
- `normalizedInverse` is the explicitly scaled inverse. Both compositions
  with `normalizedOperator` are proved to be identities at nonzero RHS.
- `scalarLeastSquares v f = inner v f / ‖v‖²` genuinely minimizes the
  residual. When `v = 0`, Lean's division-by-zero convention returns zero,
  and the proof shows that every scalar has the same residual.
- `reuseCost H f stored s t` is the actual relative residual after applying
  this scalar to `stored s`. It is not an externally supplied residual bound.
- `checkpoint` and `refreshCount` implement the sequential policy. The
  abstract counting lemmas allow an arbitrary cost function; the headline
  theorem instantiates it with `reuseCost`.
- Functions are indexed by natural numbers, but `paper_refresh_bound`
  requires nonzero right-hand sides only through `T`. The finite-prefix
  residual lemma proves that values beyond the horizon are irrelevant.
- A realized adaptive path supplies these same systems and stored vectors.
  No independence, probabilistic, or advance-knowledge assumption is used.
  The theorem does not formalize a probabilistic algorithm generating them.

## Claim map

All names are in `QipmFormal.Refresh`, except the final row, which adds
the namespace `Counterexample`.

| Claim | File and principal declarations |
|---|---|
| Actual solution, positive normalization, unit ray, normalized RHS | [Core.lean](QipmFormal/Refresh/Core.lean): `solution_equation`, `solutionNorm_pos`, `norm_ray`, `normalizedOperator_ray` |
| Both inverse identities and exact relative-residual conversion | `Core.lean`: `normalizedInverse_apply_operator`, `normalizedOperator_apply_inverse`, `normalized_residual` |
| Directed propagation, telescoping, candidate scalar bound | `Core.lean`: `propagate_norm`, `ray_difference_bound`, `candidate_residual_bound`, `candidate_residual_bound_on` |
| Explicit scalar minimization, including a zero stored vector | [LeastSquares.lean](QipmFormal/Refresh/LeastSquares.lean): `scalarLeastSquares_sq_identity`, `scalarLeastSquares_minimizes` |
| Checkpoint policy, failed intervals, strict variation charge | [Counting.lean](QipmFormal/Refresh/Counting.lean): `checkpoint`, `refreshCount`, `failed_intervals_disjoint`, `failed_test_charge_strict` |
| Count with unspent suffix and final bound | `Counting.lean`: `refresh_budget`, `refresh_count_bound` |
| Zero transitions, threshold equality, no failures, zero variation | `Counting.lean`: `refreshCount_zero`, `cache_unchanged_at_threshold`, `refresh_count_eq_one_of_no_failures`, `refresh_count_eq_one_of_zero_variation` |
| Actual minimum residual and complete manuscript theorem | [Paper.lean](QipmFormal/Refresh/Paper.lean): `reuseCost_le_candidate`, `reuseCost_bound`, `paper_refresh_bound` |
| Safe acceptance alone permits too many refreshes | [Counterexample.lean](QipmFormal/Refresh/Counterexample.lean): `constant_stepVariation`, `constant_reuseCost`, `constant_checkpoint_residual`, `constant_cross_gain`, `rejecting_proxy_count`, `safe_acceptance_only_counterexample` |

## Corrections and scope

The current manuscript now explicitly states the nonzero RHS, positive
thresholds, checkpoint accuracy, directed gain quantifiers, exact test,
and initial-solve counting convention. Its proof identifies the use of
`M_t M_(j+1)⁻¹` when transporting step `j`. Related applications retain
the same gain and accuracy assumptions.

The supporting
[feasible-OSS reuse note](../research-archive/2026-09-research-cycle/supporting-results/2026-09-02-proximal-residual-certified-oss-reuse.md)
previously used only an acceptance-safety premise for its refresh count.
That is insufficient. For the constant identity system with fixed nonzero
RHS and exact checkpoints, the true minimum residual and projective
variation are zero, and the cross-gain is one. A proxy test that always
reports two at threshold one rejects every time while satisfying safe
acceptance. Its count is `T + 1`, contradicting the proposed bound for
every positive `T`. This counterexample is formalized too. The note now
requires exact tests for the displayed bound; a noisy extension must supply
a suitable rejection guarantee and derive its resulting constants.

The original superseded projective note carries a status notice pointing
to this correction. Its historical claims have not otherwise been rewritten.
The other three current manuscripts do not invoke the refresh theorem and
needed no changes.

The following are outside this formalization:

- Establishing bounded gain or variation from strict-complementarity tail
  assumptions, or proving the exact-central feasible-OSS corollary.
- IPM feasibility, neighborhood preservation, convergence, cycling and
  proximal no-go results, or checkpoint-span query and gate counts.
- Quantum state preparation, tomography, and end-to-end runtime claims.
- Floating-point scalar minimization, residual evaluation, or a noisy test.

The result bounds checkpoint solves conditional on the displayed quantities.
It does not remove the per-iteration cost of the residual test.

## Reproduction

From `formal/`, in the configured repository environment:

```sh
conda run -n qipm --no-capture-output bash scripts/verify.sh
```

This builds all project modules and checks their axiom dependencies,
including the new refresh modules, against `propext`, `Classical.choice`,
and `Quot.sound`. Project axioms, `sorryAx`, and `Lean.ofReduceBool` are
rejected. The optional `--replay` rechecks the entire import closure in
a fresh Lean kernel environment; it is separate from the ordinary audit.

Rebuild the affected manuscript from `paper/` with
`conda run -n qipm --no-capture-output make`.

## Validation completed on 2026-09-20

- The integrated build and axiom audit passed for **1205 project
  declarations**, covering the refresh development and all existing
  scalar-certificate, QCPM, and mixture modules. All audited declarations
  depend only on the three allowed standard axioms.
- The five refresh modules compiled without warnings. The mathematical
  edge cases include no transitions, equality at the acceptance threshold,
  no failures, zero variation, zero stored vectors, and a successful suffix.
- Two independent source reviews checked the mathematical proof, the
  formal theorem statements, the finite-horizon interface, the rejecting-test
  counterexample, and the documentation. All identified issues were resolved.
- The affected manuscript rebuilt to **196 pages**, with no LaTeX warnings,
  unresolved references or citations, or overfull/underfull boxes. Pages
  **145–146**, containing Theorem 13.1, its proof and the verification scope,
  were rendered and visually checked.
- `git diff --check` passed. The optional fresh-environment replay of the
  entire Lean/Mathlib import closure was **not run**.
