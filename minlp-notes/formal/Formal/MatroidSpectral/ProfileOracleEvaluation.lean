import Formal.MatroidSpectral.ProfileOracleExecution
import Formal.MatroidSpectral.ProfileGramExecution
import Formal.MatroidSpectral.EliminationBitExecution

namespace MatroidSpectral
open ReciprocalAnchor DAGSpectral

def profileEvaluationMatrixBits (m d W B N : ℕ) : ℕ :=
  profileGramBits m B (profileMonomialBits d W N)

def profileEvaluationBits (q m d W B N : ℕ) : ℕ :=
  polynomialDeterminantBits q (profileEvaluationMatrixBits m d W B N)

/-- Conservative list, matrix, trace, and identifier copying charges. Every
matrix and every monomial is materialized before later use. -/
def profileEvaluationStorage (q m d W B N : ℕ) : ℕ :=
  32 * (q + m + d + W + 1) ^ 6 * (profileGramExecutionBits m d W B N + 1)

def profileEvaluationWork (q m d W B N : ℕ) : ℕ :=
  (m * (d * (W + 1)) + q * q * (3 * m)) *
      (256 * (profileGramExecutionBits m d W B N + 1) ^ 3) +
    Elimination.determinantBitWork q (profileEvaluationMatrixBits m d W B N) +
    profileEvaluationStorage q m d W B N

section OrderedCoordinates
variable {κ : Type*} [Fintype κ] [LinearOrder κ]

/-- The concrete evaluation pipeline: cached monomials, a stored Gram matrix,
integer determinant execution, then exact rational reconstruction. -/
def profileEvaluationRun {q m : ℕ} (A : RationalRepresentation q m)
    (w : Fin m → κ → ℕ) (B W N : ℕ) (t : κ → ℚ) : ℚ × ℕ :=
  let gram := profileGramRun A w t
  let determinant := Elimination.determinantBitRun (Elimination.view gram.matrix)
  (determinant.1,
    traceBitWork (profileGramExecutionBits m (Fintype.card κ) W B N) gram.trace +
      determinant.2 + profileEvaluationStorage q m (Fintype.card κ) W B N)

theorem profileEvaluationRun_value {q m : ℕ} (A : RationalRepresentation q m)
    (w : Fin m → κ → ℕ) (B W N : ℕ) (t : κ → ℚ) :
    (profileEvaluationRun A w B W N t).1 = profileDeterminantValue A w t := by
  simp only [profileEvaluationRun, Elimination.determinantBitRun_value,
    profileGramRun_value, profileDeterminantValue, Elimination.rationalDeterminant_correct]

theorem profileEvaluationRun_bits {q m B W N : ℕ} {A : RationalRepresentation q m}
    (hA : MatrixBits A B) (w : Fin m → κ → ℕ) (t : κ → ℚ)
    (hw : ∀ e i, w e i ≤ W) (ht : ∀ i, RationalBits (t i) N) :
    RationalBits (profileEvaluationRun A w B W N t).1
      (profileEvaluationBits q m (Fintype.card κ) W B N) := by
  simp only [profileEvaluationRun, Elimination.determinantBitRun_value]
  exact matrixBits_det_polynomial (profileGramRun_matrix_bits hA w t hw ht)

theorem profileEvaluationRun_work {q m B W N : ℕ} {A : RationalRepresentation q m}
    (hA : MatrixBits A B) (w : Fin m → κ → ℕ) (t : κ → ℚ)
    (hw : ∀ e i, w e i ≤ W) (ht : ∀ i, RationalBits (t i) N) :
    (profileEvaluationRun A w B W N t).2 ≤
      profileEvaluationWork q m (Fintype.card κ) W B N := by
  exact Nat.add_le_add_right (Nat.add_le_add (profileGramRun_bitWork hA w t hw ht)
    (Elimination.determinantBitRun_work (profileGramRun_matrix_bits hA w t hw ht))) _

theorem zeroColumns_bits {q m B : ℕ} {A : RationalRepresentation q m}
    (hA : MatrixBits A B) (retained : Finset (Fin m)) :
    MatrixBits (zeroColumns A retained) (B + 1) := by
  intro i e
  by_cases he : e ∈ retained
  · exact rationalBits_mono (by simpa only [zeroColumns, if_pos he] using hA i e) (by omega)
  · simp only [zeroColumns, if_neg he]
    exact rationalBits_mono rationalBits_zero (by omega)

def profileOracleRestrictionWork (q m B : ℕ) : ℕ :=
  8 * (q + 1) ^ 2 * (m + 1) ^ 2 * (B + Nat.size m + 1)

def oracleRepresentationStore {q m : ℕ} (A : RationalRepresentation q m) :
    Vector (Vector ℚ m) q := Vector.ofFn (fun i => Vector.ofFn (A i))

def oracleRepresentationView {q m : ℕ} (rows : Vector (Vector ℚ m) q) :
    RationalRepresentation q m := fun i e => rows[i.val][e.val]

@[simp] theorem oracleRepresentationView_store {q m : ℕ} (A : RationalRepresentation q m) :
    oracleRepresentationView (oracleRepresentationStore A) = A := by
  ext i e
  simp [oracleRepresentationView, oracleRepresentationStore]

def profileCoefficientQueryRun {q m : ℕ} (A : RationalRepresentation q m)
    (w : Fin m → κ → ℕ) (D W B : ℕ) (z : κ → Fin (D + 1))
    (retained : Finset (Fin m)) : Bool × ℕ :=
  let rows := oracleRepresentationStore (zeroColumns A retained)
  let run := coefficientQueryRun D
    (profileEvaluationBits q m (Fintype.card κ) W (B + 1) (D + 2))
    (fun t => profileEvaluationRun (oracleRepresentationView rows) w (B + 1) W (D + 2)
      (fun i => interpolationNode (t i))) z
  (run.1, run.2 + profileOracleRestrictionWork q m B)

theorem profileCoefficientQueryRun_value {q m : ℕ} (A : RationalRepresentation q m)
    (w : Fin m → κ → ℕ) (D W B : ℕ) (z : κ → Fin (D + 1))
    (retained : Finset (Fin m)) :
    (profileCoefficientQueryRun A w D W B z retained).1 =
      profileCoefficientOracle A w D z retained := by
  simp only [profileCoefficientQueryRun, coefficientQueryRun_value,
    oracleRepresentationView_store, profileEvaluationRun_value, profileCoefficientOracle]

def profileCoefficientQueryWork (q m d D W B : ℕ) : ℕ :=
  coefficientQueryWork d D
    (profileEvaluationBits q m d W (B + 1) (D + 2))
    (profileEvaluationWork q m d W (B + 1) (D + 2)) +
    profileOracleRestrictionWork q m B

theorem profileCoefficientQueryRun_work {q m B W : ℕ} {A : RationalRepresentation q m}
    (hA : MatrixBits A B) (w : Fin m → κ → ℕ) (hw : ∀ e i, w e i ≤ W)
    (D : ℕ) (z : κ → Fin (D + 1)) (retained : Finset (Fin m)) :
    (profileCoefficientQueryRun A w D W B z retained).2 ≤
      profileCoefficientQueryWork q m (Fintype.card κ) D W B := by
  simp only [profileCoefficientQueryRun, oracleRepresentationView_store]
  apply Nat.add_le_add_right
  apply coefficientQueryRun_work
  · intro t
    exact profileEvaluationRun_bits (zeroColumns_bits hA retained) w _ hw
      (fun i => (interpolationNode_integralBound (t i)).bits)
  · intro t
    exact profileEvaluationRun_work (zeroColumns_bits hA retained) w _ hw
      (fun i => (interpolationNode_integralBound (t i)).bits)

end OrderedCoordinates
end MatroidSpectral
