# W3 verification report — group `limits` (second pass)

Files verified and edited: `sections/limits.tex`,
`sections/appendix-lbproduct.tex`, `sections/appendix-moments.tex`. Details
are in the section "Verification, second pass" of `reports/limits.md`.

## 1. Adjudication check

Each assigned finding (`assign/limits.json`) was compared with the revising
agent's adjudication in `reports/limits.md` and with the current files.

| id | revising agent | verifier | note |
|---|---|---|---|
| F0 | MODIFIED | confirmed | TU paragraph matches CONVENTIONS §5. The abstract and intro belong to front. |
| F13 | ACCEPTED | confirmed | CT, TRIAL, TU-GRID and "nodes per coordinate" are used throughout. "CT (Algorithm ref)" now appears at the first use in §10.2 (this pass). |
| F27 | ACCEPTED | confirmed | "does real work" is gone. |
| F29 | ACCEPTED | confirmed | Lemma `lem:unique-growth` is referenced, and the random vector is Y. |
| F30 | ACCEPTED | confirmed | ETH and rETH are defined in §10.3 with citations. |
| F36 | MODIFIED | confirmed | As F0. |
| F44 | ACCEPTED | confirmed | "cannot be o(p)" everywhere, and the effective form is proved. |
| F52 | ACCEPTED | confirmed | The bullet has the CONVENTIONS §5 wording. |
| F53 | REJECTED (my part) | confirmed | The proposed wording is false after F178. `rem:grading` uses the restricted wording. |
| F55 | ACCEPTED | confirmed | Set growth uses g_S and κ_S. |
| F59 | ACCEPTED | confirmed | The files use 𝒮 and ξ_t, and the support of a binary x has no letter. |
| F65 | ACCEPTED | confirmed | As F13. |
| F68 | ACCEPTED | confirmed | Prop. `lim:prop:messages` is complete. |
| F70 | ACCEPTED | confirmed | g_S and κ_S are used with Def. `def:growth`. |
| F88 | ACCEPTED | confirmed | The opening paragraph is correct. |
| F90 | ACCEPTED | confirmed | V(v) is the right choice (m_i is reserved). Further clashes were fixed in this pass: q_l → φ_l, J, P_z. |
| F94 | ACCEPTED | confirmed | The files use L_i. |
| F134 | ACCEPTED | confirmed | Bienstock–Muñoz and Cifuentes–Parrilo are credited before Prop. `lim:prop:constraints`. |
| F146 | ACCEPTED | confirmed | The files cite NemirovskiYudin1983, DellEtAl2014, ChenEtAl2006 and CyganEtAl2015 Thm 14.21. |
| F147 | ACCEPTED | confirmed | The files cite KPR 2016, KAP 2024, Vorob'ev 1962 and Cifuentes–Parrilo. |
| F178 | ACCEPTED | confirmed | (a), (b) and (c) re-derived, and the example re-checked. |
| F180 | ACCEPTED | confirmed | The t_c argument and the first-Q argument are correct. |
| F181 | ACCEPTED | confirmed | The bullets and §10.3 have the CONVENTIONS wording. |
| F182 | ACCEPTED | confirmed | rETH is defined. The Clique → multicolored clique reduction and the effective o(p) are proved. |
| F183 | ACCEPTED | confirmed | The notation is fixed, and the uniqueness hypothesis is stated. |
| F184 | ACCEPTED | confirmed | The union bound is explicit. |
| F185 | ACCEPTED | confirmed | The files use L_i, and the sentence is rewritten. |
| F186 | MODIFIED | confirmed | Occupied widths are defined per feasible point. |
| F190 | ACCEPTED | confirmed | The decoding of α is proved. |
| F191 | ACCEPTED | confirmed | The L = 0 instance Ψ_0 has g = 1/n. |
| F192 | ACCEPTED | confirmed | The paragraph is simplified in this pass: it uses the f(p,κ) formula of Thm `thm:approx` directly. |
| F193 | ACCEPTED | confirmed | B^L_i, B^R_j, Y and Ψ_0. |
| F195 | ACCEPTED | confirmed | The files use CT, and the idiom is gone. |

Further fixes in this pass:
- Prop. `prop:oraclebarrier`: k → n, and `\abs` → `\norm`.
- Repeated sentence on DK uniqueness removed.
- appendix-moments: constant term c → F(0), and explicit sum ranges.
- appendix-lbproduct: wording.
- "toward" → "towards".

## 2. Labels deleted or renamed

None.

## 3. Requests for other files

None new. The earlier requests from `reports/limits.md` are already done:
- computation.tex uses Ψ_m and ξ_m and the restricted set-growth sentence;
- appendix.tex inputs lbproduct before moments;
- the constraints.tex discussion after Thm `thm:tu-approx` is present.

## 4. New BibTeX entries

None.

## 5. Checks run

- `python3 process/w3/checks/limits-verify-misc.py`: PASS. It covers:
  - Prop. `lim:prop:messages` parts 2 and 3;
  - the identities and counting of Prop. `prop:oraclebarrier`;
  - Prop. `prop:lbwidth`, exhaustively for all 75 graphs with n ≤ 4;
  - the padding claim.
- `limits-setgrowth.py`, `limits-reductions.py`, `limits-moments.py` and
  `limits-verify-setgrowth.py`: all PASS.
- `latexmk -pdf -interaction=nonstopmode -outdir=build/limits-verify
  main.tex`: exit 12.
  - Cause: the shared root `main.aux`/`main.bbl` is rewritten by concurrent
    builds, and latexmk stopped with "Maximum runs of pdflatex reached".
  - The pdflatex log has no errors and no overfull boxes.
- Isolated snapshot (`/tmp/lv2copy`): exit 0.
  - No errors, no undefined references or citations, no multiply defined
    labels, no overfull boxes and no warnings.
  - I read the rendered Section 10 and Appendix G.

No project-wide verification was run, and CI was not consulted.

## 6. Unresolved

- It is open whether every valid path certificate for the set-growth family
  needs ε^{−Ω(1)} nodes in total. The paper states this.
- I did not check these against primary sources:
  - the Del Pia–Khajavirad construction details in Remark `lim:rem:dk`;
  - the Bienstock–Muñoz locator "Appendix A";
  - Cygan et al. Theorem 14.21.
