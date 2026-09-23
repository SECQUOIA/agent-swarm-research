import Formal.MultilinearGap.StructuralFeedbackUniversal
import Formal.MultilinearGap.StructuralFeedbackRepair

/-! Composition of the universal law with residual repair. -/
namespace MultilinearGap.StructuralFeedback
open CubicGap
noncomputable section
variable {J : Type*} [Fintype J] [DecidableEq J]

theorem map_equiv_weight {A B : Type*} [Fintype A] [Fintype B]
    (P : Law A) (e : A ≃ B) (b : B) : (P.map e).weight b = P.weight (e.symm b) := by
  classical
  simp [Law.map, ← e.eq_symm_apply]

theorem feedbackMass_eq_expect {S : Type*} [Fintype S] [DecidableEq S]
    (P : Law (S × Vertex J)) (s : S) :
    feedbackMass P s = P.expect (fun z => if z.1 = s then 1 else 0) := by
  simp only [Law.expect, Fintype.sum_prod_type, mul_ite, mul_one, mul_zero]
  rw [Finset.sum_comm]
  simp [feedbackMass]

theorem pairMass_eq_expect {S : Type*} [Fintype S] [DecidableEq S]
    (P : Law (S × Vertex J)) (i : J) (s : S) (b : Bool) :
    pairMass P i s b = P.expect (fun z => if z.1 = s ∧ z.2 i = b then 1 else 0) := by
  simp [Law.expect, Fintype.sum_prod_type, mul_ite, pairMass, ite_and]

section Arbitrary
variable {I : Type*} [Fintype I] [DecidableEq I]

/-- Split coordinates at an arbitrary feedback set, retaining their names. -/
def splitAt (A : Finset I) : Vertex I ≃ Vertex {j // j ∈ A} × Vertex {j // j ∉ A} where
  toFun v := (fun j => v j.1, fun j => v j.1)
  invFun z j := if h : j ∈ A then z.1 ⟨j, h⟩ else z.2 ⟨j, h⟩
  left_inv v := by funext j; dsimp; split_ifs <;> rfl
  right_inv z := by
    apply Prod.ext <;> funext j
    · simp [j.2]
    · simp [j.2]

theorem feedbackMass_splitAt (A : Finset I) (P : Law (Vertex I)) (s : Vertex I) :
    feedbackMass (P.map (splitAt A)) (fun j => s j.1) = feedbackCellMass P A s := by
  rw [feedbackMass_eq_expect, Law.expect_map]
  unfold feedbackCellMass
  apply congrArg P.expect
  funext v
  rw [feedbackCell_eq_indicator]
  change (if (fun j : {j // j ∈ A} => v j.1) = (fun j => s j.1) then 1 else 0) = _
  congr 1
  apply propext
  constructor
  · intro h j hj
    exact congrFun h ⟨j, hj⟩
  · intro h
    funext j
    exact h j.1 j.2

theorem pairMass_splitAt (A : Finset I) (P : Law (Vertex I)) (s : Vertex I)
    (i : {j // j ∉ A}) :
    pairMass (P.map (splitAt A)) i (fun j => s j.1) (s i.1) =
      feedbackCellMass P (insert i.1 A) s := by
  rw [pairMass_eq_expect, Law.expect_map]
  unfold feedbackCellMass
  apply congrArg P.expect
  funext v
  rw [feedbackCell_eq_indicator]
  change (if (fun j : {j // j ∈ A} => v j.1) = (fun j => s j.1) ∧ v i.1 = s i.1
    then 1 else 0) = _
  congr 1
  apply propext
  constructor
  · rintro ⟨h, hi⟩ j hj
    rcases Finset.mem_insert.mp hj with rfl | hj
    · exact hi
    · exact congrFun h ⟨j, hj⟩
  · intro h
    refine ⟨?_, h i.1 (Finset.mem_insert_self _ _)⟩
    funext j
    exact h j.1 (Finset.mem_insert_of_mem j.2)

theorem law_eq_of_weights {Ω : Type*} [Fintype Ω] (P Q : Law Ω)
    (h : ∀ z, P.weight z = Q.weight z) : P = Q := by
  cases P
  cases Q
  simp_all only [Law.mk.injEq]
  exact funext h

theorem map_equiv_cancel {A B : Type*} [Fintype A] [Fintype B]
    (P : Law A) (e : A ≃ B) : (P.map e).map e.symm = P := by
  apply law_eq_of_weights
  intro a
  simp only [map_equiv_weight, Equiv.symm_symm, Equiv.symm_apply_apply]

/-- Complete local repair on the original coordinate type. All feedback and
feedback-plus-one-coordinate marginals agree with the same universal target. -/
theorem exists_local_repair (A : Finset I) (x : I → ℝ)
    (P : Law (Vertex I)) (hP : HasMeans P x) :
    ∃ R : Law (Vertex I),
      (∀ v, (1 / 2 : ℝ) ^ A.card * P.weight v ≤ R.weight v) ∧
      (∀ s, feedbackCellMass R A s = feedbackCellMass (feedbackUniversalLaw A x) A s) ∧
      ∀ i s, feedbackCellMass R (insert i A) s =
        feedbackCellMass (feedbackUniversalLaw A x) (insert i A) s := by
  let e := splitAt A
  let Q := feedbackUniversalLaw A x
  have hdomF (s : Vertex {j // j ∈ A}) :
      (1 / 2 : ℝ) ^ A.card * feedbackMass (P.map e) s ≤ feedbackMass (Q.map e) s := by
    let v : Vertex I := e.symm (s, fun _ => false)
    have hv : (fun j : {j // j ∈ A} => v j.1) = s := by funext j; simp [v, e, splitAt, j.2]
    rw [← hv, feedbackMass_splitAt, feedbackMass_splitAt]
    exact feedbackUniversalLaw_dominates_feedback A x P hP v
  have hdompair (i : {j // j ∉ A}) (s : Vertex {j // j ∈ A}) (b : Bool) :
      (1 / 2 : ℝ) ^ A.card * pairMass (P.map e) i s b ≤ pairMass (Q.map e) i s b := by
    let v : Vertex I := e.symm (s, fun _ => b)
    have hv : (fun j : {j // j ∈ A} => v j.1) = s := by funext j; simp [v, e, splitAt, j.2]
    have hi : v i.1 = b := by simp [v, e, splitAt, i.2]
    rw [← hv, ← hi, pairMass_splitAt, pairMass_splitAt]
    exact feedbackUniversalLaw_dominates_pair A x P hP v i.1
  obtain ⟨R, hweight, hfeedback, hpair⟩ := exists_repaired_law_to_target
    (P.map e) (Q.map e) ((1 / 2 : ℝ) ^ A.card)
    (pow_nonneg (by norm_num) _) hdomF hdompair
  have hcancel : (R.map e.symm).map e = R := by
    simpa only [Equiv.symm_symm] using map_equiv_cancel R e.symm
  refine ⟨R.map e.symm, ?_, ?_, ?_⟩
  · intro v
    rw [map_equiv_weight]
    have h := hweight (e v)
    simpa only [map_equiv_weight, Equiv.symm_apply_apply, Equiv.symm_symm] using h
  · intro s
    rw [← feedbackMass_splitAt A _ s, ← feedbackMass_splitAt A Q s]
    change feedbackMass ((R.map e.symm).map e) _ = _
    rw [hcancel]
    exact hfeedback _
  · intro i s
    by_cases hi : i ∈ A
    · rw [Finset.insert_eq_of_mem hi]
      rw [← feedbackMass_splitAt A _ s, ← feedbackMass_splitAt A Q s]
      change feedbackMass ((R.map e.symm).map e) _ = _
      rw [hcancel]
      exact hfeedback _
    · rw [← pairMass_splitAt A _ s ⟨i, hi⟩, ← pairMass_splitAt A Q s ⟨i, hi⟩]
      change pairMass ((R.map e.symm).map e) _ _ _ = _
      rw [hcancel]
      exact hpair _ _ _

end Arbitrary
end
end MultilinearGap.StructuralFeedback
