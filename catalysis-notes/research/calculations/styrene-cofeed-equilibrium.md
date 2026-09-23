# Choose a cofeed that can make net styrene

2026-09-15. Screening calculation supporting the [early product-cofeed gate](../reviews/styrene-product-headroom.md). These are thermodynamic design boundaries, not measured rates or predicted process performance. A [fresh independent review](../reviews/styrene-thermodynamics-independent-review.md) checked source selections, reproduced the integrations independently at all three temperatures, and verified the saved output. Its required affinity-margin correction is included below.

## Decision

At 773 K, the selected ideal-gas thermochemistry gives dimensionless `K ≈ 0.026` for ethylbenzene → styrene + H2, with a 1 bar standard pressure. At the reference H2 pressure of 12 kPa, a styrene/ethylbenzene ratio of one would favor hydrogenation. Such a test cannot reject zirconia for failing to make net styrene.

For a proposed cofeed with appreciable forward driving force, define `η = Q/K` and choose a target such as 0.5. This target is an experimental design choice, not an optimum. Since

```text
Q = (pS/pE) (pH2/p°),
pS/pE at target η = η K p°/pH2,
```

the calculated conditions are:

| Temperature | K, dimensionless | S/E at η = 0.5, H2 = 12 kPa | H2 at η = 0.5, S/E = 1 |
|---|---:|---:|---:|
| 723 K | 0.0069 | 0.029 | 0.34 kPa |
| 773 K | 0.026 | 0.11 | 1.3 kPa |
| 800 K | 0.050 | 0.21 | 2.5 kPa |

Reducing H2 makes a product-rich cofeed thermodynamically interpretable at the same temperature. It does not establish that the catalyst keeps the same activity, cleaning chemistry or durability at that lower H2 pressure. Much of the resulting H2 range lies below the published forward-rate pressure study; it must be measured. Alternatively, choose a lower S/E ratio with its narrower practical meaning. Do not silently turn a required lower H2 chemical potential into a free separation benefit.

## Data and calculation

The [NIST styrene entry](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100425&Mask=1) supplies the selected 298 K formation enthalpy (Prosen and Rossini, 1945), entropy (Pitzer, 1946, as compiled) and recommended gas heat capacities (TRC, 1997). The page also lists strongly discrepant historical formation enthalpies; they are not combined. Ethylbenzene and H2 use the previously documented [base inputs](styrene_thermochemistry_inputs.json).

The calculation integrates tabulated organic Cp and Cp/T from 298.15 K with piecewise-linear interpolation, and uses the in-range H2 Shomate relation. The reaction is atom-balanced and the elemental reference terms cancel. At 773 K the selected data give approximately ΔH = 124 kJ/mol, ΔS = 130 J/(mol K), and ΔG = 23.5 kJ/mol. Values should not be replaced by a rounded room-temperature reaction enthalpy/entropy carried unchanged to reaction temperature.

Reproduce offline with `python research/calculations/styrene_cofeed.py`. [Inputs](styrene_cofeed_inputs.json), [script](styrene_cofeed.py), and [output](styrene_cofeed_output.json) preserve selections and input hashes. The script reuses the reviewed integration function rather than maintaining a second numerical implementation.

## Uncertainty and boundary of inference

The selected sources do not supply a complete common uncertainty model or Cp/enthalpy covariance. Reference-entropy pressure conventions also retain the small unresolved 1 atm/1 bar ambiguity documented in the base calculation. The numbers are screening estimates, not certified equilibrium constants.

For an explicitly assumed ±5 kJ/mol change in ΔG at 773 K, K changes by a factor of about 2.2; the corresponding H2 threshold at S/E = 1 and η = 0.5 spans about 0.60–2.8 kPa. This is a sensitivity scenario, **not a confidence interval**. A feed set to η = 0.5 using the central K would span approximately η = 0.23–1.09 over that scenario: one end actually favors hydrogenation. The central table therefore cannot alone establish a safe forward-affinity margin.

If the whole stated scenario is retained as a planning margin, choose composition from its lower K: at 773 K, η no greater than 0.5 would require S/E no greater than about 0.050 at 12 kPa H2, or H2 no greater than about 0.60 kPa at S/E = 1. These remain scenario-based limits, not certified confidence bounds. Actual cofeeds should allow measured composition/thermochemistry uncertainty and report its effect on η. The calculation supports avoiding an obviously hydrogenation-favored test at the 12 kPa H2 reference; it does not validate a precise operating optimum.

Equilibrium alone does not quantify inhibition or persistence of active pairs. Direct net styrene production and return-to-reference behavior remain the required observations. Coupled reactions and changes in working state require their own carbon/oxygen balances. A loss near equilibrium must not be divided by a nearly zero affinity factor and presented as a precise intrinsic rate.

## Net-output precision can determine the usable cofeed

For inlet ratio `ρ = FS,in/FE,in`, actual net EB conversion X and molar net styrene yield per reacted EB s, the fractional styrene increase above its feed is `ΔFS/FS,in = s X/ρ`. This follows from molar flow accounting; it assumes neither the published forward-rate law nor a value of s. Use only when net EB consumption is positive and the reported yield basis is explicit.

For illustration, at ρ = 1, s near one, and X = 0.5–2%, the styrene increment is only 0.5–2% of fed styrene. Independent inlet/outlet uncertainties of 1% each would give about 1.4% uncertainty in the difference on the inlet-flow basis, using the same uncertainty convention. That could obscure much or all of the proposed net production. These are assumed precision and conversion values, not an instrument specification or a prediction for the cofeed.

Commission the paired flow/composition measurement, including correlation, tracer recovery and switching memory. Lower S/E or a larger resolved conversion may improve the difference measurement, but changes the tested operating window or creates stronger bed gradients. A high outlet styrene signal is not a substitute for a resolved increment. If no useful net difference can be measured at the selected cofeed, report that limitation before assigning a catalyst-performance verdict.

## Forward branching does not fix net selectivity

For a local model with only reversible EB/styrene interconversion and irreversible EB cleavage, let `R = rforward/rC–C`, counting each cleaved EB **once**. If `rnet = rforward(1−η)` remains valid and `0 <= η < 1`, then

```text
Snet = rnet/(rnet + rC–C) = R(1−η)/[1 + R(1−η)],
R required for target Snet = Snet/[(1−Snet)(1−η)].
```

For example, 95% net selectivity requires R at least 38 at η = 0.5, or at least 190 at η = 0.9. These are independently checked algebraic requirements, not catalyst predictions. The source's statement that a forward dehydrogenation/cleavage ratio exceeds 25 does not establish whether either requirement is met.

Use rates at the same feed and working state. Counting both products of one cleavage event would double-count EB consumption. Cofed styrene must be subtracted from outlet styrene, and additional cleaning branches or styrene side reactions require an expanded balance. The expression describes a local rate selectivity; a bed with changing composition needs integrated balances. Its value is to interpret the existing cofeed measurements, without adding another experimental campaign.
