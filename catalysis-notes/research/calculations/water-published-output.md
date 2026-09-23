# Does the reported durability compensate for lower initial activity?

2026-09-16. Secondary analysis of published data, not a new catalytic result. Companion to [physical water management](../working/program-development/physical-water-management.md). [Calculation](water_published_output.py) · [machine-readable output](water_published_output.json).

**Within the published comparison, sustained output appears large enough to outweigh the initial penalty.** That supports studying the reported phenomenon. The source reports matched bed volumes, so the within-experiment ratio also applies on that nominal volume basis. It does not establish an advantage over an optimized catalyst or a new improvement from the proposed program.

## Source and calculation

Use the Figure 1 sheet of [Fang et al. 2026 source data](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-026-76571-8/MediaObjects/41467_2026_76571_MOESM5_ESM.xlsx), linked to the [primary article](https://doi.org/10.1038/s41467-026-76571-8). Columns A/B and G/H give reference/promoted CO conversion; C/E and I/K give their C5+ carbon selectivities. Both use 0.5 g catalyst and the same nominal feed per catalyst mass; the promoted material adds 0.025 g PDVB. The common interval containing both conversion and selectivity observations is **25–585 h**. The longer promoted run has no matching late reference; it is not extrapolated here.

Define the reported-output proxy

`Q* = integral X_CO(t) S_C5+(t) dt`.

At equal constant CO feed this is proportional to a C5+ carbon-output estimate. It remains a proxy: the spreadsheet does not provide independent interval carbon closures, replicate/time-correlation information, or an explicit correction for possible hydrocarbon-only selectivity normalization. Figure 1 reports ±2% error bounds for conversion and selectivity; these are not enough to derive a statistical uncertainty for the integrated ratio. CO2 is reported low, but no correction is silently invented. The source's typical carbon balance above 95% is not a measurement of this calculation's uncertainty.

The script linearly interpolates each series independently and integrates their product exactly between the combined time knots. It removes one exact duplicate promoted-conversion pair at 154 h; conflicting duplicate values would fail the check. It does not fit deactivation kinetics or extrapolate a lifetime.

| Basis, 25–585 h | Reference | PDVB mixture | Mixture/reference |
|---|---:|---:|---:|
| Integrated reported-output proxy, feed-carbon hours | 116.0 | 219.8 | **1.89** |
| Same proxy per catalyst plus PDVB mass, normalized to reference mass basis | 116.0 | 209.4 | **1.80** |

The second row charges the extra 5% additive mass and is not a complete-bed mass comparison, because quartz inventory is not included. The main text explicitly reports equal catalyst-bed volumes against the quartz-diluted reference: the first-row ratio therefore also describes output proxy per reported equal bed volume within this experiment. Absolute bed volume, packing details and scale-up consequences remain unquantified here.

A sensitivity case coherently shifts all promoted conversion/selectivity points down by two percentage points and reference points up by two, then reverses those choices. The resulting 25–585 h ratios are **1.61–2.24 per catalyst mass**, or **1.53–2.14 after charging PDVB mass**. This is an analyst-selected interpretation of the caption's error magnitude, not a confidence interval or a bound on all systematic errors. It shows that this particular perturbation does not reverse the comparison.

## Missing startup data and the comparison boundary

The 25 h start omits part of the initial disadvantage. To test its importance without extrapolating selectivity, retain all available conversion points from 2 h and bound unobserved selectivity between zero and one: reference 2–25 h and promoted 2–5 h. Include observed promoted selectivity thereafter.

These deliberately wide early-data bounds give a 2–585 h mixture/reference proxy ratio of **1.74–1.97 per catalyst mass**, or **1.66–1.88 after charging PDVB mass**. They are missing-data bounds within the interpolation model, not confidence intervals. The most unfavorable early bound becomes cumulatively favorable to PDVB at approximately **194 h on the catalyst-mass basis**, before charging additive mass. No conclusion covers the unobserved first two hours, experimental error, regeneration or replacement of the reference, or operation beyond the measured comparison. The startup bounds and error sensitivity above are separate calculations, not a combined uncertainty interval.

A crossover near 123 h also appears if integration starts at 25 h; that restricted-window value must not be presented as a full-startup recovery time. Neither crossover is financial payback.

## Consequence for research selection

Lower initial activity is a real formulation cost, but it does not erase the reported cumulative benefit over this reference. The stronger unresolved issue is whether a new causal rule can improve or transfer that benefit. Proposed formulations should be assessed by cumulative useful output and inventory/volume burden from the outset, with an optimized reference and realistic regeneration policy introduced before claiming a process advantage.

Reproduce with Python's standard library:

```sh
python research/calculations/water_published_output.py /path/to/ft-source.xlsx
```

The JSON records the source SHA-256, time ranges, exact calculated values and limits. An [independent review](../reviews/water-quantitative-followup-review.md) reproduced the results with separate XML extraction and numerical integration, and checked the source basis. Its corrections concerning reported error bounds, matched bed volumes and crossover mass basis are incorporated. This analysis strengthens the evidence for a worthwhile phenomenon; it does not change the ranking or establish the originality of the proposed research.
