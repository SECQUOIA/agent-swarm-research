# Independent mathematical review of the finite-grid one-switch minimax

Reviewed 2026-09-07 by a separate agent. Scope: [the proposed finite-grid theorem](cia-reopened-finite-grid.md), its LP formulation, its extremizer compression, the nine-interval example, and the implementation's interpretation. The review does not establish novelty; that is addressed by the separate literature investigation.

**Verdict: the stated mathematical theorem is correct, including the subsequent explicit-formula refinement (2)–(7).** No missing case or invalid boundary step was found. A short analytic upper proof also confirms the flagship value `F_5(9)=17/5` without optimization software. The original LP code is a certificate finder rather than a guaranteed complete exact solver for every rational input; the explicit rational formula removes that implementation limitation.

## Mathematical audit

The original discrepancy is the maximum absolute cumulative allocation error over modes and time, with constant controls allowed and the initial activation free. All schedules used below conform to this definition. On each original grid interval the discrepancy is affine, so endpoint evaluation is exact.

1. **Schedule identity.** For a schedule `p` followed by `q`, the first mode's negative discrepancy peaks at the switch and the final mode's negative discrepancy peaks at the horizon. Positive discrepancies of those two modes are bounded by these terms or omitted totals. This gives exactly the displayed three-term identity. Endpoint switches correctly include constant controls. A largest-total final mode distinct from the initial mode weakly improves both the final deficit and the omitted-mode maximum. Ties present no problem.

2. **Sufficiency of the closed regions.** A switch strictly before `t_a` lies at most at `t_(a-1)`. The upper cutoff inequality then forces final deficit at least `E`, including equality. A switch at or after `t_a` has initial deficit at least its value at `t_a`, because `t-A_p(t)` is nondecreasing. The second cutoff works identically. Thus weak inequalities suffice throughout; no strict-feasibility assumption is hidden in the lower-witness argument. In the second program, any schedule other than the two orders involving both distinguished modes omits a mode with total at least `m_2>=E`. Constant schedules also do so.

3. **Coverage of an arbitrary maximizer.** Compactness holds because the input is a finite product of simplices and the optimal error is a finite minimum of continuous schedule errors. The universal lower bound `T/3` follows by putting total `T/3` on each of three modes, even on a one-interval grid. For `T/3<E<F`, there are at most two totals strictly above `E`. The first eligible cutoff cannot be zero: selecting mode 1 constantly would otherwise have error `T-m_1<=E`. Cutoffs exist because `T-E-m_j<T`. This proves `1<=a<=b<=N`.

4. **Exhaustiveness of the two cases.** If `m_2<=E`, all dominant schedules omit only totals at most `E`. Their final deficit at the first eligible cutoff is at most `E`; strict failure therefore forces the initial deficit to be strictly above `E`. If `m_2>E`, then `m_3<E` follows from `3E>T`, and the same conclusion is needed only for the two schedules selecting both large modes. These are exactly the common constraints of the second program. The split is exhaustive, including `m_2=E` in the first case.

5. **Averaging the remaining modes.** Averaging cumulative trajectories 3 through `n` preserves monotonicity, the total cumulative allocation at every time, and the upper bound on their final totals by `m_2`. In the first case it preserves all their initial-deficit inequalities because those inequalities have the same right-hand side. In the second case there is no tail-mode initial-deficit constraint to preserve. Consequently the use of one per-mode variable with multiplicity `n-2` is valid. No ordering of the tail modes' intermediate allocations is assumed or needed.

6. **Limit at the optimum.** There are finitely many region labels. Along a subsequence their label is fixed, endpoint allocations are bounded, and all region constraints are closed. The limiting point therefore has objective `F`. This is the correct reason to allow equality at both ends of cutoff ranges.

7. **Boundary `F=T/3`.** The proposed direct point satisfies every constraint: `t_a>=E`, `t_(a-1)<=E`, and `t_a<=3E` give `0<=(t_a-E)/2<=E`; all three weighted sum equations hold. Since `a=b`, monotonicity plus equal weighted sums forces the two endpoint vectors to agree. The construction works for `n=3`, `N=1`, an exact grid hit at `E`, and a grid interval containing `E`.

8. **Lifting to the actual grid.** On each segment between `0,t_a,t_b,T`, nonnegative endpoint increments have weighted sum equal to segment length. Dividing by that length therefore gives valid simplex-valued rates, each at most one. All segment boundaries are original grid endpoints, so the interpolated control is constant on every original interval. If `a=b` or `b=N`, the associated endpoint vectors coincide by monotonicity and their equal weighted sums; the empty segment is ignored. Thus at most three phases and three component types are established, not merely asserted for a coarsened model.

9. **Exact bit complexity.** Each region has ten variables, three independent equalities, and nineteen inequalities. Coefficients have rational encoding length polynomial in the grid encoding length and `log n`. Variables are bounded, including `E<=t_a<=T`, so a nonempty region has an optimal vertex. One fully explicit theoretical algorithm enumerates choices of seven inequality rows to supplement the three equalities, solves every nonsingular resulting rational system, and checks all constraints exactly. There are only `binomial(19,7)` such choices per region, an absolute constant. This proves the claimed polynomial bit complexity even without invoking a general polynomial-time LP method. The `log n` dependence refers to the value and a compressed witness; printing `n` separate rows would necessarily take at least linear time in `n`.

## Solver-independent proof of the nine-interval upper bound

Sort the five totals `m_1>=...>=m_5`, summing to 9.

If `m_1>=13/5`, select mode 2 until time 3 and mode 1 afterward. The initial deficit is at most 3. Every omitted total is at most `m_3<=3`. The final deficit is `6-m_1<=17/5`. This schedule therefore has error at most `17/5`.

If `m_1<13/5`, then

\[
m_2\ge\frac{9-m_1}{4}>\frac85.
\]

Choose an initial mode `p` maximizing `A_p(4)`, so `A_p(4)>=4/5`, and choose as final mode `q` a largest-total mode distinct from `p`. Then `m_q>=m_2>8/5`. Switch at time 4. Its initial deficit is at most `4-4/5=16/5`; its final deficit is below `5-8/5=17/5`; and every omitted total is below `13/5`. Again its error is at most `17/5`.

This proves the universal upper bound. The original lower witness and the proposed three-phase representative both attain `17/5`, proving equality. In particular, the exact nine-interval result can be presented with a short elementary proof independently of the general LP theorem and its certificates.

## Independent computational checks

The separate script [check_finite_math_review.py](../code/cia_reopened/check_finite_math_review.py) passed the following checks:

- 33 comparisons between the candidate compressed LP optimum and independently assembled LPs retaining every original mode and every original grid-interval rate. After the explicit formula was implemented, the same script was extended and rerun to compare all three values: rational formula, rational-certified compressed LP, and full-control LP. These cover `n=3,4,5,7`, unit grids with one through five intervals, the five-mode nine-interval case, and twelve rational nonuniform grids with `n=3,4,5,8` and two, four, or six intervals. The independent full-control LP comparison is numerical supporting evidence for compression; the proof above supplies exact justification.
- Every returned extremizer in those comparisons was checked in rational arithmetic by enumerating all initial modes, all final modes, and all grid cutoffs, including constant schedules, and accumulating the original absolute prefix discrepancies. This check does not use the schedule identity or the candidate region constraints.
- Both the earlier irregular five-mode nine-interval matrix and the new three-phase matrix have exact best discrepancy `17/5` under that same original-definition enumeration.

Reproduce with:

```bash
python code/cia_reopened/check_finite_math_review.py
```

The candidate primal and dual checks correctly verify feasibility, multiplier signs, stationarity, and equal rational objectives. The separate universal upper-bound certificate for every region avoids trusting a numerical infeasibility status. However, bounded-denominator recovery from floating-point solutions can fail on valid rational inputs. Such a failure is not a counterexample to the theorem; the implementation does not promise complete exact solution on all rational data. Also, when the optimum equals the initialized baseline `T/3`, the current code can return no maximizing witness, although the proof explicitly supplies one. Neither point invalidates the certified values or the mathematical result.

## Audit of the explicit-formula refinement

The author subsequently added equations (2)–(7), eliminating linear programming and improving the structural statement to two component types. These equations were independently audited after the original review above.

### Two-large-modes term

In the second LP family, the initial deficit of mode 2 at `t_b` is at least its deficit at `t_a`, which is at least `E`. Thus both distinguished cumulative allocations at `t_b` are at most `t_b-E`. Remaining total allocation is at most `T-2E`; summing gives `4E<=T+t_b`. The cutoff and `m_2>=E` give `2E<=T-t_(b-1)`. For a value strictly above `T/3`, these inequalities require `t_(b-1)<T/3<t_b`, except that an endpoint at `T/3` permits only equality `E=T/3`. This justifies selecting the first endpoint `C=t_c>=T/3`.

The proposed `H` satisfies all needed inequalities:

\[
T/3\le H\le T/2,\quad H\le C,\quad
4H\le T+C,\quad T-C\le2H\le T-t_{c-1}.
\]

Here `H<=C` follows from `(T+C)/4<=C` when `C>=T/3`. The tail total `T-2H` is nonnegative and at most `H`, so the ordering of individual tail totals also holds for every `n>=3`. At `C`, the two distinguished cumulative values sum to `max(0,C-T+2H)` and the tail values sum to `min(C,T-2H)`, totaling `C` exactly. Each distinguished value is at most both `H` and `C-H`; the latter bound is exactly `4H<=T+C` in the nonzero case. These facts verify all constraints of the original second LP with `a=b=c`. When `C=T`, its endpoint states equal their totals, so no positive-length segment is lost.

### Averaging all but one mode

This strengthens the earlier averaging argument validly. In the strict-threshold first case, every tail mode has initial deficit above `E` at `t_a`. Averaging all of them retains that inequality and gives a common total no larger than the old second-largest total. The final eligibility cutoff for a tail mode consequently moves later. Mode 1's trajectory is unchanged, so its nondecreasing initial deficit remains above `E` at that later cutoff. The limiting argument handles equality and proves that a single distinguished mode suffices for coverage of this family. It does not assert that averaging preserves the label `b` of every original region; allowing a later label is essential and correctly included.

### Eliminating the cumulative allocations

Let `A=t_a`, `B=t_b`, `P=t_(a-1)`, `Q=t_(b-1)`, and put

\[
K=(n-1)E-(n-2)A.
\]

All original state constraints require `x>=K`, `y<=B-E`, `0<=x<=y<=M`, and `0<=A-x<=B-y<=T-M`. Necessity of `E<=A`, `nE<=(n-2)A+B`, and the interval (6) follows directly. For sufficiency take an `M` in that interval and use `x=max(0,K,A-T+M)`, `y=max(x,B-T+M)`.

- `x<=A`: the three candidates satisfy this because `E<=A` and `M<=T`.
- `x<=M`: use `M>=T/n>0`, `M>=K`, and `A<=T`.
- `x<=B-E`: the zero candidate uses `E<=A<=B`; the `K` candidate uses `nE<=(n-2)A+B`; and `A-T+M<=A-P-E<=B-E` uses `M<=T-P-E`.
- `y<=M` follows from `x<=M` and `B<=T`; `y<=B-E` follows from `x<=B-E` and `M<=T-E`.
- `y-x<=B-A` follows from `x>=A-T+M`. Together with `x<=A`, this gives `0<=A-x<=B-y`. The final inequality `B-y<=T-M` follows from `y>=B-T+M`.

Thus the max formulas satisfy every state constraint. In particular `a=b` forces `x=y`; no separate division or limiting argument is needed for reconstruction of the endpoint states.

### Eliminating the largest total

Denote the four lower endpoints of (6), in their displayed order, by `l_1,...,l_4`, and its two upper endpoints by `r_1,r_2`. The eight comparisons are exactly:

| Comparison | Equivalent condition |
|---|---|
| `l_1<=r_1` | `E<=(n-1)T/n-P` |
| `l_1<=r_2` | `E>=(n-1)T/n-B` |
| `l_2<=r_1` | `P<=A`, automatic |
| `l_2<=r_2` | `E>=((n-1)T-A-(n-1)B)/n` |
| `l_3<=r_1` | `E<=((n-1)T-P-(n-1)Q)/n` |
| `l_3<=r_2` | `Q<=B`, automatic |
| `l_4<=r_1` | `E<=(T-P+(n-2)A)/n` |
| `l_4<=r_2` | `(n-2)(T-A)<=(n-1)B` |

Adding `E>=T/3`, `E<=A`, and `nE<=(n-2)A+B` gives precisely the three lower bounds, five upper bounds, and separate time condition in equations (3)–(4). The interval is closed, so `U_ab=L_ab` is correctly retained. No denominator changes sign because `n>=3`.

The resulting maximum over `H` and retained `U_ab` is therefore exact. Each pair uses a fixed number of rational operations, and all expressions depend directly on input endpoints and `n`, giving the claimed `O(N^2)` arithmetic and polynomial bit bounds. The rational formula also gives a complete exact computational route without numerical infeasibility decisions or floating-point rational recovery. A separate code reviewer is independently testing the formula's implementation and reconstruction.
