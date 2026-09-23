# Independent review of the styrene cleaning thermodynamic screen

Date: 2026-09-15. Scope: [thermodynamic screen](styrene-cleaning-thermodynamics.md), its [recorded inputs](../calculations/styrene_thermochemistry_inputs.json), [offline calculation](../calculations/styrene_thermochemistry.py), [stored output](../calculations/styrene_thermochemistry_output.json), and the [oxygen-fate program](../programs/zirconia-styrene-oxygen-fate.md).

## Verdict

**The calculations support a useful, bounded experimental branch. They do not yet strengthen the evidence for practical catalyst performance.** Ordinary benzene or toluene in a feed can reduce the driving force of the proposed terminal-alcohol cleaning reactions without directly poisoning active sites. That is a testable distinction worth adding to the program. Product identity, sustained oxygen balance, and kinetic accessibility are still unknown; no route has been demonstrated or excluded as a complete cleaning mechanism.

I independently reconstructed the main numbers from the source heat-capacity tables, using numerical midpoint integration rather than the original analytic segment method. All important reported figures agree. I also read the calculation code and reran it; the generated JSON exactly matches the stored output. The main remaining risks are interpretation and incomplete thermochemical uncertainty, not an arithmetic error.

## 1. Equations, phases, and standard states

All three proposed reactions balance carbon, hydrogen, and oxygen. They use ideal-gas products and reactants, with dimensionless activities `a = p/(1 bar)`. Thus `ΔrG = ΔrG° + RT ln Q` and `K = exp(−ΔrG°/RT)` are applied correctly. At 773 K, `RT = 6.42708 kJ/mol`.

The benzene/ethanol and toluene/methanol reactions have zero gas mole change; a common total-pressure factor cancels from Q. The acetophenone reaction has gas mole change +1; its stated activity expression correctly retains that pressure dependence. Its factor of `a_H2²` is a thermodynamic stoichiometric factor, not a prediction of kinetic hydrogen order.

Using gas thermochemistry at 298 K is valid even for compounds whose stable bulk phase at that temperature is liquid: the calculation requires the gas standard state. Liquid formation enthalpies must not be substituted.

The organic Cp integration is correct:

```text
ΔH = ∫ Cp dT
ΔS = ∫ Cp/T dT
ΔrG°(T) = ΔrH°298 − TΔrS°298 + ∫ ΔCp(1 − T/T′) dT′.
```

The water Shomate expression is evaluated at 773 K inside its stated 500–1700 K range. Its enthalpy expression explicitly returns `H(T) − H(298.15)`, so using that value does not extrapolate its Cp fit below 500 K. Its entropy expression returns absolute S(T). Hydrogen is also evaluated within its stated range. These equations and coefficients were independently checked against the [NIST water](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=1) and [hydrogen](https://webbook.nist.gov/cgi/cbook.cgi?ID=C1333740&Mask=1) pages.

Taylor's Table 8 image does give experimental toluene entropy 76.33 ± 0.25 cal/(mol K), at 298.16 K and 1 atm. The correction `S_1bar = S_1atm + R ln(1.01325)`, with the small temperature correction, gives **319.4707 J/(mol K)**. This is distinct from the adjacent calculated value, 76.42. The original [Taylor et al. paper](https://nvlpubs.nist.gov/nistpubs/jres/37/jresv37n2p95_A1b.pdf), printed p.102, was checked as an image.

Other inherited 1 atm/1 bar ambiguities remain disclosed in the inputs. Each unresolved species correction changes its Gibbs term by only about 0.0846 kJ/mol at 773 K. A consistent common pressure change cancels for the two zero-mole-change reactions; inconsistent species conventions do not exactly cancel. This is small for screening, but the ambiguity should be resolved before reporting precise equilibrium constants.

## 2. Independent numerical reconstruction

The Cp values were separately transcribed from [ethylbenzene](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100414&Mask=1), [benzene](https://webbook.nist.gov/cgi/cbook.cgi?ID=C71432&Mask=1), [ethanol](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Mask=1), [toluene](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108883&Mask=1), and [methanol](https://webbook.nist.gov/cgi/cbook.cgi?ID=C67561&Mask=1). I integrated each linear interpolation segment with 10,000 midpoint panels and evaluated the independently transcribed water/H2 coefficients. Values below retain extra digits only to make the calculation auditable.

| Quantity at 773 K | Independent result | Assessment |
|---|---:|---|
| Benzene/ethanol ΔrH° | 56.9933 kJ/mol | Consistent |
| Benzene/ethanol ΔrS° | −5.67085 J/(mol K) | Consistent |
| Benzene/ethanol ΔrG° and K | 61.3769 kJ/mol; 7.12206 × 10−5 | Reported +61 and 7 × 10−5 are appropriate |
| Equal benzene/ethanol with **local** 4 ppm water | 1.84894 ppm each | Correct chemical-potential boundary |
| Product-free feed with **inlet** 4 ppm water | 1.47029 ppm each | Includes water depletion and exact EB depletion |
| Same inlet calculation at 1 and 10 ppm water | 0.59112 and 2.52695 ppm each | Consistent |
| Toluene/methanol ΔrG° and K | 56.4978 kJ/mol; 1.52159 × 10−4 | Reported +56 and 1.5 × 10−4 are appropriate |
| Ethanol at 1, 10, 100 ppm benzene, local 4 ppm water | 3.4186, 0.34186, 0.034186 ppm | Consistent |
| Methanol at 1, 10, 100 ppm toluene, local 4 ppm water | 7.3036, 0.73036, 0.073036 ppm | Consistent |
| Comparator-ratio aromatic concentrations | 71.071 ppm toluene; 6.5752 ppm benzene | Consistent |
| Comparator-ratio alcohol boundaries | 0.10277 ppm methanol; 0.51992 ppm ethanol | Consistent |

The exact finite-feed equation is `x² = K(0.012 − x)(y_water,in − x)`. Omitting EB depletion is harmless at these trace extents. The local 1.85 ppm boundary and inlet-balanced 1.47 ppm extent answer different questions; neither should replace the other.

The comparator mass percentages were checked against the locally retrieved MacroCat paper's Table 2: 99.22 wt% EB, 0.51 wt% toluene, and 0.04 wt% benzene. Their use is explicitly conditional; this company's comparator feed is not evidence of the necessary zirconia feed composition. [MacroCat industrial report](https://www.mdpi.com/2073-4344/15/4/308).

### Acetophenone

The adopted 298 K values reproduce `ΔrH° = 125.3264 kJ/mol`, `ΔrS° = 84.805 J/(mol K)`, and the unresolved expression `ΔrG°773 = 59.7721 + C kJ/mol`. The missing correction must remain explicit. The [NIST acetophenone page](https://webbook.nist.gov/cgi/cbook.cgi?ID=C98862&Mask=1) confirms the recorded formation enthalpy and entropy but supplies no gas Cp table.

Independent calculation gives:

```text
weight integral = 261.5734 K
C = 40.4582 − 0.2615734 × weighted_Cp_AP  [kJ/mol]
weighted_Cp_EB = 178.344 J/(mol K).
```

At 0.01, 0.1, 1, and 10 ppm acetophenone, the required weighted Cp values are **240.447, 297.023, 353.600, and 410.176 J/(mol K)**. These are correctly reported thresholds, not an estimated acetophenone Cp or a demonstrated impossibility. Lowering H2 from 12 to 1.2 kPa changes ΔrG by **−29.5978 kJ/mol**, and raises the conditional acetophenone concentration boundary 100-fold.

The parent review identified a [NOAA/CHRIS acetophenone table](https://cameochemicals.noaa.gov/chris/ACP.pdf), section 9.27, covering only approximately 272–400 K. That is a partial data lead; it does not fill the required range through 773 K. No extrapolation or absolute acetophenone K is justified here.

### Uncertainty and source-verification limit

The ±5 kJ/mol sensitivity multiplies/divides K by **2.1770**. The resulting comparator ranges are approximately 0.047–0.224 ppm methanol and 0.239–1.132 ppm ethanol. These are sensitivity cases, not statistical bounds. Missing Cp/entropy uncertainties, correlations, and mixed evaluations preclude a complete confidence interval.

Direct web-tool retrieval of CCCBDB repeatedly failed, but the author subsequently supplied fresh HTTP-200 HTML captures with URL/SHA-256 metadata. I checked those hashes and inspected the captured source content: [benzene entropy](https://cccbdb.nist.gov/exp2x.asp?casno=71432&charge=0), [ethanol H/S](https://cccbdb.nist.gov/exp2x.asp?casno=64175&charge=0), and [methanol H/S](https://cccbdb.nist.gov/exp2x.asp?casno=67561&charge=0) match the recorded values and reference assignments. The capture directory is `/tmp/styrene-oxygen-review/thermochemistry-source-captures`; preserve it through the designated literature workflow. This checks transcription from the databases, not the underlying Gurvich/TRC determinations or a complete common uncertainty model.

## 3. What the concentration boundaries do not establish

**A free-alcohol boundary is not a total oxygen-removal or cleaning-rate ceiling.** Further alcohol conversion changes the net reaction. For example, adding `CH3OH → CO + 2 H2` to the toluene route gives `EB + H2O → toluene + CO + 2 H2`. The full reaction has its own Q and equilibrium constant. A high forward flux through a low-concentration intermediate is possible; its concentration alone does not measure oxygen throughput.

Alcohol adsorption is a finite sink until the adsorbed inventory stops increasing or a removal/regeneration process closes the balance. Persistent adsorption or solid oxygen/carbon uptake cannot support an unqualified claim of sustained catalytic export. Conversely, a cold analytical trap downstream of a once-through hot bed does not impose its low product activity upstream.

**Sustained cleaning need not export the entire inlet water flux.** Some water can leave unreacted while the active-site population remains stationary. Comparing 0.10 or 0.52 ppm terminal alcohol to a 4 ppm inlet water feed can reject a proposed account in which most feed water leaves through that outlet. It cannot establish inadequate cleaning without measured inlet/outlet oxygen fluxes, retained inventories, and the working-site state. Convert concentrations to molar fluxes with the actual inlet and outlet flows; ppm is not itself a flux.

A finite prelabel experiment has different initial and final catalyst inventories. Its solid-state Gibbs contribution does not cancel, so its labelled-product pulse cannot establish or refute the sustained gas-cycle equilibrium. Isotope exchange can also produce labelled molecules at zero net product generation. Neither label transfer nor recovery alone establishes a forward closed-cycle flux.

## 4. Can the cofeeds distinguish thermodynamics from inhibition?

The proposed clean-feed controls, both-product perturbations, and product-sink tests are necessary and useful. Aromatic cofeed suppression alone remains non-diagnostic: adsorption on hydroxylated sites or changed intermediate coverages can selectively inhibit recovery while barely affecting a clean dry catalyst.

Add these requirements before claiming driving-force control:

1. **Establish a sustained baseline.** Feed independently measured water continuously and require stationary water breakthrough, oxygen/carbon inventories, and working-site capacity. Integrate enough oxygen throughput to exceed plausible accessible storage, with measured inventory bounds. A flat styrene rate alone is insufficient. Keep finite prelabel recovery as a separate experiment.
2. **Measure net species formation.** Use inlet/outlet molar balances for alcohol and aromatic products, alongside isotope signals and all other oxygen outlets. Account for water or other products generated by the cofeeds themselves.
3. **Measure the relevant local Q.** Trace-water conversion can be large despite low EB conversion. Use a sufficiently differential bed or constrain axial composition changes; an inlet-water value with outlet products is generally not one local reaction quotient.
4. **Use a two-product grid.** Vary aromatic and alcohol pressures independently, include equal-Q combinations, and seek reproducible net-flux zero crossings or reversal near the calculated boundary at a comparable stationary catalyst state. Approach from both directions and check recovery after washout. Equal-Q rate collapse is not required away from equilibrium, because kinetics can still depend separately on adsorption.
5. **Close the sink test.** Dose the authentic alcohol over the working catalyst at relevant exposure, measure its net conversion and retained oxygen/carbon, and distinguish a steady downstream product from temporary storage. Recompute the complete net reaction if a sink operates.

A zero crossing consistent with Q is stronger evidence than rate suppression, but a network of coupled reactions can shift it. Interpret it with the measured full reaction balance. The H2 perturbation is similarly informative only after separating styrene equilibrium, coverage changes, and alternative oxygen-product chemistry.

## 5. Decision for the research program

Retain this branch as a product-identification and feasibility gate within Aim 1, followed by a controlled product-consequence test in Aim 2. Explicitly separate direct inhibition, loss of cleaning driving force, and changed oxygen-product fate. Require stationary-inventory measurements before extending the result to sustained operation.

The branch improves the questions the campaign can answer and could prevent a mistaken product assignment or unnecessary purification hardware. It does not yet show that aromatic feed components limit useful operation, that alcohols are the actual cleaning products, or that zirconia offers a practical advantage over established catalysts. **The present evidence remains bounded screening; practical value depends on the proposed discrimination experiments.**

## Addendum: independent check of the early product-cofeed calculation

Date: 2026-09-15. Reviewed [cofeed inputs](../calculations/styrene_cofeed_inputs.json), [calculation](../calculations/styrene_cofeed.py), [output](../calculations/styrene_cofeed_output.json), and the proposed [early net-product gate](styrene-product-headroom.md). This addendum checks the new thermodynamic composition selection; it does not independently re-review every kinetic quotation in the gate note.

**The new equilibrium calculation is correct and supports selecting a small cofeed experiment before elaborate oxygen attribution. One planning correction is needed: a composition chosen at central η = 0.5 is not necessarily forward-favored across the stated sensitivity scenario.**

### Source and numerical check

I reopened the [NIST styrene gas page](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100425&Mask=1). Its selected values are correctly transcribed: Prosen/Rossini ΔfH°298 = 146.9 ± 1.0 kJ/mol; compiled Pitzer S°298 = 345.1 ± 2.1 J/(mol K); and the recommended Cp table from 298.15 through 800 K. The older alternative enthalpies are not equally reliable independent replicates to average with the selected value. The stated source selection and exclusion are appropriate for this screening calculation. The original thermochemical determinations and complete uncertainty model have not been newly evaluated here.

I independently integrated the separately transcribed styrene and EB Cp tables with 10,000 midpoint panels per linear segment, and separately evaluated hydrogen's Shomate expression. No shared integration function was used in this reconstruction. I also reran the supplied script; its JSON matches the stored output exactly.

| Temperature | Independent ΔrG°, kJ/mol | Independent dimensionless K |
|---|---:|---:|
| 723 K | 29.9382 | 0.00687220 |
| 773 K | 23.4617 | 0.0259795 |
| 800 K | 19.9556 | 0.0497806 |

At 773 K, ΔrH° = 123.7607 kJ/mol and ΔrS° = 129.7529 J/(mol K). All temperatures are inside the adopted Cp/Shomate ranges. These decimal digits show reproducibility, not thermochemical precision.

### Pressure convention and interpretation

For ideal gases and `E ⇌ S + H2`,

```text
Q = (p_S/p_E)(p_H2/p°)
η = Q/K
(S/E)_target = η_target K p°/p_H2.
```

The script correctly uses `p° = 100 kPa`, so it does not mix dimensional and dimensionless equilibrium constants. At 773 K and central `η = 0.5`, the result is **S/E = 0.10825 at 12 kPa H2**, or **H2 = 1.29898 kPa at S/E = 1**. The calculation specifies local gas compositions, not achievable reactor conversion. Total pressure need not enter separately once the actual H2 partial pressure and S/E ratio are specified.

These composition constraints follow from equilibrium without extrapolating a rate law. Inferring `r_net/r_forward = 1 − η`, an absolute rate, or unchanged working sites in an unmeasured cofeed still requires kinetic assumptions. A lower-H2 operating point can therefore be selected thermodynamically while its kinetic response remains an experimental question. The gate should judge directly measured net output and reversible/persistent changes, as proposed.

### Required planning qualification

The declared ±5 kJ/mol sensitivity changes K773 by a factor **2.1770**, giving **0.0119335–0.0565580**. Holding a composition chosen for central `η = 0.5` fixed gives **η = 0.2297–1.0885** across that scenario. Thus such a point does not satisfy the gate's intended appreciable forward-driving-force criterion throughout the sensitivity range; a small or negative net rate there could still have a thermodynamic explanation.

If the entire stated sensitivity scenario is retained as the planning margin, selecting from its lower K endpoint gives `η ≤ 0.5` throughout that scenario:

- At 12 kPa H2: **S/E ≤ 0.04972**.
- At S/E = 1: **H2 ≤ 0.59668 kPa**.

These are sensitivity-based design margins, **not confidence-qualified safe boundaries**. The alternative is a better constrained consistent K(T) or an independently established equilibrium boundary before assigning a kinetic failure. Composition uncertainty and reactor gradients also need margin. The approximately 0.60 kPa H2 option is outside the focal paper's quoted forward kinetic range; do not predict its cleaning, selectivity, or durability from the earlier rate laws.

No arithmetic or coding fix is required for the stated inputs. Carry the sensitivity through to the selected cofeed pressures and keep nominal and conservative scenarios distinct. With that qualification, the early gate strengthens experimental ordering and can reject an unproductive operating window efficiently. It remains a local chemical continuation test, not a process-performance prediction.
