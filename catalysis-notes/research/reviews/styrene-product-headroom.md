# Test net styrene production before elaborate oxygen-fate work

Date: 2026-09-15.

## Decision

**Yes: place a small ethylbenzene/styrene/H2 cofeed experiment before specialist isotope accounting or a large oxygen-product campaign.** It should measure whether zirconia retains useful **net styrene production** in a specified product-containing feed with a favorable reaction driving force. Calibrated moisture control and reproduction of the published dilute-feed behavior remain prerequisites. Native product collection can accompany the gate if the existing train permits it.

The current [oxygen-fate program](../programs/zirconia-styrene-oxygen-fate.md) already recognizes product-rich inhibition as a competing limitation, but places its main investment in oxygen accounting. The [practical selection assessment](../working/practical-selection.md) likewise puts the product-rich test late in its proposed sequence. Reverse-reaction kinetics make the earlier cofeed gate a stronger practical ordering. A failure can remove the application reason for elaborate oxygen attribution without resolving the identity of X. Oxygen provenance can still be scientifically interesting; that is a separate reason to continue it.

This is a **local experimental gate**, not a claim that zirconia is viable or unviable as an industrial catalyst. Existing data do not establish either conclusion in product-rich operation.

## What the focal paper actually measures

The source is Artsiusheuski et al., [main article](https://doi.org/10.1021/acscatal.5c04904) and [supporting information](https://doi.org/10.1021/acscatal.5c04904.s001). The local original PDFs and extracted texts were read; main Figure 1–2 and SI Figure S6 were also inspected visually.

| Observation | Conditions and meaning | Boundary of inference |
|---|---|---|
| Forward ethylbenzene dehydrogenation is first order in ethylbenzene and zero order in H2 | Main p.3–4, eqs.1–3 and Figure 1a: ethylbenzene 1–6 kPa and H2 5–25 kPa at 723 K, as stated in the results text; rates are corrected for approach to equilibrium | Zero H2 order is a property of the **forward rate** in this regime, not independence of net styrene output from H2 |
| Reverse styrene hydrogenation is first order in styrene and H2 | Main p.4, eq.4 and Figure 1b: styrene 1–3 kPa and H2 7–25 kPa at 623 K | The catalyst actively consumes styrene when the composition favors hydrogenation; this does not by itself indicate adsorption inhibition |
| Forward and reverse rate constants agree with the equilibrium relation | Main p.4–5, Figure 2 and eqs.7–9; dehydrogenation and hydrogenation activation energies are 115 ± 11 and −12 ± 3 kJ/mol | Supports a common kinetically relevant transition state on essentially bare pairs in the measured regimes. It does not establish unchanged coverages, rate laws, or working-site populations in a concentrated E/S/H2 mixture |
| Changing residence time has little effect on the asymptotic recovery interpretation | Main p.6–7; SI p.8, Figure S6. The plotted average styrene pressures are approximately 15–50 **Pa**, read from the graph. The text describes 0.5–2% ethylbenzene conversion | This is a small internally generated styrene perturbation, not an independently controlled product-rich cofeed. The main text points to S5 here; the pertinent SI graph is S6 |
| About 70% of the initial DME-activated rate persists with rigorously purified feed | Main p.6–8, Figure 5 and SI p.7, Figure S5: 773 K, dilute ethylbenzene, approximately 12 kPa H2; inferred water about 4 ppm; stable interval exceeds 50 ks | A stable dilute-feed rate over about 14 h is not a high-conversion or product-rich durability demonstration. The approximately 95% value at 1 ppm is a model prediction |
| Zirconia rates compare favorably with published catalysts | Main p.5–6, Figure 4; SI p.9, Table S1 | The zirconia comparison values are extrapolations to other studies' temperatures and ethylbenzene pressures, not matched measurements of sustained net output in those feeds |

Methods give the broader summary range of hydrocarbon pressures 1–5 kPa and H2 5–30 kPa; the more specific Figure 1 ranges above come from the results text. These ranges should not be merged into one experimentally validated mixed-feed domain. In particular, separate hydrogenation measurements at 623 K do not establish the same behavior in styrene-rich dehydrogenation feeds at 773 K or higher.

The SI cleaning model is especially unsuitable as a product-rich reactor prediction without extension and validation. Its p.10–12 equations assume less than 3% ethylbenzene depletion, neglect consumption of ethylbenzene by cleaning, treat X as irrelevant to subsequent transformations, and describe styrene formation with a one-way ethylbenzene term. They model the reported recovery regime; they do not supply a validated net-product balance for feeds approaching equilibrium.

## Reconstruct the rate distinction before interpreting a cofeed

Write E for ethylbenzene, S for styrene, and use dimensionless gas activities `a_i = f_i/p°`. At these dilute gas conditions the fugacity `f_i` can be approximated by partial pressure. For the reaction `E ⇌ S + H2`:

```text
Q = a_S a_H2 / a_E
η = Q/K(T)
A = RT ln[K(T)/Q] = −RT ln η
```

Here `A` is the forward reaction affinity: positive values favor dehydrogenation. The paper writes pressures with a consistent equilibrium-constant convention, for example bar. Using activities makes the standard pressure explicit and avoids mixing a pressure-valued ratio with a dimensionless K.

In the regime described by the paper's eqs.1–4 and 7–9:

```text
r_forward = k_forward a_E
r_reverse = k_reverse a_S a_H2
k_forward/k_reverse = K(T)
r_net = r_forward − r_reverse = r_forward (1 − η)
```

The activity-based rate constants here include the appropriate pressure-unit factors. If the same active-pair fraction multiplies both rates, loss of those pairs reduces both rates while leaving their ratio unchanged. That is a conditional extension of the common-site account, not a measured product-rich site balance.

Three distinct effects must remain separate:

1. **Reverse reaction:** increasing S or H2 increases Q and reduces net styrene output even if forward kinetics and the working surface are unchanged.
2. **Additional reversible inhibition:** S or another component lowers the forward rate at fixed working-site inventory beyond the affinity effect; this requires evidence beyond a net-rate decrease.
3. **Persistent loss of activity:** baseline production does not recover after removing the cofeed. Possible causes include feed contaminants, water exposure, deposits, or a changed catalyst state; the cofeed response alone does not identify which.

There is no defensible adsorption constant or quantitative styrene-blocking penalty to extract from the reported bare-surface power laws. Those observations argue against strong coverage effects in their measured ranges. They do not establish absence of inhibition at all compositions, and they do not support asserting strong styrene adsorption in the proposed feed.

### A conditional numerical consequence that does not extrapolate a rate law

The table evaluates the paper's `r_net/r_forward = 1 − η` relationship at specified approaches to equilibrium. The affinities use 773 K and `RT = 6.427 kJ/mol`. These are algebraic scenarios, **not measured compositions or productivities**; no high-pressure rate extrapolation is involved.

| η = Q/K | Net/forward rate under the stated relation | Forward affinity at 773 K, kJ/mol |
|---|---:|---:|
| 0.10 | 0.90 | 14.80 |
| 0.50 | 0.50 | 4.45 |
| 0.90 | 0.10 | 0.677 |
| 0.99 | 0.01 | 0.0646 |

At η = 1, the E/S/H2 interconversion has zero net rate; at η > 1 it favors styrene hydrogenation. These equilibrium statements do not depend on zirconia's activity. Additional coupled chemistry must be included in the material balance if it is significant.

A large forward rate can therefore coexist with small net production. Near equilibrium, dividing a small measured rate by `1 − η` also amplifies composition and equilibrium-constant uncertainty. Use the correction as a diagnostic away from equilibrium, and retain direct net output as the practical endpoint. This review does not assign an absolute equilibrium styrene pressure from the article's rounded reaction enthalpy/entropy or digitize Figure 2 into a precise K table. Select actual cofeed pressures using a checked K(T) and its uncertainty at the chosen temperature.

Likewise, high dilute-feed selectivity need not remain high for **incremental net styrene production** if cleavage continues while reverse hydrogenation cancels much of the styrene formation. Quantifying that penalty requires measuring cleavage and net styrene under the same cofeed; the existing selectivity figures cannot supply it by themselves.

## Strongest missing measurement

**Direct, sustained `F_S,out − F_S,in` per initial catalyst mass, under an independently specified E/S/H2 cofeed with measured water, accompanied by a return-to-baseline test.** A small differential reactor can measure this local behavior without first creating a high-conversion bed and its temperature/composition gradients.

Measuring a large outlet styrene concentration is insufficient when styrene is fed. The incremental difference must exceed the propagated inlet/outlet measurement uncertainty and line holdup. Use a calibrated flow tracer, an inert-train cofeed blank, and steady collection windows. Report mass-normalized net styrene, side products, and carbon closure. Report packed catalyst volume when available, but do not infer a volumetric advantage from surface area or surviving-site-normalized rates.

This measurement addresses a different uncertainty from the identity of cleaning product X: does the catalyst make useful net styrene while exposed to its own products? It is the more direct first test of the proposed application.

## Minimal practical gate

Use the existing parent zirconia preparation and its published activation protocol. Begin at a reproduced 773 K reference condition, approximately 1.2 kPa E and 12 kPa H2, or document any necessary departure. Independently measure moisture and characterize styrene feed impurities, including any carried-through stabilizer. The published styrene reagent contains 4-tert-butylcatechol; attributing a cofeed-induced rate loss to styrene requires excluding an accompanying impurity or moisture change.

1. **Establish a stable reference.** Reproduce the dilute-feed rate under independently measured low moisture, with inlet and outlet composition, adequate net-production precision, and verified absence of material transport or temperature artifacts. Preserve the actual reference history and initial catalyst-mass denominator. Reproduction of the two pretreatment histories remains necessary before claiming their published convergence mechanism.
2. **Run a small cofeed matrix.** Hold E pressure, temperature, total flow and measured moisture fixed by replacing inert gas. Use two styrene levels, including the low-product reference, and two H2 levels. Choose at least one product-containing point with appreciable forward driving force, for example η no greater than about 0.5 with its uncertainty, so a weak signal cannot be dismissed as an intentional near-equilibrium test. Select the S/E ratio from an explicit prospective operating composition; merely repeating the 15–50 Pa SI perturbation would not close the gap. If that S/E ratio requires lower H2 to remain on the dehydrogenation side, state and test that requirement. Do not silently infer a separation solution from it.
3. **Separate prompt response from exposure effects.** Interleave return-to-reference measurements and follow the product-containing state long enough to resolve drift on the observed recovery/deactivation timescale. Repeat the decisive contrast on a matched specimen or with a reversed sequence. Initially dry cofeeds isolate product effects; a matched measured-water challenge is the next small extension if loss of cleaning function becomes the consequential hypothesis.
4. **Evaluate direct output first.** Calculate `r_net = (F_S,out − F_S,in)/m_initial`, product losses and integrated net production during the exposure. Evaluate `r_net/[a_E(1 − η)]` only away from equilibrium as a diagnostic for departures from the focal relation; do not use it as the production endpoint or as proof of an unchanged surface.

Two H2 levels help distinguish the predictable Q dependence from an unexplained product response. They are not by themselves a complete mechanistic separation: changing H2 can change surface chemistry. The matched reference states and recovery sequence are therefore part of the minimal gate.

### What the gate can falsify

| Result | Supported decision | Claim not supported |
|---|---|---|
| At a verified favorable η, net output is small relative to the predeclared practical requirement, or selectivity/drift is unacceptable | Reject the selected operating window and its presumed output advantage; pause application-driven oxygen-fate expansion unless a bounded remedy is independently justified | All zirconia feeds, temperatures, or catalysts are unviable |
| Rate falls by approximately the affinity factor and recovers on returning to reference | The apparent loss needs no additional inhibition mechanism at those conditions | Styrene never adsorbs, X is harmless, or the catalyst has an industrial advantage |
| A reproducible additional loss appears promptly and reverses on return | Reject transfer of the simple forward-rate relation to that cofeed; investigate product inhibition or another reversible surface change | Persistent coking or harmful oxygen export has been identified |
| Baseline fails to recover after cofeed, with contaminants and apparatus effects controlled | Reject unchanged durable function over that exposure; measure the cause before investing in oxygen-specific attribution | The missing oxygen product necessarily caused the damage |
| Sustained net production and selectivity meet the local requirement | Product exposure has passed a necessary gate; proceed to the smallest oxygen-fate experiment that answers a remaining consequential question | Process viability, long lifetime, or savings from steam removal are established |

Predeclare the practical net-rate/selectivity requirement and detectable change from the proposed operating window and catalyst-inventory constraint; the paper provides no universal success percentage. In the absence of such a requirement, the experiment can pass a **chemical continuation gate**—resolvable sustained net production without a consequential new loss—but cannot pass an economic viability gate. An η ≥ 1 challenge can verify reverse behavior, but failure to produce net styrene there does not falsify catalyst usefulness.

## Recommended revision to the program order

Use **measured-moisture reference → matched product-cofeed/net-output gate → native oxygen-product pilot → targeted isotope attribution**, with product collection alongside the gate where convenient. Keep the program's existing isotope exchange, water-regeneration, and retained-inventory controls for the stronger claims they protect. The earlier gate simplifies the investment decision; it does not relax the evidence required to assign oxygen provenance or count oxygen removed per recovered pair.

No literature-package changes or new source retrieval were needed for this review. The missing item is primarily an experiment, not another unvalidated extrapolation of the published kinetics.
