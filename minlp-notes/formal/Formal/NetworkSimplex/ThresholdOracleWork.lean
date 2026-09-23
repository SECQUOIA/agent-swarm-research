import Formal.NetworkSimplex.ThresholdThreePacked

/-! Word-operation accounting for cached masks, row traversal, and indexed grouping.

The model charges one indexed array access, constructor/tag test, counter update,
or shift/add of an `O(m)`-bit normal key as one word operation. Rational work is
counted by the executed oracle and receives its separate schoolbook bit bound.
The traversal allowance below overestimates each explicit source loop; it is not
a claim about a compiler's instruction count or allocation strategy.
-/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.ThresholdOracle

/-- The actual cached subset-mask computations, including all endpoint masks. -/
def cachedMaskWork {m L : ℕ} (D : RationalData m L) : ℕ :=
  (List.ofFn fun j : Fin m => (subsetMaskCounted {j}).2).sum +
    (subsetMaskCounted (Finset.univ : Finset (Fin m))).2 +
    (List.ofFn fun i : Fin L =>
      (subsetMaskCounted (D.cache.gadget i).subsetB).2 +
      (subsetMaskCounted (D.cache.gadget i).subsetA).2).sum

theorem cachedMaskWork_le {m L : ℕ} (D : RationalData m L) :
    cachedMaskWork D ≤ 4 * m * (L + 1) := by
  have hend : (List.ofFn fun i : Fin L =>
      (subsetMaskCounted (D.cache.gadget i).subsetB).2 +
      (subsetMaskCounted (D.cache.gadget i).subsetA).2).sum ≤ L * (4 * m) := by
    rw [List.sum_ofFn]
    calc
      _ ≤ ∑ _i : Fin L, 4 * m := by
        apply Finset.sum_le_sum
        intro i _
        rw [subsetMaskCounted_work, subsetMaskCounted_work]
        have h1 := subsetMaskWork_le (D.cache.gadget i).subsetB
        have h2 := subsetMaskWork_le (D.cache.gadget i).subsetA
        omega
      _ = _ := by simp
  unfold cachedMaskWork
  simp only [List.sum_ofFn, subsetMaskCounted_work, subsetMaskWork,
    Finset.card_singleton, Nat.mul_one, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, smul_eq_mul] at *
  nlinarith

/-- Constant work per emitted original row and each cached classification entry.
Global key constants may be recomputed; the final square covers this parameter-only work. -/
def packingLoopWork {m L : ℕ} (D : RationalData m L) : ℕ :=
  8 * (D.indexedRows packNormal).length + 4 * m * L + cachedMaskWork D + 4 * (m + 1) ^ 2

/-- Rational arithmetic uses the executed charge. Structural work includes the
executed grouping access count and all circuit-selection list traversals. -/
def packedWordWork {m L : ℕ} (D : RationalData m L)
    (library : List (Circuit (normalKeyCount m))) : ℕ :=
  (packedOracle D library).2 + (packedGroup D).accesses + packingLoopWork D +
    (library.map fun c => 6 * c.length + 2).sum

theorem packedWordWork_le {m L : ℕ} (D : RationalData m L) (hm : 1 ≤ m)
    (library : List (Circuit (normalKeyCount m))) :
    packedWordWork D library ≤
      100 * m * (L + 1) + normalKeyCount m + 4 * (m + 1) ^ 2 +
        (library.map fun c => 8 * c.length + 3).sum := by
  have ha := packedOracle_arithmeticCharge D hm library
  have hg := (NetworkSimplex.ThresholdGrouping.group_cost (D.indexedRows packNormal)).2
  have hk := cachedMaskWork_le D
  have hsum : (library.map fun c => 2 * c.length + 1).sum +
      (library.map fun c => 6 * c.length + 2).sum =
      (library.map fun c => 8 * c.length + 3).sum := by
    clear ha
    induction library with
    | nil => simp
    | cons c cs ih => simp only [List.map_cons, List.sum_cons]; omega
  rw [D.indexedRows_length packNormal] at hg
  unfold packedWordWork packingLoopWork
  rw [D.indexedRows_length packNormal]
  change (packedOracle D library).2 +
    (NetworkSimplex.ThresholdGrouping.group (D.indexedRows packNormal)).accesses + _ + _ ≤ _
  rw [hg]
  nlinarith

theorem threeOracle_wordWork {L : ℕ} (D : RationalData 3 L) :
    packedWordWork D threeLibrary ≤ 300 * (L + 1) + 1543 := by
  have h := packedWordWork_le D (by decide) threeLibrary
  have hc : (threeLibrary.map fun c => 8 * c.length + 3).sum = 1467 := by decide +kernel
  rw [hc] at h
  convert h using 1
  norm_num [normalKeyCount]

end NetworkSimplex.Chain.Threshold
