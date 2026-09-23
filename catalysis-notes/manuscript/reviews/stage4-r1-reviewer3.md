# Stage 4, round 1 — reviewer 3

Verdict: **approve with one minor clarification; no major issues found.**

Independently reviewed `manuscript/sections/04-silver.tex`, `manuscript/evidence/stage4-silver.md`, and the new bibliography entries. Focus: stoichiometry, carbon-source accounting, complete clocks and resource burdens, recovery versus absolute policy output, and uncertainty. No other review reports were consulted. No chapter or library files were changed.

## Minor issue

**Specify when the operating acceptance requirements apply.** At `manuscript/sections/04-silver.tex:42`, failing a conversion, selectivity, or work-rate requirement makes a policy inadmissible. The same paragraph includes conditioning and recovery downtime in the clock, and lines 70–77 explicitly price recovery through its lost output. A literal requirement to maintain the minimum work rate at every instant would reject those planned intervals before their benefit could be evaluated. Conversely, merely zeroing inconvenient low-rate intervals must not let a failing production policy pass.

**Remedy:** distinguish the prespecified production/return windows in which conversion, selectivity, and work-rate limits apply from bounded, prespecified conditioning or recovery intervals that may have zero accepted output. State that the latter retain all elapsed time and resource costs and that failure to return within the allowed window makes the policy inadmissible. This clarifies the intended decision rule without adding an experiment or changing the equations.

## Quantitative and source checks

- **Reaction accounting is correct.** For one mole EO with only epoxidation and complete combustion, ethylene consumption is `1/S`, oxygen consumption is `0.5 + 3(1/S − 1)`, and CO2 production is `2(1/S − 1)`. Independent evaluation for 0.90→0.91 selectivity gives reductions of 1.0989%, 4.3956%, and 10.9890%, respectively. These are properly restricted to reaction-level quantities at fixed EO output.
- **The prior Ni result is accurately bounded.** Parsed Kemp's original HTML to verify 13.5 wt% Ag, 88 ppm Ni, A/C Cs values of 460/430 ppm, common Re/S values, the unaged solvent-control limitation, and Table III's −4.3/−6.1 percentage-point losses. The bulk Ag:Ni ratio is 834.73. The chapter does not turn separate initial-selectivity ranges into an exact final difference or infer integrated output from accelerated-aging endpoints.
- **Carbon-source qualifications are appropriate.** Line 28 distinguishes net formation from concentration with product cofeeds, explicitly includes ethane conversion, and limits the EO/CO2 shortcut to the case where its assumptions hold. Ordinary EO cofeed is not called a selective secondary-combustion measurement. Physical flows and unfiltered net EO remain reported even when product or policy acceptance fails.
- **The productivity and recovery metrics are consistent.** `P_p` has units of mol EO per initial Ag mass per time. `B_m` is an EO-amount difference over one common remaining horizon, including treatment and return. Adding it to the corresponding continuation output gives the recovery-policy output only for that same history and clock; line 77 states this restriction. A larger within-material benefit is not mistaken for a superior material. Ag, total catalyst, and occupied volume are retained as distinct inventory bases, and resource differences use the same time boundary.
- **The familiar-model baseline is substantive prior art.** Checked Iyer 2021 original PDF pp.9–11: independently assessed oxidation, chlorine exchange, and EO degradation are integrated in a forward reactor model and compared with measured outlet rates. The chapter correctly requires calibration on the present formulation and does not treat an uncalibrated transfer as the null model.
- **Site-count restraint is supported.** Checked Iyer 2023 original PDF pp.1–4: inactive adsorption cannot be excluded, total TFE uptake is an upper-bound estimate, and the alternative estimators differ substantially. The chapter appropriately avoids a working-site census or a derived mechanistic population from that assay.

## Program validity

The proposed untreated/sham/Ni comparison protects against mistaking processing damage and rescue for improvement of a functioning reference. Common-condition contrasts and individually selected policies are kept separate. Ordinary-operation output precedes any excursion campaign, and the Ni-free chloride alternative receives an explicit comparison. A fresh null does not close a potentially different retention response.

Independent preparations, finite horizons, meaningful uncertainty, observed response times, a second training duration, and a withheld prediction make the program testable without invented performance. Neither curve collapse nor departure alone is assigned a microscopic meaning. The scope also correctly stops short of periodic service, complete industrial lifetime, or a unique Ni-to-Re oxygen-transfer mechanism.
