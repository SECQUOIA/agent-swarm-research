# CIA reopening: literature boundary and practical opportunities

Date: 2026-09-06–07. Investigator: independent literature agent. This supplements [the earlier novelty audit](cia-novelty.md). It is a targeted primary-source review, not a proof of priority. The retained results have passed their separate independent mathematical and implementation reviews, linked below; this note audits source scope and the literature boundary.

## Main findings

1. **Support-preserving rounding with discrepancy at most one uniform grid interval is established.** Any new transfer from a continuous switching schedule to a grid should cite this ingredient and distinguish its additional switch-count conclusion.
2. **An exact graph algorithm for switching costs is established, but its general complexity grows exponentially with the mode count.** The proved linear-time one-switch specialization and fixed-budget algorithm have distinct complexity guarantees.
3. **A 2025 DP-inspired method explicitly lacks a general global-optimality guarantee.** It is a useful practical comparator, not a substitute for an exactness proof.
4. **Ordinary cumulative-error-to-state-error bounds are established.** A practical study should demonstrate actual state, objective, and constraint outcomes; simply substituting a new discrepancy coefficient into Gronwall's inequality is an application of existing theory.

## Support-preserving grid transfer: closest prior results

Bestehorn and Kirches, *The integrated control deviation of mixed-integer optimal control problems with vanishing constraints*, PAMM 20(1), e202000022, published online in 2021, [DOI](https://doi.org/10.1002/pamm.202000022), [open final PDF](https://d-nb.info/122645075X/34), pp.1–2. Corollary 2.7 on p.2 gives a binary rounding on an equidistant grid with integrated deviation at most the grid width `Delta`, satisfying `w[j,i]=1 => a[j,i]>0`. The proof uses bipartite matching. This is exactly the support-preserving approximation ingredient needed when the relaxed cell averages come from an existing continuous integer schedule. The article does not state a chronological-subsequence conclusion or a bound on the number of switches of that particular input-to-grid transfer.

The expanded manuscript, Bestehorn and Kirches, *Matching Algorithms and Complexity Results for Constrained Mixed-Integer Optimal Control with Switching Costs*, [open manuscript](https://optimization-online.org/wp-content/uploads/2020/10/8059.pdf), defines the support restriction in Definition 2.5, p.7. Theorem 4.4, pp.12–13, proves the same `Delta` guarantee with runtime `O(N M sqrt(N+M))`. Corollary 5.2, p.17, minimizes the deviation itself in `O(N M sqrt(N+M) log(N+M))` without a hard switching budget. Sequence-dependent switching costs are a different, hard problem; Theorem 6.2 and Corollary 6.3, pp.19–22, give hardness and inapproximability results for that general cost class. These results do not by themselves make unit-cost switch minimization equally hard. The publication year of this particular manuscript version was not established from search-engine dates.

**Assessment for the verified transfer:** no matching sharp switch-budget-preserving theorem was found in these sources or targeted searches. The [retained theorem](../results/cia-sharp-grid-transfer.md) combines the chronological support argument with a sharp instance-wise discretization bound and an explicit half-grid counterexample. Credit the established matching-rounding ingredient. Deleting intermediate modes can introduce an inadmissible direct transition, so the transfer does not preserve arbitrary transition graphs or minimum dwell times.

## Newly accessible thesis: a material qualification

A complete fresh download of Zeile's *Combinatorial Integral Decompositions for Mixed-Integer Optimal Control* succeeded from the [author PDF](https://mathopt.de/publications/Zeile2021a.pdf). The university bitstream instead returned HTML despite HTTP 200. Relevant sections were inspected in full extracted text; this is not a claim to have read the entire dissertation.

- Section 6.4.3, printed pp.78–80, gives a switching-time branch-and-bound algorithm. Remark 6.3 on p.78 counts the mode sequences and switch-position possibilities; it does not give the reopening's linear-time one-switch dominance rule.
- Printed p.139, immediately before Conjecture 7.1, already argues for an additive `Delta/2` continuous-to-grid correction by moving switching times to nearby grid points. This passage is motivation for the conjecture, not an independently proved general transfer theorem in the inspected text. The verified counterexample below shows that its claimed universal half-grid comparison fails.
- Conjecture 7.1 and the summary table, pp.139–140, still contain the multi-mode conjecture audited earlier.

Consequently, the sharp `Delta` transfer is not the first suggestion of a budget-independent discretization correction. Its contribution is a rigorous sharp statement, a construction, and a counterexample to the earlier half-grid assertion.

## Exact algorithms and the one-switch specialization

Bestehorn, Hansknecht, Kirches, and Manns, *Mixed-integer optimal control problems with switching costs: a shortest path approach*, [DOI](https://doi.org/10.1007/s10107-020-01581-3), [open final PDF](https://d-nb.info/1223084523/34), Section 3, introduces SCARP: minimize switching costs while bounding integral discrepancy. Section 1.1, PDF p.3, states an `O(N(2 theta+3)^(2M))` runtime bound on equidistant grids. Minimum dwell times and vanishing constraints can be accommodated; the objective can also reflect CIA. The general graph formulation therefore already supplies exact methods and flexible constraints. Merely casting a new formulation as a shortest path or adding a switch counter is insufficient novelty.

No specialized exact `O(nN)` one-switch algorithm, terminal-mass dominance rule, or reduction to three initial-mode candidates per grid point was found in the inspected algorithm sections or targeted searches. The [one-switch algorithm and its review](cia-reopened-practical-algorithm.md) are complete. Its specialized dominance rule and linear dependence on input size are the substantive distinction. No exhaustive priority claim follows; endpoint/minimum-duration and transition-constrained variants must retain their own precise scopes.

## Recent DP method and reproducible application data

Abbasi-Esfeden, Plate, Sager, and Swevers, *A dynamic programming-inspired approach for Mixed Integer Optimal Control Problems with dwell time constraints*, Journal of Process Control 154 (2025), 103522, [primary publisher page](https://www.sciencedirect.com/science/article/pii/S0959152425001507), [DOI](https://doi.org/10.1016/j.jprocont.2025.103522), [author preprint record](https://ssrn.com/abstract=5043263). The accessible introduction explicitly explains that the method loses optimal substructure and therefore does not generally guarantee global optimality. It accommodates flexible cost-to-go choices and general dwell constraints and compares with Gurobi and pycombina on four MIOCPs. The full final PDF was not retrieved during this review; the introduction and primary abstract are the evidence for these claims. The SSRN record lists a February 2025 manuscript with an August 2025 revision.

The maintained [pycombina repository](https://github.com/adbuerger/pycombina) supports maximum switch counts, dwell times, and switching adjacencies. Its `main` branch provides an existing realistic relaxed-control input:

- [Lotka–Volterra relaxed-control data](https://github.com/adbuerger/pycombina/blob/main/examples/data/mmlotka_nt_12000_400.csv).
- [Associated example driver](https://github.com/adbuerger/pycombina/blob/main/examples/lotka_volterra_multimode.py).

The filenames and paths were confirmed through the repository's public GitHub API tree. This permits a reproducible rounding comparison without first re-solving a nonlinear optimal-control problem. Report discrepancy and runtime separately from state/objective performance, and do not represent one-switch rounding as competitive with a comparator allowed many switches.

## State performance and MPC: established boundary

Zeile, Weber, and Sager, *Combinatorial Integral Approximation Decompositions for Mixed-Integer Optimal Control*, has an openly retrievable [2019 manuscript](https://optimization-online.org/wp-content/uploads/2018/02/6472.pdf); the [2022 final article](https://doi.org/10.3390/a15040121) is a distinct version. In the manuscript, Theorem 4.2, pp.9–10, gives a state-error bound of the form `(initial error + n(B+Ct) delta) exp(Lt)` under its stated regularity conditions. Sections 4.2–4.3 also incorporate model information into scaled and adjoint-based discrepancy objectives, and Section 5 uses recombination. The final article is now also available in the local literature package (retrieved September 5), closing the access gap recorded in the earlier audit. Its Section 3.4 introduces a switch limit and defers that class to prior work; Theorem 1 and Corollary 1 supply state bounds, while later sections develop recombination. The relevant final-text sections were inspected. [[zeile2022-combinatorial-integral-approximation-decompositions-for]] p.8-12. A basic state bound obtained by inserting the repository's new `delta` is an established-method corollary.

Makarow and Kirches, *Sequential Rounding in Mixed-Integer Model Predictive Control*, [primary record](https://optimization-online.org/2025/03/rounding-in-mixed-integer-model-predictive-control/), studies practical asymptotic stability through sequential rounding and MPC robustness. The live record read during this run showed an August 14, 2026 update, while indexed versions showed May 6, 2026. The formerly linked `autosam.pdf` returned HTTP 404 during direct retrieval, and the live record exposed no replacement PDF. Therefore only its abstract-level scope was checked; this review does not claim to have audited its newest theorems. Closed-loop stability is already an active literature topic and cannot be inferred from fixed-horizon CIA minimax alone.

## Search and access record

Searches covered CIA dynamic programming, one/single-switch rounding, fixed budgets, support-preserving rounding, vanishing constraints, subsequences, switch-time grid projection, TV-preserving discretization, and the exact source titles above. Primary texts were preferred over secondary summaries. No new citation census or exhaustive search of all adjacent scheduling terminology was completed. No author was contacted.

Downloaded PDFs and `pdftotext -layout` extracts were kept under `/tmp/cia-lit-20260906/`: `thesis-author`, `decomposition-preprint`, `scarp`, `matching`, `vc-bound`, and `sager-zeile-final`. These are temporary working copies; persistent evidence is supplied by the primary links and document locators above. No paper package was created or replaced manually in `literature/`. Its `AGENTS.md` was read before this review.

The earlier qualified novelty assessment for exact continuous one-, two-, and three-switch minimax results remains unchanged: no overlapping theorem was found here, but this targeted review cannot establish publication priority. The reopened results now have separate independent mathematical audits; the remaining qualification concerns literature coverage and publication priority.

## Verified exact one-switch minimax on arbitrary grids

The [retained finite-grid theorem](../results/cia-finite-grid-one-switch-minimax.md) computes the full worst-case one-switch error for `n>=3` on any rational grid with **`O(N^2)` rational arithmetic operations**. It evaluates an explicit formula, so no LP solver is required. It constructs a worst relaxed control with two component types and at most three time phases. A compressed witness keeps the dependence on `n` logarithmic in bit complexity; expanding every component necessarily costs at least linear time in `n`.

The derivation first gave constant-dimensional LPs, then eliminated them analytically. Both versions passed the [mathematical review](review-cia-reopened-finite-grid.md) and [implementation review](review-cia-reopened-finite-grid-code.md). The final paper contribution is the explicit formula, its structural reduction, and the extremizers. The LP characterization is supporting evidence rather than the final algorithm's required implementation.

No matching exact formula, top-two-mode reduction, or component symmetrization theorem was found in the checked primary sources and targeted searches. Sager–Zeile formulate the outer worst-case problem but leave general multi-mode bounds unresolved. [[sager2020-on-mixed-integer-optimal-control]] p.24-27. Symmetry averaging and LP elimination are established tools; the valid CIA-specific reduction is the substantive step. This is **mathematically verified; no matching prior result found in the targeted search**.

The instance algorithm computes a schedule for a supplied input. The outer minimax formula instead certifies a specified grid's worst-case capability before the input is known. These are separate practical guarantees.

## Verified sharp grid transfer and the source's half-grid assertion

The [sharp transfer theorem](../results/cia-sharp-grid-transfer.md) and [independent review](review-cia-reopened-grid-transfer.md) establish a uniform-grid replacement with no more switches and cumulative schedule discrepancy strictly below `Delta`. The coefficient one is optimal uniformly over mode counts and budgets. The rounding primitive is established; the temporal support argument, sharp instance-wise consequence, and counterexample are the additional content. No matching combined statement was found.

For the sharp family use `n>=2`, `N=n+1` unit cells, and `s=n-1=N-2`. The relaxed input is uniform across all modes on the first cell and pure mode `n` afterward. Its grid optimum is `1-1/n`. A continuous schedule visits each mode for `1/n` in the first cell and stays in mode `n` afterward; its error is `(n-1)/n^2`. Hence the optimal-value gap is at least `(1-1/n)^2`, tending to one. Taking `n=4,N=5,s=3` gives a gap at least `9/16`, exceeding one half.

The source scope was independently checked: initial activation is free, these inputs are admissible, and the budget belongs to `1<=s<=N-2`. The final Sager–Zeile article gives the half-grid comparison on **printed p.615**, immediately before Conjecture 1. The matching local manuscript locator is [[sager2020-on-mixed-integer-optimal-control]] p.27; the thesis repeats it on printed p.139. The appropriate description is **a sharp universal instance-wise grid-transfer bound correcting the source's half-grid justification**. The passage is an argument leading to a conjecture, not a proved half-grid theorem. The result does not claim a matching sharp gap between suprema over different relaxed-input classes.

## Verified correction to published Corollary 5

The [five-cell theorem](../results/cia-five-interval-two-switch-minimax.md) proves `F_grid(3,5,2)=1` on unit cells. Its [independent review](review-cia-reopened-small-grid.md) checked the integer-arithmetic proof through a separate implementation: all 14,400 candidate cumulative-floor histories were enumerated, with 396 nonempty strict chambers; each permits a word with at most two switches and error below one. Continuity covers chamber boundaries, and an alternating pure input attains error one.

This directly contradicts the lower value `8/7` from **Sager–Zeile, Corollary 5, printed p.611**. Its assumptions are `n>2` and `1<=s<=N-2`, so `n=3,N=5,s=2` is admissible. Definitions 4–7 on printed pp.579–581 use the same grid prefix error and TV constraint. Fixing horizon `[0,5]`, `N=5`, and maximum cell length one also removes grid-quantifier ambiguity: every cell must then have length one. This is a counterexample to the worst-case lower bound, established by a universal upper proof, not merely by a favorable individual input.

The source proof cites Theorem 4 and Corollary 4. Corollary 4's upper-bound attainment argument on **printed p.610** only establishes equality for `N=k(3+2s)+s+2`; it does not justify using that expression as a lower bound at every grid length. The earlier exact one-switch values do not create this contradiction: their lower bound `N/3` already exceeds `(N+2)/5` for every admissible `N>=3`.

The [final publisher PDF](https://link.springer.com/content/pdf/10.1007/s10589-020-00244-5.pdf) was retrieved, rendered, and inspected visually at printed p.611 (zero-based PDF index 36). Temporary source files are `/tmp/cia-lit-20260906/sager-zeile-final.pdf` and `corollary5-final-page611.png`. The local manuscript has the corresponding statement on p.24. [[sager2020-on-mixed-integer-optimal-control]] p.24. The repository helper that reproduced the source formula is a reference claim, not a valid unrestricted lower-bound routine; the earlier caution is superseded by the verified correction.

Fresh exact title/DOI/Corollary 5/`8/7` searches with correction and erratum found no later resolution. The publisher still carries the statement. Crossref returned no `update-to` entry and an empty `relation` field; this does not exclude every possible correction. No author was contacted. The defensible novelty description is **a verified counterexample to published Corollary 5; no prior correction found in the targeted search**.

## Verified exact algorithms for many modes and a fixed switch budget

The [retained fixed-budget result](../results/cia-fixed-switch-budget-algorithm.md), with [full derivation](cia-reopened-practical-algorithm.md), assigns subsets of `k` positive time blocks to modes, allowing repeated modes and empty assignments. Unary per-mode costs are the exact cumulative discrepancy. A standard subset-partition DP gives total work

```
O(nN + binom(N-1,k-1) n (k 2^k + 3^k))
```

for a switch budget of at most `k-1`, with the stated conventions when the budget exceeds the grid's possible switches. The [independent review](review-cia-reopened-fixed-budget.md) passed the recurrence, boundary enumeration, exact oracle comparisons, and mode-label candidate-set lemma.

Mode-specific minimum dwell times remain compatible with the DP: a mode's assigned subset determines its maximal consecutive active runs, whose durations can be checked in its unary cost. The implemented convention includes the initial and final maximal runs; unused modes have no dwell obligation. Adjacent blocks assigned to the same mode form one run; checking each nominal block separately would incorrectly exclude feasible schedules. The method does **not** cover coupled restrictions on successive distinct modes by this argument.

Targeted searches found no matching CIA theorem with this dependence on mode count. The important comparison is with established SCARP and the 2025 DP-inspired method discussed above: SCARP already gives exact graph methods and dwell support; the latter already gives flexible dwell-constrained heuristics. Therefore do not claim invention of dwell-constrained rounding, dynamic programming, or shortest-path formulations. The contribution is an exact CIA reduction with linear dependence on `n` for a fixed block budget, including the specified dwell constraints, on arbitrary grids.

The exponent of `N` depends on `k`, so the whole algorithm is not claimed fixed-parameter tractable in `k`. Its complexity guarantee is fixed-budget polynomial time. No general runtime advantage over SCARP, pycombina, or the 2025 heuristic is claimed: the mode-count dependence and exactness are proved, while practical runtime depends strongly on the grid and budget. A related exchange lemma retaining at most `d^2+d` mode labels for a fixed equality pattern is verified, but generic assignment exchange is established. Both should be presented with their CIA-specific contracts and **no matching prior theorem found in the bounded search**, rather than an exhaustive priority claim.
