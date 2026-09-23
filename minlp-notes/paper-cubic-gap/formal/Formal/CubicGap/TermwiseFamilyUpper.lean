import Formal.CubicGap.TermwiseFamilies
import Formal.CubicGap.TermwiseUpper

/-! Exact sums of individual monomial upper envelopes for the two- and three-group families. -/
namespace CubicGap
noncomputable section

def factorUpper {I : Type*} [Fintype I] [DecidableEq I]
    (s : Finset I) (x : I → ℝ) : ℝ := sSup (envelopeValues (monomial s) x)

theorem factorUpper_group {I J : Type*} [Fintype I] [DecidableEq I]
    (e : J ↪ I) (s : Finset J) (hs : s.Nonempty) (x : I → ℝ) (hx : x ∈ cube I)
    (q : ℝ) (hmean : ∀ j ∈ s, x (e j) = q) : factorUpper (s.map e) x = q := by
  obtain ⟨i,hi⟩ := hs
  rw [← hmean i hi]
  apply IsGreatest.csSup_eq
  apply monomial_maximum_of_min_coordinate _ x hx (e i)
  · exact Finset.mem_map.mpr ⟨i, hi, rfl⟩
  · intro j hj
    obtain ⟨k,hk,rfl⟩ := Finset.mem_map.mp hj
    rw [hmean i hi, hmean k hk]

theorem factorUpper_mixed {I J : Type*} [Fintype I] [DecidableEq I]
    (e : J ↪ I) (s : Finset J) (a : I) (x : I → ℝ) (hx : x ∈ cube I)
    (hmean : ∀ j ∈ s, x a ≤ x (e j)) :
    factorUpper (insert a (s.map e)) x = x a := by
  apply IsGreatest.csSup_eq
  apply monomial_maximum_of_min_coordinate _ x hx a (Finset.mem_insert_self _ _)
  intro j hj
  rcases Finset.mem_insert.mp hj with rfl | hj
  · exact le_rfl
  · obtain ⟨k,hk,rfl⟩ := Finset.mem_map.mp hj
    exact hmean k hk

def termwiseUpperThree (m : ℕ) (coef : Fin 6 → ℚ) : ℝ :=
  (coef 0 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 3,
    factorUpper (s.map (groupEmbedding (2 : Fin 3))) (thresholdThreeMeans m)) +
  (coef 1 : ℝ) * (∑ i : Fin m, ∑ s ∈ Finset.univ.powersetCard 2,
    factorUpper (insert (1,i) (s.map (groupEmbedding (2 : Fin 3)))) (thresholdThreeMeans m)) +
  (coef 2 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 2,
    factorUpper (s.map (groupEmbedding (1 : Fin 3))) (thresholdThreeMeans m)) +
  (coef 3 : ℝ) * (∑ i : Fin m, ∑ j : Fin m,
    factorUpper {(0,i), (2,j)} (thresholdThreeMeans m)) +
  (coef 4 : ℝ) * (∑ i : Fin m, ∑ j : Fin m,
    factorUpper {(0,i), (1,j)} (thresholdThreeMeans m)) +
  (coef 5 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 2,
    factorUpper (s.map (groupEmbedding (0 : Fin 3))) (thresholdThreeMeans m))

def termwiseUpperTwo (m : ℕ) : ℝ :=
  (∑ i : Fin m, ∑ s ∈ Finset.univ.powersetCard 2,
    factorUpper (insert (0,i) (s.map (groupEmbedding (1 : Fin 2)))) (thresholdTwoMeans m)) +
  (5 * (m : ℝ) / 4) * (∑ s ∈ Finset.univ.powersetCard 2,
    factorUpper (s.map (groupEmbedding (0 : Fin 2))) (thresholdTwoMeans m))


theorem three_group_upper (m : ℕ) (g : Fin 3) (s : Finset (Fin m)) (hs : s.Nonempty) :
    factorUpper (s.map (groupEmbedding g)) (thresholdThreeMeans m) =
      if g = 0 then 1 / 4 else if g = 1 then 1 / 2 else 3 / 4 := by
  apply factorUpper_group _ s hs _ (thresholdThreeMeans_mem_cube m)
  intro j _
  rfl

theorem three_bcc_upper (m : ℕ) (i : Fin m) (s : Finset (Fin m)) :
    factorUpper (insert (1,i) (s.map (groupEmbedding (2 : Fin 3))))
      (thresholdThreeMeans m) = 1 / 2 := by
  rw [factorUpper_mixed _ s (1,i) _ (thresholdThreeMeans_mem_cube m)]
  · norm_num [thresholdThreeMeans]
  · intro j _
    change (1:ℝ) / 2 ≤ 3 / 4
    norm_num

theorem three_cross_upper (m : ℕ) (g : Fin 3) (i j : Fin m) :
    factorUpper {(0,i), (g,j)} (thresholdThreeMeans m) = 1 / 4 := by
  have h := monomial_maximum_of_min_coordinate {(0,i),(g,j)} (thresholdThreeMeans m)
    (thresholdThreeMeans_mem_cube m) (0,i) (by simp) (by
      intro k hk
      simp only [Finset.mem_insert, Finset.mem_singleton] at hk
      rcases hk with rfl | rfl
      · exact le_rfl
      · fin_cases g <;> norm_num [thresholdThreeMeans, Fin.ext_iff])
  simpa [factorUpper, thresholdThreeMeans] using h.csSup_eq

theorem two_group_upper (m : ℕ) (s : Finset (Fin m)) (hs : s.Nonempty) :
    factorUpper (s.map (groupEmbedding (0 : Fin 2))) (thresholdTwoMeans m) = 1 / 2 := by
  apply factorUpper_group _ s hs _ (thresholdTwoMeans_mem_cube m)
  intro j _
  rfl

theorem two_acc_upper (m : ℕ) (i : Fin m) (s : Finset (Fin m)) :
    factorUpper (insert (0,i) (s.map (groupEmbedding (1 : Fin 2))))
      (thresholdTwoMeans m) = 1 / 2 := by
  rw [factorUpper_mixed _ s (0,i) _ (thresholdTwoMeans_mem_cube m)]
  · norm_num [thresholdTwoMeans]
  · intro j _
    change (1:ℝ) / 2 ≤ 3 / 4
    norm_num

theorem termwiseUpperThree_eq (m : ℕ) (coef : Fin 6 → ℚ) :
    termwiseUpperThree m coef = (orbitUpper m coef : ℝ) := by
  have hc (g : Fin 3) (d : ℕ) (hd : 0 < d) :
      (∑ s ∈ Finset.univ.powersetCard d,
        factorUpper (s.map (groupEmbedding g)) (thresholdThreeMeans m)) =
      (m.choose d : ℝ) * (if g = 0 then 1 / 4 else if g = 1 then 1 / 2 else 3 / 4) := by
    calc
      _ = ∑ _s ∈ Finset.univ.powersetCard d,
          (if g = 0 then (1:ℝ) / 4 else if g = 1 then 1 / 2 else 3 / 4) := by
        apply Finset.sum_congr rfl
        intro s hs
        apply three_group_upper
        apply Finset.card_pos.mp
        rw [(Finset.mem_powersetCard.mp hs).2]
        exact hd
      _ = _ := by simp [Finset.card_powersetCard]
  simp [termwiseUpperThree, hc 2 3 (by decide), hc 1 2 (by decide), hc 0 2 (by decide),
    three_bcc_upper, three_cross_upper, Finset.card_powersetCard, orbitUpper, Fin.ext_iff]
  ring

theorem termwiseUpperTwo_eq (m : ℕ) : termwiseUpperTwo m = (twoUpper m : ℝ) := by
  have hc : (∑ s ∈ Finset.univ.powersetCard 2,
      factorUpper (s.map (groupEmbedding (0 : Fin 2))) (thresholdTwoMeans m)) =
      (m.choose 2 : ℝ) * (1 / 2) := by
    calc
      _ = ∑ _s ∈ Finset.univ.powersetCard 2, (1:ℝ) / 2 := by
        apply Finset.sum_congr rfl
        intro s hs
        apply two_group_upper
        apply Finset.card_pos.mp
        rw [(Finset.mem_powersetCard.mp hs).2]
        norm_num
      _ = _ := by simp [Finset.card_powersetCard]
  simp [termwiseUpperTwo, hc, two_acc_upper, Finset.card_powersetCard, twoUpper]
  ring

end
end CubicGap
