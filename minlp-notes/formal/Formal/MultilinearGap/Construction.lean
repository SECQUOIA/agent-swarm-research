import Formal.CubicGap.Polynomial
import Formal.CubicGap.Hull

/-! A dyadic family of positive squarefree polynomials. -/
namespace MultilinearGap
noncomputable section
open scoped BigOperators

abbrev Coord (L : ℕ) := Sum (Fin L) (Fin (2 ^ L))
def blockCount (L : ℕ) (j : Fin L) : ℕ := 2 ^ (j.val + 1)
def blockSize (L : ℕ) (j : Fin L) : ℕ := 2 ^ (L - (j.val + 1))

theorem blockCount_mul_blockSize (L : ℕ) (j : Fin L) :
    blockCount L j * blockSize L j = 2 ^ L := by
  rw [blockCount, blockSize, ← pow_add, Nat.add_sub_of_le (by omega : j.val + 1 ≤ L)]

def blockEquiv (L : ℕ) (j : Fin L) :
    Fin (2 ^ L) ≃ Fin (blockCount L j) × Fin (blockSize L j) :=
  (finCongr (blockCount_mul_blockSize L j).symm).trans finProdFinEquiv.symm

def block (L : ℕ) (j : Fin L) (b : Fin (blockCount L j)) : Finset (Fin (2 ^ L)) :=
  Finset.univ.image (fun r => (blockEquiv L j).symm (b, r))

theorem block_mem_iff (L : ℕ) (j : Fin L) (b : Fin (blockCount L j))
    (i : Fin (2 ^ L)) : i ∈ block L j b ↔ (blockEquiv L j i).1 = b := by
  simp only [block, Finset.mem_image, Finset.mem_univ, true_and]
  constructor
  · rintro ⟨r, rfl⟩; simp
  · intro h
    refine ⟨(blockEquiv L j i).2, ?_⟩
    apply (blockEquiv L j).injective
    simp [← h]

theorem block_card (L : ℕ) (j : Fin L) (b : Fin (blockCount L j)) :
    (block L j b).card = blockSize L j := by
  rw [block, Finset.card_image_of_injective]
  · simp
  · intro a c h
    exact (Prod.mk.inj ((blockEquiv L j).symm.injective h)).2

theorem block_nonempty (L : ℕ) (j : Fin L) (b : Fin (blockCount L j)) :
    (block L j b).Nonempty := by
  rw [← Finset.card_pos, block_card]
  exact pow_pos (by decide) _

theorem sum_blocks (L : ℕ) (j : Fin L) (g : Fin (2 ^ L) → ℝ) :
    ∑ b, ∑ i ∈ block L j b, g i = ∑ i, g i := by
  have hinj (b : Fin (blockCount L j)) : Function.Injective
      (fun r : Fin (blockSize L j) => (blockEquiv L j).symm (b,r)) := by
    intro a c h
    exact (Prod.mk.inj ((blockEquiv L j).symm.injective h)).2
  simp only [block, Finset.sum_image (fun a _ b _ h => hinj _ h)]
  rw [← Fintype.sum_prod_type (f := fun p => g ((blockEquiv L j).symm p))]
  exact Equiv.sum_comp (blockEquiv L j).symm g

def support (L : ℕ) (j : Fin L) (b : Fin (blockCount L j)) : Finset (Coord L) :=
  insert (Sum.inl j) ((block L j b).image Sum.inr)

@[simp] theorem inl_mem_support (L : ℕ) (j k : Fin L) (b : Fin (blockCount L j)) :
    Sum.inl k ∈ support L j b ↔ k = j := by simp [support]

@[simp] theorem inr_mem_support (L : ℕ) (j : Fin L) (b : Fin (blockCount L j))
    (i : Fin (2 ^ L)) : Sum.inr i ∈ support L j b ↔ i ∈ block L j b := by
  simp [support]

theorem support_card (L : ℕ) (j : Fin L) (b : Fin (blockCount L j)) :
    (support L j b).card = blockSize L j + 1 := by
  rw [support, Finset.card_insert_of_notMem (by simp)]
  rw [Finset.card_image_of_injective _ Sum.inr_injective, block_card]

theorem support_injective (L : ℕ) : Function.Injective
    (fun p : (j : Fin L) × Fin (blockCount L j) => support L p.1 p.2) := by
  rintro ⟨j,b⟩ ⟨k,c⟩ h
  change support L j b = support L k c at h
  have hj : j = k := (inl_mem_support L k j c).mp (h ▸ by simp)
  subst k
  have hb : b = c := by
    obtain ⟨i, hi⟩ := block_nonempty L j b
    have hc : i ∈ block L j c := (inr_mem_support L j c i).mp (h ▸ by simpa using hi)
    exact ((block_mem_iff L j b i).mp hi).symm.trans ((block_mem_iff L j c i).mp hc)
  subst c
  rfl

def polynomial (L : ℕ) (x : Coord L → ℝ) : ℝ :=
  ∑ j, ∑ b, CubicGap.monomial (support L j b) x

theorem polynomial_separatelyAffine (L : ℕ) : CubicGap.SeparatelyAffine (polynomial L) := by
  intro x i t
  simp only [polynomial, Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro b _
  exact CubicGap.monomial_coordinate_affine _ _ _ _

def means (L : ℕ) : Coord L → ℝ
  | Sum.inl j => 1 / (blockCount L j : ℝ)
  | Sum.inr _ => 1 - 1 / (2 : ℝ)^L

def failureCount (L : ℕ) (v : CubicGap.Vertex (Coord L)) : ℝ :=
  ∑ i : Fin (2^L), (1 - CubicGap.vertexPoint v (Sum.inr i))

theorem means_mem_cube (L : ℕ) : means L ∈ CubicGap.cube (Coord L) := by
  intro i
  cases i with
  | inl j =>
    have hp : (1 : ℝ) ≤ (blockCount L j : ℝ) := by
      exact_mod_cast (Nat.one_le_pow (j.val+1) 2 (by decide))
    exact ⟨by dsimp [means]; positivity,
      by simpa [means] using (one_div_le_one_div_of_le (by norm_num) hp)⟩
  | inr i =>
    have hp : (1 : ℝ) ≤ (2 : ℝ)^L := one_le_pow₀ (by norm_num)
    have hi : 1 / (2 : ℝ)^L ≤ 1 := by simpa using one_div_le_one_div_of_le (by norm_num) hp
    constructor <;> dsimp [means]
    · linarith
    · have : 0 ≤ 1 / (2 : ℝ)^L := by positivity
      linarith

/-- The counterexample uses a point strictly inside the unit cube. -/
theorem means_strict (L : ℕ) (hL : 0 < L) (i : Coord L) :
    0 < means L i ∧ means L i < 1 := by
  cases i with
  | inl j =>
    have hp : (1 : ℝ) < (blockCount L j : ℝ) := by
      simp only [blockCount, Nat.cast_pow, Nat.cast_ofNat]
      exact one_lt_pow₀ (by norm_num) (by omega)
    constructor
    · dsimp [means]; positivity
    · simpa [means] using one_div_lt_one_div_of_lt (by norm_num) hp
  | inr i =>
    have hp : (1 : ℝ) < (2 : ℝ)^L := one_lt_pow₀ (by norm_num) (by omega)
    have hi : 1 / (2 : ℝ)^L < 1 := by
      simpa using one_div_lt_one_div_of_lt (by norm_num) hp
    have hz : 0 < 1 / (2 : ℝ)^L := by positivity
    dsimp [means]
    constructor <;> linarith

theorem monomial_support (L : ℕ) (j : Fin L) (b : Fin (blockCount L j))
    (x : Coord L → ℝ) :
    CubicGap.monomial (support L j b) x =
      x (Sum.inl j) * ∏ i ∈ block L j b, x (Sum.inr i) := by
  simp only [support, CubicGap.monomial,
    Finset.prod_insert (by simp : Sum.inl j ∉ (block L j b).image Sum.inr)]
  rw [Finset.prod_image]
  exact fun a _ b _ h => Sum.inr_injective h

theorem support_erase_anchor_card (L : ℕ) (j : Fin L) (b : Fin (blockCount L j)) :
    ((support L j b).erase (Sum.inl j)).card = blockSize L j := by
  simp only [support, Finset.erase_insert (by simp : Sum.inl j ∉ (block L j b).image Sum.inr)]
  rw [Finset.card_image_of_injective _ Sum.inr_injective, block_card]

theorem vertexPoint_mem_cube (L : ℕ) (v : CubicGap.Vertex (Coord L)) :
    CubicGap.vertexPoint v ∈ CubicGap.cube (Coord L) := by
  intro i
  simp only [CubicGap.vertexPoint]
  split <;> norm_num

theorem failureCount_nonneg (L : ℕ) (v : CubicGap.Vertex (Coord L)) :
    0 ≤ failureCount L v := by
  exact Finset.sum_nonneg (fun i _ => sub_nonneg.mpr ((vertexPoint_mem_cube L v (Sum.inr i)).2))

/-- At one level, every failed leaf can destroy at most one block. -/
theorem level_lower_bound (L : ℕ) (j : Fin L) (v : CubicGap.Vertex (Coord L)) :
    CubicGap.vertexPoint v (Sum.inl j) *
        ((blockCount L j : ℝ) - min (blockCount L j : ℝ) (failureCount L v)) ≤
      ∑ b, CubicGap.monomial (support L j b) (CubicGap.vertexPoint v) := by
  let x := CubicGap.vertexPoint v
  let P := fun b : Fin (blockCount L j) => ∏ i ∈ block L j b, x (Sum.inr i)
  let D : ℝ := ∑ b, (1 - P b)
  have hx : x ∈ CubicGap.cube (Coord L) := vertexPoint_mem_cube L v
  have hP (b : Fin (blockCount L j)) : 0 ≤ P b :=
    Finset.prod_nonneg (fun i _ => (hx (Sum.inr i)).1)
  have hDb : D ≤ (blockCount L j : ℝ) := by
    calc
      D ≤ ∑ _b : Fin (blockCount L j), (1 : ℝ) :=
        Finset.sum_le_sum (fun b _ => by linarith [hP b])
      _ = _ := by simp
  have hDr : D ≤ failureCount L v := by
    calc
      D ≤ ∑ b, ∑ i ∈ block L j b, (1 - x (Sum.inr i)) := by
        apply Finset.sum_le_sum
        intro b _
        have h := CubicGap.monomial_lower (block L j b) (x := fun i => x (Sum.inr i))
          (fun i _ => hx (Sum.inr i))
        simp only [Finset.sum_sub_distrib, Finset.sum_const, nsmul_eq_mul, mul_one]
        dsimp [P, CubicGap.monomial] at *
        linarith
      _ = failureCount L v := sum_blocks L j _
  have hD : D ≤ min (blockCount L j : ℝ) (failureCount L v) := le_min hDb hDr
  calc
    _ ≤ x (Sum.inl j) * ((blockCount L j : ℝ) - D) :=
      mul_le_mul_of_nonneg_left (by linarith) (hx (Sum.inl j)).1
    _ = ∑ b, CubicGap.monomial (support L j b) x := by
      simp only [monomial_support, ← Finset.mul_sum]
      congr 1
      simp [D, Finset.sum_sub_distrib, P]

theorem polynomial_lower_bound (L : ℕ) (v : CubicGap.Vertex (Coord L)) :
    (∑ j, CubicGap.vertexPoint v (Sum.inl j) *
        ((blockCount L j : ℝ) - min (blockCount L j : ℝ) (failureCount L v))) ≤
      polynomial L (CubicGap.vertexPoint v) := by
  exact Finset.sum_le_sum (fun j _ => level_lower_bound L j v)

end
end MultilinearGap
