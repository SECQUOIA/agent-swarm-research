# W5 report: group tu (sections/constraints.tex, sections/appendix-tu.tex)

Only these two files were edited. One check script was added:
`process/w3/checks/tu-w5-polycurv.py`.

## 1. Cut-plan items

| Item | Status | Change |
|---|---|---|
| 8.6: keep eq:tu-constants paragraph and thm:tu-exact; move TU-EXACT box and remaining text | done | The TU-EXACT box and the cost paragraph after it moved to App. E.4 (`app:tu-snap`, retitled "The algorithm TU-EXACT and snapping on rows"). They now come before Lemma lem:tu-snap, which uses steps (i)-(ii). The main text keeps the eq:tu-constants paragraph, the acceptance sentence and the statement of thm:tu-exact. A 7-line description of TU-EXACT was added, because the theorem refers to the algorithm. A one-sentence pointer to the proof (App. E.5) remains. In (c), "steps (i)-(iii)" became "recovery and the acceptance test", since the step numbers are no longer in the main text. |
| 8.7: move prop:tu-misaligned, its numerical instance and ex:tu-sum | done | Moved to App. E.6 (`app:tu-limits`, under a "Non-uniform alternatives" paragraph). The separate verification paragraphs were merged into the example and the instance text. The main text keeps the prescribed sentence (pointing to `app:tu-limits`) and one sentence on why each alternative fails. |
| Move rem:tu-curv, prop:tu-align, ex:tu-union | done | rem:tu-curv and prop:tu-align moved to the new App. E.1 (`app:tu-model`). ex:tu-union moved to the new App. E.2 (`app:tu-union`). Section 8.1 keeps one paragraph: alignment takes $1+\sum_k\lvert Z_k\rvert$ vector tests, (8.2) has polynomial-time rational checks, (8.2) with $\mathcal W=\R^{n_c}$ implies coordinate curvature, and Example ex:tu-fullcurv shows that coordinate curvature is not enough. Section 8.4 keeps one sentence on why step (3) filters by unions (hull: $2^j+1$ nodes; union: a number bounded independently of $j$). |
| Optional HS sentence | done (1 sentence) | Section 8 introduction: "The levels of the algorithm resemble the scaling phases of Hochbaum and Shanthikumar [HS90] for separable convex objectives; Section 2 compares the two." rem:tu-bm is unchanged, as the C-literature-1 verifier asked. **This sentence depends on the front group adding the HS comparison to related.tex (see section 4).** |

Appendix E now has six subsections:

- E.1 Checking the model
- E.2 Union versus hull filtering
- E.3 Stationary face polytopes and rational height
- E.4 The algorithm TU-EXACT and snapping on rows
- E.5 Exact output
- E.6 Details for Section 8.7

The appendix title is now "Coupling constraints: checks, exact output and examples". The notation paragraph ($\phi_z$, $\hat A_{\mathcal J}$, integrality) moved from the appendix opening to the start of E.3, where it is first used. All dependencies stay available:

- The moved proofs use only Section 8 definitions that remain in the main text: def:tu-model, eq:tu-align, eq:tu-curv, eq:tu-setgrowth, def:tu-domain, TU-GRID, and the Section 8.6 constants.
- They also cite results in other sections: def:curvature, lem:intcurv, def:graded, lem:tu-allow, thm:tu-states, prop:sharp and cor:uniformgrid.

### Page savings (measured from builds, using `\pdfsavepos` markers before and after each `\input`)

Lengths are in pages of 9 in text height.

| Build | Section 8 | Appendix E |
|---|---|---|
| Before (snapshot `sections-before-w5`, `/tmp/w5-tu-before`) | pp. 44-53, 8.99 pages | pp. 112-116, 3.71 pages |
| After, isolated (snapshot for all other files, my two files current; `/tmp/w5-tu-iso-m`) | pp. 44-52, 7.52 pages | pp. 111-117, 5.92 pages |
| After, current tree (all agents' current files; `/tmp/w5-tu`) | pp. 44-52, 7.66 pages (sec:constraints p. 44, sec:optsets p. 52) | pp. 107-112, 5.87 pages (app:tu p. 107, app:proximal p. 113) |

**Main-text saving: 1.47 pages** (isolated measurement). This is less than the moved material suggests, for two reasons:

- The 8.6 theorem needed a short description of TU-EXACT.
- Section 8.1 needed a pointer paragraph for the curvature and alignment checks, because the certificate claim of thm:tu-approx depends on them.

The appendix grew by 2.21 pages. This includes the new polynomial curvature check (M-tu-optsets-1).

A further 0.5 page could be saved by moving rem:tu-bm to App. E. This is not in the cut plan. intro.tex and related.tex cite the remark by label only, so their references would survive. I did not do it.

## 2. Assigned findings

| Id | Verdict | Reason | Change |
|---|---|---|---|
| M-tu-optsets-1 | ACCEPTED | The paper gave no checkable certificate of (8.2) for non-quadratic factors, yet thm:tu-approx claims certification for them. | rem:tu-curv (now App. E.1) has item (i) for explicit polynomial factors of fixed degree and any $\mathcal W$. For continuous $i,i'$, $b_{ii'}=\sum_m\lvert c_m\rvert\max\{\lvert\underline\mu_m\rvert,\lvert\overline\mu_m\rvert\}$ over the monomials of $\partial_{ii'}F$. The monomial ranges are taken on $[\ell,u]\times\prod_k[\min Z_k,\max Z_k]$ and computed as in lem:intcurv. Every positive rational $\ge\max_i\sum_{i'}b_{ii'}$ is a valid $\bar L$ (row-sum bound on the largest eigenvalue). The remark also gives the polynomial cost, and notes that for quadratics this is exactly the old row-sum test. Item (ii) keeps the two quadratic tests for $\mathcal W=\ker C$. The certificate record in 8.3 now cites rem:tu-curv, and Section 8.1 states that the checks exist. Indices $i,i'$ replace the reviewer's $i,k$, because $k$ indexes the discrete coordinates $Z_k$ in the same formula. |
| M-tu-optsets-2 | MODIFIED | The quantifier issue is real. The reviewer's fix covers TU-GRID only. However, the proof of thm:tu-exact cites prop:tu-sound(e) at TU-EXACT levels, and rem:tu-cf cites prop:tu-sound(d) and thm:tu-states(c) there. TU-EXACT runs TU-GRID without the stopping test. | prop:tu-sound: "Consider TU-GRID or its hull variant, with or without the stopping test of step (2). For every level $j$ that is reached, (a), (b) and (e) hold, and (c) and (d) hold if step (3) is executed at level $j$". thm:tu-states: "Run TU-GRID with or without the stopping test of step (2). For every level $j$ at which step (3) is executed". (c) still covers the hull variant. |
| M-tu-optsets-3 | ACCEPTED | Off by one: levels are numbered from 0. | thm:tu-exact(c): "hence at the latest at level $J_{\rm ex}=\dots$". The trailing "levels" was removed. The cost sentence ("$J$ replaced by $J_{\rm ex}$") was already correct. |
| C-consistency-4 (my files) | MODIFIED | The point $m$ in prop:tu-misaligned clashes with the row count $m$ and the min-marginals $m_i$. The suggested $\mu_0$ would clash with $\mu_0$, the level-0 grid minimum of TU-GRID (step (1), "If $\mu_0=+\infty$"). | The point is renamed $\bar t$ (unused elsewhere) in prop:tu-misaligned, eq:tu-gap, the proof, the instance and the graded-grid paragraph. The dummy node variable $\nu$ there became $t$. In thm:tu-states(b), "at most $r_i$ points" became "if $\mathcal S_i$ is finite" with the factor $\lvert\mathcal S_i\rvert$. (c) now reads "the bound in (b) holds". The follow-up sentence uses $\prod_i\lvert\mathcal S_i\rvert$, and ex:tu-union says "every projection $\mathcal S_i$ has two points". The row count $m$ and min-marginals $m_i$ are unchanged (reserved/standard). The Table 2 entry for $r$ is a request to the setting.tex owner (section 4). |
| C-consistency-5 (my files) | ACCEPTED (my part) | $\nu$ was an integer counter in lem:tu-uniform but means negative curvature elsewhere. | In lem:tu-uniform, its proof and the counting paragraph, $\nu\to k_0$. coreB uses the same $k_0$ in Cor 5.7 / App. A, so the "as in the proof of Corollary cor:uniformgrid" reference matches. The dummy $\nu\in\mathcal S_i$ in the proof of thm:tu-states(b) became $t$. TU mesh unit $\eta$: no rename (it is defined in def:tu-model and used throughout Section 8); a Table 2 entry is requested (section 4). |
| C-literature-1 (my files) | ACCEPTED (my part) | The verifier says to leave rem:tu-bm unchanged and put the comparison in related.tex only. | rem:tu-bm is unchanged. One pointer sentence was added in the Section 8 introduction, as the cut plan allows. It does not repeat the comparison. |
| R-referee-4 (my files) | ACCEPTED (my part), no text change | For my files: $\eta$ (TU mesh unit) is defined locally in def:tu-model, and $J$ in Section 8 is the last level, which is the stage-limit meaning in Table 2. $r$ is the number of optimal values per coordinate, consistent with Sections 9-10, Table 1 and the intro. No $e_i$ or unsubscripted $R$ occurs; the radii in lem:tu-uniform are already $\rho_j$. | None in my files; a Table 2 request is in section 4. |

## 3. Labels

No label was deleted or renamed.

- **Moved from constraints.tex to appendix-tu.tex:**
  - `rem:tu-curv` and `prop:tu-align` → App. E.1
  - `ex:tu-union` → App. E.2
  - `alg:tuexact` → App. E.4
  - `prop:tu-misaligned`, `eq:tu-gap` and `ex:tu-sum` → App. E.6
- **New labels:** `app:tu-model` (E.1) and `app:tu-union` (E.2).

External references to the moved labels still resolve: conclusion.tex cites prop:tu-misaligned and ex:tu-sum. No file outside my group references `alg:tuexact`, `rem:tu-curv`, `prop:tu-align`, `ex:tu-union` or `eq:tu-gap`.

## 4. Requests for other files

1. **front (related.tex):** The Section 8 introduction now says that Section 2 compares the levels of TU-GRID with the scaling phases of Hochbaum and Shanthikumar. Please add the HS comparison from the C-literature-1 verifier's corrected_fix (and the Meyer1977 sentence, if the coordinator adds the key). If the comparison is not added, the clause "; Section~\ref{sec:related} compares the two" in constraints.tex line 13 must be deleted.
2. **setting.tex owner (Table tab:notation):**
   - Add a row for the TU mesh unit: "$\eta$, $h_j=\eta2^{-j}$ & mesh unit and level-$j$ mesh under coupling constraints & Def.~\ref{def:tu-model}". (C-consistency-5, R-referee-4)
   - Add a row: "$r$ & largest number of optimal values of a coordinate (Sections 8-10); number of private blocks in Section 7". (C-consistency-4, R-referee-4)
3. **coordinator:** None for appendix.tex; the input list is unchanged.

## 5. Checks run (targeted; no project-wide verification, CI not inspected)

- **`python3 -B process/w3/checks/tu-w5-polycurv.py` (new): PASS.** This checks the M-tu-optsets-1 bound:
  - 60 random rational polynomials of degree at most 4 in 3 continuous variables and 1 discrete variable, on random boxes;
  - $\max_i\sum_{i'}b_{ii'}$ was compared with the largest Hessian eigenvalue at 200 random points each, with 0 violations;
  - for the quadratic instances, the bound equals the largest absolute row sum of $H_{xx}$.
- **`python3 -B process/w4/checks/M-tu-optsets-grids.py` (W4 script, re-run): ALL PASS.** It re-checks the numbers of the moved prop:tu-misaligned instances and ex:tu-sum, which are unchanged apart from the rename $m\to\bar t$.
- **Builds** (`latexmk -pdf -interaction=nonstopmode main.tex`, private copies):
  - `/tmp/w5-tu-before` (snapshot): baseline page numbers.
  - `/tmp/w5-tu-iso-m` (snapshot plus my two files): no errors, no undefined references, no overfull boxes. An overfull box (29.7 pt) in rem:tu-curv(i) was fixed by displaying the formula for $b_{ii'}$.
  - `/tmp/w5-tu` (current tree of all agents): exit 0, no errors, and no overfull or underfull boxes or warnings from constraints.tex or appendix-tu.tex. The only remaining warning is an undefined citation `AbelloEtAl2001` on p. 61, which is not from my files.
  - An earlier current-tree build failed on transient errors in appendix-growth.tex ("\lek_0", "\leR_j"), which was being edited by another agent at the time. They were gone in the final build.
- **Re-derivations:**
  - thm:tu-exact(c): with the thresholds $h_j\le\tau_{\rm TU}/(n_c\sqrt{\kappa_c})$ and $h_j\le2/(\Omega_{\rm TU}\sqrt{n_c\bar L})$, the conditions hold for every $j\ge J_{\rm ex}$, so the first qualifying level is at most $J_{\rm ex}$.
  - prop:tu-sound: (e) at the returning level uses (d) only at earlier levels, where step (3) was executed.
  - thm:tu-approx: the bound $K_j\le K$ for $j\ge1$ uses thm:tu-states at level $j-1$, where step (3) was executed.

## 6. Unresolved

- The HS pointer sentence depends on request 4.1.
- The main-text saving (1.47 pages) is below what the moved material suggests; see section 1 for the reasons and the rem:tu-bm option.

## Verification (W5 verifier for group tu)

I diffed both files against `process/w5/sections-before-w5/`, re-derived every changed statement and proof, re-ran the checks, and rebuilt. I found no mathematical error. I fixed four problems in the text; they are listed below. The assignment file `process/w5/assign/tu-verify.json` does not exist, so I verified against `process/w5/assign/tu.json`.

### Findings: adjudication checked

| Id | Revision verdict | Verifier result |
|---|---|---|
| M-tu-optsets-1 | ACCEPTED | **Confirmed, with one fix.** The math is correct. Monomial ranges bound each $\lvert\partial_{ii'}F\rvert$ on a box that contains $[\ell,u]\times\mathcal Z$. The largest eigenvalue is at most the largest absolute row sum, so the bound gives a valid $\bar L$ for every $\mathcal W$. The bit length $O(dI)$ and the quadratic case are also correct. **Fix:** rem:tu-curv(i) used $m$ as the monomial index, a fourth meaning of $m$ in Section 8 / App. E. prop:tu-align, directly below it, uses $m$ as the row count ($\Z^m$), and C-consistency-4 is about exactly this overload. The sum is now over exponent vectors $\alpha$, with $c_\alpha$, $\underline\mu_\alpha$ and $\overline\mu_\alpha$; $\alpha$ is unused elsewhere in both files. |
| M-tu-optsets-2 | MODIFIED | **Confirmed.** The extension "with or without the stopping test" is needed. At its returning level, TU-EXACT returns at step (iii) and skips step (3), so the reviewer's statement that "TU-EXACT runs step (3) at every level" is wrong at that level. I checked every use of the two statements: (b) and (e) at level $j$ use (d) only at levels $<j$; the bound $K_j\le K$ in thm:tu-approx uses level $j-1$; the proof of thm:tu-exact uses (e) only; rem:tu-cf uses (d) and thm:tu-states(c) only at filtering levels; lem:tu-uniform already says "at which TU-GRID filters". |
| M-tu-optsets-3 | ACCEPTED | **Confirmed.** I re-derived it: $h_{J_{\rm ex}}\le\tau_{\rm TU}/(n_c\sqrt{\kappa_c})$ gives $E_j\le\bar L\tau_{\rm TU}^2/(8n_c\kappa_c)\le g_S\tau_{\rm TU}^2/(4n_c)$, and $h_{J_{\rm ex}}\le1/(\Omega_{\rm TU}\sqrt{n_c\bar L})$ gives $E_j\le1/(8\Omega_{\rm TU}^2)$. So the first qualifying level is at most $J_{\rm ex}$. |
| C-consistency-4 | MODIFIED | **Confirmed.** $\mu_0$ is the level-0 grid minimum in TU-GRID step (1), so rejecting the reviewer's $\mu_0$ is justified. Correction to the report: $\bar t$ is not entirely unused, since appendix-recourse-convex.tex:392-396 uses it as a local step length inside a proof. That use is local to another appendix, so there is no clash. thm:tu-states(b),(c) with $\lvert\mathcal S_i\rvert$ is correct; in (c), $\mathcal S=\{v^*\}$ gives $\lvert\mathcal S_i\rvert=1$. |
| C-consistency-5 | ACCEPTED (my part) | **Confirmed.** $k_0$ matches growth-sharp.tex:38 and appendix-growth.tex:224-243. No $\nu$ remains in either file. The inequalities with $k_0$ were re-checked. |
| C-literature-1 | ACCEPTED (my part) | **Confirmed, with one fix.** rem:tu-bm is unchanged, as the verifier required. **Fix:** the pointer sentence sat between "...then carry over." and "The price is visible in two places", so "the price" read as if it referred to Hochbaum-Shanthikumar. It now ends the introductory paragraph: "Its levels resemble the scaling phases of Hochbaum and Shanthikumar [HS90] for separable convex objectives; Section 2 compares the two." **This still depends on front adding the comparison** (see Unresolved). |
| R-referee-4 | no text change | **Confirmed.** The requests to the setting.tex owner are the right place for this. |

### Cut-plan items checked

1. **8.6.** The TU-EXACT box and the cost paragraph (snapshot 519-545) moved to E.4 unchanged. The one exception is the clause defining $\hat A_{\mathcal J}$, which is now in the E.3 opening; that opening explicitly covers E.4 and E.5. Snapshot 561-566 is the end of the statement of thm:tu-exact and correctly stays. The proof pointer (568-571) stays as one sentence. The 7-line description of TU-EXACT in the main text matches steps (i)-(iii).
2. **prop:tu-misaligned, eq:tu-gap, its instances, ex:tu-sum.** All moved to E.6. I compared the text sentence by sentence with the snapshot (main text and appendix paragraphs), and nothing was lost. The main text keeps the prescribed sentence and one correct sentence on the reasons.
3. **rem:tu-curv, prop:tu-align, ex:tu-union.** All moved complete. **Fix:** the 8.1 pointer was a 10-line paragraph. The plan asks for one sentence, and "checks (8.2)" overstated item (i), which is a sufficient test. It is now one sentence: "Conditions (8.1) and (8.2) can be certified in time polynomial in $I$ (App. E.1): alignment by $1+\sum_k\lvert Z_k\rvert$ vector tests, without enumerating $\mathcal Z$ (Prop. E.2), and directional curvature, for quadratic and fixed-degree polynomial factors, by rational sufficient tests such as a bound on the absolute row sums of the continuous Hessian (Remark E.1)." The dropped clause (that (8.2) with $\mathcal W=\R^{n_c}$ implies coordinate curvature, and Example 8.5) remains in rem:tu-curv, and the Section 8 introduction states it.
4. **HS sentence.** Present; repositioned as described above.

**Further edit.** In 8.4, "This is why step (3) filters by unions of cells" followed a sentence on the size of $\mathcal S$, which does not explain the filter. It now reads: "Step (3) filters by unions of cells because one coordinate can have optimal values far apart: ...".

**Dependencies.**
- E.1 uses def:curvature, lem:intcurv, ex:tu-fullcurv, eq:tu-align, eq:tu-curv, and $H_{xx}$ from 8.6.
- E.2 uses thm:tu-states.
- E.3-E.5 use the 8.6 notation, which the E.3 opening states explicitly.
- E.6 uses the corrections of sec:grids, def:graded and lem:tu-allow.

All of these are available.

**Labels.** No label was deleted, and there are no duplicate labels in `sections/*.tex`. All moved labels resolve. conclusion.tex:64-65 cites prop:tu-misaligned and ex:tu-sum, and both resolve. Moved proofs keep their statements, so plain `proof` environments are correct; the moved proof of thm:tu-exact starts with "Proof of Theorem ...".

### Checks run (targeted; CI not inspected)

- `python3 -B process/w5/checks/tu-verify-curv-jex.py` (new): **ALL PASS.** It checks:
  - (1) rem:tu-curv(i): 80 random polynomials with 1-3 continuous and 0-2 discrete coordinates, of degree at most 4. At 30 random points each, the entry bounds are checked exactly with rationals and the eigenvalue bound numerically. In the quadratic case, $b_{ii'}=\lvert H_{ii'}\rvert$.
  - (2) the projector row-sum test of rem:tu-curv(ii), on 200 instances;
  - (3) thm:tu-exact(c): first qualifying level $\le J_{\rm ex}$, on 400 exact rational instances, including $\kappa_c=1$;
  - (4) the node count $\lfloor4a/h\rfloor+5$ of thm:tu-states(b), on 2000 cases.
- `python3 -B process/w3/checks/tu-w5-polycurv.py`: PASS.
- `python3 -B process/w4/checks/M-tu-optsets-grids.py`: ALL PASS.
- **Builds:**
  - `/tmp/w5-tu-verify` (current tree, task command): exit 0. No errors, no undefined references, and no overfull or underfull boxes from constraints.tex or appendix-tu.tex. The only warning is an undefined citation `AbelloEtAl2001` (limits.tex:270, p. 60), which is not in this group's files.
  - `/tmp/w5-tu-verify-iso` (snapshot plus the two verified files, with position markers): clean.
- **Pages:**
  - Current tree (`main.aux`): Section 8 pp. 43-51 (sec:optsets starts p. 51); App. E pp. 105-110 (app:proximal starts p. 111); 126 pages in total.
  - Isolated: Section 8 is 7.52 pages, unchanged by the verifier edits. The lines removed from 8.1 became vertical slack on p. 46, and the page breaks from p. 45 on are identical. App. E is 5.92 pages.

### Unresolved

- The HS pointer sentence (constraints.tex, end of the Section 8 introduction) says that Section 2 compares TU-GRID's levels with HS scaling. As of this verification, related.tex has no such comparison: HochbaumShanthikumar1990 is cited only at related.tex:115, and there is no front report. If front does not add the C-literature-1 comparison, delete "; Section~\ref{sec:related} compares the two" (or the whole sentence).
- The Table tab:notation rows for $\eta$ and $r$ (requests 4.2) are pending with the setting.tex owner.
