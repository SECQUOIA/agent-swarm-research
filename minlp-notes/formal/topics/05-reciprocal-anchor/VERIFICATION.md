Completed locally on 2026-09-11.

| Check | Result |
|---|---|
| Import coverage | PASS: all 87 project modules, including 9 reciprocal-anchor modules |
| Full project build with `--wfail` | PASS |
| Full project axiom audit | PASS: 13,379 declarations, including private helpers |
| Allowed axioms | Only `propext`, `Classical.choice`, `Quot.sound` |
| Kernel replay | PASS: all 9 `Formal.ReciprocalAnchor` modules |
| Previously completed topics | PASS: all four source fingerprints unchanged |
| Independent review | PASS: moment allocation, zero-mass cases, six-atom representation, actual PSD equivalence, cut coefficients, and exact witnesses |

The [run log](verification/run.log) records the checks. The main hull theorems
are `mem_hull_iff_conicBounds` and `mem_hull_iff_psd`.
`individual_hulls_not_joint` establishes the obstruction, and `joint_cut_valid`
proves the separating inequality on the true hull.

The [coverage record](COVERAGE.md) states the exact scope and excluded claims.
These are proofs of the full stated hull equalities and joint nonmembership,
not only tests of necessary inequalities or numerical examples. The fixed-anchor
case is proved separately by `mem_hull_degenerate_iff`.

This stage rebuilt and audited the whole project and replayed the newly added
reciprocal-anchor modules. Kernel replay uses the installed Lean kernel and
imported Mathlib base. Lean 4.33.1 and Mathlib v4.33.1 remain pinned. No custom
axioms, unfinished proofs, native-computation axioms, or external solver results
are used.

Run `bash scripts/verify.sh` from `formal/` for the complete project check.
[SHA256SUMS](verification/SHA256SUMS) fingerprints the proofs, dependencies, and
mathematical source; check with
`sha256sum -c topics/05-reciprocal-anchor/verification/SHA256SUMS` from `formal/`.
