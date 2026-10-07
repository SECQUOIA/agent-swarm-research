# W7 verification report: group tu (sections/constraints.tex, sections/appendix-tu.tex)

The verifier checked the editor's work against process/w7/sections-before-w7/. No change to the group's files was needed. The Decision column gives the final status of each finding as applied by the editor. The Verification column gives what I checked and found.

| Finding | Decision | Verification | Reason for deviation (confirmed) |
|---|---|---|---|
| F-referee-1(a), Section 8 part | MODIFIED | Confirmed, no change. The proofs of `prop:tu-sound` and `thm:tu-states` are identical word for word in E.2 (318 and 150 words). The proof of `thm:tu-approx` differs only by the pointer change. The subsection title, label, position and Appendix E opening match verify-F-referee-1.md. All 23 labels of constraints.tex stay in place. The proofs of `lem:tu-round` and `lem:tu-allow` stay in the main text. All references and symbols in the moved proofs resolve. | (1) "the tree computation above" became "the tree computation of Section~\ref{sec:tu-filter}". This is needed because "above" would point into Appendix E. (2) The Appendix E title now includes "proofs". This is accurate, matches the retitled Appendix D, and leaves the label unchanged. |
| F-proofread-7 | ACCEPTED | Confirmed, no change. The text matches the given replacement, and (8.4) sits beside the display (p. 47). | None. |
| F-proofread-8 | ACCEPTED | Confirmed, no change. The text matches the given replacement and reads correctly in Remark 8.11 (p. 48). | None. |
| F-proofread-14 (constraints.tex part) | MODIFIED | Confirmed, no change. "nonuniform" now appears 3 times in constraints.tex, including the Section 8.7 title, and the label `sec:tu-limits` is unchanged. No "non-uniform" remains in sections/. | The appendix-tu.tex heading had the same spelling and was fixed too. A separate private build confirmed that the original word order then gives a 1.39pt overfull box. The reordered sentence removes it and keeps the meaning. |

## Cross-file requests

None.

## Commands run

- `diff process/w7/sections-before-w7/{constraints,appendix-tu}.tex sections/...`
- `python3 process/w7/checks/tu-verify-wordcmp.py`: a whole-file word diff of both files, a word comparison of the three moved proofs, a label check for both files, and a reference check for the moved proofs. Result: only the intended differences; one pointer change; all labels present once; no undefined targets.
- `grep` over sections/ for references to the moved results and to `app:tu`, `app:tu-proofs` and the Section 8 subsections; for relative pointers ("above", "below", "next two"); for hard-coded appendix numbers; and for "non-uniform".
- `rm -rf /tmp/w7-tu-verify && mkdir -p /tmp/w7-tu-verify && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-tu-verify/ && cd /tmp/w7-tu-verify && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`: exit 0, 127 pages. The whole log has 0 errors, 0 undefined references, 0 multiply defined labels, 0 overfull or underfull boxes and no hyperref warnings.
- A copy of that build with the original "Nonuniform alternatives." sentence order (/tmp/w7-tu-verify-alt, since deleted): "Overfull \hbox (1.3938pt too wide)" at appendix-tu.tex lines 515-518. This confirms the reason for the editor's rewording.
- `pdftotext` and `pdftoppm` of pp. 45-48, 104-106 and 109-110, and a check of the bookmarks in out/main.out.
- These are targeted checks only. No project-wide verification was run; CI handles it.
