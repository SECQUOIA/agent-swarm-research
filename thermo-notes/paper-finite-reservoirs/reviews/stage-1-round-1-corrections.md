# Stage 1, round 1 — corrections

All five accepted minor issues in the coordinator's adjudication have been addressed. No theorem hypothesis, conclusion, or proof argument was changed.

1. **R1.1/R3.1 — cutoff equality.** In `sections/framework.tex`, the secant weight is now explicitly zero **at and above** the cutoff. This agrees with the exact marginal and covers an atom at the cutoff.
2. **R1.2/R2.1 — interpolation conclusion.** The secant-bound proof now states that the convex difference is nonpositive **throughout the interval**, removing the ambiguous word “there.”
3. **R3.2 — asymptotic wording.** Both abstract threshold descriptions in `main.tex` now say the exponent **grows faster than** the relevant scale. A fixed multiplicative excess is no longer suggested.
4. **R4.1 — unbounded observables.** The framework now says matching a mean energy, pressure, or a few local observables need not determine total variation. It separately states that total variation controls uniformly bounded observables and that convergence of expectations of unbounded observables requires additional tail control, such as uniform integrability under both laws. The reviewer's valid rare-high-energy counterexample remains preserved in the independent review; no unbounded-moment implication is claimed.
5. **Coordinator normalization clarification.** The secant log-weight is now called a **reference-normalized residual log-weight**, with its reference-center subtraction specified. The following sentence distinguishes this reference normalization from probability normalization by the expectation of the weight.

## Validation

Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in `paper-finite-reservoirs`. Compilation completed successfully and produced the 10-page `main.pdf`. The automatic second pass resolved the temporary cross-reference warning. The final `main.log` contains no warnings or overfull/underfull box diagnostics. I checked the corrected wording against all five accepted issues and left the Stage 2 material and workflow untouched.
