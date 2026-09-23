import Mathlib

/-!
# SC19: elimination of the cumulative states in the all-initial-modes family

This module discharges obligation SC19 of `topics/17-grid-switching/CLAIMS.md`, the step
"Eliminate cumulative states" of the proof of `thm:finite-one` in
`paper-switching-control/sections/08-finite-grid-one-switch.tex`.

The module is deliberately **standalone and purely algebraic**: it does not import
`Formal.GridSwitching.Model`, uses no measure theory, and speaks only about real numbers.
The mode count `n` enters as a real parameter `nu` subject to `3 ≤ nu`, and the grid data
`t_a, t_b, t_{a-1}, t_{b-1}` enter as reals `A, B, P, Q`. This is exactly the content that an
earlier published version of the formula got wrong, so every equivalence below is proved in
both directions and no comparison is assumed.

## Contents

* `L`, `U` (`eq:grid-L`, `eq:grid-U`) and `Admissible` (`eq:grid-admissible`).
* `MLower`, `MUpper`, `MNonempty` (`eq:grid-M-interval`).
* The eight endpoint comparisons of the paragraph "Compare the four lower endpoints":
  `cmp_TA_TP`, `cmp_EQ_EB` (the two automatic ones, with the unconditional forms
  `cmp_TA_TP_of_le` and `cmp_EQ_EB_of_le`), `cmp_EA_EB` (which *is* the first inequality of
  `eq:grid-admissible`), and the five remaining ones `cmp_Tnu_TP`, `cmp_Tnu_EB`, `cmp_TA_EB`,
  `cmp_EQ_TP`, `cmp_EA_TP`. Each is stated as an `Iff`, so both directions are available.
* `mNonempty_iff_comparisons`: nonemptiness of the `M`-interval is *exactly* the conjunction
  of the eight comparisons, in their reduced forms.
* `elimination_iff`: the packaged equivalence
  `M`-interval nonempty ∧ `T/3 ≤ E` ∧ `E ≤ A` ∧ `nu*E ≤ (nu-2)*A+B`
  ↔ `Admissible` ∧ `L ≤ E` ∧ `E ≤ U`.
* `StateOK`, `reconX`, `reconY` (`eq:grid-xy-reconstruct`), the explicit reconstruction
  `stateOK_recon`, and the state-existence equivalence `exists_state_iff`, together with the
  two boundary specializations `exists_state_iff_same_cell` (`a = b`) and
  `exists_state_iff_last_cell` (`b = N`).

## Hypotheses

Division is total in Lean, so the hypotheses that the source leaves implicit are stated. The
order hypotheses are kept minimal and non-strict, which is what makes the boundary cases
`a = b` (`A = B`, `P = Q`) and `b = N` (`B = T`) instances of the general statements rather
than separate arguments.
-/

namespace GridSwitching

variable {nu T A B P Q E x y M : ℝ}

/-! ## The formula data -/

/-- `L_ab` of `eq:grid-L`. -/
noncomputable def L (nu T A B : ℝ) : ℝ :=
  max (T / 3) (max ((nu - 1) * T / nu - B) (((nu - 1) * T - A - (nu - 1) * B) / nu))

/-- `U_ab` of `eq:grid-U`. -/
noncomputable def U (nu T A B P Q : ℝ) : ℝ :=
  min A (min (((nu - 2) * A + B) / nu) (min ((nu - 1) * T / nu - P)
    (min (((nu - 1) * T - P - (nu - 1) * Q) / nu) ((T - P + (nu - 2) * A) / nu))))

/-- The first inequality of `eq:grid-admissible`. -/
def Admissible (nu T A B : ℝ) : Prop := (nu - 2) * (T - A) ≤ (nu - 1) * B

/-- The maximum of the four lower endpoints of `eq:grid-M-interval`. -/
noncomputable def MLower (nu T A Q E : ℝ) : ℝ :=
  max (T / nu) (max (T - A - E)
    (max ((nu - 1) * (E + Q) - (nu - 2) * T) ((nu - 1) * E - (nu - 2) * A)))

/-- The minimum of the two upper endpoints of `eq:grid-M-interval`. -/
noncomputable def MUpper (nu T B P E : ℝ) : ℝ :=
  min (T - P - E) ((nu - 1) * (E + B) - (nu - 2) * T)

/-- The `M`-interval of `eq:grid-M-interval` is nonempty. -/
def MNonempty (nu T A B P Q E : ℝ) : Prop :=
  ∃ M : ℝ, MLower nu T A Q E ≤ M ∧ M ≤ MUpper nu T B P E

/-- Nonemptiness of the `M`-interval is the comparison of its two ends. -/
theorem mNonempty_iff (nu T A B P Q E : ℝ) :
    MNonempty nu T A B P Q E ↔ MLower nu T A Q E ≤ MUpper nu T B P E :=
  ⟨fun ⟨_, h1, h2⟩ => h1.trans h2, fun h => ⟨_, le_rfl, h⟩⟩

/-! ## The eight endpoint comparisons

The four lower endpoints of `eq:grid-M-interval` are `T/nu`, `T - A - E`,
`(nu-1)*(E+Q) - (nu-2)*T` and `(nu-1)*E - (nu-2)*A`; the two upper endpoints are
`T - P - E` and `(nu-1)*(E+B) - (nu-2)*T`. Each of the eight comparisons is proved to be
*equivalent* to the stated reduced condition.
-/

/-- Comparison `T - A - E ≤ T - P - E`: it is equivalent to `P ≤ A`, hence automatic on a
grid. No hypothesis on `nu` is used. -/
theorem cmp_TA_TP (T A P E : ℝ) : T - A - E ≤ T - P - E ↔ P ≤ A := by
  constructor <;> intro h <;> linarith

/-- The automatic form of `cmp_TA_TP`. -/
theorem cmp_TA_TP_of_le (T E : ℝ) (hPA : P ≤ A) : T - A - E ≤ T - P - E :=
  (cmp_TA_TP T A P E).2 hPA

/-- Comparison `(nu-1)*(E+Q) - (nu-2)*T ≤ (nu-1)*(E+B) - (nu-2)*T`: it is equivalent to
`Q ≤ B`, hence automatic on a grid. -/
theorem cmp_EQ_EB (hnu : 3 ≤ nu) (T B Q E : ℝ) :
    (nu - 1) * (E + Q) - (nu - 2) * T ≤ (nu - 1) * (E + B) - (nu - 2) * T ↔ Q ≤ B := by
  have hnu1 : (0 : ℝ) < nu - 1 := by linarith
  constructor
  · intro h
    have key : (nu - 1) * Q ≤ (nu - 1) * B := by linarith
    exact le_of_mul_le_mul_left key hnu1
  · intro h
    nlinarith [mul_le_mul_of_nonneg_left h hnu1.le]

/-- The automatic form of `cmp_EQ_EB`. -/
theorem cmp_EQ_EB_of_le (hnu : 3 ≤ nu) (T E : ℝ) (hQB : Q ≤ B) :
    (nu - 1) * (E + Q) - (nu - 2) * T ≤ (nu - 1) * (E + B) - (nu - 2) * T :=
  (cmp_EQ_EB hnu T B Q E).2 hQB

/-- Comparison `(nu-1)*E - (nu-2)*A ≤ (nu-1)*(E+B) - (nu-2)*T`: it is *exactly* the first
inequality of `eq:grid-admissible`. No hypothesis whatsoever is used. -/
theorem cmp_EA_EB (nu T A B E : ℝ) :
    (nu - 1) * E - (nu - 2) * A ≤ (nu - 1) * (E + B) - (nu - 2) * T ↔ Admissible nu T A B := by
  unfold Admissible
  constructor <;> intro h <;> nlinarith [h]

/-- Comparison `T/nu ≤ T - P - E`: it is the `(nu-1)*T/nu - P` term of `U`. -/
theorem cmp_Tnu_TP (hnu : 3 ≤ nu) (T P E : ℝ) :
    T / nu ≤ T - P - E ↔ E ≤ (nu - 1) * T / nu - P := by
  have hnu0 : (0 : ℝ) < nu := by linarith
  rw [div_le_iff₀ hnu0, le_sub_iff_add_le, le_div_iff₀ hnu0]
  constructor <;> intro h <;> nlinarith [h]

/-- Comparison `T/nu ≤ (nu-1)*(E+B) - (nu-2)*T`: it is the `(nu-1)*T/nu - B` term of `L`. -/
theorem cmp_Tnu_EB (hnu : 3 ≤ nu) (T B E : ℝ) :
    T / nu ≤ (nu - 1) * (E + B) - (nu - 2) * T ↔ (nu - 1) * T / nu - B ≤ E := by
  have hnu0 : (0 : ℝ) < nu := by linarith
  have hnu1 : (0 : ℝ) < nu - 1 := by linarith
  rw [div_le_iff₀ hnu0, sub_le_iff_le_add, div_le_iff₀ hnu0]
  constructor
  · intro h
    have key : (nu - 1) * ((nu - 1) * T) ≤ (nu - 1) * ((E + B) * nu) := by nlinarith [h]
    exact le_of_mul_le_mul_left key hnu1
  · intro h
    nlinarith [mul_le_mul_of_nonneg_left h hnu1.le]

/-- Comparison `T - A - E ≤ (nu-1)*(E+B) - (nu-2)*T`: it is the
`((nu-1)*T - A - (nu-1)*B)/nu` term of `L`. -/
theorem cmp_TA_EB (hnu : 3 ≤ nu) (T A B E : ℝ) :
    T - A - E ≤ (nu - 1) * (E + B) - (nu - 2) * T ↔
      ((nu - 1) * T - A - (nu - 1) * B) / nu ≤ E := by
  have hnu0 : (0 : ℝ) < nu := by linarith
  rw [div_le_iff₀ hnu0]
  constructor <;> intro h <;> nlinarith [h]

/-- Comparison `(nu-1)*(E+Q) - (nu-2)*T ≤ T - P - E`: it is the
`((nu-1)*T - P - (nu-1)*Q)/nu` term of `U`. -/
theorem cmp_EQ_TP (hnu : 3 ≤ nu) (T P Q E : ℝ) :
    (nu - 1) * (E + Q) - (nu - 2) * T ≤ T - P - E ↔
      E ≤ ((nu - 1) * T - P - (nu - 1) * Q) / nu := by
  have hnu0 : (0 : ℝ) < nu := by linarith
  rw [le_div_iff₀ hnu0]
  constructor <;> intro h <;> nlinarith [h]

/-- Comparison `(nu-1)*E - (nu-2)*A ≤ T - P - E`: it is the `(T - P + (nu-2)*A)/nu` term
of `U`. -/
theorem cmp_EA_TP (hnu : 3 ≤ nu) (T A P E : ℝ) :
    (nu - 1) * E - (nu - 2) * A ≤ T - P - E ↔ E ≤ (T - P + (nu - 2) * A) / nu := by
  have hnu0 : (0 : ℝ) < nu := by linarith
  rw [le_div_iff₀ hnu0]
  constructor <;> intro h <;> nlinarith [h]

/-! ## The packaged equivalence -/

/-- Nonemptiness of the `M`-interval is exactly the conjunction of the eight endpoint
comparisons, each in its reduced form. Only `3 ≤ nu` is needed; in particular the two
"automatic" comparisons appear here as the genuine conditions `P ≤ A` and `Q ≤ B`. -/
theorem mNonempty_iff_comparisons (hnu : 3 ≤ nu) (T A B P Q E : ℝ) :
    MNonempty nu T A B P Q E ↔
      (P ≤ A ∧ Q ≤ B ∧ Admissible nu T A B ∧
        E ≤ (nu - 1) * T / nu - P ∧ (nu - 1) * T / nu - B ≤ E ∧
        ((nu - 1) * T - A - (nu - 1) * B) / nu ≤ E ∧
        E ≤ ((nu - 1) * T - P - (nu - 1) * Q) / nu ∧
        E ≤ (T - P + (nu - 2) * A) / nu) := by
  rw [mNonempty_iff]
  simp only [MLower, MUpper, max_le_iff, le_min_iff]
  rw [cmp_Tnu_TP hnu, cmp_Tnu_EB hnu, cmp_TA_TP, cmp_TA_EB hnu, cmp_EQ_TP hnu,
    cmp_EQ_EB hnu, cmp_EA_TP hnu, cmp_EA_EB]
  tauto

/-- **SC19, the endpoint comparisons.** The comparisons of `eq:grid-M-interval`, together
with the side conditions `T/3 ≤ E`, `E ≤ A` and `nu*E ≤ (nu-2)*A + B`, are exactly
`eq:grid-admissible` together with `L_ab ≤ E ≤ U_ab`.

Both directions are proved. The only order hypotheses used are `P ≤ A` and `Q ≤ B`, which
are what make the two automatic comparisons automatic. -/
theorem elimination_iff (hnu : 3 ≤ nu) (hPA : P ≤ A) (hQB : Q ≤ B) (T E : ℝ) :
    (MNonempty nu T A B P Q E ∧ T / 3 ≤ E ∧ E ≤ A ∧ nu * E ≤ (nu - 2) * A + B) ↔
      (Admissible nu T A B ∧ L nu T A B ≤ E ∧ E ≤ U nu T A B P Q) := by
  have hnu0 : (0 : ℝ) < nu := by linarith
  have hdiv : E ≤ ((nu - 2) * A + B) / nu ↔ nu * E ≤ (nu - 2) * A + B := by
    rw [le_div_iff₀ hnu0]
    constructor <;> intro h <;> nlinarith [h]
  rw [mNonempty_iff_comparisons hnu]
  simp only [L, U, max_le_iff, le_min_iff, hdiv]
  constructor
  · rintro ⟨⟨-, -, hadm, h4, h5, h6, h7, h8⟩, hT3, hEA, hs⟩
    exact ⟨hadm, ⟨hT3, h5, h6⟩, hEA, hs, h4, h7, h8⟩
  · rintro ⟨hadm, ⟨hT3, h5, h6⟩, hEA, hs, h4, h7, h8⟩
    exact ⟨⟨hPA, hQB, hadm, h4, h5, h6, h7, h8⟩, hT3, hEA, hs⟩

/-! ## State existence and the reconstruction `eq:grid-xy-reconstruct` -/

/-- The full list of constraints on the cumulative state `(x, y, M)` of the distinguished
mode: `x = A_1(A)`, `y = A_1(B)`, `M = m_1`, with every other mode carrying
`(A-x)/(nu-1)`, `(B-y)/(nu-1)`, `(T-M)/(nu-1)`.

The six monotonicity inequalities come first, then the two failure constraints, then the
four cutoff constraints, then `T/nu ≤ M` (mode `1` has the largest mass). -/
def StateOK (nu T A B P Q E x y M : ℝ) : Prop :=
  0 ≤ x ∧ x ≤ y ∧ y ≤ M ∧ 0 ≤ A - x ∧ A - x ≤ B - y ∧ B - y ≤ T - M ∧
  (nu - 1) * E - (nu - 2) * A ≤ x ∧ y ≤ B - E ∧
  T - A ≤ E + M ∧ E + M ≤ T - P ∧
  T - B ≤ E + (T - M) / (nu - 1) ∧ E + (T - M) / (nu - 1) ≤ T - Q ∧
  T / nu ≤ M

/-- The `x` of `eq:grid-xy-reconstruct`. -/
noncomputable def reconX (nu T A E M : ℝ) : ℝ :=
  max 0 (max ((nu - 1) * E - (nu - 2) * A) (A - T + M))

/-- The `y` of `eq:grid-xy-reconstruct`. -/
noncomputable def reconY (nu T A B E M : ℝ) : ℝ :=
  max (reconX nu T A E M) (B - T + M)

/-- **SC19, the reconstruction.** For any `M` in the `M`-interval, the explicit state
`eq:grid-xy-reconstruct` satisfies *every* constraint of `StateOK`.

The source verifies two of these inequalities explicitly; all thirteen are verified here.
Order hypotheses used: `3 ≤ nu`, `0 ≤ P`, `P ≤ A`, `A ≤ B`, `B ≤ T`. All are non-strict, so
`A = B` (with `P = Q`) and `B = T` are covered. -/
theorem stateOK_recon (hnu : 3 ≤ nu) (hP : 0 ≤ P) (hPA : P ≤ A) (hAB : A ≤ B) (hBT : B ≤ T)
    (hEA : E ≤ A) (hE2 : nu * E ≤ (nu - 2) * A + B)
    (hlow : MLower nu T A Q E ≤ M) (hupp : M ≤ MUpper nu T B P E) :
    StateOK nu T A B P Q E (reconX nu T A E M) (reconY nu T A B E M) M := by
  have hnu0 : (0 : ℝ) < nu := by linarith
  have hnu1 : (0 : ℝ) < nu - 1 := by linarith
  have hA0 : (0 : ℝ) ≤ A := le_trans hP hPA
  have hAT : A ≤ T := le_trans hAB hBT
  have hT0 : (0 : ℝ) ≤ T := le_trans hA0 hAT
  -- the four lower and two upper endpoint bounds on `M`
  have hl1 : T / nu ≤ M := le_trans (le_max_left _ _) hlow
  have hl2 : T - A - E ≤ M :=
    le_trans ((le_max_left _ _).trans (le_max_right _ _)) hlow
  have hl3 : (nu - 1) * (E + Q) - (nu - 2) * T ≤ M :=
    le_trans (((le_max_left _ _).trans (le_max_right _ _)).trans (le_max_right _ _)) hlow
  have hl4 : (nu - 1) * E - (nu - 2) * A ≤ M :=
    le_trans (((le_max_right _ _).trans (le_max_right _ _)).trans (le_max_right _ _)) hlow
  have hu1 : M ≤ T - P - E := le_trans hupp (min_le_left _ _)
  have hu2 : M ≤ (nu - 1) * (E + B) - (nu - 2) * T := le_trans hupp (min_le_right _ _)
  -- derived facts
  have hM0 : (0 : ℝ) ≤ M := le_trans (div_nonneg hT0 hnu0.le) hl1
  have hMT : M ≤ T := by
    have k1 : (0 : ℝ) ≤ (nu - 1) * (T - P - E - M) := mul_nonneg (by linarith) (by linarith)
    have k2 : (0 : ℝ) ≤ (nu - 1) * (T - B + P) := mul_nonneg (by linarith) (by linarith)
    have k3 : nu * M ≤ nu * T := by nlinarith [k1, k2, hu2]
    exact le_of_mul_le_mul_left k3 hnu0
  have hME : M ≤ T - E := by linarith
  have hEB : E ≤ B := le_trans hEA hAB
  -- the three components of `x`
  have hxlow : (nu - 1) * E - (nu - 2) * A ≤ reconX nu T A E M :=
    (le_max_left _ _).trans (le_max_right _ _)
  have hxAM : A - T + M ≤ reconX nu T A E M :=
    (le_max_right _ _).trans (le_max_right _ _)
  have hx0 : (0 : ℝ) ≤ reconX nu T A E M := le_max_left _ _
  have hxA : reconX nu T A E M ≤ A := by
    refine max_le hA0 (max_le ?_ (by linarith))
    linarith [mul_le_mul_of_nonneg_left hEA hnu1.le]
  have hxM : reconX nu T A E M ≤ M := max_le hM0 (max_le hl4 (by linarith))
  have hxBE : reconX nu T A E M ≤ B - E :=
    max_le (by linarith) (max_le (by nlinarith [hE2]) (by linarith))
  -- the two components of `y`
  have hyx : reconX nu T A E M ≤ reconY nu T A B E M := le_max_left _ _
  have hyBM : B - T + M ≤ reconY nu T A B E M := le_max_right _ _
  have hyM : reconY nu T A B E M ≤ M := max_le hxM (by linarith)
  have hyBE : reconY nu T A B E M ≤ B - E := max_le hxBE (by linarith)
  have hyBA : reconY nu T A B E M ≤ B - A + reconX nu T A E M :=
    max_le (by linarith) (by linarith)
  refine ⟨hx0, hyx, hyM, by linarith, by linarith, by linarith, hxlow, hyBE,
    by linarith, by linarith, ?_, ?_, hl1⟩
  · rw [← sub_le_iff_le_add', le_div_iff₀ hnu1]
    nlinarith [hu2]
  · rw [← le_sub_iff_add_le', div_le_iff₀ hnu1]
    nlinarith [hl3]

/-- **SC19, state existence.** Cumulative states `(x, y, M)` satisfying the monotonicity,
failure and cutoff constraints and `T/nu ≤ M` exist **iff** `E ≤ A`, `nu*E ≤ (nu-2)*A + B`
and the `M`-interval of `eq:grid-M-interval` is nonempty.

Both directions are proved. The forward ("only if") direction is the displayed monotonicity
and cutoff computation and uses only `3 ≤ nu`. The backward ("if") direction is the explicit
reconstruction `stateOK_recon` and additionally uses `0 ≤ P`, `P ≤ A`, `A ≤ B` and `B ≤ T`,
all non-strict. -/
theorem exists_state_iff (hnu : 3 ≤ nu) (hP : 0 ≤ P) (hPA : P ≤ A) (hAB : A ≤ B)
    (hBT : B ≤ T) (Q E : ℝ) :
    (∃ x y M : ℝ, StateOK nu T A B P Q E x y M) ↔
      E ≤ A ∧ nu * E ≤ (nu - 2) * A + B ∧ MNonempty nu T A B P Q E := by
  have hnu0 : (0 : ℝ) < nu := by linarith
  have hnu1 : (0 : ℝ) < nu - 1 := by linarith
  constructor
  · rintro ⟨x, y, M, hx0, hxy, hyM, hAx, hAxBy, hByTM, hfail1, hfail2,
      hcut1, hcut2, hcut3, hcut4, hmass⟩
    rw [← sub_le_iff_le_add', le_div_iff₀ hnu1] at hcut3
    rw [← le_sub_iff_add_le', div_le_iff₀ hnu1] at hcut4
    refine ⟨?_, by linarith, ?_⟩
    · have key : (nu - 1) * E ≤ (nu - 1) * A := by nlinarith [hfail1, hAx]
      exact le_of_mul_le_mul_left key hnu1
    · refine ⟨M, ?_, ?_⟩
      · simp only [MLower, max_le_iff]
        exact ⟨hmass, by linarith, by nlinarith [hcut4], by linarith⟩
      · simp only [MUpper, le_min_iff]
        exact ⟨by linarith, by nlinarith [hcut3]⟩
  · rintro ⟨hEA, hE2, M, hlow, hupp⟩
    exact ⟨_, _, M, stateOK_recon hnu hP hPA hAB hBT hEA hE2 hlow hupp⟩

/-- The boundary case `a = b` (`A = B` and `P = Q`) of `exists_state_iff`. -/
theorem exists_state_iff_same_cell (hnu : 3 ≤ nu) (hP : 0 ≤ P) (hPA : P ≤ A) (hAT : A ≤ T)
    (E : ℝ) :
    (∃ x y M : ℝ, StateOK nu T A A P P E x y M) ↔
      E ≤ A ∧ nu * E ≤ (nu - 2) * A + A ∧ MNonempty nu T A A P P E :=
  exists_state_iff hnu hP hPA le_rfl hAT P E

/-- The boundary case `b = N` (`B = T`) of `exists_state_iff`. -/
theorem exists_state_iff_last_cell (hnu : 3 ≤ nu) (hP : 0 ≤ P) (hPA : P ≤ A) (hAT : A ≤ T)
    (Q E : ℝ) :
    (∃ x y M : ℝ, StateOK nu T A T P Q E x y M) ↔
      E ≤ A ∧ nu * E ≤ (nu - 2) * A + T ∧ MNonempty nu T A T P Q E :=
  exists_state_iff hnu hP hPA hAT le_rfl Q E

end GridSwitching
