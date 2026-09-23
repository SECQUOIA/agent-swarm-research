# Outcome of the 2026-09-16 direction search

Synthesis of thirteen candidate screens and four independent reviews written on 2026-09-16 to find a direction stronger than the existing bounded studies. No experiments were performed; nothing under `literature/` was changed. This document is the record of what the search found, what it corrected, and what it changes in the portfolio. The screens are in `research/working/direction-search/`; the reviews are `direction-search-*.md` in this folder.

## Result in one paragraph

**No candidate reached the bar for a substantial original program.** Thirteen candidates not previously screened were examined with open-literature prior-art searches: oxide acid–base pair alkane dehydrogenation, zeolite Al-siting for an unscreened reaction, Cu/Pd-zeolite emissions durability, liquid-phase oxygenate conversion, supported-metal interface catalysis, a kinetic or site-counting method, ethane oxidative dehydrogenation, zeolite synthesis as an enabling capability, a cross-reaction water-titration rule for Zr–O pairs, retained-aromatics regeneration in methanol-to-hydrocarbons, bifunctional intimacy as inhibitor scavenging, framework Lewis acid–base pairs in hydrophobic zeolites as confined oxide-pair analogues, and a mining of the open problems stated in the professors' own 2025–2026 papers. Every screen recommended against promotion; five retained a bounded diagnostic; independent review lowered two of those five further. Reviewers found and corrected three substantive errors in the screens. The search also produced one small methodological result on during-reaction titration that has been added to the standards, and a diagnosis of why the screening template tends to produce diagnostics rather than programs.

## Ranking of the retained diagnostics

Judgments in words, following `standards.md`. Independent reviews overrode the screens' self-assessments where they disagreed; disagreements are preserved in the linked reviews.

| Candidate | Screen | Independent review | Standing after review |
|---|---|---|---|
| Cu-SSZ-13: desulfation atmosphere and irreversible Cu loss per event | Bounded diagnostic; "clearer operating decision than wet methane" | [Review](direction-search-cu-desox-independent-review.md): He 2025 already compared regeneration with and without NO + NH3 at the conversion level (minor effect); Cummins 2013 patents already show matched reductant-versus-temperature sulfur removal; design faults (wrong comparator arm, ammonium-sulfate-forming sulfation, 5-point EPR target near noise, about 50 specimens) | Documented diagnostic, ranked alongside wet methane, below Ag and polymer; natural home is a protocol-knowledge option under the zeolite-durability program. Portfolio reviewer ranked it higher (second tier); the specific review is followed here because it verified sources the portfolio reviewer did not. |
| m-ZrO2 ketonization: water dependence of slow loss and non-oxidative recovery | Bounded diagnostic with promotion gate | [Review](direction-search-ketonization-independent-review.md): NREL's own TEA shows lifetime down to three months changes cost by under 1%; NREL deck shows the wet/dry deactivation contrast already under study by the route owners; Lin 2023 shows full reversibility on anatase; reference-return design confounds k_d with the purge under test | Documented conditional check below the zirconia styrene pilot; only the water-only exposure/recovery arm is worth adding if that pilot commissions. |
| Methods: during-reaction titration in packed beds | Bounded calibration pilot | [Review](direction-search-methods-independent-review.md): front physics is textbook (Wheeler–Robell 1969) and Wrasman 2024 already states upstream-first coverage; the linear-intercept consequence, the identifiability point and known-spectator calibration are the only unpublished parts; Davis 2018 attribution withdrawn | A standards correction (applied) and an optional calibration; not a program. The [plug-flow model](../calculations/titration-front-regime.md) sharpens the condition: equal per-pass uptake on all titratable classes hides heterogeneity at any front sharpness. |
| Zn/MFI ethane aromatization: paired-Al fraction and cation re-speciation across regenerations | Materials-conditional diagnostic | Not separately reviewed; portfolio reviewer ranked it fourth | Documented diagnostic without a table entry; pair loss under steam and Ga's pairing-insensitivity for ethane weaken it. |
| m-ZrO2 PDH site identity: dry-18O2 uptake and CO-treatment H2/CO2 balance | Add-on to the zirconia pilot only | Not separately reviewed; portfolio reviewer ranked it fifth | Documented add-on; Jaegers 2024 already removed reduction as a requirement at 723 K. |
| Ru polyolefin hydrogenolysis: methane fraction versus H2 pressure across alloys | Do not promote; optional diagnostic | Not separately reviewed; ranked sixth | Documented only. |
| Cross-reaction Zr–O water rule (ketonization, ethylbenzene, propane) | Do not promote | Portfolio reviewer independently reached "not substantial as proposed"; Iglesia's patent WO2024177986A2 already transfers water management across dehydrogenation and hydrogenation; ketonization water effect is not pair titration | Closed as a single-rule program; a frozen ethylbenzene-to-propane transfer prediction remains a cheap appendix to the zirconia pilot. |
| Ethane ODH (M1 CO2 origin at industrial conversion) | Do not promote | Not separately reviewed | Documented; boron ODH, Te loss, chemical looping and pellet transport are all occupied by expert groups and industry. |
| Zeolite synthesis: paired-Al fraction at fixed composition and Cu-CHA durability under HTA + SO2 | Do not promote; materials-conditional diagnostic | Not separately reviewed | Documented; every ingredient established, only the fixed-composition durability comparison open; pair-rich frameworks may be less stable. |
| MTH retained aromatics: dry thermal swing versus burn | Do not promote | Not separately reviewed | Documented; Schulz and Lee/Choi already separated desorbable from combustible deposits on MFI; DICP steam regeneration on CHA is practiced. |
| Bifunctional intimacy as inhibitor scavenging | Do not promote | Not separately reviewed | Documented test design (sign test on the proximity factor versus inhibitor concentration); Hu/Noh/Iglesia 2023 already showed the cascade needs no scavenging channel, and Fischer's inlet-impurity control was negative. |
| Framework Lewis acid–base pairs in hydrophobic zeolites (Zr-, Hf-, Sn-Beta) as confined ZrO2-pair analogues | Do not promote; no table entry | Not separately reviewed | Closed M–O–Si pairs are chemically implausible: Yue 2021 DFT gives C–H barriers of 242–301 kJ/mol on Sn-Beta and DeMuth 2024 gives 251 kJ/mol for Zr–O–Si against 84 kJ/mol measured on m-ZrO2; the same organozirconium is active on Si3N4 but gives 0.27% conversion on silica; Bell's 2026 Account says nested Sn/Zr/Ti/Hf sites are closed and inactive; siliceous single-site PDH (Zn, Fe, Co, Cr, Ga) is owned. A one-day blank comparison remains as a zirconia-pilot add-on. |
| Open problems stated in Gounder/Iglesia 2025–2026 papers (22 inventoried) | Strongest candidate (what hydrothermal aging changes in the Cu-CHA oxidation half-cycle; whether O2 compensation survives severe aging) does not meet the threshold | Not separately reviewed | Every checkable stated problem is already being pursued by its authors; a stated open problem is a declaration of intent. Residue: owner-supplied frozen predictions (Gjetja O2 ratio; Saxena Al-per-cage) attached to the zeolite-durability program. |

None of these displaces Ag Ni-retention as the first bounded study or polymer ethenolysis as the second. The current portfolio statement remains "no substantial lead established; bounded studies retained".

## Corrections produced by the search

Reviewers found the following errors, now annotated at the head of the affected screens:

1. The Cu screen misread He/Ding 2025: that study did regenerate with and without NO + NH3 and found the atmosphere effect minor at the conversion level. It also missed Cummins' 2013-priority patents with matched reductant-versus-temperature comparisons, and mis-attributed DOI 10.1021/acs.iecr.8b04543.
2. The ketonization screen omitted NREL's lifetime-insensitive TEA result, the NREL deck showing the wet/dry deactivation contrast already under study, and Lin 2023's full-reversibility finding; it transcribed η as 0.96 instead of 0.94.
3. The methods screen attributed to Davis 2018 a claim ("linear decrease shows every Zn site equally active") that is not in the manuscript, and understated Wrasman 2024's prior statement of upstream-first coverage.
4. The bifunctional screen flags that `literature/topics/metals-oxides-cox-ft-and-lohc.md` (line about Fischer 2023) states "polyaromatic cofeeds suppress the enhancement", which the local full text does not contain. This is a knowledge-base correction for the literature worker; research agents do not edit `literature/`.

## Why the template produces diagnostics

The [portfolio review](direction-search-portfolio-review.md) diagnosed three causes, and this synthesis accepts them:

- "One reaction, one uncertainty, two alternatives, smallest campaign" yields a binary question on one process, which reads as narrow.
- The prior-art test was being applied to interventions rather than knowledge; `standards.md` asks for the narrow additional knowledge, not a new intervention.
- No promotion threshold was written down, so the safe verdict was always "diagnostic".

The reviewer's proposed bar (substantial by breadth of consequence, decisive first campaign, knowledge novelty after a documented search, frozen prediction as expansion gate) has been added to `standards.md`. The two third-wave screens written against that bar (MTH regeneration; bifunctional scavenging) still failed, in both cases because the probable outcome confirms current practice and the knowledge is already partly published. So the bar is reachable in form but was not reached by these candidates; the template is not the only obstacle. Mature fields are mature because their owners are already measuring the next obvious thing, and every candidate here had an identified owner who had started.

## What would still be worth doing at low cost

Cheap items that attach to already-retained pilots, each with a frozen prediction:

- On the zirconia styrene pilot's m-ZrO2 batch: a water-only exposure and recovery arm (ketonization H4), and a frozen ethylbenzene-to-propane transfer prediction of the water-titration and product-cleaning constants (cross-reaction screen, narrow remaining question).
- Under the zeolite-durability program: the Cu-SSZ-13 desulfation-atmosphere comparison with the corrected design (NO present in both arms, Cu-sulfate-forming exposure, 10-point EPR resolution, sulfur balance), only after reading Shen 2019, Gao/Mossin/Vennestrøm 2025 and the He 2025 SI.
- Before any site-normalized claim in the Ag or zirconia programs: record titrant breakthrough during in-situ titration and, if feasible, calibrate on a mixture of known spectator fraction.

## Territories still unexamined

The portfolio reviewer named three (bifunctional scavenging, MTH retained aromatics, oxygen-carrier design for chemical-looping ethane ODH); two were screened in the third wave and declined, and the ethane-ODH screen judged chemical looping occupied by Li, Wachs and Kondratenko. A fourth wave screened confined framework Lewis pairs (declined on computed barriers and Bell's negative silica results) and mined the owners' stated open problems (all already in progress). Territories connected to the professors' interests that no screen has examined include Fischer–Tropsch under water-rich CO2-derived syngas with Iglesia's transport framework, and reactor-scale cyclic or looping operation in which the professors' kinetics are inputs rather than the object. Both are either speculative or owned; neither is promoted, and no further search is scheduled.

## Literature handoff

The consolidated [handoff list](direction-search-literature-handoff.md) gives every DOI cited by the screens and reviews that is absent from the knowledge base, plus the Fischer 2023 "polyaromatic cofeed" topic-sentence correction. Ingestion is low priority because no direction was promoted.

## Integration into retained programs

The search's usable residue was written into the existing programs rather than new entries: a site-count reporting rule and a decisive TFE-titration design in the [Ag program](../programs/ag-selective-oxygen-use.md); four frozen-prediction add-ons in the [zirconia pilot](../programs/zirconia-styrene-oxygen-fate.md); two protocol-knowledge options in the [zeolite-durability program](../programs/zeolite-durability-and-measurement.md); and a Ni-carbonyl caveat on the CO-addition policy in the [CO/CO2 note](../working/co2-practical-challenge.md).
