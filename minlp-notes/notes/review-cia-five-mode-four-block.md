# Independent audit of five-mode four-block reach

Date: 2026-09-04. Reviewer: `review_extension`. Status: mathematical proof and exact certificates passed. This is an independent agent audit, not external peer review or a certification of literature novelty.

Reviewed [the result](../results/cia-five-mode-four-block-reach.md), [standalone checker](../code/cia-distinct-reach/verify_n5_weighted_pairs.py), and [rational certificates](../code/cia-distinct-reach/certificates_n5_weighted_pairs.json). The weighted inequality `H_S>=675E/16`, reach `min(T,1845E/256)` with at most four distinct modes, and exact one-sided minimax value `256T/1845` are correct.

## Continuous-control semantics

For a measurable simplex-valued control, each allocation `A_i` is continuous and nondecreasing, `sum A_i(t)=t`, and each `F_i=t-A_i` is continuous and nondecreasing. These facts justify the event LP without assuming piecewise constant controls or a time grid.

For a mode not used previously, its cumulative excess occupation at the end of a block `[b,t]` equals `F_i(t)-b`. Its largest excess during that block occurs at the endpoint; before the block it has no positive excess, and after the block its excess cannot increase if it is not used again. The inverse `Phi_i(b)` is therefore the correct latest feasible endpoint for distinct-mode schedules. It is nondecreasing in `b` and at least `b`, so choosing previous endpoints greedily does not reduce attainable reach.

Under `M<L`, every first reach is uncapped: each first reach occurs before some available two-mode reach, and all pair reaches are at most `M`. Thus `F_i(R_i)=E` by continuity. If a pair endpoint is no later than `v<L`, then monotonicity gives `F_k(v)>=R_j+E`. Equality holds at the actual uncapped endpoint even with a flat portion, since a latest feasible endpoint with strict slack could be extended by continuity. This proves both the first-reach equality and each pair inequality used in the LP.

Every asserted order is valid. A first reach precedes a pair maximum whenever its mode is available in that maximum. Each `Q_ij` is at most `P_i` for an included `i`, and all pair maxima are at most `M`. If a globally maximizing ordered pair uses the unordered mode set `{p,q}`, every restricted maximum still allowing these two modes equals `M`. No orientation information is needed for these equalities.

## Program construction and exhaustive coverage

I checked the checker row by row against these necessary conditions. There are 18 events and 108 nonnegative variables: a time and five allocations at each event. Its 18 mass equations and five first-reach equations give 23 equalities. It enforces known orders by all five componentwise allocation inequalities; the mass equations imply the corresponding time order. Imposing the reverse allocation inequalities at equal events gives equal allocations and times. None of these calls passes the same event twice, so dictionary construction does not accidentally overwrite cancelling coefficients.

For a `q` event, the available modes are exactly the complement of its excluded pair; for an `m` event they exclude its single index; and for the global event all five modes are available. Every ordered pair of distinct available modes is included in the endpoint inequalities. The checker does not assume an unproved ordering between different excluded-pair events.

For a selected three-mode set relabeled to `{0,1,2}`, permutations preserving that set have exactly three orbits on unordered pairs: both endpoints inside, one inside, or neither inside. Representatives `{0,1}`, `{0,3}`, and `{3,4}` therefore suffice. After mapping the actual maximizing pair to its representative, some permutation of the five first reaches puts them in nondecreasing order. All 120 such permutations are checked. Ties can use any compatible order; multiple maximizing pairs can use any one of them. Thus all controls are covered by the 360 cases.

The objective has coefficient one on the three `P_i` times. Its nine `Q_ij` times have coefficient two for the three pairs inside the selected set and coefficient one for the six crossing pairs. The total coefficient weight is `3+6+6=15`, exactly as in `H_S`. The three pair types produce respectively 485, 495, and 500 inequalities; their differences are precisely the available equality-to-global-maximum constraints.

## Exact certificate verification

For `Ax<=b`, `Bx=d`, and `x>=0`, the checked conditions

```
y<=0,   c-A^T y-B^T z>=0
```

imply

```
c^T x >= y^T A x+z^T B x >= y^T b+z^T d.
```

The checker verifies valid multiplier indices, signs of all inequality multipliers, every nonnegative dual residual, the exact target bound, and the expected case identifiers. It checks all 360 cases, rather than accepting the supplied list's coverage assertion. Omitted sparse multipliers are zeros. Every arithmetic operation uses `Fraction`; no floating-point reconstruction is performed during checking. Running under optimized Python is explicitly rejected so assertions cannot be silently removed.

I ran the checker successfully. I also constructed the uniform-control primal witness independently: every first event has time `5/4`, every pair event has time `45/16`, and every allocation at an event equals one fifth of its time. Exact rational checks confirmed that this witness satisfies all constraints in every one of the 360 LPs and has objective `675/16`. This both verifies sharpness and rules out an infeasible case being mistaken for a meaningful lower bound.

Audited file hashes:

```
verify_n5_weighted_pairs.py
feb252e4d98fa2c5d04074f27e27df6100e151d35cae46d98e2b88b1a7310f88

certificates_n5_weighted_pairs.json
5f5a5d22b369ba3132913fb0d90ff399f9fc0c06e2ff2aacc8bb2b969eedaf0a
```

The necessary LP need not characterize all possible controls. Its relaxation direction is correct: a lower bound valid on this larger feasible set also holds for every control. The finite rational certificates, together with the verified constraint semantics, are a complete proof of the weighted inequality.

## Transfer to four blocks and horizon caps

Set `L=min(T,B_4)` and assume no sequence of at most four distinct modes reaches it. Every reach of up to three distinct modes is then strictly below `L`, so all subsequent endpoint inequalities are valid uncapped inequalities. If `L<=B_3`, the previously proved three-block theorem already contradicts this assumption. Otherwise that theorem on the horizon `[0,L]` gives `G>=B_3`.

At `N_i`, appending each `k!=i` to a pair realizing `Q_ik` gives a three-mode sequence excluding `i`. Hence `F_k(N_i)>=Q_ik+E`. Summing over the four such modes and using the allocation mass equation gives the stated lower bound on `A_i(N_i)`. Similarly, a pair realizing `P_i` followed by `i` has endpoint at most `G`, so `A_i(G)<=G-E-P_i`. Monotonicity between `N_i` and `G` proves equation (5), with coefficient `3N_i` and no reversed inequality.

Choose a maximizing triple with mode set `S`. For the two indices outside `S`, `N_i=G`. Summing equation (5) only over the three indices in `S` therefore gives

```
sum_i N_i >= G+5E+H_S/3
           >= G+305E/16
           >= 5 B_3.
```

The last equality uses `B_3=305E/64`. Appending each excluded mode `i` to a triple attaining `N_i` yields four distinct modes. Failure at `L` gives the strict inequality `F_i(L)>N_i+E`; a weak inequality in the opposite direction would make `L` feasible by definition. Summing proves

```
4L > sum_i N_i+5E >= 5 B_3+5E = 4 B_4,
```

contradicting `L<=B_4`. This establishes the claimed result for short horizons as well as the uncapped target horizon. Flat cumulative functions do not require a separate perturbation argument.

## Exact one-sided minimax and limitations

For the upper bound, choose `E=256T/1845`; then `B_4=T`, and the reach result gives a schedule controlling the whole one-sided trajectory with at most three switches. For uniform controls, a block ending at `t_j` contributes at least its own length to that mode's occupation, even if the mode appeared before. Thus one-sided error at most `E` implies

```
t_j <= (5/4)(t_(j-1)+E).
```

Iterating at most four times yields `T<=1845E/256`, proving the matching lower bound without assuming distinct modes in the competing schedules. A minimizing schedule exists because there are finitely many mode sequences and their ordered endpoint sets are compact, with continuous discrepancy as a function of endpoints. The zero-horizon case is trivial.

The proof establishes a one-sided result. It does not bound the opposite discrepancy, prove the exact three-switch two-sided minimax, or extend the weighted certificate argument to arbitrary numbers of modes or blocks. Its literature novelty remains a separate question.
