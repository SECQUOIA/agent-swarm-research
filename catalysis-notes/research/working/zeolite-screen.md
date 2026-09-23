# Zeolite program screen: can irreversible dealumination be interrupted before commitment?

Working research assessment, 2026-09-15. This is a proposal, not an experimental finding. The principal recommendation is a bounded falsification study before committing to a catalyst-development campaign. Independent review has narrowed the first question to assay effects on subsequent aging; see [developed program](../programs/zeolite-durability-and-measurement.md) and [review](../reviews/aging-independent-review.md).

## Recommendation

**2026-09-16 update:** first resolve whether inserting the recovery-capable assay changes subsequent H-CHA damage or useful function. Compare complete assay, thermal/water sham without NH3, and uninterrupted histories; verify residual ligand removal and predict a held-out assay spacing only after a meaningful contrast appears. The [current program](../programs/zeolite-durability-and-measurement.md) contains the operative design and stopping criteria. The recovery-window question below is a conditional application branch, not evidence that such a window exists. The [post-upload audit](../reviews/post-upload-cha-styrene-audit.md) updates the prior-art boundaries.

If that first question justifies the branch, test whether short, controlled recovery intervals can return partly hydrolyzed framework Al to catalytically useful states **before it becomes irrecoverable**, at fixed cumulative steam exposure, temperature history, and regeneration duty. The useful advance would be a measured time window and a predictive criterion for preserving catalytic function during regeneration. Neither Al reinsertion nor ammonia protection is itself new.

Begin with H-CHA because its relatively simple crystallographic environment and existing quantitative dealumination kinetics make a causal test feasible. If a useful window survives rigorous controls, transfer to MFI in a cyclic acid-catalysis application. Cu-CHA SCR is a later extension because Cu redistribution, ammonia chemistry, and N2O add several independent state variables. Do not promise an exhaust intervention that requires removing water continuously from engine exhaust.

The decisive question is narrower than the repository's general two-timescale durability card: **does exposure segmentation change irreversible loss because a reversible Al population relaxes between damaging events, and can that effect improve lifetime productivity without an offsetting regeneration penalty?** A negative result can bound the schedule benefit under the tested conditions. It cannot alone distinguish fast equilibration, an ineffective recovery step, offsetting damage, or an assay that removes the contrast; it does not by itself establish a commitment time.

## Why this opportunity survives initial screening

### Established evidence

1. In isolated-Al H-CHA, Class-Martínez et al. measured dealumination with an apparent Al dependence slightly above second order, inconsistent with a simple first-order hydrolysis description in the studied regime. They interpret the data through reversible hydrolysis followed by non-mean-field encounter/agglomeration of Al-derived species. This is strong motivation for a possible separation of timescales; it is not a measurement of a recoverable intermediate's lifetime. [[martinez2026-consequences-of-non-mean-field]] p.2-3, p.6-10. DOI: [10.1016/j.jcat.2026.116848](https://doi.org/10.1016/j.jcat.2026.116848).
2. The same study already uses repeated hydrothermal exposures, cooling, NH3 titration, wet purging, and reheating. It explicitly counts both framework Al and framework-associated sites that recover under the assay. Its data therefore concern loss after a recovery-capable measurement, not the instantaneous population of unperturbed framework Al under steam. Merely repeating this protocol with another steam duration would not establish the proposed advance. [[martinez2026-consequences-of-non-mean-field]] p.4-5.
3. Al coordination and acidity are not interchangeable. Penta-coordinate Al can carry Brønsted acidity, and water can reveal or create acidic ensembles from initially NMR-invisible Al. A larger tetrahedral-Al signal or NH3 uptake does not alone prove Si–O–Al reconnection. [[zheng2024-revealing-the-brnsted-acidic-nature]] p.4-10; [[wang2025-observation-of-water-induced-synergistic]] p.3-9.
4. Al distributions influence both activity and survival. In aged Cu-CHA, surviving Cu can be more active per remaining site even when the total useful inventory falls. Any proposed improvement must therefore be reported per original catalyst mass and reactor volume as well as per measured site. [[schmithorst2025-origins-of-the-hydrothermal-stability]] p.2-4, p.7-9.

### Contrary evidence and nearby prior art

- The now-read [Luo 2018 primary paper](../../literature/papers/luo2018-nh3-tpd-methodology-for-quantifying/original.pdf), pp.5–6, tests two Cu/SSZ-13 cores exposed to 700 °C for 2 h and 600 °C for 24 h in opposite orders. Both sequences contain intermediate NH3-TPD on the same cores; final TPD ratios and catalytic functions agree. This is a tested cumulative-aging null in a mild Cu-redistribution regime. It does not compare an inserted assay with sham-treated or uninterrupted isolated-Al H-CHA.
- [Ladshaw 2022](../../literature/papers/ladshaw2022-measurement-and-modeling-of-the/original.pdf), pp.8–10, predicts aged Cu-SSZ-13 storage transients with fixed adsorption kinetics and updated age-dependent site densities. Predicting generic aged NH3 storage is prior art. The proposed added value is consequential prediction across different assay schedules, beyond ordinary population-change models.
- The uploaded Wouters 1998/2001 and Agostini 2010 papers support the existing coordination/connectivity distinction and active role of hydration during cooling in Y zeolite. Nielsen 2015 supplies a model-dependent H-SSZ-13 kinetic alternative compared with experimental H-ZSM-5 data. These are controls and domain limits, not measured H-CHA recovery times; see the [source-located audit](../reviews/post-upload-cha-styrene-audit.md).
- A 2025 ZSM-5 study reports NH3 protection against steaming and partial Al reinsertion after low-temperature hydrothermal treatment. Those interventions and the broad reversible/irreversible distinction are prior art. The proposed contribution must be a **time-resolved causal and functional test**, not another claim that ammonia or water can recover acidity. [Steam-Induced Aluminum Speciation and Catalytic Enhancement in ZSM-5 Zeolites](https://www.mdpi.com/2073-4344/15/12/1130).
- Stockenhuber and Lercher showed in faujasites that acidity recovery after aqueous ammonium treatment can follow removal of charge-compensating extra-framework species without increasing framework Al. Their result directly motivates the structural and mass-balance controls below. It does not prove this explanation applies to gas-treated CHA. [Characterization and removal of extra lattice species in faujasites, 1995, lawful full text](https://ris.utwente.nl/ws/files/6515540/Stockenhuber95characterization.pdf).

Targeted searches found no direct demonstration combining exposure-order controls, recovery-time measurements, independent framework-connectivity evidence, and a regeneration-productivity test. This is provisional originality, not proof of literature completeness. The missing full texts and relevant supplementary material must be checked before a novelty claim is finalized.

## Hypothesis, alternatives, and confidence

**Proposed mechanistic hypothesis.** Steam produces a recoverable Al population, R. Some R returns to a useful framework-connected state, F, when the chemical potential or ligation changes; another fraction becomes operationally irrecoverable, D, through detachment, transport, association, or structural closure. A practical recovery interval can reduce the probability of entering D if applied before commitment.

Use `F <-> R -> D` as an intentionally coarse hypothesis. R need not be a single molecular species and D need not be bulk alumina. The more detailed Class-Martínez mechanism cannot be assumed from this notation. Start by determining whether a distinct recoverable population is needed at all; add molecular states only when observations constrain them.

**Strongest null.** Damage follows a memory-free law `dF/dt = -k(T,a_w) F^n`, with site heterogeneity and condition-dependent activity or visibility. Include multiple site classes with different stability as a competing null. Equal integrated steam dose alone does not distinguish these descriptions. Some heterogeneous models can produce order effects under multiple severities without a recoverable pool; positive order dependence is necessary evidence of hidden state under certain protocols, not sufficient proof of healing.

**Additional alternatives.** Recovery restores proton availability by moving EFAl counterions; restores pore accessibility; alters NMR visibility; changes strength of surviving sites; or simply reduces local steam/temperature peaks. All may change activity without reversing framework dealumination.

| Judgment | Current confidence | Basis and limit |
|---|---|---|
| Reversible Al coordination/hydrolysis exists | High within studied zeolites | Prior observations and explicit interpretation in the existing CHA work; microscopic populations vary with conditions. |
| A finite recovery window is long enough to exploit | Low to moderate | Sequential chemistry makes it plausible, but hydrolysis and commitment may equilibrate too quickly, and existing aging assays already include recovery. |
| A bounded experiment will be informative | High | Exposure histories and post-treatment can be controlled; disagreement between functional and structural recovery is itself consequential. |
| Molecular attribution to Al reattachment can be resolved | Moderate | NMR visibility, proton stoichiometry, and EFAl compensation require complementary measurements; a unique atomistic mechanism may remain unavailable. |
| Meaningful process improvement | Low until tested | Dry or cooled intervals consume time and utilities; gains must survive realistic coke burnoff and repeated cycles. |

## Experiment 1: detect a recovery window without an intervening titration

### Material and baseline

Use two existing isolated-Al H-CHA preparations near the compositions studied by Class-Martínez, initially avoiding Cu and added stabilizers. Characterize total Al/Si, residual Na, crystal size, micropore volume, XRD, and the initial acid inventory. A matched pair-rich sample is an optional second perturbation only after a signal exists; syntheses that change Al proximity can also change defects, residual ions, and water uptake.

Choose a steam condition that gives readily measured but incomplete irreversible loss; an initial bracket within 873–923 K and 10–30 kPa H2O follows the existing experimental envelope. These are screening conditions, not an asserted optimum. Use actual measured bed temperature and water response to select the shortest resolvable pulse; a nominal subminute pulse is meaningless if tubing or the bed takes minutes to exchange water.

First acquire unsegmented time courses on **separate sacrificial aliquots**, without NH3 or deliberate ambient hydration between exposures. This differs fundamentally from repeatedly titrating the same sample. It establishes the response of an unmeasured specimen and quantifies what the assay itself changes.

### Matched histories

At fixed temperature, compare histories with exactly the same wet-pressure level, cumulative wet duration, cumulative dry duration, total duration, flow, and terminal handling:

- One wet block followed by one dry block.
- One dry block followed by one wet block.
- Alternating wet/dry intervals, varying the number of intervals while retaining the same totals.
- A randomized ordering of the same interval types, useful for testing a fitted model on a history it has not seen.

For example, a study can compare a total of two hours wet and two hours dry delivered as single blocks versus multiple alternating blocks. The exact periods should be chosen after measuring the gas-response time and initial damage kinetics. Include a zero-steam dry-history control. Measure local temperature; compensate for evaporation-related cooling and hold total flow fixed. Record the delivered H2O waveform rather than treating the mass-flow command as the exposure.

At fixed wet conditions with genuinely inert dry intervals, a memory-free irreversible model predicts identical loss at equal wet time even if the Al-order is nonlinear. If dry conditions themselves change damage, calibrate that process separately. If variable temperature or pressure is introduced later, simulate all competing nulls on the measured waveforms before attributing order dependence to recovery.

Run both (i) identical terminal conditioning and (ii) separate aliquots preserved immediately at selected interval boundaries. Common conditioning allows a fair catalyst-use comparison but can erase the intermediate population; boundary aliquots reveal that limitation. Randomize reactor order and use independent preparations to separate a true protocol effect from batch or instrument drift.

### Recovery challenge

After selected wet exposures, apply a defined recovery treatment for increasing durations. Start with dry carrier at the same temperature, because it preserves the strongest equal-temperature control. If that does not recover function, use one separately motivated lower-temperature NH3/humidity challenge based on established recovery chemistry. An expensive suite of many healing recipes would obscure the central test.

Compare early and late intervention at the same cumulative wet/dry/thermal exposures. A shrinking recoverable fraction as prior steam duration increases, and a saturating recovery response to intervention duration, would support a commitment window. Failure of dry recovery does not falsify all hydrolysis reversibility; it does falsify the simplest practical version.

## Experiment 2: establish what actually recovered

Use three independent levels of evidence, on carefully matched aliquots:

1. **Working function:** a small-reactant acid-catalysis test under a common, quantified feed, performed before NH3 titration. For H-CHA, a validated alcohol-dehydration assay is feasible, but its product water may itself alter the state; track the earliest and stabilized rates and do not mistake equilibration during the assay for prior recovery. The MFI transfer stage enables differential dry n-hexane cracking, avoiding this particular complication.
2. **Acidity and accessibility:** common gas-phase NH3 titration with explicit accounting for the fact that the titration can heal or protonate sites. Record proton and framework/AlOH infrared signals before titration. The difference between first measurement and post-NH3 measurement is an output, not an error to hide. Avoid treating every NH3 molecule as proof of one intact framework Al.
3. **Structure and Al balance:** quantitative multinuclear NMR under specified hydration/dehydration, with 29Si–27Al connectivity where sensitivity allows, supported by 1H–27Al correlations and total Al mass balance. A tetrahedral 27Al resonance is inadequate evidence of reinsertion. Check for changes in counterions, EFAl populations, micropore access, and condensed/escaped Al. Use sealed transfers or reproducible hydration where possible; characterize its effect explicitly.

Only label recovery as framework reconnection if restored connectivity and function agree. If proton access recovers without increased framework connectivity, report useful acid regeneration by a different mechanism. If only NMR intensity changes, reject the functional-healing claim. If improved site-normalized activity masks fewer sites per initial catalyst mass, reject the durability improvement.

Do not require operando high-temperature multinuclear NMR to launch the program. Sacrificial boundary aliquots, in situ IR, controlled transfers, and catalyst-function tests can first establish whether an expensive structural campaign is justified. H2(18)O exchange is optional support; oxygen scrambling can occur without net Al reinsertion and cannot be the decisive evidence.

## Experiment 3: validate useful regeneration, conditional on the first gates

Transfer the successful schedule to one MFI catalyst used for methanol-to-hydrocarbon chemistry or a similarly relevant cyclic acid-catalysis process. Match initial coke inventory and chemistry, catalyst mass, bed shape, final residual carbon, and terminal conditioning. Compare against the best conventional regeneration at equal coke removal, with local temperature and water measured during combustion. Do not claim success from a lower maximum temperature or incomplete burnoff unless those are explicitly the process change being evaluated.

Report total useful product over the full reaction/regeneration cycle per initial catalyst mass and reactor volume, loss of accessible acid function per cycle, product distribution, carbon closure, regeneration duration, purge demand, and utility requirements. A retained acid count is not sufficient if selectivity worsens or the longer regeneration loses more productivity than improved durability gains.

The first target is scheduled regeneration, where dry intervals can plausibly be engineered. Continuous wet exhaust is a poor first application. A later Cu-CHA extension would require Cu inventory/speciation, redox half-cycle response, NH3 slip, and N2O as additional outcomes; changes to those observables cannot be assigned automatically to preserved framework Al.

## Stop/go gates and expected outcomes

**Gate 0 — assay audit.** Reproduce the unsegmented loss curve and demonstrate the magnitude of conditioning/titration effects. Stop mechanistic interpretation if the measurement perturbation is comparable to the claimed protocol benefit and cannot be separated.

**Gate 1 — a history effect beyond calibrated nulls.** Require an effect larger than combined batch and measurement uncertainty, reproducible across independent preparations, and predictable in a withheld schedule. An arbitrary significance threshold or tiny reproducible gain is insufficient. If the effect disappears after local-temperature/H2O correction or heterogeneous-site modeling, retain the negative result and do not proceed to material development.

**Gate 2 — a recoverable functional population.** Require genuine post-intervention catalytic function and an intervention-time response. A unique molecular assignment is desirable but not required for an operationally useful program; be explicit if framework reconnection remains unproved.

**Gate 3 — useful repeated regeneration.** Require repeat-cycle lifetime-productivity benefit at matched coke removal after charging the protocol for downtime and utility use. Reject a treatment needing an autoclave between each operating cycle unless a specific off-line refurbishment case justifies it. If improvement is only a small fresh-catalyst rate increase, stop.

Expected results are conditional:

- A positive result yields a recovery-window map, a minimal predictive damage/recovery model, and a credible scheduling intervention.
- No history effect bounds the schedule benefit within the tested periods and conditions. It does not by itself bound intermediate lifetime: negligible abundance, ineffective recovery, opposing dry damage, or an insensitive endpoint assay can also produce a null result. A lifetime bound requires independently constrained population/recovery kinetics.
- An assay-induced effect reveals a consequential normalization problem and helps reconcile apparently conflicting aging/acid-count studies, but by itself is a methods result rather than a practical catalyst advance.
- Functional recovery without framework restoration may still be valuable, but changes the claimed mechanism and requires its own durability test.

## Strongest alternative and rejected near-duplicates

The strongest practical alternative is **preventing damage through a demonstrably better material or milder regeneration**: lower-defect crystals, a stable topology, an appropriate Al distribution, or a lower-temperature coke-removal protocol. The proposed timing strategy must outperform that simple baseline on lifecycle productivity. If a cheap formulation already delivers the same survival, scheduling complexity is unjustified.

Several Cu-centered ideas were screened and deprioritized for novelty:

- Stable framework anchors combined with mobile Cu partners largely restate the existing Al-density, dynamic-pair, and survivor-site literature. [[krishna2023-influence-of-framework-al-density]] p.5-7, p.11-22; [[bjerregaard2025-influence-of-aluminium-distribution-on]] p.3-6; [[schmithorst2025-origins-of-the-hydrothermal-stability]] p.7-9.
- Mixing Cu-CHA with Cu-free H-CHA as a migration acceptor is explicitly demonstrated in both older interparticle-migration work and a recent high-water durability study. Varying contact distance alone is also prior art. [Lee et al., 2019](https://doi.org/10.1039/C8RE00281A); [Gao et al., 2026 online, 2027 volume](https://doi.org/10.1016/j.apcatb.2026.127245). The latter is currently assessed from publisher abstract/excerpts, not a retrieved full text.
- A generic water-tolerant Cu-CHA screen is too close to existing water-inhibition, NH3-inhibition, and Al-density studies without a specific new causal intervention. [[gronbeck2025-inhibition-of-nh3-scr-over]] p.3-6; [[deka2026-insights-into-the-mechanisms-of]] p.4-11.

## Historical literature requests sent to the parent

This list records the original 2026-09-15 handoff, not current availability. Luo's main article and the other sources explicitly reassessed above are now local and read; additional package status is maintained by the literature workflow. Preserve the original request scope without treating these lines as a current missing-source report.

All identified additions are routed to the single reusable literature agent; no KB maintenance was run by this researcher.

1. Luo et al., *NH3-TPD methodology for quantifying hydrothermal aging of Cu/SSZ-13 SCR catalysts*, 2018, [DOI 10.1016/j.ces.2018.06.015](https://doi.org/10.1016/j.ces.2018.06.015). Critical sequence-independent contrary evidence; the uploaded main article has now been assessed above.
2. *Steam-Induced Aluminum Speciation and Catalytic Enhancement in ZSM-5 Zeolites*, 2025, [DOI 10.3390/catal15121130](https://doi.org/10.3390/catal15121130), [open full text](https://www.mdpi.com/2073-4344/15/12/1130). Closest recovery/protection prior art.
3. Stockenhuber and Lercher, *Characterization and removal of extra lattice species in faujasites*, 1995, [open full text](https://ris.utwente.nl/ws/files/6515540/Stockenhuber95characterization.pdf). Acid recovery without framework reinsertion; DOI requires authoritative verification because scan identifiers are inconsistent.
4. Lee et al., *Inter-particle migration of Cu ions in physically mixed Cu-SSZ-13 and H-SSZ-13 treated by hydrothermal aging*, 2019, [DOI 10.1039/C8RE00281A](https://doi.org/10.1039/C8RE00281A). Novelty boundary for Cu-acceptor alternative; full text still needed here.
5. Gao et al., *Stabilizing Cu-SSZ-13 SCR catalysts under high-water-vapor conditions: Insights into Cu migration and Cu–Al interactions*, [DOI 10.1016/j.apcatb.2026.127245](https://doi.org/10.1016/j.apcatb.2026.127245). Published online 2026, assigned 2027 volume; recent practical comparator and novelty boundary; full text still needed here.
6. Class-Martínez et al., AIChE 2025, *Influences of Al Density and Proximity and Framework Topology on the Dealumination Kinetics of Proton-Form Zeolites*, [public conference abstract](https://proceedings.aiche.org/conferences/aiche-annual-meeting/2025/proceeding/paper/influences-al-density-and). Scope-overlap evidence; distinguish the conference abstract from the existing 2026 journal article.

## Open questions for independent review

1. The focal 2026 SI has now been reviewed and does not report the proposed repeated-assay/sham/uninterrupted comparison. Wider novelty remains provisional; the uploaded prior art does not establish a usable recovery window.
2. What is the fastest credible independently measured Al-recovery time, and does it exceed water-exchange/temperature-control times in available equipment?
3. Which combinations of measured function, connectivity, and proton balance can distinguish reattachment from counterion redistribution at realistic sensitivity?
4. Can a conventional mild-regeneration schedule achieve the same benefit with less downtime and control complexity?
5. Does the apparent Al dependence itself survive measurements that omit the intervening NH3/water recovery assay? This is a consequential methodological uncertainty, not a presumption that the existing result is wrong.
