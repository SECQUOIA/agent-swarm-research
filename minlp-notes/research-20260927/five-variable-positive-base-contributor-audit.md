# Contributor audit of the five-variable positive-base argument

Date: 2026-09-28. Reviewer: `one_parameter_spectrahedral_fields`.
Status: full proof read; no mathematical defect found. This reviewer
helped develop the low-degree case analysis and is therefore a
**contributor**, not a fresh independent reviewer. Separate fresh
reviews of the [classification](five-variable-positive-base-classification-review.md)
and [perturbation step](quadratic-base-blowup-review.md) passed; I read
both completed reviews and checked their clarifications. The
[root's full independent review](five-variable-degree-root-review.md)
also passed, including direct primary-source checks; I read its
completed record.

The source is
[five-variable-positive-base-bound.md](five-variable-positive-base-bound.md).
Its geometric assertion is that a real quadratic system in projective
five-space, with at least 23 isolated regular points, cannot have a
positive-dimensional complex base without real points. Combined with
the separately reviewed odd-residual theorem, it gives the verified
sharp arithmetic degree bound 21 for five-variable rational SOS
globally convex quartics with a regular zero. This audit neither
establishes publication priority nor extends the claim to rational
polynomials that have only a real SOS representation.

## Weighted degree and the full base

The generic-five-equation step is necessary. On the complement of
the full base, each point imposes one nonzero evaluation condition
on each of five independently chosen coefficient rows. The incidence
space has dimension equal to the parameter space. Its generic fibers
are therefore finite or empty. Simultaneously requiring independent
gradients at each of the finitely many specified regular points is a
nonempty open condition. These conditions can be imposed over the
reals, or over the rationals when the system has a rational basis.

I checked the elementary weighted intersection proof directly. For
an irreducible variety not contained in the next quadric, the proper
intersection has total degree twice its degree and dimension one
less. Its total weight `2^dimension * degree` is unchanged if
multiplicities are retained, and cannot increase after reduction.
A contained component keeps its weight. The union of supports is
preserved at each intersection step, so every maximal component of
the final intersection appears. In particular, every maximal positive
component of the full base appears: a larger positive component of
the selected intersection would itself lie in the full base, contrary
to maximality. Each isolated regular point contributes at least one.
Thus the bound `D + sum 2^dimension * degree <= 32` applies to the
full base, including when its scheme structure is nonreduced.

Conjugation preserves dimensions and degrees. A positive-dimensional
real projective variety of odd degree has a real point, by generic
real linear slicing and parity. With a remaining weight at most nine,
this rules out dimensions at least three and leaves only surfaces
of total degree two or curves of total degree at most four. The
argument does not count a curve inside a surface as another maximal
component.

## Classification and quadratic generation

I independently reconstructed all cases in the source.

- Conjugate lines or planes must be disjoint: a nonempty intersection
  would be an invariant projective linear space and would contain
  real points. Their unions have quadratic equations from products
  between the coordinate blocks, together with linear equations of
  their span where necessary.
- A real geometrically integral quadric surface is a quadric in
  projective three-space. A singular such quadric has a real linear
  singular locus, so the real-point-free case is smooth.
- An integral real quartic curve has span dimension at most four.
  In a plane it forces every containing quadric to vanish on that
  real plane. In projective three-space, zero or one independent
  containing quadric forces a whole real span or quadric surface
  into the base. Two independent containing quadrics have no common
  surface component, since such a component would force the integral
  nonplanar curve into a plane. Their complete intersection has
  degree four and therefore equals the curve. Equality holds
  scheme-theoretically because a complete intersection is unmixed;
  equal degree excludes both other components and generic thickening.
  In projective four-space the curve is the classical rational normal
  quartic and has a quadratic ideal.
- For conjugate conics whose planes meet along a line, there must be
  a real containing quadric nonzero on both planes; otherwise the
  real intersection line lies in the base. Together with the union
  of the two planes it cuts out exactly their reduced degree-four
  union, a complete intersection of two quadrics. This avoids any
  assumption that this union is smooth.
- For planes meeting at a point, that point is real and lies on
  neither conic. In the source's coordinates, four cross-products
  generate the plane union, and `c+c'-x0^2` restricts to the respective
  normalized conic equations and is nonzero at the intersection point.
  Away from that point the assertion is local on disjoint planes;
  at the point the added equation is a unit. This proves generation
  of the ideal **sheaf** by quadrics, which is exactly what the
  blowup argument requires. It does not require the displayed graded
  ideal to be saturated.

Every chosen subvariety is disjoint from the specified isolated regular
points. The low-degree case list either produces one of these
subvarieties or forces a real point into the positive base. It does
not assume that the actual positive base is reduced, smooth, or a
local complete intersection.

## Perturbation and intersection numbers

For a reduced local complete intersection subvariety `Y` with
`I_Y(2)` globally generated, its blowup has globally generated line
bundle `L=2H-E`. Five generic sections avoid the exceptional divisor,
which has dimension four, and meet in finitely many points on the
smooth complement, or not at all. Their total intersection degree
is `L^5`. At each original isolated regular zero outside `Y`, the
complex implicit function theorem preserves a zero under sufficiently
small perturbations of the five coefficient vectors. Generic choices
are dense, so the number of such original points is at most `L^5`.
This argument needs no comparison of Segre classes of the original
possibly thickened base and its reduced support.

For a local complete intersection curve, the normal degree gives
`L^5 = 30 - 4 degree(Y) + 2 arithmetic_genus(Y)`. In the singular
complete-intersection cases, the displayed normal bundles suffice
directly. I separately expanded the relevant Chern-series ratios over
the rationals with SymPy and obtained:

| Chosen subvariety | Excess contribution | Remaining intersection degree |
| --- | ---: | ---: |
| Conic | 10 | 22 |
| Two disjoint lines | 12 | 20 |
| Quartic complete intersection in projective three-space | 16 | 16 |
| Rational normal quartic | 18 | 14 |
| Two disjoint conics | 20 | 12 |
| Quadric surface | 22 | 10 |
| Two disjoint planes | 32 | 0 |

For example, the quadric surface computation is
`2 * coefficient(H^2, (1+2H)^4/(1+H)^2) = 22`;
one plane contributes
`coefficient(H^2, (1+2H)^5/(1+H)^3) = 16`.
All computations passed. This exact arithmetic checks the numerical
consequences of the normal-bundle formulas; it does not prove the
classification, perturbation, or intersection-theoretic formulas.

## Transfer to the optimization statement

Rationality of every quadratic square factor is needed. A rational
polynomial expressed using arbitrary real factors would not suffice
for the Galois-orbit or rational flat-direction steps. I requested
that the displayed application hypotheses state this explicitly; the
author applied the clarification and I rechecked it. I also checked
the fresh reviewer's added pure-dimension hypothesis in the general
perturbation lemma; all classified subvarieties satisfy it.

If the convex quartic leading form has a nonzero real zero direction,
the previously proved rational flat-direction reduction preserves
the minimizer's coordinate field and reduces the problem to at most
four variables; the isolated quadratic Bezout bound 16 is already
sufficient. Otherwise the projective common real zero set of the
homogenized factors consists only of the prescribed minimizer. Its
full-rank quadratic Jacobian isolates it even over the complex numbers.
The geometric theorem thus applies. Once the base is finite, generic
rational combinations give the proper complete intersection needed
by the independently reviewed odd-residual theorem. The cyclic family
attains degree 21 with the stated convexity and rational SOS properties.

After the independent Chern arithmetic, I ran the author's retained
targeted checker:

```text
python research-20260927/check_five_variable_positive_base.py
```

All seven intersection counts and both exact conic-union ideal
calculations passed. No new universal Lean proof, project-wide test,
or CI inspection was performed in this review. The fresh reviews and
separate primary-source audit remain distinct evidence from this
contributor reconstruction.
