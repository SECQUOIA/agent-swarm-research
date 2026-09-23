import QipmFormal.Mixture.Incidence
import QipmFormal.SDPMixture.Residual
import QipmFormal.SDPMixture.Decoder
import QipmFormal.SDPMixture.Centrality
import QipmFormal.SDPMixture.NormBounds
import QipmFormal.SDPMixture.Frobenius
import QipmFormal.SDPMixture.Sandwich
import QipmFormal.SDPMixture.VarianceBounds

/-!
# SDP central-mixture soundness

The output contracts use actual positive-definite matrix triples, their
algebraic objective gap, the stacked measurement residual, and the actual
normalized complementarity matrix. Both centering conventions and both
Euclidean operator and Frobenius norms are covered.
-/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators MatrixOrder Matrix.Norms.L2Operator

variable {I n J R : Type*} [Fintype I] [Fintype n] [DecidableEq n]
  [Fintype J] [Fintype R]

/-- A sound SDP output contract, with its centering parameter and matrix norm
specified explicitly. The gap remains `r μ` under either convention. -/
def SDPOutputSound (A : R → SymmetricMatrix n) (b : R → ℝ) (C : SymmetricMatrix n)
    (μ ε θ : ℝ) (ν : Matrix n n ℝ → ℝ)
    (center : Matrix n n ℝ → Matrix n n ℝ → ℝ)
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop) : Prop :=
  ∀ X y S, (toMatrix X).PosDef → (toMatrix S).PosDef →
    Matrix.trace (toMatrix C * toMatrix X) - Mixture.dot b y =
      (Fintype.card n : ℝ) * μ →
    Real.sqrt (sdpKktSqResidual A b C X y S) ≤ ε →
    ν (sdpDefect (toMatrix X) (toMatrix S) (center (toMatrix X) (toMatrix S))) ≤ θ →
    ¬ Wrong X y S

abbrev CentralOutputSound (A : R → SymmetricMatrix n) (b : R → ℝ) (C : SymmetricMatrix n)
    (μ ε θ : ℝ) (ν : Matrix n n ℝ → ℝ)
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop) : Prop :=
  SDPOutputSound A b C μ ε θ ν (fun _ _ => μ) Wrong

abbrev PointCenteredOutputSound (A : R → SymmetricMatrix n) (b : R → ℝ) (C : SymmetricMatrix n)
    (μ ε θ : ℝ) (ν : Matrix n n ℝ → ℝ)
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop) : Prop :=
  SDPOutputSound A b C μ ε θ ν pointParameter Wrong

/-- Assemble the actual matrix certificate. This lemma isolates the two
numerical estimates; the following theorems supply them from raw data. -/
theorem soundness_from_bounds
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q κ : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hX : ∀ i, (toMatrix (X i)).PosDef)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y) (symmetricMix w S) ≤ Q)
    (ν : Matrix n n ℝ → ℝ) (center : Matrix n n ℝ → Matrix n n ℝ → ℝ)
    (hwidth : ν (sdpDefect (toMatrix (symmetricMix w X))
      (toMatrix (symmetricMix w S))
      (center (toMatrix (symmetricMix w X)) (toMatrix (symmetricMix w S)))) ≤ κ)
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix w X) (Mixture.mix w y) (symmetricMix w S))
    (hsound : SDPOutputSound A b C μ ε θ ν center Wrong) :
    ε ^ 2 < Q ∨ θ < κ := by
  by_contra h
  push Not at h
  have hXm : (toMatrix (symmetricMix w X)).PosDef := by
    rw [toMatrix_mix]
    exact matrixMix_posDef hw hX
  have hSm : (toMatrix (symmetricMix w S)).PosDef := by
    rw [toMatrix_mix]
    apply matrixMix_posDef hw
    intro i
    rw [hc i]
    exact (hX i).inv.smul hμ
  exact hsound _ _ _ hXm hSm
    (sdp_mixture_objective_gap e A' X S C b y μ w hw hp hd hX hc)
    (Real.sqrt_le_iff.mpr ⟨hε, hbound.trans h.1⟩) (hwidth.trans h.2) hwrong

/-- The scalar sandwich constant minus one in the spectral-ratio form. -/
theorem sandwich_width_identity (m M : ℝ) (hm : 0 < m) (hM : 0 < M) :
    (m + M)^2 / (4 * m * M) - 1 = (M / m - 1)^2 / (4 * (M / m)) := by
  field_simp [hm.ne', hM.ne']
  ring

/-- Kantorovich bounds the common-parameter operator defect. -/
theorem mixture_opNorm_le
    (w : I → ℝ) (hw : Mixture.ProbWeights w) (X : I → Matrix n n ℝ)
    (m M : ℝ) (hm : 0 < m) (hmM : m ≤ M)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ)) :
    opNorm (centralMatrix w X - 1) ≤ (M / m - 1)^2 / (4 * (M / m)) := by
  have hM := hm.trans_le hmM
  have hK : 1 ≤ (m + M)^2 / (4 * m * M) := by
    apply (le_div_iff₀ (by positivity : 0 < 4 * m * M)).mpr
    nlinarith [sq_nonneg (M - m)]
  rw [← sandwich_width_identity m M hm hM]
  exact opNorm_defect_le (one_le_centralMatrix hw fun i => posDef_of_scalar_lower hm (hlo i))
    (centralMatrix_le hw hm hmM hlo hhi) hK

/-- The dimension factor in the Frobenius sandwich bound is `sqrt r`. -/
theorem mixture_frobeniusNorm_le
    (w : I → ℝ) (hw : Mixture.ProbWeights w) (X : I → Matrix n n ℝ)
    (m M : ℝ) (hm : 0 < m) (hmM : m ≤ M)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ)) :
    frobeniusNorm (centralMatrix w X - 1) ≤
      Real.sqrt (Fintype.card n) * ((M / m - 1)^2 / (4 * (M / m))) :=
  (frobeniusNorm_le_sqrt_card_mul_opNorm _).trans
    (mul_le_mul_of_nonneg_left (mixture_opNorm_le w hw X m M hm hmM hlo hhi)
      (Real.sqrt_nonneg _))

/-- Actual common and point-centered operator widths obey the same bound. -/
theorem actual_operator_widths [Nonempty n]
    (w : I → ℝ) (hw : Mixture.ProbWeights w) (X S : I → Matrix n n ℝ)
    (μ m M : ℝ) (hμ : 0 < μ) (hm : 0 < m) (hmM : m ≤ M)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ))
    (hc : ∀ i, S i = μ • (X i)⁻¹) :
    opNorm (sdpDefect (matrixMix w X) (matrixMix w S) μ) ≤
      (M / m - 1)^2 / (4 * (M / m)) ∧
    opNorm (sdpDefect (matrixMix w X) (matrixMix w S)
      (pointParameter (matrixMix w X) (matrixMix w S))) ≤
      (M / m - 1)^2 / (4 * (M / m)) := by
  have hX : ∀ i, (X i).PosDef := fun i => posDef_of_scalar_lower hm (hlo i)
  have hb := mixture_opNorm_le w hw X m M hm hmM hlo hhi
  constructor
  · rw [sdpDefect_mixture hw hμ hX hc]
    exact hb
  · rw [sdpDefect_mixture_point hw hμ hX hc]
    exact (opNorm_recentered_le (sub_nonneg.mpr (one_le_centralMatrix hw hX))).trans hb

/-- Actual common and point-centered Frobenius widths obey the same bound. -/
theorem actual_frobenius_widths [Nonempty n]
    (w : I → ℝ) (hw : Mixture.ProbWeights w) (X S : I → Matrix n n ℝ)
    (μ m M : ℝ) (hμ : 0 < μ) (hm : 0 < m) (hmM : m ≤ M)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ X i)
    (hhi : ∀ i, X i ≤ M • (1 : Matrix n n ℝ))
    (hc : ∀ i, S i = μ • (X i)⁻¹) :
    frobeniusNorm (sdpDefect (matrixMix w X) (matrixMix w S) μ) ≤
      Real.sqrt (Fintype.card n) * ((M / m - 1)^2 / (4 * (M / m))) ∧
    frobeniusNorm (sdpDefect (matrixMix w X) (matrixMix w S)
      (pointParameter (matrixMix w X) (matrixMix w S))) ≤
      Real.sqrt (Fintype.card n) * ((M / m - 1)^2 / (4 * (M / m))) := by
  have hX : ∀ i, (X i).PosDef := fun i => posDef_of_scalar_lower hm (hlo i)
  have hb := mixture_frobeniusNorm_le w hw X m M hm hmM hlo hhi
  constructor
  · rw [sdpDefect_mixture hw hμ hX hc]
    exact hb
  · rw [sdpDefect_mixture_point hw hμ hX hc]
    exact (frobeniusNorm_recentered_le _
      (Matrix.le_iff.mp (one_le_centralMatrix hw hX))).trans hb

/-- A width estimate for both actual centering conventions gives the same
strict soundness alternative under either output contract. -/
theorem soundness_either_centering
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q κ : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε)
    (hX : ∀ i, (toMatrix (X i)).PosDef)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y)
      (symmetricMix w S) ≤ Q)
    (ν : Matrix n n ℝ → ℝ)
    (hwidth : ν (sdpDefect (matrixMix w (fun i => toMatrix (X i)))
      (matrixMix w (fun i => toMatrix (S i))) μ) ≤ κ ∧
      ν (sdpDefect (matrixMix w (fun i => toMatrix (X i)))
        (matrixMix w (fun i => toMatrix (S i)))
        (pointParameter (matrixMix w (fun i => toMatrix (X i)))
          (matrixMix w (fun i => toMatrix (S i))))) ≤ κ)
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix w X) (Mixture.mix w y) (symmetricMix w S))
    (hsound : CentralOutputSound A b C μ ε θ ν Wrong ∨
      PointCenteredOutputSound A b C μ ε θ ν Wrong) :
    ε ^ 2 < Q ∨ θ < κ := by
  rcases hsound with hs | hs
  · exact soundness_from_bounds e w hw A A' b C X S y μ ε θ Q κ hμ hε hX hp hd hc
      hbound ν (fun _ _ => μ) (by simpa only [toMatrix_mix, matrixMix] using hwidth.1)
      Wrong hwrong hs
  · exact soundness_from_bounds e w hw A A' b C X S y μ ε θ Q κ hμ hε hX hp hd hc
      hbound ν pointParameter (by simpa only [toMatrix_mix, matrixMix] using hwidth.2)
      Wrong hwrong hs

/-- Operator phase boundary from actual neighboring centers and any certified
stacked residual bound. -/
theorem operator_soundness_dichotomy [Nonempty n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y)
      (symmetricMix w S) ≤ Q)
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix w X) (Mixture.mix w y) (symmetricMix w S))
    (hsound : CentralOutputSound A b C μ ε θ opNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ opNorm Wrong) :
    ε ^ 2 < Q ∨ θ < (M / m - 1)^2 / (4 * (M / m)) :=
  soundness_either_centering e w hw A A' b C X S y μ ε θ Q _ hμ hε
    (fun i => posDef_of_scalar_lower hm (hlo i)) hp hd hc hbound opNorm
    (actual_operator_widths w hw _ _ μ m M hμ hm hmM hlo hhi hc) Wrong hwrong hsound

/-- Frobenius phase boundary, including point-centered neighborhoods. -/
theorem frobenius_soundness_dichotomy [Nonempty n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y)
      (symmetricMix w S) ≤ Q)
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix w X) (Mixture.mix w y) (symmetricMix w S))
    (hsound : CentralOutputSound A b C μ ε θ frobeniusNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ frobeniusNorm Wrong) :
    ε ^ 2 < Q ∨ θ < Real.sqrt (Fintype.card n) * ((M / m - 1)^2 / (4 * (M / m))) :=
  soundness_either_centering e w hw A A' b C X S y μ ε θ Q _ hμ hε
    (fun i => posDef_of_scalar_lower hm (hlo i)) hp hd hc hbound frobeniusNorm
    (actual_frobenius_widths w hw _ _ μ m M hμ hm hmM hlo hhi hc) Wrong hwrong hsound

/-- Complete weighted operator phase boundary from the one-bit-local
measurement data and exact neighboring SDP centers. -/
theorem weighted_operator_soundness_dichotomy [DecidableEq J] [Nonempty n]
    [DecidableEq I]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (C : SymmetricMatrix n)
    (w : I → ℝ) (D : R → Finset J) (label : R → J → I)
    (sr sc : ℕ) (B H : ℝ) (hw : Mixture.ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (Mixture.transposePositions D j).card ≤ sc)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j)
    (μ ε θ m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix w X)
      (Mixture.mix w y)
      (symmetricMix w S))
    (hsound : CentralOutputSound A b C μ ε θ opNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ opNorm Wrong) :
    ε ^ 2 < 4 * (sr + sc : ℕ) * B^2 * H^2 *
      ∑ i, (Mixture.incidence D label i : ℝ) * (w i)^2 ∨
      θ < ((M / m - 1)^2 / (4 * (M / m))) := by
  exact operator_soundness_dichotomy e w hw A A' b C X S y μ ε θ _ m M hμ hε hm hmM
    hp hd hc hlo hhi
    (sdp_weighted_kkt_bound e A A' X S y b C w D label sr sc B H hw hB hH
      hA hA' hx hy hr hcol hp hd hlocal) Wrong hwrong hsound

/-- Complete uniform operator phase boundary from the one-bit-local
measurement data and exact neighboring SDP centers. -/
theorem uniform_operator_soundness_dichotomy [DecidableEq J] [Nonempty n]
    [Nonempty I]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (C : SymmetricMatrix n)
    (D : R → Finset J) (label : R → J → I)
    (sr sc : ℕ) (B H : ℝ) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (Mixture.transposePositions D j).card ≤ sc)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j)
    (μ ε θ m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix (Mixture.uniformWeight I) X)
      (Mixture.mix (Mixture.uniformWeight I) y)
      (symmetricMix (Mixture.uniformWeight I) S))
    (hsound : CentralOutputSound A b C μ ε θ opNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ opNorm Wrong) :
    ε ^ 2 < 8 * (max sr (sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      Mixture.totalIncidence D / (Fintype.card I : ℝ)^2 ∨
      θ < ((M / m - 1)^2 / (4 * (M / m))) := by
  classical
  have hb := sdp_weighted_kkt_paper_bound e A A' X S y b C (Mixture.uniformWeight I)
    D label sr sc B H (Mixture.uniformWeight_prob I) hB hH hA hA' hx hy hr hcol hp hd hlocal
  have hsum : (∑ i, (Mixture.incidence D label i : ℝ)) = Mixture.totalIncidence D := by
    have hh := Mixture.incidence_sum D label (fun _ => (1 : ℝ))
    simpa [Mixture.totalIncidence] using hh.symm
  rw [Mixture.uniform_incidence_cost, hsum] at hb
  have heq : 8 * (max sr (sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      ((Mixture.totalIncidence D : ℝ) / (Fintype.card I : ℝ)^2) =
      8 * (max sr (sc + 1) : ℕ) * (max B 1)^2 * H^2 *
        Mixture.totalIncidence D / (Fintype.card I : ℝ)^2 := by ring
  rw [heq] at hb
  exact operator_soundness_dichotomy e (Mixture.uniformWeight I) (Mixture.uniformWeight_prob I)
    A A' b C X S y μ ε θ _ m M hμ hε hm hmM hp hd hc hlo hhi hb Wrong hwrong hsound

/-- Complete weighted frobenius phase boundary from the one-bit-local
measurement data and exact neighboring SDP centers. -/
theorem weighted_frobenius_soundness_dichotomy [DecidableEq J] [Nonempty n]
    [DecidableEq I]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (C : SymmetricMatrix n)
    (w : I → ℝ) (D : R → Finset J) (label : R → J → I)
    (sr sc : ℕ) (B H : ℝ) (hw : Mixture.ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (Mixture.transposePositions D j).card ≤ sc)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j)
    (μ ε θ m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix w X)
      (Mixture.mix w y)
      (symmetricMix w S))
    (hsound : CentralOutputSound A b C μ ε θ frobeniusNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ frobeniusNorm Wrong) :
    ε ^ 2 < 4 * (sr + sc : ℕ) * B^2 * H^2 *
      ∑ i, (Mixture.incidence D label i : ℝ) * (w i)^2 ∨
      θ < Real.sqrt (Fintype.card n) * ((M / m - 1)^2 / (4 * (M / m))) := by
  exact frobenius_soundness_dichotomy e w hw A A' b C X S y μ ε θ _ m M hμ hε hm hmM
    hp hd hc hlo hhi
    (sdp_weighted_kkt_bound e A A' X S y b C w D label sr sc B H hw hB hH
      hA hA' hx hy hr hcol hp hd hlocal) Wrong hwrong hsound

/-- Complete uniform frobenius phase boundary from the one-bit-local
measurement data and exact neighboring SDP centers. -/
theorem uniform_frobenius_soundness_dichotomy [DecidableEq J] [Nonempty n]
    [Nonempty I]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (C : SymmetricMatrix n)
    (D : R → Finset J) (label : R → J → I)
    (sr sc : ℕ) (B H : ℝ) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (Mixture.transposePositions D j).card ≤ sc)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j)
    (μ ε θ m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix (Mixture.uniformWeight I) X)
      (Mixture.mix (Mixture.uniformWeight I) y)
      (symmetricMix (Mixture.uniformWeight I) S))
    (hsound : CentralOutputSound A b C μ ε θ frobeniusNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ frobeniusNorm Wrong) :
    ε ^ 2 < 8 * (max sr (sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      Mixture.totalIncidence D / (Fintype.card I : ℝ)^2 ∨
      θ < Real.sqrt (Fintype.card n) * ((M / m - 1)^2 / (4 * (M / m))) := by
  classical
  have hb := sdp_weighted_kkt_paper_bound e A A' X S y b C (Mixture.uniformWeight I)
    D label sr sc B H (Mixture.uniformWeight_prob I) hB hH hA hA' hx hy hr hcol hp hd hlocal
  have hsum : (∑ i, (Mixture.incidence D label i : ℝ)) = Mixture.totalIncidence D := by
    have hh := Mixture.incidence_sum D label (fun _ => (1 : ℝ))
    simpa [Mixture.totalIncidence] using hh.symm
  rw [Mixture.uniform_incidence_cost, hsum] at hb
  have heq : 8 * (max sr (sc + 1) : ℕ) * (max B 1)^2 * H^2 *
      ((Mixture.totalIncidence D : ℝ) / (Fintype.card I : ℝ)^2) =
      8 * (max sr (sc + 1) : ℕ) * (max B 1)^2 * H^2 *
        Mixture.totalIncidence D / (Fintype.card I : ℝ)^2 := by ring
  rw [heq] at hb
  exact frobenius_soundness_dichotomy e (Mixture.uniformWeight I) (Mixture.uniformWeight_prob I)
    A A' b C X S y μ ε θ _ m M hμ hε hm hmM hp hd hc hlo hhi hb Wrong hwrong hsound

/-- The affine neighbor margins instantiate the operator soundness contract. -/
theorem affine_operator_soundness_dichotomy [Nonempty n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y)
      (symmetricMix w S) ≤ Q)
    (AX AS : Matrix n n ℝ) (ay : R → ℝ) (a₀ p γ : ℝ)
    (hmargin : ∀ i, p * matrixTripleScore AX AS ay a₀ (toMatrix (X i)) (y i)
      (toMatrix (S i)) ≤ -γ)
    (hsound : CentralOutputSound A b C μ ε θ opNorm
      (fun X y S => p * matrixTripleScore AX AS ay a₀ (toMatrix X) y (toMatrix S) ≤ -γ) ∨
      PointCenteredOutputSound A b C μ ε θ opNorm
      (fun X y S => p * matrixTripleScore AX AS ay a₀ (toMatrix X) y (toMatrix S) ≤ -γ)) :
    ε ^ 2 < Q ∨ θ < ((M / m - 1)^2 / (4 * (M / m))) := by
  apply operator_soundness_dichotomy e w hw A A' b C X S y μ ε θ Q m M hμ hε hm hmM
    hp hd hc hlo hhi hbound _ _ hsound
  simpa only [toMatrix_mix, matrixMix] using
    matrixTripleScore_wrong_mix w hw AX AS ay a₀ p γ
      (fun i => toMatrix (X i)) (fun i => toMatrix (S i)) y hmargin

/-- The observable neighbor margins instantiate the operator soundness contract. -/
theorem observable_operator_soundness_dichotomy [Nonempty n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y)
      (symmetricMix w S) ≤ Q)
    (O : Matrix n n ℝ) (p γ : ℝ)
    (hOlo : -(1 : Matrix n n ℝ) ≤ O) (hOhi : O ≤ 1)
    (hmargin : ∀ i, γ * (toMatrix (X i)).trace ≤ p * (O * toMatrix (X i)).trace)
    (hsound : CentralOutputSound A b C μ ε θ opNorm
      (fun X _ _ => 0 ≤ plusProbability O (toMatrix X) ∧
        plusProbability O (toMatrix X) ≤ 1 ∧ γ ≤ p * observableExpectation O (toMatrix X)) ∨
      PointCenteredOutputSound A b C μ ε θ opNorm
      (fun X _ _ => 0 ≤ plusProbability O (toMatrix X) ∧
        plusProbability O (toMatrix X) ≤ 1 ∧ γ ≤ p * observableExpectation O (toMatrix X))) :
    ε ^ 2 < Q ∨ θ < ((M / m - 1)^2 / (4 * (M / m))) := by
  apply operator_soundness_dichotomy e w hw A A' b C X S y μ ε θ Q m M hμ hε hm hmM
    hp hd hc hlo hhi hbound _ _ hsound
  have hXm : (matrixMix w (fun i => toMatrix (X i))).PosDef :=
    matrixMix_posDef hw fun i => posDef_of_scalar_lower hm (hlo i)
  have hv := plusProbability_valid hXm.posSemidef hXm.trace_pos hOlo hOhi
  have hmarg := observable_normalized_margin_mix w hw (fun i => toMatrix (X i))
    O p γ hXm.trace_pos hmargin
  simpa only [toMatrix_mix, matrixMix] using And.intro hv.1 (And.intro hv.2 hmarg)

/-- The affine neighbor margins instantiate the frobenius soundness contract. -/
theorem affine_frobenius_soundness_dichotomy [Nonempty n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y)
      (symmetricMix w S) ≤ Q)
    (AX AS : Matrix n n ℝ) (ay : R → ℝ) (a₀ p γ : ℝ)
    (hmargin : ∀ i, p * matrixTripleScore AX AS ay a₀ (toMatrix (X i)) (y i)
      (toMatrix (S i)) ≤ -γ)
    (hsound : CentralOutputSound A b C μ ε θ frobeniusNorm
      (fun X y S => p * matrixTripleScore AX AS ay a₀ (toMatrix X) y (toMatrix S) ≤ -γ) ∨
      PointCenteredOutputSound A b C μ ε θ frobeniusNorm
      (fun X y S => p * matrixTripleScore AX AS ay a₀ (toMatrix X) y (toMatrix S) ≤ -γ)) :
    ε ^ 2 < Q ∨ θ < Real.sqrt (Fintype.card n) * ((M / m - 1)^2 / (4 * (M / m))) := by
  apply frobenius_soundness_dichotomy e w hw A A' b C X S y μ ε θ Q m M hμ hε hm hmM
    hp hd hc hlo hhi hbound _ _ hsound
  simpa only [toMatrix_mix, matrixMix] using
    matrixTripleScore_wrong_mix w hw AX AS ay a₀ p γ
      (fun i => toMatrix (X i)) (fun i => toMatrix (S i)) y hmargin

/-- The observable neighbor margins instantiate the frobenius soundness contract. -/
theorem observable_frobenius_soundness_dichotomy [Nonempty n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y)
      (symmetricMix w S) ≤ Q)
    (O : Matrix n n ℝ) (p γ : ℝ)
    (hOlo : -(1 : Matrix n n ℝ) ≤ O) (hOhi : O ≤ 1)
    (hmargin : ∀ i, γ * (toMatrix (X i)).trace ≤ p * (O * toMatrix (X i)).trace)
    (hsound : CentralOutputSound A b C μ ε θ frobeniusNorm
      (fun X _ _ => 0 ≤ plusProbability O (toMatrix X) ∧
        plusProbability O (toMatrix X) ≤ 1 ∧ γ ≤ p * observableExpectation O (toMatrix X)) ∨
      PointCenteredOutputSound A b C μ ε θ frobeniusNorm
      (fun X _ _ => 0 ≤ plusProbability O (toMatrix X) ∧
        plusProbability O (toMatrix X) ≤ 1 ∧ γ ≤ p * observableExpectation O (toMatrix X))) :
    ε ^ 2 < Q ∨ θ < Real.sqrt (Fintype.card n) * ((M / m - 1)^2 / (4 * (M / m))) := by
  apply frobenius_soundness_dichotomy e w hw A A' b C X S y μ ε θ Q m M hμ hε hm hmM
    hp hd hc hlo hhi hbound _ _ hsound
  have hXm : (matrixMix w (fun i => toMatrix (X i))).PosDef :=
    matrixMix_posDef hw fun i => posDef_of_scalar_lower hm (hlo i)
  have hv := plusProbability_valid hXm.posSemidef hXm.trace_pos hOlo hOhi
  have hmarg := observable_normalized_margin_mix w hw (fun i => toMatrix (X i))
    O p γ hXm.trace_pos hmargin
  simpa only [toMatrix_mix, matrixMix] using And.intro hv.1 (And.intro hv.2 hmarg)

/-- Additive variance replaces the global ratio in the operator phase
boundary. No upper spectral bound is needed. -/
theorem operator_variance_soundness_dichotomy [Nonempty n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q m : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y)
      (symmetricMix w S) ≤ Q)
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix w X) (Mixture.mix w y) (symmetricMix w S))
    (hsound : CentralOutputSound A b C μ ε θ opNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ opNorm Wrong) :
    ε ^ 2 < Q ∨ θ < m⁻¹ ^ 2 * ∑ i, w i *
      opNorm (toMatrix (X i) - matrixMix w (fun j => toMatrix (X j)))^2 := by
  have hX : ∀ i, (toMatrix (X i)).PosDef := fun i => posDef_of_scalar_lower hm (hlo i)
  apply soundness_either_centering e w hw A A' b C X S y μ ε θ Q _ hμ hε hX
    hp hd hc hbound opNorm _ Wrong hwrong hsound
  constructor
  · rw [sdpDefect_mixture hw hμ hX hc]
    exact centralMatrix_operator_variance_bound hw hm hlo
  · rw [sdpDefect_mixture_point hw hμ hX hc]
    exact recentered_operator_variance_bound hw hm hlo

/-- Additive variance replaces the global ratio in the frobenius phase
boundary. No upper spectral bound is needed. -/
theorem frobenius_variance_soundness_dichotomy [Nonempty n]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (w : I → ℝ) (hw : Mixture.ProbWeights w)
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (b : R → ℝ) (C : SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ)
    (μ ε θ Q m : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hbound : sdpKktSqResidual A b C (symmetricMix w X) (Mixture.mix w y)
      (symmetricMix w S) ≤ Q)
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix w X) (Mixture.mix w y) (symmetricMix w S))
    (hsound : CentralOutputSound A b C μ ε θ frobeniusNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ frobeniusNorm Wrong) :
    ε ^ 2 < Q ∨ θ < m⁻¹ ^ 2 * ∑ i, w i *
      frobeniusNorm (toMatrix (X i) - matrixMix w (fun j => toMatrix (X j)))^2 := by
  have hX : ∀ i, (toMatrix (X i)).PosDef := fun i => posDef_of_scalar_lower hm (hlo i)
  apply soundness_either_centering e w hw A A' b C X S y μ ε θ Q _ hμ hε hX
    hp hd hc hbound frobeniusNorm _ Wrong hwrong hsound
  constructor
  · rw [sdpDefect_mixture hw hμ hX hc]
    exact centralMatrix_frobenius_variance_bound hw hm hlo
  · rw [sdpDefect_mixture_point hw hμ hX hc]
    exact recentered_frobenius_variance_bound hw hm hlo

/-- Sharper uniform operator phase boundary from the one-bit-local
measurement data and exact neighboring SDP centers. -/
theorem uniform_sharp_operator_soundness_dichotomy [DecidableEq J] [Nonempty n]
    [Nonempty I]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (C : SymmetricMatrix n)
    (D : R → Finset J) (label : R → J → I)
    (sr sc : ℕ) (B H : ℝ) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (Mixture.transposePositions D j).card ≤ sc)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j)
    (μ ε θ m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix (Mixture.uniformWeight I) X)
      (Mixture.mix (Mixture.uniformWeight I) y)
      (symmetricMix (Mixture.uniformWeight I) S))
    (hsound : CentralOutputSound A b C μ ε θ opNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ opNorm Wrong) :
    ε ^ 2 < 4 * (sr + sc : ℕ) * B^2 * H^2 *
      Mixture.totalIncidence D / (Fintype.card I : ℝ)^2 ∨
      θ < ((M / m - 1)^2 / (4 * (M / m))) := by
  classical
  have hb := sdp_weighted_kkt_bound e A A' X S y b C (Mixture.uniformWeight I)
    D label sr sc B H (Mixture.uniformWeight_prob I) hB hH hA hA' hx hy hr hcol hp hd hlocal
  have hsum : (∑ i, (Mixture.incidence D label i : ℝ)) = Mixture.totalIncidence D := by
    have hh := Mixture.incidence_sum D label (fun _ => (1 : ℝ))
    simpa [Mixture.totalIncidence] using hh.symm
  rw [Mixture.uniform_incidence_cost, hsum] at hb
  have heq : 4 * (sr + sc : ℕ) * B^2 * H^2 *
      ((Mixture.totalIncidence D : ℝ) / (Fintype.card I : ℝ)^2) =
      4 * (sr + sc : ℕ) * B^2 * H^2 *
        Mixture.totalIncidence D / (Fintype.card I : ℝ)^2 := by ring
  rw [heq] at hb
  exact operator_soundness_dichotomy e (Mixture.uniformWeight I) (Mixture.uniformWeight_prob I)
    A A' b C X S y μ ε θ _ m M hμ hε hm hmM hp hd hc hlo hhi hb Wrong hwrong hsound


/-- Sharper uniform frobenius phase boundary from the one-bit-local
measurement data and exact neighboring SDP centers. -/
theorem uniform_sharp_frobenius_soundness_dichotomy [DecidableEq J] [Nonempty n]
    [Nonempty I]
    (e : OrthonormalBasis J ℝ (SymmetricMatrix n))
    (A : R → SymmetricMatrix n) (A' : I → R → SymmetricMatrix n)
    (X S : I → SymmetricMatrix n) (y : I → R → ℝ) (b : R → ℝ) (C : SymmetricMatrix n)
    (D : R → Finset J) (label : R → J → I)
    (sr sc : ℕ) (B H : ℝ) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, j ∈ D r → |coordinateMatrix e A r j| ≤ B)
    (hA' : ∀ i r j, j ∈ D r → |coordinateMatrix e (A' i) r j| ≤ B)
    (hx : ∀ i j, |svec e (X i) j| ≤ H) (hy : ∀ i r, |y i r| ≤ H)
    (hr : ∀ r, (D r).card ≤ sr) (hcol : ∀ j, (Mixture.transposePositions D j).card ≤ sc)
    (hp : ∀ i, measurement (A' i) (X i) = b)
    (hd : ∀ i, measurementAdjoint (A' i) (y i) + S i = C)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i →
      coordinateMatrix e (A' i) r j = coordinateMatrix e A r j)
    (μ ε θ m M : ℝ) (hμ : 0 < μ) (hε : 0 ≤ ε) (hm : 0 < m) (hmM : m ≤ M)
    (hc : ∀ i, toMatrix (S i) = μ • (toMatrix (X i))⁻¹)
    (hlo : ∀ i, m • (1 : Matrix n n ℝ) ≤ toMatrix (X i))
    (hhi : ∀ i, toMatrix (X i) ≤ M • (1 : Matrix n n ℝ))
    (Wrong : SymmetricMatrix n → (R → ℝ) → SymmetricMatrix n → Prop)
    (hwrong : Wrong (symmetricMix (Mixture.uniformWeight I) X)
      (Mixture.mix (Mixture.uniformWeight I) y)
      (symmetricMix (Mixture.uniformWeight I) S))
    (hsound : CentralOutputSound A b C μ ε θ frobeniusNorm Wrong ∨
      PointCenteredOutputSound A b C μ ε θ frobeniusNorm Wrong) :
    ε ^ 2 < 4 * (sr + sc : ℕ) * B^2 * H^2 *
      Mixture.totalIncidence D / (Fintype.card I : ℝ)^2 ∨
      θ < Real.sqrt (Fintype.card n) * ((M / m - 1)^2 / (4 * (M / m))) := by
  classical
  have hb := sdp_weighted_kkt_bound e A A' X S y b C (Mixture.uniformWeight I)
    D label sr sc B H (Mixture.uniformWeight_prob I) hB hH hA hA' hx hy hr hcol hp hd hlocal
  have hsum : (∑ i, (Mixture.incidence D label i : ℝ)) = Mixture.totalIncidence D := by
    have hh := Mixture.incidence_sum D label (fun _ => (1 : ℝ))
    simpa [Mixture.totalIncidence] using hh.symm
  rw [Mixture.uniform_incidence_cost, hsum] at hb
  have heq : 4 * (sr + sc : ℕ) * B^2 * H^2 *
      ((Mixture.totalIncidence D : ℝ) / (Fintype.card I : ℝ)^2) =
      4 * (sr + sc : ℕ) * B^2 * H^2 *
        Mixture.totalIncidence D / (Fintype.card I : ℝ)^2 := by ring
  rw [heq] at hb
  exact frobenius_soundness_dichotomy e (Mixture.uniformWeight I) (Mixture.uniformWeight_prob I)
    A A' b C X S y μ ε θ _ m M hμ hε hm hmM hp hd hc hlo hhi hb Wrong hwrong hsound


end
end QipmFormal.SDPMixture
