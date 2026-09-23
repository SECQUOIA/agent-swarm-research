# Independent review: impurity budgets in Na/alumina–WOx/silica ethenolysis

Date: 2026-09-15. Reviewed: `research/working/alternative-screen.md`, with comparison to the zeolite and oxide screens. This is a critical proposal assessment, not experimental evidence.

**2026-09-16 correction after upload:** the [post-upload audit](post-upload-polymer-audit.md) visually checked Science Figure 4B and SI S20. The published reference uses **three total 1 g PE charges, with 400 mg fresh Na/alumina added before charge 2 only**; charge 3 receives only PE. The nominal fresh-solid total is 1.2 g and the conditional three-charge material-productivity ratio is `B = 2f`, not the separate every-later-charge illustration `B = 1.5f`. The Science SI reports **19.9658 g warm oil, 29.9717 g remaining solid and 80.1% apparent conversion** for its scale-up; the patent record below contains different numbers and remains a distinct source. Neither residue subtraction nor the condensate volume/density estimate closes a polymer-specific carbon balance. These corrections supersede the old missing-dose/Science-access limits; patent regeneration figures and the dissertation body remain unresolved.

**Later source update:** the [recovered patent benchmark](polymer-patent-benchmark-accounting.md) and [independent protocol review](polymer-patent-protocol-review.md) now establish key batch inventories, contaminant challenges, fresh-Na replacement and solvent preparation. Full cycle inventories and DME composition/efficacy remain unresolved because figures are missing. Science main/SI are now locally available and checked by the 2026-09-16 audit; the historical table below records this reviewer's earlier reading. The dissertation body and patent regeneration figures remain unavailable.

## Decision

**Recommend a bounded pilot, conditional on a protocol and assay audit. Do not promote this to a full program yet.** The strongest possible contribution is a measured contaminant budget that predicts component failure and a useful intervention at realistic cumulative feed throughput. “A catalyst partner protects metathesis,” “oxygenates poison tungsten,” and “add an adsorbent” are insufficient novelty claims.

The screen already recognizes most obvious limitations. Its remaining weakness is that the proposed component-recombination experiments are more diagnostic of *where function was lost* than of *why the mixture was protected*. The claim of a moving bottleneck requires time-resolved functional measurements; a decline in propylene yield alone cannot establish it. The practical case also needs a capacity calculation before an extensive protection campaign.

## Prior art: scope of the original 2026-09-15 review

| Source and access in this review | Consequence for the proposal |
|---|---|
| Conk et al., [Science 2024, 10.1126/science.adq7316](https://doi.org/10.1126/science.adq7316). Author publication record and public abstract verified; publisher access failed. Original methods/SI not independently read. | The Na/alumina–W/silica platform and high-yield polyolefin conversion are established. This review cannot supply verified catalyst/feed inventories or baseline contaminant tolerances. Those are launch requirements. |
| Conk, [2025 dissertation abstract](https://escholarship.org/uc/item/7v07b7c8), searchable public abstract; body embargoed until September 30, 2027. | Reuse losses, impurity sensitivity, transfer-dehydrogenation initiation, modified catalysts, and DME regeneration are already disclosed. The detailed scope of unpublished/embargoed experiments remains a material novelty uncertainty. |
| Kim et al., [Applied Catalysis B 2022, 10.1016/j.apcatb.2022.121873](https://doi.org/10.1016/j.apcatb.2022.121873), publisher abstract, introduction, and conclusion excerpts read; full methods not read. | 4A protection of WOx/silica against oxygenates generated during activation is direct prior art. The distinction between activation poisoning and destruction of operating sites matters; a protection benefit need not indicate improved steady operation. |
| Wang et al., [JACS 2022, 10.1021/jacs.2c07781](https://doi.org/10.1021/jacs.2c07781); [ChemRxiv manuscript](https://chemrxiv.org/engage/api-gateway/chemrxiv/assets/orp/resource/item/6331eff7fee74e83a04b709d/original/chemical-recycling-of-polyethylene-by-tandem-catalytic-conversion-to-propylene.pdf), PDF pp.1–5 read. | Beyond initiation and product removal, this source already reports a stability tradeoff from adding a second catalyst. On PDF p.5, catalyst 2 lowers the initial propylene rate from 1.40 to 0.85 mmol/h while extending the reported deactivation time from 5 to 15 h. These concern a different catalyst system; they nevertheless rule out broad novelty for cross-component durability effects. |

Wang's manuscript also directly establishes isotope-based carbon-source allocation (PDF p.4) and shows that an added catalyst can change rate and lifetime in opposite directions. Its preliminary environmental assessment identifies ethylene production as the largest contributor under its assumptions (PDF p.5). None of these observations proves or disproves Na-mediated oxygenate interception; they strengthen the case for evaluating lifetime productivity and ethylene use together.

The local Quesada–Iglesia artifact was read at pp.18–27. It supports the screen's caution: productive-site titration requires reaction-specific coverage corrections and subtraction of support-bound propylene. In that Mo system, the authors check restoration of the original reaction rate after titration. This does not validate a W site assay at polymer-processing conditions. The artifact carries an explicit preprint notice. [[quesada2026-alkene-metathesis-on-dispersed-moox]] p.18-27

**Novelty judgment:** plausible for the narrow quantitative prediction, unestablished for the mechanistic interpretation, weak for the proposed materials intervention. The inaccessible dissertation is an uncertainty to resolve through available papers/SI or author-provided material, not evidence that the work has already been done.

## Main scientific challenges

### 1. Component recombination does not establish cross-protection

Exposed-Na/fresh-W versus fresh-Na/exposed-W identifies operationally damaged components only if exposure and handling are comparable. It does not show that Na reduced the poison dose reaching W in an operating mixture. Independently exposing each component also omits the mixture's evolving substrate and byproduct concentrations.

Fresh Na can improve output by supplying initiation/isomerization activity, capturing residual poison carried into the recombination test, changing the W activation environment, or changing polymer–solid contact. Fresh W can similarly provide new activity and additional adsorption inventory. An asymmetrical rescue is therefore not a unique mechanistic signature. A failed rescue does not prove irreversible destruction: residual poison can immediately damage the replacement.

**Required correction:** call this a *component-function matrix*. Reserve “protection” for experiments that independently show reduced harmful exposure at W and preserved W function. Quantify the poison remaining in liquid/polymer, transferred with each solid, transformed into other species, and released during the subsequent assay. Use paired aliquots for chemical inventory, immediate function, and controlled recovery rather than measuring all three sequentially on one specimen.

Two comparisons answer different questions and should both appear:

- At equal external contaminant input, does adding Na alter W survival? This establishes a system-level benefit.
- At equal measured contaminant history reaching W, does the survival difference persist? Disappearance of the difference supports interception; persistence suggests an additional activation or chemical interaction effect.

Separate compartments or sequential exposures can help with volatile poisons, but are mechanistic models. They do not reproduce polymer-bound oxygenates in a stirred melt. Removal of one powder from an intimate mixture is not a credible initial rescue experiment.

### 2. “Function” is not synonymous with one catalyst component

Run the same molecular substrates over each component, both bare supports, and the mixture before assigning initiation to Na, isomerization to Na, and metathesis to W. Small-molecule assays are operational readouts; a retained small-alkene rate does not establish access to a polymer chain. Conversely, lower assay activity after cooling may reflect altered adsorption or activation rather than the working-state loss.

An internal-alkene/ethylene W assay can generate or restore metathesis sites during measurement. Standardize activation, record the initial transient and later plateau separately, and include an interrupted clean control. Do not allow a long “conditioning” period to erase the phenomenon being tested. A fresh catalyst exposed before activation and an already operating catalyst exposed to the same impurity represent different causal experiments.

For initiation, residual PE unsaturation may be sufficient for substantial deconstruction despite being difficult to detect. Specify unsaturation detection limits and chain-number normalization. Ethane may have sources other than the test alkane, while alkene products can disappear rapidly by subsequent chemistry. An initiation bypass should match polymer molecular weight, branching, viscosity, and preparation residues sufficiently to avoid attributing easier transport to restored chemistry. It still requires isomerization.

### 3. A sharp threshold is not evidence of sacrificial protection

Tandem throughput can resemble `min(initiation supply, isomerization capacity, metathesis capacity)`. Smooth, independent declines can therefore produce a sharp change in total yield when the limiting function changes. Induction, polymer depletion, and a finite batch observation window create further apparent thresholds.

Measure function trajectories and contaminant inventories over time. Fit independent damage plus measured transport before introducing a protective capacity. Require a withheld contaminant waveform or Na:W ratio to be predicted without adjusting each component's parameters. A single total-dose curve cannot separate capture capacity, poison delivery, activation lag, and intrinsic damage susceptibility.

### 4. The ketone/4A comparison needs its own chemical audit

2-Hexanone is a reasonable analytical probe, but its disappearance could reflect adsorption, catalytic transformation, evaporation, or retention in sampling lines. Transformation may create a different poison, including water. Measure products and water, not just inlet-minus-outlet ketone.

Do not assume that 4A has a useful working capacity for this ketone at 320 °C from its established protection against other in-situ oxygenates. Measure capacity and breakthrough with the actual molecule, temperature, ethylene, and hydrocarbon matrix first. External adsorption, access to micropores, competitive occupancy, and transformation can all matter. A negative 4A result would reject this adsorbent/probe pairing, not the general possibility of sacrificial protection.

## Practical significance and dose realism

No “realistic ppm” value can be assigned from the present source record. First measure a specified feed before and after the proposed cleanup: water, extractable oxygenates, polymer-bound oxygen, relevant additives, and lot variation. Total elemental oxygen alone cannot distinguish a benign filler from a readily delivered poison. A volatile ketone spike should be labeled a controlled stress test until its exposure is connected to these measurements.

Report catalyst masses separately, catalyst/feed ratio, catalyst metal loading, accessible function where validated, and cumulative kilograms of polymer processed per kilogram of each solid. Repeat additions to a retained catalyst inventory are more revealing than repeatedly using fresh catalyst. If a high catalyst dose merely buffers one small polymer charge, apparent feed tolerance may be stoichiometric reagent use.

For one impurity, let `c` be mmol impurity per kg feed and `q` the measured working uptake in mmol per g adsorbent. Even perfect capture requires:

`adsorbent demand >= c/q g per kg feed`.

**Illustrative arithmetic, not reported capacities or waste compositions:** for a 100 g/mol impurity, 100 ppm by mass is 1 mmol/kg feed. At `q = 1 mmol/g`, it requires at least 1 g adsorbent/kg feed. At 1 wt%, the lower bound is 100 g/kg; at `q = 0.1 mmol/g`, that becomes 1 kg/kg. Incomplete bed utilization and other adsorbates increase demand. If regeneration works, replace fresh demand with measured makeup plus regeneration energy, purge use, contaminants discharged, and loss of capacity across cycles.

Make this estimate before optimizing new catalyst formulations. Separate catalytic tolerance, reversible inhibition, regenerable capture, and sacrificial capture in the conclusions. Protection can be useful without being intrinsic tolerance, but its material cost must be charged to the process.

The proposed polymer-carbon metric is sound, but report cumulative throughput per reactor volume and full cycle time alongside it. A cheap adsorbent can increase solids handling and displace catalytic volume even when mass-normalized results look favorable. Compare against drying/washing only for contaminants those operations actually remove. DME regeneration is a disclosed baseline whose protocol and effectiveness still need verification.

A relevant external process benchmark is [Closed-loop recycling of polyethylene to ethylene and propylene via a kinetic decoupling–recoupling strategy, 10.1038/s44286-025-00290-y](https://doi.org/10.1038/s44286-025-00290-y). Publisher-indexed text reports waste containing oxygenated additives, cycling, and an 8 h continuous experiment. Its different chemistry and large reported solids inventories preclude direct superiority claims, but comparison should extend beyond fresh-batch yield. This source was sent to the parent for the single literature agent; its full methodological claims remain unaudited here.

## Smallest decisive pilot

1. **Protocol gate:** obtain Na/W synthesis, activation, catalyst/feed masses, product-carbon definitions, and reuse/impurity protocols from the original work/SI. Reproduce one clean PE time course and establish gas/melt transport sensitivity. Do not launch a broad impurity matrix first.
2. **Assay gate:** validate component-specific operational functions with cross-component and support controls, including whether the assay restores activity. Measure uptake/transformation of the chosen impurity under reaction conditions. If these measurements cannot resolve a damaged function, narrow the claim to empirical lifetime rather than rescue mechanism.
3. **Causal gate:** compare sham exposure and a small bracket of damaging doses on operating W alone, Na alone, and the mixture. Use the function matrix plus measured poison histories. Include one Na inventory perturbation and one constant-total-dose experiment delivered at a different rate. Change pulse rate only with the residence/transport controls needed to interpret it.
4. **Capacity gate:** compare extra Na against one independently validated adsorbent and inert dilution at fixed catalyst inventory, with both a controlled comparison and explicit accounting of the extra solids. Demonstrate continued polymer-carbon productivity through repeated contaminated feed charges; measure capacity exhaustion or bound it quantitatively.
5. **Transfer gate:** only after a signal, test one characterized oxidized PE or selected postconsumer feed against cleanup and regeneration. This is where practical relevance becomes established; the ketone result alone cannot do so.

Advance only if a simple component/exposure model predicts a held-out condition and the intervention yields a meaningful lifecycle benefit after solids and regeneration costs. Reject the cross-protection hypothesis if independent damage explains the data, while retaining a useful validated feed specification. Stop materials development if capture demand or cleanup severity removes the practical benefit. Do not require absolute W site counts to reach this decision.

## Relative merit

On the current evidence, I would rank **zeolite recovery first for a mechanistic pilot**, with this polymer pilot and the oxide-carbon-fate pilot both conditional alternatives. The zeolite screen has a better defined exposure intervention and stronger locally read kinetic foundation. Its recovery assay can itself heal sites, so it retains a serious but explicit identification problem.

The oxide screen has a more direct literature foundation for the proposed cross-component interaction and a clear carbon-fate question. Its main liability is detecting and manipulating a very small native inhibitor flux at conditions where a useful support advantage persists. The polymer screen has more direct waste-feed relevance, but weaker accessible evidence for the exact mechanism, incomplete benchmark methods, and a larger gap between tractable molecular poisoning and realistic polymer contamination.

This is a judgment about readiness and expected information from the first experiment, not an established ranking of eventual industrial value. Access to complete Na/W protocols plus a convincing dose/function pilot could change it. Present evidence supports a narrow decision experiment, not rejection of the field and not commitment to a flagship program.

## Record of limits at the original 2026-09-15 review

Read the KB README, relevant local Quesada primary-text sections, all three working screens, the public prior-art material identified above, and the linked Wang manuscript. No literature packages or generated KB files were changed; no maintenance was run. New-source metadata was handed to the parent. At the original review, Science 2024 methods/SI, Kim 2022 full methods, and the embargoed dissertation were unresolved; this paragraph preserves that historical reading scope, not current availability; no catalyst dose, adsorption capacity, or exact novelty conclusion was inferred from missing material.
