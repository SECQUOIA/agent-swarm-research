# Independent review: Stage 01, round 01, reviewer 3

Reviewer: `/root/paper_reviewer_3`. Date: 2026-09-07.

Reviewed snapshot: `64708f8c61e751a8447d7955def9a2929c159b2bfc457eae8e2baf1900497f31`, as recorded in `snapshot.json`. I read `sections/01-model-transfer.tex`, the author handoff, notation ledger, and the accepted preparation-stage scope. I did not read other reviewers' reports or coordinate findings. I made no changes to manuscript sources.

## Independent mathematical checks

### Arbitrary and unbounded coefficients

The separation between an always-defined scalar smooth-test response and a physical minimal closed form is sound. In particular, the argument does not silently invoke closability for all L1 weights. With a positive floor, an energy-Cauchy sequence converging to zero in L2 has unweighted derivatives converging to zero; simultaneous almost-everywhere subsequences identify the weighted derivative limit as zero because D is finite almost everywhere. Thus the proof at lines 135–142 covers integrable, arbitrarily high spikes without requiring a bound on D.

The rate-anchor inequality controls constants, while the derivative term controls mean-zero wall functions. It yields the stated coercivity with `min(m,1)`. Contractions preserve the closed surface energy; simultaneous contractions of bulk and wall values also decrease the exchange penalty. Bulk trace continuity gives the claimed closed coupled form. Constants belong to the domain and have zero energy, consistent with conservativeness on the compact state space. The separate boundary copy correctly represents adsorption rather than identifying adsorbed particles with reflecting bulk-boundary states.

For positive floors, the mean-bulk gauge plus trace control gives the coupled spectral gap. For degenerate fields, the text appropriately permits extra kernel states and an infinite response instead of assuming ergodicity. For example, a wall region with both zero diffusivity and zero exchange can carry a nontrivial invariant component, and the stationary velocity need not have a finite integrated covariance. The spectral formulation handles this case.

### Physical coefficient and finite-response completion

I rechecked the normalization: the physical energy is the displayed unnormalized energy divided by Z, and the forcing in the same inner product is the displayed F divided by Z. The surface trial `v=-V phi`, with bulk zero, therefore gives exactly `KV^2 J/Z` as the lower bound.

The finite-time stationary covariance identity has the factor `1-r/t`, and a zero spectral atom contributes `t/2` to the variance divided by `2t`, as stated. The spectral limit is valid without a central limit theorem. Axial Brownian noise has zero conditional mean given the transverse path, so its covariance with the advective integral vanishes when its stochastic integral is well-defined (see the minor assumption below).

For the finite-J extension, the source functional is bounded in the energy norm by the quotient definition. The energy completion is the right space even if the corrector is not in L2. The reaction image satisfies

`||w||_2^2 <= k_max ||sqrt(k) h||_2^2 <= k_max J`.

This supplies an explicit finite bound for the bulk load and validates the finite remainder assertion. The source induced by a bulk trace is bounded independently by `||sqrt(k)b||_2`; its Riesz representative permits the square completion without subtracting infinite values. The source and trace representatives have cross product `integral w b`, giving the stated negative sign. The constant-test relation `integral w=P` and `integral_Omega(u-V)=KPV` justify the common-constant gauge. The nonnegative residual S is an actual infimum, not an assumed inverse formula for degenerate fields.

### Uniform logarithmic remainder

I checked the estimate through each scale: `J<=C/m`, `||h'||_2<=C/m`, positivity and the fundamental theorem give `||w||_infinity<=C/m`, while `integral w=P` is exact. With the stated Fourier normalization, every Fourier coefficient of w has modulus at most one and their squared sum is `||w||_2^2/P<=||w||_infinity`. The low-frequency contribution is logarithmic and the high-frequency contribution is at most `C||w||_infinity/N`. Taking N proportional to `2+||w||_infinity` gives the advertised logarithm. Trace duality, followed by maximization of a coercive bulk quadratic, gives the remainder bound. No derivative, support regularity, oscillation scale, or upper bound of D entered this chain.

### Policies, observation laws, and positive moments

For fixed smooth tests, all coefficient dependence is continuous in L1. Rational trigonometric polynomials and a countable C1-dense bulk core give countable suprema; the physical variational response therefore has a Borel extension to the whole coefficient space. The formulation needs no assertion that the closable subset is Borel, since a policy is already a Borel L1-valued map whose values are individually restricted. It also never interchanges an expectation with a pointwise infimum.

The mixture uses precisely the original budget and original information. The reaction term has the correct identity in the convex combination of forms, so `a_mixed >= (1-theta)a_original` holds even for nonclosable competitors. The lower and upper comparisons therefore cover arbitrary observation-dependent spikes and fine structure. The uniform positive policy makes both infima finite.

For q below one, the proof correctly uses subadditivity, not Minkowski. Division of its upper bound by `chi^q Fq` gives an additive relative error bounded by a constant times `log(1/M)^q/Fq`. For q at least one the root comparison gives `log(1/M)/Fq^(1/q)`. Thus the stated growth condition is sufficient in both cases, without regular variation, minimizers, or restrictions on how the observation law varies with M.

The canonical root bump bounds *every* budget-M field, since its derivative penalty uses the entire budget and a supremum derivative norm. With width `ell=M^(1/5)`, numerator and denominator scale as `ell^2` and `M/ell^2+ell^3`, respectively, yielding `M^(-1/5)`. The marginal event has probability 1/4 even when the observation reveals the full realization. This establishes the claimed uniformity over information laws and both quantitative errors. The mixture error of order M is smaller than the stated errors for each fixed q.

## Findings

### R3-01 — Minor: state the integrability assumptions for axial molecular diffusion

Location: `sections/01-model-transfer.tex:233–241`, with initial molecular coefficients introduced at lines 25–30.

The stochastic-integral interpretation and the finite formula for the molecular contribution require a finite nonnegative bulk axial diffusivity and a nonnegative, measurable, integrable surface axial diffusivity. These assumptions are not stated. Calling a coefficient a diffusivity suggests nonnegativity but does not establish the integrability needed for the random-clock Brownian integral and its second moment. The central isotropic example is safe because D is already nonnegative L1; the optional general surface coefficient is not yet restricted.

Remedy: explicitly assume `D_b^x` is finite and nonnegative and `D_s^x` is a nonnegative measurable L1 wall function whenever the Brownian contribution is included. Then stationarity gives finite expected quadratic variation on each finite interval and justifies the variance addition. For the final uniformly bounded-addition statement, retain its separate uniform bound across designs and realizations. No main flow-design theorem changes.

## Verdict and scope

No major mathematical or scientific issue found in this stage. Correct the minor molecular-integrability omission before stage acceptance. The core transfer theorem, its degenerate-coefficient interpretation, and its observation-uniform cosine corollary withstand the adversarial checks above. This review does not certify later singular asymptotics or unresolved variational limits. The requested one-author/five-reviewer workflow is being followed for this round; coordinator adjudication and a different agent's minor correction remain necessary before acceptance.
