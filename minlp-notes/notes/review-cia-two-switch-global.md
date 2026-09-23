# Independent audit of the global two-switch CIA bound

Date: 2026-09-04. Reviewer: independent `review_fbbt` agent.

The refined theorem in `results/cia-two-switch-global-upper.md` passes this independent audit. The heavy-mode lemma, unrestricted-total scope of the ordered-pair reach argument, final-mode selection, balancing formula, exact values for four through six modes, and asymptotic squeeze were checked independently. The proof applies to arbitrary measurable simplex-valued relaxed controls and uses at most two switches.

For `n>=4`, the audited bound is

`F_(n,2)(T) <= T max{1/4, (n-1)^3/(3n^3-3n^2-5n+4)}`.

## Discrepancy convention and endpoint control

Write `A_i(t)=integral_0^t alpha_i`, `m_i=A_i(T)`, and let the discrepancy be relaxed cumulative allocation minus integer occupation. Every `A_i` is continuous, nondecreasing, and one-Lipschitz, with `sum_i A_i(t)=t`. If an integer schedule uses a mode only once, its discrepancy is nondecreasing before its block, nonincreasing during the block, and nondecreasing afterward. The negative discrepancy is therefore controlled at the end of its active block; positive discrepancies are controlled before activation and at the final time.

In particular, whenever every total is at most `E`, **all positive discrepancies are automatically at most `E`**, regardless of the schedule. This is why the all-light construction only needs to check selected negative endpoints.

The exact one-switch formula used in the heavy-mode proof is valid. For modes `p,q` with a switch at `t`, the apparent additional positive endpoint `A_q(t)` is at most `t-A_p(t)`. The other apparent endpoint `m_p-t` is at most `T-m_q-t`. Thus the error is exactly the maximum of the omitted-mode totals and the two displayed negative-endpoint expressions. There is no missing positive-discrepancy term.

## Heavy-mode lemma

Assume `E>=T/4` and at least one total exceeds `E`. Then `E<T`, and at most three totals exceed `E`.

If the largest total `m_q>=T-2E`, the remaining totals sum to at most `2E`; hence at most one remaining total exceeds `E`. Select that mode as `p` if needed. The schedule `p` until `E`, then `q` until `T`, has all omitted totals at most `E`, initial negative endpoint at most `E`, and final negative endpoint `T-m_q-E<=E`.

Otherwise the largest total is less than `T-2E<=2E`. Since a total above `E` exists, this also gives `E<T/3`, so the block endpoints `E,2E` lie inside the time horizon.

If at least two totals exceed `E`, one such mode `q` must satisfy `A_q(2E)<=E`; otherwise two cumulative allocations would already sum to more than `2E`. Put the other heavy modes in the first two blocks of length `E`, filling any unused block with a distinct mode different from `q`. There are at most two other heavy modes, and `n>=3` supplies enough distinct names. The first two blocks have negative error at most their lengths. Their preactivation positive errors are at most `E` because their starting times are zero and `E`; their final positive errors are at most `m_i-E<E`. The last mode has preactivation error at most `E` by selection and final negative error

`T-2E-m_q<T-3E<=E`.

All omitted totals are at most `E`.

For a unique heavy mode `h`, the same last-mode construction works when `A_h(2E)<=E`. Otherwise use `h` first for length `2E`. Its negative endpoint is `2E-A_h(2E)<E`; its final discrepancy `m_h-2E` is negative because `m_h<2E`. Divide the remaining time equally between two other modes. Each new block has length `(T-2E)/2<=E`, and these modes have totals at most `E`. All discrepancies are therefore bounded.

These arguments also cover equality boundaries such as `m_q=T-2E`, `m_i=E`, and `A_q(2E)=E` in their stated branches. The proof does not silently assume that every total is at most `E` in the heavy case.

## The reach lemma does not require equal totals

The ordered-pair lemma is imported from a file about equal-total controls, but its **own proof does not assume equal totals**. This distinction was checked directly.

For a horizon `L>0`, define `R_i=max{t in [0,L]:t-A_i(t)<=E}`. Continuity and monotonicity ensure the maximum exists. If all `R_i<L`, each satisfies `R_i-A_i(R_i)=E`, including when the cumulative functions have flat pieces.

Let `x,y` be the largest and second largest reaches, and choose `p` attaining `x`. At time `y`, every other mode obeys `A_i(y)<=y-E`, while `A_p(y)<=x-E`. Summing gives

`x+(n-2)y>=nE`.

Since `x>=y`, the identity in the imported proof yields

`(n-1)x+y>=n^2 E/(n-1)`

for `n>=3`; its surplus coefficient is `(n^2-3n+1)/(n-1)>0`. If every ordered-pair value `R_p+A_q(L)` were below `C`, summation against the largest and second-largest reaches would give

`L<nC-[(n-1)x+y]`.

Choosing `C=nE/(n-1)+L/n` contradicts the preceding lower bound. Thus the asserted ordered pair exists for arbitrary totals.

## The third-largest-total lemma

Assume all totals are at most `E`, and write `b=m_(3)`, `r=n/(n-1)`, and `L=T-b-E`. If `L<=0`, constant use of a top-three mode works. If `L>0`, it lies below `T`. A reach equal to `L` gives a one-switch schedule ending with an unused top-three mode, whose total is at least `b`.

Otherwise the pair lemma applies. The condition

`E>=(T-b)/(1+r+r^2)`

is exactly equivalent to `rE+L/n>=L-E`: both reduce to `E(r+r^2)>=L`. Thus there are distinct `p,q` with `R_p+A_q(L)>=L-E`. The first switch

`t_1=max(0,L-A_q(L)-E)`

satisfies `0<=t_1<=R_p<=L`. Use `p`, then `q`, then a top-three mode distinct from both. Such a final mode always exists, even if both initial modes belong to the top three or the first block has zero length.

The initial and middle negative endpoints are at most `E` by construction. The final endpoint is at most `T-L-b=E`. Every positive discrepancy is at most its mode total, hence at most `E`. This establishes the lemma without an implicit equal-total condition or a mode-reuse assumption.

## Global balancing is not circular

Normalize `T=1`. The proof fixes the threshold explicitly from `n`:

`E=max{1/4, (n-1)/[(n-2)(1+r+r^2)+6]}`.

Its second fraction simplifies to the theorem's rational expression, and `1/4<=E<1/3` for `n>=4`.

The first split uses the **fixed threshold one quarter**, not the unknown actual error: if any total exceeds one quarter, the heavy-mode lemma already constructs error at most one quarter. Otherwise all totals are at most one quarter and therefore at most `E`.

Let `a` be the largest total in this all-light case. If `a>=1-3E`, use a largest-total mode last, beginning at `2E`, and two other distinct modes on the first two blocks of length `E`. All positive errors are at most `E`, the first two negative errors are at most the block lengths, and the last negative endpoint is `1-2E-a<=E`.

If `a<1-3E`, the remaining `n-2` totals after the two largest sum to at least `1-2a`. Each is at most the third largest, so

`m_(3)>=(1-2a)/(n-2)>(6E-1)/(n-2)`.

The explicit definition of `E` gives

`E(1+r+r^2)>=1-(6E-1)/(n-2)>1-m_(3)`.

Thus the third-largest lemma applies. Its assumption that all totals are at most `E` was already established before this calculation. There is no circular use of the conclusion to justify a mass bound.

## Exact small-mode values and asymptotic squeeze

For `n=4,5,6`, the rational term in the upper bound equals `27/128`, `64/279`, and `125/514`, respectively; each is at most one quarter. Four successive pure-mode blocks of duration `T/4` give a matching lower bound: every schedule with at most two switches visits at most three distinct modes, leaving one of these four modes unvisited. Its final cumulative discrepancy is `T/4`.

For `n>=8`, the established uniform-input lower bound is

`T(n-1)^3/[n(3n^2-3n+1)]`.

Subtracting it from the new upper bound gives exactly

`T(n-1)^3(6n-4)/[n(3n^2-3n+1)(3n^3-3n^2-5n+4)]`.

This is `2T/(3n^2)+O(T/n^3)`. Both bounds have first terms `T/3-2T/(3n)`, so the claimed equality up to `O(T/n^2)` follows by squeezing. More explicitly, their second-order coefficients are `2/9` and `8/9`, respectively; the true coefficient is not identified by this theorem.

The uniform expression exceeds `T/4` for all `n>=8`: the comparison reduces to `n^3-9n^2+11n-4>=0`, which holds at eight and increases thereafter. The remaining-gap discussion is therefore consistent with the exact small-mode lower construction.

## Constructibility and supplementary checks

For arbitrary measurable controls, the theorem is an existence statement using cumulative-integral access. The reach times are well-defined monotone inverse evaluations. For piecewise-constant rational relaxed data, all displayed thresholds and switch times can be computed by finite cumulative-array scans and rational arithmetic. No computability claim for arbitrary noncomputable measurable inputs is needed.

An independent exact-rational implementation constructed and checked schedules for 600 randomized piecewise-constant inputs with four through sixteen modes. It checked all relaxed-grid endpoints and all schedule switch times, which suffices because every discrepancy is affine between such points. All 600 schedules met the claimed bound. Cases included 91 large-heavy schedules, 108 multiple-heavy schedules, 108 unique-heavy-last schedules, seven unique-heavy-first schedules, 120 all-light largest-total schedules, and 166 all-light ordered-pair schedules.

These computations supplement the proof. No mathematical error or unresolved scope issue was found. The author was asked only to make explicit that filler modes in the heavy construction are distinct from each other and the final mode; the required choices always exist.
