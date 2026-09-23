Completed locally on 2026-09-11 20:00:13 UTC.

All selected switching-control results passed the full verification script.
The [coverage record](COVERAGE.md) identifies the exact statements and exclusions.

| Check | Result |
|---|---|
| Import coverage | PASS: all 32 project proof modules imported, including 21 switching modules |
| `lake build --wfail` | PASS: no errors or warnings |
| Module-ownership axiom audit | PASS: all 11,882 project declarations, including private helpers |
| Allowed axioms | Only `propext`, `Classical.choice`, and `Quot.sound` |
| `LEAN_NUM_THREADS=1 lake env leanchecker -v Formal` | PASS: every project module replayed, including the existing exact-count package |
| Auditor negative control | PASS: unrelated-namespace axiom in a temporary project module was rejected |
| Certificate regeneration | PASS: deterministic generator output matches the checked-in certificate file |
| Specification review | Universal inputs, all budgeted schedules, boundary extension, full-time interpolation, measurable realization, and positive scaling reviewed |

The main full-scope grid declarations are `five_measurable_grid_exact`,
`six_measurable_grid_exact`, and `seven_measurable_grid_exact` in
[`GridResults.lean`](../../Formal/SwitchingControl/GridResults.lean).
They quantify over every positive cell width and bound error throughout every
cell. Matching measurable inputs force the same errors against all competing
grid words. The continuous result is
`ContinuousResults.measurable_three_mode_two_switch_minimax`, for every `T > 0`.

The complete [run log](verification/run.log) and
[negative-control record](verification/audit-negative-control.log) are retained.
The [source fingerprints](verification/SHA256SUMS) cover this topic's proof
sources, generator, toolchain pins, and source manuscript/checker. Run
`sha256sum -c topics/01-switching-control/verification/SHA256SUMS` from `formal/`.

Lean 4.33.1 and Mathlib v4.33.1 are shared with the existing project. The
certificate's warning-free build took about six minutes locally; replay used
one worker to bound memory. Neither Python nor an external solver is trusted
to validate a mathematical claim. Generated witnesses use ordinary kernel
reduction, and there are no unfinished proofs or custom axioms.

Replay uses Lean's installed kernel and imported Mathlib declarations. It is
not an independently implemented proof assistant or a fresh replay of all
Mathlib. The formal guarantee applies to the documented definitions; it does
not verify every auxiliary or bibliographic claim in the paper. No changes
were pushed or published, and the GitHub workflow was not run remotely.
