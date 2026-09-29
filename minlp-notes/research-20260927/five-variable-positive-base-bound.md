# Removing the positive-dimensional base in five variables

Date: 2026-09-28. Status: the proof passed a
[fresh independent blowup audit](quadratic-base-blowup-review.md) and
[fresh independent classification audit](five-variable-positive-base-classification-review.md),
as well as a [contributor audit](five-variable-positive-base-contributor-audit.md).
The [root review](five-variable-degree-root-review.md) additionally
reconstructed the complete proof and checked the cited primary
residual-intersection and minimal-degree statements.
The author and `one_parameter_spectrahedral_fields` are
co-contributors to the case analysis. No priority claim is made.

The argument below completes the sharp five-variable upper bound 21
for a rational sum of quadratic squares that is globally convex, has
a unique real zero, and has a positive definite Hessian there. It
addresses the positive-dimensional complex base left open by the
[finite residual argument](degree23-residual-obstruction.md).

The new step is a geometric reduction. If 23 or more simple isolated
zeros coexist with a positive-dimensional base having no real points,
the elementary weighted degree count confines that base to curves of
total degree at most four or surfaces of total degree at most two.
Every resulting case contains a small subvariety whose quadrics can
have at most 22 isolated simple zeros away from it. This is a
contradiction. The count uses generic perturbations of all quadrics
through the subvariety, so it does not assume that the original
equations have full normal rank along the positive base.

## 1. Statement for a quadratic linear system

Let \(\mathcal Q\) be a real vector space of homogeneous quadrics in
\(\mathbb P^5\). Let \(W\) be its full common zero set over
\(\mathbb C\). Assume that every positive-dimensional component of
\(W\) has no real points. Suppose that \(\Gamma\subset W\) consists
of \(D\) distinct points at which the gradients of \(\mathcal Q\)
have projective rank five.

**Theorem.** If \(D\geq23\), then \(W\) is
zero-dimensional.

The theorem does not assert that every selection of five equations
has finite intersection. Once \(W\) is finite, however, five generic
real linear combinations do form a proper quadratic complete
intersection and remain nonsingular at \(\Gamma\). If
\(\mathcal Q\) has a rational basis and \(\Gamma\) is a simple
Galois orbit, the combinations can be chosen rational.

The real vector space may be replaced by a rational vector space
extended to \(\mathbb R\). No assumption that the isolated points
are real is needed in this theorem.

## 2. The weighted degree count

Choose five generic real combinations \(h_1,\ldots,h_5\) from
\(\mathcal Q\). They can be chosen nonsingular at every point of
\(\Gamma\), and with no positive-dimensional intersection component
outside \(W\). For the latter statement, on
\(U=\mathbb P^5\setminus W\), a fixed point imposes five independent
linear conditions on the matrix of combination coefficients. The
incidence variety therefore has the same dimension as that coefficient
space, and its generic fibers are finite or empty. The two generic
conditions can be imposed simultaneously.

For completeness, the weighted Bézout construction starts with
\(\mathbb P^5\) and assigns a reduced irreducible variety the weight

\[
 w(X)=2^{\dim X}\deg X.
 \tag{1}
\]

Intersect with the five quadrics successively. A component contained
in the next quadric is retained. Otherwise replace it by the
components of its proper hypersurface intersection. Their total
weight is at most its former weight. Keep repeated components as
separate entries, which only overcounts their contributions. The initial weight is 32;
the final weight is at most 32. Each point of \(\Gamma\) contributes
at least one and cannot belong to a positive-dimensional component,
by the rank-five assumption. Thus

\[
 \sum_{X\text{ positive component of }W}
       2^{\dim X}\deg X\leq32-D\leq9.
 \tag{2}
\]

Distinct maximal components of \(W\) appear among the final
components because the positive intersection is contained in \(W\).
Discarding repeated entries only decreases the left side. This use
of degrees concerns reduced supports; it does not assume that the
original base scheme is reduced.

A projective variety defined over \(\mathbb R\) with odd degree has
a real point: intersect with generic real hyperplanes to obtain a
zero-dimensional scheme of odd length. Nonreal points contribute in
conjugate pairs. In particular, an invariant projective linear space
has real points.

It follows from (2) that the positive base has one of these forms:

- If it has a surface component, the sum of the degrees of its
  surface components is at most two. It contains either two conjugate
  planes or a real geometrically integral quadric surface.
- Otherwise all positive components are curves and the sum of their
  degrees is at most four. A real geometrically integral component
  has degree two or four. A component not fixed by conjugation has
  degree one or two, together with its conjugate.

There are no components of dimension at least three: a single
degree-one three-dimensional component would be invariant and have
real points, while every other possibility already has weight at
least 16. In the surface case, a degree-one invariant component is
likewise impossible. The two lists are about maximal components,
so curves contained in a surface are not counted again.

## 3. A perturbation lemma for a quadratic subbase

Let \(Y\subset\mathbb P^5_{\mathbb C}\) be a nonempty proper closed
reduced, pure-dimensional local complete intersection such that its
ideal sheaf \(\mathcal I_Y(2)\)
is globally generated. Let \(h_1,\ldots,h_5\) be any quadrics
vanishing on \(Y\), and suppose they have \(D\) distinct simple
common zeros outside \(Y\). Let

\[
 \pi:\widetilde{\mathbb P^5}=\operatorname{Bl}_Y\mathbb P^5
       \longrightarrow\mathbb P^5,
 \qquad M=2\pi^*H-E,
 \tag{3}
\]

where \(E\) is the exceptional divisor. Then

\[
 D\leq\int_{\widetilde{\mathbb P^5}}M^5
   =32-e(Y),
 \qquad
 e(Y)=\int_Y\left\{
       \frac{(1+2H)^5}{c(N_{Y/\mathbb P^5})}
                  \right\}_{\dim Y}.
 \tag{4}
\]

For disconnected \(Y\) of the same dimension, the integral is the
sum over its components.

In particular, an ideal generated by linear and quadratic forms has
\(\mathcal I_Y(2)\) globally generated. The quadratic generators
already give sections, and a linear generator is recovered locally
from its products with coordinates, one of which is nonzero at the
point under consideration.

Here are the reasons the lemma applies to an arbitrary original
five-tuple. Global generation makes \(M\) globally generated. Five
generic quadrics through \(Y\) give a zero-dimensional residual
intersection outside \(Y\), with length \(\int M^5\). This remains
valid if the blowup is singular. Equivalently, use the generic
residual-intersection formula of Eklund–Jost–Peterson, Theorem 3.2:
apply it to the homogeneous ideal generated by
\(H^0(\mathcal I_Y(2))\), which defines \(Y\) as a projective
scheme because of global generation. Its generators all have degree
two, even if this ideal is not saturated. For a local complete
intersection, the Segre class is \(c(N)^{-1}\cap[Y]\), giving (4).

At each original simple zero outside \(Y\), choose a small disjoint
complex analytic neighborhood disjoint from \(Y\). The implicit
function theorem preserves one common zero there for every
sufficiently small perturbation of the five coefficients. Generic
five-tuples of quadrics through \(Y\) are arbitrarily close to the
original tuple. Their residual length therefore is at least \(D\),
which proves the inequality. In particular, no positivity assertion
about an excess class of the original possibly nonreduced base is
being inferred from a formal normal-bundle calculation.

For a smooth connected curve of degree \(d\) and genus \(g\), the
normal bundle has degree \(6d+2g-2\), so

\[
 e(Y)=4d-2g+2.
 \tag{5}
\]

For the possibly reducible complete-intersection curves below, the
normal bundle is known directly and (4) avoids a smoothness assumption.

## 4. Surface components

Two distinct conjugate planes in \(\mathbb P^5\) must be disjoint.
If they intersect, their intersection is an invariant projective
linear space and hence has a real point in \(W\). Their disjoint
union \(Y\) has an ideal generated by quadratic products between
the two coordinate blocks. It is a smooth, possibly disconnected
local complete intersection. A plane has normal bundle
\(\mathcal O(1)^3\) in \(\mathbb P^5\), so

\[
 e(\mathbb P^2)
 =[H^2]\frac{(1+2H)^5}{(1+H)^3}=16.
\]

The union has \(e(Y)=32\), leaving no isolated simple points. One
can also see this directly: quadrics through two complementary
planes are bilinear in their coordinate blocks, and every zero
outside the planes lies on a line of zeros obtained by independently
scaling the blocks.

A real geometrically integral degree-two surface spans a
\(\mathbb P^3\) and is a quadric hypersurface there. If singular,
its singular locus is an invariant linear space, hence supplies a
real point. Thus the real-point-free case is smooth. Its ideal in
\(\mathbb P^5\) has generators of degrees \((1,1,2)\), and

\[
 e(Y)
 =2[H^2]\frac{(1+2H)^4}{(1+H)^2}=22.
\]

Consequently its quadrics have at most ten simple isolated common
zeros outside it. Both surface cases contradict \(D\geq23\).

## 5. Real curve components

A real geometrically integral conic is smooth and spans a plane.
Its ideal is generated by three linear forms and one quadric. Formula
(5), with \(d=2,g=0\), gives \(e(Y)=10\), so (4) bounds the
number of simple isolated zeros by 22.

Consider a real geometrically integral quartic curve \(C\). Its
linear span is real and has dimension at most four, since a
nondegenerate integral curve of degree four has span dimension at
most four.

If its span is a plane, every quadric containing it contains the
plane. This would put real points in \(W\), so this case is
impossible.

If its span is \(\mathbb P^3\), consider the space of quadrics
through \(C\) in that span. With no such quadric, the restrictions
of all elements of \(\mathcal Q\) are zero and the entire span is
in \(W\). With exactly one independent quadric, its whole quadric
surface is in \(W\). A real-point-free such surface is the surface
case already treated; otherwise it contradicts the assumptions.
If there are two independent quadrics, they have no common surface
component: a common linear factor would force the integral
nonplanar curve into a plane. Their complete intersection has degree
four and contains the reduced integral degree-four curve \(C\).
Equality of degrees, and the absence of embedded components in a
complete intersection, show that the intersection is precisely \(C\)
as a scheme. Thus \(C\subset\mathbb P^5\) has complete-intersection
type \((1,1,2,2)\). Its ideal is generated in degrees at most two,
and

\[
 e(C)=4[H]\frac{(1+2H)^3}{(1+H)^2}=16.
\]

This computation does not require the curve to be smooth.

If the span is \(\mathbb P^4\), an integral degree-four curve in
that span is a rational normal quartic. This is the curve case of
the classical classification of varieties of minimal degree. Over
\(\mathbb C\) it is smooth of genus zero, with ideal generated by
the quadratic minors of the standard catalecticant matrix; adjoining
the linear equation of its span proves global generation of
\(\mathcal I_C(2)\) in \(\mathbb P^5\). Formula (5) gives
\(e(C)=18\). This remains valid for a real form having no real
points, since the degree and normal-bundle calculation are over
\(\mathbb C\).

Every real quartic-curve case therefore leaves at most sixteen
simple isolated points, unless it has already reduced to a surface
case. This again contradicts \(D\geq23\).

## 6. Conjugate curve components

Two distinct conjugate lines must be disjoint, since otherwise their
intersection point is real. Their union has an ideal generated in
degrees at most two: in their \(\mathbb P^3\) span its equations are
the products between two coordinate blocks, and the span contributes
linear equations. Each line has \(e=6\) by (5), so their union has
\(e=12\) and leaves at most twenty simple isolated points.

It remains to treat a pair of conjugate conics \(C,\overline C\).
Let \(P,\overline P\) be their planes.

If the planes coincide, that common plane is real. A quadratic
restriction vanishing on both distinct integral conics must be zero.
All quadrics in \(\mathcal Q\) would therefore vanish on the real
plane, a contradiction.

If the planes are disjoint, the conics are disjoint. Their union
has an ideal sheaf generated by quadrics: use the products between
the two coordinate blocks, together with the conic equations in
the respective blocks. Each conic has \(e=10\), so their union
has \(e=20\) and leaves at most twelve simple isolated points.

If the planes meet at a point \(a\), that point is real and is not
on either conic. The union of the planes spans \(\mathbb P^4\).
Over \(\mathbb C\), choose coordinates there such that

\[
 P=V(x_3,x_4),\quad
 \overline P=V(x_1,x_2),\quad a=[1:0:0:0:0].
\]

Normalize the conic equations \(c(x_0,x_1,x_2)\) and
\(c'(x_0,x_3,x_4)\) to have coefficient one on \(x_0^2\).
The four products \(x_i x_j\), \(i\in\{1,2\}\),
\(j\in\{3,4\}\), define the union of the planes. Adding the
quadric

\[
 c+c'-x_0^2
\]

cuts out the two conics as a projective scheme. Locally this assertion
is immediate away from \(a\), where the planes are disjoint; at
\(a\) the added quadric is nonzero, so that point is excluded.
Hence the ideal sheaf of the disjoint union is generated by quadrics,
even if a displayed homogeneous generating ideal needed saturation.
The contribution is again 20.

Finally suppose that the planes meet along a line. Their span is a
real \(\mathbb P^3\), and their union is a real quadric surface
\(Q_0\), the product of their linear equations. Some real
\(q\in\mathcal Q\) must restrict nontrivially to \(P\);
otherwise every quadric in \(\mathcal Q\) vanishes on both planes
and on their real line of intersection. By conjugation, \(q\)
restricts nontrivially to both planes. Its restrictions are scalar
multiples of the two defining conic equations. The proper complete
intersection

\[
 Y=V(Q_0,q)\subset\mathbb P^3
\]

is exactly the reduced union \(C\cup\overline C\): its two
degree-two components account for its full degree four, each with
generic multiplicity one, and a complete intersection has no embedded
components. It is a local complete intersection even when the conics
meet. Its ideal in \(\mathbb P^5\) has type \((1,1,2,2)\), so
\(e(Y)=16\), leaving at most sixteen simple isolated points.

All cases contradict \(D\geq23\), completing the theorem.

## 7. Consequence for convex rational SOS quartics

Let

\[
 F=\sum_jq_j^2,
 \qquad q_j\in\mathbb Q[x_1,\ldots,x_5],
 \qquad \deg q_j\leq2,
\]

be globally convex, with real zero set \(\{p\}\) and
\(\nabla^2F(p)\succ0\). The rank of the quadratic Jacobian at
\(p\) is five. The existing degree argument gives a simple Galois
orbit of odd degree \(D\leq31\).

If the leading quartic form has a real nonzero zero direction, the
rational flat-direction reduction in
[the degree note](quartic-zero-degree-adversarial.md) preserves the
coordinate field and reduces to at most four variables. The ordinary
quadratic Bézout bound there is at most 16, already less than 21.

Otherwise homogenize the quadratic factors. Their full common real
projective zero set is \(\{p\}\), and \(p\) is isolated even
over \(\mathbb C\). Therefore every positive-dimensional complex
base component has no real point. If \(D\geq23\), the theorem
above forces the full base to be finite. Five generic rational
combinations define a proper complete intersection and remain simple
at the orbit. The
[odd-residual obstruction](degree23-residual-obstruction.md) then
rules out all odd \(D\geq23\). Thus

\[
 [\mathbb Q(p):\mathbb Q]\leq21.
\]

The [cyclic construction](cyclic-quartic-exponential-degree.md) reaches
degree 21 with global strong convexity and rational quadratic squares,
so the upper bound is exact for the stated class. It does not
bound arbitrary rational convex quartics without a rational SOS
representation. It gives an exact arithmetic limitation and a sharp
construction target, without claiming a solver speedup.

## 8. Sources, scope, and verification

- Eklund, Jost, and Peterson,
  [*A method to compute Segre classes of subschemes of projective space*](https://arxiv.org/pdf/1109.5895),
  Theorem 3.2, its proof, Remark 3.3, and Section 2.3 were examined.
  The theorem gives the generic residual degree for an ideal generated
  by quadrics. The proof uses a blowup without requiring it to be
  smooth; its generic residual avoids the exceptional divisor in the
  zero-dimensional case. This is the primary source for (4).
- Eisenbud, Green, Hulek, and Popescu,
  [*Small schemes and varieties of minimal degree*](https://arxiv.org/pdf/math/0404517),
  Theorems 0.1–0.2, state the classical minimal-degree classification
  and its regularity characterization. Only the familiar integral
  curve case, a rational normal curve, is needed above. No claim
  about arbitrary nonreduced minimal-degree schemes is used.
- The weighted count and generic-selection argument are reconstructed
  here and in [the earlier degree note](quartic-zero-degree-adversarial.md).
  They concern the full base of \(\mathcal Q\), followed by a generic
  five-equation intersection, not an arbitrary initially selected
  five-tuple.

The [primary-source audit](small-residual-and-excess-prior.md) also
records the corresponding Fulton–Lazarsfeld positivity bound and
compares the exact residual-intersection hypotheses. The separate
[priority comparison](five-variable-degree21-prior.md) examined the
closest Cayley–Bacharach, convex-quartic, rational-SOS, and optimization
degree results. It did not locate an equivalent theorem in those
sources, but that bounded search does not establish novelty. The
candidate contribution is the sharp arithmetic extremum obtained by
combining the real residual argument and the low-degree base analysis;
the component intersection formulas and duality tools are classical.

The independent reviews checked completeness of the low-degree case
list, global generation for the unions of conics, and the deformation
argument that transfers a generic residual count to isolated simple
zeros of a special system. Nonreduced structure of
the actual positive base is bypassed by choosing reduced local
complete-intersection subvarieties \(Y\) inside it. Every point of
\(\Gamma\) is disjoint from \(Y\), since it is isolated by the
Jacobian rank. No normal-rank or transversality assumption on the
original equations along \(Y\) is made.

The retained checker
[check_five_variable_positive_base.py](check_five_variable_positive_base.py)
checks the Chern-series arithmetic in the table of cases and an
explicit quadratic description of two conics whose planes meet at
an external point. It does not verify the universal classification,
minimal-degree theorem, or residual-intersection theorem. The fresh
reviews linked at the opening independently checked the geometric case
list and the perturbation lemma, including the singular-blowup case.
The latter review identified the need to say that the center in the
general lemma is pure-dimensional; this was corrected and all actual
centers already satisfy the condition. The root agent then independently
reconstructed the full proof and directly checked the primary
residual-intersection theorem and minimal-degree facts. The root read
did not rerun the checker. These reviews do not establish priority.

The absence of real points on positive components is essential.
Generic five quadrics through a real line have 26 simple residual
points, since a line has contribution six. Generic five quadrics
through a smooth real conic without real points have 22 simple
residual points. These facts concern generic geometric counts; they
make no claim that a rational residual is irreducible or has exactly
one real embedding.

Targeted commands actually run:

- `python research-20260927/check_five_variable_positive_base.py`:
  the first invocation found an invalid SymPy `extension=False`
  option in the checker. After specifying the exact coefficient
  fields directly, the full checker passed. This was a checker API
  error, not a failed mathematical assertion.
- A local Python structural check of this note and the residual note:
  local links, paired display delimiters, control characters, and
  trailing whitespace passed.

No project-wide verification or CI inspection was performed.
