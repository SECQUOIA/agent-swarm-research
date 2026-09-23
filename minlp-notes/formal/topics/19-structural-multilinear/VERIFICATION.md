# Topic 19 verification record

Lean verification date: 2026-09-21. All 25 obligations in [CLAIMS.md](CLAIMS.md) have
complete declaration mappings and independent reviews. **The final topic-only
build, all-declaration axiom audit and all 66 kernel replays passed.** Source
fingerprints stayed unchanged throughout the run. Topic 19 is complete
within this frozen gap scope.

## Reproduce the targeted Lean checks

From the repository root:

```sh
python3 formal/topics/19-structural-multilinear/verification/run_checks.py
```

The runner sets `PATH=$HOME/.elan/bin:$PATH` and `LEAN_NUM_THREADS=1`, then
runs the following from `formal/`:

1. `lake build --wfail` with exactly the 66 explicit targets in
   [modules.json](verification/modules.json): passed without warnings.
2. `lake env lean topics/19-structural-multilinear/verification/AuditStructural.lean`:
   passed for **1,904 declarations across 66 modules**. Module ownership
   includes private helpers and generated declarations. Every transitive axiom
   dependency belongs to `propext`, `Classical.choice`, or `Quot.sound`.
   The audit would reject `sorryAx` or any other custom axiom.
3. `lake env leanchecker MODULE` once per listed module: all 66 exited zero.
4. Verify that every topic module is imported by the canonical `Formal.lean`,
   and that the topic sources have identical SHA-256 hashes before and after
   the run: both checks passed. The runner never builds or imports the full
   canonical root.

The checked toolchain is `leanprover/lean4:v4.33.1`. The runner records the
pinned Lake manifest hash and each topic source hash in
[manifest.json](verification/manifest.json). The combined build output is in
[build.log](verification/build.log); the owned-declaration audit output is in
[axioms.log](verification/axioms.log). Individual `kernel-*.log` files hold
kernel-checker output; an empty file is normal for a successful silent check.
The completed manifest is written only after all commands exit zero and the
source-fingerprint comparison passes.

Kernel replay checks the compiled proof terms with the installed Lean kernel
and pinned imports. It is not a fresh replay of all Mathlib or an independently
implemented proof checker. The human-readable claim correspondence is assessed
by the [independent reviews](REVIEW.md), separately from kernel validity.

No project-wide verification or CI status/log inspection was performed.
Earlier scoped implementation and review checks are preserved in their
individual reports; the final source hashes identify the integrated version.

## Shared finite-mixture definition (2026-09-21)

A source search and inspection of the existing declaration indexes for all
684 proof modules found one declaration-name collision:
`MultilinearGap.finiteMixture` was defined in both `ExactLaw` and
`StructuralAveraging`. Other repeated short names were private or belonged
to different namespaces.

`StructuralAveraging` now imports `ExactLaw` and reuses its finite-mixture
definition and expectation theorem. This preserves the theorem statements
and makes a duplicate definition fail during the targeted module build,
without requiring the project root to expose the collision. Inspection of
the rebuilt declaration indexes found no remaining collision.

The targeted runner above passed and refreshed the build log, axiom audit,
all 66 kernel replays, and source manifest. The audit now counts 1,904
topic-owned declarations; the shared definition belongs to `ExactLaw`.
`git diff --check` also passed. No project-wide build or CI inspection was
performed for this correction.

## Related paper and documentation

The following targeted command passed from `paper-relaxation-limits/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The current [paper PDF](../../../paper-relaxation-limits/main.pdf) has 113
pages. The final log contains no undefined references or citations, duplicate
labels, or overfull boxes. Three underfull boxes remain in the navigation
table and a supporting appendix. `pdftotext` confirmed that the new scope and
proof-route paragraphs are present. This was not a complete visual review.

The [build log](verification/paper-build.log),
[final TeX log](verification/paper-final.log), and
[paper source/PDF hashes](verification/paper-build.json) preserve this check.
The introduction, sections 5–6, paper README and four related result notes
identify the proved scope and excluded algorithmic claims. The feedback lemma
now states the residual-incidence acyclicity hypothesis explicitly. The
formal TU proof uses the proved Ghouila–Houri signing route in place of the
source's Camion argument. No mathematical defect was found in the scoped gap
statements by the independent reviews.

The source coverage retains the verified unequal-positive-box ratio `7/6`
and the unresolved general frequency-two bound there. Generic nonnegative
payoff sharpness is distinguished from unproved positive-monomial sharpness
for arbitrary feedback size. Historical manuscript snapshots and unrelated
standalone proof exports were not changed.

The final documentation check resolved 405 local Markdown links across 29
changed or topic-specific documents, with no missing targets. `git diff --check`
passed. The recorded check output is `verification/documentation-check.json`.
A final comparison confirmed that all 66 source hashes still match the
successful Lean audit manifest.
