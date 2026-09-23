# Independent review of factor aggregation and cardinality averaging

Reviewed 2026-09-20. The reviewer did not author or change
`StructuralFactorGaps.lean`, `StructuralAveraging.lean`, or
`StructuralTwoClasses.lean`. The reviewer did complete their TU-law dependency
`StructuralCardinalityTU.lean`; that dependency is therefore not an independent
review result here.

**Result: no mathematical or statement-scope defect found in the three reviewed
modules. They prove the stated aggregation implications, and the two-class
result constructs both laws from its TU hypotheses. They do not prove that a
graph of incidence treewidth two has such a partition.**

The review traced the definitions of `envelopeValues` and `hullGap` in
`CubicGap/Envelope.lean`, the actual attained endpoints in
`MultilinearGap/Attainment.lean`, and the cardinality endpoint statements in
`StructuralCardinality.lean` and `StructuralCardinalityUpper.lean`. The averaging
argument was compared with equations (3)–(6) in
`results/convex-cardinality-frequency-two-gap.md`.

- `factorSum_maximum` proves attainment of the sum of individual upper
  endpoints by the supplied common law. `factorSum_gap_of_law` uses the actual
  lower graph-hull endpoint and an actual feasible law. It does not assume
  that this law minimizes the sum.
- `factorSum_two_law_bound` preserves every singleton mean with the equal
  mixture. For each factor one class law attains its lower endpoint, while the
  other is bounded by its own upper endpoint. Hence the mixture deficiency is
  at least half the individual gap. The factor two has the correct direction.
- `finiteMixture` proves nonnegativity and normalization directly, and its
  expectation and mean lemmas account for every mixture component.
- `cardinalityLower_eq_chord_on_slab` includes the closed upper endpoint. When
  the mean equals `k+1`, the floor advances but the next interpolation
  coefficient vanishes; no assumption on the unused next table entry is
  required. `cardinalityLower_average` therefore gives equality, not a Jensen
  bound, throughout the common slab.
- `upperEnvelope_average_le` has the correct concavity direction. Combined
  with exact lower averaging, `cardinalityGaps_average_le` states
  `E[T(Z)] ≤ T(E[Z])`, as required by the source.
- `cardinality_gap_of_slab_rounding` assumes local excess at most `η*T(z)` and
  `η ≥ 0`, then proves `(1-η)*T(x) ≤ H(x)`. The nonnegative sign of `η` is
  precisely the sign needed to multiply the averaging inequality. No upper
  bound on `η` is needed: values above one merely give a weaker conclusion.
  Setting `η=1/g` yields the source coefficient `(g-1)/g`; setting `η=0`
  yields simultaneous lower attainment. The module deliberately takes the
  decomposition and rounding laws as inputs and does not claim to construct
  odd cycles or their rounding.
- `cardinality_two_TU_classes_bound` actually constructs each class law from
  TU incidence and integer slab bounds. The color-class matrix retains all
  original coordinates; therefore both laws preserve all singleton means,
  including coordinates absent from one class. Arbitrary overlaps, an empty
  class, empty factor families, and zero factor gaps need no division or
  nondegeneracy assumption.
- Convexity is restricted to attainable counts; table values and slopes may
  have either sign. Nonnegative scalar coefficients can be absorbed into
  those tables. The concrete corollary uses the multiaffine cardinality
  interpolant, not substitution of the mean sum into a nonlinear function.

Targeted verification actually run from `formal/`:

```text
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake build Formal.MultilinearGap.StructuralFactorGaps Formal.MultilinearGap.StructuralAveraging Formal.MultilinearGap.StructuralTwoClasses
```

Result: passed. No project-wide verification or CI inspection was performed.
