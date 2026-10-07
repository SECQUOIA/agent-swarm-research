# Findings from the bounded prototype benchmark

The prototype produces replayable rational bounds on the tested small and
moderate sparse problems. Pruning reduces table work on the curvature
diagnostics. Exact removal of certified affine convex recourse avoids the
stiffness penalty on a deliberately constructed family. The implementation
does not establish general computational superiority: the 256-variable
path misses its target within the assigned resources, and neither full
QPLIB instance reaches even one DP stage with the supplied decomposition.

These findings use the final saved runs in `results/` and
`extension-results/`, completed on 2026-10-02. The initial preliminary run
was replaced after the solver's iterable-input fix and improvements to
provenance and SCIP incumbent recording. All reported numbers below are
from the final runs. Source snapshots and hashes record their exact code.

## Coverage and validation

The main suite contains 60 runs: 15 case/accuracy configurations and four
methods. Thirteen configurations have independently enumerated exact
rational optima; two are full binary QPLIB instances. The extension suite
adds 14 runs covering increasing dimension and affine recourse.

All **56 rational certificates** across the two final suites passed the
separately implemented checker. This includes certificates returned after
resource limits. All **39 small-case bound intervals** in the main suite
enclose the independent exact optimum. The four affine runs also enclose
their known zero optimum. No exhaustive-reference claim is made for the
larger random paths or library problems.

| Main-suite method | Small configurations meeting tolerance | Library configurations meeting tolerance |
| --- | ---: | ---: |
| Geometric, pruned | 13 / 13 | 0 / 2 |
| Geometric, unpruned | 13 / 13 | 0 / 2 |
| Uniform, unpruned | 11 / 13 | 0 / 2 |
| SCIP, numerical bounds | 13 / 13 | 0 / 2 |

SCIP used version 10.0.2 through PySCIPOpt 6.2.1. Its recorded lower and
upper bounds are floating-point quantities. The supplied scripts also save
a repaired rational feasible point and its exactly recomputed objective;
that operation does not turn the numerical dual bound into a certificate.
The small numerical bound intervals contain the reference values to a
`1e-6` checking tolerance. This is a diagnostic, not a replacement for
exact verification.

The final suites took 20.23 and 22.23 seconds of summed subprocess wall
time. Each solver was limited to two seconds, each exact DP stage to
20,000 aggregate table states, and each worker to 14 seconds including
construction and certificate replay. All runs were sequential with one
solver/BLAS thread. No worker crashed or hit the outer wall limit. Solver
limits are cooperative, so a small overrun at a budget check is possible.

## Curvature and pruning

The two four-variable near-convex cases have numerical smallest
eigenvalues about `-0.01133` and `-0.01001`. Their largest positive
diagonal entries are exactly 2 and 512. Thus the large change is in the
positive curvature. These statistics do not establish growth constants.

For the larger positive-curvature case at absolute tolerance `1/1000`:

| Method | Status | Cumulative completed states | Largest completed stage | Solve seconds | Replay seconds | Final gap |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Geometric, pruned | Certified | 771 | 128 | 0.0182 | 0.0254 | 0.000611 |
| Geometric, unpruned | Certified | 13,527 | 4,278 | 0.2428 | 0.2972 | 0.000611 |
| Uniform, unpruned | Table limit | 12,417 | 8,910 | 0.2198 | 0.2345 | 0.185203 |
| SCIP | Numerical gap limit | — | — | 0.0127 | — | 0.000725 |

The next uniform stage exceeds the aggregate table cap; the largest
*completed* stage is therefore below 20,000. Geometric spacing and pruning
each save work in this diagnostic. The numerical SCIP solve is faster
than the exact solve plus replay here. The experiment supports retaining
pruning as an implementation component, not a general speed ranking.

## Dimension and width

The additional random paths use the same unplanted generator and fixed
coefficient distributions at `n=16,64,256`, with tolerance `1/50`. Their
supplied decompositions have width one. The width-two check uses 16
variables. Only exact grid outputs have replay times.

| Instance | Method | Status | Gap | Solve seconds | Replay seconds | Peak process MiB |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Path 16 | Pruned | Certified | 0.01497 | 0.0253 | 0.0231 | 24.3 |
| Path 16 | Unpruned | Certified | 0.01497 | 0.0272 | 0.0325 | 24.3 |
| Path 16 | SCIP | Numerical optimum | 0 | 0.2228 | — | 60.0 |
| Path 64 | Pruned | Certified | 0.01361 | 0.2020 | 0.1967 | 24.8 |
| Path 64 | Unpruned | Certified | 0.01361 | 0.2745 | 0.2338 | 25.7 |
| Path 64 | SCIP | Numerical gap limit | 0.000099 | 0.7371 | — | 65.8 |
| Path 256 | Pruned | Time limit | 0.05786 | 2.0023 | 1.2388 | 46.5 |
| Path 256 | Unpruned | Table limit | 0.05786 | 2.0079 | 1.7897 | 49.0 |
| Path 256 | SCIP | Numerical gap limit | 0.000612 | 1.7965 | — | 84.4 |
| Width two, 16 | Pruned | Certified | 0.01953 | 0.0318 | 0.0546 | 24.3 |

Pruned cumulative table work grows from 585 to 5,644 to 29,225 completed
states across the three paths. The 256-variable pruned run completes a
largest stage of 8,584 states; its failure is elapsed time, not width.
The unpruned 256-variable run completes 38,317 states in total and hits
the next stage's table cap. Preprocessing the supplied decompositions
takes about `0.0002`, `0.0005`, and `0.0094` seconds in the pruned runs.
Validation, construction, serialization, and process startup are recorded
separately from solve and replay; process peaks include them all.

These are three instances, not a complexity estimate or a statistically
representative scaling study. In particular, fixed width does not imply
that the Python rational implementation is fast at every dimension.

## Certified affine recourse

The additional comparison uses equation (17) of
[the affine-recourse result](../../negative-curvature/affine-convex-recourse.md)
with `m=2`. It compares the original six-variable model at stiffness
`M=1,100,1000` with the identical four-variable reduced core. All use
the same pruned algorithm, tolerance `1/1000`, time limit, and table cap.
The core is solved once because it is exactly the same rational problem
at all three stiffness values.

| Representation | Status | Cumulative states | Solve seconds | Replay seconds | Certified gap |
| --- | --- | ---: | ---: | ---: | ---: |
| Original, M=1 | Certified | 1,694 | 0.0352 | 0.0425 | 0.000458 |
| Original, M=100 | Time limit | 64,564 | 2.0044 | 2.0668 | 0.399817 |
| Original, M=1000 | Time limit | 76,986 | 2.0033 | 2.5630 | 7.406978 |
| Reduced core, all M | Certified | 394 | 0.0121 | 0.0151 | 0.000519 |

The script checks the coefficient identity
`F(u,v,y)=q(u,v)+M*sum_i(y_i-u_i)^2` exactly. The response `y=u` is
feasible on the full core box. Thus the reduced lower bound is valid for
each original model, and the reduced incumbent lifts to a feasible original
point with exactly the same objective. The saved lift records contain the
rational point and transferred interval. Its upper bound is exactly
`2/2862423051509815793`, and its gap is about `0.000519` for every M.

This demonstrates the implemented value of a certified preprocessing
step on its stated class. It is a designed family with a simple analytic
zero-optimum proof. No claim is made that the unreduced models are hard
for other solvers, or that general convex recourse has one globally valid
affine response. The scoped affine-selector recognition and changing-active
convex-value-factor theorems are separate theoretical results; their
recognition and recourse algorithms are not implemented or benchmarked here.

## Full library instances and practical limits

The greedy minimum-degree decompositions for QPLIB_3852 and QPLIB_5881
have width 25 and 95. Every grid variant refuses its first table under
the cap. Their exact fallback intervals are `[-652,-198]` and
`[-57353,-12515]` after converting to minimization, with gaps 454 and
44,838. These are valid but weak bounds. Replay of the pruned fallback
certificates takes 0.151 and 0.064 seconds.

SCIP reaches its two-second numerical limit on both, with gaps about
89.67 and 20,529.5. None of these runs reaches tolerance. The recorded
decompositions are heuristic upper bounds on treewidth; their failure is
not a lower-bound proof on what a different decomposition could achieve.
The library results rule out describing the current prototype as a
generally competitive binary-QP solver.

Certificate replay can take as long as, or longer than, solving. Process
memory includes Python or SCIP libraries, tables, construction, and replay.
It is not directly comparable to a solver's internal allocated-memory
counter. Timing comes from one run on a shared machine. Wider workloads,
optimized message storage, and systematic decomposition selection would
be needed before making deployment or broad performance claims.

## Targeted commands actually run

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python research-20261002-decomposition/solver/extra-benchmarks/run_benchmarks.py --run

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python research-20261002-decomposition/solver/extra-benchmarks/run_extensions.py --run

python -m py_compile \
  research-20261002-decomposition/solver/extra-benchmarks/corpus.py \
  research-20261002-decomposition/solver/extra-benchmarks/run_benchmarks.py \
  research-20261002-decomposition/solver/extra-benchmarks/run_extensions.py
```

The first command was rerun once after the API/provenance changes; the
saved final outputs replace the preliminary run. The second command ran
once. Before the sweeps, targeted corpus checks validated all supplied
decompositions and exact reference witnesses; a one-case SCIP smoke check
validated the numerical comparison path. An independent review rechecked
the exact oracle, parsing convention, and decomposition invariants. A final
artifact audit checked run counts, saved incumbent witnesses, certificate
file presence, and agreement of archived source hashes. No
project-wide verification or CI inspection was performed.
