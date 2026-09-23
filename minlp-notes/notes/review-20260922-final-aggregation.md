# Fresh integrated review of the infinite aggregation result

Date: 2026-09-22. Reviewed artifact:
[the integrated result](../results/infinite-quadratic-aggregation-hhc.md),
as read at the start of this review. The reviewer did not edit that result
and did not delegate this review. Earlier favorable reviews were not
treated as proof certificates.

**Verdict:** I found no mathematical error in the integrated theorem or its
proofs. The example establishes the assertion of BDS Conjecture 3.1 in the
open versions checked. Two source-version corrections are needed: the
aggregation theorem is Theorem 2.8 in the linked 2022 author PDF but Theorem
2.9 in arXiv v2; WKK Appendix B.2 belongs to v1, not the linked v2. The
published BDS full text was inaccessible in this review, so an attribution
to its exact published numbering should remain qualified. Priority and
solver benefits remain unproved.

## HHC, including replication two

I reconstructed the proof using the pair `(G,T)=(U^T U,t²)`, without assuming
that the orthogonal group is connected. For every PSD two by two matrix
`G` and `r>=2`, each matrix with Gram matrix `G` can be written
`U=Q G^(1/2)` with `Q^TQ=I`. For singular `G`, the isometry on its range
extends to two orthonormal columns. The SVD optimization gives the attained
maximum `M=||P G^(1/2)||_*` of `tr(P^T U)`.

The path `Q R(theta) G^(1/2)`, where `R` rotates from `I` to `-I`, keeps
the Gram matrix fixed. Its functional values join `M` and `-M`. The
intermediate value theorem supplies every number in this interval, even
in dimension two. The hyperplane condition is therefore equivalent to
`s²T<=M²`, including `s=0`, `P=0`, and singular `G`.

The identity
`M²=tr(P^TP G)+2 sqrt(det(P^TP)det(G))` follows from the two singular
values. Concavity of `sqrt(det(G))` on the PSD cone follows from the
displayed infimum formula. The infimum need not be attained at a singular
`G`; the argument uses only its value and concavity, so this causes no
gap. Thus the attainable pair set is convex and its linear image is the
actual hyperplane image, with no closure operation. This proves the stated
HHC property for all `r>=2`.

## All good multipliers and the strict and closed obstructions

Any negative eigenvalue in the two by two leading block has multiplicity
at least two. Permissibility forces that block to be PSD, hence exactly
the stated cone `K`. Conversely, for nonzero `lambda in K`,
`lambda1+lambda2>0` and
`lambda3/2-lambda1-lambda2 <= -(lambda1+lambda2)/2<0`.
The aggregate is convex in the original variables. Jensen's inequality
makes it strictly negative on every finite convex combination from `S`.
There are no unaccounted good multipliers outside `K`.

The witness Gram matrix is positive definite throughout `[1,2]`. At the
witness, weighted AM–GM gives

```
lambda3 <= 2sqrt(lambda1 lambda2)
        <= lambda1/tau + lambda2*tau.
```

Equality in both inequalities forces a positive multiple of
`(tau,1/tau,2)`; zero coordinate multipliers introduce no other equality
case. Excluding one ray leaves its witness satisfying every other strict
good aggregation, even if an uncountable set of other rays is retained.
This proves the claimed uncountable necessity.

For the closed claim, a finite family has a positive minimum strict slack
at an omitted-ray witness. A small reduction of the Gram off-diagonal
preserves positive definiteness and all those slacks. The omitted
normalized aggregate becomes `2 eta>0` and separates the point from the
closed hull. This does not mistake a strict boundary witness for a point
outside the closed hull.

The introductory countable-sufficiency claim for the closed hull can be
made explicit: use the coordinate rays and positive rational `tau`.
Continuity extends their non-strict inequalities to every positive real
`tau`. For `p,q>0` the minimum is attained; if one is zero, taking the
appropriate endpoint limit yields `u·v>=1/2`. Their intersection is
therefore exactly the closed formula. This non-strict argument does not
contradict strict uncountable necessity.

## Ordinary hull formula and unrestricted quadratics

BDS exact aggregation applies to the homogenization: `n=2r>=4`, the set
is nonempty, and its bounded hull is proper. The coordinate rays force
`p,q>0`. Consequently the minimum of `tau*p+q/tau` occurs at the finite
positive value `tau=sqrt(q/p)`. The strict hull formula does not infer
a strict bound from an unattained infimum. The direct midpoint argument
for `r>=3` also works: squared norms remain below one and the inner
product approaches `u·v+sqrt(pq)>1/2` as `alpha` approaches one from below.
It is correctly not used for `r=2`.

The planar section uses the already established full-space hull formula;
it never assumes that convexification commutes with taking the plane.
An explicit regular boundary arc is

```
x in [1/4,1/2],
y=sqrt((3/4-x²)/(1-x²)).
```

The irreducibility argument is correct. The rational function has simple
zeros at `±sqrt(3)/2` and simple poles at `±1`, so it is not a square in
`R(x)`. The coefficients of the polynomial in `y` are relatively prime
in `R[x]`, so Gauss's lemma applies.

Every hypothesized restricted quadratic is nonzero because its value at
the origin must be strictly negative. Its restriction to the displayed
arc is real analytic on a neighborhood of the compact interval. Unless
it vanishes identically on an interval, its zeros there are finite. Thus
a finite family covering the arc must contain one that vanishes on an
interval. Dividing that quadratic by `P` over `R(x)[y]` gives a remainder
`A(x)y+B(x)`. A nonzero remainder vanishing on the arc would make `y` a
rational function, contradicting the nonsquare observation. Gauss's lemma
then forces divisibility by the degree-four `P`, impossible
for a nonzero polynomial of degree at most two. This independently
verifies the stronger finite original-space quadratic obstruction.

## SDP hull equality and compactness

The Schur complement of `I_r` in (9) gives precisely
`p,q>=0` and `|sigma-u·v|<=sqrt(pq)`. A feasible `sigma>=1/2` exists
exactly when the upper endpoint of that interval is at least `1/2`.
This establishes the displayed closed formula directly, including zero
slack cases; a general projection-closedness claim is unnecessary.

At the origin, `sigma=1/2` makes the full matrix positive definite.
A strict convex combination of this matrix with any feasible PSD matrix
is positive definite, and its `sigma` remains at least `1/2`. Its upper
Schur interval endpoint is then strictly greater than `1/2`, giving a
point in the ordinary hull. This proves density of the ordinary hull in
(9). The reverse inclusion follows because (9) is closed and contains
the ordinary hull. The strict version with `sigma>1/2` is also equivalent:
when the upper endpoint exceeds `1/2`, choose `sigma` strictly inside the
interval and above `1/2`.

Let `T` be the original closed system. It is compact, contains `S`, and
is contained in (9): choose `sigma=u·v` for a point of `T`. Its convex
hull is compact in finite dimensions and thus contains `cl conv(S)`.
Convexity of (9) gives the reverse containment. This sandwich proves
`conv(T)=cl conv(S)=(9)` without asserting `T=cl(S)` or commuting
convexification with a hypograph level slice.

PDLC fails also for signed multipliers: positive definiteness of the
leading block implies `lambda1+lambda2>|lambda3|`, incompatible with
positivity of the scalar block. No PDLC finiteness theorem is contradicted.

## Source scope and significance

I checked the BDS definitions, exact-aggregation theorem, and Conjecture
3.1 in the [2022 author PDF](https://www2.isye.gatech.edu/~sdey30/HHC.pdf)
and the [2023 arXiv v2](https://arxiv.org/html/2210.01722v2).
The conjecture's assertion is unchanged. The exact-aggregation theorem
changes from 2.8 to 2.9; the finiteness theorem changes from 2.17 to 2.18.
The [publisher record](https://epubs.siam.org/doi/10.1137/22M1528215)
confirms publication in 2024, but full-text retrieval returned 403. The
local `fulltext.md` is extracted from the older author PDF, despite its
2024 bibliographic directory name.

I checked [Wang–Kılınç-Karzan v2](https://arxiv.org/html/2403.04752v2),
Section 4.1. Its replication-width condition covers the closed system
when `r>=3`, using zero objective and the positive definite sum of the
two ball Hessians. That result neither supplies HHC nor states finite
quadratic impossibility. The integrated result correctly credits this
prior SDP exactness; the reference to Appendix B.2 must explicitly name
v1, since v2 contains no such appendix.

I read the existing detailed novelty review for the Dey–Muñoz–Serrano,
Brun–Sun–Watson, Blekherman–Dunbar, and Dey–Han–Wang comparisons. I did
not independently repeat all their full-text audits. Nothing in those
reported comparisons contradicts the limited novelty claim, but those
prior reviews remain the evidence for their detailed source assertions.

The possible contribution is a small explicit construction satisfying
the exact HHC conjecture together with strong original-space formulation
obstructions. It does not establish computational hardness, a general new
SDP exactness principle, or impossibility of finite lifted SOC/SDP models.
The result may justify replacing quadratic aggregation cuts by a lift for
recognized structures, but a demonstrated solver advantage requires
additional work. An unsuccessful literature search cannot establish
priority; this review makes no stronger priority claim.

## Targeted verification

I read and ran
`python3 code/research_20260922/check_infinite_aggregation.py`.
It passed 2,601 exact rational ray identities and six finite-family
perturbation witnesses. Its finite examples do not prove the universal
obstruction, HHC, irreducibility, or novelty; those were checked by the
arguments above. Only targeted file reads, primary-source queries, and
this checker were used. No Lean formalization, project-wide checks, or
CI inspection were performed.

