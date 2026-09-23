# Completion coverage

The complete paper-to-declaration map is maintained with the standalone paper
in [its coverage guide](../../../paper-multilinear-gap/formal/COVERAGE.md).
The additions in this package are:

| Canonical module | Mathematical obligation |
|---|---|
| [Attainment](../../Formal/MultilinearGap/Attainment.lean) | Finite-box vertex laws, compact graph hulls, and attained envelope endpoints |
| [EnvelopeFunctions](../../Formal/MultilinearGap/EnvelopeFunctions.lean) | Identification with the greatest convex underestimator and least concave overestimator |
| [MonomialEnvelope](../../Formal/MultilinearGap/MonomialEnvelope.lean) | General exact individual envelopes and attaining laws preserving all ambient means |
| [PaperFoundations](../../Formal/MultilinearGap/PaperFoundations.lean) | Original-box scaled terms and `0 ≤ H_B ≤ T_B` |
| [ExactSize](../../Formal/MultilinearGap/ExactSize.lean) | Exact support count, attained maximum degree, occurrence count, and sparsity |
| [ExactAsymptotics](../../Formal/MultilinearGap/ExactAsymptotics.lean) | Actual-family logarithmic error and normalized gap-ratio limit |
| [Examples](../../Formal/MultilinearGap/Examples.lean) | Actual graph-hull equalities for all four printed examples and cutoff-boundary arithmetic |

The additions contain seven modules. Their dependency-complete standalone
closure has 48 modules; those files are copies of the canonical sources, not
independent formalizations. The existing disproof, exact-gap and sharp-growth
modules retain their earlier mathematical scope.

The [review](REVIEW.md) checks the full manuscript, including supporting prose.
Equivalent formal proofs need not reproduce every intermediate written
calculation. Literature attributions, novelty and external peer review are
not Lean theorem claims.
