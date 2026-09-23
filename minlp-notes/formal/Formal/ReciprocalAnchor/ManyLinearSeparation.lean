import Formal.ReciprocalAnchor.ManyMembership

/-! An executable finite scan produces rational affine cuts for every linear violation. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

/-- The cut is the inequality `eval ≤ 0`. Coefficients use exact rational arithmetic. -/
structure RationalAffineCut (n : ℕ) where
  offset : ℚ := 0
  mean : ℚ := 0
  reciprocal : ℚ := 0
  leafQ : Fin n → ℚ := fun _ => 0
  leafW : Fin n → ℚ := fun _ => 0

def RationalAffineCut.eval {n : ℕ} (C : RationalAffineCut n) (m t : ℚ)
    (q w : Fin n → ℚ) : ℚ :=
  C.offset + C.mean * m + C.reciprocal * t + ∑ j, C.leafQ j * q j + ∑ j, C.leafW j * w j

noncomputable def RationalAffineCut.evalReal {n : ℕ} (C : RationalAffineCut n) (m t : ℝ)
    (q w : Fin n → ℝ) : ℝ :=
  C.offset + (C.mean : ℝ) * m + (C.reciprocal : ℝ) * t +
    ∑ j, (C.leafQ j : ℝ) * q j + ∑ j, (C.leafW j : ℝ) * w j

theorem RationalAffineCut.eval_cast {n : ℕ} (C : RationalAffineCut n) (m t : ℚ)
    (q w : Fin n → ℚ) :
    (C.eval m t q w : ℝ) = C.evalReal m t (fun j => q j) (fun j => w j) := by
  simp [eval, evalReal]

def meanLowerCut {n : ℕ} (a : ℚ) : RationalAffineCut n := ⟨a, -1, 0, fun _ => 0, fun _ => 0⟩
def meanUpperCut {n : ℕ} (b : ℚ) : RationalAffineCut n := ⟨-b, 1, 0, fun _ => 0, fun _ => 0⟩
def reciprocalUpperCut {n : ℕ} (a b : ℚ) : RationalAffineCut n :=
  ⟨-(a + b), 1, a * b, fun _ => 0, fun _ => 0⟩
def qLowerCut {n : ℕ} (j : Fin n) : RationalAffineCut n :=
  ⟨0, 0, 0, Pi.single j (-1), fun _ => 0⟩
def qUpperCut {n : ℕ} (j : Fin n) : RationalAffineCut n :=
  ⟨-1, 0, 0, Pi.single j 1, fun _ => 0⟩
def wLowerCut {n : ℕ} (a : ℚ) (j : Fin n) : RationalAffineCut n :=
  ⟨0, 0, 0, Pi.single j a, Pi.single j (-1)⟩
def wUpperCut {n : ℕ} (b : ℚ) (j : Fin n) : RationalAffineCut n :=
  ⟨0, 0, 0, Pi.single j (-b), Pi.single j 1⟩
def complementLowerCut {n : ℕ} (a : ℚ) (j : Fin n) : RationalAffineCut n :=
  ⟨a, -1, 0, Pi.single j (-a), Pi.single j 1⟩
def complementUpperCut {n : ℕ} (b : ℚ) (j : Fin n) : RationalAffineCut n :=
  ⟨-b, 1, 0, Pi.single j b, Pi.single j (-1)⟩

def leafCuts {n : ℕ} (a b : ℚ) (j : Fin n) : List (RationalAffineCut n) :=
  [qLowerCut j, qUpperCut j, wLowerCut a j, wUpperCut b j,
    complementLowerCut a j, complementUpperCut b j]

def linearCuts {n : ℕ} (a b : ℚ) : List (RationalAffineCut n) :=
  [meanLowerCut a, meanUpperCut b, reciprocalUpperCut a b] ++
    (List.ofFn (fun j : Fin n => leafCuts a b j)).flatten

private theorem sum_single_mul {n : ℕ} (j : Fin n) (c : ℚ) (q : Fin n → ℚ) :
    ∑ k, (Pi.single j c : Fin n → ℚ) k * q k = c * q j := by
  simp [Pi.single_apply, ite_mul, Finset.sum_ite_eq']

private theorem sum_single_mul_real {n : ℕ} (j : Fin n) (c : ℚ) (q : Fin n → ℝ) :
    ∑ k, ((Pi.single j c : Fin n → ℚ) k : ℚ) * q k = (c : ℝ) * q j := by
  simp [Pi.single_apply, apply_ite, ite_mul, Finset.sum_ite_eq']

@[simp] theorem leafCuts_eval {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) (j : Fin n) :
    (∀ C ∈ leafCuts a b j, C.eval m t q w ≤ 0) ↔
      0 ≤ q j ∧ q j ≤ 1 ∧ a * q j ≤ w j ∧ w j ≤ b * q j ∧
        a * (1 - q j) ≤ m - w j ∧ m - w j ≤ b * (1 - q j) := by
  simp only [leafCuts, List.mem_cons, List.not_mem_nil, or_false,
    forall_eq_or_imp, forall_eq, RationalAffineCut.eval,
    qLowerCut, qUpperCut, wLowerCut, wUpperCut, complementLowerCut, complementUpperCut,
    sum_single_mul, zero_mul, Finset.sum_const_zero, add_zero, zero_add, one_mul, neg_mul,
    neg_nonpos]
  constructor <;> rintro ⟨h₁,h₂,h₃,h₄,h₅,h₆⟩ <;> constructor <;> try assumption
  all_goals repeat' constructor
  all_goals linarith

@[simp] theorem linearCuts_eval {n : ℕ} {a b : ℚ} (ha : 0 < a) (hab : a < b)
    (m t : ℚ) (q w : Fin n → ℚ) :
    (∀ C ∈ linearCuts a b, C.eval m t q w ≤ 0) ↔
      rationalLinearBounds a b m q w ∧ t ≤ (a + b - m) / (a * b) := by
  have hp : 0 < a * b := mul_pos ha (ha.trans hab)
  simp only [linearCuts, List.forall_mem_append, List.forall_mem_cons,
    List.forall_mem_flatten, List.forall_mem_ofFn_iff]
  simp only [leafCuts_eval]
  simp only [meanLowerCut, meanUpperCut, reciprocalUpperCut,
    RationalAffineCut.eval, zero_mul, Finset.sum_const_zero, add_zero, one_mul, neg_one_mul]
  rw [le_div_iff₀ hp]
  unfold rationalLinearBounds
  constructor <;> intro h
  · obtain ⟨⟨ha', hb', ht⟩, hj⟩ := h
    exact ⟨⟨by linarith, by linarith, hj⟩, by nlinarith [ht.1]⟩
  · obtain ⟨⟨ha', hb', hj⟩, ht⟩ := h
    exact ⟨⟨by linarith, by linarith, ⟨by nlinarith [ht], by simp⟩⟩, hj⟩

/-- A direct list scan; no choice principle or real arithmetic is used. -/
def findLinearViolation {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    Option (RationalAffineCut n) :=
  (linearCuts a b).find? (fun C => decide (0 < C.eval m t q w))

theorem linearCuts_real_valid {n : ℕ} {a b : ℚ} (ha : 0 < a) (hab : a < b)
    {m t : ℝ} {q w : Fin n → ℝ} (h : point m t q w ∈ hull n a b)
    (C : RationalAffineCut n) (hC : C ∈ linearCuts a b) : C.evalReal m t q w ≤ 0 := by
  have haR : (0 : ℝ) < a := by exact_mod_cast ha
  have habR : (a : ℝ) < b := by exact_mod_cast hab
  obtain ⟨hl, _, ht⟩ := (mem_hull_iff_bounds haR habR).mp h
  have hp : (0 : ℝ) < (a : ℝ) * b := mul_pos haR (haR.trans habR)
  have ht' := (le_div_iff₀ hp).mp ht
  rcases List.mem_append.mp hC with hC | hC
  · simp only [List.mem_cons, List.not_mem_nil, or_false] at hC
    rcases hC with rfl | rfl | rfl
    all_goals simp only [meanLowerCut, meanUpperCut, reciprocalUpperCut,
      RationalAffineCut.evalReal, Rat.cast_neg, Rat.cast_one, Rat.cast_zero,
      Rat.cast_add, Rat.cast_mul, zero_mul, Finset.sum_const_zero, add_zero,
      one_mul, neg_one_mul]
    · linarith [hl.1]
    · linarith [hl.2.1]
    · nlinarith [ht']
  · obtain ⟨l, hl', hC⟩ := List.mem_flatten.mp hC
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hl'
    obtain ⟨h₁,h₂,h₃,h₄,h₅,h₆⟩ := hl.2.2 j
    simp only [leafCuts, List.mem_cons, List.not_mem_nil, or_false] at hC
    rcases hC with rfl | rfl | rfl | rfl | rfl | rfl
    all_goals simp only [qLowerCut, qUpperCut, wLowerCut, wUpperCut,
      complementLowerCut, complementUpperCut, RationalAffineCut.evalReal,
      sum_single_mul_real, Rat.cast_neg, Rat.cast_one, Rat.cast_zero,
      zero_mul, Finset.sum_const_zero, add_zero, zero_add, one_mul, neg_one_mul]
    all_goals nlinarith

theorem findLinearViolation_none {n : ℕ} {a b : ℚ} (ha : 0 < a) (hab : a < b)
    (m t : ℚ) (q w : Fin n → ℚ) :
    findLinearViolation a b m t q w = none ↔
      rationalLinearBounds a b m q w ∧ t ≤ (a + b - m) / (a * b) := by
  rw [findLinearViolation, List.find?_eq_none]
  simpa only [decide_eq_true_eq, not_lt] using linearCuts_eval ha hab m t q w

theorem findLinearViolation_sound {n : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a < b) {C : RationalAffineCut n}
    (h : findLinearViolation a b m t q w = some C) :
    0 < C.eval m t q w ∧ ∀ (m' t' : ℝ) (q' w' : Fin n → ℝ),
      point m' t' q' w' ∈ hull n a b → C.evalReal m' t' q' w' ≤ 0 := by
  refine ⟨by simpa only [decide_eq_true_eq] using List.find?_some h, ?_⟩
  intro m' t' q' w' hmem
  exact linearCuts_real_valid ha hab hmem C (List.mem_of_find?_eq_some h)

end ReciprocalAnchor.ManyLeaf
