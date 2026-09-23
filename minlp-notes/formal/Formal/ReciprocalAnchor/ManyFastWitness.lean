import Formal.ReciprocalAnchor.ManyFastLaw
import Formal.ReciprocalAnchor.ManyFastLawSize
import Formal.ReciprocalAnchor.ManyRationalProducer
import Formal.ReciprocalAnchor.ManyRationalCandidate
import Formal.ReciprocalAnchor.ManyWitnessLists

/-! Complete executable rational graph-witness construction from original candidate data. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators
open FastEnvelope

structure WitnessOutput (n K : ℕ) where
  mass : Vector ℚ K
  location : Vector ℚ K
  inverse : Vector ℚ K
  products : Vector (Option (List ℚ)) n
  leaves : Vector (Option (List ℚ) × ℕ) n
  work : ℕ

/-- The fast envelope is executed once. Mixed arrays are materialized before leaf
selection, so every selector reads stored rational values. The charge for mixed
array generation permits recomputing the base reciprocal in each array entry.
The last charge covers recovering reciprocal and product graph coordinates. -/
def fastWitnessOutput {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    WitnessOutput n ((fastLaw m q w).length + 2) :=
  let source := sourceLines m q w
  let built := buildAtoms source
  let atoms := built.1
  let p : Fin atoms.length → ℚ := fun i => (atoms.get i).mass
  let x : Fin atoms.length → ℚ := fun i => (atoms.get i).location
  let mass := Vector.ofFn (mixedMass p x a b m t)
  let location := Vector.ofFn (mixedLocation x a b)
  let leaves := Vector.ofFn (fun j => rationalSelectorCounted mass.get location.get (q j) (w j))
  { mass := mass
    location := location
    inverse := location.map (fun x => 1 / x)
    products := Vector.ofFn (fun j => (leaves.get j).1.map
      (fun ys => List.zipWith (· * ·) location.toList ys))
    leaves := leaves
    work := built.2 + 6 * source.length + 40 * (atoms.length + 3) ^ 2 +
      (∑ j, (leaves.get j).2) + 3 * (n + 1) * (atoms.length + 2) }

theorem fastWitnessOutput_mass {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ)
    (i : Fin ((fastLaw m q w).length + 2)) :
    (fastWitnessOutput a b m t q w).mass.get i =
      mixedMass (fastLawMass m q w) (fastLawLocation m q w) a b m t i := by
  exact Vector.get_ofFn _ _

theorem fastWitnessOutput_location {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ)
    (i : Fin ((fastLaw m q w).length + 2)) :
    (fastWitnessOutput a b m t q w).location.get i =
      mixedLocation (fastLawLocation m q w) a b i := by
  exact Vector.get_ofFn _ _

theorem fastWitnessOutput_leaf {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) (j : Fin n) :
    (fastWitnessOutput a b m t q w).leaves.get j =
      rationalWitnessProducer (fastLawMass m q w) (fastLawLocation m q w) a b m t q w j := by
  have hv {K : ℕ} (f : Fin K → ℚ) : (Vector.ofFn f).get = f := funext (Vector.get_ofFn f)
  simp only [fastWitnessOutput, Vector.get_ofFn, hv]
  rfl

/-- This charge includes envelope construction, rational interpolation, materialized
mixed arrays, all actual leaf searches, and recovery of the graph coordinates. -/
theorem fastWitnessOutput_polynomial_work {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) :
    (fastWitnessOutput a b m t q w).work ≤
      (2 * n + 2) * ((2 * n + 2).log2 + 37) +
      (40 + 64 * n) * (2 * n + 4) ^ 2 + 3 * (n + 1) * (2 * n + 3) := by
  have hcost := fastLaw_cost m q w
  have hsize := fastLaw_length m q w
  have hleaf := rationalWitnessProducer_cost (fastLawMass m q w) (fastLawLocation m q w)
    a b m t q w
  have he : (∑ j, ((fastWitnessOutput a b m t q w).leaves.get j).2) =
      ∑ j, (rationalWitnessProducer (fastLawMass m q w) (fastLawLocation m q w)
        a b m t q w j).2 := by simp only [fastWitnessOutput_leaf]
  have hw : (fastWitnessOutput a b m t q w).work =
      (buildAtoms (sourceLines m q w)).2 + 6 * (2 * n + 2) +
      40 * ((fastLaw m q w).length + 3) ^ 2 +
      (∑ j, ((fastWitnessOutput a b m t q w).leaves.get j).2) +
      3 * (n + 1) * ((fastLaw m q w).length + 2) := by
    simp only [fastWitnessOutput, sourceLines, List.length_ofFn, fastLaw]
  rw [hw, he]
  have hs : ((fastLaw m q w).length + 3) ^ 2 ≤ (2 * n + 4) ^ 2 :=
    Nat.pow_le_pow_left (by omega) 2
  have hlin := Nat.mul_le_mul_left (3 * (n + 1)) (show
    (fastLaw m q w).length + 2 ≤ 2 * n + 3 by omega)
  nlinarith [Nat.mul_le_mul_left (64 * n) hs, Nat.mul_le_mul_left 40 hs]

/-- Every feasible rational candidate is accepted by the actual finite witness producer. -/
theorem fastWitnessOutput_spec {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a < b)
    (hlin : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)))
    (hlo : lowerMoment a b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ≤ (t : ℝ))
    (hhi : t ≤ rationalSecant a b m)
    (haB : RationalBits a B) (hbB : RationalBits b B)
    (hmB : RationalBits m B) (htB : RationalBits t B)
    (hqB : ∀ j, RationalBits (q j) B) (hwB : ∀ j, RationalBits (w j) B) :
    let out := fastWitnessOutput a b m t q w
    ∃ θ : Fin n → Fin ((fastLaw m q w).length + 2) → ℚ,
      (∀ i, 0 ≤ out.mass.get i) ∧ (∑ i, out.mass.get i = 1) ∧
      (∀ i, a ≤ out.location.get i ∧ out.location.get i ≤ b) ∧
      (∑ i, out.mass.get i * out.location.get i = m) ∧
      (∑ i, out.mass.get i / out.location.get i = t) ∧
      (∀ i, RationalBits (out.mass.get i) (mixedAtomBits n B) ∧
        RationalBits (out.location.get i) (mixedAtomBits n B)) ∧
      ∀ j, (out.leaves.get j).1 = some (List.ofFn (θ j)) ∧
        (∀ i, θ j i ∈ Set.Icc (0 : ℚ) 1) ∧
        (∑ i, out.mass.get i * θ j i = q j) ∧
        (∑ i, out.mass.get i * out.location.get i * θ j i = w j) ∧
        ∀ i, RationalBits (θ j i)
          (witnessBits ((fastLaw m q w).length + 2) (mixedAtomBits n B)) := by
  let p := fastLawMass m q w
  let x := fastLawLocation m q w
  have hp : ∀ i, 0 ≤ p i := fun i => (fastLawMass_pos m q w i).le
  have hp1 := fastLawMass_total hlin
  have hx := fastLawLocation_bounds hlin
  have hm := fastLawLocation_mean hlin
  have hsize := fastLaw_length m q w
  have hmab : a ≤ m ∧ m ≤ b := by exact_mod_cast And.intro hlin.1 hlin.2.1
  have hT : (∑ i, p i / x i) ≤ t := by
    have he := fastLawAsLaw_reciprocal hlin ha
    change (∑ i, (p i : ℝ) / (x i : ℝ)) = _ at he
    have hh := he.trans_le hlo
    exact_mod_cast hh
  have hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1 := by
    intro j
    have hh : (0 : ℝ) ≤ (q j : ℝ) ∧ (q j : ℝ) ≤ 1 :=
      ⟨(hlin.2.2 j).1, (hlin.2.2 j).2.1⟩
    exact_mod_cast hh
  have hcall : ∀ j s, w j - q j * s ≤ selectionCall p x s ∧
      m - w j - (1 - q j) * s ≤ selectionCall p x s := by
    intro j s
    have he := fastLawAsLaw_call hlin (s : ℝ)
    change (∑ i, (p i : ℝ) * max ((x i : ℝ) - (s : ℝ)) 0) = _ at he
    have hc : ((selectionCall p x s : ℚ) : ℝ) =
        envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) (s : ℝ) := by
      simpa only [selectionCall, Rat.cast_sum, Rat.cast_mul, Rat.cast_max, Rat.cast_sub,
        Rat.cast_zero] using he
    have h₁ := leaf_le_envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) (s : ℝ) j
    have h₀ := complement_le_envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) (s : ℝ) j
    rw [← hc] at h₁ h₀
    exact_mod_cast And.intro h₁ h₀
  have hbits : ∀ i, RationalBits (p i) (atomBits B) ∧ RationalBits (x i) (atomBits B) := by
    intro i
    have hh := buildAtoms_bits hmB hqB hwB ((fastLaw m q w).get_mem i)
    refine ⟨rationalBits_mono hh.1 (by unfold atomBits; omega), ?_⟩
    convert hh.2 using 1 <;> first | rfl | unfold atomBits; omega
  have hBA : B ≤ mixInputBits n B := by unfold mixInputBits; omega
  have hAA : atomBits B ≤ mixInputBits n B := by unfold mixInputBits; omega
  have hTB : RationalBits (∑ i, p i / x i) (mixInputBits n B) := by
    apply rationalBits_mono (reciprocal_sum_bits p x (fun i => (hbits i).1) (fun i => (hbits i).2))
    simp only [Fintype.card_fin]
    unfold mixInputBits
    nlinarith
  have hpB : ∀ i, RationalBits (mixedMass p x a b m t i) (mixedAtomBits n B) := by
    intro i
    exact rationalMixMass_bits p (fun i => rationalBits_mono (hbits i).1 hAA)
      (rationalBits_mono haB hBA) (rationalBits_mono hbB hBA)
      (rationalBits_mono hmB hBA) (rationalBits_mono htB hBA) hTB _
  have hxB : ∀ i, RationalBits (mixedLocation x a b i) (mixedAtomBits n B) := by
    intro i
    exact rationalBits_mono (rationalMixLocation_bits x
      (fun i => rationalBits_mono (hbits i).2 hAA)
      (rationalBits_mono haB hBA) (rationalBits_mono hbB hBA) _) (by unfold mixedAtomBits; omega)
  have hBD : B ≤ mixedAtomBits n B := by unfold mixedAtomBits; omega
  obtain ⟨θ, hθ⟩ := rationalWitnessProducer_spec p x q w hp hp1 hx hm ha hab hmab hT hhi hq hcall
    hpB hxB (fun j => rationalBits_mono (hqB j) hBD) (fun j => rationalBits_mono (hwB j) hBD)
  have hmix := mixedLaw_spec p x hp hp1 hx hm ha hab hmab hT hhi
  refine ⟨θ, ?_⟩
  simpa only [fastWitnessOutput_mass, fastWitnessOutput_location, fastWitnessOutput_leaf] using
    And.intro hmix.1 (And.intro hmix.2.1 (And.intro hmix.2.2.1
      (And.intro hmix.2.2.2.1 (And.intro hmix.2.2.2.2 (And.intro
        (fun i => And.intro (hpB i) (hxB i)) hθ)))))

theorem fastWitnessOutput_inverse {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ)
    (i : Fin ((fastLaw m q w).length + 2)) :
    (fastWitnessOutput a b m t q w).inverse.get i =
      1 / (fastWitnessOutput a b m t q w).location.get i := by
  exact Vector.get_map _ _ _

theorem fastWitnessOutput_products {n : ℕ} (a b m t : ℚ) (q w : Fin n → ℚ) (j : Fin n)
    (θ : Fin ((fastLaw m q w).length + 2) → ℚ)
    (he : ((fastWitnessOutput a b m t q w).leaves.get j).1 = some (List.ofFn θ)) :
    (fastWitnessOutput a b m t q w).products.get j =
      some (List.ofFn (fun i => (fastWitnessOutput a b m t q w).location.get i * θ i)) := by
  change (Vector.ofFn (fun j => ((fastWitnessOutput a b m t q w).leaves.get j).1.map
    (fun ys => List.zipWith (· * ·) (fastWitnessOutput a b m t q w).location.toList ys))).get j = _
  rw [Vector.get_ofFn, he, Option.map_some]
  have hv : (fastWitnessOutput a b m t q w).location.toList =
      List.ofFn (fastWitnessOutput a b m t q w).location.get := by
    rw [← Vector.toList_ofFn]
    congr 1
    exact Vector.ofFn_getElem.symm
  rw [hv, zipWith_mul_ofFn]

/-- The materialized output lists are coordinates of a rational graph decomposition;
all fractions in the emitted graph atoms obey one polynomial input-size bound. -/
theorem fastWitnessOutput_complete {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a < b)
    (hlin : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)))
    (hlo : lowerMoment a b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ≤ (t : ℝ))
    (hhi : t ≤ rationalSecant a b m)
    (haB : RationalBits a B) (hbB : RationalBits b B)
    (hmB : RationalBits m B) (htB : RationalBits t B)
    (hqB : ∀ j, RationalBits (q j) B) (hwB : ∀ j, RationalBits (w j) B) :
    let out := fastWitnessOutput a b m t q w
    ∃ θ : Fin n → Fin ((fastLaw m q w).length + 2) → ℚ,
      point (m : ℝ) (t : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ∈
        hull n (a : ℝ) (b : ℝ) ∧
      (∀ j, (out.leaves.get j).1 = some (List.ofFn (θ j)) ∧
        out.products.get j = some (List.ofFn (fun i => out.location.get i * θ j i))) ∧
      ∀ i, RationalBits (out.mass.get i) (candidateBits n B) ∧
        RationalBits (out.location.get i) (candidateBits n B) ∧
        RationalBits (out.inverse.get i) (candidateBits n B) ∧
        ∀ j, RationalBits (θ j i) (candidateBits n B) ∧
          RationalBits (out.location.get i * θ j i) (candidateBits n B) := by
  obtain ⟨θ, hp, hp1, hx, hm, ht, hbits, hθ⟩ :=
    fastWitnessOutput_spec ha hab hlin hlo hhi haB hbB hmB htB hqB hwB
  refine ⟨θ, ?_, ?_, ?_⟩
  · apply rational_representation_mem_hull
      (fastWitnessOutput a b m t q w).mass.get
      (fastWitnessOutput a b m t q w).location.get (fun i j => θ j i)
      hp hp1 hx (fun i j => (hθ j).2.1 i) hm ht
      (fun j => (hθ j).2.2.1)
    intro j
    simpa only [mul_assoc] using (hθ j).2.2.2.1
  · intro j
    exact ⟨(hθ j).1, fastWitnessOutput_products a b m t q w j (θ j) (hθ j).1⟩
  · intro i
    have hlow : mixedAtomBits n B ≤ candidateBits n B := by unfold candidateBits; omega
    refine ⟨rationalBits_mono (hbits i).1 hlow,
      rationalBits_mono (hbits i).2 hlow, ?_, ?_⟩
    · rw [fastWitnessOutput_inverse]
      simpa only [one_div] using rationalBits_mono (rationalBits_inv (hbits i).2) hlow
    · intro j
      have hy := (hθ j).2.2.2.2 i
      have hn : (fastLaw m q w).length + 2 ≤ 2 * n + 3 := by
        have hh := fastLaw_length m q w
        omega
      have hy' := rationalBits_mono hy (witnessBits_mono (B := mixedAtomBits n B) hn)
      exact ⟨rationalBits_mono hy' (by unfold candidateBits; omega),
        rationalBits_mul (hbits i).2 hy'⟩

end ReciprocalAnchor.ManyLeaf
