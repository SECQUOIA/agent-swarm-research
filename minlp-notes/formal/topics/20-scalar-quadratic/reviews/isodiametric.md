# Independent review: sharp Euclidean isodiametric inequality

Date: 2026-09-20. Reviewer: independent source-review agent.
Reviewed all nine `Isodiametric*.lean` modules in
[Formal/QuadraticPrecision](../../../Formal/QuadraticPrecision), including
the full polarization, weighted-measure, compact-maximization, and final
comparison arguments.

Verdict: **PASS**. No mathematical defect or unproved geometric premise
was found. The headline proves that every compact set with pairwise
Euclidean distances at most `D>=0` has volume at most the ball of radius
**`D/2`**. The explicit dimension-positive version proves the exact
unit-ball multiplier `volume(closedBall 0 1) * (D/2)^d`.

The theorem does not assume convexity, positive volume, nonempty interior,
a regular boundary, an extremizer, or a symmetrization convergence
theorem. Its extremizer and strictly improving polarization are proved
inside the package. In particular, no Brunn–Minkowski or isodiametric
inequality is supplied as an assumption. Applying this result to the
quadratic parity contacts remains the separate sharp-curvature assembly.

## Finite radial-weight comparison

The weight is the actual continuous function
`w_C(x)=max(0,C-norm(x)^2)`. It is nonnegative, bounded above by `C`
when `C>=0`, and has compact support. In finite-dimensional Euclidean
space this makes it integrable; its density defines a finite Borel
measure. The weighted-measure formula is proved by the relation between
the real integral and the nonnegative density integral.

If a bounded measurable set `S` has volume `s` strictly larger than a
finite-volume comparison set of volume `b`, the proof chooses a finite
`C` larger than both `R^2` and `R^2*s/(s-b)`, where `S` lies in the
radius-`R` ball. On `S`, the weight is at least `C-R^2`; globally it is
at most `C`. Therefore

```text
weightedVolume(S) >= (C-R^2)*s > C*b >= weightedVolume(B).
```

This is the exact comparison required for the contradiction. Although
the introductory prose describes growing the cutoff, the formal proof
uses this explicit finite choice. It needs no interchange of a limit,
supremum, or integral. The comparison ball need not lie in the radius-`R`
ball, since its upper weight estimate is global.

## Actual compact maximizer

Outer regularity makes compact-set measure upper semicontinuous in the
Vietoris topology: for any strict upper bound on a compact set's measure,
an open superset has measure below that bound, and every compact subset
of that open set satisfies the same inequality. This is an upper
semicontinuity argument, which is the correct direction for a maximum.

The family of compact subsets of a fixed compact ambient ball is compact.
The pairwise-diameter constraint is closed: the continuous map
`K -> K × K` pulls back the closed condition of containment in
`{(x,y) | dist(x,y)<=D}`. The family is nonempty because it contains
the empty compact set. Hence upper semicontinuity supplies an actual
weighted-measure maximizer. The final application obtains outer
regularity from the finite Borel weighted measure in the finite-dimensional
metric space; regularity is not an extra hypothesis on the original set.

The original compact set is a feasible competitor in this family.
Thus a putative volume excess produces a maximizing compact `K` with
weighted measure strictly greater than that of the radius-`D/2` ball.

## Support point and exact reflection radius

The weighted excess implies that `K` has positive ordinary volume
outside the radius-`D/2` ball, using absolute continuity of the weighted
measure. The support of `volume.restrict K` consequently contains a
point `x` with `norm(x)>D/2`. Since `K` is compact and closed, that
support point belongs to `K`. This use of measure support is essential:
an isolated zero-volume outlier would not suffice for strict improvement.

Write `r=norm(x)>D/2`, choose `e=x/r`, and set
`t=(r-D/2)/2>0`. The affine reflection in the plane
`inner(e,z)=t` is
`R(z)=z+2(t-inner(e,z))*e`. The proof establishes all identities from
this formula. In particular,

```text
R(x)=(-D/2)*e,   norm(R(x))=D/2<r,
dist(x,R(x))=r+D/2>D.
```

Thus `R(x)` cannot belong to `K`. The preferred closed halfspace
`H={z | inner(e,z)<=t}` contains the origin, and reflection moves this
particular occupied point strictly inward to an unoccupied point.

The reflection is a genuine involutive isometry and measurable
equivalence. Its preservation of Euclidean volume follows from the
linear orthogonal reflection followed by translation. The fixed affine
hyperplane has zero volume: its unit normal exhibits a point outside
it, so it is a proper affine subspace. Consequently reflection swaps
membership in the two halfspaces almost everywhere; the closed-boundary
overlap is correctly discarded only as a null set.

## Polarization geometry and strict gain

The polarized set keeps doubly occupied reflection pairs and puts a
singly occupied pair's point on the preferred side:

```text
P(K) = (K ∩ R⁻¹(K)) ∪ ((K ∪ R⁻¹(K)) ∩ H).
```

Compactness follows by replacing the reflected preimage with the image
under the continuous involution and taking finite unions/intersections.
The diameter proof handles every membership combination. Its only
non-isometric comparison is for two points in the preferred halfspace,
where the exact squared-distance identity shows that their direct
distance is no greater than the crossed reflected distance. Hence the
same bound `D` holds without a convexity premise.

The ambient radius is also preserved. The identity
`norm(R(z))^2=norm(z)^2+4t(t-inner(e,z))` implies that a point on the
preferred side is no farther from the origin than its mate. Since
`t>0`, moving singly occupied pairs inward cannot leave the ambient
ball. The polarized compact set is therefore a valid competitor for
the same maximum.

On each reflection pair, placing a single occupied point on the preferred
side does not decrease its weighted contribution. The measure module
proves this by all membership cases, and integrates the paired
inequality using measure preservation. Integrability of the weight
justifies the ordinary integral additions and subtractions; no infinite
quantity is subtracted.

For strictness, `C>R^2` ensures that the weight is strictly decreasing
with squared norm throughout the relevant portion of `K`. At the support
point `x`, its mate is absent from `K`, the side inequality is strict,
and the inward weight gain is strict. Closedness of `K` and continuity
of reflection and weight make all these conditions persist on an open
neighborhood `U` of `x`. The support condition gives
`volume(U ∩ K)>0`. Reflection transfers this positive-measure chunk
to the preferred-side set of strictly improved pairs.

The strict integral theorem combines almost-everywhere nonnegative
paired improvement with a positive-measure set of strictly improved
pairs. Positivity of the integral of this nonnegative integrable
difference yields a strict weighted-measure increase. Thus the proof
does not mistake a pointwise gain at one point for a positive integral
gain. The resulting valid competitor contradicts the constructed
maximum.

## Constants, measure normalization, and boundaries

The geometric comparison uses radius `D/2` throughout; no radius-`D`
ball or coordinate box replaces it. The final unit-ball formula uses
Mathlib's volume scaling for `EuclideanSpace ℝ (Fin d)` with its
Euclidean norm and canonical Lebesgue measure. It therefore has the
exact `omega_d` normalization required for the sharp curvature constant.

The generic ball-comparison theorem allows dimension zero, `D=0`, empty
sets, and zero-volume sets. Its contradiction proof simply never reaches
the construction of a unit normal when the hypothesized strict volume
excess is impossible. The explicit unit-ball-power theorem assumes
`d>0`, consistently with the closed-ball scaling formula it invokes.
For that theorem `D=0` implies zero volume. Both the zero-diameter
positive-dimensional consequence and the dimension-zero generic
specialization were checked as direct clients.

## Targeted checks actually run

The author confirmed all nine source modules were stable before the
independent checks. From `formal/`, with
`PATH="$HOME/.elan/bin:$PATH"` and `LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.Isodiametric
lake env lean /tmp/Topic20IsodiametricReview.lean
```

Both commands passed. The temporary audit checked the two boundary
specializations and printed axioms for `exists_weightedMeasure_lt`,
`upperSemicontinuous_compact_measure`,
`exists_compact_measure_maximizer`, `exists_support_outside_ball`,
`exists_improving_reflection`, `integral_polarize_lt`,
`exists_strict_polarization`, `volume_le_closedBall_half_diameter`,
and `volume_le_unitBall_mul_half_diameter_pow`. Every list was exactly
`[propext, Classical.choice, Quot.sound]`.

Reviewed SHA-256 hashes:

- `Isodiametric.lean`: `b2a11dc2713d7b8889b25a9f15e7c9c50216d9f5f6d6bc3e4ed362e3566acce2`
- `IsodiametricCompact.lean`: `58caa4152ff316f5b39c8f9fde007ed3c47e72b5144e6c2063c11deec86bd77e`
- `IsodiametricDiameterClosed.lean`: `22ac5936ffaa5fc0afb1d946c572a21d959cd7d8009089a89b4fef4301b7fcb3`
- `IsodiametricGeometry.lean`: `049cbdc72821ab78e277124d0a6a0aec13401ee31032edb7a55021c6f9c7c1cb`
- `IsodiametricPolarizationMeasure.lean`: `a4a0d8ce09ee84702f10a818af33cf0b9d598e3b0c5c4df2f041649f1e4d6268`
- `IsodiametricReflection.lean`: `ff1e7dc85b8b8db6407d85e41d6613c84f20fbdc3a601b7f11573d155c23e8fb`
- `IsodiametricStrict.lean`: `74af524efdc18a4f2cc85d1014e16dd396898f754aa39d730664b0ff9fb73f1e`
- `IsodiametricSupport.lean`: `2f03dccee6cdb7e408aa61e42a885176763f105ddd2696ffb7b9b5eed9b935a1`
- `IsodiametricWeight.lean`: `210cc1df9393af24c745fd279520669854decfcf9b94a94f512a9f6f5660121d`

No source file was changed by this review. No project-wide verification
or CI inspection was performed.
