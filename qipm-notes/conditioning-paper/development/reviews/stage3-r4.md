# Stage 3 independent review — reviewer 4

**Decision: no major issues identified. One minor terminology correction is requested.** I did not read other Stage 3 reports.

## Review scope and evidence

I read all three submitted sections (`05-classifications.tex`, `06-lp-limits.tex`, and `07-fractional-sdp.tex`), the new bibliography entries, the author notes, and the earlier definitions needed to interpret the notation. I checked the derivations below directly. I also inspected the local primary text of Drusvyatskiy–Wolkowicz, especially Theorem 4.5.1, Example 4.5.2 and §4.7, and Alizadeh–Haeberly–Overton §4. The earlier independent literature review of Adler–Monteiro and Peña remains relevant. The integrated draft builds successfully.

## Mathematical assessment

**Classification and plateau.** The error-to-diameter estimate uses nearest optimal points and is valid on sufficiently small sublevels. The lower diameter bound follows from a segment attaining every intermediate gap. Only an upper conditioning rate is inferred from an upper error bound; the matching claims expressly require attained diameter growth. The finite-vertex argument works for a degenerate unique optimum. For the simplex family, the diameter constants are uniform and the projected objective squared norm is exactly `(2/3)(ϑ²−ϑ+1)`. The fixed geometry and uniform attained-gap result justify the barrier-family statement. The generalized limiting Rayleigh quotient has characteristic equation `3λ²−2(1+ϑ²)λ+ϑ²=0`; it gives the displayed eigenvalues, ratio and iterated `4/3` limit. No interchange of limits is used.

**Curved singleton.** The two-coordinate Frobenius Gram matrix is `2I`. Dividing the coordinate Hessian by two gives the listed eigenvalues, and their ratio is asymptotic to `1/(2g)`. The chord lower bound and distance upper bound are consistent with this direct calculation.

**LP endpoint.** The hypotheses imply strict primal and dual feasibility for the stated compact LP. The use of the classical centered endpoint is explicit. Complementarity converts the scaled reduced Hessian into the diagonal slack compression. The uniqueness argument gives full column rank of A_B without assuming |B|=m, and then proves positivity of the compression on ker A. The active-set maximization exists because pairing nonnegative dual slacks with a fixed positive primal point bounds them, and full row rank controls their multipliers. Its Hessian is strictly definite in the remaining multiplier directions. The singular-value bounds have the correct extremal directions. I checked the compact witness's feasibility, nullspace columns, Gram matrix, slack derivative equation, and selected root. The unbounded witness solves centrality exactly and has compact positive objective sublevels; it is correctly separated from the initial compact setup.

**Paired SDP geometry and facial reduction.** The principal-minor estimates give the claimed upper diameters. For the full-set lower witness, the determinant is `g^(3/2)(a/2−1/4)>0`, and the Frobenius separation is exactly `g^(1/4)`. The restricted witness gives a square-root lower bound. The optimum is unique because a zero second diagonal annihilates its row and then forces the third row to vanish. The two-step facial chain works for both displayed systems. A one-step certificate must have zero trace multiplier and hence zero first diagonal. PSD then annihilates the first row, forcing the relevant coefficients to zero; the third row eliminates the remaining off-diagonal coefficient. Thus only E22 is available at the first step. The same coefficient check makes the only optimal dual slack E22, so the failure of strict complementarity follows. The formulation qualifier is essential and present: the count concerns the displayed S3 cone optimality systems, including X22=0.

**Exact fractional spectrum.** Stationarity in b gives the displayed quadratic and positive root. Stationarity in g gives μ=q/q_g; q and q_g are positive on a sufficiently small tail. Symmetry eliminates the two off-block entries and mixed Hessian terms. For off-block directions, the factor two in the Hessian quadratic form cancels the factor two in the Frobenius norm, yielding A2⁻¹/b. For the (b,g) directions, the Gram matrix is `[[4,1],[1,2]]`. The scaled coordinate limits are `(6,−sqrt(2),1)`, the leading generalized eigenvalue constant is `(G⁻¹)22=4/7`, and `μ³ det K→4` gives the smaller constant one. Consequently the four ordered scales, both condition-number constants, and the restricted two-scale conclusion are correct. Equal-gap Loewner comparison transfers orders, while the text correctly reserves the leading constants for the logarithmic barrier.

## Prior work and presentation

The classical nested construction is explicitly present in Drusvyatskiy–Wolkowicz Example 4.5.2 and attributed to Sturm in §4.7. The manuscript does not claim that construction or quarter-power error geometry as new. The prior SDP Schur spectral analysis is explicitly distinguished by matrix and regularity assumptions. The qualified novelty claim names the four constants for this specified normalization and its all-barrier transfer; it avoids a broader first-result assertion. Source-access limits remain honestly recorded.

The distinction between a degree-based upper error exponent and its actual attainment is particularly clear. The paired examples establish the intended limitation without claiming a full characterization of SDP geometry.

## MINOR R4-1 — call μ the central-path parameter

**Location:** `sections/07-fractional-sdp.tex`, Theorem `thm:fractional-spectrum`, immediately before equation `eq:fractional-gap-mu`.

**Issue:** The phrase “its barrier parameter satisfies” refers to μ. Throughout the manuscript, the established barrier parameter is ν, while μ parameterizes centrality. Conflating them weakens an otherwise careful distinction and could be confusing precisely where explicit spectral constants are introduced.

**Correction:** Replace that phrase with “the corresponding central-path parameter satisfies” (or “the associated value of μ is given by”). No mathematical change is needed.

## Outcome

Address R4-1 before proceeding. This review identifies no major issue requiring another five-reviewer round for Stage 3. Later solver, numerical, and final synthesis stages remain outside this review.
