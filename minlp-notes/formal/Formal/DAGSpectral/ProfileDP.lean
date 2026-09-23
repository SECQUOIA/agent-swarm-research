import Formal.DAGSpectral.Profiles

namespace DAGSpectral.ExplicitDAG
variable {v m : ℕ} {κ : Type*} [Fintype κ]

abbrev PathTable (v m : ℕ) := Fin v → List (List (Fin m))

/-- Only stored representatives are extended. No path enumeration occurs here. -/
def candidates (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s t : Fin v)
    (table : PathTable v m) : List (List (Fin m)) :=
  (if t = s then [[]] else []) ++
  ((List.finRange m).filter (fun e => decide (G.dst e = t) && allowed e)).flatMap
    (fun e => (table (G.src e)).map (fun es => es ++ [e]))

theorem candidates_mem (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s t : Fin v)
    (table : PathTable v m) (es : List (Fin m)) :
    es ∈ candidates G allowed s t table ↔
      (t = s ∧ es = []) ∨ ∃ e, G.dst e = t ∧ allowed e = true ∧
        ∃ pre ∈ table (G.src e), pre ++ [e] = es := by
  simp only [candidates, List.mem_append, List.mem_flatMap, List.mem_filter,
    List.mem_finRange, true_and, Bool.and_eq_true, decide_eq_true_eq, List.mem_map]
  by_cases h : t = s <;> simp [h]
  all_goals aesop

/-- Process vertices in their given topological order. -/
def run (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) : ℕ → PathTable v m
  | 0 => fun _ => []
  | n+1 =>
    let old := run G allowed s required label n
    if hn : n < v then
      let t : Fin v := ⟨n,hn⟩
      Function.update old t (DAGSpectral.representatives (stateKey required label)
        (candidates G allowed s t old))
    else old

def output (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s t : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) : List (List (Fin m)) :=
  (run G allowed s required label v t).filter (fun es => decide (ownerMask required es = required))

variable (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
  (required : Finset (Fin m)) (label : Fin m → κ → ℤ)

theorem candidates_sound (table : PathTable v m) (t : Fin v)
    (hs : ∀ u es, es ∈ table u → G.AllowedPath allowed s u es)
    {es : List (Fin m)} (he : es ∈ candidates G allowed s t table) :
    G.AllowedPath allowed s t es := by
  rcases (candidates_mem G allowed s t table es).mp he with ⟨rfl,rfl⟩ | ⟨e,htgt,ha,pre,hpre,rfl⟩
  · exact AllowedPath.nil allowed _
  · rw [← htgt]
    exact (hs _ _ hpre).snoc e rfl ha

theorem run_sound (n : ℕ) (t : Fin v) (es : List (Fin m))
    (he : es ∈ run G allowed s required label n t) : G.AllowedPath allowed s t es := by
  induction n generalizing t es with
  | zero => simp [run] at he
  | succ n ih =>
    by_cases hn : n < v
    · by_cases ht : t = ⟨n,hn⟩
      · subst t
        simp only [run, hn, ↓reduceDIte, Function.update_self] at he
        exact candidates_sound G allowed s _ _ (fun u es hm => ih u es hm)
          (DAGSpectral.representatives_subset _ _ he)
      · simp only [run, hn, ↓reduceDIte, Function.update_of_ne ht] at he
        exact ih _ _ he
    · simp only [run, hn, ↓reduceDIte] at he
      exact ih _ _ he

omit [Fintype κ] in
/-- Completeness needs only predecessors, not a list of all actual paths. -/
theorem candidates_complete (table : PathTable v m) (t : Fin v)
    (hc : ∀ u, u < t → ∀ es, G.AllowedPath allowed s u es →
      ∃ rep ∈ table u, stateKey required label rep = stateKey required label es)
    {es : List (Fin m)} (he : G.AllowedPath allowed s t es) :
    ∃ rep ∈ candidates G allowed s t table,
      stateKey required label rep = stateKey required label es := by
  rcases he with ⟨hp,ha⟩
  cases hp with
  | nil =>
    exact ⟨[], (candidates_mem G allowed s s table []).mpr (Or.inl ⟨rfl,rfl⟩), rfl⟩
  | @snoc u pre hp e hsrc =>
    have hu : u < G.dst e := hsrc ▸ G.forward e
    have hpre : G.AllowedPath allowed s u pre :=
      ⟨hp, fun f hf => ha f (List.mem_append_left _ hf)⟩
    obtain ⟨rep,hr,hkey⟩ := hc u hu pre hpre
    refine ⟨rep ++ [e], ?_, stateKey_extension required label hkey e⟩
    apply (candidates_mem G allowed s (G.dst e) table _).mpr
    refine Or.inr ⟨e,rfl,ha e (by simp),rep,?_,rfl⟩
    simpa only [hsrc] using hr

theorem run_complete (n : ℕ) (hn : n ≤ v) (t : Fin v) (ht : t.val < n)
    (es : List (Fin m)) (he : G.AllowedPath allowed s t es) :
    ∃ rep ∈ run G allowed s required label n t,
      stateKey required label rep = stateKey required label es := by
  induction n generalizing t es with
  | zero => omega
  | succ n ih =>
    have hnv : n < v := by omega
    by_cases htn : t.val = n
    · have hte : t = ⟨n,hnv⟩ := Fin.ext htn
      subst t
      obtain ⟨rep,hr,hkey⟩ := candidates_complete G allowed s required label
        (run G allowed s required label n) ⟨n,hnv⟩ (fun u hu pre hp =>
          ih (by omega) u hu pre hp) he
      obtain ⟨rep',hr',hkey'⟩ := DAGSpectral.representatives_complete (stateKey required label) hr
      refine ⟨rep', ?_, hkey'.trans hkey⟩
      simpa only [run, hnv, ↓reduceDIte, Function.update_self] using hr'
    · obtain ⟨rep,hr,hkey⟩ := ih (by omega) t (by omega) es he
      refine ⟨rep, ?_, hkey⟩
      have hne : t ≠ ⟨n,hnv⟩ := by intro he; exact htn (congrArg Fin.val he)
      simpa only [run, hnv, ↓reduceDIte, Function.update_of_ne hne] using hr

theorem run_unique (n : ℕ) (t : Fin v) :
    ((run G allowed s required label n t).map (stateKey required label)).Nodup := by
  induction n with
  | zero => simp [run]
  | succ n ih =>
    by_cases hn : n < v
    · by_cases ht : t = ⟨n,hn⟩
      · subst t
        simp only [run, hn, reduceDIte, Function.update_self]
        exact DAGSpectral.representatives_keys_nodup _ _
      · simpa only [run, hn, reduceDIte, Function.update_of_ne ht] using ih
    · simpa only [run, hn, reduceDIte] using ih

theorem output_sound (t : Fin v) {es : List (Fin m)}
    (he : es ∈ output G allowed s t required label) :
    G.AllowedPath allowed s t es ∧ required ⊆ es.toFinset := by
  obtain ⟨hp,hm⟩ := List.mem_filter.mp he
  have heq : ownerMask required es = required := of_decide_eq_true hm
  refine ⟨run_sound G allowed s required label v t es hp, ?_⟩
  rw [← heq]
  exact Finset.inter_subset_right

theorem output_complete (t : Fin v) (es : List (Fin m))
    (he : G.AllowedPath allowed s t es) (hr : required ⊆ es.toFinset) :
    ∃ rep ∈ output G allowed s t required label,
      stateKey required label rep = stateKey required label es := by
  obtain ⟨rep,hrep,hkey⟩ := run_complete G allowed s required label v le_rfl t t.isLt es he
  have hm : ownerMask required rep = ownerMask required es := congrArg Prod.fst hkey
  have hfull : ownerMask required es = required := Finset.inter_eq_left.mpr hr
  refine ⟨rep, List.mem_filter.mpr ⟨hrep, ?_⟩, hkey⟩
  exact decide_eq_true (hm.trans hfull)

theorem output_nil_iff (t : Fin v) : output G allowed s t required label = [] ↔
    ¬ ∃ es, G.AllowedPath allowed s t es ∧ required ⊆ es.toFinset := by
  constructor
  · intro h ⟨es,he,hr⟩
    obtain ⟨rep,hrep,_⟩ := output_complete G allowed s required label t es he hr
    simp [h] at hrep
  · intro h
    apply List.eq_nil_iff_forall_not_mem.mpr
    intro es he
    exact h ⟨es, output_sound G allowed s required label t he⟩

theorem output_nodup (t : Fin v) : (output G allowed s t required label).Nodup := by
  exact (List.Nodup.of_map _ (run_unique G allowed s required label v t)).filter _

theorem output_self_mem (es : List (Fin m)) :
    es ∈ output G allowed s s required label ↔ es = [] ∧ required = ∅ := by
  constructor
  · intro he
    obtain ⟨hp,hr⟩ := output_sound G allowed s required label s he
    have hn := Path.self_iff.mp hp.1
    refine ⟨hn, ?_⟩
    simpa only [hn, List.toFinset_nil, Finset.subset_empty] using hr
  · rintro ⟨rfl,rfl⟩
    obtain ⟨rep,hrep,_⟩ := output_complete G allowed s ∅ label s []
      (AllowedPath.nil allowed s) (by simp)
    have hn := Path.self_iff.mp (output_sound G allowed s ∅ label s hrep).1.1
    simpa only [hn] using hrep

theorem output_self : output G allowed s s required label =
    if required = ∅ then [[]] else [] := by
  by_cases hr : required = ∅
  · rw [if_pos hr]
    have hm : [] ∈ output G allowed s s required label :=
      (output_self_mem G allowed s required label []).mpr ⟨rfl,hr⟩
    have hn := output_nodup G allowed s required label s
    have hall : ∀ es ∈ output G allowed s s required label, es = [] :=
      fun es he => ((output_self_mem G allowed s required label es).mp he).1
    generalize output G allowed s s required label = xs at hm hn hall ⊢
    cases xs with
    | nil => simp at hm
    | cons a tail =>
      have ha := hall a (by simp)
      subst a
      have ht : tail = [] := by
        apply List.eq_nil_iff_forall_not_mem.mpr
        intro es he
        have heq := hall es (by simp [he])
        exact (List.nodup_cons.mp hn).1 (heq ▸ he)
      rw [ht]
  · rw [if_neg hr]
    apply List.eq_nil_iff_forall_not_mem.mpr
    intro es he
    exact hr ((output_self_mem G allowed s required label es).mp he).2

end DAGSpectral.ExplicitDAG
