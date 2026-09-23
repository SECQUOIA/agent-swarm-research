# Independent review: interrupting zeolite steam damage

Date: 2026-09-15. Reviewer role: independent critical reviewer; not the proposer. Reviewed `research/working/zeolite-screen.md` after an independent source search. No experiments were performed. Literature files were not changed.

**Current status, 2026-09-16:** the [uploaded-literature update below](#2026-09-16-update-uploaded-prior-art-and-current-recommendation) and [developed program](../programs/zeolite-durability-and-measurement.md) govern the current recommendation. Earlier source-access statements below are dated history; they must not be treated as a current missing-source list.

## Decision: bounded screen, with narrower claims

The proposed NH3-free, isothermal timing experiment is worth a small falsification campaign. A full catalyst-development program is premature. Reversible Al coordination, partially hydrolyzed intermediates, ammonia-induced recovery, and staged steaming are established prior art. The remaining potentially original question is whether an experimentally accessible relaxation time permits **more retained catalytic function after a common terminal treatment at equal measured wet and dry exposures**, and whether that benefit exceeds credible irreversible-aging models.

The main reason for caution is mechanistic: slow permanent loss does not imply a useful delay before permanent loss. The 2026 CHA interpretation assumes quasi-equilibrated hydrolysis upstream of slower association. If the intermediate population re-equilibrates much faster than gas exchange, each wet segment promptly restores the same loss rate. Drying then adds no advantage beyond the exposure time removed. The paper motivates the question; it does not establish the needed timing window.

| Judgment | Assessment |
|---|---|
| Narrow experimental novelty | Plausible but provisional; no equal-history, NH3-free pulse-frequency demonstration found in this search. |
| Identifiability of a practical schedule benefit | Good if local exposure and terminal treatment are controlled. |
| Identifiability of hydrolysis followed by aggregation | Weak from endpoints alone; at best identify an additional state before assigning its chemistry. |
| Feasibility | Reasonable for one H-CHA composition and sacrificial aliquots; equipment and transfer sensitivity remain unconfirmed. |
| Practical priority | Conditional and below an established durability improvement until a useful timing effect survives. |

## What the key source actually establishes

I reread the relevant extracted pages and visually checked original PDF pages 4–5.

- **The kinetic series already contains interventions.** The same packed bed undergoes steam exposure, dry-air cooldown, transfer, NH3 titration, and return to the aging reactor. Before steaming, it receives a dry-air hold at 873 K for 2–4 h. The H-form assay includes 2 h NH3 saturation at 433 K, an 8 h wet-He purge at 433 K, dry purge, and heating to 873 K. These are substantial chemical and thermal treatments. The cumulative steam-time curve is therefore not an uninterrupted specimen history. [[martinez2026-consequences-of-non-mean-field]] p.4; [DOI](https://doi.org/10.1016/j.jcat.2026.116848).
- **The measured population includes recoverable sites.** The authors explicitly interpret their titration as counting framework-associated Al that heals under NH3 and use its loss as a measure of Al that cannot be recovered by that procedure. This is a defined operational endpoint, not a direct census of framework bonds under steam. A new common endpoint assay is appropriate for retained capacity, but cannot by itself show that dry intervals repaired bonds. [[martinez2026-consequences-of-non-mean-field]] p.5.
- **The molecular assignment remains an interpretation.** Apparent Al orders slightly above two support an association-based explanation in the authors' framework. Their analysis does not distinguish monomer–monomer from monomer–framework-associated association. It assumes quasi-equilibrated hydrolysis in these candidate models and does not measure the intermediate lifetime. [[martinez2026-consequences-of-non-mean-field]] p.6-8.

The draft acknowledges the first two points correctly. It should emphasize the third more strongly. The local package contains no supporting-information artifact, so I cannot settle whether the SI separately tests continuous versus repeatedly assayed aging. That check remains necessary before claiming a new protocol result.

## Independent prior-art and contrary-evidence check

Evidence labels below distinguish direct source reading from abstract-level constraints. Cross-topology observations are warnings, not assumed CHA mechanisms.

| Source and evidence tier | Consequence for this proposal |
|---|---|
| Wouters, Chen and Grobet, *Steaming of Zeolite Y: Formation of Transient Al Species*, 2001, [10.1021/jp001620p](https://pubs.acs.org/doi/10.1021/jp001620p). Publisher abstract read. | Framework-related Al–OH intermediates and ammonia-driven octahedral-to-tetrahedral conversion are old observations. Intermediate detection or coordination recovery alone is not new and does not prove lattice repair. |
| Fan et al., *Dynamic evolution of Al species in the hydrothermal dealumination process of CHA zeolites*, 2022, [10.1039/D2QI00750A](https://pubs.rsc.org/en/content/articlelanding/2022/qi/d2qi00750a). Publisher abstract read; [author-hosted full text located](https://dmto.dicp.ac.cn/2022-9.pdf), not fully read. | Prior CHA work identifies partially hydrolyzed framework-associated Al and EFAl interactions with BAS. Changed proton environments are an immediate alternative to restored connectivity. |
| Nielsen et al., *Kinetics of Zeolite Dealumination: Insights from H-SSZ-13*, 2015, [10.1021/acscatal.5b01496](https://doi.org/10.1021/acscatal.5b01496). [Author-institution abstract read](https://www.sintef.no/en/publications/publication/0198cc3d7700-96988b19-3fae-4514-a472-cb73b29ad61d/). | DFT/microkinetic work identifies later hydrolysis as sufficient to estimate rates above 700 K in its model. This is a competing theoretical account, not an experimental measurement of a recovery window. |
| Benešová et al., *Oxygen exchange mechanisms in zeolite chabazite under steaming conditions*, 2024, [10.1016/j.micromeso.2024.113007](https://www.sciencedirect.com/science/article/pii/S1387181124000295). Publisher abstract and exposed results/conclusion excerpts read. | Simulations allow exchange and framework healing alongside hydrolysis. Isotope exchange therefore cannot establish net Al reinsertion. These results also caution against assuming monotonic dependence on local water loading. |
| Agostini et al., *In Situ XAS and XRPD Parametric Rietveld Refinement To Understand Dealumination of Y Zeolite Catalyst*, 2010, [10.1021/ja907696h](https://pubs.acs.org/doi/10.1021/ja907696h). Publisher abstract read. | In NH4-Y, substantial Al migration occurs during wet cooling as water repopulates pores. Cooling and hydration can create damage; a recovery interval is not intrinsically protective. Start isothermally and preserve terminal histories. |
| Wang et al., *Evidence of Preferential Aluminum Site Loss during Reaction-Induced Dealumination*, 2024, [10.1021/jacs.4c13212](https://doi.org/10.1021/jacs.4c13212). Local primary text p.3-4 read. | Site location affects survival and residual catalytic activity. Crucially, greater loss of pair signals is consistent with random loss of individual sites: the paper says isolated and proximate sites have similar propensity. Pair-signal depletion does not uniquely prove encounter-controlled damage. [[wang2024-evidence-of-preferential-aluminum-site]] p.3-4. |
| Madeo et al., *Steam-Induced Aluminum Speciation and Catalytic Enhancement in ZSM-5 Zeolites*, 2025, [10.3390/catal15121130](https://www.mdpi.com/2073-4344/15/12/1130). Publisher sections and conclusion returned by search read; full article not systematically assessed. | Already reports ammonia protection, partially reversible Al speciation after low-temperature hydrothermal treatment, and enhanced activity through altered acid ensembles. An NH3 or autoclave fallback has much weaker novelty than the dry timing experiment. |

Exact-phrase searches for interrupted, intermittent, cyclic, periodic and pulsed steaming found adjacent staged treatments rather than the proposed matched experiment. For example, Kraushaar's 1989 thesis interrupts steaming for acid leaching, explicitly changing composition ([thesis DOI](https://doi.org/10.6100/IR302523), printed pp.86–88, [repository PDF](https://pure.tue.nl/ws/portalfiles/portal/1979092/302523.pdf)). This does not anticipate an equal-composition dry-pulse test. Search non-discovery is not proof of novelty.

The draft's Luo sequence-independence source is a particularly relevant counterexample. I verified its publisher record/excerpts, but not the complete experiment or SI; its conditions and observables need checking before treating it as a decisive null result for H-CHA. [Luo et al., 2018](https://www.sciencedirect.com/science/article/abs/pii/S0009250918303774).

## Decisive scientific fixes

### 1. State exactly which null a matched histogram rejects

With an inert dry interval and one fixed wet condition, any autonomous irreversible law `dA/dt = -g(A)` gives the same final A at equal wet time. More generally, `dA/dt = -k(u)g(A)` is determined by cumulative kinetic dose. This holds for nonlinear orders; curvature alone cannot create a segmentation benefit.

But equal time at each condition does **not** reject every memory-free model `dA/dt = f(A,u)`. For example, let wet loss be `-kw A²` and dry loss be `-kd A`. Writing `q = exp(-kd td)` and `b = kw tw`, wet-then-dry gives `A0 q/(1+b A0)`, whereas dry-then-wet gives `A0 q/(1+b A0 q)`. Both models are irreversible and have no recoverable intermediate, yet ordering matters. This is an analytic counterexample, not a proposed zeolite mechanism.

Calibrate dry effects on both fresh and previously steamed aliquots, since a fresh-only dry control misses dry evolution of an aging-generated population. Test scalar and simple heterogeneous nulls on withheld schedules. A difference between restart hazards at the same total measured A indicates that A alone is insufficient; heterogeneous site populations can still account for that difference. Do not name the missing state “aggregating Al” without structural evidence.

### 2. Measure the actual accessible timing range before expanding the matrix

Measure wet-to-dry and dry-to-wet water responses through the loaded apparatus, including adsorption tails, and bed temperature during switching. Match the **joint** temperature/water exposure distribution, not just separate temperature and water summaries. Integrated water flow or inlet setpoints alone do not match local chemical exposure. Use dilute beds and flow/particle-size checks for any positive result.

A resolvable intermediate requires more than slow net loss: its relevant buildup and relaxation must be distinguishable from apparatus response and sample transfer. Fast quasi-equilibrium is a first-class negative hypothesis. The smallest planned pulse must follow measured response time, rather than an attractive nominal number.

### 3. Keep the first screen smaller than the full draft

Start with one well-characterized H-CHA preparation, sacrificial aliquots, no intermediate NH3, one constant temperature/wet pressure, and three schedules: wet-then-dry, dry-then-wet, and repeated wet/dry at matched totals. Include unaged and dry-only controls. First determine endpoint repeatability and a duration giving measurable partial loss. Use independent reactor runs for the decisive contrast; then repeat it with an independent preparation. Add a second composition and a period sweep only after a signal survives exposure correction.

An initial negative result should stop the dry-timing branch over the measured range. A single known recovery chemistry can serve as a positive assay control; it should not automatically reopen an unrestricted intervention search.

### 4. Separate three claims and their evidence

1. **More retained operational capacity:** a common terminal NH3/water assay can support this claim despite its chemical perturbation, provided its selectivity is established and all histories share it.
2. **More useful acid function before NH3:** requires a functional test on separate matched aliquots, because reaction-generated water or probe adsorption can change the material. Early and stabilized rates answer different questions.
3. **Framework reconnection before aggregation:** requires independently constrained connectivity/speciation and Al/proton balances, not tetrahedral-Al intensity or uptake alone. Quantitative NMR must account for invisible Al and treatment-dependent response; generic proximity correlations are not automatically bond counts.

If only the first claim survives, report retained recoverable capacity. If function survives without reconnection, classify the result as acid-function regeneration and reconsider its novelty against EFAl/counterion literature. Do not relabel every positive assay response as support for the original mechanism.

### 5. Make the negative-result statement honest

No schedule effect does not by itself bound intermediate lifetime. It may mean negligible recoverable population, ineffective dry recovery, fast equilibration, countervailing dry damage, or an assay that erases differences. Report an upper confidence bound on the **schedule benefit over the tested periods and conditions**. Translate that into a lifetime bound only with a validated model and independent sensitivity to intermediate abundance/recovery.

## Stop/go recommendation

Proceed only through an assay-and-waveform audit and the minimal schedule comparison. Set a practically relevant effect threshold before examining the definitive contrast, based on assay precision and the regeneration time penalty. Statistical significance alone is not a useful threshold.

Advance to structural attribution only if retained capacity or function improves reproducibly beyond exposure uncertainty and calibrated irreversible nulls. Advance to an applied program only if a feasible schedule subsequently improves product per initial catalyst mass and reactor time at matched coke removal, including dry-gas demand and downtime. H-CHA-to-MFI transfer is a new mechanistic test, not routine validation; topology, Al environments, and regeneration chemistry change.

Reject a full program now. Preserve the bounded screen because a clean negative result can establish that intermittent measurements do not conceal an accessible timing benefit in this regime. Do not promise discovery of an aggregation clock, lattice repair, or industrial lifetime extension.

## Unresolved evidence and requests

- Obtain and read the 2026 CHA supporting information for continuous/interrupted or assay-repetition controls.
- Missing primary-source requests sent to the parent: Wouters 2001, DOI `10.1021/jp001620p`; Agostini 2010, DOI `10.1021/ja907696h`. Both directly affect interpretation.
- Fan 2022 author-hosted PDF and Benešová 2024 should be retrieved/read if absent before molecular claims are expanded. Nielsen 2015 merits comparison as a contrary kinetic model. These are requests for the sole literature agent, not completed literature promotion.
- No positive recovery timescale in the proposed high-temperature, NH3-free CHA protocol was verified in this review. Instrument access and achievable timing remain unknown.

## Addendum: review of the revised lead

The parent proposed reframing the lead as **separating assay-assisted regeneration from intrinsic hydrothermal durability, then exploiting any verified recovery window**. I support this as the first bounded question. It is more directly connected to the actual 2026 protocol than a presumed dry-recovery clock. It does not presently justify a full methods program: reversible probe-induced coordination is old, and the SI could already resolve protocol dependence.

The defensible estimand is the effect of inserting the assay protocol on subsequent loss and working function. Avoid implying that a chemically untreated specimen has a uniquely “intrinsic” durability; all durability measurements refer to specified temperature, atmosphere, and handling histories. The existing paper states its assay and interpretation explicitly. The open issue is transferability of its measured kinetics to a different exposure/measurement schedule, not an established error in its results.

The first experiment should compare repeated complete assays with sacrificial endpoint specimens, using the same starting pretreatment and a common terminal assay. Then use a matched sham intervention that retains the cooling, heating, flow and wet-purge history while omitting NH3. The full-assay versus sham contrast isolates the NH3-containing treatment more closely; the sham versus uninterrupted contrast tests thermal/water/handling effects. An NH3-free sham is not chemically inert, and differences should initially be attributed to the complete intervention. Add component controls only when the first contrasts require them.

Use separate matched specimens for function before terminal NH3. A repeated-assay group with better terminal capacity but no greater pre-assay function establishes protocol-dependent recoverable capacity. A repeated-assay group with sustained higher function demonstrates assay-assisted regeneration. Agreement between groups supports portability within the tested range. Either conclusion needs measured waveform matching and independent repeats; neither uniquely assigns framework reconnection.

For a model-based contribution, calibrate on one intervention spacing and test another without refitting. Compare against the simplest model that treats the assay as an explicit state-changing operation; do not assume that two measured inventories uniquely identify a two-population kinetic model. If the only result is a familiar immediate NH3-induced signal change, the contribution is too small. If assay frequency changes subsequent apparent aging kinetics or materially changes predicted remaining useful life, a focused protocol paper could be consequential, even if dry pulses fail. SI novelty clearance is therefore a gate before expanding this revised lead.

## Final consistency check of developed program

Reviewed `programs/zeolite-durability-and-measurement.md`, `calculations/aging-identifiability.md`, the calculation source, and its saved numerical summary. **No conceptual blocker to the bounded campaign beyond the stated SI/prior-art and commissioning gates.** The program correctly distinguishes causal A/B/C arms from matched-history pulse tests, common final capacity from pre-assay function, and operational prediction from molecular identification. The nonseparable scalar counterexample is correct. The coarse model conserves Al equivalents, and its ideal terminal observation `F+R` is explicitly identified as an assumption. The saved fast-equilibration result supports the limited claim made: capacity benefit is negligible for those illustrative parameters, not universally zero.

Three small wording edits are needed for consistency:

1. In the mathematical note, replace “never-assayed trajectory under matched histories” with “trajectory without intermediate assays at matched initial state and damaging wet exposure, using sham controls for the deliberately different interruption histories.” Both capacity trajectories do receive a common terminal assay; their complete histories cannot be identical.
2. In that note, replace “With no recovery and no dry damage” and “no-recovery limit” with “With no evolution during dry intervals” and “dry-inert limit.” The `no_dry_recovery` case still has wet recovery (`kr=0.1`). Its invariance follows because the entire dry-state evolution is zero.
3. In program H0, change “The published kinetic description transfers” to “Agreement supports transferability between these tested histories.” Equal observations do not independently validate the original fitted law, parameters, or other samples.

One interpretive detail should remain explicit in reporting: equal post-assay capacity can coexist with different pre-assay populations. In the saved fast-equilibration example, final F changes substantially with segmentation while F+R barely changes, partly because the final dry bout has different duration. This illustrates why the phase and delay of the functional measurement must be defined. A useful immediate functional difference should be reported separately from prevention of irreversible loss; neither should be inferred from the other. The developed program's common-feed tests and recorded terminal timelines can handle this without adding a new experimental branch.

The developed program's negative-result wording is sound: bound the schedule benefit over the measured range, and infer no intermediate lifetime without additional evidence. The mathematical note's independently **measured** relaxation bound is also defensible; a null pulse result alone must not supply that bound.

## SI novelty gate resolved: the specific contrast remains open

**Updated 2026-09-15 after primary-source inspection.** The previously unresolved supporting-information check is now complete for the proposed contrast. I read SI Sections S4–S5 and the start of S6, printed pages S14–S24, together with the related parent-characterization, kinetic-analysis, mechanism, and uncertainty sections. I inspected the original figures/schemes on pages S15, S16 and S21 visually. Source: Class-Martínez et al., supporting information to [10.1016/j.jcat.2026.116848](https://doi.org/10.1016/j.jcat.2026.116848), [public author-shared PDF](https://app.box.com/s/d2g0eiqdy2usji5nswueefcs5fnc3aqg), read locally as `/tmp/styrene-oxygen-review/cha-dealumination-si.pdf`. Printed SI labels below are source-page locators, not invented KB citations. This addendum supersedes earlier statements that the SI was unavailable.

**Finding:** I found no reported continuous-versus-interrupted aging comparison, complete-assay-versus-NH3-free-sham comparison, or recovery-duration/frequency series that tests subsequent aging. The SI therefore does **not** preempt the proposed A/B/C assay-history experiment. This clears the specific SI gate; it does not establish priority over the wider literature or unpublished work.

| SI location | What is actually reported | What it does not establish |
|---|---|---|
| S3, Figures S3–S4 on S6–S7 | Parent CHA NH4-form and gas-NH3/wet-purge H-form TPD comparisons. | Equality of future aging after different measurement histories. |
| Section S4, S14 | Prior MFI validation of selective H-site counting: wet purge removes Lewis-bound NH3; comparisons with aqueous ammonium exchange, IR and n-propylamine titration are discussed. | NH3-free aging sham controls or recovery of the next-cycle durability of aged CHA. The dry-versus-wet purge comparison concerns adsorption selectivity, not dry treatment as a healing intervention. |
| S15–S16, Schemes S1–S3 | Titration sequence and the repeated aging/titration/TPD/air-treatment loop. | A control branch that omits the assay or varies its frequency while holding the relevant exposures fixed. |
| S17–S20, Figures S9–S11 | NH3 TPD profiles versus cumulative steam time; peak shifts and tailing are explained through readsorption/packed-bed effects. | An independent time-resolved Al recovery measurement or comparison with unassayed specimens. |
| Section S5, S21; Figures S12–S14, S22–S23 | Framework Al is obtained from NH3 uptake; extra-framework Al is **calculated as total ICP Al minus NH3-derived framework Al**. | Independent structural verification of the evolving EFAl inventory. These plots cannot independently identify or time an aggregation intermediate. |
| Sections S6–S8, S24–S51 | Fits, residuals, analytical derivatives, reaction orders and comparisons among temperature, pressure and starting composition. | A new measurement-history control. Robustness across empirical fits addresses a different uncertainty. |
| Section S9, S52–S57 | Literature-motivated reversibility assumptions and candidate rate-law derivations, including quasi-equilibrated upstream steps in the association-limited models. | A measured recovery time or a demonstrated high-temperature dry recovery route. S52 explicitly notes missing evidence for reinsertion of fully extra-framework monomers or reversal of dimers under the studied conditions. |
| Section S11, S62–S63 | Discussion of water's effects on hydrolysis, Al speciation, diffusion and silanol nests, with unresolved alternatives. | Experimental separation of those effects during recovery bouts. |
| Section S12, S64 | TPD measurements on three different packed beds estimate concentration uncertainty, followed by error propagation. | Independent replicas of an uninterrupted-versus-repeated-assay causal contrast. |

The appropriate revision is to credit the paper's existing validation: **the question is whether a selective, explicitly recovery-capable assay changes the subsequent state trajectory, not whether the authors ignored Lewis-bound NH3 or failed to validate acid counting.** Selective measurement of the defined endpoint and a nonperturbing measurement history are separate properties. Existing validation of the former does not settle the latter.

### Reproduction detail to resolve before commissioning

There is a visible temperature-label discrepancy. SI Scheme S3, S16, labels air-treatment steps (a) and (e) at **773 K**; the main paper p.4 specifies a **873 K** pre-aging dehydration hold. SI Scheme S1, S15, separately specifies **723 K** before NH3 saturation, consistent with the main H-form assay description. Do not silently combine these into a claimed exact reproduction. Define the chosen A-arm timeline explicitly, use the same actual timeline for the sham, and seek clarification of the 773/873 K discrepancy before claiming replication of the published treatment. This documentation issue does not show that the reported kinetics are wrong and does not itself establish novelty.

**Recommendation after SI review:** retain the bounded assay-transferability campaign. The SI strengthens the rationale for the common terminal assay and sharpens the distinction between endpoint selectivity and treatment-history effects. It supplies no demonstrated dry-recovery timescale, so the pulse/application branch remains conditional.

## Priority update after the 2017 and 2025 primary papers

**Priority narrows further: retain a conditional validation pilot, not a broad “measurement changes durability” program.** These papers lower the novelty of an initial positive contrast. They do not settle whether serial H-CHA acid assays change subsequent steaming kinetics, but the difference in material/protocol is insufficient by itself to make that result consequential.

**Albarracin-Caballero et al., 2017:** I read publisher full-text methods and relevant results, particularly Sections 2.3–2.4 and 3.5–3.6. The comparison includes fresh, hydrothermally aged, and aged-then-SCR-exposed Cu-zeolites. Subsequent SCR changes Cu spectra in CHA and RTH despite little change in bulk framework metrics; RTH also loses detectable acid response. This directly establishes that reaction testing can change aged catalysts. It does not isolate NH3 from the complete SCR feed, nor test repeated H-CHA acid assays before further steaming. The distinction is between a known post-aging state change and a still-untested effect of assay frequency on future damage. [Primary article, 10.1039/C6RE00198J](https://pubs.rsc.org/en/content/articlehtml/2017/re/c6re00198j).

**Madeo et al., 2025:** I read the full PDF's relevant results and methods, especially pp.6–9, 16–17, 20–21 and 25–26. Ammonia protection is tested by adding NH3 **during** steaming (Figure 7, p.7). Separately, already-steamed samples receive aqueous autoclave treatment before activity/speciation measurements (Table 3, p.9; Table 9, p.17); methods include sequential water treatments and ammonium exchange before NMR (p.25). This is substantial recovery and measurement-conditioning prior art. It does not report a matched serial-NH3-assay/sham comparison followed by another steam interval. Its activity and Al-speciation changes also reinforce that more framework-assigned Al need not mean better catalytic function. [Primary article](https://www.mdpi.com/2073-4344/15/12/1130); [publisher PDF, 10.3390/catal15121130](https://mdpi-res.com/d_attachment/catalysts/catalysts-15-01130/article_deploy/catalysts-15-01130.pdf).

### Required threshold for further priority

The additional knowledge must be more specific than ammonia interaction, recovery, or state changes during testing:

1. Identify a reproducible **carryover into the next steam interval** after defined common removal of residual NH3, with the thermal/water sham retained. Otherwise protection by remaining ligands may reproduce the known cofeed result. Verify residual nitrogen/NH3 removal to the attainable detection limit; do not simply assume a purge erases ligation.
2. Show that explicitly representing assay history materially improves prediction of future working function or recoverable capacity for a withheld assay spacing, relative to calibrated cumulative-aging and heterogeneous-loss models. Report failure as well as improvement; model flexibility alone does not count.
3. Alternatively, establish a changed durability ranking using at least two genuinely relevant materials under both histories, with uncertainty sufficient to resolve the ranking. One material at two schedules cannot support a ranking claim. A reversal is not required; a robust change that affects selection is the relevant criterion.

A/B/C is still the appropriate economical first comparison. If only an immediate response changes, or if the later trajectory needs no history term after measured residual ligands and exposure differences are accounted for, stop at protocol validation. A specialist characterization campaign would not rescue weak novelty.

Do not designate any functional probe “nonperturbing” at this stage. For the proposed small-alcohol assay, commission contact-time and cumulative-probe-dose dependence on separate H-CHA aliquots and track generated water. If the earliest reproducible rate depends materially on assay dose or conditioning, report a conditioned functional endpoint rather than an unperturbed working-state measurement. The program can begin with operational capacity and next-interval behavior while that functional measurement is validated.

## 2026-09-16 update: uploaded prior art and current recommendation

The earlier abstract-only and missing-artifact statements above describe their original review dates. The focal SI was subsequently checked in the earlier SI addendum; Wouters 1998/2001, Agostini 2010, Nielsen 2015, Luo 2018 and Ladshaw 2022 are now available locally and their relevant primary passages have been read. The [post-upload audit](post-upload-cha-styrene-audit.md) records original-PDF locators. **Retain a conditional assay-transferability pilot; these sources do not establish persistent assay carryover or a usable dry-recovery window.**

Luo's [original PDF](../../literature/papers/luo2018-nh3-tpd-methodology-for-quantifying/original.pdf), pp.5–6, tests 700 °C/2 h and 600 °C/24 h in opposite orders on two Cu/SSZ-13 cores. Both receive intermediate NH3-TPD before the same cores undergo the next aging step. Final TPD ratios and catalytic activity are similar. This supports cumulative aging in the tested mild Cu-redistribution regime, but does not compare a repeated assay against a sham or an unassayed history. It is stronger contrary evidence than the original abstract-level account and leaves the proposed H-CHA A/B/C contrast unresolved.

Ladshaw's [original PDF](../../literature/papers/ladshaw2022-measurement-and-modeling-of-the/original.pdf), pp.8–10, predicts aged Cu-SSZ-13 storage transients with adsorption kinetics fitted to the de-greened state and updated age-dependent site densities. A generic aging/storage model is therefore insufficient novelty. The contribution must be consequential prediction across **different assay schedules** beyond cumulative-aging or population-change baselines. The fitted densities are not independent atomic counts.

Wouters' [1998 paper](../../literature/papers/wouters1998-reversible-tetrahedraloctahedral-framework-aluminum-transformation/original.pdf), p.7, and [2001 paper](../../literature/papers/wouters2001-steaming-of-zeolite-y-formation/original.pdf), p.5, reinforce the distinction between coordination response and framework connectivity. Agostini's [primary paper](../../literature/papers/agostini2010-in-situ-xas-and-xrpd/original.pdf), p.11, reinforces the active role of water readsorption during cooling in NH4-Y. The existing thermal/water sham, residual-nitrogen check and separate functional specimens remain necessary. None of these Y-zeolite findings supplies numerical H-CHA damage or recovery kinetics.

Nielsen's [2015 primary paper](../../literature/papers/nielsen2015-kinetics-of-zeolite-dealumination-insights/original.pdf), p.8, computes H-SSZ-13 kinetics but improves comparison with experimental **H-ZSM-5** rates. Its later-hydrolysis rate-control prediction is conditional on its model and water reference; it is not a measured CHA recovery time. Read alongside the 2019 cooperative-water calculation, it strengthens the need to match local water history without assigning one universal rate-controlling hydrolysis step.

The first campaign should still compare complete assay, matched NH3-free sham and uninterrupted histories at matched damaging wet exposure, with common final capacity measurements and separately commissioned functional readouts. Continue only for a resolved next-interval effect after residual ligand and exposure controls, followed by a held-out schedule prediction or a consequential material-ranking test. A familiar immediate uptake change is insufficient. A null result bounds the intervention benefit within tested conditions; it does not uniquely determine an intermediate lifetime. The current program already states these gates, distinct confidence judgments and practical limits.
