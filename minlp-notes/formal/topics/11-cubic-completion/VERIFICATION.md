# Cubic completion verification

Status: complete. All canonical and standalone checks passed on 2026-09-16.

The package adds thirteen proof modules. The canonical project contains
160 proof modules at this completion stage; the standalone cubic paper
exports 61 modules and the pinned Lean and Mathlib 4.33.1 configuration.

| Check | Result |
|---|---|
| Canonical import coverage | PASS: 160 proof modules |
| Generated certificate reproducibility | PASS |
| Canonical warning-free build | PASS |
| Canonical transitive axiom audit | PASS: 15,019 declarations |
| Canonical kernel replay | PASS: all 160 proof modules and the root import |
| Standalone import coverage | PASS: 61 proof modules |
| Standalone warning-free build | PASS |
| Standalone transitive axiom audit | PASS: 1,247 declarations |
| Standalone kernel replay | PASS: all 61 proof modules and the root import |
| Source export comparison | PASS: all 61 sources and three pinned configuration files |
| Mathematical claim review | PASS: complete focused manuscript and all new modules |
| Paper build | PASS: six pages, no unresolved references, overfull boxes, or layout/package warnings |
| Paper visual inspection | PASS: all six pages |
| Delivery links and fingerprints | PASS: 38 standalone local links, 88 delivery files, and 71 topic-navigation links |

The [canonical run log](verification/run.log) records the integrated checks.
[Source fingerprints](verification/SHA256SUMS), relative to the canonical
`formal/` directory, cover the complete 61-module exported proof closure and
three pinned configuration files. The
[standalone record](../../../paper-cubic-gap/formal/VERIFICATION.md) documents
the separate source build and replay. The [review](REVIEW.md) and
[coverage map](COVERAGE.md) identify the mathematical scope.

## Reproduce

From the canonical `formal/` directory:

```sh
bash scripts/verify.sh
sha256sum --check topics/11-cubic-completion/verification/SHA256SUMS
```

From the repository root:

```sh
python3 paper-cubic-gap/scripts/export_proofs.py formal --check
```

Only `propext`, `Classical.choice`, and `Quot.sound` are permitted. The audit
checks every module-owned declaration transitively, including private helpers.
The kernel replay uses the installed Lean kernel; it is not a separately
implemented checker. Cached standard dependencies are reused. The isolated
paper build compiles its own exported project sources and does not copy
canonical project proof objects.

Topic 2 began after topic 1 passed both its canonical and standalone
verification scripts. Earlier topic verification records describe their own
historical source snapshots and counts.
