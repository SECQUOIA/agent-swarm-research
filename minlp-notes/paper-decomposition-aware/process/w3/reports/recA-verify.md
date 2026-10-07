# W3 report: recA-verify (verification of Section 7 intro, 7.1-7.3, Appendix C)

Files verified and edited: `sections/recourse.tex` (text only),
`sections/recourse-valuefn.tex`, `sections/recourse-local.tex`,
`sections/recourse-convex.tex`, `sections/appendix-recourse-convex.tex`.
The detailed account is the "Verification (recA-verify)" section appended to
`process/w3/reports/recA.md`. No assignment file `assign/recA-verify.json`
exists; the findings verified are those of `assign/recourse.json`.

## (1) Adjudication check

"Confirmed" means recA's decision is justified and the change is in the files
and correct. "Completed" means the change was right in substance and the
verifier finished it.

| Id | recA status | Verification | Verifier change |
|---|---|---|---|
| F7 | other owner | Confirmed (no text in recA files) | none |
| F9 | MODIFIED | Confirmed; replacement sentence completed | last paragraph of 7.3: no unproved necessity claim; "global constants cannot be used" follows from prop:cv-limit |
| F10 | MODIFIED | Confirmed (cr-semiconcave deleted; lem:cr-cell from prop:cellwise(a); thm:cv(iii) cites prop:accept) | none |
| F11 | MODIFIED | Confirmed; rem:cv-instances checked against DPK's account of Khajavirad | none (see (3)) |
| F12 | ACCEPTED | Confirmed | none |
| F13 | ACCEPTED | Completed | REC (Algorithm~\ref{alg:rec}) at first use in Section 7 |
| F15 | ACCEPTED | Confirmed | none |
| F20 | other owner | Confirmed | none |
| F24 | ACCEPTED | Completed | roadmap now cites Remark~\ref{rem:cr-mixed} |
| F25 | MODIFIED | Confirmed | none |
| F26 | ACCEPTED | Confirmed (no British spellings left) | none |
| F29 | other owner | Confirmed | none |
| F30 | ACCEPTED | Confirmed | none |
| F34 | ACCEPTED | Confirmed (0 overfull boxes in the whole build) | none |
| F35 | MODIFIED | Confirmed | none |
| F41 | ACCEPTED | Confirmed | none |
| F42 | other owner | Confirmed | none |
| F43 | ACCEPTED | Confirmed | none |
| F45 | ACCEPTED | Confirmed | none |
| F46 | ACCEPTED | Completed | "quadratic growth" -> "point growth" in thm:cv(iii) |
| F49 | other owner | Confirmed | none |
| F56 | ACCEPTED | Confirmed | none |
| F58 | ACCEPTED | Completed | leaves Pi_1.. -> Pi'_1.. (clash with scope box Pi_t) |
| F59 | ACCEPTED | Confirmed | none |
| F60 | MODIFIED | Confirmed (CONVENTIONS scheme) | none |
| F63 | ACCEPTED | Confirmed | none |
| F65 | other owner | Confirmed | none |
| F67 | MODIFIED | Confirmed (REC needs a box; slices of 7.3 are polytopes) | none |
| F68 | ACCEPTED | Confirmed | none |
| F69 | ACCEPTED | Confirmed | none |
| F70 | ACCEPTED | Completed | thm:cv(iii), its proof, cor:cv-nu: kappa -> kappa_V = kappa(L^+,g); thm:valuefn: kappa_V = kappa(L^V,g) |
| F71 | other owner | Confirmed | roadmap \ref added (rem:cr-mixed) |
| F72 | ACCEPTED | Confirmed | none |
| F79 | other owner | Confirmed | none |
| F81 | other owner | Confirmed | none |
| F84 | ACCEPTED | Confirmed | none |
| F87 | ACCEPTED | Confirmed | none |
| F88 | ACCEPTED | Confirmed | "recourse" defined in one sentence |
| F89 | ACCEPTED | Confirmed in recA files; recB still writes eta = 0 when citing thm:cr-filter | request in (3) |
| F91 | other owner | Confirmed | none |
| F92 | ACCEPTED | Confirmed | none |
| F93 | other owner | Confirmed | none |
| F94 | ACCEPTED | Confirmed | none |
| F110 | ACCEPTED | Confirmed | none |
| F111 | ACCEPTED | Confirmed (proof re-derived; exact check rerun) | none |
| F112 | MODIFIED | Completed: the constant also depends on the encoding-length bound of the L_i^V, F_0's factors need exact polynomial-time evaluation, and (c) needs the box model | statement of thm:valuefn and App C.1 rewritten (see recA.md, Verification, item 1-2) |
| F113 | MODIFIED | Confirmed | none |
| F115 | ACCEPTED | Confirmed | none |
| F116 | ACCEPTED | Confirmed | none |
| F117 | MODIFIED | Confirmed (per-coordinate L_i is sharper; core search takes L_i = L) | none |
| F118 | ACCEPTED | Confirmed | none |
| F119 | other owner | Confirmed | none |
| F120 | other owner | Confirmed | none |
| F121 | ACCEPTED | Confirmed | none |
| F122 | ACCEPTED | Confirmed | none |
| F123 | other owner | Confirmed | none |
| F124 | ACCEPTED | Confirmed | none |
| F125 | ACCEPTED | Confirmed | none |
| F126 | ACCEPTED | Confirmed | none |
| F127 | ACCEPTED | Confirmed | none |
| F128 | ACCEPTED | Confirmed | none |
| F129 | other owner | Confirmed | none |
| F130 | other owner | Confirmed | none |
| F131 | other owner | Confirmed | none |
| F132 | ACCEPTED | Confirmed | none |
| F150 | other owner | Confirmed | none |
| F151 | ACCEPTED | Confirmed | none |
| F203 | other owner | Confirmed | none |

Further verifier fixes not tied to one finding: Section 7.1 discussion and
closing paragraph now state accurately what Sections 7.3 and 7.4 provide;
"slope" -> "linear part" (CONVENTIONS); prop:star preamble "center x" ->
"coordinate x"; the proof of prop:vf-curv(b) states why a subinterval lies in
one leaf interval; App C.1(c) states the growth assumption of the bound.

## (2) Labels deleted or renamed

None by the verifier. recA's deletions (lem:cr-semiconcave, lem:cv-energy,
lem:cv-envelope) were checked: no references remain in `sections/` except
in `appendix-smoothed.tex`, which is to be deleted and cites only
lem:valuefunction and eq:cr-oracle.

## (3) Requests for other files

1. recB, `sections/recourse-cuts.tex`, proof of thm:cr-search, "(b), (c)
   These are Theorem~\ref{thm:cr-filter} with ... $\underline V=V$ and
   $\eta=0$": replace "$\eta=0$" by "$\varepsilon_{\mathrm{or}}=0$".
2. front, `sections/related.tex` lines 19-22: "Their tractable classes of
   unbounded treewidth, and those of Khajavirad, take variables with
   nonpositive diagonal to be binary and eliminate the continuous components
   into value functions of their binary neighbors." Del Pia and Khajavirad's
   Theorem 4 eliminates binary components first; only Khajavirad's Theorem 5
   eliminates the continuous components (DPK, paragraph after Theorem 5).
   Suggested: "Their tractable classes of unbounded treewidth, and those of
   Khajavirad \cite{Khajavirad2026PolyBox}, take variables with nonpositive
   diagonal to be binary; Remark~\ref{rem:cv-instances} compares Khajavirad's
   elimination of the continuous components with our value factors."
3. coordinator: page budget of Section 7 (pp. 31-45, target about 12 pages);
   optional global renames G_t -> another letter and sigma_j -> another letter
   (see recA.md, Verification, "What remains").

## (4) New BibTeX entries

None.

## (5) Checks run

* `python3 -B process/w3/checks/recA-verify-identities.py` (new, exact
  arithmetic): lem:cr-cell 0 violations on 400 random instances; ladder
  identity True; ex:cv-fm True; eq:cv-energy 0 violations; ex:cr-star32 and
  prop:star(A) corner minimum True; prop:cv-limit True.
* `python3 -B process/w3/checks/recA-cv-height.py`: PASS (3944 instances,
  1061 with several minimizers).
* `TEXINPUTS=.: pdflatex -interaction=nonstopmode
  -output-directory=build/recA-verify main.tex` twice, then
  `latexmk -pdf -interaction=nonstopmode -outdir=build/recA-verify main.tex`
  (exit 0): 0 errors, 0 warnings, 0 undefined references, 0 overfull boxes.
  No project-wide verification was run; CI is not consulted.

## (6) Unresolved

* recB citation of thm:cr-filter still uses eta (request 1).
* Section 7 page budget (coordinator).
* G_t and sigma_j kept (no rename in CONVENTIONS; A_t would clash with the
  w-polytope matrix A used in 7.3).
