# Stage 2, round 2 — independent reviewer 1

Verdict: **Accept with one minor statistical wording correction. No remaining or new major issue identified.** The revised program now directly tests ordinary-cycle steam compatibility before applying a special recovery treatment. Its narrower opening and closing claims match that design.

## Scope and resolved concerns

I reread the complete revised `manuscript/sections/02-cyclic-oxides.tex` and `manuscript/evidence/stage2-cyclic.md`, examined extracted text from the current 16-page PDF, and visually inspected the revised experimental table/contrasts and closing discussion on pages 10 and 14. I retained the independent primary-source checks from round 1 and checked the newly relevant Gao Mössbauer passages and the cited NanoSIMS method precedent. I did not read other reviewers' reports or the correction report and edited only this report.

The revisions resolve the interpretation problem:

- Lines 47–49 measure ordinary steam versus Ar cycling without supplementary CO2 or a special reset. They preserve the operating penalty, including reversible inhibition and carryover, in the measured endpoint.
- Lines 49 and 82 distinguish a terminal recovery treatment from ordinary oxidation. Recovery is explicitly conditional on that treatment and is not assigned to a unique repair mechanism.
- Line 76 now requires the two matched wet–dry contrasts in addition to the timing interaction and Ar comparisons. This addresses my round 1 request.
- Lines 96, 102, and 124 specify treatment cadence and keep terminal analytical treatment outside the counted production block. Managed policies are compared with untreated steam and Ar on matched histories.
- Lines 78 and 86 qualify state preservation and gas washout. Lines 88–92 distinguish direct output, carbon-source attribution, total Li inventory, spatial mapping, and bulk Fe-state information. These qualifications prevent unsupported microscopic conclusions without making the direct functional comparison depend on complete mechanism identification.

## Major issues

None. No further experimental outcomes are required to complete this proposal. Pilot-selected operating conditions, reset feasibility, detection limits, and predictive success remain appropriately declared experimental dependencies.

## Minor issue

### Use the direct timing-contrast interval to close the timing-benefit claim

**Location:** `manuscript/sections/02-cyclic-oxides.tex:126`, sentence beginning “If both timing arms recover within the consequential-loss bound.”

**Evidence:** Separate recovery bounds for two arms do not necessarily exclude a consequential difference between them. For example, normalized outputs of 1.09 and 0.91 are each within 0.10 of a common baseline but differ by 0.18. Sampling uncertainty further matters. One-sided exclusion of consequential loss also permits improvement above baseline. Thus the stated recovery condition alone does not establish that a persistent concurrent-over-delayed advantage is absent. The design already measures the necessary direct contrast.

**Remedy:** Replace the condition with: “If the uncertainty interval for the post-reset wet concurrent-minus-delayed contrast excludes the predeclared consequential benefit, that timing-benefit claim closes under this reset.” Retain the separate qualification that this does not establish that all CO2 treatment is unnecessary. Use the timing interaction interval separately for any specifically steam-dependent claim.

**Severity:** Minor. This is a decision-rule wording correction using existing measurements and contrasts, not a design change or a request for additional experiments.

## Prior art, evidence, and presentation

The Gao, Brody, Barckholtz, Chacko, and Fereres claims remain supported by the primary passages checked in round 1. The revised line 86 is more precise about Gao: coated-LSF inhibition and the separate molten-salt reversible-switch experiment are now distinguished. Gao's Results and Methods explicitly support Mössbauer as a candidate Fe-state method on this material family. The [Xu et al. primary preprint](https://arxiv.org/abs/2102.13148) supports Li mapping by NanoSIMS in an alloy; the evidence note correctly treats it only as a method-class precedent, without transferring alloy resolution or quantitative coverage to coated LSF.

The chapter continues to credit regeneration and prevention/recovery precedents and confines novelty to the specified purge comparison and conditional history prediction. I found no new unsupported prior-art claim. The equations and numerical illustrations remain consistent. The current log has no `Warning`, `Overfull`, or `Underfull` matches, and the sampled rendered pages show readable equations, table entries, citations, and chemical notation.

No broader materials screen, additional purge location, isotope campaign, or commercial demonstration is needed to resolve this review.
