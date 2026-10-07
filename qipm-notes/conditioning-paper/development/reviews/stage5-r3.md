# Stage 5 independent review — reviewer 3

## Decision

No major or minor issues identified in the completed Stage 5 material. The numerical package reproduces independently from its bundled inputs, the exact certificates establish the stated instance hypotheses, and the manuscript clearly distinguishes certified input facts from finite-precision spectral observations.

I read the abstract, introduction, numerical section, discussion, README files, Makefile, reproduction programs, provenance manifest, generated tables, and Stage 5 author record. I did not read other current reviewers' reports. No manuscript or shared generated output was changed during verification.

## Isolated reproduction

I copied the entire reproduction package, excluding bytecode caches, into:

`/tmp/conditioning-r3-stage5-w8uynzgu`

I created empty `figures/` and `tables/` directories there and ran:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /workspace/local-home/miniconda3/envs/qipm/bin/python repro/reproduce.py
```

The isolated run finished with `All reproduction checks passed.` No network or parent-repository import was needed. Comparing the new and supplied manifests found **no artifact hash differences** across their recorded inputs, scripts, numerical outputs, tables, and figures. Thus the empty-output-directory run regenerated the complete numerical artifact set, rather than merely reading the supplied figures.

Netlib accepted counts reproduced as 14/27, 19/27, and 12/27. Last accepted gaps were approximately `3.3393612069e-6`, `1.3995337102e-8`, and `0.6799205298`. Synthetic CG stopping iterations reproduced as 43, 71, 96, and 124. At the deepest test its recursive residual was about `2.9498312320e-9`, true residual `2.5184064628e-8`, and relative energy error `8.5488267705e-9`, matching the manuscript's distinction between contracts.

## Independent certificate and provenance checks

In addition to running the package verifier, I wrote an independent Fraction-based check directly against each frozen JSON input. It did not import the package's rational helpers. For all three instances it verified:

- the strictly positive rational point satisfies every equality exactly;
- the rational primal upper-bound point is nonnegative and exactly feasible;
- the rational dual lower-bound point has nonnegative slack in every coordinate;
- the compactness/sublevel certificate has strictly positive margin;
- the stored objective bounds equal the independently evaluated rational primal and dual objectives.

The independently calculated objective bracket widths were:

| Instance | Width |
|---|---:|
| afiro | `8.1596928010e-12` |
| sc50b | `9.3973813292e-12` |
| adlittle | `4.4338481164e-7` |

I also checked the original MPS and cached `.std` file hashes against the available source cache: all six matched the provenance record. Independently loading each cached sparse standard-form matrix and comparing it with the frozen JSON showed exact float64 equality for every A, b, and c entry. Ordinary reproduction does not depend on that cache; these checks strengthen the provenance evidence for the bundled frozen representations.

## Numerical and mathematical contracts

The compactness certificate is mathematically sufficient: the positive vector `A^T y+eta c` bounds every nonnegative coordinate on an upper objective sublevel. Eta zero certifies boundedness of the whole feasible set, and eta one certifies bounded objective sublevels. Together with strict feasibility and a finite rational dual lower bound, the latter supports the stated localization use.

Rational repair solves a verified square column subsystem while fixing the other coordinates to their binary-rational values. The resulting equality checks are exact. Optimal-gap brackets are formed by exact objective arithmetic before float export, avoiding subtraction of two poorly resolved floating-point objective values. Positivity and repair size are separately screened. The subsequent nullspace, decrement, and factor-SVD calculations remain numerical, as the prose says.

The factor SVD gives the eigenvalues of the reduced log-Hessian by squaring singular values and avoids forming the normal matrix. The resolution threshold is correctly described as an indicator, not a rigorous singular-value enclosure. All attempted rows are retained, and no asymptotic exponent is inferred from accepted Netlib curves. The very limited resolved adlittle tail is stated rather than hidden.

The high-precision CG reference uses the actual symmetrized float64 matrix and RHS, interpreted as exact binary rationals, rather than the ideal prescribed eigenvalues. Its reference solve is independently residual-checked at 80-digit precision. The final energy-error denominator is the zero-start solution energy `u_exact^T rhs`, and its numerator is the actual error quadratic form for that rounded matrix. The history's ideal-spectrum diagnostics are explicitly subordinate to the final reference values. Counts exceeding dimension are correctly interpreted as a floating-point phenomenon, not as a violation of exact-arithmetic CG termination.

The analytic-example numerical formulas agree with the reviewed mathematics: stable determinant-based small roots, the Frobenius generalized Hessian factors, phase-subsequence projection, and distinct residual/direction ratios. Their computations illustrate proved results and do not bear the burden of proving the asymptotics.

## Exposition and integration

The introduction makes the fixed metric, reduced primal operator, finite barrier parameter, and primal-gap conventions explicit. Its novelty statement is specific and qualified, while the prior-work discussion recognizes same-point comparisons, sublevel geometry, classical gap parameterization, LP endpoint theory, the classical fractional SDP construction, and oscillatory-barrier antecedents. The abstract and discussion remain consistent with the developed theorem package and avoid an end-to-end quantum lower-bound claim.

The reproduction instructions distinguish the definitive frozen arrays from an optional reconstruction using the original presolver. Anonymous author metadata is not invented. Internal development records are excluded from the manuscript/reproduction requirements. I found no stage placeholders or unsupported numerical precision claims in the reviewed final-facing material.

No corrections are requested from this review. The prescribed whole-manuscript review remains the next independent check.
