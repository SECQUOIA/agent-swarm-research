# Bit-complexity audit of min-marginal pruning for shared grids

Date: 2026-10-02. Status: the proposed pruning route is mathematically
viable for rational mixed-integer box QP, provided unsuccessful growth
trials are capped and integer unit intervals are handled as below.
This is an independent audit of the proposed argument, not an external
priority assessment or an implementation claim.

The starting algorithm is the corrected point-grid DP in
[theorem.md](../geometric-dp/theorem.md). Its rational QP height and
reconstruction arguments are in
[exact-box-qp.md](../geometric-dp/exact-box-qp.md).
The resulting [main draft](pruned-coordinate-grid.md) uses slightly
tighter localization constants and a smaller safe cap than the
conservative versions derived independently here.

## 1. Conditional bounds and safe hull pruning

At the current product box, let `G_i` be the shared coordinate grids,
let `d_i(v)` be their existing curvature corrections, and write

```
C(y)=F(y)-sum_i d_i(y_i),
m_i(v)=min {C(y): y in product G, y_i=v}.
```

For consecutive coordinate-grid values `u<v`, define

```
LB_i([u,v])=min(m_i(u),m_i(v)).                                     (1)
```

This bounds the original objective below on the entire conditional
slice `x_i in [u,v]`, with all other coordinates in the current box.
Indeed, the original independent rounding argument rounds coordinate
`i` only to `u,v`, or fixes it when it is already an endpoint. It gives
`E C(Y)<=F(x)`, while every possible rounded value has corrected
objective at least the right side of (1). The same argument applies
to integer coordinates. Unit intervals have no feasible interior
integer points, which is exactly why their correction may be zero.

Discard an interval only if its lower bound is **strictly greater**
than a feasible incumbent value `UB`. Retain the coordinate hull of
all remaining intervals. Every point of the current box with
`F(x)<=UB` survives in the product of those hulls. In particular, the
global minimizer remains and the restricted optimum equals the original
optimum. The hull can reintroduce discarded interior intervals; this
weakens pruning but does not invalidate it.

Use the current corrected-grid minimizer `z_j` to update
`UB=min(previous UB,F(z_j))` before pruning. An arbitrary feasible
center's objective gap is not bounded by its distance to the optimum
under only upper curvature. The current minimizer's feasible objective
has the gap guarantee needed in Section 2.

The new center `z_j` lies in every retained hull, since
`m_i((z_j)_i)=LB<=f*<=UB`. The best feasible incumbent also survives.
Original singleton domains must be preserved or substituted out
explicitly. Taking hulls of whole nonzero intervals does not produce
new singleton domains. Empty retained families cannot occur in exact
arithmetic when the current box contains a minimizer.

## 2. Retained endpoints localize, with an integer correction

Let `g` be the actual mixed-domain quadratic-growth constant, let
`kappa=max(1,L/g)`, and use the original theorem's stage scales
`h_j=s0 2^-j`. Assume

```
theta^2 <= min(1/4,g/(8L)),
B=max(1,4L/(11g)).
```

The existing contraction proof continues to hold on the restricted
boxes, because they contain `x*`, the center is feasible, and the same
mesh inequality holds. In particular,

```
||z_j-x*||^2 <= B n h_j^2,
UB-f* <= 7L n h_j^2/8,
||z_(j-1)-x*||^2 <= 4B n h_j^2.                                   (2)
```

The last inequality also holds at the initial stage by the original
box-diameter estimate.

Suppose a grid value `v` has `m_i(v)<=UB`, and take a minimizing grid
witness `y` with `y_i=v`. The witness need not minimize the unrestricted
corrected objective. Nevertheless,

```
g ||y-x*||^2 <= F(y)-f* <= UB-f*+D(y).
```

The original mesh estimate bounds

```
D(y) <= L n h_j^2/4
        +(L theta^2/2)(||y-x*||^2+||z_(j-1)-x*||^2).
```

Using (2), `theta^2 B<=1/4`, and `L theta^2/2<=g/16` gives

```
||y-x*||^2 <= (26/15)(L/g)n h_j^2
            < (16/9)kappa n h_j^2.                                (3)
```

Every retained interval has at least one endpoint satisfying (3).
For a continuous interval, its length is at most
`h_j+theta |v-z_(j-1),i|`, evaluated at that endpoint. Since `B<=kappa`
and `theta<=1/2`, both endpoints of every retained continuous interval
are within

```
4 sqrt(n kappa) h_j
```

of the optimum coordinate. For integer intervals of length at least
two the same argument applies. Integer intervals of length one may
survive because one endpoint has a low marginal, even though their
other endpoint remains one unit from the optimum as `h_j` tends to
zero. The correct uniform bounds are therefore

```
continuous retained diameter <= 8 sqrt(n kappa) h_j,
integer retained diameter    <= 2+8 sqrt(n kappa) h_j.              (4)
```

Different retained endpoints may use different witnesses in (3).
No common witness is needed for these coordinatewise bounds.

## 3. Grid counts and the FPT dependence

At the next stage, the continuous scale is `h_(j+1)=h_j/2`.
Divide each continuous retained diameter by that scale. For an integer
coordinate, divide its diameter by `H=max(h_(j+1),1)`, as required by
the integer grid-count lemma. Equation (4) bounds these ratios by
`16 sqrt(n kappa)` and `2+16 sqrt(n kappa)`, respectively.

Consequently every coordinate has

```
q_grid <= C theta^-1 [1+log(2+n kappa)]                            (5)
```

states for an absolute constant `C`, independent of the stage index.
Use the coordinate-specific retained diameter here. A single global
mixed-domain diameter could stay at least one because of integer unit
intervals and would give the wrong continuous-coordinate count.
The initial stage has at most three nodes per coordinate because
`h_0=s0` spans every original side.

Exact marginal computation has the same table-order bound as one
optimization pass. Compute directed messages both ways on the supplied
tree. A bag belief sums its assigned objective and penalty terms and
all incoming messages. Minimizing it with one coordinate fixed gives
that coordinate's global min-marginal. Compute each coordinate's
marginal at one containing bag. This takes

```
O(p (N+number of factors) q_grid^p)
```

table operations per stage. For outgoing messages, scan the bag table
once per incident tree edge; the sum of bag degrees is `2(N-1)`.
There is no maximum-degree factor. All table values are finite for
these product-box grids, so forming an outgoing belief by subtracting
one incoming message does not involve infinite arithmetic.

The logarithmic power in (5) can be absorbed into a fixed-parameter
factor and one additional polynomial factor in `n`. For example,
maximizing `(1+t)^p exp(-t)` for `t>=0` proves
`(1+log n)^p <= e p^p n`. Thus (5), with admissible
`theta^-1=O(sqrt(kappa))`, gives per-stage work

```
f(p,kappa) poly(I)
```

with an absolute polynomial exponent. Unlike the unpruned proof, it
does not raise the accuracy-bit count to the bag dimension.

## 4. Unknown growth requires a cap on failed trials

The old restart schedule cannot inherit this improved complexity
without a change. A trial with an inadmissibly large `theta` can fail
to prune; its grids can then have `Theta(j)` states and consume
`J^p` table work before the first successful trial. The eventual
successful trial's small grids do not retroactively bound that work.

A sufficient correction is a deterministic grid-size cap. For trial
`theta=2^-mu`, `mu>=1`, allow at most

```
Q_mu = 64*2^mu*(mu+ceil(log2(n+1))+1)                              (6)
```

nodes per coordinate. Abort this trial as soon as grid generation would
exceed the cap. The integer in (6) is computable without real logarithms.
The constant is deliberately loose.

The first trial satisfying the contraction threshold has
`kappa<=theta^-2`. Applying the continuous and integer grid counts to
the ratios after (4) shows that it fits (6), so it cannot abort. Every
earlier trial has bounded work whether or not its localization proof
applies. Initial grids fit the cap as well. Use the original prescribed
stage limit

```
J=max(0,ceil(log2(7 L n s0^2/(8 eps))/2)).
```

Gap validity and every pruning step are independent of the guessed
growth constant. A trial that finishes early has a valid answer.
Otherwise the first admissible trial succeeds by stage `J`. The number
of trials is `O(1+log kappa)`, and their cap bounds increase with `mu`.
Bounding them by the last trial times this number already suffices for
`f(p,kappa) poly(I+log(1/eps))`. No delicate geometric-series claim is
needed. A bit-work dovetail is another possible implementation, but
is unnecessary once (6) is enforced.

The main draft sharpens this cap to
`100 theta^-1 ceil(log2(n+2))`, with `theta<=1/4` and the sufficient
condition `theta^2<=1/(8kappa)`. This is valid: the grid-count numerator
contains `theta` times the radius/mesh ratio, and
`theta sqrt(kappa)<=1/sqrt(8)` cancels its apparent conditioning
dependence. The integer additive-one term contributes only a constant.
No `log(kappa)` factor is needed inside that sharper cap.

## 5. Rational denominators do not multiply across stages

For QP data let `D` be a common denominator for the original objective
coefficients, box endpoints, `L`, and `s0`. Its binary length is `O(I)`.
Start each trial at an original rational endpoint vector. Use the fixed
trial parameter `theta=2^-mu` and the original scales `h_j=s0 2^-j`.

The `k`th untruncated continuous outward distance from its center is

```
t_k = h_j [(2^mu+1)^k-2^(mu k)] / 2^(mu(k-1)),     k>=1.             (7)
```

It is independent of the center's denominator. Under the state cap,
`k<=Q_mu` for every emitted nonfinal point and for the possible next
candidate used to detect an abort, up to one harmless extra step.
Take `K=Q_mu+1`. All stage-`j` grid points, inherited box endpoints,
and chosen centers have denominators dividing

```
A_j=D 2^(j+mu K).                                                (8)
```

Proof is induction: new offsets satisfy (8) by (7), earlier points
have denominators dividing `A_(j-1)`, and clipping selects either an
inherited endpoint or a new candidate. Adding rational numbers on one
dyadic lattice takes the larger dyadic denominator, not their product.
Integer grids use integral centers, integral steps and integral clipped
endpoints, so introduce no additional coordinate denominators.

Thus coordinate bit length is `O(I+j+mu K)`. It does not require the
more pessimistic bound proportional to the sum of all stage grid
lengths. Intermediate integer-step comparisons and untruncated next
candidates have the same polynomial bound.

Every quadratic factor value and every curvature correction at stage
`j` is an integer multiple of

```
1/(8D A_j^2).                                                    (9)
```

DP messages, beliefs and min-marginals are sums and minima of such
values, hence retain the common denominator in (9). Message summation
does not multiply denominators. Numerator lengths add only polynomial
input-magnitude and term-count allowances: all coordinates stay in the
original bounded box, and corrections use intervals no longer than
its original sides.

Consequently exact evaluations, comparisons, floors, messages,
min-marginals and backtracking each have bit cost polynomial in
`I+j+mu K`, with an absolute polynomial exponent. Combining this with
the capped table count proves the proposed uniform FPT bit bound for
rational QP approximation. This argument is specific to explicitly
encoded quadratic data; it does not supply a bit bound for arbitrary
real factor-evaluation oracles.

## 6. Exact recovery and certificate scope

The original rational-QP height argument applies to continuous,
integer and mixed coordinates. Compute its denominator bounds `R,V`
from the **original input**. Pruning does not change the true optimizer
or optimal value, so there is no need to recompute these height bounds
from newly generated hull endpoints.

Use the existing trial targets

```
eps_mu=min(1/(4V^2), L theta^2/(16R^4))
```

and the corresponding stage limits. The first admissible trial both
isolates the optimal rational value and places its center close enough
for coordinate reconstruction. Check original bounds, required
integrality and exact equality of the reconstructed objective to the
isolated optimal value. These tests are essential for accepting trials
before the growth threshold is known to hold. Stage counts have
polynomial input bit length plus `O(mu)`, so exact recovery preserves
the FPT bit bound.

The main draft alternatively calls the certified approximate solver at
`eps=2^-q` for `q=1,2,4,8,...`. This also works with an explicit
acceptance rule: first require gap at most `1/(4V^2)`, reconstruct the
unique denominator-`V` value in the interval, then reconstruct each
coordinate within radius `rho=1/(4R^2)` of the returned feasible point.
Accept only after checking original bounds, integrality and exact
objective equality. The process succeeds once

```
eps <= min(1/(4V^2), g/(32R^4)).
```

The sufficient requested bit count is `poly(I)+O(log(kappa))`, using
`g>=L/kappa` and the input bit bound on `L`. Doubling overshoots this
count by at most a factor of two, and summing the approximate solver
costs preserves the FPT bound. This makes precise the main draft's
geometric precision schedule.

For purely integer boxes, the original zero-gap stopping argument also
continues to apply. Once a center equals the unique integer optimizer,
small enough first steps give zero adjacent corrections there. The
additive one in (4) does not prevent exact stopping.

A final restricted-box DP alone does not certify the original problem.
Retain a pruning certificate chain: previous grids and verified
min-marginals, the feasible incumbent used for each deletion, and the
strict conditional comparisons. A checker verifies that every
restriction preserves the original optimum, then checks the final
bound and any rational reconstruction. Storing the chain costs at
most the total work already bounded over all stages. Growth is used
for runtime, not certificate validity.

## Verification and remaining limits

A delegated independent audit confirmed the interval bound, endpoint
localization constants, mixed-domain count, and need to cap failed
trials. It independently identified the integer additive-one issue
and the need to use each coordinate's retained diameter.
The completed main draft was also read through its rational-arithmetic
and exact-output section. Its tighter `22/15` witness constant, cap,
denominator invariant and exact-recovery precision bound are sound.

The targeted command actually run was `python3 - <<'PY'`, using exact
`fractions.Fraction` arithmetic on a coupled two-coordinate QP with
one integer coordinate. Across 12 actual pruning stages, it checked
160 corrected assignments, 89 marginal nodes, 766 conditional-bound
samples, optimal-coordinate retention, retained-center feasibility,
and the dyadic denominator invariant. Twelve retained integer endpoints
explicitly violated the uncorrected continuous-only radius bound,
confirming the need for the additive one. The maximum coordinate grid
had five states in this small example.

These finite checks do not implement the two-pass tree algorithm or
establish practical performance. The table and bit bounds above are
analytic. No project-wide verification, CI inspection, external search,
or knowledge-base access was performed.
