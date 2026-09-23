# Independent audit of the arbitrary-block one-sided CIA bound

Date: 2026-09-04. Reviewer: independent `review_fbbt` agent.

The theorem and recursive construction in `results/cia-arbitrary-block-one-sided-bound.md` pass independent audit. The proof establishes the coefficient

`C_(n,k)=[n(n-1)+(n-k)(n-k-1)]/[nk(2n-k-1)]`

for arbitrary-profile **one-sided** error using at most `k` distinct blocks, for every `n>=2` and `1<=k<n`. Its two-sided consequence is restricted to profiles whose terminal masses are at most the target error, including all equal-total profiles. The proof does not establish this two-sided bound for unrestricted profiles.

## Base case and inductive invariant

For one block, use a mode with largest terminal mass `a>=T/n`. Its negative discrepancy `t-A_i(t)` is nondecreasing and ends at `T-a<=(n-1)T/n`. Other modes have nonpositive negative discrepancy. This proves the base coefficient and preserves the auxiliary invariant `C_(n,1)>=1/n` for `n>=2`.

For the inductive step, `k>=2`, `n>=3`, and the child instance has `n-1>=2` modes and `1<=k-1<n-1`. Thus it remains inside the theorem's domain. Assume the child coefficient `C` is a valid upper bound and satisfies `C>=1/(n-1)`.

The proposed parent threshold is

`E/T=[(n-1)^2 C+1]/[n(n-1)(1+C)]`.

Its difference from `1/n` is exactly

`(n-2)[(n-1)C-1]/[n(n-1)(1+C)]>=0`.

Hence the inductive coefficient invariant propagates together with the error bound. There is no need to assume the closed form in advance to justify this invariant.

## Largest-mass shortcut and positivity

Choose a maximum-mass mode `q`, with total `a`. If `a>=T-E`, constant use of `q` has negative error at most `E` and finishes the instance. This shortcut includes equality.

Otherwise define `L=T-a-E` and `E'=E-a/(n-1)`. The strict branch inequality gives `L>0`. Because `E>=T/n`,

`a<T-E<=(n-1)E`,

so `E'>0`. This is the key point allowing the theorem to cover arbitrary totals without an all-light assumption. At the boundary where this argument could yield zero child tolerance, the constant-mode shortcut has already applied.

Also `L<T` because `a+E>0` for a positive horizon. All resulting prefix and final-block durations are valid.

## Completed-control prefix and cumulative transfer

On the other modes, define

`alpha_hat_i=alpha_i+alpha_q/(n-1)`.

These rates are nonnegative and sum to one, so they are valid simplex-valued measurable rates. Their cumulative allocations satisfy

`A_hat_i(t)=A_i(t)+A_q(t)/(n-1)`.

Apply the child theorem to their restriction to the **absolute interval `[0,L]`**. Its negative error is at most `CL`. The required comparison `CL<=E'` is equivalent to

`E>=[CT+(1/(n-1)-C)a]/(1+C)`.

Since `C>=1/(n-1)`, the right side is nonincreasing in `a`. Substitution of the lower bound `a>=T/n` yields exactly the chosen parent threshold. The sign of this substitution was checked explicitly.

The original negative discrepancy of every prefix mode is completed-control negative discrepancy plus `A_q(t)/(n-1)`. Hence it is at most `E'+a/(n-1)=E` throughout the prefix. This uses cumulative history from time zero; it does not reset discrepancies or marginal integrals when a recursive block is created.

Append `q` on `[L,T]`. During that block its negative discrepancy is `t-L-A_q(t)`, which is nondecreasing and ends at `E`. Before activation it is nonpositive. All previous modes receive no more occupation and their negative discrepancies cannot increase. The prefix excludes `q`, so the resulting at-most-`k` blocks use pairwise distinct modes.

Recursive calls may choose a different maximum-mass mode after completing and restricting the rates. This is permitted: the child theorem applies to its entire transformed instance, and the parent transfer compares the resulting child schedule back to the parent's cumulative allocations.

## Recurrence transform and closed form

With `D_(n,k)=n C_(n,k)`, direct substitution gives

`D_(n,k)=[(n-1)D_(n-1,k-1)+1]/[n-1+D_(n-1,k-1)]`.

For `eta=(D-1)/(D+1)`, the recurrence is exactly

`eta_(n,k)=[(n-2)/n] eta_(n-1,k-1)`.

The base dimension is `m=n-k+1>=2`, and its base value is `eta_(m,1)=(m-2)/m`. Including that base factor gives the product over **all** `j=n-k+1,...,n`, not only over the recursive steps:

`eta_(n,k)=prod_j (j-2)/j=(n-k)(n-k-1)/[n(n-1)]`.

Solving for `D` gives the stated coefficient. Its denominator is positive because

`n(n-1)-(n-k)(n-k-1)=k(2n-k-1)>0`.

The formula confirms `C_(n,k)>=1/n`, with equality at `k=n-1`. When that endpoint case is reached, the product contains the factor zero at `j=2`; this is legitimate and introduces no division by zero. The formula also recovers `(n-1)/n` at `k=1`.

## Uniform one-sided lower bound, including repeated modes

The lower coefficient

`L_(n,k)=1/[n((n/(n-1))^k-1)]`

is correct for uniform relaxed controls even when integer schedules are allowed to reuse a mode. To see this directly, let `b_j` be the endpoint of block `j`, and let `v>=0` be prior integer occupation of its selected mode before that block. A one-sided tolerance `E` implies

`(1-1/n)b_j-b_(j-1)+v<=E`.

Thus, with `r=n/(n-1)`,

`b_j<=r(b_(j-1)+E-v)<=r(b_(j-1)+E)`.

Iteration gives `b_k<=nE(r^k-1)`. Covering the horizon therefore requires the displayed lower coefficient. Conversely, choosing `k` distinct modes and the equality endpoints attains this one-sided value when `k<n`. This supplies an independent derivation rather than relying on a two-sided formula whose extra omitted-mode term is irrelevant here.

## Fixed-block asymptotics and precise scope

For every fixed `k`, expansion of the closed form gives

`C_(n,k)=1/k-(k+1)/(2kn)+(k^2-1)/(4kn^2)+O_k(n^-3)`.

Expanding `(1-1/n)^(-k)` in the uniform expression gives

`L_(n,k)=1/k-(k+1)/(2kn)+(k^2-1)/(12kn^2)+O_k(n^-3)`.

Both expansions and their difference were checked algebraically. Uniform input is admissible for the unrestricted one-sided minimax and the equal-total two-sided minimax. The one-sided theorem supplies the first upper bound. For equal-total profiles, each mass is `T/n<=C_(n,k)T`, so all positive discrepancies are automatically below the same target, supplying the second upper bound.

Each of the two minimax quantities is therefore squeezed separately to

`T/k-(k+1)T/(2kn)+O_k(T/n^2)`.

The draft correctly does not assert equality of the two finite-`n` minimax values. The asymptotic statement is for fixed `k`; it does not claim a uniform remainder when `k` grows with `n`.

## Constructibility and independent recursive tests

The recursion decreases both mode count and available block count, so it terminates after at most `k-1` reductions or earlier through the largest-mass shortcut. For piecewise-constant rational rates, every completion, cumulative integral, threshold, and truncation endpoint is rational and can be computed finitely. The output always uses original mode names, with no repeated activation block.

An independent exact-rational implementation tested 360 inputs with two through thirteen modes and varying admissible block counts. It verified the negative-error contract at **every recursive level**, not only for the final original control. The tests exercised 928 recursive reductions, five non-base largest-mass shortcuts, and 355 one-block base cases. All contracts and final schedules passed. On 241 inputs satisfying the terminal-mass condition, the same final schedules also passed both-sided error checks.

All tests evaluated discrepancies at every relaxed-grid endpoint and every recursively generated switch time; discrepancies are affine between these points. The computations supplement the analytic proof. No mathematical correction or unresolved boundary case was found.
