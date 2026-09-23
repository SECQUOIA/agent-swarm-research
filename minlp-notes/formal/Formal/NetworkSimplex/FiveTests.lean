import Mathlib

namespace NetworkSimplex

def FiveTests (l₁ u₁ l₂ u₂ ls us : ℝ) : Prop :=
  l₁ ≤ u₁ ∧ l₂ ≤ u₂ ∧ ls ≤ us ∧ l₁ + l₂ ≤ us ∧ ls ≤ u₁ + u₂

def Hexagon (l₁ u₁ l₂ u₂ ls us x y : ℝ) : Prop :=
  l₁ ≤ x ∧ x ≤ u₁ ∧ l₂ ≤ y ∧ y ≤ u₂ ∧ ls ≤ x + y ∧ x + y ≤ us

/-- The formula in the paper constructs a feasible point from the five tests. -/
theorem five_tests_witness {l₁ u₁ l₂ u₂ ls us : ℝ}
    (h : FiveTests l₁ u₁ l₂ u₂ ls us) :
    Hexagon l₁ u₁ l₂ u₂ ls us
      (max l₁ (max ls (l₁+l₂) - u₂))
      (max ls (l₁+l₂) - max l₁ (max ls (l₁+l₂) - u₂)) := by
  rcases h with ⟨h₁, h₂, hs, hlow, hhigh⟩
  let s := max ls (l₁+l₂)
  let x := max l₁ (s-u₂)
  have hsl : ls ≤ s := le_max_left _ _
  have hsum : l₁+l₂ ≤ s := le_max_right _ _
  have hsu : s ≤ us := max_le hs hlow
  have hst : s ≤ u₁+u₂ := max_le hhigh (by linarith)
  have hxl : l₁ ≤ x := le_max_left _ _
  have hxu : x ≤ u₁ := max_le h₁ (by linarith)
  have hxy : x ≤ s-l₂ := max_le (by linarith) (by linarith)
  have hxy' : s-u₂ ≤ x := le_max_right _ _
  change Hexagon l₁ u₁ l₂ u₂ ls us x (s-x)
  unfold Hexagon
  exact ⟨hxl, hxu, by linarith, by linarith, by linarith, by linarith⟩

/-- Exact feasibility, including empty intervals and lower-dimensional regions. -/
theorem five_tests_iff_feasible (l₁ u₁ l₂ u₂ ls us : ℝ) :
    FiveTests l₁ u₁ l₂ u₂ ls us ↔ ∃ x y, Hexagon l₁ u₁ l₂ u₂ ls us x y := by
  constructor
  · intro h
    exact ⟨_, _, five_tests_witness h⟩
  · rintro ⟨x, y, hx₁, hx₂, hy₁, hy₂, hs₁, hs₂⟩
    unfold FiveTests
    exact ⟨by linarith, by linarith, by linarith, by linarith, by linarith⟩

end NetworkSimplex
