import Formal.ReciprocalAnchor.ManyRationalWitness
import Formal.ReciprocalAnchor.ManyRationalMixCall
import Formal.ReciprocalAnchor.ManyAlgorithmSize
import Formal.ReciprocalAnchor.ManyGeometry

/-! Rational graph witnesses for the complete many-leaf reciprocal hull. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

def atomBits (B : ℕ) : ℕ := 4 * (2 * B + 2) + 2

theorem exists_rational_minimal_law {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a < b)
    (hlin : LinearBounds (a : ℝ) (b : ℝ) (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)))
    (haB : RationalBits a B) (hbB : RationalBits b B) (hmB : RationalBits m B)
    (hqB : ∀ j, RationalBits (q j) B) (hwB : ∀ j, RationalBits (w j) B) :
    ∃ μ : Law (a : ℝ) (b : ℝ), ∃ p x : Fin μ.size → ℚ,
      μ.size ≤ 2 * n + 1 ∧ μ.mean = (m : ℝ) ∧
      μ.call = envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ∧
      μ.reciprocal = lowerMoment a b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ∧
      (∀ i, μ.mass i = (p i : ℝ) ∧ μ.location i = (x i : ℝ)) ∧
      ∀ i, RationalBits (p i) (atomBits B) ∧ RationalBits (x i) (atomBits B) := by
  let c := fun i => (rationalLines m q w i).intercept
  let d := fun i => -(rationalLines m q w i).negSlope
  have hc : ∀ i, (c i : ℝ) = lineIntercept (m : ℝ)
      (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) i := by
    intro i
    simp [c, lineIntercept, ← rationalLines_evalReal, RationalLine.evalReal]
  have hd : ∀ i, (d i : ℝ) = lineSlope (m : ℝ)
      (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) i := by
    intro i
    simp [d, lineSlope, ← rationalLines_evalReal, RationalLine.evalReal]
  have he : affineEnvelope (fun i => (c i : ℝ)) (fun i => (d i : ℝ)) =
      envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) := by
    simp_rw [hc, hd]
    exact (envelope_eq_affineEnvelope _ _ _).symm
  have hleft : ∃ i, d i = -1 := by
    refine ⟨⟨2 * n + 1, by omega⟩, ?_⟩
    apply Rat.cast_injective (α := ℝ)
    rw [hd, lineSlope_neg_one]
    norm_cast
  have hright : ∃ i, d i = 0 := by
    refine ⟨⟨2 * n, by omega⟩, ?_⟩
    apply Rat.cast_injective (α := ℝ)
    rw [hd, lineSlope_zero]
    norm_cast
  obtain ⟨μ, p, x, hsize, hmean, hcall, hatoms, hbits⟩ :=
    exists_bounded_rational_envelope_law c d hab m
      (by intro s hs; rw [he]; exact envelope_left hlin hs)
      (by intro s hs; rw [he]; exact envelope_right hlin hs)
      hleft hright (rationalBits_mono haB (by omega : B ≤ 2 * B + 2))
      (rationalBits_mono hbB (by omega : B ≤ 2 * B + 2))
      (fun i => (rationalLines_bits hmB hqB hwB i).1)
      (fun i => rationalBits_neg (rationalLines_bits hmB hqB hwB i).2)
  rw [he] at hcall
  refine ⟨μ, p, x, ?_, hmean, hcall, ?_, hatoms, hbits⟩
  · simpa using hsize
  · rw [μ.reciprocal_eq_call_integral (by exact_mod_cast ha) (by exact_mod_cast hab.le), hmean]
    rw [hcall]
    rfl

def mixInputBits (n B : ℕ) : ℕ :=
  1 + (2 * n + 1) * (2 * atomBits B + 1) + atomBits B + B

def mixedAtomBits (n B : ℕ) : ℕ := 12 * mixInputBits n B + 6

def candidateBits (n B : ℕ) : ℕ :=
  mixedAtomBits n B + witnessBits (2 * n + 3) (mixedAtomBits n B)

theorem witnessBits_mono {N M B : ℕ} (h : N ≤ M) : witnessBits N B ≤ witnessBits M B := by
  unfold witnessBits interpolationBits momentBits tailBits
  gcongr

/-- Every rational candidate satisfying the complete hull inequalities has at most
`2n+3` rational graph atoms, all with polynomially bounded reduced fractions. -/
theorem rational_candidate_witness {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (ha : 0 < a) (hab : a < b)
    (hlin : LinearBounds (a : ℝ) (b : ℝ) (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)))
    (hlo : lowerMoment a b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ≤ (t : ℝ))
    (hhi : t ≤ rationalSecant a b m)
    (haB : RationalBits a B) (hbB : RationalBits b B)
    (hmB : RationalBits m B) (htB : RationalBits t B)
    (hqB : ∀ j, RationalBits (q j) B) (hwB : ∀ j, RationalBits (w j) B) :
    ∃ K ≤ 2 * n + 1, ∃ p x : Fin K ⊕ Fin 2 → ℚ, ∃ y : (Fin K ⊕ Fin 2) → Fin n → ℚ,
      (∀ i, 0 ≤ p i) ∧ (∑ i, p i = 1) ∧ (∀ i, a ≤ x i ∧ x i ≤ b) ∧
      (∀ i j, 0 ≤ y i j ∧ y i j ≤ 1) ∧ (∑ i, p i * x i = m) ∧
      (∑ i, p i / x i = t) ∧ (∀ j, ∑ i, p i * y i j = q j) ∧
      (∀ j, ∑ i, p i * (x i * y i j) = w j) ∧
      (∀ i, RationalBits (p i) (candidateBits n B) ∧
        RationalBits (x i) (candidateBits n B) ∧
        RationalBits (1 / x i) (candidateBits n B) ∧
        ∀ j, RationalBits (y i j) (candidateBits n B) ∧
          RationalBits (x i * y i j) (candidateBits n B)) := by
  classical
  obtain ⟨μ, p, x, hsize, hmean, hcall, hrec, hatoms, hbits⟩ :=
    exists_rational_minimal_law ha hab hlin haB hbB hmB hqB hwB
  have hpc : ∀ i, (p i : ℝ) = μ.mass i := fun i => (hatoms i).1.symm
  have hxc : ∀ i, (x i : ℝ) = μ.location i := fun i => (hatoms i).2.symm
  have hp : ∀ i, 0 ≤ p i := by
    intro i
    have hh := μ.nonneg i
    rw [← hpc] at hh
    exact_mod_cast hh
  have hp1 : ∑ i, p i = 1 := by
    apply Rat.cast_injective (α := ℝ)
    push_cast
    simpa only [hpc] using μ.total
  have hx : ∀ i, a ≤ x i ∧ x i ≤ b := by
    intro i
    have hh := μ.bounds i
    rw [← hxc] at hh
    exact_mod_cast hh
  have hm : ∑ i, p i * x i = m := by
    apply Rat.cast_injective (α := ℝ)
    push_cast
    simpa only [hpc, hxc, Law.mean] using hmean
  let T := ∑ i, p i / x i
  have hTc : (T : ℝ) = μ.reciprocal := by
    dsimp [T, Law.reciprocal]
    push_cast
    simp only [hpc, hxc]
  have hT : T ≤ t := by
    have hh : (T : ℝ) ≤ (t : ℝ) := by rw [hTc, hrec]; exact hlo
    exact_mod_cast hh
  have hmab : a ≤ m ∧ m ≤ b := by exact_mod_cast And.intro hlin.1 hlin.2.1
  have hbase : ∀ j s, w j - q j * s ≤ selectionCall p x s ∧
      selectionMean p x - w j - (1 - q j) * s ≤ selectionCall p x s := by
    intro j s
    have hcs : ((selectionCall p x s : ℚ) : ℝ) = μ.call (s : ℝ) := by
      simp only [selectionCall, Law.call]
      push_cast
      simp only [hpc, hxc]
    have hms : ((selectionMean p x : ℚ) : ℝ) = (m : ℝ) := by
      unfold selectionMean
      exact_mod_cast hm
    constructor
    · have hh := leaf_le_envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) (s : ℝ) j
      rw [← hcall, ← hcs] at hh
      exact_mod_cast hh
    · have hh := complement_le_envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) (s : ℝ) j
      rw [← hcall, ← hcs, ← hms] at hh
      exact_mod_cast hh
  let p' := rationalMixMass p a b m t T
  let x' := rationalMixLocation x a b
  have hp' := rationalMixMass_nonneg p hp hab hmab hT hhi
  have hp1' := rationalMixMass_total (m := m) (t := t) (T := T) p hp1 hab
  have hx' := rationalMixLocation_bounds x hx hab.le
  have hm' := rationalMix_mean (t := t) (T := T) p x hm hab
  have ht' := rationalMix_reciprocal p x rfl ha hab hT hhi
  have hsel : ∀ j, 0 ≤ q j ∧ q j ≤ 1 ∧ ∀ s,
      w j - q j * s ≤ selectionCall p' x' s ∧
      selectionMean p' x' - w j - (1 - q j) * s ≤ selectionCall p' x' s := by
    intro j
    have hq0 : (0 : ℝ) ≤ (q j : ℝ) := (hlin.2.2 j).1
    have hq1 : (q j : ℝ) ≤ 1 := (hlin.2.2 j).2.1
    refine ⟨by exact_mod_cast hq0, by exact_mod_cast hq1, ?_⟩
    intro s
    have hmono := rational_call_le_mix p x hp hp1 hx hm hab hT hhi s
    have hh := hbase j s
    refine ⟨hh.1.trans hmono, ?_⟩
    have hmeans : selectionMean p' x' = selectionMean p x := hm'.trans hm.symm
    rw [hmeans]
    exact hh.2.trans hmono
  have hBA : B ≤ mixInputBits n B := by unfold mixInputBits; omega
  have hAA : atomBits B ≤ mixInputBits n B := by unfold mixInputBits; omega
  have hTB : RationalBits T (mixInputBits n B) := by
    apply rationalBits_mono (reciprocal_sum_bits p x (fun i => (hbits i).1) (fun i => (hbits i).2))
    simp only [Fintype.card_fin]
    unfold mixInputBits
    nlinarith
  have hpB' : ∀ i, RationalBits (p' i) (mixedAtomBits n B) :=
    rationalMixMass_bits p (fun i => rationalBits_mono (hbits i).1 hAA)
      (rationalBits_mono haB hBA) (rationalBits_mono hbB hBA)
      (rationalBits_mono hmB hBA) (rationalBits_mono htB hBA) hTB
  have hxB' : ∀ i, RationalBits (x' i) (mixedAtomBits n B) := by
    intro i
    apply rationalBits_mono (rationalMixLocation_bits x
      (fun i => rationalBits_mono (hbits i).2 hAA)
      (rationalBits_mono haB hBA) (rationalBits_mono hbB hBA) i)
    unfold mixedAtomBits
    omega
  have hBD : B ≤ mixedAtomBits n B := by unfold mixedAtomBits; omega
  have hyexists := fun j => exists_rational_selection_bounded p' x' hp' hp1' (q j) (w j)
    (hsel j) hpB' hxB' (rationalBits_mono (hqB j) hBD) (rationalBits_mono (hwB j) hBD)
  choose θ hθ hθm hθw hθB using hyexists
  refine ⟨μ.size, hsize, p', x', fun i j => θ j i, hp', hp1', hx', fun i j => hθ j i,
    hm', ht', hθm, ?_, ?_⟩
  · intro j
    simpa only [selectionMoment, mul_assoc] using hθw j
  · intro i
    have hdy : ∀ j, RationalBits (θ j i) (witnessBits (2 * n + 3) (mixedAtomBits n B)) := by
      intro j
      apply rationalBits_mono (hθB j i)
      apply witnessBits_mono
      simp only [Fintype.card_sum, Fintype.card_fin]
      omega
    refine ⟨rationalBits_mono (hpB' i) (by unfold candidateBits; omega),
      rationalBits_mono (hxB' i) (by unfold candidateBits; omega), ?_, ?_⟩
    · simpa only [one_div] using rationalBits_mono (rationalBits_inv (hxB' i))
        (by unfold candidateBits; omega)
    · intro j
      exact ⟨rationalBits_mono (hdy j) (by unfold candidateBits; omega),
        rationalBits_mul (hxB' i) (hdy j)⟩

end ReciprocalAnchor.ManyLeaf
