import Formal.MultilinearGap.PhysicalEnvelope
import Formal.CubicGap.OrientationRounding

/-!
# Sorted threshold moments and the fair endpoint-orientation moments

This module completes the positive-box obligation PB05 and discharges PB07,
PB08 and PB09 of `formal/topics/18-positive-box/CLAIMS.md`.  It builds on the
moment interface of `Formal.MultilinearGap.PhysicalEnvelope`: every moment here
is a `binomMoment s μ j` with `j : ℤ`, so the PB12 conventions (order zero is
one, negative orders vanish, orders above the support cardinality vanish) hold
verbatim for this family too.

* PB05, sorted form: `PhysicalEnvelope` computed the common-threshold moment as
  the subset-minimum sum `C_j(u) = ∑_{A ⊆ s, |A| = j} min_{i ∈ A} u i`
  (`thresholdLaw_binomMoment`).  `thresholdLaw_binomMoment_sorted` turns that
  into the sorted form `C_j(u) = ∑_i u_(i) * binom(n - i, j - 1)` along any
  enumeration of the support that sorts the means.  Ties are handled by
  grouping the `j`-subsets by the *first sorted position* attaining the
  minimum, not by the minimal value; the grouping is carried out by the two
  peeling lemmas `sum_monomialUpper_peel_min` and `sum_monomialUpper_peel_max`,
  which extract the coefficients of the smallest and the largest sorted
  coordinate directly and are the form the spreading argument differentiates.

* PB07: `orientMoment s x j` is the `j`-th binomial moment of the fair
  endpoint-orientation law.  The law itself is `CubicGap.orientationLaw`, the
  one uniform variable with an independent fair choice per coordinate between
  the success intervals `[0, u i]` and `[1 - u i, 1]`, written in the folded
  parametrization of `Formal.CubicGap.OrientationRounding`: conditionally on the
  folded uniform variable the coordinates are independent, because flipping
  *all* orientation coins exchanges the two preimages of a folded value and
  preserves the fair coin measure.  Its means are `orientationLaw_hasMeans`,
  restated at the moment level as `orientMoment_one`.

* PB08: `two_mul_orientMoment_two` is `2 O_2 = C_2 + L_2` with
  `L_2 = frechetPairLower s x = ∑_{a < b} max (0, u a + u b - 1)`.  The per-pair
  reason — equal orientations with probability one half, opposite with
  probability one half, so the pair expectation is the average of the two
  Fréchet values — is `orientationLaw_expect_pair_frechet`.

* PB09: `orientMoment_mono` (coordinatewise monotone) and
  `orientMoment_update_sub_le` / `orientMoment_update_abs_le` (coordinate
  Lipschitz constant `binom(n - 1, j - 1)`).  The proof is the source's
  coupling, in its integrated form: the orientation law shares one uniform
  variable, so raising a single mean raises exactly that coordinate's
  conditional success probability, by a total amount `h`, and on that event the
  remaining `binom(n - 1, j - 1)` subsets each contribute a factor in `[0, 1]`.
  **No derivative is taken**; the partial derivatives need not exist on an
  orientation breakpoint.
-/

namespace MultilinearGap

open CubicGap MeasureTheory Set

noncomputable section

variable {I : Type*} [DecidableEq I]

/-! ## Splitting a sum over equal-cardinality subsets at one element -/

/-- Splitting the `(j+1)`-subsets of `s` at a distinguished element `a`: those
avoiding `a` are the `(j+1)`-subsets of `s.erase a`, and those containing `a`
are the `j`-subsets of `s.erase a` with `a` inserted. -/
theorem sum_powersetCard_succ_split {s : Finset I} {a : I} (ha : a ∈ s) (j : ℕ)
    (g : Finset I → ℝ) :
    ∑ A ∈ s.powersetCard (j + 1), g A =
      ∑ A ∈ (s.erase a).powersetCard (j + 1), g A +
        ∑ B ∈ (s.erase a).powersetCard j, g (insert a B) := by
  have hnot : a ∉ s.erase a := Finset.notMem_erase a s
  have hdisj : Disjoint ((s.erase a).powersetCard (j + 1))
      (((s.erase a).powersetCard j).image (insert a)) := by
    refine Finset.disjoint_left.mpr fun A hA hA' => ?_
    obtain ⟨B, _, rfl⟩ := Finset.mem_image.mp hA'
    exact hnot ((Finset.mem_powersetCard.mp hA).1 (Finset.mem_insert_self a B))
  have hinj : ∀ B ∈ (s.erase a).powersetCard j, ∀ B' ∈ (s.erase a).powersetCard j,
      insert a B = insert a B' → B = B' := by
    intro B hB B' hB' h
    have hB0 : a ∉ B := fun hmem => hnot ((Finset.mem_powersetCard.mp hB).1 hmem)
    have hB0' : a ∉ B' := fun hmem => hnot ((Finset.mem_powersetCard.mp hB').1 hmem)
    rw [← Finset.erase_insert hB0, ← Finset.erase_insert hB0', h]
  calc ∑ A ∈ s.powersetCard (j + 1), g A
      = ∑ A ∈ (insert a (s.erase a)).powersetCard (j + 1), g A := by
        rw [Finset.insert_erase ha]
    _ = ∑ A ∈ (s.erase a).powersetCard (j + 1) ∪
          ((s.erase a).powersetCard j).image (insert a), g A := by
        rw [Finset.powersetCard_succ_insert hnot]
    _ = ∑ A ∈ (s.erase a).powersetCard (j + 1), g A +
          ∑ B ∈ (s.erase a).powersetCard j, g (insert a B) := by
        rw [Finset.sum_union hdisj, Finset.sum_image hinj]

/-! ## PB05: the sorted common-threshold moment -/

/-- The subset minimum of a pair. -/
theorem monomialUpper_pair (x : I → ℝ) (a b : I) :
    monomialUpper ({a, b} : Finset I) x = min (x a) (x b) := by
  rcases le_total (x a) (x b) with h | h
  · rw [min_eq_left h]
    refine monomialUpper_eq_anchor _ _ a (Finset.mem_insert_self _ _) ?_
    intro i hi
    rcases Finset.mem_insert.mp hi with rfl | hi
    · exact le_rfl
    · rw [Finset.mem_singleton.mp hi]; exact h
  · rw [min_eq_right h]
    refine monomialUpper_eq_anchor _ _ b (by simp) ?_
    intro i hi
    rcases Finset.mem_insert.mp hi with rfl | hi
    · exact h
    · rw [Finset.mem_singleton.mp hi]

/-- Peeling a minimal coordinate: it carries the coefficient `binom(n - 1, j)`
in the subset-minimum sum of order `j + 1`, and the rest of the sum does not
depend on it.  Ties are irrelevant: any minimizer may be chosen. -/
theorem sum_monomialUpper_peel_min {s : Finset I} {a : I} (ha : a ∈ s) (x : I → ℝ)
    (hmin : ∀ i ∈ s, x a ≤ x i) (j : ℕ) :
    ∑ A ∈ s.powersetCard (j + 1), monomialUpper A x =
      x a * (((s.card - 1).choose j : ℕ) : ℝ) +
        ∑ A ∈ (s.erase a).powersetCard (j + 1), monomialUpper A x := by
  rw [sum_powersetCard_succ_split ha j fun A => monomialUpper A x]
  have hterm : ∀ B ∈ (s.erase a).powersetCard j, monomialUpper (insert a B) x = x a := by
    intro B hB
    refine monomialUpper_eq_anchor _ _ a (Finset.mem_insert_self a B) ?_
    intro i hi
    rcases Finset.mem_insert.mp hi with rfl | hi
    · exact le_rfl
    · exact hmin i (Finset.mem_of_mem_erase ((Finset.mem_powersetCard.mp hB).1 hi))
  rw [Finset.sum_congr rfl hterm, Finset.sum_const, Finset.card_powersetCard,
    Finset.card_erase_of_mem ha, nsmul_eq_mul, mul_comm, add_comm]

/-- Peeling a maximal coordinate: at orders at least two it carries coefficient
zero, the sum splitting into the two lower-dimensional sums of orders `j + 2`
and `j + 1`.  Ties are irrelevant: any maximizer may be chosen. -/
theorem sum_monomialUpper_peel_max {s : Finset I} {b : I} (hb : b ∈ s) (x : I → ℝ)
    (hmax : ∀ i ∈ s, x i ≤ x b) (j : ℕ) :
    ∑ A ∈ s.powersetCard (j + 2), monomialUpper A x =
      ∑ A ∈ (s.erase b).powersetCard (j + 2), monomialUpper A x +
        ∑ A ∈ (s.erase b).powersetCard (j + 1), monomialUpper A x := by
  rw [sum_powersetCard_succ_split hb (j + 1) fun A => monomialUpper A x]
  congr 1
  refine Finset.sum_congr rfl fun B hB => ?_
  obtain ⟨hBs, hBcard⟩ := Finset.mem_powersetCard.mp hB
  have hBne : B.Nonempty := Finset.card_pos.mp (by rw [hBcard]; exact Nat.succ_pos j)
  obtain ⟨i, hi, hile⟩ := monomial_min_anchor B hBne x
  rw [monomialUpper_eq_anchor _ _ i hi hile]
  refine monomialUpper_eq_anchor _ _ i (Finset.mem_insert_of_mem hi) ?_
  intro k hk
  rcases Finset.mem_insert.mp hk with rfl | hk
  · exact (hile i hi).trans (hmax i (Finset.mem_of_mem_erase (hBs hi)))
  · exact hile k hk

omit [DecidableEq I] in
/-- PB05, combinatorial core: along an enumeration `f` of the support that sorts
the means, the subset-minimum sum of order `j + 1` is
`∑_a u_(a) * binom(n - 1 - a, j)`. -/
theorem sum_monomialUpper_sorted (x : I → ℝ) (j : ℕ) :
    ∀ {n : ℕ} (f : Fin n ↪ I), (Monotone fun a => x (f a)) →
      ∑ A ∈ (Finset.univ.map f).powersetCard (j + 1), monomialUpper A x =
        ∑ a : Fin n, x (f a) * (((n - 1 - (a : ℕ)).choose j : ℕ) : ℝ) := by
  classical
  intro n
  induction n with
  | zero =>
    intro f _
    have hempty : (Finset.univ.map f).powersetCard (j + 1) = ∅ :=
      Finset.powersetCard_eq_empty.mpr (by simp)
    rw [hempty]
    simp
  | succ n ih =>
    intro f hmono
    have h0 : f 0 ∈ Finset.univ.map f := Finset.mem_map_of_mem f (Finset.mem_univ 0)
    have hmin : ∀ i ∈ Finset.univ.map f, x (f 0) ≤ x i := by
      intro i hi
      obtain ⟨b, -, rfl⟩ := Finset.mem_map.mp hi
      exact hmono (Fin.zero_le b)
    have hcard : (Finset.univ.map f).card = n + 1 := by simp
    let f' : Fin n ↪ I :=
      ⟨fun c => f c.succ, fun a b h => Fin.succ_injective n (f.injective h)⟩
    have herase : (Finset.univ.map f).erase (f 0) = Finset.univ.map f' := by
      ext i
      simp only [Finset.mem_erase, Finset.mem_map, Finset.mem_univ, true_and, f']
      constructor
      · rintro ⟨hne, b, rfl⟩
        rcases Fin.eq_zero_or_eq_succ b with rfl | ⟨c, rfl⟩
        · exact absurd rfl hne
        · exact ⟨c, rfl⟩
      · rintro ⟨c, rfl⟩
        refine ⟨fun h => Fin.succ_ne_zero c (f.injective h), c.succ, rfl⟩
    have hf'c : ∀ c : Fin n, f' c = f c.succ := fun _ => rfl
    have hmono' : Monotone fun c => x (f' c) := by
      intro c d hcd
      exact hmono (Fin.succ_le_succ_iff.mpr hcd)
    rw [sum_monomialUpper_peel_min h0 x hmin j, hcard, herase, ih f' hmono',
      Fin.sum_univ_succ]
    congr 1
    refine Finset.sum_congr rfl fun c _ => ?_
    have hnat : n + 1 - 1 - ((c.succ : Fin (n + 1)) : ℕ) = n - 1 - (c : ℕ) := by
      rw [Fin.val_succ]
      omega
    rw [hnat, hf'c]

omit [DecidableEq I] in
/-- A sorting enumeration of a support always exists. -/
theorem exists_sorted_emb (s : Finset I) (x : I → ℝ) :
    ∃ f : Fin s.card ↪ I, Finset.univ.map f = s ∧ Monotone fun a => x (f a) := by
  classical
  let g : Fin s.card → I := fun a => ((s.equivFin.symm a : { i // i ∈ s }) : I)
  have hg : Function.Injective g := fun a b h =>
    s.equivFin.symm.injective (Subtype.ext h)
  let σ := Tuple.sort fun a => x (g a)
  refine ⟨⟨fun a => g (σ a), fun a b h => σ.injective (hg h)⟩, ?_,
    Tuple.monotone_sort fun a => x (g a)⟩
  refine Finset.eq_of_subset_of_card_le ?_ ?_
  · intro i hi
    obtain ⟨a, -, rfl⟩ := Finset.mem_map.mp hi
    exact (s.equivFin.symm (σ a)).2
  · simp

variable [Fintype I]

/-- PB05, the sorted moment formula.  Along any enumeration `f : Fin n ↪ I` of
the support `s` that sorts the means, the common-threshold binomial moment of
order `j + 1` is `C_{j+1}(u) = ∑_a u_(a) * binom(n - 1 - a, j)`, the sorted form
`∑_i u_(i) * binom(n - i, j)` in zero-based indexing. -/
theorem thresholdLaw_binomMoment_sorted {n : ℕ} {s : Finset I} (f : Fin n ↪ I)
    (hf : Finset.univ.map f = s) (x : I → ℝ) (hx : x ∈ cube I)
    (hmono : Monotone fun a => x (f a)) (j : ℕ) :
    binomMoment s (thresholdLaw x) ((j + 1 : ℕ) : ℤ) =
      ∑ a : Fin n, x (f a) * (((n - 1 - (a : ℕ)).choose j : ℕ) : ℝ) := by
  rw [thresholdLaw_binomMoment s x hx, ← hf, sum_monomialUpper_sorted x j f hmono]

/-- PB05, coefficient extraction at the minimum: a minimal coordinate enters the
common-threshold moment of order `j + 1` with coefficient exactly
`binom(n - 1, j)`, the rest being the moment of the same order on the remaining
coordinates. -/
theorem thresholdLaw_binomMoment_peel_min {s : Finset I} {a : I} (ha : a ∈ s)
    (x : I → ℝ) (hx : x ∈ cube I) (hmin : ∀ i ∈ s, x a ≤ x i) (j : ℕ) :
    binomMoment s (thresholdLaw x) ((j + 1 : ℕ) : ℤ) =
      x a * (((s.card - 1).choose j : ℕ) : ℝ) +
        binomMoment (s.erase a) (thresholdLaw x) ((j + 1 : ℕ) : ℤ) := by
  rw [thresholdLaw_binomMoment s x hx, thresholdLaw_binomMoment (s.erase a) x hx,
    sum_monomialUpper_peel_min ha x hmin j]

/-- PB05, coefficient extraction at the maximum: at orders at least two a
maximal coordinate enters the common-threshold moment with coefficient zero. -/
theorem thresholdLaw_binomMoment_peel_max {s : Finset I} {b : I} (hb : b ∈ s)
    (x : I → ℝ) (hx : x ∈ cube I) (hmax : ∀ i ∈ s, x i ≤ x b) (j : ℕ) :
    binomMoment s (thresholdLaw x) ((j + 2 : ℕ) : ℤ) =
      binomMoment (s.erase b) (thresholdLaw x) ((j + 2 : ℕ) : ℤ) +
        binomMoment (s.erase b) (thresholdLaw x) ((j + 1 : ℕ) : ℤ) := by
  rw [thresholdLaw_binomMoment s x hx, thresholdLaw_binomMoment (s.erase b) x hx,
    thresholdLaw_binomMoment (s.erase b) x hx, sum_monomialUpper_peel_max hb x hmax j]

/-! ## PB07: the fair endpoint-orientation moments -/

/-- `O_j`: the `j`-th binomial moment of the fair endpoint-orientation law on
the support `s`.  The PB12 conventions are inherited from `binomMoment`. -/
def orientMoment (s : Finset I) (x : I → ℝ) (j : ℤ) : ℝ := binomMoment s (orientationLaw x) j

/-- PB12 for the orientation family: order zero is one. -/
@[simp] theorem orientMoment_zero (s : Finset I) (x : I → ℝ) : orientMoment s x 0 = 1 :=
  binomMoment_zero s _

/-- PB12 for the orientation family: negative orders vanish. -/
theorem orientMoment_of_neg (s : Finset I) (x : I → ℝ) {j : ℤ} (hj : j < 0) :
    orientMoment s x j = 0 :=
  binomMoment_of_neg s _ hj

/-- PB12 for the orientation family: orders above the support cardinality
vanish. -/
theorem orientMoment_of_card_lt (s : Finset I) (x : I → ℝ) {j : ℤ} (hj : (s.card : ℤ) < j) :
    orientMoment s x j = 0 :=
  binomMoment_of_card_lt s _ hj

/-- PB07, the prescribed means: the first orientation moment is the sum of the
means on the support. -/
theorem orientMoment_one (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    orientMoment s x 1 = ∑ i ∈ s, x i :=
  binomMoment_one s x _ (orientationLaw_hasMeans x hx)

/-- The orientation moments in integrated product form: one shared uniform
variable, conditionally independent coordinates. -/
theorem orientMoment_eq_sum_integral (s : Finset I) (x : I → ℝ) (j : ℕ) :
    orientMoment s x (j : ℤ) =
      ∑ A ∈ s.powersetCard j, ∫ t in (0 : ℝ)..1, ∏ i ∈ A, orientationProbability (x i) t := by
  rw [orientMoment, binomMoment_eq_sum_monomial]
  exact Finset.sum_congr rfl fun A _ => orientationLaw_expect_monomial x A

/-- The orientation moments are nonnegative. -/
theorem orientMoment_nonneg (s : Finset I) (x : I → ℝ) (j : ℤ) : 0 ≤ orientMoment s x j := by
  refine Finset.sum_nonneg fun v _ => mul_nonneg ((orientationLaw x).nonneg v) ?_
  simp only [chooseInt]
  split_ifs
  · exact Nat.cast_nonneg _
  · exact le_rfl

/-- PB07, generating form: the orientation expectation of a physical monomial is
`∑_j O_j t ^ j`. -/
theorem orientationLaw_physMonomial_eq_sum (t : ℝ) (s : Finset I) (x : I → ℝ) :
    (orientationLaw x).expect (fun v => physMonomial t s (vertexPoint v)) =
      ∑ j ∈ Finset.range (s.card + 1), orientMoment s x (j : ℤ) * t ^ j :=
  expect_physMonomial_eq_sum_binomMoment t s (orientationLaw x)

/-! ## PB08: the order-two identity -/

/-- `L_2 = ∑_{a < b} max (0, u a + u b - 1)`, the sum of the pairwise lower
Fréchet values on the support. -/
def frechetPairLower (s : Finset I) (x : I → ℝ) : ℝ :=
  ∑ A ∈ s.powersetCard 2, max 0 ((∑ i ∈ A, x i) - 1)

/-- PB08, the per-pair fact: two distinct coordinates have equal orientations
with probability one half and opposite orientations with probability one half,
so their orientation expectation is the average of their upper and lower
Fréchet values. -/
theorem orientationLaw_expect_pair_frechet (x : I → ℝ) (hx : x ∈ cube I) {a b : I}
    (hab : a ≠ b) :
    2 * (orientationLaw x).expect (fun v => monomial {a, b} (vertexPoint v)) =
      min (x a) (x b) + max 0 (x a + x b - 1) := by
  have key : ∀ u v : ℝ, u ∈ Icc (0 : ℝ) 1 → v ∈ Icc (0 : ℝ) 1 → u ≤ v →
      2 * ∫ t in (0 : ℝ)..1, orientationProbability u t * orientationProbability v t =
        min u v + max 0 (u + v - 1) := by
    intro u v hu hv huv
    rw [orientation_integral_pair hu hv huv, min_eq_left huv]
    rcases le_total u (1 - v) with h | h
    · rw [min_eq_left h, max_eq_left (by linarith)]; ring
    · rw [min_eq_right h, max_eq_right (by linarith)]; ring
  rcases le_total (x a) (x b) with h | h
  · rw [orientationLaw_expect_pair x a b hab]
    exact key _ _ (Set.mem_Icc.mpr (hx a)) (Set.mem_Icc.mpr (hx b)) h
  · rw [Finset.pair_comm a b, orientationLaw_expect_pair x b a hab.symm,
      min_comm, add_comm (x a) (x b)]
    exact key _ _ (Set.mem_Icc.mpr (hx b)) (Set.mem_Icc.mpr (hx a)) h

/-- **PB08**: `2 O_2 = C_2 + L_2`. -/
theorem two_mul_orientMoment_two (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    2 * orientMoment s x 2 = binomMoment s (thresholdLaw x) 2 + frechetPairLower s x := by
  rw [show (2 : ℤ) = ((2 : ℕ) : ℤ) from rfl, orientMoment, binomMoment_eq_sum_monomial,
    thresholdLaw_binomMoment s x hx, frechetPairLower, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun A hA => ?_
  obtain ⟨-, hcard⟩ := Finset.mem_powersetCard.mp hA
  obtain ⟨a, b, hab, rfl⟩ := Finset.card_eq_two.mp hcard
  rw [Finset.sum_pair hab, orientationLaw_expect_pair_frechet x hx hab, monomialUpper_pair]

/-! ## PB09: monotonicity and the coordinate Lipschitz bound -/

/-- Each conditional orientation success probability is nondecreasing in the
mean, at every value of the shared uniform variable. -/
theorem orientationProbability_mono {u v : ℝ} (huv : u ≤ v) (t : ℝ) :
    orientationProbability u t ≤ orientationProbability v t := by
  unfold orientationProbability lowerStep
  split_ifs <;> linarith

omit [Fintype I] [DecidableEq I] in
/-- Conditional orientation monomials take values in the unit interval. -/
theorem orientProd_mem_Icc (x : I → ℝ) (A : Finset I) (t : ℝ) :
    (∏ i ∈ A, orientationProbability (x i) t) ∈ Icc (0 : ℝ) 1 :=
  ⟨Finset.prod_nonneg fun i _ => (orientationProbability_mem (x i) t).1,
    Finset.prod_le_one (fun i _ => (orientationProbability_mem (x i) t).1)
      fun i _ => (orientationProbability_mem (x i) t).2⟩

omit [Fintype I] [DecidableEq I] in
/-- Conditional orientation monomials are integrable in the uniform variable. -/
theorem orientProd_integrable (x : I → ℝ) (A : Finset I) :
    IntervalIntegrable (fun t => ∏ i ∈ A, orientationProbability (x i) t) volume 0 1 :=
  intervalIntegrable_of_mem_unitInterval _
    (Finset.measurable_prod _ fun i _ => orientationProbability_measurable (x i))
    (orientProd_mem_Icc x A)

/-- **PB09, monotonicity**: every orientation moment is coordinatewise
nondecreasing in the means.  Proved by the shared-uniform coupling: raising the
means raises every conditional success probability pointwise. -/
theorem orientMoment_mono (s : Finset I) {x y : I → ℝ} (hxy : ∀ i, x i ≤ y i) (j : ℤ) :
    orientMoment s x j ≤ orientMoment s y j := by
  rcases lt_or_ge j 0 with hj | hj
  · rw [orientMoment_of_neg s x hj, orientMoment_of_neg s y hj]
  · obtain ⟨k, rfl⟩ := Int.eq_ofNat_of_zero_le hj
    rw [orientMoment_eq_sum_integral, orientMoment_eq_sum_integral]
    refine Finset.sum_le_sum fun A _ => ?_
    refine intervalIntegral.integral_mono (by norm_num) (orientProd_integrable x A)
      (orientProd_integrable y A) fun t => ?_
    exact Finset.prod_le_prod (fun i _ => (orientationProbability_mem (x i) t).1)
      fun i _ => orientationProbability_mono (hxy i) t

omit [Fintype I] in
/-- Updating one coordinate to a value of the unit interval stays in the cube. -/
theorem update_mem_cube {x : I → ℝ} (hx : x ∈ cube I) (i₀ : I) {r : ℝ}
    (hr0 : 0 ≤ r) (hr1 : r ≤ 1) : Function.update x i₀ r ∈ cube I := by
  intro i
  by_cases hi : i = i₀
  · subst hi; rw [Function.update_self]; exact ⟨hr0, hr1⟩
  · rw [Function.update_of_ne hi]; exact hx i

/-- **PB09, the Lipschitz bound**: raising a single mean from `x i₀` to `r`
raises the orientation moment of order `j + 1` by at most
`(r - x i₀) * binom(n - 1, j)`.

This is the source's coupling argument, in integrated form: the two laws share
the uniform variable and the orientation coins, the flipped coordinate turns
from failure to success on an event of total probability exactly `r - x i₀`, and
on that event each of the `binom(n - 1, j)` subsets containing `i₀` contributes a
conditional factor in `[0, 1]`.  No derivative is taken. -/
theorem orientMoment_update_sub_le (s : Finset I) {x : I → ℝ} (i₀ : I) {r : ℝ}
    (hx : x ∈ cube I) (hr0 : 0 ≤ r) (hr1 : r ≤ 1) (hle : x i₀ ≤ r) (j : ℕ) :
    orientMoment s (Function.update x i₀ r) ((j + 1 : ℕ) : ℤ) -
        orientMoment s x ((j + 1 : ℕ) : ℤ) ≤
      (r - x i₀) * (((s.card - 1).choose j : ℕ) : ℝ) := by
  set y := Function.update x i₀ r with hy
  have hy0 : y i₀ = r := Function.update_self i₀ r x
  have hyx : ∀ i, i ≠ i₀ → y i = x i := fun i hi => Function.update_of_ne hi r x
  have hdiff0 : 0 ≤ r - x i₀ := sub_nonneg.mpr hle
  rw [orientMoment_eq_sum_integral, orientMoment_eq_sum_integral, ← Finset.sum_sub_distrib]
  by_cases hmem : i₀ ∈ s
  · have hzero : ∀ A ∈ (s.erase i₀).powersetCard (j + 1),
        ((∫ t in (0 : ℝ)..1, ∏ i ∈ A, orientationProbability (y i) t) -
          ∫ t in (0 : ℝ)..1, ∏ i ∈ A, orientationProbability (x i) t) = 0 := by
      intro A hA
      have hA0 : i₀ ∉ A := fun hmem' =>
        Finset.notMem_erase i₀ s ((Finset.mem_powersetCard.mp hA).1 hmem')
      rw [sub_eq_zero]
      refine intervalIntegral.integral_congr fun t _ => ?_
      exact Finset.prod_congr rfl fun i hi =>
        congrArg (fun z => orientationProbability z t) (hyx i fun h => hA0 (h ▸ hi))
    have hterm : ∀ B ∈ (s.erase i₀).powersetCard j,
        ((∫ t in (0 : ℝ)..1, ∏ i ∈ insert i₀ B, orientationProbability (y i) t) -
          ∫ t in (0 : ℝ)..1, ∏ i ∈ insert i₀ B, orientationProbability (x i) t) ≤
        r - x i₀ := by
      intro B hB
      have hB0 : i₀ ∉ B := fun hmem' =>
        Finset.notMem_erase i₀ s ((Finset.mem_powersetCard.mp hB).1 hmem')
      have hbound : ∀ t, (∏ i ∈ insert i₀ B, orientationProbability (y i) t) -
          (∏ i ∈ insert i₀ B, orientationProbability (x i) t) ≤
          orientationProbability r t - orientationProbability (x i₀) t := by
        intro t
        have hBeq : (∏ i ∈ B, orientationProbability (y i) t) =
            ∏ i ∈ B, orientationProbability (x i) t :=
          Finset.prod_congr rfl fun i hi =>
            congrArg (fun z => orientationProbability z t) (hyx i fun h => hB0 (h ▸ hi))
        rw [Finset.prod_insert hB0, Finset.prod_insert hB0, hy0, hBeq]
        have hP := orientProd_mem_Icc x B t
        have hd : 0 ≤ orientationProbability r t - orientationProbability (x i₀) t :=
          sub_nonneg.mpr (orientationProbability_mono hle t)
        have h1 : (orientationProbability r t - orientationProbability (x i₀) t) *
            (∏ i ∈ B, orientationProbability (x i) t) ≤
            (orientationProbability r t - orientationProbability (x i₀) t) * 1 :=
          mul_le_mul_of_nonneg_left hP.2 hd
        linarith [h1]
      have hint : IntervalIntegrable
          (fun t => orientationProbability r t - orientationProbability (x i₀) t)
          volume 0 1 :=
        (orientationProbability_integrable r).sub (orientationProbability_integrable (x i₀))
      rw [← intervalIntegral.integral_sub (orientProd_integrable y _)
        (orientProd_integrable x _)]
      refine le_trans (intervalIntegral.integral_mono (by norm_num)
        (((orientProd_integrable y _).sub (orientProd_integrable x _))) hint hbound) ?_
      rw [intervalIntegral.integral_sub (orientationProbability_integrable r)
        (orientationProbability_integrable (x i₀)),
        orientationProbability_integral (Set.mem_Icc.mpr ⟨hr0, hr1⟩),
        orientationProbability_integral (Set.mem_Icc.mpr (hx i₀))]
    rw [sum_powersetCard_succ_split hmem j
      fun A => (∫ t in (0 : ℝ)..1, ∏ i ∈ A, orientationProbability (y i) t) -
        ∫ t in (0 : ℝ)..1, ∏ i ∈ A, orientationProbability (x i) t,
      Finset.sum_congr rfl hzero, Finset.sum_const, smul_zero, zero_add]
    refine le_trans (Finset.sum_le_card_nsmul _ _ _ hterm) ?_
    rw [Finset.card_powersetCard, Finset.card_erase_of_mem hmem, nsmul_eq_mul, mul_comm]
  · have hzero : ∀ A ∈ s.powersetCard (j + 1),
        ((∫ t in (0 : ℝ)..1, ∏ i ∈ A, orientationProbability (y i) t) -
          ∫ t in (0 : ℝ)..1, ∏ i ∈ A, orientationProbability (x i) t) = 0 := by
      intro A hA
      have hA0 : i₀ ∉ A := fun hmem' => hmem ((Finset.mem_powersetCard.mp hA).1 hmem')
      rw [sub_eq_zero]
      refine intervalIntegral.integral_congr fun t _ => ?_
      exact Finset.prod_congr rfl fun i hi =>
        congrArg (fun z => orientationProbability z t) (hyx i fun h => hA0 (h ▸ hi))
    rw [Finset.sum_congr rfl hzero, Finset.sum_const, smul_zero]
    exact mul_nonneg hdiff0 (Nat.cast_nonneg _)

/-- **PB09**, two-sided form: the orientation moment of order `j + 1` is
Lipschitz in each coordinate with constant `binom(n - 1, j)`. -/
theorem orientMoment_update_abs_le (s : Finset I) {x : I → ℝ} (i₀ : I) {r : ℝ}
    (hx : x ∈ cube I) (hr0 : 0 ≤ r) (hr1 : r ≤ 1) (j : ℕ) :
    |orientMoment s (Function.update x i₀ r) ((j + 1 : ℕ) : ℤ) -
        orientMoment s x ((j + 1 : ℕ) : ℤ)| ≤
      |r - x i₀| * (((s.card - 1).choose j : ℕ) : ℝ) := by
  rcases le_total (x i₀) r with h | h
  · have hmono : orientMoment s x ((j + 1 : ℕ) : ℤ) ≤
        orientMoment s (Function.update x i₀ r) ((j + 1 : ℕ) : ℤ) := by
      refine orientMoment_mono s (fun i => ?_) _
      by_cases hi : i = i₀
      · subst hi; rw [Function.update_self]; exact h
      · rw [Function.update_of_ne hi]
    rw [abs_of_nonneg (sub_nonneg.mpr hmono), abs_of_nonneg (sub_nonneg.mpr h)]
    exact orientMoment_update_sub_le s i₀ hx hr0 hr1 h j
  · set y := Function.update x i₀ r with hy
    have hy0 : y i₀ = r := Function.update_self i₀ r x
    have hycube : y ∈ cube I := update_mem_cube hx i₀ hr0 hr1
    have hback : Function.update y i₀ (x i₀) = x := by
      rw [hy, Function.update_idem, Function.update_eq_self]
    have hmono : orientMoment s y ((j + 1 : ℕ) : ℤ) ≤ orientMoment s x ((j + 1 : ℕ) : ℤ) := by
      refine orientMoment_mono s (fun i => ?_) _
      by_cases hi : i = i₀
      · subst hi; rw [hy0]; exact h
      · rw [hy, Function.update_of_ne hi]
    have hstep := orientMoment_update_sub_le s (x := y) i₀ hycube (hx i₀).1 (hx i₀).2
      (by rw [hy0]; exact h) j
    rw [hback, hy0] at hstep
    rw [abs_of_nonpos (sub_nonpos.mpr hmono), abs_of_nonpos (by linarith)]
    linarith

end

end MultilinearGap
