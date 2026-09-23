import QipmFormal.Mixture.Defs
import Mathlib.Analysis.Matrix.Order

/-! # Matrix mixtures used in the semidefinite central-mixture results -/
namespace QipmFormal.SDPMixture
noncomputable section
open scoped BigOperators MatrixOrder

variable {I n : Type*} [Fintype I] [Fintype n] [DecidableEq n]

def matrixMix (w : I → ℝ) (X : I → Matrix n n ℝ) : Matrix n n ℝ :=
  ∑ i, w i • X i

def inverseMix (w : I → ℝ) (X : I → Matrix n n ℝ) : Matrix n n ℝ :=
  matrixMix w fun i => (X i)⁻¹

def centralMatrix (w : I → ℝ) (X : I → Matrix n n ℝ) : Matrix n n ℝ :=
  CFC.sqrt (matrixMix w X) * inverseMix w X * CFC.sqrt (matrixMix w X)

def variance (w : I → ℝ) (X : I → Matrix n n ℝ) : Matrix n n ℝ :=
  ∑ i, w i • ((X i - matrixMix w X) * (X i)⁻¹ * (X i - matrixMix w X))

end
end QipmFormal.SDPMixture
