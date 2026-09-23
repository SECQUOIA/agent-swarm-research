import Mathlib

/-!
# Scalar-dilation certificate: definitions

The `v`-coordinate transform of
`notes/central-path-cost/sections/03-sharp-centrality.tex`, equation
`eq:scalar-elementary`.  For `x > 0` and `v = √2 x / √(1+x²) ∈ (0,1)`,

  `Y v = 2 artanh v - √2 artanh (v/√2) = ρ x`,
  `A v = √(2-v²)/(1-v²) = p' (Y v)`,
  `P v = v * A v = p (Y v)`.

All statements in this development are phrased in the `v` coordinate.
-/

namespace QipmFormal.ScalarCert

open Real

/-- `Y v = 2 artanh v - √2 artanh (v / √2)`. -/
noncomputable def Y (v : ℝ) : ℝ := 2 * artanh v - √2 * artanh (v / √2)

/-- `A v = √(2 - v²) / (1 - v²)`. -/
noncomputable def A (v : ℝ) : ℝ := √(2 - v ^ 2) / (1 - v ^ 2)

/-- `P v = v * A v`. -/
noncomputable def P (v : ℝ) : ℝ := v * A v

end QipmFormal.ScalarCert
