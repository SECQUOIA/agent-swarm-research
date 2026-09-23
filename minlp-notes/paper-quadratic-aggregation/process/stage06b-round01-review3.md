# Stage 6b, round 1, independent review 3

Date: 2026-09-22. Verdict: **pass; no major or minor correction identified**.

I reviewed the appendix, its author and literature reports, the source
snapshot, the exact-check script, and the source research note. I did not
read the other current reviewers' reports. I made no manuscript edits and
used no subagents.

## Mathematical audit

The cone argument correctly uses strict feasibility to exclude every
nonzero nonnegative dependence equal to zero. The negative evaluation
functional is strictly positive on the nonzero matrix cone, and its unit
section is the convex hull of the normalized generators. Consequently the
section is a full-dimensional polygon in a plane, the cone is pointed,
and its numbers of rays and facets coincide. Removing generators away
from extreme rays preserves both the strict feasible set and the cone of
aggregation matrices.

The HHC deduction has the needed dimension: a hyperplane in the
homogeneous space has dimension n, and n is at least three. Restricting
the positive definite combination preserves positive definiteness. The
joint image of the original forms is a linear image of the joint image
of three basis forms, so the full-system HHC theorem applies.

In the directional argument, the exit time is finite and nonnegative,
all facet inequalities remain nonnegative, and a selected facet is
reached. The zero-matrix possibility is correctly excluded by inertia.
The proof explicitly supplies two nonnegative coefficient representations
and their signed difference, which is precisely the hypothesis needed
for PSD improvement. A cut on a selected facet dominates each original
nonredundant good cut. The two-generator reduction is applied relative
to the full feasible set, rather than to a larger two-row subsystem.
This proves the count 2|J_-(D)|. The perturbation of a PSD matrix outside
the negative cone to a positive definite direction also has the correct
sign and proves the conditional 2k-2 bound.

The ellipsoid construction is valid for every listed n and m. The
Vandermonde identity makes the span exactly three-dimensional. Its
boundary witnesses give zero for exactly one row and strictly negative
values for every other row. Thus every exact strict aggregation family,
including an infinite family, must contain the corresponding multiplier
ray. For a finite weak family omitting that ray, strict slack persists in
a neighborhood and a radial outward perturbation contradicts exactness.
The manuscript correctly does not extend this finite-family argument to
infinite weak families.

Appending the two negative-square rows changes the strict feasible set.
The small midpoint perturbation proves that its hull is still the old
open convex set. Both added rows are strictly negative at every witness,
so all old multiplier rays remain indispensable. The witness functionals
expose the old matrix rays, while the zero constant coefficient argument
proves extremality of the two new rays. The total is therefore k=m+2.
The displayed combination producing the negative constant basis matrix
proves containment of the negative PSD cone, including its boundary.
The weak set is unchanged, compact, has nonempty interior, is the closure
of its interior, and has no nonzero feasible direction at infinity.
Exactly m good rows describe each relevant hull. This refutes the
proposed general-cone two-bound, but does not refute 2k-2; the final
paragraph correctly states that distinction.

The final inertia example is correct and is used only to invalidate
unrestricted addition as a proof strategy. The appendix does not claim
that its two illustrative matrices alone supply a counterexample to an
unstated full aggregation theorem.

## Prior work and presentation

I inspected the relevant passages in the locally available primary BDS
v2 and BD v1 text and freshly opened both primary arXiv HTML versions:

- [BDS v2](https://arxiv.org/html/2210.01722v2), especially Propositions
  2.22, 9.1 and 9.6;
- [BD v1](https://arxiv.org/html/2405.18282v1), especially Propositions
  8.6 and 8.10.

The cited BDS result supplies the known facet count and its pair-support
reduction. BD's cited complementary-case result concerns three
generators; the appendix distinguishes that theorem from the proposed
many-generator extension. Credit and version-specific locators are
accurate. The manuscript avoids claiming an optimal general count or
priority from unsuccessful searches. The new examples are presented as
supporting consequences with complete elementary proofs. I found no
unclear notation, unsupported novelty claim, or missing hypothesis that
requires a correction.

## Targeted checks actually run

1. Ran `python3 paper-quadratic-aggregation/supplement/check_three_dimensional_span.py`.
   Passed the exact polynomial identities and all 1,235 rational witness
   evaluations. I also checked the algebra and the universal proofs by
   hand; sampled signs do not establish the general theorems.
2. Recomputed SHA-256 hashes for all 12 entries in
   `process/stage06b-author-snapshot.json`. Every entry matched.
3. Searched the existing targeted stage build log
   `build/stage06b/main.log` for `Warning`, `Overfull`, `Underfull`, and
   `undefined`. No matches. This is inspection of the author's local
   build output, not an independently rerun compilation.

No project-wide checks, CI queries, solver experiments, or Lean reruns
were performed.
