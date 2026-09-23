import Formal.PotentialFlow.FieldDuality
import Formal.PotentialFlow.RationalBridge

/-!
# Curvature bounds and the constrained Laplacian

Fix a network `G`, a linear goal `w` and edge curvatures `h` with `0 ≤ h e`.
Write `P = {e | h e ≠ 0}` for the positive-curvature edges and
`Z = {e | h e = 0}` for the zero-curvature ones.  A potential `v` is
*zero-admissible* when the prescribed drops match the goal on `Z`, and its
*factor* is the curvature-weighted energy of the residual `w - Aᵀ v` on `P`.

This file proves, for arbitrary finite directed networks (self-loops, parallel
edges, disconnected graphs and redundant conservation rows all allowed):

* `Network.exists_zeroAdmissible_iff`: solvability of the zero-edge condition
  is equivalent to the goal annihilating every conserved vector supported on
  `Z` (no hypothesis on `h`);
* `Network.exists_unbounded_of_not_zeroGoalCompatible`: when that fails, the
  goal is unbounded on the quadratic error set for every positive `δ`;
* `Network.exists_optimalFactor`: the minimal factor is attained;
* `Network.optimalFactor_iff_exists_kktCirculation`: a matrix-free first-order
  characterization of the minimizers, with `Network.schurKkt_iff` and
  `Network.optimalFactor_iff_exists_schurKkt` identifying it with the source's
  Schur-complement system `eq:a-cert-kkt`;
* `Network.isLeast_factor` and `Network.exists_isLeast_factor`: the optimal
  factor `C_*` is the least element of the set of admissible factors;
* `RationalNetwork.exists_rational_optimalFactor`: with rational data a
  rational minimizer exists;
* `Network.isGreatest_goalError`: `√(2 δ C_*)` is the exact, attained maximum
  of `|wᵀ d|` on the quadratic error set.

All existence statements come from `PotentialFlow.exists_stationary_pair`, so
no completeness or compactness argument is used; the rational case is the same
theorem over `ℚ`.
-/

namespace PotentialFlow

/-- The curvature-weighted factor of a residual vector: `∑_{e ∈ P} s e ^ 2 / h e`,
with the zero-curvature edges contributing nothing. -/
noncomputable def curvatureFactor {m : ℕ} (h s : Fin m → ℝ) : ℝ :=
  ∑ e, if h e = 0 then 0 else s e ^ 2 / h e

theorem curvatureFactor_nonneg {m : ℕ} {h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e)
    (s : Fin m → ℝ) : 0 ≤ curvatureFactor h s := by
  refine Finset.sum_nonneg fun e _ => ?_
  split
  · exact le_rfl
  · exact div_nonneg (sq_nonneg _) (hh e)

namespace Network

variable {n m : ℕ} (G : Network n m)

/-- The residual `w - Aᵀ v` of the goal against a potential vector. -/
def goalResidual (w : Fin m → ℝ) (v : Fin n → ℝ) : Fin m → ℝ := fun e => w e - G.drops v e

/-- A potential vector is zero-admissible when its drops match the goal on every
zero-curvature edge; this is the condition `A_Zᵀ v = w_Z`. -/
def ZeroAdmissible (w h : Fin m → ℝ) (v : Fin n → ℝ) : Prop :=
  ∀ e, h e = 0 → G.drops v e = w e

/-- The optimized Laplacian factor `C(v)` of a potential vector. -/
noncomputable def factor (w h : Fin m → ℝ) (v : Fin n → ℝ) : ℝ :=
  curvatureFactor h (G.goalResidual w v)

/-- A conserved circulation realizing the first-order optimality condition at `v`. -/
def KktCirculation (w h : Fin m → ℝ) (v : Fin n → ℝ) (d : Fin m → ℝ) : Prop :=
  G.loads d = 0 ∧ ∀ e, h e ≠ 0 → h e * d e = G.goalResidual w v e

/-- A potential vector minimizes the factor among all zero-admissible ones. -/
def OptimalFactor (w h : Fin m → ℝ) (v : Fin n → ℝ) : Prop :=
  ∀ v', G.ZeroAdmissible w h v' → G.factor w h v ≤ G.factor w h v'

/-- The goal annihilates every conserved vector supported on the zero-curvature
edges; this is the obstruction condition `w_Zᵀ z = 0` for `z ∈ ker A_Z`. -/
def ZeroGoalCompatible (w h : Fin m → ℝ) : Prop :=
  ∀ d : Fin m → ℝ, (∀ e, h e ≠ 0 → d e = 0) → G.loads d = 0 → ∑ e, w e * d e = 0

theorem factor_nonneg {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e) (v : Fin n → ℝ) :
    0 ≤ G.factor w h v := curvatureFactor_nonneg hh _

/-- Conservation rewritten through the incidence entries. -/
theorem loads_eq_zero_iff (d : Fin m → ℝ) :
    G.loads d = 0 ↔ ∀ v, ∑ e, G.incidence v e * d e = 0 := by
  constructor
  · intro hd v
    have := congrFun hd v
    rwa [G.loads_apply] at this
  · intro hd
    funext v
    rw [G.loads_apply]
    exact hd v

/-! ### CC25: solvability of the zero-edge condition -/

/-- A zero-admissible potential forces the goal to annihilate conserved vectors
supported on the zero-curvature edges. -/
theorem zeroGoalCompatible_of_zeroAdmissible {w h : Fin m → ℝ} {v : Fin n → ℝ}
    (hv : G.ZeroAdmissible w h v) : G.ZeroGoalCompatible w h := by
  intro d hsupp hd
  have hterm : ∀ e ∈ (Finset.univ : Finset (Fin m)), w e * d e = G.drops v e * d e := by
    intro e _
    by_cases he : h e = 0
    · rw [hv e he]
    · rw [hsupp e he, mul_zero, mul_zero]
  rw [Finset.sum_congr rfl hterm]
  exact G.potential_stationary v d hd

/-- Reading a stationarity solution as a zero-admissible potential together with
its optimality circulation. -/
theorem zeroAdmissible_and_kkt_of_stationary {w h : Fin m → ℝ} {p : Fin n → ℝ}
    {d : Fin m → ℝ} (hd : ∀ x, ∑ e, G.incidence x e * d e = 0)
    (heq : ∀ e, (if h e = 0 then 0 else h e * d e) + ∑ x, p x * G.incidence x e = w e) :
    G.ZeroAdmissible w h p ∧ G.KktCirculation w h p d := by
  have hload : G.loads d = 0 := (G.loads_eq_zero_iff d).mpr hd
  have hrow : ∀ e, (if h e = 0 then 0 else h e * d e) + G.drops p e = w e := by
    intro e
    rw [← G.incidence_transpose p e]
    exact heq e
  refine ⟨fun e he => ?_, hload, fun e he => ?_⟩
  · have := hrow e
    rw [if_pos he, zero_add] at this
    exact this
  · have := hrow e
    rw [if_neg he] at this
    simp only [goalResidual]
    linarith

/-- Existence of a zero-admissible potential together with its optimality
circulation, under the zero-curvature compatibility condition. -/
theorem exists_kktCirculation_of_compatible {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e)
    (hc : G.ZeroGoalCompatible w h) :
    ∃ (v : Fin n → ℝ) (d : Fin m → ℝ),
      G.ZeroAdmissible w h v ∧ G.KktCirculation w h v d := by
  obtain ⟨p, d, hd, heq⟩ :=
    exists_stationary_pair (K := ℝ) (ν := Fin n) (ε := Fin m) G.incidence h w hh
      (fun z hsupp hcons => hc z hsupp ((G.loads_eq_zero_iff z).mpr hcons))
  exact ⟨p, d, G.zeroAdmissible_and_kkt_of_stationary hd heq⟩

/-- **CC25.**  The zero-edge condition `A_Zᵀ v = w_Z` is solvable exactly when the
goal annihilates every conserved vector supported on the zero-curvature edges.

This is a pure Fredholm criterion for the zero-curvature columns of the incidence
matrix; nothing is assumed about `h` beyond the edges it declares to be of zero
curvature. -/
theorem exists_zeroAdmissible_iff {w h : Fin m → ℝ} :
    (∃ v, G.ZeroAdmissible w h v) ↔ G.ZeroGoalCompatible w h := by
  classical
  refine ⟨fun ⟨v, hv⟩ => G.zeroGoalCompatible_of_zeroAdmissible hv, fun hc => ?_⟩
  set M : Matrix (Fin n) (Fin m) ℝ :=
    Matrix.of (fun x e => if h e = 0 then G.incidence x e else 0) with hM
  have hvecMul : ∀ (p : Fin n → ℝ) (e : Fin m),
      Matrix.vecMul p M e = ∑ x, p x * (if h e = 0 then G.incidence x e else 0) :=
    fun _ _ => rfl
  have hmulVec : ∀ (z : Fin m → ℝ) (x : Fin n),
      Matrix.mulVec M z x = ∑ e, (if h e = 0 then G.incidence x e else 0) * z e :=
    fun _ _ => rfl
  have hsolve : ∃ p : Fin n → ℝ, Matrix.vecMul p M = fun e => if h e = 0 then w e else 0 := by
    rw [exists_vecMul_iff]
    intro z hz
    have hsupp : ∀ e, h e ≠ 0 → (if h e = 0 then z e else 0) = 0 := by
      intro e he
      rw [if_neg he]
    have hload : G.loads (fun e => if h e = 0 then z e else 0) = 0 := by
      refine (G.loads_eq_zero_iff _).mpr fun y => ?_
      have hy : ∑ e, (if h e = 0 then G.incidence y e else 0) * z e = 0 := by
        have hzy := congrFun hz y
        rwa [hmulVec] at hzy
      refine Eq.trans ?_ hy
      refine Finset.sum_congr rfl fun e _ => ?_
      by_cases he : h e = 0
      · rw [if_pos he, if_pos he]
      · rw [if_neg he, if_neg he, mul_zero, zero_mul]
    have hgoal := hc _ hsupp hload
    refine Eq.trans ?_ hgoal
    refine Finset.sum_congr rfl fun e _ => ?_
    by_cases he : h e = 0
    · rw [if_pos he, if_pos he]
    · rw [if_neg he, if_neg he, mul_zero, zero_mul]
  obtain ⟨p, hp⟩ := hsolve
  refine ⟨p, fun e he => ?_⟩
  have hpe := congrFun hp e
  rw [hvecMul] at hpe
  simp only [if_pos he] at hpe
  rw [← G.incidence_transpose p e]
  exact hpe

/-! ### CC26: the zero-curvature obstruction makes the goal unbounded -/

/-- **CC26.**  If the zero-curvature compatibility condition fails, then for every
`δ > 0` and every bound `M` the quadratic error set contains a circulation whose
goal exceeds `M` in absolute value. -/
theorem exists_unbounded_of_not_zeroGoalCompatible {w h : Fin m → ℝ}
    (hc : ¬ G.ZeroGoalCompatible w h) {δ : ℝ} (hδ : 0 < δ) (M : ℝ) :
    ∃ d : Fin m → ℝ, G.loads d = 0 ∧ (1 / 2) * ∑ e, h e * d e ^ 2 ≤ δ ∧
      M < |∑ e, w e * d e| := by
  rw [ZeroGoalCompatible] at hc
  push Not at hc
  obtain ⟨z, hsupp, hload, hgoal⟩ := hc
  set a : ℝ := ∑ e, w e * z e with ha
  have hane : a ≠ 0 := hgoal
  set t : ℝ := (|M| + 1) / |a| with ht
  have htpos : 0 < t := by
    have : 0 < |a| := abs_pos.mpr hane
    positivity
  refine ⟨fun e => t * z e, ?_, ?_, ?_⟩
  · have : (fun e => t * z e) = t • z := by
      funext e
      simp [Pi.smul_apply]
    rw [this]
    change G.divergenceLinear (t • z) = 0
    rw [map_smul]
    change t • G.loads z = 0
    rw [hload, smul_zero]
  · have hzero : ∀ e ∈ (Finset.univ : Finset (Fin m)), h e * (t * z e) ^ 2 = 0 := by
      intro e _
      by_cases he : h e = 0
      · rw [he, zero_mul]
      · rw [hsupp e he]
        ring
    rw [Finset.sum_congr rfl hzero, Finset.sum_const_zero, mul_zero]
    exact hδ.le
  · have hsum : ∑ e, w e * (t * z e) = t * a := by
      rw [ha, Finset.mul_sum]
      exact Finset.sum_congr rfl fun e _ => by ring
    have hval : t * |a| = |M| + 1 := by
      rw [ht]
      field_simp
    rw [hsum, abs_mul, abs_of_pos htpos, hval]
    linarith [le_abs_self M]

/-! ### The exact expansion of the factor around a stationary point -/

/-- Exact second-order expansion: from a potential carrying an optimality
circulation, the factor of any other zero-admissible potential exceeds it by the
curvature-weighted energy of the difference of drops. -/
theorem factor_eq_add_of_kktCirculation {w h : Fin m → ℝ} {v v' : Fin n → ℝ}
    {d : Fin m → ℝ} (hv : G.ZeroAdmissible w h v) (hv' : G.ZeroAdmissible w h v')
    (hk : G.KktCirculation w h v d) :
    G.factor w h v' =
      G.factor w h v + ∑ e, if h e = 0 then 0 else (G.drops v' e - G.drops v e) ^ 2 / h e := by
  obtain ⟨hload, hkk⟩ := hk
  have hcross : ∑ e, (G.drops v' e - G.drops v e) * d e = 0 := by
    simp only [sub_mul]
    rw [Finset.sum_sub_distrib, G.potential_stationary v' d hload,
      G.potential_stationary v d hload, sub_zero]
  have key : ∀ e ∈ (Finset.univ : Finset (Fin m)),
      (if h e = 0 then 0 else G.goalResidual w v' e ^ 2 / h e) =
        (if h e = 0 then 0 else G.goalResidual w v e ^ 2 / h e)
          - 2 * ((G.drops v' e - G.drops v e) * d e)
          + (if h e = 0 then 0 else (G.drops v' e - G.drops v e) ^ 2 / h e) := by
    intro e _
    by_cases he : h e = 0
    · have hz : G.drops v' e - G.drops v e = 0 := by rw [hv' e he, hv e he, sub_self]
      rw [if_pos he, if_pos he, if_pos he, hz]
      ring
    · have hs : G.goalResidual w v e = h e * d e := (hkk e he).symm
      have hs' : G.goalResidual w v' e = h e * d e - (G.drops v' e - G.drops v e) := by
        simp only [goalResidual] at hs ⊢
        linarith
      rw [if_neg he, if_neg he, if_neg he, hs, hs']
      field_simp
      ring
  simp only [factor, curvatureFactor]
  rw [Finset.sum_congr rfl key, Finset.sum_add_distrib, Finset.sum_sub_distrib,
    ← Finset.mul_sum, hcross]
  ring

/-! ### CC27 and CC28: attainment and the matrix-free stationarity system -/

/-- Sufficiency in the first-order characterization. -/
theorem optimalFactor_of_kktCirculation {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e)
    {v : Fin n → ℝ} {d : Fin m → ℝ} (hv : G.ZeroAdmissible w h v)
    (hk : G.KktCirculation w h v d) : G.OptimalFactor w h v := by
  intro v' hv'
  rw [G.factor_eq_add_of_kktCirculation hv hv' hk]
  have : 0 ≤ ∑ e, if h e = 0 then 0 else (G.drops v' e - G.drops v e) ^ 2 / h e := by
    refine Finset.sum_nonneg fun e _ => ?_
    split
    · exact le_rfl
    · exact div_nonneg (sq_nonneg _) (hh e)
  linarith

/-- **CC27.**  When some potential is zero-admissible, the minimum of the factor
over all zero-admissible potentials is attained. -/
theorem exists_optimalFactor {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e)
    {v₀ : Fin n → ℝ} (hv₀ : G.ZeroAdmissible w h v₀) :
    ∃ v, G.ZeroAdmissible w h v ∧ G.OptimalFactor w h v := by
  obtain ⟨v, d, hv, hk⟩ :=
    G.exists_kktCirculation_of_compatible hh (G.zeroGoalCompatible_of_zeroAdmissible hv₀)
  exact ⟨v, hv, G.optimalFactor_of_kktCirculation hh hv hk⟩

/-- **CC28.**  A zero-admissible potential minimizes the factor exactly when some
conserved circulation `d` satisfies `h e * d e = (w - Aᵀ v) e` on every
positive-curvature edge. -/
theorem optimalFactor_iff_exists_kktCirculation {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e)
    {v : Fin n → ℝ} (hv : G.ZeroAdmissible w h v) :
    G.OptimalFactor w h v ↔ ∃ d, G.KktCirculation w h v d := by
  constructor
  · intro hopt
    obtain ⟨p, d, hp, hk⟩ :=
      G.exists_kktCirculation_of_compatible hh (G.zeroGoalCompatible_of_zeroAdmissible hv)
    have hid := G.factor_eq_add_of_kktCirculation hp hv hk
    have hle : G.factor w h v ≤ G.factor w h p := hopt p hp
    set T : ℝ := ∑ e, if h e = 0 then 0 else (G.drops v e - G.drops p e) ^ 2 / h e with hT
    have hTnn : 0 ≤ T := by
      rw [hT]
      refine Finset.sum_nonneg fun e _ => ?_
      split
      · exact le_rfl
      · exact div_nonneg (sq_nonneg _) (hh e)
    have hTzero : T = 0 := by linarith
    have hdrops : ∀ e, G.drops v e = G.drops p e := by
      intro e
      by_cases he : h e = 0
      · rw [hv e he, hp e he]
      · have hnn : ∀ e' ∈ (Finset.univ : Finset (Fin m)),
            0 ≤ (if h e' = 0 then 0 else (G.drops v e' - G.drops p e') ^ 2 / h e') := by
          intro e' _
          split
          · exact le_rfl
          · exact div_nonneg (sq_nonneg _) (hh e')
        have hterm := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp hTzero e (Finset.mem_univ e)
        rw [if_neg he] at hterm
        rcases div_eq_zero_iff.mp hterm with hcase | hcase
        · exact sub_eq_zero.mp (sq_eq_zero_iff.mp hcase)
        · exact absurd hcase he
    refine ⟨d, hk.1, fun e he => ?_⟩
    rw [hk.2 e he]
    simp only [goalResidual]
    rw [hdrops e]
  · rintro ⟨d, hk⟩
    exact G.optimalFactor_of_kktCirculation hh hv hk

/-! ### The Schur-complement form `eq:a-cert-kkt` -/

/-- The source's stationarity system

```
[A_P D A_Pᵀ  A_Z] [v]   [A_P D w_P]
[A_Zᵀ         0 ] [ξ] = [   w_Z   ]
```

with `D = diag(1/h e : e ∈ P)`, written componentwise over the incidence entries.
The first conjunct is the top row, the second is the bottom row `A_Zᵀ v = w_Z`.
Only the zero-curvature entries of `ξ` occur, matching the fact that `A_Z` has
columns indexed by `Z`. -/
def SchurKkt (w h : Fin m → ℝ) (v : Fin n → ℝ) (ξ : Fin m → ℝ) : Prop :=
  (∀ x : Fin n,
      (∑ e, if h e = 0 then 0 else G.incidence x e * (G.drops v e / h e)) +
        (∑ e, if h e = 0 then G.incidence x e * ξ e else 0) =
      ∑ e, if h e = 0 then 0 else G.incidence x e * (w e / h e)) ∧
  G.ZeroAdmissible w h v

/-- The circulation attached to a solution of `eq:a-cert-kkt`:
`d_P = D (w_P - A_Pᵀ v)` and `d_Z = -ξ`. -/
noncomputable def schurCirculation (w h : Fin m → ℝ) (v : Fin n → ℝ) (ξ : Fin m → ℝ) :
    Fin m → ℝ :=
  fun e => if h e = 0 then -ξ e else (w e - G.drops v e) / h e

/-- **CC28, correspondence with `eq:a-cert-kkt`.**  A pair `(v, ξ)` solves the
Schur-complement system exactly when `v` is zero-admissible and the attached
circulation `d_P = D (w_P - A_Pᵀ v)`, `d_Z = -ξ` is an optimality circulation at
`v`.  No hypothesis on `h` is needed, so `P = ∅`, `Z = ∅`, singular potential
gauges and redundant zero-edge rows are all covered. -/
theorem schurKkt_iff (w h : Fin m → ℝ) (v : Fin n → ℝ) (ξ : Fin m → ℝ) :
    G.SchurKkt w h v ξ ↔
      G.ZeroAdmissible w h v ∧ G.KktCirculation w h v (G.schurCirculation w h v ξ) := by
  have hres : ∀ e, h e ≠ 0 →
      h e * G.schurCirculation w h v ξ e = G.goalResidual w v e := by
    intro e he
    simp only [schurCirculation, if_neg he, goalResidual]
    field_simp
  have hkey : ∀ x : Fin n,
      ((∑ e, if h e = 0 then 0 else G.incidence x e * (G.drops v e / h e)) +
          (∑ e, if h e = 0 then G.incidence x e * ξ e else 0)) -
        (∑ e, if h e = 0 then 0 else G.incidence x e * (w e / h e)) =
      -∑ e, G.incidence x e * G.schurCirculation w h v ξ e := by
    intro x
    have hterm : ∀ e ∈ (Finset.univ : Finset (Fin m)),
        ((if h e = 0 then 0 else G.incidence x e * (G.drops v e / h e)) +
            (if h e = 0 then G.incidence x e * ξ e else 0)) -
          (if h e = 0 then 0 else G.incidence x e * (w e / h e)) =
        -(G.incidence x e * G.schurCirculation w h v ξ e) := by
      intro e _
      by_cases he : h e = 0
      · simp only [schurCirculation, if_pos he]
        ring
      · simp only [schurCirculation, if_neg he]
        field_simp
        ring
    calc ((∑ e, if h e = 0 then 0 else G.incidence x e * (G.drops v e / h e)) +
            (∑ e, if h e = 0 then G.incidence x e * ξ e else 0)) -
          (∑ e, if h e = 0 then 0 else G.incidence x e * (w e / h e))
        = ∑ e, (((if h e = 0 then 0 else G.incidence x e * (G.drops v e / h e)) +
              (if h e = 0 then G.incidence x e * ξ e else 0)) -
            (if h e = 0 then 0 else G.incidence x e * (w e / h e))) := by
          rw [Finset.sum_sub_distrib, Finset.sum_add_distrib]
      _ = ∑ e, -(G.incidence x e * G.schurCirculation w h v ξ e) :=
          Finset.sum_congr rfl hterm
      _ = -∑ e, G.incidence x e * G.schurCirculation w h v ξ e :=
          Finset.sum_neg_distrib _
  constructor
  · rintro ⟨hrow, hadm⟩
    refine ⟨hadm, (G.loads_eq_zero_iff _).mpr fun x => ?_, hres⟩
    have hx := hkey x
    rw [hrow x, sub_self] at hx
    linarith
  · rintro ⟨hadm, hload, -⟩
    refine ⟨fun x => ?_, hadm⟩
    have hz := (G.loads_eq_zero_iff _).mp hload x
    have hx := hkey x
    rw [hz, neg_zero] at hx
    linarith

/-- Conversely, every optimality circulation supplies a multiplier for
`eq:a-cert-kkt`, namely `ξ = -d`. -/
theorem schurKkt_neg_of_kktCirculation {w h : Fin m → ℝ} {v : Fin n → ℝ} {d : Fin m → ℝ}
    (hv : G.ZeroAdmissible w h v) (hk : G.KktCirculation w h v d) :
    G.SchurKkt w h v (fun e => -d e) := by
  have hsc : G.schurCirculation w h v (fun e => -d e) = d := by
    funext e
    by_cases he : h e = 0
    · simp only [schurCirculation, if_pos he, neg_neg]
    · have hkk := hk.2 e he
      simp only [goalResidual] at hkk
      simp only [schurCirculation, if_neg he]
      field_simp
      linarith
  rw [G.schurKkt_iff, hsc]
  exact ⟨hv, hk⟩

/-- **CC28, Schur-complement form.**  A zero-admissible potential minimizes the
factor exactly when the source's system `eq:a-cert-kkt` admits a multiplier. -/
theorem optimalFactor_iff_exists_schurKkt {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e)
    {v : Fin n → ℝ} (hv : G.ZeroAdmissible w h v) :
    G.OptimalFactor w h v ↔ ∃ ξ, G.SchurKkt w h v ξ := by
  constructor
  · intro hopt
    obtain ⟨d, hk⟩ := (G.optimalFactor_iff_exists_kktCirculation hh hv).mp hopt
    exact ⟨fun e => -d e, G.schurKkt_neg_of_kktCirculation hv hk⟩
  · rintro ⟨ξ, hξ⟩
    obtain ⟨-, hk⟩ := (G.schurKkt_iff w h v ξ).mp hξ
    exact G.optimalFactor_of_kktCirculation hh hv hk

/-! ### The optimal factor as a least element -/

/-- The optimal factor is the least element of the set of admissible factors. -/
theorem isLeast_factor {w h : Fin m → ℝ} {v : Fin n → ℝ} (hv : G.ZeroAdmissible w h v)
    (hopt : G.OptimalFactor w h v) :
    IsLeast {r : ℝ | ∃ v', G.ZeroAdmissible w h v' ∧ r = G.factor w h v'}
      (G.factor w h v) := by
  refine ⟨⟨v, hv, rfl⟩, ?_⟩
  rintro r ⟨v', hv', rfl⟩
  exact hopt v' hv'

/-- **CC27 as an infimum.**  Under the zero-curvature compatibility condition the
set of admissible factors has a least element, the optimal factor `C_*`. -/
theorem exists_isLeast_factor {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e)
    (hc : G.ZeroGoalCompatible w h) :
    ∃ v, G.ZeroAdmissible w h v ∧
      IsLeast {r : ℝ | ∃ v', G.ZeroAdmissible w h v' ∧ r = G.factor w h v'}
        (G.factor w h v) := by
  obtain ⟨v, d, hv, hk⟩ := G.exists_kktCirculation_of_compatible hh hc
  exact ⟨v, hv, G.isLeast_factor hv (G.optimalFactor_of_kktCirculation hh hv hk)⟩

/-! ### CC30: sharpness of the optimized Laplacian radius -/

/-- The goal of a conserved circulation is the pairing with the residual. -/
theorem sum_goal_eq_sum_residual {w : Fin m → ℝ} (v : Fin n → ℝ) {d : Fin m → ℝ}
    (hd : G.loads d = 0) : ∑ e, w e * d e = ∑ e, G.goalResidual w v e * d e := by
  simp only [goalResidual, sub_mul]
  rw [Finset.sum_sub_distrib, G.potential_stationary v d hd, sub_zero]

/-- Weighted Cauchy-Schwarz: the squared goal of a conserved circulation is at
most the factor times its curvature energy. -/
theorem sq_sum_goal_le {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e) {v : Fin n → ℝ}
    (hv : G.ZeroAdmissible w h v) {d : Fin m → ℝ} (hd : G.loads d = 0) :
    (∑ e, w e * d e) ^ 2 ≤ G.factor w h v * ∑ e, h e * d e ^ 2 := by
  classical
  set f : Fin m → ℝ := fun e => if h e = 0 then 0 else G.goalResidual w v e / Real.sqrt (h e)
    with hf
  set g : Fin m → ℝ := fun e => Real.sqrt (h e) * d e with hg
  have hfg : ∀ e, f e * g e = G.goalResidual w v e * d e := by
    intro e
    by_cases he : h e = 0
    · have : G.goalResidual w v e = 0 := by
        simp only [goalResidual, hv e he, sub_self]
      rw [hf, hg]
      simp [he, this]
    · have hpos : 0 < h e := lt_of_le_of_ne (hh e) (Ne.symm he)
      have hs : Real.sqrt (h e) ≠ 0 := Real.sqrt_ne_zero'.mpr hpos
      rw [hf, hg]
      simp only [if_neg he]
      field_simp
  have hfsq : ∀ e, f e ^ 2 = if h e = 0 then 0 else G.goalResidual w v e ^ 2 / h e := by
    intro e
    by_cases he : h e = 0
    · simp [hf, he]
    · have : Real.sqrt (h e) ^ 2 = h e := Real.sq_sqrt (hh e)
      rw [hf]
      simp only [if_neg he, div_pow, this]
  have hgsq : ∀ e, g e ^ 2 = h e * d e ^ 2 := by
    intro e
    have : Real.sqrt (h e) ^ 2 = h e := Real.sq_sqrt (hh e)
    rw [hg]
    simp only [mul_pow, this]
  have hcs := Finset.sum_mul_sq_le_sq_mul_sq (Finset.univ : Finset (Fin m)) f g
  rw [Finset.sum_congr rfl (fun e _ => hfg e), Finset.sum_congr rfl (fun e _ => hfsq e),
    Finset.sum_congr rfl (fun e _ => hgsq e)] at hcs
  rw [G.sum_goal_eq_sum_residual v hd]
  exact hcs

/-- The optimality circulation carries the whole factor: its curvature energy and
its goal both equal `C(v)`. -/
theorem kktCirculation_energy {w h : Fin m → ℝ} {v : Fin n → ℝ} {d : Fin m → ℝ}
    (hv : G.ZeroAdmissible w h v) (hk : G.KktCirculation w h v d) :
    ∑ e, w e * d e = G.factor w h v ∧ ∑ e, h e * d e ^ 2 = G.factor w h v := by
  obtain ⟨hload, hkk⟩ := hk
  have hres : ∀ e, h e = 0 → G.goalResidual w v e = 0 := by
    intro e he
    simp only [goalResidual, hv e he, sub_self]
  have hfac : G.factor w h v = ∑ e, h e * d e ^ 2 := by
    simp only [factor, curvatureFactor]
    refine Finset.sum_congr rfl fun e _ => ?_
    by_cases he : h e = 0
    · rw [if_pos he, he, zero_mul]
    · rw [if_neg he, ← hkk e he]
      field_simp
  refine ⟨?_, hfac.symm⟩
  rw [G.sum_goal_eq_sum_residual v hload, hfac]
  refine Finset.sum_congr rfl fun e _ => ?_
  by_cases he : h e = 0
  · rw [hres e he, zero_mul, he, zero_mul]
  · rw [← hkk e he]
    ring

/-- A vanishing factor at a zero-admissible potential means the goal is a pure
cut goal: the prescribed drops reproduce `w` on every edge. -/
theorem drops_eq_goal_of_factor_eq_zero {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e)
    {v : Fin n → ℝ} (hv : G.ZeroAdmissible w h v) (hzero : G.factor w h v = 0) :
    G.drops v = w := by
  funext e
  by_cases he : h e = 0
  · exact hv e he
  · have hnn : ∀ e' ∈ (Finset.univ : Finset (Fin m)),
        0 ≤ (if h e' = 0 then 0 else G.goalResidual w v e' ^ 2 / h e') := by
      intro e' _
      split
      · exact le_rfl
      · exact div_nonneg (sq_nonneg _) (hh e')
    have hterm := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp hzero e (Finset.mem_univ e)
    rw [if_neg he] at hterm
    rcases div_eq_zero_iff.mp hterm with hcase | hcase
    · have : G.goalResidual w v e = 0 := sq_eq_zero_iff.mp hcase
      simp only [goalResidual] at this
      linarith
    · exact absurd hcase he

/-- With a vanishing factor every conserved circulation has zero goal. -/
theorem sum_goal_eq_zero_of_factor_eq_zero {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e)
    {v : Fin n → ℝ} (hv : G.ZeroAdmissible w h v) (hzero : G.factor w h v = 0)
    {d : Fin m → ℝ} (hd : G.loads d = 0) : ∑ e, w e * d e = 0 := by
  rw [← G.drops_eq_goal_of_factor_eq_zero hh hv hzero]
  exact G.potential_stationary v d hd

/-- **CC30.**  For every `δ > 0`, the greatest goal magnitude on the quadratic
error set is exactly `√(2 δ C_*)`. -/
theorem isGreatest_goalError {w h : Fin m → ℝ} (hh : ∀ e, 0 ≤ h e) {v : Fin n → ℝ}
    (hv : G.ZeroAdmissible w h v) (hopt : G.OptimalFactor w h v) {δ : ℝ} (hδ : 0 < δ) :
    IsGreatest {r : ℝ | ∃ d : Fin m → ℝ, G.loads d = 0 ∧
        (1 / 2) * ∑ e, h e * d e ^ 2 ≤ δ ∧ r = |∑ e, w e * d e|}
      (Real.sqrt (2 * δ * G.factor w h v)) := by
  have hCnn : 0 ≤ G.factor w h v := G.factor_nonneg hh v
  have hprod : 0 ≤ 2 * δ * G.factor w h v := by positivity
  constructor
  · rcases eq_or_lt_of_le hCnn with hzero | hpos
    · refine ⟨fun _ => 0, ?_, ?_, ?_⟩
      · change G.divergenceLinear (fun _ => (0 : ℝ)) = 0
        exact map_zero G.divergenceLinear
      · simpa using hδ.le
      · rw [← hzero]
        simp
    · obtain ⟨d, hk⟩ := (G.optimalFactor_iff_exists_kktCirculation hh hv).mp hopt
      obtain ⟨hgoal, henergy⟩ := G.kktCirculation_energy hv hk
      have htnn : 0 ≤ Real.sqrt (2 * δ / G.factor w h v) := Real.sqrt_nonneg _
      have htsq : Real.sqrt (2 * δ / G.factor w h v) ^ 2 = 2 * δ / G.factor w h v :=
        Real.sq_sqrt (by positivity)
      refine ⟨fun e => Real.sqrt (2 * δ / G.factor w h v) * d e, ?_, ?_, ?_⟩
      · have hsm : (fun e => Real.sqrt (2 * δ / G.factor w h v) * d e)
            = Real.sqrt (2 * δ / G.factor w h v) • d := by
          funext e
          simp [Pi.smul_apply]
        rw [hsm]
        change G.divergenceLinear (Real.sqrt (2 * δ / G.factor w h v) • d) = 0
        rw [map_smul]
        change Real.sqrt (2 * δ / G.factor w h v) • G.loads d = 0
        rw [hk.1, smul_zero]
      · have hsum : ∑ e, h e * (Real.sqrt (2 * δ / G.factor w h v) * d e) ^ 2
            = Real.sqrt (2 * δ / G.factor w h v) ^ 2 * ∑ e, h e * d e ^ 2 := by
          rw [Finset.mul_sum]
          exact Finset.sum_congr rfl fun e _ => by ring
        rw [hsum, henergy, htsq, div_mul_cancel₀ _ hpos.ne']
        linarith
      · have hsum : ∑ e, w e * (Real.sqrt (2 * δ / G.factor w h v) * d e)
            = Real.sqrt (2 * δ / G.factor w h v) * G.factor w h v := by
          rw [← hgoal, Finset.mul_sum]
          exact Finset.sum_congr rfl fun e _ => by ring
        rw [hsum, abs_of_nonneg (by positivity)]
        have hsq : (Real.sqrt (2 * δ / G.factor w h v) * G.factor w h v) ^ 2
            = 2 * δ * G.factor w h v := by
          rw [mul_pow, htsq]
          field_simp
        rw [← hsq, Real.sqrt_sq (by positivity)]
  · rintro r ⟨d, hload, hen, rfl⟩
    have hcs := G.sq_sum_goal_le hh hv hload
    have hbound : (∑ e, w e * d e) ^ 2 ≤ 2 * δ * G.factor w h v := by
      have h2 : ∑ e, h e * d e ^ 2 ≤ 2 * δ := by linarith
      calc (∑ e, w e * d e) ^ 2 ≤ G.factor w h v * ∑ e, h e * d e ^ 2 := hcs
        _ ≤ G.factor w h v * (2 * δ) := mul_le_mul_of_nonneg_left h2 hCnn
        _ = 2 * δ * G.factor w h v := by ring
    have hle := Real.sqrt_le_sqrt hbound
    rwa [Real.sqrt_sq_eq_abs] at hle

end Network

namespace RationalNetwork

variable {n m : ℕ} (G : RationalNetwork n m)

/-- Signed incidence of the rational network, matching `Network.incidence` after
casting. -/
def incidence (v : Fin n) (e : Fin m) : ℚ :=
  (if G.tail e = v then 1 else 0) - (if G.head e = v then 1 else 0)

@[simp] theorem toReal_incidence (v : Fin n) (e : Fin m) :
    G.toReal.incidence v e = (G.incidence v e : ℝ) := by
  by_cases h1 : G.tail e = v <;> by_cases h2 : G.head e = v <;>
    simp [Network.incidence, incidence, toReal, h1, h2]

/-- **CC29.**  With rational network data, rational goal and rational
nonnegative curvatures, a real zero-admissible potential forces the existence of
a *rational* zero-admissible potential that minimizes the factor. -/
theorem exists_rational_optimalFactor (wQ hQ : Fin m → ℚ) (hh : ∀ e, 0 ≤ hQ e)
    {v : Fin n → ℝ}
    (hv : G.toReal.ZeroAdmissible (fun e => (wQ e : ℝ)) (fun e => (hQ e : ℝ)) v) :
    ∃ vQ : Fin n → ℚ,
      G.toReal.ZeroAdmissible (fun e => (wQ e : ℝ)) (fun e => (hQ e : ℝ))
        (fun x => (vQ x : ℝ)) ∧
      G.toReal.OptimalFactor (fun e => (wQ e : ℝ)) (fun e => (hQ e : ℝ))
        (fun x => (vQ x : ℝ)) := by
  have hhR : ∀ e, (0 : ℝ) ≤ (hQ e : ℝ) := fun e => by exact_mod_cast hh e
  have hcR := G.toReal.zeroGoalCompatible_of_zeroAdmissible hv
  have hcQ : ∀ z : Fin m → ℚ, (∀ e, hQ e ≠ 0 → z e = 0) →
      (∀ x, ∑ e, G.incidence x e * z e = 0) → ∑ e, wQ e * z e = 0 := by
    intro z hsupp hcons
    have hloadR : G.toReal.loads (fun e => (z e : ℝ)) = 0 := by
      refine (G.toReal.loads_eq_zero_iff _).mpr fun x => ?_
      have : ∑ e, (G.incidence x e : ℝ) * (z e : ℝ) = ((0 : ℚ) : ℝ) := by
        rw [← hcons x]
        push_cast
        rfl
      simpa using this
    have hsuppR : ∀ e, ((hQ e : ℝ)) ≠ 0 → ((z e : ℝ)) = 0 := by
      intro e he
      have : hQ e ≠ 0 := by exact_mod_cast he
      rw [hsupp e this]
      norm_num
    have hR := hcR (fun e => (z e : ℝ)) hsuppR hloadR
    have : ((∑ e, wQ e * z e : ℚ) : ℝ) = 0 := by push_cast; exact hR
    exact_mod_cast this
  obtain ⟨pQ, dQ, hdQ, heqQ⟩ :=
    exists_stationary_pair (K := ℚ) (ν := Fin n) (ε := Fin m) G.incidence hQ wQ hh hcQ
  refine ⟨pQ, ?_⟩
  have hdR : ∀ x, ∑ e, G.toReal.incidence x e * (dQ e : ℝ) = 0 := by
    intro x
    have : ∑ e, (G.incidence x e : ℝ) * ((dQ e : ℝ)) = ((0 : ℚ) : ℝ) := by
      rw [← hdQ x]
      push_cast
      rfl
    simpa using this
  have heqR : ∀ e, (if (hQ e : ℝ) = 0 then 0 else (hQ e : ℝ) * (dQ e : ℝ)) +
      ∑ x, ((pQ x : ℝ)) * G.toReal.incidence x e = (wQ e : ℝ) := by
    intro e
    have hif : (((if hQ e = 0 then 0 else hQ e * dQ e : ℚ)) : ℝ)
        = if (hQ e : ℝ) = 0 then 0 else (hQ e : ℝ) * (dQ e : ℝ) := by
      by_cases he : hQ e = 0
      · simp [he]
      · have hne : ((hQ e : ℝ)) ≠ 0 := by exact_mod_cast he
        simp [he, hne]
    have hsumcast : ((∑ x, pQ x * G.incidence x e : ℚ) : ℝ)
        = ∑ x, (pQ x : ℝ) * (G.incidence x e : ℝ) := by push_cast; rfl
    have hcast : (((if hQ e = 0 then 0 else hQ e * dQ e) +
        ∑ x, pQ x * G.incidence x e : ℚ) : ℝ) = ((wQ e : ℚ) : ℝ) := by rw [heqQ e]
    rw [Rat.cast_add, hif, hsumcast] at hcast
    simp only [G.toReal_incidence]
    exact hcast
  obtain ⟨hadm, hkkt⟩ := G.toReal.zeroAdmissible_and_kkt_of_stationary hdR heqR
  exact ⟨hadm, G.toReal.optimalFactor_of_kktCirculation hhR hadm hkkt⟩

end RationalNetwork

end PotentialFlow
