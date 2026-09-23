# Independent review: infinitely many quadratic aggregations

Date: 2026-09-22. Reviewed source:
[aggregation frontier draft](research-20260922-aggregation-frontier.md).

Verdict: no substantive error found in the draft's HHC construction for
`r >= 6`, its exact characterization of good aggregations, or its continuum
of witnesses excluding every finite subfamily. The result answers the
mathematical existence question in BDS Conjecture 3.1 as stated in the
examined source. Priority remains provisional. The semidefinite hull
description is closely related to established quadratic matrix programming
results and should not be presented as independently new.

This review independently reconstructs the essential arguments below. It
does not certify the arguments with Lean, and a favorable review is not a
substitute for further proof and novelty checks.

## Scope and assumptions

Use `0 < a < 1` and

```
S = {(u,v): ||u||² < 1, ||v||² < 1, u·v > a},
u,v in R^r.
```

The draft specializes to `a=1/2`. The ordinary convex hull, with no closure,
is intended. Every inequality in the aggregation representation is strict.
The BDS definition tests negative eigenvalues of the homogenized matrix,
not merely the quadratic block. This distinction has been checked.

## Audit of the draft's HHC proof

For the more general map
`phi_i(X,t)=tr(A_i XX^T)+c_i t²`, with `X` of size `k by r`, the draft fixes
an arbitrary hyperplane `<B,X>+beta*t=0`. The construction preserves the
entire pair `(XX^T,t²)` under convex combinations; hence it preserves every
listed quadratic form simultaneously.

The potentially delicate steps are valid:

- The covariance residual `D=W-ZZ^T` is PSD by the stated vector
  Cauchy--Schwarz inequality, including zero mixing weights.
- If the scalar second moment vanishes, the direct choice `Z=0,t=0`
  satisfies the hyperplane. It need not preserve a first moment.
- The common right kernel of `B,Z` has dimension at least `r-2k`.
  The assumption `r>=3k` provides `k` orthonormal rows in this kernel.
- With `Y=D^(1/2)U`, the required identities are
  `YY^T=D`, `ZY^T=0`, and `BY^T=0`. The last identity implies
  `<B,Y>=0` by taking the trace.

Thus the proof covers every homogeneous hyperplane, including `t=0`,
and establishes actual convexity of its image without a closure operation.

## Independent stronger HHC lemma for two columns

The following independent route shows that the particular three-form
example has HHC already when `r>=2`. It is not needed to validate the
draft's conservative dimension threshold.

Let `U=[u v]` and `P=[p q]` be `r by 2` matrices, and fix the hyperplane

```
tr(P^T U)+s t=0.
```

Write `G=U^T U`, `T=t²`, and `H=P^T P`. For each PSD `G`, the range of
`tr(P^T U)` over matrices with `U^TU=G` is precisely `[-M(G),M(G)]`, where

```
M(G) = nuclear_norm(P G^(1/2)),
M(G)² = tr(HG)+2 sqrt(det(H) det(G)).
```

To check the range assertion, write `U=QG^(1/2)` with `Q^TQ=I_2`.
Such a factorization is available also when `G` is singular, by extending
an orthonormal basis. The singular value decomposition gives the maximum
`M(G)`. Starting at a maximizing `Q`, replace it by `Q R(theta)`, where
`R(theta)` is a planar rotation from `I_2` to `-I_2`. The Gram matrix stays
fixed, and the linear functional varies continuously from `M(G)` to
`-M(G)`. It attains every intermediate value. This avoids any incorrect
assumption that the full orthogonal group is connected.

The pair `(G,T)` is therefore attainable on the hyperplane exactly when

```
G PSD,  T>=0,  s² T <= tr(HG)+2 sqrt(det(H)det(G)).
```

This set is convex. Indeed, `sqrt(det G)` is concave on the PSD cone of
order two. One elementary proof is the variational identity

```
sqrt(det G) = inf {tr(ZG)/2: Z positive definite, det Z=1}.
```

For positive definite `G`, the arithmetic--geometric mean inequality gives
the lower bound and the choice `Z=sqrt(det G)G^(-1)` gives equality.
For singular `G`, diagonalization and a sequence of determinant-one
diagonal matrices gives infimum zero. An infimum of linear functions is
concave. The displayed attainable-pair set is consequently a hypograph
of a concave function intersected with the PSD cone and `T>=0`.

Finally the quadratic-map output is the linear image

```
(G,T) -> (G11-T, G22-T, a*T-G12).
```

Every hyperplane image is convex. The proof handles `P=0`, `s=0`, and
singular `G` without exceptional assumptions.

## Direct ordinary hull formula for r >= 3

Put `A=1-||u||²`, `B=1-||v||²`, and `C=u·v`. Then

```
conv(S) = {A>0, B>0, a-C < sqrt(A B)}.
```

Necessity follows from the two ball constraints and all convex quadratic
aggregations

```
tau*(||u||²-1)+(||v||²-1)/tau+2*(a-u·v) < 0,
tau>0.
```

The left side has quadratic part `||sqrt(tau)u-v/sqrt(tau)||²`.
Minimizing `tau*A+B/tau` over `tau>0` gives `2 sqrt(AB)`, with the
minimum attained because `A,B>0`. Strictness at that minimum is essential.

For sufficiency, if `C>a`, the point is already in `S`. Otherwise choose
`0<eta<1` so that `eta² sqrt(AB)>a-C`. Since `r>=3`, there is a unit
vector `e` orthogonal to both `u,v`. The two points

```
(u + eta sqrt(A)e, v + eta sqrt(B)e),
(u - eta sqrt(A)e, v - eta sqrt(B)e)
```

have squared norms strictly below one and inner product
`C+eta²sqrt(AB)>a`. Their midpoint is `(u,v)`. This proof establishes the
ordinary hull by two feasible points and does not rely on a closure or on
the BDS aggregation theorem.

## Independent finite-aggregation obstruction

For `lambda>=0`, the homogeneous aggregation has matrix

```
([[lambda1,-lambda3/2],[-lambda3/2,lambda2]] tensor I_r)
  direct_sum [a lambda3-lambda1-lambda2].
```

If the two by two block has a negative eigenvalue, it occurs at least
`r>=2` times. Otherwise `lambda3<=2sqrt(lambda1 lambda2)` and, for
`lambda!=0`, the final scalar is strictly negative because `a<1`.
Convexity then guarantees strict validity throughout the ordinary hull.
Thus good multipliers are exactly the nonzero elements of
`{lambda>=0:lambda3²<=4lambda1lambda2}`.

An alternative to the draft's valid epsilon construction is, for
`|theta|<-log(a)`,

```
u_theta=sqrt(1-a exp(theta)) e1,
v_theta=sqrt(1-a exp(-theta)) e2.
```

At this point `A=a exp(theta)`, `B=a exp(-theta)`, and `C=0`.
Every good aggregation is nonpositive there, and equality holds only on
the multiplier ray satisfying

```
lambda3=2sqrt(lambda1lambda2),
lambda1/lambda2=exp(-2theta).
```

These rays are different for different `theta`. Each point fails its
corresponding strictly valid aggregation, so it is outside the hull.
A finite list omits one of these rays and is strictly satisfied at the
corresponding outside point. This is already a complete obstruction; no
irreducibility claim is necessary for BDS Conjecture 3.1.

The author subsequently observed a stronger cardinality conclusion, which
also follows from the equality calculation: an exact strict description
must contain the unique multiplier ray for every `theta` in the interval.
There must therefore be uncountably many rays. In particular, a countable
dense subfamily does not describe the ordinary hull: its omitted boundary
witnesses satisfy every selected inequality strictly. This strict-system
phenomenon must not be transferred to the closed hull, for which continuous
non-strict aggregation inequalities can be enforced by a countable dense
subfamily.

## Stronger obstruction to arbitrary finite strict quadratics

The root agent proposed a stronger statement, which survives review.
On the plane `u=x e1,v=y e2`, the hull slice is

```
x²<1, y²<1, (1-x²)(1-y²)>a².
```

Its positive boundary arc lies on
`P(x,y)=(1-x²)(1-y²)-a²=0`. This polynomial is irreducible over
`R[x,y]`: over `R(x)`, its root equation is

```
y²=(1-a²-x²)/(1-x²),
```

whose right side has distinct simple zeros and poles and is therefore
not a square. The polynomial is primitive over `R[x]`, so Gauss's lemma
applies.

If a finite list of strict quadratic inequalities represented the hull,
their restrictions to this plane would all be nonzero, because the
origin lies in the hull and each restriction is strictly negative there.
At every point on a compact subarc of the boundary, some restricted
quadratic must vanish: all are nonpositive by continuity from the hull,
and simultaneous strict negativity would wrongly include the boundary
point. A finite union of their zero sets covers the arc. By the Baire
theorem on that compact arc, one vanishes on a nonempty open subarc.
Equivalently, one may use analyticity of the graph parametrization.
Irreducibility then forces `P` to divide that polynomial, impossible for
a nonzero polynomial of degree at most two.

This conclusion concerns descriptions in the original variables. It does
not preclude lifted conic descriptions. The proof as written treats
finite conjunctions of strict inequalities, not arbitrary logical formulas.

## Literature comparison and novelty limits

Sources actually inspected on 2026-09-22:

- [Blekherman--Dey--Sun, arXiv:2210.01722v2](https://arxiv.org/html/2210.01722v2)
  and the [author PDF](https://www2.isye.gatech.edu/~sdey30/HHC.pdf).
  The examined definition uses every linear hyperplane; Conjecture 3.1
  asks for HHC with no finite good aggregation representation. The
  construction above addresses that conjunction. Their finiteness theorem
  additionally imposes PDLC, which this example fails.
- [Wang--Kılınç-Karzan, arXiv:2403.04752v2](https://arxiv.org/html/2403.04752v2),
  especially Section 4.1 and Remark 5. The QMP result gives convex-hull
  exactness of the standard SDP under quadratic multiplicity at least the
  number of constraints and a positive-definite quadratic-part
  combination. With zero objective it applies to the closed version of
  the present three-constraint example for `r>=3`. This already accounts
  for its closed SDP hull, but the inspected result does not assert HHC
  or rule out finite quadratic descriptions.
- [Brun--Sun--Watson, Modeling Adversarial Wildfires for Power Grid Disruption](https://optimization-online.org/wp-content/uploads/2026/03/AdversarialWildfire.pdf),
  Section 3.2, Theorem 1 and Corollary 1. This 2026 source derives the
  Shor convex hull of an inner-product hypograph over two Euclidean balls
  in dimension at least two, using the preceding QMP theorem. This is
  closely related prior work with a concrete mixed-integer application.
  Its hypograph result does not by itself imply the hull of a fixed
  superlevel slice, since convexification need not commute with slicing.
  No HHC or finite-description impossibility was found in the inspected
  section.
- [Blekherman--Dunbar, arXiv:2405.18282v1](https://arxiv.org/html/2405.18282v1)
  was opened as a relevant later aggregation source. This review did not
  complete a theorem-by-theorem audit of that paper; the author draft
  records a more detailed comparison.

Searches included the exact conjecture number, hidden hyperplane convexity
with infinitely many aggregations, quadratic matrix programming, and
quadratic eigenvalue multiplicity. No inspected source supplied the same
HHC-plus-infinite-necessity example. This is limited discovery evidence,
not proof of novelty. Claims of a new general HHC class need a separate
joint-numerical-range literature audit.

## Verification boundary

This review checked the author's proof algebra, all rank and dimension
conditions, strict inequalities, singular Gram cases, multiplier
degeneracies, and the difference between original and lifted descriptions.
No project-wide verification, CI inspection, numerical solver, or Lean
build was run. No author file was modified.
