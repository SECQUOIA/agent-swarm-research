# Independent review: what the ammonia H₂-scavenging experiment establishes

Updated 2026-09-16 after literature uploads. Original mechanistic checks are retained; source status and finite-pressure comparisons below incorporate the [post-upload audit](post-upload-pdh-ammonia-audit.md). The [working screen](../working/ammonia-kinetics-screen.md) contains the completed minimum experiment and stopping decisions.

## Decision

Qiu et al. provide convincing evidence that added H₂ inhibits their Ru/MgAl₂O₄ catalyst and that small O₂ cofeeds substantially increase ammonia conversion under the dilute conditions studied. Their thermal and structural controls deserve weight. The evidence does **not** identify zero working H* coverage, uniquely establish removal of an unchanged inhibitory H* population as the entire cause of promotion, or demonstrate the predicted concentrated-feed rate gain with physically recovered hydrogen.

A useful finite study could determine whether the large low-H₂ rate reserve survives **oxygen-free operation at the finite H₂ pressure imposed by a specified separation device**. Its decision would be whether to invest in hydrogen-removal hardware for this catalyst, or instead select a catalyst that works better at the device's unavoidable H₂ pressure. This is a concrete catalyst–device selection question. Generic demonstration of kinetic promotion by membranes, kinetic-model discrimination, and hydrogen scavenging are established prior art. This review does not yet identify a substantial original program beyond that literature.

### Sources actually checked

- [Qiu et al., 2026, main article](https://doi.org/10.1039/D6RE00086J): original `/tmp/ammonia-screen/qiu2026.pdf`, main text and methods read; Fig. 3 visually inspected.
- Original two-page SI `/tmp/ammonia-screen/qiu2026-si.pdf`: all text read; Table S1 and Figs. S1–S2 visually inspected.
- Conference precursor `/tmp/ammonia-screen/qiu-iscre.pdf`: text read. Its O₂ range and author list differ from the final paper; use the final paper for the definitive experiment. Its “turnover frequency” description is not a reason to reinterpret the final SI's fitted constants as measured TOFs.
- [Itoh et al., 2014](../../literature/papers/itoh2014-kinetic-enhancement-of-ammonia-decomposition/original.pdf): full text now checked in the post-upload audit; experimental finite-pressure kinetic enhancement and the recovery denominator are resolved below.
- Coelho2026 journal main and its distinct preprint are now available. The journal work models non-isothermal balances and finite sweep; optimized performance is a prediction. Qiu2025, Coelho2025, Napolitano2025 and Lundin2024 originals were also checked for the post-upload corrections. Current package links are in the working screen.

## 1. Strong observations and their limits

| Observation in Qiu | Supported inference | Inference requiring more evidence |
|---|---|---|
| Adding 1–25% H₂ shifts conversion curves upward in temperature at fixed dilute NH₃ feed; one empirical rate law describes multiple composition series | H₂ has a strong inhibitory effect in the tested operating window | Unique elementary rate-determining step, unique identity or abundance of the blocking adsorbate |
| O₂ cofeed raises conversion; independent bed thermocouple gives approximately 0.7 °C deviation from furnace setpoint | The measured bulk bed-temperature rise cannot plausibly account for the large enhancement by itself | Oxygen has no chemical role beyond lowering H₂/H* |
| XRD, HRTEM, ICP-OES and H₂-TPR comparisons show no major Ru loss, crystallite growth or bulk oxidation under the tested NH₃/O₂ treatment | A large persistent transformation into a bulk Ru oxide or gross sintering is an implausible explanation | No transient O*, OH*, NHₓ or minority-site change during turnover |
| Reference activity at 1% NH₃ and 320 °C remains essentially stable across 15 days of tests involving varying O₂ | Useful operational evidence against major lasting damage in this experiment | Fifteen days of uninterrupted operation at one fixed O₂ feed, concentrated-feed durability, or an operando surface census |
| He-TPD gives much less detectable H₂ after NH₃/O₂ exposure | Pretreatment changes the inventory that survives the intervening purge/cooling sequence and later releases H₂ | Zero H* during reaction, or a quantitative working H* coverage |

The alternative to pure unblocking need not be bulk oxidation. A low population of adsorbed oxygen or hydroxyl groups could alter NHₓ dehydrogenation and disappear on switching feeds, while Ru remains predominantly metallic. This is a **possible unresolved alternative**, not a demonstrated explanation of Qiu's data. Absence of detected NOₓ and rapid separate H₂ oxidation support the proposed consecutive scheme but do not uniquely establish its elementary route; direct oxygen-assisted conversion to N₂/H₂O would have the same net stoichiometry.

The paper expressly acknowledges that O₂ consumes the hydrogen product and that practical H₂ production needs another removal method. Calling the diagnostic experiment a failed H₂-productivity demonstration would misrepresent its purpose.

## 2. TPD is especially easy to overinterpret

The main methods specify reaction pretreatment, then **one hour of He at 250 °C**, cooling to 50 °C in He, and a ramp to 450 °C at 5 °C/min followed by a one-hour hold. The figure also includes a 320 °C reaction pretreatment. Desorption, reaction and redistribution can occur during the purge and cooling before the recorded ramp. The material being measured is a retained post-treatment population.

SI Fig. S2 itself assigns part of the later H₂ signal to NH₃/NHₓ reaction during the temperature ramp. Consequently, total H₂ released is not a direct pre-existing H* inventory. Conversely, little H₂ released after NH₃/O₂ treatment could reflect removal of a strongly retained population, its conversion into another reservoir, or altered subsequent chemistry. The working population need not be zero.

The SI's graphical H₂ peak annotations are approximately 1.2 + 2.1 µmol after the 250 °C NH₃ pretreatment and 0.4 + 1.7 µmol after 320 °C. These do not establish a rising **absolute** H* inventory with pretreatment temperature. Changing assignments and relative populations may support a qualitative interpretation, but the main-text phrase about H* growing with temperature should not be repeated as a measured absolute coverage trend. No surface-Ru-normalized coverage, full H balance through the purge, or calibrated upper bound on residual H* is supplied.

### Keep the TPD pretreatment separate from the zero-outlet-H₂ points

Main Fig. 3 selects O₂-cofeed temperatures where H₂ and O₂ are both reported exhausted. The highest-O₂ point, 0.25% O₂ with 1% NH₃, is near 238 °C and roughly 37% conversion by visual reading. SI Fig. S1 gives 238.7 °C for a 238 °C furnace setpoint.

By contrast, SI Fig. S2c describes **250 °C and approximately 70% conversion** during pretreatment with 1% NH₃ + 0.25% O₂. This is not the same chemical state. For N₂ and H₂O products,

`F_H2,out = 1.5 F_NH3,in X − 2 F_O2,consumed`.

The feed ratio 0.25% O₂/1% NH₃ can consume all generated H₂ only through `X = 1/3`. At 70% conversion, remaining H₂ is `0.55 F_NH3,in`, assuming steady material balances and no other net H reservoir. Thus the TPD comparison does not even nominally examine a gas phase with zero H₂ during its NH₃/O₂ pretreatment. This makes its identification with zero working H* particularly unwarranted.

The visually read highest Fig. 3 point exceeds the exact 33.3% stoichiometric endpoint modestly. Raw flow calibrations, detection limits and balances would be needed to resolve that difference. Treat it as a closure/uncertainty qualification; it does not erase the large observed conversion promotion or justify alleging an invalid experiment.

## 3. The ideal rate is a model extrapolation

Main eq. 4 is

`r = k(T) P_NH3 (1 + K_H2 P_H2)^−1.5 (1 − η)`.

The authors explicitly state that this modified expression has no direct mechanistic derivation. The zero-inhibition construction sets `K_H2 = 0` and `η = 0`, keeping `k(T)` fixed. This is a useful conditional limit of that fitted model. It is not an independently measured rate constant of an unchanged catalyst with H* removed.

A catalyst modification that weakens H binding may also change NH₃ activation, nitrogen binding, active ensembles and `k(T)`. Physical H₂ removal changes gas chemical potentials but does not change the catalyst's adsorption constant. Neither operation is automatically equivalent to deleting the fitted denominator while preserving everything else. In particular, consumption or removal of a product does not eliminate all transient surface hydrogen formed during N–H cleavage.

SI Table S1 fits simulated inhibited conversion curves to pseudo-first-order kinetics, then divides the ideal fitted constant by those effective constants. The factors **14, 57 and 633** refer respectively to modeled 1%, 10% and pure-NH₃ feed cases at 250 °C. They are not measured site-normalized rates, and the 633-fold number is not an experimental high-pressure result. The comparison also includes the consequences of reactor composition profiles and the model assumptions. The reported concentration-independent ideal conversion is not separately observed over this range. First-order kinetics alone give that result only with the corresponding constant-flow approximation; changes in gas molar flow matter for concentrated feeds, as checked below.

The now-read Qiu2025 main explicitly acknowledges low-temperature H2-lean limitations of its hydrogen-rich power law, correlated adsorption parameters and possible desorption control outside its preferred regime. Coelho2025 reanalyses Lundin2024 data on commercial 0.5 wt% Ru/Al2O3, rather than independently reproducing Qiu's 1 wt% Ru/MgAl2O4. Its preference for an N-desorption model is a model-selection result in that domain, not a contradiction of a universal mechanism established by Qiu. Both descriptions require testing where they would lead to different attainable device choices. Qiu2025 main p.7 also reports successful representation of commercial Heraeus Ru-catalyst data up to pure NH3 feed (Fig. S7), which is meaningful high-concentration validation. Pure NH3 produces H2 during conversion and therefore does not test a near-zero local H2 regime. Its separate Ru/MgAl2O4 low-GHSV reactor-sizing result in Figure 11 is modeled. The present validation requirement concerns transfer to the selected material and attainable low-H2 boundary, not an absence of any published pure-NH3 validation.


### Additional consistency check: 250 °C conversion and gas expansion

Using SI Table S1's ideal `k = 3.58 × 10⁻⁴ mol/(g s atm)` (the table's printed units are inconsistent with its first-order equation), inlet `GHSV = 20 Nl/(g h)` and `22.414 Nl/mol` give `Ftot,in/W = 2.47861 × 10⁻⁴ mol/(g s)`. At one atmosphere the dilute, constant-flow first-order Damköhler number is 1.44436, giving **76.4% conversion**. Main Fig. 3 visually approaches approximately 80% near 250 °C and nearly complete conversion closer to 280 °C. Thus the main-text statement of full conversion at 250 °C does not follow from these printed values. This is a consistency qualification, not evidence that the observed O₂ promotion disappears.

For pure NH₃, gas flow must be specified. Instantaneous removal of all generated H₂ leaves `Ftot/FNH3,in = 1 − X/2`; integrating the same first-order rate gives `Da = −0.5 ln(1−X) + 0.5X`, or **86.8% conversion** at the same Da. Retaining generated H₂ while merely deleting its inhibition instead gives `Ftot/FNH3,in = 1 + X`, `Da = −2 ln(1−X) − X`, and **64.9% conversion**. These are explicitly conditional analytical checks with the equilibrium term also removed. They are not reconstructions of the authors' unpublished code. The paper's stated species balances do not supply enough implementation detail to resolve how its ideal concentration-independent curve handles removal and changing molar flow.

## 4. Finite-pressure check independently reproduced

Taking the published `K_H2 = 5000 atm⁻¹` literally, and isolating the denominator at the same temperature, NH₃ pressure and thermodynamic driving force, the fraction `f` of the model's uninhibited forward factor requires

`P_H2 ≤ (f^(−2/3) − 1)/5000 atm`.

| Retained fraction `f` | Maximum H₂ partial pressure under this model |
|---|---:|
| 0.10 | 73.8 Pa |
| 0.50 | 11.9 Pa |
| 0.90 | 1.47 Pa |

A passive H₂-selective membrane needs higher H₂ chemical potential on the retentate side than on the permeate side. A one-bar pure-H₂ permeate therefore cannot maintain the near-zero retentate H₂ pressure associated with these particular model limits. Increasing total NH₃ pressure does not remove that constraint. Finite membrane resistance and transport from catalyst to membrane add a required gradient.

These are model-dependent feasibility bounds, not measured adsorption thresholds or universal requirements for useful membrane promotion. Lowering H₂ from several bars to around one bar may still improve an inhibited rate substantially. The bound only limits proximity to this model's ideal zero-H₂ rate. Its constant `K_H2`, the low-pressure extrapolation, and transfer to concentrated NH₃ require validation.

For illustration, reversible isothermal compression of pure H₂ from 11.9 Pa to one bar requires `RT ln(Pout/Pin)`: **39.3 kJ/mol at 523.15 K**, or approximately **22.4 kJ/mol at 298.15 K**. The first is not a universal plant minimum: cooling before compression changes the work. Neither value is a complete vacuum/sweep/purification/heat-integration cost or proves an economic disadvantage. Avoid counting vacuum removal and subsequent compression twice.

## 5. What experiment would change a consequential decision?

The cleanest bounded objective is to locate the usable rate at the **actual lowest achievable H₂ chemical potential**, before buying a membrane system on the strength of the 633-fold extrapolation.

1. Specify one candidate separation device's permeate pressure, attainable flux, delivered-H₂ specification and allowable recovery burden. Without these, there is no meaningful practical target pressure.
2. Measure oxygen-free differential rates on the reproduced Ru/MgAl₂O₄ catalyst over H₂ partial pressures bracketing that target. Maintain NH₃ partial pressure and measured catalyst temperature; include independently metered product H₂, N₂ and NH₃ balances. Reduce catalyst loading/contact time enough that generated H₂ does not silently dominate the supposedly low-H₂ feed. Calibrate the resulting small conversion signals and establish transport independence.
3. Test the transfer of the rate prediction to a concentrated NH₃ condition **without refitting the original decision point**. Include a credible high-performing Ru catalyst at equal Ru inventory and the same product boundary, rather than comparing with an intentionally weak inhibited case. The comparison can use a chemically different material; it is a practical selection test, not a proof of one support mechanism.
4. Proceed to physical removal only if measured rates and attainable membrane flux support a useful delivered-H₂ rate. A paired membrane-on/off experiment should quantify H₂ exported, NH₃ slip, additional Ru/Pd inventory, area, heating and pressure work. The scientifically useful result is whether measured finite-pressure kinetics correctly select the catalyst/device combination, not whether the conversion rises on opening a permeate valve.

An oxygen-free low-H₂ rate plateau would strengthen the inference that a substantial reserve is available without oxygen chemistry. A substantial shortfall would prevent extrapolating the O₂ diagnostic into a hardware target. Neither outcome by itself identifies the unique elementary rate-determining step. If uncertainty in that identity does not change material or device choice, an elaborate isotope campaign has little added decision value here.

**Prior-art restriction:** [Itoh2014](../../literature/papers/itoh2014-kinetic-enhancement-of-ammonia-decomposition/original.pdf) derives seven rate models, demonstrates model-dependent membrane enhancement, and reports conversion rising from approximately 73% to 87% at 723 K with a roughly 200 µm membrane and 1000 Pa permeate pressure. This is about 14 percentage points, rounded to 15% in the conclusion. Recovery near 60% is relative to the theoretical hydrogen in incoming NH3, not simply the fraction of produced H2 permeating. The thinner-membrane gain is simulated. This directly establishes that kinetics guided membrane design before Qiu's study.

[Napolitano2025](../../literature/papers/napolitano2025-enhanced-ammonia-decomposition-using-a/original.pdf) demonstrates useful atmospheric-permeate operation at 400 °C and 3–5 bar feed on a different catalyst. Its recovery denominator includes inlet H2. The largest conversion ratio combines a mixed-feed membrane reactor with a pure-NH3 conventional reference; >90% purity applies to selected mixed feeds, not all cases. Figures 6 and 7 give inconsistent recovery for one nominal mixed-feed 5-bar point. The comparison should therefore use net newly generated H2 at a stated purity, include upstream conversion, and avoid combining maxima. These results do not reach or validate Qiu's near-zero-pressure ideal factor.

[Lundin2024](../../literature/papers/lundin2024-modeling-of-an-ammonia-decomposition/original.pdf) provides measured membrane-reactor validation and coupled kinetics, radial transport, real geometry, heat and impurity permeation. It uses local atmospheric permeate pressure near 82 kPa without experimental sweep; tests last less than 12 h. Trace-purity validation is limited by detection, even when conversion and recovery are well predicted. Coelho2026 provides further finite-sweep configuration modeling. A generic coupled model or another fit comparison is consequently insufficient originality.

**Confidence:** strong that H₂ inhibition and O₂ promotion are real in Qiu's tested window; low that the TPD establishes zero working H*; moderate that the proposed finite-pressure screen would be informative on an appropriately equipped platform; uncertain that it produces a practically superior catalyst/process. No relevant platform has been verified. A broader program would need a demonstrated consequential catalyst/device selection error in current practice and a transferable improvement beyond these prior results. This is a reason to keep the bounded opportunity conditional, not to require a successful experiment before proposing research.

## Literature handoff retained

Original requests were routed to the sole literature worker. Current available/read packages include Itoh2014 **10.1016/j.cattod.2014.02.054**, Cechetto2023 **10.1021/acs.energyfuels.3c00760**, Coelho2026 **10.1016/j.seppur.2026.137082** and its distinct preprint **10.2139/ssrn.5935018**, the active-membrane preprint **10.26434/chemrxiv-2025-cv1ld**, and the pressure-boundary study **10.1016/j.ijhydene.2026.154910**. The old HTTP failures describe retrieval history, not current lack of source access. Qiu2025, Coelho2025, Prasad2009, Napolitano2025 and Lundin2024 are also now available. See the [current source register](../working/ammonia-kinetics-screen.md#current-sources-and-unresolved-content) for package links and the two still-unretrieved thesis bodies. This review did not edit the KB.

## Independent follow-up: product H₂ limits differential-rate measurements

The root's proposed feasibility calculation is correct. For decomposition alone at constant total pressure, no inlet H₂, inlet NH₃ mole fraction `y`, and inert balance, `Ftot,out/Ftot,in = 1 + yX` and `y_H2,out = 1.5yX/(1+yX)`. Writing the allowable H₂ mole fraction as `z = P_H2,limit/Ptotal`, inversion gives `Xmax = z/[y(1.5−z)]`.

At `y = 0.01` and one atmosphere, the model's half-rate H₂-pressure threshold gives `Xmax = 0.007832627`, or **0.7833% conversion**. Its 90%-rate threshold gives `Xmax = 0.000970223`, or **0.09702% conversion**. These independently reproduced values are analytical measurement targets, not measured achievable conversions or universal differential-reactor criteria. They concern the outlet bulk gas; hydrogen gradients at or within catalyst particles can require lower conversion, and deliberately cofed H₂ uses part of the allowable H₂ pressure. Resolving such small NH₃ consumption or N₂ formation accurately is therefore a material feasibility requirement for the proposed oxygen-free low-H₂ test.
