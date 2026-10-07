# Fixing a core boundary face through all optimal integer flows

Date: 2026-10-02. Status: passed a
[fresh independent review](../reviews/flow-optimal-face-adversary.md),
with distinct exact diagnostics. This note supplies a certificate; it does
not assume a probabilistic stopping result.

The [uniform-flow certificate](smoothed-interior-core-flow.md) can fail at a
core boundary because different integer flows win in different inward
directions. The certificate below instead minimizes each inward derivative
over **all** flows optimal on that face. Those flows are represented by
tightened arc intervals. A quantitative cost bound controls every remaining
flow. No list of the tied flows is needed.

## 1. Model and the optimal-flow intervals

Use a fixed directed network with `r` arcs, integral supplies and finite
integral arc intervals. Let its nonempty feasible integer-flow set be `Y`.
The continuous core is `v in [0,1]^k`, and

```
F(v,z)=phi(v)+sum_a f_a(v,z_a)+gamma'v.
```

The functions are rational polynomials of fixed degree at most `d>=1`. Each
arc cost is convex in its scalar flow throughout its native real interval,
for every core point. The core changes only costs.

Fix a core face `A`: some coordinates are fixed to zero or one; the rest
are free. An inward normal coordinate has direction `s_i=+1` at zero and
`s_i=-1` at one. Let `D` be a rational core box touching those chosen bounds,
and let `D_A` be its projection onto that face. Choose rational `c in D_A`.
An exact conditional flow solve gives an optimal flow `z^0` and rational
potentials `pi(c)` with nonnegative residual marginal reduced costs.
For each original arc `a=(u,v)`, put

```
g_a(c,t)=f_a(c,t)+(pi_u(c)-pi_v(c))t.
```

The integer minimizers of this convex function form an interval
`I_a=[ell'_a,u'_a] intersect Z` containing `z^0_a`. Its endpoints can be
found by binary search on monotone first differences, using polynomially
many rational evaluations in the binary input length. Let

```
Y_0={z in Y:z_a in I_a for all a}.
```

Then `Y_0` is exactly the set of conditional optimal integer flows at `c`.
Indeed every `g_a` is minimized at `z^0_a`; the potential terms sum to a
fixed number over all feasible flows. Equality in the resulting sum of
nonnegative arc gaps holds precisely when every arc is in its minimizing
interval. In particular, `Y_0` is nonempty and is another network-flow
problem with tightened integral arc bounds.

## 2. Why inward derivative minimization is convex flow

For a chosen inward coordinate `i`, the arc derivative

```
q_{ia}(t)=s_i partial_i f_a(c,t)
```

has an exact convex-cost representation on `I_a` agreeing at every integer
point:

- If `I_a` has one point, substitute that point.
- If it has two consecutive points, linearly interpolate their two values.
- If its length is at least two, `q_{ia}` itself is convex on its whole
  real interval.

For the third claim, a convex function with equal values at three ordered
points, all of them minimizers over the integer interval, is affine between
the first and last points. Thus `f_a(c,t)` is affine throughout the interval.
Its second derivative in `t` is zero there. For every sufficiently small
inward displacement `h>=0`, convexity of `f_a(c+h s_i e_i,t)` gives

```
partial_tt f_a(c+h s_i e_i,t)>=0.
```

The right derivative at `h=0` is therefore nonnegative:
`partial_tt q_{ia}(t)>=0`. Polynomial smoothness justifies this derivative.
The two-point interpolation is necessary: equality of two integer costs
does not imply affinity between them.

Consequently the exact convex-flow oracle computes the rational number

```
beta_i=min_(z in Y_0) s_i partial_i F(c,z)                 (1)
```

in polynomial bit time. The derivative of `phi` and the linear core noise
are constants in this flow problem. Tangent-line extensions outside the
tightened real interval supply globally convex query costs when required by
the chosen oracle. The bound is over all optimal flows, not the arbitrary
flow returned by the first oracle call.

## 3. A distance bound for tightened flow intervals

For any feasible integer flow `z`, write

```
v_I(z)=sum_a dist(z_a,I_a).
```

There exists `bar z in Y_0` with

```
||z-bar z||_1<=r v_I(z).                                 (2)
```

Choose a member of the finite nonempty set `Y_0` minimizing its distance
to `z`. The circulation `z-bar z` has a conformal decomposition into simple
directed cycles in the signed residual graph, with nonnegative integer
multiplicities. Each cycle uses at most `r` original arcs. Every such cycle
must contain an arc at a bound of `I_a` whose directed unit change toward
`z_a` leaves `I_a`. Otherwise that unit cycle is feasible in `Y_0` and
strictly reduces the chosen distance. On a blocking arc, `z_a` is outside
`I_a`, and its full difference from `bar z_a` is exactly its interval
violation. Charge each cycle's multiplicity to one blocking arc. Conformality
bounds the total charge to that arc by its violation. Summing cycle lengths
proves (2). The argument is valid with parallel arcs, cycles, redundant
balance rows and singular flow polytopes. Self-loops may be treated as
one-arc cycles.

## 4. Uniform face costs and a sound fixing test

Choose polynomial potentials `pi(w)` on the face of core degree at most
`d-1`, agreeing with the potentials at `c`. The shortest-path tree
construction in the interior note has this property: a unit difference in
the flow coordinate reduces total degree by one. Thus `g_a(w,t)` has total
degree at most `d`. Define it as above with these potentials. Verify:

1. `g_a(w,t)=g_a(w,z^0_a)` for every `w in D_A` and every integer `t in I_a`.
2. Every available first outside marginal is at least a rational threshold
   `mu>=0` throughout `D_A`:

```
g_a(w,ell'_a-1)-g_a(w,ell'_a)>=mu,
g_a(w,u'_a+1)-g_a(w,u'_a)>=mu.                            (3)
```

Only the inequality with a point in the original native interval is used.
Convexity then gives, for every feasible integer flow,

```
F(w,z)-V(w)>=mu v_I(z),
V(w)=min_(y in Y) F(w,y),   w in D_A.                     (4)
```

Every flow in `Y_0` is optimal throughout `D_A`. The equality tests in step
1 require only `d+1` distinct integer representatives per arc, or all its
points if there are fewer: the difference is a degree-at-most-`d` polynomial
in `t`. After substituting fixed core coordinates, verify polynomial
identities in the remaining coordinates. Singleton intervals of `D_A` are
substituted as well. The outside tests are fixed-degree polynomial minima
on a rational box, with constant-base `c_d^k poly(input bits)` cost through
the [deterministic box solver](polynomial-component-primitive-limit.md).

Supply computable rational bounds on the original real bounding domain:

```
H>=1,  ||Hess_v F(v,z)||_2<=H,
K>=0,  |partial_i partial_(z_a) f_a(v,z_a)|<=K
        for every core coordinate i and arc a.
```

Monomial bounds suffice. Let `R` bound `||w-c||_2` over `D_A`. For example,
`k` times its largest coordinate width is a rational bound. Let `T_1` be
the sum of the inward normal widths of `D`, and `T_infty` their maximum.
If there is at least one active normal, put `beta=min_i beta_i`. The test is

```
mu>=r K T_1,
beta-H R-(H/2)T_infty>0.                                 (5)
```

There is no need to compute a tiny best `mu`: directly use `mu=rKT_1` in
the exact polynomial tests (3). If no outside marginal exists, every
feasible flow belongs to `Y_0` and those tests are vacuous.

To prove the test, take `v in D`, let `w` be its face projection, and write
`v=w+sum_i s_i d_i e_i` with `d_i>=0`. Choose `bar z` from (2). Core and
flow derivative bounds imply

```
s_i partial_i F(w,z)>=beta-H R-K||z-bar z||_1.
```

Taylor's theorem, (2) and (4) now give

```
F(v,z)>=V(w)
 +(mu-rK||d||_1)v_I(z)
 +(beta-HR)||d||_1-(H/2)||d||_2^2
 >=V(w)+[beta-HR-(H/2)T_infty]||d||_1.                   (6)
```

The final coefficient is strictly positive. Every point of `D` off the
chosen face is therefore worse than a feasible point on that face.

If `D` contains all original optimal core points, the test fixes this face
for every original optimizer. Since every flow of `Y_0` is optimal on
`D_A`, the slice with `z=z^0` contains an original optimizer. Exact
optimization of `F(.,z^0)` over the **entire original core box** finishes
the original problem. There is no need to preserve the selected face during
that final solve. With no active normals, use the same interval identities
and outside tests with `mu=0` directly. They certify uniform flow optimality
without testing the artificial source arcs used to construct the potentials.

## 5. The boundary example is closed

In the [two-arc example](core-only-flow-boundary-obstruction.md), choose the
origin face. Both arc intervals remain `[0,1]`, so `Y_0=Y` and there are
no outside tests. At the origin, minimizing each inward derivative over
the two flows gives `beta_i=gamma_i`. Here `H=1`, `R=0`. For an origin box
whose maximum width is less than `2 min_i gamma_i`, (5) holds. In particular
it closes throughout the positive-probability event used in that obstruction,
without choosing one flow optimal on the full adjacent box.

## Verification and scope

This is a deterministic, exact certificate. Each successful test is sound
regardless of noise, core growth or an assumed face. Searching all `3^k`
faces adds only a factor depending on the core dimension. A probabilistic
argument must still prove adequate face margins and separation from chart
zeros; geometric separation alone does not give a coefficient-independent
positive marginal value. The [completed-file review](../reviews/flow-optimal-face-adversary.md)
approved the argument and ran a distinct exact diagnostic: 703 tightened
interval boxes, 3,942 proximity checks, and 54 derivative/Taylor checks.
Those tests include a cycle attaining factor `r` and rejection guards for
using one tied flow's derivative or dropping the outside-cost threshold.
The [focused prior comparison](../prior-art/smoothed-boundary-core-flow-prior.md)
credits the classical flow-duality and circulation ingredients; it does
not establish publication novelty for this composition.

The author-side diagnostic was run with

```sh
python3 -B research-20261002/new-direction/check_flow_optimal_face.py
```

The [exact-fraction checker](check_flow_optimal_face.py) passed five network
fixtures, including parallel arcs, a directed cycle, signed native bounds
and a self-loop. It checked 22 exhaustive optimal-flow classifications and
22 nearest-tight-flow bounds, 12 tied-flow derivative comparisons, and 84
exact Taylor polynomial minima. Two fixtures attain the factor `r` in (2).
The derivative tests include eight long flat intervals, four two-point
intervals (two with genuinely concave derivatives requiring interpolation),
and three singleton intervals. Nine boundary-example boxes passed 18 exact
minima. A losing-flow guard satisfies the normal-derivative test but fails
the outside-cost threshold and attains a strictly better off-face value;
it confirms that the latter test cannot simply be dropped.

This checker enumerates small feasible-flow sets and verifies supplied
potentials. It does not implement a production convex-flow oracle, binary
search on large capacities, or general polynomial box optimization. Its
core minimizations are quadratic or affine in the tangential coordinate.
No project-wide checks or CI inspection were performed.
