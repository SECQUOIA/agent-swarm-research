# Stage 4 independent review 3

Reviewed 2026-09-13/14. Scope: Section 6 and its generated tables; Stage 4 author record; local failed-step extracts and extraction/recombination scripts; solver/source/primal audit; frozen V1/V2/V3 distinctions; and the merged bound catalogue. Primary evidence was inspected directly. No other reviewer report was read, no agent was delegated, no numerical generation or complete bulk replay/hash campaign was run, and no manuscript/checker file was edited.

## Verdict

**No major issues found.** One minor numerical-description correction is required. The scientific distinctions central to this section are correct: rejected proof rules are not refutations of final bounds; a failed sufficient safe-cut test is not proof that the cut is globally invalid; source-formula equivalence is not compiler/runtime verification; and a checked original-model witness plus matching lower bound does establish exact optimality. The historical, uniform, and repair populations remain distinguishable.

## Required minor correction

**R3-1 — Identify the size of the rational component that triggered the reporting guard.** In Section 6's reporting-repair paragraph, “a 4,326-digit bound” is imprecise. The saved `tls12` primary kernel result has a rational lower-bound token of 8,652 characters: its numerator has 4,326 decimal digits, its denominator 4,325, with one separating slash. The reported Python exception is the numerator conversion, not a 4,326-digit whole bound.

Proposed replacement: “a rational bound with a 4,326-digit numerator failed during subsequent report construction.” The denominator count can be added if useful but is not necessary. The claim that this happened after complete internal proof acceptance is supported by the raw report. This correction affects neither the mathematical value nor campaign outcomes.

## Direct evidence checks

### Historical and new invalid inference records

- Independently recombined all twelve historical first-failure extracts using standard-library `Fraction`. Eleven have exactly matching resultant coefficients, an upper relation, and a positive difference between the supplied combination RHS and the stronger claimed RHS. The smallest and largest differences are approximately `1.5474925795191292e-12` and `1.9319551763282518e-10`, agreeing with the section.
- The remaining historical extract, `smallinvDAXr5b200-220`, has both positive and negative multiplied inequality senses. The section correctly diagnoses an incompatible supplied combination rather than concluding that the final bound is false.
- Read the three fresh extracts and independently compared every extracted target and antecedent against bounded reads of the actual selected proof prefixes. All match: 41 rows for `smallinvDAXr1b200-220`, 41 for `smallinvDAXr3b100-110`, and five for `smallinvDAXr4b200-220`. No whole large proof was replayed in this inspection.
- In the two new combination cases the offending upper rows carry strictly positive multipliers and nonzero coefficients. They are not constant tautologies. In the new `uns` case the actual assumptions on integer variable index 4 have coefficient 1 and RHS 64/66 with opposite upper/lower directions. Integer activity 65 satisfies neither. The text appropriately allows that unrelated master constraints could exclude 65, while explaining that this standalone submitted split does not prove it.
- The raw generation records identify external acceptance on the conservative completed attempts followed by internal failure at steps 4082, 1639, and 26121. Therefore the external-acceptance/internal-rejection comparison is evidence for these particular supplied artifacts, not an inference merely from an aggregate count.

These checks establish local rule failures. They do not certify antecedent derivations or prove the final mathematical bound false. Both the extracts and Section 6 retain that boundary. The term “invalid inference” in this context means invalid under the stated local proof rule; it should continue to be used with that context.

### Nonlinear cut rejection

The recorded `risk2bpb_cut1_replay.json` distinguishes the historical intercept from the newly computed sufficient support-intercept endpoint and gives an excess of approximately `1.169668042854472e-12`. Section 6 faithfully calls this failure of the certificate test. It does not mistake a conservative bound on the best admissible intercept for the actual best intercept or a counterexample to the inequality. The targeted repaired generation is kept separate from the uniform experiment.

### Exact primal optimum and returned points

- Independently reran the current exact rational evaluator on the archived 52-variable `clay0204m` witness: no variable/row feasibility failures and objective exactly 6545. Independently replayed its small complete bundle without an external solver: accepted lower bound exactly 6545. These two checks establish the claimed loaded-model optimum.
- Inspected the BARON printed source of that witness. The nonzero values replaced by zero are `x41`, `x48`, `x49`, and `x52`; the manuscript's explanation that distance coordinates were explicitly repaired is consistent with the artifact. Feasibility is established by reevaluation, not inherited from the solver.
- The original SBB listing reports normal completion and model status 8, Integer Solution. Its separate log contains “Non convex model!”. The section correctly avoids an unqualified optimality-status claim. The cited GAMS rows are exactly `x2-x4+51*b13 <= 46.5` and `x6-x7+86*b24 <= 82`. Their residuals and robustness calculation agree: coefficient absolute sums 53 and 88 times the allowed coordinate perturbation `0.00005` give `0.00265` and `0.0044`, far below 4.5 and 3.
- The SHOT listing reports optimal model status, while the source explicitly fixes `b4` and `b5` to zero. The unit returned-point violations suffice regardless of tiny residuals elsewhere. The saved log records SHOT 1.1 and CPLEX 22.1; the baseline script gives the stated tolerance and thread requests.
- Independently reran both source-equivalence checks. They confirm 52 variables/90 retained constraints for `clay0204m` and 463/580 for `risk2bpb`, with the documented objective-variable elimination and index map. The paper explicitly limits this to the common exact binary64-constant source interpretation and does not claim to verify GAMS compilation or recover historical solver memory. The actual violated row coefficients and fixed values are exactly representable, so the stated violations do not rely on rounding a decimal model coefficient.

### Versioned representation repairs and catalogue

- Parsed the original uniform, producer-repair, and reporting-repair replay JSONL files: respectively 203 verified/19 rejected/67 missing; 12 verified; and two verified. The two last records concern distinct completed proofs of the same `tls12` model.
- The original `tls12` report records passing nonlinear, master identity, and internal kernel checks, followed by the 4,300-digit integer-string guard exception. This supports calling the repair a reporting-boundary repair rather than a new proof acceptance rule.
- Compared `exact_model.py`, `convexity.py`, `safecut.py`, and `vipr.py` bytes across V1, V2, V3, and the current lab: unchanged. Inspected the driver diff: it changes exact bound parsing/serialization after proof success, not model/cut/master validation. The V1-to-V2 producer diff replaces guarded Python integer text conversion with FLINT fraction canonicalization. The section's characterization of these observed repairs as representation fixes is justified.
- Independently checked every catalogue candidate's sense/model-hash compatibility and that each of the 222 selected normalized lower bounds is the exact maximum over its candidate records. The candidate total is 405, and selection counts are 162 historical, 51 primary, nine producer-repair. All selected model hashes also match the actual model-file bytes. This is a valid strongest-bound union under the stated source interpretation. It is correctly excluded from uniform-budget success-rate claims.
- Recomputed the historical negative normalized reference differences: 23 values, maximum magnitude approximately `5.833656876857371e-10`, matching the stated bound below `6e-10`. These are comparisons with reference strings and are not treated as primal certificates.

## Scope of this review

The bounded case replay and exact local calculations above were executed independently. The full large-proof campaigns, timing measurements, 93 GB member stream, and all package-extraction tests were not rerun here. Their recorded evidence and explicit scope are consistent with the scientific claims inspected. Stage 5's abstract/discussion integration remains a later obligation, not a Stage 4 defect. No correction to the mathematical checker or rerun of a campaign is requested by this review.
