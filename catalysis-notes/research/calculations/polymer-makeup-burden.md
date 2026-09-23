# What does retaining W save if Na must be replenished?

2026-09-15. Conditional material accounting for the [polymer exposure study](../reviews/polymer-exposure-falsifiability.md). This is an algebraic comparison, not a measured reuse result or economic estimate. An [independent review](../reviews/polymer-makeup-accounting-review.md) checked the algebra, source boundary and interpretation.

## Why this bound matters

The disclosed 1 g PE recipe uses 0.4 g W-containing solid and 0.4 g Na-containing solid. The uploaded Science main article now specifies the rescue schedule: 0.4 g fresh Na-containing solid before charge 2 only, with only PE added before charge 3 (Figure 4B and caption). This is a three-charge experiment, not an unspecified-dose rescue. Retaining W can increase W turnover while leaving substantial total solid demand. A useful exposure model should predict how much Na supplementation is needed, not merely whether supplementation restores output. [Primary accounting and source limitations](../reviews/polymer-patent-benchmark-accounting.md).

## Equal-feed comparison

Compare `n` equal polymer charges. Let `Y0` be accepted polymer-derived product carbon per fresh-catalyst charge, and `Y_i` the same quantity on retained solids in charge `i`. Let `m_i` be fresh Na-containing solid added before charge `i`, excluding the initial 0.4 g. Assume no additional W-containing solid and use fresh solid charged, including its support, as the denominator. Then

`B = [Σ Y_i / (0.8 g + Σ m_i)] / [Y0 / 0.8 g]`.

`B` is the ratio of cumulative product carbon per fresh solid supplied to that of using the original fresh recipe for each charge. It is dimensionless. A product specification and carbon attribution must be common to both cases. Externally supplied ethylene carbon must not silently inflate the numerator. Count accepted product leaving the boundary once, including final retained inventories; successive conversion estimates can double-count polymer carried between charges.

### Published three-charge schedule

For three 1 g PE charges, initial solids are 0.8 g and Na makeup is 0.4 g once, before charge 2. Thus total fresh solid supplied is 1.2 g, compared with 2.4 g for three fresh 0.8 g charges. With `f = ΣY_i/(3Y0)`,

`B = 2f`.

At unchanged mean accepted polymer-derived output, `B = 2`; beating the fresh-solid baseline requires `f > 1/2`. This is conditional material accounting using the **published mass schedule**, not a measured twofold economic gain. The Science plot shows similar supplemented cycle outputs, but does not by itself validate complete cycle-specific polymer-carbon allocation, retained inventories or cycle time. No indefinite repetition of this three-charge result is established. The visually checked original and source limits are documented in the [post-upload audit](../reviews/post-upload-polymer-audit.md).

### Separate illustrative policy

For an **illustrative, unmeasured policy** that adds 0.4 g Na solid before every later charge, define `f = ΣY_i/(nY0)`. Then

`B = 2 n f / (n + 1)`.

At unchanged mean accepted output (`f = 1`), three charges give `B = 1.5`; infinitely many charges approach `B = 2`. If output falls, beating the fresh-solid baseline requires `f > (n+1)/(2n)`. For three charges the mean accepted output must exceed two-thirds of the fresh baseline. These limits come from the assumed mass schedule, not from the published once-before-charge-2 rescue schedule. They are not limits on every possible supplementation or regeneration policy.

## What this comparison leaves out

Equal-feed material productivity does not establish equal accepted output or equal reactor capacity. Equal grams of the two solids need not have equal cost, embodied energy, preparation burden or disposal burden. The equation deliberately does not assign such equivalence. If Na can be restored with a smaller dose or a reagent, include the measured dose and other supplied materials in a separate, explicit accounting. If W is also replenished, its added mass enters the denominator. An unusually high initial laboratory catalyst loading must not be treated as an optimized process requirement.

Keeping all powders also increases reactor solids inventory. The illustrative policy leaves `0.4(n+1)` g nominal charged catalyst after `n` charges before any losses or withdrawal, even though each charge contains only 1 g new polymer. This is not total physical solids: retained polymer and deposits add further inventory. Mixing, contact, retained polymer and capacity may then change; the large-`n` algebra is not a physically validated operating limit. Withdrawal changes both the W and Na inventories and must be measured rather than modeled as selective removal of spent Na.

Product per supplied solid also omits reaction time, cooling, recharge, regeneration, ethylene consumption, feed preparation and product separation. A favorable `B` can coexist with worse useful throughput per reactor or greater overall resource use. These remain separate measured comparisons; no scalar commercial ranking is justified yet.

## Consequence for the first study

Use the published three-charge schedule as the clean makeup control. Record actual Na addition and retained-solid inventory along with carbon output and the full cycle time. Test one predicted dose or timing only after unequal component response transfers to the mixture. A source-specific exposure relation earns practical value if it reduces unnecessary makeup, identifies a useful feed limit, or shows that the proposed retention policy cannot meet the chosen output/material target. A high W turnover count alone does not answer any of these questions.
