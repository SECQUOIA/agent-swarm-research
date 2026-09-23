# Stage 2, round 1 — independent reviewer 1

Verdict: **Accept with minor revision as a research proposal. No major issue identified.** The chapter develops a credible compatibility and recovery program rather than assuming that steam causes the published Ar-aged decline. Its originality is narrower than carbonate stabilization or regeneration, and that distinction is supported by the closest cited primary work.

## Review scope

I independently reviewed `manuscript/sections/02-cyclic-oxides.tex`, `manuscript/evidence/stage2-cyclic.md`, the new bibliography entries, and the current 14-page `manuscript/main.pdf`. I checked relevant primary passages in Gao 2020, Brody 2022, Barckholtz 2021, Chacko's 2025 dissertation, and Fereres 2018. Brody's Table 1 and Chacko's printed carbonation equation were also extracted directly from their original PDFs. Targeted online searches checked the steam/LSF/coating question and adjacent molten-salt regeneration work. I did not read other review reports, communicate with reviewers, or edit the chapter or knowledge base.

## Major issues

None. The experimental unknowns are properly treated as qualification decisions. A proposal does not need demonstrated steam damage, a measured Li-loss rate, or a successful reset to be complete. The existing design includes independent specimens, intermediate endpoints, wet and dry timing controls, a shared reset, direct Li inventories, functional output, and prospective validation. Those are the necessary components of the stated program.

## Minor issue requiring correction

### State the steam main effects explicitly, and keep the null conclusion conditional on recovery

**Location:** `manuscript/sections/02-cyclic-oxides.tex:66–72` and `:118`.

**Evidence:** Equation 10 tests whether the *timing effect* differs between wet and dry operation. It is zero when steam produces the same persistent loss in both timing arms. The instruction to compare each arm with Ar is useful for overall performance, but that comparison also changes CO2 exposure history. For the primary compatibility question, the design already provides better matched comparisons: wet concurrent versus dry early, and wet delayed versus dry late. These isolate the water substitution within each CO2 schedule. The text recognizes equal damage in the wet arms but does not explicitly require these direct contrasts or their uncertainty intervals.

In addition, both wet arms receive CO2 and the common carbonation/oxidation reset. Recovery to baseline therefore establishes compatibility *with that recovery treatment*. It does not establish that unassisted steam purging needs no CO2 or restoration. The final statement that unnecessary protection can be ruled out should distinguish a lack of benefit from concurrent CO2 from a lack of need for any recovery intervention.

**Remedy:** Add the two planned simple contrasts, `q_wet,P − q_dry,early` and `q_wet,R − q_dry,late`, with intervals against the predeclared consequential loss. Keep the Ar comparisons as overall formulation/history comparisons. Qualify the null conclusion as excluding a consequential persistent penalty after the stated reset, and, where supported, excluding an advantage of concurrent over delayed CO2 under that policy. This is an analysis and wording correction using existing arms; no extra experimental campaign is needed.

**Why minor:** The required controls and measurements are already present. This omission does not invalidate the design, but the reported contrasts should directly answer its primary question and prevent an overly broad interpretation of recovery.

## Source accuracy and originality findings

- **Gao:** The primary text supports the supported molten coating, the attributed peroxide/Fe redox mechanism, and the approximately 0.42 wt% oxygen use. The chapter properly attributes the mechanism rather than presenting it as a new finding. Its warning that the coating is already molten avoids an incorrect premise that hydroxide formation must initiate melting.
- **Brody:** The 300 g bed, 16-minute cycle, Ar purges, early and late C2+ yields, and modeled steam heat-exchange substitution are supported. The original Table 1 confirms 53.2% and 47.24%. The 10 versus 20 wt% inconsistency is real and is handled honestly. The threshold calculation gives 2.0186 added minutes per cycle and is correctly restricted to hypothetical recovery of the documented Ar-aged yield.
- **Barckholtz:** The Raman experiments used a 52/48 Li/Na carbonate mixture at 923 K and several hours per condition. The authors explicitly lacked Raman response factors needed for absolute concentrations. The manuscript correctly uses this as qualitative chemical support, not a five-minute supported-coating law.
- **Chacko:** Despite its placement under “Future Works,” chapter 4.1 contains actual experiments with 45 wt% mixed salt on porous LSF at 800°C and CO2/O2 regeneration. The manuscript accurately credits that prior work. The original printed hydroxide-carbonation equation lacks the factor of two; the manuscript's correction is chemically correct. Attribution of regeneration H2 to coupled water/iron chemistry remains clearly an interpretation.
- **Fereres:** Section 3.6 supports the 30-day air exposure followed by CO2 at 640°C and incomplete restoration under the tested treatment. The manuscript correctly identifies prevention versus incomplete recovery as existing prior art rather than its own general discovery.
- The online search also found the adjacent [Vogt-Lowell et al. molten-salt ODH/carbon-capture study](https://doi.org/10.1002/cssc.202401473) and an [official 2023 NETL presentation](https://netl.doe.gov/sites/default/files/netl-file/23CM_CC28_Li.pdf) describing carbonate/LSF regeneration observations. These reinforce the already acknowledged regeneration precedent; they do not establish the proposed equal-dose, steam-specific persistent-function experiment. I found no verified novelty-defeating source in this scoped search. That is not a universal originality guarantee.

## PDF and presentation

I inspected extracted PDF text and rendered pages 8, 10, 12, and 14, including the section opening, experimental table, interaction, reset protocol, productivity inequality, conclusion, and new references. The sampled pages are readable, the equations and chemical notation render correctly, and citations resolve. No presentation defect requiring correction was identified. The chapter distinguishes ethylene from C2+ output and elapsed cycling time from continuous ethane processing.

No additional salt screen, temperature survey, vapor-species identification, or commercial demonstration is required to resolve this review.
