# Stopped BP certificate experiment

Date: 2026-10-02. Status: **stopped at the user's request; incomplete**.
No continuation, replacement run, or new research direction was started.

## What was stopped

The command `python3 certify_closure_point.py wcorner_BP BP`, running from
`orbit-closure/code/` as PID 244853, was terminated with `SIGTERM` after its
arguments, working directory, and log destination were checked. Its exit was
confirmed by 18:39:50 UTC (14:39:50 EDT). A subsequent process scan found no
process with the same script and instance/family arguments. This is a check
of this experiment, not a claim about unrelated repository jobs.

The earlier research stop had missed this separate background process.
The [retained log](logs/closure_cert_wcorner_BP.log) was preserved. No search
or verifier code was changed.

The [producer](code/certify_closure_point.py) attempts a sufficient certificate
for closure membership of `lam_hat = (6,6,0,0)` in the BP point-rule family
at the bilinear corner `sbar = (1,-1,1)`, with rays
`e_x, -e_y, e_w, -e_w`. The point-rule parameters are trace-one symmetric
matrices

```
S(u) = [[(1+u1)/2, u2/2], [u2/2, (1-u1)/2]],  u1^2 + u2^2 < 1.
```

The search subdivides two triangles covering `[-1,1]^2`. For each triangle
that meets the open unit disk, it tries to cover the relevant cut-vector
simplex with rational matrix certificates valid throughout that triangle.
A completed, checked cover would address this particular instance and
family. This interrupted run does not establish that conclusion.

## Retained evidence and lost state

The final log has 25,362 lines and 2,688,476 bytes. It contains:

- 430 messages reporting successfully certified outer triangles;
- 24,931 messages reporting exhaustion of the local 80-SDP budget;
- no final `ALL PASS`, `FAILED`, certificate-written message, or traceback.

These are counts of log messages, not independently verified certificates
or a percentage of completed work. The last log modification was
2026-10-02 18:39:26.431848 UTC. Its SHA-256 is
`a67b695e54082db436f33f1c728ce382ff2260c9b5dabd30a11d98324ba0aa41`.

The expected output `logs/closure_cert_wcorner_BP_BP.json` does not exist.
The producer writes it only after `run()` returns. It has no checkpoint,
resume path, or handler that saves state on interruption. Termination lost
the accepted rational witness matrices and pending queue held in memory.
The log records triangle coordinates and counts, but not those witnesses;
it cannot serve as a certificate or a resumable checkpoint.

## Why the run did not finish within a known budget

`run_BP` passes `max_sdp=80` to each inner `cover` call. Exhausting that
budget normally causes another outer triangle subdivision and a fresh
inner search. Partial inner certificates from exhausted calls are discarded.
There is no overall elapsed-time, triangle-count, or SDP-count limit.

A local refinement cutoff does exist: the maximum of three selected
coordinate differences must be less than `2^-12`. This is not an exact
triangle diameter test. At the cutoff, failure records an unresolved block
with `ok=False`; the program continues processing the other queued blocks.
Thus the code has a geometric stopping rule, but no practical runtime
guarantee or useful completion estimate. Even draining the queue could
produce an incomplete result rather than a successful certificate.

Exhaustion only means this search did not find a sufficient certificate
within its local budget. It does not prove infeasibility, nonmembership,
impossibility of certification, or a mathematical counterexample. The log
does not distinguish inadequate local work from numerical failure,
rounding failure, lack of a strict search margin, or insufficient certificate
conditions. The numerical search imposes positive margins stronger than
some conditions accepted by the exact checker; completeness of that search
has not been established.

## Remaining work, only if this experiment is explicitly resumed

1. **Make partial work durable and bounded.** Save accepted rational
   witnesses, pending regions, instance data, and run settings in atomic
   checkpoints. Support restart and a global time/work budget that returns
   an explicit incomplete status. Record solver outcomes and pending work.
   A hard wall-clock limit also needs bounded individual solver calls.
   Editing the script would not have retrofitted these features into the
   terminated process; its lost witnesses must be recomputed.
2. **Diagnose representative unresolved regions before a long rerun.**
   Separate solver failure, nonpositive numerical margins, exact rounding
   rejection, and budget exhaustion. Check whether a larger local budget
   actually helps. Audit the coordinate-based refinement guard before using
   it as a geometric accuracy criterion. Further subdivision alone has no
   established success guarantee.
3. **Implement independent BP verification.** The existing
   [verifier](code/verify_closure_cert.py) expects `sector` blocks, whereas BP
   emits `triangle`, `skip`, and `ok` blocks. BP verification must check the
   complete outer subdivision cover, exact justification of disk-exclusion
   skips, and each inner simplex cover. It must check the rational PSD and
   positive-trace conditions using `sym(R)`, the point-rule `N_E`
   inequalities at parameter-triangle vertices, and the permitted nonzero
   multipliers on positive `e_w` rays whose cut coefficient is zero. The
   current blanket rule `Y_j=0` when `lam_j=0` does not support that last
   case. Reject unsupported families, unresolved blocks, missing coverage,
   and corrupted witnesses; return a nonzero exit status on verification
   failure. Include targeted rejection tests, not just successful examples.
4. **Close the mathematical claim only after full coverage and review.**
   Check the BP certificate argument and its assumptions independently,
   as well as the serialized arithmetic and coverage. If any region remains
   unresolved, report an incomplete sufficient-certificate search. Neither
   partial successes nor a producer success banner replaces independent
   verification. No solver-performance improvement follows from this log.

These are documented outstanding tasks, not work performed or authorized
by this closeout. No new theory, rerun, or literature investigation was
undertaken to finish this record.

## Verification of this closeout

Root inspected the producer, verifier, and final log. An independent Astra
review confirmed the budget, serialization, and BP-verifier limitations.
This was source inspection, not independent verification of the lost
certificates. Targeted checks were:

```
test ! -e /proc/244853
test ! -e research-20261001/orbit-closure/logs/closure_cert_wcorner_BP_BP.json
sha256sum research-20261001/orbit-closure/logs/closure_cert_wcorner_BP.log
git diff --check -- research-20261001/orbit-closure/CLOSEOUT.md research-20261001/PROGRAM.md research-20261002/CLOSEOUT.md
```

The process and output absence checks passed; the hash matched the value
above, and the scoped diff check passed. A targeted Python read counted the
final log messages and checked matching process arguments. Markdown links
and whitespace in the new closeout were also checked locally. No solver
was run, and no Lean, project-wide local verification, or CI checks are
claimed.
