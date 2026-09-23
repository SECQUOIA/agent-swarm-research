# Topic 20 verification record

Date: 2026-09-20. All 24 obligations in [CLAIMS.md](CLAIMS.md) have complete
[declaration mappings](COVERAGE.md) and [independent reviews](REVIEW.md).
**The final topic-only build, all-declaration axiom audit and all 57 kernel
replays passed.** Topic sources stayed unchanged throughout the run.
Topic 20 is complete within its frozen scalar quadratic scope.

## Targeted Lean checks

Reproduce from the repository root:

```sh
python3 formal/topics/20-scalar-quadratic/verification/run_checks.py
```

The runner sets `PATH=$HOME/.elan/bin:$PATH` and `LEAN_NUM_THREADS=1`, then
runs these commands from `formal/`:

1. `lake build --wfail` with exactly the 57 explicit targets in
   [modules.json](verification/modules.json): passed without warnings.
2. `lake env lean topics/20-scalar-quadratic/verification/AuditQuadratic.lean`:
   passed for **979 declarations across 57 modules**, including private helpers
   and generated declarations. Every transitive axiom dependency belongs to
   `propext`, `Classical.choice`, or `Quot.sound`. The audit rejects `sorryAx`
   and other custom axioms.
3. `lake env leanchecker MODULE` for every listed module: all 57 exited zero.
4. Every listed module is imported by canonical `Formal.lean`, and SHA-256
   source fingerprints match before and after the checks. The runner does
   not build or import the full canonical root.

The checked toolchain is `leanprover/lean4:v4.33.1`. The
[manifest](verification/manifest.json) records the pinned Lake manifest hash
and each topic source hash. See [build output](verification/build.log),
[axiom output](verification/axioms.log), and the individual `kernel-*.log`
files. Empty kernel logs are normal for successful silent checks. The runner
writes the completed manifest only after every check passes.

Kernel replay checks compiled proof terms with the installed Lean kernel and
pinned imports; it is not a fresh replay of all Mathlib or an independently
implemented checker. The claim-to-theorem correspondence is assessed by the
independent reviews. No project-wide verification or CI inspection was run.

## Related paper and documentation

These targeted commands passed from `paper-integer-dimension/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
python verification/check_manuscript.py
pdftotext -layout build/main.pdf build/topic20-review.txt
```

The current [paper PDF](../../../paper-integer-dimension/build/main.pdf) has
88 pages. The final LaTeX log has no warnings, and the manuscript checker
found no duplicate labels, unresolved references, duplicate bibliography keys,
or unresolved citations. PDF text on pages 3, 13 and 15 was inspected for the
scope and proof-route updates; this was not a complete visual page review.
See the [build log](verification/paper-build.log),
[final LaTeX log](verification/paper-final.log),
[paper checks](verification/paper-checks.json), and
[note, manuscript and PDF fingerprints](verification/paper-sources.json).
Historical submission and review artifacts were not replaced.

The three related result notes and manuscript distinguish scalar verification
from the remaining vector quadratic results. They state the missing `δ≥0`
contact-volume hypothesis, actual construction sizes, folding-depth convention,
and exact convex product attainment versus positive-slack finite linear lifts.
The [documentation review](reviews/documentation.md) passed. Its release
prerequisite—the then-running final audit—is now satisfied by this record.
Targeted local Markdown link checks and `git diff --check` also passed.
