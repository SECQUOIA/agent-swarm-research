import Formal.NetworkSimplex.ThresholdBalancedProfile
import Formal.NetworkSimplex.ThresholdFace
import Formal.NetworkSimplex.ThresholdAffineRows

/-! Balanced incidence yields an actual original-coordinate graph-hull section. -/
namespace NetworkSimplex.Chain.Balanced
open scoped BigOperators
noncomputable section
variable {N : ℕ}

abbrev Obs (S : Fin N → Finset (Fin N)) := Observation (pattern S) (fun _ => False)
noncomputable instance (S : Fin N → Finset (Fin N)) : Fintype (Obs S) := Fintype.ofFinite _

/-- An individual observed a-arc product outside its allowed set. -/
def observation (S : Fin N → Finset (Fin N)) (r jr : Fin N) (hr : jr ∉ S r) : Obs S :=
  ⟨(Chain.a r, jr), by simp [Selected, Chain.a, hr]⟩

def sectionPoint (S : Fin N → Finset (Fin N)) (a : ℝ) (r s jr js : Fin N) (u v : ℝ) :=
  chainPoint (pattern S) (observed a r s jr js u v) (fun _ _ => 0) (fun _ => 2 * a)
    (aggregate S a) (fun i => 1 / 2 - aggregate S a i) (1 / 2) (fun _ => False) (fun _ => 0)

def originalGraph (S : Fin N → Finset (Fin N)) :=
  OriginalGraph (incidence N) (demand N) (fun _ => 1)
    (fun o : Obs S => o.val.1) (fun o => o.val.2)

theorem observation_ne (S : Fin N → Finset (Fin N)) {r s : Fin N} (hrs : r ≠ s)
    (jr js : Fin N) (hr : jr ∉ S r) (hs : js ∉ S s) :
    observation S r jr hr ≠ observation S s js hs := by
  intro h
  have he := congrArg (fun o : Obs S => o.val.1) h
  simp only [observation, Chain.a, Sum.inl.injEq, Prod.mk.injEq, and_true] at he
  exact hrs he

/-- Every coordinate except the two individual product entries is fixed. -/
theorem sectionPoint_eq_productSlice (S : Fin N → Finset (Fin N)) (a : ℝ)
    (r s jr js : Fin N) (hr : jr ∉ S r) (hs : js ∉ S s) (u v : ℝ) :
    sectionPoint S a r s jr js u v = productSlice (sectionPoint S a r s jr js 0 0)
      (observation S r jr hr) (observation S s js hs) u v := by
  classical
  refine Prod.ext (by rfl) ?_
  refine Prod.ext (by rfl) ?_
  funext o
  rcases o with ⟨⟨e, j⟩, ho⟩
  rcases e with ⟨i, flag⟩ | z
  · cases flag
    · simp [sectionPoint, chainPoint, pack, observed, productSlice, observation,
        Chain.a, Observation, Subtype.ext_iff]
    · exact False.elim (pattern_not_b S i j ho)
  · exact ho.elim

/-- Explicit weights really are a simplex point with zero residual state. -/
theorem weights_simplex {a : ℝ} (ha : 0 < a) (hscale : (N : ℝ) * a = 1 / 2) :
    Simplex (fun _ : Fin N => 2 * a) := by
  refine ⟨fun _ => by positivity, ?_⟩
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  nlinarith

/-- The quantitative neighborhood includes its feasible boundary and describes the actual hull. -/
theorem section_hull_iff (S : Fin N → Finset (Fin N)) (hK : IsUnit (incidenceMatrix S).det)
    (hne : ∀ i, (S i).Nonempty) (alpha : Fin N → ℝ) (halpha : ∀ i, 0 < alpha i)
    {beta a u v : ℝ} (hbeta : 0 < beta) (ha : 0 < a) (hscale : (N : ℝ) * a = 1 / 2)
    (hbal : ∀ j, ∑ i, alpha i * incidenceMatrix S i j = beta)
    {r s : Fin N} (hrs : r ≠ s) (jr js : Fin N) (hr : jr ∉ S r) (hs : js ∉ S s)
    (hu : |u| < epsilon a (alpha r / alpha s) (inverseSize (incidenceMatrix S)))
    (hv : |v| < epsilon a (alpha r / alpha s) (inverseSize (incidenceMatrix S))) :
    sectionPoint S a r s jr js u v ∈ convexHull ℝ (originalGraph S) ↔
      0 ≤ alpha r * u + alpha s * v := by
  have hw := weights_simplex ha hscale
  unfold originalGraph
  rw [original_hull_iff_full_of_sum_one _ _ _ _ _ _ hw.2]
  change chainPoint _ _ _ _ _ _ _ _ _ ∈ convexHull ℝ (chainGraph _ _) ↔ _
  rw [mem_chainHull_iff_profile _ _ _ _ _ _ _ _ _ hw (by intro i; ring)
    (fun i => observed_nonnegative ha (div_pos (halpha r) (halpha s))
      (norm_nonneg _) hu hv S hrs jr js i)]
  exact ⟨fun ⟨w, hw⟩ => profile_necessary S alpha halpha hscale hbal r s jr js hr hs u v hw,
    fun hh => ⟨_, profile_sufficient S hK hne alpha halpha hbeta ha hscale hbal hrs
      jr js hr hs hu hv hh⟩⟩

/-- Proper, nonempty rows give the strict original flow margins stated in the construction. -/
theorem aggregate_bounds (S : Fin N → Finset (Fin N)) {a : ℝ} (ha : 0 < a)
    (hscale : (N : ℝ) * a = 1 / 2) (hne : ∀ i, (S i).Nonempty)
    (hproper : ∀ i, S i ≠ Finset.univ) (i : Fin N) :
    0 < aggregate S a i ∧ aggregate S a i < 1 / 2 := by
  have hall : ∀ j : Fin N, 0 < (if j ∈ S i then a else a / 4) := by
    intro j; split_ifs <;> positivity
  have hle : ∀ j : Fin N, (if j ∈ S i then a else a / 4) ≤ a := by
    intro j; split_ifs <;> linarith
  obtain ⟨j, hj⟩ := hne i
  have hsum : 0 < aggregate S a i :=
    Finset.sum_pos' (fun l _ => (hall l).le) ⟨j, Finset.mem_univ _, hall j⟩
  have hex : ∃ j, j ∉ S i := by
    by_contra hh
    push Not at hh
    apply hproper i
    ext j
    simp [hh j]
  obtain ⟨l, hl⟩ := hex
  have hstrict : (∑ j : Fin N, if j ∈ S i then a else a / 4) < ∑ _ : Fin N, a := by
    apply Finset.sum_lt_sum (fun j _ => hle j)
    exact ⟨l, Finset.mem_univ _, by simp [hl]; linarith⟩
  simpa only [aggregate, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    hscale] using And.intro hsum hstrict

/-- The standard paper normalization satisfies the scale equation exactly. -/
theorem normalization {N : ℕ} (hN : 0 < N) :
    0 < 1 / (2 * (N : ℝ)) ∧ (N : ℝ) * (1 / (2 * (N : ℝ))) = 1 / 2 := by
  have hNR : (0 : ℝ) < N := by exact_mod_cast hN
  constructor
  · positivity
  · field_simp

end
end NetworkSimplex.Chain.Balanced
