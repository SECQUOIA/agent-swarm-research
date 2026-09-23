import Formal.MultilinearGap.MonomialEnvelope
import Formal.MultilinearGap.PhysicalEnvelope
import Formal.MultilinearGap.PositiveBox

/-! # The complete positive bilinear graph and the lower bound two

This file formalizes the `2` branch of the positive-box lower bound (PB44),
together with the PB42-style positive scaling it needs.

The witness is the complete positive bilinear graph: `2 * m` variables, one
monomial `z_a z_b` with coefficient one for every unordered pair `a ≠ b`,
evaluated at the point where every normalized mean is one half. Its exact
termwise-to-hull ratio in `n = 2 * m ≥ 2` variables is `2 * (n - 1) / n`
(`bilinearGraph_cube_ratio`), which tends to two along the even dimensions
(`bilinearGraph_ratio_tendsto`). In an odd dimension `n = 2 * m + 1 ≥ 3` the
ratio is `2 * n / (n + 1)` (`bilinearGraph_cube_ratio_odd`), because the mean
success count is a half integer and the convex envelope is the chord value
of the adjacent-count law. At `n = 1` both gaps vanish, so the totalized ratio
is zero.

The two cube envelopes are exact. The concave value is the common-threshold
value `C(n, 2) / 2` of `positive_polynomial_maximum_general`; the convex value
is `C(m, 2)` when `n = 2 * m`, proved by a tangent-line bound on the success
count (the pointwise inequality is `(K - m) ^ 2 ≥ 0`) together with the uniform
rotation of the balanced vertex, which attains it. When `n = 2 * m + 1`, the
convex value is `m ^ 2 / 2`, proved using the discrete convexity of the count
objective and attainment by an adjacent-count law.

The transfer to `[1, rho]^n` is exact as well. Rescaling multiplies every
bilinear term by the common positive factor `(rho - 1) ^ 2` and adds terms of
degree at most one. Such terms are *mean exact* (`MeanExact`): every law with
the prescribed means integrates them to the same value, so they have zero gap
(`affine_hullGap_eq_zero`) and only shift the envelope by a constant
(`hullGap_of_meanExact_split`). Both gaps are therefore multiplied by
`(rho - 1) ^ 2` and the ratio is unchanged (`bilinearGraph_box_ratio_eq`).

To let `PositiveBoxHeadline` combine these lower bounds with the upper bound
without a circular boundedness argument, the conclusion has two forms: every
upper bound of the ratio set is at least two (`two_le_of_forall_mem_boxAspectRatios`),
and `2 ≤ C_box(rho)` under an explicit `BddAbove` hypothesis
(`two_le_boxAspectSupremum`).

All box semantics, the affine invariance `boxHullGap_eq_of_mem`, the expansion
`monomial_box_expansion`, the common-threshold maximum
`positive_polynomial_maximum_general`, the exact monomial gap
`monomial_hullGap_of_min_coordinate`, the class `commonAspectBoxRatios` and its
inclusion `commonAspectBoxRatios_subset_boxAspectRatios` are reused unchanged.
-/

namespace MultilinearGap

open CubicGap Filter Topology

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-! ## Mean-exact parts: affine terms have zero gap -/

/-- A part of a polynomial that every law with the prescribed means integrates
to the same value. Such a part shifts all envelope values by one constant and
therefore contributes no gap. Terms of degree at most one are the example. -/
def MeanExact (x : I → ℝ) (g : (I → ℝ) → ℝ) : Prop :=
  ∀ μ : Law (Vertex I), HasMeans μ x → μ.expect (fun v => g (vertexPoint v)) = g x

private theorem expect_finset_sum {ι κ : Type*} [Fintype ι] (μ : Law ι)
    (S : Finset κ) (f : κ → ι → ℝ) :
    μ.expect (fun v => ∑ s ∈ S, f s v) = ∑ s ∈ S, μ.expect (f s) := by
  simp only [Law.expect, Finset.mul_sum]
  rw [Finset.sum_comm]

/-- Mean exactness passes to finite sums. -/
theorem meanExact_sum {x : I → ℝ} {κ : Type*} (S : Finset κ) (g : κ → (I → ℝ) → ℝ)
    (hg : ∀ s ∈ S, MeanExact x (g s)) : MeanExact x (fun q => ∑ s ∈ S, g s q) := by
  intro μ hm
  exact (expect_finset_sum μ S (fun s v => g s (vertexPoint v))).trans
    (Finset.sum_congr rfl fun s hs => hg s hs μ hm)

/-- Mean exactness passes to constant multiples. -/
theorem meanExact_const_mul {x : I → ℝ} (c : ℝ) (g : (I → ℝ) → ℝ) (hg : MeanExact x g) :
    MeanExact x (fun q => c * g q) := by
  intro μ hm
  rw [Law.expect_const_mul, hg μ hm]

/-- A monomial of degree at most one is mean exact: constants and single
coordinates are integrated exactly by the mean constraints. -/
theorem meanExact_monomial_of_card_le_one {x : I → ℝ} (t : Finset I) (ht : t.card ≤ 1) :
    MeanExact x (monomial t) := by
  intro μ hm
  rcases Nat.eq_zero_or_pos t.card with h0 | h1
  · rw [Finset.card_eq_zero.mp h0]
    simp [monomial]
  · obtain ⟨i, rfl⟩ := Finset.card_eq_one.mp (le_antisymm ht h1)
    simpa [monomial] using hm i

/-- Every polynomial all of whose terms have degree at most one is mean exact. -/
theorem meanExact_supportPolynomial_of_degree_le_one {x : I → ℝ}
    (T : Finset (Finset I)) (b : Finset I → ℝ) (hT : ∀ t ∈ T, t.card ≤ 1) :
    MeanExact x (supportPolynomial T b) := by
  have h : MeanExact x (fun q => ∑ t ∈ T, b t * monomial t q) :=
    meanExact_sum T _ fun t ht =>
      meanExact_const_mul (b t) _ (meanExact_monomial_of_card_le_one t (hT t ht))
  exact h

/-- Affine terms have zero gap: a polynomial of degree at most one has exactly
one envelope value at every point of the cube. -/
theorem affine_hullGap_eq_zero (T : Finset (Finset I)) (b : Finset I → ℝ)
    (hT : ∀ t ∈ T, t.card ≤ 1) (x : I → ℝ) (hx : x ∈ cube I) :
    hullGap (supportPolynomial T b) x = 0 := by
  have hset : envelopeValues (supportPolynomial T b) x = {supportPolynomial T b x} := by
    ext z
    constructor
    · intro hz
      obtain ⟨μ, hmean, hv⟩ := (mem_cubeGraph_hull_iff _
        (supportPolynomial_coordinate_affine T b) x z).mp hz
      exact hv.symm.trans (meanExact_supportPolynomial_of_degree_le_one T b hT μ hmean)
    · rintro rfl
      exact subset_convexHull ℝ _ ⟨hx, rfl⟩
  rw [hullGap, hset, csSup_singleton, csInf_singleton, sub_self]

/-- Positive scaling with a mean-exact shift multiplies the gap by the scale:
if `h = c * f + g` with `0 ≤ c` and `g` mean exact at `x`, then the whole
envelope of `h` is the envelope of `f` scaled by `c` and translated by `g x`. -/
theorem hullGap_of_meanExact_split (f g h : (I → ℝ) → ℝ)
    (hf : SeparatelyAffine f) (hh : SeparatelyAffine h)
    (x : I → ℝ) (hx : x ∈ cube I) (c : ℝ) (hc : 0 ≤ c)
    (hsplit : ∀ q, h q = c * f q + g q) (hg : MeanExact x g) :
    hullGap h x = c * hullGap f x := by
  have hfwd : ∀ z ∈ envelopeValues h x, ∃ w ∈ envelopeValues f x, z = c * w + g x := by
    intro z hz
    obtain ⟨μ, hmean, hv⟩ := (mem_cubeGraph_hull_iff h hh x z).mp hz
    refine ⟨μ.expect (fun v => f (vertexPoint v)),
      (mem_cubeGraph_hull_iff f hf x _).mpr ⟨μ, hmean, rfl⟩, ?_⟩
    rw [← hv]
    simp_rw [hsplit]
    rw [Law.expect_add, Law.expect_const_mul, hg μ hmean]
  have hbwd : ∀ w ∈ envelopeValues f x, c * w + g x ∈ envelopeValues h x := by
    intro w hw
    obtain ⟨μ, hmean, hv⟩ := (mem_cubeGraph_hull_iff f hf x w).mp hw
    refine (mem_cubeGraph_hull_iff h hh x _).mpr ⟨μ, hmean, ?_⟩
    simp_rw [hsplit]
    rw [Law.expect_add, Law.expect_const_mul, hg μ hmean, hv]
  obtain ⟨hlow, hhigh⟩ := envelopeValues_endpoints f hf x hx
  have hmax : IsGreatest (envelopeValues h x) (c * sSup (envelopeValues f x) + g x) := by
    refine ⟨hbwd _ hhigh.1, ?_⟩
    intro z hz
    obtain ⟨w, hw, rfl⟩ := hfwd z hz
    have h := mul_le_mul_of_nonneg_left (hhigh.2 hw) hc
    linarith
  have hmin : IsLeast (envelopeValues h x) (c * sInf (envelopeValues f x) + g x) := by
    refine ⟨hbwd _ hlow.1, ?_⟩
    intro z hz
    obtain ⟨w, hw, rfl⟩ := hfwd z hz
    have h := mul_le_mul_of_nonneg_left (hlow.2 hw) hc
    linarith
  rw [hullGap, hmax.csSup_eq, hmin.csInf_eq, hullGap]
  ring

/-! ## PB42: positive scaling of a bilinear graph to `[1, rho]^n` -/

/-- The degree at most one remainder of one bilinear term rescaled from the unit
cube to `[1, rho]`, read off the positive affine expansion. -/
def boxPairRemainder (rho : ℝ) (s : Finset I) (q : I → ℝ) : ℝ :=
  ∑ t ∈ s.powerset.erase s,
    boxExpansionCoefficient (fun _ => (1 : ℝ)) (fun _ => rho) s t * monomial t q

omit [Fintype I] in
/-- Every proper subset of a pair has degree at most one. -/
theorem card_le_one_of_mem_powerset_erase {s t : Finset I} (hs : s.card = 2)
    (ht : t ∈ s.powerset.erase s) : t.card ≤ 1 := by
  obtain ⟨hne, hmem⟩ := Finset.mem_erase.mp ht
  have hsub : t ⊆ s := Finset.mem_powerset.mp hmem
  have hlt : t.card < s.card :=
    Finset.card_lt_card (Finset.ssubset_iff_subset_ne.mpr ⟨hsub, hne⟩)
  omega

omit [Fintype I] in
/-- The exact expansion of one rescaled bilinear term: the common positive
factor `(rho - 1) ^ 2` on the quadratic part, plus terms of degree at most one. -/
theorem monomial_box_pair_split (rho : ℝ) (s : Finset I) (hs : s.card = 2) (q : I → ℝ) :
    monomial s (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q) =
      (rho - 1) ^ 2 * monomial s q + boxPairRemainder rho s q := by
  have hcoef : boxExpansionCoefficient (fun _ => (1 : ℝ)) (fun _ => rho) s s =
      (rho - 1) ^ 2 := by
    simp [boxExpansionCoefficient, hs]
  rw [monomial_box_expansion]
  simp only [supportPolynomial]
  rw [← Finset.add_sum_erase _
    (fun t => boxExpansionCoefficient (fun _ => (1 : ℝ)) (fun _ => rho) s t * monomial t q)
    (Finset.mem_powerset_self s), hcoef]
  rfl

/-- The remainder of a rescaled bilinear term is mean exact. -/
theorem meanExact_boxPairRemainder (rho : ℝ) (s : Finset I) (hs : s.card = 2)
    (x : I → ℝ) : MeanExact x (boxPairRemainder rho s) := by
  have h : MeanExact x (fun q => ∑ t ∈ s.powerset.erase s,
      boxExpansionCoefficient (fun _ => (1 : ℝ)) (fun _ => rho) s t * monomial t q) :=
    meanExact_sum _ _ fun t ht =>
      meanExact_const_mul _ _
        (meanExact_monomial_of_card_le_one t (card_le_one_of_mem_powerset_erase hs ht))
  exact h

/-- PB42 for one bilinear term: the positive affine map onto `[1, rho]` multiplies
its gap by the common factor `(rho - 1) ^ 2`. -/
theorem boxHullGap_pair_monomial (rho : ℝ) (hrho : 1 ≤ rho) (s : Finset I) (hs : s.card = 2)
    (p : I → ℝ) (hp : p ∈ cube I) :
    boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (monomial s)
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) =
      (rho - 1) ^ 2 * hullGap (monomial s) p := by
  rw [boxHullGap_eq_of_mem _ _ (fun _ => hrho) _ p hp]
  exact hullGap_of_meanExact_split (monomial s) (boxPairRemainder rho s) _
    (monomial_coordinate_affine s)
    (separatelyAffine_box_monomial (fun _ => (1 : ℝ)) (fun _ => rho) s)
    p hp _ (sq_nonneg _) (monomial_box_pair_split rho s hs)
    (meanExact_boxPairRemainder rho s hs p)

/-- PB42 for a whole positive bilinear graph: the full hull gap is multiplied by
the same common factor. -/
theorem boxHullGap_bilinear (rho : ℝ) (hrho : 1 ≤ rho) (S : Finset (Finset I))
    (a : Finset I → ℝ) (hS : ∀ s ∈ S, s.card = 2) (p : I → ℝ) (hp : p ∈ cube I) :
    boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (supportPolynomial S a)
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) =
      (rho - 1) ^ 2 * hullGap (supportPolynomial S a) p := by
  rw [boxHullGap_eq_of_mem _ _ (fun _ => hrho) _ p hp]
  refine hullGap_of_meanExact_split (supportPolynomial S a)
    (fun q => ∑ s ∈ S, a s * boxPairRemainder rho s q) _
    (supportPolynomial_coordinate_affine S a)
    (separatelyAffine_boxPoint _ (supportPolynomial_coordinate_affine S a) _ _)
    p hp _ (sq_nonneg _) ?_ ?_
  · intro q
    simp only [supportPolynomial]
    rw [Finset.mul_sum, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun s hs => ?_
    rw [monomial_box_pair_split rho s (hS s hs)]
    ring
  · exact meanExact_sum S _ fun s hs =>
      meanExact_const_mul _ _ (meanExact_boxPairRemainder rho s (hS s hs) p)

/-- PB42 for the termwise relaxation: every term gap is multiplied by the same
common factor. -/
theorem boxTermwiseGap_bilinear (rho : ℝ) (hrho : 1 ≤ rho) (S : Finset (Finset I))
    (a : Finset I → ℝ) (hS : ∀ s ∈ S, s.card = 2) (p : I → ℝ) (hp : p ∈ cube I) :
    boxTermwiseGap S a (fun _ => (1 : ℝ)) (fun _ => rho)
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) =
      (rho - 1) ^ 2 * weightedTermwiseGap S a p := by
  unfold boxTermwiseGap weightedTermwiseGap
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun s hs => ?_
  rw [boxHullGap_pair_monomial rho hrho s (hS s hs) p hp]
  ring

/-- PB42, ratio form: positive affine scaling of a bilinear graph to `[1, rho]^n`
leaves the termwise-to-hull ratio unchanged. -/
theorem bilinearGraph_box_ratio_eq (rho : ℝ) (hrho : 1 < rho) (S : Finset (Finset I))
    (a : Finset I → ℝ) (hS : ∀ s ∈ S, s.card = 2) (p : I → ℝ) (hp : p ∈ cube I) :
    boxTermwiseGap S a (fun _ => (1 : ℝ)) (fun _ => rho)
          (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) /
        boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (supportPolynomial S a)
          (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) p) =
      weightedTermwiseGap S a p / hullGap (supportPolynomial S a) p := by
  have hne : (rho - 1) ^ 2 ≠ 0 := pow_ne_zero 2 (sub_ne_zero.mpr hrho.ne')
  rw [boxTermwiseGap_bilinear rho hrho.le S a hS p hp,
    boxHullGap_bilinear rho hrho.le S a hS p hp, mul_div_mul_left _ _ hne]

/-! ## The complete positive bilinear graph on the unit cube -/

/-- The complete bilinear support: every unordered pair of distinct coordinates. -/
def bilinearSupports (I : Type*) [Fintype I] [DecidableEq I] : Finset (Finset I) :=
  Finset.univ.powersetCard 2

/-- The complete positive bilinear graph: coefficient one on every pair. -/
def bilinearGraph (I : Type*) [Fintype I] [DecidableEq I] : (I → ℝ) → ℝ :=
  supportPolynomial (bilinearSupports I) (fun _ => 1)

/-- The point where every normalized coordinate mean is one half. -/
def halfPoint (I : Type*) : I → ℝ := fun _ => 1 / 2

theorem mem_bilinearSupports {s : Finset I} : s ∈ bilinearSupports I ↔ s.card = 2 := by
  simp [bilinearSupports, Finset.mem_powersetCard]

theorem bilinearSupports_card :
    (bilinearSupports I).card = (Fintype.card I).choose 2 := by
  simp [bilinearSupports, Finset.card_powersetCard]

omit [Fintype I] [DecidableEq I] in
theorem halfPoint_mem_cube : halfPoint I ∈ cube I := fun _ => by
  constructor <;> norm_num [halfPoint]

theorem separatelyAffine_bilinearGraph : SeparatelyAffine (bilinearGraph I) :=
  supportPolynomial_coordinate_affine _ _

theorem bilinearGraph_eq_elementary (x : I → ℝ) : bilinearGraph I x = elementary 2 x := by
  simp [bilinearGraph, bilinearSupports, supportPolynomial, elementary, monomial]

/-- At a vertex the bilinear graph counts the pairs of successful coordinates. -/
theorem bilinearGraph_vertex (v : Vertex I) :
    bilinearGraph I (vertexPoint v) = ((count v).choose 2 : ℝ) := by
  rw [bilinearGraph_eq_elementary]
  exact elementary_binary 2 v

/-- The exact concave value at the half point: common-threshold rounding attains
every pair's minimum coordinate simultaneously. -/
theorem bilinearGraph_maximum :
    IsGreatest (envelopeValues (bilinearGraph I) (halfPoint I))
      (((Fintype.card I).choose 2 : ℝ) / 2) := by
  have h := positive_polynomial_maximum_general (bilinearSupports I) (fun _ => (1 : ℝ))
    (fun _ _ => zero_le_one) (halfPoint I) halfPoint_mem_cube
  have hterm : ∀ s ∈ bilinearSupports I, (1 : ℝ) * monomialUpper s (halfPoint I) = 1 / 2 := by
    intro s hs
    have hcard := mem_bilinearSupports.mp hs
    obtain ⟨i, hi⟩ : s.Nonempty := Finset.card_pos.mp (by omega)
    rw [one_mul, monomialUpper_eq_anchor s _ i hi (fun j _ => le_rfl)]
    rfl
  rw [Finset.sum_congr rfl hterm, Finset.sum_const, bilinearSupports_card,
    nsmul_eq_mul] at h
  simpa [bilinearGraph, div_eq_mul_inv] using h

/-- Exact convex lower bound: every law with the prescribed means has at least
`C(m, 2)` expected successful pairs, by the tangent line to `k ↦ C(k, 2)`. -/
private theorem bilinearGraph_expect_lower (m : ℕ) (μ : Law (Vertex (Fin (2 * m))))
    (hmean : HasMeans μ (halfPoint (Fin (2 * m)))) :
    ((m.choose 2 : ℕ) : ℝ) ≤ μ.expect (fun v => bilinearGraph (Fin (2 * m)) (vertexPoint v)) := by
  have hcount : μ.expect (fun v => (count v : ℝ)) = (m : ℝ) := by
    have hfun : (fun v : Vertex (Fin (2 * m)) => (count v : ℝ)) =
        fun v => ∑ i, vertexPoint v i := by
      funext v
      exact (sum_binary v).symm
    rw [hfun, Law.expect_sum]
    have : ∀ i : Fin (2 * m), μ.expect (fun v => vertexPoint v i) = 1 / 2 := by
      intro i
      exact hmean i
    rw [Finset.sum_congr rfl fun i _ => this i, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul]
    push_cast
    ring
  have hpt : ∀ v : Vertex (Fin (2 * m)),
      (((m : ℝ) ^ 2 - m) / 2 + ((m : ℝ) - 1 / 2) * ((count v : ℝ) - m)) ≤
        bilinearGraph (Fin (2 * m)) (vertexPoint v) := by
    intro v
    rw [bilinearGraph_vertex, Nat.cast_choose_two]
    nlinarith [sq_nonneg ((count v : ℝ) - m)]
  have hlin : μ.expect (fun v =>
      ((m : ℝ) ^ 2 - m) / 2 + ((m : ℝ) - 1 / 2) * ((count v : ℝ) - m)) =
      ((m : ℝ) ^ 2 - m) / 2 := by
    rw [Law.expect_add, Law.expect_const, Law.expect_const_mul, Law.expect_sub,
      Law.expect_const, hcount]
    ring
  calc ((m.choose 2 : ℕ) : ℝ) = ((m : ℝ) ^ 2 - m) / 2 := by
        rw [Nat.cast_choose_two]; ring
    _ = μ.expect (fun v =>
          ((m : ℝ) ^ 2 - m) / 2 + ((m : ℝ) - 1 / 2) * ((count v : ℝ) - m)) := hlin.symm
    _ ≤ _ := μ.expect_mono hpt

/-- The balanced attaining law: the uniform rotation of the vertex whose first
`m` coordinates succeed. Every coordinate mean is one half and every vertex in
its support has exactly `m` successes, hence exactly `C(m, 2)` successful pairs. -/
private theorem bilinearGraph_lower_attaining_law (m : ℕ) (hm : 0 < m) :
    ∃ μ : Law (Vertex (Fin (2 * m))), HasMeans μ (halfPoint (Fin (2 * m))) ∧
      μ.expect (fun v => bilinearGraph (Fin (2 * m)) (vertexPoint v)) =
        ((m.choose 2 : ℕ) : ℝ) := by
  have : NeZero (2 * m) := ⟨by omega⟩
  have : Nonempty (Fin (2 * m)) := ⟨⟨0, by omega⟩⟩
  have hcount : count (prefixVertex (2 * m) m) = m :=
    count_prefixVertex (2 * m) m (by omega)
  refine ⟨(Law.uniform (Fin (2 * m))).map
    (fun s => rotate (prefixVertex (2 * m) m) s), ?_, ?_⟩
  · intro i
    rw [Law.expect_map, Law.expect_uniform]
    have h' : (∑ s, (vertexPoint (rotate (prefixVertex (2 * m) m) s) i : ℝ)) = (m : ℝ) := by
      have h := sum_rotate (prefixVertex (2 * m) m) i
      rw [hcount] at h
      simpa only [vertexPoint] using h
    have hmpos : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm
    change (∑ s, (vertexPoint (rotate (prefixVertex (2 * m) m) s) i : ℝ)) /
      (Fintype.card (Fin (2 * m)) : ℝ) = halfPoint (Fin (2 * m)) i
    rw [h', Fintype.card_fin]
    change (m : ℝ) / ((2 * m : ℕ) : ℝ) = 1 / 2
    push_cast
    rw [div_eq_div_iff (by linarith) (by norm_num : (2 : ℝ) ≠ 0)]
    ring
  · rw [Law.expect_map, Law.expect_uniform]
    have hval : ∀ s : Fin (2 * m),
        bilinearGraph (Fin (2 * m)) (vertexPoint (rotate (prefixVertex (2 * m) m) s)) =
          ((m.choose 2 : ℕ) : ℝ) := by
      intro s
      rw [bilinearGraph_vertex, count_rotate, hcount]
    change (∑ s, bilinearGraph (Fin (2 * m))
      (vertexPoint (rotate (prefixVertex (2 * m) m) s))) /
        (Fintype.card (Fin (2 * m)) : ℝ) = ((m.choose 2 : ℕ) : ℝ)
    rw [Finset.sum_congr rfl fun s _ => hval s, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul]
    have h2m : ((2 * m : ℕ) : ℝ) ≠ 0 := by
      have : (0 : ℕ) < 2 * m := by omega
      exact_mod_cast this.ne'
    field_simp

/-- The exact convex value at the half point. -/
theorem bilinearGraph_minimum (m : ℕ) (hm : 0 < m) :
    IsLeast (envelopeValues (bilinearGraph (Fin (2 * m))) (halfPoint (Fin (2 * m))))
      ((m.choose 2 : ℕ) : ℝ) :=
  minimum_from_laws _ separatelyAffine_bilinearGraph _ _
    (fun μ hmean => bilinearGraph_expect_lower m μ hmean)
    (bilinearGraph_lower_attaining_law m hm)

/-- The exact cube hull gap of the complete bilinear graph in `2 * m` variables. -/
theorem bilinearGraph_hullGap (m : ℕ) (hm : 0 < m) :
    hullGap (bilinearGraph (Fin (2 * m))) (halfPoint (Fin (2 * m))) = (m : ℝ) ^ 2 / 2 := by
  rw [hullGap, (bilinearGraph_maximum (I := Fin (2 * m))).csSup_eq,
    (bilinearGraph_minimum m hm).csInf_eq, Fintype.card_fin, Nat.cast_choose_two,
    Nat.cast_choose_two]
  push_cast
  ring

/-- Each pair contributes exactly one half to the termwise relaxation. -/
theorem bilinearGraph_term_hullGap (s : Finset I) (hs : s.card = 2) :
    hullGap (monomial s) (halfPoint I) = 1 / 2 := by
  obtain ⟨i, hi⟩ : s.Nonempty := Finset.card_pos.mp (by omega)
  rw [monomial_hullGap_of_min_coordinate s (halfPoint I) halfPoint_mem_cube i hi
    (fun j _ => le_rfl)]
  have hsum : (∑ j ∈ s, halfPoint I j) = 1 := by
    simp only [halfPoint]
    rw [Finset.sum_const, hs, nsmul_eq_mul]
    norm_num
  rw [hsum, hs]
  norm_num [halfPoint]

/-- The exact cube termwise gap of the complete bilinear graph. -/
theorem bilinearGraph_termwiseGap (m : ℕ) :
    weightedTermwiseGap (bilinearSupports (Fin (2 * m))) (fun _ => 1)
        (halfPoint (Fin (2 * m))) = (m : ℝ) * (2 * m - 1) / 2 := by
  unfold weightedTermwiseGap
  have hterm : ∀ s ∈ bilinearSupports (Fin (2 * m)),
      (1 : ℝ) * hullGap (monomial s) (halfPoint (Fin (2 * m))) = 1 / 2 := by
    intro s hs
    rw [one_mul, bilinearGraph_term_hullGap s (mem_bilinearSupports.mp hs)]
  rw [Finset.sum_congr rfl hterm, Finset.sum_const, bilinearSupports_card,
    Fintype.card_fin, nsmul_eq_mul, Nat.cast_choose_two]
  push_cast
  ring

/-- PB44 on the unit cube: the exact termwise-to-hull ratio of the complete
positive bilinear graph in `n = 2 * m` variables at the half point is
`2 * (n - 1) / n`. -/
theorem bilinearGraph_cube_ratio (m : ℕ) (hm : 0 < m) :
    weightedTermwiseGap (bilinearSupports (Fin (2 * m))) (fun _ => 1)
          (halfPoint (Fin (2 * m))) /
        hullGap (bilinearGraph (Fin (2 * m))) (halfPoint (Fin (2 * m))) =
      2 * ((2 * m : ℝ) - 1) / (2 * m) := by
  have hmpos : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm
  have h1 : (0 : ℝ) < (m : ℝ) ^ 2 / 2 := div_pos (pow_pos hmpos 2) two_pos
  have h2 : (0 : ℝ) < 2 * (m : ℝ) := by linarith
  rw [bilinearGraph_termwiseGap m, bilinearGraph_hullGap m hm,
    div_eq_div_iff h1.ne' h2.ne']
  ring

/-! ## The odd dimensions: the ratio `2 * n / (n + 1)`

At `n = 2 * m + 1` the mean success count `n / 2 = m + 1 / 2` is a half integer,
so no law with the prescribed means can be supported on a single count. The
convex envelope is the chord value of the adjacent-count law
(`exists_adjacentLaw`) at the two counts `m` and `m + 1`, namely
`(1 / 2) * C(m, 2) + (1 / 2) * C(m + 1, 2) = m ^ 2 / 2`, and the lower bound for
every law is the discrete convexity of `k ↦ C(k, 2)` (`convex_count_expect_lower`).
The concave value is the same common-threshold value `C(n, 2) / 2` as in the even
case, so the hull gap is `m * (m + 1) / 2` against a termwise gap
`m * (2 * m + 1) / 2`. For `m > 0`, division gives the ratio
`(2 * m + 1) / (m + 1) = 2 * n / (n + 1)`. At `m = 0` both gaps are zero.
-/

omit [DecidableEq I] in
/-- At the half point the expected success count is half the dimension. -/
theorem meanSum_halfPoint :
    meanSum (Finset.univ : Finset I) (halfPoint I) = (Fintype.card I : ℝ) / 2 := by
  rw [meanSum]
  simp only [halfPoint]
  rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  ring

/-- In an odd dimension the lower adjacent count at the half point is `m`. -/
theorem countFloor_halfPoint_odd (m : ℕ) :
    countFloor (Finset.univ : Finset (Fin (2 * m + 1))) (halfPoint (Fin (2 * m + 1))) = m := by
  have hmean : meanSum (Finset.univ : Finset (Fin (2 * m + 1))) (halfPoint (Fin (2 * m + 1)))
      = (m : ℝ) + 1 / 2 := by
    rw [meanSum_halfPoint, Fintype.card_fin]
    push_cast
    ring
  refine (Nat.floor_eq_iff ?_).mpr ⟨?_, ?_⟩
  · rw [hmean]; positivity
  · rw [hmean]; linarith
  · rw [hmean]; linarith

/-- In an odd dimension the upper adjacent count at the half point carries weight
one half. -/
theorem countFrac_halfPoint_odd (m : ℕ) :
    countFrac (Finset.univ : Finset (Fin (2 * m + 1))) (halfPoint (Fin (2 * m + 1))) = 1 / 2 := by
  rw [countFrac, countFloor_halfPoint_odd, meanSum_halfPoint, Fintype.card_fin]
  push_cast
  ring

/-- The pair count `k ↦ C(k, 2)` is discretely convex: its successive
differences are `0, 1, 2, ...`. -/
private theorem choose_two_convex (k : ℕ) :
    (((k + 1).choose 2 : ℕ) : ℝ) - ((k.choose 2 : ℕ) : ℝ) ≤
      (((k + 2).choose 2 : ℕ) : ℝ) - (((k + 1).choose 2 : ℕ) : ℝ) := by
  simp only [Nat.cast_choose_two]
  push_cast
  linarith

/-- The exact convex value at the half point of an odd dimension. The mean
success count `m + 1 / 2` is a half integer, so the adjacent-count law splits its
mass evenly between `m` and `m + 1` successes and the value is
`(1 / 2) * C(m, 2) + (1 / 2) * C(m + 1, 2) = m ^ 2 / 2`. -/
theorem bilinearGraph_minimum_odd (m : ℕ) :
    IsLeast (envelopeValues (bilinearGraph (Fin (2 * m + 1))) (halfPoint (Fin (2 * m + 1))))
      ((m : ℝ) ^ 2 / 2) := by
  have hfun : (fun v : Vertex (Fin (2 * m + 1)) =>
      bilinearGraph (Fin (2 * m + 1)) (vertexPoint v)) =
      fun v => (((countOn Finset.univ v).choose 2 : ℕ) : ℝ) := by
    funext v
    rw [bilinearGraph_vertex, countOn_univ]
  have hchord : (1 - countFrac (Finset.univ : Finset (Fin (2 * m + 1)))
          (halfPoint (Fin (2 * m + 1)))) *
        (((countFloor (Finset.univ : Finset (Fin (2 * m + 1)))
          (halfPoint (Fin (2 * m + 1)))).choose 2 : ℕ) : ℝ) +
      countFrac (Finset.univ : Finset (Fin (2 * m + 1))) (halfPoint (Fin (2 * m + 1))) *
        (((countFloor (Finset.univ : Finset (Fin (2 * m + 1)))
          (halfPoint (Fin (2 * m + 1))) + 1).choose 2 : ℕ) : ℝ) = (m : ℝ) ^ 2 / 2 := by
    rw [countFloor_halfPoint_odd, countFrac_halfPoint_odd]
    simp only [Nat.cast_choose_two]
    push_cast
    ring
  refine minimum_from_laws _ separatelyAffine_bilinearGraph _ _ ?_ ?_
  · intro μ hmean
    rw [hfun, ← hchord]
    exact convex_count_expect_lower (fun k => ((k.choose 2 : ℕ) : ℝ)) choose_two_convex
      Finset.univ _ μ hmean
  · obtain ⟨μ, hmean, hval⟩ := exists_adjacentLaw (Finset.univ : Finset (Fin (2 * m + 1)))
      (halfPoint (Fin (2 * m + 1))) halfPoint_mem_cube
    exact ⟨μ, hmean, by rw [hfun, hval (fun k => ((k.choose 2 : ℕ) : ℝ)), hchord]⟩

/-- The exact cube hull gap of the complete bilinear graph in `2 * m + 1`
variables: the concave value `C(2 * m + 1, 2) / 2` against the convex value
`m ^ 2 / 2`. -/
theorem bilinearGraph_hullGap_odd (m : ℕ) :
    hullGap (bilinearGraph (Fin (2 * m + 1))) (halfPoint (Fin (2 * m + 1))) =
      (m : ℝ) * ((m : ℝ) + 1) / 2 := by
  rw [hullGap, (bilinearGraph_maximum (I := Fin (2 * m + 1))).csSup_eq,
    (bilinearGraph_minimum_odd m).csInf_eq, Fintype.card_fin, Nat.cast_choose_two]
  push_cast
  ring

/-- The exact cube termwise gap of the complete bilinear graph in `2 * m + 1`
variables: each of the `C(2 * m + 1, 2)` pairs contributes one half. -/
theorem bilinearGraph_termwiseGap_odd (m : ℕ) :
    weightedTermwiseGap (bilinearSupports (Fin (2 * m + 1))) (fun _ => 1)
        (halfPoint (Fin (2 * m + 1))) = (m : ℝ) * (2 * (m : ℝ) + 1) / 2 := by
  unfold weightedTermwiseGap
  have hterm : ∀ s ∈ bilinearSupports (Fin (2 * m + 1)),
      (1 : ℝ) * hullGap (monomial s) (halfPoint (Fin (2 * m + 1))) = 1 / 2 := by
    intro s hs
    rw [one_mul, bilinearGraph_term_hullGap s (mem_bilinearSupports.mp hs)]
  rw [Finset.sum_congr rfl hterm, Finset.sum_const, bilinearSupports_card,
    Fintype.card_fin, nsmul_eq_mul, Nat.cast_choose_two]
  push_cast
  ring

/-- PB44 in odd dimension: the exact termwise-to-hull ratio of the complete
positive bilinear graph in `n = 2 * m + 1` variables at the half point is
`2 * n / (n + 1)`, not the even-dimensional value `2 * (n - 1) / n`. -/
theorem bilinearGraph_cube_ratio_odd (m : ℕ) (hm : 0 < m) :
    weightedTermwiseGap (bilinearSupports (Fin (2 * m + 1))) (fun _ => 1)
          (halfPoint (Fin (2 * m + 1))) /
        hullGap (bilinearGraph (Fin (2 * m + 1))) (halfPoint (Fin (2 * m + 1))) =
      2 * ((2 * m : ℝ) + 1) / ((2 * m : ℝ) + 1 + 1) := by
  have hmpos : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm
  have h1 : (0 : ℝ) < (m : ℝ) * ((m : ℝ) + 1) / 2 := by positivity
  have h2 : (0 : ℝ) < (2 * m : ℝ) + 1 + 1 := by linarith
  rw [bilinearGraph_termwiseGap_odd m, bilinearGraph_hullGap_odd m,
    div_eq_div_iff h1.ne' h2.ne']
  ring

/-- At every odd dimension `n = 2 * m + 1` with `m ≥ 1` the exact ratio is
*different* from the even-dimensional expression `2 * (n - 1) / n`: the two
values `(2 * m + 1) / (m + 1)` and `4 * m / (2 * m + 1)` never agree, since
`(2 * m + 1) ^ 2 = 4 * m * (m + 1) + 1`. -/
theorem bilinearGraph_cube_ratio_odd_ne (m : ℕ) (hm : 0 < m) :
    weightedTermwiseGap (bilinearSupports (Fin (2 * m + 1))) (fun _ => 1)
          (halfPoint (Fin (2 * m + 1))) /
        hullGap (bilinearGraph (Fin (2 * m + 1))) (halfPoint (Fin (2 * m + 1))) ≠
      2 * ((2 * m : ℝ) + 1 - 1) / ((2 * m : ℝ) + 1) := by
  have hmpos : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm
  rw [bilinearGraph_cube_ratio_odd m hm]
  intro h
  rw [div_eq_div_iff (by linarith) (by linarith)] at h
  nlinarith

/-! ## PB44: the lower bound two for `C_box(rho)` -/

omit [Fintype I] [DecidableEq I] in
/-- The half point of the cube is carried to the centre of `[1, rho]^n`. -/
theorem boxPoint_halfPoint (rho : ℝ) :
    boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (halfPoint I) = fun _ => (1 + rho) / 2 := by
  funext i
  change (1 : ℝ) + (rho - 1) * (1 / 2) = (1 + rho) / 2
  ring

/-- The complete bilinear graph scaled to `[1, rho]^n` still has ratio
`2 * (n - 1) / n`, so that value is a ratio of the common-aspect class. -/
theorem bilinearGraph_mem_commonAspectBoxRatios (m : ℕ) (hm : 0 < m) {rho : ℝ}
    (hrho : 1 < rho) :
    2 * ((2 * m : ℝ) - 1) / (2 * m) ∈ commonAspectBoxRatios rho := by
  have hS : ∀ s ∈ bilinearSupports (Fin (2 * m)), s.card = 2 :=
    fun s hs => mem_bilinearSupports.mp hs
  have hp : halfPoint (Fin (2 * m)) ∈ cube (Fin (2 * m)) := halfPoint_mem_cube
  have hgap : boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho)
      (supportPolynomial (bilinearSupports (Fin (2 * m))) (fun _ => 1))
      (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (halfPoint (Fin (2 * m)))) =
        (rho - 1) ^ 2 * ((m : ℝ) ^ 2 / 2) := by
    rw [boxHullGap_bilinear rho hrho.le _ (fun _ => 1) hS _ hp]
    exact congrArg _ (bilinearGraph_hullGap m hm)
  refine ⟨Fin (2 * m), inferInstance, inferInstance, bilinearSupports (Fin (2 * m)),
    (fun _ => 1), boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (halfPoint (Fin (2 * m))),
    fun _ _ => zero_le_one,
    boxPoint_mem _ _ _ (fun _ => hrho.le) hp, ?_, ?_⟩
  · rw [hgap]
    have h1 : (0 : ℝ) < (rho - 1) ^ 2 := by positivity
    have h2 : (0 : ℝ) < (m : ℝ) ^ 2 / 2 := by
      have : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm
      positivity
    exact mul_pos h1 h2
  · rw [bilinearGraph_box_ratio_eq rho hrho _ (fun _ => 1) hS _ hp]
    exact (bilinearGraph_cube_ratio m hm).symm

/-- The same ratio belongs to the general strictly positive aspect class. -/
theorem bilinearGraph_mem_boxAspectRatios (m : ℕ) (hm : 0 < m) {rho : ℝ} (hrho : 1 < rho) :
    2 * ((2 * m : ℝ) - 1) / (2 * m) ∈ boxAspectRatios rho :=
  commonAspectBoxRatios_subset_boxAspectRatios hrho.le
    (bilinearGraph_mem_commonAspectBoxRatios m hm hrho)

/-- The exact ratios `2 * (n - 1) / n` tend to two along the even dimensions. -/
theorem bilinearGraph_ratio_tendsto :
    Tendsto (fun m : ℕ => 2 * ((2 * m : ℝ) - 1) / (2 * m)) atTop (𝓝 2) := by
  have h2 : Tendsto (fun m : ℕ => 2 - 1 / (m : ℝ)) atTop (𝓝 2) := by
    simpa using (tendsto_one_div_atTop_nhds_zero_nat (𝕜 := ℝ)).const_sub 2
  refine h2.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with m hm
  have hmpos : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm
  have hm0 : (m : ℝ) ≠ 0 := hmpos.ne'
  have h2 : (0 : ℝ) < 2 * (m : ℝ) := by linarith
  have key : (1 / (m : ℝ)) * (2 * (m : ℝ)) = 2 := by field_simp
  rw [eq_div_iff h2.ne', sub_mul, key]
  ring

/-- PB44 without any boundedness hypothesis: every upper bound of the strictly
positive aspect-ratio class is at least two. -/
theorem two_le_of_forall_mem_boxAspectRatios {rho U : ℝ} (hrho : 1 < rho)
    (hU : ∀ r ∈ boxAspectRatios rho, r ≤ U) : 2 ≤ U := by
  refine le_of_tendsto bilinearGraph_ratio_tendsto ?_
  filter_upwards [eventually_gt_atTop 0] with m hm
  exact hU _ (bilinearGraph_mem_boxAspectRatios m hm hrho)

/-- The same statement for the common-aspect class on `[1, rho]^n`. -/
theorem two_le_of_forall_mem_commonAspectBoxRatios {rho U : ℝ} (hrho : 1 < rho)
    (hU : ∀ r ∈ commonAspectBoxRatios rho, r ≤ U) : 2 ≤ U := by
  refine le_of_tendsto bilinearGraph_ratio_tendsto ?_
  filter_upwards [eventually_gt_atTop 0] with m hm
  exact hU _ (bilinearGraph_mem_commonAspectBoxRatios m hm hrho)

/-- PB44: `2 ≤ C_box(rho)` for every `rho > 1`, under the explicit boundedness
hypothesis that the supremum needs. -/
theorem two_le_boxAspectSupremum {rho : ℝ} (hrho : 1 < rho)
    (hbdd : BddAbove (boxAspectRatios rho)) : 2 ≤ boxAspectSupremum rho :=
  two_le_of_forall_mem_boxAspectRatios hrho fun _ hr => le_csSup hbdd hr

/-- The common-aspect supremum on `[1, rho]^n` is at least two as well. -/
theorem two_le_commonAspectBoxSupremum {rho : ℝ} (hrho : 1 < rho)
    (hbdd : BddAbove (commonAspectBoxRatios rho)) : 2 ≤ commonAspectBoxSupremum rho :=
  two_le_of_forall_mem_commonAspectBoxRatios hrho fun _ hr => le_csSup hbdd hr

end
end MultilinearGap
