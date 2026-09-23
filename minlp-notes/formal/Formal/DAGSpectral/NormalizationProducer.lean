import Formal.DAGSpectral.RangeNormalization
import Formal.DAGSpectral.RationalMatrixArithmetic

/-! Executable rational normalization agrees with the algebraic Gram inverse. -/
namespace DAGSpectral
open Matrix
variable {p r : ℕ}

def gramLeftInverseProducer (V : Matrix (Fin p) (Fin r) ℚ) : Matrix (Fin r) (Fin p) ℚ :=
  rationalMatrixInverse (Vᵀ * V) * Vᵀ

def rangeProjectorProducer (V : Matrix (Fin p) (Fin r) ℚ) : Matrix (Fin p) (Fin p) ℚ :=
  V * gramLeftInverseProducer V

def normalizerProducer (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ) :
    Matrix (Fin r) (Fin p) ℚ := diagonal τ * gramLeftInverseProducer V

def reconstructorProducer (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ) :
    Matrix (Fin p) (Fin r) ℚ := V * diagonal (fun i => (τ i)⁻¹)

def transformProducer (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ)
    (Q : Matrix (Fin p) (Fin p) ℚ) : Matrix (Fin r) (Fin r) ℚ :=
  normalizerProducer V τ * Q * (normalizerProducer V τ)ᵀ

@[simp] theorem gramLeftInverseProducer_eq (V : Matrix (Fin p) (Fin r) ℚ) :
    gramLeftInverseProducer V = gramLeftInverse V := by
  simp only [gramLeftInverseProducer, rationalMatrixInverse_eq, gramLeftInverse]

@[simp] theorem rangeProjectorProducer_eq (V : Matrix (Fin p) (Fin r) ℚ) :
    rangeProjectorProducer V = rangeProjector V := by
  simp only [rangeProjectorProducer, gramLeftInverseProducer_eq, rangeProjector]

@[simp] theorem normalizerProducer_eq (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ) :
    normalizerProducer V τ = normalizer V τ := by
  simp only [normalizerProducer, gramLeftInverseProducer_eq, normalizer]

@[simp] theorem reconstructorProducer_eq (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ) :
    reconstructorProducer V τ = reconstructor V τ := rfl

@[simp] theorem transformProducer_eq (V : Matrix (Fin p) (Fin r) ℚ) (τ : Fin r → ℚ)
    (Q : Matrix (Fin p) (Fin p) ℚ) :
    transformProducer V τ Q = normalizer V τ * Q * (normalizer V τ)ᵀ := by
  simp only [transformProducer, normalizerProducer_eq]

/-- Executable identities have only full-column-rank and nonzero-scale premises. -/
theorem normalizationProducer_leftInverse (V : Matrix (Fin p) (Fin r) ℚ)
    (hV : Function.Injective V.mulVec) (τ : Fin r → ℚ) (hτ : ∀ i, τ i ≠ 0) :
    normalizerProducer V τ * reconstructorProducer V τ = 1 := by
  simpa only [normalizerProducer_eq, reconstructorProducer_eq] using
    normalizer_reconstructor V hV τ hτ

theorem normalizationProducer_reconstruct (V : Matrix (Fin p) (Fin r) ℚ)
    (τ : Fin r → ℚ) (hτ : ∀ i, τ i ≠ 0)
    (Q : Matrix (Fin p) (Fin p) ℚ) (hQ : Qᵀ = Q)
    (hrange : rangeProjectorProducer V * Q = Q) :
    reconstructorProducer V τ * transformProducer V τ Q * (reconstructorProducer V τ)ᵀ = Q := by
  simpa only [reconstructorProducer_eq, transformProducer_eq] using
    reconstruct_retained V τ hτ Q hQ (by simpa only [rangeProjectorProducer_eq] using hrange)

end DAGSpectral
