# Oligomerization benchmark: conversion, product quality and retained activity

**Source and decision update, 2026-09-16:** This is a historical screen of an existing idea, not an active campaign. The [decision brief](../decision-brief.md) controls current priorities. Access statements and source-request lists below describe the original review unless explicitly updated; current access is recorded in the [literature status](../literature-status.md). Availability of a full text does not mean that every claim or benchmark in it has been rechecked. No new idea or experimental campaign is started by this update.

The Fuchs main paper and thesis are now archived in the KB, so the temporary-file ingestion request below is historical. The main paper's single-bed, elapsed-history and unhydrogenated-product qualifications still apply. The added Nozik/Koninckx source checks below improve the existing comparator; they do not promote a new oligomerization program.

2026-09-15. Root source audit for the [independent opportunity screen](../working/oligomerization-value-challenge.md). These are literature observations and comparison requirements, not new experimental results.

## A useful counterexample to conversion-based durability

Fuchs, Arnold and Sauer report mixed C2/C3/C4 oligomerization over commercial mesoporous silica–alumina with and without Ni, including sequential catalyst beds and a 222-hour test. This is strong direct prior art for separating ethylene activation from acid-catalyzed growth and branching. It is also evidence that high ethylene conversion can conceal loss of the function that makes the desired liquid product. [Original paper, DOI 10.1016/j.fuel.2024.133680](https://doi.org/10.1016/j.fuel.2024.133680); [lawful repository PDF](https://publikationen.bibliothek.kit.edu/1000177148/156087948).

Root inspected the original methods and relevant results, particularly pp. 3 and 9–11. The retained original and extraction are `/tmp/oligomerization-check/co-oligomerization-saf.pdf` and `.txt`; centralized ingestion is requested in the [source handoff](../working/oligomerization-source-handoff.md).

| Observation in the original | What it does and does not establish |
|---|---|
| The long test uses 5 g of single-bed 40/2Ni catalyst, 120 °C, 32 bar olefin partial pressure, 40 bar total pressure and WHSV 4 h−1; its olefin feed is 40/40/20 mol% ethylene/propylene/1-butylene. | A meaningful mixed-feed laboratory benchmark. It does not validate the separately demonstrated tandem bed over 222 h, nor represent pure-ethylene oligomerization or the 623 K conditions of Cao's H-MFI study. |
| Ethylene conversion remains above 95%, while propylene conversion and the net butylene balance deteriorate. | The ethylene-consuming function survives better than the measured acid-dependent product growth. Newly formed butylene obscures disappearance of supplied butylene; the authors explicitly recognize this. |
| Kerosene-range material falls from over 77 wt% initially to 47 wt% at 222 h; the aggregate collected liquid contains 63 wt%. | The abstract's phrase about remaining above 63% must not be used as a time-resolved durability claim. The 63% number is a collected-product fraction, not a feed-carbon yield. |
| Regeneration occurs after 102 h at 300 °C under Ar; the next reported post-regeneration point is 126 h. Recovery is incomplete. | The record contains a recovery intervention, not uninterrupted operation. The source does not establish that the whole 24-hour gap is required active regeneration time. Incomplete recovery does not uniquely prove hard coke or permanent acid-site loss. |
| The total test collects 3.8 L of liquid; branching falls with time and only partially recovers. | Product volume and a carbon-number fraction alone do not give mass productivity, carbon closure, or specification-qualified fuel productivity. |

## Product quality changes the benchmark

The fuel-property tests use **unhydrogenated olefin mixtures**. Separate aliquots are hydrogenated to simplify the branching analysis; those aliquots do not establish the properties of a fully processed fuel batch. The tested kerosene fraction has a −38.2 °C freezing point and 304.1 °C final boiling point, outside the respective limits quoted in the paper. A narrower distillation cut, hydrogenation and blending are proposed remedies. They were not demonstrated as a fully qualified fuel pathway in this experiment. These are comparisons to the paper's stated specifications, not a current regulatory or certification assessment.

The source's C8 branching index is a useful operational observable. It is not a complete molecular description of the kerosene fraction or a substitute for its measured cold-flow properties. More branching cannot simply be scored as universally better without considering product range and application.

Fuel-property samples pool production only through 200 h, whereas the product-volume and aggregate-fraction discussion covers the longer run. The analytical gasoline C5–C10 and kerosene C9–C16 categories overlap; so do the described physical boiling cuts. Their reported fractions cannot be added as independent coproduct yields.

## Consequence for a new cofeed or pore-design proposal

A retained oligomer can accelerate ethylene consumption while also encouraging undesired secondary chemistry. Replacing retention with external cofeeding is therefore a hypothesis about **net useful output**, not a benefit demonstrated by an increased ethylene rate.

Use a boundary around the complete proposed process, including any recycle. Count all fresh feed carbon and all net product exports; internal recycle cancels from that balance. For a single reactor with an externally supplied heavier olefin, count that olefin as fresh feed. Calling it an initiator does not remove its material contribution or cost. At steady inventory, report desired-product carbon divided by total fresh-feed carbon, alongside production per catalyst mass, reactor volume and elapsed time. Over a transient, include inventory changes in retained hydrocarbons, liquid holdup and deposits.

For mechanistic interpretation, ordinary species inlet/outlet differences measure **net rates**. They cannot separate simultaneous formation and consumption of a cofed oligomer. A carbon-isotope experiment can resolve source contributions when its balance and analytical sensitivity are validated; it does not by itself identify a unique intermediate, distinguish all parallel pathways, or prove a regenerative hydrocarbon pool. Such tracing is warranted only if that distinction changes the proposed intervention.

Compare a candidate with the relevant existing mixed-feed, tandem and regeneration recipe. Include losses from product cutting, hydrogenation requirements, regeneration and any recycle burden. Do not claim aviation-fuel improvement from a carbon-number window alone. A new mechanism or measurement earns a substantial program only if it predicts a consequential improvement or a useful operating limit beyond these precedents.

## Independent check

A fresh reviewer checked the numerical and process-boundary claims against the original paper and identified the single-bed, sample-period and overlapping-cut qualifications now included above. No remaining numerical or accounting error was identified in that review.


## Newly available mechanism comparators

2026-09-16. The new source access resolves the earlier abstract-only boundary for these existing comparators. It does not establish a useful output improvement for the proposed external-acid intervention.

- **Koninckx Ni/Beta model:** the [original SI](../../literature/papers/koninckx2022-supplemental-information-for-kinetic-modeling/original.pdf), pp.2–3, explicitly converts one study's total acidity to estimated Brønsted acidity using another study's BAS/LAS–Ni relation. That is an imported characterization assumption, not an independently measured common site inventory. Table S2 gives 7.2% measured versus 16.4% modeled conversion for the 1.0 wt% Ni, 393 K entry, and 26.9% versus 19.2% for 1.7 wt% Ni. The model is important network prior art and supplies meaningful predictions; these residuals and site-count assumptions prevent calling it a uniquely validated mechanism or using it as a precise lifetime benchmark. Its fitted stabilization relation becomes linear above C9; modeled heavy-product behavior must retain that boundary.
- **Nozik Ga/H-MFI:** the [original SI](../../literature/papers/nozik2022-supplemental-information-for-role-of/original.pdf), p.3, reports approximately 64% rate retention on H-MFI after 10 h versus 30–35% on Ga/H-MFI at 523 K and 5 kPa ethylene, relative to the 5 min rate. This supports a fresh-activity/durability tradeoff, not a favorable complete-cycle result. Sections S.9–S.10 report reactant transport criteria and repeat the comparison with restricted low-space-time data and without the deactivation correction; these are substantive controls and must not be described as absent. Estimated independence of ethylene supply from transport at those conditions does not establish that retained larger oligomers or product escape are irrelevant. Nor does the sensitivity analysis establish an invariant long-term working state. The [thesis](../../literature/papers/nozik2022-propane-dehydrogenation-and-ethene-oligomerization/paper.md) is also retained; its availability closes the old acquisition request without silently merging thesis and article versions.

These sources reinforce the need to compare recovered accepted product over time, and to separate net rates, modeled coverages and independently measured inventories. They do not replace the Fuchs process benchmark or the external-site/passivation prior art.
