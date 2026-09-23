import Formal.CubicGap.Polynomial
import Formal.CubicGap.Hull

/-!
# The variable-radix anchor/leaf support family

This module sets up the radix-`b` anchor/leaf family of
`results/positive-multilinear-incidence-sharp-growth.md`: `L` anchor variables
and `b ^ L` leaf variables, the leaves being cut at level `j` into `b ^ (j+1)`
nested equal blocks, with one term for every level and every block of that
level.

It is the radix-`b` counterpart of the radix-2 family in
`Formal/MultilinearGap/Construction.lean`, which is left untouched: every
declaration here lives in the `MultilinearGap.Radix` namespace, so the two
families can be imported together.

Level indices are `j : Fin L` and correspond to the sources' levels `1, …, L`:
level `j` carries `blockCount b L j = b ^ (j+1)` blocks of
`blockSize b L j = b ^ (L - (j+1))` leaves each, and the normalized anchor mean
of level `j` is `1 / blockCount b L j = b ^ -(j+1)`.
-/

namespace MultilinearGap
namespace Radix

noncomputable section
open scoped BigOperators

/-- Coordinates of the radix-`b` family: `L` anchors and `b ^ L` leaves. -/
abbrev Coord (b L : ℕ) := Sum (Fin L) (Fin (b ^ L))

/-- The number of blocks at level `j`, namely `b ^ (j+1)`. -/
def blockCount (b L : ℕ) (j : Fin L) : ℕ := b ^ (j.val + 1)

/-- The number of leaves in a level-`j` block, namely `b ^ (L - (j+1))`. -/
def blockSize (b L : ℕ) (j : Fin L) : ℕ := b ^ (L - (j.val + 1))

/-- The level-`j` blocks partition all `b ^ L` leaves. -/
theorem blockCount_mul_blockSize (b L : ℕ) (j : Fin L) :
    blockCount b L j * blockSize b L j = b ^ L := by
  rw [blockCount, blockSize, ← pow_add, Nat.add_sub_of_le (by omega : j.val + 1 ≤ L)]

/-- The level-`j` identification of a leaf with its (block, offset) pair. -/
def blockEquiv (b L : ℕ) (j : Fin L) :
    Fin (b ^ L) ≃ Fin (blockCount b L j) × Fin (blockSize b L j) :=
  (finCongr (blockCount_mul_blockSize b L j).symm).trans finProdFinEquiv.symm

/-- The level-`j` block index of a leaf is its quotient by the block size. -/
theorem blockEquiv_fst_val (b L : ℕ) (j : Fin L) (i : Fin (b ^ L)) :
    ((blockEquiv b L j i).1 : ℕ) = i.val / blockSize b L j := rfl

/-- A coarse block consists of `b ^ (k-j)` fine blocks in index order. -/
theorem blockSize_eq_mul_of_le (b L : ℕ) (j k : Fin L) (hjk : j ≤ k) :
    blockSize b L j = blockSize b L k * b ^ (k.val - j.val) := by
  rw [blockSize, blockSize, ← pow_add]
  congr 1
  have : j.val ≤ k.val := hjk
  omega

/-- The coarse block index is obtained by dividing the fine block index by
the number of fine blocks in each coarse block. -/
theorem blockEquiv_fst_val_of_le (b L : ℕ) (j k : Fin L) (hjk : j ≤ k)
    (i : Fin (b ^ L)) :
    ((blockEquiv b L j i).1 : ℕ) =
      ((blockEquiv b L k i).1 : ℕ) / b ^ (k.val - j.val) := by
  rw [blockEquiv_fst_val, blockEquiv_fst_val, blockSize_eq_mul_of_le b L j k hjk,
    Nat.div_div_eq_div_mul]

/-- The level-`j` block with index `c`, as a finite set of leaves. -/
def block (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j)) : Finset (Fin (b ^ L)) :=
  Finset.univ.image (fun r => (blockEquiv b L j).symm (c, r))

/-- A leaf lies in the level-`j` block selected by its own level-`j` index. -/
theorem block_mem_iff (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j))
    (i : Fin (b ^ L)) : i ∈ block b L j c ↔ (blockEquiv b L j i).1 = c := by
  simp only [block, Finset.mem_image, Finset.mem_univ, true_and]
  constructor
  · rintro ⟨r, rfl⟩; simp
  · intro h
    refine ⟨(blockEquiv b L j i).2, ?_⟩
    apply (blockEquiv b L j).injective
    simp [← h]

/-- Every level-`j` block has exactly `blockSize b L j` leaves. -/
theorem block_card (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j)) :
    (block b L j c).card = blockSize b L j := by
  rw [block, Finset.card_image_of_injective]
  · simp
  · intro a d h
    exact (Prod.mk.inj ((blockEquiv b L j).symm.injective h)).2

/-- Blocks are nonempty once the radix is positive. -/
theorem block_nonempty (b L : ℕ) (hb : 0 < b) (j : Fin L) (c : Fin (blockCount b L j)) :
    (block b L j c).Nonempty := by
  rw [← Finset.card_pos, block_card]
  exact pow_pos hb _

/-- Fine blocks lie inside the coarse block selected by any one of their leaves. -/
theorem block_subset_of_mem_of_le (b L : ℕ) (j k : Fin L) (hjk : j ≤ k)
    (d : Fin (blockCount b L k)) (i : Fin (b ^ L)) (hi : i ∈ block b L k d) :
    block b L k d ⊆ block b L j (blockEquiv b L j i).1 := by
  intro x hx
  rw [block_mem_iff]
  apply Fin.ext
  rw [blockEquiv_fst_val_of_le b L j k hjk, blockEquiv_fst_val_of_le b L j k hjk,
    (block_mem_iff b L k d x).mp hx, (block_mem_iff b L k d i).mp hi]

/-- The partitions are nested: each fine block lies in exactly one coarse block
when the radix is positive. -/
theorem block_subset_unique (b L : ℕ) (hb : 1 ≤ b) (j k : Fin L) (hjk : j ≤ k)
    (d : Fin (blockCount b L k)) :
    ∃! c : Fin (blockCount b L j), block b L k d ⊆ block b L j c := by
  obtain ⟨i, hi⟩ := block_nonempty b L hb k d
  refine ⟨(blockEquiv b L j i).1, block_subset_of_mem_of_le b L j k hjk d i hi, ?_⟩
  intro c hc
  exact ((block_mem_iff b L j c i).mp (hc hi)).symm

/-- Summing over the level-`j` blocks and then inside each block sums over all leaves. -/
theorem sum_blocks (b L : ℕ) (j : Fin L) (g : Fin (b ^ L) → ℝ) :
    ∑ c, ∑ i ∈ block b L j c, g i = ∑ i, g i := by
  have hinj (c : Fin (blockCount b L j)) : Function.Injective
      (fun r : Fin (blockSize b L j) => (blockEquiv b L j).symm (c, r)) := by
    intro a d h
    exact (Prod.mk.inj ((blockEquiv b L j).symm.injective h)).2
  simp only [block, Finset.sum_image (fun a _ d _ h => hinj _ h)]
  rw [← Fintype.sum_prod_type (f := fun p => g ((blockEquiv b L j).symm p))]
  exact Equiv.sum_comp (blockEquiv b L j).symm g

/-- The support of the term attached to the level-`j` block `c`: its anchor and its leaves. -/
def support (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j)) : Finset (Coord b L) :=
  insert (Sum.inl j) ((block b L j c).image Sum.inr)

@[simp] theorem inl_mem_support (b L : ℕ) (j k : Fin L) (c : Fin (blockCount b L j)) :
    Sum.inl k ∈ support b L j c ↔ k = j := by simp [support]

@[simp] theorem inr_mem_support (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j))
    (i : Fin (b ^ L)) : Sum.inr i ∈ support b L j c ↔ i ∈ block b L j c := by
  simp [support]

/-- Each term has degree `blockSize b L j + 1`. -/
theorem support_card (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j)) :
    (support b L j c).card = blockSize b L j + 1 := by
  rw [support, Finset.card_insert_of_notMem (by simp)]
  rw [Finset.card_image_of_injective _ Sum.inr_injective, block_card]

/-- Distinct (level, block) pairs give distinct supports, so the terms are distinct. -/
theorem support_injective (b L : ℕ) (hb : 0 < b) : Function.Injective
    (fun p : (j : Fin L) × Fin (blockCount b L j) => support b L p.1 p.2) := by
  rintro ⟨j, c⟩ ⟨k, d⟩ h
  change support b L j c = support b L k d at h
  have hj : j = k := (inl_mem_support b L k j d).mp (h ▸ by simp)
  subst k
  have hc : c = d := by
    obtain ⟨i, hi⟩ := block_nonempty b L hb j c
    have hd : i ∈ block b L j d := (inr_mem_support b L j d i).mp (h ▸ by simpa using hi)
    exact ((block_mem_iff b L j c i).mp hi).symm.trans ((block_mem_iff b L j d i).mp hd)
  subst d
  rfl

/-- Removing the anchor from a term leaves exactly its block of leaves. -/
theorem support_erase_anchor_card (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j)) :
    ((support b L j c).erase (Sum.inl j)).card = blockSize b L j := by
  simp only [support, Finset.erase_insert (by simp : Sum.inl j ∉ (block b L j c).image Sum.inr)]
  rw [Finset.card_image_of_injective _ Sum.inr_injective, block_card]

/-- A term factors as its anchor times the product over its block. -/
theorem monomial_support (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j))
    (x : Coord b L → ℝ) :
    CubicGap.monomial (support b L j c) x =
      x (Sum.inl j) * ∏ i ∈ block b L j c, x (Sum.inr i) := by
  simp only [support, CubicGap.monomial,
    Finset.prod_insert (by simp : Sum.inl j ∉ (block b L j c).image Sum.inr)]
  rw [Finset.prod_image]
  exact fun a _ d _ h => Sum.inr_injective h

/-- The radix-`b` family polynomial, with every coefficient one. -/
def polynomial (b L : ℕ) (x : Coord b L → ℝ) : ℝ :=
  ∑ j, ∑ c, CubicGap.monomial (support b L j c) x

/-- The family polynomial is affine in each coordinate separately. -/
theorem polynomial_separatelyAffine (b L : ℕ) :
    CubicGap.SeparatelyAffine (polynomial b L) := by
  intro x i t
  simp only [polynomial, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun c _ => ?_
  exact CubicGap.monomial_coordinate_affine _ _ _ _

/-- The normalized evaluation point: anchor means `b ^ -(j+1)` and leaf means `1 - b ^ -L`. -/
def means (b L : ℕ) : Coord b L → ℝ
  | Sum.inl j => 1 / (blockCount b L j : ℝ)
  | Sum.inr _ => 1 - 1 / (b : ℝ) ^ L

/-- The normalized means lie in the unit cube. -/
theorem means_mem_cube (b L : ℕ) (hb : 1 ≤ b) : means b L ∈ CubicGap.cube (Coord b L) := by
  have hb1 : (1 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb
  intro i
  cases i with
  | inl j =>
    have hp : (1 : ℝ) ≤ (blockCount b L j : ℝ) := by
      exact_mod_cast Nat.one_le_pow (j.val + 1) b hb
    exact ⟨by dsimp [means]; positivity,
      by simpa [means] using (one_div_le_one_div_of_le (by norm_num) hp)⟩
  | inr i =>
    have hp : (1 : ℝ) ≤ (b : ℝ) ^ L := one_le_pow₀ hb1
    have hpos : (0 : ℝ) < (b : ℝ) ^ L := lt_of_lt_of_le zero_lt_one hp
    have hi : 1 / (b : ℝ) ^ L ≤ 1 := by simpa using one_div_le_one_div_of_le (by norm_num) hp
    have hz : 0 < 1 / (b : ℝ) ^ L := by positivity
    exact ⟨by dsimp [means]; linarith, by dsimp [means]; linarith⟩

/-- For radix at least two the normalized means are strictly inside the unit cube. -/
theorem means_strict (b L : ℕ) (hb : 2 ≤ b) (hL : 0 < L) (i : Coord b L) :
    0 < means b L i ∧ means b L i < 1 := by
  have hb1 : (1 : ℝ) < (b : ℝ) := by exact_mod_cast hb
  cases i with
  | inl j =>
    have hp : (1 : ℝ) < (blockCount b L j : ℝ) := by
      simp only [blockCount, Nat.cast_pow]
      exact one_lt_pow₀ hb1 (by omega)
    exact ⟨by dsimp [means]; positivity,
      by simpa [means] using one_div_lt_one_div_of_lt (by norm_num) hp⟩
  | inr i =>
    have hp : (1 : ℝ) < (b : ℝ) ^ L := one_lt_pow₀ hb1 (by omega)
    have hi : 1 / (b : ℝ) ^ L < 1 := by
      simpa using one_div_lt_one_div_of_lt (by norm_num) hp
    have hz : 0 < 1 / (b : ℝ) ^ L := by positivity
    exact ⟨by dsimp [means]; linarith, by dsimp [means]; linarith⟩

end
end Radix
end MultilinearGap
