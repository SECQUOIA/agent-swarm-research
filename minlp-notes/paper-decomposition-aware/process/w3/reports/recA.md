# W3 report: recA (Section 7 intro, 7.1, 7.2, 7.3, Appendix C)

Files edited: `sections/recourse.tex` (text only; input list unchanged),
`sections/recourse-valuefn.tex`, `sections/recourse-local.tex`,
`sections/recourse-convex.tex`, new `sections/appendix-recourse-convex.tex`
(Appendix C, label `app:recourse-convex`, title "Value functions, local
corrections and convex recourse: deferred proofs").

## Summary of structural changes

* Section 7 intro: corrected first sentence (condition numbers are built from
  the coordinate curvatures L_i), defines recourse, fixes the Section-7
  notation (retained set \mathcal K, recourse set \mathcal R, v = x_K,
  y = x_R, value function V) and adds a roadmap of 7.1-7.5 that names the main
  results (7.1, 7.3, 7.4) and the side results (7.2, concave-convex
  residuals); 7.5 is described as not using recourse.
* 7.1: V defined on the continuous hull; Lemma lem:valuefunction (a) restated
  precisely (also covers non-box X_R, needed by 7.3), (b) with V(v*) = OPT
  proved; Cannarsa-Sinestrari attribution at the point of use; the "Part (a)
  ..." paragraph moved directly after the proof and now says
  "Lemma~\ref{lem:valuefunction}(a)/(b)"; lem:cr-semiconcave deleted; private
  blocks in the convention scheme (y^{(t)}, t = 1..r, E_t, phi_t, psi_t).
  Thm thm:valuefn rewritten (R2 M3): L_i^V of polynomial encoding length,
  oracle returns psi_t(w) AND a minimizer, (b) growth of V suffices, bound
  f(p,kappa_V) kappa_V^C (I+q+1)^C with C depending only on the oracle's
  exponents, (c) exact output for a rational quadratic F with EX on V and
  REC/acceptance on F; |A|+r+n summands; log(1/L^V) <= poly(I). Proof of
  (b),(c) in App C.1.
* 7.2: starts with the bag-cell block (W_B -> V_B, e_B(C) = sum_{i in B}
  (L_i/8) w([a_i,b_i])^2 with the effective width w of Section 4).
  Lemma lem:cr-cell is now proved in three lines from Prop prop:cellwise(a)
  applied to V_B (whose proof uses only Def curvature) - this removes the
  duplicated Jensen argument (F10, F68). Thm thm:cr-filter: oracle bound
  ell(v) -> \underline V(v), oracle error eta -> \varepsilon_{or} (eta is
  reserved for the mesh scale, F89), proof moved to App C.2. The untitled
  remark became a short paragraph with the covering hypothesis (F127).
  Prop prop:cr-osc (statement+proof) and Example ex:cr-star32 moved to App C.2
  with a 1-paragraph summary in the main text; prop:star statement kept in
  the main text (compacted), proof in App C.2; V_h -> V^G; "centre" -> "center".
* 7.3 rewritten in the Section-7 scheme: retained \mathcal K, v; blocks
  y^{(t)} in Y_t = {y : G_t y <= b_t}, t = 1..r; scopes E_t; scope boxes
  Pi_t (replaces "attachment box"); block objectives
  phi_t(w,y) = 1/2 y^T C_t y + y^T Gamma_t w + c_t^T y (coupling K_t ->
  Gamma_t, because K is reserved for grid-size bounds); value factors psi_t;
  F_0 with Hessian H_0. Def def:leaf now requires a rational binary space
  partition (R2 M1); checking paragraph rewritten without the conditional.
  Lemma lem:leaf keeps (a),(b) with proofs; part (c) (energy formula,
  eq:cv-energy) moved to App C.3 with a one-sentence pointer. Prop
  prop:vf-curv kept (proofs of (a),(c) in main; proof of (b) sketched in main,
  full in App C.3). Thm thm:cv: eq:cv-L now defines L_i (signed),
  L_i^+ = max{L_i,0}, L^+ = max_i L_i^+; (i) signed, (ii) L^+ = 0, (iii) uses
  L_i^+ and growth of V for the approximation and growth of F for exact
  output, (iv) signed. Exact-output part of (iii) proved in App C.3 via
  Lemma lem:cv-height (now without uniqueness) and Prop prop:accept with the
  denominator bound Omega_0 = 2 Delta_P Lambda_0^2. Remark rem:cv-instances
  now contrasts value factors with Khajavirad's elimination (F43, F151).
  Deleted: Lemmas lem:cv-energy, lem:cv-envelope, paragraph "The
  negative-curvature target", the speculative paragraph (old 734-746),
  replaced by one sentence (see F9 for the corrected wording).
* Appendix C: C.1 proof of thm:valuefn(b),(c); C.2 proofs of thm:cr-filter
  and prop:star, prop:cr-osc, ex:cr-star32; C.3 energy formula, proof of
  prop:vf-curv(b), prop:cert-exist, lem:cv-bits, lem:cv-height (new proof
  without uniqueness), proof of the exact part of thm:cv(iii); C.4 proof of
  thm:cv-recog and its two examples; C.5 lem:cv-growth, cor:cv-affine,
  cor:cv-nu; C.6 ex:cv-fm, prop:cv-ladder, rem:cv-unstable; C.7 proof of
  prop:cv-limit.

Length (build/recA, last compile): Section 7 intro + 7.1-7.3 = about 8.3
pages (pp. 31-39); before: about 15 pages. See "Unresolved".

## (1) Adjudication

Status refers to the parts in recA files. "Other owner" means the finding has
no part in recA files.

| Id | Status | Reason | Change |
|---|---|---|---|
| F7 | other owner (recB, optsets) | recourse-balanced 163-164, optsets FG | none in recA files |
| F9 | MODIFIED | Valid. Rewrite 19's sentence ("pieces that contain no near-optimal point") is false for K = {x} in prop:cv-limit (the stiff piece [0,x_c] contains the minimizer) | Deleted 734-798, cv-energy, cv-envelope; one accurate sentence: the upper bounds on g_K come from points with objective gap >= 1/8 and the curvature 2M-1/4 from the stiff part, so a p, nu/g bound would need curvature and growth measured only near-optimally (pointer to Sec. 12 question 1). Moved prop:cert-exist, lem:cv-bits, lem:cv-height, proof of thm:cv-recog, cor:cv-affine, cor:cv-nu, prop:cv-ladder, rem:cv-unstable to App C. Roadmap added. 7.4/7.5 parts: recB |
| F10 | MODIFIED (recA part) | Valid | lem:cr-semiconcave deleted; lem:cr-cell now derived from prop:cellwise(a) (one rounding argument instead of two); thm:cv(iii) acceptance cites prop:accept. lem:cv-height kept as the general polytope height lemma (App C); unifying it with cor:height is the exact agent's choice (see requests) |
| F11 | MODIFIED (recA part) | Valid | In-section comparisons kept only where technical (rem:cv-instances: Bemporad critical regions, Khajavirad elimination). Request to front to remove the duplicate Khajavirad-elimination description from related.tex (see (3)) |
| F12 | ACCEPTED (recA part) | Valid | K/R scheme, ell_i, no P = Delta H in recA files; leaf polytopes Pi', leaf count N_Pi |
| F13 | ACCEPTED (recA part) | Valid | "CT (Algorithm~\ref{alg:ct})", "nodes per coordinate", "two endpoint nodes"; no "corrected-grid algorithm" left |
| F15 | ACCEPTED | Valid | As Rewrite 17: cr-semiconcave deleted, paragraph moved, bag cells moved to 7.2, e_B with L_i and ell_i |
| F20 | other owner (recB) | recourse-balanced | none |
| F24 | ACCEPTED (recA part) | Valid | "This subsection"; roadmap in recourse.tex. Duplicate headings in recourse-cuts: recB |
| F25 | MODIFIED (recA part) | The untitled remark in recourse-local is now a two-sentence paragraph (no remark needed) | Others: recB/optsets |
| F26 | ACCEPTED (recA part) | Valid | centre -> center (6x, now in 7.2 and App C.2). grids/related/computation: other owners |
| F29 | other owner | limits, optsets, appendix-smoothed (deleted), boundary | none |
| F30 | ACCEPTED (recA part) | Valid | "attachment box" -> scope box Pi_t (defined in def:cv-model); "calibrated table entry" -> "bag-table entry". Others: recB, tu, limits |
| F34 | ACCEPTED (recA part) | Valid | No overfull boxes from recA files in the final build |
| F35 | MODIFIED (recA part) | Paper stays one paper (CONVENTIONS) | cv-energy/cv-envelope deleted; cor:cv-nu moved to App C rather than deleted (CONVENTIONS; it is cited by the conclusion's open question); 7.3 proofs moved |
| F41 | ACCEPTED (recA part) | Valid | K retained / R recourse throughout 7.1-7.3; polytope RHS gamma_t -> b_t; ell_i |
| F42 | other owner | balanced, optsets, appendix-localized, exact | none |
| F43 | ACCEPTED (recA part) | Valid | rem:cv-instances contrasts value factors with Khajavirad's elimination (checked against DPK's account of [22], Thm 5 and its proof). optsets/intro: other owners |
| F45 | ACCEPTED | Valid | lem:cr-semiconcave deleted; paragraph right after lem:valuefunction, with "Lemma~\ref{lem:valuefunction}(a)/(b)" |
| F46 | ACCEPTED | Valid | L_i^+ = max{L_i,0} in eq:cv-L and (iii); signed L_i in (i),(ii),(iv); (iii) approximation assumes growth of V, exact output growth of F |
| F49 | other owner | computation, proximal, boundary, optsets, conclusion, smoothed | none |
| F56 | ACCEPTED | Same as F46 | (iii): "V has upper coordinate curvatures L_i^+; coordinates with L_i <= 0 get the two endpoint nodes" |
| F58 | ACCEPTED (recA part) | Valid | certificate polytopes P, P_r -> Pi', leaves Pi_1..Pi_{N_Pi}; height-lemma polytope -> calligraphic P (App C). Other parts: core/exact/tu/optsets |
| F59 | ACCEPTED (recA part) | Valid | attachment scopes S_t -> E_t |
| F60 | MODIFIED | Scheme of CONVENTIONS used (phi_t block objective, psi_t value factor) instead of the reviewer's f_t/phi_t | 7.1 and 7.3 use one scheme; W_B -> V_B, V_h -> V^G |
| F63 | ACCEPTED (recA part) | Valid | oracle bound ell(v) -> \underline V(v). d_i, m_i, Delta, B_i, ell(x): other owners |
| F65 | other owner | no hand-numbered algorithms in recA files | none |
| F67 | MODIFIED (recA part) | thm:cv(iii) now accepts by prop:accept with the lemma's Omega_0. REC is not used because the slice feasible set is a polytope (box x Y_t), not a box; coordinatewise rational reconstruction is kept | App C.3 proof of exact part |
| F68 | ACCEPTED (recA part) | Valid | Lemma 7.2 (= cr-semiconcave) deleted; Lemma 7.3 (cr-cell) derived from prop:cellwise(a). Others: optsets, tu, core |
| F69 | ACCEPTED | Valid | as F15 |
| F70 | ACCEPTED (recA part) | Valid | kappa_V = max{1, L^V/g} (= kappa(L^V,g)); thm:cv uses kappa = max{1, L^+/g} |
| F71 | other owner (recB) | recourse-mixed | roadmap mentions the concave-convex extension as a side result |
| F72 | ACCEPTED (recA part) | Valid | l_i -> ell_i in recA files |
| F79 | other owner (recB) | | none |
| F81 | other owner (recB) | | none |
| F84 | ACCEPTED (recA part) | Valid | Theorem bounds written with the f of thm:approx: f(p,kappa) kappa^C (I+q+1)^C and f(p,kappa) kappa^{C_1}(I+1)^{C_1}; no new f-functions; the height lemma's objective renamed F_P |
| F87 | ACCEPTED | Valid | prop:cv-ladder: "growth holds with constant 1/12, and no growth constant exceeds 33/16" |
| F88 | ACCEPTED (recA part) | Valid | recourse.tex first sentence corrected; limits.tex: other owner |
| F89 | ACCEPTED (recA part) | Valid | oracle error eta -> \varepsilon_{or} in thm:cr-filter, prop:cr-osc; ladder path weight eta -> literal 1/16 |
| F91 | other owner (recB) | recourse-cuts 235 | none |
| F92 | ACCEPTED | Valid | "Hadamard's inequality for rows, |det S| <= prod ||S_i||" |
| F93 | other owner | appendix-smoothed is deleted | none |
| F94 | ACCEPTED (recA part) | Valid | e_B and lem:cr-cell use per-coordinate L_i |
| F110 | ACCEPTED | Valid (coNP-hardness of covering) | def:leaf requires a rational BSP with certificates on leaves; checking paragraph states BSP coverage by induction and LP checks of nonempty interiors; prop:cert-exist and lem:cv-bits consistent |
| F111 | ACCEPTED | Valid | lem:cv-height proved without uniqueness (maximal active set, reduced Hessian nonsingular, saddle matrix); exact-output validity now proved; exact arithmetic check (see (5)) |
| F112 | MODIFIED | The proposed statement keeps f(p,kappa) unchanged; that is not justified because grid nodes have encoding length O((1+mu 2^mu)(I+q+1)) and the oracle cost is polynomial in it, which adds a factor kappa^{O(1)} | thm:valuefn(b): f(p,kappa_V) kappa_V^C (I+q+1)^C; (c) f(p,kappa_V) kappa_V^{C_1}(I+1)^{C_1}; |A|+r+n; L_i^V of polynomial encoding length; oracle returns a minimizer; full accounting in App C.1 |
| F113 | MODIFIED | CONVENTIONS scheme used instead of the reviewer's | recA renames: leaf count R -> N_Pi; constraint index k -> s; multiplier support calK -> calE; tangent space calT -> calW; D_0 -> Delta_H; beta (height lemma) -> beta_H; beta (bits) -> b'; beta (bracket) -> hat nu; beta (prop:star) -> omega_A; beta (prop:cv-limit) -> xi_2; pattern sigma -> J; final leaf L -> Pi'; central gradient g_0 -> zeta_0; K_l, K_u, J -> I_ell, I_u, I_0; coupling K_t -> Gamma_t; metric M -> calJ^T calJ; selection matrix E_t removed. bar h, Phi(S), r_i, N_gamma, core: recB |
| F115 | ACCEPTED | Valid | as F46 |
| F116 | ACCEPTED | Valid | as F15; V defined on bar X_K in eq:valuefn |
| F117 | MODIFIED | Per-coordinate e_B(C) = sum (L_i/8) w^2 (R6 Rewrite 17, CONVENTIONS) is sharper than L_B; the lemma needs L_i only for i in B, so the core search's core-only L is covered (take L_i = L) | 7.2 bag-cell block |
| F118 | ACCEPTED | Valid | as F92 |
| F119 | other owner (recB) | | none |
| F120 | other owner (recB) | | none |
| F121 | ACCEPTED | Valid | title "An instance with h = 1/2" (example now in App C.2); last sentence about families (A) and (B) in the main text |
| F122 | ACCEPTED | Valid | "it suffices to control the oscillation" wording; no necessity claim |
| F123 | other owner (recB) | | none |
| F124 | ACCEPTED | Valid | cor:cv-nu: tested up to a factor two; L^+ <= C_0 hat nu/2 implies L^+ <= C_0 nu |
| F125 | ACCEPTED | Valid | "Since every certified L_i is valid (Theorem cv(i)), L^+ >= L_K, and every growth constant ... satisfies g <= g_K" |
| F126 | ACCEPTED | Valid | "The certified curvature is a maximum over pieces, however small the piece." |
| F127 | ACCEPTED | Valid | eta (now eps_or) >= 0 introduced; covering hypothesis in the multilevel paragraph |
| F128 | ACCEPTED | Valid | "With a common curvature bound L, every node ..." |
| F129 | other owner (recB / deleted appendix) | | none |
| F130 | other owner (recB) | | none |
| F131 | other owner (recB / coordinator) | | none |
| F132 | ACCEPTED | Valid | "Clearly" deleted; numerators bounded in absolute value; exponent renamed b' |
| F150 | other owner (recB) | | none |
| F151 | ACCEPTED | Valid | Cannarsa-Sinestrari at lem:valuefunction; Khajavirad contrast in rem:cv-instances |
| F203 | other owner (computation) | computation.tex / solver | none |

## (2) Labels deleted or renamed

* `lem:cr-semiconcave` deleted (it was the unused restatement "Lemma 7.2").
  Any reference should become `Lemma~\ref{lem:valuefunction}(a)`. No
  remaining references in sections/ (checked by grep; appendix-smoothed.tex,
  to be deleted, cited lem:valuefunction(a) only).
* `lem:cv-energy`, `lem:cv-envelope` deleted with the paragraph "The
  negative-curvature target"; no references elsewhere. If the conclusion
  wants to mention the proximal-envelope idea, it should describe it in words
  (no label).
* Kept but moved to Appendix C (labels unchanged): `prop:cr-osc`,
  `ex:cr-star32`, `eq:cv-energy`, `prop:cert-exist`, `lem:cv-bits`,
  `lem:cv-height`, `eq:recog-system`, `lem:cv-growth`, `cor:cv-affine`,
  `cor:cv-nu`, `ex:cv-fm`, `prop:cv-ladder`, `rem:cv-unstable`.
* All other labels in recA files kept: sec:recourse, sec:valuefn,
  eq:valuefn, lem:valuefunction, eq:privateblocks, thm:valuefn, sec:local,
  lem:cr-cell, thm:cr-filter, eq:cr-oracle, prop:star, sec:convexrecourse,
  def:cv-model, eq:cv-model, eq:cv-value, def:leaf, eq:leaf-feas,
  eq:leaf-stat, eq:leaf-comp, lem:leaf, eq:kkt-identity, prop:vf-curv,
  thm:cv, eq:cv-L, rem:cv-instances, thm:cv-recog, prop:cv-limit.
* New label: `app:recourse-convex` (Appendix C).
* Statement changes others may cite: eq:cv-L now defines L_i, L_i^+, L^+;
  thm:cv(iii) is phrased with L^+; thm:cr-filter uses \underline V and
  \varepsilon_{or} (was ell, eta).

## (3) Requests for other files

1. recB, `recourse-cuts.tex` (core search, proof of thm:cr-search):
   * "(b)--(c) This is Theorem~\ref{thm:cr-filter} with $\ell=V$ and
     $\eta=0$" -> "(b)--(c) This is Theorem~\ref{thm:cr-filter} with
     $\underline V=V$ and $\varepsilon_{\mathrm{or}}=0$".
   * e_B(C) is now $\sum_{i\in B}\frac{L_i}8w([a_i,b_i])^2$. With
     $L_i:=L$ for every core coordinate (valid because L is an upper
     coordinate curvature in each core coordinate), "every cell of
     $\mathcal Q_j$ has $e_{\mathcal C}(C)=e_j$" stays true; please write
     "$e_{\mathcal K}(C)=e_j$ (with $L_i=L$ for $i\in\mathcal K$)".
   * `W_{\mathcal C}` -> `V` (CONVENTIONS; Lemma cr-cell now uses `V_B`).
   * The roadmap in recourse.tex refers to "the extension of the cut oracle
     to concave--convex residuals" without a \ref. If recB keeps a label for
     it, tell the coordinator; a `\ref` can then be added.
2. front, `related.tex` lines 14-17: the description of Khajavirad's
   elimination now lives in Remark~\ref{rem:cv-instances} (CONVENTIONS:
   each comparison in one place). Suggested text: "Their tractable classes
   of unbounded treewidth, and those of Khajavirad
   \cite{Khajavirad2026PolyBox}, take variables with nonpositive diagonal to
   be binary and eliminate the other components; Remark~\ref{rem:cv-instances}
   compares this with our value factors."
3. front, `conclusion.tex` question (1) (Rewrite 21 / R2 M5): "Theorem~\ref{thm:cv}
   and Corollary~\ref{cor:cv-nu} answer this when certified responses reduce
   every coordinate curvature to $O(\nu)$, Proposition~\ref{prop:cv-limit}
   shows ...". Corollary cor:cv-nu is now in Appendix C and phrased with
   $L^+$.
4. exact: prop:accept will be cited as "Proposition~\ref{prop:accept} with the
   denominator bound $\Omega_0$ for $\OPT$" for a feasible point of the
   convex-recourse model (box times polytopes). Please state it for any
   feasible point of a problem whose optimal value has denominator at most
   $\Omega'$ (the one-line proof is generic). My proof also repeats the
   one-line reason, so it stays correct either way. Lemma lem:cv-height
   (App C) is a height lemma for quadratics over integral polytopes without
   uniqueness; it can serve as the general lemma requested by F10/F67 if the
   exact agent wants one.
5. coordinator: Appendix C now also contains the proof of thm:valuefn(b),(c)
   (Section 7.1); title "Value functions, local corrections and convex
   recourse: deferred proofs". appendix.tex already inputs
   appendix-recourse-convex; recourse.tex input list unchanged.
6. limits and intro: references to prop:star, thm:cr-filter,
   lem:valuefunction, thm:cv, prop:cv-limit remain valid; intro.tex line ~92
   "bag-local corrections are valid only with such exact or certified
   recourse" is still accurate.

## (4) New BibTeX entries

None. Existing keys used: CannarsaSinestrari2004 (new citation site),
Khajavirad2026PolyBox (new citation site), BemporadEtAl2002,
KozlovTarasovKhachiyan1980, Mangasarian1988, GrotschelLovaszSchrijver1988.
The Khajavirad statement was checked against Del Pia-Khajavirad's account of
arXiv:2604.25033 (literature/papers/pia2026-treewidth-and-the-complexity-of,
Introduction and Theorem 5 with its proof): positive-diagonal components are
eliminated into value functions of their neighbours, which have nonpositive
diagonal, can be taken binary and are enumerated.

## (5) Checks run

* `python3 -B process/w3/checks/recA-cv-height.py` -> "checked 3944
  instances, 1061 with several minimizers: PASS". Exact (Fraction) face
  enumeration of random 2-D integer QPs over integral polygons, including
  singular and indefinite Hessians; for a minimizer with a maximal active
  set it verifies that the saddle matrix is nonsingular, x* = z/|det S| with
  |det S| <= Lambda_0, and that OPT has denominator <= 2 D Lambda_0^2 and
  dividing 2 D |det S|^2 (Lemma lem:cv-height without uniqueness).
* Hand re-derivation of all changed statements: lem:valuefunction(b)
  (V(v*) = OPT), lem:cr-cell from prop:cellwise(a), thm:valuefn(b)
  (weighted growth g/L^V; node encoding length O((1+mu 2^mu)(I+q+1)),
  2^mu <= 6 sqrt(kappa_V)), thm:cv(i)-(iv) with L_i^+, exact-output threshold
  eps <= min{1/(2 Omega_0^2), g/(32 Lambda_0^4)}, cor:cv-affine with
  calJ^T calJ, cor:cv-nu bracket, prop:cv-ladder after renaming (identity
  z^2 + phi_M - 1/20 = t^2 + M rho_1^2 + rho_2^2 + alpha_1/5 re-expanded),
  ex:cr-star32 numbers (23/32, 27/32, 31/16, 1/8, 33/16).
* `latexmk -pdf -interaction=nonstopmode -outdir=build/recA main.tex`: exit
  12 because latexmk's bibtex step read an aux without \bibdata (shared
  working directory; not from recA files). Then
  `TEXINPUTS=.: pdflatex -interaction=nonstopmode -output-directory=build/recA main.tex`
  (twice): 0 LaTeX errors, 0 undefined references, 0 undefined citations,
  no overfull boxes from recA files (the remaining small overfull boxes are
  in optsets.tex and appendix-moments.tex).
* No project-wide verification run (CI handles it).

## (6) Unresolved

* Page budget: Section 7 intro + 7.1-7.3 is about 8.3 pages in the current
  build (target about 7). Reaching 7 would require moving the proofs of
  lem:leaf and prop:vf-curv(a),(c) (about 0.8 page) to Appendix C, which the
  task asked to keep in the main text. The coordinator can decide.
* The roadmap's mention of concave-convex residuals has no \ref until recB
  fixes the label/placement (request 1).
* recB must update the cr-filter citation (eta -> eps_or, ell -> \underline V)
  in the proof of thm:cr-search.

## Verification (recA-verify)

Scope: `sections/recourse.tex`, `recourse-valuefn.tex`, `recourse-local.tex`,
`recourse-convex.tex`, `appendix-recourse-convex.tex`, diffed against
`process/w3/sections-before-w3/`. All 68 findings in
`process/w3/assign/recourse.json` were checked against the parts in these
files.

### What was checked

* Adjudications. Every ACCEPTED fix in the table above is present in the
  files and correct. The MODIFIED decisions (F9, F10, F11, F25, F35, F60,
  F67, F112, F113, F117) are justified: Rewrite 19's sentence is false for
  K = {x}; REC needs a box, so the polytope slices of 7.3 use coordinatewise
  reconstruction and Proposition prop:accept; the per-coordinate e_B of
  F117 is sharper than L_B and covers the core search by taking L_i = L;
  the factor kappa_V^C of F112 is needed because the oracle's polynomial is
  applied to grid nodes of length O(mu 2^mu (I+q)). "Other owner" findings
  have no part in these files.
* Mathematics, line by line: Lemma lem:valuefunction (a), (b); Lemma
  lem:cr-cell from Proposition prop:cellwise(a) (subbox spanned by C, grid of
  corners, effective width, integer coordinates); Theorem thm:cr-filter (a)-(c)
  and the multilevel paragraph; Proposition prop:cr-osc; Proposition prop:star
  (A), (B) and Example ex:cr-star32; Definition def:leaf and the checking
  paragraph (BSP coverage, LP checks, Farkas multipliers); Lemma lem:leaf;
  eq:cv-energy; Proposition prop:vf-curv (a)-(c); Proposition prop:cert-exist
  (pattern polyhedra, triangulation, BSP termination and leaf containment);
  Theorem thm:cv (i)-(iv); Lemma lem:cv-bits; Lemma lem:cv-height without
  uniqueness (maximal active set, line argument, saddle matrix, row Hadamard,
  Cramer); the exact-output proof of thm:cv(iii) (slice constants, windows
  1/(4 Lambda_0^2), threshold min{1/(2 Omega_0^2), g/(32 Lambda_0^4)},
  acceptance by prop:accept, which exact now states for any feasible set and
  any Omega'); Theorem thm:cv-recog; Lemma lem:cv-growth; Corollaries
  cor:cv-affine and cor:cv-nu; Example ex:cv-fm; Proposition prop:cv-ladder in
  the renamed variables; Remark rem:cv-unstable; Proposition prop:cv-limit;
  the limits paragraph (F125); Remark rem:cv-instances against Del Pia and
  Khajavirad's account of arXiv:2604.25033 (Theorem 5 and the comparison of
  the proofs of their Theorems 4 and 5).
* Moved material: every moved label is defined once and keeps its proof;
  nothing proved was lost except the deleted items listed in CONVENTIONS
  (lem:cr-semiconcave, lem:cv-energy, lem:cv-envelope, the speculative
  paragraph). The old lem:cv-growth claims "z* is the unique minimizer of V"
  and the metric I + sum E^T B^T B E were dropped; neither is used, and the
  metric is in cor:cv-affine.
* Conventions and writing: K/R scheme, y^{(t)}, E_t, phi_t, psi_t, V_B, V^G,
  \underline V, epsilon_or, ell_i, L_i^+, algorithm names, "nodes per
  coordinate", "bag-table entry", American spelling, no filler, no artifacts.

### What was fixed

1. Theorem thm:valuefn. (i) The hypotheses now require that the factors of
   F_0 be evaluated exactly in polynomial time; Theorem thm:approx covers
   only explicit quadratic factors, and Example ex:polylimits(c) shows that exact
   evaluation can fail for binary-encoded exponents. (ii) "C depends only on
   the exponents of the running time of the oracle" was incomplete: the stage
   count J and the node lengths depend on the encoding length of the L_i^V,
   and constant factors are absorbed into the exponent; C and C_1 now
   "depend only on the polynomials in the hypotheses". (iii) Part (c) is
   restricted to a rational quadratic on the mixed box X of eq:model, because
   REC, Corollary cor:height and Theorem thm:transfer are box statements.
   (iv) "quadratic growth" -> "point growth" (CONVENTIONS terminology);
   kappa_V = kappa(L^V, g); REC (Algorithm~\ref{alg:rec}) at first use.
2. Appendix C.1. Proof of (b) rewritten with explicit polynomials P_L (for
   the L_i^V) and P (oracle and F_0 factors): J = O(P_L(I)+q), node length
   c(1+mu 2^mu)(P_L(I)+q+1), per-operation cost (c'' kappa_V (I+q+1))^{C'},
   absorption of constants using I+q+1 >= 2. Proof of (c): the growth
   assumption for the bound is stated, and the case L^V = 0 says why the test
   passes.
3. Lemma lem:valuefunction(b), Theorem thm:cv(iii), Appendix C.3 and
   Corollary cor:cv-affine: "quadratic growth" -> "point growth".
4. Theorem thm:cv(iii) and its proof, Corollary cor:cv-nu and the summary
   after Remark rem:cv-instances: kappa -> kappa_V = kappa(L^+, g). kappa is
   reserved for kappa(L, g) of F; this matches thm:valuefn, the intro table
   and the conclusion.
5. Definition def:leaf: leaves Pi_1, ..., Pi_{N_Pi} -> Pi'_1, ...,
   Pi'_{N_Pi} (Pi_1 clashed with the scope box Pi_t of block 1).
6. "slope B_{Pi'}" -> "linear part B_{Pi'} of the response"; Example
   ex:cv-fm "changes slope" -> "is not affine" (CONVENTIONS: no "slope").
7. End of 7.3: "A bound ... would need curvature and growth measured only
   where near-optimal points can lie" claimed a necessity that is not proved,
   and "the curvature 2M-1/4 from the stiff part of the domain" was vague.
   New text: every upper bound on g_K in the proof comes from a point with
   objective gap at least 1/8, so a bound along this route cannot use the
   global constants L_K, g_K; measuring curvature and growth only where
   near-optimal points can lie is one possibility.
8. Section 7.1 discussion and closing paragraph: Section 7.4 bounds the
   curvature of V by that of F on the core, and Section 7.2 gives no class of
   oracles, so "Sections 7.3 and 7.4 ... bound its curvature by quantities
   that do not see stiff convex terms" and "The next subsections give classes
   where ... L^V is certified" were inaccurate; both now say what 7.3 and 7.4
   provide.
9. recourse.tex: "recourse" is now defined in one sentence; the roadmap cites
   Remark~\ref{rem:cr-mixed} (recB's label) for the concave-convex extension.
10. Proposition prop:star preamble: "grid value function of the center x" ->
    "of the coordinate x" (the star is introduced later, and "center" also
    names CT's grid centers).
11. Appendix C, proof of prop:vf-curv(b): the reason a subinterval lies in
    one leaf interval (no endpoint strictly inside) is stated.

### Checks run

* `python3 -B process/w3/checks/recA-verify-identities.py` (new; exact
  Fraction/SymPy): lem:cr-cell on 400 random nonconvex mixed QPs with an
  integer bag coordinate and exact V_B, 0 violations; ladder identity and the
  bounds on alpha_1^2, alpha_2^2, 41/4 / (1/12) = 123, 33/16: True;
  ex:cv-fm data (C, Gamma, c, retained part), the three responses, values,
  B^T C B and piece second derivatives: True; eq:cv-energy on 60 random
  one-leaf instances: 0 violations; ex:cr-star32 numbers and the corner
  minimum of prop:star(A) for j = 1, 2, 3: True; prop:cv-limit SOS identity,
  y_c, x_c, V on [0, x_c], F_M(2,2) = 3/2: True.
* `python3 -B process/w3/checks/recA-cv-height.py`: "checked 3944 instances,
  1061 with several minimizers: PASS".
* `TEXINPUTS=.: pdflatex -interaction=nonstopmode
  -output-directory=build/recA-verify main.tex` (twice) and `latexmk -pdf
  -interaction=nonstopmode -outdir=build/recA-verify main.tex` (exit 0):
  0 errors, 0 warnings, 0 undefined references, 0 overfull boxes; 123 pages.
  (A first latexmk run failed on a stale `main.out` in the fresh output
  directory, not on these files.) No project-wide verification was run.

### What remains

* recB, `recourse-cuts.tex` proof of thm:cr-search (b), (c): still
  "$\underline V=V$ and $\eta=0$"; should be "$\underline V=V$ and
  $\varepsilon_{\mathrm{or}}=0$".
* Page budget: Section 7 runs pp. 31-45 (about 14 pages; target about 12),
  of which the recA part is pp. 31-39. Moving the proofs of lem:leaf and
  prop:vf-curv(a), (c) to Appendix C would save under a page; coordinator
  decision.
* Notation kept deliberately: G_t for the private constraint matrix (G is
  reserved for grids; R5 proposed A_t, but A already denotes the matrix of
  the w-polytopes in 7.3 and of the polytope in lem:cv-height, so A_t would
  create a new clash; CONVENTIONS lists no rename) and sigma_j for the
  certified cancellation (sigma(t) is the step function of Section 5;
  CONVENTIONS lists no rename). The coordinator can rename globally if
  wanted.
* front, `related.tex` 19-22 (not a recA file): "Their tractable classes ...
  eliminate the continuous components into value functions of their binary
  neighbors" fits Khajavirad's Theorem 5 but not Del Pia and Khajavirad's
  Theorem 4, which eliminates binary components first (DPK, discussion after
  Theorem 5). Remark rem:cv-instances describes Khajavirad's elimination
  correctly; the duplicate in related.tex can be shortened as requested.
