# CIA total-variation investigation, 2026-09-04

The September 7 continuation supersedes the unresolved finite-grid and source-correction labels below. See [the current paper-readiness record](cia-reopened-paper-readiness.md) for the exact arbitrary-grid one-switch formula, fixed-budget algorithms, sharp grid transfer, corrected source lower bound, and remaining open questions. The earlier investigation is retained as history.

## Final lane index

The investigation is being closed at the user's request. The following retained claims, including the exact full-to-one-sided identity, have completed independent mathematical reviews. Novelty means only that the documented open-literature search found no matching statement, not a certificate of priority.

| Result | Scope and status | Main file |
|---|---|---|
| Published-conjecture counterexamples and exact uniform formulas | Continuous and finite-grid formulas; analytic proof and exact checks | [Uniform switching obstruction](../results/cia-uniform-switching-obstruction.md) |
| Exact continuous one-switch minimax | n≥3; analytic | [One-switch theorem](../results/cia-uniform-switching-obstruction.md) |
| Exact continuous two-switch minimax | n≥4; analytic | [Two-switch theorem](../results/cia-exact-two-switch-worst-case.md) |
| Exact continuous three-switch minimax | n≥5; analytic heavy/transfer argument with independently audited exact finite and symbolic prefix certificates | [Three-switch theorem](../results/cia-exact-three-switch-worst-case.md) |
| Universal heavy-mode bound and exact reduction to one-sided minimax | Every switch budget; analytic | [Universal heavy-mode rounding](../results/cia-universal-heavy-mode-rounding.md) |
| Explicit one-sided coefficient for every block count | 1≤k<n; analytic completion induction | [Arbitrary-block theorem](../results/cia-arbitrary-block-one-sided-bound.md) |
| Full arbitrary-profile bound, general exact plateau, and sharp first correction | 1≤k<n; analytic | [Arbitrary-switch global theorem](../results/cia-arbitrary-switch-global-bound.md) |
| Exact three-mode one-switch grid values | All unit-grid lengths, with separately handled one-interval boundary | [Finite-grid theorem](../results/cia-exact-three-mode-one-switch.md) |

The broadest new upper bound is

F_{n,k−1}(T)≤T max{1/(k+1),[n(n−1)+(n−k)(n−k−1)]/[nk(2n−k−1)]}.

It gives exact F_{n,k−1}=T/(k+1) for every k≥2 and k+1≤n≤k(k+1)/2. For every fixed k it determines the first mode-count correction sharply:

F_{n,k−1}(T)=T/k−(k+1)T/(2kn)+O_k(T/n²).

The exact full-discrepancy minimax reduces to max{T/(k+1),G^-_{n,k}(T)}, where G^- is the unrestricted-profile one-sided minimax with at most k blocks, including repeated modes. Exact one-sided values beyond the established small block counts remain open. The [many-mode investigation](cia-many-mode-switching-investigation.md) preserves the unproved higher-order aggregate route. The [adjacent-repeat investigation](cia-adjacent-repeat-investigation.md) preserves the now-proved existential property, an unproved largest-mode strengthening, and two exact counterexamples to stronger shortcuts.

The literature audit is [cia-novelty.md](cia-novelty.md). Independent reviews are linked from each result file. Intermediate equal-mass and analytic global bounds remain in the repository as separately reviewed arguments, with links to later results that supersede their finite-n gaps.

## Retained results

See [the main result](../results/cia-uniform-switching-obstruction.md) and [independent audit](review-cia.md).

1. The Sager–Zeile published Conjecture 1 is false as an upper bound: five uniform modes, 45 unit intervals, one allowed switch have exact CIA error 16, exceeding 31/2.
2. Uniform relaxed controls have an exact continuous error formula for every switch budget 0≤s≤n−2 and an exact discrete scalar recurrence.
3. The **full continuous worst-case error with one switch** is exactly T max{1/3,(n−1)^2/[n(2n−1)]}. This completely determines the dependence on the number of modes: three or four modes have value T/3, whereas five or more have uniform controls as extremizers.
4. A constructive procedure evaluates cumulative controls at at most two times. Rounding its sole switch to a nearest grid endpoint gives the corrected discrete upper bound H_n(T)+Δbar/2.
5. On the smallest admissible grid N=3, the full discrete worst case is 2−3/n. Seven modes give the compact counterexample 11/7>3/2.
6. The [exact three-mode, one-switch discrete worst case](../results/cia-exact-three-mode-one-switch.md) is k, k+1/2, or k+3/4 for N=3k, 3k+1, or 3k+2 respectively. Explicit relaxed controls attain every value; the proof is independently reviewed.

Proofs were independently checked by `audit_scaling`. The audit also enumerated all 885 one-switch schedules of the principal counterexample. The local exact-rational scripts independently check broader special cases and the constructive algorithm.

## Literature checks and novelty limits

The local preprint is `literature/papers/sager2020-on-mixed-integer-optimal-control/original.pdf`. Conjecture 1, equation (7.6), is unchanged in the final published article, printed page 615. The final PDF was fetched and checked independently by the reviewer: [open final PDF](https://www.econstor.eu/bitstream/10419/288496/1/s10589-020-00244-5.pdf), [DOI](https://doi.org/10.1007/s10589-020-00244-5).

Targeted web searches included:

- `Sager Zeile total variation constrained control rounding Conjecture 1 2021 7.6`
- `combinatorial integral approximation switching constraints sharp bounds Sager Zeile 2024 2025`
- `"Sager" "Zeile" "conjecture" "variation"`
- `"Conjecture" "combinatorial integral approximation"`
- `"integral approximation" "one switch"`
- `"combinatorial integral approximation" "worst-case" "switch"`

These located the original article, Zeile's dissertation, and later related work; none of the inspected search results supplied the present correction or exact one-switch formula. This is evidence of an apparent gap, not proof of novelty. Primary later/adjacent literature identified for broader comparison includes:

- Zeile, [*Combinatorial Integral Decompositions for Mixed-Integer Optimal Control*](https://mathopt.de/publications/Zeile2021a.pdf), 2021 dissertation. The search-extracted section 7.5.2 retains the same conjectural direction.
- Bestehorn et al., [*Non-uniform Grid Refinement for the Combinatorial Integral Approximation*](https://arxiv.org/abs/2305.12846), 2023. Concerns adaptive discretization for switching-cost-aware rounding.
- [*Extended formulations for binary optimal control problems*](https://doi.org/10.1007/s10107-024-02162-4), 2025. Concerns extended formulations for binary switching restrictions.
- [*Parabolic optimal control problems with combinatorial switching constraints, part III: branch-and-bound algorithm*](https://doi.org/10.1007/s10589-025-00654-3), 2025. Its primal-bound section cites AMDR for bounded switching and CIA rounding; the extracted discussion does not claim the sharp one-switch constant.
- [*Mixed-integer optimal control problems with switching costs: a shortest path approach*](https://doi.org/10.1007/s10107-020-01581-3). Its stated worst-case analysis concerns runtime, not the extremal rounding error studied here.

An independent citation-forward novelty search is documented in [notes/cia-novelty.md](cia-novelty.md). It screened 29 OpenAlex citing records through 2026 and found no prior resolution. Human expert review remains appropriate before publication.

## Computation and cautions

The existing `cia_tv.py` uses Gurobi and is runnable with `/home/sgusev/miniconda3/envs/minlp-notes/bin/python`; the system Python does not have Gurobi. The new certificate scripts use only the standard library and exact rational/integer arithmetic.

Exploratory full worst-case MILP values on unit grids:

| N | n | s | optimum (numerical) |
|---|---|---|---|
| 3 | 3 | 1 | 1 |
| 4 | 3 | 1 | 3/2 |
| 5 | 3 | 1 | 7/4 |
| 6 | 3 | 1 | 2 |
| 3 | 4 | 1 | 5/4 |
| 3 | 5 | 1 | 7/5 |
| 4 | 4 | 1 | 3/2 |
| 5 | 5 | 1 | 2 |
| 4 | 3 | 2 | 1 |
| 5 | 3 | 2 | 1 |
| 6 | 3 | 2 | 4/3 |
| 5 | 4 | 2 | 4/3 |

These are exploratory solver outputs, not exact symbolic proofs. In particular, literal finite-grid equality in the conjecture is already inconsistent with several small examples, but the retained n=5,N=45 construction is stronger: it violates the conjecture's upper bound and does so asymptotically.

A separate caution, resolved in the September 7 continuation: the original helper `cor5_lower` returned (N+s+1)/(3+2s), following the paper's stated Corollary 5. The [exact five-cell theorem](../results/cia-five-interval-two-switch-minimax.md) now proves a counterexample to that lower bound, with independent integer enumeration and source review. The helper is renamed `cor5_claim` and explicitly retained only as a historical source expression. The original observation was numerical; the later universal upper proof is what establishes the correction.

## Remaining questions at closure

Exact one-sided minimax values beyond four activation blocks remain open, and the full minimax reduces to that question by the universal heavy-mode identity. General finite-grid worst cases beyond the retained special cases also remain open. These are documented questions, not active work: the user requested that the current investigation be finalized and stopped.


## Additional finite-grid exploration

Further numerical worst-case one-switch values: F(7,4)=5/2, F(8,4)=3, F(9,4)=3, F(8,5)=16/5, F(9,5)=17/5. The tempting conjecture that every finite-grid worst case is the maximum of the three-mode value and the uniform-input value is false numerically at N=9,n=5: the respective quantities are 17/5, 3, and 16/5. A rational candidate attaining 17/5 has mode totals (13/5,8/5,8/5,8/5,8/5) and cumulative allocations at time 4 equal to (8/5,3/5,3/5,3/5,3/5). The extra unit between times 4 and 5 can go to one of the four smaller modes. This candidate is not needed for the retained theorems; a full exact finite-grid formula for n≥4 remains open here.

For such finite-grid work, a threshold E is feasible with an ordered pair p,q switching at integer k exactly when all omitted mode totals are at most E, A_p(k)≥k−E, and m_q≥N−E−k. Thus possible initial modes shrink with k while possible final modes grow with k. When all totals are at most E, failure at a given k means one of these sets is empty, or both consist of the same single mode. This nested-set structure may permit a compact exact characterization; no complete theorem is claimed from it here.

The N=9,n=5 candidate above was subsequently certified in exact arithmetic over all 200 ordered-pair/switch-time schedules. Its full relaxed matrix is 1/10 times

```
 5  7  4  0  0 10  0  0  0
 5  0  0  1 10  0  0  0  0
 0  0  6  0  0  0  0 10  0
 0  0  0  6  0  0 10  0  0
 0  3  0  3  0  0  0  0 10
```

A direct proof of its minimum 17/5 avoids enumeration. If the switch time is at most 3, every final-mode total is at most 13/5, and the final negative error is at least 9−13/5−3=17/5. If the switch time is at least 5, every mode's cumulative allocation at time 5 is at most 8/5, and the initial-mode negative error is at least 5−8/5=17/5. At switch time 4, either the final mode is one of the four modes with total 8/5, yielding final error 9−8/5−4=17/5, or it is mode 1, forcing a different initial mode whose cumulative allocation at time 4 is 3/5, yielding initial negative error 4−3/5=17/5. A switch at time 3 to mode 1 attains 17/5. Thus the tempting max-of-uniform-and-three-mode extension is rigorously false, even though the full numerical upper value 17/5 has not received a symbolic proof.
