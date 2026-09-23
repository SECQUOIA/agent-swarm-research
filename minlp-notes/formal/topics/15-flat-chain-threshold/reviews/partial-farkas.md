# Independent review: Farkas and partial circuit libraries

No soundness defect or missing assumption was found in the three reviewed modules:
[ThresholdFarkas.lean](../../../Formal/NetworkSimplex/ThresholdFarkas.lean),
[ThresholdPartial.lean](../../../Formal/NetworkSimplex/ThresholdPartial.lean), and
[ThresholdThreeCompleteness.lean](../../../Formal/NetworkSimplex/ThresholdThreeCompleteness.lean).
The review inspected the proof bodies and the existing `Circuits` and `ThreeState`
completeness proofs, then ran the targeted checks below. No proof source was changed.

## Findings

- `farkas_inequalities` proves the inequality alternative for arbitrary finite real
  row systems. Its sufficiency proof inducts on the number of variables, retains
  zero-coefficient rows, and combines each positive/negative pair with nonnegative
  multipliers. Certificate lifting preserves both cancellation and the right-hand
  side. No boundedness, interior-point, rank, or feasibility premise is hidden.
- Zero-dimensional systems are checked by singleton certificates, so contradictory
  scalar inequalities are rejected. `finite_interval_point` explicitly handles
  either or both bound families being empty. Empty row systems remain feasible in
  every dimension.
- `complete_partial_library` explicitly requires a complete full library and
  weights that are either zero or at least one. These premises are appropriate
  for the primitive integer library; they are not asserted for arbitrary positive
  real weights. The finite sum `S` bounds all potentially negative existing terms.
  Filling an absent participating group with `S + 1` therefore makes its full
  test nonnegative.
- The fill value is internal to the existence proof. The conclusion contains only
  constraints whose original `Option` right-hand side is `some`. The test predicate
  checks only circuits supported on present groups; no artificial row or bound
  appears in either public conclusion. This remains valid when all groups are absent.
- `three_full_complete` obtains completeness for every real right-hand side from
  `circuit_tests_iff_feasible`. Inspection of that dependency reaches the explicit
  five-test construction in `ThreeState.tests_imply_feasible`; it does not depend
  on the new partial-library or Farkas results. `boundsOfRhs` has a proved exact
  right inverse, including the four lower-bound sign changes. The partial theorem
  discharges positivity and cancellation from the actual sixteen integer circuits.
  There is no circular completeness assumption in the final theorem.

These modules prove feasibility and certificate equivalences. They do not by
themselves establish the executed recovery algorithm, its operation count, or
its bit complexity; those require the separate topic results.

## Targeted checks actually run

From `formal/`:

```sh
lake build Formal.NetworkSimplex.ThresholdFarkas Formal.NetworkSimplex.ThresholdPartial Formal.NetworkSimplex.ThresholdThreeCompleteness --wfail
lake env lean -DwarningAsError=true /tmp/threshold-partial-farkas-review.lean
```

Both final commands passed. The temporary review file checked empty row systems,
a contradictory zero-dimensional scalar row, the all-absent circuit predicate,
and feasibility with all eleven groups absent. It also printed the transitive
axioms of `farkas_inequalities`, `complete_partial_library`, and
`three_partial_feasible_iff`: each used only `propext`, `Classical.choice`, and
`Quot.sound`. The initial probe invocation used an unsupported Lean CLI flag;
the recorded successful invocation uses `warningAsError` instead.

No project-wide verification was run, and CI status or logs were not inspected.

Reviewed SHA-256 values, in the file order given above:

```text
1a0ca318bf996871789770e230d1eb5ece16526d74194e0574fe6e9bbd3d4695
f4add29a1e432f2a4bdd6dc6123642553450faf36138b0e0b6f13c47d3045628
3c2b3dd610c7cfd09a376196f903a9bcfcad97aa46cf420078ae8d312bd59c8b
```
