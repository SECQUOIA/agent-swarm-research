# Can the first native-product pilot resolve useful cleaning?

2026-09-15. Independent decision review of the [program](../programs/zirconia-styrene-oxygen-fate.md), [measurement review](oxygen-measurement-feasibility.md), [feed-scaling calculation](../calculations/styrene-feed-scaling.md), and [decision brief](../decision-brief.md). This review uses their documented source facts and makes experimental-design deductions; it introduces no new literature claim. Instruments, catalyst access, and whole-method precision remain unconfirmed.

## Decision

**Keep the unlabeled pilot, but change its first scientific comparison.** Comparing two pretreatments and collecting products can establish reproducibility and find candidates. It cannot distinguish water-dependent recovery from thermal recovery plus an unrelated oxygenate transient. A small factorial comparison of water history and ethylbenzene exposure gives more useful evidence with the same kinds of measurements.

The first defensible positive result is **water-history-dependent, ethylbenzene-assisted recovery accompanied by incremental oxygen output**. It is stronger than a new peak and weaker than proving that organic oxygen export removes the blocking species. No unlabeled protocol in the current proposal guarantees the latter inference. If that stronger inference is indispensable, the pilot should select a specific follow-up rather than be presented as capable of delivering it.

There are two distinct reasons to continue: a resolved connection to recovery, or an identified product that demonstrably changes useful styrene output at credible exposure. Product identity without either result does not justify a larger program.

## 1. Set the decision scale before commissioning

The source-based inventory is approximately 2.4 μmol pairs in 20 mg zirconia. A 25% recovery would correspond to 0.604 μmol oxygen **if** one water blocks one pair and rate recovery counts that population. Use this as a sensitivity example, not a measured denominator. Its 10% branch is 0.0604 μmol O.

The measurement review estimates that 125–500 standard cm³/min, defined at 273.15 K and 1 atm, would give roughly 2–0.5% EB conversion at its stated illustrative styrene rate and 1.2 mol% EB. Applying those flows to the finite example gives:

| Signal or background | 125 standard cm³/min | 500 standard cm³/min |
|---|---:|---:|
| 0.604 μmol O exported over 1 h, as one-O products | 1.81 ppm mean | 0.451 ppm mean |
| 10% branch over 1 h | 0.181 ppm mean | 0.0451 ppm mean |
| Same finite 10% branch averaged over 14 h | 0.0129 ppm mean | 0.00322 ppm mean |
| Water admitted at 4 ppm over 14 h | 18.7 μmol | 75.0 μmol |

These flows are design illustrations, not the reported recovery flow or a recommended operating range. Collection can recover a useful integrated mass even when the instantaneous concentration is small. However, prolonged collection does not amplify an exhausted transient.

For scale, if inlet and outlet integrated water each had an independent uncertainty equal to 1% of the 14 h water throughput, their difference would have an uncertainty of approximately 0.265–1.06 μmol using the same uncertainty convention. That exceeds the entire 0.0604 μmol branch and can exceed the full recovery example. This is illustrative error propagation, not an instrument specification. Direct differential calibration, correlated errors, drift, and switching tails can change the result. The calibration must establish their actual effect.

Choose one question the complete method can answer. For example: can it exclude an organic outlet above a stated number of nmol O per recovery, or above a stated fraction of reacted EB during maintained operation? The former requires a measured recovery-associated inventory or an explicitly hypothetical denominator; the latter uses independently measured formation rates. A 10% branch is not intrinsically consequential. A smaller potent poison can matter; a larger harmless branch may have little process effect.

Commission the actual collection window, matrix, and blank subtraction used in the comparison below. Require uncertainty on the **difference between histories**, including specimen variability, rather than quoting a single-sample detection limit. Failure here stops molecular attribution at that scale. It does not constitute a negative chemistry result.

## 2. Smallest coherent first sequence

### A. Establish a water-responsive starting state and a valid activity readout

Use one reproducible preparation and pretreatment. On matched portions, apply either a measured partial water dose or a sham treatment, with identical temperature, H2, elapsed time, and purge. Measure dose, breakthrough, and water released during purge. Verify a reproducible water-associated loss of styrene-forming function. Do not infer admitted moisture from the loss.

The two published pretreatment histories can be reproduced as context, but they should not substitute for this water/sham contrast: pretreatment also changes residual carbon and possibly structure. Do not introduce DME during the measured recovery window.

Use styrene formation at a fixed diagnostic feed as the operational measure of function. A no-EB recovery arm requires an endpoint EB assay, and EB may itself reactivate the specimen during that assay. Establish an early readout whose state change is below the functional contrast being tested, or quantify a defensible correction and its uncertainty. Match switching and residence-time delays. If recovery is faster than a valid assay, the no-EB arm has no comparable endpoint; resolve the readout before claiming EB-assisted recovery. A fitted extrapolation alone does not remove this ambiguity.

If the initial state disappears during mixing or detector delay, the minimal identifiable observations are the oxygen outlets during the prescribed exposures and function **after the common assay exposure**. Equal final rates then cannot distinguish thermal recovery before EB admission from recovery caused by the assay. Resolved transients within the EB arms remain observable, but do not recover the missing no-EB functional endpoint. Retain product discovery and oxygen-release bounds; stop the thermal-versus-EB functional inference unless a validated non-erasing readout becomes available. Include EB admitted during switching and readout in the exposure record.

### B. Cross water history with recovery exposure

Use four matched histories, with repeats sufficient to resolve their differences:

| Starting history | Recovery interval with EB | Same interval without EB |
|---|---|---|
| Measured water dose and purge | Candidate recovery and oxygen output | Thermal/H2 recovery and oxygen output |
| Sham dose and matched purge | Baseline EB chemistry and aging | Baseline thermal/H2 history |

Hold temperature, pressure, H2, flow, and interval fixed; replace EB with carrier in the no-EB arm. Collect water and calibrated organic/COx outlets across dosing, purge, and recovery, retaining their time boundaries. Use the same common endpoint assay after each recovery interval. Run the corresponding train/quartz blanks so feed switching and wet-train release cannot become a catalyst signal.

For endpoint activity, compare the EB effect in the water-dosed history with the EB effect in the sham history. For integrated non-water oxygen output, make the same difference of differences:

```text
I_O = (O_water,EB − O_water,noEB) − (O_sham,EB − O_sham,noEB)
```

Each O is net outlet oxygen after measured feed and apparatus contributions, on a common collection basis. Report the four underlying results as well as the difference; cancellations can otherwise conceal substantial thermal output or baseline drift. Keep water release as a separate channel, then examine the total oxygen account. Do not normalize product output by rate-derived site counts.

This contrast removes a simple additive thermal-release background and baseline EB side chemistry. It does **not** exclude an interaction in which water independently changes side chemistry while EB independently changes the catalyst. Equal timing or a nonzero interaction is evidence of association, not mediation by a particular product route. Changes in thermal water release induced by EB also remain a possible recovery pathway.

### C. Repeat the informative contrast once the signal is resolved

At the same dose, perform a further water/sham and recovery cycle without renewing activation reagents; retain matched controls and watch baseline drift. Then use a second independently measured partial dose only if the first contrast is resolved. Ask whether recovered activity and incremental O output recur and vary together, without forcing proportionality or a one-O-per-pair slope.

This is the smallest useful challenge to a one-off activation residue. A declining oxygen burst with repeatable recovery makes that burst a poor explanation of continuing cleaning. A continuing burst without recovery makes it a poor functional marker. Repeated coupled responses support continued investigation.

**A few cycles cannot exclude a large reservoir.** Ten example cycles export only about 6 μmol O, versus about 325 μmol lattice O in the zirconia and approximately 33 mmol structural O in the reported quartz charge. Those total capacities do not establish accessibility; they show why repeatability alone cannot establish exhaustion. Reject a specified storage-only account only when the exported amount exceeds a defensible bound on the reservoir it invokes, or an independent retained-inventory measurement constrains its change. An empty/quartz blank does not bound EB-induced oxygen release unique to zirconia.

Matched integrated input/output balances can bound **net** oxygen accumulation or depletion over repeated cycles. They cannot exclude equal counterflows, isotope exchange, or a changing carbon reservoir. Report which storage claim is actually bounded. Do not demand weeks of operation solely to exceed the entire lattice inventory; select a targeted provenance or inventory measurement if that ambiguity controls the next decision.

## 3. Interpret outcomes before choosing more experiments

| Resolved result | Interpretation and next decision |
|---|---|
| Water-dosed material recovers as much without EB as with EB; no useful EB-specific oxygen contrast | Thermal/H2 recovery is sufficient under the tested history. Stop claiming EB-assisted cleaning in that experiment. This does not invalidate the published behavior under different conditions. |
| EB gives additional recovery; incremental output is predominantly water and non-water outlets have sufficiently small summed bounds | Organic export is not needed above the stated bound. Pursue EB-assisted water release or another state change only if it has useful consequences; do not label this proof of organic cleaning. |
| EB gives additional recovery and a repeatable water-history-dependent organic/COx output | Advance with the narrowed association claim. A targeted isotope experiment can address water origin; it still needs exchange controls and cannot alone identify the blocking site. |
| Oxygenated product appears equally in sham EB runs, or its transient fades while recovery repeats | Generic side chemistry or finite precursor inventory is a sufficient explanation of that product signal. Do not use it as the cleaning marker. |
| Recovery occurs but outlet bounds or net-water differences are too imprecise | Analytical ambiguity. Redesign the collection/dose/throughput only within validated chemistry, or stop at functional recovery. Nondetection does not reject export. |
| Apparent net oxygen deficit persists, with no bounded solid/train inventory | Storage or missing outlets remain unresolved. Do not calculate a sustained cleaning yield or apply gas-only cycle thermodynamics. |
| Product is resolved but no recovery-specific contrast exists | Product discovery alone. Continue only if its measured or credibly bounded practical exposure produces a useful functional effect. |

For a consequence test, use the actual product concentration and a stated plausible return range; compare against a sham feed and measured water generated by its conversion. A persistent loss of styrene output at that exposure is an actionable adverse result even before the precise cleaning mechanism is assigned. No effect excludes only the tested exposure and duration. Failure to know separation return is not a reason to build a recycle apparatus: first state the exposure range for which the decision would change.

A selective change in the proposed route, with corresponding recovery change and little effect on dry-state function, would strengthen causal attribution. A product/co-product challenge may supply such a test once the net route is known. It remains conditional on adsorption, water generation, and inhibition controls; it is not part of the first pilot by default.

## 4. Water uptake is not automatically an independent functional capacity

The proposed instruction to measure “calibrated water uptake and the associated rate loss” needs a narrower interpretation. Calibrated dose-minus-effluent measurement independently measures **net retained water-equivalent oxygen**, within its inventory assumptions. An activity assay independently measures **styrene-forming function under its assay conditions**. Their combination does not independently count the active Zr–O pairs.

The fatal circular inference would be:

1. Assume one retained water blocks one pair and rate is proportional to free pairs.
2. Use uptake and the rate loss to define pair capacity.
3. Use recovered rate or renewed water uptake to calculate recovered pairs.
4. Treat oxygen export per such recovered pair as independent confirmation of the same blocking stoichiometry.

Using separate specimens removes destructive-measurement interference, but does not remove those shared assumptions. Water can populate inactive surfaces, refill newly accessible reservoirs, exchange, or react during titration; the same rate change can reflect different per-site turnover rates. Uptake may still be a useful operational capacity, provided it is named and reported as such.

The simplest robust pilot does **not** need a site census. Report delivered and retained water, recovered styrene rate, native oxygen output, and their uncertainties as separate observables. If an independently validated site-selective assay is actually available, add it for an oxygen-per-pair claim. Otherwise leave that claim open rather than inventing an orthogonal assay or relabeling uptake as a count.

## Changes recommended to the lead decision

Replace “reproduce recovery and collect native products” with the water-history × EB-exposure contrast and explicit assay-validity gate. Separate three deliverables: recovered function, incremental oxygen output, and a product effect at credible exposure. Reserve claims of sustained water-derived cleaning and pair stoichiometry for the evidence that specifically tests them.

Defer the 2 × 2 feed-scaling matrix, coproduct thermodynamic grid, and recycle experiments until a result identifies which question matters. Their algebra may be sound, but none resolves the initial causal ambiguity. The next commitment should be conditional on actual sample access and measured method performance, not an assumed instrument list or the nominal μmol inventory.
