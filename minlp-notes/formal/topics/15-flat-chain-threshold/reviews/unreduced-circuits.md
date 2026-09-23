# Independent review: unreduced signed-subset circuits

No soundness defect or hidden coefficient/support bound was found in
`ThresholdUnreducedCircuits`, `ThresholdUnreducedClassification`,
`ThresholdUnreducedCover`, `ThresholdUnreducedSupport`, and
[ThresholdUnreducedResults.lean](../../../Formal/NetworkSimplex/ThresholdUnreducedResults.lean).
The review inspected all five proof sources. No proof source was changed.

## Findings

- `normal_injective` and `normal_range` establish that the fourteen rows are
  exactly the distinct nonzero signed zero-one vectors in three coordinates.
  Zero normals are excluded. The candidate rows have independently checked
  nonnegative weights, nonzero support, and exact cancellation.
- `PositiveCircuit` means a nonzero nonnegative real cancellation with minimal
  support among positive dependencies. It is not defined by membership in the
  candidate table. `dependence_on_support` proves the stronger fact that every
  real cancellation on each listed support is a scalar multiple of its displayed
  weight vector. The checked pivot has weight one. This proves the displayed
  supports are minimal and supplies their primitive normalization.
- The completeness proof covers all 16,384 subsets of the fourteen normals.
  `supportMask_bits` and `separatorMask_bits` connect the numeric masks to actual
  circuit supports and strictly positive integer dot products. The block checks
  use kernel reduction. `encodeBits_lt` and `encodeBits_testBit` cover every
  Boolean support; the 64-by-256 split has no omitted boundary mask.
- `dependence_contains_circuit` applies that support cover to arbitrary
  nonnegative real coefficients. A strictly separating vector would give a
  strictly positive weighted sum, while cancellation makes the same sum zero.
  The proof assumes neither integral coefficients nor a bound on support size,
  coefficient size, or denominators.
- Minimality then makes the contained listed support equal to the original
  circuit support. `positiveCircuit_classification` proves positive scalar
  proportionality. For natural weights, the gcd-one condition forces that
  scalar to be one because the pivot weight is one. Consequently
  `primitiveCircuit_iff` classifies every primitive circuit without a bounded
  search premise. Injectivity prevents duplicate counting; the exact finite
  image theorem justifies the use of `Set.ncard`.
- Dimensions one and two are represented by zero padding into the first one or
  two coordinates of `Fin 3`. `normalLibrary_range` characterizes exactly those
  signed nonzero vectors with vanishing unused coordinates. `InDimension`
  forces every nonzero circuit weight onto these rows. The extra cancellation
  equations are zero, and restricting the row universe preserves support
  minimality and primitive gcd normalization. Thus the counts refer to the full
  one-, two-, and three-dimensional universes, not a selected observation set.
  The definitions remain syntactically usable for larger `d`, but still describe
  this three-coordinate ambient universe; the stated count results concern only
  dimensions one through three.
- `full_signed_subset_circuit_counts` proves the exact primitive counts 1, 5,
  and 41. `full_signed_subset_weight_maxima` combines universal upper bounds
  with witnesses attaining 1, 1, and 2. These are actual maxima over all primitive
  circuits. The usual support-size bound is a consequence of classification,
  not an input to completeness.

## Targeted checks actually run

From `formal/`:

```sh
lake build Formal.NetworkSimplex.ThresholdUnreducedResults --wfail
lake env lean -DwarningAsError=true /tmp/threshold-unreduced-review.lean
```

Both passed. The temporary review file checked that the zero dependency is not a
circuit, dimension zero has no normals or circuits, the normal counts are
2/6/14, and primitive classification has no additional premise. Transitive
axiom prints for support coverage, real circuit classification, exact circuit
counts, and exact weight maxima used only `propext`, `Classical.choice`, and
`Quot.sound`.

No project-wide verification was run, and CI status or logs were not inspected.

Reviewed SHA-256 values, in the five-module order listed above:

```text
24a1d91dba0120f692863b3a45ed6709f86b7a64535d5f069baabc90764f32c5
12fd202d6a33885305d43a38b89761fd5bb399e6f00b54be5edb1ce1316f394f
2563099e91cdb82dc78664c002546c64c0afd13519bf4178a121ab8b7d91631a
5b68279c022f46e0607474a43ff274cb3ba28d42b0a55107f63bf790a74b6218
1bea8f89aa4d750c6d2923dc0459e2cada033d32c4c0bcb0b35ce7dc56dc4bad
```
