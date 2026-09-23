# Quadratic aggregation consequences

Status: complete within the [frozen scope](CLAIMS.md). All 12 obligations
are proved and independently reviewed. Warning-free builds of 10 new
modules, the 158-declaration axiom audit, and all module kernel replays passed.

This package extends [topic 27](../27-quadratic-aggregation/README.md) with
the closed-system equivalence, the Shor-relaxation equivalence, its converse
without hyperplane convexity, an exact SDP characterization, and the two
recommended examples delimiting these conclusions. Its source is Section 4
and the relaxation-strength example in Section 7 of the
[quadratic aggregation note](../../../results/quadratic-aggregation-trivial-hull-certificate.md).
The [source inventory](SOURCE-REVIEW.md) records the mathematical interfaces
and review requirements before completion.

The Shor projection uses the usual positive semidefinite block matrix
`[1 x^T; x X]` and linear lifted inequalities. A covariance formulation is
proved equivalent to that block formulation. The converse without
hyperplane convexity uses open-set separation, producing actual strictly
feasible PSD covariance slacks without assuming the PSD-image cone is
closed. The boundary examples prove their actual HHC using the new
algebraic proof of Dines' theorem.

- [Claim-to-declaration coverage](COVERAGE.md).
- [Independent reviews](REVIEW.md).
- [Targeted verification and fingerprints](VERIFICATION.md).
- [Final consequence interfaces](../../Formal/QuadraticAggregation/Consequences.lean).

The SDP result is an exact characterization by feasibility and optimum values;
it does not verify a numerical solver. The full BDS good-aggregation hull
description, the general classical convexity criteria, and additional source
examples remain outside this package. The separately recommended infinite
aggregation construction is a later package, not a claim of topic 28.

Topic 27's frozen claims and historical verification records remain intact.
Only targeted checks for the new modules and their interfaces are authorized
locally. The verification record lists the actual commands and outcomes;
no CI result or project-wide local check is inferred.

The related paper is under concurrent development. The
[consequences supplement](../../../paper-quadratic-aggregation/formal-consequences.tex)
and [new section](../../../paper-quadratic-aggregation/sections/91-formal-consequences.tex)
distinguish the old core from these verified consequences. The supplement
builds independently; paper-stage acceptance remains a separate process.

The separately completed [infinite-aggregation package](../29-infinite-aggregation/README.md)
extends the recommended work to actual HHC, exact spectral goodness,
uncountably many indispensable strict rays, and finite closed-hull
impossibility for that explicit construction.
