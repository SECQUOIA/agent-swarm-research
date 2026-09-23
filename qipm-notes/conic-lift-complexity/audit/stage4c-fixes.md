# Stage 4C corrections

Implemented the four minor corrections accepted by the root agent after the five independent reviews. No theorem, asymptotic bound, or proof conclusion changes.

1. **Review 2, item 1 — rotating-example angle.** In `sections/10g-conditioning-counterexamples.tex`, the example now specifies `0 < theta < pi/2`. Both displayed norm and residual formulas therefore have nonnegative sine factors, while the signed derivative and mixed-channel formulas remain unchanged.
2. **Review 2, item 2 — relative recourse domain.** In `sections/10e-projected-compilers.tex`, the reconstruction map now explicitly varies over the affine space `{x: h_i - Tx in range W}`. The KKT derivative is stated for tangent directions, with the same independent-row reduction applied to `W` and `T`. Smoothness is restricted to the relative open subset admitting strictly positive recourse. This retains the compatibility equalities when `W` is rank deficient.
3. **Review 2, item 3 — bit-count constants.** In `sections/10g-conditioning-counterexamples.tex`, the conditional bit-count consequence now explicitly assumes `C > 0`, `K_0 > 0`, and `q > 0` before the logarithm and division by `q`.
4. **Review 4 — entropy Hessian setup.** In `sections/10b-entropy-aggregation.tex`, assembling `G` explicitly requires the additional product `A^T (1/s)`. The two-product count now refers to each solve after assembly. The stated `O(N+B+nnz A)` arithmetic bound includes assembly and remains valid.

Validation: ran `conda run -n qipm --live-stream make` successfully. The resulting `main.pdf` has 114 pages. The final LaTeX log contains no warnings, undefined references or citations, multiply defined labels, or overfull/underfull boxes. Only the three listed manuscript files and this audit were intentionally edited; the build refreshed generated artifacts.
