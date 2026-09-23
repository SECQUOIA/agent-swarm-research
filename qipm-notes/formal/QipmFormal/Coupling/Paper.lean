import QipmFormal.Coupling.Block
import QipmFormal.Coupling.Asymptotics

/-!
# Filtering parameters of the actual block inverse

This interface connects the inverse of a linear equivalence H to the exact
Schur formulas and then to the asymptotic estimates. The orthogonal-sum norm
is used explicitly. Values of a path at μ = 0 need not model an invertible
Newton matrix: all theorems apply on filters where μ is eventually positive.
-/

open Filter Asymptotics
open scoped Topology

namespace QipmFormal.Coupling
noncomputable section

variable {U K : Type*} [NormedAddCommGroup U] [NormedSpace ℝ U]
  [NormedAddCommGroup K] [NormedSpace ℝ K]

/-- A family of exact block models, together with the actual invertible H.
The block identities are imposed by `BlockFamily.ValidAt`, not by the data. -/
structure BlockFamily (U K : Type*) [NormedAddCommGroup U] [NormedSpace ℝ U]
    [NormedAddCommGroup K] [NormedSpace ℝ K] where
  C : ℝ → U →ₗ[ℝ] U
  D : ℝ → U →ₗ[ℝ] U
  F : ℝ → U →ₗ[ℝ] K
  T : ℝ → K →ₗ[ℝ] U
  E : ℝ → K ≃ₗ[ℝ] K
  S : ℝ → U ≃ₗ[ℝ] U
  H : ℝ → (U × K) ≃ₗ[ℝ] (U × K)

namespace BlockFamily

variable (d : BlockFamily U K)

/-- Exact block realization at a nonzero central parameter. -/
def ValidAt (μ : ℝ) : Prop :=
  μ ≠ 0 ∧ HasSchurFactor μ (d.C μ) (d.D μ) (d.F μ) (d.T μ) (d.E μ) (d.S μ) ∧
    ∀ z, d.H μ z = blockOperator μ (d.C μ) (d.D μ) (d.F μ) (d.T μ) (d.E μ) z

def p (b : U) (μ : ℝ) : U := couplingP (d.S μ) b
def g (b : U) (μ : ℝ) : K := couplingG (d.F μ) (d.E μ) (d.S μ) b
def q (b : U) (μ : ℝ) : U := couplingQ (d.F μ) (d.T μ) (d.E μ) (d.S μ) b
def h (b : U) (μ : ℝ) : K := (d.E μ).symm (d.g b μ)
def r (b : U) (μ : ℝ) : K := (d.E μ).symm (d.F μ (d.q b μ))

/-- The actual first inverse vector, with active right-hand side `(b,0)`. -/
def firstVector (b : U) (μ : ℝ) : U × K := (d.H μ).symm (b, 0)

/-- The actual second inverse vector. -/
def secondVector (b : U) (μ : ℝ) : U × K := (d.H μ).symm (d.firstVector b μ)

def firstInverseNorm (b : U) (μ : ℝ) : ℝ :=
  blockNorm (d.firstVector b μ).1 (d.firstVector b μ).2

def secondInverseNorm (b : U) (μ : ℝ) : ℝ :=
  blockNorm (d.secondVector b μ).1 (d.secondVector b μ).2

/-- First-inverse amplification from the paper, using the actual inverse H⁻¹. -/
def xi (α : ℝ → ℝ) (b : U) (μ : ℝ) : ℝ :=
  α μ * d.firstInverseNorm b μ / ‖b‖

/-- Ideal filtering parameter, using the actual H⁻² and H⁻¹. -/
def rho (α : ℝ → ℝ) (b : U) (μ : ℝ) : ℝ :=
  α μ * d.secondInverseNorm b μ / d.firstInverseNorm b μ

lemma equiv_eq {μ : ℝ} (hd : d.ValidAt μ) :
    d.H μ = blockEquiv μ (d.C μ) (d.D μ) (d.F μ) (d.T μ) (d.E μ) (d.S μ)
      hd.1 hd.2.1 := by
  apply LinearEquiv.ext
  intro z
  exact hd.2.2 z

lemma firstVector_eq {μ : ℝ} (hd : d.ValidAt μ) (b : U) :
    d.firstVector b μ = (μ • d.p b μ, -μ • d.g b μ) := by
  unfold firstVector
  rw [d.equiv_eq hd]
  exact first_inverse _ _ _ _ _ _ _ hd.1 hd.2.1 b

lemma secondVector_eq {μ : ℝ} (hd : d.ValidAt μ) (b : U) :
    d.secondVector b μ = (μ ^ 2 • d.q b μ, -d.h b μ - μ ^ 2 • d.r b μ) := by
  unfold secondVector firstVector
  rw [d.equiv_eq hd]
  exact second_inverse _ _ _ _ _ _ _ hd.1 hd.2.1 b

lemma firstInverseNorm_eq {μ : ℝ} (hd : d.ValidAt μ) (b : U) :
    d.firstInverseNorm b μ = firstNorm (d.p b) (d.g b) μ := by
  unfold firstInverseNorm
  rw [d.firstVector_eq hd]
  simp [firstNorm]

lemma secondInverseNorm_eq {μ : ℝ} (hd : d.ValidAt μ) (b : U) :
    d.secondInverseNorm b μ = secondNorm (d.q b) (d.h b) (d.r b) μ := by
  unfold secondInverseNorm
  rw [d.secondVector_eq hd]
  rfl

lemma rho_eq {μ : ℝ} (hd : d.ValidAt μ) (α : ℝ → ℝ) (b : U) :
    d.rho α b μ = filtering α (d.p b) (d.q b) (d.g b) (d.h b) (d.r b) μ := by
  simp only [rho, filtering, d.firstInverseNorm_eq hd, d.secondInverseNorm_eq hd]

/-- Rescaling the centering right-hand side rescales each actual inverse. -/
lemma firstVector_smul (c : ℝ) (b : U) (μ : ℝ) :
    d.firstVector (c • b) μ = c • d.firstVector b μ := by
  simp [firstVector, ← map_smul]

lemma secondVector_smul (c : ℝ) (b : U) (μ : ℝ) :
    d.secondVector (c • b) μ = c • d.secondVector b μ := by
  simp [secondVector, d.firstVector_smul]

lemma firstInverseNorm_smul (c : ℝ) (b : U) (μ : ℝ) :
    d.firstInverseNorm (c • b) μ = |c| * d.firstInverseNorm b μ := by
  simp only [firstInverseNorm, d.firstVector_smul, Prod.smul_fst, Prod.smul_snd,
    blockNorm_smul]

lemma secondInverseNorm_smul (c : ℝ) (b : U) (μ : ℝ) :
    d.secondInverseNorm (c • b) μ = |c| * d.secondInverseNorm b μ := by
  simp only [secondInverseNorm, d.secondVector_smul, Prod.smul_fst, Prod.smul_snd,
    blockNorm_smul]

/-- The nonzero scalar `(1-σ)` in the exact-centering Newton RHS is immaterial. -/
lemma xi_smul (α : ℝ → ℝ) {c : ℝ} (hc : c ≠ 0) (b : U) (μ : ℝ) :
    d.xi α (c • b) μ = d.xi α b μ := by
  simp only [xi, d.firstInverseNorm_smul, norm_smul, Real.norm_eq_abs]
  rw [mul_left_comm, mul_div_mul_left _ _ (abs_ne_zero.mpr hc)]

lemma rho_smul (α : ℝ → ℝ) {c : ℝ} (hc : c ≠ 0) (b : U) (μ : ℝ) :
    d.rho α (c • b) μ = d.rho α b μ := by
  simp only [rho, d.firstInverseNorm_smul, d.secondInverseNorm_smul]
  rw [mul_left_comm, mul_div_mul_left _ _ (abs_ne_zero.mpr hc)]

/-- The encoding factor is retained for the actual inverse of H. -/
theorem rho_nontight {l : Filter ℝ} (b : U)
    (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (hbounds : UniformBounds l (d.p b) (d.q b) (d.g b) (d.h b) (d.r b))
    (hμ : ∀ᶠ μ in l, 0 < μ) (α : ℝ → ℝ) :
    d.rho α b =Θ[l] (fun μ => α μ * (μ + ‖d.g b μ‖ / μ)) := by
  have he : d.rho α b =ᶠ[l]
      filtering α (d.p b) (d.q b) (d.g b) (d.h b) (d.r b) :=
    hd.mono fun _ h => d.rho_eq h α b
  exact he.isTheta.trans (filtering_nontight hbounds hμ α)

/-- Exact-center filtering law for an encoding with scale Θ(μ⁻¹). -/
theorem rho_tight {l : Filter ℝ} (b : U)
    (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (hbounds : UniformBounds l (d.p b) (d.q b) (d.g b) (d.h b) (d.r b))
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ => μ⁻¹)) :
    d.rho α b =Θ[l] (fun μ => 1 + ‖d.g b μ‖ / μ ^ 2) := by
  have he : d.rho α b =ᶠ[l]
      filtering α (d.p b) (d.q b) (d.g b) (d.h b) (d.r b) :=
    hd.mono fun _ h => d.rho_eq h α b
  exact he.isTheta.trans (filtering_tight hbounds hμ hα)

/-- The first-inverse parameter stays Θ(1), including in the coupled case. -/
theorem xi_tight {l : Filter ℝ} {b : U} (hb : b ≠ 0)
    (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (hbounds : UniformBounds l (d.p b) (d.q b) (d.g b) (d.h b) (d.r b))
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ => μ⁻¹)) :
    d.xi α b =Θ[l] (fun _ => (1 : ℝ)) := by
  have he : d.xi α b =ᶠ[l]
      (fun μ => α μ * firstNorm (d.p b) (d.g b) μ / ‖b‖) := by
    filter_upwards [hd] with μ hd
    simp only [xi, d.firstInverseNorm_eq hd]
  exact he.isTheta.trans (firstAmplification_tight hbounds hμ hα ‖b‖ (norm_ne_zero_iff.mpr hb))

/-- Bounded actual filtering is equivalent to quadratic coupling decay. -/
theorem rho_bounded_iff {l : Filter ℝ} (b : U)
    (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (hbounds : UniformBounds l (d.p b) (d.q b) (d.g b) (d.h b) (d.r b))
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ => μ⁻¹)) :
    d.rho α b =O[l] (fun _ => (1 : ℝ)) ↔ d.g b =O[l] (fun μ => μ ^ 2) :=
  (d.rho_tight b hd hbounds hμ hα).isBigO_congr_left.trans (profile_bounded_iff hμ)

/-- Nonzero limiting coupling forces the full inverse-square scale. -/
theorem rho_full_scale {l : Filter ℝ} (b : U)
    (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (hbounds : UniformBounds l (d.p b) (d.q b) (d.g b) (d.h b) (d.r b))
    (hμ : ∀ᶠ μ in l, 0 < μ) (hzero : Tendsto (fun μ : ℝ => μ) l (𝓝 0))
    {g₀ : K} (hg : Tendsto (d.g b) l (𝓝 g₀)) (hg₀ : g₀ ≠ 0)
    {α : ℝ → ℝ} (hα : α =Θ[l] (fun μ => μ⁻¹)) :
    d.rho α b =Θ[l] (fun μ => (μ ^ 2)⁻¹) := by
  have he : d.rho α b =ᶠ[l]
      filtering α (d.p b) (d.q b) (d.g b) (d.h b) (d.r b) :=
    hd.mono fun _ h => d.rho_eq h α b
  exact he.isTheta.trans (filtering_full_scale hbounds hμ hzero hg hg₀ hα)

/-- The precise coupling criterion: strict improvement is little-o of μ⁻². -/
theorem rho_improves_iff {l : Filter ℝ} [NeBot l] (b : U)
    (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (hbounds : UniformBounds l (d.p b) (d.q b) (d.g b) (d.h b) (d.r b))
    (hμ : ∀ᶠ μ in l, 0 < μ) (hzero : Tendsto (fun μ : ℝ => μ) l (𝓝 0))
    {g₀ : K} (hg : Tendsto (d.g b) l (𝓝 g₀))
    {α : ℝ → ℝ} (hα : α =Θ[l] (fun μ => μ⁻¹)) :
    d.rho α b =o[l] (fun μ => (μ ^ 2)⁻¹) ↔ g₀ = 0 := by
  have he : d.rho α b =ᶠ[l]
      filtering α (d.p b) (d.q b) (d.g b) (d.h b) (d.r b) :=
    hd.mono fun _ h => d.rho_eq h α b
  exact he.isTheta.isLittleO_congr_left.trans
    (filtering_improves_iff hbounds hμ hzero hg hα)

end BlockFamily
end
end QipmFormal.Coupling
