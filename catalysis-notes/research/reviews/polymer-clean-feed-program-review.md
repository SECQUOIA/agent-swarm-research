# Independent review: clean-feed polymer ethenolysis

2026-09-16. Fresh review of [the developing program](../working/program-development/polymer-clean-feed.md) against [the revised standards](../standards.md). This review reports no new experimental results. It inspected original Science main-text and SI passages, visually checked the original Figure 4B, read the original Wang 2022 article, and checked the public Conk dissertation abstract and patent text. Access limits for the closest kinetic articles remain explicit below.

## Recommendation

**Support a bounded program-development campaign, but change its central claim and first decision rule.** Establish whether feed preparation or restart conditioning can reduce the fresh catalyst needed to process successive polymer charges. Treat selective loss of polymer initiation as one possible explanation, not the default thesis that a saturated/unsaturated comparison can identify.

The problem is important, and a useful improvement in this one system could meet the revised program standard. Existing competition does not disqualify it. However, the present binary feed comparison is insufficient to establish unequal loss of catalytic functions, and its negative branch is less informative than the proposal implies. Extensive site characterization should wait until there is an experimentally reproducible operational distinction worth explaining.

The strongest eventual contribution would be a measured relation between catalyst history, polymer chain populations, and the amount of fresh catalyst required for a specified throughput. A mechanism explaining that relation would strengthen the program. A successful unsaturated-feed rescue alone would remain a focused observation.

## What the original sources establish

**Reuse and Na makeup.** Science Figure 4B shows three charges and one fresh Na/alumina addition before charge 2. The original figure and caption support the program's corrected inventory accounting. They do not measure the independent rate or active population of either catalyst component. The statement in the original discussion that W activity remains nearly constant is the authors' interpretation of Na rescue, not a direct W-function measurement. The reuse plot reports accumulated product per W at a fixed endpoint; calling its decline an intrinsic rate-constant loss would overinterpret it. [[conk2024-polyolefin-waste-to-light-olefins]] p.4–5, Figure 4B.

**The feed is changing during the experiment.** Separate-component experiments show major molecular-weight changes even without catalyst, and Na changes the observed olefin population. The SI recovers and precipitates polymer for analysis; these are endpoint observations of a recovered fraction, not direct rates of creating reactive chains. The main-text Figure 2 caption says 10 bar ethylene whereas the associated text and SI procedures use 15 bar. Use the actual SI protocol for replication and preserve that source discrepancy. [[conk2024-polyolefin-waste-to-light-olefins]] p.2; [[conk2024-supporting-information-for-polyolefin-waste]] p.7–8.

**Initiation and regeneration are already explicit prior work.** The public [Conk dissertation abstract](https://escholarship.org/uc/item/7v07b7c8) describes Na/alumina-mediated transfer dehydrogenation, a Lewis acid–base hypothesis, modified catalysts, and DME regeneration. Its body remains embargoed until September 30, 2027. No detailed claim about its experiments or absent topics is justified from that abstract.

**The patent does not resolve the regeneration benchmark.** [WO2026011187A2](https://patents.google.com/patent/WO2026011187A2/en), paragraphs 0172–0177, describes air, air/H2, and air/DME treatments. The DME sequence includes substantial oxidative treatment; it is not an isolated DME intervention. Its Figure 21 caption names Na–Fe/alumina while adjacent procedures include unmodified Na/alumina. Original plotted yields and the exact material assignment were not recovered in this review. Do not use this disclosure as a quantified successful regeneration benchmark for the Science mixture. It does establish that generic regeneration with DME is not a new proposal.

**Substrate population and catalyst history were already coupled in earlier tandem ethenolysis.** Wang et al. explicitly distinguish monounsaturated and saturated PE; discuss ethylene inhibition; attribute an early transient partly to polymer dissolution and internal-olefin population; and report that adding a dehydrogenation catalyst lowers initial rate while extending activity. Their partially dehydrogenated high-molecular-weight PE gives poor conversion, with both sparse unsaturation and viscosity offered as explanations. These observations are directly relevant precedents against treating polymer unsaturation as a chemically isolated switch. [[wang2022-chemical-recycling-of-polyethylene-by]] p.2–4, DOI [10.1021/jacs.2c07781](https://doi.org/10.1021/jacs.2c07781).

## Specific identification problems and revisions

### 1. A positive bypass is useful but does not measure unequal function decay

The essential fresh/aged × saturated/unsaturated comparison changes several quantities at once: the number and position of C=C bonds, the supply of terminal olefins after the first ethenolysis events, adsorption competition, catalyst activation, and the subsequent molecular-weight and viscosity trajectories. Hydrogenating aliquots of one parent improves initial matching but cannot keep their reacting chain populations or contact identical. Those differences are consequences of the intervention and need measurement; they cannot all be removed by better feed preparation.

A simple illustrative rate expression makes the ambiguity visible:

`r_product = M_working × k × U_accessible / (K + U_accessible)`

Here `M_working` is an operational downstream capacity and `U_accessible` is a reactive olefin population. This is an identification example, not a proposed rate law for Na/W. Product output alone cannot separate changes in these factors. Increasing unsaturation can compensate for reduced downstream capacity in a nonsaturated regime, while a high-coverage assay can conceal changes relevant to low-coverage polymer entry. Product traces add information but do not make the inverse problem unique without independent perturbations.

The closest [Chen–Sadow–Peters model](https://pubs.acs.org/doi/abs/10.1021/acscatal.4c00465) already predicts substrate saturation and ethylene-dependent regimes for a homogeneous system; its publisher abstract was inspected. It provides a reason to test concentration dependence, not permission to transplant its rate law to a heterogeneous melt. The [Guironnet–Peters 2020 model](https://pubs.acs.org/doi/10.1021/acs.jpca.0c01363) is also prior art for connecting molecular-weight evolution to tandem kinetics. Its abstract was inspected; neither complete article was read here.

**Revision:** define the initial result as an aged-inventory feed response. Measure at least a low and a higher verified unsaturated-chain fraction at fixed total polymer mass and matched initial molecular-weight distribution, in addition to the saturated endpoint. Blends of the unsaturated parent and its hydrogenated counterpart offer a practical route if purification and chain architecture are validated. Report C=C location and distribution as far as the characterization supports them. Bulk olefin percentage alone is insufficient: one C=C on each chain and several C=C bonds on a minority of chains are different substrates. This response curve still does not assign a Na site or uniquely measure initiation; it determines whether bypass effectiveness depends strongly on olefin supply.

### 2. Conditioning controls are asymmetric in what they can establish

The proposal correctly identifies alkene-induced metathesis activation. This is a concrete issue for the actual catalyst lineage: Conk used the W/silica preparation developed by Howell, Li and Bell. Their [2016 primary abstract](https://escholarship.org/uc/item/6pt130c2) reports activation transients under propene and pretreatment-dependent activity. The full article download was unsuccessful in this review, so no detailed activation mechanism is adopted here.

A positive olefin-conditioning effect on subsequent saturated PE demonstrates a useful history effect. It does not establish that W alone changed, or exclude simultaneous initiation loss. A negative effect after conditioning and purging does not exclude activation that requires continuing olefin exposure, rapidly decays, or depends on long-chain adsorbates. Comparing a prolonged molecular assay with a fresh polymer restart can therefore create a misleading assurance that W capacity is intact.

**Revision:** record conditioning dose, time, purge duration, retained carbon, and both early and later response. Where practical, test the persistence of the effect over a short and longer delay using separate specimens. Keep the immediate spent-state assay and the conditioned assay separate. Do not expand the conditioning matrix until the first intervention produces a reproducible effect. Phrase unsuccessful conditioning as a negative result for that protocol.

### 3. Failed unsaturated rescue cannot reject initiation loss

An aged mixture may lose initiating and downstream functions together. Unsaturated PE can also inhibit or be poorly contacted, even if it converts well with fresh catalyst. Failure on both feeds therefore cannot distinguish common loss from two simultaneous losses. The proposal's statement that the campaign can rule out selective initiation failure needs narrower language.

**Revision:** a sufficiently precise negative result can reject the practical claim that the tested unsaturation treatment preserves useful output under those conditions. It can also show that loss of initiation alone is insufficient to explain the data if the downstream-function assumptions are independently supported. It cannot show that initiation is unchanged. Preserve this distinction in the stopping rule rather than adding more assays to force a unique site assignment.

### 4. Fresh-Na rescue needs a dose response before mechanistic interpretation

The published intervention adds as much Na/alumina as was present initially. It alters activity, adsorption capacity, solid inventory, contact, and the Na:W ratio. An added-support control is necessary but does not reproduce the surface chemistry or rheology of fresh Na/alumina. Restored endpoint yield does not imply restoration of the original initiating function.

**Revision:** after confirming the decline, compare no makeup, a smaller makeup dose, and the published full dose, while retaining the support control. Record rate trajectories and incomplete polymer fractions. The useful target is the minimum fresh Na material needed for a defined accepted output and cycle time, not proof that a full-dose rescue restores every function. This also supplies a much stronger practical comparator for any later restoration strategy.

### 5. Molecular probes and residual polymer need explicit analytical limits

Isomerization, initiation and metathesis assays are not automatically specific because each component has several functions. Small probes may reach sites unavailable to polymer; conversely, alkene probes may create active sites. Steady unsaturation is the difference between formation and consumption, so a low NMR signal is not a low formation rate. SEC and NMR on only soluble or precipitated fractions can miss the material whose access is most impaired.

**Revision:** validate probe selectivity on the separate components and supports; report earliest resolvable and conditioned responses separately; recover and account for soluble, insoluble, catalyst-bound and volatile carbon. State unsaturation detection limits on a chain-number basis where possible. Do not interpret an undetected change as unchanged initiation. For the first campaign, these are measurement limits to document, not reasons to demand every possible analytical instrument.

## The smallest informative campaign

The program should answer an operational causal question before attempting unique chemical attribution: **Can a defined feed or restart intervention preserve useful conversion with less fresh catalyst than the published Na makeup strategy?**

1. **Confirm what deteriorates.** Reproduce the clean-feed decline and fresh-Na rescue with time-resolved products, recovered polymer and cycle timing. Include an interrupted fresh control and a closed inert restart if existing hardware allows a valid matched comparison. Establish whether the apparent loss is an induction delay, lower sustained rate, or an earlier plateau. If only endpoint yields reproduce, mechanistic inversion remains premature.
2. **Measure a small feed-response surface.** Cross fresh and identically aged mixtures with saturated PE and two verified unsaturated-chain fractions, using the same parent distribution and matched workup. Observe early evolution as well as total output. Pair this with the small fresh-Na dose response. Independent specimens avoid sequential assay-induced changes. A modest number of conditions with independent repeats is more informative than a large characterization campaign.
3. **Test one explanation suggested by the response.** If olefin supply produces a clear aged-inventory advantage, use one controlled conditioning intervention to ask whether some benefit carries over to saturated feed. If the advantage appears only after large molecular-weight changes, prioritize contact and residual-chain observations. Do not execute all chemical-state and transport hypotheses in parallel without a discriminating observation.
4. **Validate one consequential prediction.** Choose a withheld catalyst history or polymer chain-length distribution and prospectively predict the makeup dose or cycle time needed for an accepted output. A useful operational predictor is sufficient for this stage. Failure should be reported without fitting a new deactivation law to the validation trace.

This campaign can yield an original, bounded map of which retained inventories remain useful for which feed states. It does not need to claim a unique elementary mechanism. A positive carryover conditioning result or reduced makeup demand would justify mechanistic expansion. Mere reproduction of the original rescue would not.

## Practical value and program depth

The program correctly accounts for total fresh solids and complete cycle time. Keep separate Na- and W-material demands: reducing a cheap support-rich component while worsening ethylene recycle, reactor productivity, or regeneration downtime is not automatically useful. Polymer-derived carbon accounting matters because much of the product carbon comes from the ethylene cofeed. The original Wang article's preliminary LCA identifies ethylene supply as an important contribution under its assumed process; it does not establish an environmental benefit for the proposed Na/W intervention. [[wang2022-chemical-recycling-of-polyethylene-by]] p.4–5.

There is no need to prove that upstream unsaturation is an economical pretreatment before using it diagnostically. There is also no basis yet to present it as the preferred practical solution. If diagnostics identify a reversible loss, the more valuable result may be preserving the useful working state or reducing fresh makeup under ordinary saturated feed. The existing DME disclosure must remain in that comparison.

Under the revised standards, this is a **credible candidate for substantial development with a bounded first stage**, not a demonstrated strong program ready for unrestricted investment. Its merit comes from the important resource-use question and a plausible experimental route to useful knowledge. Its uncertainty comes from mechanism identification, measurement feasibility, and overlap with inaccessible dissertation details. It should compete with alternatives on expected scientific and practical value; it should neither be dismissed because another group is active nor promoted merely because a binary bypass experiment is possible.

| Judgment | Fresh assessment |
|---|---|
| Selective initiation-loss hypothesis | Plausible, weakly supported. Na rescue supplies motivation but not functional localization. |
| Ability of revised experiments to give useful operational knowledge | Moderate, provided matched probes, time courses and carbon recovery are feasible. This is stronger than confidence in unique molecular attribution. |
| Meaningful practical improvement | Uncertain. A lower fresh-material demand at comparable complete-cycle output is a credible target; no present evidence establishes the size or net benefit. |
| Original program depth | Conditional. A validated catalyst-history/feed-response relation plus an intervention has depth. A single rescue or a generic model fitted to endpoint yields does not. |

## Source handoff and unresolved material

No literature packages or shared KB summaries were edited. The following were sent to the root for its sole literature agent:

1. **Howell, Li and Bell (2016), Propene Metathesis over Supported Tungsten Oxide Catalysts: A Study of Active Site Formation.** DOI [10.1021/acscatal.6b01842](https://doi.org/10.1021/acscatal.6b01842); [repository landing page](https://escholarship.org/uc/item/6pt130c2). Directly relevant W-preparation and activation precedent. The public primary abstract was inspected; attempted PDF retrieval yielded no usable artifact. The repository advertises an open PDF.
2. **Ziqiu Chen, Modeling Cross Scales in Polymer Upcycling.** [Illinois repository item](https://www.ideals.illinois.edu/items/129200), [advertised PDF](https://www.ideals.illinois.edu/items/129200/bitstreams/431101/data.pdf). Chapter 6 contains the IE microkinetics and may provide lawful full text for the closest model. Retrieval returned HTTP 403. Search results exposing its chapter heading are not a substitute for reading the chapter.
3. **Mougel et al. (2016), Low Temperature Activation of Supported Metathesis Catalysts by Organosilicon Reducing Agents.** [Open primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC4999968/). Direct precedent for W/silica activation, relevant to any proposal that generic preactivation is original. Abstract and introduction were inspected; full quantitative audit was not performed here. Sent for bibliographic verification and intake, not used as a quantitative premise in this review.

Previously queued or existing unresolved works remain: Chen–Sadow–Peters 2024 ([10.1021/acscatal.4c00465](https://doi.org/10.1021/acscatal.4c00465)) and Guironnet–Peters 2020 ([10.1021/acs.jpca.0c01363](https://doi.org/10.1021/acs.jpca.0c01363)), whose abstracts but not bodies were read here; the embargoed Conk dissertation body; and original patent Figure 21 with unambiguous material identity. The main recommendation does not depend on claiming to know their inaccessible results. Their unresolved scope limits mechanistic and novelty conclusions.
