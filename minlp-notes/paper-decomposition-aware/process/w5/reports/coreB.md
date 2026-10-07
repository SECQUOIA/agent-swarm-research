# W5 report: coreB (growth.tex, growth-sharp.tex, appendix-growth.tex)

## 1. CUTPLAN item

**Item:** move the numeric part of the proof of Lemma `lem:states`
(growth.tex 162-174 of the snapshot) to Appendix A, and keep the main
argument in the main text.

**Done.**

- The main-text proof keeps the localization argument and the step that
  bounds the next grid. That step uses `theta R_ij / h-hat <= 4 sqrt(2 n_P) + 1/4`
  and Lemma `lem:graded`(b) to bound the grid by
  `1 + 2 ceil((4/theta) ln(5/4 + 4 sqrt(2 n_P))) <= K(theta, n_P)` nodes. It
  ends with "(Appendix A)" and keeps the stage-0 and `i not in P` cases.
- The calculus showing this is at most `10 theta^{-1} ceil(log2(n_P+2))` is
  now a separate block in Appendix A:
  `\begin{proof}[Proof of the bound $K(\theta,n_P)$ in Lemma~\ref{lem:states}]`.
  It covers `phi`, the values `phi(1)` and `phi(2)`, and the derivative
  comparison. The block sits right after the proof of Lemma `lem:graded`, so
  everything it uses (`lem:graded`(b), `K`, `theta <= 1/4`) is defined before
  it.

**Page measurements.** Both builds are in private copies with identical
files from the other groups:

- `/tmp/w5-coreB-orig`: my three snapshot files.
- `/tmp/w5-coreB`: my edited files.

| | Section 5 | Appendix A |
|---|---|---|
| Rendered text lines (pdftotext) | 292 -> 290 | 206 -> 211 |
| Position of the section heading on its page (fraction of the page) | 18.00-23.72 -> 18.00-23.75 | 86.84-90.46 -> 86.84-90.55 |
| Total PDF | 126 pp. in both builds | |

**Net effect on the main text: about zero.**

- The move itself saves about 5 rendered lines.
- The finding fixes add about the same:
  - the R-referee-6 existence sentence;
  - the C-writing-14 clause;
  - the definition of `Gamma_F`;
  - the subsection heading required by C-writing-7.
- The shortened lower-bound sentence in Remark `rem:fpt` makes up part of
  this.

I did not move more of Section 5. The plan keeps the main line (Sections
3-6) fully proved in the main text.

**Page span of my sections** (current build, other groups' files as of
12:59):

- Section 5: pp. 18-23 (`sec:growth` p. 18, `sec:exact` p. 23).
- Appendix A: pp. 86-90 (`app:growth` p. 86, `app:localized` p. 90).
- Pre-W5 snapshot: Section 5 pp. 17-23, Appendix A pp. 92-96.

## 2. Adjudication of the assigned findings

There is no `verifier` field for any of these minor findings, so the
reviewer's fix was the reference. Only my three files were edited.

| id | verdict | reason / change |
|---|---|---|
| M-core-1 | ACCEPTED | The denominator bound contains `J`, so "do not grow with the number of stages" is inaccurate. **growth.tex** (proof of Thm 5.7(b)): "so one bound holds at all stages of a trial: denominators do not compound from stage to stage". **appendix-growth.tex** (bit lengths): "So the bound does not compound from stage to stage; it depends on the stage limit only through the term $j_{\max}$ in $\alpha$." The remark after TRIAL also said "all denominators stay bounded". It now says "denominators do not compound from stage to stage (Appendix A)". |
| M-core-2 | MODIFIED | Kept `rho = sqrt(k n_P)` and `rho = sqrt(n kappa)` in the two localization proofs. Renamed the block variable of Example `ex:family` to `omega_b` (statement and App. A proof). The proposed `r_0`, `r_j` would clash with the reserved Section 5 scale `r_i = 2^{-varpi_i}`. I used `R_0` and `R_j` instead; in Section 5 and App. A, `R` with subscripts already denotes a radius (Lemma `lem:graded`(b), `R_ij`, the (G5) proof). So: the box half-width of Prop `prop:sharp` is `R_0` (statement and proof); the induction radius in the proof of Cor `cor:uniformgrid` is `R_j`; the radius of the graded part of Cor `cor:uniformgrid` is `R_0`, which is exactly the Proposition's `R_0` with `h = h_j`. |
| M-core-3 | ACCEPTED | growth.tex: "needs only $O(1+\theta^{-1}\log(1+\theta R/h))$ nodes". |
| M-limits-1 | ACCEPTED (by removal) | The imprecise rETH summary in Remark `rem:fpt` is gone (see C-writing-5 / R-referee-2). The remark now refers to Theorem `thm:intro-lower`, whose part (c) is stated precisely. The other locations belong to front and limits. |
| C-consistency-4 | NO CHANGE in my files | The `r_i` clash is fixed on the Section 8 side (tu: write `\|S_i\|` in Thm 8.10(b)). The rows for `r`, `m` and `mu_0` are coreA's and tu's. Section 5 keeps `r_i = 2^{-varpi_i}`. |
| C-consistency-5 | ACCEPTED (my part) | Integer counter `nu` -> `k_0` in Cor `cor:uniformgrid` and its proof. The other items (`eta`, `P`, `q`, ETH, Lemma E.6) are in other groups' files. |
| C-consistency-6 | ACCEPTED (my part) | growth.tex, proof of Thm 5.7(b): "Let $\Gamma_X$ and $\Gamma_F$ be the products of the denominators of the box endpoints and of the coefficients." The `C_2` part belongs to exact. |
| C-writing-5 | ACCEPTED (my part) | Remark `rem:fpt` was rewritten following the reviewer's text for (b). It keeps the technical points: exponent 5, `q` only through `log(1/eps)`, `log` factor absorbed by (5.4), no bound on bags, Hessian norms or local minima, Korhonen. The five-line lower-bound summary is replaced by "Theorem~\ref{thm:intro-lower} states the lower bounds, proved in Section~\ref{sec:limits}; they are stated for $\kappa$ and apply to $\bar\kappa$, which can always be taken at most $\kappa$." The last clause keeps the one technical point of the old text, that the bounds transfer to `kappa-bar`. Parts (a), (c), (d) and (e) of the finding concern other files. |
| C-writing-7 | MODIFIED | `\input{sections/growth-sharp}` moved from after Lemma `lem:states` to just before `\subsection{Examples}`. growth-sharp.tex now opens with `\subsection{Sharpness of the localization radius}` (it was a `\paragraph`). The references to Thm `thm:approx`, Rem `rem:fpt` and Lemma `lem:commonmesh` now point backward. In Cor `cor:uniformgrid` I wrote "run the stages of a trial with a common mesh (Lemma~\ref{lem:commonmesh}) without a cap, with $h_j=s2^{-j}=2^{1-j}$, uniform grids ... and initial center $0$". The suggested "stages of CT with a common mesh" would be inaccurate, because CT runs several trials with `theta = 2^{-mu}`, while the corollary uses one trial with `theta = 0`. The opening sentence also cites Lemma `lem:commonmesh` next to `lem:states` for the radius `Theta(sqrt(n kappa) h_j)`. The Appendix A proofs were reordered to follow the new order: Lemma `lem:graded`, `K` bound of `lem:states`, bit lengths, `lem:commonmesh`, `prop:sharp`, `cor:uniformgrid`, examples. |
| C-writing-8 | ACCEPTED (my part) | coreA added Cor `cor:filtercert` in grids.tex. It is cited in three places: the proof of Thm 5.7(a) ("validity follows from Corollary~\ref{cor:filtercert}, because every threshold is the value of a feasible point"); the remark after TRIAL; and the "CT with a common mesh" part of the proof of `lem:commonmesh` (App. A). Each of these places previously cited Thm `thm:certificate`. |
| C-writing-10 | ACCEPTED (my part) | (a) Stage limit `J` -> `j_max` everywhere in my files: TRIAL, CT, the proof of Thm 5.7, Lemma `lem:commonmesh`, and the App. A bit lengths and termination. The double-index mesh is written `h_{i,j_{\max}}` for readability. (c) Thm 5.7 now defines `f(p,t)=c_0(c_1 p sqrt t)^p t (1+log_2 t)^2`. Other files: see the requests below. |
| C-writing-14 | ACCEPTED | Thm 5.7(b): "Neither $\gamma$ nor $\bar\kappa$ is an input. Since $f$ is increasing in $t\ge1$, the bound also holds with any larger number in place of $\bar\kappa$, such as the Euclidean condition number $\kappa$ under point growth." `f` is increasing only for `t >= 1`, which suffices because `kappa-bar >= 1`. |
| R-referee-2 | ACCEPTED (my part) | The lower-bound summary in Remark `rem:fpt` is replaced by a reference (see C-writing-5). |
| R-referee-6 | ACCEPTED | Remark `rem:fpt`: "As the parameter we take the smallest weighted condition number of the instance. It exists: since weighted growth determines $x^*_P$ and $\norm{x-x^*}_{\mathbf L}$ depends only on $x_P$, the valid constants in (3.3) form a set $(0,\gamma^*]$ or $(0,\infty)$, and the minimum is $\max\{1,1/\gamma^*\}$ or $1$." See note (i) below. |
| R-referee-4 | MODIFIED (my part) | **Exponent `e_i`:** renamed to `varpi_i` (`4^{varpi_i-1} < L_i <= 4^{varpi_i}`, `r_i = 2^{-varpi_i}`) in growth.tex and the App. A bit lengths (`|varpi_i|`, `2^{E-j-varpi_i}`, `alpha`). `\varpi` was unused in the paper. exact.tex and appendix-recourse-convex.tex already refer to "the integer exponents that define the meshes `h_ij`", so they need no change. **`J`:** see C-writing-10. **Radius `R`:** not renamed, because in Section 5 and App. A `R` (with subscripts `ij`, `0`, `j`) consistently denotes a radius defined at each use, and the reserved height constant `R` of Section 6 does not occur there. Renaming the radii to `rho`, as the finding suggests, would clash with `rho = sqrt(k n_P)`, which M-core-2 keeps. **`eta`:** unchanged in my files, where it is only the reserved stage scale `eta_j`. |

**Note (i), R-referee-6.** The existence argument behind the new sentence:

- Weighted growth determines `x*_P`. If `x*` witnesses (3.3) with `gamma_0`
  and `x**` is any minimizer, then `0 = F(x**) - OPT >= gamma_0 ||x** - x*||_L^2`.
- So the valid set is
  `{gamma > 0 : F(x) - OPT >= gamma ||x - xbar||_L^2 for all x}` for one fixed
  witness `xbar`.
- Each inequality is closed in `gamma` and preserved when `gamma` decreases,
  so the set is `(0, gamma*]` or `(0, inf)`. The second case occurs, for
  example, when `P` is empty.
- Hence `min max{1, 1/gamma}` is attained.

## 3. Labels

- No label was deleted, renamed or moved to another file.
- `prop:sharp` and `cor:uniformgrid` moved within Section 5: they are now
  Prop 5.10 and Cor 5.11, in the new Section 5.4, after Lemma
  `lem:commonmesh` (5.9).
- Thm `thm:approx` is now 5.7, Rem `rem:fpt` 5.8, Lemma `lem:commonmesh`
  5.9, and the examples 5.12 and 5.13.
- The proofs in Appendix A were reordered within the file. The new proof
  block for the `K` bound has no label.

## 4. Requests for other files

1. **coreA, setting.tex Table `tab:notation`** (row "`$J$ & also the number
   of refinement stages (stage limit)`", currently line 181): replace it by
   "`$j_{\max}$ & stage limit of TRIAL and CT & \S\ref{sec:growth}`", or
   delete it (C-writing-10a).
   - Optional, for R-referee-4: add "`$\varpi_i$, $r_i$ & curvature exponent
     and scale, $r_i=2^{-\varpi_i}$ & \S\ref{sec:growth}`".
   - Optional: note that in Section 5 and App. A a subscripted `R` is a
     local radius.
2. **recA, appendix-recourse-convex.tex 21 and 23:** the CT stage limit is
   now `j_max`. Write `c(j_{\max}+1)pI^2(60p\sqrt{\kappa_V})^p` and "so
   `j_{\max}=O(\pi_L(I)+q)`".
3. **computation, computation.tex 26-27:** "the stage limit is the least
   `$J$` with `$\frac78Lns^24^{-J}\le\varepsilon$`" -> use `$j_{\max}$`, for
   consistency with Section 5.
4. **front / limits (optional, C-writing-10c):** intro.tex already uses
   `f(p,t)`. Two places still write the formula with `kappa`: conclusion.tex
   54 and limits.tex 168. appendix-lbproduct.tex 161 does the same. These are
   evaluations at `kappa`, so they are correct as they stand; switch them to
   the `t` form only if consistency is wanted.
5. **front (R-referee-6):** the intro paragraph "Parameterized form" can cite
   Remark `rem:fpt` for the smallest `kappa-bar` instead of repeating the
   existence argument.

## 5. Checks run (targeted, local; not CI)

- **Numeric check of the moved bound:** `python3
  process/w3/checks/coreB-w5-kbound.py`. It checks:
  - `phi(1) = 16.2101 < 16.3` and `phi(2) = 18.5470 < 18.6`;
  - `phi'(m) <= 4/m` and `d/dm 10 log2(m+2) >= 7.2/m` for `m <= 10^5`;
  - the bound `1 + 2 ceil((4/theta) ln(5/4 + 4 sqrt(2m))) <= 10 theta^{-1} ceil(log2(m+2))`
    directly for `theta = 2^{-mu}`, `mu = 2..12`, `m = 1..10^5`.

  Result: OK, 0 violations.
- **Build:** `rm -rf /tmp/w5-coreB && mkdir -p /tmp/w5-coreB && rsync -a main.tex macros.tex references.bib sections figures /tmp/w5-coreB/ && cd /tmp/w5-coreB && latexmk -pdf -interaction=nonstopmode main.tex`.
  - The final build has no LaTeX errors and no undefined references.
  - All 30 `\ref` targets used in my files resolve in `main.aux`.
  - It has one undefined citation, `AbelloEtAl2001` (p. 61, not my files).
  - It has one overfull box, in appendix-tu.tex lines 19-34 (not my files).
  - Nothing in my files is overfull.
  - An earlier build caught `\leR_j` and `\lek_0` concatenations left by
    the renames; these are fixed.
- **Comparison builds:**
  - `/tmp/w5-coreB-orig`: the same tree with my three snapshot files, used
    for the page comparison.
  - `/tmp/w5-coreB-before`: the full pre-W5 snapshot, used for the "before"
    span.
- **Labels:** the label sets of all three files are identical to the snapshot
  (`diff` of the `\label` lists).

## 6. Unresolved

- After the change, the main text of Section 5 is not shorter (see Section
  1). The CUTPLAN item was done as specified, but the required finding fixes
  cost about the same space. Further savings would mean moving
  main-line proofs (for example the termination argument of Thm 5.7(a)),
  which the plan does not ask for.
- The requests in Section 4 are open until the owners act on them.

## Verification

The verifier diffed `sections/growth.tex`, `sections/growth-sharp.tex` and
`sections/appendix-growth.tex` against `process/w5/sections-before-w5/`. It
re-derived every changed statement and fixed the problems below directly in
these files. `process/w5/assign/coreB-verify.json` does not exist, so the
findings were checked against `process/w5/assign/coreB.json` (15 findings,
none with a `verifier` field).

### Outcome

- **CUTPLAN item: done and complete.** Every removed sentence of the
  snapshot (growth.tex 162-174) is in the new Appendix A block: the
  definition of `phi`, the step `3 <= 3/(4 theta)`, `phi(1)`, `phi(2)`, the
  derivative comparison and the conclusion. The block also states the step
  `ceil(x) < x+1`, which the old text left implicit. It uses only Lemma
  `lem:graded`(b) and eq. `eq:statecap`, which come before it. The stage-0
  and `i not in P` cases stay in the main text.
- **Labels.** The label sets of the three files equal the snapshot's. No
  label is duplicated in the paper.
- **Findings.** All 15 adjudications are justified, and the changes match
  the stated reasons. The R-referee-4 rename (`e_i` to `varpi_i`) is
  consistent with coreA's notation table (setting.tex 185). M-core-2 uses
  `omega_b`, a local example variable; `omega` has no reserved meaning in
  CONVENTIONS. C-writing-7 is correct: the corollary runs one trial with
  `theta = 0`, so "a trial with a common mesh" is the accurate wording.
  C-writing-14 is correct: `f` increases for `t >= 1`, and `kappa-bar >= 1`.
  M-core-1 is correct, because `alpha` contains `j_max`.

### Problems found and fixed

1. **`R_0` with two values in the proof of Cor `cor:uniformgrid` (from the
   M-core-2 rename).** The induction radius `R_j = min{1, 2(k_0+1)h_j}` has
   `R_0 = 1`. The graded rule had been renamed to
   `R_0 = h_j sqrt((n-2)kappa/16)`, so one proof gave `R_0` two different
   values. **Fix:** the graded radius is plain `R` again, as before W5, in
   growth-sharp.tex (corollary statement) and appendix-growth.tex (graded
   rule: "Apply Proposition ... with h = h_j and R_0 = R"). The notation
   table already lists "radius R in Section 5". `R_0` remains the half-width
   parameter of Prop `prop:sharp`. The stage-0 instance "h = 1 and R_0 = 1"
   agrees with `R_0 = 1` of the induction.
2. **Rem `rem:fpt` repeated the existence argument for the smallest
   `kappa-bar` (R-referee-6).** coreA has added the same argument, with the
   definition "as a parameter of the instance, kappa-bar denotes this value",
   to Section 3 after Def `def:growth` (setting.tex 102-111). **Fix:** the
   remark now reads "As a parameter, kappa-bar is the smallest weighted
   condition number of the instance, which exists by
   Section~\ref{sec:setting}. It is a real number, not part of the input,
   and CT never computes it." R-referee-6 stays resolved, and the CONVENTIONS
   FPT wording is kept.
3. **Last sentence of `rem:fpt` (C-writing-5, M-limits-1).** It now reads
   "since kappa-bar <= kappa, the bounds stated for kappa also apply to
   kappa-bar" (Section 3 proves `kappa-bar <= kappa`). This is the correct
   transfer: a running time `T(kappa-bar) <= T(kappa)` that beat a lower
   bound stated for `kappa` would contradict it.
4. **Ambiguous pointer in the proof of Lemma `lem:states`.** The text
   "... <= K(theta,n_P) nodes (Appendix A)" now reads "... nodes, which is at
   most K(theta,n_P) by a calculus estimate in Appendix~\ref{app:growth}". It
   now says which step is proved in the appendix.

### Re-derivations (all correct)

- **Moved bound.** `1+2ceil(y) < 3+2y <= theta^{-1}phi(n_P)` for
  `theta <= 1/4`. `phi(1) = 16.2101`, `phi(2) = 18.5470`.
  `m phi'(m) = 16x/(5/4+4x) < 4` with `x = sqrt(2m)`.
  `10/((m+2)ln 2) >= 7.2/m` for `m >= 2`.
- **Main-text step.** `theta R_ij/hat h <= 16 theta rho + theta
  <= 4 sqrt(2n_P) + 1/4`, using `hat h >= h/2`, `hat h >= 1` for `i in I_Z`,
  and `theta sqrt k <= 1/sqrt 8`.
- **Bit lengths.** The node formula
  `h_ij((1+theta)^k-1)/theta = 2^{E-j-varpi_i}((2^mu+1)^k-2^{mu k})/2^{mu(k-1)}`
  holds, and its 2-adic exponent is at most `alpha`.
- **Prop `prop:sharp`.** The completed square, the bound
  `Q_1(a,v_a) <= 2g(Lambda-g)a^2/Lambda` and the threshold
  `(n-2)h^2 kappa^2/(16(kappa-1)) >= (n-2)h^2 kappa/16` hold.
- **Graded rule of Cor `cor:uniformgrid`.** `t_k = h'((1+theta)^k-1)/theta`
  holds.
- **Rem `rem:fpt`.** `f(p,t)` is increasing for `t >= 1`.

### Checks run (targeted, local; not CI)

- `python3 process/w5/checks/coreB-verify-kbound.py`. It checks the items
  under Re-derivations with sympy and exact fractions, plus a direct check of
  the `K` bound for `theta = 2^{-mu}` (`mu = 2..13`) and 40 random
  `theta in (0, 1/4]`, with `m` up to `10^9`. Result: OK, 0 violations.
- **Labels:** `diff` of the `\label` lists against the snapshot (identical),
  and a duplicate-label scan over `sections/*.tex` (none).
- **Build** in `/tmp/w5-coreB-verify` (rsync of main.tex, macros.tex,
  references.bib, sections, figures; `latexmk -pdf -interaction=nonstopmode
  main.tex`). Result: 126 pages, no LaTeX errors, no undefined references,
  no overfull boxes. One undefined citation, `AbelloEtAl2001` (p. 60), is
  not in coreB files.
- **Comparison build** `/tmp/w5-coreB-verify-agent`: the same tree with the
  revision agent's versions of the edited passages. Rendered lines (pdftotext,
  non-empty):

  | | Section 5 | Appendix A |
  |---|---|---|
  | Revision agent's version | 376 lines (17.00-22.80) | 327 lines (83.43-87.24) |
  | After verification | 373 lines (17.00-22.68) | unchanged |

  The verifier's edits shorten Section 5 by 3 rendered lines.

### Page span after verification (from `/tmp/w5-coreB-verify/main.aux`)

- Section 5 (`sec:growth`): pp. 17-22. `sec:exact` starts on p. 22.
- Appendix A (`app:growth`): pp. 83-87. `app:localized` (B.1) starts on
  p. 87.

### Status of the cross-file requests in Section 4

- **Closed:**
  - Request 1 (coreA, setting.tex): the table has `j_max`, `varpi_i` and
    the radius note.
  - Request 2 (recA, appendix-recourse-convex.tex): uses `j_max`.
  - Request 5 (front, intro.tex 107-111): cites Section 3 and Rem
    `rem:fpt`.
  - C-consistency-4 (tu): `r_i` no longer occurs in Section 8.
- **Open:**
  - Request 3, computation: the stage-limit sentence has moved to
    `appendix-computation.tex` 14-16 and still uses `J`
    ("least `$J$` with `\frac78Lns^24^{-J}`...").
  - Request 4, optional: conclusion.tex 54, limits.tex 168 and
    appendix-lbproduct.tex 161 still write the formula with `kappa`. These
    are correct as evaluations.
- **New, optional (tu):** `appendix-tu.tex` 376-405 mirrors the proof of
  Cor `cor:uniformgrid` with `rho`, `rho_j`. For parallel notation it could
  use `R_j` as in Appendix A. It is correct as it stands.
