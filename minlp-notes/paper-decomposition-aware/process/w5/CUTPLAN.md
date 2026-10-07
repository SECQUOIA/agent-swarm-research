# W5 revision plan (binding together with process/w3/CONVENTIONS.md)

Source: second independent review round W4 (`process/w4/*.md`,
`process/w4/all-results.json`). No reviewer found a mathematical error. The
confirmed major issues are editorial: the main text is 80 pages (target of
CONVENTIONS / Option B: about 60 pages before the references), the
introduction is about 6 pages, the growth-scope caveat attributes to growth a
restriction that minimality already implies, the Hochbaum-Shanthikumar
comparison is missing, and the SCIP explanation in Section 11 is wrong.

Target after W5: main text about 62-65 pages (pp. 1 to the end of the
conclusion). Every proved result stays in the paper; labels are unchanged.
A moved block leaves its labelled statement, or a 2-4 line summary that says
what is proved and where ("Appendix~\ref{...}"). Proofs moved to an appendix
start with "\begin{proof}[Proof of Proposition~\ref{...}]".

## Moves and cuts per group (line numbers refer to process/w5/sections-before-w5/)

front (abstract, intro, related, conclusion)
* Introduction: Results subsection at most 3 pages plus Table 1. Use the
  verified proposal `process/w4/checks/verify-C-writing-2-proposed.tex`
  (four parts separated by %%%) as the starting point: shorter "Thus ..."
  paragraph, one short paragraph per extension without undefined terms.
  Keep Theorems 1.1, 1.2 and Table 1 (shrink the table if possible).
* Scope caveat: replace with the verified text of C-writing-3 (in
  process/w4/all-results.json, verifier corrected_fix): minimality alone
  confines negative curvature to directions involving active bounds or
  integer coordinates; growth adds the quantitative local condition
  H_{J0J0} >= 2gI (point growth) and the global one (distant near-optimal
  points force kappa to be large).
* FPT wording: the parameter is the best kappa-bar of the instance (R-referee
  minor).
* Related work: shorten toward 2 pages, keep each comparison in one place.
  Delete the duplicate novelty sentence at related.tex 54-56 (keep the intro
  one). Add the Hochbaum-Shanthikumar proximity-scaling comparison (verified
  fix of C-literature-1), concisely (3-5 sentences): what HS do (fixed-size
  grid per scale, log(1/eps) scales, proximity theorem for separable convex
  objectives; TU specialization with Meyer 1977 if the key exists), and what
  differs here (nonconvex objectives, proximity from growth and filtering
  instead of convexity, certificates).
* Conclusion: keep it to about one page.

coreB: move the numeric part of the proof of Lemma lem:states (growth.tex
162-174) to Appendix A, leaving the main argument.

recA:
* Section 7.2: keep the definitions of bag cells, V_B, e_B(C), Lemma
  lem:cr-cell and Theorem thm:cr-filter (Section 7.4 uses them). Move
  recourse-local.tex 68-147 (multilevel/gap discussion, setup, statement and
  discussion of prop:star) to Appendix C, with a one-sentence summary such as
  "With grid min-marginals in place of exact recourse, a constant correction
  charged to one bag must grow with the dimension (Proposition~\ref{prop:star}
  in Appendix~\ref{app:recourse-convex})."
* Section 7.3: move the affine-selector recognition paragraph and Theorem
  thm:cv-recog (recourse-convex.tex 282-300) to Appendix C with the summary
  "One exact convex QP and one LP decide whether a block has an affine
  optimal selector, and if so return a one-leaf certificate
  (Theorem~\ref{thm:cv-recog} in Appendix~\ref{app:recourse-convex})."
  Keep the definitions needed for Proposition prop:cv-limit and its
  statement (intro and conclusion cite it); move the discussion after it
  (from "Disjoint copies give ..." on, lines 331-345) to Appendix C, keeping
  its first two sentences.

tu:
* Section 8.6: keep the paragraph with eq:tu-constants and the statement of
  thm:tu-exact; move the TU-EXACT box and the remaining text
  (constraints.tex 519-545, 561-571) to Appendix E.
* Move prop:tu-misaligned, its numerical instance and ex:tu-sum
  (constraints.tex 590-650) to Appendix E; keep: "Two natural non-uniform
  alternatives, misaligned coordinate grids and a common graded pattern, give
  invalid bounds with curvature-only corrections
  (Proposition~\ref{prop:tu-misaligned} and Example~\ref{ex:tu-sum} in
  Appendix~\ref{app:tu})."
* Move rem:tu-curv, prop:tu-align and ex:tu-union (constraints.tex 86-118,
  382-406) to Appendix E, keeping one sentence on how alignment is checked.
* Add, if useful, one sentence in rem:tu-bm or Section 8 relating TU-GRID to
  the Hochbaum-Shanthikumar TU scaling (the front group puts the main
  comparison in related work; do not duplicate it).

optsets:
* Move the proofs of prop:twocenters, lem:endpointid and cor:facecsp
  (optsets.tex 65-127, 303-345, 412-443) to Appendix F; retitle Appendix F
  "Proofs for Section 9" (keep label app:proximal).
* Section 9.3: keep the definitions of box KKT points and Lambda, the
  statement of lem:diagcert, rem:shor shortened to the definition of the
  class plus the credit sentence, a precise 4-6 line description of PROX
  and DISC (CONVENTIONS requires PROX to be defined in the main text; keep
  labels alg:prox and alg:disc on whichever environment holds the
  definition), then the statement of thm:diagdiscovery. Move the algorithm
  boxes if they are long, lem:proximal (replace by the one-paragraph summary
  in the C-writing-1 verifier fix), the discussion after the theorem, and
  prop:sshard with its proof to Appendix F.

limits:
* Move the proofs at limits.tex 422-466, 502-545, 576-607 and 647-660 to
  Appendix G. Shorten the opening bullet list of Section 10 (C-writing-9).

computation:
* Fix the SCIP paragraph (C-computation-1 verified fix; incumbents lie
  ~1e-8 outside the box at active coordinates; the 1.3e-14 refers to the
  projected incumbents) and Table caption.
* Merge E3 into E2, merge Sections 11.5 and 11.6, shorten 11.9.
* Create sections/appendix-computation.tex (section "Additional
  computational results", label app:computation; the coordinator adds it
  to appendix.tex as the last appendix) and move there the E6 detail table,
  the SCIP detail table, and the recourse subsection's table and detail,
  each leaving one summary paragraph with the key numbers in Section 11.
  Target for Section 11: about 4.5 pages.

coreA, exact, recB: assigned minor findings only.

## Rules

As in CONVENTIONS section 6, with these changes: findings are in
`process/w5/assign/<group>.json` (W4 findings that were not refuted; a
`verifier` field holds the verified severity and the corrected fix — prefer
it over the reviewer's fix); reports go to `process/w5/reports/<group>.md`;
build into `build/w5-<group>` with
`latexmk -pdf -interaction=nonstopmode -outdir=build/w5-<group> main.tex`
(the paper root has main.aux/main.bbl from the user's editor; if bibtex
complains, build in a private copy, e.g. rsync main.tex macros.tex
references.bib sections figures to /tmp/w5-<group>/ and build there).
Do not change anything outside your files. Do not touch the root main.*
files. Report the page span of your sections after the change.
