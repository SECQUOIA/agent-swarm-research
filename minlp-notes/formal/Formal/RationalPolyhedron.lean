import Formal.Model

/-! Explicit finite rational affine inequalities, including their convexity. -/
namespace ExactCounts
noncomputable section
variable {n p q : ℕ}

/-- Syntax containing only rational constants and affine operations. -/
inductive RationalAffine (n p q : ℕ) where
  | const : ℚ → RationalAffine n p q
  | visible : Fin n → Fin 3 → RationalAffine n p q
  | code : Fin p → RationalAffine n p q
  | aux : Fin q → RationalAffine n p q
  | add : RationalAffine n p q → RationalAffine n p q → RationalAffine n p q
  | scale : ℚ → RationalAffine n p q → RationalAffine n p q

namespace RationalAffine

def eval : RationalAffine n p q → Ambient n p q → ℝ
  | .const r, _ => r
  | .visible i j, y => y.1 i j
  | .code i, y => y.2.1 i
  | .aux i, y => y.2.2 i
  | .add e f, y => eval e y + eval f y
  | .scale r e, y => r * eval e y

def sub (e f : RationalAffine n p q) := add e (scale (-1) f)

def listSum (es : List (RationalAffine n p q)) : RationalAffine n p q :=
  es.foldr add (const 0)

def sum {ι : Type} [Fintype ι] (f : ι → RationalAffine n p q) :
    RationalAffine n p q := listSum (Finset.univ.toList.map f)

@[simp] theorem eval_const (r : ℚ) (y : Ambient n p q) : eval (.const r) y = r := rfl
@[simp] theorem eval_visible (i : Fin n) (j : Fin 3) (y : Ambient n p q) :
    eval (.visible i j) y = y.1 i j := rfl
@[simp] theorem eval_code (i : Fin p) (y : Ambient n p q) :
    eval (.code i) y = y.2.1 i := rfl
@[simp] theorem eval_aux (i : Fin q) (y : Ambient n p q) :
    eval (.aux i) y = y.2.2 i := rfl
@[simp] theorem eval_add (e f : RationalAffine n p q) (y : Ambient n p q) :
    eval (.add e f) y = eval e y + eval f y := rfl
@[simp] theorem eval_scale (r : ℚ) (e : RationalAffine n p q) (y : Ambient n p q) :
    eval (.scale r e) y = r * eval e y := rfl
@[simp] theorem eval_sub (e f : RationalAffine n p q) (y : Ambient n p q) :
    eval (sub e f) y = eval e y - eval f y := by simp [sub, sub_eq_add_neg]

@[simp] theorem eval_listSum (es : List (RationalAffine n p q)) (y : Ambient n p q) :
    eval (listSum es) y = (es.map (fun e => eval e y)).sum := by
  induction es with
  | nil => simp [listSum]
  | cons e es ih => simpa [listSum, eval] using congrArg (eval e y + ·) ih

@[simp] theorem eval_sum {ι : Type} [Fintype ι] (f : ι → RationalAffine n p q)
    (y : Ambient n p q) : eval (sum f) y = ∑ i, eval (f i) y := by
  simp [sum, List.map_map]

theorem eval_convexCombination (e : RationalAffine n p q) (x y : Ambient n p q)
    (a b : ℝ) (hab : a + b = 1) :
    eval e (a • x + b • y) = a * eval e x + b * eval e y := by
  induction e with
  | const r => simp only [eval]; rw [← add_mul, hab, one_mul]
  | visible i j => simp [eval, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  | code i => simp [eval, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  | aux i => simp [eval, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  | add e f he hf => simp only [eval, he, hf]; ring
  | scale r e he => simp only [eval, he]; ring

end RationalAffine

def rationalPolyhedron {ι : Type} (rows : ι → RationalAffine n p q) :
    Set (Ambient n p q) := {y | ∀ i, (rows i).eval y ≤ 0}

theorem rationalPolyhedron_convex {ι : Type} (rows : ι → RationalAffine n p q) :
    Convex ℝ (rationalPolyhedron rows) := by
  intro x hx y hy a b ha hb hab i
  rw [RationalAffine.eval_convexCombination _ _ _ _ _ hab]
  exact add_nonpos (mul_nonpos_of_nonneg_of_nonpos ha (hx i))
    (mul_nonpos_of_nonneg_of_nonpos hb (hy i))

/-- Encode an equality as its two opposing inequalities. -/
def systemRows {I E : Type} (ineq : I → RationalAffine n p q)
    (eqn : E → RationalAffine n p q) : I ⊕ (E × Fin 2) → RationalAffine n p q
  | .inl i => ineq i
  | .inr (e, k) => if k = 0 then eqn e else .scale (-1) (eqn e)

theorem mem_systemRows {I E : Type} (ineq : I → RationalAffine n p q)
    (eqn : E → RationalAffine n p q) (y : Ambient n p q) :
    y ∈ rationalPolyhedron (systemRows ineq eqn) ↔
      (∀ i, (ineq i).eval y ≤ 0) ∧ (∀ e, (eqn e).eval y = 0) := by
  constructor
  · intro h
    refine ⟨fun i => h (.inl i), fun e => ?_⟩
    have h₀ := h (.inr (e, 0))
    have h₁ := h (.inr (e, 1))
    simp [systemRows] at h₀ h₁
    linarith
  · rintro ⟨hi, he⟩ (i | ⟨e, k⟩)
    · exact hi i
    · fin_cases k <;> simp [systemRows, he]

/-- A rational MILP here means a finite list of rational affine inequalities,
with existential real auxiliaries and the stated integer/binary coordinates. -/
def HasRationalIntegerLift (n p : ℕ) : Prop :=
  ∃ q r, ∃ rows : Fin r → RationalAffine n p q,
    Admissible (rationalPolyhedron rows) (IntegerCodes p)

def HasRationalBinaryLift (n p : ℕ) : Prop :=
  ∃ q r, ∃ rows : Fin r → RationalAffine n p q,
    Admissible (rationalPolyhedron rows) (BinaryCodes p)

theorem HasRationalIntegerLift.toHasIntegerLift (h : HasRationalIntegerLift n p) :
    HasIntegerLift n p := by
  obtain ⟨q, r, rows, h⟩ := h
  exact ⟨q, rationalPolyhedron rows, rationalPolyhedron_convex rows, h⟩

theorem HasRationalBinaryLift.toHasBinaryLift (h : HasRationalBinaryLift n p) :
    HasBinaryLift n p := by
  obtain ⟨q, r, rows, h⟩ := h
  exact ⟨q, rationalPolyhedron rows, rationalPolyhedron_convex rows, h⟩

theorem hasRationalIntegerLift_of_rows {ι : Type} [Finite ι]
    (rows : ι → RationalAffine n p q)
    (h : Admissible (rationalPolyhedron rows) (IntegerCodes p)) :
    HasRationalIntegerLift n p := by
  let := Fintype.ofFinite ι
  refine ⟨q, Fintype.card ι, rows ∘ (Fintype.equivFin ι).symm, ?_⟩
  have he : rationalPolyhedron (rows ∘ (Fintype.equivFin ι).symm) =
      rationalPolyhedron rows := by
    ext y
    constructor
    · intro h i
      simpa using h ((Fintype.equivFin ι) i)
    · intro h i
      exact h ((Fintype.equivFin ι).symm i)
  rwa [he]

theorem hasRationalBinaryLift_of_rows {ι : Type} [Finite ι]
    (rows : ι → RationalAffine n p q)
    (h : Admissible (rationalPolyhedron rows) (BinaryCodes p)) :
    HasRationalBinaryLift n p := by
  let := Fintype.ofFinite ι
  refine ⟨q, Fintype.card ι, rows ∘ (Fintype.equivFin ι).symm, ?_⟩
  have he : rationalPolyhedron (rows ∘ (Fintype.equivFin ι).symm) =
      rationalPolyhedron rows := by
    ext y
    constructor
    · intro h i
      simpa using h ((Fintype.equivFin ι) i)
    · intro h i
      exact h ((Fintype.equivFin ι).symm i)
  rwa [he]

end
end ExactCounts
