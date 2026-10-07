# Stage 3a, round 1 — independent reviewer 2

Reviewed `sections/06-coherent.tex`, `sections/07-scalar-realizations.tex`, the extended accuracy range in Section 3's norm-sensitive overlap theorem, and `audit/stage3a-author.md`. I did not read other reviewers' reports and did not change manuscript files.

## Findings

1. **Minor — malformed norm-tree summation subscript.** In Section 7, immediately before `eq:tree-center`, the product barrier is written with `\\sum_{v\\ {` followed by `m internal}}`. This compiles, but prints an unintended mathematical string instead of identifying internal vertices. **Fix:** use `\\sum_{v\\ \\mathrm{internal}}`, or explicitly define the internal-vertex set and sum over it.

2. **Minor — qualify the symmetry argument in the padded norm tree.** The proof of `eq:tree-center` says automorphisms are transitive at each depth. That is true of the complete tree with all D leaves free, but fixing only the padded leaves to zero generally breaks the feasible problem's automorphism group. The center formula is nevertheless correct. **Fix:** first establish stationarity and uniqueness for the full D-leaf norm ball. Its center has every leaf equal to zero, hence lies on the padded-leaf affine slice and remains its unique minimizer by restriction. Alternatively, compute the individual tree-variable derivatives at the displayed point directly. This avoids relying on symmetry that the padding constraints do not preserve.

3. **Minor — avoid reusing the failure-probability symbol for vector error.** In the sampling-output subsection, the text first uses `epsilon_v` for relative vector error, then switches to `zeta` in the paragraphs beginning “If the sampler is promised relative vector error” and in the conditioning/generic-feasible-sample comparisons. Section 1 and the cited scalar-overlap bound already use `zeta` for failure probability. This is particularly confusing in a subsection whose main purpose is to distinguish approximation error from unflagged failure. **Fix:** consistently use `epsilon_v` (or another dedicated vector-error symbol) there, retaining `zeta` for failure probability. State that the choices `p=Theta(epsilon_v)` and `p=Theta(epsilon_v^2)` are for sufficiently small vector error relative to the fixed source gap, as required by the preceding perturbation inequality.

No major findings. The formulas and lower/upper reductions checked below are valid under the stated source and access contracts.

## Coherent section

- Checked the specialization of CGJ full-version Theorem 33 against `/tmp/qipm-cgj.txt`: c=1/2 gives the displayed alpha kappa block term, square-root-kappa preparation term, logarithms, and sufficient encoding accuracy. Squaring an epsilon/3-relative norm estimate gives the required relative inverse-form estimate.
- The three-dimensional lower family has the claimed exact condition and separated relative intervals. Only one interior scalar block changes; the completion distance is O(epsilon/(alpha kappa)). The hybrid argument also covers inverse, controlled, and adaptive queries. The one-entry bypass is valid and correctly prevents transfer to exact sparse-value access.
- The single-transform probability error and amplitude-estimation cost are correct. The interior Bernstein obstruction applies to the real part of the complex polynomial and to bounded Laurent transforms; the text correctly limits its conclusion and does not apply it to variable-time or rational algorithms.

## Cyclic clock and oracle simulation

- Re-derived the orthogonal gauge and inverse geometric series. Even cycle length gives both endpoint singular values and exact condition K. Orthogonality of clock positions gives `R^2=K(1+gamma^(3T))/(1-gamma^(3T))`; segment summation gives `p=z/(1+z+z^2)`.
- The matrix and Hessian row/column supports are disjoint across clock regions. Transition norm one gives exactly the public row masses shown in the manuscript. All locations and squared-magnitude samples are public; values need at most one source-sign query. The same holds for `M^T e`, and its support is disjoint from the plateau readout.
- The allowed-length rounding has bounded gaps, so the delta, plateau mass, inverse norm, layer count, and dimension relations hold uniformly for K>=3 and sufficiently small delta.
- The scalar readout has norm 1/R and overlap sqrt(p) Phi. The accumulator has the stated sparse incidence and no hidden coefficients. Exact feasibility plus objective gap tau implies scalar error at most sqrt(K tau).
- Independently checked the fixed-k source promise and lower bound in [Bansal–Sinha, Theorem 1.3 and Corollary 1.4](https://arxiv.org/pdf/2008.07003). The high promise is positive, the low threshold is half the high threshold, and the fixed-k query exponent and logarithmic denominator agree with the manuscript. The clock uses k+1 Hadamard layers and preserves the construction.

## Public normalized tilt and affine LP

- Under the gauge, the inverse-transpose readout is a clock vector tensored with the unit vector `V^T|0>`. Its norm G is therefore public. The homogeneous recurrence before the plateau proves both the explicit lower bound on G and the plateau-restricted optimality bound. Together with the singular-value upper bound these give G=Theta(sqrt K).
- The normalized tilt has exactly squared value `5/4+(h/G)Phi`. Its optimal-value and squared-decrement signals have the claimed scale. The reduced right-hand side is a disjoint public-norm mixture, so direct Hessian/RHS SQ access does not leak the source amplitude.
- The box-LP diagnostic and its central-subproblem gap transfer are correct. Its optimal value is not confused with the ball/SOCP value.
- For the affine LP, invertibility forces `x=tM^{-1}e`; the unit objective gives value Rh|Phi|. The equality matrix's smallest singular value is preserved because the minimal eigenspace has work-space multiplicity at least two, leaving a direction orthogonal to e. Its maximum singular value lies between one and sqrt two. The resulting condition interval is correct.
- The extension of Section 3 to `0<epsilon<=R_e/2` is valid: its residual tolerance remains at most 1/8, and the second-moment/sample proof needs no epsilon<=1/2 restriction. The affine value application consequently has the stated matching exponential upper dependence, including when its absolute accuracy exceeds 1/2.
- The intrinsic interval barrier and decrement calculation are correct. The projected objective is explicitly not granted as an input oracle, so the equality-preprocessing interpretation is justified.

## Norm tree and sampling contracts

- The norm tree has the correct projection and cone count. The stated center, leaf Hessian `2(D-1)I`, zero leaf/tree cross block, and normalized-tilt decrement follow from the product barrier. The center proof only needs the minor padding clarification above.
- The projected norm perturbation bounds imply event probabilities separated by a constant times p when vector error is sufficiently small relative to the source gap times sqrt p. O(1/p) samples are enough; the resulting lower bound properly carries a p repetition factor.
- The manuscript distinguishes fresh unflagged failures, flagged retries, and reusable randomized setups, and charges setup in the latter contract. It does not obtain a per-draw lower bound by hiding preprocessing.
- The constructed-family classical and coherent history samplers have the asserted source-query counts. For the generic feasible-sample envelope, the polynomial gives an MP residual, normalization gives objective gap O(xi squared), and rescaling preserves the x-block sample law. The text correctly withholds free normalization and explicit feasible coordinates.

## Validation

`/workspace/local-home/miniconda3/envs/qipm/bin/python notes/scalar-newton-paper/scripts/verify_cyclic.py` passed. It checks cyclic spectra, the inverse history, public norms, readout/value/decrement identities, row metadata, norm-tree derivatives, and completion distance. The independent algebra above is the basis for the conclusions; finite numerical tests do not establish the theorems.

Attribution remains suitably qualified: the manuscript separates existing Forrelation/history, variable-time norm estimation, and cone constructions from the precise parameter/access/optimization refinements claimed here.
