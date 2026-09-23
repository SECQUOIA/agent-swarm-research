# Stage 1, round 1 — independent reviewer 1

Verdict: **Accept with minor revisions as a research proposal. No major issue identified.** The proposed late-addition comparison has a defensible contribution distinct from the cited demonstrations of hydrophobic promotion. The factorial challenge/sham design, absolute output endpoint, handling qualification, and independently validated pulse prediction address the central interpretive problems. The text consistently distinguishes a proposal from experimental results and formulation performance from a microscopic mechanism.

This review covers `sections/01-water.tex`, `main.tex`, `references.bib`, and `evidence/stage1-water.md`. I read `literature/AGENTS.md` and did not edit the knowledge base or inspect other reviewer reports. I checked the local Fang 2022 and 2026 primary texts, the relevant supplementary passages, Hanssen 1997, and relevant passages from Li 2023, Wolf 2019, and Brandani 2022. Publisher-indexed primary text independently supports the narrow Sengupta claim. Direct publisher opening encountered access errors; this review does not claim a fresh complete reading of every cited original.

## Major issues

None. In particular, the absence of a demonstrated damage threshold, successful transfer protocol, or successful prediction is not a defect in a proposal: the chapter provides sensible qualification and stopping decisions for those experimental dependencies. Neither a commercial comparison nor a spatial measurement of cobalt-site water is required to complete its stated formulation-level program.

## Minor issues requiring correction

### 1. “Operating boundary” overstates the coverage of the decisive comparison

**Location:** `manuscript/sections/01-water.tex:103`; compare lines 58–59, 68, 85, and 99.

**Evidence:** The decisive experiment uses one additive dose, one conditioning schedule, one selected water plateau, and one predefined observation horizon. It can establish benefit or its absence at that operating point. The conditional pulse experiment adds a local predictive test within its calibrated range. Neither experiment locates a boundary in water amplitude, exposure duration, catalyst age, or economic performance. The manuscript otherwise carefully restricts these conclusions, so the concluding phrase is broader than its own design.

**Remedy:** Replace “a controlled operating boundary for late low-dose PDVB” with “a controlled test of late low-dose PDVB at a defined catalyst state and disturbance,” or equivalent precise wording. Retain the separate conditional claim for a predictive rule within the calibrated range. A parameter sweep is an optional later expansion, not required to fix this wording.

### 2. Give “conditioned” an operational definition without implying a fully stationary catalyst

**Location:** `manuscript/sections/01-water.tex:4`, `:20`, and `:48`.

**Evidence:** The central distinction is intervention after conditioning, but the proposal specifies only “the same schedule”; it gives neither a starting duration nor a rule for selecting that schedule. Its own prior-work discussion explains that catalyst water affinity evolves during operation. Sengupta et al. report extended evolution of oxygenate loading and water signals in their operando system, which reinforces why a common clock time and a fully mature pore environment should not be conflated. This is a specification gap, not a failure of randomization or a reason to demand identical microscopic states. [Primary publisher text](https://pubs.acs.org/doi/abs/10.1021/jacsau.5c01157).

**Remedy:** State how the parent-only pilot selects and then freezes conditioning duration and feed conditions before randomization. For example, use a defined duration beyond the initial activity transient and report the preceding rate/selectivity drift. Explicitly identify this as an operationally conditioned state; steady activity alone need not prove that water affinity has stopped evolving. Do not import a duration from a different support and metal system as a universal threshold.

### 3. Complete the Hanssen reference metadata

**Location:** `manuscript/references.bib:50–54`.

**Evidence:** The current entry omits volume and pages. The local primary original begins at printed page 193 and ends at 202; it belongs to *Studies in Surface Science and Catalysis*, volume 109. This is also a contribution to the edited volume *Dynamics of Surfaces and Reaction Kinetics in Heterogeneous Catalysis*, edited by G. F. Froment and K. C. Waugh, as shown on the original first page. The DOI and cited scientific claim are correct.

**Remedy:** Add volume `109` and pages `193--202`. Prefer an appropriate chapter/proceedings entry with the edited-volume metadata if consistent with the bibliography style; correcting the missing locator information is the necessary part.

## Source support and originality assessment

- Fang 2022 already reports mixing geometry, water-cofeed contrasts, and removal of PDVB from used CoMnC followed by performance comparable to the original catalyst (local primary text, extracted pp.2–3). The chapter properly excludes physical mixing and cross-reaction transfer from its originality claim. A short mention of the removal experiment would sharpen the relationship to prior work, but it is **optional**, because removal from previously promoted carbide is not the proposed randomized late addition to commonly conditioned Co/SiO2.
- Hanssen's dry–wet–dry sequence and water pretreatment comparison are directly supported by local primary pp.2–3. Their inclusion appropriately prevents treating water-history experiments themselves as new.
- Fang 2026 supports the low-dose separate-granule longevity contrast. The manuscript correctly avoids transferring the powder co-granulate geometry and high-dose controls into that exact packing. Its criticism of equilibrium-gradient reasoning is compatible with preserving the observed functional effect.
- The single- and two-pool balances are dimensionally consistent. The two-pool construction demonstrates a specific nonidentifiability example without falsely claiming that every conceivable experiment is nonidentifying.
- Running `python manuscript/evidence/check_water_output.py` reproduced 116.0352 h, 219.8266 h, 1.89448, and 1.80427. This confirms the calculation from the retained arrays, not independent experimental uncertainty or a complete carbon balance; the chapter states those limits.
- `main.tex` provides an appropriate citation and cross-reference structure. I found no source-level LaTeX issue in the reviewed files; I did not perform a fresh PDF build or visual layout inspection in this review.

The minor corrections above can be made without adding experiments, expanding the materials campaign, or weakening the useful central question.
