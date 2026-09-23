import Formal.FBBT.Circuit

/-!
# Fair propagation and limits

An arbitrary fair schedule visits each defining equation infinitely often, with
no bound on the delay between visits. Contracting, sound boxes give monotone
bounded lower endpoints. If an update enforces the forward lower evaluation of a
continuous right-hand side, the limit is a prefixed point of every equation.
This lemma does not assume that upstream circuit variables start at exact values.
-/

open Filter Set Topology

namespace FBBT

/-- Every coordinate is selected again after any finite time. -/
def FairSchedule {ι : Type*} (schedule : ℕ → ι) : Prop :=
  ∀ i t, ∃ k, t ≤ k ∧ schedule k = i

/-- The coordinatewise supremum of a bounded monotone endpoint sequence. -/
noncomputable def lowerLimit {ι : Type*} (lower : ℕ → ι → ℝ) (i : ι) : ℝ :=
  ⨆ t, lower t i

lemma lower_le_limit {ι : Type*} {lower : ℕ → ι → ℝ} {upper : ι → ℝ}
    (hbound : ∀ t i, lower t i ≤ upper i) (t : ℕ) (i : ι) :
    lower t i ≤ lowerLimit lower i :=
  le_ciSup ⟨upper i, by rintro _ ⟨s, rfl⟩; exact hbound s i⟩ t

lemma lowerLimit_le {ι : Type*} {lower : ℕ → ι → ℝ} {upper : ι → ℝ}
    (hbound : ∀ t i, lower t i ≤ upper i) (i : ι) :
    lowerLimit lower i ≤ upper i :=
  ciSup_le fun t => hbound t i

/-- Monotone bounded lower endpoints converge jointly in the product topology. -/
theorem lower_tendsto_limit {ι : Type*} {lower : ℕ → ι → ℝ} {upper : ι → ℝ}
    (hmono : ∀ i, Monotone fun t => lower t i)
    (hbound : ∀ t i, lower t i ≤ upper i) :
    Tendsto lower atTop (𝓝 (lowerLimit lower)) := by
  apply tendsto_pi_nhds.mpr
  intro i
  exact tendsto_atTop_ciSup (hmono i)
    ⟨upper i, by rintro _ ⟨s, rfl⟩; exact hbound s i⟩

/-- Fairness alone suffices to enforce every continuous forward inequality at
    the limit; visits need not have uniformly bounded delays. -/
theorem fair_limit_prefixed {ι : Type*} {lower : ℕ → ι → ℝ} {upper : ι → ℝ}
    {schedule : ℕ → ι} {rhs : ι → (ι → ℝ) → ℝ}
    (hmono : ∀ i, Monotone fun t => lower t i)
    (hbound : ∀ t i, lower t i ≤ upper i)
    (hfair : FairSchedule schedule)
    (hcontinuous : ∀ i, Continuous (rhs i))
    (hforward : ∀ t, rhs (schedule t) (lower t) ≤ lower (t + 1) (schedule t)) :
    ∀ i, rhs i (lowerLimit lower) ≤ lowerLimit lower i := by
  intro i
  have hconv := (hcontinuous i).tendsto (lowerLimit lower) |>.comp
    (lower_tendsto_limit hmono hbound)
  apply le_of_tendsto_of_frequently hconv
  apply frequently_atTop.mpr
  intro t
  obtain ⟨k, htk, hki⟩ := hfair i t
  refine ⟨k, htk, ?_⟩
  have hf : rhs i (lower k) ≤ lower (k + 1) i := by simpa only [hki] using hforward k
  exact hf.trans (lower_le_limit hbound (k + 1) i)

/-- If the feasible point is the only nonnegative bounded prefixed point,
    every fair run converges to it, even from inexact upstream endpoints. -/
theorem fair_lower_tendsto_exact {ι : Type*} {lower : ℕ → ι → ℝ} {exact : ι → ℝ}
    {schedule : ℕ → ι} {rhs : ι → (ι → ℝ) → ℝ}
    (hmono : ∀ i, Monotone fun t => lower t i)
    (hnonneg : ∀ t i, 0 ≤ lower t i)
    (hbound : ∀ t i, lower t i ≤ exact i)
    (hfair : FairSchedule schedule)
    (hcontinuous : ∀ i, Continuous (rhs i))
    (hforward : ∀ t, rhs (schedule t) (lower t) ≤ lower (t + 1) (schedule t))
    (hprefixed : ∀ x : ι → ℝ, (∀ i, 0 ≤ x i) → (∀ i, x i ≤ exact i) →
      (∀ i, rhs i x ≤ x i) → x = exact) :
    Tendsto lower atTop (𝓝 exact) := by
  have heq : lowerLimit lower = exact := hprefixed (lowerLimit lower)
    (fun i => (hnonneg 0 i).trans (lower_le_limit hbound 0 i))
    (lowerLimit_le hbound)
    (fair_limit_prefixed hmono hbound hfair hcontinuous hforward)
  simpa only [heq] using lower_tendsto_limit hmono hbound


/-- The acyclic variables of a prefixed point below the feasible point are exact. -/
theorem circuitPrefixed_upstream {n : ℕ} {x : CircuitVar n → ℝ}
    (hbound : ∀ a, x a ≤ circuitPoint n a)
    (hpre : ∀ a, (circuitRhs n a).eval x ≤ x a) (i : Fin (n + 1)) :
    x (.b i) = bValue i ∧ x (.c i) = cValue i := by
  obtain ⟨i, hi⟩ := i
  induction i with
  | zero =>
    constructor
    · exact le_antisymm (hbound (.b ⟨0, hi⟩))
        (by simpa [circuitRhs, PrimitiveRhs.eval] using hpre (.b ⟨0, hi⟩))
    · exact le_antisymm (hbound (.c ⟨0, hi⟩))
        (by simpa [circuitRhs, PrimitiveRhs.eval] using hpre (.c ⟨0, hi⟩))
  | succ i ih =>
    obtain ⟨hb, hc⟩ := ih (by omega)
    have hh : x (.h ⟨i, by omega⟩) = bValue i :=
      le_antisymm (hbound (.h ⟨i, by omega⟩))
        (by simpa [circuitRhs, PrimitiveRhs.eval, Fin.castSucc, Fin.castAdd, Fin.castLE, hb] using
          hpre (.h ⟨i, by omega⟩))
    have hv : x (.v ⟨i, by omega⟩) = bValue i * cValue i :=
      le_antisymm (hbound (.v ⟨i, by omega⟩))
        (by simpa [circuitRhs, PrimitiveRhs.eval, Fin.castSucc, Fin.castAdd,
          Fin.castLE, hb, hc] using
          hpre (.v ⟨i, by omega⟩))
    constructor
    · apply le_antisymm (hbound (.b ⟨i + 1, hi⟩))
      simpa [circuitPoint, circuitRhs, PrimitiveRhs.eval, hb, hh, bValue_succ] using
        hpre (.b ⟨i + 1, hi⟩)
    · apply le_antisymm (hbound (.c ⟨i + 1, hi⟩))
      simpa [circuitPoint, circuitRhs, PrimitiveRhs.eval, hc, hv, cValue_succ] using
        hpre (.c ⟨i + 1, hi⟩)

/-- A prefixed point dominated by the feasible point equals that point. -/
theorem circuitPrefixed_unique {n : ℕ} {x : CircuitVar n → ℝ}
    (hbound : ∀ a, x a ≤ circuitPoint n a)
    (hpre : ∀ a, (circuitRhs n a).eval x ≤ x a) :
    x = circuitPoint n := by
  obtain ⟨hb, hc⟩ := circuitPrefixed_upstream hbound hpre (Fin.last n)
  have hz := hpre .z
  have hw := hpre .w
  simp only [circuitRhs, PrimitiveRhs.eval, hb, hc, Fin.val_last] at hz hw
  have hz1 : x .z = 1 := by
    apply le_antisymm (hbound .z)
    change 1 ≤ x .z
    have hp := bValue_pos n
    dsimp [cValue] at hw
    nlinarith
  have hw1 : x .w = cValue n :=
    le_antisymm (hbound .w) (by simpa [hz1] using hw)
  funext a
  cases a with
  | b i => exact (circuitPrefixed_upstream hbound hpre i).1
  | c i => exact (circuitPrefixed_upstream hbound hpre i).2
  | h i =>
    apply le_antisymm (hbound (.h i))
    simpa [circuitRhs, PrimitiveRhs.eval, circuitPoint,
      (circuitPrefixed_upstream hbound hpre i.castSucc).1] using hpre (.h i)
  | v i =>
    apply le_antisymm (hbound (.v i))
    simpa [circuitRhs, PrimitiveRhs.eval, circuitPoint,
      (circuitPrefixed_upstream hbound hpre i.castSucc).1,
      (circuitPrefixed_upstream hbound hpre i.castSucc).2] using hpre (.v i)
  | z => exact hz1
  | w => exact hw1

lemma PrimitiveRhs.continuous_eval {ι : Type*} (rhs : PrimitiveRhs ι) :
    Continuous (fun x : ι → ℝ => rhs.eval x) := by
  cases rhs with
  | half => exact continuous_const
  | copy a => exact continuous_apply a
  | add a b => exact (continuous_apply a).add (continuous_apply b)
  | mul a b => exact (continuous_apply a).mul (continuous_apply b)

/-- Full-circuit lower endpoints converge to the unique feasible point under
    any fair sequence of sound contracting updates that enforce forward bounds. -/
theorem fair_circuit_lower_tendsto {n : ℕ}
    {lower : ℕ → CircuitVar n → ℝ} {schedule : ℕ → CircuitVar n}
    (hmono : ∀ a, Monotone fun t => lower t a)
    (hnonneg : ∀ t a, 0 ≤ lower t a)
    (hbound : ∀ t a, lower t a ≤ circuitPoint n a)
    (hfair : FairSchedule schedule)
    (hforward : ∀ t, (circuitRhs n (schedule t)).eval (lower t) ≤
      lower (t + 1) (schedule t)) :
    Tendsto lower atTop (𝓝 (circuitPoint n)) := by
  apply fair_lower_tendsto_exact hmono hnonneg hbound hfair
    (fun a => (circuitRhs n a).continuous_eval) hforward
  intro x _ hx hp
  exact circuitPrefixed_unique hx hp


/-- The coordinatewise infimum of decreasing upper endpoints. -/
noncomputable def upperLimit {ι : Type*} (upper : ℕ → ι → ℝ) (i : ι) : ℝ :=
  ⨅ t, upper t i

lemma limit_le_upper {ι : Type*} {upper : ℕ → ι → ℝ} {lower : ι → ℝ}
    (hbound : ∀ t i, lower i ≤ upper t i) (t : ℕ) (i : ι) :
    upperLimit upper i ≤ upper t i :=
  ciInf_le ⟨lower i, by rintro _ ⟨s, rfl⟩; exact hbound s i⟩ t

lemma le_upperLimit {ι : Type*} {upper : ℕ → ι → ℝ} {lower : ι → ℝ}
    (hbound : ∀ t i, lower i ≤ upper t i) (i : ι) :
    lower i ≤ upperLimit upper i :=
  le_ciInf fun t => hbound t i

lemma upper_tendsto_limit {ι : Type*} {upper : ℕ → ι → ℝ} {lower : ι → ℝ}
    (hanti : ∀ i, Antitone fun t => upper t i)
    (hbound : ∀ t i, lower i ≤ upper t i) :
    Tendsto upper atTop (𝓝 (upperLimit upper)) := by
  apply tendsto_pi_nhds.mpr
  intro i
  exact tendsto_atTop_ciInf (hanti i)
    ⟨lower i, by rintro _ ⟨s, rfl⟩; exact hbound s i⟩

/-- Fair forward upper propagation enforces every postfixed inequality at the limit. -/
theorem fair_limit_postfixed {ι : Type*} {upper : ℕ → ι → ℝ} {lower : ι → ℝ}
    {schedule : ℕ → ι} {rhs : ι → (ι → ℝ) → ℝ}
    (hanti : ∀ i, Antitone fun t => upper t i)
    (hbound : ∀ t i, lower i ≤ upper t i)
    (hfair : FairSchedule schedule)
    (hcontinuous : ∀ i, Continuous (rhs i))
    (hforward : ∀ t, upper (t + 1) (schedule t) ≤ rhs (schedule t) (upper t)) :
    ∀ i, upperLimit upper i ≤ rhs i (upperLimit upper) := by
  intro i
  have hconv := (hcontinuous i).tendsto (upperLimit upper) |>.comp
    (upper_tendsto_limit hanti hbound)
  apply ge_of_tendsto_of_frequently hconv
  apply frequently_atTop.mpr
  intro t
  obtain ⟨k, htk, hki⟩ := hfair i t
  refine ⟨k, htk, ?_⟩
  have hf : upper (k + 1) i ≤ rhs i (upper k) := by simpa only [hki] using hforward k
  exact (limit_le_upper hbound (k + 1) i).trans hf

/-- The upstream coordinates are also forced by postfixed inequalities. -/
theorem circuitPostfixed_upstream {n : ℕ} {x : CircuitVar n → ℝ}
    (hbound : ∀ a, circuitPoint n a ≤ x a)
    (hpost : ∀ a, x a ≤ (circuitRhs n a).eval x) (i : Fin (n + 1)) :
    x (.b i) = bValue i ∧ x (.c i) = cValue i := by
  obtain ⟨i, hi⟩ := i
  induction i with
  | zero =>
    constructor
    · exact le_antisymm
        (by simpa [circuitRhs, PrimitiveRhs.eval] using hpost (.b ⟨0, hi⟩))
        (hbound (.b ⟨0, hi⟩))
    · exact le_antisymm
        (by simpa [circuitRhs, PrimitiveRhs.eval] using hpost (.c ⟨0, hi⟩))
        (hbound (.c ⟨0, hi⟩))
  | succ i ih =>
    obtain ⟨hb, hc⟩ := ih (by omega)
    have hh : x (.h ⟨i, by omega⟩) = bValue i :=
      le_antisymm
        (by simpa [circuitRhs, PrimitiveRhs.eval, Fin.castSucc, Fin.castAdd, Fin.castLE, hb] using
          hpost (.h ⟨i, by omega⟩))
        (hbound (.h ⟨i, by omega⟩))
    have hv : x (.v ⟨i, by omega⟩) = bValue i * cValue i :=
      le_antisymm
        (by simpa [circuitRhs, PrimitiveRhs.eval, Fin.castSucc, Fin.castAdd,
          Fin.castLE, hb, hc] using hpost (.v ⟨i, by omega⟩))
        (hbound (.v ⟨i, by omega⟩))
    constructor
    · apply le_antisymm _ (hbound (.b ⟨i + 1, hi⟩))
      simpa [circuitPoint, circuitRhs, PrimitiveRhs.eval, hb, hh, bValue_succ] using
        hpost (.b ⟨i + 1, hi⟩)
    · apply le_antisymm _ (hbound (.c ⟨i + 1, hi⟩))
      simpa [circuitPoint, circuitRhs, PrimitiveRhs.eval, hc, hv, cValue_succ] using
        hpost (.c ⟨i + 1, hi⟩)

/-- The unit upper bound pins the feedback coordinate of a sound postfixed point. -/
theorem circuitPostfixed_unique {n : ℕ} {x : CircuitVar n → ℝ}
    (hbound : ∀ a, circuitPoint n a ≤ x a) (hz : x .z ≤ 1)
    (hpost : ∀ a, x a ≤ (circuitRhs n a).eval x) :
    x = circuitPoint n := by
  have hz1 : x .z = 1 := le_antisymm hz (hbound .z)
  funext a
  cases a with
  | b i => exact (circuitPostfixed_upstream hbound hpost i).1
  | c i => exact (circuitPostfixed_upstream hbound hpost i).2
  | h i =>
    apply le_antisymm _ (hbound (.h i))
    simpa [circuitRhs, PrimitiveRhs.eval, circuitPoint,
      (circuitPostfixed_upstream hbound hpost i.castSucc).1] using hpost (.h i)
  | v i =>
    apply le_antisymm _ (hbound (.v i))
    simpa [circuitRhs, PrimitiveRhs.eval, circuitPoint,
      (circuitPostfixed_upstream hbound hpost i.castSucc).1,
      (circuitPostfixed_upstream hbound hpost i.castSucc).2] using hpost (.v i)
  | z => exact hz1
  | w =>
    apply le_antisymm _ (hbound .w)
    simpa [circuitRhs, PrimitiveRhs.eval, circuitPoint, hz1,
      (circuitPostfixed_upstream hbound hpost (Fin.last n)).2] using hpost .w

/-- Fair upper propagation converges to the same feasible point as the lower
    endpoints; together the two results establish a singleton limiting box. -/
theorem fair_circuit_upper_tendsto {n : ℕ}
    {upper : ℕ → CircuitVar n → ℝ} {schedule : ℕ → CircuitVar n}
    (hanti : ∀ a, Antitone fun t => upper t a)
    (hbound : ∀ t a, circuitPoint n a ≤ upper t a)
    (hunit : upper 0 .z ≤ 1)
    (hfair : FairSchedule schedule)
    (hforward : ∀ t, upper (t + 1) (schedule t) ≤
      (circuitRhs n (schedule t)).eval (upper t)) :
    Tendsto upper atTop (𝓝 (circuitPoint n)) := by
  have heq : upperLimit upper = circuitPoint n := circuitPostfixed_unique
    (le_upperLimit hbound) ((limit_le_upper hbound 0 .z).trans hunit)
    (fair_limit_postfixed hanti hbound hfair
      (fun a => (circuitRhs n a).continuous_eval) hforward)
  simpa only [heq] using upper_tendsto_limit hanti hbound

end FBBT
