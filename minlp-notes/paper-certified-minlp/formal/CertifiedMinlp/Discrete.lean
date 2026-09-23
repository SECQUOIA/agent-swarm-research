import CertifiedMinlp.DiscreteRows
import CertifiedMinlp.Transfer

/-! A finite, sequential checker for discrete derivations. The complete list of
steps is checked, and references can only address the already checked prefix.
This is a structured checker; it does not claim to verify a text parser. -/
namespace CertifiedMinlp.Discrete

def masterFeasible {n : ℕ} (master : List (Row n)) (ints : Fin n → Bool) :
    Set (Fin n → ℝ) := {x | Integral ints x ∧ ∀ r ∈ master, Holds r x}

structure Entry (n : ℕ) where
  row : Row n
  deps : Finset ℕ
  assumption : Bool

inductive Reason where
  | original (index : ℕ)
  | assume
  | solution
  | combine (kind : Kind) (terms : List (ℚ × ℕ))
  | round (kind : Kind) (terms : List (ℚ × ℕ))
  | unsplit (left right leftBranch rightBranch : ℕ)

structure Step (n : ℕ) where
  entry : Entry n
  reason : Reason

def dependencies {n : ℕ} : List (ℚ × Entry n) → Finset ℕ
  | [] => ∅
  | (q, e) :: es => (if q = 0 then ∅ else e.deps) ∪ dependencies es

def fetch {n : ℕ} (env : List (Entry n)) : List (ℚ × ℕ) → Option (List (ℚ × Entry n))
  | [] => some []
  | (q, i) :: rest => do
    let e ← env[i]?
    let es ← fetch env rest
    pure ((q, e) :: es)

def Assumptions {n : ℕ} (claims : ℕ → Row n) (deps : Finset ℕ)
    (x : Fin n → ℝ) : Prop := ∀ i ∈ deps, Holds (claims i) x

def ValidEntry {n : ℕ} (claims : ℕ → Row n) (S : Set (Fin n → ℝ))
    (e : Entry n) : Prop := ∀ x ∈ S, Assumptions claims e.deps x → Holds e.row x

def ValidEnv {n : ℕ} (claims : ℕ → Row n) (S : Set (Fin n → ℝ))
    (env : List (Entry n)) : Prop := ∀ e ∈ env, ValidEntry claims S e

/-- All tests here are finite comparisons of rational data and natural indices. -/
def StepCheck {n : ℕ} (master : List (Row n)) (ints : Fin n → Bool)
    (cutoff : Option (Row n)) (claims : ℕ → Row n) (env : List (Entry n))
    (step : Step n) : Prop :=
  step.entry.row = claims env.length ∧
  match step.reason with
  | .original i => step.entry.assumption = false ∧ step.entry.deps = ∅ ∧
      match master[i]? with
      | none => False
      | some r => dominates r step.entry.row = true
  | .assume => step.entry.assumption = true ∧ step.entry.deps = {env.length}
  | .solution => step.entry.assumption = false ∧ step.entry.deps = ∅ ∧
      match cutoff with
      | none => False
      | some r => dominates r step.entry.row = true
  | .combine kind refs => step.entry.assumption = false ∧
      match fetch env refs with
      | none => False
      | some terms => step.entry.deps = dependencies terms ∧
          match combination kind (terms.map fun t => (t.1, t.2.row)) with
          | none => False
          | some r => dominates r step.entry.row = true
  | .round kind refs => step.entry.assumption = false ∧
      match fetch env refs with
      | none => False
      | some terms => step.entry.deps = dependencies terms ∧
          match combination kind (terms.map fun t => (t.1, t.2.row)) with
          | none => False
          | some r => match rounded ints r with
              | none => False
              | some rr => dominates rr step.entry.row = true
  | .unsplit i j k l => step.entry.assumption = false ∧
      match env[i]?, env[j]?, env[k]?, env[l]? with
      | some a, some b, some c, some d =>
          a.assumption = true ∧ b.assumption = true ∧
          a.row = claims i ∧ b.row = claims j ∧
          (splitRows ints a.row b.row || splitRows ints b.row a.row) = true ∧
          dominates c.row step.entry.row = true ∧
          dominates d.row step.entry.row = true ∧
          step.entry.deps = (c.deps.erase i) ∪ (d.deps.erase j)
      | _, _, _, _ => False

instance {n : ℕ} (master : List (Row n)) (ints : Fin n → Bool)
    (cutoff : Option (Row n)) (claims : ℕ → Row n) (env : List (Entry n))
    (step : Step n) : Decidable (StepCheck master ints cutoff claims env step) := by
  unfold StepCheck
  repeat' first | split | infer_instance

def checkStep {n : ℕ} (master : List (Row n)) (ints : Fin n → Bool)
    (cutoff : Option (Row n)) (claims : ℕ → Row n) (env : List (Entry n))
    (step : Step n) : Bool := decide (StepCheck master ints cutoff claims env step)

lemma fetch_mem {n : ℕ} {env : List (Entry n)} {refs : List (ℚ × ℕ)}
    {terms : List (ℚ × Entry n)} (h : fetch env refs = some terms)
    {q : ℚ} {e : Entry n} (he : (q, e) ∈ terms) : e ∈ env := by
  induction refs generalizing terms with
  | nil => simp [fetch] at h; subst terms; simp at he
  | cons r rs ih =>
    obtain ⟨q', i⟩ := r
    cases hi : env[i]? with
    | none => simp [fetch, hi] at h
    | some e' =>
      cases hr : fetch env rs with
      | none => simp [fetch, hi, hr] at h
      | some es =>
        have hh : terms = (q', e') :: es := by simpa [fetch, hi, hr] using h.symm
        subst terms
        simp only [List.mem_cons] at he
        rcases he with he | he
        · cases he
          exact List.mem_of_getElem? hi
        · exact ih hr he

lemma dependencies_contains {n : ℕ} {terms : List (ℚ × Entry n)}
    {q : ℚ} {e : Entry n} (he : (q, e) ∈ terms) (hq : q ≠ 0) :
    e.deps ⊆ dependencies terms := by
  induction terms with
  | nil => simp at he
  | cons t ts ih =>
    rcases List.mem_cons.mp he with ht | ht
    · cases ht
      simp [dependencies, hq]
    · exact fun i hi => Finset.mem_union_right _ (ih ht hi)

lemma fetched_sound {n : ℕ} {claims : ℕ → Row n} {S : Set (Fin n → ℝ)}
    {env : List (Entry n)} (hv : ValidEnv claims S env)
    {refs : List (ℚ × ℕ)} {terms : List (ℚ × Entry n)}
    (hf : fetch env refs = some terms) {x : Fin n → ℝ} (hx : x ∈ S)
    (ha : Assumptions claims (dependencies terms) x) :
    ∀ t ∈ terms.map (fun t => (t.1, t.2.row)), t.1 ≠ 0 → Holds t.2 x := by
  intro t ht hq
  obtain ⟨⟨q, e⟩, he, rfl⟩ := List.mem_map.mp ht
  exact hv e (fetch_mem hf he) x hx (fun i hi => ha i (dependencies_contains he hq hi))

/-- Every checked rule preserves the dependency invariant. Arithmetic rules are
proved from their rational tests in `DiscreteRows`; no rule-soundness oracle is used. -/
theorem step_sound {n : ℕ} {master : List (Row n)} {ints : Fin n → Bool}
    {cutoff : Option (Row n)} {claims : ℕ → Row n} {env : List (Entry n)}
    {step : Step n} {S : Set (Fin n → ℝ)}
    (hmaster : ∀ x ∈ S, ∀ r ∈ master, Holds r x)
    (hints : ∀ x ∈ S, Integral ints x)
    (hcutoff : ∀ r, cutoff = some r → ∀ x ∈ S, Holds r x)
    (hv : ValidEnv claims S env)
    (hc : checkStep master ints cutoff claims env step = true) :
    ValidEntry claims S step.entry := by
  have h := of_decide_eq_true hc
  rcases h with ⟨hclaim, h⟩
  intro x hx ha
  cases hr : step.reason with
  | original i =>
    simp only [hr] at h
    rcases h with ⟨_, _, h⟩
    cases hi : master[i]? with
    | none => simp [hi] at h
    | some r =>
      exact dominates_sound (by simpa [hi] using h)
        (hmaster x hx r (List.mem_of_getElem? hi))
  | assume =>
    simp only [hr] at h
    rw [hclaim]
    exact ha env.length (by simp [h.2])
  | solution =>
    simp only [hr] at h
    cases hi : cutoff with
    | none => simp [hi] at h
    | some r => exact dominates_sound (by simpa [hi] using h.2.2) (hcutoff r hi x hx)
  | combine kind refs =>
    simp only [hr] at h
    cases hf : fetch env refs with
    | none => simp [hf] at h
    | some terms =>
      simp only [hf] at h
      have ht := fetched_sound hv hf hx (h.2.1 ▸ ha)
      cases hs : combination kind (terms.map fun t => (t.1, t.2.row)) with
      | none => simp [hs] at h
      | some r =>
        exact dominates_sound (by simpa [hs] using h.2.2)
          (combination_sound hs ht)
  | round kind refs =>
    simp only [hr] at h
    cases hf : fetch env refs with
    | none => simp [hf] at h
    | some terms =>
      simp only [hf] at h
      have ht := fetched_sound hv hf hx (h.2.1 ▸ ha)
      cases hs : combination kind (terms.map fun t => (t.1, t.2.row)) with
      | none => simp [hs] at h
      | some r =>
        simp only [hs] at h
        cases hr : rounded ints r with
        | none => simp [hr] at h
        | some rr =>
          exact dominates_sound (by simpa [hr] using h.2.2)
            (rounded_sound hr (hints x hx) (combination_sound hs ht))
  | unsplit i j k l =>
    simp only [hr] at h
    cases hi : env[i]? with
    | none => simp [hi] at h
    | some a =>
      cases hj : env[j]? with
      | none => simp [hi, hj] at h
      | some b =>
        cases hk : env[k]? with
        | none => simp [hi, hj, hk] at h
        | some c =>
          cases hl : env[l]? with
          | none => simp [hi, hj, hk, hl] at h
          | some d =>
            simp only [hi, hj, hk, hl] at h
            obtain ⟨_, _, _, hai, hbj, hs, hc, hd, hdeps⟩ := h
            rw [hdeps] at ha
            have hex : Holds a.row x ∨ Holds b.row x := by
              rcases Bool.or_eq_true_iff.mp hs with hab | hba
              · exact splitRows_sound hab (hints x hx)
              · exact (splitRows_sound hba (hints x hx)).symm
            rcases hex with hleft | hright
            · apply dominates_sound hc
              apply hv c (List.mem_of_getElem? hk) x hx
              intro t ht
              by_cases hti : t = i
              · simpa [hti, ← hai] using hleft
              · exact ha t (Finset.mem_union_left _ (Finset.mem_erase.mpr ⟨hti, ht⟩))
            · apply dominates_sound hd
              apply hv d (List.mem_of_getElem? hl) x hx
              intro t ht
              by_cases htj : t = j
              · simpa [htj, ← hbj] using hright
              · exact ha t (Finset.mem_union_right _ (Finset.mem_erase.mpr ⟨htj, ht⟩))

/-- A Boolean pass consumes every supplied row, including rows after the bound. -/
def checkFrom {n : ℕ} (master : List (Row n)) (ints : Fin n → Bool)
    (cutoff : Option (Row n)) (claims : ℕ → Row n) :
    List (Entry n) → List (Step n) → Bool
  | _, [] => true
  | env, step :: rest => checkStep master ints cutoff claims env step &&
      checkFrom master ints cutoff claims (env ++ [step.entry]) rest

theorem checkFrom_sound {n : ℕ} {master : List (Row n)} {ints : Fin n → Bool}
    {cutoff : Option (Row n)} {claims : ℕ → Row n} {S : Set (Fin n → ℝ)}
    (hmaster : ∀ x ∈ S, ∀ r ∈ master, Holds r x)
    (hints : ∀ x ∈ S, Integral ints x)
    (hcutoff : ∀ r, cutoff = some r → ∀ x ∈ S, Holds r x)
    (steps : List (Step n)) (env : List (Entry n)) (hv : ValidEnv claims S env)
    (hc : checkFrom master ints cutoff claims env steps = true) :
    ValidEnv claims S (env ++ steps.map Step.entry) := by
  induction steps generalizing env with
  | nil => simpa using hv
  | cons step rest ih =>
    obtain ⟨hstep, hrest⟩ := Bool.and_eq_true_iff.mp hc
    have he := step_sound hmaster hints hcutoff hv hstep
    have hv' : ValidEnv claims S (env ++ [step.entry]) := by
      intro e h
      rcases List.mem_append.mp h with h | h
      · exact hv e h
      · simpa using (List.mem_singleton.mp h ▸ he)
    simpa [List.map_cons, List.append_assoc] using ih _ hv' hrest

/-- Claim lookup is determined by the certificate, not by an external oracle. -/
def certificateClaims {n : ℕ} (steps : List (Step n)) (i : ℕ) : Row n :=
  ((steps.map Step.entry)[i]?).map Entry.row |>.getD ⟨fun _ => 0, 0, .le⟩

def check {n : ℕ} (master : List (Row n)) (ints : Fin n → Bool)
    (cutoff : Option (Row n)) (steps : List (Step n)) : Bool :=
  checkFrom master ints cutoff (certificateClaims steps) [] steps

theorem check_sound {n : ℕ} {master : List (Row n)} {ints : Fin n → Bool}
    {cutoff : Option (Row n)} {S : Set (Fin n → ℝ)}
    (hmaster : ∀ x ∈ S, ∀ r ∈ master, Holds r x)
    (hints : ∀ x ∈ S, Integral ints x)
    (hcutoff : ∀ r, cutoff = some r → ∀ x ∈ S, Holds r x)
    {steps : List (Step n)} (hc : check master ints cutoff steps = true) :
    ValidEnv (certificateClaims steps) S (steps.map Step.entry) := by
  simpa using checkFrom_sound hmaster hints hcutoff steps [] (by simp [ValidEnv]) hc

theorem checked_assumption_free {n : ℕ} {master : List (Row n)} {ints : Fin n → Bool}
    {cutoff : Option (Row n)} {S : Set (Fin n → ℝ)}
    (hmaster : ∀ x ∈ S, ∀ r ∈ master, Holds r x)
    (hints : ∀ x ∈ S, Integral ints x)
    (hcutoff : ∀ r, cutoff = some r → ∀ x ∈ S, Holds r x)
    {steps : List (Step n)} (hc : check master ints cutoff steps = true)
    {e : Entry n} (he : e ∈ steps.map Step.entry) (hdeps : e.deps = ∅)
    {target : Row n} (hdom : dominates e.row target = true) :
    ∀ x ∈ S, Holds target x := by
  intro x hx
  exact dominates_sound hdom (check_sound hmaster hints hcutoff hc e he x hx
    (by simp [Assumptions, hdeps]))

end CertifiedMinlp.Discrete
