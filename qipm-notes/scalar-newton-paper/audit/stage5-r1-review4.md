# Whole-manuscript review, round 1, reviewer 4

I independently read all eleven section files, `macros.tex`, `main.tex`, and the bibliography. I did not read the other whole-manuscript review reports or change the manuscript. The principal emphasis of this review was Section 10, with a separate check of its compatibility with the earlier oracle and output contracts.

## Verdict

No concrete major or minor issue was identified. No correction is requested by this review.

The results are conditional query/arithmetic statements, with several explicitly unmatched general regimes. Those limitations are stated consistently in the abstract, introduction, individual theorems, and conclusion; they are not missing hypotheses or unfinished proofs of the claimed results. In particular, the paper does not claim a general end-to-end quantum interior-point advantage, a uniform finite-bit implementation, a product of independently established lower bounds, or free acquisition of iterate-dependent sampling access.

## Structured-system checks

- The identity for the inverse small core uses neither invertibility nor positivity of the correction matrix. Its norm bound follows from the supplied Loewner lower bound and the projection identity for the full-row-rank sparse base. The perturbation estimate for the core and the subsequent vector-error allocation are consistent.
- The entrywise estimates of the small Gram matrix and right-hand side start from the supplied source vectors. Their second moments, conversion from entry errors to matrix/vector errors, polynomial biases, and union-bound cost are sufficient. Both directions of access to the one-entry maps are explicitly required.
- The raw sampler correctly handles rectangular or singular transforms. The mixture and second rejection step give a raw output mass proportional to the squared coordinates of one fixed vector. No small correction-column norm is divided out. The good-setup acceptance bound, setup checks, finite draw cap, and conditional exact sampling law agree with the advertised output contract.
- The scalar corollary uses a tighter vector tolerance and an independent right-hand-side importance estimator. Its baseline and second-moment bounds suffice for relative error without assuming positivity of the approximate map.
- The Lorentz inverse eigenvalues, signed correction, and comparison factors are consistent. For generalized-power cones, I checked the normalized Hessian, the determinant and trace of its two-dimensional restriction, the clipping interval, the inverse-core derivative, and propagation of its estimated coefficient error to the final inverse solution. The separate block norm access and supplied barrier scalars are material and are stated in the corollary.
- The geometric-mean obstruction simulates classical SQ and a specified coherent preparation completion with constant hidden-bit overhead. The relative-error construction separates adjacent possible scalar values and explicitly charges its growing logarithmic coordinate range.
- The profile preconditioner yields the stated spectral interval and energy certificate. Its signed small core is nonsingular, and its setup/application counts include sparse-base formation, transformed update columns, the dense core, and vector work. The rank lower bound is restricted to its stated base-plus-update witness family; it is not presented as a universal oracle lower bound.
- The one-hub augmentation is nonsingular under the stated full-row-rank condition. Doubling graph vertices covers its row-column bipartite graph. I checked the cited tree-decomposition preprocessing and solve theorem directly in the primary [Fürer–Hoppen–Trevisan paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol351-esa2025/LIPIcs.ESA.2025.116/LIPIcs.ESA.2025.116.pdf): Section 3 gives the nice-decomposition conversion with the claimed cost and number of nodes; Corollary 3 gives the required single-right-hand-side solve. The manuscript appropriately separates this result from reusable symmetric factors and numerical stability.
- The two-hub quasidefinite alternative, regularization error, coarse-graph construction, and final full-output comparison respect their stated additional hypotheses. The near-linear comparison charges explicit writes and requires uniform outer-algorithm assumptions.

## Other sections and integration

I checked the positive-form importance estimator, its complex-coordinate convention and support restriction, the relative polynomial error, and the norm-sensitive nonsymmetric variant. The two lower-bound mechanisms are kept separate. The single-form composition argument retains its concentration threshold and signal-to-baseline ratio; the explicit Jacobi and constant-path calculations connect those quantities to their respective regimes.

The coherent block lower bound uses an explicit completion and does not transfer it to exact entry access. The scalar optimization wrappers distinguish public unperturbed values, hard coordinates, tilted values, direct decrements, and the affine slice's hidden reduced objective. The temporal section states joint success and uses Boolean recovery only at an accuracy that permits representative outputs. The reuse section charges current residual testing, retains the normalized-checkpoint hypothesis in the volume argument, and does not turn a movement bound into an input-query direct sum.

The main rate table and conclusion accurately summarize those distinctions. The literature discussion identifies the established primitives and narrows the additional contribution claims to the parameterized statements proved here. I also consulted the repository's Chen–Goulart literature entry when checking the distinction between established cone algebra and the present sampling theorem.

## Validation

I ran `conda run -n qipm --live-stream make -C notes/scalar-newton-paper check`. All five diagnostic suites passed, including the 152 structured identities/comparison checks, 25 witness Jacobi realizations, and 25 constant paths. These computations support the algebraic review; they do not substitute for the proofs above.
