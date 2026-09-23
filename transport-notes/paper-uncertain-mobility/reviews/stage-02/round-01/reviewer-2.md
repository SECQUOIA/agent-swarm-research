# Independent review: stage 02, round 01, reviewer 2

Date: 2026-09-07. Reviewed snapshot `0d15634123d5c1e1db222f2d9fbea4cdaf77b36ccc1e523c39220fc0b71df943`; independently recomputed all hashes in its manifest and found every file unchanged. Read the complete new section, author handoff, accepted Stage 1 prerequisites, notation, bibliography, and current plan/claim inventory. Did not read other reviewers' reports or coordinator checks. No manuscript edits were made.

## Verdict

**Accept Stage 02. No major or minor issue found.** The local source problems, uniform cosine estimates, baseline moment laws, stronger finite-bulk limit, and counterexamples are supported at the stated scope. This review does not certify later design or measurement theorems.

## Independent checks

### 1. Whole-line constant source and free-endpoint localization

The proposed energy spaces control L² mass on the fixed core by a derivative estimate and a positive-potential anchor interval, and control both L² and the polynomially weighted L² norm outside that core. The proof does not use a Dirichlet endpoint condition. Weighted Cauchy–Schwarz then gives the stated `L^((1-p)/2)` source-tail bound; since p is 2 or 4, the constant source is continuous in the energy-dual norm despite not being an L² function.

This tail bound is also enough for the Neumann upper-limit argument. Uniform energy bounds give local weak H¹ and strong L² subsequences; the source tails vanish uniformly, while energy is lower semicontinuous on successive compact intervals. The resulting limit lies in the whole-line energy space, whose compact-test density is justified by cutoff and mollification. This proves the free-endpoint limit instead of incorrectly assuming monotonicity of Neumann responses. Uniformly comparable weights preserve these bounds, and local convergence of weights suffices to identify the limiting energy/source. Compact-parameter uniformity follows by the sequential compactness argument stated in the text.

The Dirichlet/Neumann bracketing directions are correct for the response and for the minimum Rayleigh quotient. Complementary intervals with positive potential may indeed be bounded by the reciprocal-potential integral after dropping derivative energy.

### 2. Harmonic coefficient and isolated-zero scaling

I independently integrated the displayed Mehler kernel. Its Gaussian exponent matrix has determinant one, so the double integral is `sqrt(2π/sinh(2t))`. With `r=exp(-4t)`, the resolvent integral becomes `sqrt(π)/2 B((z+1)/4,1/2)`, producing exactly the stated gamma ratio. Applying the resolvent first to finite indicator sources and passing in the dual energy norm is legitimate by the source-tail bound and kernel positivity.

The quadratic scaling `x=(ε/a)^(1/4)y` has operator scale `(εa)^(1/2)` and integrated inverse scale `ε^(-1/4)a^(-3/4)`. The fixed-neighborhood upper/lower comparisons with curvatures `a_j±η`, then ε→0 and η→0, yield the claimed coefficient sum. A positive complementary rate gives only a bounded contribution for fixed η, which is sufficient for a relative equivalent. No unjustified bounded error for the whole scalar response is asserted. The zero-free trial `1/k0` is admissible by H¹ approximation and gives the separate reciprocal-rate limit.

Independent 40-digit arithmetic gave:

- `C0 = 4.647476009400966922629424651053969768508`;
- `C0²/sqrt(π) = 12.1859495788412001453907159624634294198`;
- `2^(1/3) C0^(4/3)/6 = 1.628601974379059597958657945708134875647`.

These are consistency computations, not error certificates for any numerically approximated quartic integral.

### 3. Quartic fold scale and both exact pair tails

For `(b x²-t)²`, balancing `ε/ell²` against `b² ell⁴` gives `ell=(ε/b²)^(1/6)`. The potential parameter is `μ=t/(ε^(1/3)b^(1/3))`, and dividing the spatial length by the operator scale gives `ε^(-1/2)b^(-1)`. Thus the fold scaling, including the factor two when b=1/2, is correct.

For large positive μ, each root has quadratic curvature `4μ`, so the two local contributions give `2 C0(4μ)^(-3/4)=C0 μ^(-3/4)/sqrt(2)`. With the author's choice `η=μ^(-3/8)`, the scaled harmonic interval radius grows like `μ^(3/8)`, the relative local potential error vanishes, and the complementary reciprocal integral is `O(μ^(-3/2)η^(-1))=O(μ^(-9/8))`, smaller than the leading `μ^(-3/4)`.

For μ=-a, the change `x=sqrt(a)z` gives integrated inverse factor `a^(-3/2)` and derivative coefficient `a^(-3)` relative to `(1+z²)²`. Dropping the derivative gives π/2, and the reciprocal-potential trial gives the matching lower bound with error `a^(-3)∫|v'|²`. Its energy cutoff is justified. The resulting positive-side tail determines the threshold q>4/3 for the whole-line pair-moment integral; the negative side would only require q>2/3. The text correctly distinguishes these whole-line tails from potentially invalid simultaneous interval/parameter equivalents.

### 4. Uniform compact-cosine localization and spectral gaps

The exact coordinate identity near c=1 is correct: with x=s-π and y=2 sin(x/2), `c+cos(s)=y²/2-t`, `ds=b0 dy`, and the derivative weight is `b0^(-1)`. Under the fold scaling, these weights remain uniformly comparable and converge locally to one. Dirichlet/Neumann bracketing and the interval lemma thus give both the compact-μ response limit and the gap scale `ε^(2/3)`; the complementary rate is uniformly positive in that regime.

For separated roots, r is comparable to sqrt(t), the harmonic width is `(ε/t)^(1/4)`, and `r/ell` is comparable to `(t³/ε)^(1/4)`. The complementary gap `t²` is at least `sqrt(εt)` when t³≥ε, and the complementary response `t^(-3/2)` is at most `ε^(-1/4)t^(-3/4)` there. Bounded intermediate ratios are covered by the compact fold argument, so no region between the two analyses is omitted.

For the sharp separated-root statement, the shrinking ratio `η=(ε/t³)^(1/8)` makes the scaled neighborhoods expand while the local curvature error vanishes. The complement divided by the proposed leading response is `O((ε/t³)^(1/8))`. Away from folds, fixed neighborhoods have uniformly nonzero slopes. The rootless lower bound follows from `k≥ν²+(1-cos s)²`; the reciprocal-rate response is `O(ν^(-3/2))` for ν≥ε^(1/3). These arguments establish the stated uniform response and gap envelopes on the whole compact family.

### 5. Every moment coefficient, the logarithmic cutoff, and the limiting law

For q<4/3, the pointwise inside limit is `2 C0(1-c²)^(-3/4)`. At density 1/4, integrating its qth power gives exactly the displayed beta coefficient. The exterior domination is sound: writing ν=ε^(1/3)z reduces the required bound to boundedness of `z^(3/4)/(1+z)^(3/2)`. Thus an integrable envelope works on both sides of the folds in this subcritical range.

For q>4/3, the two fold neighborhoods contribute factors: two folds, probability density 1/4, response amplitude `2^q ε^(-q/2)`, and Jacobian `(ε/2)^(1/3)`. Their product is `2^(q-4/3) ε^(1/3-q/2)`. The rescaled envelopes are integrable exactly in the stated range, and regions away from folds are smaller by a factor tending to zero.

At q=4/3, each inside fold contributes `(1/4)(2C0)^(4/3) ε^(-1/3)/(2t)` at leading order. Both folds integrated from ε^b to fixed t0 therefore contribute `(2C0)^(4/3)b/4` after division by `ε^(-1/3)log(1/ε)`. The omitted inside contribution has normalized upper bound `C(1/3-b)+o(1)`, with a b-independent constant from the uniform envelope; the rootless side is only `O(ε^(-1/3))`. Taking ε→0 and then b→1/3 determines the coefficient `(2C0)^(4/3)/12` without using compact-fold convergence at unbounded μ. This is a complete logarithmic matching argument.

The mean beta coefficient equals `C0²/sqrt(π)`. The square of the mean has order ε^(-1/2), strictly smaller than the second moment's ε^(-2/3), proving the variance equivalent. Budget normalization is correctly stated as ε=M/(2π), including the logarithm. The squared coefficient of variation has exponent -1/6.

The almost-sure normalized limit has probability 1/2 at zero because half the parameter range is rootless. Inverting its positive branch gives `P(W>w)=(1/2)[1-sqrt(1-(2C0/w)^(4/3))]`, and its tail coefficient is `(2C0)^(4/3)/4=2^(-2/3)C0^(4/3)`. Finite positive-ε moments are not confused with moments of this limiting random variable or with tracer-displacement moments.

### 6. Uniform flux estimate and the finite-bulk remainder

I rederived the multiplier identity from `-εh''+kh=1`. Testing against kh gives `ε∫k|h'|²-(ε/2)∫k''h²+∫(kh)²=P`. Since `∫kh=P`, subtracting P yields exactly the stated norm identity. Direct differentiation also gives `k''=2(1-c²)+6c(c+cos s)-4(c+cos s)²`.

After Cauchy–Schwarz and the spectral bound, the inside terms are `ε^(1/4)t(t+d)^(-5/4)` and `ε^(1/2)(t+d)^(-1)`, each bounded by `Cε^(1/6)` for d=ε^(1/3). Outside the bound is `ε(|t|+d)^(-5/2)≤ε^(1/6)`. Taking the square root produces the uniform ε^(1/12) flux error.

The Neumann problem has the correct compatibility and sign: `∫Ω(u-V)=KPV=-Db∫Γ∂n f0`. Its variational load is exactly the limiting Schur load. The flux error controls the difference of loads in the bulk energy dual, giving the upper remainder estimate after dropping its nonnegative surface penalty. With a C² domain, L² source, and constant compatible Neumann datum, H² regularity gives a trace in H^(3/2), hence in H¹ on the wall. The trace is therefore an admissible surface trial for D=ε, bounding the penalty by `ε∫|∂s tr(f0)|²` and supplying the lower estimate. This proves the offset-independent R0 expansion at the stated rate.

I checked the regularity requirements against [Guermond's author-hosted chapter](https://people.tamu.edu/~guermond/M661_FALL_2017/chap27.pdf), Theorem 27.23 and its compatible-Neumann discussion; the manuscript's C² boundary is sufficient for the cited H² conclusion. The whole-line scalar equivalent is not incorrectly used to claim a bounded scalar remainder.

The uniformly bounded physical correction transfers moments: subadditivity handles 0<q≤1, while the q>1 difference is controlled by `C(J^(q-1)+1)`, whose expectation is lower order by Hölder. The variance transfer follows separately from the second moment and the mean bound. All factors χ and χ² are correct.

### 7. Gaussian and averaged-rate counterexamples

For `g=ξ1 cos s+ξ2 sin s`, writing R²=ξ1²+ξ2² gives two roots of slope magnitude R and `∫g²=PR²/2`. The constant source test therefore yields `J≥2P/R²` independently of the mobility field and of any observation policy. The Rayleigh density makes E[R^(-2)] infinite even though E[R^(-3/2)] is finite. This correctly identifies a global amplitude failure of uniform integrability, not a failure of the samplewise local theorem.

For the more general stationary Gaussian context, the value and derivative are independent at a point, and the derivative is centered. The marked Rice formula yields the stated first inverse-slope moment. Its diagonal second-moment lower bound is infinite because the integrand becomes `E|U|^(-2)`. Zero-intensity sampling weights the absolute Gaussian derivative by its magnitude, producing exactly the Rayleigh density and the inverse-3/2-mark tail shown. I checked [Azaïs–Wschebor's author draft](https://www.math.univ-toulouse.fr/~azais/styles/other/student/level.pdf), Theorems 6.2 and 6.4: the manuscript supplies the C¹, nondegeneracy, and no-critical-zero conditions needed for this use; bounded continuous truncations cover the singular marks. No multipoint nondegeneracy is needed for the first marked formula or the diagonal lower bound.

Finally, `E c²=4/3` and `E c=0`, so the averaged rate is `4/3+cos²s`; dropping derivative energy bounds its response by 3P/4 for every nonnegative D. This cannot reproduce the actual divergent uniform-design mean. The counterexample is correctly limited to averaging the operator coefficient before inversion.

## Completeness and presentation

The section supplies the current local/baseline claims without importing repository-note proofs. It separates relative scalar equivalents, compact-parameter limits, whole-line tails, genuinely uniform bounds, and the stronger bulk remainder. The proof of the critical logarithm makes its two sequential limits explicit. The Gaussian discussion attributes its standard ingredients and does not imply independent zeros, a stable law, or a new general Gaussian theorem.

No currently actionable error, unsupported coefficient, missing major assumption, or clarification essential to following the arguments was identified. Numerical quartic integral values and later unrestricted-design constants appropriately remain outside this stage.
