# Verification record

The standalone project contains 61 exported proof modules, pinned to Lean
and Mathlib 4.33.1. Status: complete. All standalone checks passed on 2026-09-16.

| Check | Result |
|---|---|
| Complete module imports | PASS: 61 proof modules |
| Warning-free project build | PASS |
| Transitive declaration audit | PASS: 1,247 declarations |
| Kernel replay of all proof modules and the root import | PASS |
| Byte equality with the canonical source export | PASS |
| Complete manuscript claim review | PASS |

The [run log](verification/run.log) records the actual standalone command:

```sh
bash scripts/verify.sh
```

The local run started with no project build cache. It reused the canonical
installation's cached standard dependencies through a local, ignored
`.lake/packages` symlink. Every exported project module was compiled from
its own source here; canonical project proof objects were not copied.
This was a fresh project build, not a fresh download or rebuild of Mathlib.
The symlink is not part of the distribution. A separate checkout can fetch
the dependencies from the pinned configuration.

The axiom audit checks every package-owned declaration, including private
helpers, transitively. It permits only `propext`, `Classical.choice`, and
`Quot.sound`. Kernel replay uses the installed Lean kernel; it does not use
an independently implemented kernel.

The [claim map](COVERAGE.md) and [independent review](../verification/completion-review.md)
cover the entire mathematical manuscript. They distinguish actual graph-hull
statements from scalar identities and distinguish the convergent lower
certificate from an unclaimed limit of the actual ratios. They do not
establish publication priority or external peer review.

The [export manifest](verification/export.json) records the endpoint closure
and canonical source fingerprints. The [delivery fingerprints](../verification/SHA256SUMS)
cover the paper, scripts, proof sources, and recorded checks. Paper build
and link results are in [paper-build.json](../verification/paper-build.json)
and [bundle-check.json](../verification/bundle-check.json).
