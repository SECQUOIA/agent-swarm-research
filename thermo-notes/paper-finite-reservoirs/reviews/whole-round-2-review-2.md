# Whole-paper round 2 — independent reviewer 2

Recommendation: accept the revised manuscript. No major or minor revision request remains from this review.

I read the complete current `main.tex` and all 11 section/appendix inputs, including every theorem and proof, and reread the bibliography, numerical presentation, README, and coverage audit. I read the permitted round-1 adjudication and corrections records, but no other reviewer's report. My previous independent source and numerical checks informed the reassessment of unchanged material; the current 48-page manuscript is the target of this recommendation. I made no manuscript edits and did not delegate.

## Verification of every accepted correction

**Nonnegative curvature in the standalone necessity proposition.** `prop:smooth-necessity` now explicitly assumes `kappa_N >= 0`, independently of the sufficient theorem. This excludes the stated negative-curvature-scale counterexample. I rechecked the sign of the modified concave function and the chord identity: the chord defect is at least

`(k kappa_N/2) (y_N-x_N) (z_N-y_N)`.

The product of spacings is comparable to `N^(3/2)`. The nonnegative right side is bounded above by a quantity tending to zero, which now establishes the literal conclusion. The case `kappa_N=0` is included without difficulty. The physical-reservoir applications use positive curvature scales and are unaffected.

**Nonnegative vector-Gaussian curvature.** The vector model now states `kappa_N >= 0` at its own definition. This ensures a positive denominator in the completed-square formulas and transformed covariance no larger than the target covariance. Those are precisely the properties used in component matching and the phase-loss proof. The scalar and anisotropic formulations remain consistent with this sign convention.

**Contour-cap wording.** The phrase is now “positive exponential cap.” This resolves my round-1 wording request. The actual proof continues to use absolute continuity and first derivatives almost everywhere for the minimum-truncated system, obtains the Lipschitz free-energy bound, removes all cutoffs in the finite-size temperature window, and only then takes second derivatives. The wording and argument now agree.

**Leading canonical coexistence heat capacity.** The new paragraph is restricted to the verified microscopic examples and states only the justified leading limit. Boundedness of `U_N/N`, together with the two-atom weak limit, gives convergence of its first and second moments. Hence

`Var(U_N)/N^2 -> w_- w_+ (u_+-u_-)^2`.

For independent kinetic energy of Gamma shape `aN`, the variance addition is exactly `aN/beta_N^2`; after multiplication by `beta_N^2/N^2`, this adds `a/N`, which vanishes. The gap is unchanged by the common kinetic mean. The finite canonical identity `C_S,can/k_B = beta_N^2 Var(E_N)` therefore gives the displayed limit with the Hamiltonian held fixed. This remains consistent with the prescribed balancing shifts, where the limiting weights change as already stated in the shared-bath section.

The positive phase moments imply an `O(N)` bound on within-phase variance, including the degenerate disordered mean-field spin phase. The paragraph does not turn this into an unjustified `O(N)` remainder for the total variance expressed using limiting weights. Its conclusion that `N^(3/2) << c_N << N^2` permits full-law accuracy with a smaller bath heat capacity is supported by the two verified microscopic threshold theorems. The surface/canonical bath-capacity offset is still explained separately in the framework.

**New capillarity attribution.** I independently read the retained primary texts, not just the corrections record. Biskup–Chayes–Kotecký's abstract distinguishes the rigorous two-dimensional Ising setting from heuristic generalizations; its page 2, equations (1)–(2), explicitly compares background fluctuation and droplet surface costs. Kim–Keyes–Straub's page 3 specifies a toroidal two-dimensional Potts model, and the page-4 discussion of Figure 3 describes droplets, strips, and droplet/strip transition markers. The new manuscript sentences credit exactly this physical motivation. They neither import a full energy-density envelope nor assert that these sources derive the manuscript's square-torus rate for its microscopic models. The added bibliography entries identify the sources actually inspected.

## Whole-paper mathematical reassessment

The revised introduction, framework, abstract, main theorems, appendices, and conclusions have consistent scope. The new heat-capacity observation does not add a moment assumption to the general weak-support theorem or claim that weak convergence alone always controls unbounded observables.

I rechecked the exact power-law likelihood, admissibility, surface-capacity convention, energy/full-state TV equality, centered global bound, and secant calibration. The weak-support necessity proof continues to handle arbitrary total-energy choices and the physical cutoff through good-energy selections. The unequal-scale argument supplies its third relevant energy from one nondegenerate phase. Sufficiency retains separate positive phase moments and amplified exceptional mass; the density-envelope alternative retains its own explicit hypotheses.

The mean-field minimum classification, Hessians, relative phase weights, conditional energy variances, positive moment bound, and exact Gamma/Beta formulas remain valid. The ordered energy variance already proves the pure-spin necessity; the disordered square-root-scale degeneracy is preserved in every subsequent applicability statement.

I reread the full short-range appendix, including its unchanged original-source inputs. The spin/random-cluster normalization, original BCT exterior convention, stable-side free-energy identification, real one-sided transform proof of phase CLTs, and stable-branch variance positivity remain consistent. The activity derivative estimates, exponential cluster majorant, cutoff removal, and fugacity-to-spin-energy transfer preserve the needed positive probability control. The exceptional surface estimate yields the stated threshold in every fixed dimension at least two. The boundary extension still uses every fixed exponential parameter only in dimensions above two; the two-dimensional result retains the necessary strict moment and surface-gain restrictions.

The shared-bath results still distinguish disjoint microscopic phase events from auxiliary decompositions, specified balancing temperatures from fixed unbalanced targets, and marginal accuracy from joint accuracy. The bounded-likelihood entropy argument remains separate from TV convergence. The linear-capacity formulas retain their positive-variance scope, so they do not silently cover the degenerate pure-spin mean-field phase.

The physical boundary theorem retains integrability stronger than the limiting tilt and a separate exceptional-mass assumption. Its optimization over every calibration correctly includes phase loss and uses overlap in both phases to control all competing calibrations. The Gaussian sphere classification and optimal phase-loss proof retain the treatment of escaping fields/centers. The anisotropic remark remains limited to its finite-size algebra. The capillarity LDP, tied-minimum qualification, square-torus minimizers, histogram-norm example, and fixed-energy barrier identities remain clearly separated from microscopic morphology or dynamical claims.

## Verification and presentation

I inspected all 48 current PDF pages through page contact sheets. The additions are present and no clipped equations, figures, or bibliography entries were apparent. The current build log has no warning or overfull/underfull box entries. An independent source audit found 214 labels with no duplicates or missing references and 25 cited bibliography keys with none missing.

The archived numerical dataset still has SHA-256 `93fed9507ceaf9126feb93e79ae5bbb295be185a56f9a84dabe0608e55aab2c1`. The revised text does not change its formulas, plotted values, or interpretation. I did not repeat numerical runs in this round: my previous explicit small-spin enumeration, two direct-density quadratures, weighted-normal/compensation checks, and four-regime size-300 recomputation already tested the unchanged calculations. No size-12000 computation was repeated.

All accepted corrections are resolved and integrated without a new scientific or presentation defect. No further action is requested by reviewer 2.
