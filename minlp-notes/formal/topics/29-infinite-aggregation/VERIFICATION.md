# Topic 29 verification record

Date: 2026-09-22. The package covers all 12 frozen claims in 18 Lean
modules. It formalizes the recommended infinite-aggregation construction
for every `r≥2`, including the four-variable case.

## Targeted Lean checks

From the repository root:

```sh
python3 formal/topics/29-infinite-aggregation/verification/run_checks.py
```

The runner uses the pinned Lean 4.33.1 toolchain and one Lean worker. It
checks only the explicit targets in [modules.json](verification/modules.json):

1. `lake build --wfail` on the 18 modules: passed without warnings.
2. `lake env lean topics/29-infinite-aggregation/verification/AuditAggregation.lean`:
   passed for **248 owned declarations**, including private and generated
   declarations. Transitive axiom dependencies are limited to `propext`,
   `Classical.choice`, and `Quot.sound`.
3. `lake env leanchecker MODULE` separately for all 18 modules: passed.
4. Canonical root imports and before/after SHA-256 source checks: passed.

The [manifest](verification/manifest.json), [build log](verification/build.log),
[axiom log](verification/axioms.log), and `kernel-*.log` files record the
results. Successful kernel replays are silent and exit zero. Kernel replay
uses the pinned Lean kernel, not an independently implemented checker.
Imported declarations are included in transitive axiom checking; the
module replays do not rebuild every dependency from source.

No project-wide checks or CI inspection were run. Source fingerprints also
confirmed that all 11 topic-27 and 10 topic-28 proof files remain unchanged
from their respective verification manifests. Independent semantic review
is recorded in [REVIEW.md](REVIEW.md).

## Paper and documentation checks

From `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build formal-infinite-aggregation.tex
```

This produced a two-page supplement. The initial build exposed one
overfull path; using a breakable path fixed it. The final LaTeX log has
no warnings, overfull or underfull boxes, undefined references, or
duplicate labels. `pdftotext -layout` and `pdfinfo` also passed; a targeted
text check confirmed the HHC, eigenvalue, uncountability, and closed-hull
discussion. See the [build log](verification/paper-build.log),
[final LaTeX log](verification/paper-final.log),
[extracted text](verification/paper-text.txt), [PDF information](verification/paper-info.txt),
and [source/PDF fingerprints](verification/paper-sources.json).

The supplement states the proved construction and explicitly excludes
the exact hull formula, arbitrary-quadratic obstruction, countable weak
sufficiency, SDP lift, and quantitative or general Gram-map claims.
It does not certify the concurrently developed main manuscript as a whole
or replace its separate review stages. The source note and repository
indices distinguish this Lean scope from their broader mathematical claims.

The final [documentation checks](verification/documentation-checks.txt)
passed: 436 local links across 33 related Markdown documents, whitespace
checks, and targeted `git diff --check`. All 39 Lean source fingerprints
across topics 27–29 still matched their respective manifests.
