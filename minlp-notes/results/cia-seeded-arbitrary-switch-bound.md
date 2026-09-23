# Stronger general switching bounds from the exact four-block theorem

Date: 2026-09-07. Status: analytic transfer and independent full review complete. This is a supporting consequence of the existing exact reach theorem, with a modest new plateau case.

Let `k` be the allowed number of activation blocks and let `n>k>=4`. Define

```
m=n-k+4,
theta = m(m-1)/(n(n-1)) * [2((m-1)/m)^4-1],
C* = (1+theta)/(n(1-theta)).
```

Every measurable `n`-mode relaxed control has a schedule with at most `k` distinct activation blocks and one-sided cumulative error at most `C* T`. The full two-sided minimax consequently obeys

```
F_(n,k-1)(T) <= T max{1/(k+1),C*}.
```

The one-sided coefficient strictly improves the previous general coefficient for every `n>k>=4`. Full-error improvement occurs where the maximum with the omitted-mode threshold changes. In particular,

```
F_(16,4)(T)=T/6.
```

The prior general bound certified the four-switch plateau through fifteen modes. For fixed `k`, the upper-minus-uniform-lower gap is

```
(k^3-k-60)/(6k^2 n^2) + O_k(n^-3),
```

halving the leading gap for five blocks. This does not give an exact general finite-mode formula or a sharp second-order asymptotic law.

## Transfer mechanism

If an `(n-1)`-mode problem admits a one-sided coefficient `C>0` with at most `k-1` distinct blocks, completion of one removed mode gives at most `k` distinct blocks and coefficient

```
[(n-1)^2 C+1]/[n(n-1)(1+C)].
```

Choose a maximum-terminal-mass mode when `C>=1/(n-1)`, as in the earlier proof, and a minimum-terminal-mass mode when `C<1/(n-1)`. The latter choice supplies the reversed monotonicity required by the same inequality; no clipping of the seed is necessary. Under `eta=(nC-1)/(nC+1)` the recurrence multiplies `eta` by `(n-2)/n`. Starting with the proved exact four-block coefficient and telescoping yields `C*`. The universal heavy-mode theorem gives the full-error statement.

The [full proof and retained predecessor](../notes/cia-reopened-general-reach.md), [independent review](../notes/review-cia-reopened-general-reach.md), and [independent exact checker](../code/cia_reopened/check_seeded_review.py) verify all hypotheses, algebra, asymptotics, and the new plateau. The exact four-block seed retains its existing computer-assisted certificate dependency.

The same investigation retains an exact counterexample to a proposed event-LP relaxation for five-block reach. It satisfies the stated relaxation but has decreasing allocations between chronologically ordered events, so it is **not** a control counterexample. The higher-budget exact reach question remains open. No new general rounding principle or exhaustive literature priority is claimed for this seed propagation.
