# coreB report (W3): Section 5 and Appendix A

Files edited: `sections/growth.tex`, `sections/growth-sharp.tex`,
`sections/appendix-growth.tex`. No other file was touched. Check script:
`process/w3/checks/coreB-commonmesh.py` (logs `coreB-commonmesh-seed7.log`,
`coreB-commonmesh-seed23.log`).

## Summary of changes

* Algorithms: `\begin{algorithm}[TRIAL: one trial]\label{alg:trial}` and
  `\begin{algorithm}[CT: capped trials]\label{alg:ct}`. TRIAL now keeps an
  explicit incumbent `\hat x`, states the initial value without the ambiguous
  "(at least F(ell))", and says when a trial fails. All "Algorithm 1/2",
  "filtered algorithm", "labels" and "slope" are gone from my files.
* New Lemma `lem:commonmesh` (CT with a common mesh), placed in Section 5.3
  after Remark `rem:fpt`. It has one set of constants, items (G1)–(G5), defines
  "CT with a common mesh", and is proved in full in Appendix A by redoing the
  proofs of Lemmas `lem:inv` and `lem:states` with `a_j = L n h_j^2` and
  `||.||_L^2 -> L||.||^2`. All target constants were proved:
  - (G1) `D(z) <= (L/4) n h_j^2 + (L theta^2/2)(||z-x*||^2+||c-x*||^2)`;
  - (G2) `||c-x*||^2 <= 4 kappa n h_j^2`, `||y_j-x*||^2 <= kappa n h_j^2`
    (the proof gives 8/15), and `||z-x*||^2 <= (17/15) kappa n h_j^2` for
    every grid point z with `Q(z) <= U`;
  - (G3) `U-OPT <= F(y_j)-OPT <= F(y_j)-beta_j = D(y_j) <= (9/16) L n h_j^2`
    (the proof gives 8/15);
  - (G4) the filtered interval lies within `4.2 sqrt(n kappa) h_j` of
    `(y_j)_i` for `i in I_C`, `L_i>0`, and within `1 + 4.2 sqrt(n kappa) h_j`
    for `i in I_Z`, `L_i>0`. The exact constant is
    `(2+sqrt(17/15))(1+1/sqrt 8) = 4.1481`;
  - (G5) cap `8 theta^{-1} ceil(log2(n+2))` nodes per coordinate. With
    `psi(m) = 3/4 + 8 ln(5/4 + 3 sqrt m)`, `psi(1) = 12.33 <= 16`.
  
  The lemma also states that every bound holds for any initial center in X.
  This covers the implementation's restart at the incumbent; see the
  computation request below. Termination on every instance and success by
  trial `mu = max{2, ceil(log_4(8 kappa))}` under point growth are proved
  as well.
* Lemma `lem:inv`: the free parameter is now `k >= max{1,1/gamma}` with
  `8 k theta^2 <= 1` (R1 m5). Theorem `thm:approx`(b) applies it with
  `k = kappa-bar` and the constant gamma that defines `kappa-bar`. Part (i)
  now has an explicit induction. Part (ii) at j=0 holds for any `c^(0) in X`.
* Lemma `lem:states`: the `phi(1)` ceiling statement is corrected. The proof
  now uses `[a,a']` and an endpoint v with `m_i(v) <= U`, since J is the
  stage limit. The hull statement is explicit, and the Iverson bracket is
  defined.
* Theorem `thm:approx`(a): states that `h_ij` is a power of two, so
  `floor(h_ij) = h_ij` for `h_ij >= 1`. The integer case `h_ij < 1` is
  attached to the right sentence. The count is now `1+2/theta`. (b): "all
  numbers" is replaced by grid nodes (`Gamma_X 2^alpha`) and table entries
  (`8 Gamma_F Gamma_X^2 4^alpha`).
* Appendix A bit lengths: "at most I+n terms" (R1 m9). Corrections are
  described as products of node differences, and `mu K_mu <= 10 mu 2^mu (I+1)`.
* Remark `rem:fpt` was rewritten with the CONVENTIONS wording. It states the
  fixed-parameter bound in p and `ceil(kappa-bar)`, which CT neither receives
  nor computes. It gives the lower bounds with their assumptions (P≠NP, ETH,
  randomized ETH), noting that they hold for kappa and hence for
  `kappa-bar <= kappa`. "Must grow linearly" is gone.
* Remark `rem:cluster` is deleted. After Lemma `lem:states` there is one
  pointer sentence to Section `sec:related`.
* `growth-sharp.tex`:
  - The unsupported `(2+sqrt2) sqrt(n kappa)+7` claim is replaced by the
    proven bound `12(2 sqrt(n kappa)+1)` of Theorem `thm:cells` for UC
    (Algorithm `alg:uc`) with a single minimizer.
  - Prop `prop:sharp` now uses the hypothesis `w_i(0) >= h` (R1 m11). Its
    coupling is parametrized as `Lambda - 2g`, since sigma is reserved for
    the step. `q_k` was renamed `Q_k`.
  - Cor `cor:uniformgrid` names TRIAL stages, the common mesh
    `h_j = s 2^{-j} = 2^{1-j}`, uniform grids as the construction of
    Definition `def:graded` with theta=0, and initial center 0 (R1 m12).
    `r` was renamed `nu` because it clashed with `r_i` and with r in
    `thm:cells`, and the graded part has `theta in (0,1/4]`.
  - Cor `cor:uniformgrid` remains the single statement of the
    `Theta(sqrt(n kappa))` lower bound for filtered uniform grids.
* Examples:
  - `ex:family`: the graph is renamed `\mathcal G` (it clashed with
    `Gamma_X`, `Gamma_F` in App. A), and the maximum degree is
    `Delta_{\mathcal G} >= 1`. The text now gives `kappa-bar <= kappa <= 21/4`
    and "at least a fixed amount".
  - `ex:chain` is shortened to a pointer to Prop `lim:prop:messages`.
    Following R9's optional request, it now reports the Euclidean kappa of
    the unit-box rescaling: L = 4^{m+1}, largest growth constant in
    [1/8, 20], so `kappa >= 4^m/5` for every valid constant and
    `kappa <= 32*4^m` for the largest. This is proved in Appendix A.
* After TRIAL there is one sentence on centering, per R9's optional request.
  The first center may be any point of X, since `lem:inv`(ii) holds at j=0.
  We take the vertex ell and then the corrected minimizers, which are grid
  nodes; this keeps denominators bounded, and `lem:inv`(iii) bounds their
  distance.
* Notation (CONVENTIONS section 4):
  - stage boxes `B^(j) -> X^(j)`;
  - subbox in Def. `def:graded`: `B_i -> X'_i`;
  - `H -> \hat h` in Lemma `lem:graded`(b), since H is the Hessian;
  - chain states `S_t -> xi_t` in App. A;
  - the rescaled states are `\varsigma_t`, a symbol unused elsewhere.

## (1) Adjudication

core.json is shared with coreA. "No coreB part" means the finding concerns
only files owned by others. Where a finding has parts in several groups, only
the parts in my files are adjudicated here.

| id | decision | reason | change made (coreB files) |
|---|---|---|---|
| F10 | MODIFIED | My part is only `prop:sharp`/`prop:tu-tight`. The height, snap and accept unification and `lem:cr-semiconcave` belong to exact/tu/recourse. | Cor `cor:uniformgrid` made self-contained (mesh, center, theta=0 stated) so that tu can replace `prop:tu-tight` by a pointer. |
| F11 | MODIFIED | Accepted the deletion of `rem:cluster`. Rewrite 12's replacement sentence repeats related.tex lines 103–106 (CONVENTIONS: one place per comparison), so a pure pointer is used instead. | `rem:cluster` deleted. "Section~\ref{sec:related} relates Lemmas~\ref{lem:inv} and~\ref{lem:states} to the cluster problem of branch-and-bound." Other remarks: not coreB. |
| F12 | MODIFIED | My parts only. | Graph Γ→𝒢 and Δ→Δ_𝒢 (ex:family); B→X′/X^{(j)}; S_t→ξ_t; H→ĥ; σ (coupling) removed; r→ν; q_k→Q_k. ℓ_i was already used throughout. |
| F13 | ACCEPTED | — | TRIAL/CT environments. "Graded grid", "grading", "nodes per coordinate" and "table entries" are used throughout Section 5 and App. A; "slope" and "labels" are removed. Other files: see requests. |
| F19 | MODIFIED | Combined with F159 (same issue). | TRIAL: "and the incumbent x̂=ℓ with value U=F(ℓ), or a better feasible point and its value if one is known"; explicit incumbent update in step (ii). |
| F22 | ACCEPTED — no coreB part | setting-growthcert/exact-localized (coreA/exact). | none |
| F26 | ACCEPTED — no coreB part | No British spellings in my files (checked by grep). | none |
| F28 | ACCEPTED — no coreB part | coreA rewrote Def. 3.2 (constants "for some valid constant"). My files are consistent with it: Lemma `lem:inv` uses a free k, `thm:approx` uses κ̄ = max{1,1/γ} for the defining γ, and `lem:commonmesh` uses κ=max{1,L/g}. | none needed |
| F34 | ACCEPTED | Build log: no overfull box from growth.tex, growth-sharp.tex or appendix-growth.tex. | Rewrapped text. |
| F37 | ACCEPTED — no coreB part | intro/setting (front/coreA). | none |
| F38 | ACCEPTED | My part is Remark `rem:fpt`. | Rewritten per CONVENTIONS §5: the bound holds for every instance; κ̄ is a real parameter, not part of the input and not computed by CT; it is a fixed-parameter bound in p and ⌈κ̄⌉, which CT does not need to know; f is computable. Abstract/intro/conclusion: front. |
| F41 | MODIFIED | My parts only (same as F12). | See F12. P stays {i: L_i>0}. |
| F47 | ACCEPTED | The claim was unproved. | Replaced by the proven `12(2√(nκ)+1)` of Thm `thm:cells` (r=1), attributed to UC, the algorithm that theorem analyzes. |
| F48 | ACCEPTED | — | `rem:cluster` deleted (see F11). |
| F51 | ACCEPTED | My part is Remark 5.8 = `rem:fpt`. | CONVENTIONS lower-bound wording with P≠NP, ETH and randomized ETH; no "must". Conclusion: front. |
| F57 | ACCEPTED | — | New Lemma `lem:commonmesh` with (G1)–(G5), one set of constants, full proof in App. A. The other users and the 100θ⁻¹ cap note are listed in the requests. |
| F58 | ACCEPTED — no coreB part | Section 6/8.6/App. E renames. | My files use P only as {i:L_i>0}. |
| F59 | MODIFIED | My part: chain states. | Chain states written ξ_t in App. A; the example no longer names them. |
| F61 | ACCEPTED — no coreB part | γ is used in my files only for weighted growth. | none |
| F63 | ACCEPTED — no coreB part | — | none (no B_i, Δ_i or ℓ(x) remains in my files) |
| F65 | ACCEPTED | My part: algorithm names. | TRIAL/CT numbered environments with labels `alg:trial`, `alg:ct`. "FG" etc. in other files: see requests. |
| F68 | MODIFIED | (c) and (d) are mine; (e) is resolved by deleting Remark 5.9; (a) and (b) belong to others. | (c) Cor `cor:uniformgrid` kept as the single statement. (d) Example `ex:chain` shortened to a pointer to Prop `lim:prop:messages`. It keeps only what is new there: the rescaled κ bracket and the pointer to Section 11. |
| F70 | ACCEPTED — no coreB part | coreA extended Def. 3.2. | Lemma `lem:inv` uses k instead of κ̄ as its free symbol (see F160). |
| F75 | ACCEPTED | Same as F47. | Same as F47. |
| F83 | ACCEPTED | My part. | "nodes", "grading", "graded", "stage" and "minimizer" are used throughout my files. |
| F84 | ACCEPTED — no change needed | f is the reserved function of `thm:approx`. | none |
| F85 | ACCEPTED — no change needed | `thm:approx` already counts O((J+1)p(\|A\|+n+N)K_μ^p). | none |
| F89 | MODIFIED | CONVENTIONS §4 fixes the common mesh as h_j, not h_j^c; η_j appears only in Section 5. | The common mesh is h_j = s2^{-j} in `lem:commonmesh` and Cor `cor:uniformgrid`. |
| F91 | ACCEPTED — no coreB part | The listed forward references are in setting/grids/recourse-cuts. My forward references (to `thm:cells` and `lim:prop:messages`) are explicit pointers. | none |
| F136 | ACCEPTED — no coreB part | intro (front). | none |
| F139 | ACCEPTED — no coreB part | grids (coreA). | none |
| F140 | ACCEPTED | The sentence is in `rem:cluster`, which is deleted; related.tex already says "can be". | Deletion. |
| F152 | ACCEPTED — no coreB part | coreA added the footnote in setting.tex. | none |
| F155 | MODIFIED | Option 1. R1's sentence "filtered uniform grids also have O(√(nκ)) nodes" would assert an unproved bound for the hull grids of TRIAL with θ=0. I attribute the bound only to UC, which `thm:cells` analyzes. | "Uniform grids also give accuracy-independent counts without any grading condition: UC (Algorithm~\ref{alg:uc}), which filters unions of uniform cells, has at most 12(2√(nκ)+1) nodes per coordinate at every stage when the minimizer is unique (Theorem~\ref{thm:cells} with a single minimizer). The resulting bound is polynomial for fixed p, but because of the factor √n per coordinate it is not a fixed-parameter bound." |
| F156 | ACCEPTED | — | Lemma `lem:commonmesh`. It includes the +[i∈I_Z] term, the stage limit J (least with (9/16)Lns²4^{-J} ≤ ε) and the cap. |
| F157 | ACCEPTED — no coreB part | setting (coreA; already changed) and abstract (front). | none |
| F158 | ACCEPTED — no coreB part | setting (coreA; already changed) and exact. | none |
| F159 | MODIFIED | Combined with F19 (R6 Rewrite 11 wording plus an explicit incumbent). | See F19. |
| F160 | ACCEPTED | — | "let k ≥ max{1,1/γ} satisfy 8kθ² ≤ 1" in Lemma `lem:inv`; Lemma `lem:states` uses √(k n_P); `thm:approx` applies both with k=κ̄. |
| F161 | ACCEPTED | φ(1)=16.21 > 10 log₂3 = 15.85. | "Hence φ(m) ≤ 10log₂(m+2) for m ≥ 2, and φ(m) ≤ 10⌈log₂(m+2)⌉ for all m ≥ 1." |
| F162 | ACCEPTED | — | Mesh paragraph: "every h_ij is a power of two". `thm:approx`(a) rewritten: steps ≥ h_ij because ⌊h_ij⌋ = h_ij for h_ij ≥ 1; at most 1/θ steps per side, 1+2/θ < K_μ nodes; the integer case h_ij < 1 is in its own sentence. |
| F163 | ACCEPTED | — | "all grid nodes of a trial have denominators dividing Γ_X2^α … all table entries are integers of O((1+μ2^μ)(I+q+1)) bits over the common denominator 8Γ_FΓ_X²4^α". |
| F164 | ACCEPTED | — | "a sum of at most I+n terms, each a coefficient times a product of at most two nodes or of two differences of nodes"; μK_μ ≤ 10μ2^μ(I+1). |
| F165 | ACCEPTED | — | "for a graph 𝒢 on the blocks with maximum degree Δ_𝒢 ≥ 1"; coupling 1/(16Δ_𝒢); the proof is updated. |
| F166 | ACCEPTED | — | "let every G_i contain 0 with w_i(0) ≥ h". |
| F167 | ACCEPTED | — | Cor `cor:uniformgrid`: "run the stages of TRIAL with the common mesh h_j=s2^{-j}=2^{1-j}, uniform grids (the construction of Definition~\ref{def:graded} with θ=0) and initial center 0"; graded part has θ ∈ (0,1/4]; nodes/grading wording. |
| F168 | ACCEPTED — no coreB part | setting-growthcert (coreA). | none |
| F177 | ACCEPTED — no coreB part | grids (coreA). My proofs of `lem:states`/`lem:commonmesh`(G4) use the hull, consistent with coreA's new (C1). | none |
| F181 | ACCEPTED | My part: Remark `rem:fpt`. | Uses "cannot be o(p)" with randomized ETH; no "grows linearly". limits/abstract/intro/conclusion: others. |
| F187 | ACCEPTED — no coreB part | grids (C1) (coreA, already changed) and appendix-boundary (exact). | none |
| F204 | ACCEPTED — no coreB part | grids/computation and solver. | none |

Optional or explicitly requested items outside core.json:
* R9 optional (centering): done, with one sentence after TRIAL. R9 says
  "the implementation centers at the incumbent". That is true only at trial
  restarts. Within a trial, `certified_grid.py` line 512
  (`center, bounds = point, next_bounds`) centers at the corrected minimizer,
  as TRIAL does.
* R9 optional (ex:chain Euclidean κ): done, as a proved bracket. The
  experiments (Table `tab:chain`) run the original, unscaled chain, whose
  Euclidean κ ≤ 80, so there is no "measured" unit-box κ to report.

## (2) Labels deleted or renamed

| label | status | references should become |
|---|---|---|
| `rem:cluster` | deleted | No references exist. Any future reference should use `Section~\ref{sec:related}`. |

New labels other groups may cite:
* `alg:trial`: Algorithm TRIAL (one trial with grading θ, cap K, accuracy ε, stage limit J).
* `alg:ct`: Algorithm CT (capped trials).
* `lem:commonmesh`: Lemma "CT with a common mesh". Cite items as
  `Lemma~\ref{lem:commonmesh}(G1)`–`(G5)`: (G1) correction bound; (G2) the
  distance bounds 4κnh_j², κnh_j² and 17/15·κnh_j²; (G3) 9/16·Lnh_j²;
  (G4) radius 4.2√(nκ)h_j + [i∈I_Z]; (G5) cap 8θ⁻¹⌈log₂(n+2)⌉. It also
  defines "CT with a common mesh", states its termination and success trial,
  and states that every bound holds for any initial center in X.

All other labels are unchanged: `sec:growth`, `def:graded`, `eq:step`,
`lem:graded`, `lem:inv`, `eq:energy`, `lem:states`, `eq:statecap`,
`thm:approx`, `eq:logabsorb`, `rem:fpt`, `ex:family`, `ex:chain`,
`prop:sharp`, `cor:uniformgrid`, `app:growth`. Statement changes that
affect citers:
* `lem:inv` and `lem:states` take a free parameter k ≥ max{1,1/γ} with
  8kθ² ≤ 1 instead of κ̄.
* The graph of `ex:family` is now 𝒢, with maximum degree Δ_𝒢 ≥ 1.

## (3) Requests for other files

**exact (appendix-boundary.tex, exact-localized.tex, appendix-localized.tex):**
* appendix-boundary.tex 17–23: replace the paragraph "We use the common-mesh
  variant of Algorithm~1 … We use the rounder constants 22/15 and 5 below."
  by: "We use CT with a common mesh (Lemma~\ref{lem:commonmesh}) under point
  growth. By (G2) and (G4) of that lemma, whenever $8\kappa\theta^2\le1$,
  every grid point $z$ with $Q(z)\le U$ at stage $j$ satisfies
  $\norm{z-x^*}^2\le\frac{17}{15}\kappa nh_j^2\le\frac{22}{15}\kappa nh_j^2$,
  and retained intervals lie within
  $4.2\sqrt{n\kappa}\,h_j+[i\in I_Z]\le5\sqrt{n\kappa}\,h_j+[i\in I_Z]$ of
  $y_{j,i}$. We use the rounder constants $\frac{22}{15}$ and $5$ below."
* appendix-boundary.tex 27: "The pruned-grid trials of
  Section~\ref{sec:growth}" → "The trials of CT with a common mesh
  (Lemma~\ref{lem:commonmesh})".
* appendix-boundary.tex 99 and 180: "the cap
  $8\theta^{-1}\lceil\log_2(n+2)\rceil$ of the common-mesh variant" → "the
  cap of Lemma~\ref{lem:commonmesh}(G5)".
* exact-localized.tex 89: "common-mesh variant" → "CT with a common mesh
  (Lemma~\ref{lem:commonmesh})".
* appendix-localized.tex already cites (G1)–(G5) of `lem:commonmesh` with
  my constants. I checked the items it uses against the lemma: (G2) bounds
  for c, y_j and the 17/15 bound for nodes with m_i(v) ≤ U, and the (G4)
  radius 4.2ρ_j + [i∈I_Z]. They match.

**computation (computation.tex):**
* Line 18: "the capped trials of Algorithm~2" → "CT
  (Algorithm~\ref{alg:ct})".
* Lines 19–21: "It uses a common mesh $h_j=s2^{-j}$ in all coordinates,
  which is CT with a common mesh (Lemma~\ref{lem:commonmesh}), analyzed with
  the Euclidean condition number $\kappa$, but with the cap
  $100\theta^{-1}\lceil\log_2(n+2)\rceil$, larger than the analyzed cap
  $8\theta^{-1}\lceil\log_2(n+2)\rceil$ of Lemma~\ref{lem:commonmesh}(G5);
  it restarts each trial at the current incumbent rather than at $\ell$,
  which Lemma~\ref{lem:commonmesh} allows (its bounds hold for any initial
  center in $X$) but our bit-length analysis does not cover; …"
* Fig. 2 caption: if the plotted radius bound is "5√(nκ)", use
  "4.2√(nκ) (Lemma~\ref{lem:commonmesh}(G4))"; and "labels" → "nodes".
* Line 97: "the √n law of Proposition~\ref{prop:tu-tight}" → "the
  $\sqrt n$ law of Corollary~\ref{cor:uniformgrid}"; "labels" → "nodes".

**optsets (optsets.tex):**
* Lines 45 and 92: "FG" → "TRIAL (Algorithm~\ref{alg:trial})". For example,
  "Consequently, in every trial of TRIAL and of CT every stage has certified
  gap …" and "so every box of TRIAL is $[0,M]^2$".
* Create `\label{alg:uc}` for UC. growth-sharp.tex cites
  `Algorithm~\ref{alg:uc}`.
* Remark `rem:grading` ("makes Theorem~\ref{thm:approx} fixed-parameter
  tractable in $(p,\kappa)$") → "makes Theorem~\ref{thm:approx} a
  fixed-parameter bound in $p$ and $\lceil\bar\kappa\rceil$
  (Remark~\ref{rem:fpt})".

**tu (constraints.tex):** replace `prop:tu-tight` by a sentence citing
Corollary~\ref{cor:uniformgrid}. R5's suggestion: "Corollary~\ref{cor:uniformgrid}
applies verbatim with the constant correction $E_j$". Line 425 should then
cite Corollary~\ref{cor:uniformgrid}. `rem:tu-hybrid` (which cites
`lem:inv`, `lem:states`) is deleted by CONVENTIONS.

**limits (limits.tex):**
* Lines 15–17: use the CONVENTIONS lower-bound wording ("under ETH the
  dependence on $p$ is exponential even when $\kappa\le2$
  (Proposition~\ref{prop:lbwidth}), and under randomized ETH the exponent of
  $\kappa$ cannot be $o(p)$ (Proposition~\ref{prop:lbproduct})").
* Line 281 "the capped algorithm" → "CT".
* End of Prop `lim:prop:messages`: "the corrected-grid algorithm" → "CT".
* My App. A restates the chain objective with states $\xi_t$, controls
  $z_t$ and $\xi_0=0$, and does not name the objective. A rename of
  $G_m$ is therefore harmless, but please keep states $\xi_t$ (CONVENTIONS)
  and controls $z_t$.

**recourse (recourse-balanced.tex):** line 113 "the capped algorithm" → "CT";
line 139 "the choice of $J$ in Algorithm~2" → "the choice of $J$ in CT
(Algorithm~\ref{alg:ct})". Lemmas `lem:inv`/`lem:states` now use the free
parameter $k$ (any $k\ge\max\{1,1/\gamma\}$ with $8k\theta^2\le1$) instead
of $\bar\kappa$.

**front (abstract/intro/conclusion/related):**
* FPT and lower-bound wording as in `rem:fpt` (CONVENTIONS §5).
* related.tex 103–106 is now the only place for the cluster-problem
  comparison, and Section 5 points to it.

**coreA (setting.tex notation table):**
* The table reserves $J$ for grid intervals. In Sections 5 (TRIAL, CT,
  `thm:approx`, `lem:commonmesh`), 8 (TU last level) and 9 (UC), $J$ is the
  stage limit or last stage. I kept $J$ as the stage limit and write grid
  intervals as $[a,a']$ in my files. Please either add "$J$: also the stage
  limit (Sections 5, 8, 9)" to the table, or drop $J$ from the grid-interval
  row.
* Optionally add "$h_j=s2^{-j}$: common mesh (Lemma~\ref{lem:commonmesh})" to
  the $\theta,h_{ij},\eta_j$ row.

## (4) New BibTeX entries

None.

## (5) Checks run (targeted, local; not CI)

* `cd process/w3/checks && python3 coreB-commonmesh.py 1 20 40`, plus seeds
  7 (`… 7 30 4`) and 23 (`… 23 30 200`), with logs in
  `coreB-commonmesh-seed{7,23}.log`. The script checks:
  - with 60-digit mpmath: the radius constants 7.2961 (< 7.3) and 4.1481
    (< 4.2); 8.4/√8 < 3; φ(m) ≤ 10⌈log₂(m+2)⌉ and ψ(m) ≤ 8⌈log₂(m+2)⌉ for
    m ≤ 5000 and m = 10^4…10^15, with the plain log₂ version for m ≥ 2, and
    the m=1 failure of the plain version for φ; the derivative claims;
  - with exact Fractions: the algebra 8/15, 9/16, 17/15 and 32/15 ≤ 4;
  - the rescaled chain for m = 2..8: L = 4^{m+1} exactly, the ray value
    20δ², and objective ≥ (1/8)‖(ς,z)‖² at random points;
  - a brute-force exact simulation of TRIAL with the common mesh on planted
    mixed-integer box QPs (n = 2, 3). Each instance has an exactly certified
    point-growth constant (H + 2M − 2gI ⪰ 0 by exact LDL), κ up to 88, and
    θ = 2^{-μ} with 8κθ² ≤ 1. At every stage the script asserts x* ∈ X^{(j)},
    β_j ≤ OPT, (G1) for all grid points, (G2) with 8/15 for y_j, (G3), (G4)
    with 4.2 and (G5).
  
  Results: all assertions held on 80 instances (20 + 30 + 30).
* `latexmk -pdf -interaction=nonstopmode -outdir=build/coreB main.tex`:
  exit 0, no LaTeX errors. My files produce no overfull boxes. The only
  undefined reference from my files is `alg:uc` (owned by optsets). The
  remaining warnings come from other agents' concurrent edits: undefined
  `alg:ex`, `alg:rec`, `cor:tu-height`, etc.; multiply defined
  `eq:setgrowth` and `rem:np`; overfull boxes in intro, recourse-convex and
  optsets. I also read the PDF text of Section 5 and Appendix A
  (pdftotext).

## (6) Unresolved

* Notation-table clash: $J$ is both grid interval (coreA table) and stage
  limit (Sections 5, 8, 9). See the request to coreA.
* `alg:uc` must be defined by the optsets agent; growth-sharp.tex cites it.
* The κ̄ ≤ 80 statement for the chain relies on Prop `lim:prop:messages`
  (g = 1/8, L = 10), which the limits agent owns. My appendix uses only its
  lower bound $\frac18(\norm\xi^2+\norm z^2)$ and the explicit objective.

## Verification (coreB verifier)

Scope: `sections/growth.tex`, `sections/growth-sharp.tex`,
`sections/appendix-growth.tex`, checked against
`process/w3/sections-before-w3/`, the 51 findings in `assign/core.json`
(the file `assign/coreB-verify.json` named in the task does not exist; the
group file `core.json` was used), the W2 reports R1, R5, R6 and R9 where the
findings point to them, and `CONVENTIONS.md`.

### What was checked

* **Adjudications.** Every finding id in the table above was checked against
  the current text. All ACCEPTED fixes in these files are present and
  correct: F13/F65 (TRIAL and CT environments, labels `alg:trial`, `alg:ct`;
  no "Algorithm 1/2", "FG", "slope", "labels" left in these files), F19/F159
  (initial incumbent), F38/F51/F181 (Remark `rem:fpt` uses the CONVENTIONS
  FPT and lower-bound wording with P≠NP, ETH, randomized ETH), F47/F75/F155
  (UC bound 12(2√(nκ)+1) is what Theorem `thm:cells` states for r=1),
  F57/F156 (Lemma `lem:commonmesh`), F11/F48/F140 (`rem:cluster` deleted;
  no reference to it remains anywhere), F160–F167. The MODIFIED and "no
  coreB part" decisions are justified; for F11 the pure pointer is right,
  because `related.tex` already has the full cluster-problem comparison.
* **Mathematics, line by line.** Re-derived: Lemma `lem:graded` (a)–(c)
  including 72/23 ≤ 4; the mesh construction (h_ij powers of two,
  ¼ < L_i r_i² ≤ 1); Lemma `lem:inv` (i)–(v) with the free parameter k,
  including eq:energy and the constants 8/15, 9/16, 13/16, 17/15; Lemma
  `lem:states` (radius constant 7.2961 < 7.3 < 8, θR/ĥ ≤ 4√(2n_P)+¼,
  φ(1)=16.21 ≤ 20, φ(2)=18.55 ≤ 20, φ' ≤ 4/m, derivative 7.21/m);
  Theorem `thm:approx` (a) termination count 1+2/θ and (b) 2^{μ*} ≤ 6√κ̄,
  μ* ≤ 3(1+log₂κ̄), eq:logabsorb via sup t^p e^{-t}, the K_μ^p sum, the
  table-work bound c(J+1)pI²(60p√κ̄)^p; the bit-length paragraph (node
  formula h_ij((1+θ)^k−1)/θ, α, I+n terms, μK_μ ≤ 10μ2^μ(I+1)); Lemma
  `lem:commonmesh` (G1)–(G5), its termination argument (steps ≥ h_j/2 for
  integer coordinates because h_j = s2^{-j} need not be a power of two,
  1+4/θ nodes) and the success trial; Proposition `prop:sharp` with the
  coupling Λ−2g (completing the square, κ²/(κ−1) ≥ κ); Corollary
  `cor:uniformgrid` (both cases of the induction, the count 4ν+5, the graded
  bound); Example `ex:family` (a)–(d); the rescaled chain bracket of
  Example `ex:chain` (curvatures 10·4^t, 4^{m+1}, 7/4; ray value 20δ²;
  growth 1/8 from Proposition `lim:prop:messages`). All statements are
  correct and proved.
* **Consumers of the new lemma.** `appendix-localized.tex`,
  `appendix-boundary.tex`, `exact-localized.tex`, `optsets.tex` and
  `computation.tex` cite (G1)–(G5) with constants that the lemma states.
  `appendix-tu.tex` uses Proposition `prop:sharp` with the new
  parameterization (g = L̄/2), and the requests of coreB to computation,
  optsets, exact, limits and recourse have been applied by those groups.
* **CONVENTIONS.** Algorithm names and first-use form, terminology (graded
  grid, grading, nodes per coordinate, table entries, minimizer), notation
  (X', X^{(j)}, ĥ, ξ_t, 𝒢, Δ_𝒢, ν, Q_k, k), claim wording (FPT, lower
  bounds, UC count). No British spellings, filler words or report
  artifacts.

### What was fixed

1. **CT, case P = ∅** (`growth.tex`, Algorithm `alg:ct`): "evaluate F on the
   grid ∏{ℓ_i,u_i}" read as enumerating 2^n vertices, which is not within
   the bound of Theorem `thm:approx`(b). Now: "minimize F over the grid
   ∏_i{ℓ_i,u_i} by Lemma `lem:dp` and return a minimizer x̂, β=F(x̂) and
   this grid" (the grid is the certificate).
2. **Stage-J gap in Theorem `thm:approx`(a) and in the proof of Lemma
   `lem:commonmesh`**: "every grid interval has length at most
   h_{iJ}+θs_i ≤ 2h_{iJ}" is false for integer intervals of length one when
   h_{iJ} < 1/2. The proofs now bound the effective widths:
   "Lemma `lem:graded`(a) gives w_i(v) ≤ h_{iJ}+θs_i ≤ 2h_{iJ} for every
   node v", which is what D needs.
3. **growth-sharp.tex, opening paragraph**: "filtering alone leaves
   Θ(√(nκ)) nodes per coordinate on uniform grids" claimed an upper bound for
   the uniform-grid hulls that the section no longer proves (coreB removed
   the unproved constant for that reason). Now "at least of order √(nκ)",
   which Corollary `cor:uniformgrid` proves. "O(√κ log n)" became
   "O(√κ̄ log n) (Lemma `lem:states`)", the quantity that lemma bounds.
   "The slack U−β is a sum of n correction terms" became "can be as large
   as a sum of n correction terms" (U−β ≤ D(y), with equality only when
   U = F(y)).
4. **Corollary `cor:uniformgrid`**: the statement now says the stages of
   TRIAL run "without a cap" and that the box statements concern stages
   "that end by filtering"; the graded part says "With graded grids of
   grading θ ∈ (0,1/4] instead". Without this, a cap could abort the trial
   and stage j+1 would not exist.
5. **UC sentence** (end of growth-sharp.tex): "when the minimizer is unique
   (Theorem `thm:cells` with a single minimizer)" → "under point growth,
   ... (Theorem `thm:cells` with r=1 and κ_S=κ)", because κ is defined only
   under point growth.
6. **Centering paragraph after TRIAL**: rewritten so that the reason for
   centering at y^{(j)} is stated precisely: "by Lemma `lem:inv`(iii), the
   corrected minimizer y^{(j)} is as close to x* as Lemma `lem:inv`(ii)
   requires of the center of stage j+1. Because the centers are ℓ and grid
   points, all denominators stay bounded."
7. **Example `ex:family`**: the grid graph "k×m'" reused k, the free
   parameter of Lemma `lem:inv`; it is now "an m_1×m_2 grid graph, so
   m=m_1m_2", with p = max{m_1+1,3} and 2^m strict local minima. The vague
   "growth forces each flipped block to cost at least a fixed amount" is
   now the exact consequence of (a): "F−OPT is at least 9/8 times the
   number of blocks at (0,0,0)".
8. **Example `ex:chain`**: "leaves κ̄ ≤ 80 unchanged" → "does not change
   κ̄, which stays at most 80"; the appendix proof names the coordinate of
   each rescaled curvature (10·4^t for t<m, 4^{m+1} for ς_m, 7/4 for z_t).
   Source lines rewrapped.

No labels were added, deleted or renamed by the verifier.

### Checks run (targeted, local; not CI)

* `python3 process/w3/checks/coreB-verify-growth.py 11 6`, `... 5 30`
  (log `coreB-verify-growth-seed5.log`) and `... 29 30` (log
  `coreB-verify-growth-seed29.log`): all assertions held. The script checks,
  in exact Fractions: Lemma `lem:graded` (a)–(c) on 3000 random grids;
  termination counts 1+2/θ (power-of-two meshes) and 1+4/θ (common mesh)
  on 2000 random grids; Example `ex:family` (growth 1/2, curvature ≤ 21/8,
  strict local minima) on a path and an edge; Proposition `prop:sharp` on
  random grids (1012 min-marginals tested); Corollary `cor:uniformgrid`
  for n = 4, 6 and κ ∈ {2, 8, 40, 200} (16 stages with (ν+1)h_j ≤ 1);
  scalar facts of Theorem `thm:approx`; and a brute-force simulation of
  TRIAL with per-coordinate meshes under an exactly certified weighted
  growth constant (H+2M−2γ diag(L) ⪰ 0), asserting Lemma `lem:inv` (i)–(v)
  and Lemma `lem:states` (radius with 7.3, cap K(θ,n_P)) at every stage,
  on 66 planted instances with n = 2, 3 and curvatures up to 768.
* `python3 process/w3/checks/coreB-commonmesh.py 101 15 40` (log
  `coreB-verify-commonmesh-seed101.log`): constants and (G1)–(G5) held on
  15 further instances.
* `latexmk -pdf -interaction=nonstopmode -outdir=build/coreB-verify
  main.tex`: exit 0, no LaTeX errors, no overfull boxes, no undefined or
  multiply defined references or citations in the final run. (Two earlier
  runs stopped in BibTeX with "no \bibdata" while other agents were
  writing files; a rerun was clean.) The rendered text of Section 5 and
  Appendix A was read with `pdftotext`.

### Remaining

* Notation-table clash (coreA, `setting.tex`): the table lists J as a grid
  interval, while Sections 5, 8 and 9 use J for the stage limit. Still
  open; coreB's request to coreA stands.
* R_ij (radius in Lemma `lem:states`) and R (Lemma `lem:graded`(b),
  Corollary `cor:uniformgrid`) are local radii. R5's table proposed ϱ_ij,
  but CONVENTIONS does not require the rename, and appendix-proximal uses
  ϱ for another radius; left unchanged.

## Verification (coreB verifier, second pass)

Scope: the current `sections/growth.tex`, `sections/growth-sharp.tex` and
`sections/appendix-growth.tex`, which include the first verifier's fixes.
They were checked against `process/w3/sections-before-w3/`, the 51 findings
of `assign/core.json` (`assign/coreB-verify.json` does not exist), R1 (M3,
m1–m12), R6 (Rewrites 11 and 12), R9 (Section 5 items and optional
requests) and `CONVENTIONS.md`.

### What was checked

* **Adjudications.** Every row of the table in part (1) was rechecked against
  the text. The ACCEPTED fixes are present and correct, and the MODIFIED and
  "no coreB part" decisions are justified. For F155 the UC attribution
  (option 1) is right: R1's alternative sentence would assert an unproved
  O(√(nκ)) bound for TRIAL's hull grids with θ=0. For F89, CONVENTIONS fixes
  the common mesh as h_j.
* **Mathematics, re-derived line by line.**
  - Lemma `lem:graded` (a)–(c), including the integer cases with ĥ, the
    factor 72/23 ≤ 4 and m ≤ ⌈·⌉ when m = 1.
  - The mesh paragraph.
  - TRIAL and CT.
  - Lemma `lem:inv` (i)–(v), including eq:energy and the constants 8/15,
    9/16, 13/16 and 17/15.
  - Lemma `lem:states`: radius 7.296 < 7.3, θR/ĥ ≤ 4√(2n_P)+¼, φ(1),
    φ(2), the derivative comparison, and stage 0.
  - Theorem `thm:approx`:
    - (a): termination trial, 1+2/θ, s_i+1, gap ≤ (8/9)ε;
    - (b): μ*, 2^{μ*} ≤ 6√κ̄, ΣK_μ^p ≤ 2K_{μ*}^p, eq:logabsorb (via
      e·ln2 > 1), and the table-work and b² bookkeeping, including the factor
      evaluations.
  - The bit-length paragraph: node formula, cumulative dyadic centers,
    common denominator 8Γ_FΓ_X²4^α, and the I+n terms.
  - Lemma `lem:commonmesh` (G1)–(G5), termination and the success trial.
  - Proposition `prop:sharp` (eigenvalues 2Λ−2g and 2g, completing the
    square, κ²/(κ−1) ≥ κ).
  - Corollary `cor:uniformgrid`: both inductions, the count 4ν+5, and the
    graded lower bound.
  - Example `ex:family` (a)–(d) and the 9/8 sentence.
  - The rescaled-chain bracket of Example `ex:chain`, against the current
    Proposition `lim:prop:messages` (Ψ_m ≥ ⅛(‖ξ‖²+‖z‖²), L = 10, m ≥ 2).

  No mathematical error was found.
* **Consumers.** These citations match the current statements:
  - `appendix-localized.tex`, `appendix-boundary.tex`, `exact-localized.tex`
    and `computation.tex` cite (G1)–(G5) with constants the lemma states;
  - `appendix-tu.tex` applies Proposition `prop:sharp` with Λ=L̄ and g=L̄/2
    (coupling 0, κ=2, hypothesis w_i(0) ≥ h);
  - `constraints.tex`, `computation.tex` and `intro.tex` cite Corollary
    `cor:uniformgrid` correctly;
  - `optsets.tex` defines `alg:uc`, and `thm:cells` states
    K_S = 12r(2√(nκ_S)+1);
  - `limits.tex` states the lower bounds exactly as Remark `rem:fpt`
    summarizes them;
  - ETH and rETH are defined in `intro.tex` before Section 5.
* **Labels.** All pre-revision labels survive except `rem:cluster`, which
  CONVENTIONS deletes; no file references it. The new labels are `alg:trial`,
  `alg:ct` and `lem:commonmesh`.
* **CONVENTIONS and writing.** Algorithm names and first use, terminology,
  notation, and the FPT and lower-bound wording all comply. There are no
  British spellings, filler words or report artifacts.

### What was fixed (second pass)

1. **Corollary `cor:uniformgrid`** (statement and proof). The corollary
   counted the nodes of "the grid of stage j+1" even when j is the last
   stage, which filters and then fails, so stage j+1 does not exist. Both
   parts now say "the grid of stage j+1, if that stage is run", and the
   proof's counting sentence starts "When (ν+1)h_j ≤ 1 and stage j+1 is
   run".
2. **UC sentence** (end of growth-sharp.tex). "The resulting bound is
   polynomial for fixed p" was imprecise, because κ can be exponential in I.
   It now reads "The resulting running-time bound is polynomial in I+q and κ
   for fixed p" (Theorem `thm:cells`).
3. **Example `ex:family`.** The family assumes Δ_𝒢 ≥ 1, but a 1×1 grid graph
   has no edge. The text now says "an m_1×m_2 grid graph with m=m_1m_2 ≥ 2".
4. **Sentence after Lemma `lem:commonmesh`.** It gave the reason for the
   smaller constants as "because all coordinates share one mesh". The actual
   reason is that (G2) bounds Euclidean distances in units of the common
   mesh, so (G4) needs no conversion through √L_i > 1/(2r_i), which costs
   Lemma `lem:states` up to a factor 2. The sentence now says this and adds
   the price, κ ≥ κ̄.
5. **Proof for Example `ex:chain`.** The objective is now named Ψ_m, as in
   Proposition `lim:prop:messages`, and the proof states which coordinate
   has curvature 10·4^t (ς_t with t<m).
6. **Wording.** In the centering paragraph after TRIAL, "Later centers must
   be close to x*" became "need to be close".

No labels were added, deleted or renamed in this pass.

### Checks run (targeted, local; not CI)

* New script `process/w3/checks/coreB-verify-ct.py`, run as `… 41 300` and
  `… 97 300` (logs `coreB-verify-ct-seed{41,97}.log`). It runs the full CT
  schedule in exact arithmetic on planted mixed-integer box QPs (n = 2, 3)
  with an exactly certified weighted growth constant (κ̄ up to 256). It
  asserts:
  - Theorem `thm:approx`(a): β ≤ OPT ≤ F(x̂) ≤ β+ε;
  - validity of the returned record under Definition `def:cert`, with (C1)
    and (C2) recomputed from the grids alone;
  - Theorem `thm:approx`(b): the successful μ satisfies μ ≤ μ* and
    2^μ ≤ 6√κ̄, and trial μ* run alone succeeds;
  - the termination trial μ_T of the proof of (a) succeeds with at most
    max(1+2/θ, s_i+1) nodes;
  - every node denominator divides Γ_X2^α.

  A stress mode with caps 5 for μ ≤ 3, then 2^{μ+1}+2, forces aborts. It
  exercised 556 aborted or failed trials, after each of which the CT output
  still satisfied (a) and (C1)/(C2). The scalar facts of (b), eq:logabsorb
  (p ≤ 40), the node formula and an exhaustive integer check of Lemma
  `lem:graded` (3360 grids) also passed. All assertions held.
* Reruns of the first-pass scripts with new seeds also held:
  - `coreB-verify-growth.py 13 10` (log
    `coreB-verify2-growth-seed13.log`): Lemmas `lem:inv` and `lem:states` on
    10 instances;
  - `coreB-commonmesh.py 77 10 40` (log
    `coreB-verify2-commonmesh-seed77.log`): (G1)–(G5) on 10 instances.
* `latexmk -pdf -interaction=nonstopmode -outdir=build/coreB-verify main.tex`
  exited 0, with no LaTeX errors, no overfull boxes, and no undefined or
  multiply defined references in the whole build. The changed passages were
  read in the rendered PDF (`pdftotext`).

### Remaining

* Notation-table clash (coreA, `setting.tex`). Table `tab:notation` lists J
  only as a grid interval, while Sections 5, 8 and 9 use J for the stage
  limit. coreA has not answered. Requested row text:
  "$J$, $w(J)$, $w_i(v)$ & grid interval (in Sections~\ref{sec:growth},
  \ref{sec:constraints} and~\ref{sec:optsets} $J$ is also the stage limit),
  its effective width, largest width at node $v$".
* Local radii R and R_ij in Section 5 coincide in letter with the reserved
  R of Section 6. CONVENTIONS does not require a rename, and each use is
  defined where it appears. They are left unchanged, as in the first pass.
