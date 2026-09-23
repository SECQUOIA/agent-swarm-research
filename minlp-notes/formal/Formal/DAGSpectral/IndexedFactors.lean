import Formal.DAGSpectral.LabeledFactors
import Mathlib.Algebra.BigOperators.Fin

/-! Executable indexing of all LDL labels, ordered first by owner and then by
position in that owner's factor list. No arbitrary finite equivalence is used. -/
namespace DAGSpectral
open scoped BigOperators
variable {n m : ℕ}

def indexedFactorCount (A : Fin m → Matrix (Fin n) (Fin n) ℚ) : ℕ :=
  ∑ o, (rationalLDL n (A o)).length

def indexedFactorEquiv (A : Fin m → Matrix (Fin n) (Fin n) ℚ) :
    FactorLabel A ≃ Fin (indexedFactorCount A) := finSigmaFinEquiv

def indexedFactorOwner (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : Fin (indexedFactorCount A)) : Fin m := factorOwner ((indexedFactorEquiv A).symm k)

def indexedFactorWeight (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : Fin (indexedFactorCount A)) : ℚ := factorWeight A ((indexedFactorEquiv A).symm k)

def indexedFactorVector (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : Fin (indexedFactorCount A)) : Fin n → ℚ :=
  factorVector A ((indexedFactorEquiv A).symm k)

/-- The integer label is the sum of preceding list lengths plus the local index. -/
theorem indexedFactorEquiv_apply (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : FactorLabel A) :
    (indexedFactorEquiv A k : ℕ) =
      (∑ i : Fin k.1, (rationalLDL n (A (Fin.castLE k.1.2.le i))).length) + k.2 :=
  finSigmaFinEquiv_apply k

@[simp] theorem indexedFactorOwner_equiv (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : FactorLabel A) : indexedFactorOwner A (indexedFactorEquiv A k) = k.1 := by
  simp [indexedFactorOwner, factorOwner]

@[simp] theorem indexedFactorWeight_equiv (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : FactorLabel A) : indexedFactorWeight A (indexedFactorEquiv A k) = factorWeight A k := by
  simp [indexedFactorWeight]

@[simp] theorem indexedFactorVector_equiv (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : FactorLabel A) : indexedFactorVector A (indexedFactorEquiv A k) = factorVector A k := by
  simp [indexedFactorVector]

theorem indexedFactorCount_le (A : Fin m → Matrix (Fin n) (Fin n) ℚ) :
    indexedFactorCount A ≤ n*m := by
  unfold indexedFactorCount
  calc
    ∑ o, (rationalLDL n (A o)).length ≤ ∑ _o : Fin m, n :=
      Finset.sum_le_sum (fun o _ => rationalLDL_length_le n (A o))
    _ = _ := by simp [Nat.mul_comm]

theorem indexedFactor_positive (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (k : Fin (indexedFactorCount A)) :
    0 < indexedFactorWeight A k ∧ indexedFactorVector A k ≠ 0 :=
  factorLabel_positive A hA ((indexedFactorEquiv A).symm k)

theorem indexedFactor_owner_reconstruct (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (o : Fin m) (i j : Fin n) :
    A o i j = ∑ k : Fin (indexedFactorCount A),
      if indexedFactorOwner A k = o then
        indexedFactorWeight A k * indexedFactorVector A k i * indexedFactorVector A k j
      else 0 := by
  have he := Equiv.sum_comp (indexedFactorEquiv A).symm
    (fun k : FactorLabel A => if factorOwner k = o then
      factorWeight A k * factorVector A k i * factorVector A k j else 0)
  rw [show (∑ k : Fin (indexedFactorCount A),
      if indexedFactorOwner A k = o then
        indexedFactorWeight A k * indexedFactorVector A k i * indexedFactorVector A k j
      else 0) = _ from he]
  exact factorLabel_owner_reconstruct A hA o i j

theorem indexedFactor_selected_reconstruct (A : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (hA : ∀ o, (ratMatrixReal (A o)).PosSemidef) (s : Finset (Fin m)) (i j : Fin n) :
    (∑ o ∈ s, A o i j) = ∑ k : Fin (indexedFactorCount A),
      if indexedFactorOwner A k ∈ s then
        indexedFactorWeight A k * indexedFactorVector A k i * indexedFactorVector A k j
      else 0 := by
  have he := Equiv.sum_comp (indexedFactorEquiv A).symm
    (fun k : FactorLabel A => if factorOwner k ∈ s then
      factorWeight A k * factorVector A k i * factorVector A k j else 0)
  rw [show (∑ k : Fin (indexedFactorCount A),
      if indexedFactorOwner A k ∈ s then
        indexedFactorWeight A k * indexedFactorVector A k i * indexedFactorVector A k j
      else 0) = _ from he]
  exact factorLabel_selected_reconstruct A hA s i j

/-- Prior is owner zero; atom `e` is owner `e.succ`. -/
def priorAtomMatrices (Q0 : Matrix (Fin n) (Fin n) ℚ)
    (Q : Fin m → Matrix (Fin n) (Fin n) ℚ) : Fin (m+1) → Matrix (Fin n) (Fin n) ℚ :=
  Fin.cases Q0 Q

@[simp] theorem priorAtomMatrices_zero (Q0 : Matrix (Fin n) (Fin n) ℚ)
    (Q : Fin m → Matrix (Fin n) (Fin n) ℚ) : priorAtomMatrices Q0 Q 0 = Q0 := rfl

@[simp] theorem priorAtomMatrices_succ (Q0 : Matrix (Fin n) (Fin n) ℚ)
    (Q : Fin m → Matrix (Fin n) (Fin n) ℚ) (e : Fin m) :
    priorAtomMatrices Q0 Q e.succ = Q e := rfl

def indexedPriorAtomOwner (Q0 : Matrix (Fin n) (Fin n) ℚ)
    (Q : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : Fin (indexedFactorCount (priorAtomMatrices Q0 Q))) : Option (Fin m) :=
  Fin.cases none some (indexedFactorOwner (priorAtomMatrices Q0 Q) k)

theorem indexedPriorAtomCount_le (Q0 : Matrix (Fin n) (Fin n) ℚ)
    (Q : Fin m → Matrix (Fin n) (Fin n) ℚ) :
    indexedFactorCount (priorAtomMatrices Q0 Q) ≤ n*(m+1) := indexedFactorCount_le _

theorem indexedFactor_owner_card (A : Fin m → Matrix (Fin n) (Fin n) ℚ) (o : Fin m) :
    (Finset.univ.filter (fun k : Fin (indexedFactorCount A) => indexedFactorOwner A k = o)).card =
      (rationalLDL n (A o)).length := by
  classical
  calc
    _ = ∑ k : Fin (indexedFactorCount A), if indexedFactorOwner A k = o then 1 else 0 := by simp
    _ = ∑ k : FactorLabel A, if k.1 = o then 1 else 0 :=
      Equiv.sum_comp (indexedFactorEquiv A).symm (fun k : FactorLabel A => if k.1 = o then 1 else 0)
    _ = _ := by
      rw [Fintype.sum_sigma]
      have hs (o' : Fin m) : (∑ _k : Fin (rationalLDL n (A o')).length,
          if o'=o then 1 else 0) = if o'=o then (rationalLDL n (A o')).length else 0 := by
        split_ifs <;> simp
      simp_rw [hs]
      simp

def priorOwnerIndex (o : Option (Fin m)) : Fin (m+1) := o.elim 0 Fin.succ

theorem indexedPriorAtomOwner_eq_iff (Q0 : Matrix (Fin n) (Fin n) ℚ)
    (Q : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (k : Fin (indexedFactorCount (priorAtomMatrices Q0 Q))) (o : Option (Fin m)) :
    indexedPriorAtomOwner Q0 Q k = o ↔
      indexedFactorOwner (priorAtomMatrices Q0 Q) k = priorOwnerIndex o := by
  unfold indexedPriorAtomOwner
  generalize indexedFactorOwner (priorAtomMatrices Q0 Q) k = j
  cases j using Fin.cases <;> cases o <;> simp [priorOwnerIndex, Fin.succ_ne_zero, eq_comm]

theorem indexedPriorAtom_owner_reconstruct (Q0 : Matrix (Fin n) (Fin n) ℚ)
    (Q : Fin m → Matrix (Fin n) (Fin n) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (o : Option (Fin m)) (i j : Fin n) :
    (o.elim Q0 Q) i j = ∑ k : Fin (indexedFactorCount (priorAtomMatrices Q0 Q)),
      if indexedPriorAtomOwner Q0 Q k = o then
        indexedFactorWeight (priorAtomMatrices Q0 Q) k *
          indexedFactorVector (priorAtomMatrices Q0 Q) k i *
          indexedFactorVector (priorAtomMatrices Q0 Q) k j else 0 := by
  have hA : ∀ o', (ratMatrixReal (priorAtomMatrices Q0 Q o')).PosSemidef := by
    intro o'
    cases o' using Fin.cases
    · exact hQ0
    · exact hQ _
  have he := indexedFactor_owner_reconstruct (priorAtomMatrices Q0 Q) hA (priorOwnerIndex o) i j
  simp_rw [indexedPriorAtomOwner_eq_iff]
  convert he using 1
  cases o <;> rfl

theorem indexedPriorAtom_owner_card_le (Q0 : Matrix (Fin n) (Fin n) ℚ)
    (Q : Fin m → Matrix (Fin n) (Fin n) ℚ) (o : Option (Fin m)) :
    (Finset.univ.filter (fun k : Fin (indexedFactorCount (priorAtomMatrices Q0 Q)) =>
      indexedPriorAtomOwner Q0 Q k = o)).card ≤ n := by
  simp_rw [indexedPriorAtomOwner_eq_iff]
  rw [indexedFactor_owner_card]
  exact rationalLDL_length_le _ _

end DAGSpectral
