# W7 report: group tu (sections/constraints.tex, sections/appendix-tu.tex)

| Finding | Decision | What was done | Reason for any deviation |
|---|---|---|---|
| F-referee-1(a), Section 8 part (corrected fix of verify-F-referee-1.md) | MODIFIED | Moved the proofs of `prop:tu-sound`, `thm:tu-states` and `thm:tu-approx` word for word into the new `\subsection{Proofs for Sections~\ref{sec:tu-filter}--\ref{sec:tu-complexity}}\label{app:tu-proofs}` (now E.2), between E.1 "Checking the model" and "Union versus hull filtering". Each proof starts with `\begin{proof}[Proof of Proposition/Theorem~\ref{...}]`. Each main-text proof is replaced by "The proof is in Appendix~\ref{app:tu-proofs}.", which opens the paragraph that follows the statement, as in limits.tex and optsets.tex. The proofs of `lem:tu-round` and `lem:tu-allow` stay in the main text. Every statement and label stays in place: 23 labels kept, checked by `tu-verify-move.py`. The opening of Appendix E was changed as in the corrected fix. | Three small additions. (1) In the moved proof of `thm:tu-approx`, "the tree computation above" became "the tree computation of Section~\ref{sec:tu-filter}". From the appendix, "above" no longer points to Section 8.3. This is the only word change in the moved text. (2) Appendix E was retitled from "Coupling constraints: checks, exact output and examples" to "Coupling constraints: checks, proofs, exact output and examples", so that the title covers the new E.2 (cf. F-proofread-15 for Appendix F). The label `app:tu` is unchanged. (3) None of the moved proofs uses anything undefined at its new place. Every lemma, equation and symbol it uses (`lem:tu-round`, `lem:tu-allow`, `eq:tu-setgrowth`, $t_i$, $a_j$, $E_j$, $\mathcal D^{(j)}$, $U_j$, $m_i$, $J$) is either cited by `\ref` or defined in the statement it proves. No text cites the proof of any of these results. |
| F-proofread-7 | ACCEPTED | `eq:tu-constants` is now a two-line `gathered` display, using the given text. In the build, the number (8.4) sits beside the display (p. 47). | None. |
| F-proofread-8 | ACCEPTED | Remark `rem:tu-bm` now reads "... a constraint intersection graph of treewidth $\omega$ and a tolerance $\epsilon$ (we keep their symbol, distinct from our accuracy $\varepsilon$), a linear program with ...". | None. Only the source lines were rewrapped. |
| F-proofread-14 (constraints.tex part) | MODIFIED | Replaced "non-uniform" with "nonuniform" at all three places in constraints.tex: the intro of Section 8, the title of Section 8.7 and its second paragraph. The label `sec:tu-limits` is unchanged. The same fix applies to `\paragraph{Non-uniform alternatives.}` in appendix-tu.tex (E.7), which became "Nonuniform alternatives.". | The appendix-tu.tex heading has the same inconsistency, and that file is mine. After the change, the first line of that paragraph was overfull by 1.39 pt, so I rewrote its sentence as "With a single order constraint, misaligned coordinate grids already give invalid bounds with curvature-only corrections." The meaning is unchanged, and the build now has no overfull box. |

## Cross-file requests

None. Nothing outside my files cites the moved proofs. The other references to `prop:tu-sound`, `thm:tu-states`, `thm:tu-approx` and `app:tu` (intro.tex, conclusion.tex, limits.tex) cite statements, and those stay in place. No other file contains "non-uniform".

Observation, not caused by my changes: my private build had three undefined references to `app:cr-proofs`, from recourse-cuts.tex lines 116, 186 and 204. The recourse group's matching appendix subsection was not yet present when I copied the sources.

## Commands run

- `python3 process/w7/checks/tu-move.py`: moved the three proof blocks and edited the opening of Appendix E (run once).
- `python3 process/w7/checks/tu-verify-move.py`: checks that the moved proofs match the pre-W7 text up to whitespace, apart from the one pointer change; that all 23 labels of constraints.tex remain exactly once; and that there are 3 pointers, with 2 proofs left in the main text. Result: pass (318, 150 and 116 words moved verbatim).
- `rm -rf /tmp/w7-tu && mkdir -p /tmp/w7-tu && cp -r main.tex macros.tex references.bib sections figures /tmp/w7-tu/ && cd /tmp/w7-tu && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=out main.tex`, run twice: before and after the overfull-box fix, recopying sections/ the second time. Final result: exit 0, 126 pages, no errors, no multiply defined labels, no overfull or underfull boxes, no hyperref warnings. The only undefined references are the three `app:cr-proofs` ones from recourse-cuts.tex (see above).
- `grep` of out/main.log and out/main.aux; `pdftotext` and `pdftoppm` of pp. 45-48 and 104-105: checked the pointer sentences, equation (8.4) with its number beside the display, Remark 8.11 and the new Appendix E.2.
- These are targeted checks only. No project-wide verification was run (CI handles it).

## Verification

Independent check of group tu (sections/constraints.tex, sections/appendix-tu.tex) against process/w7/sections-before-w7/. Result: all four findings are handled correctly. I made no changes to the group's files.

What I checked:
- **Every change in both files.** `process/w7/checks/tu-verify-wordcmp.py` compares the whole pre-W7 and current files word by word and prints every difference. The only differences are the intended ones: three proof blocks replaced by pointers, the gathered display, the Remark 8.11 wording, "nonuniform" (3 times in constraints.tex, once in appendix-tu.tex), the Appendix E title and opening, the new E.2, and the reordered "Nonuniform alternatives." sentence. Nothing else changed.
- **Moved proofs.** The same script compares the three removed proof bodies with the proof bodies in E.2. Results:
  - `prop:tu-sound` (318 words) and `thm:tu-states` (150 words) are identical.
  - `thm:tu-approx` differs in exactly one place: "the tree computation above" became "the tree computation of Section~\ref{sec:tu-filter}". This change is needed, because "above" would point into Appendix E. Section 8.3 is where the tree computation and its operation count are stated.
  - Each proof starts with `\begin{proof}[Proof of ...~\ref{...}]`. The subsection title, the label `app:tu-proofs`, its position (after E.1, before "Union versus hull filtering") and the Appendix E opening all match verify-F-referee-1.md word for word. The PDF bookmark reads "Proofs for Sections 8.3–8.5".
- **The moved proofs are complete at their new place.**
  - Every `\ref`/`\eqref` target in them is defined: `lem:tu-round`, `lem:tu-allow`, `eq:tu-setgrowth`, `prop:tu-sound`, `thm:tu-states`, `sec:tu-filter`.
  - The symbols they use are fixed in Section 8.1, Algorithm 8.6, Lemma 8.3 or the statement being proved: $t_i$, $a_j$, $E_j$, $U_j$, $\beta_j$, $m_i$, $K$, $K_Z$, $s$, $\Delta_\eta$.
  - The internal phrases "as before", "for the last claim" and "the argument of (a)" refer to text inside the same proof.
  - No proof contained a `\label`. No text in any file cites the proof (as opposed to the statement) of these three results.
- **Labels and statements.** All 23 old labels of constraints.tex and all 20 old labels of appendix-tu.tex are still defined, once each and in the same file. The proofs of `lem:tu-round` and `lem:tu-allow` are still in the main text.
- **Surrounding text.** I read the three pointer paragraphs in the PDF (pp. 45-46): "The proof is in Appendix E.2." opens the paragraph that follows each statement, as in growth.tex, limits.tex and optsets.tex, and each reads correctly. I found no dangling "above/below/the theorem" near the edits. In appendix-tu.tex, "In this subsection and the next two" (E.4) still refers to E.4-E.6. Neither file hard-codes an appendix number. Other files cite only the statements (intro.tex, conclusion.tex, limits.tex), and those statements stay in place.
- **Deviations.**
  - The pointer change in `thm:tu-approx` is needed (see above).
  - The retitled Appendix E is accurate, matches the parallel retitling of Appendix D, and keeps `app:tu`.
  - The "Nonuniform alternatives." heading applies F-proofread-14's spelling rule to the only other occurrence in this group's files.
  - I tested the reworded sentence in a separate private build: with the new heading, the original word order gives "Overfull \hbox (1.3938pt too wide)" at appendix-tu.tex lines 515-518. The rewording removes it without changing the meaning.
- **F-proofread-7, -8 and -14.**
  - F-proofread-7: the text matches the given replacement, and (8.4) is set beside the two-line display (p. 47).
  - F-proofread-8: the text matches the given replacement, and the Remark 8.11 wording reads correctly (p. 48).
  - F-proofread-14: no "non-uniform" or "Non-uniform" remains in sections/.
  - F-dependencies-2 is fixed in appendix-growth.tex, another group's file. That fix renames its induction radius to $\rho_j$, which now matches the proof of `lem:tu-uniform` here.
- **Build.** I built a private copy in /tmp/w7-tu-verify from the current sources of all groups. It finished with exit 0 and 127 pages. The whole log has no errors, no undefined references, no multiply defined labels, no overfull or underfull boxes, and no hyperref warnings. The earlier undefined `app:cr-proofs` references are resolved now that the recourse group's subsection exists.

Fixed: nothing; no problems found.

Open: nothing for this group. One cosmetic point, left on purpose: two merged source lines in constraints.tex (288 and 328) are longer than the usual wrap width. This has no effect on the output, and leaving them keeps the diff small.
