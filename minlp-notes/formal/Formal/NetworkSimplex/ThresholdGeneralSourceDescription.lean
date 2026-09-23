import Formal.NetworkSimplex.ThresholdGeneralCoefficients

/-! A finite exact affine description using only original source rows. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold

/-- All choices are finite: at most m+1 source rows and bounded natural weights. -/
abbrev GeneralSourceBranch (m : ℕ) (I : Type*) :=
  Σ s : Fin (m + 2), (Fin s.val → ProfileRow m I) ×
    (Fin s.val → Fin (delta01 m + 1))

theorem generalSourceBranch_finite {m : ℕ} {I : Type*} [Finite I] :
    Finite (GeneralSourceBranch m I) := by
  let : Fintype I := Fintype.ofFinite I
  infer_instance

def GeneralSourceBranch.cancels {m : ℕ} {I : Type*}
    (D : ReductionData m I) (b : GeneralSourceBranch m I) : Prop :=
  ∀ j, ∑ i, (b.2.2 i : ℤ) * normalVector (D.rowNormal (b.2.1 i)) j = 0

def GeneralSourceBranch.value {m : ℕ} {I : Type*}
    (D : ReductionData m I) (b : GeneralSourceBranch m I) : ℝ :=
  ∑ i, (b.2.2 i : ℝ) * D.rowRhs (b.2.1 i)

def GeneralSourceTests {m : ℕ} {I : Type*} (D : ReductionData m I) : Prop :=
  ∀ b : GeneralSourceBranch m I, b.cancels D → 0 ≤ b.value D

theorem sourceNormals_rowSignedZeroOne {m : ℕ} {I : Type*}
    (D : ReductionData m I) : RowSignedZeroOne (fun r => normalVector (D.rowNormal r)) := by
  intro r
  cases he : D.rowNormal r with
  | subset s => left; intro j; simp only [he, normalVector]; split_ifs <;> simp
  | negativeSingleton k => right; intro j; simp only [he, normalVector]; split_ifs <;> simp
  | negativeTotal => right; intro j; simp [he, normalVector]

/-- The finite bounded branch family is exactly profile feasibility. Zero rows
are tested by its one-row branches; absent normal groups need no added rows. -/
theorem general_source_tests_iff_profile {m : ℕ} {I : Type*} [Finite I]
    (D : ReductionData m I) :
    GeneralSourceTests D ↔ ∃ x : Fin m → ℝ, D.ReducedProfile x := by
  let : Fintype I := Fintype.ofFinite I
  constructor
  · intro ht
    have hex := (feasible_iff_bounded_integer_tests
      (fun r => normalVector (D.rowNormal r)) (sourceNormals_rowSignedZeroOne D)
      D.rowRhs).mpr (by
        intro s hs rows p hp _ hc
        let b : GeneralSourceBranch m I :=
          ⟨⟨s, by omega⟩, rows, fun i => ⟨p i, by have h := (hp i).2; omega⟩⟩
        exact ht b hc)
    obtain ⟨x, hx⟩ := hex
    refine ⟨x, (D.rows_iff_reducedProfile x).mp ?_⟩
    intro r
    simpa only [profileNormal_value_eq_dot] using hx r
  · rintro ⟨x, hx⟩ b hb
    exact integer_cancel_valid (fun r => normalVector (D.rowNormal r)) D.rowRhs
      b.2.1 (fun i => (b.2.2 i).val) hb (x := x) (fun r => by
        simpa only [← profileNormal_value_eq_dot] using (D.rows_iff_reducedProfile x).mpr hx r)

/-- This is an exact finite family in the original graph coordinates. -/
theorem general_mem_hull_iff_source_tests {L m : ℕ} (D : ReductionData m (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔ D.OriginalDomain ∧ GeneralSourceTests D := by
  rw [D.mem_hull_iff, general_source_tests_iff_profile]
  rw [D.exists_fullProfile_iff_rows hc hh]
  exact and_congr_right fun _ => exists_congr fun x => D.rows_iff_reducedProfile x

/-- A fixed affine syntax tree for the expanded branch, using repeated addition. -/
def GeneralSourceBranch.expression {m : ℕ} {I : Type*}
    (D : ReductionData m I) (b : GeneralSourceBranch m I) : AffineExpression (Coordinate m I) :=
  AffineExpression.sum fun i =>
    AffineExpression.sum fun _ : Fin (b.2.2 i).val => rowExpression D (b.2.1 i)

theorem GeneralSourceBranch.expression_eval {m : ℕ} {I : Type*}
    (D E : ReductionData m I) (b : GeneralSourceBranch m I) (xb : I → ℝ)
    (hpattern : D.c = E.c) (hh : D.observedH = E.observedH)
    (hc : ∀ i, E.c i 0 = .neither) :
    (b.expression D).eval (coordinates E xb) = b.value E := by
  simp [GeneralSourceBranch.expression, GeneralSourceBranch.value,
    rowExpression_eval_other D E xb hpattern hh hc]

theorem GeneralSourceBranch.expression_coefficient {m : ℕ} {I : Type*} [DecidableEq I]
    (D : ReductionData m I) (b : GeneralSourceBranch m I) (z : Coordinate m I) :
    (b.expression D).coefficient z =
      ∑ i, (b.2.2 i : ℤ) * rowCoefficient D (b.2.1 i) z := by
  simp [GeneralSourceBranch.expression, rowCoefficient]

/-- Every member has the actual original-coordinate determinant coefficient bound. -/
theorem GeneralSourceBranch.coefficient_bound {m : ℕ} {I : Type*} [DecidableEq I]
    (D : ReductionData m I) (b : GeneralSourceBranch m I)
    (z : Coordinate m I) (hz : FlowOrProduct z) :
    |∑ i, (b.2.2 i : ℤ) * rowCoefficient D (b.2.1 i) z| ≤
      ((m + 1) * delta01 m : ℕ) :=
  sourceBranch_coefficient_bound D b.2.1 (fun i => (b.2.2 i).val)
    (by have h := b.1.isLt; omega) (fun i => by have h := (b.2.2 i).isLt; omega) z hz

end NetworkSimplex.Chain.Threshold
