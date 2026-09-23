# Does the measurement change zeolite durability?

## Decision and research question

**Priority: a conditional protocol-validation pilot. Expand only for a consequential predictive result, with an application branch conditional on that evidence.** Investigate whether inserting a recovery-capable acid-site measurement changes subsequent hydrothermal aging and useful catalytic function. Only then test whether a simpler intervention can preserve that function during regeneration.

This is an experimental research proposal, updated 2026-09-16 after [independent review](../reviews/aging-independent-review.md) and the [post-upload evidence audit](../reviews/post-upload-cha-styrene-audit.md). No new catalyst performance is established. Independent inspection of the closest 2026 study's supporting information found no comparison of repeated assays with uninterrupted aging or an NH3-free sham. This clears the specific SI gate; wider priority remains provisional. The initial [opportunity screen](../working/zeolite-screen.md) contains the broader literature context; this document defines the narrower experiment to prioritize.

Prior art on NH3 protection during steaming, post-steaming recovery, and testing-induced state changes lowers the value of merely finding a positive assay contrast. The intended advance is a predictive relationship between exposure history, recoverable acid capacity, and working catalytic function. A method that predicts catalyst lifetime under a different measurement schedule could be useful even if no inexpensive regeneration improvement exists. A familiar immediate increase in NH3 uptake would be insufficient.

## Why the question matters

Durability studies often compare retained acidity after successive aging intervals. Such a curve is portable to a reactor only if the interruptions and measurements do not materially alter subsequent damage, or if their effects are included in the prediction. Misjudging this transfer can select the wrong catalyst or regeneration schedule.

The concrete starting point is isolated-Al H-CHA. Class-Martínez et al. explicitly use repeated steam exposure followed by NH3/water titration and thermal treatment. Their reported Al inventory includes framework-associated species recoverable under that assay. They interpret the loss kinetics using hydrolysis and association/transport of Al species. These are statements of the published method and interpretation, not evidence of an error. [[martinez2026-consequences-of-non-mean-field]] p.4-5, p.7-9; [journal DOI](https://doi.org/10.1016/j.jcat.2026.116848). We checked the method and recovery statement against the original PDF.

Gounder's site-counting, Al-siting, and zeolite-kinetics expertise fits the first campaign directly. Iglesia's transient kinetics and reaction-engineering methods support the state-change analysis and the later regeneration comparison. Cross-topology transfer is a separate research question, not assumed from CHA results.

## Established evidence and unsettled claims

| Statement | Status and limit |
|---|---|
| The published CHA series inserts chemical and thermal treatments between steam intervals | Established from the primary paper, p.4. |
| Its terminal assay can count recoverable framework-associated sites | Established interpretation explicitly stated by the authors, p.5. |
| Inserting that assay changes the subsequent aging curve compared with unassayed exposure | Proposed hypothesis; the main text and SI do not report the proposed causal comparison. |
| NH3 can change Al coordination or restore acid response | Established prior art; not the proposed novelty. Molecular reconnection and acid response are distinct. |
| A dry interval can exploit a delay before irreversible loss | Speculative. Fast hydrolysis equilibration may make it ineffective. |
| A useful schedule improves commercial catalyst lifetime | Unvalidated; requires a separate reaction/regeneration test and process accounting. |

The [SI review](../reviews/aging-independent-review.md) credits the existing endpoint validation: S14 discusses removal of Lewis-bound NH3 and comparisons with other acid-counting methods. Selective counting does not establish that the complete assay leaves subsequent aging unchanged. Also, S21 calculates extra-framework Al by subtracting NH3-derived framework Al from ICP total Al; these EFAl plots are not an independent structural inventory.

Broader history effects are also prior art: the [2017 Cu-zeolite study](https://doi.org/10.1039/C6RE00198J), section 3.6, reports further Cu changes when aged specimens encounter SCR reactants. This is a different material and intervention from repeated H-CHA assays, but rules out claiming that post-aging testing can change a catalyst as a general new discovery.

Madeo et al. report NH3 protection during steaming and separate post-steaming aqueous recovery ([2025 primary paper](https://doi.org/10.3390/catal15121130), pp.6–9, 17, 25). These results further narrow the opportunity: the question must concern carryover into future damage after the intervening treatment, with useful prediction beyond familiar recovery chemistry.

The uploaded primary texts strengthen the prior-art controls. Wouters reports partially hydrolyzed framework-related Al in Y zeolite and ammonia-induced changes from octahedral to tetrahedral coordination; that signal change is not proof of restored framework bonds ([1998 original](../../literature/papers/wouters1998-reversible-tetrahedraloctahedral-framework-aluminum-transformation/original.pdf), p.7; [2001 original](../../literature/papers/wouters2001-steaming-of-zeolite-y-formation/original.pdf), p.5). Agostini observes substantial Al migration during water readsorption on cooling in NH4-Y ([original](../../literature/papers/agostini2010-in-situ-xas-and-xrpd/original.pdf), p.11). Thus the thermal/water sham is chemically consequential. Neither study establishes the same mechanism in H-CHA.

Luo's Cu/SSZ-13 study provides a tested cumulative-aging null: two cores exposed to 700 °C for 2 h and 600 °C for 24 h in opposite orders retain similar final NH3-TPD ratios and catalytic activity. **Both sequences include an intermediate NH3-TPD on the same cores** ([original](../../literature/papers/luo2018-nh3-tpd-methodology-for-quantifying/original.pdf), pp.5–6, Section 3.4.2 and Figure 7). This is evidence against a general claim that aging order must matter; it does not compare inserted assays with uninterrupted or sham-treated aging. Its mild Cu-redistribution regime also differs from isolated-Al H-CHA dealumination.

Nielsen's 2015 H-SSZ-13 microkinetic calculation predicts increasing control by the final hydrolysis at high temperature, while its improved experimental comparison is with H-ZSM-5 ([original](../../literature/papers/nielsen2015-kinetics-of-zeolite-dealumination-insights/original.pdf), p.8). Read together with the [2019 cooperative-water calculation](../../literature/papers/nielsen2019-collective-action-of-water-molecules/paper.md), these studies require attention to local water loading and model domain. They do not measure a usable H-CHA recovery window or establish one universal rate-controlling hydrolysis step.

The now-retrieved [Stockenhuber and Lercher study](https://doi.org/10.1016/0927-6513(94)00056-2) provides a direct counterexample to equating recovered acidity with framework repair. Aqueous ammonium treatment increased the ammonia capacity of dealuminated FAU while the lattice-Al concentration inferred from 29Si NMR stayed nearly unchanged. The authors attribute the change to removal/replacement of extra-lattice charge-compensating species, and distinguish gas-phase ammonia adsorption from aqueous exchange (sections 4.1–4.2 and conclusions). This is a different topology and intervention; it strengthens the required structural distinction without predicting the H-CHA assay effect. [[stockenhuber1995-characterization-and-removal-of-extra]]

## Competing explanations

**H1: the inserted assay changes the population that survives the next steam interval.** Ligation, hydration, or heating restores, rearranges, or removes vulnerable ensembles, changing subsequent loss or useful function. A beneficial effect is possible; accelerated damage is also possible.

**H0: the assay changes only what is visible at measurement.** Under a common final treatment, serial and sacrificial specimens have the same recoverable capacity and pre-assay catalytic function within uncertainty. Agreement supports transferability between the tested histories; it does not validate every extrapolation of a fitted kinetic law.

**H2: handling or temperature/water history causes the difference.** The complete assay and an NH3-free sham behave similarly, whereas both differ from uninterrupted aging. Calling this an ammonia effect would be incorrect.

**H3: the final response changes without preserving the original framework population.** EFAl counterions, accessibility, acid strength, or NMR response changes explain recovery. The result may still be functional regeneration, but does not demonstrate Al reinsertion.

**H4: the apparent history effect is an exposure or sampling artifact.** Unequal bed temperature, water transients, particle gradients, batch variability, or state changes during the functional test account for it.

## First campaign: smallest decisive comparison

### Commission the measurement before fixing sample counts

Start with one well-characterized isolated-Al H-CHA preparation near the published composition range. Use independent packed beds drawn from that batch. Establish endpoint repeatability and a wet exposure that produces clearly measurable, incomplete loss. The published 823–973 K and 3–30 kPa steam range supplies an experimental envelope, not a required optimum. Select one constant-temperature condition for the first comparison.

Measure the loaded-system water step response, bed temperature, flow, and transfer/conditioning effects. Determine how long an exposure is actually constant. Before expanding the matrix, verify that a final acid-capacity difference can be resolved against reactor-to-reactor variation. Repeat the decisive comparison using an independently prepared catalyst batch.

### Histories to compare

Resolve and document the reference timeline first: SI Scheme S3 (S16) labels air treatments at 773 K, whereas the main text p.4 specifies an 873 K pre-aging dehydration hold. Define the chosen temperature and match it in the sham; do not claim exact replication until this discrepancy is clarified. It is a documentation issue, not evidence that the reported kinetics are wrong.

Use a fixed number of identical damaging steam intervals. Define each specimen's complete timeline, including initial activation, all holds and ramps, ambient exposure if unavoidable, and the final measurement. Use the same final measurement on specimens used for recoverable-capacity comparison.

| Arm | Intermediate treatment | What the comparison answers |
|---|---|---|
| A: complete repeated assay | Reproduce the published NH3/wet-purge/dry-purge/heating sequence between steam intervals | Reference for the published operational measurement history. |
| B: matched sham | Match A's thermal, water, gas-flow, and handling sequence; replace NH3 with the carrier at matched flow | A versus B estimates the effect of the NH3-containing intervention in that defined sequence. The sham is not chemically inert. |
| C: no intermediate assay | No cooldown or chemical assay between damaging exposure segments; sacrificial specimens provide endpoints | C provides the uninterrupted-history reference. B versus C includes the full interruption/handling effect. |
| D: dry/handling controls | Apply corresponding non-steaming histories to fresh and previously steamed specimens | Constrains direct dry damage and changes specific to aging-generated populations. |

Do not claim A/B/C have identical full histories: they deliberately differ. Their causal contrasts are the experiment. Match damaging wet exposure and initial state for the first comparison, report all added dwell time, and use additional time-matched dry blocks when needed to distinguish the effect of elapsed thermal time. The later pulse comparison must have matched wet/dry totals and joint temperature/water distributions.

Before interpreting A versus B as a persistent state change, verify removal of residual NH3/nitrogen after the defined terminal heating/purge to the attainable detection limit. Protection from remaining ligands during the next wet interval would need to be distinguished from the known NH3-cofeed effect.

Use several sacrificial endpoint durations sufficient to measure a trajectory, rather than only a fresh and fully aged specimen. Run order should be randomized. Separate specimens are required for capacity and pre-assay functional measurements because each measurement may itself modify the material.

### Three outputs kept distinct

1. **Working acid function before terminal NH3.** Use an independently validated small-reactant probe and report initial and stabilized rates under a common feed. An alcohol-dehydration probe may generate water and change the sample. Commission cumulative probe-dose and contact-time dependence on separate aliquots; if even the earliest reproducible rate depends on conditioning, call it a conditioned functional endpoint. No probe is presumed nonperturbing. Report rate per initial catalyst mass as well as any site-normalized quantity.
2. **Recoverable capacity after the common terminal assay.** Use the established NH3 method with its operational interpretation. The purpose is a fair capacity endpoint, not a nonperturbing census of the steaming state.
3. **Al structure and accessibility on matched aliquots.** Begin with calibrated IR, elemental balance, and quantitative NMR with controlled hydration; add specific connectivity measurements only when function/capacity contrasts justify them. A tetrahedral-Al peak or 1H–27Al proximity alone does not count restored framework bonds.

For each branch, include blanks for transfer and final conditioning. Quantify the consequences of hydration for NMR visibility. A lack of change in XRD does not rule out local loss of acid function. Track total Al and residual cations so proton recovery cannot silently stand in for framework recovery.

Specify the final wet/dry phase and elapsed delay before every functional measurement. Different last recovery intervals can produce different working populations even when permanent loss is identical. Compare that operational difference separately from capacity after common conditioning.

## Interpretation and predictive test

The first deliverable is a contrast, not a large fitted mechanism:

- **A differs from B in subsequent loss and pre-assay function:** the NH3-containing intervention changes useful durability under the tested history. Identify which part of the intervention matters only after this result.
- **A differs in final recoverable capacity but not pre-assay function:** report protocol-dependent recoverable capacity; do not claim a useful operating benefit.
- **A and B agree, both differ from C:** investigate thermal/hydration/handling effects before assigning ammonia chemistry.
- **All agree within a practically meaningful uncertainty:** support transferability within the tested range. This does not prove every measurement is harmless in every zeolite.
- **Structure and function disagree:** retain the disagreement and test counterion/accessibility explanations. Do not force a lattice-repair narrative.

A compact state model may represent aging by `dx/dt = f(x, T, water)` and the assay by an explicit state-changing operation. Its outputs are pre-assay function and post-assay capacity. Do not infer a unique two-state mechanism merely because two observables exist. Fit one intervention spacing and predict another without refitting, while comparing against a simple cumulative-aging model and calibrated heterogeneous irreversible-loss models.

Predictive NH3-storage models are already established. Ladshaw carries adsorption kinetic parameters fitted to de-greened Cu-SSZ-13 forward to aged transients after updating age-dependent site densities ([original](../../literature/papers/ladshaw2022-measurement-and-modeling-of-the/original.pdf), pp.8–10). Those site densities come from the storage/aging analysis; they are not independent atomic counts. The proposed advance must predict the consequence of **different assay schedules**, beyond an ordinary changing-population model, rather than merely reproduce aged storage.

The method matters if including the assay materially improves held-out predictions of subsequent useful function/capacity or changes a consequential durability ranking. A ranking claim requires at least two relevant materials under both histories; do not infer it from one specimen type. Add that comparison only after the first contrast justifies it. Reproducing an immediate known NH3-induced signal change does not justify a broad methodological claim.

## Conditional application branch: simplify and exploit a real intervention

Only after the first comparison reveals a consequential effect should the program ask whether a short dry or other established recovery step retains the benefit. The strong first option is isothermal dry interruption because it minimizes added variables. Compare wet-then-dry, dry-then-wet, and repeated wet/dry histories with matched totals and measured local exposure. Calibrate dry evolution on previously aged specimens.

[The kinetic design calculation](../calculations/aging-identifiability.md) establishes two important limits:

- Equal exposure-order effects do not uniquely demonstrate a recoverable intermediate; even a nonseparable scalar irreversible-loss law can depend on order.
- A very fast equilibrating hydrolyzed population can eliminate a useful timing benefit despite slow overall irreversible loss.

Use the measured response range to choose pulse periods. A null result bounds the schedule benefit over that range; it does not bound an intermediate lifetime without additional evidence. If no feasible simple treatment retains the benefit, stop the timing branch rather than inventing a complex recovery cycle.

If the branch survives, transfer to **one** MFI catalyst and a specified cyclic acid-catalysis process. This transfer requires new validation because topology, Al environments, and coke chemistry change. Match initial coke, final carbon removal, actual maximum temperature and wet history when comparing regeneration. Benchmark against both conventional regeneration and a simpler milder regeneration/material choice.

The useful process metric is saleable product integrated over reaction periods, divided by initial catalyst inventory and total occupied reactor time, including regeneration. Also report product selectivity, catalyst replacement, purge/steam demand, and utility use. For equal catalyst inventory, a scheduling change improves time productivity only when its fractional increase in integrated useful product exceeds its fractional increase in total cycle time. This is an accounting identity; it does not predict that either increase will occur.

## Protocol-knowledge options from the 2026-09-16 direction search

Two Cu-CHA items from the [direction search](../reviews/direction-search-outcome.md) belong here as options rather than as new portfolio entries. Neither starts before the first comparison above is commissioned.

- **Desulfation atmosphere and per-cycle Cu speciation.** Whether regenerating a sulfated Cu-SSZ-13 with NH3 (and NO) present changes the fraction of isolated Cu converted irreversibly to CuOx per event is unmeasured at the speciation level; at the conversion level He 2025 found the atmosphere effect minor, and reductant-assisted deSOx is 2013–2024 patent prior art. The [screen](../working/direction-search/cu-pd-zeolite-durability.md) and its [review](../reviews/direction-search-cu-desox-independent-review.md) fix the design: NO present in both arms (dosing on versus off), a Cu-sulfate-forming exposure (400 °C SO2 or SO3) rather than 250 °C ammonium-sulfate formation, a closed sulfur balance, a 10-percentage-point EPR resolution target, sham and exotherm-matched arms, and about fifty specimens. Read Shen 2019 (10.1007/s11814-019-0307-x), Gao, Mossin and Vennestrøm 2025 (10.1002/cctc.202500597) and the He 2025 SI first; any of them may already contain the speciation-resolved comparison. The likely outcome (no atmosphere effect) fixes accelerated-aging protocol design and changes no calibration.
- **Owner-supplied frozen predictions for any Cu-CHA series prepared here.** Gjetja and Kamasamudram 2026 report that raising O2 restores mildly aged low-temperature performance, and Saxena 2026 predicts higher turnover with more non-Cu-compensated framework Al per cage. Both are one-run checks on the materials this program already handles; record them as predictions before the runs. The [open-problems screen](../working/direction-search/stated-open-problems-2026.md) shows the owners are measuring the aged oxidation half-cycle now, so these checks are validation, not a program.

## Go, narrow, or stop

| Gate | Advance only if | Otherwise |
|---|---|---|
| Prior art | The focal SI gate is clear; directly relevant prior work must also leave the comparison unresolved | Reuse their result; do not run a nominally new duplicate study. |
| Measurement | Actual histories and assay repeatability resolve a practically relevant contrast | Fix the measurement or reduce the claim. |
| Transferability | A repeated intervention changes subsequent function/capacity or a lifetime prediction beyond uncertainty | Retain the validated portability result; stop the regeneration narrative. |
| Mechanism | Added structural/functional observables discriminate among useful alternatives | Keep an operational model; do not claim unique Al aggregation or reconnection. |
| Application | A simpler feasible intervention improves full-cycle product output after downtime/utilities are counted | Preserve mechanistic knowledge; reject the process-improvement claim. |

Define the minimum useful effect before examining the definitive comparison, using measured analytical variance and the regeneration-time penalty. Numerical targets are experimental design decisions, not literature-established facts.

## Confidence and remaining limits

- **Scientific hypothesis:** moderate plausibility that assay history changes later behavior; the direction and magnitude are unknown. Confidence in a useful dry recovery window is lower.
- **Feasible and informative first experiment:** moderately high, because histories and operational outputs can be compared with standard kinetics/characterization. Instruments, material access, and specimen-transfer capability are unconfirmed.
- **Unique molecular explanation:** moderate to low without stronger structural constraints. An operationally predictive result can still be valuable.
- **Meaningful practical improvement:** low at present. Regeneration time, utility costs, and transfer to a useful reaction may erase the benefit.
- **Originality and significance:** narrow and provisional. Known recovery and testing-induced changes make a simple positive assay contrast insufficient; the required new result is consequential carryover and prediction. Specifically, the focal SI leaves the comparison open, and the uploaded recovery, cumulative-aging and storage-model studies narrow the contribution to consequential assay carryover and prediction. They do not establish the proposed effect. No priority claim is warranted now.

The current recommendation is to resolve the specific protocol-transfer question. It is not a claim that prior aging kinetics are wrong, that dry pulses heal zeolites, or that an industrial regeneration improvement has been found.
