import Formal.CubicGap.Counts
import Formal.CubicGap.Polynomial

/-! The distinct degree-three supports of the 52-variable homogeneous witness. -/
namespace CubicGap
noncomputable section
open scoped BigOperators

abbrev HomCoord := (Fin 2 × Fin 16) ⊕ Fin 20

def homA : Fin 16 ↪ HomCoord := ⟨fun i => Sum.inl (0, i), by intro i j h; simpa using h⟩
def homC : Fin 16 ↪ HomCoord := ⟨fun i => Sum.inl (1, i), by intro i j h; simpa using h⟩
def homD : Fin 20 ↪ HomCoord := ⟨Sum.inr, Sum.inr_injective⟩

private def mixedSupport {I J K : Type*} [DecidableEq K]
    (a : I ↪ K) (b : J ↪ K) (p : I × Finset J) : Finset K :=
  insert (a p.1) (p.2.map b)

private theorem mixedSupport_injective {I J K : Type*} [DecidableEq K]
    (a : I ↪ K) (b : J ↪ K) (hab : ∀ i j, a i ≠ b j) :
    Function.Injective (mixedSupport a b) := by
  intro p q heq
  have hp : a p.1 ∈ mixedSupport a b q := heq ▸ Finset.mem_insert_self _ _
  have hi : p.1 = q.1 := by
    rcases Finset.mem_insert.mp hp with h | h
    · exact a.injective h
    · obtain ⟨j, _, hj⟩ := Finset.mem_map.mp h
      exact (hab p.1 j hj.symm).elim
  have hs : p.2 = q.2 := by
    apply Finset.map_injective b
    ext k
    have h : k ∈ mixedSupport a b p ↔ k ∈ mixedSupport a b q := by rw [heq]
    by_cases hk : k = a p.1
    · subst k
      simp only [Finset.mem_map]
      constructor <;> rintro ⟨j, _, hj⟩ <;> exact (hab p.1 j hj.symm).elim
    · simpa [mixedSupport, hi, hk, show k ≠ a q.1 by simpa [hi] using hk] using h
  exact Prod.ext hi hs

private def mixedSupports {I J K : Type*} [Fintype I] [Fintype J] [DecidableEq K]
    (a : I ↪ K) (b : J ↪ K) : Finset (Finset K) :=
  (Finset.univ ×ˢ Finset.univ.powersetCard 2).image (mixedSupport a b)

private theorem mixedSupports_card {I J K : Type*} [Fintype I] [Fintype J]
    [DecidableEq K] (a : I ↪ K) (b : J ↪ K) (hab : ∀ i j, a i ≠ b j) :
    (mixedSupports a b).card = Fintype.card I * (Fintype.card J).choose 2 := by
  rw [mixedSupports, Finset.card_image_of_injective _ (mixedSupport_injective a b hab),
    Finset.card_product, Finset.card_univ, Finset.card_powersetCard, Finset.card_univ]

private theorem mixedSupports_degree {I J K : Type*} [Fintype I] [Fintype J]
    [DecidableEq K] (a : I ↪ K) (b : J ↪ K) (hab : ∀ i j, a i ≠ b j)
    {s : Finset K} (hs : s ∈ mixedSupports a b) : s.card = 3 := by
  obtain ⟨⟨i, t⟩, ht, rfl⟩ := Finset.mem_image.mp hs
  have ht2 : t.card = 2 := (Finset.mem_powersetCard.mp (Finset.mem_product.mp ht).2).2
  have hi : a i ∉ t.map b := by
    rintro h
    obtain ⟨j, _, hj⟩ := Finset.mem_map.mp h
    exact hab i j hj.symm
  simp [mixedSupport, Finset.card_insert_of_notMem hi, ht2]

private theorem mixedSupports_polynomial {I J K : Type*} [Fintype I] [Fintype J]
    [DecidableEq K] (a : I ↪ K) (b : J ↪ K) (hab : ∀ i j, a i ≠ b j)
    (x : K → ℝ) :
    supportPolynomial (mixedSupports a b) (fun _ => 1) x =
      (∑ i, x (a i)) * elementary 2 (fun j => x (b j)) := by
  unfold supportPolynomial mixedSupports
  simp only [one_mul]
  rw [Finset.sum_image (fun _ _ _ _ h => mixedSupport_injective a b hab h)]
  rw [Finset.sum_product]
  simp only [monomial, mixedSupport]
  have hi (i : I) (s : Finset J) : a i ∉ s.map b := by
    rintro h
    obtain ⟨j, _, hj⟩ := Finset.mem_map.mp h
    exact hab i j hj.symm
  simp_rw [Finset.prod_insert (hi _ _), Finset.prod_map]
  simp only [elementary, Finset.sum_mul, Finset.mul_sum]
  exact Finset.sum_comm

def homSupportsAC : Finset (Finset HomCoord) := mixedSupports homA homC
def homSupportsDA : Finset (Finset HomCoord) := mixedSupports homD homA
def homSupports : Finset (Finset HomCoord) := homSupportsAC ∪ homSupportsDA

private theorem homAC_disjoint (i j : Fin 16) : homA i ≠ homC j := by
  change Sum.inl ((0 : Fin 2), i) ≠ Sum.inl ((1 : Fin 2), j)
  simp
private theorem homDA_disjoint (i : Fin 20) (j : Fin 16) : homD i ≠ homA j := by
  simp [homD, homA]

theorem homSupports_disjoint : Disjoint homSupportsAC homSupportsDA := by
  apply Finset.disjoint_left.mpr
  intro s hs ht
  obtain ⟨⟨i, t⟩, _, hst⟩ := Finset.mem_image.mp hs
  obtain ⟨⟨k, u⟩, _, hsu⟩ := Finset.mem_image.mp ht
  have hk : homD k ∈ mixedSupport homA homC (i, t) := by
    rw [hst, ← hsu]
    exact Finset.mem_insert_self _ _
  simp only [mixedSupport, Finset.mem_insert, Finset.mem_map] at hk
  rcases hk with h | ⟨j, _, h⟩
  · exact homDA_disjoint k i h
  · simp [homC, homD] at h

theorem homSupports_card : homSupports.card = 4320 := by
  rw [homSupports, Finset.card_union_of_disjoint homSupports_disjoint]
  rw [homSupportsAC, homSupportsDA, mixedSupports_card _ _ homAC_disjoint,
    mixedSupports_card _ _ homDA_disjoint]
  decide

theorem homSupports_degree {s : Finset HomCoord} (hs : s ∈ homSupports) : s.card = 3 := by
  rcases Finset.mem_union.mp hs with h | h
  · exact mixedSupports_degree _ _ homAC_disjoint h
  · exact mixedSupports_degree _ _ homDA_disjoint h

theorem homSupports_polynomial (x : HomCoord → ℝ) :
    supportPolynomial homSupports (fun _ => 1) x =
      (∑ i, x (Sum.inl (0, i))) * elementary 2 (fun i => x (Sum.inl (1, i))) +
      (∑ k, x (Sum.inr k)) * elementary 2 (fun i => x (Sum.inl (0, i))) := by
  unfold supportPolynomial homSupports
  rw [Finset.sum_union homSupports_disjoint]
  exact congrArg₂ (· + ·)
    (mixedSupports_polynomial homA homC homAC_disjoint x)
    (mixedSupports_polynomial homD homA homDA_disjoint x)

theorem homCoord_card : Fintype.card HomCoord = 52 := by decide

private theorem mixedSupport_sum {I J K : Type*} [DecidableEq K]
    (a : I ↪ K) (b : J ↪ K) (hab : ∀ i j, a i ≠ b j)
    (x : K → ℝ) (i : I) (s : Finset J) :
    (∑ j ∈ mixedSupport a b (i,s), x j) = x (a i) + ∑ j ∈ s, x (b j) := by
  have hi : a i ∉ s.map b := by
    rintro h
    obtain ⟨j, _, hj⟩ := Finset.mem_map.mp h
    exact hab i j hj.symm
  simp [mixedSupport, Finset.sum_insert hi]

theorem homSupports_means (x : HomCoord → ℝ)
    (hA : ∀ i, x (homA i) = 1 / 2) (hC : ∀ i, x (homC i) = 3 / 4)
    (hD : ∀ i, x (homD i) = 999 / 1000)
    {s : Finset HomCoord} (hs : s ∈ homSupports) :
    (∀ j ∈ s, (1 / 2 : ℝ) ≤ x j) ∧
      (∃ j ∈ s, x j = (1 / 2 : ℝ)) ∧ (∑ j ∈ s, x j) ≤ 2 := by
  rcases Finset.mem_union.mp hs with hs | hs
  · obtain ⟨⟨i, t⟩, ht, rfl⟩ := Finset.mem_image.mp hs
    have ht2 : t.card = 2 := (Finset.mem_powersetCard.mp (Finset.mem_product.mp ht).2).2
    refine ⟨?_, ⟨homA i, Finset.mem_insert_self _ _, hA i⟩, ?_⟩
    · intro j hj
      rcases Finset.mem_insert.mp hj with rfl | hj
      · rw [hA]
      · obtain ⟨k, _, rfl⟩ := Finset.mem_map.mp hj
        rw [hC]
        norm_num
    · rw [mixedSupport_sum _ _ homAC_disjoint, hA]
      norm_num [hC, ht2]
  · obtain ⟨⟨i, t⟩, ht, rfl⟩ := Finset.mem_image.mp hs
    have ht2 : t.card = 2 := (Finset.mem_powersetCard.mp (Finset.mem_product.mp ht).2).2
    have hne : t.Nonempty := Finset.card_pos.mp (by omega)
    obtain ⟨k, hk⟩ := hne
    refine ⟨?_, ⟨homA k, ?_, hA k⟩, ?_⟩
    · intro j hj
      rcases Finset.mem_insert.mp hj with rfl | hj
      · rw [hD]
        norm_num
      · obtain ⟨k, _, rfl⟩ := Finset.mem_map.mp hj
        rw [hA]
    · exact Finset.mem_insert_of_mem (Finset.mem_map.mpr ⟨k, hk, rfl⟩)
    · rw [mixedSupport_sum _ _ homDA_disjoint, hD]
      norm_num [hA, ht2]

theorem homSupports_nonempty {s : Finset HomCoord} (hs : s ∈ homSupports) : s.Nonempty :=
  Finset.card_pos.mp (by rw [homSupports_degree hs]; norm_num)

theorem homSupports_minimum (x : HomCoord → ℝ)
    (hA : ∀ i, x (homA i) = 1 / 2) (hC : ∀ i, x (homC i) = 3 / 4)
    (hD : ∀ i, x (homD i) = 999 / 1000)
    {s : Finset HomCoord} (hs : s ∈ homSupports) :
    s.inf' (homSupports_nonempty hs) x = 1 / 2 := by
  obtain ⟨hle, ⟨j, hj, heq⟩, _⟩ := homSupports_means x hA hC hD hs
  apply le_antisymm
  · rw [← heq]
    exact Finset.inf'_le _ hj
  · exact Finset.le_inf' _ _ hle

theorem homSupports_upper_total (x : HomCoord → ℝ)
    (hA : ∀ i, x (homA i) = 1 / 2) (hC : ∀ i, x (homC i) = 3 / 4)
    (hD : ∀ i, x (homD i) = 999 / 1000) :
    (∑ s ∈ homSupports.attach, s.val.inf' (homSupports_nonempty s.property) x) = 2160 := by
  have h : (∑ s ∈ homSupports.attach, s.val.inf' (homSupports_nonempty s.property) x) =
      ∑ _s ∈ homSupports.attach, (1 / 2 : ℝ) := by
    apply Finset.sum_congr rfl
    intro s _
    exact homSupports_minimum x hA hC hD s.property
  rw [h]
  norm_num [homSupports_card]

theorem homSupports_lower_total (x : HomCoord → ℝ)
    (hA : ∀ i, x (homA i) = 1 / 2) (hC : ∀ i, x (homC i) = 3 / 4)
    (hD : ∀ i, x (homD i) = 999 / 1000) :
    (∑ s ∈ homSupports, max (0 : ℝ) ((∑ j ∈ s, x j) - (s.card - 1))) = 0 := by
  apply Finset.sum_eq_zero
  intro s hs
  have hb := (homSupports_means x hA hC hD hs).2.2
  rw [homSupports_degree hs]
  norm_num only [Nat.cast_ofNat]
  apply max_eq_left
  linarith

end
end CubicGap
