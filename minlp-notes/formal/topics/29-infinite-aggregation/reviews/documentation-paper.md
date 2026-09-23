# Independent documentation and paper review

Reviewer: the topic 29 source-inventory agent. Date: 2026-09-22.

Reviewed the final topic 29 declaration map and
`paper-quadratic-aggregation/sections/92-formal-infinite-aggregation.tex`
against the frozen scope and final model, goodness, HHC, witness,
cardinality, and obstruction interfaces. No mathematical or scope mismatch
was found. The coordinator's final recorded machine checks now justify
the account's completion wording; this review did not run those checks.

The paper's system uses the exact Euclidean formulas, and its dimension
range `r≥2` includes the four-variable example. Its nonemptiness,
boundedness, and proper-hull claims are exported from `Model.lean`.
HHC is correctly described as the actual homogeneous image condition,
proved rather than supplied. The final added Gram-domain paragraph also
matches the proof: both support-bound necessity and realization are proved,
and determinant concavity gives the convex domain. Singular matrices and
zero hyperplane coefficients are covered. The section does not suggest a
proof of the excluded general Gram-map theorem.

Goodness retains both source conditions: the actual homogeneous matrix
has at most one negative eigenvalue counted with multiplicity, and its
strict aggregation contains the ordinary hull. The block decomposition,
at-least-`r` obstruction outside the cone, and exactly-one conclusion inside
the nonzero nonnegative cone match the formal statements. Neither the
source's spectral condition nor hull containment is replaced by the cone
inequality before the classification is proved. The final wording expressly
restricts the outside-cone lower inertia bound to nonnegative multipliers
violating the discriminant, and the inside-cone exact-one conclusion to
nonzero nonnegative multipliers.

The displayed Gram matrix, residual vector, and ray weights are exact.
The paper correctly uses a zero aggregate value to exclude the unperturbed
witness from the ordinary hull and reserves strict positivity for the
closed-hull witness. It states the indispensable-ray theorem conditional
on an actual exact strict description and explicitly says the full
intersection equality is not proved by this package. The nonexistence
of countable strict descriptions itself is unconditional for any proposed
countable good family in each required dimension.

The cardinality wording is faithful: `normalizeRay_pos_smul` gives positive
scale invariance, and the final theorem says the normalized-weight image
is uncountable. Thus the conclusion counts distinct rays, not repeated
family indices. The common third-coordinate-zero image collapses to zero
and cannot create an artificial uncountability result.

The finite closed obstruction is separately proved by actual perturbed
vectors and continuity of valid aggregates on `closure(convexHull S)`.
The paper does not identify this closure with the convex hull of the
original weak feasible set, claim countable weak sufficiency, or present
the strict witness argument as sufficient for the closed case.

The scope paragraph excludes the hull formula, countable weak sufficiency,
the weak-system hull identity, the SDP lift, arbitrary-quadratic
impossibility, approximation, the general Gram theorem, and literature
priority. These match `CLAIMS.md`. The standalone
`formal-infinite-aggregation.tex` includes the shared macros and the
self-contained section 92; it does not include a section with unresolved
cross-references to an omitted certificate proof.

This was a read-only review of Lean and LaTeX sources. No Lean or LaTeX
build was run by this reviewer. Targeted Python checks passed for local
Markdown links, all twelve claim rows, and occurrence of every mapped
declaration in the eighteen-module source list. A scan of the coordinator's
final two-page supplement log found no warnings, undefined references or
citations, or overfull/underfull boxes. Actual build, axiom audit, kernel
replay, PDF checks, and source fingerprints are in the coordinator's
targeted verification record. Paper-stage acceptance remains separate.
