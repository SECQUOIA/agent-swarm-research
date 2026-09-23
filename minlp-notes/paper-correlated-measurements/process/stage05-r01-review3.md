# Stage 5 independent review 3

Decision: **No major issues. One valid minor checker issue.** The fresh nested-anchor and full-block results are mathematically supported by the saved rational witnesses. I found no false numerical inequality, mismatched feasible family, unsupported strictness claim, or material omission in their reported cost comparisons.

## Scope and evidence

I read the Stage 5 author report, the computational section and model appendix, `fresh_experiments.py`, `validate_models.py`, the relevant complete-block locality theorem, and the separator certificate and nested-hierarchy theorem. I also inspected the standalone validation entry point, supplement README, the underlying augmented kinetic balance/sensitivity generator, and the complete saved fresh study.

Independent checks are in `verification/stage05-review3/check_fresh.py`, `check_local_hulls.py`, and `checks.json`. They import no producer or certificate helper. The exact comparisons use SymPy rational matrices and LDL signs; logarithms are separately checked with 90-digit mpmath as a diagnostic rather than described as an additional interval proof. The production rational logarithm proof remains the source of the certified endpoints. Frozen manuscript and supplement files were not changed.

Checks passed:

- Reconstructed all 56 size-three schedules and the stipulated n=8, p=2 sensitivity/covariance/prior model independently. The unique true determinant optimum is exactly the reported schedule `{1,4,6}`.
- Reconstructed all 224 augmented information atoms and verified their complete parameter Schur matrices against the direct selected-covariance information, not merely determinants.
- Verified every saved mixture weight is nonnegative, the weights sum exactly to one, the stored information matrix equals the true mixture Schur complement, each saved nuisance witness solves the exact stationarity equation, the weight witness is its inverse, and all 224 support prices and maximizing atoms agree.
- Verified disjoint strict hierarchy intervals and the remaining no-anchor integrality gap. All displayed nested table endpoints are outward.
- Independently computed the dense extension using the inverse of the effective covariance on positive support; verified exact cardinality, split positive definiteness, full gradient and support gap, and the strict placement of the dense continuous interval between the three-anchor and all-anchor intervals. The saved dense witness therefore establishes the claimed comparison independently of optimizer status.
- Reconstructed and checked the 112 local-information atoms and saved transferred hull witnesses for L=4 and L=7. Full history gives the same no-anchor hull; the L=2 bound is at least one. The displayed L=4 upper bound `2.212989488` is outward: its saved rational upper value is approximately `2.212989487135879332538491771343293786738`.
- Built the n=8, d=3 covariance independently from the initial latent state and process-noise block covariance, rather than the producer's lag formula. Verified positive process covariance and nonnormal transition.
- Verified **112 full 9-by-9 matrix inequalities** by exact rational LDL signs, namely both sides of the innovation-covariance sandwich for all 56 schedules. This is stronger finite-instance evidence than the producer's scalar-information sandwich check.
- Verified exact local and true optima, common incumbent, old and sharp-far errors, both upper bounds, and both relative gaps. Every displayed fresh-block certified inequality is outward.
- Inspected the archived d=4/d=16 promise checks and the old/new constant formulas. The paper correctly identifies these as a new constant comparison, without assigning a new certified bound to an old floating-point run.
- Checked fresh table timing fields against the saved records. Atom construction and common optimum setup are charged separately; numerical search includes numerical pricing; exact certification includes the full support price. The larger separator table and surrounding prose retain certification and common work, including the n=192, b=16 total above 30 seconds. No speedup claim is made from the tiny fresh example.

## Minor finding M1: verify Schur stationarity before accepting the saved lower witness

Location: `supplement/validate_models.py`, around lines 64–70.

The independent checker currently sets `N = E.T * M * E`, verifies `W*N == I`, then treats `log(det(N))` as the feasible-mixture lower value. For arbitrary saved `G`, the variational identity gives `E.T*M*E >= Schur(M)`; therefore this quadratic form is generally an **upper** matrix, not the mixture Schur matrix. Positive `W` and `W*N == I` alone do not establish the lower witness. The producer does compute the minimizing `G`, and I independently verified that all four current saved witnesses satisfy the exact stationarity equation. Thus the present paper's intervals are correct, and this is a localized omission in the checker contract, not a false scientific bound.

Remedy: explicitly verify that the nuisance principal block is SPD (or use its already-established structural SPD property with a clear assertion), then assert

```python
M[p:, p:] * G + M[p:, :p] == zeros(q, p)
```

for nonempty anchors. Compute the Schur matrix directly, assert that it equals `N` and the stored `mixture_information`, and then accept the lower bound. The empty-anchor case is immediate. An additional small negative fixture with a perturbed `G` would provide distinct confidence that this condition is actually enforced, but the essential correction is the exact identity check itself.

## Broader assessment

The experiment is careful about the difference between a true integer objective and a feasible mixture lower bound. It uses complete schedules at every hierarchy level, avoiding the expected-count relaxation mismatch. Its scalar split comparison disproves universal separator dominance rather than asserting it. The full-block evidence supports a modest improvement in a conservative uniform constant, and the negative large-packet results are retained. The kinetic derivative formulas and augmented linear ODE formulation agree structurally; their numerical checks are appropriately distinguished from validated derivative enclosures. No new literature-based novelty assertion is introduced in this stage. I found no major mathematical or scientific problem requiring a repeated five-reviewer cycle.
