# Can transport bound the escape of locally formed O2?

Date: 2026-09-15. Independent mathematical check of the [oxygen-return calculation](epoxidation-oxygen-return.md), [isotope feasibility review](../reviews/epoxidation-isotope-feasibility.md), and [balance review](../reviews/epoxidation-balance-review.md). No catalyst dimensions, transport coefficients, instrument performance, or local capture rates are assumed to have been measured.

## Conclusion

**A validated reaction–diffusion model can supply a conservative positive escape bound for O2 already in the gas population that the model describes. The current inlet-tracer proposal does not, by itself, validate that model or its worst local sink.** The bound is useful only if its lower uncertainty limit is large enough to resolve the required return flux. A mathematically positive but arbitrarily small number does not rescue the experiment.

This adds a conditional feasibility gate, not an established measurement capability. Use existing working-state transport and uptake evidence to assess the gate. If those data cannot exclude a fast source-associated sink, retain the observed escaping mixed-O2 flux as the result and do not commission a new instrument campaign on the strength of this calculation.

The model cannot bound pre-bulk/geminate recapture or surface `O2*` reuse. Even thermalization of translational energy does not automatically establish that a molecule born beside a wall has entered the spatially averaged pore-gas population. That distinction must remain explicit when comparing the bound with the return required by the chemical balance.

## 1. Quantity and minimal model

Let `p(x)` be the probability that a mixed-isotope O2 molecule starting at position `x` reaches a specified escape boundary before its detectable identity is lost. At a fixed working state assume:

- The molecule belongs to a diffusing pore-gas population with a constant, isotropic transport coefficient `D > 0`.
- Loss of the intact mixed-O2 signal has a first-order hazard `k ≥ 0`, independent of the dilute tracer concentration. Loss includes reaction or isotope replacement. Counting every adsorption as permanent loss is conservative if the adsorption hazard itself has a valid upper bound; reversible intact release can only improve survival over that construction.
- The slab or sphere is a valid transport domain, with the boundary conditions given below. It is not merely a drawing around an unresolved pore network.
- All rate and transport coefficients use the same gas-storage convention. In a porous-medium balance, divide transport and volumetric loss by the same gas capacity before identifying `D` and `k`; apply the corresponding convention to the boundary coefficient.

For diffusion with killing, the backward equation is

\[
D\nabla^2p-kp=0.
\]

Equivalently, if `T` is the first escape time of the nonreacting transport process,

\[
p(x)=\mathbb E_x[\exp(-kT)].
\]

This representation explains the required information: escape depends on residence after **birth at x**, not just residence after entry from the feed. For a spatially varying loss field, replacing it by a genuine pointwise upper bound `k_max` is conservative for the same transport process. Replacing a heterogeneous transport process by a fitted scalar `D` needs separate justification; a lower scalar diffusivity inferred from bulk data is not automatically a comparison theorem for arbitrary pore geometry.

An unknown nonnegative source distribution can be handled by `p_min = min_x p(x)`, over every position where the relevant return may originate. No assumption of uniform source strength is then needed.

## 2. Perfectly escaping particle boundary

### Slab

Take a slab `−L ≤ x ≤ L`, escaping through both faces, or equivalently `0 ≤ x ≤ L` with reflection at `x=0`. Thus `L` is the half-thickness, not the full thickness. With `p(±L)=1`, set `α=√(k/D)` and `φ=αL`. Solving the equation gives

\[
p(x)=\frac{\cosh(\alpha x)}{\cosh\phi},\qquad
p_{\min}=p(0)=\operatorname{sech}\phi.
\]

### Sphere

For a sphere of radius `R`, require regularity at `r=0` and `p(R)=1`. With `φ=R√(k/D)`,

\[
p(r)=\frac{R\sinh(\alpha r)}{r\sinh\phi},\qquad
p_{\min}=p(0)=\frac{\phi}{\sinh\phi}.
\]

The center is the minimum in both cases. These are **minimum source-position probabilities**, not volume-averaged probabilities or catalyst effectiveness factors. They approach one as `k→0` and zero as `φ→∞`. The slab and sphere formulas are alternatives justified by geometry, not interchangeable estimates selected for a favorable bound.

If this homogeneous model applies, upper bounds on `k` and `L` or `R`, and a lower bound on `D`, supply a conservative minimum. A macroscopic particle radius alone does not bound residence in narrow, tortuous, or poorly connected pores. Such restrictions must already be represented and bounded by the transport model.

## 3. Finite external transfer

Setting `p=1` at the particle exterior declares arrival there a success. It is optimistic when molecules can linger and re-enter before reaching the specified external gas boundary.

For an idealized, nonreactive external film represented by a transfer coefficient `h>0`, use a radiation boundary leading to an irreversible escape reservoir:

\[
D\,\partial_n p=h(1-p).
\]

This sign uses the outward normal. Define `Bi=hL/D` for the slab and `Bi=hR/D` for the sphere. The minima become

\[
\boxed{p_{\min,\mathrm{slab}}
=\frac{1}{\cosh\phi+(\phi/\mathrm{Bi})\sinh\phi}}
\]

and

\[
\boxed{p_{\min,\mathrm{sphere}}
=\frac{\phi}{\sinh\phi+
(\phi\cosh\phi-\sinh\phi)/\mathrm{Bi}}.}
\]

For example, the spherical surface value is

\[
p(R)=\frac{h}{h+(D/R)(\phi\coth\phi-1)};
\]

multiply this by `φ/sinh φ` to obtain the center value. As `h→∞`, both expressions recover the perfectly escaping boundaries. For `k>0`, they vanish as `h→0`. For finite positive `h`, they approach one as `k→0`.

Even infinitely fast internal diffusion does not remove finite-transfer losses: at fixed `k` and `h`, the slab minimum approaches `h/(h+kL)` and the spherical minimum approaches `h/(h+kR/3)`. These limits also check the geometry factors.

A conservative parameter calculation must include a lower bound on `h`. Minimize over the jointly admissible working-state parameter set; do not treat a best-fit parameter tuple as a guaranteed minimum. A stagnant or reactive exterior requiring resolved transport is not automatically covered by this simple film boundary.

## 4. Particle exit is not detector recovery

An escaped molecule can be captured by another particle, lost farther downstream, or lost in sampling. Let `β_min` bound the conditional probability of reaching analysis with its identity intact **from every possible particle-escape location**. Then

\[
\epsilon_{\min}\ge p_{\min}\,\beta_{\min}.
\]

This product does not require statistical independence; each factor must hold conditionally at the stage where it is used. The second factor must include possible return to the source particle after the first-stage boundary crossing. Alternatively, solve a validated whole-bed transport/loss model directly to the analysis boundary.

An inlet tracer measures recovery averaged over its inlet paths. It does not establish `β_min` for an arbitrary internal source in a bed with bypassing, stagnant regions, or spatially varying sinks. Under an independently established unidirectional homogeneous plug-flow model, an internal source has no more downstream residence than an inlet source; then inlet survival can provide a lower bound for that downstream stage. The plug-flow and homogeneity assumptions do the necessary work. Inlet survival alone does not prove them.

As a general mathematical alternative, a uniform upper bound `τ_max` on mean first escape time, valid for every source position, and a pointwise hazard upper bound give

\[
p(x)\ge\mathbb E_x[e^{-k_{\max}T}]
\ge e^{-k_{\max}\mathbb E_x T}
\ge e^{-k_{\max}\tau_{\max}}.
\]

The middle step is Jensen's inequality. This does not require a finite maximum residence time, which diffusion need not have. But an inlet mean residence time is not the required maximum of source-position means.

## 5. Why integrated inlet uptake does not identify the bound

A small accessible compartment illustrates the problem without choosing numerical values. Let its gas volume be `V`, its exchange conductance with the external gas be `g` in volume/time, and its first-order loss rate be `k`. At external tracer concentration `C`, its stationary concentration and uptake are

\[
c=\frac{gC}{g+kV},\qquad
J=\frac{gC\,kV}{g+kV}\le gC.
\]

For a molecule born inside this well-mixed compartment, competing escape and loss rates give

\[
p_{\mathrm{local}}=\frac{g}{g+kV}.
\]

Small `g` makes the compartment almost invisible to overall inlet consumption, while large `kV/g` makes local escape arbitrarily poor. The productive source can be concentrated in that compartment. Neither low net O2 conversion nor high overall mixed-O2 transmission excludes this case.

In a **known homogeneous** slab or sphere with independently bounded transport, measured uptake can constrain `k` through the model. Fitting that model to integrated uptake does not establish homogeneity or exclude the compartment counterexample. Inverse inference from a missing productive isotope signal is circular if that same inference supplies the capture bound needed to interpret the missing signal.

## 6. What evidence could make the gate measurable?

The following are requirements on the evidence, not a recommended new measurement program.

| Bound or assumption | Evidence that could support it | Evidence that does not suffice alone |
| --- | --- | --- |
| Maximum relevant transport dimension and connectivity | Actual particle/active-layer dimensions; evidence that active source regions communicate with the modeled pore network, including poorly connected regions | Nominal sieve size or maximum straight-line distance to the outside |
| Lower transport coefficient at the working state | Transport characterization in the actual structure and gas state, with uncertainty and a justified treatment of tortuosity, constrictions, pore blockage, and any retention | Gas-phase molecular diffusivity, a room-temperature porosity measurement, or an inert inlet residence-time fit alone |
| Upper signal-loss hazard for every relevant local source environment | Independently constrained capture/exchange kinetics at the working temperature, pressure, coverage, and cofeed state, plus evidence that a faster minority environment is absent or bounded | Net O2 consumption, an average fitted uptake constant, a no-ethylene experiment, or a recombination barrier |
| Boundary and downstream recovery | External-transfer and bed-transport evidence covering all source locations, followed by calibrated line recovery | High integrated inlet-tracer recovery with untested bypass or stagnant regions |
| Entry into the modeled gas population | Evidence or a physical bound for the nascent molecule's launch and early wall encounters, unless the stated mechanism already requires entry into that population | Describing the molecule as desorbed or translationally thermalized |

A fully absorbing pore-wall model could sometimes provide a conservative loss calculation without fitting chemical capture probabilities. It would still require actual pore geometry and an admissible distribution of gas-birth positions and directions. For a source allowed arbitrarily close to an absorbing wall, the minimum survival can be zero. Replacing wall encounters by a finite homogeneous `k` cannot silently remove this boundary issue. An average gas–wall collision frequency is not automatically a pointwise hazard bound for nascent molecules beside a wall.

Particle-size or flow dependence, inert transport checks, and small reacting-state tracer perturbations can test a proposed model where those data already exist. Agreement provides useful checks, but a finite collection of bulk responses does not prove the absence of a small source-associated sink. The uncertainty set must retain any such sink that the evidence cannot exclude.

### Existing Hwang transport check

Hwang's [SI §S2, p. S3](../../literature/papers/hwang2026-supplementary-information-for-mechanism-and/fulltext.md) estimates effective diffusivity from gas kinetic theory and uses measured O2 consumption to assess concentration gradients. This supplies relevant particle and transport context. It does **not** upper-bound the gross loss of an O2 isotope identity: recombination and reconsumption can preserve a small net O2 consumption rate while increasing gross capture. Using `k=rV/C` as the required upper hazard bound would therefore assume away the return/reconsumption pathway being tested. The reported diffusivity estimate is also not, as presented, a validated working-state lower confidence bound.

There is a separate arithmetic discrepancy in the printed table: `rV=1.1×10⁻⁷ mol cm⁻³ s⁻¹`, `R=0.011 cm`, `D=0.12 cm² s⁻¹`, and `C=1.8×10⁻⁵ mol cm⁻³` give `rV R²/(D C)=6.16×10⁻⁶`, whereas the table reports `0.0010`. Both are small. This discrepancy does not itself overturn the qualitative net-rate transport check, and neither value supplies the missing gross-capture bound.

## 7. Keep the chemical boundary and rejection claim intact

For the extended balance with the specified ethane oxygen sink, define the joint lower bound

\[
d_{\mathrm{cross,required,lower}}
=\left[\frac{e-3z-a}{2}\right]_{\mathrm{lower},+}.
\]

Under the isotope-ancestry assumptions in the existing calculation, an equimolar independent-label feed requires mixed-O2 formation of at least half this cross-parent return. If **all of that required return enters the modeled gas population**, a rejection test is

\[
U_{34}<\frac12\epsilon_{\min}
d_{\mathrm{cross,required,lower}},
\]

where `U34` is the upper bound on newly generated mixed O2 surviving to analysis, allowing for consumption of inlet mixed O2. The transport calculation does not establish the isotope-ancestry assumptions or remove that inlet correction.

If only a fraction `f` of chemically required return enters the modeled population, the valid right-hand side is instead multiplied by an independently supported `f_min`. With no positive bound on `f`, a pore-gas transport model cannot exclude the entire return-only mechanism. It only bounds the part that reaches its modeled starting population.

In particular:

- **Thermalized, adequately described pore-gas O2:** the reaction–diffusion bound can apply, even before escape to bulk gas, provided the local-source and transport assumptions are validated.
- **Pre-bulk/geminate recapture after a nascent gas release:** it requires an additional entry/launch bound or a resolved near-surface model. Calling it gas-phase return does not make a continuum escape factor applicable.
- **Surface `O2*` reformation and reuse without gas release:** it lies outside the model. In the existing balance it supplies additional surface oxygen use; excluding gas escape does not distinguish it from other surface salvage routes or identify a Re intermediate.

Thus there is a possible mathematical bridge from pore-gas birth to a measurable isotope bound, but no demonstrated empirical bridge in the reviewed notes. Treat it as a gate that must be passed with independent, relevant bounds. If it remains an unconstrained local-capture model, it supplies no useful rescue of a negative outlet signal.

## Verification and source handling

The slab and sphere differential equations, Robin boundary conditions, and zero-loss limits were checked symbolically. The perfect-transfer and fast-diffusion limits follow directly from the displayed expressions. These are self-contained derivations, not literature-derived numerical estimates. No new literature was needed, and no literature knowledge-base files were edited.
