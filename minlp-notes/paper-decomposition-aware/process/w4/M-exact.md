# W4 review M-exact: mathematics of Section 6 and Appendix B

Scope: `sections/exact.tex`, `sections/exact-localized.tex`,
`sections/appendix-localized.tex`, `sections/appendix-boundary.tex`, read
against the results they invoke (Def. 3.1, Def. 3.2, Lemma 3.3
`lem:growthcert`, Prop. 4.2 `prop:cellwise`, Prop. `prop:filter`,
Def. `def:cert`, Thm `thm:certificate`, Lemma `lem:dp`, TRIAL/CT,
Thm `thm:approx`, Lemma 5.11 `lem:commonmesh` with its proof in Appendix A,
and the bit-length paragraph of Appendix A). Label numbers are from
`/tmp/dpaper/out/main.aux` (Section 6 = pp. 23-30, Appendix B = pp. 96-101).

## Overall assessment

I found no mathematical error in Section 6 or Appendix B. Every statement in
my scope that I re-derived holds as stated, with the stated constants. This
includes the revised parts:

- Prop. 6.6 `prop:accept`, now parameterized by a denominator bound.
- Def. 6.18 `def:facecand` and Cor. 6.19 `cor:local` with its new proof in
  B.1, including the stage count.
- The convention L_i := L in B.2.

Exact-arithmetic tests on small instances agree with every claim tested
(details below). The earlier findings in my area (F82/F173, F154, F171,
F172, F175, F179, F187, F189, F194) are fixed in the current text. The two
problems below are both minor: one inaccurate cost sentence in a proof, and
one notation clash with the paper's own table of reserved symbols.

## Findings

### M-exact-1 (minor): REC's cost in the proof of Theorem 6.14 omits the bit length of x̂

Location: `sections/exact.tex:373-374` (proof of `thm:exact`, "Bound under
growth").

Problem: the text says "REC, the evaluation of F(x̃) and the comparison cost
poly(I+q\*)". REC reads the CT output x̂ and compares its continuous
coordinates with ℓ_i+τ and u_i−τ. By the bit-length paragraph of Appendix A
(`appendix-growth.tex:115-144`), x̂ is a grid node with denominator dividing
Γ_X 2^α. Here α = J + O(I) + μK_μ and μK_μ ≤ 10μ2^μ(I+1), so x̂ has
O((1+μ2^μ)(I+q+1)) bits. With 2^{μ\*} ≤ 6√κ this length is not bounded by
poly(I+q\*), because q\* contains only log κ.

Consequence: the final bound f_1(p,κ)(I+1)^{C_1} is still correct. The extra
factor is a power of μ\*2^{μ\*}, which is a function of κ only and is
absorbed into f_1. Only the sentence is wrong.

Fix: replace the sentence by:
"REC, the evaluation of $F(\tilde x)$ and the comparison cost a polynomial in
$I+q^*$ and in the bit length of $\hat x$, which is
$O((1+\mu2^\mu)(I+2q^*+1))$ with $2^\mu\le6\sqrt\kappa$
(Appendix~\ref{app:growth}); this factor is also absorbed into $f_1$."

### M-exact-2 (minor): `s` names a minimizer, but the paper reserves s_i and s for widths

Locations: `sections/exact.tex:64-69` (Def. 6.2), `:71-125`
(Lemma 6.3 and its proof), `:135-140` (proof of Cor. 6.4),
`:204-230` (proof of Lemma 6.8).

Problem: Section 6.2-6.3 writes "s ∈ 𝒮" for a minimizer and s_i for its
coordinates. Table 3.1 (`setting.tex:159`) and CONVENTIONS §4 reserve s_i and
s for the widths u_i−ℓ_i and their maximum. The reserved meaning appears
nearby:

- Lemma 3.3 uses μ_i = |ζ_i|/s_i, and the Section 6 results cite it.
- Appendix B.1 and B.2 use h_j = s2^{-j}, with s the largest width.

In the proof of Lemma 6.8, "If s_i = ℓ_i then y_i−ℓ_i ≤ τ/2" can be read as
"the width equals the lower bound".

Fix: rename the minimizer in Def. 6.2, Lemma 6.3, Cor. 6.4(a) and
Lemma 6.8 to a letter that is not reserved. For example, use $\bar x$, which
is used elsewhere only locally in Appendices A and moments. Then write
$\mathcal P(\bar x)$, $J_0(\bar x)$, and "Let $\bar x\in\mathcal S$ be nearest
to $y$". In the same spirit, the cost A_\* in the proof of Thm B.4(b)
(`appendix-boundary.tex:206-210`) sits next to the set A = J_∂ ∩ I_C of the
same theorem; renaming it, for example to T_\*, avoids a second clash. This
is optional.

## What I checked and found correct

### 6.1 Scaled data
- Ĥ = ΔH is integral and symmetric: Ĥ_ii = 2Δ(H_ii/2) and Ĥ_ij = ΔH_ij.
- Ĥ_ii = ΔL_i for i ∈ I_C^+, and log R is polynomial in I.
- L ≥ 2/Δ when L > 0.
- The two elementary facts: Δρ²F(x) ∈ ℤ for x ∈ ρ^{-1}ℤ^n, and the
  separation 1/(WW′).

### Lemma 6.3 (`lem:statpoly`)
- (a) s + tw ∈ X for small |t| gives ∇_{J0}F(s) = 0 and H_{J0J0} ⪰ 0.
- (b) 𝒫(s) is a nonempty polytope in X, and H_{J0J0}d_{J0} = 0 gives
  F(x) = F(s).
- (c) J_v ⊆ J_0, and H_{J0Jv} has trivial kernel (vertex argument). Then
  H_{JvJv} ≻ 0 by the PSD argument, so J_v ⊆ I_C^+.
- The Δ²-scaled stationarity rows have an integral right side, and Cramer's
  rule gives the denominator Δ·det Ĥ_{JvJv}.
- Δ ≤ ρ ≤ R by Hadamard's inequality.

### Cor. 6.4 (`cor:height`) and Rem. 6.5 (`rem:heights`)
- Cor. 6.4: some vertex of 𝒫(s) is a minimizer of the stated height, and an
  isolated minimizer is a vertex of its own polytope. W ≤ Δρ² ≤ Ω.
- Rem. 6.5: the diagonal bound is at most both the Leibniz bound and the
  row-sum bound, and the latter two also bound nonprincipal minors.

### Prop. 6.6 (`prop:accept`)
- The proof uses only rationality of F(x), the denominator bound Ω′ for OPT,
  and β ≤ OPT. It is valid for any feasible set, as Sections 7-8 use it.

### REC and Lemma 6.8 (`lem:snap`)
- Integer coordinates of y and s agree.
- Endpoints differ by ≥ 1/Δ ≥ 1/R = 4nτ > 2τ, so the ℓ-then-u rule fixes
  every bound coordinate of s at its value, and J ⊆ J_0.
- φ(s) ≤ (3/2)|J′|τ ≤ 3/(8R).
- The vertex minimizing φ has φ ∈ ρ^{-1}ℤ, so φ = 0.
- Every LP solution differs from s′ by a kernel direction of H_JJ, so it is
  optimal. Nonsingularity is not used.

### Thm 6.9 (`thm:transfer`) and Remarks 6.10-6.11
- Thm 6.9: τ²/4 = 1/(64n²R²), and 1/(2Ω²) < 1/(ΩW).
- Part (b): Y is compact, and ε_Y > 0.
- Rem. 6.10: the inequality log₂(1/ε_S) ≤ poly(I) + max{0, log₂(1/g_S)}
  holds (the intro restates it).
- Rem. 6.11: the NP/coNP sentence is correct ("certificates of OPT > t").

### Lemma 6.12 (`lem:unique-growth`)
- The subsequence argument, including the sign constraints on u at active
  bounds and u_{I_Z} = 0.

### EX and Thm 6.14 (`thm:exact`)
- The L = 0 paragraph: REC fixes every vertex coordinate, because
  s_i ≥ 1/Δ > τ.
- Validity and termination.
- q\* ≥ 1, and the largest q used is < 2q\*.
- q\* ≤ poly(I) + log₂κ, via g ≥ L/κ and L ≥ 2/Δ.
- O(log q\*) CT calls, with Thm 5.9(b) applied at κ ≥ κ̄.
- H_{J0J0} ≻ 0 under uniqueness, so skipping singular REC calls does not
  change the bound.
- The only inaccuracy is M-exact-1.

### Rem. 6.15 (`rem:cf`)
- The continued-fraction route needs ‖x̂−x\*‖ < 1/(4R²); 2^{-q} ≤ g/(32R⁴)
  gives ≤ 1/(√32 R²).
- The comparison with g/(64n²R²) holds if and only if R² ≥ 2n².

### Section 6.5 (main text)
- Setup: the filtering thresholds are ≥ U, so {F ≤ U} ⊆ X^{(j+1)}, and
  coordinates outside P are never narrowed.
- Lemma 6.16 (`lem:node`):
  - (a) follows from Prop. 4.2(c), last claim and interval claim.
  - (b) follows from concavity along i ∉ P with d_i = 0.
- Prop. 6.17 (`prop:local`):
  - The sequential moves of Lemma 6.16(b) keep the point in X^{(j+1)}.
  - The resulting x″ lies in the narrowed box X̃.
  - The cases give ζ_i d_i ≥ μ_i d_i²; case (iv) uses d_i ∈ ℤ.
  - The quadratic identity is exact.
- y_j ∈ X̃ (text before Def. 6.18).
- The remark "with several minimizers the test can fail" is true. Example:
  F = x₁(2x₂−1) + (x₂−1)² on [0,1]² has optimal vertices (0,1) and (1,0) and
  x₁ ∉ P. The face candidate is (0,0) with F = 1 > U = 0 at every stage
  (checked).

### Def. 6.18 / Cor. 6.19 and the proof in B.1
The proof is correct line by line:
- Facts about x\*: J_0 ⊆ P; x\*_i is at a bound for i ∉ P (concavity plus
  uniqueness). The coordinates split into I_Z∩P, i ∉ P, J_0 and A.
- (G2) gives the node bound |v−x\*_i|² ≤ (17/15)ω_j².
- i ∉ P: the other endpoint has distance ≥ δ_X ≥ 6ω_j, so m > U, and
  X̃_i = {x\*_i}.
- i ∈ I_Z∩P:
  - The center is an integer within 2ω_j ≤ 1 of x\*_i.
  - The steps at t ≤ 5 are 1, since h_j+θt ≤ 1/2+5/4 < 2.
  - X^{(j+1)}_i lies within 1+5.2ω_j ≤ 3.6 of x\*_i, hence within 4.6 ≤ 5
    of c_i. So every integer is a node, and Z_i ∩ X^{(j+1)}_i = {x\*_i}.
- Continuous i ∈ P:
  - Radius 5.2ω_j < δ_X, so a bound is contained exactly for i ∈ A.
  - The interval has positive length.
  - J_+ = J_0 ∪ A.
- Candidate = x\*: J = J_0, and H_{J0J0} ⪰ 2gI.
- Test:
  - For i ∈ A, length ≤ 5.2ω_j gives μ_i ≥ (5/5.2)Γ ≥ Γ/2.
  - The three cases A = ∅, J_0 = ∅, and both nonempty (Schur complement
    with ‖H_{J0J0}^{-1}‖ ≤ 1/(2g)) all give a PSD matrix.
- Stage count:
  - δ_X ≥ 1/R and λ_A ≥ 1/(ΔR), since ∂_iF(x\*) ∈ (Δρ)^{-1}ℤ.
  - 1/g ≤ Δκ/2 when A ≠ ∅.
  - log₂Γ ≤ log₂‖H‖ + log₂(1+‖H‖Δ/4) + log₂κ.
  - Hence log₂(s/h\*) ≤ poly(I) + (3/2)log₂κ + O(1), which is
    poly(I) + O(log κ).
- The statement correctly restricts to stages that the trial reaches and
  that end by filtering. This needs a small enough ε, so the corollary does
  not by itself bound the work of an algorithm. The text does not claim
  that it does.

### Section 6.6
- Lemma 6.20 (`lem:intcurv`): interval products are exact for independent
  coordinates, the zero case for even powers is right, and the bit length is
  O(dI).
- Prop. 6.21 (`prop:lattice`): F(X) ⊆ Γ_F^{-1}ℤ, and 2^{-q} ≤ 1/(2Γ_F).
- Cor. 6.22 (`cor:poly`):
  - L_i ∈ (Γ_FΓ_X^{d−2})^{-1}ℤ.
  - |e_i|, |E| = O(dI).
  - The denominators Γ_F(Γ_X2^α)^d and 8Γ_F(Γ_X2^α)^d are right; d ≥ 2 is
    needed for the corrections.
- Example 6.23 (a)-(c): factorization (x−√2)²(x+2√2); g = 3 and κ ≤ 4;
  ∂_xx ≤ 2; F(1/2,0) has denominator 2^{2^k+1} (checked for k = 1..6).

### Appendix B.2
- L_i := L is valid, P = [n], and the L = 0 case holds.
- Lemma B.1 (`lem:labelfilter`):
  - (i) Soundness holds.
  - The second alternative of (C1) holds for every interval removed by the
    extra filter, also when it is combined with the regular filter (fixes
    F187).
  - (ii) The radius 1+10√(nκ)h_j ≤ 2 holds, the steps are 1, and
    (17/1500) < 1.
  - The extra filter keeps x\* and the centers, so Lemma 5.11 still applies.
- Lemmas B.2 (`lem:monotone`) and B.3 (`lem:patch`): the MVT and row-sum
  arguments hold.
- Thm B.4 (`thm:boundary`) (a): soundness.
- Thm B.4 (b):
  - 4^{μ\*} ≤ 32κ.
  - Reductions never remove x\* (uniqueness), so only coordinates in A are
    fixed.
  - λ_A − 2C_2r ≥ λ_A/2.
  - 2C_3r ≤ L/(4·4^{μ\*}) ≤ g/32, and σ_{μ\*} ≤ g/32.
  - j\* = poly(I) + O(log κ + B_λ).
  - Phase accounting: 2^{q\*} ≤ 2·2^{μ\*}A\*.
- Prop. B.5 (`prop:margin`), checked with sympy for n = 1, 2, 3:
  - The identity, a_i, b_i ∈ [0,1/4], ‖ρ‖ ≥ (3/4)‖e‖, and g = 9/64.
  - L = 35/16, κ = 140/9, and λ_A = 3a_n/2.
  - The (x_n,y) minor is −5.
  - α_n ∈ [a_n/2, a_n], so it needs ≥ 4·2^n−2 bits.
  - Node denominators divide Γ_X 2^{j+μK}, with Γ_X = 2^{n+2}.
- Prop. B.6 (`prop:weakcompl`): the identity, g = 1/2, L = 12, ∇_wΨ(x\*) = 0,
  v^T∇²Ψ v = −2, and the sign changes along w = 0.
- The example (x²−1/2)² + y + xy²: ∂_y = 1+2xy > 0.

### Consistency
- The S1 and E4 numbers quoted in 6.5 match Sections 11.5 and 11.6:
  - thresholds 2^{-315} to 2^{-21} (21 to 315 bits);
  - 29 of 30 instances;
  - within nine stages for the face candidate and five for the incumbent
    rule;
  - 40 to 72 stages;
  - up to 542 stages.
- Intro Theorem 1.1(c) and the intro sentence on k = poly(I) + max{0,
  log₂(1/g_S)} match Thms 6.9 and 6.14.
- No "??" in the PDF text of pp. 23-30 and 96-101.

## Checks run (targeted, local; not CI)

All scripts are in `process/w4/checks/` and use exact rational arithmetic.

1. `python3 process/w4/checks/M-exact-heights-snap.py` → ALL PASS.
   - 260 random mixed box QPs with n = 2..4; 35% have rank-deficient H.
   - 269 oracle minimizers were checked against Lemma 6.3(c): H_{JvJv} ≻ 0,
     J_v ⊆ I_C^+, height ρ = Δ det Ĥ_{JvJv}, and Δ ≤ ρ ≤ R.
   - Cor. 6.4(a)/(b): the reduced denominator of OPT is ≤ Ω.
   - 1092 REC calls on points within τ/2 of minimizers and of continuum
     midpoints, 16 of them with singular H_JJ (solved by an exact face
     enumeration that plays the role of the LP). All returned optimal points.
   - The acceptance inequality was checked at the computed W.
   - Four hand-made continuum cases of F = (x₁−x₂)² near the bounds,
     including a nonempty J′: all correct.
2. `OMP_NUM_THREADS=1 python3 process/w4/checks/M-exact-local.py 600` →
   ALL PASS (1.7 s).
   - This is my own exact implementation of TRIAL with a common mesh:
     graded grids, corrections, brute-force integer-scaled min-marginals, and
     filtering.
   - Instances: 600 random and planted QPs with n = 2, 3, of which 518 have
     a unique minimizer, and g is certified by Lemma 3.3(a) for most of them.
   - Coverage: A ≠ ∅ in 211, J_0 ≠ ∅ in 184, I_Z∩P ≠ ∅ in 231, a coordinate
     outside P in 241.
   - At all 4942 filtering stages: y_j ∈ X̃, and x\* ∈ X̃ when the minimizer
     is unique.
   - Soundness: all 3428 acceptances were optimal.
   - At 988 stages with h_j ≤ h\*: every conclusion of Cor. 6.19 held
     (X̃_i = {x\*_i}, J_+ = J_0 ∪ A, J = J_0, candidate = x\*, test passes).
   - No trial with 8κθ² ≤ 1 aborted.
   - The first acceptance always came at or before the least j with
     h_j ≤ h\* (max 9 against j\* up to 16).
   - A shorter run on 15 instances (the first command) also passed.
3. `python3 process/w4/checks/M-exact-boundary-examples.py` → ALL PASS.
   It covers the sympy checks of Example 6.23 and Props. B.5 and B.6 listed
   above.
4. An inline run of the multi-minimizer example from Section 6.5 (see above):
   the test fails at every stage, as the remark after Cor. 6.19 says.

I did not verify citation locators. These are GLS Theorems 6.4.12 and 5.1.9,
Luo–Sturm Theorem 3.3, and Horn–Johnson Theorem 7.8.1; they are the
literature reviewer's area.
