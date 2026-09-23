import CertifiedMinlp.Coordinates

/-! Exact rational interval arithmetic and the finite-endpoint comparison contract.
These theorems do not verify a floating-point or transcendental interval library. -/
namespace CertifiedMinlp

/-- Finite rational endpoints. Enclosure does not assume ordering as an extra premise. -/
structure RationalInterval where
  lower : ℚ
  upper : ℚ
  deriving DecidableEq

namespace RationalInterval

def contains (I : RationalInterval) (x : ℝ) : Prop :=
  (I.lower : ℝ) ≤ x ∧ x ≤ (I.upper : ℝ)

def point (q : ℚ) : RationalInterval := ⟨q, q⟩
def add (I J : RationalInterval) : RationalInterval :=
  ⟨I.lower + J.lower, I.upper + J.upper⟩
def neg (I : RationalInterval) : RationalInterval := ⟨-I.upper, -I.lower⟩
def sub (I J : RationalInterval) : RationalInterval := I.add J.neg

def mul (I J : RationalInterval) : RationalInterval :=
  ⟨min (min (I.lower * J.lower) (I.lower * J.upper))
    (min (I.upper * J.lower) (I.upper * J.upper)),
   max (max (I.lower * J.lower) (I.lower * J.upper))
    (max (I.upper * J.lower) (I.upper * J.upper))⟩

def scale (q : ℚ) (I : RationalInterval) : RationalInterval := (point q).mul I

def max (I J : RationalInterval) : RationalInterval :=
  ⟨Max.max I.lower J.lower, Max.max I.upper J.upper⟩

def reciprocal (I : RationalInterval) : RationalInterval := ⟨I.upper⁻¹, I.lower⁻¹⟩

@[simp] theorem contains_point (q : ℚ) : (point q).contains (q : ℝ) := ⟨le_rfl, le_rfl⟩

theorem contains_add {I J : RationalInterval} {x y : ℝ}
    (hx : I.contains x) (hy : J.contains y) : (I.add J).contains (x + y) := by
  simpa only [contains, add, Rat.cast_add] using
    And.intro (add_le_add hx.1 hy.1) (add_le_add hx.2 hy.2)

theorem contains_neg {I : RationalInterval} {x : ℝ}
    (hx : I.contains x) : I.neg.contains (-x) := by
  simpa only [contains, neg, Rat.cast_neg] using
    And.intro (neg_le_neg hx.2) (neg_le_neg hx.1)

theorem contains_sub {I J : RationalInterval} {x y : ℝ}
    (hx : I.contains x) (hy : J.contains y) : (I.sub J).contains (x - y) := by
  simpa only [sub, sub_eq_add_neg] using contains_add hx (contains_neg hy)

private theorem four_lower {l u v w x y c : ℝ}
    (hx : l ≤ x ∧ x ≤ u) (hy : v ≤ y ∧ y ≤ w)
    (h₁ : c ≤ l * v) (h₂ : c ≤ l * w) (h₃ : c ≤ u * v) (h₄ : c ≤ u * w) :
    c ≤ x * y := by
  rcases le_total 0 y with h | h
  · apply le_trans _ (mul_le_mul_of_nonneg_right hx.1 h)
    rcases le_total 0 l with hl | hl
    · exact h₁.trans (mul_le_mul_of_nonneg_left hy.1 hl)
    · exact h₂.trans (mul_le_mul_of_nonpos_left hy.2 hl)
  · apply le_trans _ (mul_le_mul_of_nonpos_right hx.2 h)
    rcases le_total 0 u with hu | hu
    · exact h₃.trans (mul_le_mul_of_nonneg_left hy.1 hu)
    · exact h₄.trans (mul_le_mul_of_nonpos_left hy.2 hu)

private theorem four_upper {l u v w x y c : ℝ}
    (hx : l ≤ x ∧ x ≤ u) (hy : v ≤ y ∧ y ≤ w)
    (h₁ : l * v ≤ c) (h₂ : l * w ≤ c) (h₃ : u * v ≤ c) (h₄ : u * w ≤ c) :
    x * y ≤ c := by
  rcases le_total 0 y with h | h
  · apply le_trans (mul_le_mul_of_nonneg_right hx.2 h)
    rcases le_total 0 u with hu | hu
    · exact (mul_le_mul_of_nonneg_left hy.2 hu).trans h₄
    · exact (mul_le_mul_of_nonpos_left hy.1 hu).trans h₃
  · apply le_trans (mul_le_mul_of_nonpos_right hx.1 h)
    rcases le_total 0 l with hl | hl
    · exact (mul_le_mul_of_nonneg_left hy.2 hl).trans h₂
    · exact (mul_le_mul_of_nonpos_left hy.1 hl).trans h₁

theorem contains_mul {I J : RationalInterval} {x y : ℝ}
    (hx : I.contains x) (hy : J.contains y) : (I.mul J).contains (x * y) := by
  simp only [contains, mul, Rat.cast_min, Rat.cast_max, Rat.cast_mul]
  constructor
  · apply four_lower hx hy
    · exact (min_le_left _ _).trans (min_le_left _ _)
    · exact (min_le_left _ _).trans (min_le_right _ _)
    · exact (min_le_right _ _).trans (min_le_left _ _)
    · exact (min_le_right _ _).trans (min_le_right _ _)
  · apply four_upper hx hy
    · exact (le_max_left _ _).trans (le_max_left _ _)
    · exact (le_max_right _ _).trans (le_max_left _ _)
    · exact (le_max_left _ _).trans (le_max_right _ _)
    · exact (le_max_right _ _).trans (le_max_right _ _)

theorem contains_scale {I : RationalInterval} {x : ℝ} (q : ℚ)
    (hx : I.contains x) : (I.scale q).contains ((q : ℝ) * x) :=
  contains_mul (contains_point q) hx

theorem contains_max {I J : RationalInterval} {x y : ℝ}
    (hx : I.contains x) (hy : J.contains y) : (I.max J).contains (Max.max x y) := by
  simpa only [contains, max, Rat.cast_max] using
    And.intro (max_le_max hx.1 hy.1) (max_le_max hx.2 hy.2)

theorem contains_reciprocal_pos {I : RationalInterval} {x : ℝ}
    (hx : I.contains x) (hl : 0 < I.lower) : I.reciprocal.contains x⁻¹ := by
  have hl' : (0 : ℝ) < I.lower := by exact_mod_cast hl
  have hx' : 0 < x := hl'.trans_le hx.1
  simpa only [contains, reciprocal, Rat.cast_inv] using
    And.intro (inv_anti₀ hx' hx.2) (inv_anti₀ hl' hx.1)

theorem contains_reciprocal_neg {I : RationalInterval} {x : ℝ}
    (hx : I.contains x) (hu : I.upper < 0) : I.reciprocal.contains x⁻¹ := by
  have hneg : 0 < I.neg.lower := by simpa only [neg, Left.neg_pos_iff] using hu
  have h := contains_reciprocal_pos (contains_neg hx) hneg
  simpa only [contains, reciprocal, neg, Rat.cast_neg, Rat.cast_inv,
    inv_neg, neg_le_neg_iff] using h.symm

theorem contains_reciprocal {I : RationalInterval} {x : ℝ}
    (hx : I.contains x) (hzero : 0 < I.lower ∨ I.upper < 0) :
    I.reciprocal.contains x⁻¹ := by
  rcases hzero with h | h
  · exact contains_reciprocal_pos hx h
  · exact contains_reciprocal_neg hx h

def natPower (I : RationalInterval) : ℕ → RationalInterval
  | 0 => point 1
  | n + 1 => (natPower I n).mul I

theorem contains_natPower {I : RationalInterval} {x : ℝ}
    (hx : I.contains x) (n : ℕ) : (I.natPower n).contains (x ^ n) := by
  induction n with
  | zero => simpa only [natPower, pow_zero, Rat.cast_one] using contains_point 1
  | succ n ih => simpa only [natPower, pow_succ] using contains_mul ih hx

/-- Negative exponents first invert an interval whose sign has been certified. -/
def intPower (I : RationalInterval) : ℤ → RationalInterval
  | .ofNat n => I.natPower n
  | .negSucc n => I.reciprocal.natPower (n + 1)

theorem contains_intPower {I : RationalInterval} {x : ℝ}
    (hx : I.contains x) (n : ℤ) (hzero : n < 0 → 0 < I.lower ∨ I.upper < 0) :
    (I.intPower n).contains (x ^ n) := by
  cases n with
  | ofNat n => simpa only [intPower, Int.ofNat_eq_natCast, zpow_natCast] using
      contains_natPower hx n
  | negSucc n =>
    have h := contains_natPower (contains_reciprocal hx (hzero (by omega))) (n + 1)
    simpa only [intPower, zpow_negSucc, inv_pow] using h

def product : List RationalInterval → RationalInterval
  | [] => point 1
  | I :: Is => I.mul (product Is)

theorem contains_product (Is : List RationalInterval) (xs : List ℝ)
    (h : List.Forall₂ contains Is xs) : (product Is).contains xs.prod := by
  induction h with
  | nil => simpa only [product, List.prod_nil, Rat.cast_one] using contains_point 1
  | cons hx _ ih => simpa only [product, List.prod_cons] using contains_mul hx ih

/-- The exact comparison made after extracting a finite lower endpoint. -/
theorem lower_endpoint_sound {I : RationalInterval} {x : ℝ} {b : ℚ}
    (hx : I.contains x) (hb : b ≤ I.lower) : (b : ℝ) ≤ x := by
  have hb' : (b : ℝ) ≤ I.lower := by exact_mod_cast hb
  exact hb'.trans hx.1

end RationalInterval

/-- Monotone integer powers on a nonnegative interval use its two endpoints. -/
theorem nonnegative_power_bounds {l u x : ℝ} (hl : 0 ≤ l)
    (hx : l ≤ x ∧ x ≤ u) (n : ℕ) : l ^ n ≤ x ^ n ∧ x ^ n ≤ u ^ n :=
  ⟨pow_le_pow_left₀ hl hx.1 n, pow_le_pow_left₀ (hl.trans hx.1) hx.2 n⟩

/-- Even powers reverse the endpoints of a nonpositive interval. -/
theorem nonpositive_even_power_bounds {l u x : ℝ} {n : ℕ}
    (hu : u ≤ 0) (hx : l ≤ x ∧ x ≤ u) (hn : Even n) :
    u ^ n ≤ x ^ n ∧ x ^ n ≤ l ^ n := by
  have h := nonnegative_power_bounds (neg_nonneg.mpr hu)
    (And.intro (neg_le_neg hx.2) (neg_le_neg hx.1)) n
  simpa only [hn.neg_pow] using h

/-- Across zero, zero and the larger endpoint power form an enclosure. -/
theorem even_power_bounds {l u x : ℝ} {n : ℕ}
    (hx : l ≤ x ∧ x ≤ u) (hn : Even n) :
    0 ≤ x ^ n ∧ x ^ n ≤ max (l ^ n) (u ^ n) := by
  refine ⟨hn.pow_nonneg x, ?_⟩
  rcases le_total 0 x with h | h
  · exact (pow_le_pow_left₀ h hx.2 n).trans (le_max_right _ _)
  · have hp := pow_le_pow_left₀ (neg_nonneg.mpr h) (neg_le_neg hx.1) n
    rw [hn.neg_pow, hn.neg_pow] at hp
    exact hp.trans (le_max_left _ _)

/-- Products of nonnegative half-lines have the product of their finite lower bounds. -/
theorem product_lower_nonnegative {l v x y : ℝ}
    (hl : 0 ≤ l) (hv : 0 ≤ v) (hx : l ≤ x) (hy : v ≤ y) : l * v ≤ x * y :=
  mul_le_mul hx hy hv (hl.trans hx)

/-- Products of nonpositive half-lines have the product of their finite upper bounds. -/
theorem product_lower_nonpositive {u w x y : ℝ}
    (hu : u ≤ 0) (hw : w ≤ 0) (hx : x ≤ u) (hy : y ≤ w) : u * w ≤ x * y := by
  have h := product_lower_nonnegative (neg_nonneg.mpr hu) (neg_nonneg.mpr hw)
    (neg_le_neg hx) (neg_le_neg hy)
  simpa only [neg_mul_neg] using h

/-- A nonnegative and a nonpositive half-line yield a finite upper product endpoint. -/
theorem product_upper_nonnegative_nonpositive {l w x y : ℝ}
    (hl : 0 ≤ l) (hw : w ≤ 0) (hx : l ≤ x) (hy : y ≤ w) : x * y ≤ l * w := by
  exact (mul_le_mul_of_nonpos_right hx (hy.trans hw)).trans
    (mul_le_mul_of_nonneg_left hy hl)

theorem product_upper_nonpositive_nonnegative {u v x y : ℝ}
    (hu : u ≤ 0) (hv : 0 ≤ v) (hx : x ≤ u) (hy : v ≤ y) : x * y ≤ u * v := by
  simpa only [mul_comm] using product_upper_nonnegative_nonpositive hv hu hy hx

/-- Exact numerator/denominator interpretation; no binary64 approximation occurs. -/
theorem rational_input_exact (q : ℚ) :
    (q.num : ℝ) / (q.den : ℝ) = (q : ℝ) := by
  exact_mod_cast Rat.num_div_den q

/-- Value reconstructed from a finite binary endpoint's sign, mantissa and exponent. -/
def dyadicEndpoint (negative : Bool) (mantissa : ℕ) (exponent : ℤ) : ℚ :=
  (if negative then -1 else 1) * mantissa * (2 : ℚ) ^ exponent

theorem dyadic_endpoint_exact (negative : Bool) (mantissa : ℕ) (exponent : ℤ) :
    (dyadicEndpoint negative mantissa exponent : ℝ) =
      (if negative then -1 else 1) * (mantissa : ℝ) * (2 : ℝ) ^ exponent := by
  cases negative <;> simp [dyadicEndpoint]

/-- A downward endpoint comparison preserves an enclosed intercept bound. -/
theorem dyadic_intercept_sound {negative : Bool} {mantissa : ℕ} {exponent : ℤ}
    {v : ℝ} {b : ℚ}
    (hendpoint : (if negative then -1 else 1) * (mantissa : ℝ) *
      (2 : ℝ) ^ exponent ≤ v)
    (hb : b ≤ dyadicEndpoint negative mantissa exponent) : (b : ℝ) ≤ v := by
  have hb' : (b : ℝ) ≤ (dyadicEndpoint negative mantissa exponent : ℝ) := by
    exact_mod_cast hb
  rw [dyadic_endpoint_exact] at hb'
  exact hb'.trans hendpoint

end CertifiedMinlp
