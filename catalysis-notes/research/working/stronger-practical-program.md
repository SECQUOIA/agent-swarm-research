# Independent practical challenge: lower-recycle solid-acid alkylation

**Source and decision update, 2026-09-16:** This is a historical screen of an existing idea, not an active campaign. The [decision brief](../decision-brief.md) controls current priorities. Access statements and source-request lists below describe the original review unless explicitly updated; current access is recorded in the [literature status](../literature-status.md). Availability of a full text does not mean that every claim or benchmark in it has been rechecked. No new idea or experimental campaign is started by this update.

The Li Al-location article and Van Minnebruggen experimental comparator are now retained and marked read, as are the older kinetic/deactivation main texts listed in the historical handoff. The source-specific comparator update below resolves the most important former methods gap. The low-recycle alkylation idea remains nonselected: working-state branching, cumulative accepted product, internal circulation and regeneration burden still need a demonstrated favorable tradeoff.

Date: 2026-09-15. **Decision: do not promote this candidate above the bounded Ag investigation.** The practical problem is substantial, but the proposed intervention overlaps explicit mechanistic and materials prior art. No experimentally supported way to decouple selective hydride transfer from oligomerization emerged. This negative finding does not validate Ag by elimination.

## Candidate and practical purpose

The candidate was to place Brønsted acid sites in large-pore zeolites where a bulky hydride-transfer intermediate can form while adjacent confinement favors isobutane over butene. The intended benefit is sustained production of highly branched C8 alkylate with less isobutane circulation and less frequent regeneration. This would support a solid catalyst alternative to liquid-acid alkylation and could reduce separation and circulation burdens. Neither a process saving nor a new catalyst performance is established here.

The connection to Gounder is direct: Purdue describes his work on solid-acid hydrocarbon alkylation as part of research on safer alternatives to liquid HF. His group also develops synthesis–structure–reactivity relationships for acid-site location in zeolite voids. [Purdue project description](https://engineering.purdue.edu/P2SAC/research/P2SAC_Funded_PhD_Research_Project); [Gounder faculty profile](https://engineering.purdue.edu/ChE/people/ptProfile?resource_id=85277).

The proposed hypothesis was: **at comparable accessible acid-site density and effective transport, changing the local environment can increase productive hydride transfer relative to further olefin addition enough to retain useful alkylate output at lower isobutane circulation.** Alternatives are higher effective acid density, reduced diffusion gradients, preferential adsorption that changes both useful and harmful rates, or slower pore blocking without an intrinsic selectivity change.

This is a more consequential target than a longer time before butene breakthrough at extreme dilution. It is also substantially harder than selecting the material with the highest initial C8 fraction.

## Primary evidence that narrowed the opportunity

### 1. The proposed confinement principle is already explicit

Liu et al. model isobutane–propene alkylation on FAU and La-FAU. Their preferred hydride-transfer route involves a carbenium ion, isobutane and another olefin; a competing route produces isobutene through proton transfer to the framework. They explicitly discuss the competing need for a large reaction cavity and strong isobutane confinement and propose a bimodal channel structure. Their calculated chemistry also connects carbenium deprotonation to loss of the productive cycle. These are theoretical results, not proof that the same dominant path applies to every working butene catalyst. Relevant mechanism, model and discussion sections were read in the open full text. [Liu et al., ACS Catalysis 2017, DOI 10.1021/acscatal.7b02877](https://repository.tudelft.nl/file/File_a3e5b797-6e1b-4c29-b9c0-72587f5dc4d8).

**Consequence:** neither “provide a larger hydride-transfer cavity” nor “combine that cavity with an alkane-enriching environment” is an original program. An experimental test could still be valuable if it establishes a usable design rule beyond these predictions.

### 2. Al-location control of the local reactant ratio is also direct prior art

Li et al. calculate adsorption and diffusion of isobutane and 1-butene in H-BEA with different framework Al locations. Their abstract identifies T5 and T7 environments as favorable for the intracrystalline isobutane/olefin ratio. The full article remains unread here; no actual synthesis, catalytic selectivity or lifetime improvement is inferred from its abstract. [Fuel 2025, DOI 10.1016/j.fuel.2025.135562](https://doi.org/10.1016/j.fuel.2025.135562).

**Consequence:** transferring Gounder's site-placement expertise into this particular adsorption question would not itself establish novelty. The missing contribution would need to connect a measured working-state branching change to an achievable placement intervention and a resource-relevant operating benefit.

### 3. There is a stronger experimental benchmark than an arbitrary conventional zeolite

Van Minnebruggen et al. report OSDA-free Beta with cumulative productivity above 30 g product/g catalyst, C8 selectivity above 85%, and three regenerations without activity loss, preferably using hydrogen. Their paper compares with La-HY and conventional Beta. At the initial screen, only the publisher abstract, introduction and exposed conclusion had been inspected. The original-PDF check below now resolves the feed and formulation basis. Complete-cycle comparison still requires consistent product, time, inventory and regeneration accounting. [J. Catal. 2022, DOI 10.1016/j.jcat.2022.01.007](https://doi.org/10.1016/j.jcat.2022.01.007).

**Consequence:** more Al, OSDA-free preparation, better lifetime than a weak Beta, and hydrogen regeneration are already demonstrated directions. The former methods-access gap is resolved by the source check below; the Pt-containing formulation must be included in the comparator definition.

### Updated operating basis of the 2022 Beta comparator

The now-retained [original Van Minnebruggen paper](../../literature/papers/minnebruggen2022-alkylation-of-isobutane-with-butenes/original.pdf), PDF pp.4–5, resolves the main operating basis. Table 3 uses 0.3 g catalyst, an initial 62.8 mL isobutane charge, 0.72 g/h mixed feed and 85 °C. At feed paraffin/olefin molar ratio 14.5, OF-BEA-2 gives 28.9 g product/g catalyst before deactivation at 79 h; the 0.4 wt% Pt version gives 30.5 g/g at 83 h. Increasing feed P/O to 17.3 and 20.4 gives 97 and 101 h but 29.5 and 26.2 g/g, respectively. Thus longer operation does not mean more product per catalyst, and the >30 g/g result must not be assigned indiscriminately to unmodified Beta.

These are cumulative product yields at the specified continuously fed reactor conditions, not accepted C8 productivity including regeneration, internal-circulation energy or initial isobutane inventory. The paper separately compares oxidative and hydrogenative regeneration; hydrogen regeneration uses the Pt-containing formulation. The full text strengthens the existing comparator and removes a methods-access gate. It does not supply the proposed low-circulation material advantage.

### 4. Long operating time can conceal large dilution and low olefin throughput

Chen et al. report a HY experiment lasting 72 h. Its methods specify an inlet isobutane/butene molar ratio of 180, 2.0 MPa and WHSV 7.5 h−1. Air regeneration at 450 °C for 12 h restores initial conversion but subsequent lifetime and product distribution worsen. Their selectivity is defined among C5+ effluent products; it is not a complete carbon efficiency. Methods and relevant performance/regeneration sections were read in the open article. [RSC Advances 2018, DOI 10.1039/C7RA12629H](https://doi.org/10.1039/C7RA12629H).

An illustrative normalization makes the comparison issue concrete. **If** 7.5 h−1 uses total feed mass, an I/O ratio of 180 corresponds to only

`7.5 × 56.11 / (180 × 58.12 + 56.11) = 0.0400 g butene gcat−1 h−1`.

Over 72 h, ideal complete cross-alkylation of that butene would make about 5.86 g C8/g catalyst. This is a conditional stoichiometric calculation, not a reconstructed observed yield or a confirmed WHSV definition. It cannot be ranked directly against the 2022 cumulative productivity. It shows why hours and nominal WHSV require their denominators.

### 5. Local dilution, staged feed, regeneration and catalyst–reactor co-design are established

In a developer-authored 2006 pilot report, Mukherjee et al. distinguish fresh-feed I/O of 10–15 from a reactor ratio around 400 achieved with recycle. They describe structured pores, acid-site distribution, staged feed and hydrogen regeneration. Reported pilot cycles use 8–12 h alkylation followed by 2 h regeneration; plotted time excludes regeneration. This is primary developer evidence, not independent modern commercial validation. The report's reactor, operating and pilot sections were read directly. [Oil & Gas Journal, July 10, 2006](https://www.ogj.com/refining-processing/refining/article/17224985/scale-up-strategy-applied-to-solid-acid-alkylation-process).

An earlier ABB/Akzo Nobel developer report likewise describes staged olefin injection, isobutane washing and hundreds of operating cycles; its two-year catalyst life is a projection. [ABB Review 2/2000, pp. 71–76](https://library.e.abb.com/public/436e0e59f93e253bc1256ef500466fd0/71-76%20-%20M610.pdf).

**Consequence:** better feed distribution, a recovery cycle, or a generic reaction–diffusion model is not a new contribution. A lower reported external feed ratio can coexist with considerable internal recycle.

## What a consequential new result would have to establish

The unresolved question worth retaining is whether a material change improves **intrinsic competition at the functioning organic/zeolite ensemble**, rather than merely reproducing a more favorable local composition. A simple two-rate caricature is useful for defining the burden of proof, but not for fitting the real network:

`rHT = kHT aI NC`, `radd = kadd aO NC`.

Here `NC` is a shared reactive carbenium inventory and `aI`, `aO` are local isobutane and olefin activities. Then the branch ratio is `(kHT/kadd)(aI/aO)`. Doubling the local ratio has the same branch effect as doubling the intrinsic rate-constant ratio in this deliberately restricted model. A feed-level selectivity improvement cannot distinguish them. Moreover, the olefin-assisted route in Liu's model would put olefin activity in productive hydride transfer too; this simple ratio could then be wrong. The local inventory and the parallel initiation/deprotonation/cracking routes also change during operation.

This is why neither inert adsorption selectivity nor an apparent olefin reaction order alone identifies the intended intervention. The working pore contains reactive organics and may differ substantially from an empty zeolite. An inert-probe hydride-transfer ranking is informative only after it predicts actual alkylation behavior.

### A bounded reopening test, not a recommended new campaign

Reopen only if an already available pair has a defensible difference in acid-site environment with sufficiently comparable accessible acidity and transport, and the available 2022 benchmark methods have been incorporated into a reproducible comparison. Do not start a synthesis library to manufacture this contrast.

1. Reproduce useful alkylation on the stronger reference. Use a liquid-phase reactor with measured mixing and heat removal, a defined feed composition and accurate low-level heavy-product analysis. Confirm catalyst and reactor capability before committing.
2. Compare cumulative useful alkylate mass and product quality over complete reaction/regeneration cycles at matched olefin throughput per initial catalyst mass. Include catalyst inventory, regeneration time, hydrogen, washes and retained carbon.
3. Vary isobutane circulation independently from olefin throughput where the reactor allows it. Distinguish fresh-feed I/O, internal reactor recycle and the estimated local ratio. Compare each material with the reference operated with the same dosing/recycle freedom.
4. If the pair changes the useful selectivity–throughput relation, identify the smallest kinetic or isotope comparison that separates altered branching from changed local concentration. A carbon/hydrogen tracer is conditional, since isotope exchange, alkene isomerization and retained organics can make a label response nonunique.
5. Before expansion, predict one untested lower-circulation operating condition and its cumulative useful output. The prediction must survive independent material preparation or regeneration replication appropriate to the intervention.

A useful result would preserve product quality and integrated output while reducing a measured circulation or regeneration burden, with a supported explanation that predicts where the advantage fails. A small endpoint selectivity change at lower output is insufficient. A decrease in pump flow is not automatically an energy saving: pressure drop, separation, heat duty, conversion and equipment size must be included in a later process comparison.

Stop if the response is explained by ordinary dilution/transport or changed acid density, if the stronger reference removes the advantage, or if local branching cannot be constrained without a large speculative measurement program. Even a clear negative mechanistic result would need a consequential design decision to justify a substantial program.

## Confidence and portfolio decision

| Question | Assessment |
|---|---|
| Importance of the bottleneck | High. Solid-acid productivity, regeneration and recycle all affect practical viability. |
| Does the proposed placement hypothesis have scientific support? | Plausible, but its generic chemical rationale is already published. No distinct favorable working-state intervention was identified. |
| Can a rate/product comparison be informative? | Moderate with an existing capable liquid-phase setup and suitable pair; lower for uniquely separating local adsorption, active organic inventory and elementary hydride transfer. |
| Is a substantial practical improvement likely on current evidence? | Low evidentiary confidence. Strong prior materials and integrated reactor practices raise the benchmark. |
| Should it displace Ag? | No. It presently needs a new material contrast and a new discriminating premise before it becomes a focused experimental program. |

The source checks are not exhaustive. In particular, the 2022 and 2025 full texts could identify a better narrowly testable opening. The conclusion is to reject the current **generic acid-site-placement/lower-recycle proposal**, not to reject solid-acid alkylation as a field.

## Exact literature handoff to the sole literature agent

Use `$lit`, **Add identified literature**, sequentially. Skill: `/home/sgusev/repo/skills/literature/SKILL.md`; project: `/home/sgusev/repo/catalisys-notes`; knowledge base: `/home/sgusev/repo/catalisys-notes/literature`. No KB edits or maintenance were performed by this reviewer. Include metadata and relevance for inaccessible sources, preserve their unread status, and report unresolved full texts. Do not equate an inspected abstract with a read full paper.

Core sources:

1. **10.1021/acscatal.7b02877**, Liu et al., *Hydride Transfer versus Deprotonation Kinetics in the Isobutane–Propene Alkylation Reaction: A Computational Study* (2017). Direct mechanism and confinement-design prior art. Open full text inspected in relevant sections; saved PDF `/tmp/stronger-practical-read/liu2017.pdf`; source https://repository.tudelft.nl/file/File_a3e5b797-6e1b-4c29-b9c0-72587f5dc4d8 . Retrieve SI if accessible, but SI was not read here.
2. **10.1016/j.fuel.2025.135562**, Li et al., *Unveiling the role of Al location in H-BEA zeolite on the adsorption and diffusion of iso-butane and 1-Butene in C4 alkylation*. Direct nearest site-placement prior art. Publisher abstract read; full text unread/unretrieved here.
3. **10.1016/j.jcat.2022.01.007**, Van Minnebruggen et al., *Alkylation of isobutane with butenes using OSDA-free zeolite beta*. Essential experimental comparator and regeneration benchmark. Publisher abstract/introduction/exposed conclusion inspected; full text unread/unretrieved here. https://www.sciencedirect.com/science/article/abs/pii/S0021951722000070 . Complete feed/OSV/productivity definitions are necessary before quantitative comparison.
4. **10.1039/C7RA12629H**, Chen et al., *Mechanism of byproducts formation in the isobutane/butene alkylation on HY zeolites*. Primary lifetime and product-accounting example; relevant methods/results read. Open full PDF https://pdfs.semanticscholar.org/5449/da22be7cb73e26f21c37f7f1b67815c0a7ed.pdf ; publisher https://pubs.rsc.org/en/content/articlepdf/2018/ra/c7ra12629h . Inspect original WHSV definition before labeling it total-feed based; this report's normalization is conditional.
5. **10.1039/D1RA03892C**, Sun et al., *Preparation of CuHY catalyst via solid-state ion exchange method and its catalytic performance in isobutane/2-butene alkylation*. Relevant adsorption/acid-modification competing intervention; exposed publisher sections only, not full paper read. PMC9034412; PMID35480456; open PDF https://pdfs.semanticscholar.org/f3c4/d9c48f400356c807c85afcd652e64081cf68.pdf . Direct publisher and PMC access failed in this review; lawful alternatives remain.
6. **10.1021/ie960172y**, Simpson, Wei and Sundaresan, *Kinetic Analysis of Isobutane/Butene Alkylation over Ultrastable H–Y Zeolite* (1996). Explicit reaction–diffusion and pulsed-flow prior art. Publisher abstract read; full text unread here.
7. Mukherjee et al., *Scale-up strategy applied to solid-acid alkylation process*, **Oil & Gas Journal, July 10, 2006**. Primary developer pilot benchmark distinguishing feed and reactor I/O and excluding regeneration from plotted time. Relevant full webpage sections read: https://www.ogj.com/refining-processing/refining/article/17224985/scale-up-strategy-applied-to-solid-acid-alkylation-process . Preserve developer affiliation and evidence limits.
8. *New solid acid alkylation process for motor gasoline*, **ABB Review 2/2000, pp. 71–76**. Primary developer staged-feed/recovery prior art, with lifetime projections distinct from observations. Relevant process sections read; PDF `/tmp/stronger-practical-read/abb2000.pdf`; https://library.e.abb.com/public/436e0e59f93e253bc1256ef500466fd0/71-76%20-%20M610.pdf . Verify exact authors/title in the PDF.
9. **10.1016/j.apcata.2004.12.005**, Platon and Thomson, *Solid acid characteristics and isobutane/butene alkylation*. Prior experimental link between hydride-transfer activity, competitive adsorption and alkylation; publisher abstract read, full text unread here.
10. **10.1016/S0021-9517(03)00251-3**, *Deactivation pathways in zeolite-catalyzed isobutane/butene alkylation*. Direct chemical-deposit and hydride-transfer prior art; publisher abstract/introduction inspected, full text unread here.
11. **10.1016/S0009-2509(02)00246-4**, *Deactivation behavior of the catalyst in solid acid catalyzed alkylation: effect of pore mouth plugging*. Needed transport/deactivation prior art; publisher abstract only, full text unread here.
12. **10.1016/j.fuel.2024.130938**, *Rare earth cation-modified X zeolites for isobutane alkylation: The influence of ionic radius*. Competing recent acidity/site-environment intervention; publisher abstract only, full text unread here.

Clearly relevant sources identified during the initial cross-topic search, not used to support this candidate's conclusion:

13. **10.1039/D5SC01637A**, *Mechanistic insights into spontaneous redispersion of ZnO onto TiO2 in water-containing environments*. Open primary text https://pubs.rsc.org/en/content/articlehtml/2025/sc/d5sc01637a . Exposed catalytic test section reports water-induced redispersion but rapid deactivation and improved stability after oxidation. Relevant to retained oxide/water/regeneration programs; body not fully read here.
14. **10.1007/s12209-025-00455-z**, *Inhibitory Effect of Water on Propane Dehydrogenation over Metal Oxides via Dissociative Adsorption*. Open primary source https://link.springer.com/article/10.1007/s12209-025-00455-z ; abstract only read. Direct boundary for oxide dehydrogenation/water ideas.
15. **10.1002/aic.18930**, *A tandem electro-thermocatalysis platform for practical hydrogen peroxide-mediated oxygenation reactions at high rates*. Relevant integrated peroxide/zeolite prior art; publisher abstract only read: https://aiche.onlinelibrary.wiley.com/doi/abs/10.1002/aic.18930 . No system-performance comparison claimed here.
16. **10.1021/acscatal.1c03174**, *Elucidating the Significance of Copper and Nitrate Speciation in Cu-SSZ-13 for N2O Formation during NH3-SCR*. Direct mechanistic prior art for retained emissions screens; exposed sections only read. Open author/repository PDF https://eprints.whiterose.ac.uk/id/eprint/217177/1/negahdar-et-al-2021-elucidating-the-significance-of-copper-and-nitrate-speciation-in-cu-ssz-13-for-n2o-formation-during.pdf .
17. *Towards rational design of Cu-SSZ-13 catalysts with less N2O formation in NH3-SCR reaction: The effect of Brønsted acid sites*. DOI not verified here; discovery identifier **OpenAlex W4405093180**, https://openalex.org/W4405093180 . Abstract claims more BAS suppress N2O in its studied materials; relevant conflicting direction to qualify, not a fact to adopt from a search abstract. Verify primary metadata/full text sequentially with the skill; mark unread if inaccessible.
18. *CeO2/Cu-SSZ-13 composite NH3-SCR catalysts for breaking the trade-off between low-temperature activity and N2O formation*. Publisher PII **S092633732501344X**, https://www.sciencedirect.com/science/article/pii/S092633732501344X . Abstract proposes nitrate migration/spatial separation; relevant close precedent for any acid/nitrate separation program. DOI and full text unresolved here; do not infer operating robustness from the abstract.

The literature agent's eventual retrieval/read reports and unresolved-source list remain authoritative. These handoffs are requests, not completed ingestion claims.
