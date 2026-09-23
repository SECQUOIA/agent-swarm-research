# Feasibility review: bounding oxygen return with a mixed-isotope feed

Date: 2026-09-15. Scope: measurement and inference for the [oxygen-return calculation](../calculations/epoxidation-oxygen-return.md), using the [balance review](epoxidation-balance-review.md), [value review](epoxidation-value-review.md), and [working opportunity](../working/epoxidation-opportunity.md). No instrument access or performance has been confirmed.

**Later measurement-choice revision:** the [recovered Esposito/Bhan SI review](ag-isotope-reversibility-prior-art.md) establishes quantitative prior art using CO2 labeling and a common-gas isotope balance. That approach already corrects ordinary gas readsorption and should be assessed first for an ethylene adaptation. The mixed-feed design below is retained as a conditional alternative; its separate escape-factor requirement is not a universal requirement for every isotope-return measurement. Pre-mixing recapture, population mismatch and isotope gradients remain distinct limitations.

**Follow-up transport check:** the [escape-bound derivation](../calculations/oxygen-escape-bound.md) shows what a validated reaction–diffusion model could establish. Current evidence does not bound the worst relevant local sink or entry into the modeled gas population. Net reaction rates and integrated inlet recovery do not fill that gap. This remains a conditional experiment, not a demonstrated exclusion method.

**2026-09-16 source update:** Esposito2024 main and Esposito2026 main/SI are now checked in the [updated isotope review](ag-isotope-reversibility-prior-art.md). Ethylene/propylene competition supports related oxidant function on K/NO/Cl–Ag, but ethylene has different rate dependencies and no measured isotope-return bound in these sources. The prior propylene result also permits a reversible O2 precursor upstream of irreversible formation of the exchanging oxidant. These limits strengthen the existing conditional status; no new apparatus campaign follows.

## Decision

**Retain a small, conditional test of return to the bulk gas. Do not promise a bound on every surface recombination event.** A steady mixture of 16O2 and 18O2 removes the brief overlap window of a pure-isotope switch. Its illustrative signal is large enough to justify a calibration trial on existing equipment. The decisive gate is whether the experiment can establish a positive lower bound on the fraction of productive return recorded as mixed-isotope O2, while resolving the return required by the product balance.

The experiment can exclude the return-only version of the restricted cycle if these gates pass. It cannot do so from a missing mass-34 peak alone. In particular, immediate recapture before equilibration with bulk gas can hide a substantial gross recycling flux. If ruling out that possibility requires a new operando suite or an unconstrained multisite model, stop this diagnostic and retain the formulation comparison as a separate question.

## 1. State the measured boundary before collecting data

Distinguish three quantities:

| Quantity | What an outlet experiment can establish |
| --- | --- |
| Productive O2 returned from leftover oxygen into a well-mixed bulk gas | A conditional upper bound, if mixed-pair yield and subsequent survival through the reactor and sampling line have defensible lower bounds. |
| O2 formed locally and immediately readsorbed, including near-surface or pore recapture | No general upper bound from outlet mass 34. A bulk-gas tracer does not reproduce birth at a particular surface site. |
| O2 isotope exchange on sites unrelated to EO formation | Contributes to the observed signal. A positive result cannot assign it to productive leftover oxygen. |

The restricted-cycle rate `D` counts a specified gross return process consistently with its initial O2 activation rate. It is not automatically net O2 generation at the outlet. If oxygen returns and is activated again inside the chosen boundary, both events must be counted. Consequently, a bound on bulk-gas return excludes the full return-only explanation only when that explanation requires the bounded route, or when unobserved local recycling is independently negligible. Do not change boundaries silently to claim exclusion.

Low net O2 conversion does not establish a high escape probability: rapid adsorption/desorption can produce substantial gross exchange with little net consumption. Conversely, poor escape does not make local recycling chemically impossible; it makes this measurement unable to exclude it.

Surface reformation `2O* → O2*` followed by epoxidation without gas release is different again. Its net effect is additional surface oxygen use, represented by `H` in the restricted balance. A bulk-gas return bound does not exclude that route or identify a Re intermediate. See the [balance review's isotope appendix](epoxidation-balance-review.md#appendix-a-stronger-isotope-test-for-productive-oxygen-return).

## 2. Use a one-sided flux bound, not a peak/no-peak decision

Write the surviving productive contribution to the measured mixed-O2 flow as

```
F34,productive = p34 × epsilon × D
```

Here `p34` is the fraction of productive returned O2 born as 16O18O, and `epsilon` is the fraction of that signal recovered after release at the stated boundary. This recovery includes chemical loss or isotope replacement, reactor transport, and sampling losses; calibrated instrument response converts signal to flow separately. A rate-weighted version is needed if sources differ materially along the bed.

For independent isotope labels on fresh parent-O2 events and isotope-blind pairing of their leftover atoms, `p34 = 2x(1−x)`. Lateral mixing of a homogeneous surface pool is not necessary under those assumptions. A leftover atom cannot recombine with its already-exported EO partner; recombination of an untouched parent pair is a different exchange process. Thus, merely citing spatially separate sites or geminate recombination does not defeat the productive prediction. Return and reactivation within the restricted network alone also do not recreate a second surviving atom of a fresh parent. Relevant failures include re-entry of product oxygen that restores both fresh-parent atoms, different isotope compositions in chemically distinct oxygen supplies, or exchange of the leftover oxygen with product/support oxygen before return. An EO isotope ratio near one-half is a useful consistency check, not by itself proof of every required event-label assumption.

Let `U34` be a joint, one-sided upper uncertainty limit on the total newly generated mixed-O2 flow that survives to analysis, after allowing for inlet mixed-O2 survival. Let `k_min` be a defensible lower bound on `p34 × epsilon`. Then

```
D_upper = U34 / k_min.
```

Keep spectator scrambling in `U34`: it makes this upper bound conservative. Subtracting a no-ethylene exchange result is unjustified because removing ethylene changes the working surface. A large spectator signal can make the upper bound useless, even when measured very precisely.

**Raw outlet-minus-inlet mass 34 is insufficient.** Inlet 16O18O can be consumed or isotopically replaced in the bed, offsetting newly formed 16O18O. The uncertainty bound must allow for that loss. For example, if the incoming mixed-O2 survival has a validated lower bound `t_min`, use an upper bound on `F34,out − t_min F34,in`, with blank and response uncertainty, rather than treating `F34,out − F34,in` as gross formation. Isotopic atomic purity alone does not specify the supplied 32/34/36 molecular fractions; measure them.

The required return in the restricted cycle is `D_required = (e−3z)/2`, where `e` and `z` are net EO and CO2 molar formation rates. The subsequently [audited extension](../calculations/epoxidation-oxygen-return.md#conservative-extension-for-dissociation-secondary-combustion-and-ethane) includes independent O2 dissociation, secondary EO combustion and the specified ethane-to-ethylene oxygen sink `a`. For that model, use the conservative required **cross-parent** return `max[0,(e−3z−a)/2]`; isotope analysis does not bound all gross same-parent recombination. Obtain a joint lower limit from the actual net product/cofeed measurements. Reject the applicable return-only explanation at the stated boundary only if

```
U34 < k_min × D_required,lower,
```

using a prespecified joint uncertainty level, for example 95%, for both sides, with systematic error and drift included. Two unrelated nominal 95% limits do not automatically give 95% joint coverage. If `k_min` cannot be bounded above zero, or `D_required,lower ≤ 0`, a negative isotope result is not decisive.

### Numerical target, conditional on the illustrative state

At 10% inlet O2, 1% O2 conversion, and `S=1.4`, normalization to inlet total flow gives:

| Flow | ppm of inlet total molar flow |
| --- | ---: |
| Net O2 consumption `q` | 1,000 |
| Net EO formation `e` | 1,166.7 |
| Net CO2 formation `z` | 277.8 |
| Required O2 return `D_required` | 166.7 |
| Mixed O2 born at `p34=0.5` | 83.3 |

These are normalized flows, not uncorrected outlet concentrations. As an illustrative acceptance target, a complete one-sided upper limit `U34=20 ppm` and independently supported `k_min=0.40` give `D_upper=50 ppm`. That would provide useful margin if the lower bound on required return remained well above 50 ppm. Neither 20 ppm capability nor 80% recovery is established here. Merely demonstrating instrument sensitivity to an 83 ppm standard does not establish either quantity under reaction conditions.

## 3. The product balance may be harder than the isotope peak

The required return is a difference of measured product rates. With 0.5% CO2 cofed, the illustrative 278 ppm net CO2 formation is only a 5.6% increment over the inlet. Independent 1% relative errors in inlet and outlet CO2 readings would give roughly 70–73 ppm standard uncertainty in their difference, before flow corrections. Multiplication by three gives about 212–218 ppm standard uncertainty in `3z`, against an excess `e−3z` of only 333 ppm. Even perfect mass-34 analysis would not rescue an unresolved required-return rate.

First use a matched inlet/outlet calibration and internal flow normalization, with measured repeatability, drift, and covariance. If necessary, choose a somewhat higher conversion already shown to preserve the relevant working state, and repeat the necessary transport and secondary-oxidation checks. Increased conversion is not a free signal amplifier: it changes product partial pressures, oxygen depletion, and possibly surface chlorine coverage.

A 13CO2 cofeed could separate newly formed predominantly 12CO2 from cofed carbon, but adds isotope supply, analytical channels, and retained-carbon/exchange checks. Do not add it by default. If ordinary difference measurements cannot resolve the excess at a valid operating point, the proposed small diagnostic fails its first gate. Independent O2 consumption and atom-balance closure remain useful cross-checks; reconstructing O2 consumption from the same EO/CO2 data does not add independent evidence.

## 4. Minimum viable calibration and reaction sequence

Use one existing, stable catalyst state with a resolved positive required-return rate. Do not begin with the entire Ni × Re matrix.

1. **Confirm analysis in the actual matrix.** Quantify 32/34/36 O2 at inlet and outlet; calibrate response, background, peak tails/cross-talk, inlet impurities, pressure dependence, and drift. Use standards or calibrated additions around the decision threshold, carried through the sampling train. Check matrix interferences experimentally. Any carrier contribution at the selected masses needs measured correction. Use an inert internal standard and flow accounting. Confirm ordinary EO/CO2 analysis; if product isotope fractions become necessary, separate overlapping EO and CO2 molecular-ion signals rather than assigning shared nominal masses to one product.
2. **Check the apparatus separately.** Run bypass and hot empty/support blanks under matched gases to identify scrambling or losses in plumbing, packing, support, and the sampling train. These calibrate the apparatus; they do not reproduce catalyst spectator exchange. Measure residence time with an inert tracer.
3. **Bound bulk-path recovery under reaction.** Introduce a small calibrated change in incoming mixed-O2 content, keeping total O2 and, as closely as practical, total isotope atom fraction fixed. Measure its recovery through the working bed. Choose the tracer amount to leave chemical rates unchanged. Interpret it with a simple transport model whose source locations are stated; establish why its conservative recovery applies to oxygen entering the bulk gas within the bed. An inlet tracer's recovery cannot certify recovery before surface-born oxygen has escaped into that gas. If unknown gross exchange prevents a positive useful recovery bound, stop.
4. **Measure a steady mixed feed and repeat the reference.** Keep total O2, ethylene, ethane if present, CO2, water, chloride, pressure, temperature, and flow matched. Confirm unchanged net rates and selectivity within the prespecified uncertainty. Maintain each isotope plateau until gas signals and relevant product-label responses stop drifting; chemical steady state alone does not establish isotope steady state. Repeat the central mixture after a return to the reference to quantify drift and memory. If a resolved signal needs a pairing check, add one second isotope fraction; agreement with the expected curvature is a consistency test, not proof of productive assignment.

No O2-free pulse or nonreacting TPD measurement substitutes for this sequence. An ethylene-off exchange measurement may characterize an alternative state, but cannot provide the required background subtraction or recovery correction for the working catalyst.

## 5. Product exchange and transport: constrain only what affects the decision

CO2, water, support oxygen, and retained oxygen can exchange isotope labels without net accumulation or a corresponding EO-forming turnover. They can generate spectator scrambling, alter the isotope composition of leftover oxygen, or replace labels after return. Water handling can also delay isotope responses in transfer lines. Consequently, a delayed product label or mixed CO2 is not a direct measure of return.

For an upper-bound experiment, additional nonnegative scrambling sources need no mechanistic separation. The critical question is whether exchange can suppress the expected productive mixed-O2 signal or invalidate the fresh-parent label assumption. Start with inlet/outlet isotope distributions, stable plateaus, total product balances, and the recovery check. If these expose significant unmatched isotope reservoirs or product-to-O2 exchange, add the one targeted product-isotope measurement needed to bound that effect. If multiple unconstrained reservoirs require simultaneous fits to O2, EO, CO2, water, and site-specific spectra, classify the small test as unidentifiable and stop. Such a fit does not automatically produce a reliable bound.

Use the actual promoted state and its pressure. A low-pressure mass-spectrometer-compatible surrogate does not answer the high-pressure working-state question. Preserve the product environment when changing flow or bed dilution. Existing heat/mass-transfer checks should establish negligible gradients at the chosen point; a narrowly targeted flow/dilution check can test an apparent escape or transport dependence. Even successful bulk checks do not establish the absence of microscopic recapture.

## 6. What the existing precedent supplies

[Pu et al. 2024](../../literature/papers/pu2024-revealing-the-nature-of-active/fulltext.md), DOI [10.1021/acscatal.3c04361](https://doi.org/10.1021/acscatal.3c04361), §2.8, used a 16O2→18O2 switch at 225 °C with 1.2% ethylene and 3000 ppm O2 in Ar, after 50 minutes of conditioning. Section 3.5 reports no detected mixed O2 and points to Fig. S16. This supports the relevance of the observable, but does not supply a numerical upper flux limit in the inspected main text. Its unpromoted catalyst, dilute oxygen feed, and isotope-switch window do not establish sensitivity or recovery for a steady mixed feed on Ni/Cs/Re/Cl–Ag. The reported calculated recombination barrier does not supply the missing analytical calibration.

The [subsequently recovered SI](../../literature/papers/pu2024-supplementary-information-for-revealing-the/fulltext.md), p. 18, supplies Fig. S16 but no reported m/z-34 calibration, detection limit, isotope-feed purity or response correction. Its p. 22 product-isotope table and model-dependent MvK estimate do not supply that calibration. The retrieval gap is resolved; the quantitative measurement limitation remains.

## 7. Burden and stopping rules

If a suitable working reactor, isotope-compatible gas delivery, calibrated O2 isotope analysis, and a stable catalyst already exist, the bounded work is a calibration/recovery block and one repeated reacting-state comparison, with a second isotope fraction only when informative. Long chemical conditioning and isotope washout may still dominate elapsed time and isotope consumption. No defensible calendar or budget estimate follows without actual flow, pressure, hold-time, and equipment information.

Proceed beyond calibration only when all three quantities are supported: a positive lower bound on required return, a useful positive `k_min`, and a total mixed-O2 upper limit capable of crossing the rejection threshold. A small negative signal then constrains the specified bulk-return explanation. A large signal leaves it viable without proving it. Failure of recovery or label assumptions limits the claim to observed escaped mixed O2. Failure of analytical or product-balance precision stops the test.

**Recommendation:** assess feasibility using existing capability before considering a new instrument campaign. The expected value is a clean exclusion of a specific bulk-return mechanism if the gates pass. It is not a general measurement of every leftover-oxygen fate or a site-specific demonstration of Ni-to-Re transfer.

## Source handling

No literature knowledge-base files were edited and no literature checks were run by this reviewer. The Pu SI request was sent to the existing `/root/literature` agent; a later root update records its completed retrieval and reading while preserving the original experiment's analytical limitation.
