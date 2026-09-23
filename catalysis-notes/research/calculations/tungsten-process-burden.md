# What tungsten retention would have to improve

2026-09-16. Process accounting for the [coordination and tungsten-retention program](../working/program-development/oxygenate-program-alternative.md). These are balance equations and comparison requirements, not a techno-economic result or experimental demonstration. No tungsten price, separation energy, industrial performance or catalyst lifetime is assumed.

## Prior art changes the comparator

[WO2022066160A1](https://patents.google.com/patent/WO2022066160A1/en), description paragraphs 073–075, discloses 200–1500 mg W/L operation, varying or ceasing W addition to dissolve deposits, and optional pH changes. It identifies deposition on the hydrogenation catalyst as a potential burden. Consequently, feed interruption, a dissolving reservoir, and lower soluble-W concentration are established proposed operating strategies. The inspected description contains no labeled working examples or numerical experimental tables. Its cumulative-conversion and duration requirements are disclosures, not an independently documented performance series.

[US12297166B2](https://patents.google.com/patent/US12297166B2/en) discloses ion-exclusion recovery of W from an organic-rich stream after glycol separation, water addition when needed, and optional treatment to restore useful catalyst species. Its stated recovery ranges are not accompanied by a working-example series in the inspected description. This is a relevant process alternative, not verified economics. Lowering W concentration need not eliminate processing of the organic stream or its water-removal duty.

These conclusions come from the complete public descriptions retrieved on 2026-09-16. They do not assess every patent-family member or incorporated reference. The sole literature agent has these sources in its intake queue. Local temporary inspection copies are `/tmp/tungsten-process-audit/WO2022066160A1.html` and `US12297166B2.html`; canonical links above are the durable references.

An experimentally supported retained-W comparator is also necessary. The now-read [Li 2020 main original](https://doi.org/10.1021/acssuschemeng.0c00836) reports Ti–O–W stabilization and seven recycling runs with filtration, water washing and air drying between runs. Its SI Tables S2–S3 include preleachate and soluble-AMT controls. Soluble-W recovery and supported-W retention should both compete with a new proposal; neither should be handicapped by choosing an unnecessarily poor implementation.

### Newly available Li 2020 data: concentration is not inventory loss

Figure 4b (PDF p. 6, visually checked) labels postreaction W concentrations of 28, 22, 19, 21, 18, 20 and 19 ppm across seven runs. Their sum is 147 mg/L if ppm is interpreted as mg/L for these dilute aqueous liquids. The nominal initial W inventory from 0.15 g catalyst at 20 wt% W is 30 mg. Applying the methods' 40 mL charge to each concentration gives 147 × 0.040 = **5.88 mg W**, or **19.6% of nominal initial W**, across seven runs. This is a conditional scale check, not a closed balance: actual recovered liquid volumes, sampling, wash liquors, support loading basis and solid inventories must be measured.

The original contains a consequential inconsistency: methods and Table 1 specify 40 mL water (pp. 2, 4), but the Figure 3 caption specifies 100 mL (p. 5). Using 100 mL would give 14.7 mg W, or 49% of nominal W. Neither branch should be selected silently or quoted as measured cumulative loss. The source's characterization of the leaching as negligible is not justified by ppm values alone. At minimum, the new information makes cumulative export worth checking; it does not establish an economic bottleneck or an anchor modification that resolves it.

## Keep four quantities separate

A subsequent [working-example audit](tungsten-ash-recovery-comparator.md) finds actual recovery and catalytic-use experiments in **WO2022064039A1**. That evidence is stronger than the untested recovery ranges above: selected ash from a model waste is processed and the recovered W functions in a product-rich continuous sugar reactor. The short trial does not establish an overall recycle fraction or economics. Preserve this source distinction when defining the soluble-W reference.

Choose and draw a fixed process boundary. Let P be saleable EG output in kg/h, Q the liquid flow crossing the selected outlet in L/h, and C_W the total measured W concentration in that stream in g/L, including whatever dissolved and colloidal fractions the stated assay recovers. The gross export from that boundary per product is

\[
E_W=Q C_W/P \quad [\mathrm{g\ W/kg\ EG}].
\]

For a solid-retaining reaction zone, this quantifies W exported in the selected outlet. Net accumulation or loss requires subtracting returned W and counting other streams. It does not count rapid release and return within the zone, or establish which population performs turnover. For a separator boundary, use the actual separator feed after direct recycle splits. Repeatedly counting a large internal recycle as fresh loss would be wrong. Report particulate attrition separately when the analytical fractionation permits it.

If a fraction η of this stream's W is recovered and actually returned across the same boundary, after separator, purge and regeneration losses, with no other outlets and constant total inventory, the fresh makeup requirement is

\[
M_W=(1-\eta)E_W.
\]

This restricted balance is useful for interpreting an experiment, not for assuming an actual recovery yield. With multiple outlets, accumulated deposits, retained inventory changes or additional W inputs, use the full balance:

\[
\dot m_{W,\mathrm{fresh}}+\dot m_{W,\mathrm{other\ inputs}}
=\sum\dot m_{W,\mathrm{unreturned\ outputs}}+dI_W/dt.
\]

Internal recycle cancels. Recoverable W inventory is distinct from active W inventory: a recovered inactive species still closes the elemental balance but may require treatment before it restores output. Measure productivity after recovery rather than multiplying elemental recovery by an assumed activity factor. If an inactive fraction accumulates, include it explicitly in the inventory and purge balance.

For a finite campaign, also report initial W charge, later fresh additions, final reusable inventory and unrecovered W per cumulative saleable EG. Dividing only later makeup by product hides the startup charge; counting all final reusable W as irreversibly consumed overstates loss. Inventory commitment and consumption are different burdens.

The remaining two quantities are recovery duty and output. At minimum measure liquid volume sent to recovery, elution/wash water, reagent demand, returned catalyst activity, off-spec product, hydrogenation-catalyst replacement, and downtime per EG output. Full catalyst/support and hydrogenation-metal inventories matter alongside W. A more strongly anchored catalyst could lower export while requiring more catalyst volume or losing EG productivity.

## Useful comparisons without invented economics

For baseline B and candidate A, if the simple constant-inventory balance applies,

\[
\frac{M_{W,A}}{M_{W,B}}
=\frac{E_{W,A}}{E_{W,B}}
\frac{1-\eta_A}{1-\eta_B}.
\]

Thus a lower export is not automatically lower makeup when the architectures have different recovery fractions. A purely illustrative counterexample: reducing export tenfold while discarding all exported W uses more fresh W than a baseline that recovers 99% of its export. These numbers are chosen to explain the equation; neither is a measured performance claim. Conversely, eliminating a recovery step or avoiding hydrogenation-catalyst fouling can be valuable even when tungsten purchase savings are small.

At matched EG output and yield, compare at least these architectures:

| Architecture | Burden it could reduce | Burden that must still be measured |
|---|---|---|
| Supported W retained in the reactor | Net metal export and possibly recovery demand | Catalyst volume, working-state drift, hot export, attrition, regeneration and replacement |
| Low-concentration soluble W with recovery | Required dissolved inventory and fresh makeup | Recovery feed volume, water/reagents, returned function, fouling and purge |
| Solid reservoir with useful local release/return | External W circulation while retaining flexible coordination | Same process quantities, plus whether the reservoir depletes or changes selectivity |

The third architecture is not a failed heterogeneous catalyst by definition. If useful output is sustained and W export is small, it may be an effective process even when permanent atomic attachment is unproven. Its novelty must lie in a new predictive chemical relationship or consequential improvement beyond the existing reservoir and cycling disclosures.

## First practical decision

Establish which unresolved burden limits the best accessible reference: declining useful productivity, W makeup, loss of hydrogenation function, or actual recovery duty. Then report the new coordination/anchoring intervention against that burden over the same output horizon. A mechanistic result can warrant publication and further study without a demonstrated process advantage; describe that narrower contribution honestly.

Do not claim a separation benefit solely from lower effluent W concentration. Do not claim a lifetime benefit from a few recovered batches without the lost material, recovered function and elapsed operating time. Do not require a complete plant model before testing a consequential chemical hypothesis: these balances identify the measurements that make later practical claims credible.

Independent review checked the equations, units, illustrative counterexample and patent-description scope; its corrections to gross versus net flow and effective return fraction are incorporated. See the process-accounting addendum in the [tungsten program review](../reviews/tungsten-sugar-program-review.md).
