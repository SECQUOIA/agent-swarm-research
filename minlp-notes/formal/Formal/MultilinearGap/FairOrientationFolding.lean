import Formal.MultilinearGap.BalancedOrientation
import Formal.MultilinearGap.OrientationMoments

/-! # The literal fair endpoint-orientation law, and why folding is lossless

This file closes the last gap in obligation PB07 of topic 18
(`topics/18-positive-box/CLAIMS.md`): *the fair endpoint-orientation law — one
uniform variable plus `n` independent fair coins — has the prescribed means,
and its moments `O_j` are well defined.*

`CubicGap.orientationLaw` is a **folded** model of that experiment: the fair
coin is absorbed into the conditional success probability
`CubicGap.orientationProbability`, and the uniform variable is folded at one
half.  All of `O_j = orientMoment` and everything downstream of it is proved
against the folded model.  Here the literal model is built and the two are
proved equal, so the folded computations are computations about the literal
experiment.

## The literal law

`fairSubsets I` is the uniform law on **all** `2^n` subsets of the coordinates:
`n` independent fair coins, the coin of coordinate `i` deciding whether `i` is
oriented low or high.  `fairOrientationLaw x` mixes
`MultilinearGap.orientedLaw H x` — one shared uniform variable on `[0,1]`,
coordinate `i` succeeding on `[0, x i]` when `i ∈ H` and on `(1 - x i, 1]` when
`i ∉ H` — over that coin law.  So `fairOrientationLaw` is exactly "one uniform
variable plus `n` independent fair coins", with no folding anywhere.

## The two ingredients

* **Conditional independence survives averaging the coins.**
  `fairOrientationLaw_weight` computes the mixture weight as a single
  integrated Bernoulli product with the *unfolded* conditional success
  probability `fairCoinProb x t = ([t ≤ x] + [1 - x < t]) / 2`.  The coins
  factor out of the subset sum because the product over coordinates depends on
  `H` only coordinatewise (`sum_prod_ite_mem`).

* **Folding is measure preserving.**  `foldUnit u = min (2u) (2(1-u))` pushes
  Lebesgue measure on `[0,1]` forward to Lebesgue measure on `[0,1]`, so
  `intervalIntegral_comp_foldUnit` gives `∫₀¹ g (foldUnit u) du = ∫₀¹ g t dt`
  for every `g` that is interval integrable on `[0,1]`.

`fairCoinProb x t = orientationProbability x (foldUnit t)` holds **off the two
points `t = x` and `t = 1 - x`** (`fairCoinProb_eq_orientationProbability`),
and genuinely fails at them
(`fairCoinProb_ne_orientationProbability_foldUnit` exhibits `x = 1/4`,
`t = 3/4`, where the values are `0` and `1/2`).  The exceptional set of the
whole vector `x` is contained in `range x ∪ range (1 - x ·)`, which is finite
because the coordinate type is a `Fintype`, hence Lebesgue null; the integrals
are therefore compared with `intervalIntegral.integral_congr_ae`, not
pointwise.

## The conclusion

`fairOrientationLaw_eq_orientationLaw` is the headline:
`fairOrientationLaw x = CubicGap.orientationLaw x` as laws on `Vertex I`, for
**every** `x : I → ℝ` — no cube hypothesis is needed, because the folding
identity and the change of variables hold for arbitrary real coordinates.
`fairOrientationLaw_hasMeans` and `binomMoment_fairOrientationLaw` then
transfer PB07's two assertions, and every existing downstream result about
`orientMoment`, verbatim, to the literal law.
-/

namespace MultilinearGap

open CubicGap MeasureTheory Set

noncomputable section

/-- The folding map `u ↦ min (2u) (2(1-u))`, which carries the uniform variable
of the literal experiment to the uniform variable of the folded one. -/
def foldUnit (u : ℝ) : ℝ := min (2 * u) (2 * (1 - u))

/-- Below one half the fold is the doubling map. -/
theorem foldUnit_of_le_half {u : ℝ} (hu : u ≤ 1 / 2) : foldUnit u = 2 * u :=
  min_eq_left (by linarith)

/-- Above one half the fold is the reflected doubling map. -/
theorem foldUnit_of_half_le {u : ℝ} (hu : 1 / 2 ≤ u) : foldUnit u = 2 * (1 - u) :=
  min_eq_right (by linarith)

/-- **Folding is measure preserving.**  The fold pushes Lebesgue measure on
`[0,1]` forward to Lebesgue measure on `[0,1]`: each half contributes exactly
half of the integral.  No hypothesis beyond integrability of `g` is needed. -/
theorem intervalIntegral_comp_foldUnit {g : ℝ → ℝ}
    (hg : IntervalIntegrable g volume 0 1) :
    (∫ u in (0 : ℝ)..1, g (foldUnit u)) = ∫ t in (0 : ℝ)..1, g t := by
  have h2 : IntervalIntegrable (fun x => g (2 * x)) volume 0 (1 / 2) := by
    have h := hg.comp_mul_left (c := 2)
    norm_num at h
    exact h
  have h3 : IntervalIntegrable (fun x => g (2 * (1 - x))) volume (1 / 2) 1 := by
    have h := (h2.comp_sub_left 1).symm
    norm_num at h
    exact h
  have hF1 : IntervalIntegrable (fun u => g (foldUnit u)) volume 0 (1 / 2) := by
    refine h2.congr fun u hu => ?_
    rw [Set.uIoc_of_le (by norm_num : (0:ℝ) ≤ 1 / 2)] at hu
    rw [foldUnit_of_le_half hu.2]
  have hF2 : IntervalIntegrable (fun u => g (foldUnit u)) volume (1 / 2) 1 := by
    refine h3.congr fun u hu => ?_
    rw [Set.uIoc_of_le (by norm_num : (1:ℝ) / 2 ≤ 1)] at hu
    rw [foldUnit_of_half_le hu.1.le]
  have hsplit := intervalIntegral.integral_add_adjacent_intervals hF1 hF2
  have e1 : (∫ u in (0:ℝ)..(1/2), g (foldUnit u)) = ∫ u in (0:ℝ)..(1/2), g (2 * u) := by
    refine intervalIntegral.integral_congr fun u hu => ?_
    rw [Set.uIcc_of_le (by norm_num : (0:ℝ) ≤ 1 / 2)] at hu
    rw [foldUnit_of_le_half hu.2]
  have e2 : (∫ u in (1/2 : ℝ)..1, g (foldUnit u)) = ∫ u in (0:ℝ)..(1/2), g (2 * u) := by
    have hc : (∫ u in (1/2 : ℝ)..1, g (foldUnit u)) =
        ∫ u in (1/2 : ℝ)..1, (fun y => g (2 * y)) (1 - u) := by
      refine intervalIntegral.integral_congr fun u hu => ?_
      rw [Set.uIcc_of_le (by norm_num : (1:ℝ) / 2 ≤ 1)] at hu
      rw [foldUnit_of_half_le hu.1]
    rw [hc, intervalIntegral.integral_comp_sub_left (fun y => g (2 * y)) 1]
    norm_num
  have ehalf : (∫ u in (0:ℝ)..(1/2), g (2 * u)) = (∫ t in (0:ℝ)..1, g t) / 2 := by
    rw [intervalIntegral.integral_comp_mul_left g (two_ne_zero),
      show (2:ℝ) * 0 = 0 by ring, show (2:ℝ) * (1/2) = 1 by ring, smul_eq_mul]
    ring
  rw [e1, e2] at hsplit
  rw [← hsplit, ehalf]
  ring

/-- The unfolded conditional success probability of a coordinate with mean `x`,
given the shared uniform value `t` and that coordinate's own fair coin:
`(1/2)([t ≤ x] + [1 - x < t])`.  For `x ≤ 1/2` the two events are disjoint; for
`x > 1/2` they overlap on `(1 - x, x]`, where the probability is one. -/
def fairCoinProb (x t : ℝ) : ℝ :=
  ((if t ≤ x then (1 : ℝ) else 0) + (if 1 - x < t then (1 : ℝ) else 0)) / 2

/-- The fold lies below `2 y` exactly when the point or its reflection lies
below `y`.  This is the only property of the fold used to compare the two
conditional probabilities. -/
theorem foldUnit_le_iff (u y : ℝ) : foldUnit u ≤ 2 * y ↔ (u ≤ y ∨ 1 - y ≤ u) := by
  simp only [foldUnit, min_le_iff]
  constructor
  · rintro (h | h)
    · exact Or.inl (by linarith)
    · exact Or.inr (by linarith)
  · rintro (h | h)
    · exact Or.inl (by linarith)
    · exact Or.inr (by linarith)

/-- **The folding identity.**  The unfolded conditional success probability of
a coordinate with mean `x` at the uniform value `t` agrees with the folded one
at `foldUnit t`, **except possibly at the two points `t = x` and `t = 1 - x`**.
The exclusions are necessary: see
`fairCoinProb_ne_orientationProbability_foldUnit`. -/
theorem fairCoinProb_eq_orientationProbability (x : ℝ) {t : ℝ}
    (ht : t ≠ x) (ht' : t ≠ 1 - x) :
    fairCoinProb x t = orientationProbability x (foldUnit t) := by
  unfold fairCoinProb orientationProbability lowerStep
  by_cases hx : x ≤ 1 / 2
  · rw [if_pos hx]
    by_cases ha : t ≤ x
    · rw [if_pos ha, if_neg (by linarith : ¬ (1 - x < t)),
        if_pos ((foldUnit_le_iff t x).mpr (Or.inl ha))]
      norm_num
    · by_cases hb : 1 - x < t
      · rw [if_neg ha, if_pos hb,
          if_pos ((foldUnit_le_iff t x).mpr (Or.inr hb.le))]
        norm_num
      · have hno : ¬ (foldUnit t ≤ 2 * x) := by
          intro hc
          rcases (foldUnit_le_iff t x).mp hc with h | h
          · exact ha h
          · exact ht' (le_antisymm (not_lt.mp hb) h)
        rw [if_neg ha, if_neg hb, if_neg hno]
        norm_num
  · rw [if_neg hx]
    have hx' : 1 / 2 < x := not_le.mp hx
    have hiff : foldUnit t ≤ 2 * (1 - x) ↔ (t ≤ 1 - x ∨ x ≤ t) := by
      have h := foldUnit_le_iff t (1 - x)
      simpa using h
    by_cases hc : foldUnit t ≤ 2 * (1 - x)
    · rw [if_pos hc]
      rcases hiff.mp hc with h | h
      · rw [if_pos (by linarith : t ≤ x), if_neg (by linarith : ¬ (1 - x < t))]
        norm_num
      · have hlt : x < t := lt_of_le_of_ne h (Ne.symm ht)
        rw [if_neg (by linarith : ¬ (t ≤ x)), if_pos (by linarith : 1 - x < t)]
        norm_num
    · have h1 : ¬ (t ≤ 1 - x) ∧ ¬ (x ≤ t) := by
        constructor <;> intro h <;> exact hc (hiff.mpr (by tauto))
      rw [if_neg hc, if_pos (by linarith [not_le.mp h1.2] : t ≤ x),
        if_pos (by linarith [not_le.mp h1.1] : 1 - x < t)]
      norm_num

/-- The unfolded conditional probability is a probability. -/
theorem fairCoinProb_mem (x t : ℝ) : fairCoinProb x t ∈ Icc (0 : ℝ) 1 := by
  unfold fairCoinProb
  split_ifs <;> norm_num

/-- The unfolded conditional probability is measurable in the uniform
variable. -/
theorem fairCoinProb_measurable (x : ℝ) : Measurable (fairCoinProb x) := by
  unfold fairCoinProb
  exact (((Measurable.ite measurableSet_Iic measurable_const measurable_const).add
    (Measurable.ite measurableSet_Ioi measurable_const measurable_const))).div_const 2

/-- Two finite laws with the same weights are equal. -/
theorem law_eq_of_weight_eq {ι : Type*} [Fintype ι] {μ ν : Law ι}
    (h : ∀ w, μ.weight w = ν.weight w) : μ = ν := by
  cases μ with
  | mk w hn hm =>
    cases ν with
    | mk w' hn' hm' =>
      have hw : w = w' := funext h
      cases hw
      rfl

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- **The `n` independent fair coins.**  The uniform law on all `2 ^ n` subsets
of the coordinates; membership of `i` is the outcome of coordinate `i`'s own
coin, and the coins are independent because the law is a product of `n` fair
bits. -/
def fairSubsets (I : Type*) [Fintype I] [DecidableEq I] : Law (Finset I) where
  weight _ := ((2 : ℝ) ^ Fintype.card I)⁻¹
  nonneg _ := by positivity
  mass_one := by
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_finset, nsmul_eq_mul, Nat.cast_pow]
    norm_num

/-- **PB07, the literal law.**  One uniform variable on `[0,1]` together with
`n` independent fair coins: the uniform mixture over all `2 ^ n` orientation
subsets `H` of the shared-uniform law `orientedLaw H x`. -/
def fairOrientationLaw (x : I → ℝ) : Law (Vertex I) where
  weight v := ∑ H : Finset I, (fairSubsets I).weight H * (orientedLaw H x).weight v
  nonneg v :=
    Finset.sum_nonneg fun H _ =>
      mul_nonneg ((fairSubsets I).nonneg H) ((orientedLaw H x).nonneg v)
  mass_one := by
    have h : ∀ H : Finset I, ∑ v : Vertex I, (orientedLaw H x).weight v = 1 :=
      fun H => (orientedLaw H x).mass_one
    rw [Finset.sum_comm]
    simp only [← Finset.mul_sum, h, mul_one]
    exact (fairSubsets I).mass_one

/-- **The coins factor out.**  Summing a coordinatewise product over all
subsets `H` replaces each coordinate's two-valued choice by the sum of its two
values.  This is the combinatorial form of "conditional on the uniform
variable, the `n` fair coins are independent". -/
theorem sum_prod_ite_mem (a b : I → ℝ) :
    (∑ H : Finset I, ∏ i, (if i ∈ H then a i else b i)) = ∏ i, (a i + b i) := by
  have key : ∀ H : Finset I,
      (∏ i, (if i ∈ H then a i else b i)) = (∏ i ∈ H, a i) * ∏ i ∈ Hᶜ, b i := by
    intro H
    rw [← Finset.prod_mul_prod_compl H (fun i => if i ∈ H then a i else b i)]
    congr 1
    · exact Finset.prod_congr rfl fun i hi => if_pos hi
    · exact Finset.prod_congr rfl fun i hi => if_neg (Finset.mem_compl.mp hi)
  simp_rw [key]
  exact (Fintype.prod_add a b).symm

/-- The weight of an integrated Bernoulli law, spelled out. -/
theorem integratedBernoulli_weight (p : ℝ → I → ℝ) (hp : ∀ t, p t ∈ cube I)
    (hm : ∀ i, Measurable (fun t => p t i)) (v : Vertex I) :
    (integratedBernoulli p hp hm).weight v =
      ∫ t in (0 : ℝ)..1, ∏ i, (if v i then p t i else 1 - p t i) := rfl

/-- **The literal law in conditionally independent form.**  Averaging the `2^n`
orientation patterns turns the mixture into a single integrated Bernoulli law
whose conditional success probabilities are the *unfolded* `fairCoinProb`. -/
theorem fairOrientationLaw_weight (x : I → ℝ) (v : Vertex I) :
    (fairOrientationLaw x).weight v =
      ∫ t in (0 : ℝ)..1,
        ∏ i, (if v i then fairCoinProb (x i) t else 1 - fairCoinProb (x i) t) := by
  change (∑ H : Finset I, ((2:ℝ) ^ Fintype.card I)⁻¹ * (orientedLaw H x).weight v) = _
  have hint : ∀ H : Finset I, IntervalIntegrable
      (fun t => ((2:ℝ) ^ Fintype.card I)⁻¹ *
        ∏ i, (if v i then orientedProb H x t i else 1 - orientedProb H x t i)) volume 0 1 := by
    intro H
    exact (bernoulliLaw_weight_integrable (orientedProb H x) (orientedProb_cube H x)
      (orientedProb_measurable H x) v).const_mul _
  simp only [orientedLaw, integratedBernoulli_weight, ← intervalIntegral.integral_const_mul]
  rw [← intervalIntegral.integral_finsetSum (fun H _ => hint H)]
  refine intervalIntegral.integral_congr fun t _ => ?_
  set a : I → ℝ := fun i => if v i = true then (if t ≤ x i then (1:ℝ) else 0)
    else 1 - (if t ≤ x i then (1:ℝ) else 0) with ha_def
  set b : I → ℝ := fun i => if v i = true then (if 1 - x i < t then (1:ℝ) else 0)
    else 1 - (if 1 - x i < t then (1:ℝ) else 0) with hb_def
  have hsplit : ∀ H : Finset I,
      (∏ i, if v i = true then orientedProb H x t i else 1 - orientedProb H x t i) =
        ∏ i, (if i ∈ H then a i else b i) :=
    fun H => Finset.prod_congr rfl fun i _ => by
      by_cases h : i ∈ H <;> simp [orientedProb, h, ha_def, hb_def]
  rw [← Finset.mul_sum]
  simp_rw [hsplit]
  rw [sum_prod_ite_mem a b]
  have hab : ∀ i : I, a i + b i =
      2 * (if v i = true then fairCoinProb (x i) t else 1 - fairCoinProb (x i) t) := by
    intro i
    simp only [ha_def, hb_def, fairCoinProb]
    by_cases h : v i = true <;> simp [h] <;> ring
  simp_rw [hab]
  rw [Finset.prod_mul_distrib, Finset.prod_const, Finset.card_univ, ← mul_assoc,
    inv_mul_cancel₀ (by positivity : ((2:ℝ) ^ Fintype.card I) ≠ 0), one_mul]

/-- **PB07, the headline.**  The literal fair endpoint-orientation law — one
uniform variable on `[0,1]` together with `n` independent fair coins — is equal
to the folded law `CubicGap.orientationLaw` used throughout topic 18.  Holds
for every `x : I → ℝ`; no cube hypothesis is required. -/
theorem fairOrientationLaw_eq_orientationLaw (x : I → ℝ) :
    fairOrientationLaw x = orientationLaw x := by
  refine law_eq_of_weight_eq fun v => ?_
  set g : ℝ → ℝ := fun s =>
    ∏ i, (if v i = true then orientationProbability (x i) s
      else 1 - orientationProbability (x i) s) with hg_def
  have hg : IntervalIntegrable g volume 0 1 :=
    bernoulliLaw_weight_integrable (fun t i => orientationProbability (x i) t)
      (orientationProbability_cube x) (fun i => orientationProbability_measurable (x i)) v
  have hbad : (Set.range x ∪ Set.range fun i => 1 - x i).Finite :=
    (Set.finite_range x).union (Set.finite_range _)
  have hae : ∀ᵐ t ∂(volume : Measure ℝ), t ∉ (Set.range x ∪ Set.range fun i => 1 - x i) :=
    MeasureTheory.compl_mem_ae_iff.mpr (hbad.measure_zero volume)
  have hcongr : (∫ t in (0:ℝ)..1,
      ∏ i, (if v i = true then fairCoinProb (x i) t else 1 - fairCoinProb (x i) t)) =
      ∫ t in (0:ℝ)..1, g (foldUnit t) := by
    refine intervalIntegral.integral_congr_ae ?_
    filter_upwards [hae] with t ht _
    refine Finset.prod_congr rfl fun i _ => ?_
    have h1 : t ≠ x i := fun h => ht (Or.inl ⟨i, h.symm⟩)
    have h2 : t ≠ 1 - x i := fun h => ht (Or.inr ⟨i, h.symm⟩)
    rw [fairCoinProb_eq_orientationProbability (x i) h1 h2]
  rw [fairOrientationLaw_weight, hcongr, intervalIntegral_comp_foldUnit hg]
  rfl

/-- The folding identity genuinely fails at the excluded endpoints, so the
comparison of the two laws must be made almost everywhere rather than
pointwise.  At `x = 1/4`, `t = 3/4` the unfolded probability is `0` while the
folded one is `1/2`. -/
theorem fairCoinProb_ne_orientationProbability_foldUnit :
    fairCoinProb (1 / 4) (3 / 4) ≠ orientationProbability (1 / 4) (foldUnit (3 / 4)) := by
  norm_num [fairCoinProb, orientationProbability, lowerStep, foldUnit]

/-- Expectations under the literal law are the uniform average, over the `2 ^ n`
orientation patterns, of the shared-uniform conditional expectations. -/
theorem fairOrientationLaw_expect (x : I → ℝ) (f : Vertex I → ℝ) :
    (fairOrientationLaw x).expect f =
      (fairSubsets I).expect fun H => (orientedLaw H x).expect f := by
  simp only [Law.expect, fairOrientationLaw, Finset.sum_mul, Finset.mul_sum, mul_assoc]
  exact Finset.sum_comm

/-- **PB07, the prescribed means.**  The literal fair endpoint-orientation law
has mean `x i` in every coordinate, for every point of the cube. -/
theorem fairOrientationLaw_hasMeans {x : I → ℝ} (hx : x ∈ cube I) :
    HasMeans (fairOrientationLaw x) x := by
  rw [fairOrientationLaw_eq_orientationLaw]
  exact orientationLaw_hasMeans x hx

/-- Monomial moments of the literal law, in integrated product form. -/
theorem fairOrientationLaw_expect_monomial (x : I → ℝ) (s : Finset I) :
    (fairOrientationLaw x).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, monomial s fun i => orientationProbability (x i) t := by
  rw [fairOrientationLaw_eq_orientationLaw]
  exact orientationLaw_expect_monomial x s

/-- **PB07, the moments `O_j`.**  The binomial moments of the literal fair
endpoint-orientation law are exactly the moments `orientMoment` on which every
downstream result of topic 18 is proved, so those results transfer verbatim. -/
theorem binomMoment_fairOrientationLaw (s : Finset I) (x : I → ℝ) (j : ℤ) :
    binomMoment s (fairOrientationLaw x) j = orientMoment s x j := by
  rw [orientMoment, fairOrientationLaw_eq_orientationLaw]

end

end MultilinearGap
