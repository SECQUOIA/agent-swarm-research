import Formal.MultilinearGap.ExactArithmetic
import Formal.MultilinearGap.ExactGeometry
import Formal.MultilinearGap.ExactWeights
import Formal.MultilinearGap.Construction
import Formal.CubicGap.Envelope
import Formal.CubicGap.Expectation

/-! Finite mixtures used to attain the exact dyadic hull gap. -/
namespace MultilinearGap
noncomputable section
open CubicGap
open scoped BigOperators

/-- A finite mixture of finite laws, allowing the conditional law to vary
with the outer state. -/
def finiteMixture {Ω V : Type*} [Fintype Ω] [Fintype V]
    (μ : Law Ω) (ν : Ω → Law V) : Law V where
  weight v := ∑ ω, μ.weight ω * (ν ω).weight v
  nonneg v := Finset.sum_nonneg fun ω _ => mul_nonneg (μ.nonneg ω) ((ν ω).nonneg v)
  mass_one := by
    rw [Finset.sum_comm]
    simp only [← Finset.mul_sum, Law.mass_one, mul_one]

theorem expect_finiteMixture {Ω V : Type*} [Fintype Ω] [Fintype V]
    (μ : Law Ω) (ν : Ω → Law V) (f : V → ℝ) :
    (finiteMixture μ ν).expect f = μ.expect (fun ω => (ν ω).expect f) := by
  simp only [Law.expect, finiteMixture, Finset.sum_mul]
  rw [Finset.sum_comm]
  simp only [Finset.mul_sum, mul_assoc]

theorem expect_mix {V : Type*} [Fintype V] (μ ν : Law V)
    (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : a + b = 1) (f : V → ℝ) :
    (μ.mix ν a b ha hb hab).expect f = a * μ.expect f + b * ν.expect f := by
  simp [Law.expect, Law.mix, add_mul, Finset.sum_add_distrib, Finset.mul_sum, mul_assoc]

/-- Conditional leaf law at one dyadic state. -/
def cutoffLeafLaw (L q l : ℕ) : Law (Vertex (Fin (2 ^ L))) :=
  if l < q then Law.point (fun _ => true) else leafLaw L (l - q + 1)

/-- The active anchors form an initial segment of levels. -/
def cutoffStateLaw (L q : ℕ) (l : Fin (L + 1)) : Law (Vertex (Coord L)) :=
  (cutoffLeafLaw L q l.val).map (fun v => Sum.elim (fun j => decide (j.val + 1 ≤ l.val)) v)

/-- A dyadic cutoff law on the original binary coordinates. -/
def cutoffLaw (L q : ℕ) : Law (Vertex (Coord L)) :=
  finiteMixture (dyadicLaw L) (cutoffStateLaw L q)

theorem cutoffLeafLaw_mean (L q : ℕ) (hq : 1 ≤ q) (l : Fin (L + 1))
    (i : Fin (2 ^ L)) :
    (cutoffLeafLaw L q l.val).expect (fun v => vertexPoint v i) =
      1 - dyadicFailures q l.val / 2 ^ L := by
  by_cases h : l.val < q
  · simp [cutoffLeafLaw, h, dyadicFailures, vertexPoint]
  · simp only [cutoffLeafLaw, if_neg h, dyadicFailures]
    exact leafLaw_mean L (l.val - q + 1) (by omega) i

theorem cutoffLeafLaw_level (L q : ℕ) (hq : 1 ≤ q) (l : Fin (L + 1))
    (j : Fin L) :
    (cutoffLeafLaw L q l.val).expect (fun v =>
      ∑ b : Fin (blockCount L j), ∏ i ∈ block L j b, vertexPoint v i) =
      (blockCount L j : ℝ) - min (blockCount L j : ℝ) (dyadicFailures q l.val) := by
  by_cases h : l.val < q
  · simp [cutoffLeafLaw, h, dyadicFailures, vertexPoint]
  · simp only [cutoffLeafLaw, if_neg h, dyadicFailures]
    exact leafLaw_level_sum L (l.val - q + 1) (by omega) j

theorem cutoffLaw_anchor (L q : ℕ) (j : Fin L) :
    (cutoffLaw L q).expect (fun v => vertexPoint v (Sum.inl j)) = means L (Sum.inl j) := by
  rw [cutoffLaw, expect_finiteMixture]
  simp only [cutoffStateLaw, Law.expect_map, Function.comp_def, vertexPoint, Sum.elim_inl,
    decide_eq_true_eq, Law.expect_const]
  simpa [means, blockCount] using dyadicLaw_tail L (j.val + 1) (by omega)

theorem cutoffLaw_leaf (L q : ℕ) (hq : 1 ≤ q) (hqL : q ≤ L) (i : Fin (2 ^ L)) :
    (cutoffLaw L q).expect (fun v => vertexPoint v (Sum.inr i)) =
      1 - cutoffBudget L q / 2 ^ L := by
  rw [cutoffLaw, expect_finiteMixture]
  simp only [cutoffStateLaw, Law.expect_map, Function.comp_def]
  change (dyadicLaw L).expect (fun l =>
    (cutoffLeafLaw L q l.val).expect (fun v => vertexPoint v i)) = _
  simp only [cutoffLeafLaw_mean L q hq, Law.expect_sub, Law.expect_const,
    Law.expect_div_const, dyadicLaw_failures L q hqL]

theorem cutoffStateLaw_polynomial (L q : ℕ) (hq : 1 ≤ q) (l : Fin (L + 1)) :
    (cutoffStateLaw L q l).expect (fun v => polynomial L (vertexPoint v)) =
      ∑ j : Fin L, if j.val + 1 ≤ l.val then
        (blockCount L j : ℝ) - min (blockCount L j : ℝ) (dyadicFailures q l.val) else 0 := by
  rw [cutoffStateLaw, Law.expect_map]
  simp only [Function.comp_def, polynomial, monomial_support, Law.expect_sum]
  apply Finset.sum_congr rfl
  intro j _
  simp only [vertexPoint, Sum.elim_inl, Sum.elim_inr, decide_eq_true_eq]
  by_cases h : j.val + 1 ≤ l.val
  · simp only [if_pos h, one_mul]
    rw [← Law.expect_sum]
    exact cutoffLeafLaw_level L q hq l j
  · simp [h]

theorem cutoffLaw_polynomial (L q : ℕ) (hq : 1 ≤ q) (hqL : q ≤ L) :
    (cutoffLaw L q).expect (fun v => polynomial L (vertexPoint v)) =
      (L : ℝ) - cutoffDeficit L q := by
  rw [cutoffLaw, expect_finiteMixture]
  simp only [cutoffStateLaw_polynomial L q hq]
  have hsplit (l : Fin (L + 1)) :
      (∑ j : Fin L, if j.val + 1 ≤ l.val then
        (blockCount L j : ℝ) - min (blockCount L j : ℝ) (dyadicFailures q l.val) else 0) =
      (∑ j : Fin L, (if j.val + 1 ≤ l.val then 1 else 0) * (blockCount L j : ℝ)) -
        dyadicSelected L q l.val := by
    rw [dyadicSelected, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro j _
    split <;> simp_all [blockCount]
  simp only [hsplit, Law.expect_sub, Law.expect_sum, Law.expect_mul_const,
    dyadicLaw_selected L q hqL]
  have hscale (j : Fin L) :
      (dyadicLaw L).expect (fun l => if j.val + 1 ≤ l.val then 1 else 0) *
        (blockCount L j : ℝ) = 1 := by
    rw [dyadicLaw_tail L _ (by omega)]
    simp [blockCount]
  simp only [hscale, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    mul_one]

/-- Adjacent cutoff laws combine into a law with the prescribed means and
the exact expectation of destroyed terms. -/
theorem mix_cutoff_laws (L s : ℕ) (hs : s ≤ L)
    (hlo : cutoffBudget L (s + 1) ≤ 1) (hhi : 1 ≤ cutoffBudget L s)
    (μ ν : Law (Vertex (Coord L)))
    (ha : ∀ j, μ.expect (fun v => vertexPoint v (Sum.inl j)) = means L (Sum.inl j))
    (hb : ∀ j, ν.expect (fun v => vertexPoint v (Sum.inl j)) = means L (Sum.inl j))
    (hla : ∀ i, μ.expect (fun v => vertexPoint v (Sum.inr i)) =
      1 - cutoffBudget L s / 2 ^ L)
    (hlb : ∀ i, ν.expect (fun v => vertexPoint v (Sum.inr i)) =
      1 - cutoffBudget L (s + 1) / 2 ^ L)
    (hva : μ.expect (fun v => polynomial L (vertexPoint v)) = (L : ℝ) - cutoffDeficit L s)
    (hvb : ν.expect (fun v => polynomial L (vertexPoint v)) = (L : ℝ) - cutoffDeficit L (s + 1)) :
    ∃ ρ : Law (Vertex (Coord L)), HasMeans ρ (means L) ∧
      ρ.expect (fun v => polynomial L (vertexPoint v)) =
        (L : ℝ) - ((s : ℝ) + ((L : ℝ) - s) / 2 ^ s) := by
  obtain ⟨hp0, hp1⟩ := cutoffMix_mem_unit L s hs hlo hhi
  let ρ := μ.mix ν (cutoffMix L s) (1 - cutoffMix L s) hp0 (by linarith) (by ring)
  refine ⟨ρ, ?_, ?_⟩
  · intro i
    cases i with
    | inl j =>
      rw [show ρ = _ from rfl, expect_mix, ha, hb]
      ring
    | inr i =>
      rw [show ρ = _ from rfl, expect_mix, hla, hlb]
      have hbudget := cutoffMix_budget L s hs
      dsimp [means]
      calc
        _ = 1 - (cutoffMix L s * cutoffBudget L s +
          (1 - cutoffMix L s) * cutoffBudget L (s + 1)) / 2 ^ L := by ring
        _ = _ := by rw [hbudget]
  · rw [show ρ = _ from rfl, expect_mix, hva, hvb]
    have hdeficit := cutoffMix_deficit L s hs
    linarith

/-- An explicit mixture of the two adjacent cutoff constructions attains
the exact lower envelope candidate at the prescribed coordinate means. -/
theorem exists_exact_attaining_law (L s : ℕ) (hs1 : 1 ≤ s) (hsL : s < L)
    (hlo : cutoffBudget L (s + 1) ≤ 1) (hhi : 1 ≤ cutoffBudget L s) :
    ∃ ρ : Law (Vertex (Coord L)), HasMeans ρ (means L) ∧
      ρ.expect (fun v => polynomial L (vertexPoint v)) =
        (L : ℝ) - ((s : ℝ) + ((L : ℝ) - s) / 2 ^ s) := by
  exact mix_cutoff_laws L s (by omega) hlo hhi (cutoffLaw L s) (cutoffLaw L (s + 1))
    (cutoffLaw_anchor L s) (cutoffLaw_anchor L (s + 1))
    (cutoffLaw_leaf L s hs1 (by omega))
    (cutoffLaw_leaf L (s + 1) (by omega) (by omega))
    (cutoffLaw_polynomial L s hs1 (by omega))
    (cutoffLaw_polynomial L (s + 1) (by omega) (by omega))

end
end MultilinearGap
