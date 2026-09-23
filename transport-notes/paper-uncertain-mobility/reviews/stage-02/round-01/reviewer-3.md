# Independent review: Stage 02, round 01, reviewer 3

Reviewer: `/root/paper_reviewer_3`. Date: 2026-09-07.

Snapshot: `0d15634123d5c1e1db222f2d9fbea4cdaf77b36ccc1e523c39220fc0b71df943`.

I reviewed the complete `sections/02-local-baseline.tex`, its author handoff, bibliography, and the relevant accepted Stage 01 definitions and comparison results. I did not read other reviewer reports or coordinator checks, and did not edit manuscript files.

## Independent checks

### Energy source and free endpoints

The anchored estimate is valid on large Neumann intervals, not just on zero-trace functions: a fixed exterior anchor interval controls the core's otherwise uncontrolled constant, and the potential controls the remaining exterior. It yields a uniform bound in the weighted L2 norm. Weighted Cauchy–Schwarz gives source tails of order `L^((1-p)/2)` times the energy norm. Thus neither the constant source nor escaping source mass is being treated as an L2 vector without justification.

For the Neumann limsup, a locally weakly convergent maximizer sequence has a limiting weighted-energy function. The uniform source-tail bound promotes local source convergence to full source convergence, while lower semicontinuity handles the subtracted energy with the correct inequality direction. Compactly supported tests provide the Dirichlet liminf. Uniformly comparable weights that converge locally uniformly preserve both steps, even if the weights oscillate or change near expanding endpoints. Compact parameter subsequences justify the stated compact-parameter uniformity.

The bracketing directions are correct. Cutting without continuity enlarges the response space and lowers the lowest eigenvalue. In an exterior interval the derivative-free upper bound needs no endpoint assumptions. The manuscript explicitly distinguishes a compact-parameter interval limit from a joint large-negative-parameter limit with insufficiently remote endpoints; this avoids the rootless-endpoint counterexample.

### Harmonic and quartic constants

I rederived the harmonic scaling directly. For potential `a x^2`, coordinate scale `(epsilon/a)^(1/4)` and operator scale `(epsilon a)^(1/2)` give integrated-response factor `epsilon^(-1/4)a^(-3/4)`. The double integral of the displayed Mehler kernel is `sqrt(2pi/sinh(2t))`; substitution `r=exp(-4t)` gives `(sqrt(pi)/2) B((z+1)/4,1/2)`, agreeing with the gamma coefficient.

At a quartic fold `(b x^2-t)^2`, the coordinate scale is `epsilon^(1/6)b^(-1/3)` and the response factor is `epsilon^(-1/2)b^(-1)`. For large positive pair parameter, each root has quadratic curvature `4mu`; two contributions therefore give `C0/sqrt(2) mu^(-3/4)`. The chosen relative cutoff `eta=mu^(-3/8)` has expanding harmonic radius and omitted reciprocal response `O(mu^(-9/8))`, smaller than the leading order. For a large negative parameter, the reciprocal trial has finite derivative energy, yielding the exact rootless coefficient `pi/2`. These two tails give integrability of the qth power exactly when `q>4/3`.

### Adversarial sequences and uniform cosine bounds

The exact sine coordinate near a cosine fold correctly produces the potential `y^2/2-t`, derivative weight `b0^(-1)`, and source/reaction weight `b0`. The coordinate interval becomes large while all weights remain uniformly comparable; the weighted expanding-interval lemma applies in the compact scaled-parameter region.

The separated-root envelope has harmonic width `(epsilon/t)^(1/4)` and root distance of order `sqrt(t)`. Large values of their ratio permit harmonic Neumann brackets; bounded ratios are already covered by compact fold parameters. On the complement, the lower rate bound is of order `t^2`, compatible with the harmonic spectral gap because `t^3>=epsilon`. Outside the zero-containing side, `k >= nu^2+(1-cos s)^2` supplies the stated gap, and the reciprocal-rate bound supplies the response estimate.

For sharp matching, set `rho=epsilon/t^3`. The shrinking relative neighborhoods `eta=rho^(1/8)` still have scaled radius `rho^(-1/8)` tending to infinity. The local Taylor error is uniformly O(eta), and the complementary response divided by the leading response is O(rho^(1/8)). Hence a sequence approaching the fold arbitrarily slowly or rapidly is covered whenever rho tends to zero. Sequences bounded away from the fold follow from uniformly separated roots. No compact-parameter limit is improperly invoked for a parameter tending to infinity.

### Moment regimes and logarithmic cutoff

Below `q=4/3`, the inside domination is `t^(-3q/4)`. The outside estimate after multiplying the response by `epsilon^(1/4)` has the same integrable singular envelope, while its pointwise limit is zero. This justifies the beta coefficient over only the zero-containing offset interval.

Above `q=4/3`, two folds, density 1/4, amplitude `2^q epsilon^(-q/2)`, and Jacobian `epsilon^(1/3)2^(-1/3)` multiply to `2^(q-4/3) epsilon^(1/3-q/2)`. The envelope is integrable in the scaled parameter precisely in this regime. Contributions a fixed distance from the folds have lower order.

At criticality, the two inside folds together have logarithmic integrand coefficient `(2C0)^(4/3)/4` multiplying `epsilon^(-1/3) dt/t`. Integrating over `epsilon^b <= t <= t0` gives this coefficient times b. The omitted inside contribution, normalized by the claimed scale, is at most a constant times `(1/3-b)`; this constant comes from the parameter-uniform envelope and does not diverge as b approaches 1/3. The outside contribution is only O(epsilon^(-1/3)). Taking epsilon to zero before b approaches 1/3 gives `(2C0)^(4/3)/12`, exactly the stated critical coefficient. Thus the sharp logarithm does not depend on an unjustified interchange of moving cutoffs.

The squared mean is of order `epsilon^(-1/2)` and is negligible against the second moment of order `epsilon^(-2/3)`. Direct inversion of the limiting response gives the stated half-mass atom and tail coefficient `2^(-2/3)C0^(4/3)`. All positive moments at fixed epsilon remain finite by the uniform rate anchor and positive-mobility coercivity, so the heavy limiting tail does not establish infinite finite-epsilon moments.

### Full-bulk refinement

Direct differentiation gives `k''=2(1-c^2)+6c g-4g^2`. Multiplication of the periodic equation by kh yields the stated flux identity with the correct sign and factor 1/2. The energy and spectral-gap estimates give `||h||_2^2<=J/lambda`. Inside the fold, the resulting two terms are bounded by `epsilon^(1/4)(t+d)^(-1/4)` and `epsilon^(1/2)(t+d)^(-1)`; both are at most a constant times `epsilon^(1/6)`. Outside, `epsilon(nu+d)^(-5/2)` has the same bound. Taking square roots gives the claimed flux exponent 1/12.

The Neumann compatibility condition has the correct sign. Perturbing the bulk load in its energy-dual norm gives the upper remainder estimate. Testing the Schur penalty with the trace of the regular Neumann solution gives an O(epsilon) lower-error term; the assumed C2 domain and L2 source supply the needed H2 regularity. A uniformly bounded remainder transfers every fixed positive moment, including q below one through subadditivity. The variance transfer uses the previously checked second-moment dominance.

I independently inspected the author-hosted regularity statement, which covers C1,1 domains and the compatible zero-reaction Neumann problem; the manuscript's C2 domain is sufficient. [Guermond, Theorem 27.23 and Remark 27.24](https://people.tamu.edu/~guermond/M661_FALL_2017/chap27.pdf).

### Gaussian counterexample and marked zeros

The constant test yields `P^2/integral g^2=2P/R^2` irrespective of the chosen mobility, so the Rayleigh amplitude law gives infinite expected response even for an adaptive design. The limiting zero sum has mean governed by the integrable density behavior `r^(-1/2)` near zero, whereas its square has divergent expectation. This is a genuine failure of uniform integrability, with global rate anchoring absent.

The first marked-root identity uses only single-point slope statistics; it does not assert independence of zeros or require a two-root density for the displayed second-moment lower bound. Weighting the Gaussian derivative density by its magnitude gives the Rayleigh zero-intensity distribution. For the first zero-sum moment the Gaussian absolute moment is `sigma1^(-1/2)2^(-1/4)Gamma(1/4)/sqrt(pi)`; the diagonal lower bound for its second moment involves the divergent moment `E|U|^(-2)`. The manuscript's hypotheses and continuous bounded mark truncation agree with the cited weighted formula. I independently inspected those hypotheses and the auxiliary-field condition in the [Azaïs–Wschebor draft, Theorems 6.2 and 6.4](https://www.math.univ-toulouse.fr/~azais/styles/other/student/level.pdf).

Finally, the mean-rate counterexample is direct: the rate average is bounded below by 4/3 and the derivative-free response bound is at most `3P/4`, while the true uniform-design mean diverges.

## Findings and verdict

No major or minor issue identified in this stage. The checked joint limits, free endpoints, exact constants, uniform envelopes, finite-bulk refinement, and counterexample scope are consistent and justified. I recommend accepting Stage 02 subject to the coordinator's assessment of all five independent reports. This verdict does not certify later design asymptotics, generic-family extensions, or unresolved local variational limits. The new-stage author and independent-review sequence follow the required process; final stage acceptance remains the coordinator's decision.
