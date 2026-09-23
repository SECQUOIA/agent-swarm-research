import Formal.QuadraticPrecision.SquareSystem
import Formal.QuadraticPrecision.BinaryModel

noncomputable section
namespace QuadraticPrecision

def squareBinaryLift (L : ℕ) (hypo : Bool) : BinaryLinearLift 1 L (2 + (L + L)) where
  system := squareSystem L hypo
  code_bounds x hx i := (squareSystem_feasible L hypo x |>.mp hx).1 i

@[simp] theorem squareBinaryLift_rowCount (L : ℕ) (hypo : Bool) :
    (squareBinaryLift L hypo).system.rowCount = 11 + L * 10 := rfl

def squareAuxWitness (L : ℕ) (r q : ℝ) (v t : Fin L → ℝ) : Fin (2 + (L+L)) → ℝ :=
  Fin.addCases ![r,q] (Fin.addCases v t)

theorem squareLift_relaxation (L : ℕ) (hypo : Bool) (x : Input 1) (w : ℝ) :
    (x,w) ∈ (squareBinaryLift L hypo).relaxation ↔
      if hypo then SquareHypographRelaxation L (x 0) w else SquareRelaxation L (x 0) w := by
  constructor
  · rintro ⟨b,hb,a,ha⟩
    have h := (squareSystem_feasible L hypo (x,w,a,b)).mp ha
    cases hypo
    · exact ⟨b, (fun i => squareV L i (x,w,a,b)),
        (fun i => squareT L i (x,w,a,b)), squareR L (x,w,a,b), squareQ L (x,w,a,b),
        hb, h.2⟩
    · exact ⟨b, (fun i => squareV L i (x,w,a,b)),
        (fun i => squareT L i (x,w,a,b)), squareR L (x,w,a,b), squareQ L (x,w,a,b),
        hb, h.2⟩
  · intro h
    cases hypo <;> obtain ⟨b,v,t,r,q,hb,h⟩ := h
    all_goals
      refine ⟨b,hb,squareAuxWitness L r q v t, ?_⟩
      apply (squareSystem_feasible L _ _).mpr
      constructor
      · intro i
        change 0 ≤ b i ∧ b i ≤ 1
        rcases hb i with he | he <;> simp [he]
      · simpa only [squareInput, squareOutput, squareR, squareQ, squareV, squareT,
          squareAux, squareBit, squareAuxWitness,
          LinearMap.comp_apply, LinearMap.proj_apply, LinearMap.fst_apply, LinearMap.snd_apply,
          Fin.addCases_left, Fin.addCases_right, Matrix.cons_val_zero,
          Matrix.cons_val_succ, Matrix.cons_val_one,
          Bool.false_eq_true, Bool.true_eq, reduceIte] using h

theorem squareBinaryLift_graph (L : ℕ) :
    IsGraphRelaxation {x : Input 1 | x 0 ∈ Set.Icc 0 1} (fun x => (x 0)^2)
      ((squareWidth L)^2/4) (squareBinaryLift L false).relaxation := by
  constructor
  · intro x hx
    apply (squareLift_relaxation L false x _).mpr
    exact squareRelaxation_contains_graph L (x 0) hx
  · intro z hz
    exact squareRelaxation_error ((squareLift_relaxation L false z.1 z.2).mp hz)

theorem squareBinaryLift_hypograph (L : ℕ) :
    IsHypographRelaxation {x : Input 1 | x 0 ∈ Set.Icc 0 1} (fun x => (x 0)^2)
      ((squareWidth L)^2/4) (squareBinaryLift L true).relaxation := by
  constructor
  · intro x hx w hw
    apply (squareLift_relaxation L true x w).mpr
    exact squareHypograph_contains hx hw
  · intro z hz
    exact squareHypograph_error ((squareLift_relaxation L true z.1 z.2).mp hz)

theorem square_hasBinaryGraphLift (L : ℕ) :
    HasBinaryGraphLift {x : Input 1 | x 0 ∈ Set.Icc 0 1} (fun x => (x 0)^2)
      ((squareWidth L)^2/4) L :=
  ⟨2+(L+L), squareBinaryLift L false, squareBinaryLift_graph L⟩

theorem square_hasBinaryHypographLift (L : ℕ) :
    HasBinaryHypographLift {x : Input 1 | x 0 ∈ Set.Icc 0 1} (fun x => (x 0)^2)
      ((squareWidth L)^2/4) L :=
  ⟨2+(L+L), squareBinaryLift L true, squareBinaryLift_hypograph L⟩

theorem squareBinaryLift_attains (L : ℕ) :
    ((fun _ : Fin 1 => squareWidth L / 2), (squareWidth L)^2 / 2) ∈
      (squareBinaryLift L false).relaxation ∧
    (squareWidth L)^2 / 2 - (squareWidth L / 2)^2 = (squareWidth L)^2 / 4 := by
  exact ⟨(squareLift_relaxation L false _ _).mpr (squareRelaxation_attains L).1,
    (squareRelaxation_attains L).2⟩

end QuadraticPrecision
