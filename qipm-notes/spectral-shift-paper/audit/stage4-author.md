# Stage 4 author audit

Status: complete and frozen for five independent Stage 4 reviews, 2026-09-22.
This author pass does not replace those reviews or the later five-reviewer
full-manuscript cycle. No subagents were used.

## Scope and files

Read the complete reviewed manuscript, `presentation-plan.md`, `literature.md`,
`source-map.md`, and all three prior author audits. Checked the eight source-note
claim headings against the final statements and earlier source verification.
Read the project AGENTS instructions and used the qipm environment for all
Python and builds. All writes stayed inside `spectral-shift-paper/`.

Added:

- `sections/01-introduction.tex`: independently readable motivation and model;
  precise results overview, detailed related-work comparisons, qualified
  originality statement, and proof roadmap.
- `sections/07-conclusion.tex`: significance and remaining mathematical and
  synthesis questions.
- `sections/08-reproducibility.tex`: portable reproduction and the distinction
  between floating-point diagnostics and continuous-domain proofs.
- `scripts/query_overview.py`, `figures/query-overview.pdf` and PNG/CSV outputs:
  proved unrestricted staircase and precise parity comparison on a certified
  range. Threshold equality has filled/open boundary markers. Math text uses
  embedded STIX fonts with correct searchable Unicode extraction.
- `scripts/package_source.py`, `README.md`, `submission-source.zip`.

Updated `main.tex` (abstract and new sections), `macros.tex` (graphics and PDF
metadata), `bibliography.bib` (18 cited references), `Makefile` (portable build,
figure regeneration, and source packaging), `.gitignore` (retain submission
bibliography, ignore Python cache), and the source/literature audits.
Sections 2–6 and their reviewed mathematical statements/proofs were left intact.
The existing parity table remains in the manuscript.

## Literature evidence and originality scope

The primary-source evidence and URLs are recorded in `literature.md`. In this
stage I independently inspected relevant local primary full-text passages for
Dong–Larsen–Lin–Sarkar, Orsucci–Dunjko, Laneve, and Haah, and rechecked primary
publisher/arXiv metadata for the added and corrected entries. I also read the
primary abstracts for Somma–de Wolf and Sarkar–Yoder, and the latter's HTML
introduction, Definition 1.1, and density conclusion. References based only on
broad historical evidence (Lewis, Taylor, Campos-Pinto et al.) receive only
broad comparisons; no unseen theorem is excluded by inference.

The introduction explicitly gives the following boundaries:

- Orsucci–Dunjko Section 4.3 already raises normalized I−eta A construction,
  LCU subnormalization, and generic amplification obstructions. Our result is
  a quantitative promise/accuracy law for plain-block access and does not
  resolve their distinct general sparse-value question.
- QSVT/GQSP implementation, arbitrary-parity synthesis, uniform amplification,
  trigonometric query methods, adversary/state-conversion framing, exterior
  Chebyshev, Fejer–Riesz, positive constrained approximation, sign approximation,
  generic factor benefits, and amplitude estimation are prior tools.
- Dong et al. solve a closely related prescribed-parity constrained-minimax
  design problem numerically and restore global feasibility by Fourier
  retraction. Our claims concern the analytic limiting extremizer, exact
  accuracy thresholds, all-circuit lower bounds, and proved contact-preserving
  contractive construction for this specific target and promise.
- Sarkar–Yoder's exterior-constrained density results are qualitative context;
  they are not presented as absent prior work on global constraints.
- King et al. and Somma–de Wolf are included as distinct factor/SOS simulation,
  energy, and state-preparation antecedents. Their tasks and hypotheses are
  not silently transferred to complement conversion.

The qualified originality claim concerns the exact shift thresholds,
equality-attaining constructions and optimal coherent-query exponents, the
strong even plateau and concrete separation, uniform continuum precision
bounds, and the exact-central LP realization with complete oracle contracts.
It makes no unconditional first claim. The full eight-note ledger in
`source-map.md` records retained, subsumed, corrected, and strengthened claims
with final theorem labels and numbers.

## Accuracy and interpretation safeguards

The abstract and introduction explicitly include positive K in the matched
high-accuracy regime. The overview states the c<1 versus c=1 coarse distinction,
implicit even staircase, F1=F2 plateau, concrete Theta(delta^-5/6) versus
Theta(delta^-1/2) result, odd logarithmic factor, and the residual O(r^2) gap
away from upper tier boundaries. The margin factor is retained near those
boundaries. The degree-six witness is only an upper bound for F3, never its
exact threshold. The figure uses a range where its displayed parity orders
are proved and does not plot that witness error as a transition.

The LP discussion distinguishes dual-state preparation, matrix-only reusable
compilation, and factor access; states the zero-query LP coarse exception;
and explicitly excludes an end-to-end LP/QIPM lower bound. The introduction
also states that queries are paid when applying the output conversion circuit:
reusability does not make subsequent applications free.

## Validation

Commands used include:

```sh
conda run -n qipm --live-stream make figures
conda run -n qipm --live-stream make
conda run -n qipm --live-stream make submission
```

- Both scripts completed. The overview verifies the closed G1 formula,
  monotonicity of the displayed thresholds, and the strict inequalities
  defining its parity range. G1(2)=0.0211310131443375; the degree-six witness
  error bound is 0.020011288318253, used only as a bound.
- Supplementary diagnostics reproduce the earlier threshold/asymptotic CSV
  and pinned signed errors. Sampled absolute normalized error maxima are 1;
  pin leakage is zero to working precision. These are not proof certificates.
- Final PDF: 31 pages. Final LaTeX log has no warnings, undefined references,
  duplicate labels, overfull boxes, or underfull boxes. BibTeX has no warnings.
- Independently checked 100 unique LaTeX labels and all their references;
  all 18 bibliography entries are cited, and every citation key is defined.
- Checked text extraction, including correct mathematical symbols in the
  overview figure. No TODOs, placeholders, temporary abstract, or unfinished
  prose remains in manuscript sources.
- Visually inspected the figure and representative PDF pages: title/abstract,
  figure/results, detailed related work, model/roadmap, parity table and joint
  transition, LP compiler theorem, conclusion/reproduction, and bibliography.
  Rendered artifacts are under `audit/stage4-visual/`.
- PDF title, subject, and keywords are set; author metadata is blank. No author
  identity, affiliation, or acknowledgment was invented.
- `submission-source.zip` passes its CRC check and contains 18 allowlisted
  files: source, required figure PDF, bbl/bib, README, Makefile, and scripts.
  It excludes audits, logs, literature copies, previews, and build outputs.
- Extracted the archive into a fresh temporary directory under `audit/`, ran
  its standalone LaTeX build, regenerated both figures there, and rebuilt.
  All commands passed. Extracted PDF text is identical to the workspace PDF
  text, and the extracted build log is clean. The temporary extraction was
  then removed. `audit/stage4-extract-build.log` records the run.

Reproduction environment: Python 3.12.14, NumPy 2.5.2, SciPy 1.18.0,
Matplotlib 3.11.1, pdfTeX 1.40.25/BibTeX 0.99d (TeX Live 2023/Debian).
No packages were installed. The standalone LaTeX build does not need Python.

## Remaining scope

No author-identified mathematical or packaging issue is outstanding. The
intermediate uniform multiplicative optimum, explicit higher F_r formulas,
and finite-precision synthesis costs are open scope stated in the paper, not
unfinished claims. Literature review supports the narrowly qualified novelty
statement rather than a guarantee of universal priority. Independent Stage 4
and final full-manuscript reviews remain required by the workflow.
