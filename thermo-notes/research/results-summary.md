# Results of the completed research pass

Exploratory research closed 2026-09-07 at the user's request. The existing finite-reservoir developments were subsequently completed and assembled in [the 48-page LaTeX paper](../paper-finite-reservoirs/README.md). All five author stages and two whole-paper review rounds are complete, with every accepted issue corrected; the full record is in [WORKFLOW.md](../paper-finite-reservoirs/WORKFLOW.md). No unrelated research direction was opened.

The strongest outcome is a set of physical finite-reservoir theorems, consolidated in [Finite reservoirs at phase coexistence: full-state accuracy and phase correlations](../paper-finite-reservoirs/main.pdf). Their mathematical claims have independent support. The bounded open-literature audit found close precedents but no exact predecessor for the combined sharp classification. This supports a manuscript candidate for expert review, not a certification of novelty or publication readiness.

## 1. Sharp physical reservoir-size classification

The bath has density of states proportional to `U_B^c` for positive bath energy; its surface-entropy heat capacity is `k_B c`. The target is the complete canonical probability law of the subsystem. Distance is total variation (TV), which controls every bounded observable. Only composite total energy is optimized; the target canonical temperature is specified.

**General support theorem.** If `(E_N−a_N)/b_N` converges weakly to a probability law with at least three support points, where `b_N→∞`, canonical accuracy is achievable if and only if `c_N/b_N²→∞`. No density, Gaussian, moment, or tail assumption is needed. The proof uses the exact concavity of the logarithm of the physical bath weight. Exactly two energy atoms can instead be matched at any positive capacity, so the support condition is essential.

**Two-phase refinement.** Suppose two phases have positive limiting weights and centers separated by `Δ_N`. At least one phase has a nondegenerate weak fluctuation limit at scale `s_N`, with `s_N→∞` and `s_N/Δ_N→0`, and the other concentrates within `o(Δ_N)` of its center. Full accuracy then necessarily requires `c_N≫Δ_N s_N`. Suitable phase-tail control makes this sufficient. At ordinary first-order coexistence, `Δ_N` is of order `N` and `s_N` of order `√N`, giving `c_N≫N^(3/2)`. The sufficient tail assumptions and alternative positive-mixture criterion are explicit; weak phase limits alone do not prove sufficiency.

**Microscopic realizations.** The N^(3/2) iff result holds for three-state mean-field Potts spins with or without quadratic kinetic degrees. Ordered spins alone supply the nondegenerate fluctuation required for necessity. Exact continuous-energy calculations reach 12,000 spins. For plain nearest-neighbor Potts spins at sufficiently large fixed q, the iff result is now proved in every fixed spatial dimension d>=2. The previously missing sufficient phase-energy bound follows from positive contour restricted-partition estimates and conditional binomial transfer from occupied bonds to actual spin energy. See the [complete microscopic statement](../paper-finite-reservoirs/sections/microscopic.tex) and [contour appendix](../paper-finite-reservoirs/appendices/short-range-proof.tex).

Proofs and evidence: [support classification](reservoir-support-classification.md), [physical two-phase theorem](finite-bath-physical-extension.md), [positive-mixture criterion](phase-decomposition-reservoir-criterion.md), [mean-field model](potts-physical-bath.md), [short-range model](short-range-potts-route.md), and [independent support-theorem review](verification/three-support-bath-review.md).

## 2. Correct subsystem marginals can conceal persistent bath-induced correlations

Take two identical coexisting systems of size N, initially independent, with positive limiting phase weights, phase-energy separation proportional to N, and tight conditional energy fluctuations on scale `√N`. Center their common physical bath at the total energy of an opposite-phase pair. In the window `N≪c_N≪N²`, their full joint law approaches the canonical product conditioned on opposite phases.

For balanced canonical phase weights:

- Each complete subsystem marginal approaches its canonical law in TV.
- Joint TV distance from the independent canonical product approaches `1/2`.
- Full microscopic mutual information approaches `log 2`, or one bit.

Thus checking either subsystem separately can miss a persistent error in their joint equilibrium statistics. For unequal positive canonical phase weights, the bath still produces equal opposite-phase assignments; the marginal TV error becomes `|w_−−1/2|`.

The pair has three macroscopic total-energy support points. Consequently **joint** canonical accuracy is achievable if and only if `c_N≫N²`. This is a complete result for two copies of the plain short-range large-q Potts model and uses only macroscopic support, independently of the stronger isolated-copy phase-tail theorem. For that model, balanced target weights require the stated finite-size inverse-temperature adjustment, rather than the unadjusted coexistence temperature.

The lower boundary is also resolved for the specified centered bath. If `c_N/N→γ>0` and conditional energy fluctuations have positive weak Gaussian limits with variances `v_−,v_+`, then, writing `a=β²/γ`,

\[
 I\longrightarrow \log2+\frac12\log
 \frac{(1+av_-)(1+av_+)}{1+a(v_-+v_+)}.
\]

The extra term measures correlated within-phase fluctuations. Each marginal has a strictly positive TV error even at balanced weights. Exact covariance and TV formulas are proved. The entropy limits use bounded likelihood arguments; they are not inferred from TV continuity of entropy. No arbitrary-calibration lower-scale necessity is claimed.

See [the complete derivation](shared-bath-phase-correlations.md), [independent review](verification/shared-bath-review.md), and [prior-art audit](verification/shared-bath-prior-art.md). Opposite-phase locking and locally thermal but globally correlated states are established phenomena. The candidate contribution is the quantitative full-law result and its physical bath-size classification.

## 3. Two further verified candidates

**Survival-conditioned thermodynamic integration.** In reversible killed networks with fixed transition-state conductances, occupations sampled in the interior of long surviving trajectories derive from an exact spectral potential. Endpoint-survivor occupations generally do not: an exact three-state example violates Maxwell symmetry. Their normalized geometric-mean relation to canonical and interior-survivor laws gives a quantitative force-integration error bound, of second order in weak killing under a spectral-gap condition. A response identity includes an escape-rate-weighted autocovariance integral. Changing how conductances depend on control parameters can restore a first-order defect, so detailed balance alone is insufficient. Endpoint-assembled force integration is also distinct from mechanical work conditioned on survival of the entire protocol. See [the theorem and scope](survival-conditioned-thermodynamics.md), [independent mathematical review](verification/survival-thermodynamics-review.md), and [prior art](verification/survival-prior-art.md).

**Interfacial energy from bulk response in an explicit variational model.** A positive nonlocal double-parabola model admits exact planar tension and finite spatial-window response certificates, with controlled truncation error. Matching interaction mass, second and fourth moments, and a common interaction-range bound does not determine tension; smooth positive examples retain distinct tensions. The response is the homogeneous variational Hessian response, not the exact structure factor of a fluctuating microscopic Gibbs model. The finite-moment extremizers are sharp in the strong-well limit; no exact finite-well extremizer or general nucleation-barrier theorem is asserted. See [the results](interfacial-inference-scout.md), [independent proof review](verification/interfacial-inference-review.md), and [prior art](verification/interfacial-inference-prior-art.md).

Both are credible mathematical candidates with substantial established ingredients. Their priority remains less clear than their correctness within the specified models.

## 4. Retained findings and corrections

The repository also preserves useful capacity certificates, finite-field rate bounds, droplet stability criteria, and finite-record kinetic bounds. They are not presented as major new methods. In particular, the planar channel inequality reproduces the classical Ahlfors–Warschawski result, and the central stabilized-saddle reconstruction reproduces published restrained-fluctuation/Grote–Hynes work. Those negative novelty findings are documented to prevent rediscovery claims.

Final consolidation incorporated reviewer qualifications into the main notes: the capacity extension requires the correct coarea measure, tangent mobility, and compatible boundaries; the droplet singular-value test requires a positive semidefinite reservoir Hessian and certifies strict quadratic stability only on the specified subspace. General reversible kinetics do not inherit the survival theorem’s fixed-conductance protection.

## 5. Verification and remaining limits

Independent subagents re-derived the principal results and challenged cutoff behavior, weak-limit arguments, entropy limits, boundary conditions, stability claims, and prior-art wording. The earlier [Markdown manuscript](reservoir-coexistence-manuscript.md) and [shared-bath note's linear-capacity development](shared-bath-phase-correlations.md) completed their historical review cycles. Review status for the subsequent LaTeX manuscript, including its separate whole-paper review, is recorded in [WORKFLOW.md](../paper-finite-reservoirs/WORKFLOW.md). Reproducible scripts and saved outputs are linked from [the repository index](../README.md).

Numerical evidence includes independent spin enumeration and energy-density integration for the finite-bath formulas, exact occupancy calculations through N=12,000, 120 reversible-network capacity checks, 200 random Schur-complement checks, 250 harmonic kinetic checks, and 150 survival-network checks. Driven survival calculations test the protocol distinction. Shared-bath quadrature tests the exact power-law bath on a Gaussian phase benchmark; it is not a short-range Potts simulation. Numerical evidence supplements the analytic proofs and does not replace them.

Remaining limits include historical priority, microscopic realizations beyond the stated models, and the all-gamma short-range boundary in two dimensions. Isolated short-range sufficiency is no longer unresolved. The exact Gaussian optimal phase-loss equality and physical boundary optimization over all composite energies are also completed in the paper. Its capillarity tie weights are nonidentifiable from a leading rate function alone, an explicit model limitation rather than an unfinished theorem. No confirmed wholly novel publication is claimed. The completed manuscript candidate and supporting notes are ready for technical assessment by Corti or another specialist in molecular and finite-system thermodynamics. Nothing has been submitted, published, or sent externally.
