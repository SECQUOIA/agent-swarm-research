Independent implementation review of the latent-separator prototype, 2026-09-12.

The repaired implementation and all 13 saved numerical probes pass this review.
The initial source hash was
`ba2d1e2178e0d34b0d67cd5a6b7265ec30f2f4f33f58213e9d65f6794ff28213`.
The final reviewed repair has hash
`6366451ad20c815b6a66675a6eb9be8f7bad34b9db95b469af2c9fc67210184c`.
The saved probes retain the initial hash because they predate the repair. Their
stored numerical witnesses were reconstructed independently; their timings were
not rerun or endorsed. This review provides implementation confidence in addition
to the separate [theory review](research-20260912-latent-separator-independent-review.md).
It does not certify the floating-point bounds by exact arithmetic.

The reviewer found and reported two related error-handling defects. On the valid
input `F=ones((4,2))`, `rho=.8`, latent variance `1`, nugget variance `1e-16`,
prior `.01 I`, `k=2`, and block size `1`, cancellation in the augmented Schur
complement caused a Cholesky failure. The main loop caught the error, but
finalization recomputed the same Schur complement outside its exception handler
and raised again. The author guarded finalization and made a numerical linear
algebra failure fall back to the dense full-selection upper value. The independent
regression now returns `numerical_linear_algebra_failure`, retains the dense
incumbent `-3.628536228873067`, returns the dense upper value
`-3.620597946697548`, and leaves the unavailable hull value and hull gap null.
The saved mixture remains diagnostic data. The second defect was a computed
tangent that the consistency check correctly rejected, but that still appeared
in the returned upper-bound field. The final repair sends both numerical failure
statuses through the same cleanup: retain the dense marginal endpoints, null the
unreliable hull information and objective, and clear the tangent witness. Both
regressions passed. The producer was not edited by this reviewer.

The independent script is
[review_latent_separator_implementation.py](../code/research_20260912/review_latent_separator_implementation.py).
Its saved report is
[latent-separator-independent-implementation-checks.json](../code/research_20260912/results/latent-separator-independent-implementation-checks.json).
It imports the producer only to call the routines under review. Reference
conditional means and covariances come from dense conditioning on the entire
anchor vector. Reference selected information comes directly from the original
dense selected covariance. A full augmented inverse and a determinant ratio
provide independent Schur and gradient comparisons. Saved support prices use a
separate exhaustive subset recursion based on dense Gaussian conditioning, then
a separate cardinality convolution; they do not use producer pattern matrices.

All assertions passed with `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`.
The checks cover:

- 68 configurations with `n=1,2,4,7`, negative correlation, zero correlation,
  positive correlation up to `.98`, zero latent variance, non-diagonal SPD priors,
  singleton blocks, unequal final blocks, and requested blocks larger than `n`.
- 2,968 all-subset augmented-matrix and original-information comparisons,
  including empty selections, full selections, unselected blocks, and selected
  anchor endpoints. The largest original-information entry error was
  `4.18e-14`. Anchor observations belong to exactly their ending block and have
  residual variance equal to the nugget.
- 68 dense gradient comparisons and 68 finite differences in general symmetric
  directions. The largest gradient entry error was `8.89e-16`; the largest
  finite-difference error was `1.20e-9`.
- 996 exhaustive cardinality support comparisons and schedule/mask
  reconstructions, using the PSD objective gradient, arbitrary signed symmetric
  prices, and all-zero prices. Every cardinality from zero through `n` is tested.
  The largest price error was `9.60e-14`. Another 332 checks compare the tangent
  upper value with the exhaustive discrete optimum.
- 28 end-to-end solves compared with exhaustive discrete optima and independent
  reconstruction of every returned feasible mixture. The tests distinguish a
  feasible selected schedule from a convex mixture.
- Memory preflight rejection; setup timeout with a retained dense incumbent;
  interruption during a later pricing round with the previous complete bound
  preserved; stalled correction with a retained bound; correction failure and
  timeout after a feasible improvement; and the repaired numerical-failure
  fallback above, together with dense fallback after a finite but inconsistent
  tangent.

All 13 saved probes passed independent reconstruction of the dense incumbent,
dense full-selection upper value, mixture matrix and objective, witness Schur
information and nuisance minimizer, fixed prior contribution, complete cardinality
support maximum, priced mask selection, final upper value, and both reported
gaps. Across these probes, the script enumerated 1,293,632 local patterns and
reconstructed 381 mixture support entries. It also compared 896 representative
recursive pattern scores against direct selected covariance solves. The largest
reconstructed upper-value error was `1.25e-14`; the largest hull-objective error
was `1.27e-13`.

| Candidates | Block size | Feasible lower value | Numerical upper value | True-objective gap |
|---:|---:|---:|---:|---:|
| 48 | 4 | 14.866090380 | 15.096634752 | 0.230544372 |
| 48 | 6 | 14.904405743 | 15.030050657 | 0.125644914 |
| 48 | 8 | 14.925507607 | 15.005243601 | 0.079735994 |
| 96 | 4 | 14.856451769 | 15.247510979 | 0.391059210 |
| 96 | 6 | 14.842137067 | 15.134837344 | 0.292700278 |
| 96 | 8 | 14.887809405 | 15.109085513 | 0.221276108 |
| 96 | 12 | 14.904798197 | 15.051419291 | 0.146621094 |
| 96 | 16 | 14.916594941 | 15.025970610 | 0.109375669 |
| 192 | 4 | 14.799649310 | 15.406524064 | 0.606874753 |
| 192 | 6 | 14.840010348 | 15.321797066 | 0.481786718 |
| 192 | 8 | 14.831374036 | 15.247511547 | 0.416137511 |
| 192 | 12 | 14.837091229 | 15.139311161 | 0.302219932 |
| 192 | 16 | 14.886781445 | 15.110331264 | 0.223549819 |

The saved hull gaps range from `4.30e-7` to `2.11e-6`. Three runs have
`hull_optimal_tolerance`; ten have `correction_stalled`. None proves a discrete
optimum. In particular, nearly closing the mixture problem does not close the
remaining true-objective gap. Larger nonnested block partitions also need not
obey a general mathematical monotonicity claim.

The resource controls need their stated scope. The deadline is cooperative:
the timer starts before seed evaluation and setup, but an individual dense solve,
pattern batch, correction evaluation, and finalization cannot be preempted.
Very short requested limits can therefore be exceeded. The memory limit rejects
an estimated workspace before the large pattern allocation; it is not a process
RSS ceiling. Setup timeout now records elapsed setup time. These numerical
prototypes should not be described as hard real-time or process-memory bounded.

Very small nugget variance and correlation extremely close to unit magnitude can
make floating-point Schur elimination unreliable even though the mathematical
model is SPD. The repaired failure is handled, but the repair does not make such
algebra reliable. An additional spot check with `rho=nextafter(1,0)`, latent
variance `1`, nugget `1e-8`, `F=ones((4,1))`, prior `1e-8 I`, `k=2`, and block size
`1` originally returned `numerical_bound_inconsistency` with a negative reported
gap near `-0.992`. In the repaired code it retains that failure status, returns
the dense incumbent `4.9999999633626455e-9` and full-selection upper value
`7.500000162401072e-9`, and clears the hull value, hull gap, Schur information,
and tangent witness. This is a checked fallback, not a reliable augmented
calculation for that example. The consistency check does not constitute an
outward-rounding guarantee on runs that pass it. Exact certification remains
separate, and no inconsistency was found in the 13 saved probe witnesses.

Reproduce the independent numerical review from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  code/research_20260912/.venv/bin/python \
  code/research_20260912/review_latent_separator_implementation.py
```
