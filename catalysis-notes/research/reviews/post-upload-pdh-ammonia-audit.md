# Post-upload audit: PDH and ammonia

Reviewed 2026-09-16. Bounded reassessment of the existing proposals; no new research direction or experiment. This review does not edit the knowledge base. **Implementation update, 2026-09-16:** the findings below have now been applied to both working screens and their independent reviews. Each screen includes its completed minimum experimental campaign, practical comparison boundary and stopping decisions. “Required change” below records the audit finding rather than an outstanding research-file edit; KB repairs remain the sole literature worker’s responsibility.

## Decision

**Yes: substantive corrections and better comparisons are needed. Neither direction should be promoted to a substantial research program on this evidence.** The new texts strengthen the need to compare complete operating histories and attainable hydrogen separation conditions. They also remove several source-access uncertainties that the current screens still describe as unresolved.

- **PDH:** retain the conditional Ga regeneration study, but replace headline durability comparisons with the actual reaction/regeneration schedules. The modern Pt benchmarks are strong, with distinct productivity, stability and regeneration tradeoffs. None makes a selective Ga-state census unnecessary by itself; none establishes that a new Ga census would improve useful output.
- **Ammonia:** retain the narrow oxygen-probe-to-oxygen-free-rate validation question only if it changes an attainable operating decision. Full-text Itoh and Napolitano establish actual membrane benefits at finite pressure. Qiu2025 explicitly describes the limits of its hydrogen-rich rate law; Coelho's model preference is a reanalysis of a different catalyst dataset. These results strengthen existing cautions and reduce any residual generic kinetic-model novelty claim.

Confidence is high in the textual and accounting corrections below. Confidence that the proposed experiments would produce a useful practical improvement remains lower and platform-dependent.

## Evidence checked

Read the current `paper.md` and relevant full-text sections for Lu2026, Xu2025, Hong2025, He2025, Sun2024, Itoh2014, Qiu2025, Napolitano2025, Coelho2025 and Coelho2026. Important numbers and definitions were checked against freshly extracted original PDFs. Original figures were also inspected visually for Lu Figures 3 and associated regeneration discussion, Xu Figure 3, He Figures 3–4, and Napolitano Figures 6–8. Page numbers below refer to PDF pages unless a journal page is specified. Supporting information was not assumed available merely because the main article is now read.

## 1. PDH benchmark corrections

### Lu: cumulative reaction time and initial productivity are not complete-cycle output

The [current screen](../working/dehydrogenation-consequential-screen.md) reproduces the abstract-level statement of approximately 1 mol propylene gcat−1 h−1 for more than 300 h with air regeneration. The full text now permits a much more precise statement:

- Pure propane, 550 °C, WHSV 165 h−1; initial productivity about 1.17 mol gcat−1 h−1, remaining above 1 for at least 60 h.
- More than 300 h of **reaction** across six regeneration cycles. Figure 3c shows the initial productivity after each cycle, rather than an uninterrupted production trace or elapsed-cycle average.
- After the initial 100 h reaction, regeneration used 1–2 h air calcination at 500 °C. Later calcinations were extended to 10 h. Figure 3 explicitly adds pure-H2 treatment at 600 °C for 2 h after calcination. Methods also include cooling, purging and reheating.
- At WHSV 660 h−1, the study used 10 h reaction segments and overnight regeneration; the reported reaction productivity ranged from high initial values to above 1.5 mol gcat−1 h−1 over the cumulative test. These are still strong reaction results, but not demonstrated whole-cycle averages.

Source: [Lu main](../../literature/papers/lu2026-subnanometre-ptsn-alloyed-clusters-encapsulated/original.pdf), pp.4–6 and regeneration methods. DOI [10.1038/s41929-026-01538-3](https://doi.org/10.1038/s41929-026-01538-3).

**Required change:** replace the unresolved-main label and specify cumulative reaction hours, initial versus time-resolved productivity, and the full regeneration sequence. Do not infer a corrected average without the full time histories. This supports the existing demand for complete-cycle accounting; it does not establish that Ga is a better material.

### He: the 5000 h claim is a mixed operating history

[He's original Figure 3](../../literature/papers/he2025-ultradurable-regenerative-propane-dehydrogenation-catalyst/original.pdf), p.4, shows a history spanning about 5000 h: an initial diluted-propane/H2 segment at 600 °C, an explicit H2 treatment near 1200 h, and subsequent pure-propane segments at several temperatures from 550 to 600 °C. It is neither 5000 h at one fixed condition nor a 5000 h uninterrupted pure-propane test. The text on p.5 gives a decline from 62.7% to 50.1% conversion over the first 1200 h before recovery by H2 treatment.

Figure 4 is a separate, clearly specified test: twenty 50 h pure-propane reaction segments, with 2 h H2 regeneration at 600 °C, WHSV 28 h−1. The downstream quartz collects carbon during this treatment. Catalyst regeneration therefore does not by itself close the whole-reactor carbon handling problem. DOI [10.1021/jacs.5c11524](https://doi.org/10.1021/jacs.5c11524).

**Required change:** replace the screen's “original time history needed” with this resolved qualification. In the KB note, distinguish direct post-test microscopy at the stated sampled times from the full 5000 h performance history; do not imply a 5000 h microscopy measurement merely from prolonged stable operation.

### Xu: long continuous stability is real, but at a different productivity boundary

[Xu Figure 3](../../literature/papers/xu2025-pt-migrationlockup-in-zeolite-for/original.pdf), pp.3–4, reports 4500 h on stream at 550 °C, pure propane, 1 atm and WHSV 5.3 h−1, with about 28.4% conversion and 98.3% selectivity. The stated 91% is the ratio to equilibrium conversion, **not 91% propane conversion**. The expected lifetime of 4.6 × 10^5 h is an extrapolation, not observed operation.

The separately reported 18.7 kg propylene kgcat−1 h−1 uses 0.37 wt% Pt at 600 °C and another operating condition. It must not be combined with the 4500 h test as if achieved simultaneously. The authors themselves identify synthesis requirements and cost as barriers to industrial use. DOI [10.1038/s41586-025-09168-8](https://doi.org/10.1038/s41586-025-09168-8).

**Required change:** replace the abstract-only row with these conditional benchmarks. The long-term stability result is substantial and should not be dismissed because Lu has a much larger mass-specific reaction rate under a different feed rate.

### Hong and Sun: stronger prior-art grounding, not a contradiction

[Hong2025](../../literature/papers/hong2025-a-self-regenerating-pt-ge/paper.md) now provides full-text support for reversible Pt cluster/single-atom transformation during reaction and oxidation, repeated recovery, and kilogram-scale preparation. This strengthens the existing conclusion that generic redispersion or atom/cluster cycling is occupied territory. Cycle count still does not establish a matched process advantage over Ga.

[Sun2024](../../literature/papers/sun2024-metastable-gallium-hydride-mediates-propane/paper.md) now provides spectroscopy, hydrogen-order, isotope and computational evidence for beneficial hydride chemistry on reduced GaOx/Al2O3. The screen should replace “primary abstracts only” for this source. It should continue to distinguish that material and coverage regime from inhibitory hydrogen on other Ga systems. The KB phrase that isotope effects “exclude H2 desorption” should be attributed to the authors' interpretation and limited to the tested kinetic regime; an inverse isotope effect is not a universal exclusion of hydrogen-release involvement.

### Consequence for the existing Ga experiment

Keep the strong mixed GaAlOx material and the patent-informed simple regeneration policies in Stage A. Before expanding spectroscopy, assemble one comparable operating record for the relevant external Pt benchmark: feed, catalyst/Pt inventory, instantaneous and integrated propylene output, regeneration and heat history, hydrogen use, and downstream carbon disposition. A headline competition among 300 h, 4500 h and 5000 h tests is uninformative. No new numerical performance hurdle is justified without matching the application boundary.

The Wu water/CO omission and productive-state-identification uncertainty remain scientifically valid. The new papers do not demonstrate that the omission materially biases Wu's measurements, nor that resolving it improves operation.

## 2. Ammonia corrections and sharper comparison

### Itoh: the finite-pressure kinetic enhancement is directly demonstrated

[Itoh2014 original](../../literature/papers/itoh2014-kinetic-enhancement-of-ammonia-decomposition/original.pdf), pp.2,5–6, resolves the previously uncertain percentage basis. At 723 K the reported comparison is approximately **73% to 87% NH3 conversion**, an increase of about 14 percentage points; the conclusion rounds the gain to about 15%. Hydrogen recovery reaches about 60%. The experimental membrane is about 200 μm thick, and the permeate is held at 0.001 MPa, or 1000 Pa, by vacuum. The much thinner 2 μm membrane improvement is a simulation.

Recovery in Eq.3 is permeated H2 divided by `1.5 × incoming NH3`, which is the theoretical H2 available from complete feed conversion. The paper also shows that candidate kinetic models predict different membrane gains, and distinguishes kinetic relief from near-complete equilibrium conversion.

**Required change:** remove the “full text missing / percentage basis awaits full text” labels from the screen and [independent review](ammonia-hydrogen-inference.md). Give the actual gain and pressure boundary. This is stronger prior art than an abstract-level conceptual overlap.

### Napolitano: useful atmospheric-permeate operation, with incompatible recovery denominators

[Napolitano2025 original](../../literature/papers/napolitano2025-enhanced-ammonia-decomposition-using-a/original.pdf), pp.3,6–8, uses a 4 μm Pd–Ag membrane, 25 cm² active area and 7 g of 4 wt% Ru/La2Ce2O7. The permeate is atmospheric; reaction tests use 400 °C and 3–5 bar feed pressure. Feeds combine NH3 with H2/N2 to simulate upstream partial cracking. Avoiding back-permeation and using more membrane area is a real, experimentally supported device consideration.

The reported approximately 85% conversion at 5 bar uses NH3/H2/N2 flows of 9/3.4/1.1 mL(STP) min−1. This is not evidence that the Qiu2026 Ru/MgAl2O4 surface reaches its ideal zero-H2 kinetic limit. It is evidence that a different catalyst/device can improve conversion while operating at finite hydrogen pressure.

Important qualifications now available from the full text:

1. Equation 5 defines recovery as permeated H2 divided by **all outgoing H2**, including inlet hydrogen. This differs from Itoh's feed-NH3-based denominator. Neither equals net newly produced, purified hydrogen per total catalyst or device inventory.
2. The compared conventional reactor uses pure NH3, whereas the largest membrane benefit uses an H2/N2-containing feed. The reported 3.6 conversion ratio is a combined configuration/feed result, not a matched-feed isolation of the membrane effect. The simulated upstream conversion must be included in any whole-train comparison.
3. “Purity always greater than 90%” in the abstract/conclusion is too broad: Table 5 gives 63–99%, and Figures 6–7 show approximately 60–70% purity for the pure-NH3 feed. The >90% claim belongs to selected mixed-feed cases.
4. The paper contains numerical inconsistencies requiring caution: for the nominal 9/3.4/1.1 mixed feed at 5 bar, Figure 6 shows recovery near 96%, whereas Figure 7 shows about 80%. Text says the 97% maximum occurs at 4 bar, whereas Figure 6 places its largest plotted value at 5 bar. These are visually checked reporting discrepancies, not resolved measurements. Do not silently choose the most favorable value or combine all maxima as a single demonstrated operating point.

**Required change:** update the now-obsolete “main unread” status and add these definitions. The KB note should correct its unqualified purity statement and should not state that the compared headline maxima establish one operating point.

### Qiu2025 and Coelho2025 do not establish competing universal mechanisms

[Qiu2025 original](../../literature/papers/qiu2025-kinetic-investigation-of-nh3-decomposition/original.pdf), pp.7–8, explicitly limits its simple NH3-first-order/H2-minus-1.5 law: it works best in hydrogen-rich feeds, while low-temperature H2-lean data expose neglected coverage terms. Some relative errors there reach 80–100%, although the reported average absolute conversion error stays within 6 percentage points. More elaborate fits have correlated adsorption parameters. The same main text p.7 reports successful description of commercial Heraeus Ru-catalyst measurements up to pure NH3 feed (Fig. S7). This is real high-NH3 validation, but generated H2 makes that reacting regime distinct from extrapolation to near-zero local H2. The separate low-GHSV Ru/MgAl2O4 reactor-sizing result in Figure 11 is a model prediction. The authors acknowledge that desorption may become controlling at lower temperature and that their fitted constant cannot separately identify the support effects on the elementary barrier and H adsorption.

[Coelho2025 original](../../literature/papers/coelho2025-hydrogen-production-via-ammonia-decomposition/original.pdf), pp.3,8–10, reanalyses raw data from Lundin2024 on a commercial **0.5 wt% Ru/Al2O3**, at 1 bar; the illustrated temperature domain includes 623.15–673.15 K. It is not an independent new experimental replication of Qiu's 1 wt% Ru/MgAl2O4 system. Model 5A1 gives the preferred fit under the tested comparison, but the authors explicitly acknowledge that additional parameters can improve fit without establishing mechanistic validity.

**Required change:** replace the current “two abstracts, full domains unread” paragraph with this material/domain distinction. Preserve the existing warning against claiming that one study disproves the other. The low-H2 validation requirement is now supported by Qiu2025's explicit domain limitation, not merely an external objection.

[Coelho2026](../../literature/papers/coelho2026-hydrogen-production-through-ammonia-decomposition/paper.md) is also now available. Its comparison couples non-isothermal reactor balances, pressure, feed/sweep conditions and membrane configuration under ideal H2 selectivity. Treat optimized conversion/recovery values as **model predictions**, not new experimental validation. The screen's insistence on a real pressure, purity and heat boundary is well justified, but that generic modeling task is not novel.

### Consequence for the existing ammonia experiment

Retain the calculated low-H2 thresholds solely as a conditional extrapolation of Qiu2026's empirical coefficient. The new finite-pressure membrane results do not violate the chemical-potential bound and do not validate that coefficient in the oxygen-free low-H2 regime. A useful comparison should use net newly produced H2, required purity, feed and permeate pressures, catalyst and membrane inventories, and actual upstream/sweep/compression burdens. First determine whether competing rate descriptions change an attainable device choice. Only then pursue the existing oxygen-free validation experiment.

## 3. Files and knowledge-base improvements

**Research files needing update:** the PDH and ammonia working screens; the source-status and prior-art passages in `dehydrogenation-fresh-value.md` and `ammonia-hydrogen-inference.md`; central literature-status and missing-source handoffs. Preserve old reviews as dated assessments, but clearly link this update so an old “unread” statement is not interpreted as current access status.

**Targeted KB repair:** Lu2026, Xu2025, Qiu2025, Coelho2025 and Coelho2026 have `status: read` but their current notes largely repeat introductory sentences and use generic “late-stage synthesis” and limitations text. They omit the crucial operating boundaries and distinctions above. Their available originals are useful; the notes need actual source-specific findings, quantitative conditions and caveats before they serve as reliable research summaries. Napolitano needs the particular corrections above. This is not a reason to downgrade all newly processed literature or reread every source indiscriminately.

The missing primary source identified by this audit, **Lundin et al.2024, “Modeling of an ammonia decomposition membrane reactor including purity with complex geometry and non-isothermal behavior,” DOI [10.1016/j.memsci.2023.122345](https://doi.org/10.1016/j.memsci.2023.122345)**, has now been added/read by the sole literature worker using the lawful DOE accepted manuscript. The [local source](../../literature/papers/lundin2024-modeling-of-an-ammonia-decomposition/original.pdf) confirms 0.5 wt% Ru/Al2O3 kinetics at 350–400 °C, separate membrane experiments with 27 g catalyst and local atmospheric permeate pressure near 82 kPa, no experimental sweep, and measurement runs shorter than 12 h. The paper directly covers coupled geometry, radial transport, heat and impurity permeation; trace impurity validation remains detection-limited. These main-text conditions were checked during implementation, and the existing ammonia proposal now incorporates this prior-art and validation boundary.

The later status check also found current KB-read packages for Peng, Zhou, Alcala and other PDH sources, and for the membrane preprints and boundary studies formerly listed as unavailable. Working-screen source tables now separate current KB reading status from this reviewer's independent figure checks. Qiu2025 and Abate2024 thesis bodies, Hong's dataset and the Co induction-stage article remain the specifically identified unread items in these source registers. No further literature discovery or new research direction was started.

## Overall conclusion

The uploads materially improve the evidentiary basis. They justify concrete corrections to performance comparisons, recovery accounting, source status and note quality. They support retaining the two existing directions as bounded conditional studies. They do not establish a substantial original program, invalidate the existing elemental balances, or warrant raising either direction's priority solely because the literature is now accessible.
