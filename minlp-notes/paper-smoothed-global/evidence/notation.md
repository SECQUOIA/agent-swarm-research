# Shared notation and file ownership

The root owns `main.tex`, `macros.tex`, `references.bib`, packaging, and final
integration. Authors may request macro additions in their reports. Do not edit
another author's files. Use standard LaTeX when a macro is unavailable.

- `I`: base rational input bit length, before perturbation sampling.
- `n`: total original coordinates; `n_c`, `n_z`: continuous and native integer
  counts when useful.
- `k`: auxiliary nonconvex factor dimension or continuous core dimension.
- `p`: maximum bag size (treewidth plus one).
- `d`: fixed polynomial degree. Counts of input inequalities may use `r`.
- `L`: upper coordinate curvature on the relevant continuous domain.
- `alpha`: supplied core/factor quadratic convexifier.
- `nu`: magnitude of the most negative original quadratic Hessian eigenvalue.
- `sigma`: noise width; `gamma`: original/core random linear coefficients;
  `xi`: aligned factor coefficients when these differ.
- `M`: number of equally spaced labels per noise marginal; it is a power of
  two computed from base data. Use a different symbol for constraint matrices.
- `h_j`: mesh at stage `j`; `J`: base-selected stopping stage.
- `E_j` or `B_j`: rounding/lower-bound correction; state which coordinates
  contribute. `U_j`: feasible upper value; `f^*`: sampled global minimum.
- `B`: base-computable fallback work factor with polynomial-length encoding.
- `g_0`: analysis growth threshold; `tau`: active-gradient or label-gap threshold.

All theorem/lemma labels must use a chapter prefix. Prefixes are `count:`,
`qp:`, `sp:`, `con:`, `rec:`, `int:`, `lim:`, and `model:`. Appendix labels
may use the same prefix. Use `\label{thm:qp:...}` or analogous full labels.

Proposed ownership: counting and quadratic sections plus Appendices A/B;
sparse and constrained sections plus Appendices C/D; continuous/integer
recourse sections plus Appendices E/F; front matter, model, limitations,
discussion and Appendix G. Every block needs a source-development-to-label
map, complete proof dependencies, and an author verification report.
