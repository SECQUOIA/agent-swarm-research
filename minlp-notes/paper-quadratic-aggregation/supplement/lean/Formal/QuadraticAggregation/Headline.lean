import Formal.QuadraticAggregation.Coefficients
import Formal.QuadraticAggregation.LimitCompactness
import Formal.QuadraticAggregation.SweepBounds
import Formal.QuadraticAggregation.Hyperplanes
import Formal.QuadraticAggregation.EasyDirection
import Formal.QuadraticAggregation.DefinitionsSequence

/-!
# Aggregation certificates for a proper quadratic hull

The theorem starts from the original coefficients, strict feasibility, and
asymptotic hyperplane convexity. All separation and limiting certificates are
constructed in the proof. The constant term is eliminated at one feasible
point before a single compactness argument on the actual coefficient cone.
-/

open Filter Set
open scoped BigOperators Matrix Matrix.Norms.Elementwise Topology

namespace QuadraticAggregation.System
variable {n m : ℕ}

/-- The difficult implication: a proper hull admits a nontrivial globally
convex quadratic aggregation under asymptotic hyperplane convexity. -/
theorem exists_certificate_of_proper (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHC)
    (hproper : convexHull ℝ D.feasible ≠ Set.univ) :
    ∃ w, D.Certificate w := by
  classical
  obtain ⟨x₀, hx₀⟩ := hS
  obtain ⟨α, hα, hcert⟩ := D.exists_unbounded_certificates ⟨x₀, hx₀⟩ hproper hHC
  have hseq : ∀ k : ℕ, ∃ s : ℝ, (k : ℝ) < s ∧ 0 < s ∧
      ∃ w : Vec m, (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧
        ∀ x : Vec n, 0 ≤ q (D.aggA w) x +
          2 * (α ⬝ᵥ x / s) * (D.aggB w ⬝ᵥ x) +
          D.aggC w * (α ⬝ᵥ x / s) ^ 2 := fun k => hcert k
  choose s hs hspos w hw hsum hsweep using hseq
  have hwne (k : ℕ) : w k ≠ 0 := by
    intro heq
    have hh := hsum k
    simp [heq] at hh
  let z : ℕ → Coeff n := fun k => (D.aggA (w k), D.aggB (w k))
  have hzP (k : ℕ) : z k ∈ D.coefficientCone := ⟨w k, hw k, rfl⟩
  have hsweep' (k : ℕ) : ∀ x, 0 ≤ q (D.aggA (w k)) x +
      2 * ((s k)⁻¹ * (α ⬝ᵥ x)) * (D.aggB (w k) ⬝ᵥ x) +
      D.aggC (w k) * ((s k)⁻¹ * (α ⬝ᵥ x)) ^ 2 := by
    simpa only [div_eq_mul_inv, mul_comm (s k)⁻¹] using hsweep k
  have hzne (k : ℕ) : z k ≠ 0 :=
    D.sweep_pair_ne_zero hx₀ (hw k) (hwne k) hα
      (inv_ne_zero (ne_of_gt (hspos k))) (hsweep' k)
  have ht : Tendsto s atTop atTop :=
    tendsto_atTop_mono (fun k => (hs k).le) tendsto_natCast_atTop_atTop
  have hr : Tendsto (fun k => (s k)⁻¹) atTop (𝓝 (0 : ℝ)) :=
    tendsto_inv_atTop_zero.comp ht
  obtain ⟨z₀, hz₀, hnorm, hpsd⟩ := exists_nonzero_psd_limit
    coefficientQuadratic coefficientLinear
    (coefficientQuadratic x₀ + (2 : ℝ) • coefficientLinear x₀)
    (fun x => α ⬝ᵥ x) D.coefficientCone D.isClosed_coefficientCone
    D.coefficientCone_smul z hzP hzne (fun k => (s k)⁻¹) hr (by
      intro k x
      exact D.sweep_constant_elimination hx₀ (hw k) (hwne k) α ((s k)⁻¹) (hsweep' k) x)
  exact D.certificate_of_coefficientCone hz₀
    (by intro heq; simp [heq] at hnorm) hpsd

/-- The source's full main equivalence, with asymptotic hyperplane convexity. -/
theorem proper_hull_iff_certificate (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHC) :
    convexHull ℝ D.feasible ≠ Set.univ ↔ ∃ w, D.Certificate w := by
  exact ⟨D.exists_certificate_of_proper hS hHC,
    fun ⟨_, hw⟩ => hw.convexHull_ne_univ⟩

/-- The source's increasing-sequence formulation gives the same full theorem. -/
theorem proper_hull_iff_certificate_of_sequence (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHCSequence) :
    convexHull ℝ D.feasible ≠ Set.univ ↔ ∃ w, D.Certificate w :=
  D.proper_hull_iff_certificate hS (D.asymptoticHC_iff_sequence.mpr hHC)

/-- Hidden hyperplane convexity specializes the main theorem to the statement
identified in the source as Blekherman--Dey--Sun Conjecture 3.3. -/
theorem proper_hull_iff_certificate_of_hhc (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.HHC) :
    convexHull ℝ D.feasible ≠ Set.univ ↔ ∃ w, D.Certificate w :=
  D.proper_hull_iff_certificate hS hHC.asymptoticHC

end QuadraticAggregation.System
