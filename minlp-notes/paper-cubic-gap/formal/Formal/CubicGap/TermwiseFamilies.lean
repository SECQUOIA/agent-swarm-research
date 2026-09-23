import Formal.CubicGap.Termwise
import Formal.CubicGap.Threshold

/-! Exact sums of the individual monomial lower envelopes in the displayed families. -/
namespace CubicGap
noncomputable section

/-- A factor's exact lower envelope on the full ambient cube. -/
def factorLower {I : Type*} [Fintype I] [DecidableEq I]
    (s : Finset I) (x : I → ℝ) : ℝ := sInf (envelopeValues (monomial s) x)

def groupEmbedding {k m : ℕ} (g : Fin k) : Fin m ↪ (Fin k × Fin m) :=
  ⟨fun i => (g, i), by intro i j h; exact congrArg Prod.snd h⟩

theorem factorLower_pair {I : Type*} [Fintype I] [DecidableEq I]
    (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (i j : I) (hij : i ≠ j) (hi : i ∈ s) (hj : j ∈ s)
    (hab : x i + x j ≤ 1) : factorLower s x = 0 :=
  (monomial_minimum_zero_of_pair s x hx i j hij hi hj hab).csInf_eq

theorem thresholdTwoMeans_mem_cube (m : ℕ) : thresholdTwoMeans m ∈ cube (Fin 2 × Fin m) := by
  intro i
  simp only [thresholdTwoMeans]
  split <;> norm_num

theorem thresholdThreeMeans_mem_cube (m : ℕ) : thresholdThreeMeans m ∈ cube (Fin 3 × Fin m) := by
  intro i
  simp only [thresholdThreeMeans]
  split <;> (try split) <;> norm_num

/-- The six sums follow the actual monomial expansions of `threeFamily`. -/
def termwiseLowerThree (m : ℕ) (coef : Fin 6 → ℚ) : ℝ :=
  (coef 0 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 3,
    factorLower (s.map (groupEmbedding (2 : Fin 3))) (thresholdThreeMeans m)) +
  (coef 1 : ℝ) * (∑ i : Fin m, ∑ s ∈ Finset.univ.powersetCard 2,
    factorLower (insert (1,i) (s.map (groupEmbedding (2 : Fin 3)))) (thresholdThreeMeans m)) +
  (coef 2 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 2,
    factorLower (s.map (groupEmbedding (1 : Fin 3))) (thresholdThreeMeans m)) +
  (coef 3 : ℝ) * (∑ i : Fin m, ∑ j : Fin m,
    factorLower {(0,i), (2,j)} (thresholdThreeMeans m)) +
  (coef 4 : ℝ) * (∑ i : Fin m, ∑ j : Fin m,
    factorLower {(0,i), (1,j)} (thresholdThreeMeans m)) +
  (coef 5 : ℝ) * (∑ s ∈ Finset.univ.powersetCard 2,
    factorLower (s.map (groupEmbedding (0 : Fin 3))) (thresholdThreeMeans m))

def termwiseLowerTwo (m : ℕ) : ℝ :=
  (∑ i : Fin m, ∑ s ∈ Finset.univ.powersetCard 2,
    factorLower (insert (0,i) (s.map (groupEmbedding (1 : Fin 2)))) (thresholdTwoMeans m)) +
  (5 * (m : ℝ) / 4) * (∑ s ∈ Finset.univ.powersetCard 2,
    factorLower (s.map (groupEmbedding (0 : Fin 2))) (thresholdTwoMeans m))


theorem factorLower_pair_map {I J : Type*} [Fintype I] [DecidableEq I]
    (e : J ↪ I) (s : Finset J) (hs : s.card = 2)
    (x : I → ℝ) (hx : x ∈ cube I) (hmean : ∀ j ∈ s, x (e j) ≤ 1 / 2) :
    factorLower (s.map e) x = 0 := by
  classical
  obtain ⟨i, j, hij, rfl⟩ := Finset.card_eq_two.mp hs
  apply factorLower_pair _ x hx (e i) (e j) (e.injective.ne hij)
  · simp
  · simp
  · have hi := hmean i (by simp)
    have hj := hmean j (by simp)
    linarith

theorem three_pair_lower (m : ℕ) (g : Fin 3) (hg : g ≠ 2)
    (s : Finset (Fin m)) (hs : s.card = 2) :
    factorLower (s.map (groupEmbedding g)) (thresholdThreeMeans m) = 0 := by
  apply factorLower_pair_map _ s hs _ (thresholdThreeMeans_mem_cube m)
  intro j _
  change (if g = 0 then (1:ℝ) / 4 else if g = 1 then 1 / 2 else 3 / 4) ≤ 1 / 2
  fin_cases g <;> norm_num [Fin.ext_iff] at *

theorem three_cross_lower (m : ℕ) (g : Fin 3) (hg : g ≠ 0) (i j : Fin m) :
    factorLower {(0,i), (g,j)} (thresholdThreeMeans m) = 0 := by
  apply factorLower_pair _ _ (thresholdThreeMeans_mem_cube m) (0,i) (g,j)
  · intro h
    exact hg (congrArg Prod.fst h).symm
  · simp
  · simp
  · fin_cases g <;> norm_num [thresholdThreeMeans, Fin.ext_iff] at *

theorem two_pair_lower (m : ℕ) (s : Finset (Fin m)) (hs : s.card = 2) :
    factorLower (s.map (groupEmbedding (0 : Fin 2))) (thresholdTwoMeans m) = 0 := by
  apply factorLower_pair_map _ s hs _ (thresholdTwoMeans_mem_cube m)
  intro j _
  change (1:ℝ) / 2 ≤ 1 / 2
  rfl


theorem factorLower_triple {I : Type*} [Fintype I] [DecidableEq I]
    (x : I → ℝ) (hx : x ∈ cube I) (i j k : I)
    (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k)
    (hsum : 2 ≤ x i + x j + x k) :
    factorLower {i,j,k} x = x i + x j + x k - 2 :=
  (triple_monomial_minimum x hx i j k hij hik hjk hsum).csInf_eq

theorem three_ccc_lower (m : ℕ) (s : Finset (Fin m)) (hs : s.card = 3) :
    factorLower (s.map (groupEmbedding (2 : Fin 3))) (thresholdThreeMeans m) = 1 / 4 := by
  obtain ⟨i,j,k,hij,hik,hjk,rfl⟩ := Finset.card_eq_three.mp hs
  simp only [Finset.map_insert, Finset.map_singleton]
  change factorLower {(2,i),(2,j),(2,k)} (thresholdThreeMeans m) = 1 / 4
  rw [factorLower_triple _ (thresholdThreeMeans_mem_cube m)
    (2,i) (2,j) (2,k) (by simpa using hij) (by simpa using hik)
    (by simpa using hjk) (by norm_num [thresholdThreeMeans, Fin.ext_iff])]
  norm_num [thresholdThreeMeans, Fin.ext_iff]

theorem three_bcc_lower (m : ℕ) (i : Fin m) (s : Finset (Fin m)) (hs : s.card = 2) :
    factorLower (insert (1,i) (s.map (groupEmbedding (2 : Fin 3))))
      (thresholdThreeMeans m) = 0 := by
  obtain ⟨j,k,hjk,rfl⟩ := Finset.card_eq_two.mp hs
  simp only [Finset.map_insert, Finset.map_singleton]
  change factorLower {(1,i),(2,j),(2,k)} (thresholdThreeMeans m) = 0
  rw [factorLower_triple _ (thresholdThreeMeans_mem_cube m)
    (1,i) (2,j) (2,k) (by simp) (by simp)
    (by simpa using hjk) (by norm_num [thresholdThreeMeans, Fin.ext_iff])]
  norm_num [thresholdThreeMeans, Fin.ext_iff]

theorem two_acc_lower (m : ℕ) (i : Fin m) (s : Finset (Fin m)) (hs : s.card = 2) :
    factorLower (insert (0,i) (s.map (groupEmbedding (1 : Fin 2))))
      (thresholdTwoMeans m) = 0 := by
  obtain ⟨j,k,hjk,rfl⟩ := Finset.card_eq_two.mp hs
  simp only [Finset.map_insert, Finset.map_singleton]
  change factorLower {(0,i),(1,j),(1,k)} (thresholdTwoMeans m) = 0
  rw [factorLower_triple _ (thresholdTwoMeans_mem_cube m)
    (0,i) (1,j) (1,k) (by simp) (by simp)
    (by simpa using hjk) (by norm_num [thresholdTwoMeans])]
  norm_num [thresholdTwoMeans]

/-- The termwise relaxation has the manuscript's lower endpoint, using actual
exact lower envelopes of every individual factor. -/
theorem termwiseLowerThree_eq (m : ℕ) (coef : Fin 6 → ℚ) :
    termwiseLowerThree m coef = (orbitLower m coef : ℝ) := by
  have hc (s : Finset (Fin m)) (hs : s ∈ Finset.univ.powersetCard 3) :=
    three_ccc_lower m s (Finset.mem_powersetCard.mp hs).2
  have hb (i : Fin m) (s : Finset (Fin m)) (hs : s ∈ Finset.univ.powersetCard 2) :=
    three_bcc_lower m i s (Finset.mem_powersetCard.mp hs).2
  have hp (g : Fin 3) (hg : g ≠ 2) (s : Finset (Fin m))
      (hs : s ∈ Finset.univ.powersetCard 2) :=
    three_pair_lower m g hg s (Finset.mem_powersetCard.mp hs).2
  simp only [termwiseLowerThree]
  simp_rw [Finset.sum_congr rfl hc]
  have hb' (i : Fin m) : (∑ s ∈ Finset.univ.powersetCard 2,
      factorLower (insert (1,i) (s.map (groupEmbedding (2 : Fin 3))))
        (thresholdThreeMeans m)) = 0 := Finset.sum_eq_zero (hb i)
  have hp' (g : Fin 3) (hg : g ≠ 2) : (∑ s ∈ Finset.univ.powersetCard 2,
      factorLower (s.map (groupEmbedding g)) (thresholdThreeMeans m)) = 0 :=
    Finset.sum_eq_zero (hp g hg)
  simp [hb', hp' 0 (by decide), hp' 1 (by decide), three_cross_lower m 2 (by decide),
    three_cross_lower m 1 (by decide), Finset.card_powersetCard, orbitLower]
  ring

theorem termwiseLowerTwo_eq (m : ℕ) : termwiseLowerTwo m = 0 := by
  have ha (i : Fin m) : (∑ s ∈ Finset.univ.powersetCard 2,
      factorLower (insert (0,i) (s.map (groupEmbedding (1 : Fin 2))))
        (thresholdTwoMeans m)) = 0 := by
    apply Finset.sum_eq_zero
    intro s hs
    exact two_acc_lower m i s (Finset.mem_powersetCard.mp hs).2
  have hp : (∑ s ∈ Finset.univ.powersetCard 2,
      factorLower (s.map (groupEmbedding (0 : Fin 2))) (thresholdTwoMeans m)) = 0 := by
    apply Finset.sum_eq_zero
    intro s hs
    exact two_pair_lower m s (Finset.mem_powersetCard.mp hs).2
  simp [termwiseLowerTwo, ha, hp]

end
end CubicGap
