The replay and reporting code now keeps historical acceptance separate from a
new verification verdict. This review covers `certify/recheck.py`,
`certify/run_all.py`, `certify/summarize.py`, and their replay tests. It does
not establish certificate soundness independently of the mathematical and
VIPR reviews, and it does not establish completion of a particular benchmark
campaign. The campaign's own manifest and summary supply that evidence.

The review found and resolved the following reporting and integration defects:

- The summary originally lacked an expected record count. It now reports
  `expected_records` and `replay_complete`; a complete replay requires every
  historical record index exactly once. A partial output or a duplicated index
  cannot establish completion.
- Historical acceptance counters now read the replay's `historical_checker`
  and `historical_viprchk` fields. An old acceptance flag cannot create a new
  verified bound.
- Replay now fingerprints artifacts again after checking. A change during
  checking produces `artifacts_changed` and no top-level certified bound.
- The producer now runs the authoritative checker within each SCIP attempt.
  An externally accepted default proof that fails internal replay triggers
  the safe retry. Its final record says `verified` or `rejected` and exposes
  a bound only on acceptance.
- Producer worker output goes to temporary files, avoiding an undrained pipe
  blocking a running worker. Replay timeouts terminate the process group,
  including a checker descendant. Timeout termination tolerates a worker
  exiting concurrently.
- Producer campaigns require a new output file and preserve existing artifact
  directories. This prevents the old instance-name-only resume logic from
  combining different campaigns or appending to an interrupted JSON line.
  Resumable verification belongs to `certify.recheck`.

The replay manifest pins the historical input, source files, instance and
artifact roots, Python executable, relevant package versions, optional external
checker executable, and timeout. Each record pins its model, lemma, master,
and completed proof by SHA-256 and byte size. Resume rejects a changed manifest
or changed artifacts. It recovers only an interrupted final JSON line; complete
corrupt records and duplicate record indices fail. Historical files remain
unchanged, and the replay output must differ from its input.

Bound and reference comparisons use rational arithmetic, including the
objective sense. A negative signed gap is a discrepancy rather than a closed
gap. Recorded primal values remain unverified references: proximity is not an
optimality certificate, and a discrepancy alone is not evidence of a solver
defect.

Independent verification used:

```sh
cd code/minlp_solver_lab
.venv/bin/python -m pytest certify/tests/test_replay.py certify/tests/test_replay_review.py -q
```

Result: **11 passed**. The independent review tests exercise an artifact changed
inside a checker call, termination of a real hanging worker and its descendant,
partial and duplicated replay indices, safe retry after authoritative rejection,
final rejection without a bound, and conversion of a maximization bound to the
minimization master sense, and refusal to append a producer campaign to existing
output. Existing tests additionally cover exact large-integer
comparisons, negative gaps, value-preserving proof canonicalization, recovery of
an incomplete output line, and refusal to resume changed historical input.

These checks assume trusted local Python model files and installed dependencies.
The environment manifest records package versions rather than vendoring or
hashing every installed dependency. Input models can execute Python when loaded.
Keep code and artifacts fixed during a campaign; pre/post hashes detect ordinary
concurrent changes but do not make a mutable filesystem an adversarially secure
snapshot.
