import Formal.MultilinearGap.OrientationMoments

/-!
# The positive-box coefficient inequality

This module discharges the Tier C obligations PB13-PB18 of
`formal/topics/18-positive-box/CLAIMS.md`: the definition of the coefficient

`F_{n,j} = 2 C_j + V_j - P_j - 2 O_j + C_{j-1} - P_{j-1}`

and its **nonnegativity for every support, every point of the cube and every
integer order**.  All four moment families are the ones fixed by
`Formal.MultilinearGap.PhysicalEnvelope` and
`Formal.MultilinearGap.OrientationMoments`, at integer orders, under the PB12
conventions (order zero is one, negative orders vanish, orders above the support
cardinality vanish):

* `C_j = thresholdMoment s x j`, the common-threshold moment
  `binomMoment s (thresholdLaw x) j`;
* `V_j = lowerMomentInt s x j`, the minimal adjacent-count moment
  `(1 - θ) binom(⌊S⌋, j) + θ binom(⌊S⌋ + 1, j)`;
* `P_j = elementaryInt s x j`, the independent-rounding moment, the elementary
  symmetric polynomial `elementaryOn s j x`;
* `O_j = orientMoment s x j`, the fair endpoint-orientation moment.

The results, in the order of the obligations:

* PB13: `coeffF_zero` and `coeffF_one` give `F_{n,0} = F_{n,1} = 0`, and
  `coeffF_of_neg` records that negative orders vanish too.
* PB14: `coeffF_card_add_one` is `F_{n,n+1} = C_n - P_n`,
  `coeffF_card_add_one_nonneg` its nonnegativity, and
  `coeffF_of_card_add_one_lt` the vanishing above order `n + 1`.
* PB15: `coeffF_two` is `F_{n,2} = (C_2 - P_2) + (V_2 - L_2)` and
  `coeffF_two_nonneg` its nonnegativity, through PB08 and the two pairwise
  Fréchet bounds (`elementaryInt_le_thresholdMoment` and
  `frechetPairLower_le_lowerMomentInt`).
* PB16: the boundary recursions `coeffF_insert_of_mean_zero` and
  `coeffF_insert_of_mean_one`, assembled from the per-family statements
  `thresholdMoment_insert_of_mean_*`, `elementaryInt_insert_of_mean_*`,
  `orientMoment_insert_of_mean_*` and `lowerMomentInt_insert_of_mean_*`.  The
  threshold and orientation families use the law-level lemmas
  `binomMoment_insert_of_mean_zero` and `binomMoment_insert_of_mean_one`.
  The elementary family uses `elementaryOn_peel`; the adjacent-count family
  uses the integer-order Pascal identity `chooseInt_succ` after its floor
  shifts by one.
* PB17: `coeffF_spread_le`, the spreading step at a **global minimum** and a
  **global maximum**.  The hypothesis is genuinely global: `F` is *not*
  Schur-concave, and the source records a four-variable counterexample to the
  stronger statement, so the minimum/maximum hypotheses may not be weakened to
  arbitrary mean-preserving spreading.  Ties are handled exactly as in the peel
  lemmas of `OrientationMoments`: the hypotheses are `∀ i ∈ s, x a ≤ x i` and
  `∀ i ∈ s, x i ≤ x b`, so *any* minimizer and *any* maximizer work, and no
  uniqueness is required.
* PB18: `coeffF_nonneg`, `0 ≤ F_{n,j}` for every `s`, every `x ∈ cube I` and
  every `j : ℤ`, by induction on the support cardinality.
-/

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-! ## Integer-order Pascal identity -/

/-- Pascal's identity for `chooseInt`, valid at **every** integer order: at
negative orders both sides vanish and at order zero the second summand is the
vanishing order `-1`. -/
theorem chooseInt_succ (k : ℕ) (j : ℤ) :
    chooseInt (k + 1) j = chooseInt k j + chooseInt k (j - 1) := by
  rcases lt_or_ge j 0 with hj | hj
  · rw [chooseInt_of_neg _ hj, chooseInt_of_neg _ hj,
      chooseInt_of_neg _ (show j - 1 < 0 by omega)]
    ring
  · obtain ⟨n, rfl⟩ := Int.eq_ofNat_of_zero_le hj
    match n with
    | 0 =>
      rw [Nat.cast_zero, chooseInt_zero, chooseInt_zero,
        chooseInt_of_neg _ (show (0 : ℤ) - 1 < 0 by norm_num)]
      ring
    | (m + 1) =>
      have h1 : ((m + 1 : ℕ) : ℤ) - 1 = ((m : ℕ) : ℤ) := by push_cast; ring
      rw [h1, chooseInt_natCast, chooseInt_natCast, chooseInt_natCast,
        Nat.choose_succ_succ]
      push_cast
      ring

/-! ## The four moment families at integer orders -/

/-- `P_j`, the independent-rounding binomial moment at an integer order: the
elementary symmetric polynomial of the means on the support, with negative
orders set to zero. -/
def elementaryInt (s : Finset I) (x : I → ℝ) (j : ℤ) : ℝ :=
  if 0 ≤ j then elementaryOn s j.toNat x else 0

/-- `V_j`, the minimal adjacent-count binomial moment at an integer order. -/
def lowerMomentInt (s : Finset I) (x : I → ℝ) (j : ℤ) : ℝ :=
  (1 - countFrac s x) * chooseInt (countFloor s x) j +
    countFrac s x * chooseInt (countFloor s x + 1) j

/-- `C_j`, the common-threshold binomial moment at an integer order. -/
def thresholdMoment (s : Finset I) (x : I → ℝ) (j : ℤ) : ℝ :=
  binomMoment s (thresholdLaw x) j

/-! ### The independent family -/

omit [Fintype I] [DecidableEq I] in
/-- At a nonnegative order `P_j` is the elementary symmetric polynomial. -/
@[simp] theorem elementaryInt_natCast (s : Finset I) (x : I → ℝ) (j : ℕ) :
    elementaryInt s x (j : ℤ) = elementaryOn s j x := by
  simp [elementaryInt]

omit [Fintype I] [DecidableEq I] in
/-- PB12 for the independent family: order zero is one. -/
@[simp] theorem elementaryInt_zero (s : Finset I) (x : I → ℝ) :
    elementaryInt s x 0 = 1 := by
  rw [show (0 : ℤ) = ((0 : ℕ) : ℤ) from rfl, elementaryInt_natCast, elementaryOn,
    Finset.powersetCard_zero]
  simp [monomial]

omit [Fintype I] [DecidableEq I] in
/-- PB12 for the independent family: negative orders vanish. -/
theorem elementaryInt_of_neg (s : Finset I) (x : I → ℝ) {j : ℤ} (hj : j < 0) :
    elementaryInt s x j = 0 := by
  rw [elementaryInt, if_neg (not_le.mpr hj)]

/-- The independent moments are the binomial moments of Bernoulli rounding. -/
theorem elementaryInt_eq_binomMoment (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) (j : ℤ) :
    elementaryInt s x j = binomMoment s (bernoulliLaw x hx) j := by
  rcases lt_or_ge j 0 with hj | hj
  · rw [elementaryInt_of_neg s x hj, binomMoment_of_neg s _ hj]
  · obtain ⟨k, rfl⟩ := Int.eq_ofNat_of_zero_le hj
    rw [elementaryInt_natCast, bernoulliLaw_binomMoment s x hx k]

/-- Bernoulli rounding has the prescribed means. -/
theorem bernoulliLaw_hasMeans (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (bernoulliLaw x hx) x := fun i => bernoulliLaw_mean x hx i

omit [Fintype I] [DecidableEq I] in
/-- PB12 for the independent family: orders above the support cardinality
vanish. -/
theorem elementaryInt_of_card_lt (s : Finset I) (x : I → ℝ) {j : ℤ}
    (hj : (s.card : ℤ) < j) : elementaryInt s x j = 0 := by
  obtain ⟨k, rfl⟩ := Int.eq_ofNat_of_zero_le (le_trans (Int.natCast_nonneg _) hj.le)
  rw [elementaryInt_natCast, elementaryOn,
    Finset.powersetCard_eq_empty.mpr (by exact_mod_cast hj), Finset.sum_empty]

omit [Fintype I] in
/-- Peeling one coordinate out of an elementary symmetric polynomial. -/
theorem elementaryOn_peel {s : Finset I} {a : I} (ha : a ∈ s) (x : I → ℝ) (r : ℕ) :
    elementaryOn s (r + 1) x =
      elementaryOn (s.erase a) (r + 1) x + x a * elementaryOn (s.erase a) r x := by
  rw [elementaryOn, sum_powersetCard_succ_split ha r fun A => monomial A x]
  congr 1
  rw [elementaryOn, Finset.mul_sum]
  refine Finset.sum_congr rfl fun B hB => ?_
  have hB0 : a ∉ B := fun hmem =>
    Finset.notMem_erase a s ((Finset.mem_powersetCard.mp hB).1 hmem)
  rw [monomial, Finset.prod_insert hB0]
  rfl

omit [Fintype I] [DecidableEq I] in
/-- On the cube the elementary symmetric polynomial is nonnegative. -/
theorem elementaryOn_nonneg (s : Finset I) {x : I → ℝ} (hx : x ∈ cube I) (j : ℕ) :
    0 ≤ elementaryOn s j x :=
  Finset.sum_nonneg fun _ _ => Finset.prod_nonneg fun i _ => (hx i).1

omit [Fintype I] [DecidableEq I] in
/-- On the cube the elementary symmetric polynomial is at most the number of
its terms, `E_r ≤ binom(n, r)`. -/
theorem elementaryOn_le_choose (s : Finset I) {x : I → ℝ} (hx : x ∈ cube I) (j : ℕ) :
    elementaryOn s j x ≤ ((s.card.choose j : ℕ) : ℝ) := by
  have h : ∀ A ∈ s.powersetCard j, monomial A x ≤ 1 := fun _ _ =>
    Finset.prod_le_one (fun i _ => (hx i).1) fun i _ => (hx i).2
  have hle : elementaryOn s j x ≤ (s.powersetCard j).card • (1 : ℝ) :=
    Finset.sum_le_card_nsmul _ _ _ h
  rwa [Finset.card_powersetCard, nsmul_eq_mul, mul_one] at hle

/-! ### The minimal (adjacent-count) family -/

omit [Fintype I] [DecidableEq I] in
/-- At a nonnegative order `V_j` is `binomMomentLower`. -/
@[simp] theorem lowerMomentInt_natCast (s : Finset I) (x : I → ℝ) (j : ℕ) :
    lowerMomentInt s x (j : ℤ) = binomMomentLower s x j := by
  simp [lowerMomentInt, binomMomentLower]

omit [Fintype I] [DecidableEq I] in
/-- PB12 for the minimal family: order zero is one. -/
@[simp] theorem lowerMomentInt_zero (s : Finset I) (x : I → ℝ) :
    lowerMomentInt s x 0 = 1 := by
  rw [lowerMomentInt, chooseInt_zero, chooseInt_zero]
  ring

omit [Fintype I] [DecidableEq I] in
/-- PB12 for the minimal family: negative orders vanish. -/
theorem lowerMomentInt_of_neg (s : Finset I) (x : I → ℝ) {j : ℤ} (hj : j < 0) :
    lowerMomentInt s x j = 0 := by
  rw [lowerMomentInt, chooseInt_of_neg _ hj, chooseInt_of_neg _ hj]
  ring

omit [Fintype I] [DecidableEq I] in
/-- The first minimal moment is the sum of the means on the support. -/
theorem lowerMomentInt_one (s : Finset I) (x : I → ℝ) :
    lowerMomentInt s x 1 = ∑ i ∈ s, x i := by
  have h1 : ∀ k : ℕ, chooseInt k 1 = (k : ℝ) := fun k => by
    rw [show (1 : ℤ) = ((1 : ℕ) : ℤ) from rfl, chooseInt_natCast, Nat.choose_one_right]
  simp only [lowerMomentInt, countFrac, meanSum, h1]
  push_cast
  ring

omit [Fintype I] [DecidableEq I] in
/-- PB12 for the minimal family: orders above the support cardinality vanish. -/
theorem lowerMomentInt_of_card_lt [Finite I] (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) {j : ℤ}
    (hj : (s.card : ℤ) < j) : lowerMomentInt s x j = 0 := by
  obtain ⟨k, rfl⟩ := Int.eq_ofNat_of_zero_le (le_trans (Int.natCast_nonneg _) hj.le)
  rw [lowerMomentInt_natCast, binomMomentLower_of_card_lt s x hx (by exact_mod_cast hj)]

omit [Fintype I] [DecidableEq I] in
/-- `V_j` depends on the means only through their sum on the support. -/
theorem lowerMomentInt_congr_of_meanSum {s s' : Finset I} {x y : I → ℝ}
    (h : meanSum s x = meanSum s' y) (j : ℤ) :
    lowerMomentInt s x j = lowerMomentInt s' y j := by
  simp only [lowerMomentInt, countFrac, countFloor, h]

/-! ### The common-threshold family -/

/-- PB12 for the common-threshold family: order zero is one. -/
@[simp] theorem thresholdMoment_zero (s : Finset I) (x : I → ℝ) :
    thresholdMoment s x 0 = 1 := binomMoment_zero s _

/-- PB12 for the common-threshold family: negative orders vanish. -/
theorem thresholdMoment_of_neg (s : Finset I) (x : I → ℝ) {j : ℤ} (hj : j < 0) :
    thresholdMoment s x j = 0 := binomMoment_of_neg s _ hj

/-- PB12 for the common-threshold family: orders above the support cardinality
vanish. -/
theorem thresholdMoment_of_card_lt (s : Finset I) (x : I → ℝ) {j : ℤ}
    (hj : (s.card : ℤ) < j) : thresholdMoment s x j = 0 := binomMoment_of_card_lt s _ hj

/-- The first common-threshold moment is the sum of the means on the support. -/
theorem thresholdMoment_one (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    thresholdMoment s x 1 = ∑ i ∈ s, x i :=
  binomMoment_one s x _ (thresholdLaw_hasMeans x hx)

omit [Fintype I] [DecidableEq I] in
/-- The subset minimum depends only on the means inside the subset. -/
theorem monomialUpper_congr {A : Finset I} {x y : I → ℝ} (h : ∀ i ∈ A, x i = y i) :
    monomialUpper A x = monomialUpper A y := by
  by_cases hA : A.Nonempty
  · obtain ⟨i, hi, hmin⟩ := monomial_min_anchor A hA x
    rw [monomialUpper_eq_anchor A x i hi hmin,
      monomialUpper_eq_anchor A y i hi fun k hk => by
        rw [← h i hi, ← h k hk]; exact hmin k hk, h i hi]
  · rw [Finset.not_nonempty_iff_eq_empty.mp hA, monomialUpper_empty, monomialUpper_empty]

/-- `C_j` depends only on the means inside the support. -/
theorem thresholdMoment_congr {s : Finset I} {x y : I → ℝ} (hx : x ∈ cube I) (hy : y ∈ cube I)
    (h : ∀ i ∈ s, x i = y i) (j : ℤ) :
    thresholdMoment s x j = thresholdMoment s y j := by
  rcases lt_or_ge j 0 with hj | hj
  · rw [thresholdMoment_of_neg s x hj, thresholdMoment_of_neg s y hj]
  · obtain ⟨k, rfl⟩ := Int.eq_ofNat_of_zero_le hj
    rw [thresholdMoment, thresholdMoment, thresholdLaw_binomMoment s x hx,
      thresholdLaw_binomMoment s y hy]
    exact Finset.sum_congr rfl fun A hA =>
      monomialUpper_congr fun i hi => h i ((Finset.mem_powersetCard.mp hA).1 hi)

/-- Common-threshold rounding maximizes every binomial moment among the laws
with the prescribed means. -/
theorem binomMoment_le_thresholdLaw (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (μ : Law (Vertex I)) (hm : HasMeans μ x) (j : ℤ) :
    binomMoment s μ j ≤ thresholdMoment s x j := by
  rcases lt_or_ge j 0 with hj | hj
  · rw [binomMoment_of_neg _ _ hj, thresholdMoment_of_neg s x hj]
  · obtain ⟨k, rfl⟩ := Int.eq_ofNat_of_zero_le hj
    rw [thresholdMoment, binomMoment_eq_sum_monomial, binomMoment_eq_sum_monomial]
    refine Finset.sum_le_sum fun A _ => ?_
    rw [thresholdLaw_monomial_upper A x hx]
    exact monomial_expect_le_upper A x μ hm

/-- The pairwise upper Fréchet bound at the moment level: `P_j ≤ C_j`. -/
theorem elementaryInt_le_thresholdMoment (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) (j : ℤ) :
    elementaryInt s x j ≤ thresholdMoment s x j := by
  rw [elementaryInt_eq_binomMoment s x hx]
  exact binomMoment_le_thresholdLaw s x hx _ (bernoulliLaw_hasMeans x hx) j

/-! ## PB13: the coefficient and its vanishing base orders -/

/-- PB13: the coefficient `F_{n,j} = 2 C_j + V_j - P_j - 2 O_j + C_{j-1} - P_{j-1}`. -/
def coeffF (s : Finset I) (x : I → ℝ) (j : ℤ) : ℝ :=
  2 * thresholdMoment s x j + lowerMomentInt s x j - elementaryInt s x j -
    2 * orientMoment s x j + thresholdMoment s x (j - 1) - elementaryInt s x (j - 1)

/-- Negative orders contribute nothing. -/
theorem coeffF_of_neg (s : Finset I) (x : I → ℝ) {j : ℤ} (hj : j < 0) :
    coeffF s x j = 0 := by
  have hj1 : j - 1 < 0 := by omega
  rw [coeffF, thresholdMoment_of_neg s x hj, lowerMomentInt_of_neg s x hj,
    elementaryInt_of_neg s x hj, orientMoment_of_neg s x hj,
    thresholdMoment_of_neg s x hj1, elementaryInt_of_neg s x hj1]
  ring

/-- **PB13**: `F_{n,0} = 0`. -/
theorem coeffF_zero (s : Finset I) (x : I → ℝ) : coeffF s x 0 = 0 := by
  rw [coeffF, thresholdMoment_zero, lowerMomentInt_zero, elementaryInt_zero,
    orientMoment_zero, thresholdMoment_of_neg s x (by norm_num),
    elementaryInt_of_neg s x (by norm_num : (0 : ℤ) - 1 < 0)]
  ring

/-- **PB13**: `F_{n,1} = 0`. -/
theorem coeffF_one (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) : coeffF s x 1 = 0 := by
  have h0 : (1 : ℤ) - 1 = 0 := by norm_num
  rw [coeffF, thresholdMoment_one s x hx, lowerMomentInt_one s x,
    orientMoment_one s x hx, h0, thresholdMoment_zero, elementaryInt_zero]
  have hP : elementaryInt s x 1 = ∑ i ∈ s, x i := by
    rw [elementaryInt_eq_binomMoment s x hx]
    exact binomMoment_one s x _ (bernoulliLaw_hasMeans x hx)
  rw [hP]
  ring

/-! ## PB14: the top order -/

/-- **PB14**: at order `n + 1` the coefficient collapses to `C_n - P_n`. -/
theorem coeffF_card_add_one (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    coeffF s x ((s.card : ℤ) + 1) =
      thresholdMoment s x (s.card : ℤ) - elementaryInt s x (s.card : ℤ) := by
  have hlt : (s.card : ℤ) < (s.card : ℤ) + 1 := by omega
  have hsub : (s.card : ℤ) + 1 - 1 = (s.card : ℤ) := by ring
  rw [coeffF, thresholdMoment_of_card_lt s x hlt, lowerMomentInt_of_card_lt s x hx hlt,
    elementaryInt_of_card_lt s x hlt, orientMoment_of_card_lt s x hlt, hsub]
  ring

/-- **PB14**: the top-order coefficient is nonnegative, by maximality of
common-threshold rounding against the feasible Bernoulli law. -/
theorem coeffF_card_add_one_nonneg (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    0 ≤ coeffF s x ((s.card : ℤ) + 1) := by
  rw [coeffF_card_add_one s x hx, sub_nonneg]
  exact elementaryInt_le_thresholdMoment s x hx _

/-- **PB14**: orders above `n + 1` vanish. -/
theorem coeffF_of_card_add_one_lt (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) {j : ℤ}
    (hj : (s.card : ℤ) + 1 < j) : coeffF s x j = 0 := by
  have h1 : (s.card : ℤ) < j := by omega
  have h2 : (s.card : ℤ) < j - 1 := by omega
  rw [coeffF, thresholdMoment_of_card_lt s x h1, lowerMomentInt_of_card_lt s x hx h1,
    elementaryInt_of_card_lt s x h1, orientMoment_of_card_lt s x h1,
    thresholdMoment_of_card_lt s x h2, elementaryInt_of_card_lt s x h2]
  ring

/-! ## PB15: order two -/

/-- The pairwise lower Fréchet bound: every law with the prescribed means has
second binomial moment at least `L_2`. -/
theorem frechetPairLower_le_binomMoment (s : Finset I) (x : I → ℝ)
    (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    frechetPairLower s x ≤ binomMoment s μ 2 := by
  rw [show (2 : ℤ) = ((2 : ℕ) : ℤ) from rfl, binomMoment_eq_sum_monomial, frechetPairLower]
  refine Finset.sum_le_sum fun A hA => ?_
  obtain ⟨-, hcard⟩ := Finset.mem_powersetCard.mp hA
  obtain ⟨a, b, hab, rfl⟩ := Finset.card_eq_two.mp hcard
  rw [Finset.sum_pair hab]
  refine max_le ?_ ?_
  · exact μ.expect_nonneg fun v => Finset.prod_nonneg fun i _ => by
      unfold vertexPoint; split <;> norm_num
  · have hpt : ∀ v : Vertex I,
        vertexPoint v a + vertexPoint v b - 1 ≤ monomial {a, b} (vertexPoint v) := by
      intro v
      rw [monomial, Finset.prod_pair hab]
      unfold vertexPoint
      split <;> split <;> norm_num
    have hexp := μ.expect_mono hpt
    have hval : μ.expect (fun v => vertexPoint v a + vertexPoint v b - 1) = x a + x b - 1 := by
      simp only [Law.expect_sub, Law.expect_add, Law.expect_const, hm a, hm b]
    rwa [hval] at hexp

omit [Fintype I] [DecidableEq I] in
/-- The minimal second moment dominates `L_2`: the adjacent-count law is
feasible, hence respects every pair's lower Fréchet bound. -/
theorem frechetPairLower_le_lowerMomentInt [Finite I] (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) : frechetPairLower s x ≤ lowerMomentInt s x 2 := by
  classical
  let := Fintype.ofFinite I
  obtain ⟨μ, hmean, hmom, -⟩ := exists_law_attaining_lower s x hx
  have hV : lowerMomentInt s x 2 = binomMoment s μ 2 := by
    rw [show (2 : ℤ) = ((2 : ℕ) : ℤ) from rfl, lowerMomentInt_natCast, hmom 2]
  rw [hV]
  exact frechetPairLower_le_binomMoment s x μ hmean

/-- **PB15**: `F_{n,2} = (C_2 - P_2) + (V_2 - L_2)`, using PB08. -/
theorem coeffF_two (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    coeffF s x 2 =
      (thresholdMoment s x 2 - elementaryInt s x 2) +
        (lowerMomentInt s x 2 - frechetPairLower s x) := by
  have h1 : (2 : ℤ) - 1 = 1 := by norm_num
  have hO := two_mul_orientMoment_two s x hx
  have hP : elementaryInt s x 1 = ∑ i ∈ s, x i := by
    rw [elementaryInt_eq_binomMoment s x hx]
    exact binomMoment_one s x _ (bernoulliLaw_hasMeans x hx)
  rw [coeffF, h1, thresholdMoment_one s x hx, hP]
  have hC : thresholdMoment s x 2 = binomMoment s (thresholdLaw x) 2 := rfl
  rw [hC] at *
  linarith [hO]

/-- **PB15**: the order-two coefficient is nonnegative. -/
theorem coeffF_two_nonneg (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    0 ≤ coeffF s x 2 := by
  rw [coeffF_two s x hx]
  have h1 : 0 ≤ thresholdMoment s x 2 - elementaryInt s x 2 :=
    sub_nonneg.mpr (elementaryInt_le_thresholdMoment s x hx 2)
  have h2 : 0 ≤ lowerMomentInt s x 2 - frechetPairLower s x :=
    sub_nonneg.mpr (frechetPairLower_le_lowerMomentInt s x hx)
  linarith

/-! ## PB16: the boundary recursions -/

/-- Under a law with prescribed means, a coordinate of mean zero fails on every
vertex of positive weight. -/
theorem vertex_eq_false_of_mean_zero {μ : Law (Vertex I)} {x : I → ℝ} (hm : HasMeans μ x)
    {a : I} (h0 : x a = 0) {v : Vertex I} (hv : 0 < μ.weight v) : v a = false := by
  by_contra hva
  have hva' : v a = true := by
    cases hvv : v a
    · exact absurd hvv hva
    · rfl
  have hzero : ∑ w : Vertex I, μ.weight w * vertexPoint w a = 0 := by
    rw [show ∑ w : Vertex I, μ.weight w * vertexPoint w a =
      μ.expect (fun w => vertexPoint w a) from rfl, hm a, h0]
  have hnn : ∀ w ∈ (Finset.univ : Finset (Vertex I)), 0 ≤ μ.weight w * vertexPoint w a :=
    fun w _ => mul_nonneg (μ.nonneg w) (by unfold vertexPoint; split <;> norm_num)
  have hterm := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp hzero v (Finset.mem_univ v)
  rw [vertexPoint, if_pos hva', mul_one] at hterm
  exact absurd hterm (ne_of_gt hv)

/-- Under a law with prescribed means, a coordinate of mean one succeeds on
every vertex of positive weight. -/
theorem vertex_eq_true_of_mean_one {μ : Law (Vertex I)} {x : I → ℝ} (hm : HasMeans μ x)
    {a : I} (h1 : x a = 1) {v : Vertex I} (hv : 0 < μ.weight v) : v a = true := by
  by_contra hva
  have hva' : v a = false := by
    cases hvv : v a
    · rfl
    · exact absurd hvv hva
  have hzero : ∑ w : Vertex I, μ.weight w * (1 - vertexPoint w a) = 0 := by
    have : μ.expect (fun w => 1 - vertexPoint w a) = 0 := by
      simp only [Law.expect_sub, Law.expect_const, hm a, h1, sub_self]
    rw [show ∑ w : Vertex I, μ.weight w * (1 - vertexPoint w a) =
      μ.expect (fun w => 1 - vertexPoint w a) from rfl, this]
  have hnn : ∀ w ∈ (Finset.univ : Finset (Vertex I)), 0 ≤ μ.weight w * (1 - vertexPoint w a) :=
    fun w _ => mul_nonneg (μ.nonneg w) (by unfold vertexPoint; split <;> norm_num)
  have hterm := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp hzero v (Finset.mem_univ v)
  rw [vertexPoint, if_neg (by simp [hva']), sub_zero, mul_one] at hterm
  exact absurd hterm (ne_of_gt hv)

omit [Fintype I] in
/-- Adding a failed coordinate does not change the success count. -/
theorem countOn_insert_of_false (s : Finset I) (a : I) {v : Vertex I}
    (hv : v a = false) : countOn (insert a s) v = countOn s v := by
  rw [countOn, countOn, Finset.filter_insert, if_neg (by simp [hv])]

omit [Fintype I] in
/-- Adding a successful coordinate raises the success count by one. -/
theorem countOn_insert_of_true {s : Finset I} {a : I} (ha : a ∉ s) {v : Vertex I}
    (hv : v a = true) : countOn (insert a s) v = countOn s v + 1 := by
  rw [countOn, countOn, Finset.filter_insert, if_pos hv,
    Finset.card_insert_of_notMem fun hmem => ha (Finset.mem_of_mem_filter a hmem)]

/-- **PB16**, law level, mean zero: a deterministic failed coordinate may be
deleted from the support. -/
theorem binomMoment_insert_of_mean_zero {μ : Law (Vertex I)} {x : I → ℝ} (hm : HasMeans μ x)
    {a : I} {s : Finset I} (h0 : x a = 0) (j : ℤ) :
    binomMoment (insert a s) μ j = binomMoment s μ j := by
  unfold binomMoment CubicGap.Law.expect
  refine Finset.sum_congr rfl fun v _ => ?_
  rcases (μ.nonneg v).lt_or_eq with hv | hv
  · simp only [countOn_insert_of_false s a (vertex_eq_false_of_mean_zero hm h0 hv)]
  · rw [← hv]; ring

/-- **PB16**, law level, mean one: a deterministic successful coordinate may be
deleted from the support at the cost of Pascal's identity. -/
theorem binomMoment_insert_of_mean_one {μ : Law (Vertex I)} {x : I → ℝ} (hm : HasMeans μ x)
    {a : I} {s : Finset I} (ha : a ∉ s) (h1 : x a = 1) (j : ℤ) :
    binomMoment (insert a s) μ j = binomMoment s μ j + binomMoment s μ (j - 1) := by
  rw [binomMoment, binomMoment, binomMoment, ← Law.expect_add]
  unfold CubicGap.Law.expect
  refine Finset.sum_congr rfl fun v _ => ?_
  rcases (μ.nonneg v).lt_or_eq with hv | hv
  · simp only [countOn_insert_of_true ha (vertex_eq_true_of_mean_one hm h1 hv), chooseInt_succ]
  · rw [← hv]; ring

/-- **PB16** for the common-threshold family, mean zero. -/
theorem thresholdMoment_insert_of_mean_zero {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {s : Finset I} (h0 : x a = 0) (j : ℤ) :
    thresholdMoment (insert a s) x j = thresholdMoment s x j :=
  binomMoment_insert_of_mean_zero (thresholdLaw_hasMeans x hx) h0 j

/-- **PB16** for the common-threshold family, mean one. -/
theorem thresholdMoment_insert_of_mean_one {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {s : Finset I} (ha : a ∉ s) (h1 : x a = 1) (j : ℤ) :
    thresholdMoment (insert a s) x j = thresholdMoment s x j + thresholdMoment s x (j - 1) :=
  binomMoment_insert_of_mean_one (thresholdLaw_hasMeans x hx) ha h1 j

omit [Fintype I] in
/-- **PB16** for the independent family, mean zero: peeling the deterministic
coordinate kills the term that carries it. -/
theorem elementaryInt_insert_of_mean_zero {x : I → ℝ} {a : I}
    {s : Finset I} (ha : a ∉ s) (h0 : x a = 0) (j : ℤ) :
    elementaryInt (insert a s) x j = elementaryInt s x j := by
  rcases lt_or_ge j 0 with hj | hj
  · rw [elementaryInt_of_neg _ _ hj, elementaryInt_of_neg _ _ hj]
  · obtain ⟨k, rfl⟩ := Int.eq_ofNat_of_zero_le hj
    match k with
    | 0 => rw [show ((0 : ℕ) : ℤ) = 0 from rfl, elementaryInt_zero, elementaryInt_zero]
    | (r + 1) =>
      rw [elementaryInt_natCast, elementaryInt_natCast,
        elementaryOn_peel (Finset.mem_insert_self a s) x r, Finset.erase_insert ha, h0,
        zero_mul, add_zero]

omit [Fintype I] in
/-- **PB16** for the independent family, mean one: peeling the deterministic
coordinate splits the moment across two consecutive orders. -/
theorem elementaryInt_insert_of_mean_one {x : I → ℝ} {a : I}
    {s : Finset I} (ha : a ∉ s) (h1 : x a = 1) (j : ℤ) :
    elementaryInt (insert a s) x j = elementaryInt s x j + elementaryInt s x (j - 1) := by
  rcases lt_or_ge j 0 with hj | hj
  · rw [elementaryInt_of_neg _ _ hj, elementaryInt_of_neg _ _ hj,
      elementaryInt_of_neg _ _ (show j - 1 < 0 by omega)]
    ring
  · obtain ⟨k, rfl⟩ := Int.eq_ofNat_of_zero_le hj
    match k with
    | 0 =>
      rw [show ((0 : ℕ) : ℤ) = 0 from rfl, elementaryInt_zero, elementaryInt_zero,
        elementaryInt_of_neg _ _ (show (0 : ℤ) - 1 < 0 by norm_num)]
      ring
    | (r + 1) =>
      have hj1 : ((r + 1 : ℕ) : ℤ) - 1 = ((r : ℕ) : ℤ) := by push_cast; ring
      rw [elementaryInt_natCast, elementaryInt_natCast, hj1, elementaryInt_natCast,
        elementaryOn_peel (Finset.mem_insert_self a s) x r, Finset.erase_insert ha, h1,
        one_mul]

/-- **PB16** for the orientation family, mean zero. -/
theorem orientMoment_insert_of_mean_zero {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {s : Finset I} (h0 : x a = 0) (j : ℤ) :
    orientMoment (insert a s) x j = orientMoment s x j :=
  binomMoment_insert_of_mean_zero (orientationLaw_hasMeans x hx) h0 j

/-- **PB16** for the orientation family, mean one. -/
theorem orientMoment_insert_of_mean_one {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {s : Finset I} (ha : a ∉ s) (h1 : x a = 1) (j : ℤ) :
    orientMoment (insert a s) x j = orientMoment s x j + orientMoment s x (j - 1) :=
  binomMoment_insert_of_mean_one (orientationLaw_hasMeans x hx) ha h1 j

omit [Fintype I] in
/-- **PB16** for the adjacent-count family, mean zero: the mean sum is
unchanged. -/
theorem lowerMomentInt_insert_of_mean_zero {x : I → ℝ} {a : I}
    {s : Finset I} (ha : a ∉ s) (h0 : x a = 0) (j : ℤ) :
    lowerMomentInt (insert a s) x j = lowerMomentInt s x j := by
  refine lowerMomentInt_congr_of_meanSum ?_ j
  rw [meanSum, meanSum, Finset.sum_insert ha, h0, zero_add]

omit [Fintype I] in
/-- **PB16** for the adjacent-count family, mean one: the mean sum shifts by
one, so the floor shifts by one and the fractional part is unchanged; Pascal's
identity then gives the recursion. -/
theorem lowerMomentInt_insert_of_mean_one {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {s : Finset I} (ha : a ∉ s) (h1 : x a = 1) (j : ℤ) :
    lowerMomentInt (insert a s) x j = lowerMomentInt s x j + lowerMomentInt s x (j - 1) := by
  have hsum : meanSum (insert a s) x = meanSum s x + 1 := by
    rw [meanSum, meanSum, Finset.sum_insert ha, h1, add_comm]
  have hfloor : countFloor (insert a s) x = countFloor s x + 1 := by
    rw [countFloor, countFloor, hsum, Nat.floor_add_one (meanSum_nonneg hx)]
  have hfrac : countFrac (insert a s) x = countFrac s x := by
    rw [countFrac, countFrac, hsum, hfloor]
    push_cast
    ring
  rw [lowerMomentInt, lowerMomentInt, lowerMomentInt, hfloor, hfrac,
    chooseInt_succ (countFloor s x + 1) j, chooseInt_succ (countFloor s x) j]
  ring

/-- **PB16**: a coordinate of mean zero is deterministic and may be deleted. -/
theorem coeffF_insert_of_mean_zero {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {s : Finset I} (ha : a ∉ s) (h0 : x a = 0) (j : ℤ) :
    coeffF (insert a s) x j = coeffF s x j := by
  rw [coeffF, coeffF, thresholdMoment_insert_of_mean_zero hx h0,
    thresholdMoment_insert_of_mean_zero hx h0,
    lowerMomentInt_insert_of_mean_zero ha h0,
    elementaryInt_insert_of_mean_zero ha h0,
    elementaryInt_insert_of_mean_zero ha h0,
    orientMoment_insert_of_mean_zero hx h0]

/-- **PB16**: a coordinate of mean one is deterministic, and deleting it splits
the coefficient across two consecutive orders. -/
theorem coeffF_insert_of_mean_one {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {s : Finset I} (ha : a ∉ s) (h1 : x a = 1) (j : ℤ) :
    coeffF (insert a s) x j = coeffF s x j + coeffF s x (j - 1) := by
  rw [coeffF, coeffF, coeffF, thresholdMoment_insert_of_mean_one hx ha h1,
    thresholdMoment_insert_of_mean_one hx ha h1,
    lowerMomentInt_insert_of_mean_one hx ha h1,
    elementaryInt_insert_of_mean_one ha h1,
    elementaryInt_insert_of_mean_one ha h1,
    orientMoment_insert_of_mean_one hx ha h1]
  ring

/-! ## PB17: spreading the global minimum and the global maximum -/

/-- The spreading move: decrease the coordinate `a` by `h` and increase the
coordinate `b` by `h`.  The mean sum is preserved. -/
def spreadPoint (x : I → ℝ) (a b : I) (h : ℝ) : I → ℝ :=
  Function.update (Function.update x a (x a - h)) b (x b + h)

omit [Fintype I] in
/-- The moved minimum. -/
@[simp] theorem spreadPoint_left {x : I → ℝ} {a b : I} (hab : a ≠ b) (h : ℝ) :
    spreadPoint x a b h a = x a - h := by
  rw [spreadPoint, Function.update_of_ne hab, Function.update_self]

omit [Fintype I] in
/-- The moved maximum. -/
@[simp] theorem spreadPoint_right (x : I → ℝ) (a b : I) (h : ℝ) :
    spreadPoint x a b h b = x b + h := Function.update_self _ _ _

omit [Fintype I] in
/-- Every other coordinate is untouched. -/
theorem spreadPoint_of_ne {x : I → ℝ} {a b : I} {i : I} (hia : i ≠ a) (hib : i ≠ b) (h : ℝ) :
    spreadPoint x a b h i = x i := by
  rw [spreadPoint, Function.update_of_ne hib, Function.update_of_ne hia]

omit [Fintype I] in
/-- Splitting a sum over the support at two distinct elements. -/
theorem sum_pair_erase {s : Finset I} {a b : I} (ha : a ∈ s) (hb : b ∈ s) (hab : a ≠ b)
    (f : I → ℝ) :
    ∑ i ∈ s, f i = f a + f b + ∑ i ∈ (s.erase a).erase b, f i := by
  have hb' : b ∈ s.erase a := Finset.mem_erase.mpr ⟨hab.symm, hb⟩
  rw [← Finset.add_sum_erase _ f ha, ← Finset.add_sum_erase _ f hb', ← add_assoc]

omit [Fintype I] in
/-- Peeling two distinct coordinates out of an elementary symmetric polynomial:
`e_{r+2} = E_{r+2} + (x a + x b) E_{r+1} + x a x b E_r`. -/
theorem elementaryOn_peel_two {s : Finset I} {a b : I} (ha : a ∈ s) (hb : b ∈ s) (hab : a ≠ b)
    (x : I → ℝ) (r : ℕ) :
    elementaryOn s (r + 2) x =
      elementaryOn ((s.erase a).erase b) (r + 2) x +
        (x a + x b) * elementaryOn ((s.erase a).erase b) (r + 1) x +
        x a * x b * elementaryOn ((s.erase a).erase b) r x := by
  have hb' : b ∈ s.erase a := Finset.mem_erase.mpr ⟨hab.symm, hb⟩
  have h1 : elementaryOn s (r + 2) x =
      elementaryOn (s.erase a) (r + 2) x + x a * elementaryOn (s.erase a) (r + 1) x :=
    elementaryOn_peel ha x (r + 1)
  have h2 : elementaryOn (s.erase a) (r + 2) x =
      elementaryOn ((s.erase a).erase b) (r + 2) x +
        x b * elementaryOn ((s.erase a).erase b) (r + 1) x :=
    elementaryOn_peel hb' x (r + 1)
  have h3 : elementaryOn (s.erase a) (r + 1) x =
      elementaryOn ((s.erase a).erase b) (r + 1) x +
        x b * elementaryOn ((s.erase a).erase b) r x :=
    elementaryOn_peel hb' x r
  rw [h1, h2, h3]
  ring

/-- Peeling the global minimum and the global maximum out of a common-threshold
moment of order at least two.  Since the order is at least two the maximum
carries coefficient zero, so the minimum's coefficient is exactly
`binom(n - 1, r + 1)`.  Ties are irrelevant: the hypotheses only say that `a`
attains the minimum and `b` the maximum. -/
theorem thresholdMoment_peel_two {s : Finset I} {a b : I} (ha : a ∈ s) (hb : b ∈ s)
    (hab : a ≠ b) {x : I → ℝ} (hx : x ∈ cube I) (hmin : ∀ i ∈ s, x a ≤ x i)
    (hmax : ∀ i ∈ s, x i ≤ x b) (r : ℕ) :
    thresholdMoment s x ((r + 2 : ℕ) : ℤ) =
      x a * (((s.card - 1).choose (r + 1) : ℕ) : ℝ) +
        (thresholdMoment ((s.erase a).erase b) x ((r + 2 : ℕ) : ℤ) +
          thresholdMoment ((s.erase a).erase b) x ((r + 1 : ℕ) : ℤ)) := by
  have hcard2 : 2 ≤ s.card := Finset.one_lt_card.mpr ⟨a, ha, b, hb, hab⟩
  have ha' : a ∈ s.erase b := Finset.mem_erase.mpr ⟨hab, ha⟩
  have hmin' : ∀ i ∈ s.erase b, x a ≤ x i := fun i hi => hmin i (Finset.mem_of_mem_erase hi)
  have hcardb : (s.erase b).card = s.card - 1 := Finset.card_erase_of_mem hb
  have hstep0 : thresholdMoment s x ((r + 2 : ℕ) : ℤ) =
      thresholdMoment (s.erase b) x ((r + 2 : ℕ) : ℤ) +
        thresholdMoment (s.erase b) x ((r + 1 : ℕ) : ℤ) :=
    thresholdLaw_binomMoment_peel_max hb x hx hmax r
  have hstep1 : thresholdMoment (s.erase b) x ((r + 2 : ℕ) : ℤ) =
      x a * ((((s.erase b).card - 1).choose (r + 1) : ℕ) : ℝ) +
        thresholdMoment ((s.erase b).erase a) x ((r + 2 : ℕ) : ℤ) :=
    thresholdLaw_binomMoment_peel_min ha' x hx hmin' (r + 1)
  have hstep2 : thresholdMoment (s.erase b) x ((r + 1 : ℕ) : ℤ) =
      x a * ((((s.erase b).card - 1).choose r : ℕ) : ℝ) +
        thresholdMoment ((s.erase b).erase a) x ((r + 1 : ℕ) : ℤ) :=
    thresholdLaw_binomMoment_peel_min ha' x hx hmin' r
  have hcb : (s.erase b).card - 1 = s.card - 2 := by rw [hcardb]; omega
  have hpascal : ((s.erase b).card - 1).choose (r + 1) + ((s.erase b).card - 1).choose r =
      (s.card - 1).choose (r + 1) := by
    have hrw : s.card - 1 = (s.card - 2) + 1 := by omega
    rw [hcb, hrw, Nat.choose_succ_succ']
    ring
  have herase : (s.erase b).erase a = (s.erase a).erase b := Finset.erase_right_comm
  rw [hstep0, hstep1, hstep2, herase]
  have hcast : ((((s.erase b).card - 1).choose (r + 1) : ℕ) : ℝ) +
      ((((s.erase b).card - 1).choose r : ℕ) : ℝ) = (((s.card - 1).choose (r + 1) : ℕ) : ℝ) := by
    rw [← Nat.cast_add, hpascal]
  linear_combination x a * hcast

omit [Fintype I] in
/-- **PB17, the independent-rounding estimate.**  Spreading a coordinate `a`
down by `h` and a coordinate `b` up by `h` lowers the sum of the two
consecutive independent-rounding moments by at most `h binom(n - 1, m + 1)`.
The exact change of each moment is `h (x b - x a + h) E_r` on the `n - 2`
untouched coordinates (`elementaryOn_peel_two`); the factor `x b - x a + h`
lies in `[0, 1]`, and `E_{m+1} + E_m` on `n - 2` coordinates is at most
`binom(n - 1, m + 1)` by `elementaryOn_le_choose` and Pascal's identity.
Neither coordinate need be extremal, and no ordering of `x a` and `x b` is
assumed. -/
theorem elementaryInt_spread_sub_le {s : Finset I} {a b : I} (ha : a ∈ s) (hb : b ∈ s)
    (hab : a ≠ b) {x : I → ℝ} (hx : x ∈ cube I) {h : ℝ} (hh0 : 0 ≤ h)
    (hhb : h ≤ 1 - x b) (m : ℕ) :
    (elementaryInt s x ((m + 3 : ℕ) : ℤ) + elementaryInt s x ((m + 2 : ℕ) : ℤ)) -
        (elementaryInt s (spreadPoint x a b h) ((m + 3 : ℕ) : ℤ) +
          elementaryInt s (spreadPoint x a b h) ((m + 2 : ℕ) : ℤ)) ≤
      h * (((s.card - 1).choose (m + 1) : ℕ) : ℝ) := by
  classical
  set y := spreadPoint x a b h with hydef
  set t := (s.erase a).erase b with htdef
  have hya : y a = x a - h := spreadPoint_left hab h
  have hyb : y b = x b + h := spreadPoint_right x a b h
  have hxy : ∀ i ∈ t, x i = y i := by
    intro i hi
    have hib : i ≠ b := (Finset.mem_erase.mp hi).1
    have hia : i ≠ a := (Finset.mem_erase.mp (Finset.mem_of_mem_erase hi)).1
    exact (spreadPoint_of_ne hia hib h).symm
  have hcard2 : 2 ≤ s.card := Finset.one_lt_card.mpr ⟨a, ha, b, hb, hab⟩
  have hcardt : t.card = s.card - 2 := by
    rw [htdef, Finset.card_erase_of_mem (Finset.mem_erase.mpr ⟨hab.symm, hb⟩),
      Finset.card_erase_of_mem ha]
    omega
  have hEcongr : ∀ r : ℕ, elementaryOn t r x = elementaryOn t r y := fun r =>
    Finset.sum_congr rfl fun A hA =>
      Finset.prod_congr rfl fun i hi => hxy i ((Finset.mem_powersetCard.mp hA).1 hi)
  have hPgen : ∀ r : ℕ,
      elementaryOn s (r + 2) x - elementaryOn s (r + 2) y =
        h * (x b - x a + h) * elementaryOn t r x := by
    intro r
    rw [elementaryOn_peel_two ha hb hab x r, elementaryOn_peel_two ha hb hab y r,
      hya, hyb, ← htdef, ← hEcongr (r + 2), ← hEcongr (r + 1), ← hEcongr r]
    ring
  have hEnn : ∀ r : ℕ, 0 ≤ elementaryOn t r x := fun r => elementaryOn_nonneg t hx r
  have hEle : elementaryOn t (m + 1) x + elementaryOn t m x ≤
      (((s.card - 1).choose (m + 1) : ℕ) : ℝ) := by
    have h1 := elementaryOn_le_choose t hx (m + 1)
    have h2 := elementaryOn_le_choose t hx m
    have hpascal : t.card.choose (m + 1) + t.card.choose m = (s.card - 1).choose (m + 1) := by
      have hrw : s.card - 1 = (s.card - 2) + 1 := by omega
      rw [hcardt, hrw, Nat.choose_succ_succ']
      ring
    have hcast : ((t.card.choose (m + 1) : ℕ) : ℝ) + ((t.card.choose m : ℕ) : ℝ) =
        (((s.card - 1).choose (m + 1) : ℕ) : ℝ) := by
      rw [← Nat.cast_add, hpascal]
    linarith
  have hq1 : x b - x a + h ≤ 1 := by linarith [(hx a).1]
  have hsum : (elementaryInt s x ((m + 3 : ℕ) : ℤ) + elementaryInt s x ((m + 2 : ℕ) : ℤ)) -
      (elementaryInt s y ((m + 3 : ℕ) : ℤ) + elementaryInt s y ((m + 2 : ℕ) : ℤ)) =
      h * ((x b - x a + h) * (elementaryOn t (m + 1) x + elementaryOn t m x)) := by
    simp only [elementaryInt_natCast]
    have hA : elementaryOn s (m + 3) x - elementaryOn s (m + 3) y =
        h * (x b - x a + h) * elementaryOn t (m + 1) x := hPgen (m + 1)
    have hB : elementaryOn s (m + 2) x - elementaryOn s (m + 2) y =
        h * (x b - x a + h) * elementaryOn t m x := hPgen m
    linarith [hA, hB]
  rw [hsum]
  have hEsum0 : 0 ≤ elementaryOn t (m + 1) x + elementaryOn t m x :=
    add_nonneg (hEnn (m + 1)) (hEnn m)
  have hstep : (x b - x a + h) * (elementaryOn t (m + 1) x + elementaryOn t m x) ≤
      1 * (((s.card - 1).choose (m + 1) : ℕ) : ℝ) :=
    mul_le_mul hq1 hEle hEsum0 zero_le_one
  rw [one_mul] at hstep
  exact mul_le_mul_of_nonneg_left hstep hh0

/-- **PB17**: moving a global minimum down by `h` and a global maximum up by `h`
does not increase the coefficient, for every order at least three. -/
theorem coeffF_spread_le {s : Finset I} {a b : I} (ha : a ∈ s) (hb : b ∈ s) (hab : a ≠ b)
    {x : I → ℝ} (hx : x ∈ cube I) (hmin : ∀ i ∈ s, x a ≤ x i) (hmax : ∀ i ∈ s, x i ≤ x b)
    {h : ℝ} (hh0 : 0 ≤ h) (hha : h ≤ x a) (hhb : h ≤ 1 - x b) {j : ℤ} (hj : 3 ≤ j) :
    coeffF s (spreadPoint x a b h) j ≤ coeffF s x j := by
  classical
  obtain ⟨m, rfl⟩ : ∃ m : ℕ, j = (m : ℤ) + 3 := ⟨(j - 3).toNat, by omega⟩
  set y := spreadPoint x a b h with hydef
  set t := (s.erase a).erase b with htdef
  -- basic values of the moved point
  have hya : y a = x a - h := spreadPoint_left hab h
  have hyb : y b = x b + h := spreadPoint_right x a b h
  have hyo : ∀ i, i ≠ a → i ≠ b → y i = x i := fun i hia hib => spreadPoint_of_ne hia hib h
  have hycube : y ∈ cube I := by
    intro i
    by_cases hib : i = b
    · subst hib; rw [hyb]; exact ⟨by linarith [(hx i).1], by linarith⟩
    · by_cases hia : i = a
      · subst hia; rw [hya]; exact ⟨by linarith, by linarith [(hx i).2]⟩
      · rw [hyo i hia hib]; exact hx i
  have hab' : x a ≤ x b := hmin b hb
  have hymin : ∀ i ∈ s, y a ≤ y i := by
    intro i hi
    by_cases hib : i = b
    · subst hib; rw [hya, hyb]; linarith
    · by_cases hia : i = a
      · subst hia; exact le_rfl
      · rw [hyo i hia hib, hya]; linarith [hmin i hi]
  have hymax : ∀ i ∈ s, y i ≤ y b := by
    intro i hi
    by_cases hib : i = b
    · subst hib; exact le_rfl
    · by_cases hia : i = a
      · subst hia; rw [hya, hyb]; linarith
      · rw [hyo i hia hib, hyb]; linarith [hmax i hi]
  have hxy : ∀ i ∈ t, x i = y i := by
    intro i hi
    have hib : i ≠ b := (Finset.mem_erase.mp hi).1
    have hia : i ≠ a := (Finset.mem_erase.mp (Finset.mem_of_mem_erase hi)).1
    exact (hyo i hia hib).symm
  -- order bookkeeping
  have e3 : (m : ℤ) + 3 = ((m + 3 : ℕ) : ℤ) := by push_cast; ring
  have e2 : ((m + 3 : ℕ) : ℤ) - 1 = ((m + 2 : ℕ) : ℤ) := by push_cast; ring
  set B2 : ℝ := (((s.card - 1).choose (m + 2) : ℕ) : ℝ) with hB2
  set B1 : ℝ := (((s.card - 1).choose (m + 1) : ℕ) : ℝ) with hB1
  -- (5): the exact change of the common-threshold moments
  have hCgen : ∀ r : ℕ,
      thresholdMoment s y ((r + 2 : ℕ) : ℤ) =
        thresholdMoment s x ((r + 2 : ℕ) : ℤ) - h * (((s.card - 1).choose (r + 1) : ℕ) : ℝ) := by
    intro r
    rw [thresholdMoment_peel_two ha hb hab hx hmin hmax r,
      thresholdMoment_peel_two ha hb hab hycube hymin hymax r, hya,
      thresholdMoment_congr hx hycube hxy ((r + 2 : ℕ) : ℤ),
      thresholdMoment_congr hx hycube hxy ((r + 1 : ℕ) : ℤ)]
    ring
  have hCj : thresholdMoment s y ((m + 3 : ℕ) : ℤ) =
      thresholdMoment s x ((m + 3 : ℕ) : ℤ) - h * B2 := hCgen (m + 1)
  have hCj1 : thresholdMoment s y ((m + 2 : ℕ) : ℤ) =
      thresholdMoment s x ((m + 2 : ℕ) : ℤ) - h * B1 := hCgen m
  -- the adjacent-count moment is constant along the path
  have hmean : meanSum s x = meanSum s y := by
    rw [meanSum, meanSum, sum_pair_erase ha hb hab x, sum_pair_erase ha hb hab y, hya, hyb]
    have : ∑ i ∈ t, x i = ∑ i ∈ t, y i := Finset.sum_congr rfl fun i hi => hxy i hi
    rw [← htdef, this]
    ring
  have hV : lowerMomentInt s y ((m + 3 : ℕ) : ℤ) = lowerMomentInt s x ((m + 3 : ℕ) : ℤ) :=
    (lowerMomentInt_congr_of_meanSum hmean _).symm
  -- (6): the exact change of the independent moments, and its estimate
  have hP := elementaryInt_spread_sub_le ha hb hab hx hh0 hhb m
  rw [← hydef, ← hB1] at hP
  -- PB09: the orientation moment cannot drop by more than the Lipschitz amount
  have hO : orientMoment s x ((m + 3 : ℕ) : ℤ) - orientMoment s y ((m + 3 : ℕ) : ℤ) ≤
      h * B2 := by
    set z : I → ℝ := Function.update x a (x a - h) with hzdef
    have hza : z a = x a - h := Function.update_self _ _ _
    have hzo : ∀ i, i ≠ a → z i = x i := fun i hia => Function.update_of_ne hia _ _
    have hzcube : z ∈ cube I :=
      update_mem_cube hx a (by linarith) (by linarith [(hx a).2])
    have hback : Function.update z a (x a) = x := by
      rw [hzdef, Function.update_idem, Function.update_eq_self]
    have hstep1 : orientMoment s x ((m + 3 : ℕ) : ℤ) - orientMoment s z ((m + 3 : ℕ) : ℤ) ≤
        (x a - z a) * (((s.card - 1).choose (m + 2) : ℕ) : ℝ) := by
      have := orientMoment_update_sub_le s (x := z) a hzcube (hx a).1 (hx a).2
        (by rw [hza]; linarith) (m + 2)
      rwa [hback] at this
    have hstep2 : orientMoment s z ((m + 3 : ℕ) : ℤ) ≤ orientMoment s y ((m + 3 : ℕ) : ℤ) := by
      refine orientMoment_mono s (fun i => ?_) _
      by_cases hib : i = b
      · subst hib
        rw [hyb, hzo i hab.symm]
        linarith
      · by_cases hia : i = a
        · subst hia; rw [hya, hza]
        · rw [hyo i hia hib, hzo i hia]
    rw [hza] at hstep1
    have : x a - (x a - h) = h := by ring
    rw [this] at hstep1
    linarith
  -- assembling
  rw [coeffF, coeffF, e3, e2]
  linarith [hCj, hCj1, hV, hP, hO]

/-! ## PB18: nonnegativity -/

omit [Fintype I] [DecidableEq I] in
/-- A maximizing coordinate of a nonempty support always exists. -/
theorem exists_max_anchor (s : Finset I) (hs : s.Nonempty) (x : I → ℝ) :
    ∃ i ∈ s, ∀ j ∈ s, x j ≤ x i := by
  obtain ⟨i, hi, hv⟩ := Finset.exists_mem_eq_sup' hs x
  exact ⟨i, hi, fun j hj => hv ▸ Finset.le_sup' x hj⟩

/-- The non-inductive orders: at most two, or above the support cardinality. -/
theorem coeffF_nonneg_base (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) (j : ℤ)
    (h : j ≤ 2 ∨ (s.card : ℤ) < j) : 0 ≤ coeffF s x j := by
  rcases h with hj | hj
  · rcases lt_or_ge j 0 with hneg | hpos
    · rw [coeffF_of_neg s x hneg]
    · interval_cases j
      · rw [coeffF_zero]
      · rw [coeffF_one s x hx]
      · exact coeffF_two_nonneg s x hx
  · rcases lt_trichotomy ((s.card : ℤ) + 1) j with hgt | heq | hlt
    · rw [coeffF_of_card_add_one_lt s x hx hgt]
    · rw [← heq]
      exact coeffF_card_add_one_nonneg s x hx
    · omega

/-- **PB18**, the induction on the support cardinality. -/
theorem coeffF_nonneg_of_card_le : ∀ (n : ℕ) (s : Finset I) (x : I → ℝ),
    s.card ≤ n → x ∈ cube I → ∀ j : ℤ, 0 ≤ coeffF s x j := by
  intro n
  induction n with
  | zero =>
    intro s x hcard hx j
    have hs : s.card = 0 := Nat.le_zero.mp hcard
    refine coeffF_nonneg_base s x hx j ?_
    rcases le_or_gt j 2 with h | h
    · exact Or.inl h
    · right; omega
  | succ n ih =>
    have hbd : ∀ (s : Finset I) (x : I → ℝ), s.card ≤ n + 1 → x ∈ cube I →
        (∃ a ∈ s, x a = 0 ∨ x a = 1) → ∀ j : ℤ, 0 ≤ coeffF s x j := by
      rintro s x hcard hx ⟨a, ha, hval⟩ j
      have hins : insert a (s.erase a) = s := Finset.insert_erase ha
      have hane : a ∉ s.erase a := Finset.notMem_erase a s
      have hpos : 1 ≤ s.card := Finset.card_pos.mpr ⟨a, ha⟩
      have hcard' : (s.erase a).card ≤ n := by
        rw [Finset.card_erase_of_mem ha]; omega
      rcases hval with h0 | h1
      · rw [← hins, coeffF_insert_of_mean_zero hx hane h0]
        exact ih _ _ hcard' hx j
      · rw [← hins, coeffF_insert_of_mean_one hx hane h1]
        exact add_nonneg (ih _ _ hcard' hx j) (ih _ _ hcard' hx (j - 1))
    intro s x hcard hx j
    rcases le_or_gt j 2 with hj2 | hj2
    · exact coeffF_nonneg_base s x hx j (Or.inl hj2)
    rcases lt_or_ge (s.card : ℤ) j with hjn | hjn
    · exact coeffF_nonneg_base s x hx j (Or.inr hjn)
    -- the spreading regime: `3 ≤ j ≤ n`
    have hcard2 : 2 ≤ s.card := by omega
    have hsne : s.Nonempty := Finset.card_pos.mp (by omega)
    obtain ⟨a, ha, hmin⟩ := monomial_min_anchor s hsne x
    have hene : (s.erase a).Nonempty := by
      rw [← Finset.card_pos, Finset.card_erase_of_mem ha]
      omega
    obtain ⟨b, hb', hmax'⟩ := exists_max_anchor (s.erase a) hene x
    have hb : b ∈ s := Finset.mem_of_mem_erase hb'
    have hab : a ≠ b := fun hh => (Finset.mem_erase.mp hb').1 hh.symm
    have hmax : ∀ i ∈ s, x i ≤ x b := by
      intro i hi
      by_cases hia : i = a
      · subst hia; exact hmin b hb
      · exact hmax' i (Finset.mem_erase.mpr ⟨hia, hi⟩)
    set h : ℝ := min (x a) (1 - x b) with hhdef
    have hh0 : 0 ≤ h := le_min (hx a).1 (by linarith [(hx b).2])
    have hha : h ≤ x a := min_le_left _ _
    have hhb : h ≤ 1 - x b := min_le_right _ _
    set y := spreadPoint x a b h with hydef
    have hycube : y ∈ cube I := by
      intro i
      by_cases hib : i = b
      · subst hib
        rw [hydef, spreadPoint_right]
        exact ⟨by linarith [(hx i).1], by linarith⟩
      · by_cases hia : i = a
        · subst hia
          rw [hydef, spreadPoint_left hab]
          exact ⟨by linarith, by linarith [(hx i).2]⟩
        · rw [hydef, spreadPoint_of_ne hia hib]; exact hx i
    have hbdry : ∃ c ∈ s, y c = 0 ∨ y c = 1 := by
      rcases min_cases (x a) (1 - x b) with ⟨heq, -⟩ | ⟨heq, -⟩
      · refine ⟨a, ha, Or.inl ?_⟩
        rw [hydef, spreadPoint_left hab, hhdef, heq]
        ring
      · refine ⟨b, hb, Or.inr ?_⟩
        rw [hydef, spreadPoint_right, hhdef, heq]
        ring
    have hstep := coeffF_spread_le ha hb hab hx hmin hmax hh0 hha hhb (show (3 : ℤ) ≤ j by omega)
    have hzero := hbd s y hcard hycube hbdry j
    rw [← hydef] at hstep
    linarith

/-- **PB18**: the coefficient `F_{n,j} = 2 C_j + V_j - P_j - 2 O_j + C_{j-1} - P_{j-1}`
is nonnegative for every support, every point of the cube and every integer
order. -/
theorem coeffF_nonneg (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) (j : ℤ) :
    0 ≤ coeffF s x j :=
  coeffF_nonneg_of_card_le s.card s x le_rfl hx j

end

end MultilinearGap
