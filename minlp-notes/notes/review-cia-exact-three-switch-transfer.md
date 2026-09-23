# Independent audit of the exact three-switch CIA transfer

Date: 2026-09-04. Reviewer: independent `review_fbbt` agent.

The elementary transfer and final formula in `results/cia-exact-three-switch-worst-case.md` pass independent audit, using the four-distinct-mode prefix theorem as a separately audited input. This review does not duplicate its finite and symbolic certificate verification. The dependency's precise statement and passed audit in `notes/review-cia-general-four-block.md` were checked.

For every `n>=5`, the final formula is

`F_(n,3)(T)=T max{1/5,1/[n((n/(n-1))^4-1)]}`.

## Upper bound and dependency scope

Let `E` be the proposed right-hand side. It is at least `T/5`, so `T<=5E`.

If any terminal mass is strictly greater than `E`, the independently audited heavy-mode theorem applies. It has the required hypothesis `n>=4`, permits arbitrary measurable profiles, and gives a full two-sided schedule with at most three switches. There is no need to infer a stronger or different heavy threshold.

Otherwise every terminal mass is at most `E`. Every positive discrepancy satisfies `A_i(t)-W_i(t)<=A_i(T)<=E`, independently of the schedule. The separate four-block theorem applies for `n>=5`, controls original one-sided discrepancy for every mode, and reaches

`min{T,nE((n/(n-1))^4-1)}=T`.

It uses at most four distinct activation blocks, hence at most three switches. It requires no equal-total assumption. Combining its negative bound with the automatic positive bound gives the claimed full error. Equality cases at the mass threshold and at the reached horizon are included in these non-strict bounds.

This transfer is analytic. The four-block prefix theorem on which it relies has a computer-assisted exact proof, with finite rational and symbolic polynomial certificates. The final result should preserve this distinction rather than describe its entire proof as elementary or analytic.

## Matching lower witnesses

Five consecutive pure-mode intervals of length `T/5` are admissible when `n>=5`. Any schedule with three switches has at most four distinct visited modes, so one of the five is unvisited and has final discrepancy `T/5`.

The established uniform-control theorem applies because its switch budget satisfies `3<=n-2`. Its full two-sided value is

`T max{1/n,1/[n((n/(n-1))^4-1)]}`.

The additional term `T/n` is no larger than `T/5`. Therefore the maximum of the two admissible lower witnesses equals the proposed upper bound exactly. This proves the full finite-`n` formula, not only an asymptotic sandwich.

## Plateau transition and expansion

Comparison of the uniform fraction against `1/5` is equivalent to

`P(n)=n^4-14n^3+26n^2-19n+5>=0`.

Direct substitution gives negative values for `n=5,...,11`. The claimed expansion about twelve is exact:

`P(12+h)=h^4+34h^3+386h^2+1469h+65`.

Every coefficient is positive, so the polynomial is positive for `h>=0`. Thus the exact plateau ends at eleven modes, and uniform input is a worst case at every mode count from twelve onward.

Expanding the exact uniform fraction gives

`F_(n,3)(T)=T/4-5T/(8n)+5T/(16n^2)+O(T/n^3)`.

The second-order coefficient `5/16` is now the exact global coefficient, in contrast with the earlier upper-bound sandwich.

## Verification boundary

The heavy-mode proof was independently audited in `notes/review-cia-three-switch-heavy.md`, including its endpoint, deadline, and repeated-mode cases. The general four-block proof and checker have a distinct independent audit. No large certificate checker was rerun for this transfer review, because the present argument uses that result only through its stated, verified theorem.

No further mathematical correction was identified. The transfer file's provisional status can be synchronized with its now-passed dependency review. Novelty and external peer review remain separate questions.
