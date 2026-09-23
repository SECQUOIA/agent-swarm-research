# Independent review: two-switch CIA with equal mode totals

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.
Reviewed: `results/cia-two-switch-equal-masses.md`.

## Verdict

The theorem and full written proof are correct. For `n≥4`, arbitrary measurable
simplex-valued relaxed controls with equal total allocation `T/n` have exact
worst-case two-switch error

```
E = T max{1/n, 1/[n((n/(n−1))³−1)]}.
```

The constant uniform control attains this worst case. No assumption of uniform
allocation in time is used in the upper-bound argument. This is a proof audit,
not a literature novelty determination.

## Regularity and reach-time endpoints

For a measurable simplex-valued control, each cumulative allocation
`A_i(t)=∫_0^t α_i` is absolutely continuous, nondecreasing, and 1-Lipschitz.
The function `f_i(t)=t−A_i(t)` is therefore continuous and nondecreasing.
Its sublevel set at a nonnegative error threshold is a closed initial interval,
so the reach time on `[0,L]` exists.

If `R_i<L`, then `f_i(R_i)=E`. A value strictly smaller than `E` would, by
continuity, allow a larger feasible time, contradicting maximality. Thus
`A_i(R_i)=R_i−E`, and `R_i≥E`. This remains true when `f_i` has flat portions;
maximality chooses the last endpoint of a flat portion at the threshold.
If `R_i=L`, the separate large-reach branch applies and no equality is required.

## The two largest reach values

Assume every reach is smaller than `L`. Let `p` attain the largest reach `x`,
and let `y` be the largest reach of any mode different from `p`. For every
`i≠p`, monotonicity gives `f_i(y)≥E`, while
`A_p(y)≤A_p(x)=x−E`. Hence

```
y=Σ_i A_i(y) ≤ (n−1)(y−E)+(x−E),
```

which proves `x+(n−2)y≥nE`. Ties for the largest reach cause no issue: after
choosing one maximizing index as `p`, another index can supply `y=x`.

The identity in the draft is exact:

```
(n−1)x+y
 = [n/(n−1)] [x+(n−2)y]
   + [(n²−3n+1)/(n−1)] (x−y).
```

The last coefficient is positive for `n≥3`. Since `x≥y`, this proves
`(n−1)x+y≥n²E/(n−1)`.

## The ordered-pair guarantee really uses distinct modes

Let `C=max_{p≠q}(R_p+A_q(L))`. Choose `p` attaining `x`. For every `q≠p`,
`A_q(L)≤C−x`. To bound `A_p(L)`, choose an index different from `p` attaining
`y`, which gives `A_p(L)≤C−y`. Summing yields

```
L≤nC−[(n−1)x+y].
```

Therefore

```
C≥nE/(n−1)+L/n.
```

This direct non-strict proof is equivalent to the draft's strict-contradiction
argument. It confirms that the result does not accidentally use an inadmissible
pair with the same first and second mode.

The reach lemma needs only simplex-valued dynamics, not equal terminal totals.
Equality of the terminal totals enters the schedule argument separately.

## Constants and the terminal time

Write `r=n/(n−1)` and choose
`L=T−T/n−E`. For `n≥4`, both terms in the maximum defining `E/T` are below
`1/3` (the first is at most `1/4`); hence `0<L<T`.
The asserted algebraic equivalence is correct:

```
rE+L/n≥L−E
 ⇔ E≥T/[n(r³−1)].
```

For example, multiplying the first inequality by `r` gives
`(r²+r+1)E≥T/r`, and `n(r−1)=r` makes the denominator exactly
`n(r³−1)`. The chosen `E` satisfies this inequality and `E≥T/n`.

## Complete trajectory control

Since every relaxed mode has total `T/n`,

```
A_i(t)−∫_0^t ω_i ≤ A_i(t)≤T/n≤E
```

for every time and every schedule. Thus every positive discrepancy is already
controlled. No temporal ordering property of the relaxed allocation is needed.

If some `R_p=L`, activate `p` on `[0,L)` and a different mode on `[L,T]`.
The first block's negative discrepancy is at most `E` by reachability. The final
mode has never been used earlier, so its terminal negative discrepancy is

```
T−L−A_q(T)=T−L−T/n=E.
```

This branch correctly uses at most one switch; it does not apply the root
identity to a reach truncated at `L`.

Otherwise the pair guarantee and the constant inequality produce distinct
`p,q` with `R_p+A_q(L)≥L−E`. Define

```
t_1=max(0,L−A_q(L)−E),    t_2=L.
```

The pair inequality and `R_p≥0` imply `t_1≤R_p`. Nonnegativity of `A_q(L)`
and positivity of `E` imply `0≤t_1<L`. Select a third mode distinct from `p,q`,
which exists because `n≥4`, and activate the three modes consecutively.

The first endpoint is feasible since `t_1≤R_p`. The second endpoint satisfies
`L−t_1−A_q(L)≤E` by the definition of `t_1`, including the case where the maximum
chooses zero. The final mode has not appeared before, so its endpoint discrepancy
is again exactly `E`. If `t_1=0`, the first block disappears and the schedule
still uses at most two switches.

For each selected mode, its discrepancy is nondecreasing before activation,
nonincreasing during its sole active block, and nondecreasing after deactivation.
The negative minimum is therefore at that block's endpoint. Each unused mode
has nonnegative discrepancy throughout. These observations, together with the
positive bound above, control the entire continuous trajectory rather than just
the displayed three times.

## Sharpness and scope

The uniform relaxed control belongs to the equal-total class. The independently
reviewed uniform-control formula with `s=2` applies because `2≤n−2`, exactly the
reason for the theorem's restriction `n≥4`. Its optimal error equals the upper
bound above. The lower bound permits repeated modes in competitors; the distinct
modes in the upper construction do not restrict the optimization problem.

The proof does not assert that equal terminal totals can be imposed without
loss in the unrestricted two-switch problem. It also gives no discrete
half-grid rounding claim. Its conclusion is the exact continuous worst case
within the stated equal-total class, for arbitrary measurable temporal profiles.
