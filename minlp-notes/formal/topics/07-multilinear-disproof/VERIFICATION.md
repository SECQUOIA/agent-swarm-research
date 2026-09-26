Completed locally on 2026-09-12 with pinned Lean 4.33.1 and Mathlib v4.33.1.

| Check | Result |
|---|---|
| New-package build with warnings treated as failures | PASS: all nine `Formal.MultilinearGap` modules |
| Root build with `lake build Formal --wfail` | PASS; unchanged dependencies reused |
| Explicit proof-module import coverage | PASS: all 115 project proof modules |
| Project-wide transitive axiom audit | PASS: 14,171 declarations, including private helpers |
| Both final disproof declarations | Only `propext`, `Classical.choice`, and `Quot.sound` |
| Kernel replay | PASS: all nine new modules; process exited with status zero |
| Independent implementation/specification reviews | PASS: two agent reviews; see [record](REVIEW.md) |
| Documentation review | PASS: claims and exclusions checked against the declarations |
| Whitespace check | PASS: `git diff --check` for the changed formalization and result note |

The [run log](verification/run.log) records the root build, import coverage,
full axiom audit, and new-package kernel replay. The audit rejects unfinished
proofs, custom axioms, and native-computation axioms transitively. No external
solver output or finite sample is a trusted proof step.

Kernel replay used the bundled `leanchecker` with one worker and target
`Formal.MultilinearGap`. It rechecked the new compiled declarations against
their imports using the installed Lean kernel. It is not a separate kernel
implementation and did not replay the previous 106 modules or Mathlib from
scratch. The project-wide axiom audit still covers all imported project
declarations. This is a local verification record, not a hosted CI result.

The endpoints are `MultilinearGap.unbounded_gap_ratio` and
`MultilinearGap.no_uniform_positive_multilinear_bound`. They establish the
disproof on unit cubes with coefficient-one squarefree polynomials. The
[coverage table](COVERAGE.md) excludes the exact hull formula and the sharp
asymptotic replacement.

Reproduction commands appear in the [package README](README.md). Check the
recorded source and documentation fingerprints from `formal/` with:

```bash
sha256sum -c topics/07-multilinear-disproof/verification/SHA256SUMS
```

## Fingerprint note (2026-09-25)

`sha256sum -c` on this topic's manifest now reports
`Formal/CubicGap/Envelope.lean`, `Formal/CubicGap/Results.lean` and
`Formal/MultilinearGap/EnvelopeBounds.lean` as mismatches.
Commit `6fe57343` moved the `CubicGap.hullGap` definition from
`CubicGap/Results.lean` into `CubicGap/Envelope.lean` and marked it
`noncomputable`, retaining its body and explicit typeclass parameters. It also
narrowed the import in `MultilinearGap/EnvelopeBounds.lean` from
`Formal.CubicGap.Results` to `Formal.CubicGap.Envelope`. This removes
unrelated cubic example modules from that import path without changing any
theorem statement or mathematical definition. The later full canonical runs at
`413aaccb` (160 proof modules, 15,019 audited declarations) and `c31ceb7e`
(171 proof modules, 15,240 audited declarations) built these files with
warnings treated as failures, audited their declarations and replayed them in
the kernel. The files have not changed since `6fe57343`.
The check also reports `Formal.lean` and `Verify.lean`, the project import
registry and axiom audit, which were extended as later topics were added, and
`topics/07-multilinear-disproof/VERIFICATION.md`, which gained this note.
