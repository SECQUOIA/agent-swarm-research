# Manuscript development and review

Requested deliverable: a standalone journal manuscript on unit-normalized
spectral shifts, with verified results and a careful literature comparison.

Each stage uses a separate author, five independent reviewers, root assessment,
and a separate fixer for all accepted findings. A finding judged major triggers
another five-reviewer round after correction. Accepted minor findings are fixed
before the next stage. The full manuscript receives the same final cycle.

## Stages

1. Oracle contracts, exact two-point conversion, interval conversion, constrained
   approximation, arbitrary-circuit lower bounds, and fixed-accuracy staircase.
2. Joint gap--accuracy bounds, an independent lower-bound route, uniform
   growing-degree construction, and quantitative verification artifacts.
3. Sparse LP Newton realization, matrix/factor access separation, bypasses,
   robustness and computational scope.
4. Introduction, literature synthesis, statement of contributions, source
   completeness, conclusion, figures, and submission packaging.
5. Independent whole-manuscript review and final corrections.

## Status

- Stage 1: complete. Five round-1 reviews found no major issues; all accepted
  minor issues were repaired by a separate fixer and checked by root. Clean build.
- Stage 2: complete. Five round-1 reviews found zero major issues. The one
  accepted minor quantifier correction was repaired separately and checked.
- Stage 3: complete. Five independent reviews found zero major or minor issues.
- Stage 4: complete. Five independent reviews found zero major or minor
  issues; root assessed all reports and verified the frozen artifact hashes.
- Stage 5: complete. All five fresh whole-manuscript reviews found zero
  major issues. Three identified the same minor literature omission;
  a separate fixer repaired it, and root verified the exact changes,
  bibliography, layout, final build logs, and source archive.

Final deliverables: `main.pdf` (31 pages), `submission-source.zip`
(18 portable source files), and `README.md`. The bibliography has 19
cited entries. All accepted findings are closed; the final artifact checks
are recorded in `final-verification.md` and `final-freeze.sha256`.

Internal review is evidence of checking, not journal acceptance or a guarantee
that future readers will find no errors. Mathematical limitations must remain
explicit in the submitted manuscript.
