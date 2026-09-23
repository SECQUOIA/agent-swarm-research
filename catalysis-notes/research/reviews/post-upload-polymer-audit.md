# Polymer research after the uploaded full texts

2026-09-16. Bounded audit of the existing polymer catalyst-use proposal. No new research direction, experiments, or knowledge-base edits were made. The findings below distinguish corrections to the current handoff from qualifications of historically accurate patent-only reviews.

## Implementation status

**Implemented on 2026-09-16 after authorization.** The current exposure/recovery design, value review, initial screen and makeup calculation now use the verified three-charge Na schedule and `B = 2f` as the published comparator. Patent accounting now separates Science's 80.1% apparent conversion from the patent's 69.8% record and retains the carbon/mixture limitations. The earlier independent, protocol, makeup and coke reviews have dated source corrections; their historical reading scope remains explicit.

The active screen now consistently uses the already refined 2-pentanone hypothesis and the minimal controlled sequence in the falsifiability review. It specifies live null outcomes, practical comparison, closure/expansion gates and separate confidence judgments. It does not initiate another adsorbent or contaminant program. The dissertation and patent regeneration limits remain unresolved rather than being filled by inference.

Verification: local Markdown targets in the nine revised polymer files resolve; `git diff --check` passes for those files. Exact arithmetic independently gives `B/f = 2` for the published schedule and `3/2` for the illustrative alternative; residue-subtraction calculations give 80.0566% and 69.8% respectively. These checks verify documentation and arithmetic, not experimental performance. Literature-note curation and repository-wide status/index updates are assigned to the coordinating agent and sole literature worker; this researcher did not modify those files.

The audit findings below preserve the basis for these implemented changes. Their requests to update polymer files are now completed.

## Decision

**Yes: the polymer files need substantive updates. Retain the bounded exposure/reuse study, but use a stronger, now explicit published makeup benchmark.** The new Science article and SI resolve the Na addition schedule and provide a different scale-up mass record from the patent. They strengthen confidence that the clean-feed reference can be reproduced; they do not establish the proposed ketone-dependent Na loss or a practical improvement from controlling it.

The existing final decision remains reasonable: polymer is a useful finite study, conditional on the platform, rather than an established substantial original program. The current evidence does not independently justify moving it above Ag. This review does not assess the newly uploaded Ag evidence.

## 1. Correct the Na makeup benchmark

**Verified evidence:** Conk et al., *Science* 385, 1322–1327 (2024), DOI `10.1126/science.adq7316`, original PDF page 4, **Figure 4B and its caption** explicitly specify three total 1 g PE charges. The initial mixture contains 400 mg WO3/SiO2 and 400 mg Na/γ-Al2O3. In the supplemented sequence, **400 mg fresh Na/γ-Al2O3 is added before the second charge only; the third charge receives only PE**. The plotted supplemented outputs remain near the first-cycle output over this three-charge sequence. I visually inspected the original page. The bars should not be treated as exact numerical raw data.

The patent prose ambiguity about “repeated three times” is therefore resolved for the published Science experiment. Its supplement mass is no longer unknown. The figure uses the label “Replaced Sodium,” but its caption describes addition to the retained mixture; this is not evidence of selective removal of spent Na material.

**Files requiring an update or a prominent later-evidence note:**

- [Makeup calculation](../calculations/polymer-makeup-burden.md): the opening unknown-dose statement is obsolete. The illustrative policy of adding 0.4 g before every later charge remains mathematically valid, but is not the closest published comparator.
- [Independent makeup review](polymer-makeup-accounting-review.md), [patent accounting](polymer-patent-benchmark-accounting.md), and [patent protocol review](polymer-patent-protocol-review.md): preserve the historical limits of the patent rendering, then link this resolved Science benchmark.
- [Exposure proposal](polymer-exposure-falsifiability.md) and [value review](polymer-value-after-patent.md): specify the actual published schedule in the clean-feed/makeup control.

With the existing notation, three charges under the disclosed schedule consume 1.2 g fresh catalyst solids, compared with 2.4 g for three fresh 0.8 g charges. If `f = ΣY_i/(3Y0)` is the mean accepted polymer-derived output relative to the fresh reference, the existing general equation gives **`B = 2f`**. Thus `B = 2` at equal mean output, conditionally. The old illustrative every-later-charge policy gives `B = 1.5f` over three charges. Neither is a measured economic benefit or a universal lifetime bound. Reliable polymer-carbon attribution, retained inventories and complete cycle time remain necessary; the published plot alone does not close those balances.

**Research consequence:** a new dose or exposure model must improve on, or explain a useful limit of, this disclosed once-in-three-charges supplementation schedule. Demonstrating fresh-Na rescue, stable W-normalized output for three supplemented charges, or a higher W TON is already covered by stronger prior art than the old missing-dose language suggested. Rescue still does not uniquely identify the damaged molecular function or prove that W sites are unchanged.

## 2. Keep Science scale-up data separate from the patent

**Verified evidence:** Science SI **S18–S20**, particularly original PDF page S20, reports the 50 g HDPE experiment with 10 g of each catalyst, 90 mL cold condensate, **19.9658 g warm condensate**, and **29.9717 g remaining reactor solid**. It assigns **80.1% apparent HDPE conversion** by subtracting the initial 20 g catalyst from the remaining solid. I visually inspected S20 and its equation S18.

The current [patent accounting](polymer-patent-benchmark-accounting.md) correctly records the distinct patent figures: 11.81 g warm condensate in its detailed methods, 35.100 g reactor solid, and 69.8% apparent conversion, alongside its approximately 20 g narrative value. Those figures must not become the Science benchmark by implication. The uploaded SI supplies a source-specific record; it does not prove that the patent used the same run or identify which patent number is erroneous.

The SI explicitly gives the source estimate **1.00 mol propylene, 28.1% yield, 364 W turnovers**. This should now be cited directly rather than presented only as reconstructed patent arithmetic. The main article's 438 TON is for the collected propylene/butenes mixture and is not the propylene-only TON.

The prior accounting caution survives: equation S18 multiplies estimated total liquid mass by a stated *mole fraction*, then divides by propylene molar mass. A mixture-based conversion from mass to total moles would require the mixture-average molar mass; the density is itself approximated using pure propylene at its boiling point. Therefore retain the reported estimate with its assumptions. Do not relabel it as an independently corrected measured yield. Likewise, residual-solid subtraction is an apparent conversion, not a polymer-specific residue assay.

**Research consequence:** this improves the evidence base and avoids understating the published apparent conversion. It does not turn the scale-up into a high-yield propylene process demonstration or establish lifetime. Mixing, feed preparation, substantial solid inventory, ethylene supply, product collection and throughput remain material constraints.

## 3. The oxygenate hypothesis survives, with stronger alternative explanations

The uploaded full texts of van Schalkwyk et al. (2003), DOI `10.1016/S0926-860X(03)00536-2`, and Moodley et al. (2007), DOI `10.1016/j.apcata.2006.10.053`, substantively support the final proposal's caution. The previous qualifier “unretrieved original” is obsolete for both.

- **Van Schalkwyk:** original Figures 4 and 6, journal pp.148 and 150, visually confirm the distinct recycle inhibition/recovery and 200 ppm tolerance experiments. The main text pp.146–149 also describes tolerance up to 500 ppm in a once-through sequence, inhibition at higher concentrations, and a lower nominal-feed threshold in recycle. These are operating-domain results, not transferable universal poison limits. Importantly, p.149 reports carbonyl-containing material in two product purges and interprets it as formation of heavier oxygenates from 2-pentanone. Parent-ketone delivery is therefore not automatically the concentration of the species affecting the catalyst. This directly supports the existing requirement to measure transformed products and washout; it does not prove what those products are at 320 °C in a polymer mixture.
- **Moodley:** original p.158, Figures 5–6, visually confirms the 100 ppm oxygenate comparisons over 72 h at 460 °C. Ketone cofeed reduces coke markedly without an assigned additional performance penalty. The source does not show that less coke gives a useful lifetime advantage in the proposed tandem. High-conversion traces and unreported uncertainty also do not establish equality of intrinsic rates. Keep useful output and later clean-feed function as decision variables; do not upgrade coke mass to an active-site census.
- **Maksasithorn et al. (2014):** the uploaded full text, DOI `10.1016/S1872-2067(12)60760-8`, confirms that aqueous NaOH preparation treatment can preserve metathesis performance at higher W loadings while changing acidity, selectivity and induction, whereas low-loading material suffers substantial W leaching and structural change. Methods §2.1 use aqueous treatment followed by drying/calcination; §2.3 tests at 400 °C. This remains evidence against assigning destructive poisoning from Na detection alone. It is not evidence for beneficial or harmful in-reactor Na migration in the polymer mixture.

No 2-pentanone exposure/recovery study of the Na/W polymer mixture was found in the Science main text and the SI methods/results inspected here. This is a bounded reading result, not proof of global originality. The dissertation body and the patent's missing original regeneration figures still limit the record.

**Research consequence:** retain the latest falsifiable question—whether a measured exposure leaves persistent Na-function loss while W function is retained or recovers, and whether that distinction predicts tandem throughput or a makeup choice. Do not revive the early assumption that Na necessarily protects W sacrificially. The newer full texts reinforce the live null outcomes of W tolerance, transformed-oxygenate effects, and noncontaminant clean-feed decay.

## 4. The literature notes need scientific curation

Local `original.pdf` and `fulltext.md` files now exist for the Science main article/SI, van Schalkwyk, Moodley, and Maksasithorn. Several associated `paper.md` entries are marked `status: read` but their notes are generic extraction summaries rather than useful evidence reviews:

- The Conk SI note presents the title of a cited dehydrogenation paper on its last page as the file's “central outcome.” It omits the actual reuse and scale-up evidence.
- The Conk main note repeats the abstract and an editorial blurb, omitting the known makeup schedule and experimental limits.
- The van Schalkwyk note repeats an abstract interpretation about morphology without the actual concentration/recycle boundaries.
- The Maksasithorn note uses historical process background as its principal finding.

These notes should be replaced by specific source claims, conditions, locators and limitations, through the sole literature-maintenance worker. A `read` flag should not be treated as proof that these sources have been integrated into the research assessment. Moodley's current note is substantially more informative; retain its distinction between observations and the authors' proposed coke-location interpretation.

The active [decision brief](../decision-brief.md), literature status and [initial screen](../working/alternative-screen.md) also need stale access claims reconciled. Preserve historically dated reviews rather than silently rewriting what they had access to; attach a current superseding note where the conclusion or comparator changes.

## Confidence and remaining limits

**Confidence in the corrections: high** for the disclosed Na mass/schedule, three total charges, and Science SI scale-up figures, verified on the originals. The comparative material-productivity arithmetic is conditional, not experimental validation.

**Confidence in the chemical hypothesis: low to moderate, unchanged.** The new sources support a rational test and several important alternatives. They do not establish persistent ketone-induced Na loss.

**Confidence in feasibility and information value: moderate, improved for reproducing the reference.** The recipe and known makeup control are better defined. Operational exposure, assay reactivation, polymer trajectory and retained inventories remain the central experimental difficulties.

**Confidence in practical improvement: low, unchanged.** The now stronger existing makeup option raises the bar for a useful intervention. Resolving an unnecessary cleanup requirement or rejecting a damaging feed can still be valuable without producing a better catalyst.

No new literature source was identified for intake in this audit. The patent's original regeneration figures and the dissertation body remain unresolved. No literature files were changed and no KB maintenance was run.
