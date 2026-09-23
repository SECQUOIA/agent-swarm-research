import Formal.ExactBoxCounts
import Formal.ClosedLifts

/-! Transport the exact representation contract through the output shear.
The input, integer codes, and continuous auxiliary coordinates are preserved. -/
namespace ExactCounts
noncomputable section
variable {n p q : ℕ}

def shearPoint (s : ℝ) (v : Point) : Point := ![v 0, v 1 + s * v 0, v 2]
def shearVisible (s : ℝ) (v : Visible n) : Visible n := fun i => shearPoint s (v i)
def shearAmbient (s : ℝ) (y : Ambient n p q) : Ambient n p q :=
  (shearVisible s y.1, y.2)

/-- The first signed vertical error is preserved exactly, not just bounded. -/
theorem shearPoint_left_error (s : ℝ) (v : Point) :
    (shearPoint s v) 1 - (leftValue ((shearPoint s v) 0) + s * (shearPoint s v) 0) =
      v 1 - leftValue (v 0) := by
  simp [shearPoint]

theorem shearPoint_right_error (s : ℝ) (v : Point) :
    (shearPoint s v) 2 - rightValue ((shearPoint s v) 0) = v 2 - rightValue (v 0) := rfl

@[simp] theorem shearPoint_zero (v : Point) : shearPoint 0 v = v := by
  ext j; fin_cases j <;> simp [shearPoint]
@[simp] theorem shearPoint_neg (s : ℝ) (v : Point) :
    shearPoint (-s) (shearPoint s v) = v := by
  ext j; fin_cases j <;> simp [shearPoint]
@[simp] theorem shearVisible_neg (s : ℝ) (v : Visible n) :
    shearVisible (-s) (shearVisible s v) = v := by
  funext i; exact shearPoint_neg s (v i)
@[simp] theorem shearVisible_neg_rev (s : ℝ) (v : Visible n) :
    shearVisible s (shearVisible (-s) v) = v := by
  simpa only [neg_neg] using shearVisible_neg (-s) v
@[simp] theorem shearAmbient_neg (s : ℝ) (y : Ambient n p q) :
    shearAmbient (-s) (shearAmbient s y) = y := by
  apply Prod.ext
  · funext i; exact shearPoint_neg s (y.1 i)
  · rfl

@[simp] theorem shearAmbient_neg_rev (s : ℝ) (y : Ambient n p q) :
    shearAmbient s (shearAmbient (-s) y) = y := by
  simpa only [neg_neg] using shearAmbient_neg (-s) y

/-- A linear map, hence also an affine shear, on the entire lift. -/
def shearLinear (s : ℝ) : Ambient n p q →ₗ[ℝ] Ambient n p q where
  toFun := shearAmbient s
  map_add' x y := by
    apply Prod.ext
    · funext i j; fin_cases j <;> simp [shearAmbient, shearVisible, shearPoint]; ring
    · rfl
  map_smul' a y := by
    apply Prod.ext
    · funext i j; fin_cases j <;> simp [shearAmbient, shearVisible, shearPoint]; ring
    · rfl

theorem continuous_shearAmbient (s : ℝ) : Continuous (shearAmbient (n := n) (p := p) (q := q) s) :=
  (shearLinear s).continuous_of_finiteDimensional

def ShearedGraph (s : ℝ) (x : Fin n → ℝ) : Visible n := shearVisible s (graph x)
def ShearedValid (s : ℝ) (v : Visible n) : Prop := ∀ i,
  0 ≤ v i 0 ∧ v i 0 ≤ 1 ∧
  |v i 1 - (leftValue (v i 0) + s * v i 0)| ≤ 1 ∧
  |v i 2 - rightValue (v i 0)| ≤ 1

theorem shearedValid_iff (s : ℝ) (v : Visible n) :
    ShearedValid s v ↔ Valid (shearVisible (-s) v) := by
  unfold ShearedValid Valid ValidPoint
  apply forall_congr'
  intro i
  simp [shearVisible, shearPoint, sub_eq_add_neg, add_assoc, add_comm]

def ShearedAdmissible (s : ℝ) (C : Set (Ambient n p q)) (codes : Set (Code p)) : Prop :=
  (∀ x, InDomain x → ∃ z ∈ codes, ∃ a, (ShearedGraph s x, z, a) ∈ C) ∧
  (∀ v z a, z ∈ codes → (v, z, a) ∈ C → ShearedValid s v)

/-- Pulling a lift back by the shear is exactly the original graph-error contract. -/
theorem shearedAdmissible_iff (s : ℝ) (C : Set (Ambient n p q)) (codes : Set (Code p)) :
    ShearedAdmissible s C codes ↔ Admissible (shearAmbient s ⁻¹' C) codes := by
  constructor
  · rintro ⟨hg, hv⟩
    refine ⟨hg, ?_⟩
    intro v z a hz h
    have hvalid := (shearedValid_iff s (shearVisible s v)).mp (hv _ z a hz h)
    simpa only [shearVisible_neg] using hvalid
  · rintro ⟨hg, hv⟩
    refine ⟨hg, ?_⟩
    intro v z a hz h
    apply (shearedValid_iff s v).mpr
    apply hv _ z a hz
    change shearAmbient s (shearAmbient (-s) (v, z, a)) ∈ C
    simpa using h

/-- Forward transport preserves every code and auxiliary count. -/
theorem admissible_sheared_preimage (s : ℝ) (C : Set (Ambient n p q)) (codes : Set (Code p)) :
    ShearedAdmissible s (shearAmbient (-s) ⁻¹' C) codes ↔ Admissible C codes := by
  rw [shearedAdmissible_iff]
  have he : shearAmbient s ⁻¹' (shearAmbient (-s) ⁻¹' C) = C := by
    ext y; simp
  rw [he]

def HasShearedLift (s : ℝ) (codes : Set (Code p)) : Prop :=
  ∃ q, ∃ C : Set (Ambient n p q), Convex ℝ C ∧ ShearedAdmissible s C codes

theorem hasShearedLift_iff (s : ℝ) (codes : Set (Code p)) :
    HasShearedLift (n := n) s codes ↔
      ∃ q, ∃ C : Set (Ambient n p q), Convex ℝ C ∧ Admissible C codes := by
  constructor
  · rintro ⟨q, C, hc, ha⟩
    exact ⟨q, shearAmbient s ⁻¹' C, hc.linear_preimage (shearLinear s),
      (shearedAdmissible_iff s C codes).mp ha⟩
  · rintro ⟨q, C, hc, ha⟩
    exact ⟨q, shearAmbient (-s) ⁻¹' C, hc.linear_preimage (shearLinear (-s)),
      (admissible_sheared_preimage s C codes).mpr ha⟩

def HasClosedShearedLift (s : ℝ) (codes : Set (Code p)) : Prop :=
  ∃ q, ∃ C : Set (Ambient n p q), Convex ℝ C ∧ IsClosed C ∧ ShearedAdmissible s C codes

theorem hasClosedShearedLift_iff (s : ℝ) (codes : Set (Code p)) :
    HasClosedShearedLift (n := n) s codes ↔
      ∃ q, ∃ C : Set (Ambient n p q), Convex ℝ C ∧ IsClosed C ∧ Admissible C codes := by
  constructor
  · rintro ⟨q, C, hc, hcl, ha⟩
    exact ⟨q, shearAmbient s ⁻¹' C, hc.linear_preimage (shearLinear s),
      hcl.preimage (continuous_shearAmbient s), (shearedAdmissible_iff s C codes).mp ha⟩
  · rintro ⟨q, C, hc, hcl, ha⟩
    exact ⟨q, shearAmbient (-s) ⁻¹' C, hc.linear_preimage (shearLinear (-s)),
      hcl.preimage (continuous_shearAmbient (-s)),
      (admissible_sheared_preimage s C codes).mpr ha⟩

namespace RationalAffine
/-- Exact rational substitution; no rows, codes, or auxiliary coordinates are added. -/
def shearSubst (s : ℚ) : RationalAffine n p q → RationalAffine n p q
  | .const r => .const r
  | .visible i j => if j = 1 then .add (.visible i j) (.scale s (.visible i 0))
      else .visible i j
  | .code i => .code i
  | .aux i => .aux i
  | .add e f => .add (shearSubst s e) (shearSubst s f)
  | .scale r e => .scale r (shearSubst s e)

@[simp] theorem eval_shearSubst (s : ℚ) (e : RationalAffine n p q) (y : Ambient n p q) :
    (e.shearSubst s).eval y = e.eval (shearAmbient s y) := by
  induction e with
  | const r => rfl
  | visible i j => fin_cases j <;> simp [shearSubst, eval, shearAmbient, shearVisible, shearPoint]
  | code i => rfl
  | aux i => rfl
  | add e f he hf => simp only [shearSubst, eval_add, he, hf]
  | scale r e he => simp only [shearSubst, eval_scale, he]
end RationalAffine

theorem rationalPolyhedron_shearSubst {ι : Type} (s : ℚ) (rows : ι → RationalAffine n p q) :
    rationalPolyhedron (fun i => (rows i).shearSubst s) =
      shearAmbient (s : ℝ) ⁻¹' rationalPolyhedron rows := by
  ext y; simp [rationalPolyhedron]

def HasRationalShearedLift (s : ℝ) (codes : Set (Code p)) : Prop :=
  ∃ q r, ∃ rows : Fin r → RationalAffine n p q,
    ShearedAdmissible s (rationalPolyhedron rows) codes

theorem hasRationalShearedLift_iff (s : ℚ) (codes : Set (Code p)) :
    HasRationalShearedLift (n := n) s codes ↔
      ∃ q r, ∃ rows : Fin r → RationalAffine n p q,
        Admissible (rationalPolyhedron rows) codes := by
  constructor
  · rintro ⟨q, r, rows, ha⟩
    refine ⟨q, r, fun i => (rows i).shearSubst s, ?_⟩
    rw [rationalPolyhedron_shearSubst]
    exact (shearedAdmissible_iff s _ codes).mp ha
  · rintro ⟨q, r, rows, ha⟩
    refine ⟨q, r, fun i => (rows i).shearSubst (-s), ?_⟩
    rw [rationalPolyhedron_shearSubst, Rat.cast_neg]
    exact (admissible_sheared_preimage s _ codes).mpr ha

/-- All six count minima survive every rational output shear. -/
theorem sheared_exact_counts (s : ℚ) (n : ℕ) :
    IsLeast {p | HasShearedLift (n := n) s (IntegerCodes p)} n ∧
    IsLeast {p | HasShearedLift (n := n) s (BinaryCodes p)} (binaryCount n) ∧
    IsLeast {p | HasClosedShearedLift (n := n) s (IntegerCodes p)} n ∧
    IsLeast {p | HasClosedShearedLift (n := n) s (BinaryCodes p)} (binaryCount n) ∧
    IsLeast {p | HasRationalShearedLift (n := n) s (IntegerCodes p)} n ∧
    IsLeast {p | HasRationalShearedLift (n := n) s (BinaryCodes p)} (binaryCount n) := by
  simp only [hasShearedLift_iff, hasClosedShearedLift_iff, hasRationalShearedLift_iff]
  exact ⟨integer_count_exact n, binary_count_exact n, closed_integer_exact_count n,
    closed_binary_exact_count n, rational_integer_count_exact n, rational_binary_count_exact n⟩

/-- The monotone shear retains three weights and thirteen inequalities per input. -/
theorem sheared_integer_linear_size (s : ℚ) (n : ℕ) :
    ∃ rows : Fin (13 * n) → RationalAffine n n (n * 3),
      ShearedAdmissible s (rationalPolyhedron rows) (IntegerCodes n) := by
  obtain ⟨rows, h⟩ := integer_upper_linear_size n
  refine ⟨fun i => (rows i).shearSubst (-s), ?_⟩
  rw [rationalPolyhedron_shearSubst, Rat.cast_neg]
  exact (admissible_sheared_preimage s _ _).mpr h

end
end ExactCounts
