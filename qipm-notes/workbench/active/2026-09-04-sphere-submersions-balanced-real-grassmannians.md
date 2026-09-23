# Sphere submersions onto balanced real Grassmannians

Status: Proved; independently audited; literature-backed  \
Started: 2026-09-04  \
Paper status: Not incorporated  \
Confidence: High

## Classification

Put

\[
 B_r=\operatorname{Gr}_{\lfloor r/2\rfloor}(\mathbb R^r)
\]

and let \(\widetilde B_r\) be the oriented Grassmannian.  The following
classification includes arbitrary connected finite covers of \(B_r\).

1. For every \(r\geq4\), there is no proper \(C^1\) submersion
   \[
   S^n\longrightarrow B_r
   \]
   for any \(n\), and none onto \(\widetilde B_r\) or any other connected
   finite cover.
2. For \(r=3\), \(B_3=\mathbb {RP}^2\) and
   \(\widetilde B_3=S^2\).  The only possible dimensions are \(n=2,3\),
   and both occur:
   \[
   S^2\to S^2,\qquad S^3\to S^2
   \]
   by the identity and complex Hopf map, and
   \[
   S^2\to\mathbb {RP}^2,\qquad
   S^3\to S^2\to\mathbb {RP}^2
   \]
   by composing with the antipodal covering.
3. For \(r=2\), both the ordinary and oriented line Grassmannians are
   circles.  Proper submersions \(S^1\to S^1\) are the usual nonzero-degree
   covering maps, while no \(S^n\to S^1\) exists for \(n\geq2\).
4. The degenerate \(r=1\) target is a point, so every map to it is a
   submersion in the zero-dimensional convention.

In particular, a single normalized real state sphere cannot smoothly and
everywhere regularly parameterize the balanced rank-\(\lfloor r/2\rfloor\)
projector orbit once \(r\geq4\).  This obstruction allows arbitrary compact
fibers; it does not assume that the fiber is a sphere.

## From \(C^1\) submersions to sphere-total-space bundles

A submersion from a compact manifold to a connected manifold has open and
closed image, hence is onto and proper.  A \(C^1\) submersion on the compact
sphere has a uniform positive surjectivity margin for its derivative.
Smooth approximation in the \(C^1\) topology therefore produces a smooth
submersion to the same target.  Its image is again open and closed.  It is
enough to exclude smooth proper submersions.

Ehresmann's theorem makes such a map a locally trivial bundle

\[
 F\longrightarrow S^n\longrightarrow B.
 \tag{1}
\]

For \(n\geq2\), the map lifts through every connected covering
\(\widehat B\to B\).  The lift is still a submersion, and its compact image
is open and closed in \(\widehat B\), so it is onto.  Thus it is enough to
work with the universal oriented cover.

For \(r\geq3\), \(\widetilde B_r\) is simply connected.  The homotopy exact
sequence of (1) then shows that \(F\) is connected.  This is the point at
which disconnected fibers over the ordinary Grassmannian are handled:
after lifting to the oriented cover, the relevant fiber component is
connected.

## Browder and the Gysin obstruction

Assume first that the fiber has positive dimension.  Browder's theorem
applies to an arbitrary polyhedral base and arbitrary connected finite
polyhedral fiber:

> If \(F\to S^n\to B\) is a fiber bundle with nontrivial base and connected
> fiber, then \(F\) has the homotopy type of \(S^1,S^3\), or \(S^7\).

This is a conclusion, not an assumption about the fiber.  Write
\[
 q=\dim F\in\{1,3,7\},\qquad h=q+1\in\{2,4,8\}.
\]

The mod-two Gysin sequence now determines the entire cohomology of the base.
If \(e\in H^h(B;\mathbb F_2)\) is the transgression of the fiber class, then
cup product with \(e\) is an isomorphism through the base degrees
\(0<i\leq\dim B<n\).  Consequently, for some \(a\geq1\),

\[
 H^*(B;\mathbb F_2)
 \cong
 \mathbb F_2[e]/(e^{a+1}),
 \qquad |e|=h,
 \tag{2}
\]

\[
 \dim B=ah,\qquad
 n=(a+1)h-1,\qquad
 \chi(B)=a+1=\frac{\dim B}{h}+1.
 \tag{3}
\]

For completeness, (2) follows directly from exactness: cohomology vanishes
in degrees \(0<i<h\); multiplication by \(e\) then recursively generates a
one-dimensional group in degrees \(h,2h,\ldots,ah\) and zero in every other
degree.  Poincare duality puts the last nonzero power in the top degree.

The primary source is [Browder, *Fiberings of spheres and H-spaces which are
rational homology spheres*, Theorem 1, Bull. AMS 68 (1962),
202--203](https://doi.org/10.1090/S0002-9904-1962-10747-2).  Browder proves
that the fiber is first a mod-two homology sphere, invokes the Hopf-invariant
restriction, removes odd torsion, and concludes the stated homotopy types.
That two-page article is a published theorem announcement and proof sketch;
it points to Browder's longer differential-Hopf-algebra and higher-torsion
work for the underlying arguments.

## Euler characteristic of the oriented Grassmannian

Write \(p=\lfloor r/2\rfloor\), \(s=\lceil r/2\rceil\), so
\(\dim\widetilde B_r=ps\).  The Hopf--Samelson equal-rank formula, or the
equivalent Weyl-group calculation for

\[
 SO(p+s)/(SO(p)\times SO(s)),
\]

gives, for \(0<p<r\),

\[
 \chi(\widetilde B_r)=
 \begin{cases}
 0,&p,s\text{ both odd},\\[2mm]
 2\binom{\lfloor r/2\rfloor}{\lfloor p/2\rfloor},
   &\text{otherwise}.
 \end{cases}
 \tag{4}
\]

The factor two is also immediate from the connected double cover of the
ordinary Grassmannian.  Formula (4) can be checked directly from
\(|W_{SO(r)}|/|W_{SO(p)}||W_{SO(s)}|\) in the equal-rank case; unequal rank
has Euler characteristic zero.

We compare (4) with the necessary value in (3).

### Even \(r=2m\)

Here \(p=s=m\) and the dimension is \(m^2\).

- If \(m\) is odd, the dimension is odd and cannot equal \(ah\) for even
  \(h\).  Equivalently, (4) gives Euler characteristic zero.
- If \(m\) is even,
  \[
  \chi(\widetilde B_r)=2\binom m{m/2}.
  \]
  For \(m=2\), this is \(4\), whereas \(m^2/h+1\) is \(3\) or \(2\) for
  the divisors \(h\in\{2,4,8\}\).  For every even \(m\geq4\),
  \[
  2\binom m{m/2}>\frac{m^2}{2}+1
  \geq\frac{m^2}{h}+1.
  \tag{5}
  \]
  The first inequality starts with \(12>9\) at \(m=4\) and follows by the
  two-step central-binomial recurrence
  \[
  \frac{\binom{m+2}{(m+2)/2}}{\binom m{m/2}}
  =\frac{4(m+1)}{m+2}.
  \]

Thus no even \(r\geq4\) survives (3).

### Odd \(r=2m+1\)

Now \(\dim\widetilde B_r=m(m+1)\) and

\[
 \chi(\widetilde B_r)=
 2\binom m{\lfloor m/2\rfloor}.
 \tag{6}
\]

For \(m\geq4\), the two parity versions of the same two-step recurrence give

\[
 2\binom m{\lfloor m/2\rfloor}>
 \frac{m(m+1)}2+1
 \geq \frac{m(m+1)}h+1.
 \tag{7}
\]

The two initial checks are \(12>11\) at \(m=4\) and \(20>16\) at \(m=5\).
For \(m=3\), the left side of (6) is \(6\), whereas the possible right sides
of (3) are \(7\) for \(h=2\) and \(4\) for \(h=4\).

Only two numerical cases survive:

\[
 (m,r,h)=(1,3,2),\qquad (2,5,2).
 \tag{8}
\]

The first is \(\widetilde B_3=S^2\), which gives the counterexamples listed
above.

## The apparent \(r=5\) exception fails mod two

There is a standard diffeomorphism

\[
 \widetilde{\operatorname{Gr}}_2(\mathbb R^5)\cong Q^3,
 \tag{9}
\]

where \(Q^3\subset\mathbb {CP}^4\) is the smooth complex quadric.  An
oriented orthonormal pair \((u,v)\) is sent to the isotropic line
\([u+iv]\); the inverse takes the oriented real and imaginary parts.

The quadric has one integral cohomology generator in each of degrees
\(0,2,4,6\).  If \(x\in H^2(Q^3;\mathbb Z)\) is the hyperplane class and
\(y\in H^4(Q^3;\mathbb Z)\) is the complementary generator normalized by
\(\int_{Q^3}xy=1\), then

\[
 x^2=2y.
 \tag{10}
\]

Indeed, \(Q^3\) has projective degree two, so
\(\int_{Q^3}x^3=2\); since \(\int x\,y=1\), (10) follows.  Reducing mod two
gives \(x^2=0\).  This contradicts (2) with \(h=2,a=3\), which requires the
square of the unique nonzero degree-two class to generate degree four.
Thus \(r=5\) is excluded even though its dimension and Euler characteristic
alone imitate \(\mathbb {CP}^3\).

## Zero-dimensional fibers

If \(n=\dim B\), a proper submersion is a covering map.  For \(n\geq2\), its
lift to the simply connected oriented Grassmannian would be a diffeomorphism
from a sphere.  This is impossible for \(r\geq4\):

- \(r=4\) gives
  \(\widetilde{\operatorname{Gr}}_2(\mathbb R^4)\cong S^2\times S^2\);
- \(r=5\) is the quadric above; and
- for \(r\geq6\), with \(p,s\geq3\), the homogeneous-space homotopy sequence
  gives
  \[
  \pi_2(\widetilde B_r)
  =
  \ker\!\left[
  \pi_1(SO(p))\oplus\pi_1(SO(s))
  \longrightarrow\pi_1(SO(r))
  \right]
  \cong\mathbb Z_2,
  \]
  while \(\pi_2(S^{ps})=0\).

For \(r=2\), if \(n\geq2\), a map \(S^n\to S^1\) lifts to
\(\mathbb R\).  A lifted submersion would have compact image that is both
open and closed in \(\mathbb R\), an impossibility.  The \(n=1\) coverings
remain.

## Scope

The obstruction concerns everywhere-regular proper maps.  It does not rule
out surjective maps with critical points, charts with singular seams,
randomized encodings, maps from products or Stiefel manifolds, or
parameterizations of a proper subset of the projector orbit.  Those are the
relevant escape routes for saturated PSD-slack constructions.
