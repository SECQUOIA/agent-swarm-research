# W3 report: coreA verifier

There were two verification passes over `sections/setting.tex`,
`sections/setting-growthcert.tex` and `sections/grids.tex`. The details are in
the sections "Verification (coreA-verify)" and "Verification (coreA-verify,
second pass)" at the end of `process/w3/reports/coreA.md`. This file gives the
six required parts for both passes.

## (1) Adjudication (verifier verdict on the coreA rows)

"NOT IN coreA" means that no part of the finding touches the three coreA
files. "Confirmed" means the decision is justified and the fix is in the text.

| id | coreA status | verifier verdict |
|---|---|---|
| F10 | MODIFIED (coreA part) | Confirmed. Section 4 has one self-contained rounding proof and the families form. |
| F11 | ACCEPTED (coreA part) | Confirmed. The prior-work text in grids.tex is reduced to the technical comparison. |
| F12 | ACCEPTED (coreA part) | Confirmed. The notation table exists and was checked row by row against the defining sections. |
| F13 | ACCEPTED (coreA part) | Confirmed. "Nodes", "nodes per coordinate" and "table entries" are defined in Section 4. |
| F19 | NOT IN coreA | Confirmed (TRIAL is in growth.tex). |
| F22 | ACCEPTED (coreA part) | Confirmed: `ζ^T d`. |
| F26 | ACCEPTED (coreA part) | Confirmed. No British spellings remain in coreA files. |
| F28 | MODIFIED | Confirmed: there is no largest weighted constant when `P = ∅`. **Second pass:** the convention sentence after Def 3.2 was corrected (item 1 below). |
| F34 | ACCEPTED (coreA part) | Confirmed. The whole build has no overfull boxes. |
| F37 | MODIFIED (pass 1) | Confirmed. Lemma growthcert(b) and the remark separate what minimality and growth each give. The intro request is still open (part 3). |
| F38 | NOT IN coreA | Confirmed. |
| F41 | ACCEPTED (coreA part) | Confirmed. |
| F47 | NOT IN coreA | Confirmed. |
| F48 | NOT IN coreA | Confirmed. |
| F51 | NOT IN coreA | Confirmed. |
| F57 | NOT IN coreA | Confirmed. |
| F58 | ACCEPTED (coreA part) | Confirmed. |
| F59 | ACCEPTED (coreA part) | Confirmed: `𝒮`, `𝒮_i`, `J_0`, `J_∂`. |
| F61 | ACCEPTED (coreA part) | Confirmed: `g_0`. |
| F63 | ACCEPTED (coreA part) | Confirmed: `X'`, `X^{(j)}`, `X''`, `w(J)`. |
| F65 | NOT IN coreA | Confirmed. |
| F68 | MODIFIED (coreA part) | Confirmed. UC stage cells satisfy the hypotheses of the families form, so `lem:cells` is an instance. |
| F70 | ACCEPTED (coreA part) | Confirmed. **Second pass:** convention sentence corrected (item 1). |
| F75 | NOT IN coreA | Confirmed. |
| F83 | ACCEPTED (coreA part) | Confirmed. |
| F84 | NOT IN coreA | Confirmed. |
| F85 | ACCEPTED (coreA part) | Confirmed. Lemma dp states `O(p(|𝒜|+n+N)K^p)`; `thm:cells` matches. |
| F89 | NOT IN coreA | Confirmed. |
| F91 | ACCEPTED (coreA part) | Confirmed. The planted-instance text is now in computation.tex 96–106. |
| F136 | ACCEPTED (coreA part) | Confirmed. |
| F139 | MODIFIED | Confirmed: the theorem number is unverifiable. **Second pass:** "we use one bound `L_i` per coordinate" was added (item 2). |
| F140 | NOT IN coreA (row added in pass 1) | Confirmed: it concerns `rem:cluster` in growth.tex. |
| F152 | ACCEPTED | Confirmed against Lemma 20 and reference `[22]` of the local Del Pia–Khajavirad full text. |
| F155 | NOT IN coreA | Confirmed. |
| F156 | NOT IN coreA | Confirmed. |
| F157 | ACCEPTED (coreA part) | Confirmed. |
| F158 | MODIFIED | Confirmed. The two-variable example was re-derived. Request E5 has been applied (exact.tex 330). |
| F159–F167 | NOT IN coreA | Confirmed. |
| F168 | MODIFIED | Confirmed. |
| F177 | MODIFIED | Confirmed: degenerate subboxes are needed by `lem:labelfilter` and `prop:local`. |
| F181 | NOT IN coreA | Confirmed. |
| F187 | ACCEPTED | Confirmed. Soundness of (C1) with both alternatives was checked exactly. |
| F204 | MODIFIED (pass 1) | Confirmed. grids.tex points to Section 11, which now reports replay times. |

Changes made by the verifier:

- **Pass 1:**
  - `rem:nonconvex` and `lem:growthcert`(b) now credit positive
    semidefiniteness to minimality.
  - The integer-coordinate sentence of the remark was corrected.
  - The justification of the two-variable example was completed.
  - The cell-bound lead-in now covers unit integer intervals.
  - Replay figures are no longer quoted in grids.tex.
  - The filtering-record paragraph now proves `U_j ≥ β_j`.
  - Precision and wording fixes; two rows added to the notation table.
- **Pass 2:**
  1. The convention after Def 3.2 said that every statement involving κ, κ̄
     or κ_S holds for each valid constant. That is false for existential
     statements: "κ ≤ 2" in limits.tex 19 and 303, "κ_S ≤ 40" in optsets.tex
     37, "κ_S ≤ 2n(n−1)" in limits.tex 481. It now reads "a result that
     assumes growth holds for every valid constant, and a statement that an
     instance has, for example, κ ≤ c means that some valid constant gives
     this bound."
  2. Bajaj–Hasan: "the vertex bound of Bajaj and Hasan, who build …; we use
     one bound L_i per coordinate".
  3. The lead-in to Lemma growthcert now says "what minimality and growth
     imply".
  4. A wording split in the paragraph after Def 3.2.

## (2) Labels deleted or renamed

None. All 21 labels of the original coreA files survive. The 24 current
labels (the 21 old ones plus `eq:setgrowth`, `tab:notation` and
`sec:grids-dp`) are each defined once in the whole paper.

## (3) Requests for other files

- **front (intro.tex 136–138, "Scope of the growth hypothesis"). Still open.**
  Replace

  "Growth restricts where nonconvexity can occur. For a box QP, point growth
  forces the Hessian block of the continuous coordinates strictly inside their
  bounds to be positive definite, and weighted growth forces it to be positive
  semidefinite (Lemma~\ref{lem:growthcert})."

  with

  "For a box QP, the Hessian block of the continuous coordinates strictly
  inside their bounds at a minimizer is positive semidefinite, and point
  growth makes it positive definite (Lemma~\ref{lem:growthcert})."

  Positive semidefiniteness holds at every minimizer, with or without growth.
  The rest of the paragraph can stay.
- Requests C1, E1, E2, E5, O1 and O2 of coreA.md have been applied in the
  other files. C2 is obsolete.

## (4) New BibTeX entries

None.

## (5) Checks run (local, targeted; not CI)

- **Pass 2:**
  - `python3 process/w3/checks/coreA-verify-dp.py 1 300` and `… 7 300`
    (new): both passed.
    - Exact check of Lemma `lem:dp`: the two-pass messages, `A_t`, β, all
      min-marginals, and root-outward recovery of a minimizer.
    - A mutated message rule fails at once.
  - `coreA-cellwise.py 13 200`, `coreA-growthcert.py 17 300` and
    `coreA-verify-cert.py 23 200`: all passed.
  - `latexmk -pdf -interaction=nonstopmode -outdir=build/coreA-verify
    main.tex`:
    - From an empty build directory, latexmk hit two transient
      `\@@BOOKMARK` errors from an intermediate bookmark file. One more
      `pdflatex` pass exited 0.
    - The final log has no errors, no overfull or underfull boxes, no
      undefined references and no multiply defined labels in the whole
      build.
- **Pass 1:**
  - `coreA-verify-cert.py 3 200` and `… 11 200`: both passed. A mutation
    that makes (C1) unsound fails at once.
  - `coreA-cellwise.py 5 200` and `coreA-growthcert.py 9 300`: both passed.

## (6) Unresolved

- The intro scope sentence (front's file) stays imprecise for weighted growth
  until the request in (3) is applied.
- Bajaj–Hasan's theorem number and constant convention remain unverifiable
  (paywalled). The text depends on neither.
