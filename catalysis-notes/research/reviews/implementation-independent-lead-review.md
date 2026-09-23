# Independent verification of the implemented Ag and polymer proposals

2026-09-16. Fresh, bounded review of the implemented existing ideas. This reviewer did not develop a new direction, change the proposal files or edit the literature knowledge base. No experiments were performed. The review checks the active program/design/accounting files against the uploaded primary evidence and the decision brief, rather than accepting the implementation summaries alone.

## Verdict

**The implemented polymer and Ag corrections pass this bounded review.** One moderate inconsistency in the Ag experimental gates was found, corrected by its implementer, and rechecked below. No unresolved correction was identified in the reviewed lead files. Neither proposal establishes practical superiority or a substantial original program before experiments. Their retained status as finite decision studies is appropriate. The remaining chemical uncertainties are explicit research questions, not errors that editorial revision can remove.

## Finding corrected and rechecked

| Severity | Location at review | Finding and required resolution |
|---|---|---|
| Moderate: experimental sequence | [Ag core design](ag-core-experimental-design.md), Section 2, originally lines 39–45; minimum sequence, originally line 114. Related [program](../programs/ag-selective-oxygen-use.md) fresh-response row, originally line 20. | Section 2 still describes the required matched-condition response as a Ni-with/without-Re comparison, despite the new minimum being one promoted Ni/no-Ni pair. Its first-pair gate also says to continue when an advantage or incompatibility is resolved, before the subsequent ordinary-retention stage. The historical motivation includes little initial selectivity difference and later divergence. Specify the initial matched-condition pair, make Re interaction conditional, and state that lack of a fresh advantage alone does not cancel the predefined finite retention comparison when both formulations meet the useful-output floor. Close after the ordinary-operation horizon lacks a useful difference, or if platform qualification fails. |

**Resolution verified:** the implementer corrected core Section 2, its chloride-collapse paragraph and first-pair stage, plus the program's fresh stage, first decision, Aim 2 entry and curve-collapse paragraph. The first matched-condition comparison is now the promoted Ni/no-Ni pair; the Re interaction is conditional. Both qualified formulations proceed through the predefined ordinary-retention horizon despite equal fresh output. The finite stop remains in force. This reviewer read the updated clauses after the correction. The finding is closed. It concerns consistency between executable stages, not evidence that Ni improves retention. The decision brief's finite-horizon and uncertainty statements agree with the detailed proposals.

## Polymer: primary evidence and accounting pass

- **Science Figure 4B:** independently rendered and inspected original main PDF page 4. The caption specifies three total PE charges, 400 mg of each solid initially, 400 mg fresh Na/alumina added in the second charge, and only PE in the third. “Replaced Sodium” is a plot label; the caption describes addition to the retained mixture. The implementation correctly treats this as established supplementation, not selective removal or new rescue chemistry.
- **Science SI S20:** independently rendered and inspected the original page. It gives 19.9658 g warm condensate, 29.9717 g remaining solid and 80.1% apparent conversion. The equation reports an estimated 1.00 mol propylene, 28.1% yield and 364 W turnovers. These remain distinct from the main article's mixed-condensate 438 TON and the patent's separate mass record. Original equation S18 indeed multiplies total estimated liquid mass by a stated mole fraction and divides by propylene molar mass. The implementation appropriately preserves this as the source estimate with a mixture-molar-mass/density limitation, rather than presenting a corrected measured yield.
- **Arithmetic:** independently recalculated `B/f = 0.8 × 3 / 1.2 = 2` for the published schedule, versus `3/2` for the separate every-later-charge illustration. Residue subtraction gives 80.0566% for Science and 69.8% for the patent. These are conditional accounting results; neither calculation measures polymer-carbon recovery, total cost or lifetime.
- **Carbon boundary:** the [makeup calculation](../calculations/polymer-makeup-burden.md) defines accepted polymer-derived carbon, excludes silently counting ethylene carbon, and prevents double counting carried-over polymer. It distinguishes fresh solid supplied from physical retained inventory, equal feed from equal output/capacity, and reaction time from the full cycle. The [benchmark accounting](polymer-patent-benchmark-accounting.md) preserves the ethylene-incorporation and scale-up limits.

Primary files inspected: [Conk main](../../literature/papers/conk2024-polyolefin-waste-to-light-olefins/original.pdf) and [Conk SI](../../literature/papers/conk2024-supporting-information-for-polyolefin-waste/original.pdf). The main was rendered from its matching inbox original, `literature/inbox/science.adq7316.pdf`.

## Polymer: experimental logic and value pass

The [active exposure design](polymer-exposure-falsifiability.md), especially Sections “Smallest useful sequence” and “Falsification and the decision each result changes,” contains the necessary causal distinctions:

- Clean aging and handling are separate from added exposure. Already functioning components receive clean interruption controls.
- Parent-ketone input is not automatically effective exposure. Transformation, water, melt/pore retention and washout must be measured sufficiently for the claim.
- Molecular assays can reactivate material; a component recovery result must predict operating-mixture behavior and a common subsequent clean charge.
- Polymer trajectory and residual inventories can imitate catalyst memory. Unresolved attribution is retained rather than assigned to damage.
- Equal dose predicts equal final function only under the specified simple model; it does not predict equal integrated output.
- The known three-charge makeup policy is the comparator. Independent preparations and decision-resolving repeats are required without an invented universal replicate count.
- Failure of unequal recovery, transfer, useful output significance or a relevant feed connection closes the corresponding claim. A successful molecular contrast alone does not establish a feed specification.

The [value review](polymer-value-after-patent.md) appropriately gives low-to-moderate chemical confidence, conditional moderate information value, and low confidence in practical improvement. Published rescue, W oxygenate tolerance/recovery and coke reduction constrain novelty. The remaining proposed contribution is a prospective exposure relationship that changes a consequential feed or makeup choice. This is a plausible bounded opportunity, not verified originality across the inaccessible dissertation and patent figures.

## Ag: uploaded primary corrections pass

- **Iyer2021:** independently rendered original PDF p.9 and checked Section 3.4 with Figures 8–9 text. The paper computes local coverage and rate from partial pressures while integrating from the inlet, and compares predictions with integral-reactor output and averaged coverage. The program now credits this demonstrated assembled steady-reactor prediction. It does not claim this is a validated arbitrary-time recovery model or equate individual residuals with a confidence interval.
- **Jalil2025 SI:** independently inspected original preparation text and rendered Figure S21. The no-Ni control follows NiAg processing without Ni addition; glycol lot/water/impurity and PVP sensitivity, and NaOH/hydrazine treatment, are explicit. The methods distinguish the Figure 2 hydrogen reduction from optimized Figure 3. Figure S21 directly shows the NiAg EO-rate rise followed by substantial decline through about 20 h. The program correctly avoids sustained-rate, stationary-endpoint or lifetime claims from that plot.
- **Working-state scope:** the preparation and proximity controls strengthen association of Ni with Ag while leaving the working atomic distribution and transfer to Cs/Re-promoted Ag unresolved. The new matched processing control is correctly treated as required methodology with prior art, not the proposed originality.
- **Optional isotope branch:** independently checked the algebra `D/A = (m+y)/(x²+m)` and `D/q = (m+y)/(x²−y)`, the three numerical rows and the conditional 0.0619 probability-bound illustration in the [isotope review](ag-isotope-reversibility-prior-art.md). Net 16O2 formation sign, ordinary readsorption, return-weighted labeling, random-pair alternatives and the distinction between gas return and local recycling remain explicit. The 2024/2026 main/SI evidence does not transfer the propylene bound or rate control to ethylene or Ni/Cs/Re. The branch remains conditional and has a clear stop if population contrast or useful discrimination cannot be established.

Primary sources checked: [Iyer original](../../literature/papers/iyer2021-interdependencies-among-ethylene-oxidation-and/original.pdf), [Jalil original SI](../../literature/papers/jalil2025-supplementary-information-for-nickel-promotes/original.pdf), and the source-linked isotope analysis. This reviewer verified the isotope derivation and its source qualifications; it did not remeasure the published isotope signals or establish their statistical confidence.

## Ag: value and remaining experimental limits

The [program](../programs/ag-selective-oxygen-use.md) correctly starts from the old Ni/Cs/Re aging result and known chloride-policy competitors. It separates common-condition causal comparisons from separately chosen operating policies, requires independent preparation, and measures integrated useful EO rather than a favorable selectivity endpoint alone. Ordinary continuation/sham recovery, carryover, finite persistence and the limits of structure correlations are explicit. No unsupported industrial upset frequency or remote lifetime crossover is used to justify investment.

No mechanistic uniqueness follows from collapsed curves, net EO cofeeds or a failed transferred model. The proposed additional contribution must exceed a calibrated chlorine/product baseline and predict a material or operating choice under a withheld condition. The practical confidence remains low. These requirements prevent relabeling ordinary Ni promotion, model fitting or another aging curve as a substantial program.

## Residual limits and scope of the pass

The review does not certify that either scientific hypothesis is true or that experiments will improve a process. Facilities, achievable precision, material reproducibility, working-state identities, complete cycle balances and economic values remain to be established. Missing sources remain explicit. They do not warrant inventing results, numerical success probabilities or new directions.

Historical source-access statements inspected in the polymer and Ag review files have dated superseding notices. Current active descriptions use the uploaded sources. A preserved historical statement is not itself a current missing-source request. The shared source inventory and literature-note maintenance remain the coordinating agent's and sole literature worker's responsibility.
