# Review: optimal intersection cuts from maximal quadratic-free sets

Target: `research-20260928b/sfree/optimal-intersection-cuts.md`, its code in `sfree/code/` and logs in
`sfree/logs/`. Background: `scouting/s-free-intersection-cuts.md` and its `sources/` folder (full texts
of Muñoz–Serrano arXiv:1911.12341, Muñoz–Paat–Serrano (MPS) arXiv:2211.05185 and arXiv:2605.30602,
Chmiela–Muñoz–Serrano ZIB 20-29). Date: 2026-09-29.

Reviewer: independent adversarial review. I did not write the note and did not edit it. My scripts
and logs are in [`sfree/`](sfree/). I wrote my own exact and numerical checks. The author's code was
imported only to compare its `corner_bound` output with mine, and I re-implemented the 11-parameter
decoding of the adversarial instances from its docstring.

## Verdict summary

| Claim | Verdict | Main point |
|---|---|---|
| Theorem 1 (1)–(3), (5): single cut = corner bound; closure = dominant | **correct** | Every step checked. Folklore, as the note says. |
| Theorem 1(4): attainment under the KKT condition | **correct** | The contradiction argument is sound. Remark (iii) (Fritz John) is correct. |
| Proposition 2 (zero reduced cost; non-attainment) | **correct** | Both examples verified exactly (`rv_props.py`). |
| Lemma 3 (≤ rank P rays) | **correct** | Standard. |
| Theorem 4 (ρ(q) = n₊ + n₀ + 1 − [b ∉ range Q]) | **correct** | Proof checked. Numerically, 80 instances with ρ = 2 in k = 3 showed no three-ray improvement over SCIP; a positive control detects such improvements. Two corollary statements need fixing (§3). |
| Corollary: Tuy cut bound-optimal for reverse-convex S | correct, but **trivial** | It follows from Theorem 1(2)–(3) plus uniqueness of the maximal S-free set, for every closed S with convex complement. Theorem 4 is not needed, so it should not be listed as a consequence of the new bound. |
| Theorem 5(1) Renegar, 5(2) O(N^⌊k/2⌋) and 2N − 4, 5(3) closed forms, 5(4) Motzkin–Straus and 1/(5k²) | **correct** | Arithmetic checked exactly. The two-ray routine agrees with my dense scan and SCIP (80 instances, relative difference ≤ 7·10⁻⁸). |
| Proposition 6 (SCIP's set vs the strip) and Remark 7 table | **correct** | Formulas verified exactly. Remark 7 table reproduced to all printed digits. |
| Theorem 8 (Lorentz orbit = all maximal sets, signatures (n,1), (1,m), incl. inhomogeneous) | **statement correct; glosses overstated** | The mathematics holds, including the use of MPS 2026 Lemma 1. But "the Muñoz–Serrano construction / SCIP's family under all transformations produces every maximal set" is true only if λ is free. With MS's and SCIP's rule λ = x̂(Ts̄)/‖x̂(Ts̄)‖, the family at a fixed s̄ is one-parameter and **misses z_K** in 2 of 24 random two-variable corners (0.989, 0.944) (§4). The h ≠ 0 step cites a remark that states only one direction; a two-line proof closes it (§4). |
| Proposition 9 (triangle and disk, first-round lowest point (1 + √13)/6) | **correct** | Verified exactly, including the shape of the rank-1 closure. |
| Lemma 10 (orbit = {C_F}, completion = upward closure, SCIP Case 4 = constant-Γ member) | **correct** | Symbolic identities verified. The rank-one decomposition argument is sound. Chmiela's φ_λ is the support function of the cap G, as claimed. |
| Theorem 11 (exact corner bound with O(N²) two-ray closed forms) | **correct** | |
| Proposition 12 (quasiconvex best-orbit problem) | **correct** | Add: the strict LMI at s̄ already forces det F > 0. |
| Lemma 13 (tangent-edge rigidity, one-parameter pencil) | **correct** | Proof checked. Independent derivation: the three linear conditions have rank 2 (dependent because of tangency), and their null space is span(G₀, G₁). Checked on both instances. |
| Theorem 14 (1)–(3): certified counterexample, z_A ≤ z_B < z_K | **correct; independently re-certified in exact arithmetic** | Re-certified in exact arithmetic with my own face enumeration, pencil derivation, sign of θ, K_A intervals and (B) certificates, plus a numeric τ-sweep. z_A = 0.975384 reproduced; best (B) 0.975385. |
| Theorem 14(4): neighbourhood | **plausible sketch** | Needs strict complementarity for ray 3 and second-order nondegeneracy, stated and checked. Not verified. |
| Second rational instance (z_A = 0.83477, strictness for (A)) | **correct** | Exact K_A sets and the boundary position of (x₀, y₀) reproduced. My numeric sweep suggests family (B) is also excluded, but this is not certified. |
| Remark 15 (McCormick wedge maximal; (B) misses it) | plausible | The (B)-curvature argument is fine. The maximality proof of W is a sketch. |
| §8.6 adversarial ratios (0.4526, 0.6224) | **reproduced for (A)** | My own code reproduces z_K = 1 and z_A. The 0.45 instance sits exactly on the 10⁻² grazing margin. "(both families) … verified" in the Summary is too strong: the (B) numbers are heuristic lower bounds. |
| **Conjecture 16** (support-1 minimizer ⇒ orbit attains z_K) | **numerically refuted** | Some corners have a unique support-1 minimizer, every edge at t* transversal and z_K = 1 exactly, yet z_A ≈ 0.9974. Two SDP solvers and a direct search agree (§6). Not certified. |
| §9 tables (one cut, loop) | **consistent with logs** | All means, medians and win counts recomputed from the JSON records. The runs were not repeated. |
| Novelty | mostly as stated, with qualifications | See §8. Theorem 4's technique is standard (inertia and second-order conditions, as in sparsity bounds for standard quadratic programs). Older "deeper cut" literature is not cited. |

## 1. Theorem 1 and Proposition 2

**Theorem 1.**
- (1) The feasible set is closed and the sublevel sets are compact, so the minimum is attained.
- (2) T_ε is compact and misses S. δ-fattening preserves S-freeness, and α_j ≥ (1 − ε)z/w_j.
- (3) Zorn's lemma. The interior of a nested union of convex sets is the union of their interiors,
  because a small simplex around the point has finitely many vertices.
- (4) I checked the sequence argument in detail.
  - θ = 0 follows even if R is not injective. If θ > 0, the scaled λ lies in X with cost < z.
  - The mean-value step needs s_n − t_n instead of s_n − ξ_n. The difference tends to 0, so the
    argument goes through.
  - Interior points of M* would be local minima of q, so ∇q = 0 there.
- (5) Separation with u ≥ 0 and the perturbation u + ε1 are correct.
- Remark (iii): multiplying the Fritz John system by λ* gives σ∇q^T(x̄ − t*) = σ₀z. Correct.

**Proposition 2**, verified in `rv_props.py`.
- (a): q(2/δ, −δ/2) = −δ/2 < 0.
- (b): For λ₁ ≥ 1 the minimum cost is the golden ratio φ, attained at λ₁ = φ, λ₂ = 0. The note's
  claim "at least the golden ratio" is right, because λ₂ ≥ 0 matters. Also q(−s², 1 − s) = −s⁴, and
  the tangency ∇q(0,1)·(0,−1) = 0.

## 2. Lemma 3, Theorem 4, Theorem 5

**Theorem 4, LICQ case.**
- The second-order condition on {w_J^T d = 0} gives Q ⪰ 0 on V, with dim V = |J| − 1.
- V ∩ ker Q ⊆ ker Q ∩ b^⊥, because ∇q(t*)^T v = b^T v for v ∈ ker Q.
- A subspace on which a nondegenerate form is PSD has dimension ≤ n₊.
- Together: |J| − 1 ≤ n₊ + n₀ − [b ∉ range Q]. Correct.

**Theorem 4, degenerate case.** q restricted to the face is exactly d^T G d. The open set {d^T G d < 0}
cannot lie in the hyperplane w_J^⊥. Correct.

**Numerical test** (`rv_zk_check.py`, `rv_posctrl.py`). For each instance I compared the best value
over supports ≤ 2 (my scan) with a global SCIP solve over all supports.

| Family | ρ | Instances | Three-ray improvements | Max relative difference |
|---|---|---|---|---|
| bilinear, random reals | 2 | 20 | 0 | 6·10⁻⁸ |
| bilinear, integer/half-integer (ties) | 2 | 20 | 0 | 4·10⁻⁸ |
| signature (1,2) | 2 | 20 | 0 | 2·10⁻⁷ |
| rank-2 Q with b ∉ range Q | 2 | 20 | 0 | 4·10⁻⁷ |
| positive control: ball, Q = I | 4 | 15 | 14 | — |

The note's `corner_bound` agrees with my scan to 7·10⁻⁸ relative on all 80 ρ = 2 instances. My first
positive control (signature (2,1), random data) produced no three-ray minimizers and so proved nothing.
The ball control does.

**Corrections to the corollaries of Theorem 4.**
- "2-variable quadratics: ρ ≤ 2 = k" is false. For example, q = x² − 1 or q = x² + y² − 1 has ρ = 3.
  Only min(k, ρ) = 2 holds. This is harmless.
- The reverse-convex corollary is immediate without Theorem 4. If cl(ℝ^k \ S) is the unique maximal
  S-free set, then every S-free C lies inside it, so its z_C equals sup_C z_C = z_K (Theorem 1(2)–(3)).
  This holds for any closed S with convex complement. The support-1 fact does need Theorem 4 (or the
  classical argument for concave minimization). §10.2 should not present the Tuy statement as a
  consequence of the new bound.

**Theorem 5.**
- (1) Renegar in O(r) variables with r + 2 polynomials; O(N^r) supports. Correct.
- (2) LP duality and the normal cones of D_w; the upper bound theorem after bounding by one extra
  facet. For k = 3, the bounded polytope with N + 1 facets has 2N − 2 vertices, at least 3 of them on
  the new facet, so ≤ 2N − 4 holds. At most 3N − 6 edges in a triangulated disk or sphere. Correct.
- (3) I re-derived the face-KKT formula: plugging μ = −G⁻¹(m + τw) into g gives
  τ² = (m^T G⁻¹ m − g₀)/(w^T G⁻¹ w). The two-ray reduction to maximizing u₊(θ), where a is quadratic,
  b linear and D quadratic, is correct.
- (4) Verified exactly: z_K ≤ ω₀ ⟺ ω ≥ ω₀ for ω, ω₀ ≤ 11; the consecutive ratio exceeds
  (1 + δ)/(1 − δ) for δ = 1/(5k²) and all k < 60; max over the simplex of ν^T A_{C₅} ν = 1/2.
- The efficacy remark (ellipsoid method) was not checked.

## 3. Proposition 6, Remark 7, Proposition 9

**Proposition 6.**
- α₁ = x₀ + 1/x₀ and α₂ = √(1 + x₀²), exact.
- SCIP's set is C_λ ∩ {t = 1} with λ = (x₀, 1)/‖·‖ in the homogenized coordinates (x, t | y).
- z_K = εx₀ + √(1 − ε²), both symbolically and on a grid for (x₀, ε) = (3, 0.2).
- The hypothesis x₀ ≥ ε/√(1 − ε²) is what makes the stationary point feasible.

**Remark 7.** I rebuilt the table with my own formulas.

| a | η | z_K | Split | Closure bound |
|---|---|---|---|---|
| 10 | a⁻³ | 0.986117 | 0.986021 | 0.099500 |
| 100 | a⁻³ | 0.999859 | 0.999859 | 0.010000 |
| 10 | a⁻¹ | 0.5106 | — | — |

This matches the note, including z_K ≈ 0.51 for η = a⁻¹.

**Proposition 9.** Verified exactly:
- t = (1 + 2√13)/17 and p₁ = (−(1 − t)/2, 2t);
- the two disk cuts meet at height (1 + √13)/6 ≈ 0.767592 < 2t ≈ 0.966012;
- the mirror cut passes below p₁, so the closure polygon is (0,2), p₁, X, p₂;
- conv(P ∩ S) is the triangle (0,2), p₁, p₂, because the arc lies above the chord;
- the second-round rays end on ∂D at p₁ and p₂.

## 4. Theorem 8 (checked against the sources)

**Homogeneous part.** Checked against MPS 2025 (`2211.05185.plain.txt`, Theorems 1.1–1.2). The
maximality condition there is (0,0) ∉ conv{(Γ(β), −β)}. MPS 2026 restates it as 0 ∉ conv Γ(D^m).
The two conditions agree for m = 1 and for n = 1, which are the only cases used.
- m = 1: the maximal sets are {γ₁^T x ≥ y, γ₂^T x ≥ −y} with γ₁ ≠ −γ₂. Each is determined by the
  ordered pair of its tangency null lines (γ₁, 1) and (−γ₂, 1).
- The "upper" halfspace contains the whole past cone, and orthochronous maps preserve this. So the
  order is preserved, and 2-transitivity of the orientation-preserving Möbius group on ordered pairs
  gives L.
- n = 1: trivial.

**Inhomogeneous part.** MPS 2026 Lemma 1 (`2605.30602.plain.txt`, §2.2) states exactly what the note
uses: every full-dimensional maximal Q_g-free K equals C_Γ ∩ H with C_Γ maximal Q_h-free. I checked its
proof: cone(K) is Q_h-free, it extends by Zorn's lemma, and relint(C_Γ ∩ H) = int C_Γ ∩ H. So part (3)
is correct for h = 0.

**Gap: the h ≠ 0 step.** The note relies on "Muñoz–Serrano Remark 3.2 as cited in MPS 2026" and says
it was not re-derived. The Muñoz–Serrano text (their §4, after Remark 5) states only one direction:
C × ℝ^ℓ *is* maximal for any maximal C. The converse needed here is short:
- For h ≠ 0, the map (x, y, z) ↦ (x, y, z − (h^T z/‖h‖²)h) is an affine bijection from H′ onto
  ℝ^{n+m} × h^⊥ that sends Q′_g to Q_h × ℝ^{ℓ−1}.
- For a set invariant under a subspace V, every maximal S-free set contains V in its lineality space,
  because int(C + V) = int C + V.

The note should include this.

**Overstated glosses: the point rule versus the orbit.** Theorem 8 is about the orbit {L(C_λ)} with
L free, which also means λ is free. Three statements go further:
- "In words: the Muñoz–Serrano construction under all admissible transformations produces *every*
  maximal S-free set";
- §6: "'SCIP's family under all transformations' is the orbit family";
- the claim that Theorem 8 "settles" MS's role-of-transformations question.

Muñoz–Serrano (Theorem 7, Example 9) and Chmiela et al. (Cases 1–4) use λ = x̂(Ts̄)/‖x̂(Ts̄)‖. With this
rule, Ts̄ lies in the plane spanned by the two tangency null lines of C_λ. So for m = 1, every set the
rule produces under any T has s̄ in the timelike plane spanned by its two tangency lines. For n = 2 this
is a one-parameter family at a fixed s̄, while the maximal sets containing s̄ form a two-parameter
family.

Test (`rv_ms_rule.py`, `rv_ms_rule_verify.py`): 24 random two-variable corners of signature (2,1), two
rays.
- The full family attains z_K in 24 of 24.
- The point rule under all of SO⁺(2,1) attains it in 20 of 24 without the MPS completion. With the
  completion (applied only when ‖a‖ ≤ |d|, as MPS Theorem 4 requires) it attains it in 22 of 24.
- The two failures have ratios 0.989405 and 0.944347. Both are in the ‖d‖ < ‖a‖ case, where no
  completion exists.
- An exact one-parameter scan of the point-rule family (10⁵ angles) confirms both values. They are
  not optimizer misses.

So the transformation question in MS's own setting (λ tied to the point) does not have the answer
"every transformation family is complete". Varying λ, or equivalently optimizing over the whole orbit,
is essential. The note's computations do use the full orbit, so its numbers are unaffected. Only the
wording needs fixing.

Minor points on Theorem 8:
- "Every quadratic in two variables … (its 2×2 part is indefinite)" should read "every *indefinite*
  quadratic". Degenerate cases such as S = {x = 0} (form x², signature (1,0) plus zeros) are not
  covered. Convex and reverse-convex cases are classical anyway.
- `orbit_n1.py` checks Theorem 1 together with the MPS parametrization (SOCP over relaxed γᵢ). It does
  not check the Lorentz transitivity, which is pure group theory and needs no check.

## 5. Bilinear section (Lemma 10 – Theorem 14)

**Lemma 10.** Checked symbolically (`rv_props.py`):
- det Φ = x₁² + x₂² − y₁² − y₂², and the eigenvalues of sym(Φ) are x₁ ± ‖y‖;
- M ∈ C_I ⟺ AMB^T ∈ C_{F} with F^T = BA⁻¹ (2000 random tests);
- h(F^{−T}(Jv)(Jv)^T) = (Fv)₁v₁/det F, ⟨Fvv^T, e₁e₁^T⟩ = (Fv)₁v₁, and adj(F^T) = JFJ^T.

The dual description C_F^* = F·PSD and the 2×2 rank-one decomposition give cl(C_F + ℝ₊E). Correct.

SCIP Case 4 (Chmiela, ZIB 20-29, eq. (12) and Case 4): a = −e_{p₊+1}, d = e_{p₋+1}, and the
second branch of φ_λ is √((1 − λ²_{p₊+1})(‖y‖² − y²_last)) + λ_{p₊+1} y_last. This is the maximum of
β^T y over the cap {β_last ≤ λ_{p₊+1}}, so the identification with the constant-Γ member of (B) is
right.

**Lemma 13.** Proof checked. In particular:
- u^T Z u > 0, because the u-inequality's tangency point is c⁻¹M₀, with h = 1 > 0;
- τ ≡ 0, from the two-sided argument;
- det(M(d) + κM₀) = det M(d), because the polarization term equals ∇q(t*)^T d = 0.

I also derived the pencil independently. The three linear conditions on F^T have rank 2, with a
two-dimensional null space equal to span(G₀, G₁), on both instances. The G₁ component alone is
singular, so θ ≠ 0.

The sign of θ comes from G₀a₀ = c₀b₀: c₀ = 4 (Theorem 14) and c₀ = 189/2 (second instance), both
positive. The author's script instead picks the sign from trace(sym(G₀M₀)). Here that gives the same
answer, but the lemma's criterion c > 0 is the one to check.

**Theorem 14, re-certified independently** (`rv_thm14_exact.py`, sympy).

1. **z_K and the minimizer.**
   - det P = 249 and q(s̄) = 3/2.
   - Exact enumeration of the 15 faces gives min over T* of q = 0, attained only at λ* = (1/2, 1/2, 0),
     so t* = (−3, 0, 0).
   - The only singular face is the interior, where the Hessian has rank 2. A continuum of interior
     minimizers would produce a second boundary minimizer, and none exists. So uniqueness is proved.
   - ∇q·d = 0 and det M(d; 0) = 48.
2. **Family (A).** The exact sets match the note:
   - K_A(s̄) = [12 − 8√2, 12 + 8√2];
   - K_A(v₁) = (−∞, 2];
   - K_A(v₂) = [−2, ∞);
   - K_A(v₃) = [−13/5 − 2√30/5, −13/5 + 2√30/5];
   - their intersection is empty.
3. **Family (B).**
   - Certificates recomputed: u_s = (1 − √2/3, 1) for κ < κ_s and u₃ = (−3/10 + √30/60, 1) for
     κ > κ₃, with κ₃ < κ_s. The slopes and signs are as in the note.
   - Numeric cross-check: over κ ∈ [−60, 60], the quantity max over τ ∈ [0, q(v)] of λ_min(A_v − τZ),
     minimized over v ∈ {s̄, v₃}, never exceeds −0.399. For large |κ| the pencil is dominated by the
     rank-one G₁, which makes the matrices indefinite.
4. **Strictness (part 3).** The compactness argument is sound.
   - A rank-2 limit contradicts (2).
   - In a rank-one limit, the lowered vertices lie in a plane Σ, and τ₁ = τ₂ = 0 because the lowered
     midpoint cannot lie in int S.
   - The interior tangent-plane argument needs (x₀, y₀) interior to proj T*. I confirmed this exactly:
     the signed distances to the hull edges are 9, 9, 23, 23.
5. **Numbers.** z_A = 0.975384: the bisection interval and the exact bound of the returned F agree to
   10⁻⁸ (`rv_orbit_numeric.py`). My own (B) search (membership via concave τ-maximization, 13 starts)
   finds 0.975385.

**Second instance.** Reproduced: q(s̄) = 5/4, λ* = (6/7, 1/7, 0), t* = (−1, −3, 3),
K_A(s̄) ≈ [4.693, 17.473] and K_A(v₃) ≈ [−1.675, 1.532], which are disjoint.
- (x₀, y₀) lies on the hull edge [v₁, v₂] (signed distance 0). So only (A)-strictness follows, as the
  note says.
- z_A = 0.834765 reproduced; best (B) found 0.834767.
- My τ-sweep also excludes every (B) set for κ ∈ [−60, 60], with margin −4.4. This supports the (B)
  claim, but it is not a certificate.

**Theorem 14(4)** (an open neighbourhood of instances) is a continuity sketch. It needs:
- the minimizer to stay unique and on the tangent edge, which requires a positive multiplier on ray 3
  and det M(d) > 0;
- the endpoints and certificate inequalities to move continuously.

This is plausible but not written out. I did not check it.

**Remark 15.** "(B) sets have curved boundaries" is right: C_F ∩ H is an affine section of a cylinder
over the circular 2×2 PSD cone, and its lower envelope is a piece of a nondegenerate quadric. The
maximality proof of the wedge W is a sketch. The conclusion is plausible; I did not check it.

## 6. Section 8.6 and Conjecture 16

**Adversarial instances** (`rv_adversarial_spot.py`). I re-implemented only the 11-parameter decoding.

| Restart | z_K (my scan / SCIP) | z_A (exact bound of SDP optimum) | Best (B) found |
|---|---|---|---|
| 4 | 1.0000000 / 1.0000000 | 0.452621 | 0.452627 |
| 1 | 1.0000000 / 1.0000000 | 0.622388 | 0.707297 (note: 0.7078) |

Caveats:
- In restart 4, two rays have relative discriminant −0.0100 and −0.0101, exactly at the imposed margin
  10⁻². The search is pinned to the margin, so the 0.45 ratio is margin-limited. Read "non-degenerate"
  as "rays 1% from grazing".
- The Summary's "up to 55% (both families) in a verified adversarial search" is too strong for (B).
  Only z_K and z_A are verified (two solvers). The (B) values are heuristic lower bounds on z_B, and
  (B)-strictness on these instances rests on a κ-grid, not a proof.
- The near-∂S 0.028 instance was not rerun.

**Conjecture 16 is numerically refuted.** Targeted test (`rv_conj16*.py`): support-1 bilinear corners
where t* = v₁ is the unique minimizer and one edge [t*, v₂] of T* is tangent to ∂S at t* (zero
multiplier on ray 2). The note's `adversarial_supp1.py` imposes transversal contact of the ray and no
grazing ray, but does not target this configuration.

- **Tangent edge.** In 25 random corners of this kind, z_A < 1 in 5. The largest gaps are 0.996927
  (instance 13) and 0.997890 (instance 14).
- **Exact data.** After rationalizing so that t* ∈ ∂S and the tangency hold exactly, face enumeration
  shows min over T* of q = 0 only at λ = e₁. So z_K = 1 exactly, with a unique support-1 minimizer.
- **Cross-checks for instance 13.** SCS gives an even lower value, 0.996468. A direct maximization of
  the exact orbit bound (201 starts, no SDP) gives 0.996927. Best (B) found: 0.996927.
- **Strict complementarity.** I tilted the edge outward so that ∇q(t*)·(v₂ − t*) > 0 (edge cosine
  10⁻³, 10⁻², 3·10⁻²). All edges at t* are then transversal, and the minimizer stays unique with
  support 1 (exact face enumeration for 10⁻³ and 10⁻²; SCIP gives 1.0000000). Results for instance 13:

  | Edge cosine | z_A |
  |---|---|
  | 10⁻³ | 0.997395 |
  | 10⁻² | 0.999726 |
  | 3·10⁻² | 0.999992 |
  | 10⁻¹ | 1 |

- **Strength of the evidence.** For cosine 10⁻³:
  - Clarabel's returned F certifies z_A ≥ 0.997395.
  - Clarabel infeasibility and a 151-start direct search both give z_A ≈ 0.99740.
  - SCS stops at 0.996951. This is SCS inaccuracy on the feasible side: Clarabel's F is exactly
    feasible at the higher value.
  - The upper bound z_A < 1 rests on two SDP solvers plus the direct search. It is not certified.

The mechanism fits Lemma 13's proof. A one-sided (or nearly tangent) edge at t* gives only the
inequality u^T Y u ≥ 0 instead of equality. The edge must still stay inside the orbit set to second
order, which is a curvature constraint that can conflict with containing s̄ and v₃. The gaps are small
(≤ 0.3%) and shrink as the edge becomes clearly transversal.

Suggested fix: withdraw Conjecture 16, or restrict it to corners where every edge of T* at t* makes an
angle bounded away from the tangent plane, and state it as open. The "orbit exactness on LP corners"
observations in §9 are unaffected, because those are measured, not conjectured.

## 7. Section 9 computations

Recomputed from `exp_mccormick_11_final.json` and `exp_mccormick_12_big_final.json` (120 records):
- every mean and median in the §9.2 table;
- orbit better than SCIP's set by > 0.01 in 60 instances, worse in 26, mean gain 0.035;
- objective-parallel cut worse by > 0.01 in 58;
- SCIP's set below 0.9·z_K in 26 and below 0.5·z_K in 3.

Trivial: the worst orbit/z_K is 0.9999695, i.e. 3.05·10⁻⁵ from 1, not "within 3·10⁻⁵".

From `exp_loop_small.json` and `exp_loop_big.json`:
- the table rows;
- round 1 on 4×4 instances: orbit better in 8 of 12, worse in 1;
- 6×8 instances after 10 rounds: SCIP's rule ahead in 5 of 10, behind in 0;
- cut counts 7.2 / 5.2 and 32.6 / 33.2 / 33.3.

The experiments were not rerun. "SCIP's set" is the scout's re-implementation (`scout_sfree.py`),
not cuts extracted from SCIP, as §11 of the note states. I checked only the Case 4 formula, not that
code.

## 8. Novelty

- **Theorem 1, Lemma 3, Theorem 5.** Folklore or routine, as the note says. The attainment criterion
  and Proposition 2 are elementary.
- **Theorem 4.** New as a statement about corner relaxations with one quadratic constraint, as far as
  I can tell. The technique is standard: second-order necessary conditions plus inertia counting.
  Sparsity bounds of this kind for local minimizers of standard quadratic programs (support bounded
  via the nonnegative inertia) are known, e.g. in the Bomze school and Chen–Peng–Zhang. I cite these
  from memory: the shared web-search budget was exhausted, and one arXiv API query found nothing. The
  note should cite this line of work. The reverse-convex corollary is not new (§2).
- **Theorem 8.** A short consequence of MPS 2025 and MPS 2026 Lemma 1 plus Möbius 2-transitivity. I
  found no statement of it. Its practical content needs the λ-free qualifier (§4).
- **Section 8** (the explicit orbit {sym(F^T M) ⪰ 0}, completion = upward closure, quasiconvex
  best-orbit bisection, tangent-edge rigidity, certified obstruction). No prior statement found.
  - arXiv API queries on 2026-09-29: `abs:"quadratic-free" OR abs:"quadratic free sets"` returned
    only the three Muñoz–Serrano/MPS papers among relevant hits. `abs:"intersection cut" AND
    (strongest OR deepest OR "corner relaxation") AND (quadratic OR nonconvex OR bilinear)` returned
    only the two MPS papers.
  - No paper after MPS 2026 (May 2026) on selecting among quadratic-free sets appeared.
- **Missing related work.** The note does not cite older work on choosing deeper cuts for concave and
  bilinear programs. This work does not anticipate the orbit results, but it belongs in §10 (cited
  from memory, not re-read):
  - Glover, "Convexity cuts and cut search", Oper. Res. 1973;
  - Konno, "A cutting plane algorithm for solving bilinear programs", Math. Program. 1976;
  - Sherali–Shetty, polar and disjunctive face cuts for bilinear programs, Math. Program. 1980;
  - Porembski, "How to extend the concept of convexity cuts to derive deeper cutting planes",
    JOGO 1999;
  - Balas–Margot, generalized intersection cuts, Math. Program. 2013 (optimizing the cut over a
    relaxation).
- **Risk.** The MPS group calls the characterization a "new avenue". Concurrent work remains a risk,
  as the note says. An unsuccessful search does not establish novelty.

## 9. Corrections requested (the note was not edited)

1. **Conjecture 16.** Withdraw or restrict it, and report the numerical counterexamples of §6.
2. **Theorem 8 glosses.** Qualify "MS construction / SCIP's family under all transformations" as
   "with λ free". Add the point-rule observation (s̄ lies in the span of the two tangency lines),
   and weaken "settles" to "answers which sets are reachable".
3. **Theorem 8(3), h ≠ 0.** Add the two-line converse argument of §4.
4. **§3 corollaries.** "ρ ≤ 2 = k" should become "min(k, ρ) = 2". Derive the Tuy statement from
   Theorem 1 and uniqueness, and drop it from Theorem 4's novelty.
5. **Summary item 7.** "up to 55% (both families) in a verified adversarial search" should say
   "(A) verified; (B) heuristic". Mention that the 0.45 instance lies on the 10⁻² margin.
6. **Theorem 8 consequences.** "every quadratic in two variables" should be "every indefinite
   quadratic in two variables".
7. **Proposition 12.** Note that the strict LMI at s̄ forces det F > 0.
8. **`certify_counterexample.py`.** Fix the sign of the pencil by the lemma's criterion
   F^T a₀ = c b₀ with c > 0, not by the trace. It gives the same result on both instances.
9. **Theorem 14(4).** Either write out the nondegeneracy conditions or drop the neighbourhood claim.
10. **§10.** Add the related work of §8, and the 3.05·10⁻⁵ detail of §7.

## 10. What remains unchecked

- Theorem 14(4) (neighbourhood) and the maximality proof of the wedge W in Remark 15.
- A certified (exact) upper bound for z_A in the Conjecture 16 counterexamples. Only numerical
  evidence exists (two SDP solvers plus direct search).
- (B)-strictness on the second rational instance and on the adversarial instances (numeric only).
- The scout's re-implementation of Chmiela Cases 1–3 used as "SCIP's set", and the experiment runs
  themselves. Only statistics were recomputed from the JSON records.
- The near-∂S adversarial instance (0.028), `test_B_identity.py`, and the bug-fix history in §9.1.
- The efficacy/ellipsoid remark, and the lexicographic-perturbation details of Theorem 5(2) in
  degenerate cases (accepted as standard).
- The prior-art search was limited: the web-search budget was exhausted, so only the arXiv API and
  the local source texts were used.

## 11. Commands run (targeted checks only)

All from `research-20260928b/reviews/sfree/` with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`. No
project-wide checks were run and CI was not consulted.

| Command | Result (log) |
|---|---|
| `python3 rv_thm14_exact.py` | Theorem 14 (1)–(3) certified exactly; second instance (A) certified, (x₀,y₀) on the boundary (`rv_thm14_exact.log`) |
| `python3 rv_orbit_numeric.py 12` | z_A = 0.975384 / 0.834765; best (B) 0.975385 / 0.834767 (`rv_orbit_numeric.log`) |
| `python3 rv_props.py` | Propositions 2, 6, 9, Theorem 5(4), Lemma 10, Remark 7: ALL PASS (`rv_props.log`) |
| `python3 rv_ms_rule.py 0 24`; `python3 rv_ms_rule_verify.py` | full orbit 24/24 = z_K; point rule misses in 2/24 (0.989405, 0.944347) (`rv_ms_rule*.log`) |
| `python3 rv_zk_check.py 7 20`; `python3 rv_posctrl.py` | z_K agreement ≤ 7·10⁻⁸; no three-ray improvement for ρ = 2; control detects 14/15 (`rv_zk_check.log`, `rv_posctrl.log`) |
| `python3 rv_adversarial_spot.py 4 1` | 0.452621 / 0.622388 reproduced (`rv_adversarial_spot.log`) |
| `python3 rv_conj16.py 11 25`; `python3 rv_conj16_verify.py 13 14`; `python3 rv_conj16_tilt.py`; `python3 rv_conj16_tilt_verify.py` | Conjecture 16 counterexample candidates, z_A ≈ 0.9969–0.99999 with z_K = 1 exact (`rv_conj16*.log`, `rv_conj16_instances.jsonl`) |
| inline Python over `sfree/logs/*.json` | §9 tables and counts reproduced |
