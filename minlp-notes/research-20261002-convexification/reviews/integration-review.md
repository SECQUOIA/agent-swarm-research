# Independent solver integration review

This review covers the small-block separator, its native SCIP model binding,
sample selection, and saved-cut replay. It does not certify SCIP's numerical
primal or dual bounds. Review tests use the original source expressions and
actual SCIP solutions or rows; they do not infer correctness from a stronger
reported bound.

## Findings and changes required before the experiment

1. **Algebraic equality did not preserve source domains.** Deduplicating atoms
   by their SymPy expression merged `x^2` and `sqrt(x)^4`, removing the second
   occurrence's domain restriction. Discovery now deduplicates exact source
   trees. The review checks both distinct auxiliary definitions using original
   SCIP solution feasibility.
2. **Native expression construction can change exact coefficients.** For
   example, a constant subtree `1e16 + 1 - 1e16` was evaluated as zero, although
   its exact source value is one. Constant arithmetic is now normalized only
   when its exact final value is representable. Candidate auxiliary graphs are
   compared with the exact interpretation of the constructed PySCIPOpt
   expression. A mismatch cannot receive a source-graph certificate.
3. **Checking each atom was insufficient.** A complete row can lose a small
   coefficient when large coefficients cancel, even though every atom is
   represented exactly. Conversely, replacing source occurrences by separate
   auxiliaries can change the cancellation order. The integration now checks
   complete original rows in every mode and checks reconstructed rows after
   exact auxiliary substitution. Original-row mismatches are refused; a
   reconstructed-row mismatch retains the admitted original row.
4. **The inserted row needed its own check.** Repeating requested coefficients
   in a log does not show which row SCIP received. The integration now reads
   the row's actual columns, coefficients, bounds, constant, and scope before
   insertion. It rejects changed coefficients and all missing nonzero columns,
   including numerical presolve fixings. No certificate for a presolve fixing
   is assumed.
5. **Zero-weight source domains require a separate guard.** Direct probes
   found that SCIP removes the domain in `0*sqrt(x)`,
   `sqrt(x)-sqrt(x)`, and `0*log(x)`. On `[-1,1]`, a baseline minimizing `x`
   returned `-1`, while the auxiliary model retained the domain. The raw native
   expression still contained these function nodes, so comparing node presence
   was insufficient. Every mode now proves all original source domain
   restrictions throughout the declared box before normalizing expressions.
   The guard visits children of zero products and powers. An unresolved
   restriction produces a recorded refusal. This deliberately rejects some
   models whose domain validity would require additional constraints.
6. **Finite source sides must remain finite to SCIP.** The importer refuses
   declared finite variable bounds or constraint sides at or beyond SCIP's
   infinity sentinel. It also refuses reversed bounds, incorrectly signed
   infinities, NaNs, and mismatched variable metadata lengths.

## What the independent replay checks

`experiments/replay.py` runs in a fresh process against the experiment's frozen
source snapshot. It verifies all snapshot hashes, frozen case descriptors,
archived OSiL input hashes, and each saved original-model fingerprint. It then
checks that every auxiliary comes from an original source subtree and that
expanding the saved row replacements recovers the original expression trees.
Quadratic products, variable indices, original declared boxes, affine rows,
column names, actual inserted row data, and certificate coefficients are bound
separately. Feature strings are never evaluated.

The support checker recomputes each proof against independently reconstructed
source features. Tamper controls change the input fingerprint, source trees,
variable columns, affine domain, box, feature text, coefficient, right-hand
side, cut scope, actual inserted coefficient, actual bound, and transformed
column mapping. Missing proofs do not count as certified. A worker without a
complete cut log has an unknown cut count, rather than zero cuts.

The native sampling kernel and floating-point LP supply proposals only. Exact
screening accepts source polynomials, checks sample feasibility against exact
declared bounds and affine rows, and uses scaled L1 distance for the LP's
coordinatewise coefficient bounds. A skipped, failed, capped, or unsupported
block never establishes hull membership. Added rows use global source domains
and separation is restricted to the root.

## Verification record

The following targeted commands were run during review:

```text
PYTHONPATH=research-20261002-convexification code/minlp_solver_lab/.venv/bin/python -m unittest discover -s research-20261002-convexification/reviews -p 'test_replay_review.py' -v
PYTHONPATH=research-20261002-convexification code/minlp_solver_lab/.venv/bin/python research-20261002-convexification/reviews/test_source_model_review.py
```

The five replay tests and 13 source-model tests passed. They include a real
SCIP mechanism solve, certificate replay, independent original-coordinate
activity checks, 12 distinct replay tamper controls, both complete-row
cancellation defects, and 24 cancelled-domain cases across the four modes.
Mocked row tests separately change coefficients, bounds, scope, columns, and
fixed-variable substitutions. No project-wide verification or CI inspection
was performed.

The experiment was cleared to freeze after these fixes. Final reviewed source
SHA256 values are:

| File | SHA256 |
| --- | --- |
| `solver/integration.py` | `6a97294496c8571b82bae30c01b6be4f60cb421062e63242f0637597402cafd8` |
| `solver/model_binding.py` | `334efac58cbdb2c0fd6a36fbbecfd9cea8b98eb31e94029c383f15fade5c9348` |
| `solver/native_sampling.py` | `989130d4cfa49b3930b8a9db6e295e1aac8664a51b53e684b3df55fd781dc213` |
| `solver/native_sampling.c` | `b78231ad142e33a135319f6492219b1848830406728bf5db738586ea90821ff0` |
| `solver/screening.py` | `2a98eee1c7719127bdbeb95e6660ab9d8d952a3c116f6e11216f07cc95377b8e` |
| `experiments/replay.py` | `4fe01fcdde876ba1c5ecf44437def18794d59404d92fbfeff1493df612781efc` |
| `reviews/test_source_model_review.py` | `027c7115450edd7fb46a4a22f8192b2a0be4cf61f537ddd7c771cdc75f122a01` |
| `reviews/test_replay_review.py` | `29ff08a38701668978643ad437fdec464c8b35c60ceb5ca862dc0a76fa871733` |

## Archived campaign replay

After `campaign-v1/completion.json` was written, the following command was run
in a fresh process:

```text
code/minlp_solver_lab/.venv/bin/python research-20261002-convexification/experiments/replay.py research-20261002-convexification/experiments/campaign-v1 --output research-20261002-convexification/experiments/campaign-v1/replay.json
```

The command exited successfully. The saved
[replay result](../experiments/campaign-v1/replay.json) verifies 101 frozen
source and input files, binds 308 returned model records to the archived
original inputs, and replays **all 1,082 recorded cuts**. All 12 tamper controls
were rejected. The job list, ledger, unique run identifiers, and raw result
files each contain 316 entries. The current integration, model-binding, and
replay source hashes still match the frozen versions.

The 308 bound model records include 36 explicit strict-importer refusals;
binding an input record does not imply that its model was solved. Eight
`cvxnonsep_pcon40r` worker errors lack a complete model/cut record and remain
listed separately with an unknown cut count. Their archived logs show an
unsupported variable exponent during model construction. No unrecorded row
is counted as certified. There were no failed checks among the recorded cuts.

A preliminary fresh-process replay of the first 42 records also passed;
[its saved output](replay-partial-review.json) is retained as a pipeline check.
The final 316-record replay is the evidence used for the complete campaign.

The requested integration time is a soft budget: setup reduces the subsequent
SCIP limit, but an individual setup or support operation is not preempted.
The experiment separately records total and process wall time, overshoots,
and a hard worker timeout. Timing on a shared host does not establish a
population runtime improvement.
