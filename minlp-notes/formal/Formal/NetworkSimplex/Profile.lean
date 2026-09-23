import Mathlib

/-! Exact common-profile reconstruction for a chain of parallel-arc gadgets. -/
namespace NetworkSimplex
namespace Chain

open Finset

variable {J : Type*} [Fintype J]

/-- Every total between zero and the sum of nonnegative capacities can be allocated. -/
theorem exists_bounded_sum (w : J → ℝ) (hw : ∀ j, 0 ≤ w j) (r : ℝ)
    (hr : 0 ≤ r) (hrw : r ≤ ∑ j, w j) :
    ∃ f : J → ℝ, (∀ j, 0 ≤ f j ∧ f j ≤ w j) ∧ ∑ j, f j = r := by
  let W := ∑ j, w j
  have hW : 0 ≤ W := Finset.sum_nonneg fun j _ => hw j
  by_cases hzero : W = 0
  · have hrzero : r = 0 := by change r ≤ W at hrw; linarith
    refine ⟨fun _ => 0, fun j => ⟨le_rfl, hw j⟩, ?_⟩
    simp [hrzero]
  · have hpos : 0 < W := lt_of_le_of_ne hW (Ne.symm hzero)
    have hq : 0 ≤ r / W := div_nonneg hr hW
    have hqone : r / W ≤ 1 := (div_le_one hpos).2 hrw
    refine ⟨fun j => (r / W) * w j, fun j => ⟨mul_nonneg hq (hw j), ?_⟩, ?_⟩
    · nlinarith [hw j]
    · rw [← Finset.mul_sum]
      change r / W * W = r
      exact div_mul_cancel₀ r hzero

/-- Independent real intervals have every sum between their endpoint sums. -/
theorem exists_interval_sum (lo hi : J → ℝ) (h : ∀ j, lo j ≤ hi j) (r : ℝ)
    (hl : ∑ j, lo j ≤ r) (hu : r ≤ ∑ j, hi j) :
    ∃ f : J → ℝ, (∀ j, lo j ≤ f j ∧ f j ≤ hi j) ∧ ∑ j, f j = r := by
  obtain ⟨g, hg, hsum⟩ := exists_bounded_sum (fun j => hi j - lo j)
    (fun j => sub_nonneg.mpr (h j)) (r - ∑ j, lo j) (sub_nonneg.mpr hl)
    (by rw [Finset.sum_sub_distrib]; linarith)
  refine ⟨fun j => lo j + g j, fun j => ⟨by linarith [(hg j).1],
    by linarith [(hg j).2]⟩, ?_⟩
  rw [Finset.sum_add_distrib, hsum]
  ring

inductive StateClass where
  | aOnly | bOnly | both | neither
  deriving DecidableEq

open StateClass

def observesA (s : StateClass) : Prop := s = aOnly ∨ s = both
def observesB (s : StateClass) : Prop := s = bOnly ∨ s = both
instance (s : StateClass) : Decidable (observesA s) := by unfold observesA; infer_instance
instance (s : StateClass) : Decidable (observesB s) := by unfold observesB; infer_instance

def fixedA (c : J → StateClass) (u v w : J → ℝ) (j : J) : ℝ :=
  match c j with
  | aOnly | both => u j
  | bOnly => w j - v j
  | neither => 0

def freeA (c : J → StateClass) (w : J → ℝ) (j : J) : ℝ :=
  if c j = neither then w j else 0

def bSum (c : J → StateClass) (w : J → ℝ) : ℝ :=
  ∑ j, if c j = bOnly then w j else 0

def residual (c : J → StateClass) (u v : J → ℝ) (xa : ℝ) : ℝ :=
  xa - (∑ j, if observesA (c j) then u j else 0) +
    (∑ j, if c j = bOnly then v j else 0)

/-- The nonnegativity checks apply exactly to coordinates that are observed. -/
def ObservedNonnegative (c : J → StateClass) (u v : J → ℝ) : Prop :=
  (∀ j, observesA (c j) → 0 ≤ u j) ∧ (∀ j, observesB (c j) → 0 ≤ v j)

def GadgetProfile (c : J → StateClass) (u v w : J → ℝ) (xa : ℝ) : Prop :=
  (∀ j, c j = aOnly → u j ≤ w j) ∧
  (∀ j, c j = bOnly → v j ≤ w j) ∧
  (∀ j, c j = both → w j = u j + v j) ∧
  bSum c w ≤ residual c u v xa ∧
  residual c u v xa ≤ bSum c w + ∑ j, freeA c w j

/-- The a-arc entries determine b-arc entries by subtraction from the common profile. -/
def GadgetDisaggregation (c : J → StateClass) (u v w : J → ℝ) (xa : ℝ) : Prop :=
  ∃ a : J → ℝ, (∀ j, 0 ≤ a j ∧ a j ≤ w j) ∧
    (∀ j, observesA (c j) → a j = u j) ∧
    (∀ j, observesB (c j) → w j - a j = v j) ∧ ∑ j, a j = xa

theorem sum_fixedA (c : J → StateClass) (u v w : J → ℝ) :
    (∑ j, fixedA c u v w j) =
      (∑ j, if observesA (c j) then u j else 0) + bSum c w -
        (∑ j, if c j = bOnly then v j else 0) := by
  simp only [bSum, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro j _
  cases hc : c j <;> simp [fixedA, hc, observesA]

theorem gadget_profile_iff (c : J → StateClass) (u v w : J → ℝ) (xa : ℝ)
    (hw : ∀ j, 0 ≤ w j) (hn : ObservedNonnegative c u v) :
    GadgetProfile c u v w xa ↔ GadgetDisaggregation c u v w xa := by
  constructor
  · rintro ⟨hA, hB, hT, hlo, hhi⟩
    have hfixed : ∀ j, 0 ≤ fixedA c u v w j ∧
        fixedA c u v w j + freeA c w j ≤ w j := by
      intro j
      cases hc : c j with
      | aOnly =>
          simpa [fixedA, freeA, hc] using
            And.intro (hn.1 j (by simp [observesA, hc])) (hA j hc)
      | bOnly =>
          have hv := hn.2 j (by simp [observesB, hc])
          have hbw := hB j hc
          simp only [fixedA, freeA, hc, reduceCtorEq, ↓reduceIte, add_zero]
          constructor <;> linarith
      | both =>
          have hu := hn.1 j (by simp [observesA, hc])
          have hv := hn.2 j (by simp [observesB, hc])
          have ht := hT j hc
          simp only [fixedA, freeA, hc, reduceCtorEq, ↓reduceIte, add_zero]
          exact ⟨hu, by linarith⟩
      | neither => simp [fixedA, freeA, hc]
    have hfree : ∀ j, 0 ≤ freeA c w j := by intro j; simp [freeA]; split <;> simp_all
    have hsum := sum_fixedA c u v w
    obtain ⟨a, ha, hasum⟩ := exists_interval_sum (fixedA c u v w)
      (fun j => fixedA c u v w j + freeA c w j)
      (fun j => le_add_of_nonneg_right (hfree j)) xa
      (by unfold residual at hlo; linarith)
      (by rw [Finset.sum_add_distrib]; unfold residual at hhi; linarith)
    refine ⟨a, fun j => ⟨le_trans (hfixed j).1 (ha j).1,
      le_trans (ha j).2 (hfixed j).2⟩, ?_, ?_, hasum⟩
    · intro j hj
      have hal := (ha j).1
      have hau := (ha j).2
      rcases hj with hj | hj <;> simp [fixedA, freeA, hj] at hal hau <;> linarith
    · intro j hj
      have hal := (ha j).1
      have hau := (ha j).2
      rcases hj with hj | hj
      · simp [fixedA, freeA, hj] at hal hau
        linarith
      · have ht := hT j hj
        simp [fixedA, freeA, hj] at hal hau
        linarith
  · rintro ⟨a, ha, hA, hB, hasum⟩
    have hinter : ∀ j, fixedA c u v w j ≤ a j ∧
        a j ≤ fixedA c u v w j + freeA c w j := by
      intro j
      cases hc : c j with
      | aOnly => simp [fixedA, freeA, hc, hA j (by simp [observesA, hc])]
      | bOnly =>
          have hb := hB j (by simp [observesB, hc])
          simp only [fixedA, freeA, hc, reduceCtorEq, ↓reduceIte, add_zero]
          constructor <;> linarith
      | both => simp [fixedA, freeA, hc, hA j (by simp [observesA, hc])]
      | neither => simpa [fixedA, freeA, hc] using ha j
    have hsum := sum_fixedA c u v w
    have hlo := Finset.sum_le_sum fun j (_ : j ∈ (Finset.univ : Finset J)) => (hinter j).1
    have hhi := Finset.sum_le_sum fun j (_ : j ∈ (Finset.univ : Finset J)) => (hinter j).2
    rw [hasum] at hlo hhi
    rw [Finset.sum_add_distrib] at hhi
    refine ⟨?_, ?_, ?_, ?_, ?_⟩
    · intro j hj
      rw [← hA j (by simp [observesA, hj])]
      exact (ha j).2
    · intro j hj
      have hb := hB j (by simp [observesB, hj])
      linarith [(ha j).1]
    · intro j hj
      have hab := hA j (by simp [observesA, hj])
      have hbb := hB j (by simp [observesB, hj])
      linarith
    · unfold residual
      linarith
    · unfold residual
      linarith


variable {I : Type*}

/-- The complete profile system, before eliminating the residual state. -/
def Profile (c : I → J → StateClass) (u v : I → J → ℝ) (weights : J → ℝ)
    (xa : I → ℝ) (xh : ℝ) (observedH : J → Prop) (zh w : J → ℝ) : Prop :=
  (∀ j, 0 ≤ w j ∧ w j ≤ weights j) ∧
  (∑ j, w j) = 1 - xh ∧
  (∀ j, observedH j → w j = weights j - zh j) ∧
  ∀ i, GadgetProfile (c i) (u i) (v i) w (xa i)

structure StateFlows (I J : Type*) where
  a : I → J → ℝ
  b : I → J → ℝ
  h : J → ℝ

/-- Full state capacities, balances, aggregates, and all observed entries. -/
def ValidStateFlows (c : I → J → StateClass) (u v : I → J → ℝ)
    (weights : J → ℝ) (xa xb : I → ℝ) (xh : ℝ)
    (observedH : J → Prop) (zh : J → ℝ) (f : StateFlows I J) : Prop :=
  (∀ i j, 0 ≤ f.a i j ∧ f.a i j ≤ weights j) ∧
  (∀ i j, 0 ≤ f.b i j ∧ f.b i j ≤ weights j) ∧
  (∀ j, 0 ≤ f.h j ∧ f.h j ≤ weights j) ∧
  (∀ i j, f.a i j + f.b i j + f.h j = weights j) ∧
  (∀ i, ∑ j, f.a i j = xa i) ∧
  (∀ i, ∑ j, f.b i j = xb i) ∧
  (∑ j, f.h j) = xh ∧
  (∀ i j, observesA (c i j) → f.a i j = u i j) ∧
  (∀ i j, observesB (c i j) → f.b i j = v i j) ∧
  (∀ j, observedH j → f.h j = zh j)

/-- Exact reconstruction for every number of gadgets and states, including zero weights. -/
theorem profile_iff_stateFlows (c : I → J → StateClass) (u v : I → J → ℝ)
    (weights : J → ℝ) (xa xb : I → ℝ) (xh : ℝ)
    (observedH : J → Prop) (zh : J → ℝ)
    (hweights : (∑ j, weights j) = 1) (haggregate : ∀ i, xa i + xb i = 1 - xh)
    (hn : ∀ i, ObservedNonnegative (c i) (u i) (v i)) :
    (∃ w, Profile c u v weights xa xh observedH zh w) ↔
      ∃ f, ValidStateFlows c u v weights xa xb xh observedH zh f := by
  classical
  constructor
  · rintro ⟨w, hw, hsumw, hH, hg⟩
    have hag : ∀ i, GadgetDisaggregation (c i) (u i) (v i) w (xa i) :=
      fun i => (gadget_profile_iff (c i) (u i) (v i) w (xa i)
        (fun j => (hw j).1) (hn i)).mp (hg i)
    choose a ha hobsA hobsB hsuma using hag
    let f : StateFlows I J := ⟨a, fun i j => w j - a i j, fun j => weights j - w j⟩
    refine ⟨f, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · intro i j
      exact ⟨(ha i j).1, le_trans (ha i j).2 (hw j).2⟩
    · intro i j
      change 0 ≤ w j - a i j ∧ w j - a i j ≤ weights j
      constructor <;> linarith [(ha i j).1, (ha i j).2, (hw j).2]
    · intro j
      change 0 ≤ weights j - w j ∧ weights j - w j ≤ weights j
      constructor <;> linarith [(hw j).1, (hw j).2]
    · intro i j
      change a i j + (w j - a i j) + (weights j - w j) = weights j
      ring
    · exact hsuma
    · intro i
      change (∑ j, (w j - a i j)) = xb i
      rw [Finset.sum_sub_distrib, hsumw, hsuma i]
      linarith [haggregate i]
    · change (∑ j, (weights j - w j)) = xh
      rw [Finset.sum_sub_distrib, hweights, hsumw]
      ring
    · exact hobsA
    · exact hobsB
    · intro j hj
      change weights j - w j = zh j
      linarith [hH j hj]
  · rintro ⟨f, ha, hb, hh, hbalance, hsuma, _hsumb, hsumh, hobsA, hobsB, hobsH⟩
    let w : J → ℝ := fun j => weights j - f.h j
    have hw : ∀ j, 0 ≤ w j ∧ w j ≤ weights j := by
      intro j
      dsimp [w]
      constructor <;> linarith [(hh j).1, (hh j).2]
    refine ⟨w, hw, ?_, ?_, ?_⟩
    · change (∑ j, (weights j - f.h j)) = 1 - xh
      rw [Finset.sum_sub_distrib, hweights, hsumh]
    · intro j hj
      change weights j - f.h j = weights j - zh j
      rw [hobsH j hj]
    · intro i
      apply (gadget_profile_iff (c i) (u i) (v i) w (xa i)
        (fun j => (hw j).1) (hn i)).mpr
      refine ⟨f.a i, ?_, hobsA i, ?_, hsuma i⟩
      · intro j
        refine ⟨(ha i j).1, ?_⟩
        dsimp [w]
        linarith [hbalance i j, (hb i j).1]
      · intro j hj
        dsimp [w]
        linarith [hbalance i j, hobsB i j hj]

/-- No hidden division by a state weight is needed: zero weights force all entries to zero. -/
theorem zero_weight_entries (c : I → J → StateClass) (u v : I → J → ℝ)
    (weights : J → ℝ) (xa xb : I → ℝ) (xh : ℝ)
    (observedH : J → Prop) (zh : J → ℝ) (f : StateFlows I J)
    (hf : ValidStateFlows c u v weights xa xb xh observedH zh f)
    (j : J) (hj : weights j = 0) :
    f.h j = 0 ∧ ∀ i, f.a i j = 0 ∧ f.b i j = 0 := by
  obtain ⟨ha, hb, hh, _⟩ := hf
  refine ⟨le_antisymm (by simpa [hj] using (hh j).2) (hh j).1, ?_⟩
  intro i
  exact ⟨le_antisymm (by simpa [hj] using (ha i j).2) (ha i j).1,
    le_antisymm (by simpa [hj] using (hb i j).2) (hb i j).1⟩

end Chain
end NetworkSimplex
