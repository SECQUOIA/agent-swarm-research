# Independent adversarial review of Stage 1

Reviewed `main.tex`, both current section files, `appendices/wellposedness.tex`, `references.bib`, and `development/COVERAGE.md`. I did not read other review reports or research notes, communicate with other reviewers, edit the manuscript, or delegate this review. Introduction and later-stage material are outside this review's requested scope.

The current mathematical conclusions withstand the boundary, atomic-measure, zero-rate, and measurability checks below. I found no major issue. There is one minor mismatch between a general lemma's hypotheses and its supplied proof.

## Findings

### ADV-001 — Minor: the loss-formula proof uses a local bound absent from the abstract hypotheses

**Location:** `appendices/wellposedness.tex:34–48`, leading to `lem:weighted-comparison` at lines 66–81; specifically the justification of `eq:loss-duhamel`.

The abstract setting assumes that the nonnegative loss rate has a finite time integral for each fixed size. Lines 43–45 then restrict to `x <= R` and assert that multiplication by the loss rate is bounded by an integrable function of time. Pointwise time integrability does not imply that bound. The preceding sentence says the stronger bound holds *in the application*, but does not impose it on the abstract lemma's setting.

For example, `a_s(x) = 1/x` satisfies the stated pointwise condition and is unbounded on every `(0,R]`. This remains an admissible loss equation with genuinely finite weighted integrals: set `H_s = 0` and

\[
 d_t(dx)=\mathbf 1_{(0,1)}(x)\,x e^{-t/x}\,dx.
\]

Then `d_t = d_0 - integral_0^t a_s d_s ds`, and both required weighted-variation integrals are finite on every finite time interval. Nevertheless, the loss multiplication operator used in the proposed restricted Volterra-series proof is unbounded on `(0,R]`.

This is a proof-scope issue, not a counterexample to the Duhamel formula or the comparison conclusion. It does not undermine the existence or uniqueness application: there the loss is explicitly `lambda(t)(bar m(t) + bar N(t)x) + sigma(t)`, which has the asserted bound on every `(0,R]`.

**Suggested fix:** State in the abstract setting that for every finite `R,T`, there is `A_R` in `L^1(0,T)` with `a_s(x) <= A_R(s)` for `0 < x <= R`. That makes the supplied proof valid and covers every use in the paper. Alternatively, retain the greater generality and supply a loss-formula argument that does not use the missing uniform bound. The first fix is smaller and sufficient.

## Proof-chain checks with no issue found

- **Expected daughters versus actual binary events.** The deterministic assumptions genuinely admit nonsymmetric daughter measures, and the proofs do not silently impose complementary binary splitting. For example, `(1/2) delta_{x/5} + (3/2) delta_{3x/5}` has count two, first moment `x`, and support strictly below the parent, but is not symmetric about `x/2`. Jensen's fractional-moment estimate and the upper polynomial-moment bounds still hold for this example. The text correctly reserves eventwise binary conservation for future finite-particle results.

- **Pair inequality and equality.** The transformation to `g` is correct. The ratio controlling the second derivative strictly decreases on `(0,1/2)`: its numerator decreases, and both positive denominator factors increase. Together with the endpoint values and derivative signs this proves strict inequality away from the diagonal. There is no missed interior equality or endpoint included in the stated domain.

- **Unbounded fractional tests.** For `f_R = min(x^p,R)`, monotonicity and subadditivity give a coagulation defect between zero and `min(x^p,y^p)`. Multiplication by `x+y` is dominated by `xy^p + yx^p`, whose integral is `2mM_p`. Daughter support and mass conservation make `f_R(z)/z` give the required nonnegative fragmentation defect. Jensen bounds it uniformly by `2^(1-p)x^p`. Locally bounded count, fixed mass, and the rate assumptions therefore justify the entire time-integrated limiting argument without a second moment or a logarithmic moment.

- **Normalization, zero rates, and sharpness.** Count testing gives exactly `N' = (sigma-m lambda)N`. The normalized fractional coefficients are consequently `-a_p b-a_(1-p) sigma`. The argument remains valid when either rate, both rates, or the rates on any time interval vanish. Monodisperse initial data and equal splitting attain both scalar inequalities initially. For constant rates, the required initial right derivative is supported by weighted-variation continuity: the fractional coagulation integrand is bounded by a constant times `(1+x)(1+y)`, and the equal-split fragmentation integrand is a multiple of `x^p`. Thus each coefficient really is sharp in the stated instantaneous, prefactor-one sense. The paper does not overstate this as an optimal asymptotic exponent.

- **Sampling-law separation and boundaries.** Since `min(1,u) <= u^p`, the overlap bound is valid for atomic and nonatomic populations alike. Positivity of both decay constants implies affinity tends to zero whenever the combined clock diverges. At criticality, fixed count and the two window estimates prove the stated weak limits without losing material at finite time. The moving-window endpoint calculations are correct: `kappa_p/p` tends to `log 2` at zero and `kappa_p/(1-p)` tends to `log 2` at one. The two windows can require different `p`; the text says so and excludes the unproved limiting speed.

- **Perturbed rates.** The fractional coagulation defect has the correct sign for using the lower kernel bound, while the upper kernel and selection bounds justify the test. The identity `2-2^p = 2^p(2^(1-p)-1)` gives the stated `gamma_p`. Choosing `p` near one proves the sufficient threshold `s_* < 2am`, without asserting the endpoint or optimality.

- **Signed comparison.** After the loss formula is justified as discussed in ADV-001, the majorant argument is sound. In particular, from `z >= |d|`, subtracting the integrated nonnegative loss of `z` gives an upper bound by subtracting the loss of `|d|`. This is the direction needed for the displayed Gronwall inequality. It does not require differentiation of a Hahn sign or an unjustified derivative of total variation.

- **Nonlinear polarization and second-moment stability.** Polarization has the correct factor with `mu=(n+v)/2`. The direct loss remains negative; only the cross loss is majorized positively. With `w=1+x`, the exact bracket is `w(x+y)+w(x)-w(y)=1+2x`, producing `bar m+2 bar M_2+y(bar N+2 bar m)`. Thus the stated stability coefficient is a valid upper bound. Different masses cause no missing cancellation or extra term.

- **Measurable time-dependent daughters and weak integration.** The construction uses setwise integrals with integrable weighted variation, which both define countably additive measures and give norm-continuous integrated paths. A moving atom need not be strongly measurable in total variation; the manuscript explicitly avoids that requirement. Norm-continuous Picard paths are measurable kernels, and composition with the given measurable daughter kernel preserves the needed setwise measurability. No passage of a merely measurable parent-dependent operator through a narrow limit is used.

- **Positive cutoff construction and polynomial bounds.** For bounded coagulation rate, the third-moment weighted space controls the bilinear operator. Adding the stated scalar loss bound makes the remaining map positive on the nonnegative ball. The second- and third-moment increments give `2 lambda m M_2` and `3 lambda(mM_3+M_2^2)` respectively. Cauchy–Schwarz then gives the displayed third-moment bound, uniformly in the cutoff. These bounds control continuation.

- **Cutoff removal and initial approximation.** The cutoff defect is bounded by the indicated second and third double moments, with error integrable in time and of order `1/r`. Its forcing interpretation allows the full-equation stability estimate to compare two cutoff solutions. Weighted-variation convergence preserves count and mass and controls every bounded Borel test, including the fragmentation term. Lower semicontinuity gives the moment upper bounds. Initial truncation then uses only a common second-moment bound, so no uniform third moment has been smuggled into the final theorem. Initial truncations that happen to be zero simply give the zero approximation, or can be omitted until their mass is positive.

- **Finite-time boundary claims.** A continuous curve in weighted variation on a compact time interval has compact image. The finite-cover argument gives uniform count tightness near zero; its weighted version also controls the mass tails. The resulting measures stay on `(0,infinity)` and their first moment is inherited in norm, rather than being inferred from an insufficient narrow limit.

## References and coverage

The bibliography entries and the limited contextual claims attached to them check out against the primary sources. Cepeda's article covers homogeneous-like kernels through homogeneity one and uses a daughter-ratio law independent of parent mass; this supports the stated comparison with the time-independent selfsimilar setting. The manuscript does not cite it as a theorem covering arbitrary measurable parent dependence. See [Cepeda's paper](https://arxiv.org/pdf/1301.1934) and its [journal metadata](https://arxiv.org/abs/1301.1934).

The Deaconu–Fournier–Tanré citation accurately supports probabilistic representation of mass sampling in pure coagulation, and the author, journal, volume, year, and page information agree with the [primary article](https://www-sop.inria.fr/members/Etienne.Tanre/publication/AOP104.pdf).

The Stage 1 destinations listed in the coverage map are present. The claims deliberately deferred to Stages 2–5 are not missing requirements for this review. No broader priority claim is needed to validate this stage's proofs.

## Optional improvements

For an especially self-contained sharpness paragraph, add the one-sentence weighted-integrand continuity justification given above for the initial right derivative. The conclusion is already supported by the appendix and the estimates; this is exposition, not an additional finding.

**Major issue count: 0. Minor issue count: 1. Recommendation: accept Stage 1 after the small hypothesis/proof alignment in ADV-001.**
