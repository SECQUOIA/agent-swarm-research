import Formal.QuadraticPrecision.Folding
import Formal.QuadraticPrecision.BinaryModel

/-! A concrete continuous linear lift of the folding epigraph.
Every inequality is an affine map. Depth `n` uses `n` continuous auxiliary
coordinates, no binary coordinates, and exactly `3*n+3` inequality rows,
including the two input-domain inequalities. -/

namespace QuadraticPrecision
noncomputable section

private def foldingT (n : ℕ) : LiftPoint 1 0 n →ₗ[ℝ] ℝ where
  toFun v := v.1 0
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

private def foldingW (n : ℕ) : LiftPoint 1 0 n →ₗ[ℝ] ℝ where
  toFun v := v.2.1
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

private def foldingG (n : ℕ) (i : Fin n) : LiftPoint 1 0 n →ₗ[ℝ] ℝ where
  toFun v := v.2.2.1 i
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

private def foldingTail (n : ℕ) : LiftPoint 1 0 (n+1) →ₗ[ℝ] LiftPoint 1 0 n where
  toFun v := (fun _ => v.2.2.1 0, v.2.1, fun i => v.2.2.1 i.succ, v.2.2.2)
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

private def foldingObjective (n : ℕ) : LiftPoint 1 0 n →ₗ[ℝ] ℝ where
  toFun v := foldObjective n v.2.2.1
  map_add' v w := foldObjective_add n v.2.2.1 w.2.2.1
  map_smul' c v := foldObjective_smul n c v.2.2.1

private def foldingRows : (n : ℕ) → List (LiftPoint 1 0 n →ᵃ[ℝ] ℝ)
  | 0 => []
  | n+1 => [-(foldingG (n+1) 0).toAffineMap,
      (foldingG (n+1) 0).toAffineMap - 2 • (foldingT (n+1)).toAffineMap,
      (foldingG (n+1) 0).toAffineMap + 2 • (foldingT (n+1)).toAffineMap -
        AffineMap.const ℝ _ 2] ++
      (foldingRows n).map (fun r => r.comp (foldingTail n).toAffineMap)

private theorem foldingRows_length (n : ℕ) : (foldingRows n).length = 3*n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [foldingRows, ih]; omega

private theorem foldingRows_feasible (n : ℕ) (v : LiftPoint 1 0 n) :
    (∀ r ∈ foldingRows n, r v ≤ 0) ↔ FoldFeasible n (v.1 0) v.2.2.1 := by
  induction n with
  | zero => simp [foldingRows, FoldFeasible]
  | succ n ih =>
    simp only [foldingRows, List.forall_mem_append, List.forall_mem_cons,
      List.forall_mem_map]
    rw [show (∀ a ∈ foldingRows n, (a.comp (foldingTail n).toAffineMap) v ≤ 0) ↔
      FoldFeasible n ((foldingTail n v).1 0) (foldingTail n v).2.2.1 from ih _]
    simp only [AffineMap.coe_neg, LinearMap.coe_toAffineMap, Pi.neg_apply,
      Left.neg_nonpos_iff, AffineMap.coe_sub, AffineMap.coe_smul, nsmul_eq_mul,
      Nat.cast_ofNat, Pi.sub_apply, Pi.mul_apply, Pi.ofNat_apply, tsub_le_iff_right,
      zero_add, AffineMap.coe_add, AffineMap.coe_const, Pi.add_apply,
      Function.const_apply, List.not_mem_nil, IsEmpty.forall_iff, implies_true,
      and_true, Fin.isValue]
    constructor
    · rintro ⟨⟨h0,h1,h2⟩,h3⟩
      change v.2.2.1 0 + 2 * v.1 0 ≤ 2 at h2
      exact ⟨h0,h1,by linarith,h3⟩
    · rintro ⟨h0,h1,h2,h3⟩
      exact ⟨⟨h0,h1,by change v.2.2.1 0 + 2 * v.1 0 ≤ 2; linarith⟩,h3⟩

private def foldingAllRows (n : ℕ) : List (LiftPoint 1 0 n →ᵃ[ℝ] ℝ) :=
  [-(foldingT n).toAffineMap,
   (foldingT n).toAffineMap - AffineMap.const ℝ _ 1,
   (foldingT n).toAffineMap - (foldingObjective n).toAffineMap -
     AffineMap.const ℝ _ (foldError n) - (foldingW n).toAffineMap] ++ foldingRows n

/-- The folding LP, including the two input-domain inequalities. -/
def foldingSystem (n : ℕ) : LinearSystem (LiftPoint 1 0 n) where
  rowCount := (foldingAllRows n).length
  row := (foldingAllRows n).get

theorem foldingSystem_rowCount (n : ℕ) : (foldingSystem n).rowCount = 3*n+3 := by
  simp [foldingSystem, foldingAllRows, foldingRows_length]

theorem foldingSystem_feasible (n : ℕ) (v : LiftPoint 1 0 n) :
    v ∈ (foldingSystem n).feasible ↔
      v.1 0 ∈ Set.Icc (0 : ℝ) 1 ∧ FoldFeasible n (v.1 0) v.2.2.1 ∧
      v.1 0-foldObjective n v.2.2.1-foldError n ≤ v.2.1 := by
  change (∀ i, (foldingAllRows n).get i v ≤ 0) ↔ _
  have he : (∀ i, (foldingAllRows n).get i v ≤ 0) ↔
      (∀ r ∈ foldingAllRows n, r v ≤ 0) := by
    constructor
    · intro h r hr
      obtain ⟨i, rfl⟩ := List.mem_iff_get.mp hr
      exact h i
    · intro h i
      exact h _ (List.get_mem _ _)
  rw [he]
  simp only [foldingAllRows, List.forall_mem_append, List.forall_mem_cons,
    foldingRows_feasible]
  simp [foldingT, foldingW, foldingObjective, Set.mem_Icc]
  tauto

def foldingBinaryLift (n : ℕ) : BinaryLinearLift 1 0 n where
  system := foldingSystem n
  code_bounds := by intro v hv i; exact Fin.elim0 i

theorem foldingBinaryLift_relaxation (n : ℕ) (v : Input 1 × ℝ) :
    v ∈ (foldingBinaryLift n).relaxation ↔
      v.1 0 ∈ Set.Icc (0 : ℝ) 1 ∧ FoldEpigraph n (v.1 0) v.2 := by
  constructor
  · rintro ⟨z, hz, g, hg⟩
    obtain ⟨ht, hg, hw⟩ := (foldingSystem_feasible n _).mp hg
    exact ⟨ht,g,hg,hw⟩
  · rintro ⟨ht,g,hg,hw⟩
    refine ⟨Fin.elim0, (by intro i; exact Fin.elim0 i), g, ?_⟩
    exact (foldingSystem_feasible n _).mpr ⟨ht,hg,hw⟩

theorem foldingBinaryLift_isEpigraph (n : ℕ) :
    IsEpigraphRelaxation {x : Input 1 | x 0 ∈ Set.Icc (0 : ℝ) 1}
      (fun x => (x 0)^2) (foldError n) (foldingBinaryLift n).relaxation := by
  constructor
  · intro x hx w hw
    rw [foldingBinaryLift_relaxation]
    refine ⟨hx, (foldEpigraph_iff n hx).mpr ?_⟩
    linarith [(foldApprox_error n hx).2]
  · intro v hv
    obtain ⟨ht,hw⟩ := (foldingBinaryLift_relaxation n v).mp hv
    exact ⟨ht,foldEpigraph_error n ht hw⟩

theorem square_has_zeroBinary_epigraph (n : ℕ) :
    HasBinaryEpigraphLift {x : Input 1 | x 0 ∈ Set.Icc (0 : ℝ) 1}
      (fun x => (x 0)^2) (foldError n) 0 :=
  ⟨n, foldingBinaryLift n, foldingBinaryLift_isEpigraph n⟩

end
end QuadraticPrecision
