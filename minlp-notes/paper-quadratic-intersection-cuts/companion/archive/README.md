# Evidence archive

This archive preserves selected original code, certificate data, and saved
numerical records. Files under `source/` retain their original repository-relative
paths and names. Source notes and closeout documents are omitted;
`neutral-reference.json` records their hashes as provenance references.

From this directory, run the metadata check with Python 3.9 or later:

```sh
python3 check_manifest.py
```

The check tests file hashes, counts, and cohort consistency. It runs no solvers
or certificate verifiers and does not replay mathematical proofs. Matching
metadata establishes archive integrity, not the validity of a mathematical claim.

Completed machine certificates include the ratio-bound facet-cover JSONL files,
the completed orbit-closure box and closure-point JSON files, and the saved
rational cuts for the closure lower bound. Other logs record numerical results
or successful checks. In particular, the minor-set A and S1 near-endpoint
brackets and the ratio-bound near-boundary upper-bound logs do not retain all
rational endpoint matrices. Some accompanying scripts generate witnesses
numerically before checking them exactly. These receipts are not complete saved
certificates.

The original sfree one-cut summaries contain ten superseded corner bounds.
The corrected affected-corner records and exact two-ray receipts are under
`source/research-20261001/scip-rule-fidelity/logs/`; multiround recheck summaries
are under the corresponding multiround directory. The fidelity corrected root
loops and the multiround fast loops use different implementations and retain
distinct trajectories. Failed box searches and short stopped-job logs are
diagnostics; they are not completed certificates.

`survey-labels.json` maps manuscript labels R1–R8 to their original record names,
saved apex and ray coordinates, code definitions, and exact record selectors.
The coordinates copy retained floating-point data; the mapping makes no new
exact-arithmetic claim. In the table, `a` and `b` refer to the archived
[A/P survey a](source/research-20261001/orbit-closure/logs/closure_survey_a.jsonl)
and [A/P survey b](source/research-20261001/orbit-closure/logs/closure_survey_b.jsonl);
numbers give physical line numbers.

| Manuscript label | Original record name | Saved coordinate row |
| --- | --- | --- |
| R1 | `adv8_1` | a:3 |
| R2 | `adv8_4` | a:4 |
| R3 | `prop16_v2_1` | b:2 |
| R4 | `prop16_v8` | b:3 |
| R5 | `supp1_1074` | b:4 |
| R6 | `supp1_3437` | b:5 |
| R7 | `supp1_4580` | b:6 |
| R8 | `supp1_5512` | b:7 |

[closure_survey.py](source/research-20261001/orbit-closure/code/closure_survey.py)
defines R3–R8 in `INST` and constructs R1–R2 from the saved adversarial
restart records. The mapping also points to the archived constructor and
parameter records for those two cases, plus the available B/BP survey rows.

The following entry points support separate exact checks without numerical
witness generation. Paths below are relative to
`source/research-20261001/`; their mathematical assumptions still require review.

| Entry point | Python dependencies |
| --- | --- |
| `ratio-bound/code/verify_zB.py FILE RHO [FAMILY]` | Standard library; sibling `certify_zB.py` |
| `orbit-closure/code/verify_box_cert.py FILE` | Standard library and SymPy |
| `orbit-closure/code/verify_closure_cert.py FILE` | Standard library |
| `orbit-closure/code/closure_lower.py --verify FILE` | Standard library in this mode |
| `orbit-closure/reviews/r2-code/indep_prop10_replay.py FILE` | Standard library |
| `multiround/reviews/r2-scripts/oq3_r2.py` | Standard library; checks a fixed finite sequence |

Preserve directory relationships for sibling imports. Original code can contain
absolute machine paths, original names, and historical metadata. The archive
therefore has limits on portability and anonymity. No redistribution license is
added; existing notices remain with their files.

Stock-SCIP timing claims are withdrawn, and debug-solution results retain
unresolved warnings and reference-value issues.
Optional diagnostic multiround traces with full detail are omitted; their saved
summaries are retained. Summaries do not replace those omitted traces for an
independent reconstruction.

## Public export

This public copy contains privacy and redistribution edits. Current package hashes describe the exported files; `original_sha256` records identify the original committed bytes when an exported file changed. Historical experiment and review hashes remain provenance records. Scientific result values were retained, and the experiments were not rerun. Repository-level `THIRD_PARTY_NOTICES.md` records licenses for retained third-party material.
