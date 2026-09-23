import QipmFormal.SDPMixture.Residual
import QipmFormal.Mixture.Multibit

/-!
# SDP residuals for coefficients depending on several bits

Both residual blocks are matrix-change sums. The same raw dependent position
occurs once in each block, and the identity block contributes no incidence.
The degree bound is on each coefficient's set of influencing bits; a bound
on the union in each row implies this assumption.
-/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators
open Mixture
variable {I R C : Type*} [Fintype I] [Fintype R] [Fintype C]

/-- Squared multibit residual bound with the exact total incidence count. -/
theorem multibit_matrixChangeMix_sq [Nonempty I] (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ)
    (D : R → Finset C) (J : R → C → Finset I) (s d : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hd : ∀ r j, (J r j).card ≤ d)
    (hD : ∀ r j, j ∉ D r → J r j = ∅)
    (hlocal : ∀ i r j, i ∉ J r j → A' i r j = A r j) :
    sqNorm (matrixChangeMix A A' x (uniformWeight I)) ≤
      4 * B ^ 2 * H ^ 2 * d * s *
        (∑ r, ∑ j, ((J r j).card : ℝ)) / (Fintype.card I : ℝ) ^ 2 := by
  classical
  let f : R → C → I → ℝ := fun r j i => (A r j - A' i r j) * x i j
  have hf (r : R) (j : C) (i : I) (hj : j ∈ D r) : (f r j i) ^ 2 ≤ 4 * B ^ 2 * H ^ 2 := by
    have hdiff : |A r j - A' i r j| ≤ 2 * B :=
      (abs_sub _ _).trans (by linarith [hA r j hj, hA' i r j hj])
    have hh : |f r j i| ≤ 2 * B * H := by
      dsimp [f]
      rw [abs_mul]
      exact mul_le_mul hdiff (hx i j) (abs_nonneg _) (by positivity)
    have hh' := (sq_le_sq₀ (abs_nonneg (f r j i)) (by positivity : 0 ≤ 2 * B * H)).mpr hh
    simp only [sq_abs] at hh'
    nlinarith
  have heq (r : R) : matrixChangeMix A A' x (uniformWeight I) r =
      (∑ j ∈ D r, ∑ i ∈ J r j, f r j i) / (Fintype.card I : ℝ) := by
    unfold matrixChangeMix
    simp only [uniformWeight, ← Finset.mul_sum, div_eq_mul_inv]
    rw [mul_comm]
    congr 1
    rw [← Finset.sum_subset (Finset.subset_univ (D r))]
    · apply Finset.sum_congr rfl
      intro j _
      symm
      apply Finset.sum_subset (Finset.subset_univ (J r j))
      intro i _ hi
      dsimp [f]
      rw [hlocal i r j hi]
      ring
    · intro j _ hj
      apply Finset.sum_eq_zero
      intro i _
      rw [hlocal i r j (by rw [hD r j hj]; simp)]
      ring
  have hrow (r : R) : (∑ j ∈ D r, ∑ i ∈ J r j, f r j i) ^ 2 ≤
      (s : ℝ) * d * (4 * B ^ 2 * H ^ 2) * ∑ j, ((J r j).card : ℝ) := by
    have hinc : (∑ j ∈ D r, ((J r j).card : ℝ)) = ∑ j, ((J r j).card : ℝ) := by
      apply Finset.sum_subset (Finset.subset_univ (D r))
      intro j _ hj
      simp [hD r j hj]
    calc
      _ ≤ ((D r).card : ℝ) * ∑ j ∈ D r, (∑ i ∈ J r j, f r j i) ^ 2 :=
        sum_square_le_card_mul _ _
      _ ≤ (s : ℝ) * ∑ j ∈ D r, (∑ i ∈ J r j, f r j i) ^ 2 :=
        mul_le_mul_of_nonneg_right (Nat.cast_le.mpr (hs r))
          (Finset.sum_nonneg fun _ _ => sq_nonneg _)
      _ ≤ (s : ℝ) * ∑ j ∈ D r, (d : ℝ) * (4 * B ^ 2 * H ^ 2) * (J r j).card := by
        apply mul_le_mul_of_nonneg_left _ (Nat.cast_nonneg _)
        apply Finset.sum_le_sum
        intro j hj
        calc
          _ ≤ ((J r j).card : ℝ) * ∑ i ∈ J r j, (f r j i) ^ 2 :=
            sum_square_le_card_mul _ _
          _ ≤ (d : ℝ) * ∑ i ∈ J r j, (f r j i) ^ 2 :=
            mul_le_mul_of_nonneg_right (Nat.cast_le.mpr (hd r j))
              (Finset.sum_nonneg fun _ _ => sq_nonneg _)
          _ ≤ (d : ℝ) * ∑ _i ∈ J r j, (4 * B ^ 2 * H ^ 2) :=
            mul_le_mul_of_nonneg_left (Finset.sum_le_sum fun i _ => hf r j i hj) (Nat.cast_nonneg _)
          _ = _ := by simp; ring
      _ = _ := by rw [← Finset.mul_sum, hinc]; ring
  unfold sqNorm
  calc
    _ = (∑ r, (∑ j ∈ D r, ∑ i ∈ J r j, f r j i) ^ 2) / (Fintype.card I : ℝ) ^ 2 := by
      simp only [heq, div_pow]
      rw [Finset.sum_div]
    _ ≤ (∑ r, (s : ℝ) * d * (4 * B ^ 2 * H ^ 2) * ∑ j, ((J r j).card : ℝ)) /
        (Fintype.card I : ℝ) ^ 2 :=
      div_le_div_of_nonneg_right (Finset.sum_le_sum fun r _ => hrow r) (sq_nonneg _)
    _ = _ := by rw [← Finset.mul_sum]; ring


variable {n : Type*} [Fintype n]

/-- The degree-weighted SDP KKT bound, derived from both actual residual blocks. -/
theorem sdp_multibit_kkt_sq [Nonempty I] [DecidableEq C]
    (e : OrthonormalBasis C ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (Q : SymmetricMatrix n)
    (D : R → Finset C) (L : R → C → Finset I) (sr sc d : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hdegree : ∀ r j, (L r j).card ≤ d)
    (hD : ∀ r j, j ∉ D r → L r j = ∅)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = Q)
    (hlocal : ∀ i r j, i ∉ L r j →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j) :
    sdpKktSqResidual A b Q (symmetricMix (uniformWeight I) X)
      (mix (uniformWeight I) y) (symmetricMix (uniformWeight I) S) ≤
      4 * B^2 * H^2 * d * (sr + sc : ℕ) *
        (∑ r, ∑ j, ((L r j).card : ℝ)) / (Fintype.card I : ℝ)^2 := by
  classical
  let a := coordinateMatrix e A
  let a' := fun i => coordinateMatrix e (A' i)
  let x := fun i => svec e (X i)
  let s := fun i => svec e (S i)
  have hp' (i : I) (r : R) : ∑ j, a' i r j * x i j = b r := by
    change (∑ j, coordinateMatrix e (A' i) r j * svec e (X i) j) = b r
    rw [← measurement_coordinates, hp i]
  have hd' (i : I) (j : C) : (∑ r, a' i r j * y i r) + s i j = svec e Q j := by
    have h := congrArg (fun T => svec e T j) (hd i)
    simpa [svec_add, adjoint_coordinates, a', s] using h
  have hprimal : Mixture.residual a (mix (uniformWeight I) x) b =
      matrixChangeMix a a' x (uniformWeight I) := by
    funext r
    exact residual_mix_eq a a' x b _ (uniformWeight_prob I) hp' r
  have hdual : stationarity a (mix (uniformWeight I) y)
      (mix (uniformWeight I) s) (svec e Q) =
      matrixChangeMix (fun j r => a r j) (fun i j r => a' i r j) y (uniformWeight I) := by
    funext j
    rw [stationarity_mixture_identity _ (uniformWeight_prob I) a a' y s _ hd' j]
    simp only [matrixChangeMix, Finset.mul_sum]
    exact Finset.sum_comm
  have hpb := multibit_matrixChangeMix_sq a a' x D L sr d B H
    hB hH hA hA' hx hr hdegree hD hlocal
  have hdb := multibit_matrixChangeMix_sq (fun j r => a r j)
    (fun i j r => a' i r j) y (transposePositions D) (fun j r => L r j) sc d B H
    hB hH (fun j r h => hA r j (by simpa [transposePositions] using h))
    (fun i j r h => hA' i r j (by simpa [transposePositions] using h)) hy hcol
    (fun j r => hdegree r j) (fun j r h => hD r j (by simpa [transposePositions] using h))
    (fun i j r h => hlocal i r j h)
  rw [Finset.sum_comm (f := fun j r => ((L r j).card : ℝ))] at hdb
  rw [sdpKktSqResidual_coordinates e, svec_mix, svec_mix]
  change kktSqResidual a b (svec e Q) (mix (uniformWeight I) x)
    (mix (uniformWeight I) y) (mix (uniformWeight I) s) ≤ _
  unfold kktSqResidual
  rw [hprimal, hdual]
  have h := add_le_add hpb hdb
  calc
    _ ≤ _ := h
    _ = _ := by push_cast; ring

/-- The multibit norm bound with the sharper direct row-plus-column constant. -/
theorem sdp_multibit_kkt_bound [Nonempty I] [DecidableEq C]
    (e : OrthonormalBasis C ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (Q : SymmetricMatrix n)
    (D : R → Finset C) (L : R → C → Finset I) (sr sc d : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hdegree : ∀ r j, (L r j).card ≤ d)
    (hD : ∀ r j, j ∉ D r → L r j = ∅)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = Q)
    (hlocal : ∀ i r j, i ∉ L r j →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j) :
    Real.sqrt (sdpKktSqResidual A b Q (symmetricMix (uniformWeight I) X)
      (mix (uniformWeight I) y) (symmetricMix (uniformWeight I) S)) ≤
      2 * B * H * Real.sqrt ((d : ℝ) * (sr + sc : ℕ) *
        (∑ r, ∑ j, ((L r j).card : ℝ))) / Fintype.card I := by
  have h := sdp_multibit_kkt_sq e A A' X S y b Q D L sr sc d B H
    hB hH hA hA' hx hy hr hcol hdegree hD hp hd hlocal
  apply Real.sqrt_le_iff.mpr
  constructor
  · positivity
  · calc
      _ ≤ _ := h
      _ = _ := by rw [div_pow, mul_pow, mul_pow, Real.sq_sqrt (by positivity)]; ring

end
end QipmFormal.SDPMixture
