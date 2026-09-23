# Stage 3, round 2 — independent reviewer 1

Verdict: **Approve as a research proposal. No remaining major or minor issue requiring correction identified.** The revised pressure-by-dose comparison resolves the central design problem from my first review. The program now tests the stated partial-makeup substitution question without assuming that pressure and makeup act independently.

## Scope

I reread the complete revised `manuscript/sections/03-polymer.tex` and `manuscript/evidence/stage3-polymer.md`. I assessed the revisions against the primary-source checks in my first review and checked the newly specified tracer method against the cited manufacturer's documentation. I did not read other reviewers' reports, spawn agents, or edit the manuscript or knowledge base. Only this report was written.

## Resolution of the major issue

At `03-polymer.tex:77`, both ethylene conditions are now crossed with 0, 0.2, and 0.4 g once-only Na/alumina additions. The nonzero doses are tested regardless of the zero-dose result, using independent sequences with a common charge-1 history. Lines 81–83 require the reduced-dose comparisons before closing the partial-substitution claim and restrict a negative conclusion to the tested doses and pressures. This directly resolves the unsupported screening inference identified in round 1.

The validation is also appropriately matched. Lines 97–99 retain pressure–dose interaction in the predictor and test the withheld dose at both pressures after freezing both predictions. A claim that pressure enables that dose saving requires acceptance at lower pressure and informative failure of the same dose at reference pressure. If both pass, the manuscript reports an adequate lower dose without assigning its necessity to pressure. It does not infer a minimum over unmeasured doses.

## Full-program assessment

- **Decision and accounting:** The catalyst-solid demands, accepted polymer-origin carbon denominator, complete-time requirement, and cumulative sequence basis remain coherent. The isotope expression uses carbon atom fractions and explicitly requires source-history consistency, analytical calibration, and bounds on other carbon contributions.
- **Analytical method:** Line 29 now provides a plausible route for the carbon-free tracer rather than leaving its detection implicit. Agilent's [site-preparation guidance, Table 4 and Note B](https://www.agilent.com/cs/library/support/documents/a15283.pdf) supports Ar-carrier TCD analysis of He. The text correctly requires matrix calibration, hydrogen separation, flow recovery, and independently calibrated hydrocarbon detection; it does not assert that equipment or method qualification already exists.
- **Reuse extension:** Lines 101–103 now specify the intervention trigger, full-mixture replacement, restart history, output target, and maximum bounds. Failed charges, withdrawn residues, fresh solids, and interruption time remain in the comparison. This can test whether the initial saving survives the stated replacement policy without assuming selective recovery of a catalyst component.
- **Mechanistic scope:** The proposal still distinguishes operating benefit from selective initiation loss. Chain-state and component-specific studies are conditional and must pass access, quench, and specificity checks. A useful operating result does not depend on a unique microscopic explanation.
- **Prior art:** The corrected Guironnet wording at line 14 distinguishes the described varying-ethylene extension from displayed fixed-ethylene calculations. The Conk reuse schedule, theoretical model limits, Wang workup warning, dissertation access limit, and patent ambiguity remain consistent with the primary evidence reviewed previously. No new claim transfers molecular-system kinetics to aged Na/W.

The present LaTeX log contains no matches for warning, overfull, or underfull messages. This round did not include a fresh visual PDF inspection.

Experimental access, reproducibility, method resolution, actual pressure response, and predictive success remain declared dependencies. They require future experiments and do not constitute unresolved flaws in this proposal. No broader pressure survey, extra materials campaign, or demonstrated positive outcome is required for approval.
