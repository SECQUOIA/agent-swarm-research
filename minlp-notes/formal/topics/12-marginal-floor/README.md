# Sharp multilinear gaps under a marginal floor

Status: complete and verified on 2026-09-17.

This is the first topic in the [recommended-topic sequence](../../RECOMMENDED-TOPICS-PLAN.md).
The source is the [marginal-floor result note](../../../results/positive-multilinear-marginal-floor-gap.md).
The complete scope includes its finite bound, leading-constant-one asymptotic,
two-sided-strip variant, and bound on the original nonnegative-box termwise gap.

- [Mathematical obligations](CLAIMS.md).
- [Claim-to-declaration coverage](COVERAGE.md).
- [Independent review](REVIEW.md).
- [Verification record](VERIFICATION.md).
- Canonical sources: [`Formal/MultilinearGap`](../../Formal/MultilinearGap).

The new density is different from the previously verified degree-dependent
harmonic law. Existing proofs of general envelope semantics, integrated finite
laws, easy-term bounds and the dyadic lower family are reused where their
statements apply. They do not by themselves prove the marginal-floor theorem.

## Mathematical result

Let `C(δ)` be the supremum of the sum of individual monomial hull widths divided
by the polynomial's graph-hull width, over positive-coefficient multilinear
polynomials on unit cubes of every finite dimension and degree, evaluated at
points whose coordinates are at least `δ`. Only positive denominators enter
the ratio class. For `0 < δ < 1`, the class is nonempty and bounded above.
As the real variable `δ` tends to zero from above,

```
C(δ) / (log(1/δ) / log(log(1/δ))) → 1.
```

The same limit holds when every mean must also be at most `1-δ`. This is an
asymptotic statement, not equality of the two worst-case functions at every
fixed floor.

The finite upper bound uses

```
B = max 2 (log(1/δ))
τ = δ/B²
L = log((1+τ)/τ)
I = ∫ z in 0..1, 1-exp(-1/(L*(z+1/B²)))
C(δ) ≤ 1/I + 2/(1-exp(-1)).
```

A single explicitly defined finite law preserves all coordinate means and
gives the required bound for every term simultaneously. Clipped failure
probabilities are repaired to have exactly the required means. The lower
witnesses have unit coefficients and use `floor(log₂(1/δ))` levels of the
existing dyadic family, so they apply to every sufficiently small real floor.

For a nonnegative box, the hypothesis concerns each nonfixed coordinate's
normalized mean `(x_i-l_i)/(u_i-l_i)`. The conclusion bounds the original
monomial factorization. Fixed coordinates, zero coefficients introduced by
expansion, and zero hull widths are covered by the multiplicative bound.

## Proof layout

| Module | Purpose |
|---|---|
| `FloorDomain` | Actual ratio classes, nonempty witnesses and original-box transfer |
| `FloorSemantics` | Exact monomial gap and attained maximum deficiency |
| `FloorDensity` | Shifted density, clipping and exact marginal repair |
| `FloorCoupling` | Common finite law, means, clipping-sensitive union estimate |
| `FloorGain` | Uniform integral gain and positivity |
| `FloorUpper` | Simultaneous two-law mixture and finite cube bound |
| `FloorExpBound`, `FloorIntegralBounds` | Explicit integral sandwich |
| `FloorAsymptotics` | Parameter and upper-bound limits |
| `FloorLower` | Actual unit-coefficient strip witnesses and lower limits |
| `FloorResults` | Finite supremum bound, both sharp limits, original-box theorem |

The public terminal declarations are `floor_finite_bound`,
`sharp_marginal_floor_growth`, and `marginal_floor_original_box_bound` in
[`FloorResults.lean`](../../Formal/MultilinearGap/FloorResults.lean).
They use the canonical actual graph-hull definitions and assume none of the
new density, integral, or asymptotic claims.

## Reproduce

From `formal/`, run:

```sh
bash scripts/verify.sh
```

This checks the complete canonical project. The topic verification record
contains the passing output and the dependency-source fingerprints.
Literature priority, numerical experiments and physical
validation are separate from these mathematical conclusions.

The user requested a stop after this topic. Later topics remain queued in
the recommended-topic sequence.
