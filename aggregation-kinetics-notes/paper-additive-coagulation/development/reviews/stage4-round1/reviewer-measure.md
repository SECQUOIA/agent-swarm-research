# Stage 4 independent review: measure, moment, and probability arguments

I reviewed all new mathematics in `sections/finite-population.tex`, `sections/observable-boundaries.tex`, `appendices/finite-count.tex`, and `appendices/unbounded-moments.tex`, together with the relevant accepted results, Stage 4 coverage map, author report, source developments, and numerical supplement. I did not read another current Stage 4 review, communicate with reviewers, alter manuscript or data files, or compile the manuscript. All frozen source hashes match the Stage 4 snapshot.

**Findings: no actionable mathematical, scientific, or expository defect identified. Major issues: 0. Minor issues: 0.**

## Unbounded tests and entropy sharpness

**Locations:** `appendices/unbounded-moments.tex`, lines 11–85; `sections/observable-boundaries.tex`, Proposition `prop:broadening-entropy`, lines 95–148.

The tangent extensions are valid for both observables. Subtracting the tangent slope times mass gives a bounded Borel test, so their balances follow directly from the accepted weak equation and conserved first moment. Both the extension and its remainder are convex and vanish continuously at zero. Their coagulation increments are therefore nonnegative and bounded by the original increment; the same reasoning gives the stated daughter-loss bounds. This reasoning also works for \(x\log x\), despite that function being negative at small sizes.

The second-moment coagulation majorant integrates to \(4mM_2\), not a third moment. The entropy coagulation majorant integrates to a constant times \(NM_2+m^2\). The daughter majorants are respectively \(x^2\) and \(x\log2\). All are integrable over finite time intervals under the stated locally bounded second-moment assumption and locally integrable rates. The endpoint dominations are also correct. Dominated convergence thus proves the complete balances and local absolute continuity without an added third moment, negative logarithmic moment, or daughter logarithmic moment.

The second-moment daughter interval follows from expected count two and expected mass, so no eventwise binary assumption is needed here. It gives the two broadening exponents and the exact equal-split identity. Passing the accepted fractional pair inequality to order one gives the stronger entropy inequality with coefficient \(4\log2\). Its combination with daughter Jensen yields precisely \(\lambda m^2\log2\).

The initial right derivative used for sharpness is justified. Continuity of \(M_2(t)\), together with total variation continuity, gives uniform integrability of the second-moment tails near zero time. The explicit remainder involving \(\min(x^2,R^2)\) correctly controls the tail beyond \(\sqrt2R\). Hence convergence holds in variation weighted by \(1+x^2\). The entropy pair integrand has the required quadratic bound, and the equal-split fragmentation increment is exactly linear. The entropy drift therefore converges to its monodisperse value at zero. The sharpness statement is about actual solutions, not merely a formal vector field.

## Rate-weighted stationary inverse-power test

**Location:** `sections/observable-boundaries.tex`, Theorem `thm:power-no-equilibrium`, lines 178–275.

Finite count and mass imply finite, positive \(M_\alpha\) for every \(0<\alpha\le1\). The count test forces the selection coefficient to equal the mass. The rewritten population generator has the correct two losses and total rate \(q(x)=xD+2mx^\alpha\). Its integrated rate is \(3mD\), so the rate-weighted measure is a probability and bounded-test stationarity is exactly its invariance under the embedded transition kernel.

Although \(x^{-\alpha}\) need not be integrable under the population, its integral under that probability is finite because the required population moments are only \(M_{1-\alpha}\) and count. Testing the invariant measure identity with \(x^{-\alpha}\wedge k\) and using monotone convergence correctly forces the gain integral to be finite. Both sides may then be subtracted. This also handles daughter inverse moments that were not separately assumed finite. No nonexplosive path construction or time-dependent power-kernel solution is being smuggled into the stationary argument.

The symmetrization and concavity estimate give the claimed upper bound \(\alpha mN\) for the coagulation loss. Daughter Jensen gives the stated fragmentation lower bound, and their difference is strictly positive throughout \(0<\alpha\le1\). The multiplicative endpoint calculation is consistent with the same rate weighting and supplies a valid direct contradiction.

The count-neutral classification and observable-rigidity arguments also pass review. The preparation class fixes mass and allows count to vary; monodisperse and two-point substitutions determine all diagonal and off-diagonal rates. The fractional and second-moment tests then force the nonnegative coefficient to vanish. The full-time neutrality assertion includes the needed event-integrability and mass-conservation qualifications.

The power-kernel two-atom drift formula is correct, including its diagonal terms and fragmentation multiplicity. Its divergent positive term dominates the bounded negative cross term when \(p>1-\alpha\). The exact half-moment lower bound at \((\alpha,p,R)=(1,1/2,64)\) is valid. The manuscript limits this counterexample to vector fields unless an appropriate trajectory is separately established.

## Finite count, nonexplosion, and diffusion tightness

**Locations:** `sections/finite-population.tex`, Proposition `prop:finite-count`, lines 34–84; `appendices/finite-count.tex`, Proposition `prop:count-diffusion`.

The sum over distinct unordered pairs gives total death rate \(b(\ell-1)\), with birth rate \(b\ell\). A linear pure-birth bound on the event count proves nonexplosion and supplies finite moments sufficient to remove the count stopping. The count drift, squared-count drift, predictable bracket, exact variance, and constants in the maximal concentration estimate all agree. The concentration conclusion is correctly absolute when the normalized initial count tends to zero.

Shifting the count by one gives critical branching with immigration. The single-family generating function and Poisson immigration factor are correct, including the shift factor in the scaled Laplace transform. Transition convergence is uniform on bounded scaled starting states, and iteration of conditional Laplace transforms identifies the finite-dimensional limits.

The path argument goes beyond transition convergence. The scaled bracket is

\[
\int_0^\tau(2bZ_n(s)-b/n)\,ds.
\]

The nonnegative-submartingale estimate gives compact containment. Before the count-level stopping time, the bracket rate is bounded by \(2bR\); the exit overshoot does not change that time-integrated bound. The martingale isometry between the two stopped stopping times gives the asserted bound proportional to their separation. Together with the stopped drift estimate this verifies the stopping-time tightness criterion. Vanishing jump sizes make every limit continuous. The explicit two-dimensional Brownian construction then gives exactly the stated drift, diffusion coefficient, transition transform, and variance, including initial value zero.

## Finite-population discrepancy and numerical evidence

**Location:** `sections/finite-population.tex`, Theorem `thm:finite-discrepancy` and the following calculations, lines 94–275; numerical supplement.

The mass-CDF lower bound compares exactly matched empirical initial measures. The physical mass ceiling is pathwise, while the continuum fractional-moment bound is uniform in the daughter law. The selection of a single fixed fractional order for every coefficient strictly above \(1/(b\log2)\) is correct. Only an upper bound on normalized initial count is needed. The same ceiling proves the expected-mass-law version, and the relative-moment lower bound has the stated exponent. The paper does not infer earlier growing-time accuracy or a first breakdown time.

Removing the empirical diagonal gives exactly the correction \(\lambda(2-2^p)M_{p+1}/n\). Its count endpoint agrees with the independently derived drift \(b/n\). The physical process's complementary two-daughter law is explicitly distinguished from the broader expected-daughter class used in the deterministic analysis.

I inspected the simulator, runner, plot script, saved-data verifier, optional count-check wrapper, rational counterexample script, and the supplied figure. The two-stage coagulation sampler has the desired unordered pair rates. The snapshot logic retains its already sampled event time rather than restarting at observation times. Removal and tree updates are consistent with the stated dense-array representation. The figure retains all nine runs and labels the continuum references appropriately.

Independent validation in this review:

- The saved-data verifier passed all 90 snapshots, count identities, normalizations, support and half-moment checks, event totals, and saved summary comparisons.
- The power-kernel script passed the direct-versus-closed-form checks and the exact rational lower bound \(151/500\).
- A private temporary C++ build passed the supplied self-test, including weighted selection, resizing, removal, pair rates, count drift, and conservation. It wrote no shared executable or simulation data.

I did not rerun the nine research trajectories or the 2,000-seed optional diagnostic. The manuscript accurately separates those records, three-seed descriptive ranges, finite-precision checks, and mathematical results. Its numerical observations do not claim a computed continuum comparison or variance convergence.

## Sources and coverage

I checked the relevant portions of the [Tran–Van primary preprint](https://arxiv.org/pdf/1910.13424), including its rate convention and Proposition 4.3/Remark 4.4. The rescaling to the present multiplicative model is correct. The displayed stationary Bernstein identity gives first moment one and unbounded transform growth, hence infinite count; that boundary does not contradict the finite-count stationary exclusion. The citation does not substitute transformed-equation well-posedness for a general population existence theorem.

The Feller reference is contextual: the manuscript independently derives the count PGF, normalization, tightness, and continuous limiting process. Its publisher page was unavailable to this review, so I do not claim to have verified that article's full text. This does not leave a proof dependency in the stated diffusion argument.

All Stage 4 coverage items are present and consistent with the accepted earlier results. Stage 5 is outside this review.

**Final major issue count: 0. Final minor issue count: 0. Recommendation: accept Stage 4.**
