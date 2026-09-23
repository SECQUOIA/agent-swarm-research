# Complete verification of the focused cubic-gap paper

This is topic 2 of the requested sequential completion. Work began after
[topic 1](../10-multilinear-completion/README.md) passed its canonical and
standalone checks, including both kernel replays.

- [Focused paper and standalone distribution](../../../paper-cubic-gap/README.md).
- [Mathematical coverage](COVERAGE.md).
- [Independent mathematical review](REVIEW.md).
- [Verification record](VERIFICATION.md).
- Canonical proof sources: [`Formal/CubicGap`](../../Formal/CubicGap).
- [Earlier finite-witness package](../04-cubic-gaps/README.md).

The scope is the universal `31/12` upper bound on all finite nonnegative boxes,
optimality of the fixed `18:6:7` mixture for uniform termwise guarantees,
and the analytic integer-coefficient family giving the limiting lower bound
`1610000/743033` (equivalently `4830000/2229099`). Seven existing exact finite
witnesses supply supporting examples. The exact cubic supremum is not known.

General coefficient removal, equal-marginal classification, and the general
two-level asymptotic family are outside the focused paper. The paper and
coverage guide identify this boundary explicitly.

Status: complete. All canonical and standalone checks passed, including
both kernel replays. See [the verification record](VERIFICATION.md) for
logs, fingerprints, and the completed claim review.
