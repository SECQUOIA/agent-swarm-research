# Certified MINLP mathematical formalization

This standalone Lean project proves the mathematical implications specified in
[the coverage table](COVERAGE.md). The paper's Section 5 describes the scope.
The current extension adds 24 modules, covering 49 mathematical obligations
and executable Lean checks for structured discrete certificates, master
identity, and rational PSD matrices. It does not run or verify the Python
checker or any saved benchmark certificate.

## Reproduce

During repository development, use targeted builds for the changed modules.
Project-wide verification is assigned to CI: do not run it locally or inspect
CI status or logs. The committed workflow, `.github/workflows/lean.yml`, covers
only `formal/`, so no CI job currently runs this standalone project. The full
reproduction commands below are the standalone reproduction entry point, not
required local development checks.
The [current verification record](VERIFICATION.md) records targeted checks
separately from the historical verification log. The [inventory](CLAIMS.md)
and [independent reviews](REVIEW.md) accompany the source package.

Install Elan, Git, and Python 3, then run from this directory:

```bash
lake exe cache get
sha256sum -c verification/extension-SHA256SUMS-2026-09-25
bash scripts/verify.sh
```

Elan selects `leanprover/lean4:v4.33.1` from `lean-toolchain`. Mathlib's
release is `v4.33.1` and its exact commit is
`0df444a360eaa60ab8c11dca51a86af692955474`. The committed manifest pins all
transitive dependencies. Lake obtains dependencies using that manifest; the
mathlib cache download supplies compiled dependency files. No solver or Python
optimization library is needed. Downloaded packages and build products under
`.lake/` are excluded from the source deliverable.

For development in this repository, `.lake/packages` is an ignored symlink to
`../../../formal/.lake/packages`, reusing the same pinned dependencies. That
symlink is not part of the standalone source package and is not required by any
committed configuration. A fresh checkout resolves packages from the manifest.

The script checks complete umbrella-import coverage, runs `lake build --wfail`,
audits every project-owned declaration's transitive axioms (including private
and generated declarations), and invokes `leanchecker -v CertifiedMinlp`.
The axiom allowlist is exactly `propext`, `Classical.choice`, and `Quot.sound`.
The kernel replay uses the installed Lean kernel and the compiled dependencies;
it is neither an independent proof assistant nor a fresh kernel replay of all
mathlib declarations. One replay worker bounds memory use.

[The baseline log](verification/run.log) and its original source manifest
record the earlier three-module verification. They do not verify the current
extension and their old manifest is not a fingerprint of the current umbrella
import. The current extension manifest,
[extension-SHA256SUMS-2026-09-25](verification/extension-SHA256SUMS-2026-09-25),
fingerprints the same 34 files at `549a5786`. It was written after both audit
programs passed on those sources; see the [run log](verification/extension-run-2026-09-25.log)
and the [verification record](VERIFICATION.md). The historical manifest,
[extension-SHA256SUMS](verification/extension-SHA256SUMS), records the sources
committed in `875a71ab`. On current sources its check reports two mismatches,
`Verify.lean` and `verification/ExtensionAudit.lean`, whose long log-message
lines were wrapped in `fa2a6f42`.

## Meaning and limitations

Coordinate endpoints, cut data and enclosure endpoints are rational; true
support values, slopes and evaluation variables are real. Infinite bounds are
constructors, not numeric sentinels. The main cut theorem derives the affine
inequality from a support inequality, genuine value/gradient enclosures, and
the rational intercept test. It never assumes the resulting underestimator.

The extension proves the curvature rules, derives support from actual segment
derivatives, and connects these facts to accepted cut data. It proves rational
propagation, the full discrete inference invariant, checked incumbent selection,
unconditional master bounds, and explicit nonlinear graph embedding. A checked
master bijection and positive row scaling preserve that bound. Affine constants,
maximization signs, empty sets, and primal completion are included.

Derivative and enclosure data must describe the actual interpreted function.
The mathematical rules do not verify their production by Pyomo, SymPy, mpmath,
or the existing Python checker. The Lean checker consumes structured values;
ASCII parsing, mutable storage, lifetime annotations, source extraction, and
the Python-to-Lean correspondence remain outside its proof. No current CI
result or renewed full-project kernel replay is claimed.
