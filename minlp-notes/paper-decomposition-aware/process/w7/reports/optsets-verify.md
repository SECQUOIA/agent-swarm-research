# W7 verification report: optsets (sections/optsets.tex, sections/appendix-proximal.tex)

Verifier for the edits described in `process/w7/reports/optsets.md`. All checks
compare against `process/w7/sections-before-w7/`.

| Finding | Editor's decision | Verdict | What I checked or did | Reason for any deviation |
|---|---|---|---|---|
| F-referee-1(a), Section 9 part (corrected fix in verify-F-referee-1.md) | ACCEPTED | ACCEPTED, no change | The main text has "The proof is in Appendix~\ref{app:cells}." right after Theorem `thm:cells`. The proof is the first subsection of Appendix F, `\subsection{Uniform cells}\label{app:cells}`, and opens with `\begin{proof}[Proof of Theorem~\ref{thm:cells}]`. My word-level script finds 267 tokens before and after, all identical. The moved proof contains no `\label`. It cites `lem:cells`, `lem:dp`, `sec:exact-data`, `thm:transfer` and `thm:exact` by `\ref`. The context sentence the editor added before the proof points to UC and to the stage-cell paragraph after it (Section 9.1). Those are the sources of step (iii), $\mathcal G_{ij}$, $h_j$, $J$, $y^{(j)}$, $m_i$ and the facts about stage-cell lengths, spacing and interior points that the proof uses. All other symbols are global or come from the theorem statement. The surrounding main text reads correctly, and no other file refers to the proof's old location (`growth-sharp.tex:54`, `limits.tex:467`, `intro.tex:175,311` and `setting.tex:181` cite only the theorem). | Not a deviation; the context sentence is outside the proof environment and is needed so that the proof reads correctly at its new place. Open point for the coordinator: F.1 (thm:cells) now comes before F.2 (prop:twocenters), although Section 9.1 states prop:twocenters first. The coordinator and the corrected fix both required "first subsection", so I kept that order. |
| F-proofread-9 | ACCEPTED | ACCEPTED, no change | optsets.tex:65-67 matches the replacement text exactly and renders correctly (p. 49). | None. |
| F-proofread-10 | ACCEPTED | MODIFIED (layout only) | The pointer was moved below `\end{lemma}` as required, but with no blank line, so LaTeX set it as an unindented continuation. In 18 of the other 20 places in the paper, a blank line separates `\end{...}` from "The proof is in ...". I added the blank line (optsets.tex:342). The pointer now renders upright and indented, like the others (p. 53). | The finding's replacement block shows no blank line. I followed the paper's dominant convention instead, for consistent typesetting. |
| F-proofread-15 | ACCEPTED | ACCEPTED, no change | The title is now `\section{Proofs and supplements for Section~\ref{sec:optsets}}\label{app:proximal}`, which matches Appendix G's title pattern. No other file quotes the old title. The intro's "Organization" paragraph does not name appendix titles. | None. |
| F-dependencies-6 | MODIFIED | MODIFIED, no change | (1) The new opening lists everything the finding names. As the coordinator required, it also says that the appendix starts with the proof of Theorem `thm:cells`. Splitting it into two sentences reads better than the finding's single sentence. (2) The `\paragraph{Uniqueness in $\mathfrak D$ is coNP-hard.}` heading follows the paper's `\paragraph` style (title ending with a period). It renders as the last paragraph of Appendix F, just before Appendix G (p. 116). The build log has no hyperref token warnings. (3) The pointer in optsets.tex:432-433, "last paragraph of Appendix~\ref{app:proximal}", is accurate. | The editor's reasons (the coordinator's requirement, and readability) are sound. |

Labels and statements: the two files keep all 28 pre-W7 labels and every theorem-like environment. The only new label is `app:cells`. Reference counts changed only by the added references (`alg:uc`, `app:cells`, plus one more each of `ex:diagtilt`, `sec:exact-nonunique` and `thm:cells`).

## Cross-file requests

None.

## Commands run

All are targeted checks. CI checks were not run or inspected.

- `diff -u process/w7/sections-before-w7/optsets.tex sections/optsets.tex` and the same for `appendix-proximal.tex`: only the edits listed above.
- `python3 process/w7/checks/optsets-verify-moved-proof.py`: compares the pre-W7 proof of `thm:cells` with the moved proof, word by word. Result: `IDENTICAL` (267 tokens each). It also lists the references and labels in the moved proof.
- awk/grep scan of `sections/*.tex` for "The proof is in" directly after `\end{lemma|theorem|proposition|corollary}`: 18 places with a blank line, 2 without (optsets.tex, now fixed; recourse-local.tex:65, which another group owns and which predates W7).
- `diff` of the sorted `\label`, environment and `\ref` lists of both files, before vs. after.
- `grep` across `sections/*.tex` and `main.tex` for `thm:cells`, `app:cells`, `app:proximal` and the old appendix title.
- Private build: `rm -rf /tmp/w7-optsets-verify && mkdir -p /tmp/w7-optsets-verify && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-optsets-verify/ && cd /tmp/w7-optsets-verify && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`. Result: exit 0. `main.log` contains no warnings of any kind: no errors, undefined references, multiply defined labels, overfull boxes or hyperref token warnings. `app:cells` is F.1 on p. 111, and `thm:cells` is Theorem 9.4 on p. 50.
- `pdftotext -layout` on pp. 48-54 and 111-117: checked the rendered Appendix F opening, the F.1 heading, the context sentence and the proof, the coNP paragraph, and the main-text pointers.
