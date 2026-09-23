# An unbounded coordinate effect in the basic P-split relaxation

Status: the original and rational coordinate comparisons passed independent
mathematical audit, 2026-09-04; novelty remains provisional. See the
[audit](review-common-factor-p-split-rotation-gap.md).
The auxiliary-only strengthening and exact-image comparison in Sections 5–6
also passed the final independent audit.

## 1. Model and precise comparison

Let \(D\ge5\). In two variables consider the disjunction

\[
\mathcal D_0=\{x:x_1^2+x_2^2\le1\},\qquad
\mathcal D_1=\{x:(x_1-D)^2+(x_2-D)^2\le1\},
\]

over the retained domain \(X=[-1,D+1]^2\). Both complete unit balls lie in
\(X\), they are disjoint, and their hull is

\[
C=[(0,0),(D,D)]+\mathbb B_2^2.
\tag{1}
\]

Use the basic P-split construction from
[Kronqvist–Misener–Tsay](https://doi.org/10.1007/s10107-025-02232-1):
natural coordinate summands, exact global interval bounds over the retained
domain, epigraph links outside the auxiliary disjunction, the exact hull of
that auxiliary disjunction, and shared auxiliaries for identical functions.
Do not add other valid linking inequalities, substitute polynomial identities,
or strengthen global bounds to disjunct-specific bounds. These choices define
the relaxation being compared, rather than a claim about every possible
strengthening of P-split.

Let \(R_D\) be its full two-coordinate split in the original coordinates.
Apply the following orthogonal change of coordinates to the complete model,
including \(X\):

\[
t=(x_1+x_2)/\sqrt2,\qquad w=(x_1-x_2)/\sqrt2.
\tag{2}
\]

Write \(T\) for this orthogonal map, \(d=\sqrt2D\), and

\[
X'=T(X)=\{(t,w):-\sqrt2\le t+w,t-w\le\sqrt2(D+1)\}.
\tag{3}
\]

Define \(R'_D\) by applying the same basic two-coordinate split to the
rotated natural summands \(t^2,(t-d)^2,w^2\), retaining exactly the diamond
\(X'\) and recomputing tight global bounds over that diamond.

**Theorem.** With Euclidean Hausdorff distance \(d_H\),

\[
d_H(R_D,C)\ge \frac{D}{3\sqrt2}-1,
\qquad
d_H(R'_D,T(C))\le\sqrt2-1.
\tag{4}
\]

Thus the absolute improvement in this error measure from a fixed orthogonal
change of coordinates grows without bound, already with two continuous
variables, two strictly convex disjuncts, and fixed unit-radius balls. The
comparison uses the same feasible set and the same retained global domain,
up to that rotation. The separation between the centers grows with \(D\).

## 2. Explicit original-coordinate lift

Put \(U=(D+1)^2\). The original full split uses four auxiliary coordinates

\[
a_i\ge x_i^2,\quad b_i\ge(x_i-D)^2,\qquad 0\le a_i,b_i\le U,
\]

and convexifies

\[
a_1+a_2\le1\quad\text{or}\quad b_1+b_2\le1.
\tag{5}
\]

There are no identical coordinate functions across these two disjuncts.
Consider

\[
p=(2D/3,D/3),\quad
a=(4D^2/9,D^2/9),\quad b=(D^2/9,4D^2/9).
\tag{6}
\]

These auxiliary values equal the nonlinear functions at \(p\). Moreover,
\(2a_i,2b_i\le8D^2/9\le U\). Therefore \((a,b)\) is the half-weight
average of \((0,2b)\), which satisfies the first auxiliary disjunct, and
\((2a,0)\), which satisfies the second. This is a valid exact auxiliary-hull
lift, so \(p\in R_D\).

The orthogonal projection of \(p\) onto the center segment in (1) is
\((D/2,D/2)\). Its distance to that segment is \(D/(3\sqrt2)\).
Consequently

\[
\operatorname{dist}(p,C)=D/(3\sqrt2)-1>0,
\]

which proves the first inequality in (4). Convexity and validity of the
relaxation give \(C\subseteq R_D\), so directed and ordinary Hausdorff
distance coincide. The original one-group relaxation contains this two-group
relaxation by direct aggregation of its bounded auxiliary coordinates; the
same lower bound therefore applies to both basic coordinate partitions here.

## 3. The rotated relaxation has bounded error

The rotated disjuncts are

\[
t^2+w^2\le1\quad\text{or}\quad(t-d)^2+w^2\le1.
\]

The identical transverse function is shared, as required by the source's
minimal-auxiliary convention. Hence the split uses

\[
a\ge t^2,\quad b\ge(t-d)^2,\quad c\ge w^2,
\]

with exact global bounds

\[
0\le a,b\le2(D+1)^2,\qquad 0\le c\le(D+2)^2/2.
\tag{7}
\]

These extrema follow by evaluating the linear coordinates \(t,w\) at the
four corners of the original box. The auxiliary disjunction is
\(a+c\le1\) or \(b+c\le1\). Every point in either disjunct has \(c\le1\),
and so does every point in its convex hull. Thus

\[
R'_D\subseteq X'\cap\{|w|\le1\}.
\tag{8}
\]

The rotated true hull is the capsule \(T(C)=[0,d]e_t+\mathbb B_2^2\).
For \(0\le t\le d\), every point in (8) belongs to this capsule.
If \(t\le0\), set \(\rho=|w|\in[0,1]\). The diamond inequalities imply
\(-t+\rho\le\sqrt2\). Therefore

\[
t^2+w^2\le(\sqrt2-\rho)^2+\rho^2\le2.
\tag{9}
\]

The last quadratic is convex in \(\rho\); at the two endpoints of \([0,1]\)
its values are \(2\) and \(4-2\sqrt2<2\). The closest point on the center
segment is its left endpoint, so distance to the unit-radius capsule is at
most \(\sqrt2-1\). If \(t\ge d\), the upper diamond inequalities instead
give \(t-d+\rho\le\sqrt2\), and the same argument applies at the right
endpoint. This proves the second inequality in (4), since validity also gives
\(T(C)\subseteq R'_D\).

The rotated domain is a diamond, not a Cartesian product. In particular,
global component bounds over it need not be additive. No refinement hierarchy
or claim that the rotated two-group partition dominates every other partition
is used or asserted.

## 4. Rational-data version

The same separation holds with a fixed rational orthogonal transformation and
rational input data. Let the centers be \(0\) and \(v=(3D,4D)\), with
\(D\ge2\), unit radii, and retained box
\(X=[-1,3D+1]\times[-1,4D+1]\). The original-coordinate point

\[
p=(2D,4D/3)
\]

has a valid half-weight auxiliary lift. Indeed, for each coordinate, both
\(p_i\) and \(v_i-p_i\) are at most \(2v_i/3\), so twice their
squares are at most \(8v_i^2/9\le(v_i+1)^2\), the exact global upper
bound of either corresponding quadratic. The two lifted disjunct points
again set their respective active auxiliary pair to zero.

Use

\[
t=(3x_1+4x_2)/5,\qquad w=(4x_1-3x_2)/5.
\tag{10}
\]

The centers become \(0\) and \(5D e_t\), while the witness satisfies
\(t(p)=34D/15\in[0,5D]\) and \(w(p)=4D/5\). Therefore the original
relaxation has Hausdorff error at least \(4D/5-1\).

After transforming the complete retained box, the shared transverse auxiliary
again implies \(|w|\le1\). If \(t\le0\), the inverse formulas give

\[
x_1=(3t+4w)/5\le4/5,\qquad x_2=(4t-3w)/5\le3/5.
\]

The retained domain also gives \(x_1,x_2\ge-1\), so
\(t^2+w^2=x_1^2+x_2^2\le2\). If \(t\ge5D\), put
\(h=x-v\) and \(s=t-5D\ge0\). The inverse formulas now give
\(h_1\ge-4/5\), \(h_2\ge-3/5\), whereas the retained box gives
\(h_1,h_2\le1\). Thus \(s^2+w^2=\|h\|^2\le2\).
Between the centers, \(|w|\le1\) already puts the point in the capsule.
The transformed relaxation therefore has Hausdorff error at most
\(\sqrt2-1\) for every \(D\).

Both displayed coordinate maps are orthogonal with determinant \(-1\).
Negating their transverse coordinate gives proper rotations and leaves every
absolute-value argument unchanged. In (10) all data, including the coordinate
map, the transformed domain inequalities, and tight quadratic interval bounds,
are rational when \(D\) is rational.

## 5. Lower bound survives arbitrary auxiliary-only strengthening

The explicit lower-bound construction admits a stronger interpretation. For a
center vector \(v\), define the coordinate lift

\[
F(x)=\bigl(x_i^2,(x_i-v_i)^2\bigr)_{i=1}^2.
\]

Let \(Q\) be **any convex set** of auxiliary values containing \(F(0)\)
and \(F(v)\), and form the epigraph relaxation

\[
R(Q)=\{x\in X:\exists\alpha\in Q,\ F(x)\le\alpha\},
\tag{11}
\]

where the inequality is coordinatewise. Convexity forces

\[
\bar\alpha=\tfrac12F(0)+\tfrac12F(v)
=\bigl(v_i^2/2,v_i^2/2\bigr)_{i=1}^2\in Q.
\tag{12}
\]

For either witness in Sections 2 and 4, each coordinate lies at either one
third or two thirds of the corresponding center coordinate. Hence

\[
\max\{p_i^2,(p_i-v_i)^2\}=4v_i^2/9\le v_i^2/2,
\]

so \(p\in R(Q)\), regardless of any further restrictions defining
\(Q\). In particular, the lower bounds remain valid even for

\[
Q=\operatorname{conv}F(\mathcal D_0\cup\mathcal D_1),
\tag{13}
\]

which is the smallest convex auxiliary set preserving every actual feasible
function image. This also covers any valid auxiliary-only linking constraints
and disjunct-specific auxiliary bounds, provided the nonlinear coupling to
\(x\) remains exactly the coordinate epigraph links in (11).

This observation isolates the obstruction in the epigraph links themselves.
It does **not** cover added constraints coupling original and auxiliary
variables, added original-space cuts, equality identities replacing epigraph
links, or a different family of lifted functions. Those can remove the witness.
In the transformed coordinates, auxiliary strengthening that remains a subset
of the basic auxiliary hull preserves \(c\le1\), so the same uniform
upper bound remains valid as well. Thus the coordinate comparison persists
between the smallest exact-image auxiliary convexifications of the two models.

## 6. Exact-image auxiliary convexification becomes exact after alignment

There is a stronger comparison for the smallest auxiliary hull (13). In aligned
coordinates, let \(d>2\) and define

\[
F'(t,w)=(a,b,c)=(t^2,(t-d)^2,w^2),\qquad
Q'=\operatorname{conv}F'(\mathcal D'_0\cup\mathcal D'_1),
\]

where the two disjuncts are complete unit balls centered at \(0\) and
\(d e_t\). Set

\[
f(c)=d^2+1-c+2d\sqrt{1-c},\qquad 0\le c\le1.
\tag{14}
\]

This function is concave and decreasing. Every actual feasible image satisfies

\[
0\le c\le1,\qquad a\le f(c),\quad b\le f(c).
\tag{15}
\]

Indeed, at fixed \(w^2=c\), put \(q=\sqrt{1-c}\). Feasible longitudinal
coordinates lie in \([-q,q]\cup[d-q,d+q]\), so both \(t^2\) and
\((t-d)^2\) are at most \((d+q)^2=f(c)\). The hypographs in (15) are
convex, so (15) holds throughout \(Q'\).

If the epigraph links \(t^2\le a\), \((t-d)^2\le b\), and
\(w^2\le c\) are feasible for \((a,b,c)\in Q'\), then monotonicity
of \(f\) gives

\[
|t|\le d+\sqrt{1-w^2},\qquad
|t-d|\le d+\sqrt{1-w^2}.
\]

Their intersection is exactly

\[
|w|\le1,\qquad
-\sqrt{1-w^2}\le t\le d+\sqrt{1-w^2},
\tag{16}
\]

which describes the true capsule. Conversely, the epigraph relaxation is
convex and contains both balls, so it contains their capsule. Therefore its
projection is exactly the true hull, including when the common retained
domain is the exact orthogonal image of either box above.

In fact, the two convex auxiliary inequalities \(a\le f(c)\),
\(b\le f(c)\), together with \(0\le c\le1\), already give this exact
projection; computing the full set \(Q'\) is unnecessary. This is a
specialized repair for the two-ball family, not a new general formulation of
capsules. Each inequality can be represented with a nonnegative variable
\(s\), \(s^2+c\le1\), and respectively
\(a+c-d^2-1\le2ds\) or \(b+c-d^2-1\le2ds\).

Combining Sections 5 and 6: for rational two-ball models and a fixed rational
orthogonal change of coordinates, the tightest convexification confined to the
chosen auxiliary function space can change from unbounded Hausdorff error to
an exact hull. The remaining epigraph links are identical in form; the chosen
coordinate functions and their sharing change.

This section passed the final independent audit, including the conic representation.

## 7. Meaning and limitations

The source already recognizes that variable grouping and auxiliary choices
affect relaxation strength. The quantitative claim here is narrower: tight
global bounds and full coordinate splitting can have an unbounded absolute
error before an orthogonal change of coordinates, while after the change the
same basic construction has a uniform error bound. Function sharing exposes
the common transverse quadratic after rotation. The retained global domain
is transformed exactly, so the comparison does not introduce a new domain
restriction.

The lower bound covers auxiliary-only strengthening as specified in Section 5;
it does not cover arbitrary strengthened P-split formulations, affine-invariant
methods, or the convex-hull perspective formulation. It does not give an
algorithm for selecting a good coordinate system in a general MINLP. The mathematical claims passed independent review. Publication novelty remains
provisional, as detailed below.

Related local notes: [source theorem correction](common-factor-p-split-correction.md)
and [exact relaxation for axis-aligned translated balls](common-factor-p-split-balls.md).


## 8. Bounded novelty check and validation limits

On 2026-09-04, I searched the exact P-split name with orthogonal transformations,
rotations, coordinate dependence, Hausdorff error, and nonlinear relaxation
gaps, and searched more broadly for coordinate changes in disjunctive epigraph
convexification. No direct statement of the quantitative comparison above was
found. Searches returned mainly the original paper, its conference predecessor,
and work on different quadratic epigraph/indicator models. This limited search
does not establish priority or exhaust related lifting literature.

The primary sources are the [published P-split paper](https://doi.org/10.1007/s10107-025-02232-1)
and its [conference predecessor](https://arxiv.org/abs/2101.12708).
The published paper already explains that auxiliary sharing, variable grouping,
linking constraints, and disjunct-specific bounds affect strength. The proposed
contribution is the explicit unbounded quantitative separation and its survival
under every auxiliary-only convexification with the fixed epigraph map. The
capsule description and its second-order-cone representability are elementary
known geometry; those are not claimed as new.

All claims here have symbolic proofs. No numerical optimizer is needed for the
witness lifts or geometric distance bounds. The related axis-aligned ball note
has an independent 240-case LP comparison, but those tests do not constitute
a separate validation of every claim in this note.
