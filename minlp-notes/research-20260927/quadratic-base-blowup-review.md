# Independent review of the quadratic-base blowup bound

Date: 2026-09-28. Reviewed independently of the construction in
[the positive-base draft](five-variable-positive-base-bound.md).
Scope: Section 3's perturbation lemma, its intersection signs, and
the centers and counts used in Sections 4–6. This review does not
independently certify the full classification in Section 2 or the
previous finite-residual theorem.

The blowup inequality is correct. Singularities of the center or
blowup, nonreduced structure of the original common-zero scheme,
and deficient normal rank of the original five equations do not
invalidate it. All seven proposed numerical values are correct.
The author corrected the one statement-level clarification found
in this review: the center is now explicitly pure-dimensional,
as required when its contribution uses a single degree component
indexed by \(\dim Y\). Every center used already had this property.

## A direct justification of the perturbation step

Write \(X=\operatorname{Bl}_Y\mathbb P^5\),
\(L=\pi^*\mathcal O(2)\otimes\mathcal O_X(-E)\), and
\(V=H^0(\mathbb P^5,\mathcal I_Y(2))\). The evaluation map gives

\[
V\otimes\mathcal O_X\twoheadrightarrow L.
\]

Thus the quadrics in \(V\), viewed as sections after removing one
copy of the exceptional divisor, generate \(L\). One does not
need the original five sections to generate it. The blowup is an
integral projective fivefold, is unchanged outside \(Y\), and has
an effective Cartier exceptional divisor. These assertions do not
require a smooth center; see
[Stacks, Section 31.33](https://stacks.math.columbia.edu/tag/01OF).

Let \(T=V^5\) parametrize five-tuples. At a fixed point of \(X\),
vanishing of all five sections imposes five independent linear
conditions on \(T\). Therefore the universal zero incidence over
\(X\) has dimension \(\dim T\), and the incidence over \(E\)
has dimension at most \(\dim T-1\). Projectivity makes the image
of the latter incidence closed. A generic tuple consequently has
no zero anywhere on \(E\).

The full incidence either fails to dominate \(T\), giving an
empty generic zero scheme, or has zero-dimensional generic fiber.
On \(X\setminus E\cong\mathbb P^5\setminus Y\), the incidence
is a vector bundle over a smooth variety. Generic smoothness in
characteristic zero makes that zero-dimensional generic fiber
reduced. Thus a generic tuple has finitely many simple zeros, all
on the smooth complement of \(E\). The top-Chern zero formula
gives their number as

\[
\deg\bigl(c_5(L^{\oplus5})\cap[X]\bigr)=\int_Xc_1(L)^5.
\]

This formula only needs a regular zero scheme at its points, not a
smooth ambient blowup; its precise form is
[Stacks, Lemma 42.44.1](https://stacks.math.columbia.edu/tag/0FA9).
If the morphism defined by \(V\) has image dimension below five,
the generic zero scheme is empty and the integral is zero.

For the original five-tuple, take disjoint analytic neighborhoods
of its \(D\) simple zeros outside \(Y\). The complex implicit
function theorem preserves one zero in each neighborhood under
every sufficiently small perturbation in \(T\). The generic good
tuples form a nonempty Zariski open subset and are therefore
arbitrarily close to the original tuple. Hence

\[
D\leq\int_X(2H-E)^5.
\]

No flatness assertion about the original whole zero scheme is
needed. In fact, this inequality only needs global generation of
\(\mathcal I_Y(2)\); the local-complete-intersection condition is
used to express the integral through the normal bundle.

## Intersection signs and numerical values

For a pure local-complete-intersection center of codimension \(r\),
let \(i:Y\hookrightarrow\mathbb P^5\) and
\(N=(\mathcal I_Y/\mathcal I_Y^2)^\vee\). Then

\[
\pi_*E^k=0\quad(1\leq k<r),\qquad
\pi_*E^{r+j}=(-1)^{r+j-1}i_*s_j(N),
\quad s(N)=c(N)^{-1}.
\]

These signs follow from
\(E=\mathbb P(\mathcal I_Y/\mathcal I_Y^2)\),
\(\mathcal O_E(E)=\mathcal O_E(-1)\), and projective-bundle
pushforward. These facts apply to singular regular embeddings;
see [Stacks, Lemma 42.59.11](https://stacks.math.columbia.edu/tag/0FVA),
[Lemma 42.36.1](https://stacks.math.columbia.edu/tag/02TW), and
[the projective-bundle Chern relation](https://stacks.math.columbia.edu/tag/02U0).

For a curve, in particular,
\(\pi_*E^4=-[Y]\) and \(\pi_*E^5=-i_*c_1(N)\). Thus

\[
\int_X(2H-E)^5=32-10d+\deg N=30-4d+2p_a(Y).
\]

The second equality uses adjunction
\(\det N=\omega_Y\otimes\mathcal O_Y(6)\) and
\(p_a(Y)=1-\chi(\mathcal O_Y)\). It remains valid for singular,
reducible, or disconnected pure lci curves. The identity
\(\deg\omega_Y=-2\chi(\mathcal O_Y)\) in this generality is
[Stacks, Lemma 53.5.2](https://stacks.math.columbia.edu/tag/0BS6).
In particular, two disjoint rational curves have arithmetic genus
\(-1\), not zero.

For a surface the corresponding expression is

\[
32-40\deg Y+10\int_YHc_1(N)
   -\int_Y\bigl(c_1(N)^2-c_2(N)\bigr).
\]

| Center in \(\mathbb P^5\) | Data used | \(\int_X(2H-E)^5\) |
| --- | --- | ---: |
| Smooth conic | \(d=2,p_a=0\) | 22 |
| Two disjoint lines | \(d=2,p_a=-1\) | 20 |
| \((2,2)\) curve in \(\mathbb P^3\) | \(d=4,p_a=1\) | 16 |
| Rational normal quartic | \(d=4,p_a=0\) | 14 |
| Two disjoint smooth conics | \(d=4,p_a=-1\) | 12 |
| Smooth quadric surface in \(\mathbb P^3\) | \(N=\mathcal O(1)^2\oplus\mathcal O(2)\) | 10 |
| Two disjoint planes | \(N=\mathcal O(1)^3\) on each plane | 0 |

The table gives intersection numbers. Their use as bounds still
requires global generation in each embedding.

## Global generation and the actual centers

Disjoint conics do not satisfy that hypothesis in every embedding.
If their planes meet in a line and their conic intersections with
the line are disjoint, the binary quadratic restrictions cannot
be proportional. Every quadric containing both conics must then
contain both planes. If the planes meet at a point on exactly one
conic, every containing quadric contains the other whole plane.
Both configurations fail global generation.

Section 6 avoids these cases correctly. It uses disjoint planes,
or planes meeting at a point outside both conics, where its
displayed quadratic equations generate the required ideal sheaf.
For planes meeting along a line, the available real quadric with
nonzero restriction to both planes gives a proper \((2,2)\)
complete intersection. Its two conics account for the whole
degree, and the complete intersection has no embedded components,
so it is their reduced scheme-theoretic union. Its possible
singularities cause no problem for the lemma.

The other centers in Sections 4–6 have ideals generated in degrees
at most two. Multiplying any linear generators by all coordinates
shows that their ideal sheaves twisted by two are globally
generated. No additional transversality along any center is needed.

Verification: the formulas and seven values above were recomputed
directly from projective-bundle pushforward and the displayed
normal bundles. The primary sources linked above were checked.
After reading the retained checker, the targeted command
`python research-20260927/check_five_variable_positive_base.py`
passed: all seven values and the two explicit conic-union ideal
equalities agreed. Those examples support the equations but do
not replace the general argument above. The targeted command
`git diff --check -- research-20260927/quadratic-base-blowup-review.md`
also passed. No project-wide checks or CI inspection were performed.
