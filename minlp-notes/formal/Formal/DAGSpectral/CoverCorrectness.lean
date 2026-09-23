import Formal.DAGSpectral.CoverProducer
import Formal.DAGSpectral.PathInformation
import Formal.DAGSpectral.NormalizationComplete

namespace DAGSpectral
open Matrix
namespace NormalizationTrials
variable {v m p M : ℕ}

theorem trialAtom_psd (D : FactorData p m M) (b : Finset (Fin M))
    (o : Option (Fin m)) : (ratMatrixReal (trialAtom D b o)).PosSemidef := by
  simpa only [trialAtom, ratMatrixReal_mul, ratMatrixReal_transpose,
    Matrix.conjTranspose_eq_transpose_of_trivial] using
    (atom_real_psd D o).mul_mul_conjTranspose_same
      (ratMatrixReal (transformCode D.vector D.weight b))

theorem restore_pathMatrix (D : FactorData p m M) (b : Finset (Fin M))
    (es : List (Fin m)) (hn : es.Nodup)
    (ha : acceptsSelection D.vector D.weight D.owner b D.atom es.toFinset) :
    let K := ratMatrixReal (restore D.vector D.weight b)
    K * pathMatrix (ratMatrixReal (trialAtom D b none))
      (fun e => ratMatrixReal (trialAtom D b (some e))) es * Kᵀ =
      pathMatrix (ratMatrixReal (D.atom none)) (fun e => ratMatrixReal (D.atom (some e))) es := by
  dsimp only
  simp only [trialAtom, transformCode_eq]
  rw [transformed_pathMatrix_eq D b es hn, pathMatrix_eq_information D es hn]
  have hh := reconstruct_retained (columns D.vector b) (scales D.weight b)
    (fun i => (scale_spec (D.weight_pos (label b i))).1.ne')
    (information D es.toFinset) (information_symmetric D es.toFinset)
    (accepted_range D es.toFinset b ha)
  simpa only [ratMatrixReal_mul, ratMatrixReal_transpose, restore, transform] using
    congrArg ratMatrixReal hh

theorem trialPathSet_complete (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (hη : 0 < η)
    (b : Finset (Fin M)) (hb : 0 < b.card) (hi : independent D.vector b)
    (es : List (Fin m)) (he : G.Path s t es)
    (ha : acceptsSelection D.vector D.weight D.owner b D.atom es.toFinset) :
    ∃ fs ∈ trialPathSet G s t D η b,
      RelativeSandwich (η : ℝ)
        (pathMatrix (ratMatrixReal (D.atom none)) (fun e => ratMatrixReal (D.atom (some e))) es)
        (pathMatrix (ratMatrixReal (D.atom none))
          (fun e => ratMatrixReal (D.atom (some e))) fs) := by
  have hp : G.AllowedPath (trialAllowed D b) s t es := by
    refine ⟨he,fun e he' => ?_⟩
    exact decide_eq_true ((acceptsAtomCode_iff _ _ _ _).mpr
      (ha.2.2 e (List.mem_toFinset.mpr he')))
  have hfloor : Loewner 1 (pathMatrix (ratMatrixReal (trialAtom D b none))
      (fun e => ratMatrixReal (trialAtom D b (some e))) es) := by
    simp only [trialAtom,transformCode_eq]
    rw [transformed_pathMatrix_eq D b es he.nodup]
    exact accepted_floor D es.toFinset b hi ha
  obtain ⟨fs,hfs,hpf,hof,hrel⟩ := trial_output_relative G (trialAllowed D b) s t
    (forcedOwners D.owner b) (trialAtom D b none) (fun e => trialAtom D b (some e))
    (trialAtom_psd D b none).isHermitian (fun e => (trialAtom_psd D b (some e)).isHermitian)
    η hη hb es hp ha.1 hfloor
  have hmem : fs ∈ trialPathSet G s t D η b := by
    unfold trialPathSet
    rw [if_pos ((acceptsAtomCode_iff _ _ _ _).mpr ha.2.1)]
    exact List.mem_toFinset.mpr hfs
  have hacc := (trialPathSet_sound G s t D η b hmem).2
  refine ⟨fs,hmem,?_⟩
  have hh := hrel.congruence (ratMatrixReal (restore D.vector D.weight b))
  simpa only [restore_pathMatrix D b es he.nodup ha,
    restore_pathMatrix D b fs hpf.1.nodup hacc] using hh

theorem pathMatrix_zero_of_atoms (D : FactorData p m M) (es : List (Fin m))
    (h0 : D.atom none = 0) (he : ∀ e ∈ es, D.atom (some e) = 0) :
    pathMatrix (ratMatrixReal (D.atom none)) (fun e => ratMatrixReal (D.atom (some e))) es = 0 := by
  unfold pathMatrix
  rw [h0,ratMatrixReal_zero,zero_add]
  apply List.sum_eq_zero
  intro A hA
  obtain ⟨e,he',rfl⟩ := List.mem_map.mp hA
  simp [he e he']

theorem zeroPathSet_complete (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (es : List (Fin m)) (he : G.Path s t es)
    (h0 : D.atom none = 0) (hz : ∀ e ∈ es, D.atom (some e) = 0) :
    ∃ fs ∈ zeroPathSet G s t D, RelativeSandwich (η : ℝ)
      (pathMatrix (ratMatrixReal (D.atom none)) (fun e => ratMatrixReal (D.atom (some e))) es)
      (pathMatrix (ratMatrixReal (D.atom none)) (fun e => ratMatrixReal (D.atom (some e))) fs) := by
  let allowed := fun e => decide (D.atom (some e) = 0)
  let labels := fun (_ : Fin m) (_ : Fin 0) => (0 : ℤ)
  have hpath : G.AllowedPath allowed s t es := ⟨he,fun e he => decide_eq_true (hz e he)⟩
  obtain ⟨rep,hrep,_⟩ := G.output_complete allowed s ∅ labels t es hpath (Finset.empty_subset _)
  have hne : G.output allowed s t ∅ labels ≠ [] := List.ne_nil_of_mem hrep
  obtain ⟨fs,tail,ht⟩ := List.exists_cons_of_ne_nil hne
  have hf : fs ∈ zeroPathSet G s t D := by
    simp only [zeroPathSet,h0,if_true]
    change fs ∈ ((G.output allowed s t ∅ labels).take 1).toFinset
    simp [ht]
  obtain ⟨_,h00,hzz⟩ := zeroPathSet_sound G s t D hf
  refine ⟨fs,hf,?_⟩
  rw [pathMatrix_zero_of_atoms D es h0 hz,pathMatrix_zero_of_atoms D fs h00 hzz]
  simp [RelativeSandwich,Loewner,Matrix.PosSemidef.zero]

theorem spectralPathSet_complete (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (hη : 0 < η)
    (es : List (Fin m)) (he : G.Path s t es) :
    ∃ fs ∈ spectralPathSet G s t D η, RelativeSandwich (η : ℝ)
      (pathMatrix (ratMatrixReal (D.atom none)) (fun e => ratMatrixReal (D.atom (some e))) es)
      (pathMatrix (ratMatrixReal (D.atom none)) (fun e => ratMatrixReal (D.atom (some e))) fs) := by
  have hηr : 0 ≤ (η : ℝ) := by exact_mod_cast hη.le
  by_cases hst : s = t
  · subst t
    have he0 := ExplicitDAG.Path.self_iff.mp he
    subst es
    refine ⟨[],by simp [spectralPathSet],?_⟩
    have hpsd := pathMatrix_psd (atom_real_psd D none) (fun e => atom_real_psd D (some e)) []
    constructor
    · simpa only [one_smul] using psd_smul_mono hpsd (show 1-(η:ℝ) ≤ 1 by linarith)
    · simpa only [one_smul] using psd_smul_mono hpsd (show 1 ≤ 1+(η:ℝ) by linarith)
  · by_cases hr0 : selectedRank D es.toFinset = 0
    · obtain ⟨h0,hz⟩ := (selectedRank_zero_iff D es.toFinset).mp hr0
      obtain ⟨fs,hfs,hrel⟩ := zeroPathSet_complete G s t D η es he h0
        (fun e he => hz e (List.mem_toFinset.mpr he))
      exact ⟨fs,by simp only [spectralPathSet,hst,if_false]; exact Finset.mem_union_left _ hfs,hrel⟩
    · obtain ⟨b,hb,ha,_⟩ := exists_accepted_trial D es.toFinset
      have hc := ((mem_trials _ _ _).mp hb).1
      have hi := ((mem_trials _ _ _).mp hb).2
      have hrpos : 0 < selectedRank D es.toFinset := Nat.pos_of_ne_zero hr0
      obtain ⟨fs,hfs,hrel⟩ := trialPathSet_complete G s t D η hη b
        (hc.symm ▸ hrpos) hi es he ha
      have hrle := selectedRank_le D es.toFinset
      let r : Fin p := ⟨selectedRank D es.toFinset - 1,by omega⟩
      have hre : r.val+1 = selectedRank D es.toFinset := by dsimp [r]; omega
      refine ⟨fs,?_,hrel⟩
      simp only [spectralPathSet,hst,if_false]
      apply Finset.mem_union_right
      apply Finset.mem_biUnion.mpr
      refine ⟨r,Finset.mem_univ _,Finset.mem_biUnion.mpr ⟨b,?_,hfs⟩⟩
      simpa only [hre] using hb

theorem spectralPathSet_empty_iff (G : ExplicitDAG v m) (s t : Fin v)
    (D : FactorData p m M) (η : ℚ) (hη : 0 < η) :
    spectralPathSet G s t D η = ∅ ↔ ¬ ∃ es, G.Path s t es := by
  constructor
  · intro h ⟨es,he⟩
    obtain ⟨fs,hfs,_⟩ := spectralPathSet_complete G s t D η hη es he
    simp [h] at hfs
  · intro h
    apply Finset.eq_empty_iff_forall_notMem.mpr
    intro es he
    exact h ⟨es,spectralPathSet_sound G s t D η he⟩

end NormalizationTrials
end DAGSpectral
