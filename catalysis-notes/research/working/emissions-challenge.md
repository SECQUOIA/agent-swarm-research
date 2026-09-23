# Challenge screen: does wet low-temperature emissions control offer a stronger program?

**Source and decision update, 2026-09-16:** This is a historical screen of an existing idea, not an active campaign. The [decision brief](../decision-brief.md) controls current priorities. Access statements and source-request lists below describe the original review unless explicitly updated; current access is recorded in the [literature status](../literature-status.md). Availability of a full text does not mean that every claim or benchmark in it has been rechecked. No new idea or experimental campaign is started by this update.

The formerly unresolved main texts for Tyrewala's engine study, Nygård's N2O model, Jensen's Pt–Rh study, Wenig's engine study and Yan's HCN hydrolysis are now retained and marked read. This removes their access gaps without establishing a new useful intervention. The [N2O screen](n2o-mechanism-opportunity.md) still distinguishes nitrogen residence time from a unique elementary-path assignment.

Date: 2026-09-15. **Decision: do not promote an emissions program on the evidence examined.** The practical need is strong, but this screen did not identify a distinct, supported intervention with a better combination of originality, feasibility, and likely practical benefit. This is a bounded rejection of the proposals examined, not a judgment that emissions research is exhausted. The later [N2O mechanism review](n2o-mechanism-opportunity.md) retains a nitrogen-residence-time test, but finds no unique nitrate-versus-Cu isotope discriminator. See the [current portfolio](../README.md) for subsequent priority changes.

## The practical target is important

A useful advance would preserve NOx removal during wet, low-load operation while preventing NH3 slip and N2O formation, including emissions released during the subsequent warm-up. For carbon-containing cofuels or lubricant-derived oxygenates, it should also prevent HCHO from becoming HCN. HCHO is not an intrinsic product of chemically pure NH3/H2 combustion; a carbon source must be specified.

For an initial laboratory comparison, a concrete **chosen screening target, not a regulation or performance forecast**, would be simultaneous ≥90% NOx conversion, ≤10 ppm NH3, ≤1 ppm additional N2O, and no detectable HCN with an experimentally validated detection limit of ≤1 ppm. Test at 200–250 °C, 20% H2O, 500 ppm NO, 500–1000 ppm NH3, and 10% O2 at a fixed practical monolith space velocity. Add a separately justified HCHO challenge, such as 25 ppm, only to represent a carbon-containing feed. Also measure 150–200 °C cool-down and rewarming: short-term storage cannot count as pollutant conversion. These demanding targets indicate the intended capability; the literature below does not establish that they are jointly achievable.

The appropriate benchmark is an optimized Cu-CHA SCR plus ammonia-slip-catalyst system with the same catalyst volume, metal inventory, thermal input, pressure drop, and dosing freedom. A new powder compared only with Cu-CHA alone would not establish a practical system advantage. A benefit in NOx conversion cannot offset an unreported increase in N2O, NH3, or HCN.

## What reading the actual papers changed

### Barth 2025: HCN is a working-state poison, but the design remedy is warm

The main reaction tests use 0.5% water. HCHO strongly suppresses low-temperature SCR across the composition series. Changing Si/Al and Cu loading improves HCN conversion primarily above 350 °C through the inferred ZCuOH-rich population; it does not establish a composition that avoids the cold Cu–CN state. Direct HCN transients show incomplete recovery at 300 °C and full recovery at 450 °C. The authors describe NH3 formation during cyanide conversion as probable and explicitly leave detailed HCN formation/conversion kinetics unresolved. Relevant experimental, recovery, and conclusion sections were read directly. [[barth2025-tailoring-the-active-sites-in]] p.2-4 [[barth2025-tailoring-the-active-sites-in]] p.11-14

**Consequence:** “increase ZCuOH” is established prior art for warm HCN cleanup, not a new cold-start solution. Increasing that population also raises questions about NH3 oxidation and N2O, so HCN disappearance alone is not sufficient evidence of beneficial nitrogen fate.

### Gao 2025: there is no justified single universal N2O mechanism

The actual manuscript develops BAS-catalyzed ammonium-nitrate decomposition, thermal decomposition, Cu-bound nitrate-related chemistry, and NO oxidation routes involving CuO or isolated Cu. It argues that a small nitrate inventory could evade IR detection and explicitly challenges exclusive assignments to direct Cu-centered routes. Its impregnated and in-situ nitrate experiments are useful but do not exactly reproduce every operating SCR state. The relevant TPD interpretation, mechanism discussion, and computational sections were read directly. [[gao2025-mechanistic-insights-into-n2o-formation]] p.19-21 [[gao2025-mechanistic-insights-into-n2o-formation]] p.24-34

**Consequence:** a catalyst suppressing one nominal Cu ensemble might merely move N2O formation to a different inventory or temperature. Full-cycle nitrogen accounting is necessary. The disagreement is scientifically valuable, but a proposal cannot convert that disagreement into an assumed materials-design rule.

### Collier/Usberti 2026: the useful half-cycle model and its limits already exist

The monolith study separates reduction and oxidation half-cycles and fits an N2O branch with a third-order dependence on oxidized Cu fraction. In its experiments, excess NH3 inhibits oxidation and suppresses N2O; the NH3 effects are represented empirically. Water is held at 2.3%, and the discussion explicitly reserves its mechanistic incorporation for later work. Relevant model interpretation and NH3-response sections were read directly. [[collier2026-standard-nh3-scr-and-n2o]] p.4-5 [[collier2026-standard-nh3-scr-and-n2o]] p.8-11

**Consequence:** a third-order fitted population dependence is not proof of a three-Cu transition state. The paper explicitly allows NO2/NH4NO3 intermediates consistent with its global stoichiometry; it is not a nitrate-free rival to Gao's interpretation. “Create dimers but eliminate trimers to eliminate N2O” is presently an unjustified synthesis program. Extending a half-cycle model to wetter conditions is useful but substantially overlaps the repository's existing half-cycle opportunity cards. The [follow-up review](n2o-mechanism-opportunity.md) explains why common isotope signatures do not resolve this overlap.

### Two missing primary works close tempting novelty openings

Singh et al. already measure water inhibition over Cu-CHA from 2 to 25% H2O at 200 °C and model competition between water and NO at Cu-containing intermediates. The institutional version-of-record PDF was read, including methods, the measured water trend, and mechanistic/model limitations. It concerns one catalyst composition and does not identify a generally water-tolerant material. A generic water-inhibition map or unspecified hydrophobic shell would add too little; direct Cu coordination by water must be addressed. [J. Catal. 2025, DOI 10.1016/j.jcat.2025.116071](https://research.chalmers.se/publication/545758/file/545758_Fulltext.pdf).

Nasello et al. already develop dynamic NH3 injection using stored ammonia, test a commercial monolith with 8% H2O, and find opposite NH3 effects on N2O in different temperature regimes. Their methods and dynamic-protocol sections were read in the open publisher full text. Pulsed dosing itself is therefore not an original intervention; any extension must improve complete-system emissions at matched NOx removal and NH3 use. [Emission Control Science and Technology 2024, DOI 10.1007/s40825-024-00242-7](https://link.springer.com/article/10.1007/s40825-024-00242-7).

Maunula et al. combine a review with small-scale aftertreatment experiments, including high-water conditions and several catalyst arrangements. Their experimental and system-discussion sections show that staged oxidation, SCR, ammonia storage, and thermal management are already considered together. “Integrate SCR and ammonia oxidation” is consequently not a sufficient new program. [Topics in Catalysis 2025, DOI 10.1007/s11244-025-02131-x](https://link.springer.com/article/10.1007/s11244-025-02131-x).

## Interventions rejected in this screen

| Tempting intervention | Why it does not presently exceed the existing programs |
|---|---|
| Increase ZCuOH to remove HCN | Demonstrated chiefly above 350 °C; low-temperature poisoning remains. The NH3/N2O consequences must be measured. |
| Reduce Cu clustering or engineer only Cu dimers | The active nuclearity inference is not established by the third-order rate law, and nitrate/BAS routes remain plausible. |
| Add a hydrophobic coating or raise Si/Al | Bulk water uptake and water coordination at the functioning Cu complex are different quantities. No specific matched material/measurement route was identified that would selectively change the latter while preserving Cu mobility and NH3/NO access. |
| Pulse NH3 to control N2O | Already demonstrated. The direction of the effect changes with temperature, and a downstream ASC can change the final emissions outcome. |
| Add a cold HCN hydrolysis/oxidation catalyst | Low-temperature HCN-removal materials and hydroxyl-mediated HCHO-tolerant SCR are already reported. Simultaneous NH3-rich, NOx-containing, high-water selectivity is not established by the accessible abstracts. Uptake can masquerade as HCN conversion. |
| Add downstream N2O removal | A consequential application, but no specific low-temperature, wet-feed intervention emerged that avoids reductant competition and added thermal/resource cost. Generic bed integration is insufficient. |

The last two entries are **screening leads, not literature conclusions**. The primary Cu8Mn2/CeO2 paper is openly accessible and distinguishes chemisorption from catalytic removal; its relevance is a warning against counting disappearance as conversion. A recent MnCoOx paper claims hydroxyl-assisted HCHO oxidation and HCN/formamide conversion. These findings make a generic hydrolysis-guard proposal less original; neither abstract proves suitability as a practical ammonia-engine guard bed. [RSC Advances 2021, DOI 10.1039/D0RA10177J](https://pmc.ncbi.nlm.nih.gov/articles/PMC8695306/); [Fuel, DOI 10.1016/j.fuel.2025.137480](https://doi.org/10.1016/j.fuel.2025.137480).

## One decisive experiment that could reopen the decision

This is a **gate for reopening the research direction**, not an additional recommended full program: determine whether the useful warm HCN-conversion state provides a net nitrogen-selectivity benefit under high water, or merely stores/transfers nitrogen to NH3, NOx, or N2O.

Use a pair of existing Cu-CHA compositions bracketing the Barth Z2Cu/ZCuOH-rich contrast; do not initiate a new synthesis library. Compare 0.5% and 20% water through the same 200 → 300 → 450 → 200 °C cycle with and without a finite carbonyl exposure. Give the two specimens the same inlet carbonyl dose and close the carbon balance through the entire exposure, purge, and rewarming sequence. Measure NO, NO2, NH3, N2O, HCHO, HCN, CO, and CO2 simultaneously. Where nitrogen fate is consequential but obscured by N2 carrier, run a targeted isotope experiment in He/Ar with independently calibrated N2 detection. A 13C-HCHO pulse labels the carbonyl-derived carbon; separate 15NH3/NO experiments can resolve nitrogen origin. Isotope scrambling and stored ammonia/nitrate require a reservoir balance, not simple peak labeling.

A useful reopening result would be a reproducible, composition-dependent decrease in cumulative HCN **and** N2O without increased NH3/NOx escape, carbon retention, or regeneration energy, followed by a feasible lower-temperature intervention suggested by those measured fluxes. This would identify a new design constraint absent from an HCN-only comparison. Conversely, equivalent emissions after complete reservoir emptying would reject a claimed selectivity benefit even if instantaneous HCN traces look excellent.

This experiment is feasible with established gas analysis and isotope methods, but it does not itself promise a cold catalyst. A benefit requiring 450 °C regeneration must be compared with the same heat supplied to the reference system; heating is not a free catalytic improvement. The nominally warm recovery result alone therefore cannot justify promotion.

## Confidence and decision logic

| Assessment axis | Judgment |
|---|---|
| Scientific importance of wet multi-pollutant control | High: a catalyst can exchange one pollutant for another, and both water and stored species materially affect the working state. |
| Confidence in a specific new beneficial catalytic hypothesis | Low at present: no selective material intervention survived the prior-art and competing-mechanism checks. |
| Feasibility/informativeness of the reopening experiment | Moderately high for identifying net product fate and reservoir artifacts; lower for assigning a unique elementary mechanism. |
| Likelihood of a consequential practical advance from the current idea | Uncertain and insufficiently supported to rank above the conditional pilots. Wet monolith operation, thermal cost, downstream ASC behavior, and actual engine feed histories remain material constraints. |
| Confidence that this field has no stronger opportunity | Low: the rejection is narrow, and it does not establish exhaustive novelty coverage. |

The retained polymer pilot also has substantial novelty and practical-risk caveats. Keeping it means its component-rescue experiment currently provides a clearer bounded causal test, not that polymer upcycling is intrinsically more important than emissions control.

## Literature handoff

No KB changes or maintenance were performed. Send these identified works through the existing single literature agent; retain metadata even if the original remains unavailable.

1. Singh et al., *Inhibition of NH3-SCR over Cu-CHA at high partial pressures of water: Measurements and DFT-based kinetic modeling*, DOI **10.1016/j.jcat.2025.116071**. Direct high-water mechanistic prior art. Lawful full text: https://research.chalmers.se/publication/545758/file/545758_Fulltext.pdf . Read here; a temporary local copy is `/tmp/emissions-challenge-read/singh.pdf`.
2. Nasello et al., *A Strategic NH3-Dosing Approach for the Minimization of N2O Production During NH3-SCR Reactions over Cu-SSZ-13 Catalysts*, DOI **10.1007/s40825-024-00242-7**. Direct dynamic-control prior art. Open publisher full text: https://link.springer.com/article/10.1007/s40825-024-00242-7 . Relevant body sections read here.
3. Maunula et al., *Catalytic Aftertreatment Systems for Combustion Exhaust Gases from Future Hydrogen, Ammonia and e-HC Engines*, DOI **10.1007/s11244-025-02131-x**. Practical system architecture and wet-feed benchmark. Open publisher full text: https://link.springer.com/article/10.1007/s11244-025-02131-x . Relevant experimental/system sections read here.
4. *The highly efficient removal of HCN over Cu8Mn2/CeO2 catalytic material*, DOI **10.1039/D0RA10177J**. Necessary prior art and chemisorption/conversion distinction for any HCN guard proposal. Open full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC8695306/ . Selected product-balance sections and abstract examined; full paper not read here.
5. MnCoOx hydroxyl-mediated HCHO-tolerant NH3-SCR primary study, DOI **10.1016/j.fuel.2025.137480**. Relevant competing low-temperature HCHO/HCN pathway. Publisher abstract examined; exact title/metadata and full-text retrieval remain for ingestion verification: https://doi.org/10.1016/j.fuel.2025.137480 . Do not infer N2O performance from the abstract.
6. *Simultaneous Control of Unburned NH3 and NOx Emissions From High Load Dual-Fuel Ammonia Operation on a High-Speed Diesel Engine Using a Cu-SCR System*, DOI **10.1115/1.4069586**. Engine-based SCR/ASC benchmark and aftertreatment-generated N2O warning. Institutional abstract: https://impact.ornl.gov/en/publications/simultaneous-control-of-unburned-nhsub3sub-and-nosubxsub-emission/ . Full text unread/unretrieved here.

7. Nygård et al., *Kinetic modelling of catalytic N2O removal*, DOI **10.1038/s41598-025-28647-6**. Relevant dedicated N2O-removal benchmark for ammonia-engine architectures; abstract examined, full body unread here. Open landing page: https://www.nature.com/articles/s41598-025-28647-6 .
8. *Pt–Rh Model Nanoparticle Catalysts for Selective Oxidation of Ammonia to Nitrogen: A Systematic Screening Study*, DOI **10.1021/acsanm.5c01442**. Primary low-temperature ammonia-oxidation benchmark and working-composition stability caution; abstract examined, body unread here. https://doi.org/10.1021/acsanm.5c01442 .
9. Wenig et al., *Low-emission operation of an NH3-diesel dual-fuel 4-stroke engine targeting EU Stage V performance via combined combustion control and exhaust gas aftertreatment*, DOI **10.1177/14680874261460191**. Relevant system benchmark including carbon-containing cofuel and HCHO/HCN concerns; abstract/search text only, full text unread here. https://doi.org/10.1177/14680874261460191 .
10. Yan et al., *Catalytic hydrolysis of gaseous HCN over Cu–Ni/γ-Al2O3 catalyst: parameters and conditions*, DOI **10.1007/s11783-016-0872-8**. Relevant hydrolysis prior art showing why temperature and oxygen-dependent nitrogen products must be checked; abstract read, body unread here. https://academic.hep.com.cn/fese/EN/10.1007/s11783-016-0872-8 .

Items 7–10 were not used to support a new mechanism or performance claim in this decision; they still warrant bibliographic inclusion for later assessment. No engine-emission limits or regulatory compliance claims are made in this screen.
