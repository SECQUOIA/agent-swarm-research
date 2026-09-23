This topic proves the exact reciprocal-anchor hull with one box-bounded leaf,
and an explicit obstruction when two individual leaf hulls are intersected.
The source is [`common-factor-reciprocal-anchor-hulls.md`](../../../results/common-factor-reciprocal-anchor-hulls.md).

For `0 < a < b`, Lean proves that the convex hull of
`(X, 1/X, Y, XY)`, with `a ≤ X ≤ b` and `0 ≤ Y ≤ 1`, is exactly the
stated linear inequalities plus either the 3×3 PSD condition or two rotated
SOC constraints. The proof covers leaf means zero and one and handles zero
perspective denominators. Sufficiency constructs a representation with at most
six atoms. The fixed-anchor case `a = b` has a separate linear description.

Lean also proves that the two rational leaf examples each belong to their
individual hull, while their combined point lies outside the true two-leaf
hull. The separating inequality has the exact correction `1/400`.

Start with [`Hull.lean`](../../Formal/ReciprocalAnchor/Hull.lean) and
[`Joint.lean`](../../Formal/ReciprocalAnchor/Joint.lean). All proofs are in
[`Formal/ReciprocalAnchor`](../../Formal/ReciprocalAnchor); the
[coverage record](COVERAGE.md) gives their scope and the
[verification record](VERIFICATION.md) records completed checks.

Run `bash scripts/verify.sh` from `formal/` to check the project.
