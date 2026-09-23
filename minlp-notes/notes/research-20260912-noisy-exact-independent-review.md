# Independent review of the rational noisy-Markov certificate

Date: 2026-09-12. Status: passed for the reviewed source and saved instance.
This fresh review was conducted independently of the author. No remaining
mathematical or implementation defect was found. The result certifies the
stated rational instance and its recorded positive gap; it does not prove that
the selected design is exactly optimal or establish research priority.

Reviewed artifacts:

- [Certificate implementation](../code/research_20260912/certify_noisy_markov.py).
- [Self-contained n=48 certificate](../code/research_20260912/results/noisy-markov-exact-certificate-n48.json).
- [Independent reusable verifier](../code/research_20260912/review_noisy_markov_exact.py).
- [Independent verification report](../code/research_20260912/results/noisy-markov-exact-independent-review.json).
- [Scalar and block approximation theorem](research-20260912-noisy-markov-memory.md)
  and its [fresh mathematical review](research-20260912-noisy-markov-independent-review.md).

## What the certificate proves

The model has candidate covariance

```text
R_ij = P rho^|i-j| + r 1{i=j},
|rho| < 1, P >= 0, r > 0,
J(S) = J0 + F_S^T R_SS^-1 F_S,  |S| = k, J0 > 0.
```

Here covariance is fixed with respect to the estimated mean parameters. The
candidate calendar is the consecutive integer grid, and the memory length
counts calendar intervals, including unselected candidates. All JSON decimal
input numbers are interpreted as exact rationals. This is explicit in the
certificate: it does not silently claim that the displayed decimal instance
is identical to an unrecorded, higher-precision physical model.

Let `W_L(S)` be the sum of local conditional information contributions, with
the prior excluded. The previously reviewed theorem gives

```text
(1-delta) F_S^T R_SS^-1 F_S <= W_L(S).
```

For `delta < 1`, the matrix

```text
E(S) = J0 + W_L(S)/(1-delta)
```

therefore dominates `J(S)`. For **any** rational SPD reference `N`, monotonicity
and concavity of the log determinant yield

```text
log det J(S)
 <= log det N - p + tr(N^-1 J0)
    + sum_(t selected) tr(N^-1 W_(t,H_t))/(1-delta).
```

No accuracy, feasibility, or optimality of the numerical matrix used to choose
`N` is required. Symmetrizing and rounding that matrix is harmless after its
rounded value passes an exact SPD check. This avoids treating a numerical
inverse, gradient, or optimization stopping criterion as a proof.

Each last term is calculated exactly, multiplied by a positive integer grid,
and rounded **up** to an integer. The count/mask dynamic program maximizes
their sum over every cardinality-`k` subset. Dividing its integer maximum by
the grid gives a valid global linear upper bound. The rounding adds less than
`k/grid` to the maximum exact linear score when `k>0`; no rounding correction
needs to be subtracted. Exact-count reachability pruning is correct, and the
mask update retains precisely the last `L` calendar decisions. The `L=0`
transition and empty selected set are handled correctly when the spectral
certificate is usable.

Finally, a rational upper enclosure of `log det N` completes the objective
upper bound. A rational lower enclosure of the determinant log of the **true**
selected covariance information gives the feasible lower bound. The stored
rational difference is thus an exact global objective-gap certificate.

## Why the full-calendar innovation floor is valid

The implementation computes

```text
d_star = min_(t=0,...,n-1) Var(Y_t | Y_0,...,Y_(t-1)).
```

Every local history is a subset of the complete past. Conditional variances
under this fixed Gaussian covariance decrease when observations are added, so
every local conditional variance is at least `d_star`. Dividing the residual
covariance bounds by this floor is valid. It is important that only the
normalization denominator changes: the gain factor remains `P/(P+r)`.

The author's stationary Kalman loop evaluates exactly the `n` needed
innovation variances, including the unconditional first one. Negative `rho`
has the same variance recursion but the correct signs in regression
coefficients. The reviewer recomputed `d_star` from the diagonal of an exact
LDL decomposition of the **dense full covariance**, independently of that
recursion. The two rational values agree for the saved n=48 instance and all
tested smaller instances.

The reviewer also reconstructed the refined spectral constant by summing the
near and far residual-distance bounds separately. This agrees exactly with
the author's closed form. The overrides `rho=0`, `P=0`, or `L>=n-1` correctly
give zero approximation error.

## Logarithm endpoints

The author's range reduction puts a positive rational into `2^e z` with
`1<=z<2`. Lower and upper grid neighbors of `z` remain in `[1,2]`. For
`t=(z-1)/(z+1)`, the positive atanh series has remainder at most

```text
2 t^(2m+1) / ((2m+1)(1-t^2)).
```

Thus using the lower neighbor for the partial sum and the upper neighbor for
the partial sum plus remainder gives correctly directed bounds. Multiplying
the `log 2` enclosure by a negative exponent reverses its endpoints; the
implementation makes that reversal correctly.

The independent verifier uses a different positive series,

```text
log z = sum_(j>=1) (1-1/z)^j/j,
tail_m <= (1-1/z)^(m+1) / ((m+1)/z),
```

with substantially narrower rational enclosures. These independent intervals
lie inside every tested author interval, including values near one and two,
positive and negative binary exponents, and deliberately coarse grids/orders.

## Independent checks and the saved instance

The reusable verifier passed:

- 244 complete tiny certificates, checking all 816 relevant subsets against
  each global upper bound with independent rational determinant-log bounds.
- 504 true-information identities against dense selected-covariance inversion.
- 480 local regression/variance identities against dense conditional inversion.
- Exact PSD checks of the prior-aware transfer on every enumerated subset.
- 141 logarithm enclosure checks, including `2^300`, `2^-300`, and rational
  values close to range-reduction boundaries.
- 29 malformed input/option rejections, including non-SPD or asymmetric priors,
  bad dimensions, invalid cardinalities/windows/selections, forbidden inexact
  inputs, invalid covariance values, and state-cap refusal.

Tiny cases cover `n=1,...,6`, one to three parameters, empty/intermediate/full
cardinality, zero latent variance, zero/positive/negative correlation, zero
memory, truncated memory, and complete or longer-than-calendar memory.

For the saved `n=48`, `p=3`, `k=16`, `L=6` certificate, independent recursive
pricing used tuples of recent calendar indices, rather than the author's bit
masks. It visited 26,335 suffix states and evaluated 2,751 arc scores. It
reproduced the recorded integer maximum and priced selection exactly. The
true selected information was independently recomputed by inverting its
16-by-16 rational covariance. A separate 90-digit log evaluation gives

```text
log det J(selected)
 = 7.69664964662398042987266313070535827594017901207805796727270264558...

stored rational lower bound, decimal display = 7.696649646623975
stored rational upper bound, decimal display = 7.708927433337252
stored rational gap, decimal display         = 0.012277786713277497
```

The exact rational fields are the formal endpoints. Their ordinary
floating-point display fields are for readability and are not separately
rounded outwards. The independent check takes about ten seconds on the
current machine; this is a verifier timing, separate from the author's
certificate construction time. Exhaustive enumeration of all `48 choose 16`
designs is unnecessary: the reviewed spectral theorem, tangent inequality,
and independent exact pricing establish the global upper bound.

The saved problem data were compared rationally with the indexed benchmark
case. The saved input and source hashes also matched. Including complete
problem data and the actual tangent reference makes the proof reconstructible
without relying only on a hash of an otherwise changing benchmark file.

## Review corrections and limits

An initial source version indexed the tangent source before checking its
dimensions. It could silently truncate an oversized matrix. The author added
the missing dimension guard during this review; the reviewed version rejects
both undersized and oversized inputs. This was an input-validation issue,
not a way to obtain an invalid bound, because the resulting tangent reference
was still checked for SPD. No author file was edited by this reviewer.

The state cap limits the stated state-count estimate; it is not a precise
Python memory or rational-bit-complexity bound. Very large inputs or rational
numerators can still make construction expensive. Failure of exact SPD
validation after coarse rounding causes refusal rather than a certificate.
These are explicit computational limits, not mathematical qualifications to
a successfully produced result.

Reproduce from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_noisy_markov_exact.py
```

The JSON review report records source, certificate, and verifier hashes to
identify the actual checked versions. This review supports correctness of
this certificate implementation and the saved instance. It adds no claim
that this is the strongest possible certificate, that the finite-history
method is novel, or that it is faster than a suitable competing solver.
