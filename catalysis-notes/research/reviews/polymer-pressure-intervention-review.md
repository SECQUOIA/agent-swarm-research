# Review of lowering ethylene partial pressure before Na makeup

2026-09-16. Independent review of [polymer-causal-intervention.md](../working/program-development/polymer-causal-intervention.md) and [polymer-clean-feed.md](../working/program-development/polymer-clean-feed.md). No experiments performed; no proposal, literature package or shared KB edits.

**Retain this as one bounded operating test in an established Na/W campaign. It is not yet a substantial original program.** Lowering ethylene partial pressure can test whether retained inventory has useful capacity under another condition. It cannot, by itself, identify ethylene inhibition, selective initiation loss or a particular W intermediate. The practical contribution would be a reproducible reduction in fresh material demand at matched accepted polymer-carbon output and complete cycle time, followed by a successful prediction under another catalyst history or feed state.

The existing intervention note handles most inference limits well. Four details need to become explicit before execution: establish the reuse benchmark in the reactor mode actually used; assess whether the apparatus can resolve the proposed reversible response; validate polymer-carbon attribution under changed conditions; and separate a three-charge saving from a durable decrease in catalyst demand.

## Source check: what the thesis does and does not support

I read the relevant original-derived Chapter 6 text and checked original PDF p.69 visually. The title page of the original PDF specifies **2023**, despite the current `chen2025` package identifier. The following locators are PDF page numbers, which exceed the printed chapter-page numbers by four.

- Chapter 6 treats Conk's earlier Ir dehydrogenation followed by Pd/Ru isomerizing ethenolysis, with random internal unsaturation and early cleavage into shorter reactive chains. It does not model untreated PE reacting over Na/alumina and W/silica. The predicted rate depends on the reacting-chain distribution, not simply the initial number-average molecular weight. [[chen2025-modeling-cross-scales-in-polymer]] pp.58–63.
- The microkinetic treatment assumes quasi-equilibrated alpha/beta olefins, simplified classes of metathesis rate constants, irreversible propylene-forming steps because product is removed, and spatially uniform dissolved ethylene. Its metathesis equilibrium parameter is estimated for Hoveyda–Grubbs Ru and is explicitly catalyst-dependent. These assumptions do not transfer quantitatively to supported W or a transport-sensitive polymer mixture. [[chen2025-modeling-cross-scales-in-polymer]] pp.64–67.
- Figures 23–24 predict a nonmonotonic ethylene response and chain-end saturation. Accumulation of a nonproductive metallacyclobutane is a **model explanation**, not measured W speciation. In Figure 24a the marked Conk condition is on the rising portion before the maximum: even this modeled example does not say that lowering ethylene from its experimental reference increases rate. The caption reverses the panel descriptions; the plotted axes show panel a varying ethylene and panel b varying olefin concentration. [[chen2025-modeling-cross-scales-in-polymer]] pp.68–69.
- The conclusion calls the model ongoing work and acknowledges an inconsistency between quasi-equilibrated isomerization and the restricted olefin population. This is a limitation of the dissertation treatment; it must not be imputed to the unread final ACS Catalysis article. [[chen2025-modeling-cross-scales-in-polymer]] p.70.

Thus, the thesis supplies a reason to **measure** the pressure response, including its dependence on substrate population. It gives neither a Na/W optimum nor evidence that aging moves Na/W into an ethylene-inhibited regime. Removing active sites without changing the relevant substrate or working state need not change the optimum at all. A pressure-response shift is a separate empirical hypothesis.

## Causal value and the main competing explanations

The manipulable quantity is gas-phase ethylene partial pressure, with dissolved ethylene activity remaining an inferred local quantity. A repeatable change in sustained, attributed product formation establishes an operating effect within the tested history. Returning to the reference condition helps distinguish a reversible operating response from ordinary trajectory changes, provided the response times can be resolved.

Several explanations remain compatible with that result:

| Explanation | What the first pressure test can establish |
|---|---|
| Changed metathesis occupancy or working-state activation | A compatible response, without assigning a metallacycle or proving that the number of active sites is unchanged. A persistent response after restoring pressure may reflect conditioning rather than rapid occupancy. |
| Slower initiation when ethylene supply is reduced | A competing contribution. Ethylene may act as the hydrogen acceptor in transfer dehydrogenation; a benefit downstream can be outweighed by loss of entry into the olefin network. |
| Changed isomerization/metathesis balance or reactive-chain population | A net tandem response. Initial bulk unsaturation and average chain length do not identify the evolving number or accessibility of reactive chains. |
| Changed gas–polymer transfer, swelling, viscosity or catalyst contact | An operational benefit or loss, without proof of intrinsic ethylene kinetics. Fixed total pressure, inlet molar flow and stirring do not hold these quantities fixed. |
| Different propylene or heavier-olefin retention and removal | A change in measured outlet composition that may differ from newly formed product or ultimately accepted output. |

The fresh/aged contrast is useful, but equal elapsed time does not imply equal conversion or reactive-chain distributions. Conversely, matching conversion does not match catalyst history. For the first operating comparison, report these differences rather than claiming exact chemical isolation. A later claim that catalyst aging changes the pressure regime needs measured substrate-state observations and a prediction that survives this distinction. It need not require a complete molecular site assignment.

## Make the first test feasible and interpretable

**Bridge the reactor modes first.** The published three-charge makeup result used sealed batch operation, cooling and dismantling under inert atmosphere. The pressure perturbation assumes gas flow and product removal. These change product activities, residence times and potentially both activation and aging. Reproduce a useful fresh/aged contrast and the direction of Na rescue in the semibatch mode before describing its pressure response as recovery of the published reuse deficit. Preserve the original batch sequence as a literature replication; compare pressure and makeup within one common reactor mode. [[conk2024-polyolefin-waste-to-light-olefins]] Figure 4B–C; [[conk2024-supporting-information-for-polyolefin-waste]] semibatch procedures, PDF pp.16–17.

**Do not assume rapid switching is available.** The original semibatch procedure uses a 300 mL Parr vessel and samples the GC every 12 minutes. For illustration, 0.2–0.3 L of effective gas volume at 20 bar absolute and 593 K contains about 1.8–2.7 standard liters of gas, taking roughly 9–14 minutes to replace once at 0.2 standard L/min under an ideal-gas estimate. Several replacement times, plumbing volumes and dissolution can consume a substantial fraction of the useful reaction window. This is an apparatus estimate, not a measured residence time. The effective volume, actual outlet flow and pressure conventions must be measured. [[conk2024-supporting-information-for-polyolefin-waste]] PDF pp.16–17.

An inert-tracer response bounds gas replacement but does not reproduce propylene sorption or dissolution. A matched blank response should include relevant polymer and solids where possible, while acknowledging that fresh and reacted melts differ. If response, substrate evolution and aging cannot be separated, use independently prepared, time-matched complete-charge experiments. This fallback is a sound first experiment and may be simpler than upgrading the gas analysis to support an ambiguous transient claim.

**Control the gas condition that reaches the reactor.** Compare a reproduced reference with one lower ethylene fraction at fixed total pressure and calibrated total inlet molar flow. Retain an appropriate flow tracer and measure outlet composition and molar flow. Do not equate the cylinder blend with reactor partial pressure during substantial consumption and product evolution. A gas-composition substitution should have matched delivery, purity and switching history; do not let an impurity or valve-change event become the intervention. If flow, temperature or total pressure drifts materially, interpret the experiment as the combined operating change.

The source reports 26.9% propylene yield at ambient pressure and 10 SCCM ethylene versus 84.5% at 20 bar and 200 SCCM. Pressure and flow both changed. It also reports strong transport effects on scale-up. These are direct reasons to avoid assuming that low ethylene improves this platform; they are not an intrinsic reaction order. [[conk2024-polyolefin-waste-to-light-olefins]] Figure 4C and semibatch/scale-up discussion.

## Product attribution is an essential measurement, not a label

The note correctly asks for polymer-derived carbon, but it does not yet specify how that quantity will be established. Propylene contains ethylene-derived carbon even when polymer conversion follows the intended pathway. Gross propylene carbon, polymer mass loss and a closed total-carbon balance therefore do not independently establish polymer carbon in the accepted product.

The original Na/W study used labeled polymer to show that its propylene was not primarily made from ethylene alone under the tested fresh-batch conditions. That result supports the platform but is not a calibration valid for every pressure, aged working state or semibatch residence time. [[conk2024-polyolefin-waste-to-light-olefins]] Figure 4A; [[conk2024-supporting-information-for-polyolefin-waste]] isotopic-labeling procedure and analysis.

Use the preliminary gas response as a screen. Before claiming a useful makeup reduction, validate carbon attribution in the decisive reference and beneficial condition, for example with representative isotopic experiments and product-resolved balances. A polymer-free catalyst blank can bound an ethylene-only pathway, but cannot fully reproduce a polymer-conditioned catalyst or prove that the pathway is absent in its presence. Include condensed heavy products, residue and retained carbon. A pressure-induced outlet spike or earlier escape of incomplete-chain products must not become an apparent recovery of accepted polymer output.

## What would justify expansion

The staged sequence should remain small:

1. Establish the reference reuse response in the common operating mode and compare one lower partial pressure with independent repeats. Use a reversible sequence only if the apparatus resolves it.
2. After a sustained useful response, compare complete charges at the beneficial fixed condition and the reference with no makeup, a smaller Na addition and the published addition schedule. Predetermine accepted output, product specification, complete cycle time and the smallest material saving worth detecting. Compare with the best fixed condition tested.
3. If a three-charge saving is real, extend the best pair of conditions through enough additional feed to test whether the avoided Na addition is merely deferred or paid for by earlier W replacement. Include retained-solids losses, gas handling and any extra downtime. A bounded initial saving is publishable at that scope; it is not a demonstrated durable makeup rate.
4. Expand mechanistic work only if a measured history or feed descriptor predicts a pressure response or makeup requirement under a withheld condition. An optimum-pressure plot or an independent fitted aging parameter for every run does not meet this bar.

A flat or negative pressure response should close the proposed rate-recovery intervention over the tested domain. A lower-pressure condition giving equal output may have a separate gas-handling benefit, but inert dilution at fixed total pressure is not evidence of lower compression cost or lower stoichiometric ethylene use. A useful transport-based response can remain valuable without being renamed molecular inhibition.

The intervention is modest **only when** the pressure reactor, controlled gas mixing, quantitative outlet analysis and polymer characterization already exist. It does not presently justify building a dedicated apparatus. Its experimental simplicity relative to preparing matched unsaturated polymer makes it a reasonable early screen once reuse is reproduced, despite low confidence that the chosen direction will help.

## Prior art and unresolved full text

Wang et al. already discuss excess-ethylene inhibition, continuous feed/product removal, isomerization limitation and catalyst rate–lifetime tradeoffs in tandem PE conversion. Generic inhibition and pressure optimization are not original contributions. [[wang2022-chemical-recycling-of-polyethylene-by]] pp.2–4.

I tried both the [Illinois item 126888](https://www.ideals.illinois.edu/items/126888) and its [advertised PDF](https://www.ideals.illinois.edu/items/126888/bitstreams/414577/data.pdf). Web retrieval and a direct download returned 403. A primary-repository search-index excerpt from Chapter 4 states that reducing ethylene pressure from 60 to 14.7 PSI did not significantly change olefin formation rates, interpreted there as an isomerization-limited cascade, and points to Figures 4.9, 4.10 and C7. Another indexed passage describes the flow reactor. **The full experiment, author/title, pressure convention, controls and figure data remain unverified here.** The indexed passage establishes a directly relevant retrieval lead; it does not supply an audited quantitative comparator for Na/W. This limits any claim that the proposed pressure comparison is experimentally unprecedented.

Sent to the root for the sole literature agent: identify and retrieve item 126888; resolve the Chen 2023 title-page date; retain the requests for the final Chen/Sadow/Peters article (DOI 10.1021/acscatal.4c00465), Guironnet/Peters model (DOI 10.1021/acs.jpca.0c01363), Conk dissertation body and original regeneration evidence. I created no new source packages and make no claims about unread final-paper corrections or inaccessible dissertation results.

**Assessment:** moderate confidence that a bounded test can give useful operational knowledge in an existing platform; low confidence in a makeup saving or an aging-specific inhibition mechanism. Meaningful originality remains conditional on a predictive history–feed–operating-condition relation with a measured cumulative catalyst-use consequence.
