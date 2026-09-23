# Independent audit of the general four-block reach theorem

Date: 2026-09-04. Reviewer: `review_extension`. Status: passed. This is an independent mathematical and implementation audit, not external peer review or a literature-priority determination.

Reviewed [the theorem](../results/cia-general-four-block-reach.md), [integer/polynomial checker](../code/cia-distinct-reach/verify_general_four_block.py), and [certificates](../code/cia-distinct-reach/certificates_general_four_block.json). The four-distinct-block reach formula holds for every integer `n>=5`, and the resulting one-sided three-switch minimax value is exactly

```
T / {n[(n/(n-1))^4-1]}.
```

## Necessary continuous-control constraints

The same endpoint facts checked in [the five-mode audit](review-cia-five-mode-four-block.md) apply for general `n`. Under `M<L`, every first reach and pair endpoint is uncapped. Continuity gives `F_i(R_i)=E`, and any available ordered pair whose latest endpoint is no later than `v<L` satisfies `F_k(v)>=R_j+E`. This proves each pair inequality. Event allocations are nonnegative and sum to their event time.

The imposed allocation orders follow from inclusions between available pair sets. Deleting indices outside a globally maximizing pair preserves that pair, so the appropriate restricted maxima equal `M`; imposing both allocation orders correctly enforces these equalities. The program omits all first-reach allocation variables and first-reach equations, enlarging the feasible set. It also imposes no total ordering of reaches beyond the stated inclusion orders. Both omissions are safe for a lower-bound certificate.

There are `3n-6` excluded pairs meeting a fixed three-element set, and therefore `3n-2` pair-maximum events after adding the three single-exclusion events and the global event. The objective coefficients in the program are exactly those of

```
C=(n-1)^2 H_S - 3n^2 sum_(i!=z) R_i.
```

The certificate bound `C>=3n^2(n-1)` is consequently equivalent to the claimed strong weighted inequality at `E=1`.

## Exhaustive symmetry reduction

Permutations preserving the selected set give three possible intersection sizes for the maximizing pair. Once that unordered pair is fixed, the distinguished index has respectively three, four, or three orbits: an endpoint or nonendpoint inside/outside the selected set, with the outside distinctions retained when needed. These are exactly the ten cases listed by the checker. The last case requires six different indices and is correctly omitted only at `n=5`. Hence `n=5,...,22` gives `9+17*10=179` finite cases.

For a chosen case, permuting modes outside `S union P union {z}` preserves every constraint and the objective of the full auxiliary LP. Averaging feasible points over that finite group preserves their objective. Equalities of variables in each orbit therefore preserve the optimal value of the LP relaxation, even though the averaged event data need not come from one actual control. Realizability of the averaged data is unnecessary.

I checked the canonical variable labels carefully. A pair event contains at most one unlabeled index because its excluded pair meets `S`. For its allocation variables, the unlabeled index of the event and an allocation to a different unlabeled mode are distinguished. The local `seen` dictionary in `canonical` retains exactly this equality information. It does not identify the self-allocation with another mode's allocation. Individual `R` variables have one common orbit outside the distinguished set. The row builder adds coefficients when variables share an orbit; it does not overwrite them.

Every available ordered pair is inserted before duplicate quotient rows are removed. Both the available-set exclusion and the condition of distinct pair indices are enforced. Deduplication is safe because it checks that coinciding left-hand sides have the same right-hand side. Objective multiplicities are added over the original events and modes before interpretation as a quotient objective, so orbit sizes are not lost.

## Why the symbolic program is exact for every large integer

There are at most six individually labeled indices. A nonsum row can involve at most three additional indices: one in a pair event and the two distinct modes in an endpoint inequality. Monotonicity rows need no more. Thus three unlabeled modes suffice to realize every possible row orbit. Since all representative cases label an initial segment contained in `{0,...,5}`, `n>=9` contains every pattern.

Additional indices introduce only rows and variables already in these orbits. Their first representatives occur before the extra indices are reached, so the insertion order also stabilizes. In particular, the row numbering used by saved symbolic certificates is consistent with the actual quotient, not merely consistent up to an unverified permutation.

Mass rows are sums over all modes and must be considered separately from this three-index statement. Their orbit coefficients are constants, `n-s`, or `n-s-1`: the second subtraction occurs when the event itself singles out one unlabeled mode. Objective orbit multiplicities are constants or `n-s`. These are the only count-dependent coefficients. Therefore the equality matrix is affine in `n`, and the objective is the relevant affine count times `(n-1)^2` or `-3n^2`. Its degree is at most three. Reconstruction from `n=9,10` is exact for these known affine counts; it is not a guess from two samples.

As a separate implementation check, I evaluated the symbolic equality matrices and objectives at `n=11,23,31` and compared them with freshly constructed integer quotients for all ten cases. All 30 comparisons agreed exactly, including variable order, inequality row order and right-hand sides, and equality row order. This corroborates the preceding structural argument; finite comparisons alone would not prove the all-`n` claim.

## Certificate algebra and exact checks

For finite cases, the checker verifies a positive integer denominator `q`, nonpositive integer inequality multipliers, valid row indices, and the identity

```
q c=A^T y+B^T z.
```

It also verifies `b^T y+d^T z=q*3n^2(n-1)`. Multiplying `Ax<=b` by `y<=0` reverses the inequality, and the equality rows have unrestricted multipliers. Dividing by `q` gives the required lower bound by weak duality. No nonnegative-variable residual needs to be inferred: the residual is checked to be exactly zero.

For symbolic cases, multiplication, addition, coefficient trimming, and the binomial shift are implemented with exact integer lists in ascending coefficient order. I checked the shift formula: the coefficient of `t^k` in `p(h+t)` is the sum of `p_j * binom(j,k) * h^(j-k)` over `j>=k`.

The checker establishes the polynomial identities

```
D=(n-1)^2 D0,
D0 c=A^T Y+B(n)^T Z,
b^T Y+d^T Z=3n^2(n-1) D0.
```

The coefficient test for `D(23+t)` guarantees `D>0` for every real `t>=0`; hence `D0>0` there because `(n-1)^2>0`. The coefficient test for each `-Y(23+t)` guarantees `Y<=0`. Equality multipliers need no sign condition. Division by `D0` is therefore justified, giving the same weak-duality bound for every integer `n>=23`. The extra denominator polynomial `D` is not mistakenly used as the coefficient-identity denominator.

I ran the standalone checker: all 179 finite cases and all ten polynomial certificates passed. Its expected case list covers every required integer, and its input contains only integer polynomial coefficients and multiplier data, not executable symbolic expressions. It rejects optimized Python execution that would remove assertions.

I also checked uniform-control primal witnesses in every one of the 30 independent quotient comparisons. Use `R_i=n/(n-1)`, all pair-event times `n(2n-1)/(n-1)^2`, and allocation equal to event time divided by `n`. These satisfy every quotient constraint exactly and attain `C=3n^2(n-1)`. Thus the certificates match feasible, sharp LP values.

## From the strong inequality to four blocks

Choose `z` with minimum first reach. At that time, monotonicity and the uncapped first-reach equalities give

```
R_z=sum_i A_i(R_z)<=sum_i A_i(R_i)=sum_i R_i-nE.
```

Therefore `sum_(i!=z)R_i>=nE`. Substituting in the strong inequality gives `H_S>=3nB_2` with the stated constant, without any ordering constraint in the certificate LP.

Assuming failure to reach `L=min(T,B_4)`, all three-block reaches are also uncapped. The established three-block theorem either contradicts `L<=B_3` directly or proves `G>=B_3`. Appending each available final mode to an excluded-pair maximizer and comparing allocations at `N_i` and `G` gives

```
(n-2)N_i >= nE+P_i+sum_(k!=i)Q_ik-G.
```

For a maximizing triple with mode set `S`, all `n-3` other excluded-mode maxima equal `G`. Summing the preceding inequality over its three indices yields the displayed bound on `sum_i N_i`. The coefficient of `G` is

```
n-3-3/(n-2)=(n^2-5n+3)/(n-2)>0  for n>=5.
```

Substituting `G>=B_3`, `H_S>=3nB_2`, and `(n-1)B_3=n(B_2+E)` simplifies exactly to `sum_i N_i>=nB_3`. Failure of each appended fourth mode at `L` gives the strict inequality `F_i(L)>N_i+E`, including flat reaches. Summing contradicts `L<=B_4`.

The selected modes are distinct, so the endpoint constraints control their entire one-sided trajectories. Uniform controls give the converse even for schedules that repeat modes, because a block's current occupation is at least its own duration. The recurrence `t_j<=r(t_(j-1)+E)` iterated at most four times gives `T<=B_4`. This verifies both the reach theorem and the exact one-sided minimax consequence.

The result does not establish a two-sided three-switch minimax formula or a formula for arbitrary numbers of blocks. The polynomial certificate proves all mode counts in the stated four-block problem; it does not extrapolate the result from numerical experiments.
