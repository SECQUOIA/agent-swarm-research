# Hidden hyperplane convexity does not imply finite quadratic aggregation

Date: 2026-09-22. Status: complete mathematical proof, two independent
adversarial reviews, targeted exact witness checks, and Lean verification
of the scope specified below. Internal reviews are not external peer review;
the Lean checks are separate evidence. Priority remains qualified.

This construction answers the mathematical assertion of Conjecture 3.1 in
the inspected arXiv v2 of Blekherman–Dey–Sun's work, published in 2024:
hidden hyperplane convexity can hold although no
finite family of good quadratic aggregations describes the convex hull.
The example needs only three inequalities in four variables. Every ray in a
continuum is indispensable for an exact **strict** aggregation description.
The closed hull also needs infinitely many good aggregations, although a
countable dense family suffices there.

The contribution is this conjunction of hidden hyperplane convexity and
infinite necessity. SDP hull exactness for the higher-dimensional versions
already follows from quadratic matrix programming results. Neither the
existence of an SDP formulation nor infinite aggregation in other models is
claimed new. The sources examined and the precise distinctions appear below.

The [Lean package](../formal/topics/29-infinite-aggregation/README.md)
verifies the construction for every `r≥2`, including actual HHC, spectral
classification of good multipliers, indispensable strict rays and their
uncountability, and the obstruction to finite weak good-aggregation
descriptions of `cl conv(S)`. All 12 frozen claims are covered by 18 modules.
The warning-free targeted build, 248-declaration axiom audit, and all module
kernel replays passed; independent reviews found no unresolved issue.
The [verification record](../formal/topics/29-infinite-aggregation/VERIFICATION.md)
and [paper supplement](../paper-quadratic-aggregation/formal-infinite-aggregation.tex)
record the results.

The subsequent [exact-hull package](../formal/topics/30-infinite-aggregation-hull/README.md)
adds the strict and closed hull formulas, actual PD/PSD lifts, equality with
the hull of the original weak system, and both all-good intersection
identities. Its direct two-point proof works for every `r≥2` and does not
require the external general BDS hull theorem. Countable weak sufficiency,
the obstruction to arbitrary quadratic descriptions and literature-priority
claims remain outside these two formal packages. The separately completed
[accuracy package](../formal/topics/31-aggregation-accuracy/README.md) verifies
the explicit finite-aggregation error bounds and rational coefficient sizes;
it excludes the single-objective proposition from the broader accuracy note.

## 1. Statement and relevance

Let `r>=2`, let `u,v in R^r`, and define

```
f1 = ||u||²-1,    f2 = ||v||²-1,    f3 = 1/2-u·v,
S = {(u,v): f1<0, f2<0, f3<0}.
```

For a nonzero `lambda>=0`, set `f_lambda=sum_i lambda_i f_i` and let
`Q_lambda` be its homogeneous matrix in `(u,v,t)`. Following BDS, an
aggregation is **good** if `Q_lambda` has at most one negative eigenvalue
and `conv(S) subset {f_lambda<0}`. Hidden hyperplane convexity (HHC) means
that the image of every linear hyperplane under
`f^h=(||u||²-t², ||v||²-t², t²/2-u·v)` is convex.

**Theorem 1.** The set `S` is nonempty and bounded, and `f^h` has HHC.
Its good multipliers are exactly

```
K \ {0},    K={lambda>=0: lambda3²<=4 lambda1 lambda2}.
```

Every exact representation of `conv(S)` as an intersection of strict good
aggregations contains the ray `(tau,1/tau,2)` for every `tau in [1,2]`.
Consequently it requires uncountably many rays.

No finite list of their non-strict versions describes `cl conv(S)`.
In fact, `conv(S)` has no description by a finite conjunction of strict
quadratic inequalities in the original variables, even if those quadratics
are not aggregations.

Thus complete aggregation theory does not guarantee a finite original-space
quadratic formulation, even for a bounded, low-dimensional system. This
explains a concrete limitation of precomputing a finite list of aggregated
quadratic cuts. It does not rule out efficient separation or compact lifted
formulations; Section 5 gives such an SDP representation. No general lower
bound on solver runtime follows.

## 2. Hidden hyperplane convexity in four variables

The proof uses only two by two positive semidefinite matrices. Write
`U=[u v] in R^(r by 2)` and express an arbitrary homogeneous hyperplane as

```
tr(P^T U)+s t=0,    P in R^(r by 2), s in R.
```

Put `G=U^T U`, `T=t²`, and `H=P^T P`. For fixed `G>=0`, the range of
`tr(P^T U)` over `U^T U=G` is the full interval `[-M(G),M(G)]`, where

```
M(G)=||P G^(1/2)||_* ,
M(G)²=tr(HG)+2 sqrt(det(H) det(G)).                         (1)
```

Here `||.||_*` denotes the sum of singular values. To verify the range,
write `U=Q G^(1/2)` with `Q^TQ=I_2`; singular `G` is covered by extending
an orthonormal basis. Singular value decomposition gives the stated maximum.
Starting with a maximizing `Q`, rotate its two columns continuously by a
planar rotation from `I_2` to `-I_2`. The Gram matrix remains `G`, and the
linear functional moves continuously from its maximum to its negative.
This argument works at `r=2` despite the disconnectedness of the full
orthogonal group. Formula (1) follows by expanding the square of the sum
of the two singular values.

It follows that the pairs `(G,T)` attained on the hyperplane are exactly

```
G>=0,    T>=0,    s² T <= tr(HG)+2 sqrt(det(H) det(G)).       (2)
```

The right side is concave in `G`. For completeness,

```
sqrt(det G)=inf {tr(ZG)/2: Z>0, det Z=1}                    (3)
```

is concave as an infimum of linear functions. For positive definite `G`,
AM–GM proves the lower bound in (3) and
`Z=sqrt(det G) G^(-1)` attains it. For singular `G`, diagonalization and
determinant-one diagonal matrices approaching the boundary give infimum
zero. Thus (2) is convex, including when `H` is singular or `s=0`.

The image of the hyperplane under `f^h` is the linear image

```
(G,T) -> (G11-T, G22-T, T/2-G12)
```

of (2), and is therefore convex. This proves HHC for every `r>=2`.
Nonemptiness follows from `u=v=sqrt(3/4)e1`; boundedness follows from the
two unit-ball constraints.

## 3. Good aggregations and their indispensable rays

Up to a permutation of coordinates,

```
Q_lambda = ([[lambda1,-lambda3/2],[-lambda3/2,lambda2]] tensor I_r)
             direct_sum [lambda3/2-lambda1-lambda2].       (4)
```

A negative eigenvalue of the two by two block repeats `r>=2` times,
violating permissibility. Otherwise the block is PSD, exactly when
`lambda3²<=4lambda1lambda2`. For such a nonzero nonnegative multiplier,

```
lambda3<=2sqrt(lambda1lambda2)<=lambda1+lambda2,
lambda3/2-lambda1-lambda2<0.
```

There is exactly one negative eigenvalue in (4). Moreover `f_lambda` is
convex and strictly negative on `S`, hence strictly negative on every
finite convex combination of points of `S`. This proves the claimed
description of the good cone.

For `tau in [1,2]`, set `epsilon=1/10` and choose `u_tau,v_tau` with Gram
matrix

```
G_tau = [[1-epsilon/tau, 2/5],
         [2/5, 1-epsilon*tau]].                           (5)
```

Both diagonal entries are at least `4/5`, and the determinant is at least
`12/25`, so these vectors exist in `R²` and can be embedded in `R^r`.
At `x_tau=(u_tau,v_tau)`,

```
f(x_tau)=epsilon(-1/tau,-tau,1),
f_lambda(x_tau)=epsilon(-lambda1/tau-lambda2*tau+lambda3)<=0. (6)
```

Weighted AM–GM and membership in `K` show that equality in (6) holds
precisely when `lambda` is a positive multiple of `(tau,1/tau,2)`.
That aggregation is strictly negative throughout `conv(S)`, so `x_tau`
is outside the ordinary hull. All other good aggregations are strictly
satisfied there. An exact strict description must therefore include that
specific ray for every `tau`. This proves the uncountability statement.

The distinction between ordinary and closed hulls matters. To prove the
closed statement, start with any finite good family and choose an omitted
ray. All family members have strictly negative slack at `x_tau`. Reduce
the off-diagonal entry `2/5` of (5) by a sufficiently small `eta>0`, leaving
the diagonals fixed. The Gram matrix stays positive definite. Every member
of the finite family stays strictly negative by continuity, but the omitted
aggregation becomes `2eta>0`. It is nonpositive on `cl conv(S)`, so the
perturbed point is outside that closed hull. This proves finite impossibility
there without relying on strict inequalities.

A countable dense set of positive `tau`, together with the coordinate rays,
does suffice for the closed hull. Continuity in `tau` extends its non-strict
inequalities to all `tau>0`. With `p,q>=0`, the infimum of `tau p+q/tau`
is `2sqrt(pq)`, including the endpoint cases `p=0` or `q=0`, where a limit
may be required. The resulting inequality is exactly the closed condition
in Section 5. This limit argument is not valid for an exact strict hull.

## 4. Hull formula and arbitrary quadratic descriptions

The exact ordinary-hull formula below now has a direct Lean-verified proof
for every `r≥2`. The preceding HHC proof and BDS Theorem 2.9 in arXiv v2
(Theorem 2.8 in the older author PDF) give an alternative mathematical
route, because `2r>=4` and the hull is nonempty and proper. The formal
proof does not depend on that external theorem. The two coordinate extreme
rays of `K` enforce
`p=1-||u||²>0`, `q=1-||v||²>0`. Its other extreme rays are
`(tau,1/tau,2)`, `tau>0`. Their inequalities are

```
tau p+q/tau > 2(1/2-u·v),    for every tau>0.
```

The left side attains its minimum `2sqrt(pq)`. Therefore

```
conv(S)={||u||²<1, ||v||²<1,
          u·v+sqrt((1-||u||²)(1-||v||²))>1/2}.             (7)
```

A direct two-point proof of sufficiency works already for `r>=2`. Put
`a=sqrt(p)`, `b=sqrt(q)`, and choose a unit vector `e` perpendicular to
`b u-a v`. Then `u·e/a=v·e/b=h`. Choose

```
max(0,(1/2-u·v)/(ab)) < k < 1,
t_-=-h-sqrt(h²+k),   t_+=-h+sqrt(h²+k).
```

The roots have opposite signs and satisfy `2h t+t²=k`. For each root
`t∈{t_-,t_+}`, at `x(t)=(u+t a e,v+t b e)` the squared norms increase by `p k` and `q k`,
and the inner product increases by `ab k`. Both `x(t_-)` and `x(t_+)`
therefore lie in `S`. Their convex combination with weights
`t_+/(t_+-t_-)` and `-t_-/(t_+-t_-)` is the original point. This argument
only requires a perpendicular to one weighted difference, so it includes
the four-variable case. The formalization proves the endpoints and weights
explicitly; no hull-description theorem is assumed as a premise.

On the plane `u=x e1,v=y e2`, formula (7) becomes

```
x²<1, y²<1, (1-x²)(1-y²)>1/4.                            (8)
```

The polynomial `P=(1-x²)(1-y²)-1/4` is irreducible over `R[x,y]`:
over `R(x)`, its root equation is
`y²=(3/4-x²)/(1-x²)`, a rational function with distinct simple zeros
and poles, hence not a square. The polynomial is primitive over `R[x]`,
so Gauss's lemma applies.

Suppose finitely many strict quadratic inequalities describe the ordinary
hull. Their restrictions to this plane are nonzero, since the origin lies
in the hull and all their values there must be strictly negative. At every
point of a compact boundary subarc of (8), some restricted quadratic
must vanish: continuity gives nonpositive values, and simultaneous strict
negativity would incorrectly include that boundary point. A finite family
of polynomial zero sets cannot cover this analytic arc unless one vanishes
on a subarc. Irreducibility would then force its divisibility by the quartic
`P`, impossible for a nonzero quadratic. This establishes the stronger
original-space obstruction. No claim about arbitrary Boolean formulas or
lifted formulations is needed.

## 5. A finite lifted formulation and what remains tractable

The closed hull has the affine semidefinite representation

```
exists sigma>=1/2:
  [[1, sigma, u^T],
   [sigma, 1, v^T],
   [u, v, I_r]] >= 0.                                  (9)
```

The Schur complement says that `p,q>=0` and
`|sigma-u·v|<=sqrt(pq)`. A `sigma>=1/2` exists exactly when
`u·v+sqrt(pq)>=1/2`. This is the closure of (7): the set in (9) is
convex, and mixing any of its points with the origin makes the matrix
positive definite for mixture weight strictly between zero and one
(use `sigma=1/2` at the origin). Thus the mixture lies in (7) and tends
to the original point.

Likewise (7) uses a strict positive-definite version of (9) with
`sigma>1/2`. The closed formulation also equals the hull of the original
closed system: that system is compact, contains `S`, and is contained in
(9). Its compact convex hull therefore lies between `cl conv(S)` and (9),
which have just been shown equal.

Thus the obstruction concerns finite original-space quadratics, not an
intrinsically difficult convex hull. A solver can enforce the full closed
family using one small SDP lift. Whether such a lift is worthwhile inside
MINLP requires computational work; no speedup is established here.

PDLC of the homogeneous matrices fails. For an arbitrary signed multiplier,
positive definiteness of the two by two block in (4) requires
`lambda1+lambda2>|lambda3|`, while positivity of its scalar block requires
`lambda3/2>lambda1+lambda2`. These conditions are incompatible. The example
does not contradict finiteness results that assume PDLC.

### Quantitative finite approximation

The [reviewed accuracy analysis](../notes/research-20260922-aggregation-accuracy.md)
shows that the smallest Hausdorff error achievable by at most `N` good
closed quadratic aggregations is `Theta(N^-2)`, with constants independent
of `r>=2`. This includes arbitrary interior multipliers. Rational
multiplier meshes achieve the rate with `O(log N)` bits per coefficient.
By contrast, each fixed linear objective has an objective-dependent
single good aggregation attaining its exact optimum. Thus uniform finite
representation has a quantitative cost, but this is not a cut-iteration
lower bound for solving one objective. The approximation exponent and
single-objective duality principle are classical; the contribution here
is their precise consequence for this construction.

The [Lean accuracy package](../formal/topics/31-aggregation-accuracy/README.md)
now verifies the uniform error bounds and exact rational construction,
including arbitrary interior good cuts and every `r≥2`. Its finite-grid
proof gives a slightly stronger lower constant and implies the displayed
source bound. The single-objective statement in this paragraph remains
outside that formal package.

## 6. Closest prior results and novelty limits

- **Blekherman, Dey, Sun (published 2024),**
  [Aggregations of quadratic inequalities and hidden hyperplane convexity](https://arxiv.org/html/2210.01722v2),
  arXiv v2, Definition 2.1, Theorem 2.9, and Conjecture 3.1: HHC implies the good
  aggregation hull description; the conjecture asks whether infinitely many
  can be necessary. Theorem 1 supplies an explicit instance. Their
  finite-description results require additional definiteness assumptions.
  The older author PDF numbers the hull theorem 2.8. The journal full text
  was not retrieved; conjecture wording and numbering here refer to the
  inspected preprint versions.
- **Wang, Kılınç-Karzan (2024),**
  [On semidefinite descriptions for convex hulls of quadratic programs](https://arxiv.org/html/2403.04752v2),
  v2 Section 4.1 (also v1 Appendix B.2): quadratic matrix programming and eigenvalue
  multiplicity give closed SDP hull exactness. Their result covers this
  three-constraint system at replication `r>=3`. The inspected theorem does
  not assert HHC or finite quadratic impossibility. Formula (9) is not
  presented as a new SDP convexification principle.
- **Brun, Sun, Watson (2026),**
  [Modeling Adversarial Wildfires for Power Grid Disruption](https://optimization-online.org/wp-content/uploads/2026/03/AdversarialWildfire.pdf),
  Section 3.2: derives the SDP hull of an inner-product hypograph over two
  balls using the preceding theory. This gives an important application
  context. Convexifying a hypograph and then fixing its level need not give
  the fixed-level hull automatically; the results should not be conflated.
- **Blekherman, Dunbar (2025),**
  [A Topological Approach to Simple Descriptions of Convex Hulls of Sets Defined by Three Quadrics](https://epubs.siam.org/eprint/VRNXYR5GPAAPTF5RJHV3/full),
  Theorem 1.4: a four-aggregation result under PDLC and stated regularity and
  infinity conditions. It does not apply here. The published statement was
  inspected; a search excerpt suggesting a stronger thesis theorem was not
  verified in full and is not used.
- **Dey, Muñoz, Serrano (2022),** *On obtaining the convex hull of quadratic
  inequalities via aggregations*, Proposition 2.8: an earlier infinite-
  aggregation example does not satisfy HHC, and its required aggregations
  need not obey the good-family inertia restriction. See the explicit
  source comparison and HHC counterexample in the novelty review below.
- **Dey, Han, Wang (2026),**
  [Aggregation of Bilinear Bipartite Equality Constraints and its Application to Structural Model Updating Problem](https://link.springer.com/article/10.1007/s10898-026-01607-8):
  infinite aggregation can be required in a different architecture, involving
  boxed bilinear equalities and convexification after aggregation. This is
  not the HHC/direct-good-inequality question addressed here.

Searches covered the conjecture itself and equivalent terminology involving
quadratic matrix programming, joint numerical ranges, ball inner-product
hulls, and infinite aggregation. No examined source resolved this conjunction
already. An unsuccessful search does not establish priority. The possible
contribution should be stated as the explicit construction and its
finite-description consequences, with the classical ingredients credited.

## 7. Verification and development record

- [Author investigation](../notes/research-20260922-aggregation-frontier.md):
  independent covariance-completion proof at `r>=6`, multiplier cone, and
  exact witnesses.
- [Proof review](../notes/review-20260922-infinite-aggregation.md):
  independently verified that proof and supplied the stronger `r>=2`
  argument used here.
- [Novelty and second proof review](../notes/review-20260922-aggregation-novelty.md):
  source comparisons and an independent recheck of the `r>=2` argument.
- [Fresh integrated review](../notes/review-20260922-final-aggregation.md):
  rechecked the complete result, closed-hull arguments, and source versions.
- `python3 code/research_20260922/check_infinite_aggregation.py` passed
  2,601 exact rational ray identities and six finite-family outside
  witnesses. It works with Gram matrices, avoiding numerical square roots.
  These checks test the witness formulas, not HHC, irreducibility, or novelty.
  The archived output is from the manuscript supplement's version of this
  checker (`paper-quadratic-aggregation/supplement/check_infinite_aggregation.py`,
  same checks with added assertions):
  [`exact-checks.log`](../paper-quadratic-aggregation/build/stage07/exact-checks.log).

The earlier mathematical review separately re-derived HHC, the multiplier
cone, the hull formula, and the boundary obstruction. Subsequent Lean
packages 29 and 30 verified the exact scopes listed at the top of this
note. Their targeted builds, axiom audits, kernel replays and independent
semantic reviews are recorded separately; the arbitrary-quadratic boundary
obstruction remains outside them. No project-wide verification or CI
inspection was run for these packages. The quantitative follow-up is linked
above. A further useful question is recognition of structures where a
small lifted cone should replace aggregation cuts.
