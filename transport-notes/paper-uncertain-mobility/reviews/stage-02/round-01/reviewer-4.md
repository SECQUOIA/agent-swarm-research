# Independent review: Stage 02, round 01, reviewer 4

Reviewer: `paper_reviewer_4`. Date: 2026-09-07.

**Verdict: no major or minor issue requiring correction found.** The new section is acceptable at its present scope, subject to the coordinator's assessment of the other independent reviews.

## Snapshot and independence

Reviewed snapshot: `0d15634123d5c1e1db222f2d9fbea4cdaf77b36ccc1e523c39220fc0b71df943`. I independently recomputed the eleven file hashes in the manifest; all matched. I read the new local-baseline section, its handoff, the accepted model and transfer conventions, notation, and bibliography. I did not read other reviewers' reports or coordinator checks and made no manuscript edits.

## Independent mathematical checks

### Whole-line response and interval limits

The anchor estimate controls the core L² norm by the derivative energy and a fixed interval on which the potential is bounded below. Outside that core, the quadratic or quartic potential controls the weighted L² norm. This gives a source-tail bound proportional to `L^((1-p)/2)` by weighted Cauchy–Schwarz, uniformly for compact z or μ sets. It is valid for free endpoint traces as well as Dirichlet trials.

The proof of the Neumann upper limit uses the important missing ingredient in many informal localization arguments: tightness of the source integrals. Local H¹ compactness alone would not suffice for an integral over expanding intervals. Here the tail bound supplies it. The limiting function belongs to the whole-line energy space by the stated cutoff/mollification argument, and lower semicontinuity has the correct direction for the upper response bound. Uniformly comparable weights preserve these arguments; locally uniform convergence is sufficient to identify the limiting energy and source. No derivatives of those weights are required.

The bracketing rule has the correct directions. Disjoint zero-trace trials provide a lower response bound; freeing every interval's endpoint values enlarges the variational space and provides an upper bound. Discarding derivative energy on a rootless piece yields the reciprocal-potential integral. The corresponding Neumann partition lowers the spectral gap, as used later.

### Harmonic coefficient and pair scaling

I checked the kernel normalization independently. The quadratic form in the exponent of the Mehler kernel has determinant one; its double Gaussian integral is therefore `sqrt(2π/sinh(2t))`. Substituting `r=exp(-4t)` in its Laplace integral gives `sqrt(π) B((z+1)/4,1/2)/2`, hence the displayed gamma ratio. The cutoff constant sources converge in the dual energy norm, so the calculation does not apply an L² inverse to a non-L² constant.

For a quadratic zero `a x²`, the local scale is `(ε/a)^(1/4)` and the integrated inverse prefactor is `ε^(-1/4)a^(-3/4)`. Fixed local brackets followed by the curvature-tolerance limit prove the stated relative equivalent for a C² rate. The manuscript correctly makes no additive O(1) claim for the scalar approximation.

For the fold rate `(b x²-t)²`, balancing diffusion and killing gives `ell=(ε/b²)^(1/6)`, operator scale `ε^(2/3)b^(2/3)`, parameter scale `t/(εb)^(1/3)`, and integrated inverse factor `ε^(-1/2)/b`. These match the manuscript. The positive-μ pair consists of two wells of curvature `4μ`, so their combined coefficient is `C0 μ^(-3/4)/sqrt(2)`. The chosen neighborhoods have scaled radius tending to infinity and an exterior reciprocal-rate contribution smaller than that leading order. The negative tail follows from a derivative coefficient `a^(-3)` and the limiting reciprocal integral `π/2`; the trial's derivative energy is finite. Therefore the pair response is q-integrable exactly for q>4/3.

### Uniform cosine estimates

The exact coordinate `y=2sin(x/2)` gives the stated rate and Jacobian near the fold. At b=1/2 the amplitude is `2ε^(-1/2)` and the offset scale is `(ε/2)^(1/3)`. Comparable coordinate weights and the expanding-interval lemma justify compact-parameter convergence.

On the separated side, root distance is of order `sqrt(t)`, harmonic width is `(ε/t)^(1/4)`, and their ratio is `(t³/ε)^(1/4)`. Fixed-relative neighborhoods produce the envelope and gap for large ratios; bounded ratios belong to the compact fold regime. The complementary potential bound `t²` dominates `sqrt(εt)` when t³≥ε. On the rootless side, `k≥ν²+(1-cos s)²` directly yields the claimed gap. The reciprocal-rate integral gives `ν^(-3/2)` outside the inner fold layer.

For the sharp matching, choosing `eta=(ε/t³)^(1/8)` makes the scaled interval radius tend to infinity. The complementary response divided by the leading response is at most `(ε/t³)^(1/4)/eta=(ε/t³)^(1/8)`, which tends to zero. This establishes sequential uniformity, not merely pointwise matching. The text correctly separates that result from compact-μ convergence and from whole-line rootless tails.

### Disorder moments and limiting random variable

The subcritical inside domination is `t^(-3q/4)`. The outside estimate becomes the same integrable exponent after multiplying by ε^(q/4), since `z^(3/4)(1+z)^(-3/2)` is bounded. Thus the beta coefficient includes exactly the density factor 1/4 and two ordinary roots.

Above the critical order, the two folds contribute the product `2 × (1/4) × 2^q × 2^(-1/3)=2^(q-4/3)`. The q-integrable rescaled envelope justifies integration over growing parameter ranges. At q=4/3, each inside fold contributes `(2C0)^(4/3)ε^(-1/3)/(8t)` to leading order. Both folds and the cutoff down to order ε^(1/3) give `(2C0)^(4/3)/12`, equal to the displayed `2^(1/3)C0^(4/3)/6`. The retained interval with b<1/3 plus its controlled omitted logarithmic fraction proves this coefficient without an unjustified interchange of compact-fold and large-μ limits.

The mean identity follows from the beta–gamma relation. Its square has order ε^(-1/2), lower than the second moment's ε^(-2/3), so the variance coefficient is correct. The squared coefficient of variation has order ε^(-1/6). Inverting `W=2C0(1-c²)^(-3/4)` for |c|<1 gives the displayed tail law and coefficient `2^(-2/3)C0^(4/3)`. Half the offset interval is rootless, giving the atom of mass 1/2 at zero. This is an almost-sure limiting variable; it does not imply uniform integrability of high moments. All fixed-ε moments are finite by the positive-floor bounds.

### Stronger finite-bulk limit

I independently differentiated `(c+cos s)²` and symbolically checked the residual in `k''=2(1-c²)+6c(c+cos s)-4(c+cos s)²`; it is zero. Multiplication of `-εh''+kh=1` by kh gives `||kh-1||₂²+ε∫k|h′|²=(ε/2)∫k''h²` after using `∫kh=P`. The sign and factor one-half are correct.

Combining the energy and spectral estimates gives `||kh-1||₂² ≤ CεJ[(1-c²)+/λ+λ^(-1/2)]`. For t≥0, its two terms are bounded by `ε^(1/4)t(t+d)^(-5/4)` and `ε^(1/2)(t+d)^(-1)`, both at most a constant times ε^(1/6) because d=ε^(1/3). For t<0 the bound is `ε(|t|+d)^(-5/2)≤ε^(1/6)`. Taking the square root yields the claimed uniform ε^(1/12) rate.

The Neumann bulk problem is compatible because integrating `-Db Δf0=u-V` yields `-Db∫∂n f0=KPV`. The limiting load has exactly this boundary sign. The Schur penalty is nonnegative, giving the upper bound from the unpenalized bulk supremum. The accepted C² domain, L² bulk source, and constant Neumann datum give H² regularity; consequently the tangential derivative of the trace is square-integrable. Testing the surface penalty with that trace costs O(ε), giving the lower bound at the stated rate. The proof therefore establishes an error relative to the exact scalar J, not relative to its leading local approximation.

The uniformly bounded bulk correction transfers all fixed positive moments with the χ powers given in the text. For q>1, `E J^(q-1) ≤ (E J^q)^((q-1)/q)` makes the difference negligible compared with the diverging qth moment. For q≤1, subadditivity bounds it uniformly. Mean-square and second-moment orders also justify the variance transfer. The fixed positive Db and fixed nonzero V restrictions remain essential and are preserved.

## Physical interpretation, negative results, and citations

All calculations continue in the fixed dimensionless units established in Stage 01; uniform budget is M=2πε. The explicit instruction to substitute this relation in every power and logarithm prevents a hidden perimeter-factor error. Dimensional dispersion coefficients retain Stage 01's response conversion and χ prefactor. Disorder moments are consistently distinguished from particle-displacement moments, and no non-Gaussian tracer law or general central limit theorem is asserted.

For the Gaussian amplitude example, `∫g²=PR²/2` gives the constant-trial lower bound `2P/R²`, regardless of D or its dependence on the realization. Integrating against the Rayleigh density diverges logarithmically at zero amplitude. By contrast, the two-zero geometric sum `2R^(-3/2)` has finite mean and infinite second moment. The example lies outside the uniform rate-anchor assumptions, as explicitly noted, and disproves the proposed averaging inference without contradicting the bounded-family theorem.

I checked the marked-zero calculation against the [author-hosted Azaïs–Wschebor draft](https://www.math.univ-toulouse.fr/~azais/styles/other/student/level.pdf), Theorems 6.2 and 6.4, printed pages 121–122. The stated Gaussianity, almost-sure C¹ paths, nondegenerate point value, and simple zeros on a neighborhood of the observation interval meet its first-moment hypotheses. Taking the derivative as the auxiliary jointly Gaussian continuous field is permitted. Bounded continuous truncations of negative powers and monotone convergence justify the possibly infinite marks. Stationarity makes value and derivative independent; the zero-intensity bias changes the absolute normal slope to the Rayleigh density. The displayed `E S_L` coefficient and the diagonal lower bound `E S_L²≥L p_g(0)E|U|^(-2)=∞` are correct. No second factorial-moment theorem, multi-point nondegeneracy, independence of zeros, or stable-limit assumption is being smuggled into that conclusion.

For regularity, I checked [Guermond's author-hosted chapter](https://people.tamu.edu/~guermond/M661_FALL_2017/chap27.pdf), Theorem 27.23(ii) and Remark 27.24. They cover W²,p Neumann regularity on a C¹,¹ domain with the specified source and boundary spaces and explain the compatible pure-Neumann case. This supports the manuscript's use of the cited Grisvard section under the stronger accepted C² boundary assumption. The full Grisvard chapter was not independently obtained in this review.

Finally, `E k=4/3+cos²s≥4/3` makes the mean-rate response uniformly bounded by 3P/4 after discarding derivative energy. The realized uniform-design mean diverges. The conclusion concerns failure of averaging the coefficient before inversion; it does not claim that all forms of homogenization or disorder averaging fail. These limitations and the standard status of the oscillator and Kac–Rice ingredients are stated clearly.

## Findings and overall assessment

I found no actionable mathematical, scientific, citation, or exposition issue in this stage. The section is detailed enough to support later local design arguments, including the Neumann and moving-parameter estimates often omitted in informal treatments. The source and budget conventions are consistent with the accepted model. Final introduction, transport literature positioning, numerical pair-integral evaluation, and later optimal-design results remain assigned to future stages and are not required for this stage's acceptance.
