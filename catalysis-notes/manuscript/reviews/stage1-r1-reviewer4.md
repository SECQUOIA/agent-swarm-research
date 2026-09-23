# Stage 1, round 1 — reviewer 4

**Verdict: approve the scientific program with minor revisions.** No major scientific defect requires replacing the proposed program. The remaining corrections concern the scope of its predictive and explanatory claims, not the absence of measurements in a proposed experiment.

The chapter establishes a consequential question beyond diagnosing faster water clearance. The late-addition comparison asks whether an inexpensive intervention benefits an already conditioned formulation, and the absolute cumulative-output endpoint prevents fractional retention from concealing an activity penalty. Common handling, independent charges, time-matched shams, and the distinction between formulation function and surviving cobalt sites make the central comparison interpretable. A positive result would exclude an explanation confined entirely to the original conditioning, while leaving restart chemistry, liquid redistribution, rate changes, and local transport as competing explanations. The text generally preserves those limits well.

The thermodynamic argument and both compartment examples are coherent. The two-pool example demonstrates a genuine limitation of aggregate observation without pretending to prove that every conceivable experiment is nonidentifying. The proposed conductance stop rule correctly recognizes reaction-source feedback. A useful formulation result can therefore survive failure of mechanistic identification, as it should.

## Essential corrections — minor

1. **Choose the validation pulse for a consequential functional distinction, not merely a distinguishable water trace.** `manuscript/sections/01-water.tex:99`, with implications for lines 103–105.

   The proposed selection criterion says that surviving models must predict measurably different “responses.” Make explicit that the difference must concern the selected functional endpoint. In the nearby linear regime invoked at line 97, a stable response with impulse kernel `h` gives a full pulse-response integral proportional to `(integral h) × (integral input)`. Models with different time constants but equal steady gains can therefore predict different water traces and the same product deficit integrated through complete recovery. This follows from the proposed response framework; no missing experiment is needed to identify the limitation.

   **Remedy:** preselect either a fixed, operationally meaningful output horizon or a defined recovery-time endpoint, and require the competing predictions to differ consequentially on that endpoint. State what operating choice a successful prediction would inform. Retain the existing independent-charge validation and uncertainty requirement. If only the water curves differ, the transport interpretation may remain interesting, but the promised functional contribution has not been demonstrated.

2. **Extend the source-explanation check to recovery when the conclusion concerns post-recovery retention.** `manuscript/sections/01-water.tex:89`, read with lines 70–87.

   The manuscript's own balance gives generated/supplied water ratios of 0.025 during the high plateau and 0.20 at the recovery baseline. Yet the proposed parent bracketing checks only the residual *plateau* difference before rejecting a whole-bed source explanation. Since the primary endpoint is measured after recovery, formulation-dependent reaction-water production during recovery can influence that endpoint through reversible water sensitivity or continued state evolution. Plateau-only bracketing does not exclude this explanation for the full measured response.

   **Remedy:** either bracket the relevant measured water histories during challenge and recovery, or explicitly restrict the exclusion to a plateau whole-bed source explanation. This does not invalidate the formulation-level protection contrast; it limits the explanatory inference drawn from it.

3. **Narrow the “operating boundary” language to the scope actually tested.** `manuscript/sections/01-water.tex:103`, also line 4.

   Experiment 2 establishes benefit or lack of benefit for one conditioning protocol, one selected disturbance, and one output horizon. Experiment 3 validates one withheld pulse in a nearby reversible range. These can support a useful tested operating case and a bounded prediction, but do not locate a boundary in conditioning age, disturbance duration, water pressure, or cumulative duty. The careful restrictions elsewhere should also govern the headline contribution.

   **Remedy:** describe a tested operating case with explicit validity limits, or identify one boundary variable that would be bracketed after a positive result. A multidimensional optimization campaign is unnecessary.

## Optional enhancement

At `manuscript/sections/01-water.tex:99`, compare the proposed functional prediction with a simple baseline using inlet humidity, the calibrated steady product response, and independently measured apparatus delays. This would show whether water-transient characterization adds predictive value. Accurate empirical prediction remains legitimate even if it does not; the resulting claim should then concern the empirical operating rule rather than the necessity of a water-transport model.

## Evidence checked and overall scope judgment

- Checked the decisive Fang 2026 dose, separate-granule configuration, operating conditions, transient times, and synthesis reduction/passivation against the local original HTML, alongside its extracted text. The manuscript appropriately separates the low-dose longevity bed from powder co-granulate imaging and high-dose controls. [Primary source](https://doi.org/10.1038/s41467-026-76571-8).
- Read the relevant Fang 2022 extracted primary text, including mixing distance, water cofeed, and removal of PDVB from used catalyst. These support the chapter's restrained originality claim; physical mixing and post-use additive manipulation already have precedents. [Primary source](https://doi.org/10.1126/science.abo0356).
- Checked Hanssen's pretreatment/cofeed/dry-return sequence and Wolf's low-conversion external-water sequence in the local primary texts. Wolf's strongest exposure uses water/hydrogen = 5, so the chapter correctly treats its proposed ratio of 0.4 as a feasibility choice rather than an established damage threshold. [Hanssen](https://doi.org/10.1016/S0167-2991(97)80407-7), [Wolf](https://doi.org/10.1016/j.jcat.2019.04.030).
- Ran `manuscript/evidence/check_water_output.py`; it reproduced 116.035 and 219.827 feed-carbon hours, ratio 1.89448, and additive-mass-adjusted ratio 1.80427. The chapter labels these as secondary output proxies with appropriate limitations.
- Reviewed `manuscript/main.tex`, the selected bibliography, and `manuscript/evidence/stage1-water.md`. Online attempts to open the Fang publisher page and the Sengupta PMC page encountered access checks. I did not bypass them or independently verify Sengupta's full original; the evidence note already discloses that limitation.

The stop and expansion rules are proportionate. Failure to reproduce the platform, uncontrolled handling, inadequate challenge dynamic range, or unresolved functional differences legitimately closes the affected branch. Neither a difficult mechanism nor an unmeasured proposed threshold is by itself fatal. With the localized corrections above, the program supports a modest but credible contribution in catalyst operation and formulation, with mechanistic expansion conditional on additional selective evidence.
