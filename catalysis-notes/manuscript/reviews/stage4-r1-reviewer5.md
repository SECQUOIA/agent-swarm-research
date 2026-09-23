# Stage 4, round 1 — independent reviewer 5

**Verdict: revise one major decision-rule issue and one minor cost-reporting clarification.**

The proposed chemistry and main experimental comparisons are coherent. The chapter appropriately starts from a functioning promoted catalyst, separates the Ni-addition intervention from gross processing damage, and distinguishes matched exposure from individually useful operating choices. Its full-clock output and resource accounting are substantially stronger than endpoint selectivity comparisons. The main remaining problem is that the final rule for deciding whether chloride recovery substitutes for Ni excludes a Ni recovery policy that the program itself tests.

## Major issue

**Include the Ni recovery policy before closing the useful Ni advantage.** `manuscript/sections/04-silver.tex:77` proposes comparing the new Ni-free recovery policy against the best Ni and Ni-free **ordinary** policies to close the useful Ni advantage. Yet lines 52 and 68–77 explicitly measure and predict recovery for both materials. The Ni recovery policy is therefore an available, relevant contender, not an untested speculative alternative.

For a simple counterexample on a common full-clock basis, suppose ordinary Ni and sham produce 100 and 90 accepted EO units. Recovery adds 30 units for Ni and 20 for sham, including its downtime. The proposed final comparison would show recovered sham at 110 beating ordinary Ni at 100, although recovered Ni produces 130. Thus it could declare that chloride recovery replaces the useful Ni advantage while overlooking the best measured Ni policy. This affects the principal formulation-versus-operation conclusion, not merely presentation.

**Remedy:** construct absolute full-clock recovery outputs for both materials, `Q_m,R = Q_m,C + B_m`, using their appropriate common-setting histories. Compare all admissible tested ordinary and recovery policies on the same horizon, acceptance rules, resource boundary, and normalization. Carry the decisive Ni recovery prediction through independent validation as well as the Ni-free prediction. If only the narrower replacement of a particular ordinary Ni policy is tested, state that narrower conclusion and do not close the broader useful-Ni claim. The existing design already supplies both materials' recovery traces, so this repair need not expand the program into a new campaign or optimization library.

## Minor issue

**Define the break-even preparation-cost calculation without implying that unpriced flows determine money.** `manuscript/sections/04-silver.tex:42` asks for “the break-even added preparation cost” in the absence of defensible prices but does not specify how that quantity will be reported. Physical EO and resource differences alone cannot determine a monetary break-even value.

Add a symbolic expression or sensitivity boundary, for example extra allowed preparation cost equals valued additional accepted EO minus valued additional resource and handling requirements over the same horizon. State the comparison policy and whether the result is per bed, per initial Ag mass, or per campaign. If no valuation is supplied, report that expression and measured physical differences rather than a numerical monetary result. This is a reporting clarification; a detailed economic model is unnecessary.

## Scientific validity, sources, and completeness

I followed the previously read `literature/AGENTS.md` and checked relevant primary passages in Kemp, Jalil and its SI, Hwang, Iyer/Bhan's reactor model, and the chemical-titration article. I did not consult other reviewers' reports.

Kemp's preparation and composition table confirm the unmatched Cs contents and the unaged ethanol-treated control. Table III reports losses from individual starting selectivities, as the chapter correctly explains. Independent arithmetic gives an Ag/Ni atomic ratio of 834.73 and the conditional selectivity-based resource reductions of 1.0989%, 4.3956%, and 10.9890%, agreeing with the text.

I rendered the original Jalil SI Figure S21. The NiAg EO rate first rises and then declines substantially, supporting the chapter's limited transient interpretation. Hwang's architecture argument is presented as a motivation rather than direct evidence of Ni-to-Re transfer. Iyer and Bhan's 2021 model is correctly credited with forward reactor predictions, while its existence is not treated as validation of arbitrary temporal recovery. The 2023 titration source explicitly permits inactive adsorption and bounds its site estimate; the manuscript preserves that limitation.

The proposed common-conditioning histories, fixed ordinary-operation horizon, lower-chloride alternative, matched-age recovery controls, independent preparations, and withheld duration make the program experimentally testable. The discussion of ethane and cofed-product carbon avoids a naive EO/CO2 selectivity assignment. The distinction between policy inadmissibility and actual unqualified product is useful, with unfiltered net output retained. Conditional structural and isotope work is kept subordinate to a consequential functional question. I found no need to demand performed positive results or a larger materials campaign.

## Reader comprehension and PDF

The reaction-level motivation, practical endpoint, comparison histories, and limits of microscopic interpretation are sufficiently explained for a catalysis reader. The principal recovery-benefit equation is readable and dimensionally correct; the major finding above concerns the subsequent policy ranking, not that equation.

I inspected the stage's extracted PDF text and rendered pages 23, 24, 26, and 27, including both accounting equations and the complete recovery-decision paragraph. Chemical notation, equations, citations, and paragraph headings are legible. The short final page is a harmless pagination consequence. The 30-page build log has no undefined-reference, overfull-box, or underfull-box warnings. No PDF formatting correction is required.

This report is the only authored file; no chapter, bibliography, or knowledge-base file was changed.
