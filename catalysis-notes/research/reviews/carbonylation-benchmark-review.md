# Independent review of the carbonylation benchmarks

Initial review: 2026-09-15. Post-upload update: 2026-09-16. Fresh bounded review of [the carbonylation screen](../working/carbonylation-value-screen.md). No experiments or knowledge-base mutations. This review checks the principal quantitative comparisons; it is not a new literature-wide originality assessment.

## Decision

**Retaining carbonylation as a conditional validation opportunity, without selecting a substantial new program, is fair.** Existing results already demonstrate strong dry-feed durability and appreciable improvements in wet tandem operation. The proposed wet/dry/recovery experiment could answer a useful operating question, but the generic experiment and water-exclusion hypothesis do not yet establish an original research program.

The earlier screen transcription error has been corrected: **Fan Figure 6 says GHSV 10,000, not 9000 mL gcat−1 h−1.** It agrees with the methods. The source's 514 h versus “over 520 h” statements remain inconsistent. The Han feed-carbon calculations are correct on their stated conditional basis. Its temperature discrepancy is real. Its exact mass normalization remains insufficiently specified for a definitive interstudy productivity comparison.

## Sources inspected independently

The Fan/Han list below records the original 2026-09-15 review and its temporary working paths. Their main articles, Han SI and Han source-data workbook are now retained in the knowledge base. Shimura main was additionally checked on 2026-09-16; this update does not imply that all newly uploaded carbonylation sources or supporting files were independently re-read.

- Fan 2024, DOI [10.1021/acsami.3c18170](https://doi.org/10.1021/acsami.3c18170): original `/tmp/carbonylation-screen/h2-benign.pdf`, methods §2.3, relevant results and conclusions, original Figure 6 and caption visually inspected. The retained image `/tmp/carbonylation-screen/fan-fig6.png` shows the same original page, 18750. Fan SI was not read.
- Han 2025, DOI [10.1038/s41467-025-66117-9](https://doi.org/10.1038/s41467-025-66117-9): original publisher HTML `/tmp/carbonylation-screen/han2025.html`, relevant methods/results and Figure 2 caption; original SI `/tmp/carbonylation-screen/han2025-si.pdf`, Tables 2–4 visually inspected and relevant captions read.
- Han original Figure 4 image retrieved and visually inspected at `/tmp/carbonylation-screen/han2025-fig4-review.png`; [publisher image](https://media.springernature.com/lw1200/springer-static/image/art%3A10.1038%2Fs41467-025-66117-9/MediaObjects/41467_2025_66117_Fig4_HTML.png).
- Han original source-data workbook retrieved at `/tmp/carbonylation-screen/han2025-source-data-review.xlsx`; [publisher workbook](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-025-66117-9/MediaObjects/41467_2025_66117_MOESM3_ESM.xlsx). Only the Figure2 and Figure4 sheets were read. Remaining sheets and peer-review file were not read.

The new available workbook and figure artifact were sent to the sole `/root/literature` worker for the already queued Han entry. No new paper was needed for this bounded check.

## Fan: a strong dry reference, with one screen error

Methods §2.3 gives 0.2 g catalyst, 275 °C, 4 MPa, DME/CO/H2 = 5/35/60, and GHSV 10,000 mL gcat−1 h−1. Figure 6 caption gives 200 kPa DME, 1.4 MPa CO, 2.4 MPa H2 and **the same 10,000**. No 9000-versus-10,000 conflict is present in this original. The screen now uses 10,000 and no longer treats the initial transcription error as unresolved source uncertainty.

Figure 6 supports approximately 30% DME conversion, near-98% MA selectivity, and roughly 0.4–0.5 g MA gcat−1 h−1 after an initial induction period. The time axis extends slightly beyond 500 h and includes an axis break. §3.7 separately says termination at TOS = 514 h and a plateau spanning over 520 h; abstract/conclusion repeat over 520 h. Thus “roughly 500 h of operation” is a defensible summary. “Over 520 h at steady output” or an exact integrated mass should not be reconstructed from conflicting prose. The preceding 26 h precoking and initial reduction/conditioning belong in a complete operating-cycle comparison.

H2/DME = 12 is the inlet molar ratio. It gives neither H2 conversion nor net consumption. The laboratory experiment does not demonstrate a recycle loop, so “H2-rich cofeed” is more precise than “circulating H2.” A proposed industrial recycle could reduce fresh-H2 requirements, but compressor duty, purge, methane/byproducts and net H2 uptake must be measured or modeled under an explicit boundary. Conversely, treating all incoming H2 as consumed would unfairly penalize the reference. No finite run determines eventual catalyst life or multicycle regeneration performance.

The screen correctly uses this result to reject a weak parent-MOR durability baseline. It does not establish that every dry-feed CuZn material, every water content or every process configuration would retain the demonstrated performance.

## Han: denominators and arithmetic

Main methods Eqs. 1–3 define CO2 conversion from CO2 disappearance, CO selectivity per converted CO2, and organic-product selectivity per carbon atom in the organic products, excluding CO. The organic denominator includes hydrocarbons. SI Table 2 explicitly confirms that AA contributes two carbon atoms and MA three.

For the full treatment, the conditional fraction of entering CO2 carbon recovered as AA+MA is therefore

`0.275 × (1 − 0.680) × (0.455 + 0.320) = 0.068200 = 6.82%`.

For Table 2's untreated MOR-8 reference,

`0.278 × (1 − 0.768) × (0.288 + 0.125) = 0.026636848 ≈ 2.66%`.

**These calculations are correct.** They assume that converted carbon other than measured CO is represented by the quantified organic products. The retrieved definitions do not themselves establish an independently closed carbon balance or exclude accumulation/unmeasured species. The screen appropriately labels these as inferred fractions rather than new measured balances. Neither value establishes overall recycle yield, carbon efficiency including upstream preparation, energy efficiency, or economics. CO can remain a useful recycle intermediate.

Keep the calculation tied to **SI Table 2**. The source-data Figure2 sheet instead lists AA+MA values 39.9% and 77.2%, whereas Table 2 sums are 41.3% and 77.5%; Table 4 reports 78.8%. These are small differences in reported datasets, not an invitation to combine selected entries into a more precise result. They do not erase the appreciable reported treatment improvement.

### Temperature discrepancy is confirmed

The original images of SI Tables 2 and 3 specify upstream 673 K and downstream 558 K. Main Figure 2 caption specifies 623 K and 558 K, and SI Table 4 specifies 623 + 558 K. Main text also identifies 623 K upstream as the selected optimum. These observations make a table-caption error plausible, but they do not resolve it. Retain the conflict before replication or kinetic interpretation.

### Space-time yield: a credible scale, incomplete mass definition

SI Table 4 gives 25.9 mg gcat−1 h−1 for AA+MA. Original Figure 4 uses **mmol g−1 h−1**, with values near 0.36–0.39 for representative selected conditions. The source-data sheet likewise lists 0.3591 for the 1200 mL gcat−1 h−1 point and 0.38721 for the 5 MPa point. These molar and mass scales are broadly compatible; Figure 4's numbers must not be treated as grams.

Methods load 0.5 g GaZrOx plus 1.0 g MOR-8-C1@PC, with that downstream mixture containing 0.5 g zeolite and 0.5 g PC. SI Figure 37 explicitly says its total catalyst mass excludes PC. That caption and the nominal GHSV suggest that the authors often normalize to GaZrOx plus zeolite, but do not unambiguously define the denominator of Table 4's AA+MA entry.

A useful consistency calculation illustrates this limit. Taking the methods' 21 mL min−1 total feed, 23.75% CO2, a conditional reference molar volume of 22.414 L mol−1, and Table 2's fractions yields about **25.3 mg AA+MA h−1** for the entire apparatus. Dividing this by 1.0 g GaZrOx plus zeolite gives a value close to Table 4; dividing by all 1.5 g solids would give about 16.9 mg g−1 h−1, and dividing by zeolite alone would give about 50.7 mg g−1 h−1. These are **conditional accounting examples, not corrected measurements**: feed reference temperature is not specified here, the table/figure datasets differ, and the temperature discrepancy remains. They support retaining the screen's request for a definite mass denominator.

For a matched practical comparison, report total output, output per zeolite, per total solids including promoter, and per occupied reactor volume. Fan's nominal mass-specific dry-feed productivity is much higher, but it uses a preformed DME/CO feed rather than the full CO2-to-oxygenate tandem. Neither the mass-specific difference nor Han's lower once-through feed-carbon fraction alone ranks complete routes.

### What 50 h establishes

The original Figure 4e and source-data sheet support roughly 50 h with CO2 conversion near 27% after induction. They do not establish an eventual lifetime or repeated regeneration. The workbook's AA+MA selectivity is about 76–77% through much of the run and about 73–74% at late times; it is not strictly above 75% throughout, despite that wording in the main text. This is a small observed drift, without sufficient independent uncertainty analysis to label a specific deactivation mechanism. A cautious description is “approximately maintained acetate selectivity over a roughly 50 h test,” not proof of zero deactivation.

## Shimura: now-read wet tandem comparison

The [post-upload audit](post-upload-carbonylation-audit.md) verifies the retained [main PDF](../../literature/papers/shimura2026-direct-synthesis-of-methyl-acetate/original.pdf), including visual checks of pages 3, 4 and 10. Its **93.7% combined MA/AA selectivity at 2.8% CO conversion** uses 0.5 g CMA plus 3.0 g Cu-MOR, 230 °C and 5 MPa. The maximum **3.22% yield** belongs to a different ratio, 0.75 g CMA plus 2.25 g Cu-MOR. The **10 h** time course instead uses Y-containing CMYA, with approximately **7 h induction** before AA/MA selectivity settles near 85%. This evidence strengthens the practical reference requirement without establishing high single-pass yield or durability of the maximum-selectivity case.

The reported maximum **0.67 mmol g−1 h−1** still lacks a verified mass definition here; the main tables also do not supply the mathematical selectivity definition needed for interstudy normalization. The [SI](../../literature/papers/shimura2026-supporting-information-for-direct-synthesis/paper.md) is now represented by a metadata-only, unread package. Original printed granule units and differing apparent gas-flow bases for GHSV also need clarification before replication. None of these unresolved details changes the reported low-conversion conclusion. Do not import Han's denominator or manufacture a precise normalized comparison.

Cu promotion is an observed result; protection against water occupancy is not separately demonstrated by a controlled water comparison. The H-MOR water-poisoning explanation is explicitly speculative in the main text. The existing study therefore needs a reproduced relevant reference, an induction-aware comparison and a real drying decision, as now specified in the screen's minimal gates.

## Is the conditional experiment worth retaining?

Yes, as a **bounded process-validation question** when a real wet feed and a real drying alternative exist. A balanced dry/wet/recovery comparison on an existing strong material can establish whether moisture tolerance changes useful output enough to avoid a particular separation. It can be informative even if the best answer is a conventional drying or recycle choice.

It does not yet exceed prior art merely by adding a water step, an adsorption fit, a hydrophobic material, or a withheld transient. Han already targets water protection; the screen identifies other wet-operation and product-inhibition precedents. A new contribution would require a consequential prediction that those existing results cannot supply for the selected feed and material. The proposed model should first compete with ordinary inhibition and transport explanations. Inferring “working-state occupancy” from a rate fit would not independently identify that occupancy.

Three refinements preserve the useful scope:

1. Specify a real feed/comparator before commissioning a campaign. A dry-feed material and a hydrophobic wet-feed material need not be the same best choice; evaluate the actual alternative while preserving matched tests for causal interpretation.
2. Define recovery, output and the observation horizon before testing. A finite wet/dry experiment can reveal reversible inhibition or persistent loss under those conditions; it cannot prove irreversible site damage or lifetime moisture tolerance.
3. Interpret a readily predicted water penalty smaller than drying cost as a **resolved operating decision in favor of tolerating water**, when the common boundary supports that conclusion. It is a reason to end mechanistic expansion, not evidence that the practical result lacks value.

The updated screen now specifies entry and measurement gates, independent wet-step/sham beds, a withheld feed history, net integrated acetate units and separate product/carbon accounting. These complete the bounded study design without establishing novelty from the protocol alone. The screen's modest scientific/practical confidence is appropriate. No strong new substantial-program claim follows from the corrected benchmarks, and the one Fan transcription error does not change the portfolio recommendation.
