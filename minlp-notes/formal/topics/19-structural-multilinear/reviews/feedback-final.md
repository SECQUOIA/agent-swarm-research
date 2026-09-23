# Independent final feedback and cardinality-envelope review

Reviewed 2026-09-20 against F01–F05 and C01–C02 in
[CLAIMS.md](../CLAIMS.md), following the earlier
[feedback-foundations review](feedback-foundations.md). The reviewer did not
author or edit the proof modules.

**Result: no mathematical or statement defect found. The final feedback
assembly closes the graph-to-gap obligations left open in the foundation
review. F01–F05 and C01–C02 are proved for their declared representation and
hypotheses. This review does not discharge sharpness, frequency-two, or
treewidth-two obligations.**

## Actual structural hypothesis and theorem chain

`feedbackIncidence F S` is the ordinary bipartite incidence graph with an
edge between variable `i` and original factor `s` exactly when `s ∈ S` and
`i ∈ s \ F`. The vertex type retains feedback variables and inactive
factor labels as isolated vertices. Removing those isolated vertices would
not change whether a cycle exists. The theorem does not use a graph of
expanded box monomials.

`ForestGluing.exists_leaf_factor` uses a longest factor-ending path in a
connected component of the active graph. A terminal factor cannot share two
different variables with the remaining active factors: an incidence at any
variable other than the penultimate path vertex would extend that path by
two edges, or contradict acyclicity. The choice of root requires only one
active factor, so disconnected components and isolated factors are allowed.
`exists_eliminationOrder_active` repeats this argument after removing a
factor. Its graph restriction is proved to delete edges, and ordinary
`SimpleGraph.IsAcyclic` is preserved under that restriction.

The probability and assembly steps have no hidden global-law premise:

1. `feedbackUniversalLaw` is an actual finite probability law. Its
   singleton means are `x`; its cells on `F` and on every `insert i F`
   dominate the corresponding cells of every feasible law by
   `(1/2)^F.card`.
2. `exists_local_repair` constructs a law for every original comparison
   law. It retains that fraction of every atom and makes all feedback and
   feedback-plus-one marginals equal to those of the same universal law.
3. `exists_global_feedback` glues these repaired laws along the proved
   elimination order for `s \ F`. The separator is `F` together with at
   most one remaining variable. Equality of all cell probabilities implies
   equality of every separator-local observable through
   `agreesOn_of_feedbackCellMass_eq`; it is not merely a singleton-moment
   substitute for a joint marginal.
4. `feedback_payoff_coupling_of_order` preserves all singleton means,
   including coordinates outside the factor scopes, and proves the
   simultaneous guarantee for every nonnegative original-scope payoff.
   Exact preservation of each repaired factor marginal prevents repeated
   multiplication of the retention factor during gluing.
5. `feedbackBoxDeficiency_attains_gap` supplies an actual maximizing local
   deficiency law. The deficiency is nonnegative and depends only on its
   original factor scope. Its affine-majorant expectation is fixed by the
   means and equals that factor's attainable upper endpoint.
6. `feedback_variable_gap_bound` combines these facts to prove
   `boxTermwiseGap ≤ 2^F.card * boxHullGap` at every `z ∈ coordinateBox l u`
   with `0 ≤ l ≤ u`. Its only structural premise is residual incidence
   acyclicity. The earlier conditional helper's assumed law has therefore
   been constructed and its premises discharged.

`incidence_forest_gap_exact` specializes to empty `F` and combines the
resulting upper bound with the independently proved `H ≤ T`. No strict
positivity of `H` is assumed or needed. A temporary Lean example also
checked the exact unit-cube specialization using the existing
`weightedTermwiseGap` and `hullGap` definitions. There is no separate named
unit-cube wrapper in the reviewed module; the specialization requires only
the proved box-to-cube identity and simplification.

## Boundary cases and representation

The reviewed statements allow empty ambient types, empty factor families,
empty scopes, disconnected forests, unused variables, `F = ∅`, and `F`
containing every variable. They impose no nonempty-complement premise.
Zero residual mass is handled before division; separator states of mass
zero contribute zero, with both marginals still preserved. Endpoint means
and tied minimum means introduce no strict inequalities.

The box theorem assumes `l i ≤ u i`, not strict width. The box-envelope
identity explicitly repairs arbitrary normalized means of fixed
coordinates without changing physical graph values, and `exists_boxPoint`
covers every physical box point. The structural graph keeps the original
scopes even for fixed coordinates. The theorem does not claim a smaller
feedback count after deleting fixed coordinates without a corresponding
graph argument. A temporary Lean example successfully applies the public
statement to a fully fixed zero box.

Nonnegative coefficients may be zero. Constant and affine factors and
zero gaps need no special exclusions. Division occurs only by the positive
retention fraction. Ratios would additionally require a positive hull gap;
the reviewed public theorem states an inequality, not such a ratio.

The polynomial representation is a finite set of scopes with one
coefficient per scope. Repeated identical original monomials are represented
by adding their nonnegative coefficients. Documentation should continue to
state this convention rather than suggesting this theorem directly accepts
an arbitrary indexed multiset of factor copies.

## C01 and C02

`StructuralInterpolation.cardinalityFactor` is the tensor-product
multiaffine interpolant of the binary count table. Its vertex values and
separate affinity are proved, and `cardinalityFactor_minimum` applies the
lower-envelope theorem to that actual interpolant.

Convexity is required only on attainable counts. The lower-envelope proof
extends the final slope for convenience, proves the extension agrees on
those counts, and eliminates the extraneous table value at `card + 1` when
its interpolation weight is zero. The existing adjacent-count law supplies
all prescribed means and attains the lower endpoint. Thus negative,
decreasing, and nonmonotone convex tables are included; no unstated
positivity assumption is used.

`convex_cardinality_common_upper` uses finite strong induction on the
support, peeling a minimum-mean coordinate. Ordered first differences
bound the change for every vertex; common-threshold support makes that
bound exact for the threshold law. This is a terminating induction, so no
uncrossing termination or compact secondary-optimization premise is missing.
`cardinality_maximum` connects the law to the continuous graph hull. A
temporary Lean example checked it applies directly to `cardinalityFactor`.

## Verification

The following targeted commands passed from `formal/`:

```sh
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake build Formal.MultilinearGap.StructuralFeedbackAssembly Formal.MultilinearGap.StructuralCardinalityUpper Formal.MultilinearGap.StructuralInterpolation
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-feedback-final-review.lean
```

The build reported success (8735 dependency jobs). It was a build of the
three named modules, not project-wide verification. No CI status or logs
were inspected.

The temporary review file prints axioms for leaf-factor existence,
elimination-order existence, both universal domination statements,
residual extension, local repair, feedback forest gluing, payoff assembly,
the public box theorem, forest equality, the concrete interpolant minimum,
the cardinality maximum, the common cardinality upper law, and the attaining
lower law. Each lists only `propext`, `Classical.choice`, and `Quot.sound`;
none uses `sorryAx`. The same file checks the concrete C02 interpolant,
a fully fixed box, and the exact unit-cube specialization. The initial
unit-cube example needed an explicit function-extensionality identity for
the zero-to-one box map before simplification; that temporary test was
corrected and rerun successfully. No proof module needed correction.

Reviewed assembly and order SHA-256 values:

```text
4c35d47fae8f25f78db0c754c6f220b312b267a6d20f789b5410dc19cdbb29eb  StructuralFeedbackAssembly.lean
9f5844da42d3c495772332b7c0d89b81735b4b04a0d76ab487f34725b2b2d676  StructuralFeedbackOrder.lean
81344b22d979ed87d6a8b77e1f87d4fc66d120e49d177e18a1e2ce2012bd8895  StructuralCardinality.lean
9e9f0dd6d95ea55447fab2338c1a26bbc9d6464ffdc489fa3c6c3cd153bd8ee4  StructuralCardinalityUpper.lean
a01ffd1a827dc0aadca6e904f83e081791bb79b820324e24936a66ee5126cf3d  StructuralInterpolation.lean
```

The other five feedback foundations retain the hashes recorded in the
foundation review.
