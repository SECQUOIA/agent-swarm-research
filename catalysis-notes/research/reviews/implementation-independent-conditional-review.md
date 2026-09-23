# Independent implementation review: PDH, ammonia and carbonylation

Reviewed 2026-09-16 by a fresh reviewer after implementation. Scope: the three existing working screens, their associated independent reviews, the post-upload audits and their treatment in the [decision brief](../decision-brief.md). No new research direction, literature discovery, experiment or KB mutation was undertaken.

## Decision

**The corrected comparisons and bounded research decisions pass this review.** One moderate design ambiguity was found in PDH: the initial campaign could have measured the second history before calling it a prospective validation. The implementer corrected the working screen and associated review to reserve those outcomes until model, policies, decision margin and predictions are frozen. The revised sequence was independently rechecked.

None of these directions should be promoted above the current leads on this evidence. They have adequate conditional hypotheses, alternatives, practical boundaries and stopping rules for a bounded next experiment on an existing platform. This is a judgment about the written plans; it is not experimental validation or a guarantee that every source error has been discovered.

## Findings and disposition

| Severity | File and evidence | Disposition |
|---|---|---|
| Moderate, corrected | [PDH minimum campaign](../working/dehydrogenation-consequential-screen.md#minimum-campaign-and-stopping-decisions) originally compared policies at both spent histories before withholding the second for model selection. Merely excluding a known output from a fit does not make the subsequent operating-choice claim prospective. | Stage A now uses the first history only. Stage C explicitly freezes the model, candidate policies, margin and second-history output/ranking predictions before measuring those outcomes. This is a valid prospective gate. The [associated review](dehydrogenation-fresh-value.md#5-strongest-experiment-and-clear-stopping-rule) now uses this sequence in its numbered steps as well. |
| Pass | [PDH benchmark table](../working/dehydrogenation-consequential-screen.md#1-strong-modern-benchmarks-constrain-generic-stability-proposals) separates Lu's cumulative reaction hours and regeneration, Xu's continuous stability from a separate productivity condition, and He's mixed operating history and downstream carbon. | Primary-source text checks below support these distinctions. Complete-cycle superiority remains unclaimed. |
| Pass | [Ammonia finite-pressure bound](../working/ammonia-kinetics-screen.md#a-conditional-finite-pressure-bound) labels its empirical extrapolation, local pressure and ideal compression assumptions. | Independent arithmetic agrees. A passive approximately isothermal membrane producing pure H2 at 1 bar cannot drive its retentate interface below that H2 pressure. This restricts the particular ideal-rate target, not finite-pressure membrane usefulness. |
| Pass | [Ammonia minimum experiment](../working/ammonia-kinetics-screen.md#minimum-experiment-and-decision-gates) includes generated H2, a real device boundary, independent preparations, reference returns, oxygen-free validation, a credible catalyst alternative and a held-out prediction. | The oxygen diagnostic is not counted as recovered H2. Analytical limits terminate unsupported extrapolation. A better fit alone does not pass the expansion gate. |
| Pass | [Carbonylation experiment](../working/carbonylation-value-screen.md#one-conditional-discriminating-experiment) specifies a real wet feed and drying alternative, induction, wet/sham beds, common-feed recovery, a withheld history and complete operating choices. | Net MA+AA molecules are explicitly acetate units, with separate product split, mass and carbon accounting. Actual H2 loss and drying/reheating burdens replace charging all inlet H2 as consumed. Ordinary inhibition can resolve a useful wet-operation choice without a new mechanism. |
| Pass | [Decision brief](../decision-brief.md), final three conditional-screen summaries and readiness rules. | Rankings, uncertainty and expansion conditions agree with the detailed screens. Equivalence requires a useful prespecified margin and precision; a nonsignificant difference is not equality. |

## Independent numerical reproduction

Calculations were recomputed directly from the stated equations, without fitting data or simulating a real reactor:

| Check | Reproduced result | Interpretation |
|---|---:|---|
| Qiu empirical inhibition factor, fractions 0.1 / 0.5 / 0.9 | 73.797 / 11.904 / 1.475 Pa H2 | Matches rounded 74 / 12 / 1.5 Pa. Conditional on the empirical coefficient and its unvalidated low-H2 extension. |
| Generated-H2 ceiling at 1% NH3 and 1 atm, half-rate / 90%-rate thresholds | 0.7833% / 0.09702% conversion | Matches the proposed analytical targets; gradients and inlet H2 tighten them. |
| Arrhenius rate at 523.15 K and dilute first-order plug-flow result | k = 3.586 × 10−4; Da = 1.4467; X = 76.47% | Matches approximately 76%; this is not the measured O2 point. Normal molar volume was taken as 22.414 L mol−1. |
| Pure NH3 with instantaneous H2 removal / retained H2 but artificially deleted inhibition and equilibrium term | 86.81% / 64.94% | Reproduces the distinct gas-expansion balances. Neither is measured conversion. |
| Reversible compression, 12 Pa to 1 bar, 298 / 523 K | 22.37 / 39.26 kJ mol−1 | Matches the rounded illustrative estimates; not a full process duty. |
| Han SI Table 2 carbon-fraction products | 6.820% / 2.6637% | Supports the reported 6.82% / 2.66% conditional feed-carbon yields, not a recycle-process yield. |
| Wu retained-H equivalents for 0.42 / 0.97 / 1.30 µmol excess O2 | 1.68 / 3.88 / 5.20 µmol H atoms | Correct stoichiometric equivalents; presence of those inventories remains unmeasured. |

## Primary-source checks

Fresh text was extracted from retained original PDFs for [Lu](../../literature/papers/lu2026-subnanometre-ptsn-alloyed-clusters-encapsulated/original.pdf), [Xu](../../literature/papers/xu2025-pt-migrationlockup-in-zeolite-for/original.pdf), [He](../../literature/papers/he2025-ultradurable-regenerative-propane-dehydrogenation-catalyst/original.pdf), [Itoh](../../literature/papers/itoh2014-kinetic-enhancement-of-ammonia-decomposition/original.pdf) and [Napolitano](../../literature/papers/napolitano2025-enhanced-ammonia-decomposition-using-a/original.pdf). The relevant Shimura retained main-text extraction was checked against the [post-upload review](post-upload-carbonylation-audit.md). This review did not independently inspect every original plot or supplement.

- **Lu:** the text confirms initial productivity near 1.17 mol gcat−1 h−1, above 1 for at least 60 h, then more than 300 reaction hours with six regenerations. Calcination increases from 1–2 h to 10 h; the figure caption includes H2 treatment. These do not supply a measured complete-cycle average.
- **Xu:** the long test gives approximately 28.4% conversion and 98.3% selectivity at 550 °C and WHSV 5.3 h−1. The 91% number is relative to equilibrium. The 18.7 kg kgcat−1 h−1 result is a distinct experiment.
- **He:** the text and Figure 4 caption confirm 50 h reaction segments and 2 h H2 regeneration, and describe carbon transfer onto downstream quartz. The source does not justify treating catalyst recovery as removal of the reactor carbon burden.
- **Itoh:** the text directly gives 73% to 87% conversion at 723 K, 0.001 MPa permeate pressure, a 200 µm membrane and about 60% recovery. Equation 3 uses theoretical hydrogen from incoming NH3. The later membrane description specifies a rolled palladium–silver alloy tube; the screen's Pd–Ag description is supported despite shorthand references to palladium elsewhere.
- **Napolitano:** Equation 5 divides permeated H2 by permeate-plus-retentate H2. Atmospheric permeate and mixed-feed comparisons are explicit. The source's broad abstract purity claim conflicts with its conditional results, as already recorded by the post-upload audit. This review confirmed the denominator and case distinctions; it did not independently redigitize conflicting plotted recovery points.
- **Shimura:** main text confirms separate maximum-selectivity, maximum-yield and 10 h time-course conditions, approximately 7 h induction, 0.67 mmol g−1 h−1 and the printed 0.35–0.71 nm granule unit. The existing source-definition and SI caveats remain necessary.

## Remaining limits

Unmeasured chemistry and process data cannot be repaired editorially. Wu's complete cycle chronology and selective redox inventory remain unresolved; Qiu's oxygen-free low-H2 response remains unvalidated; Shimura's missing SI definitions and protocol ambiguities remain open. Actual platforms, sample access, calibration precision and feed/separation costs are not established. The plans appropriately gate expansion on these conditions, preserve useful negative outcomes and avoid industrial lifetime claims from finite tests.

The benchmark corrections do not establish that Ga outperforms Pt, that the Qiu material is the best membrane catalyst, or that wet carbonylation beats drying. No remaining high-severity scientific or accounting error was found within this bounded review. Final documentation should retain this scope and uncertainty rather than claiming that the ideas have no possible issues.

## Final Qiu2025 fairness check

The final ammonia screen, associated review and post-upload audit now explicitly credit Qiu2025's commercial-catalyst validation. This addition was independently checked against freshly extracted [original main text](../../literature/papers/qiu2025-kinetic-investigation-of-nh3-decomposition/original.pdf), pp.7–8, §§3.5–4. The authors report successful temperature/composition predictions for commercial Heraeus Ru catalyst in 1 mm beads up to pure NH3 feed, referring to Figure S7. They distinguish this high-H2 reacting regime from low-temperature H2-lean conditions where their reduced law loses accuracy. The Ru/MgAl2O4 result at GHSV below 2500 normal L kgcat−1 h−1 and below 500 °C is explicitly a Figure 11 model prediction.

The implementation now represents those distinctions fairly: pure inlet NH3 generates H2 during reaction and does not establish the near-zero local-H2 extrapolation on the selected catalyst/device. The remaining proposed validation addresses that specific transfer, not an absence of all published high-NH3 validation. This check verifies the main text's account of Figure S7; it does not independently reconstruct that supplement's fit. No correction to the final wording, experimental gates or priority is needed.
