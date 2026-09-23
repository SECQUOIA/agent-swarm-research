# Stage 1 corrections

Correction agent: `correction_agent`, distinct from the stage author and all
five reviewers. Date: 2026-09-07. Authority: the accepted changes in
`process/assessments/stage01-round01.md`.

All five accepted issues and the accepted approximation-literature clarification
are fixed. No accepted issue remains unresolved. Stage acceptance remains the
root's decision; this correction does not begin stage 2.

## Changes and verification

Locations refer to the corrected live source.

| Issue | Exact change | Verification |
| --- | --- | --- |
| S1-1 | `sections/01-foundations.tex:198–204` restricts the infeasibility and attainment promise to exact algorithms. Approximation guarantees remain theorem-specific, and the paragraph distinguishes original infeasibility, relaxed output, and empty inner surrogates. | Compared with Theorems 1 and 2 in `results/bilevel-response-constraint-accuracy-bit-algorithm.md`. An outer output need not certify original feasibility, and inner emptiness need not certify original infeasibility. The revised text preserves both distinctions. |
| S1-2 | `sections/01-foundations.tex:224–227` bounds output degree, coefficient lengths, and combined coordinate encoding polynomially in `(L,delta)`, with a bound polynomial in `L` only under the preceding degree-encoding condition. | Compared with the runtime convention at lines 208–218 and the sparse-exponent example in Section 6 of `results/bilevel-fixed-aggregate-response-algorithm.md`. The degree `2^t` example is no longer covered by an unconditional polynomial-in-`L` output promise. |
| S1-3 | `sections/01-foundations.tex:24–27` explicitly describes the classical fixed-follower-dimension positive results as optimistic. | Checked that the qualifier directly governs the Liu–Spencer attribution and does not depend on the later warning about pessimistic conventions. This is the local qualification accepted from reviewers 02 and 05; no theorem number or historical attribution was changed. |
| S1-4 | `sections/01-foundations.tex:92–93` requires every polynomial datum in the model to be supplied explicitly with rational coefficients; lines 118–120 declare `c_b(x)` as a rational polynomial vector in `Q[x]^{d_b}`. | Inspected the complete model declaration. The local linear term now has an explicit domain and representation, and the shared declaration also covers right-hand sides, quadratic matrices, aggregate data, and polynomial upper data. |
| S1-5 | `process/coverage.md:23–28` adds zero and negative local curvature to stage 5; the new row at line 53 assigns both elementary 3SAT examples explicitly. | Compared with Section 6 of `results/bilevel-fixed-aggregate-response-algorithm.md`. The zero-cost example retains quadratic upper Boolean equations plus linear clauses; the negative-quadratic example retains linear upper clauses alone. The row expressly excludes a novelty claim. |
| Accepted literature clarification | `sections/01-foundations.tex:59–69` distinguishes Hochbaum–Shanthikumar's logarithmic accuracy dependence under their oracle and matrix assumptions from Vigneron's inverse-relative-error schemes for nonnegative algebraic functions of constant description complexity. | Read the relevant primary source passages listed below and checked key original PDF pages. Both existing bibliography entries cite the primary papers; no bibliography change or additional proof dependency was needed. |

## Literature basis and access

I read `../literature/AGENTS.md` before consulting the literature collection.
The clarification is based on
`[[hochbaum1990-convex-separable-optimization-is-not]] p.2-4` and
`[[vigneron2014-geometric-optimization-and-sums-of]] p.1-3`.
I visually checked Hochbaum–Shanthikumar's original PDF page 4, including the
resource-allocation accuracy statement and computational model, and Vigneron's
original PDF page 3, including the inverse-relative-error level count.
The local Vigneron original is the author manuscript used by reviewer 02, rather
than the final typeset article. The clarification uses the explicit scope of
that manuscript. No literature package was changed, and no external review is
used as a mathematical citation in the added manuscript text.

## Build and source checks

The live paper was rebuilt from scratch with:

```sh
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The command exited successfully and produced the six-page `build/main.pdf`.
The final log has no LaTeX warnings, undefined citations or references, overfull
or underfull boxes, or fatal errors. I inspected rendered pages 2 and 4, which
contain the revised literature, model, and output passages; they are legible
and have no clipping or overlapping material.

I inspected the complete source diff against `process/snapshots/stage01-round01`.
Of the five manifest-listed live files, only `sections/01-foundations.tex` and
`process/coverage.md` changed, as authorized. `main.tex`, `references.bib`, and
`README.md` remain byte-identical to the snapshot. Every frozen file still
matches its recorded hash, and the manifest's SHA-256 remains
`2230f1e9da9d015278c6bbf424d04167961f6c7911646ca287e899b9ccae36de`.
No frozen snapshot, root assessment, or `STATUS.md` was edited.

Evidence is under `verification/correction-agent/stage01/`:

- `build-command.log`: complete clean-build transcript.
- `final-main.log`: final LaTeX log.
- `source.diff`: complete changes to manifest-listed source files.
- `checks.json`: snapshot integrity, changed-file list, and final diagnostics.
- `corrected-p2.png` and `corrected-p4.png`: inspected manuscript pages.
- `hochbaum-p4.png` and `vigneron-p3.png`: inspected primary-source pages.

Remaining accepted issues: **none**. Later-stage proof obligations retain their
existing assignments and are not certified by this correction.
