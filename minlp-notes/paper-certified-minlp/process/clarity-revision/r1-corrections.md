# R1 corrections

Completed by the correction agent, distinct from the author. Read the R1
adjudication, reviewer 5 report, and coordinator findings. Addressed all three
accepted minor issues using only `main.tex` and `sections/07-discussion.tex`.

1. The conclusion now assigns **203 of 289** to accepted artifacts in separate
   replay and explicitly contrasts it with **198 successful producer returns**.
   The following sentence retains the explanation of complete proofs surviving
   unsuccessful producer returns. No experiment count or interpretation changed.
2. The abstract now identifies acceptance as coming from **an external MILP
   proof checker**, making the reported failure evidence intelligible without
   the protocol section. It still identifies invalid supplied steps, without
   claiming that the ultimate numerical bounds are false.
3. The conclusion now says two-pass replay reduces **proof rows retained in
   memory**. It retains the qualification that the number of simultaneously
   live rows is not bounded. It does not imply smaller certificate files.

Ran `scripts/build-paper.sh`, which builds from fresh source copies and updates
root `main.pdf` and `main.bbl`. The resulting PDF has 31 pages. The final LaTeX
log has no warnings, undefined references/citations, or overfull/underfull boxes.
PDF text extraction succeeded. Saved build and final LaTeX logs are
`r1-corrections-build.log` and `r1-corrections-main.log` in this directory.

No mathematical statement, code, formal source, numerical data, or campaign
record changed. No tests, numerical generation, or replay were warranted. The
source archive and delivery documentation remain deliberately pending R2;
no repackaging or R2 work was performed. No further issue was identified.
Acceptance remains the coordinator's decision.
