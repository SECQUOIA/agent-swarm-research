# Independent review: weighted contrast selection

Verdict: **PASS for `CriterionSelectWeighted.lean` semantics and the final
weighted arithmetic transcript, scan-cost modules, and path-specific
composition.** The complete cover producer's bit complexity is a separate review.

`rationalWeightedTerm` removes a zero weight before inspecting whether the
cost is infinite. This implements the extended nonnegative-real convention
`0 * infinity = 0`. For a nonzero nonnegative weight, an infinite term remains
infinite. Finite rational terms are clipped at zero before multiplication;
`rationalCostAdd` also clips its two finite inputs. The value lemmas therefore
agree exactly with `ENNReal.ofReal`, including negative rational values
outside the PSD contract. Nonnegative weights are explicit premises; there
is no unsupported guarantee for negative weights.

The list fold has zero as its empty value. Its induction handles infinite
terms and zero weights without a finiteness assumption. The matrix-level
bridge uses the actual rational estimability and variance computations from
`CriterionSelectContrast`, with PSD required for their mathematical meaning.
Singular matrices and unestimable contrasts remain allowed. Zero-weight
unestimable contrasts do not make the weighted objective infinite.

`weightedContrastCostLE` compares the exact rational/extended costs.
`selectWeightedContrast` supplies its comparator in the correct direction
to `bestBy` to minimize the objective; the proof uses `OrderDual` consistently.
The selection theorem proves membership and minimality over the actual input
list. The relative-cover theorem proves membership in the feasible set and
the factor `(1-eta)^(-1)` against every feasible target. It requires
`0 <= eta < 1`, PSD matrices on the feasible set, and nonnegative rational
weights. Its premise that selection returns `some b` is the usual nonempty
selection premise, not a supplied optimum or objective oracle. The empty list
returns `none`.

Targeted verification:

- `lake build --wfail Formal.DAGSpectral.CriterionSelectWeighted
  Formal.DAGSpectral.TopologicalMaterializeCost` passed.
- `topics/21-dag-spectral/verification/CoverPreprocessingReview.lean`, run with
  `lake env lean -DwarningAsError=true`, passed runtime assertions for zero
  times infinity, negative finite clipping, mixed aggregation, positive
  infinite terms, an empty family, a singular matrix with a zero-weight
  unestimable contrast, a positive-weight unestimable contrast, actual
  minimization over two matrices, and empty selection.
- Axiom inspection of `rationalWeightedContrastCost_value` and
  `IsRelativeCover.selectWeightedContrast_guarantee` returned only
  `propext`, `Classical.choice`, and `Quot.sound`. No new axioms or admitted
  proofs were found in this module. No project-wide or CI checks were run.

Reviewed SHA-256:
`bc187f7f8dc8272169630501bb309c234c3b32524de1832731b86830a83b235f`.

## Execution and arithmetic cost

The additional reviewed modules are `CriterionSelectWeightedTrace`,
`CriterionSelectWeightedScan`, and `CriterionSelectCostTrace`.
`weightedContrastInputsWithTrace` executes each actual contrast computation
once, stores its returned estimability flag, variance, and events, and gives
the stored optional costs to the weighted fold. In turn, each fold step uses
the returned clipped product and returned tail sum. No variance or
estimability oracle is an input. Zero-weight contrasts are still computed;
the trace and length bound include that deliberate work.

The weight-equality branch charges both ordered comparisons against zero.
Finite clipping and addition use stored clipped values. The common rational
cost comparator also caches both clipped inputs before comparing them.
`weightedContrastCostLERun` consumes the two computed weighted costs, and
`bestByRun` uses its returned Boolean to choose the next incumbent. Thus the
scan transcript belongs to the actual adaptive selection, rather than to a
separate evaluation of the specification.

The fold width is `1 + m*(2*K+1)`: each weighted term uses at most `2*K` bits,
and each addition adds the two operand widths and one. This avoids an
exponential-in-contrast-count bound. Input contrast widths are linear in the
original common rational bit bound at fixed matrix dimension. The final
theorem `selectWeightedContrastRun_polynomial_bitWork` bounds the actual
scan's event work by
`weightedSelectionBitConstant n * xs.length * (m+1)^4 * (B+1)^3`.
The only numerical input-size premises are the original matrix, contrast,
and weight bounds and `B>0`; PSD and nonnegative weights are needed for the
objective interpretation, not for this arithmetic bound. Empty and singleton
candidate lists have no comparator events. A zero-length contrast family
returns finite zero and remains covered by the bounds.

This is a polynomial bound in the established rational primitive cost model.
Allocation, transcript concatenation, option/list control, arbitrary candidate
accessors, and path-matrix construction are not included in the event sum.
The result does not by itself assert a full bit-machine running time or a
timing bound for Lean's evaluator.

Additional targeted verification:

- `lake build --wfail Formal.DAGSpectral.CriterionSelectWeightedScan` passed.
- `topics/21-dag-spectral/verification/WeightedExecutionReview.lean`, run with
  `lake env lean -DwarningAsError=true`, passed eleven runtime assertions for
  mixed/infinite/zero weighting, clipping, exact trace-length bounds, singular
  cost evaluation, actual selection and comparator-transcript equality,
  empty/singleton scans, and a zero-length contrast family.
- Axiom inspection of `selectWeightedContrastRun_result` and
  `selectWeightedContrastRun_polynomial_bitWork` returned only the three
  standard axioms listed above.

Additional reviewed SHA-256 values:

| Module | SHA-256 |
| --- | --- |
| `CriterionSelectWeightedTrace` | `71991971fd108378a95c2d956616bee20939c607a8e63dd864eb743af50c3ca8` |
| `CriterionSelectWeightedScan` | `9bd9f86a3a887d34a7eda68ca992c046b7938018b21d30508707fe56c5789a0b` |
| `CriterionSelectCostTrace` | `dbca7718993452b4362119537cb5b2b0b4758f14b605326e7f49768cafad19eb` |

## Original path matrices

`CriterionSelectWeightedPath` specializes the actual `selectPathsRun`.
Each adaptive comparison first stores the two original rational path sums,
then passes those matrices to the weighted comparator. Its output is proved
equal to `selectWeightedContrast (rationalPathInformation Q0 Q)` on the same
candidate list. The event bound includes both path sums and every weighted
comparison; it does not assume precomputed path matrices or their bit sizes.
The final bound is
`weightedPathSelectionConstant p * xs.length * (N+1)^4 * (k+1)^4 * (B+1)^3`
from the original prior/edge, contrast, and weight bit bounds and maximum
candidate path length `N`. The linear path-sum width is promoted to a common
width before invoking the comparator theorem. No PSD, rank, or graph
acyclicity premise is needed for this computational bound; the separate
objective/cover theorem supplies the semantic premises.

`lake build --wfail Formal.DAGSpectral.CriterionSelectWeightedPath` passed.
The runtime client was extended with actual selection between two raw path
lists and equality of its event count to the weighted comparator count plus
the sixteen original matrix-addition events. All thirteen assertions passed.
The path polynomial theorem's axioms are again only the three standard ones.
Its SHA-256 is
`64d5b6702d65138b42bd33f8c8665c552c724556abf50f7256c7314336de3086`.
