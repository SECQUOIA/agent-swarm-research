Completed locally on 2026-09-11.

| Check | Result |
|---|---|
| Import coverage | PASS: all 100 project modules, including 13 network–simplex modules |
| Full project build with `--wfail` | PASS |
| Full project axiom audit | PASS: 13,902 declarations, including private helpers |
| Allowed axioms | Only `propext`, `Classical.choice`, `Quot.sound` |
| Kernel replay | PASS: all 13 `Formal.NetworkSimplex` modules |
| Earlier certificate generators | PASS: potential-flow JSON and large cubic certificate reproduce their Lean sources |
| Previously completed topics | PASS: all five source fingerprints unchanged |
| Independent specification review | PASS: actual chain incidence, simplex encoding, domain checks, residual elimination, zero weights, grouping, and exact hull/oracle equivalences |

The [run log](verification/run.log) records the checks. The final statements are
`mem_hull_iff_five_tests`, `mem_hull_iff_sixteen_tests`, and
`mem_hull_iff_circuit_tests` in `NetworkSimplex.Chain.ReductionData`.
The general disaggregation theorem is `NetworkSimplex.original_mem_hull_iff`.

The [coverage record](COVERAGE.md) specifies the mathematical statements and
excluded claims. No custom axioms, unfinished proofs, native-computation axioms,
or external solver results are used. The formalization uses Lean 4.33.1 and
Mathlib v4.33.1. Replay uses the installed Lean kernel with the imported Mathlib
base; it is not a separately implemented checker or a fresh replay of Mathlib.

Run `bash scripts/verify.sh` from `formal/` for the whole project. The topic's
[SHA256SUMS](verification/SHA256SUMS) covers its proofs, dependency pins, and
mathematical sources; check it from `formal/` with
`sha256sum -c topics/06-network-simplex/verification/SHA256SUMS`.
