Completed locally on 2026-09-12 with pinned Lean 4.33.1 and Mathlib v4.33.1.

| Check | Result |
|---|---|
| Endpoint and integrated root build with warnings treated as failures | PASS |
| Explicit proof-module import coverage | PASS: all 140 project proof modules |
| Project-wide transitive axiom audit | PASS: 14,663 declarations, including private helpers |
| Cube upper bound, box transfer, and final sharp-growth declarations | Only `propext`, `Classical.choice`, and `Quot.sound` |
| Kernel replay | PASS: all eighteen sharp-growth modules; process exit status zero |
| Independent specification review | PASS; see [record](REVIEW.md) |

The [shared integration log](../08-exact-multilinear/verification/run.log)
records the root build and full axiom audit for both new packages.
This package's [replay log](verification/run.log) records its eighteen
new modules. The seven exact-formula modules have a separate
[verification record](../08-exact-multilinear/VERIFICATION.md).

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

Replay the sharp-growth modules with one worker:

```bash
LEAN_NUM_THREADS=1 lake env leanchecker -v \
  Formal.MultilinearGap.AsymptoticScalars \
  Formal.MultilinearGap.BoxSuprema \
  Formal.MultilinearGap.BoxTransfer \
  Formal.MultilinearGap.Couplings \
  Formal.MultilinearGap.EasyTerms \
  Formal.MultilinearGap.ExactDimension \
  Formal.MultilinearGap.FamilySize \
  Formal.MultilinearGap.GeneralGaps \
  Formal.MultilinearGap.HarmonicDensity \
  Formal.MultilinearGap.HarmonicGain \
  Formal.MultilinearGap.HarmonicLawGain \
  Formal.MultilinearGap.IntegratedLaws \
  Formal.MultilinearGap.LowerAsymptotics \
  Formal.MultilinearGap.Mixture \
  Formal.MultilinearGap.Padding \
  Formal.MultilinearGap.SharpAsymptotics \
  Formal.MultilinearGap.SharpUpper \
  Formal.MultilinearGap.Suprema
```

Source, dependency, and documentation fingerprints are in
`verification/SHA256SUMS`. Check them from `formal/` with
`sha256sum -c topics/09-sharp-multilinear/verification/SHA256SUMS`.
The [coverage table](COVERAGE.md) states the precise mathematical scope
and distinguishes the proved leading-order result from the stronger
finite and second-order upper bounds still to be verified.
