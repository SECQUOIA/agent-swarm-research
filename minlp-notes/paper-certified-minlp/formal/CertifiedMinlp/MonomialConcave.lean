import Mathlib.Analysis.MeanInequalities
import Mathlib.Analysis.SpecialFunctions.Pow.Continuity
import Mathlib.Analysis.Convex.SpecificFunctions.Basic

/-! Concavity of real monomials, including the continuous nonnegative boundary. -/
namespace CertifiedMinlp

open Finset

variable {I : Type*} [Fintype I]

/-- Real-power monomial; zero exponents contribute one, including at zero. -/
noncomputable def realMonomial (a x : I → ℝ) : ℝ := ∏ i, x i ^ a i

def positiveOrthant : Set (I → ℝ) := {x | ∀ i, 0 < x i}

def nonnegativeOrthant : Set (I → ℝ) := {x | ∀ i, 0 ≤ x i}

omit [Fintype I] in
theorem convex_positiveOrthant : Convex ℝ (positiveOrthant : Set (I → ℝ)) := by
  intro x hx y hy a b ha hb hab i
  change 0 < a * x i + b * y i
  rcases lt_or_eq_of_le hb with hb | hb
  · exact add_pos_of_nonneg_of_pos (mul_nonneg ha (hx i).le) (mul_pos hb (hy i))
  · have ha' : a = 1 := by linarith
    simp [← hb, ha', hx i]

omit [Fintype I] in
theorem convex_nonnegativeOrthant : Convex ℝ (nonnegativeOrthant : Set (I → ℝ)) := by
  intro x hx y hy a b ha hb _ i
  exact add_nonneg (mul_nonneg ha (hx i)) (mul_nonneg hb (hy i))

theorem realMonomial_continuous (a : I → ℝ) (ha : ∀ i, 0 ≤ a i) :
    Continuous (realMonomial a) := by
  unfold realMonomial
  exact continuous_finsetProd _ fun i _ =>
    (Real.continuous_rpow_const (ha i)).comp (continuous_apply i)

theorem realMonomial_pos (a x : I → ℝ) (hx : x ∈ positiveOrthant) :
    0 < realMonomial a x :=
  Finset.prod_pos fun i _ => Real.rpow_pos_of_pos (hx i) _

/-- AM-GM with unused weight assigned to the constant one. -/
theorem realMonomial_le_affine (a x : I → ℝ) (ha : ∀ i, 0 ≤ a i)
    (hs : ∑ i, a i ≤ 1) (hx : x ∈ nonnegativeOrthant) :
    realMonomial a x ≤ (1 - ∑ i, a i) + ∑ i, a i * x i := by
  let w : Option I → ℝ := Option.elim' (1 - ∑ i, a i) a
  let z : Option I → ℝ := Option.elim' 1 x
  have hw : ∀ i ∈ (univ : Finset (Option I)), 0 ≤ w i := by
    intro i _
    cases i with
    | none => exact sub_nonneg.mpr hs
    | some i => exact ha i
  have hw' : ∑ i, w i = 1 := by simp [w, Fintype.sum_option]
  have hz : ∀ i ∈ (univ : Finset (Option I)), 0 ≤ z i := by
    intro i _
    cases i with
    | none => exact zero_le_one
    | some i => exact hx i
  simpa [w, z, Fintype.prod_option, Fintype.sum_option, realMonomial] using
    Real.geom_mean_le_arith_mean_weighted univ w z hw hw' hz

/-- Each positive point supplies a global affine upper support. -/
theorem realMonomial_support (a x z : I → ℝ) (ha : ∀ i, 0 ≤ a i)
    (hs : ∑ i, a i ≤ 1) (hx : x ∈ nonnegativeOrthant)
    (hz : z ∈ positiveOrthant) :
    realMonomial a x ≤ realMonomial a z *
      ((1 - ∑ i, a i) + ∑ i, a i * (x i / z i)) := by
  have h := realMonomial_le_affine a (fun i => x i / z i) ha hs
    (fun i => div_nonneg (hx i) (hz i).le)
  have heq : realMonomial a (fun i => x i / z i) =
      realMonomial a x / realMonomial a z := by
    simp only [realMonomial, Real.div_rpow (hx _) (hz _).le, Finset.prod_div_distrib]
  rw [heq] at h
  exact (div_le_iff₀ (realMonomial_pos a z hz)).mp h |>.trans_eq (mul_comm _ _)

theorem realMonomial_concaveOn_positiveOrthant (a : I → ℝ)
    (ha : ∀ i, 0 ≤ a i) (hs : ∑ i, a i ≤ 1) :
    ConcaveOn ℝ positiveOrthant (realMonomial a) := by
  refine ⟨convex_positiveOrthant, ?_⟩
  intro x hx y hy b c hb hc hbc
  let z := b • x + c • y
  have hz : z ∈ positiveOrthant := convex_positiveOrthant hx hy hb hc hbc
  have h1 := realMonomial_support a x z ha hs (fun i => (hx i).le) hz
  have h2 := realMonomial_support a y z ha hs (fun i => (hy i).le) hz
  have hid : b * ((1 - ∑ i, a i) + ∑ i, a i * (x i / z i)) +
      c * ((1 - ∑ i, a i) + ∑ i, a i * (y i / z i)) = 1 := by
    calc
      _ = (b + c) * (1 - ∑ i, a i) +
          ∑ i, a i * ((b * x i + c * y i) / z i) := by
        have he : (∑ i, a i * ((b * x i + c * y i) / z i)) =
            b * (∑ i, a i * (x i / z i)) + c * (∑ i, a i * (y i / z i)) := by
          simp only [Finset.mul_sum, ← Finset.sum_add_distrib]
          apply Finset.sum_congr rfl
          intro i _
          ring
        rw [he]
        ring
      _ = 1 := by
        have heach : ∀ i, (b * x i + c * y i) / z i = 1 := by
          intro i
          change z i / z i = 1
          exact div_self (ne_of_gt (hz i))
        simp [hbc, heach]
  change b * realMonomial a x + c * realMonomial a y ≤ realMonomial a z
  calc
    _ ≤ b * (realMonomial a z * _) + c * (realMonomial a z * _) :=
      add_le_add (mul_le_mul_of_nonneg_left h1 hb) (mul_le_mul_of_nonneg_left h2 hc)
    _ = realMonomial a z * (b * ((1 - ∑ i, a i) + ∑ i, a i * (x i / z i)) +
        c * ((1 - ∑ i, a i) + ∑ i, a i * (y i / z i))) := by ring
    _ = realMonomial a z := by rw [hid, mul_one]

/-- Concavity passes to zero coordinates by continuity. -/
theorem realMonomial_concaveOn_nonnegativeOrthant (a : I → ℝ)
    (ha : ∀ i, 0 ≤ a i) (hs : ∑ i, a i ≤ 1) :
    ConcaveOn ℝ nonnegativeOrthant (realMonomial a) := by
  refine ⟨convex_nonnegativeOrthant, ?_⟩
  intro x hx y hy b c hb hc hbc
  let f : ℝ → ℝ := fun t => b * realMonomial a (fun i => x i + t) +
    c * realMonomial a (fun i => y i + t)
  let g : ℝ → ℝ := fun t =>
    realMonomial a (b • (fun i => x i + t) + c • (fun i => y i + t))
  have hcont := realMonomial_continuous a ha
  have hf : Continuous f := by unfold f; fun_prop
  have hg : Continuous g := by unfold g; fun_prop
  have hsub : Set.Ioi (0 : ℝ) ⊆ {t | f t ≤ g t} := by
    intro t ht
    exact (realMonomial_concaveOn_positiveOrthant a ha hs).2
      (fun i => add_pos_of_nonneg_of_pos (hx i) ht)
      (fun i => add_pos_of_nonneg_of_pos (hy i) ht) hb hc hbc
  have hzero : (0 : ℝ) ∈ closure (Set.Ioi (0 : ℝ)) := by simp
  have h := closure_minimal hsub (isClosed_le hf hg) hzero
  simpa [f, g] using h

/-- A monomial supported on one coordinate is exactly that coordinate power. -/
theorem realMonomial_single (a x : I → ℝ) (j : I)
    (hzero : ∀ i, i ≠ j → a i = 0) : realMonomial a x = x j ^ a j := by
  classical
  unfold realMonomial
  exact Finset.prod_eq_single j (by intros; simp [hzero _ ‹_›]) (by simp)

/-- The nonnegative boundary in the convex single-positive-exponent case. -/
theorem realMonomial_convexOn_nonnegativeOrthant_single (a : I → ℝ) (j : I)
    (hj : 1 ≤ a j) (hzero : ∀ i, i ≠ j → a i = 0) :
    ConvexOn ℝ nonnegativeOrthant (realMonomial a) := by
  refine ⟨convex_nonnegativeOrthant, ?_⟩
  intro x hx y hy b c hb hc hbc
  simp only [realMonomial_single a _ j hzero]
  exact (convexOn_rpow hj).2 (hx j) (hy j) hb hc hbc

omit [Fintype I] in
/-- Any continuous function convex on the positive orthant remains convex on its boundary. -/
theorem convexOn_nonnegativeOrthant_of_continuous (f : (I → ℝ) → ℝ)
    (hf : Continuous f) (hpos : ConvexOn ℝ positiveOrthant f) :
    ConvexOn ℝ nonnegativeOrthant f := by
  refine ⟨convex_nonnegativeOrthant, ?_⟩
  intro x hx y hy b c hb hc hbc
  let lhs : ℝ → ℝ := fun t =>
    f (b • (fun i => x i + t) + c • (fun i => y i + t))
  let rhs : ℝ → ℝ := fun t => b * f (fun i => x i + t) + c * f (fun i => y i + t)
  have hlhs : Continuous lhs := by unfold lhs; fun_prop
  have hrhs : Continuous rhs := by unfold rhs; fun_prop
  have hsub : Set.Ioi (0 : ℝ) ⊆ {t | lhs t ≤ rhs t} := by
    intro t ht
    exact hpos.2 (fun i => add_pos_of_nonneg_of_pos (hx i) ht)
      (fun i => add_pos_of_nonneg_of_pos (hy i) ht) hb hc hbc
  have hzero : (0 : ℝ) ∈ closure (Set.Ioi (0 : ℝ)) := by simp
  have h := closure_minimal hsub (isClosed_le hlhs hrhs) hzero
  simpa [lhs, rhs] using h

end CertifiedMinlp
