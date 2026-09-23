import Mathlib

/-! The constant-coefficient paired-squaring input circuit for primitive FBBT. -/
namespace FBBT

noncomputable section

def bValue (n : ℕ) : ℝ := (1 / 2 : ℝ) ^ (2 ^ n)
def cValue (n : ℕ) : ℝ := 1 - bValue n

@[simp] theorem bValue_zero : bValue 0 = 1 / 2 := by norm_num [bValue]
@[simp] theorem cValue_zero : cValue 0 = 1 / 2 := by norm_num [cValue]

theorem bValue_pos (n : ℕ) : 0 < bValue n := by
  unfold bValue
  positivity
theorem bValue_le_one (n : ℕ) : bValue n ≤ 1 := by
  exact pow_le_one₀ (by norm_num) (by norm_num)
theorem bValue_lt_one (n : ℕ) : bValue n < 1 := by
  exact pow_lt_one₀ (by norm_num) (by norm_num) (by positivity)
theorem cValue_nonneg (n : ℕ) : 0 ≤ cValue n := by
  unfold cValue; linarith [bValue_le_one n]
theorem cValue_pos (n : ℕ) : 0 < cValue n := by
  unfold cValue; linarith [bValue_lt_one n]
theorem cValue_lt_one (n : ℕ) : cValue n < 1 := by
  unfold cValue; linarith [bValue_pos n]
@[simp] theorem bValue_add_cValue (n : ℕ) : bValue n + cValue n = 1 := by
  simp [cValue]

theorem bValue_succ (n : ℕ) : bValue (n + 1) = bValue n * bValue n := by
  simp [bValue, pow_succ, pow_mul]
theorem cValue_succ (n : ℕ) : cValue (n + 1) = cValue n + bValue n * cValue n := by
  rw [cValue, bValue_succ]; unfold cValue; ring

theorem bValue_inverse_power (n : ℕ) : bValue n = ((2 : ℝ) ^ (2 ^ n))⁻¹ := by
  simp [bValue, one_div, inv_pow]

/-- Two initial variables, four per squaring stage, and two feedback variables. -/
inductive CircuitVar (n : ℕ) where
  | b : Fin (n + 1) → CircuitVar n
  | c : Fin (n + 1) → CircuitVar n
  | h : Fin n → CircuitVar n
  | v : Fin n → CircuitVar n
  | z : CircuitVar n
  | w : CircuitVar n
  deriving DecidableEq, Fintype

/-- Only the literal `1/2`, a copy, addition, and a product occur. -/
inductive PrimitiveRhs (α : Type*) where
  | half : PrimitiveRhs α
  | copy : α → PrimitiveRhs α
  | add : α → α → PrimitiveRhs α
  | mul : α → α → PrimitiveRhs α
  deriving DecidableEq

def PrimitiveRhs.eval {α : Type*} (x : α → ℝ) : PrimitiveRhs α → ℝ
  | .half => 1 / 2
  | .copy a => x a
  | .add a b => x a + x b
  | .mul a b => x a * x b

def PrimitiveRhs.arguments {α : Type*} [DecidableEq α] : PrimitiveRhs α → Finset α
  | .half => ∅
  | .copy a => {a}
  | .add a b => {a, b}
  | .mul a b => {a, b}

def circuitRhs (n : ℕ) : CircuitVar n → PrimitiveRhs (CircuitVar n)
  | .b ⟨0, _⟩ => .half
  | .b ⟨i + 1, hi⟩ => .mul (.b ⟨i, by omega⟩) (.h ⟨i, by omega⟩)
  | .c ⟨0, _⟩ => .half
  | .c ⟨i + 1, hi⟩ => .add (.c ⟨i, by omega⟩) (.v ⟨i, by omega⟩)
  | .h i => .copy (.b i.castSucc)
  | .v i => .mul (.b i.castSucc) (.c i.castSucc)
  | .z => .add (.b (Fin.last n)) .w
  | .w => .mul (.c (Fin.last n)) .z

def CircuitSolution (n : ℕ) (x : CircuitVar n → ℝ) : Prop :=
  ∀ a, x a = (circuitRhs n a).eval x

def circuitPoint (n : ℕ) : CircuitVar n → ℝ
  | .b i => bValue i
  | .c i => cValue i
  | .h i => bValue i
  | .v i => bValue i * cValue i
  | .z => 1
  | .w => cValue n

theorem circuitPoint_solution (n : ℕ) : CircuitSolution n (circuitPoint n) := by
  intro a
  cases a with
  | b i =>
    obtain ⟨i, hi⟩ := i
    cases i with
    | zero => simp [circuitPoint, circuitRhs, PrimitiveRhs.eval]
    | succ i => simpa [circuitPoint, circuitRhs, PrimitiveRhs.eval] using bValue_succ i
  | c i =>
    obtain ⟨i, hi⟩ := i
    cases i with
    | zero => simp [circuitPoint, circuitRhs, PrimitiveRhs.eval]
    | succ i => simpa [circuitPoint, circuitRhs, PrimitiveRhs.eval] using cValue_succ i
  | h i => rfl
  | v i => rfl
  | z => simp [circuitPoint, circuitRhs, PrimitiveRhs.eval]
  | w => simp [circuitPoint, circuitRhs, PrimitiveRhs.eval]

theorem circuitPoint_mem_unit (n : ℕ) (a : CircuitVar n) :
    0 ≤ circuitPoint n a ∧ circuitPoint n a ≤ 1 := by
  cases a with
  | b i => exact ⟨(bValue_pos i).le, bValue_le_one i⟩
  | c i => exact ⟨cValue_nonneg i, (cValue_lt_one i).le⟩
  | h i => exact ⟨(bValue_pos i).le, bValue_le_one i⟩
  | v i => exact ⟨mul_nonneg (bValue_pos i).le (cValue_nonneg i),
      mul_le_one₀ (bValue_le_one i) (cValue_nonneg i) (cValue_lt_one i).le⟩
  | z => norm_num [circuitPoint]
  | w => exact ⟨cValue_nonneg n, (cValue_lt_one n).le⟩

theorem circuitSolution_upstream {n : ℕ} {x : CircuitVar n → ℝ}
    (hx : CircuitSolution n x) (i : Fin (n + 1)) :
    x (.b i) = bValue i ∧ x (.c i) = cValue i := by
  obtain ⟨i, hi⟩ := i
  induction i with
  | zero =>
    constructor
    · simpa [circuitRhs, PrimitiveRhs.eval] using hx (.b ⟨0, hi⟩)
    · simpa [circuitRhs, PrimitiveRhs.eval] using hx (.c ⟨0, hi⟩)
  | succ i ih =>
    obtain ⟨hb, hc⟩ := ih (by omega)
    have hh := hx (.h ⟨i, by omega⟩)
    have hv := hx (.v ⟨i, by omega⟩)
    simp only [circuitRhs, PrimitiveRhs.eval] at hh hv
    constructor
    · have he := hx (.b ⟨i + 1, hi⟩)
      simpa [circuitRhs, PrimitiveRhs.eval, hh, hb, bValue_succ] using he
    · have he := hx (.c ⟨i + 1, hi⟩)
      simpa [circuitRhs, PrimitiveRhs.eval, hv, hb, hc, cValue_succ] using he

theorem circuitSolution_feedback {n : ℕ} {x : CircuitVar n → ℝ}
    (hx : CircuitSolution n x) : x .z = 1 ∧ x .w = cValue n := by
  obtain ⟨hb, hc⟩ := circuitSolution_upstream hx (Fin.last n)
  have hz := hx .z
  have hw := hx .w
  simp only [circuitRhs, PrimitiveRhs.eval, hb, hc, Fin.val_last] at hz hw
  have hmul : bValue n * (x .z - 1) = 0 := by
    dsimp [cValue] at hw
    nlinarith [hz, hw]
  have hz1 : x .z = 1 := by
    have := (mul_eq_zero.mp hmul).resolve_left (ne_of_gt (bValue_pos n))
    linarith
  exact ⟨hz1, by simpa [hz1] using hw⟩

theorem circuitSolution_unique {n : ℕ} {x : CircuitVar n → ℝ}
    (hx : CircuitSolution n x) : x = circuitPoint n := by
  funext a
  cases a with
  | b i => exact (circuitSolution_upstream hx i).1
  | c i => exact (circuitSolution_upstream hx i).2
  | h i =>
    simpa [circuitRhs, PrimitiveRhs.eval, circuitPoint,
      (circuitSolution_upstream hx i.castSucc).1] using hx (.h i)
  | v i =>
    simpa [circuitRhs, PrimitiveRhs.eval, circuitPoint,
      (circuitSolution_upstream hx i.castSucc).1,
      (circuitSolution_upstream hx i.castSucc).2] using hx (.v i)
  | z => exact (circuitSolution_feedback hx).1
  | w => exact (circuitSolution_feedback hx).2

theorem circuit_unique_feasible (n : ℕ) :
    ∃! x : CircuitVar n → ℝ, CircuitSolution n x ∧ ∀ a, 0 ≤ x a ∧ x a ≤ 1 := by
  refine ⟨circuitPoint n, ⟨circuitPoint_solution n, circuitPoint_mem_unit n⟩, ?_⟩
  intro x hx
  exact circuitSolution_unique hx.1

/-- Fixing all upstream variables to their exact values satisfies every upstream equation. -/
theorem upstreamEquation_independent {n : ℕ} {x : CircuitVar n → ℝ}
    (hx : ∀ a, a ≠ .z → a ≠ .w → x a = circuitPoint n a)
    (a : CircuitVar n) (haz : a ≠ .z) (haw : a ≠ .w) :
    x a = (circuitRhs n a).eval x := by
  rw [hx a haz haw]
  have he := circuitPoint_solution n a
  rw [he]
  cases a with
  | b i =>
    obtain ⟨i, hi⟩ := i
    cases i <;> simp [circuitRhs, PrimitiveRhs.eval, hx]
  | c i =>
    obtain ⟨i, hi⟩ := i
    cases i <;> simp [circuitRhs, PrimitiveRhs.eval, hx]
  | h i => simp [circuitRhs, PrimitiveRhs.eval, hx]
  | v i => simp [circuitRhs, PrimitiveRhs.eval, hx]
  | z => contradiction
  | w => contradiction

/-- Equation indices are precisely variable names: one equation defines each variable. -/
theorem circuit_variable_count (n : ℕ) : Fintype.card (CircuitVar n) = 4 * n + 4 := by
  rw [← Fintype.card_congr (CircuitVar.proxyTypeEquiv n)]
  simp
  omega

theorem circuit_equation_count (n : ℕ) :
    Fintype.card {_a : CircuitVar n // True} = 4 * n + 4 := by
  simpa using circuit_variable_count n

theorem circuit_product_distinct {n : ℕ} {a u v : CircuitVar n}
    (h : circuitRhs n a = .mul u v) : u ≠ v := by
  cases a with
  | b i =>
    obtain ⟨i, hi⟩ := i
    cases i <;> simp_all [circuitRhs]
    obtain ⟨rfl, rfl⟩ := h
    simp
  | c i =>
    obtain ⟨i, hi⟩ := i
    cases i <;> simp_all [circuitRhs]
  | h i => simp_all [circuitRhs]
  | v i =>
    simp only [circuitRhs, PrimitiveRhs.mul.injEq] at h
    obtain ⟨rfl, rfl⟩ := h
    simp
  | z => simp_all [circuitRhs]
  | w =>
    simp only [circuitRhs, PrimitiveRhs.mul.injEq] at h
    obtain ⟨rfl, rfl⟩ := h
    simp

theorem circuit_equation_names (n : ℕ) (a : CircuitVar n) :
    (insert a (circuitRhs n a).arguments).card ≤ 3 := by
  have h : ∀ e : PrimitiveRhs (CircuitVar n), e.arguments.card ≤ 2 := by
    intro e
    cases e with
    | half => simp [PrimitiveRhs.arguments]
    | copy a => simp [PrimitiveRhs.arguments]
    | add a b =>
      simpa [PrimitiveRhs.arguments] using Finset.card_insert_le a ({b} : Finset (CircuitVar n))
    | mul a b =>
      simpa [PrimitiveRhs.arguments] using Finset.card_insert_le a ({b} : Finset (CircuitVar n))
  exact (Finset.card_insert_le _ _).trans (by have := h (circuitRhs n a); omega)

/-- Dependency edges point from a defined variable to an argument of its equation. -/
def CircuitDependency {n : ℕ} (a b : CircuitVar n) : Prop :=
  b ∈ (circuitRhs n a).arguments

def circuitRank {n : ℕ} : CircuitVar n → ℕ
  | .b i => 3 * i.val
  | .c i => 3 * i.val
  | .h i => 3 * i.val + 1
  | .v i => 3 * i.val + 1
  | .z => 3 * n + 1
  | .w => 3 * n + 1

theorem upstream_dependency_rank {n : ℕ} {a b : CircuitVar n}
    (haz : a ≠ .z) (haw : a ≠ .w) (hab : CircuitDependency a b) :
    circuitRank b < circuitRank a := by
  cases a with
  | b i =>
    obtain ⟨i, hi⟩ := i
    cases i with
    | zero => simp [CircuitDependency, circuitRhs, PrimitiveRhs.arguments] at hab
    | succ i =>
      simp only [CircuitDependency, circuitRhs, PrimitiveRhs.arguments,
        Finset.mem_insert, Finset.mem_singleton] at hab
      rcases hab with rfl | rfl <;> simp [circuitRank]; omega
  | c i =>
    obtain ⟨i, hi⟩ := i
    cases i with
    | zero => simp [CircuitDependency, circuitRhs, PrimitiveRhs.arguments] at hab
    | succ i =>
      simp only [CircuitDependency, circuitRhs, PrimitiveRhs.arguments,
        Finset.mem_insert, Finset.mem_singleton] at hab
      rcases hab with rfl | rfl <;> simp [circuitRank]; omega
  | h i => simp_all [CircuitDependency, circuitRhs, PrimitiveRhs.arguments, circuitRank]
  | v i =>
    simp only [CircuitDependency, circuitRhs, PrimitiveRhs.arguments,
      Finset.mem_insert, Finset.mem_singleton] at hab
    rcases hab with rfl | rfl <;> simp [circuitRank]
  | z => contradiction
  | w => contradiction

theorem dependency_rank {n : ℕ} {a b : CircuitVar n}
    (hab : CircuitDependency a b) : circuitRank b ≤ circuitRank a := by
  by_cases haz : a = .z
  · subst a
    simp only [CircuitDependency, circuitRhs, PrimitiveRhs.arguments,
      Finset.mem_insert, Finset.mem_singleton] at hab
    rcases hab with rfl | rfl <;> simp [circuitRank]
  by_cases haw : a = .w
  · subst a
    simp only [CircuitDependency, circuitRhs, PrimitiveRhs.arguments,
      Finset.mem_insert, Finset.mem_singleton] at hab
    rcases hab with rfl | rfl <;> simp [circuitRank]
  exact (upstream_dependency_rank haz haw hab).le

theorem dependency_path_rank {n : ℕ} {a b : CircuitVar n}
    (hab : Relation.ReflTransGen CircuitDependency a b) : circuitRank b ≤ circuitRank a := by
  induction hab using Relation.ReflTransGen.head_induction_on with
  | refl => exact le_refl _
  | head h _ ih => exact ih.trans (dependency_rank h)

/-- Every directed cycle is confined to the two feedback variables. -/
theorem circuit_cycle_only_feedback {n : ℕ} {a : CircuitVar n}
    (hcycle : Relation.TransGen CircuitDependency a a) : a = .z ∨ a = .w := by
  by_contra h
  push Not at h
  have hs : ∀ {b}, Relation.TransGen CircuitDependency a b → circuitRank b < circuitRank a := by
    intro b hp
    induction hp with
    | single hab => exact upstream_dependency_rank h.1 h.2 hab
    | tail _ hab ih => exact lt_of_le_of_lt (dependency_rank hab) ih
  exact (lt_irrefl _ (hs hcycle))

theorem circuit_feedback_cycle (n : ℕ) :
    CircuitDependency (CircuitVar.z : CircuitVar n) .w ∧
    CircuitDependency (CircuitVar.w : CircuitVar n) .z := by
  simp [CircuitDependency, circuitRhs, PrimitiveRhs.arguments]

end
end FBBT
