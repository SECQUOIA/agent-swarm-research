# What a granule-size experiment can discriminate

2026-09-16. Conditional follow-up to the [qualified first test](../working/program-development/water-management-first-test.md), extending the [sphere calculation](water-transport-limits.md). No coefficients are fitted, no new numerical properties are assigned, and no experimental result is claimed.

An [independent quantitative review](../reviews/water-quantitative-followup-review.md) checked the sphere/film balance, scaling ambiguity and sufficient inequalities below. Their application remains conditional on experimentally available parameter bounds.

**Two catalyst sizes, by themselves, cannot identify whether PDVB changes external transfer or internal diffusion.** They can make a useful formulation comparison. A mechanistic or predictive shaping claim additionally needs an independently constrained size dependence of the relevant resistance and a justified link between exposure and the measured endpoint. In particular, an external-transfer effect can scale as radius squared, just like an internal-diffusion effect.

## Sphere with an external transfer resistance

Let qv be uniform net water production per granule-envelope volume, R the radius, D the internal effective diffusivity, k the external transfer coefficient, cb the bulk mobile-phase concentration and cs the surface concentration. Both coefficients must use the same concentration basis; D has units m²/s and k m/s. Constant coefficients, a stationary single phase, unchanged geometry, and no internal sink are assumed. The centre and external boundary balances give

\[
J_s=q_vR/3=k(c_s-c_b),
\]

\[
c(r)-c_b=q_v\left[\frac{R^2-r^2}{6D}+\frac{R}{3k}\right].
\]

Thus the centre excess is

\[
E_c=q_v\left[\frac{R^2}{6D}+\frac{R}{3k}\right],
\]

and the volume-average excess is

\[
E_{avg}=q_v\left[\frac{R^2}{15D}+\frac{R}{3k}\right].
\]

The surface flux integrated over 4πR² equals the complete source 4πR³qv/3. These equations extend the existing fixed-surface sphere result without identifying either coefficient for the Fang material. A bed-average measured production rate is only an approximation to local qv. A porous or wax-filled interface may not be described by one k.

At **equal qv, cb and R**, denote reference and promoted coefficients by subscripts 0 and P. The absolute centre-exposure decrease is

\[
\Delta E_c=\frac{q_vR^2}{6}\left(\frac{1}{D_0}-\frac{1}{D_P}\right)
+\frac{q_vR}{3}\left(\frac{1}{k_0}-\frac{1}{k_P}\right).
\]

This subtraction does not apply unchanged when PDVB lowers production. Then subtract `qv,0[A0+B0] − qv,P[AP+BP]` explicitly; a smaller source is a separate contribution. Do not compensate it by changing temperature and thereby changing catalyst kinetics and damage.

## Four different meanings of “benefit”

With Bi = k0R/D0, the external resistance accounts for `1/(1 + Bi/2)` of the **centre excess**, or `1/(1 + Bi/5)` of the volume-average excess. If only k increases by a factor β, at fixed R, qv and D,

\[
\frac{\Delta E_c}{E_{c,0}}=
\frac{1-1/\beta}{1+\mathrm{Bi}/2}.
\]

At fixed k0 and β, the absolute external-transfer benefit grows as R, but its fraction of the total excess decreases as R grows because the unchanged internal term grows as R². There is no contradiction: a larger absolute reduction can remove a smaller fraction of a larger excess. A fraction relative to **total concentration** additionally includes cb and is smaller still.

None of these quantities equals normalized formulation retention. Retention integrates an unknown exposure/state history and is measured with different complete formulations still present. Observed rate additionally depends on H2/CO delivery, inhibition, active-site state and effectiveness. Even a monotonic water-damage response can have a threshold: halving an exposure excess may leave retention unchanged, remove nearly all damage, or move both formulations into the same damaging region. Do not regress a radius exponent from retention or rate and call it a diffusion exponent.

## Why linear versus quadratic scaling is not a general discriminator

External-only promotion gives `ΔEc = qv R(1/k0 − 1/kP)/3`. Its radius dependence is linear **only when those k values stay constant**. For a fixed enhancement β and `k0 ∝ R^−m`, it instead scales as `qv R^(1+m)`.

As an algebraic counterexample, define the Sherwood number `Sh = 2R k/Dg`. If Sh and gas diffusivity Dg are constant over the size change, k is proportional to 1/R; external-only promotion then scales as R². An internal-only change at fixed D values also scales as R². This is not an assertion that the present bed has constant Sh. It proves that radius-squared behavior does not identify an internal mechanism without further constraints.

Conversely, changing catalyst size while holding promoter size fixed changes contact number, packing and possibly liquid connectivity. The promoter's enhancement factor need not remain fixed. Source strength and granule-envelope density can also change. Two exposure points would not identify these possibilities; two recovered-function points identify still less.

## The smallest useful prospective shaping prediction

The practical question is **whether smaller unpromoted catalyst granules can replace the original promoted formulation under the already qualified challenge, without losing useful output or imposing an unacceptable pressure-drop burden**. This is more useful than identifying an exponent after observing four results.

A conservative prediction can avoid fitting the internal resistance if independent evidence bounds the external change. Define, at the original radius R,

\[
A=R^2/(6D_0),\qquad B=R/(3k_{0,L}).
\]

Let the smaller radius be αR, the measured source-density ratio be `γ = qv,small,0/qv,large,P`, and `κ = k0,small/k0,large`. Under the **external-only** model with `kP,large = β k0,large` and unchanged internal D,

\[
E_{small,0}=q_{v,large,P}\gamma(\alpha^2 A+\alpha B/\kappa),
\]

\[
E_{large,P}=q_{v,large,P}(A+B/\beta).
\]

A sufficient, deliberately conservative condition for the smaller unpromoted granule to have no greater excess everywhere at corresponding relative radii is

\[
\gamma\alpha^2\leq1,\qquad
\gamma\alpha/\kappa\leq1/\beta.
\]

The same componentwise condition also bounds the volume-average excess. It requires neither the numerical A/B partition nor a direct local-water measurement. Use an independently supported upper bound on β, lower bound on κ and upper bound on γ to choose α **before** observing the small-granule challenge. These bounds must pertain to the conditioned formulation and its actual transfer path. Molecular self-diffusivity, dry contact angle, a fitted deactivation curve, or a generic gas-film correlation assigned to an unverified wax interface does not supply them.

For an **internal-only** enhancement `DP,large = βD D0` with unchanged external transfer, the corresponding sufficient inequalities are

\[
\gamma\alpha^2\leq1/\beta_D,\qquad
\gamma\alpha/\kappa\leq1.
\]

These conditions are conservative dominance tests, not necessary conditions or material predictions. They assume the relevant coefficient changes have been isolated independently. They also concern stationary exposure only. Inferring no worse damage requires a monotonic exposure-response relation in the tested interval, comparable initial state, and controlled transition histories. Inferring no worse **useful output** additionally requires measuring the initial-rate penalty, selectivity, and recovery response; the inequalities cannot supply that result.

If the first experiment and independent transport measurements cannot constrain β and κ sufficiently to select a resolvable α, **do not label the two-size experiment a prospective mechanism discriminator**. No defensible numerical size target follows from the present evidence. It may still be worth a direct operational substitution test, with its more limited claim stated in advance.

## Minimal execution and decision

Proceed only after the first-test formulation contrast and handling are reproducible. Retain its fixed challenge/recovery horizon, balances and endpoint definitions. Use the already qualified original-size ±PDVB pair and add just one smaller catalyst-size pair, keeping PDVB dose and promoter granule size fixed. The smaller unpromoted arm tests substitution; the smaller promoted arm distinguishes substitution from a generally improved small-granule formulation that still benefits from PDVB. Requalify conditioning across size: different dimensions can create different activation and retained-liquid histories even under nominally identical gas programs.

Before the challenge, record representative size distributions, catalyst mass per envelope volume, initial production per catalyst mass, pressure drop and initial useful productivity. Do not set qv from mesh labels or bulk bed density. During the comparison measure the actual water source and gas balances, including the greater generated-water fraction in the low-water recovery interval. Source evolution during damage limits a constant-source prediction; count it as a failed assumption rather than adjusting γ after the result to rescue agreement.

Freeze one design decision: whether the smaller unpromoted formulation meets a predefined, experimentally resolvable useful-output target relative to the original promoted formulation under a stated pressure-drop constraint. Choose that target from the actual process or experiment decision, not a universal percentage. Report retention separately. If the conditional exposure prediction is also justified, test it through the previously qualified water-sensitive response and state its dependence on that calibration; do not infer local activity from the same endpoint being predicted.

A successful substitution supports a specific shaping choice under this history. It does not prove which resistance changed. A failed substitution rejects that design or its assumptions; it does not falsify hydrophobic promotion. Improved small-granule retention with insufficient useful output remains a scientific result without an established practical advantage.

## Existing size evidence and originality

[Fang et al. 2026](https://doi.org/10.1038/s41467-026-76571-8), main Fig. 1 and SI Table 4, already compare granule sizes and mixing arrangements. Table 4 uses 0.5 g Co/SiO2 with **1.0 g PDVB**, spanning 10–20 through 60–80 mesh; its conversion entries are observations at 36 h, not independently determined water conductances. The main text distinguishes coarse-granule deactivation and stable finer mixtures, with changed initial conversions. These data establish that geometry matters, and they prevent claiming a size screen as new. They do not uniquely identify external versus internal resistance or validate transfer to the low-dose, late-addition, imposed-water protocol.

The subsequently supplied [Yang et al. 2020 original](../../literature/papers/yang2020-investigation-of-the-deactivation-behavior/fulltext.md), pp. 7–9, adds a closer geometry–deactivation precedent: silica-shell thickness comparisons at about 75% initial CO conversion and calculated 0.36–0.37 MPa bulk water pressure. Thinner-shell catalysts retained more activity over 50 h at 240 °C; the authors attribute this to local water removal. These are different encapsulated materials with changing cobalt loading, pore dimensions and GHSV, not an independently isolated transfer coefficient or a direct local-water measurement. Their 220 °C results also implicate heavy-hydrocarbon retention. Thus neither geometry-linked durability nor the competing wax explanation is itself new.

The defensible advance would be a held-out shaping decision predicted from independently constrained quantities. At present the analytical framework identifies what such a prediction needs; **it does not establish that those constraints are experimentally available**. If they are not, retain the smaller-granule comparison only when its direct formulation decision warrants the work.
