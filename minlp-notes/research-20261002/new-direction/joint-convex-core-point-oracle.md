# Polynomial expected evaluation of selected noisy convex coordinates

Date: 2026-10-02. Status: passed a
[fresh independent actual-file review](joint-convex-core-point-oracle-review.md).
The [focused prior comparison](../prior-art/joint-convex-core-point-oracle-prior.md)
is complete, without a publication-priority claim. The key change
from the [coupled core certificate](coupled-polytope-core-oracle.md) is
to bound a convex near-optimal sublevel set directly. There is no cell
enumeration and no exponential factor in the number of queried coordinates.

## 1. Input, exact output, and scope

Fix a degree bound `d`. Let `P` be a nonempty bounded rational polytope
in continuous variables `x=(v,z)`, where `v in [0,1]^k`, `k>=1`, and
a rational bounding box for the remaining coordinates is supplied.
Let `F_0` be an explicitly represented rational polynomial of degree at
most `d`, convex on `P`. Convexity is verified or has a supplied
certificate. The base length `I` includes the polynomial, polytope,
bounding box, chosen core coordinates, certificate data, and a rational
noise half-width `sigma>0`. The claimed polynomial bound presumes
polynomial-time certificate verification; otherwise add its actual cost.
Convexity recognition is not an uncharged computational step.

Perturb only the selected coordinates:

```
F_gamma(x)=F_0(x)+gamma'v.                               (1)
```

Let `x_gamma^lex` be the lexicographically first global optimizer, with
core coordinates ordered first, and let `a_gamma` denote its core.
Compactness makes this selector well-defined even with flat optimizer
sets. There is one base-computable power-of-two grid size `M`, with
`log M=poly_d(I)`, such that independent endpoint-inclusive uniform
`M`-point noise in `[-sigma,sigma]^k` admits the following evaluator.

**Theorem.** For every draw and every integer `q>=0`, the evaluator
returns a rational feasible point `x_q=(v_q,z_q) in P` and a rational
global value interval satisfying

```
ell_q <= min_P F_gamma <= U_q=F_gamma(x_q),
U_q-ell_q <= 2^(-q),
||v_q-a_gamma||_2 <= 2^(-q).                             (2)
```

Expected bit work and expected output/verification-record size are

```
poly_d(I+q).                                            (3)
```

The polynomial exponent does not depend on the number of selected or
unselected variables. A single random work factor of constant expected
size bounds all query precisions after a fixed polynomial in `I+q`.
The finite law is chosen once; there is no accuracy-dependent resampling.
There is no numerical inverse-curvature, inverse-noise, or condition
parameter in (3): `sigma` and all coefficient magnitudes are charged
through their binary input lengths.

The output is an exact selected-core Cauchy name and certified objective
approximation for one sampled rational instance. The residual vector
`z_q` need not approach any selected optimal residual point. Taking
every variable as core, when its box is the unit box, gives full selected
optimizer Cauchy output under independent noise on every coordinate.
No polynomial-size expanded algebraic representation is asserted.

If no core coordinate remains, only convex value evaluation is needed.
Rational singleton polytopes are handled by direct evaluation. Rational
affine scaling can normalize a nonunit chosen coordinate box, but changes
the physical perturbation directions and must be included in the input;
no invariance under such scaling is claimed here.

## 2. Two reviewed interfaces and one finite law

The [convex polytope interface](convex-polytope-value-interface.md) gives
certified rational feasible objective approximations on `P` in polynomial
bit work, with no strong-convexity premise. It uses exact rational LP
affine-hull reduction, the verified Turing weak-optimization interface,
and rational error-box feasibility repair. Its exact fallback uses
core-first lexicographic scalar singleton formulas and has cost

```
B_0 poly_d(I+b+q),   B_0=2^(poly_d(I)),                  (4)
```

where `b` is sampled coefficient length. The base exponential budget is
computable before sampling and is independent of `b,q`. It handles tied
and positive-dimensional optimum sets and supports feasible rational
approximation as well as exact point/value refinement.

The compact-domain projected growth proof in Section 2 of the
[coupled core note](coupled-polytope-core-oracle.md) supplies a
base-computable `C_g=2^(poly_d(I))` for

```
Pr(g<t) <= k t/sigma+C_g/M,    t>0,                      (5)
```

where `g` is the largest constant for which some global optimizer
`(a,z_0)` satisfies
`F_gamma(v,z)-F_gamma(a,z_0)>=g||v-a||_2^2` on `P`.
Residual ties do not force `g=0`; distinct optimal cores do. The projected
singleton case has `g=+infinity`. This tail follows directly from the
compact full-domain proximal proof and two-block finite-format transfer.
It does not assume a continuous partially minimized value function.
That lemma is independent of the coupled value theorem's cell counts;
the present proof uses no cell-count interface or cell algorithm.

Choose, once from base data,

```
B>=max(2,B_0),   log B=poly_d(I),
g_0=sigma/(2kB),
M=least power of two >=max(2,2C_gB).                     (6)
```

It follows that

```
Pr(g<g_0) <= 1/B.                                       (7)
```

These quantities have polynomial base bit length. In particular, although
`g_0` can be very small numerically, its logarithm has polynomial binary
size. Equation (7) pays for a fallback if a later, independently valid
coordinate enclosure fails to become small. The evaluator never trusts
`g>=g_0` as a correctness premise.

## 3. A buffered convex sublevel set has a known relative ball

Given `epsilon=2^(-q)`, set

```
delta=min(epsilon/4, g_0 epsilon^2/(128k)),
zeta=epsilon/(8k).                                      (8)
```

Use the convex value interface to obtain a rational feasible incumbent
`y in P`, its objective `U=F_gamma(y)`, and a global interval of width
at most `delta`. Thus `0<=U-f*<=delta`. Define

```
K={x in P:F_gamma(x)<=U+delta}.                         (9)
```

It contains the incumbent and every global optimizer, is compact and
convex, and consists entirely of points of objective gap at most
`2delta`. The buffer `delta` is essential to the following known-ball
construction; no quantitative relative-interiority promise for an
optimizer is required.

Use the exact rational affine-hull reduction from the convex interface:

```
x=x_0+A w,    w in R,                                   (10)
```

where `R` is a bounded full-dimensional rational polytope, zero is a
known relative-interior point, and known rational radii satisfy
`B(0,r_R) subset R subset B(0,R_R)`, with `r_R>0`. Their encoding
lengths are polynomial in `I`. Fixed zero-dimensional cases were already
handled. Put `psi(w)=F_gamma(x_0+A w)` and write `w_y` for the incumbent.
Choose a rational coefficient bound on a box containing `R`:

```
W>=max(1,sup_R |psi|).                                  (11)
```

Its bit length is polynomial in `I+b`; fixed degree keeps polynomial
expansion under affine substitution within that bound. Let

```
lambda=min(1/2,delta/(8W)),
c=(1-lambda)w_y,
r=lambda r_R.                                          (12)
```

Convexity and `|psi(0)|,|psi(w_y)|<=W` give

```
psi(c) <= (1-lambda)U+lambda psi(0)
       <= U+2W lambda <= U+delta/4.                     (13)
```

More generally, the entire homothetic copy
`(1-lambda)w_y+lambda R` lies in the sublevel set: for every `u in R`,
convexity gives
`psi((1-lambda)w_y+lambda u)<=U+2W lambda<=U+delta/4`.
That copy contains `B(c,lambda r_R)`. Hence the reduced sublevel set
`K_w` contains `B(c,r)`. It lies in `B(c,2R_R)`. Both radii, center, and threshold
have polynomial encoding length in `I+b+q`.

A separation oracle for `K_w` first checks the linear rows of `R`.
At a point within `R` but above the sublevel threshold, the rational
tangent inequality to `psi` separates it from `K_w`. Convexity is
needed only on `R`, and all gradients are exactly rational at rational
queries. Thus the verified rational weak-optimization theorem applies
after translating the known center `c` to the origin. No exact solution
of a nonlinear feasibility problem has been assumed.

## 4. Certified coordinate bounds from weak, possibly infeasible output

For each selected original coordinate, (10) writes

```
v_i=b_i+a_i'w.
```

Let `A_i>=||a_i||_2` be a rational bound, for example its one-norm.
Both `v_i` and `-v_i` have range width at most one on `K_w`, since
`K subset P` and `v_i in [0,1]`. Their affine constant terms can be
added after linear weak optimization.

Consider either affine objective `p(w)`. Write `p*` for its maximum on
`K_w`, and let `w*` be a maximizer. For `0<eta<=r/2`, the homothetic point

```
w_eta=(1-eta/r)w*+(eta/r)c
```

belongs to the eroded body `S(K_w,-eta)`. Its objective is at least
`p*-(eta/r)`, because the feasible objective range has width at most one.
The exact [GLS weak-optimization contract](convex-patch-evaluation.md)
returns rational `w_hat` in `S(K_w,eta)` satisfying

```
p(w_hat) >= p*-eta(1+1/r).                              (14)
```

The alternative empty-eroded-body outcome is impossible because the
known radius-`r` ball exists and `eta<=r/2`. Near-feasibility supplies
some `bar w in K_w` at Euclidean distance at most `eta`, so

```
p(w_hat) <= p*+A_i eta.                                (15)
```

There is no need to compute `bar w` or repair `w_hat`: only a bound on
the scalar extremum is used. Equations (14)--(15) prove that

```
p* <= p(w_hat)+eta(1+1/r)
   <= p*+eta(A_i+1+1/r).                                (16)
```

Choose the rational precision

```
eta_i=min(r/2,zeta/(A_i+1+1/r)).                        (17)
```

Maximizing `v_i` produces a certified upper bound `u_i` with
`max_K v_i<=u_i<=max_K v_i+zeta`. Maximizing `-v_i` and negating its
upper bound gives `l_i` with
`min_K v_i-zeta<=l_i<=min_K v_i`. Intersecting these intervals with
`[0,1]` preserves them. There are exactly `2k` convex weak-optimization
calls, each of polynomial bit cost in `I+b+q`. No enumeration exponential
in `k` occurs.

The rational hull `H=prod_i[l_i,u_i]` contains the incumbent core and
every optimal core. Thus the exact test

```
sum_i (u_i-l_i)^2 <= epsilon^2                          (18)
```

certifies the desired distance in (2) for that incumbent, independently
of any growth claim. If it passes, return `y` and its previously
certified value interval. That interval has width at most
`delta<=epsilon/4`. All output feasibility comes from `y`, not from a
possibly infeasible weak-optimization point.

The coordinate-bound record may include the rational weak-optimization
transcripts with their exact separation queries, the verified inner
ball, and the homothety/error calculations. Replaying the deterministic
Turing algorithm and its rational separation oracle verifies (16).
This is a polynomial verification record, not a claim that every
coordinate bound has a short rational first-order KKT certificate.

## 5. Failure is one small-growth event at every precision

Suppose `g>=g_0`. The core optimizer is unique, unless the projected
domain is already a singleton, which is even simpler. Every point of
`K` has objective gap at most `2delta`, so its core lies within

```
sqrt(2delta/g_0) <= epsilon/(8sqrt(k))                   (19)
```

of the optimal core. Its coordinate range is therefore at most
`epsilon/(4sqrt(k))`. By the certified extrema errors, the width of
each interval in `H` is at most

```
epsilon/(4sqrt(k))+2zeta
 <= epsilon/(2sqrt(k)).                                (20)
```

Consequently `diam_2(H)<=epsilon/2`, and (18) passes. Failure at any
precision implies the same event `g<g_0`. This implication is uniform
over all permissible convex value and weak-optimization answers.
There is no union over requested accuracies.

If (18) fails, use the exact core-first lex fallback on this same
sampled instance. Refine its selected coordinates to max-norm error
`tau=min(epsilon/(4(k+1)),epsilon/(4G_0))`, where
`G_0>=max(1,sup_P||grad F_gamma||_1)` is a polynomial-bit bound. Find
a rational feasible point in the intersection of `P` and the
radius-`tau` coordinate box about that approximation. The selected
exact optimizer proves the intersection nonempty. Any such LP output
is within `2tau` in max norm of the selected point. Its core distance
is at most `epsilon` and objective gap at most `epsilon/2`.
Refine the exact optimal-value enclosure to width `epsilon/2` for
the other half of (2). This is precisely the reviewed polytope
fallback repair with an additional polynomial-bit core tolerance.

Ordinary work, including all `2k` extrema, has a fixed polynomial bound
`P_d(I+b+q)`. Equation (6) makes `b=poly_d(I)`. Enlarging that polynomial
to absorb the fallback's precision exponent gives the pathwise bound

```
[1+B_0 1_{g<g_0}] P_d(I+q).                            (21)
```

It holds simultaneously for every query. By (7) and `B>=B_0`, its
random factor has expectation at most two. This proves (3), including
expected trace and output lengths. On rare draws the exact expanded
representation can be large, as allowed by the fallback budget.
Caching it is optional and does not affect selector consistency.

## 6. Meaning and limitations

Global convexity already makes objective-gap approximation efficient.
The additional conclusion is certified coordinate distance to one fixed
global optimizer's selected projection, on one finite sampled objective
and at every requested precision. It holds even when the unperturbed
residual optimizer set has positive dimension and the objective has no
useful numerical growth modulus supplied to the algorithm.

Only the perturbed coordinates receive this guarantee. Selecting every
coordinate therefore changes the noise model to full independent
perturbations; it does not obtain unperturbed residual coordinates from
core-only noise. The theorem is compatible with the reviewed
[PosSLP point comparison](posslp-convex-point-extraction.md), which
encodes the difficult coordinate in an unperturbed residual. It does
not solve the original deterministic instance or claim polynomial-size
expanded algebraic output.

The ingredients are classical convex sublevel optimization and the
reviewed compact-domain growth/fallback interfaces. The proposed
advance is their combination into an ordinary-polynomial, every-draw
correct, fixed-finite-law coordinate Cauchy guarantee, with sound
coordinate certificates on ordinary draws. The
[completed prior comparison](../prior-art/joint-convex-core-point-oracle-prior.md)
credits standard convex value optimization, low-dimensional polynomial
perturbation algorithms, and qualitative tilt results. It distinguishes
the selected-coordinate output and fixed finite law without claiming
publication priority.

## Verification status

The fresh independent review passed the relative inner-ball construction,
GLS coordinate extrema bounds, diameter constants, fixed selector, and
common event budget. It also checked the actual primary GLS definition's
arbitrary-rational-objective precision convention. The distinct exact
diagnostic
`python3 -B research-20261002/new-direction/check_joint_convex_core_hull.py`
passed 36 fixtures, 108 sublevel-ball points, 216 weak-extremum enclosures,
and 36 certified core hulls. It includes five selected coordinates,
100-bit thin diagonal polytopes, 40-bit accuracy requests, and slightly
infeasible weak outputs. It is not a general GLS implementation or a
test of the algebraic fallback. Existing value and fallback diagnostics
were not duplicated.

A targeted inline Python check passed local links, mathematical
delimiters, fences, whitespace, control characters, and checker syntax;
a scoped `git diff --check` also passed. No index edits, project-wide
tests, CI inspection, or external source searches were performed.
