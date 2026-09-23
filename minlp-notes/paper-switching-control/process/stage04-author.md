# Stage 4 author report

Stage 4 is complete and ready for five independent reviews. All author writes
are now stopped. The new mathematical material is in sections 08 and 09 (printed
Sections 11 and 12, pages 32–40 of the current 40-page PDF).

## Work completed

`08-finite-grid-one-switch.tex` comprehensively develops the repository's
arbitrary-grid one-switch minimax theorem. It includes both closed LP families,
constant-schedule dominance, strict-level coverage and compact limits, explicit
T/3 boundary feasibility, two-large-mode elimination, stronger averaging of the
other modes, every surviving elimination condition, exact rational extremizer
reconstruction and complexity. The three-mode unit-grid residue theorem is
proved directly with all endpoint cases and witnesses. The five-mode, nine-cell value 17/5
example has a short analytic proof independent of LP software. The failed
nonuniform simplification and its exact rational values are retained.

`09-three-mode-floor-chambers.tex` develops a complete three-state description
of strict three-mode floor histories for arbitrary N. Its realization proof uses
incoming/outgoing coverage and averages of full integer paths; no feasibility
LP is required. The switch-count recursion tracks count node and last mode.
The original exact five-cell theorem is proved with this smaller enumeration,
with two unchanged historical enumerations retained for independent coverage.
The theorem plus the accepted cell-averaging comparison closes the continuous
boundary F_{3,2}(T)=T/5. The source already supplies its lower bound, which is
credited precisely; an alternative pure witness is proved directly.

Further development from root research, independently checked here, establishes
F_grid(3,N6,s3)=1 and F_grid(3,N7,s3)=4/3 on unit cells. There are 8,856 strict
seven-cell histories; only six need four switches for error below one. They are
exactly the permutations of the explicit printed floor history. Three explicit
three-switch repair words each have only one exceptional prefix coordinate;
monotonicity makes their three exceptional allocations sum to at most4. This
proves the 4/3 minimax upper. A simple input with two uniform cells and five pure
cells attains4/3, verified through both the complete nine-entry DP table and all
2187 words. This resolves the natural 2s+1-cell unit-error extension negatively
at s=3. The continuous consequences are accurately stated as T/7<=F_{3,3}<=T/6;
the cited lower is independently justified by an activation-count argument.
No theorem assumes an exact continuous n3/s3 value or an arbitrary-budget
unit-error extension.

The published Corollary 5 correction is checked against the final 49-page
Sager–Zeile PDF, downloaded directly from the publisher. Printed p.610 contains
the restricted attainment argument, p.611 the unqualified lower bound, and
p.612 Proposition 4's separate continuous lower bound. The author recorded the
source URL, institutional mirror, PDF SHA-256 and exact locators in
`verification/stage04/source-record.md`. No source original is redistributed.

## Verification completed

- All accepted sections 01–07, macros and references.bib match the
  stage03-accepted snapshot byte for byte. Original repository files and frozen
  snapshots were not changed.
- Six historical scripts were bundled unchanged. The manifest now verifies 25
  original artifacts; all hashes pass.
- New exact formula checker: 172 expanded rational extremizers, each checked
  by enumerating every one-switch schedule using original absolute cumulative
  discrepancies. Additional scaling checks, all three-mode residues through
  N12, the failed nonuniform formula, n5/N9, and very large rational inputs pass.
- New floor checker: complete distributions through N=7; incoming/outgoing graph
  coverage, no duplicate histories, exceptional-orbit equality, all repair-word
  exceptions, exact seven-cell instance optimum, five/six-cell lower witnesses,
  and the continuous two-switch witness all pass.
- Historical five-cell author enumeration and independent flat14400-history
  enumeration both pass.
- Optional full-control LP audit: 33 comparisons pass, each witness additionally
  checked in exact original-error arithmetic.
- Optional compressed LP audit: 99 further rational-certified comparisons pass;
  the independent full-control LP values are numerical corroboration. 24 extreme
  arithmetic cases, 100 random-control error comparisons, all input validation,
  and the documented region audit pass.
- All six checks were run via `run_checks.py --with-lp-audits`; stable outputs
  are stored in `verification/stage04/check-summary.json`.
- A clean relocated copy at `/tmp/switching-stage04-portable-8tj7vjum` built
  successfully and passed the standard-library suite under `python -S`, proving
  the documented checks do not depend on the repository import path or installed
  third-party modules. Reproduction commands and exact/optional distinctions
  are documented in `verification/stage04/README.md`.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeds.
  The final main.log has no undefined references/citations, overfull or underfull
  boxes, or warnings. The current PDF is 40 pages. I visually inspected every
  affected page32–40; displays, tables, headings and the bibliography fit.

## Review focus and remaining scope

Review the exact region coverage/elimination, repeated or constant schedules,
all-N floor-history realization, exhaustive seven-cell coverage, three repair
words and their common4/3 bound, continuous/grid quantifiers, and primary-source
scope particularly carefully. New theorems use only printed arguments and the
new exact checker, with original enumerations as separate corroboration.

Stage 5 still owns instance algorithms, dwell constraints, sharp grid transfer,
and certified coarsening. Stage 6 owns the full bibliography, introduction,
abstract, experiments and overall coverage synthesis. The general continuous
three-switch boundary remains a clearly stated interval, not a completed exact
minimax theorem; no claimed result depends on closing that interval.
