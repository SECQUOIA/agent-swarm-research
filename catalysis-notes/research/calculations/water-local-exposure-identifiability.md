# Why two water-tracing inputs need not identify local exposure

2026-09-16. Analyst derivation for the [water measurement pilot](../working/program-development/water-measurement-feasibility.md). This is a conditional counterexample, not a proposed description of Co/SiO2–PDVB, an experimental result, or a new general theorem. The algebra and its interpretation were independently checked in the [measurement review](../reviews/water-measurement-feasibility-review.md).

**Even complete inlet-water and reaction-source tracer responses can agree while the water concentration at a producing site differs.** Such measurements are useful, but claiming local exposure requires identifying which measured inventory belongs to the source-containing region. Measuring a second outlet transient does not guarantee that identification.

## A minimal counterexample

Consider two internally mixed water pools, each exchanging with a common well-mixed gas. Use a local linear concentration coordinate on a common gas-referenced basis:

\[
B_i\dot c_i=G_i(c_g-c_i)+q_i,\qquad G_i=\lambda B_i,\quad i=1,2.
\]

Here capacity B has units m³, concentration c has units mol/m³, conductance G has units m³/s, and production q has units mol/s. Both pools have the same positive relaxation rate λ, but may have different capacities. The gas balance is

\[
V\dot c_g=F(c_{in}-c_g)+\sum_iG_i(c_i-c_g),
\]

with gas holdup V and actual volumetric flow F on that concentration basis. The measured outlet is c_g. Define total capacity B_T = B_1 + B_2, total retained inventory W = B_1 c_1 + B_2 c_2 and total source q_T = q_1 + q_2. Summing gives

\[
\dot W=\lambda(B_Tc_g-W)+q_T,
\]

\[
V\dot c_g=F(c_{in}-c_g)+\lambda(W-B_Tc_g).
\]

These two observable equations contain B_T and λ, but not the division of capacity or production between the pools. For identical initial aggregate inventories and the same inlet/source histories, any positive capacity split gives exactly the same outlet trajectory and total inventory. This remains true at any tested flow in this model, provided its other coefficients remain unchanged.

At steady state, however,

\[
c_i-c_g=\frac{q_i}{\lambda B_i},\qquad
c_g-c_{in}=\frac{q_T}{F}.
\]

Suppose all production occurs in pool 1. Changing its capacity from B_T/4 to 3B_T/4, holding B_T, λ and q_T fixed, decreases its concentration excess by a factor of three while preserving every outlet response above. Choose a small enough source that both alternatives remain within the stated linear range; no vanishing capacity or infinite concentration is required. The total excess retained inventory is q_T/λ in both cases.

The same summation applies separately to an ideal conserved water isotope. Therefore an inlet-water-label perturbation and an independently specified reaction-water-label perturbation can both be indistinguishable between these alternatives. This result assumes negligible isotope effects, accounted exchange chemistry and identical aggregate initial label inventories. In actual CO oxygen-label experiments, chemical oxygen pools and the time of water formation add further unknowns unless independently constrained.

## Scope and experimental consequence

The example establishes a failure of guaranteed identification. It does **not** establish that local exposure is always unknowable. Distinct resolved exchange rates, spatial measurements, a selective reporter of the producing region, or a known local rate law can add information absent here. In particular, an independently calibrated water-dependent production law would couple q_i to c_i and could break the counterexample. Its calibration would have to remain valid when PDVB changes the working catalyst, H2/CO transport and retained liquid.

The useful decision is to choose the added constraint from the prediction that matters:

- To predict total water release into downstream equipment, the aggregate inventory/response model can be sufficient within its validated state and operating range.
- To predict a cobalt-site damage threshold or substitute smaller granules for PDVB, total inventory and exchange need an additional constraint linking them to the source-containing region and its transport path.
- To predict useful catalyst recovery after a pulse, measure and predict the recovered catalytic function directly. A matched outlet water trace alone cannot establish that the local damage exposure was matched.

Before adding isotope equipment, test whether the planned second input would discriminate the plausible models. Oxygen labeling is established FT methodology, not a novel intervention in itself. The now-audited [den Breejen JACS 2009 original](../../literature/papers/breejen2009-on-the-origin-of-the/fulltext.md), pp. 2–3 and 5, uses C16O/C18O switches on Co/CNF at 210 °C, 1.85 bar and H2/CO = 10. Its water transient contains O and OH intermediates as well as adsorbed H2O; the authors warn that readsorption can inflate the inferred residence time and coverage. The [2010 thesis](../../literature/papers/breejen2010-cobalt-particle-size-effects-in/fulltext.md), Chapter 2, PDF pp. 23–29, repeats these details. This original-derived evidence strengthens the chemical-pool and apparatus cautions. It does not identify source-site water exposure or supply a transport coefficient for wax-bearing Co/SiO2–PDVB.

This constraint narrows the mechanistic promise of the pilot. It still permits a useful operating-response result, provided an independently predicted change in recovered function or useful output is demonstrated. Failure to identify local exposure is a measurement limitation; it is not evidence that PDVB fails to protect cobalt or that water transport is irrelevant.
