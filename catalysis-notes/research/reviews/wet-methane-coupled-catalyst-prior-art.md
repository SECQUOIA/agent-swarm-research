# Coupled oxidation catalysts and regeneration are established comparators

2026-09-15. Root source check for the [low-NO methane study](../working/wet-methane-value-screen.md). No experiments performed.

## Recovered evidence

The open [Nevalainen 2021 dissertation](https://erepo.uef.fi/bitstream/123456789/26561/1/urn_isbn_978-952-61-4430-6.pdf), *Environmental Catalysts Study – Emission Abatement in Heavy-Duty Transportation and Stationary Applications*, includes the complete [Auvinen et al. Fuel article, DOI 10.1016/j.fuel.2021.120223](https://doi.org/10.1016/j.fuel.2021.120223) as Publication IV. Root read its methods and selected results/discussion. The original thesis and extracted text are retained in `/tmp/wet-methane-screen/uef-thesis.pdf` and `.txt` and were supplied to the sole literature worker.

The article compares commercial methane, diesel-oxidation and three-way catalysts, including paired arrangements. Its simulated exhaust contains methane, propane, CO, NO, water and SO2. Nine hours of poisoning includes three light-off ramps. Four 200 s rich regeneration protocols at 450 °C vary oxygen supply, followed by 30 min operating comparisons. The paired catalysts improve reported conversion retention, but have additional material and reactor volume. Upstream sulfur capture, altered NO/NO2 and reaction heat remain contributing explanations. Regeneration changes NH3, N2O and CO output as well as methane performance. These are finite protocol results, not demonstrated service life. [Fuel methods §§2.1–2.2 and results §§3.2–3.3](https://doi.org/10.1016/j.fuel.2021.120223).

Thus, placing another catalyst upstream to protect methane oxidation or alter NOx chemistry is prior art. The recovered article does not close the specific Ryu low-NO question.

## Comparison rule that survives the source check

The Fuel paper plots sums of individual catalyst conversions for illustration and explicitly acknowledges that these sums have no physical meaning. They must not be reused as a quantitative synergy baseline. Even in an idealized independent two-bed sequence with unchanged fractional conversion in each bed, the combined conversion would be

`X_series = 1 − (1 − X_A)(1 − X_B)`.

This formula is itself conditional: real beds change composition, temperature and catalyst history. The defensible comparator measures or predicts the second bed under its actual inlet conditions. Additional metal, residence time, heat release and sulfur storage must enter a useful system comparison. A higher conversion than either single bed establishes neither intrinsic synergy nor superior material efficiency.

The low-NO study therefore needs two distinct controls already identified by the independent review: an omission-treatment pair for the preparation effect, and a credible practical catalyst for useful methane-slip performance. A later coupled-system comparison must include total solids, precious metal, volume, full-cycle slip and regeneration emissions. No new combined-bed campaign follows merely from this source.

## Version and reading limits

Updated after uploads, 2026-09-16. Consult the [current literature status](../literature-status.md) for retrieval status; original temporary paths and handoff statements above are historical provenance.

The thesis also summarizes work titled *Modern methane oxidation catalyst for dual-fuel engine: The effect of TWC space velocity and MOC metal loading on durability and NO2 formation* in Chapter 3.2, printed pp.55–65. Publication III is marked “submitted for publication,” and its appendix contains only a cover page. The thesis summary is available; the complete separate manuscript and any later journal version remain unverified. Do not label them recovered.

The thesis cites the critical NO-promotion article [10.1016/j.cej.2020.128050](https://doi.org/10.1016/j.cej.2020.128050) but does not reproduce it. That historical main-text gap is now closed by the [retained Auvinen CEJ article](../../literature/papers/auvinen2021-effects-of-no-and-no2/original.pdf); the thesis itself still does not reproduce it. The selected reading here is not a full review of the thesis's other soot and three-way-catalyst chapters. Both the new sources and the unresolved version request were sent to the sole literature worker.

## Independent source-boundary check

The independent reviewer checked the retained original thesis's Publication III/IV transition and the reproduced Fuel methods §§2.1–2.2, Tables 1–2 and 5, and results §§3.2.3–3.3. **The interpretation above is supported; no substantive correction is required.** Four details further constrain reuse:

- The paired catalysts have twice the single-catalyst geometric volume at the same 1180 mL min−1 feed. Reported space velocities are 50,000 h−1 for a single catalyst and 25,000 h−1 for a pair. The added upstream component has its own precious metal: TWC and MOC each have nominal 200 g ft−3 loading, whereas DOC has 35 g ft−3. Thus a pair does not hold either total volume or precious-metal inventory constant against a single MOC.
- The nine-hour aging protocol includes three light-off ramps and intervening cooling under O2/N2/H2O. It is not nine uninterrupted hours at one temperature with sulfur present. Each of the four 200 s regeneration strategies is repeated four times; the article presents the third regeneration for each strategy, with 30 min lean sulfur-containing operation between regenerations. This is a repeated sequential protocol, not evidence from independently fresh samples for every strategy or long-term service validation.
- The authors explicitly disavow physical meaning for the summed single-catalyst conversions in Figure 8. The conditional series formula above is correct, but neither it nor arithmetic sums replace a matched measurement of the downstream bed's changed inlet. The paper itself leaves heat and NO/NO2 effects among competing explanations. Its final elemental sulfur results follow Reg 4, five minutes of stabilization and cooling; they are not an untouched working-state sulfur census. The authors also decline absolute cross-catalyst comparison of integrated SO2 desorption because FTIR overlap changes the baseline. Those signals cannot be reused as a closed comparative sulfur balance.
- In the retained PDF, Publication III has its submitted-manuscript cover at PDF page 131; Publication IV's cover follows at page 133 and the complete Fuel paper follows it. The CEJ2021 NO-promotion work appears in the thesis bibliography, not as a reproduced appendix. The thesis recovery does not supply either separate work. The later Auvinen CEJ upload closes that main-text request independently; the complete separate Publication III version remains unverified in this review.

These boundaries preserve the consequential prior-art conclusion: upstream NOx modification and sulfur protection with a second oxidation catalyst are established ideas. They do not establish the mechanism or material efficiency of a new coupled system, and they do not answer the anchored Pd/SSZ-13 low-NO compatibility question.
