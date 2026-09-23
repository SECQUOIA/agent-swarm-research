# Stage 5, round 1 — corrections

All five merged minor issues accepted by the coordinator are corrected. No theorem, formal proof, numerical core, or workflow status was changed.

1. **TV and thermodynamic summaries — `sections/introduction.tex`.** Replaced the unconditional “stronger than” comparison with the statement that agreement of thermodynamic potentials, energy density, or a finite set of averages does not generally establish full-law TV convergence. Retained the preceding bounded-measurement statement and added the need for extra integrability for unbounded averages, with a framework cross-reference.

2. **Short-range derivative guide — `sections/microscopic.tex`.** The guide now identifies the **logarithms** of the positive restricted contour partition functions as the objects whose second derivatives are bounded in absolute value by `CN` in the stated finite-size temperature window. This matches the formal appendix; the appendix itself is unchanged.

3. **Boundary hypotheses and microscopic range — `main.tex` and `sections/introduction.tex`.** The abstract now qualifies the physical boundary result by stronger phase-tail and exceptional-mass assumptions. The introduction specifies stronger phase-tail integrability and exceptional-mass suppression, then states their verified range: every fixed positive capacity coefficient for the mean-field model and short-range dimensions above two, and sufficiently large coefficients for the two-dimensional short-range model. The optimization claim is retained within this scope.

4. **Historical review status — `research/results-summary.md`.** The review-completion sentence now explicitly identifies and links the earlier Markdown manuscript and shared-bath note's linear-capacity development. It directs readers to the LaTeX paper's `WORKFLOW.md` for subsequent review status, including the separate whole-paper review. It does not declare that review completed.

5. **Strict growth wording — `sections/conclusions.tex`.** The support-theorem summary now requires capacity **growing faster than the square** of the energy scale, matching the diverging-ratio theorem.

## Validation

Checked each corrected synthesis statement against its unchanged formal theorem or framework statement. Verified that the historical and current review-status file links resolve. Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from the paper directory: successful 47-page PDF, with no warnings or overfull/underfull box diagnostics in the final log. No new mathematical issue arose during these corrections. The manuscript is ready for coordinator inspection and the mandatory whole-paper review.
