# A reversible two-state cleaning cycle: constraints and discriminating observations

Date: 2026-09-15. Algebraic extension of the focal study's water-titration/cleaning model, not an assigned mechanism or a fit. The published model treats cleaning as irreversible and excludes further transformations of X. See [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]], main-text Scheme 1 and SI section 1.7, and the [thermodynamic screen](../reviews/styrene-cleaning-thermodynamics.md).

A [fresh independent review](../reviews/reversible-cleaning-independent-review.md) verified the algebra, supplied a constructive nonidentifiability example, and checked the limits of the proposed experimental inferences. This is a consistency test for the research plan, not a claim of a new general kinetic theorem.

## Main result

A product can reduce the working free-pair fraction through reverse cleaning without changing the intrinsic activity of a free pair. However, **under matched complete product activities, the simplest two-state cycle predicts at least as much steady inhibition in dry operation as in wet operation**. Strong suppression of wet recovery with little effect on a sufficiently long dry test is therefore not the generic signature of thermodynamic reversal. Missing reverse-reaction coproducts, short observations, or a change in forward cleaning kinetics can produce that contrast and must be distinguished.

## 1. Minimal reversible model and detailed balance

Let F be a free pair and P a poisoned pair containing one water equivalent relative to F. Let θ be the fraction F and 1−θ the fraction P. This stoichiometry is a bookkeeping hypothesis to test; the model does not identify hydroxyl structures or localize an isotope.

```text
Water uptake/release:   F + W ⇌ P
Chemical cleaning:     P + E ⇌ F + Σνi Xi
Net gas cycle:         W + E ⇌ Σνi Xi
```

W is water and E is ethylbenzene. Select one balanced one-water oxygen-export route. For benzene/ethanol, the product activity factor is `ΠX = a_benzene a_ethanol`; for acetophenone/H2 it is `ΠX = a_AP a_H2²`. Activities are dimensionless and use a common standard state. This model does not cover an arbitrary multi-water, lattice-oxygen, or deposit-forming route without changing its bookkeeping.

Define four transition frequencies, each in s−1:

```text
A = kads aW       water adsorption:      F → P
B = kdes         water desorption:      P → F
C = kclean aE    forward cleaning:      P → F
D = kreturn ΠX   reverse cleaning:      F → P
```

They are effective mass-action terms for this minimal cycle, not a claim that either arrow is an elementary reaction. Positive rate constants and ideal pair-state activities give:

```text
Ka = kads/kdes = (1−θeq)/(θeq aW)
Kc = kclean/kreturn = θeq ΠX / [(1−θeq) aE]
Kgas = Ka Kc = kads kclean / (kdes kreturn)
Qgas = ΠX/(aW aE)
AC/(BD) = Kgas/Qgas
```

The product of the two equilibrium constants must equal the independently specified gas-cycle equilibrium constant. Fitting four unconstrained constants would permit an unphysical steady cycle at gas equilibrium. Surface free energies cancel only when the cycle restores the same catalyst state. A finite specified Kgas requires positive finite kdes and kreturn together with positive finite forward constants. Setting thermal desorption kdes exactly to zero while retaining finite reverse cleaning breaks detailed balance for that finite-K cycle. Setting a rate constant to zero can only serve as a documented far-from-equilibrium approximation. D can still vanish in the limiting case of a missing gas coproduct without setting kreturn to zero.

## 2. Occupancy, oxygen export, and transients are different observables

Use per-pair net event rates:

```text
jW = Aθ − B(1−θ)                 net water uptake
jX = C(1−θ) − Dθ                 net oxygen export through cleaning
θdot = jX − jW
     = (B+C)(1−θ) − (A+D)θ
```

Multiply j by moles of pairs to obtain molar flux; multiplying by a count of pairs instead gives events per second. The equality between events and oxygen atoms uses the stated one-water stoichiometry. Gross labelled-product appearance can include exchange and is not automatically jX.

At fixed local gas activities, with `Λ = A+B+C+D`:

```text
θss = (B+C)/Λ
jss = jW,ss = jX,ss = (AC−BD)/Λ
    = (AC/Λ)[1 − Qgas/Kgas]
θ(t) = θss + [θ(0)−θss] exp(−Λt)
```

The sign of net oxygen export follows the gas-cycle driving force. At Qgas=Kgas, net flux is zero although forward/reverse exchange may continue; θss reduces to B/(A+B), the water adsorption equilibrium occupancy. Positive θ does not require positive jX: under a dry product cofeed, reverse cleaning can form P while desorption releases water.

The quotient-factorized expression assumes positive reactant activities. At exactly zero water activity, Qgas is undefined; use the finite unfactorized result `(AC−BD)/Λ`. Also distinguish dry inlet gas from dry local conditions: reverse cleaning can generate water in the bed and make A nonzero.

At any steady state with fixed A and B:

```text
jss = (A+B)θss − B
```

Near gas equilibrium, a large fractional change in a small net oxygen flux can accompany a modest occupancy change. Conversely, measuring θ alone does not measure gross cleaning or gross water uptake. At nonsteady conditions, their net difference changes the surface inventory: `jW − jX = d(1−θ)/dt`. These statements are local; a reactor outlet measurement needs the corresponding spatial balance.

## 3. Product cofeed: a useful rejection criterion

Hold A, B, and C fixed and change the **complete** product factor so D increases from D0 to D1. Write β=B+C. Then:

```text
θ1/θ0 = (A+β+D0)/(A+β+D1)
θ0−θ1 = β(D1−D0)/[(A+β+D0)(A+β+D1)]
```

Here θ0 and θ1 denote the two steady states. Increasing A makes the ratio closer to one and the absolute difference smaller. Thus, for identical B, C, D0, and D1:

- The fractional steady free-pair loss is greater in dry operation (A=0).
- The absolute steady free-pair loss is also greater in dry operation.
- The intrinsic catalytic rate per free pair may remain unchanged, but the number of free pairs still decreases.

If dehydrogenation rate is independently established to be proportional to θ under matched chemical affinity, its steady rate change follows the same inequality. A much larger wet-only effect rejects reverse return as the sole explanation **within these conditions and this model**. It does not reject all effects of product chemical potentials.

### Exact limits of this comparison

**Incomplete product cofeed.** Benzene alone cannot drive reverse benzene/ethanol cleaning when ethanol activity is negligible. A wet working catalyst may generate ethanol while a clean dry catalyst does not. Then the same benzene cofeed gives different D values, and the inequality above does not compare the experiments. Quantify or match both product activities, including internally generated alcohol. The same issue applies to any other multiproduct route.

**Short or unequal histories.** Starting with a fully free dry surface, `θdot(0)=−D`; the rate per remaining free pair is unchanged, but reverse poisoning begins immediately. A short observation can miss its accumulated effect. Starting from a fully poisoned surface, `θdot(0)=B+C`, independent of D: reverse return acts only after free pairs appear. More generally, the instantaneous effect of a D step on recovery slope is `−ΔD θ`. Suppression of the initial recovery slope near θ=0 requires something beyond reverse return alone, such as a change in C. Different starting occupancies and durations cannot be treated as the steady-state contrast.

**Changed forward cleaning kinetics.** A cofeed might reduce C by interfering with ethylbenzene reaction on P. With D negligible, a truly dry bed has θss=1 whatever C, whereas a wet bed has θss=(B+C)/(A+B+C) and loses free pairs as C falls. This can produce wet-only inhibition, but it is suppression of forward cleaning kinetics, not evidence by itself for an unfavorable net reaction quotient. It requires testing the existing C term's invariance rather than silently fitting a new product effect into D.

**Changed local feeds or additional states.** Product conversion, water generation, adsorption, gas gradients, and deposit formation can alter A–D or invalidate the two-state closure. Keep those alternatives in the measured mass balance. In particular, rapid alcohol conversion to CO or carbonyls changes the net cycle; an isolated alcohol equilibrium ceiling is not a limit on total cleaning flux.

## 4. Smallest discriminating experiment

After identifying a plausible oxygen outlet and establishing analytical recovery, compare dry operation and a measured water-perturbed history at matched local E/H2 and complete product activities, with water as the deliberate contrast. Measure dehydrogenation activity and net oxygen flux, including water, separately. Add an independent free-pair inventory only if a validated selective assay exists; water uptake correlated with rate is not such a census by itself. Without it, retain the model-conditional occupancy interpretation and do not claim that a prompt rate change demonstrates unchanged site inventory.

1. **Match the whole product factor.** For a proposed cleavage route, vary aromatic and alcohol partial pressures separately and together; an aromatic-only control is insufficient if the alcohol is present only during recovery. Correct dehydrogenation for its own approach to equilibrium.
2. **Resolve immediate and accumulated effects.** A prompt change in activity at unchanged independently measured pair inventory is inconsistent with occupancy-only reverse cleaning. A delayed loss of pairs with reverse-route water production is consistent with it, although additional states could mimic the pattern. Use matched start states and observe long enough to establish whether a plateau exists.
3. **Test the flux sign, not just rate suppression.** With complete gas activities measured, seek a zero crossing or reversal of net oxygen export near Qgas=Kgas for the identified full route. Track surface accumulation during transients. Ordinary competitive inhibition can suppress rates and even slow recovery; it need not produce the stoichiometric reverse oxygen/water flux. A slow reverse reaction may make this test inconclusive rather than negative.
4. **Apply the dry/wet inequality.** If the wet effect remains much stronger after complete product matching and adequate observation, abandon reverse return alone as its explanation. Check forward-cleaning inhibition or additional surface states before introducing them into a fitted model.

A labelled product can help distinguish reverse transfer from feed contamination or oxygen exchange, but its appearance is not a substitute for the net balance. These are falsification tests for a minimal model, not sufficient proof of a unique atomistic mechanism.

## 5. Identifiability and practical interpretation

A θ transient at one fixed composition identifies at most the combined frequencies A+D and B+C. It cannot separate water poisoning from reverse product return, or desorption from chemical cleaning. The gas equilibrium constraint adds a relation, but does not in general identify all four rates from occupancy alone. Independent water/oxygen flux and controlled activity changes provide distinct information.

An optional consistency check avoids claiming an independent pair census. If validated dehydrogenation kinetics give `F* = rnet/(1−ηdehyd) = N kcat aE θ`, with N in mol pairs, then the steady water balance requires `Jwater = [(A+B)/(kcat aE)] F* − N B` across product cofeeds at fixed A, B, N, kcat and aE. Thus water flux and the inferred forward rate lie on a line within those assumptions. This follows from water uptake closure and holds whether C or D changes; it cannot diagnose reverse cleaning or independently validate θ. Nonlinearity rejects at least one shared assumption. Use it only where the existing measurements resolve both net water flux and the affinity correction; it does not justify an extra experimental matrix.

A low terminal-product equilibrium concentration also does not establish inadequate site recovery. Most inlet water can pass through unreacted while a smaller cleaning flux maintains useful θ. Determine net water consumption and oxygen export at stationary inventories, then relate them to functional occupancy. The contribution of this model is therefore a specific consistency test: the proposed chemical account must explain **both** working-site population and net oxygen flux without violating the closed-cycle equilibrium or the matched dry/wet response.
