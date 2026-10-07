# Verification record

Date: 2026-10-03. Scope: the global-convex sparse-polynomial point theorem
and its unbounded-polyhedron extension in this folder.

The [main theorem](theorem.md) has been independently reconstructed in
the [full point-output review](../reviews/point-core/global-extension-review.md)
and by the radius reviewer. The latter's
[written review](radius-independent-review.md) covers the integrated
quadratic lower bound, affine-slope normalization, exact boundedness
alternative, sublevel estimates, integer-minor Hoffman bound, and the
attainment argument. A separate review of the sparse coefficient-row
argument found no mathematical blocker. These are internal mathematical
reviews, not external peer review or a priority determination.

The [exact-rational diagnostic](check_radius_construction.py) checks finite
fixtures for interpolation, integrated quadratic bounds, sparse invariant
subspaces, and radius formulas. The radius reviewer ran

```text
python3 research-20261003-arithmetic/global-point/check_radius_construction.py
```

The command passed nine interpolation-degree checks, 455 integrated
quadratic/decomposition checks, 121 sublevel checks, five radius fixtures,
one closed-form integration check, one check of a bounded representative
of an unbounded sublevel, the source equation (22) counterexample, and one
unboundedness certificate. The main author did not duplicate that run.
This diagnostic does not implement the general convex
value oracle, certify convexity for arbitrary input, or test asymptotic
running time.

The main author also ran an inline `python3 -B -` document check limited
to this folder. It passed for all five Markdown files and 18 local links,
paired code fences, trailing whitespace, control characters, and Python
syntax of the diagnostic. The targeted command

```text
git diff --check -- research-20261003-arithmetic/global-point
```

also passed. The inline whitespace checks include the new files, which
are not necessarily included in an unstaged Git diff.

Only targeted checks for this folder are in scope. No project-wide
verification, CI status, or CI logs are part of this record.
