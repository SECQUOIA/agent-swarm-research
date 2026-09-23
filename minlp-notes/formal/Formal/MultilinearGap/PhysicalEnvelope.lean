import Formal.MultilinearGap.GeneralGaps
import Formal.CubicGap.Counts

/-!
# Exact envelopes of the physical monomial on a positive interval

This module computes the two exact envelopes of the *physical* monomial

`physMonomial t s y = ∏ i ∈ s, (1 + t * y i)`

over the unit cube, for a shift parameter `t ≥ 0`.  Writing `rho = 1 + t`, the
normalization `x i = 1 + t * y i` carries `[0,1]^n` onto `[1, rho]^n`, so
`physMonomial t s` is the monomial `∏ i ∈ s, x i` read in cube coordinates; at a
binary point with `K` successes inside `s` its value is `rho ^ K`.

The results are the positive-box obligations PB05, PB06, PB10, PB11 and PB12:

* `physMonomial_maximum` (PB05): the concave envelope is
  `∑ A ⊆ s, t ^ |A| * monomialUpper A x`, attained by the common-threshold law
  `thresholdLaw x` **simultaneously for every support** `s`.
* `bernoulliLaw_physMonomial` (PB06): independent rounding reproduces the
  product `∏ i ∈ s, (1 + t * x i)`, and its binomial moments are the elementary
  symmetric polynomials of `x` on `s`.
* `exists_adjacentLaw` (PB10): an explicit law with the prescribed means whose
  success count on `s` lives on the two adjacent integers `⌊S⌋` and `⌊S⌋ + 1`,
  where `S = ∑ i ∈ s, x i`.
* `physMonomial_minimum` (PB11): the convex envelope is **exactly**
  `rho ^ ⌊S⌋ * (1 + (rho - 1) * (S - ⌊S⌋))`, both bounded below for every law
  and attained by the adjacent-count law.
* `binomMoment_zero`, `binomMoment_of_neg`, `binomMoment_of_card_lt` (PB12): the
  moment conventions, stated once for the binomial moments of an arbitrary law
  and therefore valid uniformly for all four rounding families.

The cube monomial results `positive_polynomial_maximum_general` and
`monomial_minimum` are about `∏ i ∈ s, y i`, a different objective with a
different envelope; only their proof ideas and the law definitions are reused.
-/

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*}

/-! ## The physical monomial and its binary values -/

/-- The number of successful coordinates of a binary point inside `s`. -/
def countOn (s : Finset I) (v : Vertex I) : ℕ := (s.filter fun i => v i = true).card

/-- The success count on `s` never exceeds the size of `s`. -/
theorem countOn_le_card (s : Finset I) (v : Vertex I) : countOn s v ≤ s.card :=
  Finset.card_filter_le _ _

/-- The empty support carries no successes. -/
@[simp] theorem countOn_empty (v : Vertex I) : countOn (∅ : Finset I) v = 0 := by
  simp [countOn]

/-- On the full index set the restricted count is the ambient success count. -/
theorem countOn_univ [Fintype I] (v : Vertex I) : countOn Finset.univ v = count v := rfl

/-- The success count on `s` is the sum of the binary coordinates of `s`. -/
theorem countOn_eq_sum (s : Finset I) (v : Vertex I) :
    ((countOn s v : ℕ) : ℝ) = ∑ i ∈ s, vertexPoint v i := by
  simp [countOn, vertexPoint, Finset.sum_boole]

/-- The physical monomial `∏ i ∈ s, (1 + t * y i)`, the image of the ordinary
monomial under the affine map `[0,1] → [1, 1 + t]`. -/
def physMonomial (t : ℝ) (s : Finset I) (y : I → ℝ) : ℝ := ∏ i ∈ s, (1 + t * y i)

/-- The empty physical monomial is the constant one. -/
@[simp] theorem physMonomial_empty (t : ℝ) (y : I → ℝ) :
    physMonomial t (∅ : Finset I) y = 1 := by simp [physMonomial]

/-- Updating a coordinate of the support splits off its own factor. -/
theorem physMonomial_update_of_mem [DecidableEq I] (t : ℝ) {s : Finset I} {i : I}
    (hi : i ∈ s) (y : I → ℝ) (r : ℝ) :
    physMonomial t s (Function.update y i r) =
      (1 + t * r) * ∏ j ∈ s.erase i, (1 + t * y j) := by
  rw [physMonomial, ← Finset.mul_prod_erase s _ hi, Function.update_self]
  congr 1
  exact Finset.prod_congr rfl fun j hj => by
    rw [Function.update_of_ne (Finset.ne_of_mem_erase hj)]

/-- Updating a coordinate outside the support changes nothing. -/
theorem physMonomial_update_of_notMem [DecidableEq I] (t : ℝ) {s : Finset I} {i : I}
    (hi : i ∉ s) (y : I → ℝ) (r : ℝ) :
    physMonomial t s (Function.update y i r) = physMonomial t s y :=
  Finset.prod_congr rfl fun j hj => by
    rw [Function.update_of_ne (by rintro rfl; exact hi hj)]

/-- The physical monomial is affine in each coordinate separately. -/
theorem physMonomial_coordinate_affine [DecidableEq I] (t : ℝ) (s : Finset I) :
    SeparatelyAffine (physMonomial t s) := by
  intro y i r
  by_cases hi : i ∈ s
  · rw [physMonomial_update_of_mem t hi, physMonomial_update_of_mem t hi,
      physMonomial_update_of_mem t hi]
    ring
  · rw [physMonomial_update_of_notMem t hi, physMonomial_update_of_notMem t hi,
      physMonomial_update_of_notMem t hi]
    ring

/-- PB03, binary half: at a binary point the physical monomial is `(1 + t) ^ K`
with `K` the number of successes inside the support. -/
theorem physMonomial_vertex (t : ℝ) (s : Finset I) (v : Vertex I) :
    physMonomial t s (vertexPoint v) = (1 + t) ^ countOn s v := by
  have hfac : ∀ i ∈ s, (1 + t * vertexPoint v i) = if v i = true then 1 + t else 1 := by
    intro i _
    cases hv : v i <;> simp [vertexPoint, hv]
  rw [physMonomial, Finset.prod_congr rfl hfac, Finset.prod_ite, Finset.prod_const,
    Finset.prod_const_one, mul_one]
  rfl

/-- The multilinear expansion of the physical monomial into ordinary monomials. -/
theorem physMonomial_expand (t : ℝ) (s : Finset I) (y : I → ℝ) :
    physMonomial t s y = ∑ A ∈ s.powerset, t ^ A.card * monomial A y := by
  classical
  have h := Finset.prod_add (fun i => t * y i) (fun _ => (1 : ℝ)) s
  have hl : ∏ i ∈ s, (t * y i + (1 : ℝ)) = physMonomial t s y :=
    Finset.prod_congr rfl fun i _ => by ring
  rw [hl] at h
  rw [h]
  refine Finset.sum_congr rfl fun A _ => ?_
  rw [Finset.prod_const_one, mul_one, Finset.prod_mul_distrib, Finset.prod_const]
  rfl

/-! ## Support means, the two adjacent counts, and discrete convexity -/

/-- The sum of the prescribed means over the support, `S = ∑ i ∈ s, u i`. -/
def meanSum (s : Finset I) (x : I → ℝ) : ℝ := ∑ i ∈ s, x i

/-- The lower of the two adjacent success counts, `⌊S⌋`. -/
def countFloor (s : Finset I) (x : I → ℝ) : ℕ := ⌊meanSum s x⌋₊

/-- The fractional part `S - ⌊S⌋`, the weight carried by the upper count. -/
def countFrac (s : Finset I) (x : I → ℝ) : ℝ := meanSum s x - (countFloor s x : ℝ)

/-- The convex envelope value of the physical monomial: with `rho = 1 + t` it is
`rho ^ ⌊S⌋ * (1 + (rho - 1) * (S - ⌊S⌋))`. -/
def physLower (t : ℝ) (s : Finset I) (x : I → ℝ) : ℝ :=
  (1 + t) ^ countFloor s x * (1 + countFrac s x * t)

/-- On the cube the support mean sum is nonnegative. -/
theorem meanSum_nonneg {s : Finset I} {x : I → ℝ} (hx : x ∈ cube I) : 0 ≤ meanSum s x :=
  Finset.sum_nonneg fun i _ => (hx i).1

/-- The lower adjacent count does not exceed the mean sum. -/
theorem countFloor_le {s : Finset I} {x : I → ℝ} (hx : x ∈ cube I) :
    (countFloor s x : ℝ) ≤ meanSum s x := Nat.floor_le (meanSum_nonneg hx)

/-- The upper count carries a nonnegative weight. -/
theorem countFrac_nonneg {s : Finset I} {x : I → ℝ} (hx : x ∈ cube I) :
    0 ≤ countFrac s x := sub_nonneg.mpr (countFloor_le hx)

/-- The upper count carries weight less than one. -/
theorem countFrac_lt_one (s : Finset I) (x : I → ℝ) : countFrac s x < 1 := by
  have h := Nat.lt_floor_add_one (meanSum s x)
  rw [countFrac, countFloor]
  linarith

/-- A function on the naturals with nondecreasing first differences lies above
every chord through two consecutive points, extended affinely in both
directions. This is the discrete supporting-line form of convexity. -/
theorem chord_le_of_convex (f : ℕ → ℝ)
    (hf : ∀ k, f (k + 1) - f k ≤ f (k + 2) - f (k + 1)) (m k : ℕ) :
    f m + ((k : ℝ) - m) * (f (m + 1) - f m) ≤ f k := by
  have hmono : Monotone (fun k => f (k + 1) - f k) := monotone_nat_of_le_succ (fun k => hf k)
  have hsum : ∀ a d : ℕ, f (a + d) - f a =
      ∑ i ∈ Finset.range d, (f (a + i + 1) - f (a + i)) := by
    intro a d
    induction d with
    | zero => simp
    | succ d ih =>
      have hstep : a + (d + 1) = a + d + 1 := by omega
      rw [Finset.sum_range_succ, ← ih, hstep]
      ring
  rcases le_total m k with h | h
  · obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le h
    have hlow : (Finset.range d).card • (f (m + 1) - f m) ≤
        ∑ i ∈ Finset.range d, (f (m + i + 1) - f (m + i)) :=
      Finset.card_nsmul_le_sum _ _ _ fun i _ => hmono (show m ≤ m + i by omega)
    rw [Finset.card_range, nsmul_eq_mul] at hlow
    have hd := hsum m d
    push_cast
    linarith
  · obtain ⟨e, rfl⟩ := Nat.exists_eq_add_of_le h
    have hhigh : ∑ i ∈ Finset.range e, (f (k + i + 1) - f (k + i)) ≤
        (Finset.range e).card • (f (k + e + 1) - f (k + e)) :=
      Finset.sum_le_card_nsmul _ _ _ fun i hi =>
        hmono (show k + i ≤ k + e by simp only [Finset.mem_range] at hi; omega)
    rw [Finset.card_range, nsmul_eq_mul] at hhigh
    have hd := hsum k e
    push_cast
    linarith

/-- Discrete convexity of `k ↦ (1 + t) ^ k` for `t ≥ 0`. -/
theorem pow_succ_convex {t : ℝ} (ht : 0 ≤ t) (k : ℕ) :
    (1 + t) ^ (k + 1) - (1 + t) ^ k ≤ (1 + t) ^ (k + 2) - (1 + t) ^ (k + 1) := by
  have h1 : (1 : ℝ) ≤ 1 + t := by linarith
  have h : (1 + t) ^ k ≤ (1 + t) ^ (k + 1) := pow_le_pow_right₀ h1 (Nat.le_succ k)
  have e1 : (1 + t) ^ (k + 1) - (1 + t) ^ k = (1 + t) ^ k * t := by ring
  have e2 : (1 + t) ^ (k + 2) - (1 + t) ^ (k + 1) = (1 + t) ^ (k + 1) * t := by ring
  rw [e1, e2]
  exact mul_le_mul_of_nonneg_right h ht

/-- Discrete convexity of `k ↦ binom (k, j)` for every order `j ≥ 1`, in
particular for the orders `j ≥ 2` that PB11 needs. -/
theorem choose_convex (j k : ℕ) :
    (((k + 1).choose (j + 1) : ℕ) : ℝ) - ((k.choose (j + 1) : ℕ) : ℝ) ≤
      (((k + 2).choose (j + 1) : ℕ) : ℝ) - (((k + 1).choose (j + 1) : ℕ) : ℝ) := by
  have h1 : (k + 1).choose (j + 1) = k.choose j + k.choose (j + 1) := Nat.choose_succ_succ k j
  have h2 : (k + 2).choose (j + 1) = (k + 1).choose j + (k + 1).choose (j + 1) :=
    Nat.choose_succ_succ (k + 1) j
  have hm : k.choose j ≤ (k + 1).choose j := Nat.choose_le_choose j (Nat.le_succ k)
  have h1' : (((k + 1).choose (j + 1) : ℕ) : ℝ) =
      ((k.choose j : ℕ) : ℝ) + ((k.choose (j + 1) : ℕ) : ℝ) := by exact_mod_cast h1
  have h2' : (((k + 2).choose (j + 1) : ℕ) : ℝ) =
      (((k + 1).choose j : ℕ) : ℝ) + (((k + 1).choose (j + 1) : ℕ) : ℝ) := by exact_mod_cast h2
  have hm' : ((k.choose j : ℕ) : ℝ) ≤ (((k + 1).choose j : ℕ) : ℝ) := by exact_mod_cast hm
  linarith

/-! ## Binomial moments and the order conventions (PB12) -/

/-- The binomial coefficient at an integer order. Order zero is one, negative
orders vanish, and orders above the first argument vanish. -/
def chooseInt (k : ℕ) (j : ℤ) : ℝ := if 0 ≤ j then (k.choose j.toNat : ℝ) else 0

/-- At a nonnegative order the integer-order coefficient is the usual one. -/
@[simp] theorem chooseInt_natCast (k j : ℕ) : chooseInt k (j : ℤ) = (k.choose j : ℝ) := by
  simp [chooseInt]

/-- PB12 at the scalar level: order zero is one. -/
@[simp] theorem chooseInt_zero (k : ℕ) : chooseInt k 0 = 1 := by simp [chooseInt]

/-- PB12 at the scalar level: negative orders are zero. -/
theorem chooseInt_of_neg (k : ℕ) {j : ℤ} (hj : j < 0) : chooseInt k j = 0 := by
  simp [chooseInt, not_le.mpr hj]

/-- PB12 at the scalar level: orders above the count are zero. -/
theorem chooseInt_of_lt {k : ℕ} {j : ℤ} (hj : (k : ℤ) < j) : chooseInt k j = 0 := by
  have h0 : (0 : ℤ) ≤ j := le_trans (Int.natCast_nonneg k) hj.le
  rw [chooseInt, if_pos h0, Nat.choose_eq_zero_of_lt (by omega), Nat.cast_zero]

variable [Fintype I] [DecidableEq I]

private theorem expect_finsetSum {κ : Type*} (μ : Law (Vertex I)) (u : Finset κ)
    (g : κ → Vertex I → ℝ) :
    μ.expect (fun v => ∑ k ∈ u, g k v) = ∑ k ∈ u, μ.expect (g k) := by
  simp only [Law.expect, Finset.mul_sum]
  rw [Finset.sum_comm]

/-- The `j`-th binomial moment `E binom(K, j)` of the success count on `s`. -/
def binomMoment (s : Finset I) (μ : Law (Vertex I)) (j : ℤ) : ℝ :=
  μ.expect fun v => chooseInt (countOn s v) j

/-- PB12: order zero is one. -/
@[simp] theorem binomMoment_zero (s : Finset I) (μ : Law (Vertex I)) :
    binomMoment s μ 0 = 1 := by simp [binomMoment]

/-- PB12: negative orders are zero. -/
theorem binomMoment_of_neg (s : Finset I) (μ : Law (Vertex I)) {j : ℤ} (hj : j < 0) :
    binomMoment s μ j = 0 := by simp [binomMoment, chooseInt_of_neg _ hj]

/-- PB12: orders above the dimension of the support vanish. -/
theorem binomMoment_of_card_lt (s : Finset I) (μ : Law (Vertex I)) {j : ℤ}
    (hj : (s.card : ℤ) < j) : binomMoment s μ j = 0 := by
  have h : ∀ v : Vertex I, chooseInt (countOn s v) j = 0 := fun v =>
    chooseInt_of_lt (lt_of_le_of_lt (by exact_mod_cast countOn_le_card s v) hj)
  simp [binomMoment, h]

/-- The first binomial moment of a law with prescribed means is the sum of the
means on the support. -/
theorem binomMoment_one (s : Finset I) (x : I → ℝ) (μ : Law (Vertex I))
    (hm : HasMeans μ x) : binomMoment s μ 1 = ∑ i ∈ s, x i := by
  have h : ∀ v : Vertex I, chooseInt (countOn s v) 1 = ∑ i ∈ s, vertexPoint v i := by
    intro v
    rw [show (1 : ℤ) = ((1 : ℕ) : ℤ) by norm_num, chooseInt_natCast,
      Nat.choose_one_right, countOn_eq_sum]
  simp only [binomMoment, h]
  rw [expect_finsetSum]
  exact Finset.sum_congr rfl fun i _ => hm i

/-- PB12, generating form: the physical monomial expectation is the binomial
moment generating sum, `E ∏ (1 + t Y) = ∑ j ≤ |s|, C_j t ^ j`. -/
theorem expect_physMonomial_eq_sum_binomMoment (t : ℝ) (s : Finset I)
    (μ : Law (Vertex I)) :
    μ.expect (fun v => physMonomial t s (vertexPoint v)) =
      ∑ j ∈ Finset.range (s.card + 1), binomMoment s μ (j : ℤ) * t ^ j := by
  have hpt : ∀ v : Vertex I, physMonomial t s (vertexPoint v) =
      ∑ j ∈ Finset.range (s.card + 1), chooseInt (countOn s v) (j : ℤ) * t ^ j := by
    intro v
    have hk : countOn s v ≤ s.card := countOn_le_card s v
    have hexp : (1 + t) ^ countOn s v =
        ∑ j ∈ Finset.range (countOn s v + 1),
          chooseInt (countOn s v) (j : ℤ) * t ^ j := by
      rw [add_comm, add_pow]
      exact Finset.sum_congr rfl fun j _ => by rw [chooseInt_natCast, one_pow, mul_one]; ring
    have hsub : Finset.range (countOn s v + 1) ⊆ Finset.range (s.card + 1) := by
      intro j hj
      simp only [Finset.mem_range] at hj ⊢
      omega
    rw [physMonomial_vertex, hexp]
    refine Finset.sum_subset hsub ?_
    intro j _ hj
    rw [Finset.mem_range, not_lt] at hj
    rw [chooseInt_natCast, Nat.choose_eq_zero_of_lt hj, Nat.cast_zero, zero_mul]
  simp only [hpt]
  rw [expect_finsetSum]
  exact Finset.sum_congr rfl fun j _ => by rw [binomMoment, ← Law.expect_mul_const]

/-! ## Restricted elementary symmetric polynomials -/

/-- The elementary symmetric polynomial of `x` over the subsets of `s`. -/
def elementaryOn (s : Finset I) (j : ℕ) (x : I → ℝ) : ℝ :=
  ∑ A ∈ s.powersetCard j, monomial A x

omit [DecidableEq I] in
/-- On the full index set the restricted elementary polynomial is the ordinary
elementary symmetric polynomial. -/
theorem elementaryOn_univ (j : ℕ) (x : I → ℝ) :
    elementaryOn Finset.univ j x = elementary j x := rfl

omit [Fintype I] [DecidableEq I] in
/-- At a binary point the restricted elementary polynomial counts the `j`-subsets
of the successful coordinates of `s`. -/
theorem elementaryOn_vertex (s : Finset I) (j : ℕ) (v : Vertex I) :
    elementaryOn s j (vertexPoint v) = ((countOn s v).choose j : ℝ) := by
  classical
  set T := s.filter (fun i => v i = true) with hT
  have hTs : T ⊆ s := Finset.filter_subset _ _
  have hprod : ∀ A ∈ s.powersetCard j,
      monomial A (vertexPoint v) = if A ⊆ T then (1 : ℝ) else 0 := by
    intro A hA
    have hAs : A ⊆ s := (Finset.mem_powersetCard.mp hA).1
    split_ifs with hAT
    · exact Finset.prod_eq_one fun i hi => by
        have := Finset.mem_filter.mp (hAT hi)
        simp [vertexPoint, this.2]
    · obtain ⟨i, hi, hv⟩ : ∃ i ∈ A, v i ≠ true := by
        by_contra! hh
        exact hAT fun i hi => Finset.mem_filter.mpr ⟨hAs hi, hh i hi⟩
      exact Finset.prod_eq_zero hi (by simp [vertexPoint, hv])
  have hfilter : (s.powersetCard j).filter (fun A => A ⊆ T) = T.powersetCard j := by
    ext A
    simp only [Finset.mem_filter, Finset.mem_powersetCard]
    exact ⟨fun h => ⟨h.2, h.1.2⟩, fun h => ⟨⟨h.1.trans hTs, h.2⟩, h.1⟩⟩
  rw [elementaryOn, Finset.sum_congr rfl hprod, Finset.sum_boole, hfilter,
    Finset.card_powersetCard]
  rfl

/-- The binomial moments are the expectations of the restricted elementary
symmetric polynomial, hence sums of ordinary monomial expectations. -/
theorem binomMoment_eq_sum_monomial (s : Finset I) (μ : Law (Vertex I)) (j : ℕ) :
    binomMoment s μ (j : ℤ) =
      ∑ A ∈ s.powersetCard j, μ.expect (fun v => monomial A (vertexPoint v)) := by
  have h : ∀ v : Vertex I, chooseInt (countOn s v) (j : ℤ) =
      ∑ A ∈ s.powersetCard j, monomial A (vertexPoint v) := by
    intro v; rw [chooseInt_natCast, ← elementaryOn_vertex]; rfl
  simp only [binomMoment, h]
  exact expect_finsetSum μ _ _

/-! ## PB05: common-threshold rounding attains every physical maximum -/

/-- The concave envelope value of the physical monomial: the multilinear
expansion evaluated at the ordinary monomial maxima. -/
def physUpper (t : ℝ) (s : Finset I) (x : I → ℝ) : ℝ :=
  ∑ A ∈ s.powerset, t ^ A.card * monomialUpper A x

/-- Every law expands the physical monomial expectation into the ordinary
monomial expectations. -/
theorem expect_physMonomial_expand (t : ℝ) (s : Finset I) (μ : Law (Vertex I)) :
    μ.expect (fun v => physMonomial t s (vertexPoint v)) =
      ∑ A ∈ s.powerset, t ^ A.card * μ.expect (fun v => monomial A (vertexPoint v)) := by
  simp only [physMonomial_expand]
  rw [expect_finsetSum]
  exact Finset.sum_congr rfl fun A _ => by rw [Law.expect_const_mul]

/-- No law with the prescribed means exceeds the physical concave envelope. -/
theorem physMonomial_expect_le (t : ℝ) (ht : 0 ≤ t) (s : Finset I) (x : I → ℝ)
    (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    μ.expect (fun v => physMonomial t s (vertexPoint v)) ≤ physUpper t s x := by
  rw [expect_physMonomial_expand, physUpper]
  exact Finset.sum_le_sum fun A _ =>
    mul_le_mul_of_nonneg_left (monomial_expect_le_upper A x μ hm) (pow_nonneg ht _)

/-- The common-threshold law attains the physical concave envelope. -/
theorem thresholdLaw_physMonomial (t : ℝ) (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    (thresholdLaw x).expect (fun v => physMonomial t s (vertexPoint v)) = physUpper t s x := by
  rw [expect_physMonomial_expand, physUpper]
  exact Finset.sum_congr rfl fun A _ => by rw [thresholdLaw_monomial_upper A x hx]

/-- PB05: one common-threshold law simultaneously maximizes every positive
physical monomial among all laws with the prescribed means. -/
theorem thresholdLaw_maximizes_physMonomial (x : I → ℝ) (hx : x ∈ cube I)
    (t : ℝ) (ht : 0 ≤ t) (s : Finset I) (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    μ.expect (fun v => physMonomial t s (vertexPoint v)) ≤
      (thresholdLaw x).expect (fun v => physMonomial t s (vertexPoint v)) := by
  rw [thresholdLaw_physMonomial t s x hx]
  exact physMonomial_expect_le t ht s x μ hm

omit [Fintype I] [DecidableEq I] in
/-- PB05: the exact concave envelope of the physical monomial, attained by the
common-threshold law. -/
theorem physMonomial_maximum [Finite I] (t : ℝ) (ht : 0 ≤ t) (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) :
    IsGreatest (envelopeValues (physMonomial t s) x) (physUpper t s x) := by
  classical
  let := Fintype.ofFinite I
  apply maximum_from_laws _ (physMonomial_coordinate_affine t s)
  · exact fun μ hm => physMonomial_expect_le t ht s x μ hm
  · exact ⟨thresholdLaw x, thresholdLaw_hasMeans x hx, thresholdLaw_physMonomial t s x hx⟩

/-- PB05, moments: the binomial moments of the common-threshold law are the sums
of subset minima, `C_j(u) = ∑_{A ⊆ s, |A| = j} min_{i ∈ A} u i`. -/
theorem thresholdLaw_binomMoment (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) (j : ℕ) :
    binomMoment s (thresholdLaw x) (j : ℤ) = ∑ A ∈ s.powersetCard j, monomialUpper A x := by
  rw [binomMoment_eq_sum_monomial]
  exact Finset.sum_congr rfl fun A _ => thresholdLaw_monomial_upper A x hx

/-! ## PB06: independent Bernoulli rounding -/

/-- PB06: independent rounding reproduces the physical monomial at the means. -/
theorem bernoulliLaw_physMonomial (t : ℝ) (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    (bernoulliLaw x hx).expect (fun v => physMonomial t s (vertexPoint v)) =
      physMonomial t s x := by
  have hprodEq : ∀ y : I → ℝ, physMonomial t s y = ∏ i, (if i ∈ s then 1 + t * y i else 1) := by
    intro y
    have h := Finset.prod_ite_mem (Finset.univ : Finset I) s (fun i => 1 + t * y i)
    rw [Finset.univ_inter] at h
    exact h.symm
  have hL : (bernoulliLaw x hx).expect (fun v => physMonomial t s (vertexPoint v)) =
      (bernoulliLaw x hx).expect (fun v => ∏ i, (fun (i : I) (b : Bool) =>
        if i ∈ s then 1 + t * (if b then (1 : ℝ) else 0) else 1) i (v i)) := by
    simp only [Law.expect]
    refine Finset.sum_congr rfl fun v _ => ?_
    rw [hprodEq (vertexPoint v)]
    rfl
  rw [hL, bernoulliLaw_expect_prod x hx (fun (i : I) (b : Bool) =>
    if i ∈ s then 1 + t * (if b then (1 : ℝ) else 0) else 1), hprodEq x]
  refine Finset.prod_congr rfl fun i _ => ?_
  by_cases hi : i ∈ s
  · rw [if_pos hi, if_pos hi, if_pos hi]
    change (1 - x i) * (1 + t * 0) + x i * (1 + t * 1) = 1 + t * x i
    ring
  · rw [if_neg hi, if_neg hi, if_neg hi]
    ring

/-- PB06, moments: the binomial moments of independent rounding are the
elementary symmetric polynomials of the means on the support. -/
theorem bernoulliLaw_binomMoment (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) (j : ℕ) :
    binomMoment s (bernoulliLaw x hx) (j : ℤ) = elementaryOn s j x := by
  rw [binomMoment_eq_sum_monomial]
  exact Finset.sum_congr rfl fun A _ => bernoulliLaw_expect_monomial x hx A

/-! ## PB10: the adjacent-count rounding law

The route taken here is the direct construction of the law, not a proof that the
slab polytope is integral: the coordinates of the support are added one at a
time to an independent base law, and each new coordinate is coupled to the
current success count so that the count stays on two adjacent integers. -/

private def splitLaw (μ : Law (Vertex I)) (q : Vertex I → ℝ)
    (hq : ∀ v, 0 ≤ q v ∧ q v ≤ 1) : Law (Vertex I × Bool) where
  weight p := μ.weight p.1 * (if p.2 then q p.1 else 1 - q p.1)
  nonneg p := mul_nonneg (μ.nonneg _) (by
    cases p.2
    · exact sub_nonneg.mpr (hq _).2
    · exact (hq _).1)
  mass_one := by
    simp only [Fintype.sum_prod_type, Fintype.sum_bool]
    convert μ.mass_one using 1
    apply Finset.sum_congr rfl
    intro v _
    simp
    ring

private theorem splitLaw_expect (μ : Law (Vertex I)) (q : Vertex I → ℝ)
    (hq : ∀ v, 0 ≤ q v ∧ q v ≤ 1) (f : Vertex I × Bool → ℝ) :
    (splitLaw μ q hq).expect f =
      μ.expect (fun v => (1 - q v) * f (v, false) + q v * f (v, true)) := by
  simp only [Law.expect, splitLaw, Fintype.sum_prod_type, Fintype.sum_bool]
  apply Finset.sum_congr rfl
  intro v _
  simp
  ring

/-- Resample coordinate `a` with a success probability that may depend on the
rest of the point. -/
private def resampleLaw (μ : Law (Vertex I)) (a : I) (q : Vertex I → ℝ)
    (hq : ∀ v, 0 ≤ q v ∧ q v ≤ 1) : Law (Vertex I) :=
  (splitLaw μ q hq).map (fun p => Function.update p.1 a p.2)

private theorem resampleLaw_expect (μ : Law (Vertex I)) (a : I) (q : Vertex I → ℝ)
    (hq : ∀ v, 0 ≤ q v ∧ q v ≤ 1) (f : Vertex I → ℝ) :
    (resampleLaw μ a q hq).expect f =
      μ.expect (fun v => (1 - q v) * f (Function.update v a false)
        + q v * f (Function.update v a true)) := by
  rw [resampleLaw, Law.expect_map, splitLaw_expect]
  rfl

omit [Fintype I] in
private theorem countOn_insert {s : Finset I} {a : I} (ha : a ∉ s) (v : Vertex I) (b : Bool) :
    countOn (insert a s) (Function.update v a b) =
      countOn s v + (if b then 1 else 0) := by
  have hfil : s.filter (fun i => Function.update v a b i = true) =
      s.filter (fun i => v i = true) := by
    refine Finset.filter_congr fun i hi => ?_
    rw [Function.update_of_ne (show i ≠ a by rintro rfl; exact ha hi)]
  have hnot : a ∉ s.filter (fun i => Function.update v a b i = true) := by
    rw [hfil]
    exact fun hmem => ha (Finset.mem_of_mem_filter _ hmem)
  unfold countOn
  rw [Finset.filter_insert, Function.update_self]
  cases b
  · simp [hfil]
  · rw [if_pos rfl, Finset.card_insert_of_notMem hnot, hfil]
    simp

/-- One coordinate of the inductive construction: given a law whose success
count on `s` is carried by two adjacent integers, resampling a fresh coordinate
`a` with a count-dependent probability keeps the means and moves the count
distribution to the next pair. -/
private theorem adjacent_step (μ : Law (Vertex I)) (x : I → ℝ) (a : I) {s : Finset I}
    (ha : a ∉ s) (hmean : HasMeans μ x) (m : ℕ) (θ : ℝ)
    (hcount : ∀ f : ℕ → ℝ, μ.expect (fun v => f (countOn s v)) =
      (1 - θ) * f m + θ * f (m + 1))
    (qhat : ℕ → ℝ) (hq : ∀ k, 0 ≤ qhat k ∧ qhat k ≤ 1) (q₀ q₁ : ℝ)
    (hq₀ : qhat m = q₀) (hq₁ : qhat (m + 1) = q₁) (m' : ℕ) (θ' : ℝ)
    (hmeanq : (1 - θ) * q₀ + θ * q₁ = x a)
    (hval : ∀ f : ℕ → ℝ,
      (1 - θ) * ((1 - q₀) * f m + q₀ * f (m + 1)) +
        θ * ((1 - q₁) * f (m + 1) + q₁ * f (m + 1 + 1)) =
      (1 - θ') * f m' + θ' * f (m' + 1)) :
    ∃ ν : Law (Vertex I), HasMeans ν x ∧ ∀ f : ℕ → ℝ,
      ν.expect (fun v => f (countOn (insert a s) v)) =
        (1 - θ') * f m' + θ' * f (m' + 1) := by
  have hval' : ∀ f : ℕ → ℝ,
      (1 - θ) * ((1 - qhat m) * f m + qhat m * f (m + 1)) +
        θ * ((1 - qhat (m + 1)) * f (m + 1) + qhat (m + 1) * f (m + 1 + 1)) =
      (1 - θ') * f m' + θ' * f (m' + 1) := by
    intro f
    rw [hq₀, hq₁]
    exact hval f
  refine ⟨resampleLaw μ a (fun v => qhat (countOn s v)) (fun v => hq _), ?_, ?_⟩
  · intro i
    rw [resampleLaw_expect]
    by_cases hia : i = a
    · rw [hia]
      have hpt : ∀ v : Vertex I,
          (1 - qhat (countOn s v)) * vertexPoint (Function.update v a false) a +
            qhat (countOn s v) * vertexPoint (Function.update v a true) a =
            qhat (countOn s v) := by
        intro v
        simp [vertexPoint]
      simp only [hpt]
      rw [hcount qhat, hq₀, hq₁]
      exact hmeanq
    · have hpt : ∀ v : Vertex I,
          (1 - qhat (countOn s v)) * vertexPoint (Function.update v a false) i +
            qhat (countOn s v) * vertexPoint (Function.update v a true) i =
            vertexPoint v i := by
        intro v
        simp only [vertexPoint, Function.update_of_ne hia]
        ring
      simp only [hpt]
      exact hmean i
  · intro f
    rw [resampleLaw_expect]
    have hpt : ∀ v : Vertex I,
        (1 - qhat (countOn s v)) * f (countOn (insert a s) (Function.update v a false)) +
          qhat (countOn s v) * f (countOn (insert a s) (Function.update v a true)) =
        (fun k => (1 - qhat k) * f k + qhat k * f (k + 1)) (countOn s v) := by
      intro v
      rw [countOn_insert ha, countOn_insert ha]
      simp
    simp only [hpt]
    exact (hcount (fun k => (1 - qhat k) * f k + qhat k * f (k + 1))).trans (hval' f)

/-- PB10: an explicit law with the prescribed means whose success count on `s`
lives on the two adjacent integers `⌊S⌋` and `⌊S⌋ + 1`, the upper count carrying
weight `S - ⌊S⌋`. -/
theorem exists_adjacentLaw (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧ ∀ f : ℕ → ℝ,
      μ.expect (fun v => f (countOn s v)) =
        (1 - countFrac s x) * f (countFloor s x) +
          countFrac s x * f (countFloor s x + 1) := by
  classical
  induction s using Finset.induction_on with
  | empty =>
    refine ⟨bernoulliLaw x hx, fun i => bernoulliLaw_mean x hx i, fun f => ?_⟩
    have h0 : countFloor (∅ : Finset I) x = 0 := by simp [countFloor, meanSum]
    have h1 : countFrac (∅ : Finset I) x = 0 := by simp [countFrac, countFloor, meanSum]
    rw [h0, h1]
    simp
  | @insert a s ha ih =>
    obtain ⟨μ, hmean, hcount⟩ := ih
    have hxa := hx a
    have hθ0 : 0 ≤ countFrac s x := countFrac_nonneg hx
    have hθ1 : countFrac s x < 1 := countFrac_lt_one s x
    have hSm : meanSum s x = (countFloor s x : ℝ) + countFrac s x := by
      rw [countFrac]; ring
    have hins : meanSum (insert a s) x = x a + meanSum s x := Finset.sum_insert ha
    have h0 : (0 : ℝ) ≤ meanSum (insert a s) x := meanSum_nonneg hx
    by_cases hcase : 1 ≤ countFrac s x + x a
    · have hfl : countFloor (insert a s) x = countFloor s x + 1 :=
        (Nat.floor_eq_iff h0 (n := countFloor s x + 1)).mpr
          ⟨by rw [hins, hSm]; push_cast; linarith,
           by rw [hins, hSm]; push_cast; linarith⟩
      have hfr : countFrac (insert a s) x = countFrac s x + x a - 1 := by
        rw [countFrac, hfl, hins, hSm]; push_cast; ring
      set c : ℝ := if countFrac s x = 0 then 0
        else (x a - 1 + countFrac s x) / countFrac s x with hc
      have hθc : countFrac s x * c = countFrac s x + x a - 1 := by
        by_cases hz : countFrac s x = 0
        · have hone : x a = 1 := le_antisymm hxa.2 (by rw [hz] at hcase; linarith)
          rw [hc, if_pos hz, hz, hone]; ring
        · rw [hc, if_neg hz]
          field_simp
          ring
      have hc01 : 0 ≤ c ∧ c ≤ 1 := by
        by_cases hz : countFrac s x = 0
        · rw [hc, if_pos hz]; exact ⟨le_refl 0, zero_le_one⟩
        · have hpos : 0 < countFrac s x := lt_of_le_of_ne hθ0 (Ne.symm hz)
          rw [hc, if_neg hz]
          exact ⟨div_nonneg (by linarith) hpos.le,
            (div_le_one hpos).mpr (by linarith [hxa.2])⟩
      rw [hfl, hfr]
      refine adjacent_step μ x a ha hmean (countFloor s x) (countFrac s x) hcount
        (fun k => if k = countFloor s x then 1 else c) ?_ 1 c (if_pos rfl) (if_neg (by omega))
        (countFloor s x + 1) (countFrac s x + x a - 1) ?_ ?_
      · intro k
        by_cases hk : k = countFloor s x
        · rw [if_pos hk]; exact ⟨zero_le_one, le_refl 1⟩
        · rw [if_neg hk]; exact hc01
      · linarith
      · intro f
        linear_combination (f (countFloor s x + 1 + 1) - f (countFloor s x + 1)) * hθc
    · rw [not_le] at hcase
      have hfl : countFloor (insert a s) x = countFloor s x :=
        (Nat.floor_eq_iff h0 (n := countFloor s x)).mpr
          ⟨by rw [hins, hSm]; linarith, by rw [hins, hSm]; linarith⟩
      have hfr : countFrac (insert a s) x = countFrac s x + x a := by
        rw [countFrac, hfl, hins, hSm]; ring
      have hne : (1 : ℝ) - countFrac s x ≠ 0 := by linarith
      have hkey : (1 - countFrac s x) * (x a / (1 - countFrac s x)) = x a := by
        field_simp
      rw [hfl, hfr]
      refine adjacent_step μ x a ha hmean (countFloor s x) (countFrac s x) hcount
        (fun k => if k = countFloor s x then x a / (1 - countFrac s x) else 0) ?_
        (x a / (1 - countFrac s x)) 0 (if_pos rfl) (if_neg (by omega))
        (countFloor s x) (countFrac s x + x a) ?_ ?_
      · intro k
        by_cases hk : k = countFloor s x
        · rw [if_pos hk]
          exact ⟨div_nonneg hxa.1 (by linarith),
            (div_le_one (by linarith)).mpr (by linarith)⟩
        · rw [if_neg hk]; exact ⟨le_refl 0, zero_le_one⟩
      · linarith [hkey]
      · intro f
        linear_combination (f (countFloor s x + 1) - f (countFloor s x)) * hkey

/-! ## PB11: the exact convex envelope -/

/-- With the prescribed means the expected success count on `s` is `S`. -/
theorem expect_countOn (s : Finset I) (x : I → ℝ) (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    μ.expect (fun v => (countOn s v : ℝ)) = meanSum s x := by
  simp only [countOn_eq_sum]
  rw [expect_finsetSum]
  exact Finset.sum_congr rfl fun i _ => hm i

/-- Discrete convexity of `f` plus the prescribed means force the adjacent-count
chord value as a lower bound for `E f(K)` over all laws with those means. -/
theorem convex_count_expect_lower (f : ℕ → ℝ)
    (hf : ∀ k, f (k + 1) - f k ≤ f (k + 2) - f (k + 1))
    (s : Finset I) (x : I → ℝ) (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    (1 - countFrac s x) * f (countFloor s x) + countFrac s x * f (countFloor s x + 1)
      ≤ μ.expect (fun v => f (countOn s v)) := by
  have hle := μ.expect_mono (fun v => chord_le_of_convex f hf (countFloor s x) (countOn s v))
  have hlhs : μ.expect (fun v => f (countFloor s x) +
      ((countOn s v : ℝ) - (countFloor s x : ℝ)) *
        (f (countFloor s x + 1) - f (countFloor s x))) =
      f (countFloor s x) + (meanSum s x - (countFloor s x : ℝ)) *
        (f (countFloor s x + 1) - f (countFloor s x)) := by
    simp only [Law.expect_add, Law.expect_const, Law.expect_mul_const, Law.expect_sub]
    rw [expect_countOn s x μ hm]
  rw [hlhs] at hle
  have hre : (1 - countFrac s x) * f (countFloor s x) +
      countFrac s x * f (countFloor s x + 1) =
      f (countFloor s x) + (meanSum s x - (countFloor s x : ℝ)) *
        (f (countFloor s x + 1) - f (countFloor s x)) := by
    rw [countFrac]; ring
  rw [hre]
  exact hle

omit [Fintype I] [DecidableEq I] in
/-- PB11: the **exact** convex envelope of the physical monomial, namely
`rho ^ ⌊S⌋ * (1 + (rho - 1) * (S - ⌊S⌋))` with `rho = 1 + t`. Both halves are
proved: no law with the prescribed means falls below this value, and the
adjacent-count law of PB10 attains it. -/
theorem physMonomial_minimum [Finite I] (t : ℝ) (ht : 0 ≤ t) (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) :
    IsLeast (envelopeValues (physMonomial t s) x) (physLower t s x) := by
  classical
  let := Fintype.ofFinite I
  have hpl : (1 - countFrac s x) * (1 + t) ^ countFloor s x +
      countFrac s x * (1 + t) ^ (countFloor s x + 1) = physLower t s x := by
    rw [physLower, pow_succ]; ring
  apply minimum_from_laws _ (physMonomial_coordinate_affine t s)
  · intro μ hm
    have h := convex_count_expect_lower (fun k => (1 + t) ^ k) (pow_succ_convex ht) s x μ hm
    simp only [physMonomial_vertex]
    rw [← hpl]
    exact h
  · obtain ⟨μ, hmean, hcount⟩ := exists_adjacentLaw s x hx
    refine ⟨μ, hmean, ?_⟩
    simp only [physMonomial_vertex]
    rw [hcount (fun k => (1 + t) ^ k)]
    exact hpl

/-- The minimal `j`-th binomial moment, `V_j = (1 - θ) binom(⌊S⌋, j) + θ binom(⌊S⌋ + 1, j)`. -/
def binomMomentLower (s : Finset I) (x : I → ℝ) (j : ℕ) : ℝ :=
  (1 - countFrac s x) * (((countFloor s x).choose j : ℕ) : ℝ) +
    countFrac s x * (((countFloor s x + 1).choose j : ℕ) : ℝ)

/-- PB11, moments: for every order `j ≥ 1` the binomial moment of any law with
the prescribed means is at least `binomMomentLower`. -/
theorem binomMomentLower_le (s : Finset I) (x : I → ℝ) {j : ℕ} (hj : 1 ≤ j)
    (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    binomMomentLower s x j ≤ binomMoment s μ (j : ℤ) := by
  obtain ⟨j', rfl⟩ : ∃ j', j = j' + 1 := ⟨j - 1, by omega⟩
  have h := convex_count_expect_lower (fun k => ((k.choose (j' + 1) : ℕ) : ℝ))
    (fun k => choose_convex j' k) s x μ hm
  have hb : binomMoment s μ (((j' + 1 : ℕ) : ℤ)) =
      μ.expect (fun v => (((countOn s v).choose (j' + 1) : ℕ) : ℝ)) := by
    simp only [binomMoment, chooseInt_natCast]
  rw [hb, binomMomentLower]
  exact h

/-- PB11, attainment: one adjacent-count law realizes the physical convex
envelope for every `t` and, simultaneously, the minimal binomial moment of every
order. -/
theorem exists_law_attaining_lower (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧
      (∀ j : ℕ, binomMoment s μ (j : ℤ) = binomMomentLower s x j) ∧
      (∀ t : ℝ, μ.expect (fun v => physMonomial t s (vertexPoint v)) = physLower t s x) := by
  obtain ⟨μ, hmean, hcount⟩ := exists_adjacentLaw s x hx
  refine ⟨μ, hmean, fun j => ?_, fun t => ?_⟩
  · have hb : binomMoment s μ ((j : ℕ) : ℤ) =
        μ.expect (fun v => (((countOn s v).choose j : ℕ) : ℝ)) := by
      simp only [binomMoment, chooseInt_natCast]
    rw [hb, hcount (fun k => ((k.choose j : ℕ) : ℝ))]
    rfl
  · simp only [physMonomial_vertex]
    rw [hcount (fun k => (1 + t) ^ k), physLower, pow_succ]
    ring

omit [Fintype I] [DecidableEq I] in
/-- PB12 for the minimal moment family: order zero is one. -/
@[simp] theorem binomMomentLower_zero (s : Finset I) (x : I → ℝ) :
    binomMomentLower s x 0 = 1 := by
  rw [binomMomentLower]
  simp

omit [Fintype I] [DecidableEq I] in
/-- PB12 for the minimal moment family: orders above the dimension of the
support vanish. -/
theorem binomMomentLower_of_card_lt [Finite I] (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) {j : ℕ} (hj : s.card < j) : binomMomentLower s x j = 0 := by
  classical
  let := Fintype.ofFinite I
  obtain ⟨μ, _, hmom, _⟩ := exists_law_attaining_lower s x hx
  rw [← hmom j]
  exact binomMoment_of_card_lt s μ (by exact_mod_cast hj)

omit [Fintype I] [DecidableEq I] in
/-- PB11, generating form: the minimal moments assemble into the physical convex
envelope, `V(t) = ∑ j, V_j t ^ j = rho ^ ⌊S⌋ (1 + (rho - 1)(S - ⌊S⌋))`. -/
theorem sum_binomMomentLower [Finite I] (t : ℝ) (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) :
    ∑ j ∈ Finset.range (s.card + 1), binomMomentLower s x j * t ^ j = physLower t s x := by
  classical
  let := Fintype.ofFinite I
  obtain ⟨μ, _, hmom, hphys⟩ := exists_law_attaining_lower s x hx
  rw [← hphys t, expect_physMonomial_eq_sum_binomMoment]
  exact Finset.sum_congr rfl fun j _ => by rw [hmom j]

/-- The exact envelope width of the physical monomial on the cube. -/
theorem physMonomial_hullGap (t : ℝ) (ht : 0 ≤ t) (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) :
    hullGap (physMonomial t s) x = physUpper t s x - physLower t s x := by
  rw [hullGap, (physMonomial_maximum t ht s x hx).csSup_eq,
    (physMonomial_minimum t ht s x hx).csInf_eq]

end

end MultilinearGap
