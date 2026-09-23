# Independent review: exact eigenvalue comparison and path information

Verdict: **PASS for exact comparator semantics, the complete rational
execution transcript and its polynomial arithmetic cost, and original
path-information size/arithmetic bounds.** This review does not certify the whole cover
producer's C05 cost or an E-optimal path selector.

Reviewed semantic modules are `EigenComparePSD`, `EigenCompareDifference`,
`EigenCompareBisection`, and `EigenCompare`; the exact separation and
coefficient-size foundations were also reviewed in
[bit-foundations.md](bit-foundations.md). The execution review covers
`EigenCompareCoefficientTrace`, `EigenCompareDifferenceTrace`,
`EigenComparePreprocessingTrace`, `EigenCompareTrace`,
`EigenCompareThresholdTrace`, `EigenCompareFinishTrace`,
`EigenCompareExecution`, `EigenCompareComplexity`, and the final stable
`EigenCompareExecutionCost`. The path-information
review covers `PathInformationBits`. All are in `formal/Formal/DAGSpectral/`.

## Exact PSD threshold test

For a real symmetric matrix `A`, the characteristic polynomial of `-A` is
the product of `X+lambda_i` over the actual eigenvalues, including their
multiplicities. If all eigenvalues are nonnegative, all its coefficients
are nonnegative. Conversely, nonnegative coefficients and monicity force
the polynomial to be positive at every positive argument. A negative
eigenvalue of `A` would provide such a positive root, a contradiction.

`rationalPSDTest` checks the `n+1` actual rational coefficients of `-A`.
The rational coefficient formula is proved equal to the characteristic
polynomial coefficient; higher coefficients are zero. Thus the Boolean
test is exact for symmetric matrices, including singular matrices and
repeated roots. Symmetry is an explicit premise of its correctness theorem;
the Boolean test alone is not a general nonsymmetric PSD validator.

`eigenThresholdTest A q` applies that test to `A-qI`. Its correctness theorem
proves equivalence to `q<=lambda_min(A)` for every rational threshold,
including exact equality. The final comparator supplies symmetry from its
original PSD premises. No real eigenvalue query is executed.

## Computed separation, bisection, and ties

The rational Kronecker difference has entries from `A` and `B` with the
appropriate identity factors. Multiplying it by the tensor product of two
nonzero eigenvectors proves that every eigenvalue difference is a root of
its characteristic polynomial. In particular, the difference of the two
actual minimum eigenvalues is a root. The polynomial is monic, nonzero,
and has degree `n^2`; reindexing by `Fin (n*n)` preserves it.

`eigenComparisonGap` computes all its rational coefficients and derives the
positive denominator/height separation bound. The earlier trailing-degree
argument handles zero coefficients and arbitrary multiplicity at zero.
There is no square-free factorization, isolated-root certificate, supplied
gap, or exact-real comparison premise. The nonzero-root bound is applied
only under an assumption that the minima differ; equality is not treated
as a positive gap.

The radius `1+sum_i |A_ii|+sum_i |B_ii|` is positive and bounds both minimum
eigenvalues above. PSD bounds them below by zero. `dyadicIndex` stores an
integer in `[0,2^t)` and queries rational midpoints. The interval invariant
is closed on both sides, so a minimum exactly at a midpoint is included.
After `t` steps the two lower approximations have error at most
`w=R/2^t`.

The chosen depth is the numerator digit count of `4R/gap`, not its numerical
magnitude. This proves `2w<gap`. If the minima coincide, their lower
approximations differ by at most `w`, hence strictly less than `gap-w`.
Conversely, being closer than `gap-w` contradicts the computed separation
if the minima differ. The two remaining signed threshold branches decide
the strict ordering. `compareMinimumEigenvalues_correct` proves all three
equivalences, with only PSD promises and positive dimension. Its Boolean
`minimumEigenvalueLE` wrapper therefore implements actual weak comparison,
including ties.

The comparator is a total computation on rational matrices, but its semantic
minimum-eigenvalue theorem requires nonempty dimension and PSD inputs.
These are the intended E-optimality hypotheses. No positive-definiteness,
simple-spectrum, or common-kernel premise is required.

## Actual execution transcript

`compareMinimumEigenvaluesWithTrace` executes the difference construction,
characteristic coefficient computation, denominator/height gap formula,
radius computation, depth ratio, both adaptive bisections, and final
comparisons. It uses the returned intermediate values. The equality
`compareMinimumEigenvaluesWithTrace_eq` identifies both its returned
ordering and its entire event transcript with the specified comparator and
trace. `compareMinimumEigenvaluesWithTrace_correct` then inherits the actual
eigenvalue correctness theorem; no threshold oracle is left as a premise.

Coefficient evaluation uses finite deterministically ordered minors and
permutations. Each expression is proved to evaluate to the actual minor or
coefficient. The trace includes matrix negation and coefficient sign tests.
The implementation evaluates all coefficients, so its count remains valid
even when a Boolean test could have stopped early.

Gap preprocessing records denominator multiplications, absolute-value
comparisons and sign changes, additions, the maximum-with-one comparison,
the product, and inversion. Radius preprocessing records both absolute
diagonal sums and its two additions. The adaptive search records the
midpoint arithmetic and the events returned by the actual threshold call;
the returned Boolean drives its next integer index. The final stage records
power construction and both rational comparison expressions, even when
the first already determines the ordering.

The operand-width lemmas include shifted entries, intermediate determinant
expressions, the full coefficient list, denominator products, midpoint
numerators/denominators, and final comparison operands. `EigenCompareComplexity`
derives the gap and radius widths and a linear depth bound from original
matrix-entry widths. It does not assume coefficient sizes or separation
as extra inputs.

These are arithmetic transcripts in the stated schoolbook model. Reading
canonical rational fields, integer digit counts, index updates, expression
construction, finite-data storage, and list traversal still need their
appropriate treatment in any complete Turing-work claim. The transcripts
are not advertised as timings of Lean's backend.

## Final comparator arithmetic-cost theorem

The frozen `EigenCompareExecutionCost` module derives a common event width
from the original `MatrixBits A C` and `MatrixBits B C` assumptions. It
covers each part of the full returned transcript, including both adaptive
searches. The base width is linear in `C`; the generic arithmetic-depth
factor depends only on dimension. In the bisection loop, query width grows
linearly with the step count, which is already bounded linearly in `C`.
The proof never applies an exponential arithmetic-depth recurrence across
all bisection steps.

The exact transcript length is bounded by fixed-dimensional preprocessing
work plus `2T*(T+thresholdTestOperations n+5)+T`. The quadratic term includes
reconstructing each query's dyadic power, both adaptive searches, and the
final power construction. Preprocessing includes the degree-`n^2`
characteristic coefficients, gap, radius, and depth-ratio arithmetic; final
comparisons are also counted.

Combining this quadratic length bound, linear depth and width bounds, and
the cubic schoolbook primitive bound gives

```
traceBitWork (eigenExecutionWidth n C)
  (compareMinimumEigenvaluesWithTrace A B).2
  <= eigenComparisonBitConstant n * (C+1)^5.
```

`compareMinimumEigenvalues_polynomial_bitWork` proves this with only original
entry-size assumptions and `C>0`; no gap, coefficient-size, root-separation,
or test-cost premise remains. The returned ordering's correctness is the
separate proved PSD theorem. Dimension is absorbed only into the explicit
constant. This is a complete bound for the recorded rational arithmetic,
with the global representation/control-work boundary stated above.

## Original path information and long sums

`rationalPathInformation` is the original rational matrix
`Q0+sum_(e in path) Q_e`. Its cast theorem identifies it with the real
`pathMatrix` used by the cover and criteria. There is no normalization
certificate or transformed-input premise.

`rationalSumRun` computes the actual sum and records each addition with the
already computed tail as an operand. `rationalPathEntryRun` applies it to
the prior followed by the actual path entries. It produces the correct
matrix entry and uses exactly `length(path)+1` additions, including the
final addition to zero. Negative off-diagonal entries and cancellations
are allowed.

For input entries bounded by `B` bits and path length at most `N`, both
values and actual intermediate operands have budget
`K=1+(N+1)*(B+1)`. This is linear in path length and input bits. It does not
use the exponential generic arithmetic-depth bound on an `N`-step chain.
The resulting proved rational arithmetic cost is

```
p^2 * (N+1) * 256 * (2+(N+1)*(B+1))^3.
```

The theorem handles empty paths, repeated entries in a general input list,
and dimension zero. For actual DAG paths the length premise comes from the
graph. Additional storage or path-recovery costs remain distinct from this
entry-summation cost.

## Targeted checks

From `formal`, with `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1`:

```
lake build --wfail Formal.DAGSpectral.EigenCompareExecution Formal.DAGSpectral.EigenCompareComplexity Formal.DAGSpectral.PathInformationBits
lake build --wfail Formal.DAGSpectral.EigenCompareExecutionCost Formal.DAGSpectral.PathInformationBits
lake env lean -DwarningAsError=true topics/21-dag-spectral/verification/ExactCriteriaReview.lean
```

Both targeted builds and the final client passed. The independent runtime
client checks singular PSD acceptance,
symmetric indefinite rejection, exact repeated-eigenvalue threshold equality,
a threshold strictly above it, equal irrational minima under coordinate
permutation, both strict comparison directions, singular ties with different
kernels, and a positive gap of `2^-80`. It also checks the instrumented
ordering and full trace, signed rational summation, and ten negative
off-diagonal contributions with exactly eleven additions including the
prior. It printed:

```
Thirteen exact-criteria and path-sum checks passed; equal-irrational trace has 1100 events.
```

The checks use `#eval` assertions and introduce no native-decision proof
axioms. The first client draft needed explicit `Ordering.eq/lt/gt` names;
no reviewed source was changed. Selected production axiom checks covered
the PSD coefficient criterion, rational PSD test, actual difference root,
three-way comparator correctness, instrumented-run equality/correctness,
linear depth, path-information size/cost, full execution event widths and
length, and the final degree-five bound. All reported only `propext`,
`Classical.choice`, and `Quot.sound`. No project-wide verification or CI
inspection was run.

Reviewed SHA-256 digests, rechecked after the final cost follow-up:

```
46d89dc64811808236d135124106d8889bba056d4808bfd5c4b8830b0eee90a3  EigenComparePSD.lean
d6dbfaec5970d8add09b611eee997e14ed756770fb342b8a022f30ec96c9a8d4  EigenCompareDifference.lean
c39b8c529c9aeea88df9d1bb1129ad28f25bdcba80ab0bd0bbe393ab0c38fa8e  EigenCompareBisection.lean
64284d6d340b6e2138f2735b7839ac3ebd700304b531eaba3cee2daa3235f149  EigenCompare.lean
716008b4eaf12f1805c60f2c0ef4678879bd6fb409a412bd49da238a39e5873f  EigenCompareExecution.lean
eba3c8f4a3a0d48aca5e12884e9aaa5bf7441335d0d4b0be2e8989b22d4fb308  EigenCompareTrace.lean
fb0fc962e040dd4d1ff33765ffa7325eb036092b19383f4d204e99d1202296ce  EigenCompareThresholdTrace.lean
28b77f5b9ee351f5103f20e1cda4b8d39c32d6427f3b8613fc8cb00e5c28954b  EigenCompareFinishTrace.lean
066dcabc1e3d1e320f0857148ecc997af556291c7246e5c9a51c089016ee4e11  EigenCompareDifferenceTrace.lean
57b0be18b8c09f28ddcd2cab0d946bf0b74e2a84cf892d8f4b00ebdbcafc62f9  EigenCompareCoefficientTrace.lean
d1cea62f0dca963ebf3df62c85b3673e3cd3e73a14bbf909a5dfac4034d97c64  EigenComparePreprocessingTrace.lean
eaa4f60a5a50f4c459097984d51637709b9c2390e5e59ed2fd2c859a7ef83617  EigenCompareComplexity.lean
9d0100fa0236296a13461208ba56a6ad85afe589cc5030744923e23f3199e0b9  EigenCompareExecutionCost.lean
82be7690500ecc18cf5ec107edea6819214f1a8742b6f6aa81bb5f5cc9e70560  PathInformationBits.lean
```
