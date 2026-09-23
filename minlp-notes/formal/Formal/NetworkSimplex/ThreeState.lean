import Formal.NetworkSimplex.FiveTests

/-! Exact feasibility tests for the three-state profile normal system. -/

namespace NetworkSimplex

structure ThreeStateBounds where
  l1 : ℝ
  l2 : ℝ
  l3 : ℝ
  ls : ℝ
  u1 : ℝ
  u2 : ℝ
  u3 : ℝ
  u12 : ℝ
  u13 : ℝ
  u23 : ℝ
  us : ℝ

namespace ThreeStateBounds

def Feasible (b : ThreeStateBounds) (x y z : ℝ) : Prop :=
  b.l1 ≤ x ∧ x ≤ b.u1 ∧ b.l2 ≤ y ∧ y ≤ b.u2 ∧ b.l3 ≤ z ∧ z ≤ b.u3 ∧
  x + y ≤ b.u12 ∧ x + z ≤ b.u13 ∧ y + z ≤ b.u23 ∧
  b.ls ≤ x + y + z ∧ x + y + z ≤ b.us

/-- Seven subset lower tests, five partition tests, three overlapping-pair tests,
and the one twice-total test. -/
def SixteenTests (b : ThreeStateBounds) : Prop :=
  b.l1 ≤ b.u1 ∧ b.l2 ≤ b.u2 ∧ b.l3 ≤ b.u3 ∧
  b.l1 + b.l2 ≤ b.u12 ∧ b.l1 + b.l3 ≤ b.u13 ∧ b.l2 + b.l3 ≤ b.u23 ∧
  b.l1 + b.l2 + b.l3 ≤ b.us ∧
  b.ls ≤ b.us ∧ b.ls ≤ b.u1 + b.u23 ∧ b.ls ≤ b.u2 + b.u13 ∧
  b.ls ≤ b.u3 + b.u12 ∧ b.ls ≤ b.u1 + b.u2 + b.u3 ∧
  b.ls + b.l1 ≤ b.u12 + b.u13 ∧ b.ls + b.l2 ≤ b.u12 + b.u23 ∧
  b.ls + b.l3 ≤ b.u13 + b.u23 ∧ 2 * b.ls ≤ b.u12 + b.u13 + b.u23

theorem feasible_implies_tests {b : ThreeStateBounds} {x y z : ℝ}
    (h : b.Feasible x y z) : b.SixteenTests := by
  rcases h with ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11⟩
  unfold SixteenTests
  and_intros <;> linarith

theorem tests_imply_feasible {b : ThreeStateBounds} (h : b.SixteenTests) :
    ∃ x y z, b.Feasible x y z := by
  rcases h with ⟨h1, h2, h3, h12, h13, h23, hs, hss, hs1, hs2, hs3,
    hs123, hsp1, hsp2, hsp3, hsp⟩
  have hfive : FiveTests (max b.l1 (b.ls - b.u23)) (min b.u1 (b.u13 - b.l3))
      (max b.l2 (b.ls - b.u13)) (min b.u2 (b.u23 - b.l3))
      (b.ls - b.u3) (min b.u12 (b.us - b.l3)) := by
    unfold FiveTests
    and_intros
    all_goals simp only [max_def, min_def]; split_ifs <;> linarith
  obtain ⟨x, y, hxy⟩ := (five_tests_iff_feasible _ _ _ _ _ _).mp hfive
  rcases hxy with ⟨hxlo, hxhi, hylo, hyhi, hslo, hshi⟩
  simp only [max_le_iff, le_min_iff] at hxlo hxhi hylo hyhi hshi
  refine ⟨x, y, max b.l3 (b.ls - x - y), ?_⟩
  unfold Feasible
  rcases hxlo with ⟨hxlo1, hxlo2⟩
  rcases hxhi with ⟨hxhi1, hxhi2⟩
  rcases hylo with ⟨hylo1, hylo2⟩
  rcases hyhi with ⟨hyhi1, hyhi2⟩
  rcases hshi with ⟨hshi1, hshi2⟩
  simp only [max_def]
  split_ifs <;> (and_intros <;> linarith)

/-- The sixteen fixed tests completely characterize this profile region. -/
theorem sixteen_tests_iff_feasible (b : ThreeStateBounds) :
    b.SixteenTests ↔ ∃ x y z, b.Feasible x y z := by
  exact ⟨tests_imply_feasible, fun ⟨x, y, z, h⟩ => feasible_implies_tests h⟩

end ThreeStateBounds
end NetworkSimplex
