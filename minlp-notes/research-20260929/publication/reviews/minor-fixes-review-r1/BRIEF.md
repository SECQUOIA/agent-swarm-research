# Brief for minor-fixes verifier agents

Repo: /workspace/minlp-notes. Publication dir P = research-20260929/publication.
Task: an author fixed minor issues raised in reviews of research tracks. You independently verify the fixes for your assigned tracks.

Inputs
- Author's issue table and integration list: P/reviews/minor-fixes/summary.md (rows for your tracks), issues.json, commands.md.
- Each review: P/reviews/<review>.md (the issues as raised) plus the reviewer's evidence dir P/reviews/<review-dir>/.
- Each track report now: P/<track>/report.md, ending with a "Response to review" section.
- Pre-fix report: P/reviews/minor-fixes/before/<track with / -> __>.txt (identical to git HEAD for tracked reports).
- Author's new check scripts/logs: P/<track>/minor_review_check.py and logs/minor_review_check.log (or checks/ for literature).

For each issue in your tracks:
1. Read the issue in the review. Read the fix in the report (body + response row). Decide: fix present, correct and complete? Or "no change needed" reasoning holds?
2. Verify factual corrections against the evidence yourself: where a number is involved, write your own small independent script (do not just rerun the author's check); for literature facts, read the saved source text/PDF (pdftotext available) and confirm page/table/value.
3. Check the corresponding integration-change cell in summary.md is correct.
Also: diff before/<track>.txt against the current report (`diff -u`), and examine EVERY hunk for collateral damage: accidental deletions, changed numbers not explained by an issue, new unsupported claims, broken links/paths, inconsistencies between the body and the response table, stale statements that still contradict the fix elsewhere in the report.

Rules
- Do NOT edit any track files, scripts, or the author's files. Do not commit/push/contact anyone/no network submissions (reading public web sources is OK if the saved source is missing, but prefer saved sources).
- Write only to P/reviews/minor-fixes-review-r1/ : your notes file group-<X>.md and scratch scripts under P/reviews/minor-fixes-review-r1/scratch-<X>/ (logs too).
- CPU: run at most ONE process at a time, single-threaded (prefix OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1). Another session runs experiments. Do not rerun main constructions/solver campaigns; any script you run should finish in a few minutes at most. Skip anything expensive and say so.
- Ignore path-only changes in scripts (another agent is replacing hard-coded /workspace/local-home paths with relative roots); they are not part of this review.
- Record every command you ran (exact) in your notes file.

Output: write group-<X>.md with, per issue: track, issue number/title, verdict (OK / problem), evidence (what you checked, numbers you got), and for problems a severity (blocker/major/minor), location (file:line), and suggested fix. Then a "collateral" section from the diff review, and a "commands" section. Your final message should be a compact version of the same findings (problems in full; OK items one line each).
Severity guide: blocker = a false certified/numerical claim that would enter the paper; major = a wrong factual statement or an issue not actually fixed; minor = incomplete wording, small inconsistency, stale cross-reference.
