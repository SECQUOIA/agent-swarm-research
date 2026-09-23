# Independent check of the three-witness obstruction

Date: 2026-09-05. Verdict: PASS on the
[supporting note](positive-vector-three-witness-integer-obstruction.md).

For an integer-label distance `q>=3`, the stated choice
`ceil(2q/3)/q` lies in `[2/3,4/5]`: the cases three and four are immediate,
and the upper bound follows from `(2q+2)/3<=4q/5` for `q>=5`.
This weight gives an integer label regardless of the relative orders of
the graph inputs and integer labels. The positive lower endpoint deficit
forces `xi<=1-64/(5D_j)`. The exponential estimate and exact resulting
fraction `8785/8192` are correct and strictly exceed one.

Equal labels are excluded by the previously reviewed two-thirds chord
argument. Consequently any three proposed labels must be distinct and
consecutive. Their arithmetic mean is an integer. The uniform convex
combination of the three exact lifted graph points is therefore feasible
with an integer label and has weight one third on the smallest input.
Its component error is at least `2177/2144>1`, by the earlier family bounds.
This proves the same contradiction as the note's equivalent two-stage
midpoint-and-fiber argument, for every permutation of the labels.

The known two-binary upper formulation for `M=3` completes
`p_conv=p_bin=2`. Arbitrary auxiliary size, unbounded integer labels,
and nonclosed convex lifted sets do not affect these finite convex
combinations. The limitation to this particular three-component case,
without a general integer-count conclusion for larger families, is explicit.
No correction was required.
