# W7 report: optsets (sections/optsets.tex, sections/appendix-proximal.tex)

| Finding | Decision | What I did | Reason for any deviation |
|---|---|---|---|
| F-referee-1(a), Section 9 part (corrected fix in verify-F-referee-1.md) | ACCEPTED | Replaced the proof of `thm:cells` (old optsets.tex:148-186) by "The proof is in Appendix~\ref{app:cells}." Inserted the proof as the new first subsection of Appendix F, `\subsection{Uniform cells}\label{app:cells}`, opening with `\begin{proof}[Proof of Theorem~\ref{thm:cells}]`. The proof body is unchanged (checked with `diff`, 37 identical lines). Before the proof I added one context sentence: "We use the notation of UC (Algorithm~\ref{alg:uc}) and the properties of its stage cells stated after it in Section~\ref{sec:exact-nonunique}." | No deviation from the fix. The context sentence follows the existing pattern of Appendix F ("As in Section~\ref{sec:diagcert}, ..."). It is needed because the moved proof uses "step~(iii)", $\mathcal G_{ij}$, $h_j$, $J$, $y^{(j)}$ and the facts about stage-cell lengths and spacing from the paragraph after UC; it does not cite these explicitly. All other lemmas and sections it uses (`lem:cells`, `lem:dp`, `sec:exact-data`, `thm:transfer`, `thm:exact`) are cited by `\ref`. Note: as instructed, the uniform-cells proof is F.1, before "One center and two minimizers" (F.2). In the main text, `prop:twocenters` comes before `thm:cells`, so swapping F.1 and F.2 would follow section order exactly. I left the order as instructed. |
| F-proofread-9 | ACCEPTED | optsets.tex:65-67 now reads "...; the proposition shows that the failure comes from the single center, not from conditioning." | None. |
| F-proofread-10 | ACCEPTED | Moved "The proof is in Appendix~\ref{app:proximal}." from inside Lemma `lem:diagcert` to the line after `\end{lemma}`. It is now set upright, after the statement. | None. |
| F-proofread-15 | ACCEPTED | Appendix F title is now `\section{Proofs and supplements for Section~\ref{sec:optsets}}\label{app:proximal}`. | None. The intro's "Organization" paragraph does not quote appendix titles, so no other file needs a change. |
| F-dependencies-6 | MODIFIED | (1) New opening of Appendix F: "This appendix contains the proofs for Section~\ref{sec:optsets}, starting with the proof of Theorem~\ref{thm:cells} on uniform cells. It also contains Example~\ref{ex:diagtilt} of tilted and disconnected optimal sets in $\mathfrak D$, the lemma on proximal stages used by DISC (Algorithm~\ref{alg:disc}), Proposition~\ref{prop:sshard} on the hardness of discovery within $\mathfrak D$, and, in its last paragraph, the proof that deciding uniqueness of a given minimizer in $\mathfrak D$ is coNP-hard." (2) Added `\paragraph{Uniqueness in $\mathfrak D$ is coNP-hard.}` before the closing paragraph. (3) optsets.tex now says "coNP-hard (last paragraph of Appendix~\ref{app:proximal})". | The coordinator required the opening to mention the new uniform-cells subsection, so I added it. I split the finding's single long sentence into two for readability; the content is otherwise the finding's text. |

## Cross-file requests

None.

## Commands run

All are targeted checks. CI checks were not run or inspected.

- `sh process/w7/checks/optsets-moved-proof.sh`: diffs the pre-W7 proof (sections-before-w7/optsets.tex:149-185) against the moved proof in appendix-proximal.tex. Result: identical, 37 lines.
- `diff process/w7/sections-before-w7/optsets.tex sections/optsets.tex`: shows only the four intended edits.
- Private build: `rm -rf /tmp/w7-optsets && mkdir -p /tmp/w7-optsets && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-optsets/ && cd /tmp/w7-optsets && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`. Result: exit 0, PDF built.
  - My files have no errors, undefined references, multiply defined labels, overfull boxes or hyperref token warnings. `app:cells` resolves to F.1, p. 111.
  - Two warnings come from files other groups are editing, not from my changes:
    - undefined reference `app:cv-proof` at recourse-convex.tex:215;
    - an overfull hbox of 1.39pt in appendix-tu.tex, lines 515-518.
- `pdftotext` of the build: checked the rendered Appendix F opening, the F.1 heading and context sentence, the coNP paragraph heading, and the main-text pointers. In this build, Section 9 is on pp. 49-54 and Appendix F on pp. 110-115.

## Verification

The independent verifier's full report is `process/w7/reports/optsets-verify.md`.

Checked:
- Each assigned finding (F-referee-1(a) Section 9 part, F-proofread-9, F-proofread-10, F-proofread-15, F-dependencies-6), checked against the W6 findings, the corrected fix in `process/w6/verify-F-referee-1.md` and the coordinator decisions. All are handled correctly. The one deviation (F-dependencies-6: the uniform-cells mention and the split into two sentences) has a sound reason.
- The moved proof of `thm:cells`, checked with `process/w7/checks/optsets-verify-moved-proof.py`. It is identical word for word: 267 tokens, no differences. It starts with `\begin{proof}[Proof of Theorem~\ref{thm:cells}]` and contains no label. At its new place, every symbol it uses is defined or referenced: the added context sentence points to UC and to the stage-cell paragraph in Section 9.1, and all lemmas and sections are cited by `\ref`.
- The text around each edit reads correctly, with no dangling words or broken sentences. No label, statement or result was lost: the label and environment lists before and after differ only by the new `app:cells`. No other file depends on the old proof location or the old appendix title.
- Private build in `/tmp/w7-optsets-verify`: exit 0, and `main.log` has no warnings of any kind (no errors, undefined references, multiply defined labels, overfull boxes or hyperref token warnings).

Fixed:
- optsets.tex:341-342: added a blank line between `\end{lemma}` and "The proof is in Appendix~\ref{app:proximal}." (F-proofread-10). Without it, LaTeX set the pointer as an unindented continuation. With it, the pointer matches the 18 other places that have a blank line before the pointer sentence.

Open:
- Order within Appendix F: F.1 (proof of `thm:cells`) comes before F.2 (proof of `prop:twocenters`), but Section 9.1 states `prop:twocenters` first. This order was kept because the coordinator and the corrected fix both require the uniform-cells proof to be the first subsection. Swapping the two would follow section order exactly; the opening sentence of Appendix F would then need "starting with" removed. The decision is the coordinator's.
- Not in this group's files, and not caused by this group: recourse-local.tex:65 also has its pointer sentence directly after `\end{theorem}` with no blank line. This is a cosmetic difference that predates W7.
