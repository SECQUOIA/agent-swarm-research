# Front revision, round 2

Date: 2026-10-05. Completed the Sol fallback revision of `sections/00-abstract.tex`, `sections/01-introduction.tex`, `sections/02-setting.tex`, and `sections/10-discussion.tex` after the partial Opus revision. These four files are ready for final integration. No technical section, appendix, bibliography, source note, or other evidence file was edited.

## Main changes

The abstract now attributes the finite-separator obstruction to the examples and describes ordinary-module kernel smoothing together with its density correction. It states the private-block size result at fixed shared width and qualifies rational box certificates by positive slack and expanded SDP dimensions.

The introduction and discussion distinguish the exact local-measure identity from finite SDP gaps. The identity `2 E_{2r}(h)` is stated for the paired two-bag examples with local minima `-h,+h`; their actual local measures give lower bounds for finite hierarchies. It is not presented as an exact description of arbitrary sparse gaps. The discussion gives the order-one quadratic comparison, `1/4` for the SDP gap versus `3-2 sqrt(2)` for the local-measure gap, and notes agreement at order two.

The corner explanation is repaired. Lipschitz derivatives imply an inverse-square approximation upper bound; they do not determine an exact rate. Constraint activation can produce a corner but is not equivalent to one. The discussion's example `min y^2` subject to `y>=x`, `y>=0`, and the boxes has value `x_+^2` and a continuous derivative. The inverse-order sharp example instead has value `|x|` and a projected multiplier jump. The regularity theorems are described through their projected-multiplier hypotheses and repair estimates.

The computational interpretation now separates the fixed-domain inverse-square grid bound from the general affine inverse-order grid bound. It explicitly states the discretization bracket `G_r-epsilon_r <= f* <= G_r`, so lower bounds are not portrayed as exclusive to SOS. The distinct result is control of the specified sparse SDP, its feasible moment points, and its algebraic certificate cone. Numerical runtime and practical speedup are not inferred from matrix sizes or approximation rates.

The setting edits are limited to the canonical Guo--Wang citation key and a paragraph explaining the unused shared-coordinate embedding for examples with entirely private data, with shared evaluation at zero and natural conventions for individual empty shared bags. All five previous setting repairs, including the positive global width/order scope, are preserved. No degree condition, cone definition, or proof was changed.

## Disposition of front-root-r1 findings

| Finding | Disposition |
| --- | --- |
| 1. Universal separator obstruction in abstract | Resolved in the partial abstract revision and preserved; examples can obstruct the rate even with exact local measures. |
| 2. Compactness-only convergence | Replaced by dense Archimedean and sparse local Archimedean convergence hypotheses, with running intersection. |
| 3. Lipschitz derivative implies exact order | Replaced by an approximation upper bound and separate sharp examples; smoother functions can converge faster. |
| 4. Convex corner iff affine constraint active | Removed; an explicit smooth active-set-change example disproves the equivalence. |
| 5. Regularity row overstates Holder theorem | The table identifies weighted Chebyshev regularity or coordinatewise Lipschitz dependence and explicitly restricts the Holder inverse-square claim to beta=1. Prose gives the full beta rate. |
| 6. Product kernels unavailable to ordinary module | Corrected: normalized interval-positive tensor certificates involve generator products; globally SOS products remain available. |
| 7. Grid baseline implies inverse-square affine recourse | Fixed and affine grid exponents are stated separately as r^-2 and r^-1. |
| 8. Abstract block-count exaggeration | Abstract block-count comparison omitted; body retains exact v+1 versus up to 2^v counts. |
| 9. All constants explicitly numerical | Replaced by finite-order parameter dependence; discussion names coefficient, geometric, and regularity dependence. |
| 10. Provisional constrained lift comparison | Removed the unverified dense/lift comparison and those introductory citations. The introduction states the proved displacement and global-repair mechanism instead. |
| 11. Grid subtraction gives lower bounds | The explicit grid optimum minus proved error lower bound appears in both introduction and discussion. |

The additional structure-review finding about the scope of `2 E_{2r}(h)` is resolved as described above. Box boundary dual attainment, recourse equality with strict-level certificates only, and the primal-only constrained conclusion remain distinct. Private convex rounding is described as a bounded increase in objective, not absolute closeness, because conditional means can improve the objective.

## Attribution and integration

No literature research was conducted. Drafting used `LITERATURE-PRELIMINARY.md`, the architecture, the theorem audits, and the supplied source notes. The known provisional Guo--Wang, Peyrl--Parrilo, and Davis--Papp citation aliases in the owned files were replaced by the canonical keys supplied by Luna. Other existing draft keys and their exact source locators remain for the bibliography owner and final integration; this revision makes no unsupported negative search claim or broad priority claim. The sparse-preordering inverse-square rate is explicitly attributed to the earlier lecture slides. The ordinary contribution is described as the exactly consistent finite-order sparse transfer and coefficient normalization. Partial-degree convex hierarchies and rational SOS recovery are treated as established methods.

The theorem references were compared with current Sections 3--6 and the accepted audits for Sections 7--9. This reviewer did not edit those sections. The regularity section and complete bibliography are being integrated by their owners, so no final bibliography/reference resolution or submission PDF claim is made here.

## Targeted verification actually run

A focused inline Python command read only the four owned TeX files. It checked final newlines, absence of trailing whitespace, balanced nonescaped grouping braces, and properly nested LaTeX environments. All four files passed. It then checked that the existing setting repair markers remained present and that the revised front contained the Archimedean, beta-one, SOS-product, grid-subtraction, local-measure, and dummy-coordinate scope statements, while the identified false formulations were absent. Both focused scope checks passed.

Targeted `cat`, `sed`, and `rg` reads were used to inspect the owned files, the review evidence, and the relevant existing theorem statements. The proof claims were checked against the accepted audits; no experiment, historical checker rerun, numerical solve, project-wide verification, CI inspection, or commit was performed. A full build is reserved for root's final integration once all sections and the bibliography are available. These targeted document checks do not establish mathematical correctness by themselves or substitute for the independent theorem reviews.
