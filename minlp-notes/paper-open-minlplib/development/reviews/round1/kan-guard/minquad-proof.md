# Proof of the guarded quadratic lower bound

The copied `kan_bnb_rigexp.py` returns a binary64 lower bound, possibly
`-inf`, for

\[
\mu=\min_{g\in[g_l,g_h],\ s\in[s_l,s_h]}\left(gs+\frac m2s^2\right).
\]

All finite binary64 inputs are interpreted as their exact dyadic rational
values. The contract requires ordered intervals, `gl <= gh` and `sl <= sh`.
In particular it applies to every finite input with `sl <= 0 <= sh` and an
ordered slope interval. Signed zeros represent the same rational zero.
The result need not be the greatest binary64 lower bound.

The proof assumes round-to-nearest binary64 arithmetic with gradual
underflow, correctly implemented `nextafter` and comparisons, and correct
Python integer, `Fraction`, and rational-to-binary64 conversion operations.
It does not assume that halving every binary64 value is exact.

## Reduction to two ordinary quadratics

For each fixed real `s`, the expression is affine in `g`, so its minimum
on the slope interval is attained at `gl` or `gh`. Thus

\[
\mu=\min\left\{\min_{s\in[s_l,s_h]}q_{g_l}(s),
                 \min_{s\in[s_l,s_h]}q_{g_h}(s)\right\},\qquad
q_g(s)=gs+\frac m2s^2.
\]

For each endpoint slope, the interval minimum is attained at an endpoint
of the displacement interval, or, when `m > 0`, at the vertex
`s* = -g/m` if it belongs to the interval. If `m <= 0`, endpoint minima
suffice. This includes constant quadratics and zero-width intervals.

## Fast path: guards and endpoints

Guards run for every scalar entry of every vector invocation. The fast path
is accepted only when:

1. All five inputs are finite and both intervals are ordered.
2. `sl <= 0 <= sh`.
3. `half_m = RN(0.5*m)` satisfies `2*half_m == m`.
4. All raw and outward-rounded arithmetic intermediates are finite,
   including those in subsequently ignored `np.where` branches.
5. The downward-rounded vertex denominator is positive.

Here `RN` denotes binary64 rounding to nearest. `half_m` is finite for
finite `m`. Doubling the halved value is exact: it is a power-of-two scaling
that cannot lose a bit at the subnormal boundary and cannot overflow in this
range. Consequently the equality in guard 3 implies the exact identity
`half_m = m/2`, including zeros. This check is needed even for a normal `m`
just above the smallest normal value; “normal input” alone is insufficient.

Write `D(x)` and `U(x)` for a rounded binary64 operation followed by
`nextafter` toward negative and positive infinity. With finite guarded
intermediates, these enclose the exact operation even if it underflows.
For an endpoint displacement `s`, the code computes

\[
G=D(gs),\qquad
M=\begin{cases}
 D((m/2)D(s^2)),&m\ge0,\\
 D((m/2)U(s^2)),&m<0.
\end{cases}
\]

By monotonicity with respect to the square and the sign of `m/2`,
`G <= gs` and `M <= (m/2)*s^2`. This remains true when `D(s^2)` is negative
because the rounded square was zero. Thus `D(G+M) <= q_g(s)`. The minimum
of the four endpoint lower bounds covers every endpoint minimizer.

## Fast path: vertices

For positive `m`, the denominator `d = D(2*m)` satisfies `0 < d <= 2*m`.
The numerator `n = U(g*g)` satisfies `n >= g^2 >= 0`. Therefore

\[
- U(n/d)\ \le\ -\frac{g^2}{2m}.
\]

This is a lower bound for the exact unconstrained vertex value. The code
also computes `v = RN(-g/m)` and `[D(v), U(v)]`, an enclosure of the exact
vertex location. The vertex is included if that enclosure intersects
`[sl,sh]`. A vertex actually in `[sl,sh]` cannot be excluded. An extra
vertex included because of enclosure width cannot hurt the lower bound:
its unconstrained value is no greater than the interval minimum of the
same quadratic. The former unrounded division with heuristic `1e-9` and
`1e-300` padding is no longer used.

For nonpositive `m`, `mpos = 1` keeps unused vertex arithmetic defined,
and the vertex candidate is never included. Its intermediates are still
checked. Taking the minimum of the endpoint bounds and all included vertex
bounds proves `best <= mu` for accepted entries. The signed-displacement
guard is checked explicitly, although this new enclosure argument itself
would work on any ordered displacement interval.

## Fallback and invalid inputs

Every failed entry goes to `_minquad_exact`; accepted entries retain the
fast result. For finite, ordered inputs the fallback converts all five
binary64 values exactly to `Fraction`, evaluates the four endpoint values,
and includes each exact admissible vertex value when `m > 0`. The preceding
reduction proves that its minimum rational `q` equals `mu`. This also covers
ordered intervals wholly to the left or right of zero, which trigger the
signed-displacement guard.

If `float(q)` is finite, it is converted back to a rational. The fallback
returns it when it is at most `q`; otherwise it returns its predecessor
using `math.nextafter`. Correct rounding ensures that predecessor is at
most `q`, including at zero and subnormal transitions. If conversion
overflows, a negative `q` returns `-inf`; a positive `q` returns the largest
finite binary64, which is below `q`. Thus overflow never produces a false
finite lower bound or a positive infinity result.

If any input is nonfinite, or either interval is reversed, the fallback
returns `-inf`. There is no claimed real optimization problem for NaN data
or reversed intervals. This result supplies no useful pruning bound and
cannot turn such data into a finite certificate. There are no exceptions
for signed zeros or zero widths. Broadcast-compatible scalar and array
inputs are supported; an empty array has no entries to certify.

## Counters

`calls` counts vector invocations; `entries` counts scalar quadratics.
`guard_calls` and `fallback_calls` count invocations with at least one failed
entry. `guard_entries` and `fallback_entries` count the union of failed
entries, once per entry. Every guard failure causes exactly one fallback
for that entry, including the invalid-input `-inf` response.
`invalid_entries` counts nonfinite or unordered data. The `reasons` counts
are per-entry counts for individual predicates, so they can overlap and
must not be summed to obtain the number of failed entries. The replay
counters cover all calls from process startup, including local-search
candidate certification and the branch-and-bound evaluations.

The denominator positivity predicate is a defensive guard. For finite
positive binary64 `m`, `2*m >= 2*t`, where `t = 2^-1074`; its predecessor
is at least `t` unless overflow occurs (which the finiteness guard catches).
Other `m` values select `mpos = 1`, except positive infinity, which is also
caught by finiteness. Its zero trigger count in the tests is therefore
expected.
