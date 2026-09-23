import Formal.QuadraticPrecision.Parity
import Mathlib.Data.Fintype.Pigeonhole
import Mathlib.Analysis.SpecialFunctions.Log.Base

/-! Sharp one-dimensional integer-coordinate lower bounds. The finite grid
argument uses actual integer witnesses and does not assume a closed lift. -/
namespace QuadraticPrecision

def unitIntervalDomain : Set (Input 1) := {x | 0 ≤ x 0 ∧ x 0 ≤ 1}
def squareOne (x : Input 1) : ℝ := (x 0)^2
def concaveProductOne (x : Input 1) : ℝ := x 0 * (1 - x 0)

/-- There are more equally spaced contacts than parity codes. Two contacts
therefore have an integer midpoint witness, with separation at least `2⁻ᵖ`. -/
theorem interval_parity_lower {p q : ℕ} (L : ConvexIntegerLift 1 p q)
    (f : Input 1 → ℝ) (ε : ℝ)
    (hgraph : ∀ x ∈ unitIntervalDomain, (x, f x) ∈ L.relaxation)
    (herr : ∀ x y : Input 1,
      ((1 / 2 : ℝ) • x + (1 / 2 : ℝ) • y, (f x + f y) / 2) ∈ L.relaxation →
      (x 0 - y 0)^2 ≤ 4 * ε) :
    (1 / 4 : ℝ)^p / 4 ≤ ε := by
  classical
  let N : ℕ := 2^p
  have hN : 0 < N := by dsimp [N]; positivity
  have hNr : (0 : ℝ) < N := by exact_mod_cast hN
  let x : Fin (N+1) → Input 1 := fun i _ => (i.val : ℝ) / N
  have hx (i : Fin (N+1)) : x i ∈ unitIntervalDomain := by
    constructor
    · exact div_nonneg (Nat.cast_nonneg _) hNr.le
    · apply (div_le_one hNr).mpr
      exact_mod_cast (show i.val ≤ N by omega)
  have hw (i : Fin (N+1)) := hgraph (x i) (hx i)
  choose z hz using hw
  obtain ⟨i, j, hij, hcode⟩ := Fintype.exists_ne_map_eq_of_card_lt
    (fun i => parityCode (z i)) (by rw [card_parityCode]; simp [N])
  have hm := L.rawContact_midpoint
    (show x i ∈ L.rawContact unitIntervalDomain f (parityCode (z i)) from
      ⟨hx i, z i, rfl, hz i⟩)
    (show x j ∈ L.rawContact unitIntervalDomain f (parityCode (z i)) from
      ⟨hx j, z j, hcode.symm, hz j⟩)
  have he := herr (x i) (x j) hm
  have hsep : (1 : ℝ) ≤ ((i.val : ℝ) - j.val)^2 := by
    have hv : i.val ≠ j.val := fun h => hij (Fin.ext h)
    rcases lt_or_gt_of_ne hv with h | h
    · have hh : (i.val : ℝ) + 1 ≤ j.val := by exact_mod_cast h
      nlinarith
    · have hh : (j.val : ℝ) + 1 ≤ i.val := by exact_mod_cast h
      nlinarith
  have hden : (0 : ℝ) < (N : ℝ)^2 := sq_pos_of_pos hNr
  have he' : (((i.val : ℝ) - j.val)^2) / (N : ℝ)^2 ≤ 4 * ε := by
    simpa only [x, ← sub_div, div_pow] using he
  have hbound : 1 / (N : ℝ)^2 ≤ 4 * ε :=
    (div_le_div_of_nonneg_right hsep hden.le).trans he'
  have hid : (1 / (N : ℝ)^2) = (1 / 4 : ℝ)^p := by
    dsimp [N]
    push_cast
    rw [div_pow, one_pow, ← pow_mul, mul_comm p 2, pow_mul]
    norm_num
  rw [hid] at hbound
  linarith

theorem square_graph_integer_lower {ε : ℝ} {p : ℕ}
    (h : HasGraphLift unitIntervalDomain squareOne ε p) :
    (1 / 4 : ℝ)^p / 4 ≤ ε := by
  obtain ⟨q, L, hgraph, hsound⟩ := h
  apply interval_parity_lower L squareOne ε hgraph
  intro x y hm
  have hs := (hsound _ hm).2
  have he := (abs_le.mp hs).2
  simp only [squareOne, Pi.add_apply, Pi.smul_apply, smul_eq_mul] at he
  nlinarith [sq_nonneg (x 0 - y 0)]

theorem square_hypograph_integer_lower {ε : ℝ} {p : ℕ}
    (h : HasHypographLift unitIntervalDomain squareOne ε p) :
    (1 / 4 : ℝ)^p / 4 ≤ ε := by
  obtain ⟨q, L, hgraph, hsound⟩ := h
  apply interval_parity_lower L squareOne ε (fun x hx => hgraph x hx _ le_rfl)
  intro x y hm
  have he := (hsound _ hm).2
  simp only [squareOne, Pi.add_apply, Pi.smul_apply, smul_eq_mul] at he
  nlinarith [sq_nonneg (x 0 - y 0)]

theorem concaveProduct_epigraph_integer_lower {ε : ℝ} {p : ℕ}
    (h : HasEpigraphLift unitIntervalDomain concaveProductOne ε p) :
    (1 / 4 : ℝ)^p / 4 ≤ ε := by
  obtain ⟨q, L, hgraph, hsound⟩ := h
  apply interval_parity_lower L concaveProductOne ε (fun x hx => hgraph x hx _ le_rfl)
  intro x y hm
  have he := (hsound _ hm).2
  simp only [concaveProductOne, Pi.add_apply, Pi.smul_apply, smul_eq_mul] at he
  nlinarith [sq_nonneg (x 0 - y 0)]

/-- Natural ceiling implements the maximum with zero, including coarse errors. -/
noncomputable def squarePrecisionCount (ε : ℝ) : ℕ :=
  ⌈(Real.logb 2 (1 / ε) - 2) / 2⌉₊

theorem squarePrecisionCount_le_iff {ε : ℝ} (hε : 0 < ε) (p : ℕ) :
    squarePrecisionCount ε ≤ p ↔ (1 / 4 : ℝ)^p / 4 ≤ ε := by
  have hfour : Real.logb 2 4 = 2 := by
    have h := Real.logb_pow 2 2 2
    norm_num [Real.logb_self_eq_one] at h ⊢
    exact h
  have hquarter : Real.logb 2 (1 / 4) = -2 := by
    rw [Real.logb_div (by norm_num) (by norm_num), Real.logb_one, hfour]
    norm_num
  have hlog : Real.logb 2 ((1 / 4 : ℝ)^p / 4) = -2 * (p : ℝ) - 2 := by
    rw [Real.logb_div (by positivity) (by norm_num), Real.logb_pow, hquarter, hfour]
    ring
  have hinv : Real.logb 2 (1 / ε) = -Real.logb 2 ε := by
    simp only [one_div, Real.logb_inv]
  rw [squarePrecisionCount, Nat.ceil_le,
    ← Real.logb_le_logb (by norm_num : (1 : ℝ) < 2) (by positivity) hε,
    hlog, hinv]
  constructor <;> intro h <;> linarith

theorem squarePrecisionCount_sufficient {ε : ℝ} (hε : 0 < ε) :
    (1 / 4 : ℝ)^(squarePrecisionCount ε) / 4 ≤ ε :=
  (squarePrecisionCount_le_iff hε _).mp le_rfl

theorem square_graph_count_lower {ε : ℝ} (hε : 0 < ε) {p : ℕ}
    (h : HasGraphLift unitIntervalDomain squareOne ε p) :
    squarePrecisionCount ε ≤ p :=
  (squarePrecisionCount_le_iff hε p).mpr (square_graph_integer_lower h)

end QuadraticPrecision
