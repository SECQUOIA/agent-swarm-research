# Independent review: normalization assembly

Reviewed `NormalizationTrials`, `NormalizationAtoms`, `NormalizationData`,
`NormalizationComplete`, `SortedTrial`, `IndexedFactors`, `GraphInput`, and
`RangeObstruction`, and the completed `NormalizationInput`. The reviewer did not author those modules. `FactorRange`
and the underlying LDL producer were authored by this reviewer and are not
claimed as independently reviewed here.

Verdict: **PASS for the reviewed normalization assembly, including its
constructor from the original rational PSD prior and atoms**. This review
does not certify the final all-trials graph producer or its bit-work bound.

## Actual labels and sorted trials

`IndexedFactors` flattens the actual LDL lists in owner order and then list
position, using `finSigmaFinEquiv`. Its explicit offset theorem gives the
sum of preceding owners' list lengths plus the local index. It does not use
an arbitrary finite equivalence. Zero matrices contribute no labels;
singular matrices retain their actual nonzero factors. Prior owner zero is
mapped to `none`, and each subsequent owner to its original edge identity.
Owner reconstruction is proved from the actual factor lists. The total
label count is at most `p*(m+1)`.

Trials are subsets of labels of cardinality `r`, listed in the increasing
order supplied by the subset. The unfiltered number is exactly `M.choose r`;
independence filtering only decreases it. `SortedTrial` uses maximum volume
in the existence proof, then explicitly reindexes its chosen basis into
that same sorted order. No ordered-tuple enumeration, factorial count, or
maximum-volume optimization is introduced into the algorithm. Rank zero
uses the single empty candidate rather than requiring a positive dimension.

The scales are produced by rational dyadic arithmetic, with proved
`1 <= scale^2 * weight < 4`. `transformCode`, `restoreCode`, and
`acceptsAtomCode` use the rational inverse producer and are proved equal to
the semantic normalization maps and tests. The square roots in the
maximum-volume proof do not become input computations.

## Survival and exact range

`FactorData` contains atom reconstruction, positive weights, and at most
`p` factors per owner. `exists_accepted_trial` derives a trial for every
selected owner set from those facts. It does not take a successful trial,
a coordinate bound, or a target basis as an additional hypothesis.

The selected original information matrix is exactly the sum of the selected
rank-one factors. Its rank equals the dimension used by trial enumeration.
The maximum-volume argument gives coordinate magnitude below two for every
selected weighted factor. The proof converts that real statement to the
rational squared bound, proves the exact rational projector fixes each
factor, and sums at most `p` factors for each original atom. This establishes
the actual per-atom diagonal test `<= 4*p`, including the prior.

Forced owners are a set union of optional edge owners. A prior label forces
no edge; repeated labels from one atom force that edge only once. Every
forced edge belongs to the target selection and their number is at most
`r`. Containment of the chosen factors supplies the normalized lower bound
`I <= J`. The projector test supplies range containment. Together they prove
that each accepted information matrix has exactly the trial range, rather
than merely lying in it. Hence subsequent relative comparisons cannot
silently replace a singular matrix by one on a different subspace.

The rank-zero equivalence is about the original matrices: the selected
information has rank zero exactly when the prior and every selected atom
are zero. There is no positivity or nonemptiness exception that excludes
this case. The graph algorithm's separate zero-rank branch remains a later
assembly obligation.

## Original-input bridge

`producedData` fills every `FactorData` field from the indexed LDL output of
the original prior and atoms. Positivity follows from their real-cast PSD
assumptions; reconstruction uses the original owner fibers. The fiber
cardinality is proved equal to that owner's actual LDL list length, so the
per-owner bound is derived rather than supplied by a caller.

`original_input_trial` specializes the generic survival theorem to
`Q0 + sum_{a in S} Q a`, substitutes its actual real matrix rank, and returns
executable acceptance and normalization maps. Its exact-range conclusion
and forced-owner bound concern that same original matrix. It has no hidden
factorization, basis, good-trial, or positive-rank premise.
`original_input_size` supplies the actual flattened label and binomial
trial counts. The independent client also specializes the rank-zero theorem
to the original prior and atoms, checking that this boundary crosses the
interface without another hypothesis.

## Graph input and obstructions

`checkDAG` checks every actual edge endpoint against the supplied vertex
order. Its successful result preserves the endpoints and proves strict
increase; rejection is equivalent to an edge that fails that check.
`checkDAGWithOrder` first applies a supplied permutation. This is a validator
of an ordering, not a topological-sort algorithm. That matches the option to
verify an ordering in G01; callers must keep source and sink in that order.

`RangeObstruction` proves arbitrarily close rational rank-one PSD matrices
can have different kernels and fail multiplicative domination in both
directions. Its explicit two-parallel-edge graph also shows why deleting a
Loewner-dominated path can destroy a small-error relative cover. The examples
use actual feasible edge lists, not abstract matrix labels with assumed
path realizations.

## Independent targeted checks

From `formal/`, with Elan on `PATH` and `LEAN_NUM_THREADS=1`:

- `lake build --wfail Formal.DAGSpectral.ProfileDPExecution Formal.DAGSpectral.NormalizationComplete Formal.DAGSpectral.GraphInput Formal.DAGSpectral.RangeObstruction` — passed.
- `lake build --wfail Formal.DAGSpectral.NormalizationInput` — passed.
- `lake env lean topics/21-dag-spectral/verification/NormalizationReview.lean` — passed.

The client uses `native_decide` as an executable smoke check for a zero prior
and two singular rational atoms, including exact factor ownership, weight,
and vector coordinates. It checks binomial and empty-trial counts, prior
and repeated-edge owner handling, and graph-order acceptance/rejection,
including a supplied reversed permutation. These smoke checks are separate
from the universally quantified proof modules. The six printed theorem
axiom sets contain only `propext`, `Classical.choice`, and `Quot.sound`.
No project-wide verification or CI inspection was performed.
