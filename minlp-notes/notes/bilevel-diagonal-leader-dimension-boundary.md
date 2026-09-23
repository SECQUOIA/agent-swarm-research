# Leader dimension: an established hardness boundary for diagonal followers

Date: 2026-09-05. Status: supporting investigation, **not a new hardness
claim**. The proposed parameterized direction is already covered by an
open primary source. The alternative proof below is retained for its simple
mixed-radix construction. It passed an
[independent mathematical audit](review-bilevel-diagonal-leader-dimension-boundary.md)
and a separate source-agent sanity check.

## Source outcome

Froese, Grillo, Hertrich and Stargalla,
[*Parameterized Hardness of Zonotope Containment and Neural Network Verification*](https://arxiv.org/pdf/2509.22849v3),
September 3, 2026 version, Proposition 4.1, gives a clique reduction with a
constant value gap for two-layer ReLU networks and input dimension equal
to the clique parameter. Corollary 5.5 explicitly uses a bounded box.
Its W[1] and ETH lower bounds transfer to identity-Hessian unit-box
followers by replacing each bounded ReLU with a scaled capped ramp.
Polynomial duplication also bounds upper coefficients. Consequently the
restrictions investigated here do not supply a new complexity result.
The [separate source audit](bilevel-diagonal-box-parameterized-hardness-source-audit.md)
records the precise comparisons and the corresponding results in the
September 2025 first version; the overlap predates the latest revision.

## Direct alternative construction

Let `G` be a graph with `n>=2` labelled vertices `0,...,n-1`. Given a clique
size `k>=2`, use exactly `k` leaders `x_i in [0,1]`, and write
`t_i=(n-1)x_i`. Put `clip(s)=min(1,max(0,s))`.

Define `d(t)` to be distance from `t` to the nearest integer in
`{0,...,n-1}`. The half-grid interpolation identity is

```
2d(t)=sum_(a=0)^(2n-3) (-1)^a clip(2t-a).          (1)
```

Both sides vanish at zero and are linear between consecutive half-integers;
their values alternate between zero and one on that grid, proving the
identity on the entire interval.

Define the table on integers `s=0,...,n^2-1` by

```
f(s)=0 if the two labels in s=u+n*v are distinct adjacent vertices,
f(s)=1 otherwise.
```

Let `phi` be its piecewise-linear interpolation. Since `f(0)=1`,

```
phi(s)=1+sum_(a=0)^(n^2-2) [f(a+1)-f(a)] clip(s-a). (2)
```

This follows by checking values and slopes on each unit interval. In
particular `0<=phi<=1`, its Lipschitz constant is at most one, and every
coefficient in the sum belongs to `{-1,0,1}`.

Consider the leader objective

```
H(x)=2n sum_i d(t_i)+2 sum_(i<j) phi(t_i+n*t_j).    (3)
```

It is nonnegative everywhere. A clique gives an integer-label witness with
value zero. Conversely, round each `t_i` to a nearest label `b_i`, breaking
ties arbitrarily, and put `D=sum_i |t_i-b_i|`. If the graph has no `k`-clique,
some pair has a repeated or nonadjacent rounded label. Its table value is
one, and Lipschitz continuity yields

```
phi(t_i+n*t_j) >= max{0,1-|t_i-b_i|-n|t_j-b_j|}
                >= max{0,1-nD}.
```

Therefore every leader satisfies

```
H(x)>=2nD+2max{0,1-nD}>=2.                         (4)
```

This is a uniform continuous-domain gap; no claim about an exponential
number of response cells is being substituted for the reduction.

## Identity-Hessian box realization

For each capped ramp `clip(h(x))`, introduce a follower coordinate that
minimizes `z^2/2-h(x)z` on `[0,1]`. Combining these independent coordinates
gives a unique follower response with `Q=I`. Every affine form uses at most
two leader coordinates.

Use (1) and (2) in (3). Duplicate each half-grid ramp `n` times, each with
upper coefficient `(-1)^a`, to realize `2n*d(t_i)`. Each pair ramp has upper
coefficient `2[f(a+1)-f(a)]`; omit zero coefficients. For the constant
`2*binom(k,2)`, either retain an affine upper constant or introduce one
fixed-one follower per pair with upper coefficient two. A fixed-one follower
minimizes `z^2/2-z` on the unit interval.

Thus the upper objective can be purely linear, with coefficients in
`{-2,-1,1,2}`. There are no upper constraints except the leader unit box.
There are `O(k^2*n^2)` follower coordinates, all data are integers of
polynomial magnitude, and every follower linear coefficient has at most
two nonzero leader coefficients. There is no small-gap or ill-conditioning
mechanism: the exact gap is zero versus at least two, and all eigenvalues
of the follower Hessian are one.

One can also bound every follower affine coefficient in magnitude by one.
Take the integer `R=2n^2`. Every used form `h`, and the form `h-1`, has
coefficient magnitudes and positive range at most `R`. The identity

```
clip(h)=ReLU(h)-ReLU(h-1)
       =R[clip(h/R)-clip((h-1)/R)]
```

therefore holds on the leader box. Replace each original ramp by these two
scaled followers and duplicate each `R` times. This preserves the upper
coefficient set and the gap while giving `O(k^2*n^4)` followers. The
normalization must use the difference of two ReLUs: simply scaling a capped
ramp's argument would not preserve saturation. Rational denominators have
polynomial encoding. This additional restriction is also covered by the
source transfer and is not a separate novelty claim.

The formulas also give an immediate exact witness when a clique exists.
For any rational leader, its follower response is rational and easy to
compute. More generally, guessing the finitely many clipping regimes gives
an affine rational system, so the ordinary threshold problem belongs to NP.
The reduction is parameter preserving with leader dimension `r=k`.
Combined with the established clique lower bounds, it rules out an
`f(r)*poly(input size)` exact algorithm under `FPT!=W[1]`, and an
`f(r)*input_size^(o(r))` algorithm under ETH. A value estimate with additive error less than one, or a returned feasible
leader with suboptimality less than two, would distinguish (4) as well. These conclusions agree with the
cited neural-network theorem and are not asserted as new.

## Interpretation and remaining direction

The fixed-dimensional clipped-affine arrangement algorithm is polynomial
for every fixed leader dimension. Parameterized hardness says its exponent
cannot generally be replaced by a dimension-independent polynomial with
an arbitrary prefactor depending only on the dimension. Conditioning,
unit boxes, and two-coordinate follower dependence do not remove this
barrier. In contrast, a follower affine form depending on only one leader
coordinate makes the response objective separable across leaders when the
leader domain is a product box and there are no upper coupling constraints;
then independent one-dimensional piecewise-linear minimizations suffice.
This last observation is an elementary tractable special case, not a new
parameterized theorem.

## Exact diagnostics

[The exact checker](../code/bilevel_parameterized/check_mixed_radix_gap.py)
checks all eight graphs on three vertices at 125 rational leader points
each, all integral three-label assignments, triangle identities for several
label counts and rational grids, and the scaled-ramp identity. It uses
exact fractions; these diagnostics supplement the general argument.
