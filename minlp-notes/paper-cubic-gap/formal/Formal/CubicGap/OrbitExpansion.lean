import Formal.CubicGap.TermwiseFamilies

/-! The displayed polynomials are exactly the support orbits used by the
individual-factor envelope sums. -/

namespace CubicGap

noncomputable section

theorem monomial_group {k m : ℕ} (g : Fin k) (s : Finset (Fin m))
    (x : Fin k × Fin m → ℝ) :
    monomial (s.map (groupEmbedding g)) x = ∏ i ∈ s, x (g,i) := by
  simp only [monomial, Finset.prod_map]
  rfl

theorem monomial_mixed {k m : ℕ} (g h : Fin k) (hgh : g ≠ h)
    (i : Fin m) (s : Finset (Fin m)) (x : Fin k × Fin m → ℝ) :
    monomial (insert (g,i) (s.map (groupEmbedding h))) x =
      x (g,i) * ∏ j ∈ s, x (h,j) := by
  have hi : (g,i) ∉ s.map (groupEmbedding h) := by
    intro hh
    obtain ⟨j, _, hj⟩ := Finset.mem_map.mp hh
    exact hgh (congrArg Prod.fst hj).symm
  rw [monomial, Finset.prod_insert hi]
  congr 1
  exact monomial_group h s x

theorem monomial_cross {k m : ℕ} (g h : Fin k) (hgh : g ≠ h)
    (i j : Fin m) (x : Fin k × Fin m → ℝ) :
    monomial {(g,i),(h,j)} x = x (g,i) * x (h,j) := by
  have hi : (g,i) ≠ (h,j) := fun hh => hgh (congrArg Prod.fst hh)
  simp [monomial, hi]

/-- The two-group polynomial is the sum of precisely the factors whose
individual lower and upper envelopes define its termwise relaxation. -/
theorem twoFamily_orbit_expansion (m : ℕ) (x : Fin 2 × Fin m → ℝ) :
    twoFamily m x =
      (∑ i : Fin m, ∑ s ∈ Finset.univ.powersetCard 2,
        monomial (insert (0,i) (s.map (groupEmbedding (1 : Fin 2)))) x) +
      (5 * (m : ℝ) / 4) * (∑ s ∈ Finset.univ.powersetCard 2,
        monomial (s.map (groupEmbedding (0 : Fin 2))) x) := by
  simp_rw [monomial_mixed (0 : Fin 2) 1 (by decide), monomial_group]
  simp only [← Finset.mul_sum, ← Finset.sum_mul]
  rfl

/-- Each of the six displayed polynomial terms expands into the support orbit
used by `termwiseLowerThree` and `termwiseUpperThree`. -/
theorem threeFamily_orbit_expansion (m : ℕ) (coef : Fin 6 → ℚ)
    (x : Fin 3 × Fin m → ℝ) :
    threeFamily m coef x =
      (coef 0 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 3,
        monomial (s.map (groupEmbedding (2 : Fin 3))) x) +
      (coef 1 : ℝ) * (∑ i : Fin m, ∑ s ∈ Finset.univ.powersetCard 2,
        monomial (insert (1,i) (s.map (groupEmbedding (2 : Fin 3)))) x) +
      (coef 2 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 2,
        monomial (s.map (groupEmbedding (1 : Fin 3))) x) +
      (coef 3 : ℝ) * (∑ i : Fin m, ∑ j : Fin m, monomial {(0,i), (2,j)} x) +
      (coef 4 : ℝ) * (∑ i : Fin m, ∑ j : Fin m, monomial {(0,i), (1,j)} x) +
      (coef 5 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 2,
        monomial (s.map (groupEmbedding (0 : Fin 3))) x) := by
  simp_rw [monomial_mixed (1 : Fin 3) 2 (by decide), monomial_group,
    monomial_cross (0 : Fin 3) 2 (by decide), monomial_cross (0 : Fin 3) 1 (by decide)]
  simp only [← Finset.mul_sum, ← Finset.sum_mul]
  unfold threeFamily elementary
  ring

/-- Nonnegative coefficients scale the actual lower envelope of each factor. -/
theorem envelope_minimum_scale {I : Type*} [Finite I] [DecidableEq I]
    (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) (x : I → ℝ) (q c : ℝ)
    (hc : 0 ≤ c) (hmin : IsLeast (envelopeValues f x) q) :
    IsLeast (envelopeValues (fun y => c * f y) x) (c * q) := by
  let : Fintype I := Fintype.ofFinite I
  have hcf : SeparatelyAffine (fun y => c * f y) := by
    intro y i t
    dsimp only
    rw [hf y i t]
    ring
  apply minimum_from_laws _ hcf
  · intro μ hm
    rw [Law.expect_const_mul]
    apply mul_le_mul_of_nonneg_left _ hc
    apply hmin.2
    exact (mem_cubeGraph_hull_iff f hf x _).mpr ⟨μ, hm, rfl⟩
  · obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff f hf x q).mp hmin.1
    exact ⟨μ, hm, by rw [Law.expect_const_mul, hv]⟩

/-- Nonnegative coefficients scale the actual upper envelope of each factor. -/
theorem envelope_maximum_scale {I : Type*} [Finite I] [DecidableEq I]
    (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f) (x : I → ℝ) (q c : ℝ)
    (hc : 0 ≤ c) (hmax : IsGreatest (envelopeValues f x) q) :
    IsGreatest (envelopeValues (fun y => c * f y) x) (c * q) := by
  let : Fintype I := Fintype.ofFinite I
  have hcf : SeparatelyAffine (fun y => c * f y) := by
    intro y i t
    dsimp only
    rw [hf y i t]
    ring
  apply maximum_from_laws _ hcf
  · intro μ hm
    rw [Law.expect_const_mul]
    apply mul_le_mul_of_nonneg_left _ hc
    apply hmax.2
    exact (mem_cubeGraph_hull_iff f hf x _).mpr ⟨μ, hm, rfl⟩
  · obtain ⟨μ, hm, hv⟩ := (mem_cubeGraph_hull_iff f hf x q).mp hmax.1
    exact ⟨μ, hm, by rw [Law.expect_const_mul, hv]⟩

end
end CubicGap
