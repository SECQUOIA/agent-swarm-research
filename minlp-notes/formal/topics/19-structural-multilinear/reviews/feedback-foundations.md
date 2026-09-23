# Independent review of feedback foundations

Reviewed 2026-09-20 against F01–F05 in [CLAIMS.md](../CLAIMS.md) and
`results/positive-multilinear-feedback-gap.md`. The reviewer did not author
or change the reviewed feedback proof modules.

**Result: no mathematical defect found in the compiled foundation modules.
F01 and F02 are discharged. The probability construction for F03 and the
original-box envelope construction for F05 are proved. Final graph-to-gap
assembly was still changing during this review and is distinguished below.**

## Foundation checks

| Module | Finding |
|---|---|
| `StructuralFeedbackUniversal` | An actual finite law with all prescribed means and simultaneous cell domination on `F` and every `F ∪ {i}`. The loss is exactly `(1/2)^F.card`. |
| `StructuralFeedbackRepair` | Explicit nonnegative residual extension and repaired probability law, preserving all prescribed feedback and pair marginals. |
| `StructuralFeedbackLocal` | Converts the repair back to the original coordinate type using a proved equivalence. Entrywise domination and all cell equalities survive the conversion. |
| `StructuralFeedbackForest` | Exact separator gluing, scope-observable preservation, and induction constructing a global law from a factor elimination order. |
| `StructuralFeedbackBoxes` | Nonnegative scope-local deficiency for each original box monomial, attainable local gap, simultaneous upper attainment, and the semantic conversion from a supplied global deficiency guarantee to a box gap bound. |

### Universal law and repair

The universal law integrates independent binary coordinates conditional on
one uniform parameter. Feedback success probabilities average the two
endpoint orientations; outside coordinates use the common lower threshold.
The expected cell indicator is proved equal to the integral of its
conditional product probability. The endpoint lower bound retains one half
per feedback coordinate, and arbitrary comparison-law cell masses are
bounded by every specified literal's marginal. Integrating an interval of
that cell mass proves domination without an extra scope-dependent factor.

The domination theorem does not explicitly require `x ∈ cube I`, but it
requires an actual law with means `x`, which already forces valid means.
The separate means theorem explicitly assumes cube membership. This is not
a missing hypothesis.

For zero residual total mass, `exists_residual` uses the zero measure and
proves every residual binary mass is zero from nonnegativity and its sum.
For positive mass it divides by that mass, constructs the Bernoulli product,
and multiplies back. An empty outside-coordinate type still has one binary
assignment, so its product law correctly carries the entire residual mass.
The repaired law has total mass one, retains the original cell masses scaled
by the loss, and has exactly the target pair and feedback marginals.

`exists_local_repair` actually repairs a law on all ambient coordinates.
This is stronger than repairing only `F ∪ e` and is valid: universal
domination is available on every ambient `(F,i)` pair. It simplifies the
later preservation of unused-coordinate means. The arbitrary-set split is
a genuine equivalence, and both mapping directions have proved weight and
cancellation identities. Coordinates already in `F` are handled by
`insert_eq_of_mem`; no outside-variable existence assumption is used.

These arguments include empty feedback sets, no outside variables, an empty
ambient coordinate type, means zero or one, and zero comparison-cell masses.
For `F=∅`, the loss is one and no artificial conditioning denominator appears.

### Separator and forest gluing

Conditional-product weights vanish on incompatible separator states. When
a separator mass is zero, every corresponding input atom has zero weight;
the marginal preservation proofs use that fact before division. For
nonzero mass, cancellation is justified. Both input marginals and total
mass one are proved, including unreachable separator states.

Scope gluing takes old coordinates from the left assignment and the rest
from the right. Agreement on the intersection guarantees preservation of
all observables on either scope. The special feedback-pair lemma also
preserves `F ∪ {i}` when `i` lies outside both factor scopes; it does not
silently lose unused-coordinate means.

`exists_global_feedback` is an induction over an explicit elimination
order. It carries the feedback block in every separator and proves all
factor marginals are preserved. Empty intersections, disconnected components,
empty scopes, and factors contained in `F` cause no exception. Crucially, it
does not multiply the domination loss along the forest: the repaired local
law is preserved exactly at every gluing step.

The elimination order is a combinatorial premise, not an assumed global
law. On its own this theorem is a conditional part of F03. The separate
`StructuralFeedbackOrder` module derives such an order from ordinary
incidence acyclicity by choosing a longest factor-ending path and removing
its terminal factor. Its source argument was reviewed and correctly allows
disconnected forests and isolated factors. Its changing build status is
recorded below.

### Original-box factors and envelope semantics

`feedbackBoxMajorant` expands an original factor only to construct a local
affine majorant. Every anchor of every expansion term lies in that term,
which lies in the original scope. `feedbackBoxDeficiency_congr` proves the
resulting payoff depends only on that original scope. The graph is never
replaced by a graph with expansion subterms as factors.

Nonnegative lower bounds and ordered endpoints make all expansion
coefficients nonnegative. This proves deficiency nonnegativity even on the
whole normalized cube, hence on all binary states used by the coupling.
Every feasible law has the same majorant expectation; the threshold law
attains that expectation for the original factor. Compact graph-hull
attainment supplies a law realizing the entire original-factor gap as
expected deficiency. The polynomial upper endpoint follows by simultaneous
attainment and nonnegative term weights.

Fixed coordinates are allowed: no proof assumes `l i < u i`. The imported
`boxEnvelopeValues_eq_of_mem` explicitly resets arbitrary normalized means
on fixed coordinates while preserving graph values. `exists_boxPoint`
covers every point of a degenerate physical box. Keeping fixed coordinates
in the structural graph preserves the given hypothesis; deleting them for
a sharper structural count would require a separate graph argument.

Empty scopes, constant and affine factors, zero coefficients and zero gaps
are covered by the formulas. The final bound divides only by the strictly
positive retained fraction, never by the hull gap. Factors are represented
by a finite set of supports with a coefficient function; repeated identical
monomials must be combined into that coefficient representation or handled
by a separately indexed wrapper.

## Assembly boundary at review time

The latest source of `StructuralFeedbackAssembly` was also inspected. Its
cell-equality-to-`AgreesOn` interface extends every restricted assignment to
an ambient one, so equality of all cells really implies equality of every
scope-local payoff.

The newly written `feedback_payoff_coupling_of_order` applies forest gluing
to the reduced scope `scope e \ F`, carries `F` in the separator, obtains
`HasMeans` from preserved feedback-plus-one marginals, and transfers each
original-scope payoff to `F ∪ (scope e \ F)`. Its retained fraction comes
solely from local repair. `feedback_box_gap_of_order` chooses actual
attaining factor laws and uses the proved original-scope deficiency locality.
No mathematical gap was found in these source-level connections.

These two assembly theorems were not included in the successful stable-module
build or axiom check below. At this checkpoint, claiming the unconditional
F04/F05 theorem still requires checking the final assembly build and the
following source-level interfaces:

- Derive the reduced-scope elimination order from the actual declared
  feedback-forest condition, using the graph order theorem.
- State precisely whether feedback deletion removes vertices or deletes
  their incident edges and leaves isolated vertices. The latter has the
  same acyclicity semantics, but this connection should be explicit.
- Instantiate the graph wrapper on exactly the original active factors.
  Derive forest equality using the existing reverse bound `H ≤ T` and the
  empty-feedback specialization.
- Verify the public physical-box theorem is stated at every point in the
  original box, and the unit-cube theorem follows with the documented gap
  definitions.

The conditional lemma `feedbackBox_gap_of_local_deficiencies` honestly
assumes the global law and local guarantee. It must not alone be used to
mark the structural theorem complete. The new assembly is designed to
construct, rather than assume, that missing law.

## Targeted checks

The following stable-module build passed from `formal/`:

```sh
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake build Formal.MultilinearGap.StructuralFeedbackBoxes Formal.MultilinearGap.StructuralFeedbackUniversal Formal.MultilinearGap.StructuralFeedbackRepair Formal.MultilinearGap.StructuralFeedbackLocal Formal.MultilinearGap.StructuralFeedbackForest
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-feedback-review.lean
```

The temporary review file printed axioms for the universal means and both
domination theorems, residual and target repair, arbitrary-set repair,
both separator marginal identities, global feedback gluing, gap attainment,
and the conditional box gap theorem. All listed only `propext`,
`Classical.choice`, and `Quot.sound`, with no `sorryAx`. Additional examples
checked positive residual mass with no outside coordinates and the
empty-feedback loss-one specialization.

An earlier seven-module build also included `StructuralFeedbackOrder` and
`StructuralFeedbackAssembly`. It failed during concurrent editing because
`StructuralFeedbackOrder` had a documentation comment before an `omit`
command (`unexpected token 'omit'; expected 'lemma'`). The author was
notified; the source was subsequently corrected. That transient failure
is not reported as a successful final assembly check. No project-wide
verification or CI inspection was run, and no proof file was edited by this
reviewer.

Stable foundation SHA-256 values:

```text
e0d73184bccc76e93f265c798b2eff5b638b1554fb1ae123397fc3d9d84fad33  StructuralFeedbackBoxes.lean
f4c99e31d892cbf3246ee52c212e5bc4015b49853cd6f97ba9969d60638c487b  StructuralFeedbackUniversal.lean
e34c81f6212a38f2f8c145a89ba23bb15eaac55a98b00c180fc3c9ffe36135bb  StructuralFeedbackRepair.lean
d0c6d1c8f83cf898ba1c2d254b72a879294b5b9df6a1bb23d8c5913fffad3ea7  StructuralFeedbackLocal.lean
f5592e1be7d396b78312c722178d1d249703f5e896a721485164eaf6dbee77a3  StructuralFeedbackForest.lean
```
