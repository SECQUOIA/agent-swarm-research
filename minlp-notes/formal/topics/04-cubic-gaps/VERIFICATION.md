Completed locally on 2026-09-11.

| Check | Result |
|---|---|
| Import coverage | PASS: all 78 project modules, including 28 cubic modules |
| Full project build with `--wfail` | PASS |
| Full project axiom audit | PASS: 13,273 declarations, including private helpers |
| Allowed axioms | Only `propext`, `Classical.choice`, `Quot.sound` |
| Kernel replay | PASS: every `Formal.CubicGap` module |
| Large certificate reproduction | PASS: generated source matches the checked-in proof |
| Previously completed topics | PASS: switching, FBBT, and potential-flow fingerprints unchanged |
| Independent specification review | PASS as recorded here; no separate review report was retained: continuous graph hull, finite coverage, rational casts, all singleton means, attainment, and the homogeneous construction |

The [run log](verification/run.log) records the checks other than the
specification review; the table row above is the only retained record of that
review. A later, separately documented review of the existing `CubicGap`
statements, dated 2026-09-16, is in
[topic 11's REVIEW.md](../11-cubic-completion/REVIEW.md). This stage rebuilt and
audited the complete project and replayed all 28 cubic modules through the
installed Lean kernel. The largest finite certificate covers every one of the
274,625 count triples for the 192-variable example. Its clean build took about
139 seconds on this machine; memory use is kept bounded by one Lean worker.

`Ratios.lean` proves all seven exact finite ratios using actual graph-hull widths
and sums of individual monomial envelope values. `OrbitExpansion.lean` connects
their factors to the original polynomial definitions and proves nonnegative
coefficient scaling. `homogeneous52_exact_envelope_ratio` proves the explicit
52-variable unit-coefficient bound. `Bernstein.scalar_minorant` proves the
universal positive-slack scalar certificate.

See [COVERAGE.md](COVERAGE.md) for the claims excluded from this package.
No numerical solver or Python computation is a trusted proof step. There are
no custom axioms, unfinished proofs, or native-computation axioms. Kernel replay
uses the installed Lean kernel and imported Mathlib base. The environment
remains pinned to Lean 4.33.1 and Mathlib v4.33.1.

Run `bash scripts/verify.sh` from `formal/` to reproduce the complete project
check. Source fingerprints are in [SHA256SUMS](verification/SHA256SUMS); check
with `sha256sum -c topics/04-cubic-gaps/verification/SHA256SUMS` from `formal/`.

## Fingerprint note (2026-09-25)

`sha256sum -c` on this topic's manifest now reports
`Formal/CubicGap/Envelope.lean` and `Formal/CubicGap/Results.lean` as
mismatches. This manifest does not list `MultilinearGap/EnvelopeBounds.lean`.
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
The check also reports the two `paper-relaxation-limits` manuscript sections,
which were revised later (`367fcbc8`, `aee2afbf`); they are not proof sources.
