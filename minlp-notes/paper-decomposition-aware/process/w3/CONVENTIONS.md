# W3 revision conventions (binding for every revision agent)

The paper stays one paper (the user asked for one large paper). It follows
Option B of `process/w2/R6-writing.md` section 4: a focused main text, with
secondary results and long proofs moved to appendices ordered by section.
A proved result is removed only where this file says so.

## 1. Section structure after revision

Main text (file owners in brackets):

1. Introduction [front]. No table of contents. Sections 1.1 and 1.2 merged
   into one results section: Theorem 1.1 (headline: certificate + accuracy-
   independent approximation + exact output, combining Thm thm:certificate,
   Thm thm:approx, Thm thm:exact), Theorem 1.2 (lower bounds, with their
   complexity assumptions), a paragraph on the scope of the growth hypothesis
   (Rewrite 5 of R6), one paragraph per extension with precise novelty
   statements, a results table (setting, parameter, bound, certificate),
   organization paragraph.
2. Related work [front]. Each comparison with prior work lives in ONE place
   (here, or a technical remark in the section that needs it).
3. Problem class, decompositions and conditioning [core]. Definition of growth
   covers point growth (g, kappa), weighted growth (gamma, kappa-bar) and set
   growth (g_S, kappa_S). Lemma growthcert. A short notation table closes the
   section.
4. Corrected coordinate grids [core].
5. Accuracy-independent grids under quadratic growth [core]. Algorithms
   TRIAL and CT as numbered algorithm environments. A stated and proved
   common-mesh lemma (one set of constants, used by Section 6 and appendices).
6. Exact output [exact]. Order: 6.1 scaled data; 6.2 stationary polytopes and
   height; 6.3 acceptance and recovery (+ Remark rem:np moved here from
   optsets); 6.4 exact output under growth; 6.5 localized acceptance
   (currently exact-localized.tex, moved BEFORE polynomials); 6.6 explicit
   polynomial factors. Prop prop:accept is stated in a form parameterized by
   a denominator bound Omega for OPT so that Sections 7 and 8 cite it instead
   of reproving it.
7. Conditional recourse [recourse], target about 12 pages, with a roadmap
   paragraph in recourse.tex. 7.1 value functions; 7.2 bag-local filter and
   local corrections; 7.3 certified convex recourse (core statements); 7.4
   separately concave residuals and minimum cuts; 7.5 corrected grids without
   a tree decomposition (balanced quadratics). Concave-convex residuals
   (current 7.5) become a short subsection or remark that is explicitly
   connected to Theorem thm:cr-oracle, with details in the appendix.
8. Coupling constraints [tu]. Exact output (current 8.6) is reduced to the TU
   constants plus a citation of the Section 6 arguments; details in an
   appendix. prop:tu-tight becomes a sentence citing the Section 5 lower bound
   (prop:sharp / its corollary). rem:tu-hybrid is deleted (one sentence in the
   conclusion's open problems is enough; the front agent writes it).
9. Several minimizers [optsets].
10. Structural limits [limits].
11. Implementation and computational illustration [computation].
12. Conclusions and open problems [front].

Appendices (one file each; created/owned as stated):

* A. Proofs for Section 5 — appendix-growth.tex [core]
* B. Exact output: proof of Cor cor:local (appendix-localized.tex) and exact
  implicit output for polynomial boundary optima (appendix-boundary.tex)
  [exact]
* C. Recourse: moved proofs and supplementary results — NEW
  appendix-recourse.tex [recourse]
* D. Coupling constraints: exact output and moved proofs — NEW
  appendix-tu.tex [tu]
* E. The proximal stage — appendix-proximal.tex [optsets]
* F. Lower-bound proofs — appendix-lbproduct.tex, appendix-moments.tex [limits]

DELETED: appendix-smoothed.tex (smoothed core count) and the text that points
to it; Lemma lem:cr-semiconcave; the unused restatement Lemma 7.2 in
recourse-valuefn (if it is never cited); Lemmas lem:cv-energy and
lem:cv-envelope with the paragraph "The negative-curvature target" and
recourse-convex.tex lines ~734-798 (replace by at most one sentence); Remark
rem:cluster; Remark rem:tu-hybrid; the table of contents.

The coordinator owns main.tex, macros.tex, appendix.tex, recourse.tex input
lists and references.bib, and will update input lists to match.

## 2. Algorithm names and environments

The coordinator adds to macros.tex:

    \theoremstyle{definition}
    \newtheorem{algorithm}[theorem]{Algorithm}

Use `\begin{algorithm}[CT: capped trials]\label{alg:ct} ... \end{algorithm}`.
Names (one name per algorithm, used everywhere, also in captions):

| Name | Meaning | Label |
|---|---|---|
| TRIAL | one trial with grading theta, cap K, accuracy eps (old "Algorithm 1") | alg:trial |
| CT | capped trials (old "Algorithm 2", "capped algorithm", "pruned-grid", "filtered-grid", "FG") | alg:ct |
| CT with a common mesh | variant with h_j = s 2^{-j} in all gridded coordinates and Euclidean kappa | (lemma lem:commonmesh) |
| REC | rational recovery/snapping | alg:rec |
| EX | exact output | alg:ex |
| UC | unions of uniform cells | alg:uc |
| CORE | core search (cut recourse) | alg:core |
| TU-GRID | grids under TU coupling | alg:tugrid |
| TU-EXACT | exact output under TU coupling | alg:tuexact |
| PROX | proximal stage (defined in the main text of Section 9, details in App E) | alg:prox |
| DISC | discovery with unknown growth (if it is a separate algorithm) | alg:disc |

Refer to them as "CT (Algorithm~\ref{alg:ct})" at first use in a section,
then "CT". Never write "Algorithm 1"/"Algorithm 2" by hand.

## 3. Terminology

* "graded grid", "grading theta" (not geometric grid, slope).
* "nodes per coordinate" for |G_i|; "table entries" for bag-table sizes;
  never "labels"/"states"/"points" for |G_i| (computation may say "table
  entries" for DP states).
* "point growth", "weighted growth", "set growth" (all defined in Def 3.2).
* "corrected grid", "min-marginal", "filtering", "path certificate".
* Prop prop:cellwise may be called an observation in prose; credit the
  single-cell inequality to Bajaj and Hasan.

## 4. Notation (reserved meanings; rename conflicting uses)

Based on the table at the end of `process/w2/R5-consistency.md`.

| Symbol | Reserved meaning | Rename conflicting uses to |
|---|---|---|
| n | number of variables | items in reductions: m |
| I | input length | grid intervals: [a,a'] or J |
| I_C, I_Z | continuous / integer index sets | (App boundary C_c -> I_C) |
| \ell_i, u_i, s_i, s | box bounds, widths, max width | write \ell_i, never l_i; TU width W -> s; gradient \ell(x) -> \zeta(x) or \nabla F(x); oracle bound \ell(v) -> \underline V(v) |
| X, X', X^{(j)} | domain, subbox, stage box | subboxes B, B_i -> X', X'_i where B clashes with bags B_t |
| T, N, B_t, S_{tu} | tree, number of bags, bags, separators | blocks count -> r; free set T -> J |
| \mathcal A, f_a, S_a | factors, scopes | attachment scopes -> E_t; chain states S_t -> \xi_t |
| p | maximum bag size | |
| \mathcal S, \mathcal S_i | optimal set, its projection on coordinate i | S, S_i, \pi_i(S) -> \mathcal S, \mathcal S_i |
| L_i, L, P, n_P | coordinate curvatures, max, P={i:L_i>0}, |P| | P=\Delta H -> \hat H; polytopes P, P_r -> \Pi, \Pi_r; proximal objective P(y) -> Q_\eta(y); negative L_i -> use L_i^+ = max{L_i,0} |
| \bar L | directional curvature (Section 8) | |
| g, kappa | point growth, kappa = max{1, L/g} | set-growth g -> g_S |
| gamma, \bar kappa | weighted growth | Euclidean gamma in Lemma growthcert -> g_0; smallest inward derivative -> \lambda_A (B_\gamma -> B_\lambda); gaps gamma -> \delta |
| g_S, kappa_S | set growth | kappa_c -> kappa(\bar L, g_S) or keep kappa_c defined via this; kappa in Sec 9.3/10.4 with set growth -> kappa_S |
| kappa(L',g') | := max{1, L'/g'} (general convention) | kappa_V = kappa(L^V, g) |
| G_i, G | grids | |
| w_i(v), w(J) | largest adjacent width; effective width | \Delta_i(I) -> w(J) |
| d_i, D, Q, \beta, m_i | corrections, sum, corrected objective, bound, min-marginals | signed widths d_i -> \delta_i; m_i = |G_i|-1 -> k_i |
| K, K_S | grid-size bounds | retained set K -> \mathcal K; guess K in 9.3/App E -> \hat\kappa |
| U | incumbent value | |
| \Delta, R, \Omega, \tau | denominator and height constants of Section 6 | TU versions -> \Delta, R_{TU}, \Omega_{TU}, \tau_{TU}; leaf count R -> N_\Pi |
| \theta, \sigma(t) | grading, step | fractional parts -> \vartheta |
| h_{ij}, \eta_j | per-coordinate mesh, scale | common mesh h_j |
| \mathcal K, \mathcal R | retained and recourse (eliminated) index sets in ALL of Section 7 | retained \mathcal R (7.3), core \mathcal C, C (7.6) -> \mathcal K ("core" may stay as a word); recourse/residual -> \mathcal R (= \mathcal R_- \cup \mathcal R_+ in concave-convex part) |
| v = x_{\mathcal K}, y = x_{\mathcal R} | retained / recourse variables | |
| V, V_B, V^G | value function, bag version, grid value function | W_B, W_C, V_h -> V_B, V^G |
| y^{(t)}, t=1..r, E_t, \phi_t, \psi_t | private blocks, scopes, block objectives, value factors (as in recourse-valuefn eq:privateblocks) | 7.3's y_t, S_t, T, f_t -> this scheme |
| J_0, J_\partial | interior / active coordinates of a point | S, A in Lemma growthcert, Cor local, App localized -> J_0, J_\partial (keep \lambda_A notation by writing \lambda_\partial or define \lambda_A with A = J_\partial; choose one and use it in Sec 6 and App B) |

If a needed rename is not covered, choose a symbol that is unused in the
whole paper (`grep` all sections) and list it in your report.

## 5. Claim wording (use these exact substance; adapt grammar)

* Growth scope (intro, Section 3 after Lemma growthcert): "Growth restricts
  where nonconvexity can occur. For a continuous box QP, growth forces the
  Hessian block of the coordinates strictly inside their bounds to be
  positive definite (Lemma growthcert). The nonconvex instances covered by
  our bounds therefore have their negative curvature in directions that
  involve active bounds or integer coordinates; such instances can have
  exponentially many strict local minima (Example ex:family)."
* FPT: kappa-bar is a real parameter of the instance, not part of the input
  and never computed by CT. Say: "the running time is bounded by
  f(p, kappa-bar) poly(I+q) for every instance; in parameterized terms this
  is a fixed-parameter bound in the parameters p and ceil(kappa-bar), which
  the algorithm does not need to know" (see R9 R4 for exact phrasing).
* Lower bounds: "unless P=NP, neither parameter can be dropped and the
  dependence on kappa cannot be polylogarithmic; under ETH the dependence on
  p is exponential even for kappa <= 2; under randomized ETH the exponent of
  kappa cannot be o(p), already for integer box quadratics." Never write
  "must be polynomial" or "must grow linearly".
* TU coupling: "Totally unimodular coupling constraints with mesh-aligned
  data admit exactly feasible correlated rounding. Under set growth with
  finitely many optimal values per coordinate, the algorithm is polynomial
  for fixed width when the condition number kappa_c, the box widths measured
  in mesh units (s/eta), and r are polynomially bounded; it is not FPT, and
  the pseudopolynomial level-0 grid cannot be removed unless P=NP (Prop
  lim:prop:constraints)." Uniform meshes: "two natural non-uniform
  alternatives, misaligned coordinate grids and a common graded pattern,
  give invalid bounds with curvature-only corrections" — never "forced".
* Unions of uniform cells: "O(r sqrt(n kappa_S)) nodes per coordinate".
* Endpoint/face description: credit Rosenberg (1972) for multilinear optimal
  faces, Wainwright-Jaakkola-Willsky (2005) and Werner (2007) for
  zero-residual descriptions of all optimal labelings; Khajavirad /
  Del Pia-Khajavirad where R7 says.
* Subset Sum running-sum encoding: credit Bienstock and Munoz (2018, App. A)
  and Cifuentes-Parrilo (2016, Ex. 1); what is added is a unique minimizer
  and kappa = 1.

## 6. Rules for revision agents

* Edit ONLY the files you own (listed in your task). You may create the new
  files assigned to you. Do not touch main.tex, macros.tex, appendix.tex,
  recourse.tex, references.bib (coordinator).
* Keep existing \label names whenever the object survives (also when moved
  to an appendix). If you delete a labelled object, list the label in your
  report together with what references to it should become. Do not edit
  references in files you do not own; list them instead.
* New citations: use existing keys (grep references.bib). If a new key is
  needed, include a complete BibTeX entry in your report (verified against
  the primary source; DOI where available).
* Every finding assigned to you gets an adjudication line in your report:
  id, ACCEPTED / MODIFIED / REJECTED, one-line reason, and what was changed.
  Reject only with a concrete reason (e.g., the reviewer misread; give the
  line).
* Mathematics: when a fix changes a statement or proof, re-derive it fully;
  run small exact-arithmetic checks (Python fractions) where useful. Put
  check scripts in process/w3/checks/<agent>-*.py. At most 4 concurrent
  processes on this shared machine; keep checks short.
* Writing: plain, direct language; no filler; no "we note that", "it is
  worth noting", "crucially", "importantly", "delve"; no rhetorical
  questions; no bold claims beyond the theorems. Keep the existing voice
  ("we").
* After editing, compile once to catch your own LaTeX errors:
  `cd paper-decomposition-aware && latexmk -pdf -interaction=nonstopmode
  -halt-on-error -outdir=build/<agent> main.tex` (use your own outdir;
  undefined references to labels other agents own are expected and fine;
  fix only errors from your files).


## 7. Amendments after the W4 review (applied in W5)

* Growth scope (replaces the first bullet of section 5): minimality alone
  confines negative curvature at a minimizer of a box QP to directions that
  involve active bounds or integer coordinates (H_{J0J0} is positive
  semidefinite). Growth adds quantitative conditions: locally, point growth
  gives H_{J0J0} >= 2gI; globally, every feasible x' gives
  kappa >= L||x'-x*||^2/(F(x')-OPT), so distant near-optimal points force a
  large condition number (Remark rem:nonconvex; verified fix of C-writing-3).
* FPT: kappa-bar in "f(p, kappa-bar)" means the smallest weighted condition
  number of the instance (the infimum over valid gamma).
* Renames recorded in W5: stage limit of TRIAL and CT -> j_max (J remains
  the grid-interval symbol and the last level of CORE, TU-GRID and UC);
  curvature exponent -> varpi_i; proximal objective Q_omega(y) with
  omega = L theta^2/4 (not Q_eta); a minimizer in Section 6 -> x^circ
  (s and s_i are widths); free set of REC -> J_f.
* Title: kept as given in the user's request ("Decomposition-aware global
  optimization: certified coordinate grids, conditional recourse, and
  structural limits"); C-writing-15's retitling proposal was not adopted.
* Table 1 (tab:results): four columns; certificate/output information is in
  the caption.
