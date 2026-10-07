# W3 report — group `limits`

Files edited: `sections/limits.tex`, `sections/appendix-lbproduct.tex`,
`sections/appendix-moments.tex`. No other file was edited. Check scripts:
`process/w3/checks/limits-setgrowth.py`, `limits-reductions.py`,
`limits-moments.py`.

## Summary of structural changes

- Section 10 now has seven subsections: 10.1 conditioning; 10.2 value-oracle
  model; 10.3 width and the exponent of κ (new label `sec:limits-width`,
  holding `prop:lbwidth` and `prop:lbproduct`); 10.4 messages; 10.5 set
  growth; 10.6 product domains; 10.7 local corrections and moments (now a
  one-paragraph summary).
- Remark `lim:rem:dk` moved to the appendix (new subsection `app:dk`), with a
  four-line summary after Corollary `lim:cor:nopolylog`.
- The former Section 10.6 material (Lemma `lim:lem:mixture`, Definition
  `lim:def:moments`, Proposition `lim:prop:moments` with its statement,
  proof, discussion and Remark `lim:rem:moments`) is now in
  `appendix-moments.tex`.
- Appendix structure: `appendix-lbproduct.tex` now opens the appendix
  section "Proofs and supplements for Section 10" (`app:limits`) with
  subsections `app:dk` and `app:lbproduct`; `appendix-moments.tex` is the
  subsection `app:moments`. The input order lbproduct → moments must stay.
- Notation: Subset Sum items `m`, target `a_0`, item sum `A`, penalty
  `‖a‖²` (was M), tie-break weight `λ` (was ε), binary code `χ`; running
  sums `y` (was s); chain states `ξ_t`, chain objective `Ψ_m` (was G_m),
  residuals `ρ_t`, value function `V`; random vector `Y`; multilinear part
  `Ψ_0`; set growth `g_S`, `κ_S`; optimal set `𝒮`; per-coordinate `L_i` in
  Prop. `lim:prop:setgrowth`; lbproduct: class size `N_0`, edge lists
  `E_cd`, weight range `ρ`, ground set `𝒰`, pair superscripts, `σ` counter,
  `y,z` running sums; moments: bags `B^L_i`, `B^R_j`, sums `ū, v̄`,
  nodes `ζ_k`, residual sum `c̄`, `Υ` (was Π), weight `λ`, occupied width
  `ω_i(μ)`, control-cell length `h'` (was ω), mean `x̄` in the lemma.
- Algorithm names: CT (`alg:ct`), TRIAL (`alg:trial`), TU-GRID
  (`alg:tugrid`); "nodes per coordinate".

## 1. Adjudication

| id | verdict | reason | change |
|---|---|---|---|
| F0 | MODIFIED (my part) | Abstract/intro are front's. In my files the TU statement must match CONVENTIONS. | Paragraph after Prop. `lim:prop:constraints` rewritten: the instances satisfy Def. `def:tu-model` with η=1, s=a_0, two values per discrete coordinate, κ_c=1; by the discussion after Thm `thm:tu-approx`, the pseudopolynomial level-0 grid of TU-GRID cannot be removed unless P=NP. No polynomiality claim in my files. |
| F13 | ACCEPTED (my part) | Terms in my files. | "capped algorithm", "filtered-grid algorithm", "corrected-grid algorithm", "Algorithms 1 and 2", "state cap", "states" → CT / TRIAL / "nodes per coordinate". |
| F27 | ACCEPTED | limits.tex 7 "does real work". | Opening sentence rewritten: "This section shows what fails when a hypothesis is dropped without such a replacement…". |
| F29 | ACCEPTED (my part) | Both slips are in my files. | "qualitative growth lemma" → Lemma `lem:unique-growth` (in moved Remark `lim:rem:dk`); random vector in `prop:lbwidth` → `Y`. Other items (optsets, smoothed, boundary) are not mine. |
| F30 | ACCEPTED (my part) | rETH not expanded near use. | ETH and rETH defined at the start of §10.3 with citations (IPZ 2001, Dell et al. 2014); Prop. `prop:lbproduct` follows directly. |
| F36 | MODIFIED (my part) | Same as F0. The "uniform meshes are forced" wording is not in my files. | As F0. |
| F44 | ACCEPTED (my part) | Overstatement. | Bullets, §10.3 lead-in and the paragraph after Prop. `prop:lbproduct` now say "cannot be o(p), already for integer box quadratics, under rETH"; "must grow linearly", "Θ(p)" removed. Prop. `prop:lbproduct` "In particular" clause made effective (a(p) ≤ p/ψ(p)) and proved in App. (ψ' = max{1, min{ψ, p/C}}). |
| F52 | ACCEPTED (my part) | Bullet attributed both props to ETH. | Bullet uses the CONVENTIONS §5 wording verbatim in substance. |
| F53 | REJECTED for my files / note | The reviewer's proposed wording ("no corrected-grid certificate has accuracy-independent grid size") is false after M1 (F178). | Nothing in my files. The optsets agent already wrote the correct restricted wording in Remark `rem:grading` (checked: consistent with the new Prop. `lim:prop:setgrowth`). |
| F55 | ACCEPTED (my part) | Prop. `prop:oraclebarrier` used g, κ for set growth. | Now g_S, κ_S, with the set-growth inequality written inline for general C² f. |
| F59 | ACCEPTED (my part) | S for optimal set, chain S_t, support S. | Optimal set 𝒮; chain states ξ_t; "support of a binary x" without a letter. |
| F65 | ACCEPTED (my part) | As F13. | As F13. |
| F68 | ACCEPTED (my part) | Prop. `lim:prop:messages` is the statement with proof. | Kept complete (p, I, growth, L, κ ≤ 80, ν, pieces, CT polynomial). The core agent already shortened Example `ex:chain` to a pointer. |
| F70 | ACCEPTED (my part) | Set growth notation. | g_S, κ_S used in Props. `lim:prop:setgrowth` and `prop:oraclebarrier`, citing Def. `def:growth`. |
| F88 | ACCEPTED (my part) | §10 opening said Sections 4–8 assume a unique minimizer. | Opening now: Sections 4–6 rest on the four hypotheses; §7 replaces corrections by value functions, §8 replaces the product domain, §§8–9 use set growth. |
| F90 | ACCEPTED (my part) | Letter collisions. | Prop. `prop:lbwidth`: V→Y, vertex set [n]; bags (moments) → B^L_i, B^R_j; edge set (lbproduct) → E_cd; μ(v) in Prop. `lim:prop:messages` → value function V(v) (it is the value function of ξ_m in the sense of §7; m_i is reserved for grid min-marginals of Q, so m_{ξ_m} would be wrong); objective G_m → Ψ_m; S_t → ξ_t. |
| F94 | ACCEPTED (my part) | Prop. `lim:prop:setgrowth` used one L. | Stated with L_i (any valid L_i ≥ 2); κ_S bound uses L = max L_i. |
| F134 | ACCEPTED (my part) | Missing credit. | After Prop. `lim:prop:constraints`: "The running-sum encoding of Subset Sum is that of Bienstock and Muñoz [App. A]; see also [CifuentesParrilo2016, Example 1.1]. What we add is a unique minimizer and the growth constant, so that κ=1." Locator is Example 1.1 (numbering in arXiv v2 = journal version; CONVENTIONS said "Ex. 1"). Prop. `prop:lbwidth` introduced as "the standard box formulation of maximum independent set"; hidden-well and hidden-bump arguments cite Nemirovski–Yudin. Intro item (v) is front's (already updated). |
| F146 | ACCEPTED (my part) | Missing sources. | Hidden-bump argument cites NemirovskiYudin1983; rETH cites DellEtAl2014; Clique lower bound cites ChenEtAl2006 and [CyganEtAl2015, Theorem 14.21]; the Clique → multicolored clique reduction is stated explicitly. |
| F147 | ACCEPTED (my part) | Missing references at my locations. | §10.4 intro cites KolmogorovPockRolinek2016 and KuricAhmetspahicPock2024 (exponential worst-case bound for nonconvex costs, verified in the abstract) and states that our result bounds the message itself. Moments discussion cites Vorobev1962 for gluing of separator-consistent bag laws. Cifuentes–Parrilo cited (F134). Other references in F147 belong to other files. |
| F178 | ACCEPTED, with a proved extension | The proof covered only filtering runs; the reviewer's counterexample is valid (re-checked). | Prop. `lim:prop:setgrowth` restated: (a) every min-marginal satisfies m_j(v) ≤ −(L_j/8)w_j(v)² on every grid of X (stronger form of the old β bound, same proof); (b) filtering with U ≥ OPT removes nothing, so every run of filtering with U_j ≥ OPT, in particular TRIAL/CT, that certifies ε ends with ≥ 1+1/(2√ε) nodes per coordinate; (c) proved statement for general valid path certificates: every stage-0 interval not contained in B^(1) (every interval if k=0) has length ≤ 2√ε. Text after the proof gives the reviewer's n=2, ε=1/50 certificate (two-node last grid) and says we do not know whether every valid certificate has ε^{−Ω(1)} nodes in total. Bullet now says "does not bound the grids produced by filtering". |
| F180 | ACCEPTED | Bound was shown for the constant run. | Deterministic part: indices t_c, at most one infinite, finite ones distinct ⇒ some F_c forces ≥ |𝒞|−1 evaluations. Randomized part: "first Q evaluation points of the constant run" and the halting argument written out. |
| F181 | ACCEPTED (my part) | As F44/F52. | Bullets and §10.3 text. Conclusion/abstract/intro/rem:fpt already changed by their owners (checked). |
| F182 | ACCEPTED | rETH undefined; Chen et al. is for Clique; effective o(p). | rETH defined (Dell et al. definition: error ≤ 1/3); reduction Clique → multicolored clique stated; Cygan Thm 14.21 cited; "In particular" clause stated and proved in the effective form; I also justified that a bound needed only for p ≥ k_0 suffices. |
| F183 | ACCEPTED | Notation clashes, missing hypothesis. | Range {1..ρ}; ground set 𝒰; class size N_0; edge lists E_cd with superscripts cd (omitted inside brackets, stated); S_l → σ_l; A_l,B_l → y_l,z_l; "Suppose the minimum-weight clique is unique" before g ≥ 1/(n_v N_0²). |
| F184 | ACCEPTED | Union bound implicit. | Added. |
| F185 | ACCEPTED | Uniform L; misplaced phrase. | d_i = L_i w_i²/8 and L_i ≥ 2 throughout; the cellwise sentence rewritten as suggested. |
| F186 | MODIFIED | Whose widths was unclear. | Chose the reviewer's second option, which needs no extra hypothesis: occupied width ω_i(μ) is defined per feasible point; the proposition gives a feasible point μ with value 1/4−(2r+1)/(16r) and Σω_i(μ)² ≤ (4r−2)max{2rh,h'}², and the consequence says no φ makes value(μ) ≥ OPT − φ(p, ν̄/g, k) ν̄ Σ ω_i(μ)² for all feasible μ. R_k is no longer needed and was dropped. |
| F190 | ACCEPTED | Decoding step missing. | Proof: n ≥ 1 ⇒ α ≥ 1, x* ≠ 0, χ(x*) ∈ [1, 2^n−1], so ⌊A/2^n⌋ = −α for every A within 1/2. Statement also says the problem is NP-hard (used by the bullet "neither parameter can be dropped"). |
| F191 | ACCEPTED | L=0 claim needed an L=0 instance. | Paragraph after the SETH remark: the multilinear part Ψ_0 has L=0, the same unique minimizer and g=1/n by new eq. `lim:eq:lbwidth`, so κ=1; CT runs in 2^p poly(I) for L=0; hence optimal up to the base under ETH and optimal under SETH (LMS 2018). |
| F192 | ACCEPTED | Overclaim and vague clause. | Paragraph after Cor. `lim:cor:nopolylog`: polynomial for κ ≤ I^{O(1)} (Thm `thm:exact`), NP-hard for κ ≤ 2^{O(I)}, and, by padding with decoupled t_j² terms in separate bags (p, uniqueness and κ unchanged), NP-hard for κ ≤ 2^{I^δ} for every fixed δ>0; "bit length polynomial in I+q+log κ". |
| F193 | ACCEPTED (my part) | Clashes. | Moments bags B^L_i, B^R_j; lbwidth Y and Ψ_0 (the reviewer's P(x) would clash with P = {i: L_i>0}). Boundary part is not mine. |
| F195 | ACCEPTED (my part) | Terms and idiom. | limits.tex 539 → CT; limits.tex 7 rewritten (F27). Boundary part not mine. |

## 2. Labels deleted or renamed

None deleted or renamed. Moved (references need no change):
`lim:rem:dk` (now Appendix, subsection `app:dk`); `lim:lem:mixture`,
`lim:def:moments`, `lim:prop:moments`, `lim:rem:moments`, `lim:eq:momsplit`,
`lim:eq:pi` (all in `appendix-moments.tex`). `app:lbproduct` and
`app:moments` are now subsection labels.

New labels: `app:limits` (appendix section for Section 10),
`app:dk` (conditioning of the DK bounded-coefficient reduction),
`sec:limits-width` (§10.3, width and the exponent of κ),
`lim:eq:lbwidth` (growth 1/n of the multilinear independent-set instance).

## 3. Requests for other files

1. **computation.tex (computation)**. Prop. `lim:prop:messages` now writes
   the chain objective as Ψ_m and the states as ξ_t (F90; G_m clashed with
   grids, S_t with scopes/separators). Please change "the family $G_m$ of
   Example~\ref{ex:chain}" → "the family $\Psi_m$ of
   Proposition~\ref{lim:prop:messages} (Example~\ref{ex:chain})", "Bellman
   message for $S_m$" → "Bellman message for $\xi_m$", and the caption
   "expanding-box chain $G_m$" → "expanding-box chain $\Psi_m$".
2. **computation.tex (computation), ~line 254.** "on which corrected-grid
   certificates of accuracy $\varepsilon$ need of order
   $\varepsilon^{-1/2}$ nodes per coordinate" is no longer proved (F178).
   Replace by: "on which every run of filtering with thresholds
   $U_j\ge\OPT$, in particular CT, that certifies accuracy $\varepsilon$
   ends with at least $1+1/(2\sqrt\varepsilon)$ nodes per coordinate".
3. **appendix.tex (coordinator).** Keep `appendix-lbproduct` immediately
   before `appendix-moments`: the first opens the appendix section
   (`\section`, `app:limits`), the second is its third `\subsection`.
4. **constraints.tex (tu).** My TU paragraph after Prop.
   `lim:prop:constraints` cites "the discussion after
   Theorem~\ref{thm:tu-approx}" for the parameter accounting (η, s/η, K_Z,
   κ_c). Please keep that discussion (it is currently correct and
   consistent).
5. **setting.tex notation table (core), optional.** If the table lists
   renamings, the chain states are ξ_t and the Subset Sum target is a_0 (items
   a_1,…,a_m, sum A) in Section 10.

## 4. New BibTeX entries

None needed. All new keys I cite are already in `references.bib`
(CifuentesParrilo2016, DellEtAl2014, CyganEtAl2015,
KolmogorovPockRolinek2016, KuricAhmetspahicPock2024, Vorobev1962), and I
checked their metadata against Crossref: 10.1137/151002666,
10.1145/2635812, 10.1007/978-3-319-21275-3, 10.1137/15M1010257,
10.1137/23M1556915, 10.1137/1107014 (all match). Content checks: Cifuentes–
Parrilo Example 1.1 (arXiv 1411.1745v2, journal version) is the Subset Sum
path system; Dell et al. (arXiv 1206.1775) define rETH with error ≤ 1/3;
Kuric–Ahmetspahic–Pock's abstract states the exponential bound for the
nonconvex case; Cygan et al. Theorem 14.21 (Clique, f(k)n^{o(k)}, ETH) was
confirmed through a verbatim quotation in arXiv 2311.08988, not from the
book itself.

## 5. Checks run (targeted)

- `python3 process/w3/checks/limits-setgrowth.py`: 400 random rational
  grids, n=2..4: m_j(v) ≤ −(L_j/8)w_j(v)² at every node, every interval
  retained at U=0, β ≤ −(L_j/8)W_j²; the n=2, ε=1/50 certificate is valid
  ((C1),(C2), gap 1/50), last grid 2 nodes, removed stage-0 intervals 1/5 ≤
  2√ε. PASS.
- `python3 process/w3/checks/limits-reductions.py`: Prop.
  `lim:prop:unique` in the new notation (25 random instances: split
  identity, uniqueness, decision gap, growth with g=λ/(m(1+2(m−1)‖a‖²)),
  κ bound); Prop. `lim:prop:constraints` (60 random instances: unique
  minimizer, x_0*=0 iff yes, OPT values); Prop. `prop:lbwidth` (random
  graphs n ≤ 5: decoding ⌊A/2^n⌋=−α for A within 1/2, growth 1/(2n), and
  growth 1/n of Ψ_0). PASS.
- `python3 process/w3/checks/limits-moments.py`: r=1..4: split identity
  (`lim:eq:momsplit`), Ψ−1/4 = 2Υ+λ(ū+v̄), growth with g_r at random
  points, witness value 1/4−(2r+1)/(16r), moments of s equal below order
  2r and unequal at 2r; Remark `lim:rem:moments` moments. PASS.
- `latexmk -pdf -interaction=nonstopmode -outdir=build/limits main.tex`:
  pdflatex has no errors from my files. latexmk exits 12 because bibtex
  read a partial `main.aux` in the paper root, written concurrently by
  another agent's build (the "\@@BOOKMARK" error of the first run had the
  same cause: a partial `./main.out`). Not caused by my files.
- Same command on an isolated snapshot (`/tmp/limcopy`, copies of
  main.tex, macros.tex, references.bib, sections/, figures/): exit 0. My
  files produce no errors, no undefined references or citations, no
  overfull boxes (one 0.23pt box was removed by a wording change), and no
  hyperref warnings (math in the §10.3 title wrapped in
  `\texorpdfstring`). Remaining undefined items belong to other files
  (HornJohnson2013, tab:scip).

No project-wide verification was run, and CI was not consulted.

## 6. Unresolved

- Whether every valid path certificate for the set-growth family needs
  ε^{−Ω(1)} nodes in total is open; the paper now says so and proves only
  the stage-0 statement (c).
- The rename G_m → Ψ_m depends on request 1; until computation.tex follows,
  Section 11 writes G_m for the same family.
- The DK construction details in Remark `lim:rem:dk` (ℓ, D, 5ℓ+2 variables,
  diagonal entry 10) were not re-read against the DK PDF by me; R4 and R7
  verified them (R7 with an exact script), and I only renamed symbols
  (B → c, q → ϱ, R → ‖d‖²).
- The Bienstock–Muñoz locator "Appendix A" is taken from R7 (arXiv v15);
  I did not re-check it against the SIOPT version.

## Verification (verifier for group `limits`)

Files re-checked and edited: `sections/limits.tex`,
`sections/appendix-lbproduct.tex`, `sections/appendix-moments.tex`. No other
file was edited. New check script: `process/w3/checks/limits-verify-setgrowth.py`.

### What was checked

- **Adjudications.** I checked all 33 findings in `assign/limits.json`
  against the diff from `sections-before-w3/` and against the full R4
  report. Every ACCEPTED fix is present in the files. The MODIFIED decisions
  (F0, F36, F186) and the REJECTED part of F53 are justified. F53's proposed
  wording would restate the claim that F178 shows to be false, and Remark
  `rem:grading` in optsets.tex (lines 258–264) already uses the correct
  restricted wording. For F90, choosing V(v) instead of the reviewer's
  m_{ξ_m}(v) is right: m_i is reserved for grid min-marginals of Q, and
  CONVENTIONS reserves V for value functions.
- **Mathematics.** I re-derived every changed statement and proof line by
  line:
  - Prop. `lim:prop:unique` and Cor. `lim:cor:nopolylog` after the renames;
  - Prop. `lim:prop:oracle`: the t_c argument; the randomized argument with
    the first Q evaluations;
  - Remark `lim:rem:oracle`;
  - Prop. `prop:lbwidth`: decoding, the L = 0 instance Ψ_0 with g = 1/n,
    κ = κ̄ = 2;
  - the SETH and L = 0 remarks;
  - Prop. `prop:lbproduct` and its appendix proof: isolation with the union
    bound, the Hessian diagonal, n ≤ k + 2k²N_0², the effective ψ' argument,
    and (1+log₂κ)² ≤ 4κ;
  - Prop. `lim:prop:messages`;
  - Prop. `lim:prop:setgrowth` (a), (b), (c) and the n = 2, ε = 1/50 example;
  - Prop. `prop:oraclebarrier`;
  - Prop. `lim:prop:constraints` and the TU paragraph, against Def.
    `def:tu-model` and the discussion after Thm `thm:tu-approx`;
  - Lemma `lim:lem:mixture`, Def. `lim:def:moments`, Prop.
    `lim:prop:moments` (identities, vertex values of Υ, growth g_r, parity
    moments, witness value, occupied widths, consequence) and Remark
    `lim:rem:moments`.
- **Moved material.** All 35 labels of the three pre-W3 files still exist, and
  moved objects kept their proofs. Nothing proved was lost: the DK remark and
  the moments material are complete in the appendix. The citation claims I
  could check online are correct: Cifuentes–Parrilo Example 1.1 in arXiv
  1411.1745v2 is the Subset Sum path system, and Kuric–Ahmetspahic–Pock state
  exponential worst-case complexity in the nonconvex case.
- **CONVENTIONS and wording.** I checked algorithm names (CT, TRIAL,
  TU-GRID), "nodes per coordinate", g_S/κ_S, 𝒮, ξ_t, L_i, the §5 claim
  wording for lower bounds and TU, the credit to Bienstock–Muñoz and
  Cifuentes–Parrilo, and the absence of banned phrases and process artifacts.
- **Other files.** computation.tex has already applied requests 1 and 2 of
  this report (Ψ_m, ξ_m, and the restricted set-growth sentence). Other
  files cite these labels consistently with the current statements: intro
  Thm `thm:intro-lower`, conclusion, Remark `rem:fpt`, optsets
  `rem:grading` and constraints §8.

### Problems found and fixed

1. **False bit-length claim** (limits.tex, paragraph after Cor.
   `lim:cor:nopolylog`; it came from R4's suggested wording in F192). "All
   numbers have bit length polynomial in I+q+log κ" is false. Appendix
   `app:growth` gives b ≤ c(1+μ2^μ)(I+q+1) with 2^μ ≤ 6√κ̄, which is
   polynomial in κ, not in log κ. The text now says "O(√κ(1+log κ)(I+q+1))
   bits (Appendix app:growth)". It also states why Theorem `thm:exact` is
   polynomial for κ ≤ I^{O(1)}: its proof bounds f_1 by f(p,κ) times a power
   of 1+log₂κ. The theorem itself only says that f_1 is computable.
2. **Notation in Prop. `lim:prop:setgrowth`.** Part (c) and its proof used
   the undefined B^{(1)}_i and B^{(0)}. CONVENTIONS and Def. `def:cert` use
   X^{(j)} for stage boxes, so these are now X^{(1)}_i and X^{(0)}. Grid
   interval lengths γ_i were renamed to δ_i, because CONVENTIONS reserves γ
   for weighted growth and uses δ for gaps.
3. **Scope of (b).** "The filtering step with U ≥ OPT removes nothing" holds
   only for a grid of X, so the statement now says "applied to a grid of X",
   and the run is "a run … that starts from a grid of X". The proof now
   starts with "Let G be a grid of X" and says "by induction". "Every trial
   of TRIAL" was changed to "every run of TRIAL and hence of CT".
4. **Proof of (c).** It now notes that the second alternative of (C1)
   requires w(J) = 0. For k = 0 it now writes the chain
   −W_i²/4 ≥ min Q^{(0)} ≥ β ≥ −ε, which separates the corrected minimum
   from the certificate's β. The text after the proof now says "[β,0)", and
   "part (c) bounds only the stage-0 grid" replaces "part (c) is what the
   argument gives for it".
5. **Prop. `prop:lbwidth` proof.** "Since n ≥ 1, α ≥ 1 and x* ≠ 0, so …" did
   not justify x* ≠ 0. It now reads: Φ(x*) = −α < Φ(0), so x* ≠ 0. The
   approximation A was renamed to Ψ̃, because A is the item sum in
   §10.1.
6. **Prop. `lim:prop:constraints`.** The credit paragraph sat between the
   proposition and its proof, so I moved it before the proposition as a
   lead-in. In the TU paragraph, "κ_c = 1" holds only for a suitable \bar L.
   It now says "the objective is affine, so every \bar L > 0 is valid, and
   \bar L ≤ g_S gives κ_c = 1", which matches constraints.tex.
7. **Opening paragraph (F88).** Sections 4–6 use weighted growth (Section 5)
   and point growth (Section 6). The text now says "weighted or point
   growth", and "set growth instead of growth at one minimizer".
8. **§10.4 lead-in.** "The next proposition bounds the size of the message
   itself" read as an upper bound. It now says "gives a lower bound for the
   message itself".
9. **Sentence after Prop. `prop:lbproduct`.** It said "cannot be improved to
   f(p)κ^{o(p)}", which drops the I factor and the effective o(p). It now
   says "the exponent p/2+O(1) of κ … cannot be improved to o(p), in the
   sense a(p) ≤ p/ψ(p) above, on integer instances".
10. **§10.7 summary.** "a fixed growth constant" was wrong, because the
    constant depends on r and hence on k. The text now says "∇²F ⪰ −2I and a
    growth constant that depends only on k". I also fixed the plurals:
    "order-k relaxations have feasible points".
11. **Prop. `prop:oraclebarrier` proof.** The query count q was renamed to Q,
    because q is reserved for the accuracy 2^{−q}. Q also matches Prop.
    `lim:prop:oracle`.
12. **appendix-lbproduct.tex.**
    - The running sums z^{cd}_l clashed with the point z, z*, ẑ in the same
      proof. They are now y'^{cd}_l.
    - n_v is now n (CONVENTIONS: n is the number of variables).
    - N in "f(k)N^{o(k)}" is now N_0 (F183: N is the number of bags), and the
      text states that the Clique-to-multicolored-clique instance has
      classes of size N_0.
    - In the "in particular" proof, C is first made a positive integer, so
      that ψ' is computable and nondecreasing.
13. **appendix-moments.tex, Remark `lim:rem:moments`.** The Gram vectors
    φ_1, φ_2 clashed with the function φ in Prop. `lim:prop:moments`. They
    are now χ_1, χ_2.
14. **"Elimination of the states"** (proof of `lim:prop:unique`) is now
    "Elimination of y", because "states" is reserved for other uses.

No labels were deleted or renamed. No new citations are needed.

### Checks run (targeted)

- `python3 process/w3/checks/limits-setgrowth.py`,
  `limits-reductions.py` and `limits-moments.py` (the revising agent's
  scripts): all PASS.
- `python3 process/w3/checks/limits-verify-setgrowth.py` (new, independent,
  exact Fractions): PASS. It checks:
  - (a) by brute force on 150 random grids of X (n = 2..4) with
    L = (2,4,…,4,2);
  - (c) on 150 random path certificates with k = 0 or 1 and the largest
    valid β (n = 2, 3), where every removed stage-0 interval has length at
    most 2√ε;
  - the n = 2, ε = 1/50 example;
  - (1+log₂κ)² ≤ 4κ on [1, 2^40], and κ_S ≤ 2n(n−1).
- An inline exact check of Remark `lim:rem:moments`: the identity
  F_h − 1/4 = 16δ² + 2[…] + (u_1+u_2+v)/16, the growth constant g = 1/22 and
  the distance bound, at 2000 random rational points. PASS.
- `latexmk -pdf -interaction=nonstopmode -outdir=build/limits-verify
  main.tex` in the paper directory. The first run, before my edits, exited
  12 because bibtex read the shared `main.aux` in the paper root. The final
  run exited 0, with no LaTeX errors and no overfull boxes.
- The same command on an isolated snapshot (`/tmp/lvcopy`) exited 0, with no
  errors, no undefined references or citations, no multiply defined labels
  and no overfull boxes.

No project-wide verification was run, and CI was not consulted.

### Remaining

- It is open whether every valid path certificate for the set-growth family
  needs ε^{−Ω(1)} nodes in total. The paper states this.
- I did not re-check these against the primary sources:
  - Del Pia–Khajavirad construction details in Remark `lim:rem:dk` (R4 and
    R7 verified them);
  - the Bienstock–Muñoz locator "Appendix A";
  - Cygan et al. Theorem 14.21;
  - the claim that the proof of that theorem composes only deterministic
    reductions. This is standard, and R4 agrees.
- Cosmetic: the remark in app:dk names DK points y, y′, and the lbproduct
  proof now uses y′ for running sums. These are separate subsections, so I
  left them.

## Verification, second pass (verifier for group `limits`)

I re-checked the three files independently after the first verification pass
above. Files edited: `sections/limits.tex`, `sections/appendix-lbproduct.tex`,
`sections/appendix-moments.tex`. No other file was edited. New check script:
`process/w3/checks/limits-verify-misc.py`.

### What was checked

- **Adjudications.** I checked all 33 findings in `assign/limits.json`
  against the diff from `sections-before-w3/` and the full R4 report.
  - Every ACCEPTED fix is present and correct.
  - The MODIFIED and REJECTED decisions are justified:
    - F0 and F36: the abstract and introduction are not in these files.
    - F186: per-point occupied widths need no extra hypothesis.
    - F53, my part: the proposed wording would restate the claim that F178
      shows to be false, and `rem:grading` already uses the restricted
      wording.
    - F90: V(v) is the right symbol, because m_i is reserved for grid
      min-marginals.
- **Mathematics.** I re-derived the following line by line:
  - Prop. `lim:prop:unique`, Cor. `lim:cor:nopolylog` and the padding
    argument (κ is unchanged because L ≥ 2 and g ≤ 1);
  - Prop. `lim:prop:oracle`: the t_c argument and the first-Q argument;
  - Remark `lim:rem:oracle`;
  - Prop. `prop:lbwidth`: decoding, Ψ_0 with g = 1/n, and κ̄ = 2 in the
    weighted norm;
  - the SETH and L = 0 paragraphs;
  - Prop. `prop:lbproduct` and its appendix proof:
    - isolation with the union bound;
    - encoding, the variable count and the Hessian diagonal;
    - the reduction;
    - the reduction from Clique to multicolored clique;
    - one-sided error, which does not accumulate over the sparsified
      instances;
    - the ψ′ argument for the effective o(p);
    - (1+log₂κ)² ≤ 4κ;
  - Prop. `lim:prop:messages`;
  - Prop. `lim:prop:setgrowth` (a), (b) and (c), and the n = 2, ε = 1/50
    example, against Def. `def:filter`, Def. `def:cert` (both alternatives of
    (C1)) and TRIAL;
  - Prop. `prop:oraclebarrier`;
  - Prop. `lim:prop:constraints` and the TU paragraph, against Def.
    `def:tu-model` and the discussion after Thm `thm:tu-approx`;
  - the algebra of Remark `lim:rem:dk`;
  - Lemma `lim:lem:mixture`, Def. `lim:def:moments`, Prop.
    `lim:prop:moments` and Remark `lim:rem:moments`.
- **Cross-file facts used here.** I checked them against their sources:
  - the formula for f(p,κ) in Thm `thm:approx`;
  - the cap in Lemma `lem:states`;
  - the bound on f_1 in the proof of Thm `thm:exact`;
  - Defs. `def:curvature` and `def:growth`;
  - the summary of Prop. `prop:star`;
  - the statements that cite this section: intro Thm `thm:intro-lower` and
    the results table, Remark `rem:fpt`, Remark `rem:grading`, the
    conclusion, computation.tex, and growth.tex and appendix-growth.tex for
    `lim:prop:messages`.

  All are consistent with the current statements.
- **References.** All 57 labels referenced from the three files exist, and
  all 15 citation keys are in `references.bib`.
- **Earlier requests.** computation.tex uses Ψ_m and ξ_m (text and
  caption) and the restricted set-growth sentence. appendix.tex inputs
  lbproduct before moments.

### Problems found and fixed in this pass

1. **Paragraph after Cor. `lim:cor:nopolylog`.** The text justified "f(p,κ)
   is polynomial in κ for fixed p" indirectly, through the cap and bit
   lengths with an appendix pointer. It now states the formula
   f(p,κ) = c_0(c_1p√κ)^pκ(1+log₂κ)² of Thm `thm:approx`, from which this is
   immediate.
2. **Prop. `prop:oraclebarrier`.** It used k for the number of variables,
   while the adjacent Prop. `lim:prop:setgrowth` uses k for the number of
   certificate stages (Def. `def:cert`), and CONVENTIONS reserve n for the
   number of variables. I changed k to n in the statement, proof, following
   paragraph and opening bullet ("in n variables", "n = p = 1"). Euclidean
   norms are now `\norm{x-c}` instead of `\abs{x-c}`, as elsewhere in the
   paper.
3. **Prop. `lim:prop:messages`.**
   - The quadratic pieces q_l clashed with the accuracy exponent q in the
     same proposition. They are now φ_l.
   - The shift operator J clashed with J for grid intervals. It is now
     described without a letter.
   - P_z clashed with P = {i: L_i>0}. It is now Σ_t e_{z_t}e_{z_t}ᵀ, as in
     Remark `lim:rem:moments`.
   - "On the interval" (ambiguous next to the pieces) now reads "on
     [0,2^m−1]".
4. **CONVENTIONS §2.** "CT (Algorithm `alg:ct`)" now appears at the first use
   in Section 10 (§10.2 lead-in). The reference was removed from Remark
   `lim:rem:oracle`.
5. **Repetition.** "Their minimizers need not be unique" appeared three
   times: in the section opening, in the paragraph before §10.2 and in
   Remark `lim:rem:dk`. I removed the last two. The remark now opens with
   the construction.
6. **appendix-moments.tex.**
   - The constant term c of F clashed with the vector c of residual offsets
     in the proof of Prop. `lim:prop:moments`. The constant term is now F(0),
     as in constraints.tex.
   - The summation ranges in F_{r,h} are explicit: ρ′_j for j ≤ r, and v_j
     for j ≤ r−1.
7. **appendix-lbproduct.tex.** "That proof composes …" had an unclear
   antecedent. It now reads "The proof of this lower bound composes …".
8. **Spelling.** "toward" is now "towards", as elsewhere in the section.

No labels were deleted or renamed. No new citations or BibTeX entries are
needed. No requests to other files.

### Checks run (targeted)

- `python3 process/w3/checks/limits-verify-misc.py` (new, exact Fractions
  and sympy): PASS. It checks:
  - Prop. `lim:prop:messages`:
    - part 2 at random rational points and at exact binary chains, m = 2..7;
    - the Hessian diagonal 10, 4 and 7/4;
    - ∇²Ψ_m + ¼Σe_{z_t}e_{z_t}ᵀ ⪰ 0, by an exact PSD test.
  - Prop. `prop:oraclebarrier`:
    - the derivative formulas (symbolic, n = 1..3);
    - 1−(1−ρ)³−ρ = ρ(1−ρ)(2−ρ);
    - ∂_ii f ≤ 1;
    - the subcube count M^n > Q+1 and M < 1/(2√(6ε)).
  - Prop. `prop:lbwidth`, exhaustively for all 75 graphs with n ≤ 4:
    - unique binary minimizer, and x* ≠ 0;
    - ⌊Ψ̃/2^n⌋ = −α for Ψ̃ within 1/2;
    - growth 1/(2n) for Ψ and 1/n for Ψ_0;
    - the weighted bound with κ̄ = 2.
  - The padding claim: κ is unchanged.
- `limits-setgrowth.py`, `limits-reductions.py`, `limits-moments.py` and
  `limits-verify-setgrowth.py`, rerun: all PASS.
- `latexmk -pdf -interaction=nonstopmode -outdir=build/limits-verify
  main.tex` in the paper directory: exit 12.
  - The cause is outside these files: latexmk runs bibtex on the shared
    `main.aux`/`main.bbl` in the paper root, which concurrent builds
    rewrite. The second run stopped with "Maximum runs of pdflatex reached".
  - The pdflatex log in `build/limits-verify` has no LaTeX errors and no
    overfull boxes.
- The same command without `-outdir`, on an isolated snapshot of the current
  sources (`/tmp/lv2copy`), exited 0. I then read the rendered Section 10 and
  Appendix G with pdftotext. The log has:
  - no errors;
  - no undefined references or citations;
  - no multiply defined labels;
  - no overfull boxes;
  - no other warnings.

No project-wide verification was run, and CI was not consulted.

### Remaining

- It is open whether every valid path certificate for the set-growth family
  needs ε^{−Ω(1)} nodes in total. The paper states this.
- I did not check these against primary sources:
  - the Del Pia–Khajavirad construction details in Remark `lim:rem:dk` (R4
    and R7 did);
  - the Bienstock–Muñoz locator "Appendix A";
  - Cygan et al. Theorem 14.21.
- Local symbols that I left in place:
  - In Appendix `app:moments`, s is the separator state variable, although
    s is reserved for the largest box width. It is defined explicitly, and
    no width appears there.
  - ℓ and D in Remark `lim:rem:dk` are marked as Del Pia–Khajavirad's
    notation.
