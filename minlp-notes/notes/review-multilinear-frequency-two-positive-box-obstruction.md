# Independent review of the positive-box obstruction

Date: 2026-09-04. Reviewer: `review_extension`. Status: passed.

Reviewed [the exact counterexample](multilinear-frequency-two-positive-box-obstruction.md) independently. All six affine certificates, all four attaining distributions, and the ratio `7/6` are correct. This disproves extension of bipartite frequency-two exactness to arbitrary boxes with positive lower bounds.

## Exact certificate checks

For the binary states in lexicographic order `000,001,010,011,100,101,110,111`, the nonnegative certificate slacks are:

| Certificate | Slack vector |
|---|---|
| `xy >= 1+a+b` | `0,0,0,0,0,0,1,1` |
| `xyz >= 2a+2b+3c` | `1,0,0,1,0,1,0,5` |
| `f >= 4a+4b+4c` | `2,0,0,0,0,0,0,4` |
| `f <= 2+8a+4b+2c` | `0,0,2,0,6,4,6,0` |
| `xy <= 1+2a+b` | `0,0,0,0,1,1,0,0` |
| `xyz <= 1+6a+3b+2c` | `0,0,2,0,5,3,6,0` |

Slacks mean function minus lower bound, or upper bound minus function. Each slack is multilinear, so nonnegativity at all vertices establishes the bound throughout the cube. Moreover, any law on the cube can be replaced by a law on its vertices with the same means and the same expectations of all these multilinear functions: round coordinates independently conditional on the original point. Vertex-supported optimization therefore gives the exact envelopes.

An independent Python calculation using `Fraction` checked every slack and each displayed distribution's normalization, means `(1/4,1/4,3/4)`, and objective expectation. The lower expectations are `3/2` for `xy`, `13/4` for `xyz`, and `5` for their sum. The common upper distribution attains `7/4` for `xy` and `19/4` for `xyz`, totaling `13/2`. Thus the termwise gap is `7/4`, the hull gap is `3/2`, and their ratio is exactly `7/6`.

## Incompatibility and scope

The stated incompatibility can be made stronger: the optimum vertex law for the lower envelope of `xyz` is unique. Its tight states are `001,010,100,110`. The mean of `c` forces mass `3/4` on `001`; the remaining mass `1/4`, together with the means of `a` and `b`, forces all remaining mass onto `110`. It therefore has `P(a=b=1)=1/4`. In contrast, attaining the lower envelope of `xy` requires `P(a=b=1)=0` because its slack is exactly `ab`. A single law cannot attain both lower envelopes.

The original factor scopes are `{x,y}` and `{x,y,z}`. Each variable occurs in at most two factors. The dual multigraph consists of two parallel edges between the factor vertices and one dummy leaf for `z`; it has no odd cycle and is bipartite. The example concerns exact individual monomial envelopes, so it does not depend on a weaker recursive relaxation.

The example leaves the unit-cube and zero-lower-bound scaling results intact. Its ratio is below `3/2`, so it also leaves open whether a universal `3/2` gap bound extends to these positive boxes. No literature novelty claim is certified by this review.
