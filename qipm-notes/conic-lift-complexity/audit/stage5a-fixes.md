# Stage 5A corrections

Implemented all five consolidated minor corrections accepted in
`audit/stage5a-assessment.md`. No substantive result or proof was changed.

1. **Positive compression parameters:** In the principal-minor contraction
   proposition in `sections/11a-exposed-movement.tex`, the injective
   compression has `r >= 1` columns and the optional sharper gradient
   parameter satisfies `vartheta > 0` before the distance bound divides by
   its square root. The matrix-ball example also states `1 <= r`.
2. **Defined compression matrix:** The matrix-ball example now defines `U`
   as the `p` by `r` matrix of the selected orthonormal left coordinate
   vectors.
3. **Positive divided chord bounds:** The exposed spectral-profile bound
   now specifies `0 < R_0 < 1`. The general bounded-move consequences in
   11a and 11c explicitly require an integer `m >= 1` and `0 < R < 1`
   when dividing by `-m log(1-R)`, and an integer `M >= 1` when dividing
   by `M`. The formulas in 11b already specify these conventions, as does
   the tube-increment proposition in 11c, so they needed no edit.
4. **Central arc domain:** The central route and chord-count formula in
   11c explicitly use `0 < epsilon <= k` and `0 < R < 1`. The text records
   the zero-length endpoint at `epsilon = k` and explains that larger
   tolerances are already met at the analytic center.
5. **Entropy normalization:** Changed “equal objective weights” to “unit
   objective weights” for the specialization
   `Delta_eff = exp(H(p))`.

## Validation

Ran a clean rebuild with `conda run -n qipm --live-stream latexmk -C
main.tex`, followed by `conda run -n qipm --live-stream latexmk -pdf
-interaction=nonstopmode -halt-on-error main.tex`. The build completed
successfully and produced a 133-page PDF. The final `main.log` contains
no warnings, undefined references or citations, overfull boxes, or
underfull boxes. The complete multipass build output is retained in
`audit/stage5a-fixes-build.log`; its initial missing-reference messages
are resolved by the later passes.

Checked all divided bounded-chord expressions in 11a–11c for consistent
positive-radius and positive-integer count domains. Only the two cited
manuscript section files, this correction record, the build log, and
generated LaTeX artifacts were changed by this correction task. Stage 5B
and final integration were not started.
