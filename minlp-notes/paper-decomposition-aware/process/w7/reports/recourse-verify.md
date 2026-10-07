# W7 verification report: recourse group

Verifier for `sections/recourse.tex`, `recourse-valuefn.tex`, `recourse-local.tex`,
`recourse-convex.tex`, `recourse-cuts.tex`, `recourse-mixed.tex`, `recourse-balanced.tex`,
`appendix-recourse-convex.tex`, `appendix-recourse-cuts.tex`. Editor's report:
`process/w7/reports/recourse.md`, which now ends with a `## Verification` section.

The verdict column rates the editor's decision. No source file needed a correction.

| Finding | Verdict on editor's decision | What I checked | Deviation reason sound? |
|---|---|---|---|
| F-referee-1(a), Section 7: proof of `thm:cv` | MODIFIED, confirmed | The proof is word for word the pre-W7 proof. The only exception is the pointer change in (iii) prescribed by verify-F-referee-1.md: "bound; Appendix~\ref{app:recourse-convex}" became "bound. The proof below". The proof sits directly before "Proof of the exact-output part of Theorem~\ref{thm:cv}(iii)". Every symbol and result it uses is defined in Def. `def:cv-model`, in the statement, or by an explicit `\ref`. `lem:cv-bits` and `lem:cv-height` precede it. The main text keeps the statement and label, followed by "The proof is in Appendix~\ref{app:cv-proof}." The rendered text reads "Appendix C.4". | Yes. Without the new heading, the proof would sit at the end of C.3, "Certificates: energy, existence, evaluation and height", where a reader would not look for it. The heading followed by a titled proof environment has precedents in B.1 (`cor:local`) and in the subsection with the proof of `prop:lbproduct`. The C opening ("proofs deferred from Sections 7.1-7.3") covers C.4. |
| F-referee-1(a), Section 7: proofs of `thm:cr-oracle`, `thm:cr-search`, `prop:cr-growth` | MODIFIED, confirmed | All three proofs are word for word the pre-W7 proofs (0 word differences each). They appear in this order in the new D.1, `\subsection{Proofs for Section~\ref{sec:cuts}}\label{app:cr-proofs}`, before "Exact output with a cut residual". Each statement and label stays in the main text, followed by "The proof is in Appendix~\ref{app:cr-proofs}." Everything the proofs use is defined at D.1: `e_K(C)` through the explicit `lem:cr-cell`, the CORE quantities through the D opening and the D.1 lead sentence, and `thm:cr-filter` and `prop:cr-cut` through explicit refs. | Yes. "By (b), CORE stops" would dangle after the pointer sentence, so it had to become "By Theorem~\ref{thm:cr-search}(b)". The one-sentence D.1 lead is accurate: `e_B(C)` is defined in Section 7.2, before `lem:cr-cell`. It is short and not filler. |
| F-proofread-4 | ACCEPTED, confirmed | recourse.tex:25 reads "These are the main results of this section." | n/a |
| F-proofread-5 | ACCEPTED, confirmed | Both `\paragraph` lines and their blank lines are deleted. In the PDF, Definition 7.5 and Theorem 7.9 follow the preceding paragraphs directly, and no heading stands alone. | n/a |
| F-proofread-6 | MODIFIED, confirmed | It now reads "with a certificate that can be checked without optimization (Proposition~\ref{prop:cr-greedy}(d))". Part (d) of `prop:cr-greedy` is in fact the check without optimization. | Yes. The proposed "a certificate that part~(d) of ... checks" is a garden-path sentence. The new text removes the ambiguous "its", as the finding asks. |
| F-dependencies-5 | MODIFIED, confirmed | The new opening names `thm:cr-oracle`, `thm:cr-search`, `prop:cr-growth` (the new D.1), `thm:cr-exact`, `rem:cr-mixed` and the results deferred from Section 7.5. "The first three subsections" is right: D.1-D.3 use the Section 7.4 notation and D.4 uses that of Section 7.5. | Yes. The given text predates D.1, and the task required that D.1 be mentioned. |
| Roadmap / proof-location check | no change needed, confirmed | Every "Appendix" or "proof is in" sentence in the owned files still points to the right place: recourse.tex:29; recourse-local.tex:65, 67, 76; recourse-valuefn.tex:114; recourse-convex.tex:126, 156, 172, 215, 235, 246, 278; recourse-cuts.tex:116, 186, 204, 234; recourse-mixed.tex:20; recourse-balanced.tex:38, 89, 109. Outside the owned files, only conclusion.tex:36 and limits.tex:546 cite these appendices, for `cor:cv-nu` and `prop:star`, and both are unaffected. No text cites the proof of a moved result. | n/a |

## Cross-file requests

None.

## Commands run (targeted, local; not CI)

- `diff process/w7/sections-before-w7/<f> sections/<f>` for all nine owned files.
- `python3 process/w7/checks/recourse-verify-wordcmp.py` (new). It runs four checks:
  - a word-level comparison of the four moved proofs: 1 difference in `thm:cv`, the prescribed pointer change, and 0 in the other three;
  - a word-level diff of every owned file with the moved blocks masked, which shows only the documented edits;
  - a label check: 64 old labels all present exactly once in the same file, plus the two new ones, `app:cv-proof` and `app:cr-proofs`;
  - environment counts, where only the four proof environments moved.

  Result: OK.
- `python3 process/w7/checks/recourse-verbatim.py` (editor's script), rerun: all checks pass.
- `grep` for every reference to the moved results and to `app:recourse-convex`, `app:recourse-cuts`, `app:cv-proof` and `app:cr-proofs` in `sections/*.tex` and `main.tex`.
- Private build: `rm -rf /tmp/w7-recourse-verify && mkdir -p /tmp/w7-recourse-verify && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-recourse-verify/ && cd /tmp/w7-recourse-verify && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`.
  - Exit 0, 127 pages.
  - The log has no errors, no undefined or multiply defined references, no overfull or underfull boxes, and no warnings.
  - `main.aux`: `app:cv-proof` = C.4 (p. 95), `app:cr-proofs` = D.1 (p. 100), §7 at pp. 30-42, §8 from p. 42.
- `pdftotext -layout` on pp. 30-42 and 95-101 to read every edited passage as rendered.

No project-wide verification was run. CI was not consulted.
