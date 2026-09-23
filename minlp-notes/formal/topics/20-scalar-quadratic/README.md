# Scalar quadratic precision

Status: complete. All 24 frozen obligations, independent reviews and targeted
build, axiom and kernel checks passed.
Topic 20 verifies the scalar quadratic rank and inertia
laws against arbitrary convex lifts with unrestricted integer coordinates,
and the matching explicit binary linear constructions.

Sources are the rank and inertia result notes and the scalar section of
[the integer-dimension paper](../../../paper-integer-dimension/README.md).
The package proves actual least-count laws, including the exact square
threshold, the graph coefficient `rank(H)/2`, and the epigraph/hypograph
coefficients `k_-/2` and `k_+/2`. It includes the sharp curvature constant,
zero-rank and zero-inertia cases, actual finite affine constructions and their
sizes, one-sided product formulas, continuous folding, and the square
epigraph row lower bound. Product lifts attain the exact error in the convex
model; finite linear lifts have arbitrarily small positive additional error
at the same binary count. The broader
quadratic-system results remain in topic 26.

- [Frozen claims](CLAIMS.md).
- [Independent source review](SOURCE-REVIEW.md).
- [Coverage](COVERAGE.md).
- [Review record](REVIEW.md).
- [Targeted verification](VERIFICATION.md).

Only topic-specific checks are run locally; no project-wide verification or
CI inspection is part of this work. Topics 21–26 remain queued.
