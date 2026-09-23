# Independent audit of the arbitrary-polynomial vector overlay

Date: 2026-09-05. Verdict: PASS for the extension, conditional on the linked
scalar and convex-overlay constructions as stated.

Reviewed [the full candidate](compiled-polynomial-vector-overlay-precision.md).
The additional arguments beyond the convex overlay are correct.

The scalar source construction orders its polynomially many convexity pieces
and root brackets. Reversing reflected local indices makes each local array
ordered, and concatenation preserves that order. Projecting the global vector
lift and restricting its input preserves its integer count, so the imported
`4096 D_j 2^p` count is applicable to each scalar output.

Merging all right endpoints with multiplicity yields exactly `sum K_j` cells.
For a positive-width cell, the last source knot at most its left endpoint has
a successor at least its right endpoint. Otherwise that successor would occur
strictly between consecutive merged endpoints. This identifies a valid source
cell and its curvature sign without an enumeration. Duplicate knots and the
domain endpoint are handled by the stated zero-width convention.

The rounding signs and graph bands were checked directly. Writing `e=y-f`,
the three cases give respectively

```
convex:   -epsilon/16 <=e<=13epsilon/16,
concave:  -13epsilon/16<=e<=epsilon/16,
bracket:  -epsilon/8  <=e<=epsilon/16.
```

The proposed bands contain zero error in every case. Their largest admitted
absolute error is `15epsilon/16`: in particular, the bracket's downward
rounding and potentially negative chord error together reach `-epsilon/8`,
which is still covered by the upper band offset. This was the main new sign
issue to verify; there is no gap.

Source-cell flags are computed Boolean outputs of the same input-index
circuit. Selecting rational band offsets uses linear equations and adds no
declared integer variables. The common interpolation parameter places every
output at the same input point. Dense rational evaluation on the common input
denominator has polynomial bit length even though the number of implicit
cells is exponential.

The final count follows from `K<=4096 (sum D_j)2^p` and gives the stated
`p+12+ceil(log2(sum D_j))`. Affine outputs can remain exact and do not need
arrays. No coupled-error-body, sparse huge-degree, or necessary convex-vector
output-penalty conclusion is inferred. No correction was needed.
