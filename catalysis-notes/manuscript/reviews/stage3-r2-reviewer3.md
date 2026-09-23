# Stage 3, round 2 — reviewer 3

Verdict: **approve. No remaining major or minor issues requiring correction found.**

Independently reviewed the entire revised `manuscript/sections/03-polymer.tex` and `manuscript/evidence/stage3-polymer.md`, including unchanged accounting and interpretation alongside the revised pressure–dose design, analytical method, validation, and replacement policy. No other reviewer reports were consulted. No chapter or library files were changed.

## Design and inference

- **The pressure–dose gate is resolved.** Lines 77–83 require all six combinations of the two pressures and three existing doses, regardless of the zero-dose result. Common charge-1 histories and once-only additions preserve the intended comparison. Pressure contrasts within dose and reduced-dose comparisons against the full-dose reference policy directly address partial substitution. Closure is limited to informative results at the measured doses and pressures.
- **Paired validation supports the claimed distinction.** Lines 97–99 retain pressure–dose interaction in the predictor and freeze predictions at both pressures for the withheld dose. A passing lower-pressure policy alone is no longer called evidence that pressure enabled the saving. The same-dose reference result must informatively fail an acceptance criterion; if both pass, the conclusion is an adequate lower dose plus any separately demonstrated pressure benefit. The text correctly avoids inferring a minimum over unmeasured doses.
- **The replacement extension is executable and bounded.** Lines 101–103 specify the intervention trigger, time and charge-count bounds, full-mixture removal, measured carbon/solid withdrawal, fresh 0.4 g additions of each component, and restart of the validated history and makeup schedule. No selective W separation or unqualified regeneration is assumed. Failed charges and shorter service intervals incur their actual costs. A common credited output target, separate reporting of excess, and no extrapolated credit for a failed target make the finite comparison interpretable.

## Balances, units, and uncertainty

The isotope equation remains the correct two-source carbon atom balance. Constant ethylene enrichment across conditioning and all charges preserves original-source classification despite carryover; it does not identify individual PE charges, as stated. Other carbon sources, isotope discrimination, fragmentation, collection, and retained inventories must be qualified before using the polymer-carbon denominator. Product is credited once, and neither discarded residue nor residue disappearance becomes recovered carbon.

The catalyst-solid demand and complete-time productivity equations remain dimensionally correct. The three-charge totals of 2.4, 0.8, 1.0, and 1.2 g, the `2 f` and `2.4 f` productivity factors, and the conditional 25% Na/alumina and 16.7% total-solid savings remain correct. The extension preserves both catalyst-component costs rather than hiding W replacement behind a Na-only improvement. Pilot-based resolution, independent sequence replication, propagated attribution uncertainty, product specification, and a complete-time criterion remain part of acceptance.

## Source and analytical-method checks

The newly specified He tracer route is technically plausible and explicitly conditional on actual qualification. [Agilent's TCD documentation](https://openlab.help.agilent.com/2.7/en/mergedProjects/GCHelp/mergedProjects/78xxGC/TCD_ThermalConductivityDet.htm) supports detection relative to carrier gas; its [site-preparation manual, printed p.10/Table 4](https://www.agilent.com/cs/library/support/documents/a15283.pdf) identifies Ar for hydrogen/helium analysis. The chapter separately requires hydrocarbon calibration, synchronized sampling, hydrogen separation, flow recovery, and reference requalification. These documents do not establish that the proposed equipment or method is already qualified, and the manuscript does not claim otherwise.

Rechecked Guironnet's original PDF p.5: it describes how to extend the model numerically to changing ethylene while showing fixed-concentration solutions. The corrected attribution is accurate. The source reuse schedule, batch-versus-semibatch distinction, final Chen-model limits, and Wang workup warning remain consistent with the original material checked in round 1.

No experimental saving, pressure response, long-term durability, or selective loss of initiation is presented as already measured. The remaining experimental dependencies are appropriate limits of a proposed program rather than missing results.
