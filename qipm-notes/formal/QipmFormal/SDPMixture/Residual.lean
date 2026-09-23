import QipmFormal.SDPMixture.Coordinates

/-!
# Sparse residual bounds for actual SDP measurement maps

The primal norm is Euclidean and the dual matrix norm is Frobenius. Sparsity
and coefficient bounds refer to the fixed isometric coordinates, exactly as
in the manuscript. The slack identity block changes no input coefficients.
-/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators
open Mixture

variable {n J R I : Type*} [Fintype n] [Fintype J] [Fintype R] [Fintype I]

/-- Sum of the squared primal Euclidean and dual Frobenius residuals. -/
def sdpKktSqResidual (A : R → SymmetricMatrix n) (b : R → ℝ)
    (C X : SymmetricMatrix n) (y : R → ℝ) (S : SymmetricMatrix n) : ℝ :=
  sqNorm (measurement A X - b) +
    ∑ i, ∑ j, (toMatrix (measurementAdjoint A y + S - C) i j)^2

theorem sdpKktSqResidual_nonneg (A : R → SymmetricMatrix n) (b : R → ℝ)
    (C X : SymmetricMatrix n) (y : R → ℝ) (S : SymmetricMatrix n) :
    0 ≤ sdpKktSqResidual A b C X y S := by
  unfold sdpKktSqResidual
  exact add_nonneg (sqNorm_nonneg _)
    (Finset.sum_nonneg fun _ _ => Finset.sum_nonneg fun _ _ => sq_nonneg _)

/-- The explicit residual is the sum of the squared Euclidean and Frobenius norms. -/
theorem sdpKktSqResidual_eq_norms (A : R → SymmetricMatrix n) (b : R → ℝ)
    (C X : SymmetricMatrix n) (y : R → ℝ) (S : SymmetricMatrix n) :
    sdpKktSqResidual A b C X y S = euclideanNorm (measurement A X - b)^2 +
      frobeniusNorm (toMatrix (measurementAdjoint A y + S - C))^2 := by
  rw [euclideanNorm_sq, frobeniusNorm_sq]
  rfl

/-- Isometric vectorization exactly preserves both SDP residual blocks. -/
theorem sdpKktSqResidual_coordinates (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (b : R → ℝ) (C X : SymmetricMatrix n)
    (y : R → ℝ) (S : SymmetricMatrix n) :
    sdpKktSqResidual A b C X y S =
      kktSqResidual (coordinateMatrix e A) b (svec e C) (svec e X) y (svec e S) := by
  unfold sdpKktSqResidual kktSqResidual
  rw [← sqNorm_svec e]
  congr 1
  · congr 1
    funext r
    simp [Mixture.residual, measurement_coordinates e]
  · congr 1
    funext j
    simp [stationarity, svec_sub, svec_add, adjoint_coordinates]

/-- Public positions cancel, so only dependent coefficients require a bound. -/
theorem matrixChangeMix_bound_on_positions [DecidableEq I]
    (A : R → J → ℝ) (A' : I → R → J → ℝ)
    (x : I → J → ℝ) (w : I → ℝ) (D : R → Finset J) (label : R → J → I)
    (s : ℕ) (B H : ℝ) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    sqNorm (matrixChangeMix A A' x w) ≤
      4 * s * B^2 * H^2 * ∑ i, (incidence D label i : ℝ) * (w i)^2 := by
  classical
  let a : R → J → ℝ := fun r j => if j ∈ D r then A r j else 0
  let a' : I → R → J → ℝ := fun i r j => if j ∈ D r then A' i r j else 0
  have ha : ∀ r j, |a r j| ≤ B := by
    intro r j
    by_cases hj : j ∈ D r <;> simp only [a, hj, ↓reduceIte]
    · exact hA r j hj
    · simpa using hB
  have ha' : ∀ i r j, |a' i r j| ≤ B := by
    intro i r j
    by_cases hj : j ∈ D r <;> simp only [a', hj, ↓reduceIte]
    · exact hA' i r j hj
    · simpa using hB
  have he : matrixChangeMix A A' x w = matrixChangeMix a a' x w := by
    funext r
    unfold matrixChangeMix
    apply Finset.sum_congr rfl
    intro j _
    apply Finset.sum_congr rfl
    intro i _
    by_cases hj : j ∈ D r
    · simp [a, a', hj]
    · simp [a, a', hj, hlocal i r j (Or.inl hj)]
  rw [he]
  apply matrixChangeMix_bound a a' x w D label s B H hB hH ha ha' hx hs
  intro i r j hl
  by_cases hj : j ∈ D r
  · simpa [a, a', hj] using hlocal i r j hl
  · simp [a, a', hj]

/-- The single-flip weighted bound for the actual SDP primal and dual residuals.
Only the primal and multiplier coordinates need the magnitude bound. -/
theorem sdp_weighted_kkt_bound [DecidableEq I] [DecidableEq J]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (C : SymmetricMatrix n)
    (w : I → ℝ) (D : R → Finset J) (label : R → J → I)
    (sr sc : ℕ) (B H : ℝ) (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j) :
    sdpKktSqResidual A b C (symmetricMix w X) (mix w y) (symmetricMix w S) ≤
      4 * (sr + sc : ℕ) * B^2 * H^2 * ∑ i, (incidence D label i : ℝ) * (w i)^2 := by
  classical
  let a := coordinateMatrix e A
  let a' := fun i => coordinateMatrix e (A' i)
  let x := fun i => svec e (X i)
  let s := fun i => svec e (S i)
  have hp' (i : I) (r : R) : ∑ j, a' i r j * x i j = b r := by
    change (∑ j, coordinateMatrix e (A' i) r j * svec e (X i) j) = b r
    rw [← measurement_coordinates, hp i]
  have hd' (i : I) (j : J) : (∑ r, a' i r j * y i r) + s i j = svec e C j := by
    have h := congrArg (fun T => svec e T j) (hd i)
    simpa [svec_add, adjoint_coordinates, a', s] using h
  have hprimal : Mixture.residual a (mix w x) b = matrixChangeMix a a' x w := by
    funext r
    exact residual_mix_eq a a' x b w hw hp' r
  have hdual : stationarity a (mix w y) (mix w s) (svec e C) =
      matrixChangeMix (fun j r => a r j) (fun i j r => a' i r j) y w := by
    funext j
    rw [stationarity_mixture_identity w hw a a' y s _ hd' j]
    simp only [matrixChangeMix, Finset.mul_sum]
    exact Finset.sum_comm
  have hpb := matrixChangeMix_bound_on_positions a a' x w D label sr B H
    hB hH hA hA' hx hr hlocal
  have hdb := matrixChangeMix_bound_on_positions (fun j r => a r j)
    (fun i j r => a' i r j) y w (transposePositions D) (fun j r => label r j) sc B H
    hB hH (fun j r h => hA r j (by simpa [transposePositions] using h))
    (fun i j r h => hA' i r j (by simpa [transposePositions] using h)) hy hcol
    (fun i j r h => hlocal i r j (by simpa [transposePositions] using h))
  have hcost : (∑ i, (incidence (transposePositions D) (fun j r => label r j) i : ℝ) *
      (w i)^2) = ∑ i, (incidence D label i : ℝ) * (w i)^2 := by
    rw [← incidence_sum, ← incidence_sum]
    exact transpose_position_sum D (fun r j => (w (label r j))^2)
  rw [hcost] at hdb
  rw [sdpKktSqResidual_coordinates e, svec_mix, svec_mix]
  change kktSqResidual a b (svec e C) (mix w x) (mix w y) (mix w s) ≤ _
  unfold kktSqResidual
  rw [hprimal, hdual]
  have h := add_le_add hpb hdb
  push_cast
  nlinarith

/-- The manuscript's SDP constant follows from the sharper direct estimate. -/
theorem sdp_weighted_kkt_paper_bound [DecidableEq I] [DecidableEq J]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (C : SymmetricMatrix n)
    (w : I → ℝ) (D : R → Finset J) (label : R → J → I)
    (sr sc : ℕ) (B H : ℝ) (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j) :
    sdpKktSqResidual A b C (symmetricMix w X) (mix w y) (symmetricMix w S) ≤
      8 * (max sr (sc + 1) : ℕ) * (max B 1)^2 * H^2 *
        ∑ i, (incidence D label i : ℝ) * (w i)^2 := by
  apply (sdp_weighted_kkt_bound e A A' X S y b C w D label sr sc B H
    hw hB hH hA hA' hx hy hr hcol hp hd hlocal).trans
  have hs : sr + sc ≤ 2 * max sr (sc + 1) := by
    have := le_max_left sr (sc + 1)
    have := le_max_right sr (sc + 1)
    omega
  have hs' : ((sr + sc : ℕ) : ℝ) ≤ 2 * (max sr (sc + 1) : ℕ) := by
    exact_mod_cast hs
  have hb' : B^2 ≤ (max B 1)^2 := pow_le_pow_left₀ hB (le_max_left _ _) 2
  have hscale : 4 * ((sr + sc : ℕ) : ℝ) ≤ 8 * (max sr (sc + 1) : ℕ) := by linarith
  exact mul_le_mul_of_nonneg_right
    (mul_le_mul_of_nonneg_right
      (mul_le_mul hscale hb' (sq_nonneg B) (by positivity)) (sq_nonneg H)) (by positivity)

/-- Uniform single-flip residual theorem with the exact manuscript constant. -/
theorem sdp_uniform_kkt_paper_bound [DecidableEq J] [Nonempty I]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (C : SymmetricMatrix n)
    (D : R → Finset J) (label : R → J → I)
    (sr sc : ℕ) (B H : ℝ) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (transposePositions D j).card ≤ sc)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j) :
    Real.sqrt (sdpKktSqResidual A b C (symmetricMix (uniformWeight I) X)
      (mix (uniformWeight I) y) (symmetricMix (uniformWeight I) S)) ≤
      2 * max B 1 * H * Real.sqrt (2 * (max sr (sc + 1) : ℕ) * totalIncidence D) /
        Fintype.card I := by
  classical
  have hn : (Fintype.card I : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr Fintype.card_pos)
  have hh := sdp_weighted_kkt_paper_bound e A A' X S y b C (uniformWeight I)
    D label sr sc B H (uniformWeight_prob I) hB hH hA hA' hx hy hr hcol hp hd hlocal
  rw [← incidence_sum] at hh
  have hsum : (∑ r, ∑ j ∈ D r, (uniformWeight I (label r j)) ^ 2) =
      (totalIncidence D : ℝ) * ((Fintype.card I : ℝ)⁻¹) ^ 2 := by
    simp [uniformWeight, totalIncidence, Nat.cast_sum, Finset.sum_mul]
  rw [hsum] at hh
  apply Real.sqrt_le_iff.mpr
  constructor
  · positivity
  · have hr : Real.sqrt (2 * (max sr (sc + 1) : ℕ) * totalIncidence D)^2 =
        2 * (max sr (sc + 1) : ℕ) * totalIncidence D := Real.sq_sqrt (by positivity)
    calc
      _ ≤ _ := hh
      _ = _ := by rw [div_pow, mul_pow, mul_pow, mul_pow, hr]; field_simp; ring

end
end QipmFormal.SDPMixture
