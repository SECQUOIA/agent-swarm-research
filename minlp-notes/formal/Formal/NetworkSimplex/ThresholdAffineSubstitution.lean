import Formal.NetworkSimplex.ThresholdRows

/-! Exact evaluation and coefficient rules for substitution of affine syntax. -/
namespace NetworkSimplex.Chain.Threshold.AffineExpression
variable {C D : Type*}

/-- Replace each variable by its affine expression in the target coordinates. -/
def substitute (σ : C → AffineExpression D) : AffineExpression C → AffineExpression D
  | .constant q => .constant q
  | .variable c => σ c
  | .add e f => .add (substitute σ e) (substitute σ f)
  | .neg e => .neg (substitute σ e)

theorem eval_substitute (σ : C → AffineExpression D) (x : D → ℝ)
    (e : AffineExpression C) :
    (substitute σ e).eval x = e.eval (fun c => (σ c).eval x) := by
  induction e with
  | constant q => rfl
  | «variable» c => rfl
  | add e f he hf => simp only [substitute, eval, he, hf]
  | neg e he => simp only [substitute, eval, he]

theorem evalRat_substitute (σ : C → AffineExpression D) (x : D → ℚ)
    (e : AffineExpression C) :
    (substitute σ e).evalRat x = e.evalRat (fun c => (σ c).evalRat x) := by
  induction e with
  | constant q => rfl
  | «variable» c => rfl
  | add e f he hf => simp only [substitute, evalRat, he, hf]
  | neg e he => simp only [substitute, evalRat, he]

/-- If a target coordinate occurs with coefficient one in exactly one source
variable's replacement, substitution preserves that source coefficient. -/
theorem coefficient_substitute [DecidableEq C] [DecidableEq D]
    (σ : C → AffineExpression D) (source : C) (target : D)
    (hσ : ∀ c, (σ c).coefficient target = if c = source then 1 else 0)
    (e : AffineExpression C) :
    (substitute σ e).coefficient target = e.coefficient source := by
  induction e with
  | constant q => rfl
  | «variable» c => exact hσ c
  | add e f he hf => simp only [substitute, coefficient, he, hf]
  | neg e he => simp only [substitute, coefficient, he]

/-- A target coordinate absent from every replacement stays absent. -/
theorem coefficient_substitute_zero [DecidableEq D]
    (σ : C → AffineExpression D) (target : D)
    (hσ : ∀ c, (σ c).coefficient target = 0) (e : AffineExpression C) :
    (substitute σ e).coefficient target = 0 := by
  induction e with
  | constant q => rfl
  | «variable» c => exact hσ c
  | add e f he hf => simp only [substitute, coefficient, he, hf, add_zero]
  | neg e he => simp only [substitute, coefficient, he, neg_zero]

end NetworkSimplex.Chain.Threshold.AffineExpression
