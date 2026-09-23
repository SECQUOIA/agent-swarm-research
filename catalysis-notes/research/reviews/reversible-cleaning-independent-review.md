# Independent review: reversible cleaning cycle

Date: 2026-09-15. Scope: independent algebra and experimental-inference audit of the [two-state calculation](../calculations/reversible-cleaning-cycle.md), checked against the minimal pilot and cofeed sections of the [research program](../programs/zirconia-styrene-oxygen-fate.md). No additional literature or fitted predictions were needed.

## Verdict

**The derivation is correct within its stated two-state, one-water, fixed-local-activity model.** Its strongest new result is a conditional rejection criterion: complete matched product cofeeds cause at least as much steady free-pair loss in dry operation as in wet operation when B and C are unchanged. Wet-only suppression is not a generic signature of reverse cleaning.

This supports tightening the interpretation of later cofeed experiments. It does not justify enlarging the first pilot or requiring an independent active-pair census before product discovery. The current revision explicitly acknowledges that such a census is unvalidated; keep every occupancy-based discrimination conditional on validating it, or on separately establishing the activity-to-occupancy relation.

## Checks

| Item | Independent result |
|---|---|
| Dimensions | With dimensionless gas activities, A–D and all four k values have units s−1. θ is dimensionless and j is events per pair per second. Multiplication by **moles of pairs** gives mol s−1; multiplication by a count of pairs gives events s−1 and requires division by Avogadro's constant. Clarify the calculation's current “number of pairs” wording. |
| Detailed balance | Water equilibrium gives `(1−θ)/θ = Ka aW`; cleaning equilibrium gives `θ ΠX/[(1−θ)aE] = Kc`. Their product is `Kgas`, and `AC/(BD) = Kgas/Qgas` when the denominators are nonzero. A finite equilibrium constant is incompatible with deleting only a reverse elementary frequency while retaining the other finite constants. |
| Occupancy and flux | Direct substitution gives `θss=(B+C)/Λ` and `jss=(AC−BD)/Λ`. At fixed A and B, `jss=(A+B)θss−B`. At equilibrium, `AC=BD` and `θss=B/(A+B)`. The quotient-factorized flux expression is only defined at positive reactant activities; use `(AC−BD)/Λ` in the exactly dry limit. |
| Dry/wet inequality | For `ΔD>0`, fractional loss is `ΔD/(A+B+C+D1)` and decreases with A. Absolute loss is `(B+C)ΔD/[(A+B+C+D0)(A+B+C+D1)]` and also decreases with A. Both conclusions require matched B, C, D0 and D1. |
| Initial slopes | At θ=1, `θdot=−(A+D)`, reducing to −D for A=0. At θ=0, `θdot=B+C`. A D step changes slope by `−ΔD θ`; thus reverse return alone cannot immediately suppress recovery from θ=0. For a partly recovered specimen it can. |

“Dry” must mean negligible **local** water activity for the exact A=0 result. Water formed during reverse cleaning can make a dry-inlet experiment locally wet. More generally, the inequality still compares two known A values if the other frequencies remain matched.

## Identifiability: the warning is substantive

An informative calibrated θ transient identifies `u=A+D` and `v=B+C`. Even knowing `r=Kgas/Qgas>0` leaves a continuum of positive solutions. For any `0<b<v`, set

```text
B=b, C=v−b,
A=rbu/[v+(r−1)b], D=u−A.
```

Every member has the same θ transient and satisfies `AC/(BD)=r`. A specimen already at its steady occupancy supplies even less transient information. Flux measurements and controlled activity changes add information, but a zero net flux at equilibrium does not by itself remove this ambiguity. No claim of four separately measured constants is warranted from occupancy fitting alone.

## Counterexamples and experimental limits

1. **Incomplete coproducts defeat the dry/wet comparison.** With benzene cofed but alcohol generated only during wet recovery, D can be negligible in dry operation and substantial in wet operation. Matching benzene pressure alone does not test the inequality. Matching inlet pressures also fails if conversion creates different local product activities.

2. **Forward-cleaning inhibition produces wet-only loss without reverse return.** At negligible D, decreasing C leaves the dry steady occupancy at one but lowers wet occupancy. This is already a sufficient alternative within the existing terms; a new surface state is unnecessary to explain that contrast.

3. **Function is not a census.** An immediate activity drop could reflect intrinsic inhibition, changing occupancy, or both. Water uptake and rate loss cannot independently establish unchanged pair inventory when they share the model being tested. Initial-slope tests also require adequate switching resolution and a validated common functional assay; EB can clean the specimen during that assay.

4. **Reverse net flux is stronger evidence, but not unique site attribution.** A parallel reversible reaction on another surface population could consume the complete products and produce EB/water near the same gas equilibrium boundary, while generic inhibition independently reduces dehydrogenation. That reproduces reverse stoichiometry without proving return through the functional pairs. Label transfer alone is weaker still because exchange can reproduce it. Require net balances, bounded storage, complete local activities and a credible full-route equilibrium constant; retain ambiguity when those are unavailable.

An optional consistency check avoids counting pairs: if independently validated kinetics give `F*=rnet/(1−η)=N kcat aE θ`, stationary net water uptake obeys

```text
Jwater = [(A+B)/(kcat aE)] F* − NB.
```

Here N is moles of pairs and the comparison holds A, B, N, kcat and aE fixed. This predicts linear covariation across steady product cofeeds. It tests the shared water/functional-state assumptions, **not reverse cleaning specifically**: changing C alone also obeys it. Avoid using it near dehydrogenation equilibrium or when the net water difference is unresolved. It should remain an optional later check, not a new pilot gate.

## Recommendation

Retain the small water/sham × EB/no-EB pilot and its assay-validity gate. Add the conditional dry/wet rejection criterion to later, identified-product cofeed work. Make the molar-flux normalization and exactly dry quotient limit explicit. Present net-flux reversal as evidence for a reversible net route, with separate evidence still needed to assign that route to recovery of functional pairs. No numerical operating prediction or larger experimental matrix follows from this unfitted derivation.
