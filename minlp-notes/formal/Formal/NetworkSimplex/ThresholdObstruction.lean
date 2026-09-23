import Formal.NetworkSimplex.ProfileHull

/-! The seven-observation four-label obstruction on the actual five-vertex chain. -/
namespace NetworkSimplex.Chain.ThresholdObstruction
open scoped BigOperators
open StateClass
noncomputable section

/-- Four allowed sets: {0,1,2}, {0,3}, {1,3}, and {2,3}. -/
def classes : Fin 4 → Fin 4 → StateClass :=
  ![![neither, neither, neither, aOnly],
    ![neither, aOnly, aOnly, neither],
    ![aOnly, neither, aOnly, neither],
    ![aOnly, aOnly, neither, neither]]

def observedA (U V : ℝ) : Fin 4 → Fin 4 → ℝ :=
  ![![0, 0, 0, U], ![0, V, 1 / 32, 0],
    ![1 / 32, 0, 1 / 32, 0], ![1 / 32, 1 / 32, 0, 0]]

def aggregateA : Fin 4 → ℝ := ![13 / 32, 5 / 16, 5 / 16, 5 / 16]
def aggregateB (i : Fin 4) : ℝ := 1 / 2 - aggregateA i

def sectionPoint (U V : ℝ) :=
  chainPoint classes (observedA U V) (fun _ _ => 0) (fun _ => 1 / 4)
    aggregateA aggregateB (1 / 2) (fun _ => False) (fun _ => 0)

def obstructionGraph := chainGraph classes (fun _ => False)

def Near (U V : ℝ) : Prop := |U - 1 / 32| < 1 / 128 ∧ |V - 1 / 32| < 1 / 128

theorem near_bounds {U V : ℝ} (h : Near U V) :
    -(1 / 128 : ℝ) < U - 1 / 32 ∧ U - 1 / 32 < 1 / 128 ∧
      -(1 / 128 : ℝ) < V - 1 / 32 ∧ V - 1 / 32 < 1 / 128 :=
  ⟨(abs_lt.mp h.1).1, (abs_lt.mp h.1).2, (abs_lt.mp h.2).1, (abs_lt.mp h.2).2⟩

theorem observed_nonnegative {U V : ℝ} (h : Near U V) :
    ∀ i, ObservedNonnegative (classes i) (observedA U V i) (fun _ => 0) := by
  obtain ⟨hU₀, _, hV₀, _⟩ := near_bounds h
  intro i
  constructor
  · intro j hj
    fin_cases i <;> fin_cases j <;>
      norm_num [classes, observesA, observedA] at hj ⊢ <;> linarith
  · intro j _
    norm_num

/-- Necessary common-profile rows yield the coefficient-two inequality. -/
theorem profile_necessary {U V : ℝ} {w : Fin 4 → ℝ}
    (h : Profile classes (observedA U V) (fun _ _ => 0) (fun _ => 1 / 4)
      aggregateA (1 / 2) (fun _ => False) (fun _ => 0) w) : 3 / 32 ≤ 2 * U + V := by
  have hs := h.2.1
  have h₀ := (h.2.2.2 0).2.2.2.2
  have h₁ := (h.2.2.2 1).2.2.2.2
  have h₂ := (h.2.2.2 2).2.2.2.2
  have h₃ := (h.2.2.2 3).2.2.2.2
  simp [bSum, residual, freeA, classes, observedA, aggregateA,
    observesA, Fin.sum_univ_four, Matrix.cons_val, reduceCtorEq] at h₀ h₁ h₂ h₃ hs
  linarith

/-- An affine common profile suffices on the entire nearby feasible half-plane. -/
def recoveryProfile (U : ℝ) : Fin 4 → ℝ :=
  ![1 / 8 + (U - 1 / 32), 1 / 8 - (U - 1 / 32), 1 / 8 - (U - 1 / 32), 1 / 8 + (U - 1 / 32)]

theorem profile_sufficient {U V : ℝ} (h : Near U V) (hedge : 3 / 32 ≤ 2 * U + V) :
    Profile classes (observedA U V) (fun _ _ => 0) (fun _ => 1 / 4)
      aggregateA (1 / 2) (fun _ => False) (fun _ => 0) (recoveryProfile U) := by
  obtain ⟨hU₀, hU₁, hV₀, hV₁⟩ := near_bounds h
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro j
    fin_cases j <;> norm_num [recoveryProfile] <;> constructor <;> linarith
  · norm_num [recoveryProfile, Fin.sum_univ_succ]
    ring
  · intro j hj
    exact hj.elim
  · intro i
    refine ⟨?_, ?_, ?_, ?_, ?_⟩
    · intro j hj
      fin_cases i <;> fin_cases j <;>
        norm_num [classes, observedA, recoveryProfile, reduceCtorEq] at hj ⊢ <;> linarith
    · intro j hj
      fin_cases i <;> fin_cases j <;> simp [classes, reduceCtorEq] at hj
    · intro j hj
      fin_cases i <;> fin_cases j <;> simp [classes, reduceCtorEq] at hj
    · fin_cases i <;>
        simp [bSum, residual, classes, observesA, observedA, aggregateA,
          recoveryProfile, Fin.sum_univ_four, Matrix.cons_val, reduceCtorEq] <;> linarith
    · fin_cases i <;>
        simp [bSum, residual, freeA, classes, observesA, observedA, aggregateA,
          recoveryProfile, Fin.sum_univ_four, Matrix.cons_val, reduceCtorEq] <;> linarith

/-- The section is a genuine section of the original bilinear graph hull. -/
theorem section_hull_iff {U V : ℝ} (h : Near U V) :
    sectionPoint U V ∈ convexHull ℝ obstructionGraph ↔ 3 / 32 ≤ 2 * U + V := by
  have hw : Simplex (fun _ : Fin 4 => (1 / 4 : ℝ)) := by
    constructor
    · intro j; norm_num
    · norm_num [Fin.sum_univ_succ]
  have ha : ∀ i, aggregateA i + aggregateB i = 1 - (1 / 2 : ℝ) := by
    intro i
    unfold aggregateB
    ring
  change chainPoint _ _ _ _ _ _ _ _ _ ∈ convexHull ℝ (chainGraph _ _) ↔ _
  rw [mem_chainHull_iff_profile _ _ _ _ _ _ _ _ _ hw ha (observed_nonnegative h)]
  exact ⟨fun ⟨w, hw⟩ => profile_necessary hw, fun he => ⟨_, profile_sufficient h he⟩⟩

end
end NetworkSimplex.Chain.ThresholdObstruction
