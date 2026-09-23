import Mathlib.Data.Real.Basic
import Mathlib.Data.Rat.Floor
import Mathlib.Tactic

/-! Exact rational row arithmetic used by the discrete certificate checker. -/
namespace CertifiedMinlp.Discrete
open scoped BigOperators

inductive Kind where
  | le | ge | eq
  deriving DecidableEq, Repr

structure Row (n : ℕ) where
  coeff : Fin n → ℚ
  rhs : ℚ
  kind : Kind
  deriving DecidableEq

variable {n : ℕ}

def value (r : Row n) (x : Fin n → ℝ) : ℝ := ∑ i, (r.coeff i : ℝ) * x i

def Rel (kind : Kind) (lhs rhs : ℝ) : Prop :=
  match kind with
  | .le => lhs ≤ rhs
  | .ge => rhs ≤ lhs
  | .eq => lhs = rhs

def Holds (r : Row n) (x : Fin n → ℝ) : Prop := Rel r.kind (value r x) r.rhs

def Integral (ints : Fin n → Bool) (x : Fin n → ℝ) : Prop :=
  ∀ i, ints i = true → ∃ z : ℤ, x i = z

def contradictory (r : Row n) : Bool := (decide (∀ i, r.coeff i = 0)) &&
  match r.kind with
  | .le => decide (r.rhs < 0)
  | .ge => decide (0 < r.rhs)
  | .eq => decide (r.rhs ≠ 0)

def rhsDominates (s t : Row n) : Prop :=
  match s.kind, t.kind with
  | .le, .le => s.rhs ≤ t.rhs
  | .ge, .ge => t.rhs ≤ s.rhs
  | .eq, .le => s.rhs ≤ t.rhs
  | .eq, .ge => t.rhs ≤ s.rhs
  | .eq, .eq => s.rhs = t.rhs
  | _, _ => False

instance (s t : Row n) : Decidable (rhsDominates s t) := by
  unfold rhsDominates
  split <;> infer_instance

def dominates (s t : Row n) : Bool :=
  contradictory s || decide ((∀ i, s.coeff i = t.coeff i) ∧ rhsDominates s t)

theorem contradictory_sound {r : Row n} {x : Fin n → ℝ}
    (h : contradictory r = true) : ¬ Holds r x := by
  obtain ⟨hc, hb⟩ := Bool.and_eq_true_iff.mp h
  have hc := of_decide_eq_true hc
  have hv : value r x = 0 := by simp [value, hc]
  cases hk : r.kind <;> simp only [Holds, hk, Rel, hv] <;>
    simp only [hk, decide_eq_true_eq] at hb
  · have : (r.rhs : ℝ) < 0 := by exact_mod_cast hb
    linarith
  · have : (0 : ℝ) < r.rhs := by exact_mod_cast hb
    linarith
  · intro he
    apply hb
    exact_mod_cast he.symm

theorem dominates_sound {s t : Row n} {x : Fin n → ℝ}
    (h : dominates s t = true) (hs : Holds s x) : Holds t x := by
  rcases Bool.or_eq_true_iff.mp h with hc | hr
  · exact False.elim (contradictory_sound hc hs)
  obtain ⟨hc, hr⟩ := of_decide_eq_true hr
  have hv : value s x = value t x := by simp [value, hc]
  cases hk : s.kind <;> cases ht : t.kind <;>
    simp only [rhsDominates, hk, ht] at hr <;>
    simp only [Holds, hk, ht, Rel] at hs ⊢
  all_goals try
    have hcast : (s.rhs : ℝ) ≤ t.rhs := by exact_mod_cast hr
    linarith
  all_goals try
    have hcast : (t.rhs : ℝ) ≤ s.rhs := by exact_mod_cast hr
    linarith
  have hcast : (s.rhs : ℝ) = t.rhs := by exact_mod_cast hr
  linarith

def allowed (kind : Kind) (term : ℚ × Row n) : Prop :=
  match kind, term.2.kind with
  | .le, .le | .ge, .ge => 0 ≤ term.1
  | .le, .ge | .ge, .le => term.1 ≤ 0
  | _, .eq => True
  | .eq, _ => term.1 = 0

instance (kind : Kind) (term : ℚ × Row n) : Decidable (allowed kind term) := by
  unfold allowed
  split <;> infer_instance

def combinedRow (kind : Kind) (terms : List (ℚ × Row n)) : Row n where
  coeff i := (terms.map (fun t => t.1 * t.2.coeff i)).sum
  rhs := (terms.map (fun t => t.1 * t.2.rhs)).sum
  kind := kind

def combination (kind : Kind) (terms : List (ℚ × Row n)) : Option (Row n) :=
  if terms.all (fun t => decide (allowed kind t)) then some (combinedRow kind terms) else none

theorem combined_value (kind : Kind) (terms : List (ℚ × Row n)) (x : Fin n → ℝ) :
    value (combinedRow kind terms) x =
      (terms.map (fun t => (t.1 : ℝ) * value t.2 x)).sum := by
  induction terms with
  | nil => simp [combinedRow, value]
  | cons t ts ih =>
    simp only [combinedRow, List.map_cons, List.sum_cons, Rat.cast_add, Rat.cast_mul,
      value, add_mul, Finset.sum_add_distrib] at *
    rw [ih]
    congr 1
    simp only [← Finset.mul_sum, mul_assoc]

theorem allowed_sound {kind : Kind} {t : ℚ × Row n} {x : Fin n → ℝ}
    (ha : allowed kind t) (hs : t.1 ≠ 0 → Holds t.2 x) :
    Rel kind ((t.1 : ℝ) * value t.2 x) ((t.1 : ℝ) * t.2.rhs) := by
  by_cases hz : t.1 = 0
  · cases kind <;> simp [Rel, hz]
  have htS := hs hz
  cases hk : kind <;> cases hr : t.2.kind <;>
    simp only [allowed, hk, hr] at ha <;> simp only [Holds, hr, Rel] at htS <;>
    simp only [Rel]
  all_goals try
    have hh : (0 : ℝ) ≤ t.1 := by exact_mod_cast ha
    nlinarith
  all_goals try
    have hh : (t.1 : ℝ) ≤ 0 := by exact_mod_cast ha
    nlinarith
  all_goals try contradiction
  all_goals simp [htS]

theorem combination_sound {kind : Kind} {terms : List (ℚ × Row n)} {r : Row n}
    {x : Fin n → ℝ} (h : combination kind terms = some r)
    (hs : ∀ t ∈ terms, t.1 ≠ 0 → Holds t.2 x) : Holds r x := by
  unfold combination at h
  split at h
  next ha =>
    have hr : r = combinedRow kind terms := (Option.some.inj h).symm
    subst r
    have hterm : ∀ t ∈ terms,
        Rel kind ((t.1 : ℝ) * value t.2 x) ((t.1 : ℝ) * t.2.rhs) := by
      intro t ht
      exact allowed_sound (of_decide_eq_true ((List.all_eq_true.mp ha) t ht)) (hs t ht)
    have rhs_cast : ((combinedRow kind terms).rhs : ℝ) =
        (terms.map (fun t => (t.1 : ℝ) * (t.2.rhs : ℝ))).sum := by
      simp [combinedRow, List.map_map, Function.comp_def]
    unfold Holds
    rw [combined_value, rhs_cast]
    change Rel kind _ _
    clear ha h
    cases kind <;> simp only [Rel] at hterm ⊢
    · exact List.sum_le_sum hterm
    · exact List.sum_le_sum hterm
    · apply congrArg List.sum
      apply List.map_congr_left
      exact hterm
  next => simp at h



/-- Every nonzero coefficient is integral and refers to an integer variable. -/
def integralCoefficients (ints : Fin n → Bool) (r : Row n) : Bool :=
  decide (∀ i, r.coeff i = 0 ∨ (ints i = true ∧ r.coeff i = (⌊r.coeff i⌋ : ℚ)))

theorem value_integral {ints : Fin n → Bool} {r : Row n} {x : Fin n → ℝ}
    (hc : integralCoefficients ints r = true) (hx : Integral ints x) :
    ∃ z : ℤ, value r x = z := by
  classical
  have hc' := of_decide_eq_true hc
  have hi : ∀ i, ∃ z : ℤ, (r.coeff i : ℝ) * x i = z := by
    intro i
    rcases hc' i with hz | ⟨hm, ha⟩
    · exact ⟨0, by simp [hz]⟩
    · obtain ⟨z, hz⟩ := hx i hm
      refine ⟨⌊r.coeff i⌋ * z, ?_⟩
      have ha' : (r.coeff i : ℝ) = (⌊r.coeff i⌋ : ℝ) := by exact_mod_cast ha
      simp [ha', hz]
  choose z hz using hi
  refine ⟨∑ i, z i, ?_⟩
  simp [value, hz]

def rounded (ints : Fin n → Bool) (r : Row n) : Option (Row n) :=
  if integralCoefficients ints r then
    match r.kind with
    | .le => some {r with rhs := (⌊r.rhs⌋ : ℚ)}
    | .ge => some {r with rhs := (⌈r.rhs⌉ : ℚ)}
    | .eq => none
  else none

theorem rounded_sound {ints : Fin n → Bool} {r out : Row n} {x : Fin n → ℝ}
    (h : rounded ints r = some out) (hx : Integral ints x) (hr : Holds r x) :
    Holds out x := by
  unfold rounded at h
  split at h
  next hc =>
    obtain ⟨z, hz⟩ := value_integral hc hx
    cases hk : r.kind <;> simp only [hk] at h
    · have ho := Option.some.inj h
      subst out
      have hr' : (z : ℝ) ≤ (r.rhs : ℝ) := by simpa [Holds, hk, Rel, hz] using hr
      have hq : (z : ℚ) ≤ r.rhs := by exact_mod_cast hr'
      have hi := Int.le_floor.mpr hq
      have hi' : (z : ℝ) ≤ (⌊r.rhs⌋ : ℝ) := by exact_mod_cast hi
      simpa [Holds, hk, Rel, value, ← hz] using hi'
    · have ho := Option.some.inj h
      subst out
      have hr' : (r.rhs : ℝ) ≤ (z : ℝ) := by simpa [Holds, hk, Rel, hz] using hr
      have hq : r.rhs ≤ (z : ℚ) := by exact_mod_cast hr'
      have hi := Int.ceil_le.mpr hq
      have hi' : (⌈r.rhs⌉ : ℝ) ≤ (z : ℝ) := by exact_mod_cast hi
      simpa [Holds, hk, Rel, value, ← hz] using hi'
    · contradiction
  next => simp at h

/-- The two branches partition integer values at consecutive integer thresholds. -/
def splitRows (ints : Fin n → Bool) (left right : Row n) : Bool :=
  integralCoefficients ints left && decide
    (left.kind = .le ∧ right.kind = .ge ∧
      (∀ i, left.coeff i = right.coeff i) ∧
      left.rhs = (⌊left.rhs⌋ : ℚ) ∧ right.rhs = left.rhs + 1)

theorem splitRows_sound {ints : Fin n → Bool} {left right : Row n} {x : Fin n → ℝ}
    (h : splitRows ints left right = true) (hx : Integral ints x) :
    Holds left x ∨ Holds right x := by
  obtain ⟨hc, hs⟩ := Bool.and_eq_true_iff.mp h
  obtain ⟨hl, hr, he, hb, hd⟩ := of_decide_eq_true hs
  obtain ⟨z, hz⟩ := value_integral hc hx
  have hv : value right x = (z : ℝ) := by
    rw [← hz]
    simp [value, he]
  have hb' : (left.rhs : ℝ) = (⌊left.rhs⌋ : ℝ) := by exact_mod_cast hb
  have hd' : (right.rhs : ℝ) = (⌊left.rhs⌋ : ℝ) + 1 := by
    have hdc : (right.rhs : ℝ) = (left.rhs : ℝ) + 1 := by exact_mod_cast hd
    rw [hdc, hb']
  by_cases hi : z ≤ ⌊left.rhs⌋
  · left
    have hi' : (z : ℝ) ≤ (⌊left.rhs⌋ : ℝ) := by exact_mod_cast hi
    simpa [Holds, hl, Rel, hz, hb'] using hi'
  · right
    have hi' : ⌊left.rhs⌋ + 1 ≤ z := by omega
    have hi'' : (⌊left.rhs⌋ : ℝ) + 1 ≤ (z : ℝ) := by exact_mod_cast hi'
    simpa [Holds, hr, Rel, hv, hd'] using hi''

end CertifiedMinlp.Discrete
