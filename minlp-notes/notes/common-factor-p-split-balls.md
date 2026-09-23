# Exact basic P-split relaxation for two translated balls

Status: mathematical proof independently audited, 2026-09-04; novelty provisional.
See the [independent audit](review-common-factor-p-split-balls.md).
This is a quantitative follow-up to the [Theorem 6 correction](common-factor-p-split-correction.md).

## 1. Scope and formula

Let \(n\ge2\), \(r>0\), and \(d>2r\). Write \(x=(t,w)\), with
\(w\in\mathbb R^{n-1}\). Consider the two disjuncts

\[
D_0=\{t^2+\|w\|_2^2\le r^2\},\qquad
D_d=\{(t-d)^2+\|w\|_2^2\le r^2\},
\]

over their common coordinate bounding box
\(X=[-r,d+r]\times[-r,r]^{n-1}\).
Their true hull is the capsule

\[
C=[0,d]e_1+r\mathbb B_2^n.
\tag{1}
\]

Use the basic P-split construction of Kronqvist–Misener–Tsay, with tight global interval
bounds over X, the natural coordinate functions \(t^2,(t-d)^2,w_i^2\), and the shared
auxiliaries for identical transverse functions required by their Remark 1.
No extra linking cuts, polynomial rewriting, or alternative auxiliary identities
are included in the following claim; these could change the relaxation.

**Theorem.** The fully split relaxation projects exactly to

\[
R=\left\{(t,w):\|w\|_2\le r,\quad
2(t-d/2)^2+\|w\|_2^2\le2(d/2+r)^2\right\}.
\tag{2}
\]

The two-group partition \(\{t\},\{w_1,\ldots,w_{n-1}\}\) gives the same
relaxation. Thus further splitting the transverse variables adds no strength in
this family. Every basic coordinate partition has a relaxation containing (2),
by the additive-bound refinement property proved in the source.

## 2. Exact auxiliary hull

Put \(U=(d+r)^2\). In the full split, introduce

\[
a\ge t^2,\qquad b\ge(t-d)^2,\qquad c_i\ge w_i^2.
\]

The auxiliary bounds are \(0\le a,b\le U\) and \(0\le c_i\le r^2\).
The auxiliary disjunction is

\[
a+\sum_i c_i\le r^2
\quad\text{or}\quad
b+\sum_i c_i\le r^2.
\tag{3}
\]

Its exact convex hull is

\[
0\le a,b\le U,\qquad c_i\ge0,\qquad
\sum_i c_i\le r^2,\qquad
a+b+\sum_i c_i\le U+r^2.
\tag{4}
\]

Necessity follows separately in each disjunct. For sufficiency fix any vector
\(c\) satisfying (4), and put \(h=r^2-\sum_i c_i\in[0,r^2]\).
At that fixed \(c\), the union in the \((a,b)\) square is
\([0,h]\times[0,U]\ \cup\ [0,U]\times[0,h]\).
Its hull is exactly the square intersected with \(a+b\le U+h\); each vertex
of this truncated square belongs to the union. Thus the fixed-\(c\) slice in
(4) is contained in the convex hull of (3), proving sufficiency. The individual
upper bounds on \(c_i\) are redundant in (4).

The polytope (4) is downward closed in \((a,b,c)\). Consequently its epigraph
projection is obtained by substituting the actual function values:

\[
\|w\|_2^2\le r^2,\qquad
t^2+(t-d)^2+\|w\|_2^2\le(d+r)^2+r^2.
\]

These are exactly (2). The original box bounds are implied by (2): the cylinder
gives the transverse bounds, and the ellipsoid at \(w=0\) gives
\(-r\le t\le d+r\). The argument also covers the two-group split using a
single \(c\ge\|w\|_2^2\). Its initial interval upper bound is
\((n-1)r^2\), but the disjunction itself enforces \(c\le r^2\), so the same
auxiliary hull and projection result.

## 3. Exact quantitative loss

Define

\[
e=\sqrt{(d/2+r)^2-r^2/2}-d/2>0.
\tag{5}
\]

At \(\|w\|_2=r\), the relaxation includes \((-e,w)\), while the capsule's
left boundary on that transverse slice is \((0,w)\). Hence the relaxation is
strictly larger. More precisely, its directed Euclidean Hausdorff distance from
the true hull is

\[
\boxed{\quad
\sup_{x\in R}\operatorname{dist}_2(x,C)
=\sqrt{r^2+e^2}-r.
\quad}
\tag{6}
\]

**Proof.** Between the centers, every point in the cylinder belongs to the
capsule. By symmetry it suffices to consider \(t\le0\). At transverse norm
\(\rho\in[0,r]\), the farthest admissible point from the first center has

\[
t=-e(\rho),\qquad e(\rho)=\sqrt{(d/2+r)^2-\rho^2/2}-d/2.
\]

Here \(e(\rho)>0\). Distance to the capsule is
\(\sqrt{e(\rho)^2+\rho^2}-r\), since the closest point of the center segment is
its first endpoint. With \(u=\rho^2\) and \(L=d/2+r\), the squared radial norm
is

\[
L^2+d^2/4+u/2-d\sqrt{L^2-u/2}.
\]

Its derivative is \(1/2+d/(4\sqrt{L^2-u/2})>0\). The maximum occurs at
\(\rho=r\), which proves (6). ∎

As \(d/r\to\infty\), \(e/r\to1\), and therefore

\[
\frac1r\sup_{x\in R}\operatorname{dist}_2(x,C)\longrightarrow\sqrt2-1.
\tag{7}
\]

The loss is independent of dimension and persists even at the strongest basic
coordinate partition. This contrasts with the truncated-domain counterexample,
where the true hull is the entire retained box and every split is exact.

## 4. Literature status

The auxiliary formulation, sharing rule, and additive-bound hierarchy are known
from the [P-split paper](https://doi.org/10.1007/s10107-025-02232-1).
Equation (2) and the distance formula are a direct calculation for this special
family. They are not claimed to be a general characterization of nonlinear
P-split exactness. A bounded search for the specific ball relaxation and Hausdorff formula found
no direct antecedent; this is not an exhaustive novelty certificate. The proof
has passed independent mathematical and source-scope review.

## 5. Verification

[The verification script](../code/common-factor-p-split-balls-verify.py) compares
the proposed projected inequalities, evaluated in exact rational arithmetic,
with an LP formed directly from the two auxiliary disjuncts and their perspective
bounds. All 240 classifications passed (122 feasible, 118 infeasible). The LP
uses numerical HiGHS and is corroboration rather than an exact proof certificate.
For \(r=1,d=3\), the rational point \((t,w)=(-7/8,1)\) is certified to satisfy
(2) and violate the true left ball; its nearest center on the segment is zero.
The analytic proof passed [independent review](review-common-factor-p-split-balls.md).
