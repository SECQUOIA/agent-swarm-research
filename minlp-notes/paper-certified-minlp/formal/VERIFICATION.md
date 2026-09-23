# Certified MINLP extension verification

Status: complete. Targeted mathematical and documentation checks passed on
2026-09-17.

The extension adds 24 modules to the existing three-module standalone project.
The [coverage map](COVERAGE.md) accounts for all 49 mathematical obligations.

| Check | Result |
|---|---|
| Targeted warning-free builds | PASS: all 24 added modules and their dependencies |
| Targeted transitive axiom audit | PASS: 1,112 declarations owned by the 24 added modules |
| Structured checker examples | PASS: 18 kernel-evaluated acceptance/rejection examples |
| Rational PSD examples | PASS: three kernel-evaluated boundary examples |
| Independent mathematical review | PASS: all 49 obligations |
| Source fingerprints | PASS: 34 proof, audit, and configuration files |
| Documentation links | PASS: 139 topic and standalone links |
| Revised manuscript | PASS: fresh PDF build without warnings; revised Section 5 pages visually checked |
| Project-wide verification | Not run locally; assigned to CI |
| CI status/log inspection | Not performed |
| Full-project kernel replay | Not run for this extension |

The [module list](verification/extension-modules.txt) names the explicit build
targets. The [build log](verification/extension-build.log) records the complete
command and successful exit. The targeted
[audit source](verification/ExtensionAudit.lean) imports those modules and
checks ownership by their exact module names, including private and generated
declarations. Its [log](verification/extension-axioms.log) records the result.
The allowed transitive axioms are only `propext`, `Classical.choice`, and
`Quot.sound`. There are no unfinished proofs or extra axioms.

For targeted reproduction from this directory, run:

```sh
xargs lake build --wfail < verification/extension-modules.txt
lake env lean verification/ExtensionAudit.lean
sha256sum -c verification/extension-SHA256SUMS
```

Lean checks proofs during elaboration; the examples use `decide`, not
`native_decide`. The extension does not claim another project-wide kernel
replay. The original `verification/run.log` and `verification/SHA256SUMS`
remain historical records of the earlier three-module package. Its old
umbrella fingerprint is not the current umbrella fingerprint.

Project-wide verification belongs to CI. Do not run it locally or inspect CI
status or logs. This rule applies to the canonical and standalone projects;
local work uses explicit topic/module targets. No current CI outcome is
asserted by this record.

The mathematical proofs and structured Lean checkers do not verify the
Python implementation, external arithmetic libraries, parser, or benchmark
artifacts. See [coverage](COVERAGE.md) and [review](REVIEW.md) for exact limits.
