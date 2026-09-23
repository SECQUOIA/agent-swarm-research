import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Topology.Sequences

open Filter Set
open scoped Topology

namespace QuadraticAggregation

/-- A sequence of nonzero coefficients in a closed cone, whose quadratic
forms become positive semidefinite after vanishing linear perturbations,
has a nonzero positive semidefinite limit after normalization.

For a strictly feasible quadratic system, evaluate the aggregated inequality
at a feasible point to eliminate its constant term before applying this
lemma. This avoids a separate limit of the simplex weights. -/
theorem exists_nonzero_psd_limit
    {E X : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [ProperSpace E]
    (q b : X → E →L[ℝ] ℝ) (d : E →L[ℝ] ℝ) (a : X → ℝ)
    (P : Set E) (hP : IsClosed P)
    (hscale : ∀ t : ℝ, 0 ≤ t → ∀ z ∈ P, t • z ∈ P)
    (z : ℕ → E) (hzP : ∀ k, z k ∈ P) (hzne : ∀ k, z k ≠ 0)
    (r : ℕ → ℝ) (hr : Tendsto r atTop (𝓝 0))
    (hsweep : ∀ k x,
      0 ≤ q x (z k) + 2 * (r k * a x) * b x (z k) -
        (r k * a x)^2 * d (z k)) :
    ∃ z₀ ∈ P, ‖z₀‖ = 1 ∧ ∀ x, 0 ≤ q x z₀ := by
  let u : ℕ → E := fun k => ‖z k‖⁻¹ • z k
  have hunorm : ∀ k, ‖u k‖ = 1 := by
    intro k
    simp [u, norm_smul, norm_ne_zero_iff.mpr (hzne k)]
  have huP : ∀ k, u k ∈ P := by
    intro k
    exact hscale _ (inv_nonneg.mpr (norm_nonneg _)) _ (hzP k)
  obtain ⟨u₀, hu₀, f, hf, hfu⟩ :=
    (isCompact_sphere (0 : E) 1).tendsto_subseq (fun k => by simpa using hunorm k)
  have hu₀P : u₀ ∈ P :=
    hP.mem_of_tendsto hfu (Filter.Eventually.of_forall (fun k => huP (f k)))
  refine ⟨u₀, hu₀P, by simpa using hu₀, ?_⟩
  intro x
  have hq := (q x).continuous.tendsto u₀ |>.comp hfu
  have hb := (b x).continuous.tendsto u₀ |>.comp hfu
  have hd := d.continuous.tendsto u₀ |>.comp hfu
  have hrf : Tendsto (fun k => r (f k)) atTop (𝓝 0) := hr.comp hf.tendsto_atTop
  have hlim := (hq.add ((hrf.mul_const (a x)).const_mul 2 |>.mul hb)).sub
    (((hrf.mul_const (a x)).pow 2).mul hd)
  have hnonneg : ∀ k,
      0 ≤ q x (u k) + 2 * (r k * a x) * b x (u k) - (r k * a x)^2 * d (u k) := by
    intro k
    have hm := mul_nonneg (inv_nonneg.mpr (norm_nonneg (z k))) (hsweep k x)
    simpa only [u, map_smul, smul_eq_mul, mul_sub, mul_add, mul_assoc,
      mul_left_comm, mul_comm] using hm
  have := ge_of_tendsto hlim (Filter.Eventually.of_forall (fun k => hnonneg (f k)))
  simpa using this

end QuadraticAggregation
