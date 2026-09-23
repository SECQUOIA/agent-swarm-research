# Stage 1 author report

Completed 2026-09-22. Scope: source inventory, literature evidence, notation,
the original conjecture and background, plus a standalone LaTeX scaffold.
No main proof or consequences section has been written at this stage.

## Files

- `main.tex`, `macros.tex`, `sections/01-setting.tex`: three-page preliminary
  document with explicit open-system convention, ordinary hull, multiplier
  cone including zero, HHC, conjecture, and distinction from good aggregations.
- `references.bib`: verified core bibliographic metadata plus entries needed
  by later stages. Unused entries are not printed by the current build.
- `process/coverage.md`: complete canonical-topic coverage and dispositions.
- `process/literature.md`: exact-version source locators, search scope, source
  hashes, bibliographic corrections, access limitations and later-stage checks.

## Main source findings

The conjecture is unchanged in BDS arXiv v2, but most background theorem
numbers differ from the local 2022 author manuscript. All manuscript
numbered citations explicitly refer to v2. Blekherman–Dunbar is a 2025
published paper, not merely a 2024 preprint. The Nguyen–Chu–Sheu 2025
arXiv upload identifies a 2022 journal publication. No subsequent resolution
was found in a targeted search; this does not establish priority.

The main prospective new result is the resolution of the all-trivial
multiplier case and the weakening of its convexity hypothesis. The
two-quadratic case, diagonal case, and elementary cone separation are
explicitly credited as established material.

The coordinator's primary-PDF inspection of Kojima–Tunçel identified a
problem with relying on its universal exact-equality statement. This is
documented in the literature record and must be resolved by the independent
argument and examples in stage 3. Stage 1 does not state that equality.
Polyak and Sheriff exact source followups also belong to stage 3; no
roundness theorem is imported at this stage. Publisher text unavailable
for BDS/BD is handled by explicit arXiv version locators.

## Targeted checks actually run

From `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
rg -n 'Warning|Overfull|Underfull|undefined' build/main.log
```

Build passed: `build/main.pdf`, three pages. Final log search found no
warnings, overfull/underfull boxes, or undefined references/citations.
Initial-pass citation warnings disappeared after automatic BibTeX and reruns.
No numerical experiments were rerun; no project-wide verification or CI
inspection was performed. A Python metadata helper initially attempted
unavailable BeautifulSoup; it was replaced with a standard-library parser
without installing anything. AMS and Harvard PDF HTTP failures are recorded
as access limits, not represented as successful full-text retrievals.

Stage 1 awaits the coordinator's five independent reviews.
