# Independent review of the water-management quantitative follow-up

2026-09-16. Reviewed the [published-output calculation](../calculations/water-published-output.md), its Python and JSON, and the [size discriminator](../calculations/water-size-discriminator.md). Checked the original Figure 1 XLSX, main article and relevant SI in `/tmp/catalysis-program-development/`. Only this review was written in the repository.

**The output arithmetic and size-model algebra pass independent checks.** The published comparison supports a cumulative reported-output advantage despite lower initial activity. It does not establish a new improvement, an optimized process advantage, or an experimentally available transport discriminator. The three source/basis clarifications identified below have been incorporated into the calculation note.

## Output calculation

Workbook headers confirm A/B and G/H as reference/promoted conversion and C/E and I/K as their separate selectivity time series. Their common interval is 25–585 h. Independent XML extraction confirmed the series counts and the single identical promoted-conversion duplicate at 154 h. The source SHA-256 matches the JSON. I used NumPy interpolation and Simpson integration on the merged knots, independently of the submitted script; Simpson integration is exact for the quadratic product on each interval.

| Independently checked quantity | Result |
|---|---:|
| Reference integrated proxy, 25–585 h | 116.0351956683 feed-carbon h |
| Promoted integrated proxy, 25–585 h | 219.8266193204 feed-carbon h |
| Promoted/reference | 1.8944822565 |
| Ratio after charging 5% additive mass | 1.8042688157 |
| 2–585 h missing-selectivity ratio bounds | 1.7388324308–1.9731815849 |
| Same bounds after charging additive mass | 1.6560308865–1.8792205570 |

The startup construction is correct within the interpolation model. Reference conversion integrated over 2–25 h is 14.9829116000 h; observed promoted conversion-times-selectivity over 5–25 h contributes 7.9919146215 h; promoted conversion over the unknown-selectivity interval 2–5 h is 1.1399773500 h. Bounding the missing selectivities by zero and one gives the stated numerator/denominator extremes without extrapolating selectivity.

The restricted-window crossing is 122.8630491 h. The unfavorable startup construction crosses at **194.3390992 h on the catalyst-mass basis**; instantaneous promoted advantage stays positive thereafter through 585 h. This is a missing-data construction, not an experimental uncertainty bound or a mass-charged crossover. The first two hours remain outside its claim.

The Figure 1 caption and Methods support equal nominal feed, 0.5 g catalyst in each arm and 0.025 g additional PDVB. Dividing the ratio by 1.05 correctly charges catalyst-plus-additive mass, while excluding quartz. Carbon-based selectivity is reported, but the SI hydrocarbon columns sum to 100% with CO2 listed separately. This supports retaining the explicit hydrocarbon-normalization caveat: `X × S` remains a reported-output proxy until the complete selectivity denominator and carbon closure are resolved. [Fang et al. 2026](https://doi.org/10.1038/s41467-026-76571-8), Fig. 1, Methods “Catalytic tests in FTS,” SI Table 2.

Three clarifications were incorporated:

- The 194 h crossover is explicitly the catalyst-mass comparison, since the surrounding text also discusses additive-mass normalization.
- The caption reports **±2% error bounds**. Their statistical meaning and temporal correlation are not supplied. Interpreting them as ±2 percentage points for an analyst-selected sensitivity case, shifting every promoted conversion/selectivity downward and every reference value upward gives a 25–585 h ratio of **1.60581**, or **1.52934** after additive mass. Reversing the shifts gives **2.24259**, or **2.13580**. These scenarios preserve the qualitative advantage but are neither confidence intervals nor rigorous uncertainty bounds.
- The main text states that the two beds had consistent volumes. Under that reported equality, the output ratio also applies per nominal bed volume within this experiment. Absolute bed volume, detailed packing and quartz inventories remain unavailable; broader process productivity remains unestablished. The revised note acknowledges the source's bed-volume control. [Fang et al. 2026](https://doi.org/10.1038/s41467-026-76571-8), Fig. 1 caption and following paragraph.

## Size discriminator

The spherical source balance, film term, centre coefficient `1/6`, volume-average coefficient `1/15`, and external-resistance fractions are correct. With constant Sherwood number, `k ∝ 1/R`, so external-only promotion can produce the same `R²` dependence as internal-diffusion promotion. This valid counterexample defeats identification by radius exponent alone without claiming that constant Sherwood number applies to the actual bed.

Both sets of componentwise inequalities correctly give sufficient exposure dominance at corresponding relative radii and in the volume average. They require matched bulk concentration, positive source strengths, the specified coefficient model and valid bounds on source-density and transfer changes. They need not hold to obtain dominance, and they cannot establish useful-output dominance. The note correctly requires a separate exposure-response link, controlled histories and measured useful output.

The proposed smaller-unpromoted versus original-promoted substitution is a useful conditional formulation decision. The stronger prediction remains contingent on independently obtaining relevant coefficient bounds; no numerical size target follows yet. SI Table 4 confirms the prior size screen used 1.0 g PDVB per 0.5 g catalyst and reports conversion at 36 h. Its results cannot identify the transport coefficients or validate the low-dose, late-addition challenge. No algebraic correction or additional literature was needed.
