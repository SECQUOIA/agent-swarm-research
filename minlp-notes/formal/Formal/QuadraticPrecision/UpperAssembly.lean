import Formal.QuadraticPrecision.BinaryModel
namespace QuadraticPrecision
noncomputable section
open scoped BigOperators
namespace UpperAssembly
variable {n : ℕ} {J : Type*} [Fintype J]
abbrev CodeIndex (p : J → ℕ) := Σ j, Fin (p j)
abbrev AuxIndex (q : J → ℕ) := Σ j, Option (Fin (q j))
abbrev Ambient (n : ℕ) (p q : J → ℕ) :=
  LiftPoint n (Fintype.card (CodeIndex p)) (Fintype.card (AuxIndex q))
def input (p q : J → ℕ) : Ambient n p q →ₗ[ℝ] Input n := LinearMap.fst ℝ _ _
def output (p q : J → ℕ) : Ambient n p q →ₗ[ℝ] ℝ :=
  (LinearMap.fst ℝ _ _).comp (LinearMap.snd ℝ _ _)
def aux (p q : J → ℕ) (i : AuxIndex q) : Ambient n p q →ₗ[ℝ] ℝ :=
  (LinearMap.proj (Fintype.equivFin _ i)).comp
    ((LinearMap.fst ℝ _ _).comp ((LinearMap.snd ℝ _ _).comp (LinearMap.snd ℝ _ _)))
def code (p q : J → ℕ) (i : CodeIndex p) : Ambient n p q →ₗ[ℝ] ℝ :=
  (LinearMap.proj (Fintype.equivFin _ i)).comp
    ((LinearMap.snd ℝ _ _).comp ((LinearMap.snd ℝ _ _).comp (LinearMap.snd ℝ _ _)))
def component (p q : J → ℕ) (y : J → Input n →ᵃ[ℝ] ℝ) (j : J) :
    Ambient n p q →ᵃ[ℝ] LiftPoint 1 (p j) (q j) :=
  (AffineMap.pi fun _ => (y j).comp (input p q).toAffineMap).prod
    ((aux p q ⟨j,none⟩).toAffineMap.prod
      ((AffineMap.pi fun i => (aux p q ⟨j,some i⟩).toAffineMap).prod
        (AffineMap.pi fun i => (code p q ⟨j,i⟩).toAffineMap)))
def assembledOutput (p q : J → ℕ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ) :
    Ambient n p q →ᵃ[ℝ] ℝ :=
  a.comp (input p q).toAffineMap + ∑ j, c j • (aux p q ⟨j,none⟩).toAffineMap
private theorem affine_sum_eval {V : Type*} [AddCommGroup V] [Module ℝ V]
    (f : J → V →ᵃ[ℝ] ℝ) (v : V) : (∑ j, f j) v = ∑ j, f j v := by
  classical
  induction (Finset.univ : Finset J) using Finset.induction_on with
  | empty => simp
  | @insert j s hj ih => simp [Finset.sum_insert, hj, ih, AffineMap.coe_add]
@[simp] theorem assembledOutput_apply (p q : J → ℕ) (a : Input n →ᵃ[ℝ] ℝ)
    (c : J → ℝ) (v : Ambient n p q) :
    assembledOutput p q a c v = a v.1 + ∑ j, c j * aux p q ⟨j,none⟩ v := by
  simp [assembledOutput, affine_sum_eval, input]
abbrev RowIndex (D : LinearSystem (Input n)) (p q : J → ℕ)
    (S : ∀ j, BinaryLinearLift 1 (p j) (q j)) :=
  Fin D.rowCount ⊕ (Σ j, Fin (S j).system.rowCount) ⊕ Fin 2
def system (D : LinearSystem (Input n)) (p q : J → ℕ)
    (S : ∀ j, BinaryLinearLift 1 (p j) (q j))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ)
    (epi : Bool) : LinearSystem (Ambient n p q) where
  rowCount := Fintype.card (RowIndex D p q S)
  row k := Sum.elim (fun i => (D.row i).comp (input p q).toAffineMap)
    (Sum.elim (fun i => ((S i.1).system.row i.2).comp (component p q y i.1))
      (fun i => if i = 0 then assembledOutput p q a c - (output p q).toAffineMap
        else if epi then 0 else (output p q).toAffineMap - assembledOutput p q a c))
    ((Fintype.equivFin _).symm k)
theorem system_feasible (D : LinearSystem (Input n)) (p q : J → ℕ)
    (S : ∀ j, BinaryLinearLift 1 (p j) (q j))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ)
    (epi : Bool) (v : Ambient n p q) :
    v ∈ (system D p q S y a c epi).feasible ↔
      v.1 ∈ D.feasible ∧ (∀ j, component p q y j v ∈ (S j).system.feasible) ∧
      assembledOutput p q a c v ≤ v.2.1 ∧
      (epi = false → v.2.1 ≤ assembledOutput p q a c v) := by
  change (∀ k, _ ≤ 0) ↔ _
  have he : (∀ k, (system D p q S y a c epi).row k v ≤ 0) ↔
      ∀ i : RowIndex D p q S, (system D p q S y a c epi).row
        (Fintype.equivFin _ i) v ≤ 0 := by
    constructor
    · intro h i; exact h _
    · intro h k
      obtain ⟨i, rfl⟩ := (Fintype.equivFin (RowIndex D p q S)).surjective k
      exact h i
  rw [he]
  simp only [system, Equiv.symm_apply_apply,
    Sum.forall, Sum.elim_inl, Sum.elim_inr, Sigma.forall,
    AffineMap.comp_apply, input,
    Fin.forall_fin_succ, Fin.forall_fin_zero]
  cases epi <;> simp [LinearSystem.feasible, output]

def lift (D : LinearSystem (Input n)) (p q : J → ℕ)
    (S : ∀ j, BinaryLinearLift 1 (p j) (q j))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ)
    (epi : Bool) : BinaryLinearLift n (Fintype.card (CodeIndex p))
      (Fintype.card (AuxIndex q)) where
  system := system D p q S y a c epi
  code_bounds := by
    intro v hv i
    obtain ⟨hvD,hvS,hvW⟩ := (system_feasible D p q S y a c epi v).mp hv
    let ji := (Fintype.equivFin (CodeIndex p)).symm i
    have h := (S ji.1).code_bounds _ (hvS ji.1) ji.2
    simpa [component, code, ji] using h
/-- Exact semantics of the finite assembled rows, including the original domain. -/
theorem relaxation (D : LinearSystem (Input n)) (p q : J → ℕ)
    (S : ∀ j, BinaryLinearLift 1 (p j) (q j))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ)
    (epi : Bool) (x : Input n) (w : ℝ) :
    (x,w) ∈ (lift D p q S y a c epi).relaxation ↔
      x ∈ D.feasible ∧ ∃ t : J → ℝ,
        (∀ j, ((fun _ => y j x), t j) ∈ (S j).relaxation) ∧
        a x + ∑ j, c j * t j ≤ w ∧
        (epi = false → w ≤ a x + ∑ j, c j * t j) := by
  classical
  constructor
  · rintro ⟨z,hz,b,hb⟩
    obtain ⟨hD,hS,hW,hW'⟩ := (system_feasible D p q S y a c epi (x,w,b,z)).mp hb
    refine ⟨hD, fun j => aux p q ⟨j,none⟩ (x,w,b,z), ?_, ?_, ?_⟩
    · intro j
      refine ⟨fun i => code p q ⟨j,i⟩ (x,w,b,z), ?_,
        fun i => aux p q ⟨j,some i⟩ (x,w,b,z), ?_⟩
      · intro i; exact hz _
      · exact hS j
    · simpa using hW
    · simpa using hW'
  · rintro ⟨hD,t,hS,hW,hW'⟩
    choose z hz b hb using hS
    let Z : Fin (Fintype.card (CodeIndex p)) → ℝ := fun i =>
      let ji := (Fintype.equivFin (CodeIndex p)).symm i
      z ji.1 ji.2
    let B : Fin (Fintype.card (AuxIndex q)) → ℝ := fun i =>
      let ji := (Fintype.equivFin (AuxIndex q)).symm i
      ji.2.elim (t ji.1) (b ji.1)
    have ha (j : J) : aux p q ⟨j,none⟩ (x,w,B,Z) = t j := by
      change B ((Fintype.equivFin _) ⟨j,none⟩) = t j
      dsimp only [B]
      rw [Equiv.symm_apply_apply]
      rfl
    refine ⟨Z, (fun i => hz _ _), B, ?_⟩
    apply (system_feasible D p q S y a c epi _).mpr
    refine ⟨hD, ?_, ?_, ?_⟩
    · intro j
      have he : component p q y j (x,w,B,Z) = (fun _ => y j x, t j, b j, z j) := by
        apply Prod.ext
        · rfl
        apply Prod.ext
        · exact ha j
        apply Prod.ext
        · funext i
          change B ((Fintype.equivFin _) ⟨j,some i⟩) = b j i
          dsimp only [B]
          rw [Equiv.symm_apply_apply]
          rfl
        · funext i
          change Z ((Fintype.equivFin _) ⟨j,i⟩) = z j i
          dsimp only [Z]
          rw [Equiv.symm_apply_apply]
      rw [he]
      exact hb j
    · simpa [ha] using hW
    · simpa [ha] using hW'
@[simp] theorem code_count (p : J → ℕ) : Fintype.card (CodeIndex p) = ∑ j, p j := by
  simp [CodeIndex, Fintype.card_sigma]
@[simp] theorem aux_count (q : J → ℕ) : Fintype.card (AuxIndex q) = ∑ j, (q j + 1) := by
  simp [AuxIndex, Fintype.card_sigma]
@[simp] theorem row_count (D : LinearSystem (Input n)) (p q : J → ℕ)
    (S : ∀ j, BinaryLinearLift 1 (p j) (q j))
    (y : J → Input n →ᵃ[ℝ] ℝ) (a : Input n →ᵃ[ℝ] ℝ) (c : J → ℝ)
    (epi : Bool) :
    (lift D p q S y a c epi).system.rowCount =
      D.rowCount + (∑ j, (S j).system.rowCount) + 2 := by
  simp [lift,system,RowIndex,Fintype.card_sigma,Nat.add_assoc]
end UpperAssembly
end
end QuadraticPrecision
