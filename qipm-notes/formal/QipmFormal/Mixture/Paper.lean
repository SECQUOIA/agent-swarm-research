import QipmFormal.Mixture.KKT
import QipmFormal.Mixture.Decoder
import QipmFormal.Mixture.Centrality
import QipmFormal.Mixture.Incidence

/-! # Central-mixture output contracts

These results connect the LP constraints to a sound output contract. The
contract includes positivity, the algebraic objective gap, the Euclidean
stacked residual, and the specified coordinatewise central neighborhood.
-/
namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators
variable {I R C : Type*} [Fintype I] [Fintype R] [Fintype C]

def tripleScore (ax as' : C → ℝ) (ay : R → ℝ) (a₀ : ℝ)
    (x : C → ℝ) (y : R → ℝ) (s : C → ℝ) : ℝ :=
  dot ax x + dot ay y + dot as' s - a₀

theorem tripleScore_mix (w : I → ℝ) (hw : ProbWeights w)
    (ax as' : C → ℝ) (ay : R → ℝ) (a₀ : ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) :
    tripleScore ax as' ay a₀ (mix w x) (mix w y) (mix w s) =
      ∑ i, w i * tripleScore ax as' ay a₀ (x i) (y i) (s i) := by
  unfold tripleScore
  simp only [dot_mix, mul_sub, mul_add, Finset.sum_sub_distrib,
    Finset.sum_add_distrib, ← Finset.sum_mul, hw.2, one_mul]

theorem tripleScore_wrong_mix (w : I → ℝ) (hw : ProbWeights w)
    (ax as' : C → ℝ) (ay : R → ℝ) (a₀ p γ : ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ)
    (hwrong : ∀ i, p * tripleScore ax as' ay a₀ (x i) (y i) (s i) ≤ -γ) :
    p * tripleScore ax as' ay a₀ (mix w x) (mix w y) (mix w s) ≤ -γ := by
  rw [tripleScore_mix w hw, Finset.mul_sum]
  calc
    _ ≤ ∑ i, w i * (-γ) := by
      apply Finset.sum_le_sum
      intro i _
      calc
        _ = w i * (p * tripleScore ax as' ay a₀ (x i) (y i) (s i)) := by ring
        _ ≤ _ := mul_le_mul_of_nonneg_left (hwrong i) (hw.1 i)
    _ = _ := by rw [← Finset.sum_mul, hw.2, one_mul]

omit [Fintype C] in
theorem mixture_pos (w : I → ℝ) (hw : ProbWeights w)
    (x : I → C → ℝ) (hx : ∀ i j, 0 < x i j) (j : C) : 0 < mix w x j := by
  have hex : ∃ i, 0 < w i := by
    by_contra h
    push Not at h
    have hz : ∑ i, w i ≤ 0 := Finset.sum_nonpos fun i _ => h i
    linarith [hw.2]
  obtain ⟨i, hi⟩ := hex
  unfold mix
  exact Finset.sum_pos' (fun k _ => mul_nonneg (hw.1 k) (hx k j).le)
    ⟨i, Finset.mem_univ i, mul_pos hi (hx i j)⟩

/-- The common-parameter contract, with an arbitrary named wrong-output predicate. -/
def CentralOutputSound (A : R → C → ℝ) (b : R → ℝ) (c : C → ℝ)
    (μ ε θ : ℝ) (Wrong : (C → ℝ) → (R → ℝ) → (C → ℝ) → Prop) : Prop :=
  ∀ x y s, (∀ j, 0 < x j) → (∀ j, 0 < s j) →
    dot c x - dot b y = (Fintype.card C : ℝ) * μ →
    Real.sqrt (kktSqResidual A b c x y s) ≤ ε →
    (∀ j, |x j * s j / μ - 1| ≤ θ) → ¬ Wrong x y s

omit [Fintype C] in
/-- Exact centrality formula for actual central triples. -/
theorem actual_mixture_defect (w : I → ℝ) (x s : I → C → ℝ) (μ : ℝ)
    (hμ : 0 < μ) (hx : ∀ i j, 0 < x i j) (hc : ∀ i j, x i j * s i j = μ)
    (j : C) :
    mix w x j * mix w s j / μ - 1 = multiplicativeDefect w (fun i => x i j) := by
  exact central_mixture_defect w (fun i => x i j) (fun i => s i j) μ hμ
    (fun i => hx i j) (fun i => hc i j)

omit [Fintype C] in
/-- The paper's weighted variance formula, for the actual primal/slack mixture. -/
theorem actual_mixture_variance (w : I → ℝ) (hw : ProbWeights w)
    (x s : I → C → ℝ) (μ : ℝ) (hμ : 0 < μ)
    (hx : ∀ i j, 0 < x i j) (hc : ∀ i j, x i j * s i j = μ) (j : C) :
    mix w x j * mix w s j / μ - 1 =
      (1 / 2 : ℝ) * ∑ i, ∑ k,
        w i * w k * (x i j - x k j)^2 / (x i j * x k j) := by
  rw [actual_mixture_defect w x s μ hμ hx hc,
    weighted_multiplicative_variance w _ hw (fun i => hx i j)]

/-- Once a residual estimate is available, the wrong mixture forces one of
    the two strict failures. Both gap and centrality are derived from the LP. -/
theorem central_soundness_from_residual_bound
    (w : I → ℝ) (hw : ProbWeights w) (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (b : R → ℝ) (c : C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (μ ε θ Q : ℝ)
    (hμ : 0 < μ) (hε : 0 ≤ ε) (hx : ∀ i j, 0 < x i j)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hc : ∀ i j, x i j * s i j = μ)
    (hbound : kktSqResidual A b c (mix w x) (mix w y) (mix w s) ≤ Q)
    (Wrong : (C → ℝ) → (R → ℝ) → (C → ℝ) → Prop)
    (hwrong : Wrong (mix w x) (mix w y) (mix w s))
    (hsound : CentralOutputSound A b c μ ε θ Wrong) :
    ε ^ 2 < Q ∨ ∃ j, θ < multiplicativeDefect w (fun i => x i j) := by
  by_contra h
  push Not at h
  have hs : ∀ i j, 0 < s i j := by
    intro i j
    have := hc i j
    exact (mul_pos_iff.mp (this ▸ hμ)).resolve_right (by intro hh; linarith [hx i j]) |>.2
  apply hsound (mix w x) (mix w y) (mix w s)
    (mixture_pos w hw x hx) (mixture_pos w hw s hs)
    (central_mixture_objective_gap w hw A' b c x s y μ hp hd hc)
    (Real.sqrt_le_iff.mpr ⟨hε, hbound.trans h.1⟩) _ hwrong
  intro j
  rw [actual_mixture_defect w x s μ hμ hx hc,
    abs_of_nonneg (multiplicativeDefect_nonneg w _ hw (fun i => hx i j))]
  exact h.2 j

/-- Complete common-parameter dichotomy from raw matrix locality, exact
    neighboring central triples, and a uniform affine wrong-output margin. -/
theorem central_affine_soundness_dichotomy [DecidableEq I] [DecidableEq C]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (b : R → ℝ) (c : C → ℝ)
    (w : I → ℝ) (D : R → Finset C) (label : R → C → I)
    (sr sc : ℕ) (B H : ℝ) (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (μ ε θ : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hxpos : ∀ i j, 0 < x i j) (hc : ∀ i j, x i j * s i j = μ)
    (ax as' : C → ℝ) (ay : R → ℝ) (a₀ p γ : ℝ)
    (hwrong : ∀ i, p * tripleScore ax as' ay a₀ (x i) (y i) (s i) ≤ -γ)
    (hsound : CentralOutputSound A b c μ ε θ
      (fun x y s => p * tripleScore ax as' ay a₀ x y s ≤ -γ)) :
    ε^2 < 12 * (max sr (2 * sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      ∑ i, (incidence D label i : ℝ) * (w i)^2 ∨
      ∃ j, θ < multiplicativeDefect w (fun i => x i j) := by
  exact central_soundness_from_residual_bound w hw A A' b c x s y μ ε θ _
    hμ hε hxpos hp hd hc
    (weighted_kkt_paper_bound A A' x s y b c w D label sr sc B H hw hB hH
      hA hA' hx hy hr hcol hp hd hlocal)
    _ (tripleScore_wrong_mix w hw ax as' ay a₀ p γ x s y hwrong) hsound

def PointCenteredOutputSound (A : R → C → ℝ) (b : R → ℝ) (c : C → ℝ)
    (μ ε θ : ℝ) (Wrong : (C → ℝ) → (R → ℝ) → (C → ℝ) → Prop) : Prop :=
  ∀ x y s, (∀ j, 0 < x j) → (∀ j, 0 < s j) →
    dot c x - dot b y = (Fintype.card C : ℝ) * μ →
    Real.sqrt (kktSqResidual A b c x y s) ≤ ε →
    (∀ j, |x j * s j / coordinateMean (fun k => x k * s k) - 1| ≤ θ) →
    ¬ Wrong x y s

/-- Exact normalized defect of a central mixture under point centering. -/
theorem actual_point_centered_defect [Nonempty C]
    (w : I → ℝ) (hw : ProbWeights w) (x s : I → C → ℝ) (μ : ℝ)
    (hμ : 0 < μ) (hx : ∀ i j, 0 < x i j) (hc : ∀ i j, x i j * s i j = μ)
    (j : C) :
    |mix w x j * mix w s j /
      coordinateMean (fun k => mix w x k * mix w s k) - 1| =
      |multiplicativeDefect w (fun i => x i j) -
        coordinateMean (fun k => multiplicativeDefect w (fun i => x i k))| /
      (1 + coordinateMean (fun k => multiplicativeDefect w (fun i => x i k))) := by
  apply point_centered_absolute_defect_identity
    (fun k => mix w x k * mix w s k)
    (fun k => multiplicativeDefect w (fun i => x i k)) μ hμ _ _ j
  · intro k
    have h := actual_mixture_defect w x s μ hμ hx hc k
    have heq : mix w x k * mix w s k / μ =
        1 + multiplicativeDefect w (fun i => x i k) := by linarith
    have := (div_eq_iff (ne_of_gt hμ)).mp heq
    nlinarith
  · intro k
    exact multiplicativeDefect_nonneg w _ hw (fun i => hx i k)

/-- Point-centered soundness gives the same residual alternative and the
    exact normalized coordinate-width alternative. -/
theorem point_centered_soundness_from_residual_bound [Nonempty C]
    (w : I → ℝ) (hw : ProbWeights w) (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (b : R → ℝ) (c : C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (μ ε θ Q : ℝ)
    (hμ : 0 < μ) (hε : 0 ≤ ε) (hx : ∀ i j, 0 < x i j)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hc : ∀ i j, x i j * s i j = μ)
    (hbound : kktSqResidual A b c (mix w x) (mix w y) (mix w s) ≤ Q)
    (Wrong : (C → ℝ) → (R → ℝ) → (C → ℝ) → Prop)
    (hwrong : Wrong (mix w x) (mix w y) (mix w s))
    (hsound : PointCenteredOutputSound A b c μ ε θ Wrong) :
    ε ^ 2 < Q ∨ ∃ j, θ <
      |multiplicativeDefect w (fun i => x i j) -
        coordinateMean (fun k => multiplicativeDefect w (fun i => x i k))| /
      (1 + coordinateMean (fun k => multiplicativeDefect w (fun i => x i k))) := by
  by_contra h
  push Not at h
  have hs : ∀ i j, 0 < s i j := by
    intro i j
    have := hc i j
    exact (mul_pos_iff.mp (this ▸ hμ)).resolve_right (by intro hh; linarith [hx i j]) |>.2
  apply hsound (mix w x) (mix w y) (mix w s)
    (mixture_pos w hw x hx) (mixture_pos w hw s hs)
    (central_mixture_objective_gap w hw A' b c x s y μ hp hd hc)
    (Real.sqrt_le_iff.mpr ⟨hε, hbound.trans h.1⟩) _ hwrong
  intro j
  rw [actual_point_centered_defect w hw x s μ hμ hx hc]
  exact h.2 j

/-- Kantorovich controls either convention for every probability mixture,
    not just the uniform mixture appearing in the manuscript. -/
theorem central_ratio_soundness_dichotomy [Nonempty I] [Nonempty C]
    (w : I → ℝ) (hw : ProbWeights w) (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (b : R → ℝ) (c : C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (μ ε θ Q ratio : ℝ)
    (hμ : 0 < μ) (hε : 0 ≤ ε) (hx : ∀ i j, 0 < x i j)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hc : ∀ i j, x i j * s i j = μ)
    (hbound : kktSqResidual A b c (mix w x) (mix w y) (mix w s) ≤ Q)
    (hratio : 0 < ratio) (hspread : ∀ j i k, x i j / x k j ≤ ratio)
    (Wrong : (C → ℝ) → (R → ℝ) → (C → ℝ) → Prop)
    (hwrong : Wrong (mix w x) (mix w y) (mix w s))
    (hsound : CentralOutputSound A b c μ ε θ Wrong ∨
      PointCenteredOutputSound A b c μ ε θ Wrong) :
    ε^2 < Q ∨ θ < (ratio - 1)^2 / (4 * ratio) := by
  have hdb (j : C) : 0 ≤ multiplicativeDefect w (fun i => x i j) ∧
      multiplicativeDefect w (fun i => x i j) ≤ kantorovich ratio - 1 :=
    ⟨multiplicativeDefect_nonneg w _ hw (fun i => hx i j),
      kantorovich_pairwise_ratio_bound w _ hw (fun i => hx i j) ratio hratio (hspread j)⟩
  rw [← kantorovich_sub_one ratio hratio]
  rcases hsound with hsound | hsound
  · rcases central_soundness_from_residual_bound w hw A A' b c x s y μ ε θ Q
      hμ hε hx hp hd hc hbound Wrong hwrong hsound with h | ⟨j, hj⟩
    · exact Or.inl h
    · exact Or.inr (hj.trans_le (hdb j).2)
  · rcases point_centered_soundness_from_residual_bound w hw A A' b c x s y μ ε θ Q
      hμ hε hx hp hd hc hbound Wrong hwrong hsound with h | ⟨j, hj⟩
    · exact Or.inl h
    · exact Or.inr (hj.trans_le (point_centered_defect_bound _ _ hdb j))

/-- Uniform-weight resource/centrality dichotomy, for either neighborhood
    convention, with the number of dependent raw matrix positions. -/
theorem central_uniform_soundness_dichotomy
    [DecidableEq C] [Nonempty I] [Nonempty C]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (b : R → ℝ) (c : C → ℝ)
    (D : R → Finset C) (label : R → C → I)
    (sr sc : ℕ) (B H : ℝ) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (μ ε θ ratio : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hxpos : ∀ i j, 0 < x i j) (hc : ∀ i j, x i j * s i j = μ)
    (hratio : 0 < ratio) (hspread : ∀ j i k, x i j / x k j ≤ ratio)
    (Wrong : (C → ℝ) → (R → ℝ) → (C → ℝ) → Prop)
    (hwrong : Wrong (mix (uniformWeight I) x) (mix (uniformWeight I) y)
      (mix (uniformWeight I) s))
    (hsound : CentralOutputSound A b c μ ε θ Wrong ∨
      PointCenteredOutputSound A b c μ ε θ Wrong) :
    ε^2 < 12 * (max sr (2 * sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      totalIncidence D / (Fintype.card I : ℝ)^2 ∨
      θ < (ratio - 1)^2 / (4 * ratio) := by
  classical
  have hb := weighted_kkt_paper_bound A A' x s y b c (uniformWeight I) D label
    sr sc B H (uniformWeight_prob I) hB hH hA hA' hx hy hr hcol hp hd hlocal
  have hsum : (∑ i, (incidence D label i : ℝ)) = totalIncidence D := by
    have hh := incidence_sum D label (fun _ => (1 : ℝ))
    simpa [totalIncidence] using hh.symm
  rw [uniform_incidence_cost, hsum] at hb
  have heq : 12 * (max sr (2 * sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      ((totalIncidence D : ℝ) / (Fintype.card I : ℝ)^2) =
      12 * (max sr (2 * sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      totalIncidence D / (Fintype.card I : ℝ)^2 := by ring
  rw [heq] at hb
  exact central_ratio_soundness_dichotomy (uniformWeight I) (uniformWeight_prob I)
    A A' b c x s y μ ε θ _ ratio hμ hε hxpos hp hd hc hb hratio hspread Wrong hwrong hsound

/-- The normalized pair decoder supplies the wrong-output premise from
    neighbor margins; the squared norm is strictly positive. -/
theorem central_pair_soundness_dichotomy
    [DecidableEq I] [DecidableEq C] {P : Type*} [Fintype P] [Nonempty P]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (b : R → ℝ) (c : C → ℝ)
    (w : I → ℝ) (D : R → Finset C) (label : R → C → I)
    (sr sc : ℕ) (B H : ℝ) (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (μ ε θ : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hxpos : ∀ i j, 0 < x i j) (hc : ∀ i j, x i j * s i j = μ)
    (e : P × Bool ↪ C) (p a : ℝ) (hpSign : p = 1 ∨ p = -1) (ha : 0 < a)
    (hmargin : ∀ i l, a ≤ (-p) * (x i (e (l, true)) - x i (e (l, false))))
    (hsound : CentralOutputSound A b c μ ε θ
      (fun x _ _ => 0 < sqNorm x ∧ (Fintype.card P : ℝ) * a ^ 2 /
        ((Fintype.card C : ℝ) * H ^ 2) ≤ (-p) * pairExpectation e x)) :
    ε^2 < 12 * (max sr (2 * sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      ∑ i, (incidence D label i : ℝ) * (w i)^2 ∨
      ∃ j, θ < multiplicativeDefect w (fun i => x i j) := by
  have hpneg : -p = 1 ∨ -p = -1 := by rcases hpSign with rfl | rfl <;> norm_num
  exact central_soundness_from_residual_bound w hw A A' b c x s y μ ε θ _
    hμ hε hxpos hp hd hc
    (weighted_kkt_paper_bound A A' x s y b c w D label sr sc B H hw hB hH
      hA hA' hx hy hr hcol hp hd hlocal)
    _ (mixture_pair_decoder_bound e hw (fun i j => (hxpos i j).le) hx hpneg ha hmargin)
    hsound

/-- Raw-data point-centered dichotomy with an explicit affine decoder. -/
theorem point_centered_affine_soundness_dichotomy
    [DecidableEq I] [DecidableEq C] [Nonempty C]
    (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x s : I → C → ℝ) (y : I → R → ℝ) (b : R → ℝ) (c : C → ℝ)
    (w : I → ℝ) (D : R → Finset C) (label : R → C → I)
    (sr sc : ℕ) (B H : ℝ) (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hd : ∀ i j, (∑ r, A' i r j * y i r) + s i j = c j)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j)
    (μ ε θ : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hxpos : ∀ i j, 0 < x i j) (hc : ∀ i j, x i j * s i j = μ)
    (ax as' : C → ℝ) (ay : R → ℝ) (a₀ p γ : ℝ)
    (hwrong : ∀ i, p * tripleScore ax as' ay a₀ (x i) (y i) (s i) ≤ -γ)
    (hsound : PointCenteredOutputSound A b c μ ε θ
      (fun x y s => p * tripleScore ax as' ay a₀ x y s ≤ -γ)) :
    ε^2 < 12 * (max sr (2 * sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      ∑ i, (incidence D label i : ℝ) * (w i)^2 ∨
      ∃ j, θ < |multiplicativeDefect w (fun i => x i j) -
        coordinateMean (fun k => multiplicativeDefect w (fun i => x i k))| /
      (1 + coordinateMean (fun k => multiplicativeDefect w (fun i => x i k))) := by
  exact point_centered_soundness_from_residual_bound w hw A A' b c x s y μ ε θ _
    hμ hε hxpos hp hd hc
    (weighted_kkt_paper_bound A A' x s y b c w D label sr sc B H hw hB hH
      hA hA' hx hy hr hcol hp hd hlocal)
    _ (tripleScore_wrong_mix w hw ax as' ay a₀ p γ x s y hwrong) hsound

end
end QipmFormal.Mixture
