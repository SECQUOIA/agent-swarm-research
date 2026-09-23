# Exact rational algorithms

The query algorithms use original profile rows. They retain the identifier of
whichever original row attains each group minimum. Missing normal groups remain
absent. A zero-normal group receives a separate direct nonnegativity test.
Consequently, a returned cut never acquires an artificial positive-subset box row.

## Source rows, grouping, and cuts

- `ThresholdRationalRows`: rational input data, cached residuals and subset keys,
  and all `(4m+2)(L+1)` original reduced row tags. `indexedRows_constraints`
  identifies their rational values with the real reduced profile system.
- `ThresholdKeys`: direct subset masks and canonical negative-normal keys.
  Coincident normals in dimensions zero and one share a key. The proved compiler
  simplification `subsetMask_eq_counted` makes mask production use shifts and
  additions. `keyNormal_packNormal` proves exact decoding.
- `ThresholdGrouping`: an indexed array of optional minima. `group_minimum`
  proves source-row provenance and minimality; `group_real_constraints_iff`
  proves equivalence with every original inequality.
- `ThresholdCircuitOracle`: executable selection and exact rational circuit
  evaluation. Zero weights do not require a present row. Rejection returns
  integer weights and original row identifiers, a compact affine-cut encoding.
- `ThresholdDenseOracle`: exact agreement between the executed circuit scan and
  finite partial-table circuit tests.
- `ThresholdPackedOracle`: the concrete packed source-row pipeline.
  `packedOracle_separates_real` proves strict violation at the rational query and
  validity at every real feasible comparison point with the same row normals.
  The selected rows remain fixed when the cut is evaluated elsewhere.

## Complete acceptance criteria

`ThresholdThreePacked.threeOracle_none_iff` proves that the actual sixteen-test
oracle, together with its zero-normal check, accepts exactly when the original
three-label reduced profile system has a real solution. It uses
`ThresholdThreeCompleteness.three_partial_feasible_iff`; absent directions are
handled by a proof-only completion argument and are never inserted into the
query or its returned cut.

`ThresholdGeneralPacked.generalOracle_none_iff` gives the corresponding result
in every dimension for the actual finite output of `preprocessCircuits`.
`ThresholdPreprocessCriterion` proves completeness of those computed circuits.
The cached general library is supplied to `generalOracle`; it depends only on
the number of labels and is not recomputed per original row.

`ThresholdResults.membershipRun_correct` composes the actual domain checks and
profile oracle into exact original-hull admission. `checkedWitness_success_iff`
and `checkedWitness_sound` give the corresponding complete graph-witness
interface. `ThresholdPositiveAtoms` filters the cached atoms to positive weights,
preserving total weight one and every original moment; this adds at most
`2(m+1)` state visits and emitted indices.

`ThresholdSeparation` returns an actual violated cut for either kind of failure.
`separateGeneral` returns a domain expression or a compact integer-weighted list
of original profile rows. `separateThree` returns a literal affine expression
with unit flow/product coefficients, using `ThresholdUnitOracle` to add or
subtract a proved gadget balance when necessary. Their acceptance theorems are
exact original-hull equivalences, and their returned inequalities are valid at
all real hull points sharing the observation pattern. The three-label complete
separator has proved work at most `1033L+3228`, including domain rejection.

## Cost and representation bounds

`ThresholdPackedOracle.packedOracle_arithmeticCharge` bounds cached source-row
construction, actual grouping comparisons, and actual circuit arithmetic by
`26m(L+1)` plus the fixed library charge. For three labels,
`ThresholdThreePacked.threeOracle_charge` gives `78(L+1)+371`.
For arbitrary positive `m`, `ThresholdGeneralPacked.generalOracle_charge` gives

```
26m(L+1) + 2^(4(m+1)^2)(2m+3).
```

`ThresholdOracleWork` also accounts for the actual cached-mask counts, indexed
grouping accesses, and a conservative allowance for the explicit row and circuit
traversal loops. Its three-label word-model bound is `300(L+1)+1543`. This is
before input observation normalization and the original-domain admission checks.
The word model treats a shift or indexed access as one operation. Normal keys
use `O(m)` bits; row, gadget, and array indices also require the bits needed to
address the input. This is not a compiled instruction or allocation count.

`ThresholdOracleSize` bounds each actual cached row by `(2m+6)(B+2)` numerator
and denominator bits for `B`-bit original rational fields.
`ThresholdOracleBitCost` covers all tested circuit selections, products,
arbitrary partial sums, cached residual expression intermediates, and grouping
comparison operands. It combines the actual rational-operation ledger with the
schoolbook arithmetic model reused from topic 13. For three labels, its bit-work
bound is

```
(78(L+1)+371) * 256 * (132B+299)^3.
```

These are mathematical cost-model results with proved operand bounds. They do
not refine Lean's compiled `Rat` implementation or a binary-machine program.
The integer preprocessing and cached-basis modules supply their separate
parameter-only work and representation bounds. `ThresholdPreprocessOperands`
covers the validation and normalization intermediates, including rejected
candidates. `ThresholdBasisPreprocess` includes the exponential preprocessing
bound; `ThresholdPipelineSize` carries original input bounds through actual
returned basis profiles, restored profiles, state flows, and normalized atoms.
`ThresholdDomainSize` and `ThresholdDomainOracleSize` cover the domain scans.

The basis-trial ledger counts a multiply-accumulate as one work unit. The
`scanBases_primitive_charge_le` and `recoverWitness_primitive_work` theorems
convert it to a conservative primitive rational-operation bound by a factor of
two. Recovery bounds count rational arithmetic and written output entries;
they do not count structural traversal of nested finite functions. The packed
oracle's separate word-model bound should not be read as a word-runtime claim
for every recovery routine.

## Observed-label input and compact output

`ThresholdObservedCache` materializes the sorted distinct label array, reverse
rank table, all compressed data fields, and the merged residual weight. The
rational compressed-data lookup uses these arrays; it does not recompute a
label enumeration or residual sum. The observation list may contain duplicates.
Its coverage contract retains every structurally observed label, including
labels with zero weight. The full original simplex is checked separately.

`ThresholdObservedHull` and `ThresholdObservedReal` prove the compression
identity for the actual rational and real chain hulls. `ThresholdObservedAlgorithm`
instantiates the membership and witness programs on that cached input.
`ThresholdObservedSeparation` returns an original-weight cut or a compressed
cut together with its fixed label substitution, and proves strict violation and
validity at every real original hull point.

Writing `a` for the number of distinct listed labels, their complete query-work
bounds have the form `O((a+1)L + labels.length + m) + 2^(O(a²))`. The supplied
list is the structural observation metadata; when it lists one label per
observation, its length is at most the observation count. The original `m+1`
weight scan is included. Parameter-only circuit and basis preprocessing remains
separate from online query work.

The witness stores original weights once and references compressed normalized
flows through the cached rank table. `ThresholdObservedRecovery` proves that
those actual lookups produce graph atoms and recover every original moment.
The normalized decomposition payload has `(m+1)+(a+1)(2L+1)` flow/weight
entries, plus linear label/rank bookkeeping. This is not the total size of the
returned `ObservedRecovery`: it also retains compressed input data, restored
profiles, and unnormalized flows alongside the normalized atoms.
`observedWitness_compact_flow_size` bounds the payload formula; it does not
measure the returned structure. The retained data have the same
`O(m + (a+1)(L+1))` order. Materializing all original state-arc flows instead
requires `(m+1)(2L+1)` entries; compact recovery does not write that expansion.

## Targeted validation

The online pipeline modules were checked with explicit module-targeted
`lake build Formal.NetworkSimplex.<module> --wfail` commands.
`ThresholdOracleExamples` contains kernel-checked executions for acceptance with
absent pair groups, circuit rejection, and zero-normal rejection returning the
actual violated endpoint row. No project-wide local verification or CI checks
were run for this work.
