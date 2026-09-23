# Ethylene epoxidation: what an improvement must change

## Purpose and present decision

This is a comparison framework for the [epoxidation screen](../working/epoxidation-opportunity.md), not a new catalyst proposal or a process-economic model. A mechanistic intervention must improve a useful operating tradeoff after comparison with an appropriately promoted reference. High initial selectivity alone is insufficient.

## Practical reference

Shell reports that its EO technology has enabled operators to run for at least three years between catalyst replacements at about 90% average selectivity. This is a supplier statement, not an independently matched experiment, but it makes an 18–50 h laboratory test an early stability screen. It cannot establish competitive catalyst life. [Shell process description, updated October 2025](https://www.shell.com/business-customers/catalysts-technologies/licensed-technologies/petrochemicals/ethylene-oxide-production.html).

Temperature, pressure, conversion, product cofeeds, particle size, promoter composition and chloride conditioning must accompany any comparison. In particular, choose a useful chloride policy separately for each formulation: a shared feed chloride concentration need not give equivalent working surfaces, and maximum fresh selectivity need not maximize useful output through aging. Quantify sustained net EO production per initial total catalyst mass and per Ag mass; record promoter inventories separately. Saving a small amount of Re cannot automatically offset lower EO output, greater ethylene consumption, or shorter life.

## Stoichiometric value of selectivity

Consider stationary chemistry with ethylene as the only carbon feed and EO, CO2 and water as the only products. Define carbon selectivity `s = net mol EO formed / mol ethylene consumed`. Per mole of net EO formed:

\[
n_{\mathrm{ethylene}}=1/s,\quad
n_{\mathrm{burned\ ethylene}}=(1-s)/s,
\]

\[
n_{\mathrm{CO_2}}=2(1-s)/s,\quad
n_{\mathrm{O_2}}=1/2+3(1-s)/s.
\]

These follow from `C2H4 + 0.5 O2 → EO` and `C2H4 + 3 O2 → 2 CO2 + 2 H2O`. They also describe the final balance when EO forms first and is subsequently burned. They exclude purge losses, incomplete recovery, other products, carbonaceous deposits and oxidation of cofeeds.

| Carbon selectivity | Ethylene consumed / EO | CO2 formed / EO | O2 consumed / EO |
|---|---:|---:|---:|
| 90% | 1.111 | 0.222 | 0.833 |
| 91% | 1.099 | 0.198 | 0.797 |
| 94% | 1.064 | 0.128 | 0.691 |

All entries are calculated molar ratios, not measured catalyst results. At fixed net EO production, an increase from 90% to 91% reduces reaction ethylene consumption by about **1.1%**, reaction CO2 formation by **11%**, and reaction O2 consumption by **4.4%**. The differing percentages arise from differing denominators. They are not plant-wide emissions, purchased-feed, utility or cost reductions.

This establishes why a modest absolute selectivity change can matter in a large process. It does not establish that a proposed intervention can deliver it. A useful research contribution still requires consequential mechanistic knowledge, a durable intervention, or a transferable capability.

For the same closed product set, `EO/net O2 = s/(3−2.5s)`. Applying this relation to the [1995 patent's](../reviews/ag-older-ni-prior-art.md) reported starting-selectivity range and 50-day losses gives **about 5–9% greater EO per net O2** for the Ni-containing endpoint. This is conditional stoichiometric context, independently checked, not a reconstructed production rate. The range reflects unspecified individual starting selectivities, not statistical uncertainty. Reference-corrected selectivities and missing endpoint flows and temperatures prevent a claim about measured productivity, integrated output or lifetime.

## Judge trajectories by integrated output

For a conditioning or feed-switching intervention, calculate:

\[
\overline P_{\mathrm{EO}}=
\frac{\int_0^\tau(F_{\mathrm{EO,out}}-F_{\mathrm{EO,in}})dt}
{m_{\mathrm{cat,initial}}\tau}.
\]

Include the relevant conditioning, production and recovery periods in `τ`. Report first-start conditioning separately from genuinely recurring downtime; amortize the former only over a stated, justified service period. Integrate reactant consumption and net products over the same boundary. A time average of instantaneous selectivity ratios does not give aggregate selectivity when rates vary.

Compare against a reference that has also been optimized for its own chloride level and stabilized history. If performance differs only during transitions, assess the actual frequency and duration of those transitions before claiming a large operating benefit. A transient peak drawing from stored oxygen or carbon is not sustained catalytic production.

The [operating-aging review](../reviews/ag-operating-aging-prior-art.md) adds a concrete comparator: one defensible lower-chloride or other documented ordinary policy, selected from the reproduced material's response. Use actual flow-corrected output; equal outlet EO concentrations at different flow rates are not equal production. Charge any selectivity penalty throughout its observed evolution, and do not invoke a modeled distant crossover to erase a measured disadvantage. A nearly constant optimum chloride setting can coexist with declining activity or selectivity.

## Recovery versus Ni stabilization: the minimum decision calculation

For the revised [retention program](../programs/ag-selective-oxygen-use.md), compare three observed histories over the same explicit horizon: ordinary operation of the Ni-free material, Ni-free operation with the proposed recovery, and the Ni-containing material under its selected policy. Do not construct the recovery advantage by subtracting an assumed flat baseline if ordinary operation also recovers or drifts.

If repeatable cycling is actually established, let `f(t)` be net EO rate during a production interval of length `T`, and `g(t)` its rate during a recovery interval of length `δ`, on the same initial inventory basis. Then the cycle-average output is

\[
P_{\mathrm{recovery}}=
\frac{\int_0^T f(t)dt+\int_0^\delta g(t)dt}{T+\delta}.
\]

It exceeds a measured, stationary Ni-reference rate `P_Ni` only when

\[
\int_0^T [f(t)-P_{\mathrm{Ni}}]dt
>\int_0^\delta [P_{\mathrm{Ni}}-g(t)]dt.
\]

The left side is extra production earned between recoveries; the right side is production lost during recovery. A higher restored endpoint is insufficient when this inequality fails. If the Ni reference drifts, integrate its actual rate over the common horizon instead. If cycles keep deteriorating, do not extrapolate one cycle as a stationary average. No numerical interval is justified before measuring these trajectories.

Output alone is not the full choice. Integrate ethylene/O2 consumption, carbon loss and treatment consumables over the same histories, and report temperature and Ag inventory. A recovery that increases output but worsens resource use presents a tradeoff; neither quantity should be hidden inside an unsupported economic score. This is ordinary production accounting applied to the decision, not a new method or a prediction that recovery will outperform Ni.

## Why reactor translation remains a separate test

Berg's 2025 thesis reports axial chloride accumulation and spatial loss of reaction on otherwise unpromoted Ag/α-Al2O3. Its pilot-scale model reproduced profiles better before rapid thermal acceleration than at that onset. Those results establish close prior art for spatial moderator effects; they do not establish that a modern fully promoted formulation has the same limitation. Root inspected the methods, selected profiles and conclusions, not the entire thesis. [Primary thesis](https://doi.org/10.15480/882.14136), chapters 4–6.

Accordingly, a difference in a dilute isothermal bed should first be interpreted as a local kinetic or state effect. A process claim requires a compatible reactor model or experiment that includes product accumulation, heat removal, chloride chemistry and relevant catalyst history. Do not turn a fitted small-reactor model into a numerical plant benefit without those checks.

## Confidence

- **Stoichiometric relationships:** high, within the stated closed product set.
- **Informative laboratory comparison:** plausible, provided trace chloride delivery, net product analysis and stable catalyst conditioning can be controlled. Instrument access is unconfirmed.
- **Practical improvement from a new formulation:** presently unsupported. Neither the arithmetic nor the supplier benchmark supplies evidence that the candidate intervention works.
