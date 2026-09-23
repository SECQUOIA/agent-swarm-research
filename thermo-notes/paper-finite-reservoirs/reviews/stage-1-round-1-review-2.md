# Stage 1, round 1: independent review 2

Verdict: **no major issues**. The framework and threshold results are mathematically supported under their stated assumptions. I found one minor wording issue below.

Scope: `main.tex`, `sections/framework.tex`, and `sections/thresholds.tex`, as frozen for this round. I read `reviews/README.md`; I did not read other reviewers' reports, edit the manuscript, or delegate work. Later-stage material is outside this review.

## Issue requiring a minor correction

1. **Location:** `sections/framework.tex`, proof of the two-center bounds, immediately after the parabolic interpolation bound (line 222 in the reviewed version).

   **Text:** The difference is convex and vanishes at both endpoints, “hence is nonpositive there.”

   **Assessment:** The proof is correct, but “there” can refer to the endpoints, where the difference is already zero. The required conclusion is nonpositivity throughout the interval.

   **Remedy:** Replace “hence is nonpositive there” with “hence is nonpositive throughout the interval.” No mathematical revision is needed.

## Independent checks performed

- **Exact physical marginal and integrability.** Integrating the reservoir shell gives a subsystem measure proportional to `(total energy − subsystem energy)^c` below the cutoff. Dividing by the canonical reference produces exactly the stated likelihood. Writing the residual energy as `u > 0`, its unrestricted maximum is `exp(beta * total energy) * (c / (e * beta))^c`, so its expectation is finite under any probability reference, including one whose energy is unbounded below. Its expectation is positive exactly when the reference gives positive probability below the cutoff. No bounded-energy or density assumption has been smuggled into the framework.

- **Surface convention.** Differentiating the stated entropy gives inverse temperature `c/U` and microcanonical surface heat capacity `k_B c`. Direct integration of the canonical reservoir density gives Gamma shape `c+1`, mean `(c+1)/beta`, and heat capacity `k_B(c+1)`. A positive definite quadratic energy in `f` scalar coordinates has shell exponent `f/2−1`. The manuscript explicitly distinguishes these conventions and restricts the theorem to `c>0`.

- **Full-state total variation.** The energy-only Radon–Nikodym derivative is also the derivative of the energy pushforward. Integrating its absolute deviation from one gives exactly the same distance on both spaces. This requires neither a regular conditional distribution nor positive probability at individual energies. Discrete, continuous, and mixed laws are covered.

- **Normalization and cutoffs.** The normalization lemma follows by the stated triangle inequality. Its uses establish positivity of normalization for all sufficiently large indices. The centered weight is globally at most one, including on the negative-energy tail, by `log(1-y) <= -y`. Tightness and `c >> b^2` make the cutoff irrelevant with probability tending to one. The proof appropriately permits adjusting finitely many inadmissible early choices.

- **Secant calibration.** Solving equality of endpoint likelihoods gives the two displayed, equivalent total-energy formulas. Both endpoints are strictly feasible for every positive exponent. The derivatives and their signs are correct. The parabolic bound follows from the second-derivative bound with the claimed inequality direction; concavity gives both the exterior non-amplification and the global tangent estimate. The local windows have size `o(c)`, so their feasibility and curvature estimates hold.

- **Weak-support necessity.** I rederived both chord identities and the uniform bound `f_theta(q) >= theta(1-theta) min(q^2,q)/(2e)`. Three positive-probability, separated scaled intervals intersect the good-likelihood set even for nonatomic laws. The endpoint identity makes `cq` diverge; the chord identity first forces `q -> 0`, then `cq^2 -> 0`, yielding `b^2/c -> 0`. The proof does not differentiate an approximate likelihood or infer pointwise control from an integral without the good-set argument.

- **Two-atom boundary.** Equal endpoint weights reproduce any prescribed positive probabilities on exactly two energies, including arbitrary degeneracy within those energy levels. This verifies that three points in the scaling limit are a substantive hypothesis. A two-atom scaling limit is correctly distinguished from a finite law with exactly two energies.

- **Two-scale necessity.** The positive mixture weights transfer the good-set probability to each phase. Two local energies and one energy in the other phase give chord fraction of order `s/Delta`. The resulting obstruction is `min(Delta*s/c, s) -> 0`; the explicit assumption `s -> infinity` is what turns it into `c >> Delta*s`. The proof works when the fluctuating phase is the upper phase as well. Exceptional mass need not vanish for this necessary condition.

- **Positive-phase sufficiency.** The exponential moment controls the actual exchanged energy and gives a uniform second-moment bound for the reweighting factors once their slope tends to zero. This establishes uniform integrability, rather than assuming local convergence suffices after exponential reweighting. The exceptional component is controlled by the global amplification bound. The sharper corollary and the more general exceptional-rate sufficient condition follow with the stated scales. The manuscript correctly excludes signed partition-function remainders from this argument.

- **Interior-density criterion.** I checked both ratios between reservoir gain and the Gaussian/interfacial costs. The second is bounded by a constant times `kappa*N^(3/2)*N^(1/2-alpha)`, so the endpoint `alpha=1/2` is included. Splitting the exponential of the minimum bounds the weighted tail by a Gaussian tail plus an integrable stretched-exponential contribution with prefactor `N^(-1/2)`. Exterior energies cannot be amplified. The local density limits have total weight one, which supplies tightness in the union of phase windows and justifies the conditional weak limits used for necessity. No exterior envelope is needed.

## Limits of this review

These were analytic checks of every statement and proof in the assigned stage, including discrete and unbounded-energy boundary cases. I did not run numerical experiments or perform a new priority search. The review establishes no claim of literature novelty and assesses no later microscopic application.
