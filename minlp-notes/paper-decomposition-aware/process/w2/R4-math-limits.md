# R4 — Mathematical correctness: structural limits and the three appendices

Date: 2026-10-03.
Scope: `sections/limits.tex`, `sections/appendix-moments.tex`,
`sections/appendix-lbproduct.tex`, `sections/appendix-boundary.tex`. Summary
claims about these results in the abstract, introduction and conclusion are
also checked. Line numbers refer to the source files as of this date.

## Verdict

The lower-bound results are essentially correct. I re-derived every
proposition in scope, and no main claim is false. Two statements are wrong
as written and need a scope fix:

1. **Proposition `lim:prop:setgrowth`** claims that *every* corrected-grid
   certificate has a large last-stage grid. This is false for valid path
   certificates in the sense of Definition `def:cert`; an exact
   counterexample is given below. The proof covers only filtering runs with
   thresholds U_j ≥ OPT.
2. **Theorem `thm:boundary`(b)**, with Lemma `lem:labelfilter`(ii), uses
   localization for every coordinate. Under the paper's own common-mesh
   convention (per-coordinate L_i, two-point grids for L_i = 0), a coordinate
   with L_i = 0 is never narrowed. A concrete instance satisfies all
   hypotheses of (b), yet the procedure never succeeds on it.

Both fixes take one sentence each. The remaining findings are local proof
gaps and imprecise summaries:

- Proposition `lim:prop:oracle` proves its bound for the constant-answer run
  rather than for an admissible F_c.
- The rETH result is attributed to ETH, and "grows linearly" overstates
  "is not o(p)".
- The witness in Proposition `lim:prop:moments` has small widths, but the
  optimal relaxation measure need not.
- The label filter is not covered by condition (C1) of Definition `def:cert`.
- Notation clashes.

## Checks run (targeted, exact arithmetic)

All scripts are in `process/w2/checks/`. Each finished in under a minute, and
at most one process ran at a time.

| Command | Result |
|---|---|
| `python3 r4_setgrowth_cert.py` | The counterexample to the last-stage claim of `lim:prop:setgrowth` passes (C1) and (C2), with gap ε and a two-node last grid. Cases: n=2 with ε=1/50 and 1/200; n=3, ε=1/25; n=4, ε=3/32. |
| `python3 r4_limits_identities.py` | Checks for `lim:prop:unique`: the split identity (symbolic, n=4); growth with g = ε/(n(1+2(n−1)M)) at 3,000 random rational points on 40 random Subset Sum instances; and the decision gap 1/(2n) versus 1/n. Moments, r = 1..4: the reduction identity Ψ − 1/4 = 2Π + τ(U+V), parity moments equal below order 2r and unequal at order 2r, and witness value 1/4 − (2r+1)/(16r). Boundary appendix: the identity in `prop:margin`, a_i = 2^{−(4·2^i−2)}, ∂_yG(a,0) = (3/2)a_n, the diagonal Hessian entries, the identity in `prop:weakcompl`, and vᵀ∇²W(x*)v = −2. Common mesh: radius constant (1+√(17/15)) + 1 + (2+√(17/15))/√8 = 4.1481 < 4.2. Cap: φ(n)/(8⌈log₂(n+2)⌉) ≤ 0.895 for n < 2·10⁵, and ≤ 0.963 even with radius 5. |
| `python3 r4_lbproduct.py` | Brute force for k = 2: Φ = 0 exactly at the encodings, Ψ_w is integral, every point with Φ ≥ 1 has Ψ_w ≥ W₀, OPT ≤ W₀ − 1, the minimizer is unique when the minimum weight is unique, and g = 1/(n_vN²) is valid. For random instances with k = 3, 4, 8 and N = 2, 3: the stated decomposition is a valid tree decomposition with p ≤ max{k,7}, the maximum Hessian diagonal is at most W₀(2+4N²+2k), and n_v ≤ k + 2k²N². |

I did not run any project-wide verification. I did not consult CI.

## What was re-derived and found correct

- **Proposition `lim:prop:unique` (unique-minimizer Subset Sum).**
  - Bags and path decomposition: correct.
  - The elimination identity (`lim:eq:split`) holds, and σ(x) ∈ [−U, 2U]^{n−1}.
  - Path inequality: Σ(Δδ)² ≥ 2/(n(n−1))·Σδ_k².
  - Φ is concave: its Hessian is (2/n)aaᵀ − 2MI with ‖a‖² = M.
  - Vertex values are distinct, because |Δ| < ε2ⁿ = 1/(2n).
  - γ ≥ ε. The concavity and Jensen argument gives Φ − Φ* ≥ (ε/n)‖h‖².
  - ‖σ(x) − σ(x*)‖² ≤ (n−1)M‖h‖², because |c_kj| ≤ 1 and Cauchy–Schwarz gives |Σc_kj a_j h_j| ≤ √M‖h‖.
  - g = ε/(n(1+2(n−1)M)) is valid, since 2g ≤ 2/(n(n−1)).
  - L = 4 (∂²/∂s_k² = 4 and ∂²/∂x_i² = 2a_i² − 2M ≤ 0).
  - κ ≤ 4/g = 2^{n+3}n²(1+2(n−1)M) ≤ 2^{n+3}n²(1+2nM).
  - Decision gap: OPT < 1/(2n) versus OPT ≥ 1/n.
- **Corollary `lim:cor:nopolylog`.** With q = ⌈log₂ 4n⌉, the threshold 3/(4n) separates the two cases. Correct.
- **Remark `lim:rem:dk`.** Checked against DK (pp. 21–25 of the PDF): ℓ = ⌈log₂(U+1)⌉ = ⌈log₂ 2B⌉; there are N = 2nℓ + n + ℓ = 5ℓ + 2 variables; the penalty is only on x_{i1}.
  - Maximum diagonal entry: 10 (z and w variables: 8 + 2). Ψ(y′) = D^{−2} and ‖y′ − v*‖² ≥ 2ℓ, so κ ≥ 20ℓD² ≥ 80ℓB².
  - The fractional point (1/B, 1) is feasible with all residuals zero; Ψ = q/B and dᵀ∇²Ψd = −2(q²+1), so ν/g ≥ 2B(q + 1/q) ≥ 4B. The weight-invariance claim is correct.
- **Proposition `lim:prop:oracle`.** Curvature (a minimum of concave functions), growth (needs κ ≥ 2), 2r ≤ 1, |𝒞| ≥ (κ/(8p))^{p/2}, and the disjoint balls are correct. A local gap is listed in Minor 1.
- **Remark `lim:rem:oracle`.** Correct.
- **Proposition `prop:lbwidth`.** Correct:
  - Binary uniqueness via τ, and min Φ = −α (deleting an endpoint changes Φ by 1 − 2deg_S(u) ≤ −1).
  - Multilinear extension, with Pr[V = x*] ≤ 1 − max δ_i.
  - x_i(1−x_i) ≤ δ_i, so g = 1/(2n), L = 1/n, κ = κ̄ = 2.
  - The value α can be recovered from any approximation A within 1/2: τ* ∈ [1, 2ⁿ−1] gives ⌊A/2ⁿ⌋ = −α. This step is not written out; see Minor 12.
- **Proposition `prop:lbproduct` and Appendix `app:lbproduct`.** Checked in full:
  - *Decomposition.* Every square lies in a bag, the running intersection property holds, and p = max{k,7}.
  - *Encoding.* Φ is a nonnegative integer. Φ = 0 forces exactly one ζ_{l*} = 1 per pair and (x_c, x_d) ∈ R_cd, and each clique has exactly one encoding.
  - *Values.* The tie-break is at most C(k,2)·2|R| = W₀ − 1, and Ψ_w ≥ W₀ whenever Φ ≥ 1.
  - *Uniqueness.* The minimizer is unique when the minimum-weight clique is unique. For k ≥ 2, distinct multicolored cliques have distinct edge sets.
  - *Isolation.* The lemma gives probability ≥ 1 − |R|/(2|R|) = 1/2.
  - *Conditioning.* g ≥ 1/(n_vN²) (the values are integral and the domains have length ≤ N); the diagonal is ≤ W₀(2+4N²+2k); n_v ≤ k + 2k²N²; κ, I ≤ (kN)^{c₂}.
  - *Reduction.* There are no false positives, and on yes-instances it succeeds with probability ≥ 1/2. The running time is f′(k)·N^{2c₂k/ψ(k)+O(1)}, which is effectively N^{o(k)} because ψ is computable, nondecreasing and unbounded.
  - *rETH.* Sparsification, the Chen et al. reduction from 3-SAT to Clique, and the reduction from Clique to multicolored clique are all deterministic. A one-sided-error f(k)N^{o(k)} algorithm for multicolored clique therefore gives a one-sided-error 2^{o(n)} algorithm for 3-SAT, which contradicts rETH (any bounded-error form).
  - *Theorem `thm:approx`.* It has a(p) = p/2 + O(1) and C = 5.
  - Precision issues are listed in Minor 2–4.
- **Proposition `lim:prop:messages`.** Correct:
  - The induction S_t ≤ 2^{t−m}S_m + Σ_{j>t}2^{t−j}|r_j|.
  - ‖(2^{t−m})‖² < 4/3, and the shift-series operator norm is ≤ 1.
  - The chain to ‖S‖² + ‖z‖² ≤ 8G_m.
  - Diagonal entries 10, 4 and 7/4, so κ ≤ 80; also ∇²G_m ⪰ −¼I.
  - W vanishes exactly on {0, …, 2^m − 1}.
  - Both representation bounds give K ≥ 2^{m−1}.
- **Proposition `prop:oraclebarrier`.** Correct:
  - ∂_i f = w z_i(1−ρ)², ∂_{ij}f = δ_{ij}(1−ρ)² − 4z_iz_j(1−ρ), and ∂_{ii}f ≤ 1.
  - 1 − (1−ρ)³ − ρ = ρ(1−ρ)(2−ρ), so g = w²/(6k).
  - The subcube pigeonhole argument and the choice √(6ε) < w < 1/(2M) work. Both output types are refuted.
- **Proposition `lim:prop:constraints`.** Correct: the uniqueness argument, g = 1/(2n+3), κ = 1, the separation by 1/2, and the remark on K₀ = W + 1 (the integer columns B are arbitrary in Definition `def:tu-model`, η = 1, W = B).
- **Lemma `lim:lem:mixture` and Definition `lim:def:moments`.** Correct.
- **Proposition `lim:prop:moments` and Appendix `app:moments`.** Correct:
  - Node relabelling, c = (u, −½, −v_{r−1}, …, −v₁), the identity (`lim:eq:momsplit`).
  - Π is multilinear with vertex values (a−b)(a−b−1)/2 ≥ 0.
  - The path inequality for 2r edges gives 2/(2r−1).
  - Node displacement ≤ 2‖(u,v)‖₁, so g_r = τ/(1+8(2r−1)²) ≤ 1/(2r−1); ν ≤ 2.
  - The parity laws are probability laws; the moments agree through order 2r − 1; E U = r/2 and E V = (r−1)/2; the value is (2r−1)/(16r).
  - The widths are right: 2r − 1 continuous coordinates and 2r − 1 controls.
  - Remark `lim:rem:moments`: the identity, g = 1/22, ν = 2, L = 32/h², the moments 1/2, 5/16, 7/32 versus 11/64 and 41/256, the value 3/32 and the PSD completion are all correct. The completion also satisfies McCormick with s ∈ [0,h], not only [0,2h].
- **Appendix `app:boundary`, common-mesh constants.** Rewriting Lemma `lem:inv` in Euclidean form with A_j = nh_j² gives:
  - (iii) Y ≤ (8/15)κA, (iv) D(y) ≤ (9/16)LA, (v) Z ≤ (17/15)κA.
  - Localization radius (1+√(17/15)) + 1 + (2+√(17/15))/√8 < 4.15 < 4.2 (plus one for integer coordinates).
  - The cap 8θ^{−1}⌈log₂(n+2)⌉ holds, even with radius 5.
  - The adapted constants 22/15 ≥ 17/15 and 5 ≥ 4.2 are therefore valid but weaker than what is proved (see Minor 9).
  - Lemmas `lem:monotone` and `lem:patch` are correct; the row-sum bound gives C₂r and C₃r.
  - Theorem `thm:boundary`(a) is correct.
  - In (b), with all coordinates localized: γ − 2C₂r ≥ γ/2; 2C₃r ≤ L/(4·4^{μ*}) ≤ g/32 and σ ≤ g/32; the phase accounting 2^{q*} ≤ 2·2^{μ*}A* = O(√κA*) holds.
- **Proposition `prop:margin`.** Correct: a_i; ‖r‖ ≥ (3/4)‖e‖; the identity; g = 9/64, L = 35/16, κ = 140/9, γ = (3/2)a_n; the minor −5; and α_n ∈ [a_n/2, a_n], which forces the denominator bound.
- **Proposition `prop:weakcompl`.** Correct: the identity; u² ≥ (x − x₁*)² because x + x₁* > 1; L = 12, κ = 24; the sign changes on w = 0; vᵀHv = −2.

## Findings

### Major

**M1. Proposition `lim:prop:setgrowth`: the last-stage claim is false for general path certificates.**
Location: `limits.tex` 455–458 (statement), 481–487 (proof); summarized at `limits.tex` 20–21 and `intro.tex` 132–133.

*Issue.* The statement says that "every corrected-grid certificate of accuracy ε, including its filtering history, has a last-stage grid with at least 1 + 1/(2√ε) nodes in every coordinate". The proof uses the *filtering rule* with a threshold U ≥ OPT = 0. That rule never removes an interval, because every interval contains a coordinate of some optimal point t𝟏. A valid path certificate (Definition `def:cert`) obeys a different rule: (C1) lets it remove any interval whose endpoint min-marginals are ≥ β, and here β < 0.

*Counterexample.* Take n = 2, F = (x₁ − x₂)², L_i = 2 and ε = 1/50.
- G⁽⁰⁾ is the uniform grid {0, 1/5, …, 1}² on [0,1]². All min-marginals equal −1/50.
- B⁽¹⁾ = [0, 1/5]² with G⁽¹⁾ = {0, 1/5}². Then min Q⁽¹⁾ = −1/50.
- Take β = −1/50 and x̂ = 0. Conditions (C1) and (C2) hold, and the gap is 1/50 = ε.
- The last grid has 2 nodes per coordinate, but the claim requires ≥ 4.54.
- The script `r4_setgrowth_cert.py` checks this exactly and also gives cases with n = 3 and 4.

The weaker conclusion, that the certificate size is not polynomial in log(1/ε), still holds in this example: the stage-0 grid has about 1/√(2ε) nodes. However, the paper proves it only for filtering runs.

*Fix.* Restrict the statement to what the proof shows. Replace "Hence every corrected-grid certificate of accuracy ε, including its filtering history, has a last-stage grid …" with:

> "Hence every run of the filtering method with thresholds U_j ≥ OPT (in particular every run of Algorithms 1 and 2) that certifies accuracy ε ends with a grid of at least 1 + 1/(2√ε) nodes in every coordinate. A general path certificate may remove intervals whose min-marginals lie in [β, 0], so its last grid can be small, but its stage-0 grid then has gaps of length at most 2√ε on the removed part."

At `limits.tex` 20–21, replace "does not bound the size of any corrected-grid certificate" with "does not bound the grids produced by filtering". Make the same change at `intro.tex` 133.

**M2. Theorem `thm:boundary`(b) and Lemma `lem:labelfilter`(ii) assume localization for coordinates with L_i = 0.**
Location: `appendix-boundary.tex` 5–8, 17–23, 36–37, 48–54, 154–156.

*Issue.* The appendix uses "the common-mesh variant of Algorithm 1". In Algorithm 1(i) and Definition `def:filter`, a coordinate with L_i = 0 gets the grid {ℓ_i, u_i} and is never narrowed (B′_i = B_i for i ∉ P). Appendix `app:localized` defines the same "common-mesh variant" with "two-point grids for coordinates with L_i = 0". Its (G4) also restricts localization to L_i > 0. The boundary appendix states the localization bound without this restriction. It then uses the bound for every continuous coordinate (r ≤ 5√(nκ)h_{j*}) and for every integer coordinate (Lemma `lem:labelfilter`(ii) needs unit intervals).

*Counterexample under that convention.* Take F = x(2 − x) + x/2 + (y² − 1/2)², with x ∈ {0,1,2} and y ∈ [0,1].
- The unique optimizer is (0, 1/√2) with OPT = 0. Point growth holds with g = 1/5, L_y = 10 and L_x = 0. No continuous coordinate is active, so the hypotheses of (b) hold.
- Coordinate x keeps the grid {0, 2} and the box {0, 1, 2}. The label filter needs unit intervals, so it never applies.
- So "every integer coordinate of the retained box is a singleton" never holds, and the reduction phase is never entered.
- A zero gap is impossible because y* is irrational. The procedure never succeeds, contradicting (b).

A coordinate with L_i = 0 that stays at full width also makes r large in the midpoint test and the patch test.

*Fix.* Add after line 8: "In this appendix every coordinate uses the single bound L (L_i := L for all i), so every coordinate is gridded and filtered." The Euclidean proof of Lemma `lem:inv`(v) then bounds every coordinate of z. If L = 0, the first stage is exact and has zero gap. Alternatively, import the node-exclusion argument of `app:localized`, which fixes coordinates with L_i = 0 at their optimal endpoint once h_j is small, and state (G4) with the restriction L_i > 0.

### Minor

**1. `lim:prop:oracle`, deterministic part (`limits.tex` 243–245, 262–268).**
The proof shows that the run with constant answers gp makes ≥ |𝒞| − 1 evaluations. That run is not a run on any admissible F_c. The statement claims the bound "on some F_c".

*Fix.* Add: "For c ∈ 𝒞 let t_c be the index of the first evaluation of the constant run that lies in B(c,r). The run on F_c agrees with the constant run up to and including evaluation t_c. At most one c (the one whose ball contains y) has no such index. Since each point lies in at most one ball, the finite t_c are distinct, so some F_c forces at least |𝒞| − 1 evaluations."

In the randomized part (lines 270–276), "the run on the constant answers has at most Q evaluations" should read "consider the first Q evaluations of the run on the constant answers".

**2. rETH attribution and "grows linearly".**
Locations: `limits.tex` 14–17; `abstract.tex` 24–25; `intro.tex` 129–131; `growth.tex` 237–239; `conclusion.tex` 14, 39.

At `limits.tex` 15–17, both propositions are attributed to "the exponential-time hypothesis", but `prop:lbproduct` assumes rETH. Also, Proposition `prop:lbproduct` proves that the exponent is not (effectively) o(p). That means a(p) ≥ cp for infinitely many p, not that it "grows linearly".

*Fix.* At `limits.tex` 15–17, write: "under ETH the dependence on p is exponential even when κ ≤ 2 (Proposition `prop:lbwidth`), and under rETH the exponent of κ cannot be o(p) (Proposition `prop:lbproduct`)". Use "cannot be o(p)" in the abstract, the introduction, Remark `rem:fpt` and the conclusion.

**3. `prop:lbproduct` statement and appendix: definitions and citations (`limits.tex` 346–351; `appendix-lbproduct.tex` 58–61).**
- rETH is never defined. Add: "(rETH: 3-SAT on n variables has no randomized algorithm with error probability ≤ 1/3 and running time 2^{o(n)})", with a citation such as Dell, Husfeldt, Marx, Taslaman and Wahlén (2014).
- Chen et al. (2006) prove the bound for Clique. Add the parameter-preserving reduction from Clique to multicolored clique, or cite a textbook statement for multicolored clique (Cygan et al. 2015, Ch. 13–14).
- "In particular a bound f(p)κ^{a(p)}I^C requires a(p) ≠ o(p)" follows from the main statement only for effectively o(p). Write "requires that a(p) ≤ p/ψ(p) fails for every computable nondecreasing unbounded ψ".

**4. Appendix `app:lbproduct`: notation and a missing hypothesis.**
- R denotes both the weight range in Lemma `lem:isolation` (lines 4–6) and the edge set (lines 20–22). Rename the range to {1, …, ρ}.
- N denotes vertices per class here but the number of tree nodes in Section `sec:setting`.
- The variables ζ_l, S_l, A_l, B_l and m = |R_cd| need a pair index (ζ_l^{cd}, …, m_{cd}).
- The binary S_l clashes with the separator notation S.
- Line 47: g ≥ 1/(n_vN²) holds only when the minimizer is unique. Write "If the minimum-weight clique is unique, the values are integral and the minimizer is unique, so g ≥ 1/(n_vN²)".

**5. Lemma `lem:isolation` proof (`appendix-lbproduct.tex` 12–14).**
The union bound is implicit. Add: "a union bound over e ∈ W gives probability at most |W|/R that the minimizer is not unique".

**6. `lim:prop:setgrowth` uses a uniform L (`limits.tex` 447–452, 476–478, 485).**
The corrections of Definition `def:corr` use L_i (here L₁ = L_n = 2 and L_i = 4 otherwise). Write d_i(v) = L_iw_i(v)²/8 and β ≤ −(L_j/8)W_j², and use L_i ≥ 2. The bound L/g_S ≤ 2n(n−1) holds for L = max_i L_i = 4.

In lines 482–483, the phrase "for t ∈ [a,b′]" is misplaced. Write: "for t ∈ [a,b′], Proposition `prop:cellwise`(c) at x = t𝟏 gives min{m_i(a), m_i(b′)} ≤ F(t𝟏) = 0 ≤ U".

**7. `lim:prop:moments` consequence: whose widths? (`limits.tex` 649–659; `appendix-moments.tex` 90–92).**
The bound Σw_i² ≤ (4r−2)max{2rh,ω}² holds for the witness. The partition may contain wide cells, so a measure that attains R_k may occupy them. The inequality "OPT − R_k ≤ C·ν̄·Σw_i²" does not say which measure's widths are meant.

*Fix.* Require every cell to have width ≤ max{2rh, ω}. A uniform partition with [0, 2rh] as one cell does this. Then every feasible point has Σw_i² ≤ (4r−2)max{2rh,ω}². Alternatively, state the consequence for feasible points: "there is no C with value(μ) ≥ OPT − C(p, ν̄/g, k)·ν̄·Σw_i(μ)² for all feasible μ".

**8. Notation clashes in scope.**
- `appendix-moments.tex` 19–21: the bag names L_i and R_j clash with the curvatures L_i and the relaxation values R_k. Rename them, for example to 𝓛_i and 𝓡_j.
- `limits.tex` 296 and 319–320 (`prop:lbwidth`): V is both the vertex set and the random vector, and M is the multilinear part (M = Σa_i² in `lim:prop:unique`). Use Y for the random vector, as in `lim:prop:unique`, and P(x) for the multilinear part.
- `appendix-boundary.tex` 203–207, 223, 247 (`prop:margin`): h is both the mesh and the function x_n − x_{n−1}²/8; β_i is both a coefficient and a box endpoint; r is both a half-width and a residual. Rename the function to η(x), the coefficient to b_i, and the box endpoints to [α_i, α_i′].

**9. "Rounder constants" 22/15 and 5 (`appendix-boundary.tex` 19–23, 54).**
The proof gives 17/15. The value 22/15 is valid but neither rounder nor needed: Lemma `lem:labelfilter`(ii) needs only (17/15)κnh_j² < 1. Write: "…gives ‖z − x*‖² ≤ (17/15)κnh_j² for every grid point z with Q(z) ≤ U at stage j, and retained intervals within 4.2√(nκ)h_j ≤ 5√(nκ)h_j of y_{j,i} (plus one for integer coordinates); we use the radius 5 below." Change line 54 to 17/15.

**10. Label filter versus (C1) (`appendix-boundary.tex` 30–34; `grids.tex` 193–194).**
After the label filter, the unit interval [v_max, v_max+1] is not contained in B⁽ʲ⁺¹⁾_i, but m_i(v_max) ≤ U may be below β. So (C1) as stated fails, and "the filtering-history argument of Proposition `prop:filter` remains valid" is not literally true for Definition `def:cert`.

*Fix.* Add to (C1): "for an integer coordinate whose grid intervals all have length one, every label v ∈ G_i⁽ʲ⁾ outside B_i⁽ʲ⁺¹⁾ has m_i⁽ʲ⁾(v) ≥ β". Part (i) of the lemma already proves that this condition is sound.

**11. The case L = 0 in Theorem `thm:boundary`(b) (`appendix-boundary.tex` 140–151).**
The third condition defining j* and the term log(1/L) are undefined when L = 0. Add: "If L = 0, the first stage is exact (endpoint grids) and has zero gap, so the trial succeeds at stage 0; otherwise …".

**12. `prop:lbwidth`: decoding α (`limits.tex` 330–333).**
The proof does not say how α is obtained from an approximation A within 1/2. Add: "since τ(x*) ∈ [1, 2ⁿ−1], ⌊A/2ⁿ⌋ = −α".

**13. The L = 0 optimality remark (`limits.tex` 340–342).**
"Optimal up to the base" needs a lower bound for instances with L = 0, but the instance of `prop:lbwidth` has L = 1/n. Add: "dropping the term (1/(2n))Σ(x_i² − x_i) gives a multilinear instance with L = 0, the same unique binary minimizer, g = 1/n and κ = 1, to which the same ETH (and SETH) bounds apply".

**14. "κ locates the complexity boundary" (`limits.tex` 170–177).**
The regimes κ ≤ I^{O(1)} and κ ≤ 2^{O(I)} leave a large gap. Replace "The parameter κ therefore locates the complexity boundary at fixed width" with: "At fixed width the problem is thus polynomial when κ ≤ I^{O(1)} and NP-hard when κ may be 2^{O(I)}; padding with decoupled terms t_j², which leaves κ unchanged, gives NP-hardness already for κ ≤ 2^{I^δ}, for every fixed δ > 0." Also, "the arithmetic is polynomial in its numerator lengths" (line 172) is vague. Write "and the bit lengths are polynomial in I + q + log κ".

**15. Conclusion wording (`conclusion.tex` 13–15).**
"The dependence on the condition number must be polynomial" overstates Corollary `lim:cor:nopolylog`, which excludes only polylogarithmic dependence. Write: "the dependence on κ cannot be polylogarithmic unless P = NP, and under rETH its exponent cannot be o(p)".

**16. Statement of Theorem `thm:boundary`(a) (`appendix-boundary.tex` 113–118).**
The statement describes only the face-box output. Add: "or, after a zero certified gap, the incumbent, which is then a rational optimizer".

**17. Terminology (`appendix-boundary.tex` 27, 98; `limits.tex` 539).**
"Pruned-grid trials", "capped pruned-grid algorithm" and "filtered-grid algorithm" are not the terms of Section `sec:growth`, which uses "capped trials" and "Algorithm 1/2". Use "the capped trials of Algorithm 2 (common-mesh variant)".

**18. Wording (`limits.tex` 7; `intro.tex` 126).**
"Does real work" is informal. Write: "and that none of them can be dropped".

## Overall recommendation

Accept the limits section and the three appendices after these revisions:

- Restrict the scope of `lim:prop:setgrowth` (M1).
- Fix the coordinate convention used in `app:boundary` (M2).
- Close the small proof gaps (Minor 1, 7 and 10).
- Correct the attribution and wording of the lower-bound summaries (Minor 2, 3, 14 and 15).

All other propositions in scope re-derive correctly with the stated constants.
