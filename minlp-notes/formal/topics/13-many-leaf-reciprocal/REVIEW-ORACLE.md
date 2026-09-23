# Independent review of membership and the rational separation oracle

The reviewer compared `ManyMembership`, `ManyMembershipExamples`,
`ManyLinearSeparation`, `ManyOracle`, `ManyFastSeparation`,
`ManyFastCutSize`, `ManyOracleSize`, `ManyOracleBitCost`, and
`ManyOracleExamples` with the actual hull theorem and obligations MR33–MR37.
The review also checked the relevant interfaces in `ManyFastEvaluation`,
`ManyFastConstruction`, `ManyFastOperandSize`, `ManyBitCost`, and `ManyEuclidCost`.
Files are in [the proof directory](../../Formal/ReciprocalAnchor).

The executable definitions, semantic theorem statements, and full-oracle
arithmetic-charge model have the intended scope. The author reported that
`lake build Formal.ReciprocalAnchor.ManyOracle --wfail` passed after the final
charge declarations were added. The root integrator also reported passing
targeted warning-free builds of `ManyOracleSize` and `ManyOracleBitCost`,
and kernel-checked examples in `ManyOracleExamples`. The final size and
bit-work interfaces have now been reviewed. This review does not claim a
project-wide check, a CI result, or verification of Lean's compiled rational
backend.

## Exact membership

`rationalMembership` evaluates a total Boolean expression over rational
numbers. It checks the explicit mean bounds, all six inequalities for every
leaf, the computed lower moment, and the reciprocal upper secant.
`rationalMembership_correct` proves equivalence with membership in the actual
original-graph convex hull under `0 < a < b`. It uses
`fastLowerMoment_eq`, which proves that the executable sorted-stack evaluator
equals the real integral definition; it does not assume a supplied correct
envelope certificate.

The Boolean function is total outside the positive ordered endpoint domain,
but the correctness theorem deliberately makes no hull claim there.
The source's fixed-endpoint case has a separate linear hull theorem.

`ManyMembershipExamples` uses `decide +kernel` to check the complete Boolean
program on four cases: acceptance at the two-leaf minimum `31/50`, rejection
of the separate-hull candidate `3/5`, acceptance with no leaves, and rejection
of an invalid mean with no leaves. These examples use kernel reduction, not
native evaluation, and supplement the general correctness theorem.

`ManyOracleExamples` additionally evaluates the actual cut-producing program.
It checks acceptance at the exact minimum, a returned lower cut with violation
exactly `1/50`, a zero-leaf mean cut, an upper-secant cut, and a leaf-bound cut.
All use `decide +kernel` and exercise the output's rational affine evaluation.

## Actual affine cuts and complete dispatch

`RationalAffineCut` represents the inequality `eval <= 0`, with rational
coefficients for the constant, mean, reciprocal, leaf masses, and products.
`eval_cast` connects exact rational evaluation at the candidate to real
evaluation on arbitrary hull points.

The explicit cut list contains both mean bounds, the reciprocal upper secant,
and all six leaf inequalities. The reciprocal cut multiplies by `a*b`; its
equivalence proof establishes positivity of that product before changing the
inequality. `findLinearViolation` uses an executable list search. The proof
that no violation is found is equivalent to all these bounds, and a found
cut is strictly violated at the candidate and valid at every real hull point.
There is no nonempty-leaf assumption or unchecked index selection.

`separationOracle` first runs this affine scan. If no cut is found, it computes
the exact lower moment. It returns `none` when that bound passes and the
computed lower cut otherwise. `separationOracle_none_iff` connects acceptance
to the actual graph hull. `separationOracle_some_sound` proves strict
separation and validity at every real hull point for either rejection branch.
`separationOracle_complete` obtains an actual output from this total program
for every rejected rational point; it is not merely existence of some
unrelated separator.

## Extracting the lower cut

`fastCut` constructs its coefficients from the actual sorted-stack segments.
For each retained line, `lookupSource` performs a terminating search through
the finite input family. `sourceIndex` has a total fallback value, but
`sourceIndex_correct` proves that a retained line always has a matching input
index. `built_segment_source_eval` connects that recovered index to the
line used by the segment. Thus the fallback cannot introduce a spurious
supporting line for a produced segment.

`fastCut_exact` proves equality with the computed lower moment at the
construction point. `fastCut_valid` proves the same coefficient vector is a
lower bound on the integral expression at every other real candidate. This
proof keeps interval endpoints fixed and compares each selected source line
with the new candidate's envelope. It does not assume that selected lines
remain active after candidate coordinates change.

All segment endpoints are proved to lie in the positive common-factor
interval, with ordered bounds. The segment chain covers that interval and
the integral sum is proved equal to the full integral. Zero-length pieces
are harmless. The extracted cut is rational by construction and is placed
into the full oracle with reciprocal coefficient `-1`, matching the
`eval <= 0` convention.

## Complexity scope

The reviewed fast envelope has a counted sorting/stack operation bound of
order `N log N`. Cut extraction additionally searches for a source index for
each segment. `fastCutLookupCharge_le` bounds these actual search visits by
`(2*n+2)^2`. `fastCutArithmeticCharge_le` gives a conservative polynomial
arithmetic charge for source lookup and coefficient-vector materialization.
This additional work is polynomial; it is not advertised as preserving the
sharper envelope-only `O(n log n)` bound.

`fastCut_bits` bounds every actual reduced numerator and denominator of the
output coefficient vector by an explicit polynomial in the leaf count and
the common input bit bound. The interval formulas and finite sums have
separate bit-size lemmas. `ManyBitCost` supplies a stated schoolbook charge
model; `ManyEuclidCost` proves correctness and a bit-length iteration bound
for the explicit Euclidean remainder recursion. These are mathematical
arithmetic and bit-work bounds. They do not verify execution cost of Lean's
`Rat`, compiler, machine instructions, or the repository's Python script.

The final oracle charge covers its entire dispatch. `linearScanVisits`
follows the same terminating scan conditions as `findLinearViolation` and
has at most `6*n+3` visits. The dense cut-evaluation charge `4*n+7` per visit
covers two length-`n` dot products, the mean and reciprocal products, the
remaining additions, and comparison. Source coefficient construction is
charged separately. `lowerEvaluationCharge` adds segment integration and
input-line setup to the envelope charge.

On lower-bound rejection the program builds the envelope twice: once for
`fastLowerMoment` and once for `fastCut`. The final
`separationOracleArithmeticCharge` explicitly includes both stages, while
affine rejection and acceptance use their corresponding shorter branches.
`separationOracleArithmeticCharge_le` proves a polynomial bound for this
complete arithmetic model. The earlier concern about an omitted scan or
second construction is resolved.

`separationOracle_bits` bounds every coefficient of every actual returned
cut, handling both branches. The linear branch uses only endpoint values,
their sum/product, and constants; the lower branch uses `fastCut_bits` and
adds reciprocal coefficient `-1`. The representation bound does not need
feasibility or ordered endpoints. It also does not require a bit bound on
`t`, since the returned coefficients do not depend arithmetically on `t`.
The execution-width bounds do include `t` when evaluating inequalities.

The final width accounting covers intermediate values, not only final
outputs. `RationalAffineCut.evalTerms` is proved to sum to the actual dense
affine evaluation. `eval_partial_bits` bounds every sublist sum, so either
the two dot products or the outer partial sums are covered regardless of
grouping. `linearScan_eval_partial_bits` applies this to every tested linear
cut, not just the returned cut. The evaluator width lemmas cover source-line
setup, sorting coefficients, redundancy tests, intersections, segment
integration, tangent setup, and accumulated integral sums. The cut width
lemmas cover endpoint factors, tangent coefficients, and partially accumulated
coefficient vectors.

`oracleOperandBits` dominates these families, and
`separationOracle_charge_polynomial` bounds the actual dispatch's declared
arithmetic charge. `separationOracleBitWork_polynomial` combines that charge
with the declared schoolbook rational-step budget to give an explicit
polynomial expression. The budget inequality itself holds for any width
parameter; interpreting that parameter as a bound on this input's arithmetic
requires the separately stated `RationalBits` hypotheses proved through the
width lemmas. This distinction is visible in the declarations and should
remain explicit in the coverage record.

This closes the mathematical oracle accounting in the stated charge model.
There is no claimed refinement to a digit-level arithmetic program or to
Lean's compiled rational implementation.

No unresolved semantic defect was found in the reviewed membership,
separation, output-size, operand-width, or declared bit-work interfaces.
