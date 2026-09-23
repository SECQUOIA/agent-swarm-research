# Stage 7, round 1 — independent reviewer 4

**Verdict: no major issues; two minor reproducibility/documentation issues.**

## Scope and positive findings

I read the stage author report, new abstract/introduction/discussion, formal overview, README files, complete bibliography, submission script, portable verification runner, and the rewritten all-dimension two-point hull proof. I also checked the good-cone and cardinality arguments surrounding that proof. The synthesis correctly distinguishes certificate existence, exact descriptions, approximation, original-variable cardinality, and lifted descriptions. Prior results are credited rather than claimed as new; the strict PDLC transfer and inherited four-necessary example are distinguished. The new two-point proof works for r=2: e perpendicular to b*u-a*v gives the required common gamma, both roots are strictly feasible, and the displayed positive weights recover the original point.

The portable scope table expressly distinguishes the stronger paper lower constant and smaller SDP test from the formal interfaces, and states exclusions. The archive contains the required sources and figure, excludes dependencies and historical reviews, and has no surrounding-repository dependency for LaTeX compilation.

## Minor 1: failed verification can leave stale success evidence

` supplement/lean/verify.py ` writes a success manifest only at the end, but does not remove a manifest left from an earlier successful run. `package_submission.py` then packages verification evidence solely on the existence of that manifest. A failed rerun can therefore leave an old success manifest beside changed inputs or overwritten failed logs, contrary to the packager comment that an incomplete run is never represented as success.

I reproduced this only in the isolated extracted archive: append a harmless comment to a fingerprinted Lean file; run `python3 verify.py`; the runner correctly exits 1 with `Source fingerprint mismatch`, but `verification/manifest.json` remains present. The test source was restored. No workspace proof source was modified. The existing delivered success evidence is valid: I independently matched every manifest input hash against the extracted inputs.

Required correction: invalidate/remove the old success manifest before any attempted verification; when including evidence, have the packager validate the recorded input hashes against current packaged files and refuse stale evidence. A regression should demonstrate that a failed rerun leaves no success manifest and that packaging rejects evidence whose input hash no longer matches. Because the runner is itself fingerprinted, its changed version needs a fresh successful portable run before final evidence is packaged. This is minor because it affects future rerun robustness, not current theorem validity or current evidence.

## Minor 2: author report understates supplement page count

`process/stage07-author.md` says the detailed supplement is 14 pages (twice). The frozen `formal-supplement.pdf` and a clean extracted-source build are both 15 pages. Correct the process record; no manuscript change is needed for this.

## Independent targeted checks actually run

- Extracted `dist/quadratic-aggregation-source.zip` to `/tmp/s7-review4-wc3sjrp1/quadratic-aggregation/`.
- Checked all source ZIP hashes, exact agreement with current workspace inputs, and every recorded portable verification input hash: PASS.
- In the isolated extraction, ran `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/review main.tex`: PASS, 42 pages.
- Ran the same command for `formal-supplement.tex`: PASS, 15 pages.
- Checked both final logs: no warnings, undefined references, overfull or underfull boxes.
- Compared extracted PDF text of the rebuilt and delivered formal supplements: identical.
- Rendered and visually inspected delivered main pages 1 and 33 (abstract/introduction and formal coverage table/discussion): readable, no clipping or layout defect.
- Performed the isolated failed-verification reproduction described above. No full Lean rerun was duplicated; current complete evidence was checked by hashes.

No project-wide checks or CI inspection were performed. No manuscript, proof, or packaging source was edited by this reviewer.
