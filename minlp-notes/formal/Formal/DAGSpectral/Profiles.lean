import Formal.DAGSpectral.Graph

namespace DAGSpectral

/-- Keep one actual object for each key, without enumerating any new objects. -/
def representatives {α κ : Type*} [DecidableEq κ] (key : α → κ) (xs : List α) : List α :=
  xs.pwFilter (fun a b => key a ≠ key b)

theorem representatives_subset {α κ : Type*} [DecidableEq κ] (key : α → κ) (xs : List α) :
    representatives key xs ⊆ xs := List.pwFilter_subset _

theorem representatives_keys {α κ : Type*} [DecidableEq κ] (key : α → κ) (xs : List α) :
    (representatives key xs).map key = (xs.map key).dedup := by
  exact (List.pwFilter_map (R := (· ≠ ·)) key xs).symm

theorem representatives_keys_nodup {α κ : Type*} [DecidableEq κ]
    (key : α → κ) (xs : List α) : ((representatives key xs).map key).Nodup := by
  rw [representatives_keys]
  exact List.nodup_dedup _

theorem representatives_complete {α κ : Type*} [DecidableEq κ]
    (key : α → κ) {xs : List α} {x : α} (hx : x ∈ xs) :
    ∃ y ∈ representatives key xs, key y = key x := by
  have h : key x ∈ (representatives key xs).map key := by
    rw [representatives_keys, List.mem_dedup]
    exact List.mem_map.mpr ⟨x,hx,rfl⟩
  exact List.mem_map.mp h

namespace ExplicitDAG
variable {v m : ℕ} {κ : Type*}

def profile (label : Fin m → κ → ℤ) (es : List (Fin m)) : κ → ℤ :=
  (es.map label).sum

def ownerMask (required : Finset (Fin m)) (es : List (Fin m)) : Finset (Fin m) :=
  required ∩ es.toFinset

def stateKey (required : Finset (Fin m)) (label : Fin m → κ → ℤ)
    (es : List (Fin m)) := (ownerMask required es, profile label es)

@[simp] theorem profile_nil (label : Fin m → κ → ℤ) : profile label [] = 0 := rfl
@[simp] theorem profile_append (label : Fin m → κ → ℤ) (es fs : List (Fin m)) :
    profile label (es ++ fs) = profile label es + profile label fs := by
  simp [profile]
@[simp] theorem profile_singleton (label : Fin m → κ → ℤ) (e : Fin m) :
    profile label [e] = label e := by simp [profile]

@[simp] theorem profile_apply (label : Fin m → κ → ℤ) (es : List (Fin m)) (i : κ) :
    profile label es i = (es.map (fun e => label e i)).sum := by
  induction es with
  | nil => rfl
  | cons e es ih =>
    simp only [profile, List.map_cons, List.sum_cons, Pi.add_apply] at ih ⊢
    rw [ih]

@[simp] theorem ownerMask_nil (required : Finset (Fin m)) : ownerMask required [] = ∅ := by
  simp [ownerMask]

theorem ownerMask_subset (required : Finset (Fin m)) (es : List (Fin m)) :
    ownerMask required es ⊆ required := Finset.inter_subset_left

@[simp] theorem ownerMask_append (required : Finset (Fin m)) (es fs : List (Fin m)) :
    ownerMask required (es ++ fs) = ownerMask required es ∪ ownerMask required fs := by
  simp only [ownerMask, List.toFinset_append, Finset.inter_union_distrib_left]

theorem stateKey_extension (required : Finset (Fin m)) (label : Fin m → κ → ℤ)
    {es fs : List (Fin m)} (h : stateKey required label es = stateKey required label fs)
    (e : Fin m) : stateKey required label (es ++ [e]) = stateKey required label (fs ++ [e]) := by
  have hm := congrArg Prod.fst h
  have hp := congrArg Prod.snd h
  simp only [stateKey] at hm hp ⊢
  simp only [ownerMask_append, profile_append, hm, hp]

end ExplicitDAG
end DAGSpectral
