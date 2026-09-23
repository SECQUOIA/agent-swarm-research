# Exact one-switch rounding in linear arithmetic time

Date: 2026-09-07. Status: proved structural results and exact prototypes, independently reviewed. This is an instance optimization result, separate from the worst-case minimax theorems.

## Result and practical scope

An instance of combinatorial integral approximation (CIA) with at most one switch can be solved exactly in **O(nN) arithmetic operations** on an arbitrary grid, where n is the number of modes and N the number of intervals. The algorithm reads the allocation table twice and checks at most three ordered mode pairs at each permitted switch boundary. It uses rational arithmetic and returns an optimal schedule and its exact error.

The result also permits an arbitrary subset of switching boundaries and a fixed initial mode. A common minimum duration for both nonempty blocks can be enforced by keeping only boundaries t with d <= t <= T-d, assuming T >= d so that a constant schedule remains admissible. This is not a solution for general mode-specific dwell requirements or transition restrictions.

The contribution is modest but useful: a solver-free exact benchmark for a constrained rounding problem, including nonuniform grids and fixed initial controls. It does not establish good state-space or economic performance for a control application, and one switch can be much too restrictive in practice.

## Setting

Let 0=t_0<t_1<...<t_N=T. Let A_i(t) be cumulative relaxed allocation with A_i(0)=0, each A_i nondecreasing, and sum_i A_i(t)=t. Write m_i=A_i(T). The error of a binary schedule w is

    D(A,w) = max_i sup_{0<=t<=T} |A_i(t)-integral_0^t w_i(r)dr|.

Switches may occur only at a prescribed subset K of the internal grid boundaries. Constant schedules are allowed. No assumption about constancy of the relaxed control within a grid interval is required: the signed discrepancy of an active mode is nonincreasing, and that of an inactive mode is nondecreasing. Thus its extrema occur at block endpoints.

The code takes each interval's integrated allocation mass, not its average rate. Every interval row must be nonnegative and sum exactly to its duration.

## Lemma 1: three terms determine a one-switch error

For distinct initial and final modes p,q, switching at t, the error is exactly

    C(p,q,t) = max{ max_{i not in {p,q}} m_i, t-A_p(t), T-t-m_q },

with an empty omitted maximum equal to zero.

Proof. For p, the signed discrepancy decreases from zero to A_p(t)-t, then increases to m_p-t. For q, it increases to A_q(t), then decreases to m_q-(T-t). Omitted modes have largest discrepancy m_i. The two additional positive quantities satisfy

    A_q(t) <= t-A_p(t),
    m_p-t <= T-t-m_q,

by conservation of relaxed allocation. A possible negative terminal error for p is no worse than its error at t, and a positive terminal error for q is no worse than its error at t. The displayed three terms therefore suffice, and each is itself an attained discrepancy or a nonnegative lower bound supplied by an omitted mode. The quantity t-A_p(t) is nonnegative, so the formula also covers negative T-t-m_q. QED.

A constant schedule p has error T-m_p, because all omitted totals are at most their sum T-m_p.

## Lemma 2: the best final mode has largest available total

Fix p and t. Among all q != p, a mode with largest m_q minimizes C(p,q,t).

Proof. Replace q by r != p with m_r >= m_q. The term t-A_p(t) is unchanged and T-t-m_r decreases. In the omitted maximum, r is removed and q is inserted. Its value cannot increase: the inserted total is no larger than the removed total. QED.

This domination holds before minimizing over t. It uses the unrestricted choice of a final mode; arbitrary transition restrictions or mode-dependent terminal eligibility require a fresh argument.

## Theorem: three candidates per boundary

Fix an ordering h_1,h_2,... of the modes by nonincreasing total, breaking ties consistently. For n>=3 and each boundary t, an optimal ordered pair occurs among

1. (h_1,h_2),
2. (h_2,h_1),
3. (p_t,h_1), where p_t maximizes A_i(t) among i outside {h_1,h_2}.

For n=2 only the first two candidates are needed. For n=1 the unique constant schedule is optimal.

Proof. Lemma 2 fixes the final mode as h_2 if p=h_1 and h_1 otherwise. The initial modes h_1,h_2 give the first two candidates. For every remaining initial mode, the largest omitted total is exactly m_{h_2}; the final-mode term is T-t-m_{h_1}. Only t-A_p(t) varies. Maximizing A_p(t) gives the third candidate. QED.

Evaluate these candidates at every permitted boundary and compare with the best constant schedule h_1. Totals and cumulative allocations require O(nN) operations. Three leaders can be selected with three linear scans; sorting all modes is unnecessary. Selecting p_t requires one scan per boundary. The claimed complexity counts exact arithmetic operations; it is not a unit-cost bit-complexity claim for arbitrary rational input. The provided implementation stores O(nN) rational input values after validation and O(n+N) working state (including the allowed-boundary list and set).

If the initial mode is fixed to p, retain only the constant p and the candidate (p,q_p) at each boundary, where q_p has largest total among other modes. This proves the same bound and does not require choosing three initial candidates.

## Further consequence: only neighboring boundaries around a crossing matter

For a fixed initial p, let q_p be its best final mode from Lemma 2 and let M_p be its omitted maximum. The two nonconstant terms

    L_p(t)=t-A_p(t),   R_p(t)=T-t-m_{q_p}

are respectively nondecreasing and strictly decreasing. Their difference 2t-A_p(t)-T+m_{q_p} is strictly increasing. Therefore the optimal permitted boundary for this pair occurs at one of the two permitted boundaries adjacent to their crossing, with the first or last boundary used if the crossing lies outside the permitted range. The constant M_p does not alter this conclusion. With cumulative allocations already available for random access, this permits O(n log N) additional boundary queries rather than a full grid scan. The prototype uses the simpler linear input scan; the crossing observation is retained for sparse-query or continuous-oracle settings. No separate implementation is needed for the present input format.

## Exact implementation and verification

- [Optimizer and direct discrepancy evaluation](../code/cia_reopened/rounding.py).
- [Independent-enumeration test script](../code/cia_reopened/check_rounding.py).

Run:

```bash
python code/cia_reopened/check_rounding.py --benchmark
```

The script compares the optimizer with direct prefix evaluation of every one-switch schedule for 530 exact rational cases. These cover all half-integral columns for several small mode/grid sizes, 65 nonuniform random rational instances with both unrestricted and restricted/fixed-initial variants, the retained five-mode nine-interval 17/5 example, and the uniform five-mode 45-interval value 16. Invalid data and accidental floating input are rejected explicitly. Tests evaluate observable prefix error, without relying on the optimizer's dominance formula.

A synthetic n=100,N=1000 exact-rational case completed in about 0.30 seconds in this workspace; the returned error is 97301/200. This is a stress case, not an application validation. Times depend on hardware and rational denominator sizes.

## Public control profile benchmark

The public [pycombina multimode Lotka-Volterra data](https://github.com/adbuerger/pycombina/blob/6b073fe29984186dccfc7e2108bfba9692a6cc9c/examples/data/mmlotka_nt_12000_400.csv) supplies a 3-mode relaxed profile over 12 time units and 12,000 intervals. Associated pycombina example drivers permit more switches and use per-mode switching restrictions; their historical revisions use different grid strides and mode selections. This test reads all three source modes on the full grid; the present test uses its input profile with a total budget of **one** switch. It is not a reproduction of the original example's optimization problem.

Input: [mmlotka_nt_12000_400.csv](https://raw.githubusercontent.com/adbuerger/pycombina/6b073fe29984186dccfc7e2108bfba9692a6cc9c/examples/data/mmlotka_nt_12000_400.csv), SHA256 `1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883`.

The published decimal rates do not sum exactly to one. The benchmark normalizes each row and then uses largest-remainder apportionment to denominator 10^6. Each resulting rate differs from its normalized source by strictly less than 10^-6. Consequently the cumulative discrepancy, and hence its optimal value over the same schedules, changes by strictly less than T*10^-6=0.000012 relative to the normalized decimal source. Exact arithmetic verifies the apportionment bound. The script also reports the separate source-to-normalized rate change.

Download this cited CSV to a local file, then run:

```bash
python code/cia_reopened/check_rounding.py --public-benchmark /path/to/mmlotka_nt_12000_400.csv
```

The exact quantized optimum is **1889/1000 = 1.889**, attained by mode 1 followed by mode 2 at boundary 1889 (zero-based mode numbering, switching time 1.889). The optimizer took approximately 0.27 seconds in this workspace. The largest source-to-normalized rate change was below 4.959*10^-7.

The benchmark verifies the exact result with a separate O(n^3 N) scan over every ordered pair and switching boundary. That scan directly evaluates every mode's errors at the boundary and horizon and does not use largest-total dominance.

## Literature comparison and novelty limits

The existing one-switch minimax proof already uses the three-term error expression in Lemma 1. The new point here is the total-dominance reduction and resulting three-candidate instance algorithm. The exact algorithm is not claimed as a novel dynamic programming principle.

- Sager, Jung, and Kirches, *Combinatorial Integral Approximation* (2011), [DOI](https://doi.org/10.1007/s00186-011-0355-4), develops CIA and tailored branch and bound with switching constraints.
- Bestehorn, Hansknecht, Kirches, and Manns, *Mixed-integer optimal control problems with switching costs: a shortest path approach*, [open final PDF](https://d-nb.info/1223084523/34), [DOI](https://doi.org/10.1007/s10107-020-01581-3), gives a more general graph algorithm, with dependence exponential in mode count and a discrepancy parameter. Its broader constraint support is not provided by the present specialization.
- Zeile, *Combinatorial Integral Decompositions for Mixed-Integer Optimal Control* (2021), [author PDF](https://mathopt.de/publications/Zeile2021a.pdf), Section 6.4.3 and Remark 6.3, discusses switching-time enumeration/branch and bound with n(n-1)^s binomial(N-1,s) possible schedules. An independent literature lane inspected the algorithm chapter and found no specialized one-switch dominance rule.
- Abbasi-Esfeden, Plate, Sager, and Swevers, *A dynamic programming-inspired approach for Mixed Integer Optimal Control Problems with dwell time constraints* (2025), [DOI](https://doi.org/10.1016/j.jprocont.2025.103522), provides a broader heuristic framework; its introduction explicitly discusses loss of optimal substructure and the absence of a general global-optimality guarantee.

Targeted searches on 2026-09-07 for `"combinatorial integral approximation" "one switch"`, `"combinatorial integral approximation" "linear time"`, and switching-cost shortest-path one-switch variants found no matching three-candidate theorem. The literature lane separately searched one/single-switch variants. This supports retaining the result as potentially new, not asserting publication priority. Expert comparison with the earlier CIA literature remains appropriate before publication.

## Extension 1: largest residual is the best final mode after any prefix

Fix **any** binary prefix ending at grid time u<T. Repeated modes and arbitrarily many earlier switches are allowed. Let E_0 be its maximum discrepancy over [0,u], let c_i be the binary service already given to mode i, and define residual totals

    r_i = m_i-c_i,    sum_i r_i=T-u.

Appending a single constant suffix in mode j gives exactly

    max{ E_0, max_{i != j} r_i, T-u-r_j }.

Indeed, each inactive discrepancy increases from its prefix-end value to r_i. Its possible negative error is already covered by E_0, and its final positive error is r_i. The active discrepancy decreases to r_j-(T-u); its possible initial positive error is covered by E_0, and its final negative error is T-u-r_j. These quantities cover all extrema. Negative residual totals cause no problem because E_0>=0.

Among any fixed nonempty set of eligible suffix modes, a mode with largest residual r_j is optimal. Replacing j by an eligible larger-residual mode reduces the final negative term and cannot increase the maximum residual of omitted modes. Eligibility may, for example, require a change from the prefix's last mode. The lemma concerns optimizing the last block after a **fixed** prefix; it does not justify a greedy algorithm for selecting earlier blocks.

`complete_with_one_block` implements this formula. Its tests compare 90 random rational prefix/eligibility cases against direct error evaluation for every eligible final mode, including prefixes with repeated modes. The n=1 boundary is also checked. This lemma can remove final-mode branching in a schedule search but is not used as a substitute for global optimization.

## Extension 2: exact fixed-budget optimization with linear mode-count dependence

The one-switch theorem has a broader algorithmic extension: for a fixed small switch budget, remove enumeration of mode words by using a standard subset-partition dynamic program. The new CIA-specific observation is that repeated uses of one mode can be assigned together and evaluated independently once the possible block boundaries have been fixed. The dynamic programming technique itself is elementary and is not claimed to be new.

### Assignment of modes to fixed blocks

Fix k nonempty consecutive grid blocks with endpoints

    0=b_0<b_1<...<b_k=N.

Let l_j=t_{b_j}-t_{b_{j-1}}. For each mode i and subset U of {1,...,k}, define

    c_i(U) = max_{1<=j<=k} | A_i(t_{b_j}) - sum_{h in U, h<=j} l_h |.

The mode is active precisely in blocks U; U may be disconnected. Its signed discrepancy is monotone within each block, so c_i(U) is its exact full-horizon error. In particular c_i(empty)=m_i, and every mode, including unused modes, must contribute a cost.

A block labeling is equivalent to a partition (U_1,...,U_n) of the k blocks, with empty parts allowed. Its objective is max_i c_i(U_i). Define D_i(S) as the best maximum cost for modes 1,...,i assigning precisely blocks S among them. Initialize D_0(empty)=0 and D_0(S)=infinity for nonempty S. The exact recurrence is

    D_i(S) = min_{U subset S} max{ D_{i-1}(S minus U), c_i(U) }.

It enumerates which blocks belong to mode i and delegates the remaining blocks to preceding modes; those possibilities are exhaustive and disjoint. Hence D_n({1,...,k}) is the exact optimum. Recording the minimizing U at each state reconstructs an optimal labeling.

There are 2^k costs per mode, each computable with one k-step cumulative scan, and sum_S 2^|S|=3^k transitions per mode. After input preprocessing, runtime is

    O(n (k 2^k + 3^k))

arithmetic operations for a fixed block partition. Traceback storage is O(n2^k); the current costs and objective rows require O(2^k) additional storage. Repeated modes are fully allowed; adjacent blocks may have the same label.

### Optimization over all schedules with a small switch budget

Let s>=0 and k=min(s+1,N). Enumerate all binomial(N-1,k-1) internal boundary sets and apply the fixed-block algorithm. Every labeling has at most k-1 switches. Conversely any schedule with at most s switches can be represented: subdivide its constant stretches at unused grid boundaries until it has k nonempty blocks, allowing adjacent equal labels. This is possible because k<=N. Therefore the best result is exactly the unrestricted CIA optimum under the total switch budget.

With O(nN) cumulative-allocation preprocessing, the total arithmetic complexity is

    O(nN + binomial(N-1,k-1) n (k 2^k + 3^k)).

Storage is O(nN+n2^k). In particular, **two switches admit exact O(nN^2) optimization**, including repeated modes and arbitrary nonuniform rational grids. For every fixed switch budget the dependence on the number of modes is linear. The algorithm remains exponential in k and has an N^(k-1) boundary-enumeration factor. Thus it is not fixed-parameter tractable in k alone, and it is not intended for large switch budgets or very fine grids with multiple switches. The specialized one-switch solver remains faster than this general construction when s=1.

The implementation is `optimal_block_assignment` for prescribed boundaries and `optimal_few_switches` for a budget. The fixed-block routine is useful independently when engineering constraints or a previous optimization already specify switching windows or candidate blocks. The current API implements unrestricted assignments and the minimum-dwell extension detailed below. The same recurrence also handles further restrictions that depend only on an individual mode's assigned subset: set c_i(U)=infinity for an inadmissible subset U. This includes mode-specific dwell times, activation counts, availability windows, and bounds on total service. Dwell lengths must be computed from maximal consecutive runs in U, merging adjacent assigned blocks; unused modes and endpoint runs follow the particular application's explicitly chosen conventions. If each admissibility check costs O(k), the stated arithmetic-operation order is unchanged. General transition graphs couple different modes and are outside this separation argument.

### Verification and limits

The check script adds 110 direct brute-force comparisons on rational grids: fixed partitions versus all binary schedules respecting those boundaries, and budgets 0,1,2, and larger than N versus all n^N schedules in small instances. The repeated schedule (0,1,0), with zero discrepancy on its integral relaxed profile, is a separate regression: a distinct-mode-only algorithm would fail it. These checks complement, rather than replace, the recurrence and subdivision proofs. Independent mathematical and implementation reviews are linked below.

No assertion is made that this exact algorithm outperforms existing branch and bound on typical low-mode control problems. Its clear complexity advantage concerns many modes and a fixed small number of blocks. A useful paper presentation would separate the input-linear one-switch method, the general fixed-budget reduction, and existing broadly applicable exact/heuristic algorithms.

## Additional retained structural lemma: a small mode-label candidate set

An alternative formulation fixes both block boundaries and the pattern of equal labels, leaving d<=k distinct roles to assign injectively to modes. Let c_{ri} be mode i's full-horizon discrepancy when assigned role r's blocks. Unselected modes contribute m_i. Then an optimal assignment uses only the following set of at most d^2+d mode labels:

- the d modes with largest totals m_i;
- for each role r, the d modes with smallest c_{ri}.

If n<d, an injective assignment is impossible; otherwise tie-breaking may be arbitrary but consistent.

Proof. Start from any optimal assignment with a selected mode i outside this candidate set. Since i is outside the d largest totals and only d modes are selected in total, at least one of those d largest-total modes is omitted. Thus m_i is no greater than the current omitted-mode maximum. Among the d cheapest labels for i's role, at least one j is not used by the other d-1 roles. Replace i by j. Its role cost cannot increase because i was outside that cheapest set. The new omitted mode i has total no greater than the old omitted maximum, so the omitted penalty cannot increase. The replacement enters the candidate set and leaves every other assignment unchanged. Repeat until every selected mode belongs to the set. QED.

This is an elementary exchange argument, not a claim of a new general matching principle. It gives a separate explanation for why fixed-pattern label searches can avoid a power of n. The subset-partition implementation is simpler for the current goal and avoids enumerating equality patterns or candidate-set injections, so no second optimizer is added solely to implement this alternative proof.

The bounded follow-up literature check found no matching CIA fixed-budget subset-partition reduction or stated candidate-set theorem. The closest inspected exact methods remain SCARP and switching-time branch and bound; see the [reopened literature audit](cia-reopened-literature.md). This is a qualified search result, not a priority claim.

## Public-profile switch-budget comparison on restricted grids

For a small exact multi-switch demonstration, the benchmark aggregates consecutive masses from the same quantized 12,000-interval Lotka-Volterra profile into 24 blocks of length 0.5, or 12 blocks of length 1. This changes the permissible switching times but **does not approximate the relaxed cumulative input** at those boundaries. Moreover, for a returned schedule constant in each coarse block, discrepancy is monotone inside each block for every mode. Thus its maximum error on the complete original profile equals its coarse-boundary error, even though the relaxed rates vary inside the coarse blocks.

| Permitted switching grid | Total switch budget | Exact optimal discrepancy | Approximate runtime |
|---|---:|---:|---:|
| 24 half-unit intervals | 0 | 4721469/1250000 = 3.7771752 | <0.001 s |
| 24 half-unit intervals | 1 | 4999999/2500000 = 1.9999996 | 0.003 s |
| 24 half-unit intervals | 2 | 3/2 = 1.5 | 0.061 s |
| 12 unit intervals | 3 | 1067507/1250000 = 0.8540056 | 0.070 s |

The two-switch optimum uses modes (1,2,0) at times (1.5,9). The three-switch optimum uses **repeated mode 2**, with mode word (2,0,1,2) and times (2,3,5). Mode numbers are zero-based. Every value was checked by a separate exhaustive enumeration of mode words and permitted boundary sets, and every returned coarse schedule was expanded and directly evaluated on all 12,000 original intervals. The public benchmark option reproduces these checks. Runtimes are illustrative workspace measurements, not a comparison against another optimizer.

The first three rows compare budgets on exactly the same restricted grid. The fourth row uses a different grid and should not be read as the next point on that same grid's optimum curve. None of these multi-switch values claims global optimality on the full 12,000-interval switching grid. They demonstrate exact scheduling decisions with a small number of permitted switching times, not state-space or economic performance.

## Implemented mode-specific minimum dwell extension

Both `optimal_block_assignment` and `optimal_few_switches` accept the optional `minimum_dwell` sequence, with one nonnegative rational duration d_i per mode. The exact convention is:

- every maximal active run of mode i must last at least d_i;
- the initial and terminal active runs obey the same requirement;
- adjacent blocks with the same mode form one run;
- an unused mode has no dwell requirement to satisfy.

For each mode subset U, the implementation scans its selected blocks and merges consecutive selected blocks into maximal runs. If any run is shorter than d_i, it marks c_i(U) infeasible. Otherwise it uses the usual discrepancy cost. The same subset recurrence is exact because the validity of a mode's runs depends only on U, the physical block lengths, and d_i. This adds only O(k) work per subset and preserves all complexity bounds. The subdivision argument also remains valid: subdividing a constant run does not create a new maximal active run.

Both APIs return `None` if no admissible schedule exists, distinguishing infeasibility from an infinite numerical error. Negative or incorrectly sized dwell vectors are rejected. A dwell duration larger than T is allowed as input and simply prevents that mode from being used.

The main check script adds 44 exact brute-force comparisons with random per-mode dwell requirements on nonuniform rational grids. These test both prescribed boundaries and a two-switch budget, including infeasible instances. Explicit regressions verify that adjacent assigned blocks merge for dwell testing and that an instance with all available modes requiring a run longer than the horizon returns `None`.

This constrained extension is an exact alternative for small block budgets to broader dwell-time rounding methods. It does not claim to replace the 2025 dynamic-programming-inspired method on its broader dynamics-aware objective or high-resolution examples.

## Independent review

The [practical-algorithm review](review-cia-reopened-practical-algorithm.md) independently checks the one-switch dominance theorem, crossing observation, arbitrary-prefix suffix rule, subset recurrence, candidate-set exchange, and implementations. Its exact checker includes thousands of cases and reports documentation/input-validation corrections made during review. Those corrections are incorporated here and in the code.

A [second fixed-budget review](review-cia-reopened-fixed-budget.md) independently verifies the fixed-block and budget algorithms, their complexity, the candidate-set lemma, and the minimum-dwell extension. Its separate fine-breakpoint oracle checks relaxed inputs that vary within coarse grid cells, including 3,836 budget and 3,139 partition cases plus 608 dwell comparisons (52 infeasible). Both reviews found the final stated mathematics sound. These are internal independent reviews, not external peer review.
