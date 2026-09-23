# Water storage, transport, and the size of a source-generated gradient

2026-09-16. Analytical checks for the [physical-water-management candidate](../working/program-development/physical-water-management.md). These are illustrative calculations, not fitted catalyst properties or simulated experiments. [Executable calculation](water_transport_limits.py) and [output](water_transport_limits_output.json).

## The same washout can imply different stationary exposures

For a single linear compartment with reversible storage B, conductance G, positive source q and boundary concentration c_b,

\[
B\dot c=q-G(c-c_b),\quad \tau=B/G,\quad c_{ss}-c_b=q/G.
\]

With a unit source turned on from c=c_b=0, the integrated concentration in the unit interval is

\[
\int_0^1c(t)dt=\frac{q}{G}\left[1-\tau(1-e^{-1/\tau})\right].
\]

The dimensionless illustration gives:

| Case | B | G | Washout time | Stationary excess | Concentration integrated during first unit of ingress |
|---|---:|---:|---:|---:|---:|
| Reference | 1 | 1 | 1 | 1 | 0.368 |
| Lower storage | 0.5 | 1 | 0.5 | 1 | 0.568 |
| Greater conductance | 1 | 2 | 0.5 | 0.5 | 0.284 |

Both modified cases have the same faster normalized washout. They predict different stationary concentrations and opposite changes in early ingress exposure relative to the reference. Concentration integral is not a validated cobalt-damage law. Nonlinear damage, recovery and coupled chemistry can change the functional consequence. These identities are standard mass balances, not a claimed new theoretical discovery.

## A conditional check on the magnitude of gas-referenced pore gradients

For a spherical particle with uniform water generation q_v, constant effective diffusivity D, and fixed surface concentration c_b,

\[
c(r)-c_b=\frac{q_v(R^2-r^2)}{6D},\qquad
\Delta c_{centre}=\frac{q_vR^2}{6D}.
\]

The derivative is zero at the centre, the surface equals c_b, and integrating outward flux gives the full volumetric source. This is a passive, stationary, single-phase model without adsorption-mediated surface flux, internal sinks, changing catalyst state, or wax-phase partitioning.

**Reported source-scale inputs:** Fang et al. 2026 ([main source](https://doi.org/10.1038/s41467-026-76571-8)) report 2400 mL gas per g catalyst per hour, inlet CO fraction 0.32, about 44.1% conversion and 220 °C. Approximating one mole water per mole converted CO gives about 3.85–4.20 micromol water per g catalyst per second. This is a hydrocarbon-dominated source estimate, not a direct measured water rate. The range uses gas molar volumes at 0 and 25 °C because the precise volumetric reference was not established in this reading.

**Analyst assumptions:** approximate 40–60 mesh granules by spherical radii 125–212.5 micrometres; examine pellet densities 0.5–1.5 g/cm3 and boundary water partial pressures 1–4 bar. Density here means catalyst mass per granule-envelope volume, not bed bulk density or skeletal density. The source is a bed-average estimate, not a bound on the rate in an inlet particle; the chosen water backgrounds also exclude dry inlet regions. These are sensitivity choices, not measured source properties or confidence intervals. Use D = 2.2×10^-7 m2/s solely as a counterfactual numerical scenario. Although that number appears in the source's pore-network model, it originates in earlier molecular self-diffusion simulations. It is **not established as the gas-concentration-referenced effective D in the equation above**.

Under those assumptions, centre-to-surface water-pressure excess is approximately **93–883 Pa (0.00093–0.00883 bar)**. Relative to the chosen 1–4 bar water background it is less than 1%. This calculation therefore does not support assuming a large local drying effect from that particular constant-D gas model. It also does not show that the real particles have such small gradients: the concentration basis, liquid phases, tortuosity and relevant transport resistance are unmeasured.

The D required for a specified fractional centre excess f is

\[
D_f=\frac{q_vR^2RT}{6 f p_b}.
\]

The executable output records D_f for f=0.1 for every chosen radius, density, gas-volume convention and boundary pressure, giving approximately 5.1×10^-10 to 1.9×10^-8 m2/s. This inverse calculation is the more useful planning result: it states which independently measured, correctly referenced transport coefficients would permit a chosen gradient. Ten percent is an illustrative diagnostic magnitude, not the minimum exposure change required to affect cobalt stability. An independently measured sharp damage boundary could make a smaller change consequential.

## Consequence for the first experiment

Measure the relevant transport resistance and the sensitivity of reaction/damage to water before treating a faster purge as evidence of enough stationary drying to explain stabilization. A long normalized tail can arise from stored or chemically generated water even when mobile-phase gradients are small. Conversely, a wax-filled or interfacial path can have a much larger resistance than a gas-pore model suggests.

If the promoter changes only an external series resistance, the maximum removable local excess is the source times that resistance. It cannot eliminate an unchanged internal resistance. The proposed experiment must therefore identify where resistance and water inventory reside, and whether the operative quantity is a stationary exposure or a damaging history.

Checks performed: the script verifies square-radius and inverse-diffusivity scaling and the distinct ingress predictions at equal normalized washout time. An [independent review](../reviews/ft-hydrophobic-transport-review.md) verified the equations, units and output and required the concentration-basis, density and axial-position qualifications above. No parameter has been fitted to published curves. This remains a conditional scale illustration, not evidence of the actual catalyst's water gradient.

The newly supplied [Barrer and Fender 1961 original](../../literature/papers/barrer1961-the-diffusion-and-sorption-of/fulltext.md), p. 1 and its diffusion analysis, distinguishes water-sorption diffusion from isotope self-diffusion in zeolites. The [IUPAC report](../../literature/papers/karger2024-diffusion-in-nanoporous-materials-with/fulltext.md), pp. 5–12, formalizes the self/transport distinction, thermodynamic factor and concentration basis. These sources support the coefficient caution above; their zeolite coefficients are not substituted into the Co/SiO2–PDVB calculation. No numerical output changes follow from the uploaded literature.
