# Stage 1, round 1: independent review 05

Reviewer: reviewer05. Date: 2026-09-07.

## Reviewed snapshot and scope

Frozen source: `process/snapshots/stage01-round01/`.
SHA-256 of its `SHA256.json`:
`2230f1e9da9d015278c6bbf424d04167961f6c7911646ca287e899b9ccae36de`.
I independently checked that all five source files match their manifest hashes.
Locations below refer to that snapshot, not subsequent live edits.

I read all of `main.tex`, `sections/01-foundations.tex`, `references.bib`,
`README.md`, and `process/coverage.md`. I compiled only a private snapshot copy
under `verification/reviewer05/stage01-round01/`. I did not read the other
current reviewers' reports, coordinate findings, edit the manuscript, or delegate.

The stage is sound overall. I found no major issue and two minor corrections.
Later theorem proofs, the final abstract, and the integrated contribution table
are expressly scheduled for later stages and are not omissions from this review
gate.

## Major findings

None found in the stage 1 material.

## Minor findings requiring correction

### R05-01: Identify the optimistic convention in the classical positive comparison

Location: `sections/01-foundations.tex`, lines 24–27; related qualification at
lines 35–45.

The opening comparison says that Liu–Spencer give a polynomial algorithm when
the follower dimension is fixed, without identifying the response convention.
This paper subsequently treats both optimistic and universally feasible
pessimistic models, so the omitted qualifier leaves a substantive ambiguity.
The later sentence that conventions matter does not tell the reader which
convention applies to the classical positive claim.

Evidence: Ketkov–Prokopyev explicitly distinguish polynomial solvability in the
optimistic fixed-follower-variable case from strong NP-hardness in the
pessimistic case with coupling constraints. Their discussion also warns that
Deng's pessimistic formulation was not explicitly defined. See
`[[ketkov2026-on-the-complexity-of-bilevel]] p.4`, Table 1 and the paragraph
discussing Deng; I checked that page against the original PDF. Their Theorem 1,
`p.8`, states the positive result for the optimistic problem. The repository's
`notes/bilevel-classical-positioning.md`, subsection “Optimistic and pessimistic
historical statements need explicit conventions,” makes the same distinction.

Requested fix: say “optimistic linear bilevel optimization” in the first
positive-result sentence, or otherwise attach “under optimistic selection”
directly to the Liu–Spencer claim. No additional historical proof is needed.

### R05-02: Declare the linear local-cost data as rational polynomials

Location: `sections/01-foundations.tex`, lines 103–118, especially the introduction
of `c_b(x)` in equation (3); encoding discussion at lines 195–205.

The model introduces `c_b(x)` inside the follower objective but never states
that it is a polynomial vector, nor gives its coefficient domain. In contrast,
the text explicitly calls `Q_b`, `U`, and `phi` polynomial. The rational bit-model
discussion makes the intended restriction inferable, but it should be part of
the actual model specification: polynomial response elimination requires it.
The right-hand sides and `Q_b`, `phi` would also benefit from one shared rational
coefficient declaration rather than leaving that restriction to inference.

Evidence: the canonical block theorem, `results/bilevel-fixed-block-response-algorithm.md`,
“Statement,” requires all data to have the scalar theorem's explicit polynomial
representation; its local effective cost contains `c_b(x)` and must be
polynomial before the local rational formulas and sign tests are constructed.

Requested fix: declare `c_b(x) in Q[x]^{d_b}` and state once that every polynomial
datum in the primary model is explicitly supplied with rational coefficients.
This is a specification clarification, not a request to expand the model.

## Mathematical and coverage checks

- The bounded-coordinate premise and compact leader domain give uniform
  follower boundedness. For each feasible leader, the polynomial objective
  attains its minimum; the optimal-response set is compact. The fixed-leader
  pessimistic maximum therefore exists. The text correctly distinguishes this
  from leader attainment and excludes empty follower fibers from universal
  feasibility.
- The optimistic definition applies upper rows only after follower optimization.
  The pessimistic definition quantifies those rows over all follower optima.
  Near-optimal responses use the nominal global value and need not be stationary.
  The separate measurement restriction for robust compression is retained.
- Lemma 1.1 is correct: the denominator exponent is nonnegative because
  `|gamma| <= delta`; its stated degree bound is valid; the fixed number of
  target variables bounds the expanded monomial count polynomially. Products
  and sums have polynomial coefficient bit length in the stated numerical
  degree and encoding parameters. Positivity of the denominator preserves signs.
- The numerical-degree versus sparse-binary-exponent distinction is explicit.
  The common-field definition controls combined coordinate output and correctly
  avoids promising one polynomial-degree field for unrelated adversarial
  witnesses. Accuracy-bit output is tied to the true induced objective, not an
  approximate follower substituted without justification. XP and FPT are
  distinguished correctly.
- The cited fixed-dimensional algebraic tools support the statements used here.
  I checked Basu–Pollack–Roy's Theorem 1.3.1 and bit-size discussion,
  `[[basu1996-on-the-combinatorial-and-algebraic]] p.3-4`, and the sample-points
  construction and encoding discussion, `p.27-28`. The theorem and sample-output
  formulas were also checked against original PDF pages 4 and 27. Fixing the
  total free and bound dimension is essential and is expressly required here.
- Hoffman's statement correctly requires a nonempty polyhedron, allows equality
  rows via paired inequalities, and keeps the uniformity in right-hand sides
  separate from varying normals and quantitative encoding bounds.
- I compared the inventory with the canonical bilevel result list and the paper
  scope, response complexity map, continuation status/closeout, nonconvex
  closeout, and relevant broad closeout dispositions. All canonical bilevel
  result families are assigned. The inventory also retains the note-only low-rank
  corollary, moving normals, positive and signed inverse dependencies, arithmetic
  obstructions, growing-leader boundaries, both distinct path constructions,
  affine-strip feasibility result, and original-objective contact reconstruction.
  I found no concrete missing development. The proposed continuous-leader
  baseline is clearly future work for stage 6, not claimed existing evidence.

## Build, PDF, references, and limits

The README build command succeeded from the isolated copy:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The resulting `build/main.pdf` has six pages. The final LaTeX log contains no
warnings, undefined citations/references, or overfull/underfull box reports.
I rendered and visually inspected all six pages; equations, accents, references,
and page transitions are readable, with no clipped material or overlapping text.
The final reference list contains all 13 cited entries. Early compilation passes
had expected unresolved citations, which disappeared on completion. Build logs,
PDF, extracted text, and rendered page images remain in the private verification
folder. A first attempt to render with Python failed because `fitz` was absent;
the successful PDF rendering and extraction used `pdftoppm` and `pdftotext`.

I inspected the relevant primary text for Ketkov–Prokopyev,
Sugishita–Carvalho, Basu–Pollack–Roy, and Hochbaum–Shanthikumar, and compared the
remaining related-work claims with the repository's source-positioning records.
The Sugishita–Carvalho single-leader, unit-cube, no-extra-upper-row statement is
supported by `[[sugishita2026-complexity-of-bilevel-linear-programming]] p.1-3`.
Hochbaum–Shanthikumar explicitly discuss logarithmic accuracy dependence for
separable resource allocation; the manuscript does not incorrectly identify
that as a new ingredient. I did not independently retrieve the unavailable
Liu–Spencer or Deng originals, re-prove all cited literature results, or audit
every proof assigned to later stages. This is a full review of the current
stage and its inventory, not certification of unwritten stages.

## Optional suggestions

At the synthesis stage, a short scalar tariff example could give optimization
readers a concrete instance before the full block notation. This is an
expository suggestion only; the present foundations are intelligible without it.
