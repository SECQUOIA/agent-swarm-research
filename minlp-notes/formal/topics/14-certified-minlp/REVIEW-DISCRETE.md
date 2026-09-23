# Independent review: propagation and discrete inference

The review found no mathematical soundness defect in the declarations covering
CM05–CM08 and CM21–CM29. The proofs establish the stated rules from exact
arithmetic and actual checked dependencies. The final bound theorem does not
assume the desired inference invariant or an unchecked feasible incumbent.

Reviewed sources:

- [Propagation.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/Propagation.lean)
- [DiscreteRows.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/DiscreteRows.lean)
- [Discrete.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/Discrete.lean)
- [DiscreteSolutions.lean](../../../paper-certified-minlp/formal/CertifiedMinlp/DiscreteSolutions.lean)
- [Section 3](../../../paper-certified-minlp/sections/03-soundness.tex), especially propagation,
  the inference invariant, and the unconditional master bound.
- [Section 4](../../../paper-certified-minlp/sections/04-implementation.tex), for the
  distinction between arithmetic inference and parser/executable correctness.

The reviewer implemented the separate quadratic modules and did not author the
modules reviewed here. This was a read-only semantic review of those modules;
no build was repeated, no project-wide verification ran, and CI was not checked.

## Obligation checks

| Obligations | Evidence and assessment |
|---|---|
| CM05 | `termLower` selects the correct signed endpoint and returns `none` when the necessary endpoint is absent. A zero coefficient returns zero even for an unbounded coordinate. `termUpper` uses negation. Their soundness theorems concern real values. `ResidualLower` and `ResidualUpper` require successful endpoint checks for every coordinate except the selected one; their finite sums are proved bounds. |
| CM06 | `rowInstruction_sound` proves all four upper/lower row and positive/negative coefficient cases. Its coefficient-nonzero premise is explicit, and it uses the appropriate proved residual bound before division. |
| CM07 | `roundInstruction_sound` requires the actual selected coordinate to equal an integer. The admitted rounding constructor additionally requires membership in the declared integer set. Binary and fixed constructors use their declared feasible-point conditions. `fixed_substitution` proves exact row-value preservation. |
| CM08 | `contains_tightenLower` and `contains_tightenUpper` identify updates with intersections. `admitted_sound` discharges each admitted update from primitive checks. `transcript_preserves` checks the induction against the current intermediate box, and `propagation_preserves_feasible` starts at the declared box. `empty_interval_infeasible` handles contradictory endpoints. `constant_row_iff` identifies exact tautologies and contradictions. No sweep count or convergence premise occurs. |
| CM21 | `dominates_sound` covers both inequality directions, equality-to-inequality, equality-to-equality, and exact constant contradictions. Matching coefficients and right-hand-side directions are checked rationally. |
| CM22 | `allowed` checks multiplier signs for the chosen resulting direction; equality terms are unrestricted and an equality combination permits inequality terms only with zero multipliers. `combination_sound` proves the actual summed row and its relation. Zero terms require no source-row semantic truth. |
| CM23 | `integralCoefficients` checks every nonzero coefficient is integral and belongs to a declared integer coordinate. `value_integral` constructs the integer sum. `rounded` refuses equality rows; `rounded_sound` proves both floor and ceiling directions. |
| CM24 | `splitRows_sound` proves the disjunction from an integral linear form and consecutive integer thresholds. `StepCheck.unsplit` checks actual earlier entries marked as assumptions, their claim identities, either branch ordering, both domination tests, and exactly the union after the two separate singleton deletions. The soundness proof restores only the discharged assumption in the relevant branch. Cross-branch and unrelated assumptions remain. |
| CM25 | Original rows are retrieved from the master, assumptions receive their own current index, and solution rows require an actual optional cutoff. The final solution layer builds that cutoff only from a member of a checked solution list. |
| CM26 | `step_sound` proves each rule from its executable arithmetic tests. `checkFrom_sound` inducts over the supplied list from a valid prefix. `check_sound` starts from the empty prefix; its claim lookup is computed from the certificate rather than supplied as an oracle. |
| CM27 | `checkFrom` checks every supplied step through conjunction and recursion. It does not stop at a proving row. References are looked up only in the checked prefix; `fetch` also looks up zero-multiplier references. The final checker therefore rejects an invalid suffix even when an earlier row proves the bound. Its typed-input boundary is described below. |
| CM28 | `checkSolution_sound` checks every original row and every declared integer coordinate. `bestSolution_spec` proves the selected member is in the supplied finite list and minimizes its objective, with `none` exactly for an empty list. `checked_bound` uses the selected checked member and `incumbent_cutoff_lifting` to remove the weak cutoff. `checked_max_bound` applies the same construction to the negated objective; specializing `bestSolution_spec` to that objective selects the greatest original objective value. No master optimum or attainment premise is used. |
| CM29 | `checked_assumption_free` removes empty dependencies and applies row domination. `checkBound` requires such a row anywhere in a wholly checked list. `checkInfeasible` explicitly uses no solution cutoff, and `checked_infeasible` proves the master feasible set is empty from an assumption-free contradiction. |

## Premises and representation boundary

`step_sound` and `check_sound` are reusable lemmas with premises saying the
master rows, declared integrality, and optional cutoff hold on a set `S`.
These are legitimate interfaces, and the end results discharge them:
`checked_bound` uses the actual master feasible set or its incumbent-restricted
subset, and proves the cutoff from the selected checked solution. The
infeasibility theorem uses the actual master and `none` for the cutoff. There
is no remaining assumption that the supplied derivations are semantically valid.

The discrete checker takes structured Lean values. Coordinate coefficients and
solutions are total functions on `Fin n`, so coordinate indices are in range and
one value exists per coordinate. Row relations are an inductive type, arithmetic
is rational, and proof references are natural indices checked by finite list
lookup. Declared integer membership is a Boolean function. This representation
covers arbitrary finite dimension, including zero.

This does not verify ASCII parsing, sparse-entry uniqueness, omitted-coordinate
reconstruction, declared textual counts, lifetimes, a terminal `global` marker,
or end-of-file consumption. In particular, lists of combination references need
not be unique in the Lean representation; repeated references have well-defined
summed arithmetic. The Python parser's stricter duplicate-entry policy remains
CS04. Checking the complete supplied Lean list establishes the mathematical
invalid-suffix protection once parsing has faithfully supplied that list.

Propagation has explicit computable endpoint and update operations, together
with an inductive `Admitted`/`Transcript` proof representation. Its preservation
theorem verifies every represented finite sequence; it is not a verification of
the Python sweep scheduler or a separate serialized propagation parser. These
implementation connections remain CS03. The mathematical CM05–CM08 assertions
do not require those software connections.
