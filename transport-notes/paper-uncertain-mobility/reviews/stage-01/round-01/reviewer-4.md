# Independent review: Stage 01, round 01, reviewer 4

Reviewer: `paper_reviewer_4`. Date: 2026-09-07.

**Verdict: no major mathematical or scientific issue found. Three minor clarifications should be corrected.**

## Snapshot and independence

I reviewed snapshot `64708f8c61e751a8447d7955def9a2929c159b2bfc457eae8e2baf1900497f31`. I independently recomputed every hash in its manifest; all nine files matched. I read `sections/01-model-transfer.tex`, the author handoff, references, notation, and the relevant scope/plan. I did not read any other reviewer report or coordinate with other reviewers. The inspection covers the present model and comparison results, not the still unwritten later asymptotic theorems.

## Independent checks and reasoning

### Physical equations, normalization, and units

Integrating the bulk diffusion term gives `Db ∫Γ ∂n p = -∫Γ(Kkp-kρ)`. The wall equation adds precisely the opposite flux. With the wall concentration equal to K times the bulk concentration, both this exchange and tangential diffusion vanish. This verifies conservation, the invariant probability weights, and `V=∫Ωu/Z` for zero axial wall drift.

Integration by parts in the stated weighted energy gives the backward condition `Db ∂n f=Kk(v-fΓ)`, wall generator `(Dv′)′+k(fΓ-v)`, and the same forward system after multiplying the wall density by its equilibrium weight. The signs and factors K are consistent. The state space's disjoint bulk-boundary and adsorbed-wall copies are appropriate: surface residence and an instantaneous visit to the reflecting bulk boundary represent different states.

I checked the physical response dimensions independently. The source inverse has time units, so its arclength integral has units LT. Since `[χ]=L/T²`, the product χJ has diffusivity units L²/T. The stated nondimensional conversions, including the extra `ell_ref/k_ref` needed for dimensional scalar asymptotic constants, are correct.

### Physical process, spectral variance, and degenerate coefficients

For a closable wall preform, the bulk and wall closure norms control the bounded-rate exchange term by the trace theorem. Smooth pairs remain dense in the form norm and in continuous functions on the compact disjoint union, so the regular-form construction is applicable. The constant pair lies in the domain and has zero energy, which on this finite stationary space supplies conservativity. The positive-floor gap proof correctly gauges by the bulk mean and then passes to the smaller norm obtained by subtracting the total stationary mean.

The distinction between arbitrary scalar L¹ designs and closable physical designs is necessary and is handled explicitly. Positive-floor mixtures reconnect the two optimization problems without assuming that every formal diffusivity has a diffusion realization. Stationary initialization also avoids unsupported claims about arbitrary exceptional starting points in the process correspondence.

For the advective additive functional, stationarity gives `Var X(t)=2∫₀ᵗ(t-r)C(r)dr`. Reversibility makes `C(r)=∫e^(-λr)νg(dλ)` nonnegative. The kernel `(1-r/t)1_{r<t}` increases pointwise in t, so monotone convergence does give the extended diffusivity. A kernel component produces a t² variance term and an infinite coefficient, as the text correctly allows. Finite spectral inverse energy suffices for the linear variance asymptotic; a central limit theorem and an L² corrector are not needed.

### Schur identity and logarithmic error

At fixed bulk trace b, I independently expanded the surface square. The source is `kb-V`, its constant response is `KV²J`, its cross term is `-2KV∫kh b`, and its remaining quadratic term is `-K S(b)`. The identity `∫Ω(u-V)=KPV` cancels the constant bulk shift using `∫kh=P`. This verifies the gauge and all signs in the remainder.

For finite J without a floor, the energy-completion construction is sufficient: the constant source is continuous exactly when its quotient supremum is finite, and the reaction image gives `w=√k(√k h)∈L²`. The trace source is energy-continuous, so completing the surface square in that space is legitimate. The nonnegative residual and the bulk Poincaré estimate then make the bulk remainder finite. No illegal subtraction of infinite inverse energies is used.

As a physical consistency test, take a disk of radius R, a positive constant rate k, and plug velocity U. Then `h=1/k`, `J=P/k`, and `w=1`, regardless of D. A radial bulk trial has constant boundary trace and therefore S=0. The bulk equation gives `f′(r)=-(U-V)r/(2Db)` and remainder `(U-V)²πR⁴/(8Db Z)`, with `U-V=2KV/R`. This agrees with the stated Schur formula, including its nonnegative sign and normalization.

The logarithmic estimate uses only the mobility floor, not smoothness or an upper bound. From J≤C/m one gets `||h′||₂≤C/m`, hence `||w||∞≤C/m`. Positivity and mass give `|ŵn|≤1`, while Parseval gives `Σ|ŵn|²≤||w||∞`. Splitting the negative-half Sobolev sum at N of order `||w||∞` indeed yields `1+log(1/m)`. Pairing with the H¹ bulk trace and dropping S gives the claimed remainder bound. The one-dimensional connected-wall restriction is used, rather than silently assuming the same logarithm in higher boundary dimensions.

### Policies, information, and optimized-value transfer

The countable C¹ cores are sufficient for response measurability because smooth trial derivatives are bounded and k,D vary in L¹. This gives a Borel extension of the full smooth variational response without needing the closable-weight subset itself to be Borel. Defining the infimum over Borel policies avoids an unjustified `E inf = inf E` interchange.

The floor mixture preserves each observation's exact budget and uses no added information. Its form dominates `(1-θ)` times the original scalar form, so the inverse quotient gives the factor `(1-θ)^(-1)`. Minkowski is used only for q≥1 and subadditivity for q<1. Choosing θ=M makes the additive logarithm negligible under the precise stated growth assumption. The lower and upper optimization classes are compared in the right direction.

The root-bump lower certificate uses `ell=M^(1/5)`, source numerator of order ell², and energy at most `M/ell²+ell³`, giving the order `M^(-1/5)` independently of all spatial fine structure. The event `|c|≤1/2` has probability 1/4 under the stated marginal. Thus the lower moment bound and the observation-uniform error orders follow as written. The result concerns optimized values, not a claim that original singular optimizers all have small bulk corrections.

### Literature support and presentation scope

I opened the [publisher preview](https://api.pageplace.de/preview/DT0400.9783110218091_A15362972/preview-9783110218091_A15362972.pdf), which confirms the book's author names, second revised and extended edition, series volume 19, electronic ISBN matching the DOI, and 2011 copyright. I also checked [Li and Ying](https://arxiv.org/pdf/1701.02411), Section 3.4, which identifies FOT Theorem 3.1.6 with Hamza's closability result, and the [open regular-form application](https://arxiv.org/pdf/1308.0234), page 2, which identifies FOT Theorems 4.2.3 and 7.2.1 with the associated Hunt-process construction. The full book theorem pages are not in the publisher preview; the primary open applications support the theorem identifiers and the general correspondence used here.

No novelty claim is improperly attached to these standard tools. Detailed transport-history citations are explicitly assigned to Stage 7, so their absence from this model-only stage is not an issue requiring premature synthesis. The finite-bulk assumptions and distinction between quenched disorder moments and tracer-displacement moments are clear. The detailed form arguments may later fit better in an appendix, but that is already allowed by the synthesis plan.

## Findings

### R4-01 — Minor: explicitly state the admissibility assumptions for axial molecular diffusivity

Location: `sections/01-model-transfer.tex`, lines 233–241, and the first introduction of `Db^x, Ds^x` in lines 23–30.

The molecular term is stated for “local diffusivities” without explicitly imposing `0≤Db^x<∞` and nonnegative `Ds^x∈L¹(Γ)`. These conditions make the independent stochastic integral square-integrable under stationary initialization and justify the finite covariance/variance decomposition. The isotropic case already has them because D is nonnegative L¹. The general displayed statement should say so too.

Remedy: add the nonnegativity and integrability conditions when introducing this optional contribution, or explicitly restrict that paragraph to finite stationary mean diffusivity. This does not affect the flow-only transfer theorem.

### R4-02 — Minor: show the zero-mode trial in the variational spectral identity

Location: `sections/01-model-transfer.tex`, lines 252–257.

The text says spectral cutoffs of `λ^(-1)g` establish the reverse variational inequality “including an infinite value.” Positive-spectrum cutoffs do establish an infinite integral from λ approaching zero, but by themselves do not recover a positive atom exactly at zero. The preceding resolvent explanation and stationary spectral discussion already handle that case, so this is a small completeness issue in the purportedly self-contained alternative proof, not a theorem-level gap.

Remedy: add that if `g0` is the nonzero projection onto the kernel, trials `w=t g0` have zero energy and linearly unbounded source pairing; otherwise use the positive-spectrum cutoffs. Alternatively use the epsilon-resolvent argument consistently for both cases.

### R4-03 — Minor: define closability before using it as the physical-class boundary

Location: `sections/01-model-transfer.tex`, lines 102–116.

Closability is the decisive difference between the scalar and physical optimization classes, but is only named and cited before those classes are defined. The positive-floor proof later exhibits its sequence criterion without stating that this is the definition. A transport reader unfamiliar with Dirichlet forms would benefit from one sentence explaining the precise condition and its role.

Remedy: state the sequence criterion explicitly: if `vn→0` in L² and `eD[vn-vm]→0`, then `eD[vn]→0`. Explain briefly that this ensures that passing to the energy completion defines an unambiguous closed diffusion form in the physical state space. No long functional-analysis digression is needed.

## Overall assessment

The stage establishes the intended bridge from stationary transport to unrestricted scalar design without assuming nonexistent rough-coefficient processes or correctors. The proofs and transfer claims survived this independent check. After the minor clarifications and their verification, I find no Stage 01 mathematical reason to delay the next stage. Later sharp scalar asymptotics and publication-level literature novelty remain outside this verdict.
