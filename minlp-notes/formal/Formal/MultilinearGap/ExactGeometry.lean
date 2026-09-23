import Formal.MultilinearGap.Construction
import Formal.MultilinearGap.ResidueSums

/-! Equally spaced leaf failures attain the block-count bound at every dyadic level. -/
namespace MultilinearGap
noncomputable section
open scoped BigOperators

private theorem block_mod (S q b r : ℕ) (_hS : 0 < S) (hq : 0 < q) (hr : r < S) :
    (b * S + r) % (q * S) = (b % q) * S + r := by
  have hmul : (b % q + 1) * S ≤ q * S := Nat.mul_le_mul_right S (Nat.mod_lt b hq)
  have hbound : b % q * S + r < q * S := by nlinarith
  rw [Nat.add_mod, Nat.mul_mod_mul_right, Nat.mod_eq_of_lt (by nlinarith : r < q * S),
    Nat.mod_eq_of_lt hbound]

private theorem block_product_residue (S q b t : ℕ) (hS : 0 < S) (hq : 0 < q)
    (_ht : t < q * S) :
    (∏ r : Fin S, if (b * S+r.val) % (q * S) = t then (0 : ℝ) else 1) =
      if b % q = t / S then 0 else 1 := by
  by_cases h : b % q = t / S
  · rw [if_pos h]
    apply Finset.prod_eq_zero (i := ⟨t % S, Nat.mod_lt t hS⟩) (Finset.mem_univ _)
    rw [block_mod S q b _ hS hq (Nat.mod_lt t hS), h]
    simp [Nat.mul_comm, Nat.div_add_mod]
  · rw [if_neg h]
    apply Finset.prod_eq_one
    intro r _
    rw [if_neg]
    intro heq
    rw [block_mod S q b r.val hS hq r.isLt] at heq
    have hh := congrArg (fun z => z / S) heq
    rw [Nat.mul_comm (b % q), Nat.mul_add_div hS, Nat.div_eq_of_lt r.isLt, Nat.add_zero] at hh
    exact h hh

/-- A periodic pattern with `2 ^ r` failures; the offset randomizes the leaf marginals. -/
def spacedLeaf (L r : ℕ) (t : Fin (2 ^ (L - r))) (i : Fin (2 ^ L)) : Bool :=
  decide (i.val % 2 ^ (L - r) ≠ t.val)

@[simp] theorem spacedLeaf_point (L r : ℕ) (t : Fin (2 ^ (L - r))) (i : Fin (2 ^ L)) :
    CubicGap.vertexPoint (spacedLeaf L r t) i =
      if i.val % 2 ^ (L - r) = t.val then 0 else 1 := by
  simp only [CubicGap.vertexPoint, spacedLeaf, decide_eq_true_eq]
  split_ifs <;> simp_all

private theorem blockEquiv_symm_val (L : ℕ) (j : Fin L)
    (b : Fin (blockCount L j)) (r : Fin (blockSize L j)) :
    ((blockEquiv L j).symm (b,r)).val = b.val * blockSize L j + r.val := by
  simp [blockEquiv, finProdFinEquiv, Nat.add_comm, Nat.mul_comm]

theorem spacedLeaf_block_product (L r : ℕ) (j : Fin L) (t : Fin (2 ^ (L - r)))
    (b : Fin (blockCount L j)) :
    (∏ i ∈ block L j b, CubicGap.vertexPoint (spacedLeaf L r t) i) =
      ∏ k : Fin (blockSize L j),
        if (b.val * blockSize L j + k.val) % 2 ^ (L - r) = t.val then (0 : ℝ) else 1 := by
  rw [block, Finset.prod_image]
  · simp [blockEquiv_symm_val]
  · intro a _ c _ h
    exact (Prod.mk.inj ((blockEquiv L j).symm.injective h)).2

/-- Each translated pattern contains exactly the prescribed number of failures. -/
theorem spacedLeaf_failure_count (L r : ℕ) (hr : r ≤ L) (t : Fin (2 ^ (L - r))) :
    (∑ i : Fin (2 ^ L), (1 - CubicGap.vertexPoint (spacedLeaf L r t) i)) =
      (2 : ℝ)^r := by
  simp only [spacedLeaf_point, sub_ite, sub_zero, sub_self]
  have hN : 2 ^ L = 2 ^ r * 2 ^ (L - r) := by
    rw [← pow_add, Nat.add_sub_of_le hr]
  rw [hN]
  simpa only [Nat.cast_pow, Nat.cast_ofNat] using sum_residue_indicator (2 ^ r) (2 ^ (L - r)) t

/-- Every leaf has the same failure probability under a uniform offset. -/
theorem spacedLeaf_mean (L r : ℕ) (hr : r ≤ L) (i : Fin (2 ^ L)) :
    (CubicGap.Law.uniform (Fin (2 ^ (L - r)))).expect
      (fun t => CubicGap.vertexPoint (spacedLeaf L r t) i) =
      1 - (2 : ℝ)^r / (2 : ℝ)^L := by
  have hd : 0 < 2 ^ (L - r) := by positivity
  let u : Fin (2 ^ (L - r)) := ⟨i.val % 2 ^ (L - r), Nat.mod_lt _ hd⟩
  have heq (t : Fin (2 ^ (L - r))) : i.val % 2 ^ (L - r) = t.val ↔ t = u := by
    simp [u, Fin.ext_iff, eq_comm]
  rw [CubicGap.Law.expect_uniform]
  simp only [spacedLeaf_point, heq, Fintype.card_fin]
  have hs : (∑ t : Fin (2 ^ (L - r)), if t = u then (0 : ℝ) else 1) =
      (2 ^ (L - r) : ℕ) - 1 := by
    classical
    have hpoint (t : Fin (2 ^ (L - r))) :
        (if t = u then (0 : ℝ) else 1) = 1 - (if t = u then 1 else 0) := by
      split_ifs <;> norm_num
    simp [hpoint, Finset.sum_sub_distrib]
  rw [hs]
  have hp : (2 : ℝ)^(L - r) * (2 : ℝ)^r = (2 : ℝ)^L := by
    rw [← pow_add, Nat.sub_add_cancel hr]
  push_cast
  field_simp
  nlinarith [hp]

/-- Every periodic pattern attains the maximum number of hit blocks at every level. -/
theorem spacedLeaf_level_sum (L r : ℕ) (hr : r ≤ L) (j : Fin L)
    (t : Fin (2 ^ (L - r))) :
    (∑ b : Fin (blockCount L j),
      ∏ i ∈ block L j b, CubicGap.vertexPoint (spacedLeaf L r t) i) =
      (blockCount L j : ℝ) - min (blockCount L j : ℝ) ((2 : ℝ)^r) := by
  simp only [spacedLeaf_block_product]
  by_cases hj : j.val + 1 ≤ r
  · have hdiv : 2 ^ (L - r) ∣ blockSize L j :=
      Nat.pow_dvd_pow 2 (by omega)
    have hz (b : Fin (blockCount L j)) :
        (∏ k : Fin (blockSize L j),
          if (b.val * blockSize L j + k.val) % 2 ^ (L - r) = t.val then (0 : ℝ) else 1) = 0 :=
      block_product_residue_zero _ _ _ _ (by positivity) hdiv
        (by dsimp [blockSize]; positivity) t.isLt
    simp only [hz, Finset.sum_const_zero]
    have hle : (blockCount L j : ℝ) ≤ (2 : ℝ)^r := by
      simp only [blockCount, Nat.cast_pow, Nat.cast_ofNat]
      exact pow_le_pow_right₀ (by norm_num) hj
    rw [min_eq_left hle, sub_self]
  · have hjr : r ≤ j.val + 1 := by omega
    let q := 2 ^ (j.val + 1 - r)
    have hq : 0 < q := by dsimp [q]; positivity
    have hS : 0 < blockSize L j := by dsimp [blockSize]; positivity
    have hd : 2 ^ (L - r) = q * blockSize L j := by
      dsimp [q, blockSize]
      rw [← pow_add]
      congr 1
      omega
    have hK : blockCount L j = 2 ^ r * q := by
      dsimp [blockCount, q]
      rw [← pow_add, Nat.add_sub_of_le hjr]
    have hp (b : Fin (blockCount L j)) :
        (∏ k : Fin (blockSize L j),
          if (b.val * blockSize L j + k.val) % 2 ^ (L - r) = t.val then (0 : ℝ) else 1) =
            if b.val % q = t.val / blockSize L j then 0 else 1 := by
      simpa only [← hd] using
        block_product_residue (blockSize L j) q b.val t.val hS hq (by rw [← hd]; exact t.isLt)
    simp only [hp]
    have ht : t.val / blockSize L j < q := by
      apply (Nat.div_lt_iff_lt_mul hS).mpr
      simpa [hd, Nat.mul_comm] using t.isLt
    have hle : (2 : ℝ)^r ≤ (blockCount L j : ℝ) := by
      simp only [blockCount, Nat.cast_pow, Nat.cast_ofNat]
      exact pow_le_pow_right₀ (by norm_num) hjr
    rw [min_eq_right hle]
    -- Counting residue classes reduces the remaining sum to a rectangular finite product.
    rw [hK]
    simpa only [Nat.cast_pow, Nat.cast_ofNat] using
      sum_residue_complement (2 ^ r) q ⟨t.val / blockSize L j, ht⟩

/-- Uniform translations of the periodic failure pattern. -/
def leafLaw (L r : ℕ) : CubicGap.Law (CubicGap.Vertex (Fin (2 ^ L))) :=
  (CubicGap.Law.uniform (Fin (2 ^ (L - r)))).map (spacedLeaf L r)

@[simp] theorem leafLaw_mean (L r : ℕ) (hr : r ≤ L) (i : Fin (2 ^ L)) :
    (leafLaw L r).expect (fun v => CubicGap.vertexPoint v i) =
      1 - (2 : ℝ)^r / (2 : ℝ)^L := by
  simpa [leafLaw, Function.comp_def] using spacedLeaf_mean L r hr i

@[simp] theorem leafLaw_level_sum (L r : ℕ) (hr : r ≤ L) (j : Fin L) :
    (leafLaw L r).expect (fun v =>
      ∑ b : Fin (blockCount L j), ∏ i ∈ block L j b, CubicGap.vertexPoint v i) =
      (blockCount L j : ℝ) - min (blockCount L j : ℝ) ((2 : ℝ)^r) := by
  rw [leafLaw, CubicGap.Law.expect_map]
  simp only [Function.comp_def, spacedLeaf_level_sum L r hr j]
  simp [CubicGap.Law.expect, ← Finset.sum_mul, CubicGap.Law.mass_one]

end
end MultilinearGap
