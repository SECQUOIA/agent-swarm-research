# Stage 2 independent review 3

Reviewed 2026-09-13. Read sections 3–4, their connection to sections 1–2, the Stage 2 author report and analytic validation, and the actual `exact_model`, `convexity`, `safecut`, `driver`, `vipr`, `run_all`, `recheck`, and `summarize` implementations as relevant. Focus: operational truth, arithmetic/precision, API scope, master identity, streaming, provenance, generation and replay behavior, and consistency with the mathematical argument. No manuscript or checker changes were made.

## Verdict

**No major Stage 2 issues found.** Two minor wording corrections in the provenance paragraph should be made. The soundness arguments inspected are valid under their stated support, arithmetic, and model-identity hypotheses, and the implementation section usually makes the boundary between mathematical implication and trusted executable implementation unusually clear. I found no counterexample invalidating the supported certificate pipeline.

## Required minor corrections

### R3-1 — Summary completeness is reported, not required for producing a summary

Location: `sections/04-implementation.tex:158`, “Summaries require complete cohort accounting”.

Actual behavior: `certify/summarize.py` produces summaries for incomplete cohorts too. It sets `replay_complete` by checking the supplied `expected_records` against the number and set of record indices; the flag is false when records are missing, duplicated, or the expected count is absent. It does not reject an incomplete summary. `test_replay_review.py:71–77` explicitly exercises this behavior.

Proposed correction: “Summaries report whether all expected record indices are present exactly once and use exact rational objective-sense comparisons before converting values for display.” A completed campaign claim can then require this flag in the experimental analysis. The current complete historical cohort passes the test, so this correction does not change its results.

### R3-2 — Resume matches pinned settings, not every execution setting

Location: `sections/04-implementation.tex:158`, “Resume requires matching inputs and settings”.

Actual behavior: `recheck.environment_manifest` pins record input, roots, Python executable/version, platform, package versions, source files, optional checker, and timeout. It does not pin `--jobs`; resuming with different parallelism is allowed. Per-artifact identity is separately rechecked. Since timing and process accounting are a substantive part of this paper, “settings” without qualification could suggest the worker count is protected too.

Proposed correction: “Resume requires matching artifact fingerprints and the inputs, source/environment identifiers, external checker, and timeout pinned in the manifest; worker parallelism may change.” Alternatively use the shorter phrase “matching inputs and manifest-pinned settings” and state the worker count separately in the experimental protocol. No change to the checker or frozen evidence is needed.

## Independent validation

- Re-executed `process/stage02-analytic-validation.py` with the solver-lab environment. All rational/symbolic identity assertions passed, and the self-contained quadratic bundle again replayed 11 cuts and 39 derivations with exact normalized lower bound `1/4`.
- Recomputed the script's seven certification-source hashes; output matches the recorded Stage 2 JSON. No source drift was found.
- Independently ran `.venv/bin/python -m pytest -q certify/tests -p no:cacheprovider`: **152 passed in 2.03 seconds**. This is this review's run time, not a replacement of the author's separately recorded 2.51 seconds.
- No large-proof campaign or additional numerical producer campaign was run in this review. Tests and one bundle replay do not establish universal software correctness.

## Findings supporting acceptance

### Precision and arithmetic

`convexity._rpow` and `_iv_bound` use 128-bit interval precision for nonrational range endpoints; `SafeCutter` and given-cut replay use 200 bits. The manuscript accurately distinguishes these contexts. Rational point conversion uses numerator/denominator interval division. Endpoint extraction reads the internal dyadic tuple, avoiding an intermediate lower-precision conversion. The producer's default 12-digit slopes and downward 30-digit intercepts match the code. The text correctly refuses to treat the latter as a guaranteed positive separation margin: exact replay compares the proposed intercept to its own recomputed rigorous endpoint. The safe-cut worked example and half-line signs check exactly.

### API and model/proof identity

The four-step complete-check contract matches `check_certificate`: exact model preparation, nonlinear lemma replay, regenerated-LP equality and VIPR problem matching, complete internal proof validation, then optional external corroboration. Partial results expose no certified top-level bound. Lower-level VIPR support for maximization and infeasibility is correctly separated from the finite minimization lower-bound MINLP API.

The exact master matcher checks objective sense/coefficient identity, integrality, variables under the restricted transformed-name bijection, and a constraint/bound multiset. Its positive-scaling normalization does not accept negative equality scaling, exactly as stated. Objective constants use a fixed-one variable; the nonlinear epigraph is free. Constant affine tautologies are omitted and contradictions rejected. The loader's execution/dedenting behavior and loaded-tree semantics are not hidden behind the source hash.

### Discrete invariant and streaming

The incumbent-restricted set `S` is the appropriate invariant for solution cutoffs. The proof lifts its final bound to all master-feasible points using an actually supplied best feasible witness, rather than assuming an optimizer exists. The linear-combination, rounding, and unsplit rules track nonzero dependencies correctly. The formal unsplit premise (integrality of the form on master-feasible points) is mathematically sufficient; the executable enforces the stronger syntactic condition of integer coefficients on integer variables. This is conservative rather than unsound.

The parser checks all supplied solutions, requires every reference—including zero multiplier references—to precede the current row, validates lifetime constraints, and checks the suffix after an earlier proving derivation. `global` is an assertion about independently tracked assumptions rather than a discharge operation. The actual implementation uses two `array('q')` arrays during scanning and one thereafter, retaining the initial rows during solution checking and the scan, plus live sparse rows during derivation replay. The paper includes initial-row and longest-line costs and avoids a constant-memory claim. Assumption sets and rational objects are part of the live-row storage, so the array byte figures must continue to be described as array costs rather than total memory.

### Generation, hashing, and error behavior

`run_all` preserves existing artifact directories, constructs new proofs, canonicalizes fraction tokens without changing their values, can retry after an authoritative replay failure, and returns a certified value only from an accepted internal report. Its distinct search, completion, external-checker, and total-worker limits support the manuscript's warning that solver time is not total pipeline time.

`recheck` hashes artifact files before and after checking, kills the process group on timeout and abnormal exit, flushes/fsyncs records, and recovers only a malformed final uncompleted JSON line. The section explicitly assumes stable files and excludes adversarial change-and-restore protection. Library versions are identifiers rather than complete library binary hashes; the wording appropriately says source/environment identifiers rather than claiming a verified or hermetically reproduced environment.

### Scope and integration

Sections 3–4 develop the mathematical obligations promised in the introduction rather than proposing new universal curvature recognition or proof-system completeness. The domain, support-at-boundary, and shared-trust qualifications connect consistently to section 2. The monomial and PSD arguments provide standalone justifications for the stated sufficient rules. Recognized norms and absolute values do not silently become general nonsmooth gradient support. Rejection/refutation distinctions survive the implementation discussion. Missing later Lean, experiment, or supplement work is outside this stage's acceptance verdict.
