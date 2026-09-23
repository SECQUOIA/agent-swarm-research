# Topic 28 verification record

Date: 2026-09-22. All 12 frozen obligations are covered by 10 new Lean
modules. This extends topic 27 without changing its 11 proof modules or
its frozen source claims.

## Targeted Lean verification

The following command passed from the repository root:

```sh
python3 formal/topics/28-quadratic-aggregation-consequences/verification/run_checks.py
```

The runner uses the pinned Lean 4.33.1 toolchain and one Lean worker. It ran:

1. `lake build --wfail` on the 10 explicit targets in
   [modules.json](verification/modules.json): passed without warnings.
2. `lake env lean topics/28-quadratic-aggregation-consequences/verification/AuditAggregation.lean`:
   passed for **158 owned declarations**, including private helpers and
   generated declarations. Every transitive axiom dependency belongs to
   `propext`, `Classical.choice`, or `Quot.sound`.
3. `lake env leanchecker MODULE` for each of the 10 modules: every replay
   exited zero.
4. Canonical root import checks and before/after SHA-256 source comparisons:
   passed. No topic source changed during verification.

See the [manifest](verification/manifest.json),
[build output](verification/build.log), [axiom output](verification/axioms.log),
and individual `kernel-*.log` files. Empty kernel logs indicate successful
silent checks. The manifest records the source, toolchain, and dependency
manifest fingerprints. Imported topic-27 and Mathlib declarations are
dependencies; the axiom sweep checks them transitively, while the module
replays do not rebuild all dependencies from source.

No project-wide verification or CI inspection was run. Kernel replay uses
the pinned Lean kernel, not a separately implemented checker. Independent
semantic review is recorded in [REVIEW.md](REVIEW.md).

## Related paper and documentation

The following command passed from `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build formal-consequences.tex
```

From the repository root, these commands also passed:

```sh
pdftotext -layout paper-quadratic-aggregation/build/formal-consequences.pdf formal/topics/28-quadratic-aggregation-consequences/verification/paper-text.txt
pdfinfo paper-quadratic-aggregation/build/formal-consequences.pdf
```

The checked supplement has nine pages. A targeted Python scan found no
LaTeX or box warnings, missing references/citations, or duplicate labels
or bibliography keys. Its extracted text contains the Shor characterization,
exact SDP tests, and boundary examples. The initial wrapper omitted the
concurrently added certificate-proof section, causing undefined references;
the wrapper was corrected and the final build was clean. See the
[build log](verification/paper-build.log),
[final LaTeX log](verification/paper-final.log),
[extracted text](verification/paper-text.txt), and
[source/PDF fingerprints](verification/paper-sources.json).

The source note records the simpler strict-separation proof of Lemma 4.
The formal package indices and source reviews distinguish the newly
verified consequences from the deferred full hull theorem, general
three-form convexity criteria, numerical software and other examples.
The supplement is independent of the concurrently developed main paper's
review stages. This record does not certify that manuscript as a whole.

Targeted local Markdown-link checks and `git diff --check` on the related
tracked files passed. A fingerprint comparison also confirmed that all 11
topic-27 Lean source files remain unchanged from their original manifest.
