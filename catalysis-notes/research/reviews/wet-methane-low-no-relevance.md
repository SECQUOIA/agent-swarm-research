# Low-NO wet methane oxidation: application boundary review

Updated 2026-09-16. Fresh independent challenge of the [proposed study](../working/wet-methane-value-screen.md), [experimental review](wet-methane-independent-value.md), and [engine benchmark](wet-methane-engine-benchmark.md). No experiments or platform assessment were performed.

## Decision

**Narrow the proposal to a finite test of whether the reported Pd/SSZ-13 advantage depends on NO cofeed. Its practical relevance to a low-NOx sulfur-containing application remains unestablished.** The zero-NO experiment is a defensible diagnostic boundary. It is not yet an application specification, nor does failure at zero NO justify rejecting the material for the documented engine stream.

Methane-slip control is consequential. That fact does not establish the importance of this particular missing condition. The current evidence supports a modest, platform-dependent experiment if the material can be reproduced cheaply; it does not support promoting this question to a substantial research program. Scientific plausibility of NO-dependent behavior is appreciably stronger than evidence that the dependence will change a real catalyst choice.

## Lower NO does not establish a more difficult sulfur condition

Ryu's published sulfur test supplies 200 ppm NO and 10 ppm SO2. Their molar feed ratio is 20. The proposal's illustrative 60 ppm NO and 2 ppm SO2 would give 30. Thus lower absolute NO can accompany **more NO per incoming sulfur**, not less. Seipel's engine reports about 60 ppm NO but negligible sulfur without a quantitative sulfur balance; its actual NO/S ratio cannot be calculated from that description. The 2 ppm SO2 value comes from a different laboratory study, not from that engine. [Ryu2024](https://doi.org/10.1038/s41467-024-52698-4), [Seipel2025](https://doi.org/10.5281/zenodo.15191505), [Mortensen2025](https://doi.org/10.1007/s11244-025-02114-y)

These ratios are bookkeeping, **not a proposed protection law**. NO may change hydroxyl coverage, redox kinetics or sulfur partitioning catalytically; no fixed consumption ratio or universal saturation concentration has been established here. Equal NO/S ratios at different partial pressures need not give equal rates or sulfur histories. Conversely, a response to 200→0 ppm cannot establish a consequential response to 200→60 ppm. The latter could lie entirely within a saturated response range. Total NOx also does not replace separately measured NO and NO2.

Do not claim that the 60/2 condition is harsher, more realistic, or less protected than 200/10 without evidence. It is a proposed condition whose usefulness depends on an identified feed envelope.

## Application candidates and why none yet closes the gap

| Candidate | Defensible connection | Missing condition that prevents a practical claim |
|---|---|---|
| Seipel-type lean dual-fuel engine, with MOC exposed to engine exhaust | An actual wet, dilute methane stream with approximately 60 ppm NO; substantial retention failure makes sustained slip important. | Reported sulfur is negligible; no demonstrated sulfur-driven choice or zero-NO exposure. Its roughly 500 °C operating region also differs from Ryu's 350 °C sulfur benchmark. |
| Lean natural-gas or biogas engine with sulfur from fuel or lubricant | A credible application class for wet sulfur tolerance and finite NO. | A sufficiently low-NO, consequential sulfur history at the same installation position has not been demonstrated by the sources examined. Fuel sulfur concentration is not exhaust SO2 concentration. |
| Methane oxidation after an SCR unit that removes NOx | A plausible way to produce low NOx while methane survives. | This is an installation hypothesis. The proposed location must supply adequate temperature and account for NH3, NO2, sulfur transmission/speciation, heat loss and space velocity. A binary laboratory NO switch does not establish its advantage over upstream placement. |
| Non-combustion methane-containing offgas | Such a source could avoid combustion-generated NO. | No particular stream with a consequential wet sulfur burden, practical heating requirement and credible throughput/comparator has been identified in this review. Do not import the engine feed by analogy. |

The second row is the most credible **eventual** class: a lean engine operated with low engine-out NOx and trace sulfur entering an oxidation catalyst before heat recovery. It becomes a defensible research target only when one concrete operating history jointly specifies NO/NO2, sulfur species and exposure, temperature, water, methane and flow. It is presently a candidate class, not the requested completed application demonstration. No new engine measurements or access are assumed.

### Placement is a real constraint

Villamaina and colleagues explicitly describe an MOC → SCR → ammonia-slip-catalyst sequence and study methane passing to SCR. In that architecture, NO removal downstream does not reduce NO at the upstream MOC. The MOC's NO-to-NO2 activity can also assist downstream SCR. Their laboratory results find little methane effect on the SCR catalysts except under excess NO2 at high temperature. This supports separate examination of the actual sequence; it does not establish that moving the MOC after SCR is beneficial. The source is an experimental 2018 study, not proof of a universal current installation standard. [Villamaina2018](https://doi.org/10.1007/s11244-018-1004-4)

A methane catalyst behind SCR would additionally need acceptable NH3 conversion and nitrogen-product selectivity under its actual feed. Those are conditional installation requirements, not reasons to expand the initial powder study into an exhaustive aftertreatment campaign. Without a concrete reason to choose downstream placement, omit placement benefits from the proposal's value claim.

### A second engine study strengthens realism but does not rescue zero-NO relevance

Tomin and colleagues test PdO/alumina with actual CNG-engine exhaust at a simulated post-turbine reference position. Table 4's lean points have about 540–1950 ppm inlet NO and 546–576 °C inlet temperature, far from NO-free operation. The paper identifies sulfur in grid gas and lubricant; its SO2 readings are at or below the stated 4 ppm detection limit. This establishes credible sulfur sources, not a quantitative low-NO sulfur challenge. The selected methods and sulfur discussion also show why changing engine operation alters several catalyst boundary conditions together. [Tomin2024](https://doi.org/10.1007/s41104-024-00140-8)

The already reviewed coupled-catalyst work demonstrates upstream sulfur storage and NO2 changes. It supplies prior art for exploiting those effects, not evidence that every NO-removal step creates an important new materials problem. [Existing source review](wet-methane-coupled-catalyst-prior-art.md)

## Smallest revision that preserves a useful experiment

1. **Rename its purpose:** “Does the reported anchored-Pd sulfur-tolerance advantage depend on NO cofeed?” Replace “low-NOx compatibility window” with “tested NO-cofeed boundary” until a real window is identified.
2. **Keep zero NO as a diagnostic.** At matched wet sulfur exposure, compare the reproduced cluster with the omission-treatment control and a credible practical reference. Preserve sulfur-free switches, matched thermal conditions, separate exposure histories and sham continuation. Conversion alone cannot locate sulfur or identify coupled surface chemistry.
3. **Require a consequential comparison, not merely an NO effect.** If NO removal worsens all catalysts similarly and does not change the material advantage or required inventory, the result largely confirms established behavior. A changed ranking or a large loss of the claimed advantage supports a specific material limitation; zero-NO failure still does not prove failure at finite NO.
4. **Before an application claim, test one independently chosen real finite-NO history.** The selection must jointly specify sulfur exposure and temperature, not assemble independently convenient numbers from unrelated papers. Do not run a dense NO/S library without a decision that requires it. If no application envelope is available, report the diagnostic result and stop at that boundary.
5. **Evaluate integrated outlet methane under the same imposed service.** Count measured methane flow, startup and recovery; compare actual internal temperatures and precious-metal inventories. If engine operation changes, use its new methane inlet and flow and report its energy consequence. Do not use higher conversion alone to infer less emitted methane.

A useful negative result would narrow a broad material claim. A useful positive result would show that the material advantage survives the specified cofeed removal. Both are scientifically legitimate, but neither independently proves practical improvement. Sulfur mapping, catalyst-placement experiments and a new regeneration protocol should remain conditional on a result that changes a specified decision.

## Confidence and portfolio consequence

- **Scientific hypothesis:** low to moderate confidence that this particular cluster has a consequential NO dependence; moderate confidence that NO can alter wet sulfur-associated behavior on Pd generally.
- **Feasibility and informativeness:** moderate conditional on reproducible materials, thermal control and wet-gas analytics. A bounded functional comparison is easier than a unique sulfur-partition mechanism.
- **Application importance:** methane-slip abatement is important; confidence that the proposed zero-NO sulfur boundary controls a real deployment choice is low with current evidence.
- **Practical improvement:** unestablished. The credible immediate output is an applicability limit or validation of a material claim, not a demonstrated lower-slip system.

**Recommendation:** retain this as a lower-priority diagnostic option, conditional on modest reproduction effort and a working platform. Do not rank it alongside the more concretely defined Ag or polymer decisions solely because methane emissions are important. Promotion requires an application-relevant finite-NO comparison or a transferable mechanistic result beyond the known NO effect. This review does not establish that such an opportunity is absent; it establishes that the current practical premise has not yet been supplied.

## Historical literature handoff and reading limits

**Current source update, 2026-09-16:** Auvinen2021, Sadokhina2017/2018, Tan2025, Hutter2018 and Kinnunen2013/2018 main texts are now retained. The rows below preserve original access/reading limits and are not current missing-source requests; see the [post-upload audit](post-upload-methane-audit.md) and [current literature status](../literature-status.md). Tan’s 0.3 g, 1500 ppm CH4, 5% O2, 10% water, atmospheric-pressure, 100,000 h−1 Pd/Na-IWV test is a defined wet sulfur-free comparator. Its approximately 85% conversion at 330 °C over 100 h does not establish sulfur tolerance. The additional full texts do not supply the missing joint low-NO/sulfur application envelope. NO effects observed on sulfated Pd/Pt/alumina remain distinct from proposed hydroxyl-removal or sulfur-partition mechanisms on Ryu’s zeolite.

The following were routed to the sole `/root/literature` worker for sequential **Add identified literature** processing using `/home/sgusev/repo/skills/literature/SKILL.md`; project `/home/sgusev/repo/catalisys-notes`; KB `/home/sgusev/repo/catalisys-notes/literature`. No KB edits or checks were performed here. Metadata and relevance remain required if full text cannot be recovered.

| Identifier | Relevance and artifact/reading status |
|---|---|
| **10.1007/s41104-024-00140-8**, Tomin2024, *Innovative engine test bench set-up for testing of exhaust gas aftertreatment and detailed gas species analysis for CNG-SI-operation* | Actual engine feed, sulfur-detection limit and installation reference. Authentic open [publisher PDF](https://link.springer.com/content/pdf/10.1007/s41104-024-00140-8.pdf), 2,674,598 bytes, `/tmp/wet-methane-screen/tomin2024.pdf`; extracted text alongside. Selected main methods, Table 4 text, NO and sulfur discussion read. Original figures not visually inspected. |
| **10.1007/s11244-018-1004-4**, Villamaina2018, *The Effect of CH4 on NH3-SCR Over Metal-Promoted Zeolite Catalysts for Lean-Burn Natural Gas Vehicles* | Explicit MOC/SCR order and methane/SCR interaction. Authentic open [publisher PDF](https://link.springer.com/content/pdf/10.1007/s11244-018-1004-4.pdf), 856,333 bytes, `/tmp/wet-methane-screen/villamaina2018.pdf`; text alongside. Primary HTML introduction/methods and abstract read selectively; no exhaustive original-figure review. |
| **10.1002/cctc.201701884**, Kinnunen2018, *Engineered Sulfur-Resistant Catalyst System with an Assisted Regeneration Strategy for Lean-Burn Methane Combustion* | Direct upstream-TWC sulfur protection and regeneration prior art. [Publisher](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/cctc.201701884). Abstract/exposed publisher discussion only; main/SI unread. |
| **10.4271/2013-24-0155**, Kinnunen/Kinnunen/Kallinen2013, *Improved Sulfur Resistance of Noble Metal Catalyst for Lean-Burn Natural Gas Applications* | Earlier washcoat/support-acidity and MOC/SCR integration prior art. [SAE source](https://saemobilus.sae.org/downloads/papers/2013-24-0155/Full%20Text%20PDF). Abstract only; full main unread. |
| **10.1016/j.cej.2018.05.054**, Hutter/De Libero/Elbert/Onder2018, *Catalytic methane oxidation in the exhaust gas aftertreatment of a lean-burn natural gas engine* | Thermal-management/CO heat and dynamic active-zone modeling are established. [Publisher](https://www.sciencedirect.com/science/article/pii/S138589471830843X). Abstract read only; main unread. Not used to assert a quantitative operating protocol. |

At the original review, the last three sources were prior-art requests, not full-text-verified grounds for a quantitative claim. Their main texts are now retained; no new quantitative protocol is inferred here without checking its specific source. Use current literature status rather than this historical handoff for remaining supplements or source gaps. No new full-text request was put to the user.
