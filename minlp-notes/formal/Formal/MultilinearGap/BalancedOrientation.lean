import Formal.MultilinearGap.Couplings

/-! # The balanced ambient orientation law and its pair constant

This file discharges obligations PB27 and PB28 of topic 18
(`topics/18-positive-box/CLAIMS.md`), following
`notes/review-positive-box-balanced-orientation-closure.md`.

## PB27, the constant

`pairOppositeProb N` is `p_N = 2 ⌊N/2⌋ ⌈N/2⌉ / (N (N - 1))` and
`orientationBeta N` is `β_N = 1 / p_N`. The closed form `β_N = 2 - 2/N` for
even `N` and `β_N = 2 - 2/(N+1)` for odd `N` is proved in
`orientationBeta_even` and `orientationBeta_odd`, both under the source's
standing hypothesis `2 ≤ N`.

**Convention at `N = 0` and `N = 1`.** The source fixes an ambient dimension
`N ≥ 2`; for `N ≤ 1` the denominator `N (N - 1)` vanishes and `p_N` is not
defined mathematically. Lean's division is total, so the definitions evaluate
to the junk values `p_0 = p_1 = 0` and `β_0 = β_1 = 0`
(`pairOppositeProb_of_lt_two`, `orientationBeta_of_lt_two`). Those junk values
do **not** satisfy the closed form (under the same total division
`2 - 2/0 = 2` and `2 - 2/(1+1) = 1`), which is why every closed-form and
probability statement below carries `2 ≤ N` explicitly. The source says
nothing about `N ≤ 1` beyond noting that dimensions zero and one have zero
gaps.

## PB28, the law

A low set `H` is drawn uniformly among the subsets of size `⌊N/2⌋`
(`balancedSubsets`), independently of one uniform variable on `[0,1]`.
A coordinate in `H` succeeds on `[0, x i]`, a coordinate outside `H` succeeds
on `(1 - x i, 1]` (`orientedProb`); both intervals have length `x i`, so the
mixture `balancedOrientationLaw` has the prescribed means
(`balancedOrientationLaw_hasMeans`).

Every distinct pair is oppositely oriented with probability exactly `p_N`
(`balancedSubsets_pair_opposite`), and — the point of the construction — that
probability is unchanged when the coins are restricted to any set `S` of
coordinates (`balancedSubsets_restrict_pair_opposite`): the restricted coins
are `H ∩ S` for the *ambient* `H`, never resampled in dimension `#S`. The
ambient constant `p_N` is what appears, not `p_{#S}`; the two differ in
general (`pairOppositeProb_two` versus `pairOppositeProb_three`).

Individual fairness is **not** claimed and genuinely fails for odd `N`: a
coordinate is low with probability `⌊N/2⌋ / N` (`balancedSubsets_mem`), which
equals `1/2` only for even `N` (`balancedSubsets_mem_ne_half_of_odd`).

Probabilities are expectations of indicators of events under `CubicGap.Law`.
-/

namespace MultilinearGap

open CubicGap MeasureTheory

noncomputable section

/-! ### PB27: the pair constant `p_N` and the coefficient `β_N` -/

/-- The balanced pair constant `p_N = 2 ⌊N/2⌋ ⌈N/2⌉ / (N (N - 1))`. Division is
total, so `p_0 = p_1 = 0`; every statement about `p_N` assumes `2 ≤ N`. -/
def pairOppositeProb (N : ℕ) : ℝ :=
  2 * (N / 2 : ℕ) * ((N + 1) / 2 : ℕ) / ((N : ℝ) * ((N : ℝ) - 1))

/-- The balanced orientation coefficient `β_N = 1 / p_N`. -/
def orientationBeta (N : ℕ) : ℝ := 1 / pairOppositeProb N

/-- Junk convention below the source's standing hypothesis `2 ≤ N`: the
denominator `N (N - 1)` vanishes, so total division returns zero. -/
theorem pairOppositeProb_of_lt_two {N : ℕ} (hN : N < 2) : pairOppositeProb N = 0 := by
  interval_cases N <;> norm_num [pairOppositeProb]

/-- The same junk convention for `β_N`: the closed forms below fail at
`N = 0, 1` and are therefore stated for `2 ≤ N`. -/
theorem orientationBeta_of_lt_two {N : ℕ} (hN : N < 2) : orientationBeta N = 0 := by
  rw [orientationBeta, pairOppositeProb_of_lt_two hN, div_zero]

/-- `p_2 = 1`: with two coordinates the pair is always oppositely oriented. -/
theorem pairOppositeProb_two : pairOppositeProb 2 = 1 := by
  norm_num [pairOppositeProb]

/-- `p_3 = 2/3`. Together with `pairOppositeProb_two` this shows that the pair
constant depends on the ambient dimension, so a restricted law must not be
resampled in the smaller dimension. -/
theorem pairOppositeProb_three : pairOppositeProb 3 = 2 / 3 := by
  norm_num [pairOppositeProb]

/-- The pair constant is positive in every admissible ambient dimension. -/
theorem pairOppositeProb_pos {N : ℕ} (hN : 2 ≤ N) : 0 < pairOppositeProb N := by
  have h1 : (1 : ℝ) ≤ (N / 2 : ℕ) := by
    exact_mod_cast Nat.one_le_iff_ne_zero.mpr (by omega : N / 2 ≠ 0)
  have h2 : (1 : ℝ) ≤ ((N + 1) / 2 : ℕ) := by
    exact_mod_cast Nat.one_le_iff_ne_zero.mpr (by omega : (N + 1) / 2 ≠ 0)
  have hN' : (2 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  exact div_pos (by nlinarith) (by nlinarith)

/-- `β_N p_N = 1`, the identity used by the coefficient induction. -/
theorem orientationBeta_mul_pairOppositeProb {N : ℕ} (hN : 2 ≤ N) :
    orientationBeta N * pairOppositeProb N = 1 :=
  one_div_mul_cancel (pairOppositeProb_pos hN).ne'

/-- `p_N` as a ratio of binomial coefficients: the two ways of splitting a fixed
pair among the `⌊N/2⌋`-subsets, out of `binom(N, ⌊N/2⌋)` subsets in all. -/
theorem pairOppositeProb_eq_choose {N : ℕ} (hN : 2 ≤ N) :
    pairOppositeProb N =
      2 * ((N - 2).choose (N / 2 - 1) : ℝ) / (N.choose (N / 2) : ℝ) := by
  obtain ⟨m, rfl⟩ : ∃ m, N = m + 2 := ⟨N - 2, by omega⟩
  obtain ⟨a, ha⟩ : ∃ a, (m + 2) / 2 = a + 1 := ⟨(m + 2) / 2 - 1, by omega⟩
  have hsub : m + 2 - 2 = m := by omega
  have hone : (m + 2) / 2 - 1 = a := by omega
  have hceil : (m + 2 + 1) / 2 = m + 1 - a := by omega
  have key : Nat.choose m a * ((m + 2) * (m + 1)) =
      Nat.choose (m + 2) (a + 1) * ((a + 1) * (m + 1 - a)) := by
    have h1 := Nat.add_one_mul_choose_eq m a
    have h2 := Nat.choose_succ_right_eq (m + 1) a
    have h3 := Nat.add_one_mul_choose_eq (m + 1) a
    calc Nat.choose m a * ((m + 2) * (m + 1))
        = (m + 1) * Nat.choose m a * (m + 2) := by ring
      _ = Nat.choose (m + 1) (a + 1) * (a + 1) * (m + 2) := by rw [h1]
      _ = Nat.choose (m + 1) a * (m + 1 - a) * (m + 2) := by rw [h2]
      _ = (m + 1 + 1) * Nat.choose (m + 1) a * (m + 1 - a) := by ring
      _ = Nat.choose (m + 2) (a + 1) * (a + 1) * (m + 1 - a) := by rw [h3]
      _ = Nat.choose (m + 2) (a + 1) * ((a + 1) * (m + 1 - a)) := by ring
  have keyR : (Nat.choose m a : ℝ) * (((m : ℝ) + 2) * ((m : ℝ) + 1)) =
      (Nat.choose (m + 2) (a + 1) : ℝ) * (((a : ℝ) + 1) * ((m + 1 - a : ℕ) : ℝ)) := by
    exact_mod_cast congrArg (fun n : ℕ => (n : ℝ)) key
  have hchoose : ((m + 2).choose (a + 1) : ℝ) ≠ 0 := by
    have hpos : 0 < (m + 2).choose (a + 1) := Nat.choose_pos (by omega)
    exact_mod_cast hpos.ne'
  have hden : ((m + 2 : ℕ) : ℝ) * (((m + 2 : ℕ) : ℝ) - 1) ≠ 0 := by
    refine ne_of_gt ?_
    have h : (0 : ℝ) ≤ (m : ℝ) := Nat.cast_nonneg m
    push_cast
    nlinarith
  rw [pairOppositeProb, hsub, hone, ha, hceil]
  rw [div_eq_div_iff hden hchoose]
  push_cast
  linear_combination (-2 : ℝ) * keyR

/-- PB27 for even ambient dimension: `β_N = 2 - 2/N`. -/
theorem orientationBeta_even {N : ℕ} (hN : 2 ≤ N) (hpar : Even N) :
    orientationBeta N = 2 - 2 / (N : ℝ) := by
  obtain ⟨m, rfl⟩ := hpar
  have hm : (m : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
  have h1 : (m + m) / 2 = m := by omega
  have h2 : (m + m + 1) / 2 = m := by omega
  rw [orientationBeta, pairOppositeProb, h1, h2, one_div_div]
  push_cast
  field_simp
  ring

/-- PB27 for odd ambient dimension: `β_N = 2 - 2/(N+1)`. -/
theorem orientationBeta_odd {N : ℕ} (hN : 2 ≤ N) (hpar : Odd N) :
    orientationBeta N = 2 - 2 / ((N : ℝ) + 1) := by
  obtain ⟨m, rfl⟩ := hpar
  have hm : (m : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
  have hm1 : (m : ℝ) + 1 ≠ 0 := by positivity
  have h1 : (2 * m + 1) / 2 = m := by omega
  have h2 : (2 * m + 1 + 1) / 2 = m + 1 := by omega
  rw [orientationBeta, pairOppositeProb, h1, h2, one_div_div]
  push_cast
  field_simp
  ring

/-- The refinement never exceeds the ambient constant two: `1 ≤ β_N < 2`. -/
theorem orientationBeta_lt_two {N : ℕ} (hN : 2 ≤ N) : orientationBeta N < 2 := by
  have hN' : (2 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  rcases Nat.even_or_odd N with hpar | hpar
  · rw [orientationBeta_even hN hpar]
    have : 0 < 2 / (N : ℝ) := by positivity
    linarith
  · rw [orientationBeta_odd hN hpar]
    have : 0 < 2 / ((N : ℝ) + 1) := by positivity
    linarith

/-- The refinement is never weaker than one. -/
theorem one_le_orientationBeta {N : ℕ} (hN : 2 ≤ N) : 1 ≤ orientationBeta N := by
  have hN' : (2 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  rcases Nat.even_or_odd N with hpar | hpar
  · rw [orientationBeta_even hN hpar]
    have : 2 / (N : ℝ) ≤ 1 := by rw [div_le_one (by linarith)]; linarith
    linarith
  · rw [orientationBeta_odd hN hpar]
    have : 2 / ((N : ℝ) + 1) ≤ 1 := by rw [div_le_one (by linarith)]; linarith
    linarith

/-! ### PB28: the balanced low sets -/

variable {I : Type*} [Fintype I] [DecidableEq I]

omit [DecidableEq I] in
/-- The subsets of size `⌊N/2⌋` are exactly the `⌊N/2⌋`-element subsets of the
whole coordinate set. -/
theorem balancedSupport_eq :
    (Finset.univ.filter fun H : Finset I => H.card = Fintype.card I / 2) =
      Finset.powersetCard (Fintype.card I / 2) (Finset.univ : Finset I) := by
  ext H
  simp [Finset.mem_powersetCard]

/-- The low coordinates: a uniformly random subset `H` of size `⌊N/2⌋` of the
`N` ambient coordinates. This is the orientation coin of the balanced law; it
is drawn once, ambiently, and never resampled. -/
def balancedSubsets (I : Type*) [Fintype I] [DecidableEq I] : Law (Finset I) where
  weight H :=
    if H.card = Fintype.card I / 2 then
      (((Fintype.card I).choose (Fintype.card I / 2) : ℝ))⁻¹
    else 0
  nonneg H := by
    split_ifs
    · exact inv_nonneg.mpr (Nat.cast_nonneg _)
    · exact le_rfl
  mass_one := by
    have hc : ((Fintype.card I).choose (Fintype.card I / 2) : ℝ) ≠ 0 := by
      have hpos := Nat.choose_pos (Nat.div_le_self (Fintype.card I) 2)
      exact_mod_cast hpos.ne'
    rw [← Finset.sum_filter, balancedSupport_eq, Finset.sum_const,
      Finset.card_powersetCard, Finset.card_univ, nsmul_eq_mul]
    exact mul_inv_cancel₀ hc

/-- Expectations under the balanced coin law are averages over the
`⌊N/2⌋`-subsets. -/
theorem balancedSubsets_expect (f : Finset I → ℝ) :
    (balancedSubsets I).expect f =
      (∑ H ∈ Finset.powersetCard (Fintype.card I / 2) (Finset.univ : Finset I), f H) /
        ((Fintype.card I).choose (Fintype.card I / 2) : ℝ) := by
  simp only [Law.expect, balancedSubsets, ite_mul, zero_mul]
  rw [← Finset.sum_filter, balancedSupport_eq, ← Finset.mul_sum, inv_mul_eq_div]

/-- Two coordinates are oppositely oriented under the low set `H` when exactly
one of them is low. -/
def OppositeOrientation (H : Finset I) (i j : I) : Prop :=
  (i ∈ H ∧ j ∉ H) ∨ (j ∈ H ∧ i ∉ H)

instance (H : Finset I) (i j : I) : Decidable (OppositeOrientation H i j) :=
  inferInstanceAs (Decidable ((i ∈ H ∧ j ∉ H) ∨ (j ∈ H ∧ i ∉ H)))

/-- Erasing `i` is a bijection from the `k`-subsets containing `i` but not `j`
onto the `(k-1)`-subsets of the other `N - 2` coordinates. -/
theorem card_powersetCard_filter_mem_notMem {k : ℕ} (hk : 1 ≤ k) {i j : I} (hij : i ≠ j) :
    ((Finset.powersetCard k (Finset.univ : Finset I)).filter
        (fun H => i ∈ H ∧ j ∉ H)).card = (Fintype.card I - 2).choose (k - 1) := by
  have hTcard : (((Finset.univ : Finset I).erase i).erase j).card = Fintype.card I - 2 := by
    rw [Finset.card_erase_of_mem (by simp [Ne.symm hij]),
      Finset.card_erase_of_mem (Finset.mem_univ i), Finset.card_univ]
    omega
  rw [← hTcard, ← Finset.card_powersetCard]
  refine Finset.card_bij' (fun H _ => H.erase i) (fun G _ => insert i G) ?_ ?_ ?_ ?_
  · intro H hH
    simp only [Finset.mem_filter, Finset.mem_powersetCard] at hH
    obtain ⟨⟨-, hcard⟩, hiH, hjH⟩ := hH
    rw [Finset.mem_powersetCard]
    refine ⟨fun x hx => ?_, ?_⟩
    · have hxi : x ≠ i := Finset.ne_of_mem_erase hx
      have hxH : x ∈ H := Finset.mem_of_mem_erase hx
      have hxj : x ≠ j := fun h => hjH (h ▸ hxH)
      simp [Finset.mem_erase, hxi, hxj]
    · rw [Finset.card_erase_of_mem hiH, hcard]
  · intro G hG
    rw [Finset.mem_powersetCard] at hG
    obtain ⟨hGT, hGcard⟩ := hG
    have hiG : i ∉ G := fun h => by simpa using hGT h
    have hjG : j ∉ G := fun h => by simpa using hGT h
    simp only [Finset.mem_filter, Finset.mem_powersetCard]
    refine ⟨⟨Finset.subset_univ _, ?_⟩, Finset.mem_insert_self i G, ?_⟩
    · rw [Finset.card_insert_of_notMem hiG, hGcard]
      omega
    · simp [Finset.mem_insert, Ne.symm hij, hjG]
  · intro H hH
    simp only [Finset.mem_filter] at hH
    exact Finset.insert_erase hH.2.1
  · intro G hG
    rw [Finset.mem_powersetCard] at hG
    exact Finset.erase_insert (fun h => by simpa using hG.1 h)

/-- Erasing `i` is a bijection from the `k`-subsets containing `i` onto the
`(k-1)`-subsets of the other `N - 1` coordinates. -/
theorem card_powersetCard_filter_mem {k : ℕ} (hk : 1 ≤ k) (i : I) :
    ((Finset.powersetCard k (Finset.univ : Finset I)).filter
        (fun H => i ∈ H)).card = (Fintype.card I - 1).choose (k - 1) := by
  have hTcard : ((Finset.univ : Finset I).erase i).card = Fintype.card I - 1 := by
    rw [Finset.card_erase_of_mem (Finset.mem_univ i), Finset.card_univ]
  rw [← hTcard, ← Finset.card_powersetCard]
  refine Finset.card_bij' (fun H _ => H.erase i) (fun G _ => insert i G) ?_ ?_ ?_ ?_
  · intro H hH
    simp only [Finset.mem_filter, Finset.mem_powersetCard] at hH
    obtain ⟨⟨-, hcard⟩, hiH⟩ := hH
    rw [Finset.mem_powersetCard]
    refine ⟨fun x hx => ?_, ?_⟩
    · have hxi : x ≠ i := Finset.ne_of_mem_erase hx
      simp [Finset.mem_erase, hxi]
    · rw [Finset.card_erase_of_mem hiH, hcard]
  · intro G hG
    rw [Finset.mem_powersetCard] at hG
    obtain ⟨hGT, hGcard⟩ := hG
    have hiG : i ∉ G := fun h => by simpa using hGT h
    simp only [Finset.mem_filter, Finset.mem_powersetCard]
    refine ⟨⟨Finset.subset_univ _, ?_⟩, Finset.mem_insert_self i G⟩
    rw [Finset.card_insert_of_notMem hiG, hGcard]
    omega
  · intro H hH
    simp only [Finset.mem_filter] at hH
    exact Finset.insert_erase hH.2
  · intro G hG
    rw [Finset.mem_powersetCard] at hG
    exact Finset.erase_insert (fun h => by simpa using hG.1 h)

/-- **PB28, pair probability.** Every distinct pair of ambient coordinates is
oppositely oriented with probability exactly `p_N`. -/
theorem balancedSubsets_pair_opposite (hN : 2 ≤ Fintype.card I) {i j : I} (hij : i ≠ j) :
    (balancedSubsets I).expect (fun H => if OppositeOrientation H i j then 1 else 0) =
      pairOppositeProb (Fintype.card I) := by
  have hk : 1 ≤ Fintype.card I / 2 := by omega
  have hpoint : ∀ H : Finset I, (if OppositeOrientation H i j then (1 : ℝ) else 0) =
      (if i ∈ H ∧ j ∉ H then (1 : ℝ) else 0) + (if j ∈ H ∧ i ∉ H then (1 : ℝ) else 0) := by
    intro H
    by_cases h1 : i ∈ H <;> by_cases h2 : j ∈ H <;> simp [OppositeOrientation, h1, h2]
  rw [balancedSubsets_expect]
  simp only [hpoint]
  rw [Finset.sum_add_distrib, Finset.sum_boole, Finset.sum_boole,
    card_powersetCard_filter_mem_notMem hk hij,
    card_powersetCard_filter_mem_notMem hk (Ne.symm hij),
    pairOppositeProb_eq_choose hN]
  ring

/-- **PB28, restriction.** Restricting the ambient coins to a set `S` of
coordinates replaces `H` by `H ∩ S`; the pair probability of any two distinct
coordinates of `S` is still the **ambient** `p_N`, not `p_{#S}`. This is the
statement that makes the coefficient induction close with one constant. -/
theorem balancedSubsets_restrict_pair_opposite (hN : 2 ≤ Fintype.card I) (S : Finset I)
    {i j : I} (hi : i ∈ S) (hj : j ∈ S) (hij : i ≠ j) :
    ((balancedSubsets I).map (fun H => H ∩ S)).expect
        (fun H => if OppositeOrientation H i j then 1 else 0) =
      pairOppositeProb (Fintype.card I) := by
  rw [Law.expect_map]
  have hfun : (fun H : Finset I =>
      (fun K : Finset I => if OppositeOrientation K i j then (1 : ℝ) else 0) (H ∩ S)) =
      fun H : Finset I => if OppositeOrientation H i j then (1 : ℝ) else 0 := by
    funext H
    have hiff : OppositeOrientation (H ∩ S) i j ↔ OppositeOrientation H i j := by
      simp [OppositeOrientation, Finset.mem_inter, hi, hj]
    exact if_congr hiff rfl rfl
  rw [Function.comp_def, hfun]
  exact balancedSubsets_pair_opposite hN hij

/-- Individual orientations are **not** fair: a coordinate is low with
probability `⌊N/2⌋ / N`. -/
theorem balancedSubsets_mem (hN : 2 ≤ Fintype.card I) (i : I) :
    (balancedSubsets I).expect (fun H => if i ∈ H then 1 else 0) =
      ((Fintype.card I / 2 : ℕ) : ℝ) / (Fintype.card I : ℝ) := by
  have hk : 1 ≤ Fintype.card I / 2 := by omega
  obtain ⟨n, hn⟩ : ∃ n, Fintype.card I = n + 1 := ⟨Fintype.card I - 1, by omega⟩
  obtain ⟨a, ha⟩ : ∃ a, Fintype.card I / 2 = a + 1 := ⟨Fintype.card I / 2 - 1, by omega⟩
  have key : (n + 1) * Nat.choose n a = Nat.choose (n + 1) (a + 1) * (a + 1) :=
    Nat.add_one_mul_choose_eq n a
  have hchoose : ((Fintype.card I).choose (Fintype.card I / 2) : ℝ) ≠ 0 := by
    have hpos := Nat.choose_pos (Nat.div_le_self (Fintype.card I) 2)
    exact_mod_cast hpos.ne'
  have hcard : (Fintype.card I : ℝ) ≠ 0 := by
    have : Fintype.card I ≠ 0 := by omega
    exact_mod_cast this
  rw [balancedSubsets_expect, Finset.sum_boole, card_powersetCard_filter_mem hk i,
    div_eq_div_iff hchoose hcard]
  have hsub : Fintype.card I - 1 = n := by omega
  have hone : Fintype.card I / 2 - 1 = a := by omega
  have key' : Nat.choose n a * (n + 1) = (a + 1) * Nat.choose (n + 1) (a + 1) := by
    rw [mul_comm (Nat.choose n a), key]
    ring
  rw [hsub, hone, ha, hn]
  exact_mod_cast key'

/-- For odd ambient dimension the individual orientations are genuinely unfair.
Nothing in the closure argument needs fairness; this lemma records that it must
not be assumed. -/
theorem balancedSubsets_mem_ne_half_of_odd (hN : 2 ≤ Fintype.card I)
    (hpar : Odd (Fintype.card I)) (i : I) :
    (balancedSubsets I).expect (fun H => if i ∈ H then 1 else 0) ≠ 1 / 2 := by
  obtain ⟨m, hm⟩ := hpar
  have hhalf : Fintype.card I / 2 = m := by omega
  have hmpos : (0 : ℝ) < (m : ℝ) := by
    have : 0 < m := by omega
    exact_mod_cast this
  rw [balancedSubsets_mem hN i, hhalf, hm]
  intro hcontra
  rw [div_eq_div_iff (by push_cast; linarith) (by norm_num : (2 : ℝ) ≠ 0)] at hcontra
  push_cast at hcontra
  linarith

/-! ### PB28: the balanced ambient orientation law -/

/-- Coordinate success probabilities given the low set `H` and the shared
uniform parameter `t`: a low coordinate succeeds on `[0, x i]`, a high
coordinate on `(1 - x i, 1]`. Both intervals have length `x i`. -/
def orientedProb (H : Finset I) (x : I → ℝ) (t : ℝ) (i : I) : ℝ :=
  if i ∈ H then (if t ≤ x i then 1 else 0) else (if 1 - x i < t then 1 else 0)

omit [Fintype I] in
/-- Conditional success probabilities are indicators, hence lie in the cube. -/
theorem orientedProb_cube (H : Finset I) (x : I → ℝ) (t : ℝ) :
    orientedProb H x t ∈ cube I := by
  intro i
  dsimp [orientedProb]
  split_ifs <;> norm_num

omit [Fintype I] in
/-- Threshold indicators are measurable in the shared parameter. -/
theorem orientedProb_measurable (H : Finset I) (x : I → ℝ) (i : I) :
    Measurable (fun t => orientedProb H x t i) := by
  unfold orientedProb
  split
  · exact Measurable.ite measurableSet_Iic measurable_const measurable_const
  · exact Measurable.ite measurableSet_Ioi measurable_const measurable_const

omit [Fintype I] in
/-- Both orientations have the prescribed marginal success probability. -/
theorem intervalIntegral_orientedProb (H : Finset I) {x : I → ℝ} (hx : x ∈ cube I) (i : I) :
    (∫ t in (0 : ℝ)..1, orientedProb H x t i) = x i := by
  unfold orientedProb
  split
  · exact intervalIntegral_lower_indicator (hx i)
  · rw [intervalIntegral_upper_indicator ⟨sub_nonneg.mpr (hx i).2, by linarith [(hx i).1]⟩]
    ring

/-- The law of the rounded vertex given the low set `H`: one shared uniform
variable drives every coordinate, with the orientation prescribed by `H`. -/
def orientedLaw (H : Finset I) (x : I → ℝ) : Law (Vertex I) :=
  integratedBernoulli (orientedProb H x) (orientedProb_cube H x) (orientedProb_measurable H x)

/-- Every orientation pattern already has the prescribed means. -/
theorem orientedLaw_hasMeans (H : Finset I) {x : I → ℝ} (hx : x ∈ cube I) :
    HasMeans (orientedLaw H x) x := by
  intro i
  rw [orientedLaw, integratedBernoulli_mean, intervalIntegral_orientedProb H hx i]

/-- Monomial moments of a fixed orientation pattern. -/
theorem orientedLaw_expect_monomial (H : Finset I) (x : I → ℝ) (s : Finset I) :
    (orientedLaw H x).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, monomial s (orientedProb H x t) :=
  integratedBernoulli_expect_monomial _ _ _ _

/-- **PB28, the law.** The balanced ambient orientation law: a uniformly random
low set `H` of size `⌊N/2⌋`, independent of one uniform variable on `[0,1]`. -/
def balancedOrientationLaw (x : I → ℝ) : Law (Vertex I) where
  weight v := ∑ H : Finset I, (balancedSubsets I).weight H * (orientedLaw H x).weight v
  nonneg v :=
    Finset.sum_nonneg fun H _ =>
      mul_nonneg ((balancedSubsets I).nonneg H) ((orientedLaw H x).nonneg v)
  mass_one := by
    have h : ∀ H : Finset I, ∑ v : Vertex I, (orientedLaw H x).weight v = 1 :=
      fun H => (orientedLaw H x).mass_one
    rw [Finset.sum_comm]
    simp only [← Finset.mul_sum, h, mul_one]
    exact (balancedSubsets I).mass_one

/-- Expectations factor as an average over the ambient low sets of the
conditional orientation expectations. The coin `H` is drawn once and shared by
every coordinate; this is the only place the two sources of randomness meet. -/
theorem balancedOrientationLaw_expect (x : I → ℝ) (f : Vertex I → ℝ) :
    (balancedOrientationLaw x).expect f =
      (balancedSubsets I).expect (fun H => (orientedLaw H x).expect f) := by
  simp only [Law.expect, balancedOrientationLaw, Finset.sum_mul, Finset.mul_sum, mul_assoc]
  exact Finset.sum_comm

/-- **PB28, the means.** The balanced ambient orientation law has the prescribed
means, for every point of the cube. -/
theorem balancedOrientationLaw_hasMeans {x : I → ℝ} (hx : x ∈ cube I) :
    HasMeans (balancedOrientationLaw x) x := by
  intro i
  have h : (fun H : Finset I => (orientedLaw H x).expect (fun v => vertexPoint v i)) =
      fun _ : Finset I => x i :=
    funext fun H => orientedLaw_hasMeans H hx i
  rw [balancedOrientationLaw_expect, h]
  simp only [Law.expect]
  rw [← Finset.sum_mul, (balancedSubsets I).mass_one, one_mul]

/-- Monomial moments of the balanced law: average the conditional orientation
moments over the ambient low sets. -/
theorem balancedOrientationLaw_expect_monomial (x : I → ℝ) (s : Finset I) :
    (balancedOrientationLaw x).expect (fun v => monomial s (vertexPoint v)) =
      (balancedSubsets I).expect
        (fun H => ∫ t in (0 : ℝ)..1, monomial s (orientedProb H x t)) := by
  rw [balancedOrientationLaw_expect]
  simp only [orientedLaw_expect_monomial]

end

end MultilinearGap
