import Formal.DAGSpectral.CriteriaBasic

namespace DAGSpectral

/-- One comparison per additional candidate, retaining an actual candidate. -/
def bestFrom {α : Type*} (better : α → α → Bool) (a : α) (xs : List α) : α :=
  xs.foldl (fun b c => if better b c then c else b) a

def bestBy {α : Type*} (better : α → α → Bool) : List α → Option α
  | [] => none
  | a::xs => some (bestFrom better a xs)

/-- The exact comparison pairs executed by the selector, in execution order. -/
def bestFromWithTrace {α : Type*} (better : α → α → Bool) (a : α) :
    List α → α × List (α × α)
  | [] => (a,[])
  | b::xs =>
    let r := bestFromWithTrace better (if better a b then b else a) xs
    (r.1,(a,b)::r.2)

def bestByWithTrace {α : Type*} (better : α → α → Bool) :
    List α → Option α × List (α × α)
  | [] => (none,[])
  | a::xs => let r := bestFromWithTrace better a xs; (some r.1,r.2)

theorem bestFromWithTrace_result {α : Type*} (better : α → α → Bool) (a : α) (xs : List α) :
    (bestFromWithTrace better a xs).1 = bestFrom better a xs := by
  induction xs generalizing a with
  | nil => rfl
  | cons b xs ih => simpa only [bestFromWithTrace, bestFrom, List.foldl_cons] using ih _

theorem bestFromWithTrace_length {α : Type*} (better : α → α → Bool) (a : α) (xs : List α) :
    (bestFromWithTrace better a xs).2.length = xs.length := by
  induction xs generalizing a with
  | nil => rfl
  | cons b xs ih => simp [bestFromWithTrace,ih]

theorem bestByWithTrace_result {α : Type*} (better : α → α → Bool) (xs : List α) :
    (bestByWithTrace better xs).1 = bestBy better xs := by
  cases xs <;> simp [bestByWithTrace,bestBy,bestFromWithTrace_result]

theorem bestByWithTrace_length {α : Type*} (better : α → α → Bool) (xs : List α) :
    (bestByWithTrace better xs).2.length = xs.length-1 := by
  cases xs <;> simp [bestByWithTrace,bestFromWithTrace_length]

theorem bestFrom_spec {α β : Type*} [LinearOrder β]
    (better : α → α → Bool) (score : α → β) (P : α → Prop)
    (hcompare : ∀ a, P a → ∀ b, P b → (better a b = true ↔ score a ≤ score b))
    (a : α) (ha : P a) (xs : List α) (hxs : ∀ b ∈ xs, P b) :
    bestFrom better a xs ∈ a::xs ∧ P (bestFrom better a xs) ∧
      ∀ b ∈ a::xs, score b ≤ score (bestFrom better a xs) := by
  induction xs generalizing a with
  | nil => simp [bestFrom,ha]
  | cons b xs ih =>
    have hb := hxs b (by simp)
    have hs : ∀ c ∈ xs, P c := fun c hc => hxs c (by simp [hc])
    cases hh : better a b with
    | false =>
      have hba : score b ≤ score a := le_of_not_ge (by
        intro hab
        have := (hcompare a ha b hb).mpr hab
        simp [hh] at this)
      obtain ⟨hm,hp,hscores⟩ := ih a ha hs
      simp only [bestFrom, List.foldl_cons, hh, Bool.false_eq_true, ↓reduceIte] at *
      refine ⟨?_,hp,?_⟩
      · simp only [List.mem_cons] at hm ⊢
        tauto
      · intro c hc
        rcases List.mem_cons.mp hc with hca | hc
        · subst c
          exact hscores a (by simp)
        rcases List.mem_cons.mp hc with hcb | hc
        · subst c
          exact hba.trans (hscores a (by simp))
        · exact hscores c (by simp [hc])
    | true =>
      have hab := (hcompare a ha b hb).mp hh
      obtain ⟨hm,hp,hscores⟩ := ih b hb hs
      simp only [bestFrom, List.foldl_cons, hh, ↓reduceIte] at *
      refine ⟨?_,hp,?_⟩
      · exact List.mem_cons_of_mem _ hm
      · intro c hc
        rcases List.mem_cons.mp hc with hca | hc
        · subst c
          exact hab.trans (hscores b (by simp))
        · exact hscores c hc

theorem bestBy_eq_none_iff {α : Type*} (better : α → α → Bool) (xs : List α) :
    bestBy better xs = none ↔ xs = [] := by cases xs <;> simp [bestBy]

theorem bestBy_spec {α β : Type*} [LinearOrder β]
    (better : α → α → Bool) (score : α → β) (P : α → Prop)
    (hcompare : ∀ a, P a → ∀ b, P b → (better a b = true ↔ score a ≤ score b))
    (xs : List α) (hxs : ∀ a ∈ xs, P a) {b : α} (hb : bestBy better xs = some b) :
    b ∈ xs ∧ P b ∧ ∀ a ∈ xs, score a ≤ score b := by
  cases xs with
  | nil => simp [bestBy] at hb
  | cons a xs =>
    simp only [bestBy, Option.some.injEq] at hb
    subst b
    exact bestFrom_spec better score P hcompare a (hxs a (by simp)) xs
      (fun b hb => hxs b (by simp [hb]))

theorem bestBy_exists {α : Type*} (better : α → α → Bool) (xs : List α)
    (hxs : xs ≠ []) : ∃ b, bestBy better xs = some b := by
  cases xs with
  | nil => exact (hxs rfl).elim
  | cons a xs => exact ⟨_,rfl⟩

/-- Only stored candidates are compared. A cover turns the selector's finite
maximum into its comparison guarantee for every feasible object. -/
theorem IsRelativeCover.bestBy_guarantee {α β : Type*} [DecidableEq α] [LinearOrder β]
    {n : ℕ} {η : ℝ} {J : α → RealMatrix n} {F : Finset α} {xs : List α}
    (h : IsRelativeCover η J F xs.toFinset) (better : α → α → Bool)
    (score lower : α → β)
    (hcompare : ∀ a ∈ F, ∀ b ∈ F, better a b = true ↔ score a ≤ score b)
    (hlower : ∀ a ∈ F, ∀ b ∈ F, RelativeSandwich η (J a) (J b) → lower a ≤ score b)
    {b : α} (hb : bestBy better xs = some b) :
    b ∈ F ∧ ∀ a ∈ F, lower a ≤ score b := by
  have hs := bestBy_spec better score (fun a => a ∈ F) hcompare xs
    (fun a ha => h.1 (List.mem_toFinset.mpr ha)) hb
  refine ⟨hs.2.1,?_⟩
  intro a ha
  obtain ⟨c,hc,hsc⟩ := h.2 a ha
  exact (hlower a ha c (h.1 hc) hsc).trans (hs.2.2 c (List.mem_toFinset.mp hc))

end DAGSpectral
