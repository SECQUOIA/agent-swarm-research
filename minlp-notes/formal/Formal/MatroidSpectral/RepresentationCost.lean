import Formal.MatroidSpectral.RepresentationExecution
import Formal.MatroidSpectral.EliminationExecution

/-! Arithmetic execution for row preprocessing. Gram entries are materialized
once, and the determinant execution includes denominator clearing. -/
namespace MatroidSpectral
open Matrix Elimination DAGSpectral ReciprocalAnchor
open scoped BigOperators

def gramEntryRun {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) (i j : Fin S.card) : ScalarRun ℚ :=
  sumRun (List.ofFn fun k : Fin m =>
    mul (atom (A (S.orderEmbOfFin rfl i) k)) (atom (A (S.orderEmbOfFin rfl j) k)))

theorem gramEntryRun_value {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) (i j : Fin S.card) :
    (gramEntryRun A S i j).value = rowGramFin A S i j := by
  simp [gramEntryRun, List.map_ofFn, Function.comp_def, mul, atom,
    List.sum_ofFn, rowGramFin, rowGram, rowRestriction, Matrix.submatrix, Matrix.mul_apply]

theorem gramEntryRun_operations {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) (i j : Fin S.card) :
    (gramEntryRun A S i j).operations = 2*m := by
  simp [gramEntryRun, List.map_ofFn, Function.comp_def, mul, atom]
  omega

def gramRun {a m : ℕ} (A : RationalRepresentation a m) (S : Finset (Fin a)) :
    MatrixRun ℚ S.card :=
  let entries := Vector.ofFn fun i => Vector.ofFn fun j => gramEntryRun A S i j
  ⟨entries.map (fun row => row.map ScalarRun.value),
    ∑ i : Fin S.card, ∑ j : Fin S.card, entries[i.val][j.val].operations,
    (List.ofFn fun i : Fin S.card => (List.ofFn fun j : Fin S.card =>
      entries[i.val][j.val].operands).flatten).flatten⟩

theorem gramRun_value {a m : ℕ} (A : RationalRepresentation a m) (S : Finset (Fin a)) :
    view (gramRun A S).matrix = rowGramFin A S := by
  ext i j
  simpa only [view, gramRun, Vector.getElem_map, Vector.getElem_ofFn] using
    gramEntryRun_value A S i j

theorem gramRun_operations {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) : (gramRun A S).operations = S.card*S.card*(2*m) := by
  simp [gramRun, gramEntryRun_operations, Nat.mul_assoc]

structure RowReductionRun (a : ℕ) where
  selected : Finset (Fin a)
  operations : ℕ
  operands : List (ℚ × ℚ)

/-- Each scan step caches its Gram matrix and its full determinant execution. -/
def rowReductionRun {a m : ℕ} (A : RationalRepresentation a m) :
    List (Fin a) → RowReductionRun a
  | [] => ⟨∅, 0, []⟩
  | i :: is =>
      let prior := rowReductionRun A is
      let candidate := insert i prior.selected
      let gram := gramRun A candidate
      let result := rationalDeterminantRun (view gram.matrix)
      ⟨if result.value ≠ 0 then candidate else prior.selected,
        prior.operations + gram.operations + result.operations + 1,
        prior.operands ++ gram.operands ++ result.operands ++ [(result.value, 0)]⟩

theorem rowReductionRun_selected {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) : (rowReductionRun A rows).selected = selectRows A rows := by
  induction rows with
  | nil => rfl
  | cons i is ih =>
      simp only [rowReductionRun, rationalDeterminantRun_correct, gramRun_value,
        rowGramFin_det, selectRows]
      rw [ih]

def rowReductionStepOperations (a m : ℕ) : ℕ := a*a*(2*m) + 8*(a+1)^4 + 1

theorem rowReductionRun_operations_le {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) :
    (rowReductionRun A rows).operations ≤ rows.length * rowReductionStepOperations a m := by
  induction rows with
  | nil => simp [rowReductionRun]
  | cons i is ih =>
      let S := insert i (rowReductionRun A is).selected
      have hcard : S.card ≤ a := by simpa using Finset.card_le_univ S
      have hg : (gramRun A S).operations ≤ a*a*(2*m) := by
        rw [gramRun_operations]
        gcongr
      have hd : (rationalDeterminantRun (view (gramRun A S).matrix)).operations ≤
          8*(a+1)^4 := by
        apply (rationalDeterminantRun_operations_le _).trans
        gcongr
      change (rowReductionRun A is).operations + (gramRun A S).operations +
        (rationalDeterminantRun (view (gramRun A S).matrix)).operations + 1 ≤ _
      simp only [List.length_cons]
      unfold rowReductionStepOperations at *
      nlinarith

theorem sumRun_rat_value_bits {B : ℕ} (xs : List (ScalarRun ℚ))
    (hx : ∀ x ∈ xs, RationalBits x.value B) :
    RationalBits (sumRun xs).value (1+xs.length*(B+1)) := by
  rw [sumRun_value]
  have hh : ∀ x ∈ xs.map ScalarRun.value, RationalBits x B := by
    intro x hx'
    obtain ⟨r, hr, rfl⟩ := List.mem_map.mp hx'
    exact hx r hr
  simpa only [List.length_map] using rationalBits_list_sum hh

theorem sumRun_rat_operands_bits {B K : ℕ} (xs : List (ScalarRun ℚ))
    (hv : ∀ x ∈ xs, RationalBits x.value B)
    (he : ∀ x ∈ xs, ∀ e ∈ x.operands, RationalBits e.1 K ∧ RationalBits e.2 K)
    (hBK : B ≤ K) (hL : 1 + xs.length * (B + 1) ≤ K) :
    ∀ e ∈ (sumRun xs).operands, RationalBits e.1 K ∧ RationalBits e.2 K := by
  induction xs with
  | nil => simp [sumRun, atom]
  | cons x xs ih =>
      have htail : 1+xs.length*(B+1) ≤ K := by
        simp only [List.length_cons] at hL
        nlinarith
      have hi := ih (fun y hy => hv y (by simp [hy]))
        (fun y hy => he y (by simp [hy])) htail
      have ht := sumRun_rat_value_bits xs (fun y hy => hv y (by simp [hy]))
      intro e hem
      simp only [sumRun, Elimination.add, List.mem_append, List.mem_singleton] at hem
      rcases hem with (hem | hem) | rfl
      · exact he x (by simp) e hem
      · exact hi e hem
      · exact ⟨rationalBits_mono (hv x (by simp)) hBK, rationalBits_mono ht htail⟩

theorem gramEntryRun_operands_bits {a m K : ℕ} {A : RationalRepresentation a m}
    (hA : MatrixBits A K) (S : Finset (Fin a)) (i j : Fin S.card) :
    ∀ e ∈ (gramEntryRun A S i j).operands,
      RationalBits e.1 (2*K+1+m*(2*K+1)) ∧ RationalBits e.2 (2*K+1+m*(2*K+1)) := by
  apply sumRun_rat_operands_bits (B := 2*K)
  · intro x hx
    obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hx
    simpa [mul, atom, two_mul] using rationalBits_mul (hA _ k) (hA _ k)
  · intro x hx e he
    obtain ⟨k, rfl⟩ := List.mem_ofFn.mp hx
    simp only [mul, atom, List.nil_append, List.mem_singleton] at he
    subst e
    exact ⟨rationalBits_mono (hA _ k) (by omega), rationalBits_mono (hA _ k) (by omega)⟩
  · omega
  · simp only [List.length_ofFn]
    omega

theorem gramRun_operands_bits {a m K : ℕ} {A : RationalRepresentation a m}
    (hA : MatrixBits A K) (S : Finset (Fin a)) :
    ∀ e ∈ (gramRun A S).operands,
      RationalBits e.1 (2*K+1+m*(2*K+1)) ∧ RationalBits e.2 (2*K+1+m*(2*K+1)) := by
  intro e he
  simp only [gramRun, Vector.getElem_ofFn] at he
  obtain ⟨_, hi, he⟩ := List.mem_flatten.mp he
  obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hi
  obtain ⟨_, hj, he⟩ := List.mem_flatten.mp he
  obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hj
  exact gramEntryRun_operands_bits hA S i j e he

def rowReductionRepresentation {a m : ℕ} (A : RationalRepresentation a m) :
    RationalRepresentation (rowReductionRun A (List.finRange a)).selected.card m :=
  A.submatrix (((rowReductionRun A (List.finRange a)).selected).orderEmbOfFin rfl) id

theorem rowReductionRun_rank {a m : ℕ} (A : RationalRepresentation a m) :
    (rowReductionRun A (List.finRange a)).selected.card = A.rank := by
  rw [rowReductionRun_selected]
  exact independentRows_card A

theorem rowReductionRepresentation_isBase_iff {a m : ℕ}
    (A : RationalRepresentation a m) (B : Finset (Fin m)) :
    IsBase (rowReductionRepresentation A) B ↔ IsColumnBase A B := by
  have hs : (rowReductionRun A (List.finRange a)).selected = independentRows A :=
    rowReductionRun_selected A _
  have he := congrArg (fun S : Finset (Fin a) =>
    IsBase (A.submatrix (S.orderEmbOfFin rfl) id) B) hs
  exact he.to_iff.trans (reducedRepresentation_isBase_iff A B)

theorem rowReductionRepresentation_bits {a m K : ℕ} {A : RationalRepresentation a m}
    (hA : MatrixBits A K) : MatrixBits (rowReductionRepresentation A) K :=
  fun _i j => hA _ j

theorem rowReductionRepresentation_independent {a m : ℕ} (A : RationalRepresentation a m) :
    LinearIndependent ℚ (rowReductionRepresentation A).row := by
  have hs : (rowReductionRun A (List.finRange a)).selected = independentRows A :=
    rowReductionRun_selected A _
  have he := congrArg (fun S : Finset (Fin a) =>
    LinearIndependent ℚ (A.submatrix (S.orderEmbOfFin rfl) id).row) hs
  exact he.mpr (reducedRepresentation_independent A)

end MatroidSpectral
