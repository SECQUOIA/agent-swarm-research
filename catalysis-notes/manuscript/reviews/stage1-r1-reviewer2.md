# Stage 1, round 1 — independent reviewer 2

**Verdict: accept with minor revisions. No major issue identified.**

The proposed late-addition experiment has a defensible causal target: the effect of the complete PDVB formulation on the fractional functional penalty of an imposed water disturbance after a common conditioning and handling protocol. The independent-charge, blocked 2×2 design, time-matched shams, absolute rates, and cumulative output endpoint make this substantially clearer than a comparison of normalized deactivation curves. The text correctly limits the interpretation to formulation function and does not claim to count surviving sites. Its handling and challenge qualifications are legitimate proposed experiments; their results need not exist before accepting the research proposal.

The identifiability argument is correct within its stated assumptions. Summing the two pool balances produces the stated aggregate outlet dynamics, while redistributing capacity changes the source-pool concentration. This is a constructive counterexample to guaranteed local identification, not an assertion that every possible experiment is nonidentifying. The reversible predictive branch also keeps an appropriate separation between empirical prediction, transport coefficients, and a damage law. The held-out pulse on independent charges is a concrete prospective test.

The original contribution is appropriately narrower than physical hydrophobic promotion: a boundary for addition after common conditioning, plus conditional prediction of useful function under another disturbance history. Fang 2022 already supplies mixing, water-cofeed, and additive-removal precedents; Hanssen 1997 supplies water-history and dry-return precedents. Those do not, on the evidence reviewed, eliminate the specific proposed combination. The importance is credible as a formulation decision and limitation study, with commercial and microscopic claims explicitly reserved. A broader materials campaign or an isotope campaign is not necessary to make this proposal valid.

## Minor issues requiring clarification

1. **Define how the common conditioning endpoint will be selected and fixed.** Location: `manuscript/sections/01-water.tex:48`, with the novelty statement at line 20 and the state-specific interpretation at line 89; corresponding evidence claim: `manuscript/evidence/stage1-water.md:39`.

   “Conditioned under the same schedule” leaves the defining pre-intervention state less concrete than the later challenge protocol. This matters because late addition is the principal new intervention: addition after a few hours of startup and addition after established wax-bearing operation answer different questions. Independent charges and common handling address assignment and recovery, but do not define which operational age the result represents. The existing text properly avoids equating common history with identical microscopic state; no new structural characterization is required to fix this omission.

   **Remedy:** state that the parent pilot will select a fixed pre-intervention time and feed/temperature/pressure schedule before the comparison, using a stated observable criterion for being past startup (for example, a predefined rate/selectivity drift tolerance over a defined window). Freeze that same duration for all comparison charges, report pre-handling rates and retained-liquid observations, and describe the resulting rule as applying to that operational age. The proposal need not invent a numerical stability tolerance before obtaining pilot variability.

2. **Make the diluent-replacement operation compatible with whole-charge recovery.** Location: `manuscript/sections/01-water.tex:48` and `manuscript/sections/01-water.tex:64`.

   The manuscript sensibly rejects assuming that wax-bearing catalyst can be pooled, homogenized, and repartitioned with known catalyst mass. It then says to recover the complete catalyst zone while preserving liquid and to add PDVB by replacing a measured volume of diluent. If the conditioning diluent is already intimately mixed with the recovered catalyst, selective removal can reintroduce the solid/liquid separation problem that the independent-charge design was intended to avoid. The text does not establish that this is the intended arrangement, so this is an operational ambiguity rather than evidence that the experiment cannot work.

   **Remedy:** specify the initial and final packing arrangement. One simple option is to condition identical catalyst zones without the replaceable internal diluent, recover them whole, and add either the measured PDVB dose or its quartz volume control when repacking to the same final bed volume. Another is to keep the replaceable diluent physically recoverable separately during conditioning. Whichever route is chosen, apply it identically to all four arms and include its solid/liquid recovery in the already proposed handling pilot. No additional experimental branch is needed.

## Evidence checked and limits

- Read `literature/AGENTS.md` before consulting the library; did not modify the library or read other reviewers' reports.
- Reviewed `manuscript/sections/01-water.tex`, `manuscript/main.tex`, `manuscript/references.bib`, and `manuscript/evidence/stage1-water.md` in full.
- Consulted the local Fang 2022 full text, especially mixing, additive removal, and water-cofeed descriptions, and the Fang 2026 full text, especially the separate-granule catalytic protocol, reduction/passivation description, transient method, and distinct imaging geometry.
- Checked Hanssen 1997 original PDF p.3 directly: water starts after 24 h, continues for 24 h, and is followed by another 24 h with dry feed. The [publisher record](https://www.sciencedirect.com/science/article/pii/S0167299197804077) also confirms the pretreatment and cofeed precedent.
- Checked Wolf 2019 original PDF p.7 directly: its pressure schedule and maximum water/H2 ratio of 5 support the manuscript's refusal to transfer a damage threshold to the proposed ratio of 0.4.
- Checked Brandani's original title/abstract and local full-text balance and experimental discussion. Its passive silica-gel procedure supports the methodological precedent, not transfer of coefficients to the reacting cobalt bed.
- A focused web search for PDVB addition to spent cobalt catalysts surfaced the existing [Fang 2026 platform](https://www.nature.com/articles/s41467-026-76571-8), without a closer late-addition counterpart. This is a scoped originality check, not proof of exhaustive novelty.

I did not independently reconstruct the published source-data integral. The chapter labels it an output proxy and states its material limits; the central proposed causal comparison does not depend on that exact ratio. No material issue was found in the mathematical balances, source-dominance arithmetic, or stated basis of the gas-demand estimate.
