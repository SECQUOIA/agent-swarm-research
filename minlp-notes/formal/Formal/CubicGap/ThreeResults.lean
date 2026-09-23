import Formal.CubicGap.Finite
import Formal.CubicGap.Laws
import Formal.CubicGap.Families
import Formal.CubicGap.CountLaws
import Formal.CubicGap.Expectation
import Formal.CubicGap.Envelope
import Formal.CubicGap.LargeBridge

namespace CubicGap

noncomputable section

namespace PrimalLaw

variable {k m : ℕ} {states : Fin k → Fin 3 → Fin (m + 1)} {weights : Fin k → ℚ}
  {value : ℕ → ℕ → ℕ → ℚ} {objective : ℚ}

/-- A rational primal certificate is an actual probability law over the reals. -/
def realLaw (h : PrimalLaw states weights value objective) : Law (Fin k) where
  weight i := (weights i : ℝ)
  nonneg i := by exact_mod_cast h.1 i
  mass_one := by exact_mod_cast h.2.1

theorem expect_real (h : PrimalLaw states weights value objective) (f : Fin k → ℚ) :
    h.realLaw.expect (fun i => (f i : ℝ)) = ((∑ i, weights i * f i : ℚ) : ℝ) := by
  simp [realLaw, Law.expect]

theorem mean_real (h : PrimalLaw states weights value objective) (j : Fin 3) :
    h.realLaw.expect (fun i => (states i j : ℝ)) =
      ![(m : ℝ)/4, (m : ℝ)/2, 3*(m : ℝ)/4] j := by
  have hh := h.2.2.1 j
  have hr := h.expect_real (fun i => (states i j : ℚ))
  rw [hh] at hr
  fin_cases j <;> simpa using hr

end PrimalLaw

def threeMarginals (m : ℕ) : Fin 3 × Fin m → ℝ :=
  fun p => ![1/4, 1/2, 3/4] p.1

theorem primalLaw_attains {k m : ℕ} [NeZero m]
    {states : Fin k → Fin 3 → Fin (m + 1)} {weights : Fin k → ℚ}
    {coef : Fin 6 → ℚ} {q : ℚ} (h : PrimalLaw states weights (countPhi coef) q) :
    ∃ μ : Law (Vertex (Fin 3 × Fin m)),
      (∀ i, μ.expect (fun v => vertexPoint v i) = threeMarginals m i) ∧
      μ.expect (fun v => threeFamily m coef (vertexPoint v)) = (q : ℝ) := by
  let kf : Fin k → Fin 3 → ℕ := fun i g => states i g
  have hk : ∀ i g, kf i g ≤ m := fun i g => Nat.le_of_lt_succ (states i g).isLt
  refine ⟨h.realLaw.liftCounts kf, ?_, ?_⟩
  · rintro ⟨g,j⟩
    rw [liftCounts_mean _ _ hk]
    change h.realLaw.expect (fun i => (states i g : ℝ)) / m = _
    rw [h.mean_real]
    have hm : (m : ℝ) ≠ 0 := by exact_mod_cast NeZero.ne m
    fin_cases g <;> simp [threeMarginals] <;> field_simp
  · have hv : ∀ v : Vertex (Fin 3 × Fin m),
        threeFamily m coef (vertexPoint v) =
        ((countPhi coef (count fun j => v (0,j)) (count fun j => v (1,j))
          (count fun j => v (2,j)) : ℚ) : ℝ) := fun v => threeFamily_binary m coef v
    simp_rw [hv]
    rw [liftCounts_value _ _ hk
      (fun cs => ((countPhi coef (cs 0) (cs 1) (cs 2) : ℚ) : ℝ))]
    rw [h.expect_real]
    exact_mod_cast h.2.2.2

/-- Taking expectations transfers every finite affine certificate to every binary law. -/
theorem three_law_lower (m : ℕ) (coef : Fin 6 → ℚ) (α β γ δ D : ℚ)
    (hminorant : ∀ a b c : Fin (m + 1),
      (α*(a : ℚ)+β*(b : ℚ)+γ*(c : ℚ)+δ)/D ≤ countPhi coef a b c)
    (μ : Law (Vertex (Fin 3 × Fin m)))
    (hmean : ∀ i, μ.expect (fun v => vertexPoint v i) = threeMarginals m i) :
    (((α*((m : ℚ)/4)+β*((m : ℚ)/2)+γ*(3*(m : ℚ)/4)+δ)/D : ℚ) : ℝ) ≤
      μ.expect (fun v => threeFamily m coef (vertexPoint v)) := by
  let cs (v : Vertex (Fin 3 × Fin m)) (g : Fin 3) : Fin (m + 1) :=
    ⟨count (fun j => v (g,j)), Nat.lt_succ_iff.mpr (by simpa using count_le (fun j => v (g,j)))⟩
  have hv (v : Vertex (Fin 3 × Fin m)) :
      ((α : ℝ)*(cs v 0 : ℝ)+(β : ℝ)*(cs v 1 : ℝ)+
        (γ : ℝ)*(cs v 2 : ℝ)+(δ : ℝ))/(D : ℝ) ≤
      threeFamily m coef (vertexPoint v) := by
    rw [show threeFamily m coef (vertexPoint v) =
      ((countPhi coef (cs v 0) (cs v 1) (cs v 2) : ℚ) : ℝ) from
      threeFamily_binary m coef v]
    exact_mod_cast hminorant (cs v 0) (cs v 1) (cs v 2)
  have hb := μ.expect_mono hv
  have hc (g : Fin 3) : μ.expect (fun v => (cs v g : ℝ)) =
      (m : ℝ) * ![(1/4 : ℝ),1/2,3/4] g := by
    exact expect_group_count_of_mean m μ _ (fun g j => hmean (g,j)) g
  simp only [Law.expect_div_const, Law.expect_add, Law.expect_const_mul,
    Law.expect_const, hc] at hb
  change ((α : ℝ)*((m : ℝ)*(1/4))+(β : ℝ)*((m : ℝ)*(1/2))+
    (γ : ℝ)*((m : ℝ)*(3/4))+(δ : ℝ))/(D : ℝ) ≤ _ at hb
  push_cast
  convert hb using 1
  ring

/-- Exact convex-envelope value for the 18-variable three-group example. -/
theorem three_minimum6 :
    IsLeast (envelopeValues (threeFamily 6 coefficients6) (threeMarginals 6))
      (2750/13) := by
  apply minimum_from_laws _ (threeFamily_coordinate_affine 6 coefficients6)
  · intro μ hμ
    have h := three_law_lower 6 coefficients6 962 778 842 (-4816) 13
      (fun a b c => by simpa only [threeValue6, sub_eq_add_neg] using minorant6 a b c) μ hμ
    norm_num at h ⊢
    exact h
  · simpa only [HasMeans, Rat.cast_div, Rat.cast_ofNat] using primalLaw_attains primal6

/-- Exact convex-envelope value for the 24-variable three-group example. -/
theorem three_minimum8 :
    IsLeast (envelopeValues (threeFamily 8 coefficients8) (threeMarginals 8))
      (3572/7) := by
  apply minimum_from_laws _ (threeFamily_coordinate_affine 8 coefficients8)
  · intro μ hμ
    have h := three_law_lower 8 coefficients8 793 770 798 (-5882) 7
      (fun a b c => by simpa only [threeValue8, sub_eq_add_neg] using minorant8 a b c) μ hμ
    norm_num at h ⊢
    exact h
  · simpa only [HasMeans, Rat.cast_div, Rat.cast_ofNat] using primalLaw_attains primal8

/-- Exact convex-envelope value for the 192-variable three-group example. -/
theorem three_minimum64 :
    IsLeast (envelopeValues (threeFamily 64 coefficients64) (threeMarginals 64))
      (34172072/105) := by
  apply minimum_from_laws _ (threeFamily_coordinate_affine 64 coefficients64)
  · intro μ hμ
    have h := three_law_lower 64 coefficients64 871710 900446 899046 (-51743768) 105
      (fun a b c => by simpa only [threeValue64, sub_eq_add_neg] using minorant64 a b c) μ hμ
    norm_num at h ⊢
    exact h
  · simpa only [HasMeans, Rat.cast_div, Rat.cast_ofNat] using primalLaw_attains primal64

end
end CubicGap
