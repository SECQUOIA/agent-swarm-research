# Independent review: model, cuts, matching, and bound transfer

The review found no mathematical soundness defect in CM01–CM03, CM17,
CM19–CM20, or CM30–CM33. The new integration proves an actual graph embedding
from propagation and analytic cut evidence and applies the executable discrete
checker. It does not merely assume that original feasible points belong to the
master.

Reviewed primary sources:

- [ModelSemantics.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/ModelSemantics.lean)
- [CutCertificate.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/CutCertificate.lean)
- [EndToEnd.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/EndToEnd.lean)
- [MasterIdentity.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/MasterIdentity.lean)

Supporting sources checked for the named obligations:

- [Support.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/Support.lean)
- [Transfer.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/Transfer.lean)
- [ExactCorrections.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/ExactCorrections.lean)
- [Examples.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/Examples.lean)
- [Section 2](../../../paper-certified-minlp/sections/02-model.tex),
  [Section 3](../../../paper-certified-minlp/sections/03-soundness.tex), and
  [Section 4](../../../paper-certified-minlp/sections/04-implementation.tex).

The reviewer authored the separate quadratic modules, not these integration
modules. This review was read-only for Lean sources. No build was repeated,
no project-wide verification ran, and CI was not checked.

## Obligation checks

| Obligations | Evidence and assessment |
|---|---|
| CM01 | `normalized_upper_row` and `normalized_lower_row` give exact feasibility equivalences. `signed_min_bound`, `signed_max_bound`, and `checked_nonlinear_max_bound` handle objective signs. They do not infer convexity of a normalized lower row from convexity of the unnormalized expression. |
| CM02 | `extendedPoint` explicitly appends the epigraph value and then one. The projection recovers every original coordinate. `extendedBox` leaves the epigraph coordinate free and fixes the constant coordinate to one. `epigraph_graph_row` is zero at the graph, `epigraphObjective_value` returns the epigraph value, and `affineObjective_value` includes the affine constant exactly once. The affine-objective wrapper uses these identities. |
| CM03 | `extendedOptimum` is an `EReal` indexed infimum. `extendedOptimum_lower` follows directly from every feasible point's bound, and `extendedOptimum_empty` returns positive infinity. No attainment or nonempty-domain premise is introduced for that result. |
| CM17 | `lower_directed_slope` and `upper_directed_slope` prove the required residual signs from rigorous slope enclosures. `free_matched_slope` proves the free-coordinate case. `Examples.epigraph_free_residual` specializes to nonlinear derivative zero and matching affine/cut coefficients minus one, with zero correction. |
| CM19 | `support_of_segment_right_derivative` applies convexity to the actual segment and compares the right derivative to its secant. `support_of_hasFDerivAt` supplies that derivative from an ambient derivative. `support_of_feasible_segment_derivatives` matches the paper's coordinate formula. `CutData.underestimator` uses this support theorem, rather than assuming the support inequality as a new unexplained premise. |
| CM20 | `neg_sqrt_no_finite_support` constructs a failing positive point for every real candidate slope. The product example proves both axis derivatives are zero and separately refutes the resulting zero support at `(1,1)`. These are mathematical boundary counterexamples and do not claim to certify a symbolic differentiation library. |
| CM30 | `checkMaster` checks strictly positive scales, source and target row permutations with multiplicity, integer flags, objective coefficients, and the objective constant under a typed variable equivalence. `matches_feasible` proves both directions, `matches_objective` proves exact value equality, and `matches_attainable_values` states the complete semantic correspondence. Zero or negative scale witnesses cannot pass. Coordinate bounds and fixed-one equalities use the same row semantics. |
| CM31 | `graph_master_feasible` constructs the actual graph point. `justifiedRow_holds` derives its propagated-box membership from the transcript; source affine rows from original feasibility; inferred bounds from `Propagation.admitted_sound`; fixed-one equality by construction; and cuts from `CutData.row_valid`. Every cut names either a source constraint or the epigraph row and supplies exact equality of its decomposed expression with that target on the checked box. The target is nonpositive at every feasible graph point. `extendedPoint_integral` preserves every declared integer coordinate and also proves binary coordinates integral. |
| CM32 | `checked_nonlinear_bound` and `checked_affine_bound` apply `Discrete.checked_bound` to that proved graph membership and the explicit objective identity. `checked_matched_objective_bound` composes the actual matching test, the graph embedding, and the actual discrete proof for the matched target master. `checked_matched_nonlinear_bound` supplies its epigraph objective identity. `checked_nonlinear_max_bound` applies sign normalization, and `checked_nonlinear_infeasible` applies the no-cutoff checked contradiction. |
| CM33 | `primal_infimum_bounds` constructs nonemptiness from the actual nonlinear witness and boundedness below from the certified bound before using the real infimum. It proves the bound chain and witness gap. `primal_enclosure_gap` also proves the enclosure-minus-infimum gap. `matching_primal_attains` proves objective equality and global optimality when the witness enclosure matches the lower bound. A master witness is not substituted for the required nonlinear witness. |

## The composed acceptance assumptions

The new end result has concrete evidence rather than a final inclusion premise:

1. A propagation transcript is checked against intermediate boxes and supplies
   the box containing each original mixed-integer feasible point.
2. Every included master row has an explicit `JustifiedRow` constructor: an
   original affine row, an admitted bound, the fixed-one equality, an accepted
   cut of an identified source expression, or checked weakening of such a row.
3. `CutData.Accepted` requires actual convexity, a support point in the box,
   segment derivatives, residual enclosures, a value enclosure, and the rational
   intercept comparison. Its conclusion is derived underestimation, not stored
   cut validity. These analytic and enclosure hypotheses are the intended
   mathematical inputs; verifying their production by Python remains separate.
4. `checkBound = true` validates actual rational solution data and every typed
   derivation before furnishing the master bound. The separate discrete review
   checks this layer.
5. For a differently indexed proof master, `checkMaster = true` supplies the
   algebraic matching and the target discrete checker is applied to that target.
   The source has external objective constant zero because any affine constant
   is represented by its fixed-one coordinate. Matching forces the target's
   external objective constant to zero as well, preventing double counting.

The general matched-objective theorem has an explicit objective identity premise.
That premise concerns the encoding's scalar value and is not a feasible-set
inclusion assumption. The nonlinear specialization proves it directly. The
`affineObjective_value` theorem supplies the corresponding affine identity.

## Representation limits that should remain explicit

The master supplied to `graph_master_feasible` may omit some otherwise valid
original rows or bounds. This is sound: omitting a restriction makes a weaker
relaxation, and every included row is still justified. The theorem does not
verify that the Python LP exporter emits every prescribed row. Source/target
matching separately requires exact equality of the supplied row multisets up
to its permitted transformations. The coverage record should not conflate
these two claims.

The graph encoding always has both an epigraph and a fixed-one coordinate.
For an affine objective the epigraph coefficient is zero; that unused real
coordinate does not change the proved objective. This is a uniform mathematical
encoding, not a claim that the Python exporter allocates the same coordinates
in every model.

`MasterIdentity` receives a Lean equivalence, whose type guarantees a true
bijection, and a rational row-scaling witness that its Boolean checker validates.
It does not verify the parser's string-name matching, optional prefix handling,
or construction of canonical row scales. Source and target objectives use the
same normalized minimization convention; the mathematical sign-normalization
theorems cover maximization. A textual objective-sense token is a parser
obligation, not a field checked by `checkMaster`.

No result here establishes that model loading, symbolic differentiation,
interval evaluation, byte serialization, or the Python implementations produce
these exact Lean inputs and evidence. Those remain the software boundaries
CS01–CS05. Infeasibility transfer is a mathematical implication and does not
expand the finite-bound public API.
