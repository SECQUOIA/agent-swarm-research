# Independent audit of the universal heavy-mode CIA lemma

Date: 2026-09-04. Reviewer: audit_mccormick, independently of cia.
Status: the analytic proof in
[cia-universal-heavy-mode-rounding.md](../results/cia-universal-heavy-mode-rounding.md)
passes this fresh full audit. The argument applies to every finite number of
modes and every nonnegative integer switch budget. This is a mathematical
verification, not a priority or external-refereeing claim.

## Precise statement and normalization

For a measurable simplex-valued relaxed control on `[0,T]`, write
`A_i(t)=∫_0^t α_i(u)du`. These functions are continuous, nondecreasing, and
1-Lipschitz; they satisfy `Σ_i A_i(t)=t`. The claimed bound concerns both signs
of every cumulative error, uniformly over time.

The assumptions are `E>0`, `s≥0` an integer, `T≤(s+2)E`, and at least one
terminal mass strictly greater than `E`. Extending the relaxed control to the
larger horizon `(s+2)E` preserves that strict mass condition. Under `t=Eu`, the
normalized allocation is `A_i(Eu)/E`; its derivative remains simplex-valued.
Thus the normalized problem has integer horizon `M=s+2≥2` and error target one.
Restriction after rounding preserves the discrepancy and cannot add switches.

There is no hidden requirement such as `n≥s+1`. A one-mode profile is harmless,
and the construction covers switch budget zero through `M=2`. A zero horizon
cannot meet the strict heavy-mode assumption and therefore makes no unsupported
existence claim.

## Integral prefix rounding

I checked the finite network independently. Each of the `M` time nodes supplies
one unit. Assignment arcs enter the chosen mode's chain at that slot. A chain
edge following slot `k` carries exactly the cumulative assigned count through
that slot. Its integral capacity interval is

```
[floor(A_i(k)), ceil(A_i(k))].
```

The final edges feed a common sink with demand `M`. The actual interval-average
allocations define a feasible fractional flow. Assignment arcs can be bounded
by one and every chain flow by `M`, so a bounded feasible network polytope
suffices. Integral supplies and capacities give integral vertices. At an integral
vertex, the one-unit supply at each time node selects exactly one assignment arc,
hence one mode per slot.

For a heavy mode `h`, maximizing its final chain flow has an optimum at least
`A_h(M)>1`, because the original fractional flow is feasible. An integral
optimum therefore selects that mode at least twice. Merely taking an arbitrary
rounded vertex would not establish this last conclusion; the objective used in
the proof is necessary for its stated reasoning and is valid.

Real-valued prefix allocations cause no integrality problem: their floors and
ceilings are integers. The existence proof requires no rational approximation.
For rational finite input the network can also be constructed exactly. No claim
about exact computational access to arbitrary measurable functions is needed.

At an integer prefix, floor/ceiling rounding forces exact equality when the
allocation is integral, and bounds the error by less than one otherwise.
The subsequent reordering may use the full closed error-one interval; this is
why its lemma is properly stated with non-strict inequalities.

## First-repeat prefix and preserved information

If a word contains a repeated mode, its first repetition occurs at some position
`r≥2`. In the first `r` slots, the repeated mode `q` occurs twice, precisely
`r−2` other modes occur once, and all others occur zero times. Endpoint error
one consequently gives

```
1≤A_q(r)≤3;
A_i(r)≤2 for the other selected modes;
A_i(r)≤1 for every omitted mode.
```

These inequalities concern the shortened prefix only. An omitted mode may have
large allocation later; that does not affect the argument because the reordered
prefix keeps every mode's cumulative service at `r` unchanged. The original
suffix then has exactly the same cumulative error as before, at every later
time, not merely at its grid points.

I independently reconstructed the scheduling step before reading the author's
full proof. Its useful feature is the restricted service multiset: one service
block of length two and all remaining selected service blocks of length one.
This avoids an unjustified application of a generic nonpreemptive scheduling
claim with arbitrary job lengths.

## Deadlines, plateaus, and the double block

The set `{t∈[0,r]:A_q(t)≤1}` is nonempty and compact, so its latest point `d_q`
is well defined. Since `A_q(t)≤t`, one has `d_q≥1`. If `A_q(r)=1`, the latest
point is `r`; otherwise continuity gives `A_q(d_q)=1`. Thus allocation is at
most one before `d_q` and at least one at and after `d_q`, including plateau
endpoints.

The chosen integer

```
j=min(r−2,max(0,ceil(d_q)−2))
```

lies in `[0,r−2]` and satisfies `j≤d_q≤j+2`. If the right truncation is active,
`j+2=r≥d_q`; otherwise the ceiling expression gives the required right inequality.
The left inequality follows from `ceil(d_q)−2≤d_q` and the endpoints. This also
covers `r=2`, integer deadlines, and `d_q=r`.

Giving `q` slots `[j,j+2]` therefore bounds its allocation before activation by
one and ensures its allocation at the end of the double service is at least one.
The final prefix discrepancy is at most one because `A_q(r)−2≤1`.

For the remaining selected modes with mass greater than one, the latest
level-one deadline has the same strict implication:

```
t>d_i  implies  A_i(t)>1.
```

Modes of prefix mass at most one get artificial deadline `r`. They cannot cause
a deadline violation because every unit slot starts by `r−1`.

## Independent check of the deadline-order proof

Order the `r−2` single-service modes by nondecreasing deadline; ties may be
resolved arbitrarily. Let `ℓ` be a mode's position in that order.

Before the double block its start is `ℓ−1`. If its deadline were smaller, the
first `ℓ` modes would all have allocation strictly greater than one at that
time. Their sum would exceed `ℓ`, contradicting total allocation `ℓ−1`.

After the double block its start is `ℓ+1`, and `ℓ≥j+1`. A violating deadline
would force the first `ℓ` modes to have combined allocation strictly greater
than `ℓ`. At this time the double-block mode has allocation at least one,
since `d_q≤j+2≤ℓ+1`. The total allocation would then exceed `ℓ+1`, again
contradicting its exact value. The non-strict contribution of `q` is sufficient
because the other contribution is strict. Thus deadline plateaus do not invalidate
the contradiction.

This proves the required earliest-deadline order directly, without relying on
an external EDF theorem that might require different release-time or job-length
assumptions.

## Both discrepancy signs and continuous time

For a single-service mode, cumulative integer service never exceeds one, so
negative error `W_i−A_i` is at most one automatically. Before activation,
positive error `A_i−W_i` is bounded by the deadline. During its selected unit
block it is nonincreasing. Afterwards its largest positive value is at most
`A_i(r)−1≤1`.

For the double-service mode, positive error before activation is at most one.
During service it is nonincreasing. The negative error is nondecreasing during
service and is at most `2−A_q(j+2)≤1` at the end. After service the negative
error decreases, while positive error is bounded by `A_q(r)−2≤1`. Every omitted
mode has zero integer service and allocation at most one over the entire prefix.

All these monotonicity arguments hold for arbitrary measurable original rates:
on a selected interval, `(W_i−A_i)'=1−α_i≥0` almost everywhere, and on an
unselected interval the derivative is `−α_i≤0`. Absolute continuity converts
those derivative inequalities into monotonicity. Therefore endpoint checks on
each constant-mode block control the whole interval even when the relaxed rate
varies within it. Averaging the input did not silently replace the original
continuous-time discrepancy objective.

The two consecutive slots assigned to `q` give at least one adjacent equality
in the final `M`-letter word. A word has at most `M−1` switch positions, so one
equality reduces this to at most `M−2=s`. Other equalities only improve the count.

## Independent exact-rational checks

I wrote a separate checker,
[audit_universal_heavy.py](../code/cia_tv_conjecture/audit_universal_heavy.py),
using dynamic programming over integral prefix-count vectors rather than the
author's network-flow implementation. It finds a floor/ceiling word whose chosen
heavy mode has terminal count at least two, performs the first-repeat reordering,
and checks all resulting prefix discrepancies exactly with rational arithmetic.

The deterministic run checked 1,412 randomly generated heavy profiles with
one through seven modes and horizons two through fourteen. It made 810
nontrivial reorderings and left 6,941 suffix slots unchanged. First-repeat
positions ranged from two through eight, and double-block starts ranged from
zero through six.

Three additional feasible error-one words explicitly exercised prefix repeated
mass exactly one, prefix repeated mass exactly three, and an interior plateau
at level one. All passed. In total 1,415 exact checks passed. These computations
supplement the analytic proof and do not establish its arbitrary-size scope
on their own.

## Outcome and limits

No mathematical correction was needed. The full heavy-mode theorem is valid
as stated. Its adjacent pair need not use the mode whose terminal count was
maximized: the first-repeat rule may select another mode. The earlier counterexample
to forcing an arbitrary prescribed heavy mode is therefore consistent with this
proof. The largest-mode adjacent-pair strengthening remains separate.

The conditional reduction to a future universal one-sided distinct-mode reach
bound is logically valid. It is not a proof of that reach bound. In particular,
this audit does not infer a complete exact minimax formula for every mode and
switch count from the heavy-mode lemma alone.

## Addendum: global upper bound and plateau transfer

At the author's request I also checked the short consequence in
[cia-arbitrary-switch-global-bound.md](../results/cia-arbitrary-switch-global-bound.md).
I used the stated, already independently reviewed arbitrary-block one-sided
bound as a dependency; this addendum is not a new full audit of its recursive
proof.

For `1≤k<n`, let

```
C=[n(n−1)+(n−k)(n−k−1)]/[nk(2n−k−1)],
E=T max{1/(k+1),C}.
```

A mass greater than `E` invokes the heavy-mode theorem with `s=k−1`. Otherwise
all positive errors are bounded by their terminal masses, and the one-sided
schedule bounds every negative error by `CT≤E`. The transfer is valid for all
profiles and requires no assertion about which mode is largest.

I independently verified the exact identity

```
C−1/(k+1)
=2(n−k−1)(n−k(k+1)/2)/[nk(k+1)(2n−k−1)].
```

The denominator is positive on the stated domain. Consequently the upper bound
is `T/(k+1)` throughout `k+1≤n≤k(k+1)/2`, for integer `k≥2`. The matching
profile uses `k+1` distinct pure modes with equal total allocations. A schedule
with at most `k` activation blocks uses at most `k` different names, even when
repetitions are allowed, so at least one positive-mass mode is omitted. Its
terminal discrepancy proves the lower bound. The plateau conclusion is correct
and does not assert that this sufficient interval is maximal.

The two expansions in the draft also pass. For the uniform lower coefficient,
put `z=1/n` and expand

```
(1−z)^(-k)=1+kz+k(k+1)z²/2+k(k+1)(k+2)z³/6+O_k(z⁴).
```

After division by `z` and inversion this gives
`1/k−(k+1)/(2kn)+(k²−1)/(12kn²)+O_k(n^−3)`. Direct expansion of the rational
upper coefficient gives the same first two terms and second-order coefficient
`(k²−1)/(4k)`. These establish the claimed sharp first mode-count correction
for every fixed `k`, with a remaining difference `(k²−1)/(6kn²)+O_k(n^−3)`.
The assertion also handles `k=1`, when both displayed coefficients are exactly
`1−1/n`. I checked the rational factorization symbolically for general `n,k`
and the lower expansion explicitly for `k=1,...,9`, in addition to the algebra
above. No correction to this transfer or its corollaries was required.

## Final addendum: exact full-to-one-sided minimax identity

I freshly read the complete new corollary (4) and proof in
[cia-universal-heavy-mode-rounding.md](../results/cia-universal-heavy-mode-rounding.md).
The identity passes:

```
F_{n,k−1}(T)=max{T/(k+1),G^-_{n,k}(T)}   for 1≤k<n,
```

where `G^-` is the worst, over the same relaxed-profile class, of the minimum
negative discrepancy using at most `k` activation blocks. Repeated mode names
are allowed. This is an identity between worst-case minimax values, not a
profile-by-profile identity with the fixed lower threshold.

The minimum for an individual profile is attained. Fix a mode word of length
`k` and let its `k−1` internal switch times vary over the compact ordered
simplex in `[0,T]`. Zero-length intervals represent schedules with fewer blocks.
For two such vectors of switch times, the measure of the intervals where their
selected controls differ is at most the sum of the absolute switch-time changes.
Each mode's cumulative occupation therefore varies continuously in uniform norm
(a bound by twice that sum also suffices). The maximum negative discrepancy is
1-Lipschitz in that uniform occupation norm. Taking a minimum over this compact
simplex and then over the finitely many mode words proves attainment. Measurable
relaxed profiles have continuous cumulative allocations, so no additional rate
regularity is needed.

For `T>0`, the threshold `E=max{T/(k+1),G^-}` is positive. For every relaxed
profile a mass greater than `E` invokes the heavy-mode theorem with `s=k−1`.
Otherwise its attained one-sided minimum is at most the global supremum `G^-`,
and every positive discrepancy is at most the corresponding terminal mass.
This proves the upper bound simultaneously for all profiles. Attainment of the
supremum over profiles is not required.

For each fixed profile and schedule the full discrepancy dominates the negative
one. Taking first minima over the same schedule class and then suprema over
profiles proves `F≥G^-`. The separate omitted-mode witness proves
`F≥T/(k+1)` because `k<n` supplies `k+1` distinct modes. The explicit zero-horizon
case is correct. These establish both directions of the identity without any
conjecture about distinct optimal modes or uniform worst-case profiles.

No change was needed to the written corollary. This completes the requested
final bounded audit; no additional investigation was started.
