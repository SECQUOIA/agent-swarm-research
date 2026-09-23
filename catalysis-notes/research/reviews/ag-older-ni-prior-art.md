# Independent review: older Ni/Cs/Re working durability evidence

## Decision

**US5380885A materially narrows the proposed Ag program.** It reports preparation, pressurized ethylene epoxidation, and repeated accelerated-aging measurements for Ni-postdoped Ag containing Cs, Re and sulfur. The current question cannot be presented simply as discovering whether Ni remains useful with Cs/Re/Cl, or whether that combination can improve durability. Those outcomes were already reported in 1995. This is stronger prior evidence than a list of contemplated promoters.

The patent does not independently validate its own results or identify the working Ni state. It also leaves important control gaps. A useful program remains possible, but its central question should become **which Ni-dependent working-state change preserves useful selective output, and whether that explanation produces a design or operating choice beyond the historical result**. This review supports a bounded redesign, not cancellation based solely on the existence of a patent and not an unconditional reaffirmation of portfolio priority.

## Source and scope

Primary source: [US5380885A, published 10 January 1995](https://patents.google.com/patent/US5380885A/en), *Process for preparing ethylene oxide*. Read the complete descriptive experimental example and Table III in the root-provided HTML-derived text `/tmp/epoxidation-process/us5380885a.txt`, especially lines 3300–3398, with preceding definitions and preparation description. The experimental section is **Illustrative Embodiment 1, Parts A–D**; it does not contain three separately numbered experimental embodiments. The Google web tool could not reopen the page during this review; the retained primary artifact supplies the text. No legal-status inference is made.

The complete patent source has since been [centrally ingested](../../literature/papers/kemp1995-process-for-preparing-ethylene-oxide/fulltext.md).

Comparison sources read: [current program](../programs/ag-selective-oxygen-use.md) and the publicly accessible author manuscript for [Jalil et al., Science 2025](https://doi.org/10.1126/science.adt1213), retained in `research/working/source-artifacts/jalil2025-nickel.txt`. The Jalil supporting information was not read in this original review. **2026-09-16:** it is now retained and incorporated in the [post-upload audit](post-upload-ag-audit.md), which confirms processing controls and Ni-proximity evidence while retaining working-state and durability limits.

## What the older experiment actually reports

### Material and route

The patent uses carrier C: an approximately 98.8 wt% alpha-alumina carrier with BET area 0.51 m²/g and water pore volume 0.38 cm³/g. Silver oxalate/ethylenediamine solution is combined with ammonium perrhenate, lithium sulfate, lithium nitrate and CsOH. Vacuum impregnation is followed by curing in flowing air at approximately 250–270 °C. This prepares the promoted Ag parent before nickel addition.

Nickel is introduced by a **second impregnation after the other components and curing**. A nickel-nitrate stock containing ethylenediamine, ammonia and ammonium carbonate is diluted into ethanol, vacuum-impregnated, excess solution decanted, and the material dried through staged temperatures ending at 250 °C. The text explicitly distinguishes this route from adding Ni together with all components. It does not demonstrate the location, dispersion or chemical state of working Ni. The preceding description explicitly proposes, without direct evidence, that ionic Ni binds to perrhenate oxyanions. A generic Ni–Re association is therefore already a stated mechanistic hypothesis, although its existence and catalytic role are not established.

All three catalysts contain approximately 13.5 wt% Ag. The disclosed approximate promoter contents are:

| Catalyst | Ni, ppmw | Cs, ppmw | Re, ppmw | S, ppmw | Processing |
|---|---:|---:|---:|---:|---|
| A | 88 | 460 | 280 | 48 | Ni post-impregnation |
| B | None | 460 | 280 | 48 | Ethanol post-impregnation |
| C | None | 430 | 280 | 48 | Cured parent without post-impregnation |

These are amounts per total catalyst mass, not surface atom fractions. The precursor recipe includes Li, although the final summary table does not report its concentration. Calling this a bare Ag/Cs/Re ternary material would omit sulfur and lithium-containing preparation.

The Ni:Ag atomic ratio calculated from the disclosed bulk contents is approximately **1:835**, using `(88×10⁻⁶/58.6934)/(0.135/107.8682)`. That differs from Jalil's approximately 1:200 bulk ratio. No Ag particle-size measurement in this experiment supports conversion to comparable Ni surface coverage. Neither the bulk-ratio difference nor the preparation route proves a different working mechanism. This is a dilute-Ni example, within the same broad bulk-loading scale as the approximately 1:450 geometric transfer estimate in the current program; it must not be conflated with a separate high-Ni sintering patent. A uniquely new single-atom state cannot be assumed from nominal loading alone.

### Reaction and aging protocol

- Catalyst: 3–5 g, crushed to 14–20 mesh, in a 1/4-inch stainless-steel U-tube immersed in a molten-metal bath.
- Inlet pressure: **210 psig**. GHSV: **3300 volumes of gas per catalyst volume per hour**, under the patent's stated convention.
- Inlet gas: **30% ethylene, 8.5% O2, 5% CO2, 54.5% N2, and 2–6 ppmv ethyl chloride**. No ethane cofeed is listed.
- Startup: one hour each at 225, 235 and 245 °C, then temperature adjusted to **40% O2 conversion**. Initial performance is normally determined after at least 2–3 days on stream.
- Samples are tested with a reference catalyst, and reported values are corrected relative to its average initial selectivity and temperature at 40% O2 conversion.
- Accelerated aging: either **85% O2 conversion or a maximum temperature of 285 °C**, for ten days. After each interval, samples return to 40% O2 conversion and are reoptimized before selectivity is measured. This repeats through 50 days of severe aging.

The source defines selectivity as moles of EO per mole of ethylene converted. Here `S40` is conventional ethylene selectivity at **40% oxygen conversion**, not Hwang's EO/CO2 ratio metric. The two selectivity symbols must not be compared directly.

### Endpoints

A and C reportedly start at **86.0–86.5% selectivity**, with `T40 = 259 ± 4 °C`. B starts at approximately **84%**, and the authors explicitly omit it from long-term testing because its initial performance is worse.

| Severe-aging duration | A: change from fresh S40 | C: change from fresh S40 | A minus C in change |
|---|---:|---:|---:|
| 10 days | −0.1 percentage points | −1.2 percentage points | +1.1 points |
| 20 days | −0.1 | −2.3 | +2.2 |
| 30 days | −0.8 | −3.4 | +2.6 |
| 40 days | −2.4 | −5.0 | +2.6 |
| 50 days | −4.3 | −6.1 | +1.8 |

The source prints percent signs, but these are differences between selectivities expressed in percent and therefore **percentage-point losses**. The 50-day advantage is 1.8 points in the loss from each catalyst's own initial value; an exact final-selectivity difference is unavailable because individual starting values are not provided. The advantage is not monotonically increasing throughout the experiment. From day 20 to day 50, A loses another 4.2 points and C loses another 3.8. The table can therefore resemble delayed onset of loss followed by comparable or faster later deterioration; it does not establish a persistently lower decay rate. Five points, missing uncertainties and adaptive stress conditions cannot support a lifetime or hazard model.

## What is and is not established

**Reported evidence:** a prepared Ni-containing, Cs/Re/S-promoted Ag material functions under a pressurized, chloride-containing oxidation feed and loses less selectivity than a Ni-free parent through this particular accelerated-aging protocol. Initial selectivity of A and C is similar. This directly anticipates useful Ni compatibility with a complete promoted formulation and a selectivity-retention benefit.

**Important limitations:**

1. **A versus C is not a composition- and processing-matched Ni contrast.** Cs differs, and C lacks the second impregnation. The text calls A a post-treatment of C while its table lists different Cs amounts; the exact preparation genealogy is not fully reconciled. Accept the reported approximate values rather than silently assuming equal Cs.
2. **B helps with initial performance but does not close the aging control.** A and B have matched listed Cs, but B was not aged. Ethanol-only treatment is also not a complete blank for the ligands and counterions in the small Ni-stock aliquot. The patent's inference that the effect is specifically nickel is stronger than the long-term control supports.
3. **The stress histories need not be identical.** A temperature ceiling and conversion target can expose catalysts to different temperatures and gas profiles. Per-catalyst trajectories, optimized chloride values, cumulative EO production, and aged `T40` values are not reported in Table III.
4. **No replicated aging uncertainties or working-state measurements are supplied.** Statistical robustness, promoter redistribution, silver morphology, and reversible chloride-state changes cannot be separated from the table.
5. **Reoptimized endpoint selectivity is not integrated useful output or commercial life.** This test does not establish a multiyear advantage, a fixed-output benefit, or a change in any particular elementary oxygen pathway.

These gaps limit causal attribution and extrapolation. They do not turn an actual disclosed experiment back into a merely speculative composition claim.

## Relation to Jalil 2025 and the proposed program

Jalil's supported catalysts lack Cs/Re in the reported Ni experiments, use approximately 70–75 nm Ag and a roughly 1:200 Ni:Ag optimum, and show a large fresh selectivity response at atmospheric pressure. The chloride-containing experiment extends about 18 hours and exhibits evolving rates. Its surface-science work supports hypotheses about Ni-dependent oxygen activation and stabilization, but does not establish the active state in the older complete promoted catalyst.

The historical example has a different empirical emphasis: **little reported initial A/C selectivity difference and improved retention after aging**. This is a reason to distinguish an immediate suppression of combustion from preservation of a selective working structure or promoter configuration. It is not proof that different mechanisms operate: the formulation, loading, pressure, gas composition and protocol also differ.

The present program already rejects composition-only novelty and requires a predictive mechanism. Nevertheless, its opening rationale treats compatibility with a full promoted catalyst mainly as an untested extrapolation from two separate recent parent studies. That framing now needs correction. The older experiment supplies both a practical antecedent and an additional parent behavior worth understanding.

## Recommended redesign and stopping rules

1. **Replace generic compatibility as the novelty claim.** State that Ni-dependent selectivity retention on promoted Ag is reported historical evidence, while the working cause and a transferable design rule remain unresolved in the sources inspected. Establish whether further literature already explains them before claiming an open mechanism.
2. **Make one consequential distinction the first research decision:** does Ni primarily change fresh reaction selectivity, prevent deterioration of the useful promoted state that persists through the specified recovery, or alter a reversible operating state that can be recovered without Ni? These possibilities imply different interventions and different accounting of useful output.
3. **Use a matched promoted pair before expanding a full factorial.** Anchor preparation in a functioning promoted catalyst and a justified Ni route. Match Cs and the treatment blank, retain pre/post-treatment composition and size information, and compare fresh behavior, a documented exposure history, and recovery at a common reference state. Chloride adjustment and repeated reference checks remain necessary. Re-free formulations become useful if they distinguish the selected explanation; they need not be the initial large commitment. Because the old experiment already returned catalysts to a reoptimized reference state, merely adding such a return is not new. Record the recovery trajectory, the defined intervention and its useful-output cost, and show that the resulting explanation predicts a previously untested response.
4. **Require a prediction that changes a choice.** For example, a supported diagnosis of reversible operating-state loss should predict a recovery procedure and its recurring output cost; a supported structural-retention mechanism should predict which exposure causes persistent divergence after equal reconditioning. An extra aging curve or spectrum alone would reproduce or decorate the old observation.
5. **Retain practical endpoints.** Compare integrated net EO output, selectivity, required temperature and promoter inventory through the documented protocol. A gain after accelerated stress is only useful within its tested scope until normal-operation relevance is demonstrated.
6. **Keep oxygen-isotope work optional.** The old patent does not validate a unique oxygen-transfer mechanism, and an isotope campaign does not itself solve the durability question. Use it only if a discriminating bound would change the chosen intervention.

**Confidence:** high that actual combined-catalyst working and aging data predate the proposed program; moderate that a careful matched comparison can clarify the historical effect if materials and pressurized-reactor capability are available; uncertain that the necessary Ni state or useful durability gain transfers to a modern reference. Practical upside remains credible because retention matters, but no incremental advantage over current technology is established.

**Evidence update:** this source raises confidence that useful Ni compatibility with a promoted formulation is experimentally plausible, while lowering the originality of testing compatibility itself. It does not establish modern competitive performance or the modern Ni preparation's transferability.

**Portfolio implication:** retain Ag as a candidate for a narrower, mechanism-led program, but re-review its priority after the novelty correction. Do not count generic Ni/Cs/Re compatibility, high-pressure translation, or an unspecified aging advantage as the missing contribution. If no consequential predictive distinction survives the broader historical source check, lower its priority rather than enlarge the promoter screen.
