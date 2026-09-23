Completed locally on 2026-09-11.

| Check | Result |
|---|---|
| Import coverage | PASS: all 50 project modules, including 10 potential-flow modules |
| Full project build with `--wfail` | PASS |
| Full project axiom audit | PASS: 12,574 declarations, including private helpers |
| Allowed axioms | Only `propext`, `Classical.choice`, `Quot.sound` |
| Kernel replay | PASS: all 10 `Formal.PotentialFlow` modules |
| Saved JSON translation | PASS: generator `--check` reproduces the exact Lean data |
| Previously completed topics | PASS: switching and FBBT fingerprints unchanged |
| Independent mathematical review | PASS: sign conventions, modulus, graph scope, rational transport, final soundness statement |

The [run log](verification/run.log) records these checks. The main theorem is
`PotentialFlow.RationalNetwork.accepted_sound`. The saved example is checked by
`PotentialFlow.Example.accepted` using kernel computation and applied to the
real physical flow by `PotentialFlow.Example.saved_example_verified`.

The [coverage record](COVERAGE.md) identifies the excluded claims. In particular,
this package certifies the deterministic network in the JSON, not its mapping
from an original uncertainty problem or the Python verifier implementation.

Run `bash scripts/verify.sh` from `formal/` for the complete project check.
This stage rebuilt and audited the complete project and replayed the newly
added potential-flow modules. Kernel replay uses the installed Lean kernel and
imported Mathlib base. Lean 4.33.1 and Mathlib v4.33.1 remain pinned.

[SHA256SUMS](verification/SHA256SUMS) fingerprints the proofs, generator,
dependency pins, and source certificate. Check with
`sha256sum -c topics/03-potential-flow/verification/SHA256SUMS` from `formal/`.
