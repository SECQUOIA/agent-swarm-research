# Independent review: Stage 02, round 01, reviewer 1

Reviewer: `/root/paper_reviewer_1`. Date: 2026-09-07.

Snapshot reviewed: `0d15634123d5c1e1db222f2d9fbea4cdaf77b36ccc1e523c39220fc0b71df943`. All eleven hashes in its manifest matched the files read. I reviewed `sections/02-local-baseline.tex` in full, the accepted model/form/transfer prerequisite, handoff, bibliography, and notation. I did not read other reviewers' reports or coordinator-checks and did not edit the manuscript.

## Verdict

**Accept Stage 02. No major or minor defect identified.** The whole-line and free-endpoint arguments supply the needed energy and tail control; compact-fold convergence and separated-root matching are used within their respective ranges. The moment factors, critical logarithm, and full-bulk correction check independently. The Gaussian statements are appropriately limited and supported by the cited first marked Rice formula.

This verdict covers the present stage. It does not establish later unrestricted-design lower bounds, measurable observation optimizers, or any new sharp-design limit.

## Detailed independent checks

### 1. Whole-line source and free endpoints

The constant source is bounded in the polynomially confining energy norm even though it is not an L2 vector. I checked the anchored estimate by splitting a fixed core from the exterior: a positive-potential unit anchor interval controls the core's constant mode through the fundamental theorem of calculus, while the derivative controls its variation. Outside that core, the potential controls the weighted L2 norm. The argument does not impose boundary traces, so it applies uniformly to sufficiently long Neumann intervals.

Weighted Cauchy–Schwarz gives exactly the displayed tail exponent `(1-p)/2`, because the integral of `|x|^(-p)` beyond L is proportional to `L^(1-p)`. Combining the core and tail estimates makes the source energy-continuous and bounds the maximizer energies uniformly. The Riesz solution therefore exists in the energy completion, and that completion embeds in H1 and weighted L2 for these particular polynomial potentials.

For the Neumann limsup, weak local H1 compactness and strong local L2 compactness identify a limit, while the tail inequality gives convergence of the full source integrals. Lower semicontinuity gives `limsup(2 source-energy) <= 2 source(limit)-energy(limit)`. The limiting function belongs to the whole-line energy space: its derivative, L2 norm, and polynomially weighted L2 norm are finite; cutoff and then compact mollification provide the required approximants. Thus there is no implicit endpoint-decay assumption or missing escaped-source term.

For the weighted extension, uniform comparability retains all bounds and locally uniform convergence identifies both the local energy and source. Compactness of the potential parameters then upgrades sequential convergence to the stated uniform convergence. No parameter tending to infinity is included in that lemma; the manuscript correctly addresses those tails separately.

### 2. Bracketing and harmonic response

The response bracketing is in the correct direction. Independent H1 traces on partition pieces enlarge the trial space for the upper bound; zero-trace local tests give global lower trials. On a positive-potential complement, completing the pointwise square after discarding derivative energy gives the reciprocal-rate upper bound. The eigenvalue comparison uses the same Neumann enlargement, with the global Rayleigh quotient bounded below by the minimum quotient of the pieces.

I independently recalculated the harmonic double heat-kernel integral. Its integral over x and y is `sqrt(2 pi/sinh(2t))`. Substitution `r=exp(-4t)` in the time integral gives `sqrt(pi)/2 B((z+1)/4,1/2)`, hence the displayed gamma ratio. Approximating the constant source by interval indicators is legitimate in the energy-dual norm by the source-tail estimate. This supplies an actual resolvent interpretation without applying the L2 inverse to a non-L2 constant.

The isolated-zero scaling is `x=(epsilon/a)^(1/4)y`, producing integrated-response factor `epsilon^(-1/4)a^(-3/4)`. Fixed-neighborhood comparison followed by the interval limit and then shrinking curvature error gives the claimed equivalent under C2 regularity. The complement is only bounded at each fixed neighborhood choice; the text does not incorrectly conclude an additive O(1) remainder from this proof.

### 3. Quartic pair, parameter tails, and compact cosine bounds

For `(b x^2-t)^2`, I checked the length scale `(epsilon/b^2)^(1/6)`, potential/operator scale `epsilon^(2/3)b^(2/3)`, and integrated-response factor `epsilon^(-1/2)b^(-1)`. The scaled parameter is consequently `t/(epsilon^(1/3)b^(1/3))`.

At large positive mu, the two local curvatures are `4 mu`. With `eta=mu^(-3/8)`, their rescaled interval radius is of order `mu^(3/8)`, while the omitted reciprocal integral is O(`mu^(-9/8)`), smaller than the leading `mu^(-3/4)` term. Adding the two harmonic contributions gives `C0/sqrt(2)`, as printed. For negative mu, scaling by `sqrt(a)` leaves derivative coefficient `a^(-3)` and reciprocal potential `(1+z^2)^(-2)`. Its integral is pi/2, and its finite derivative energy makes it a valid limiting trial. These two tails and compact continuity yield the stated envelope and the exact integrability threshold q>4/3.

The sine coordinate near c=1 gives the exact potential `(y^2/2-t)^2`. Its Jacobian and derivative weights are uniformly comparable and converge locally to one under fold rescaling. The complementary fixed wall interval is bounded away from zero in this compact-fold regime. This establishes both the compact-fold response limit and the quartic gap order.

For separated roots, local quadratic comparisons have curvature comparable to t, so the response scale is `epsilon^(-1/4)t^(-3/4)` and the gap scale is `sqrt(epsilon t)`. The complementary potential is at least a fixed multiple of t squared. When `t^3>=epsilon`, that lower bound exceeds the required gap, and its reciprocal response is no larger than the claimed local order. Bounded intermediate scale ratios are covered by compact-fold estimates. On the rootless side, adding `nu^2` to the zero-floor quartic potential gives the stated gap; the reciprocal-rate integral gives the other response branch.

For the sharp separated statement, `rho=epsilon/t^3` and `eta=rho^(1/8)` make the scaled local radius diverge as `rho^(-1/8)`. The complementary response divided by the leading term is O(`rho^(1/4)/eta`)=O(`rho^(1/8)`). Curvature relative errors are O(eta). Thus the proof genuinely supports sequential uniform matching as the roots approach a fold. It does not infer that matching merely from fixed-c asymptotics.

### 4. Disorder averages and limiting law

For subcritical q, the inside envelope has integrable singularity `t^(-3q/4)`. On the outside, `epsilon^(1/4)(nu+epsilon^(1/3))^(-3/2) <= C nu^(-3/4)` supplies an equally suitable envelope. This proves domination on the entire offset interval. The density 1/4 and the beta integral give the first coefficient.

For supercritical q, the two folds contribute a factor 2, the probability density contributes 1/4, the response amplitude contributes `2^q`, and the parameter Jacobian contributes `2^(-1/3)`. Their product is `2^(q-4/3)`. The pair tail is integrable in precisely the claimed range. Away from folds, the order `epsilon^(-q/4)` is negligible against `epsilon^(1/3-q/2)` exactly when q>4/3.

At criticality I checked the retained-interval argument rather than only matching exponents. The combined two-fold coefficient on `epsilon^b <= t <= t0` is `(2C0)^(4/3)b/4`. The omitted interior normalized contribution is bounded by `C(1/3-b)+o(1)`, and the rootless side contributes only O(`epsilon^(-1/3)`). Taking epsilon to zero before b increases to 1/3 therefore identifies the coefficient `(2C0)^(4/3)/12`, which equals the printed expression. The unspecified bound C causes no residual error after this second limit.

I also recalculated the mean identity and critical coefficient with 40-digit mpmath arithmetic, independently of the author output:

- `C0 = 4.64747600940096692262942465105`.
- Mean coefficient `=12.1859495788412001453907159625`.
- Critical coefficient `=1.62860197437905959795865794571`.
- Rootless integral `=1.57079632679489661923132169164`.

These are checks of the analytic formulas, not interval-certified numerical constants. The variance follows because the mean squared has order `epsilon^(-1/2)`, smaller than the second moment's `epsilon^(-2/3)`.

For the limiting random variable, inversion of `W=2C0(1-c^2)^(-3/4)` on `|c|<1` gives the displayed tail. Its coefficient is `(2C0)^(4/3)/4=2^(-2/3)C0^(4/3)`. The mass at zero is the probability of `|c|>1`, namely 1/2. The exceptional folds have probability zero. The interpretation properly concerns realization-to-realization variation, and the manuscript does not infer a tracer displacement law from it.

### 5. Uniform full-bulk correction

Multiplying `-epsilon h''+kh=1` by kh and integrating gives `int w^2-P+epsilon int k(h')^2=(epsilon/2)int k''h^2`. Since `int w=P`, its first term is exactly `||w-1||_2^2`. Direct differentiation gives `k''=2(1-c^2)+6c(c+cos s)-4(c+cos s)^2`.

Using the source energy, `||h||_2^2<=J/lambda`, and Cauchy–Schwarz for `int |g|h^2` yields the manuscript's estimate. On the inner side, the two resulting terms are bounded respectively by `epsilon^(1/4)t(t+d)^(-5/4)` and `epsilon^(1/2)(t+d)^(-1)`, both O(`epsilon^(1/6)`). Outside, the bound is `epsilon(nu+d)^(-5/2)`, also O(`epsilon^(1/6)`). Taking a square root gives the stated exponent 1/12.

The Neumann bulk problem has the required compatibility because the integrated outward flux is `-KVP` and the integrated right-hand side is `KVP`. The Schur load perturbation is O(`epsilon^(1/12)`) in the bulk energy dual. Dropping the nonnegative penalty gives the upper remainder estimate; using the fixed unperturbed optimizer gives the lower estimate. C2 boundary regularity suffices for H2 Neumann regularity with L2 source and constant conormal datum, and hence for an H1 tangential trace trial. I checked the relevant conditions in [Guermond's author-hosted chapter](https://people.tamu.edu/~guermond/M661_FALL_2017/chap27.pdf), which points to the cited Grisvard section. This review did not newly obtain the full Grisvard chapter.

The uniformly bounded remainder is negligible relative to every divergent scalar positive moment. The separate q<=1 and q>1 inequalities used for this transfer are correct, and the variance comparison follows from the already controlled first and second moments. This result concerns the exact J response and does not upgrade a local scalar equivalent into an additive expansion.

### 6. Counterexamples and marked-zero context

For the Gaussian sinusoid, `int g^2=PR^2/2`, so the constant-test lower bound is `2P/R^2` for every mobility field, including a realization-dependent one. The Rayleigh density near zero makes its expectation infinite independently of the mobility budget. In contrast, the samplewise quadratic-zero sum is `2R^(-3/2)`, whose mean is finite. This is a valid warning against exchanging expectation and the samplewise limit and explicitly lies outside the uniformly anchored ensemble.

I checked the stated regularity and noncritical-zero assumptions against Theorems 6.2 and 6.4 in the [author-hosted Azaïs–Wschebor book draft](https://www.math.univ-toulouse.fr/~azais/styles/other/student/level.pdf). The continuous derivative can serve as the auxiliary Gaussian field; bounded continuous truncations of negative-power marks extend by monotone convergence. Stationarity makes the value and derivative independent at one point. Thus the first marked moment uses `E|U|^(-1/2)` and the diagonal lower bound for the second moment uses `E|U|^(-2)`, with the stated finite and infinite values. The zero-intensity slope distribution is Rayleigh with the displayed scale. No independent-zero or stable-limit claim is implicit in these calculations.

Finally, `E k_c=4/3+cos^2(s)` is uniformly positive, and discarding derivative energy gives the stated bounded averaged-rate response. This directly contrasts with the actual divergent uniform-design mean without requiring an unjustified exchange of inverse and expectation.

## Build and remaining stage boundaries

The frozen main document builds with `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`; latexmk returned success and reported the PDF up to date. The current text supplies the analytic baseline and local tools intended for Stage 02. Reproduction of scientific figures, final bibliography/novelty synthesis, and complete-document visual inspection remain assigned later-stage obligations, not omissions from this section.

**Findings requiring correction: none.**
