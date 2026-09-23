# Independent review of the many-leaf hull core

Status: source and statement review passed for the core described below.
This is not a completion record for the entire topic. Algorithmic complexity,
rational construction, the full probability-measure extensions, and the
separation package require their own review and targeted checks.

The reviewer independently compared the source note and the frozen inventory
with `ManyModel`, `ManyLaws`, `ManyGeometry`, `ManyThreshold`, `ManySelection`,
`ManyEnvelope`, `ManySlopeJumps`, `ManyEnvelopeLaw`, `ManyActiveCount`,
`ManyLawCompress`, `ManyEnvelopeBound`, `ManyIntegrals`, `ManyResults`,
`ManyOneLeaf`, `ManyExamples`, and `ManyNormalization` in
[the proof directory](../../Formal/ReciprocalAnchor).
The integrating agent reported a passing targeted build of the final
`ManyResults` module after this review began. This review did not run a
separate compiler check or inspect CI. The final verification record must
identify the actual targeted commands and their logs.

## Main theorem and representation

`mem_hull_iff_bounds` states the claimed equivalence for the actual
`convexHull` of graph points. The graph has one reciprocal coordinate and
exactly the intended common-factor products. Its assumptions are `0 < a`,
`a < b`, and the candidate inequalities on the right side of the equivalence.
There is no supplied feasible measure, precomputed envelope, selection oracle,
or positive leaf-count premise. The number of leaves is an unrestricted
natural number, so zero leaves are included.

`mem_hull_has_finite_representation` and `mem_hull_iff_law` derive finite
representations from membership in that hull. Conversely,
`finite_representation_mem_hull` and `Law.realizes_mem_hull` reconstruct
actual graph membership from all four sets of moment equalities. The
representation is not introduced by changing the meaning of the hull.

`LinearBounds` deliberately includes the two mean bounds for every leaf count.
For a nonempty leaf type, `leaf_bounds_imply_mean_bounds` proves their
redundancy with respect to the leaf inequalities. Baseline lines are present
even when there are no leaves, so the finite maximum is never empty.

## Constructing the least law and its support bound

The chain from candidate inequalities to a law is complete:

1. `envelope_left` and `envelope_right` derive the two exterior affine pieces
   from the candidate inequalities. Convexity, continuity, and slopes in
   `[-1,0]` are proved separately in `ManyGeometry`.
2. `exists_affinePartition` constructs a genuine partition from all pairwise
   line intersections. It proves an active input line on every closed cell;
   an active partition is not assumed at the public existence interface.
   Extra intersections, including irrelevant intersections of parallel lines
   under totalized division, may create extra cells but do not affect this
   correctness proof.
3. `AffinePartition.slopeData` derives adjacent slope monotonicity and
   continuity, including both endpoint transitions. `SlopeJumpData` then
   proves nonnegative jumps, total mass one, the correct mean by telescoping,
   and exact agreement of the resulting call function with every piece.
4. `Law.compress` removes zero masses and proves preservation of every
   expectation of a function of location. `slopeJumps_card_le` injects strict
   changes into distinct input slopes and reserves the initial slope.
   Since both exterior slopes occur among the `2n+2` input lines, the
   compressed law has at most `2n+1` atoms.

Thus `envelope_exists_small_law` and `exists_minimizing_law` do not assume the
hard representation or support-count conclusions. The count is stronger than
an informal count of distinct support locations: it bounds the number of
indexed atoms in the constructed representation. Repeated slopes, inactive
lines, redundant partition knots, and zero jumps are covered by compression.
The partition construction used for this existence proof is not the claimed
fast envelope algorithm; its correctness must not be used as evidence for
`O(n log n)` running time.

## Selections, extrema, and mixtures

`exists_weighted_threshold` proves threshold existence, including mass zero
and mass one. `thresholdSelection_spec` handles a threshold with zero total
atom mass explicitly: its hypotheses force the selected remainder to zero.
It does not rely on dividing by a strictly positive mass in that case.
`fractional_selection_iff` proves both directions of the call-inequality
characterization and constructs an interpolated selector. Equal extremal
moments are handled before division by their difference. Simultaneous
selection uses one fixed scalar law for every leaf; independence is neither
required nor assumed.

The reciprocal integral is proved first pointwise, then for finite laws.
The lower-bound comparison uses positive interval endpoints, established
integrability, and actual call-function domination. The endpoint law has its
claimed mean and reciprocal moment, and `call_le_endpoints` proves domination
of every finite supported law of that mean. `endpoint_law_realizes` connects
that domination to all the leaf moments.

`exists_hull_law` mixes the minimizing and endpoint laws for each admissible
reciprocal moment, handles equal extrema without division, and proves all
means and selections. Its bound is `2n+3` indexed atoms. Together with the
finite representation theorem, this is the claimed bound on original graph
points, with no enumeration of binary endpoint patterns.

## Normalization, specialization, and example

`restore_graph` and `restore_hull` prove the affine image statements for
arbitrary ordered leaf boxes. The product coordinate includes the essential
term `l_j*m`. Strictly positive box widths have both inverse identities.
Fixed leaves are represented by zero dummy coordinates after erasure, rather
than reindexing to a smaller `Fin` type. `mem_box_hull_iff_fixed_deleted`
proves that these coordinates can be erased and restored; the two original
fixed-leaf equations are also proved. This has the required deletion
semantics, including the all-fixed case.

The positive-anchor transformation is an actual graph and hull map, and
`mem_anchored_hull_iff` uses positivity of the common-factor lower endpoint
and anchor product where inverses are needed. The fixed-common-factor hull
is proved linear for normalized and original boxed leaves. Some algebraic
degenerate theorems also admit `a=0` under Lean's totalized reciprocal;
their application to the source is restricted to positive `a`.

The one-leaf law puts zero-mass atoms at the left endpoint, so no undefined
conditional mean is used. The reciprocal perspective identity and the
two-SOC equivalence treat zero denominators through the linear bounds.
The exact example proves the entire call-envelope identity, not just a
three-atom witness with a convenient reciprocal moment. It follows that
`31/50` is the minimum, and the proposed `3/5` misses it by `1/50`.
The separate equality-support statements are proved, their supports are
disjoint, and the existing individual hull memberships are reused explicitly.

## Clarifications recorded by the review

- MR03 originally requested a counterexample after omitting explicit mean
  bounds in the zero-leaf case. That extra demand was not in the source and
  was incorrect when the reciprocal inequalities are retained. The inventory
  now asks exactly for the source's explicit mean bounds and the nonempty
  leaf implication. No source claim was removed.
- The generic second-derivative identity in `ManyIntegrals` states ambient
  derivative hypotheses at both endpoints. This is the usual interpretation
  of a function with a twice continuously differentiable extension to the
  closed interval. Its exact hypotheses should remain visible in the coverage
  map; the theorem should not be described as accepting only unspecified
  one-sided derivatives.
- The finite-law core proves the complete hull theorem. It does not alone
  discharge the source's separate assertions about arbitrary probability
  measures. Those extensions have separate modules and require separate
  review.

No unresolved semantic defect was found in the reviewed core. This finding
does not establish the still-separate rational algorithm, complexity,
cut-family, or software assertions.
