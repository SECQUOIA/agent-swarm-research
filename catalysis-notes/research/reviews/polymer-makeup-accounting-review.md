# Independent check: Na makeup accounting and the coke proxy

2026-09-15. Review of [polymer makeup accounting](../calculations/polymer-makeup-burden.md) and [the oxygenate/coke boundary](polymer-coke-proxy-boundary.md), following the [exposure falsifiability review](polymer-exposure-falsifiability.md). No experiments were performed.

**2026-09-16 update:** the [post-upload audit](post-upload-polymer-audit.md) verified the published Science Figure 4B schedule: 0.4 g Na solid once before charge 2, three charges total. Thus `Σm_i = 0.4 g`, `ΣY_i = 3fY0`, and the general equation below gives `B = 0.8 × 3f / 1.2 = 2f`. The earlier `1.5f` three-charge result remains correct only for its explicitly hypothetical addition before *both* later charges. It is no longer the primary published comparator. Moodley's uploaded original Figures 5–6 were also checked, preserving the coke qualification below. No experiments were performed.

## Accounting: correct with the stated boundaries

For `n` equal polymer charges, the fresh-recipe comparison supplies `0.8n` g solid and yields `nY0` accepted polymer-derived product carbon. Its product per supplied solid is therefore `Y0/0.8`. The retained-mixture policy gives

`B = 0.8 ΣYi / [Y0(0.8 + Σmi)]`.

With the explicitly hypothetical addition of `0.4` g Na-containing solid before each charge after the first, supplied mass is `0.8 + 0.4(n−1) = 0.4(n+1)` g. Substituting `ΣYi = nfY0` gives `B = 2nf/(n+1)`. Independent exact-fraction checks at `n = 1, 2, 3, 10` agree. At `f = 1`, three charges give `1.5`, and the large-`n` limit is `2`. The threshold `f > (n+1)/(2n)` for `B > 1` is also correct.

No correction to the equations is needed. The note correctly avoids claiming that the actual patent used this makeup mass, that this policy defines a universal upper bound, or that W turnover measures polymer-carbon recovery. In particular, the factor-two limit assumes unchanged mean output. It is not a bound when `f` changes, the makeup schedule changes, or regeneration replaces fresh solid.

Three implementation details should remain explicit:

- **Equal input is not equal output.** For `f < 1`, the retained policy produces less accepted output after the same `n` charges. `B` still compares material productivity correctly, but does not establish equal production, cycle time or reactor capacity. A fixed-output comparison would require the actual additional operating history needed to reach that output.
- **Nominal retained catalyst mass is not total physical solids.** `0.4(n+1)` g is the retained mass of supplied catalyst on the assumed loss-free charge basis. Deposits, residual polymer and chemical mass changes can alter the measured total solids. Keeping this distinction does not change the fresh-solid denominator.
- **Count accepted carbon once.** If unconverted polymer carries across cycles, sum accepted product leaving the defined process boundary, with final inventories accounted for; do not sum overlapping conversion estimates. Ethylene-derived product carbon must remain separate or be allocated by a validated balance. The symbolic `Yi` definition provides this requirement, not its experimental solution.

The note's proposal to record actual additions, retained inventory and complete cycle time is appropriate. Nothing in this algebra establishes an optimized catalyst loading, relative solid costs or a practical advantage.

## Coke note: primary-text check

Independently read exposed original methods/results on the [author-uploaded Moodley et al. page](https://www.researchgate.net/publication/254787291_Coke_formation_on_WO3SiO2_metathesis_catalysts), DOI [10.1016/j.apcata.2006.10.053](https://doi.org/10.1016/j.apcata.2006.10.053). Sections 2.2 and 3.4 support the stated once-through conditions, continuous 100 ppm additions, negligible incremental activity loss and approximately halved coke with 2-pentanone over 72 h. They explicitly distinguish ordinary activity decline from an oxygenate effect and report diminished coke suppression on returning to pure feed. Section 3.3 supports the qualified description of carbon maps; it does not independently count working sites. Figures were not visually checked by the original reviewer; the 2026-09-16 audit subsequently checked the uploaded original Figures 5–6.

One prior-art qualification deserves emphasis: p.159 already proposes relaxing oxygenate feed specifications to reduce extraction intensity. Thus, that broad practical motivation is also established. The surviving new claim concerns prediction in the coupled Na/W polymer reaction.

Do not turn the separate long recycle experiment into a precise durability benchmark: the exposed prose calls it 814 h but also discusses decline around 540 h and termination, without resolving the chronology. The root note wisely gives no exact stable-life claim. Its conclusion that less coke does not establish better tandem output is supported.

## Disposition

Both root notes are sound. The suggested refinements are wording and scope clarifications; they do not change the retained bounded-study recommendation. No new source was added, no KB files were changed, and no maintenance was run. Moodley intake has since completed; its original is locally available.
