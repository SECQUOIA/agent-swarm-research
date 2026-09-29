import Mathlib

/-!
Formal core of the succinct quadratic penalty example.  The parameter `k`
encodes `k + 1` chain variables; the paper's `n` is therefore `k + 1`.
Only the finite prefix `a 0, ..., a k` is used by `Feasible`.
-/

namespace PenaltyEncoding

noncomputable section

def delta : ℕ → ℝ
  | 0 => 1 / 4
  | k + 1 => delta k ^ 2

theorem delta_pos (k : ℕ) : 0 < delta k := by
  induction k with
  | zero => norm_num [delta]
  | succ k ih => exact sq_pos_of_pos ih

theorem delta_le_one (k : ℕ) : delta k ≤ 1 := by
  induction k with
  | zero => norm_num [delta]
  | succ k ih =>
    have h := delta_pos k
    dsimp [delta]
    nlinarith

theorem delta_closed (k : ℕ) : delta k = (1 / 2 : ℝ) ^ (2 ^ (k + 1)) := by
  induction k with
  | zero => norm_num [delta]
  | succ k ih =>
    rw [delta, ih, ← pow_mul]
    congr 1

structure Point where
  a : ℕ → ℝ
  q : ℝ
  b : ℝ
  y : ℝ

def Feasible (k : ℕ) (p : Point) : Prop :=
  1 / 4 ≤ p.a 0 ∧
  (∀ i ≤ k, 0 ≤ p.a i ∧ p.a i ≤ 1) ∧
  (∀ i < k, p.a i ^ 2 ≤ p.a (i + 1)) ∧
  (p.q = 0 ∨ p.q = 1) ∧
  (p.b = 0 ∨ p.b = 1) ∧
  -1 ≤ p.y ∧ p.y ≤ 1 ∧
  p.a k - (1 - p.q) - 2 * (1 - p.b) ≤ p.y ∧
  p.y ≤ -p.a k + (1 - p.q) + 2 * p.b

theorem sequence_lower {k : ℕ} {a : ℕ → ℝ} (hzero : 1 / 4 ≤ a 0)
    (hnonneg : ∀ i ≤ k, 0 ≤ a i)
    (hstep : ∀ i < k, a i ^ 2 ≤ a (i + 1)) :
    ∀ i ≤ k, delta i ≤ a i := by
  intro i
  induction i with
  | zero => intro _; exact hzero
  | succ i ih =>
    intro hi
    have hi' : i ≤ k := by omega
    have hrec := hstep i (by omega)
    have hlow := ih hi'
    have ha := hnonneg i hi'
    have hd := delta_pos i
    dsimp [delta]
    nlinarith

theorem chain_lower {k : ℕ} {p : Point} (hp : Feasible k p) :
    ∀ i ≤ k, delta i ≤ p.a i :=
  sequence_lower hp.1 (fun i hi => (hp.2.1 i hi).1) hp.2.2.1

theorem residual_lower {k : ℕ} {p : Point} (hp : Feasible k p)
    (hq : p.q = 1) : delta k ≤ |p.y| := by
  have ha := chain_lower hp k le_rfl
  rcases hp with ⟨_, _, _, _, hb, _, _, hlo, hhi⟩
  rcases hb with hb | hb
  · have hy : p.y ≤ -delta k := by rw [hq, hb] at hhi; linarith
    have := neg_le_abs p.y
    linarith
  · have hy : delta k ≤ p.y := by rw [hq, hb] at hlo; linarith
    exact hy.trans (le_abs_self p.y)

def zeroPoint : Point := ⟨delta, 0, 0, 0⟩
def plusPoint (k : ℕ) : Point := ⟨delta, 1, 1, delta k⟩
def minusPoint (k : ℕ) : Point := ⟨delta, 1, 0, -delta k⟩

theorem zero_feasible (k : ℕ) : Feasible k zeroPoint := by
  refine ⟨by norm_num [zeroPoint, delta], ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro i _; exact ⟨le_of_lt (delta_pos i), delta_le_one i⟩
  · intro i _; exact le_rfl
  all_goals dsimp [zeroPoint]
  · exact Or.inl rfl
  · exact Or.inl rfl
  · norm_num
  · norm_num
  · have := delta_le_one k; linarith
  · have := delta_le_one k; linarith

theorem plus_feasible (k : ℕ) : Feasible k (plusPoint k) := by
  refine ⟨by norm_num [plusPoint, delta], ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro i _; exact ⟨le_of_lt (delta_pos i), delta_le_one i⟩
  · intro i _; exact le_rfl
  all_goals dsimp [plusPoint]
  · exact Or.inr rfl
  · exact Or.inr rfl
  · have := delta_pos k; linarith
  · exact delta_le_one k
  · linarith
  · have := delta_le_one k; linarith

theorem minus_feasible (k : ℕ) : Feasible k (minusPoint k) := by
  refine ⟨by norm_num [minusPoint, delta], ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro i _; exact ⟨le_of_lt (delta_pos i), delta_le_one i⟩
  · intro i _; exact le_rfl
  all_goals dsimp [minusPoint]
  · exact Or.inr rfl
  · exact Or.inl rfl
  · have := delta_le_one k; linarith
  · have := delta_pos k; linarith
  · have := delta_le_one k; linarith
  · linarith

theorem primal_objective {k : ℕ} {p : Point} (hp : Feasible k p)
    (hy : p.y = 0) : -p.q = 0 := by
  rcases hp.2.2.2.1 with hq | hq
  · simp [hq]
  · have hres := residual_lower hp hq
    have hd := delta_pos k
    rw [hy, abs_zero] at hres
    linarith

def lagrangian (rho lam : ℝ) (p : Point) : ℝ :=
  -p.q + lam * p.y + rho * |p.y|

theorem lagrangian_zero (rho lam : ℝ) : lagrangian rho lam zeroPoint = 0 := by
  simp [lagrangian, zeroPoint]

theorem lagrangian_plus (k : ℕ) (rho lam : ℝ) :
    lagrangian rho lam (plusPoint k) = -1 + lam * delta k + rho * delta k := by
  simp [lagrangian, plusPoint, abs_of_pos (delta_pos k)]

theorem lagrangian_minus (k : ℕ) (rho lam : ℝ) :
    lagrangian rho lam (minusPoint k) = -1 - lam * delta k + rho * delta k := by
  simp [lagrangian, minusPoint, abs_of_pos (delta_pos k)]
  ring

/-- No multiplier can raise the inner problem above either witness bound. -/
theorem multiplier_witness (k : ℕ) (rho lam : ℝ) :
    ∃ p, Feasible k p ∧ lagrangian rho lam p ≤ min 0 (-1 + rho * delta k) := by
  by_cases h : 0 ≤ -1 + rho * delta k
  · exact ⟨zeroPoint, zero_feasible k, by simp [lagrangian_zero, min_eq_left h]⟩
  · have hh : -1 + rho * delta k ≤ 0 := le_of_lt (lt_of_not_ge h)
    rw [min_eq_right hh]
    by_cases hlam : 0 ≤ lam
    · refine ⟨minusPoint k, minus_feasible k, ?_⟩
      rw [lagrangian_minus]
      have := mul_nonneg hlam (le_of_lt (delta_pos k))
      linarith
    · refine ⟨plusPoint k, plus_feasible k, ?_⟩
      rw [lagrangian_plus]
      have := mul_nonpos_of_nonpos_of_nonneg (le_of_lt (lt_of_not_ge hlam))
        (le_of_lt (delta_pos k))
      linarith

/-- At multiplier zero, every feasible point meets the matching lower bound. -/
theorem zero_multiplier_lower {k : ℕ} {rho : ℝ} (hrho : 0 ≤ rho)
    {p : Point} (hp : Feasible k p) :
    min 0 (-1 + rho * delta k) ≤ lagrangian rho 0 p := by
  rcases hp.2.2.2.1 with hq | hq
  · have hnonneg := mul_nonneg hrho (abs_nonneg p.y)
    dsimp [lagrangian]
    rw [hq]
    have := min_le_left (0 : ℝ) (-1 + rho * delta k)
    linarith
  · have hres := residual_lower hp hq
    have hmul := mul_le_mul_of_nonneg_left hres hrho
    dsimp [lagrangian]
    rw [hq]
    have := min_le_right (0 : ℝ) (-1 + rho * delta k)
    linarith

def values (k : ℕ) (rho lam : ℝ) : Set ℝ :=
  {v | ∃ p, Feasible k p ∧ lagrangian rho lam p = v}

def inner (k : ℕ) (rho lam : ℝ) : ℝ := sInf (values k rho lam)

def dual (k : ℕ) (rho : ℝ) : ℝ := sSup (Set.range (inner k rho))

theorem values_nonempty (k : ℕ) (rho lam : ℝ) : (values k rho lam).Nonempty :=
  ⟨0, zeroPoint, zero_feasible k, lagrangian_zero rho lam⟩

theorem values_bddBelow (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) (lam : ℝ) :
    BddBelow (values k rho lam) := by
  refine ⟨-1 - |lam|, ?_⟩
  rintro v ⟨p, hp, rfl⟩
  have hy : |p.y| ≤ 1 := abs_le.mpr ⟨hp.2.2.2.2.2.1, hp.2.2.2.2.2.2.1⟩
  have hprod : |lam * p.y| ≤ |lam| := by
    rw [abs_mul]
    simpa using mul_le_mul_of_nonneg_left hy (abs_nonneg lam)
  have hprodlo := (abs_le.mp hprod).1
  have hq : p.q ≤ 1 := by rcases hp.2.2.2.1 with h | h <;> simp [h]
  have hpenalty := mul_nonneg hrho (abs_nonneg p.y)
  dsimp [lagrangian]
  linarith

theorem inner_le {k : ℕ} {rho : ℝ} (hrho : 0 ≤ rho) (lam : ℝ)
    {p : Point} (hp : Feasible k p) : inner k rho lam ≤ lagrangian rho lam p :=
  csInf_le (values_bddBelow k hrho lam) ⟨p, hp, rfl⟩

theorem inner_upper (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) (lam : ℝ) :
    inner k rho lam ≤ min 0 (-1 + rho * delta k) := by
  obtain ⟨p, hp, hval⟩ := multiplier_witness k rho lam
  exact (inner_le hrho lam hp).trans hval

theorem inner_zero (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) :
    inner k rho 0 = min 0 (-1 + rho * delta k) := by
  apply le_antisymm (inner_upper k hrho 0)
  apply le_csInf (values_nonempty k rho 0)
  rintro v ⟨p, hp, rfl⟩
  exact zero_multiplier_lower hrho hp

/-- The stated supremum over all real multipliers, including the inner infimum. -/
theorem dual_eq (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) :
    dual k rho = min 0 (-1 + rho * delta k) := by
  have hB : BddAbove (Set.range (inner k rho)) := by
    refine ⟨min 0 (-1 + rho * delta k), ?_⟩
    rintro v ⟨lam, rfl⟩
    exact inner_upper k hrho lam
  apply le_antisymm
  · apply csSup_le (Set.range_nonempty _)
    rintro v ⟨lam, rfl⟩
    exact inner_upper k hrho lam
  · rw [← inner_zero k hrho]
    exact le_csSup hB (Set.mem_range_self 0)

theorem exact_threshold (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) :
    dual k rho = 0 ↔ 1 / delta k ≤ rho := by
  rw [dual_eq k hrho, min_eq_left_iff, div_le_iff₀ (delta_pos k)]
  constructor <;> intro h <;> linarith

theorem reciprocal_delta (k : ℕ) :
    1 / delta k = (2 : ℝ) ^ (2 ^ (k + 1)) := by
  rw [delta_closed, one_div, ← inv_pow]
  norm_num

/-! The stronger one-binary example.  Its `b` sign selector is absent. -/

structure OnePoint where
  a : ℕ → ℝ
  q : ℝ
  y : ℝ

def OneFeasible (k : ℕ) (p : OnePoint) : Prop :=
  1 / 4 ≤ p.a 0 ∧
  (∀ i ≤ k, 0 ≤ p.a i ∧ p.a i ≤ 1) ∧
  (∀ i < k, p.a i ^ 2 ≤ p.a (i + 1)) ∧
  (p.q = 0 ∨ p.q = 1) ∧
  -1 ≤ p.y ∧ p.y ≤ 1 ∧
  p.a k - 2 * (1 - p.q) ≤ p.y

theorem one_chain_lower {k : ℕ} {p : OnePoint} (hp : OneFeasible k p) :
    ∀ i ≤ k, delta i ≤ p.a i :=
  sequence_lower hp.1 (fun i hi => (hp.2.1 i hi).1) hp.2.2.1

theorem one_residual_lower {k : ℕ} {p : OnePoint} (hp : OneFeasible k p)
    (hq : p.q = 1) : delta k ≤ p.y := by
  have ha := one_chain_lower hp k le_rfl
  have hy := hp.2.2.2.2.2.2
  rw [hq] at hy
  linarith

def oneZero : OnePoint := ⟨delta, 0, 0⟩
def onePlus (k : ℕ) : OnePoint := ⟨delta, 1, delta k⟩
def oneMinus : OnePoint := ⟨delta, 0, -1⟩

theorem one_zero_feasible (k : ℕ) : OneFeasible k oneZero := by
  refine ⟨by norm_num [oneZero, delta], ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro i _; exact ⟨le_of_lt (delta_pos i), delta_le_one i⟩
  · intro i _; exact le_rfl
  all_goals dsimp [oneZero]
  · exact Or.inl rfl
  · norm_num
  · norm_num
  · have := delta_le_one k; linarith

theorem one_plus_feasible (k : ℕ) : OneFeasible k (onePlus k) := by
  refine ⟨by norm_num [onePlus, delta], ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro i _; exact ⟨le_of_lt (delta_pos i), delta_le_one i⟩
  · intro i _; exact le_rfl
  all_goals dsimp [onePlus]
  · exact Or.inr rfl
  · have := delta_pos k; linarith
  · exact delta_le_one k
  · linarith

theorem one_minus_feasible (k : ℕ) : OneFeasible k oneMinus := by
  refine ⟨by norm_num [oneMinus, delta], ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro i _; exact ⟨le_of_lt (delta_pos i), delta_le_one i⟩
  · intro i _; exact le_rfl
  all_goals dsimp [oneMinus]
  · exact Or.inl rfl
  · norm_num
  · norm_num
  · have := delta_le_one k; linarith

theorem one_primal_objective {k : ℕ} {p : OnePoint} (hp : OneFeasible k p)
    (hy : p.y = 0) : -p.q = 0 := by
  rcases hp.2.2.2.1 with hq | hq
  · simp [hq]
  · have hres := one_residual_lower hp hq
    have hd := delta_pos k
    rw [hy] at hres
    linarith

def oneLagrangian (rho lam : ℝ) (p : OnePoint) : ℝ :=
  -p.q + lam * p.y + rho * |p.y|

def oneValue (k : ℕ) (rho : ℝ) : ℝ :=
  (2 * rho * delta k - 1) / (1 + delta k)

def oneMultiplier (k : ℕ) (rho : ℝ) : ℝ :=
  (1 + rho * (1 - delta k)) / (1 + delta k)

theorem one_lagrangian_zero (rho lam : ℝ) : oneLagrangian rho lam oneZero = 0 := by
  simp [oneLagrangian, oneZero]

theorem one_lagrangian_plus (k : ℕ) (rho lam : ℝ) :
    oneLagrangian rho lam (onePlus k) = -1 + lam * delta k + rho * delta k := by
  simp [oneLagrangian, onePlus, abs_of_pos (delta_pos k)]

theorem one_lagrangian_minus (rho lam : ℝ) :
    oneLagrangian rho lam oneMinus = rho - lam := by
  simp [oneLagrangian, oneMinus]
  ring

theorem one_weighted_identity (k : ℕ) (rho lam : ℝ) :
    oneLagrangian rho lam (onePlus k) + delta k * oneLagrangian rho lam oneMinus =
      (1 + delta k) * oneValue k rho := by
  have hd : 1 + delta k ≠ 0 := by have := delta_pos k; linarith
  rw [one_lagrangian_plus, one_lagrangian_minus]
  dsimp [oneValue]
  field_simp
  ring

/-- The two actual endpoints defeat every real multiplier. -/
theorem one_multiplier_witness (k : ℕ) (rho lam : ℝ) :
    ∃ p, OneFeasible k p ∧ oneLagrangian rho lam p ≤ min 0 (oneValue k rho) := by
  by_cases h : 0 ≤ oneValue k rho
  · exact ⟨oneZero, one_zero_feasible k, by simp [one_lagrangian_zero, min_eq_left h]⟩
  · have hh : oneValue k rho ≤ 0 := le_of_lt (lt_of_not_ge h)
    rw [min_eq_right hh]
    by_cases hminus : oneLagrangian rho lam oneMinus ≤ oneValue k rho
    · exact ⟨oneMinus, one_minus_feasible k, hminus⟩
    · refine ⟨onePlus k, one_plus_feasible k, ?_⟩
      have hid := one_weighted_identity k rho lam
      have hproduct := mul_pos (delta_pos k) (sub_pos.mpr (lt_of_not_ge hminus))
      nlinarith

theorem one_multiplier_nonneg (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) :
    0 ≤ oneMultiplier k rho := by
  dsimp [oneMultiplier]
  apply div_nonneg
  · have h := mul_nonneg hrho (sub_nonneg.mpr (delta_le_one k)); linarith
  · have := delta_pos k; linarith

theorem one_multiplier_balances (k : ℕ) (rho : ℝ) :
    rho - oneMultiplier k rho = oneValue k rho ∧
    -1 + (rho + oneMultiplier k rho) * delta k = oneValue k rho := by
  have hd : 1 + delta k ≠ 0 := by have := delta_pos k; linarith
  constructor <;> dsimp [oneMultiplier, oneValue] <;> field_simp <;> ring

/-- A concrete multiplier gives the matching lower bound on the full model. -/
theorem one_multiplier_lower {k : ℕ} {rho : ℝ} (hrho : 0 ≤ rho)
    {p : OnePoint} (hp : OneFeasible k p) :
    min 0 (oneValue k rho) ≤ oneLagrangian rho (oneMultiplier k rho) p := by
  have hlam := one_multiplier_nonneg k hrho
  have hbalance := one_multiplier_balances k rho
  rcases hp.2.2.2.1 with hq | hq
  · have hy : |p.y| ≤ 1 := abs_le.mpr ⟨hp.2.2.2.2.1, hp.2.2.2.2.2.1⟩
    have habs := abs_nonneg p.y
    have hprod := mul_nonneg hlam (show 0 ≤ p.y + |p.y| by have := neg_le_abs p.y; linarith)
    dsimp [oneLagrangian]
    rw [hq]
    by_cases hv : 0 ≤ oneValue k rho
    · rw [min_eq_left hv]
      have hm := mul_nonneg hv habs
      nlinarith [hbalance.1]
    · have hv' : oneValue k rho ≤ 0 := le_of_lt (lt_of_not_ge hv)
      rw [min_eq_right hv']
      have hm := mul_le_mul_of_nonpos_left hy hv'
      nlinarith [hbalance.1]
  · have hy := one_residual_lower hp hq
    have hypos : 0 < p.y := (delta_pos k).trans_le hy
    have hmul := mul_le_mul_of_nonneg_left hy (add_nonneg hrho hlam)
    dsimp [oneLagrangian]
    rw [hq, abs_of_pos hypos]
    have hm := min_le_right (0 : ℝ) (oneValue k rho)
    nlinarith [hbalance.2]

def oneValues (k : ℕ) (rho lam : ℝ) : Set ℝ :=
  {v | ∃ p, OneFeasible k p ∧ oneLagrangian rho lam p = v}

def oneInner (k : ℕ) (rho lam : ℝ) : ℝ := sInf (oneValues k rho lam)

def oneDual (k : ℕ) (rho : ℝ) : ℝ := sSup (Set.range (oneInner k rho))

theorem one_values_nonempty (k : ℕ) (rho lam : ℝ) : (oneValues k rho lam).Nonempty :=
  ⟨0, oneZero, one_zero_feasible k, one_lagrangian_zero rho lam⟩

theorem one_values_bddBelow (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) (lam : ℝ) :
    BddBelow (oneValues k rho lam) := by
  refine ⟨-1 - |lam|, ?_⟩
  rintro v ⟨p, hp, rfl⟩
  have hy : |p.y| ≤ 1 := abs_le.mpr ⟨hp.2.2.2.2.1, hp.2.2.2.2.2.1⟩
  have hprod : |lam * p.y| ≤ |lam| := by
    rw [abs_mul]
    simpa using mul_le_mul_of_nonneg_left hy (abs_nonneg lam)
  have hprodlo := (abs_le.mp hprod).1
  have hq : p.q ≤ 1 := by rcases hp.2.2.2.1 with h | h <;> simp [h]
  have hpenalty := mul_nonneg hrho (abs_nonneg p.y)
  dsimp [oneLagrangian]
  linarith

theorem one_inner_le {k : ℕ} {rho : ℝ} (hrho : 0 ≤ rho) (lam : ℝ)
    {p : OnePoint} (hp : OneFeasible k p) : oneInner k rho lam ≤ oneLagrangian rho lam p :=
  csInf_le (one_values_bddBelow k hrho lam) ⟨p, hp, rfl⟩

theorem one_inner_upper (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) (lam : ℝ) :
    oneInner k rho lam ≤ min 0 (oneValue k rho) := by
  obtain ⟨p, hp, hval⟩ := one_multiplier_witness k rho lam
  exact (one_inner_le hrho lam hp).trans hval

theorem one_inner_at_multiplier (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) :
    oneInner k rho (oneMultiplier k rho) = min 0 (oneValue k rho) := by
  apply le_antisymm (one_inner_upper k hrho _)
  apply le_csInf (one_values_nonempty k rho _)
  rintro v ⟨p, hp, rfl⟩
  exact one_multiplier_lower hrho hp

/-- Exact one-binary augmented dual value after optimizing every real multiplier. -/
theorem one_dual_eq (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) :
    oneDual k rho = min 0 ((2 * rho * delta k - 1) / (1 + delta k)) := by
  have hB : BddAbove (Set.range (oneInner k rho)) := by
    refine ⟨min 0 (oneValue k rho), ?_⟩
    rintro v ⟨lam, rfl⟩
    exact one_inner_upper k hrho lam
  change oneDual k rho = min 0 (oneValue k rho)
  apply le_antisymm
  · apply csSup_le (Set.range_nonempty _)
    rintro v ⟨lam, rfl⟩
    exact one_inner_upper k hrho lam
  · rw [← one_inner_at_multiplier k hrho]
    exact le_csSup hB (Set.mem_range_self _)

theorem one_exact_threshold (k : ℕ) {rho : ℝ} (hrho : 0 ≤ rho) :
    oneDual k rho = 0 ↔ 1 / (2 * delta k) ≤ rho := by
  have hd : 0 < 1 + delta k := by have := delta_pos k; linarith
  have h2d : 0 < 2 * delta k := mul_pos (by norm_num) (delta_pos k)
  rw [one_dual_eq k hrho, min_eq_left_iff, le_div_iff₀ hd, div_le_iff₀ h2d]
  constructor <;> intro h <;> nlinarith

theorem one_threshold_size (k : ℕ) :
    1 / (2 * delta k) = (2 : ℝ) ^ (2 ^ (k + 1)) / 2 := by
  rw [mul_comm 2 (delta k), div_mul_eq_div_div, reciprocal_delta]

#print axioms sequence_lower
#print axioms delta_closed
#print axioms primal_objective
#print axioms dual_eq
#print axioms exact_threshold
#print axioms one_primal_objective
#print axioms one_dual_eq
#print axioms one_exact_threshold
#print axioms one_threshold_size

end

end PenaltyEncoding
