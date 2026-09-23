# A bounded test of product feedback in the Ag comparison

2026-09-15. Independent methodological follow-up to the [core-design review](../reviews/ag-core-experimental-design.md) and [Ag program](../programs/ag-selective-oxygen-use.md). This is an experimental design, not an observed result or a new feedback mechanism. [Hwang et al., §3.4](https://doi.org/10.1016/j.jcat.2026.117021) already propose that suppressing combustion lowers CO2 inhibition of their promoted channel. Their observed inhibition is strongly chloride-dependent; their proposed Cs/ClO interpretation is not required for this test.

**2026-09-16 baseline update:** [Iyer2021 Section 3.4](../../literature/papers/iyer2021-interdependencies-among-ethylene-oxidation-and/original.pdf) already predicts reactor output and local chlorine coverage by integrating separately assessed kinetics from inlet conditions. [Santos2024 Figures 5–7 and 9](../../literature/papers/santos2024-the-complex-chlorination-effects-on/original.pdf) provide measured elevated-pressure temperature, O2, water and CO2 effects on chloride response. The crossed contrast below remains useful on the actual Ni pair but is neither a new general feedback mechanism nor evidence for a universal sign of product effects.

## Decision and smallest useful experiment

**Use a common-product-state comparison first.** It can determine whether an advantage persists after removing the difference in self-generated product concentrations. A small additional crossed cofeed challenge can measure how that advantage depends on product burden. Neither comparison alone assigns a percentage of an arbitrary finite-bed gain to feedback.

Let A denote Cs/Re–Ag and N denote Ni/Cs/Re–Ag. Measure the net EO and net CO2 rates separately, on the same inventory basis, at sufficiently low contact time that the inlet-to-outlet concentration change does not materially change the inferred rate. Verify that condition through a resolved contact-time bracket; a nominal conversion cutoff is insufficient near a strongly inhibited state.

Use two common inlet product states, L and H, bracketing the modest CO2/water difference relevant to the useful performance comparison. These are measured feed compositions, not labels for presumed surface coverages. Hold ethylene, O2, ethane, EO, total pressure and temperature fixed, replacing inert to introduce products. Include measured water in both states. If only CO2 is changed, call the result CO2 sensitivity at fixed water. If CO2 and water change together, call it their joint product response; separating them requires an additional independent perturbation only if that distinction changes the intervention.

| Measurement | Common product state L | Common product state H |
|---|---:|---:|
| Cs/Re–Ag | r_A(L) | r_A(H) |
| Ni/Cs/Re–Ag | r_N(L) | r_N(H) |

For each material, keep its previously selected chloride setting and reproducible history fixed throughout L → H → L. Confirm the return, and reverse the order only if unresolved history dependence matters. Allow the observed conditioning to settle; an immediate response and a later conditioned response answer different questions. Different selected chloride settings make this a comparison of two catalyst/operating choices. A matched-chloride overlap is needed for a composition-only conditional comparison, and even that does not match surface Cl coverage. Do not optimize chloride again at H and call the resulting difference a product response.

Rates require inlet/outlet molar-flow corrections and inlet CO2 subtraction. Choose the cofeed range and contact time together: reducing conversion can make net CO2 unresolvable against its cofeed. Include calibration covariance, feed drift and reference-return variation. EO cofeed introduces the same subtraction problem for net EO. Neither a negative net difference within uncertainty nor a small apparent selectivity change is informative by itself.

## What the four measurements identify

Define the common-state material contrasts and the environment responses:

\[
\Delta_L=r_N(L)-r_A(L),\quad \Delta_H=r_N(H)-r_A(H),
\]
\[
E_N=r_N(L)-r_N(H),\quad E_A=r_A(L)-r_A(H).
\]

Evaluate these for EO and CO2 separately before constructing selectivity. A reproducible EO advantage at both common states establishes a persistent catalyst/operating effect within that domain. It does not identify a direct Ni–Re interaction: altered primary chemistry, product tolerance and product-induced chloride changes can all contribute. If only the finite-bed advantage is resolved while both differential contrasts are small, feedback becomes a candidate explanation, not a conclusion; reactant depletion, EO loss and bed temperature remain alternatives.

The crossed endpoint contrast has two exact decompositions:

\[
r_N(L)-r_A(H)=\Delta_L+E_A=\Delta_H+E_N.
\]

Their attribution difference is

\[
I=\Delta_L-\Delta_H=E_N-E_A.
\]

Thus the apparent “material contribution” depends on which product environment is held fixed whenever the materials have different product sensitivity. Averaging the two decompositions is a reporting convention, not a uniquely identified causal fraction. Report both contrasts and both responses with uncertainty. This also prevents labeling every material × product interaction as shared-oxygen chemistry.

**The crossed endpoint contrast is not the actual finite-bed performance difference.** Each bed samples a distribution of local compositions. Matching an inlet or outlet composition, or adding the difference between outlet CO2 values to one inlet, does not match those distributions. Product uptake/release and total-flow changes also invalidate an assumed one-to-one relation between outlet CO2 and water.

## Optional quantitative check near the differential limit

Only if deciding whether feedback is the main amplification would change the next experiment, use the existing contact-time data for a local first-order prediction. No complete reactor fit is needed, but the range must remain small and smooth.

Let τ = W/F_in be catalyst mass divided by total inlet molar flow. At a common inlet state, let r_i^0 be a local net rate per catalyst mass, p the vector of local partial pressures, and

\[
s_{i,j}=\left.\frac{d p_j}{d\tau}\right|_0,\qquad
J_{i,j}=\left.\frac{\partial r_i}{\partial p_j}\right|_0.
\]

Obtain s from small-contact-time inlet/outlet differences with total-flow correction. It is not simply pressure times a product rate when the total molar flow changes. For an isothermal bed with a reproducible, differentiable local working state,

\[
\bar r_i(\tau)=r_i^0+\frac{\tau}{2}\sum_j J_{i,j}s_{i,j}+O(\tau^2).
\]

The factor one-half represents the leading linear concentration rise along the bed. The CO2/water contribution to the rate-gap slope is therefore

\[
\beta_{\rm products}=\frac12\sum_{j\in\{CO_2,H_2O\}}
(J_{N,j}s_{N,j}-J_{A,j}s_{A,j}).
\]

Directional CO2/water cofeeds along each material's measured product-rise direction can measure the corresponding dot product without identifying separate partial derivatives. The common L/H challenge supplies this direction only when it actually aligns with those rises; do not assume alignment if water production, consumption or storage differs. A second small perturbation can test local linearity when needed.

Compare this prediction, with propagated uncertainty, against the measured slope of the net rate gap and a held-out small contact time. Bound or measure the remaining terms from changing ethylene, O2, EO, ethane and chloride before assigning a dominant fraction to CO2/water. Small reactant depletion is insufficient by itself when its rate sensitivity is large. Product-induced changes in the stationary chloride state are included in the measured product response, so agreement does not uniquely establish direct adsorption inhibition at Cs domains.

Agreement establishes a local amplification relationship, conditional on the smooth-state assumptions. It does not extrapolate to a high-conversion reactor. Failure falsifies that local explanation only when uncertainty, non-product terms and reference-return drift are smaller than the discrepancy. If the estimate needs a many-parameter working-state model or unresolved small net differences, stop the attribution attempt and retain the common-state product-tolerance result.

## Value and stopping rule

This addition is useful when a gain emerges mainly with increasing conversion and the next design choice depends on whether to change combustion chemistry or product tolerance. Its distinct contribution is a testable local amplification estimate and an explicit boundary on percentage attribution. If the common-state advantage is already decisive and the explanation would not change catalyst or operating choice, the core review's simpler comparison is sufficient. No isotope experiment, broad cofeed matrix or claim of a unique oxygen-transfer route follows from this test.
