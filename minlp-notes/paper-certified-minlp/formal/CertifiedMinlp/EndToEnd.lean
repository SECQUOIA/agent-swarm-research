import CertifiedMinlp.ModelSemantics
import CertifiedMinlp.Propagation
import CertifiedMinlp.CutCertificate
import CertifiedMinlp.DiscreteSolutions
import CertifiedMinlp.MasterIdentity

/-! Concrete composition of propagation, analytic cut evidence, and a checked
discrete proof. No master-feasible embedding is assumed. -/
namespace CertifiedMinlp
open scoped BigOperators

namespace CertifiedModel
open Discrete

variable {n k : ℕ}

def feasible (p : Propagation.Problem n) (rows : Fin k → (Fin n → ℝ) → ℝ) :
    Set (Fin n → ℝ) := {x | p.Feasible x ∧ ∀ j, rows j x ≤ 0}

def extendedBox (B : Fin n → Coordinate) : Fin (n + 2) → Coordinate :=
  Fin.snoc (Fin.snoc B .free) (.bounded 1 1)

theorem extendedPoint_mem (B : Fin n → Coordinate) (x : Fin n → ℝ) (t : ℝ)
    (hx : boxContains B x) : boxContains (extendedBox B) (extendedPoint x t) := by
  intro i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · simp [extendedBox, extendedPoint, Coordinate.contains]
  · refine Fin.lastCases ?_ (fun j => ?_) j
    · simp [extendedBox, Coordinate.contains]
    · simpa [extendedBox, extendedPoint] using hx j

def extendedIntegers (p : Propagation.Problem n) : Fin (n + 2) → Bool :=
  Fin.snoc (Fin.snoc (fun i => decide (i ∈ p.integers ∨ i ∈ p.binaries)) false) false

theorem extendedPoint_integral (p : Propagation.Problem n) (x : Fin n → ℝ) (t : ℝ)
    (hx : p.Feasible x) : Integral (extendedIntegers p) (extendedPoint x t) := by
  intro i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · simp [extendedIntegers]
  · refine Fin.lastCases ?_ (fun j => ?_) j
    · simp [extendedIntegers]
    · simp only [extendedIntegers, Fin.snoc_castSucc, decide_eq_true_eq]
      intro hj
      simp only [extendedPoint, Fin.snoc_castSucc]
      rcases hj with hj | hj
      · exact hx.2.2.1 j hj
      · rcases hx.2.2.2.1 j hj with h | h
        · exact ⟨0, by simpa using h⟩
        · exact ⟨1, by simpa using h⟩

def coordinateRow (i : Fin (n + 2)) (q : ℚ) (kind : Kind) : Row (n + 2) :=
  ⟨fun j => if j = i then 1 else 0, q, kind⟩

theorem coordinateRow_holds (i : Fin (n + 2)) (q : ℚ) (kind : Kind)
    (y : Fin (n + 2) → ℝ) : Holds (coordinateRow i q kind) y ↔ Rel kind (y i) q := by
  simp [Holds, value, coordinateRow, apply_ite]

def affineRow (r : Propagation.Row n) : Row (n + 2) :=
  ⟨Fin.snoc (Fin.snoc r.coeff 0) 0, r.rhs, if r.upper then .le else .ge⟩

theorem affineRow_holds (r : Propagation.Row n) (x : Fin n → ℝ) (t : ℝ) :
    Holds (affineRow r) (extendedPoint x t) ↔ r.Holds x := by
  simp only [Holds, value, affineRow, extendedPoint, Fin.sum_univ_castSucc,
    Fin.snoc_castSucc, Fin.snoc_last, Rat.cast_zero, zero_mul, add_zero]
  cases h : r.upper <;> simp [h, Discrete.Rel, Propagation.Row.Holds]

def instructionRow (s : Propagation.Instruction n) : Row (n + 2) :=
  coordinateRow s.coord.castSucc.castSucc s.bound (if s.upper then .le else .ge)

theorem instructionRow_holds (s : Propagation.Instruction n) (x : Fin n → ℝ) (t : ℝ) :
    Holds (instructionRow s) (extendedPoint x t) ↔ s.Holds x := by
  rw [instructionRow, coordinateRow_holds]
  cases h : s.upper <;> simp [Discrete.Rel, Propagation.Instruction.Holds, h, extendedPoint]

inductive CutTarget (k : ℕ) where
  | constraint (index : Fin k)
  | objective

def targetExpression (rows : Fin k → (Fin n → ℝ) → ℝ) (f : (Fin n → ℝ) → ℝ)
    (target : CutTarget k) (y : Fin (n + 2) → ℝ) : ℝ :=
  match target with
  | .constraint j => rows j (originalPoint y)
  | .objective => f (originalPoint y) - y (Fin.last n).castSucc

/-- Each row's reason consists of original rational data, admitted propagation,
or analytic/enclosure evidence for a specified original or epigraph row. -/
inductive JustifiedRow (p : Propagation.Problem n) (B : Fin n → Coordinate)
    (rows : Fin k → (Fin n → ℝ) → ℝ) (f : (Fin n → ℝ) → ℝ) : Row (n + 2) → Prop where
  | original (r : Propagation.Row n) (hr : r ∈ p.rows) :
      JustifiedRow p B rows f (affineRow r)
  | bound (s : Propagation.Instruction n) (hs : Propagation.Admitted p B s) :
      JustifiedRow p B rows f (instructionRow s)
  | constant : JustifiedRow p B rows f (coordinateRow (Fin.last (n + 1)) 1 .eq)
  | cut (C : CutData (n + 2)) (target : CutTarget k)
      (hc : C.Accepted (extendedBox B))
      (heq : ∀ y, boxContains (extendedBox B) y →
        C.expression y = targetExpression rows f target y) :
      JustifiedRow p B rows f C.row
  | weaken (source target : Row (n + 2)) (hs : JustifiedRow p B rows f source)
      (hd : dominates source target = true) : JustifiedRow p B rows f target

theorem justifiedRow_holds (p : Propagation.Problem n) (B : Fin n → Coordinate)
    (rows : Fin k → (Fin n → ℝ) → ℝ) (f : (Fin n → ℝ) → ℝ)
    (trace : Propagation.Transcript p p.declared B) (r : Row (n + 2))
    (hr : JustifiedRow p B rows f r) (x : Fin n → ℝ) (hx : x ∈ feasible p rows) :
    Holds r (extendedPoint x (f x)) := by
  have hB : boxContains B x := Propagation.propagation_preserves_feasible p B trace x hx.1
  have hE := extendedPoint_mem B x (f x) hB
  induction hr with
  | original r hr => exact (affineRow_holds r x (f x)).mpr (hx.1.2.1 r hr)
  | bound s hs =>
    exact (instructionRow_holds s x (f x)).mpr
      (Propagation.admitted_sound p B s hs x hx.1 hB)
  | constant => simp [coordinateRow_holds, Discrete.Rel]
  | cut C target hc heq =>
    apply C.row_valid hc hE
    rw [heq _ hE]
    cases target with
    | constraint j => simpa [targetExpression] using hx.2 j
    | objective => simp [targetExpression]
  | weaken source target _ hd ih => exact dominates_sound hd ih

theorem graph_master_feasible (p : Propagation.Problem n) (B : Fin n → Coordinate)
    (rows : Fin k → (Fin n → ℝ) → ℝ) (f : (Fin n → ℝ) → ℝ)
    (trace : Propagation.Transcript p p.declared B) (master : List (Row (n + 2)))
    (hm : ∀ r ∈ master, JustifiedRow p B rows f r) :
    ∀ x ∈ feasible p rows,
      extendedPoint x (f x) ∈ masterFeasible master (extendedIntegers p) := by
  intro x hx
  exact ⟨extendedPoint_integral p x (f x) hx.1,
    fun r hr => justifiedRow_holds p B rows f trace r (hm r hr) x hx⟩

def epigraphObjective (n : ℕ) : Fin (n + 2) → ℚ :=
  Fin.snoc (Fin.snoc (fun _ => 0) 1) 0

theorem epigraphObjective_value (x : Fin n → ℝ) (t : ℝ) :
    objective (epigraphObjective n) (extendedPoint x t) = t := by
  simp [objective, epigraphObjective, extendedPoint, Fin.sum_univ_castSucc]

/-- The checker, propagation trace, and cut evidence yield a bound for the
original nonlinear feasible set without assuming the final embedding. -/
theorem checked_nonlinear_bound (p : Propagation.Problem n) (B : Fin n → Coordinate)
    (rows : Fin k → (Fin n → ℝ) → ℝ) (f : (Fin n → ℝ) → ℝ)
    (trace : Propagation.Transcript p p.declared B) (master : List (Row (n + 2)))
    (hm : ∀ r ∈ master, JustifiedRow p B rows f r) (β : ℚ)
    (solutions : List (Fin (n + 2) → ℚ)) (steps : List (Step (n + 2)))
    (hc : checkBound master (extendedIntegers p) (epigraphObjective n) β solutions steps = true) :
    LowerBoundOn (feasible p rows) f β := by
  intro x hx
  have h := checked_bound hc (extendedPoint x (f x))
    (graph_master_feasible p B rows f trace master hm x hx)
  simpa only [epigraphObjective_value] using h

def affineObjective (a : Fin n → ℚ) (c : ℚ) : Fin (n + 2) → ℚ :=
  Fin.snoc (Fin.snoc a 0) c

theorem affineObjective_value (a : Fin n → ℚ) (c : ℚ) (x : Fin n → ℝ) (t : ℝ) :
    objective (affineObjective a c) (extendedPoint x t) =
      affine (fun j => (a j : ℝ)) c x := by
  simp [objective, affineObjective, extendedPoint, Fin.sum_univ_castSucc, affine, dot]

theorem checked_affine_bound (p : Propagation.Problem n) (B : Fin n → Coordinate)
    (rows : Fin k → (Fin n → ℝ) → ℝ) (a : Fin n → ℚ) (c : ℚ)
    (trace : Propagation.Transcript p p.declared B) (master : List (Row (n + 2)))
    (hm : ∀ r ∈ master, JustifiedRow p B rows (affine (fun j => (a j : ℝ)) c) r) (β : ℚ)
    (solutions : List (Fin (n + 2) → ℚ)) (steps : List (Step (n + 2)))
    (hc : checkBound master (extendedIntegers p) (affineObjective a c) β solutions steps = true) :
    LowerBoundOn (feasible p rows) (affine (fun j => (a j : ℝ)) c) β := by
  intro x hx
  have h := checked_bound hc (extendedPoint x (affine (fun j => (a j : ℝ)) c x))
    (graph_master_feasible p B rows _ trace master hm x hx)
  simpa only [affineObjective_value] using h

/-- A checked master bijection and row matching are composed with the nonlinear
embedding and the actual discrete certificate. Any objective encoding may be
used once its explicit value identity is proved. -/
theorem checked_matched_objective_bound {m : ℕ}
    (p : Propagation.Problem n) (B : Fin n → Coordinate)
    (rows : Fin k → (Fin n → ℝ) → ℝ) (f : (Fin n → ℝ) → ℝ)
    (trace : Propagation.Transcript p p.declared B) (master : List (Row (n + 2)))
    (hm : ∀ r ∈ master, JustifiedRow p B rows f r) (c : Fin (n + 2) → ℚ)
    (hobjective : ∀ x, objective c (extendedPoint x (f x)) = f x)
    (e : Fin (n + 2) ≃ Fin m) (target : MasterIdentity.Master m)
    (witness : List (ℚ × Row (n + 2)))
    (hmatch : MasterIdentity.checkMaster e
      ⟨master, extendedIntegers p, c, 0⟩ target witness = true)
    (β : ℚ) (solutions : List (Fin m → ℚ)) (steps : List (Step m))
    (hcheck : checkBound target.rows target.integers target.objectiveCoeff
      β solutions steps = true) :
    LowerBoundOn (feasible p rows) f β := by
  intro x hx
  let y := extendedPoint x (f x)
  have hy : (MasterIdentity.Master.mk master (extendedIntegers p) c 0).Feasible y :=
    graph_master_feasible p B rows f trace master hm x hx
  have ht := (MasterIdentity.matches_feasible e _ target witness hmatch y).mpr hy
  have hb := checked_bound hcheck (MasterIdentity.renamePoint e y) ht
  have ho := MasterIdentity.matches_objective e _ target witness hmatch y
  have hzero : target.objectiveConstant = 0 := (of_decide_eq_true hmatch).2.2.2.2.2
  simp only [MasterIdentity.Master.objective, hzero, Rat.cast_zero, add_zero] at ho
  change objective target.objectiveCoeff (MasterIdentity.renamePoint e y) = objective c y at ho
  rw [ho, hobjective] at hb
  exact hb

theorem checked_matched_nonlinear_bound {m : ℕ}
    (p : Propagation.Problem n) (B : Fin n → Coordinate)
    (rows : Fin k → (Fin n → ℝ) → ℝ) (f : (Fin n → ℝ) → ℝ)
    (trace : Propagation.Transcript p p.declared B) (master : List (Row (n + 2)))
    (hm : ∀ r ∈ master, JustifiedRow p B rows f r)
    (e : Fin (n + 2) ≃ Fin m) (target : MasterIdentity.Master m)
    (witness : List (ℚ × Row (n + 2)))
    (hmatch : MasterIdentity.checkMaster e
      ⟨master, extendedIntegers p, epigraphObjective n, 0⟩ target witness = true)
    (β : ℚ) (solutions : List (Fin m → ℚ)) (steps : List (Step m))
    (hcheck : checkBound target.rows target.integers target.objectiveCoeff
      β solutions steps = true) :
    LowerBoundOn (feasible p rows) f β :=
  checked_matched_objective_bound p B rows f trace master hm (epigraphObjective n)
    (fun x => epigraphObjective_value x (f x)) e target witness hmatch β solutions steps hcheck

theorem checked_nonlinear_max_bound (p : Propagation.Problem n) (B : Fin n → Coordinate)
    (rows : Fin k → (Fin n → ℝ) → ℝ) (f : (Fin n → ℝ) → ℝ)
    (trace : Propagation.Transcript p p.declared B) (master : List (Row (n + 2)))
    (hm : ∀ r ∈ master, JustifiedRow p B rows (fun x => -f x) r) (β : ℚ)
    (solutions : List (Fin (n + 2) → ℚ)) (steps : List (Step (n + 2)))
    (hc : checkBound master (extendedIntegers p) (epigraphObjective n) β solutions steps = true) :
    ∀ x ∈ feasible p rows, f x ≤ -(β : ℝ) := by
  intro x hx
  have h := checked_nonlinear_bound p B rows (fun x => -f x) trace master hm
    β solutions steps hc x hx
  linarith

theorem checked_nonlinear_infeasible (p : Propagation.Problem n) (B : Fin n → Coordinate)
    (rows : Fin k → (Fin n → ℝ) → ℝ) (f : (Fin n → ℝ) → ℝ)
    (trace : Propagation.Transcript p p.declared B) (master : List (Row (n + 2)))
    (hm : ∀ r ∈ master, JustifiedRow p B rows f r) (steps : List (Step (n + 2)))
    (hc : checkInfeasible master (extendedIntegers p) steps = true) : feasible p rows = ∅ := by
  exact infeasible_master_transfer (feasible p rows)
    (masterFeasible master (extendedIntegers p)) (fun x => extendedPoint x (f x))
    (graph_master_feasible p B rows f trace master hm) (checked_infeasible hc)

end CertifiedModel
end CertifiedMinlp
