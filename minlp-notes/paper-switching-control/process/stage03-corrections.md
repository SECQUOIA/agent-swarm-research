# Stage 3 corrections after round 1

The correction agent read the adjudication and reports 02–04 and fixed all
three valid minor findings. There is no new mathematical result or change to
the chamber LP, its objective, or its exact bound.

## Corrections

1. **R02-01, internal process language.** Replaced “accepted small-budget
   theorems” in `sections/07-predecessors-and-frontier.tex` by an explicit
   reference to `thm:small-full`.
2. **R03-S3-01, deterministic certificate row indexing.** Added
   `verification/stage03/chronological_program.py`, shared by the exact
   checker and optional discovery. It reconstructs the historical rows,
   appends the same chronological rows, removes explicit zero coefficients,
   and sorts inequalities and equalities separately by the exact key
   `(tuple(sorted((column, coefficient) for nonzero coefficients)), rhs)`.
   Duplicate rows are retained. The variable coordinates, event permutation,
   row multisets, and objective remain unchanged. The manuscript describes
   canonical sorting; the verification README states its exact key.

   Permuted the existing exact inequality and equality dual vectors into
   this canonical order. No numerical rediscovery was performed. Checked
   that each dual's weighted coefficient vector and weighted right-hand
   side are exactly unchanged. The saved primal and event permutation were
   not changed. The resulting certificate still has 254 nonzero dual rows
   and proves the exact bound `13104/125` on the same 454-variable LP with
   4,038 inequalities and 64 equalities.

   The checker now separates exact primal/dual validation from reconstruction
   and runs a regression audit using reversed and deterministically shuffled
   historical inequality and equality rows. Both inputs also reverse sparse
   dictionary insertion order and insert explicit zero coefficients. Each
   reconstruction must equal the canonical program, and the same saved
   indexed dual is validated against it without permutation. This directly
   exercises the unspecified-traversal issue raised by the reviewer. In
   general, lexicographic sorting of the normalized row multiset yields
   the same ordered list under any input permutation; duplicate rows have
   identical coefficients and right-hand sides.

   The historical `verification/reference/general_reach_research.py` was
   not edited. Its bytes and recorded hash, and those of all 19 original
   bundled artifacts, remain unchanged. Optional discovery uses the same
   canonical constructor; it was compiled but not executed, preserving the
   supplied rational certificate rather than replacing it with a solver
   candidate.
3. **R04-01, build-log availability.** The stage 3 verification README now
   identifies `build.log` and `final-build.log` as working-directory outputs
   excluded from frozen snapshots. It includes the manuscript-root build
   command and identifies the archived text, page images, and contact
   sheets as stage 3 round 1 layout evidence. Those artifacts are retained
   unchanged and are not presented as renders of this correction.

## Checks

- Exact chronological checker passed, including the original witness,
  canonical primal/dual certificate, and both input-row permutation audits.
  It still records 239 chronological decreases, largest decrease `224/645`,
  and optimum `13104/125` with the matching uniform primal.
- Full stage 3 runner passed all eight checks with standard-library Python
  and bundled dependencies.
- Clean rebuild with
  `latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex` passed.
  The manuscript has 32 pages. The final LaTeX log contains no warnings,
  undefined references, or overfull/underfull boxes.
- All three changed Python modules compiled successfully. Optional numerical
  discovery was not run.
- `git diff --check -- paper-switching-control` passed.
- All 71 original stage 3 round 1 snapshot hashes still match. All 19 bundled
  original artifact hashes still match. No snapshot, reviewer report, or
  original research source was edited.

Working-directory evidence is under `verification/stage03/` with prefix
`corrections-`: `dual-permutation.log`, `chronological.log`, `all-checks.log`,
`build.log`, and `integrity.log`. As documented, these logs are excluded by
the existing snapshot helper; the reproducible checkers and certificate are
included.

All assigned corrections are complete. Ready for the primary agent's final
inspection and acceptance. The correction agent created no snapshot and
records no stage acceptance here.
