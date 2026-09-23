# Independent semantic review of the closed-system consequences

Reviewer: the topic 28 source-inventory agent. Date: 2026-09-22.

Reviewed `ClosedSystem.lean` after the author's additions of closedness,
unboundedness, and whole-space equivalence interfaces. No mathematical or
statement-fidelity defect remains for frozen claims C01 and C02.

`quadratic_nonpos_convex` proves the actual closed sublevel is convex from
PSD. Its quadratic identity accounts for the nonnegative term
`s t (x-y)^T A (x-y)` and the affine constant when `s+t=1`.
`quadratic_nonpos_isClosed` derives closedness from continuity without
needing PSD. `quadratic_nonpos_ne_univ` handles both nonzero quadratic and
nonzero linear parts by reducing a supposed universally nonpositive
quadratic to a universally strict one after subtracting one, contradicting
topic 27's easy certificate direction. `quadratic_unbounded_above` shifts
the constant by an arbitrary real bound and applies that properness result.
This is a valid proof of full unboundedness, not just positivity at one
point.

`System.closed_convexHull_subset_aggregate` takes nonnegative weights and
a PSD aggregate and gives containment of the ordinary closed-feasible-set
convex hull in that closed quadratic sublevel. No hull closure or strict
feasibility is inserted. Nontriviality is needed only for the following
`Certificate.closed_convexHull_ne_univ` conclusion.

`System.closed_proper_hull_iff_certificate` assumes exactly nonempty strict
feasibility and AHC. The forward direction transfers properness to the
smaller strict hull and invokes topic 27; the reverse direction is the
unconditional easy implication. `closed_hull_eq_univ_iff_strict` and its
HHC specialization state the source's whole-space equivalence directly.
The certificate equivalence also has an explicit HHC specialization.

The review requested these supporting interfaces before coverage was
declared complete, and the author added them. This review ran no additional
Lean build; the reported author build and coordinator's final targeted
verification are separate machine-check evidence.
