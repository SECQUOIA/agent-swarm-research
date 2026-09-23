import Formal.PotentialFlow.Bregman
import Formal.PotentialFlow.RationalBridge

/-! # Exact rational bisection of the Bregman sublevel boundary

This module formalizes obligation `CC06` of
`topics/16-potential-flow-certificates/CLAIMS.md`, the rational bisection of the proof of
`prop:a-cert-bregman`.

Starting from the verified outer bracket `y ± η` of `CC05`, each side of the sublevel set
`{z | D_e(y, z) ≤ δ}` is bisected with exact rational arithmetic. The candidate `y` is the
initial inner endpoint, the current outer endpoint is the one that still satisfies the
endpoint test `δ ≤ D_e(y, ·)`, and the midpoint replaces whichever endpoint preserves that
pattern. The test is the decidable rational inequality `δ ≤ ratBregman cp cm y mid`, so
`upperBracket` and `lowerBracket` are computable functions of the step count, defined by
structural recursion and using exact cubic rational evaluation only.

The proved content is:

* the bracket invariants: ordering of `y`, the inner endpoint, the outer endpoint and
  `y ± η`, the inner test `D ≤ δ` and the retained outer test `δ ≤ D`;
* the accuracy recursion `outer k - inner k = η / 2 ^ k`;
* the exact size recursion: both endpoints are dyadic points `y ± j * η / 2 ^ k` with a
  natural number `j`;
* soundness: for a rational network the two outer endpoints, cast to `ℝ`, enclose the
  physical flow on that edge, by `Network.mem_interval_of_edgeBregman` (`CC03`);
* boundary sharpness: an exact real boundary point `z*` with `D_e(y, z*) = δ` lies in every
  returned bracket, so the returned outer endpoint overshoots the exact sublevel boundary
  by at most `η / 2 ^ k`.

Neither the invariants nor boundary sharpness need any positivity or curvature hypothesis
on the edge coefficients; positivity enters only through the network soundness statement.
-/

namespace PotentialFlow

/-- The asymmetric cubic edge energy evaluated in exact rational arithmetic. -/
def ratEnergy (cp cm x : ℚ) : ℚ := (if 0 ≤ x then cp else cm) * |x| ^ 3 / 3

/-- The asymmetric cubic edge law evaluated in exact rational arithmetic. -/
def ratLaw (cp cm x : ℚ) : ℚ := (if 0 ≤ x then cp else cm) * x * |x|

/-- The edge Bregman divergence `D_e(y, z)` evaluated in exact rational arithmetic. -/
def ratBregman (cp cm y z : ℚ) : ℚ :=
  ratEnergy cp cm y - ratEnergy cp cm z - ratLaw cp cm z * (y - z)

/-- The rational edge energy is the real edge energy of the cast arguments. -/
theorem ratEnergy_cast (cp cm x : ℚ) :
    ((ratEnergy cp cm x : ℚ) : ℝ) = edgeEnergy (cp : ℝ) (cm : ℝ) (x : ℝ) := by
  by_cases hx : (0 : ℚ) ≤ x
  · have hx' : (0 : ℝ) ≤ (x : ℝ) := by exact_mod_cast hx
    simp only [ratEnergy, edgeEnergy, if_pos hx, if_pos hx']
    push_cast
    ring
  · have hx' : ¬ (0 : ℝ) ≤ (x : ℝ) := by
      simpa using hx
    simp only [ratEnergy, edgeEnergy, if_neg hx, if_neg hx']
    push_cast
    ring

/-- The rational edge law is the real edge law of the cast arguments. -/
theorem ratLaw_cast (cp cm x : ℚ) :
    ((ratLaw cp cm x : ℚ) : ℝ) = edgeLaw (cp : ℝ) (cm : ℝ) (x : ℝ) := by
  by_cases hx : (0 : ℚ) ≤ x
  · have hx' : (0 : ℝ) ≤ (x : ℝ) := by exact_mod_cast hx
    simp only [ratLaw, edgeLaw, if_pos hx, if_pos hx']
    push_cast
    ring
  · have hx' : ¬ (0 : ℝ) ≤ (x : ℝ) := by
      simpa using hx
    simp only [ratLaw, edgeLaw, if_neg hx, if_neg hx']
    push_cast
    ring

/-- The exact rational divergence agrees with `edgeBregman` after casting: the bisection
test is the real endpoint test of `CC03`, with no rounding. -/
theorem ratBregman_cast (cp cm y z : ℚ) :
    ((ratBregman cp cm y z : ℚ) : ℝ) = edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) (z : ℝ) := by
  simp only [ratBregman, edgeBregman, Rat.cast_sub, Rat.cast_mul, ratEnergy_cast, ratLaw_cast]

/-- The rational divergence vanishes on the diagonal. -/
@[simp] theorem ratBregman_self (cp cm y : ℚ) : ratBregman cp cm y y = 0 := by
  simp [ratBregman]

/-- The rational form of the initial bracket test `CC05`: the uniform radius endpoints
`y ± η` pass the divergence test as soon as `6δ ≤ η³ a` holds in `ℚ`. -/
theorem le_ratBregman_of_radius {cp cm a δ η : ℚ} (y : ℚ) (ha : 0 < a) (hcp : a ≤ cp)
    (hcm : a ≤ cm) (hη : 0 ≤ η) (hδ : 6 * δ ≤ η ^ 3 * a) :
    δ ≤ ratBregman cp cm y (y - η) ∧ δ ≤ ratBregman cp cm y (y + η) := by
  have h := le_edgeBregman_of_radius (cp := (cp : ℝ)) (cm := (cm : ℝ)) (a := (a : ℝ))
    (δ := (δ : ℝ)) (η := (η : ℝ)) (y : ℝ) (by exact_mod_cast ha) (by exact_mod_cast hcp)
    (by exact_mod_cast hcm) (by exact_mod_cast hη) (by exact_mod_cast hδ)
  constructor
  · have h₁ := h.1
    rw [show ((y : ℝ) - (η : ℝ)) = ((y - η : ℚ) : ℝ) by push_cast; ring, ← ratBregman_cast]
      at h₁
    exact_mod_cast h₁
  · have h₂ := h.2
    rw [show ((y : ℝ) + (η : ℝ)) = ((y + η : ℚ) : ℝ) by push_cast; ring, ← ratBregman_cast]
      at h₂
    exact_mod_cast h₂

/-- One bisection step on a pair `(inner, outer)`: the midpoint becomes the new outer
endpoint when it still passes the exact rational test `δ ≤ D_e(y, ·)`, and the new inner
endpoint otherwise. The step is the same on both sides of `y`. -/
def bisectStep (cp cm y δ : ℚ) (p : ℚ × ℚ) : ℚ × ℚ :=
  if δ ≤ ratBregman cp cm y ((p.1 + p.2) / 2) then (p.1, (p.1 + p.2) / 2)
  else ((p.1 + p.2) / 2, p.2)

/-- The bisection above `y`, returning the pair `(inner, outer)` after `k` steps. It starts
from the verified outer bracket `(y, y + η)` and is computable. -/
def upperBracket (cp cm y δ η : ℚ) : ℕ → ℚ × ℚ
  | 0 => (y, y + η)
  | k + 1 => bisectStep cp cm y δ (upperBracket cp cm y δ η k)

/-- The bisection below `y`, returning the pair `(inner, outer)` after `k` steps. It starts
from the verified outer bracket `(y, y - η)` and is computable. -/
def lowerBracket (cp cm y δ η : ℚ) : ℕ → ℚ × ℚ
  | 0 => (y, y - η)
  | k + 1 => bisectStep cp cm y δ (lowerBracket cp cm y δ η k)

/-- The upper bisection starts at the verified outer bracket `(y, y + η)`. -/
@[simp] theorem upperBracket_zero (cp cm y δ η : ℚ) :
    upperBracket cp cm y δ η 0 = (y, y + η) := rfl

/-- Each further upper step is one `bisectStep` on the current pair. -/
@[simp] theorem upperBracket_succ (cp cm y δ η : ℚ) (k : ℕ) :
    upperBracket cp cm y δ η (k + 1) = bisectStep cp cm y δ (upperBracket cp cm y δ η k) := rfl

/-- The lower bisection starts at the verified outer bracket `(y, y - η)`. -/
@[simp] theorem lowerBracket_zero (cp cm y δ η : ℚ) :
    lowerBracket cp cm y δ η 0 = (y, y - η) := rfl

/-- Each further lower step is one `bisectStep` on the current pair. -/
@[simp] theorem lowerBracket_succ (cp cm y δ η : ℚ) (k : ℕ) :
    lowerBracket cp cm y δ η (k + 1) = bisectStep cp cm y δ (lowerBracket cp cm y δ η k) := rfl

variable {cp cm y δ η : ℚ}

/-- The step preserves the upper-side bracket invariant and halves the bracket length. -/
private theorem bisectStep_invariant_upper (k : ℕ) {a b : ℚ} (h1 : y ≤ a) (h2 : a ≤ b)
    (h3 : b ≤ y + η) (h4 : ratBregman cp cm y a ≤ δ) (h5 : δ ≤ ratBregman cp cm y b)
    (h6 : b - a = η / 2 ^ k) :
    y ≤ (bisectStep cp cm y δ (a, b)).1 ∧
      (bisectStep cp cm y δ (a, b)).1 ≤ (bisectStep cp cm y δ (a, b)).2 ∧
      (bisectStep cp cm y δ (a, b)).2 ≤ y + η ∧
      ratBregman cp cm y (bisectStep cp cm y δ (a, b)).1 ≤ δ ∧
      δ ≤ ratBregman cp cm y (bisectStep cp cm y δ (a, b)).2 ∧
      (bisectStep cp cm y δ (a, b)).2 - (bisectStep cp cm y δ (a, b)).1 = η / 2 ^ (k + 1) := by
  have hne : ((2 : ℚ) ^ (k + 1)) ≠ 0 := by positivity
  have h6' : (b - a) * 2 ^ k = η := by
    rw [h6]
    field_simp
  have hlow : a ≤ (a + b) / 2 := by linarith
  have hhigh : (a + b) / 2 ≤ b := by linarith
  have hw1 : (a + b) / 2 - a = η / 2 ^ (k + 1) := by
    rw [eq_div_iff hne, pow_succ, ← h6']
    ring
  have hw2 : b - (a + b) / 2 = η / 2 ^ (k + 1) := by
    rw [eq_div_iff hne, pow_succ, ← h6']
    ring
  rw [bisectStep]
  split_ifs with hmid
  · exact ⟨h1, hlow, hhigh.trans h3, h4, hmid, hw1⟩
  · exact ⟨h1.trans hlow, hhigh, h3, (not_le.mp hmid).le, h5, hw2⟩

/-- The step preserves the lower-side bracket invariant and halves the bracket length. -/
private theorem bisectStep_invariant_lower (k : ℕ) {a b : ℚ} (h1 : a ≤ y) (h2 : b ≤ a)
    (h3 : y - η ≤ b) (h4 : ratBregman cp cm y a ≤ δ) (h5 : δ ≤ ratBregman cp cm y b)
    (h6 : a - b = η / 2 ^ k) :
    (bisectStep cp cm y δ (a, b)).1 ≤ y ∧
      (bisectStep cp cm y δ (a, b)).2 ≤ (bisectStep cp cm y δ (a, b)).1 ∧
      y - η ≤ (bisectStep cp cm y δ (a, b)).2 ∧
      ratBregman cp cm y (bisectStep cp cm y δ (a, b)).1 ≤ δ ∧
      δ ≤ ratBregman cp cm y (bisectStep cp cm y δ (a, b)).2 ∧
      (bisectStep cp cm y δ (a, b)).1 - (bisectStep cp cm y δ (a, b)).2 = η / 2 ^ (k + 1) := by
  have hne : ((2 : ℚ) ^ (k + 1)) ≠ 0 := by positivity
  have h6' : (a - b) * 2 ^ k = η := by
    rw [h6]
    field_simp
  have hlow : b ≤ (a + b) / 2 := by linarith
  have hhigh : (a + b) / 2 ≤ a := by linarith
  have hw1 : a - (a + b) / 2 = η / 2 ^ (k + 1) := by
    rw [eq_div_iff hne, pow_succ, ← h6']
    ring
  have hw2 : (a + b) / 2 - b = η / 2 ^ (k + 1) := by
    rw [eq_div_iff hne, pow_succ, ← h6']
    ring
  rw [bisectStep]
  split_ifs with hmid
  · exact ⟨h1, hhigh, h3.trans hlow, h4, hmid, hw1⟩
  · exact ⟨hhigh.trans h1, hlow, h3, (not_le.mp hmid).le, h5, hw2⟩

/-- The full upper-side bisection invariant after `k` steps: the endpoints stay ordered
inside `[y, y + η]`, the inner endpoint stays inside the sublevel set, the retained outer
endpoint keeps `δ ≤ D_e`, and the bracket length is exactly `η / 2 ^ k`. -/
theorem upperBracket_invariant (hδ : 0 ≤ δ) (hη : 0 ≤ η)
    (h0 : δ ≤ ratBregman cp cm y (y + η)) (k : ℕ) :
    y ≤ (upperBracket cp cm y δ η k).1 ∧
      (upperBracket cp cm y δ η k).1 ≤ (upperBracket cp cm y δ η k).2 ∧
      (upperBracket cp cm y δ η k).2 ≤ y + η ∧
      ratBregman cp cm y (upperBracket cp cm y δ η k).1 ≤ δ ∧
      δ ≤ ratBregman cp cm y (upperBracket cp cm y δ η k).2 ∧
      (upperBracket cp cm y δ η k).2 - (upperBracket cp cm y δ η k).1 = η / 2 ^ k := by
  induction k with
  | zero =>
    refine ⟨le_rfl, by simpa using hη, le_rfl, by simpa using hδ, h0, by simp⟩
  | succ k ih =>
    obtain ⟨h1, h2, h3, h4, h5, h6⟩ := ih
    rw [upperBracket_succ]
    exact bisectStep_invariant_upper k h1 h2 h3 h4 h5 h6

/-- The full lower-side bisection invariant after `k` steps. -/
theorem lowerBracket_invariant (hδ : 0 ≤ δ) (hη : 0 ≤ η)
    (h0 : δ ≤ ratBregman cp cm y (y - η)) (k : ℕ) :
    (lowerBracket cp cm y δ η k).1 ≤ y ∧
      (lowerBracket cp cm y δ η k).2 ≤ (lowerBracket cp cm y δ η k).1 ∧
      y - η ≤ (lowerBracket cp cm y δ η k).2 ∧
      ratBregman cp cm y (lowerBracket cp cm y δ η k).1 ≤ δ ∧
      δ ≤ ratBregman cp cm y (lowerBracket cp cm y δ η k).2 ∧
      (lowerBracket cp cm y δ η k).1 - (lowerBracket cp cm y δ η k).2 = η / 2 ^ k := by
  induction k with
  | zero =>
    refine ⟨le_rfl, by simpa using hη, le_rfl, by simpa using hδ, h0, by simp⟩
  | succ k ih =>
    obtain ⟨h1, h2, h3, h4, h5, h6⟩ := ih
    rw [lowerBracket_succ]
    exact bisectStep_invariant_lower k h1 h2 h3 h4 h5 h6

/-- Accuracy recursion above `y`: `k` steps halve the initial bracket `k` times. -/
theorem upperBracket_width (hδ : 0 ≤ δ) (hη : 0 ≤ η)
    (h0 : δ ≤ ratBregman cp cm y (y + η)) (k : ℕ) :
    (upperBracket cp cm y δ η k).2 - (upperBracket cp cm y δ η k).1 = η / 2 ^ k :=
  (upperBracket_invariant hδ hη h0 k).2.2.2.2.2

/-- Accuracy recursion below `y`. -/
theorem lowerBracket_width (hδ : 0 ≤ δ) (hη : 0 ≤ η)
    (h0 : δ ≤ ratBregman cp cm y (y - η)) (k : ℕ) :
    (lowerBracket cp cm y δ η k).1 - (lowerBracket cp cm y δ η k).2 = η / 2 ^ k :=
  (lowerBracket_invariant hδ hη h0 k).2.2.2.2.2

/-- Exact size recursion above `y`: after `k` steps both endpoints are dyadic points of the
initial bracket, with natural multiples of `η / 2 ^ k`. No hypothesis is needed. -/
theorem upperBracket_dyadic (cp cm y δ η : ℚ) (k : ℕ) :
    ∃ i j : ℕ, (upperBracket cp cm y δ η k).1 = y + (i : ℚ) * η / 2 ^ k ∧
      (upperBracket cp cm y δ η k).2 = y + (j : ℚ) * η / 2 ^ k := by
  induction k with
  | zero => exact ⟨0, 1, by simp, by simp⟩
  | succ k ih =>
    obtain ⟨i, j, hi, hj⟩ := ih
    have hne : ((2 : ℚ) ^ k) ≠ 0 := by positivity
    have hmid : ((upperBracket cp cm y δ η k).1 + (upperBracket cp cm y δ η k).2) / 2 =
        y + ((i + j : ℕ) : ℚ) * η / 2 ^ (k + 1) := by
      rw [hi, hj, pow_succ]
      push_cast
      field_simp
      ring
    rw [upperBracket_succ, bisectStep]
    split_ifs
    · refine ⟨2 * i, i + j, ?_, hmid⟩
      rw [hi, pow_succ]
      push_cast
      field_simp
    · refine ⟨i + j, 2 * j, hmid, ?_⟩
      rw [hj, pow_succ]
      push_cast
      field_simp

/-- Exact size recursion below `y`. -/
theorem lowerBracket_dyadic (cp cm y δ η : ℚ) (k : ℕ) :
    ∃ i j : ℕ, (lowerBracket cp cm y δ η k).1 = y - (i : ℚ) * η / 2 ^ k ∧
      (lowerBracket cp cm y δ η k).2 = y - (j : ℚ) * η / 2 ^ k := by
  induction k with
  | zero => exact ⟨0, 1, by simp, by simp⟩
  | succ k ih =>
    obtain ⟨i, j, hi, hj⟩ := ih
    have hne : ((2 : ℚ) ^ k) ≠ 0 := by positivity
    have hmid : ((lowerBracket cp cm y δ η k).1 + (lowerBracket cp cm y δ η k).2) / 2 =
        y - ((i + j : ℕ) : ℚ) * η / 2 ^ (k + 1) := by
      rw [hi, hj, pow_succ]
      push_cast
      field_simp
      ring
    rw [lowerBracket_succ, bisectStep]
    split_ifs
    · refine ⟨2 * i, i + j, ?_, hmid⟩
      rw [hi, pow_succ]
      push_cast
      field_simp
    · refine ⟨i + j, 2 * j, hmid, ?_⟩
      rw [hj, pow_succ]
      push_cast
      field_simp

/-- The rational endpoint test transfers verbatim to the real divergence. -/
private theorem le_edgeBregman_of_ratBregman {z : ℚ} (h : δ ≤ ratBregman cp cm y z) :
    (δ : ℝ) ≤ edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) (z : ℝ) := by
  rw [← ratBregman_cast]
  exact_mod_cast h

/-- The rational inner test transfers verbatim to the real divergence. -/
private theorem edgeBregman_le_of_ratBregman {z : ℚ} (h : ratBregman cp cm y z ≤ δ) :
    edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) (z : ℝ) ≤ (δ : ℝ) := by
  rw [← ratBregman_cast]
  exact_mod_cast h

/-- The edge law is continuous: the two coefficient branches agree at the origin, where the
sign-dependent coefficient switches. -/
theorem continuous_edgeLaw (cp cm : ℝ) : Continuous (edgeLaw cp cm) := by
  have h : edgeLaw cp cm = fun x : ℝ => if (0 : ℝ) ≤ x then cp * x * |x| else cm * x * |x| := by
    funext x
    rw [edgeLaw]
    split_ifs <;> rfl
  rw [h]
  exact Continuous.if_le ((continuous_const.mul continuous_id').mul continuous_abs)
    ((continuous_const.mul continuous_id').mul continuous_abs) continuous_const continuous_id'
    (fun x hx => by rw [← hx]; simp)

/-- The edge energy is continuous, being differentiable by `hasDerivAt_edgeEnergy`. -/
theorem continuous_edgeEnergy (cp cm : ℝ) : Continuous (edgeEnergy cp cm) :=
  continuous_iff_continuousAt.mpr fun x => (hasDerivAt_edgeEnergy cp cm x).continuousAt

/-- The divergence is continuous in its second argument, including across the origin. -/
theorem continuous_edgeBregman (cp cm z : ℝ) : Continuous (edgeBregman cp cm z) := by
  change Continuous fun w => edgeEnergy cp cm z - edgeEnergy cp cm w - edgeLaw cp cm w * (z - w)
  exact (continuous_const.sub (continuous_edgeEnergy cp cm)).sub
    ((continuous_edgeLaw cp cm).mul (continuous_const.sub continuous_id'))

/-- Intermediate value form of the sublevel boundary: any bracket whose endpoint values
straddle `δ` contains an exact boundary point. -/
theorem exists_edgeBregman_eq {cp' cm' y' δ' l u : ℝ} (hlu : l ≤ u)
    (hl : edgeBregman cp' cm' y' l ≤ δ') (hu : δ' ≤ edgeBregman cp' cm' y' u) :
    ∃ z, l ≤ z ∧ z ≤ u ∧ edgeBregman cp' cm' y' z = δ' := by
  obtain ⟨z, hz, hz'⟩ := intermediate_value_Icc hlu
    (continuous_edgeBregman cp' cm' y').continuousOn ⟨hl, hu⟩
  exact ⟨z, hz.1, hz.2, hz'⟩

/-- Boundary sharpness above `y`: an exact real solution of `D_e(y, z) = δ` lies inside the
bracket returned after `k` steps, so the returned outer endpoint overshoots the exact
sublevel boundary by at most `η / 2 ^ k`. The degenerate cases `δ = 0` and `η = 0` are
included, and then `z = y`. -/
theorem upperBracket_boundary (hδ : 0 ≤ δ) (hη : 0 ≤ η)
    (h0 : δ ≤ ratBregman cp cm y (y + η)) (k : ℕ) :
    ∃ z : ℝ, (y : ℝ) ≤ z ∧ edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) z = (δ : ℝ) ∧
      (((upperBracket cp cm y δ η k).1 : ℚ) : ℝ) ≤ z ∧
      z ≤ (((upperBracket cp cm y δ η k).2 : ℚ) : ℝ) ∧
      (((upperBracket cp cm y δ η k).2 : ℚ) : ℝ) - z ≤ (η : ℝ) / 2 ^ k := by
  obtain ⟨h1, h2, _, h4, h5, h6⟩ := upperBracket_invariant hδ hη h0 k
  have hw : (((upperBracket cp cm y δ η k).2 : ℚ) : ℝ) -
      (((upperBracket cp cm y δ η k).1 : ℚ) : ℝ) = (η : ℝ) / 2 ^ k := by
    rw [← Rat.cast_sub, h6]
    push_cast
    ring
  have hle : (((upperBracket cp cm y δ η k).1 : ℚ) : ℝ) ≤
      (((upperBracket cp cm y δ η k).2 : ℚ) : ℝ) := by exact_mod_cast h2
  obtain ⟨z, hz1, hz2, hz3⟩ := exists_edgeBregman_eq hle
    (edgeBregman_le_of_ratBregman h4) (le_edgeBregman_of_ratBregman h5)
  exact ⟨z, le_trans (by exact_mod_cast h1) hz1, hz3, hz1, hz2, by linarith⟩

/-- Boundary sharpness below `y`. -/
theorem lowerBracket_boundary (hδ : 0 ≤ δ) (hη : 0 ≤ η)
    (h0 : δ ≤ ratBregman cp cm y (y - η)) (k : ℕ) :
    ∃ z : ℝ, z ≤ (y : ℝ) ∧ edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) z = (δ : ℝ) ∧
      (((lowerBracket cp cm y δ η k).2 : ℚ) : ℝ) ≤ z ∧
      z ≤ (((lowerBracket cp cm y δ η k).1 : ℚ) : ℝ) ∧
      z - (((lowerBracket cp cm y δ η k).2 : ℚ) : ℝ) ≤ (η : ℝ) / 2 ^ k := by
  obtain ⟨h1, h2, _, h4, h5, h6⟩ := lowerBracket_invariant hδ hη h0 k
  have hw : (((lowerBracket cp cm y δ η k).1 : ℚ) : ℝ) -
      (((lowerBracket cp cm y δ η k).2 : ℚ) : ℝ) = (η : ℝ) / 2 ^ k := by
    rw [← Rat.cast_sub, h6]
    push_cast
    ring
  have hle : (((lowerBracket cp cm y δ η k).2 : ℚ) : ℝ) ≤
      (((lowerBracket cp cm y δ η k).1 : ℚ) : ℝ) := by exact_mod_cast h2
  obtain ⟨z, hz, hz3⟩ := intermediate_value_Icc' (f := edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ))
    hle (continuous_edgeBregman _ _ _).continuousOn
    ⟨edgeBregman_le_of_ratBregman h4, le_edgeBregman_of_ratBregman h5⟩
  obtain ⟨hza, hzb⟩ := hz
  exact ⟨z, le_trans hzb (by exact_mod_cast h1), hz3, hza, hzb, by linarith⟩

/-- Boundary sharpness above `y`, sharpened by uniqueness: with positive coefficients the
point returned by `upperBracket_boundary` is *the* sublevel boundary point on that side,
since any other point of the closed side with divergence `δ` equals it. In particular the
returned outer endpoint is within `η / 2 ^ k` of the exact boundary. -/
theorem upperBracket_boundary_unique (hcp : 0 < cp) (hcm : 0 < cm) (hδ : 0 ≤ δ) (hη : 0 ≤ η)
    (h0 : δ ≤ ratBregman cp cm y (y + η)) (k : ℕ) :
    ∃ z : ℝ, ((y : ℝ) ≤ z ∧ edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) z = (δ : ℝ) ∧
        (((upperBracket cp cm y δ η k).1 : ℚ) : ℝ) ≤ z ∧
        z ≤ (((upperBracket cp cm y δ η k).2 : ℚ) : ℝ) ∧
        (((upperBracket cp cm y δ η k).2 : ℚ) : ℝ) - z ≤ (η : ℝ) / 2 ^ k) ∧
      ∀ w : ℝ, (y : ℝ) ≤ w → edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) w = (δ : ℝ) → w = z := by
  obtain ⟨z, hz1, hz2, hz3, hz4, hz5⟩ := upperBracket_boundary hδ hη h0 k
  refine ⟨z, ⟨hz1, hz2, hz3, hz4, hz5⟩, fun w hw hwd => ?_⟩
  exact edgeBregman_injOn_Ici (cp := (cp : ℝ)) (cm := (cm : ℝ)) (by exact_mod_cast hcp)
    (by exact_mod_cast hcm) (y : ℝ)
    (Set.mem_Ici.mpr hw) (Set.mem_Ici.mpr hz1) (by rw [hwd, hz2])

/-- Boundary sharpness below `y`, sharpened by uniqueness in the same way. -/
theorem lowerBracket_boundary_unique (hcp : 0 < cp) (hcm : 0 < cm) (hδ : 0 ≤ δ) (hη : 0 ≤ η)
    (h0 : δ ≤ ratBregman cp cm y (y - η)) (k : ℕ) :
    ∃ z : ℝ, (z ≤ (y : ℝ) ∧ edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) z = (δ : ℝ) ∧
        (((lowerBracket cp cm y δ η k).2 : ℚ) : ℝ) ≤ z ∧
        z ≤ (((lowerBracket cp cm y δ η k).1 : ℚ) : ℝ) ∧
        z - (((lowerBracket cp cm y δ η k).2 : ℚ) : ℝ) ≤ (η : ℝ) / 2 ^ k) ∧
      ∀ w : ℝ, w ≤ (y : ℝ) → edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) w = (δ : ℝ) → w = z := by
  obtain ⟨z, hz1, hz2, hz3, hz4, hz5⟩ := lowerBracket_boundary hδ hη h0 k
  refine ⟨z, ⟨hz1, hz2, hz3, hz4, hz5⟩, fun w hw hwd => ?_⟩
  exact edgeBregman_injOn_Iic (cp := (cp : ℝ)) (cm := (cm : ℝ)) (by exact_mod_cast hcp)
    (by exact_mod_cast hcm) (y : ℝ)
    (Set.mem_Iic.mpr hw) (Set.mem_Iic.mpr hz1) (by rw [hwd, hz2])

/-- Exactly one point of the closed side above `y` has divergence `δ`, whenever the initial
outer test holds there. -/
theorem existsUnique_edgeBregman_eq_upper (hcp : 0 < cp) (hcm : 0 < cm) (hδ : 0 ≤ δ)
    (hη : 0 ≤ η) (h0 : δ ≤ ratBregman cp cm y (y + η)) :
    ∃! z : ℝ, (y : ℝ) ≤ z ∧ edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) z = (δ : ℝ) := by
  obtain ⟨z, ⟨hz1, hz2, _, _, _⟩, huniq⟩ := upperBracket_boundary_unique hcp hcm hδ hη h0 0
  exact ⟨z, ⟨hz1, hz2⟩, fun w hw => huniq w hw.1 hw.2⟩

/-- Exactly one point of the closed side below `y` has divergence `δ`. -/
theorem existsUnique_edgeBregman_eq_lower (hcp : 0 < cp) (hcm : 0 < cm) (hδ : 0 ≤ δ)
    (hη : 0 ≤ η) (h0 : δ ≤ ratBregman cp cm y (y - η)) :
    ∃! z : ℝ, z ≤ (y : ℝ) ∧ edgeBregman (cp : ℝ) (cm : ℝ) (y : ℝ) z = (δ : ℝ) := by
  obtain ⟨z, ⟨hz1, hz2, _, _, _⟩, huniq⟩ := lowerBracket_boundary_unique hcp hcm hδ hη h0 0
  exact ⟨z, ⟨hz1, hz2⟩, fun w hw => huniq w hw.1 hw.2⟩

namespace RationalNetwork

variable {n m : ℕ} (G : RationalNetwork n m)

/-- Soundness of the bisected endpoints (`CC06` composed with `CC03`). For a rational
network whose real interpretation has a verified energy gap `gap` at the rational candidate
`flow`, the two outer endpoints returned after `k` bisection steps enclose the minimizing
flow on every edge. The initial hypotheses are the rational endpoint tests at `flow ± rad`,
which `le_ratBregman_of_radius` supplies from the certified uniform radius. -/
theorem mem_bisection_interval (hc : ∀ e, 0 < G.positive e ∧ 0 < G.negative e)
    {b : Fin n → ℝ} {x : Fin m → ℝ} {flow : Fin m → ℚ} {gap rad : ℚ}
    (hgap : 0 ≤ gap) (hrad : 0 ≤ rad)
    (hx : G.toReal.Feasible b x)
    (hy : G.toReal.Feasible b fun e => (flow e : ℝ))
    (hmin : ∀ z, G.toReal.Feasible b z → G.toReal.energy x ≤ G.toReal.energy z)
    (hbound : G.toReal.energy (fun e => (flow e : ℝ)) - G.toReal.energy x ≤ (gap : ℝ))
    (hup : ∀ e, gap ≤ ratBregman (G.positive e) (G.negative e) (flow e) (flow e + rad))
    (hlo : ∀ e, gap ≤ ratBregman (G.positive e) (G.negative e) (flow e) (flow e - rad))
    (k : ℕ) (e : Fin m) :
    ((lowerBracket (G.positive e) (G.negative e) (flow e) gap rad k).2 : ℝ) ≤ x e ∧
      x e ≤ ((upperBracket (G.positive e) (G.negative e) (flow e) gap rad k).2 : ℝ) := by
  have hpos : G.toReal.Positive := by
    refine ⟨fun j => ?_, fun j => ?_⟩
    · change (0 : ℝ) < ((G.positive j : ℚ) : ℝ)
      exact_mod_cast (hc j).1
    · change (0 : ℝ) < ((G.negative j : ℚ) : ℝ)
      exact_mod_cast (hc j).2
  obtain ⟨hu1, hu2, _, _, hu5, _⟩ := upperBracket_invariant hgap hrad (hup e) k
  obtain ⟨hl1, hl2, _, _, hl5, _⟩ := lowerBracket_invariant hgap hrad (hlo e) k
  exact G.toReal.mem_interval_of_edgeBregman hpos hx hy hmin hbound
    (show (((lowerBracket (G.positive e) (G.negative e) (flow e) gap rad k).2 : ℚ) : ℝ) ≤
        ((flow e : ℚ) : ℝ) by exact_mod_cast hl2.trans hl1)
    (show ((flow e : ℚ) : ℝ) ≤
        (((upperBracket (G.positive e) (G.negative e) (flow e) gap rad k).2 : ℚ) : ℝ) by
      exact_mod_cast hu1.trans hu2)
    (le_edgeBregman_of_ratBregman hl5) (le_edgeBregman_of_ratBregman hu5)

end RationalNetwork

/-- Sanity check that the bisection evaluates: with unit coefficients, candidate `0`, gap
`1/3` and radius `1`, the midpoint `1/2` has divergence `1/12 < 1/3`, so the first step
replaces the inner endpoint. -/
example : upperBracket 1 1 0 (1 / 3) 1 1 = (1 / 2, 1) := by
  norm_num [upperBracket, bisectStep, ratBregman, ratEnergy, ratLaw]

end PotentialFlow
