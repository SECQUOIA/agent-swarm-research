import Formal.MatroidSpectral.InterpolationExecution
import Formal.MatroidSpectral.DeterminantBits
import Formal.DAGSpectral.EigenCompareBits

/-! Integral coefficient bounds prevent repeated rational addition from giving
an exponential size estimate for the materialized Lagrange coefficient table. -/
namespace MatroidSpectral
open ReciprocalAnchor DAGSpectral

/-- A rational is an integer with a bounded absolute value. -/
def IntegralBound (q : ℚ) (K : ℕ) : Prop :=
  ∃ z : ℤ, (z : ℚ) = q ∧ z.natAbs ≤ 2 ^ K

lemma integralBound_zero (K : ℕ) : IntegralBound 0 K := ⟨0, by simp, by simp⟩
lemma integralBound_one (K : ℕ) : IntegralBound 1 K :=
  ⟨1, by simp, by simpa using Nat.one_le_pow K 2 (by decide)⟩

lemma IntegralBound.mono {q : ℚ} {K L : ℕ} (h : IntegralBound q K) (hKL : K ≤ L) :
    IntegralBound q L := by
  obtain ⟨z, rfl, hz⟩ := h
  exact ⟨z, rfl, hz.trans (Nat.pow_le_pow_right (by decide) hKL)⟩

lemma IntegralBound.mul {q r : ℚ} {K L : ℕ}
    (hq : IntegralBound q K) (hr : IntegralBound r L) : IntegralBound (q*r) (K+L) := by
  obtain ⟨z, rfl, hz⟩ := hq
  obtain ⟨w, rfl, hw⟩ := hr
  exact ⟨z*w, by push_cast; rfl, by simpa [Int.natAbs_mul, pow_add] using Nat.mul_le_mul hz hw⟩

lemma IntegralBound.sub {q r : ℚ} {K : ℕ}
    (hq : IntegralBound q K) (hr : IntegralBound r K) : IntegralBound (q-r) (K+1) := by
  obtain ⟨z, rfl, hz⟩ := hq
  obtain ⟨w, rfl, hw⟩ := hr
  refine ⟨z-w, by push_cast; rfl, ?_⟩
  have hh := Int.natAbs_sub_le z w
  rw [pow_succ]
  omega

lemma IntegralBound.bits {q : ℚ} {K : ℕ} (h : IntegralBound q K) :
    RationalBits q (K+1) := by
  obtain ⟨z, rfl, hz⟩ := h
  constructor
  · simp only [Rat.num_intCast]
    exact hz.trans_lt (by rw [pow_succ]; have := Nat.two_pow_pos K; omega)
  · simp only [Rat.den_intCast]
    exact Nat.one_lt_two_pow (by omega)

lemma interpolationNode_integralBound {D : ℕ} (t : Fin (D + 1)) :
    IntegralBound (interpolationNode t) (D+1) := by
  refine ⟨(t.val+1 : ℕ), by simp [interpolationNode], ?_⟩
  simpa only [Int.natAbs_natCast] using
    (show t.val+1 ≤ D+1 by omega).trans (Nat.le_of_lt (D+1).lt_two_pow_self)

lemma interpolationNumeratorTable_integralBound (D N : ℕ) (xs : List ℚ)
    (hx : ∀ x ∈ xs, IntegralBound x N) (k : ℕ) :
    IntegralBound ((interpolationNumeratorTable D xs).getD k 0) (xs.length*(N+1)) := by
  induction xs generalizing k with
  | nil =>
    simp only [List.length_nil, Nat.zero_mul, interpolationNumeratorTable]
    by_cases hk : k < D+1
    · rw [List.getD_eq_getElem _ _ (by simpa using hk)]
      simp only [List.getElem_ofFn]
      split_ifs
      · exact integralBound_one _
      · exact integralBound_zero _
    · rw [List.getD_eq_default _ _ (by simpa using Nat.le_of_not_lt hk)]
      exact integralBound_zero _
  | cons x xs ih =>
    have hi := ih (fun y hy => hx y (by simp [hy]))
    have hn := hx x (by simp)
    by_cases hk : k < D+1
    · simp only [interpolationNumeratorTable]
      rw [List.getD_eq_getElem _ _ (by simpa using hk)]
      simp only [List.getElem_ofFn]
      have hp := hn.mul (hi k)
      have hl : IntegralBound
          (if k = 0 then 0 else (interpolationNumeratorTable D xs).getD (k-1) 0)
          (N+xs.length*(N+1)) := by
        split_ifs
        · exact integralBound_zero _
        · exact (hi (k-1)).mono (by omega)
      convert hl.sub hp using 1
      simp only [List.length_cons]
      ring
    · rw [List.getD_eq_default _ _ (by
        simpa [interpolationNumeratorTable_length] using Nat.le_of_not_lt hk)]
      exact integralBound_zero _

lemma interpolationOtherNodes_length_le (D : ℕ) (t : Fin (D + 1)) :
    (interpolationOtherNodes D t).length ≤ D+1 := by
  simpa only [interpolationOtherNodes, List.length_map, List.length_finRange] using
    List.length_filter_le (fun j : Fin (D + 1) => j ≠ t) (List.finRange (D+1))

lemma interpolationOtherNodes_integralBound (D : ℕ) (t : Fin (D + 1)) :
    ∀ x ∈ interpolationOtherNodes D t, IntegralBound x (D+1) := by
  intro x hx
  obtain ⟨j, _, rfl⟩ := List.mem_map.mp hx
  exact interpolationNode_integralBound j

lemma interpolationNumeratorTable_bits (D : ℕ) (t : Fin (D + 1)) (k : ℕ) :
    RationalBits ((interpolationNumeratorTable D (interpolationOtherNodes D t)).getD k 0)
      (1+(D+1)*(D+2)) := by
  have hh := (interpolationNumeratorTable_integralBound D (D+1)
    (interpolationOtherNodes D t) (interpolationOtherNodes_integralBound D t) k).bits
  apply rationalBits_mono hh
  have hm := Nat.mul_le_mul_right (D+2) (interpolationOtherNodes_length_le D t)
  convert Nat.add_le_add_right hm 1 using 1
  ring

/-- A uniform polynomial budget for one scalar Lagrange coefficient. -/
def interpolationWeightBits (D : ℕ) : ℕ := 2+(D+1)*(3*D+8)

lemma interpolationWeightRun_bits (D : ℕ) (t : Fin (D + 1)) (k : ℕ) :
    RationalBits (interpolationWeightRun D t k) (interpolationWeightBits D) := by
  have ht := (interpolationNode_integralBound t).bits
  have hd : RationalBits
      (((interpolationOtherNodes D t).map (fun x => interpolationNode t-x)).prod)
      (1+(interpolationOtherNodes D t).length*(2*(D+2)+1)) := by
    apply rationalBits_mono (rationalBits_list_prod (by
      intro x hx
      obtain ⟨y, hy, rfl⟩ := List.mem_map.mp hx
      exact rationalBits_sub ht ((interpolationOtherNodes_integralBound D t y hy).bits)))
    simp only [List.length_map]
    exact le_of_eq (by ring)
  apply rationalBits_mono (rationalBits_div (interpolationNumeratorTable_bits D t k) hd)
  unfold interpolationWeightBits
  have hm := Nat.mul_le_mul_right (2*(D+2)+1) (interpolationOtherNodes_length_le D t)
  nlinarith

/-- All tensor factors and the final sum have polynomial size in the grid size. -/
lemma interpolateCoefficientRun_bits {κ : Type*} [Fintype κ] [DecidableEq κ]
    (D B : ℕ) (values : (κ → Fin (D + 1)) → ℚ)
    (hv : ∀ t, RationalBits (values t) B) (z : κ → Fin (D + 1)) :
    RationalBits (interpolateCoefficientRun D values z)
      (1+(D+1)^(Fintype.card κ)*(B+2+Fintype.card κ*interpolationWeightBits D)) := by
  apply rationalBits_mono (rationalBits_finset_sum Finset.univ _ (by
    intro t _
    exact rationalBits_mul (hv t) (rationalBits_finset_prod Finset.univ _
      (fun i _ => interpolationWeightRun_bits D (t i) (z i).val))))
  simp only [Finset.card_univ, Fintype.card_fun, Fintype.card_fin]
  exact le_of_eq (by ring)

end MatroidSpectral
