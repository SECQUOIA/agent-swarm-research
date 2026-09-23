# Stage 5 independent review — reviewer 4

**Decision: no major issues found. One minor abstract correction is requested.** I did not read other Stage 5 reports or edit manuscript sources. All executed reproduction and numerical checks were confined to an isolated copy at `/tmp/conditioning-r4-stage5-p1l3aw/paper`.

## Scope and independent checks

I read the abstract, introduction, numerical section, discussion, paper README, reproduction README, reproduction code, Decimal reference solver, provenance metadata, new bibliography entries, and Stage 5 author notes. I compared the exposition with the established mathematical results from earlier stages.

### Standalone reproduction

The full reproduction program ran in the isolated copy using the configured qipm Python with single-threaded BLAS. Its regenerated hash map is identical to the supplied manifest for all **23** tracked artifacts. I independently recomputed the SHA-256 digest of every listed source and regenerated artifact; all agree with the manifests. This verifies the portable, bundled-input reproduction claim in the recorded environment. It does not claim identical numerical stopping counts on a different BLAS implementation, a limitation the README already states.

### CG reference calculation

To avoid merely rerunning the supplied reference solver, I separately implemented a **110-digit Decimal Cholesky solve** for the exact binary-rational rounded matrices and RHS vectors in `cg_systems.json`. This differs from the package's 80-digit Gaussian elimination. I recreated the float64 CG iterate at each stored stopping iteration and computed its residual and energy error from the Cholesky reference. All four results agree with the exported `cg.csv` values to their full float64 output precision.

In particular, the deepest matrix stops after 124 iterations with recursive residual about `2.95e-9`, true residual about `2.52e-8`, and relative energy error about `8.55e-9`. The manuscript correctly says that recursive stopping does not certify the requested true residual. It also correctly distinguishes the rounded matrix used by CG and by the reference solve from the prescribed spectral construction. The exact-arithmetic dimension bound is not misrepresented as a finite-precision bound.

The intermediate history's energy diagnostic uses the prescribed eigendecomposition; its README explicitly labels those as reference-spectrum diagnostics and gives precedence to the final rounded-matrix Decimal results. No table or theorem relies on treating the intermediate diagnostic as the exact energy error for the rounded matrix.

### Analytic examples

The fractional-SDP scalar computation uses the correct generalized trace and determinant for the nonorthogonal (b,g) coordinates. Both small roots are recovered through determinant division, avoiding subtractive cancellation. The independent trace-product generalized-eigenproblem check is part of the successful isolated rerun. At `g=1e-24`, the four normalized constants differ from one by approximately `(1.30,1.01,0.72,0.58)e-12`; the full and restricted gap-scaled condition numbers agree with their analytic constants at comparable accuracy. The plotted starting normalized constants are below 1.16 and inside the supplied vertical plotting range, so that range does not suppress the finite-gap deviations being shown.

The simplex bisection is correctly bracketed by zero and `3μ`, and the factor SVD avoids a normal-matrix eigenproblem. I compared its stored limiting constants with the cancellation-resistant formula `3 λ_max(L)^2/ϑ²`; the largest relative difference is about `3.1e-11` at `ϑ=0.001`, negligible for the displayed evidence. The smallest-gap samples approach the correct plateau. The compact degenerate LP decimals in the text agree with its final raw row and the separately specified limiting spectrum.

The oscillatory calculation uses the stable weak-eigenvector ratio `−b/(d−λ_weak)` and keeps the factor four in both solution components. Its exported forcing/gap limit and relative direction error agree with the proved formulas. The table explicitly warns that rounded values of one are not finite-gap equalities.

### Certified LP representations

The exact rational certificate verification passed for all bundled inputs. The checks establish positivity, equality feasibility, a boundedness certificate, and primal/dual objective brackets using the stated exact binary-rational interpretation of float64 data. The positive-η certificate correctly establishes bounded objective sublevels for adlittle, rather than global boundedness. The manuscript's theorem localization is therefore the relevant one.

The numerical acceptance logic matches the documented gap, centrality, equality, repair, positivity and factor-resolution thresholds. All attempted rows are retained. The singular-value screen is explicitly a numerical resolution indicator rather than an interval certificate; the paper does not claim a rigorous spectral enclosure. Accepted curves are not used to infer asymptotic classes. The frozen-coordinate metric and changed representation are disclosed before the benchmark discussion.

## Scientific claims and integration

The introduction prominently credits same-point chord/Hessian comparison, earlier sublevel conditioning analysis, objective-gap parameterization, classical LP limits, fractional SDP geometry, and prior oscillatory constructions. The remaining qualified priority claim identifies different-center equal-gap comparison and the accompanying quantitative statements. It is appropriately narrower than a claim to introduce geometric conditioning.

The discussion preserves the mathematical distinctions among a unique polytope optimum, a curved singleton, and a positive-dimensional optimal face; between degree-based upper error bounds and attained exponents; and between forcing residual and direction recovery. The final numerical section supports those proved distinctions and does not introduce new unproved asymptotic or quantum runtime conclusions.

I attempted to reopen the Duistermaat author PDF in this round, but the web tool returned HTTP 403. I therefore do not claim a new independent full-text verification of that source here; the explicit primary-reading record in the author notes and the earlier source audit remain the evidence for its precise locator.

## MINOR R4-1 — allow the single-scale LP case in the abstract

**Location:** `main.tex`, abstract: “For linear programs, every fixed barrier has two spectral scales”.

**Issue:** Theorem `thm:lp-all-spectra` correctly allows f=0, in which case all eigenvalues are at the strong scale and there is no weak cluster. Unique compact LP optima, including the manuscript's degenerate example, therefore have only one scale. The abstract's unconditional wording omits this case.

**Correction:** Change the phrase to “For linear programs, every fixed barrier has at most two spectral scales” (or “up to two spectral scales”). The existing convention for the zero weak projector handles the following sentence; no theorem or numerical change is needed.

## Outcome

Address the abstract wording before proceeding. This review identifies no major issue requiring another Stage 5 five-reviewer cycle. The required whole-manuscript review remains a separate final step.
