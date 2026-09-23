# Final manuscript review, round 1 — reviewer 3

Verdict: **no major issue found**. I found no mathematical correction or unsupported novelty claim requiring revision. One minor production issue remains: the PDF's bibliographic metadata are empty.

## Scope and method

I reread the complete integrated manuscript sources, including the introduction, abstract, conclusion, all theorem sections, and all three appendices. I checked the macros, bibliography, README, Makefile, all five Python scripts, figure captions, generated figure files and CSV, and the current 50-page PDF's text and metadata. I inspected both figures visually. The root is separately inspecting every PDF page, so I have not duplicated that complete visual pass. I read the source map and literature audit for provenance, but no other independent review report.

All numerical work used `/home/sgusev/miniconda3/envs/qipm/bin/python`. I did not install anything, change manuscript files, or rebuild in the shared paper directory. Figure regeneration ran in an isolated temporary output directory.

## Minor issue

### 1. Populate the PDF's existing bibliographic metadata

**Location:** `macros.tex:7` and the front matter of `main.tex`.

`pdfinfo main.pdf` reports empty `Title`, `Author`, `Subject`, and `Keywords` fields, although the manuscript already supplies a title, author, and keywords. This is a production omission, not a mathematical issue or a reason to withhold the manuscript from scientific review.

**Repair:** add a `\hypersetup` declaration with `pdftitle={The Cost of Following the Central Path}`, `pdfauthor={Sergey Gusev}`, and the existing keywords. A short subject is optional. Use the information already present; do not invent an affiliation or contact address. Rebuild and confirm the metadata with `pdfinfo`.

## Mathematical and cross-section assessment

- The metric conventions remain coherent across the paper. Positive scales suffice for the exact metric identities; the bounded-chord interpretation invokes standard self-concordance with the stated scale restrictions. The spectral contraction arguments allow arbitrary off-frame competitors, whereas equality is asserted only from the analytic center or for the appropriate common ordered frame.
- The closest-accurate-point allocation is strictly convex for the standard barrier. In the general scalar theorem the argument correctly uses existence and necessary KKT conditions instead of importing that convexity assertion. The scalar dilation constant is distinguished from the product comparison and from the different relaxed-envelope constant.
- The weighted prefix bound, its fixed-order realization, activation-order extrema, and the unequal-scale comparison have consistent hypotheses. The exact supremum does not accidentally require the exhibited finite weights to attain a limiting extremum.
- The objective-distribution estimates keep their normalization and truncation hypotheses. The dyadic construction and growing-tube result distinguish arclength from actual finite sequences, force terminal progress from actual accuracy, and permit arbitrary labels. The finite-start conversion used for the full primal–dual example changes the earlier primal estimates by only bounded terms.
- The normalized scalar and coupled-barrier results have the necessary scope restrictions. In particular, the radial upper bound concerns the explicitly specified family, while the general full-facet result is a lower construction. The discrete radial proof remains uniform when its allowed barrier parameters vary with dimension. The nonmonotone scalar construction has a growing parameter and therefore does not contradict the general parameter-dependent comparison.
- The negative-pairing conjugate signs, primal/dual orthogonal decomposition, and supporting-hyperplane proof for the entire feasible small-gap set are correct. The three-scale result fixes the initial full central point and permits every feasible terminal dual certificate. It does not replace a target-set lower bound by a calculation on one central endpoint.
- The exposed-minor contraction permits arbitrary inactive fibers. The weighted determinant scale and weighted AM–GM optimizer are consistent. The dimension bound uses the operational face and is explicitly a full primal–dual statement. For grouped, packed, and norm-tree formulations, the auxiliary variables remain free in the lower-bound proofs. Hadamard partial minimization and the positive-sheet norm-tree equations justify the stated centers. The exact tree parameter proof uses valid trial directions in both root cases. The heterogeneous scale correctly includes a common nonunit objective weight.

## Literature and originality

The final introduction accurately credits NT2002 for the entire feasible small-gap comparison, including intermediate affine infeasibility. It preserves the actual NN2008 endpoint estimate and acknowledges its separated target-set result. The Lorentz inequality, spectral differentiation, canonical barriers, and projection calculus are identified as antecedents rather than independent new discoveries.

I also checked the newly incorporated primary records for the [2018 logarithmic-barrier lower bounds](https://arxiv.org/abs/1708.01544), the [2022 arbitrary-self-concordant-barrier construction](https://arxiv.org/abs/2201.02186), and the [2025 straight-line-complexity comparison](https://arxiv.org/html/2206.08810v4). The introduction correctly distinguishes their path-following resources from fixed-radius local-Hessian movement. The qualified originality paragraph identifies specific comparisons and explicit constructions; it does not claim the first central-path inefficiency example or a new classical gap-set theorem. I found no evidence in the examined sources contradicting those bounded novelty statements.

## Reproduction and independent checks

All four delivered verification scripts passed again. This includes every rational scalar certificate, the weighted-order enumeration, radial implicit-center and Hessian diagnostics, and the primal–dual/formulation checks. I additionally solved 60 differentiated KKT systems with deliberately redundant equality rows using least squares; their primal and dual squared speeds summed to the cone parameter, and their tangents were orthogonal. Two separate norm-tree boundary families approached restricted parameters 3 and 4 in the root-leaf and all-internal-root cases, respectively.

I regenerated both figures and all eight CSV rows in `/tmp/review3-figures-c59hr_sb`. The regenerated CSV agrees with the delivered values to relative and absolute tolerance `1e-12`. The largest reported relative quadrature error estimate was approximately `3.59e-12`; the README correctly calls this an estimate rather than a rigorous enclosure. The stable transformed-coordinate formula is checked against independent integration and finite differences. The plots and captions distinguish endpoint distance, primal central length, and full central length, and explicitly state that the first plotted quantity is not the optimum over an entire accurate set.

The current build log contains no undefined-reference/citation warning or overfull/underfull box warning. The paper is standalone at the source/build level described in the README. The manuscript's organization, definitions, and interpretation are sufficient for an optimization reader, with the specialized Jordan and formulation details supported by explicit proofs and primary citations. Apart from the minor metadata repair, I found no unresolved issue requiring another mathematical revision cycle.
