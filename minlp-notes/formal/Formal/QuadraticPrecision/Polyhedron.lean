import Mathlib.Analysis.Convex.Basic
import Mathlib.Topology.Order.Monotone
import Mathlib.Tactic

namespace QuadraticPrecision

/-- One step of Fourier–Motzkin elimination, including absent lower or upper bounds. -/
theorem exists_scalar_inequalities {ι : Type*} [Finite ι] (a b : ι → ℝ) :
    (∃ t : ℝ, ∀ i, a i * t ≤ b i) ↔
      (∀ i, a i = 0 → 0 ≤ b i) ∧
      (∀ i j, a i < 0 → 0 < a j → b i / a i ≤ b j / a j) := by
  classical
  let := Fintype.ofFinite ι
  constructor
  · rintro ⟨t, ht⟩
    refine ⟨?_, ?_⟩
    · intro i hi
      simpa [hi] using ht i
    · intro i j hi hj
      exact ((div_le_iff_of_neg hi).2 (by simpa [mul_comm] using ht i)).trans
        ((le_div_iff₀ hj).2 (by simpa [mul_comm] using ht j))
  · rintro ⟨hz, hp⟩
    let neg := Finset.univ.filter (fun i => a i < 0)
    let pos := Finset.univ.filter (fun i => 0 < a i)
    by_cases hn : neg.Nonempty
    · obtain ⟨i, hi, hmax⟩ := neg.exists_max_image (fun i => b i / a i) hn
      refine ⟨b i / a i, fun j => ?_⟩
      rcases lt_trichotomy (a j) 0 with hj | hj | hj
      · simpa [mul_comm] using (div_le_iff_of_neg hj).1 (hmax j (by simp [neg, hj]))
      · simpa [hj] using hz j hj
      · simpa [mul_comm] using (le_div_iff₀ hj).1 (hp i j (by simpa [neg] using hi) hj)
    · by_cases hp' : pos.Nonempty
      · obtain ⟨i, hi, hmin⟩ := pos.exists_min_image (fun i => b i / a i) hp'
        refine ⟨b i / a i, fun j => ?_⟩
        have hj : 0 ≤ a j := le_of_not_gt (fun h => hn ⟨j, by simp [neg, h]⟩)
        rcases hj.eq_or_lt with hj | hj
        · simpa [← hj] using hz j hj.symm
        · simpa [mul_comm] using (le_div_iff₀ hj).1 (hmin j (by simp [pos, hj]))
      · refine ⟨0, fun j => ?_⟩
        have hj : a j = 0 := le_antisymm
          (le_of_not_gt (fun h => hp' ⟨j, by simp [pos, h]⟩))
          (le_of_not_gt (fun h => hn ⟨j, by simp [neg, h]⟩))
        simpa using hz j hj

/-- Projection of finitely many affine inequalities along finitely many real coordinates
is closed. No boundedness or absence of lines is needed. -/
theorem isClosed_exists_linear {E : Type*} [TopologicalSpace E] (n : ℕ)
    {ι : Type*} [Finite ι] (a : ι → Fin n → ℝ) (b : ι → E → ℝ)
    (hb : ∀ i, Continuous (b i)) :
    IsClosed {x : E | ∃ y : Fin n → ℝ, ∀ i, ∑ k, a i k * y k ≤ b i x} := by
  classical
  let := Fintype.ofFinite ι
  induction n generalizing ι with
  | zero =>
    have heq : {x : E | ∃ y : Fin 0 → ℝ, ∀ i, ∑ k, a i k * y k ≤ b i x} =
        {x | ∀ i, 0 ≤ b i x} := by simp
    rw [heq]
    simpa only [Set.ofPred_forall] using
      (isClosed_iInter fun i => isClosed_le
        (continuous_const : Continuous (fun _ : E => (0 : ℝ))) (hb i))
  | succ n ih =>
    let Z := {i : ι // a i 0 = 0}
    let P := {ij : ι × ι // a ij.1 0 < 0 ∧ 0 < a ij.2 0}
    let aa : Z ⊕ P → Fin n → ℝ := Sum.elim
      (fun i k => a i.1 k.succ)
      (fun ij k => a ij.1.2 k.succ / a ij.1.2 0 - a ij.1.1 k.succ / a ij.1.1 0)
    let bb : Z ⊕ P → E → ℝ := Sum.elim
      (fun i => b i.1)
      (fun ij x => b ij.1.2 x / a ij.1.2 0 - b ij.1.1 x / a ij.1.1 0)
    have hbb : ∀ i, Continuous (bb i) := by
      intro i
      cases i with
      | inl i => exact hb i.1
      | inr ij => exact ((hb _).div_const _).sub ((hb _).div_const _)
    have hclosed := ih aa bb hbb
    convert hclosed using 1
    ext x
    change (∃ y : Fin (n+1) → ℝ, ∀ i, ∑ k, a i k * y k ≤ b i x) ↔
      ∃ y : Fin n → ℝ, ∀ i, ∑ k, aa i k * y k ≤ bb i x
    have step (y : Fin n → ℝ) :
        (∃ t, ∀ i, a i 0 * t ≤ b i x - ∑ k, a i k.succ * y k) ↔
          ∀ i, ∑ k, aa i k * y k ≤ bb i x := by
      rw [exists_scalar_inequalities]
      constructor
      · rintro ⟨hz, hp⟩ i
        cases i with
        | inl i => exact sub_nonneg.mp (hz i.1 i.2)
        | inr ij =>
          have h := hp ij.1.1 ij.1.2 ij.2.1 ij.2.2
          dsimp [aa, bb]
          simp only [sub_mul, div_mul_eq_mul_div, Finset.sum_sub_distrib,
            ← Finset.sum_div] 
          rw [sub_div, sub_div] at h
          linarith
      · intro h
        constructor
        · intro i hi
          exact sub_nonneg.mpr (h (.inl ⟨i, hi⟩))
        · intro i j hi hj
          have hh := h (.inr ⟨(i, j), hi, hj⟩)
          dsimp [aa, bb] at hh
          simp only [sub_mul, div_mul_eq_mul_div, Finset.sum_sub_distrib,
            ← Finset.sum_div] at hh
          rw [sub_div, sub_div]
          linarith
    constructor
    · rintro ⟨y, hy⟩
      refine ⟨fun k => y k.succ, (step _).mp ⟨y 0, ?_⟩⟩
      intro i
      have h := hy i
      rw [Fin.sum_univ_succ] at h
      linarith
    · rintro ⟨y, hy⟩
      obtain ⟨t, ht⟩ := (step y).mpr hy
      refine ⟨Fin.cons t y, fun i => ?_⟩
      simpa only [Fin.sum_univ_succ, Fin.cons_zero, Fin.cons_succ,
        le_sub_iff_add_le, add_comm] using ht i

/-- Every feasible finite linear system with a lower-bounded scalar projection
attains its minimum scalar value. The auxiliary feasible set can be unbounded. -/
theorem exists_minimum_linear_projection (n : ℕ) {ι : Type*} [Finite ι]
    (a : ι → Fin n → ℝ) (b : ι → ℝ → ℝ) (hb : ∀ i, Continuous (b i))
    (hfeas : ∃ t, ∃ y : Fin n → ℝ, ∀ i, ∑ k, a i k * y k ≤ b i t)
    (hlower : ∃ L : ℝ, ∀ t, (∃ y : Fin n → ℝ,
      ∀ i, ∑ k, a i k * y k ≤ b i t) → L ≤ t) :
    ∃ t, ∃ y : Fin n → ℝ, (∀ i, ∑ k, a i k * y k ≤ b i t) ∧
      ∀ t', (∃ y' : Fin n → ℝ, ∀ i, ∑ k, a i k * y' k ≤ b i t') → t ≤ t' := by
  let S : Set ℝ := {t | ∃ y : Fin n → ℝ, ∀ i, ∑ k, a i k * y k ≤ b i t}
  have hc : IsClosed S := isClosed_exists_linear n a b hb
  have hn : S.Nonempty := hfeas
  have hl : BddBelow S := by
    obtain ⟨L, hL⟩ := hlower
    exact ⟨L, fun t ht => hL t ht⟩
  obtain ⟨y, hy⟩ := hc.csInf_mem hn hl
  exact ⟨sInf S, y, hy, fun t ht => csInf_le hl ht⟩

end QuadraticPrecision
