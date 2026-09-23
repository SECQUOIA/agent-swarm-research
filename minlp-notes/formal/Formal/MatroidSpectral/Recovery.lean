import Mathlib.Data.Finset.Card
import Mathlib.Data.List.FinRange
import Mathlib.Tactic

namespace MatroidSpectral

variable {α : Type*} [DecidableEq α]

/-- Test each listed column once. The second component counts the actual support
oracle calls. The oracle retains the original target family throughout the run. -/
def recoveryRun (oracle : Finset α → Bool) : List α → Finset α → Finset α × ℕ
  | [], retained => (retained, 0)
  | e :: es, retained =>
      let next := if oracle (retained.erase e) then retained.erase e else retained
      let rest := recoveryRun oracle es next
      (rest.1, rest.2 + 1)

theorem recoveryRun_calls (oracle : Finset α → Bool) (order : List α)
    (retained : Finset α) : (recoveryRun oracle order retained).2 = order.length := by
  induction order generalizing retained with
  | nil => rfl
  | cons e es ih => simp only [recoveryRun, ih, List.length_cons]

theorem recoveryRun_subset (oracle : Finset α → Bool) (order : List α)
    (retained : Finset α) : (recoveryRun oracle order retained).1 ⊆ retained := by
  induction order generalizing retained with
  | nil => exact Finset.Subset.refl _
  | cons e es ih =>
      simp only [recoveryRun]
      apply (ih _).trans
      split
      · exact Finset.erase_subset _ _
      · exact Finset.Subset.refl _

/-- A retained ground set supports a requested profile when it contains an actual
member of the fixed target family. In applications that family includes the
original represented-matroid rank and the requested profile. -/
def Supports (target : Finset α → Prop) (retained : Finset α) : Prop :=
  ∃ B, target B ∧ B ⊆ retained

omit [DecidableEq α] in
theorem supports_mono (target : Finset α → Prop) {S T : Finset α}
    (h : S ⊆ T) : Supports target S → Supports target T := by
  rintro ⟨B, hB, hBS⟩
  exact ⟨B, hB, hBS.trans h⟩

theorem recoveryRun_supports (target : Finset α → Prop) (oracle : Finset α → Bool)
    (hOracle : ∀ S, oracle S = true ↔ Supports target S)
    (order : List α) (retained : Finset α) (h : Supports target retained) :
    Supports target (recoveryRun oracle order retained).1 := by
  induction order generalizing retained with
  | nil => exact h
  | cons e es ih =>
      simp only [recoveryRun]
      apply ih
      split
      · exact (hOracle _).mp (by assumption)
      · exact h

/-- Every surviving processed column is indispensable. A rejected deletion
stays rejected after later columns are removed, by monotonicity of support. -/
theorem recoveryRun_indispensable (target : Finset α → Prop)
    (oracle : Finset α → Bool)
    (hOracle : ∀ S, oracle S = true ↔ Supports target S)
    (order : List α) (retained : Finset α) {e : α} (he : e ∈ order)
    (hmem : e ∈ (recoveryRun oracle order retained).1) :
    ¬ Supports target ((recoveryRun oracle order retained).1.erase e) := by
  induction order generalizing retained with
  | nil => simp at he
  | cons f fs ih =>
      rcases List.mem_cons.mp he with rfl | he
      · by_cases htest : oracle (retained.erase e) = true
        · have hsub := recoveryRun_subset oracle fs (retained.erase e)
          simp only [recoveryRun, htest, ↓reduceIte] at hmem
          exact False.elim ((Finset.mem_erase.mp (hsub hmem)).1 rfl)
        · simp only [recoveryRun, htest, Bool.false_eq_true, ↓reduceIte] at hmem ⊢
          intro hs
          apply htest
          apply (hOracle _).mpr
          apply supports_mono target (Finset.erase_subset_erase e
            (recoveryRun_subset oracle fs retained)) hs
      · simp only [recoveryRun] at hmem ⊢
        exact ih _ he hmem

/-- If the scan covers the initial ground, the result is an actual requested
member, not merely a retained set that still contains one. -/
theorem recoveryRun_target (target : Finset α → Prop) (oracle : Finset α → Bool)
    (hOracle : ∀ S, oracle S = true ↔ Supports target S)
    (order : List α) (retained : Finset α)
    (hCover : ∀ e ∈ retained, e ∈ order) (h : Supports target retained) :
    target (recoveryRun oracle order retained).1 := by
  obtain ⟨B, hB, hsub⟩ := recoveryRun_supports target oracle hOracle order retained h
  have heq : (recoveryRun oracle order retained).1 = B := by
    apply Finset.Subset.antisymm _ hsub
    intro e he
    by_contra hn
    have hord := hCover e (recoveryRun_subset oracle order retained he)
    apply recoveryRun_indispensable target oracle hOracle order retained hord he
    refine ⟨B, hB, ?_⟩
    intro f hf
    exact Finset.mem_erase.mpr ⟨fun hfe => hn (hfe ▸ hf), hsub hf⟩
  simpa only [heq] using hB

/-- Recover a requested base with a fixed full-ground column order. -/
def recoverBasis {m : ℕ} (oracle : Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) : Finset (Fin m) × ℕ :=
  recoveryRun oracle (List.finRange m) retained

theorem recoverBasis_calls {m : ℕ} (oracle : Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) : (recoverBasis oracle retained).2 = m := by
  simp only [recoverBasis, recoveryRun_calls, List.length_finRange]

theorem recoverBasis_subset {m : ℕ} (oracle : Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) : (recoverBasis oracle retained).1 ⊆ retained :=
  recoveryRun_subset oracle _ _

theorem recoverBasis_target {m : ℕ} (target : Finset (Fin m) → Prop)
    (oracle : Finset (Fin m) → Bool)
    (hOracle : ∀ S, oracle S = true ↔ Supports target S)
    (retained : Finset (Fin m)) (h : Supports target retained) :
    target (recoverBasis oracle retained).1 :=
  recoveryRun_target target oracle hOracle _ retained
    (fun _ _ => List.mem_finRange _) h

/-- The recovered base has the original prescribed rank; no support test changes
that rank even when its retained column set loses rank. -/
theorem recoverBasis_card {m q : ℕ} (target : Finset (Fin m) → Prop)
    (oracle : Finset (Fin m) → Bool)
    (hOracle : ∀ S, oracle S = true ↔ Supports target S)
    (hRank : ∀ B, target B → B.card = q)
    (retained : Finset (Fin m)) (h : Supports target retained) :
    (recoverBasis oracle retained).1.card = q :=
  hRank _ (recoverBasis_target target oracle hOracle retained h)

theorem recoverBasis_rank_zero {m : ℕ} (target : Finset (Fin m) → Prop)
    (oracle : Finset (Fin m) → Bool)
    (hOracle : ∀ S, oracle S = true ↔ Supports target S)
    (hRank : ∀ B, target B → B.card = 0)
    (retained : Finset (Fin m)) (h : Supports target retained) :
    (recoverBasis oracle retained).1 = ∅ :=
  Finset.card_eq_zero.mp (recoverBasis_card target oracle hOracle hRank retained h)

/-- The rank-zero case has a unique possible base and needs no oracle call. -/
def recoverBasisAtRank {m : ℕ} (q : ℕ) (oracle : Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) : Finset (Fin m) × ℕ :=
  if q = 0 then (∅, 0) else recoverBasis oracle retained

theorem recoverBasisAtRank_zero {m : ℕ} (oracle : Finset (Fin m) → Bool)
    (retained : Finset (Fin m)) : recoverBasisAtRank 0 oracle retained = (∅, 0) := by
  simp [recoverBasisAtRank]

theorem recoverBasisAtRank_calls {m : ℕ} (q : ℕ)
    (oracle : Finset (Fin m) → Bool) (retained : Finset (Fin m)) :
    (recoverBasisAtRank q oracle retained).2 ≤ m := by
  by_cases hq : q = 0
  · simp [recoverBasisAtRank, hq]
  · simp [recoverBasisAtRank, hq, recoverBasis_calls]

theorem recoverBasisAtRank_target {m q : ℕ} (target : Finset (Fin m) → Prop)
    (oracle : Finset (Fin m) → Bool)
    (hOracle : ∀ S, oracle S = true ↔ Supports target S)
    (hRank : ∀ B, target B → B.card = q)
    (retained : Finset (Fin m)) (h : Supports target retained) :
    target (recoverBasisAtRank q oracle retained).1 := by
  by_cases hq : q = 0
  · obtain ⟨B, hB, _⟩ := h
    have hBzero : B = ∅ := Finset.card_eq_zero.mp (hq ▸ hRank B hB)
    simpa only [recoverBasisAtRank, hq, ↓reduceIte, hBzero] using hB
  · simpa only [recoverBasisAtRank, hq, ↓reduceIte] using
      recoverBasis_target target oracle hOracle retained h

/-- Too few retained columns cannot pass a support test for the original rank. -/
theorem supportOracle_rejects_small_ground {m q : ℕ}
    (target : Finset (Fin m) → Prop) (oracle : Finset (Fin m) → Bool)
    (hOracle : ∀ S, oracle S = true ↔ Supports target S)
    (hRank : ∀ B, target B → B.card = q)
    (retained : Finset (Fin m)) (hsmall : retained.card < q) :
    oracle retained = false := by
  cases horacle : oracle retained with
  | false => rfl
  | true =>
      obtain ⟨B, hB, hsub⟩ := (hOracle retained).mp horacle
      have hcard := Finset.card_le_card hsub
      rw [hRank B hB] at hcard
      exact False.elim (Nat.not_le_of_lt hsmall hcard)

end MatroidSpectral
