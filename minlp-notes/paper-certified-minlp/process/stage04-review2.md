# Stage 4 independent review 2

Reviewed the Stage 4 author report, Section 6 and generated tables, V1/V2/V3 snapshots and changes, `rational_text.py` and associated tests, supplement documentation, and a freshly extracted copy of the final core archive. This reviewer performed the designated independent portable extraction and replay/test checks. No other review reports were read. No shared manuscript, implementation, archive, or evidence files were changed, and no numerical generation or full-cohort/bulk replay was repeated.

**Verdict: no major issue found; one minor reproducibility correction is required.** The default final checker, representative audits, compact summaries, and table/catalog generation all work outside the repository. The version-restoration instructions expose an incomplete V1 test-fixture snapshot, detailed below.

## Minor issue: snapshot restoration omits required data

Locations: `supplement/core/README.md`, paragraph beginning “Complete V1, V2, and V3 module/test copies”; `evidence/source-snapshots/primary/certify/tests/test_certificate_contract.py:58`; the corresponding files inside the core archive.

The README instructs readers to make a separate evidence-tree copy and replace its entire `lab/certify` and `lab/lbesh` directories with the chosen snapshot. It also states that snapshots retain each original test set. The primary/V1 snapshot contains the test source but has no `certify/tests/review_artifacts` directory. `test_sol_zero_false_bound_rejected_end_to_end` requires `review_artifacts/bogus2.vipr`.

I independently restored the V1 module directories into an isolated lab and ran the documented test command with the distributed dependencies:

```sh
python -m pytest -q certify/tests -p no:cacheprovider
```

Result: **1 failed, 151 passed**. The failure is `FileNotFoundError` for `certify/tests/review_artifacts/bogus2.vipr`. The failure occurs before the checker is exercised. The independent log is `/tmp/cert-minlp-stage04-review2-5u5_ioyr/v1-tests.log`.

Related consequence of the same directory-replacement advice: none of the three snapshot `certify` directories contains the default tree's `examples/quadratic` bundle. Replacing the whole directory also removes that representative artifact, so the subsequent `reproduce.py small` entry point cannot find its quadratic example. This does not affect the default extracted V3 tree, whose tests and examples pass.

Correction: make snapshot restoration preserve the shared example and test-artifact directories, or distribute the required unchanged fixture/example data with each restorable snapshot. Document which files are historical versioned code and which are common immutable evidence. Verify the V1 restored suite reports all 152 tests passing and that the advertised representative entry point remains usable after restoration. Regenerate the small core manifest, archive hash, and index after the correction. Preserve the frozen production module bytes and original experiment counts. No bulk proof-archive rebuild is required merely for this compact-data issue unless its contents also change.

Severity is minor because the final default artifact and the scientific bounds are unaffected; it is a concrete failure of the optional historical-version reproduction instructions.

## Independent portable reproduction

The inspected core archive had SHA-256 `031a8a47f296d7fd8f484d3ad695c9476a8f316498a8ef5f2d5ecd03d7b287a6`, matching the report/index. I extracted it to `/tmp/cert-minlp-stage04-review2-5u5_ioyr/minlp-certified-evidence` using the data extraction filter. I created a new Python 3.13 environment and installed only the distributed checker requirements plus the optional pytest requirements and pytest's dependencies. Execution unset `PYTHONPATH` and restricted `PATH` to `/usr/bin:/bin`; no optimization vendor package was installed into this environment.

Results:

- `reproduce.py verify`: all **3,779** manifest entries passed, both before and after the examples/tests.
- `reproduce.py small`: all **four complete bundles** passed; the exact source comparisons and returned-point violations were reproduced; the rational `clay0204m` witness and bound established **6545**; all **twelve historical and three new local failed-step extracts** recomputed their stated defects.
- Default V3 `pytest -q certify/tests -p no:cacheprovider`: **161 passed in 2.16 seconds**.
- `reproduce.py summaries`: preserved historical **188/92/9** and primary **203/19/67** outcomes, their exact reference counts, and the separately saved twelve/two repair successes.
- Portable `analyze.py`, `analyze_repairs.py`, and `bound_catalog.py`: all completed successfully. All **13 generated data/TeX outputs** compared byte-for-byte equal with the distributed tables. `analysis-inputs.json` differed as expected because it identifies the new path/environment.

These checks use the actual extracted scripts and data rather than repository imports. Logs and regenerated outputs are retained under the temporary review directory. I did not repeat the already completed 30.7 GB compressed bulk readback; no new concern justified that operation.

## Implementation and scientific findings

The V1→V2 production change is confined to fraction canonicalization in `run_all.py`. FLINT parses and writes the same rational values without disabling Python's integer conversion guard. The atomic temporary-file replacement preserves the original on failed normalization. Tests cover long positive/negative/reducible values, canonicalization in solution/inference sections, and failure preservation.

The V2→V3 production changes are the stated five reporting-facing modules. Direct source comparison confirmed unchanged `exact_model.py`, `convexity.py`, `safecut.py`, and `vipr.py`; the driver diff changes post-proof exact-text parsing/serialization rather than domain, cut, or master validation. Current production/test bytes match the reporting-repair snapshot. `parse_rational_text` uses exact FLINT rationals and an exact Decimal fallback for finite decimal/exponent references; no binary64 approximation enters the authoritative bound/reference arithmetic. Nonfinite text fails, optional oversized floating displays become unavailable, and exact strings remain authoritative.

The new tests provide distinct confidence: large rational round trips, exact decimal reference comparisons, preservation of the digit guard, real complete proof checks under both objective senses, and producer report completion with an exact value beyond the finite floating display range. The producer test mocks vendor execution for a reporting-boundary contract; it is not represented as a solver correctness test.

The preserved primary `tls12` record has `proof.ok=True` but final `report.ok=False`, with the 4,326-digit conversion error in the last check. The targeted V3 records have complete accepted reports. Thus the manuscript's distinction between eighteen proof-rule/grammar failures and one post-proof reporting failure is supported. The original primary **203/19/67** counts remain recorded, and the expected final-checker **204/18/67** result is labeled as an expectation rather than an unperformed full replay.

The rule-failure discussion does not infer false final numerical bounds from invalid submitted steps. The local extracts establish the submitted arithmetic/disjunction defect without claiming preceding proof-prefix correctness. Exact reference differences are kept separate from optimality gaps. The merged catalog checks matching model hashes and objective senses, chooses by exact normalized bounds, retains candidates/provenance, and is correctly described as a catalog rather than a uniform success rate.

Section 6 keeps the uniform production, separate replay, twelve producer repairs, and two reporting repairs distinct. Time budgets, outer cap, concurrency, shared-machine costs, and proof-completion thread limitations are visible. The primitive mathematical rules and formalization scope are not enlarged by the reporting repairs. No further Stage 4 mathematical issue was identified in this review.
