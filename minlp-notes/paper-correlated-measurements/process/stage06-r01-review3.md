# Stage 6 integration review 3

## Recommendation and findings

Accept this integration stage. I found **no major issues and no minor issues requiring correction** in the material reviewed. This recommendation concerns Stage 6 integration; it does not replace the required independent whole-manuscript review.

## Scope and checks

I read the Stage 6 author report; the complete new abstract, introduction, contribution table and assumptions roadmap; the complete discussion and conclusion; `main.tex`; the root README and relevant supplement README/validation entry points. I checked the integration against the all-split, robust and separator definitions, propositions, proofs and attribution passages in Section 5 (`sections/04-certification.tex`), and against the corresponding reported computations in Section 6 (`sections/05-computation.tex`). I also inspected the source-version record and the specific primary literature below. No frozen source or scientific artifact was changed.

### Relaxation-family comparisons

The abstract, contribution table and introductory roadmap are consistent with Proposition `prop:diagonal-barrier`. The witness uses one common fractional point and weak PSD duality, and the affine cuts retained are globally valid upper supports of the specified virtual-noise family. The introduction does not turn this into a result against arbitrary cutting planes or integer branch-and-bound. The discussion explicitly excludes branching and cuts outside the family, and states the lack of universal dominance.

I checked the quantifier direction in the proof: a feasible common point whose value is bounded below for every split survives every intersection of those upper supports; its value can therefore be compared with a separately certified upper bound on the integer optimum. No unjustified minimax interchange is used. The ten scalar comparisons and single diagonal comparison in the integration match the scope of the computational section. The negative complete-packet examples remain visible rather than being displaced by the positive comparisons.

### Robust normalization

The introductory claim is an explicit finite-scenario certificate with uncertainty in scenario optima, rather than a claim to invent standardized maximin design. The individual-optimum interval substitution is in the correct direction: upper normalizers give the incumbent lower bound, lower normalizers give the global upper bound. The common support prices one complete feasible schedule over all scenarios. Both the introduction and discussion retain the restriction to a declared finite set; neither infers continuous-parameter robustness.

The discussion's statement that shared prices improve separate caps is supported by the computational paragraph giving negative shared upper bounds after the reference-only zero cap. It does not confuse the numerical fixed-offset comparison with the exact unknown-optimum standardized objective.

### Anchor hierarchy

The integration matches `thm:separator-hierarchy`: the ordering is for nested anchor sets and the same complete feasible schedule family, using Schur elimination of the removed nuisance variables before applying matrix concavity. It does not claim that arbitrary block sizes, nonnested partitions, unfinished solver values, or independent expected-count mixtures inherit this order.

The introduction and discussion retain both important endpoints: the no-anchor information hull can have an integrality gap, and the all-anchor physical-nugget split need not dominate a tuned scalar split. The strict eight-time study has disjoint certified mixture intervals on a common set of 56 schedules. The discussion's 192-point cost statement matches the reported best separator row: its log gap is about 0.1573, while accounted total cost is 38.023 seconds and hence exceeds the nominal 30-second allowance. No unqualified speedup or universal superiority claim is introduced.

### Prior-work checks

- I read the local Hainy–Müller–Pázman preprint's Proposition 3 and Section 4.4. The equivalence and simplicial-decomposition attribution in the introduction is accurate.
- I read the local Sagnol–Harman 2015 primary reprint's subsystem criterion and Theorem 4.3/Corollaries 4.4–4.5. Its general information atoms, subsystem criterion and conic formulations substantiate the explicit inherited side of the contribution table. The manuscript maps its Schur criterion to that existing framework rather than presenting a new general design criterion. Primary metadata also agrees with the [author's publication page](https://www.zib.de/userpage/sagnol/publication/sh15_aos/).
- I read the local Maus et al. 2010 full text's model, correlation-uncertainty motivation and relative-efficiency discussion. Its role as a predecessor for robust design under uncertain temporal correlation is correctly retained.
- I inspected the [Chowdhary–Attia–Alexanderian primary v2 text](https://arxiv.org/html/2409.09137v2), including its correlated-covariance, exact-budget experiment. The manuscript's technical attribution to robust correlated-noise sensor design is appropriate; the integration does not make a first robust-design claim.
- Targeted primary-source searches also located and I inspected the nested-bound construction in Uddin et al., [*Nested performance bounds and approximate solutions for the sensor placement problem*](https://www.cambridge.org/core/journals/apsipa-transactions-on-signal-and-information-processing/article/nested-performance-bounds-and-approximate-solutions-for-the-sensor-placement-problem/F391F848E287F43A23700229986DAD8C), Section IV.C, Theorems 2–3. That hierarchy relaxes some coordinate selections to orthonormal measurement directions and uses generalized-eigenvalue bounds. It is a different construction from changing latent Markov-anchor representations. The present qualified, specific hierarchy claim does not assert the first nested sensor-placement bound generally, so this source does not expose an unsupported priority claim or require broadening the manuscript's citation list.

### Integration and presentation

The statistical model, feasible-design certificate and determinant-root efficiency interpretation are introduced before the detailed results. The contribution table separates inherited mechanisms from the developments actually proved. The roadmap preserves fixed dimensions, explicit rational feasibility representations and additive atoms; the discussion explicitly distinguishes the large theoretical PSD covers from the numerical prototypes. The document is broad, but its organization and repeated scope distinctions make the breadth understandable rather than contradictory.

The root README matches the standalone manuscript and supplement structure and distinguishes internal review records from external peer review. The availability paragraph and validation entry point agree on the stated source-ranking and certificate checks. I did not rerun the numerical suite, inspect every archived witness, prove all approximation/locality theorems from scratch, or independently rebuild the PDF in this integration review. Those tasks remain subject to their stage evidence and the separate final review. The bounded literature search supports a carefully qualified comparison, not an exhaustive proof of priority.
