import CertifiedMinlp.Support
import CertifiedMinlp.DiscreteRows

/-! The interface from convex nonlinear rows and enclosed segment derivatives to rational
master rows. Acceptance records the analytic and rational checks, not the desired cut validity. -/
namespace CertifiedMinlp

open scoped BigOperators

/-- Data for one nonlinear row and its proposed rational affine cut. -/
structure CutData (n : ℕ) where
  g : (Fin n → ℝ) → ℝ
  q : Fin n → ℚ
  a : Fin n → ℚ
  z : Fin n → ℚ
  lo : Fin n → ℚ
  hi : Fin n → ℚ
  p : Fin n → ℝ
  c : ℚ
  b : ℚ
  v : ℚ

namespace CutData

variable {n : ℕ}

/-- The original normalized nonlinear expression whose feasible side is `expression ≤ 0`. -/
def expression (C : CutData n) (x : Fin n → ℝ) : ℝ :=
  C.g x + dot (fun j => (C.q j : ℝ)) x + C.c

/-- The exact rational row exported to the discrete master. -/
def row (C : CutData n) : Discrete.Row n :=
  ⟨C.a, -C.b, .le⟩

/-- Analytic obligations and rational acceptance tests for one cut. The derivative is along
every feasible segment, which is stronger than merely having finite coordinate derivatives. -/
structure Accepted (C : CutData n) (B : Fin n → Coordinate) : Prop where
  convex : ConvexOn ℝ {x | boxContains B x} C.g
  point : boxContains B (fun j => (C.z j : ℝ))
  derivative : ∀ x, boxContains B x → HasDerivWithinAt
    (fun θ : ℝ => C.g (fun j => (C.z j : ℝ) + θ * (x j - (C.z j : ℝ))))
    (dot C.p (fun j => x j - (C.z j : ℝ))) (Set.Ioi (0 : ℝ)) 0
  accepted : ∀ j, (B j).accepts (C.lo j) (C.hi j)
  lower : ∀ j, (C.lo j : ℝ) ≤ C.p j + (C.q j : ℝ) - (C.a j : ℝ)
  upper : ∀ j, C.p j + (C.q j : ℝ) - (C.a j : ℝ) ≤ (C.hi j : ℝ)
  value : (C.v : ℝ) ≤ C.expression (fun j => (C.z j : ℝ)) -
    dot (fun j => (C.a j : ℝ)) (fun j => (C.z j : ℝ))
  intercept : C.b ≤ C.v - ∑ j, (B j).correction (C.z j) (C.lo j) (C.hi j)

/-- Convexity and segment derivatives establish support; rational enclosure checking then
establishes the actual affine underestimator on the entire certified box. -/
theorem underestimator (C : CutData n) {B : Fin n → Coordinate} (h : C.Accepted B)
    {x : Fin n → ℝ} (hx : boxContains B x) :
    affine (fun j => (C.a j : ℝ)) C.b x ≤ C.expression x := by
  exact rational_enclosure_cut B C.g C.q C.a C.z C.lo C.hi C.p C.c C.b C.v
    h.point (support_of_feasible_segment_derivatives h.convex h.point h.derivative)
    h.accepted h.lower h.upper h.value h.intercept x hx

/-- A feasible nonlinear row implies the exact exported rational master row. -/
theorem row_valid (C : CutData n) {B : Fin n → Coordinate} (h : C.Accepted B)
    {x : Fin n → ℝ} (hx : boxContains B x) (hr : C.expression x ≤ 0) :
    Discrete.Holds C.row x := by
  have hc := (C.underestimator h hx).trans hr
  change dot (fun j => (C.a j : ℝ)) x + (C.b : ℝ) ≤ 0 at hc
  change (∑ j, (C.a j : ℝ) * x j) ≤ ((-C.b : ℚ) : ℝ)
  rw [Rat.cast_neg]
  exact (le_neg_iff_add_nonpos_right).mpr hc

end CutData
end CertifiedMinlp
