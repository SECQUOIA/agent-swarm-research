# Stage 4, round 1 — corrections

Both accepted minor issues are corrected. All theorem statements, formulas, and scope remain unchanged.

## 1. Bounded offset in the alternative density-envelope proof

The final density paragraph of `sections/boundary-and-smooth.tex` now distinguishes the secant estimate `h_N^sec <= C x/sqrt(N)` from the finite-correction estimate `h_N <= C_0 + C_1 x/sqrt(N)`. It states that endpoint values after correction are bounded but need not vanish.

The absorption argument is now applied only to the linear term. The bounded offset is retained as the fixed prefactor `exp(C_0)` in the weighted tail integral. After taking the large-`N` limit at fixed sufficiently large `R`, that prefactor does not affect the tail's vanishing as `R` grows. The existing bounded exterior-weight argument is retained. This also covers a positive corrected endpoint value directly.

## 2. Degenerate semidefinite level sets

The final anisotropic-geometry paragraph of `sections/gaussian-geometry.tex` now includes:

- The zero-radius point for a positive-definite metric.
- For a positive-rank singular metric and a linear coefficient in its range, an elliptic cylinder at positive radius and an affine subspace at zero radius.
- A paraboloid with possible additional flat directions when the linear coefficient has a nonzero nullspace component.
- For a rank-zero metric, a hyperplane when the linear coefficient is nonzero, and the whole space when both coefficient and compatible constant vanish.
- Empty loci for inconsistent constants in the completed-square or constant cases.

These alternatives follow by splitting the variable into the metric's range and nullspace and completing the square on its range. The current `stage-4-author.md` wording was updated consistently. No previous review was changed.

## Validation

Checked the tail-integral argument with the bounded offset retained and checked the level-set classification by range/nullspace decomposition. No new major issue was found. Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in the paper directory: successful 39-page PDF, with no warnings or overfull/underfull box diagnostics in the final log. These local proof and exposition corrections require no new numerical calculation.
