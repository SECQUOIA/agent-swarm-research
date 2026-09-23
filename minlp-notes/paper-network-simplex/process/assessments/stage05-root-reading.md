# Stage 5 — root independent source reading

Read the three standalone result files in full and the smaller construction and
failed-composition discussion in the development note. Manuscript review will
follow when the author freezes the stage.

## Checked implications

- Transportation sections fix aggregate margins and two state boundary margins;
  the residual state obtains the third by subtraction. Acyclic nonnegative
  state flows of value D have every arc at most D, so scaled capacities add no
  unintended restriction. All designated table cells must be in layer one.
- Reopened the primary De Loera–Onn paper. Its coordinate-erasing injection is
  essential. The paper already includes universal bitransportation and a
  two-commodity network interpretation; attribution must distinguish that
  antecedent from transfer into sparse original bilinear coordinates.
- Padding one row/column with cross U=0 and corner layer entries one is a unique
  independent table block. It ensures positive weights without changing the
  represented polytope. Scaling all flow/product coordinates by the same B
  preserves coefficient ratios; the section changes to p+Mq<=1/B.
- For the balanced-incidence construction, alpha^T C = beta 1^T cancels the
  shared profile perturbation. C^{-1}(-delta+tau) preserves its total because
  alpha^T(-delta+tau)=0. Nonempty/proper rows provide both interior slack and an
  allowed state from which to subtract tau. This proves a full local half-plane,
  sufficient for the accepted ambient-facet lemma.
- Fibonacci D has 2q-1 rows/columns and 5q-4 incidences. Its homogeneous column
  equations force the Fibonacci recurrence and then zero through the final
  pair. The positive balanced row vector proves complement invertibility by
  the rank-one identity. Sparse encoding has O(q log q) bits; F_q is
  superpolynomial in that length in magnitude, not in bit length.
- Splitting internal joins adds N-1 vertices/arcs; subdividing each b arc adds
  N vertices/arcs. Starting with N+1 vertices and 2N+1 arcs gives 3N and 4N.
  New flows are uniquely determined and bounded by unit total acyclic flow.
- The flat-chain profile inequalities follow from summing independent intervals
  after fixing a-only, b-only, and both-observed states. Row signs can be removed
  before taking minors; positive circuits have support at most d+1 and primitive
  entries at most Delta_d. Duplicate-row minima must be frozen to actual affine
  branches to output globally valid cuts. Zero rows require separate scalar tests.
- A bounded feasible profile polytope has a vertex even on zero-weight strata;
  active rows span ambient dimension, allowing a finite-basis exact recovery.

## Useful strengthened explanation proposed to the author

The failed scalar-composition claim has a concrete local witness: choose
u=c-epsilon, v=c. The joint weighted inequality fails, but each gadget separately
can choose a profile with total 1/2. The affected gadget moves epsilon of profile
mass from a complement state to an allowed state; others keep the nominal
profile. Small epsilon preserves all fixed-cell bounds. Author must independently
verify before inclusion.

## Sources reopened

- https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf
- https://link.springer.com/article/10.1007/s10107-026-02392-8
- Primary Alon–Vu source found at https://web.math.princeton.edu/~nalon/PDFS/av1.pdf

Targeted searches for sparse network/simplex, series-parallel and Fibonacci
coefficient results returned the already identified direct predecessors, not a
matching restricted coefficient theorem. This limited search establishes no
priority claim.

## Small additional algebraic check

The displayed Fibonacci weights sum to sigma=(q-1)gamma+1, so the complement
balance constant is beta=(q-2)gamma+1. This follows by cancelling primary weights
against their appearances in auxiliary weights. An independent SymPy construction
for q=3,...,8 also gives |det D|=gamma and |det C|=beta (respectively
3/4, 5/11, 8/25, 13/53, 21/106, 34/205). The determinant identities are not needed
for the paper and are recorded only as a finite observation unless separately
proved. The complement identity follows from the matrix determinant lemma if
the first identity is established. No manuscript claim depends on this check.

## Initial manuscript reading

Read the complete initial `05-universality.tex` and `06-series-parallel.tex`
while the author continued the profile section. The explicit polynomial
transportation transfer, local incidence proof with a rational neighborhood,
small M family counts, Fibonacci sparse counts, and degree-three transformation
are correct as written. The new scalar-composition witness is now constructive.
The displayed neighborhood bound follows from
||K^{-1}(-delta+tau)||_inf <= ||K^{-1}||_inf max(1,R) epsilon < a/16;
tau_s<(1+R)epsilon<a/16. No correction was identified in these two files.
The reduced-profile discovery is recorded separately and still needs review.

## Reduced-profile manuscript reading

Read all of the initial fixed-state-chain section. The profile equivalence,
residual elimination, improved (m+1)Delta_m bound, finite-basis recovery, and
new five-test/unit-coefficient proof are sound. Sent the author three pre-freeze
local repairs: state the positive full-row x_h coefficient as 0 or -1 from the
outset, distinguish negative contributions from positive singleton rows, and
correct 'determinators'. Also requested explicit normal indexing to justify the
O(mL+|O|+m) assembly count without a tuple-copy factor per singleton row.

For the new unit proof, no positive circuit contains both -e_j and +e_other,
or both +e_j and +full. Thus no product contributes twice with the same sign.
Only x_h can have two same-sign contributions, in (+e1,+e2,-full), and its
mandatory +1 from the negative full row offsets them. The direct two-interval
recovery formula verifies every endpoint and the prescribed sum, including
zero-width intervals. This strengthens the source result without assuming
positive residual or explicit state weights.

## Three-state threshold reading

Read the complete new three-state theorem and its 7+5+3+1 circuit classification.
The minimal-support proof covers all possibilities: without -full a single
positive subset must be cancelled by its singleton coordinates; with -full,
+full gives an opposite pair, one other negative singleton forces the two
overlapping pairs, and no other negative singleton gives partitions or the
three-pair half cover. The product occurrence restrictions and two exceptional
bypass repairs are correct. Distinct selected positive normals in either extreme
case force distinct gadgets, so the chosen x_a has exactly the needed coefficient
and its x_b was absent. The m=4 actual-product section makes the threshold sharp.

The author independently reproduced all circuit counts and 539 branch repairs,
and independently checked the root's two isolating queries against an arc-state
LP. These are distinct from the forthcoming five referee reports. The stage is
not accepted until that review process concludes.

## Final pre-freeze boundary check

The observed-label corollary originally wrote O(aL+|O|+m), as in the root's
suggestion. For a=0 it omits the required O(L) flow-domain scan and default-flow
output. Sent the author the local correction O((a+1)L+|O|+m); no mathematical
mechanism changes. This correction must be in the frozen review version.
