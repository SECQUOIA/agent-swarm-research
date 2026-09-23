import Formal.DAGSpectral.ProfileDPBounds

namespace DAGSpectral.ExplicitDAG
open scoped BigOperators
noncomputable section
variable {v m : ℕ} {κ : Type*} [Fintype κ]

def spectralLabels (a : Fin m → κ → ℝ) (η : ℝ) (r N : ℕ) : Fin m → κ → ℤ :=
  fun e i => floorLabel (spectralMesh η r N) (a e i)

omit [Fintype κ] in
theorem profile_eq_pathLabel (a : Fin m → κ → ℝ) (η : ℝ) (r N : ℕ)
    (es : List (Fin m)) (i : κ) :
    profile (spectralLabels a η r N) es i =
      pathLabel (spectralMesh η r N) (es.map (fun e => a e i)) := by
  simp [profile_apply, spectralLabels, pathLabel, List.map_map, Function.comp_def]

omit [Fintype κ] in
theorem allowed_profile_window (G : ExplicitDAG v m) (allowed : Fin m → Bool)
    (s t : Fin v) (a : Fin m → κ → ℝ) (p r N : ℕ) (η : ℝ)
    (hr : 0 < r) (hN : 0 < N) (hη : 0 < η) (hv : v - 1 ≤ N)
    (ha : ∀ e, allowed e = true → ∀ i, |a e i| ≤ 4 * p)
    {es : List (Fin m)} (he : G.AllowedPath allowed s t es) (i : κ) :
    profile (spectralLabels a η r N) es i ∈ coordinateRange p N (spectralMesh η r N) := by
  rw [profile_eq_pathLabel]
  apply pathLabel_mem_coordinateRange hN (spectralMesh_pos hη hr hN)
  · simpa using he.1.length_le_vertices.trans hv
  · intro z hz
    obtain ⟨e,he',rfl⟩ := List.mem_map.mp hz
    exact ha e (he.2 e he') i

theorem spectral_state_capacity (required : Finset (Fin m)) (p r N : ℕ) (η : ℝ)
    (hr : 0 < r) (hN : 0 < N) (hη : 0 < η) (hreq : required.card ≤ r) :
    2 ^ required.card * (coordinateRange p N (spectralMesh η r N)).card ^ Fintype.card κ ≤
      2 ^ r * (coordinateCount p r N η) ^ Fintype.card κ := by
  exact Nat.mul_le_mul (Nat.pow_le_pow_right (by decide) hreq)
    (Nat.pow_le_pow_left (coordinateRange_card_le hr hN hη) _)

theorem spectral_dp_bounds (G : ExplicitDAG v m) (allowed : Fin m → Bool)
    (s t : Fin v) (required : Finset (Fin m)) (a : Fin m → κ → ℝ)
    (p r N : ℕ) (η : ℝ) (hr : 0 < r) (hN : 0 < N) (hη : 0 < η) (hv : v - 1 ≤ N)
    (hreq : required.card ≤ r) (ha : ∀ e, allowed e = true → ∀ i, |a e i| ≤ 4 * p) :
    storedStates G allowed s required (spectralLabels a η r N) v ≤
      v * (2 ^ r * coordinateCount p r N η ^ Fintype.card κ) ∧
    edgeExtensions G allowed s required (spectralLabels a η r N) ≤
      m * (2 ^ r * coordinateCount p r N η ^ Fintype.card κ) ∧
    (output G allowed s t required (spectralLabels a η r N)).length ≤
      2 ^ r * coordinateCount p r N η ^ Fintype.card κ := by
  let window := coordinateRange p N (spectralMesh η r N)
  have hw : ∀ t es, G.AllowedPath allowed s t es → ∀ i,
      profile (spectralLabels a η r N) es i ∈ window :=
    fun t _ he i => allowed_profile_window G allowed s t a p r N η hr hN hη hv ha he i
  have hcap := spectral_state_capacity (κ := κ) required p r N η hr hN hη hreq
  exact ⟨(storedStates_bound G allowed s required _ window hw v).trans
      (Nat.mul_le_mul_left v hcap),
    (edgeExtensions_bound G allowed s required _ window hw).trans (Nat.mul_le_mul_left m hcap),
    (output_length_bound G allowed s required _ window hw t).trans hcap⟩

/-- The returned object is an actual feasible path with the required owners and
all coordinate sums close. This connects state merging to the rounding proof. -/
theorem output_coordinate_close (G : ExplicitDAG v m) (allowed : Fin m → Bool)
    (s t : Fin v) (required : Finset (Fin m)) (a : Fin m → κ → ℝ)
    (r N : ℕ) (η : ℝ) (hr : 0 < r) (hN : 0 < N) (hη : 0 < η) (hv : v - 1 ≤ N)
    (es : List (Fin m)) (he : G.AllowedPath allowed s t es) (hreq : required ⊆ es.toFinset) :
    ∃ rep ∈ output G allowed s t required (spectralLabels a η r N),
      G.AllowedPath allowed s t rep ∧ required ⊆ rep.toFinset ∧
      ∀ i, |(rep.map (fun e => a e i)).sum - (es.map (fun e => a e i)).sum| <
        N * spectralMesh η r N := by
  obtain ⟨rep,hrep,hkey⟩ := output_complete G allowed s required
    (spectralLabels a η r N) t es he hreq
  obtain ⟨hp,ho⟩ := output_sound G allowed s required (spectralLabels a η r N) t hrep
  refine ⟨rep,hrep,hp,ho,?_⟩
  intro i
  have hprof : profile (spectralLabels a η r N) rep i =
      profile (spectralLabels a η r N) es i := congrFun (congrArg Prod.snd hkey) i
  rw [profile_eq_pathLabel, profile_eq_pathLabel] at hprof
  exact equal_label_sum_close (spectralMesh_pos hη hr hN) hN _ _
    (by simpa using hp.1.length_le_vertices.trans hv)
    (by simpa using he.1.length_le_vertices.trans hv) hprof

end
end DAGSpectral.ExplicitDAG
