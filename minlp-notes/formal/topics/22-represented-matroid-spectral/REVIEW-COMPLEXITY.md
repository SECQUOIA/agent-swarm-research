# Complexity review

Status: component review and final independent integration review passed.
The original-input fixed-dimension bit-work obligation is closed in the
stated arithmetic and storage model. The package audit and kernel replay
remain separate verification evidence.

The original component reviewer authored the interpolation correctness and
execution modules. That review covers the determinant implementation,
interpolation size proofs authored by another agent, and the criterion
selection wrapper. [The interpolation review](REVIEW-INTERPOLATION.md)
provides the separate independent correctness review. The final integration
review below was performed by a different reviewer who authored no production
Lean module in this package.

## Findings checked

- `Elimination.lean` stores every Bird recurrence matrix before taking the
  next step. Its arithmetic counter grows polynomially with the matrix order.
  It does not unfold a recursively defined matrix function at every entry.
  The determinant sign and the zero-order determinant are handled explicitly.
- `EliminationExecution.lean` counts denominator multiplication, entry clearing,
  cached integer determinant evaluation, the denominator power, and final
  rational division. The matrix order is variable throughout these bounds.
- `EliminationBits.lean` proves linear growth of the exponent bounding integer
  magnitudes through Bird iterations and bounds partial sums in an entry.
  `DeterminantBits.lean` uses a factorial only in a mathematical estimate of
  the determinant value; its final encoding bound is polynomial, and the
  executed determinant does not enumerate permutations.
- `InterpolationBits.lean` exploits integral numerator coefficients. This is
  necessary: iterating the generic rational-addition size bound would give an
  exponential estimate in the interpolation degree. The proved numerator,
  denominator, tensor-product, and output bounds are polynomial in the grid
  size and input encoding bound.
- `InterpolationTraceBits.lean` bounds the actual operands of the materialized
  numerator tables, denominator products, weight divisions, tensor products,
  and final sum. Its schoolbook bit-work theorem explicitly excludes producing
  the grid values; the complete query implementation must add that work.
- `CriteriaExecution.lean` includes construction of both information matrices
  in each comparison. E-selection calls the existing complete least-eigenvalue
  execution trace, including characteristic-polynomial preprocessing, root
  separation, and both adaptive searches. Its constants depend on fixed
  information dimension, not fixed matroid rank. No floating-point comparison
  or uncharged eigenvalue oracle is substituted.
- `ExecutionRecovery.lean` retains each support query's Boolean and charge
  together. The outer scan includes the initial support test, every deletion
  test, and conservative column-set scan/copy charges. Its polynomial bound
  still requires the concrete per-query bound supplied by the complete query
  implementation.

No defect was found in these checked claims.

Execution scrutiny also led to a correction in the reviewer's own interpolation
trace: each numerator-table product is now explicitly cached before it is both
used and recorded. Sample nodes are constructed by a natural-number increment
and rational cast; their construction belongs to the structural preprocessing
charge. A separate reviewer must assess these interpolation changes.

## Completed determinant and query review

The determinant component is approved independently. `EliminationBitExecution`
connects every integer and rational operand to a polynomial width bound,
proves that the operand-list length matches the arithmetic counter, and bounds
the schoolbook charge at those actual widths. It includes denominator products,
exact clearing divisions, all cached Bird stages, final powering, and rational
reconstruction. The storage allowance permits full sequential matrix scans.
The zero-order determinant and singular inputs require no invertibility
assumption.

The cost observer is not a Lean runtime model. In particular, construction of
the observer's operand transcript is excluded from the underlying arithmetic
algorithm. The reconstructed transcript describes the same operations and
operands. The documentation must retain this distinction.

The concrete profile-query pipeline is also approved at the component level.
`ProfileGramExecution` materializes monomial weights and each Gram entry.
`ProfileOracleEvaluation` stores the zeroed representation while retaining all
original rows, passes a stored Gram matrix to the determinant runner, and
includes its proved bit-work bound. `ProfileOracleExecution` evaluates each grid
point once per query, keeps the value and charge together, interpolates, and
charges the final strict-positivity comparison. The node and determinant-output
width hypotheses are discharged from original representation and weight bounds.

Review found a structural-cost mismatch: a fourth-power Gram storage allowance
did not visibly cover full sequential input scans. The author raised that
allowance to a sixth power, preserving polynomial dependence and consistency
with the determinant storage model. This resolves the finding without assuming
unit-cost array access.

`RepresentationBitCost` bounds the actual greedy row-selection run, including
stored Gram matrices, determinant operands, zero tests, row-set handling, and
copies. All representation dimensions remain variable. No factorial-time
determinant or unproved rank oracle enters that preprocessing.

`ExecutionCover` connects the counted list producer to the actual
`spectralBasisSet`. It handles matroid rank zero directly, includes the
zero-information query for positive matroid rank, and visits all prescribed
factor subsets, including rejected trials. Query and deletion costs are
composed for every accepted profile. The remaining shifted-label cache
correction below concerns the structural cost of producing and comparing
profile keys, not the returned-family correctness.

## Final independent integration review

The reduced-representation caching correction is complete.
`cachedRowSubmatrix` materializes both the row-index map and reduced entries
before the continuation starts. The row-preprocessing storage allowance
includes these copies and permits sequential input scans. `candidateRun`
now materializes every shifted label through `shiftedWeightsCacheRun` before
profile production and deduplication. The addition, sign conversion, and
copy charge uses the proved normalization width for all labels, including
rejected atoms. It does not incorrectly apply the accepted-ground numerical
weight bound to rejected atoms. The stored cache is subsequently read by
both profile queries and profile-key comparisons.

`markedQuery` zeros weights outside the retained ground before owner marking.
Its cached marked weights therefore satisfy the uniform query bound.
The supplied representation keeps its original row count in every support
test and deletion. Recomputing a smaller rank is never part of this run.
`coefficientEvaluationRun` retains each determinant value and its charge
together; interpolation does not trigger a second determinant evaluation.
The explicit grid-construction and storage allowances supplement the
arithmetic traces, whose component statements deliberately omit that work.

`representedInputRun` executes row selection once, caches the reduced
representation, executes PSD factorization once, and passes both caches into
the actual cover loop. The proof fields of `cachedFactorData` do not execute
a second factorization. `representedInputRun_value` identifies the returned
list's underlying set with `representedSpectralCover` on the supplied original
matrices. The preprocessing continuation hypotheses are instantiated and
discharged in `representedInputRun_work`; no assumed support oracle,
normalization certificate, or continuation-cost hypothesis remains.

The composed charge includes all candidate factor subsets, even rejected
ones; all normalization, range, and diagonal tests; the zero-information
branch; marked coefficient queries; the initial support test and at most
`m` deletion tests per candidate profile; profile deduplication; collection;
and witness copies. Matroid rank zero still returns the empty base for a
nonzero prior. Positive matroid rank with zero information retains the full
original rank in its support query. Zero optional rank is handled as exact
equality, without a strict zero-remainder assertion.

`representedInputRun_polynomial_work` bounds this same executed charge by
`representedInputPolynomialBound` with tolerance parameter `ceil(1/eta)`.
Inspection of the complete definition chain confirms that this is a
polynomial envelope at fixed information dimension `p`:

- The computed row count is replaced by original row count `a`, and factor
  count by `p(m+1)`. Neither `a`, matroid rank, nor `m` is fixed.
- The normalization width is
  `4^p(inputBits+1) + etaBits + p + a + 3`, linear in the variable input
  widths and row count at fixed `p`.
- The shift is bounded by `4prq ceil(1/eta)`. Numeric rational denominators
  are not substituted for encoding lengths.
- Rank sums have `p` terms. Subset exponents depend on `r <= p`, and profile
  and interpolation exponents depend on `r(r+1)/2` and its owner-marker
  increment. The extra marker affects work but not output cardinality.
- Digit lengths are majorized by their arguments, and query maxima by sums.
  All remaining variable powers have fixed exponents. Factorial determinant
  routines occur only at fixed information dimensions in reused normalization
  or criterion calculations; variable-rank determinants use cached Bird.

The final continuation assembly and polynomial wrapper passed the targeted
command `lake build --wfail Formal.MatroidSpectral.InputExecution`, with
`PATH="$HOME/.elan/bin:$PATH"` and `LEAN_NUM_THREADS=1`. The implementation
authors reported stable sources; the final review snapshot is recorded in
[REVIEW-FINAL-SOURCES.json](REVIEW-FINAL-SOURCES.json). Earlier representation
and consequence review hashes were rechecked and still matched all 29
recorded entries after the interruption.

No unresolved semantic or cost-composition finding remains. This result is
an exact arithmetic and finite-storage cost theorem, not a measurement of
Lean evaluation time or a machine-instruction simulation. The observer's
transcript construction is not charged as part of the underlying arithmetic
algorithm. Constants and degrees may be large functions of `p`; practical
performance and fixed-parameter tractability in `p` are not claimed.
The final package audit, module kernel replay, and manuscript build are
recorded separately. No project-wide verification or CI inspection was
performed for this review.
