# Phase-two benchmark protocol

This suite measures completed functionality separately from the 74 historical
phase-one runs. Its inputs, source snapshots, exact certificates, replay results,
and failures are retained. It is a diagnostic suite, not evidence of competitive
solver performance.

Each configuration runs sequentially in a fresh process with one BLAS/OpenMP
thread, a two-second cooperative solver budget, a five-second hard worker deadline,
and a 512 MiB address-space cap. Certificate checking runs in a separate
five-second worker and is separately timed. A timed-out worker does not count as a successful proof replay. Sources
are frozen before any published run; final source hashes identify the code
actually measured. The archived phase-one solver and checker form the baseline.
Decomposition, validation, solving, serialization and replay all contribute to
`total_subprocess_seconds`, which sums the solver and checker subprocess times.
Their separate peak resident memories are read from `/proc`. The table cap is
30,000 states per stage; it does not bound the sum across completed stages.
This differs from the historical phase-one 20,000-state cap, so the old runs
are not pooled with this comparison.

Small box-QP instances have independent exact references by enumeration of all
integer assignments and continuous faces. Generated random inputs use fixed new
seeds and have no planted optimizer. Analytic examples are explicitly labeled.
Moderate paths, trees, shuffled variables, expensive convex recourse, mixed integer
variables, tied optima, and refusing cases exercise separate solver contracts.
Constrained references use exact face/KKT enumeration with direct rational
feasibility checks. Numerical references, if used, are labeled numerical.

The original QPLIB binary inputs 3852 and 5881 are retained in full. Their source
objectives are checked against QPLIB's supplied feasible solutions. No public
instance is truncated or sparsified. Current QPLIB metadata was also screened
for continuous bound-only QPs: its three cases have 14,400–39,204 variables; one
has unbounded coordinates. They exceed this dense rational prototype's declared
512-variable input cap. Those are **input screening refusals, not solver runs**.
The unmodified metadata, hashes and source URLs are in `data/`.
