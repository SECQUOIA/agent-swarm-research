import Formal.SwitchingControl.Sharpness

/-! Positive cell-length scaling of all three exact grid values. -/
namespace SwitchingControl

/-- Exact error value for equal cells of length `Δ`, with validity imposed on
normalized relaxed cumulatives and physical integer counts scaled by `Δ`. -/
def ScaledGridValue (n budget : ℕ) (E Δ : ℝ) : Prop :=
    (∀ A : Profile n, ValidProfile (fun j i => A j i / Δ) →
      ∃ w : Finite.Word, w.length = n ∧ Finite.switches w ≤ budget ∧
        ∀ j i, |A j i - Δ * (Finite.countPrefix w (j.val + 1) i : ℝ)| ≤ Δ * E) ∧
    (∃ A : Profile n, ValidProfile (fun j i => A j i / Δ) ∧
      ∀ w : Finite.Word, w.length = n → Finite.switches w ≤ budget →
        ∃ j i, Δ * E ≤ |A j i - Δ * (Finite.countPrefix w (j.val + 1) i : ℝ)|)

/-- Unit-grid exactness gives both bounds at every positive cell length. -/
theorem grid_scaling {n budget : ℕ} {E : ℝ} (h : ExactGridValue n budget E)
    (Δ : ℝ) (hΔ : 0 < Δ) : ScaledGridValue n budget E Δ := by
  constructor
  · intro A hA
    obtain ⟨w, hlen, hsw, he⟩ := h.1 _ hA
    refine ⟨w, hlen, hsw, fun j i => ?_⟩
    have hh := mul_le_mul_of_nonneg_left (he j i) hΔ.le
    have heq : |A j i - Δ * (Finite.countPrefix w (j.val + 1) i : ℝ)| =
        Δ * |A j i / Δ - (Finite.countPrefix w (j.val + 1) i : ℝ)| := by
      calc
        _ = |Δ * (A j i / Δ - (Finite.countPrefix w (j.val + 1) i : ℝ))| := by
          congr 1
          field_simp
        _ = _ := by rw [abs_mul, abs_of_pos hΔ]
    rw [heq]
    exact hh
  · obtain ⟨A, hA, hlow⟩ := h.2
    refine ⟨fun j i => Δ * A j i, ?_, ?_⟩
    · simpa [hΔ.ne'] using hA
    · intro w hlen hsw
      obtain ⟨j, i, hi⟩ := hlow w hlen hsw
      refine ⟨j, i, ?_⟩
      rw [← mul_sub, abs_mul, abs_of_pos hΔ]
      exact mul_le_mul_of_nonneg_left hi hΔ.le

theorem five_grid_scaled (Δ : ℝ) (hΔ : 0 < Δ) : ScaledGridValue 5 2 1 Δ :=
  grid_scaling five_grid_exact Δ hΔ

theorem six_grid_scaled (Δ : ℝ) (hΔ : 0 < Δ) : ScaledGridValue 6 3 1 Δ :=
  grid_scaling six_grid_exact Δ hΔ

theorem seven_grid_scaled (Δ : ℝ) (hΔ : 0 < Δ) : ScaledGridValue 7 3 (4 / 3) Δ :=
  grid_scaling seven_grid_exact Δ hΔ

end SwitchingControl
