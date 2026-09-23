import Formal.NetworkSimplex.Reduction

/-! Exact grouping of profile rows, including absent directions and zero rows. -/

namespace NetworkSimplex.Chain.ReductionData

noncomputable section

variable {m : ℕ} {I : Type*}

/-- Box consequences supply every direction, so all minima have nonempty fibers. -/
def boxRhs (D : ReductionData m I) : ProfileNormal m → ℝ
  | .subset s => ∑ j ∈ s, D.weights j.succ
  | .negativeSingleton _ => 0
  | .negativeTotal => 0

def augmentedNormal (D : ReductionData m I) :
    ProfileRow m I ⊕ ProfileNormal m → ProfileNormal m :=
  Sum.elim D.rowNormal id

def augmentedRhs (D : ReductionData m I) : ProfileRow m I ⊕ ProfileNormal m → ℝ :=
  Sum.elim D.rowRhs D.boxRhs

theorem augmentedNormal_surjective (D : ReductionData m I) :
    Function.Surjective D.augmentedNormal := fun n => ⟨Sum.inr n, rfl⟩

theorem box_rows_of_reducedProfile (D : ReductionData m I) (x : Fin m → ℝ)
    (h : D.ReducedProfile x) : ∀ n, n.value x ≤ D.boxRhs n := by
  intro n
  cases n with
  | subset s =>
      exact Finset.sum_le_sum fun j _ => (h.1 j).2
  | negativeSingleton j =>
      exact neg_nonpos.mpr (h.1 j).1
  | negativeTotal =>
      exact neg_nonpos.mpr (Finset.sum_nonneg fun j _ => (h.1 j).1)

theorem augmented_rows_iff (D : ReductionData m I) (x : Fin m → ℝ) :
    (∀ r, (D.augmentedNormal r).value x ≤ D.augmentedRhs r) ↔
      D.ReducedProfile x := by
  constructor
  · intro h
    exact (D.rows_iff_reducedProfile x).mp fun r => h (.inl r)
  · intro h r
    cases r with
    | inl r => exact (D.rows_iff_reducedProfile x).mpr h r
    | inr n => exact D.box_rows_of_reducedProfile x h n

variable [Fintype I]

/-- The least bound for each normal, retaining the zero normal explicitly. -/
def grouped (D : ReductionData m I) : ProfileNormal m → ℝ :=
  groupedBound D.augmentedNormal D.augmentedRhs D.augmentedNormal_surjective

theorem grouped_iff_reducedProfile (D : ReductionData m I) (x : Fin m → ℝ) :
    (∀ n, n.value x ≤ D.grouped n) ↔ D.ReducedProfile x :=
  (groupedBound_iff D.augmentedNormal D.augmentedRhs D.augmentedNormal_surjective
    (fun n => n.value x)).symm.trans (D.augmented_rows_iff x)

end
end NetworkSimplex.Chain.ReductionData
