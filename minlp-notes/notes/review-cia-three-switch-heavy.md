# Independent audit of the three-switch heavy-mode theorem

Date: 2026-09-04. Reviewer: independent `review_fbbt` agent.

The constructions in `results/cia-three-switch-heavy-mode.md` pass independent mathematical audit. They establish the heavy-mode theorem for `n>=4`, the all-light greedy prefix bound, exact continuous CIA values `F_(n,3)(T)=T/5` for `n=5,6,7,8`, and the upper bound `T/5` for `n=4`. Neither a four-distinct-mode reach conjecture nor numerical optimization is used in these proofs.

One minor mathematical wording correction was sent to the author and incorporated: the negative-discrepancy supremum for a mode activated once is bounded by `max{0,ell-A_i(b+ell)}`, not by `ell-A_i(b+ell)` alone. The latter endpoint can be negative while discrepancy at time zero is zero. Checking that endpoint against the positive threshold is sufficient, so the correction changes none of the constructions or conclusions. The matching Case 1 wording and the greedy lemma's reached-time scope were also corrected and reread.

## Normalization and endpoint rules

If `T<=5E`, extend the relaxed control to `[0,5E]` by giving all additional allocation to any fixed mode. The original heavy mode remains heavy. Restricting any valid schedule on the extended horizon back to `[0,T]` preserves its error bound and cannot increase its number of blocks. Rescaling time reduces the proof to `T=5`, `E=1` without changing the assumptions on the number of modes.

For a mode used once on `[b,b+ell]`, relaxed-minus-integer discrepancy is nondecreasing before the block, nonincreasing on it, and nondecreasing afterward. Thus its positive-error supremum is

`max{A_i(b),m_i-ell}`,

and its negative-error supremum is

`max{0,ell-A_i(b+ell)}`.

For a heavy mode `m_i>1`, the latest level-one time

`d_i=max{t:A_i(t)<=1}`

exists, belongs to `[1,5)`, and satisfies `A_i(d_i)=1`. Before or at that time the cumulative allocation is at most one; after it the allocation is strictly greater than one. This remains valid with arbitrary flat portions of `A_i`.

## Case 1: some total is at least three

Choose `q` with `m_q>=3`. The other totals sum to at most two, so at most one other mode has mass strictly above one. Choose that mode as `p` if necessary and use `p` for one unit, then `q` for four units.

The first mode has mass at most two, so its final positive discrepancy is at most one, and its negative endpoint is at most its unit block length. For the final mode, `A_q(1)<=1` and the negative endpoint `4-m_q<=1`. Its possible final positive discrepancy introduces no missing condition: `m_q-4<=A_q(1)`, since at most four units can be allocated after time one. Every omitted mode is light.

The boundary `m_q=3` is included in this case, as is a pure control with `m_q=5`.

## Case 2: one two-unit block and three unit blocks

Assume every total is below three and at most one exceeds two. Choose that exceptional mode as `q` if it exists; otherwise choose any heavy mode. Thus `1<m_q<3`, and every other total is at most two.

There are at most four heavy modes. Select three distinct modes other than `q` containing all the remaining heavy modes. If fewer than three are needed, fill the remaining positions with light modes; `n>=4` guarantees enough distinct choices. Sort these three modes by their level-one deadlines, assigning artificial deadline five to selected light modes.

Choose an integer `j in {0,1,2,3}` with `j<=d_q<=j+2`. The proposed ceiling formula always does so because `1<=d_q<5`. Use `q` on `[j,j+2]`. The remaining three unit slots have start times

`0,...,j-1` and `j+2,...,4`.

They number exactly three and, together with the two-unit block, partition the complete horizon. Place the other selected modes on these slots in deadline order.

The deadline proof is correct, including equality cases:

- A mode with deadline-order index `ell` placed before `q` starts at `ell-1`. If its deadline were earlier, all first `ell` selected modes would have allocation strictly above one at that time, exceeding the available total allocation.
- A mode placed after `q` starts at `ell+1`, with `ell>=j+1`. If its deadline were earlier, the first `ell` selected modes would together have allocation strictly above `ell`. Also `d_q<=j+2<=ell+1`, so mode `q` has allocation **at least** one there. Their combined allocation exceeds the time `ell+1`, a contradiction.

Any violating mode and all its earlier deadline-ordered predecessors are heavy: their alleged deadlines are below their start times, which are at most four, whereas light modes have artificial deadline five. The distinction between strictness for the first `ell` modes and non-strictness for `q` is sufficient for the contradiction and handles deadline plateaus exactly.

Thus every unit-block mode starts with allocation at most one. Its mass is at most two, so its final positive discrepancy is at most one; its negative endpoint is at most the unit block length. Mode `q` starts no later than its deadline and ends no earlier, giving starting allocation at most one and ending allocation at least one. Its mass is below three and its block length is two. Both discrepancy bounds follow. All omitted modes are light.

## Case 3: two totals exceed two

If two totals exceed two while every total remains below three, those are the only heavy modes because all remaining masses sum to less than one. Order their deadlines as `a=d_q<=b=d_r`.

The proof's time bounds hold:

- `b>=2`; otherwise both heavy cumulative allocations exceed one at time two.
- `a<3`; otherwise both heavy allocations are at most one at time three and all remaining allocations total less than one, contradicting the total allocation three.
- `b<4`; each mass above two forces `A_i(4)>=m_i-1>1`.

Set `tau=max{2,a}`. Then `2<=tau<3` and `a<=tau<=b`. Choose any remaining light mode `p` and use the four-block pattern

`p: [0,tau-2]`, `q: [tau-2,tau]`, `r: [tau,tau+2]`, `p: [tau+2,5]`.

All intervals are ordered and nonnegative in length. Mode `q` starts by its deadline and ends at or after it. Mode `r` starts by its deadline and ends at or after four, strictly after its deadline. Each heavy mode receives length two and has final mass below three, so the one-block endpoint checks apply.

The repeated use of `p` does not rely on an invalid one-block monotonicity argument. Its two blocks have combined length exactly one, so its cumulative integer occupation is always at most one. Its cumulative relaxed allocation is always below one because its total is below one. These two direct bounds control both discrepancy signs. Zero-length initial blocks are simply deleted; at most four blocks remain.

These three mass cases are exhaustive, with exact masses two and three assigned to their stated non-strict branches.

## All-light greedy prefix lemma

Assume every total is at most `E` and let `1<=k<n`. Define

`t_0=0`, `t_j=j(n-j+1)E/(n-j)`.

The times increase strictly. At stage `j`, provided the previous endpoint `t_(j-1)<T`, let `u=min(T,t_j)`. The previous modes are distinct and their cumulative allocations sum to at most `(j-1)E`. One of the `n-j+1` unused modes therefore has

`A_i(u)>=[u-(j-1)E]/(n-j+1)`.

The identity

`(n-j)t_j=(n-j+1)t_(j-1)+(n-2j+2)E`

is exact. Since `n-j>0` and `u<=t_j`, it implies the required inequality

`A_i(u)>=u-t_(j-1)-E`.

This remains valid when `n-2j+2` is negative; the proof does not discard that term or require it to be nonnegative. The unused mode can thus occupy the entire next block with negative endpoint at most `E`. Previous modes receive no more occupation and retain their negative bounds. Every positive discrepancy is automatically at most the mode total.

The procedure stops at `T` if that endpoint is reached and otherwise produces a prefix of length `t_k`. Its error guarantee is for both signs up to the reached time. It does not assert completion of an arbitrary longer horizon when `t_k<T`. The author was asked to state this prefix scope explicitly if needed to avoid ambiguity in the phrase “full cumulative error.”

The algorithm is constructive and may use future cumulative allocations at the prescribed endpoint. This is an offline CIA statement, so no causal or online-information restriction is violated.

## Exact values for five through eight modes

Set `E=T/5`. If any mass exceeds `E`, the heavy theorem applies. Otherwise the greedy lemma with `k=4` reaches the whole horizon for `5<=n<=8` because

`4(n-3)E/(n-4)>=5E=T`.

At `n=8` there is equality, which the proof permits. At `n=5,6,7` the upper reach is larger than the horizon and the algorithm stops at `T`. Four blocks correspond to at most three switches.

For `n=4`, a mass is at least `T/4>T/5`, so the heavy theorem always gives the stated upper bound. The theorem does not assert a matching four-mode lower bound.

For each `n>=5`, five distinct pure-mode intervals of length `T/5` give a lower bound `T/5`: a schedule with at most three switches visits at most four distinct modes and leaves one such mode unvisited. This proves exactness for `n=5,6,7,8`.

The discussion that the uniform lower bound dominates `T/5` from `n=12` onward is consistent with its exact formula. The comparison reduces to positivity of `n^4-14n^3+26n^2-19n+5`, which is positive at twelve and increases thereafter. No resolution for nine through eleven modes or the larger-mode regime follows from the present greedy lemma.

## Independent exact-rational checks

An independent implementation tested 1,200 randomized piecewise-constant profiles with four through twelve modes. Of these, 873 met the heavy-mode hypothesis: 77 used the mass-at-least-three branch, 768 used the two-unit-block deadline construction, and 28 used the two-heavy repeated-light construction. All four possible positions `j=0,1,2,3` of the two-unit block occurred. A further 77 all-light inputs with five through eight modes were completed by the greedy construction.

For all 950 applicable inputs, exact rational arithmetic verified horizon coverage, at most four nonempty blocks, and both discrepancy signs at every relaxed-grid endpoint and switch time. Every bound passed. These tests supplement the proof and do not replace it.

No substantive mathematical issue remains. The endpoint-bound wording corrections described above have been incorporated and checked.
