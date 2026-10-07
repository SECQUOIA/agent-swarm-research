# Editorial and integration review

Status: complete. The final source, PDF, and local literature audit have been
reviewed for the abstract, introduction, Sections 2–9, and Appendices A–F.
All required editorial findings are resolved. No editorial or integration
blocker remains.
The bibliography has been checked for citation-key coverage. Sources were
being integrated during this review, so labels identify locations more
reliably than line numbers.
No manuscript sources were edited. No literature searches or optimization
experiments were run.

The draft has a coherent central question and preserves the distinctions
between unrestricted sets, restricted families, completion, fixed-corner
closure, reoptimization, convergence, and solver performance. The introduction
scopes novelty carefully. The mathematical and numerical conclusions are
distinguished accurately. The notation, development-history passages, and
empirical definitions raised below have been corrected. The
proof-duplication suggestion is advisory.

## Findings requiring disposition

### E1 — Medium: preserve the established meaning of cut coefficients

- Location: `sections/04-depth.tex`, `dp:cylinder-step`, lines 83–89 and
  subsequent depth and fixed-rule proofs.
- Evidence: Section 2 defines `a_j(C)=1/alpha_j(C)` as the cut coefficient.
  Section 4 then uses `a_j` for the normalized first-order coefficient of the
  ray restriction. Both meanings recur in the paper.
- Minimal change: use `ell_j` for the normalized first-order coefficient
  throughout the depth calculations, keeping `a_j(C)` for cut coefficients.

### E2 — Medium: matrix parameters reuse the feasible-set symbol

- Location: `sections/04-depth.tex`, `dp:contact-approx` and
  `dp:contact-intervals`, lines 399–458; `appendices/B-depth.tex`, from line 5
  onward; `appendices/C-closures.tex`, lines 5–9.
- Evidence: Section 2 reserves `X` for the feasible ray-coordinate set.
  Section 4 and Appendix B use `X` for `F^T`; Appendix C explicitly says it
  avoids that reuse and calls an apex-normalized matrix `Xi`.
- Minimal change: consistently call the raw matrix parameter `G=F^T` in the
  contact and depth proofs. Keep `Xi=F^T M(sbar)` for the distinct normalized
  parameter in the closure certificates. Remove the implementation-history
  explanation in Appendix C and start with the definitions.

### E3 — Medium: clarify the multiple-testing family and empirical policies

- Location: `sections/08-computation.tex`, `exp:multiround`, lines 172–187;
  `appendices/F-evidence.tex`, `exp:policy-details`, originally lines 196–213.
- Evidence: the main text says “14-test family”, while the appendix says
  “14-rule Holm family” and reports both round-10 and trajectory-area
  endpoints. The adjustment family cannot be reconstructed from that wording.
  “Continued-orbit recovery” in the main text differs from the appendix's
  switching-after-three-orbit-rounds description. The destination rule and
  recovery statistic are not defined. The efficacy and majority-ray rules
  are named without enough detail to identify the comparisons.
- Minimal change: give one short operational definition for each cited policy,
  the trajectory-area and recovery statistics, the destination of the switch,
  and the exact adjustment family for each endpoint. If retained records do
  not establish a definition, remove the corresponding inferential sentence
  and retain the numerical record in the companion.

### E4 — Medium: replace one causal-sounding numerical inference

- Location: `sections/08-computation.tex`, `exp:multiround`, lines 172–180.
- Evidence: “early choices create states from which subsequent progress is
  harder” reads as a causal mechanism, while the paragraph concludes that
  these observations do not identify one.
- Minimal change: state the observation: “The deficit persists when later
  rounds use the same SCIP-model rule.” Retain the qualification that the
  compared interventions do not hold exposure constant and do not identify
  a mechanism.

### E5 — Medium: give survey rows paper-facing names and data definitions

- Location: `appendices/C-closures.tex`, `cl:survey`, lines 583–593;
  `cl:numerical-records`, lines 604–639.
- Evidence: rows and prose use old note identifiers such as `thm14`,
  `prop16`, `adv8_1`, and `supp1_5512`. Several corners are otherwise
  undefined in the manuscript. This assumes readers know the source notes.
- Minimal change: use theorem references or descriptive names for corners
  defined in the paper. Give neutral numerical-example names for the others,
  with their exact input-data location defined in the companion. Preserve the
  old identifiers only in the companion mapping. The 17-of-18 observation
  should explicitly distinguish comparisons from distinct instances.

### E6 — Low: retain alternative mathematics without revision-history labels

- Location: `appendices/B-depth.tex`, `dp:dual-depth`, lines 267–276;
  `sections/01-introduction.tex`, lines 51–58.
- Evidence: “superseded orbit upper bound”, “author draft”, and “uncorrected
  version” frame substantive mathematical comparisons as revision history.
- Minimal change: rename the appendix subsection “A dual certificate for an
  orbit upper bound” and describe it as an alternative weaker bound. In the
  introduction, state the precise hypothesis difference or describe the
  version in the bibliography; omit “uncorrected” unless a specific published
  mathematical error and its correction are stated.

### E7 — Low: trim duplication between a conceptual proof and its full proof

- Location: `sections/04-depth.tex`, `dp:contact-approx`, lines 398–418 and
  `dp:contact-intervals`, lines 444–458; `appendices/B-depth.tex`,
  `dp:contact-proof`, lines 411–490.
- Evidence: the main text and appendix both give the kernel argument,
  perturbation, and both singular-limit cases. The appendix's Schur-complement
  detail adds confidence, but much of the algebra is repeated.
- Minimal change: retain the conceptual perturbation and finite-vertex
  argument in the main proof, and refer to the appendix for the kernel and
  singular-limit algebra. Keep the complete detailed proof in the appendix.

### E8 — Low: repair malformed prose and two missing macro escapes

- Location: `sections/02-corners.tex`, `fd:inertia`, line 176;
  `sections/03-quadratic-geometry.tex`, `fd:pencil`, line 209;
  `appendices/F-evidence.tex`, current lines 315, 368–393, 408–436.
- Evidence: the formula contains literal `-mathbf1`; the pencil condition
  contains literal `,quad`. The evidence appendix contains `near56.7`,
  `reports170`, `All73`, `on25`, `and60`, `with37,936`, and similar joins.
- Minimal change: restore `\\mathbf1` and `\\quad` and add ordinary spaces in
  prose. Check the rendered PDF after those fixes.

### E9 — Low: avoid local reuse of the prominent depth symbol

- Location: `sections/02-corners.tex`, `fd:two-ray`, lines 240–251;
  `sections/06-minors.tex`, `mi:support` and `mi:pencil`, lines 141–159;
  corresponding Appendix D calculations.
- Evidence: `D` denotes a discriminant, an edge-direction matrix, and the
  scaled vertex-depth measure. The contexts are local, but the shared
  notation contract reserves unadorned `D` for depth.
- Minimal change: use `Delta(theta)` for the discriminant and an edge symbol
  such as `H` or `D_edge` for the minor direction.

### E10 — Low: specify the numerical objective used in the reported ratios

- Location: `sections/08-computation.tex`, `exp:fidelity`, lines 35–42.
- Evidence: the passage mentions reduced-space tests and floored costs, then
  writes the theoretical `z_C/z_K` ratio. It does not explicitly identify
  whether both numerical values use the same floored vector and projected
  cone. The numerical label is otherwise clear.
- Minimal change: state the cost vector and cone used for both numerator and
  denominator, or label the displayed quantity as the surrogate ratio.

### E11 — Medium: restore the intended integer counts after spacing cleanup

- Location: `appendices/F-evidence.tex`, `exp:companion`, current lines
  429–435 and 449–450; `exp:debug`, current line 406. Visible in the first
  integrated PDF on pages 76–82.
- Evidence: the prose cleanup changed thousands separators to `11, 132`,
  `1, 882`, `28, 699`, `114, 699`, `37, 936`, and `171, 528`. The certificate
  count list now reads `3, 255, 38, 10, 323, 426, 7, 061`, obscuring the
  distinction between an integer and adjacent list entries.
- Minimal change: restore the grouping inside integers and separate lists
  with semicolons where useful. Do not globally collapse every
  digit-comma-space-digit pattern: some such patterns are legitimate
  seed-wise triples or lists of separate counts.

### E12 — Medium: define the minor-selection policies

- Location: `sections/08-computation.tex`, `exp:one-cut`, lines 126–128.
- Evidence: “maximum-margin” and “nearest SCIP” are compared without their
  objectives or normalization. The archived `minor_core.py` and `exp_lp.py`
  identify distinct common-eigenvalue-margin and Frobenius-distance searches
  in the apex-identity frame.
- Minimal change: give those operational definitions in `exp:minor-diagnostics`,
  including the bound-attaining target used by the comparison.

### E13 — Low: preserve an exact benchmark identifier

- Location: `appendices/F-evidence.tex`, `exp:corner-oracles`, line 149.
- Evidence: the identifier reads `waterund 25`, while the retained records
  and author report use `waterund25`.
- Minimal change: restore `waterund25` inside the text macro.

### E14 — Low: remove duplicated reference names

- Location: `appendices/B-depth.tex`, `dp:completion-membership` proof,
  line 28, and the fixed-rule derivation, line 355.
- Evidence: `Equation` followed by `cref` renders “Equation equation (26)”
  on pages 51 and 56.
- Minimal change: use `Cref` alone in both sentences.

## Optional polishing

- The abstract's evidence-management sentence was removed; its final
  computational statement now gives the substantive comparison result.
- “Linear matrix inequalities (LMIs)” is now expanded on first use in
  `fd:orbit-sdp`. Defining “radical” as the kernel of the homogeneous form
  on its first use in `fd:lorentz` remains optional for readers unfamiliar
  with quadratic-form terminology.
- Near-boundary calibration and its reproducibility limitation are repeated
  in Appendix B (`dp:calibration`) and Appendix F. One complete account in
  Appendix F with a short cross-reference from B would be clearer.

## Checks performed

- Read `AGENTS.md`, `evidence/BRIEF.md`, and `evidence/AUTHOR-CONTRACT.md`.
- Read the actual main sections and Appendices B–F, including the certificate
  descriptions and numerical qualifications. Mathematical certification is
  being independently reviewed by the separate mathematics reviewers.
- Ran a targeted Python check of manuscript labels and references. At this
  first pass there were no duplicate labels; every unresolved reference was
  to a label expected in the still-missing Appendix A.
- Repeated that targeted check after Appendix A arrived: no duplicate
  labels, unresolved references, or undefined citation keys remained.
- Ran a targeted prose-spacing scan of these LaTeX files. It confirmed the
  number joins listed in E8.
- Repeated the prose-spacing scan after the revision: the reported prose
  joins no longer appear.
- No project-wide verification and no CI inspection were performed.

## Integration disposition

The final complete LaTeX and built PDF have been reviewed, including title
anonymity, references, table widths, page breaks, formulas, main/appendix
balance, and dispositions of the findings above. The bibliography audit
has been checked against local material supplied by the sole literature
lead; this review does not independently verify external source content.

## Revision follow-up

- E1 resolved: the normalized linear coefficient is now `ell_j`.
- E2 resolved: the raw matrix parameter in the depth and contact proofs is
  now `G`; the closure appendix begins with its notation definitions.
- E3 resolved in the revised `exp:multiround` and `exp:policy-details`:
  efficacy candidates, efficacy metric, majority-ray comparison, AUC,
  switching destination, recovery contrast, and separate 14-comparison
  endpoint adjustments are now defined.
- E4 resolved: the main text now reports differing cross-evaluated progress
  and retains its explicit no-causal-mechanism qualification.
- E8's Appendix F number joins have been corrected in the revised prose;
  the targeted scan is clear. Both missing macro escapes are repaired.
- E9 resolved: the minor direction is now `D_edge`, and the two-ray
  discriminant is `Delta` throughout Section 2 and Appendix A.
- E5's closure survey now uses theorem references and neutral R1–R8 labels,
  whose companion data and source mapping are explicitly described.
  `companion/archive/survey-labels.json` and the companion READMEs now map
  all eight neutral names to the original records, saved coordinates,
  record selectors, and code definitions. The
  companion's population paragraph now explicitly distinguishes 11 distinct
  corners, seven completed-family subsets, 18 comparisons, and 17 numerical
  matches.
- E6's alternative-bound subsection now uses a mathematical description;
  the introduction removed the “uncorrected version” language and explains
  the hypothesis difference directly. “Author draft” correctly identifies
  the unpublished citation; it need not block submission.
- E10 resolved: the fidelity paragraph states that both numerical ratio
  values use the same floored cost vector.
- E11 resolved in the source: the intended integers and ordinary prose
  spacing have been restored, preserving separate lists of counts.
- E5's remaining four-ray diagnostic now identifies `famBP` and refers to
  `cl:unbounded`.
- E7 is advisory, not a submission blocker. The main text presents the
  central perturbation argument; the appendix explicitly checks the kernel,
  Schur complement, and singular-limit cases. Retaining both serves those
  distinct reading needs, though the proposed shortening remains possible.
- E12 resolved: `exp:minor-diagnostics` now defines the apex-identity
  frame, common semidefinite margin and apex normalization, Frobenius
  objective, and `(1-10^-6)` target for the minor LP comparison.
- E13 resolved: the benchmark identifier is restored to `waterund25`.
- E14 resolved: both duplicated equation-name sentences now use `Cref`
  alone.

Appendix A follow-up: proof sequence and references are coherent. The
hardness proof now defines `omega(G)` as the graph's clique number; the
two-ray proof says that the subproblem is infeasible if no positive larger
root exists; and the algorithm parameter is `min(rank P,rho)`.
The efficacy remark now states the metric, constructs a bounded epigraph,
and identifies the separation-to-optimization result used. The sole
literature lead reconciled citations for the established algebraic
decision, polytope upper-bound, Motzkin–Straus, and weak
separation-to-optimization ingredients. The inspected sources are Renegar
Part III, McMullen, Motzkin–Straus, and the GLS 1988 monograph.

## Preliminary PDF review

Reviewed the first integrated `build/main.pdf`, 84 pages, creation timestamp
6 October 2026 11:15:14 EDT. The PDF was being rebuilt during follow-up;
these page numbers identify that preliminary version.

- `pdfinfo` confirms a blank Author field. The title page has no visible
  author line or date.
- `pdftotext -layout` found no unresolved `??` references or citations in
  the full PDF.
- Rendered and visually inspected pages 1, 10, 19, 27, 39, 50, 60, 61, 68,
  71, and 72. The empirical-prose reviewer covered the text of Sections
  7–9 and Appendix F and rendered pages 31, 36, 79, and 82.
- The main text occupies approximately 36 pages and the appendices 44;
  the balance supports the paper's conceptual exposition and full proofs.
- Tables, mathematical displays, and proof typography are readable. The
  four logged overfull boxes are visible on pages 10, 46, 61, and 65 and
  are already assigned for correction. A full-PDF word-bounding-box scan
  found no other substantial margin problem.
- E11's split integer counts remain a required data-transcription fix.
  The preliminary empirical reviewer also found `under-reports;138` on
  page 81, which needs an ordinary space after the semicolon.

Targeted document commands actually run: `pdfinfo build/main.pdf`,
`pdftotext -layout build/main.pdf /tmp/qic-editorial-prelim-layout.txt`,
`rg` on the four document warnings in `build/main.log`, `mutool draw` for
the listed sample pages, and `pdftotext -bbox-layout` followed by a local
word-boundary scan. The initial scratch XML parser rejected a PDF glyph
control character; stripping XML-invalid control characters allowed the
scan to complete. This did not require any manuscript or PDF modification.

## Final PDF and source review

Reviewed the stable `paper.pdf` supplied by the lead, also present as
`build/main.pdf`, and copied it to a scratch snapshot to avoid reviewing a
moving build. The final delivery version has 85 pages, 836,086 bytes, and
creation time 6 October 2026 11:54:06 EDT.

PDF SHA-256:
`632689918cc14302a2c594e6710442c3f8831be97a71b0dc80face2daf201bd0`.

- The Author metadata field is blank. The title page has no author line or
  date, and the revised abstract reads coherently.
- Full-PDF text extraction has no unresolved references or citations, and
  none of the malformed formulas, benchmark identifier, or prose joins
  raised in E8, E11, and E13 remain.
- Visually inspected pages 1, 11, 12, 39, 41, 47, 51, 60, 61, 65, 72, 84,
  and 85. The empirical reviewer read pages 31–40 and 77–84 and rendered
  pages 37, 79, 81, and 83. The new rank-one figure, long displays, exact
  certificate tables, empirical tables, policy definitions, and references
  are clear and within the page margins.
- The main text ends on page 40, where Appendix A begins; the references
  occupy the end of page 84 and page 85. The main text explains the geometry
  and consequences, while the appendices provide full proofs and evidence
  details. This is a coherent balance for the requested substantial paper.
- The final document log has no unresolved-reference, citation, multiply
  defined label, or overfull-box warnings. The full-PDF word-bounding-box
  scan found no substantial lateral margin outliers.
- The final source scan covers 20 submission input files: 200 unique
  labels, 251 references, and 41 citation uses, with no duplicate labels,
  undefined references, or undefined citation keys.

The aggregate SHA-256 of the reviewed source inputs is
`bb3f850864a63ae11bc52133f9956cb2674168624942d2340ed9d143a77e668a`.
It hashes sorted relative path, NUL, file bytes, NUL for `main.tex`,
`macros.tex`, `references.bib`, all section and appendix TeX files, and the
figure TeX file.

Additional targeted commands actually run: `sha256sum`, `pdfinfo`,
`pdftotext -layout`, `pdftotext -bbox-layout`, `mutool draw` for the final
sample pages, and inline Python for citation/label coverage, source hashes,
literal-transcription checks, and bounding-box inspection. Only scratch
copies and the review report were written; no manuscript sources or PDF
were changed. No optimization experiments, project-wide checks, or CI
inspection were performed.

No unresolved editorial or PDF layout blocker remains. Between the full
visual review and the delivery build, the lead restored the scalar width
symbol to `widetilde X` in Appendix B, removed the two duplicated equation
names, and changed the minor implementation citation to the inspected 2020
report. The delivery PDF text was compared against the reviewed snapshot:
only those expected changes and their line spacing differ. Pages 51 and 56
were rendered again and are clear. The source coverage scan was repeated
after these changes and remains clean.

## Final local citation-audit review

Read `evidence/literature-audit.md`, supplied by the sole literature lead,
and compared its claim map with the final abstract, introduction, discussion,
and cited algorithmic ingredients. The current text follows the audit's
source versions, hypotheses, and novelty dispositions.

- The unrestricted cut-generating-function framework is explicitly
  background. The text distinguishes ordinary finite-valued functions,
  relaxed functions, cone containment, supremum equality, and attainment.
- Set and depth optimization have direct precedents. Eckstein–Nediak's
  structured finite-point-set problem is qualified; Xavier–Fukasawa–Poirrier's
  largest-coefficient objective is compared with the reduced-cost-weighted
  objective. The manuscript does not claim the general selection idea as new.
- Quadratic-free-set characterizations, the BCM rotation subfamily, and
  lattice-free closure results receive appropriate attribution. The stated
  orbit, closure, and convergence claims retain their specific settings.
- Report-specific SCIP formulas and root experiments cite the inspected
  2020 report. The 2023 journal citation is retained for the published
  implementation attribution. Fischetti–Monaci's heterogeneous effects are
  presented without a general solver-ranking claim.
- The novelty sentence is qualified and limited to the particular proved
  guarantees, contact criteria, exact obstructions, and adversarial sequence.
  Neither the abstract nor the discussion broadens that priority claim.
- Established algorithmic ingredients cite the inspected versions. The
  manuscript supplies its own encodings, reductions, truncation argument,
  bounded epigraph, and oracle application rather than citing those steps
  as consequences of a broader unrelated result.

The literature audit records unavailable exact publications and inspected
counterpart versions. The current manuscript uses that distinction
consistently. This editorial review relies on the lead's local source
inspection and does not add independent searches or a stronger priority
claim. The final reference-key and PDF link checks are clean.
