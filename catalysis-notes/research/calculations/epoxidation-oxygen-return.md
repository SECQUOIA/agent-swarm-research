# Epoxidation: an oxygen-return alternative and its measurable scale

## Status

This conditional balance sharpens the [Ag screen](../working/epoxidation-opportunity.md). It is **not evidence that recombination controls selectivity**, nor a claim that oxygen recombination is a new mechanism. The [independent balance review](../reviews/epoxidation-balance-review.md) checks the algebra and the distinction between net stoichiometry and a molecular pathway.

**Measurement update:** a [fresh review of recovered prior art](../reviews/ag-isotope-reversibility-prior-art.md) verifies an existing quantitative isotope-reversibility balance that includes ordinary readsorption. Assess that CO2-labeling approach before the earlier fresh-parent mixed-feed design. The chemical lower bound below and the isotope-to-return mapping are separate: CO2 exchange can preserve the former while invalidating assumptions of the latter.

The practical question is whether an oxygen atom left after a molecular-O2 epoxidation event can return to O2 fast enough to avoid combustion under working Ni–Ag conditions. If it can, high net oxygen utilization need not identify transfer of that atom directly to an epoxide through a Re-containing intermediate. An inactive retained oxygen population can also change branching indefinitely without acting as a continuing oxygen sink; these are different possibilities.

**2026-09-16 source update:** the [updated isotope review](../reviews/ag-isotope-reversibility-prior-art.md) now includes Esposito2024 main and Esposito2026 main/SI. Their shared-oxidant evidence does not establish identical ethylene/propylene rate control or transfer a propylene gas-return bound to Ni/Cs/Re–Ag. A reversible O2-derived precursor before irreversible generation of the CO2-exchanging oxidant remains consistent with the 2024 source. The conditional mass-balance derivation below is unchanged.

## Minimal stationary network

Assume an initial event consumes one O2, forms one EO and leaves one O atom. Let:

- `v` be the rate of these initial events, in mol/s;
- `c` be the oxygen-atom flux consumed in complete ethylene combustion;
- `h` be the oxygen-atom flux converted directly into additional EO by a second route;
- `d` be the O2-molecule flux formed by recombination of leftover oxygen atoms and returned to the gas.

There is no continuing oxygen storage, other carbon product, sacrificial cofeed oxidation, or independent oxygen-activation route in this deliberately restricted network. All rates refer to the same boundary. Its balances are:

\[
v=c+h+2d,\qquad e=v+h,\qquad z=c/3,\qquad q=v-d,
\]

where `e`, `z` and `q` are net EO formation, CO2 formation and O2 consumption. The factor three follows because combustion consumes three oxygen atoms per CO2 when its accompanying water is included.

With Hwang's selectivity ratio `S=e/(3z)=e/c`, the special case `h=0` gives:

\[
d=(e-3z)/2,\qquad \frac{d}{q}=\frac{S-1}{S+1}.
\]

Thus `S=1.4` could arise from a return flux `d=q/6` even with no direct second-oxygen transfer to EO. The net oxygen balance is identical to that of a mechanism that uses both atoms productively without gas-phase return. This establishes nonuniqueness; it does not fit rates or establish the energetic feasibility of either mechanism.

More generally, this restricted network fixes `h+d`, not the two terms separately:

\[
\frac{h+d}{q}=\frac{S-1}{S+1}.
\]

A defensible upper bound `d_max` would therefore imply `h/q ≥ (S−1)/(S+1) − d_max/q`. A positive lower bound would require selective oxygen use beyond the bounded return route. It would not identify a particular intermediate or metal site.

The equation refers to leftover-oxygen return in this model. A large unrelated dissociative adsorption/recombination exchange cycle can produce isotopic scrambling without accounting for selective turnovers. Secondary EO combustion and other oxidation channels require an expanded balance rather than silent reuse of this expression.

## Conservative extension for dissociation, secondary combustion and ethane

The exact minimal-network return estimate is not the quantity to carry unchanged into a promoted-catalyst experiment. Let `u` be independent O2 dissociation events, `b` secondary EO combustion events, and `a` oxygen-atom consumption by the specified net reaction `C2H6 + O → C2H4 + H2O`. All are nonnegative rates on the same stationary boundary. Then:

\[
v+2u=c+h+5b+a+2d,\quad e=v+h-b,\quad z=c/3+2b,\quad q=v+u-d.
\]

For `G=(e−3z)/2`, these give `h+d=G+u+b−a/2`. Independent dissociation can supply same-parent, unmixed recombination, so an isotope measurement no longer bounds **all** gross return by the minimal-network formula. However, its same-parent return cannot exceed `u` under the stated ancestry model. With `h=0`, the return formed from different O2 parents must therefore satisfy:

\[
d_{\mathrm{cross}}\geq \max(0,G-a/2).
\]

Use a joint conservative lower bound on `G−a/2`, based on measured net products and measured or bounded ethane consumption. With independent parent labels at equal isotope abundance, the required mixed-O2 formation is at least half this value; multiply by a validated escape/recovery lower bound for the detectable requirement. Secondary EO combustion strengthens rather than relaxes this minimum. Neither `u` nor `b` must be separately fitted to apply the conservative bound.

If actual O2 consumption `q` is measured independently and `S=e/(3z)`, the equivalent bound is `max[0, q(S−1)/(S+1)−aS/(S+1)]`. At the source example `q=18.09`, `S=1.4`, and an upper limit `a=2.8`, all in consistent feed-normalized flow units, required cross-parent return is at least **1.3817**, and mixed-O2 formation at least **0.6908** before escape losses. These are conditional calculations, not measured ethane conversion or return flux. The no-ethane value `q/6=3.015` would overstate the guaranteed minimum.

This extension covers the stated ethane-to-ethylene route, not arbitrary side products, persistent storage or unrestricted oxygen exchange. Product oxygen re-entry and additional oxygen sources require a revised ancestry model. Changing ethane to simplify the balance can also change chloride removal and the catalyst state. The [independent audit](../reviews/epoxidation-balance-review.md) gives the derivation and measurement distinctions.

## Evidence that motivates and limits the question

- An older isotope study explicitly considered epoxide formation from preadsorbed atomic oxygen either directly or after recombination. Only the abstract was inspected here; full text is requested. [Van Santen and de Groot, 1986](https://doi.org/10.1016/0021-9517(86)90341-6).
- Pu et al. observed no scrambled O2 during their isotope switch on supported Ag and argued against substantial recombination under those conditions. This is an important negative comparator, not a universal bound for Ni-containing or fully promoted surfaces. [Pu 2024](https://doi.org/10.1021/acscatal.3c04361), main text §3.5 and Fig. 6. The [subsequently recovered SI](../../literature/papers/pu2024-supplementary-information-for-revealing-the/fulltext.md) supplies the trace but no reported quantitative mixed-O2 calibration or detection limit.
- Jalil et al. report lower-temperature O2 release from NiAg than Ag in surface-science TPD, alongside stabilization of a different oxygen population. Neither an O2-TPD peak nor an O 1s component establishes return flux in an ethylene/O2 reaction mixture. [Jalil 2025 author manuscript](https://www.osti.gov/servlets/purl/2564884), pp. 4 and 7–8.

## Conditional isotope signal, not a proposed measurement result

Suppose recombining leftover oxygen atoms carry independent isotope labels with 18O probability `x`. If every returned O2 reaches the detector without readsorption, its mixed-isotope fraction is `2x(1−x)`. At `x=1/2`, half the return flux appears as 16O18O. Therefore, for the recombination-only explanation:

\[
\frac{F_{34,\mathrm{formed}}}{F_{\mathrm{O_2,in}}}
=\frac12 X_{\mathrm{O_2}}\frac{S-1}{S+1}.
\]

For the **illustrative** values `S=1.4` and `X_O2=0.01`, this is `8.3×10⁻⁴` of inlet O2 flow. With 10 mol% inlet O2 it corresponds to about **83 ppm of inlet total molar flow**. The number is a detectability scale under the assumptions, not a detection limit, actual outlet mole fraction, or a prediction for a reported catalyst.

This is a potentially accessible signal rather than an intrinsically sub-ppm requirement. Calibration must nevertheless resolve feed isotopologues, instrument response, gas residence time and relevant mass interferences.

### Carbon-product precision can be the tighter constraint

At those same illustrative conditions, the closed balance gives net EO and CO2 formation of about 1167 and 278 ppm of inlet total flow. The discriminator `e−3z` is only 333 ppm, even though both products are readily detectable. With an illustrative 0.5 mol% CO2 cofeed, the combustion increment is about 5.6% of the CO2 background. Independent 1% relative uncertainties on inlet and outlet CO2 readings would give about 73 ppm uncertainty on their difference, before multiplying it by three in the discriminator. These numbers describe an assumed error model, not an instrument specification or a source-reported uncertainty.

Consequently, resolving mass 34 alone is insufficient. Establish the uncertainty of the **net** carbon-product difference at the intended operating point. Matched differential calibration or a modest conversion change may suffice; a second carbon isotope should be considered only if that demonstrated limitation requires it. Changing conversion must preserve a valid local-state comparison and control secondary chemistry.

## What a test could and could not decide

A small isotope-composition switch or mixture experiment should preserve total O2, ethylene, chloride and product partial pressures and verify unchanged catalytic rates. Use the catalyst's actual stable working state. A comparison without ethylene is informative about exchange but cannot substitute for the reacting-state experiment.

**A positive scrambling signal is not enough.** It may arise from an oxygen-exchange population that does not mediate selective turnovers. Compare its quantitatively inferred flux with the return flux required by the measured `e` and `z`, and test whether its changes predict the selective-output response to one independent condition. Even agreement leaves parallel mechanisms possible.

**Independent event labels are sufficient; lateral oxygen mixing is not required.** In the restricted cycle, each productive leftover atom is the sole remaining oxygen atom from a different initial O2 molecule. With independent fresh-molecule isotope draws and isotope-blind chemistry, pairing two such leftovers gives the random-label result even in isolated surface domains. Recombining the two atoms of one original O2 molecule cannot dispose of the leftover after its other atom has departed in EO. Ordinary spatial separation or correlated event times therefore do not, by themselves, defeat the test. This argument needs qualification if product oxygen re-enters the pool, other oxygen sources contribute, or isotope histories remain nonstationary. See the [independent derivation](../reviews/epoxidation-balance-review.md).

**Detection still requires a defensible escape bound.** Let `M_max` be an upper confidence bound on newly generated mixed-O2 flux, allowing for consumption of inlet mixed O2, and let `η_min > 0` be a validated lower bound on the fraction reaching the detector after release. In the minimal network, `d ≤ 2 M_max/η_min`; with independent dissociation, apply this to cross-parent return instead. Spectator scrambling makes the upper bound less restrictive; it does not invalidate it under the stated ancestry model. Compare it with the conservative required return above, including ethane when present. If `η_min` cannot be bounded, a missing signal does not reject the route. Low net O2 conversion alone does not measure gross readsorption or establish this escape fraction.

An O2 intermediate that reforms and reacts on the surface without reaching the bulk gas is a distinct remaining possibility. At the net level it supplies another selective route from retained O to EO. A bulk-gas return test cannot exclude that route or distinguish it from direct atom transfer through Re. Its conclusion must name the gas-return route actually bounded.

The experiment becomes consequential if it excludes the return-only explanation at the flux needed to account for the observed selectivity, or identifies a return contribution that successfully predicts an untested operating change. It remains a conventional exchange measurement if it only shows that oxygen atoms scramble.

## Decision

Retain this as a **mechanism-discrimination option**, conditional on a stable high-selectivity Ni-containing reference and a defensible isotope-flux model. It does not justify building a full instrument campaign before those conditions are met. Confidence in the balance is high; confidence in the proposed return mechanism is low; confidence in an informative measurement is conditional. Practical improvements remain unproved.
