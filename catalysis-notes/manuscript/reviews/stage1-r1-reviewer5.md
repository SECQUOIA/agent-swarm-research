# Stage 1, round 1 — independent reviewer 5

**Verdict: accept with minor revisions. No major issue identified.**

This is a coherent proposed research program, rather than a claim to have completed experiments. Its strongest feature is the separation of formulation performance, prospective functional prediction, and local mechanism. The late-addition comparison has independent charges, matched handling, time-matched controls, an explicit interaction endpoint, and a separate cumulative-output decision. The transient counterexample correctly establishes a limitation of outlet measurements without pretending to describe the actual PDVB microstructure. Experimental contingencies are identified as qualification decisions; they do not require invented results or arbitrary numerical thresholds to make the proposal valid.

## Major issues

None. I found no error that materially invalidates the proposed comparisons or leaves the core program incomplete.

## Minor issues

1. **Define the intended conditioned state more concretely.** `manuscript/sections/01-water.tex:48` says that charges follow the same conditioning schedule, but does not state how that schedule is selected or what qualifies the material as conditioned. This matters because late intervention is the main distinction from prior work, and material still undergoing its original startup would support a narrower interpretation. State the planned conditioning atmosphere and a pilot-selected duration or observable acceptance criterion, then freeze that schedule across randomized charges. A criterion based on sufficiently reproducible rate/selectivity and water or liquid-inventory behavior would be useful; perfect microscopic stationarity is neither necessary nor realistic. The existing acknowledgment of state variability should remain.

2. **Give the reader one sentence of reaction context before the numerical comparison.** `manuscript/sections/01-water.tex:8–18` moves from syngas to CO conversion and C5+ selectivity without introducing the reaction or the product designation. For readers from other catalysis areas, explain that cobalt Fischer–Tropsch synthesis converts CO and hydrogen to hydrocarbons while producing water, and that C5+ denotes hydrocarbons with at least five carbon atoms. Define the selectivity basis when introducing the output proxy. This makes the importance of water and the reason for choosing useful-carbon output understandable without opening the cited papers.

3. **Make the two-pool concentration reference explicit.** `manuscript/sections/01-water.tex:34–40` gives a correct counterexample, but “its steady excess” does not explicitly identify the reference concentration. Write the result as `c_1,ss - c_g,ss = q_T/(lambda B_1)` and briefly define `q_T`, `c_in`, and `lambda`. The gas concentration also exceeds the inlet concentration by `q_T/F`; the stated threefold result applies to the pool-to-gas excess, not necessarily to the complete pool-to-inlet excess. This is a clarification of an otherwise valid argument, not a request for another model or experiment.

4. **Keep the concluding contribution at the scope of the proposed test.** `manuscript/sections/01-water.tex:103` calls the result “a controlled operating boundary,” whereas Experiment 2 selects one conditioned state and one challenge, and Experiment 3 validates a nearby reversible pulse. Those experiments can establish a controlled comparison and bounded applicability at the tested conditions; they do not locate an operating boundary across challenge severity, conditioning age, or dose. Replace “operating boundary” with wording such as “a controlled test of late low-dose PDVB under a specified disturbance.” No expanded parameter campaign is necessary.

5. **Complete two readily available bibliographic locators.** `manuscript/references.bib:25–29` omits the Paterson article's volume, although its local original identifies *Catalysis Today* **430**, 114559. `manuscript/references.bib:50–54` omits the Hanssen chapter's page range; the original runs from 193 to 202. The DOI links make both sources retrievable already, so this is a minor completeness issue. Add the verified metadata and verify the series volume before adding it.

## Evidence and presentation checks

I read `literature/AGENTS.md` before consulting local sources and made no knowledge-base changes. I checked the central Fang source passages on dose, granule configuration, catalytic conditions, activation, and water transients, plus relevant Hanssen, Paterson, and Brandani passages. The qualitative citations are appropriately limited; the evidence note explicitly discloses that the complete Sengupta original was not read. That disclosure should be preserved.

The self-contained calculation script reproduces 116.0352 and 219.8266 feed-carbon hours, a ratio of 1.89448, and an additive-mass-adjusted ratio of 1.80427. The manuscript reports these as a limited secondary proxy, which is appropriate. The low-conversion water-ratio and gas-sizing arithmetic is consistent with its stated assumptions.

I inspected the seven-page PDF's extracted text and rendered pages 3, 4, and 7, covering the equations, experimental table, and bibliography. Text and equations are legible, the table fits, links and reference numbers render, and the build log has no undefined-reference or overfull-box warnings. I found no PDF-readability issue requiring correction. `main.tex` does not introduce a substantive problem for this stage.
