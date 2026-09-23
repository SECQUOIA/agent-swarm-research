# When does a during-reaction titration curve reveal inactive titratable sites?

2026-09-16. Illustrative plug-flow model supporting the [methods screen](../working/direction-search/methods-advance.md) and the standards addition proposed in the [portfolio review](../reviews/direction-search-portfolio-review.md). No parameters are fitted to a catalyst; the numbers are dimensionless. Script: [`titration_front.py`](titration_front.py); outputs: [`titration_front.png`](titration_front.png), [`titration_front_summary.json`](titration_front_summary.json).

## Question

A titrant (pyridine, 2,6-di-tert-butylpyridine, trifluoroethanol, water, CO2) is fed continuously to a packed bed during reaction. The rate is recorded against cumulative uptake and extrapolated to zero rate to count sites. If only a fraction of the titratable sites are catalytically active, does the curve show it?

## Model

Plug flow along a bed with two irreversibly titratable site classes: active sites (per-site rate 1) and spectators (rate 0), spectator fraction f_S of the titratable total. Titrant is consumed only by adsorption; gas-phase accumulation is neglected because site inventory per bed volume far exceeds titrant inventory. Each class has an adsorption Damköhler number Da (adsorption rate constant times bed residence time; large means the titrant is consumed within a short length of bed) and, optionally, a desorption term. Observed rate is the bed-integrated active-site rate at differential reactant conversion. Uptake is normalized to the titratable total and rate to the fresh rate, so the ideal front limit predicts the line rate = 1 − uptake for every f_S. The extrapolated intercept is obtained, as an experimentalist would, from a linear fit of the portion with rate above half the fresh rate.

## Results

| Case (f_S = 0.3 unless noted) | Extrapolated intercept (fraction of titratable total) | Initial slope (fresh-rate units) | Reading |
|---|---|---|---|
| Both classes fast (Da = 400), f_S = 0, 0.3, 0.6 | 1.000 for all three | −1.00 for all three | Sharp front; the spectator fraction is invisible |
| Both classes with equal Da, scanned Da = 1 to 400 | 1.000 at every Da | −1.00 | **Equal uptake kinetics hides heterogeneity at any front sharpness**; the line is exact, not approximate |
| Slow adsorption everywhere, active sites bind 10× faster (Da 0.5 / 0.05), f_S = 0.3 / 0.6 | 0.74 / 0.48 (true active fractions 0.70 / 0.40) | −1.35 / −2.08 | Curve convex; early slope approximately counts active sites |
| Active sites fast (Da = 400), spectator Da = 0.5, 2, 5, 20, 50, 400 | 0.72, 0.78, 0.87, 0.97, 0.99, 1.00 | −1.38 to −1.00 | Heterogeneity fades as spectator uptake becomes transport-limited: intercept within 3 % of the total once spectator Da × f_S exceeds about 6 |
| Reversible titrant, both fast (Da = 400), desorption 10× the titrant feed rate, active sites bind 10× more strongly | 0.96 | −1.04 | Reversibility does not restore sensitivity while adsorption is front-limited; the steady state then reports an equilibrium coverage, not a count |

Established for the model (arithmetic and numerical solution); the transfer to a real bed is an inference that depends on whether adsorption on the slower-binding class is complete within the bed.

## Consequences

1. **The hiding condition is complete per-pass uptake on every titratable class, not the sharp front itself.** If the titrant is quantitatively consumed by the bed during the linear portion of the curve (no breakthrough), the curve cannot report which titratable sites turn over: the intercept is the titratable total and the slope is the bed-average rate per titratable site. This is the usual design for during-reaction titration, because experimenters choose slow titrant feed and complete uptake so that uptake equals the fed amount.
2. **Curve shape carries site-selectivity information only when the slower-binding class breaks through**, that is, when its uptake per pass is incomplete (Da × inventory fraction below roughly 1 in this model). In that regime the early slope overestimates the per-site rate and the early extrapolation approximately counts the faster-binding class. Whether the faster-binding class is the active one is a separate, chemistry-dependent assumption.
3. **A linear curve is consistent with any spectator fraction.** Equal adsorption kinetics on active and spectator sites gives an exact line at any Da. Linearity is therefore not evidence of uniform activity; the portfolio review's two-parameter argument (rate(0) = a·N_A and intercept N_A + N_S cannot yield a and N_A separately) applies.
4. **Operational diagnostic.** Record titrant breakthrough during the titration. Complete uptake (effluent titrant below detection during the linear region) means the count is a titratable total; report it as such. Partial breakthrough from the start means the curve may be affinity-selective, and the bed-mass and titrant-pressure invariance checks in the methods screen become informative. Mixtures with known spectator fraction remain the only ground truth for the extrapolated count.
5. **Reversible titrants.** Desorption redistributes titrant toward stronger-binding sites only when desorption is fast relative to front propagation and the front is not adsorption-limited. With fast irreversible-like uptake the line persists; at steady state the coverage reflects binding equilibria and feed rate, so a steady-state rate suppression is not a site count without an independent isotherm.

## Limits

One-dimensional plug flow without axial dispersion, isothermal, differential reactant conversion, titrant does not react or migrate between crystals, one titrant molecule per site, no titrant-induced site creation or destruction. Intracrystalline transport of the titrant (shell-first poisoning within a crystal) is not modeled; it produces the same hiding effect at the crystal scale when intracrystalline uptake is transport-limited. The Damköhler values are illustrative; a real titration should estimate its own from measured breakthrough.
