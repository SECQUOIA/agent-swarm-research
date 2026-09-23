# Independent review of the minimum-gap spectral bound

Date: 12 September 2026. Reviewer: fresh subagent
`/root/spacing_bound_review`. Verdict: the proposed theorem and the exact
helper are correct under their stated stationary scalar covariance and
minimum-gap assumptions. The review does not establish publication priority
or validate a spacing-constrained optimization implementation.

Reviewed sources:

- [Spacing theorem](research-20260912-noisy-markov-spacing.md).
- [Previously reviewed base theorem](research-20260912-noisy-markov-memory.md).
- [Exact bound helper](../code/research_20260912/noisy_markov_spacing_bound.py),
  final reviewed SHA-256
  `6e2fa17897449a9a3b2cb17e468071c904ae173b9aa5dd8bcf33848ee017a77c`.
  The exhaustive suite tested the preceding version,
  `e51cc53586291bf4d1e720f98f5aef1995e5dc3209cd809d38bea6d76aca33cd`;
  the only intervening change and its focused checks are described below.
- Its `full_grid_variance_floor` and exact-input helper dependency in
  `certify_noisy_markov.py`, SHA-256
  `e9994b835f4d39897a7af9fb1e240163a69bec004fe140c7d5204e83a3beccc4`.

The reviewer made no edits to author code. No additional literature was
identified by this bounded mathematical and implementation review.

## Proof review

Write `b=abs(rho)`, with `P>=0`, `r>0`, and `b<1`. All local prediction
variances lie in `[0,P]`. The scalar update followed by a transition across
`d` calendar positions is

```text
T_d(x) = P + b^(2d) [r*x/(r+x)-P].
```

Its derivative in `x` is nonnegative. The expression in brackets is
nonpositive, so increasing `d` cannot decrease `T_d(x)`. Consequently a
sequence of `q` observations, whose successive gaps and last gap to the
target are at least `g`, gives target prediction variance at least
`T_g^q(P)`. Monotonicity and `T_g(P)<=P` imply that this iteration decreases
with its length. There are at most `m=floor(L/g)` local observations, giving
the proposed floor `r+T_g^m(P)`. The floor is attainable by the equally spaced
history at ages `g,2g,...,mg`; it is not merely a generic lower bound. Signed
transitions do not affect these variance recursions. The gain bound still
uses `P/(P+r)`; replacing its denominator by the new variance floor would
need a different argument.

For a residual pair at selected times `s<t`, write `h=t-s`. The base proof
gives a direct term `P*b^h` only when `h>L`. Each nonzero regression term
has absolute value at most `P*kappa*b^(h+2d)`, where `d=s-j` is an earlier
history age. Those ages are at least `g` and are pairwise at least `g` apart.
When `h<=L`, orthogonality further requires `d>L-h`. The maximum sum of
the decreasing nonnegative weights `b^(2d)` over either allowed interval is
obtained by placing ages at its first allowed integer and then every `g`
positions. This gives both proposed formulas for `phi(h)`, including the
integer endpoint `L+1-h`. The near-pair formula remains necessary: overlapping
local histories do not make all nearby residuals orthogonal.

The recurrence for `B(M)` follows by excluding or including the last allowed
distance `M`. Inclusion leaves distances at most `M-g`. At an anchor `t`,
the left and right distance sets have separate minimum-gap restrictions.
Their maximizing sets can even be combined into a feasible selection because
the closest possible cross-anchor pair is `2g` apart. Thus
`B(t)+B(n-1-t)` is exactly the largest sum of the pair majorants at that
anchor when cardinality is unrestricted. It need not be attained by actual
residual covariances: those were individually bounded first.

Each normalized off-diagonal covariance divides by `sqrt(d_s*d_t)>=d_*`.
The priced raw row majorant divided by `d_*` therefore bounds every absolute
row sum of `C-I`. Symmetry gives the spectral bound. The already reviewed
congruence argument then gives the precision sandwich with the same delta.
The precision statement itself remains valid for `delta>=1`; transferring a
finite upper certificate through `1/(1-delta)` requires `delta<1`.

The zero-bound shortcuts are sound. A complete local history (`L>=n-1`)
gives the true sequential factorization. A gap `g>=n` permits only empty or
singleton selections. Independent observations (`P=0` or `rho=0`) also give
exact local factorizations. Clipping the supplied `L` to `n-1` preserves the
model and can strengthen its variance floor.

For the state count, subtract `(j-1)*(g-1)` from the position of the `j`th
set bit. This bijects separated `q`-bit placements with ordinary `q`-subsets
of `L-(g-1)*(q-1)` positions and gives the stated binomial sum. It counts
possible information masks, not necessarily a complete constraint state.
If `L<g-1`, a selection at time zero has disappeared from the `L`-bit mask
at time `L+1`, although selecting then would violate the gap. Cooldown or
at least `g-1` retained bits is therefore essential. The maximum number of
selected positions in a horizon of length `n` is `ceil(n/g)`.

## Independent checks

[The review script](../code/research_20260912/review_noisy_markov_spacing.py)
forms dense rational covariance matrices, solves the local normal equations
by exact elimination, and forms the full residual covariance. It does not
use the author's Kalman recursion to generate its reference conditionals or
innovation floor. It enumerates separated histories to check the pair-weight
maxima, and enumerates full feasible selections to check row pricing rather
than reproducing the author's dynamic program.

[The saved result](../code/research_20260912/results/noisy-markov-spacing-independent-review.json)
reports all checks passed:

| Check | Number |
| --- | ---: |
| Exact subset/window covariance models | 22,734 |
| Exact local variance comparisons | 54,366 |
| Exact residual-pair inequalities | 58,488 |
| Exact raw row inequalities | 54,366 |
| Independently enumerated floor and row-pricing cases | 1,428 each |
| Enumerated pair-weight maxima | 2,604 |
| Exhaustive mask counts | 150 |
| Short-window cooldown witnesses | 30 |
| Malformed-input rejections | 15 |

The exact suite covers every feasible subset for horizons `n=1,...,7`,
every gap `g=1,...,n+1`, and every supplied window `L=0,...,n+1`. Its six
rational covariance settings include negative correlation, `rho=99/100`
with nugget `1/100`, independent observations, zero latent variance, and
different latent-to-nugget ratios. Mask counts are exhaustive through
`L=14`. These tests explicitly include `L=0`, `g>L`, `g>=n`, and `n=1`.

For every exact model, the script also compares directly computed normalized
row sums and `||C-I||_2` against delta. These last calculations use floating
square roots and eigenvalues, with tolerance `1e-13+1e-12*delta`; the
covariance, floor, pair, and raw row checks use exact rational inequalities.
The largest ratio was one up to roundoff. Equality occurs in the two-time,
zero-memory example, where there is one nonzero off-diagonal covariance.

Reproduce from the project root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_noisy_markov_spacing.py
```

## Implementation boundary and resolved robustness observation

The helper correctly rejects invalid integer arguments, inexact float
covariance inputs, and inadmissible covariance parameters. It returns exact
rational quantities for admissible rational data. This acceptance applies to
the reviewed helper; a design solver or objective certifier using it must
separately enforce the minimum gap in its feasible set and incumbent checks.

The initial helper formed `abs(rho)**gap` before handling `gap>=n`, including
when `floor(L/gap)=0`. A huge otherwise valid gap could therefore cause
unnecessary large-integer work even though the innovation floor is simply
`P+r`. The author fixed this during review by assigning `P+r` directly when
`m=floor(L/gap)=0`. The changed expression is mathematically identical to the
previous one: a one-observation full-grid variance floor is `P+r`, independent
of the transition argument.

The reviewer inspected that change and checked four additional cases with
`(n,L,g)` equal to `(1,10^12,10^12)`, `(20,3,10^12)`, `(20,3,5)`, and
`(20,0,4)`, with `rho=-99/100`, `P=1`, and `r=1/100`. All exact floor, raw-row,
and delta comparisons passed. For the finite nonzero rows, the reference
enumerated feasible sets and summed `P*abs(rho)^h` directly; the huge-gap
cases returned zero as required. The updated hash and focused results are
stored alongside the original exhaustive-test hash in the saved result.
This fixes a resource-use issue; the original formulas were already valid.
