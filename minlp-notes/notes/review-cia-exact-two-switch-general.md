# Independent audit of exact continuous two-switch CIA

Date: 2026-09-04. Reviewer: independent `review_fbbt` agent.

The complete proof in `results/cia-exact-two-switch-worst-case.md` passes independent audit. This includes the analytic three-distinct-mode prefix theorem for every `n>=4`, its transfer to arbitrary mode totals, the new exact value at `n=7`, and the exact uniform-input regime for `n>=8`. No computational certificate is needed for the proof.

The resulting formula is

`F_(n,2)(T)=T max{1/4,(n-1)^3/[n(3n^2-3n+1)]}`, for `n>=4`.

## Reach semantics, continuity, and capped horizons

Let `A_i(t)` be cumulative relaxed allocations and `F_i(t)=t-A_i(t)`. These functions are continuous and nondecreasing, since the relaxed control is measurable and simplex-valued. The identity `sum_i F_i(t)=(n-1)t` holds at every time.

For a mode not previously used, a block beginning at `b` has negative discrepancy `F_i(t)-b` at its endpoint `t`. Its maximum negative discrepancy over the block occurs at its endpoint. Before activation its negative discrepancy is nonpositive; after deactivation it cannot increase. Thus the reach constraint controls the entire prefix trajectory for schedules using distinct modes.

The latest feasible endpoint

`Phi_i(b)=max{t in [0,L]:F_i(t)<=b+E}`

exists and is at least `b`, for `0<=b<=L`. The feasible set is closed and contains `b` because `F_i(b)<=b`. The map `Phi_i` is nondecreasing in `b`, so taking the latest first-block endpoint loses no possible extension of a two-block prefix.

Under the contradiction assumption that no prefix with at most three distinct modes reaches `L`, all first and pair reaches lie strictly below `L`. Consequently

`F_i(R_i)=E`,

and if a pair reach `Phi_k(R_j)<=u<L`, then

`F_k(u)>=R_j+E`.

Flat segments cause no problem. A latest feasible endpoint strictly below the horizon must have equality with its threshold by continuity. Any later feasible point would contradict its maximality. At the final horizon, failure to append a mode gives a **strict** inequality, because equality would make the horizon itself feasible. This strictness is retained in the final contradiction.

## First-reach inequalities

Sort the first-block reaches as `x>=y>=z>=...`, choosing distinct indices even when values tie. At time `y`, every mode except one attaining `x` has allocation at most `y-E`; the exceptional allocation is at most `x-E`. This yields

`x+(n-2)y>=nE`.

The displayed identity in the draft then gives

`(n-1)x+y>=n^2 E/(n-1)`.

At time `z`, the top two allocations are at most `x-E` and `y-E`, and all other allocations are at most `z-E`. Therefore

`x+y+(n-3)z>=nE`.

Writing `u=x+y`, the identity

`(n-1)u+2z = [2n/(n-1)][u+(n-3)z] + [(n^2-4n+1)/(n-1)](u-2z)`

is algebraically exact. Its second coefficient is positive for every `n>=4`, including the boundary value `1/3` at `n=4`. Because `u>=2z`, it gives

`(n-1)(x+y)+2z>=2n^2 E/(n-1)`.

The restriction `n>=4` is material here; the second coefficient is negative at `n=3`. The proof therefore does not accidentally claim the false three-mode, three-distinct-block generalization.

## Aggregate excluded-pair inequality

Let `M` be the global largest reach using two distinct modes, and let `M_i` be the largest such reach excluding mode `i`. Let `x_i,y_i` denote the two largest first reaches after excluding `i`.

All pairs ending in `i` reach at most `M<L`, so

`A_i(M)<=M-E-x_i`.

Since `sum_i x_i=(n-1)x+y`, summation and the first-reach bound give

`M>=nE(2n-1)/(n-1)^2=B_2`.

Next fix `i`. For each `k!=i`, all first modes `j` outside `{i,k}` give pairs reaching at most `M_i`, hence

`A_k(M_i)<=M_i-E-max_(j outside {i,k}) R_j`.

As `k` ranges over the remaining modes, these maxima sum to `(n-2)x_i+y_i`: the largest remaining reach is available except when its own index is excluded, in which case the second largest is used. Ties do not alter this identity.

Subtracting the bounds from the total cumulative allocation at `M_i`, and using `A_i(M_i)<=A_i(M)`, yields exactly

`(n-2)M_i>=nE+(n-1)x_i+y_i-M`.

Now take a pair `(p,q)` attaining `M`. For every `i` outside this pair, that same pair is admissible in the definition of `M_i`; therefore `M_i=M`. This gives the exact identity

`sum_i M_i=(n-2)M+M_p+M_q`.

The excluded first maxima satisfy `x_p+x_q>=x+y`: if one exclusion removes a largest-reach index, the other still retains it; if neither removes it, both excluded maxima equal `x`. Each excluded second maximum is at least `z`, because removal of one index leaves at least two of the original top three.

Summing the two inequalities for `M_p,M_q` and applying the top-three first-reach bound gives

`sum_i M_i >= [n-2-2/(n-2)]M + [2nE+2n^2 E/(n-1)]/(n-2)`.

The coefficient of `M` is positive for `n>=4`; it is exactly one at `n=4`. Substitution of `M>=B_2` is therefore in the correct direction. The resulting expression equals `nB_2`, not merely a weaker quantity. One direct check is

`n-[n-2-2/(n-2)]=2(n-1)/(n-2)`,

whose product with `B_2` is exactly the additive term above. This proves the aggregate inequality.

## Closing the prefix contradiction

For each `i`, choose an actual maximizing pair excluding it and append mode `i`. This is a valid sequence of three distinct modes. Failure to reach the capped horizon gives

`F_i(L)>M_i+E`.

Summing and applying the aggregate inequality gives

`(n-1)L>sum_i M_i+nE>=nB_2+nE=(n-1)B_3`.

The last identity follows from `B_3=[n/(n-1)](B_2+E)`. Since the proof set `L=min(T,B_3)`, this is a contradiction. The argument covers both `T<B_3` and the critical equality `T=B_3` because the final inequality is strict.

A prefix reaching the target may be truncated at that target. Zero-length trailing blocks, if a first or second reach already equals the target, can be omitted. Thus the theorem produces at most three active blocks and at most two switches, without requiring extra switches to fill a time gap.

## Transfer to the exact global CIA value

Let `E=T max{1/4,1/[n(r^3-1)]}`, where `r=n/(n-1)`.

If a total exceeds `T/4`, the previously and independently audited heavy-mode lemma applies at threshold `T/4` and gives error at most `T/4<=E`. That lemma does not rely on the new reach theorem, so this use is not circular.

Otherwise all mode totals are at most `T/4<=E`, which bounds all positive discrepancies independently of the schedule. The new prefix theorem at threshold `E` reaches all of `[0,T]`, because `B_3>=T`. It controls all negative discrepancies. This proves the global upper bound for arbitrary measurable controls, without an equal-total assumption.

The lower bound `T/4` comes from four consecutive pure-mode blocks. Every schedule with at most two switches uses at most three distinct modes and omits one of those four. The uniform-control lower formula supplies the other displayed term. The exact uniform-input formula also contains a possible `T/n` term; omitting it here is harmless because `T/n<=T/4` for `n>=4`.

For `n=7`, the uniform term is `216T/889<T/4`, so the new prefix upper bound together with the four-block example proves the previously unresolved value `F_(7,2)(T)=T/4`. The same argument covers `n=4,5,6`. For all `n>=8`, the comparison polynomial `n^3-9n^2+11n-4` is positive, so uniform controls attain the global value.

Expanding that exact uniform rational expression gives

`F_(n,2)(T)=T/3-2T/(3n)+2T/(9n^2)+O(T/n^3)`.

This is now an expansion of the exact global worst case, not only of an upper certificate.

## Constructibility and numerical supplementation

The construction requires the first reaches, all ordered-pair reaches, and the final append tests. A global maximizing pair supplies every excluded maximum except possibly those excluding one of its two indices; two additional scans suffice for those exceptions. All operations are finite cumulative-integral and monotone-inverse evaluations. For piecewise-constant rational data they can be performed exactly. No computability assertion for arbitrary measurable input descriptions is required.

An independent exact-rational test generated 320 piecewise-constant profiles with `n=4,...,12`, including uniform controls, pure-mode segments, zeros, and flat inverse regions. Horizons were either `B_3` or `2B_3`. Every tested profile had a valid distinct-mode prefix reaching at least `B_3`, and the constructed prefix's negative discrepancy was checked at every relaxed-grid endpoint and every switch time. In 288 cases the pair reaches were uncapped; each also satisfied `M>=B_2` and `sum_i M_i>=nB_2` exactly. The uniform examples and capped-horizon cases also checked equality at the target.

These tests supplement the analytic proof. No mathematical correction or unresolved boundary case was found. Novelty remains governed by the separate CIA literature review.
