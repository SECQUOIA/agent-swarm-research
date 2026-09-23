# Stage 5, round 1: independent whole-manuscript review 1

I read `main.tex`, `macros.tex`, all eleven section files, and `bibliography.bib`. I did not read the other final-review reports. I reviewed the paper as a standalone manuscript, with particular attention to Sections 3–5, and checked the statements in the introduction, abstract, table, and conclusion against the later theorems.

## Findings

**Major issues: none identified.**

**Minor issues requiring correction: none identified.**

No manuscript changes are requested from this review.

## Mathematical checks

- Section 3: I checked the Chebyshev residual construction, the complex-valued importance-sampling identity including support restrictions, the sharp Kantorovich second-moment bound, the relative-error budget, the bilinear energy normalization, the sparse-transform raw acceptance law, the normal-equation solution error, and the finite-error coupling. The access and output contracts are consistent with the proofs. The polynomial-degree dependence is explicitly exponential rather than described as polynomial in conditioning.
- Section 4: I checked polarization, the shift and condition-number pads, the clock norm/sampling metadata, the bidiagonal constraint factor, the rational rounding budget and four-square factor construction, the finite-population two-sphere argument, the small-population branch, and the confidence lower bound. The distinction between a two-form reduction and a routine accepting an arbitrary supplied right-hand side is stated. The quantum counting comparison uses a specified coherent completion and does not transfer the general block lower bound to entry queries.
- Section 5: I checked the contrast accounting, the high-contrast compiler's linear-complexity outer problem, the distributional product's quantifiers and concentration constants, the witness measure and its second/penultimate orthogonal polynomials, the reciprocal-clock diagonal calculation, the constant-path endpoint formulas, and the restrictions on the cyclic/two-cluster/Schur constructions. In particular, with the stated `n >= 200`, the outer weights are legal, the Hoeffding failure is below 0.004, the mean scalar separation exceeds `14 epsilon d`, and the thresholding error fits within half that separation. The paper does not incorrectly multiply its separate lower families.
- Sections 6–7: I checked the three-dimensional hybrid lower bound, its entry-access exception, the bounded-polynomial obstruction, cyclic history normalization, plateau readout and inverse-transpose norm, value/decrement transfers, affine equality conditioning, norm-tree center and Hessian, and rare-event sampling budgets. The scalar quantum upper bounds are not represented as algorithms for producing dense feasible vectors.
- Sections 8–9: I checked the classical direct-sum simulation, scalar increment and predictor sensitivity/leakage bounds, dynamic norm acquisition, threshold saturation and XOR gap propagation, the fixed KKT ray, bounded-Dikin movement comparison, residual acceptance margins, the approximate-span determinant argument, and the certification/output counterexamples. The endpoint and trajectory statements do not imply unsupported per-iteration multiplication. Stored-vector and current residual costs remain explicit.
- Section 10: I checked the nonsingular small-core identity without assuming invertible `L`, the sampled-core biases and perturbation bounds, bounded rejection without transformed-column normalization, the structured scalar readout, Lorentz and power-cone normalizations, clipping interval and coefficient Lipschitz bound, scalar-acquisition obstruction, profile certificate/rank comparison, latent augmentation, and the distinctions between exact arithmetic, stability, scalar output, and explicit directions. The hypotheses of the cone corollary include block norms and the geometric-mean scalars that its proof uses.

I also reran the two diagnostics most directly related to my assigned emphasis, using the required qipm interpreter:

- `scripts/verify_classical.py`: passed the residual, complex/support moments, sharp variance witness, rejection law, and arithmetic-transfer checks.
- `checks/check_lower_identities.py`: passed 25 witness Jacobi realizations and 25 constant paths.

These computations support the algebra checks; the proof assessment does not depend on treating numerical tests as proofs.

## Primary-source checks

I independently opened the following primary texts during this review:

- Ben-David–Blais, [arXiv:2002.10809v2](https://arxiv.org/pdf/2002.10809v2), Definitions 33–34 and Theorem 35/proof. Their proof fixes a hard pair for the inner Shaltiel-free measure before simulating the outer function; the manuscript's fixed-pair/product-distribution use is supported. The minimax discussion supplies the outer hard distribution.
- Montanaro–Shao, [arXiv:2311.06999v3](https://arxiv.org/html/2311.06999v3), the matrix-function query framework and classical approximation-degree lower bound. The manuscript attributes the underlying mechanism and separately proves the full-SQ simulation and positive-form specialization.
- Bansal–Sinha, [arXiv:2008.07003v3](https://arxiv.org/pdf/2008.07003), Theorem 1.3 and Corollary 1.4. The positive-high promise, `2^{-5k}` threshold, fixed-`k` lower exponent, and numerical quantum query scale agree with the manuscript.
- Chakraborty–Gilyén–Jeffery, [arXiv:1804.01973v2](https://arxiv.org/pdf/1804.01973v2), Theorem 33. Its `c=1/2` norm-estimation specialization supports the displayed matrix and state-preparation costs and the stated encoding-accuracy requirement.

## Overall fit and scope

The paper has a coherent progression from relative inverse forms to access-preserving optimization outputs, temporal reuse, and structured classical comparisons. Its length reflects the requested comprehensive treatment; the introductions and scope statements make clear which sections share an interface and which introduce a different comparison. The rate table accurately separates the constructions and population restrictions. The novelty paragraph is qualified and attached to precise results; established polynomial, Forrelation, scalar-optimization, cone-algebra, and recycling ingredients are credited.

The unmatched generic sparse quantum regime, the unavailable full classical factor product, ideal-arithmetic assumptions, conditional iterate access, and missing general trajectory maintenance theorem are explicitly stated limitations of the claims. They are not gaps in the theorems actually proved. I found no cross-section inconsistency or unresolved mathematical defect that requires revision.
