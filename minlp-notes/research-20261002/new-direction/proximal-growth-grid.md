# A proximal grid algorithm with a supplied growth bound

Date: 2026-10-02. Status: a complete approximation derivation, including
a rational-QP bit bound and targeted exact checks. A
[fresh independent review](proximal-grid-adversary.md) found no fatal
gap. No external priority claim is made.

The algorithm handles growth toward an arbitrary compact optimal set.
It needs no uniqueness, finite projection count, variable-occurrence
bound, or separation between optimizers. Its material tradeoff is that
a **valid growth bound must be supplied and trusted**. Its restricted
search domains and global lower intervals depend on that promise.
The stopping test does not provide the assumption-independent certificate
or unknown-growth guarantee of the
[pruned unique-optimum theorem](pruned-coordinate-grid.md).

## 1. Result and assumptions

Let `X` be a nonempty bounded product of continuous intervals and integer
intervals. Round integer endpoints inward and substitute fixed
coordinates out. Let `n>=1` be the number of remaining coordinates,
and let `s0>0` be the largest original side length.

The objective `F` is continuous on the mixed domain and has a continuous
extension to the original continuous box. It is supplied as factors on
a tree decomposition with bag size at most `p`, `N` bags and `M_f`
assigned factors. Assume a known `L>0` bounds upper coordinate curvature
on that continuous box: subtracting `L x_i^2/2` makes every coordinate
restriction concave. This is the same assumption as in the
[corrected point-grid theorem](../geometric-dp/theorem.md).

Write

```
f*=min_X F,              S={x in X:F(x)=f*}.
```

The nonempty compact set `S` can be finite or infinite. A supplied
valid growth bound `g0>0` satisfies

```
F(x)-f* >= g0 dist(x,S)^2           for every x in X.                (1)
```

Set `kappa=max(1,L/g0)`. The algorithm only needs a valid supplied
upper bound on this ratio; replacing `g0` by `L/kappa` preserves (1).
A badly underestimated growth bound worsens the numerical parameter.
The algorithm does not verify this global promise.

**Approximation theorem.** Under these assumptions, a deterministic
algorithm returns a feasible point `y` and a promise-dependent interval
`[LB,F(y)]` containing `f*`, of width at most `eps`. Its exact-oracle
work is

```
f(p,kappa) (N+M_f+n)(n+2) poly(1+log_+(L n s0^2/eps)),             (2)
```

where the polynomial exponent is absolute. For rational quadratic
input, rational `g0` and dyadic `eps=2^-q`, its bit complexity is

```
f_1(p,kappa) (I+q+1)^C,                                           (3)
```

with an absolute `C`. Here `I` includes the supplied growth bound and
decomposition. There is no bound on the number of optimal coordinate
values. For general factors, exact evaluation and comparison remain
oracle assumptions; (3) is asserted for explicitly encoded rational QP.

For a quadratic, `L` can be the largest positive diagonal Hessian entry.
If all diagonal entries are nonpositive, the separate coordinate-concave
endpoint DP solves the problem exactly without (1).

### Classical existence of growth for bounded quadratic programs

For a quadratic on a nonempty compact polytope, some positive growth
constant toward its full optimal set always exists. This is an application
of Luo and Sturm, *Error Bounds for Quadratic Systems*, Theorem 3.3
(manuscript p. 11; published chapter pp. 383--404, 2000;
[source and locator](../../literature/papers/luo2000-error-bounds-for-quadratic-systems/paper.md),
[original text](../../literature/papers/luo2000-error-bounds-for-quadratic-systems/original.pdf)).
Their theorem gives `dist(x,S)<=c |q(x)|^(1/2)` for a quadratic `q`
on a polytope when its zero set `S` is nonempty. Apply it to
`q=F-f*` and square: (1) holds with `g0=1/c^2`. Neither convexity nor
an isolated optimizer is required. This qualitative fact is classical;
it is not a contribution of the grid algorithm.

A bounded mixed box has only finitely many integer slices. Apply that
result to every slice attaining `f*`; distance to the full optimal set
is no greater than distance to the slice's optimal set. Every other
nonempty slice has a positive minimum gap above `f*`, which also bounds
gap divided by squared distance because the whole domain is bounded.
Taking the minimum of these finitely many positive constants proves the
same qualitative conclusion for mixed boxes. This is an existence
argument, not an instruction to enumerate slices.

Existence of some constant does not supply a useful numerical lower bound
on it. The theorem here still requires a supplied valid `g0` or `kappa`,
and its complexity can be large when the valid ratio is large. Neither
the classical error bound nor the final interval test validates an
untrusted numerical growth estimate.

## 2. The iteration

Choose the smallest integer `mu>=2` such that, with `theta=2^-mu`,

```
theta^2 kappa <= 1/8.
```

Then `theta<=1/4` and `theta^-1<=6 sqrt(kappa)`. Define

```
lambda=L theta^2/4,
rho=2 ceil(sqrt(kappa n)),
h_j=s0 2^-j.                                                     (4)
```

Rational comparisons compute `mu` and `rho`; no exact transcendental
operation is needed. Start at any rational feasible point `c`, for
example the original lower endpoint vector.

At stage `j=0,1,...`:

1. Build the fresh product box

   ```
   B_j = X intersect product_i [c_i-rho h_j,c_i+rho h_j].            (5)
   ```

   Round integer endpoints inward. This intersects the **original**
   box `X`, not the preceding stage's box. The center remains feasible.

2. In each coordinate of `B_j`, generate the usual geometric grid
   centered at `c_i`, with step `h_j+theta t` at distance `t` from the
   center. For integer coordinates use `max(1,floor(h_j+theta t))`.
   Clip final steps to the current coordinate endpoints.

3. At a node `v`, let `ell_i(v)` be the largest adjacent grid interval
   length. Ignore unit intervals for integer coordinates. A singleton
   has `ell_i=0`. Put

   ```
   d_i(v)=L ell_i(v)^2/8,     D(y)=sum_i d_i(y_i).
   ```

4. Minimize the finite corrected proximal objective exactly:

   ```
   P_j(y)=F(y)-D(y)+lambda ||y-c||^2.                              (6)
   ```

   Let `y_j` be a minimizer and `m_j=P_j(y_j)`. The correction and
   proximity terms are unary, so the supplied tree decomposition is
   unchanged. Ordinary finite-state min-sum DP computes this minimum
   and an attaining assignment.

5. Set `Ebar_j=4 kappa n h_j^2` and report the interval

   ```
   U_j=F(y_j),
   LB_j=m_j-lambda[(1+theta^2/2)Ebar_j+n h_j^2/2].                  (7)
   ```

   Stop when `U_j-LB_j<=eps`; otherwise set `c=y_j` and continue.

The intervals in (7) are globally valid under the supplied growth
promise. The finite DP certifies its own discrete minimum exactly;
the interpretation of (7) as a bound for the original box also uses
the growth-based containment invariant proved below.

## 3. Rounding a nearest optimizer

The standard grid construction gives, at every node,

```
ell_i(v)<=h+theta |v-c_i|,
D(y)<=L n h^2/4+lambda ||y-c||^2.                                (8)
```

The second inequality follows from `(a+b)^2<=2a^2+2b^2` and the
definition `lambda=L theta^2/4`. This exact cancellation coefficient
is sufficient; the proof needs no larger proximal penalty.

Suppose the current box contains a nearest optimizer `s in S` to the
center, and write `E=||s-c||^2=dist(c,S)^2`. Independently round each
coordinate of `s` to its enclosing grid endpoints, preserving its
mean, to obtain `Y`.

The corrected interpolation inequality gives

```
E[F(Y)-D(Y)] <= F(s)=f*.                                        (9)
```

Here the first `E` in (9) denotes expectation. To avoid ambiguity below,
write `V_round=sum_i Var(Y_i)` for the rounding variance. Independence
and preservation of the mean give

```
E[||Y-c||^2] = E+V_round.                                       (10)
```

For a coordinate not already on its grid, the enclosing interval has
length at most `h+theta |s_i-c_i|`. Its nearer endpoint to `c_i` is at
most that distance from the center, and clipping only shortens a step.
Therefore

```
Var(Y_i) <= (h+theta |s_i-c_i|)^2/4,
V_round <= (n h^2+theta^2 E)/2.                                 (11)
```

An integer point cannot be strictly inside a unit interval; rounding
there is deterministic and has zero variance. Integer intervals of
length at least two obey the same upper step bound. Singletons are
also deterministic. Thus (9)--(11) hold for mixed boxes and for
boundary optimizers.

Since a minimum is at most an expectation, (9)--(11) imply

```
m_j <= f*+lambda[(1+theta^2/2)E+n h_j^2/2].                       (12)
```

This argument rounds one nearest optimizer at the current stage.
It does not need a collection of anchors covering every member of `S`,
nor does it assume that successive stages approach the same optimizer.

## 4. Containment, contraction and the promised interval

We prove the invariant

```
dist(y_j,S)^2 <= kappa n h_j^2.                                  (13)
```

Before stage zero, `dist(c,S)^2<=n s0^2<=Ebar_0`. Before a later stage,
(13) and `h_(j-1)=2h_j` give

```
E=dist(c,S)^2 <= 4 kappa n h_j^2=Ebar_j.                          (14)
```

Compactness supplies a nearest optimizer. Each of its coordinate
differences from `c` is at most `sqrt(Ebar_j)<=rho h_j`, so it lies in
(5). Inward rounding of integer endpoints preserves its integer
coordinates. This proves the containment needed in Section 3.

Substituting (14) into (12) proves `LB_j<=f*`. Feasibility gives
`f*<=U_j`. Moreover, using (6)--(8),

```
U_j-LB_j
 = D(y_j)-lambda ||y_j-c||^2
   +lambda[(1+theta^2/2)Ebar_j+n h_j^2/2]
 <= (L n h_j^2/4)(1+theta^2/2)(1+4 kappa theta^2)
 <= (99/256)L n h_j^2
 < L n h_j^2/2.                                                 (15)
```

The last bound uses `theta<=1/4` and `kappa theta^2<=1/8`.
Growth now gives

```
dist(y_j,S)^2 <= (U_j-f*)/g0
               <= (L/g0)n h_j^2/2
               <= kappa n h_j^2/2,
```

which is stronger than (13) and closes the induction.

It suffices to run through

```
J=max(0,ceil(log2(L n s0^2/(2 eps))/2)).                          (16)
```

Compute the integer in (16) by rational comparisons with powers of
four. No estimate of a separation between members of `S` occurs.

Rebuilding from `X` in (5) matters. A nearest optimizer to the new
center may lie outside the previous stage's restricted box. Intersecting
successive boxes would need a different invariant. The fresh-box rule
allows this change of nearest optimizer directly.

## 5. The coordinate grids stay small

The distance from the center to either endpoint in (5) is at most
`rho h_j`. The continuous outward-step count is at most

```
1+ceil(log(1+theta rho)/log(1+theta)).
```

For integer grids, the original count uses denominator
`log(1+theta/3)` and normalizes distances by `H=max(h_j,1)`.
Since `h_j/H<=1`, its numerator is at most `log(1+theta rho)` too.

The definition of `rho` gives

```
theta rho <= 2 theta sqrt(kappa n)+2 theta
            <= sqrt(n/2)+1/2.
```

Thus an absolute safe bound on all grid nodes in one coordinate is

```
K=100 theta^-1 ceil(log2(n+2)).                                 (17)
```

It is independent of the stage, domain diameter and target accuracy.
The integer and continuous counts use the same bound; fixed stage
coordinates have only one state. No dense discretization of an integer
interval is assumed.

One stage costs `O(p(N+M_f)K^p)` table operations, with the standard
bag-index factors. Summing child tables does not add a branching-degree
parameter. The elementary bound

```
ceil(log2(n+2))^p <= (C p)^p (n+2)
```

for an absolute `C` absorbs the logarithmic power into one ordinary
input-size factor. Together with `theta^-1=O(sqrt(kappa))` and (16),
this proves the exact-oracle work bound (2). Variable occurrence is
irrelevant because all grid coordinates are globally consistent.

## 6. Rational quadratic bit complexity

Assume rational quadratic factors, rational endpoints and a supplied
rational `g0`. Let `I` be their total binary encoding length, including
the decomposition. For this bit bound, initialize at the lower endpoint
vector; an additional supplied center would have to be included in the
input length and common denominator. After substituting fixed coordinates,
choose a common positive denominator `D0` for the resulting quadratic coefficients,
remaining endpoints and `L`. Substitution can introduce new coefficient
denominators, so taking only a denominator of the unsubstituted factors
would be insufficient. The chosen `D0` has polynomial binary length in
the original input, and `s0` has denominator dividing `D0`.

Fix `theta=2^-mu` and the integer bound `K` in (17), increased by one
if needed for the first unretained outward candidate. An unclipped
outward displacement at stage `j` has the form

```
h_j[(2^mu+1)^k-2^(mu k)]/2^(mu(k-1)),      1<=k<=K.
```

All generated coordinates have denominators dividing

```
A_j=D0 2^(j+mu K).                                               (18)
```

Indeed, previous centers have denominators dividing `A_(j-1)`, which
divides `A_j`. New artificial endpoints `c_i plus or minus rho h_j`
and new geometric offsets also satisfy (18). Clipping selects an
original or artificial endpoint. Integer inward rounding and integer
grid steps create integral values. Sums of dyadic-lattice coordinates
take the larger dyadic denominator; they do not multiply denominators
across stages.

Quadratic factor values and the corrections have common denominators
dividing `8D0 A_j^2`. The additional term
`lambda ||y-c||^2`, with `lambda=L 2^(-2mu-2)`, has a denominator
dividing the same quantity times `2^(2mu+2)`. Consequently proximal
DP messages have a common denominator of polynomial bit length in

```
I+j+mu K.
```

Their magnitudes are bounded by input objective magnitudes, the total
factor count, and squared original-box diameters. The centers and
evaluated nodes stay in the original box. This gives polynomial-bit
numerators as well. Floors, rational comparisons, backtracking, and
forming the interval (7) have the same polynomial bound; the rational
`kappa` in that interval adds only input bit length.

The radius multiplier has `O(log n+log kappa)` bits. The stage bound
in (16) is `O(I+q+1)` for `eps=2^-q`. Combining the arithmetic bound
with the table count and logarithmic-power absorption proves (3), with
an exponent independent of `p` and `kappa`.

## 7. Scope of the promise and relation to the earlier obstruction

The supplied growth bound does two jobs: it guarantees that the fresh
box contains a global optimizer, and it justifies the error allowance
in (7). Exact verification of the local finite DP does not verify this
global growth assumption. If the supplied bound is invalid, a fresh
box can exclude every optimizer and the reported interval can fail.

Therefore an unknown-growth restart schedule cannot stop merely because
one trial reports a narrow interval in (7). Such a trial has not supplied
an independent global certificate. No such unknown-growth or
assumption-independent certification extension is proved here.

### An invalid growth bound can certify the wrong value

This failure is explicit. On `[0,1]^2`, let

```
F(x,y)=x^2+y^2-3xy+(63/128)(x+y).
```

Its unique global optimizer is `(1,1)`, with `f*=-1/64`. Indeed, setting
`t=x+y` and using `xy<=t^2/4` gives
`F>=-t^2/4+(63/128)t`; this concave expression on `[0,2]` has its
unique minimizing endpoint at `t=2`. At `(0,0)` the objective is zero,
so every valid growth constant satisfies `g0<=1/128`. Since `L=2`,
the valid conditioning ratio is at least 256.

Pretend instead that `kappa=1`, start at `(0,0)`, and use the specified
`theta=1/4`, `lambda=1/32`, `rho=4`. Exact enumeration of the first
three grids gives `(0,0)` as the proximal minimizer, with respective
minimum values `-1/2`, `-1/8`, and `-1/32`.

At every stage `j>=3`, put `h=2^-j` and `r=4h<=1/2`. The fresh box is
`[0,r]^2`, and its grid in each coordinate is

```
h times {0,1,9/4,61/16,4}.
```

The maximum adjacent length is `25h/16`, so
`D<=625h^2/512`, whereas `D(0,0)=h^2/2`. On this box,

```
F(x,y)>=(63/128-r/2)(x+y)>=31(x+y)/128.
```

Here `x^2+y^2>=2xy` and `xy<=r(x+y)/2` prove the first inequality.
Every nonzero grid point has `x+y>=h`; since `h<=1/8`, its objective
is at least `31h^2/16`. This exceeds
`(625/512-1/2)h^2`. The nonnegative proximal term therefore makes
`(0,0)` the unique proximal minimizer at every later stage as well.

The claimed interval formula gives

```
LB_j=-(101/128)h_j^2,       U_j=0.
```

Already at `j=3`, its lower endpoint is `-101/8192`, greater than
the true optimum `-128/8192`. Its width subsequently tends to zero
around the wrong value. The example shows why a narrow local interval
cannot validate an untrusted growth guess.

This tradeoff explains the difference from the diagonal-manifold example
in [projection-anchors.md](projection-anchors.md), Section 8. That example
forces fine grids across whole optimal coordinate projections for the
full-domain `F-D` certificate. Here the growth promise permits a small
region containing at least one optimizer, and (7) subtracts an explicit
proximity allowance from a different discrete objective. The original
full-domain certificate obstruction still holds.

The theorem includes infinite optimal sets, so it needs no parameter
`A=sum_i |pi_i(S)|` or `a=max_i |pi_i(S)|`. This does not resolve the
stronger finite-projection question with unknown growth and independently
checkable global certificates.

For finite optimal sets of rational QP, the existing bounded-denominator
argument in [exact-nonunique-box-qp.md](../geometric-dp/exact-nonunique-box-qp.md)
offers an exact-output extension when the growth bound is trusted.
This note's theorem and arithmetic proof establish approximation. Exact
optimizer recovery for arbitrary compact optimal sets is not asserted.

## Verification

The proximity cancellation and nearest-optimizer rounding argument were
derived independently by the parent researcher, this author, and a
delegated reviewer. The reviewer checked boundary points, integer unit
intervals, singleton domains, the fresh-box invariant, the `99/256`
constant, and rational denominator propagation. A separate fresh
adversarial review, with a second independent reviewer, found no fatal
gap; its [record](proximal-grid-adversary.md) includes separate exact
checks on continuous, disconnected and mixed optimal sets.

The targeted command actually run here was `python3 - <<'PY'`, using
`fractions.Fraction`. It performed 36 complete proximal-grid stages and
enumerated 2,661 finite-grid assignments across three two-coordinate
quadratic examples:

- a continuum of minimizers on a line segment;
- two isolated continuous minimizers;
- the same two-minimizer construction with one integer coordinate.

All stages checked the promise interval against the known optimum,
its width bound, growth-based distance contraction, rational coordinate
denominators, and 72 coordinate checks that a nearest optimizer lay in
the fresh box. Maximum coordinate-grid sizes were 9, 21 and 9.
The examples exercise the argument, not competitive performance.
The invalid-growth example was separately derived and its first six
stages checked with exact rational arithmetic by the parent researcher;
the displayed inequalities establish its behavior at every later stage.

These exact checks use exhaustive small-grid minimization rather than
a junction-tree implementation. No project-wide verification, CI
inspection, external search, or knowledge-base access was performed.
