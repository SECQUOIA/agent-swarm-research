# Stage 4 independent review: readability, mathematics, and reproduction

I reviewed both new sections and both new appendices in full, their use of the accepted earlier results, the new figure and table, the supplement source and reproduction commands, the bibliography, README, and coverage map. I did not read other current Stage 4 reports or communicate with other reviewers. All builds and executed calculations used an isolated copy at /tmp/stage4-readability-u4a844vr; no manuscript, figure, data, or build artifact in the shared directory was changed.

**This review is clean: I found no major or minor issue requiring correction.**

## Mathematical review

The finite-population construction and the continuum comparison use compatible normalizations. Pair rates sum to \(b(\ell-1)\), while physical fragmentation has rate \(b\ell\). Eventwise complementary splitting is explicitly required, and the text does not pretend that an arbitrary expected daughter measure specifies the finite process. Pure-birth domination justifies nonexplosion and the finite-horizon moment calculations.

The count generator, variance, martingale bracket, and uniform concentration constants are correct. The result allows \(c_n\to0\) and properly distinguishes absolute count accuracy from relative accuracy. The \(b/n\) normalized drift and the fractional-moment diagonal correction have the correct factors and signs.

The mass-CDF theorem compares the finite system and the continuum solution from the identical empirical initial measure. The physical ceiling is \(nm\), and the continuum bound at that ceiling is
\[
\bar\pi_t^n((0,nm])\le (nc_n)^{1-p}e^{-b\kappa_p t}.
\]
Choosing a fixed \(p<1\) from the endpoint limit of \(\kappa_p/(1-p)\) proves the stated sufficient logarithmic horizon uniformly under the declared count bound. A uniform initial second-moment bound is not needed. The expectation version preserves the same ceiling. The relative-moment consequence does not claim a nonvanishing absolute error, and the theorem does not assert accuracy before the sufficient failure horizon.

The count appendix correctly shifts by one to obtain critical branching with immigration. Its generating function has the required immigration factor. The scaled transition transforms converge uniformly on bounded initial states. The stopped martingale estimates establish path tightness, vanishing jumps make the limits continuous, and the finite-dimensional laws identify the limit. The two-dimensional Brownian construction gives the stated drift, diffusion coefficient, Laplace transform, and moments, including the initial state \(c=0\). This later count scale is clearly distinguished from the earlier mass-discrepancy scale.

The universal count-neutral classification is proved by one- and two-point preparations at fixed mass with varying count. The converse uses the complete weak count balance with event integrability. The additional fractional-moment and second-moment rigidity calculations have the correct constants and imply zero rates only under the advertised universal preparation hypothesis.

The unbounded-observable appendix supplies the needed admissibility argument. Subtracting the tangent slope makes the truncated test bounded. Both the tangent truncation and its remainder are convex with value zero at the origin, giving the signed increment bounds even for the entropy test, which takes negative values near zero. The displayed event majorants are integrable under locally bounded second moments. Dominated convergence therefore gives complete integrated balances and local absolute continuity. The argument for continuity in second-moment weighted variation at zero is sufficient for the entropy right derivative and the instantaneous sharpness assertion.

The resulting second-moment growth interval, exact equal-split growth, and sharp entropy production constant \(\lambda m^2\log2\) are correct. The comparison with a static model starts from the same initial measure and correctly shows arbitrarily large broadening while preserving the three stated bulk outputs. It does not imply finite-time gelation.

For the power kernels, finite count and mass make the total event flux finite. Count stationarity forces \(s=m\). The rate-weighted invariant transition kernel makes \(x^{-\alpha}\) integrable through \(M_{1-\alpha}\) and count, without assuming a negative population moment. Truncated stationarity legitimizes the gain/loss subtraction. The symmetrized coagulation estimate and daughter Jensen bound give the stated strictly positive drift contradiction for every \(0<\alpha\le1\).

The positive fractional-moment counterexample has the correct diagonal, cross, and fragmentation terms. Its large-\(R\) condition is stated correctly, and the half-moment example has the certified positive lower bound. The text appropriately treats these as vector-field counterexamples without claiming a time-dependent existence theorem for the power model. The infinite-count multiplicative equilibria are separated from the finite-count exclusion.

## Exposition and scope

The new material is coherent despite covering several distinct consequences. The finite-population section first proves the count statement, then the mass-CDF obstruction, and only then introduces numerical illustrations. The boundary section makes the transition from exact algebraic identification to broadening and then to the limits of the additive theory explicit. The technical appendix placement keeps the main argument readable while retaining the necessary proof details.

The finite simulation versus continuum distinction is unusually clear and sufficient for the intended reader:

- The manuscript explicitly states that no continuum PDE solution is computed.
- The dashed count and half-moment curves and the shaded mean-log interval are identified as continuum references, not finite-path bounds.
- All nine declared runs and all ninety snapshots are retained, including the low-count run.
- Three-seed ranges are described as descriptive ranges, not confidence intervals.
- The very weak discrepancy certificate at the simulated horizon is quantified, so the plots are not presented as a numerical proof of nearly maximal continuum error or a first breakdown time.
- Log-variance observations are not promoted to a consequence of first-order transport or weak convergence.

I visually inspected the manuscript pages containing the table and six-panel figure. Panel labels, axes, reference curves, and captions are readable at manuscript scale. The figure's colors consistently identify system size; the caption explains that each color contains three seeds. The table's normalizations and its min–max meaning are explicit. The float placement does not obscure the interpretation.

The earlier solution class, fractional constants, transport bounds, and count-normalization conventions are used consistently. The new power model has its own stationary definition and does not silently inherit the additive existence theorem. The current README and coverage map accurately distinguish accepted earlier stages from the current review and future Stage 5. Missing introductory and Fourier material is outside the present scope.

## Reproduction and references

The isolated LaTeX build succeeded and produced a forty-three-page PDF. The final log had no unresolved citations or references, rerun warnings, overfull boxes, or underfull boxes.

I read the C++ event loop, array/tree operations, sampler, snapshot normalization, and self-tests, together with all new Python scripts. The event-clock handling does not restart waiting times at snapshots. Selecting one mass-weighted particle and then a distinct uniform partner gives the specified unordered additive rate. The finite-precision qualifications match the implementation, including the 53-bit uniform draws and possible loss of small cumulative weights.

In the isolated copy I executed:

- Saved-data verification: all ninety rows, count identities, mass checks, CDF ranges, event totals, and saved summary values passed.
- Figure regeneration: the plotting command completed successfully from the saved CSV.
- The power-kernel verification: direct and formula calculations agreed, and the exact rational lower bound was certified.
- The full nine-run particle runner, including its built-in self-test: all runs completed, processing 6,588,932 events. The regenerated CSV was byte-for-byte identical to the archived CSV on this platform, and all numerical time-ten summaries matched exactly.
- The separate 2,000-seed count diagnostic: it reproduced mean 60.473, unbiased variance 1098.2614017008505, minimum count one, and standardized mean error 0.6407120465587508.

The documentation correctly warns that timing/platform metadata and seeded paths may differ across environments; byte-for-byte equality here is a reproduction result on this platform, not a stronger portability guarantee. The unavailable historical sanitizer harness is disclosed as unarchived rather than represented as a supplied reproducible test.

The contextual diffusion attribution agrees with [Giorno–Nobile](https://www.mdpi.com/2227-7390/9/16/1879), which treats birth–death immigration approximations to Feller-type diffusion. The equilibrium discussion matches [Tran–Van, Proposition 4.3 and Remark 4.4 in the cited preprint](https://arxiv.org/pdf/1910.13424v3): the stationary Bernstein transform satisfies the displayed implicit relation. The normalization \(n_t=m c_{2mt}\) gives the claimed kernel and selection rate, and the large-transform-argument calculation establishes infinite count.

**MAJOR count: 0. MINOR count: 0. Recommendation: accept Stage 4. No correction is required by this review.**
