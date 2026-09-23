# Independent review of the rational envelope algorithm

Status: the executable envelope, exact evaluator, and declared arithmetic
and schoolbook bit-cost model pass this review. The final combined theorem
is present and targeted checks passed. The scope limits below are part of
this result; the review does not certify compiled runtime.

The reviewer read `ManySortCost`, `ManyParallelLines`, `ManyFastEnvelope`,
`ManyStackGeometry`, `ManyFastConstruction`, `ManyFastSegments`,
`ManyFastDominance`, `ManyFastEvaluation`, `ManyFastSize`,
`ManyAlgorithmSize`, `ManyRationalSize`, `ManyEuclidCost`, `ManyBitCost`,
`ManyFastOperandSize`, and `ManyEvaluatorBitCost` in
[the proof directory](../../Formal/ReciprocalAnchor). The review concerns
MR30–MR34 and the algorithmic parts of MR37 and MR41. It does not establish
correct execution of the separate Python script.

## Actual construction and correctness

The fast producer is an executable rational algorithm. `countedSort` uses
merge sorting with enough depth, proves both permutation and sortedness,
and counts every rational key comparison. Its bound is
`N * (Nat.log2 N + 1)`. `parallelDedup` retains a highest-intercept line
among each group of parallel lines; its output uses input lines, has
strictly increasing slopes, and preserves pointwise domination. This
includes duplicate lines and equal intercepts.

The stack's `push` deletes a middle line only after proving that it is
pointwise dominated by its neighbors. Its cost identity charges additional
tests against deleted lines. `scan_good` and `buildStack_good` establish the
geometric invariant from the sorted input. A good stack is not an assumption
of the public producer theorem. The distinct slopes make adjacent
intersection denominators positive; nonredundancy orders those
intersections strictly.

`segments` clips those intervals to the supplied endpoints. The proofs
establish interval bounds, retained active lines, their dominance over every
original input line at every real point, and adjacency over the entire box.
The output has at most `N` segments. The domination proof is substantive:
`valueReal` includes an artificial zero baseline, but the later
`Dominates` proofs show domination by actual retained lines. For the source
family the zero line is genuinely present, so `built_segments_valueReal`
correctly identifies the maximum on every produced segment.

`fastLowerMoment` feeds the source lines into this producer and sums the
exact rational integral formula over its output. `fastLowerMoment_eq`
proves equality to the real `lowerMoment` for `0 < a` and `a <= b`. It
requires no supplied active partition, feasible candidate, nonzero leaf
count, or trusted envelope oracle. Zero leaves, parallel source lines,
clipping at an intersection, and a degenerate interval are covered. This
establishes the substantive construction and evaluation claims in MR30,
MR32, and MR33.

## Arithmetic-operation accounting

`buildStack` counts rational comparisons in sorting and parallel-line
removal, plus a conservative twelve rational primitive operations per
visited stack position. Inspection of `Redundant` supports that charge:
there are at most four comparisons, three subtractions, three products,
and one addition. List traversal, natural-number indices, allocation, and
counter arithmetic are outside this rational-operation model. Their
ordinary structural work must not be described as included in the
returned count.

The review found two issues in the first clipping charge: repeated textual
intersection computations and a separately executed `segmentsCharge` pass.
The author changed both recursive definitions to share each intersection
with a `let` and changed `buildSegments` to charge both traversals. Its
resulting bound is `N * (Nat.log2 N + 37)`. This is a conservative bound
for envelope construction in the stated rational-operation model; it does
not rely on a compiler erasing the counter pass.

`ManyBitCost.actualEvaluatorCharge` adds source construction and exact
integration to that producer count. Review found that the initial constants
missed signed-slope negation and the final addition to the tangent term.
The revised charge uses sixteen operations per emitted segment, six per
source line, and eight setup operations. Its bound is
`N * (Nat.log2 N + 61) + 20`. These conservative constants cover those
operations, including accumulation and sign changes. The model treats
fixed small powers as arithmetic expressions and does not claim to count
compiled instructions.

## Rational sizes and the remaining bit-complexity boundary

`RationalBits` bounds the actual reduced numerator and denominator. Its
arithmetic lemmas prove that reduction does not increase either component,
handle zero under Lean's rational operations, and give polynomial bounds
for addition, subtraction, multiplication, inversion, and division.
These are meaningful representation-size results, not assertions about an
unrelated symbolic size function.

The size chain reaches the actual fast output: retained line coefficients
come from the original source lines; every emitted knot is a box endpoint
or an intersection of two original lines; each emitted segment integral
has a linear bound in input bit size. `fastLowerMoment_bits` gives
`5*B + 5 + (2*n+2)*(52*B+70)` for the answer. The stack comparison products
and intermediate sums are also covered by dedicated size lemmas. Thus
the proofs establish polynomial sizes for the relevant rational data,
including the terms used in exact comparisons.

`ManyEuclidCost` supplies an actual Euclidean algorithm, proves that it
returns `Nat.gcd`, bounds its number of remainder steps by twice the
operand bit length, and bounds the later operand sizes. `ManyBitCost`
adds an explicit schoolbook cost model: multiplication charges digit-row
formation and accumulation; long division charges a shift, comparison,
and subtraction for each dividend digit. Normalization uses the actual
Euclidean iteration count and two final quotient operations.

The raw-component lemma bounds unreduced numerators and denominators
before gcd reduction. Thus the normalization argument does not incorrectly
substitute the final reduced size for a potentially larger intermediate.
All modeled primitives, including negation and exact comparison, have a
uniform bound of `256 * (K+1)^3` for operands of at most `K` bits. The
cost of a comparison includes its integer cross-products.

`ManyFastOperandSize` bounds the relevant operand families: source
coefficient formation, coefficient comparisons, any input-line pair
intersection, any input-line triple's redundancy test, tangent setup,
each produced integral formula, and every accumulating partial sum.
These are expression families that overapproximate the evaluator's
operands, not an automatically extracted operational trace. Inspection
found them consistent with the executable expressions. Combined with
the construction-dependent operation charge, they support the explicit
polynomial schoolbook bit-work budget.
`evaluator_schoolbook_bound` packages the actual construction-dependent
charge bound, all operand-family width bounds, and the polynomial budget
under only the original rational input-size assumptions.
`evaluator_primitive_bitCost` applies the raw-component and gcd cost bounds
to every modeled primitive on those operands. No feasibility, guessed
partition, or trusted stack premise is needed.

The model boundary must remain explicit. The digit-loop costs describe
standard schoolbook arithmetic; these modules do not implement binary
digit multiplication and long division and prove refinement of those
implementations. The actual Euclidean recursion is proved, while its
individual division steps use that schoolbook cost model. The final
budget is a theorem about this declared mathematical model, not a theorem
about Lean's `Rat` implementation, compiler, memory allocation, or CPU
instructions. List/index bookkeeping is outside the rational-arithmetic
charge. The separate Python implementation also has no refinement link.

For MR34 and the runtime portions of MR37/MR41, coverage should say
“polynomial bit-work bound in the declared schoolbook rational-arithmetic
model,” accompanied by these scope limits. A claim of verified compiled
running time would exceed the statements. This boundary does not weaken
the exact hull or evaluator equality theorems.


## Executable cut extraction

The later `ManyFastSeparation` and `ManyFastCutSize` additions also pass
source review. A finite linear search recovers an original source index
for each retained numeric line. Distinct source lines may coincide at the
candidate; selecting any matching source is sound, because every source
line lies below the envelope globally and the selected line agrees at
the candidate. The proofs establish an actual rational coefficient vector,
global validity, and exact candidate equality. Source lookup adds at most
a quadratic number of comparisons; coefficient materialization has a
polynomial charge and coefficient/partial-sum size bounds. This does not
change the sharper `O(N log N)` claim for envelope construction itself.


## Targeted checks

The reviewer ran, from `formal/`:

```sh
lake env lean -DwarningAsError=true topics/13-many-leaf-reciprocal/verification/ReviewAlgorithm.lean
```

The command passed. The [saved output](verification/review-algorithm.log)
records executable checks for zero leaves (mean two: `1/2`), both mean
endpoints (`1`, `1/3`), zero/full leaf masses (`1/2`), a degenerate box
(`1/2`), and the exact two-leaf example (`31/50`). These checks are small
execution checks alongside the general proofs, not substitutes for them.
Axiom inspection of `fastLowerMoment_eq`, `buildSegments_cost`,
`evaluator_schoolbook_bound`, `evaluator_primitive_bitCost`, and
`countedEuclid_gcd` reported no axioms outside `propext`,
`Classical.choice`, and `Quot.sound`.

No project-wide verification or CI inspection was run. The integrating author separately reported a passing targeted
`--wfail` build of `ManyEvaluatorBitCost`. The final topic verification
record must identify its own targeted commands and logs.
