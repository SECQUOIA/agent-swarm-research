import Formal.MultilinearGap.RadixFamily
import Formal.CubicGap.Laws

/-!
# The unit-box incidence bound for the variable-radix family (PB37)

For the radix-`b` anchor/leaf family of `RadixFamily.lean`, let `A_j` be the
binary anchor of level `j`, let `R` be the number of failed leaves, and let
`N_j` be the number of level-`j` blocks containing at least one failed leaf.
`results/positive-multilinear-incidence-sharp-growth.md` shows that over all
joint binary laws with the prescribed marginals

  `E A_j = b ^ -(j+1)`,  `E Z_i = 1 - b ^ -L`  (so `E R = 1`),

the maximum of `E ∑_j A_j N_j` equals `1 + (L-1)/b`.  This file proves the
**upper direction**, which is the direction imported by
`results/positive-multilinear-positive-box-lower.md`.

The proof replaces the source's rearrangement argument by the equivalent
linear-programming dual certificate it produces: with the dual weights
`dualWeight b j` (`0` at the top level, `b ^ j` below it) one has the
*pointwise* inequality, valid at every binary assignment,

  `∑_j A_j min (b ^ (j+1)) R ≤ R + ∑_j A_j * dualWeight b j`,

whose expectation against the prescribed marginals is exactly `1 + (L-1)/b`.
This needs only `1 ≤ b`; the source's hypothesis `b ≥ L` is needed for the
matching attainment, which is not proved here.
-/

namespace MultilinearGap
namespace Radix

noncomputable section
open scoped BigOperators

/-! ## Expectations of finite laws -/

variable {ι : Type*} [Fintype ι]

/-- Expectation is monotone. -/
theorem expect_mono (μ : CubicGap.Law ι) {f g : ι → ℝ} (h : ∀ i, f i ≤ g i) :
    μ.expect f ≤ μ.expect g :=
  Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_left (h i) (μ.nonneg i)

/-- Expectation of a constant. -/
theorem expect_const (μ : CubicGap.Law ι) (a : ℝ) : μ.expect (fun _ => a) = a := by
  simp [CubicGap.Law.expect, ← Finset.sum_mul, μ.mass_one]

/-- Expectation is additive. -/
theorem expect_add (μ : CubicGap.Law ι) (f g : ι → ℝ) :
    μ.expect (fun i => f i + g i) = μ.expect f + μ.expect g := by
  simp [CubicGap.Law.expect, mul_add, Finset.sum_add_distrib]

/-- Expectation commutes with a finite sum. -/
theorem expect_finsetSum {κ : Type*} (μ : CubicGap.Law ι) (s : Finset κ) (f : κ → ι → ℝ) :
    μ.expect (fun i => ∑ k ∈ s, f k i) = ∑ k ∈ s, μ.expect (f k) := by
  simp only [CubicGap.Law.expect, Finset.mul_sum]
  exact Finset.sum_comm

/-- Expectation is homogeneous. -/
theorem expect_mul_const (μ : CubicGap.Law ι) (f : ι → ℝ) (a : ℝ) :
    μ.expect (fun i => f i * a) = μ.expect f * a := by
  simp [CubicGap.Law.expect, Finset.sum_mul, mul_assoc]

/-- Vertex coordinates are nonnegative. -/
theorem vertexPoint_nonneg {I : Type*} (v : CubicGap.Vertex I) (i : I) :
    0 ≤ CubicGap.vertexPoint v i := by
  simp only [CubicGap.vertexPoint]
  split <;> norm_num

/-! ## Failed leaves and hit blocks -/

/-- The leaves that fail at a binary assignment. -/
def failedLeaves (b L : ℕ) (v : CubicGap.Vertex (Coord b L)) : Finset (Fin (b ^ L)) :=
  Finset.univ.filter (fun i => v (Sum.inr i) = false)

/-- The total number `R` of failed leaves. -/
def failureCount (b L : ℕ) (v : CubicGap.Vertex (Coord b L)) : ℕ :=
  (failedLeaves b L v).card

/-- The level-`j` blocks that contain at least one failed leaf. -/
def hitBlocks (b L : ℕ) (j : Fin L) (v : CubicGap.Vertex (Coord b L)) :
    Finset (Fin (blockCount b L j)) :=
  (failedLeaves b L v).image (fun i => (blockEquiv b L j i).1)

/-- The number `N_j` of level-`j` blocks containing at least one failed leaf. -/
def hitCount (b L : ℕ) (j : Fin L) (v : CubicGap.Vertex (Coord b L)) : ℕ :=
  (hitBlocks b L j v).card

/-- `hitBlocks` is exactly the set of level-`j` blocks meeting the failed leaves. -/
theorem mem_hitBlocks_iff (b L : ℕ) (j : Fin L) (v : CubicGap.Vertex (Coord b L))
    (c : Fin (blockCount b L j)) :
    c ∈ hitBlocks b L j v ↔ ∃ i ∈ block b L j c, v (Sum.inr i) = false := by
  simp only [hitBlocks, Finset.mem_image, failedLeaves, Finset.mem_filter, Finset.mem_univ,
    true_and, block_mem_iff]
  constructor
  · rintro ⟨i, hv, rfl⟩
    exact ⟨i, rfl, hv⟩
  · rintro ⟨i, hc, hv⟩
    exact ⟨i, hv, hc⟩

/-- `N_j` counts the level-`j` blocks containing at least one failed leaf. -/
theorem hitCount_eq_card_filter (b L : ℕ) (j : Fin L) (v : CubicGap.Vertex (Coord b L)) :
    hitCount b L j v =
      (Finset.univ.filter
        (fun c : Fin (blockCount b L j) => ∃ i ∈ block b L j c, v (Sum.inr i) = false)).card := by
  refine congrArg Finset.card (Finset.ext fun c => ?_)
  simp [mem_hitBlocks_iff]

/-- At most every level-`j` block is hit. -/
theorem hitCount_le_blockCount (b L : ℕ) (j : Fin L) (v : CubicGap.Vertex (Coord b L)) :
    hitCount b L j v ≤ blockCount b L j := by
  simpa [hitCount] using Finset.card_le_univ (hitBlocks b L j v)

/-- Each failed leaf hits one block, so `N_j ≤ R`. -/
theorem hitCount_le_failureCount (b L : ℕ) (j : Fin L) (v : CubicGap.Vertex (Coord b L)) :
    hitCount b L j v ≤ failureCount b L v :=
  Finset.card_image_le

/-- The two elementary bounds `N_j ≤ min (b ^ (j+1)) R`, over the reals. -/
theorem hitCount_le_min (b L : ℕ) (j : Fin L) (v : CubicGap.Vertex (Coord b L)) :
    (hitCount b L j v : ℝ) ≤ min ((b : ℝ) ^ (j.val + 1)) (failureCount b L v : ℝ) := by
  refine le_min ?_ ?_
  · have h := hitCount_le_blockCount b L j v
    have : ((hitCount b L j v : ℕ) : ℝ) ≤ ((blockCount b L j : ℕ) : ℝ) := by exact_mod_cast h
    simpa [blockCount] using this
  · exact_mod_cast hitCount_le_failureCount b L j v

/-- `R` as a sum over the leaf coordinates of the vertex point. -/
theorem failureCount_eq_sum (b L : ℕ) (v : CubicGap.Vertex (Coord b L)) :
    (failureCount b L v : ℝ) = ∑ i, (1 - CubicGap.vertexPoint v (Sum.inr i)) := by
  have hterm : ∀ i : Fin (b ^ L), (1 - CubicGap.vertexPoint v (Sum.inr i)) =
      if v (Sum.inr i) = false then (1 : ℝ) else 0 := by
    intro i
    cases hv : v (Sum.inr i) <;> simp [CubicGap.vertexPoint, hv]
  rw [Finset.sum_congr rfl (fun i _ => hterm i), Finset.sum_boole]
  simp [failureCount, failedLeaves]

/-! ## The dual certificate -/

/-- The dual weight of level `j`: zero at the top level, `b ^ j` below it. -/
def dualWeight (b j : ℕ) : ℝ := if j = 0 then 0 else (b : ℝ) ^ j

theorem dualWeight_nonneg (b j : ℕ) : 0 ≤ dualWeight b j := by
  unfold dualWeight
  split
  · exact le_rfl
  · exact pow_nonneg (Nat.cast_nonneg b) j

/-- The dual weight of a level is dominated by the block count of that level. -/
theorem dualWeight_le_pow (b : ℕ) (hb : 1 ≤ b) (j : ℕ) : dualWeight b j ≤ (b : ℝ) ^ (j + 1) := by
  have hb1 : (1 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb
  unfold dualWeight
  split
  · positivity
  · exact pow_le_pow_right₀ hb1 (Nat.le_succ j)

/-- The core telescoping estimate: for any set `S` of levels below `n` and any
failure count `r ≥ 0`, the dual slack accumulated by `S` is at most
`min (dualWeight b n) r`. -/
theorem dual_sum_le (b : ℕ) (hb : 1 ≤ b) (r : ℝ) (hr : 0 ≤ r) (n : ℕ) (S : Finset ℕ)
    (hS : S ⊆ Finset.range n) :
    ∑ k ∈ S, (min ((b : ℝ) ^ (k + 1)) r - dualWeight b k) ≤ min (dualWeight b n) r := by
  induction n generalizing S with
  | zero =>
    have hS' : S = ∅ := Finset.subset_empty.mp (by simpa using hS)
    subst hS'
    simp [dualWeight, min_eq_left hr]
  | succ n ih =>
    have hdw : dualWeight b (n + 1) = (b : ℝ) ^ (n + 1) := by simp [dualWeight]
    by_cases hn : n ∈ S
    · have hsub : S.erase n ⊆ Finset.range n := by
        intro k hk
        have hk1 : k ∈ S := Finset.mem_of_mem_erase hk
        have hk2 : k ≠ n := Finset.ne_of_mem_erase hk
        have := Finset.mem_range.mp (hS hk1)
        exact Finset.mem_range.mpr (by omega)
      have hrec := ih _ hsub
      have hle : ∑ k ∈ S.erase n, (min ((b : ℝ) ^ (k + 1)) r - dualWeight b k)
          ≤ dualWeight b n := le_trans hrec (min_le_left _ _)
      rw [← Finset.sum_erase_add S _ hn, hdw]
      have := min_le_right ((b : ℝ) ^ (n + 1)) r
      have hmin : min ((b : ℝ) ^ (n + 1)) r ≤ (b : ℝ) ^ (n + 1) := min_le_left _ _
      refine le_min ?_ ?_ <;> linarith
    · have hsub : S ⊆ Finset.range n := by
        intro k hk
        have hk2 : k ≠ n := fun h => hn (h ▸ hk)
        have := Finset.mem_range.mp (hS hk)
        exact Finset.mem_range.mpr (by omega)
      refine le_trans (ih _ hsub) ?_
      rw [hdw]
      exact min_le_min (dualWeight_le_pow b hb n) le_rfl

/-- The dual certificate at a fixed set `T` of selected levels and fixed failure count. -/
theorem dual_pointwise (b L : ℕ) (hb : 1 ≤ b) (r : ℝ) (hr : 0 ≤ r) (T : Finset (Fin L)) :
    ∑ j ∈ T, min ((b : ℝ) ^ (j.val + 1)) r ≤ r + ∑ j ∈ T, dualWeight b j.val := by
  have himg : T.image Fin.val ⊆ Finset.range L := by
    intro k hk
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hk
    exact Finset.mem_range.mpr j.isLt
  have h := dual_sum_le b hb r hr L (T.image Fin.val) himg
  have hsum : ∑ k ∈ T.image Fin.val, (min ((b : ℝ) ^ (k + 1)) r - dualWeight b k)
      = ∑ j ∈ T, (min ((b : ℝ) ^ (j.val + 1)) r - dualWeight b j.val) :=
    Finset.sum_image (fun a _ c _ hac => Fin.ext hac)
  rw [hsum] at h
  have h2 := le_trans h (min_le_right (dualWeight b L) r)
  rw [Finset.sum_sub_distrib] at h2
  linarith

/-- The dual certificate at a binary assignment: the objective `∑_j A_j N_j` is
dominated by `R` plus the dual weights of the selected levels. -/
theorem objective_pointwise (b L : ℕ) (hb : 1 ≤ b) (v : CubicGap.Vertex (Coord b L)) :
    (∑ j, CubicGap.vertexPoint v (Sum.inl j) * (hitCount b L j v : ℝ))
      ≤ (failureCount b L v : ℝ)
        + ∑ j, CubicGap.vertexPoint v (Sum.inl j) * dualWeight b j.val := by
  have hr : (0 : ℝ) ≤ (failureCount b L v : ℝ) := Nat.cast_nonneg _
  have h1 : (∑ j, CubicGap.vertexPoint v (Sum.inl j) * (hitCount b L j v : ℝ))
      ≤ ∑ j, CubicGap.vertexPoint v (Sum.inl j) *
          min ((b : ℝ) ^ (j.val + 1)) (failureCount b L v : ℝ) :=
    Finset.sum_le_sum fun j _ =>
      mul_le_mul_of_nonneg_left (hitCount_le_min b L j v) (vertexPoint_nonneg v _)
  refine le_trans h1 ?_
  have hT : ∀ h : Fin L → ℝ, (∑ j, CubicGap.vertexPoint v (Sum.inl j) * h j)
      = ∑ j ∈ Finset.univ.filter (fun j : Fin L => v (Sum.inl j) = true), h j := by
    intro h
    rw [Finset.sum_filter]
    refine Finset.sum_congr rfl fun j _ => ?_
    cases hv : v (Sum.inl j) <;> simp [CubicGap.vertexPoint, hv]
  rw [hT (fun j => min ((b : ℝ) ^ (j.val + 1)) (failureCount b L v : ℝ)),
    hT (fun j => dualWeight b j.val)]
  exact dual_pointwise b L hb _ hr _

/-! ## The dual objective value -/

/-- The dual weights, priced level by level, total `(L-1)/b`. -/
theorem sum_range_dualWeight (b : ℕ) (hb : 1 ≤ b) (L : ℕ) (hL : 1 ≤ L) :
    ∑ k ∈ Finset.range L, dualWeight b k * (1 / (b : ℝ) ^ (k + 1)) = ((L : ℝ) - 1) / b := by
  have hb0 : (b : ℝ) ≠ 0 := by
    have : (0 : ℝ) < (b : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hb
    exact ne_of_gt this
  induction L, hL using Nat.le_induction with
  | base => simp [dualWeight]
  | succ L hL ih =>
    have hL0 : L ≠ 0 := by omega
    have hpow : (b : ℝ) ^ L ≠ 0 := pow_ne_zero _ hb0
    rw [Finset.sum_range_succ, ih]
    have hdw : dualWeight b L = (b : ℝ) ^ L := by simp [dualWeight, hL0]
    rw [hdw, pow_succ]
    field_simp
    push_cast
    ring

/-- The dual weights, priced at the prescribed anchor means, total `(L-1)/b`. -/
theorem sum_dualWeight_anchorMean (b L : ℕ) (hb : 1 ≤ b) (hL : 1 ≤ L) :
    ∑ j : Fin L, dualWeight b j.val * (1 / (blockCount b L j : ℝ)) = ((L : ℝ) - 1) / b := by
  have hterm : ∀ j : Fin L, dualWeight b j.val * (1 / (blockCount b L j : ℝ))
      = dualWeight b j.val * (1 / (b : ℝ) ^ (j.val + 1)) := by
    intro j
    simp [blockCount]
  rw [Finset.sum_congr rfl (fun j _ => hterm j),
    Fin.sum_univ_eq_sum_range (fun k => dualWeight b k * (1 / (b : ℝ) ^ (k + 1))) L]
  exact sum_range_dualWeight b hb L hL

/-! ## The imported unit-box bound (PB37), upper direction -/

/-- **PB37, upper direction.**  For the radix-`b` family with `L` levels, every
joint binary law whose anchors have the prescribed means `b ^ -(j+1)` and whose
failed-leaf count has mean one satisfies `E ∑_j A_j N_j ≤ 1 + (L-1)/b`. -/
theorem incidence_expect_le (b L : ℕ) (hb : 1 ≤ b) (hL : 1 ≤ L)
    (μ : CubicGap.Law (CubicGap.Vertex (Coord b L)))
    (hanchor : ∀ j : Fin L,
      μ.expect (fun v => CubicGap.vertexPoint v (Sum.inl j)) = 1 / (blockCount b L j : ℝ))
    (hfail : μ.expect (fun v => (failureCount b L v : ℝ)) = 1) :
    μ.expect (fun v => ∑ j, CubicGap.vertexPoint v (Sum.inl j) * (hitCount b L j v : ℝ))
      ≤ 1 + ((L : ℝ) - 1) / b := by
  refine le_trans (expect_mono μ (fun v => objective_pointwise b L hb v)) ?_
  rw [expect_add μ (fun v => (failureCount b L v : ℝ))
    (fun v => ∑ j, CubicGap.vertexPoint v (Sum.inl j) * dualWeight b j.val), hfail,
    expect_finsetSum μ Finset.univ
      (fun j v => CubicGap.vertexPoint v (Sum.inl j) * dualWeight b j.val)]
  have hj : ∀ j : Fin L,
      μ.expect (fun v => CubicGap.vertexPoint v (Sum.inl j) * dualWeight b j.val)
        = dualWeight b j.val * (1 / (blockCount b L j : ℝ)) := by
    intro j
    rw [expect_mul_const μ (fun v => CubicGap.vertexPoint v (Sum.inl j)) (dualWeight b j.val),
      hanchor j]
    ring
  rw [Finset.sum_congr rfl (fun j _ => hj j), sum_dualWeight_anchorMean b L hb hL]

/-- The prescribed leaf marginals `1 - b ^ -L` give mean failure count one. -/
theorem expect_failureCount_of_leafMeans (b L : ℕ) (hb : 1 ≤ b)
    (μ : CubicGap.Law (CubicGap.Vertex (Coord b L)))
    (hleaf : ∀ i : Fin (b ^ L),
      μ.expect (fun v => CubicGap.vertexPoint v (Sum.inr i)) = 1 - 1 / (b : ℝ) ^ L) :
    μ.expect (fun v => (failureCount b L v : ℝ)) = 1 := by
  have hpow : (0 : ℝ) < (b : ℝ) ^ L := by
    have : (0 : ℝ) < (b : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hb
    positivity
  have hcard : ((b ^ L : ℕ) : ℝ) = (b : ℝ) ^ L := by push_cast; ring
  calc μ.expect (fun v => (failureCount b L v : ℝ))
      = μ.expect (fun v => ∑ i, (1 - CubicGap.vertexPoint v (Sum.inr i))) := by
        simp only [failureCount_eq_sum]
    _ = ∑ i : Fin (b ^ L), μ.expect (fun v => 1 - CubicGap.vertexPoint v (Sum.inr i)) :=
        expect_finsetSum μ Finset.univ (fun i v => 1 - CubicGap.vertexPoint v (Sum.inr i))
    _ = ∑ _i : Fin (b ^ L), 1 / (b : ℝ) ^ L := by
        refine Finset.sum_congr rfl fun i _ => ?_
        have := expect_add μ (fun _ => (1 : ℝ)) (fun v => -CubicGap.vertexPoint v (Sum.inr i))
        have hneg : μ.expect (fun v => -CubicGap.vertexPoint v (Sum.inr i))
            = -μ.expect (fun v => CubicGap.vertexPoint v (Sum.inr i)) := by
          simp [CubicGap.Law.expect, Finset.sum_neg_distrib]
        have hsub : μ.expect (fun v => 1 - CubicGap.vertexPoint v (Sum.inr i))
            = 1 - μ.expect (fun v => CubicGap.vertexPoint v (Sum.inr i)) := by
          simpa [sub_eq_add_neg, expect_const, hneg] using this
        rw [hsub, hleaf i]
        ring
    _ = 1 := by
        rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, hcard]
        field_simp

/-- **PB37, upper direction, marginal form.**  With the prescribed anchor means
`b ^ -(j+1)` and leaf means `1 - b ^ -L` of the sources, every joint binary law
satisfies `E ∑_j A_j N_j ≤ 1 + (L-1)/b`. -/
theorem incidence_expect_le_of_means (b L : ℕ) (hb : 1 ≤ b) (hL : 1 ≤ L)
    (μ : CubicGap.Law (CubicGap.Vertex (Coord b L)))
    (hanchor : ∀ j : Fin L,
      μ.expect (fun v => CubicGap.vertexPoint v (Sum.inl j)) = means b L (Sum.inl j))
    (hleaf : ∀ i : Fin (b ^ L),
      μ.expect (fun v => CubicGap.vertexPoint v (Sum.inr i)) = means b L (Sum.inr i)) :
    μ.expect (fun v => ∑ j, CubicGap.vertexPoint v (Sum.inl j) * (hitCount b L j v : ℝ))
      ≤ 1 + ((L : ℝ) - 1) / b :=
  incidence_expect_le b L hb hL μ hanchor
    (expect_failureCount_of_leafMeans b L hb μ hleaf)

end
end Radix
end MultilinearGap
