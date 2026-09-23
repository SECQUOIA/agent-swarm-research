# An explicit candidate resolution of BDS Conjecture 3.1

Date: 2026-09-22. Status: complete elementary proof drafted; independent
adversarial review and deeper novelty comparison are still required. Do not
promote this note to a verified result before those checks.

## Main claim

Blekherman–Dey–Sun (BDS), *Aggregations of quadratic inequalities and hidden
hyperplane convexity*, SIAM J. Optim. 34(1), 2024, Conjecture 3.1 asks whether
hidden hyperplane convexity (HHC) can hold while no finite collection of good
aggregations describes the convex hull. The following example appears to
answer this affirmatively, already with three quadratic inequalities.

Let `r >= 6`, `u,v in R^r`, and

```
f1(u,v) = ||u||² - 1,
f2(u,v) = ||v||² - 1,
f3(u,v) = 1/2 - u·v,
S = {(u,v): f1<0, f2<0, f3<0}.
```

Then the homogenized quadratic map has HHC, `S` is nonempty and bounded,
and `conv(S)` cannot be described using finitely many good aggregations.
Here a good aggregation is exactly the BDS definition: a nonzero multiplier
`lambda >= 0` for which the homogenized matrix has at most one negative
eigenvalue and `conv(S) subset {f_lambda<0}`.

The significance is a limitation of finite quadratic aggregation, despite
exactness of the complete aggregation family. This example is also a compact
matrix inequality model: the obstruction comes from the continuum of rank-one
boundary rays in a 2 by 2 positive-semidefinite multiplier cone. It does not
prove that the convex hull has no finite semidefinite or second-order-cone
extended formulation.

## General HHC construction

**Lemma.** Let `X in R^(k by r)`, `t in R`, and `r >= 3k`. Given any finite
family of symmetric `k by k` matrices `A_i` and scalars `c_i`, the quadratic map

```
phi_i(X,t) = tr(A_i XX^T) + c_i t²
```

has HHC. No definiteness or linear-independence assumptions are needed.

**Proof.** Fix a linear hyperplane

```
H = {(X,t): <B,X> + beta t = 0},
```

where `<B,X> = tr(BX^T)`. Take two points `(X1,t1),(X2,t2)` in `H` and
`0 <= theta <= 1`. Set

```
W = theta X1 X1^T + (1-theta) X2 X2^T,
s = theta t1² + (1-theta) t2².
```

If `s>0`, define

```
t = sqrt(s),
Z = [theta t1 X1 + (1-theta) t2 X2] / sqrt(s).
```

Then `<B,Z> = -beta sqrt(s)` and `D = W-ZZ^T` is positive semidefinite.
For the latter, for every vector `a in R^k`, the vector-valued Cauchy–Schwarz
inequality gives

```
||theta t1 X1^T a + (1-theta)t2 X2^T a||²
 <= s [theta ||X1^T a||² + (1-theta)||X2^T a||²].
```

If `s=0`, set `t=0`, `Z=0`, `D=W`; these definitions retain both properties.
(The cases of zero mixing weights also cause no problem.)

The common nullspace of the two `k by r` matrices `B,Z` has dimension at
least `r-2k >= k`. Choose a `k by r` matrix `U` whose rows are orthonormal
vectors in that common nullspace. Thus

```
UU^T=I_k,  BU^T=0,  ZU^T=0.
```

Let `Y=D^(1/2) U` and `X=Z+Y`. Then `YY^T=D`, `ZY^T=0`, and `<B,Y>=0`.
Consequently `(X,t) in H`, `XX^T=W`, and `t²=s`. Every output coordinate is
therefore the desired convex combination of the outputs of the two original
points. This proves convexity of `phi(H)`. Since `H` was arbitrary, HHC holds.

This sufficient dimension threshold is deliberately not claimed sharp.

## Applying the lemma

Set `k=2`, let the rows of `X` be `u^T,v^T`, and homogenize with `t`. The
three forms are

```
q1(X,t)=||u||²-t²,
q2(X,t)=||v||²-t²,
q3(X,t)=t²/2-u·v.
```

They have the form required by the lemma. HHC follows for `r>=6`.
Nonemptiness follows by taking `u=v=sqrt(3/4)e1`. Boundedness follows from
the two unit-ball inequalities, so the hull is proper.

## Exact identification of good aggregations

For `lambda >=0`, define

```
A_lambda = [[lambda1, -lambda3/2],[-lambda3/2,lambda2]],
c_lambda = -lambda1-lambda2+lambda3/2.
```

Up to permutation of coordinates, the homogenized matrix is

```
Q_lambda = (A_lambda tensor I_r) direct_sum [c_lambda].
```

If `A_lambda` has a negative eigenvalue, `Q_lambda` has at least `r>=2`
negative eigenvalues and is not permissible. If `A_lambda >=0` and
`lambda !=0`, then

```
lambda3 <= 2 sqrt(lambda1 lambda2) <= lambda1+lambda2,
c_lambda <= -(lambda1+lambda2)/2 <0.
```

Thus `Q_lambda` has exactly one negative eigenvalue. The polynomial
`f_lambda` is convex, strictly negative on `S`, and hence strictly negative
on every finite convex combination of points of `S`. Therefore it is good.
The complete set of good multipliers is exactly

```
K \ {0},  K={lambda>=0: lambda3² <=4 lambda1 lambda2}.
```

## Infinite necessity: an explicit continuum of uniquely active multipliers

For `tau in [1,2]`, put `epsilon=1/10` and choose vectors `u_tau,v_tau`
with Gram matrix

```
G_tau = [[1-epsilon/tau, 1/2-epsilon],
         [1/2-epsilon, 1-epsilon*tau]].
```

This matrix is positive definite: both diagonal entries are at least `4/5`
and its determinant is at least `(4/5)²-(2/5)²=12/25>0`. Hence such vectors
exist already in `R²` and can be padded by zeros into `R^r`. An explicit choice
is

```
u_tau = sqrt(1-epsilon/tau) e1,
v_tau = [(2/5)/sqrt(1-epsilon/tau)] e1
        + sqrt(1-epsilon*tau-(4/25)/(1-epsilon/tau)) e2.
```

At `x_tau=(u_tau,v_tau)`, the vector of original constraint values is

```
f(x_tau) = epsilon (-1/tau, -tau, 1).
```

For any good multiplier `lambda`,

```
f_lambda(x_tau)
 = epsilon[-lambda1/tau-lambda2*tau+lambda3] <=0,
```

because weighted AM–GM and positive semidefiniteness give

```
lambda1/tau+lambda2*tau >= 2 sqrt(lambda1 lambda2) >= lambda3.
```

Equality holds if and only if `lambda` is a positive multiple of

```
lambda(tau) = (tau, 1/tau, 2).
```

Indeed, equality requires both `lambda1/tau=lambda2*tau` and
`lambda3=2 sqrt(lambda1 lambda2)`; for nonzero `lambda` neither of the
first two coordinates can then vanish.

Given any finite list of good aggregations, choose `tau in [1,2]` whose
ray `lambda(tau)` is absent from that list. Then all listed aggregations
are strictly satisfied at `x_tau`. But

```
f_lambda(tau)(x_tau)=0,
```

whereas `f_lambda(tau)<0` throughout `conv(S)`, by convexity and strict
validity on `S`. Thus `x_tau` is outside the convex hull and inside the finite
intersection. No finite list of good aggregations defines `conv(S)`.

This argument does not need an algebraic-boundary irreducibility claim or
an explicit convex-hull formula.

## Optional hull formula from BDS

By the established HHC property and BDS Theorem 2.8,

```
conv(S) = { (u,v): ||u||²<1, ||v||²<1,
  1/2-u·v < sqrt((1-||u||²)(1-||v||²)) }.
```

To obtain this expression, the non-coordinate extreme rays of `K` are
`(tau,1/tau,2)` for `tau>0`. Writing `p=1-||u||²>0` and
`q=1-||v||²>0`, their inequalities say
`tau*p+q/tau > 2(1/2-u·v)` for every `tau>0`; the minimum is attained and
equals `2 sqrt(pq)`. The formula depends on the cited aggregation theorem;
the infinite-necessity proof above does not.

## PDLC fails

For an arbitrary signed multiplier `theta`, positive definiteness of
`A_theta` entails `theta1+theta2>|theta3|`. Positive definiteness of
`Q_theta` would additionally require `theta3/2 > theta1+theta2`, an
impossibility. Thus there is no positive-definite linear combination.
The example is consistent with BDS's finite-aggregation theorem under PDLC.

## Literature audit and boundary of the claim

Primary sources examined on 2026-09-22:

- Blekherman–Dey–Sun (2024), local
  `literature/papers/blekherman2024-aggregations-of-quadratic-inequalities-and/fulltext.md`,
  especially Definition 2.1, Theorem 2.8, Theorem 2.17, Conjectures 3.1–3.3,
  and Section 9. The [author PDF](https://www2.isye.gatech.edu/~sdey30/HHC.pdf)
  still states Conjecture 3.1. Its HHC examples use PDLC or a common linear
  factor; the replicated-matrix construction above is not one of those
  stated sufficient conditions.
- Blekherman–Dunbar, *A Topological Approach to Simple Descriptions of Convex
  Hulls of Sets Defined by Three Quadrics*,
  [arXiv:2405.18282v1](https://arxiv.org/html/2405.18282v1), especially
  Theorems 1.2–1.4. Theorem 1.4 gives at most four good aggregations under
  PDLC, nonempty interior, `S=cl(int(S))`, and no points at infinity.
  This is a partial negative result toward BDS Conjecture 3.2, not a
  resolution of Conjecture 3.1. The inspected arXiv page lists only v1.
- The author's [current homepage](https://alex-dunbar.github.io/) lists the
  topological paper as published in SIAM Journal on Applied Algebra and
  Geometry and a 2026 talk on duality for quadratic inequalities; it does not
  list a newer aggregation manuscript. This is limited discovery evidence.
- Search results expose Dunbar's 2025 thesis
  [PDF](https://etd.library.emory.edu/downloads/2j62s637x?locale=en), Theorem
  5.0.5, as removing the no-points-at-infinity assumption from the four-bound
  while retaining PDLC and `S=cl(int(S))`. Direct download returned HTTP 403,
  so this stronger statement has not yet been inspected in full context and
  must not be treated here as fully verified.

Novelty remains provisional. In particular, quadratic matrix programming,
semidefinite convex-hull descriptions under eigenvalue multiplicity, and
joint numerical ranges are relevant terminology that must be compared
before claiming a new general HHC theorem. Even if the hull formula is a
special case of known matrix-programming convexification, the identification
of this construction as an example for BDS Conjecture 3.1 needs a separate
prior-art check. An unsuccessful search does not establish originality.

No project-wide verification was run. At this draft stage the proof is
mathematical, not Lean-verified, and no targeted computational script has
yet been run.

### Additional primary-source comparisons

The published Blekherman–Dunbar paper is freely readable through the author's
[eprint link](https://epubs.siam.org/eprint/VRNXYR5GPAAPTF5RJHV3/full), DOI
`10.1137/24M1668445`, SIAM J. Applied Algebra and Geometry 9(2), 2025,
310–342. Its actual Theorem 1.4 still includes no points at infinity. Thus the
thesis search excerpt is not sufficient evidence for removing that hypothesis.
Theorem 3.9 concerns three quadrics in two variables, with empty projective
variety and smooth nonhyperbolic spectral curve, and allows a possibly infinite
family; it does not supply an HHC example requiring infinity. The present
example has a nonempty common projective zero set and a singular spectral
curve: `det(Q_lambda)=(lambda1 lambda2-lambda3²/4)^r
(-lambda1-lambda2+lambda3/2)`. Hence their empty-variety and smooth-curve
finiteness theorems do not apply.

Wang–Kılınç-Karzan, *On semidefinite descriptions for convex hulls of quadratic
programs* (2024), [arXiv:2403.04752, Appendix B.2](https://arxiv.org/html/2403.04752v1#A2.SS2),
proves convex-hull exactness for quadratic matrix programs with at least as
many repeated columns as constraints, under a strictly positive-definite
convex quadratic combination assumption. Our example has three constraints,
`r` repeated columns, and `A1+A2=I`, so that theorem already yields SDP
convex-hull exactness for its non-strict version when `r>=3`. The closed hull
and its SDP exactness must not be promoted as novel results. The contribution
under investigation is HHC together with the impossibility of a finite
*direct good-aggregation* description. Their earlier work and Beck's quadratic
matrix-programming results supply the relevant prior theory for the positive
exactness property.

Dey–Han–Wang, *Aggregation of bilinear bipartite equality constraints and its
application to structural model updating problem*, J. Global Optimization
94, 1099–1135 (2026),
[full text](https://link.springer.com/article/10.1007/s10898-026-01607-8),
Theorem 2, already proves infinite aggregation necessity for a different
closure. Its inputs are two bilinear equalities on a box; multipliers may be
signed, and each aggregated equality is convexified over that box before
intersection. Their example has `xy1=xy2=1/2` on `[0,1]^3`, with its hull
contained in `y1=y2`. The authors explicitly distinguish this from directly
intersecting good quadratic sublevel sets in their introduction. The theorem
neither establishes HHC nor uses the BDS good-aggregation closure, so it does
not resolve the stated conjecture. It does prevent a broad claim that infinite
aggregation necessity for nonlinear optimization is new. Local copy:
`literature/papers/dey2026-aggregation-of-bilinear-bipartite-equality/fulltext.md`.

### Independent derivations received

The root agent independently derived the same HHC construction with
`r>=3k`, and derived the hull formula directly for `r>=3`, without BDS:
for a candidate pair, put `p=1-||u||²`, `q=1-||v||²` and choose a common
unit vector `e` perpendicular to `u,v`. If `u·v+sqrt(pq)>1/2`, choose
`0<=eta<1` sufficiently near 1. Then

```
(u ± eta sqrt(p)e, v ± eta sqrt(q)e)
```

are both in `S`, with midpoint `(u,v)`. Conversely, the covariance
Cauchy–Schwarz inequality for any finite mixture of points of `S` implies
the hull inequality. A fresh reviewer independently produced another
uniquely active multiplier family on the orthogonal-coordinate slice.
These agreements provide corroboration; they do not replace a final review.

### Targeted verification performed

A `python` heredoc using SymPy was run for this topic only. It asserted the
exact 2 by 2 multiplier determinant, substituted the Gram witness into the
three constraints, checked that its designated multiplier is active, and
verified symbolically the distinct-ray slack identity

```
f_lambda(v)(x_tau) = -(v-tau)²/(10 tau v).
```

All assertions passed. It also returned
`det(G_tau)=-(2 tau²-17 tau+2)/(20 tau)`, consistent with the uniform
positive-definiteness bound in the proof. These symbolic checks verify the
finite algebraic identities. They do not verify the universal HHC argument,
quantification over arbitrary finite aggregation families, or novelty.
No project-wide checks or CI inspection were performed.

## Stronger consequence awaiting independent review

The uniquely active witness argument is stronger than finite necessity.
Suppose a family `Lambda` of good multipliers describes `conv(S)` exactly
using strict inequalities. For every `tau in [1,2]`, the family must contain
a positive multiple of `lambda(tau)`. Otherwise `x_tau` strictly satisfies
every member of the family, while lying outside the hull. Distinct values of
`tau` give distinct rays, so every exact strict good-aggregation description
has uncountably many members.

This assertion concerns strict inequalities and the ordinary open convex
hull. It does not extend to the countability requirement for the closed hull:
continuity allows a dense countable subset of multipliers to capture all
non-strict aggregated inequalities. The finite-necessity obstruction for a
closed hull can instead use a nearby point beyond an omitted supporting
quadratic, retaining strict slack in the finitely many chosen quadratics.
