import Formal.CompetitiveBranching.Model

/-!
# Basic facts and the key inequality

* `Valid.mono`: validity passes to sub-intervals.
* `node_facts` (Lemma 1(i)): at an internal node, `phi < 0` at the split point,
  and the split point is interior.
* `key_left` and `key_right` (Lemma 2 and its mirror). The hypotheses are
  weaker than in the note: the inner node `B₂` only has to lie in the child of
  `B₁` on the side of its split point; it need not contain the breakpoint.
-/

open Set

noncomputable section

namespace CompetitiveBranching

variable {m : ℝ → ℝ} {α : ℝ}

/-- Validity passes to sub-intervals. -/
theorem Valid.mono {a b l u : ℝ} (hα : 0 ≤ α) (h : Valid m α a b)
    (hl : a ≤ l) (hu : u ≤ b) : Valid m α l u := by
  intro y hy
  have hy' : y ∈ Icc a b := ⟨hl.trans hy.1, hy.2.trans hu⟩
  have h1 := h y hy'
  simp only [phi, q] at h1 ⊢
  have h2 : (y - l) * (u - y) ≤ (y - a) * (b - y) :=
    mul_le_mul (by linarith) (by linarith) (by linarith [hy.2]) (by linarith [hy'.1])
  nlinarith [mul_le_mul_of_nonneg_left h2 hα]

/-- Lemma 1(i): an internal node has `phi < 0` at its split point, which is
interior because `m > 0` at the endpoints. -/
theorem node_facts {l u y : ℝ} (hpos : ∀ z ∈ Icc l u, 0 < m z)
    (hnv : ¬ Valid m α l u) (hy : y ∈ Icc l u)
    (hmin : IsMinOn (phi m α l u) (Icc l u) y) :
    phi m α l u y < 0 ∧ l < y ∧ y < u := by
  have hneg : phi m α l u y < 0 := by
    by_contra h
    exact hnv fun z hz => (not_lt.mp h).trans (isMinOn_iff.mp hmin z hz)
  have hmy := hpos y hy
  refine ⟨hneg, lt_of_le_of_ne hy.1 ?_, lt_of_le_of_ne hy.2 ?_⟩
  · intro h
    subst h
    simp only [phi, q, sub_self, zero_mul, mul_zero, sub_zero] at hneg
    linarith
  · intro h
    subst h
    simp only [phi, q, sub_self, mul_zero, sub_zero] at hneg
    linarith

/-- Lemma 2. Let `y₁` minimize `phi` over `B₁ = [l₁, u₁]`, and let
`B₂ = [l₂, u₂] ⊆ [l₁, y₁]` have `phi_{B₂}(y₂) < 0` at a point `y₂ ∈ B₂`. If
`a < y₂ < y₁ < b` and `[a, b]` is valid, then `b < u₁`. -/
theorem key_left {a b l₁ y₁ u₁ l₂ y₂ u₂ : ℝ} (hα : 0 < α)
    (hmin : IsMinOn (phi m α l₁ u₁) (Icc l₁ u₁) y₁) (hy₁u : y₁ ≤ u₁)
    (hl : l₁ ≤ l₂) (hy₂l : l₂ ≤ y₂) (hy₂u : y₂ ≤ u₂) (hu : u₂ ≤ y₁)
    (hneg : phi m α l₂ u₂ y₂ < 0) (hJ : Valid m α a b)
    (ha : a < y₂) (h12 : y₂ < y₁) (hb : y₁ < b) : b < u₁ := by
  by_contra hub
  replace hub := not_lt.mp hub
  have F1 := isMinOn_iff.mp hmin y₂ ⟨hl.trans hy₂l, hy₂u.trans (hu.trans hy₁u)⟩
  have F3 := hJ y₁ ⟨(ha.trans h12).le, hb.le⟩
  simp only [phi, q] at F1 F3 hneg
  have P : (y₂ - l₂) * (u₂ - y₂) ≤ (y₂ - l₁) * (y₁ - y₂) :=
    mul_le_mul (by linarith) (by linarith) (by linarith) (by linarith)
  have P' := mul_le_mul_of_nonneg_left P hα.le
  -- The three facts and the bilinear identity combine to this inequality.
  have key : α * ((y₁ - a) * (b - y₁)) < α * ((y₁ - y₂) * (u₁ - y₁)) := by
    linarith
  have key' : (y₁ - a) * (b - y₁) < (y₁ - y₂) * (u₁ - y₁) :=
    lt_of_mul_lt_mul_left key hα.le
  have Q1 : (y₁ - y₂) * (u₁ - y₁) ≤ (y₁ - y₂) * (b - y₁) :=
    mul_le_mul_of_nonneg_left (by linarith) (by linarith)
  have Q2 : (y₁ - y₂) * (b - y₁) ≤ (y₁ - a) * (b - y₁) :=
    mul_le_mul_of_nonneg_right (by linarith) (by linarith)
  linarith

/-- Mirror of Lemma 2. Let `y₁` minimize `phi` over `B₁ = [l₁, u₁]`, and let
`B₂ = [l₂, u₂] ⊆ [y₁, u₁]` have `phi_{B₂}(y₂) < 0` at a point `y₂ ∈ B₂`. If
`a < y₁ < y₂ < b` and `[a, b]` is valid, then `l₁ < a`. -/
theorem key_right {a b l₁ y₁ u₁ l₂ y₂ u₂ : ℝ} (hα : 0 < α)
    (hmin : IsMinOn (phi m α l₁ u₁) (Icc l₁ u₁) y₁) (hly₁ : l₁ ≤ y₁)
    (hl : y₁ ≤ l₂) (hy₂l : l₂ ≤ y₂) (hy₂u : y₂ ≤ u₂) (hu : u₂ ≤ u₁)
    (hneg : phi m α l₂ u₂ y₂ < 0) (hJ : Valid m α a b)
    (ha : a < y₁) (h12 : y₁ < y₂) (hb : y₂ < b) : l₁ < a := by
  by_contra hal
  replace hal := not_lt.mp hal
  have F1 := isMinOn_iff.mp hmin y₂ ⟨hly₁.trans (hl.trans hy₂l), hy₂u.trans hu⟩
  have F3 := hJ y₁ ⟨ha.le, (h12.trans hb).le⟩
  simp only [phi, q] at F1 F3 hneg
  have P : (y₂ - l₂) * (u₂ - y₂) ≤ (y₂ - y₁) * (u₁ - y₂) :=
    mul_le_mul (by linarith) (by linarith) (by linarith) (by linarith)
  have P' := mul_le_mul_of_nonneg_left P hα.le
  have key : α * ((y₁ - a) * (b - y₁)) < α * ((y₂ - y₁) * (y₁ - l₁)) := by
    linarith
  have key' : (y₁ - a) * (b - y₁) < (y₂ - y₁) * (y₁ - l₁) :=
    lt_of_mul_lt_mul_left key hα.le
  have Q1 : (y₂ - y₁) * (y₁ - l₁) ≤ (y₂ - y₁) * (y₁ - a) :=
    mul_le_mul_of_nonneg_left (by linarith) (by linarith)
  have Q2 : (y₂ - y₁) * (y₁ - a) ≤ (b - y₁) * (y₁ - a) :=
    mul_le_mul_of_nonneg_right (by linarith) (by linarith)
  linarith

end CompetitiveBranching
