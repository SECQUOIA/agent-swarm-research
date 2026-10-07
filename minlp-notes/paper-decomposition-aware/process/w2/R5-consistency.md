# R5: Global consistency review

Manuscript: "Decomposition-aware global optimization: certified coordinate
grids, conditional recourse, and structural limits".

Version reviewed: the sources in `sections/` as of 2026-10-03 01:20 EDT. The
sources changed while the review ran. Files added during the review
(`setting-growthcert.tex`, `growth-sharp.tex`, `exact-localized.tex`,
`appendix-localized.tex`) are included. A private copy compiled cleanly
(104 pages, no undefined or multiply defined references). Theorem numbers below
refer to that build. File line numbers refer to the current sources. Where a
line number may have drifted, the label is also given.

## Summary

All references resolve, and each section is locally careful. The main
problems come from assembling fragments that were written separately:

1. **Symbols are overloaded across sections and, worse, within sections.**
   `P`, `S`, `γ`, `K`, `R`, `Ω`, `τ`, `Δ`, `D`, `d_i`, `m_i`, `M`, `N`, `E`,
   `W`, `V`, `Q`, `ℓ`, `σ`, `θ`, `η` and `h_j` each have three or more
   meanings. Several collisions occur inside one section or one proof. For
   example, Section 8 uses `N` for the number of bags and for a kernel basis,
   and `K` for the grid-size bound and for a saddle matrix. Section 6 redefines
   `P` while calling an algorithm that uses `P={i:L_i>0}`. Lemma 3.3 uses `γ`
   for Euclidean growth immediately after Definition 3.2 defines `γ` as the
   weighted-growth constant. A notation table and renamings are proposed at the
   end of this report.
2. **The recourse section changes its basic notation in every subsection.** The
   retained set is `K`, then `ℛ`, then `𝒞`, and `ℛ` means "retained" in 7.3 but
   "recourse" in 7.4. Blocks are `y^{(t)}, E_t, r` in 7.1 and `y_t, S_t, T` in
   7.3. `φ_t` is a block objective in 7.1 and a value factor in 7.3. The value
   function is `V`, `W_B` or `W_𝒞`.
3. **Several summary claims do not match the theorems.** The TU claims in the
   abstract and introduction omit growth, finite projections and `W/η`. The
   conclusion says the dependence on `κ` "must be polynomial". The limits
   section attributes the `p`-exponent bound to ETH, although it needs rETH. The
   introduction states the diagonal-certificate discovery result with `κ`,
   although it needs `κ_S` and continuous variables. Remark 9.4 calls a question
   open that Proposition 10.9 answers. Open problem (1) in the conclusion
   misdescribes Theorem 7.18.
4. **Hypotheses change silently between sections.** There is weighted vs
   Euclidean growth, point vs set growth, and per-coordinate vs common meshes.
   The common-mesh, Euclidean-`κ` variant is used by Theorem F.4, Corollary
   6.19 and all experiments, but it is only asserted, never proved. Its
   constants appear in four places with different values. Set growth is defined
   three times with different symbols. "Point growth" is never defined.
5. **Material is duplicated.**
   - The exact-output machinery is developed twice in parallel (Section 6 and
     Section 8.6, including a verbatim copy of the acceptance proposition), and
     a third and fourth time in Theorems 7.18(iii) and 7.39.
   - Lemma 7.2 restates Lemma 7.1(a).
   - Lemma 9.2 re-proves Proposition 4.2.
   - Proposition 8.19 and Corollary 5.6 prove the same lower bound.
   - Example 5.11 restates Proposition 10.8.
6. **There are assembly artifacts.**
   - The Section 6 introduction describes content that has moved to Section
     9.1, and the rendered text says "Throughout Sections 6.1–9.1".
   - The algorithm name "FG" is undefined.
   - "the cut-based recourse of the report".
   - An undefined tag "(F)".
   - Section 7.5 is never referenced.
   - In Section 7.1 a bag-cell block sits between Lemma 7.1 and its discussion.

No finding is critical: no main theorem is false as intended. Finding M7
(negative `L_i` in Theorem 7.18) would make a bound invalid if read literally,
but the fix is one symbol.

## Checks run (targeted, local; not CI)

* `latexmk -pdf` on a private copy in `/tmp/r5build`: 104 pages, no undefined
  or multiply defined references. I used the `.aux` file to map labels to
  numbers and pages.
* A label scan found 70 labels that are never referenced. Relevant ones:
  `sec:cr-mixed`, `prop:cr-greedy`, `lem:cr-semiconcave`, `sec:localized`,
  `thm:cr-exact`, `thm:tu-exact`, `thm:cv-recog`.
* `process/w2/checks/r5_graded_misaligned.py` (exact `Fraction` arithmetic):
  - The graded grids after Proposition 8.20 (`h=1/16`, `θ=1/4`, centers
    `3/10` and `7/10`) have 11 nodes each, share only `0` and `1`, and satisfy
    `(eq:tu-gap)` with `m=1/2`. This is confirmed.
  - The grid `{0,1,9/4,3}` of Example 8.21 and its corrections
    `L/8, 25L/128, 25L/128, 9L/128` are confirmed.
* `experiments/results/S1_localized.csv`: 30 rows, 29 accepted, acceptance
  within at most 4 stages, at most 542 height-rule stages. This matches the
  text of Section 6.6 but not Section 11 (finding m6).

---

## Findings

Severity: **critical** means a false main claim or an invalid proof. **Major**
means a real gap, a wrong or misleading statement, or a serious
clarity/structure problem. **Minor** means a local error or wording problem.

### Major

**M1. The TU claims in the abstract and introduction omit the hypotheses of
Theorem 8.11.**

*Location:* `abstract.tex` 30–32; `intro.tex` 109–114; Theorem 8.11
(`thm:tu-approx`); Remark 8.22 (`rem:tu-hybrid`).

*Issue:* The abstract says TU coupling admits "exactly feasible correlated
rounding with polynomial complexity for fixed width". The introduction says
"the algorithm is polynomial for fixed width and conditioning … the uniform
meshes responsible for this are forced". Theorem 8.11 is polynomial only under
set growth with finite optimal coordinate projections (`|𝒮_i|≤r`) and
polynomially bounded `κ_c`, `W/η`, `d` and `r`. Without growth, the last-level
tables have size `(W√(n_c L̄/ε))^p`, which is polynomial in `1/ε`, not in
`log(1/ε)`. "Forced" overstates Propositions 8.20 and 8.21. They show only that
curvature-only corrections fail on misaligned grids, and Remark 8.22 says free
coordinates may use graded grids.

*Fix:*
- Abstract: "Totally unimodular coupling constraints with mesh-aligned data
  admit exactly feasible correlated rounding; under set growth with finitely
  many optimal values per coordinate the resulting algorithm is polynomial for
  fixed width when the conditioning and box widths are polynomially bounded,
  but it is not fixed-parameter tractable."
- Introduction: replace "are forced" with "cannot be replaced by graded grids
  when the correction depends only on curvature (Propositions 8.20–8.21)".

**M2. The conclusion misstates what the lower bounds show.**

*Location:* `conclusion.tex` 12–15 and 38–40; Remark 5.8 (`growth.tex`
237–239).

*Issue:* "the dependence on the condition number must be polynomial" is not
what Corollary 10.2 shows. Corollary 10.2 shows only that the dependence cannot
be polylogarithmic, unless P = NP. A quasi-polynomial dependence is not
excluded. These passages also drop all complexity assumptions: "neither
parameter can be dropped" (P≠NP or ETH) and "its exponent must grow" (rETH).

*Fix:* "…show that this parameterization is close to the right one: unless
P = NP neither parameter can be dropped and the dependence on the condition
number cannot be polylogarithmic; under the randomized exponential-time
hypothesis its exponent cannot be o(p)." Make the same change in Remark 5.8 and
in open problem (2).

**M3. The limits section misattributes the hypothesis of Proposition 10.7.**

*Location:* `limits.tex` 14–17 (opening bullet); `abstract.tex` 24–25;
`intro.tex` 129–131; Proposition 10.7 (`prop:lbproduct`).

*Issue:* The bullet says "under the exponential-time hypothesis … the exponent
of κ must grow linearly with p (Propositions 10.6 and 10.7)". Proposition 10.7
assumes **rETH**. Its conclusion is `a(p) ≠ o(p)`, which is weaker than "grows
linearly" because it allows constant exponents along a subsequence. The
reduction also uses integer instances. Section 10 itself lists the continuous
case as open, but the abstract and introduction do not say so.

*Fix:*
- Bullet: "under ETH the dependence on p is exponential even when κ≤2
  (Proposition 10.6); under randomized ETH the exponent of κ cannot be o(p),
  already for integer box quadratics (Proposition 10.7)."
- Abstract and introduction: replace "must grow linearly with p" with "cannot
  be o(p)".

**M4. Remark 9.4 calls a question open that Proposition 10.9 already
answers.**

*Location:* `optsets.tex` 229–231 (Remark 9.4, `rem:grading`); `limits.tex`
443–461 (Proposition 10.9).

*Issue:* Remark 9.4 says that "any accuracy-independent grid bound when S is a
continuum, is open". Proposition 10.9 proves that every corrected-grid
certificate of accuracy ε needs at least `1+1/(2√ε)` nodes per coordinate when
𝒮 is a continuum. The question is therefore already answered negatively for
the methods of this paper.

*Fix:* "Whether exact output admits an `f(p,κ_S,r)poly(I)` bound when 𝒮 is
finite is open; when 𝒮 is a continuum, Proposition 10.9 shows that no
corrected-grid certificate has an accuracy-independent grid size."

**M5. Open problem (1) in the conclusion misdescribes Theorem 7.18.**

*Location:* `conclusion.tex` 30–33.

*Issue:* "Theorem 7.18 answers this when the convex part can be eliminated with
certified responses whose pieces are small". Theorem 7.18 is parameterized by
the reduced curvature `L`, not by `ν`. Remark 7.26 shows that a single *small*
piece without cancellation destroys the certified curvature. The statement that
does give a `ν/g` bound is Corollary 7.21 (`L ≤ C_0 ν`).

*Fix:* "Corollary 7.21 answers this when the reduced curvature certified by
Theorem 7.18 satisfies `L ≤ C_0ν`; Proposition 7.25 shows that recourse alone
cannot ensure this, and Remark 7.26 that one uncancelled piece suffices to
lose it."

**M6. Section 9.3, Section 10.4 and the introduction use `κ` where `κ_S` (set
growth) is meant.**

*Location:*
- `intro.tex` 121–123.
- Theorem 9.12 (`optsets.tex` 550–555, 571–578).
- Proposition 9.13 (`optsets.tex` 606, 626).
- Remark after Theorem 9.12 (`optsets.tex` 587–589).
- Proposition 10.10 (`limits.tex` 502–503, 542).
- Lemma B.1 (`appendix-proximal.tex` 36).

*Issue:* Theorem 9.12(b) takes "g … any set-growth constant" and then writes
"K ≤ 2κ" and "f(p,κ)". By Definition 3.2, `κ` is the point-growth number, and
a finite point-growth `κ` forces a unique minimizer, which this section
explicitly does not assume. The introduction states the result with `κ` and
does not say that Section 9.3 assumes continuous variables. In the same
places, `g` is used for the set-growth constant that Section 9's own
definition calls `g_S`.

*Fix:*
- Replace `κ` by `κ_S=max{1,L/g_S}` and `g` by `g_S` throughout Section 9.3,
  Appendix B and Proposition 10.10.
- Introduction: "for continuous box quadratics certified by a diagonal
  Lagrangian multiplier, an unknown optimal set is found exactly in
  `f(p,κ_S)poly(I)` time, where `κ_S` uses growth towards the optimal set."

**M7. Theorem 7.18 treats possibly negative `L_i` as upper coordinate
curvatures.**

*Location:* `recourse-convex.tex` 341–342 (eq:cv-L) and 380 (proof of
Theorem 7.18(iii)); Proposition 7.24 proof 640–643.

*Issue:* Definition 3.1 requires `L_i ≥ 0`. In (eq:cv-L),
`L_i=(H_0)_ii−Σσ` can be negative. The paper's own ladder has
`L_{v_i} = −2+2η deg_i < 0`. The proof of (iii) still says "V has upper
coordinate curvatures L_i". With a negative `L_i`, the correction
`d_i = L_i w²/8` is negative, and Proposition 4.2 no longer gives a lower
bound, because its proof needs `φ ≤ F`.

*Fix:* Define `L_i^+ = max{L_i,0}` and write "(iii) By (i), V has upper
coordinate curvatures `L_i^+`; the corrected grids use `L_i^+`, and coordinates
with `L_i ≤ 0` use two endpoint labels (Section 5, `i∉P`)."

**M8. The common-mesh, Euclidean-`κ` variant is used by two results and all
experiments but is never proved.**

*Location:*
- `growth.tex` 155–158.
- `appendix-boundary.tex` 17–23 (used for Theorem F.4).
- `appendix-localized.tex` 2–16 (used for Corollary 6.19).
- `exact-localized.tex` 88–90.
- `computation.tex` 18–21 and 80–82 (Figure 2 caption).

*Issue:* The variant is stated in one sentence: "the same proof gives the
radius `4.2√(nκ)h_j` and the cap `8θ⁻¹⌈log₂(n+2)⌉`". Its constants are then
quoted inconsistently:
- radius 4.2 or 5;
- grid-point bound 17/15 or 22/15;
- `D(y_j)` bound 9/16 or 7/8;
- cap `8θ⁻¹` (Appendix F) or `100θ⁻¹` (implementation).

Lemmas 5.3 and 5.4 are proved only for weighted growth with per-coordinate
meshes `h_ij=η_j r_i`.

*Fix:* Add "Lemma 5.4′ (common mesh)" after Lemma 5.4, stating (G1)–(G4) of
Appendix G with one set of constants, and prove it by the two-line substitution
`a_j = nLh_j²`, `‖·‖_L → L‖·‖²`. Then cite it in Appendix F, Appendix G and
Section 11 instead of restating the constants. In Section 11, say that the
implementation's cap 100θ⁻¹ exceeds the analyzed cap.

**M9. The symbol `P` has four meanings, two of them inside Section 6.**

*Location:* `setting.tex` 50 (`P={i:L_i>0}`); `exact.tex` 31 (`P=ΔH`);
`constraints.tex` 435 (`P=ΔH`); Definition 7.11 and Lemma 7.17 (polytopes
`P`, `P_r`); `appendix-proximal.tex` 24 (`P(y)`).

*Issue:* Algorithm EX in Section 6 runs CT, whose stage rule and cap use
`P={i:L_i>0}` and `n_P`, while Section 6 has just redefined `P=ΔH`. A reader
checking Theorem 6.11 meets both meanings in one proof.

*Fix:* Keep `P` for `{i:L_i>0}`. Rename `P=ΔH` to `Ĥ` (integral Hessian) in
Sections 6 and 8.6. Rename the certificate polytopes to `Π_r ⊆ Π`, since `Π` is
already the box. Rename the proximal objective `P(y)` to `Q_η(y)`.

**M10. The optimal set and the letter `S` are overloaded.**

*Location:*
- `setting.tex` (`𝒮` defined); `exact.tex` 27 (`S`); `constraints.tex` 65
  ("`S=𝒮`"); `optsets.tex` 3, 14 (`𝒮`) and 36, 175 (`S`).
- `setting-growthcert.tex` 4 (`S` = interior index set); `exact-localized.tex`
  78 (`S` = interior set).
- `recourse-convex.tex` 19 (`S_t` = attachment scope).
- `growth.tex` 284 and `limits.tex` 374 (`S_t` = chain variables).
- `recourse-cuts.tex` 264 (`S` = interior set); `limits.tex` 314 (support).
- Scopes `S_a` and separators `S_{tu}`.

*Issue:* The optimal set is written `𝒮` and `S` interchangeably, sometimes in
the same section. In Section 8 the projection `S_i` of the optimal set sits
next to the scopes `S_a`. In Example 5.11 and Proposition 10.8 the variables
`S_t` sit next to the separator `S_{tu}`.

*Fix:*
- Optimal set: `𝒮` everywhere; projections `𝒮_i` (replacing `S_i` in Section
  8 and `π_i(S)` in Section 9.1).
- Interior index set: `J_0`, consistent with `J_0(s)` in Definition 6.2.
  Active index set: `J_∂`.
- Chain state variables: `ξ_t`.
- Attachment scopes in 7.3: `E_t`, as in 7.1.
- Leave `S_a` and `S_{tu}` unchanged.

**M11. The recourse notation changes in every subsection of Section 7.**

*Location:*
- 7.1 (`recourse-valuefn.tex` 2–5, 32–44, 105–120): retained set `K`,
  recourse set `R`, value function `W_B`, blocks `y^{(t)}, E_t`, `φ_t` = block
  objective, `ψ_t` = value factor, `r` blocks.
- 7.3 (`recourse-convex.tex` 13–45): retained index set `ℛ`, variables
  `z ∈ Z`, blocks `y_t, S_t`, `f_t` = block objective, `φ_t` = value factor,
  `T` blocks, coupling matrix `K_t`.
- 7.4 (`recourse-cuts.tex` 7–9, 140): retained "core" `𝒞`, residual `ℛ`,
  `V = W_𝒞`.
- 7.5: `ℛ = 𝒟 ∪ 𝒫`.
- 7.6 (`recourse-balanced.tex` 147): enumerated core `C`.

*Issue:* `ℛ` means "retained" in 7.3 and "recourse" in 7.4. `φ_t` changes
meaning between 7.1 and 7.3. The value function has three names (`V`, `W_B`,
`W_𝒞`). The number of blocks `T` clashes with the tree `T`.

*Fix:* Fix one scheme for all of Section 7:
- retained index set `𝒦`, variables `v = x_𝒦`;
- recourse (residual) set `ℛ = [n]∖𝒦`, variables `y = x_ℛ`;
- value function `V_𝒦` (drop `W_B`; in 7.2 write `V_B`);
- blocks `y^{(t)}`, `t = 1..r`, with attachment scopes `E_t`;
- block objectives `f_t`, value factors `φ_t`;
- grid value function `V^G` (replacing `V_h`).

Then "core" is the retained set `𝒦`. In 7.5, write `ℛ = ℛ_− ∪ ℛ_+`.

**M12. The letter `γ` is overloaded, and one quantity has two names.**

*Location:*
- `setting.tex` 79–83: `γ`, `γ*` = weighted growth.
- `setting-growthcert.tex` 12–13, 29, 54–55: `γ` = Euclidean growth.
- `exact.tex` 437 and `appendix-boundary.tex` 124–127: `γ` = smallest active
  derivative, `B_γ`.
- `exact-localized.tex` 81: `λ_A`, the same quantity.
- Also `γ_t` (7.3), `γ_m` (Lemma 6.13), `γ` (Proposition 8.20, Proposition
  10.1 proof, Proposition 10.9, Appendix C).

*Issue:* Lemma 3.3 uses `γ` for a Euclidean growth constant immediately after
Definition 3.2 reserves `γ` for weighted growth. The smallest inward derivative
is `γ` in Appendix F and `λ_A` in Corollary 6.19.

*Fix:*
- Lemma 3.3 and Remark 3.4: `γ` → `g_0`.
- Smallest active derivative: `λ_A` everywhere, so `B_γ` → `B_λ`.
- Local renamings: `γ_m` → `c_m`; private polytope `{y:G_ty≤γ_t}` →
  `{y:A_ty≤a_t}`; gaps `γ`, `γ_i` → `δ`, `δ_i`; random coefficients in
  Appendix C `γ` → `ξ`.

**M13. Section 8 reuses one letter for two objects at least nine times.**

*Location:* `constraints.tex`:

| Symbol | First meaning | Second meaning |
|---|---|---|
| `N` | number of bags (40, 219) | `N_j(·)`, `N_0` (116, 140); kernel basis (483, 556) |
| `K` | grid bound (219, 397–400) | saddle matrix (507–510) |
| `M` | `M_i(t)` min-marginals (215, 330, 707) | stacked matrix (449) |
| `E` | `E_j` allowance (63) | row set and entries `e` (493–495) |
| `W` | max width (62) | reduced denominator (526, 545, 642) |
| `Q` | polytope in Lemma 8.5 (147) | `Q = F − E_j` (238) |
| `v` | point `(x,z)` (39, 245, 261) | grid minimum value `v_j` (214) |
| `θ` | fractional parts (139) | grading of Section 5 |
| `τ` | threshold (440) | step parameter in Lemma 8.13 (477–479) |

*Issue:* Proposition 8.8 uses `v` as the grid minimum and as a point in
consecutive items. Theorem 8.17 uses `W` as a denominator, while `W` is the box
width in the complexity bound it cites.

*Fix:* `N` (basis) → `Ξ_J`; `N_0` → `𝓘_0`; saddle matrix → `𝖪`; stacked
matrix → `Â`; row set `E, e` → `ℰ, ε_ℰ`; `W` (width) → `s` (as in Section 3);
Lemma 8.5 polytope → `𝒬_z`; grid minimum `v_j` → `β̃_j` or `μ_j`; fractional
parts `θ` → `ϑ`; step `τ` → `t`.

**M14. Other single-letter collisions inside a section or proof.**

*Location:*
- `recourse-cuts.tex` 38 and `recourse-mixed.tex` 10: `d_i = ±(u_i−l_i)`
  (signed widths). `recourse-balanced.tex` (proof of Theorem 7.46) uses
  `η_i = −d_i` (corrections) in the same section.
- `recourse-balanced.tex` 31: `|G_i| = m_i+1`, in the subsection whose
  algorithm uses min-marginals `m_i(v)`.
- `optsets.tex` 120 (`Δ` = effective width) vs 217 (`Δ2^j` = denominator), in
  the same algorithm.
- `grids.tex` and `growth.tex`: `B_i`, `B'_i`, `B^{(j)}_i` (subbox intervals)
  next to bags `B_t`.
- `exact-localized.tex` 7: gradient written `ℓ(x)`, defined and then unused
  (`ζ` is used). `ℓ` is the lower-bound vector.
- `setting-growthcert.tex` 25: `ℓ^T d` should be `ζ^T d`. This is a wrong
  symbol in a proof.
- `recourse-local.tex` (Theorem 7.5, Proposition 7.7): oracle bound `ℓ(v)`
  next to `ℓ_i`.

*Fix:* signed widths → `δ_i`; `m_i = |G_i|−1` → `k_i`; effective width
`Δ_i(I)` → `w(I)`, reserving `Δ` for denominators; subboxes →
`X' = ∏X'_i` and `X^{(j)}`, keeping `B` for bags; delete `ℓ(x)` in 6.6;
`ℓ^T d` → `ζ^T d`; oracle bound `ℓ(v)` → `\underline V(v)`.

**M15. The Section 6 introduction and scope sentence are stale.**

*Location:* `exact.tex` 10–15 and 19; the placement of `exact-localized.tex`
(Section 6.6).

*Issue:* The introduction promises "we show that unions of uniform cells
restore a rate that is polynomial for fixed bag size" (now Section 9.1) and
"The last subsection treats explicit polynomial factors" (Section 6.6 now
follows). Line 19 renders as "Throughout Sections 6.1–9.1, F is a quadratic",
because `sec:exact-nonunique` is now Section 9.1. That range covers Sections 7
and 8, which have other models. Section 6.6 (quadratics) also comes after 6.5
(polynomials).

*Fix:*
- Line 19: "Throughout Sections 6.1–6.4 and 6.6".
- Lines 12–15: "… Section 9.1 shows that without uniqueness the single-center
  grids can be exponentially slow. Section 6.5 treats explicit polynomial
  factors, and Section 6.6 gives an acceptance test based on the filtering
  history."
- Move 6.6 before 6.5, or 6.5 to the end.

**M16. The algorithm name "FG" is undefined, and algorithm names are
inconsistent.**

*Location:*
- `optsets.tex` 45 and 92: "FG", undefined anywhere.
- `growth.tex` 41 and 166: "Algorithm 1", "Algorithm 2 (CT)".
- `appendix-boundary.tex` 27 and 98: "pruned-grid trials/algorithm".
- `limits.tex` 539: "filtered-grid algorithm".
- `limits.tex` 281 and `recourse-balanced.tex` 96, 113: "capped algorithm".
- `computation.tex` 92, 148: "capped schedule".
- Unnamed procedures: "core search" (7.4); "proximal iteration" (Appendix B);
  "the procedure" (Theorem 9.12, Appendix F).

*Issue:* The statement of Proposition 9.1 cannot be parsed without guessing
what "FG" means. Algorithms are `\paragraph` headings numbered by hand, so
cross-references like "Algorithm~2" break silently if algorithms are added.

*Fix:*
- Replace "FG" with "a single trial (Algorithm 1)".
- Add `\newtheorem{algorithm}[theorem]{Algorithm}`, so that algorithms are
  numbered and labelled.
- Use one name per algorithm: TRIAL (Algorithm 1), CT, REC, EX, UC, CORE
  (core search), TU-GRID, TU-REC, TU-EXACT, PROX (proximal iteration), DISC
  (Theorem 9.12), BND (Appendix F).
- Delete "pruned-grid", "filtered-grid", "capped algorithm" and "capped
  schedule".

**M17. Theorem 9.12 is stated in terms of a procedure defined only in
Appendix B.**

*Location:* `optsets.tex` 540–547; `appendix-proximal.tex`.

*Issue:* The statement says "run the proximal iteration with guess K", but
neither the statement nor the surrounding text says where this iteration is
defined. The appendix title is the only link. The stage budget `J_K` also uses
`τ` from REC without saying so.

*Fix:* Add before the theorem: "The proximal iteration with guess K
(Appendix B) runs graded grids around the previous output, with the proximal
term `η‖y−c‖²` and no filtering; Lemma B.1 bounds its grids and its distance
to 𝒮 when `K ≥ L/g_S`." In the statement, write "`J_K` the least `j` with
`4^jτ² ≥ 4Kns²` (`τ` as in REC)".

**M18. The exact-output theory is developed four times.**

*Location:*
- Section 6: Definition 6.2, Lemma 6.3, Corollary 6.4, Proposition 6.6, REC,
  Lemma 6.7, EX, Remark 6.12.
- Section 8.6: Definition 8.12, Lemma 8.13, Corollary 8.14, Proposition 8.15,
  TU-REC, Lemma 8.16, TU-EXACT, Remark 8.18.
- Theorem 7.18(iii) with Lemma 7.17.
- Theorem 7.39 with Lemma 7.37.

*Issue:* Proposition 8.15 is Proposition 6.6 verbatim with a different `Ω`.
The box case is the special case `A=∅`, `M=(I;−I)` of Section 8.6. The
constants `R`, `Ω`, `τ` are redefined in 8.6 with different formulas under
the same names. Theorem 7.18(iii) uses continued fractions with `R_0, Ω_0`
instead of REC. Theorem 7.46 says its exact part "follows from the proof of
Theorem 6.11, which uses … rational reconstruction", but Theorem 6.11 uses
snapping (REC). About 250 lines are duplicated, and the reader has to check
four acceptance arguments.

*Fix:*
- State the stationary-face lemma, the height corollary, acceptance and
  snapping once, for `{x: Mx ≤ d}` with `M ∈ {0,±1}`, in Section 6. Give two
  height constants: `R_box = Δ∏P_ii` (principal case) and
  `R_TU = (2n_cC_P)^{n_c}`.
- In Section 8.6 keep only the TU constants and TU-EXACT.
- In Theorem 7.18(iii), cite Proposition 6.6 with the constants of Lemma 7.17.
- Correct the sentence in the proof of Theorem 7.46.

**M19. Several smaller duplicates and forward restatements.**

*Location:*
- (a) Lemma 7.2 (`lem:cr-semiconcave`, `recourse-valuefn.tex` 46–58)
  restates Lemma 7.1(a) for `W_B` with a common `L`. It is never cited; Lemma
  7.3 cites Lemma 7.1(a).
- (b) Lemma 9.2 (`optsets.tex` 141–168) re-proves Proposition 4.2(a),(c) by
  randomized rounding. Lemma 7.3 re-proves the same rounding bound for bag
  cells.
- (c) Proposition 8.19 (`constraints.tex` 681–724) and Corollary 5.6
  (`growth-sharp.tex` 31–43) both prove that filtered uniform grids keep
  `Θ(√(nκ))` labels on box instances. Section 11 (`computation.tex` 96–97)
  still cites 8.19.
- (d) Example 5.11 restates Proposition 10.8 (same objective, bags, `g`, `L`,
  `κ ≤ 80`, `2^{m−1}` pieces). Its claims are proved only five sections later.
- (e) `related.tex` 104–106 repeats Remark 5.9 almost word for word.

*Fix:*
- (a) Delete Lemma 7.2.
- (b) State Proposition 4.2 for a product of finite *families of intervals*
  (unions of cells), and derive Lemma 9.2 and Lemma 7.3 from it, with
  `F` replaced by `V_B` for the latter.
- (c) Keep Corollary 5.6. In Section 8.7 write "Corollary 5.6 applies
  verbatim with the constant correction `E_j`". Cite 5.6 in Section 11.
- (d) Shorten Example 5.11 to "The family `G_m` of Proposition 10.8 has
  `p = 3` and `κ ≤ 80` …".
- (e) Shorten the related-work sentence to a pointer to Remark 5.9.

**M20. The order of Section 7.1 is broken.**

*Location:* `recourse-valuefn.tex` 32–103.

*Issue:* The bag-cell material (`W_B`, `e_B(C)`, Lemmas 7.2–7.3 and the
paragraph "No coordinate outside B…") is inserted between Lemma 7.1 and its
discussion. The paragraph "Part (a) explains … part (b) …" (line 97) now
follows Lemma 7.3, which has no parts. The bag-cell material is used only in
Section 7.2. In addition, `e_B(C)` uses a common `L`, while Section 4 uses
per-coordinate `L_i`, and nothing explains the change.

*Fix:*
- Move lines 32–94 to the start of Section 7.2.
- Change "Part (a) …" to "Lemma 7.1(a) explains …".
- Define `e_B(C) = Σ_{i∈B} L_i w_i(C)²/8`. The proof of Lemma 7.3 already
  works with `L_i`.

**M21. The growth notions are defined in scattered places with inconsistent
symbols.**

*Location:*
- Definition 3.2 (`setting.tex` 72–84): quadratic and weighted growth only.
- `exact.tex` 223: set growth `g_S`, inline.
- `constraints.tex` 67–71: set growth `g`, `κ_c`.
- `optsets.tex` 12–16: set growth `g_S`, `κ_S`.
- Lemma B.1, Theorem 9.12, Proposition 10.10: set growth `g`.
- Prop 7.35: core growth `κ`.
- Theorem 7.4: `κ_V`.
- "Point growth" is used throughout Sections 6 and 9–10 and Appendices F–G
  but never defined.

*Issue:* Definition 3.2 defines `κ` from *any* valid `g` but `κ̄` from the
*best* `γ*`. Lemma 5.3 then uses `κ̄` as a free parameter `≥ max{1,1/γ}`.

*Fix:* Extend Definition 3.2 to define point growth `(g, κ)`, weighted growth
`(γ, κ̄)` and set growth `(g_S, κ_S)`, each "for some valid constant". Add the
convention "`κ(L',g') := max{1,L'/g'}`". Then:
- `κ_V` → `κ(L^V, g)`;
- `κ_c` → `κ(L̄, g_S)`;
- core growth → `κ(L_𝒦, g)`.

Delete the local definitions in Sections 8 and 9.

**M22. Section 7.5 (concave–convex residuals) is never used.**

*Location:* `recourse-mixed.tex` (Propositions 7.40–7.41).

*Issue:* Nothing in the abstract, introduction, conclusion or any other
section refers to Section 7.5 or its results, and no theorem uses them. A
reader cannot tell why it is there.

*Fix:* Either add after Proposition 7.41 "Hence Proposition 7.41 supplies the
exact oracle required by Theorem 7.33 when the residual is concave–convex, with
a certificate checkable by Proposition 7.41(d)", and mention this in the
introduction's recourse paragraph; or move Section 7.5 to an appendix or
remove it.

### Minor

**m1. `l_i` and `ℓ_i` are both used for the lower bound.**

*Location:* about 65 occurrences of `l_i`, `[l,u]` and `c^0=l` in
`recourse-valuefn`, `recourse-convex`, `recourse-cuts`, `recourse-mixed`,
`optsets` (30), `limits`, `appendix-proximal`, `appendix-boundary` and
`appendix-localized`.

*Issue:* Setting, Sections 4–6 and Section 8 use `ℓ_i`; the files listed use
`l_i`.

*Fix:* Replace `l_i` with `\ell_i` globally, with care around the bag names
`L_i` in Appendix D.

**m2. Contribution (v) misstates the parameter.**

*Location:* `intro.tex` 163–164.

*Issue:* "unique-minimizer hardness at width three": Proposition 10.1 has bag
size three, that is, width two (Section 3 defines width = `p−1`).

*Fix:* "at bag size three (treewidth two)".

**m3. The abstract's list of recourse results is redundant and partly
misgrouped.**

*Location:* `abstract.tex` 26–30.

*Issue:* "private convex blocks with certified piecewise-affine responses,
convex value factors" names Theorem 7.18 twice. "Cut-based grid oracles for
balanced quadratics" (Theorem 7.46) do not lower curvature; they remove the
width parameter.

*Fix:* "Exact recourse lowers the curvature that must be discretized: private
convex blocks become value factors certified by piecewise-affine responses, and
separately concave submodular residuals are evaluated by one minimum cut; for
balanced quadratics the whole grid problem is a minimum cut, which removes the
width parameter."

**m4. Section 5 cites Theorem 9.3 for a bound it does not give.**

*Location:* `growth-sharp.tex` 45–49.

*Issue:* The text says "at most `(2+√2)√(nκ)+7` labels … (Theorem 9.3 with a
single minimizer)". Theorem 9.3 gives `K_S = 12r(2√(nκ_S)+1) = 24√(nκ)+12`
for `r=1`.

*Fix:* Cite the constant of Theorem 9.3, or add the sharper single-minimizer
computation to its proof.

**m5. Section 11 cites the wrong result and uses the wrong growth notion.**

*Location:* `computation.tex` 96–97 and 139–141.

*Issue:* The "√n law" on box paths is attributed to Proposition 8.19 (a TU
result) rather than Corollary 5.6. The segment instances are described as
"expected without growth". These instances have set growth (Remark 6.9); what
fails is point growth (Proposition 10.9).

*Fix:* Cite Corollary 5.6, and write "expected without point growth
(Proposition 10.9)".

**m6. An experimental claim appears only in Section 6.6.**

*Location:* `exact-localized.tex` 95–98 vs `computation.tex` 128–141.

*Issue:* Section 6.6 reports "29 of 30 random unplanted … within four stages,
… up to 542 stages" (experiment S1). Section 11 does not report S1. Its exact
subsection describes 20 instances with at most 534 stages.

*Fix:* Add a short S1 paragraph to Section 11 and keep only a pointer in 6.6.

**m7. A reference tag is undefined.**

*Location:* `appendix-localized.tex` 53.

*Issue:* "because `x*∈B` by (F)": the tag (F) is not defined anywhere.

*Fix:* "by Proposition 4.5".

**m8. Assembly artifact and overclaim in Section 7.6.**

*Location:* `recourse-balanced.tex` 163–165.

*Issue:* "the cut-based recourse of the report" is a leftover from a draft.
"This removes the restriction" also overclaims: Corollary 7.47 needs global
growth and gridding of the positive-diagonal coordinates.

*Fix:* "Corollary 7.47 complements Section 7.4: residual coordinates with
positive diagonal are gridded and filtered like the core, at the price of
global growth."

**m9. Grammar slip in open problem (3).**

*Location:* `conclusion.tex` 45.

*Issue:* "Propositions 8.20 and the example after it".

*Fix:* "Proposition 8.20 and Example 8.21".

**m10. The proof of Theorem 7.46 misdescribes Theorem 6.11.**

*Location:* `recourse-balanced.tex` 141–143.

*Issue:* It says Theorem 6.11 uses "rational reconstruction". It uses REC
(snapping) and Proposition 6.6.

*Fix:* "…uses only the approximation algorithm, REC and Proposition 6.6".

**m11. Remark 6.12 says snapping "needs only" a threshold that is not always
smaller.**

*Location:* `exact.tex` 343–345.

*Issue:* "Snapping recovery needs only `g/(64n²R²)`". This is larger than
`g/(32R⁴)` only when `R² > 2n²`.

*Fix:* "needs `g/(64n²R²)`, which is larger whenever `R ≥ √2 n`, …"

**m12. Mixed terminology for the same objects.**

*Location:* throughout.

*Issue:*
- "global optimizer" (8 times) vs "global minimizer" (15 times).
- "nodes", "labels", "states", "points" and "grid values" per coordinate for
  `|G_i|`.
- "stage" vs "level".
- "grading" vs "slope" (`growth-sharp.tex` 34, 39).
- "graded" vs "geometric" grids (`appendix-proximal.tex` 18, `computation.tex`).
- "center" vs "centre" (Section 7.2); "neighbours" and "behaviour" next to
  "center".

*Fix:* Use "minimizer", "nodes", "stage", "grading", "graded" and American
spelling.

**m13. The function name `f` is reused for different functions.**

*Location:* Theorem 5.7(b) defines `f(p,κ)`. Theorem 6.11 uses `f_1`,
Corollary 6.15 uses `f_d`, Theorem 7.39 uses `f(k,κ)` with `k` = core size,
and Theorem 9.12 uses `f`.

*Issue:* `f` is used for different functions under the same name.

*Fix:* Reserve `f` for Theorem 5.7. Elsewhere write "for a computable
function `f'`" or index it (`f_cut(k,κ)`).

**m14. Table-operation counts differ between sections.**

*Location:* Lemma 4.3 `O((|𝒜|+n+N)K^p)`; Theorem 9.3 `O(p(N+|𝒜|)K_S^p)`;
Theorem 8.11 `O(p(N+|𝒜|+m)K^p)`.

*Issue:* Theorem 9.3 drops the `n` term, which counts the unary corrections.

*Fix:* Use the Lemma 4.3 form everywhere.

**m15. Proposition 9.1 does not cover the first stage of CT.**

*Location:* `optsets.tex` 39–46.

*Issue:* The hypothesis is `h ∈ (0,M]`, but "every stage of CT" includes stage
0, where `h_{i0} ∈ [s_i, 2s_i)` can exceed `M`.

*Fix:* "every stage `j ≥ 1` of CT" or allow `h ≤ 2M`; the `K=1` case still
gives `β ≤ −M²/16`.

**m16. Two incompatible statements about `g` in Proposition 7.24.**

*Location:* `recourse-convex.tex` 605 and 610.

*Issue:* "growth constant `g=1/12`" and then "`g ≤ 33/16`".

*Fix:* "growth holds with constant `1/12`, and the largest growth constant is
at most `33/16`".

**m17. Section introductions misstate the hypotheses of the sections they
introduce.**

*Location:* `recourse.tex` 2–3; `limits.tex` 3–6.

*Issue:* Section 7 says `κ` "of Section 5" is built from the largest diagonal
curvature, but Section 5's parameter is `κ̄`. Section 10 says Sections 4–8
assume "quadratic growth at a unique minimizer", but Sections 8–9 use set
growth.

*Fix:* Adjust the two sentences.

**m18. Mesh notation is defined in four different ways.**

*Location:*
- `h_{ij} = η_j r_i` (Section 5);
- `h_j = s2^{-j}` (Section 5 remark, UC, Appendices B, F and G, Section 11);
- `h_j = η2^{-j}` (Section 8);
- `h_j = 2^{-j}` (Section 7.4).

*Issue:* `η` is also the mesh scale `η_j`, the TU mesh unit, an oracle error
(7.2), a path weight (Proposition 7.24), a gap (proof of Theorem 6.8) and a
proximal weight (Appendix B).

*Fix:* Write `h_j^{c} = s2^{-j}` for the common mesh. Keep `η_j` only for
Section 5 and the TU mesh unit. Rename the others: `η` (error) → `ε_or`;
proximal weight → `λ_η`.

**m19. Single-letter collisions inside proofs.**

*Location:*
- Proposition 10.6 (`limits.tex` 296, 320, 331): `V` is the vertex set and a
  random vector.
- Appendix D 19–21: bags named `L_i`, `R_j`.
- Appendix E: range `R` in Lemma E.1 and edge set `R`.
- Proposition F.5: `β_i` twice in one proof.
- Proposition 10.8: min-marginal written `μ(v)` (elsewhere `m_i(v)`),
  variables `S_t`, objective `G_m` next to grids `G`.
- Example 5.10: `Δ` (degree), `Γ` (graph; Appendix A uses `Γ_X`), `ρ_b`.

*Fix:*
- Random vector → `Y`.
- Bags → `𝔅^L_i`, `𝔅^R_j`.
- Edge set → `E_{cd}`.
- `β_i` → `b_i` for the box endpoints.
- `μ(v)` → `m_{ξ_m}(v)`; objective → `Ψ_m`.
- Degree → `d_Γ`; graph → `𝒢`.

**m20. Forward references make the reading order hard.**

*Location:*
- `setting.tex` cites Lemmas 6.13 and 6.10 and Example 5.10.
- `setting-growthcert.tex` 52 cites Section 11.
- `grids.tex` 107 cites Lemma 8.5 for the rounding proof.
- `recourse-cuts.tex` 235 cites Appendix C inline.

*Fix:* Give the independent-rounding inequality in Section 4 in two lines
instead of pointing to Lemma 8.5. Move Remark 3.4's sentence about the planted
instances to Section 11.

**m21. The two "Hadamard's inequality" citations refer to different
inequalities.**

*Location:* `recourse-convex.tex` 331 vs Lemma 6.1.

*Issue:* Lemma 7.17 uses the row-norm version for an indefinite matrix.
Lemma 6.1 is the positive-definite diagonal version.

*Fix:* "By Hadamard's inequality for rows, `|det| ≤ ∏‖row‖`".

**m22. A dangling phrase opens Appendix C.**

*Location:* `appendix-smoothed.tex` 2.

*Issue:* "remove this effect" refers to text in Section 7.4.

*Fix:* "remove the flat-direction effect of Example 7.36".

**m23. Some results use a common `L` where Section 4 uses per-coordinate
`L_i`.**

*Location:* Lemma 7.3 and Theorem 7.5 (`e_B`), Proposition 10.9 (`d_i =
Lw_i²/8`), Proposition 7.35.

*Issue:* These results are stated with a common `L` while Section 4 uses
`L_i`. This is harmless, but it is an unexplained change of hypothesis.

*Fix:* State them with `L_i`, or say once in Section 3: "statements with a
single `L` hold a fortiori with the coordinatewise `L_i`".

---

## Proposed notation table (add as the last paragraph of Section 3)

| Symbol | Reserved meaning | Current conflicting uses | Proposed renaming |
|---|---|---|---|
| `n`, `[n]` | number of variables | `n` = number of items (Proposition 10.1) | items `m` |
| `I` | input length | grid intervals `I`, `I_i` (Proposition 4.2); interval in Lemma C.1 | `[a,a']`, `J` |
| `I_C`, `I_Z` | continuous and integer index sets | `𝒞_c` (Appendix F) | `I_C` |
| `ℓ_i`, `u_i`, `s_i`, `s` | box bounds, widths, max width | `l_i` (m1); `ℓ(v)`, `ℓ(x)` (M14); `W` (Section 8); `s` variables (Proposition 10.1) | `\ell_i`; `\underline V`; `s`; `y_k` |
| `X`, `X̄`, `X'`, `X^{(j)}` | domain, hull, subbox, stage box | `B`, `B_i`, `B^{(j)}` (Sections 4–5, Appendices B, F; 6.6) | `X'`, `X'_i`, `X^{(j)}` |
| `T`, `𝒯`, `N`, `B_t`, `S_{tu}` | tree, nodes, number of bags, bags, separators | `T` blocks (7.3); `T` free set (Lemma 6.3(c)); `N` basis (8.6); `N` colors (Appendix E) | `r` blocks; `J(v)`; `Ξ_J`; `N_col` |
| `𝒜`, `f_a`, `S_a` | factors and scopes | `S_t` attachment (7.3); `S_t` chain variables | `E_t`; `ξ_t` |
| `p` | maximum bag size | `p_a` (Lemma 7.44) | `c_a` |
| `𝒮`, `𝒮_i` | optimal set, its projection | `S`, `S_i`, `π_i(S)` | `𝒮`, `𝒮_i` |
| `L_i`, `L`, `P`, `n_P` | coordinate curvatures, max, support, size | `P = ΔH`; polytopes `P`; `P(y)`; negative `L_i` (7.3) | `Ĥ`; `Π_r`; `Q_η`; `L_i^+` |
| `L̄` | directional curvature (Section 8) | — | — |
| `g`, `κ` | point growth, `max{1,L/g}` | `g` for set growth (8, 9.3, 10.4, Appendix B) | `g_S` |
| `γ`, `κ̄` | weighted growth | Lemma 3.3 `γ`; `γ`/`B_γ` (Appendix F); `γ_t`, `γ_m`, gap `γ`s | `g_0`; `λ_A`/`B_λ`; `a_t`, `c_m`, `δ` |
| `g_S`, `κ_S` | set growth | `κ_c`, `κ_V`, `κ` in 9.3 and 10.4 | `κ(L̄,g_S)`, `κ(L^V,g)`, `κ_S` |
| `G`, `G_i` | grids | `G_t` matrices; `G_m`, `G_n` objectives; `g_{i,k}` grid points | `A_t`; `Ψ_m`, `Ψ_n`; `ϑ_{i,k}` |
| `w_i(v)`, `w(I)` | largest adjacent width; effective width | `Δ_i(I)`; `w_i` occupied width (Definition 10.13) | `w(I)`; `ω_i` |
| `d_i`, `D`, `Q`, `β`, `m_i` | corrections, sum, corrected objective, bound, min-marginal | signed widths `d_i`; TU domain `D`; `D_k`; `D_0`; `Q` polytopes; `Q_0`; `m_i = \|G_i\|−1`; `μ(v)` | `δ_i`; `𝒟^{(j)}`; `δ_k`; `Δ_η`, `Δ_0`; `𝒬_z`, `Π_σ`; `Δ_F`; `k_i`; `m_{ξ_m}` |
| `K`, `K_μ`, `K_S`, `K_θ` | per-coordinate grid-size bounds | retained set `K` (7.1); `K_t`; saddle `K`; guess `K` (9.3, Appendix B); `K` pieces; `K_i` (6.6) | `𝒦`; `𝖪_t`; `𝖪`; `κ̂`; `N_pc`; `𝒱_i` |
| `U` | incumbent value | `U = Σa_i` (Proposition 10.1); `U = Σu_i` (Appendix D) | `A`; `Σ_u` |
| `M_{t→u}` | messages | `M_i(t)` (8); stacked `M` (8.6); `M` matrices in 3.3, 7.20, 9.13; `M` counts | `m_i^F`; `Â`; `diag(μ)`, `G_M`, `H_sq`; `N_…` |
| `V`, `V_𝒦`, `V^G` | value function, grid value | `W_B`, `W_𝒞`, `V_h`; basis `V` (Remark 8.2); vertex set `V` | `V_B`; `V^G`; `𝖵`; `𝒱` |
| `Δ`, `R`, `Ω`, `τ` | denominator and height constants (Section 6) | TU versions (8.6); `Δ` degree or simplex; `R_ij`; `R` leaves; `R_0`, `Ω_0`; `R_k`; `Ω_σ` | `R_TU`, `Ω_TU`, `τ_TU`; `d_Γ`, `Σ`; `ϱ_ij`; `N_Π`; `R_cv`; `ϑ_k`; `Π̂_σ` |
| `θ`, `σ(t)`, `μ` | grading, step, trial index | `θ` fractions (8.2) or function (7.44); `σ_j`, `σ` patterns, signs, noise; `μ_m`, `μ_t`, `μ_i` | `ϑ`, `χ`; `ς_j`, `π`, `o`, `ε_n`; `[r̲_m,r̄_m]`, `ν_t`, `c_i` |
| `h_{ij}`, `η_j`, `h_j^c` | per-coordinate mesh, scale, common mesh | `h_j` four ways (m18); `η` six ways; `H` in Lemma 5.2(b); `h` linear term (Lemma 7.17); `h(S)` (7.5) | as in m18; `ĥ`; `c`; `ĥ(S)` |
| `𝒦`, `ℛ` | retained and recourse index sets (Section 7) | `ℛ` retained (7.3), `𝒞` core, `C` (7.6), `𝒟 ∪ 𝒫` (7.5) | `𝒦`, `ℛ = ℛ_− ∪ ℛ_+` |
| `C` | cell | core `C` (7.6); `{i:L_i=0}` (Corollary 6.19); class `𝒞` (9.3); grid `𝒞` (10.4) | `𝒦`; `[n]∖P`; `𝔇` (diagonal class); `𝒢` |
| `J_0`, `J_∂` | interior and active coordinates of a point | `S`, `A` (Lemma 3.3, Corollary 6.19, Appendix G) | `J_0`, `J_∂` |

Algorithm names: TRIAL (Algorithm 1), CT (Algorithm 2), REC, EX, UC, CORE,
TU-GRID, TU-REC, TU-EXACT, PROX, DISC, BND. All should be numbered
`algorithm` environments with labels (M16).
