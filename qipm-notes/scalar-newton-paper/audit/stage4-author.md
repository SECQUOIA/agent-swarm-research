# Stage 4 author report

The integrated manuscript is now a standalone 59-page paper with 40 cited
references. This stage adds synthesis and supporting build artifacts; it
does not alter any reviewed mathematical proof.

## Integration

- Added an abstract, introduction, contribution statements, a six-row
  access/error/rate table, theorem-level prior-work comparisons, and a
  reader roadmap in `sections/01-introduction.tex`.
- Organized the explanation around positive relative-form query bounds,
  scalar optimization and repeated outputs, and structured classical
  comparisons. The table and prose expressly separate lower families,
  population restrictions, the conditional composition interface, and
  the unmatched general sparse quantum bounds.
- Restricted the qualified originality claim to full-SQ positive-form
  lower bounds, explicit single-form composition/baseline calculations,
  parameterized scalar optimization/temporal realizations and reuse
  boundaries, and the sparse-full-rank correction theorem with its precise
  source-vector access. Existing polynomial/SQ primitives, Kantorovich,
  Forrelation clocks, CGJ's upper bound, cone algebra, recycling, and
  elimination are attributed. No first scalar optimization or general
  sparse dequantization claim remains.
- Added a brief convention in `02-models.tex` for C3 convex barriers with
  positive definite restricted Hessians, local/dual norms, self-concordance,
  the parameter bound, central and analytic centers, predictors, and the
  equality-restricted decrement. It makes no new theorem claim. The
  introduction explicitly distinguishes local decrement information from
  a generic global optimality certificate.
- Added a synthesis conclusion in `sections/11-conclusion.tex`, with
  limitations framed as the scope of the proved comparisons.
- Added a prior robustness citation at the beginning of the finite-error
  subsection of `03-classical.tex`. No proof or constant was changed.
- Updated the source-map coverage and literature integration records.

## Bibliography

Updated Cifuentes et al. to PRX Quantum 7,020364 (2026) and supplied Lin's
402(1),127--132 metadata. Added the current Edenhofer--Hasegawa--Le Gall
spectral-sum preprint, Le Gall's 2025 robustness article, and Zhao et al.'s
2026 adjacent streaming-space/data-sample paper. Montanaro--Shao now has
its arXiv/version locator for the full-version theorem numbering. Normalized
several existing journal fields into volume/issue/pages. Source evidence
and the one failed DOI request are recorded in `literature-review.md`.

The prior-work section compares Li--Sra--Jegelka and Bizas et al.'s full
matvec inverse-form methods; Gharibian--Le Gall's sparse polynomial overlap;
Montanaro--Shao's degree lower bound; Cifuentes et al.'s matrix-function
classification; spectral traces and approximate SQ; CGJ and Alase et al.'s
specific queried interfaces; Orsucci--Dunjko's state/stronger-access
contracts; Gronlund--Larsen's solution separation; Apers--Gribling's prior
full-SQ LP value theorem; and the established cone, low-rank SQ, recycling,
and elimination tools. The Zhao comparison imports no space lower bound.

## Standalone artifacts

`Makefile` now has `check` and `package` targets. `check` runs the five
existing diagnostics using the environment's selected Python. A small
standard-library package script bundles 24 required/supporting files,
including the PDF, TeX, bibliography and bbl, all sections, diagnostics,
Makefile, and README. It excludes the research audit. `.gitignore` omits
build logs/auxiliaries and the regenerated ZIP. The README records qipm
commands, dependencies, query/precision scope, and the diagnostic-versus-
proof distinction. No author identity or external publication was invented.

## Verification

- Forced qipm build: 59 pages, no undefined references/citations, LaTeX
  warnings, or overfull/underfull boxes in the final log.
- All five diagnostics pass: classical residual/moments/rejection;
  cyclic metadata/tilt/tree/completion; 25 Jacobi plus 25 path identities;
  temporal threshold/XOR/KKT/rank checks; 152 structured identities.
- Visually inspected the first page and the rate table. The initial
  float-only table was delayed to the end; changing its allowed placement
  puts it on page 3 within the introduction. Both render clearly.
- The submission ZIP passes its CRC check, contains 24 files and no audit
  path, and was extracted into a fresh temporary directory. A forced
  qipm build there succeeds independently, with the same 59-page output
  size and clean log. Regenerate the ZIP after subsequent corrections.

The five independent Stage 4 reviews and the separate whole-manuscript
review round remain required. This report does not replace either round.
