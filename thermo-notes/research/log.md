# Research log

## 2026-09-06 — First investigation cycle

Initial inventory found a substantial literature knowledge base, eight topic syntheses and a research roadmap, but no separate original-result notes. Corti's current Purdue profile confirms molecular thermodynamics, finite systems, soft condensed matter and simulation as appropriate scope ([profile](https://engineering.purdue.edu/ChE/people/ptProfile?id=11551)).

Independent scouts explored finite reservoirs and nucleation response while the main investigation developed a conditional transport certificate for reactive capacity. Independent reviewers checked each mathematical direction. Notes distinguish stationary transition flux, capacity divided by basin mass, last-visited-state rates, and inverse mean first-passage times.

Useful candidate: the complete two-phase Gaussian energy distribution needs reservoir heat capacity growing faster than N^(3/2) for total-variation convergence, even after retuning the bath temperature. A specified untuned bath can require N^2. Early Gaussian-ensemble work already contains the quadratic bath mechanism. The 1986 and 1988 full texts were checked without finding the exact probability-metric threshold; a 1990 review remains inaccessible. The main next task is a physical-bath and interfacial-valley extension.

Useful mathematical synthesis: a projected capacity upper bound can be paired with a positive lower bound using a divergence-free current that transports conditional equilibrium distributions. The correction equals a conditional score Poisson cost. Gaussian examples and reversible networks check the result. Conditional friction, Wasserstein geometry, and stiff-projection failures have prior art and are not new.

Negative novelty finding: the apparent all-slope corrugated-channel diffusion bound is exactly the classical Ahlfors–Warschawski geometric modulus inequality. Its equivalence to the Zwanzig resummed diffusion approximation is useful context, but the bound is a rediscovery. Higher-dimensional weighted modulus theory is also close prior art. This finding prevents a premature publication claim.

Useful nucleation response synthesis: fixed-mobility conductance tilts give finite-field moment bounds and a sharp plus/minus covariance sandwich. Independent network checks passed. First-order sensitivity and conductivity comparison principles are established; the precise standalone novelty remains unproved.

Research continues with physically controlled finite-reservoir coexistence and phase-geometry extensions. None of these milestones completes the user's open-ended objective.

## 2026-09-06 — Physical reservoirs and a microscopic example

The two-phase threshold now has a physical constant-heat-capacity bath proof, with explicit local energy and valley-tail hypotheses. Optimal total-energy calibration preserves the full canonical law precisely when c/N^(3/2) diverges. At the boundary scale, the phase peaks shift and their weights generally change. A conditional two-dimensional capillary calculation also identifies competition between bath feedback and interfacial suppression; its microscopic short-range hypotheses remain unproved.

Three distinct phase energies behave differently: an exact physical bath needs c/N² to diverge even after arbitrary total-energy tuning. Independent review confirmed the necessity proof using strict concavity and the sufficiency proof without a valley-envelope assumption. The energy distinctions matter: several ordered phases with the same energy do not count as several distinct thermal peaks.

A mean-field three-state Potts model with quadratic kinetic degrees supplies an exact microscopic example for the two-phase theorem. The local energy limits and uniform Gaussian envelope have been derived and independently reviewed. Exact occupancy sums and Gamma/Beta interval probabilities give total-variation distances through 12,000 spins. Independent explicit spin enumeration and direct energy-density integration agree with the calculation. Numerical guard checks now reject unresolved likelihood crossings or potentially significant probability lost to underflow.

The expanded [novelty audit](verification/physical-reservoir-novelty-audit.md) found established quadratic bath-size sufficiency in a strong probability metric (Riera, Gogolin, and Eisert, 2012), as well as older sharp conditioning results. The candidate contribution is the optimized two-phase exception and sharp three-phase necessity, not a new general N² sufficient bound or a new finite-bath marginal. The audit supports an internal manuscript candidate, with novelty still provisional.

## 2026-09-06 — Further stability and kinetic directions

A common reservoir changes a collection of droplet Hessians by a matrix of rank at most the number of exchanged quantities. This gives a local instability count and a quantitative penalty when distinct droplets have nearly parallel depletion vectors. Composition relaxation screens reservoir stiffness and can invalidate a frozen-composition stability prediction. Identical-droplet exchange instability and single-droplet compressibility screening have close, explicit prior art. The remaining distinct-droplet application needs a physically convincing mixture model before further novelty claims.

A separate kinetic investigation asks whether stable equilibrium fluctuations determine the unstable growth rate after removing a harmonic stabilizer. The linear reversible identity is closely related to established restrained-simulation/Grote–Hynes methods. Current work focuses on finite-observation bounds and what common correlation-time summaries fail to determine. These are research candidates, not validated claims of new physics.

The kinetic reconstruction audit subsequently found exact algebraic equivalence to a published 2013 implementation based on Straub and colleagues' 1988 method. Finite-record bounds and sharp moment-information limits were verified and retained as modest findings; they do not justify a major-method novelty claim.

## 2026-09-06 — Second research cycle

A focused reservoir manuscript passed a fresh-reader proof audit. An alternative positive phase-decomposition lemma now proves convergence using only a fixed exponential moment within each phase plus a sufficiently rare exceptional component. For short-range large-q Potts models, a primary real-temperature partition expansion supports a route to conditional weak energy limits and the necessary bath scale. The required inward spin-energy exponential-moment control is still missing, so a full short-range iff theorem has not been claimed.

A Hamiltonian-uncertainty scout obtained a reviewed mixed-scale coexistence limit and an example where restoring phase weights leaves large within-phase TV error. Generalized Clapeyron curvature and potential fitting at coexistence have strong prior art; the retained result is a diagnostic with modest, unresolved novelty.

The most promising new direction in this cycle is [survival-conditioned thermodynamic integration](survival-conditioned-thermodynamics.md). In a reversible killed Arrhenius network with fixed transition-state conductances, interior-survivor occupations are the gradient of log escape rate, whereas endpoint-survivor occupations can violate Maxwell symmetry. An exact three-state counterexample was independently checked. The endpoint law is a normalized geometric mean of two laws with exact potentials, giving a Hellinger bound on path-dependent force integration and an O(ε²) error for weak killing. A separate response identity adds an escape-rate-weighted Doob autocovariance integral to the usual variance term.

Independent mathematical review, 150 random-network checks, and forward/backward driven survival calculations support the statements. The protocol caveat is essential: the nonzero endpoint-assembled force integral is not the mechanical work of a trajectory conditioned to survive the entire slow cycle; the latter tends to zero in the examined fixed-conductance setting. Focused novelty assessment remains in progress.

## 2026-09-07 — Short-range necessity and further inference results

The remaining source check for short-range necessity is now complete. The original Borgs–Kotecký–Miracle-Solé theorem supplies the required real-temperature expansion uniformly on a fixed neighborhood, with the correct nearest-neighbor Hamiltonian and periodic geometry. Combined with the independently reviewed weak-limit deduction and kinetic smoothing, it proves the N^(3/2) necessary bath scale for the two-dimensional sufficiently-large-q Potts model. Sufficiency remains open because the inward phase-energy tail estimate is still missing.

The survival prior-art audit found no exact duplicate of the fixed-conductance Hellinger force-integration bound in the inspected sources. It also confirms substantial prior art for its ingredients and related response identities. An independently verified alternative reversible control family gives a first-order Maxwell defect, demonstrating that the quadratic cancellation is specific to how the barriers are controlled.

A further investigation develops exact interfacial-energy inference in a nonlocal double-parabola free-energy model. Independent review verified the positive resolvent construction, planar minimization, finite-moment ambiguity, and finite spatial-window error bounds. Its homogeneous response is a deterministic Hessian response; it is not the exact finite-temperature structure factor of a nonlinear fluctuating field. Close prior art covers the elimination method and bulk slab-response integral, so the candidate contribution is the quantitative inference statement within this specified model.

The reservoir obstruction has now been simplified substantially. If energy rescaled by b_N has a weak limit with at least three support points, optimal TV preservation holds iff c_N≫b_N², without any density, CLT, moment, or tail assumptions. Two independent reviewers verified the exact log-bath chord proof. Its unequal-spacing version gives the two-phase necessary scale Δ_Ns_N from weak within-phase fluctuations alone.

Two independent coexisting systems sharing one bath yield a stronger microscopic application. In N≪c_N≪N², a centered bath selects opposite phases. Balanced individual marginals converge to their complete canonical laws, while joint TV error tends to 1/2 and full microscopic mutual information tends to log2. The latter uses a separate bounded relative-entropy argument, not continuity of entropy under TV. For any positive phase weights the output phases rebalance equally; a fixed-number-of-copies extension selects a prescribed phase count.

A conditional-variance bound on independent lattice sites proves that the short-range Potts phase energy variances are positive. Kinetic smoothing is therefore unnecessary for these short-range statements: plain large-q Potts spins suffice. A pair has three macroscopic total-energy values, giving a full joint-law c_N≫N² iff theorem without the still-missing isolated-copy tail bound. Equal-weight finite-size temperature tuning is justified separately. Opposite-phase locking itself is known; the [shared-bath audit](verification/shared-bath-prior-art.md) did not locate the specified full-marginal TV and capacity-scale result.


## 2026-09-07 — Final consolidation and closure

The user narrowed the objective to finishing current developments and stopping. No new research directions were started after that instruction. The remaining shared-bath linear-capacity calculation is complete: at c_N/N→γ>0 the opposite-phase energy fluctuations acquire an explicit Gaussian covariance, balanced subsystem marginals retain positive TV error, and full microscopic mutual information equals log2 plus a positive fluctuation term. Independent review checked the cutoff, complete marginal TV limit, and both relative-entropy limits.

Final audits approved the expanded reservoir manuscript, weak-support classification, and plain-spin short-range variance argument. The source audit was updated to those final statements and retained the known precedents and unresolved priority limits. Earlier capacity and droplet notes now incorporate the reviewers’ geometric, boundary, and strict-stability qualifications. Stale pending-review statements have been replaced by completed review references where applicable.

The [results summary](results-summary.md) records the final conclusions, evidence, retained rediscoveries, and scope limits. The principal unproved extension is isolated short-range two-phase sufficiency; it is not needed for the proved pair joint-law threshold. No result is represented as having certified literature priority, and nothing has been submitted or sent externally. This research pass is closed at the user’s request.
