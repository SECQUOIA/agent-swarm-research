# Adjudication of the W6 final-check findings

W6 was the final check after revision round W5. Four fresh reviewers worked on
whole-paper consistency, the dependencies of moved proofs, proofreading, and a
final referee assessment (`process/w6/F-*.md`). The only finding rated major,
F-referee-1 (length), was checked by an adversarial verifier
(`process/w6/verify-F-referee-1.md`). The verifier downgraded it to minor and
corrected the proposed fix. The F-consistency reviewer wrote its report but its
structured result was lost when the session ended; it rated all five of its
findings minor, so none needed a verifier.

No reviewer found a wrong statement among the main claims. The referee's
verdict was "ready for submission after small changes".

The findings were applied in round W7 by five file-owner agents (recourse, tu,
optsets, exact-comp, front-core), each followed by an independent verifier.
The per-finding records are in `process/w7/reports/<group>.md` (each with a
`## Verification` section) and `process/w7/decisions.json`. Backups of the
sections before W7 are in `process/w7/sections-before-w7/`.

Decision key: ACCEPTED = fixed as proposed; MODIFIED = fixed differently or
partly, with the reason recorded; REJECTED = no change, with the reason
recorded.

Totals: ACCEPTED 22, MODIFIED 12, REJECTED 4 (38 items, including the three
parts of F-referee-1 and the four optional suggestions).

| id | decision | what was done |
|---|---|---|
| F-referee-1(a) | MODIFIED | Proofs of eight secondary results moved word for word to appendices, following the verifier's corrected fix: `thm:cv` to the new C.4 (with the existing exact-output part of (iii)), `thm:cr-oracle`, `thm:cr-search`, `prop:cr-growth` to the new D.1, `prop:tu-sound`, `thm:tu-states`, `thm:tu-approx` to the new E.2, `thm:cells` to F.2. Each statement and label stays in the main text, followed by "The proof is in Appendix ...". The coordinator placed the uniform-cells proof after the proof of `prop:twocenters`, not first as proposed, so that Appendix F follows the order of Section 9.1. |
| F-referee-1(b) | ACCEPTED | Table `tab:chain` moved to Appendix H, before the exact-output paragraph; Section 11.3 now also quotes the range of $m$ and of the stage counts. |
| F-referee-1(c) | REJECTED | Section 6.5 (localized acceptance) stays in the main text. It is the practical form of exact acceptance, and Section 11 uses it; replacing it by a summary would save about 1.4 pages but leave a dense paragraph in its place. The main text now ends on p. 67 (was 70). |
| F-referee-2 | MODIFIED | Keywords and MSC 2020 codes (90C26, 90C11, 90C20, 90C39, 90C60, 68Q27, each checked against the MSC 2020 list) added to the abstract. The code sentence now says the code, inputs, raw results and scripts, with the imported solver files, are provided as supplementary material. No author block or declarations section: the author field is intentionally blank, and `README.md` lists these items and the artifact bundling as steps before submission. |
| F-referee-3 | MODIFIED | Conclusion sentence replaced, merged with the conclusion part of F-proofread-1; it says "maximum bag size $p$" as in Theorem 1.1 and cites EX's algorithm at first use. |
| F-referee-4 | ACCEPTED | Set growth, $\mathcal S$, $g_S$ and $\kappa_S$ are now defined where the introduction first uses them; the later definition was removed. Merged with F-consistency-5. |
| F-referee-5 | ACCEPTED | The S1 sentence in Section 6.5 now says the 40 to 72 stages refer to the five instances on which EX used the most stages (checked against `S1_ex_replay.csv`). |
| F-referee-6 | ACCEPTED | Table 1 says "a description of the optimal set" and "an exact description of the optimal set". |
| F-consistency-1 | MODIFIED | The $2^{-315}$ sentence names experiment E4; with F-referee-5, both experimental sentences of Section 6.5 name their experiment. |
| F-consistency-2 | ACCEPTED | "the next two examples" changed to "the next two propositions" in Appendix B. |
| F-consistency-3 | MODIFIED | Notation table: rows for $\nu$, for $f(p,t)$, and for $f_1$, $C_1$ (two rows instead of one, which overflowed by 15.7pt). |
| F-consistency-4 | ACCEPTED | "the theorem" changed to "Theorem~\ref{thm:approx}" at the start of Section 5.5. |
| F-consistency-5 | ACCEPTED | "every rational mixed box QP has set growth", matching Remark `rem:setgrowth`. |
| F-dependencies-1 | ACCEPTED | Opening sentence for Appendix A; the exact-comp group also added one for Appendix B, which the reviewer noted has the same gap (its verifier narrowed the claim about Propositions B.5 and B.6 to "this procedure needs"). |
| F-dependencies-2 | ACCEPTED | $R_j$ renamed $\rho_j$ in the proof of Corollary `cor:uniformgrid`, matching Lemma `lem:tu-uniform`. |
| F-dependencies-3 | MODIFIED | The Appendix H sentence on separable E3 runs was rewritten as proposed, with the node count stated for the last four stages (checked on `E3_stages.csv`, 18 runs). |
| F-dependencies-4 | ACCEPTED | Appendix H item (b) uses $j_{\max}$. |
| F-dependencies-5 | MODIFIED | New opening of Appendix D; it also names the proofs in the new D.1. |
| F-dependencies-6 | MODIFIED | New opening of Appendix F (two sentences instead of one; it also mentions the uniform-cells proof); a `\paragraph` heading for the coNP argument and the pointer "last paragraph of Appendix F" in Section 9. |
| F-proofread-1 | ACCEPTED | Abstract: "computing an exact minimizer takes $f_1(p,\kappa)I^{O(1)}$ bit operations". The conclusion part is merged into F-referee-3. |
| F-proofread-2 | MODIFIED | First reference to Table 1 added at the end of the set-growth paragraph, without "and lower bounds", because the table does not list them. |
| F-proofread-3 | ACCEPTED | "they enter only the running-time bounds, never the validity of the output". |
| F-proofread-4 | ACCEPTED | "These are the main results of this section." |
| F-proofread-5 | ACCEPTED | The two empty run-in headings in Section 7.3 removed. |
| F-proofread-6 | MODIFIED | "with a certificate that can be checked without optimization (Proposition~\ref{prop:cr-greedy}(d))"; the proposed wording could be misread. |
| F-proofread-7 | ACCEPTED | Equation (8.4) set as a two-line display; the number sits beside it. |
| F-proofread-8 | ACCEPTED | Remark `rem:tu-bm` states that it keeps Bienstock and Muñoz's symbol $\epsilon$, distinct from $\varepsilon$. |
| F-proofread-9 | ACCEPTED | "the proposition shows". |
| F-proofread-10 | ACCEPTED | Proof pointer moved out of the statement of Lemma `lem:diagcert` (the verifier added the missing paragraph break). |
| F-proofread-11 | ACCEPTED | $k$ (number of color classes) defined before use in Section 10. |
| F-proofread-12 | ACCEPTED | "It shows a limitation of filtered grids, not a hard problem". |
| F-proofread-13 | ACCEPTED | Tense fixed in E6. |
| F-proofread-14 | MODIFIED | "modeled", "nonuniform" (three times in Section 8 and once in an Appendix E heading, whose sentence was reworded to avoid a 1.4pt overflow), "nonasymptotic". |
| F-proofread-15 | ACCEPTED | Appendix F is titled "Proofs and supplements for Section 9". |
| O1 (shorten references) | REJECTED | The adaptive-discretization and constraints paragraphs place the paper relative to the literature that the review rounds asked to be credited; one-line citations there cost little and dropping them would weaken the credit. |
| O2 (shorten Section 11.1) | MODIFIED | Applied; Appendix H items (c), (d), (f), (g) cover everything deleted. One sentence on the initial coordinate descent stays, because Sections 11.2 and 11.3 refer to it, and the EX implementation details moved to the sentence in Section 11.4 that uses them. |
| O3 (reorder Section 7) | REJECTED | The gain is small, and the roadmap of Section 7 already says that Section 7.4 uses Section 7.2; reordering would renumber every Section 7 object cited elsewhere. |
| O4 (cover letter) | REJECTED | Not part of the manuscript. `README.md` records that the core is Sections 3-6 and 10.1-10.3. |

## Coordinator checks after W7

* Two open items from the verifiers were resolved: the order of Appendix F
  (see F-referee-1(a)), and a missing paragraph break between
  `\end{theorem}` and its proof pointer in `recourse-local.tex`.
* Isolated build (`/tmp/dpaper`, `latexmk -pdf`): exit 0, 127 pages; the log
  has no warnings, undefined references, multiply defined labels, or overfull
  or underfull boxes. Main text pp. 1-67, references from p. 67, appendices
  A-H pp. 81-127.
* The top rule of every table touched the last line of its caption (the
  article class adds no space below a caption placed above a table).
  `macros.tex` now loads `caption` with `tableposition=top`; the page layout is
  otherwise unchanged.
* The diffs of the abstract, introduction, conclusion, Sections 6.5 and 11,
  the notation table and the changed limits, growth and appendix passages
  were read against the pre-W7 backups.
