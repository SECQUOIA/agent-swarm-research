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
| Independent specification review | PASS: continuous graph hull, finite coverage, rational casts, all singleton means, attainment, and the homogeneous construction |

The [run log](verification/run.log) records the checks. This stage rebuilt and
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
