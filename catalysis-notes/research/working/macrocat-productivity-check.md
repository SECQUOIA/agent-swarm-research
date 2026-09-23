# MacroCat-201S productivity scale: conditional accounting check

2026-09-15. Read-only check of the supplied MacroCat report; no external search or KB edit.

## Judgment

A rounded **~170 kg styrene per m3 loaded catalyst per hour**, or **~0.11–0.13 kg per kg catalyst per hour**, is a useful conditional reactor-train scale. It is **not a measured simultaneous operating result**, a verified net/saleable product rate, or a valid scalar pass/fail threshold for a differential cofeed experiment.

## Source quantities and definitions

- Table 1: bulk density 1.3–1.5 kg/L. Applying that specification to 260 m3 implies 338–390 metric tonnes; actual loaded mass is not separately audited. [[liao2025-industrial-application-of-macrocat-201s]] p.3.
- Tables 2–3: feed composition 99.22 wt% ethylbenzene, 0.19 wt% styrene; EB design stream 72,453 kg/h. Applying the purity factor assumes the flow denotes the full stream rather than already component-specific EB. [[liao2025-industrial-application-of-macrocat-201s]] p.4.
- Section 2.2.4: total catalyst loading 260 m3 over the two reactors; “effective space velocity” 0.4 h^-1. Its volumetric/temperature basis is undefined. [[liao2025-industrial-application-of-macrocat-201s]] p.5.
- Long-term narrative: approximately 64% conversion, selectivity >=96.3%, about 98.2% average feed load, with load changes and shutdowns. These are not time-matched to the design flow. [[liao2025-industrial-application-of-macrocat-201s]] p.6 p.9-10.
- **Important ambiguity:** original PDF Figure 2 caption p.7 explicitly describes conversion/selectivity as “expressed as weight percentage” (visually verified). The article does not give a selectivity equation. One cannot unconditionally apply a molecular-weight correction.

## Two transparent conventions

Using F = 72,453 kg/h, EB fraction = 0.9922, conversion = 0.64, and selectivity = 0.963:

| Assumed selectivity definition | Conditional styrene kg/h | kg/m3 catalyst/h | kg/kg catalyst/h |
|---|---:|---:|---:|
| mol styrene formed / mol EB converted; multiply by MW_ST/MW_EB ≈ 104.149/106.165 | 43,465 | 167.17 | 0.11145–0.12859 |
| kg styrene formed / kg EB converted; no MW correction | 44,306 | 170.41 | 0.11360–0.13108 |

These are two accounting conventions, **not a statistical uncertainty interval**. Multiplying by reported mean feed load 0.982 gives about 164.2 or 167.3 kg/m3/h, respectively, but adds another mixing-of-averages assumption. The actual mean of flow × conversion × selectivity need not equal the product of their separate means. Shutdown treatment is also unspecified. The extra decimal precision is solely to make the arithmetic reproducible; quote the rounded scale in program selection.

The inlet contains about 138 kg/h styrene under the design-stream assumption. If reported selectivity uses total outlet styrene rather than net formation, that must be subtracted; it corresponds to about 0.53 kg/m3/h. Do not automatically subtract it from a net-formation selectivity. Product-recovery losses are not audited, so call neither result saleable plant productivity.

## Space velocity is not an independent calibration

The stated flow divided by the inferred catalyst mass is ~0.186–0.214 kg feed/kg catalyst/h, not 0.4 h^-1. Interpreting 0.4 h^-1 as liquid volumetric flow divided by all 260 m3 would imply a reference liquid density near 697 kg/m3. Without a stated temperature, volume convention, or active-bed allocation, this neither confirms nor disproves the reported effective space velocity. Do not use 0.4 h^-1 to derive a second product rate or resolve selectivity conventions.

## Appropriate use

Use the scale to identify the order of catalyst inventory a future integrated model must justify. A local differential rate above it is unsurprising and does not demonstrate process advantage; the industrial denominator includes the complete two-stage bed, axial cooling, changing fugacities, and finite equilibrium approach. Conversely, a mechanistic cofeed experiment can be highly informative at a lower rate.

For later process selection, require a model constrained by measured kinetics and survival to predict full-train net styrene generation per loaded catalyst volume at stated feed, conversion, selectivity, pressure drop, heat delivery, and cycle duration. Compare that prediction with both the scale here and uncertainty in the industrial source. Do not promote ~170 kg/m3/h into a universal activity threshold.
