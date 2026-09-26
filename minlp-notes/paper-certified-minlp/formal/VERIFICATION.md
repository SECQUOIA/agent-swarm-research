# Certified MINLP extension verification

Status: complete. Targeted mathematical and documentation checks passed on
2026-09-17. The two axiom-audit programs and the source fingerprints were rerun
on 2026-09-25; see below.

The extension adds 24 modules to the existing three-module standalone project.
The [coverage map](COVERAGE.md) accounts for all 49 mathematical obligations.

| Check | Result |
|---|---|
| Targeted warning-free builds | PASS: all 24 added modules and their dependencies |
| Targeted transitive axiom audit | PASS: 1,112 declarations owned by the 24 added modules; rerun at `549a5786` with the same count |
| Structured checker examples | PASS: 17 acceptance/rejection examples evaluated with `decide +kernel`, and one example (`integer_half_bound`) applying the checker soundness theorem |
| Rational PSD examples | PASS: three boundary examples proved with `norm_num` and kernel-checked |
| Independent mathematical review | PASS for all 49 obligations: the three original review scopes name 47, and the [supplementary review](REVIEW-CM04-CM34.md) of 2026-09-25 covers CM04 and CM34 |
| Source fingerprints | PASS at `549a5786`: the same 34 proof, audit, and configuration files, in the new manifest `verification/extension-SHA256SUMS-2026-09-25`. The historical manifest `verification/extension-SHA256SUMS` records `875a71ab`; see below. |
| Documentation links | PASS: 139 topic and standalone links |
| Revised manuscript | PASS: fresh PDF build without warnings; revised Section 5 pages visually checked |
| Project-wide verification | Not run locally; assigned to CI, but the committed workflow does not build this standalone project |
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
sha256sum -c verification/extension-SHA256SUMS-2026-09-25
```

The historical fingerprint manifest, `verification/extension-SHA256SUMS`,
records the sources committed in `875a71ab`. Commit `fa2a6f42` later wrapped one
long log-message line in each of `Verify.lean` and
`verification/ExtensionAudit.lean`, so on current sources that manifest check
reports those two files as mismatched; the other 32 entries match. The checks
above were first run on the sources committed in `875a71ab`.

On 2026-09-25 both changed audit programs were run at `549a5786`, where no proof
module, configuration file or module list differs from `875a71ab`. The
[run log](verification/extension-run-2026-09-25.log) records the commands and
output. The documented targeted build of the 24 modules and
`lake build --wfail CertifiedMinlp` both exited 0 with no warnings; Lake found
all 27 proof modules up to date and compiled only the umbrella file. Then:

- `lake env lean Verify.lean`: PASS, 1,207 project declarations over all 27
  modules. No earlier record reports this program's count for the extended
  project; the baseline log reports 95 for the original three modules.
- `lake env lean verification/ExtensionAudit.lean`: PASS, 1,112 declarations
  in the 24 extension modules, matching the earlier audit.

Every audited declaration depends only on `propext`, `Classical.choice` and
`Quot.sound`. After these passes, the current manifest
`verification/extension-SHA256SUMS-2026-09-25` was written for the same 34 files
in the same order; it differs from the historical manifest only in the entries
for the two audit programs. This rerun renews the axiom audits and the
fingerprints. It is not a fresh compilation of the proof modules, and it is not
a kernel replay or a project-wide run.

Lean checks proofs during elaboration. The structured-checker examples are
evaluated with `decide +kernel`, and the rational PSD examples are proved with
`norm_num`; all are kernel-checked, and none uses `native_decide`. The
extension does not claim another project-wide kernel replay. The original `verification/run.log` and `verification/SHA256SUMS`
remain historical records of the earlier three-module package. Its old
umbrella fingerprint is not the current umbrella fingerprint.

Project-wide verification is assigned to CI. Do not run it locally or inspect
CI status or logs. This rule applies to the canonical and standalone projects;
local work uses explicit topic/module targets. The committed workflow,
`.github/workflows/lean.yml`, builds and audits only `formal/`; it does not
build or check this standalone project, so its project-wide verification is
assigned but not configured. No current CI outcome is asserted by this record.

The mathematical proofs and structured Lean checkers do not verify the
Python implementation, external arithmetic libraries, parser, or benchmark
artifacts. See [coverage](COVERAGE.md) and [review](REVIEW.md) for exact limits.
