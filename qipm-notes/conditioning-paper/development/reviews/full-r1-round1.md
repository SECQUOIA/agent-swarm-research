# Full-manuscript independent review, reviewer 1, round 1

## Verdict

**No major issues identified. No remaining valid minor issues identified.** No correction is requested by this review.

This was a fresh assessment of the complete manuscript, including `main.tex`, `macros.tex`, all twelve sections, the bibliography, README, generated numerical tables and figures, and the reproduction package. Earlier stage reviews were context, not substitutes for the full review. I did not read the other current full-review reports or edit manuscript files. Particular attention went to the foundational geometry, width min–max formulas, uniformity over barriers, and localization; I also checked their downstream use throughout the manuscript.

The manuscript presents a coherent and mathematically supported contribution. Its principal result is the equal-objective-gap comparison of reduced primal Hessians through a common sublevel difference body, with explicit control for finite barrier parameter and approximate centrality. The diameter law, ordered spectrum bounds, examples, and solver limitations follow a clear chain from this result. The distinction between this contribution and classical same-point barrier geometry, LP endpoint theory, and SDP error bounds is sufficiently precise. The manuscript does not turn residual estimates into unsupported solution or quantum algorithm guarantees.

## Mathematical audit

### Setup, central paths, and basic barrier consequences

I checked `sections/02-setup.tex`, including the differential definition of a finite-parameter barrier, the Dikin and semiboundedness arguments (`lem:standard-containment`), and `prop:gap-parametrization`.

- The fixed relative affine space and fixed Euclidean metric make all later eigenvalue comparisons meaningful. The nonconstant objective rules out the zero objective direction on that space.
- The one-dimensional self-concordance argument correctly yields the curvature estimate used to prove Dikin containment, including closure at local distance one. The semiboundedness proof uses the barrier-gradient inequality in the correct direction.
- The support inequality `eq:objective-support` applies at arbitrary interior points, as needed later for approximate centers.
- Compactness and boundary divergence justify existence and uniqueness of the central minimizers. Differentiation gives a strictly positive gap derivative. Integrating the reciprocal-gap inequality toward the analytic center gives the stated lower comparison between gap and path parameter; the upper comparison follows from semiboundedness. The notation for the gap-parametrized path is consistent with the distinction between a barrier parameter and the central-path parameter.

### Sublevel geometry, equal-gap comparison, and uniformity

I independently checked `sections/03-geometry.tex`, particularly `lem:approx-containment`, `thm:difference-body`, `thm:diameter-law`, `cor:uniform-rates`, and `prop:localization`.

- The approximate-centrality residual gives the claimed one-sided gradient inequality for every point in the lower objective sublevel. In the line proof, the selected threshold makes the derivative positive with the exact lower bound required to invoke semiboundedness; simplifying the resulting distance estimate gives the stated constant \(C(\nu,\rho)\).
- Both inclusions \(E_x\subset K_g\subset 2C E_x\) are valid. The first uses the objective-decreasing sign of each Dikin direction; it does not presume that the full translated Dikin ellipsoid lies in the lower sublevel. This distinction is important and is handled correctly.
- The directions of the two Loewner inequalities, their factors of four, and the resulting factor of sixteen in the condition-number comparison are correct.
- The maximum radius and centered inradius of the difference body yield the claimed aspect-ratio bounds. The chord argument yields the smallest-eigenvalue estimates with the stated constants. The contracted interior ball supplies the upper bound on the largest eigenvalue. Together these establish the two-sided diameter law rather than only an upper bound.
- The common small-gap interval for all barriers with bounded parameter is justified through the analytic-center objective gap and the containment constant. The uniformity assertion correctly requires the residual to remain bounded strictly below one. It does not claim uniform constants over arbitrarily large barrier parameters or varying problem geometry.
- The explicit canonical-barrier bound uses a strictly feasible primal point and the correct complementarity identity; it does not need LP nondegeneracy or SDP strict complementarity.
- Compact-sublevel localization is sound. The interpolation from an attained optimum to a relative interior point produces the required interior ball below the chosen level. Objective-decreasing rays relevant to the proof are bounded inside the compact sublevel. The replacement of the global objective range by the local level in the ball contraction is valid. The proposition carefully makes pointwise claims without assuming a global central path exists on the unbounded feasible set.

### Ordered spectrum and widths

I re-derived the stronger current formulas in `sections/04-widths.tex`, rather than relying on the earlier-stage version. With the manuscript's ordering of eigenvalues, the lower bound in `thm:radial-spectrum` follows by applying the pointwise reciprocal radial bound to the infimum-over-dimensional-subspaces form of Courant–Fischer; the upper bound follows from the supremum-over-codimensional-subspaces form. This gives exactly

\[
(w_j^+)^{-2}\leq\lambda_j\leq 4C^2(w_j^-)^{-2}.
\]

The order \(w_j^+\leq w_j^-\), its constant-factor converse, and the diameter/inradius endpoints are consistent. Repeating the argument for the maximum of the two directed exits gives the stated factor \(C^2\), rather than \(4C^2\). No interchange of the two min–max quantities or eigenvalue order was found.

### Classifications, LP limits, and SDP examples

I checked the downstream applications in Sections 5–7 against the preceding hypotheses.

- The error-bound dictionary correctly distinguishes a one-sided error bound from an attained diameter scale. The unique-vertex, positive-dimensional optimal-face, and curved-singleton regimes follow as stated.
- The simplex family separates fixed-instance asymptotics from uniform behavior as the cost approaches degeneracy. Its exact limiting Hessian calculation uses the affine-slice Gram matrix; the plateau constant and the two-parameter diameter bounds are consistent.
- The unique-optimum LP limiting Hessian is positive definite because the optimal support columns are independent. The active dual analytic-center description and the slack-weighted singular-value estimates use the correct support and the correct inequality directions. The compact degenerate example and the localized unbounded witness satisfy their stated feasibility and uniqueness properties.
- The paired SDP examples have the stated strict primal feasibility, unique optimum, and singularity degree two. In the first facial-reduction step, positive semidefiniteness forces the coefficients claimed in the minimality argument to vanish. Adding the two section constraints does not create an extra first-step exposing direction. The two examples therefore legitimately distinguish diameter exponents at equal singularity degree.
- The diameter lower witnesses and positive-semidefinite determinant calculation are valid. The exact central equations and the conversion between gap and path parameter agree with the Hessian asymptotics.
- The four SDP eigenvalue scales use the correct Frobenius metric, including the nonorthonormal two-coordinate Gram matrix. The leading constants for the two generalized eigenvalues and the final condition-number constants agree. Equal-gap Loewner comparison legitimately transfers the ordered scales to other fixed finite-parameter barriers.

### LP projectors, oscillation, and linear solvers

I checked Sections 8–10, including their limitations.

- The all-barrier LP cluster theorem uses classical logarithmic endpoint limits as a reference and then applies equal-gap comparison. The weak eigenspace has the optimal-face dimension. The general projector rate follows from a coercive bound on the orthogonal complement and bounded Rayleigh quotients on the tangent face; the logarithmic improvement uses the stronger matrix decomposition. The approximate-center extension is limited to the conclusions justified by the argument.
- The exact parameter-change Newton right-hand side is correctly identified. The statements about weak-subspace mass are norm statements with their squared-energy consequences distinguished. The conditional restricted-solve estimate does not assume access to a projector or imply an IPM convergence theorem.
- The oscillatory rectangle example globally certifies self-concordance and a finite parameter. The embedding metric differs from the coordinate metric by a scalar and therefore preserves the relevant condition numbers, angles, and relative errors. Along the stated subsequence, the eigenspace rotation and the weak/strong solution components have the claimed different orders. The relative solution-error conclusion follows despite a vanishing discarded residual fraction.
- The two-interval CG polynomial has the required normalization and bounds on both intervals. The degree estimate accounts for the growth of the lower-interval polynomial on the upper interval. Exact-arithmetic energy accuracy and finite-dimensional termination are correctly distinguished from finite-precision observations.
- The quantum discussion does not mistake the CG polynomial for a bounded block-encoding polynomial. The lower-bound interpretation includes the dimension dependence and does not claim that every LP quantum algorithm must depend on a reduced Hessian condition number.
- The fixed-coordinate, ambient-Hessian, Schur-complement, and augmented-system comparisons use the proper congruences. The objective-sensitivity formula applies to the explicitly fixed-data perturbation. The final counterexample has differential self-concordance but fails the finite global parameter inequality, so it appropriately demonstrates the role of that hypothesis without contradicting the main theorem.

## Prior work, novelty, and overall presentation

I checked the introduction, the local attribution surrounding the proofs, the discussion, and the bibliography together. The comparison to Nesterov–Nemirovskii's same-point symmetric-chord result is explicit. The distinction from Peña's central-gap parameterization and self-scaled Schur-complement bound is accurate. LP endpoint limits, fractional SDP error-bound phenomena, and classical clustered CG are not presented as new discoveries. The novel claims are qualified and attached to the particular equal-gap formulation, complete geometry-to-conditioning comparison, matched examples, and explicit finite-parameter sharpness construction.

For the oscillation antecedent, I independently read the cached primary Duistermaat manuscript `/tmp/conditioning-duistermaat.pdf` (Remark 2.3, printed page 4), using text extraction. Its discussion supports the manuscript's attribution of oscillation in suitably rescaled derivatives; the new example's more specific eigenspace and solution-error claims remain distinguished. The source comparisons checked in the prior stages were also reconsidered against the final wording; I found no strengthened claim unsupported by that evidence.

The abstract now says “at most two” LP spectral scales, matching the possibility of a zero-dimensional optimal face. The section order supports a standalone reading: definitions and the main comparison precede spectral widths and classifications, explicit examples precede solver implications, and the formulation limitations and numerical contracts are stated before the conclusion. The main claims in the abstract, introduction, and discussion agree with the detailed theorem hypotheses. I found no unresolved cross-reference, unexplained change of metric, unsupported novelty sentence, or gap between the front matter and the proved results requiring correction.

## Independent reproduction and build

I created an isolated standalone copy at `/tmp/conditioning-full-r1-t07gb9o0` containing the manuscript, bibliography, README, Makefile, sections, figures, tables, and reproduction package. I deliberately omitted `development/` and the surrounding repository. All numerical reruns and compilation occurred in that copy.

- `make reproduce PYTHON=/home/sgusev/miniconda3/envs/qipm/bin/python` passed all reproduction checks.
- Regenerated files under `figures/`, `tables/`, and `repro/results/` matched the submitted files byte-for-byte.
- The three Netlib accepted/attempted counts were 14/27, 19/27, and 12/27. The final accepted gaps and condition estimates agreed with the manuscript.
- The finite-precision CG experiment reproduced iteration counts 43, 71, 96, and 124. In the last case, the recursive residual was approximately \(2.95\cdot10^{-9}\), the independently recomputed true residual approximately \(2.52\cdot10^{-8}\), and the relative energy error approximately \(8.55\cdot10^{-9}\), agreeing with the stated residual-gap interpretation.
- `make` produced a 36-page PDF. The final LaTeX log contained no warnings, undefined references, multiply defined labels, or overfull/underfull boxes.

The numerical interpretation respects the code's contracts: exact rational certificates address the frozen standard-form instances and objective brackets; the singular-value resolution screen is not presented as a rigorous eigenvalue enclosure; rejected rows are retained; and the finite-range Netlib data are not used as proof of asymptotic exponents. The frozen-instance and optional data-preparation distinction is documented. The reproduction package is standalone at the scope claimed.

## Completion assessment

There are no outstanding corrections from this independent full review. The present manuscript is internally complete and scientifically defensible at the stated scope. This finding concerns the mathematical arguments, attribution, exposition, and reproducibility assessed here; it does not presume a particular journal's acceptance decision or replace author-supplied submission metadata.
