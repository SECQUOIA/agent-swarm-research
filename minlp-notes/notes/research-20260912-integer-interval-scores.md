# Integer interval arc scores for exact design certificates

**Status: [accepted by fresh independent review](research-20260912-integer-interval-scores-independent-review.md), including all 31,900 arcs after input hardening. No novelty claim for interval arithmetic.** The isolated [component](../code/research_20260912/integer_interval_scores.py) replaces repeated large-rational arc calculations with guaranteed integer upper bounds. It does not change the reviewed [spacing certifier](../code/research_20260912/certify_spacing_design.py), the information approximation, the tangent reference, or the feasible-history graph.

The saved 96-candidate kinetics certificate has minimum sampling gap 2, information window 13, and 32 selected observations. Its exact decimal correlation is \(0.6324555320336759\). The resulting tangent weights have numerators or denominators up to 4,573 bits. Evaluating all 31,900 distinct arcs with these exact rational weights took 33.01 seconds in the comparison below. The interval component evaluated the same arcs in 0.29 seconds and increased the final upper bound by exactly \(10^{-8}\).

For exact rational sensitivities \(F_t\in\mathbb Q^p\), symmetric tangent weights \(H\), conditional coefficients \(b_j\), and positive conditional variance \(d\), an arc has score

\[
 s=\frac{g^T H g}{d},\qquad
 g=F_t-\sum_j b_jF_{t-a_j}.
\]

In the spacing certificate, \(H=N^{-1}/(1-\delta)\) is positive definite. The component accepts any symmetric rational \(H\); it does not require a positive-semidefinite test on rounded entries.

Let \(G_F,G,G_s\) be positive integer grids. Each sensitivity is enclosed by integer endpoints divided by \(G_F\). Each coefficient and each entry of \(H\) is enclosed by integer endpoints divided by \(G\). Every enclosure uses exact rational floor and ceiling, including negative data. Set

\[
 d_\ell=\lfloor Gd\rfloor>0.
\]

The implementation explicitly fails if this floor is nonpositive. A finer coefficient grid can resolve a positive variance below the current grid scale.

Integer interval subtraction and multiplication give an enclosure \([g_i^-,g_i^+]/(GG_F)\) of each adjusted sensitivity. The diagonal term uses the square enclosure: its lower endpoint is zero when the interval crosses zero, and otherwise the smaller endpoint square. The upper endpoint is the larger endpoint square. Off-diagonal terms use interval multiplication and exact symmetry, so only \(i<j\) terms need evaluation, with multiplier 2. Let \(Q^+\) be the resulting integer upper endpoint. Then

\[
 g^THg\le \frac{Q^+}{G^3G_F^2}.
\]

The coefficient intervals may be dependent, and the rounded matrix may be indefinite. Neither fact invalidates the inclusion: each term is enclosed separately and interval addition preserves containment. These dependencies can only make this enclosure wider.

Set \(Q_+=\max(0,Q^+)\). Because \(d\ge d_\ell/G>0\),

\[
 s\le \frac{Q_+}{G^2G_F^2d_\ell}.
\]

For a nonnegative exact quadratic, this follows by division by the lower variance. For a negative exact quadratic, the nonnegative right-hand side is already an upper bound. The clamp is therefore necessary for the component's more general indefinite-\(H\) contract, although the certificate's exact \(H\) is positive definite. The returned integer is

\[
 U=\left\lceil
 \frac{G_sQ_+}{G^2G_F^2d_\ell}
 \right\rceil,
 \qquad U/G_s\ge s.
\]

All operations after preparation are integer operations. Python integers avoid arithmetic overflow. The rational filter remains the independently reviewed `local_coefficients` function; its coefficients are computed once per distinct history pattern. `IntegerIntervalScores.prepare` also accepts exact coefficients and variance already computed by a caller. The one-time `IntegerPattern` validation requires immutable tuples, distinct positive integer ages, matching coefficient counts, ordered integer interval endpoints, and positive integer denominators. Target checks reject histories preceding the first sensitivity row and patterns prepared with different grids.

The certificate dynamic program only adds arc scores and maximizes path totals. Replacing every arc score by a valid upper score therefore preserves its upper-bound property. For a cardinality-\(k\) problem, if the new integer score exceeds the old exact-rational ceiling by at most \(e\) units on every reachable arc, the final price increase is at most \(ke/G_s\). The actual increase can be smaller because the maximum path is recomputed.

The [full comparison report](../code/research_20260912/results/integer-interval-scores-validation.json) used \(G_F=10^{18}\), \(G=10^{12}\), and \(G_s=10^8\). It reconstructed the exact weights from the saved tangent \(N\) and exact \(\delta\), enumerated all reachable arcs using the same state transitions, and evaluated every arc with both methods.

| Check or timing | Result |
|---|---:|
| Conditional history patterns | 377 |
| Reachable arcs compared exactly | 31,900 |
| Integer scores below exact-rational ceilings | 0 |
| Changed integer scores | 418 |
| Maximum increase per changed arc | 1 unit = \(10^{-8}\) |
| Original / new integer DP price | 299,934,500 / 299,934,501 |
| Actual final upper-bound increase | \(10^{-8}\) |
| Original / new displayed certificate gap | 0.011557645731135803 / 0.011557655731135803 |
| Exact conditional-pattern preparation | 0.03952 s |
| Outward integer preparation | 0.00524 s |
| Integer arc evaluation | 0.29024 s |
| Exact rational arc evaluation | 33.00551 s |
| Arc evaluation speedup | 113.7 times |

The exact-reference dynamic program reproduced the saved certificate's integer price. The maximum possible path increase from the measured per-arc excess is \(32\times10^{-8}\), while the observed increase is one score unit. These are component timings from one thread in the shared research environment, not a claim about an integrated certifier's total runtime. The reviewed certifier was not changed for this experiment.

The [verification script](../code/research_20260912/verify_integer_interval_scores.py) also checks 1,500 primitive interval assertions, 600 exact rational arc comparisons with both fine and coarse grids and symmetric indefinite weights, 24 stationary-filter histories including zero latent variance and negative correlation, and cancellation across zero. The [subsequent input-validation report](../code/research_20260912/results/integer-interval-scores-input-validation.json) adds direct malformed `IntegerPattern` construction, bringing rejected malformed cases to 34. That constructor hardening was prompted by fresh review: the initial public dataclass could accept a negative variance and denominator. The hardened source validates these invariants once. Its arc arithmetic is unchanged. The full benchmark preserves the original pre-hardening source hash; the later input report records the new hash.

The [fresh independent review report](../code/research_20260912/results/integer-interval-scores-independent-review.json) records a separate post-hardening replay. The reviewer formed all 377 conditional patterns using exact dense covariance inverses, checked all 31,900 arcs, and used a tuple-history dynamic program visiting 753,275 states. It reproduced the 418 one-unit arc changes and the final price increase of one unit. Separate checks covered 1,950 general exact arcs, including 981 negative quadratic scores; 2,025 interval products; 45 squares; 60 dense conditional comparisons; and 27 malformed-input rejections. The accepted component hash is `b558f1b03db3f195be8fd0fbab8741396dd75264ccbef2f3a65d98908a763c1d`.

Grid errors can matter if \(d\) is very small or the chosen grids poorly resolve the data. No universal claim of negligible loss is made. For fixed finite data with \(d>0\), refining \(G_F,G\) makes the interval enclosure converge to the exact quadratic when \(H\) is positive semidefinite. At fixed \(G_s\), an arc exactly on a score-grid boundary can still have one excess integer unit for every finite interval grid. Letting \(G_s\) also grow removes that final ceiling scale. The measured loss above concerns the stated instance and grids.

To reproduce the complete comparison:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/verify_integer_interval_scores.py code/research_20260912/results/integer-interval-scores-validation.json --certificate code/research_20260912/results/noisy-markov-spacing-kinetics-certificate.json
```

Omit `--certificate` to run only the small exact arithmetic and malformed-input checks. The project environment and lock file record the Python dependencies. No dependency was added for this component.
