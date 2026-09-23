import Formal.NetworkSimplex.ThresholdRows
import Mathlib.Combinatorics.Colex

/-! Canonical finite integer keys for the distinct profile normals. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

/-- Unused slots are allowed for the coincident normals in dimensions zero and one. -/
def normalKeyCount (m : ℕ) : ℕ := 2 ^ m + m + 1

def subsetMask {m : ℕ} (s : Finset (Fin m)) : ℕ := ∑ j ∈ s, 2 ^ j.val

theorem sum_fin_pow_two (m : ℕ) : (∑ j : Fin m, 2 ^ j.val) + 1 = 2 ^ m := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [Fin.sum_univ_castSucc]
    simp only [Fin.val_castSucc, Fin.val_last]
    rw [pow_succ]
    omega

theorem subsetMask_lt {m : ℕ} (s : Finset (Fin m)) : subsetMask s < 2 ^ m := by
  have h : subsetMask s ≤ ∑ j : Fin m, 2 ^ j.val :=
    Finset.sum_le_sum_of_subset (Finset.subset_univ s)
  have hs := sum_fin_pow_two m
  omega

theorem subsetMask_testBit {m : ℕ} (s : Finset (Fin m)) (j : Fin m) :
    (subsetMask s).testBit j.val = true ↔ j ∈ s := by
  have hs : (∑ k ∈ s.image Fin.val, 2 ^ k) = subsetMask s := by
    rw [Finset.sum_image]
    · rfl
    · intro a _ b _ h
      exact Fin.ext h
  have he := Finset.toFinset_bitIndices_sum_two_pow (s.image Fin.val)
  rw [hs] at he
  have hh : j.val ∈ (subsetMask s).bitIndices.toFinset ↔ j ∈ s := by
    rw [he]
    constructor
    · intro hj
      obtain ⟨k, hk, hkj⟩ := Finset.mem_image.mp hj
      exact Fin.ext hkj ▸ hk
    · intro hj
      exact Finset.mem_image.mpr ⟨j, hj, rfl⟩
  simpa only [List.mem_toFinset, Nat.mem_bitIndices] using hh

/-- The indices of negative singleton normals follow all positive subset masks.
The negative total is canonicalized when it coincides with zero or a singleton. -/
def packNormal {m : ℕ} : ProfileNormal m → Fin (normalKeyCount m)
  | .subset s => ⟨subsetMask s, by have := subsetMask_lt s; unfold normalKeyCount; omega⟩
  | .negativeSingleton j => ⟨2 ^ m + j.val, by unfold normalKeyCount; omega⟩
  | .negativeTotal => if hm0 : m = 0 then ⟨0, by simp [normalKeyCount]⟩
      else if hm1 : m = 1 then ⟨2 ^ m, by unfold normalKeyCount; omega⟩
      else ⟨2 ^ m + m, by unfold normalKeyCount; omega⟩

def keyNormal {m : ℕ} (k : Fin (normalKeyCount m)) (j : Fin m) : ℤ :=
  if k.val < 2 ^ m then if k.val.testBit j.val then 1 else 0
  else if k.val < 2 ^ m + m then if j.val = k.val - 2 ^ m then -1 else 0
  else -1

/-- Decoding the actual integer key recovers the exact original normal vector. -/
theorem keyNormal_packNormal {m : ℕ} (p : ProfileNormal m) :
    keyNormal (packNormal p) = normalVector p := by
  funext j
  cases p with
  | subset s =>
    by_cases hj : j ∈ s
    · have hb := (subsetMask_testBit s j).mpr hj
      simp [packNormal, keyNormal, subsetMask_lt, normalVector, hj, hb]
    · have hb : ¬(subsetMask s).testBit j.val = true := mt (subsetMask_testBit s j).mp hj
      simp [packNormal, keyNormal, subsetMask_lt, normalVector, hj, hb]
  | negativeSingleton k =>
    simp only [packNormal, keyNormal, normalVector]
    have h₁ : ¬2 ^ m + k.val < 2 ^ m := by omega
    have h₂ : 2 ^ m + k.val < 2 ^ m + m := by omega
    simp [h₁, h₂, Fin.ext_iff]
  | negativeTotal =>
    by_cases hm0 : m = 0
    · subst m
      exact Fin.elim0 j
    by_cases hm1 : m = 1
    · subst m
      simp [packNormal, keyNormal, normalVector]
    · simp [packNormal, hm0, hm1, keyNormal, normalVector]

@[simp] theorem packNormal_empty {m : ℕ} :
    (packNormal (.subset ∅ : ProfileNormal m)).val = 0 := by simp [packNormal, subsetMask]

@[simp] theorem keyNormal_zero {m : ℕ} :
    keyNormal (⟨0, by simp [normalKeyCount]⟩ : Fin (normalKeyCount m)) = 0 := by
  funext j
  simp [keyNormal]

def keyValue {m : ℕ} (k : Fin (normalKeyCount m)) (x : Fin m → ℝ) : ℝ :=
  ∑ j, (keyNormal k j : ℝ) * x j

theorem keyValue_packNormal {m : ℕ} (p : ProfileNormal m) (x : Fin m → ℝ) :
    keyValue (packNormal p) x = p.value x := by
  unfold keyValue
  rw [keyNormal_packNormal]
  cases p <;> simp [normalVector, ProfileNormal.value, ite_mul]

private theorem subset_normal_ne_singleton {m : ℕ} (s : Finset (Fin m)) (j : Fin m) :
    normalVector (.subset s) ≠ normalVector (.negativeSingleton j) := by
  intro h
  have he := congrFun h j
  by_cases hj : j ∈ s <;> simp [normalVector, hj] at he

private theorem singleton_eq_total_dimension {m : ℕ} (j : Fin m)
    (h : normalVector (.negativeSingleton j) = normalVector (.negativeTotal : ProfileNormal m)) :
    m = 1 := by
  by_contra hm
  have h2 : 2 ≤ m := by have := j.isLt; omega
  have hj : ∀ k : Fin m, k = j := by
    intro k
    have he := congrFun h k
    by_contra hk
    simp [normalVector, hk] at he
  have h0 := congrArg Fin.val (hj ⟨0, by omega⟩)
  have h1 := congrArg Fin.val (hj ⟨1, by omega⟩)
  simp only at h0 h1
  omega

/-- The producer keys merge exactly equal normal vectors, including the exceptional
zero- and one-dimensional coincidences. -/
theorem packNormal_eq_iff {m : ℕ} (p q : ProfileNormal m) :
    packNormal p = packNormal q ↔ normalVector p = normalVector q := by
  constructor
  · intro h
    simpa only [keyNormal_packNormal] using congrArg keyNormal h
  · intro h
    cases p with
    | subset s =>
      cases q with
      | subset t =>
        have hs : s = t := by
          ext j
          have he := congrFun h j
          by_cases hj : j ∈ s <;> by_cases hk : j ∈ t <;> simp_all [normalVector]
        rw [hs]
      | negativeSingleton j => exact (subset_normal_ne_singleton s j h).elim
      | negativeTotal =>
        have hm : m = 0 := by
          by_contra hm
          have hmpos : 0 < m := Nat.pos_of_ne_zero hm
          have he := congrFun h ⟨0, hmpos⟩
          by_cases hj : (⟨0, hmpos⟩ : Fin m) ∈ s <;> simp [normalVector, hj] at he
        subst m
        have hs : s = ∅ := Finset.eq_empty_of_forall_notMem (fun j _ => Fin.elim0 j)
        simp [hs, packNormal, subsetMask]
    | negativeSingleton j =>
      cases q with
      | subset s => exact (subset_normal_ne_singleton s j h.symm).elim
      | negativeSingleton k =>
        have hj : j = k := by
          have he := congrFun h j
          by_contra hj
          simp [normalVector, hj] at he
        rw [hj]
      | negativeTotal =>
        have hm := singleton_eq_total_dimension j h
        subst m
        apply Fin.ext
        simp [packNormal]
    | negativeTotal =>
      cases q with
      | subset s =>
        have hm : m = 0 := by
          by_contra hm
          have hmpos : 0 < m := Nat.pos_of_ne_zero hm
          have he := congrFun h ⟨0, hmpos⟩
          by_cases hj : (⟨0, hmpos⟩ : Fin m) ∈ s <;> simp [normalVector, hj] at he
        subst m
        have hs : s = ∅ := Finset.eq_empty_of_forall_notMem (fun j _ => Fin.elim0 j)
        simp [hs, packNormal, subsetMask]
      | negativeSingleton j =>
        have hm := singleton_eq_total_dimension j h.symm
        subst m
        apply Fin.ext
        simp [packNormal]
      | negativeTotal => rfl

/-- A direct subset mask requires one power-of-two word and one addition per member. -/
def subsetMaskWork {m : ℕ} (s : Finset (Fin m)) : ℕ := 2 * s.card

theorem subsetMaskWork_le {m : ℕ} (s : Finset (Fin m)) : subsetMaskWork s ≤ 2 * m := by
  have h := Finset.card_le_univ s
  simpa [subsetMaskWork] using Nat.mul_le_mul_left 2 h

/-- Executable mask production by shifts, charging one shift and one addition
for each existing subset member. Intermediate words have at most `m` bits. -/
def subsetMaskCounted {m : ℕ} (s : Finset (Fin m)) : ℕ × ℕ :=
  ∑ j ∈ s, ((1 : ℕ) <<< j.val, 2)

theorem subsetMaskCounted_value {m : ℕ} (s : Finset (Fin m)) :
    (subsetMaskCounted s).1 = subsetMask s := by
  simp [subsetMaskCounted, Prod.fst_sum, Nat.shiftLeft_eq, subsetMask]

def subsetMaskShift {m : ℕ} (s : Finset (Fin m)) : ℕ := (subsetMaskCounted s).1

/-- The executable key path uses the shift-and-add implementation. The
compiler replacement is justified by the mask identity above. -/
@[csimp] theorem subsetMask_eq_counted :
    @subsetMask = @subsetMaskShift := by
  funext m s
  exact (subsetMaskCounted_value s).symm

theorem subsetMaskCounted_work {m : ℕ} (s : Finset (Fin m)) :
    (subsetMaskCounted s).2 = subsetMaskWork s := by
  simp [subsetMaskCounted, Prod.snd_sum, subsetMaskWork, Nat.mul_comm]

theorem subsetMask_intermediate_bits {m : ℕ} (s : Finset (Fin m)) :
    (subsetMask s).size ≤ m := by
  rw [Nat.size_le]
  exact subsetMask_lt s

/-- Masked singleton keys use constant work; no full coordinate scan is required. -/
@[simp] theorem subsetMask_singleton {m : ℕ} (j : Fin m) :
    subsetMask {j} = 2 ^ j.val := by simp [subsetMask]

/-- Every table index uses at most `m+2` bits. -/
theorem normalKeyCount_le_pow (m : ℕ) : normalKeyCount m ≤ 2 ^ (m + 2) := by
  have hm : m < 2 ^ m := Nat.lt_two_pow_self
  unfold normalKeyCount
  rw [pow_add]
  norm_num
  omega

theorem packed_key_bitlength {m : ℕ} (p : ProfileNormal m) : (packNormal p).val.size ≤ m + 2 := by
  rw [Nat.size_le]
  exact (packNormal p).isLt.trans_le (normalKeyCount_le_pow m)

end NetworkSimplex.Chain.Threshold
