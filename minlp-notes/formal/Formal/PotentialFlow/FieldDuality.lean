import Mathlib

/-!
# Solvability of finite linear systems over a field

Two field-level facts used by the constrained-Laplacian development.

* `exists_vecMul_iff` is the fundamental-subspace identity in matrix form: the
  row system `p ᵥ* M = c` is solvable exactly when `c` annihilates the kernel of
  `d ↦ M *ᵥ d`.
* `exists_stationary_pair` applies it to the block system of the constrained
  Laplacian.  Over any linearly ordered field, for an arbitrary incidence
  function `inc` and nonnegative curvatures `h`, the stationarity system is
  solvable as soon as the goal annihilates every conserved vector supported on
  the zero-curvature indices.  The ordering is used only to turn a vanishing
  sum of squares into a vanishing vector.

Both statements are field generic, so the constrained-Laplacian results can be
instantiated over `ℝ` and over `ℚ` without a separate descent argument.
-/

namespace PotentialFlow

open Matrix

section FredholmAlternative

variable {K : Type*} [Field K] {ι κ : Type*} [Fintype ι] [Fintype κ]

/-- Fundamental-subspace identity: the row system `p ᵥ* M = c` is solvable
exactly when `c` is orthogonal to the kernel of `d ↦ M *ᵥ d`. -/
theorem exists_vecMul_iff (M : Matrix ι κ K) (c : κ → K) :
    (∃ p : ι → K, p ᵥ* M = c) ↔ ∀ z : κ → K, M *ᵥ z = 0 → ∑ j, c j * z j = 0 := by
  classical
  constructor
  · rintro ⟨p, rfl⟩ z hz
    have hpair : p ⬝ᵥ (M *ᵥ z) = (p ᵥ* M) ⬝ᵥ z := Matrix.dotProduct_mulVec p M z
    rw [hz] at hpair
    simpa [dotProduct] using hpair.symm
  · intro hker
    have hL : (dotProductEquiv K κ c) ∈ (M.mulVecLin).ker.dualAnnihilator := by
      rw [Submodule.mem_dualAnnihilator]
      intro z hz
      exact hker z (by simpa using hz)
    rw [← LinearMap.range_dualMap_eq_dualAnnihilator_ker] at hL
    obtain ⟨f, hf⟩ := hL
    obtain ⟨p, rfl⟩ : ∃ p, dotProductEquiv K ι p = f :=
      ⟨(dotProductEquiv K ι).symm f, (dotProductEquiv K ι).apply_symm_apply f⟩
    refine ⟨p, (dotProductEquiv K κ).injective ?_⟩
    rw [← hf]
    refine LinearMap.ext fun z => ?_
    change (p ᵥ* M) ⬝ᵥ z = p ⬝ᵥ (M *ᵥ z)
    exact (Matrix.dotProduct_mulVec p M z).symm

end FredholmAlternative

section Blocks

variable {K : Type*} [Field K] [LinearOrder K]
variable {ν ε : Type*} [Fintype ν] [Fintype ε] [DecidableEq ε]

/-- Block matrix of the constrained-Laplacian stationarity system, in the row
convention `p ᵥ* M = c`.  Unknowns are indexed by `ν ⊕ ε` (potentials, then
circulation), equations by `ε ⊕ ν` (one per index, then conservation). -/
def kktMatrix (inc : ν → ε → K) (h : ε → K) : Matrix (ν ⊕ ε) (ε ⊕ ν) K :=
  Matrix.of (Sum.elim
    (fun v => Sum.elim (fun e => inc v e) (fun _ => 0))
    (fun e => Sum.elim (fun e' => if e = e' then (if h e = 0 then 0 else h e) else 0)
      (fun x => inc x e)))

variable (inc : ν → ε → K) (h : ε → K)

/-- Row of `kktMatrix` pairing: the equation indexed by an element of `ε`. -/
theorem kktMatrix_vecMul_inl (p : ν ⊕ ε → K) (e : ε) :
    (p ᵥ* kktMatrix inc h) (Sum.inl e) =
      (if h e = 0 then 0 else h e * p (Sum.inr e)) + ∑ v, p (Sum.inl v) * inc v e := by
  rw [Matrix.vecMul, dotProduct, Fintype.sum_sum_type]
  have hleft : ∑ v, p (Sum.inl v) * kktMatrix inc h (Sum.inl v) (Sum.inl e) =
      ∑ v, p (Sum.inl v) * inc v e := rfl
  have hright : ∑ e', p (Sum.inr e') * kktMatrix inc h (Sum.inr e') (Sum.inl e) =
      if h e = 0 then 0 else h e * p (Sum.inr e) := by
    rw [Finset.sum_eq_single e]
    · change p (Sum.inr e) * (if e = e then (if h e = 0 then 0 else h e) else 0) = _
      rw [if_pos rfl]
      by_cases hc : h e = 0 <;> simp [hc, mul_comm]
    · intro e' _ hne
      change p (Sum.inr e') * (if e' = e then (if h e' = 0 then 0 else h e') else 0) = 0
      rw [if_neg hne, mul_zero]
    · intro hmem
      exact absurd (Finset.mem_univ e) hmem
  rw [hleft, hright, add_comm]

/-- Row of `kktMatrix` pairing: the conservation equation indexed by `ν`. -/
theorem kktMatrix_vecMul_inr (p : ν ⊕ ε → K) (x : ν) :
    (p ᵥ* kktMatrix inc h) (Sum.inr x) = ∑ e, inc x e * p (Sum.inr e) := by
  rw [Matrix.vecMul, dotProduct, Fintype.sum_sum_type]
  simp only [kktMatrix, Matrix.of_apply, Sum.elim_inl, Sum.elim_inr, mul_zero,
    Finset.sum_const_zero, zero_add]
  exact Finset.sum_congr rfl fun e _ => mul_comm _ _

/-- Column of `kktMatrix` pairing: the unknown indexed by a potential. -/
theorem kktMatrix_mulVec_inl (z : ε ⊕ ν → K) (v : ν) :
    (kktMatrix inc h *ᵥ z) (Sum.inl v) = ∑ e, inc v e * z (Sum.inl e) := by
  rw [Matrix.mulVec, dotProduct, Fintype.sum_sum_type]
  simp [kktMatrix]

/-- Column of `kktMatrix` pairing: the unknown indexed by a circulation entry. -/
theorem kktMatrix_mulVec_inr (z : ε ⊕ ν → K) (e : ε) :
    (kktMatrix inc h *ᵥ z) (Sum.inr e) =
      (if h e = 0 then 0 else h e) * z (Sum.inl e) + ∑ x, inc x e * z (Sum.inr x) := by
  rw [Matrix.mulVec, dotProduct, Fintype.sum_sum_type]
  have hleft : ∑ e', kktMatrix inc h (Sum.inr e) (Sum.inl e') * z (Sum.inl e') =
      (if h e = 0 then 0 else h e) * z (Sum.inl e) := by
    rw [Finset.sum_eq_single e]
    · change (if e = e then (if h e = 0 then 0 else h e) else 0) * z (Sum.inl e) = _
      rw [if_pos rfl]
    · intro e' _ hne
      change (if e = e' then (if h e = 0 then 0 else h e) else 0) * z (Sum.inl e') = 0
      rw [if_neg (Ne.symm hne), zero_mul]
    · intro hmem
      exact absurd (Finset.mem_univ e) hmem
  have hright : ∑ x, kktMatrix inc h (Sum.inr e) (Sum.inr x) * z (Sum.inr x) =
      ∑ x, inc x e * z (Sum.inr x) := rfl
  rw [hleft, hright]

end Blocks

section Stationarity

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]
variable {ν ε : Type*} [Fintype ν] [Fintype ε]

/-- Solvability of the constrained-Laplacian stationarity system.  If the goal
`w` annihilates every conserved vector supported on the zero-curvature indices,
then there are a potential `p` and a conserved `d` with
`h e * d e + (transposed incidence applied to p) e = w e` on the
positive-curvature indices, and `(transposed incidence applied to p) e = w e`
on the zero-curvature ones. -/
theorem exists_stationary_pair (inc : ν → ε → K) (h w : ε → K) (hh : ∀ e, 0 ≤ h e)
    (hker : ∀ z : ε → K, (∀ e, h e ≠ 0 → z e = 0) →
      (∀ v, ∑ e, inc v e * z e = 0) → ∑ e, w e * z e = 0) :
    ∃ (p : ν → K) (d : ε → K),
      (∀ v, ∑ e, inc v e * d e = 0) ∧
      (∀ e, (if h e = 0 then 0 else h e * d e) + ∑ v, p v * inc v e = w e) := by
  classical
  have hsolve : ∃ q : ν ⊕ ε → K, q ᵥ* kktMatrix inc h = Sum.elim w 0 := by
    rw [exists_vecMul_iff]
    intro z hz
    set zz : ε → K := fun e => z (Sum.inl e) with hzz
    set y : ν → K := fun x => z (Sum.inr x) with hy
    have hcons : ∀ v, ∑ e, inc v e * zz e = 0 := by
      intro v
      have hv := congrFun hz (Sum.inl v)
      rwa [kktMatrix_mulVec_inl] at hv
    have hrow : ∀ e, (if h e = 0 then 0 else h e) * zz e + ∑ x, inc x e * y x = 0 := by
      intro e
      have he := congrFun hz (Sum.inr e)
      rwa [kktMatrix_mulVec_inr] at he
    have hcross : ∑ e, (∑ x, inc x e * y x) * zz e = 0 := by
      have hswap : ∑ e, (∑ x, inc x e * y x) * zz e = ∑ x, y x * ∑ e, inc x e * zz e :=
        calc ∑ e, (∑ x, inc x e * y x) * zz e
            = ∑ e, ∑ x, inc x e * y x * zz e :=
              Finset.sum_congr rfl fun e _ => Finset.sum_mul _ _ _
          _ = ∑ x, ∑ e, inc x e * y x * zz e := Finset.sum_comm
          _ = ∑ x, y x * ∑ e, inc x e * zz e := by
              refine Finset.sum_congr rfl fun x _ => ?_
              rw [Finset.mul_sum]
              exact Finset.sum_congr rfl fun e _ => by ring
      rw [hswap]
      simp [hcons]
    have hsq : ∑ e, (if h e = 0 then 0 else h e) * zz e ^ 2 = 0 := by
      have hterm : ∀ e ∈ (Finset.univ : Finset ε),
          (if h e = 0 then 0 else h e) * zz e ^ 2 = -((∑ x, inc x e * y x) * zz e) := by
        intro e _
        have hval : ∑ x, inc x e * y x = -((if h e = 0 then 0 else h e) * zz e) := by
          have := hrow e
          linarith
        rw [hval]
        ring
      rw [Finset.sum_congr rfl hterm, Finset.sum_neg_distrib, hcross, neg_zero]
    have hzero : ∀ e, h e ≠ 0 → zz e = 0 := by
      intro e he
      have hnn : ∀ e' ∈ (Finset.univ : Finset ε),
          0 ≤ (if h e' = 0 then 0 else h e') * zz e' ^ 2 := by
        intro e' _
        split
        · simp
        · exact mul_nonneg (hh e') (sq_nonneg _)
      have hterm := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp hsq e (Finset.mem_univ e)
      rw [if_neg he] at hterm
      rcases mul_eq_zero.mp hterm with hcase | hcase
      · exact absurd hcase he
      · exact sq_eq_zero_iff.mp hcase
    have hgoal := hker zz hzero hcons
    rw [Fintype.sum_sum_type]
    simpa [hzz] using hgoal
  obtain ⟨q, hq⟩ := hsolve
  refine ⟨fun v => q (Sum.inl v), fun e => q (Sum.inr e), ?_, ?_⟩
  · intro v
    have hv := congrFun hq (Sum.inr v)
    rwa [kktMatrix_vecMul_inr] at hv
  · intro e
    have he := congrFun hq (Sum.inl e)
    rwa [kktMatrix_vecMul_inl] at he

end Stationarity

end PotentialFlow
