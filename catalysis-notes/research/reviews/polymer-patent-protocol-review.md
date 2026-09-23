# Independent review: polymer reuse, regeneration, and waste protocols in WO2026011187A2

Date: 2026-09-15. Source: Hartwig, Conk, and Bell, [*Conversion of polyolefins*, WO2026011187A2](https://patents.google.com/patent/WO2026011187A2/en), published January 8, 2026. This review concerns scientific prior art and experimental interpretation, not patent scope or legal status.

**2026-09-16 correction after upload:** the [post-upload audit](post-upload-polymer-audit.md) visually checked Science Figure 4B and SI S20. The published reference uses **three total 1 g PE charges, with 400 mg fresh Na/alumina added before charge 2 only**; charge 3 receives only PE. The nominal fresh-solid total is 1.2 g and the conditional three-charge material-productivity ratio is `B = 2f`, not the separate every-later-charge illustration `B = 1.5f`. The Science SI reports **19.9658 g warm oil, 29.9717 g remaining solid and 80.1% apparent conversion** for its scale-up; the patent record below contains different numbers and remains a distinct source. Neither residue subtraction nor the condensate volume/density estimate closes a polymer-specific carbon balance. These corrections supersede the old missing-dose/Science-access limits; patent regeneration figures and the dissertation body remain unresolved.

## Decision

**The patent improves protocol readiness but further narrows the novelty of the proposed impurity program. It does not justify promotion to a substantial program.** Fresh Na/alumina addition has already restored output in a reused catalyst mixture. High impurity doses already depress yield. DME regeneration is described in experimental methods, not merely mentioned prospectively. A new campaign must therefore predict a consequential cleanup, catalyst-makeup, or regeneration decision from measured contaminant exposure and surviving functions. Repeating component rescue or showing dirty-feed inhibition is insufficient.

A material uncertainty remains: the accessible text does not securely associate the DME treatment with the older Na/alumina formulation rather than the newer Na–Fe/alumina formulation, and its numerical recovery results are in an unavailable figure. Treat the disclosed treatment as a required comparator whose applicability and efficacy need verification.

This updates the access and novelty judgments in the [earlier independent review](polymer-independent-review.md) and [alternative screen](../working/alternative-screen.md). That original patent-only review did not establish that the Science paper/SI had been read; their later upload and original-figure check now resolve the published reuse control above.

## What the experimental text establishes

### 1. Reuse and addition of fresh Na are already demonstrated claims

Paragraph **[0135]** describes ending the HDPE reaction, dismantling the reactor under inert atmosphere, adding another HDPE portion to the retained catalyst, and repeating the reaction. It reports 50% activity retention on subsequent runs and a cumulative W-based TON of 1030 over three runs. It separately reports that adding fresh Na/γ-Al2O3 in the second cycle restores activity for two new reaction cycles, referring to **Fig. 3B**.

Three limitations matter:

- The wording does not unambiguously distinguish retention relative to the initial run from successive fractional losses. Fig. 3B is needed; do not manufacture a 100–50–25% trajectory.
- The prose alternates between repeating the process three times and a TON over three runs. It does not provide the fresh-Na addition mass, numerical cycle yields, or a complete catalyst inventory for each sequence.
- Adding fresh Na-containing solid is catalyst makeup. It does not establish that the original Na component retained activity, that W retained all its original sites, or that Na protects W by capturing contaminants. Extra initiation/isomerization function, altered activation, poison capture, and solid contact remain alternatives.

The baseline batch procedure in **[0165]** uses 1.000 g PE, 400 mg WO3/SiO2 and 400 mg Na/γ-Al2O3, with 10 bar methane and 15 bar ethylene charged to a 300 mL Parr vessel. It heats to 320 °C, starts stirring after 150 °C, and samples after 90 minutes. These are useful experimental details, but they cannot fill the missing cycle-specific quantities by assumption. Neither charged pressure nor the 90-minute dwell alone specifies the full hot-pressure or turnaround history.

**Consequence:** a rescue matrix can remain a control within a new study. It is not itself the new contribution. Any practical comparison must charge fresh Na makeup and the retained total solid inventory to the process.

### 2. The DME comparator includes oxidation, purges, and handling

The three regeneration procedures differ materially:

| Text locator | Treatment before the subsequent HDPE test | Composition and outcome limits |
|---|---|---|
| **[0172]–[0173]** | Spent solids handled in ambient air; air at 150 SCCM; 10 °C/min ramp to 600 °C; 3-hour hold; cooling and glovebox transfer. | Explicitly starts from 400 mg W catalyst plus 400 mg 10 wt% Na/alumina and 1 g HDPE. Subsequent yield is referred to Fig. 21, not given numerically in this text. |
| **[0174]–[0175]** | Same air treatment at 600 °C, then He at 150 SCCM for 30 minutes and H2 at 100 SCCM for 3 hours at 600 °C; cooling and glovebox transfer. | Same explicitly named older Na/alumina starting mixture. Again refers to Fig. 21. |
| **[0176]–[0177]** | Approximately 800 mg spent mixture handled in ambient air; air at 150 SCCM with a 10 °C/min ramp to **450 °C**, then 3-hour hold; He at 150 SCCM for 30 minutes; **5% DME in He at 100 SCCM for 30 minutes**; He at 150 SCCM for another 30 minutes at 450 °C; cooling and glovebox transfer. | Does not restate the mixture's component identities. The subsequent test uses **771.0 mg** recovered mixture with 1.000 g HDPE. Numerical yield again requires Fig. 21. |

All subsequent tests in **[0173], [0175], and [0177]** charge 15 bar ethylene and 10 bar methane and use 320 °C for 120 minutes, with time zero defined at 310 °C. The text places reaching that temperature roughly 25–30 minutes after heating begins. These tests should not silently be treated as the same 90-minute baseline protocol.

The DME sequence contains **4.5 hours of specified hot holds**, before ramps, cooling, transfers, and the next reaction. It is not a simple 30-minute in-reactor pulse. Nominal regeneration gas deliveries per stated treatment are 27 standard L air, 9 standard L He in the two pure-He holds, and 3 standard L DME/He mixture, including 0.15 standard L DME. These are arithmetic from stated flows and times, not measured consumption or optimized process requirements. Ramps may add gas use. The 771 mg recovery from an approximately 800 mg starting mixture does not by itself identify catalyst loss versus removal of retained material or measurement/handling differences.

**Identification problem:** **[0032]** describes Fig. 21 as a Na–Fe/Al2O3 regeneration result. The patent separately provides Fe/alumina, Na–Fe/alumina, and Na2CO3–Fe/alumina syntheses in **[0147]–[0150]**, and its adjacent reaction methods refer to Fe formulations and Figs. 19–20. Thus, the new formulations are real experimental disclosures, not names in a broad claim alone. But the contrast between the Fig. 21 description, the explicitly Na-only air-treatment methods, and the unnamed DME mixture is unresolved without the actual figure and complete original document.

Do not assign a numerical DME recovery yield, claim repeated quantitative regeneration, or assume the regenerated component's structure. Even if numerical results are recovered, air-only at 600 °C versus air-plus-DME at 450 °C does not isolate a DME effect: the oxidation temperature also differs. A mechanistic DME comparison needs a matched 450 °C air/He sham without DME, alongside the complete disclosed sequence as a practical comparator.

### 3. Waste-polymer conversion was preceded by substantial preparation

The postconsumer examples in **[0132]** include a jug, centrifuge tube, and bread bag. **[0198]** states that **all waste sources** were cut below 10 × 10 mm, dissolved in boiling toluene, precipitated in methanol under stirring, filtered, vacuum-dried for 18 hours at 200 mTorr, and ground to powder. The laboratory recipe uses 125 mL toluene and 1.25 L methanol per 5 g waste: nominally 25 L and 250 L per kg at that scale, before any solvent-recovery credit. These ratios document the preparation; they are not a proposed industrial solvent demand.

**[0199]–[0200]** puts the waste-LDPE NMR analysis after this preparation. The reported PE fraction therefore cannot be treated as a complete characterization of the original unsorted waste stream.

The treatment can change extractable additives, water, physical form, and polymer–catalyst contact. Without before/after balances its actual impurity removal cannot be quantified. These are demonstrations on **prepared postconsumer-derived polymers**, not demonstrations of sustained tolerance to untreated postconsumer feeds. A credible new impurity program must compare against this solvent preparation, or a measured less intensive cleanup, and include polymer recovery and contaminants removed.

### 4. Contaminant intolerance is directly disclosed; a feed specification is not

**[0133]** reports reduced propylene yields with PVC, PET, and DEHP; PS causes much less change. **[0168]** supplies the test: 50 mg contaminant per 1.000 g HDPE, with the standard 400 mg + 400 mg catalyst inventory and 90-minute batch protocol. This is 5 wt% relative to HDPE, rather than 5 wt% of all polymer plus added contaminant.

These substantial challenge doses do not define an allowable residual concentration, a working capture capacity, or lifetime under repeated lower-dose feed. They also do not locate the damaged function or demonstrate Na-to-W protection. PET's polymer-bound ester oxygen and DEHP's molecular oxygenates are different exposure pathways; bulk elemental input is not the dose delivered to a working W site.

The surviving scientific opportunity is therefore narrow but meaningful: determine whether lower cumulative impurity exposures on a specified prepared feed change which function limits sustained output, and whether a measured intervention reduces total cleanup/makeup/regeneration burden. This would need held-out prediction, component-function controls, and a practical comparison. It remains a hypothesis, not something established by these disclosures.

## Revised gates and confidence

1. Use the now-verified Science Figure 4B three-charge control: 400 mg Na/alumina added before charge 2 only, with only PE added before charge 3. Keep seeking patent Figs. 19–21 and complete **[0169]–[0171]** for its distinct DME/catalyst-identity question; do not delay the published clean-reuse comparison or assign a DME efficacy without those results.
2. Reproduce one fully specified clean-feed time course and the fresh-Na makeup comparison. Establish whether the molecular assays preserve or restore the state they are meant to measure.
3. Characterize one actual feed before and after the candidate cleanup. Connect controlled contaminant exposures to measured residuals and cumulative throughput before calling them realistic.
4. Only then compare protection or recovery against documented catalyst makeup, the complete applicable regeneration sequence, and cleanup. Require a prediction that changes an economically or materially consequential choice.

Confidence that the patent contains useful reproducible synthesis and batch details is **moderate to high**. Confidence in the published Science three-charge makeup inventory is **high** after the upload check; confidence in reconstructing the patent's distinct complete regeneration benchmark remains **low**. Confidence in the proposed sacrificial cross-protection mechanism remains **low to moderate**; this patent supplies no direct verification. Confidence in practical improvement remains **low to moderate and conditional**, with the large solids inventory, solvent preparation, and regeneration downtime now more concrete concerns.

## Read limits and literature handoff at the original 2026-09-15 review

Read the accessible primary patent description around **[0121]–[0137], [0142]–[0150], [0165]–[0177], and [0198]–[0202]**, plus figure descriptions and relevant claims to distinguish them from experimental methods. The original Google HTML was preserved at `/tmp/polymer-primary-gap/WO2026011187A2.html`; the corrected UTF-8 text used for review is `/tmp/polymer-primary-gap/review-description.txt`. It contains missing pieces of paragraphs and absent figures and must not be labeled a complete original PDF.

Original-document retrieval remained unsuccessful: WIPO, Espacenet, and unauthenticated EPO OPS returned 403; Google supplied no original PDF link; the public Patsnap page exposed a signed PDF URL that returned 403, including after refreshing the public page. No restriction was bypassed. Fig. 3B, Figs. 19–21 and incomplete paragraph starts remain **unretrieved and unread**.

The single literature agent `/root/literature` received the access limits, composition ambiguity, and artifact paths. No knowledge-base files were written and no KB maintenance was run by this reviewer. The companion accounting note received the independent arithmetic and source-text check recorded below. That check does not validate the missing original experimental data or close the full carbon balance.

## Independent check of the companion accounting note

After writing this protocol assessment, independently read the [root's benchmark accounting](polymer-patent-benchmark-accounting.md), rechecked **[0130], [0134], [0137], [0168], and [0228]–[0236]**, and recomputed its elemental-input ratios, PE-to-propylene balance, 87.2% batch-yield interpretation, source condensate arithmetic, and apparent 69.8% conversion. No correction was required. The source's volume/density/mole-fraction calculation indeed gives approximately 0.9977 mol when divided by pure-propylene molar mass; the note correctly declines to label this a validated mixture-based yield. The discrepant warm-condensate masses and the distinction between 438 mixed-olefin turnovers and the source's 364 propylene turnovers are accurately preserved. None of these arithmetic checks supplies the missing figures or closes the complete experimental carbon balance.
