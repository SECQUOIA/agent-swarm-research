# Final full-manuscript review, round 1, reviewer 4

**Verdict: no major issues found.** I found one minor qualification needed in the introductory distance/count comparison. The final manuscript's theorem statements, proofs, numerical illustrations, and contribution claims otherwise form a coherent standalone paper in the stated movement model.

This was a full-manuscript review: I read the introduction, all main sections, all three appendices, interpretation, main/macros, bibliography, README, figure/data generation, and diagnostic/certificate code. I revisited the mathematical proofs rather than limiting this pass to the new introduction. I did not read other final-review reports or discuss findings with other reviewers. No manuscript, figure, or data file was edited. Figures were regenerated only in an isolated temporary directory.

## Minor finding

**Qualify the introductory count/distance comparison for integer rounding.** Location: `sections/00-introduction.tex:14–16`, “The minimum number of such moves is comparable to metric distance, with explicit constants depending only on R.”

Taken as a uniform multiplicative comparison, this is false for small positive distance: an endpoint at distance `D>0` tending to zero still takes at least one move. Corollary “Optimal bounded movement” correctly has the ceiling in its upper bound, so none of the actual theorems is affected.

**Repair:** say “The minimum number of such moves is controlled by metric distance, up to integer rounding, with explicit constants depending only on R,” or explicitly allow an additive one in the comparison. The asymptotic applications all have growing distances and need no modification.

## Mathematical review

### Metric benchmark and spectral scope

- Rechecked the forward-chord inequalities, their orientation in the starting norm, and the curve-attainment condition in the generic counting upper bound. The later exact spectral paths and compact allocation arguments provide attainment where used.
- Rechecked the real-Hessian calculation for complex rectangular matrices. The Hermitian dilation has two copies of each nonzero singular value and contributes exactly `2g''=b''`. The divided-difference formula and almost-everywhere spectral derivative argument cover repeated and zero singular values.
- The Jordan Peirce normalization agrees with the real and complex Hermitian specializations. The new reader definitions of primitive idempotents and Peirce spaces are useful. The differentiated inverse identity has the correct off-diagonal coefficients, including in the exceptional algebra.
- The ordered-spectrum contraction is used only where justified. Center-to-point paths and central subarcs have the required common ordered frames; no equality is inferred for arbitrary endpoints merely because they share singular values.
- Positive metric scales and standard-self-concordant scales are distinguished throughout. The least gradient parameter is rank times scale; inactive directions remain in the ambient metric but contribute zero to the objective gradient and central velocity.
- The exact target-set allocation has a strictly convex coercive objective, an active constraint, interior coordinates, and a unique positive multiplier. Alignment and removal of inactive coordinates work for signed Jordan objectives as well as rectangular matrix objectives. The logarithmic approximation and Lambert equation have the correct constants and domain restrictions.

### Sharp profiles, distribution laws, and finite sequences

- Rechecked the weighted prefix inequality, scale-order exchange argument, sharpness objectives, and the integrable step-profile approximation. The exact supremum is for prescribed ordered scales with separated activations; the tied-activation qualification prevents an overstatement.
- The scalar KKT dilation has the correct multiplier matching. Its exact scalar sharpness is distinguished from sharpness of the product arclength constant. Both rational bounds and every-maximizer localization are independent of numerical maximization or uniqueness assumptions.
- The rank/truncation hypotheses in the geometric and polynomial decay statements prevent invalid fixed-rank small-accuracy extrapolation. The determinant-certificate counterexample remains a valid exact-allocation witness even for the stronger certificate without the factor two.
- Rechecked exact dyadic rounding, the first-accuracy window, the two index ranges used by different lower bounds, and the ordinary bit-length claim. Summation by parts correctly controls accumulated rounding error in the length calculation.
- The finite-sequence proof uses actual initialization and accuracy to force net progress. Clipping and absolute progress increments allow arbitrary label order. The growing-tube assumption is sufficient for the terminal cutoff gap and the initial-progress estimate; the smaller diverging-overhead regime is derived with the correct denominator.
- The decrement-to-tube proof and conic residual transfer have the required norm directions. The conic distribution paragraph now explicitly requires the same restricted barrier, objective, and parameter. The unequal-scale subsection now explicitly fixes its weighted metric and compares identical endpoints when discussing the shortcut.

### Scalar and coupled barrier changes

- The normalized scalar differential inequality establishes ordered velocity, unit limiting speed, integrable tails, and a finite support endpoint. The nonconvex general target allocation uses only necessary conditions at an attained global minimizer and does not claim convexity or uniqueness.
- The relaxed scalar envelope now explicitly requires local absolute continuity. The two branch calculations, the strict bound below two, the unique maximum proof, and the relaxed extremizers are consistent. The stronger conclusion for a globally optimal smooth-profile minimax is not claimed.
- The smooth nonmonotone family is a barrier on a finite interval with full gradient range; its parameter diverges in the sharpness construction. This correctly separates it from a fixed normalized profile and from fixed-parameter comparisons.
- The canonical barrier calculations credit earlier constructions and exact dimension bounds. The spectral transfer concerns Hessian metrics and does not automatically transfer scalar self-concordance to arbitrary spectral lifts.
- The full-facet collar proof works before all other coordinates approach their boundary facets, and its same-accuracy lower bound follows from the strictly increasing central objective. The comparison path's bounded added curvature length is justified by total Euclidean variation.
- The dense and radial parameter calculations give exact parameter r. The new radial global metric bound, implicit scalar speed bound, and ordered-profile estimate yield the stated endpoint constant uniformly in dimension and the admissible coupling parameters.
- The radial accuracy proof uses an actual accurate standard center and a parameter enlargement; the direct transformed-coordinate length bound avoids an invalid reverse metric comparison. The same dyadic arbitrary-label argument remains uniform when coupling parameters vary with rank.

### Completion and changes of formulation

- The conjugate convention, differentiated central equations, and orthogonal primal/dual speed allocation are consistent. Rank-deficient equalities are handled by the tangent projector, with the inverse Schur formula confined to full row rank.
- The classical full gap-set proof genuinely addresses all feasible terminal certificates and ambient paths with possible intermediate affine infeasibility. The manuscript clearly credits this scope to Nesterov–Todd.
- The sparse completion theorem uses the same dyadic data and a finite full-central start. The primal target accuracy and full gap differ by the explicitly stated factor two. The primal central lower count uses the discrete potential, not just arclength. The full lower count applies to an arbitrary final feasible dual certificate.
- The exposed-minor covector has exactly the asserted ambient norm. Weighted AM–GM gives the stated alpha-dependent scale; arbitrary inactive eigenvalues and auxiliary fibers are allowed. The affine-slice sharpness limitation is explicit.
- The operational-face definition and compactness/dimension argument are now sufficiently explicit for the dimension-only theorem. Orthant restriction applies to coupled homogeneous barriers, and the integer factor-charge bound is correct.
- The grouped/packed Hessians retain the nonlinear residual's second-derivative contribution. Hadamard controls unrestricted off-diagonal completions. The centers, exact restricted parameters, source residual collapse, and path-length formulas are consistent.
- The norm-tree parameter calculation uses the exact root leverage, not a guessed subtraction of the fixed root's homogeneous degree. Both limiting configurations and the Schur-complement estimate are valid. The heterogeneous scale now includes the common factor for equal nonunit objective weights.

## Cross-section claims, attribution, and presentation

The abstract and introduction distinguish endpoint distance, distance to the entire accurate set, and full primal–dual feasibility. They do not identify the figure's endpoint distance with the exact target allocation. The finite start used in the completion theorem and second figure is stated locally and differs only by the proved bounded primal prefix from analytic-center initialization.

The qualified novelty paragraph enumerates specific comparisons and constructions rather than claiming that central-path inefficiency, scalar metric flattening, spectral differentiation, canonical barriers, or classical primal–dual geometry originate here. Its distinction between the sharp prefix realization and the classical Lorentz inequality is appropriate. The role of an explicit radial family versus general facet-regular couplings is also retained.

I independently checked the primary descriptions of the newer neighborhood literature:

- [Allamigeon–Benchimol–Gaubert–Joswig](https://arxiv.org/abs/1708.01544) establishes exponential logarithmic-barrier path-following lower bounds and exponential curvature. The introduction credits those antecedents rather than treating the new dyadic example as the first inefficiency result.
- [Allamigeon–Gaubert–Vandame](https://arxiv.org/abs/2201.02186) gives the barrier-independent lower-bound result in its prescribed path-following framework. The manuscript appropriately contrasts this with its own specified metric and radius contracts.
- [Allamigeon–Dadush–Loho–Natura–Végh](https://arxiv.org/abs/2206.08810) defines straight-line complexity using affine segments in a wide neighborhood and compares methods across barriers. That resource is correctly distinguished from bounded starting-local-norm moves. The [published journal record](https://epubs.siam.org/doi/abs/10.1137/23M1554588) confirms the 2025 bibliography metadata.

The exact-comparison mechanism is explained before the technical proofs, the road map accurately describes the sections, and the appendices isolate lengthy finite certificates and formulation calculations. I found no theorem relying on an unresolved development note, inaccessible repository-local result, or numerical plot as its proof. The manuscript and README contain no remaining stage placeholders. Additional front-matter details may depend on the eventual journal, but I found no mathematical or scientific completeness issue requiring further development.

## Independent checks and artifacts

- Re-ran all four verification scripts with `/home/sgusev/miniconda3/envs/qipm/bin/python`. Every exact rational assertion and all diagnostic checks passed.
- Added an independent diagnostic outside the manuscript files for 60 complex rectangular matrix points/directions, including repeated and zero singular spectra. Direct real-Hessian finite differences agreed with the matrix formula (maximum absolute discrepancy about `7.44e-6`), and the spectral-speed contraction held. This specifically checks the complex-real metric convention rather than only scalar profiles.
- Regenerated both figures and all eight CSV rows in `/tmp/final-review4-figs-dv7a5h4v`; the checked-in CSV reproduced within `rtol=1e-11, atol=1e-10`. The largest reported relative quadrature estimate was about `3.59e-12`. These remain numerical illustrations, as the captions and README say.
- Inspected both rendered vector figures. Axes, legends, and labels are readable; the first uses equal metric-coordinate aspect and the captions state the endpoint contracts accurately. I did not duplicate the root's all-page visual audit.
- The current LaTeX log reports a 50-page output with no undefined references, warnings, or overfull boxes. I avoided rebuilding in the shared output directory. README/build paths are local to the paper folder, and prebuilt figures remove a Python dependency from manuscript compilation.

No further mandatory minor issue was identified. Correcting the introductory rounding qualification does not require changing any proof or rerunning the mathematical diagnostics.
