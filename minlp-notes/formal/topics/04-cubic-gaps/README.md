The later [focused cubic completion](../11-cubic-completion/README.md) adds
the universal upper bound, fixed-mixture optimality, and analytic lower-family
bounds. This page records the earlier finite-witness scope.

This topic verifies finite cubic relaxation-gap examples from
[`03-cubic-equal-means.tex`](../../../paper-relaxation-limits/sections/03-cubic-equal-means.tex)
and its [certificate appendix](../../../paper-relaxation-limits/sections/appendix-cubic-certificates.tex).

The proofs connect the finite count certificates to the actual polynomial graph
on the continuous unit cube. They prove the exact lower envelopes, construct
attaining distributions with every singleton mean correct, and prove the exact
upper envelopes. The 192-variable example checks all 274,625 count triples.

| Family | Variables | Exact convex envelope | Exact concave envelope | T/H |
|---|---:|---:|---:|---:|
| Two groups, m=4 | 8 | 11 | 27 | 27/16 |
| Two groups, m=8 | 16 | 120 | 252 | 21/11 |
| Two groups, m=12 | 24 | 441 | 891 | 99/50 |
| Two groups, m=16 | 32 | 1088 | 2160 | 135/67 |
| Three groups, m=6 | 18 | 2750/13 | 1647/4 | 20891/10411 |
| Three groups, m=8 | 24 | 3572/7 | 971 | 6601/3225 |
| Three groups, m=64 | 192 | 34172072/105 | 587944 | 7443345/3445256 |

The package also proves the scalar two-level minorant and the five-interval
Bernstein certificate with positive slack `901/120000`. The 52-variable
homogeneous example has 4320 distinct unit-coefficient cubic monomials, strictly
interior means, and actual gap ratio at least `2700/1343 > 2`. Its proof is in
`Homogeneous.lean` and its supporting modules.

Proofs are in [`Formal/CubicGap`](../../Formal/CubicGap). The
[coverage record](COVERAGE.md) separates the proved claims from the rest of the
paper. The [verification record](VERIFICATION.md) records completed checks.

Run the complete project check from `formal/` with `bash scripts/verify.sh`.
The finite certificate generator is an untrusted source producer; every emitted
inequality is checked in Lean. Check reproducibility with:

```bash
python3 topics/04-cubic-gaps/generate_large_finite.py --check
```
