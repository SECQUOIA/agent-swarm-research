# Thermodynamic screen of sustained ethylbenzene-assisted oxygen export

Date: 2026-09-15. Bounded challenge to the [oxygen-fate program](../programs/zirconia-styrene-oxygen-fate.md). This screen examines three balanced candidate routes; none is an assigned product pathway in the focal paper.

## Conclusions

**Gas-cycle thermodynamics can constrain product assignments, but it does not yet exclude oxygen export as a whole.** For ethylbenzene + water → benzene + ethanol, evaluated gas data give a screening standard reaction Gibbs energy near **+61 kJ/mol at 773 K**. Dilution nevertheless allows approximately ppm products at the proposed feed composition. Benzene pressure provides a direct test of this route’s sustainable export capacity. The analogous toluene/methanol route gives approximately +56 kJ/mol. Aromatic coproducts can therefore limit oxygen removal through these routes even if they do not directly poison clean active pairs.

The acetophenone + 2 H2 route faces a substantial hydrogen-pressure constraint. Complete gas heat-capacity data for acetophenone were not recovered, so no absolute 773 K equilibrium constant is assigned. Instead, the calculation below specifies how large its missing heat-capacity contribution would have to be to permit a claimed output. Lowering H2 from 12 to 1.2 kPa changes that route's reaction Gibbs energy by **−29.6 kJ/mol**, at otherwise fixed partial pressures. This is a substantial, known perturbation independent of the missing absolute thermochemistry.

**An alcohol equilibrium ceiling is not a ceiling on total cleaning flux.** If kinetically accessible, `CH3OH → CO + 2 H2` or `C2H5OH → CH3CHO + H2` consumes the alcohol and changes the net oxygen-export reaction. Both are balanced possibilities, not demonstrated steps on this catalyst. Measure all oxygen exits, including CO and carbonyls, and calculate Q for the identified complete net reaction. The low free-alcohol limits below apply only when the alcohol is the terminal oxygen product.

These tests concern sustained, closed catalytic cycles. A finite prelabel experiment changes the solid inventory; it cannot be evaluated solely from a gas-phase overall reaction.

## 1. Conditions and calculation basis

Use ideal gases at 773 K, standard pressure 1 bar, ethylbenzene partial pressure 1.2 kPa, and H2 partial pressure 12 kPa. The illustrative total pressure is 100 kPa, so 4 ppm water means 0.0004 kPa, or activity 4 × 10−6. Real calculations must use **local measured water and product partial pressures**. An inlet water level is an upper bound on local water in a consuming bed, not proof of uniform concentration.

For a net reaction, `ΔrG = ΔrG° + RT ln Q`, with dimensionless gas activities `ai = pi/(1 bar)`. At 773 K, `RT = 6.43 kJ/mol`, and a factor of ten in Q changes ΔrG by 14.8 kJ/mol.

For the numerical ethanol route, gas enthalpies and entropies at 298.15 K were combined with temperature-dependent ideal-gas heat capacities. Organic Cp values were interpolated linearly between the tabulated temperatures; each segment was integrated analytically as `Cp = a + bT`, giving `ΔH = aΔT + bΔ(T²)/2` and `ΔS = a ln(T2/T1) + bΔT`. Water's NIST Shomate expression supplies H(773) − H(298.15) and S(773) directly within its stated 500–1700 K range; it was not extrapolated to 298 K.

### Input data and provenance

| Species | Gas ΔfH°298, kJ/mol | Gas S°298, J/(mol K) | Temperature-dependent data used |
|---|---:|---:|---|
| Ethylbenzene | 29.8 | 360.6 | NIST WebBook recommended Cp table through 800 K |
| Benzene | 82.93 | 269.30 | NIST WebBook recommended Cp table through 800 K |
| Ethanol | −234.80 | 281.62 | NIST WebBook recommended Cp table through 800 K |
| Water | −241.8264 | 188.835 | NIST Shomate H and S at 773 K |
| Hydrogen | 0 | 130.680 | NIST Shomate H and S at 773 K |
| Acetophenone | −86.7 | 372.88 | No Cp(T) adopted; retained as an explicit missing term |

Ethylbenzene values are the Prosen formation enthalpy and Miller entropy selected on the [NIST ethylbenzene page](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100414&Mask=1), not the old discrepant enthalpy entries on that page. Benzene enthalpy and Cp are from the [NIST benzene page](https://webbook.nist.gov/cgi/cbook.cgi?ID=C71432&Mask=1); its entropy is the TRC value in [NIST CCCBDB](https://cccbdb.nist.gov/exp2x.asp?casno=71432&charge=0). Ethanol enthalpy and entropy are the Gurvich values in [NIST CCCBDB](https://cccbdb.nist.gov/exp2x.asp?casno=64175&charge=0); Cp is the recommended table on the [NIST ethanol page](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Mask=1). Water and hydrogen use [NIST water data](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=1) and [NIST hydrogen data](https://webbook.nist.gov/cgi/cbook.cgi?ID=C1333740&Mask=1). The [NIST acetophenone entry](https://webbook.nist.gov/cgi/cbook.cgi?ID=C98862&Mask=1) provides gas formation enthalpy and entropy but no gas Cp table.

This is a screening calculation using evaluated reference data, not a new primary thermochemical determination. Report rounded ΔG and K: entropy/Cp uncertainties and correlations are not fully supplied, and the ethanol data combine two evaluations. A hypothetical ±5 kJ/mol sensitivity changes K by a factor of approximately 2.2; that is a sensitivity case, not an assigned confidence interval. Differences between 1 atm and 1 bar entropy conventions are small at the precision used here, but should be reconciled in any final high-precision calculation.

## 2. Route A: cleavage yielding benzene and ethanol

```text
C8H10(g) + H2O(g) ⇌ C6H6(g) + C2H6O(g)
Q = a_benzene a_ethanol / (a_EB a_water)
```

The calculation gives ΔrG°773 ≈ +61 kJ/mol and K ≈ 7 × 10−5. H2 does not occur in this net reaction, and the gas mole change is zero. These are thermodynamic statements, not assertions about kinetic H2 order or surface coverage.

At 1.2 kPa ethylbenzene and **local** water of 4 ppm total gas:

```text
y_benzene × y_ethanol ≈ K × 0.012 × 4×10−6
                       ≈ 3.4×10−12
```

If the two products have equal partial pressures, the boundary is approximately **1.85 ppm each**. Thus positive standard ΔG does not exclude ppm formation. If the feed initially contains no benzene or ethanol, and only this reaction consumes an inlet 4 ppm water, the appropriate balance is instead:

```text
x² = K × 0.012 × (4×10−6 − x)
```

It gives approximately **1.47 ppm of each product**, leaving approximately 2.53 ppm water. The equilibrium water conversion is roughly 37% for this restricted reaction system. This is an idealized upper extent in an uncoupled isothermal reactor, not a predicted catalyst yield. At inlet water of 1 or 10 ppm, the corresponding product amounts are approximately 0.59 or 2.53 ppm each under the same assumptions.

### A sharper experiment: vary benzene pressure

With local water held at 4 ppm, the corresponding ethanol boundaries are:

| Measured total benzene in gas | Approximate ethanol equilibrium boundary |
|---|---:|
| 1 ppm | 3.4 ppm |
| 10 ppm | 0.34 ppm |
| 100 ppm | 0.034 ppm |

The table uses specified local concentrations, not independently generated equimolar products. Lower local water lowers each boundary proportionally. Benzene already formed by ordinary ethylbenzene C–C cleavage also counts in Q; it cannot be assigned only to the cleaning route.

**Decisive consequence:** a claim that this isolated route continuously exports most of a 4 ppm incoming water load as ethanol becomes difficult to sustain when benzene is already at tens of ppm. Measure benzene, ethanol, and water together before assigning ethanol as a dominant terminal oxygen carrier. A controlled benzene cofeed can cross the predicted equilibrium region while leaving ethylbenzene, water, H2, flow, and temperature fixed. Quantify both site recovery and net ethanol formation; simple rate suppression can also reflect adsorption.

If ethanol rapidly converts to other products, it is an intermediate rather than the terminal outlet assumed in this balance. Include those products and recompute the net reaction. Likewise, a downstream cold trap improves analytical recovery but does not by itself lower ethanol partial pressure within an upstream once-through catalyst bed.

## 3. Route B: acetophenone plus hydrogen

```text
C8H10(g) + H2O(g) ⇌ C8H8O(g, acetophenone) + 2 H2(g)
Q = a_AP a_H2² / (a_EB a_water)
```

At 298.15 K, the adopted gas data give ΔrH° ≈ 125.3 kJ/mol and ΔrS° ≈ 84.8 J/(mol K). The 773 K reaction Gibbs energy must include the missing heat-capacity correction:

```text
ΔrG°773 = 59.8 kJ/mol + C
C = ∫[298.15→773] ΔCp(T) × (1 − 773/T) dT
```

The 59.8 kJ/mol term **is not** an estimate of ΔrG°773 obtained by neglecting Cp. It is the known reference-state part of an expression with an unresolved correction.

At 1.2 kPa ethylbenzene, 12 kPa H2, and local water of 4 ppm, sustaining a given acetophenone concentration through this isolated net reaction requires:

| Acetophenone in total gas | RT ln Q, kJ/mol | Required C for forward thermodynamic driving force |
|---|---:|---:|
| 0.01 ppm | −37.3 | Below approximately −22 kJ/mol |
| 0.1 ppm | −22.5 | Below approximately −37 kJ/mol |
| 1 ppm | −7.7 | Below approximately −52 kJ/mol |
| 10 ppm | +7.1 | Below approximately −67 kJ/mol |

These inequalities sharpen the missing-data requirement. Define a weighted mean Cp over 298.15–773 K using weight `(773/T − 1)`. The positive weight integral is 261.6 K. Integrating the available ethylbenzene, water, and H2 data gives:

```text
C ≈ 40.5 kJ/mol − 0.2616 × weighted_Cp_AP
```

Here `weighted_Cp_AP` is in J/(mol K). The thresholds above require acetophenone weighted Cp of approximately **240, 297, 354, or 410 J/(mol K)**, respectively. For comparison, the same weighted integral of the measured/evaluated ethylbenzene Cp table is approximately 178 J/(mol K). This comparison does not supply acetophenone Cp or prove exclusion. It identifies the specific, large missing thermal correction needed for a ppm-scale assignment. Obtain validated gas Cp(T) or thermodynamic functions before claiming that acetophenone is a sustainable major outlet under the high-H2 condition.

### Hydrogen perturbation

For the same net reaction, reducing H2 from 12 to 1.2 kPa decreases Q by 100 and ΔrG by 29.6 kJ/mol. Its equilibrium acetophenone ceiling rises 100-fold at fixed ethylbenzene and water. By contrast, route A has no direct H2 term in Q.

Run paired conditions with partial pressures, water dose, temperature, and total flow controlled, while independently following styrene/H2 equilibrium effects, site inventory, and oxygen outlets. A reversible shift in acetophenone net formation toward the pressure-predicted boundary is more informative than a change in styrene rate alone. No observed H2 effect does not exclude an acetophenone route operating far from its equilibrium limit; a measured H2 order is not automatically its stoichiometric coefficient.

## 4. Route C and the aromatic-feed constraint

```text
C8H10(g) + H2O(g) ⇌ C7H8(g, toluene) + CH4O(g, methanol)
Q = a_toluene a_methanol / (a_EB a_water)
```

The same heat-capacity integration gives ΔrG°773 ≈ **+56 kJ/mol**, K ≈ **1.5 × 10−4**. Additional adopted gas inputs are toluene ΔfH°298 = 50.00 kJ/mol and methanol ΔfH°298 = −201.00 kJ/mol, S°298 = 239.87 J/(mol K). The enthalpy/Cp sources are [NIST toluene](https://webbook.nist.gov/cgi/cbook.cgi?ID=C108883&Mask=1) and [NIST methanol](https://webbook.nist.gov/cgi/cbook.cgi?ID=C67561&Mask=1); methanol enthalpy/entropy use the Gurvich evaluation in [NIST CCCBDB](https://cccbdb.nist.gov/exp2x.asp?casno=67561&charge=0).

Neither inspected open toluene database entry supplied entropy. The primary [Taylor et al. 1946 NBS paper](https://nvlpubs.nist.gov/nistpubs/jres/37/jresv37n2p95_A1b.pdf), Table 8, printed p.102, gives experimental S°298.16 at 1 atm of 76.33 ± 0.25 cal/(mol K). The original table image was checked. Converting to joules, 1 bar, and 298.15 K gives approximately 319.47 J/(mol K). This older experimental entropy is explicitly used here; it is not presented as the latest recommended toluene entropy. Local review copies are `/tmp/styrene-oxygen-review/taylor1946.pdf` and `taylor1946.txt`; no literature-library entries were changed.

At 1.2 kPa ethylbenzene and local 4 ppm water, toluene concentrations of 1, 10, and 100 ppm imply methanol equilibrium boundaries of approximately **7.3, 0.73, and 0.073 ppm**, respectively. Specifying 1 ppm toluene and 7.3 ppm methanol is a local chemical-potential calculation, not a claim that a product-free 4 ppm-water feed can generate more than 4 ppm oxygen product. Actual inlet/outlet material balances apply separately.

### Conditional industrial-composition example

The [MacroCat-201S industrial report](https://www.mdpi.com/2073-4344/15/4/308), Table 2, p.4, lists a feed containing 99.22 wt% ethylbenzene, 0.51 wt% toluene, and 0.04 wt% benzene. **This is a comparator’s feed, not a proposed zirconia specification.** If only those aromatic-to-ethylbenzene molar ratios were retained in a dilute zirconia experiment, they would give:

```text
n_toluene/n_EB = (0.51/92.1384)/(99.22/106.165) ≈ 0.00592
n_benzene/n_EB = (0.04/78.1118)/(99.22/106.165) ≈ 0.000548
```

At 1.2 kPa ethylbenzene and 100 kPa total pressure, these ratios correspond to approximately 71 ppm toluene and 6.6 ppm benzene. At local 4 ppm water, the isolated-route boundaries become approximately **0.10 ppm methanol** and **0.52 ppm ethanol**. The ratio form is useful: `y_alcohol,eq = K × y_water/(n_aromatic/n_EB)`. At fixed aromatic/ethylbenzene ratio, simply increasing both aromatic and ethylbenzene pressures does not raise that alcohol/water ratio.

These conditional ceilings are much smaller than a 4 ppm incoming oxygen flux. This comparison tests whether most incoming water exits as these terminal alcohols; it does **not** establish whether their smaller export flux is sufficient to maintain the working sites. Unreacted water can leave the reactor while sites undergo repeated poisoning and recovery. At stationary solid/train inventories, measure net water consumption, all oxygen export, and independently accessible sites before calling an equilibrium ceiling a limit on useful cleaning capacity. They could rule out those two terminal alcohol outlets as the principal sustained cleaning route under such a feed, **if** the measured products persist, no additional oxygen outlet or coupled reaction intervenes, and thermochemical uncertainty leaves the conclusion intact. Alcohol dehydrogenation, dehydration, decomposition, or adsorption changes the full reaction system and invalidates a calculation that treats the alcohol as its sole terminal oxygen product. Identify all oxygen sinks before interpreting a missing alcohol.

### Source uncertainty and usable precision

The selected formation-enthalpy uncertainties reported by the sources are EB ±0.84, benzene ±0.50, ethanol ±0.50, toluene ±0.63, methanol ±0.60, and water approximately ±0.04 kJ/mol. Their independent root-sum-square contributions are approximately 1.1 kJ/mol for route A and 1.2 kJ/mol for route C, but independence and confidence conventions are not established. EB entropy is reported with ±0.5 J/(mol K); the older toluene entropy has ±1.05 J/(mol K). Several other entropy uncertainties, full Cp(T) uncertainties, correlations, and the effect of combining evaluations are missing. Consequently **a complete statistical uncertainty bound cannot honestly be assigned** from these pages.

Retain two significant figures only as calculation outputs, not measurement precision. A deliberately stated ±5 kJ/mol ΔG sensitivity expands the comparator example to approximately 0.05–0.22 ppm methanol and 0.24–1.1 ppm ethanol; these ranges are **sensitivity intervals, not confidence bounds**. The chemical-potential effect is large enough to justify the experiment, while any definitive exclusion requires a consistent evaluated thermodynamic set with uncertainty or an experimentally established reverse/forward equilibrium boundary.

### Separate direct inhibition from inhibited cleaning

Use a matched experimental matrix at fixed ethylbenzene, water, H2, temperature, and flow:

1. **Clean catalyst, dry feed:** vary toluene or benzene over the intended range and measure the immediate dehydrogenation rate, independently accessible sites, and washout. This estimates direct adsorption/inhibition on exposed pairs. Confirm that the aromatic cofeed brings no extra water or oxygenate.
2. **Known partially poisoned state:** repeat the same aromatic perturbation during recovery with measured water input, while following site recovery, net alcohol generation, and all oxygen outlets. Compare to the clean-catalyst response; a large loss of recovery with little effect on clean-site activity supports a cleaning-specific limitation but does not by itself prove thermodynamic control.
3. **Vary both products:** after identifying a candidate route, change its aromatic and alcohol product pressures independently. Where the reversible reaction is observable, seek a net-flux zero crossing or reversal associated with Q, using small enough doses to avoid a new surface state. Suppression should organize by the product of the two activities for the isolated route. Adsorption can mimic inhibition and must still be measured.
4. **Test the proposed product sink:** pass the candidate alcohol at its observed concentration over the working catalyst and measure conversion to other oxygen-containing products. A sink requires a revised full reaction balance; a downstream collection trap is not such an in-bed chemical sink.

The useful new branch is a **loss of cleaning driving force caused by ordinary aromatic feed components or recycled coproducts**, distinct from their direct poisoning of active pairs. It should remain conditional on actual product identity and a demonstrated reversible or near-equilibrium constraint.

## 5. What this can and cannot reject

For **sustained oxygen export**, combine water adsorption, reaction of the poisoned surface, and restoration of the same working catalyst state. Surface intermediates then cancel from the net thermodynamic cycle. Strong water binding cannot make an otherwise unfavorable closed gas cycle favorable merely by relabeling water as a surface hydroxyl.

For **finite prelabel recovery**, the initial and final catalyst states differ. The Gibbs energy of changing hydroxyl, lattice-oxygen, deposit, and site inventories remains in the balance. A labelled-product pulse neither proves sustained gas-cycle feasibility nor violates its equilibrium limit. Stored hydroxyls should not be called a source of available free energy without specifying those states.

Even in sustained operation, an unfavorable *isolated* route is not an absolute exclusion if it is chemically coupled to another favorable net transformation, including further conversion of the proposed oxygenate. Demonstrate that coupling, write the complete stoichiometry, and test its complete Q. Independent styrene production cannot simply be invoked as an unspecified energy source.

**Decision for the campaign:** retain benzene/ethanol and toluene/methanol as quantitatively testable candidates, add measured aromatic coproduct pressures to their feasibility gates, and require adequate acetophenone gas thermal data before assigning it a dominant steady outlet at 12 kPa H2. Prioritize product-pressure and H2 perturbations after the analytical recovery controls pass. None of these results selects aromatic hydroxylation: ethylphenol isomer-specific thermochemistry and product identification remain separate tasks.


## Reproduce the calculation offline

The [standalone Python calculation](../calculations/styrene_thermochemistry.py) reads [explicit inputs and source metadata](../calculations/styrene_thermochemistry_inputs.json) and produces [the preserved numerical output](../calculations/styrene_thermochemistry_output.json). It uses only the Python standard library and makes no network requests. All Cp tables, Shomate coefficients, formation enthalpies, entropies, evaluation choices, pressure conventions, and sensitivity assumptions are stored in the input file. The output includes its input SHA-256 digest and more decimal places than the source accuracy warrants so the arithmetic can be audited.

```sh
python research/calculations/styrene_thermochemistry.py --output research/calculations/styrene_thermochemistry_output.json
```

The script verifies elemental balance and refuses Cp/Shomate extrapolation. Its species `g_for_reaction_sums` uses formation enthalpy at 298 K plus sensible heat minus absolute TS; this is suitable for balanced reaction sums but is not a species Gibbs energy of formation at 773 K. The acetophenone branch deliberately returns a required missing-Cp correction rather than an equilibrium constant.
