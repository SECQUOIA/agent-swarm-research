# Independent review: wet methane oxidation after NO removal

Reviewed 2026-09-15; revised 2026-09-16 after uploads and the application-boundary review. No experiments performed. Review of the [proposed finite study](../working/wet-methane-value-screen.md), with independent inspection of the original Ryu2024 main Figure 6, SI Figure 28 and Tables 6–7, Figure 6 source-data workbook, selected public reviewer responses, and Mortensen2025 main Figure 2 and methods.

## Decision

**Retain a finite compatibility study, conditional on a suitable wet-gas reactor and reproducible catalyst. It is not yet a substantial original research program and does not currently outrank the Ag retention or polymer exposure studies.** Retain it as a lower-priority diagnostic, conditional on modest reproduction effort. Its immediate value is testing whether a published material advantage survives removal of a cofeed known to affect conventional methane-oxidation catalysts. A consequential real low-NO sulfur-containing application remains unestablished; methane abatement importance alone does not raise this study’s priority.

The important uncertainty is **whether the material advantage depends on the tested NO cofeed**, not whether NO can promote wet or sulfated Pd. The latter is established. A clean negative result could reveal a material limit; a precise null could validate the tested cofeed boundary. Either changes a practical choice only if that boundary occurs in a real application. Neither outcome needs to be known before the experiment is justified. A new mechanistic name or an extensive sulfur map is unnecessary to obtain that first useful answer.

Originality remains provisional and narrower than the proposal's general chemical motivation. The strongest surviving contribution would be a reproducible, quantitatively bounded change in the cluster catalyst's advantage under a relevant NO-removal history, followed by successful prediction at one withheld condition. A routine NO benefit common to all catalysts would contribute little beyond existing work.

## What the original sources establish

### The strong result and its boundary

Ryu Figure 6m shows the best ST-CO-N2-O2 monolith near 95% methane conversion throughout its reported sequence. The SO2-containing intervals also contain NO. The ST-CO-O2 omission-treatment sample falls from roughly 85% to 45% conversion during sulfur intervals and recovers when sulfur is removed. Therefore, the figure establishes a large treatment-dependent response under this feed, but does **not** establish irreversible sulfur damage in the weaker sample, wet sulfur tolerance without NO, or intrinsic exclusion of sulfur from the active Pd population. The late continuous sulfur interval is approximately 80–150 h; 150 h is the whole sequence. [Ryu2024](https://doi.org/10.1038/s41467-024-52698-4)

The recovered source-data workbook has three sheets for Figures 6k, 6l and 6m. Sheet 6m contains time and the two methane-conversion series. It does not supply measured NO/SO2 switching traces, sulfur balance or internal catalyst temperatures. It therefore strengthens access to the conversion record without closing those measurement gaps. [Original Figure 6 data](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-52698-4/MediaObjects/41467_2024_52698_MOESM7_ESM.xlsx)

SI Figure 28 and Table 6 support similar average prepared Pd environments for the two treatments. They do not establish identical minority active populations or working sulfur speciation. Table 7 includes 10%-water light-off measurements, with reported T50 values of 283 °C for ST-CO-N2-O2 and 323 °C for ST-CO-O2, both at 5000 ppm CH4. These are not sulfur tests. No NO-free wet sulfur experiment or internal-temperature profile was found in the inspected SI. [Original SI](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-52698-4/MediaObjects/41467_2024_52698_MOESM1_ESM.pdf)

The public review file documents powder tests at 200 and 400 mL min−1 with 60 mg catalyst diluted in 540 mg quartz. Similar rates below 20% conversion support the stated powder kinetic regime. They do not establish isothermal operation of the 95%-conversion monolith. Earlier review rounds discuss CaO and extra heating; these abandoned draft approaches must not be confused with the final material claim. [Public review file](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-52698-4/MediaObjects/41467_2024_52698_MOESM2_ESM.pdf)

Mortensen Figure 2 independently confirms a striking dry-to-wet contrast: after dry sulfur recovery and prolonged high conversion, adding 10% water while sulfur remains causes severe loss. Its 3 wt% Pd/H-CHA, preparation, temperature and feed differ from Ryu's. It supports the importance of simultaneous contaminants, not a direct contradiction of Ryu. The authors explicitly retain sulfate redistribution/storage and gas-phase release as unresolved explanations. [Mortensen2025](https://doi.org/10.1007/s11244-025-02114-y)

### Quantitative comparison checks

- **Gas throughput:** Ryu's 20,000 Lgas Lmonolith−1 h−1 divided by 100 gcat Lmonolith−1 gives approximately 200 Lgas gcat−1 h−1. Mortensen uses 126 Lgas gcat−1 h−1. At nominal 1 versus 3 wt% Pd, gas throughput per Pd mass is about 4.76 times larger for Ryu. Volume space velocity alone would give a misleading comparison. Measured Pd loading and the gas reference state remain preferable for a new experiment.
- **Heat release:** using 802 kJ molCH4−1 and an illustrative mixture heat capacity of 32 J molgas−1 K−1 gives ideal complete-conversion adiabatic rises of about 125 K at 5000 ppm CH4 and 25 K at 1000 ppm. These are bounding calculations, not observed hot spots. A temperature effect is neither established nor safely excluded by furnace temperature or powder dilution alone.
- **Sulfur input:** a 1-inch-diameter, 1-inch-long monolith has nominal volume 0.01287 L and approximately 1.287 g catalyst at the stated loading. With nominal 1 wt% Pd, 4.3 L min−1, 10 ppm SO2 and a 70 h interval, the supplied S/Pd atomic ratio is about 61 using 24.45 L mol−1. This is input, not uptake. It does not show that all sulfur reached Pd or rule out selective capture of only part of the incoming sulfur by support, binder or reactor surfaces.

## Direct prior art changes the hypothesis

Three primary publications already make generic NO promotion an inadequate novelty claim:

| Source | Established boundary used here | Reading limit |
|---|---|---|
| [Sadokhina2017, DOI 10.1016/j.apcatb.2016.07.012](https://www.sciencedirect.com/science/article/abs/pii/S0926337316305458) | Combined water and NO can restore activity even when each inhibits separately; sulfur-free wet NO switches are essential. | Main text now retained; observed response is distinct from a unique mechanism. |
| [Sadokhina2018, DOI 10.1016/j.apcatb.2018.05.018](https://research.chalmers.se/en/publication/505174) | NO delays wet sulfur inhibition on PtPd/Al2O3; authors connect this to altered sulfate/sulfite formation, with strong temperature dependence. | Main text now retained; DRIFTS supports different sulfur species, not universal mechanism transfer. |
| [Auvinen2021, DOI 10.1016/j.cej.2020.128050](https://www.sciencedirect.com/science/article/pii/S138589472034167X) | NO inhibits fresh but promotes sulfur-poisoned catalyst; hydroxyl removal and changed support/Pd sulfation are proposed. | Main text now retained; observed response is distinct from a unique mechanism. |

These sources support plausibility of an NO dependence, not its magnitude or mechanism on anchored Pd/SSZ-13. The temperature, support and metal differences prohibit direct parameter transfer. These retained main texts strengthen the prior-art boundary. They do not establish that the particular Ryu material has the same response or that the proposed sequence is unprecedented.

## A smaller, more decisive experiment

### 1. Establish a fair bridge to the published result

Reproduce the two published preparation histories with independent preparations. Measure actual Pd content and wet clean-feed activity. Use the omission treatment to test the preparation contrast; use a characterized practical Pd/Pt comparator to judge useful performance. These are different controls.

First establish the preparation contrast under the reported feed and stated formulation, then bridge sequentially to a dilute, thermally controlled diagnostic point. Immediately changing methane, water, sulfur, oxygen and temperature together would leave a failed transfer uninterpretable. A powder campaign can provide useful information, but only a matched formulated-monolith test can reproduce the Figure 6m claim. A binder-containing powder can retain the formulation boundary; a binder-free powder is a distinct material, not automatically a reproduction of Figure 6m.

Use internal temperature measurements and a dilution/flow check that preserves the chemical comparison. At useful conversion, document axial temperature differences where measurable. At a lower-conversion diagnostic condition, test whether the NO response persists when methane heat release is small. Changing methane concentration alone changes surface kinetics too, so it cannot uniquely diagnose heating. Equal nominal furnace temperature is insufficient.

### 2. Test the operational interaction before locating sulfur

On the best reproduced material, compare fixed-wet NO absent/present and sulfur absent/present histories on separate aliquots where slow exposure matters. Keep actual molar flows, temperature, Pd inventory and exposure time explicit. A sulfur-free NO switch measures the ordinary wet NO response. Sham continuation controls ordinary drift and switching disturbance.

After a defined NO/SO2 exposure, remove NO while continuing SO2, then restore NO. Compare with a never-NO sulfur history and matched continuation. **Also retain a limited SO2-off arm at fixed NO**, followed by a common wet assay, if the initial result is consequential. Otherwise a response to NO removal cannot distinguish ongoing sulfur inhibition from memory of prior exposure. Common assays can themselves relax or erase state; record their transient rather than treating a recovered endpoint as an untouched census.

The primary result is an operational interaction: does NO removal change sulfur-associated methane slip beyond the sulfur-free NO response, and does it change the material advantage? A difference-in-differences in conversion is descriptive because conversion is nonlinear in rate and may be thermally coupled. Establish the rate contrast in the controlled diagnostic regime and measure integrated methane slip directly at useful conversion.

**The null model must specify the response scale.** Even independent multiplicative effects on intrinsic rate can produce an additive NO×S interaction in conversion. As an illustration, an isothermal first-order plug-flow model gives `X = 1 − exp(−kτ)`. Starting at `kτ = 3`, independent NO and sulfur factors of 1.2 and 0.3 give an NO-associated conversion gain of about 0.0225 without sulfur and 0.0670 with sulfur. That difference does not establish coupled surface chemistry. This illustrative model is not a fit to the reported monolith. Test a predeclared independent-effects baseline using differential rates or an appropriately validated reactor model. For a multiplicative rate baseline, the ratio `r(NO,S) × r(0,0) / [r(NO,0) × r(0,S)]` equals one; an additive difference in rates is not the corresponding null test either. Matched temperature, working history and uncertainty remain necessary, and a departure from this baseline alone does not identify its molecular cause. Integrated slip can still change meaningfully under independent effects and remains a valid practical outcome.

Binary 0/200 ppm NO is a reasonable first bridge to the publication. If a consequential dependence appears, select **one application-relevant lower NO concentration or NO/NO2 mixture** for the withheld history. Choose it from an identified exhaust location or measured feed envelope; do not invent a universal “low-NOx” threshold. A dense NO-dose library is unnecessary. Changing aftertreatment location also changes temperature, NH3 and NO2, so the binary experiment alone cannot choose an installation location.

### 3. State exactly what the measurements can discriminate

| Observation under controlled local temperature | Supported inference | Inference still unavailable |
|---|---|---|
| Prompt reversible NO effect, also present without sulfur | Ordinary cofeed kinetics contribute. | Unique hydroxyl, Pd-redox or adsorbate mechanism. |
| Sulfur-specific NO response persists into a common assay | Exposure history affects measured function over that assay horizon. | Irreversible damage or its structural cause. |
| Different whole-catalyst retained S or exported sulfur | NO changes a sulfur balance or inventory. | Location on Pd versus zeolite/binder; direction of causation for activity. |
| Equal total retained S but different activity | Total S is insufficient as an activity predictor. | Absence of sulfur redistribution or identical sulfur speciation. |
| NO effect diminishes after heat release is suppressed and measured temperatures are matched | Thermal feedback contributed to the useful-conversion response. | An exclusively thermal origin without the corresponding chemical controls. |

Measure methane, CO/CO2 and NO/NO2, with N2O where relevant, from the outset. Quantitative wet sulfur sampling needs blank, line-recovery and capture checks; missing gaseous SO2 is not automatically catalyst storage. Whole-sample sulfur balance is useful, but **do not require exhaustive sulfur mapping before the primary finite compatibility decision**. Component-resolved sulfur speciation, binder comparisons or operando measurements are conditional branches if distinguishing mechanisms would change material or operating choices.

The preparation comparison remains confounded at the microscopic level even if ensemble EXAFS and microscopy look similar. An N2 hold between 700 °C CO reduction and 500 °C oxidation changes the preparation trajectory. Persistent behavior after aqueous washcoating, calcination and wet operation cannot be assigned uniquely to a temporary absence of adsorbed water. Report a preparation-dependent effect until stronger causal evidence exists.

## Prediction, stopping and value

After commissioning establishes analytical precision, ordinary drift and preparation/run variability, predeclare a finite horizon, a minimum useful change in integrated methane slip and sufficient independent preparation/history repeats to resolve it. Multiple points from one bed do not substitute for independent replication. Freeze the criterion before evaluating the decisive comparison. Compare equal measured Pd inventory for the two Pd materials; report Pt and Pd separately for a bimetallic practical reference, together with total precious-metal inventory. Equal-volume comparisons answer a packaging question; equal precious-metal mass is a resource comparison, not an intrinsic turnover-frequency measurement.

Use the calibrated response to predict one withheld NO history at a fixed wet sulfur condition. A lower finite-NO application test must use a separately established joint feed envelope; if none is available, retain the diagnostic boundary and stop. Count startup, inhibition and recovery in cumulative slip. Do not extrapolate finite sulfur tolerance to indefinite life. The prediction may establish a useful operating limit without uniquely resolving sulfur location.

**Stop or demote** if a modest reproduction effort fails, the apparent advantage is removed by thermal/sampling corrections, the NO response is conventional and does not change a useful choice, or a credible practical reference removes the benefit. A near-zero interaction with adequate precision is a useful validation of the specified NO-free diagnostic boundary, not a reason to run indefinitely for a positive effect.

**Expand** if the material retains a consequential advantage under the withheld relevant history, or if an NO-dependent failure reveals a controllable limitation and a specific intervention with a credible benefit. Expansion does not automatically mean new synthesis: material selection, an operating limit or avoiding an unsuitable placement can be the useful outcome.

Chemical confidence is moderate for an NO effect on wet Pd generally and lower for a consequential effect on this particular material. A carefully bounded operational experiment is more feasible and identifiable than a unique sulfur-partition mechanism. Methane abatement is important, but practical relevance of this particular NO/sulfur boundary and the likelihood of a new durable improvement remain unestablished. The study's broadest value would come from a transferable, validated way to separate material durability from favorable cofeed conditions; generic response fitting alone does not supply that advance.

## Historical literature handoff and retained artifacts

The access statements below record the original review. Auvinen2021 and Sadokhina2017/2018 main texts are now retained; they are not outstanding main-text requests. See the [post-upload audit](post-upload-methane-audit.md) and [current literature status](../literature-status.md). Supplement access and exhaustive figure review are separate questions.

The sole literature agent `/root/literature` received the two newly identified Sadokhina sources above and the authentic Ryu SI, source-data and public-review artifacts, with the requested **Add identified literature** path, absolute skill/project/KB paths, relevance and reading limits. No knowledge-base files were changed and no `lit.py check` was run by this reviewer.

- Skill: `/home/sgusev/repo/skills/literature/SKILL.md`.
- Project: `/home/sgusev/repo/catalisys-notes`; KB: `/home/sgusev/repo/catalisys-notes/literature`.
- Ryu SI: `/tmp/wet-methane-screen/robust2024-si.pdf` and extracted text; 16,810,701 bytes. Selected sections read and Figure 28 inspected visually; remaining SI not exhaustively reviewed.
- Figure 6 data: `/tmp/wet-methane-screen/robust2024-fig6.xlsx`; 147,495 bytes. Sheet labels and column contents inspected; no independent remeasurement of conversions claimed.
- Public review: `/tmp/wet-methane-screen/robust2024-peer-review.pdf` and text; 27,278,793 bytes. Selected sulfur and transport responses read; historical drafts remain distinct from the final paper.
- At the original review, Sadokhina2017, Sadokhina2018 and Auvinen2021 main/SI texts had not been read; metadata-only inclusion and unresolved-source reporting were requested. Their main texts are now retained, with selected Auvinen methods and mechanism interpretation checked in the post-upload audit. This does not assert exhaustive supplementary-data review.
