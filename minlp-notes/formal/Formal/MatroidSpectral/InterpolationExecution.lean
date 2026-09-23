import Formal.MatroidSpectral.Interpolation
import Mathlib.Data.List.GetD
import Mathlib.Data.List.OfFn

namespace MatroidSpectral

open scoped BigOperators
open Polynomial

/-- Materialize each coefficient row before processing the next linear factor. -/
def interpolationNumeratorTable (D : ℕ) : List ℚ → List ℚ
  | [] => List.ofFn (fun k : Fin (D + 1) => if k.val = 0 then 1 else 0)
  | x :: xs =>
    let previous := interpolationNumeratorTable D xs
    List.ofFn (fun k : Fin (D + 1) =>
      (if k.val = 0 then 0 else previous.getD (k.val-1) 0) - x * previous.getD k.val 0)

theorem interpolationNumeratorTable_length (D : ℕ) (xs : List ℚ) :
    (interpolationNumeratorTable D xs).length = D+1 := by
  cases xs <;> simp [interpolationNumeratorTable]

theorem interpolationNumeratorTable_getD (D : ℕ) (xs : List ℚ) (k : ℕ)
    (hk : k ≤ D) :
    (interpolationNumeratorTable D xs).getD k 0 =
      ((xs.map (fun x => (X : ℚ[X]) - C x)).prod).coeff k := by
  induction xs generalizing k with
  | nil =>
    simp only [interpolationNumeratorTable, List.map_nil, List.prod_nil]
    rw [List.getD_eq_getElem _ _ (by simpa using Nat.lt_succ_of_le hk)]
    simp only [List.getElem_ofFn, Polynomial.coeff_one]
  | cons x xs ih =>
    simp only [interpolationNumeratorTable, List.map_cons, List.prod_cons]
    rw [List.getD_eq_getElem _ _ (by simpa using Nat.lt_succ_of_le hk)]
    simp only [List.getElem_ofFn, sub_mul, Polynomial.coeff_sub, Polynomial.coeff_C_mul]
    rw [ih k hk]
    cases k with
    | zero => simp
    | succ k =>
      simp only [Nat.add_eq_zero_iff, Nat.one_ne_zero, and_false, ↓reduceIte,
        Nat.add_sub_cancel, Polynomial.coeff_X_mul]
      exact congrArg (fun v => v - x * ((xs.map (fun x => X - C x)).prod).coeff (k+1))
        (ih k (by omega))

/-- The node list is explicit and independent of the input polynomial. -/
def interpolationOtherNodes (D : ℕ) (t : Fin (D + 1)) : List ℚ :=
  ((List.finRange (D + 1)).filter (fun j => j ≠ t)).map interpolationNode

def interpolationWeightRun (D : ℕ) (t : Fin (D + 1)) (k : ℕ) : ℚ :=
  let nodes := interpolationOtherNodes D t
  (interpolationNumeratorTable D nodes).getD k 0 /
    (nodes.map (fun x => interpolationNode t - x)).prod

theorem interpolationWeightRun_eq (D : ℕ) (t : Fin (D + 1)) (k : ℕ) (hk : k ≤ D) :
    interpolationWeightRun D t k = interpolationWeight D t k := by
  classical
  simp only [interpolationWeightRun]
  rw [interpolationNumeratorTable_getD D _ k hk]
  unfold interpolationWeight Lagrange.basis Lagrange.basisDivisor
  rw [Finset.prod_mul_distrib, ← map_prod, Finset.prod_inv_distrib, Polynomial.coeff_C_mul]
  have hp (f : ℚ → ℚ[X]) :
      ((interpolationOtherNodes D t).map f).prod =
        ∏ j ∈ Finset.univ.erase t, f (interpolationNode j) := by
    simp only [interpolationOtherNodes, List.map_map]
    rw [← List.prod_toFinset]
    · congr 1
      ext j
      simp
    · exact (List.nodup_finRange (D + 1)).filter _
  have hq (f : ℚ → ℚ) :
      ((interpolationOtherNodes D t).map f).prod =
        ∏ j ∈ Finset.univ.erase t, f (interpolationNode j) := by
    simp only [interpolationOtherNodes, List.map_map]
    rw [← List.prod_toFinset]
    · congr 1
      ext j
      simp
    · exact (List.nodup_finRange (D + 1)).filter _
  rw [hp, hq]
  rw [div_eq_mul_inv, mul_comm]

/-- An executable rational tensor solve. -/
def interpolateCoefficientRun {κ : Type*} [Fintype κ] [DecidableEq κ] (D : ℕ)
    (values : (κ → Fin (D + 1)) → ℚ) (z : κ → Fin (D + 1)) : ℚ :=
  ∑ t : κ → Fin (D + 1), values t * ∏ i, interpolationWeightRun D (t i) (z i).val

theorem interpolateCoefficientRun_eq {κ : Type*} [Fintype κ] [DecidableEq κ] (D : ℕ)
    (values : (κ → Fin (D + 1)) → ℚ) (z : κ → Fin (D + 1)) :
    interpolateCoefficientRun D values z =
      interpolateCoefficient D values (Finsupp.equivFunOnFinite.symm (fun i => (z i).val)) := by
  simp [interpolateCoefficientRun, interpolateCoefficient,
    interpolationWeightRun_eq D _ _ (Nat.le_of_lt_succ (z _).isLt)]

theorem interpolateCoefficientRun_eq_coeff {κ : Type*} [Fintype κ] [DecidableEq κ] (D : ℕ)
    (P : MvPolynomial κ ℚ)
    (hP : ∀ a ∈ P.support, ∀ i, a i ≤ D) (z : κ → Fin (D + 1)) :
    interpolateCoefficientRun D
      (fun t => MvPolynomial.eval (fun i => interpolationNode (t i)) P) z =
        P.coeff (Finsupp.equivFunOnFinite.symm (fun i => (z i).val)) := by
  rw [interpolateCoefficientRun_eq, interpolateCoefficient_eq_coeff D P hP]

end MatroidSpectral
