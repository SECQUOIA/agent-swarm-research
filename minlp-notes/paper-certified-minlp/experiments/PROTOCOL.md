# Frozen uniform-generation protocol

This file and run_uniform.py are finalized before starting the first experiment.

Population: all 289 unique historical certificate attempts, lexicographic order.
No repaired-curvature prefilter and no omission of previous failures. The prior
299-instance library selection and its ten exclusions remain separately visible.

Per instance: 30 seconds numerical OA search; 30 seconds exact SCIP search per
attempt, at most default plus conservative fallback; one requested OA/SCIP/LP
thread, six concurrent workers. SCIP gets the recorded settings file. OMP,
OpenBLAS and MKL thread environment variables are one. A 360-second process-group
cap includes loading, OA, master construction, both attempts, proof completion,
and all in-generation checks; any unfinished instance is a hard timeout and is
not retried. Partial files are retained. Tool/phase start/end events and tool
outputs are logged. The observers time function calls without altering proof
arithmetic. Each completed proof must later pass a separate frozen complete
replay with a 1,200-second per-record cap. That replay includes all 289 names,
including any complete files surviving a timed-out generation; production and
replay outcomes are reported separately.

The selected budgets assess usable coverage under one modest uniform protocol;
they are not a tuning study, dominance claim, or speed comparison with solvers.
All attempted names stay in denominators. Record exact signed normalized
reference differences, negative reference discrepancies separately, accepted
proof bytes, production phases, independent checking cost, and failure classes.
A verified bound near a library value is not labeled an optimality gap.

The machine-readable protocol.json freezes code, model, input, tools, environment,
hardware and settings before launching workers. Any implementation change or
retry requires a new separately named campaign and an explicit explanation.
