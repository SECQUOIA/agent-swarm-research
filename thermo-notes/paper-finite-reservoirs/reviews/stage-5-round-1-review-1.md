# Stage 5, round 1, independent review 1

**Verdict: no major issues.** The synthesis is consistent with the proved results and preserves the accepted mathematics. I found three minor clarifications needed in the new prose. None requires a change to a theorem or its proof.

## Scope and independence

I reviewed the Stage 5 author record, complete `main.tex`, introduction, numerical section, conclusions, manuscript README and coverage audit, relocated short-range appendix and its new main-text guide, figure code, standalone numerical scripts, requirements, archived/derived numerical data, bibliography changes, and relevant status-note changes. I did not read other Stage 5 reports, edit manuscript files, or delegate. This stage review is distinct from the later whole-manuscript review.

## Minor issues

1. **The short-range proof guide should refer to logarithmic partition derivatives.** In the new closing guide in `sections/microscopic.tex`, “positive contour phase partition functions have bounded second derivatives in a finite-size temperature window” should say that their **logarithms** have second derivatives of order `N` in that window. The accepted appendix proves `|d² log Z_i/d beta²| <= C N`, not an order-`N` bound on `Z_i''` itself. The moment argument and formal appendix are correct; the introductory description should name the same quantity.

2. **Qualify the comparison between TV and arbitrary averages or thermodynamic potentials.** In the second introduction paragraph, the assertion that TV “is stronger than agreement of thermodynamic potentials, energy density, or any specified finite set of averages” can be read as claiming that TV convergence itself guarantees all such agreements. Without moment or uniform-integrability assumptions it does not control unbounded observables, and a normalized law does not determine an arbitrary partition-function normalization. The preceding bounded-measurement sentence is correct. A suitable correction is: “Agreement of thermodynamic potentials, an energy density, or a specified finite set of averages does not by itself establish this full-law accuracy.” Alternatively restrict the comparison explicitly to uniformly bounded observables and separately discuss thermodynamic summaries. The paper's actual TV theorems do not require modification.

3. **Mention the stronger boundary hypotheses in the abstract/introduction summary.** The abstract and introduction's boundary paragraph move directly from the general microscopic `N^(3/2)` thresholds to the boundary error/optimization result. The formal boundary theorem needs an exponential moment beyond the finite tilt and vanishing reweighted exceptional mass; in particular, the two-dimensional short-range application is established only for sufficiently large fixed `gamma`. The conclusions correctly state this restriction. Add “under stronger stated tail conditions” to the abstract's boundary sentence, and a concise qualifier in the introduction explaining that the short-range boundary formulas hold for all fixed positive `gamma` in spatial dimensions above two and for sufficiently large fixed `gamma` in two dimensions. This prevents a reader of only the leading summaries from attributing an all-`gamma` two-dimensional formula to the general microscopic iff theorem.

## Mathematical consistency of the synthesis

The weak-support result is summarized with the essential condition of at least three limiting energy support points and with optimization over composite total energy. The introduction correctly distinguishes multiple symmetry-related spin phases at the same energy from three distinct macroscopic energies. The two-phase row in the summary table names both the nondegenerate fluctuation input and the positive tail/exceptional-mass control required for sufficiency.

The summary identifies the correct microscopic scope: three-state mean-field spins and sufficiently-large fixed-`q` short-range spins in every fixed spatial dimension at least two, with optional kinetic coordinates. The short-range argument's use of positive contour measures and physical spin-energy transfer is maintained. Its main-text statement points to the complete appendix proof.

The shared-bath claims retain the independent-copy construction, the intermediate window, balanced reference weights, and the distinction between full marginal and joint canonical accuracy. The one-bit statement concerns full microscopic mutual information and is described as requiring a separate entropy argument. The conclusions do not extend the construction to interacting spatial subregions.

Physical boundary optimization is distinguished from phase-population compensation and from numerical finite-size optimization. The stated possibility of abandoning a phase is a consequence of the proved arbitrary-calibration optimum. Exact Gaussian geometry and the prescribed capillarity model are presented separately from microscopic interfacial results. The conclusions explicitly restrict the barrier discussion to specified energies and do not infer transition rates.

## Relocation verification

I independently reconstructed the earlier microscopic section by joining the current main-text portion before the new guide with the appendix body and restoring the original heading levels. Its SHA-256 is

`4f6cfab2a45063487df9a706731ca9a670f7231f4825410a72c518e3c9061fe2`,

matching the accepted Stage 2 round-2 frozen value. Thus the relocation did not alter that mathematical body. Stable result labels remain available, the main input order includes all sections and appendices, and the inspected final log has no undefined-reference/citation or box warnings.

The more technical contour proof now sits in an appropriate appendix while its statement and explanatory route remain in the main text. The exact Gaussian and capillarity material remains in the same PDF and is referenced by stable appendix labels. No required proof was omitted to shorten the principal presentation.

## Numerical and reproduction checks

- I verified that `data/potts-finite-bath-results.json` is byte-for-byte identical to the retained original archive. Its SHA-256 is the documented `93fed9507ceaf9126feb93e79ae5bbb295be185a56f9a84dabe0608e55aab2c1`.
- I independently compared the stored fresh `N=300` calculation with all four corresponding archive records. Each full-TV difference is approximately `1.11e-16`, comfortably within the stated `1e-11` tolerance.
- AST comparison confirms that `canonical_energies` and `finite_bath` are unchanged from the independently checked original algorithm. The standalone script changes the command-line plan and output handling. Both independent-check function bodies are also unchanged.
- The archived file contains the stated size/regime plan; the `--all-archived` path reads that plan rather than silently adding unsupported large-size points. Recomputed output defaults to a separate file.
- The figure code uses the archive's full-energy/full-state TV field, not the separate spin-configuration marginal TV. Its mean-field phase weights, variances, and secant slope agree with the formulas. The derived boundary values `0.15739182188178924` and `0.0379859806585022` match the numerical section's rounded statements.
- I inspected both generated PNG figures. Axes, legends, boundary reference lines, and the optimizer crossing are legible. Figure 1 is identified as finite-system mean-field data; Figure 2 is identified as a limiting equal-variance formula. No short-range numerical validation is implied.
- The README distinguishes archive provenance, quick checks, figure regeneration, and optional large enumeration. It states the surface-capacity meaning of the historical JSON field and explicitly distinguishes ordinary floating-point checks from rigorous interval bounds. The included figures and bibliography source allow a LaTeX build without Python or network access.

I did not rerun the expensive large-size enumeration; it was not necessary to check the unchanged archived provenance and relocated formulas. Earlier stage checks of the exact algorithm and Stage 4 formulas remain applicable to the unchanged functions.

## Literature positioning and status files

The new literature discussion does not claim invention of power-law baths, Gaussian ensembles, energy-range-squared sufficiency, two-Gaussian coexistence models, opposite-phase locking, or the underlying geometric constructions. It distinguishes the prescribed canonical target and full-state metric from optimized comparison temperatures and histogram Euclidean norms. The retained Griffin–Matty–Swendsen source's equation (23) and temperature-optimization discussion support that distinction; the Challa–Hetherington primary text supports the stated Gaussian finite-reservoir precedent.

The narrower claim is an exact optimized strong-distance classification with explicit microscopic assumptions. The closing literature paragraph correctly makes the mathematics independent of a historical-priority assertion. The coverage audit and status-note updates identify the short-range sufficiency and optimal Gaussian phase-loss arguments as completed during manuscript development while retaining earlier reports as historical records. They do not imply external peer review, submission, or certified priority.

The remaining issues from this review are the three local prose corrections above.
