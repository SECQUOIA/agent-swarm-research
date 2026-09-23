# Independent review: Stage 07, round 01, reviewer 3

Reviewer: `/root/paper_reviewer_3`. Date: 2026-09-07.

Snapshot: `d383884b23d489bd685197e179c0e74be518161c6cf0575298800612eae383c0`.

I recomputed every file hash in the supplied manifest; all matched. I inspected the complete new introduction, numerical section, discussion, numerical driver and both imported root scripts, stored JSON, generated table rows, README, handoff, and literature audit. I compared the new claims with their accepted theorem prerequisites. I did not read other reviewer reports or coordinator-check files, delegate work, or change manuscript/data sources. Independent computations below were run without writing regenerated artifacts.

## Independent numerical verification

I independently rebuilt the uncertain-center operator with `scipy.sparse.diags` and solved it with `spsolve`, instead of using the driver's banded matrix solver. For all nine saved fields, I reconstructed face masses from stored mobility and mesh spacing, evaluated the original training quadrature, and recomputed the gradient and simplex tangent gap.

- All masses were nonnegative and summed to one to floating precision (largest displayed departure about 2e-16).
- All nine sparse-solver objective values agreed with the stored banded-solver values to relative error below 9e-15.
- All nine independently computed tangent gaps agreed with the saved values to about 3e-14 absolute or better.
- For the four primary 400-cell cases, the recomputed gaps were approximately 0.00168410677255, 0.00219498398582, 0.000437168422001, and 0.000143303275225 for eta 0, 2, 8, and 32, respectively.

I then independently re-evaluated all nine fields using 384-point Gauss–Legendre quadrature with the sparse operator. These values agreed with saved validation values to relative error below 2e-15. In particular, the deliberately underresolved eta=32, 200-cell, 24-node field evaluates to 12.094818219837405 on 384 nodes, an increase of 11.5703316314 percent over its training objective. Thus the stated negative example is reproduced by a separate matrix implementation.

I checked the analytical gradient with centered feasible directional differences at an interior 31-cell, eta=2 design. The predicted directional derivative was -2.969249681906008. Differences with steps 1e-4, 1e-5, and 1e-6 differed from it by about 3.17e-7, 3.15e-9, and 2.44e-9, respectively. The step dependence is consistent with truncation followed by floating error.

I reran the full main circle row at M=1e-3, q=1, 32768 half-wall cells, and 48 quadrature nodes per subdivision through the manuscript driver function. Uniform, predetermined, observed-trial, and ratio values reproduced the saved row exactly in this environment. I also recalculated all reported refinement ratios directly from the stored raw moment values; the only discrepancy is the minor last-digit rounding item below.

## Discrete model and certification scope

The circle finite-volume matrix has the correct face coefficient D/h squared, midpoint reaction, reflecting endpoints, and full-circle response factor 2h. Its offset averaging factor is correct: reflection in c reduces density 1/4 on [-2,2] to one-half integration on [0,2], and the Gauss interval Jacobian yields the `(hi-lo)/4` factor in the code. Every sampled field is renormalized to `2h sum D=M`, including the uniform field. The discrete constraint differs from the exact continuum integral at finite mesh and converges to it; the text explains this distinction instead of pretending the discretized resource is exact continuum quadrature for every shape.

The imported observed trial matches the displayed branch rule, radius, extent and continuum patch value. The extra normalization inside that imported function followed by the driver normalization is mathematically idempotent apart from floating roundoff. The imported graded formula uses distance to the fold sites and the exact piecewise-power normalization. Its critical and third-moment cutoff exponents match the accepted construction.

For the local problem, with p=hD the conductance is p/h cubed. Differentiating `h times 1-transpose H-inverse 1` gives the negative squared difference quotient shown in the manuscript. The exterior reciprocal response at a given center is `1/(L-z)+1/(L+z)`; averaging gives exactly the logarithmic formula in the numerical section. There is no unaccounted potential tail for the stated zero-exterior-mobility problem.

The tangent lower value follows from minimizing the affine supporting function over the probability simplex, giving `F(p)-g dot p+min(g)`. It bounds the finite-dimensional, finite-quadrature problem when evaluated exactly; the paper appropriately states that its floating evaluation is not an interval-arithmetic or continuum certificate. The saved eta=0 value below exact Cpl and the poor-scenario example reinforce this distinction. The larger-domain difference is much smaller than the optimization gaps, and the text explicitly avoids interpreting it as a rigorous truncation estimate.

The generated table entries match the stored primary rows. The numerical plotting code uses those same values, marks the circle curves as trials, uses the proved constants only for the relevant asymptotic guides, and does not substitute the third-moment graded trial for the new supercritical optimum. It does not compute or depict an unverified numerical S_q or global H. The described spatial, scenario, and domain studies are separate checks and are recorded in the JSON.

## New asymptotic trial arguments

For the unrounded mean trial, let Z0 be the integral of `|sin s|^(-2/5)` and ZR the rounded normalization. The ratio of the unrounded field to the rounded one is

`(ZR/Z0) ((|sin s|+R)/|sin s|)^(2/5) >= ZR/Z0`,

with ZR/Z0 tending to one. The quotient form therefore gives an upper response comparison by the reciprocal normalization factor, while the accepted unrestricted sharp lower bound applies to the unrounded admissible field. This proves the stated leading mean coefficient without assuming a uniform pointwise ratio at the singular fold.

For the distance-based critical field, normalizations both have leading term `4 log(1/R)`. On retained fold annuli the distance and sine profiles differ by a relative O(r_star squared), uniformly in R. The accepted endpoint and reciprocal-potential estimates control the omitted inner annuli, while the fixed outer region contributes only order a_R^(-2/5), one fewer logarithm. Taking the small-budget limit before shrinking r_star gives the same sharp critical coefficient. This argument does not claim the third-moment trial has the sharp supercritical constant.

## Synthesis, scientific interpretation, and literature

The abstract and overview table match the accepted moment exponents, logarithms, and exact/order distinctions. The supercritical coefficient and uncertain-center value are correctly described as attained variational minima. The generic extension is restricted to orders. Exact observation has a per-realization budget, bin observation has a per-bin budget, and the discussion does not turn these mathematical controls into an experimentally established independent adjustment of diffusivity, affinity, and kinetics.

The physical discussion preserves fixed positive bulk diffusivity, nonzero mean speed, stationary long-time dispersion, and the distinction between disorder moments and displacement moments. The numerical evidence is not presented as a simulation or verification of the full bulk–surface stochastic model. The information claims concern the specified noiseless bins, and the draft does not assert an arbitrary-noise or sensor-cost result.

I independently inspected the two closest cited stochastic-conductivity coefficient classes. Buttazzo–Maestre explicitly use a positive lower and finite upper conductivity bound and random forcing. Alphonse–Kunštek–Vrdoljak use two positive conducting materials and general risk functionals of random-load responses. Thus the narrow comparison made in the introduction is supported, and it is not erroneously applied to all mass-reinforcement literature. [Buttazzo–Maestre preprint, Section 2](https://arxiv.org/pdf/1002.2770), [Alphonse–Kunštek–Vrdoljak, introduction and equations 1–2](https://arxiv.org/html/2602.19869v1).

The literature positioning attributes compliance, measure relaxation, gradient constraints, rare-bifurcation selection, and quantized decision methods to prior work. Its positive contribution statements concern the proved singular transport laws and do not claim a universal first result. The literature audit records the older full-text access limits. I have not independently exhausted the literature or verified every bibliographic datum; no novelty guarantee follows from this review.

## Finding

### R3-01 — Minor: adjust the spatial-refinement percentage rounding

Location: `sections/07-numerics.tex:132–136`.

The saved q=1 predetermined-trial values give a relative change of 0.00015841231081359375 when moving from 32768 to 65536 cells at 48-node quadrature. This is 0.015841231081359375 percent, which rounds to 0.0158 percent at the precision used for the displayed 0.0159 percent. The remaining two spatial percentages and the scenario/domain statements agree with the data.

Remedy: use approximately 0.0158 percent (or give fewer significant digits, such as 0.016 percent). This does not affect any conclusion or claimed scale of numerical uncertainty.

## Verdict

No major issue found in Stage 07. Correct the minor percentage rounding before stage acceptance. The numerical implementation, independently recomputed objectives and tangent values, trial-asymptotic arguments, and scientific scope are consistent with the accepted mathematics. The separate whole-manuscript review remains necessary and is not replaced by this stage review.
