# Topic 27 verification record

Date: 2026-09-22. All 12 frozen obligations are proved in 11 modules and
mapped in [COVERAGE.md](COVERAGE.md). Independent statement reviews are
collected in [REVIEW.md](REVIEW.md).

## Targeted Lean checks

The following command passed from the repository root:

```sh
python3 formal/topics/27-quadratic-aggregation/verification/run_checks.py
```

The runner sets `PATH=$HOME/.elan/bin:$PATH` and `LEAN_NUM_THREADS=1`,
then performs these checks from `formal/`:

1. `lake build --wfail` for the 11 explicit targets in
   [modules.json](verification/modules.json): passed without warnings.
2. `lake env lean topics/27-quadratic-aggregation/verification/AuditAggregation.lean`:
   passed for **178 declarations across all 11 modules**, including private
   helpers and generated declarations. All transitive axiom dependencies
   belong to `propext`, `Classical.choice`, and `Quot.sound`.
3. `lake env leanchecker MODULE` for every listed module: all 11 exited zero.
4. Every listed module is imported by canonical `Formal.lean`, and the
   source SHA-256 fingerprints match before and after verification.

The [manifest](verification/manifest.json) records every module source hash,
the pinned `leanprover/lean4:v4.33.1` toolchain, and the Lake manifest hash.
The [build log](verification/build.log), [axiom log](verification/axioms.log),
and individual `kernel-*.log` files record the run. Empty kernel logs mean
successful silent checks. The unused-in-the-headline cone-separation module
is included explicitly, so the independent source Lemma 3 is audited too.

Kernel replay uses the installed Lean kernel and imported dependencies.
It does not replay all of Mathlib from scratch and is not a separate proof
assistant implementation. The semantic correspondence to the source is
covered by the independent reviews. No unfinished proof, custom axiom, or
native-computation axiom is accepted.

No project-wide build, project-wide verification script, or CI inspection
was run. Source-note corollaries, example computations, literature claims,
and the rest of the developing manuscript are outside this formal package.

## Documentation and paper

The source result note now records the formally verified scope and the
shorter proof. The numerical-check README, review record, research log,
formal indices, and root README distinguish the verified theorem from the
unverified corollaries. The related paper's formal-verification section
states the same theorem and proof route without marking its separate
development stages complete.

These commands passed:

```sh
cd paper-quadratic-aggregation
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
cd ..
pdftotext -layout paper-quadratic-aggregation/build/main.pdf formal/topics/27-quadratic-aggregation/verification/paper-text.txt
pdfinfo paper-quadratic-aggregation/build/main.pdf
```

`latexmk` reported the updated PDF already up to date. The checked developing
paper snapshot had four pages; its extracted text includes the formal theorem,
proof, and limitations. A targeted Python scan found no LaTeX warnings,
overfull or underfull boxes, duplicate labels or bibliography keys, or missing
references or citations. The [build output](verification/paper-build.log),
[final LaTeX log](verification/paper-final.log),
[extracted PDF text](verification/paper-text.txt), and
[paper/source fingerprints](verification/paper-sources.json) preserve this
checked snapshot. This is not a complete review of the developing paper.
Concurrent manuscript development subsequently changed its main file and
PDF, deferring this formal section to the paper's stage 2 review. The saved
main-paper evidence therefore describes that earlier snapshot, not its live
draft.

To keep the verified material independently available, the paper now also
contains `formal-verification.tex`. This command passed from
`paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build formal-verification.tex
```

`pdftotext -layout` and `pdfinfo` were also run on
`build/formal-verification.pdf`. The standalone supplement has four pages,
with the theorem, shorter proof, and exclusions present in the extracted
text. A targeted scan found no LaTeX or box warnings, duplicate labels or
bibliography keys, or unresolved references or citations. See the
[supplement build log](verification/supplement-build.log),
[final LaTeX log](verification/supplement-final.log),
[PDF text](verification/supplement-text.txt), and
[source/PDF fingerprints](verification/supplement-sources.json).

Targeted Markdown link checks and `git diff --check` on the tracked files
changed for this topic passed. Independent documentation review is recorded
in [REVIEW.md](REVIEW.md). Unrelated concurrent changes were not checked or
modified by this work.
