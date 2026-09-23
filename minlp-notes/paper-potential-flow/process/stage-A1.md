# A1 implementation record

Status: in progress; implementation and checks complete, lead review pending. No later section was implemented. No changes were staged or committed.

## Sources read

- Scaffold: README, conventions, A01 coverage assignments, macros, process table, section labels, and build/coverage checkers.
- Research context: relevant model, aggregation, continuity, and output passages in `results/potential-flow-cactus-square-root-sum.md`, `results/potential-flow-cactus-additive-optimization.md`, `results/potential-flow-bounded-block-rank.md`, `results/fixed-core-block-polyhedral-optimization.md`, `notes/potential-flow-complexity-map.md`, and the generic cycle-routing code in `code/potential_flow_mpd/pbflow.py`. The new checker imports none of that code.
- Classical local fulltexts and metadata: Birkhoff–Diaz (1956), Sections 2–5, especially Theorems 2′/3′; Duffin (1947), especially Theorems 1–3; Minty (1960), resistor definitions, Theorem 6.4, Theorem 8.1 and its corollary. PDF text extraction recovered the Birkhoff–Diaz formulas omitted by the Markdown extraction.
- Arithmetic local fulltexts and metadata: Etessami–Yannakakis (2010), Section 1 and the SRS definition in Section 3; Allender et al. (2009), Theorem 1.4/Corollary 1.5 and counting-hierarchy discussion; Blömer (1991), Sections 1–2 and 7; Renegar (1992), Part III, Theorem 1.1 and Proposition 2.3; Basu (2014), Sections 2.1, 2.5.1, and Theorem 2.27 in Section 2.5.2. The Basu theorem's displayed bounds were checked using PDF text extraction. Basu–Pollack–Roy (2006), Chapters 2, 10, and 14, was added in round 1; its PDF verification is recorded below.
- Five new bibliography entries transcribe the corresponding `paper.md` front matter: Allender, Blömer, Renegar, Basu (2014), and Basu–Pollack–Roy (2006). Existing entries supply the other citations. Basu remains an arXiv preprint; the Renegar title identifies Part III.

## Clarifications and corrections

- No extra growth or surjectivity hypothesis is needed for existence. The proof supplies a uniform bound `E(x) >= a ||x||_1 - C`, which proves bounded sublevel sets, rather than relying only on growth along individual rays. Bounded laws are explicitly allowed.
- Made the graph loopless, allowed parallel edges explicitly, treated a parallel pair as a length-two cycle, and excluded edgeless blocks. These conventions resolve the incidence-column and singleton-graph cases; `conventions.md` was updated too.
- Corrected “cacti have block rank 1” to “at most 1, with equality when cyclic,” since trees are cacti. Retained the packet's corrected total-rank implication and nonbridge restriction on the degree bound.
- Aggregation uses components after deleting a block's edges, so a cut vertex's own nomination is counted once for that block. “Chord” in the cycle lemma means a designated existing cycle edge relative to its spanning path. The parallel example specifies its orientation and which edge carries `q`.
- Computational domains are nonempty compact rational domains with positive resistance lower bounds. A continuity argument establishes attained extrema and density establishes rational near-optimizers on these unfiltered domains. Arbitrary continuous laws are not assumed finitely encoded or to produce algebraic outputs.
- Duffin's existence theorem is stated for continuous, two-sided unbounded conductivities, not the present unrestricted resistance-variable model. Birkhoff–Diaz's primitive-coercivity hypothesis is verified directly; Minty's relation-based hypotheses are described separately.
- Allender's SRS inequality is `>=`; the text explains conversion to the required weak `<=` convention, including polynomial-time equality testing for positive integer radicands using the radical independence in Blömer's Theorem 4. Blömer's randomized field-membership/zero test is not presented as a sign algorithm.
- Renegar's local package is Part III; Proposition 2.3 supplies the decision bound used. Basu's Theorem 2.27 supplies arithmetic counts, output degrees, and intermediate/output coefficient bits. Zero free dimension is handled by a dummy variable; fixed dimension and dense numerical degree are explicit. No unverified source theorem is used as a substitute for a structural proof.

## Checks

- `python3 paper-potential-flow/verification/check_a1_preliminaries.py`: passed, 22,236 assertions; 24 glued graphs with 222 blocks and nonzero balanced nominations, singleton/bridge cases, one separate zero-nomination cycle, 30 cycle brackets, and five exact Fraction parallel identities. Maximum numerical error was `1.103e-28` against `1e-9`. The 60-digit whole-graph energy solver takes no block information; Tarjan decomposition, component aggregation, local solves, and all-pairs block paths are checked separately. All four generated graphs containing a rank-two block now use nonzero nominations and exercise coupled cycle minimization. Numerical checks supplement the proofs; they are not formal certificates.
- `python3 paper-potential-flow/verification/build_and_check.py`: passed for both manuscripts; no undefined references/citations or duplicate labels. Both manuscripts have zero overfull boxes; `verification/build-report.json` records the final results.
- `python3 paper-potential-flow/verification/check_coverage.py`: passed, 308 inventory files and 18 planned sections.
- `git diff --check`: passed. `git status --porcelain`: all changes are unstaged and under `paper-potential-flow/`.

## Round 1 accepted fixes

- A1-01/03/08: the affine matrix is `M`, thresholds are `gamma`, additive value endpoints are underlined/overlined `v`, and polynomial counts are `sigma`; the table and shared affine convention agree. To avoid further collisions, the free-variable count is `nu` (reserving `ell` for nomination bounds), and the defining polynomial is `P_alpha` with endpoints `eta_-`, `eta_+` (reserving `P` for the parameter polytope). The parameter polytope has an explicit rational linear constraint list.
- A1-02/09/15/17: homogeneity now covers symmetric and asymmetric quadratic laws. Added `lem:a-pre-attainment`, defined coefficient-dependent primitive energy before use, and cited the lemma for optimum attainment and rational near-optimizers. The cycle lemma covers all general laws using their signed limiting ranges. The bounded-law example now has two parallel edges with laws `arctan` and `2 arctan`; its strictly increasing cycle equation has opposite limiting signs for every real through-flow.
- A1-04/10: added complete proofs of the block incidence tree and cactus block characterization, and a direct branch-set proof excluding a `K_4` minor in `K_{2,k}`. The rank-sum proof cites the incidence lemma. Block aggregation now uses the external-path/cycle contradiction with unique edge-block membership.
- A1-06/07/11/13: clarified the rank-deficient multiplier argument, Duffin's onto-law applicability, and Minty's real-resistor branch uniqueness. Renegar now uses “consistent sign vectors” and identifies the Part I proposition restated in Part III.
- A1-05/12/16: replaced the incorrect Basu 2014 Section 2.1 root locator by the verified book chapters; retained Section 2.5.1 for sign determination and Theorem 2.27 for bounds, identifying the latter as a restatement of the book's quantifier-elimination theorem.
- A1-14: moved the zero-nomination cycle regression outside the random-trial loop and ensured every generated nomination is nonzero and balanced. The numerical solver itself is unchanged.
- Clarified the coefficient of each occurring square-free radical and justified counting-hierarchy closure from the iterated-PP definition. Fixed the display/prose line break and used `citet` after “described in.”

### Locator verification in round 1

- Ran `pdftotext` on the Basu–Pollack–Roy `original.pdf`, both with and without `-layout`. Its custom font encoding corrupts even the table-of-contents text, so extraction alone could not verify the locators. Rendered and visually read PDF contents pages 3, 6, and 7 instead: Chapter 2, “Real Closed Fields,” contains real root counting and Sturm's theorem; Chapter 10, “Real Roots,” contains isolation and sign determination; Chapter 14 is “Quantifier Elimination.” Also visually read pages 370–371 (rational isolating intervals), 393 (sign determination), and 407 (Thom encodings). The manuscript uses chapter-level book locators, with no new book theorem number. The bibliography fields come only from the package's `paper.md` front matter.
- Basu (2014) fulltext Section 2.5.2 explicitly assigns Theorem 2.27 to reference [25]; the bibliography identifies [25] as the 2006 second-edition book. The displayed bounds remain those verified in the first implementation.
- Renegar's local fulltext immediately before Part III Proposition 2.3 says it restates Part I Proposition 4.1, and the proposition uses “consistent sign vectors.”
- Minty's fulltext gives Definition 5.2's no-horizontal/no-vertical-segment meaning of “real resistor,” Theorem 6.4 with Corollary I, and the existence corollary after Theorem 8.1. The PDF page 203 was also inspected; its scan clips part of the left margin, so the definition and branchwise theorem supply the complete reading.
- Allender et al. Section 4 recalls the hierarchy `PP, PP^PP, ...` and points to Wagner [66], “The complexity of combinatorial problems with succinct input representation” (1986), and Torán [64], “Complexity classes defined by counting quantifiers” (1991). The manuscript cites this pointer and gives the short next-level oracle argument for closure; it does not claim to have read those two referenced papers.

All three required checks were rerun after the round 1 manuscript and checker changes and passed with the counts above. `git diff --check` passed; all work remains unstaged under `paper-potential-flow/`.

## Round 2 accepted fixes

- Completed the noncut-vertex argument in `lem:a-pre-incidence`: every edge incident to a vertex belonging only to `H` lies in `H`, so paths through that vertex can be rerouted through connected `H-v`.
- Renamed the square-free integer to `f`, the incident-block count to `rho`, the cycle's spanning-path flow to `lambda`, and the algebraic isolating-endpoint bit length to `kappa`. Updated the notation table. The complexity-bound function formerly written `f(k)` is now `varphi(k)`, avoiding a new collision with the requested square-free integer `f`.
- No theorem hypotheses, citation locators, or numerical solver code changed in this round.
- Verification: `rg` confirmed the renamed symbols are used consistently in the section. `python3 paper-potential-flow/verification/build_and_check.py` passed for both papers with zero overfull boxes and no reference/citation errors; it refreshed the generated build report. `python3 paper-potential-flow/verification/check_a1_preliminaries.py` passed all 22,236 assertions, with maximum numerical error `1.103e-28`. `git diff --check` passed. `git status --porcelain` shows only unstaged changes under `paper-potential-flow/`; the earlier A1 changes remain present.
