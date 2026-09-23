# A conditional industrial productivity scale

2026-09-15. Arithmetic for interpreting the [zirconia pilot](../programs/zirconia-styrene-oxygen-fate.md). This is not a measured zirconia result, a matched-catalyst comparison, or a verified plant mass balance.

## Source inputs and what is combined

The [MacroCat-201S industrial report](https://doi.org/10.3390/catal15040308) gives:

| Quantity | Source value and location |
|---|---|
| Designed ethylbenzene stream | 72,453 kg/h, Table 3 |
| Ethylbenzene in the reported feed | 99.22 wt%, Table 2 |
| Total loaded catalyst volume | 260 m³, section 2.2.4 |
| Catalyst bulk density specification | 1.3–1.5 kg/L, Table 1 |
| Long-run conversion/selectivity scale | About 64% conversion and at least about 96.3% selectivity, section 3.2 |

These quantities were not all reported as simultaneous calibrated observations. Combining a design flow, a composition table, density specifications and approximate long-run performance produces a **scenario**, not an independently closed production measurement. The report is supplier/operator affiliated.

## Calculation and basis ambiguity

If the designed stream is the mixed feed and selectivity is molar styrene per converted EB:

```text
styrene mass rate = 72,453 × 0.9922 × 0.64 × 0.963 × (104.1491/106.165)
                 ≈ 43,500 kg/h.
```

However, Figure 2's original caption describes conversion/selectivity as weight percentages; no explicit selectivity equation was found. If 0.963 instead denotes kg styrene per kg converted EB, omit the molecular-weight factor: about 44,300 kg/h. The [independent source/arithmetic check](../working/macrocat-productivity-check.md) verified the original table/caption and both cases.

The feed also contains 0.19 wt% styrene, about 138 kg/h at this design stream rate. The source does not resolve whether its reported selectivity subtracts that inlet styrene. The calculations above interpret selectivity as formation from converted EB; they cannot certify that the paper's reported output uses this net basis. The distinction is small on the present rough scale but must be resolved for an exact balance.

Both cases give a rough scale of **170 kg styrene/(m³ loaded catalyst·h)**. Combining the loaded volume with the bulk-density specification implies about 338–390 tonnes of catalyst, or roughly **0.11–0.13 kg styrene/(kg catalyst·h)**. The ambiguous stream/selectivity basis and nonsimultaneous inputs do not warrant finer precision. These are scenario averages over both beds; they are not intrinsic rates or a demonstrated economic break-even point.

## How to use this scale

Use it to check denominators and the magnitude of an eventual process comparison. Do not declare success because a differential zirconia rate exceeds it. The industrial average includes changing temperature, composition, pressure and catalyst history across two adiabatic beds; a local laboratory measurement samples one condition. Zirconia packing density, shaped-body activity, transport, heat supply, restart and lifetime still matter.

The same report quotes an effective space velocity of 0.4 h−1 without a sufficiently explicit basis to reconstruct all the flow/loading numbers here. Do not use that number to silently replace the reported stream flow or catalyst volume. A plant-level threshold requires a common process boundary and an integrated reactor comparison. Until then, the cofeed pilot can test sustained net chemistry and identify losses, but cannot certify commercial viability.
