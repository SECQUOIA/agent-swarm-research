# Exact certificates for noisy-Markov measurement selection

Date: 12 September 2026. Status: exact implementation has passed fresh
independent checks; broader computational comparison and publication priority
remain unresolved. The
[approximation theorem](research-20260912-noisy-markov-memory.md) and
[independent theory review](research-20260912-noisy-markov-independent-review.md)
state the scalar and fully observed block assumptions. This implementation
currently covers stationary scalar latent AR(1) noise plus independent scalar
measurement noise.

## What is certified

The problem is to select exactly `k` of `n` observations and maximize the
log determinant of the mean-parameter Fisher information plus a fixed positive
definite prior. All covariance parameters and sensitivities are fixed data.
The certificate concerns this encoded local design problem, not uncertainty
in fitted sensitivities or covariance parameters.

`code/research_20260912/certify_noisy_markov.py` treats JSON decimal data as
exact rational numbers. It recomputes a true selected-information matrix for
the supplied feasible incumbent. For the upper bound, it uses the reviewed
calendar-window information approximation and its uniform relative error
`delta<1`. If `A_L(S)` denotes the surrogate information contribution without
the prior, the theorem implies

```text
J_true(S) <= J0 + A_L(S)/(1-delta).
```

For any rational SPD reference `N`, concavity of log determinant gives

```text
logdet J_true(S)
  <= logdet N - p + tr(N^-1 J0)
     + sum_(arcs of S) tr(N^-1 W_arc)/(1-delta).
```

The reference need not be a feasible design or an optimum. Consequently the
numerical optimizer is only a producer of useful reference matrices and
candidate selections. Its convergence status, computed gradients and reported
upper bound are not trusted by this certificate.

## Exact computation

1. A rational scalar Kalman recursion gives each genuinely local conditional
   regression and variance. Applying these regressions to the mean sensitivities
   yields each PSD arc information matrix. Patterns are cached by calendar ages.
2. A full-calendar rational Kalman sweep supplies `d_star`, a lower bound on
   every local innovation variance. The reviewed gain bound uses `d_star` for
   residual normalization while retaining the original measurement-noise
   variance in the Kalman-gain cap.
3. The numerical reference is symmetrized and rounded to a rational grid.
   Exact leading principal minors check that it is SPD. A rational inverse
   gives every arc's tangent score.
4. Scores are rounded **upward** to a fixed integer grid. An integer
   calendar-mask/count dynamic program maximizes their sum over all feasible
   size-`k` selections. Upward rounding preserves the upper bound.
5. Rational logarithm enclosures use binary range reduction and a positive
   `atanh` series with an explicit remainder. The upper endpoint is used for
   the tangent constant; the lower endpoint is used for the true incumbent.

Only the displayed decimals are floating approximations. The bounds, gap,
input problem, reference matrix and price are saved exactly in the output.
The standard library supplies rational and integer arithmetic; SymPy 1.14.0
supplies small exact matrix operations, with the environment recorded in
`code/research_20260912/uv.lock`.

The [independent exact review](research-20260912-noisy-exact-independent-review.md)
uses dense rational covariance inverses, an independent logarithm enclosure,
and a separate history-state pricing method. Its initial checks passed 244
tiny certificates, 816 exhaustive subset bounds, and reconstruction of the
48-candidate certificate. The final review records exact coverage and source
hashes; journal peer review and a formal proof assistant are separate matters.

## Initial achieved bounds

All rows below use three parameters, correlation `0.4`, equal latent/noise
variance one, a synthetic sensitivity table, and `k=n/3`. The JSON files retain
the exact problem data. These are achieved global gaps for these inputs, not
an assertion that the selected designs are exact optimizers.

| Candidates | Window | Certified logdet gap | Certificate generation |
|---:|---:|---:|---:|
| 12 | 6 | 0.0409996 | 0.020 s |
| 24 | 6 | 0.0112222 | 0.080 s |
| 48 | 6 | 0.0122778 | 0.21 s |
| 48 | 8 | 0.00270073 | 0.90 s |

Times exclude the numerical hull solve. The 48-candidate/window-8 hull solve
took about 0.58 seconds in the first run. The smaller gap with window eight
costs more calendar states; this tradeoff can become prohibitive for strong
correlation. A strengthened dense comparator solves the two smaller cases
quickly and leaves a numerical gap around `0.0246` in its five-second
48-candidate run. That comparison uses a disclosed hull-generated incumbent
as its MIP start. These initial rows do not establish general solver
superiority.

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_noisy_markov.py code/research_20260912/results/noisy-markov-design-benchmark.json code/research_20260912/results/noisy-markov-exact-certificate-n48.json --case 2
```

The window-eight input and certificate are
`code/research_20260912/results/noisy-markov-l8-probe.json` and
`code/research_20260912/results/noisy-markov-exact-certificate-n48-l8.json`.
For that input, omit `--case 2`. Certificate files include their own exact
problem data, since a benchmark file can later be regenerated with new timing
metadata. A numerical input hash alone is not the certificate's only link to
the original problem.

## Six-case extension

The checkpointed extension uses the same covariance, prior, parameter count
and selection fraction as above, with independent sensitivity seeds 0, 1 and
2 at each of 48 and 96 candidates. All window-eight numerical hull runs
closed their continuous optimization tolerance. This is distinct from closing
the true discrete design gap. Each row below has a separately recomputed exact
certificate for its selected design.

| Candidates | Seed | Hull time | Exact certified gap | Certificate time | Dense OA reported gap at 5 s |
|---:|---:|---:|---:|---:|---:|
| 48 | 0 | 0.617 s | 0.00270073 | 1.000 s | 0.0246235 |
| 48 | 1 | 0.687 s | 0.00187230 | 0.872 s | 0.0180066 |
| 48 | 2 | 0.701 s | 0.00387283 | 0.989 s | 0.0256485 |
| 96 | 0 | 2.639 s | 0.00183482 | 2.336 s | 0.0341211 |
| 96 | 1 | 2.439 s | 0.00186234 | 2.444 s | 0.0184600 |
| 96 | 2 | 1.721 s | 0.00178161 | 2.446 s | 0.0235668 |

The displayed certified gaps are rounded upward. Certificate times exclude
hull construction and optimization. These six certificates ran concurrently
with one BLAS thread per process; the numerical benchmark used one solver
thread and one BLAS thread per invocation. The six numerical dense runs each
reached their five-second cap. Their starts were the best same-case hull
incumbents, whose generation time was excluded from the dense cap and is
reported separately. The dense bound columns are floating-point solver bounds;
the exact certificate columns certify the JSON decimal problem.

The input is `code/research_20260912/results/noisy-markov-extended-benchmark.json`.
Certificates are `noisy-markov-extended-certificate-0.json` through
`noisy-markov-extended-certificate-5.json` in that results directory, in table
order. The [implementation note](research-20260912-noisy-markov-design-implementation.md)
records configurations, source hashes and reuse of exactly matching earlier
runs. For example, reproduce the last certificate with:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_noisy_markov.py code/research_20260912/results/noisy-markov-extended-benchmark.json code/research_20260912/results/noisy-markov-extended-certificate-5.json --case 5
```

These random-sensitivity cases establish a limited achieved capability. They
do not establish an advantage for chemical process design, high correlation,
or larger parameter counts. A [structured dense oracle](research-20260912-structured-dense-oracle.md)
uses classical banded algebra to remove avoidable dense evaluation cost;
its [fresh review](research-20260912-structured-oracle-independent-review.md)
and [exact continuous-relaxation comparison](research-20260912-exact-dense-design-certificates.md)
are complete. The latter establishes a strict separation between a feasible
continuous value and the memory upper bound, independently of solve time.

## Research priority and later completed comparisons

Vecchia conditionals, sparse approximate inverse factors, finite-memory sensor
scheduling, logdet tangents, dynamic programming, and rational logarithm bounds
are established. The candidate contribution is their use with an explicit
subset-uniform relative Fisher bound to produce a practical, independently
checkable design-optimization certificate. No matching combined result has yet
been found in the inspected sources. Unretrieved and unread factorization or
sensor-scheduling works are listed in the
[literature report index](research-20260912-literature-report-index.md).
That is an unresolved priority question, not evidence of novelty.

The [all-splits comparison](research-20260912-all-splits-separation.md) has passed
fresh independent review for every scalar virtual-noise split on these inputs.
Four [chemical-kinetics cases](research-20260912-noisy-markov-kinetics-probe.md)
also have exact gaps below `0.001943`, with separately verified model
sensitivities. The subsequent
[all-diagonal split comparison](research-20260912-diagonal-split-separation.md)
passed [fresh review](research-20260912-diagonal-split-independent-review.md).
The [fixed-physical-grid benchmark](research-20260912-fixed-physical-grid-benchmark.md)
also records the current calendar implementation's scaling limitation under
grid refinement. These results establish particular bound improvements and
limits, not a ranking of complete mixed-integer solvers.
