# When would carbonate protection beat recovery or makeup?

2026-09-16. Decision calculation for the [cyclic-oxide reserve](../working/program-development/cyclic-oxides.md) and its [single timing intervention](../working/program-development/cyclic-oxide-causal-intervention.md). All intervention results remain unmeasured. This closes the practical question raised by the [latest portfolio review](../reviews/program-development-portfolio-review.md#reconsideration-after-the-concrete-first-tests-and-comparator-audits-2026-09-16); it does not introduce a new material search.

**Decision:** retain a bounded program on preventing loss that subsequent regeneration cannot economically restore. Give priority to establishing whether the proposed steam purge causes consequential damage and whether concurrent CO2 prevents it at acceptable gas and time burden. Demonstrating less Li in a trap is insufficient. The current evidence supports this comparison, but does not establish a useful protective dose, a Li-loss rate, inexpensive promoter replacement, or superiority over dry purging.

## What the primary studies actually supply

[Brody et al. 2022](https://doi.org/10.1021/acs.energyfuels.2c01293), [open manuscript](https://www.osti.gov/servlets/purl/2001472), Methods 2.2–2.3, Table 1 and Section 3.3, supplies the following measured and modeled scales. Its main manuscript was read directly; the supporting information was not independently read for this calculation.

| Quantity | Supported value and boundary |
|---|---|
| Experimental material | 300 g of methods-based nominal 10 wt% Li2CO3/La0.8Sr0.2FeO3, supported by alumina grit in an alumina tube. The conclusion says 20 wt%; confirm the actual loading convention before inventory work. |
| First 1,000 elapsed hours | 700 °C, 300 h−1 GHSV; 1 minute of 81.6% ethane/Ar, 5 minutes Ar, 5 minutes 20% O2/Ar, 5 minutes Ar. Same GHSV in reducing and purge steps. Thus 16 minutes/cycle and 62.5 scheduled hours of ethane feed in 1,000 elapsed hours. |
| Useful carbon yield | C2+ yield averages 53.2% in hours 0–300 and 47.24% in hours 600–1,000. C2+ includes ethylene and C3+ products; it is not ethylene yield alone. |
| Oxygen scale used in model | About 0.188 wt% available oxygen at the later optimum, 735 °C and 640 h−1. Water and oxygen availability were inferred from a hydrogen balance, not measured as a complete coating/oxide balance. |
| Actual steam evidence | None from the longevity experiment. The process model represents two steam purges by heat exchange units, with steam volumetric flow matched to total ODH gas feed across recycle ratios. Its 350 °C steam cools 735 °C solids. |
| Process heat inference | Preheating reducing/oxidizing gases to 350 °C allows modeled autothermal operation over a stated recycle range. RStoic yields and surrogate oxide thermochemistry do not predict catalyst changes caused by steam or CO2. |

[Gao et al. 2020](https://doi.org/10.1126/sciadv.aaz9339), [open article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7182410/), reports a molten coating, about 0.42 wt% oxygen use in the first six minutes at 700 °C, and inhibition by CO2 cofeed on the actual coated LSF (Fig. 4D: 10% CO2, 15% ethane, Ar balance). The article describes reversible inhibition upon removing CO2. The separate 25%-to-below-5% conversion example in Fig. 4E concerns ethane/O2 on molten Li2CO3 at 730 °C, not the LSF chemical-loop experiment. Consequently CO2 remaining after protection can cost oxygen delivery or extra washout time even if it preserves the coating. Neither study establishes a steam-tolerant operating window or periodic promoter makeup performance.

The strongest **demonstrated** comparator is therefore the original dry Ar protocol. Steam is a **modeled process option**. Recycled CO2, shorter purges and periodic promoter recovery/makeup are sensible **proposed comparisons**, not established alternatives with measured benefits on this aged material. The main manuscripts do not support claiming otherwise. Cheap Ar operation at scale is also unestablished.

## Output gives a first threshold without prices

Let `q_i` be desired product per cycle averaged over a stated block, including its aging trajectory; `τ` the common base cycle duration; and `h_i` extra time per cycle averaged over that block. Include periodic regeneration, cooling, coating restoration, reheating and washout in `h_i`. For equal initial catalyst mass, product rate is

`J_i = q_i / (τ + h_i)`.

Prevention P beats a recovery/makeup policy R in useful output when

`h_P < (q_P/q_R)(τ + h_R) − τ`.

Use measured block-integrated output, not a fresh endpoint or a fitted Li-loss-to-selectivity relation. For unequal feed or catalyst inventories, compare actual product per initial catalyst mass and elapsed time and separately report feed efficiency. Ethylene and C2+ objectives require separate accounting.

**A source-backed benchmark:** suppose, only for this calculation, a treatment completely restores Brody's later C2+ yield of 47.24% to the early 53.2%, without changing the one-minute feed pulse, and compare against continued aged operation. Then

`q_P/q_R = 0.532/0.4724 = 1.1262`,

`h_P < 16 × (1.1262 − 1) = 2.02 minutes/cycle`.

Thus a five-minute extra treatment every cycle would require a 31.25% yield increase to break even on time alone; complete restoration of this particular documented loss gives only 12.62%. A ten-minute extra treatment requires 62.5%. A treatment replacing an existing purge might add no nominal time, but any longer CO2 washout counts. A five-minute treatment every N cycles adds `5/N` minutes/cycle before other burdens, so persistence matters directly.

This is a generous upper allowance for restoring the specified Ar-aged state, not a measured recovery and not the headroom for the untested steam case. A policy that prevents only part of the loss gets less allowance. The loss from steam could be larger, smaller or absent. Nor does this endpoint calculation give the lifetime benefit of prevention from startup; that requires integrating both output histories.

## The protective-gas burden can be large

The diagnostic 10% steam/5% CO2/Ar has `p(H2O)/p(CO2)=2`. Maintaining that ratio in a binary steam/CO2 purge requires 33.3% CO2. This is a composition calculation, **not** a protective-dose prediction. Equilibrium direction in a related melt does not specify acceptable loss in this coating over five minutes.

For an explicitly hypothetical substitution into the measured 16-minute cycle, retain its total molar purge flow and one-minute 81.6% ethane feed. A five-minute post-oxidation purge containing mole fraction `z` of CO2 uses

`n_CO2 / n_ethane,fed = 5z/0.816`.

At `z=1/3`, that is 2.04 mol CO2/mol ethane fed for this one purge; applying it to both five-minute purges gives 4.08. At `z=0.05`, the respective values are 0.306 and 0.613. These are circulating gas doses, not necessarily fresh CO2 consumption. The steam/CO2 mixture displaces steam at fixed total flow. If instead the original steam dose is held fixed while preserving a 2:1 steam/CO2 ratio, total molar flow rises by 50%, requiring a new assessment of residence time, pressure drop and heating. The initial timing experiment addresses only the relatively oxidized post-oxidation purge.

Do not insert these batch timing ratios into the ASPEN model as its reported plant gas demand: the manuscript gives model flow rules and heat exchange blocks, not an independently verified mapping of all batch dwell times to a continuous solids process. They are transparent experimental comparison scales.

Recycling changes fresh CO2 demand but does not remove circulation, separation, compression or heating. Measure inlet/outlet CO2 over the complete sequence. Subtract blank holdup and reversible uptake to obtain net use; carbonate restored to the coating is distinct from gas circulated. For fixed total flow, the sensible heat increment includes `n_CO2 Δh_CO2 − n_displaced_steam Δh_steam`, plus changes in steam generation/recovery, gas cleanup, solid reheating and reaction heat. No sign or cost is assigned without a specified heat-recovery boundary. CO2 recycled from a product stream also requires a measured composition: residual H2, water or hydrocarbon is not an inert equivalence.

## Material and oxygen scales constrain what to measure

On the provisional convention of 10 wt% Li2CO3 in final catalyst, inventory is 1.353 mmol carbonate and 18.78 mg Li per gram of catalyst: about 30 g carbonate and 5.64 g Li in a 300 g bed. A 1% loss of that Li inventory is 188 μg/g catalyst; 0.1% is 18.8 μg/g. Brody's approximately 21% relative decrease of the fitted carbonate surface signal is **not** a 21% Li loss, and the paper does not supply an inventory loss rate. Surface chemistry, redistribution and instrumental overlap prevent that inference.

If `ℓ_i` is measured irreversible Li export per cycle and `f_i` the fraction of added Li that is retained usefully during an actual makeup operation, the stoichiometric Li2CO3 makeup requirement is at least

`m_makeup,i = ℓ_i × M(Li2CO3)/(2 M(Li)) / f_i`.

Here `ℓ_i` is mass of Li, giving carbonate mass in the same units. This relation cannot establish functional restoration: replacing Li may not restore coating coverage or reverse interfacial reaction. Measure that recovery and its downtime once a relevant loss exists. Wet impregnation and the source's synthesis calcination are not evidence that online makeup is simple. Report loss to grit/tube, trapped aerosol, and downstream condensable material separately; only the latter balances support escape from the apparatus, and none alone identifies LiOH vapor.

The model's 0.188 wt% available oxygen corresponds to 0.1175 mmol O atoms/g catalyst. If every atom served `C2H6 + O → C2H4 + H2O`, it could support 3.30 mg ethylene/g in that reduction. This is an oxygen-equivalent scale, not total measured ethylene capacity: nonoxidative dehydrogenation contributes ethylene and undesired reactions consume oxygen. Gao's 0.42 wt% over six minutes is 0.2625 mmol O/g at different conditions. Neither number establishes selective capacity of a steam-exposed coating or licenses mixing the optimum oxygen value with the earlier 16-minute cycle as a reported productivity.

Measure direct water, H2 and all carbon products with corrected switching response. Report retained desired output per cycle and per elapsed time; only call an oxygen amount selective when the resolved reaction balance supports that assignment. A steam treatment can also change stored OH/H2O, making water evolved in the following probe an unreliable standalone lattice-oxygen measure.

## One modest measurement that changes the decision

Complete the proposed equal-dose timing pair with its end-of-steam sister sample, common final carbonate endpoint, oxidation, CO2 washout and product probe. Keep its dry Ar reference. This identifies whether treatment order causes persistent functional or inventory differences; it does not determine a process operating dose.

If the contrast is resolved, advance **that same pair at one declared steam-rich purge composition**, chosen for a stated acceptable gas-handling boundary, and repeat actual ethane/oxidation cycles long enough to resolve cumulative output and Li inventory change. Do not preserve the diagnostic ratio automatically or launch a composition library. A failed low-dose comparison bounds that chosen option; it cannot disprove all carbonate protection. Conversely a useful effect only at large CO2 flow must carry that burden. Replace the existing post-oxidation purge so nominal time is equal; measure any additional washout needed to recover the reference response. The more reducing post-ethane purge remains a later dependency, not an unannounced second variable.

For a delayed-restoration arm that loses function, test one complete restoration using retained carbonate first. Only if material loss remains relevant, perform one measured carbonate replacement/recovery operation to estimate its restoration fraction, time and Li handling. Treat this as the recovery comparator for the same damaged state, not another catalyst formulation. If ordinary restoration already returns sustained output at lower burden, protection has no established advantage.

The block measurements supply a decision in physical units before an economic model:

- `J_P − J_R`: sustained desired-output difference after all treatment time.
- Li makeup, escaped Li, and recovered Li per unit desired product, with complete uncertainty and location budgets.
- Net fresh and circulating CO2/steam per unit desired product, additional washout and heat-recovery requirements.

If protection lowers desired output while adding gas and time without reducing consequential Li handling, stop the practical intervention. If it preserves output and reduces loss but consumes more gas, retain the tradeoff: the break-even allowed gas/heat burden must be supplied by a process assessment, not an invented price. If no functional decline or Li difference can be resolved at the exposure of interest, report an upper bound set by full-method uncertainty. Do not extrapolate a null five-minute exposure to lifetime stability or translate a detectable trace into a meaningful replacement burden.

## Final disposition and dependencies

This calculation **strengthens the decision structure but tempers the improvement claim**. The potential advance is a measured operating rule for a consequential steam-compatibility limit in this coating. Fereres 2018 already demonstrates delayed CO2 stopping further bulk-carbonate loss without restoration (printed p. 125, §3.6/Fig. 9); generic prevention versus recovery is also prior art. Existing carbonate chemistry and dual regeneration occupy the broader idea. Its added value must come from a consequential transition measured in this system and a fair prevention-versus-recovery comparison.

Confidence is moderate in the chemical plausibility of exposure-dependent recoverability, moderate in the informative value of a controlled timing/inventory test if the platform exists, and low to uncertain in a practical improvement. No local high-temperature cycling access, Li analytical recovery limit, process-relevant loss rate, protective dose or economical makeup route is established. These are actual experimental dependencies, not requests for guaranteed success before selecting research.

The reserve therefore merits one focused initial commitment, not a large parallel aging, isotope, coating and process-model campaign. Steam translation is the first intervention because it is concrete and avoids waiting hundreds of hours before testing the proposed sequence. Representative Ar-aged material remains a distinct route to explaining the published decline; pursue it next only when access and the initial evidence justify it. No further salt/material candidates are part of this finished proposal.

The [uploaded-literature audit](../reviews/current-uploads-cyclic-audit.md) removes the missing-dissertation dependency: Chapter 4.1 is now read and confirms related carbonate/LSF regeneration, including regeneration-generated water and core redox coupling. Fereres and other newly read originals narrow the originality claim without changing the arithmetic above. Brody's SI and Gao's supplement have not been independently audited here; Mohn/Wendt remains unread. The calculation supplies decision thresholds, not validation of a steam-loss rate or intervention benefit.
