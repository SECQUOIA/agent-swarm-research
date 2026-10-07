# W7 report: recourse group

Files edited: `sections/recourse.tex`, `sections/recourse-convex.tex`,
`sections/recourse-cuts.tex`, `sections/recourse-mixed.tex`,
`sections/appendix-recourse-convex.tex`, `sections/appendix-recourse-cuts.tex`.
No changes were needed in `recourse-valuefn.tex`, `recourse-local.tex` or `recourse-balanced.tex`.

| Finding | Decision | What was done | Reason for any deviation |
|---|---|---|---|
| F-referee-1(a), Section 7 part (proof of `thm:cv`) | MODIFIED | Moved the proof word for word, as `\begin{proof}[Proof of Theorem~\ref{thm:cv}]`, to directly before "Proof of the exact-output part of Theorem~\ref{thm:cv}(iii)". In its (iii) paragraph, "...with this denominator bound; Appendix~\ref{app:recourse-convex} gives the procedure and its analysis." became "...with this denominator bound. The proof below gives the procedure and its analysis." Removed the proof from the main text and left "The proof is in Appendix~\ref{app:cv-proof}." after the statement. | Added the heading `\subsection{Proof of Theorem~\ref{thm:cv}}\label{app:cv-proof}` before the moved proof. That subsection (C.4) now holds both proofs of `thm:cv`. The main-text pointer goes to C.4, not to all of Appendix C, because Appendix C runs about 10 pages over 8 subsections. This matches the existing heading "Proof of Theorem~\ref{thm:valuefn}(b),(c)" (C.1) and the D.1 pointer below. No statement or label moved. The moved proof uses nothing undefined at its new place: `lem:cv-bits` and `lem:cv-height` now come before it in C.3, and everything else is cited explicitly. |
| F-referee-1(a), Section 7 part (proofs of `thm:cr-oracle`, `thm:cr-search`, `prop:cr-growth`) | MODIFIED | Moved the three proofs word for word, in this order, to a new first subsection of Appendix D, `\subsection{Proofs for Section~\ref{sec:cuts}}\label{app:cr-proofs}`, placed before "Exact output with a cut residual". Each starts with `\begin{proof}[Proof of Theorem/Proposition~\ref{...}]`. Each main-text proof was replaced by "The proof is in Appendix~\ref{app:cr-proofs}." | Two small additions. (1) D.1 opens with one sentence: "The proofs below use the bag-cell error $e_B(C)$ of Section~\ref{sec:local} with $B=\mathcal K$, and $e_j$, $\beta_V(C)$, $\mathcal Q_j$, $\mathcal Q_j'$, $\lambda_j$ and $U$ as in CORE (Algorithm~\ref{alg:core})." The reason: the proof of `thm:cr-search` uses $e_{\mathcal K}(C)$, which is defined in Section 7.2, outside the Section 7.4 notation that the appendix opening announces. (2) In the main text, "By (b), CORE stops at the latest..." now follows the pointer sentence rather than the theorem, so it became "By Theorem~\ref{thm:cr-search}(b), CORE stops at the latest...". `process/w7/checks/recourse-verbatim.py` confirms that all four moved proofs are word for word, except the documented (iii) pointer change. |
| F-proofread-4 | ACCEPTED | recourse.tex: "These are the main results." changed to "These are the main results of this section." | none |
| F-proofread-5 | ACCEPTED | recourse-convex.tex: deleted `\paragraph{Model.}` and `\paragraph{The recourse theorem.}`, each with the blank line after it. Definition 7.5 and Theorem 7.9 keep their titles. | none |
| F-proofread-6 | MODIFIED | recourse-mixed.tex: "with a certificate checkable by its part~(d) without optimization" changed to "with a certificate that can be checked without optimization (Proposition~\ref{prop:cr-greedy}(d))". | This removes the ambiguous "its", as the finding asks. The proposed wording "a certificate that part~(d) of Proposition~\ref{prop:cr-greedy} checks" first reads as "a certificate that [is] part (d)". The citation form `\ref{...}(d)` is the one the paper already uses. |
| F-dependencies-5 | MODIFIED | Replaced the opening of Appendix D with an informative opening. It lists what the appendix proves: Theorems `thm:cr-oracle` and `thm:cr-search` and Proposition `prop:cr-growth` of Section 7.4 (the new D.1), Theorem `thm:cr-exact`, the claims of Remark `rem:cr-mixed`, and the results deferred from Section 7.5. It then says that the first three subsections use the notation of Section 7.4, which is spelled out as before, and that the last uses that of Section 7.5. | The given text was written before D.1 existed. As the task requires, it now names the new subsection's results, and "the first two subsections" became "the first three subsections". |
| Roadmap and proof-location check (task item) | no change needed | The Section 7 roadmap (recourse.tex) gives no proof location except "Proposition~\ref{prop:star} in Appendix~\ref{app:recourse-convex}", which is unchanged. The other location sentences in my files still hold after the moves: recourse-local.tex:65, 67, 76; recourse-convex.tex (proof of `prop:vf-curv`(b), `prop:cert-exist`, `thm:cv-recog`, `prop:cv-limit`, the paragraph on Appendix C supplements); recourse-cuts.tex (`thm:cr-exact` in Appendix D); recourse-mixed.tex (`prop:cr-greedy` in Appendix D); recourse-balanced.tex:38, 89, 108-109 (Appendix D). The Appendix C opening ("proofs deferred from Sections~\ref{sec:valuefn}--\ref{sec:convexrecourse} and the supplementary results") covers the new C.4. Outside my files, no text cites the proof of any moved result (grep): conclusion.tex:33-34 and intro.tex cite only the statements. | none |

Effect on length: in the private build, Section 7 spans pp. 30-42, and Section 8 now starts on p. 42 instead of p. 43. In the build of the pre-W7 sources, Section 7 spans pp. 30-43. The total stays 127 pages.

## Cross-file requests

None.

## Commands run (targeted, local; not CI)

- Baseline build of the pre-W7 sources (copy of `process/w7/sections-before-w7/` in `/tmp/w7-recourse-base`): `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`. Exit 0, 127 pages, no overfull boxes, no undefined or multiply defined references.
- Private build after the edits: `rm -rf /tmp/w7-recourse && mkdir -p /tmp/w7-recourse && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-recourse/ && cd /tmp/w7-recourse && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`. Exit 0, 127 pages, no errors, no undefined or multiply defined references, no warnings. `main.aux` resolves the new labels: `app:cv-proof` = C.4 (p. 95) and `app:cr-proofs` = D.1 (p. 100). The log has one overfull `\hbox` (15.7pt), at `sections/setting.tex` lines 161-197 (the notation table). That file is not mine, and the baseline build did not have this warning, so it comes from another group's concurrent edit, not from this change.
- `pdftotext -layout` on pp. 33-42 and 95-101 to read the pointer sentences, the removed headings, and the new C.4 and D.1 as rendered.
- `python3 process/w7/checks/recourse-verbatim.py`: checks that the four moved proofs match the pre-W7 text word for word, except the documented (iii) pointer change, and that each moved proof left exactly one pointer sentence. All checks pass.
- Scratch extracts of the moved blocks: `process/w7/checks/recourse-thmcv-proof.tex` and `process/w7/checks/recourse-cr-proofs.tex`.

No project-wide verification was run. CI was not consulted.

## Verification

Independent verifier, W7. The full table is in `process/w7/reports/recourse-verify.md`.

What I checked:
- **Every assigned finding.** I compared all nine owned files with `process/w7/sections-before-w7/`.
  - F-referee-1(a), Section 7 part; F-proofread-4, -5 and -6; and F-dependencies-5 are applied as reported.
  - Every deviation is sound:
    - the C.4 heading and the `app:cv-proof` pointer;
    - the D.1 lead sentence;
    - "By Theorem~\ref{thm:cr-search}(b)";
    - the F-proofread-6 wording;
    - the extended D opening.
  - The C.4 pattern (a "Proof of ..." subsection followed by a titled proof) already occurs in B.1 and in the subsection with the proof of `prop:lbproduct`.
- **Moved proofs are word for word.** `process/w7/checks/recourse-verify-wordcmp.py` (new) compares the old and new proof bodies word by word.
  - `thm:cr-oracle`, `thm:cr-search` and `prop:cr-growth`: 0 differences.
  - `thm:cv`: 1 difference, the pointer change prescribed by verify-F-referee-1.md.
  - With the moved blocks masked, the per-file word diffs show only the documented edits.
  - All 64 pre-W7 labels are present exactly once, in the same file. The only new labels are `app:cv-proof` and `app:cr-proofs`.
  - Only the four proof environments moved.
- **Moved proofs are complete at their new place.** Every symbol, equation and result each proof uses is defined there or cited by an explicit `\ref`:
  - `lem:cv-bits` and `lem:cv-height` precede C.4;
  - `e_K(C)` is covered by `lem:cr-cell` and by the D.1 lead;
  - the CORE quantities are covered by the D opening and the D.1 lead.
- **Surrounding text.** All pointer sentences, the roadmap and the location sentences in the owned files read correctly and still point to the right place. There is no dangling "(b)", "below" or "the theorem". "The proof below" in the moved (iii) paragraph refers to the next proof environment, which is directly below it.
- **Build.** I ran a private build in `/tmp/w7-recourse-verify` with the prescribed command.
  - latexmk exits 0, and the PDF has 127 pages.
  - The log has no errors, no undefined or multiply defined references, no overfull or underfull boxes, and no warnings. The setting.tex overfull box mentioned above no longer occurs.
  - The new labels resolve to C.4 (p. 95) and D.1 (p. 100). §7 spans pp. 30-42.
  - I also read the rendered pp. 30-42 and 95-101.

What I fixed: nothing. No defect was found, so no owned file was changed in verification.

What remains open: nothing for this group. No cross-file requests.
