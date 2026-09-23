import Mathlib.Data.Finset.Dedup
import Formal.DAGSpectral.FinRangeExecution

/-! Coupled construction and identifier work for the input to subset trials.
Finsets are built from the already deduplicated list, without a second scan. -/
namespace DAGSpectral.CoverBitCost

/-- A complete executed membership scan over the stored identifier list. -/
def identifierAbsentCounted {M : ℕ} (a : Fin M) : List (Fin M) → Bool × ℕ
  | [] => (true, 1)
  | b::xs =>
    let tail := identifierAbsentCounted a xs
    (!decide (a=b) && tail.1, tail.2+a.val.size+b.val.size+1)

@[simp] theorem identifierAbsentCounted_value {M : ℕ} (a : Fin M) (xs : List (Fin M)) :
    (identifierAbsentCounted a xs).1 = decide (a ∉ xs) := by
  induction xs with
  | nil => rfl
  | cons b xs ih => simp [identifierAbsentCounted, ih]

theorem identifierAbsentCounted_work {M : ℕ} (a : Fin M) (xs : List (Fin M)) :
    (identifierAbsentCounted a xs).2 ≤ 1+xs.length*(2*M+3) := by
  induction xs with
  | nil => simp [identifierAbsentCounted]
  | cons b xs ih =>
    have ha : a.val.size ≤ M :=
      (Nat.size_le.mpr (Nat.lt_two_pow_self)).trans a.isLt.le
    have hb : b.val.size ≤ M :=
      (Nat.size_le.mpr (Nat.lt_two_pow_self)).trans b.isLt.le
    simp only [identifierAbsentCounted, List.length_cons]
    nlinarith

/-- The proof of distinctness comes from the executed absence test. -/
def distinctIdentifiersCounted {M : ℕ} : List (Fin M) →
    {xs : List (Fin M) // xs.Nodup} × ℕ
  | [] => (⟨[], by simp⟩, 1)
  | a::xs =>
    let tail := distinctIdentifiersCounted xs
    let absent := identifierAbsentCounted a tail.1.val
    if h : absent.1 = true then
      (⟨a::tail.1.val, List.nodup_cons.mpr ⟨by
        change (identifierAbsentCounted a tail.1.val).1 = true at h
        simpa only [identifierAbsentCounted_value, decide_eq_true_eq] using h,
        tail.1.property⟩⟩, tail.2+absent.2+a.val.size+2)
    else (tail.1, tail.2+absent.2+1)

@[simp] theorem distinctIdentifiersCounted_value {M : ℕ} (xs : List (Fin M)) :
    (distinctIdentifiersCounted xs).1.val = xs.dedup := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    simp only [distinctIdentifiersCounted, identifierAbsentCounted_value, decide_eq_true_eq]
    split_ifs with h
    · simp only [ih, List.dedup_cons, List.mem_dedup] at h ⊢
      simp [h]
    · simp only [ih, List.dedup_cons, List.mem_dedup] at h ⊢
      simp [h]

theorem distinctIdentifiersCounted_work {M : ℕ} (xs : List (Fin M)) :
    (distinctIdentifiersCounted xs).2 ≤ (xs.length+1)^2*(2*M+3) := by
  induction xs with
  | nil => simp [distinctIdentifiersCounted]
  | cons a xs ih =>
    have hl : (distinctIdentifiersCounted xs).1.val.length ≤ xs.length := by
      rw [distinctIdentifiersCounted_value]
      exact (List.dedup_sublist xs).length_le
    have hc := identifierAbsentCounted_work a (distinctIdentifiersCounted xs).1.val
    have hbound : (identifierAbsentCounted a (distinctIdentifiersCounted xs).1.val).2 ≤
        1+xs.length*(2*M+3) := by
      exact hc.trans (Nat.add_le_add_left (Nat.mul_le_mul_right _ hl) 1)
    have ha : a.val.size ≤ M :=
      (Nat.size_le.mpr (Nat.lt_two_pow_self)).trans a.isLt.le
    simp only [distinctIdentifiersCounted, List.length_cons]
    split_ifs <;> dsimp
    · nlinarith
    · nlinarith

/-- The constructor takes the proved-distinct multiset directly; it does not run dedup again. -/
def subsetCounted {M : ℕ} (xs : List (Fin M)) : Finset (Fin M) × ℕ :=
  let result := distinctIdentifiersCounted xs
  (⟨result.1.val, result.1.property⟩, result.2)

@[simp] theorem subsetCounted_value {M : ℕ} (xs : List (Fin M)) :
    (subsetCounted xs).1 = xs.toFinset := by
  ext x
  simp [subsetCounted, distinctIdentifiersCounted_value]

theorem subsetCounted_work {M : ℕ} (xs : List (Fin M)) :
    (subsetCounted xs).2 ≤ (xs.length+1)^2*(2*M+3) := distinctIdentifiersCounted_work xs

/-- Convert the actual enumerated subset lists, retaining each conversion's work. -/
def subsetsCounted {M : ℕ} : List (List (Fin M)) → List (Finset (Fin M)) × ℕ
  | [] => ([], 1)
  | xs::xss =>
    let head := subsetCounted xs
    let tail := subsetsCounted xss
    (head.1::tail.1, head.2+tail.2+1)

@[simp] theorem subsetsCounted_value {M : ℕ} (xss : List (List (Fin M))) :
    (subsetsCounted xss).1 = xss.map List.toFinset := by
  induction xss with
  | nil => rfl
  | cons xs xss ih => simp only [subsetsCounted, subsetCounted_value, ih, List.map_cons]

theorem subsetsCounted_work {M r : ℕ} (xss : List (List (Fin M)))
    (hlen : ∀ xs ∈ xss, xs.length ≤ r) :
    (subsetsCounted xss).2 ≤ 1+xss.length*((r+1)^2*(2*M+3)+1) := by
  induction xss with
  | nil => simp [subsetsCounted]
  | cons xs xss ih =>
    have ht := ih (fun ys hy => hlen ys (by simp [hy]))
    have hs := subsetCounted_work xs
    have hl := hlen xs (by simp)
    have hb : (xs.length+1)^2*(2*M+3) ≤ (r+1)^2*(2*M+3) := by gcongr
    have hh := hs.trans hb
    simp only [subsetsCounted, List.length_cons]
    nlinarith

end DAGSpectral.CoverBitCost
