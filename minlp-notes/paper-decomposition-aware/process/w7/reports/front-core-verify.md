# W7 verification: front-core

Verifier for the group front-core. I compared every owned file with
`process/w7/sections-before-w7/` (`main.tex` and `macros.tex` have no backup
there. They are unchanged according to the editor's report, and the build
confirms that they work with the new sections). I checked each edit against
the W6 findings, the coordinator decisions and the current text around it. I
made no edits to the group's files, because I found no problem that needed a
fix.

| Finding | Editor's decision | Verifier verdict | Notes |
|---|---|---|---|
| F-referee-2 | MODIFIED | Correct | The keyword and MSC lines are inside `abstract`, before `\end{abstract}`, and render under the abstract on p. 1. The MSC 2020 titles of 90C26, 90C11, 90C20, 90C39, 90C60 and 68Q27 all fit the paper, so keeping all six is right. As decided, there is no author block and no declarations section. The code-availability sentence is already in `computation.tex:54-56` ("... together with the solver files they import, are provided as supplementary material"), so the editor's cross-file request is already met. |
| F-proofread-1 (abstract) | ACCEPTED | Correct | "computing an exact minimizer takes $f_1(p,\kappa)I^{O(1)}$ bit operations". |
| F-referee-3 + F-proofread-1 (conclusion) | MODIFIED | Correct | The text is F-referee-3's sentence with "maximum bag size $p$" (as in Theorem 1.1) and "EX (Algorithm~\ref{alg:ex})" (CONVENTIONS §2, first use in the section). Both deviations are sound. It says "bit operations" for both bounds. |
| F-referee-4 + F-consistency-5 | ACCEPTED | Correct | The intro sentence now reads "Every rational mixed box QP has \emph{set growth}" and defines $\mathcal S$, $g_S$ and $\kappa_S=\max\{1,L/g_S\}$. This matches Definition `def:growth` ($\kappa_S=\kappa(L,g_S)$) and Remark `rem:setgrowth`. $L$ is defined earlier in the intro (line 46), and `\dist` is a macro. The definition now comes before Table 1, "already when $\kappa_S=1$" and "Under set growth". The later duplicate definition was removed, and the "Several minimizers" sentence still reads correctly. |
| F-referee-6 | ACCEPTED | Correct | Both Table 1 cells were changed as proposed. The table renders without overflow. |
| F-proofread-2 | MODIFIED | Correct | "Table~\ref{tab:results} lists these results together with the extensions described below." Dropping "and lower bounds" is right: the table has no lower-bound rows, and its caption refers to Theorem 1.2 for them. As F-proofread-2 predicted, the table still floats into Theorem 1.2 on p. 4, but the reader now meets the reference first. |
| F-proofread-3 | ACCEPTED | Correct | "they enter only the running-time bounds, never the validity of the output." |
| F-proofread-11 | ACCEPTED | Correct | "$k$ color classes" now defines $k$ before "polynomial in $kN_0$", with the same meaning as in the proof in Appendix G.2 (`appendix-lbproduct.tex:77`). |
| F-proofread-12 | ACCEPTED | Correct | "It shows a limitation of filtered grids, not a hard problem". "It" refers to the proposition named in the sentence before. |
| F-proofread-14 (related.tex) | ACCEPTED | Correct | "nonasymptotic". A grep of all owned files finds no other `non-` compound and no British spelling. |
| F-consistency-3 | MODIFIED | Correct | Splitting the proposed row into two avoids the overfull table, and each row cites the theorem that defines its symbols: $f(p,t)$ in `thm:approx` (`growth.tex:210`), $f_1$ and $C_1$ in `thm:exact` (`exact.tex:349`). $\nu$ is defined in §7.3 (`recourse-convex.tex:238`), which is still main text after the move of the proof of `thm:cv`. The rows follow section order. The table renders inside the text width. |
| F-consistency-4 | ACCEPTED | Correct | "Theorem~\ref{thm:approx} covers". |
| F-dependencies-1 | ACCEPTED | Correct | Every item in the new opening sentence exists in Appendix A, in the order listed. The bit-length paragraph supports the pointer that is inside the proof of `thm:approx` (`growth.tex:259`). |
| F-dependencies-2 | ACCEPTED | Correct | All $R_j$, $R_1$ and $R_{j+1}$ in the uniform-rule paragraph are now $\rho_j$, $\rho_1$ and $\rho_{j+1}$. "with $h=1$ and $R_0=1$" and the graded rule's "$R_0=R$" are unchanged. "with $h=h_j$ and $R_0=\rho_j$" now reads correctly. No $R_j$ remains in the file. The name matches `lem:tu-uniform` (`appendix-tu.tex:486`). |
| Moved proofs: text in owned files | ACCEPTED (no change) | Correct | The owned files mention the eight results only as statements (Table 1, the intro paragraphs, the notation table, `growth-sharp.tex:54`, `limits.tex:467`, `limits.tex:540`, `conclusion.tex:35,60`). None of them cites one of the moved proofs. `limits.tex:540` cites "the discussion after Theorem~\ref{thm:tu-approx}", and that discussion is still in the main text (`constraints.tex`, after the new pointer sentence). The Organization paragraph ("the appendices ... contain the longer proofs and secondary results") still holds. |
| O2 | "REJECTED" (not in the group's files) | Not applicable | O2 is an edit to `computation.tex`, which this group does not own. The computation group has applied it (`computation.tex:23`). |

Moved proofs (other groups' files; checked because they bear on the owned
text). `process/w7/checks/front-core-verify-moved.py` compares, word by word,
each pre-W7 main-text proof with its new appendix copy. It also checks that a
pointer sentence follows each statement in the main text.
- Six proofs are word-identical: `thm:cr-oracle`, `thm:cr-search`,
  `prop:cr-growth`, `prop:tu-sound`, `thm:tu-states` and `thm:cells`.
- Two proofs differ only by the required pointer changes:
  - `thm:cv`: "bound; Appendix~\ref{app:recourse-convex}" became "bound. The
    proof below". This is the corrected fix of `verify-F-referee-1.md`.
  - `thm:tu-approx`: "above," became "of Section~\ref{sec:tu-filter},". The old
    "above" would point to the wrong place in the appendix.
- Each statement keeps its label in the main text. Each is followed by "The proof is in
  Appendix~\ref{...}.", and no proof remains in the main text.

## Cross-file requests

None. The editor's one request (the code-availability sentence in
`computation.tex`) is already done.

## Commands run (targeted, local; not CI)

- `diff process/w7/sections-before-w7/<f>.tex sections/<f>.tex` for all 14
  owned section files.
- A `comm` check that no `\label`, `\ref`, `\eqref` or `\cite` key was lost
  from any owned file. None was lost.
- `grep` of the owned files:
  - the eight labels whose proofs moved;
  - "Appendix", "proof of", "proved in" and "main text";
  - `non-` and British spellings;
  - `R_j` and `\rho`;
  - the definitions of $\nu$, $f(p,t)$, $f_1$ and $L$.
- `python3 process/w7/checks/front-core-verify-moved.py`, which exits with
  status 0.
- Private build: `rm -rf /tmp/w7-front-core-verify && mkdir -p /tmp/w7-front-core-verify && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-front-core-verify/ && cd /tmp/w7-front-core-verify && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`.
  - It exits with status 0 and gives 127 pages.
  - `grep -i 'undefined|multiply|overfull|^!' out/main.log` finds nothing, and
    `main.log` has no warnings at all.
  - This build includes the other groups' in-progress edits.
- `pdftotext -layout out/main.pdf` to inspect the rendered text:
  - the abstract with the keyword and MSC lines;
  - the set-growth paragraph;
  - Table 1;
  - the notation table;
  - the conclusion;
  - the opening of Appendix A.

No project-wide verification was run. CI was not consulted.
