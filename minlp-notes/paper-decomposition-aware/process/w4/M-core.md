# W4 review M-core: mathematics of Sections 3–5 and Appendix A

Scope: `sections/setting.tex`, `sections/setting-growthcert.tex`,
`sections/grids.tex`, `sections/growth.tex`, `sections/growth-sharp.tex`,
`sections/appendix-growth.tex`. Numbers refer to the current build
(`/tmp/dpaper/out/main.pdf`): Def 3.1–3.2, Lemma 3.3, Remark 3.4,
Def 4.1, Prop 4.2, Lemma 4.3, Def 4.4, Prop 4.5, Def 4.6, Thm 4.7,
Def 5.1, Lemma 5.2, Alg 5.3 (TRIAL), Lemma 5.4, Lemma 5.5, Prop 5.6,
Cor 5.7, Alg 5.8 (CT), Thm 5.9, Remark 5.10, Lemma 5.11, Examples 5.12–5.13,
Appendix A.

I read every definition, statement and proof line by line and re-derived
each inequality and constant. I checked the constants in exact rational
arithmetic where they are rational, and with explicit margins where they
involve logarithms or square roots. I simulated TRIAL with per-coordinate
meshes and TRIAL with a common mesh in exact arithmetic on random
nonconvex mixed-integer box QPs whose minimizer and growth constants are
certified exactly. I also checked Prop 4.2, Prop 4.5 and Thm 4.7 against
exact global optima, and Prop 5.6, Cor 5.7 and Examples 5.12–5.13 exactly.
The scripts are in `process/w4/checks/M-core-*.py`. I consulted the w2/w3
reports only to confirm that earlier core findings were fixed.

## Verdict

The mathematics of Sections 3–5 and Appendix A is correct. I found no
critical or major problem. All statements I was asked to verify hold as
stated, with the stated constants:

- Lemma 5.4: the constants 9/16 and 17/15.
- Lemma 5.5: the radius 8√(k n_P) h_ij + [i ∈ I_Z] and the cap
  10 θ⁻¹ ⌈log₂(n_P+2)⌉.
- Theorem 5.9: the schedule, μ*, the bound 2^{μ*} ≤ 6√κ̄, (5.4), and the
  bit-length accounting that gives f(p,κ̄)(I+q+1)⁵.
- Lemma 5.11: (G1)–(G5) and the CT-with-common-mesh statement.
- Prop 5.6 and Cor 5.7.
- Lemma 3.3.
- Prop 4.2, Lemma 4.3, Prop 4.5 and Thm 4.7.

The exact simulations raised no assertion failures (details below). The
earlier-round issues in this area (w2 R1-math-core and w3 coreA/coreB) are
fixed in the current text. These include φ(1) with the ceiling, the integer
term in the radius, denominators stated for grid nodes only, "I+n terms",
Δ_𝒢 ≥ 1, the hypothesis w_i(0) ≥ h, ζᵀd, J_0/J_∂, the stage limit and cap
of the common-mesh variant, and the explicit incumbent in TRIAL.

Only three minor wording or notation points remain. They are listed below.

## Findings

### M-core-1 (minor): "do not grow with the number of stages" is inaccurate as written

- Location: `sections/growth.tex:259–260`; `sections/appendix-growth.tex:129`.
- Problem: the text says the node denominators divide Γ_X 2^α with
  α = J + O(I) + μK_μ, "so they do not grow with the number of stages".
  However, α contains the stage limit J, so the proved bound on the
  denominators does grow linearly in bits with the number of stages. What
  the argument shows, and what the proof needs, is different: centers and
  box endpoints are nodes of earlier stages of the same trial, so one bound
  Γ_X 2^α holds at every stage and denominators do not compound from stage
  to stage.
- Fix:
  - growth.tex: replace "so they do not grow with the number of stages"
    with "so one bound holds at all stages of a trial: denominators do not
    compound from stage to stage".
  - appendix-growth.tex:129: replace "So denominators do not grow with the
    number of stages." with "So the bound does not compound from stage to
    stage; it depends on the stage limit only through the term J in α."

### M-core-2 (minor): ρ has four meanings in Section 5 and Appendix A

- Location:
  - `growth.tex:146` (ρ = √(k n_P));
  - `growth-sharp.tex:22,26` (ρ = half-width of a box in Prop 5.6);
  - `appendix-growth.tex:82–97` (ρ_j = half-width of the stage box);
  - `appendix-growth.tex:149` (ρ = √(nκ));
  - `growth.tex:340–350` and `appendix-growth.tex:250–266` (ρ_b = a block
    variable of Example 5.12).
- Problem: each use is defined locally, so no argument is wrong. But within
  about four pages the same letter is a scaled radius, a box half-width and
  a decision variable. In Appendix A, the proof of Example 5.12 writes
  "(ρ−½)² ≤ 2(ρ−u/2)² + ½d₁²" a page after "ρ = √(nκ)". The paper's own
  notation table (Table 2, "Reserved symbols") lists the symbols that keep one meaning, so this
  overloading cuts against that policy.
- Fix: keep ρ = √(k n_P) and ρ = √(nκ) in the two localization proofs
  (they play the same role). Rename the box half-width in Prop 5.6 and its
  proof to r₀, and ρ_j in the proof of Cor 5.7 to r_j. Rename the block
  variable of Example 5.12 to ω_b, in growth.tex:340–350 and
  appendix-growth.tex:250–266.

### M-core-3 (minor): "a grid of radius R needs only O(θ⁻¹ log(1+θR/h)) nodes" omits the additive constant

- Location: `sections/growth.tex:22–23`.
- Problem: as R/h → 0 the right side tends to 0, but every nonempty side
  has at least one node. Lemma 5.2(b) has a ceiling, and that ceiling
  supplies the missing +1.
- Fix: write "needs only O(1 + θ⁻¹ log(1+θR/h)) nodes".

## What I checked and found correct

### Section 3 (setting.tex, setting-growthcert.tex)

- Def 3.1:
  - For C² functions the condition is equivalent to ∂_ii F ≤ L_i on X̄.
  - For quadratics the smallest valid bound is max{H_ii, 0}, because the
    coordinate intervals are nondegenerate (ℓ_i < u_i).
  - The endpoint property for L_i = 0 holds.
- Def 3.2 and the paragraph after it:
  - Point growth implies set growth with κ_S = κ, and weighted growth with
    γ = g/L and κ̄ = κ.
  - κ̄ is invariant when a continuous coordinate is rescaled.
  - The separable example gives κ̄ = 2 and κ = 2 max L_i / min L_i.
  - Under weighted growth x*_P is unique.
  - The two-variable example: L₁ ≥ 2 + 2^{1−k}, L₂ ≥ 2, F(t,t) = 2^{−k}t²,
    g ≤ 2^{−k−1}, γ ≤ 2^{−k}/(L₁+L₂) < 2^{−k−2}, and κ ≥ L₂/g ≥ 2^{k+2}.
- Lemma 3.3(a):
  - ζ_i d_i ≥ μ_i d_i² holds in all three cases, including integer
    coordinates at a bound with inward gradient (μ_i = |ζ_i|/s_i), integer
    coordinates at a bound with outward gradient, and interior integer
    coordinates (μ_i = −|ζ_i|, using |d_i| ≤ d_i² for d_i ∈ ℤ).
  - Hence (3.4), and point growth when H + 2M ⪰ 2g₀I.
- Lemma 3.3(b):
  - ζ_{J₀} = 0 and H_{J₀J₀} ⪰ 0 at a minimizer.
  - Under point growth H_{J₀J₀} ⪰ 2gI; under weighted growth
    H_{J₀J₀} ⪰ 2γ diag(L_i)_{i∈J₀}.
  - L ≥ L_i ≥ H_ii ≥ 2g, so κ ≥ 2 when J₀ ≠ ∅.
  - J₀ = [n] gives convexity.
- Remark 3.4 is consistent with the lemma.
- Exact random check of (3.4) and of point and weighted growth:
  M-core-growthcert.py, 80 instances × 400 points, 0 violations.

### Section 4 (grids.tex)

- Prop 4.2(a):
  - φ = F − Σ_{i∈W} (L_i/2)(y_i − c_i)² is concave along each i ∈ W.
  - Coordinates with w(J_i) = 0 are already at endpoints.
  - Replacing coordinates by endpoints one at a time stays in C ∩ X.
  - (v_i − c_i)² = w(J_i)²/4.
- Prop 4.2(b): the pairs (C, y) with y ∈ vert(C) correspond exactly to
  (y, independent choices of J_i ∈ 𝒥_i(y_i)). Nonemptiness of 𝒥_i(v) also
  holds when |G_i| = 1.
- Prop 4.2(c): the formula for β_i(J), the inequality
  d_i(v) ≥ L_i w(J)²/8, and the node bound F(x) ≥ m_i(v) + d_i(v), which
  uses W∖{i}.
- The families-of-intervals generalization uses only the two stated
  properties.
- Randomized rounding: the two-point variance is
  (x−a)(a′−x) ≤ w²/4, and d_i(Y_i) ≥ L_i w(J_i)²/8.
- Lemma 4.3:
  - The running-intersection argument makes the sets 𝒲_{v→t} pairwise
    disjoint and disjoint from B_t, so A_t is the constrained minimum.
  - Count: |𝒜|K^p for factor tables, nK^p for corrections, O(N K^p) for
    messages (Σ_t deg t = 2(N−1)), nK^p for min-marginals, and O(p) index
    work per entry.
- Prop 4.5: no retained interval contains x_i ∉ X_i″. The corrected
  minimizer keeps its intervals because m_i(y_i) = β ≤ U. Integer
  endpoints are nodes.
- Def 4.6 and Thm 4.7: both alternatives of (C1) are sound.
  - When w(J) = 0, the feasible x_i is an endpoint (a = a′, or a unit
    integer interval).
  - The case analysis via the largest j with x ∈ X^(j) is complete.
  - For quadratics, a checker that uses the smallest L_i accepts every
    certificate valid for larger L_i, because smaller corrections only
    increase Q and every m_i.
- The record paragraph after Thm 4.7 is correct: U_j ≥ OPT ≥ β_j, and
  non-retained intervals have endpoint bounds > U_j ≥ β. Coordinates
  outside P are never cut.
- Exact check against global optima (face enumeration):
  M-core-cellwise.py, 150 instances with n ≤ 3 and mixed integer
  coordinates. The checks were (a), (b), (c) of Prop 4.2 at random points,
  Prop 4.5, and validity plus soundness of filtered records. 0 failures.

### Section 5 and Appendix A (growth.tex, growth-sharp.tex, appendix-growth.tex)

- Lemma 5.2:
  - (a): unit integer intervals are ignored; longer integer steps use
    σ = ⌊h+θt⌋ ≤ h+θt; the intervals at the center have length ≤ h.
  - (b): the three cases σ ≥ (ĥ+θt)/3; the recursion
    t_{k+1} + ĥ/θ ≥ (1+θ/3)(t_k + ĥ/θ); ln(1+x) ≥ (23/24)x on [0, 1/12];
    72/23 ≤ 4; and the ceiling step (m−1 < y ⇒ m ≤ ⌈y⌉).
  - (c): σ(0) ≥ R.
  - Exhaustive exact check of (a), (b), (c): 74,060 grids (integer and
    continuous, all centers, θ ∈ {1/4, 1/8, 1/16, 3/13}), 0 failures.
- Dyadic meshes: 1/4 < L_i r_i² ≤ 1, h_{i0} ≥ s_i, h_ij is a power of two,
  and √L_i > 1/(2r_i).
- Lemma 5.4:
  - (5.2): via (h + θ|z−c|)² ≤ 2h² + 2θ²(z−c)² and
    (z−c)² ≤ 2(z−x*)² + 2(c−x*)².
  - (i): by induction.
  - (ii): Σ_{i∈P} L_i s_i² ≤ a₀ at j = 0 for any center, and a_{j−1} = 4a_j.
  - (iii): Y ≤ (4/15)(γ⁻¹+k)a ≤ (8/15)ka.
  - (iv): a/4 + (θ²/2)·5ka ≤ 9a/16.
  - (v): (15/16)γZ ≤ 13a/16 + γka/4 gives Z ≤ (13/15)γ⁻¹a + (4/15)ka
    ≤ (17/15)ka.
  - All checked in exact arithmetic at the extreme kγ = 1.
- Lemma 5.5:
  - The conversion |δ| < 2λρh.
  - |v − y_i| < 2(1+√(17/15))ρh and |v − c_i| < 2(2+√(17/15))ρh.
  - The constant 3 + 2√(17/15) + (2+√(17/15))/√2 = 7.2961 < 7.3 < 8.
  - The unit integer case gives 4.13ρh + 1.
  - θR_ij/ĥ ≤ 16θρ + θ ≤ 4√(2n_P) + 1/4, including the integer case
    ĥ = max{h/2, 1}.
  - φ(1) = 16.210 < 16.3 and φ(2) = 18.547 < 18.6; φ′(m) ≤ 4/m and
    (10 log₂(m+2))′ ≥ 7.21/m for m ≥ 2.
  - Direct check: 1 + 2⌈(4/θ) ln(5/4 + 4√(2m))⌉ ≤ 10θ⁻¹⌈log₂(m+2)⌉ for
    m < 5000, m = 10⁴..10¹², and θ ∈ {1/4, 1/8, 1/64}.
  - Stage 0 has at most three nodes.
- Alg 5.3 and Alg 5.8:
  - Filtering is applied only when U − β_j > ε, so U ≥ β_j as Def 4.4
    requires.
  - Centers stay feasible.
  - The incumbent carried over from earlier trials affects none of the
    invariants: (i) needs U ≥ OPT, and (iv)–(v) need U ≤ F(y^(j)).
- Theorem 5.9(a):
  - The termination trial θ ≤ min_{i∈P} h_iJ/s_i has unclipped steps
    ≥ h_ij (powers of two ≥ 1 are integers) and at most 1 + 2/θ < K_μ
    nodes, or s_i + 1 < 1/θ + 1 nodes for integer coordinates with
    h_ij < 1.
  - At stage J the gap is ≤ a_J/2 ≤ 8ε/9.
  - P = ∅ is handled correctly.
  - Validity follows via Thm 4.7 and the record paragraph.
- Theorem 5.9(b):
  - μ* gives 8κ̄θ² ≤ 1, 2^{μ*} ≤ 4√2·√κ̄ ≤ 6√κ̄, and
    μ* ≤ 3(1 + log₂ κ̄) (checked over a range of κ̄).
  - Σ_{μ≤μ*} K_μ^p ≤ 2K_{μ*}^p.
  - (5.4) holds, even with the stronger factor (p/(e ln 2))^p ≤ p^p; it
    was checked for p < 40 and n up to 10¹⁴.
  - K_{μ*}^p ≤ 2(60p√κ̄)^p (n+2), hence the factor I².
  - Bit lengths: node = center ± 2^{E−j−e_i}((2^μ+1)^k − 2^{μk})/2^{μ(k−1)}
    with an odd numerator, so the denominator exponent is
    ≤ J + |E| + max|e_i| + μK_μ = α. Clipped endpoints and centers are
    earlier nodes. The common denominator 8Γ_F Γ_X² 4^α covers factor
    values and corrections. b = O((1 + μ2^μ)(I+q+1)) because
    ⌈log₂(n_P+2)⌉ ≤ I+1.
  - Table work × b² gives f(p,κ̄)(I+q+1)⁵ with f as stated:
    p(60p)^p ≤ (120p)^p, and (1 + μ*2^{μ*})² = O(κ̄(1 + log₂ κ̄)²). The
    b² factor is an overcount for additions, but factor evaluations do
    cost O(b²) per monomial, and their total K^p·I·b² per stage gives the
    same order. The exponent 5 is therefore consistent.
- Remark 5.10: the Korhonen width 2tw+1 gives p = 2tw+2. Hardness for κ
  transfers to κ̄ ≤ κ in the stated direction.
- Lemma 5.11:
  - (G1) uses n_P ≤ n.
  - (G2): Y ≤ (16/15)(1/4 + 1/4)κnh² = (8/15)κnh² and
    c^(j+1) ≤ (32/15)κnh_{j+1}² ≤ 4κnh_{j+1}²; the base case holds for any
    c^(0) ∈ X.
  - (G3): D(y_j) ≤ (8/15)Lnh² ≤ (9/16)Lnh².
  - Z ≤ (16/15)(17/16)κnh² = (17/15)κnh².
  - (G4): (2+√(17/15))(1+1/√8) = 4.1481 < 4.15.
  - (G5): 8.4/√8 = 2.970 < 3; ψ(1) = 12.325 < 12.4 and
    ψ(2) = 14.377 < 14.4; ψ′ ≤ 4/m and (8 log₂(m+2))′ ≥ 5.77/m; plus the
    direct check of 1 + 2⌈(4/θ) ln(5/4 + 3√m)⌉ ≤ 8θ⁻¹⌈log₂(m+2)⌉.
  - CT-with-common-mesh termination: steps ≥ h_j/2 for integer
    coordinates with h_j ≥ 1, at most 1 + 4/θ < 8θ⁻¹⌈log₂(n+2)⌉ nodes, and
    a stage-J gap ≤ (8/9)ε.
  - Success by trial max{2, ⌈log₄(8κ)⌉}.
  - The θ = 0 remark for (G1)–(G4) holds.
- Prop 5.6:
  - The eigenvalues 2Λ − 2g and 2g give the largest growth constant g
    and L_i = Λ.
  - Σ_{k≥2} min Q_k ≤ −(n−2)Λh²/8.
  - Completing the square gives Q₁(a, v_a) ≤ 2g(Λ−g)a²/Λ.
  - κ²/(κ−1) ≥ κ.
  - Exact random check on 300 random grids (n ≤ 8): 2,585 nodes tested,
    0 failures.
- Cor 5.7:
  - Uniform rule: the corrected minimizer is uniquely 0 at every stage,
    the induction with ρ_j = min{1, 2(ν+1)h_j} works (including the case
    (ν+1)h_j > 1), and the count is 4ν + 5 ≥ √((n−2)κ) + 1.
  - Graded rule: every point of [−R, R] lies in a retained interval, and
    one side of length ≥ R needs ≥ ln(1 + θR/h′)/ln(1+θ) steps.
  - Exact simulation of the stages: n ∈ {4, 6, 8}, κ ∈ {2, …, 200},
    uniform and θ ∈ {1/4, 1/8, 1/16}. The node-count claims were exercised
    45 times (uniform) and 88 times (graded), with 0 failures.
- Example 5.12:
  - (a): (1,1) gradient (−7/4, −7/4), ψ + 3/2 ≥ (3/4)‖d‖², and the ρ-term
    inequality.
  - (b): 5/2 + 2deg/(16Δ) ≤ 21/8.
  - (c): first-order term ≥ δ/8 and second-order term
    ≥ Σ(d_ρ − d_u/2)² − δ².
  - (d) holds; the m₁×m₂ grid has path width m₁, so p = max{m₁+1, 3}.
  - The 9/8 per block at (0,0,0) holds.
  - Exact sampling on four block graphs: growth ½, strictness, and the
    inequality of (c). 0 failures.
- Example 5.13: curvatures 10, 4 and 7/4; rescaled curvatures 10·4^t and
  4^{m+1}; Ψ_m = 20δ² at ς₁ = δ; the bracket 4^m/5 ≤ κ ≤ 32·4^m; κ̄ ≤ 80.
  All checked exactly for m = 2..6.
- Exact TRIAL simulations (M-core-trial.py) on random chain-structured
  mixed-integer nonconvex box QPs with n ≤ 5:
  - x* is known, and γ and g are certified exactly by Lemma 3.3(a) and an
    exact LDLᵀ test.
  - Per-coordinate meshes with θ = 2^{−μ*}: every stage was checked for
    (i)–(iv), coordinatewise (5.2), the coordinate consequence of (v), the
    radius R_ij (and the tighter 7.3ρh + [i∈I_Z]), the cap, and success by
    stage J.
  - Common mesh with θ = 2^{−μ} from κ: (G1)–(G4) and success.
  - Seeds 7 and 23 with 60 instances each: 1,232 graded stages and 1,173
    common-mesh stages, κ̄ up to 209 and κ up to 499. 0 failures.
- Consistency with the front matter: the intro's Theorem 1.1(b), the
  abstract and the Section 5 opening match Lemma 5.5 and Thm 5.9 (cap
  10·2^μ⌈log₂(n_P+2)⌉ ≤ 60√κ̄⌈log₂(n_P+2)⌉ in every trial that builds
  tables).

## Checks run (local, targeted; not CI)

All in `process/w4/checks/`:

- `python3 M-core-constants.py`: ALL OK. This covers the scalar constants
  of Lemmas 5.4/5.5/5.11, φ, ψ, the caps, (5.4), μ*, the ln bound, and an
  exhaustive check of Lemma 5.2 (74,060 grids).
- `python3 M-core-trial.py 1 6`, `… 7 60` (log `M-core-trial-seed7.log`)
  and `… 23 60` (log `M-core-trial-seed23.log`): ALL OK, 0 failures.
- `python3 M-core-sharp.py 3` and `python3 M-core-sharp.py 5`: ALL OK
  (Prop 5.6, Cor 5.7, Examples 5.12–5.13).
- `python3 M-core-cellwise.py 11 150`: ALL OK (Prop 4.2, Prop 4.5,
  Thm 4.7).
- `python3 M-core-growthcert.py 5 80`: ALL OK (Lemma 3.3(a)).

No LaTeX build was run by this reviewer. Label numbers were read from
`/tmp/dpaper/out/main.aux`.
