# Steam-free fixed-bed benchmark: documented comparator, bounded performance claims

Updated 2026-09-16 after the uploaded main article was read. **Access history:** the 2026-09-15 assessment used the publisher abstract and three-page SI only; its main-text requests returned HTTP 403. The new local PDF supersedes that access limitation. Methods below were not known during the original assessment. The [post-upload audit](post-upload-cha-styrene-audit.md) records the resulting corrections.

## Decision

**Retain Tang et al. as a documented steam-free laboratory comparator. Keep the industrial low-steam comparison and zirconia's product-cofeed/net-output gate.** The main article supplies catalyst preparation, bed geometry, nitrogen/saturator feed preparation and the averaging protocol. It does not establish a measured optimized production advantage, quantified trace-water tolerance or repeated-regeneration durability.

Renshi Tang, Yonghua Zhou and Le Xie, *Experimental, Kinetics, and Reactor Modeling Studies of the Direct Dehydrogenation of Ethylbenzene to Styrene in the Fixed-Bed Reactor*, **Industrial & Engineering Chemistry Research** 63 (2024), 11848–11860, [DOI 10.1021/acs.iecr.4c01175](https://doi.org/10.1021/acs.iecr.4c01175). Sources: [local original main article](../../literature/papers/tang2024-experimental-kinetics-and-reactor-modeling/original.pdf) and [local original SI](../../literature/papers/tang2024-supporting-information-for-experimental-kinetics/original.pdf). Page numbers below are PDF pages. Relevant main-text passages and Equation 37 were checked by independent extraction from the original PDF.

## What the main article resolves

| Evidence | Source | Meaning for a comparison |
|---|---|---|
| Mesoporous phosphorus-doped boron nitride on cordierite; preparation and support treatment are specified. | Main p.3, Section 2.1 | The comparator is sufficiently identified for a preparation assessment; it is not an unspecified dry-feed catalyst. |
| Quartz reactor, 8 mm internal diameter, 74 mm packed height; thermocouple in the bed. | Main p.3, Section 2.2 | Bed geometry is known. A model packing density is not a directly reported weighing record. |
| Nitrogen passes through an ethylbenzene saturator; tank temperature sets inlet ethylbenzene concentration. Aromatics are collected in 10 mL ethanol cooled with ice water. | Main p.3, Sections 2.2–2.3 | Carrier, feed preparation and sampled product phase are known. The four aromatic fractions do not represent the whole reactor gas. |
| Temperature series: 773.15–873.15 K, stated flow 10 mL/min and ethylbenzene partial pressure 2,860 Pa. Values average 9–11 h after an approximately 8 h induction period. | Main p.7, Section 4.1 | The SI time series has an explicit working-state convention. It is not an 11 h proof of unchanged activity from startup. |
| At 873.15 K and 10 mL/min, increasing ethylbenzene partial pressure from 2,860 to 14,332.4 Pa decreases reported conversion from about 80% to 30% and selectivity from about 97.5% to 94.9%. | Main pp.7–8, Section 4.1 and Figure 8 | Feed chemical potential strongly affects performance. Temperature alone does not define a fair catalyst comparison. |

The SI remains useful as the reported time series. Selected **11 h endpoint values**, rather than the main article's 9–11 h averages, are:

| SI table | Temperature | Reported conversion | Reported styrene selectivity |
|---|---:|---:|---:|
| S1 | 500 °C | 14.38% | 99.17% |
| S3 | 550 °C | 66.20% | 98.91% |
| S5 | 600 °C | 78.68% | 97.14% |

Do not combine an SI endpoint with an averaged main-text quantity as though they were the same measurement. The main methods explain collection of the aromatics; the four SI fractions omit hydrogen and nitrogen and sum to approximately 100%. They cannot provide all outlet partial pressures or a complete gas-phase carbon/hydrogen balance.

## The production optimum is a simulation result

The temperature-series data calibrate an apparent kinetic/reactor model, which is then compared with a partial-pressure series. Equation 37 on main p.10 defines styrene production per cylindrical packed volume using inlet ethylbenzene molar flow and the calculated styrene yield. The quoted **0.341 kmol/(m³·h) at 873.15 K, 109 mL/min and 9,350 Pa ethylbenzene** comes from the subsequent model optimization (pp.11–12). The principal measurements used 10 mL/min.

Credit the measured dilute-feed conversion/selectivity and the model's validation domain separately. Do not present the optimum as an experiment, a catalyst-mass rate or a plant productivity. The model neglects catalyst deactivation (p.4). Its optimized flow is outside the stated 10 mL/min experimental series, so validation against composition changes does not by itself validate that flow extrapolation.

## Limits that still matter

- **Dryness:** no added steam or oxygen is a feed designation. The inspected main methods and SI do not report an independently measured ppm water concentration or a controlled trace-water-tolerance series. Lack of that measurement is not evidence that the feed was wet.
- **Rates and affinity:** verify the numeric total-pressure and flow-reference conventions, directly weighed catalyst inventory, and actual outlet gas composition before reconstructing matched mass rates or chemical affinity. Known geometry and a fitted apparent-rate model do not eliminate those questions.
- **Durability:** the 9–11 h averaging follows induction. A longer test attributed to an earlier paper is not a lifetime or repeated-regeneration experiment on this run. No regeneration advantage over zirconia is established.
- **Intrinsic chemistry:** this is an apparent reaction/reactor model. Model agreement does not prove unique elementary kinetics or replace independent transport and blank controls in a matched catalyst experiment.

## Consequence for the existing zirconia program

This source removes the need to wait for the main article before assessing a specific steam-free laboratory comparator. It also narrows any claim that steam-free styrene production alone is novel. It does **not** identify zirconia's water-derived cleaning products, show that those products limit output, or demonstrate a superior net rate under matched ethylbenzene/styrene/hydrogen activities.

The [current zirconia program](../programs/zirconia-styrene-oxygen-fate.md) remains staged: validate moisture and output measurements, apply a modest product-containing feed at favorable affinity, and advance oxygen attribution only when it can resolve a consequential prediction. A failed measurement must be repaired before interpreting catalyst performance. An analytically resolved failure of useful output narrows or stops that operating window; it does not justify an unrestricted isotope campaign.

If those gates pass, use Tang for a matched laboratory comparison under reproducible feeds and use the supplier/operator-affiliated [MacroCat-201S report](https://doi.org/10.3390/catal15040308) for its longer industrial operating history. Luyben and Dimian further require fair process accounting for selectivity, recycle and heat integration; their simulation savings are not transferable to zirconia.

**Confidence:** high that the main article reports the methods and measurements summarized here; moderate that a reproducible matched laboratory comparison can be commissioned with the remaining denominators clarified; low that existing evidence establishes a practical zirconia advantage. This update supports a better comparison, not a larger experimental scope.
