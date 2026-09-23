# Stage 4 independent review 1

Reviewed `sections/04-certification.tex` and `appendices/certification.tex`, with relevant accepted locality and calendar-DP dependencies. Primary focus: support bounds, weighted trace, rational/logarithm/interval arithmetic, cardinality and spacing, and exact versus numerical claims. I did not read any other review report or change manuscript sources.

## Verdict

**MAJOR: none.** The reviewed support and arithmetic results are valid. I found one **MINOR** clarification in the rational-witness contract. The remaining Stage 4 arguments also passed my mathematical reading; their numerical experiments and final integration are reserved for later stages and are not missing Stage 4 requirements.

## MINOR 1 — make rational witness choices and the locality enclosure explicit

**Locator:** `sections/04-certification.tex:70–78`, and the opening of `appendices/certification.tex`.

The support theorem correctly allows any real SPD reference `N` and any valid real `delta < 1`. The subsequent assertion that rational model data allow `N^{-1}` to be recomputed by rational elimination needs the additional choice that `N` itself is rational. Rational model data also do not make every stated locality expression rational: for example, the accepted partial-packet bound in `eq:partial-normalized-delta` contains `sqrt(kappa*s)`. Consequently an arc score containing `1/(1-delta)` need not be rational merely because the covariance and sensitivities are rational.

**Suggested correction:** before invoking rational score arithmetic, explicitly choose a rational SPD reference (for example, a rational rounding of a numerical proposal, followed by an exact SPD check) and a certified rational upper enclosure `delta_hat` with `delta <= delta_hat < 1`. Use `delta_hat` in all certificate scores. Such an enclosure can use the rational envelopes from the approximation proof, or an outward enclosure of the square roots in the sharper bounds. If the chosen enclosure is not below one, refine it, increase memory, or decline that certificate. Apply the same rational-witness convention to scenario references and weights. This is a clarification, not a defect in the real-valued support theorem: its data atoms are PSD, so enlarging the locality factor preserves the bound.

## Independent checks

The independently written executable is `verification/stage04-review1/check.py`; its summary is `verification/stage04-review1/results.json`. It imports no repository audit helper and does not overwrite historical results. Run with the existing Python environment:

```
code/research_20260912/.venv/bin/python paper-correlated-measurements/verification/stage04-review1/check.py
```

All checks passed:

- **1,200 exact rational signed interval cases.** Independently formed component intervals, squares crossing zero, all off-diagonal products, and the common denominator `G^3 G_F^2`; checked inclusion of the exact quadratic, division by the positive variance floor, and the final score-grid ceiling. The set included **503 cases with a negative quadratic upper endpoint**, exercising the stated clamp.
- **64 exact matrix inequalities.** On a six-time rational AR-plus-nugget model with signed two-dimensional sensitivities and a nontrivial SPD prior, checked the prior-aware local upper information matrix against every selected set. Each two-dimensional PSD comparison used exact diagonal and determinant tests.
- **112 constrained schedule families.** Independently compared a count/mask/cooldown DP against exhaustive schedules over cardinalities zero through six, gaps `1, 2, 4, 9`, mandatory selections, forbidden selections, and an incompatible mandatory/forbidden case. The window was one, so some cooldowns exceeded both memory and the horizon.
- **39 feasible-family rounding comparisons.** Verified the support maximum after direct ceiling is at most the exact rational maximum plus `k/G_s`, including the zero-cardinality case.
- **Nine logarithm diagnostics.** Reimplemented the rational series and sign-aware power-of-two combination, including determinants below one and exponents `+300` and `-300`, and compared with 100-digit numerical logarithms. These are implementation diagnostics, not a replacement for the series/remainder proof.

## Mathematical assessment

The prior stays uninflated in the local certificate. The support maximum is correctly over the full feasible path family, and a mixture is never used as a feasible-experiment lower bound. Weighted trace is nonnegative under its stated PSD assumptions, making its zero-upper-value and ratio conclusions valid.

The signed interval denominator powers and clamp are correct. Non-PSD rounded weight entries cause no difficulty because termwise interval inclusion is used, rather than a false matrix-order assertion. The variance floor is explicitly rejected if nonpositive. The manuscript also correctly distinguishes an exact determinant/log interval from an ordinary floating exponential used to display efficiency.

The virtual-noise resolvent, including zero coordinates and a semidefinite split boundary, has the stated derivative. The all-split lower witness uses the right convexity and dual signs and keeps one common fractional point, so neither an implicit minimax interchange nor an assumed optimal proposal enters the proof. The robust bounds propagate standardizer intervals in the correct directions. The fixed-scenario approximation proof does need, and correctly retains, two factors when normalizers are estimated from the same returned set.

The separator support bound permits arbitrary nuisance coefficients because completing the square gives an upper information matrix. The cross-representation proof retains the nuisance prior cross terms, and the nesting direction is correct. The explicit restriction to full schedule hulls prevents an expected-count block-mixture relaxation from being confused with the claimed hierarchy.

## Primary-source checks

I read `literature/AGENTS.md` before consulting literature and made no literature-package changes. I inspected the following actual local PDFs through text extracted directly from the originals:

- Harman and Trnovská (2009), printed pp. 695–696, especially the support derivative, Theorem 1, and equations (6)–(7). These directly support the manuscript's attribution of information-hull support bounds to prior work.
- Hainy et al., arXiv:2504.17651v1, PDF pp. 9–10, especially Section 4.4 and equations (18)–(20). The explicit linear pricing and restricted master confirm the stated simplicial-decomposition predecessor. I also checked Proposition 3 and its boundary-case statement in the local extracted text.
- Kim and Kim (2006), arXiv:cs/0611043v1, pp. 1–2, Lemma 1. This supports the credited convexity result; the manuscript gives its own valid Hessian proof and does not claim that convexity as new.

No unsupported novelty claim was identified in the support/arithmetic material within this review's primary scope.
