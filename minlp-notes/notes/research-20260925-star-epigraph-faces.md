# A limit on face-based lower bounds for quadratic indicator stars

Date: 2026-09-25. Status: proved research note with
[independent adversarial review](review-20260925-star-epigraph-faces.md).
This is a modest structural observation, not a compact hull formulation or
an extension-complexity lower bound for the full hull. Publication priority
has not been established.

The earlier [frontier note](research-20260922-frontier-scout.md) embeds a
correlation polytope as a face of the inverse-principal polytope of a
well-conditioned positive-definite star. That result does not transfer to
the original quadratic epigraph by projection. This note gives an additional
reason a direct face transfer is difficult: every exposed face of the
original hull whose exposing objective gives the epigraph variable positive
weight has a polynomial-size linear extended formulation. A general face
containment argument then gives the same bound for every bounded face,
including faces that are not exposed.

## Model and statement

Let `n` be the number of leaves and let

```
Q = [a  b^T     ],    d_i > 0,    a > sum_i b_i^2/d_i.
    [b  Diag(d) ]
```

Zero entries in `b` are allowed. Thus the support graph is a star together
with any isolated leaves, and `Q` is positive definite. Define

```
H_Q = cl conv{(z,x,t): z in {0,1}^{n+1},
                       x_i=0 whenever z_i=0, t >= x^T Q x}.
```

There are no additional constraints on `x` or `z`. For arbitrary real
vectors `c,delta`, consider the exposed face minimizing

```
L(z,x,t) = t - 2 c^T x + delta^T z.
```

This covers every exposing objective with a positive coefficient on `t`
after scaling and changing notation.

**Proposition.** This exposed face is the convex hull of at most `2n+2`
affine images of cubes `[0,1]^k`, each with `k<=n`. Consequently it has a
linear extended formulation with at most `(2n+2)(2n+1)` scalar inequalities,
apart from affine equalities. The formulation uses `O(n^2)` variables and
`O(n)` affine equations. This counts scalar inequalities, not merely the
number of disjuncts. It is a bounded polytope.

The cube dimension bound includes the root-off branch as a separate cube;
it does not count a free root indicator inside the same cube.

## Proof

First justify that taking the closed hull introduces no extra minimizers.
This step works for every positive-definite `Q`. For each binary support
`z`, let `x^z` be the unique minimizer of
`x^T Q x - 2 c^T x` on that support. Put

```
m_z = (x^z)^T Q x^z - 2 c^T x^z + delta^T z,
m = min_z m_z,
p_z = (z,x^z,(x^z)^T Q x^z).
```

For every original feasible point with support `z`, stationarity on the
active coordinates gives the exact identity

```
L(z,x,t)-m = (m_z-m) + (x-x^z)^T Q(x-x^z) + (t-x^T Q x).
```

All terms on the right are nonnegative. Consider convex combinations of
original feasible points converging to a point in `H_Q` with objective
value `m`. The average of each term tends to zero. Since there are finitely
many supports, the total weight on supports with `m_z>m` tends to zero.
If `mu=lambda_min(Q)>0`, the norm of the average displacement
`x-x^z` is at most `sqrt((L-m)/mu)` by Cauchy--Schwarz. Therefore the
limiting `(z,x)` lies in the convex hull of the corresponding coordinates
of the finitely many `p_z` with `m_z=m`. The equation `L=m` determines `t`
affinely from `(z,x)`. This proves that the exposed face is exactly
`conv{p_z:m_z=m}`.

Now fix `z_0=1` and `x_0=r`. A leaf can be inactive at cost zero or active
at its unique continuous minimizer

```
x_i = (c_i-b_i r)/d_i,
A_i(r) = delta_i-(c_i-b_i r)^2/d_i.
```

After minimizing all leaves, the objective is the scalar function

```
phi(r) = a r^2 - 2 c_0 r + delta_0 + sum_i min{0,A_i(r)}.
```

Ignore polynomials `A_i` that vanish identically. The others have at most
`2n` distinct real roots in total. Their roots partition the real line into
at most `2n+1` intervals. On each closed interval, the sign pattern is
fixed in its interior, and continuity extends its quadratic formula to the
endpoints. If `S` indexes the active leaf terms in that formula, its
quadratic coefficient is

```
a - sum_(i in S) b_i^2/d_i > 0.
```

Thus `phi` is strictly convex on each interval. No interval can contain two
global minimizers: the value at their midpoint would be smaller. Every
global minimizer lies in at least one of these closed intervals, so there
are at most `2n+1` minimizing values of `r`. The function is coercive, since
all of its finitely many pieces have positive leading coefficient.

At any minimizing `r`, the leaves with `A_i(r)<0` must be active, those with
`A_i(r)>0` must be inactive, and leaves with `A_i(r)=0` can be chosen
independently. In the original minimizer points,

```
z_0=1, x_0=r, x_i=z_i(c_i-b_i r)/d_i,
t=m+2c^T x-delta^T z.
```

These are affine functions of the free tied indicators. The convex hull
of all choices at this `r` is an affine image of a cube. Include this cube
only if the root-active optimal value is the global value `m`.

If `z_0=0`, then `x_0=0`. The leaves separate in the same way, with
`A_i(0)=delta_i-c_i^2/d_i`. The convex hull of their minimizers is one more
affine cube.
Include it only if its optimal value equals `m`.

Finally, for cube images `u=v_j+T_j s`, `0<=s<=1`, use variables
`lambda_j>=0`, `0<=w_ji<=lambda_j`, and equations

```
sum_j lambda_j=1,
u=sum_j(lambda_j v_j+T_j w_j).
```

This is exactly the convex hull of their union. A cube with `k_j<=n`
uses `1+2k_j` inequalities. With at most `2n+2` cubes, the stated bound
follows. The images and their finite convex hull are compact. ∎

## Every bounded face has a small linear formulation

The next containment lemma works for every positive-definite `Q` in this
unconstrained indicator model, regardless of its graph.

**Lemma.** Every nonempty bounded face of `H_Q` is contained in an exposed
face whose exposing objective has a positive coefficient on `t`.

**Proof.** Let `F` be a nonempty bounded face and choose `u` in its relative
interior. Define the nonnegative affine function

```
p(z) = sum_(i:u_zi=0) z_i + sum_(i:u_zi=1) (1-z_i),
G = H_Q intersect {p(z)=0}.
```

Since `p>=0` and `p(u)=0`, the relative-interior condition gives `F subset G`.
The face `G` is unbounded in the positive `t` direction. If `u` were in
the relative interior of `G`, the face property would imply `F=G`.
Therefore `u` lies in the relative boundary of the closed convex set `G`.
There is a linear objective `h` that is nonconstant on `aff(G)` and is
minimized over `G` at `u`.

Write `alpha` for the coefficient of `t` in `h`. The vertical ray rules
out `alpha<0`. If `alpha=0`, choose an allowed binary support with every
coordinate not fixed off in `G` active. Its continuous coordinates can
vary arbitrarily, so every corresponding continuous coefficient of `h`
must be zero. Coordinates fixed off have `x_i=0` throughout `G`: writing
`mu=lambda_min(Q)>0`, Cauchy--Schwarz gives the valid inequality
`x_i^2<=z_i t/mu` on every convex combination and hence on `H_Q`.
The remaining
objective depends only on the indicators. Their projection from `G` is
the entire coordinate cube fixed by `p=0`, and all its free coordinates
are strictly between zero and one at `u`. Thus a minimizing linear
indicator objective is constant on that cube. This makes `h` constant
on `G`, a contradiction. Hence `alpha>0`; normalize it to one.

For each binary support `z`, let `m_z` be the minimum of `h` on its
quadratic epigraph. Every `m_z` is finite by positive definiteness.
Let `m_allowed=min{m_z:p(z)=0}`. Because there are finitely many supports,
choose a finite nonnegative `M` such that

```
m_z + M p(z) >= m_allowed                 for every binary z.
```

The inequality `h+Mp>=m_allowed` is valid on the original union and hence
on its closed convex hull. On `G`, it is `h>=m_allowed`. An allowed
support attains `m_allowed`, so `min_G h=m_allowed=h(u)`. Therefore
`h+Mp` exposes a positive-`t` face of `H_Q` containing `u`, and hence
containing `F`. ∎

**Corollary.** For a star with `n` leaves, every nonempty bounded face of
`H_Q` is a polytope with a linear extended formulation of at most
`(2n+2)(2n+1)` inequalities, apart from affine equalities.

Indeed, the lemma puts the face inside the polytope supplied by the
proposition. It remains a face of that polytope. Taking a polytope face
adds affine equalities to its extended formulation and no inequalities.

## Degeneracy and a sharper description for connected stars

Suppose `b_i!=0`. At a root of `A_i` with `delta_i>0`, the function
`min{0,A_i}` has a strictly downward jump in its one-sided derivative.
All simultaneous switching leaves contribute downward jumps, so their
sum has a strictly downward jump as well. A local minimum of a continuous
function with one-sided derivatives requires the left derivative to be
nonpositive and the right derivative to be nonnegative. A strict downward
jump cannot meet both conditions.

Therefore, at a minimizing root value, a tied connected leaf necessarily
has `delta_i=0` and `c_i-b_i r=0`. Its continuous coordinate is zero for
both indicator choices. For a connected star, each root-active cube varies
only redundant indicators of zero coordinates; its `(x,t)` coordinates
are constant. The root-off cube can still vary nonzero continuous leaf
coordinates. If `b_i=0`, a constant identity
`delta_i=c_i^2/d_i` permits a tied leaf with nonzero continuous coordinate
even in a root-active cube. The general proposition includes this case.

The number of distinct root-active continuous points can exceed `n+1`.
For a rational example with two leaves, take

```
a=9/4, b=(1,1), d=(1,1), c=(0,-2,1), delta=(0,36/5,9/5).
```

The Schur complement is `1/4>0`. The four root-active support quadratics,
for no leaves, only leaf 1, only leaf 2, and both leaves, respectively, are

```
(9/4)r^2, (5/4)(r-8/5)^2, (5/4)(r+4/5)^2, (1/4)(r-4)^2.
```

All have minimum zero, at four distinct root values. The root-off minimum
is also zero. Thus bounding the number of root-active minima by `n+1`
would already fail for two leaves.

## What this does and does not rule out

An affine image of any bounded face also has an `O(n^2)` linear extended
formulation. Consequently a correlation-polytope lower bound cannot
transfer through a bounded face when the star dimension is polynomial in
the correlation dimension: it would conflict with the known exponential
LP extension complexity of the correlation polytope. The precise prior
lower bound is [Fiorini, Massar, Pokutta, Tiwary and de Wolf,
Theorem 7](https://arxiv.org/html/1111.0837#S3.SS2):
`xc(COR(m)) >= 2^(C m)` for a positive constant `C`.
That theorem and the face/projection monotonicity in Lemma 9 were inspected.

The proposition says nothing about a single extended formulation that
represents all these faces simultaneously. The cube images depend on the
exposing objective. Small formulations for individual exposed faces do not
imply a small formulation for `H_Q` itself. Unbounded faces, arbitrary
affine sections, and other slack-matrix lower-bound constructions remain
outside the corollary. No SOCP or SDP lower bound for the original star
hull follows here.

Additional constraints on the indicators can destroy the independent
choices used in the proof. Positive definiteness is essential to this
argument's strict convexity and coercivity claims. No claim for arbitrary
trees, positive-semidefinite stars, or bounded continuous variables is made.

## Literature comparison and verification

[Bhathena, Fattahi, Gómez and Küçükyavuz,
*A parametric approach for solving convex quadratic optimization with
indicators over trees*](https://doi.org/10.1007/s10107-025-02222-3)
already prove a quadratic-time optimization algorithm on arbitrary trees.
The local full text was inspected, especially Lemma 2, Proposition 1,
and the piece-count recurrence leading to Theorem 2. Its scalar
piecewise-quadratic machinery is stronger algorithmically than the
elementary star calculation above. The candidate addition here is only
the explicit exposed-face decomposition and its implication for attempted
extension-complexity transfers. Whether this observation is already stated
elsewhere has not been established.

Additional focused searches used the combinations `"quadratic"
"indicators" "exposed face"`, `"quadratic" "indicators" "bounded
faces"`, and `"star" "indicators" "extension complexity"`. They did
not locate a matching statement; unrelated search results were discarded.
This limited unsuccessful search is not evidence of priority.

The [2026 decision-diagram paper by Choi et al.](https://arxiv.org/abs/2608.22815)
and its fixed-leaf tree formulation are compared in the frontier note.
The present proposition does not change that paper's formulation scope.

The focused command `python code/check_star_epigraph_faces.py` enumerates
rational principal-support minimizers and checks the affine-cube grouping,
the number of center/root groups, and the connected-leaf tie condition.
It includes random signed couplings, zero couplings, all-zero objectives,
constant nonzero tied leaves, and examples with two and four distinct
global center minimizers. It passed all 77 cases and 3,232 exact support
checks. These checks
test finite cases and exact algebra; they do not replace the proof or
establish novelty. No project-wide checks or CI inspection are involved.
