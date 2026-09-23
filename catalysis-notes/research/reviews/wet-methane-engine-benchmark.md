# Engine benchmark: what a 32-hour Pd-monolith test adds

Updated 2026-09-15. Independent review of Seipel et al., *Experimental Long-Term Study of a Methane Oxidation Catalyst on a Medium-Speed Dual-Fuel Engine*, CIMAC Congress 2025, paper 178. [Original paper](https://papers2025.cimaccongress.com/pdf/CIMAC_paper_178.pdf), [DOI](https://doi.org/10.5281/zenodo.15191505).

**Conclusion:** this source strengthens the practical reason to test wet, dilute methane with relatively little NO and to measure sustained outlet slip. It does not establish an NO mechanism under wet sulfur exposure or a durable catalyst benchmark. Its nominally long-term result is about **32 operating hours under several engine histories**, with substantial loss of conversion. It neither validates nor refutes the Ryu cluster's claimed wet sulfur resistance.

## Actual tested conditions

The Pd/alumina coating is on 100-cpsi cordierite, with **2.2 g Pd per litre of monolith**. The listed brick is 150 × 150 × 150 mm (3.375 L). The bypass housing accommodates two bricks, but the retrieved description does not clearly establish that both positions were occupied for every reported experiment; do not infer total Pd inventory from housing capacity.

The synthetic test uses a 25.4-mm-diameter, 50.8-mm-long core at **50,000 h−1**, referenced to **1 bar and 20 °C**. Feed contains 1050 ppm CH4 and 7.9% O2, then 250 ppm NO and subsequently 7.9% CO2. **Neither water nor SO2 is deliberately added.** Temperature ramps at 5 K min−1 from 250 to 500 °C, holds about an hour, and cools. Heating/cooling hysteresis and a small NO penalty occur; approaching the no-NO conversion at high temperature is not evidence that NO becomes a net promoter. The experiment is a dry-feed benchmark with reaction-generated water, not a wet sulfur test.

The engine is a single-cylinder medium-speed dual-fuel research engine, principally assessed at 50% load and 720 rpm. Its reference exhaust is approximately **700 ppm CH4, 10% water, 11% O2, 5% CO2 and 60 ppm NO**. The authors call SO2 negligible because the fuel is sulfur-free; no quantitative sulfur detection limit or complete lubricant-derived sulfur balance is supplied here. Reference catalyst pressure is 1.2 bar, and normalized GHSV is approximately 60,000 h−1. These are one engine's conditions, not a universal marine exhaust specification.

## What the results establish

| Observation | Supported interpretation and limitation |
|---|---|
| Engine warm-up reaches about 50% conversion near 400 °C inlet, then roughly 85–90% near 475 °C | Useful activation range for this material and history. An upstream/downstream temperature rise is observed. This is neither an intrinsic rate measurement nor a stability demonstration. |
| Retarding combustion raises inlet temperature approximately 485→517 °C and conversion 68→76% | CH4 entering the catalyst, bypass mass flow and normalized GHSV also increase. Original Fig.7 shows outlet CH4 concentration staying roughly constant. Higher conversion therefore does not demonstrate lower total slip; increased flow can increase outlet methane mass flow at the same concentration. The authors acknowledge an engine-efficiency penalty. |
| Lower air/fuel ratio changes water from roughly 9.8 to 12.3%, with temperature and CO2 changing too | Not a causal water-inhibition experiment. Opposing effects can conceal an important water response. |
| Catalyst pressure changes from 1.2 to 1.6 bar(a) at fixed normalized GHSV | Actual volumetric flow and residence time change with density; partial pressures also change. Small measured conversion differences cannot isolate a transport effect or establish intrinsic pressure independence. |
| Normalized GHSV rises 30,000→96,000 h−1; conversion falls about 87→62% despite a hotter inlet | Strong practical contact-time sensitivity over the tested configuration. Temperature, pressure and mass flow co-vary, so this is not a unique kinetic law. Larger monolith volume may help but carries packaging, Pd and pressure-drop costs. |
| Reference conversion falls about 85→35% over just over 32 operating hours | A serious operational retention problem. This is a 50-percentage-point loss, or approximately 59% relative loss of conversion; it is not a measured 59% loss of active sites. |

Original Fig.11 was inspected. Its fifteen reference measurements have GHSV approximately **60,000–71,000 h−1**, inlet temperatures roughly **500–518 °C**, and changing CH4 inlet concentrations, rather than exactly constant values. The late reference points return near the early GHSV/temperature but remain much worse, supporting substantial history-dependent loss. Nevertheless, the curve combines varied operation, shutdowns and air flushing. A partial recovery between measurement days cannot identify a unique regeneration mechanism. No catalyst speciation, deposited-poison inventory or matched uninterrupted control resolves the cause.

The reported endpoints imply an illustrative slip fraction increase from **0.15 to 0.65**, about 4.3-fold, at a common inlet flow. Actual methane mass slip requires the varying flow and inlet concentration. One cannot integrate the sparse reference points as if they described continuous operation between them. Neither operational lifetime nor regeneration cost is established.

## Fair comparison with Ryu2024 and implications for the study

Ryu's reported washcoat loading, 100 gcat Lmonolith−1 at nominal 1 wt% Pd, corresponds to approximately **1 g Pd Lmonolith−1**. At 20,000 h−1 its nominal gas flow per Pd is about **20,000 L gPd−1 h−1**. Seipel's synthetic test is approximately **22,700**, and its 60,000 h−1 engine reference approximately **27,300 L gPd−1 h−1**. Thus a factor-of-three difference in volume-based space velocity becomes only about 1.36-fold at the nominal engine reference when normalized to Pd. These are approximate throughput comparisons: Ryu's gas-volume reference, accessible Pd, washcoat geometry and thermal boundary still require matching. Seipel does not report enough coating mass here to calculate flow per total catalyst mass.

The larger differences are feed and history: Ryu's sulfur test uses 5000 ppm CH4, 5% water and 200 ppm NO, whereas the actual-engine reference is much more dilute in methane, wetter and lower in NO. Seipel operates hotter and reports negligible sulfur. No intrinsic material superiority can be deduced by comparing their conversion or duration directly.

**Recommended refinement of the existing bounded proposal:** reproduce the Ryu source pair/feed before sequentially bridging to dilute, wetter operation. An eventual 1000 ppm CH4 and 10% water point is a plausible laboratory condition informed by the engine example, not an exact reproduction of it. The first binary comparison uses 0/200 ppm NO as a diagnostic. A practical finite-NO follow-up must come from a jointly specified feed envelope; approximately 60 ppm NO alone does not justify adding sulfur to this engine example. The NO-free condition is a diagnostic boundary; this paper does not demonstrate an NO-free engine stream. Keep sulfur-free controls essential because this engine shows severe loss even when reported sulfur is negligible. Do not infer that 2 ppm SO2 is representative of this particular engine.

The practical endpoint remains integrated outlet methane at measured flow, temperature, NOx and water, with Pd inventory and any heating/regeneration burden reported. The source especially cautions against claiming success from a temperature-induced conversion rise when the engine simultaneously makes more methane. It does not justify a new regeneration program: the authors themselves point to existing reducing-pulse approaches.

## Reading and provenance

Source-update note, 2026-09-16: the [retained Seipel package](../../literature/papers/seipel2025-experimental-long-term-study-of/paper.md) and [current literature status](../literature-status.md) supersede temporary-file access records. The scientific limits below remain.

Authentic PDF `/tmp/wet-methane-screen/cimac2025-178.pdf` and extracted text were supplied by root. Methods and relevant results were read; original pages 9 and 11 were visually inspected for Figs.6, 7 and 11. No digital data, catalyst lifetime campaign, complete sulfur analysis or supplementary temperature map was available in this review. Root already routed this source to the sole literature agent; no duplicate intake or KB changes were made. Introductory climate-neutrality, GWP and regulatory claims are not adopted here.
