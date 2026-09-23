import Formal.MultilinearGap.BalancedOrientation
import Formal.MultilinearGap.CoefficientInequality

/-!
# Balanced orientation moments and the restricted coefficient

This module discharges PB29 of `formal/topics/18-positive-box/CLAIMS.md` and
supplies the part of PB30 that does not depend on the spreading induction,
following `notes/review-positive-box-balanced-orientation-closure.md`.

## The moment family

`balancedOrientMoment S x j` is `O^bal_j`, the `j`-th binomial moment of the
success count on the support `S` under the **ambient** balanced orientation law
`balancedOrientationLaw x` of `Formal.MultilinearGap.BalancedOrientation`.  It
is a `binomMoment`, so the PB12 conventions of
`Formal.MultilinearGap.PhysicalEnvelope` (order zero is one, negative orders
vanish, orders above the support cardinality vanish) hold for it verbatim, as
for `thresholdMoment` and `orientMoment`. The `lowerMomentInt` and
`elementaryInt` families prove the same conventions from their own definitions.

**The definitions retain the ambient law.**  The law argument of
`binomMoment` is the ambient `balancedOrientationLaw x` on `Vertex I`, where the
ambient dimension is `N = Fintype.card I`; the support `S : Finset I` only
selects which coordinates are counted.  There is no law indexed by `S`, so a
statement about a smaller support is a statement about the restriction of the
one ambient law by construction, never about a balanced law resampled in
dimension `#S`.  The definitions retain the ambient constants
`pairOppositeProb (Fintype.card I)` and `orientationBeta (Fintype.card I)` as
`S` shrinks. Replacing them by support-size constants is invalid in general.
This is a property of these definitions and proofs, not a type-level prohibition:
`pairOppositeProb S.card` is expressible, and a different law could be constructed
on the support and extended to the ambient coordinates. The difference matters:
at `N = 4`, `S = {a, b}` and `x ≡ 1/2` one has `O^bal_2 = 1/6 = (1 - p_4) C_2 + p_4 L_2`,
whereas the resampled `p_2 = 1` would give `0`.

## PB29

`balancedOrientMoment_two` is `O^bal_2 = (1 - p_N) C_2 + p_N L_2`, with
`L_2 = frechetPairLower` and `C_2 = thresholdMoment _ _ 2`.  The per-pair reason
is `balancedOrientationLaw_expect_pair`: conditionally on the ambient low set
`H`, a pair with equal orientations has the upper Fréchet value `min (u a) (u b)`
and a pair with opposite orientations the lower one `max 0 (u a + u b - 1)`
(`intervalIntegral_orientedProb_pair`), and PB28
(`balancedSubsets_pair_opposite`) says the second event has ambient probability
exactly `p_N`.  Since the identity is proved pairwise it holds for every support
and therefore for every restriction, with the ambient `p_N` throughout.

At the fair value `p_N = 1/2` the identity degenerates to
`O_2 = (C_2 + L_2)/2`, which is PB08 (`two_mul_orientMoment_two`).

`orientationBeta_mul_thresholdMoment_sub_balancedOrientMoment_two` is the form
the coefficient uses: `β_N (C_2 - O^bal_2) = C_2 - L_2`, by `β_N p_N = 1`.

## The restricted coefficient

`balancedCoeffF S x j` is
`F_{S,j} = β_N C_j + V_j - P_j - β_N O^bal_j + C_{j-1} - P_{j-1}` with
`β_N = orientationBeta (Fintype.card I)`, the exact analogue of the fair
`coeffF` of `Formal.MultilinearGap.CoefficientInequality` with `2` replaced by
`β_N` and `O_j` by `O^bal_j`.  Proved here:

* order conventions: `balancedCoeffF_of_neg`, `balancedCoeffF_zero`,
  `balancedCoeffF_one`;
* top order: `balancedCoeffF_card_add_one`,
  `balancedCoeffF_card_add_one_nonneg`, `balancedCoeffF_of_card_add_one_lt`;
* the pair base case: `balancedCoeffF_two`, `balancedCoeffF_two_nonneg`;
* the boundary recursions `balancedCoeffF_insert_of_mean_zero` and
  `balancedCoeffF_insert_of_mean_one`, through the balanced-family recursions
  `balancedOrientMoment_insert_of_mean_zero` and
  `balancedOrientMoment_insert_of_mean_one`.  Both are instances of the
  law-level `binomMoment_insert_of_mean_zero` / `binomMoment_insert_of_mean_one`
  applied to the ambient law, which is exactly the source's requirement that
  deleting a deterministic coordinate must not condition on its orientation
  coin: the law is untouched, only the counted support shrinks, so the
  correlations among the remaining coins are irrelevant;
* `balancedCoeffF_nonneg_base`, the assembly of the non-inductive orders.

**Deliberately not proved here**: the spreading step and the induction of PB30.
The spreading step needs the balanced orientation moments to be coordinatewise
monotone with the Lipschitz constant `binom(n-1, j-1)`
(`balancedOrientMoment_mono` and `balancedOrientMoment_update_sub_le` below
supply exactly that, by the coupling on the shared `H` and `U`), and then the
same finite comparisons for `C`, `V` and `P` that the fair argument of
`CoefficientInequality` already performs; in the assembly the fair `2` is
replaced by `β_N` and nothing else changes.
-/

namespace MultilinearGap

open CubicGap MeasureTheory Set

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-! ## The conditional orientation coins as threshold indicators -/

omit [Fintype I] in
/-- The conditional success probability of a coordinate is a threshold
indicator: a low coordinate succeeds on `[0, u i]`, a high coordinate fails on
`[0, 1 - u i]`. -/
theorem orientedProb_eq_lowerStep (H : Finset I) (x : I → ℝ) (t : ℝ) (i : I) :
    orientedProb H x t i =
      if i ∈ H then lowerStep (x i) t else 1 - lowerStep (1 - x i) t := by
  simp only [orientedProb, lowerStep]
  split_ifs <;> first | rfl | linarith

omit [Fintype I] in
/-- Conditional orientation monomials take values in the unit interval. -/
theorem orientedProb_monomial_mem_Icc (H : Finset I) (x : I → ℝ) (A : Finset I) (t : ℝ) :
    monomial A (orientedProb H x t) ∈ Icc (0 : ℝ) 1 :=
  ⟨Finset.prod_nonneg fun i _ => (orientedProb_cube H x t i).1,
    Finset.prod_le_one (fun i _ => (orientedProb_cube H x t i).1)
      fun i _ => (orientedProb_cube H x t i).2⟩

omit [Fintype I] in
/-- Conditional orientation monomials are integrable in the shared uniform
variable. -/
theorem orientedProb_monomial_integrable (H : Finset I) (x : I → ℝ) (A : Finset I) :
    IntervalIntegrable (fun t => monomial A (orientedProb H x t)) volume 0 1 :=
  intervalIntegrable_of_mem_unitInterval _
    (Finset.measurable_prod _ fun i _ => orientedProb_measurable H x i)
    (orientedProb_monomial_mem_Icc H x A)

omit [Fintype I] in
/-- **The per-pair Fréchet dichotomy.**  Given the ambient low set `H`, one
uniform variable drives both coordinates of a pair: equal orientations make the
two success events nested, giving the upper Fréchet value `min (u a) (u b)`, and
opposite orientations make them overlap in a single interval, giving the lower
Fréchet value `max 0 (u a + u b - 1)`. -/
theorem intervalIntegral_orientedProb_pair (H : Finset I) {x : I → ℝ} (hx : x ∈ cube I)
    (a b : I) :
    (∫ t in (0 : ℝ)..1, orientedProb H x t a * orientedProb H x t b) =
      if OppositeOrientation H a b then max 0 (x a + x b - 1) else min (x a) (x b) := by
  have ha : x a ∈ Icc (0 : ℝ) 1 := Set.mem_Icc.mpr (hx a)
  have hb : x b ∈ Icc (0 : ℝ) 1 := Set.mem_Icc.mpr (hx b)
  have ha' : 1 - x a ∈ Icc (0 : ℝ) 1 :=
    Set.mem_Icc.mpr ⟨by linarith [(hx a).2], by linarith [(hx a).1]⟩
  have hb' : 1 - x b ∈ Icc (0 : ℝ) 1 :=
    Set.mem_Icc.mpr ⟨by linarith [(hx b).2], by linarith [(hx b).1]⟩
  -- the opposite-orientation integral, in the orientation `u` low and `v` high
  have key : ∀ u v : ℝ, u ∈ Icc (0 : ℝ) 1 → v ∈ Icc (0 : ℝ) 1 →
      (∫ t in (0 : ℝ)..1, lowerStep u t * (1 - lowerStep (1 - v) t)) =
        max 0 (u + v - 1) := by
    intro u v hu hv
    have hpt : ∀ t : ℝ, lowerStep u t * (1 - lowerStep (1 - v) t) =
        lowerStep u t - lowerStep (min u (1 - v)) t := by
      intro t
      rw [← lowerStep_mul]
      ring
    have hmin : min u (1 - v) ∈ Icc (0 : ℝ) 1 :=
      Set.mem_Icc.mpr ⟨le_min hu.1 (by linarith [hv.2]), (min_le_left _ _).trans hu.2⟩
    simp_rw [hpt]
    rw [intervalIntegral.integral_sub (lowerStep_integrable u)
        (lowerStep_integrable (min u (1 - v))),
      integral_lowerStep hu, integral_lowerStep hmin]
    rcases le_total u (1 - v) with h | h
    · rw [min_eq_left h, max_eq_left (by linarith)]
      ring
    · rw [min_eq_right h, max_eq_right (by linarith)]
      ring
  by_cases hA : a ∈ H <;> by_cases hB : b ∈ H
  · -- both low: equal orientations
    rw [if_neg (by simp [OppositeOrientation, hA, hB])]
    simp only [orientedProb_eq_lowerStep, if_pos hA, if_pos hB]
    exact integral_lowerStep_mul ha hb
  · -- `a` low, `b` high: opposite orientations
    rw [if_pos (show OppositeOrientation H a b from Or.inl ⟨hA, hB⟩)]
    simp only [orientedProb_eq_lowerStep, if_pos hA, if_neg hB]
    exact key _ _ ha hb
  · -- `a` high, `b` low: opposite orientations
    rw [if_pos (show OppositeOrientation H a b from Or.inr ⟨hB, hA⟩)]
    simp only [orientedProb_eq_lowerStep, if_neg hA, if_pos hB]
    have hcomm : ∀ t : ℝ, (1 - lowerStep (1 - x a) t) * lowerStep (x b) t =
        lowerStep (x b) t * (1 - lowerStep (1 - x a) t) := fun t => mul_comm _ _
    simp_rw [hcomm]
    rw [key _ _ hb ha, add_comm (x b) (x a)]
  · -- both high: equal orientations
    rw [if_neg (by simp [OppositeOrientation, hA, hB])]
    simp only [orientedProb_eq_lowerStep, if_neg hA, if_neg hB]
    have hpt : ∀ t : ℝ, (1 - lowerStep (1 - x a) t) * (1 - lowerStep (1 - x b) t) =
        1 - lowerStep (1 - x a) t - lowerStep (1 - x b) t +
          lowerStep (min (1 - x a) (1 - x b)) t := by
      intro t
      rw [← lowerStep_mul]
      ring
    have hmin : min (1 - x a) (1 - x b) ∈ Icc (0 : ℝ) 1 :=
      Set.mem_Icc.mpr ⟨le_min (Set.mem_Icc.mp ha').1 (Set.mem_Icc.mp hb').1,
        (min_le_left _ _).trans (Set.mem_Icc.mp ha').2⟩
    have hint1 := lowerStep_integrable (1 - x a)
    have hint2 := lowerStep_integrable (1 - x b)
    have hint3 := lowerStep_integrable (min (1 - x a) (1 - x b))
    simp_rw [hpt]
    rw [intervalIntegral.integral_add ((intervalIntegrable_const.sub hint1).sub hint2) hint3,
      intervalIntegral.integral_sub (intervalIntegrable_const.sub hint1) hint2,
      intervalIntegral.integral_sub intervalIntegrable_const hint1,
      integral_lowerStep ha', integral_lowerStep hb', integral_lowerStep hmin]
    simp only [intervalIntegral.integral_const, smul_eq_mul, sub_zero, mul_one]
    rcases le_total (x a) (x b) with h | h
    · rw [min_eq_left h, min_eq_right (by linarith)]
      ring
    · rw [min_eq_right h, min_eq_left (by linarith)]
      ring

/-- **PB29, the per-pair identity.**  Under the ambient balanced law a distinct
pair is oppositely oriented with probability exactly `p_N`, so its expectation
is the `p_N`-mixture of the two Fréchet values.  The constant is the ambient one
for every pair of every support. -/
theorem balancedOrientationLaw_expect_pair (hN : 2 ≤ Fintype.card I) {x : I → ℝ}
    (hx : x ∈ cube I) {a b : I} (hab : a ≠ b) :
    (balancedOrientationLaw x).expect (fun v => monomial {a, b} (vertexPoint v)) =
      (1 - pairOppositeProb (Fintype.card I)) * min (x a) (x b) +
        pairOppositeProb (Fintype.card I) * max 0 (x a + x b - 1) := by
  have hpt : ∀ H : Finset I,
      (∫ t in (0 : ℝ)..1, monomial ({a, b} : Finset I) (orientedProb H x t)) =
        min (x a) (x b) + (max 0 (x a + x b - 1) - min (x a) (x b)) *
          (if OppositeOrientation H a b then 1 else 0) := by
    intro H
    have hprod : ∀ t : ℝ, monomial ({a, b} : Finset I) (orientedProb H x t) =
        orientedProb H x t a * orientedProb H x t b := by
      intro t
      rw [monomial, Finset.prod_pair hab]
    simp_rw [hprod]
    rw [intervalIntegral_orientedProb_pair H hx a b]
    split_ifs <;> ring
  rw [balancedOrientationLaw_expect_monomial]
  simp only [hpt]
  rw [Law.expect_add, Law.expect_const, Law.expect_const_mul,
    balancedSubsets_pair_opposite hN hab]
  ring

/-! ## The balanced orientation moments -/

/-- `O^bal_j`: the `j`-th binomial moment of the success count on the support
`S` under the **ambient** balanced orientation law.  The law is the one of the
whole index type `I`, so a smaller `S` is a restriction of the same law, never a
law resampled in dimension `#S`. -/
def balancedOrientMoment (S : Finset I) (x : I → ℝ) (j : ℤ) : ℝ :=
  binomMoment S (balancedOrientationLaw x) j

/-- The balanced moments are averages over the ambient low set of the
conditional orientation moments; the low set is drawn once, ambiently. -/
theorem balancedOrientMoment_eq_expect (S : Finset I) (x : I → ℝ) (j : ℤ) :
    balancedOrientMoment S x j =
      (balancedSubsets I).expect (fun H => binomMoment S (orientedLaw H x) j) :=
  balancedOrientationLaw_expect x _

/-- PB12 for the balanced family: order zero is one. -/
@[simp] theorem balancedOrientMoment_zero (S : Finset I) (x : I → ℝ) :
    balancedOrientMoment S x 0 = 1 :=
  binomMoment_zero S _

/-- PB12 for the balanced family: negative orders vanish. -/
theorem balancedOrientMoment_of_neg (S : Finset I) (x : I → ℝ) {j : ℤ} (hj : j < 0) :
    balancedOrientMoment S x j = 0 :=
  binomMoment_of_neg S _ hj

/-- PB12 for the balanced family: orders above the support cardinality vanish. -/
theorem balancedOrientMoment_of_card_lt (S : Finset I) (x : I → ℝ) {j : ℤ}
    (hj : (S.card : ℤ) < j) : balancedOrientMoment S x j = 0 :=
  binomMoment_of_card_lt S _ hj

/-- PB28 at the moment level: the balanced law has the prescribed means, so the
first balanced moment is the sum of the means on the support. -/
theorem balancedOrientMoment_one (S : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    balancedOrientMoment S x 1 = ∑ i ∈ S, x i :=
  binomMoment_one S x _ (balancedOrientationLaw_hasMeans hx)

/-- The balanced moments are nonnegative. -/
theorem balancedOrientMoment_nonneg (S : Finset I) (x : I → ℝ) (j : ℤ) :
    0 ≤ balancedOrientMoment S x j := by
  refine Finset.sum_nonneg fun v _ => mul_nonneg ((balancedOrientationLaw x).nonneg v) ?_
  simp only [chooseInt]
  split_ifs
  · exact Nat.cast_nonneg _
  · exact le_rfl

/-- **PB29.**  `O^bal_2 = (1 - p_N) C_2 + p_N L_2`, with the **ambient** `p_N`
for every support `S`.  At the fair value `p_N = 1/2` this is PB08,
`2 O_2 = C_2 + L_2`. -/
theorem balancedOrientMoment_two (hN : 2 ≤ Fintype.card I) (S : Finset I) {x : I → ℝ}
    (hx : x ∈ cube I) :
    balancedOrientMoment S x 2 =
      (1 - pairOppositeProb (Fintype.card I)) * thresholdMoment S x 2 +
        pairOppositeProb (Fintype.card I) * frechetPairLower S x := by
  rw [balancedOrientMoment, thresholdMoment, show (2 : ℤ) = ((2 : ℕ) : ℤ) from rfl,
    binomMoment_eq_sum_monomial, thresholdLaw_binomMoment S x hx, frechetPairLower,
    Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun A hA => ?_
  obtain ⟨-, hcard⟩ := Finset.mem_powersetCard.mp hA
  obtain ⟨a, b, hab, rfl⟩ := Finset.card_eq_two.mp hcard
  rw [Finset.sum_pair hab, balancedOrientationLaw_expect_pair hN hx hab, monomialUpper_pair]

/-- **PB29, the form the coefficient uses.**  Since `β_N p_N = 1`, the balanced
pair defect is exactly the fair one: `β_N (C_2 - O^bal_2) = C_2 - L_2`. -/
theorem orientationBeta_mul_thresholdMoment_sub_balancedOrientMoment_two
    (hN : 2 ≤ Fintype.card I) (S : Finset I) {x : I → ℝ} (hx : x ∈ cube I) :
    orientationBeta (Fintype.card I) *
        (thresholdMoment S x 2 - balancedOrientMoment S x 2) =
      thresholdMoment S x 2 - frechetPairLower S x := by
  have hbp := orientationBeta_mul_pairOppositeProb hN
  rw [balancedOrientMoment_two hN S hx]
  linear_combination (thresholdMoment S x 2 - frechetPairLower S x) * hbp

/-! ## The boundary recursions for the balanced family -/

/-- **PB30, boundary recursion, mean zero.**  A coordinate of mean zero fails
under the ambient law, so deleting it from the support leaves every balanced
moment unchanged.  The law is not touched: this is a statement about the same
ambient law counted on a smaller support. -/
theorem balancedOrientMoment_insert_of_mean_zero {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {S : Finset I} (h0 : x a = 0) (j : ℤ) :
    balancedOrientMoment (insert a S) x j = balancedOrientMoment S x j :=
  binomMoment_insert_of_mean_zero (balancedOrientationLaw_hasMeans hx) h0 j

/-- **PB30, boundary recursion, mean one.**  A coordinate of mean one succeeds
under the ambient law, so Pascal's identity splits the balanced moment across
two consecutive orders.  Deleting it does **not** condition on its orientation
coin — the ambient law, and with it every correlation among the remaining
coins, is unchanged; only the counted support shrinks. -/
theorem balancedOrientMoment_insert_of_mean_one {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {S : Finset I} (ha : a ∉ S) (h1 : x a = 1) (j : ℤ) :
    balancedOrientMoment (insert a S) x j =
      balancedOrientMoment S x j + balancedOrientMoment S x (j - 1) :=
  binomMoment_insert_of_mean_one (balancedOrientationLaw_hasMeans hx) ha h1 j

/-! ## The restricted coefficient -/

/-- **PB30, the coefficient.**  `F_{S,j} = β_N C_j + V_j - P_j - β_N O^bal_j +
C_{j-1} - P_{j-1}` on the support `S` inside the ambient dimension
`N = Fintype.card I`.  Both the coefficient `β_N` and the orientation moments
are ambient; only `S` varies. -/
def balancedCoeffF (S : Finset I) (x : I → ℝ) (j : ℤ) : ℝ :=
  orientationBeta (Fintype.card I) * thresholdMoment S x j + lowerMomentInt S x j -
    elementaryInt S x j - orientationBeta (Fintype.card I) * balancedOrientMoment S x j +
    thresholdMoment S x (j - 1) - elementaryInt S x (j - 1)

/-- Negative orders contribute nothing. -/
theorem balancedCoeffF_of_neg (S : Finset I) (x : I → ℝ) {j : ℤ} (hj : j < 0) :
    balancedCoeffF S x j = 0 := by
  have hj1 : j - 1 < 0 := by omega
  rw [balancedCoeffF, thresholdMoment_of_neg S x hj, lowerMomentInt_of_neg S x hj,
    elementaryInt_of_neg S x hj, balancedOrientMoment_of_neg S x hj,
    thresholdMoment_of_neg S x hj1, elementaryInt_of_neg S x hj1]
  ring

/-- **PB30, order conventions**: `F_{S,0} = 0`. -/
theorem balancedCoeffF_zero (S : Finset I) (x : I → ℝ) : balancedCoeffF S x 0 = 0 := by
  rw [balancedCoeffF, thresholdMoment_zero, lowerMomentInt_zero, elementaryInt_zero,
    balancedOrientMoment_zero, thresholdMoment_of_neg S x (by norm_num),
    elementaryInt_of_neg S x (by norm_num : (0 : ℤ) - 1 < 0)]
  ring

/-- **PB30, order conventions**: `F_{S,1} = 0`, because all four families have
first moment the sum of the means on the support. -/
theorem balancedCoeffF_one (S : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    balancedCoeffF S x 1 = 0 := by
  have h0 : (1 : ℤ) - 1 = 0 := by norm_num
  have hP : elementaryInt S x 1 = ∑ i ∈ S, x i := by
    rw [elementaryInt_eq_binomMoment S x hx]
    exact binomMoment_one S x _ (bernoulliLaw_hasMeans x hx)
  rw [balancedCoeffF, thresholdMoment_one S x hx, lowerMomentInt_one S x,
    balancedOrientMoment_one S x hx, hP, h0, thresholdMoment_zero, elementaryInt_zero]
  ring

/-- **PB30, the top order**: at order `n + 1` the coefficient collapses to
`C_n - P_n`. -/
theorem balancedCoeffF_card_add_one (S : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    balancedCoeffF S x ((S.card : ℤ) + 1) =
      thresholdMoment S x (S.card : ℤ) - elementaryInt S x (S.card : ℤ) := by
  have hlt : (S.card : ℤ) < (S.card : ℤ) + 1 := by omega
  have hsub : (S.card : ℤ) + 1 - 1 = (S.card : ℤ) := by ring
  rw [balancedCoeffF, thresholdMoment_of_card_lt S x hlt, lowerMomentInt_of_card_lt S x hx hlt,
    elementaryInt_of_card_lt S x hlt, balancedOrientMoment_of_card_lt S x hlt, hsub]
  ring

/-- **PB30, the top order**: it is nonnegative, by maximality of
common-threshold rounding against the feasible Bernoulli law. -/
theorem balancedCoeffF_card_add_one_nonneg (S : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    0 ≤ balancedCoeffF S x ((S.card : ℤ) + 1) := by
  rw [balancedCoeffF_card_add_one S x hx, sub_nonneg]
  exact elementaryInt_le_thresholdMoment S x hx _

/-- **PB30, the top order**: orders above `n + 1` vanish. -/
theorem balancedCoeffF_of_card_add_one_lt (S : Finset I) (x : I → ℝ) (hx : x ∈ cube I) {j : ℤ}
    (hj : (S.card : ℤ) + 1 < j) : balancedCoeffF S x j = 0 := by
  have h1 : (S.card : ℤ) < j := by omega
  have h2 : (S.card : ℤ) < j - 1 := by omega
  rw [balancedCoeffF, thresholdMoment_of_card_lt S x h1, lowerMomentInt_of_card_lt S x hx h1,
    elementaryInt_of_card_lt S x h1, balancedOrientMoment_of_card_lt S x h1,
    thresholdMoment_of_card_lt S x h2, elementaryInt_of_card_lt S x h2]
  ring

/-- **PB29 as the base case of PB30**: `F_{S,2} = (C_2 - P_2) + (V_2 - L_2)`,
exactly the fair base case `coeffF_two`, because `β_N p_N = 1`. -/
theorem balancedCoeffF_two (hN : 2 ≤ Fintype.card I) (S : Finset I) {x : I → ℝ}
    (hx : x ∈ cube I) :
    balancedCoeffF S x 2 =
      (thresholdMoment S x 2 - elementaryInt S x 2) +
        (lowerMomentInt S x 2 - frechetPairLower S x) := by
  have h1 : (2 : ℤ) - 1 = 1 := by norm_num
  have hP : elementaryInt S x 1 = ∑ i ∈ S, x i := by
    rw [elementaryInt_eq_binomMoment S x hx]
    exact binomMoment_one S x _ (bernoulliLaw_hasMeans x hx)
  have hO := orientationBeta_mul_thresholdMoment_sub_balancedOrientMoment_two hN S hx
  rw [balancedCoeffF, h1, thresholdMoment_one S x hx, hP]
  linarith [hO]

/-- **PB29 as the base case of PB30**: the order-two coefficient is
nonnegative, by the pairwise upper and lower Fréchet bounds. -/
theorem balancedCoeffF_two_nonneg (hN : 2 ≤ Fintype.card I) (S : Finset I) {x : I → ℝ}
    (hx : x ∈ cube I) : 0 ≤ balancedCoeffF S x 2 := by
  rw [balancedCoeffF_two hN S hx]
  have h1 : 0 ≤ thresholdMoment S x 2 - elementaryInt S x 2 :=
    sub_nonneg.mpr (elementaryInt_le_thresholdMoment S x hx 2)
  have h2 : 0 ≤ lowerMomentInt S x 2 - frechetPairLower S x :=
    sub_nonneg.mpr (frechetPairLower_le_lowerMomentInt S x hx)
  linarith

/-- **PB30, boundary recursion**: a coordinate of mean zero is deterministic
and may be deleted from the support, under the same ambient law. -/
theorem balancedCoeffF_insert_of_mean_zero {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {S : Finset I} (ha : a ∉ S) (h0 : x a = 0) (j : ℤ) :
    balancedCoeffF (insert a S) x j = balancedCoeffF S x j := by
  rw [balancedCoeffF, balancedCoeffF, thresholdMoment_insert_of_mean_zero hx h0,
    thresholdMoment_insert_of_mean_zero hx h0,
    lowerMomentInt_insert_of_mean_zero ha h0,
    elementaryInt_insert_of_mean_zero ha h0,
    elementaryInt_insert_of_mean_zero ha h0,
    balancedOrientMoment_insert_of_mean_zero hx h0]

/-- **PB30, boundary recursion**: a coordinate of mean one is deterministic,
and deleting it splits the coefficient across two consecutive orders.  The
orientation coin of the deleted coordinate is never conditioned on. -/
theorem balancedCoeffF_insert_of_mean_one {x : I → ℝ} (hx : x ∈ cube I) {a : I}
    {S : Finset I} (ha : a ∉ S) (h1 : x a = 1) (j : ℤ) :
    balancedCoeffF (insert a S) x j = balancedCoeffF S x j + balancedCoeffF S x (j - 1) := by
  rw [balancedCoeffF, balancedCoeffF, balancedCoeffF,
    thresholdMoment_insert_of_mean_one hx ha h1,
    thresholdMoment_insert_of_mean_one hx ha h1,
    lowerMomentInt_insert_of_mean_one hx ha h1,
    elementaryInt_insert_of_mean_one ha h1,
    elementaryInt_insert_of_mean_one ha h1,
    balancedOrientMoment_insert_of_mean_one hx ha h1]
  ring

/-! ## The orientation coupling for the spreading step

These are the only ingredients of the PB30 spreading step that are genuinely
balanced: the source's coupling on the shared low set `H` and the shared
uniform variable.  Every other comparison in the step concerns `C`, `V` and `P`
and is already available from `CoefficientInequality`. -/

omit [Fintype I] in
/-- Each conditional orientation success probability is nondecreasing in the
means, at every low set and every value of the shared uniform variable: a low
coordinate widens `[0, u i]`, a high coordinate widens `(1 - u i, 1]`. -/
theorem orientedProb_mono (H : Finset I) {x y : I → ℝ} (hxy : ∀ i, x i ≤ y i) (t : ℝ) (i : I) :
    orientedProb H x t i ≤ orientedProb H y t i := by
  rw [orientedProb_eq_lowerStep, orientedProb_eq_lowerStep]
  by_cases hi : i ∈ H
  · simp only [if_pos hi, lowerStep]
    split_ifs <;> linarith [hxy i]
  · simp only [if_neg hi, lowerStep]
    split_ifs <;> linarith [hxy i]

omit [Fintype I] in
/-- Conditional orientation coins are integrable in the shared uniform
variable. -/
theorem orientedProb_intervalIntegrable (H : Finset I) (x : I → ℝ) (i : I) :
    IntervalIntegrable (fun t => orientedProb H x t i) volume 0 1 :=
  intervalIntegrable_of_mem_unitInterval _ (orientedProb_measurable H x i)
    fun t => Set.mem_Icc.mpr (orientedProb_cube H x t i)

/-- The conditional moments given the ambient low set, in integrated product
form. -/
theorem binomMoment_orientedLaw_eq_sum (S H : Finset I) (x : I → ℝ) (j : ℕ) :
    binomMoment S (orientedLaw H x) (j : ℤ) =
      ∑ A ∈ S.powersetCard j, ∫ t in (0 : ℝ)..1, monomial A (orientedProb H x t) := by
  rw [binomMoment_eq_sum_monomial]
  exact Finset.sum_congr rfl fun A _ => orientedLaw_expect_monomial H x A

/-- Conditionally on the ambient low set, the orientation moments are
coordinatewise nondecreasing. -/
theorem binomMoment_orientedLaw_mono (S H : Finset I) {x y : I → ℝ} (hxy : ∀ i, x i ≤ y i)
    (j : ℤ) :
    binomMoment S (orientedLaw H x) j ≤ binomMoment S (orientedLaw H y) j := by
  rcases lt_or_ge j 0 with hj | hj
  · rw [binomMoment_of_neg _ _ hj, binomMoment_of_neg _ _ hj]
  · obtain ⟨k, rfl⟩ := Int.eq_ofNat_of_zero_le hj
    rw [binomMoment_orientedLaw_eq_sum, binomMoment_orientedLaw_eq_sum]
    refine Finset.sum_le_sum fun A _ => ?_
    refine intervalIntegral.integral_mono (by norm_num)
      (orientedProb_monomial_integrable H x A) (orientedProb_monomial_integrable H y A)
      fun t => ?_
    simp only [monomial]
    exact Finset.prod_le_prod (fun i _ => (orientedProb_cube H x t i).1)
      fun i _ => orientedProb_mono H hxy t i

/-- **The balanced coupling, monotonicity.**  Every balanced orientation moment
is coordinatewise nondecreasing in the means.  The comparison is made under one
and the same ambient low set and uniform variable, then averaged; no
independence of the orientation coins is used. -/
theorem balancedOrientMoment_mono (S : Finset I) {x y : I → ℝ} (hxy : ∀ i, x i ≤ y i) (j : ℤ) :
    balancedOrientMoment S x j ≤ balancedOrientMoment S y j := by
  rw [balancedOrientMoment_eq_expect, balancedOrientMoment_eq_expect]
  exact (balancedSubsets I).expect_mono fun H => binomMoment_orientedLaw_mono S H hxy j

/-- Conditionally on the ambient low set, raising a single mean raises the
orientation moment of order `j + 1` by at most `(r - u i₀) binom(n - 1, j)`:
the flipped coordinate turns from failure to success on an event of total
probability exactly `r - u i₀`, and on that event each of the `binom(n - 1, j)`
subsets containing `i₀` contributes a conditional factor in `[0, 1]`.  No
derivative is taken. -/
theorem binomMoment_orientedLaw_update_sub_le (S H : Finset I) {x : I → ℝ} (i₀ : I) {r : ℝ}
    (hx : x ∈ cube I) (hr0 : 0 ≤ r) (hr1 : r ≤ 1) (hle : x i₀ ≤ r) (j : ℕ) :
    binomMoment S (orientedLaw H (Function.update x i₀ r)) ((j + 1 : ℕ) : ℤ) -
        binomMoment S (orientedLaw H x) ((j + 1 : ℕ) : ℤ) ≤
      (r - x i₀) * (((S.card - 1).choose j : ℕ) : ℝ) := by
  set y := Function.update x i₀ r with hy
  have hy0 : y i₀ = r := Function.update_self i₀ r x
  have hyx : ∀ i, i ≠ i₀ → y i = x i := fun i hi => Function.update_of_ne hi r x
  have hycube : y ∈ cube I := update_mem_cube hx i₀ hr0 hr1
  have hxy : ∀ i, x i ≤ y i := by
    intro i
    by_cases hi : i = i₀
    · subst hi; rw [hy0]; exact hle
    · rw [hyx i hi]
  have hdiff0 : 0 ≤ r - x i₀ := sub_nonneg.mpr hle
  have hprobeq : ∀ (t : ℝ) (i : I), i ≠ i₀ → orientedProb H y t i = orientedProb H x t i := by
    intro t i hi
    simp only [orientedProb, hyx i hi]
  rw [binomMoment_orientedLaw_eq_sum, binomMoment_orientedLaw_eq_sum, ← Finset.sum_sub_distrib]
  by_cases hmem : i₀ ∈ S
  · have hzero : ∀ A ∈ (S.erase i₀).powersetCard (j + 1),
        ((∫ t in (0 : ℝ)..1, monomial A (orientedProb H y t)) -
          ∫ t in (0 : ℝ)..1, monomial A (orientedProb H x t)) = 0 := by
      intro A hA
      have hA0 : i₀ ∉ A := fun hmem' =>
        Finset.notMem_erase i₀ S ((Finset.mem_powersetCard.mp hA).1 hmem')
      rw [sub_eq_zero]
      refine intervalIntegral.integral_congr fun t _ => ?_
      exact Finset.prod_congr rfl fun i hi => hprobeq t i fun h => hA0 (h ▸ hi)
    have hterm : ∀ B ∈ (S.erase i₀).powersetCard j,
        ((∫ t in (0 : ℝ)..1, monomial (insert i₀ B) (orientedProb H y t)) -
          ∫ t in (0 : ℝ)..1, monomial (insert i₀ B) (orientedProb H x t)) ≤ r - x i₀ := by
      intro B hB
      have hB0 : i₀ ∉ B := fun hmem' =>
        Finset.notMem_erase i₀ S ((Finset.mem_powersetCard.mp hB).1 hmem')
      have hbound : ∀ t : ℝ, monomial (insert i₀ B) (orientedProb H y t) -
          monomial (insert i₀ B) (orientedProb H x t) ≤
          orientedProb H y t i₀ - orientedProb H x t i₀ := by
        intro t
        have hBeq : (∏ i ∈ B, orientedProb H y t i) = ∏ i ∈ B, orientedProb H x t i :=
          Finset.prod_congr rfl fun i hi => hprobeq t i fun h => hB0 (h ▸ hi)
        have hP := orientedProb_monomial_mem_Icc H x B t
        simp only [monomial] at hP ⊢
        rw [Finset.prod_insert hB0, Finset.prod_insert hB0, hBeq]
        have hd : 0 ≤ orientedProb H y t i₀ - orientedProb H x t i₀ :=
          sub_nonneg.mpr (orientedProb_mono H hxy t i₀)
        have h1 : (orientedProb H y t i₀ - orientedProb H x t i₀) *
            (∏ i ∈ B, orientedProb H x t i) ≤
            (orientedProb H y t i₀ - orientedProb H x t i₀) * 1 :=
          mul_le_mul_of_nonneg_left hP.2 hd
        nlinarith [h1]
      have hint : IntervalIntegrable
          (fun t => orientedProb H y t i₀ - orientedProb H x t i₀) volume 0 1 :=
        (orientedProb_intervalIntegrable H y i₀).sub (orientedProb_intervalIntegrable H x i₀)
      rw [← intervalIntegral.integral_sub (orientedProb_monomial_integrable H y _)
        (orientedProb_monomial_integrable H x _)]
      refine le_trans (intervalIntegral.integral_mono (by norm_num)
        ((orientedProb_monomial_integrable H y _).sub
          (orientedProb_monomial_integrable H x _)) hint hbound) ?_
      rw [intervalIntegral.integral_sub (orientedProb_intervalIntegrable H y i₀)
        (orientedProb_intervalIntegrable H x i₀),
        intervalIntegral_orientedProb H hycube i₀, intervalIntegral_orientedProb H hx i₀, hy0]
    rw [sum_powersetCard_succ_split hmem j
      fun A => (∫ t in (0 : ℝ)..1, monomial A (orientedProb H y t)) -
        ∫ t in (0 : ℝ)..1, monomial A (orientedProb H x t),
      Finset.sum_congr rfl hzero, Finset.sum_const, smul_zero, zero_add]
    refine le_trans (Finset.sum_le_card_nsmul _ _ _ hterm) ?_
    rw [Finset.card_powersetCard, Finset.card_erase_of_mem hmem, nsmul_eq_mul, mul_comm]
  · have hzero : ∀ A ∈ S.powersetCard (j + 1),
        ((∫ t in (0 : ℝ)..1, monomial A (orientedProb H y t)) -
          ∫ t in (0 : ℝ)..1, monomial A (orientedProb H x t)) = 0 := by
      intro A hA
      have hA0 : i₀ ∉ A := fun hmem' => hmem ((Finset.mem_powersetCard.mp hA).1 hmem')
      rw [sub_eq_zero]
      refine intervalIntegral.integral_congr fun t _ => ?_
      exact Finset.prod_congr rfl fun i hi => hprobeq t i fun h => hA0 (h ▸ hi)
    rw [Finset.sum_congr rfl hzero, Finset.sum_const, smul_zero]
    exact mul_nonneg hdiff0 (Nat.cast_nonneg _)

/-- **The balanced coupling, the Lipschitz bound.**  Raising a single mean from
`u i₀` to `r` raises the balanced orientation moment of order `j + 1` by at most
`(r - u i₀) binom(n - 1, j)`.  This is the source's comparison "the orientation
comparison also survives the dependence of the coins": the two laws share the
ambient low set `H` and the uniform variable, the bound holds conditionally on
`H`, and averaging preserves it. -/
theorem balancedOrientMoment_update_sub_le (S : Finset I) {x : I → ℝ} (i₀ : I) {r : ℝ}
    (hx : x ∈ cube I) (hr0 : 0 ≤ r) (hr1 : r ≤ 1) (hle : x i₀ ≤ r) (j : ℕ) :
    balancedOrientMoment S (Function.update x i₀ r) ((j + 1 : ℕ) : ℤ) -
        balancedOrientMoment S x ((j + 1 : ℕ) : ℤ) ≤
      (r - x i₀) * (((S.card - 1).choose j : ℕ) : ℝ) := by
  rw [balancedOrientMoment_eq_expect, balancedOrientMoment_eq_expect, ← Law.expect_sub]
  refine le_trans ((balancedSubsets I).expect_mono fun H =>
    binomMoment_orientedLaw_update_sub_le S H i₀ hx hr0 hr1 hle j) ?_
  rw [Law.expect_const]

/-- **PB30, the non-inductive orders**: at most two, or above the support
cardinality.  Everything outside `3 ≤ j ≤ n` is settled here; the remaining
range is the spreading regime. -/
theorem balancedCoeffF_nonneg_base (hN : 2 ≤ Fintype.card I) (S : Finset I) {x : I → ℝ}
    (hx : x ∈ cube I) (j : ℤ) (h : j ≤ 2 ∨ (S.card : ℤ) < j) :
    0 ≤ balancedCoeffF S x j := by
  rcases h with hj | hj
  · rcases lt_or_ge j 0 with hneg | hpos
    · rw [balancedCoeffF_of_neg S x hneg]
    · interval_cases j
      · rw [balancedCoeffF_zero]
      · rw [balancedCoeffF_one S x hx]
      · exact balancedCoeffF_two_nonneg hN S hx
  · rcases lt_trichotomy ((S.card : ℤ) + 1) j with hgt | heq | hlt
    · rw [balancedCoeffF_of_card_add_one_lt S x hx hgt]
    · rw [← heq]
      exact balancedCoeffF_card_add_one_nonneg S x hx
    · omega

end

end MultilinearGap
