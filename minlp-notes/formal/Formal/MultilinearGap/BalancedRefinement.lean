import Formal.MultilinearGap.BalancedMoments
import Formal.MultilinearGap.BilinearGraph
import Formal.MultilinearGap.CommonAspectBound

/-!
# The finite-dimensional refinement `rho + beta_N`

This module discharges the two remaining Tier F obligations PB30 and PB31 of
`formal/topics/18-positive-box/CLAIMS.md`, following the closure note
`notes/review-positive-box-balanced-orientation-closure.md`.

## PB30

`balancedCoeffF_nonneg` is `F_{S,j} >= 0` for **every** support `S`, every point
of the cube and every integer order, where

`F_{S,j} = β_N C_j + V_j - P_j - β_N O^bal_j + C_{j-1} - P_{j-1}`

is the `balancedCoeffF` of `Formal.MultilinearGap.BalancedMoments`, with the
ambient constant `β_N = orientationBeta (Fintype.card I)`.

**The definitions retain the ambient law.**  `balancedOrientMoment S x j` is
`binomMoment S (balancedOrientationLaw x) j`: the law argument is the ambient
balanced orientation law of the whole index type `I`, and `S` only selects which
coordinates are counted.  A statement about a smaller support is therefore a
statement about a restriction of the one ambient law. These definitions retain
the ambient law and ambient constant as `S` shrinks; substituting the support-size
constant is invalid in general. This does not prevent writing that constant or
constructing a different law on the ambient type. The proofs preserve the chosen definitions:
`balancedCoeffF_spread_le` compares two points `x` and `spreadPoint x a b h` of the
*same* cube under the *same* ambient law, and the induction
`balancedCoeffF_nonneg_of_card_le` shrinks only `S`.

The new content is the spreading step `balancedCoeffF_spread_le` and the
induction.  The step is the fair argument of
`Formal.MultilinearGap.CoefficientInequality` with `2` replaced by `β_N`: the
exact changes

`ΔC_j = -B h`, `ΔC_{j-1} = -D h`, `ΔV_j = 0`,
`Δ(-P_j - P_{j-1}) <= D h`, `ΔO^bal_j >= -B h`

with `B = binom(n-1, j-1)` and `D = binom(n-1, j-2)` combine to

`ΔF <= -β B h - D h + D h + β B h = 0`,

a cancellation that holds for **any** `β >= 0`, so the fair value `2` plays no
role.  Only `orientationBeta_nonneg` is used.  The three non-orientation changes
are the fair ones verbatim (`thresholdMoment_peel_two`,
`lowerMomentInt_congr_of_meanSum`, `elementaryInt_spread_sub_le`); the
orientation change is the balanced coupling `balancedOrientMoment_mono` and
`balancedOrientMoment_update_sub_le` of `BalancedMoments`, whose Lipschitz
constant `binom(n-1, j-1)` is attained and therefore cannot be improved.

The hypothesis `hN : 2 <= Fintype.card I` is carried through the induction.  It
is needed only by the base case `balancedCoeffF_two_nonneg`, which rests on
PB29 and hence on `balancedSubsets_pair_opposite`; the spreading step and the
boundary recursions do not use it.

## PB31

`positiveBoxAspectBound_add_orientationBeta` is
`tbtgap f <= (rho + β_N) chgap f` on every `N`-dimensional strictly positive box
with coordinate aspect ratios at most `rho`, including the unequal-box transfer.
The route mirrors `Formal.MultilinearGap.CommonAspectBound` with `2` replaced by
`β_N` throughout:

* `physCombination_eq_sum_balancedCoeffF` (the PB19 analogue): the coefficient of
  `t ^ j` in `(β_N + t) C + V - (1 + t) P - β_N O^bal` is exactly `F_{S,j}`, over
  the full range `j = 0, …, n + 1`, so no top-degree term is lost;
* `physUpper_sub_physLower_le_balanced` (the PB20 analogue):
  `C - V <= rho (C - P) + β_N (C - O^bal)`;
* `balancedMixtureLaw` (the PB21 analogue): the single law mixing independent
  Bernoulli rounding with weight `rho / (rho + β_N)` and the **ambient** balanced
  orientation law with weight `β_N / (rho + β_N)`.  It is built from `rho`, the
  ambient dimension and the means alone, so it is fixed before any support is
  chosen (`exists_common_balanced_mixture_law`);
* `commonAspect_termwiseGap_le_balanced` (the PB22 analogue) on `[1, rho]^N`;
* `positiveBoxAspectBound_add_orientationBeta` (the PB25 analogue), by the same
  transfer as `originalBox_bound_of_commonAspect_bound`, restated at a fixed
  ambient dimension because `β_N` depends on it.  The expanded supports are
  arbitrary subsets of the same `N` coordinates and use restrictions of the same
  ambient orientation law, which is exactly what PB30 covers.

**Dimensions zero and one are covered explicitly, not assumed away.**  When
`Fintype.card I <= 1` every monomial has degree at most one, so every box gap
vanishes (`boxTermwiseGap_eq_zero_of_card_le_one`) and the bound is trivially
true; `β_N = 0` there by `orientationBeta_of_lt_two`, and the conclusion
`tbtgap <= rho * chgap` still holds because both sides are zero on the left and
nonnegative on the right.  The two branches are joined inside
`commonAspect_termwiseGap_le_balanced`, so the final statement carries no
dimension hypothesis.

Since `β_N < 2` for every `N >= 2` (`orientationBeta_lt_two`), the constant is a
strict improvement on the dimension-free `rho + 2` of
`positiveBoxAspectBound_add_two` in every fixed dimension, and it degrades to it
in the limit.
-/

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-! ## Expectation helpers

These three are re-proved here because the corresponding helpers of
`Formal.MultilinearGap.CommonAspectBound` are `private`. -/

private theorem expect_finsetSum' {κ : Type*} (μ : Law (Vertex I)) (u : Finset κ)
    (f : κ → Vertex I → ℝ) :
    μ.expect (fun v => ∑ k ∈ u, f k v) = ∑ k ∈ u, μ.expect (f k) := by
  simp only [Law.expect, Finset.mul_sum]
  exact Finset.sum_comm

private theorem expect_mix' (μ ν : Law (Vertex I)) (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hab : a + b = 1) (f : Vertex I → ℝ) :
    (Law.mix μ ν a b ha hb hab).expect f = a * μ.expect f + b * ν.expect f := by
  simp only [Law.expect, Law.mix, add_mul, Finset.sum_add_distrib, Finset.mul_sum,
    mul_assoc]

private theorem expect_sub_le_hullGap' (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
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

/-! ## The ambient constant is nonnegative

This is the only property of `β_N` that the spreading step needs. -/

/-- `β_N >= 0` for every ambient dimension, including the degenerate dimensions
`0` and `1` where it is zero. -/
theorem orientationBeta_nonneg (N : ℕ) : 0 ≤ orientationBeta N := by
  rcases lt_or_ge N 2 with h | h
  · rw [orientationBeta_of_lt_two h]
  · linarith [one_le_orientationBeta h]

/-! ## PB30: the spreading step -/

/-- **PB30, the spreading step.**  Moving a global minimum down by `h` and a
global maximum up by `h` does not increase the restricted coefficient, for every
order at least three.  Both points lie in the same cube and are compared under
the same ambient balanced law; the support `S` is not changed.

The three non-orientation comparisons are the fair ones verbatim.  The
orientation comparison is `balancedOrientMoment_mono` followed by
`balancedOrientMoment_update_sub_le`, both proved in `BalancedMoments` by
coupling on the shared ambient low set and the shared uniform variable.  The
final cancellation `-β B h - D h + D h + β B h = 0` uses only `0 ≤ β`, so no
ambient-dimension hypothesis is needed here. -/
theorem balancedCoeffF_spread_le {S : Finset I} {a b : I} (ha : a ∈ S) (hb : b ∈ S)
    (hab : a ≠ b) {x : I → ℝ} (hx : x ∈ cube I) (hmin : ∀ i ∈ S, x a ≤ x i)
    (hmax : ∀ i ∈ S, x i ≤ x b) {h : ℝ} (hh0 : 0 ≤ h) (hha : h ≤ x a) (hhb : h ≤ 1 - x b)
    {j : ℤ} (hj : 3 ≤ j) :
    balancedCoeffF S (spreadPoint x a b h) j ≤ balancedCoeffF S x j := by
  classical
  obtain ⟨m, rfl⟩ : ∃ m : ℕ, j = (m : ℤ) + 3 := ⟨(j - 3).toNat, by omega⟩
  set y := spreadPoint x a b h with hydef
  set t := (S.erase a).erase b with htdef
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
  have hymin : ∀ i ∈ S, y a ≤ y i := by
    intro i hi
    by_cases hib : i = b
    · subst hib; rw [hya, hyb]; linarith
    · by_cases hia : i = a
      · subst hia; exact le_rfl
      · rw [hyo i hia hib, hya]; linarith [hmin i hi]
  have hymax : ∀ i ∈ S, y i ≤ y b := by
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
  set B2 : ℝ := (((S.card - 1).choose (m + 2) : ℕ) : ℝ) with hB2
  set B1 : ℝ := (((S.card - 1).choose (m + 1) : ℕ) : ℝ) with hB1
  -- the exact change of the common-threshold moments
  have hCgen : ∀ r : ℕ,
      thresholdMoment S y ((r + 2 : ℕ) : ℤ) =
        thresholdMoment S x ((r + 2 : ℕ) : ℤ) - h * (((S.card - 1).choose (r + 1) : ℕ) : ℝ) := by
    intro r
    rw [thresholdMoment_peel_two ha hb hab hx hmin hmax r,
      thresholdMoment_peel_two ha hb hab hycube hymin hymax r, hya,
      thresholdMoment_congr hx hycube hxy ((r + 2 : ℕ) : ℤ),
      thresholdMoment_congr hx hycube hxy ((r + 1 : ℕ) : ℤ)]
    ring
  have hCj : thresholdMoment S y ((m + 3 : ℕ) : ℤ) =
      thresholdMoment S x ((m + 3 : ℕ) : ℤ) - h * B2 := hCgen (m + 1)
  have hCj1 : thresholdMoment S y ((m + 2 : ℕ) : ℤ) =
      thresholdMoment S x ((m + 2 : ℕ) : ℤ) - h * B1 := hCgen m
  -- the adjacent-count moment is constant along the path
  have hmean : meanSum S x = meanSum S y := by
    rw [meanSum, meanSum, sum_pair_erase ha hb hab x, sum_pair_erase ha hb hab y, hya, hyb]
    have hsum : ∑ i ∈ t, x i = ∑ i ∈ t, y i := Finset.sum_congr rfl fun i hi => hxy i hi
    rw [← htdef, hsum]
    ring
  have hV : lowerMomentInt S y ((m + 3 : ℕ) : ℤ) = lowerMomentInt S x ((m + 3 : ℕ) : ℤ) :=
    (lowerMomentInt_congr_of_meanSum hmean _).symm
  -- the independent moments, by the fair estimate
  have hP := elementaryInt_spread_sub_le ha hb hab hx hh0 hhb m
  rw [← hydef, ← hB1] at hP
  -- the balanced orientation moment cannot drop by more than `B2 * h`
  have hO : balancedOrientMoment S x ((m + 3 : ℕ) : ℤ) -
      balancedOrientMoment S y ((m + 3 : ℕ) : ℤ) ≤ h * B2 := by
    set z : I → ℝ := Function.update x a (x a - h) with hzdef
    have hza : z a = x a - h := Function.update_self _ _ _
    have hzo : ∀ i, i ≠ a → z i = x i := fun i hia => Function.update_of_ne hia _ _
    have hzcube : z ∈ cube I :=
      update_mem_cube hx a (by linarith) (by linarith [(hx a).2])
    have hback : Function.update z a (x a) = x := by
      rw [hzdef, Function.update_idem, Function.update_eq_self]
    have hstep1 : balancedOrientMoment S x ((m + 3 : ℕ) : ℤ) -
        balancedOrientMoment S z ((m + 3 : ℕ) : ℤ) ≤
        (x a - z a) * (((S.card - 1).choose (m + 2) : ℕ) : ℝ) := by
      have hup := balancedOrientMoment_update_sub_le S (x := z) a hzcube (hx a).1 (hx a).2
        (by rw [hza]; linarith) (m + 2)
      rwa [hback] at hup
    have hstep2 : balancedOrientMoment S z ((m + 3 : ℕ) : ℤ) ≤
        balancedOrientMoment S y ((m + 3 : ℕ) : ℤ) := by
      refine balancedOrientMoment_mono S (fun i => ?_) _
      by_cases hib : i = b
      · subst hib
        rw [hyb, hzo i hab.symm]
        linarith
      · by_cases hia : i = a
        · subst hia; rw [hya, hza]
        · rw [hyo i hia hib, hzo i hia]
    rw [hza] at hstep1
    have hcancel : x a - (x a - h) = h := by ring
    rw [hcancel] at hstep1
    linarith
  -- assembling: `-β B h - D h + D h + β B h = 0`, valid for every `β ≥ 0`
  rw [balancedCoeffF, balancedCoeffF, e3, e2, hCj, hCj1, hV]
  linarith [hP, mul_le_mul_of_nonneg_left hO (orientationBeta_nonneg (Fintype.card I))]

/-! ## PB30: nonnegativity -/

/-- **PB30**, the induction on the support cardinality.  The ambient hypothesis
`hN` is fixed once, outside the induction; only the support shrinks, and always
under the same ambient balanced law. -/
theorem balancedCoeffF_nonneg_of_card_le (hN : 2 ≤ Fintype.card I) :
    ∀ (n : ℕ) (S : Finset I) (x : I → ℝ), S.card ≤ n → x ∈ cube I →
      ∀ j : ℤ, 0 ≤ balancedCoeffF S x j := by
  intro n
  induction n with
  | zero =>
    intro S x hcard hx j
    have hs : S.card = 0 := Nat.le_zero.mp hcard
    refine balancedCoeffF_nonneg_base hN S hx j ?_
    rcases le_or_gt j 2 with h | h
    · exact Or.inl h
    · right; omega
  | succ n ih =>
    have hbd : ∀ (S : Finset I) (x : I → ℝ), S.card ≤ n + 1 → x ∈ cube I →
        (∃ a ∈ S, x a = 0 ∨ x a = 1) → ∀ j : ℤ, 0 ≤ balancedCoeffF S x j := by
      rintro S x hcard hx ⟨a, ha, hval⟩ j
      have hins : insert a (S.erase a) = S := Finset.insert_erase ha
      have hane : a ∉ S.erase a := Finset.notMem_erase a S
      have hpos : 1 ≤ S.card := Finset.card_pos.mpr ⟨a, ha⟩
      have hcard' : (S.erase a).card ≤ n := by
        rw [Finset.card_erase_of_mem ha]; omega
      rcases hval with h0 | h1
      · rw [← hins, balancedCoeffF_insert_of_mean_zero hx hane h0]
        exact ih _ _ hcard' hx j
      · rw [← hins, balancedCoeffF_insert_of_mean_one hx hane h1]
        exact add_nonneg (ih _ _ hcard' hx j) (ih _ _ hcard' hx (j - 1))
    intro S x hcard hx j
    rcases le_or_gt j 2 with hj2 | hj2
    · exact balancedCoeffF_nonneg_base hN S hx j (Or.inl hj2)
    rcases lt_or_ge (S.card : ℤ) j with hjn | hjn
    · exact balancedCoeffF_nonneg_base hN S hx j (Or.inr hjn)
    -- the spreading regime: `3 ≤ j ≤ n`
    have hcard2 : 2 ≤ S.card := by omega
    have hsne : S.Nonempty := Finset.card_pos.mp (by omega)
    obtain ⟨a, ha, hmin⟩ := monomial_min_anchor S hsne x
    have hene : (S.erase a).Nonempty := by
      rw [← Finset.card_pos, Finset.card_erase_of_mem ha]
      omega
    obtain ⟨b, hb', hmax'⟩ := exists_max_anchor (S.erase a) hene x
    have hb : b ∈ S := Finset.mem_of_mem_erase hb'
    have hab : a ≠ b := fun hh => (Finset.mem_erase.mp hb').1 hh.symm
    have hmax : ∀ i ∈ S, x i ≤ x b := by
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
    have hbdry : ∃ c ∈ S, y c = 0 ∨ y c = 1 := by
      rcases min_cases (x a) (1 - x b) with ⟨heq, -⟩ | ⟨heq, -⟩
      · refine ⟨a, ha, Or.inl ?_⟩
        rw [hydef, spreadPoint_left hab, hhdef, heq]
        ring
      · refine ⟨b, hb, Or.inr ?_⟩
        rw [hydef, spreadPoint_right, hhdef, heq]
        ring
    have hstep :=
      balancedCoeffF_spread_le ha hb hab hx hmin hmax hh0 hha hhb (show (3 : ℤ) ≤ j by omega)
    have hzero := hbd S y hcard hycube hbdry j
    rw [← hydef] at hstep
    linarith

/-- **PB30.**  `F_{S,j} = β_N C_j + V_j - P_j - β_N O^bal_j + C_{j-1} - P_{j-1}`
is nonnegative for **every** support `S`, every point of the cube and every
integer order, with the one ambient constant `β_N = orientationBeta N` and the
one ambient balanced orientation law throughout.  No law is indexed by `S`:
smaller supports are restrictions of the same law, never laws resampled in the
smaller dimension. -/
theorem balancedCoeffF_nonneg (hN : 2 ≤ Fintype.card I) (S : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) (j : ℤ) : 0 ≤ balancedCoeffF S x j :=
  balancedCoeffF_nonneg_of_card_le hN S.card S x le_rfl hx j

/-! ## PB31: the generating identity -/

/-- `O^bal(t)`, the ambient balanced orientation expectation of the physical
monomial.  The law is the ambient one; `S` only selects the factors. -/
def physBalancedOrient (t : ℝ) (S : Finset I) (x : I → ℝ) : ℝ :=
  (balancedOrientationLaw x).expect (fun v => physMonomial t S (vertexPoint v))

/-- `O^bal(t) = ∑_{j = 0}^{n + 1} O^bal_j t ^ j`, the balanced generating sum. -/
theorem sum_balancedOrientMoment (t : ℝ) (S : Finset I) (x : I → ℝ) :
    ∑ j ∈ Finset.range (S.card + 2), balancedOrientMoment S x (j : ℤ) * t ^ j =
      physBalancedOrient t S x := by
  rw [show S.card + 2 = S.card + 1 + 1 from rfl, Finset.sum_range_succ,
    balancedOrientMoment_of_card_lt S x (by push_cast; omega), zero_mul, add_zero,
    physBalancedOrient, expect_physMonomial_eq_sum_binomMoment]
  rfl

/-- Multiplying a moment generating sum by `t` reindexes it, provided the family
vanishes at order `-1` and at the top order `N` of the range.  Re-proved here
because the corresponding helper of `CommonAspectBound` is `private`. -/
private theorem sum_shift_mul' (N : ℕ) (M : ℤ → ℝ) (t : ℝ)
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

/-- **PB31, the PB19 analogue.**  The coefficient of `t ^ j` in
`(β_N + t) C + V - (1 + t) P - β_N O^bal` is exactly `F_{S,j}`.  The range
`j = 0, …, n + 1` is essential: the order `n + 1` coefficient is
`C_n - P_n = F_{S,n+1}`, generically nonzero, so truncating at `j = n` makes the
statement false. -/
theorem physCombination_eq_sum_balancedCoeffF (t : ℝ) (S : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) :
    (orientationBeta (Fintype.card I) + t) * physUpper t S x + physLower t S x -
        (1 + t) * physMonomial t S x -
        orientationBeta (Fintype.card I) * physBalancedOrient t S x =
      ∑ j ∈ Finset.range (S.card + 2), balancedCoeffF S x (j : ℤ) * t ^ j := by
  have hr : S.card + 1 + 1 = S.card + 2 := rfl
  have hCs := sum_shift_mul' (S.card + 1) (thresholdMoment S x) t
    (thresholdMoment_of_neg S x (by norm_num))
    (thresholdMoment_of_card_lt S x (by push_cast; omega))
  have hPs := sum_shift_mul' (S.card + 1) (elementaryInt S x) t
    (elementaryInt_of_neg S x (by norm_num))
    (elementaryInt_of_card_lt S x (by push_cast; omega))
  rw [hr] at hCs hPs
  have hsplit : ∑ j ∈ Finset.range (S.card + 2), balancedCoeffF S x (j : ℤ) * t ^ j =
      orientationBeta (Fintype.card I) *
            (∑ j ∈ Finset.range (S.card + 2), thresholdMoment S x (j : ℤ) * t ^ j) +
          (∑ j ∈ Finset.range (S.card + 2), lowerMomentInt S x (j : ℤ) * t ^ j) -
          (∑ j ∈ Finset.range (S.card + 2), elementaryInt S x (j : ℤ) * t ^ j) -
          orientationBeta (Fintype.card I) *
            (∑ j ∈ Finset.range (S.card + 2), balancedOrientMoment S x (j : ℤ) * t ^ j) +
          (∑ j ∈ Finset.range (S.card + 2), thresholdMoment S x ((j : ℤ) - 1) * t ^ j) -
          ∑ j ∈ Finset.range (S.card + 2), elementaryInt S x ((j : ℤ) - 1) * t ^ j := by
    simp only [Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun j _ => by rw [balancedCoeffF]; ring
  rw [hsplit, ← hCs, ← hPs, sum_thresholdMoment t S x hx, sum_lowerMomentInt t S x hx,
    sum_elementaryInt t S x hx, sum_balancedOrientMoment t S x]
  ring

/-- **PB31, the PB20 analogue.**  `C - V ≤ rho (C - P) + β_N (C - O^bal)` with
`rho = 1 + t`, for every support and every point of the cube.  This is the
generating identity together with PB30 and `0 ≤ t`. -/
theorem physUpper_sub_physLower_le_balanced (hN : 2 ≤ Fintype.card I) (t : ℝ) (ht : 0 ≤ t)
    (S : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    physUpper t S x - physLower t S x ≤
      (1 + t) * (physUpper t S x - physMonomial t S x) +
        orientationBeta (Fintype.card I) * (physUpper t S x - physBalancedOrient t S x) := by
  have h : (0 : ℝ) ≤ ∑ j ∈ Finset.range (S.card + 2), balancedCoeffF S x (j : ℤ) * t ^ j :=
    Finset.sum_nonneg fun j _ => mul_nonneg (balancedCoeffF_nonneg hN S x hx _) (pow_nonneg ht _)
  rw [← physCombination_eq_sum_balancedCoeffF t S x hx] at h
  linarith

/-! ## PB31: one support-independent mixture -/

/-- The mixture denominator is positive in every ambient dimension. -/
theorem zero_lt_add_orientationBeta {rho : ℝ} (hrho : 1 ≤ rho) (N : ℕ) :
    0 < rho + orientationBeta N := by
  linarith [orientationBeta_nonneg N]

/-- **PB31, the PB21 analogue.**  The rounding mixture of independent Bernoulli
rounding with weight `rho / (rho + β_N)` and the **ambient** balanced
orientation law with weight `β_N / (rho + β_N)`.  It is a single law on all
coordinates, built from `rho`, the ambient dimension and the coordinate means
alone: no support and no coefficient vector occurs in its definition, and the
orientation component is the ambient law, never a law resampled on a support. -/
def balancedMixtureLaw (rho : ℝ) (hrho : 1 ≤ rho) (x : I → ℝ) (hx : x ∈ cube I) :
    Law (Vertex I) :=
  Law.mix (bernoulliLaw x hx) (balancedOrientationLaw x)
    (rho / (rho + orientationBeta (Fintype.card I)))
    (orientationBeta (Fintype.card I) / (rho + orientationBeta (Fintype.card I)))
    (div_nonneg (by linarith) (zero_lt_add_orientationBeta hrho _).le)
    (div_nonneg (orientationBeta_nonneg _) (zero_lt_add_orientationBeta hrho _).le)
    (by
      have h2 : rho + orientationBeta (Fintype.card I) ≠ 0 :=
        ne_of_gt (zero_lt_add_orientationBeta hrho _)
      field_simp)

/-- The mixture is feasible: it has the prescribed coordinate means. -/
theorem balancedMixtureLaw_hasMeans (rho : ℝ) (hrho : 1 ≤ rho) (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (balancedMixtureLaw rho hrho x hx) x := by
  have h2 : rho + orientationBeta (Fintype.card I) ≠ 0 :=
    ne_of_gt (zero_lt_add_orientationBeta hrho _)
  intro i
  rw [balancedMixtureLaw, expect_mix', bernoulliLaw_hasMeans x hx i,
    balancedOrientationLaw_hasMeans hx i]
  field_simp

/-- The mixture's expectation of a physical monomial is the corresponding convex
combination of the independent and ambient balanced orientation values. -/
theorem balancedMixtureLaw_expect_physMonomial (rho : ℝ) (hrho : 1 ≤ rho) (x : I → ℝ)
    (hx : x ∈ cube I) (S : Finset I) :
    (balancedMixtureLaw rho hrho x hx).expect
        (fun v => physMonomial (rho - 1) S (vertexPoint v)) =
      rho / (rho + orientationBeta (Fintype.card I)) * physMonomial (rho - 1) S x +
        orientationBeta (Fintype.card I) / (rho + orientationBeta (Fintype.card I)) *
          physBalancedOrient (rho - 1) S x := by
  rw [balancedMixtureLaw, expect_mix', bernoulliLaw_physMonomial _ S x hx, physBalancedOrient]

/-- **PB31, the PB21 analogue.**  The one mixture captures at least
`1 / (rho + β_N)` of the exact gap of **every** physical monomial,
simultaneously.  The law is fixed before the support `S` is chosen. -/
theorem balancedMixtureLaw_capture (hN : 2 ≤ Fintype.card I) (rho : ℝ) (hrho : 1 ≤ rho)
    (x : I → ℝ) (hx : x ∈ cube I) (S : Finset I) :
    hullGap (physMonomial (rho - 1) S) x / (rho + orientationBeta (Fintype.card I)) ≤
      physUpper (rho - 1) S x -
        (balancedMixtureLaw rho hrho x hx).expect
          (fun v => physMonomial (rho - 1) S (vertexPoint v)) := by
  have h2 : (0 : ℝ) < rho + orientationBeta (Fintype.card I) :=
    zero_lt_add_orientationBeta hrho _
  have ht : (0 : ℝ) ≤ rho - 1 := by linarith
  have hpb20 := physUpper_sub_physLower_le_balanced hN (rho - 1) ht S x hx
  have hone : (1 : ℝ) + (rho - 1) = rho := by ring
  rw [hone] at hpb20
  rw [physMonomial_hullGap _ ht S x hx, balancedMixtureLaw_expect_physMonomial rho hrho x hx S,
    div_le_iff₀ h2]
  have hclear : (physUpper (rho - 1) S x -
      (rho / (rho + orientationBeta (Fintype.card I)) * physMonomial (rho - 1) S x +
        orientationBeta (Fintype.card I) / (rho + orientationBeta (Fintype.card I)) *
          physBalancedOrient (rho - 1) S x)) * (rho + orientationBeta (Fintype.card I)) =
      (rho + orientationBeta (Fintype.card I)) * physUpper (rho - 1) S x -
        rho * physMonomial (rho - 1) S x -
        orientationBeta (Fintype.card I) * physBalancedOrient (rho - 1) S x := by
    field_simp
    ring
  rw [hclear]
  linarith

/-- **PB31, the PB21 analogue**, with the law quantified outside the support:
one feasible law captures at least `1 / (rho + β_N)` of the gap of every
physical monomial. -/
theorem exists_common_balanced_mixture_law (hN : 2 ≤ Fintype.card I) (rho : ℝ)
    (hrho : 1 ≤ rho) (x : I → ℝ) (hx : x ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧ ∀ S : Finset I,
      hullGap (physMonomial (rho - 1) S) x / (rho + orientationBeta (Fintype.card I)) ≤
        physUpper (rho - 1) S x -
          μ.expect (fun v => physMonomial (rho - 1) S (vertexPoint v)) :=
  ⟨balancedMixtureLaw rho hrho x hx, balancedMixtureLaw_hasMeans rho hrho x hx,
    fun S => balancedMixtureLaw_capture hN rho hrho x hx S⟩

/-! ## Dimensions zero and one

These are not side conditions: they are the ambient dimensions in which
`β_N = 0`, and they are discharged here by showing that every gap vanishes. -/

omit [Fintype I] [DecidableEq I] in
/-- A monomial of degree at most one has zero gap on every coordinate box: its
box expansion is a polynomial of degree at most one, which is mean exact. -/
theorem boxHullGap_monomial_eq_zero_of_card_le_one [Finite I] (l u : I → ℝ)
    (hlu : ∀ i, l i ≤ u i) {s : Finset I} (hs : s.card ≤ 1) {x : I → ℝ}
    (hx : x ∈ coordinateBox l u) :
    boxHullGap l u (monomial s) x = 0 := by
  classical
  let _ := Fintype.ofFinite I
  obtain ⟨p, hp, rfl⟩ := exists_boxPoint l u hlu x hx
  rw [boxHullGap_eq_of_mem l u hlu _ p hp]
  have hfun : (fun q => monomial s (boxPoint l u q)) =
      supportPolynomial s.powerset (boxExpansionCoefficient l u s) :=
    funext fun q => monomial_box_expansion l u q s
  rw [hfun]
  exact affine_hullGap_eq_zero _ _
    (fun w hw => le_trans (Finset.card_le_card (Finset.mem_powerset.mp hw)) hs) p hp

omit [DecidableEq I] in
/-- **Dimensions zero and one.**  In an ambient dimension of at most one every
monomial has degree at most one, so the termwise gap of every nonnegative
multilinear polynomial vanishes on every coordinate box. -/
theorem boxTermwiseGap_eq_zero_of_card_le_one (hI : Fintype.card I ≤ 1)
    (T : Finset (Finset I)) (b : Finset I → ℝ) (l u : I → ℝ) (hlu : ∀ i, l i ≤ u i)
    {x : I → ℝ} (hx : x ∈ coordinateBox l u) : boxTermwiseGap T b l u x = 0 := by
  classical
  refine Finset.sum_eq_zero fun s _ => ?_
  have hs : s.card ≤ 1 := le_trans (Finset.card_le_univ s) hI
  rw [boxHullGap_monomial_eq_zero_of_card_le_one l u hlu hs hx, mul_zero]

/-! ## PB31: the polynomial bound on `[1, rho]^N` -/

omit [DecidableEq I] in
/-- **PB31, the PB22 analogue.**  On `[1, rho]^N` the termwise relaxation gap of
an arbitrary multilinear polynomial with nonnegative coefficients is at most
`rho + β_N` times its exact hull gap.  Dimensions zero and one are included: the
first branch below is exactly those, where `β_N = 0` and both gaps of every term
vanish. -/
theorem commonAspect_termwiseGap_le_balanced (rho : ℝ) (hrho : 1 ≤ rho)
    (T : Finset (Finset I)) (b : Finset I → ℝ) (y : I → ℝ) (hb : ∀ s ∈ T, 0 ≤ b s)
    (hy : y ∈ coordinateBox (fun _ => (1 : ℝ)) (fun _ => rho)) :
    boxTermwiseGap T b (fun _ => (1 : ℝ)) (fun _ => rho) y ≤
      (rho + orientationBeta (Fintype.card I)) *
        boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (supportPolynomial T b) y := by
  classical
  have ht : (0 : ℝ) ≤ rho - 1 := by linarith
  have hlu : ∀ _ : I, (1 : ℝ) ≤ rho := fun _ => hrho
  have h2 : (0 : ℝ) ≤ rho + orientationBeta (Fintype.card I) :=
    (zero_lt_add_orientationBeta hrho _).le
  rcases le_or_gt (Fintype.card I) 1 with hdim | hdim
  · -- dimensions zero and one: every term has degree at most one
    rw [boxTermwiseGap_eq_zero_of_card_le_one hdim T b _ _ hlu hy]
    exact mul_nonneg h2
      (boxHullGap_nonneg _ _ hlu _ (supportPolynomial_coordinate_affine T b) y hy)
  have hN : 2 ≤ Fintype.card I := hdim
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
    exact Finset.sum_congr rfl fun s _ => rfl
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
    rw [expect_finsetSum' (thresholdLaw p) T (fun s v => b s * physMonomial t s (vertexPoint v))]
    exact Finset.sum_congr rfl fun s _ => by
      rw [Law.expect_const_mul, thresholdLaw_physMonomial t s p hp]
  have hMexp : (balancedMixtureLaw rho hrho p hp).expect (fun v => F (vertexPoint v)) =
      ∑ s ∈ T, b s * (balancedMixtureLaw rho hrho p hp).expect
        (fun v => physMonomial t s (vertexPoint v)) := by
    rw [hFdef]
    rw [expect_finsetSum' (balancedMixtureLaw rho hrho p hp) T
      (fun s v => b s * physMonomial t s (vertexPoint v))]
    exact Finset.sum_congr rfl fun s _ => by rw [Law.expect_const_mul]
  have hgap : (∑ s ∈ T, b s * physUpper t s p) -
      (∑ s ∈ T, b s * (balancedMixtureLaw rho hrho p hp).expect
        (fun v => physMonomial t s (vertexPoint v))) ≤ hullGap F p := by
    rw [← hCexp, ← hMexp]
    exact expect_sub_le_hullGap' F haff p _ _ (thresholdLaw_hasMeans p hp)
      (balancedMixtureLaw_hasMeans rho hrho p hp)
  -- assemble
  have hstep : ∑ s ∈ T, b s * (physUpper t s p - physLower t s p) ≤
      (rho + orientationBeta (Fintype.card I)) * ((∑ s ∈ T, b s * physUpper t s p) -
        ∑ s ∈ T, b s * (balancedMixtureLaw rho hrho p hp).expect
          (fun v => physMonomial t s (vertexPoint v))) := by
    rw [mul_sub, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib]
    refine Finset.sum_le_sum fun s hs => ?_
    have hcap := balancedMixtureLaw_capture hN rho hrho p hp s
    rw [physMonomial_hullGap _ ht s p hp,
      div_le_iff₀ (zero_lt_add_orientationBeta hrho (Fintype.card I))] at hcap
    have hs' : physUpper t s p - physLower t s p ≤
        (rho + orientationBeta (Fintype.card I)) *
          (physUpper t s p - (balancedMixtureLaw rho hrho p hp).expect
            (fun v => physMonomial t s (vertexPoint v))) := by
      rw [htdef]; linarith [hcap]
    calc b s * (physUpper t s p - physLower t s p)
        ≤ b s * ((rho + orientationBeta (Fintype.card I)) *
            (physUpper t s p - (balancedMixtureLaw rho hrho p hp).expect
              (fun v => physMonomial t s (vertexPoint v)))) :=
          mul_le_mul_of_nonneg_left hs' (hb s hs)
      _ = (rho + orientationBeta (Fintype.card I)) * (b s * physUpper t s p) -
            (rho + orientationBeta (Fintype.card I)) *
              (b s * (balancedMixtureLaw rho hrho p hp).expect
                (fun v => physMonomial t s (vertexPoint v))) := by ring
  rw [hterm, boxHullGap_eq_of_mem _ _ hlu _ p hp, hpoly]
  exact hstep.trans (mul_le_mul_of_nonneg_left hgap h2)

/-! ## PB31: every strictly positive `N`-dimensional box -/

/-- The `N`-dimensional analogue of `PositiveBoxAspectBound`.  The ambient
dimension must be fixed because `β_N` depends on it; everything else is the
dimension-free statement verbatim. -/
def PositiveBoxAspectBoundOfDim (N : ℕ) (rho U : ℝ) : Prop :=
  ∀ (K : Type) [Fintype K] [DecidableEq K], Fintype.card K = N →
    ∀ (S : Finset (Finset K)) (a : Finset K → ℝ) (l u x : K → ℝ),
      (∀ s ∈ S, 0 ≤ a s) → (∀ i, 0 < l i) → (∀ i, l i ≤ u i) → (∀ i, u i ≤ rho * l i) →
        x ∈ coordinateBox l u →
          boxTermwiseGap S a l u x ≤ U * boxHullGap l u (supportPolynomial S a) x

/-- **PB31.**  `tbtgap f ≤ (rho + β_N) chgap f` on every `N`-dimensional strictly
positive box with coordinate aspect ratios at most `rho`, including the unequal
box transfer.  The transfer is the one of
`originalBox_bound_of_commonAspect_bound`, restated at a fixed ambient dimension:
the affine substitution keeps the same `N` coordinates, so the expanded supports
are subsets of the same index type and use restrictions of the same ambient
orientation law, and the constant `β_N` is unchanged.  No nondegeneracy
hypothesis is needed, so fixed coordinates are allowed; dimensions zero and one
are covered by `commonAspect_termwiseGap_le_balanced`. -/
theorem positiveBoxAspectBound_add_orientationBeta {rho : ℝ} (hrho : 1 < rho) (N : ℕ) :
    PositiveBoxAspectBoundOfDim N rho (rho + orientationBeta N) := by
  intro K _ _ hcard S a l u z ha hl hlu hasp hz
  subst hcard
  obtain ⟨x, hx, rfl⟩ := exists_originalBoxPoint hrho hl hlu hz
  refine (boxTermwiseGap_originalBox_le_expansion hrho S a ha hl hlu hasp hx).trans ?_
  refine le_trans (commonAspect_termwiseGap_le_balanced rho hrho.le _ _ x
    (fun w _ => originalPolynomialCoefficient_nonneg hrho S a ha hl hlu hasp w) hx) ?_
  exact le_of_eq (congrArg (fun w => (rho + orientationBeta (Fintype.card K)) * w)
    (boxHullGap_originalBox_expansion hrho S a hl hlu hx).symm)

/-- **PB31**, the improvement recorded.  In every ambient dimension `N ≥ 2` the
finite-dimensional constant is strictly smaller than the dimension-free
`rho + 2` of `positiveBoxAspectBound_add_two`. -/
theorem add_orientationBeta_lt_add_two {rho : ℝ} {N : ℕ} (hN : 2 ≤ N) :
    rho + orientationBeta N < rho + 2 := by
  linarith [orientationBeta_lt_two hN]

end

end MultilinearGap
