# Stage 3, round 1 — independent reviewer 1

Verdict: **Revise the pressure-screening decision before accepting the experimental program. One major design issue; no major source-accuracy or originality issue identified.** The chapter establishes a worthwhile, bounded contribution: reduce fresh catalyst-solid demand at accepted polymer-derived output and complete time. Its present screening gate, however, can reject that opportunity without testing partial replacement.

## Scope

I reviewed `manuscript/sections/03-polymer.tex`, the Stage 3 bibliography entries, and `manuscript/evidence/stage3-polymer.md`. I checked the relevant original Conk article and supplementary methods, Chen's final model, Guironnet and Peters' model, Wang's dissertation, and the patent disclosure. Conk's Figure 4 caption and Wang's workup observation were verified by extraction directly from their original PDFs. I also checked the official indexed Conk dissertation abstract and targeted online prior-art results. The embargoed dissertation body was not accessed. I did not read other reviewer reports, communicate with other reviewers, or edit anything except this report.

## Major issue

### 1. A no-makeup pressure screen cannot decide whether pressure substitutes for part of the makeup

**Location:** `manuscript/sections/03-polymer.tex:77`, `:81`, and `:83`; consequence for the predictor at `:97–99`.

**Evidence:** The first lower-ethylene comparison is performed on retained inventories “initially without makeup.” The existing dose bracket is repeated at the lower condition only after a beneficial result, and a precise negative result closes the chosen pressure intervention. The central question in line 4 is instead whether pressure can replace **part** of the fresh Na/alumina addition.

These questions are not equivalent. If `ΔQ(m)` denotes the lower-minus-reference pressure response at makeup dose `m`, observing `ΔQ(0) = 0` does not imply `ΔQ(0.2 g) = 0`. A depleted mixture could need some fresh Na material before any pressure benefit appears. Conversely, pressure might alter the dose requirement while leaving the zero-makeup endpoint unchanged. The chapter explicitly recognizes coupled initiation, isomerization, activation, and transport, so it has no supported separability assumption that rules out this interaction. The source's full-Na rescue does not supply such an assumption.

As written, a technically valid negative screen could therefore close the program while a lower-ethylene/midpoint-dose policy meets the accepted-output requirement and saves fresh solids. That would leave the stated central substitution question materially untested.

**Remedy:** Before closing the pressure-as-partial-substitution branch, test the already proposed reduced nonzero dose at both reference and lower ethylene in the qualified semibatch mode, with the same charge-1 history and once-only addition before charge 2. Compare its accepted cumulative polymer-carbon output and time with the full-dose reference policy. Retain the no-makeup comparison as a useful endpoint, but do not make its success a prerequisite for the midpoint comparison. The existing finite dose bracket can be crossed with the two pressure conditions if that is the clearer implementation. No extra pressure levels, materials screen, or assumed positive result are needed.

**Why major:** This affects the central go/no-go inference and access to the proposed original contribution, rather than merely improving precision or adding an optional mechanism study.

## Minor issues

No additional correction is required for source accuracy or prior-art framing. The numerical and bibliographic checks below did not reveal a material factual error.

## Source and originality assessment

- Conk's Figure 4B caption confirms exactly three PE charges, with one 0.4 g Na/alumina addition before charge 2 and no further catalyst addition before charge 3. The manuscript uses the stronger existing comparator correctly and does not adopt the source's rescue observation as proof that W function remains unchanged.
- The 1 g PE and 0.4 g of each catalyst conditions are supported. The supporting procedure charges gases before heating, and the 10 versus 15 bar discrepancy in the component experiment is real. The semibatch pressure/flow confounding and 12-minute sampling interval are correctly identified.
- The official [Conk dissertation abstract](https://escholarship.org/uc/item/7v07b7c8) discloses transfer-dehydrogenation initiation, modified catalysts, and DME-based regeneration. The chapter appropriately treats these as prior disclosures while stating the body-access limit. The patent's Figure 21 identity ambiguity is also real; the manuscript does not claim a verified regeneration yield for the unmodified Na/W mixture.
- Chen's final model treats finite isomerization, identifies an ethylene-inhibition regime, and restricts applicability to relatively slow isomerization. It does not establish that lower ethylene benefits aged Na/W. Guironnet and Peters explicitly describe numerical coefficient updating for time-varying ethylene. The manuscript credits these theoretical precedents and keeps its operational prediction distinct.
- Wang's printed page 73 states that depressurization and two to three hours of cooling permit isomerization and fragment recombination. The proposed quench qualification is justified; this observation is not transferred as an established Na/W workup effect.
- The fresh-solid inventory table, `2f` and `2.4f` productivity ratios, and conditional 25% Na/alumina and 16.7% total-solid savings are arithmetically correct.
- The two-source isotope equation correctly uses carbon atom fractions. Consistent ethylene enrichment through conditioning and reuse, a carbon-free tracer, other-carbon checks, cumulative output, and retained-inventory accounting address the principal carbon-origin ambiguities. Those controls are experimental dependencies, not fabricated validation.

No verified source found in this scoped review establishes the proposed pressure-mediated partial replacement of Na makeup. That is a scoped novelty assessment, not a guarantee of universal originality. The identified design correction is necessary to test that distinct opportunity.
