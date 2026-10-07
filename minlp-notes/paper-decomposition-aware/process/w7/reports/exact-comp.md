# W7 report: group exact-comp

Files edited: `sections/exact-localized.tex`, `sections/appendix-localized.tex`,
`sections/appendix-boundary.tex`, `sections/computation.tex`,
`sections/appendix-computation.tex`. `sections/exact.tex` needed no change.

| Finding | Decision | What was done | Reason for any deviation |
|---|---|---|---|
| F-referee-1(b) | ACCEPTED | Moved the `tab:chain` table environment unchanged from computation.tex to appendix-computation.tex, directly before `\paragraph{Exact output (Section~\ref{sec:comp-exact}).}` (verifier's placement, so Appendix H follows section order). Section 11.3 now reads "Table~\ref{tab:chain} in Appendix~\ref{app:computation} reports CT on the family ...". To keep 11.3 readable without the table, it now also gives the values of $m$ ($m=2,4,8,\dots,64$) and the stage range ("from 9 to 74"); it already gave the grid sizes (5 to 11 nodes) and the message lower bound $2^{m-1}$. In Appendix H the table is introduced by a one-line paragraph "Expanding-box chain (Section~\ref{sec:comp-chain}). Table~\ref{tab:chain} gives the runs of CT on $\Psi_m$ for each~$m$.", in the same form as the other paragraphs of Appendix H. | The lead-in paragraph was added so that the table is cited in the appendix and does not stand between two unrelated paragraphs. Table numbers stay in order (Table 3 is now on p. 125, before Tables 4-6). |
| F-referee-1(a), (c) | not assigned / NOT applied | (a) belongs to other groups. (c) was not applied (coordinator decision): Section 6.5 stays in the main text. | |
| F-referee-5 | ACCEPTED | exact-localized.tex: "...on 29 of 30 random mixed-integer instances; on the five of them on which EX used the most stages, one CT run needed 40 to 72 stages to reach the threshold of Proposition~\ref{prop:accept} with the constants of~\eqref{eq:exact-constants}." | Checked against `experiments/results/S1_ex_replay.csv` and `S1_localized.csv`: the five instances with the most EX stages (542, 542, 542, 542, 534) are all among the 29 accepted (the one failure, `random_path_n8_s7014`, used 138 EX stages), so "five of them" is correct; their lemma-constant threshold stages are 72, 70, 71, 54, 40. |
| F-consistency-1 | MODIFIED | First sentence of Section 6.5 now reads "as small as about $2^{-315}$ on the instances of experiment E4 (Section~\ref{sec:comp-exact}), which have at most six variables." | Dropped "exact-output" from the proposed "exact-output instances of experiment E4": E4 is the exact-output experiment, so the word repeats itself. Combined with F-referee-5, the two sentences of Section 6.5 that quote experiments now name their experiment (E4 for the $2^{-315}$ requirement, S1 for the stage counts) and both refer to the threshold of Proposition~\ref{prop:accept} with the constants of~\eqref{eq:exact-constants}. |
| F-consistency-2 | ACCEPTED | appendix-boundary.tex: "as the next two examples show" -> "as the next two propositions show". | |
| F-referee-2 | MODIFIED (coordinator decision) | computation.tex: "Code, inputs, raw results and reproduction scripts (one command per experiment group), together with the solver files they import, are provided as supplementary material." | Supplementary material instead of the archive DOI, per the coordinator decision. Keywords/MSC are in abstract.tex (not owned); no other sentence in my files states code availability. |
| F-proofread-13 | ACCEPTED | computation.tex (E6): "...and on the remaining one no candidate was proved optimal." | |
| F-proofread-14 | ACCEPTED (my part) | computation.tex: "modelled" -> "modeled". A scan of my six files for other British spellings and hyphenated `non-` compounds found none. | "non-uniform" (constraints.tex) and "non-asymptotic" (related.tex) belong to other groups. |
| F-dependencies-3 | MODIFIED | appendix-computation.tex: "E3 was also run with $\kappa_{\mathrm{target}}=2$, for which the free coordinates are separable (Section~\ref{sec:comp-growth}); on these instances filtered uniform grids had exactly $4(\lfloor\sqrt{n/4}\rfloor+1)+1$ nodes per free coordinate in the last four stages. Section~\ref{sec:comp-growth} reports only $\kappa_{\mathrm{target}}=4$ for E3, because the separable case does not test coupling." | Two precision changes. (1) "nodes" -> "nodes per free coordinate in the last four stages": `process/w7/checks/exact-comp-e3sep.py` shows, from `experiments/results/E3_stages.csv`, that for all 18 runs the maximum and the mean over free coordinates in the last four stages both equal the formula (9, 9, 13, 13, 21, 25). (2) "reports only ... for E3": Section 11.2 does report $\kappa_{\mathrm{target}}=2$ for E2, so without "for E3" the sentence would be false. "for which the generator makes" was shortened to "for which", since Section 11.2 already describes the generator. |
| F-dependencies-4 | ACCEPTED | appendix-computation.tex item (b): $J$ -> $j_{\max}$ in both inequalities, matching Lemma~\ref{lem:commonmesh} (growth.tex:318). | |
| O2 | MODIFIED | Section 11.1 now reads: "It differs from the analysis in seven ways, none of which affects validity (Appendix~\ref{app:computation} lists them); the most important is that all coordinates share the mesh $h_j=s2^{-j}$, so the analysis that applies is Lemma~\ref{lem:commonmesh} with the Euclidean condition number $\kappa$, not Theorem~\ref{thm:approx}. Exact coordinate descent from $\ell$, $u$ and the box midpoint provides the first incumbent before stage~$0$, and each trial starts with the center at the current incumbent." The EX details and the definition of the "uniform" grids were deleted. Checks: Appendix H lists every deleted item, namely (c) center at the incumbent, (d) coordinate descent, (f) "uniform" grids and (g) the EX wrapper. Later text in Section 11 refers to two of them: "the initial coordinate descent already returns $x^*$" (11.2) and "the solver's first descent start" (11.3). So one short sentence on the descent and the first center was kept. 11.4 relied on the deleted EX item ("Because the wrapper doubles $q$ and restarts in every round", with "wrapper" never defined in the main text); it now reads "Because our implementation of EX starts at $q=4$, doubles $q$ after each round and restarts the grid solver in every round", which also justifies "a power of two" in the same sentence. The "uniform" grids remain defined by "($\theta=0$ for uniform grids)" in the E1-E3 paragraph. Because the deleted text held the first reference to EX in Section 11, "Experiment E4 runs EX" became "Experiment E4 runs EX (Algorithm~\ref{alg:ex})" (CONVENTIONS section 2). | This keeps the main text self-contained after the shortening, as the coordinator's check requires. Net saving in 11.1 is 5 source lines instead of about 8. |
| Appendix B opening (from F-dependencies-1) | ACCEPTED | appendix-localized.tex, after the `\section` heading: "This appendix proves Corollary~\ref{cor:local} and, for the explicit polynomials of Section~\ref{sec:polynomial}, gives an exact implicit output when the minimizer may be irrational and lie on the boundary (Theorem~\ref{thm:boundary}), together with two propositions showing that the margin term and strict complementarity in this theorem are needed (Propositions~\ref{prop:margin} and~\ref{prop:weakcompl})." | |

Page effect, measured on one snapshot of all sources: with my six files reverted to
`process/w7/sections-before-w7/`, the references start at the top of p. 68. With my changes they
start near the bottom of p. 67 (line 38 of 45). The total stays 127 pp.

## Cross-file requests

None.

## Commands run (targeted, local; not CI)

- Private build:
  `rm -rf /tmp/w7-exact-comp && mkdir -p /tmp/w7-exact-comp && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-exact-comp/ && cd /tmp/w7-exact-comp && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`.
  Exit 0, 127 pages. `out/main.log` has no errors, no undefined references or citations and
  no multiply defined labels. It has one overfull box (15.7pt, `sections/setting.tex` lines
  161-197, the notation table). That file is not mine and my changes do not touch it.
- Comparison build with my six files reverted (`/tmp/w7-exact-comp-base`, same snapshot of the
  other files). Page positions were read with `pdftotext -layout`.
- `pdftotext -layout` of the build. I read every changed passage in the rendered text (Section 6.5
  first and last paragraphs, Appendix B opening, Section 11.1, 11.3, 11.4, 11.6, and Appendix H
  items (b), E1-E3 and the chain table) and checked that Tables 3-6 keep their order.
- `python3 process/w7/checks/exact-comp-e3sep.py` (E3 with $\kappa_{\mathrm{target}}=2$: node
  formula confirmed for every $n$).
- Inline Python on `experiments/results/S1_ex_replay.csv` and `S1_localized.csv` (the five
  instances with the most EX stages are accepted; threshold stages 40-72 with the lemma constant
  and 139-157 with the code constant).
- `grep` over `sections/*.tex`: references to `tab:chain`, `sec:comp-impl` and the deleted 11.1
  items ("coordinate descent", "wrapper", "uniform'' grids", "q=4"); other code-availability
  sentences; British spellings and `non-` compounds in my files; `sec:polynomial`, `alg:ex` and
  `j_{\max}` usage.

No project-wide verification was run, and CI was not consulted.

## Verification

Independent verifier for group exact-comp. Checked against
`process/w7/sections-before-w7/` with `diff` and with the word-level comparison script
`process/w7/checks/exact-comp-verify-move.py`.

### What was checked

| Finding | Verdict | Check |
|---|---|---|
| F-referee-1(b) | correct | The script confirms that the `tab:chain` environment in appendix-computation.tex is word for word the old one (158 words) and that it is gone from computation.tex. It sits directly before the "Exact output (Section~\ref{sec:comp-exact})" paragraph, as in verify-F-referee-1.md. The 11.3 pointer reads "Table~\ref{tab:chain} in Appendix~\ref{app:computation}". 11.3 still reads without the table: it gives $m=2,4,\dots,64$, $n$ from 4 to 128, grid sizes 5 to 11, stages 9 to 74 and the bound $2^{m-1}$. All of these match the table. Rendered: Table 3 is at the top of p. 125, before Tables 4-6. The lead-in paragraph is sound. |
| F-referee-5 | correct | Checked independently with `S1_ex_replay.csv` and `S1_localized.csv`. The five instances with the most EX stages (542, 542, 542, 542, 534) are all accepted, and their lemma-constant threshold stages are 72, 70, 71, 54 and 40. The sentence agrees with 11.4 and with experiments/README.md. (The data hold the threshold stage for all 30 instances, with a maximum of 72, so the old sentence was not false. The new wording is still true and agrees with 11.4.) |
| F-consistency-1 | correct | E4 has $n=3,\dots,6$. Dropping "exact-output" is a sound simplification. The two experiment sentences of Section 6.5 now name E4 and S1, and both use the threshold of Proposition~\ref{prop:accept} with~\eqref{eq:exact-constants}. |
| F-consistency-2 | correct | "propositions" now matches Section 6.6 and the conclusion. |
| F-referee-2 | correct | Wording follows the coordinator decision. Keywords and MSC are in abstract.tex (another group). |
| F-proofread-13, -14 | correct | A scan of all six files for British spellings and hyphenated `non-` compounds found none. |
| F-dependencies-3 | correct | I reran `exact-comp-e3sep.py` and also read `max_nodes_free` and `mean_nodes_free` directly from `E3_stages.csv`. For all 18 uniform runs with $\kappa_{\mathrm{target}}=2$, in stages 7-10 the maximum and the mean both equal $4(\lfloor\sqrt{n/4}\rfloor+1)+1$ (9, 9, 13, 13, 21, 25). So "per free coordinate in the last four stages" is exact. "for E3" is needed because 11.2 reports $\kappa_{\mathrm{target}}=2$ for E2. The pointer to Section~\ref{sec:comp-growth} for separability is valid (11.2 states it for the generator). |
| F-dependencies-4 | correct | Lemma~\ref{lem:commonmesh} (growth.tex:318) defines $j_{\max}$ by the $\frac9{16}$ inequality. |
| O2 | correct | Every deleted clause appears in Appendix H: (c) center at the incumbent, (d) descent and its improvement after each stage, (f) "uniform" grids, (g) the EX height constant, $q=4$, doubling and restart. A grep of all `sections/*.tex` for `sec:comp-impl`, "wrapper", "coordinate descent", "descent start", "uniform'' grids" and `q=4` shows that the only later uses are 11.2 ("initial coordinate descent"), 11.3 ("first descent start", which is now $\ell$ by the kept sentence) and 11.4 (rewritten without "the wrapper"). No other file cites Section 11.1. Appendix H still lists seven items (a)-(g), so "seven ways" holds. EX is now first named in 11.1 with `(Algorithm~\ref{alg:ex})`, and Algorithm~\ref{alg:ex} defines $q$. |
| Appendix B opening | modified (see below) | |

I also checked the following:
- Labels: the 58 `\label`s in the six files before W7 are all still present, none is duplicated, and none was added.
- No proof moved in this group, so there was no proof to compare. The one moved block is the table, compared above.
- I read every edited passage in the rendered PDF: Section 6.5 (first and S1 paragraphs), the Appendix B opening, 11.1, 11.3, 11.4 (E4 and S1), 11.6 (E6), and Appendix H (b), E1-E3 and the chain. None has a dangling reference or a broken sentence.
- I compared the other W6 finding files against this group's files. No finding for these files is missing from the table above.

### What I fixed

1. **Appendix B opening (appendix-localized.tex).** The added sentence said that the two propositions show that "the margin term and strict complementarity in this theorem are needed". That claim is unscoped. Propositions~\ref{prop:margin} and~\ref{prop:weakcompl} show something narrower: this procedure's successes need large denominators, and without strict complementarity its sign and patch tests never succeed. The B.2 text itself says "needed for certificates of this form". The theorem also gives a procedure, not "an exact implicit output". The sentence now reads: "This appendix proves Corollary~\ref{cor:local} and, for the explicit polynomials of Section~\ref{sec:polynomial}, gives a procedure with exact implicit output when the minimizer may be irrational and lie on the boundary (Theorem~\ref{thm:boundary}), together with two propositions showing that this procedure needs the margin term in its cost bound and strict complementarity (Propositions~\ref{prop:margin} and~\ref{prop:weakcompl})."
2. **Appendix H chain lead-in (appendix-computation.tex).** "Table~\ref{tab:chain} gives the runs of CT" became "gives the results of CT". This matches "Table~\ref{tab:scip} gives the results of E5" and "Table~\ref{tab:recourse} gives the results", and a table reports results, not runs.

### Open

- None for this group. Cross-file requests: none.

### Build (private, targeted; not CI)

- `rm -rf /tmp/w7-exact-comp-verify && mkdir -p /tmp/w7-exact-comp-verify && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-exact-comp-verify/ && cd /tmp/w7-exact-comp-verify && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`
  - Run before and after my fixes. Both runs: exit 0, 127 pages.
  - `out/main.log` has no errors, no undefined references or citations, no multiply defined labels and no overfull boxes (the setting.tex overfull box from the editor's build is gone in the current snapshot).
  - The rendered text has no `??`. References start on p. 67 of this snapshot.
- `python3 process/w7/checks/exact-comp-verify-move.py`: PASS (table move word for word; no label lost or duplicated).
- `python3 process/w7/checks/exact-comp-e3sep.py` and inline Python on `E3_stages.csv`, `S1_ex_replay.csv` and `S1_localized.csv`.
- `grep` over `sections/*.tex` for the O2 items, cross-references to Section 11, British spellings, and `j_{\max}` in growth.tex.
