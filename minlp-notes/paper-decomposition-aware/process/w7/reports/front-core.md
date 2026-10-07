# W7 report: front-core

Files edited: `sections/abstract.tex`, `sections/intro.tex`, `sections/related.tex`,
`sections/setting.tex`, `sections/growth.tex`, `sections/limits.tex`,
`sections/conclusion.tex`, `sections/appendix-growth.tex`. I did not need to change
`main.tex`, `macros.tex`, `appendix.tex`, `setting-growthcert.tex`, `grids.tex`,
`growth-sharp.tex`, `appendix-lbproduct.tex` or `appendix-moments.tex`.

| Finding | Decision | What was done; reason for any deviation |
|---|---|---|
| F-referee-2 (keywords, MSC) | MODIFIED | Added the proposed keyword line and MSC 2020 line before `\end{abstract}`. I checked all six codes against the official MSC 2020 list (msc2020.org/MSC_2020.pdf): 90C26 "Nonconvex programming, global optimization", 90C11 "Mixed integer programming", 90C20 "Quadratic programming", 90C39 "Dynamic programming", 90C60 "Abstract computational complexity for mathematical programming problems", 68Q27 "Parameterized complexity, tractability and kernelization". All six fit the paper, so none was dropped. As the coordinator decided, there is no author block and no declarations section. The code-availability sentence is in `computation.tex`, which I do not own (see Cross-file requests). |
| F-proofread-1 (abstract) | ACCEPTED | "an exact minimizer takes $f_1(p,\kappa)I^{O(1)}$" became "computing an exact minimizer takes $f_1(p,\kappa)I^{O(1)}$ bit operations". |
| F-referee-3 + F-proofread-1 (conclusion) | MODIFIED | Used F-referee-3's sentence, which already says "bit operations". Two changes: "bag size $p$" became "maximum bag size $p$", to match Theorem 1.1 and the definition of $p$. "EX" became "EX (Algorithm~\ref{alg:ex})", because CONVENTIONS §2 asks for the algorithm reference at first use in a section, and this is EX's first use in the conclusion. |
| F-referee-4 + F-consistency-5 (intro set growth) | ACCEPTED | Replaced intro.tex 118-123 with F-referee-4's text, which starts "Every rational mixed box QP has \emph{set growth}" (F-consistency-5's qualifier, as in Remark `rem:setgrowth`) and defines $g_S$, $\mathcal S$ and $\kappa_S$. Removed the later definition of $\kappa_S$ in the "Several minimizers" paragraph, so the sentence now ends "where $r$ bounds the number of optimal values of a coordinate (Theorem~\ref{thm:cells})". $\kappa_S$ and "set growth" are now defined before Table 1 and before their uses at the old lines 256 and 293. |
| F-referee-6 (Table 1 cells) | ACCEPTED | "output: all minimizers" became "output: a description of the optimal set", and "outputs also the optimal set" became "outputs also an exact description of the optimal set". |
| F-proofread-2 (first reference to Table 1) | MODIFIED | Added the sentence at the end of the set-growth paragraph, just before the table environment, but wrote "Table~\ref{tab:results} lists these results together with the extensions described below." I dropped "and lower bounds", which the proposed text had: the table does not list the lower bounds, and its caption sends the reader to Theorem~\ref{thm:intro-lower} for them. |
| F-proofread-3 | ACCEPTED | "they bound only the running time" became "they enter only the running-time bounds, never the validity of the output". |
| F-proofread-11 (limits.tex) | ACCEPTED | "It encodes multicolored clique with $k$ color classes in the standard way, ...". $k$ is now defined before "polynomial in $kN_0$", and it has the same meaning as in Appendix G.2. |
| F-proofread-12 (limits.tex) | ACCEPTED | "It is a limit of filtered grids, not of the problem" became "It shows a limitation of filtered grids, not a hard problem". |
| F-proofread-14 (related.tex part) | ACCEPTED | "non-asymptotic" became "nonasymptotic". A grep found no other `non-` compounds, and no "modelled" or "labelled", in my files. The `computation.tex` and `constraints.tex` parts belong to other groups. |
| F-consistency-3 (notation table) | MODIFIED | Added the row for $\nu$, with the proposed text and `\S\ref{sec:convexrecourse}`. I split the proposed row for $f(p,t)$, $f_1$, $C_1$ into two rows: "$f(p,t)$ & function in the time bound of CT (not a factor $f_a$) & Thm.~\ref{thm:approx}" and "$f_1$, $C_1$ & function and exponent in the time bound of EX & Thm.~\ref{thm:exact}". Reason: the single row made the `lll` table 15.7pt too wide, mainly because of the third column "Thms. 5.7, 6.14" (I measured this with `process/w7/checks/front-core-tablewidth.tex`). Splitting also ties each symbol to its own theorem. I put the rows in section order (after the §6 rows and after the §7 row) rather than before `\bottomrule`, because the table follows section order. |
| F-consistency-4 (growth.tex) | ACCEPTED | "the theorem covers" became "Theorem~\ref{thm:approx} covers". |
| F-dependencies-1 (Appendix A opening) | ACCEPTED | Inserted the proposed sentence after the heading. I checked that each listed item is in the appendix: Lemma `lem:graded`, the $K(\theta,n_P)$ bound, the "Bit lengths in Theorem~\ref{thm:approx}" paragraph, Lemma `lem:commonmesh`, Proposition `prop:sharp`, Corollary `cor:uniformgrid`, and Examples `ex:family` and `ex:chain`. |
| F-dependencies-2 (rename to $\rho_j$) | ACCEPTED | In the "Uniform rule, filtered box" paragraph of the proof of Corollary `cor:uniformgrid`, $R_j$, $R_1$ and $R_{j+1}$ became $\rho_j$, $\rho_1$ and $\rho_{j+1}$. "with $h=1$ and $R_0=1$" and the graded rule's "$R_0=R$" are unchanged. The name now matches the proof of `lem:tu-uniform` (appendix-tu.tex:399). The $\rho$ in the proofs of `lem:states` and `lem:commonmesh` is local to those proofs, so there is no clash. |
| Moved proofs (thm:cv, thm:cr-oracle, thm:cr-search, prop:cr-growth, prop:tu-sound, thm:tu-states, thm:tu-approx, thm:cells): text about where proofs are | ACCEPTED (no change needed) | I grepped all my files for references to these results and for "proof", "proved in", "main text" and "argument of". The Organization paragraph says "The appendices follow the order of the sections and contain the longer proofs and secondary results", and "Sections~\ref{sec:grids}--\ref{sec:exact} prove Theorem~\ref{thm:intro-main}". Both still hold after the moves. No text in my files (intro, conclusion, related, limits, Table 1, notation table, growth-sharp) cites the proof of a moved result or says that it is in the main text. |
| O2 (shorten the list in §11.1) | not in my files | This edit is in `computation.tex`. I made no change. |

## Cross-file requests

1. `sections/computation.tex` (F-referee-2, as the coordinator decided; skip this if it is already assigned to the computation group). Replace the sentence "Code, inputs, raw results and reproduction scripts (one command per experiment group) accompany the paper." with a sentence saying that the code, inputs, raw results and reproduction scripts (one command per experiment group), together with the solver files they import, are provided as supplementary material.

No other file outside my group needs a change because of my edits. None of my edits removes or renames a label.

## Commands run (targeted, local; not CI)

- Read the W6 findings, `verify-F-referee-1.md`, CONVENTIONS and CUTPLAN. Ran `sed`/`grep` over my files around each finding before applying it.
- Checked the MSC 2020 titles: downloaded `https://msc2020.org/MSC_2020.pdf`, then ran `pdftotext` and grepped for the six codes. All titles were confirmed.
- `grep` over my files for references to the results with moved proofs and for text about where proofs are (none found that needs a change), for `non-`/`modelled`/`labelled`, and for `\nu`, `R_j` and `rho`.
- Applied the `$\rho_j$` rename with `sed` restricted to the "Uniform rule, filtered box" paragraph, then inspected the result.
- Measured table column widths in a scratch document (`process/w7/checks/front-core-tablewidth.tex`, compiled in `/tmp/w7-front-core`).
- Private build, 3 runs (the last one is the final state):
  `rm -rf /tmp/w7-front-core && mkdir -p /tmp/w7-front-core && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-front-core/ && cd /tmp/w7-front-core && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`.
  - First run: one overfull box (15.7pt) in the notation table. I fixed it as described under F-consistency-3.
  - Final run: exit 0, 127 pages. `grep -i 'undefined|multiply|overfull|^!' out/main.log` finds nothing.
- `pdftotext -layout out/main.pdf` to inspect the rendered abstract (keywords and MSC lines), the intro set-growth paragraph, Table 1, the notation table, the conclusion, Section 10 and the opening of Appendix A.
  - In this build, which includes the other groups' in-progress edits, the conclusion starts on p. 66 and the references on p. 68.

No project-wide verification was run. CI was not consulted.

## Verification

Independent verifier. The full table is in `process/w7/reports/front-core-verify.md`.

Checked:
- I diffed every owned section file against `process/w7/sections-before-w7/`.
  - Each edit matches its W6 finding and the coordinator's decisions.
  - The text around each edit reads correctly. There is no dangling "the
    theorem" or "below", and no broken sentence.
  - No `\label`, `\ref`, `\eqref` or `\cite` key was lost.
- The deviations have sound reasons:
  - "maximum bag size" and "EX (Algorithm~\ref{alg:ex})" in the conclusion;
  - "and lower bounds" dropped from the Table 1 reference;
  - the notation-table row split in two, to avoid an overfull box and to cite
    the right theorems.
- All six MSC 2020 codes fit the paper.
- $\kappa_S$ and set growth are now defined before their first use in the
  intro and in Table 1. The definition matches Definition `def:growth` and
  Remark `rem:setgrowth`.
- The $\rho_j$ rename is complete, and the two $R_0$ uses that must stay are
  unchanged.
- The Appendix A opening sentence lists exactly what the appendix contains.
- Moved proofs. `process/w7/checks/front-core-verify-moved.py` compares them
  word by word.
  - Six of the eight proofs are word-identical.
  - The other two (`thm:cv` and `thm:tu-approx`) differ only by the required
    pointer changes.
  - Each statement in the main text is followed by "The proof is in
    Appendix~\ref{...}."
  - No owned file cites one of the moved proofs or says that it is in the main
    text. The "discussion after Theorem~\ref{thm:tu-approx}" cited at
    `limits.tex:540` is still in the main text.
- Private build in `/tmp/w7-front-core-verify` (with the other groups'
  in-progress edits): exit 0, 127 pages. `main.log` has no errors, undefined
  references, multiply defined labels, overfull boxes or other warnings.

Fixed: nothing; no problem was found in the group's files.

Open:
- No open problems.
- The cross-file request for `computation.tex` is already done:
  `computation.tex:54-56` now says the material, "together with the solver
  files they import", is "provided as supplementary material".
- O2 belongs to the computation group, not to this group. The computation
  group applied it (`computation.tex:23`).
