import Mathlib

/-! Finite-coordinate density and boundary extension for switching profiles. -/
namespace SwitchingControl.Boundary

noncomputable section

/-- Convex interpolation of two finite real coordinate arrays. -/
def interpolate {C : Type*} (x y : C → ℝ) (ε : ℝ) (c : C) : ℝ :=
  (1 - ε) * x c + ε * y c

/-- A segment whose endpoint avoids each finite forbidden set has arbitrarily
small positive parameters avoiding all the forbidden coordinate values. -/
theorem exists_interpolation_avoiding {C : Type*} [Finite C]
    (x y : C → ℝ) (bad : C → Finset ℝ)
    (hy : ∀ c, y c ∉ bad c) {δ : ℝ} (hδ : 0 < δ) :
    ∃ ε : ℝ, 0 < ε ∧ ε < 1 ∧ ε < δ ∧
      ∀ c, interpolate x y ε c ∉ bad c := by
  classical
  let := Fintype.ofFinite C
  let forbidden : Finset ℝ := Finset.univ.biUnion fun c =>
    (bad c).image fun z => (z - x c) / (y c - x c)
  have hI := Set.Ioo_infinite (lt_min zero_lt_one hδ)
  obtain ⟨ε, hε, havoid⟩ := (hI.sdiff forbidden.finite_toSet).nonempty
  refine ⟨ε, hε.1, (lt_min_iff.mp hε.2).1, (lt_min_iff.mp hε.2).2, ?_⟩
  intro c hc
  have hdiff : y c - x c ≠ 0 := by
    intro h
    have hxy : y c = x c := sub_eq_zero.mp h
    have heq : interpolate x y ε c = y c := by
      simp only [interpolate, hxy]
      ring
    exact hy c (heq ▸ hc)
  have heq : (interpolate x y ε c - x c) / (y c - x c) = ε := by
    apply (div_eq_iff hdiff).2
    simp only [interpolate]
    ring
  apply havoid
  change ε ∈ forbidden
  exact Finset.mem_biUnion.mpr ⟨c, Finset.mem_univ c,
    Finset.mem_image.mpr ⟨interpolate x y ε c, hc, heq⟩⟩

/-- The interpolant of bounded arrays is bounded by the same interval. -/
theorem interpolate_bounds {C : Type*} (x y : C → ℝ) (M : ℝ)
    (hx : ∀ c, 0 ≤ x c ∧ x c ≤ M) (hy : ∀ c, 0 ≤ y c ∧ y c ≤ M)
    {ε : ℝ} (hε : 0 ≤ ε) (hε1 : ε ≤ 1) (c : C) :
    0 ≤ interpolate x y ε c ∧ interpolate x y ε c ≤ M := by
  dsimp [interpolate]
  constructor
  · exact add_nonneg (mul_nonneg (sub_nonneg.mpr hε1) (hx c).1)
      (mul_nonneg hε (hy c).1)
  · nlinarith [mul_nonneg (sub_nonneg.mpr hε1) (sub_nonneg.mpr (hx c).2),
      mul_nonneg hε (sub_nonneg.mpr (hy c).2)]

/-- Nonintegral coordinates are dense along interpolation toward any bounded
baseline whose coordinates are all nonintegral. -/
theorem exists_strict_interpolation {C : Type*} [Finite C]
    (x y : C → ℝ) (M : ℕ)
    (hx : ∀ c, 0 ≤ x c ∧ x c ≤ M) (hy : ∀ c, 0 ≤ y c ∧ y c ≤ M)
    (hystrict : ∀ c (z : ℤ), y c ≠ z) {δ : ℝ} (hδ : 0 < δ) :
    ∃ ε : ℝ, 0 < ε ∧ ε < 1 ∧ ε < δ ∧
      ∀ c (z : ℤ), interpolate x y ε c ≠ z := by
  classical
  let bad : Finset ℝ := (Finset.Icc (0 : ℤ) M).image (Int.cast : ℤ → ℝ)
  have hybad : ∀ c, y c ∉ bad := by
    intro c hc
    obtain ⟨z, _, hz⟩ := Finset.mem_image.mp hc
    exact hystrict c z hz.symm
  obtain ⟨ε, hε, hε1, hεδ, hs⟩ :=
    exists_interpolation_avoiding x y (fun _ => bad) hybad hδ
  refine ⟨ε, hε, hε1, hεδ, ?_⟩
  intro c z heq
  have hb := interpolate_bounds x y M hx hy hε.le hε1.le c
  have hz : z ∈ Finset.Icc (0 : ℤ) M := by
    simp only [Finset.mem_Icc]
    constructor
    · exact_mod_cast (heq ▸ hb).1
    · exact_mod_cast (heq ▸ hb).2
  exact hs c (Finset.mem_image.mpr ⟨z, hz, heq.symm⟩)

/-- For finitely many candidate witnesses, arbitrarily small additive errors
imply that one candidate satisfies the exact weak bound. -/
theorem finite_witness_closed {C W : Type*} [Finite W]
    (error : W → C → ℝ) (B : ℝ)
    (happrox : ∀ δ : ℝ, 0 < δ → ∃ w, ∀ c, error w c ≤ B + δ) :
    ∃ w, ∀ c, error w c ≤ B := by
  classical
  obtain ⟨winit, _⟩ := happrox 1 zero_lt_one
  let : Nonempty W := ⟨winit⟩
  let := Fintype.ofFinite W
  by_contra h
  push Not at h
  choose c hc using h
  obtain ⟨w₀, _, hmin⟩ := Finset.exists_min_image Finset.univ
    (fun w => error w (c w) - B) Finset.univ_nonempty
  have hpos : 0 < (error w₀ (c w₀) - B) / 2 := by linarith [hc w₀]
  obtain ⟨w, hw⟩ := happrox _ hpos
  have hm := hmin w (Finset.mem_univ w)
  have he := hw (c w)
  linarith

/-- A uniform coordinate-error bound for every strict interpolant extends to
its possibly integral boundary profile, with one of the same finitely many
candidate schedules. The candidate type can encode the switch restriction. -/
theorem extend_strict_bound {C W : Type*} [Finite C] [Finite W]
    (x y : C → ℝ) (count : W → C → ℝ) (M : ℕ) (B : ℝ)
    (hx : ∀ c, 0 ≤ x c ∧ x c ≤ M) (hy : ∀ c, 0 ≤ y c ∧ y c ≤ M)
    (hystrict : ∀ c (z : ℤ), y c ≠ z)
    (hbound : ∀ ε : ℝ, 0 < ε → ε < 1 →
      (∀ c (z : ℤ), interpolate x y ε c ≠ z) →
      ∃ w, ∀ c, |interpolate x y ε c - count w c| ≤ B) :
    ∃ w, ∀ c, |x c - count w c| ≤ B := by
  apply finite_witness_closed (fun w c => |x c - count w c|) B
  intro δ hδ
  have hM : (0 : ℝ) < M + 1 := by positivity
  obtain ⟨ε, hε, hε1, hεδ, hs⟩ :=
    exists_strict_interpolation x y M hx hy hystrict (div_pos hδ hM)
  obtain ⟨w, hw⟩ := hbound ε hε hε1 hs
  refine ⟨w, fun c => ?_⟩
  have hd : |y c - x c| ≤ M := by
    rw [abs_le]
    constructor <;> linarith [(hx c).1, (hx c).2, (hy c).1, (hy c).2]
  have hdiff : |x c - interpolate x y ε c| = ε * |y c - x c| := by
    have heq : x c - interpolate x y ε c = -(ε * (y c - x c)) := by
      dsimp [interpolate]
      ring
    rw [heq, abs_neg, abs_mul, abs_of_pos hε]
  have heps : ε * (M + 1) < δ := (lt_div_iff₀ hM).mp hεδ
  calc
    |x c - count w c| ≤ |x c - interpolate x y ε c| +
        |interpolate x y ε c - count w c| := abs_sub_le _ _ _
    _ ≤ ε * M + B := by rw [hdiff]; exact add_le_add (mul_le_mul_of_nonneg_left hd hε.le) (hw c)
    _ ≤ B + δ := by nlinarith

end
end SwitchingControl.Boundary
