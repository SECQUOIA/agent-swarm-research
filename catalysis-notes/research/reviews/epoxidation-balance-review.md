# Independent review: EO selectivity and the oxygen balance

## Finding

Hwang et al.'s `S > 1` is strong evidence against an exclusive, closed monooxygenase (MO) scheme in which every O2 gives at most one EO and the other oxygen ends in ethylene/EO combustion products. It does not identify a unique molecular pathway. The reported ethane feed cannot, even at complete conversion to ethylene and water, account for the reported `S ≈ 1.4, X_O2 ≈ 0.27` within that MO scheme. A chloride-mediated catalytic shuttle must be bounded by its reductant consumption, not by the ppm chloride feed.

**Source inspected:** the [original article](../../literature/papers/hwang2026-mechanism-and-site-requirements-for/original.pdf), DOI 10.1016/j.jcat.2026.117021: methods §2.2 (p. 3), definition §3.1/Eq. (2) (p. 4), Eqs. (3)–(5) and Fig. 2 (p. 5), steady-state/transient discussion and Fig. 5 (pp. 11–12), and the explicit paired maximum in §3.5 (p. 16). The local text extraction omits equations; Eq. (2) and the chloride reactions were checked in text extracted directly from the PDF. The complete nine-page [supporting information](https://ars.els-cdn.com/content/image/1-s2.0-S0021951726003568-mmc1.pdf) was subsequently retrieved; section S4 (pp. S5–S7) was inspected for rate definitions and model discrimination.

## 1. Exact mappings within the stated product set

Let `e`, `c`, and `w` denote **net molar formation rates** of EO, CO2, and water, and `q` net molar O2 consumption. Assume stationary chemistry, ethylene as the reacting carbon/hydrogen source, no accumulating material, and these three products. Atom balances give:

```
ethylene consumed = e + c/2
w = c
2q = e + 3c
S = e/(3c)                         [the authors' Eq. (2)]
carbon selectivity s = e/(e+c/2) = 6S/(6S+1)
oxygen-atom utilization u = e/(2q) = S/(S+1)
EO per net O2 consumed = 2u
```

Here oxygen utilization counts the fraction of consumed O2 oxygen atoms retained in **net EO product**. It is not O2 conversion. The same net balance allows secondary EO combustion and, with proper inlet subtraction, EO/CO2 cofeeds.

| Authors' S | Carbon selectivity | Oxygen-atom utilization | EO / net O2 |
|---|---:|---:|---:|
| 1 | 85.71% | 50.00% | 1.000 |
| 1.4 | 89.36% | 58.33% | 1.167 |
| 1.9 | 91.94% | 65.52% | 1.310 |

For an ideal mixture of the authors' MO and perfect DO stoichiometries, with no extra losses, the fraction of O2 consumption assigned to DO is `2u−1 = (S−1)/(S+1)`: 16.67% at `S=1.4`. This is a model-dependent channel allocation, not an independently measured molecular fraction; additional combustion changes that allocation. Likewise, `S≤1` does not exclude a DO contribution masked by losses.

## 2. What the reported feeds can explain

The paired `S=1.4, X=0.27` maximum is explicitly reported for **B-LiCsRe**, referencing Fig. 2b. Fig. 2 specifies 510 K, 67 kPa O2, 340 kPa ethylene, 5.5 kPa CO2, and 2.8 kPa ethane. These conditions therefore legitimately belong in one calculation. Fig. 1 gives 2.7 kPa ethane for its B-LiCsRe series and a chloride range of 1.4–15 Pa. Fig. 5 discusses recovery near the selectivity maximum after decreasing chloride to 2.7 Pa. Do not treat that as an exact numerical chloride coordinate read from Fig. 2; the conservative bounds below do not require it.

Use feed-normalized flow units: multiply each molar flow by total inlet pressure divided by total inlet molar flow. An inlet partial pressure then represents its molar supply, and actual net O2 consumption would be `q=67×0.27=18.09` in these units. These are **not outlet partial pressures**; reaction-induced total-flow changes must be corrected.

### Ethane as a sacrificial reductant

The most favorable carbon-preserving alternative is net `C2H6 + O → C2H4 + H2O`. Let `a` be the ethane consumption supplying the extra hydrogen. With the stated product set, hydrogen and oxygen balances become `w=c+a` and `2q=e+3c+a`. Complete oxidation of ethane also creates CO2; it is not a way to hide its carbon from the denominator.

If the exclusive MO hypothesis requires `e≤q`, then:

```
S ≤ q/(q−a)
a required at S=1.4 ≥ q(S−1)/S = 5.17
available ethane a ≤ 2.8
maximum MO-only S ≤ 18.09/(18.09−2.8) = 1.183
```

Thus even **100% ethane conversion** cannot explain the observed maximum through this sacrificial-reductant route alone. Holding independently measured `q` and `S` fixed, the extreme `a=2.8` gives `e=19.47`, or oxygen utilization at least **53.82%**, still above 50%. Actual ethane conversion is not provided in the inspected main text; the 100% case is a deliberately generous bound, not an estimate of its behavior.

### Chloride feed versus a catalytic chloride shuttle

The article gives deposition `C2H5Cl → C2H5* + Cl*` and scavenging `C2H6 + Cl* → C2H5Cl + H*` (Eqs. (3), (5)). A hypothetical cycle that also dehydrogenates the ethyl intermediate could regenerate chloride and consume ethane. Consequently, **ppm chloride supply does not cap catalytic turnover**. Such an alternative is subject to the ethane bound above; these equations alone do not establish that it occurs at an appreciable rate.

In contrast, a net, nonrecycled chloride stream is tiny. For example, the overall transformation `C2H5Cl + O → C2H3Cl + H2O` consumes one oxygen atom per chloride molecule. Even allowing the entire 15 Pa upper feed to follow that route supplies only `0.015` oxygen-atom flow units, versus the `5.17` needed above; at 2.7 Pa it supplies `0.0027`. Ordinary net chloride scavenging at that scale is negligible for this discrepancy. This comparison bounds the stated stoichiometric route, not all conceivable chemistry of a catalytic chlorine inventory. The paper's proposed ClO transfer to Re itself recycles chlorine and requires no stoichiometric chloride consumption per EO.

## 3. Measurement and reservoir qualifications

The numeric bound using `q=18.09` assumes the reported conversion is **independent actual inlet-minus-outlet O2 consumption**. Methods report inlet/outlet GC analysis of reactants and products, with CH4 as an internal standard. SI section S4 calls the rate measured O2 consumption and defines `r_O2=X/τbed`; it also distinguishes measured rates from model predictions. These statements support treating O2 consumption as an experimental quantity, but neither the methods nor that SI section explicitly gives the analytical calculation distinguishing direct O2 measurement from product reconstruction. The inspected main text also does not report a complete analytical closure, ethane conversion, water balance, or uncertainty budget. Treat the bounds as conditional calculations, not measured closure results. CH4 is treated as inert as intended by its stated internal-standard role.

If instead `q0=18.09` was reconstructed using `2q0=e+3c`, then `S=1.4` implies `c=5.025` and `e=21.105`. At these fixed product rates, the extra oxygen-atom sink needed to restore exclusive MO is `a≥e−3c=6.03`, also above the 2.8 ethane supply. The required actual O2 consumption would then differ from `q0`. **5.17 and 6.03 answer different measurement assumptions and must not be combined.** Absolute measured product rates would remove this ambiguity.

Because CO2 is cofed, `c` must subtract its inlet flow; `e` likewise subtracts inlet EO when present. The article defines S using molar yields, not raw outlet concentrations. Using total outlet CO2 without subtraction would depress S rather than manufacture a supra-MO result. An inaccurate subtraction or changing carbonate inventory could distort net CO2; neither is demonstrated here.

Finite stored oxygen can temporarily supply EO; carbon/CO2 storage can temporarily suppress apparent CO2 formation. They invalidate a stationary interpretation during inventory change. They cannot support a lasting excess after the inventories return to their initial values: integrate all net flows and inventory changes over conditioning and recovery. The paper explicitly distinguishes steady-state circles from transient crosses in Fig. 5 and reports reversible recovery over long conditioning periods. This argues against treating the headline result as an isolated transient peak. The inspected source does not supply the inventory and closure data needed to place a separate numerical reservoir bound. Missing closure data are a limit on an independent audit, not evidence of a reservoir artifact.

## 4. Mechanistic conclusion and practical cross-check

Once cofeed and inventory corrections are negligible or bounded, `S>1` establishes net oxygen use beyond the exclusive combustion-coupled MO stoichiometry. It does not by itself track the two atoms of an individual O2 molecule, distinguish initial from recycled oxygen, establish O-adatom electrophilicity, or prove ClO intermediates, transfer by Cs, or a particular Re oxidation state. Those specific assignments depend on the paper's additional kinetic and catalyst-composition evidence and remain mechanistic interpretations. Oxygen recycling between activation events can also separate a net stoichiometric result from the fate of one initially adsorbed O2 molecule; no such alternative is asserted to dominate here.

The SI explicitly acknowledges a narrower model-identification limit for **unpromoted sample B**: its 58-condition dataset cannot distinguish several candidate primary branching and secondary EO-consumption mechanisms (section S4, pp. S6–S7). Five-parameter alternatives have similarly weak parameter estimates; adding a sixth parameter improves the fits, but the tested six-parameter models remain statistically indistinguishable. This supports caution about unique assignments from those fits. It is not itself a comparison of the promoted-catalyst ClO shunt against the recombination alternative below.

The [practical metrics note](../calculations/epoxidation-practical-metrics.md) was independently checked. Its molar resource table is correct within its stated stationary EO/CO2/water balance. At fixed net EO output, 90%→91% carbon selectivity reduces reaction ethylene consumption by 1.0989%, CO2 formation by 10.9890%, and O2 consumption by 4.3956%. These are reaction-balance changes, not plant-wide savings.

## 5. Explicit recombination counterexample and its testable limits

Consider a minimal stationary network in which the initial event is `O2 + ethylene → EO + O*`, at gross rate `r0`. Let `C` be the oxygen-atom rate of leftover O* consumption in complete **ethylene** combustion, `H` its oxygen-atom rate of transfer to additional EO, and `D` the molecular O2 rate from `2O* → O2`. There are no other reactions in this counterexample, including secondary EO combustion. Then:

```
O* balance:       r0 = C + H + 2D
net EO:           e = r0 + H
net CO2:          c = C/3
net O2 consumed:  q = r0 − D
authors' ratio:   S = e/C
                  (H+D)/q = (S−1)/(S+1)
```

Thus `S>1` is possible with **H=0** and **D>0**. At `S=1.4`, recombination alone requires `D/q=1/6`, equivalently `D/r0=1/7`; two-sevenths of the leftover O atoms recombine. On the independently measured `q=18.09` basis, `D=3.015`, `r0=e=21.105`, and `C=15.075`. These reproduce the same net EO/CO2/O2 rates as the closed balance in §1. More generally S fixes **H+D**, not their separate values, in this minimal network.

In the zero-combustion limit with H=0, two initial events and one recombination sum to `2 ethylene + O2 → 2 EO`: perfect net oxygen efficiency despite using only one atom per **gross initial O2 activation**. Returned oxygen can leave the reactor or undergo another activation; gross rates must count such reactivation consistently. This is an algebraic counterexample to unique pathway assignment from S, not evidence that recombination actually competes on B-LiCsRe. The inspected Hwang main text does not explicitly evaluate recombination as this alternative. The ethane bounds above exclude a particular sacrificial-reductant explanation; they do not exclude oxygen return to the gas phase.

### What isotope scrambling would and would not establish

For random recombination from a single oxygen pool with 18O atom fraction `x`, the newly formed mixed-isotope O2 rate is `2x(1−x)D`. At `x=1/2`, the H=0 explanation of `S=1.4` predicts a formation rate of mixed O2 equal to `q/12`. This is a conditional quantitative target. The surface pool composition need not equal the inlet isotope composition.

- A low measured mixed-O2 rate can bound D only if the productive leftover-oxygen pool mixes as assumed and the fraction of recombined O2 reaching the detector is known. Re-adsorption, separate oxygen pools, incomplete label mixing, and transport must be included before converting an effluent signal into a bound on gross recombination.
- A positive scrambling signal does not establish the productive return rate D: dissociation/recombination on spectator sites can exchange oxygen without making EO. Under a validated common-pool and escape model, total recombination can provide an upper bound on productive D; a large total rate alone cannot assign that rate to the selective cycle.
- With both H and D possible, a defensible upper bound `D_max` would imply `H/q ≥ (S−1)/(S+1) − D_max/q` within this minimal network. Establishing positive H still would not identify ClO/Cs/Re as its unique molecular route.

The existing [Pu et al. 2024 source](../../literature/papers/pu2024-revealing-the-nature-of-active/fulltext.md), §3.5, reports no detected mixed 16O18O after an isotope switch and a calculated O* recombination barrier of about 1.00 eV; §3.3 also discusses absent O2 evolution during ethylene temperature-programmed reaction. Those observations constrain their unpromoted Ag/α-Al2O3 system and conditions. They are relevant precedent, not a numerical recombination-rate bound for Hwang's chloride/Cs/Re-promoted catalyst. A calculated barrier alone supplies neither the working coverage nor the rate needed for that transfer.

### Appendix: a stronger isotope test for productive oxygen return

**Lateral mixing of O atoms is not necessary for the 50% prediction.** Consider a stationary, molecularly mixed, equimolar 16O2/18O2 feed. Assign each fresh homoisotopic molecule an independent isotope label. In the minimal MO network above, one atom from each fresh molecule leaves the relevant O* pool as EO; only its partner remains. Two recombining leftovers therefore have different fresh parent molecules. If reaction, residence, and pairing probabilities are isotope-blind, their labels are independent even when they occupy separate, immobile sites. Half of their pairs are 16O18O. Ordinary correlations in arrival times or proximity do not create correlations between independent isotope labels. Separate surface domains alone therefore do not defeat this prediction when each receives the same molecularly mixed feed.

The sufficient assumptions are more precise than merely calling the surface well mixed:

1. Fresh O2 molecules supply independent labels at the scale and times at which the relevant sites react; isotope effects do not select labels.
2. Each atom in the productive return pool is the sole remaining atom of its fresh O2 parent. The EO oxygen does not re-enter that pool, and other oxygen-bearing species do not supply a correlated or differently labeled input.
3. The fraction of formed mixed O2 that escapes to the detector is known or bounded below.

Under assumptions 1–2, immediate recombination of the two atoms of one initially adsorbed O2 molecule cannot explain the productive return D: one of those atoms has already formed EO. Repeated return and activation within the same minimal network does not change this argument; it removes atoms from distinct-parent pairs without creating a second surviving atom of a fresh parent. Specific routes that restore both parent atoms to the pool—such as product oxygen returning after reaction, or oxygen exchange connecting an additional dissociation pool—require an expanded isotope balance. Their existence and magnitude must be established for the working catalyst. They should not be presumed merely because generic O2 exchange can occur. Continuous oxygen input from CO2/water and incomplete isotopic equilibration likewise need explicit accounting in the actual cofed experiment.

This supplies a useful conditional bound. Let `M` be the measured escaping mixed-O2 molar flux, after correcting inlet isotopologue impurities and instrument background. Let `η_min>0` be a defensible lower bound on the escape probability of mixed O2 formed by productive return. Additional spectator scrambling contributes a nonnegative signal, so:

```
D_productive ≤ 2 M / η_min
recombination-only S=1.4 requires M ≥ η_min q/12
```

Use an upper confidence limit on M to reject a proposed return rate. Spectator exchange weakens a positive assignment but does not invalidate this upper bound under the stated assumptions. Without an escape bound, absence of mixed O2 at the outlet cannot exclude rapid local gas release and re-adsorption. Net O2 conversion alone does not measure that gross cycling.

Finally, `2O* → O2*` followed by immediate epoxidation **without release to the gas** is a different measurable proposition. Summing that surface loop gives `O* + ethylene → EO`; it belongs in H as a net surface salvage route, even if its elementary steps use molecular oxygen. It can evade a gas-phase mixed-O2 test while increasing net oxygen efficiency. Evidence excluding substantial gas return would therefore support additional surface oxygen use, but would still not uniquely establish the Re-mediated shunt.

### Appendix: a minimum return requirement with primary and secondary losses

The required oxygen-return rate can be bounded using net whole-bed products without separately estimating primary EO production. Extend the stationary network with these nonnegative rates:

- `v`: initial `O2 + ethylene → EO + O*` events;
- `u`: direct `O2 → 2O*` dissociation events;
- `C`: O* atom consumption in complete ethylene combustion;
- `h`: O* atom transfer to additional EO;
- `b`: secondary EO combustion events, each consuming five O* and forming two CO2 and two water molecules;
- `d`: molecular O2 return to the gas through recombination.

With net EO formation `e`, net CO2 formation `z`, and net O2 consumption `q`, the balances are:

```
v + 2u = C + h + 5b + 2d
e = v + h − b
z = C/3 + 2b
q = v + u − d

G ≡ (e−3z)/2 = q(S−1)/(S+1)
h + d = G + u + b
```

Therefore an explanation with **no additional surface salvage (`h=0`)** requires:

```
d ≥ d_min ≡ max(0,G)
```

At `S=1.4`, `d_min=q/6`. Direct dissociation and secondary EO combustion increase the required return; they cannot remove this minimum. Integrating the local balances along the bed preserves the inequality, so it does not require negligible EO concentration, a differential reactor, or identification of the primary rates. It does require stationary inventories and the stated reaction/product set. An independently justified `d_upper<d_min` rejects return alone under these assumptions. Unlike the minimal network, net products no longer determine the exact sum `h+d`, because `u+b` is unknown.

**The isotope bound needs a corresponding distinction.** Direct dissociation can supply both atoms of one fresh O2 parent, allowing return without isotope scrambling. Thus `2M/η_min` is not automatically an upper bound on all of d in this extended network. Under the independent-label and restricted-oxygen-origin assumptions above, classify recombination into same-fresh-parent return `d_same` and cross-parent return `d_cross`. At stationary state, `d_same≤u`: each same-parent pair must have entered the atomic pool through a dissociation event, including repeated dissociation after gas return. Hence, for `h=0`:

```
d_cross = d − d_same ≥ d − u = G + b ≥ G
mixed O2 formation = d_cross/2
M ≥ η_min G/2                         [when G>0]
```

This retains the `M≥η_min q/12` target at `S=1.4`, now as a **minimum** despite the two extra losses. The escape bound must apply to cross-parent return. Spectator cross-parent exchange can add signal; same-parent exchange cannot explain away a deficit below this target. The argument assumes isotope-blind selection of independent fresh-parent labels and that oxygen in burned EO leaves as CO2/water rather than returning to the O* pool through an additional exchange route.

This extension does not correct for ethane oxidation, oxygen exchange with cofed CO2/water, other products, or changing inventories. Those require their own terms and cannot be silently included in `u` or `b`. In particular, the actual ethane-cofed experiment still needs the separate cofeed qualification in §§2–3 before this restricted-network minimum becomes an experimental exclusion test.

### Appendix: applying the minimum with a bounded ethane sink

The ethane cofeed need not make the return test inapplicable. Add a nonnegative oxygen-atom flux `a` for the specific net reaction `C2H6 + O* → C2H4 + H2O`. This extension covers ethane oxidative dehydrogenation; it does not silently include ethane combustion or other products. The balances become:

```
v + 2u = C + h + 5b + a + 2d
2q = e + 3z + a
G ≡ (e−3z)/2 = h+d−u−b+a/2
h+d = G+u+b−a/2
```

Under the isotope-ancestry assumptions above, `d_same≤u` still holds. Therefore an explanation with `h=0` requires:

```
d_cross ≥ max(0,G−a/2)
mixed O2 formation ≥ max(0,G−a/2)/2
```

Use measured net EO/CO2 rates to determine G and an upper bound on the ethane sink to obtain the conservative requirement `d_cross,min=max(0,G_lower−a_upper/2)`. Here `G_lower` and `a_upper` should include analytical uncertainty. The corresponding escaping mixed-O2 requirement is `M≥η_min d_cross,min/2`. A direct ethane-consumption measurement can tighten `a_upper`; assuming the entire ethane feed follows this route provides a generous supply bound, not evidence that this conversion occurs. Changing the ethane feed changes both this supply bound and the working chloride coverage, so use the feed and measured products from the same condition.

If **independently measured actual q** and S are held fixed instead of absolute product rates, then:

```
G = (q−a/2)(S−1)/(S+1)
d_cross,min = max(0, q(S−1)/(S+1) − a_upper S/(S+1))
```

For `S=1.4`, `q=18.09`, and `a_upper=2.8` in the feed-normalized flow units of §2, the corrected minimum is **1.3817** molecular O2 units, compared with **3.015** when a=0. It requires at least **0.6908** mixed-O2 formation units, or `η_min×0.6908` escaping units. These are conditional bounds using the full ethane supply as the maximum sink; they are not measured ethane conversion or isotope signals. The independently measured-q qualification remains essential.

Finally, oxygen exchange with cofed CO2 or water can alter isotope ancestry without supplying a net oxygen sink. It cannot automatically be represented by a. Its effect belongs in the isotope balance and escape calibration, even when the net material balance closes.
