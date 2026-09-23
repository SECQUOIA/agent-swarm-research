# Ag isotope reversibility: what the recovered propylene SI changes

Date: 2026-09-15. Independent, bounded review of Esposito and Bhan's supporting information, especially S7–S9. The [SI](../../literature/papers/esposito2024-supporting-information-for-isotopic-studies/fulltext.md), DOI [10.1021/acscatal.4c04218.s001](https://doi.org/10.1021/acscatal.4c04218.s001), was inspected directly; equations were checked against the original PDF, including a rendered p.30. The main journal article was unavailable for that initial review; its uploaded original was subsequently checked on 2026-09-16, as recorded below. Context: [oxygen-return balance](../calculations/epoxidation-oxygen-return.md), [escape calculation](../calculations/oxygen-escape-bound.md), and [isotope feasibility review](epoxidation-isotope-feasibility.md).

## 2026-09-16 main-text and ethylene update

The [2024 main](../../literature/papers/esposito2024-isotopic-studies-of-reaction-pathways/original.pdf), Section 3.3/Figure 4, confirms CO2 labeling of reactive oxygen and the approximately 0.02 reverse/forward scale. It explicitly allows an O2-derived precursor formed reversibly before irreversible generation of the CO2-exchanging oxidant. The result therefore does not require every prior adsorption event to be irreversible. The main does not supply a new statistical upper confidence bound for the SI calculation.

The [2026 main](../../literature/papers/esposito2026-common-active-sites-and-oxidants/original.pdf) and [SI](../../literature/papers/esposito2026-supporting-information-for-common-active/original.pdf), S2–S4, support ethylene/propylene competition for a shared oxidant on K/NO/Cl–Ag/CaCO3. They also show EO orders of approximately 0.6 in ethylene and 0.45 in O2, with selectivity increasing from 83.6% to 91.0% across the ethylene series. These kinetic distinctions prevent automatic transfer of propylene sole O2-activation control, or its return bound, to ethylene. No ethylene isotope-return measurement or Ni/Cs/Re test is supplied. The existing population, balance and usefulness gates remain required. See the [source audit](post-upload-ag-audit.md).

## Decision

**Replace the optional branch's default measurement argument with an adaptation of this established isotope balance; keep the ethylene question conditional.** The SI already uses CO2 to label the reactive oxygen population, measures return to gaseous O2, and estimates oxygen-activation reversibility near 0.02. This is substantive quantitative prior art, beyond a qualitative absence of scrambled O2. A general proposal to bound oxygen return by isotope analysis is therefore not new.

The remaining question is whether return can explain the required oxygen utilization on the actual promoted ethylene catalyst, using a measured product balance and a validated connection between its product-forming and O2-returning oxygen populations. Applying that exclusion criterion to a distinct Ni-containing working state could be useful; no practical improvement or novelty of the measurement itself follows.

The source's CSTR balance already corrects readsorption from a common gas population. It does not need an additional empirical escape factor for that same process. The previous transport discussion remains relevant where a surface-born molecule is recaptured before joining the common gas, or where spatial gradients invalidate that balance. Neither possibility is grounds to dismiss the source's conditional result without evidence that it matters.

## 1. What the SI establishes

The apparatus is an external-recycle reactor. The oxygen-label experiments used K–Ag/CaCO3 at 513 K and 110 kPa, with propylene, roughly 5% 18O2, varied C16O2, allyl chloride and NO. These are reacting, promoted-Ag measurements. They are not ethylene measurements on Ni/Cs/Re/Cl–Ag. [[esposito2024-supporting-information-for-isotopic-studies]] p.3; p.24

S7 reports CO2 isotopologue distributions close to binomial at three CO2 contents, and approximately matching oxygen isotope fractions in CO2 and products. S8 treats exchange through carbonate formation/decomposition, with each carbonate oxygen equally likely to remain on the surface. This model estimates fast exchange relative to the oxidation oxygen demand. [[esposito2024-supporting-information-for-isotopic-studies]] p.24–28

For clarity, S87 simplifies to

\[
\frac{k_sP_{CO_2}}{k_{ox}P_{C_3H_6}\nu_{ox}}
=\frac{3(1-f)}{2(f-c)},
\]

where `f` is the active oxidant's 18O atom fraction and `c` is the CO2 oxygen's 18O atom fraction. The reported approximate pairs `(f,c)=(0.06,0.02)` and `(0.45,0.40)` give 35.25 and 16.5, consistent with the authors' approximately 35 and 16. The denominator includes the oxygen-consumption stoichiometry `νox`; this is a model-normalized exchange propensity, not a directly counted number of CO2 exchanges per propylene molecule. It is sensitive to the small difference `f−c`. Fast exchange is credible; the exact ratios remain conditional on the carbonate and common-pool model. [[esposito2024-supporting-information-for-isotopic-studies]] p.27–28

The important experimental idea is to give surface oxygen a very different isotope composition from feed O2. Substantial reverse activation would then generate an O2 isotopologue that is scarce in the gas. CO2 exchange supplies that contrast without requiring labels to retain their original O2-parent ancestry.

## 2. S99 checks algebraically and numerically

Define all rates on the same steady reactor boundary:

- `A`: gross forward consumption of gaseous O2.
- `D`: gross return to that gaseous O2 population.
- `q=A−D`: net O2 consumption, positive here.
- `J32`: net 16O2 formation, positive for outlet minus inlet.
- `m=J32/q`, `y=P16O2/PO2`, and `x=θ16O/θO`.

With isotope-independent activation and random pairing in the returning atomic-oxygen population,

\[
J_{32}=x^2D-yA,\qquad
\boxed{R\equiv\frac DA=\frac{m+y}{x^2+m}},\qquad
\boxed{\frac Dq=\frac{m+y}{x^2-y}}.
\]

The first boxed expression is S99. Its numerator uses **net 16O2 formation**, despite the inconsistent prose reference to “consumption” beneath S99. The equations and final numerical application use the formation sign. [[esposito2024-supporting-information-for-isotopic-studies]] p.29–31

For the SI's `m=0.003±0.001`, `y≈0.003`, and `x≈0.55`:

| Assumed `m` | `D/A` | `D/q` |
| --- | ---: | ---: |
| 0.002 | 0.01642 | 0.01669 |
| 0.003 | 0.01964 | 0.02003 |
| 0.004 | 0.02284 | 0.02337 |

Thus the authors' approximately 0.02 scale checks. Their “maximal” wording refers to the atomic-oxidant model compared with their molecular-oxidant alternative. It is not a demonstrated statistical upper confidence limit covering measurement, pool and model uncertainty. The SI does not establish the confidence meaning of `±0.001` in S9, or give uncertainties for `x` and `y` there. [[esposito2024-supporting-information-for-isotopic-studies]] p.29; p.31

`D/A` and `D/q` should not be interchanged. Their difference is small here, but becomes consequential for more reversible activation. In the illustrative ethylene balance with `S=1.4` and no additional oxygen sink, return alone requires `D/q=1/6`, equivalently `D/A=1/7`. A valid ethylene bound as small as this propylene result would be discriminating. This comparison is a scale calculation, not a transfer of the measured bound between catalysts. Ethane consumption and the actual net product uncertainties must enter the existing conservative required-return calculation.

## 3. Exactly what recapture is included

The term `−yA` subtracts consumption of gas-phase 16O2, whether that molecule entered in the feed or was generated previously by the catalyst. Repeated return and activation are included in `D` and `A`. Setting `J32=x²D` would omit that correction and give the wrong answer.

For this treatment, oxygen leaving the surface must join the gas population whose composition determines adsorption. In an ideal CSTR that composition is the reactor/outlet composition. The SI plots its calculation using an approximately unchanged influent fraction of 0.003; a transfer experiment should measure the reacting gas fraction, rather than assume inlet and reactor compositions coincide. CSTR behavior also requires that the measured gas describes the gas encountered by relevant catalyst sites, with no important unresolved pore or film isotope gradients.

An O2 molecule formed and recaptured in a local environment whose isotope composition differs from `y` is not correctly counted by `yA`. One may instead define the boundary after that unresolved local excursion, in which case the inferred `D` is return to the common gas. That result cannot exclude all local recycling. Surface O2 reformation and reuse without gas release likewise remains outside this measured gas-return process.

The practical correction to the earlier feasibility review is specific: **do not require a separate inlet-tracer escape bound merely to correct ordinary readsorption already included by an applicable common-gas balance.** A validated spatial model remains necessary if the common-gas approximation fails. An external-recycle reactor designation supports the intended approximation; the SI alone does not provide the entire mixing and transport validation.

## 4. Surface-population assumptions that make the bound valid

1. **Product labeling represents the returning population.** Epoxide oxygen is a flux-weighted sample of oxygen transferred into epoxide. It represents the isotope fraction of oxygen capable of returning to O2 only if these are the same pool, rapidly exchange, or have separately supported matching isotope fractions. This is especially important for the ethylene proposal: the leftover atom and the atom transferred to EO must not be assigned the same isotope composition solely because both came from an oxygen intermediate. Product isotope exchange after formation must also be negligible or corrected.
2. **The pair probability is known or bounded.** S95–S96 use `P(16O,16O)=x²` for reactive pairs and isotope-independent recombination. This is a mean-field pair assumption, stronger than knowing the average oxygen isotope fraction. Actual lateral motion over the whole surface is not required if reactive pairs have independent labels with the same marginal fraction. Conversely, binomial CO2 and matching average product fractions support exchange but do not directly measure the label distribution of every O2-returning pair.
3. **Forward isotope selection is negligible or bounded.** With isotope-blind activation, the fraction of `A` consuming 16O2 equals `y`. The source assumes this and assumes negligible oxygen-isotope effects in the reverse step. It does not measure those kinetic isotope effects in S9. Its C–H/C–D effects elsewhere in the SI do not quantify 16O/18O effects.
4. **The isotope and chemical inventories are stationary.** Label stored in carbonate, support oxygen or another retained reservoir must not be drifting during the balance. Net total-oxygen exchange with an unaccounted source would require extending the balance. Exchange that only swaps oxygen labels need not invalidate it, provided the returning pool is characterized.

A compact way to retain uncertainty is to replace `x²` by the actual fraction `p` of returned O2 that is 16O2 and `y` by the actual fraction `a` of forward O2 consumption that removes 16O2:

\[
\frac Dq=\frac{m+a}{p-a}.
\]

A useful upper bound requires a supported positive lower bound on `p−a`, and joint uncertainty limits. Modest isotope effects can be propagated through these fractions. There is no source-supported oxygen-isotope-effect range here; assuming either exact equality or an arbitrarily large effect as established fact would be unjustified.

Ordinary pool heterogeneity is not automatically a loophole. If each domain pairs randomly and all domains have the same `x`, their combination still gives `p=x²`. If the **return-rate-weighted** mean is known to be `x`, variation between random-pairing domains gives `p=E[x_i²]≥E[x_i]²`, strengthening the bound. The real vulnerability is a mismatch between that weighting and the product weighting, or correlated pairs. For example, a return-dominant population poorly reached by CO2 cannot be assigned `x=0.55` from PO alone. This is a conditional failure mode, not evidence that it occurs in the reported catalyst.

Even pair independence can be relaxed if both atom positions in returned O2 have known marginal 16O fraction `x`: probability alone gives `p≥max(0,2x−1)`. At exactly `x=0.55`, this conservative replacement yields `D/q≤0.0619` for the central inputs. This illustrative calculation does not establish those return-weighted marginals experimentally. It shows why strong enrichment can retain information without perfect random pairing, whereas a product-average label fraction alone cannot.

## 5. A more useful optional ethylene adaptation

**First assess existing evidence and equipment for whether the CO2 cofeed can label the relevant return population at the actual working state.** This review does not recommend starting a new study. If a bounded consistency check is justified, change isotopic composition while holding total O2, CO2, ethylene, ethane, chloride, water and the other relevant partial pressures fixed. Measure gas O2 isotopologues and EO oxygen labeling at stationary plateaus, alongside the ordinary rate/selectivity comparison and net product balance. A reversible label-only CO2 switch could establish exchange with EO-forming oxygen; it would not alone establish exchange with the leftover oxygen that can recombine. Only a supported connection to that return population replaces the fresh-parent-label argument with a measured oxygen-pool contrast. An applicable common-gas balance could also avoid a separate survival-factor fit.

CO2 exchange can erase fresh-parent ancestry while improving the new pool-label contrast. The old cross-parent mixed-O2 prediction cannot therefore be carried unchanged into an exchange regime. The net stoichiometric required-return inequality can remain applicable if exchange only swaps atoms without net oxygen uptake or release, but its isotope-to-return mapping must be replaced and any additional net oxygen source included explicitly.

Use the existing CO2 level rather than increasing CO2 simply to obtain a favorable label fraction: changing CO2 pressure can change the state being tested. The SI's high-CO2 propylene result demonstrates the principle, not a guarantee of exchange on another support or promoter formulation. CO2 enrichment still adds isotope/product analysis, and it does not solve the uncertainty of net CO2 formation on top of a cofeed background. No evidence here establishes that the ethylene adaptation is cheaper or experimentally available.

If all three O2 isotopologues are already measured, an oxygen-atom balance offers an additional simplification. Define `t=(J32+J34/2)/q`, with both net isotopologue formation rates, and let `g` be the gas O2 oxygen's 16O atom fraction. If activation is isotope-blind and `x_r` is the 16O atom fraction of oxygen actually returned to gas, then

\[
\frac Dq=\frac{t+g}{x_r-g}.
\]

This derived alternative does not assume random pairing or fresh O2-parent ancestry. It still needs a valid return-weighted `x_r`, a common-gas boundary, and accurate net isotope flows. The SI's reported 16O2 ratio alone is insufficient to evaluate it; do not fabricate a mixed-O2 rate. It is an analysis option for existing isotope channels, not a reason to expand the instrument campaign.

The branch should stop if EO labeling and gas composition cannot support a useful lower contrast for the return population, if the net product balance cannot establish the required return, or if the state can only be represented by an unconstrained collection of oxygen pools. A negative result then reports the observed gas isotope flux; it does not exclude every leftover-oxygen fate. A positive return signal remains compatible with spectator exchange and does not prove that return causes selectivity.

## 6. Novelty and source status

**Established prior art:** CO2-to-reactive-oxygen isotope exchange on promoted Ag during epoxidation; quantitative isotope balances for oxygen-activation reversibility; a reported result near 0.02; and discrimination between activation and reverse release despite rapid CO2 exchange.

**Potential remaining contribution:** apply an appropriately validated balance to the specific promoted ethylene working state and compare its upper return flux with the lower flux required to explain measured oxygen utilization. That is a condition-specific mechanism test. It is not a new general oxygen-return diagnostic or proof of a particular Ni/Re intermediate.

No literature KB files were changed and no KB checks were run in this review. **The original missing-main request is closed:** Esposito and Bhan 2024, DOI [10.1021/acscatal.4c04218](https://doi.org/10.1021/acscatal.4c04218), is now retained with its SI. Esposito2026 main and SI are also retained and checked as described above. Remaining scientific limits concern transfer, population assignment and uncertainty, rather than access to these sources.
