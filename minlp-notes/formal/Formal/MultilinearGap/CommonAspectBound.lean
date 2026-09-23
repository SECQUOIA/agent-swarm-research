import Formal.MultilinearGap.CoefficientInequality
import Formal.MultilinearGap.OriginalBoxTransfer

/-!
# The common-aspect bound `rho + 2`

This module discharges the Tier D obligations PB19-PB22 of
`formal/topics/18-positive-box/CLAIMS.md` and, through the transfer step already
available in `Formal.MultilinearGap.OriginalBoxTransfer`, the Tier E obligation
PB25.

Throughout, `rho > 1` is the aspect ratio, `t = rho - 1 > 0` the shift of the
normalization `x i = 1 + t * u i` carrying `[0,1]^n` onto `[1, rho]^n`, and the
objective is the physical monomial `physMonomial t s = ∏ i ∈ s, (1 + t * u i)`.
The four generating polynomials of the moment families fixed by
`Formal.MultilinearGap.CoefficientInequality` are

* `C(t) = physUpper t s x`, the exact concave envelope, attained by
  `thresholdLaw x` simultaneously for every support;
* `V(t) = physLower t s x`, the exact convex envelope, attained by the
  adjacent-count law;
* `P(t) = physMonomial t s x`, the independent-rounding expectation;
* `O(t) = physOrient t s x`, the fair endpoint-orientation expectation.

The results, in the order of the obligations:

* PB19: `physCombination_eq_sum_coeffF`, the identity
  `(2 + t) C + V - (1 + t) P - 2 O = ∑_{j = 0}^{n + 1} F_{n,j} t ^ j`.
  The summation range is `Finset.range (s.card + 2)`, that is `j = 0, …, n + 1`,
  and **the top order is not lost**: `(2 + t) C` and `(1 + t) P` both have degree
  `n + 1`, and their `t ^ (n + 1)` coefficient is `C_n - P_n`, which is exactly
  `F_{n,n+1}` by `coeffF_card_add_one` and is generically nonzero.  Truncating
  the sum at `j = n` makes the statement false.
* PB20: `physUpper_sub_physLower_le`, the inequality
  `C - V ≤ rho (C - P) + 2 (C - O)` with `rho = 1 + t`, for every support and
  every cube point, from PB19, `coeffF_nonneg` and `0 ≤ t`.
* PB21: `mixtureLaw`, the explicit mixture of independent rounding with weight
  `rho / (rho + 2)` and fair orientation rounding with weight `2 / (rho + 2)`.
  It is **one law built from `rho` and the coordinate means alone**: neither the
  support nor the coefficients enter its definition.  `mixtureLaw_hasMeans` and
  `mixtureLaw_capture` state that it is feasible and that it captures at least
  `1 / (rho + 2)` of the gap of **every** physical monomial at once;
  `exists_common_mixture_law` is the same statement with the law quantified
  outside the support.
* PB22: `commonAspect_termwiseGap_le`, the polynomial bound
  `tbtgap ≤ (rho + 2) chgap` on `[1, rho]^n` for an arbitrary multilinear
  polynomial with nonnegative coefficients, and `commonAspect_termwiseGap_le_four`
  its specialization to the constant `4` on `[1,2]^n`.
* PB25: `positiveBoxAspectBound_add_two`, obtained from PB22 by direct
  application of `originalBox_bound_of_commonAspect_bound`.  No nondegeneracy
  hypothesis is needed: the transfer uses only surjectivity of the affine map,
  so fixed coordinates are allowed.
-/

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-! ## Expectation helpers -/

private theorem expect_finsetSum {κ : Type*} (μ : Law (Vertex I)) (u : Finset κ)
    (f : κ → Vertex I → ℝ) :
    μ.expect (fun v => ∑ k ∈ u, f k v) = ∑ k ∈ u, μ.expect (f k) := by
  simp only [Law.expect, Finset.mul_sum]
  exact Finset.sum_comm

private theorem expect_mix (μ ν : Law (Vertex I)) (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hab : a + b = 1) (f : Vertex I → ℝ) :
    (Law.mix μ ν a b ha hb hab).expect f = a * μ.expect f + b * ν.expect f := by
  simp only [Law.expect, Law.mix, add_mul, Finset.sum_add_distrib, Finset.mul_sum,
    mul_assoc]

/-- Two feasible laws never differ by more than the exact envelope width. -/
private theorem expect_sub_le_hullGap (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (x : I → ℝ) (μ ν : Law (Vertex I)) (hμ : HasMeans μ x) (hν : HasMeans ν x) :
    μ.expect (fun v => f (vertexPoint v)) - ν.expect (fun v => f (vertexPoint v)) ≤
      hullGap f x := by
  have hcom := envelopeValues_isCompact f hf x
  have hmu : μ.expect (fun v => f (vertexPoint v)) ∈ envelopeValues f x :=
    (mem_cubeGraph_hull_iff f hf x _).mpr ⟨μ, hμ, rfl⟩
  have hnu : ν.expect (fun v => f (vertexPoint v)) ∈ envelopeValues f x :=
    (mem_cubeGraph_hull_iff f hf x _).mpr ⟨ν, hν, rfl⟩
  have h1 := le_csSup hcom.bddAbove hmu
  have h2 := csInf_le hcom.bddBelow hnu
  rw [hullGap]
  linarith

/-! ## The four generating polynomials -/

/-- `O(t)`, the fair endpoint-orientation expectation of the physical monomial. -/
def physOrient (t : ℝ) (s : Finset I) (x : I → ℝ) : ℝ :=
  (orientationLaw x).expect (fun v => physMonomial t s (vertexPoint v))

/-- `C(t) = ∑_{j = 0}^{n + 1} C_j t ^ j`, the common-threshold generating sum,
taken over the full range `j = 0, …, n + 1` used by PB19. -/
theorem sum_thresholdMoment (t : ℝ) (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    ∑ j ∈ Finset.range (s.card + 2), thresholdMoment s x (j : ℤ) * t ^ j =
      physUpper t s x := by
  rw [show s.card + 2 = s.card + 1 + 1 from rfl, Finset.sum_range_succ,
    thresholdMoment_of_card_lt s x (by push_cast; omega), zero_mul, add_zero,
    ← thresholdLaw_physMonomial t s x hx, expect_physMonomial_eq_sum_binomMoment]
  rfl

omit [Fintype I] [DecidableEq I] in
/-- `V(t) = ∑_{j = 0}^{n + 1} V_j t ^ j`, the minimal generating sum. -/
theorem sum_lowerMomentInt [Finite I] (t : ℝ) (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    ∑ j ∈ Finset.range (s.card + 2), lowerMomentInt s x (j : ℤ) * t ^ j =
      physLower t s x := by
  rw [show s.card + 2 = s.card + 1 + 1 from rfl, Finset.sum_range_succ,
    lowerMomentInt_of_card_lt s x hx (by push_cast; omega), zero_mul, add_zero,
    ← sum_binomMomentLower t s x hx]
  exact Finset.sum_congr rfl fun j _ => by rw [lowerMomentInt_natCast]

omit [Fintype I] [DecidableEq I] in
/-- `P(t) = ∑_{j = 0}^{n + 1} P_j t ^ j`, the independent generating sum: it is
the physical monomial evaluated at the means. -/
theorem sum_elementaryInt [Finite I] (t : ℝ) (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    ∑ j ∈ Finset.range (s.card + 2), elementaryInt s x (j : ℤ) * t ^ j =
      physMonomial t s x := by
  classical
  let _ := Fintype.ofFinite I
  rw [show s.card + 2 = s.card + 1 + 1 from rfl, Finset.sum_range_succ,
    elementaryInt_of_card_lt s x (by push_cast; omega), zero_mul, add_zero,
    ← bernoulliLaw_physMonomial t s x hx, expect_physMonomial_eq_sum_binomMoment]
  exact Finset.sum_congr rfl fun j _ => by
    rw [elementaryInt_eq_binomMoment s x hx]

/-- `O(t) = ∑_{j = 0}^{n + 1} O_j t ^ j`, the orientation generating sum. -/
theorem sum_orientMoment (t : ℝ) (s : Finset I) (x : I → ℝ) :
    ∑ j ∈ Finset.range (s.card + 2), orientMoment s x (j : ℤ) * t ^ j =
      physOrient t s x := by
  rw [show s.card + 2 = s.card + 1 + 1 from rfl, Finset.sum_range_succ,
    orientMoment_of_card_lt s x (by push_cast; omega), zero_mul, add_zero, physOrient,
    orientationLaw_physMonomial_eq_sum]

/-! ## PB19: the coefficient of `t ^ j` is exactly `F_{n,j}`

The index bookkeeping is the whole content.  Multiplying a degree-`n` moment sum
by `2 + t` or `1 + t` shifts one copy of it up by one order, so the combination
has degree `n + 1` and the shifted copies contribute `C_{j-1}` and `P_{j-1}`.
The shift lemma below is where the two ends are checked: the order `-1` term
vanishes because all four families vanish at negative orders, and the order
`n + 2` term vanishes because they all vanish above order `n + 1`. -/

/-- Multiplying a moment generating sum by `t` reindexes it, provided the family
vanishes at order `-1` and at the top order `N` of the range. -/
private theorem sum_shift_mul (N : ℕ) (M : ℤ → ℝ) (t : ℝ)
    (hneg : M (-1) = 0) (htop : M (N : ℤ) = 0) :
    (∑ j ∈ Finset.range (N + 1), M (j : ℤ) * t ^ j) * t =
      ∑ j ∈ Finset.range (N + 1), M ((j : ℤ) - 1) * t ^ j := by
  rw [Finset.sum_mul, Finset.sum_range_succ, htop, zero_mul, zero_mul, add_zero,
    Finset.sum_range_succ' (fun j => M ((j : ℤ) - 1) * t ^ j) N]
  simp only [Nat.cast_zero, zero_sub, hneg, zero_mul, add_zero]
  refine Finset.sum_congr rfl fun j _ => ?_
  have hj : ((j + 1 : ℕ) : ℤ) - 1 = (j : ℤ) := by push_cast; ring
  rw [hj, pow_succ]
  ring

/-- **PB19**: the coefficient of `t ^ j` in `(2 + t) C + V - (1 + t) P - 2 O` is
exactly `F_{n,j}`, with no lost top-degree term.  The range `j = 0, …, n + 1` is
essential: the order `n + 1` coefficient is `C_n - P_n = F_{n,n+1}`, generically
nonzero. -/
theorem physCombination_eq_sum_coeffF (t : ℝ) (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) :
    (2 + t) * physUpper t s x + physLower t s x - (1 + t) * physMonomial t s x -
        2 * physOrient t s x =
      ∑ j ∈ Finset.range (s.card + 2), coeffF s x (j : ℤ) * t ^ j := by
  have hr : s.card + 1 + 1 = s.card + 2 := rfl
  have hCs := sum_shift_mul (s.card + 1) (thresholdMoment s x) t
    (thresholdMoment_of_neg s x (by norm_num))
    (thresholdMoment_of_card_lt s x (by push_cast; omega))
  have hPs := sum_shift_mul (s.card + 1) (elementaryInt s x) t
    (elementaryInt_of_neg s x (by norm_num))
    (elementaryInt_of_card_lt s x (by push_cast; omega))
  rw [hr] at hCs hPs
  have hsplit : ∑ j ∈ Finset.range (s.card + 2), coeffF s x (j : ℤ) * t ^ j =
      2 * (∑ j ∈ Finset.range (s.card + 2), thresholdMoment s x (j : ℤ) * t ^ j) +
          (∑ j ∈ Finset.range (s.card + 2), lowerMomentInt s x (j : ℤ) * t ^ j) -
          (∑ j ∈ Finset.range (s.card + 2), elementaryInt s x (j : ℤ) * t ^ j) -
          2 * (∑ j ∈ Finset.range (s.card + 2), orientMoment s x (j : ℤ) * t ^ j) +
          (∑ j ∈ Finset.range (s.card + 2), thresholdMoment s x ((j : ℤ) - 1) * t ^ j) -
          ∑ j ∈ Finset.range (s.card + 2), elementaryInt s x ((j : ℤ) - 1) * t ^ j := by
    simp only [Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun j _ => by rw [coeffF]; ring
  rw [hsplit, ← hCs, ← hPs, sum_thresholdMoment t s x hx, sum_lowerMomentInt t s x hx,
    sum_elementaryInt t s x hx, sum_orientMoment t s x]
  ring

/-! ## PB20: the physical-box inequality -/

/-- **PB20**, equation (7): `C - V ≤ rho (C - P) + 2 (C - O)` with `rho = 1 + t`,
for every physical monomial and every point of the cube.  This is PB19 together
with `coeffF_nonneg` and `0 ≤ t`. -/
theorem physUpper_sub_physLower_le (t : ℝ) (ht : 0 ≤ t) (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) :
    physUpper t s x - physLower t s x ≤
      (1 + t) * (physUpper t s x - physMonomial t s x) +
        2 * (physUpper t s x - physOrient t s x) := by
  have h : (0 : ℝ) ≤ ∑ j ∈ Finset.range (s.card + 2), coeffF s x (j : ℤ) * t ^ j :=
    Finset.sum_nonneg fun j _ => mul_nonneg (coeffF_nonneg s x hx _) (pow_nonneg ht _)
  rw [← physCombination_eq_sum_coeffF t s x hx] at h
  linarith

/-! ## PB21: one support-independent mixture -/

/-- **PB21**: the rounding mixture of independent Bernoulli rounding with weight
`rho / (rho + 2)` and fair endpoint-orientation rounding with weight
`2 / (rho + 2)`.  It is a single law on all coordinates, built from `rho` and the
coordinate means `x` alone: no support and no coefficient vector occurs in its
definition. -/
def mixtureLaw (rho : ℝ) (hrho : 1 ≤ rho) (x : I → ℝ) (hx : x ∈ cube I) :
    Law (Vertex I) :=
  Law.mix (bernoulliLaw x hx) (orientationLaw x) (rho / (rho + 2)) (2 / (rho + 2))
    (div_nonneg (by linarith) (by linarith)) (div_nonneg (by norm_num) (by linarith))
    (by
      have h2 : rho + 2 ≠ 0 := ne_of_gt (by linarith)
      field_simp)

/-- The mixture is feasible: it has the prescribed coordinate means. -/
theorem mixtureLaw_hasMeans (rho : ℝ) (hrho : 1 ≤ rho) (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (mixtureLaw rho hrho x hx) x := by
  have h2 : rho + 2 ≠ 0 := ne_of_gt (by linarith)
  intro i
  rw [mixtureLaw, expect_mix, bernoulliLaw_hasMeans x hx i, orientationLaw_hasMeans x hx i]
  field_simp

/-- The mixture's expectation of a physical monomial is the corresponding convex
combination of the independent and orientation values. -/
theorem mixtureLaw_expect_physMonomial (rho : ℝ) (hrho : 1 ≤ rho) (x : I → ℝ)
    (hx : x ∈ cube I) (s : Finset I) :
    (mixtureLaw rho hrho x hx).expect
        (fun v => physMonomial (rho - 1) s (vertexPoint v)) =
      rho / (rho + 2) * physMonomial (rho - 1) s x +
        2 / (rho + 2) * physOrient (rho - 1) s x := by
  rw [mixtureLaw, expect_mix, bernoulliLaw_physMonomial _ s x hx, physOrient]

/-- **PB21**: the one mixture captures at least `1 / (rho + 2)` of the exact gap
of **every** physical monomial, simultaneously.  The law is fixed before the
support `s` is chosen. -/
theorem mixtureLaw_capture (rho : ℝ) (hrho : 1 ≤ rho) (x : I → ℝ) (hx : x ∈ cube I)
    (s : Finset I) :
    hullGap (physMonomial (rho - 1) s) x / (rho + 2) ≤
      physUpper (rho - 1) s x -
        (mixtureLaw rho hrho x hx).expect
          (fun v => physMonomial (rho - 1) s (vertexPoint v)) := by
  have h2 : (0 : ℝ) < rho + 2 := by linarith
  have ht : (0 : ℝ) ≤ rho - 1 := by linarith
  have hpb20 := physUpper_sub_physLower_le (rho - 1) ht s x hx
  have hone : (1 : ℝ) + (rho - 1) = rho := by ring
  rw [hone] at hpb20
  rw [physMonomial_hullGap _ ht s x hx, mixtureLaw_expect_physMonomial rho hrho x hx s,
    div_le_iff₀ h2]
  have hclear : (physUpper (rho - 1) s x -
      (rho / (rho + 2) * physMonomial (rho - 1) s x +
        2 / (rho + 2) * physOrient (rho - 1) s x)) * (rho + 2) =
      (rho + 2) * physUpper (rho - 1) s x - rho * physMonomial (rho - 1) s x -
        2 * physOrient (rho - 1) s x := by
    field_simp
    ring
  rw [hclear]
  linarith

/-- **PB21**, with the law quantified outside the support: one feasible law
captures at least `1 / (rho + 2)` of the gap of every physical monomial. -/
theorem exists_common_mixture_law (rho : ℝ) (hrho : 1 ≤ rho) (x : I → ℝ)
    (hx : x ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧ ∀ s : Finset I,
      hullGap (physMonomial (rho - 1) s) x / (rho + 2) ≤
        physUpper (rho - 1) s x -
          μ.expect (fun v => physMonomial (rho - 1) s (vertexPoint v)) :=
  ⟨mixtureLaw rho hrho x hx, mixtureLaw_hasMeans rho hrho x hx,
    fun s => mixtureLaw_capture rho hrho x hx s⟩

/-! ## PB22: the polynomial bound on `[1, rho]^n` -/

omit [Fintype I] [DecidableEq I] in
/-- In cube coordinates the monomial of the box `[1, rho]^n` is the physical
monomial with shift `t = rho - 1`. -/
theorem monomial_boxPoint_eq_physMonomial (rho : ℝ) (s : Finset I) (q : I → ℝ) :
    monomial s (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q) =
      physMonomial (rho - 1) s q := rfl

omit [Fintype I] [DecidableEq I] in
/-- **PB22**: on `[1, rho]^n` the termwise relaxation gap of an arbitrary
multilinear polynomial with nonnegative coefficients is at most `rho + 2` times
its exact hull gap. -/
theorem commonAspect_termwiseGap_le [Finite I] (rho : ℝ) (hrho : 1 ≤ rho)
    (T : Finset (Finset I)) (b : Finset I → ℝ) (y : I → ℝ) (hb : ∀ s ∈ T, 0 ≤ b s)
    (hy : y ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) :
    boxTermwiseGap T b (fun _ => (1 : ℝ)) (fun _ => rho) y ≤
      (rho + 2) * boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (supportPolynomial T b) y := by
  classical
  let _ := Fintype.ofFinite I
  have ht : (0 : ℝ) ≤ rho - 1 := by linarith
  have h2 : (0 : ℝ) ≤ rho + 2 := by linarith
  have hlu : ∀ _ : I, (1 : ℝ) ≤ rho := fun _ => hrho
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) hlu y hy
  set t : ℝ := rho - 1 with htdef
  set F : (I → ℝ) → ℝ := fun q => ∑ s ∈ T, b s * physMonomial t s q with hFdef
  have haff : SeparatelyAffine F := by
    refine separatelyAffine_sum T (fun s q => b s * physMonomial t s q) fun s _ q i r => ?_
    dsimp only
    rw [physMonomial_coordinate_affine t s q i r]
    ring
  have hpoly : (fun q => supportPolynomial T b
      (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q)) = F := by
    funext q
    exact Finset.sum_congr rfl fun s _ => by
      rw [monomial_boxPoint_eq_physMonomial rho s q]
  -- the termwise gap in cube coordinates
  have hterm : boxTermwiseGap T b (fun _ => (1 : ℝ)) (fun _ => rho)
      (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) =
      ∑ s ∈ T, b s * (physUpper t s p - physLower t s p) := by
    refine Finset.sum_congr rfl fun s _ => ?_
    rw [boxHullGap_eq_of_mem _ _ hlu _ p hp]
    congr 1
    rw [show (fun q => monomial s (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q)) =
      physMonomial t s from rfl]
    exact physMonomial_hullGap t ht s p hp
  -- the two feasible laws
  have hCexp : (thresholdLaw p).expect (fun v => F (vertexPoint v)) =
      ∑ s ∈ T, b s * physUpper t s p := by
    rw [hFdef]
    rw [expect_finsetSum (thresholdLaw p) T (fun s v => b s * physMonomial t s (vertexPoint v))]
    exact Finset.sum_congr rfl fun s _ => by
      rw [Law.expect_const_mul, thresholdLaw_physMonomial t s p hp]
  have hMexp : (mixtureLaw rho hrho p hp).expect (fun v => F (vertexPoint v)) =
      ∑ s ∈ T, b s * (mixtureLaw rho hrho p hp).expect
        (fun v => physMonomial t s (vertexPoint v)) := by
    rw [hFdef]
    rw [expect_finsetSum (mixtureLaw rho hrho p hp) T
      (fun s v => b s * physMonomial t s (vertexPoint v))]
    exact Finset.sum_congr rfl fun s _ => by rw [Law.expect_const_mul]
  have hgap : (∑ s ∈ T, b s * physUpper t s p) -
      (∑ s ∈ T, b s * (mixtureLaw rho hrho p hp).expect
        (fun v => physMonomial t s (vertexPoint v))) ≤ hullGap F p := by
    rw [← hCexp, ← hMexp]
    exact expect_sub_le_hullGap F haff p _ _ (thresholdLaw_hasMeans p hp)
      (mixtureLaw_hasMeans rho hrho p hp)
  -- assemble
  have hstep : ∑ s ∈ T, b s * (physUpper t s p - physLower t s p) ≤
      (rho + 2) * ((∑ s ∈ T, b s * physUpper t s p) -
        ∑ s ∈ T, b s * (mixtureLaw rho hrho p hp).expect
          (fun v => physMonomial t s (vertexPoint v))) := by
    rw [mul_sub, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib]
    refine Finset.sum_le_sum fun s hs => ?_
    have hcap := mixtureLaw_capture rho hrho p hp s
    rw [physMonomial_hullGap _ ht s p hp, div_le_iff₀ (by linarith : (0 : ℝ) < rho + 2)] at hcap
    have : physUpper t s p - physLower t s p ≤
        (rho + 2) * (physUpper t s p - (mixtureLaw rho hrho p hp).expect
          (fun v => physMonomial t s (vertexPoint v))) := by
      rw [htdef]; linarith [hcap]
    calc b s * (physUpper t s p - physLower t s p)
        ≤ b s * ((rho + 2) * (physUpper t s p - (mixtureLaw rho hrho p hp).expect
            (fun v => physMonomial t s (vertexPoint v)))) :=
          mul_le_mul_of_nonneg_left this (hb s hs)
      _ = (rho + 2) * (b s * physUpper t s p) -
            (rho + 2) * (b s * (mixtureLaw rho hrho p hp).expect
              (fun v => physMonomial t s (vertexPoint v))) := by ring
  rw [hterm, boxHullGap_eq_of_mem _ _ hlu _ p hp, hpoly]
  exact hstep.trans (mul_le_mul_of_nonneg_left hgap h2)

omit [Fintype I] [DecidableEq I] in
/-- **PB22**, specialization: the constant on `[1,2]^n` is four. -/
theorem commonAspect_termwiseGap_le_four [Finite I] (T : Finset (Finset I)) (b : Finset I → ℝ)
    (y : I → ℝ) (hb : ∀ s ∈ T, 0 ≤ b s)
    (hy : y ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ))) :
    boxTermwiseGap T b (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) y ≤
      4 * boxHullGap (fun _ => (1 : ℝ)) (fun _ => (2 : ℝ)) (supportPolynomial T b) y := by
  have h := commonAspect_termwiseGap_le (2 : ℝ) (by norm_num) T b y hb hy
  norm_num at h
  exact h

/-! ## PB25: every strictly positive box of aspect ratio at most `rho` -/

/-- **PB25**: `tbtgap_B f ≤ (rho + 2) chgap_B f` on every strictly positive box
whose coordinate aspect ratios are at most `rho`.  Obtained from PB22 by direct
application of `originalBox_bound_of_commonAspect_bound`; no nondegeneracy
hypothesis is required, so fixed coordinates need not be removed. -/
theorem positiveBoxAspectBound_add_two {rho : ℝ} (hrho : 1 < rho) :
    PositiveBoxAspectBound rho (rho + 2) := by
  refine originalBox_bound_of_commonAspect_bound hrho ?_
  intro K _ _ T b y hb hy
  exact commonAspect_termwiseGap_le rho hrho.le T b y hb hy

end

end MultilinearGap
