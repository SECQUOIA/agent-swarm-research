# Independent algorithm review

Reviewer: `threshold_independent_algorithms`, 2026-09-19. This reviewer did not
author the proof modules reviewed here. Scope: FC09, FC18–26, FC44, and FC54–60.
Review is limited to topic 15. No project-wide build or CI inspection was run.

Status: complete. The final targeted builds, boundary executions, and generated
call inspection passed. No unresolved finding remains in this review's scope.
The cost-model boundaries below remain part of the verified claims.

## Source grouping and exact rational oracles

The actual query path generates the original reduced rows, caches gadget
residuals and endpoint masks, and stores each minimizing row's identifier.
`ThresholdGrouping.group_minimum` proves both provenance and minimality.
`packed_constraints` identifies the partial table with the original reduced
system. Absent keys remain `none`; zero-normal rows are checked separately in
the small libraries. The completeness arguments do not insert proof-only
completion bounds into returned cuts.

`packedOracle_separates_real` keeps the selected row identifiers fixed and
proves validity at arbitrary real comparison points with matching normals.
`ThresholdPattern` transfers that premise from equality of the observation
pattern. Thus validity is not confined to rational comparison points or to the
row minimizers selected at a second query.

The cofactor preprocessor enumerates actual finite candidates, performs exact
determinant and gcd computations, and checks positivity and cancellation in
every original coordinate. `ThresholdPreprocessMinimal` rules out repeated
support indices in accepted candidates and constructs the corresponding
positive circuit. Repeated *representations* of one mathematical circuit are
allowed, which the coverage document correctly distinguishes from the exact
small-dimensional circuit counts.

## Recovery and original-domain admission

`bounded_polyhedron_has_basis` does not assume a full-dimensional feasible set.
It proves that the active normals span the ambient space at an extreme point.
`packed_realPartialSet_bounded` supplies boundedness from actual coordinate box
rows, rather than assuming it externally. The basis library includes the empty
basis in dimension zero. Missing directions cannot appear in the nonsingular
basis used by the completeness proof.

Every returned basis candidate is validated against all present inequalities.
`recoverPackedProfile_success_iff` therefore proves exact recovery from a real
feasible profile, with no online LP oracle. The rational greedy allocator stores
its arrays and proves capacities, observed entries, and exact sums, including
zero capacities and zero weights. Normalization branches before division when
the weight is zero. `checkedWitness_positive_decomposition` filters zero-weight
states from the delivered convex combination and preserves the exact moments
and total weight one.

`membershipRun_correct` and `checkedWitness_success_iff` compose the actual
domain precheck with the actual general oracle or cached-basis witness pipeline.
Their residual-unobserved hypotheses remain explicit. `ThresholdAmbientDescription`
also makes the independently supplied b-flow coordinates and their balance
equations explicit, so the eliminated coordinate is not mistaken for a free
ambient coordinate.

## Cost and operand review

The mask cache uses direct indexed keys. The proved compiler replacement
`subsetMask_eq_counted` uses shifts and additions, and the word ledger includes
mask generation, indexed grouping, and source/circuit traversal. Query caches
are distinct from the dimension-only circuit and basis preprocessing.

The rational row bounds cover both cached residual sums and source right-hand
sides. Circuit operand bounds cover arbitrary partial sums for all tested
selections. Basis operand bounds quantify every cache entry, including rejected
candidates and their validation dot products. `ThresholdPipelineSize` now
derives returned profile, flow, atom, and product widths directly from original
input widths; it no longer leaves the recovered profile width as a caller's
assumption. Greedy residual and normalization bounds cover the remaining
recovery intermediates.

`ThresholdObservedBits.observedCache_inputBits` derives the actual compressed
instance width `3+(a+1)(B+1)` from original input widths, without feasibility
assumptions. Thus the generic profile and recovery encoding results also apply
after cached observed-label compression.

The ledgers are mathematical arithmetic and word models, not refinements of
Lean's compiled rational implementation. The basis trial ledger counts a fused
multiply-accumulate as one work unit, whereas the circuit ledger charges a
multiplication and addition separately. Exact combined primitive-operation
claims need the explicit factor-two conversion; the asymptotic statements are
unaffected. `scanBases_primitive_charge_le` and `recoverWitness_primitive_work`
now supply that conservative conversion.

The recovery ledger bounds rational arithmetic and emitted coordinates.
`greedyFill` returns a nested function, subsequently materialized by coordinate
lookups; its structural lookup cost is not part of the arithmetic ledger. The
packed-oracle word-operation theorem must not be extended to a claim about the
full recovery program's compiled runtime without a separate structural proof.

## Merger boundaries

The convex weighted-copy theorem requires a nonempty convex set and correctly
handles both an empty index family and zero total weight. Original simplex
constraints survive observed-label merging. Observation membership is structural,
so an observed label with zero weight is retained. Rational refinement proves
the scaled-flow constraints and totals, and the zero-total case is explicit.

The common normalized flow and constituent weights are a compact representation.
Its expansion is proved equal to proportional refinement. The storage theorem
counts a sum of the weight and flow sizes; the dense alternative counts their
product. The no-observation theorem applies with arbitrarily many unused labels.

## Integration findings sent to owners

1. Resolved at the domain interface: `ThresholdDomainOracle` scans actual
   tagged domain margins and both signs of simplex equality, returning a literal
   affine expression. It proves exact acceptance, strict query violation,
   validity throughout the real original domain, and unit coefficients.
   `ThresholdDomainOracleCost` counts every evaluation and comparison.
   `ThresholdSeparation` now composes it with the profile separator.
   `separateThree_none_iff` and `separateGeneral_none_iff` concern the actual
   original hull; their soundness theorems prove strict query violation and
   validity at arbitrary real hull points with the same observation pattern.
   The three-label output is a literal unit expression; the general output
   preserves compact weighted source-row representation. The complete
   three-label charge is bounded by `1033*L+3228`.
2. Domain margin and weight-scan intermediate bit bounds were missing from the
   initial final pipeline. Resolved by `ThresholdDomainSize`: actual domain
   margins, all four subtraction intermediates, and arbitrary sublists of the
   original weight sum have proved bounds. Independently inspected and built.
   `ThresholdDomainOracleSize` extends this to the literal separating-expression
   evaluator: `DomainEvalBits` recursively covers every AST node and the hidden
   b-flow subtraction intermediates. Both simplex signs and all actual scan
   operands have bounds from `InputBits` alone.
3. Resolved: `ThresholdUnitOracleExpression` proves that actual returned source
   expressions have at most 903 syntax nodes. `ThresholdUnitOracle` discharges
   `Repairable` from those rows, accounts for each recursive coefficient query,
   and proves the repaired cut strictly violates the query and remains valid
   at every real hull point with the same observation pattern. No query-domain
   premise is needed for this profile-cut theorem. The output coefficient
   conclusion concerns flow and product coordinates, as claimed in the paper.
4. The observed-label terminal must instantiate the downstream query/witness
   algorithm, retain original simplex admission, and cache both the observed
   index enumeration and merged residual. The merger owner was notified.
   `compressObserved_hull_iff` now proves the semantic compressed-data bridge.
   The original residual weight is an independent `RationalData` field: checking
   only explicit-weight nonnegativity and their sum at most one is insufficient
   unless its equality to the cached residual is checked as well. This boundary
   was communicated to the terminal owner.
   The actual cache now materializes all compressed fields, forward labels and
   reverse ranks. Array mapping replaces repeated index enumeration and uses
   actual array lengths in its inner loops; the merged residual is stored once.
   `originalWeightsRun` in the terminal checks every original weight, including
   the independently stored residual, for nonnegativity and exact total one.
   `observedWitness_cached_decomposition` now proves the exact original moments
   and graph membership for the returned output's actual rank-table flow lookup.
   The complete membership and recovery ledgers instantiate the concrete cached
   pipeline and include copying original weights; explicit parameter-overhead
   theorems give the stated quadratic-exponential dependence on observed count.
   The separator combines full-weight rejection with the actual compressed
   separator and transfers validity to arbitrary real original hull points.
   Its fixed observation-index map supplies the compressed cut's interpretation.
   `ThresholdObservedFiniteDescription` completes the small-observed transfer:
   actual affine pullback preserves every flow/product coefficient, omitted
   products receive zero coefficients, and a complete finite unit family is
   proved for every observed count at most three. `ThresholdObservedSmall`
   supplies the corresponding exact zero-, one-, and five-test criteria for
   observed counts zero, one, and two, always retaining the original simplex.
5. During root integration, separately compiling small-label modules revealed
   a shared autogenerated name for their local `NeZero` instances when the
   modules were imported together. The root assigned explicit distinct names.
   The final combined topic import and axiom audit must check this integration
   boundary; successful individual builds alone do not establish it.
   The preserved independent probe now imports all three small-label libraries
   together and passes after that correction.
6. A targeted inspection of generated C confirmed that implicit observed-count
   arguments still evaluated `labels.toFinset.card` through list deduplication
   in the cache rank call and downstream membership/witness calls. This does not
   change the rational arithmetic ledger, but can add structural work outside
   the intended cached-index model. The helper and merger owners are replacing
   these runtime arguments with cached array sizes and checking the emitted
   calls. The membership, witness, and separation entry points now use
   `lean_array_get_size` of the cached label array; their generated C contains
   no deduplication call. The cache rank helpers are now inlined, eliminating
   the final unused dimension argument. Independent generated-C inspection
   confirms no deduplication, finite-set cardinality, or order-isomorphism call
   in any of the four actual cache/query entry-point bodies. This is a targeted
   implementation check, not a general compiler or machine-runtime proof.

## Targeted commands actually run

From `formal/`:

```sh
lake build Formal.NetworkSimplex.ThresholdOracleExamples Formal.NetworkSimplex.ThresholdBasisOracleSize Formal.NetworkSimplex.ThresholdPreprocessOperands Formal.NetworkSimplex.ThresholdPipelineSize Formal.NetworkSimplex.ThresholdKeys --wfail
```

Passed. `ThresholdOracleExamples` contains kernel-checked executions for absent
pair directions, circuit rejection, and rejection returning the actual violated
zero-normal endpoint row.

```sh
lake build Formal.NetworkSimplex.ThresholdResults Formal.NetworkSimplex.ThresholdPositiveAtoms Formal.NetworkSimplex.ThresholdOnePacked Formal.NetworkSimplex.ThresholdTwoPacked Formal.NetworkSimplex.ThresholdPreprocessMinimal Formal.NetworkSimplex.ThresholdConvexMerge --wfail
```

This attempt overlapped an in-progress `ThresholdDetTrace` edit and failed at
line 113 (`rfl` supplied for `True`). The owner was notified; this attempt is not
reported as passing. A frozen-source rerun remains to be recorded below.

```sh
lake build Formal.NetworkSimplex.ThresholdResults Formal.NetworkSimplex.ThresholdPositiveAtoms Formal.NetworkSimplex.ThresholdOnePacked Formal.NetworkSimplex.ThresholdTwoPacked Formal.NetworkSimplex.ThresholdPreprocessMinimal Formal.NetworkSimplex.ThresholdConvexMerge Formal.NetworkSimplex.ThresholdDomainSize --wfail
```

Passed after the owner fixed `ThresholdDetTrace`. This rerun includes the newly
completed domain-operand module and the positive-only witness theorem.

```sh
lake build Formal.NetworkSimplex.ThresholdObservedHull Formal.NetworkSimplex.ThresholdAmbientDescription Formal.NetworkSimplex.ThresholdDomainSize Formal.NetworkSimplex.ThresholdPipelineSize --wfail
lake build Formal.NetworkSimplex.ThresholdUnitOracle --wfail
```

Both passed. The first includes the literal rational compression hull theorem;
the second checks the executed unit repair and its expression-size accounting.

```sh
lake build Formal.NetworkSimplex.ThresholdDomainOracleCost --wfail
```

Passed. The tagged domain separator and its arithmetic charge are independently
checked; the subsequent wrapper check below covers composition with the profile
oracle.

```sh
lake build Formal.NetworkSimplex.ThresholdSeparation --wfail
lake env lean -DwarningAsError=true /tmp/threshold-algorithm-review.lean
```

Both passed. The five kernel-checked boundary executions in the second command
cover empty-basis recovery in dimension zero, rejection of an invalid original
residual weight by the actual domain separator and witness wrapper, omission of
a zero-weight state, and successful recovery with that zero-weight state.
The probe is preserved as [ReviewAlgorithms.lean](../verification/ReviewAlgorithms.lean).

```sh
lake build Formal.NetworkSimplex.ThresholdDomainOracleSize --wfail
```

Passed. The source review verified that its recursive operand predicate covers
both the explicit AST and the arithmetic hidden by the b-flow coordinate lookup.

```sh
lake build Formal.NetworkSimplex.ThresholdOnePacked Formal.NetworkSimplex.ThresholdTwoPacked Formal.NetworkSimplex.ThresholdSeparation --wfail
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/ReviewAlgorithms.lean
```

Both passed. The preserved probe now also verifies that the one-, two-, and
three-label oracle modules can coexist in one import environment.

```sh
lake build Formal.NetworkSimplex.ThresholdObservedCache --wfail
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/ReviewAlgorithms.lean
```

Both passed. The probe now has seven kernel-checked boundary executions,
including duplicate observation labels and retention of a structurally observed
label whose weight is zero. The cache source review confirmed materialized
forward/reverse indexing and a single cached merged residual.

```sh
lake build Formal.NetworkSimplex.ThresholdObservedReal Formal.NetworkSimplex.ThresholdObservedCache Formal.NetworkSimplex.ThresholdObservedParameterCost --wfail
lake build Formal.NetworkSimplex.ThresholdObservedRecovery Formal.NetworkSimplex.ThresholdObservedAlgorithm Formal.NetworkSimplex.ThresholdWeightSeparator --wfail
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/ReviewAlgorithms.lean
```

All passed. The final probe now has nine kernel-checked executions. Its final two
checks exercise the concrete observed membership and witness wrappers: an
invalid original simplex is rejected even though compression alone would
replace its residual with one.

```sh
lake build Formal.NetworkSimplex.ThresholdObservedFiniteDescription Formal.NetworkSimplex.ThresholdObservedSeparation --wfail
lake build Formal.NetworkSimplex.ThresholdObservedSmall --wfail
```

Both passed. Actual finite original-coordinate unit families and all three
small-observed criteria were inspected, including their original simplex rows.

Final frozen-source checks:

```sh
lake build Formal.NetworkSimplex.ThresholdObservedSeparation Formal.NetworkSimplex.ThresholdObservedRecovery Formal.NetworkSimplex.ThresholdObservedFiniteDescription Formal.NetworkSimplex.ThresholdObservedSmall --wfail
lake build Formal.NetworkSimplex.ThresholdObservedBits --wfail
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/ReviewAlgorithms.lean
python3 topics/15-flat-chain-threshold/verification/ReviewGeneratedCalls.py
```

All passed. The last script checks the four generated cache/query entry-point
bodies for the specific hidden-cardinality regression and confirms cached array
size use. It does not assert general compiled-runtime correctness. One initial
attempt to launch the final build from the repository root returned a missing
Lake configuration error; the recorded final command was rerun successfully
from `formal/`.
