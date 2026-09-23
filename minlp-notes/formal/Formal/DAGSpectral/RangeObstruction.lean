import Formal.DAGSpectral.PSDAlgebra
import Formal.DAGSpectral.GraphInput

/-! Exact range and two-sided coverage cannot be replaced by numerical closeness
or by deleting Loewner-dominated paths. -/
namespace DAGSpectral
noncomputable section
open Matrix
open scoped BigOperators MatrixOrder

/-- The rank-one matrix of (1,t). -/
def tiltedRankOne (t : ℝ) : RealMatrix 2 := vecMulVec ![1, t] ![1, t]

theorem tiltedRankOne_psd (t : ℝ) : (tiltedRankOne t).PosSemidef := by
  simpa [tiltedRankOne] using posSemidef_vecMulVec_self_star (![1, t] : Fin 2 → ℝ)

theorem tiltedRankOne_kernel (t : ℝ) : tiltedRankOne t *ᵥ ![-t, 1] = 0 := by
  ext i
  fin_cases i <;> simp [tiltedRankOne, mulVec, dotProduct, Fin.sum_univ_two,
    vecMulVec_apply]

theorem tiltedRankOne_kernel_distinct {t : ℝ} (ht : t ≠ 0) :
    LinearMap.ker (tiltedRankOne t).mulVecLin ≠
      LinearMap.ker (tiltedRankOne 0).mulVecLin := by
  intro he
  have hm : ![-t, 1] ∈ LinearMap.ker (tiltedRankOne t).mulVecLin :=
    tiltedRankOne_kernel t
  rw [he] at hm
  have hz := congrFun hm 0
  have hz' : t = 0 := by
    simpa [tiltedRankOne, mulVec, dotProduct, Fin.sum_univ_two] using hz
  exact ht hz'

/-- Neither distinct rank-one range can dominate a positive multiple of the other. -/
theorem tiltedRankOne_incomparable {t c : ℝ} (ht : t ≠ 0) (hc : 0 < c) :
    ¬Loewner (c • tiltedRankOne 0) (tiltedRankOne t) ∧
      ¬Loewner (c • tiltedRankOne t) (tiltedRankOne 0) := by
  constructor
  · intro h
    have hq := h.quadratic ![-t, 1]
    rw [tiltedRankOne_kernel t, dotProduct_zero] at hq
    simp [tiltedRankOne, dotProduct, mulVec, Fin.sum_univ_two] at hq
    nlinarith [sq_pos_of_ne_zero ht]
  · intro h
    have hq := h.quadratic ![0, 1]
    simp [tiltedRankOne, dotProduct, mulVec, Fin.sum_univ_two,
      vecMulVec_apply] at hq
    nlinarith [sq_pos_of_ne_zero ht]

/-- Entry differences are small even when the exact kernels are different. -/
theorem tiltedRankOne_entry_bound {t : ℝ} (ht : |t| ≤ 1) (i j : Fin 2) :
    |tiltedRankOne t i j - tiltedRankOne 0 i j| ≤ |t| := by
  have hp : |t| * |t| ≤ |t| := by nlinarith [abs_nonneg t]
  fin_cases i <;> fin_cases j <;> simp [tiltedRankOne, vecMulVec_apply, abs_mul]
  nlinarith [sq_abs t]

/-- Arbitrarily close PSD matrices need not admit either relative domination. -/
theorem arbitrarily_close_distinct_ranges {ε : ℝ} (hε : 0 < ε) :
    ∃ t : ℝ, t ≠ 0 ∧ (∀ i j, |tiltedRankOne t i j - tiltedRankOne 0 i j| < ε) ∧
      ∀ c : ℝ, 0 < c → ¬Loewner (c • tiltedRankOne 0) (tiltedRankOne t) ∧
        ¬Loewner (c • tiltedRankOne t) (tiltedRankOne 0) := by
  let t := min ε 1 / 2
  have ht : 0 < t := by dsimp [t]; positivity
  have htε : t < ε := by dsimp [t]; have := min_le_left ε 1; linarith
  have ht1 : t ≤ 1 := by dsimp [t]; have := min_le_right ε 1; linarith
  refine ⟨t, ne_of_gt ht, ?_, fun c hc => tiltedRankOne_incomparable (ne_of_gt ht) hc⟩
  intro i j
  exact (tiltedRankOne_entry_bound (by rwa [abs_of_pos ht]) i j).trans_lt
    (by rwa [abs_of_pos ht])

/-- The obstruction persists for rational input data at every requested accuracy. -/
theorem arbitrarily_close_rational_distinct_ranges {ε : ℝ} (hε : 0 < ε) :
    ∃ t : ℚ, t ≠ 0 ∧
      (∀ i j, |tiltedRankOne (t : ℝ) i j - tiltedRankOne 0 i j| < ε) ∧
      ∀ c : ℝ, 0 < c →
        ¬Loewner (c • tiltedRankOne 0) (tiltedRankOne (t : ℝ)) ∧
          ¬Loewner (c • tiltedRankOne (t : ℝ)) (tiltedRankOne 0) := by
  obtain ⟨t, ht, htu⟩ := exists_rat_btwn (show (0 : ℝ) < min ε 1 by positivity)
  have htε : (t : ℝ) < ε := htu.trans_le (min_le_left _ _)
  have ht1 : |(t : ℝ)| ≤ 1 := by
    rw [abs_of_pos ht]
    exact htu.le.trans (min_le_right _ _)
  refine ⟨t, ?_, ?_, fun c hc => tiltedRankOne_incomparable (ne_of_gt ht) hc⟩
  · exact_mod_cast ne_of_gt ht
  · intro i j
    exact (tiltedRankOne_entry_bound ht1 i j).trans_lt (by rwa [abs_of_pos ht])

/-- Two parallel edges are two genuine feasible DAG paths. -/
def twoPathDAG : ExplicitDAG 2 2 where
  src := fun _ => 0
  dst := fun _ => 1
  forward := by intro e; decide

theorem twoPathDAG_path (e : Fin 2) : twoPathDAG.Path 0 1 [e] := by
  exact (ExplicitDAG.Path.nil (G := twoPathDAG) (s := 0)).snoc e rfl

def twoPathAtom (e : Fin 2) : RealMatrix 1 := ((e.val + 1 : ℕ) : ℝ) • 1

def twoPathInformation (es : List (Fin 2)) : RealMatrix 1 := (es.map twoPathAtom).sum

@[simp] theorem twoPathInformation_zero : twoPathInformation [0] = 1 := by
  simp [twoPathInformation, twoPathAtom]

@[simp] theorem twoPathInformation_one : twoPathInformation [1] = (2 : ℝ) • 1 := by
  simp [twoPathInformation, twoPathAtom]

theorem twoPath_dominated : Loewner (twoPathInformation [0]) (twoPathInformation [1]) := by
  simp only [twoPathInformation_zero, twoPathInformation_one]
  simpa only [one_smul] using psd_smul_mono (A := (1 : RealMatrix 1))
    Matrix.PosSemidef.one (show (1 : ℝ) ≤ 2 by norm_num)

/-- Retaining only the larger path destroys the upper half of the cover. -/
theorem dominated_path_deletion_loses_cover {η : ℝ} (hη : η < 1 / 2) :
    twoPathDAG.Path 0 1 [0] ∧ twoPathDAG.Path 0 1 [1] ∧
      Loewner (twoPathInformation [0]) (twoPathInformation [1]) ∧
      ¬RelativeSandwich η (twoPathInformation [0]) (twoPathInformation [1]) := by
  refine ⟨twoPathDAG_path 0, twoPathDAG_path 1, twoPath_dominated, ?_⟩
  intro h
  have hq := h.2.quadratic (fun _ => 1)
  simp only [twoPathInformation_zero, twoPathInformation_one, Matrix.smul_mulVec,
    Matrix.one_mulVec, dotProduct_smul, smul_eq_mul] at hq
  norm_num [dotProduct] at hq
  linarith

end
end DAGSpectral
