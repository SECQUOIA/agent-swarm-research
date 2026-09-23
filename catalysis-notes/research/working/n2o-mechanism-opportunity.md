# N2O mechanism challenge: what can a working-state isotope experiment decide?

**Source and decision update, 2026-09-16:** This is a historical screen of an existing idea, not an active campaign. The [decision brief](../decision-brief.md) controls current priorities. Access statements and source-request lists below describe the original review unless explicitly updated; current access is recorded in the [literature status](../literature-status.md). Availability of a full text does not mean that every claim or benchmark in it has been rechecked. No new idea or experimental campaign is started by this update.

The [Ruggeri ammonium-nitrate method](../../literature/papers/ruggeri2018-novel-method-of-ammonium-nitrate/paper.md), [Chen isotope study](../../literature/papers/chen2015-a-comparative-study-of-n2o/paper.md) and [Jabłońska transient study](../../literature/papers/jabonska2024-unraveling-the-nh3-scr-denox/paper.md) are retained and marked read. Historical acquisition requests below are not current gaps. No uniquely identifying isotope observation follows from access alone: the alternative atom maps and stored-nitrogen inventory controls remain necessary.

Date: 2026-09-15. **Decision: do not promote this into a full research program above the bounded [Ag retention investigation](../programs/ag-selective-oxygen-use.md).** The nitrate question is important, but the papers do not define two mutually exclusive mechanisms with an experimentally accessible unique isotope signature. A useful, narrower experiment can bound nitrogen residence times. Without a species-specific flux constraint, it cannot decide whether to change Brønsted acid sites (BAS) or Cu ensembles. No experiment has been performed here.

## 1. What the primary evidence actually disagrees about

- **Wang/Gao 2025** argues for several nitrate/ammonium-nitrate-related N2O routes, with Cu enabling nitrate formation and BAS affecting its decomposition. Its native SCR kinetics, prepared-inventory TPD and calculations support a serious competing interpretation. They do not measure the fraction of stationary N2O flux through each nitrate population. The paper itself allows Cu-bound nitrate-like species as well as ammonium nitrate. Local manuscript pp.24–34 were examined. [Primary source](https://doi.org/10.1016/j.apcatb.2025.125540); [local full text](../../literature/papers/gao2025-mechanistic-insights-into-n2o-formation/fulltext.md).
- **Usberti/Collier 2026 is not an exclusive nitrate-free model.** Its §3.1 explicitly states that the fitted third-order dependence on oxidized Cu does not exclude NO2/NH4NO3 intermediates, and gives a nitrate sequence consistent with its global Cu-reduction stoichiometry. A fit to this model cannot by itself settle the nitrate question or identify three Cu atoms in a transition state. §§3.1–3.5 and conclusions were examined. [Primary source](https://doi.org/10.1016/j.cej.2026.172622); [local full text](../../literature/papers/collier2026-standard-nh3-scr-and-n2o/fulltext.md).
- **Negahdar 2021** associates higher N2O formation with different Cu coordination and proposes nitrate-related chemistry on a Cu-aluminate-like environment. The exact Cu structure remains an interpretation, and its own embedded versus unembedded calculations change the candidate assignment of an IR feature. Thus even the proposed nitrate routes need not share one material-design remedy. Selected methods, §§3.4–3.7 and conclusions were read in the [open full text](https://eprints.whiterose.ac.uk/id/eprint/217177/1/negahdar-et-al-2021-elucidating-the-significance-of-copper-and-nitrate-speciation-in-cu-ssz-13-for-n2o-formation-during.pdf).

**Consequence:** the useful scientific target is a quantitative branching fraction under a specified working state. “Nitrate versus Cu” is an unsuitable binary target because Cu can both form a nitrate precursor and participate in its subsequent reaction. A nitrate contribution also does not, by itself, establish BAS control.

Two reasoning cautions matter when comparing these sources. Apparent activation energies include coverages, equilibria and changing populations; equal apparent barriers do not prove a common intermediate. Conversely, a smaller apparent barrier for a low-yield product does not exclude a common intermediate: different prefactors, entropies and branching probabilities can keep its rate small. Neither comparison alone adjudicates the mechanism.

## 2. Why the tempting isotope signatures are nonunique

This section is atom-balance reasoning, not an additional experimental finding.

### Nitrogen origin and position

For the simple nitrate route,

`15NH4+ + 14NO3− → 15N–14N–O + 2 H2O`.

An NH3-derived nitrogen attacking a NO-derived nitrogen in a Cu-associated `15NH2–14NO` intermediate can produce the **same** `15N–14N–O`. Both routes can preserve the NO-derived N next to oxygen. Therefore neither mixed-N N2O nor that positional isotopomer is uniquely diagnostic. A different positional ratio could constrain a particular fully specified elementary sequence, but cannot establish “nitrate present/absent” without atom maps and competing scrambling paths.

For two independently sampled N pools with label fractions `a` and `b`, the mass-isotopologue probabilities are

`P0 = (1−a)(1−b)`, `P1 = a(1−b) + (1−a)b`, `P2 = ab`.

Either chemical family can generate these probabilities. Opposed switches of 15NH3 and 15NO probe timing and pairing, but the same measured covariance can arise from retained NH4+, coordinated NH3, Cu–NOx or an already paired N–N intermediate. Stored NH3 also means an NH3-label delay is not evidence for stored nitrate.

### Oxygen origin

Nitrate contains more oxygen than H2NNO, but N2O retains only one O. A claim that nitrate must give a statistical one-third retention of labeled NO oxygen assumes equivalent nitrate oxygens and a specified exchange and elimination sequence. Those assumptions are not established under wet working SCR. Water, Cu-bound oxygen and NOx interconversion create additional exchange opportunities; a direct route need not retain the original NO oxygen either. Adding 18O2 or H2-18O therefore increases information only after a genuinely different, quantitatively bounded atom map has been established. It is not an automatic discriminator.

### A nitrate inventory is not a nitrate flux

For an unresolved population `i`, a local first-order representation gives `r_i = k_i N_i`. An upper inventory limit `N_i ≤ U_i` bounds its rate only if a defensible **working-state** upper bound on `k_i` is known. A rapidly turning-over, IR-invisible population can carry the entire small N2O flux. Large visible nitrate can conversely be mostly spectator. Impregnated-salt TPD or a nitrate-preload reaction establishes accessible chemistry, but does not supply a universal upper bound on `k_i` under simultaneous wet NO/NH3/O2.

## 3. One sharp contrast worth retaining, with its narrow meaning

**Candidate hypothesis:** a specified dominant fraction of N2O-forming NO-derived nitrogen spends longer than a practically relevant time `τ*` inside the working catalyst. Its rival is predominantly prompt nitrogen conversion. Choose `τ*` from the exhaust event or material-retention claim that would change a decision, before measuring the transient. This tests a residence-time claim; it does not test all nitrate chemistry.

At one stationary standard-SCR state, equilibrate with 15NO and ordinary NH3, then switch to otherwise identical 14NO. Hold NO, NH3, water, O2, temperature and flow constant. Use a thin, demonstrably transport-resolved specimen and measure an inert-tracer step. Monitor the total product rate and the labeled N-atom flux in N2O, rather than interpreting a single nominal mass peak. N2O, NO2 and their fragments overlap in ordinary mass spectrometry; validated separation or isotope-resolved spectroscopy is required. Measure the actual feed-label response and background.

Let `J_old(t)` be the excess 15N-atom flux in N2O after the switch and `J_old(0)` its stationary pre-switch value, corrected for enrichment and background. Following appropriate gas-residence correction, define

`y_old(t) = J_old(t) / J_old(0)`.

Under a stationary, effectively isotope-neutral tracer experiment, this is the survival function of the transit-time distribution for the NO-derived N atoms that reach N2O. The fraction with age exceeding `τ*` is

`f_slow(τ*) = y_old(τ*)`.

A one-sided uncertainty bound below a preregistered dominant fraction falsifies that **slow-nitrogen** explanation at this operating state. It remains valid as an atom-residence statement even if an atom changes chemical species along the way. Isotope effects, incomplete initial labeling, changing total activity or an unresolved gas-response correction invalidate the simple interpretation and must be checked. Do not infer a single exponential or force a many-reservoir fit when the measured step already supplies the relevant bound.

The corresponding area,

`I_to_N2O = integral J_old(t) dt`,

counts old labeled N atoms subsequently exported in N2O. It is not the complete nitrate inventory: old nitrogen can also leave in N2, NOx or NH3, and intermediate readsorption can redirect its fate. Closing the nitrogen balance through the complete release period provides a useful inventory check. A stopped feed, oxidizing purge or temperature ramp changes the branching probabilities and cannot be substituted for the unchanged working-state switch.

**Falsifiable outcomes:**

| Result | Justified conclusion | Conclusion not established |
|---|---|---|
| Small upper bound on `f_slow(τ*)` | A dominant long-lived NO-derived source of N2O is excluded at that state | All nitrate routes are excluded; BAS modification is unnecessary |
| Substantial resolved tail | Stored NO-derived nitrogen feeds N2O during normal operation | The store is NH4NO3, or is bound to BAS rather than Cu |
| Tail varies across existing catalysts at matched useful NOx removal | Nitrogen retention is a candidate explanation for different time-dependent N2O outputs | Retention causes the selectivity difference, or suppressing it will improve the complete cycle |

This is feasible in principle with established isotope methods, but the available sources and workspace do not establish access to sufficiently sensitive, time-resolved N2O isotopologue analysis. The trace product signal and instrument response may be the limiting factors. There is no reason to begin a new instrument campaign solely for this contrast before it changes a concrete design decision.

## 4. Why even this contrast does not currently justify a new program

Important prior art already covers the adjacent measurements:

- Chen et al. used nitrate formation followed by isotope-labeled reaction steps to examine NH4NO3 formation and compared Cu zeolite frameworks. Its institutional abstract establishes relevant prior art, but the complete paper has **not** been read in this audit. [J. Catal. 2015](https://doi.org/10.1016/j.jcat.2015.06.016).
- Ruggeri et al. quantified deposited ammonium nitrate through `NO + NH4NO3 → NO2 + N2 + 2H2O`, including powder and monolith validation. The exposed publisher abstract and introduction were read, not the complete article. NO titration of a native inventory is therefore an adaptation of an existing method. It also changes the working feed and can compete with other stored-N and Cu-redox chemistry. [Catal. Today 2018](https://doi.org/10.1016/j.cattod.2017.04.016).
- Jabłońska et al. already combine Cu-SSZ-13 stop-flow experiments and SSITKA, including NH3 and N2 residence information and mixed-N product interpretation. The open main paper's pp.10–12 were examined. Its NH3/N2 measurements do not settle the present N2O question, but “apply SSITKA to Cu-CHA” is not a new program. [ChemSusChem 2024](https://doi.org/10.1002/cssc.202400198); [open full text](https://d-nb.info/1353585050/34).

The sharp contrast above could reject a particular long-lived storage explanation. However, the papers permit a fast nitrate route and a retained Cu-associated NOx route. Either can reproduce the opposite observation. Their material-design consequences remain different. An acidity perturbation is also not automatically selective: it can change NH3 storage, Cu coordination/mobility, and nitrate formation together. Matching total Cu and the average Cu oxidation state does not match those kinetic populations.

**Reopening requirement:** obtain an independently defensible species-specific working-state constraint that closes this nonuniqueness. For example, a complete measured bound `sum(k_i,max U_i) < r_N2O` could exclude the specified nitrate family, but only if it covers every relevant nitrate population and the rate bounds remain valid in the SCR state. Alternatively, a demonstrably selective intervention that changes nitrate turnover without changing the competing Cu kinetics could establish a consequential causal branch. Neither capability was identified in this bounded search. This is a scientific limitation, not a request to add a larger speculative measurement package.

## 5. Practical value and portfolio decision

If a substantial, independently assigned BAS-associated nitrate branch were found at useful NOx conversion, a material choice that decreases its unselective turnover while retaining SCR activity would become rational. If most N2O instead branches before that inventory forms, suppressing nitrate storage might do little. In either case, steady N2O alone is insufficient: the same specimen must be compared over cool-down and rewarming with complete N2O, NOx and NH3 accounting. Stabilizing a store can defer emissions. These distinctions are consequential but do not establish a beneficial material intervention now.

| Assessment | Judgment |
|---|---|
| Scientific importance | High: a misleading pathway assignment can direct synthesis toward the wrong property. |
| Confidence in a universal nitrate-free or universal nitrate-only hypothesis | Low; the examined evidence supports competing, condition-dependent possibilities. |
| Confidence in the narrow isotope residence-time experiment being informative | Moderate, conditional on adequate analysis and an actual slow-storage claim to test. |
| Confidence that this experiment uniquely apportions BAS-nitrate versus Cu-centered flux | Low. Atom mapping and unresolved populations leave nonuniqueness. |
| Confidence in practical improvement from the present proposal | Low; a selective material intervention has not been identified. |

The [current Ag investigation](../programs/ag-selective-oxygen-use.md) is also bounded and constrained by old composition/durability prior art. It nevertheless starts from a reported useful retention difference and asks whether distinguishing recovery, persistent change and product loss changes an operating or formulation decision. The present N2O proposal starts from an important interpretive dispute but does not yet connect its identifiable measurement to an equally concrete useful choice. **Retain the N2O identifiability result and source leads; do not displace Ag or launch a synthesis library on this basis.**

## 6. Exact literature handoff and reading record

No knowledge-base files were edited. The following were sent together to the existing sole `/root/literature` agent for sequential `$lit` “Add identified literature,” including metadata-only records if lawful full text remains unavailable.

- Skill: `/home/sgusev/repo/skills/literature/SKILL.md`.
- Project: `/home/sgusev/repo/catalisys-notes`.
- Knowledge base: `/home/sgusev/repo/catalisys-notes/literature`.

1. **10.1021/acscatal.1c03174**, Negahdar et al. Already queued by the stronger-practical-program audit; additional available full text supplied: `/tmp/negahdar2021.pdf`, extracted `/tmp/negahdar2021.txt`, lawful White Rose URL above. Reason: competing Cu/nitrate assignment, with explicit structural and vibrational limits.
2. **10.1016/j.cattod.2017.04.016**, Ruggeri et al., *Novel method of ammonium nitrate quantification in SCR catalysts*, Catal. Today 307 (2018), 48–54. Reason: essential inventory-measurement prior art. Publisher abstract/introduction read at https://www.sciencedirect.com/science/article/pii/S0920586117302468 ; institutional record https://re.public.polimi.it/handle/11311/1037471 lists a restricted AAM. Full text not retrieved here; preserve the unresolved request if retrieval fails.
3. **10.1016/j.jcat.2015.06.016**, Chen et al., *A comparative study of N2O formation during the selective catalytic reduction of NOx with NH3 on zeolite supported Cu catalysts*. Reason: nitrate-preload isotope prior art essential to novelty and mechanism interpretation. Institutional abstract read at https://impact.ornl.gov/en/publications/a-comparative-study-of-nsub2subo-formation-during-the-selective-c/ . Full text not retrieved/read here.
4. **10.1002/cssc.202400198**, Jabłońska et al., *Unraveling the NH3-SCR-DeNOx Mechanism of Cu-SSZ-13 Variants by Spectroscopic and Transient Techniques*, ChemSusChem 17 (2024), e202400198. Reason: Cu-SSZ-13 SSITKA, stored nitrogen and product-origin prior art. Available lawful OA PDF `/tmp/jablonska2024.pdf`, extracted text `/tmp/jablonska2024.txt`, https://d-nb.info/1353585050/34 . Selected main-paper pp.10–12 read; its supporting information was not retrieved in this audit.

The local Wang/Gao 2025 and Usberti/Collier 2026 main papers were used directly; they need no duplicate ingestion. Broader statements about absence of all prior art or universal working mechanisms are not made.
