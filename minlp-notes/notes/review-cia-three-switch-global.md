# Independent audit of the three-switch global CIA upper bound

Date: 2026-09-04. Reviewer: independent `review_fbbt` agent.

The proof in `results/cia-three-switch-global-upper.md` passes independent audit. It establishes the upper coefficient

`max{1/5,U_n}`, where

`U_n=(n^4-7n^3+21n^2-29n+15)/[n(2n-3)(2n^2-6n+5)]`,

for every `n>=5`. Together with the established lower witnesses, this proves exact values `F_(n,3)(T)=T/5` for `n=5,...,11` and the asymptotic expansion

`F_(n,3)(T)=T/4-5T/(8n)+O(T/n^2)`.

The argument uses the independently audited three-distinct-mode prefix theorem and the separately audited three-switch heavy-mode lemma. It does not assume a four-distinct-mode prefix theorem.

## Completing the relaxed control after excluding one mode

Choose a largest-total mode `q`, let its total be `a`, and put `m=n-1`. The rates on the other modes

`alpha_hat_i=alpha_i+alpha_q/m`

are nonnegative and sum to one. In particular each is at most one, so this is a valid measurable simplex-valued control on `m` modes. Its cumulative allocation is

`A_hat_i(t)=A_i(t)+A_q(t)/m`.

For a schedule using only these modes, original negative discrepancy is exactly completed-control negative discrepancy plus `A_q(t)/m`. Thus a bound `E'=E-a/m` for the completed control implies the original bound `E` throughout the entire prefix. This calculation uses cumulative allocations from time zero; it does not reset discrepancies at block boundaries.

When the original totals are all at most `E`, one has `a<=E` and `E'>0` for `m>=4`. The known prefix theorem applies to the completed control without any assumption on its totals. It supplies three distinct original modes, all different from `q`, covering any target no longer than

`B=c[(n-1)E-a]`, where `c=((n-1)/(n-2))^3-1`.

## Boundary correction at five modes

An initial informal version asserted `c<1` for `n>=5`. This was caught during the audit: at `n=5`, `c=37/27>1`. The property holds for `n>=6`, since already at six `c=61/64<1` and the ratio decreases afterward.

The final proof correctly handles `n=5` using the earlier heavy-mode plus all-light greedy theorem, which already gives exact error `T/5`. The completed-control proof is then restricted to `n>=6`. No incorrect sign argument at five modes remains.

## Threshold, target, and final block

Set `E=T max{1/5,U_n}`. If any total exceeds `E`, the heavy-mode lemma applies because `T<=5E` and `n>=4`, giving error at most `E`.

Otherwise all totals are at most `E`; all positive discrepancies are consequently at most `E` for any integer schedule. The explicit formula gives `U_n<1/4`, and therefore `E<=T/4`. Thus the proposed prefix target

`L=T-a-E`

satisfies `T/2<=L<T`. In particular, it is positive and leaves a valid final block of length `a+E`.

The prefix condition `B>=L` is equivalent to

`[(n-1)c+1]E+(1-c)a>=T`.

For `n>=6`, the coefficient `1-c` is positive. Because `q` has the largest total, `a>=T/n`. The condition therefore follows from

`E/T >= (n-1+c)/[n((n-1)c+1)] = U_n`.

Every inequality uses an assumption already established: all-light masses give positivity of `E'`, and largest-total selection gives the lower bound on `a`. There is no circular threshold or reach assumption.

Use the completed-control prefix up to `L`, then activate `q` until `T`. The final mode has occupation `a+E`, so its final negative discrepancy is exactly `E`; its starting and all other positive discrepancies are at most its total `a<=E`. Earlier modes receive no additional occupation after `L`, so their negative discrepancies cannot increase. The complete schedule has at most four distinct blocks and at most three switches.

## Algebra and exact plateau

The rational expression for `U_n` follows by substituting

`c=(3n^2-9n+7)/(n-2)^3`.

The denominator is positive for `n>=5`. The claimed upper comparison checks exactly:

`1/4-U_n=(10n^3-56n^2+101n-60)/[4n(2n-3)(2n^2-6n+5)]`.

Under `n=5+h`, its numerator is `10h^3+94h^2+291h+295`, proving positivity throughout the stated range.

The table of exact values for `n=5,...,11` was checked independently. Each is below one fifth. The tightest listed case is eleven modes:

`1/5-7561/37829=24/189145>0`.

Thus the theorem gives `T/5` throughout that range. Five distinct pure-mode intervals of equal duration give the matching lower bound because three switches permit visiting at most four distinct modes. This lower construction is valid for each of the listed mode counts.

## Asymptotic lower bound and correction

For sufficiently large `n`, the exact uniform-input lower coefficient is

`L_n=(n-1)^4/[n(4n^3-6n^2+4n-1)]`.

Direct expansion gives

`U_n=1/4-5/(8n)+11/(16n^2)+O(n^-3)`,

`L_n=1/4-5/(8n)+5/(16n^2)+O(n^-3)`.

Their exact difference is the rational expression displayed in the draft and has expansion `3/(8n^2)+O(n^-3)`. Consequently the coefficient `-5/8` in the first mode-count correction belongs to the exact global worst case by squeezing. The theorem does not identify its second-order coefficient or an exact finite-mode formula beyond the plateau.

## Constructibility and independent tests

For piecewise-constant rational input, the added relaxed rates, threshold `E'`, prefix target, and all inverse evaluations remain rational and can be computed exactly. The completed control is only an auxiliary object used to choose the original integer modes. The resulting integer schedule itself uses only original modes.

An independent exact-rational implementation tested 484 all-light profiles with six through eighteen modes, including 204 profiles within the exact plateau range six through eleven. It formed the completed control, constructed the three-distinct-mode prefix, appended the excluded mode, and verified both discrepancy signs against the **original** control at every relaxed-grid endpoint and schedule switch time. All tests passed. Cases with a mode exceeding `E` are covered by the separate heavy-mode audit and its independent tests.

No substantive mathematical issue remains after the five-mode boundary correction. Novelty is a separate literature-review question.
