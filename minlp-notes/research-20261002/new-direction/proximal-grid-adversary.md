# Adversarial review of the proximal shared-grid argument

Date: 2026-10-02. Scope: an independent mathematical review, with a second
independent reviewer and targeted exact-rational checks. No external
literature search was performed. This review does not establish originality.

## Verdict and essential promise

No fatal gap was found. The argument works with an arbitrary nonempty compact
optimal set, including a continuum or several disconnected components. It
does not require a unique optimizer or a consistent choice of nearest
optimizer across stages.

The supplied valid conditioning bound is essential to the stated algorithm.
The local lower bound depends on that promise and the resulting distance
invariant. It is not an assumption-free global certificate, and an unknown
conditioning guess cannot be accepted merely because the displayed local
gap is small.

The review concerns approximate optimization. It does not establish recovery
of an exact optimizer when the optimal set is nonunique.

## 1. Setting and the moving box

Let `X` be a nonempty compact product of continuous and integer intervals,
and let `F` be a rational quadratic with known upper coordinate curvature
`L>0`. Write `S=argmin_X F` and `f*=min_X F`. Assume that a supplied rational
number `kappa` satisfies

```
kappa >= max(1,L/g),
F(x)-f* >= g dist(x,S)^2       for every x in X.
```

Use the original coordinates throughout. Fixed variables may be removed;
the singleton problem and the separately concave `L<=0` case have the
existing direct treatments. Let `n>=1`, let `s` be the maximum original side
length, and put

```
h_j=s 2^-j,
M=ceil(sqrt(n kappa)).
```

Choose the largest dyadic `theta<=1/4` satisfying
`theta^2 kappa<=1/8`. This choice ensures `theta^-1=O(sqrt(kappa))`; choosing
an arbitrarily smaller value would instead give a bound in that value.
The required comparisons and the computation of `M` use rational arithmetic
and integer comparisons, with no irrational oracle.

Given a feasible center `c` with

```
dist(c,S)^2 <= 4 kappa n h_j^2,
```

form the box

```
B_j = X intersect product_i [c_i-2M h_j, c_i+2M h_j].
```

For integer coordinates, round the new lower endpoint upward and the upper
endpoint downward. The center remains feasible, so this does not make the
box empty. A nearest `a in S` exists by compactness, and

```
|a_i-c_i| <= dist(c,S) <= 2sqrt(kappa n)h_j <= 2M h_j.
```

Thus `a` lies in `B_j`, including after inward rounding on integer
coordinates.

Each box must be formed from the **original** domain `X`. Intersecting with
the previous restricted box would require an additional argument: the
nearest point of the full optimal set can change and need not belong to
that previous box. The proposed reopening rule avoids that gap.

An arbitrary original feasible initial center satisfies the incoming
invariant at stage zero, since its distance to `S` is at most `sqrt(n)s`.

## 2. The proximal cancellation and rounding estimate

Build the usual geometric coordinate grids around `c`, clipped to `B_j`.
Let `ell_i(v)` be the maximum adjacent interval length, ignoring integer
unit intervals, and define

```
D(y) = (L/8) sum_i ell_i(y_i)^2,
lambda = L theta^2/4,
P(y) = F(y)-D(y)+lambda ||y-c||^2.
```

The existing mesh bound gives

```
D(y) <= (L/8) sum_i (h+theta |y_i-c_i|)^2
     <= L n h^2/4 + lambda ||y-c||^2.                 (1)
```

Hence every grid point satisfies `F(y)<=P(y)+Lnh^2/4`. This is the exact
cancellation needed by the argument; no curvature of the conditional value
function or convexity of `F` is being assumed.

Independently round a nearest optimizer `a` to its adjacent grid endpoints,
with mean `a`, obtaining `Y`. The correction lemma gives
`E[F(Y)-D(Y)]<=F(a)=f*`.

For each genuinely rounded coordinate, the containing interval has length
at most `h+theta |a_i-c_i|`. The nearer endpoint lies between `c_i` and
`a_i`; clipping can only shorten the step. A feasible integer cannot be
strictly inside a unit interval, so an ignored unit interval contributes
zero rounding variance. Consequently, with `d=dist(c,S)`,

```
V := E||Y-a||^2
   <= (1/4) sum_i (h+theta |a_i-c_i|)^2
   <= (n h^2+theta^2 d^2)/2.
```

The mean-zero rounding error also gives
`E||Y-c||^2=d^2+V`. If `y` minimizes `P` on the product grid, then

```
P(y) <= E P(Y)
     <= f*+lambda[(1+theta^2/2)d^2+n h^2/2].          (2)
```

This argument uses one nearest optimizer only for the current stage. The
algorithm never needs to find or identify it.

## 3. Constants and induction

Combining (1) and (2) gives the direct estimate

```
F(y)-f* <= L n h^2(1/4+theta^2/8)
          +(L theta^2/4)(1+theta^2/2)d^2.
```

Using `d^2<=4kappa n h^2`, `theta^2<=1/16`, and
`kappa theta^2<=1/8` yields

```
F(y)-f* <= (99/256)L n h^2 < (27/64)L n h^2.         (3)
```

Thus the proposed `27/64` constant is conservative. Quadratic growth gives

```
dist(y,S)^2 <= (27/64)(L/g)n h^2 <= kappa n h^2.
```

Since the next scale is `h/2`, this is the incoming invariant for the next
stage. Boundary optima, changes of nearest optimizer, and integer coordinates
cause no exception to this induction.

## 4. The lower bound is conditional

Let `p_j=min P` and use the known upper distance estimate
`E_j=4kappa n h_j^2`. Define

```
A_j=lambda[(1+theta^2/2)E_j+n h_j^2/2],
LB_j=p_j-A_j,
UB_j=F(y_j).
```

Equation (2), together with the promise-derived incoming invariant, proves
`LB_j<=f*<=UB_j`. Equation (1) gives

```
UB_j-LB_j <= L n h_j^2/4+A_j
          <= (99/256)L n h_j^2
          <  (27/64)L n h_j^2.
```

The dynamic-programming tables alone establish the minimum of `P` on its
restricted grid. They do not establish that `B_j` contains a global
optimizer. That latter fact uses the supplied conditioning promise and the
inductive argument. If the supplied `kappa` is invalid, the box can exclude
the entire optimal set and the reported lower bound can exceed `f*`.
Reopening the original domain does not by itself repair an invalid radius.

This is a correct promise-dependent approximation algorithm. An
assumption-free certificate or an unknown-growth acceptance rule would be a
separate result.

## 5. State count and bit complexity

The current side length is at most `4Mh`. Thus

```
theta side_length/h <= 4theta M
                       <= 4theta sqrt(n kappa)+4theta
                       <= sqrt(2n)+1.
```

The geometric-grid count is therefore
`O(theta^-1 log(n+2))` per coordinate, independently of the stage index.
For integer coordinates use `H=max(h,1)` in the standard count; the bound
only improves because `h/H<=1`. A temporarily fixed coordinate contributes
one state. Writing `log(n+2)` avoids the degenerate `log(1)=0` expression.

Both the correction and the proximal term are unary. They preserve the
original interaction graph and supplied tree decomposition. Exact min-sum
DP therefore computes a stage in
`O((N+number_of_factors) q^p)` table work, apart from factors depending on
bag size `p`, where `q=O(theta^-1 log(n+2))`. The inequality
`log(n+2)^p<=f(p)n` absorbs the logarithmic power into a parameter-dependent
factor and one fixed power of input size.

For rational QPs, let `D` clear the original rational input denominators,
including a chosen rational initial center, and write `theta=2^-k`. The
geometric offset after `t` outward steps is

```
h_j ((1+theta)^t-1)/theta,
```

whose denominator divides `D 2^(j+k max(t-1,0))`. New box endpoints have
the form `c_i +/- 2M h_j`, clipped to original endpoints, so they preserve
the same type of dyadic lattice. Integer rounding preserves integrality.
Selecting a new center from the grid and adding an offset takes the maximum
dyadic denominator exponent; it does not multiply unrelated denominators.

Through stage `J`, all continuous grid coordinates consequently have a
common denominator dividing `D 2^T`, with `T<=J+kq` up to an inessential
constant. QP values, corrections, and proximal terms have a common
denominator with bit length polynomial in `I+J+kq`. Exact message passing
only adds and selects these values. Input bounds control their magnitudes,
so all intermediate bit lengths remain polynomial in that quantity.

To reach error `eps=2^-b`, (3) requires
`J=poly(I)+O(b)` stages. Choosing the specified dyadic parameter gives
`q=O(sqrt(kappa)log(n+2))`. The resulting bit bound has the form
`f(p,kappa) poly(I+b)`, with a polynomial exponent independent of `p`.
The supplied conditioning bound is included in the rational input, and its
numerical value is a parameter in this claim.

## 6. Targeted verification

Two independent reviews checked nearest-point containment, reopening,
rounding, integer unit intervals, proximal cancellation, the constants,
induction, graph preservation, grid counts, and rational arithmetic.

An inline exact-`Fraction` Python check was run with `python3 -` on four
families: a continuum of diagonal optima, a union of two optimal faces, two
isolated optima, and nine mixed integer/continuous optima. It passed 36
stages, 1,217 exhaustive product-grid assignments, and 45 rounded atoms.
Assertions checked the incoming distance invariant, containment of a nearest
optimizer, the expected proximal bound, the conditional lower bound, the
`27/64` gap, and the outgoing distance invariant.

The second reviewer independently ran an inline exact-`Fraction` check with
64 stages and 1,728 product-grid assignments, including a continuum of
optima, disconnected optima, mixed optima, and purely integer optima. Its
assertions also checked the stronger `99/256` constant. All passed.

These finite examples support the reviewed proof; they do not establish
originality, competitive performance, or an assumption-free certificate.
No project-wide checks or CI inspection were performed.
