# Closed-system and consequence review

Date: 2026-09-22. Status: passed for the scope below.
Reviewer: the agent that implemented topic 27's `EasyDirection.lean`;
`ClosedSystem.lean` and `Consequences.lean` were implemented by other agents.

No correctness or source-fidelity issue remains in the reviewed modules.
The review compared their public conclusions with frozen claims C01, C02,
C05, and the C06 assembly, and with source Corollaries 1 and 4 and Lemma 4.
This is not a completion review of all twelve topic 28 claims.

## Closed-system results

The strict-to-closed inclusion, aggregation of closed inequalities, and
convexity of the PSD quadratic sublevel set have the intended orientation.
The properness argument covers a zero quadratic part with a nonzero linear
part: shifting the constant down by one would turn an everywhere nonpositive
aggregate into an everywhere strictly negative nonconstant PSD quadratic,
which the previously proved certificate theorem rules out.

`quadratic_unbounded_above` supplies the stronger conclusion explicitly for
all real thresholds and both nonconstant cases. `quadratic_nonpos_isClosed`
proves topological closedness without requiring PSD. Together with
`quadratic_nonpos_convex`, `quadratic_nonpos_ne_univ`, and
`closed_convexHull_subset_aggregate`, these discharge all parts of C01.
The initial review identified missing named unboundedness, closedness, and
containment conclusions; the author added them, and they were reviewed and
checked before this sign-off.

`Certificate.closed_convexHull_ne_univ` assumes neither strict feasibility
nor hyperplane convexity. `closed_proper_hull_iff_certificate` assumes strict
feasibility and asymptotic hyperplane convexity exactly as the source does.
Its forward direction first transfers properness from the closed hull to the
strict hull by inclusion; it does not claim that the closed feasible set
equals the closure of the strict feasible set. The equivalence of strict and
closed properness does not assert that the two hulls are equal, or that
either hull is a closed set. `closed_hull_eq_univ_iff_strict` gives the requested
whole-space formulation, and the HHC specializations preserve strict
feasibility. No positive dimension or constraint-count assumption was added.

## Consequence assembly

`shorProjection_eq_univ_iff_no_certificate` states the hypothesis-free-in-HHC
converse with strict feasibility retained. Its only premise is nonemptiness
of the original strict feasible set; it takes no cone-closedness, duality,
or separating-certificate assumption. The inspected `ShorDuality` interface
constructs strict PSD slack feasibility by separation from an open orthant,
so this assembly does not infer membership merely from closure membership.

`shor_and_hulls_eq_univ` and its HHC specialization concern `shorProjection`
from `ShorModel`. That definition uses covariance slack, and
`mem_shorProjection_iff` explicitly identifies it with the actual block-PSD
Shor projection. The two assembled equivalences therefore concern the
projection itself, not its closure or a replacement intersection of aggregate
inequalities. Both preserve strict feasibility and the stated AHC or HHC
hypothesis. The proof uses the previously established convexity of the Shor
projection when passing from feasible-set containment to hull containment.

This review checks the consequence statements and their dependency interfaces;
it does not replace the separate detailed review of block-PSD algebra,
semidefinite separation, SDP coordinate optimization, or the examples.

## Targeted verification

The following commands passed locally:

```text
lake build Formal.QuadraticAggregation.ClosedSystem
lake build --wfail Formal.QuadraticAggregation.ClosedSystem Formal.QuadraticAggregation.Consequences
lake env lean -E warning topics/28-quadratic-aggregation-consequences/verification/ReviewClosedConsequences.lean
```

The review file explicitly checks the pure linear unboundedness specialization
and the absence of an HHC premise from the unconditional Shor equivalence.
It also prints the axioms of eleven reviewed results. The captured output in
`verification/review-closed-consequences.log` reports only `propext`,
`Classical.choice`, and `Quot.sound`; the warning-as-error command passed.
An initial attempt to pass Lake's `--wfail` flag directly to Lean was rejected
as an unsupported option; the recorded successful Lean command uses its
`-E warning` option instead.

No project-wide verification was run, and no CI status or logs were inspected.
