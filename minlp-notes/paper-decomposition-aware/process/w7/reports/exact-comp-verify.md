# W7 verification report: group exact-comp

Files: `sections/exact.tex`, `exact-localized.tex`, `appendix-localized.tex`,
`appendix-boundary.tex`, `computation.tex`, `appendix-computation.tex`. The details are in the
"Verification" section of `process/w7/reports/exact-comp.md`.

| Finding | Editor | Verifier | What was checked or done; reason for any deviation |
|---|---|---|---|
| F-referee-1(b) | ACCEPTED | ACCEPTED, plus one wording fix | The table moved word for word (`exact-comp-verify-move.py`), directly before "Exact output (Section~\ref{sec:comp-exact})". The pointer in 11.3 is correct, and 11.3 quotes $m$, $n$, the nodes (5-11), the stages (9-74) and the bound $2^{m-1}$. Table 3 is placed before Tables 4-6. The lead-in now says "gives the results of CT" instead of "gives the runs of CT", which matches the other Appendix H paragraphs. |
| F-referee-5 | ACCEPTED | ACCEPTED | Checked against `S1_ex_replay.csv` and `S1_localized.csv`. The five instances with the most EX stages are all accepted, with thresholds of 40-72 stages. The sentence agrees with 11.4. |
| F-consistency-1 | MODIFIED | ACCEPTED as modified | Dropping "exact-output" is sound. The two sentences of Section 6.5 now agree (E4 and S1, with the same threshold). |
| F-consistency-2 | ACCEPTED | ACCEPTED | |
| F-referee-2 | MODIFIED | ACCEPTED as modified | The sentence follows the coordinator decision. |
| F-proofread-13 | ACCEPTED | ACCEPTED | |
| F-proofread-14 | ACCEPTED | ACCEPTED | No other British spellings or `non-` compounds in the six files. |
| F-dependencies-3 | MODIFIED | ACCEPTED as modified | The data confirm the claim. In stages 7-10 of all 18 runs, the maximum and the mean of `nodes_free` equal the formula. "for E3" is needed. |
| F-dependencies-4 | ACCEPTED | ACCEPTED | The fix matches growth.tex:318. |
| O2 | MODIFIED | ACCEPTED as modified | Appendix H (c), (d), (f) and (g) cover every deleted clause. Later uses (11.2, 11.3, 11.4) are handled. No other file cites 11.1. "Seven ways" still matches items (a)-(g). |
| Appendix B opening | ACCEPTED | MODIFIED | The sentence said the propositions show that the margin term and strict complementarity "are needed", without scope. Props. B.5 and B.6 show only that this procedure needs them; B.2 itself says "for certificates of this form". Now: "...gives a procedure with exact implicit output ... together with two propositions showing that this procedure needs the margin term in its cost bound and strict complementarity (...)". |

No proof moved in this group. The 58 labels of the six files are all still present, and none is
duplicated.

## Cross-file requests

None.

## Commands run (targeted, local; not CI)

- Private build: `rm -rf /tmp/w7-exact-comp-verify && mkdir -p /tmp/w7-exact-comp-verify && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-exact-comp-verify/ && cd /tmp/w7-exact-comp-verify && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`
  - Run before and after the fixes. Both runs: exit 0, 127 pages.
  - No errors, undefined references, multiply defined labels or overfull boxes.
  - No `??` in the `pdftotext` output.
- `python3 process/w7/checks/exact-comp-verify-move.py`: PASS.
- `python3 process/w7/checks/exact-comp-e3sep.py` and inline Python on `experiments/results/E3_stages.csv`, `S1_ex_replay.csv` and `S1_localized.csv`.
- `diff` of the six files against `process/w7/sections-before-w7/`.
- `grep` over `sections/*.tex` for the O2 items, cross-references to Section 11 and British spellings.
- I read the rendered text of every edited passage.

No project-wide verification was run, and CI was not consulted.
