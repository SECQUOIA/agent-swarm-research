import Formal.DAGSpectral.AlgorithmBitCost
import Formal.DAGSpectral.ProfileSpectralDP

namespace DAGSpectral
open ReciprocalAnchor

/-- A deliberately loose polynomial bit bound for graph-size integers. -/
theorem rationalBits_nat (n : ℕ) : RationalBits (n:ℚ) (n+1) := by
  simp only [RationalBits,Rat.num_natCast,Rat.den_natCast,Int.natAbs_natCast]
  constructor
  · exact n.lt_two_pow_self.trans_le (Nat.pow_le_pow_right (by decide) (by omega))
  · exact Nat.one_lt_pow (by omega) (by decide)

def rationalMesh (η : ℚ) (r N : ℕ) : ℚ := η/((r:ℚ) * N)

theorem rationalMesh_bits {η : ℚ} {B : ℕ} (hη : RationalBits η B) (r N : ℕ) :
    RationalBits (rationalMesh η r N) (B+r+N+2) := by
  have h := rationalBits_div hη (rationalBits_mul (rationalBits_nat r) (rationalBits_nat N))
  simpa [rationalMesh,Nat.add_assoc,Nat.add_left_comm,Nat.add_comm] using h

theorem rationalMesh_cast (η : ℚ) (r N : ℕ) :
    (rationalMesh η r N : ℝ) = spectralMesh (η:ℝ) r N := by
  simp [rationalMesh,spectralMesh]

namespace ExplicitDAG
variable {v m : ℕ} {κ : Type*} [Fintype κ]

/-- An explicit polynomial in graph size, state capacity, and operand bits. -/
def dpWorkPolynomial (v m d r B S : ℕ) : ℕ :=
  v * (1+m * S) ^ 2 * keyWorkBound v m d r B +
    (v * (m+1)+v * v) * (v+m+1)^2 + m * S * (v+1) * (m+1) + v * S * (r+1) * (v+1) * (m+1)

theorem dpWorkPolynomial_mono {v m d r r' B B' S S' : ℕ}
    (hr : r ≤ r') (hB : B ≤ B') (hS : S ≤ S') :
    dpWorkPolynomial v m d r B S ≤ dpWorkPolynomial v m d r' B' S' := by
  unfold dpWorkPolynomial keyWorkBound
  gcongr

theorem dpBitWork_capacity_bound (G : ExplicitDAG v m) (allowed : Fin m → Bool) (s : Fin v)
    (required : Finset (Fin m)) (label : Fin m → κ → ℤ) {B r S : ℕ}
    (hl : ∀ e i, IntegerBits (label e i) B) (window : Finset ℤ)
    (hw : ∀ t es, G.AllowedPath allowed s t es → ∀ i, profile label es i ∈ window)
    (hr : required.card ≤ r) (hS : 2 ^ required.card * window.card ^ Fintype.card κ ≤ S) :
    dpBitWork G allowed s required label ≤ dpWorkPolynomial v m (Fintype.card κ) r B S := by
  exact (dpBitWork_window_bound G allowed s required label hl window hw).trans
    (dpWorkPolynomial_mono hr le_rfl hS)

/-- Recomputed label functions may have a nonzero source cost. The number of
calls is bounded from the actual representative-comparison scan. -/
theorem uncachedDPBitWork_capacity_bound (G : ExplicitDAG v m) (allowed : Fin m → Bool)
    (s : Fin v) (required : Finset (Fin m)) (label : Fin m → κ → ℤ) {B r S : ℕ}
    (hl : ∀ e i, IntegerBits (label e i) B) (window : Finset ℤ)
    (hw : ∀ t es, G.AllowedPath allowed s t es → ∀ i, profile label es i ∈ window)
    (hr : required.card ≤ r) (hS : 2 ^ required.card * window.card ^ Fintype.card κ ≤ S)
    (sourceLabelCost : ℕ) :
    uncachedDPBitWork G allowed s required label sourceLabelCost ≤
      dpWorkPolynomial v m (Fintype.card κ) r B S +
        (v * (1+m*S)^2) * (2*v*Fintype.card κ) * sourceLabelCost := by
  have hd := dpBitWork_capacity_bound G allowed s required label hl window hw hr hS
  have hc : comparisonBudget G allowed s required label ≤ v*(1+m*S)^2 :=
    (comparisonBudget_bound G allowed s required label window hw).trans (by gcongr)
  have hlc := (labelAccessCount_le G allowed s required label).trans
    (Nat.mul_le_mul_right _ hc)
  unfold uncachedDPBitWork
  exact Nat.add_le_add hd (Nat.mul_le_mul_right _ hlc)

/-- The DP part for actual rational floor labels, with no assumed label width
or assumed finite state window. Normalized retained entries supply the only
numerical magnitude premise. -/
theorem spectral_rational_dpBitWork (G : ExplicitDAG v m) (allowed : Fin m → Bool)
    (s : Fin v) (required : Finset (Fin m)) (a : Fin m → κ → ℚ)
    (p r N F E : ℕ) (η : ℚ) (haBits : ∀ e i, RationalBits (a e i) F)
    (hηBits : RationalBits η E) (hr : 0 < r) (hN : 0 < N) (hη : 0 < η)
    (hv : v - 1 ≤ N) (hreq : required.card ≤ r)
    (ha : ∀ e, allowed e = true → ∀ i, |(a e i : ℝ)| ≤ 4 * p) :
    dpBitWork G allowed s required (fun e i => ⌊a e i/rationalMesh η r N⌋) ≤
      dpWorkPolynomial v m (Fintype.card κ) r (F+(E+r+N+2)+1)
        (2 ^ r * (8 * p * r * N ^ 2 * ⌈1/(η:ℝ)⌉₊+N+2) ^ Fintype.card κ) := by
  let label : Fin m → κ → ℤ := fun e i => ⌊a e i/rationalMesh η r N⌋
  have heq : label = spectralLabels (fun e i => (a e i : ℝ)) (η:ℝ) r N := by
    funext e i
    simp only [label,spectralLabels,← rationalMesh_cast]
    exact (floorLabel_ratCast _ _).symm
  have hηR : (0:ℝ) < η := by exact_mod_cast hη
  let window := coordinateRange p N (spectralMesh (η:ℝ) r N)
  have hw : ∀ t es, G.AllowedPath allowed s t es → ∀ i, profile label es i ∈ window := by
    intro t es hp i
    rw [heq]
    exact allowed_profile_window G allowed s t _ p r N (η:ℝ) hr hN hηR hv ha hp i
  have hcap := spectral_state_capacity (κ := κ) required p r N (η:ℝ) hr hN hηR hreq
  have hc := coordinateCount_le_polynomial p r N (η:ℝ)
  apply dpBitWork_capacity_bound G allowed s required label
    (rational_floor_labels_bits haBits (rationalMesh_bits hηBits r N)) window hw hreq
  exact hcap.trans (Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hc _))

/-- Rational division and floor work for every edge coordinate is polynomial in
input bits and graph size. It is paid before the integer DP. -/
theorem spectral_labelPreprocessingBitWork {a : Fin m → κ → ℚ} {η : ℚ} {F E : ℕ}
    (haBits : ∀ e i, RationalBits (a e i) F) (hηBits : RationalBits η E) (r N : ℕ) :
    labelPreprocessingBitWork a (rationalMesh η r N) F (E+r+N+2) ≤
      m * Fintype.card κ * (268 * (F+E+r+N+3) ^ 3) := by
  simpa [Nat.add_assoc] using
    labelPreprocessingBitWork_le haBits (rationalMesh_bits hηBits r N)

end ExplicitDAG
end DAGSpectral
