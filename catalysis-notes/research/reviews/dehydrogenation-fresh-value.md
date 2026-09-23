# Independent review: a finite Ga regeneration study, with a sharper decision test

Reviewed 2026-09-16. No experiments. This fresh review examines the [PDH opportunity screen](../working/dehydrogenation-consequential-screen.md), the original Wu and Malizia articles and newly recovered supporting information, and both patent originals. It also resolves a requested Pt–Sn benchmark unit discrepancy. This sentence records the original review scope. **Post-upload update, 2026-09-16:** the [subsequent audit](post-upload-pdh-ammonia-audit.md) independently checked the modern benchmark histories; the [working screen](../working/dehydrogenation-consequential-screen.md) now incorporates them and specifies the final minimum campaign.

## Decision

**Retain the conditional finite study; do not promote a substantial Ga program yet.** The chemically sound question is whether a regeneration endpoint based on useful recovery can improve complete-cycle propylene production on a competitive Pt/Ga material, and whether a measured chemical state predicts that choice under a different aging history. The source review strengthens the need to distinguish oxygen uptake from Ga reoxidation, but does not establish that the published inventory is materially wrong.

The strongest specific opportunity is a **history-dependent failure of the ordinary regeneration rule**: two spent states require different oxidation treatments to recover useful output even though their bulk carbon or gross oxygen consumption would prescribe the same treatment. Conversely, two treatments could produce the same useful recovery with different oxidation severity. A finite comparison can find or reject such a consequential distinction. Its value does not depend on already having a successful experiment. Correcting an oxygen balance alone, finding another hydrogen reservoir, or improving a weak catalyst while the strong reference already solves the problem would not meet the substantial-program goal.

Direct precedent is closer than the screen's brief patent summary suggests. Chlorine-assisted oxidative conditioning, enriched-oxygen reactivation despite little coke, and separating metal oxidation from carbon removal are all disclosed. The original opportunity therefore needs a predictive operating decision, not a claim to have discovered that coke removal and reactivation differ.

## 1. Wu's exact SI is now available: the reported balance omits other oxygen sinks

[Wu et al., 2025, DOI 10.1002/anie.202506704](https://doi.org/10.1002/anie.202506704), main p. 3 and SI pp. 2, 6, explicitly define the oxygen assigned to coke as the amount of CO2 formed and assign the difference from total O2 consumption to catalyst reoxidation. The exact SI was recovered through the lawful Europe PMC supplementary-files endpoint. Thus the absence of an H2O/CO term **in the reported calculation** is now verified, rather than merely inferred from an unread supplement. This does not prove that those species were significant or that no unpublished controls existed.

SI p. 2 specifies 100 mg spent catalyst, an 800 mg SiC layer above it, 550 °C in Ar, a 1 mL loop containing 1 vol% O2/He, and approximately one minute between manually applied pulses. The stated analysis channels are 32 for O2 and 40 for CO2. The latter is an apparent reporting error: 40 is also the Ar carrier channel, and the separate TAP methods correctly identify CO2 at 44. **Do not infer that the actual experiment measured CO2 incorrectly.** It does mean that raw signals, calibration and blank definitions would be needed to reproduce the reported inventory.

### What the balance can and cannot establish

For a deposit containing `x` C atoms, `y` H atoms and `z` O atoms, completely removed as CO2 and H2O, its O2 requirement is

`x + y/4 − z/2`.

Consequently, `O2 uptake − CO2 production` can include hydrogen oxidation, subtract oxygen initially carried by the deposit, and include oxidation or adsorption elsewhere on the catalyst. Formation of CO also changes the residual. For an oxygen-free inlet other than O2, a closed gas balance gives

`ΔO_solid = 2 O2_consumed − 2 CO2_out − CO_out − H2O_out − other_outlet_O_atoms`.

Amounts are integrated over the same boundary and time interval; any oxygen-bearing inlet must be included. `ΔO_solid` is the change in **all retained oxygen**, including the support and adsorbates. It is not the oxygen restored specifically to productive Ga centers. Hydroxyl condensation, adsorbed water, initially oxygenated deposits, and changes during specimen transfer or purge matter. Capturing a water peak without quantitative recovery and appropriate blanks would not solve the attribution.

The main paper reports residuals of 0.42, 0.97 and 1.30 µmol O2. Oxidation of 1.68, 3.88 and 5.20 µmol retained H atoms would consume those amounts. At the stated 100 mg specimen mass, these correspond to approximately 0.0017–0.0052 wt% H. These are **analytical equivalences, not measured deposits or a claim that this hydrogen survived the actual preparation and purge**. They justify a sensitivity requirement; they do not quantify an error in the published Ga inventory.

SI Fig. S2, visually checked against the original, also requires qualifications:

- Its middle aging condition is labeled **10 min**, whereas the main text describes **12 min**. Preserve the discrepancy; do not silently select a time for a quantitative history model.
- The plotted residual per pulse remains positive in the late pulses. The figure does not provide a raw blank/integration procedure sufficient to independently reconstruct the reported total. This is a replication question, not proof of erroneous baseline subtraction.
- SI p. 2 says a spent specimen was placed in the titration reactor and heated in Ar. Transfer exposure, elapsed storage and purge history are not sufficiently specified there to establish that every measured species represents the immediate working surface.

The paper also provides independent reduction, spectroscopy, activity and structural evidence. A nonselective titration does not invalidate those results. Likewise, lack of correlation between **bulk carbon** and conversion cannot exclude a small, chemically distinct blocking carbon population, but does not demonstrate that such a population exists.

## 2. The transient argument is stronger than peak order alone, but not uniquely rate control

Wu SI pp. 3 and 16–17 describes the TAP experiment and a transport calculation. In a three-zone reactor, the model makes H2 and propylene simultaneously from a common adsorbed precursor and includes Knudsen diffusion. Across three parameter choices, the simulated ratio `tmax(H2)/tmax(C3H6)` is approximately 0.47–0.54; the observed ratios are higher. Original Fig. S13 was visually checked.

This is a useful null-model comparison: molecular-mass-dependent transport alone in that model does not explain the observed H2 delay. It supports additional hydrogen residence or slower hydrogen release. It does **not** uniquely establish that the delayed population controls steady-state propylene turnover. Hydrogen exchange with a nonproductive reservoir, readsorption, and differences between pulsed vacuum and flowing reaction conditions remain possible explanations that require actual modeling and tests. The article's DFT and activity correlations are additional support, not substitutes for distinguishing these alternatives.

The best finite regeneration study need not reopen every elementary-step assignment. If hydrogen removal is central to a consequential endpoint, compare a minimal exchange-reservoir model with the productive-state model using the same transport description, pulse amplitudes, product balances and steady rates. A free additional time constant that merely improves a fit would not establish a new mechanism. Deuterated propane is a later discriminator because support OH exchange and kinetic isotope effects complicate attribution.

## 3. Durability and productivity need their original time bases

Wu main pp. 6–8 reports 45 cycles, generally 20 min reaction and 20 min oxidative regeneration, with a 60 min regeneration intervention for the impregnated catalyst. Main Fig. 5 calls its values initial conversion but says they were measured after 20 min on propane. The SI confirms air regeneration and gives conversion and selectivity histories in Fig. S14.

**Fig. S14 spans 81 h and shows multiple points within each reaction segment.** This is not reconstructed by `45 × (20 + 20) min`, even with the stated longer regeneration. The original figure and caption were checked visually. Unknown additional time, measurement scheduling or a reporting inconsistency cannot be resolved here. Therefore do not convert its nominal segments into observed full-cycle productivity, or call all 81 h productive operation. The screen's 20/40 versus 20/25 duty-factor example remains a mathematical illustration only.

The mixed-oxide catalyst retains a strong advantage in the reported sequence. Yet Fig. S14 shows within-segment conversion loss, especially at higher temperature: repeatable restoration of an early-cycle value is not constant production throughout each segment. SI Table S1 gives, at 550 °C, 26.0% propane conversion, 93.0% propylene selectivity, and 8.70 kg propylene kg-catalyst−1 h−1. The figure's ratio to equilibrium is about 0.62; this is not 62% absolute propane conversion. The 600 and 625 °C entries have different conversion/selectivity, and none is a complete-cycle average.

The strong mixed-oxide material has 8 wt% nominal Ga, whereas the principal impregnated comparator has 2 wt%. Both have 0.05 wt% Pt. They are appropriate competing materials, but their difference is not a preparation-only causal contrast. Use a matched-Ga pair only if that causal assignment becomes necessary; do not add an entire synthesis matrix before a consequential cycle comparison exists. The published loading series already constrains simplistic interpretations.

## 4. Prior art already targets the practical endpoint

### Chlorine-assisted conditioning: US10654035B2

The [original patent](https://patents.google.com/patent/US10654035B2/en), columns 13–14 and Fig. 1, goes beyond separating combustion, air soak and stripping. Its specific intervention adds a chlorine source during oxidative conditioning; examples use **21 or 61 ppm monochloroethane**. The example catalyst contains 1.6 wt% Ga, 0.25 wt% K and 200 ppm Pt on silica-modified alumina. It reports shorter air-soak times at matched propane conversion.

The experimental sequence uses 2 min reaction at 620 °C, simulated combustion products at 730 °C, and five air-soak durations. Conversion is reported **after 20 s** of reaction, after 30 cycles at the selected soak time. Three intervening cycles with 20 min air soaks reactivate the material between duration tests. Thus the disclosure supplies direct shorter-conditioning prior art, but not an integrated equal-output comparison or a unique explanation of chlorine's role. This is a scientific prior-art assessment, not an opinion on legal claim scope or permission to practice it.

### Enriched oxygen despite little coke: US20220126281A1

The [original application](https://patents.google.com/patent/US20220126281A1/en), Examples 1–7 and Tables 1–2, discloses 76 ppm Pt, 1.56 wt% Ga and 0.26 wt% K on silica-containing alumina. The **630 cycles are sample aging** before the endpoint comparison, not 630 cycles of equal measured performance. Subsequent examples compare four short cycles with conversion reported near 0.65 min; one protocol includes a 60 min wet pretreatment before propane exposure. Oxygen concentration is reported on a dry-gas basis before steam addition.

Examples 6 and 7 alter flow, water and CO2 as well as oxygen conditions. They are not a clean independent oxygen effect. Example 6 says 700 °C in prose while Table 2 says 720 °C; the discrepancy is present in the original. Carbon near or below a 0.05 wt% detection limit is evidence of low **bulk** carbon, not absence of carbon on every active site. These limitations leave a mechanistic question, but do not restore originality to “shorten oxidation on a low-coke Ga catalyst.”

### Coupled spectroscopy and carbon/redox separation: Malizia 2025

[Malizia et al., DOI 10.1021/acscatal.5c00593](https://doi.org/10.1021/acscatal.5c00593), recovered manuscript regeneration section and Figs. 6–7, directly couples gas responses with optical signatures. It distinguishes early Cr oxidation from slower carbon removal, including CO2 release after gaseous O2 is gone and accompanying Cr reduction. This is strong methodological prior art for chemically resolved regeneration.

Its exact SI adds useful boundaries. The catalyst is an industrially relevant 13.2 wt% Cr/alumina preparation, preconditioned by three H2/O2 cycles. Gas fragmentation and pulse-size calibrations are described. SI Fig. S8 explicitly labels its water signal uncalibrated and qualitative; the method therefore should not be cited as already demonstrating a complete quantitative hydrogen balance. SI pp. 8–11 and Figs. S4–S7 also examine oxygen storage/exchange not assigned to the Cr3+/Cr6+ transition, with alumina controls. This reinforces why total oxygen uptake is not automatically a metal-valence census. It does not establish the same reservoirs on Ga.

## 5. Strongest experiment and clear stopping rule

Start with a working strong mixed-GaAlOx catalyst and the conventional impregnated reference. The latter supplies a useful failure mechanism; the former determines whether the proposed intervention still matters practically.

1. **Establish the complete-cycle decision.** Compare documented oxidation with one credible shorter treatment and an established stronger oxygen policy. Include induction, purge, heating/cooling, propylene loss, cracking, gas use and measured bed temperature. A chlorine-conditioned reference is relevant prior art; it need not be experimentally added unless composition compatibility and a specific decision require it. Set the smallest useful improvement from measured platform precision and a stated operating burden before interpreting differences.
2. **Prespecify two controlled aging histories and reserve the second.** Choose reaction duration or product/H2 exposure, keeping other conditions matched. Establish the initial useful contrast among regeneration policies only on the first history. Do not measure second-history complete-cycle outcomes or use them to select the model or policies. Use separate specimens or independently reproduced first histories for partial endpoints because a propane assay changes the specimen.
3. **Only then test state discrimination on the first history.** Measure calibrated O2/CO/CO2/H2O balances and a defensible redox marker. Seek either equal bulk carbon/gross uptake but different useful recovery, or equal recovery at different unnecessary oxidation costs. Match initial/final boundaries and test specimen-transfer and water-recovery blanks. Distinguish persistence over the observation window from irreversible restructuring.
4. **Predict the reserved second history.** Compare a simple oxygen-dose/temperature policy with the proposed state relation using the first-history data. Freeze the model, candidate policies, decision margin, integrated-output predictions and selected endpoint before measuring any second-history complete-cycle outcome. An operational correlation can be useful before a selective Ga site count is available, but it should not be advertised as a unique productive-site census.

**Kill criterion:** stop expansion if the strong reference plus a simple established oxygen policy achieves equivalent useful output at acceptable resources across both histories, or if the corrected state variable cannot predict a different, useful decision beyond experimental uncertainty. Also stop the mechanistic branch if a quantitative water/oxygen balance is not recoverable at the relevant inventory size; preserve the resulting bound rather than assigning all residual uptake to Ga. A reproducible analytical correction without changed catalytic or operating consequence warrants a smaller methods result.

A positive result would justify a broader Ga study only if the new relationship survives a new history and materially improves a competitive complete cycle. Reducing bench downtime does not directly predict plant throughput: a circulating unit may instead change regenerator volume, catalyst inventory or circulation rate, and heat delivery must still close.

## 6. Requested benchmark correction: Cheng's 95.4 is normalized to Pt

[Cheng et al., 2025, DOI 10.1038/s41467-025-61182-6](https://doi.org/10.1038/s41467-025-61182-6), original main pp. 5–6, 10, Fig. 4e, and SI Table 2, resolves the apparent feed-capacity violation. **95.4 has units mol propylene g-Pt−1 h−1.** The introduction incorrectly gives g-catalyst in both PDF and HTML. The results, original plot axis, activity equation and SI table consistently use the Pt denominator.

At nominal 0.4 wt% Pt, the value corresponds to a calculated 0.3816 mol propylene g-catalyst−1 h−1, approximately 16.0 g g-catalyst−1 h−1. SI Table 2 separates the operating histories:

| Condition | Reported history | Comparison implication |
|---|---|---|
| 600 °C; total flow 85.7 L g-catalyst−1 h−1; propane flow 17.1 L g-catalyst−1 h−1 | 12.1 h; conversion 55.0→33.9%; propylene output 95.37→58.61 mol g-Pt−1 h−1 | High initial productivity with substantial decline; not 120 h retention at 95.4. |
| 550 °C; total flow 9.6 L g-catalyst−1 h−1; propane flow 0.96 L g-catalyst−1 h−1 | 120.5 h; conversion 59.2→55.7%; output 5.72→5.43 mol g-Pt−1 h−1 | Longer endurance at a different temperature and substantially lower throughput. |

These are reported catalyst tests, not full process comparisons. The authors' inverse deactivation coefficient is a fitted metric, not a measured catalyst lifetime. This correction does not diminish the material's useful performance, but prevents combining its strongest rate and strongest durability into a nonexistent experiment.

## Confidence

- **Scientific:** high confidence in the oxygen-accounting distinction and direct prior-art boundary. Low-to-moderate confidence that omitted hydrogen materially changes the Wu assignment. Moderate plausibility that Ga reactivation, retained species and Pt restructuring can be separated under at least some histories.
- **Experimental:** moderate, conditional on an existing PDH platform. Complete-cycle comparison is more accessible than micromole water recovery or selective characterization of dilute productive sites. Neither facility access nor successful material reproduction is established.
- **Practical:** low present confidence in a consequential improvement. The proposed finite test is informative precisely because a strong material, established conditioning, or heat integration could remove the opportunity.
- **Originality:** provisional. A useful, validated history-dependent endpoint could add knowledge and capability; an additional oxygen subtraction or another optimized air soak would not.

## Source recovery and sole-worker handoff

All recovered originals below were sent to `/root/literature` for sequential `$lit` **Add identified literature** promotion. Skill: `/home/sgusev/repo/skills/literature/SKILL.md`; project: `/home/sgusev/repo/catalisys-notes`; KB: `/home/sgusev/repo/catalisys-notes/literature`. This reviewer did not edit the KB or run its check.

- Wu exact SI: `/tmp/pdh-fresh-review/wu-supp/ANIE-64-e202506704-s001.pdf`, 1,412,218 bytes; source [Europe PMC supplementary-files endpoint](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12304820/supplementaryFiles). Retrieved through `lit.py get`; exact identity also checked against article XML. Text: `/tmp/pdh-fresh-review/wu-si.txt`. Methods, S2, S12–S14 and Table S1 read; original S2, S13, S14 and methods visually inspected.
- Malizia exact SI: `/tmp/pdh-fresh-review/malizia-si.pdf`, 3,977,424 bytes; [ACS Figshare original](https://ndownloader.figshare.com/files/53862703), article 28835692. Relevant methods and oxygen-storage/regeneration sections read. This is selective scientific reading, not a claim to have checked every SI figure.
- US10654035B2 original: `/tmp/pdh-fresh-review/US10654035B2.pdf`, 1,629,511 bytes; [patent PDF](https://patentimages.storage.googleapis.com/c7/08/10/2642fe18e55e57/US10654035.pdf). Description and examples read.
- US20220126281A1 original: `/tmp/pdh-fresh-review/US20220126281A1.pdf`, 1,210,911 bytes; [patent PDF](https://patentimages.storage.googleapis.com/85/f3/36/262d6c87fd8b62/US20220126281A1.pdf). Description and Examples 1–7 read.
- Cheng main: `/tmp/pdh-fresh-review/cheng2025.pdf`, 2,981,547 bytes; [publisher original](https://www.nature.com/articles/s41467-025-61182-6.pdf). SI: `/tmp/pdh-fresh-review/cheng2025-si.pdf`, 2,631,809 bytes; [publisher SI](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-025-61182-6/MediaObjects/41467_2025_61182_MOESM1_ESM.pdf). Relevant performance/methods and Table 2 read; main Fig. 4e visually inspected. Broader isotope/mechanism evidence was not independently reviewed. A KAUST request returned HTML and was not used as full text.

No new bibliographic work was added to the screen's queue by this review; it supplies originals for existing requests. Wu raw MS calibrations, specimen-transfer detail and the complete 81 h timing record remain unavailable here. These are unresolved experimental-documentation questions, not missing SI. The post-upload audit closes the prior main-text access gaps for Lu, Xu, He, Hong and Sun, and the screen now lists current KB status for the other references. Do not retain those main articles on a missing-source list. Supplement availability and raw experimental documentation require separate checks.


## Post-upload implementation: comparator and stopping refinements

The original mechanistic conclusion above is retained. The full texts now require the following concrete benchmark boundaries:

- Lu's >300 h is cumulative reaction through six regeneration cycles; the figure reports cycle-start productivity. Later regeneration includes 10 h air calcination and 2 h H2 treatment, plus thermal and purge overhead.
- Xu's 4500 h test is at 550 °C and WHSV 5.3 h−1, with 28.4% actual conversion. Its higher-throughput result is a separate condition. “91% equilibrium conversion” is not 91% feed conversion.
- He's 5000 h is a sequence of feeds and temperatures with an explicit H2 regeneration; the separate twenty-cycle experiment uses 50 h reaction/2 h H2 treatment and relocates carbon downstream.
- Hong's regenerative Pt atom/cluster transformations and Sun's material-specific hydride interpretation are now grounded in available main texts; neither constitutes a novel generic intervention for this proposal.

The [final screen](../working/dehydrogenation-consequential-screen.md#minimum-campaign-and-stopping-decisions) defines the minimal comparison: independent preparations, ordinary-cycle scatter and a useful contrast set before testing, two prespecified spent histories, documented/shorter/best-simple regeneration policies and complete gas/heat/time accounting. Use the first history for the initial comparison and model fitting; freeze the model, policies, decision margin and predictions before measuring the second history’s complete-cycle outcomes. This preserves a prospective held-out policy test. Stop before spectroscopy when the strongest material or a simple policy removes the useful difference. Stop a site-inventory claim when calibrated water/oxygen recovery cannot resolve its relevant size. These gates finish the existing proposal without creating another PDH direction.
