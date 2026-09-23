import Formal.MatroidSpectral.RepresentationReduction
import Formal.MatroidSpectral.EliminationBits

/-! Executable row selection using the polynomial Bird determinant algorithm. -/
namespace MatroidSpectral
open Matrix
open scoped BigOperators

/-- Reindexing changes no determinant and uses only the selected input rows. -/
def rowGramFin {a m : ℕ} (A : RationalRepresentation a m) (S : Finset (Fin a)) :
    Matrix (Fin S.card) (Fin S.card) ℚ :=
  (rowGram A S).submatrix (S.orderIsoOfFin rfl) (S.orderIsoOfFin rfl)

theorem rowGramFin_det {a m : ℕ} (A : RationalRepresentation a m)
    (S : Finset (Fin a)) : (rowGramFin A S).det = (rowGram A S).det :=
  Matrix.det_submatrix_equiv_self (S.orderIsoOfFin rfl).toEquiv _

/-- Each determinant call executes cached integer Bird iterations. -/
def selectRowsExecuted {a m : ℕ} (A : RationalRepresentation a m) :
    List (Fin a) → Finset (Fin a)
  | [] => ∅
  | i :: is =>
      let S := selectRowsExecuted A is
      if Elimination.rationalDeterminant (rowGramFin A (insert i S)) ≠ 0 then insert i S else S

theorem selectRowsExecuted_correct {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) : selectRowsExecuted A rows = selectRows A rows := by
  induction rows with
  | nil => rfl
  | cons i is ih =>
      simp only [selectRowsExecuted, selectRows]
      rw [ih, Elimination.rationalDeterminant_correct, rowGramFin_det]

def independentRowsExecuted {a m : ℕ} (A : RationalRepresentation a m) :
    Finset (Fin a) := selectRowsExecuted A (List.finRange a)

theorem independentRowsExecuted_correct {a m : ℕ} (A : RationalRepresentation a m) :
    independentRowsExecuted A = independentRows A := selectRowsExecuted_correct A _

/-- Executed queries are captured at the same point at which the determinant is tested. -/
def rowSelectionRun {a m : ℕ} (A : RationalRepresentation a m) :
    List (Fin a) → Finset (Fin a) × List (Finset (Fin a))
  | [] => (∅, [])
  | i :: is =>
      let prior := rowSelectionRun A is
      let candidate := insert i prior.1
      let value := Elimination.rationalDeterminant (rowGramFin A candidate)
      (if value ≠ 0 then candidate else prior.1, prior.2 ++ [candidate])

theorem rowSelectionRun_result {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) : (rowSelectionRun A rows).1 = selectRowsExecuted A rows := by
  induction rows with
  | nil => rfl
  | cons i is ih =>
      simp only [rowSelectionRun, selectRowsExecuted]
      rw [ih]

theorem rowSelectionRun_queries {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) : (rowSelectionRun A rows).2 = rowQueries A rows := by
  induction rows with
  | nil => rfl
  | cons i is ih =>
      simp only [rowSelectionRun, rowQueries, ih, rowSelectionRun_result,
        selectRowsExecuted_correct]

theorem rowSelectionRun_query_count {a m : ℕ} (A : RationalRepresentation a m) :
    (rowSelectionRun A (List.finRange a)).2.length = a := by
  rw [rowSelectionRun_queries]
  exact independentRows_queries A

theorem rowSelectionRun_card {a m : ℕ} (A : RationalRepresentation a m) :
    (rowSelectionRun A (List.finRange a)).1.card = A.rank := by
  rw [rowSelectionRun_result, selectRowsExecuted_correct]
  exact independentRows_card A

theorem rowGramFin_bits {a m K : ℕ} {A : RationalRepresentation a m}
    (hA : DAGSpectral.MatrixBits A K) (S : Finset (Fin a)) :
    DAGSpectral.MatrixBits (rowGramFin A S) (1 + m * (K + K + 1)) := by
  intro i j
  simpa [rowGramFin, rowGram, rowRestriction, Matrix.submatrix, Matrix.mul_apply]
    using ReciprocalAnchor.rationalBits_finset_sum Finset.univ
    (fun k => A (S.orderEmbOfFin rfl i) k * A (S.orderEmbOfFin rfl j) k)
    (fun k _ => ReciprocalAnchor.rationalBits_mul (hA _ k) (hA _ k))

/-- Selecting rows does not increase any entry's rational encoding size. -/
theorem reducedRepresentation_bits {a m K : ℕ} {A : RationalRepresentation a m}
    (hA : DAGSpectral.MatrixBits A K) :
    DAGSpectral.MatrixBits (reducedRepresentation A) K := fun _i j => hA _ j

/-- The Bird-operation counter is evaluated on the exact row queries of the run. -/
def rowSelectionBirdOperations {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) : ℕ :=
  (((rowSelectionRun A rows).2).map (fun S =>
    (Elimination.determinantRun S.card
      (Elimination.store (integerMatrix (rowGramFin A S)))).operations)).sum

theorem rowSelectionBirdOperations_le {a m : ℕ} (A : RationalRepresentation a m)
    (rows : List (Fin a)) :
    rowSelectionBirdOperations A rows ≤ rows.length * (4 * (a + 1) ^ 4) := by
  unfold rowSelectionBirdOperations
  have hb (S : Finset (Fin a)) :
      (Elimination.determinantRun S.card
        (Elimination.store (integerMatrix (rowGramFin A S)))).operations ≤ 4 * (a + 1) ^ 4 := by
    apply (Elimination.determinantRun_operations_le _ _).trans
    have hs : S.card ≤ a := by simpa using Finset.card_le_univ S
    gcongr
  have hs : ∀ qs : List (Finset (Fin a)),
      (qs.map (fun S => (Elimination.determinantRun S.card
        (Elimination.store (integerMatrix (rowGramFin A S)))).operations)).sum ≤
        qs.length * (4 * (a + 1) ^ 4) := by
    intro qs
    induction qs with
    | nil => simp
    | cons S qs ih =>
        simp only [List.map_cons, List.sum_cons, List.length_cons]
        exact (Nat.add_le_add (hb S) ih).trans_eq (by ring)
  have h := hs (rowSelectionRun A rows).2
  simpa [rowSelectionRun_queries] using h

end MatroidSpectral
