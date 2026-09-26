Completed locally on 2026-09-12 with pinned Lean 4.33.1 and Mathlib v4.33.1.

| Check | Result |
|---|---|
| Endpoint and integrated root build with warnings treated as failures | PASS |
| Explicit proof-module import coverage | PASS: all 140 project proof modules |
| Project-wide transitive axiom audit | PASS: 14,663 declarations, including private helpers |
| Exact gap and all-L existence declarations | Only `propext`, `Classical.choice`, and `Quot.sound` |
| Kernel replay | PASS: all seven exact-formula modules; process exit status zero |
| Independent specification review | PASS; see [record](REVIEW.md) |

The [run log](verification/run.log) includes the integrated build and audit
for both the exact-formula and sharp-growth extensions. It also records
kernel replay of this package's seven new modules. The eighteen-module
sharp-growth replay has its own [record](../09-sharp-multilinear/VERIFICATION.md).

The audit rejects unfinished proofs, custom axioms, and native-computation
axioms transitively. Replay uses the installed Lean kernel and compiled
imports as the dependency base. It is not a separate kernel implementation
and does not replay the previous 115 proof modules or Mathlib from scratch.
This is a local verification record, not a hosted CI result.

From `formal/`, with the pinned Elan toolchain on PATH, reproduce the
integrated build and audit with:

```bash
python3 scripts/check_imports.py
lake build Formal --wfail
lake env lean Verify.lean
```

Replay the exact modules with one worker:

```bash
LEAN_NUM_THREADS=1 lake env leanchecker -v \
  Formal.MultilinearGap.ExactArithmetic \
  Formal.MultilinearGap.ExactGeometry \
  Formal.MultilinearGap.ExactLaw \
  Formal.MultilinearGap.ExactResults \
  Formal.MultilinearGap.ExactUpper \
  Formal.MultilinearGap.ExactWeights \
  Formal.MultilinearGap.ResidueSums
```

Source, dependency, and documentation fingerprints are in
`verification/SHA256SUMS`. Check them from `formal/` with
`sha256sum -c topics/08-exact-multilinear/verification/SHA256SUMS`.
The [coverage table](COVERAGE.md) states the precise mathematical scope.

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
registry and axiom audit, and the documentation files `README.md`,
`VERIFICATION.md` and `topics/README.md` under `formal/`. These were updated as
later topics were added; they are not proof sources. It also reports
`topics/08-exact-multilinear/VERIFICATION.md`, which gained this note.
