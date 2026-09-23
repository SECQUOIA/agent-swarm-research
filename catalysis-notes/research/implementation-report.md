# Implementation of the post-upload corrections

2026-09-16. Scope: correct and finish the existing research plans and their evidence records. No new research direction or experiment was started.

## Status

The scientific edits, source-note curation and fresh independent reviews are complete. All identified corrections within this audit's scope have been addressed; unresolved source content and experimental questions remain explicit. The [original audit](reviews/post-upload-literature-audit.md) preserves the findings that motivated this pass.

## Changes applied

| Area | Implemented change | Detailed record |
|---|---|---|
| Polymer | Published three-charge/one-makeup control; conditional `B = 2f`; separate Science/patent mass records; delivered exposure, washout, assay and tandem-transfer controls | [Polymer audit](reviews/post-upload-polymer-audit.md) |
| Ag | Correct Iyer model credit; Santos/Chen baselines; Jalil preparation and transient controls; Esposito kinetic/isotope limits; finite pair/operation design | [Ag audit](reviews/post-upload-ag-audit.md) |
| Methane | Source-condition reproduction, explicit wet sulfur-free reference, rate-based null, material-ranking and real-application gates | [Methane audit](reviews/post-upload-methane-audit.md) |
| CHA/styrene | Assay-history versus aging-order distinction, prior predictive model credit, Tang measured/model boundaries, Dimian utility/cost boundaries | [CHA/styrene audit](reviews/post-upload-cha-styrene-audit.md) |
| PDH/ammonia | Actual reaction/regeneration histories, independent prediction gate, finite-pressure membrane comparison, recovery/purity definitions and empirical kinetic domains | [PDH/ammonia audit](reviews/post-upload-pdh-ammonia-audit.md) |
| Carbonylation | Separate Shimura operating cases, induction and uncertain definitions; minimal wet-feed versus drying comparison with complete output accounting | [Carbonylation audit](reviews/post-upload-carbonylation-audit.md) |
| Nonselected alternatives | Historical/current selection distinction and bounded corrections from newly available evidence; no direction promoted | [Screen correction record](reviews/existing-screen-correction-report.md) |
| Shared summaries | Updated decision brief, source-status/queue framing, and authoritative current priorities | [Decision brief](decision-brief.md), [literature status](literature-status.md) |

## Independent verification

Fresh reviewers checked the edited files against primary-source evidence, recomputed consequential arithmetic, and challenged the experimental sequence and practical claims.

| Independent review | Outcome |
|---|---|
| [Ag/polymer](reviews/implementation-independent-lead-review.md) | Polymer source/accounting checks passed. A premature fresh-performance gate and leftover required Re comparison in Ag were corrected and rechecked: qualifying pairs proceed through the finite ordinary-retention horizon even with equal fresh output. |
| [Methane/CHA/styrene](reviews/implementation-independent-secondary-review.md) | Checked source comparisons, numerical boundaries, assay controls, rate-based null and application/stopping gates; no substantive repair required. |
| [PDH/ammonia/carbonylation](reviews/implementation-independent-conditional-review.md) | Arithmetic and benchmark checks passed. PDH validation now reserves the second history's outcomes until model, policies, useful margin and predictions are frozen. Both the screen and numbered review sequence were corrected and rechecked. |
| [Nonselected screens](reviews/implementation-independent-screen-review.md) | Original sources support the checked scientific corrections; no rejected direction was reopened. Residual alkylation source-status wording was changed to explicit historical language and rechecked. |
| [Literature-note sample](reviews/implementation-independent-literature-review.md) | Ten rewritten notes checked against original PDFs. A cross-paper Qiu attribution error and remaining operating-condition, denominator and citation ambiguities were corrected and rechecked. The sample is purposive, not a certification of the whole knowledge base. |

These are bounded independent reviews, not proof that every historical statement or untested mechanism is correct. No known substantive finding from these reviews remains unaddressed. Existing source inconsistencies and experimental uncertainties are identified in the plans rather than silently resolved by assumption.

Local file targets and heading links were checked across changed Markdown files. Seven renamed heading links in the historical source registry were repaired. `git diff --check` passes.

## Literature-note corrections

The original audit flagged 126 notes for source-specific review. Six read-only review groups checked 104 of those sources; the literature maintainer handled the remaining priority notes and additional targeted repairs. One maintainer applies the changes and maintains source provenance, package status and indexes. The review drafts identify exact source packages and page evidence; they do not add research directions.

The [completed curation report](../literature/runs/2026-09-16-post-upload-curation/run.md) preserves the source-review drafts, serialized intake and [135-entry disposition ledger](../literature/runs/2026-09-16-post-upload-curation/round-1/curated-slugs.tsv). All 126 originally flagged entries are covered. Across the full pass, the ledger records 126 repairs, eight reviews and one recovered SI package; these action counts do not map one-to-one to the original screening set. No flagged template wording remains.

The van Hoof SI PDF was recovered and read; its original archive and videos remain preserved. The duplicate Akin SI record is an explicit unread alias. The inventory now contains 648 canonical source records plus that alias: 618 canonical records marked read, 26 unretrieved and four retained but unread. Two additional missing components of retained works remain in the [missing-material report](reviews/post-upload-missing-sources.md).

The sole maintainer's final structural check returned `KB_CHECK=ok`, `UNREAD=31` and `READ_UNCITED=96`. The unread package count includes the alias; the unique-source unread count is 30. These diagnostics do not certify scientific claims. The landscape's opportunity cards are explicitly unselected; the [decision brief](decision-brief.md) remains authoritative.

The corrections address recurring scientific problems:

- **Different operating cases combined into one benchmark.** Durability, maximum productivity and maximum selectivity often come from different conditions or catalyst formulations. Each result retains its own conditions.
- **Incorrect denominators.** Feed conversion, conversion relative to equilibrium, selectivity excluding CO, mass-normalized rates, site-normalized rates and membrane recovery are kept distinct.
- **Measurement confused with prediction.** Reactor projections and calculated mechanisms are identified as model results. Pure-feed validation is credited without claiming that it validates near-zero local product pressure.
- **Overstated stability and causal attribution.** Reported losses, regeneration histories, assay limitations and competing explanations remain visible. Spectroscopic consistency alone does not establish a unique mechanism.
- **Inconsistent source statements.** Conflicting tables, prose, temperature labels and duration claims are recorded explicitly. The notes do not silently choose the more favorable number.

A fresh reviewer checked a bounded sample of ten rewritten notes against original sources and verified the resulting corrections. This is independent content verification; the knowledge-base structural check alone cannot establish scientific accuracy.

## Scientific limits that remain

These are research uncertainties and explicit preconditions, not claims that an editorial change can settle:

- The proposed catalyst responses and mechanisms require experiments. No catalyst improvement or practical superiority has been demonstrated by this work.
- Equipment, material access, project resources and real application feeds have not been verified. Commissioning must establish analytical variance, useful contrasts, independent replication and observation horizons.
- A finite recovery test establishes persistence over its stated protocol; operational uptake and spectra do not automatically count productive sites or uniquely identify mechanisms.
- Missing source components and inconsistent original-source definitions remain explicitly qualified. Retrieved papers, curated notes and validated experimental claims are different things.
- Practical comparisons must include the appropriate output, time, inventory, feed, regeneration and separation boundaries. A useful negative result can close a decision without supporting a larger program.

The current priority remains bounded Ag and polymer studies, with their order conditional on the available platform. The other existing studies retain their narrower gates. No experimental expansion follows solely from finishing these documents.
