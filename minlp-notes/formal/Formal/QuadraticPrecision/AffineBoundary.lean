import Formal.QuadraticPrecision.BinaryModel

/-! Exact finite linear lifts for affine functions on boxes, including degenerate
and empty boxes. No integer or continuous auxiliary coordinates are needed. -/
namespace QuadraticPrecision
noncomputable section

private def affineInput (n : ℕ) : LiftPoint n 0 0 →ₗ[ℝ] Input n :=
  LinearMap.fst ℝ _ _

private def affineOutput (n : ℕ) : LiftPoint n 0 0 →ₗ[ℝ] ℝ :=
  (LinearMap.fst ℝ _ _).comp (LinearMap.snd ℝ _ _)

private def affineCoordinate (n : ℕ) (i : Fin n) : LiftPoint n 0 0 →ₗ[ℝ] ℝ where
  toFun v := v.1 i
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- The actual two affine bound rows per input coordinate. -/
def affineBoxSystem {n : ℕ} (l u : Input n) : LinearSystem (LiftPoint n 0 0) where
  rowCount := n+n
  row := Fin.addCases
    (fun i => AffineMap.const ℝ _ (l i) - (affineCoordinate n i).toAffineMap)
    (fun i => (affineCoordinate n i).toAffineMap - AffineMap.const ℝ _ (u i))

theorem affineBoxSystem_feasible {n : ℕ} (l u : Input n) (v : LiftPoint n 0 0) :
    v ∈ (affineBoxSystem l u).feasible ↔ v.1 ∈ Set.Icc l u := by
  simp [LinearSystem.feasible, affineBoxSystem, Fin.forall_fin_add,
    affineCoordinate, Set.mem_Icc, Pi.le_def, -Fin.natAdd_eq_addNat]

private def affineResidual {n : ℕ} (f : Input n →ᵃ[ℝ] ℝ) :
    LiftPoint n 0 0 →ᵃ[ℝ] ℝ :=
  (affineOutput n).toAffineMap - f.comp (affineInput n).toAffineMap

private theorem affineResidual_apply {n : ℕ} (f : Input n →ᵃ[ℝ] ℝ)
    (v : LiftPoint n 0 0) : affineResidual f v = v.2.1-f v.1 := rfl

private def singleAffineRow {V : Type*} [AddCommGroup V] [Module ℝ V]
    (r : V →ᵃ[ℝ] ℝ) : LinearSystem V := ⟨1, fun _ => r⟩

private theorem singleAffineRow_feasible {V : Type*} [AddCommGroup V] [Module ℝ V]
    (r : V →ᵃ[ℝ] ℝ) (v : V) : v ∈ (singleAffineRow r).feasible ↔ r v ≤ 0 := by
  simp [LinearSystem.feasible, singleAffineRow]

/-- Exact epigraph rows, including all box bounds. -/
def affineEpigraphSystem {n : ℕ} (l u : Input n) (f : Input n →ᵃ[ℝ] ℝ) :
    LinearSystem (LiftPoint n 0 0) :=
  (affineBoxSystem l u).append (singleAffineRow (-affineResidual f))

/-- Exact hypograph rows, including all box bounds. -/
def affineHypographSystem {n : ℕ} (l u : Input n) (f : Input n →ᵃ[ℝ] ℝ) :
    LinearSystem (LiftPoint n 0 0) :=
  (affineBoxSystem l u).append (singleAffineRow (affineResidual f))

/-- Exact graph rows: the output equality is represented by two inequalities. -/
def affineGraphSystem {n : ℕ} (l u : Input n) (f : Input n →ᵃ[ℝ] ℝ) :
    LinearSystem (LiftPoint n 0 0) :=
  (affineEpigraphSystem l u f).append (singleAffineRow (affineResidual f))

theorem affineEpigraphSystem_feasible {n : ℕ} (l u : Input n)
    (f : Input n →ᵃ[ℝ] ℝ) (v : LiftPoint n 0 0) :
    v ∈ (affineEpigraphSystem l u f).feasible ↔ v.1 ∈ Set.Icc l u ∧ f v.1 ≤ v.2.1 := by
  simp [affineEpigraphSystem, LinearSystem.feasible_append, affineBoxSystem_feasible,
    singleAffineRow_feasible, affineResidual_apply]

theorem affineHypographSystem_feasible {n : ℕ} (l u : Input n)
    (f : Input n →ᵃ[ℝ] ℝ) (v : LiftPoint n 0 0) :
    v ∈ (affineHypographSystem l u f).feasible ↔ v.1 ∈ Set.Icc l u ∧ v.2.1 ≤ f v.1 := by
  simp [affineHypographSystem, LinearSystem.feasible_append, affineBoxSystem_feasible,
    singleAffineRow_feasible, affineResidual_apply]

theorem affineGraphSystem_feasible {n : ℕ} (l u : Input n)
    (f : Input n →ᵃ[ℝ] ℝ) (v : LiftPoint n 0 0) :
    v ∈ (affineGraphSystem l u f).feasible ↔ v.1 ∈ Set.Icc l u ∧ v.2.1 = f v.1 := by
  simp only [affineGraphSystem, LinearSystem.feasible_append, Set.mem_inter_iff,
    affineEpigraphSystem_feasible, singleAffineRow_feasible, affineResidual_apply,
    sub_nonpos]
  constructor
  · rintro ⟨⟨h,h1⟩,h2⟩; exact ⟨h,le_antisymm h2 h1⟩
  · rintro ⟨h,he⟩; exact ⟨⟨h,he.ge⟩,he.le⟩

theorem affineSystem_rowCounts {n : ℕ} (l u : Input n) (f : Input n →ᵃ[ℝ] ℝ) :
    (affineGraphSystem l u f).rowCount = 2*n+2 ∧
    (affineEpigraphSystem l u f).rowCount = 2*n+1 ∧
    (affineHypographSystem l u f).rowCount = 2*n+1 := by
  simp [affineGraphSystem, affineEpigraphSystem, affineHypographSystem,
    affineBoxSystem, singleAffineRow, LinearSystem.append]; omega

/-- With no integer coordinates, every finite linear system is a binary lift. -/
def zeroBinaryLift {n q : ℕ} (S : LinearSystem (LiftPoint n 0 q)) :
    BinaryLinearLift n 0 q where
  system := S
  code_bounds := by intro v hv i; exact Fin.elim0 i

theorem zeroBinaryLift_relaxation {n : ℕ} (S : LinearSystem (LiftPoint n 0 0))
    (v : Input n × ℝ) : v ∈ (zeroBinaryLift S).relaxation ↔
      (v.1,v.2,0,0) ∈ S.feasible := by
  constructor
  · rintro ⟨z,hz,a,ha⟩
    have hz0 : z = 0 := Subsingleton.elim _ _
    have ha0 : a = 0 := Subsingleton.elim _ _
    simpa only [hz0,ha0,zeroBinaryLift] using ha
  · intro h
    exact ⟨0, (by intro i; exact Fin.elim0 i), 0, h⟩

theorem affine_has_zeroBinary_graph {n : ℕ} (l u : Input n)
    (f : Input n →ᵃ[ℝ] ℝ) : HasBinaryGraphLift (Set.Icc l u) f 0 0 := by
  refine ⟨0,zeroBinaryLift (affineGraphSystem l u f), ?_, ?_⟩
  · intro x hx
    rw [zeroBinaryLift_relaxation, affineGraphSystem_feasible]
    exact ⟨hx,rfl⟩
  · intro v hv
    rw [zeroBinaryLift_relaxation, affineGraphSystem_feasible] at hv
    change v.1 ∈ Set.Icc l u ∧ v.2 = f v.1 at hv
    exact ⟨hv.1, by simp [hv.2]⟩

theorem affine_has_zeroBinary_epigraph {n : ℕ} (l u : Input n)
    (f : Input n →ᵃ[ℝ] ℝ) : HasBinaryEpigraphLift (Set.Icc l u) f 0 0 := by
  refine ⟨0,zeroBinaryLift (affineEpigraphSystem l u f), ?_, ?_⟩
  · intro x hx w hw
    rw [zeroBinaryLift_relaxation, affineEpigraphSystem_feasible]
    exact ⟨hx,hw⟩
  · intro v hv
    rw [zeroBinaryLift_relaxation, affineEpigraphSystem_feasible] at hv
    simpa using hv

theorem affine_has_zeroBinary_hypograph {n : ℕ} (l u : Input n)
    (f : Input n →ᵃ[ℝ] ℝ) : HasBinaryHypographLift (Set.Icc l u) f 0 0 := by
  refine ⟨0,zeroBinaryLift (affineHypographSystem l u f), ?_, ?_⟩
  · intro x hx w hw
    rw [zeroBinaryLift_relaxation, affineHypographSystem_feasible]
    exact ⟨hx,hw⟩
  · intro v hv
    rw [zeroBinaryLift_relaxation, affineHypographSystem_feasible] at hv
    simpa using hv

/-- The exact epigraph of a convex function is already a convex lift with no
integer or continuous auxiliary coordinates. This does not assert linearity. -/
def exactConvexEpigraph {n : ℕ} {D : Set (Input n)} {f : Input n → ℝ}
    (hf : ConvexOn ℝ D f) : ConvexIntegerLift n 0 0 where
  carrier := {v | v.1 ∈ D ∧ f v.1 ≤ v.2.1}
  convex_carrier := by
    intro v hv w hw a b ha hb hab
    refine ⟨hf.1 hv.1 hw.1 ha hb hab, ?_⟩
    exact (hf.2 hv.1 hw.1 ha hb hab).trans
      (add_le_add (mul_le_mul_of_nonneg_left hv.2 ha) (mul_le_mul_of_nonneg_left hw.2 hb))

theorem convexOn_has_exact_epigraph {n : ℕ} {D : Set (Input n)} {f : Input n → ℝ}
    (hf : ConvexOn ℝ D f) : HasEpigraphLift D f 0 0 := by
  refine ⟨0,exactConvexEpigraph hf, ?_, ?_⟩
  · intro x hx w hw
    exact ⟨0,0,hx,hw⟩
  · rintro v ⟨z,a,ha⟩
    exact ⟨ha.1,by simpa only [sub_zero] using ha.2⟩

/-- The exact hypograph of a concave function needs no integer coordinates. -/
def exactConcaveHypograph {n : ℕ} {D : Set (Input n)} {f : Input n → ℝ}
    (hf : ConcaveOn ℝ D f) : ConvexIntegerLift n 0 0 where
  carrier := {v | v.1 ∈ D ∧ v.2.1 ≤ f v.1}
  convex_carrier := by
    intro v hv w hw a b ha hb hab
    refine ⟨hf.1 hv.1 hw.1 ha hb hab, ?_⟩
    exact (add_le_add (mul_le_mul_of_nonneg_left hv.2 ha)
      (mul_le_mul_of_nonneg_left hw.2 hb)).trans (hf.2 hv.1 hw.1 ha hb hab)

theorem concaveOn_has_exact_hypograph {n : ℕ} {D : Set (Input n)} {f : Input n → ℝ}
    (hf : ConcaveOn ℝ D f) : HasHypographLift D f 0 0 := by
  refine ⟨0,exactConcaveHypograph hf, ?_, ?_⟩
  · intro x hx w hw
    exact ⟨0,0,hx,hw⟩
  · rintro v ⟨z,a,ha⟩
    exact ⟨ha.1,by simpa only [add_zero] using ha.2⟩

end
end QuadraticPrecision
