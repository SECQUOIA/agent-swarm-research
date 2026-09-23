import Formal.NetworkSimplex.ThresholdFarkas

/-! Exact use of a complete finite circuit library when some normal groups are absent. -/
namespace NetworkSimplex.Threshold
open scoped BigOperators
universe u v

/-- Only circuits whose nonzero weights all have an available row are tested. -/
def PartialCircuitTests {C : Type u} {N : Type v} [Fintype N]
    (weight : C → N → ℝ) (rhs : N → Option ℝ) : Prop :=
  ∀ c, (∀ i, rhs i = none → weight c i = 0) →
    0 ≤ ∑ i, weight c i * (rhs i).getD 0

/-- A sufficiently large bound fills missing groups for a proof of feasibility.
It is not inserted into the executed oracle or its returned affine cuts. -/
theorem complete_partial_library {C : Type u} {N : Type v}
    [Finite C] [Fintype N] {m : ℕ}
    (A : N → Fin m → ℝ) (weight : C → N → ℝ)
    (hw : ∀ c i, weight c i = 0 ∨ 1 ≤ weight c i)
    (complete : ∀ b : N → ℝ, (∀ c, 0 ≤ ∑ i, weight c i * b i) →
      ∃ x : Fin m → ℝ, ∀ i, ∑ j, A i j * x j ≤ b i)
    (rhs : N → Option ℝ) (h : PartialCircuitTests weight rhs) :
    ∃ x : Fin m → ℝ, ∀ i b, rhs i = some b → ∑ j, A i j * x j ≤ b := by
  classical
  let _ : Fintype C := Fintype.ofFinite C
  have hnonneg (c : C) (i : N) : 0 ≤ weight c i := by
    rcases hw c i with he | he
    · rw [he]
    · linarith
  let base : N → ℝ := fun i => (rhs i).getD 0
  let S : ℝ := ∑ c, ∑ i, weight c i * |base i|
  have hS : 0 ≤ S := Finset.sum_nonneg fun c _ =>
    Finset.sum_nonneg fun i _ => mul_nonneg (hnonneg c i) (abs_nonneg _)
  let M := S + 1
  have hM : 0 ≤ M := by dsimp [M]; linarith
  let filled : N → ℝ := fun i => (rhs i).getD M
  let extra : N → ℝ := fun i => if rhs i = none then M else 0
  have heq (i : N) : filled i = base i + extra i := by
    cases hi : rhs i <;> simp [filled, base, extra, hi]
  have hextra (i : N) : 0 ≤ extra i := by dsimp [extra]; split_ifs <;> positivity
  have htests : ∀ c, 0 ≤ ∑ i, weight c i * filled i := by
    intro c
    by_cases hs : ∀ i, rhs i = none → weight c i = 0
    · have he (i : N) : weight c i * filled i = weight c i * base i := by
        cases hi : rhs i with
        | none => simp [hs i hi]
        | some b => simp [filled, base, hi]
      simpa only [he] using h c hs
    · push Not at hs
      obtain ⟨k, hk, hkw⟩ := hs
      have hwk : 1 ≤ weight c k := (hw c k).resolve_left hkw
      have hbound : (∑ i, weight c i * |base i|) ≤ S := by
        dsimp only [S]
        exact Finset.single_le_sum (f := fun d => ∑ i, weight d i * |base i|)
          (fun d _ => Finset.sum_nonneg fun i _ =>
            mul_nonneg (hnonneg d i) (abs_nonneg (base i))) (Finset.mem_univ c)
      have hbase : -S ≤ ∑ i, weight c i * base i := by
        have hh := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) =>
          mul_le_mul_of_nonneg_left (neg_abs_le (base i)) (hnonneg c i))
        simp only [mul_neg, Finset.sum_neg_distrib] at hh
        linarith
      have hsingle : weight c k * extra k ≤ ∑ i, weight c i * extra i :=
        Finset.single_le_sum (fun i _ => mul_nonneg (hnonneg c i) (hextra i))
          (Finset.mem_univ k)
      have hext : M ≤ ∑ i, weight c i * extra i := by
        have hh : M ≤ weight c k * M := by nlinarith
        rw [show extra k = M by simp [extra, hk]] at hsingle
        exact hh.trans hsingle
      simp_rw [heq, mul_add, Finset.sum_add_distrib]
      dsimp [M] at hext
      linarith
  obtain ⟨x, hx⟩ := complete filled htests
  refine ⟨x, ?_⟩
  intro i b hi
  simpa only [filled, hi, Option.getD_some] using hx i

/-- Conversely each present cancellation circuit is valid at every feasible point. -/
theorem partial_library_necessary {C : Type u} {N : Type v} [Fintype N] {m : ℕ}
    (A : N → Fin m → ℝ) (weight : C → N → ℝ)
    (hw : ∀ c i, 0 ≤ weight c i)
    (hc : ∀ c j, ∑ i, weight c i * A i j = 0)
    (rhs : N → Option ℝ) {x : Fin m → ℝ}
    (hx : ∀ i b, rhs i = some b → ∑ j, A i j * x j ≤ b) :
    PartialCircuitTests weight rhs := by
  intro c hs
  have hi (i : N) : weight c i * (∑ j, A i j * x j) ≤ weight c i * (rhs i).getD 0 := by
    cases he : rhs i with
    | none => simp [hs i he]
    | some b => exact mul_le_mul_of_nonneg_left (hx i b he) (hw c i)
  have hsum := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) => hi i)
  have hz : (∑ i, weight c i * (∑ j, A i j * x j)) = 0 := by
    simp_rw [Finset.mul_sum, ← mul_assoc]
    rw [Finset.sum_comm]
    simp_rw [← Finset.sum_mul, hc, zero_mul]
    exact Finset.sum_const_zero
  simpa only [hz] using hsum

end NetworkSimplex.Threshold
