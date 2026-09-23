# Final whole-manuscript review 4

Reviewed 2026-09-14. Scope: the complete current 32-page manuscript, all scientific sections and Appendix A, including mathematical exposition, implementation/formalization boundaries, experiments, conclusions, figure/tables, references and reproduction instructions. This is a final paper review, not a review limited to the preceding Stage 5 edits. I did not consult other Stage 6 reports, delegate, rerun experiments, or read the bulk archive.

## Verdict

**No major issue found. One minor clarification of experimental status labels remains.** Subject to that local correction, I consider the current exposition and scientific organization ready for journal review within the explicitly stated methods/software scope. I found no missing scientific development that requires an additional experiment or theorem to support its actual claims.

## Minor correction

**Name the selected model statuses, rather than giving unexplained numerical codes.** Section 6.3 (`sections/06-experiments.tex`, paragraph beginning “For saved solver objectives”) includes model-status codes 1, 2, and 8 without identifying the status system or meanings. A reader who does not use GAMS cannot tell whether the screened records claim global optimality, local optimality, or merely a feasible integer solution. Replace this with “GAMS model statuses 1 (Optimal), 2 (Locally Optimal), and 8 (Integer Solution)” or equivalent wording. This makes the meaning of the 18 flagged pairs clear and reinforces the existing distinction between an investigation candidate and a proven solver error. The names agree with the [official GAMS model-status documentation](https://www.gams.com/53/docs/UG_GAMSOutput.html). No numerical change or new experiment is needed.

## Whole-paper scientific assessment

The central claim is well defined: finite pointwise bounds for the exact loaded expression model, obtained from conservative nonlinear cuts, an identified rational master, and fully replayed discrete derivations. The title, abstract, introduction, mathematical statements, and final discussion consistently make this claim. They do not promote sufficient admission to completeness, proof acceptance to original-model feasibility, or focused Lean proofs to executable verification.

The literature review supports the stated contribution without a broad priority claim. It covers convex mixed-integer certificates, computational geometric certificates, outer approximation and numerical safeguards, rigorous convex bounding and interval approaches, rational MILP proof systems, and formal optimization precedents. The finite-box calculation and monomial criteria have local attribution beside their development. Elementary implications are included for a standalone checking contract, rather than claimed as new mathematical discoveries. The integration, repaired failure boundary, and measured reproducibility are concrete scientific results appropriate to the chosen scope.

The proofs are sufficiently explained for an optimization reader. In particular:

- Exact model semantics are fixed before any theorem about cuts. The decimal/binary counterexample demonstrates why that choice matters; source-format equivalence remains a separate issue.
- Propagation preserves the mixed-integer feasible set, while cuts remain justified on the entire resulting box. The proof does not require that integer-rounded boxes retain every continuous-relaxation point.
- Finite, one-sided, free, and fixed coordinates are covered, including all residual slopes. The worked slope-rounding example provides an actual invalid cut and its rational repair. Support-vector existence is stated separately from convexity at singular boundaries.
- The discrete induction has earlier-reference ordering, sign-valid combinations, integrality conditions, exact domination, and explicit branch dependencies. Incumbent cutoff validity is established on a restricted set and then lifted with an actual feasible witness; no unstated optimum-attainment premise is needed.
- Objective-preserving extension handles affine constants, free epigraph coordinates, and objective sense. The subsequent primal corollary requires original feasibility and an outward upper bound.
- Quadratic, monomial, fractional, and scalar composition explanations substantiate the implemented sufficient recognizers. The formalization section states exactly which further implications are mechanized and which actual software computations remain trusted.

The experiment narrative answers its advertised questions. It preserves the 299-to-289 selection, historical 188/92/9 accounting, primary 203/19/67 replay, separate producer outcomes, and separate representation repairs. The 222-model catalog is a provenance-preserving union, not a uniform-protocol success rate. Timings distinguish accepted-record sums, all-record sums, elapsed time, tool phases, requested search limits, outer limits, and thread settings. Source audits and exact primal witnesses support the two case conclusions without attributing unseen internal causes. The single remaining status-label correction improves interpretation but does not alter these conclusions.

## Organization, notation, and presentation

The section order follows the logical dependencies and works as a standalone article: model semantics, soundness, implementation, focused formalization, evidence, discussion, reproduction. The reader can assess the mathematical assertion without accessing research notes. Software details are concentrated where they explain a concrete acceptance condition or recorded failure. The discussion synthesizes completed results and their limits rather than offering an unfinished research agenda.

Notation is introduced with its local scope. The original/lifted feasible sets, nonlinear rows, affine residuals, support data, master objectives, certified bounds, and reference discrepancies are distinguishable. Cross-section statements about “complete checking,” “partial checking,” “verified,” “original model,” and formal coverage agree. I independently scanned all current source labels/references: **no undefined or duplicate labels** were found. The current clean LaTeX log contains no undefined-reference/citation or layout warnings.

The Stage 5 OA/SOS fixes are present. The main result table's caption now defines the interpretation of `d`, points to Section 6.3, and limits reference rows to verified bounds. It is therefore understandable even when it floats ahead of the metric subsection.

I inspected the delivered PDF's text and visual layout, including current renders of pages 9, 14, 24, and 28 (coordinate tables/proofs, composition table, timing/metric material, and appendix commands), in addition to the architecture/results presentation inspected during integration. Mathematical displays, tables, and commands are legible and unclipped. The figure conveys the intended evidence chain and expressly excludes a verified executable Lean connection. The delivered PDF has 32 pages.

## Standalone availability and reproduction

Appendix A and the root documentation give concrete accompanying paper, core, and bulk archive names, contents, dependencies, version distinctions, and relative-working-directory commands. They do not invent a public deposit or DOI. The core/bulk byte counts in the current index match filesystem sizes (6,478,681 and 30,664,561,063 bytes), without requiring a bulk read. The expected V3 full-primary outcome is expressly an expectation supported by targeted replay, not a new completed uniform campaign. Core examples and audit reproduction do not require licensed solvers or an external notes directory; full proof replay and optional numerical generation have separately documented requirements.

I found no stale manuscript placeholder, missing required section, unsupported end-to-end formal-verification claim, or artifact-access promise dependent on a nonexistent external publication. The final anonymous review copy is scientifically self-contained with its stated companion materials. Journal-specific formatting, author identification, and an editor's acceptance decision are separate from the completed scientific content assessed here.
