# Fresh adversarial review of unbounded mixed-integer conic optimization

Date: 2026-09-28. Reviewed manuscript:
[unbounded-misocp-multiple-integer-frontier.md](unbounded-misocp-multiple-integer-frontier.md).
I did not develop this proof. I independently read the complete manuscript,
including the general coefficient-sensitive theorem and the subsequently
added qualitative Section 4.4. I also read the compressed-projection
dependency, the earlier review records, and the relevant primary geometric
and arithmetic statements. A fresh separate reviewer saved a detailed
[general-height audit](bounded-forms-height-independent-audit.md) and
obtained a further independent lattice-height check. I reread its explicit
minor, polynomial-reduction, and unimodular-parametrization arguments.

**Finding:** no substantive gap was found. The bounded-form descent proves
the finite-value encoding bound, including nonattainment. Together with
the separately reviewed decision and attained-fiber bounds, it gives the
stated exact optimization algorithm for fixed integer dimension and
continuous Hessian span. The general theorem retains linear dependence
on individual input coefficient bit length. No mathematical correction
was required during this review.

This is proof and scope review, not a formalization or priority finding.
In particular, it does not promote the fixed-parameter polynomial bound
in \((k,h)\) to an FPT running-time bound.

## 1. The geometric argument works with strict, nonclosed sublevels

Let \(\alpha\) and \(\theta\) denote the real and mixed-integer
infima, and choose a finite rational cap \(U>\theta\) containing
an improving integer point. For \(\alpha<s<t\), an anchor with
objective \(L<s\) and one fixed \(\lambda>0\) satisfying
\((1-\lambda)L+\lambda t<s\) contract every point of \(C_t\)
into \(C_s\). A two-sided bound on a linear form over \(C_s\)
therefore gives one over \(C_t\). The same contraction works for all
points; the witnesses in the eliminated continuous coordinates need not
be bounded or selected continuously.

This proves level independence of the real linear space of bounded
forms, also when \(\alpha=-\infty\). One-sided bounds would not
give a linear space and are not what the manuscript uses.

If \(C_U\) is full-dimensional, every \(C_t\) with
\(\alpha<t<U\) is full-dimensional. Contract a projected open ball
in \(C_U\) toward an anchor below \(t\). Witness objectives for the
entire ball are below the same finite \(U\), so a single positive
contraction factor suffices. No uniform bound on the witnesses themselves
is needed.

Suppose \(\alpha<t<\theta\). Then \(C_t\) contains no integer
point. For a full-dimensional convex set,
\(\operatorname{int}\overline{C_t}=\operatorname{int}C_t\subseteq C_t\).
Consequently its closure is lattice-free in the interior sense required
by the structural theorem. Integer points on the closure's boundary do
not invalidate this assertion. This is why a nonclosed projection creates
no gap here.

I inspected Theorem 2(i) and Corollary 17 in the
[Basu--Conforti--Cornuejols--Zambelli author manuscript](https://personal.lse.ac.uk/zambelli/papers/lattice-free.pdf),
PDF pages 2 and 13. They give maximal containment and the form
\(P+L\), with bounded polytope \(P\) and rational linear space
\(L\), in the full-dimensional case. Here \(L\) is proper, since
the whole ambient space is not lattice-free. A nonzero rational vector
orthogonal to \(L\) is bounded in both directions on \(P+L\).
Level independence then contradicts a zero rational part of the
bounded-form space. Thus the no-rational-bounded-form branch correctly
gives \(\theta=\alpha\).

The theorem is used only to establish existence of a rational bounded
form. No uncontrolled coefficient size of a maximal lattice-free facet
is imported into the arithmetic argument.

## 2. Every descent step retains the infimum

The full-dimensional hypothesis cannot be omitted. The manuscript checks
affine dimension before the bounded-form dichotomy, including after each
restriction. This order resolves the irrational-line failure case.

When \(C_U\) has smaller affine dimension, sample one nonzero
algebraic affine equation containing it. Its coefficients lie in one
specified number field. For rational, hence integer, \(z\), expansion
in a rational field basis converts that equation into rational affine
equations. At least one expanded equation has a nonzero normal, because
the original normal was nonzero. All improving integer points satisfy
every expanded equation. The presence of such a point also excludes an
inconsistent constant equation.

Selecting one nonzero equation and parametrizing all its integer solutions
reduces the integer dimension. This parametrization must describe the
full affine integer lattice, not merely an arbitrary finite-index
sublattice. Hermite or Smith normal form supplies the required one.
Restricting the entire original model to that lattice retains every
integer point below \(U\), so its infimum is still \(\theta\).
Points at larger objective values are immaterial to this implication.

In the full-dimensional case with a bounded integer form \(a\), its
range on \(C_U\) is bounded. A mixed-integer minimizing sequence has
only finitely many possible values of \(a^Tz\) below the cap. Some
value occurs infinitely often, and that subsequence still approaches
\(\theta\). The corresponding slice has infimum exactly
\(\theta\): restriction cannot lower it, while the subsequence
supplies the opposite inequality. Attainment within that slice is not
assumed.

There is no enumeration of the possible slice values in the algorithm.
The argument establishes that one value and a parametrization of
controlled encoding length exist. At most \(k\) restrictions are
needed. Integer-only affine substitutions preserve the continuous
Hessian blocks. At a terminal stage, the finite real infimum is bounded
using the compressed formula; the proof never replaces the parameter
\(h\) by the potentially much larger full Hessian span.

## 3. The arithmetic bounds use individual atoms, not formula length

I directly inspected Khachiyan--Porkolab's
[primary paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
printed pages 208 and 211--212. Proposition 2.1 separates output formula
size from each atom's degree and coefficient bits. Proposition 2.2 and
Corollary 2.3 provide one common-field sample with corresponding
atom-count-independent representation bounds. Theorem 1.1 provides the
integer witness bound; the preceding paragraph reduces feasibility to
that theorem. These conclusions are linear in the input coefficient bit
bound. Their computation time depends on the number of atoms, and the
review does not discard that dependence.

The formulas for bounded forms, affine normals, and simultaneous basis
vectors use only a number of extra variables depending on \((k,h)\).
Sampling all basis vectors together supplies a common field directly;
there is no multiplication of independent sample-field degrees.
From a sampled real basis of a linear space, field linear algebra gives
an annihilating matrix. Because its entries lie in a real algebraic
field, its real kernel is exactly the original real span. Expanding
that matrix in a power basis gives rational equations whose rational
kernel is exactly the desired rational part.

The individual degree and bit bounds suffice even when the compressed
formula has exponentially many atoms. For an endpoint of a nonempty
one-dimensional semialgebraic image, some nonzero atom in a quantifier-free
description must vanish there. Otherwise all its finitely many signs are
constant in a neighborhood and the point is not a boundary. Identically
zero atoms can be discarded. This argument applies to open endpoints,
closed endpoints, and singleton images.

For a bounded linear form, it bounds both finite endpoints and hence all
integer slice values by a root bound. For the terminal real objective,
it bounds the finite infimum whether or not the endpoint belongs to the
image. These are existence bounds; no large projected formula is
constructed by the final optimization algorithm.

## 4. The general theorem preserves linear dependence on height

For a convex upward set \(E\), any mixed-integer feasible pair can have
its last coordinate increased to an integer. Thus a fully integral pair
exists, and the integer witness bound supplies a cap with controlled bit
length independently of the unknown optimum. Strict or missing boundary
points do not obstruct this upward-closure argument.

Let the original atom degree be \(d\ge2\) and individual coefficient
bits be \(H\). Each bounded-variable elimination and common-field
sample has degree \(d^{O_k(1)}\) and coefficient bits
\((H+1)d^{O_k(1)}\). The basis determinant introduces degree depending
only on \(k\), which is absorbed into the same form. The number of
atoms does not enter these individual bounds.

The remaining arithmetic also preserves linear dependence on \(H\).
For example, inversion of a nonzero field element can be performed by a
rational multiplication matrix of size bounded by the field degree.
Determinant bounds multiply coefficient bits by that size and add
dimension terms; they do not raise the bit bound to a parameter-dependent
power. The rational-part system has only \(k\) columns, so its basis
requires determinants of at most \(k\) independent rows. Clearing
denominators adds a bounded multiple of the existing bit bound.

An integer equation with coefficient bits \(L\) admits a particular
integer solution and a basis of its full integer kernel with bits
\(\operatorname{poly}(k)(L+1)\). This follows from standard lattice
determinant bounds or constructive gcd and Hermite-normal-form bounds.
It is a coefficient-size assertion stronger than merely saying that an
algorithm runs in polynomial time.

Under \(z=z_0+Ty\), carried original polynomials retain degree
\(d\). Polynomial expansion adds coefficient bits linear in the
entry-bit bound of \(z_0,T\), times a function of \(d,k\).
Carrying the transformed original atoms, rather than intermediate
elimination output, avoids a repeated increase in degree. After at most
\(k\) steps, the final endpoint has degree \(d^{G(k)}\) and
coefficient bits \((H+1)d^{G(k)}\) for an effective function \(G\).
Minimal-polynomial factor bounds preserve this form.

If that value is attained, its minimal polynomial and isolating interval
specify it using one extra real variable. Root separation gives interval
bits of the same linear-in-\(H\) form. The resulting optimal integer
projection is convex, and its integer witness bound has the claimed
form after increasing \(G\). This separate step does not infer
attainment from finite infimum.

## 5. Exact classification and attainment use the correct boxes

The finite-value bound supplies a threshold below every possible finite
infimum. Exact rational feasibility at that threshold therefore detects
unboundedness below. It does not compare integer and real unboundedness,
and it needs neither a rational ray nor an integer escape curve.

For a finite value, rational threshold bisection provides certified
approximations. If an unattained infimum equals a midpoint, the threshold
is infeasible, but retaining it as the lower endpoint still encloses the
value. The established recognition theorem then supplies the minimal
polynomial and selected real root from the proved degree and height bounds.

For attainment, the integer witness theorem is applied to the real convex
projection at the now specified algebraic value. This set may be
nonclosed or lower-dimensional; the cited theorem allows both. If an
integer point exists there, it has a bounded encoding. Its original
continuous fiber still has rational data and a rational affine objective,
so the separate attained-optimizer theorem bounds some continuous
optimizer without receiving algebraic objective coefficients.

The two conditional optimizer boxes are enough: if attainment holds,
they retain an optimizer; their intersection with the original closed
model is compact. Thus equality of its attained boxed value with the
original infimum characterizes attainment. Compact boxed value queries
also select an attained optimal integer fiber. Comparing unboxed fiber
infima would not suffice. Final continuous recovery takes place in that
selected rational fiber.

The sizes of all constructed boxes and threshold queries are polynomial
for fixed \((k,h)\). Repeated composition can enlarge the exponent
depending on those parameters, as the manuscript states. The general
height theorem is an encoding result, not by itself an algorithm for an
arbitrary explicitly or implicitly described convex set.

## 6. The qualitative extension and a distinct exact check

Section 4.4 also passes review. For an arbitrary convex upward set,
the affine hull of the integer points in a nonempty capped projection
is rational: choose a finite affine basis from those integer points.
When the projection has smaller affine dimension, this hull does too.
Its full integer lattice retains all improving integer points. The
other descent branch uses the same finite-range subsequence argument.
The result is a rational affine slice on which the real and integer
infima agree. This is only an existence statement; no encoding or
computability claim follows without additional representation assumptions.

I ran a distinct inline `python -` check over
\(\mathbb Q(\alpha)\), \(\alpha^3=2\). With
\[
 a=(1,\alpha,\alpha^2,1+\alpha),\qquad
 b=1+2\alpha+3\alpha^2,
\]
the algebraic affine equation \(a^Tz=b\) expands, for rational \(z\),
into
\[
 z_1+z_4=1,\qquad z_2+z_4=2,\qquad z_3=3.
\]
Its integer solutions are exactly
\((1,2,3,0)+\mathbb Z(-1,-1,0,1)\). The command checked
irreducibility of the cubic, a common-field basis of the real kernel,
the rational coefficient expansion, and this affine integer lattice.
It also checked that the original real normal line has zero rational
part. Thus the affine-dimension step can reveal rational restrictions
even when no nonzero rational normal bounds the whole real affine set.
This cubic-field test adds a different field and dimension pattern to
the existing quadratic examples. It passed.

The unchanged example script was not rerun. Targeted local-link,
math-delimiter, whitespace, control-character, and final-newline checks
for this review passed, as did a scoped `git diff --check`.
These finite checks do not establish the universal geometric, algebraic,
or complexity assertions. No project-wide checks, CI inspection, or
Lean formalization were performed. The separately reviewed compressed
projection, exact feasibility, and attained-fiber results remain
substantive dependencies; novelty and practical solver value still need
their own assessment.
