# W5 report: group recB

Files: `sections/recourse-cuts.tex`, `sections/recourse-mixed.tex`,
`sections/recourse-balanced.tex`, `sections/appendix-recourse-cuts.tex`.
CUTPLAN assigns recB only its minor findings, with no moves or cuts.
`recourse-mixed.tex` needed no change.

None of the six findings in `assign/recB.json` has a `verifier` field, so
the reviewers' fixes were used.

## Adjudication

| id | decision | reason | change |
|---|---|---|---|
| M-recourse-5 | ACCEPTED (deletion option) | The sentence is false for integer residual coordinates with a non-integral subbox, because Lemma `lem:cr-endpoint` needs integer bounds for them. For example, on [0,1/2] the cut returns 1/2. The sentence is also cited nowhere: `grep` finds no use of the subbox, fixing or linear-term variants. The main statement already covers core points v, where the core–residual couplings become linear terms. | `recourse-cuts.tex`, Theorem `thm:cr-oracle`: deleted "The same holds after the residual box is replaced by a rational subbox, after residual coordinates are fixed, and after rational linear terms are added." Also deleted the proof sentence that justified it ("The last statement holds because ... a fixed coordinate has δ_i=0"). |
| C-consistency-3 | MODIFIED | In the proof of Theorem `thm:cr-exact`, `s` named a minimizer, but `s` is reserved for widths. The minimizer lies in the core cube, where points are written `v`, so `v^\circ` is used instead of the reviewer's `x^\circ`. It is compatible with the exact group renaming `s` to `x^\circ` in Lemma `lem:statpoly`, because the lemma is applied to `F_{y_U}`. | `appendix-recourse-cuts.tex`, proof of Theorem `thm:cr-exact`: "let $s$ be a minimizer" became "let $v^\circ$ be a minimizer". In the same file, the proof of Proposition `prop:cr-submod`(c) used the points `s,t` in [0,1]^R (the same clash with the width `s_i`); renamed them `t,t'`. The algebra was rechecked by hand: in the opposite-sign case the difference is (t_i-t'_i)(t_j-t'_j). |
| C-writing-17 | ACCEPTED | Appendix D contains Theorem `thm:cr-exact`, which Table 1 cites, and Propositions `prop:cr-submod` and `prop:cr-greedy`, not only deferred proofs. | `appendix-recourse-cuts.tex`, line 1: "Cut-based recourse: deferred proofs" became "Cut-based recourse: exact output, concave--convex residuals and proofs". The label `app:recourse-cuts` is unchanged. The new title takes two lines. |
| C-writing-19 | MODIFIED | My files contain one use of "optimizer", at `recourse-cuts.tex:218`. Rather than replacing the word, the sentence now states the hypothesis it means, so it does not depend on recA's wording of Theorem `thm:cr-filter`. | Proof of Theorem `thm:cr-search`(b),(c): "its hypothesis on an optimizer cell holds by (a)" became "its hypothesis that some cell of $\mathcal Q_j$ contains $x^*_{\mathcal K}$ holds by (a)". |
| C-literature-10 | ACCEPTED | In TR TUD-FI06-01, the threshold ("K to 2") encoding is in Section 3 and the min-cut construction in Section 4. | `recourse-balanced.tex`: `\cite[Section~4]{SchlesingerFlach2006}` became `\cite[Sections~3--4]{SchlesingerFlach2006}`. |
| R-referee-4 | MODIFIED (my part) | Two items concern my files: `r_{ij}` (`recourse-cuts.tex:65`) and the CORE allowance `e_j` (`:173`). `r_{ij}` was a local alias for `-\omega_{ij}/2`, so I removed it instead of renaming it. `e_j` stays: it is the bag-cell allowance `e` / `e_B(C)` of Theorem `thm:cr-filter` and Lemma `lem:cr-cell` (recA's notation) at level j. The clash the referee names is with the Section 5 exponent `e_i`, which the core groups rename. | Proposition `prop:cr-cut`: the pair arcs now have "capacity $-\omega_{ij}/2\ge0$", and the proof writes $-\frac12\sum_{i<j}\omega_{ij}\abs{z_i-z_j}$ in both places. No new symbol. The LP slack `r` in the proof of Proposition `prop:cr-greedy`(c) is a local variable of one appendix proof and was kept. |

## Cut-plan items

None are assigned to recB. Two of the changes above also shorten the text:
the deleted robustness sentence and its proof sentence (5 source lines), and
the removed symbol `r_{ij}`.

Page savings, measured by building the pre-W5 snapshot alone
(`/tmp/w5-recB-before`) and the snapshot with only my four files replaced
(`/tmp/w5-recB-iso`):
- Sections 7.4–7.5 span pp. 39–44 in both builds (Section 8 starts on p. 44).
- Appendix D spans pp. 109–112 in both builds (Appendix E starts on p. 112).
- `pdftotext` finds 282 lines on pp. 39–43 after the change, against 284
  before. In Appendix D, the two-line title offsets the savings in the text.
- Net saving: about 2–3 lines; no page change.

Page spans in the full current tree (`/tmp/w5-recB`, which includes other
groups' concurrent edits):
- Section 7.4 (`sec:cuts`) starts on p. 39.
- Remark `rem:cr-mixed` and Section 7.5 (`sec:balanced`) are on p. 43.
- My main-text material ends on p. 44, and Section 8 starts at the top of p. 45.
- Appendix D (`app:recourse-cuts`) spans pp. 109–112, and Appendix E starts on p. 113.
- The shifts against the snapshot come from other files.

## Labels

No label was moved, deleted or renamed.

## Requests for other files

- coreA/coreB (`setting.tex` Table `tab:notation`, `growth.tex`): `r_{ij}`
  no longer exists. If the Section 5 exponent `e_i` is renamed (to `\varpi_i`,
  as R-referee-4 proposes), the CORE allowance `e_j` and `e_B(C)` need no
  change. If it is not renamed, list `e_j` (the allowance of Section 7.4)
  among the remaining double uses.
- exact (`exact.tex`, Lemma `lem:statpoly`): no dependency. The proof of
  Theorem `thm:cr-exact` names its own minimizer (`v^\circ`) and vertex
  (`v`), so renaming `s` to `x^\circ` in the lemma needs no change here.
- recA: none. The proof of Theorem `thm:cr-search` no longer quotes the
  wording of Theorem `thm:cr-filter`'s hypothesis.

## Checks run (local, targeted; not CI)

- `latexmk -pdf -interaction=nonstopmode main.tex` in `/tmp/w5-recB`
  (current tree): 124 pages, no LaTeX errors, no undefined references or
  citations, no overfull or underfull boxes.
- The same command in `/tmp/w5-recB-before` (pre-W5 snapshot, 123 pages)
  and in `/tmp/w5-recB-iso` (snapshot plus my four files, 123 pages): no
  errors or warnings. These two builds give the page spans above.
- I inspected the rendered pp. 40, 109 and 110 of `/tmp/w5-recB-iso`
  (Proposition 7.16, the Appendix D title, the proof of Theorem D.2).
- `python3 -B process/w4/checks/M-recourse-cuts.py`: ALL PASS. It checks the
  identity of Proposition `prop:cr-cut`(a) with pair capacities
  `-\omega_{ij}/2`, Lemma `lem:chaincut`, Lemma `lem:cr-height`, Theorem
  `thm:cr-search`(b)–(d), the Theorem `thm:cr-exact` pipeline and Proposition
  `prop:cr-submod`(c). The mathematics is unchanged; this confirms that the
  notation change matches the checked construction.

No project-wide verification was run, and CI was not consulted.

## Unresolved

None.

## Verification (recB-verify)

Method: `diff -u` of the four files against `process/w5/sections-before-w5/`,
re-derivation of every changed statement and proof, cross-file `grep`s, an
exact-arithmetic script, and a private build. `assign/recB-verify.json` does
not exist; the findings checked are those in `assign/recB.json`. No
`verifier` field exists for them in `assign/recB.json` or in
`process/w4/all-results.json`; the latter's `verified` lists contain only
major findings.

### Findings

| id | verdict on the revision | notes |
|---|---|---|
| M-recourse-5 | correct | The deleted sentence was false for integer residual coordinates on a non-integral subbox (Lemma `lem:cr-endpoint` needs integer bounds there). Nothing depends on it: `grep` over all sections finds no use of the subbox, fixed-coordinate or added-linear-term variants. Min-marginals in Section 7.5 come from Lemma `lem:chaincut`, which proves its own fixed-coordinate case. The computation section uses only the main statement. The remaining statement and proof of `thm:cr-oracle` are complete. |
| C-consistency-3 | correct | `v^\circ` in the proof of `thm:cr-exact` agrees with the exact group's current Lemma `lem:statpoly`, which is now stated for `x^\circ\in\mathcal S`. Parts (b) and (c) of that lemma are cited correctly: `\mathcal P\subseteq\mathcal S`, and `\hat H_{J_vJ_v}\succ0` with `\hat H=\Delta H`. `v^\circ` also appears in the proof of `thm:cr-filter` (Appendix C) as a local name in another proof; there is no conflict. The renaming `s,t -> t,t'` in `prop:cr-submod`(c) was re-derived: in the opposite-sign case the difference is `(t_i-t'_i)(t_j-t'_j)\le0`. The same width clash remained in the proof of `prop:cr-greedy`(a), where `s` was a summation index (`i_s=\pi(l_s)`, "summing over $s$"). **Fixed** (see below). |
| C-writing-17 | correct | The new title matches the content (D.1 exact output, D.2 concave--convex residuals, D.3 proofs for Section 7.5). No file quotes the old title. The label is unchanged. |
| C-writing-19 | correct | The four files now contain no "optimizer". The new wording matches the current hypothesis of `thm:cr-filter`(b): "if some $C\in\mathcal Q$ contains $x^*_B$ for a global minimizer $x^*$". The proof of (a) gives that hypothesis by induction over levels. Checked: (b) and (c) follow from `thm:cr-filter`(b),(c) with `\varepsilon_{\mathrm{or}}=0`, `e_{\mathcal K}(C)\le kLh_j^2/8=e_j`, and the incumbent rule of CORE, which satisfies `U\le\min_vF(x^v)`. |
| C-literature-10 | correct | Checked against the primary source (TR TUD-FI06-01, wwwpub.zih.tu-dresden.de/~ds24/publications/tr_kto2.pdf). Section 3 is "Transformation 'K to 2'" (the threshold encoding). Section 4 is "Construction of a MinCut problem, exact solution of submodular MinSum problems". |
| R-referee-4 (recB part) | correct | Re-derived `prop:cr-cut`(a) with pair capacities `-\omega_{ij}/2`, and checked it exactly. `r_{ij}` occurs nowhere in the paper now. `growth.tex` already renames the Section 5 exponent to `\varpi_i`, so the CORE allowance `e_j` no longer clashes with it. `e_j` stays because it is the level-$j$ value of recA's allowance `e`/`e_B(C)`. The remaining double use is the scalar allowance `e`, `e_B(C)`, `e_j` (Section 7) against the unit vector `e_i` (Sections 3 and 6). The notation table is not ours (see requests). |

### Fix made by the verifier

- `appendix-recourse-cuts.tex`, proof of Proposition `prop:cr-greedy`(a): the
  summation index `s` clashed with the reserved width, which the revision
  had already avoided in `prop:cr-submod`(c). The proof is now written without
  an index: for `i=\pi(l)\in S` let `S_{<i}` be the elements of `S` that
  precede `i`. Submodularity applied to `S_{<i}\cup\{i\}` and `S^\pi_{l-1}`
  gives `a^\pi_i\le\hat\Phi(S_{<i}\cup\{i\})-\hat\Phi(S_{<i})`, and summing
  over `i\in S` telescopes. The argument is re-derived: the intersection of
  the two sets is `S_{<i}` and their union is `S^\pi_l`, because
  `S_{<i}\subseteq S^\pi_{l-1}` and `i\notin S^\pi_{l-1}`. The script below
  also checks it exactly. The change adds one source line and no page.

### Cut plan, labels, layout

- CUTPLAN assigns recB no moves, and none were made. Labels in all four
  files are identical to the snapshot. No label in `sections/` is
  duplicated.
- Private build in `/tmp/w5-recB-verify` (current tree, including other
  groups' edits): 126 pages. My files cause no errors, undefined references,
  or overfull or underfull boxes. Other groups' files have one overfull
  box, in `appendix-tu.tex` (lines 19--34), and one undefined citation,
  `AbelloEtAl2001`, cited in `limits.tex`.
- Page spans (from `main.aux`):
  - Section 7.4 (`sec:cuts`) starts on p. 39.
  - `rem:cr-mixed` and Section 7.5 (`sec:balanced`) are on p. 42.
  - `cor:core` is on p. 44, and Section 8 starts on p. 44.
  - Appendix D (`app:recourse-cuts`) spans pp. 105--108.
  - `thm:cr-exact` is on p. 106 and `prop:cr-greedy` on p. 107.
  - Appendix E starts on p. 108.

  The shifts against the revision agent's numbers come from other groups'
  concurrent cuts. The verifier's edit did not change any page boundary:
  page-shipping markers are identical before and after it.
- I checked the rendered p. 107: the rewritten proof sets correctly.

### Checks run (local, targeted; not CI)

- `python3 -B process/w5/checks/recB-verify-cuts.py`: ALL PASS. It checks:
  - the cut identity `eq:cr-cutid` with capacities `-\omega_{ij}/2`
    (300 random instances, all labels);
  - the lattice inequality and the pair identity of `prop:cr-submod`(c);
  - on 200 random concave--convex instances with exact 1-D convex
    minimization: submodularity of `\Phi`, the per-element inequality of
    the new proof of `prop:cr-greedy`(a), and the statements of (a) for all
    orderings and sets.
- `python3 -B process/w4/checks/M-recourse-cuts.py`: ALL PASS (rerun).
- `latexmk -pdf -interaction=nonstopmode main.tex` in `/tmp/w5-recB-verify`,
  run before and after the verifier's edit.

No project-wide verification was run, and CI was not consulted.

### Requests for other files (updated)

- coreA (`setting.tex`, Table `tab:notation`): the exponent rename to
  `\varpi_i` is done. Optionally, list the remaining double use of `e`:
  the unit vector `e_i` (Def. `def:curvature`) and the cell allowance
  `e_B(C)`/`e_j` (Section 7). No change is needed in recB files.

### Unresolved

None.
