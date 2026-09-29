# Convex-boundary avoidance under rational grid perturbations

Date: 2026-09-25. Status: complete elementary proof with an
[independent adversarial review](smoothed-penalty-review.md). This is a
supporting geometric lemma for the penalty
research. No novelty is claimed for convex-boundary anticoncentration or
for the grid coupling. The useful point is an explicit bound in a rational
perturbation model, without smoothness, boundedness, or full-dimensionality
assumptions on the convex sets.

## Result and conventions

Let `m>=1`, `sigma>0`, and

```
B = b0 + [-sigma,sigma]^m.
```

All boundaries below are **ambient topological boundaries in R^m**.
In particular, a closed convex set with empty interior is its own boundary.
The boundaries of the empty set and of `R^m` are empty; distance to the
empty set is `+infinity`. Write `dist_inf` for distance in the infinity norm.

**Theorem 1 (continuous perturbation).** For any closed convex set
`C subset R^m`, any `d>=0`, and `U` uniform on `B`,

```
Pr[dist_inf(U,boundary C) <= d] <= min(1, 2 m d / sigma).       (1)
```

The same bound holds with Euclidean distance in the event. Its constants
are independent of the diameter, location, representation, and curvature
of `C`. The linear dependence on `m` is necessary for a uniform bound of
this form over cubes.

**Theorem 2 (centered grid).** For an integer `q>=1`, set `h=2 sigma/q` and
let `G` have independent coordinates, each uniform on the `q` cell centers

```
b0_i - sigma + (k+1/2) h,       k=0,...,q-1.
```

Then, for either infinity or Euclidean distance,

```
Pr[dist(G,boundary C) <= d]
    <= min(1, 2 m (d+h/2) / sigma).                           (2)
```

If `b0` and `sigma` are rational, every grid point is rational. Taking `q`
to be a power of two permits exact uniform sampling with `m log2(q)` bits.

**Theorem 3 (endpoint grid).** For an integer `q>=1`, set `h=2 sigma/q` and
let `G` have independent coordinates uniform on the `q+1` points

```
b0_i - sigma + k h,            k=0,...,q.
```

Then

```
Pr[dist(G,boundary C) <= d]
    <= min(1, 2 m (d+h/2) / (sigma+h/2))
    <= min(1, 2 m (d+h/2) / sigma).                           (3)
```

Thus an endpoint grid and a cell-center grid obey the same simpler bound,
but their exact coupling cubes differ. Calling endpoint jitter uniform on
the original cube would be incorrect.

## Elementary proof by interval sections

For a set `A` and a coordinate segment `S_i=[-r,r] e_i`, define

```
A + S_i  = {a+s : a in A, s in S_i},
A minus_m S_i = {x : x+S_i subset A}.
```

The second operation is Minkowski erosion; the notation `minus_m` is used
only in this proof. Both operations preserve convexity and closedness.
For addition, closedness follows because `S_i` is compact. For erosion,
write it as the intersection of the closed sets `A-s`, `s in S_i`.

Fix all coordinates other than `i`. The section of a closed convex `A`
along the resulting coordinate line is an interval, possibly empty, a
point, a ray, or the whole line. Adding `S_i` extends each finite endpoint
by `r`. Eroding by `S_i` removes at most `r` at each finite endpoint,
possibly deleting the interval. These statements remain true after
intersecting the changed part with any fixed interval on that line.
Consequently, each operation changes the length **within the original
cube section** by at most `2r`.

Fubini's theorem therefore gives

```
vol(((A+S_i) outside A) intersect B) <= 2r (2 sigma)^(m-1),
vol((A outside (A minus_m S_i)) intersect B)
                                      <= 2r (2 sigma)^(m-1).   (4)
```

These statements do not subtract infinite volumes. Only changed portions
inside the bounded cube are measured. Unbounded interval sections cause
no problem: a ray has one finite endpoint and a whole line has none.

Let `Q_r=[-r,r]^m`. Successive addition by the `m` coordinate segments
gives `A+Q_r`. Successive erosion gives `A minus_m Q_r`, because

```
(A minus_m S) minus_m T = A minus_m (S+T).
```

Sum (4) over the nested sequence of additions and, separately, the nested
sequence of erosions. With `A=C`, this yields

```
vol(((C+Q_r) outside C) intersect B)
                                      <= 2mr (2 sigma)^(m-1),
vol((C outside (C minus_m Q_r)) intersect B)
                                      <= 2mr (2 sigma)^(m-1). (5)
```

Now fix `r>d`. Every `x` with `dist_inf(x,boundary C)<=d` lies in
`C+Q_r`: choose a boundary point within distance less than `r`, and use
`boundary C subset C`. Such an `x` cannot lie in `C minus_m Q_r`.
Indeed, a boundary point within distance less than `r` has points outside
`C` arbitrarily close to it, and one of them lies in `x+Q_r`. Hence

```
{x : dist_inf(x,boundary C)<=d}
    subset (C+Q_r) outside (C minus_m Q_r).                  (6)
```

Combine (5) and (6), divide by `(2 sigma)^m`, and let `r` decrease to `d`.
This proves (1), including `d=0`. The empty-set and whole-space cases are
immediate from the boundary convention. Lower-dimensional convex sets
require no separate regularization. Finally,

```
dist_inf(x,boundary C) <= dist_2(x,boundary C),
```

so the Euclidean event is contained in the infinity-norm event. This proves
the continuous theorem. The small enlargement `r>d` handles closed-tube
endpoints; silently identifying a closed tube with an erosion difference
at exactly `r=d` would miss those endpoints.

For Theorem 2, independently add `J` uniform on `[-h/2,h/2]^m` to `G`.
The equal grid cells tile `B` up to null faces, so `U=G+J` is exactly uniform
on `B`. Distance to a fixed nonempty set is 1-Lipschitz. Therefore

```
dist_inf(G,boundary C)<=d
    implies dist_inf(U,boundary C)<=d+h/2.
```

The same implication follows from the Euclidean event at `G`. Apply (1).
Using infinity distance for the coupling is what avoids a factor `sqrt(m)`.
Theorem 3 follows identically, except the jitter cells tile
`b0+[-sigma-h/2,sigma+h/2]^m`. This proves (2) and (3).

## Simultaneous boundary avoidance and bit counts

Let `C_1,...,C_N` be fixed closed convex sets, and define

```
Delta(b) = min_j dist_inf(b,boundary C_j),     N>=1.
```

A union bound gives, for either grid convention using its simpler bound,

```
Pr[Delta(G)<=d] <= min(1, 2mN(d+h/2)/sigma).                  (7)
```

No independence between the different boundary events is needed. The
sets must be fixed independently of the sampled perturbation; permitting
an arbitrary `C_j` chosen after seeing `G` invalidates the statement.

The infinity norm here supplies the margin needed by the
[penalty theorem](smoothed-penalty.md): if `b in C_j` and `Delta(b)>d`,
then `b+[-d,d]^m subset C_j`. Otherwise the segment from `b` to a point
of that cube outside `C_j` would meet the boundary within infinity
distance `d`. If `b outside C_j`, its infinity distance from `C_j` is
greater than `d`, because distance from a point outside a nonempty
closed set to that set equals its distance to the boundary. Empty and
whole-space sets follow from the stated conventions.

As an optional consequence, (7) also holds if `Delta` is defined using
Euclidean distance. However, a Euclidean boundary distance greater than
`d` alone guarantees a Euclidean ball of radius `d`, not the cube of
radius `d`. The primary corollary therefore keeps the infinity metric.

For `0<alpha<1`, choose

```
d = alpha sigma/(4mN),       h <= alpha sigma/(2mN).          (8)
```

Then `Pr[Delta(G)>d]>=1-alpha`. For the centered grid, a power-of-two
`q>=4mN/alpha` suffices, requiring

```
log2(q) = O(log m + log N + log(1/alpha))
```

random bits per coordinate. The reciprocal separation in (8) is
`4mN/(alpha sigma)`. Even when `N` is exponential in the number of binary
variables, its **logarithm** has polynomial size. The dependence on `N`
does not disappear: the separation itself can be exponentially small.

This is a separation statement, not yet a bound on a penalty or on an
algorithm. An application must separately prove that the needed penalty
is controlled by an objective range divided by this separation, and must
account for the encoding of that range and of `sigma`.

The probability guarantee is unconditional. If `F` is the event that the
perturbed optimization problem is feasible, the direct conclusion is

```
Pr[F and Delta(G)<=d] <= alpha.
```

When `Pr[F]>0`, a conditional failure estimate is `alpha/Pr[F]`; one cannot
replace it by `alpha` without another argument. Closedness must also be
checked for each proposed residual image. A linear image of a general
closed convex set need not be closed, whereas a continuous image of a
compact native set is compact. Replacing a residual image by its closure
without explanation can change feasibility.

## Necessary losses and limitations

The dimension factor is not a proof artifact. Fix `0<a<sigma` and let
`C=[-a,a]^m`. For sufficiently small `d>0`, its entire infinity-norm
boundary tube lies in `B` and has volume

```
[2(a+d)]^m - [2(a-d)]^m.
```

After division by `(2 sigma)^m`, its derivative at `d=0` is
`(2m/sigma)(a/sigma)^(m-1)`. Sending `a` up to `sigma` shows that the
coefficient `2m` in (1) is optimal among bounds `K_m d/sigma`. Euclidean
tubes have the same first-order coefficient: each face contributes a
two-sided slab, and edge intersections contribute only higher-order terms.

The grid correction also cannot be omitted. In dimension one, choose
`C` to be a nondegenerate interval whose two endpoints are distinct grid
points. At `d=0`, the boundary event has probability `2/q` for a centered
`q`-point grid. Since `h=2 sigma/q`, this is exactly `h/sigma`, which
matches (2) at `m=1`. A continuous probability-zero assertion does not
transfer to an atomic grid distribution.

The assumptions concerning convexity and the number of sets matter. An
arbitrary closed set can have a boundary of positive Lebesgue measure.
A large union of convex sets can also place boundaries throughout the
perturbation cube; formula (7) pays explicitly for its number of sets.
Nothing here establishes a polynomial-time MINLP algorithm or a universal
bound after arbitrary perturbations of all model coefficients.

## Sources examined and relation to prior results

1. Dunagan, Spielman, and Teng, *Smoothed Analysis of Condition Numbers and
   Complexity Implications for Linear Programming*, author manuscript
   dated March 30, 2009, later Mathematical Programming 126 (2011), 315–350.
   [Author PDF](https://www.cs.yale.edu/homes/spielman/Research/lpcond.pdf).
   Theorem 2.3.3 states Ball's Gaussian boundary-area bound. Lemma 2.3.4
   bounds each of the inner and outer Euclidean boundary-tube probabilities
   by `4 m^(1/4) d/sigma` under Gaussian perturbation, by integrating convex
   shells. Corollary 2.3.5 transfers this geometry to distance from
   ill-posedness. These are stronger dimension estimates in a different
   noise model. The present cube estimate cannot inherit that dimension
   dependence, as the box example above shows. The broad use of boundary
   avoidance to control conditioning is established prior work.

2. Bürgisser and Amelunxen, *Robust Smoothed Analysis of a Condition Number
   for Linear Programming*, [arXiv:0803.0925v3](https://arxiv.org/abs/0803.0925v3).
   Theorem 3.3 bounds inner and outer neighborhoods of properly convex
   spherical sets inside spherical caps. Corollary 3.4 gives the bound
   `13 m epsilon/(4 sigma)` for each side when `epsilon<=sigma/(2m)`.
   This gives a directly relevant linear-dimension uniform-noise precedent.
   Its domain, metric, and noise distribution are spherical; it is not
   the finite rational product-grid statement used here. The downloaded
   PDF's title differs from the original 2008 version, which was called
   *Uniform Smoothed Analysis of a Condition Number for Linear Programming*.
   The theorem numbering here refers to version 3.

3. Stefani, *On the Monotonicity of Perimeter of Convex Bodies*,
   [arXiv:1612.00295v1](https://arxiv.org/abs/1612.00295v1), 2016.
   The introduction, (1.1) and (1.4), recalls classical monotonicity of
   ordinary and anisotropic perimeter under inclusion of convex bodies.
   Those facts offer another route to tube bounds. The coordinate-section
   argument above avoids requiring a perimeter formula, a coarea theorem,
   or smooth approximation. It does not advance the classical perimeter
   theory.

4. Local [finite-grid smoothing note](../notes/research-20260922-finite-grid-smoothing.md),
   especially its discussion of atomic grid noise and continuous jitter.
   That note controls crossings of univariate polynomial envelopes using
   their finitely many monotone arcs. The present argument concerns a
   neighborhood of a convex boundary in the perturbation space. Its
   direct equal-cell coupling and coordinate-section estimate do not rely
   on the envelope setting.

The searches also examined the general condition-number/tube literature
under convex boundary, smoothed feasibility, uniform cube perturbation,
and finite-precision terminology. These bounded searches do not establish
novelty. The geometric statement is used as an elementary auxiliary fact;
any research claim should concern a separately proved consequence for the
optimization model and compare that consequence with existing exact-penalty
and smoothed-conditioning results.

## Verification record

The proof explicitly checks empty sets, the whole space, lower-dimensional
sets, unbounded sections, closed tube endpoints, and both grid conventions.
The independent review reconstructed the coordinate-section proof and
found no proof-breaking gap. It identified a presentation mismatch: the
simultaneous corollary initially used Euclidean distance, whereas the
penalty application needs an infinity-norm cube margin. The corollary now
uses infinity distance throughout, with Euclidean distance retained as an
optional consequence. No numerical constants changed.
An exact rational Python check exhaustively verified (4)'s one-dimensional
clipping inequality for 187,272 cases: interval and clipping endpoints
from `{i/2:-8<=i<=8}`, all ordered nondegenerate clipping intervals, and
radii `{i/4:0<=i<=8}`. Both expansion and erosion changes were between zero
and `2r` in every case. This checks a useful local inequality but does not
replace the proof or independently verify Fubini's theorem, the set
identities, or the probabilistic coupling.

The targeted command was an inline `python` script using
`fractions.Fraction`; its reported result was
`PASS: 187272 exact clipped interval expansion/erosion cases`.
The three primary PDFs above were downloaded to `/tmp/smoothed-*.pdf` and
their relevant theorem statements inspected with `pdftotext -layout`.
No project-wide verification or CI inspection was performed.
