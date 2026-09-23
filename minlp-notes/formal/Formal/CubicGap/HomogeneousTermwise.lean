import Formal.CubicGap.HomogeneousSupports
import Formal.CubicGap.Termwise

/-! Exact individual monomial lower envelopes for the homogeneous witness. -/
namespace CubicGap
noncomputable section

/-- Every monomial has an attaining zero-valued graph-hull point at these means. -/
theorem homSupports_exact_lower (x : HomCoord → ℝ) (hx : x ∈ cube HomCoord)
    (hA : ∀ i, x (homA i) = 1 / 2) (hC : ∀ i, x (homC i) = 3 / 4)
    {s : Finset HomCoord} (hs : s ∈ homSupports) :
    IsLeast (envelopeValues (monomial s) x) 0 := by
  rcases Finset.mem_union.mp hs with hs | hs
  · change s ∈ (Finset.univ ×ˢ Finset.univ.powersetCard 2).image
      (fun p : Fin 16 × Finset (Fin 16) => insert (homA p.1) (p.2.map homC)) at hs
    obtain ⟨⟨i, t⟩, ht, rfl⟩ := Finset.mem_image.mp hs
    have ht2 : t.card = 2 := (Finset.mem_powersetCard.mp (Finset.mem_product.mp ht).2).2
    obtain ⟨j, k, hjk, rfl⟩ := Finset.card_eq_two.mp ht2
    have hij : homA i ≠ homC j := by
      change Sum.inl ((0 : Fin 2), i) ≠ Sum.inl ((1 : Fin 2), j)
      simp
    have hik : homA i ≠ homC k := by
      change Sum.inl ((0 : Fin 2), i) ≠ Sum.inl ((1 : Fin 2), k)
      simp
    have hjk' : homC j ≠ homC k := fun h => hjk (homC.injective h)
    have h := triple_monomial_minimum x hx (homA i) (homC j) (homC k)
      hij hik hjk' (by rw [hA, hC, hC]; norm_num)
    norm_num [hA, hC] at h
    simpa only [Finset.map_insert, Finset.map_singleton] using h
  · change s ∈ (Finset.univ ×ˢ Finset.univ.powersetCard 2).image
      (fun p : Fin 20 × Finset (Fin 16) => insert (homD p.1) (p.2.map homA)) at hs
    obtain ⟨⟨i, t⟩, ht, rfl⟩ := Finset.mem_image.mp hs
    have ht2 : t.card = 2 := (Finset.mem_powersetCard.mp (Finset.mem_product.mp ht).2).2
    obtain ⟨j, k, hjk, rfl⟩ := Finset.card_eq_two.mp ht2
    apply monomial_minimum_zero_of_pair _ x hx (homA j) (homA k)
      (fun h => hjk (homA.injective h))
    · simp
    · simp
    · rw [hA, hA]
      norm_num

end
end CubicGap
