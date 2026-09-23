import Formal.MatroidSpectral.InterpolationTraceBits
import Formal.MatroidSpectral.Elimination

/-! Materialized rational evaluation of the weighted Gram matrix. Monomial
weights and all resulting matrix entries are computed once and stored. -/
namespace MatroidSpectral
open ReciprocalAnchor DAGSpectral Matrix
open scoped BigOperators

/-- Linear powering suffices because the degree budget is polynomial. -/
def profilePowerExpr (x : ℚ) (n : ℕ) : ArithmeticExpr :=
  prodExpr (List.replicate n (.atom x))

@[simp] lemma profilePowerExpr_eval (x : ℚ) (n : ℕ) :
    (profilePowerExpr x n).eval = x^n := by
  simp [profilePowerExpr, ArithmeticExpr.eval]

@[simp] lemma profilePowerExpr_operations (x : ℚ) (n : ℕ) :
    (profilePowerExpr x n).operations = n := by
  simp [profilePowerExpr, prodExpr_operations, ArithmeticExpr.operations]

lemma profilePowerExpr_bits {x : ℚ} {N : ℕ} (hx : RationalBits x N) (n : ℕ) :
    RationalBits (profilePowerExpr x n).eval (1+n*(N+1)) ∧
      ∀ e ∈ (profilePowerExpr x n).trace, eventBits (1+n*(N+1)) e := by
  simpa only [List.length_replicate, profilePowerExpr] using prodExpr_polynomial_bits
    (es := List.replicate n (.atom x))
    (by intro a ha; have := List.eq_of_mem_replicate ha; subst a; exact hx)
    (by intro a ha; have := List.eq_of_mem_replicate ha; subst a; simp [ArithmeticExpr.trace])

section Coordinates
variable {κ : Type*} [Fintype κ] [LinearOrder κ]

/-- The coordinate order is explicit, so the monomial calculation is executable. -/
def profileMonomialExpr (w : κ → ℕ) (t : κ → ℚ) : ArithmeticExpr :=
  prodExpr ((interpolationCoordinateList κ).map (fun i => profilePowerExpr (t i) (w i)))

lemma profileMonomialExpr_eval (w : κ → ℕ) (t : κ → ℚ) :
    (profileMonomialExpr w t).eval = ∏ i, t i ^ w i := by
  simp only [profileMonomialExpr, prodExpr_eval, List.map_map, Function.comp_def,
    profilePowerExpr_eval]
  exact (List.prod_toFinset _ (Finset.sort_nodup _ _)).symm.trans
    (by rw [Finset.sort_toFinset])

lemma profileMonomialExpr_operations (w : κ → ℕ) (t : κ → ℚ) :
    (profileMonomialExpr w t).operations = ∑ i, w i + Fintype.card κ := by
  simp only [profileMonomialExpr, prodExpr_operations, List.map_map, Function.comp_def,
    profilePowerExpr_operations, List.length_map, interpolationCoordinateList_length]
  congr 1
  exact (List.sum_toFinset _ (Finset.sort_nodup _ _)).symm.trans
    (by rw [Finset.sort_toFinset])

lemma profileMonomialExpr_operations_le (w : κ → ℕ) (t : κ → ℚ) (W : ℕ)
    (hw : ∀ i, w i ≤ W) :
    (profileMonomialExpr w t).operations ≤ Fintype.card κ*(W+1) := by
  rw [profileMonomialExpr_operations]
  have hh := Finset.sum_le_sum (s := Finset.univ) (fun i _ => hw i)
  simpa [Nat.mul_add] using Nat.add_le_add_right hh (Fintype.card κ)

def profileMonomialBits (d W N : ℕ) : ℕ := 1+d*(2+W*(N+1))

lemma profileMonomialExpr_bits (w : κ → ℕ) (t : κ → ℚ) (W N : ℕ)
    (hw : ∀ i, w i ≤ W) (ht : ∀ i, RationalBits (t i) N) :
    RationalBits (profileMonomialExpr w t).eval (profileMonomialBits (Fintype.card κ) W N) ∧
    ∀ e ∈ (profileMonomialExpr w t).trace,
      eventBits (profileMonomialBits (Fintype.card κ) W N) e := by
  have hh (i : κ) : RationalBits (profilePowerExpr (t i) (w i)).eval (1+W*(N+1)) ∧
      ∀ e ∈ (profilePowerExpr (t i) (w i)).trace, eventBits (1+W*(N+1)) e := by
    have hp := profilePowerExpr_bits (ht i) (w i)
    have hb : 1+w i*(N+1) ≤ 1+W*(N+1) := by gcongr; exact hw i
    exact ⟨rationalBits_mono hp.1 hb, fun e he => eventBits_mono (hp.2 e he) hb⟩
  have hp := prodExpr_polynomial_bits
    (es := (interpolationCoordinateList κ).map (fun i => profilePowerExpr (t i) (w i)))
    (by intro a ha; obtain ⟨i, _, rfl⟩ := List.mem_map.mp ha; exact (hh i).1)
    (by intro a ha; obtain ⟨i, _, rfl⟩ := List.mem_map.mp ha; exact (hh i).2)
  have heq : 1+((interpolationCoordinateList κ).map
      (fun i => profilePowerExpr (t i) (w i))).length*(1+W*(N+1)+1) =
      profileMonomialBits (Fintype.card κ) W N := by
    simp only [List.length_map, interpolationCoordinateList_length, profileMonomialBits]
    ring
  simpa only [heq, profileMonomialExpr] using hp

end Coordinates

/-- Read cached monomial weights to form one weighted inner product. -/
def profileGramEntryExpr {q m : ℕ} (A : Matrix (Fin q) (Fin m) ℚ)
    (weights : Fin m → ℚ) (i j : Fin q) : ArithmeticExpr :=
  sumExpr (List.ofFn (fun e : Fin m =>
    .op .mul (.op .mul (.atom (A i e)) (.atom (weights e))) (.atom (A j e))))

lemma profileGramEntryExpr_eval {q m : ℕ} (A : Matrix (Fin q) (Fin m) ℚ)
    (weights : Fin m → ℚ) (i j : Fin q) :
    (profileGramEntryExpr A weights i j).eval = ∑ e, A i e * weights e * A j e := by
  simp [profileGramEntryExpr, ArithmeticExpr.eval, primitiveResult,
    List.map_ofFn, Function.comp_def, List.sum_ofFn]

lemma profileGramEntryExpr_operations {q m : ℕ} (A : Matrix (Fin q) (Fin m) ℚ)
    (weights : Fin m → ℚ) (i j : Fin q) :
    (profileGramEntryExpr A weights i j).operations = 3*m := by
  simp [profileGramEntryExpr, sumExpr_operations, ArithmeticExpr.operations,
    List.map_ofFn, Function.comp_def]
  omega

def profileGramBits (m B C : ℕ) : ℕ := 1+m*(2*B+C+3)

lemma profileGramEntryExpr_bits {q m B C : ℕ} {A : Matrix (Fin q) (Fin m) ℚ}
    (hA : MatrixBits A B) (weights : Fin m → ℚ) (hw : ∀ e, RationalBits (weights e) C)
    (i j : Fin q) :
    RationalBits (profileGramEntryExpr A weights i j).eval (profileGramBits m B C) ∧
    ∀ e ∈ (profileGramEntryExpr A weights i j).trace, eventBits (profileGramBits m B C) e := by
  have hh (e : Fin m) :
      RationalBits (A i e * weights e * A j e) (2*B+C+2) :=
    rationalBits_mono (rationalBits_mul (rationalBits_mul (hA i e) (hw e)) (hA j e)) (by omega)
  have hv : ∀ a ∈ List.ofFn (fun e : Fin m =>
      ArithmeticExpr.op .mul (.op .mul (.atom (A i e)) (.atom (weights e))) (.atom (A j e))),
      RationalBits a.eval (2*B+C+2) := by
    intro a ha
    obtain ⟨e, rfl⟩ := List.mem_ofFn.mp ha
    exact hh e
  have ht : ∀ a ∈ List.ofFn (fun e : Fin m =>
      ArithmeticExpr.op .mul (.op .mul (.atom (A i e)) (.atom (weights e))) (.atom (A j e))),
      ∀ v ∈ a.trace, eventBits (2*B+C+2) v := by
    intro a ha v hv
    obtain ⟨e, rfl⟩ := List.mem_ofFn.mp ha
    simp only [ArithmeticExpr.trace, List.nil_append, List.append_nil,
      List.mem_append, List.mem_singleton] at hv
    rcases hv with rfl | rfl
    · exact ⟨rationalBits_mono (hA i e) (by omega), rationalBits_mono (hw e) (by omega)⟩
    · exact ⟨rationalBits_mono (rationalBits_mul (hA i e) (hw e)) (by omega),
        rationalBits_mono (hA j e) (by omega)⟩
  have hp := sumExpr_polynomial_bits hv ht
  simpa only [List.length_ofFn, profileGramBits, profileGramEntryExpr, Nat.add_assoc,
    show 2+1 = 3 from rfl] using hp

structure ProfileGramRun (q : ℕ) where
  matrix : Elimination.StoredMatrix ℚ q
  trace : List ArithmeticEvent

section Coordinates
variable {κ : Type*} [Fintype κ] [LinearOrder κ]

/-- Monomials are stored first, then each Gram entry is evaluated exactly once. -/
def profileGramRun {q m : ℕ} (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → κ → ℕ) (t : κ → ℚ) : ProfileGramRun q :=
  let weights := Vector.ofFn (fun e : Fin m => (profileMonomialExpr (w e) t).run)
  let cells := Vector.ofFn (fun i : Fin q => Vector.ofFn (fun j : Fin q =>
    (profileGramEntryExpr A (fun e => weights[e.val].1) i j).run))
  ⟨cells.map (fun row => row.map Prod.fst),
    (List.ofFn (fun e : Fin m => weights[e.val].2)).flatten ++
      (List.ofFn (fun i : Fin q =>
        (List.ofFn (fun j : Fin q => cells[i.val][j.val].2)).flatten)).flatten⟩

lemma profileGramRun_value {q m : ℕ} (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → κ → ℕ) (t : κ → ℚ) :
    Elimination.view (profileGramRun A w t).matrix =
      A * diagonal (fun e => ∏ i, t i ^ w e i) * A.transpose := by
  ext i j
  rw [Matrix.mul_apply]
  simp [Elimination.view, profileGramRun, ArithmeticExpr.run_eq,
    profileGramEntryExpr_eval, profileMonomialExpr_eval, Matrix.mul_diagonal]

lemma profileGramRun_trace_length_le {q m : ℕ} (A : Matrix (Fin q) (Fin m) ℚ)
    (w : Fin m → κ → ℕ) (t : κ → ℚ) (W : ℕ) (hw : ∀ e i, w e i ≤ W) :
    (profileGramRun A w t).trace.length ≤
      m*(Fintype.card κ*(W+1)) + q*q*(3*m) := by
  simp only [profileGramRun, Vector.getElem_ofFn, ArithmeticExpr.run_eq, List.length_append,
    List.length_flatten, List.map_ofFn, Function.comp_def, List.sum_ofFn,
    ArithmeticExpr.trace_length, profileGramEntryExpr_operations]
  have hh := Finset.sum_le_sum (s := Finset.univ)
    (fun e _ => profileMonomialExpr_operations_le (w e) t W (hw e))
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul] at *
  nlinarith

/-- One polynomial budget covers monomial and Gram arithmetic alike. -/
def profileGramExecutionBits (m d W B N : ℕ) : ℕ :=
  profileGramBits m B (profileMonomialBits d W N) + profileMonomialBits d W N + B+N+1

lemma profileGramRun_matrix_bits {q m B W N : ℕ} {A : Matrix (Fin q) (Fin m) ℚ}
    (hA : MatrixBits A B) (w : Fin m → κ → ℕ) (t : κ → ℚ)
    (hw : ∀ e i, w e i ≤ W) (ht : ∀ i, RationalBits (t i) N) :
    MatrixBits (Elimination.view (profileGramRun A w t).matrix)
      (profileGramBits m B (profileMonomialBits (Fintype.card κ) W N)) := by
  intro i j
  simp only [Elimination.view, profileGramRun, Vector.getElem_map, Vector.getElem_ofFn,
    ArithmeticExpr.run_eq]
  exact (profileGramEntryExpr_bits hA _
    (fun e => (profileMonomialExpr_bits (w e) t W N (hw e) ht).1) i j).1

lemma profileGramRun_trace_bits {q m B W N : ℕ} {A : Matrix (Fin q) (Fin m) ℚ}
    (hA : MatrixBits A B) (w : Fin m → κ → ℕ) (t : κ → ℚ)
    (hw : ∀ e i, w e i ≤ W) (ht : ∀ i, RationalBits (t i) N) :
    ∀ e ∈ (profileGramRun A w t).trace,
      eventBits (profileGramExecutionBits m (Fintype.card κ) W B N) e := by
  intro e he
  simp only [profileGramRun, Vector.getElem_ofFn, ArithmeticExpr.run_eq, List.mem_append] at he
  rcases he with he | he
  · obtain ⟨xs, hxs, he⟩ := List.mem_flatten.mp he
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hxs
    exact eventBits_mono ((profileMonomialExpr_bits (w j) t W N (hw j) ht).2 e he)
      (by unfold profileGramExecutionBits; omega)
  · obtain ⟨xs, hxs, he⟩ := List.mem_flatten.mp he
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hxs
    obtain ⟨ys, hys, he⟩ := List.mem_flatten.mp he
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hys
    exact eventBits_mono ((profileGramEntryExpr_bits hA _
      (fun l => (profileMonomialExpr_bits (w l) t W N (hw l) ht).1) i j).2 e he)
      (by unfold profileGramExecutionBits; omega)

lemma profileGramRun_bitWork {q m B W N : ℕ} {A : Matrix (Fin q) (Fin m) ℚ}
    (hA : MatrixBits A B) (w : Fin m → κ → ℕ) (t : κ → ℚ)
    (hw : ∀ e i, w e i ≤ W) (ht : ∀ i, RationalBits (t i) N) :
    traceBitWork (profileGramExecutionBits m (Fintype.card κ) W B N)
      (profileGramRun A w t).trace ≤
      (m*(Fintype.card κ*(W+1)) + q*q*(3*m))*
        (256*(profileGramExecutionBits m (Fintype.card κ) W B N+1)^3) := by
  exact (traceBitWork_le (profileGramRun_trace_bits hA w t hw ht)).trans
    (Nat.mul_le_mul_right _ (profileGramRun_trace_length_le A w t W hw))

end Coordinates
end MatroidSpectral
