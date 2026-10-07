# Storage verification, October 5, 2026

The checks below concern evidence retention and publication size. They do not
repeat optimization experiments, full support-certificate replay, project-wide
verification or CI checks.

| Targeted command or inspection | Result |
|---|---|
| `python artifacts/verify.py /workspace/local-home/research-artifacts/minlp-notes/20261005 --contents` | Passed all six packages: asset checksums and every original file checksum, member counts and symlink targets; 10,492 members, 27,344,227,344 original bytes |
| `python paper-certified-support-cuts/verification/export_compact.py --verify` | Passed all 33 exports: 3,817 records, 279,930 observed cuts, 11,558,549 compressed bytes |
| `python paper-certified-support-cuts/verification/R10_numbers_tables.py paper-certified-support-cuts/experiments/compact` | 1,988 cells checked, zero mismatches |
| `python paper-certified-support-cuts/verification/R10_numbers_check.py paper-certified-support-cuts/experiments/compact` | Recovered 274,489 primary-population cuts and 92,222 distinct rows; zero replay-record discrepancies or uncovered primary runs; original incomplete logs and incumbent-check failure remain recorded |
| `python -m py_compile artifacts/verify.py artifacts/check_git_size.py` and the four changed compact-verification scripts | Passed |
| `python artifacts/check_git_size.py --base origin/main` before history repair | Correctly rejected all seven existing oversized historical blobs |
| `python artifacts/check_git_size.py --base origin/main` after rebuilding the unpublished commits | Passed; largest new blob is 35,483,455 bytes, below 100 MiB |
| Targeted inventory of paths excluded by the new evidence rules | All 2,872 raw-record, checkpoint and lock files are present in the archive index; no eligible untracked file is at or above 100 MiB |
| Comparison of compact source-ledger SHA-256 and size against the independent archive member index | All 33 ledgers match |
| Backup inspection with `git cat-file --batch-check` for every original unpublished object | All 17,235 objects present; no missing objects |
| Targeted `git check-ignore` inspection of archived `cases/` and `snapshot/` paths | All research inputs and source snapshots remain eligible; generated Python caches remain ignored |
| `git diff --check -- .gitignore README.md research-20261001/scip-rule-fidelity/note.md` | Passed |
| `git archive HEAD paper-certified-support-cuts`, followed by the compact export verifier and appendix table checker in an isolated directory | Passed all 33 exports and 1,988 cells with zero mismatches; the isolated committed checkout contains no raw campaign ledgers |
| Comparison of removed paths against original unpublished HEAD | All 98 omitted trace/checkpoint files are archived; the only other removal is the already-deleted `STREAM_OWNER_LOCK.txt` runtime lock |

The new unique Git blobs occupy 554,844,053 bytes in current object storage,
down from approximately 2.43 GiB for the original unpublished history. This is
not a measurement of the outgoing pack; it establishes that the excluded
evidence is absent from the rewritten commits.

After the backup completed and no Git process was active, 414 confirmed stale
`tmp_pack_*` and `tmp_obj_*` files were removed, recovering 12,160,918,758 bytes.
Every file predated the backup start. Their path/size inventory is preserved in
the external backup's `removed-git-temporaries.json`. No research file was
removed; Git's live object files were retained.

The backup's `repository/.git` retains the original six unpublished commits,
from `c3514f03e` through `b59ed1b83`, based on `8360cf60e`. No shared history is
rewritten. Stale Git temporary object files are excluded from the backup because
they are failed-operation debris, not source or evidence.

The broader compact numerical audit's saved output is
[`numerical-audit.txt`](../paper-certified-support-cuts/experiments/compact/numerical-audit.txt).
The complete raw archives retain support witnesses; compact checks compare
numbers and original replay receipts rather than rerunning certificate replay.
