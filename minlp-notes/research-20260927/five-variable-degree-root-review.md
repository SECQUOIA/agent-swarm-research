# Root review of the sharp five-variable degree bound

Date: 2026-09-28. Verdict: the combined finite-residual and
positive-dimensional-base arguments establish the upper bound 21
under the stated rational SOS and convexity assumptions. The root
read both proofs in full and independently reconstructed the steps
below. The root did not develop their geometric case analysis.
Publication priority is not established.

The reviewed statements are
[the finite residual obstruction](degree23-residual-obstruction.md)
and [the removal of a positive-dimensional base](five-variable-positive-base-bound.md).
Together they prove that a globally convex rational sum of quadratic
squares in five variables, with a unique real zero \(p\) and
\(\nabla^2F(p)\succ0\), satisfies
\[
 [\mathbb Q(p):\mathbb Q]\le21.
\]
The reviewed cyclic family attains 21. Rational SOS is essential
to the scope; this is not an upper bound for all rational convex
quartics.

## Finite complete intersections, including nonreduced residuals

The root checked the finite-algebra argument without assuming
reduced residual points. A proper intersection of five quadrics
has length 32. After choosing a linear form nonzero on its support,
its filtered affine algebra has associated graded Hilbert series
\((1+t)^5\). A nonzero functional on the top filtered quotient
gives a nondegenerate multiplication pairing and annihilates
degree at most four.

Remove a simple orbit \(\Gamma\) and write the residual algebra as
\(A_R\). For a quadric \(q\) vanishing on \(\Gamma\), the quotient
\(B=A_R/\operatorname{Ann}(q)\) has a nondegenerate pairing
\(\lambda_R(qab)\). The image \(V\) of affine linear polynomials
is totally isotropic, because \(qab\) has degree at most four.
Thus \(2\dim V\le\dim B\).

The scheme defined by \(B\) is a closed subscheme of the finite
quadratic intersection. In its linear span, of dimension
\(\dim V-1\), the restricted quadrics still have finite base.
Generic combinations and Bézout therefore give
\(\dim B\le2^{\dim V-1}\). With \(1\le\dim B\le9\), the two
inequalities force \(\dim B=8\) and \(\dim V=4\).

If no real residual point were a common zero of all quadrics
through \(\Gamma\), a rational combination \(q\) could avoid
every real residual point. It is a unit in every real local
factor. Quotienting by its annihilator preserves those factors;
the nonreal factors and their quotients have even real dimension.
Consequently \(\dim B\) has the same odd parity as a residual
of length \(1,3,5,7,\) or \(9\). This contradicts \(\dim B=8\).
The use of local factors, rather than just geometric support,
is what retains nonreduced multiplicities.

## The full quadratic base and generic selections

The positive-base proof concerns the common zero set of the entire
quadratic space. Five generic combinations have no positive-dimensional
component outside this full base: on its complement, the incidence
of a point and a combination matrix imposes five independent linear
conditions on the matrix. Its generic fibers are finite or empty.
Nonvanishing Jacobians at the finitely many orbit points impose
additional open conditions compatible with this choice.

The root reconstructed the weighted intersection count. Retain a
component when the next quadric contains it; otherwise intersect
properly and keep all resulting reduced components, allowing
duplicates as an overcount. The quantity \(2^{\dim X}\deg X\)
does not increase. Thus \(D\) simple isolated points leave weight
at most \(32-D\) for positive components.

For \(D\ge23\), this remaining weight is at most nine. An invariant
odd-degree projective component has a real point, by a generic real
linear section and parity. Components without real points are
therefore confined to the listed curves of total degree at most
four, or surfaces of total degree at most two. Components of
dimension at least three are excluded. This classification concerns
reduced maximal supports and does not assume a reduced base scheme.

## The perturbation bound and the case list

For each possible support, the proof finds a reduced pure-dimensional
local complete intersection \(Y\) whose ideal sheaf is generated
by quadratic sections. On its blowup, \(2H-E\) is globally
generated. Five generic sections have no common point on the
four-dimensional exceptional divisor and have a finite residual
intersection on the smooth complement. Every original simple
isolated zero outside \(Y\) persists under a small perturbation
by the implicit function theorem. This proves the required upper
bound using the generic intersection number. It does not assume
positive excess multiplicity for the original special equations.

The root independently checked all seven contributions:

| Reduced subbase \(Y\) | Contribution removed from 32 | Residual bound |
| --- | ---: | ---: |
| Two disjoint conjugate planes | 32 | 0 |
| Smooth quadric surface | 22 | 10 |
| Real conic without real points | 10 | 22 |
| Quartic curve of type \((2,2)\) in its three-dimensional span | 16 | 16 |
| Rational normal quartic | 18 | 14 |
| Two disjoint conjugate lines | 12 | 20 |
| Two disjoint conics with the stated quadratic generation | 20 | 12 |

Conjugate conics whose planes meet along a line instead form the
complete-intersection case with contribution 16. When their planes
meet only at an external point, the four cross products together
with \(c+c'-x_0^2\) define the union locally: the extra equation
is nonzero at the intersection point. Thus global generation
holds there as well. If the planes coincide, the quadrics vanish
on a real plane, which the hypotheses exclude.

For a real integral quartic curve in a three-dimensional span,
two independent containing quadrics form a proper complete
intersection equal to the reduced curve by degree and unmixedness.
With at most one containing quadric, the full base already contains
a real span or a quadric surface. A four-dimensional span gives
the classical rational normal quartic. These alternatives exhaust
the degree-four curve case.

Every possible positive subbase leaves at most 22 simple isolated
points. The assumed \(D\ge23\) is impossible, so the full base
is finite in the only degree range that needs exclusion.

## Application and source check

The root rechecked the earlier rational flat-direction reduction:
if the convex leading quartic has a nonzero real zero direction,
eliminating all such directions is a rational affine substitution.
It preserves the coordinate field, rational SOS, and the positive
definite Hessian at the zero. At most four variables then remain,
where even the ordinary quadratic bound 16 suffices. Otherwise
the homogenized full base has no real point at infinity and only
the prescribed affine zero. Positive components have no real points.
The preceding result makes the high-degree base finite, and the
finite residual argument excludes every odd degree at least 23.

The root directly read Eklund–Jost–Peterson,
[*A method to compute Segre classes of subschemes of projective space*](https://arxiv.org/pdf/1109.5895),
Theorem 3.2, proof Steps 0–4, Remark 3.3, and its regular-embedding
setup. The generic residual formula applies to a degree-two
generated homogeneous ideal even if it is not saturated. Its
zero-dimensional residual avoids the exceptional divisor, without
requiring the blowup to be smooth. The local complete-intersection
Segre class yields the normal-bundle expression used here.

The root also directly checked the degree–codimension inequality
and minimal-degree classification in Eisenbud–Green–Hulek–Popescu,
[*Small schemes and varieties of minimal degree*](https://arxiv.org/pdf/math/0404517),
Theorems 0.1–0.2 and their introductory setup. Only the integral
curve and degree-two surface cases are imported.

Two fresh specialists separately reviewed global generation and
the blowup argument, as linked in the main note. The author and
contributors ran the retained exact coefficient and intersection
checks. The root did not rerun them; finite arithmetic checks do
not establish the universal geometric classification. No Lean,
project-wide verification, CI inspection, or solver experiment is
claimed by this review.
