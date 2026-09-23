# A water specification must include the hydrocarbon feed

2026-09-15. Design calculation for the [zirconia oxygen-fate program](../programs/zirconia-styrene-oxygen-fate.md). This is algebra from the published two-state cleaning model, not a new mechanism or fitted prediction. Source: Artsiusheuski et al., [supporting information](https://doi.org/10.1021/acscatal.5c04904.s001), p.10–13. An [independent algebra and design review](../reviews/styrene-independent-review.md) supports the derivation under its stated assumptions.

## Decision

Report water in three ways: molar flux, total-gas mole fraction, and water/ethylbenzene molar ratio. Determine how much comes from the liquid feed, carrier gas and apparatus. A total-gas ppm limit from a dilute kinetic experiment is not a general liquid-feed purity specification.

An additional small feed-scaling experiment can test the published model's transferability before an integral reactor or recycle experiment. It cannot identify the cleaning products; the oxygen-fate measurement remains necessary.

## 1. Local model and consistent units

Let θ be the fraction of competent pairs free of the water titrant. For fixed local concentrations and one inactive population:

```text
dθ/dt = kc cE (1 − θ) − kw cw θ
θss = kc cE / (kc cE + kw cw)
λ = kc cE + kw cw
θ(t) = θss + (θ0 − θss) exp(−λ t)
```

Here cE and cw have units mol/volume, kc and kw have units volume/(mol·time), and λ has units 1/time. Constants are defined on this consistent local basis rather than copied from the SI's printed unit labels. No bed-density factor belongs in this single-site population equation. Site heterogeneity, another poison, product inhibition, structural evolution and oxygen exchange can invalidate its interpretation.

The steady population depends on `(kw/kc)(cw/cE)`. If water enters only with ethylbenzene at a fixed molar ratio β, then `cw = β cE`: raising both concentrations leaves θss unchanged in this model and increases λ. If water instead stays fixed while cE rises, θss increases. Neither result establishes behavior beyond the tested kinetic regime.

For gas mole fractions, a simple source bookkeeping expression is `yw = β yE + γ ycarrier + Japparatus/Ftotal`. The coefficients and apparatus flux must be measured, not assumed constant across vaporizer temperatures or flow changes. Water and ethylbenzene can partition differently during evaporation, drying and storage. A nominal liquid composition is not automatically the delivered vapor composition.

**Conditional conversion example:** at 1.2 mol% ethylbenzene, 4 ppm water in the total gas is 333 μmol water/mol ethylbenzene. If all that water accompanied ethylbenzene, it would correspond to about 57 mg water/kg ethylbenzene. At the same impurity ratio and 80 mol% ethylbenzene, total-gas water would be about 267 ppm. These are arithmetic translations, not measured liquid specifications or a prediction of useful zirconia activity at concentrated feed. Likewise, 1 ppm total gas in the dilute example is about 14 mg/kg on the all-feed-derived assumption.

Constant θss also does not imply constant lifetime: faster repeated poisoning/cleaning can generate more X per unit time, increasing exposure to an irreversible side route. Time and cumulative oxygen dose are separate comparison axes.

## 2. A low-conversion reactor can still have a large water gradient

The published SI already includes axial water depletion. It must not be rediscovered as new chemistry or omitted when interpreting a reactor-average transient.

For an isothermal steady plug-flow bed, constant volumetric flow Q, constant cE, site density ns (mol pairs/mass), and catalyst mass coordinate W:

```text
dFw/dW = −ns kw cw θss
Fw = Q cw
ln(cw,out/cw,in) + [kw/(kc cE)] (cw,out − cw,in)
    = −ns kw W/Q
```

Both sides are dimensionless. This follows by substituting θss and integrating `(1/cw + kw/(kc cE)) dcw = −ns kw dW/Q`. It assumes no water generation/desorption route, unchanged sites, negligible cleaning consumption of E, and the same one-water event basis used by the local model. The limiting case of almost all sites free reduces to ordinary first-order water removal. At fixed W/Q, scaling inlet water and ethylbenzene together preserves the normalized steady water and site profiles in this model. Changing pressure at fixed molar flow changes Q, so equal inlet ratios alone do not ensure equal bed-average coverage.

Low ethylbenzene conversion alone does not make cw uniform. A bed can barely consume the major reactant while removing most of a ppm impurity. Upstream/downstream differences in θ then produce a global transient that is not a single exponential. A λ fitted to the total styrene rate cannot automatically be used to calculate elementary poisoning and cleaning constants.

## 3. Smallest useful experimental contrast

1. Measure water upstream and downstream in the actual organic/H2/carrier matrix. Run feed-source blanks and verify that sample lines do not dry the sample. Use both pretreatment histories only after their direct initial-rate difference is reproducible.
2. At one temperature and fixed H2/product conditions, use a small 2 × 2 matrix within the verified kinetic range: `(e,w)`, `(αe,w)`, `(e,αw)`, `(αe,αw)`. Hold total pressure and volumetric flow fixed by replacing inert; choose α from the accessible range. The diagonal tests equal-ratio scaling; off-diagonals separate each input. Reserve an additional composition or residence time for prediction without refitting.
3. Establish θ-related activity with matched dry-feed normalization at each composition; do not assume that raw rates at different cE have the same per-free-site value. Account for affinity and inhibition. Confirm that the normalization itself does not reset the state being measured; use separate matched specimens where needed.
4. Vary catalyst inventory/flow enough to detect water gradients, while checking transport and maintaining an informative time response. Prefer a nearly uniform water concentration if measurable. Otherwise fit the distributed model to measured inlet/outlet water and activity and test an unfit residence-time condition.
5. Record transient shape, stationary rate and water flux, not only a fitted λ. Pooling all data into one apparent constant can hide either exchange/storage or a moving poisoning front.

If θss and λ are independently identifiable in a uniform local experiment, `kc = λ θss/cE` and `kw = λ(1−θss)/cw`. Those expressions do not create independent observables: the same uncertain rate normalization may affect both estimates. Near θss = 0 or 1, one inferred term is poorly constrained. A measured water flux and independent site-capacity constraint are therefore valuable.

## 4. Decision value and limits

- A successful held-out prediction supports a **composition-specific** operating model, not harmlessness of X or proof of an elementary step.
- A failure localized to product-rich conditions directs the next experiment toward product inhibition or changed cleaning chemistry.
- A failure caused by apparatus moisture or axial capture directs work toward feed control and reaction engineering before catalyst synthesis.
- No result here by itself establishes a process energy benefit. Increasing hydrocarbon concentration also changes equilibrium approach, heat transport and product exposure.

The contribution sought is a useful validated purity/working-state relationship tied to a measured oxygen fate. Routine confirmation of this existing model, by itself, would be too small to justify the broader research program.

## 5. Trace relative to total gas can be significant relative to product

For stationary operation with water as the only external oxygen source, define f as the fraction of incoming water oxygen exported through an identified cleaning route, and ν as the number of ethylbenzene equivalents diverted from styrene per oxygen atom exported. At negligible gas expansion, the fraction of reacted ethylbenzene assigned to that route is

```text
cleaning diversion / total reacted EB = ν f yw/(yE X) = ν f β/X,
```

where X is total EB conversion and β = yw/yE. This is an accounting relation, not a reaction-rate model. Use actual molar inlet/outlet flows if expansion matters. f is not known from a flat styrene rate or an inferred inlet moisture concentration. A route producing two oxygen products per EB has a different ν from one yielding a single oxygenated C8 product; the balanced net chemistry determines it. Persistent consumption of lattice oxygen, deposits, or other incoming oxygen compounds invalidates the simple water-only bound.

**Illustration, not a reported yield loss:** yE = 0.012, yw = 4 ppm, ν = 1 and f = 1 give:

| Total EB conversion | Reacted EB per total inlet gas | Maximum assigned diversion under these assumptions |
|---|---:|---:|
| 0.5% | 60 ppm | 6.7% |
| 1% | 120 ppm | 3.3% |
| 2% | 240 ppm | 1.7% |

If only one tenth of inlet water follows the route, the entries are one tenth as large. Conversely, an oxygenated product derived from a stored activation reagent would not be a sustained EB diversion. Carbon-origin and net-flux measurements are therefore needed before applying this estimate.

These numbers do not amend the paper's reported selectivity. They combine a stated hypothetical route with a representative dilute composition and conversion range; the actual cleaning flux, conditions and denominator must be measured together. In particular, the source's approximately 10 ppm X estimate is not a product measurement. Count identified oxygenated branches explicitly in target-styrene yield rather than silently equating a dehydrogenation/C–C-cleavage ratio with every possible outlet.

Reconcile whole reaction events and carbon atoms before adding a penalty: benzene or toluene from a cleavage cleaning route may already belong to the measured C–C-scission channel. An oxygenated intermediate that subsequently yields styrene is a per-pass diversion, not necessarily a final yield loss. Report actual net styrene formation, other product carbon and retained carbon, with uncertainty relative to reacted EB and net styrene. An equilibrium-corrected forward dehydrogenation rate is not the product-output denominator.

The bound `0 <= f <= 1` applies to net export of external water oxygen under stationary inventories. Gross cleaning turnovers can exceed fresh oxygen input if products regenerate water. During recovery, initially stored hydroxyl or lattice oxygen must enter the inventory balance; the stationary inlet-water-only bound does not apply. A route-specific bound also requires checking other oxygen inputs and changes in stored oxygen.

At fixed β, the direct sacrifice decreases with increasing X. For β = 4 ppm/0.012 and X = 0.5, the same ν = f = 1 bound is approximately 0.067% of reacted EB. This does not predict feasible 50% conversion on zirconia. It explains why a detectable selectivity correction in a differential experiment need not imply a large practical carbon loss. Persistent poisoning, product quality, heat transfer and separation can remain consequential even when the stoichiometric sacrifice is small.
