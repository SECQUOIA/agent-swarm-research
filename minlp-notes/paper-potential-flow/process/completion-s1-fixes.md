# Completion S1 corrections and verification

Completed 2026-09-10 by the separate correction author, after reading the lead adjudication and independent reviewer 3 and 4 reports.

## S1-C1: align the sampling guarantee with the cited source

In `complexity/sections/01-preliminaries.tex`, `prim:a-pre-sample-points` now guarantees a finite set of samples meeting every semialgebraically connected component of every realizable sign condition of the input polynomials. This replaces the unsupported description in terms of decomposition cells. The polynomial bit complexity for fixed dimension, polynomial degrees and encoding lengths, common real univariate representation, and existing Chapter 12–13 references are unchanged.

I checked all four explicit invocations. The cactus argument needs a feasible sample from a univariate formula. The block-rank arguments need a feasible active core at a retained threshold, an optimal core/value pair after quantifier elimination, and the corresponding fixed-dimension sampling complexity bound. Each formula is constant on each sign condition of its input polynomials, so the corrected guarantee supplies the required sample whenever the formula defines a nonempty set. All coordinates still share one real algebraic field. The nearby summary of sample-point calls and the same-field leaf recovery remain consistent. No invocation needs a decomposition-cell construction or a downstream edit.

## Verification

From `paper-potential-flow/complexity/`, ran:

```text
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The command exited successfully and produced a 50-page Paper A PDF. The final LaTeX log has no errors, undefined references, undefined citations, duplicate labels, or overfull boxes. I used the existing build checker's diagnostic function to refresh `process/completion-s1-build.json` without changing its schema. Its input hashes cover all Paper A TeX and BibTeX sources; only `01-preliminaries.tex` changed relative to the previous stage build evidence.

This correction changes source wording only, so numerical regression suites were not rerun. Paper B was neither edited nor rebuilt. No commit was created. The accepted finding was minor; the adjudication requires no repeat review round.
