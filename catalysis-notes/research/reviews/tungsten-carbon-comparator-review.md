# Carbon-supported tungsten comparators: what reuse establishes

2026-09-16. Independent bounded audit of Ribeiro 2022 and Morais 2024. No experiments or KB edits. This review complements the [tungsten program review](tungsten-sugar-program-review.md) and [process accounting](../calculations/tungsten-process-burden.md).

**These comparators leave substantial process questions open, but do not establish W extraction as their limiting problem.** Both demonstrate useful reuse with catalyst replenishment. Neither establishes a hot W balance at substantial product concentration. The strongest next practical boundary is maintaining cleavage, hydrogenation and W retention in a product-rich or fed operation. Another dilute reuse sequence would add little unless it tests a specific causal hypothesis.

Both studies use 0.75 g of cellulose, ball-milled for four hours, with 0.30 g catalyst and 0.300 L water at 205 °C for five hours. Hydrogen is introduced at reaction temperature to 50 bar; this pressure convention matters when comparing room-temperature charging pressures. [Ribeiro 2022](https://doi.org/10.1016/j.renene.2022.10.026), sections 2.2 and 2.5; [Morais 2024](https://doi.org/10.3390/molecules29163962), sections 3.2 and 3.4.

| Evidence | Ribeiro 2022: 20%Ni–20%W/CNT | Morais 2024: 10Ni–5W/AG–CNT1200 |
|---|---|---|
| EG carbon yield, first → last reported run | 50.3 → 42.0%, six runs | 61.7 → 56.0%, four runs |
| Between-run treatment | Filter, water wash, overnight drying at 100 °C; <5 wt% fresh catalyst added before reuse | Filter, water wash, overnight drying at 100 °C; <5 wt% fresh catalyst restores 300 mg charge |
| Separate re-reduction between runs | Not specified in the inspected reuse procedure | Not specified in the inspected reuse procedure |
| Metal loading evidence | Ni 25 ± 2 wt%; W 19 ± 4 wt%, inferred through ash accounting. Used material: Ni 23, W 19 wt% | Ni 15.8 wt% by ICP; W loading explicitly unmeasured owing to equipment limitations |
| Leaching evidence | AAS of recovered cooled liquid: below detection limits; no numerical limits identified in inspected main text | No W leaching balance in inspected main/SI |

Sources: [Ribeiro 2022](https://doi.org/10.1016/j.renene.2022.10.026), sections 2.4–2.5 and 3.2.2, Table 4; [Morais 2024](https://doi.org/10.3390/molecules29163962), Table 2, sections 2.2–2.3 and 3.4, [SI](https://mdpi-res.com/d_attachment/molecules/molecules-29-03962/article_deploy/molecules-29-03962-s001.zip), Figure S4. The latter plot was checked against the original PDF.

**Calculated comparison, not reported process performance.** On the shared initial-volume basis, cellulose concentration is 2.5 g/L and catalyst/feed mass ratio is 0.40. For a carbon yield fraction Y, the nominal EG equivalent is

\[
m_{EG}=m_{cellulose}Y\frac{3M_{EG}}{M_{C_6H_{10}O_5}}.
\]

This gives the following arithmetic estimates from the initial feed and reported yields. They assume the stated initial liquid volume; sampling, temperature-dependent volume, isolation losses and downtime are not resolved.

| Derived quantity | CNT 2022 | Hybrid 2024 |
|---|---:|---:|
| EG equivalent per initial batch | 0.43 g | 0.53 g |
| EG equivalent per initial liquid volume | 1.44 g/L | 1.77 g/L |
| Five-hour average, initial-liquid-volume basis | 0.29 g EG/L/h | 0.35 g EG/L/h |
| Initial Ni inventory per cellulose mass | Approximately 10 wt%, using reported loading | Approximately 6.3 wt%, using reported loading |
| Initial W inventory per cellulose mass | Approximately 7.6 wt%, using the indirect estimate | 2 wt% nominal only; actual value unresolved |

These are inventory ratios, not consumption rates. They must not be converted into fresh metal demand without campaign balances. The high catalyst/feed ratio and dilute output identify a practical comparison requirement; they do not prove that the catalysts cannot operate at higher throughput or concentration.

Fresh makeup prevents treating the runs as an unchanged closed catalyst inventory. However, modest replenishment does not erase the evidence that recovered catalyst remains useful. Under the explicit assumption of five or three replenishments below 5% of the target charge, cumulative added catalyst is below 25% or 15% of the initial charge, respectively. Actual additions were not reported run by run. A rigorous comparison should record them, rather than either ignoring makeup or dismissing reuse entirely.

Cold liquid measurements cannot exclude dissolution followed by return during cooling. A concentration below an unspecified detection limit cannot supply a quantitative export bound. Likewise, similar final mass fractions do not close an absolute metal balance when fresh material was added, some solid was lost, and support/deposit mass may change. These are limitations of the inference, not proof of undetected leaching. The observed performance decline could reflect another catalytic function or product accumulation; the data inspected here do not adjudicate that cause.

The [Li 2020 SI](https://doi.org/10.1021/acssuschemeng.0c00836.s001), Table S2, reports 68.7 → 66.9% EG yield over seven effective cycles. Its main-article recovery procedure remains an unresolved dependency. It is therefore a serious comparator, but the apparent smaller decline cannot establish superior lifetime across different temperatures, feeds, inventories and recovery protocols. Retained output per cumulative feed and initial-plus-added metals is more informative than cycle count alone.

[Ooms 2014](https://doi.org/10.1039/C3GC41431K) demonstrates that concentrated fed-batch operation belongs in the comparator set; its maximum yield and approximately 293 g EG/L/h productivity occur at different operating optima. The large numerical gap from the estimates above is not a matched process advantage: substrate form, staging, temperature, catalyst inventory and observation time differ. Use that work to define the concentration/productivity challenge, not to claim a thousandfold superior catalyst.

The next comparison should therefore ask whether an accessible retained-W catalyst sustains the useful reaction network and bounded W export as products accumulate at meaningful output. Distinguish high feed-solution concentration, instantaneous reactive-sugar concentration and accumulated product concentration. A fed operation can change these independently. Establish the reference response before proposing a new anchor or support. If hydrogenation loss, slow hydrolysis, retained organics or handling dominate, W immobilization alone would miss the practical limitation. If a reproducible ligand-dependent loss of cleavage accompanies W redistribution, the proposed coordination–retention program has a concrete target.

Neither title establishes low catalyst cost or low process cost. Fair accounting must include support preparation, thermal treatment, feed pretreatment, dilution, makeup, separation and elapsed time. The chemistry can remain scientifically worthwhile before all those costs are quantified; practical superiority needs the corresponding evidence.

Access record: Ribeiro's author-uploaded full text was inspected on [ResearchGate](https://www.researchgate.net/publication/364471637_Paving_the_way_towards_an_eco-_and_budget-friendly_one-pot_catalytic_conversion_of_cellulose_and_lignocellulosic_residues_into_ethylene_glycol_over_Ni-WCNT_catalysts); direct publisher/university PDF retrieval failed, so figure values were taken from the article's text, not independently digitized. Morais main PDF and SI were downloaded from the publisher, with originals at `/tmp/tungsten-carbon-review/hybrid2024.pdf` and `/tmp/tungsten-carbon-review/molecules-3163434-supplementary.pdf`; both were handed to the parent for the sole literature agent. No claim is made that the Ribeiro SI was read.

Two subsequent comparator leads were routed for intake, not audited here: [Ribeiro et al. 2024, glucose-derived carbons](https://doi.org/10.1039/D4SE00823E), and [fruit-peel-derived carbons, 2025](https://doi.org/10.1007/s10570-025-06464-4). They matter when selecting a current carbon reference and comparing support preparation burdens. Their existence does not change the experimentally bounded conclusions above.
