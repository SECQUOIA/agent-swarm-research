import Formal.CubicGap.Expectation
import Formal.MultilinearGap.StructuralFrequency

/-! Explicit matching/complement rounding on every odd cycle of length at least three. -/
namespace MultilinearGap.StructuralFrequencyCycle

open CubicGap
open scoped BigOperators
noncomputable section

/-- Both vertices and edges are numbered cyclically. Edge `e` joins `e` and `e+1`. -/
abbrev Cycle (k : ℕ) := Fin (2 * k + 3)

/-- The alternating matching whose only uncovered vertex is `r`. -/
def matching (k : ℕ) (r : Cycle k) : Vertex (Cycle k) :=
  fun e => decide ((e - r).val % 2 = 1)

/-- Coverage by the two incident cycle edges. -/
def covered {k : ℕ} (f : Vertex (Cycle k)) (v : Cycle k) : ℝ :=
  if f v || f (v - 1) then 1 else 0

private theorem adjacent_parity (k : ℕ) (d : Cycle k) :
    (d.val % 2 = 1 ∨ (d - 1).val % 2 = 1) ↔ d ≠ 0 := by
  by_cases hd : d = 0
  · subst d
    simp
  · have hv : d.val ≠ 0 := by
      intro h
      exact hd (Fin.ext h)
    rw [Fin.val_sub_one_of_ne_zero hd]
    have hlt := d.isLt
    have hp := Nat.mod_lt d.val (by omega : 0 < 2)
    have hp' := Nat.mod_lt (d.val - 1) (by omega : 0 < 2)
    constructor
    · intro _
      exact hd
    · intro _
      omega

private theorem adjacent_not_both (k : ℕ) (d : Cycle k) :
    ¬ (d.val % 2 = 1 ∧ (d - 1).val % 2 = 1) := by
  by_cases hd : d = 0
  · subst d
    simp
  · have hv : d.val ≠ 0 := by
      intro h
      exact hd (Fin.ext h)
    rw [Fin.val_sub_one_of_ne_zero hd]
    omega

/-- Each matching misses precisely its specified vertex. -/
theorem covered_matching (k : ℕ) (r v : Cycle k) :
    covered (matching k r) v = if v = r then 0 else 1 := by
  have hs : v - 1 - r = (v - r) - 1 := by abel
  simp only [covered, matching, hs, Bool.or_eq_true, decide_eq_true_eq]
  simp only [adjacent_parity, sub_ne_zero, ite_not]

/-- The complement of each matching covers every cycle vertex. -/
theorem covered_complement_matching (k : ℕ) (r v : Cycle k) :
    covered (fun e => !(matching k r e)) v = 1 := by
  have hs : v - 1 - r = (v - r) - 1 := by abel
  have hp := adjacent_not_both k (v - r)
  simp only [covered, matching, hs, Bool.or_eq_true, Bool.not_eq_true',
    decide_eq_false_iff_not]
  split_ifs with h
  · rfl
  · tauto


/-- Uniform missing vertex and an independent fair choice of matching or complement. -/
def roundingLaw (k : ℕ) : Law (Vertex (Cycle k)) :=
  ((Law.uniform (Cycle k)).prod (Law.uniform Bool)).map
    (fun rb e => if rb.2 then matching k rb.1 e else !(matching k rb.1 e))

/-- The construction preserves every fractional edge coordinate. -/
theorem roundingLaw_mean (k : ℕ) (e : Cycle k) :
    (roundingLaw k).expect (fun f => vertexPoint f e) = 1 / 2 := by
  simp only [roundingLaw, Law.expect_map, Law.expect_prod, Function.comp_def,
    Law.expect_uniform, Fintype.card_bool, Fintype.sum_bool]
  have hp (r : Cycle k) :
      (vertexPoint (fun e => matching k r e) e +
        vertexPoint (fun e => !(matching k r e)) e) / 2 = (1 : ℝ) / 2 := by
    cases h : matching k r e <;> simp [vertexPoint, h]
  simp only [Bool.false_eq_true, ↓reduceIte]
  simp only [Nat.cast_ofNat, hp]
  simp [Cycle]
  field_simp

/-- Every vertex has coverage probability `1 - 1/(2L)`, for `L = 2k+3`. -/
theorem roundingLaw_coverage (k : ℕ) (v : Cycle k) :
    (roundingLaw k).expect (fun f => covered f v) =
      1 - 1 / (2 * (2 * (k : ℝ) + 3)) := by
  simp only [roundingLaw, Law.expect_map, Law.expect_prod, Function.comp_def,
    Law.expect_uniform, Fintype.card_bool, Fintype.sum_bool,
    Bool.false_eq_true, ↓reduceIte, covered_matching, covered_complement_matching]
  have hp (r : Cycle k) : ((if v = r then (0 : ℝ) else 1) + 1) / 2 =
      1 - if r = v then 1 / 2 else 0 := by
    by_cases h : r = v
    · subst r
      norm_num
    · simp only [if_neg h, if_neg (Ne.symm h)]
      norm_num
  simp only [Nat.cast_ofNat]
  simp_rw [hp]
  simp only [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, mul_one, Finset.sum_ite_eq', Finset.mem_univ,
    ↓reduceIte, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat]
  have hn : (2 * (k : ℝ) + 3) ≠ 0 := by positivity
  field_simp


/-- Number of selected cycle edges. -/
def selectedCount {k : ℕ} (f : Vertex (Cycle k)) : ℕ :=
  ∑ e, if f e then 1 else 0

/-- Number of cycle vertices incident to a selected edge. -/
def coveredCount {k : ℕ} (f : Vertex (Cycle k)) : ℕ :=
  ∑ v, if f v || f (v - 1) then 1 else 0

/-- Every selected edge has just two endpoints. -/
theorem coveredCount_le_twice {k : ℕ} (f : Vertex (Cycle k)) :
    coveredCount f ≤ 2 * selectedCount f := by
  have hp (v : Cycle k) :
      (if f v || f (v - 1) then 1 else 0) ≤
        (if f v then 1 else 0) + (if f (v - 1) then 1 else 0) := by
    cases f v <;> cases f (v - 1) <;> decide
  have h := Finset.sum_le_sum (fun v (_ : v ∈ Finset.univ) => hp v)
  rw [Finset.sum_add_distrib] at h
  have he := (Equiv.subRight (1 : Cycle k)).sum_comp
    (fun v => if f v then (1 : ℕ) else 0)
  change (∑ v, if f (v - 1) then 1 else 0) = selectedCount f at he
  rw [he] at h
  change coveredCount f ≤ selectedCount f + selectedCount f at h
  omega

/-- Coverage cannot exceed the cycle length. -/
theorem coveredCount_le_length {k : ℕ} (f : Vertex (Cycle k)) :
    coveredCount f ≤ 2 * k + 3 := by
  have h := Finset.sum_le_sum (s := Finset.univ) (g := fun _ : Cycle k => (1 : ℕ))
    (fun v _ => show (if f v || f (v - 1) then 1 else 0) ≤ 1 by split_ifs <;> omega)
  simpa [coveredCount, Cycle] using h

/-- The pointwise inequality proving odd-cycle sharpness. -/
theorem coveredCount_le_selected_add {k : ℕ} (f : Vertex (Cycle k)) :
    coveredCount f ≤ selectedCount f + (k + 1) := by
  have h₁ := coveredCount_le_twice f
  have h₂ := coveredCount_le_length f
  omega

private theorem coveredCount_cast {k : ℕ} (f : Vertex (Cycle k)) :
    (coveredCount f : ℝ) = ∑ v, covered f v := by
  simp [coveredCount, covered]

private theorem selectedCount_cast {k : ℕ} (f : Vertex (Cycle k)) :
    (selectedCount f : ℝ) = ∑ e, vertexPoint f e := by
  simp [selectedCount, vertexPoint]

/-- No half-marginal law can exceed the coverage attained by cycle rounding. -/
theorem expected_coverage_le (k : ℕ) (μ : Law (Vertex (Cycle k)))
    (hμ : ∀ e, μ.expect (fun f => vertexPoint f e) = 1 / 2) :
    μ.expect (fun f => ∑ v, covered f v) ≤ (2 * (k : ℝ) + 3) - 1 / 2 := by
  have h := μ.expect_mono (fun f => show (∑ v, covered f v) ≤
      (∑ e, vertexPoint f e) + ((k : ℝ) + 1) by
    rw [← coveredCount_cast, ← selectedCount_cast]
    exact_mod_cast coveredCount_le_selected_add f)
  simp only [Law.expect_add, Law.expect_sum, hμ, Law.expect_const] at h
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat] at h
  rw [Law.expect_sum]
  linarith

/-- The matching/complement law attains the sharp total coverage. -/
theorem roundingLaw_total_coverage (k : ℕ) :
    (roundingLaw k).expect (fun f => ∑ v, covered f v) =
      (2 * (k : ℝ) + 3) - 1 / 2 := by
  rw [Law.expect_sum]
  simp only [roundingLaw_coverage, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat]
  have hn : (2 * (k : ℝ) + 3) ≠ 0 := by positivity
  field_simp


/-- Bilinear monomial at a vertex of the dual cycle. -/
def support (k : ℕ) (v : Cycle k) : Finset (Cycle k) := {v, v - 1}

/-- The original monomial supports of the cycle example. -/
def supports (k : ℕ) : Finset (Finset (Cycle k)) := Finset.univ.image (support k)

private theorem one_ne_zero (k : ℕ) : (1 : Cycle k) ≠ 0 := by
  intro h
  have hv := congrArg Fin.val h
  norm_num at hv

private theorem two_ne_zero (k : ℕ) : (2 : Cycle k) ≠ 0 := by
  intro h
  have hv := congrArg Fin.val h
  norm_num [Fin.val_ofNat, Nat.mod_eq_of_lt (show 2 < 2 * k + 3 by omega)] at hv

/-- Every cycle monomial is genuinely bilinear. -/
theorem support_card (k : ℕ) (v : Cycle k) : (support k v).card = 2 := by
  have h : v ≠ v - 1 := by
    intro hv
    exact one_ne_zero k (sub_eq_self.mp hv.symm)
  simp [support, h]

/-- Distinct cycle vertices have distinct monomial supports. -/
theorem support_injective (k : ℕ) : Function.Injective (support k) := by
  intro v w h
  have hv : v = w ∨ v = w - 1 := by
    have : v ∈ support k w := h ▸ (by simp [support])
    simpa [support] using this
  rcases hv with rfl | hv
  · rfl
  have hv' : v - 1 = w ∨ v - 1 = w - 1 := by
    have : v - 1 ∈ support k w := h ▸ (by simp [support])
    simpa [support] using this
  rcases hv' with hv' | hv'
  · exfalso
    apply two_ne_zero k
    have ha : v + 1 = w := eq_sub_iff_add_eq.mp hv
    have hb : v = w + 1 := sub_eq_iff_eq_add.mp hv'
    have hc : v = v + (1 + 1) := by rw [← add_assoc, ha]; exact hb
    have hz : (1 : Cycle k) + 1 = 0 :=
      add_left_cancel (hc.symm.trans (add_zero v).symm)
    have htwo : (1 : Cycle k) + 1 = 2 := by
      apply Fin.ext
      simp [Fin.val_add]
    exact htwo.symm.trans hz
  · exact sub_left_inj.mp hv'

/-- Sums indexed by the original support family equal sums over cycle vertices. -/
theorem sum_supports (k : ℕ) (f : Finset (Cycle k) → ℝ) :
    (∑ s ∈ supports k, f s) = ∑ v, f (support k v) := by
  exact Finset.sum_image (fun v _ w _ h => support_injective k h)

/-- Each cycle variable occurs in at most two original monomials. -/
theorem frequencyTwo_supports (k : ℕ) : FrequencyTwo (supports k) := by
  intro e
  have hsub : ((supports k).filter fun s => e ∈ s) ⊆
      {support k e, support k (e + 1)} := by
    intro s hs
    obtain ⟨hs, he⟩ := Finset.mem_filter.mp hs
    obtain ⟨v, _, rfl⟩ := Finset.mem_image.mp hs
    simp only [support, Finset.mem_insert, Finset.mem_singleton] at he
    rcases he with he | he
    · subst v
      simp
    · have hv : v = e + 1 := (eq_sub_iff_add_eq.mp he).symm
      subst v
      simp
  exact (Finset.card_le_card hsub).trans (by
    simpa using Finset.card_insert_le (support k e) {support k (e + 1)})

/-- Coverage semantics agree with the general support-polynomial interface. -/
theorem failureCovered_support (k : ℕ) (f : Vertex (Cycle k)) (v : Cycle k) :
    failureCovered (support k v) f = covered f v := by
  simp [failureCovered, support, covered, Bool.or_eq_true]


/-- Number of selected cycle edges incident to one vertex. -/
def incidentCount {k : ℕ} (f : Vertex (Cycle k)) (v : Cycle k) : ℕ :=
  (if f v then 1 else 0) + (if f (v - 1) then 1 else 0)

/-- A matching has degree zero at its designated missing vertex and one elsewhere. -/
theorem incidentCount_matching (k : ℕ) (r v : Cycle k) :
    incidentCount (matching k r) v = if v = r then 0 else 1 := by
  have hm := covered_matching k r v
  have hc := covered_complement_matching k r v
  by_cases h : v = r <;>
    cases h₁ : matching k r v <;> cases h₂ : matching k r (v - 1) <;>
    simp_all [covered, incidentCount]

/-- Complementation reverses the two incident binary selections. -/
theorem incidentCount_complement {k : ℕ} (f : Vertex (Cycle k)) (v : Cycle k) :
    incidentCount (fun e => !(f e)) v = 2 - incidentCount f v := by
  cases h₁ : f v <;> cases h₂ : f (v - 1) <;> simp [incidentCount, h₁, h₂]

/-- The complete incident-degree distribution, with any fixed integral degree added.
This identity supports arbitrary objective functions of the local degree. -/
theorem roundingLaw_incidentCount (k : ℕ) (v : Cycle k) (m : ℕ) (φ : ℕ → ℝ) :
    (roundingLaw k).expect (fun f => φ (m + incidentCount f v)) =
      φ (m + 1) + ((φ m + φ (m + 2)) / 2 - φ (m + 1)) /
        (2 * (k : ℝ) + 3) := by
  simp only [roundingLaw, Law.expect_map, Law.expect_prod, Function.comp_def,
    Law.expect_uniform, Fintype.card_bool, Fintype.sum_bool,
    Bool.false_eq_true, ↓reduceIte, incidentCount_complement, incidentCount_matching,
    Nat.cast_ofNat]
  have hp (r : Cycle k) :
      (φ (m + (if v = r then 0 else 1)) +
        φ (m + (2 - (if v = r then 0 else 1)))) / 2 =
        φ (m + 1) + if r = v then (φ m + φ (m + 2)) / 2 - φ (m + 1) else 0 := by
    by_cases h : r = v
    · subst r
      simp
    · simp only [if_neg h, if_neg (Ne.symm h)]
      norm_num
  simp_rw [hp]
  simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, Finset.sum_ite_eq', Finset.mem_univ,
    ↓reduceIte, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat]
  have hn : (2 * (k : ℝ) + 3) ≠ 0 := by positivity
  field_simp

end
end MultilinearGap.StructuralFrequencyCycle
