# W3 report: optsets (sections/optsets.tex, sections/appendix-proximal.tex)

Files edited: `sections/optsets.tex` (Section 9) and `sections/appendix-proximal.tex`
(appendix `app:proximal`). No other file was touched. Check scripts:
`process/w3/checks/optsets-twocenters.py` and `process/w3/checks/optsets-prox.py`.

## Summary of the main changes

- **Prop `prop:twocenters`** restated as R3 proposed, with re-derived constants.
  - `G_z` is any finite set containing {0, M}. TRIAL and CT use `G_z = {0,M}` because `L_z = 0`.
  - (a) Bound (9.1) and the gap bound hold at every stage of TRIAL/CT. Stage 0 (`M <= h_x0 < 2M`, center `l`, `G_x = {0,M}`, `beta <= -M^2/4`) is now covered, and so is CT with a common mesh.
  - (b) A stage with `beta >= -eps` has more than `M/(48 sqrt eps)` x-nodes and more than `M/(24 sqrt eps)` table entries.
  - (c) EX builds more than `M/24` entries, which is `2^{Omega(I)}`.
  - "FG" is gone.
- **UC** is now Algorithm `alg:uc`.
  - The symbol Δ in step (i) was the correction sum; it is now `D`. The effective width is `w(.)`, as in Section 4.
  - The UC mesh points `Lambda_ij` were renamed `\mathcal G_ij`, because Λ is the multiplier in 9.3.
  - Lemma `lem:cells` now cites Prop `prop:cellwise`(b),(c) in the families-of-intervals form that the core agent added. The duplicated randomized-rounding proof was removed.
  - Thm `thm:cells` uses `O(p(|A|+n+N)K_S^p)`.
- **Section 9 intro.** The local set-growth definition was deleted; the section uses Def `def:growth`(c), `g_S` and `kappa_S = kappa(L,g_S)`. The claims were rewritten: `O(r sqrt(n kappa_S))` nodes per coordinate; "an exact optimizer and an exact description of S are found in time `f'(p,kappa_S)poly(I)`".
- **Remark `rem:np`** was deleted here. The exact agent placed it in Section 6 under the same label.
- **Remark `rem:grading`.**
  - Open: whether exact output admits an `f'(p,kappa_S,r)poly(I)` bound when the optimal set is finite.
  - Settled for a continuum: `lim:prop:setgrowth` (revised by limits) shows that runs of filtering with `U_j >= OPT`, in particular TRIAL and CT, can need `1+1/(2 sqrt eps)` nodes per coordinate.
  - Still open: whether other certificates avoid this.
- **Section 9.2.**
  - Notation: `l_i` → `\ell_i`, `S` → `\mathcal S`.
  - Renames, to free reserved or clashing symbols:
    - face pattern σ → χ, and pattern τ → χ (τ is the REC threshold);
    - `\mathcal P_i` → `\Sigma_i`;
    - bag relations `\mathcal A_t` → `\mathrm{Adm}_t`;
    - `\bar F(σ)` → `face(χ)`, because `\bar F` read as the objective;
    - `φ_t` → `q_t`, the bag factor sum as in Section 4.
  - The attribution paragraph (old lines 440–446) was replaced per R7 M2 and CONVENTIONS §5:
    - Rosenberg 1972, noting that this is Cor `cor:facecsp`(ii) when `H_ii = 0`;
    - Del Pia–Khajavirad;
    - Dechter;
    - Wainwright–Jaakkola–Willsky 2005 and Werner 2007.
  - The paragraph states the new part: the tree-structured pattern problem and its `2^{O(p)}` computations.
- **Section 9.3.**
  - It now states its hypotheses explicitly: continuous box, rational quadratic.
  - `kappa` → `kappa_S`, `g` → `g_S`, guess `K` → `\hat\kappa`, class `\mathcal C` → `\mathfrak D`, dual `ψ` → `Ψ`, `P(y)` → `Q_η(y)`.
  - New algorithm environments: PROX (`alg:prox`) and DISC (`alg:disc`).
  - Lemma `lem:proximal` is now stated in the main text before the theorem; its proof is in the appendix.
  - Thm `thm:diagdiscovery` is stated for DISC:
    - (a) adds "DISC does not stop if `F ∉ 𝔇`". This is proved: acceptance implies `F ∈ 𝔇`.
    - (b) is stated for every set-growth constant.
    - (c) begins "Under the hypotheses of (b)" and says that `f'` is polynomial in `kappa_S` for fixed `p`.
  - `C_0` was replaced by the explicit table bound `2(48p sqrt(κ̂))^p(n+2) <= 2(68p sqrt(kappa_S))^p(n+2)`.
  - Prop `prop:sshard`:
    - Both consequences are under "unless P=NP".
    - (ii) is quantified precisely over set-growth constants.
    - Partial sums σ → ξ.
    - New attribution: the objective is the Subset Sum reduction of DPK Remark 2 with unscaled partial sums. What is added is that its feasible instances lie in 𝔇.
- **Appendix `app:proximal`**, retitled "The diagonal certificate and the proximal stage".
  - It now holds the proofs of `lem:diagcert`, `lem:proximal`, `thm:diagdiscovery` and `prop:sshard`, plus `rem:falseguess`. Per R9, these proofs were moved out of the main text.
  - The integer-coordinate cases were dropped, since 9.3 is continuous-only.
  - `K_theta = 8 theta^{-1} ceil(log2(n+2))`, proved directly from Lemma `lem:graded`(b).
  - Lemma `lem:proximal`(ii) is now proved by Prop `prop:cellwise`(a) applied to `F + η||·−c||^2` (curvatures `L_i + 2η`). The constant `99/64` is unchanged.
  - Bit lengths are `O(I+j+μK_θ)`, with denominators via the Section-6 `Δ`.
  - The tie statement in `rem:falseguess` is fixed.

## (1) Adjudication

| id | verdict | reason | change |
|---|---|---|---|
| F4 | MODIFIED (my part) | The claim omitted `kappa_S` and `r`. The intro belongs to front. | Section 9 intro: "unions of uniform cells give grids with `O(r sqrt(n kappa_S))` nodes per coordinate, where `r` is the largest number of optimal values of one coordinate". Front's intro already says this (checked). |
| F7 | ACCEPTED (my part) | "FG" was undefined. | FG replaced by the CONVENTIONS names TRIAL (`alg:trial`) and CT, rather than Rewrite 13's "Algorithm 1", which CONVENTIONS forbids. recourse-balanced is not mine. |
| F8 | ACCEPTED (my part) | rem:np belongs to Section 6. | rem:np deleted from optsets.tex. The exact agent placed it at the end of 6.3 (label present in exact.tex). The other parts belong to exact. |
| F13 | ACCEPTED (my part) | Unstable names. | No FG. TRIAL, CT, "CT with a common mesh", EX, REC are cited by label. UC, PROX and DISC are algorithm environments. App E says "graded grid" (was "outward geometric grid"). Terminology: "nodes per coordinate", "table entries". |
| F14 | ACCEPTED | The theorem used a procedure defined only in the appendix; `C_0` was undefined. | PROX (`alg:prox`) is defined and Lemma `lem:proximal` stated before the theorem. DISC (`alg:disc`) makes the theorem statement short. `C_0` is replaced by the explicit bound `K_theta^p <= 2(48p sqrt(κ̂))^p(n+2) <= 2(68p sqrt(kappa_S))^p(n+2)`. |
| F25 | ACCEPTED (my part) | Untitled remark. | `rem:shor` is titled "The diagonal certificate class". |
| F27 | ACCEPTED (my part) | Idiom. | "Other methods solve this instance easily; it shows that the failure comes from the single center, not from conditioning." |
| F29 | ACCEPTED (my part) | sshard's last clause also needs P≠NP. | "Consequently, unless P=NP: (i) …; (ii) there is no polynomial π such that every instance of this form in 𝔇 has a set-growth constant with `kappa_S <= π(I)`." Other slips are not mine. |
| F34 | ACCEPTED (my part) | Overfull eq. (9.6). | `eq:diagid` is split over two lines. Two small overfull lines introduced while editing (twocenters (a), lemma head) were also removed. My files now have no overfull or underfull boxes. |
| F35 | MODIFIED (my part) | The paper stays one paper (CONVENTIONS). | Proofs of `lem:diagcert`, `lem:proximal`, `thm:diagdiscovery` and `prop:sshard` moved to App `app:proximal`. Algorithm boxes UC, PROX, DISC added. The rest is not mine. |
| F42 | ACCEPTED (b) | FG undefined. | Replaced by TRIAL/CT (CONVENTIONS names). (a), (c), (d) are not mine. |
| F43 | ACCEPTED (§9.2 part) | Attribution missing at the point of use. | New attribution paragraph after `rem:endpointext` (see F135). §7.3 and intro are not mine. |
| F49 | ACCEPTED (my parts) | Local slips. | (a) "graded grid" in App E; (b) κ_S in Thm `thm:diagdiscovery`; (c) "unless P=NP" in sshard. (d), (e) and the figures are not mine. |
| F53 | MODIFIED | R5's wording ("no corrected-grid certificate has accuracy-independent grid size") is false after F178: R4's n=2 certificate has a 2-node last grid. | `rem:grading`: open for finite 𝒮; for a continuum, `lim:prop:setgrowth` shows that runs of filtering with `U_j >= OPT`, in particular TRIAL and CT, can need `1+1/(2 sqrt eps)` nodes per coordinate; other certificates are open. Matches limits' revised (b). |
| F55 | ACCEPTED (my part) | `kappa` was point growth, but 9.3 has set growth; the continuous hypothesis was implicit. | `kappa` → `kappa_S`, `g` → `g_S` in 9.3 and App E. "In this subsection X is a continuous box" opens 9.3 and is repeated in Lemma `lem:diagcert` and Thm `thm:diagdiscovery`. Intro and Prop 10.10 belong to front and limits; both now use `kappa_S` (checked). |
| F58 | ACCEPTED (my part) | Overloaded P. | `P(y)` → `Q_eta(y)` (CONVENTIONS). Pattern sets `\mathcal P_i` → `\Sigma_i`. |
| F59 | ACCEPTED (my part) | S vs 𝒮. | 𝒮 throughout; `\pi_i(S)` → `\mathcal S_i`, defined in Section 3; sshard partial sums σ → ξ. |
| F63 | ACCEPTED (my part) | Δ meant two things in UC. | Step (i)'s "Δ" was the correction sum and is now `D`. The effective width is `w(·)` (Section 4). The remaining Δ is the Section-6 denominator, with an explicit pointer to `sec:exact-data`. The proximal box `B` → `X'`. |
| F65 | ACCEPTED (my part) | FG undefined; hand-numbered algorithms. | As F13. New labels `alg:uc`, `alg:prox`, `alg:disc`. |
| F66 | ACCEPTED | The theorem pointed to the appendix; τ was implicit. | PROX and `lem:proximal` stated before the theorem. DISC says "(τ as in REC, Algorithm~\ref{alg:rec})". |
| F68 | ACCEPTED (my part) | Lemma 9.2 re-proved the rounding bound. | Core's Prop `prop:cellwise` now covers families of intervals. The proof of `lem:cells` cites (b),(c) in that form, followed by the filtering induction. The proximal proof cites Prop `prop:cellwise`(a) instead of re-proving the rounding inequality. The rest is not mine. |
| F70 | ACCEPTED (my part) | Set growth was defined several times. | Local definition and `\label{eq:setgrowth}` deleted from optsets.tex; Section 9 cites Def `def:growth`, which now carries `eq:setgrowth`. |
| F72 | ACCEPTED (my part) | `l_i` vs `ell_i`. | `\ell_i` everywhere in my files. |
| F84 | ACCEPTED (my part) | `f` reused. | `f'` ("a computable function f'") in Section 9 intro, Thm `thm:diagdiscovery` and `rem:grading`. `f(p, κ̄)` appears only as a reference to Thm `thm:approx`. |
| F85 | ACCEPTED | The `n` term was missing. | Thm `thm:cells` and Lemma `lem:proximal`(iv) state `O(p(|A|+n+N)K^p)`, as in Lemma `lem:dp`. |
| F86 | ACCEPTED | Stage 0 was not covered by `h <= M`. | Prop `prop:twocenters`(a) treats stage 0 separately: `M <= h_x0 < 2M`, center `l`, so `G_x = {0,M}`, `beta <= -M^2/4 <= -max{θ²M²/379, h_x0²/20}` (since `h_x0²/20 < M²/5`). So "every stage" is proved. |
| F95 | ACCEPTED (strengthened) | Correct: `G_z = {0,M}` in TRIAL/CT, so the old quadratic table bound was false. | Restated as described in the summary. Proof: "TRIAL never filters z (`L_z=0`) and uses `G_z={0,M}`". In (b) the hypothesis is `beta >= -eps` (implied by `U-beta <= eps`). In (c), EX's test gives `F(x̃)-beta < 1/(ΩW) <= 1` and `F(x̃) >= 0`, so `beta > -1`. Exact checks pass (see §5). |
| F98 | ACCEPTED | The tie was confirmed. | `rem:falseguess`: origin at all stages `j <= 33` for κ̂ ∈ {1,2}. For κ̂ = 4, (0,0) and (1,1) both minimize `Q_eta` at stages 0 and 1, and the origin is returned at all `j <= 33` when ties are broken towards the current center. Also states `kappa_S >= 256` for this instance. Re-verified exactly. |
| F100 | ACCEPTED | — | `kappa_S`. Thm (c) begins "Under the hypotheses of (b),". sshard (ii) is under "unless P=NP", with the quantifier made precise because `kappa_S` depends on the chosen `g_S`. |
| F101 | MODIFIED | Same issue as F53. | Same fix as F53, with wording aligned to limits' revised Prop (b). |
| F102 | MODIFIED | The citation was imprecise. Citing lem:cells's proof would not work: that proof now has no rounding argument. | The proof of Lemma `lem:proximal`(ii) applies Prop `prop:cellwise`(a) to `F~ = F + η||·−c||²` (upper coordinate curvatures `L_i + 2η`) on a cell chosen on the center side, so `w(J_i) <= h + θ|s*_i − c_i|`. It is deterministic and gives the same bound `OPT + η[(1+θ²/2)δ² + nh²/2]`, hence the same 99/64. |
| F103 | MODIFIED | The factor 10 was unexplained. A direct count is tighter. | Lemma `lem:graded`(b) gives `|G_i| <= 3 + (8/θ)ln(n+2) <= 7θ^{-1}ceil(log2(n+2))`, and `K_theta = 8θ^{-1}ceil(log2(n+2))` (the same cap as CT with a common mesh). The table bound is `(48p sqrt(κ̂))^p`-type, replacing `(600 sqrt K)^p (C_0 p)^p`. |
| F105 | ACCEPTED (my part) | Overstated output. | Section 9 intro: "an exact optimizer and an exact description of 𝒮 are found in time `f'(p,kappa_S)poly(I)`". Intro belongs to front (already similar; see request 1). |
| F106 | ACCEPTED (my part) | Same as F4. | Section 9 intro as in F4. The exact.tex/intro parts are not mine. |
| F108 | MODIFIED (my part) | Clashes are real. The proximal weight keeps the name η because CONVENTIONS fixes `Q_\eta`; η has no other meaning in Section 9 or App E. | Renames in my files: guess `K` → κ̂; x-node count `K` → `k` and `D_k` → `δ_m`; `E=||s*−c||²` → `δ²`; `ω_0` → Δ (Section 6); face pattern σ and pattern τ → χ; partial sums σ_i → ξ_i; ψ (dual) → Ψ; `\mathcal A_t` → `\mathrm{Adm}_t`; class 𝒞 → 𝔇; UC `Λ_ij` → `\mathcal G_ij`; `\ell_i` and 𝒮 throughout. TU parts are not mine. |
| F109 | ACCEPTED (my part) | Local items. | `U_j` → "the threshold U used at stage j". Segment range `0<=v<=1` added. (9.6) split. App E says "graded grid". Integer cases dropped from App E (Section 9.3 is continuous). The conclusion item is not mine. |
| F135 | ACCEPTED (wording adapted) | Rosenberg's criterion is Cor `cor:facecsp`(ii) for multilinear objectives. | Old lines 440–446 replaced. The paragraph names Rosenberg (with the exact correspondence to Cor `cor:facecsp`(ii) when `H_ii=0`), DPK, Dechter, WJW 2005 and Werner 2007. It says Thm `thm:endpointset` combines these facts and extends them to strictly concave coordinates and mixed boxes. "The new part is the factored form on the decomposition: Cor `cor:facecsp` turns the optimal set into a tree-structured pattern problem, which gives uniqueness, dimension, counts, distances and linear optimization over 𝒮 with `2^{O(p)}` operations per bag." Abstract/intro belong to front (done there). |

Further corrections not tied to a finding:

- Prop `prop:sshard` now credits `\cite[Remark~2]{DelPiaKhajavirad2026}`. It is the same objective with unscaled partial sums (cf. R7's check of DPK Remark 2).
- Thm `thm:diagdiscovery`(a) is sharpened: outside 𝔇, DISC never stops. The old text said "may run forever".
- Lemma `lem:proximal`(iv) bit length is now `O(I+j+μK_θ)`; the old bound was `poly(...)`.

## (2) Labels deleted, renamed or moved

- **Deleted:** none.
- **Removed from my files, but alive elsewhere with the same label** (no reference changes needed):
  - `rem:np` is now in exact.tex (end of 6.3), placed by the exact agent;
  - `eq:setgrowth` is now in setting.tex, Def `def:growth`(c), placed by core.
- **New labels:**
  - `alg:uc`: Algorithm UC (unions of uniform cells), Section 9.1. growth-sharp.tex and computation.tex already cite it.
  - `alg:prox`: Algorithm PROX (proximal stages with guess κ̂), Section 9.3.
  - `alg:disc`: Algorithm DISC (discovery under unknown growth: guesses κ̂ = 1, 2, 4, …, PROX, REC, diagonal test), Section 9.3.
- **Moved:**
  - `lem:proximal` is now stated in Section 9.3; its proof is in App `app:proximal`. Label unchanged.
  - The proofs of `lem:diagcert`, `thm:diagdiscovery` and `prop:sshard` moved to App `app:proximal`. Labels unchanged.
- **Unchanged and kept:** `sec:optsets`, `sec:exact-nonunique`, `prop:twocenters`, `eq:twocenters`, `lem:cells`, `thm:cells`, `eq:cellcount`, `rem:grading`, `sec:endpointset`, `lem:endpointid`, `eq:endpointid`, `thm:endpointset`, `cor:facecsp`, `rem:endpointext`, `sec:diagcert`, `lem:diagcert`, `eq:diagid`, `eq:diagset`, `rem:shor`, `thm:diagdiscovery`, `prop:sshard`, `app:proximal`, `rem:falseguess`.

## (3) Requests for other files

1. **front (intro.tex, Several-minimizers paragraph).** It currently says "found in $f(p,\kappa_S)\poly(I)$ bit operations". Per F84 and for consistency with Thm `thm:diagdiscovery`, write "found in $f'(p,\kappa_S)\poly(I)$ bit operations for a computable function $f'$". If the result table has a row for `thm:diagdiscovery`, use the same form there.
2. **front (related.tex 169–172).** The Rosenberg/WJW/Werner comparison now lives in Section 9.2 (CONVENTIONS: one place). Either keep related.tex as is or shorten it to "Section~\ref{sec:endpointset} relates the optimal-set description to Rosenberg's face criterion and to tree reparameterizations \cite{Rosenberg1972,WainwrightJaakkolaWillsky2005,Werner2007}."
3. **limits (limits.tex, sentence after Prop `lim:prop:setgrowth`).** "For finitely many optimal values per coordinate, unions of retained cells restore a bound (Theorem~\ref{thm:cells})." → "For finitely many optimal values per coordinate, unions of uniform cells give grids with $O(r\sqrt{n\kappa_S})$ nodes per coordinate (Theorem~\ref{thm:cells})."
4. **core / growth-sharp.tex 48–53.** The current text ("UC (Algorithm~\ref{alg:uc}) … at most $12(2\sqrt{n\kappa}+1)$ nodes per coordinate … (Theorem~\ref{thm:cells} with a single minimizer)") is correct. With `r=1`, `K_S = 12(2 sqrt(n kappa)+1)` and `kappa_S = kappa`. No change needed.
5. **computation (computation.tex).** No action needed. The "as Theorem~\ref{thm:cells} predicts" sentence that R8 flagged is gone, and line 44 cites UC (`alg:uc`), which now exists.
6. **coordinator (appendix.tex).**
   - CONVENTIONS orders `appendix-proximal.tex` as Appendix E. In the current build it prints as Appendix F, after appendix-tu.
   - Its new title is "The diagonal certificate and the proximal stage".
   - The input order should follow the section order: B (exact), C (recourse), D (tu), E (proximal), F (limits).
7. **exact (FYI, two dependencies).**
   - (a) Prop `prop:twocenters`(c) uses EX's acceptance test `F(x̃)−β < 1/(ΩW)` with `ΩW >= 1`.
   - (b) `rem:falseguess` says the 34 checked stages cover the DISC budgets. This uses `τ = 1/(4nR)` with `R = Δ ∏_{I_C^+} P_ii`, which gives budgets 28, 28, 29 ≤ 33 for that instance.
   - If either changes, please notify optsets.
8. **core (FYI).**
   - Prop `prop:twocenters`(a) uses `M <= h_{x0} < 2M`, which follows from `h_{ij} = η_j r_i` with `E` the least integer such that `2^E r_i >= s_i`.
   - Lemma `lem:cells` relies on the "Families of intervals" paragraph after Prop `prop:cellwise`.
   - The proximal proof relies on "the proof of Prop `prop:cellwise`(a) uses only Definition `def:curvature`" and on `eq:logabsorb`.
   - Please keep these.

## (4) New BibTeX entries

None. All keys used exist in references.bib: Rosenberg1972, WainwrightJaakkolaWillsky2005, Werner2007, Dechter1999, DelPiaKhajavirad2026, JeyakumarRubinovWu2006, LiWuQuan2015, QiuYildirim2024, GareyJohnson1979, GrotschelLovaszSchrijver1988.

## (5) Checks run (targeted; local only, no CI inspected)

- `cd process/w3/checks && python3 -B optsets-twocenters.py`: **ALL PASS**.
  - Growth: the minimum of `F_M/dist²` on a 41×41 rational sample, for M ∈ {1, 7/3, 16}, is 1/2 ≥ 1/20.
  - Bound (9.1) holds exactly on all 1372 combinations of M, θ, h, c_x tried, with `G_z={0,M}` and `d_z=0` (the worst case). The smallest ratio β/bound is 1.135.
  - Constants: `0.23²/20 > 1/379`, `(1/2−9/64)·16/25 = 23/100`, `sqrt20+sqrt379 = 23.94 < 24`, and the stage-0 and k=1 inequalities.
  - Exact runs of TRIAL/CT on `F_M` (every stage obeys (9.1); stage 0 has `G_x={0,M}` and `β<=−M²/4`; (b) holds at every stage with ε = −β):

    | M | ε | succeeds at | x-nodes | table entries |
    |---|---|---|---|---|
    | 64 | 1/4 | μ=6 | 47 (> 2.7) | 94 (> 5.3) |
    | 1024 | 1 | μ=10 | 713 (> 21.3) | 1426 (> 42.7) |
    | 4096 | 1/4 | μ=12 | 2841 (> 170.7) | 5682 (> 341.3) |

- `cd process/w3/checks && python3 -B optsets-prox.py`: **ALL PASS**.
  - PROX constants: `θ^{-1} <= 6 sqrt(κ̂)`, `8κ̂θ² <= 1`, the 99/64 arithmetic, and the grid-count inequality `3/4 + 8ln(n+2) <= 7ceil(log2(n+2))` with `3/2 + sqrt(n/2) <= n+2` for n up to 10^5. Also `48 sqrt2 < 68`.
  - Lemma `lem:proximal`(i),(iii) checked exactly for 13 stages on three instances: a separable QP (κ_S=2), `(x−y)²` (segment optimal set, κ_S=1) and `F_4` from prop:twocenters (κ_S ≤ 40), with κ̂ ∈ {κ_S, 2κ_S}. All distance bounds and node caps hold.
  - `rem:falseguess`: budgets J = 28, 28, 29. The origin is returned at stages 0..33 for κ̂ ∈ {1,2}, where the argmin is unique. For κ̂ = 4, ties occur at stages 0 and 1 (`Q_eta = −1/2` and `−1/8`, argmins (0,0) and (1,1)), and the origin is returned when ties are broken towards the center. The matrices (191/64, eigenvalue −1/64; 193/64, PD) are confirmed.
- `latexmk -pdf -interaction=nonstopmode -outdir=build/optsets main.tex`.
  - Final run: no LaTeX errors.
  - My files: no overfull or underfull boxes and no warnings from optsets.tex or appendix-proximal.tex. Every `\ref`, `\eqref` and `\cite` key in my files resolves (checked by grep against all labels and references.bib).
  - The only unresolved citation in the build is `HornJohnson2013` on page 23, which is not mine.
  - The first run failed with "File ended while scanning use of \@@BOOKMARK". It read a `./main.out` in the paper root that a concurrent build was rewriting. The rerun was clean.
- The PDF text of Section 9 and the appendix was read through after the build.

## (6) Unresolved / dependencies

- `rem:grading` depends on the limits agent's Prop `lim:prop:setgrowth`(b). The current text matches: "a run of filtering with thresholds U_j ≥ OPT, in particular every trial of TRIAL and hence CT".
- `lem:cells` depends on core's "Families of intervals" paragraph (present now). If core removes it, restore a short proof. The old randomized-rounding proof is in `process/w3/sections-before-w3/optsets.tex`, lines 150–168.
- The `rem:falseguess` budget statement depends on τ and R of Section 6 (see request 7).
- Algorithm names inside `rem:np` (now exact's) are not mine to check.

## Verification (optsets-verify)

Verifier for `sections/optsets.tex` and `sections/appendix-proximal.tex`.
I diffed both files against `process/w3/sections-before-w3/`, checked every
assigned finding, and re-derived every changed statement and proof.

### What was checked

- **Adjudications.** All 37 findings were checked against the current text.
  Each ACCEPTED fix is present and correct. The MODIFIED and REJECTED
  decisions are justified.
  - F53/F101: R5's wording would be false, because limits shows a valid path
    certificate whose last grid has two nodes. The text says what
    `lim:prop:setgrowth`(b) proves and leaves other certificates open,
    matching limits' "we do not know" sentence.
  - F102: the deterministic Prop `prop:cellwise`(a) argument applied to
    `F + eta||.-c||^2` is correct, and it gives the same 99/64.
  - F103: the cap `K_theta = 8 theta^{-1} ceil(log2(n+2))` is valid with
    slack.
  - F108: keeping `eta` for the proximal weight is required by CONVENTIONS
    (`Q_eta`). `eta` has no other meaning in 9.3 or App E.
  - Parts of findings that belong to other files were correctly left alone.
- **Re-derived line by line.**
  - **Prop `prop:twocenters`.**
    - Growth constant 1/20, the symmetry, and the k=1 and k>=2 cases (the
      `alpha'^2 >= alpha^2/5` split, the recursion, 23M/100,
      `0.23^2/20 > 1/379`).
    - Stage 0 of TRIAL: `h_{x0}` is the least power of two `>= M`, so
      `G_x = {0,M}`, `d_x(M) = M^2/4` and `h_{x0}^2/20 < M^2/5`.
    - Stages `j >= 1`: `h < M`. Common mesh: `h_j <= M`.
    - (b): steps `< 24 sqrt(eps)`, and `|G_z| = 2`.
    - (c): `Omega W >= 1` and `F(x~) >= 0`, so `beta > -1`.
  - **UC, Lemma `lem:cells`, Thm `thm:cells`.**
    - Nesting of the mesh points, including the integer ceiling identity.
    - Cell lengths, spacing `>= h_j/2`.
    - The families-of-intervals form of Prop `prop:cellwise` (present in
      grids.tex).
    - The gap bound, the count `3 * 2r(4 sqrt(n kappa_S)+2) = K_S`, and the
      exact-output bit count via `eps_S`.
  - **9.2.**
    - The renames (`chi`, `Sigma_i`, `Adm_t`, `face`, `q_t`).
    - `pi_t(v;x) > 0` iff `v` is in `cube(chi(x)_{B_t})`.
    - The new Rosenberg sentence: for `H_ii = 0`, a pattern is admissible
      iff all vertices of its face are optimal, so Cor (ii) is the
      union-of-optimal-faces statement.
  - **9.3 and App E.**
    - Lemma `lem:diagcert`(i)–(iii) and the `rem:shor` example.
    - PROX constants (`theta^{-1} <= 6 sqrt(khat)`).
    - Lemma `lem:proximal`:
      - (i) `|G_i| <= 7 theta^{-1} ceil(log2(n+2))`;
      - (ii) the full chain to 99/64;
      - (iii) the induction;
      - (iv) the denominators `Delta 2^{j+mu K_theta}`, the closed form of
        `t_k`, and the common denominator `8 * 4^mu Delta omega_j^2`.
    - Thm `thm:diagdiscovery`:
      - (a), including "does not stop outside 𝔇";
      - (b) budgets vs Lemma `lem:snap`;
      - (c) the guess count, `K_theta^p <= 2(48p sqrt(khat))^p(n+2)` via
        eq:logabsorb with n, and `48 sqrt 2 < 68`.
    - Prop `prop:sshard`: the path decomposition, `H + Lambda = H_sq`, and
      both reductions. DPK Remark 2 is the same objective with scaled
      partial sums (R7 table).
    - `rem:falseguess`: optimizer, `g_S <= 1/128`, `kappa_S >= 256`, the
      matrices, the ties, and the budgets.
- **Moved material.**
  - Every original label survives: `rem:np` is in exact.tex and
    `eq:setgrowth` in setting.tex.
  - `lem:proximal` moved from App E to 9.3, with its proof in App E.
  - The old randomized-rounding proof of `lem:cells` is replaced by a
    citation of the families form of Prop `prop:cellwise`, which covers it.
  - The old "terminates on 𝒞 by Luo–Sturm" remark is subsumed by Thm (b)
    via Remark `rem:setgrowth`.
  - Nothing proved was lost.
- **CONVENTIONS.**
  - Algorithm names TRIAL/CT/EX/REC/UC/PROX/DISC are cited by label at
    first use in Section 9.
  - Notation: `\ell_i`, `\mathcal S`, `\mathcal S_i`, `g_S`, `kappa_S`,
    `kappa(L,g_S)`, `w(J)`, `X'`, `Q_eta`, `\hat\kappa`, `f'`.
  - Terminology: "graded grid", "nodes per coordinate", "table entries".
  - Claim wording for unions of uniform cells and for the Rosenberg/WJW/Werner
    credit.
  - No FG, "the report", "Algorithm 1/2", "geometric", or filler phrases
    (grep).

### Fixes made by the verifier

1. **Section 9 intro.**
   - Problem: it said exactness costs "`poly(I)+log2(1/g_S)` bits", which can
     be negative for large `g_S` (for example if F is constant).
   - Fix: now `poly(I)+max{0,log2(1/g_S)}`, as in Remark `rem:setgrowth`.
2. **Prop `prop:twocenters`.** Added a pointer to Definition `def:graded` for
   "graded grid".
3. **Lemma `lem:diagcert`(ii).** It now says "If x̄ is a box KKT point and
   H+Λ(x̄) ⪰ 0". Λ(x̄) is defined only for box KKT points; the hypothesis was
   implicit.
4. **App E, proof of Thm `thm:diagdiscovery`.** DISC (`alg:disc`) and REC
   (`alg:rec`) are now cited by label at first use in the appendix.
   `rem:falseguess` likewise cites PROX (`alg:prox`).
5. **App E, proof of Prop `prop:sshard`.**
   - Problem: the reduction did not say why the hypothesis `|a_0| <= A` loses
     nothing.
   - Fix: added "also when restricted to targets with `|a_0| <= A`, because
     other targets have no solution".
6. **`rem:falseguess`.**
   - Problem: "These stages cover the budgets" was not checkable from the
     text.
   - Fix: now states Δ = 128 (least common denominator), R = 2^23,
     τ = 2^-26 and `J_khat = 28, 28, 29` for `khat = 1, 2, 4`.

### Checks run by the verifier (targeted, local; no CI inspected)

- `cd process/w3/checks && python3 -B optsets-verify-diag.py`: **ALL PASS**.
  Covers the `rem:shor` example and the `prop:sshard` instance
  `a=(3,-2,5)`, `a_0=3`: box KKT, `H+Lambda = H_sq ⪰ 0`.
- `python3 -B optsets-verify-falseguess.py`: **ALL PASS**.
  - Budgets 28/28/29.
  - The origin is returned at all stages `<= 33` for `khat = 1, 2, 4`.
  - Ties only for `khat = 4` at stages 0 and 1 (values −1/2 and −1/8).
  - Matrices 191/64 (eigenvalue −1/64) and 193/64 (positive definite).
  - Lemma `lem:proximal`(ii),(iii) bounds on 3 instances.
- `python3 -B optsets-verify-twocenters.py`: **ALL PASS**.
  - 3000 random rational parameter sets: min `(-beta)/bound = 1.061`.
  - Faithful TRIAL/CT runs, including the common mesh, at every stage:
    - (a) holds;
    - stage 0 has `G_x={0,M}`, `beta <= -M^2/4` and `M <= h_x0 < 2M`;
    - (b) holds with `eps=-beta`.
- New `python3 -B optsets-verify-caps.py`: **ALL PASS**.
  - The PROX node count of the worst-case unclipped graded grid is at most
    `7 theta^{-1} ceil(log2(n+2)) <= K_theta`.
    - Tested for 41 values of `khat` up to 2^20 and n up to 10^6.
    - The largest ratio nodes/`K_theta` is 0.14.
  - eq:logabsorb with n in place of `n_P`, for p <= 40.
  - `K_theta^p <= 2(48p sqrt(khat))^p(n+2)` and `48 sqrt2 = 67.88 < 68`.
  - The arithmetic of prop:twocenters.
- New `python3 -B optsets-verify-uc.py`: **ALL PASS**. Exact UC runs on two
  instances:
  - `F_8` (10 stages; at most 6 nodes, against `K_S = 453`);
  - a mixed instance `(x-z)^2+(z-1)(z-2)`, with x in [0,4] continuous and z
    in {0..3} integer. `S={(1,1),(2,2)}`, and `g_S = 3/5` is checked
    exactly on a 1/64 grid. 9 stages; at most 10 nodes, against
    `K_S = 199`.
  - At every stage: `beta_j <= OPT`, optimizers stay in `X_j`, every
    retained cell has an endpoint within `sqrt(n kappa_S) h_j` of `S_i`
    (the count step), and `U - beta_j <= nLh_j^2/2`; final gap `<= eps`.
- `latexmk -pdf -interaction=nonstopmode -outdir=build/optsets-verify main.tex`
  (run twice, after the fixes).
  - No LaTeX errors.
  - The log segments of optsets.tex (pp. 53–61) and appendix-proximal.tex
    contain no overfull or underfull boxes and no warnings.
  - No undefined references or citations in the whole log.
  - All `\ref`/`\eqref` targets and `\cite` keys in both files exist (grep
    against all section labels and references.bib).
  - latexmk exits 12 because its bibtex step reads a `main.aux` without
    `\bibdata`, apparently the one in the paper root rather than the outdir
    copy. This is an environment issue unrelated to these files; the PDF
    uses the existing `main.bbl`.
- The PDF text of Section 9 and Appendix "The diagonal certificate and the
  proximal stage" was read in full.

### Remaining items (for other owners)

- **front, intro.tex (organization paragraph, about line 383).** The appendix
  now holds the proofs for 9.3, not only the proximal stage. Suggested text:
  "the diagonal certificate and the proximal stage of
  Section~\ref{sec:diagcert} (Appendix~\ref{app:proximal})".
- **limits, limits.tex (about line 559).** Repeating optsets' request: change
  "unions of retained cells restore a bound (Theorem~\ref{thm:cells})" to
  "unions of uniform cells give grids with $O(r\sqrt{n\kappa_S})$ nodes per
  coordinate (Theorem~\ref{thm:cells})".
- **front, related.tex (about lines 210–215).** The Rosenberg/WJW/Werner
  comparison now also appears in 9.2, which conflicts with the CONVENTIONS
  one-place rule. optsets' shortening request stands.
- **coordinator, appendix.tex.** `appendix-proximal` still prints as
  Appendix F, after appendix-tu. CONVENTIONS lists it as E.
- **Dependencies, unchanged.**
  - `rem:falseguess` and the DISC budgets depend on τ and R in exact.tex.
  - `lem:cells` depends on core's "Families of intervals" paragraph.
  - `rem:grading` depends on `lim:prop:setgrowth`(b). All three are present
    and consistent now.
