# Final cumulative review

This review covered the completed manuscript and all its supporting files,
including the final increment from `1d48cd06` and the cumulative result from
`fe439d5c885e3efd7f9fc4b1392eaffca7cfcf6f`, when the paper folder did not exist.
The frozen manuscript had 21 pages. Relevant untracked files were included.
No reviewer was supplied with earlier review conclusions. The external
report is retained in `evidence/reviews/final-claude.txt` relative to this
paper folder.

| Independent review | Scope and outcome |
| --- | --- |
| Codex `final_review_whole` | Entire manuscript, repository coverage, primary sources, all three checkers and PDF consistency. No findings. |
| Codex `final_review_foundations` | Residual geometry, lower bounds, Appendix A and the exceptional quadratic atom. No findings. |
| Codex `final_review_upper` | Both encoding bounds, algebraic source statements, coefficient uniformity and conservative output. No findings. |
| Codex `final_review_calibration` | Calibration formulas, reductions, preceding literature and targeted checker. One minor source-wording clarification: exact Gibbs sampling is used for approximate optimization. |
| Codex `final_review_perturbation` | Deterministic repair, cube geometry, grids, stability, tails, exceptional atoms, Gaussian source and coverage. No findings. |
| Fresh Claude session | One Fable whole-target reviewer and three Opus reviewers for calibration, perturbations and algebraic bounds, followed by parent verification. No mathematical error found. Localized assumption, attribution, coverage, check-quality and presentation findings remained. |

## Lead adjudication

The lead independently checked the findings against the manuscript and
primary sources. The following corrections were accepted:

- State explicitly that the refined-Slater point satisfies the linking
  equality. This makes the intended equality-feasible-slice condition
  unambiguous; both upper-bound proofs already use that condition.
- Credit the existing linear-constraint case of conservative polynomial-time
  penalty output: Gu–Ahmed–Dey's encoding theorem and Lefebvre–Schmidt's
  Theorem 15 and stated convex-MIQP extension. Distinguish the present
  extensions to native quadratic inequalities and the deduction made during
  this manuscript's development from a claim to the general printing idea.
- Include the omitted fixed-zero-multiplier consequence of the same binary
  gadget. Its value threshold is `max(1/d_-,1/d_+)`, hence 1 in YES cases and
  `1/(K-1)` in NO cases for K at least 3. The existing polynomial-factor
  reduction applies directly. Clarify the ties at coefficient 1.
- Clarify the Gibbs-sampling comparison, the finite-box assumption in the
  abstract, units of the introductory bound, the RHS-dependent threshold
  notation, the chain variable reference and the singleton image wording.
- Replace the discussion's claim that scripts check reductions by the
  accurate claim that they check calibration formulas and thresholds.
  Strengthen the finite grid, atomic-event and reciprocal-graph checks.
- Repair the coverage table and add concise antecedents for convex penalty
  thresholds and mixed-integer value-function stability.
- Cite Basu–Pollack–Roy's original block quantifier-elimination theorem and
  retain the survey locator. The lead rendered the original book's pages
  559–561 in memory and read Theorem 14.16, including its output coefficient
  bound. The published Kamminga–Rudolph ITCS 2026 metadata was checked on
  Dagstuhl's primary page; all mathematical locators still refer to the
  inspected full arXiv version.
- Make the status of asymptotic constants explicit. Their uniform existence
  permits hardcoding in an existence theorem for algorithms; neither the
  paper nor the quoted quantifier-elimination statement supplies evaluated
  fixed-count constants.

The discrete tail observation was accepted with its precise hypotheses:
for centered grids on [0,1], K dividing q and q at least 2K give at least
`2(K-1)/q` probability of threshold at least q. The external report's further
comparison with `epsilon/8` is not valid for arbitrarily large q without an
upper bound on q. That comparison was rejected; the exact grid inequality
needs only the adjacent-cell count and the existing mixture witness.

The lead did not accept the suggestion to add stable-set approximation
claims. The cited generic phrase would require a specific approximation
factor and an additional theorem; the existing unit-data exact-computation
result already covers the repository development. Multiple citations for
the same elementary range/radius mechanism are not all necessary. Concise
primary-source context is preferable to reproducing a literature audit in
the paper.

All accepted changes are localized clarifications, source attributions,
finite-check improvements or immediate consequences of already reviewed
formulas. No central theorem, proof strategy or assumption actually used in
a proof changes. They can therefore be verified by direct inspection and
targeted checks without another full review round under the build skill.
The final validation record documents the resulting checks.

## Scope of verification

The author and reviewers ran only the manuscript's targeted scripts. Source
statements were read directly; the internal algorithms and proofs of the
cited general algebraic and Gaussian theorems were not independently
reconstructed. Neither finite tests nor these reviews establish exhaustive
literature priority. Lean was not rerun, and no solver experiment,
project-wide check or CI inspection was performed.

The lead visually inspected PDF pages 1, 14, 17, 20 and 21 using in-memory
Poppler renders. The whole-target Codex reviewer inspected pages 1, 10, 12
and 18, and checked all pages for out-of-page text and unresolved references.
No rendering files were created. The external session reported an unchanged
repository worktree; one reviewer disclosed an import without the bytecode
flag, which could in principle affect an installation cache but was not
observed to create a file. No unrelated repository change is part of the task.

## Final direct verification

After the writer froze the localized revision, the lead inspected all
accepted corrections in the source, the revised check implementations and
their retained outputs, and the updated source and coverage records. The
zero-multiplier consequence and finite-grid tail statement follow from
the previously reviewed formulas with the stated hypotheses. The
exceptional-atom check uses q=17 and explicitly meets the grid theorem's
resolution requirement. No accepted finding remains open.

The lead ran `git diff --check -- paper-exact-penalties` successfully and
used a read-only Python check to verify that the LaTeX log contains no
warnings, undefined references, errors or underfull/overfull boxes, that
the PDF is newer than every manuscript TeX and bibliography input, and
that Poppler-extracted text contains no unresolved reference markers.
`pdfinfo paper-exact-penalties/main.pdf` confirmed 22 pages and 381951
bytes. In-memory Poppler renders of final pages 1, 14, 18 and 22 were
visually inspected and showed no layout defects. The writer's successful
targeted checks are recorded in `stage3-validation.md`; the lead did not
repeat the unchanged tests. The final repository status contained only
changes within this paper folder.
