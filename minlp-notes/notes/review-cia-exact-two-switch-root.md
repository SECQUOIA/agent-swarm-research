# Root review of the exact continuous two-switch CIA formula

Date: 2026-09-04. This is an internal independent proof review, not external peer review.

Reviewed `results/cia-exact-two-switch-worst-case.md` in full. The analytic
three-distinct-mode reach argument and its transfer to the worst-case CIA
formula pass this review. No unresolved mathematical issue was identified.

The main checks were:

- The contradiction is posed on the compact horizon `L=min(T,B3)`. Latest
  feasible endpoints exist. Failure to reach L makes all first and pair
  reaches strictly interior, so the endpoint equalities and strict terminal
  inequalities remain valid when the cumulative functions have plateaus.
- At the second and third largest first reaches, monotonicity bounds the
  earlier-time allocations of the larger-reach modes by their allocations
  at their own reaches. Summing allocations gives the two sorted-reach
  inequalities. Both displayed algebraic identities are correct, and the
  required coefficient in the three-largest-reach identity is positive
  already at n=4.
- Pair feasibility gives an upper bound on the allocation of the final
  mode at M. Excluding mode i gives a lower bound on its allocation at Mi.
  Monotonicity between Mi and M yields inequality (5) with the stated signs.
- A maximizing pair remains available after excluding any of its n-2
  other modes. Hence only two excluded-pair reaches can differ from M.
  Their excluded maxima obey `xp+xq >= x+y` and `yp+yq >= 2z`, including
  ties. This proves the aggregate inequality without assuming that a
  maximizing pair uses the two largest first reaches.
- The coefficient of M in the aggregate bound is positive for n>=4.
  Substitution of its lower bound gives `sum Mi >= n B2`. Summing the
  strict terminal inequalities then contradicts L<=B3.
- In the CIA transfer, a total exceeding T/4 invokes the previously
  reviewed heavy-mode lemma at threshold T/4. Otherwise all totals are
  at most T/4, so positive discrepancies are bounded automatically.
  Distinct use of each selected mode makes its largest negative discrepancy
  occur at its block endpoint, exactly the quantity controlled by reach.
- Four pure blocks and the uniform-input construction provide both lower
  bounds. Adding unused modes is valid. The rational formula crosses T/4
  between n=7 and n=8, and its stated expansion is correct.

The earlier heavy-mode lemma and uniform-input formula are explicit
prerequisites. Their separate reviewed proofs remain necessary. The current
result is continuous-time only. Literature priority is a separate question;
this review does not certify novelty.
