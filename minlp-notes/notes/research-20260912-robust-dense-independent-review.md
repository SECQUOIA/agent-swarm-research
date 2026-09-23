# Independent review of the robust dense comparison

Date: 2026-09-12. The [comparison driver](../code/research_20260912/robust_dense_comparison.py),
its two application artifacts, and its validation artifact pass this bounded
independent review. No correctness defect was found in the stated comparison.
The [checker](../code/research_20260912/review_robust_dense_comparison.py) and
[machine-readable results](../code/research_20260912/results/robust-dense-independent-review.json)
record the reconstruction, exhaustive neighborhoods, stop tests, and hashes.
The production source and supplied artifacts were not modified.

Reviewed comparison source SHA-256:
`b458885e5c848086e181928d3f454469222e1598e5cffc2e677c9ab961201fb3`.
The separate [polished-certificate wrapper](../code/research_20260912/certify_robust_polish.py)
was also reviewed, at SHA-256
`2cd3bc70f88351c63c8a641375295d890f79e496a55e285b498eb2206aa83ed4`.
Literature priority is outside this review.

The dense epigraph uses one common vector `z`, the exact cardinality equality,
and one constraint `t <= f_s(z)` per scenario. Priors, offsets, sensitivities,
and covariance parameters come directly from the saved inputs. Each fixed
split is `a_s = 0.99 lambda_min(R_s)`, so `S_s = R_s-a_s I` is positive
definite. The Liu information is concave and monotone in visits; composition
with the monotone concave log determinant gives the required scenario
tangents. At a binary vector it equals the information under the selected
original covariance, including the unscaled prior.

For simplex scenario weights, the minimum scenario score is bounded above by
their weighted mean. Applying the concave tangents and maximizing the
resulting linear form over `0 <= z <= 1, sum(z)=k` gives exactly the sum of
the largest `k` weighted gradient entries plus the weighted intercept. The
scenario-weight LP has the correct inequality direction and free threshold.
Clipping and normalizing its proposed weights followed by a fresh top-`k`
calculation yields a valid numerical bound independently of its solver
status. The fallback full-observation score is also an upper bound by
monotonicity. Neither an SLSQP convergence flag nor a reported LP objective is
used as the certificate.

The independent evaluator solves the symmetric covariance
`R_AA + diag(a*(1/z_A-1))` on positive visits `A`. It reconstructs information,
values, and gradients without calling the production Liu evaluator. All saved
tangent witnesses in the two application files and validation file agree:
the largest value discrepancy is `7.25e-13`, gradient discrepancy `3.02e-14`,
and upper-bound discrepancy `4.23e-13`. Separate primal epigraph LPs verify
weak duality for the saved witnesses and additional test weights.

The saved continuous visit sums differ from `k` by at most `7.11e-15`.
The positive continuous feasible values are lower bounds for the continuous
problem, not feasible discrete schedule scores. Recomputing all returned
schedules, rounded schedules, reference scores, standardization intervals,
and efficiency conversions confirms the artifact labels and the note's
numbers. The individual-reference discrete upper caps are
`0.003468825446011792` and `0.003596996485963899`. Both are stronger than the
dense continuous upper bounds, while both negative shared-path upper bounds
are stronger still. Zero is the reference-only upper bound when subtracting
the unknown exact individual optima. These distinctions are stated correctly
in the comparison note.

Every final exchange neighborhood was evaluated independently under all three
original scenario covariances:

| Case and branch | Final score | Neighbors checked | Best neighbor minus final score |
|---|---:|---:|---:|
| 48, hull polishing | -0.089793800214 | 512 | -0.001416100858 |
| 48, dense rounding polishing | -0.117397574224 | 512 | -0.000395331172 |
| 96, hull polishing | -0.084071764958 | 2,048 | -0.000092861165 |
| 96, dense rounding polishing | -0.089678325685 | 2,048 | -0.000438273102 |

All four local-optimum claims therefore hold with margins well above the
implementation's `1e-11` improvement threshold. Recorded objective counts
equal `1+(accepted_exchanges+1)k(n-k)`, as required by completed neighborhood
passes. The hull branch starts from the original hull selection; the dense
branch starts from its own rounded fractional vector. A supplied shared
incumbent affects only the dense method's reported discrete lower bound.
A separate test with different supplied incumbents obtains identical
fractional visits and rounding.

The tiny reconstruction enumerates all 120 schedules, checks 360 individual
scenario tangent inequalities, and checks its final 21 exchange neighbors.
Twelve independent directional derivatives agree within `3.67e-11`. Additional
checks cover continuous tangent inequalities, extreme finite weights,
identical scalar scenarios with optimum `log(5)`, distinct priors, negative
correlation, and cardinalities zero, one, and all candidates. These tests add
contracts absent from the two application instances.

Forced interruptions confirm that polishing retains an improving neighbor
even when its pass is unfinished, without claiming local optimality. Dense
interruptions retain the disclosed feasible incumbent and either a completed
tangent or the full-observation fallback. Stopped LPs with no solution or
inexact weights still produce a recomputed support witness. Invalid time caps
are rejected, and the dense memory preflight precedes oracle allocation.
The 30-second limits are soft checks around numerical work, not hard process
deadlines; the note discloses this. Source/input hashes and one-thread metadata
match. Every recorded pipeline sum recomputes exactly, including the cost of
generating the shared incumbent and the independent dense rounding pipeline.
This verifies accounting, not statistical runtime superiority.

The new [96-candidate exact certificate](../code/research_20260912/results/robust-kinetic-n96-polished-certificate.json)
also passes the narrow extension review. Its selected schedule matches the
completed hull-polishing output. Its scenario data, reference certificates,
centers, weights, integer price, priced path, and upper bounds are exactly the
same as the previously independently reviewed certificate, apart from timing
metadata. The checker verifies that baseline artifact's accepted hash. It
then independently forms all three rational dense selected-information
matrices and uses the previous independent logarithm-series checker to
enclose their determinants inside the new saved log intervals. It checks the
lower-bound and gap arithmetic exactly and replays the wrapper into a
temporary output, obtaining identical non-timing content.

The exact fixed-offset interval is
`[-0.084071764959, -0.074519785109]`, with gap `0.009551979850`.
The exact standardized interval is
`[-0.086007784227, -0.074519785108]`, with gap `0.011487999119`.
The standardized lower bound implies worst D-efficiency at least
`exp(-0.086007784227/3)`, approximately **97.173780%**. The rational log
interval is certified; this decimal exponential is a display value. Exact
recomputation applies to the JSON decimal model. It does not certify the
underlying kinetic approximation or continuous parameter uncertainty.

The wrapper imports the reviewed certifier and substitutes only the selected
schedule. Thus it does not inherit a floating objective value as an exact
bound. Its description of a completed hull schedule is verified here from
the actual comparison status and independently checked neighborhood; the
exact certifier itself proves feasibility and score bounds, not local
optimality.

The dense bounds remain floating-point numerical results. Their small
continuous gaps establish that these two scalar-split relaxations are loose
relative to the shared-path upper bounds on the supplied cases. This review
does not establish a discrete global optimum, superiority across instances,
or a claim about other dense formulations or rounding methods.

Reproduce from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
code/research_20260912/.venv/bin/python \
code/research_20260912/review_robust_dense_comparison.py
```
