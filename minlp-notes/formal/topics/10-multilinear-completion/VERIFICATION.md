# Verification of the multilinear completion

The package adds seven proof modules to the canonical project, bringing it
to 147 proof modules at this completion stage. The standalone paper exports
48 modules with the same pinned Lean and Mathlib 4.33.1 dependencies.

Status: complete. All listed checks passed on 2026-09-16.

| Check | Result |
|---|---|
| Canonical import coverage | PASS: 147 modules |
| Canonical warning-free build | PASS |
| Canonical transitive axiom audit | PASS: 14,756 declarations |
| Standalone import coverage and warning-free build | PASS: 48 modules |
| Standalone transitive axiom audit | PASS: 827 declarations |
| Standalone kernel replay | PASS: all 48 proof modules and the root import |
| Canonical kernel replay | PASS: all 147 proof modules and the root import |
| Export comparison | PASS: all 48 sources and pinned dependency configuration |
| Paper build | PASS: 11 pages, no unresolved references, overfull boxes, or layout/package warnings |
| Bundle links and supplemental arithmetic | PASS: 104 local links, four table rows, 330 cutoff-law states |
| Mathematical statement review | PASS; independent review of each new module |

The two changed appendix pages were rendered and inspected. The four table
rows are also Lean theorems about the actual hull and termwise gaps, so their
formal status does not rest on the supplemental arithmetic checks.

Source fingerprints are in [SHA256SUMS](verification/SHA256SUMS), relative
to the canonical `formal/` directory. They cover all 48 exported proof sources
and the three pinned dependency configuration files.

## Reproduce

From the canonical `formal/` directory:

```sh
bash scripts/verify.sh
```

The [recorded canonical run](verification/run.log) includes import coverage,
generated-data checks, a warning-free build, transitive axiom audit, and
kernel replay. Only `propext`, `Classical.choice`, and `Quot.sound` are
permitted. The replay uses the installed Lean kernel and cached standard
dependencies; it is not an independent kernel implementation.

The [standalone verification record](../../../paper-multilinear-gap/formal/VERIFICATION.md)
records the separately built exported package. Its verification script needs
only that package and its pinned dependencies. Local tests can reuse cached
standard dependencies without trusting canonical project proof objects.

The [mathematical review](REVIEW.md) and [coverage guide](COVERAGE.md) record
the connection between the manuscript and the formal statements.
