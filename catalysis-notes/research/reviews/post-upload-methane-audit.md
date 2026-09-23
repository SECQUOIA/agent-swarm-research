# Wet-methane proposal after the literature uploads

2026-09-16. Targeted reassessment of the existing NO-cofeed diagnostic. No new direction or experiments. The Auvinen and Tan methods below were checked against text extracted directly from their retained original PDFs; this was not a complete reanalysis of their figures or raw data.

## Decision

**Retain the lower-priority diagnostic decision.** The uploaded sources strengthen the prior art for history-dependent NO effects and provide a better specified wet, sulfur-free comparator. They do not establish that the proposed NO-free sulfur condition controls a real application choice, or demonstrate its behavior on the particular Ryu Pd/SSZ-13 material.

The immediate corrections are to replace obsolete main-text access claims, distinguish measured functional effects from proposed surface mechanisms, and specify comparator conditions. There is no basis here to restore methane to the same priority as the Ag/polymer bounded studies.

## What the full texts now establish

### NO effects already depend on sulfur history

[Auvinen2021, Chemical Engineering Journal](../../literature/papers/auvinen2021-effects-of-no-and-no2/original.pdf), DOI `10.1016/j.cej.2020.128050`, studies a commercial alumina-supported Pd/Pt monolith. Methods and Table 1 on PDF p.2 specify Pd:Pt mass ratio 4:1, 7.06 g precious metal/L and 50,000 h−1. The aging protocol uses 10 ppm SO2 at 450 °C for 10 h; NO-switch experiments include 500 and 1700 ppm pulses. These are distinct conditions from Ryu's zeolite-cluster experiment.

The source reports immediate NO inhibition on fresh catalyst and promotion on a sulfur-poisoned state. Its sulfur-partition interpretation and calculated HNO2-mediated hydroxyl-removal pathway provide plausible explanations, not a demonstrated unique pathway on every supported Pd material. The abstract and conclusions explicitly retain uncertainty about the explanation of promotion. The current package summary should preserve that qualification when stating hydroxyl removal.

The now-retained [Sadokhina2017](../../literature/papers/sadokhina2017-the-influence-of-gas-composition/original.pdf) and [Sadokhina2018](../../literature/papers/sadokhina2018-deceleration-of-so2-poisoning-on/original.pdf) primary papers further support the existing warning that NO effects depend on water, temperature and aging. The 2018 paper connects slower sulfur deactivation with different sulfur species observed by DRIFTS. A newly observed NO×sulfur interaction in conversion would therefore be neither a novel general phenomenon nor a unique chemical discriminator.

**Existing experiment to retain:** test whether the *relative material advantage* survives removing NO under controlled histories, temperatures and sulfur exposure. A common penalty across all materials has less decision value than a changed ranking or inventory requirement. Do not infer such a change from these alumina-supported precedents.

### The strong wet reference now has explicit conditions

[Tan2025](../../literature/papers/tan2025-a-highly-active-and-stable/original.pdf), DOI `10.1016/j.apcatb.2024.124562`, supplies the previously missing main text for Pd/Na-IWV. Methods §2.2, PDF p.2, use 0.3 g catalyst, atmospheric pressure, 1500 ppm CH4, 5% O2 and 10% H2O at a reported GHSV of 100,000 h−1. Neither NO nor sulfur is specified in that feed. Figure 2 and the conclusions report about 85% conversion over 100 h at 330 °C for the 3 wt% Pd/Na-IWV material with Si/Al 45.

This is a credible **wet sulfur-free reference**, not proof of sulfur tolerance or a direct ranking against Ryu's 350 °C, sulfur/NO-containing monolith experiment. Do not compare the two conversion percentages without matching methane loading, water, sulfur history, actual temperatures, catalyst/PGM inventory and flow basis. GHSV alone does not supply a common precious-metal productivity denominator.

The availability of this source improves comparator design. It supplies no measured NO-free sulfur response for the Ryu material and no joint low-NO/sulfur application envelope.

## Implementation, 2026-09-16

Implemented in the existing screen and four methane reviews: current main-access statements, the defined Tan wet sulfur-free comparator, proposed-mechanism qualification, source-pair/feed reproduction before sequential bridging, independent preparation/history repeats sized after commissioning, rate-based interaction null and material-ranking decision, and the unchanged real-application gate. Old retrieval handoffs are explicitly historical and link to current status. No experiments or new research directions were added.

Tan §2.2, Fig.2 text and conclusions and Auvinen methods/Table 1 and mechanistic discussion were rechecked against text extracted directly from their retained original PDFs. This verifies the quoted conditions; it is not a fresh exhaustive figure/data reanalysis. Source-note repairs remain the responsibility of the sole literature worker and are not asserted completed by this review.

## Audit recommendations and source-note follow-up

- **Implemented:** added a dated source update to [wet-methane-value-screen.md](../working/wet-methane-value-screen.md) and [wet-methane-low-no-relevance.md](wet-methane-low-no-relevance.md). Main texts for Auvinen, Sadokhina, Tan, Hutter and Kinnunen are now retained; historical abstract-only descriptions should no longer serve as the current access record.
- **Implemented:** retained the original application gate: one real operating envelope must jointly specify NO/NO2, sulfur, methane, water, temperature and flow. The uploaded laboratory studies do not justify assembling these independently from unrelated sources.
- **Literature-worker follow-up:** repair the Sadokhina and Kinnunen literature notes before relying on them as reusable summaries. The Sadokhina2017 note uses general support background as its principal finding; Kinnunen2018 labels a keywords/reference-list fragment as a central outcome. Those are note-quality problems, not evidence against the underlying experiments.
- **Implemented:** preserved the existing coupled-catalyst accounting caveats: added bed length, precious metal, heat and sulfur storage confound simple comparisons, and a sum of separate conversion percentages is not a physical combined-system prediction.

## Confidence

Confidence that NO effects can depend on catalyst history is high for the cited tested systems. Confidence that the particular Ryu material has a consequential dependence remains lower. The bounded comparison can be informative with suitable equipment and reproducible materials, but no platform was checked. Confidence in practical improvement remains low until a real feed and a changed catalyst/operation choice are demonstrated.

No new missing source was identified in this methane audit. Literature packages were not modified.
