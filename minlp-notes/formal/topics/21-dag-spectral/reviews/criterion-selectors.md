# Independent review: criterion selection and path evaluation

Reviewed `CriterionSelect`, `CriterionSelectTrace`, `CriterionSelectMatrix`,
`CriterionSelectMatrixTrace`, `CriterionSelectContrast`, `CriterionSelectPath`,
`CriterionSelectEigenTrace`, `CriterionSelectWeighted`, and
`CriterionSelectHeadline`, `CriterionSelectContrastTrace`,
`CriterionSelectContrastPath`, `CriterionSelectWeightedTrace`, and
`CriterionSelectWeightedScan` in [the source directory](../../../Formal/DAGSpectral).
The reviewer did not implement these modules. The stable mathematical selectors and runtime wrappers pass review; the
weighted original-path runtime specialization is a follow-up described below.

The candidate scan retains an actual input candidate and performs one
comparison per additional candidate. Its invariant requires comparator
correctness only on the actual valid candidate domain. Empty input returns
`none`; a nonempty list returns a candidate. Ties are allowed, and duplicates
do not affect correctness. Minimum-cost selectors use the reversed comparator
and the order dual, consistently in both their executable scans and proofs.
The finite-cover guarantee first obtains a representative for each target,
then compares that representative with the selected optimum. It does not
interchange the target and optimum quantifiers.

The determinant comparator evaluates rational determinants exactly. The
inverse-trace comparator checks determinants to represent singular PSD costs
as infinity; positive definiteness is derived from PSD and nonsingularity.
It computes the inverse expression even on singular input for a uniform
budget, but never interprets that finite expression as the singular cost.
The E selector invokes the certified algebraic comparator and excludes zero
dimension only where an actual minimum eigenvalue is asserted. Its runtime
wrapper includes the existing coefficient, threshold and bisection event
bounds, without treating a real eigenvalue oracle as an operation.

The contrast comparator uses an optional rational cost, with `none` denoting
infinity. Exact estimability determines this branch. Clipping finite values
at zero matches `ENNReal.ofReal`; on the PSD domain actual variances are
nonnegative. The weighted semantic selector erases a zero-weight infinite
cost before addition. Its nonnegative rational weight contract is explicit,
and it handles an empty contrast family and zero total cost without division.

`bestByRun` executes each comparator once and feeds its returned Boolean into
the incumbent update. D/A expression wrappers use `ArithmeticExpr.run`;
`rationalPathRun` stores each computed matrix entry and its event list once.
`pathComparisonRun` passes the resulting matrices to the comparator. Thus the
path-level bounds include matrix evaluation from the raw rational prior and
edge data, rather than supplying precomputed information matrices for free.
Path sums use the bound `1+(N+1)*(B+1)` before fixed-dimension criterion
arithmetic. This is polynomial for growing path length; the generic expression
width recurrence is not incorrectly applied to a growing sum depth.

The execution bounds count primitive rational event work. List traversal and
bookkeeping are not equated to zero runtime by these theorems; full Turing-work
aggregation remains the scope of the whole-producer analysis. Path selection
uses only the returned candidate list, not enumeration of all feasible paths.

`CriterionSelectHeadline`, `CriterionSelectContrastTrace`,
`CriterionSelectContrastPath`, `CriterionSelectWeightedTrace`, and
`CriterionSelectWeightedScan` instantiates the guarantees on the actual
`coverBitRun` output. Width parameters affect accounting, not the candidate
semantics. `criterionCandidates_cover` discharges the cover premise from the
original PSD matrices; `criterionCandidates_nonempty` discharges selector
existence from actual feasibility. The `produced_select*` conclusions assert
actual path feasibility and compare with every original feasible path. The
D scheme uses rational `epsilon/p`, with positive dimension and accuracy;
E uses `eta<=1`, and inverse/contrast bounds require `eta<1`.

The shared `CriterionSelectCostTrace` initially repeated clipping maxima
between the returned result and event operands. The author repaired it by
storing the two clipped values, and the revised three-comparison execution
passes review. `CriterionSelectContrastTrace` feeds the returned estimability
and variance into the optional cost and then the actual cost comparator.
`CriterionSelectContrastPath` also includes original path matrix evaluation.

The weighted trace computes and stores each contrast result, folds the
optional weighted costs, and uses the returned total in the comparator.
Its fold uses an additive rational bit-length bound linear in the number of
contrasts. `selectWeightedContrastRun_polynomial_bitWork` therefore has only
fixed matrix dimension in its constant; the contrast count remains a genuine
polynomial parameter. The original-path weighted runtime specialization was
outside this initial reviewed module set; it was subsequently implemented and
passed the [weighted-criteria review](weighted-criterion-semantics.md).
The actual weighted
produced-list semantic guarantee is already proved in `CriterionSelectHeadline`.

Targeted checks from `formal/`, with `~/.elan/bin` on `PATH`:

```text
LEAN_NUM_THREADS=1 lake build --wfail Formal.DAGSpectral.RationalPseudoinverseTrace Formal.DAGSpectral.RationalContrastTrace Formal.DAGSpectral.CriterionSelectPath Formal.DAGSpectral.CriterionSelectEigenTrace Formal.DAGSpectral.CriterionSelectContrast
LEAN_NUM_THREADS=1 lake env lean topics/21-dag-spectral/verification/CriterionSelectorReview.lean
```

Both commands passed. The preserved nine-declaration audit samples selector
guarantees and D/E/A path runtime bounds; all depend only on `propext`,
`Classical.choice`, and `Quot.sound`. This review does not replace the independent review
of the underlying exact algebraic comparison or whole-producer cost theorem.
No project-wide verification or CI inspection was run.

Follow-up targeted commands:

```text
LEAN_NUM_THREADS=1 lake build --wfail Formal.DAGSpectral.CriterionSelectContrastPath Formal.DAGSpectral.CriterionSelectHeadline Formal.DAGSpectral.CriterionSelectWeightedScan
LEAN_NUM_THREADS=1 lake env lean topics/21-dag-spectral/verification/CriterionSelectorReview.lean
```

Both passed. The expanded preserved audit samples sixteen declarations,
including the actual produced-list endpoints, the single-contrast path cost,
and the polynomial weighted scan cost. Every sample uses only `propext`,
`Classical.choice`, and `Quot.sound`.
