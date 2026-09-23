# Independent semantic review of the SDP characterization and consequences

Reviewer: the topic 27 model agent, independently of these topic 28 modules'
implementation. Date: 2026-09-22.

Reviewed `SDPCharacterization.lean` and `Consequences.lean` against frozen
claims C05–C08 and source Corollaries 3–4 and Lemma 4. Also inspected the
aggregate definitions, the upper-triangular coordinate equivalence, the
Shor projection and block-formulation bridge, and the imported whole-space
implications. No mathematical or statement-fidelity defect was found.

## Normalization, compactness, and infeasibility

`normalizedPSD` is exactly the common feasible set of nonnegative weights
whose sum is one and whose aggregate `n×n` matrix is PSD. It uses the
original `m` weight variables; there are no extra feasibility or
closed-image assumptions. `Certificate.exists_normalized` proves the sum
of a nonnegative nonzero vector is strictly positive before dividing by
it. Positive rescaling preserves PSD and preserves a nonzero quadratic
or linear coefficient.

`isCompact_normalizedPSD` identifies this set with the standard simplex
intersected with a closed PSD preimage. Closedness is proved from all
quadratic inequalities and the already proved symmetry of every
aggregate. It does not assume a linear image of the PSD cone is closed.
`signed_objective_attains` applies compactness only after receiving an
explicit nonemptiness hypothesis. Its conclusion is an `IsGreatest`
statement, which includes membership of the maximum in the objective
image and therefore establishes attainment.

`SDPTestsZero` handles an empty normalized set separately. In the other
case, both objective signs must have attained maximum zero. All these
programs have the same feasible set, so this single infeasibility branch
is equivalent to the source's per-program qualification. The proof does
not assign zero to the supremum of an empty objective image. Its reverse
direction obtains a feasible weight before using zero as an attained
maximum. The statements also handle `m=0` and `n=0` without unstated
positivity assumptions; when there are no coefficient coordinates, both
aggregate coefficient blocks are necessarily zero.

## Coordinates, signs, and exact count

`CoefficientIndex n` consists of upper-triangular entries, including the
diagonal, and the linear-vector entries. `coefficients_zero_iff` uses
aggregate symmetry to recover the omitted lower-triangular entries. Thus
zero objectives mean the entire pair `(A_lambda,b_lambda)` vanishes,
not merely selected entries. `coefficientObjective_eq_sum` proves each
objective is linear in the original weights.

`sdpTestsZero_iff_no_certificate` uses the positive and negative maxima
together to force each feasible objective value to be zero. Conversely,
vanishing coefficients give zero attained maxima whenever the common set
is nonempty. The normalization theorem supplies the essential bridge
from arbitrary nonnegative weights to this compact slice.

The imported `upperCoordEquiv` indexes exactly the upper triangle, and
`card_upperCoord` proves its cardinality is `n(n+1)/2`. Adding the `n`
vector entries gives `n(n+1)/2+n` independent coordinates.
`signed_objective_count` proves the exact signed-program count
`n(n+1)+2n`, including the necessary parity of `n(n+1)`. Each program
retains `m` nonnegative variables, the sum-one equality, and one `n×n`
PSD block. No redundant full-matrix count is substituted for the source
count.

## Headline statements and scope

`full_hull_iff_sdpTestsZero` connects the exact tests to the ordinary
strict convex hull under strict feasibility and AHC. This strengthens the
source's HHC hypothesis through the existing HHC-to-AHC implication.
`no_certificate_iff_trivial` also explicitly covers zero multipliers,
which are excluded from the certificate definition but belong to the
source's coefficient cone.

`Consequences.lean` composes the intended statements without introducing
new assumptions. Its Shor/no-certificate, Shor/trivial-coefficient, and
Shor/SDP-test equivalences require strict feasibility but no HHC or AHC.
The Shor/strict-hull and Shor/closed-hull equivalences require AHC and
strict feasibility, with an explicit HHC specialization. The projection
in these statements is the actual Shor projection: the imported
`mem_shorProjection_iff` proves equivalence between its PSD-covariance
implementation and the standard lifted block PSD constraints.

The SDP conclusions are propositions about exact feasibility and exact
attained optima. They do not implement a solver, prove effective exact
SDP decidability over arbitrary real input, provide bit complexity, or
justify classifying small floating-point optima as zero. The reviewed
module comments preserve this boundary.

## Verification boundary

This was a read-only semantic review of implementation files. No Lean
build, kernel replay, project-wide verification, or CI inspection was run
for this review. The coordinator's targeted machine checks remain
separate evidence. Only this review record was written.
