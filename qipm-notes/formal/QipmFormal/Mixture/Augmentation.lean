import QipmFormal.Mixture.Defs

/-!
# Right-hand-side augmentation and inequality slacks

The homogeneous augmentation appends a coordinate equal to one. Slack conversion
requires a height bound on the selected slack coordinates as well as the primal
coordinates. Locality below follows from actual updates of the designated input.
-/

namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators
variable {R C I V : Type*}

/-- Homogenize the right-hand side by appending the column `-b`. -/
def rhsMatrix (A : R → C → ℝ) (b : R → ℝ) : R → Option C → ℝ :=
  fun r j => match j with | none => -b r | some c => A r c

/-- The appended witness coordinate is one. -/
def rhsWitness (x : C → ℝ) : Option C → ℝ :=
  fun j => match j with | none => 1 | some c => x c

theorem rhs_residual [Fintype C] (A : R → C → ℝ) (b : R → ℝ) (x : C → ℝ) :
    residual (rhsMatrix A b) (rhsWitness x) 0 = residual A x b := by
  funext r
  simp [residual, Fintype.sum_option, rhsMatrix, rhsWitness]
  ring

theorem rhsWitness_nonnegative (x : C → ℝ) (hx : ∀ j, 0 ≤ x j) :
    ∀ j, 0 ≤ rhsWitness x j := by
  intro j
  cases j <;> simp [rhsWitness, hx]

theorem rhsWitness_height (x : C → ℝ) (H : ℝ) (hx : ∀ j, |x j| ≤ H) :
    ∀ j, |rhsWitness x j| ≤ max H 1 := by
  intro j
  cases j with
  | none => simp [rhsWitness]
  | some j => exact (hx j).trans (le_max_left _ _)

theorem rhsMatrix_bound (A : R → C → ℝ) (b : R → ℝ) (B : ℝ)
    (hA : ∀ r j, |A r j| ≤ B) (hb : ∀ r, |b r| ≤ B) :
    ∀ r j, |rhsMatrix A b r j| ≤ B := by
  intro r j
  cases j <;> simp [rhsMatrix, hA, hb]

/-- The number of nonzero coefficients in a finite row. -/
def rowSupportCount [Fintype C] (a : C → ℝ) : ℕ :=
  ∑ j, if a j = 0 then 0 else 1

theorem rowSupportCount_eq_card [Fintype C] (a : C → ℝ) :
    rowSupportCount a = (Finset.univ.filter fun j => a j ≠ 0).card := by
  classical
  rw [Finset.card_eq_sum_ones, Finset.sum_filter]
  unfold rowSupportCount
  apply Finset.sum_congr rfl
  intro j hj
  split_ifs <;> simp_all

theorem rhsMatrix_supportCount [Fintype C] (A : R → C → ℝ) (b : R → ℝ) (r : R) :
    rowSupportCount (rhsMatrix A b r) =
      rowSupportCount (A r) + if b r = 0 then 0 else 1 := by
  simp only [rowSupportCount, Fintype.sum_option, rhsMatrix, neg_eq_zero]
  rw [add_comm]
  congr 1

theorem rhsMatrix_sparsity [Fintype C] (A : R → C → ℝ) (b : R → ℝ) (s : ℕ)
    (hs : ∀ r, rowSupportCount (A r) ≤ s) :
    ∀ r, rowSupportCount (rhsMatrix A b r) ≤ s + 1 := by
  intro r
  rw [rhsMatrix_supportCount]
  split_ifs <;> have := hs r <;> omega

theorem rhsWitness_mix [Fintype I] (w : I → ℝ) (hw : ProbWeights w)
    (x : I → C → ℝ) : mix w (fun i => rhsWitness (x i)) = rhsWitness (mix w x) := by
  funext j
  cases j with
  | none => simpa [mix, rhsWitness] using hw.2
  | some j => rfl

/-- Add nonnegative slacks for inequalities `A x ≤ b`. -/
def slackMatrix [DecidableEq R] (A : R → C → ℝ) : R → C ⊕ R → ℝ :=
  fun r j => match j with | Sum.inl c => A r c | Sum.inr q => if r = q then 1 else 0

def slackWitness (x : C → ℝ) (z : R → ℝ) : C ⊕ R → ℝ := Sum.elim x z

theorem slack_residual [Fintype C] [Fintype R] [DecidableEq R]
    (A : R → C → ℝ) (b z : R → ℝ) (x : C → ℝ) (r : R) :
    residual (slackMatrix A) (slackWitness x z) b r = residual A x b r + z r := by
  simp [residual, Fintype.sum_sum_type, slackMatrix, slackWitness]
  ring

theorem slack_conversion [Fintype C] [Fintype R] [DecidableEq R]
    (A : R → C → ℝ) (b : R → ℝ) (x : C → ℝ)
    (hx : ∀ c, 0 ≤ x c) (hineq : ∀ r, ∑ c, A r c * x c ≤ b r) :
    let z := fun r => b r - ∑ c, A r c * x c
    (∀ j, 0 ≤ slackWitness x z j) ∧
      residual (slackMatrix A) (slackWitness x z) b = 0 := by
  dsimp only
  constructor
  · intro j
    cases j with
    | inl c => exact hx c
    | inr r => exact sub_nonneg.mpr (hineq r)
  · funext r
    rw [slack_residual]
    simp [residual]

theorem slackWitness_height (x : C → ℝ) (z : R → ℝ) (H : ℝ)
    (hx : ∀ c, |x c| ≤ H) (hz : ∀ r, |z r| ≤ H) :
    ∀ j, |slackWitness x z j| ≤ H := by
  intro j
  cases j with
  | inl c => exact hx c
  | inr r => exact hz r

theorem slackMatrix_bound [DecidableEq R] (A : R → C → ℝ) (B : ℝ)
    (hA : ∀ r j, |A r j| ≤ B) :
    ∀ r j, |slackMatrix A r j| ≤ max B 1 := by
  intro r j
  cases j with
  | inl c => exact (hA r c).trans (le_max_left _ _)
  | inr q =>
    simp only [slackMatrix]
    split_ifs <;> simp only [abs_one, abs_zero]
    · exact le_max_right _ _
    · exact (by norm_num : (0 : ℝ) ≤ 1).trans (le_max_right _ _)

theorem slackMatrix_supportCount [Fintype C] [Fintype R] [DecidableEq R]
    (A : R → C → ℝ) (r : R) :
    rowSupportCount (slackMatrix A r) = rowSupportCount (A r) + 1 := by
  classical
  simp only [rowSupportCount, Fintype.sum_sum_type, slackMatrix]
  simp
  congr 1

/-- A raw coefficient is public or is a function of its designated input bit. -/
def oneBitMatrix [DecidableEq C] (D : R → Finset C) (label : R → C → I)
    (fixed : R → C → ℝ) (value : R → C → V → ℝ) (input : I → V) : R → C → ℝ :=
  fun r j => if j ∈ D r then value r j (input (label r j)) else fixed r j

/-- Updating one input leaves every public or differently labelled coefficient fixed. -/
theorem oneBitMatrix_update_locality [DecidableEq C] [DecidableEq I]
    (D : R → Finset C) (label : R → C → I) (fixed : R → C → ℝ)
    (value : R → C → V → ℝ) (input : I → V) (replacement : I → V) :
    ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      oneBitMatrix D label fixed value (Function.update input i (replacement i)) r j =
        oneBitMatrix D label fixed value input r j := by
  intro i r j h
  rcases h with h | h
  · simp [oneBitMatrix, h]
  · simp [oneBitMatrix, Function.update_of_ne h]

/-- Dependent positions include the extra column precisely for dependent RHS rows. -/
def rhsDependent [DecidableEq C] (D : R → Finset C) (rhsDep : R → Bool) :
    R → Finset (Option C) :=
  fun r => if rhsDep r then insert none ((D r).image some) else (D r).image some

def rhsLabel (label : R → C → I) (rhsLabel : R → I) : R → Option C → I :=
  fun r j => match j with | none => rhsLabel r | some c => label r c

theorem rhsDependent_card [DecidableEq C] (D : R → Finset C) (rhsDep : R → Bool)
    (r : R) :
    (rhsDependent D rhsDep r).card = (D r).card + if rhsDep r then 1 else 0 := by
  classical
  simp only [rhsDependent]
  split_ifs <;> simp [Finset.card_image_of_injective, Option.some_injective]

theorem rhsDependent_sparsity [DecidableEq C] (D : R → Finset C) (rhsDep : R → Bool)
    (s : ℕ) (hs : ∀ r, (D r).card ≤ s) :
    ∀ r, (rhsDependent D rhsDep r).card ≤ s + 1 := by
  intro r
  rw [rhsDependent_card]
  split_ifs <;> have := hs r <;> omega

theorem rhsDependent_incidence [Fintype R] [DecidableEq C]
    (D : R → Finset C) (rhsDep : R → Bool) :
    ∑ r, (rhsDependent D rhsDep r).card =
      (∑ r, (D r).card) + ∑ r, if rhsDep r then 1 else 0 := by
  simp only [rhsDependent_card, Finset.sum_add_distrib]

theorem rhsMatrix_locality [DecidableEq C]
    (A : R → C → ℝ) (A' : I → R → C → ℝ) (b : R → ℝ) (b' : I → R → ℝ)
    (D : R → Finset C) (label : R → C → I) (rhsDep : R → Bool) (rhsBit : R → I)
    (hA : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (hb : ∀ i r, rhsDep r = false ∨ rhsBit r ≠ i → b' i r = b r) :
    ∀ i r j, j ∉ rhsDependent D rhsDep r ∨ rhsLabel label rhsBit r j ≠ i →
      rhsMatrix (A' i) (b' i) r j = rhsMatrix A b r j := by
  intro i r j h
  cases j with
  | none =>
    simp only [rhsMatrix]
    congr 1
    apply hb i r
    cases hd : rhsDep r
    · exact Or.inl rfl
    · simpa [rhsDependent, rhsLabel, hd] using h
  | some c =>
    apply hA i r c
    cases hd : rhsDep r <;> simpa [rhsDependent, rhsLabel, hd] using h

/-- Slack columns are public, so single-bit locality is inherited unchanged. -/
theorem slackMatrix_locality [DecidableEq R]
    (A : R → C → ℝ) (A' : I → R → C → ℝ) (D : R → Finset C)
    (label : R → C → I)
    (hA : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    ∀ i r j, (∀ c, j = Sum.inl c → c ∉ D r ∨ label r c ≠ i) →
      slackMatrix (A' i) r j = slackMatrix A r j := by
  intro i r j h
  cases j with
  | inl c => exact hA i r c (h c rfl)
  | inr q => rfl

end
end QipmFormal.Mixture
