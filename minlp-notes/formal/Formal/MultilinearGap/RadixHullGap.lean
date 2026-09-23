import Formal.MultilinearGap.RadixTermwise
import Formal.MultilinearGap.RadixIncidence
import Formal.MultilinearGap.BilinearGraph

/-!
# The exact hull gap of the variable-radix family and the lower bound `rho`

This module completes the lower-bound branch of topic 18 for the variable-radix
family of `RadixFamily.lean` and `RadixTermwise.lean` on the strictly positive
box `[eps, 1]`, with `eps = 1 / rho`, `rho > 1`, `L >= 2`, `b = L ^ 2` and
`m = b ^ L`.  Its obligations are PB36, PB38-PB41 and PB43 of
`formal/topics/18-positive-box/CLAIMS.md`, whose source is
`results/positive-multilinear-positive-box-lower.md`.

Writing `H_L = hullTotal b L eps` for the hull gap of the whole family at
`physMeans`, `T_L = termwiseTotal b L eps` for its termwise gap and
`D_L = dCorrection b L eps` for the source's correction:

* **PB36** (`coverage`, `coverage_eq_sum`, `radix_hullGap_isGreatest`).  Equation
  (4): `H_L + D_L` is the **maximum**, over all binary laws with the prescribed
  marginals, of the softened coverage objective
  `(1-eps) ∑_j A_j ∑_{B ∈ P_j} (1 - eps ^ R_B) + eps ∑_j ∑_{B ∈ P_j} (1 - eps ^ R_B)`.
  It is stated as an `IsGreatest`, so the maximum is attained, not merely
  approached.  The proof combines the exact concave value `concaveTotal` of the
  whole family (attained by `thresholdRounding`) with the pointwise identity
  `polynomial_add_coverage`, which trades the polynomial for the coverage
  objective against an affine part, and with the attainment of the lower
  envelope endpoint on the compact graph hull.
* **PB38** (`radix_hullGap_le`).  Equation (5):
  `H_L ≤ eps (1-eps) L + (1-eps) [1 + (L-1)/b] - D_L`, from
  `1 - eps ^ R_B ≤ 1[R_B > 0]` on each block (`blockCoverage_le_hitCount`), from
  `1 - eps ^ r ≤ (1-eps) r` (`one_sub_pow_le_mul`), and from the imported
  unit-box incidence bound `incidence_expect_le_of_means` of
  `RadixIncidence.lean` (PB37, whose upper direction is all that is needed).
* **PB39** (`radix_hullGap_ge`).  Equation (6):
  `H_L ≥ eps (1-eps) L + (1-eps) ^ 2 ∑_j b ^ -j - D_L`, from the law
  `singleFailRounding` of `RadixTermwise.lean`, which fails exactly one
  uniformly random leaf: under it every level contributes exactly `1 - eps`
  deterministically (`blockCoverage_singleFailVertex`).
* **PB40** (`hullTotal_pos`).  `H_L > 0` for every finite `L`, from PB39 and the
  sharper correction bound `dCorrection_le_mul : D_L ≤ eps (1-eps) L`.  **No
  division by a hull gap occurs anywhere before this point.**
* **PB41** (`hullTotal_div_tendsto`, `radix_ratio_tendsto`).  Equation (7):
  `H_L / L → eps (1-eps)` and `T_L / H_L → rho` as `L → ∞`.  Both are stated
  with `rho` bound **outside** the limit: `rho` — hence `eps = 1 / rho`, hence
  the radix `b = L ^ 2` used at stage `L` — is fixed while `L → ∞`.  There is no
  interchange of the `L` and `rho` limits.
* **PB43** (`rho_le_of_forall_mem_commonAspectBoxRatios`,
  `rho_le_of_forall_mem_boxAspectRatios`, `rho_le_boxAspectSupremum`,
  `rho_le_commonAspectBoxSupremum`).  Equation (1): `C_box(rho) ≥ rho` for every
  `rho > 1`.  The PB42 rescaling from `[1/rho, 1]` to `[1, rho]` is the
  pointwise identity `boxPoint_eps_eq`, which scales every physical variable by
  `rho`; a degree-`d` term acquires the positive coefficient `rho ^ -d`
  (`scaledCoeff`).  The whole family is carried to *exactly the same function*
  of the cube parameters, so its hull gap is unchanged
  (`hullTotal_eq_boxHullGap`), while each single monomial is multiplied by the
  positive constant `eps ^ d`, whose gap is rescaled by the mean-exact splitting
  `hullGap_of_meanExact_split` of `BilinearGraph.lean`
  (`boxHullGap_monomial_eps`).  The conclusions use the `BddAbove`-free forms
  that `BilinearGraph.lean` established for the bound two, together with the
  `BddAbove`-hypothesis supremum form.
-/

namespace MultilinearGap
namespace Radix

noncomputable section
open scoped BigOperators
open CubicGap Filter Topology

/-! ## A scalar inequality -/

/-- The geometric bound `1 - eps ^ k ≤ (1 - eps) k` of the source, used both for
the blockwise estimate of PB38 and for the correction bound of PB40. -/
theorem one_sub_pow_le_mul (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) (k : ℕ) :
    1 - eps ^ k ≤ (1 - eps) * (k : ℝ) := by
  cases k with
  | zero => simp
  | succ n =>
      have h := geom_chord eps h0 h1 (s := 1) (k := n + 1) (by omega)
      simp only [Nat.cast_one, one_mul, pow_one] at h
      linarith

/-! ## The softened coverage objective of equation (4) -/

/-- The softened coverage of the level-`j` blocks at a binary assignment:
`∑_{B ∈ P_j} (1 - eps ^ R_B)`, where `R_B` is the number of failed leaves of the
block `B`. -/
def blockCoverage (b L : ℕ) (eps : ℝ) (j : Fin L) (v : Vertex (Coord b L)) : ℝ :=
  ∑ c, (1 - eps ^ blockFails b L j c v)

/-- The source's coverage objective of equation (4):
`(1-eps) ∑_j A_j ∑_{B ∈ P_j} (1 - eps ^ R_B) + eps ∑_j ∑_{B ∈ P_j} (1 - eps ^ R_B)`. -/
def coverage (b L : ℕ) (eps : ℝ) (v : Vertex (Coord b L)) : ℝ :=
  (1 - eps) * ∑ j : Fin L, vertexPoint v (Sum.inl j) * blockCoverage b L eps j v
    + eps * ∑ j : Fin L, blockCoverage b L eps j v

/-- The coverage objective collected level by level. -/
theorem coverage_eq_sum (b L : ℕ) (eps : ℝ) (v : Vertex (Coord b L)) :
    coverage b L eps v =
      ∑ j : Fin L, (eps + (1 - eps) * vertexPoint v (Sum.inl j)) * blockCoverage b L eps j v := by
  rw [coverage, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl fun j _ => by ring

/-- The vertex value of one whole level: the physical anchor factor times the
uncovered part of the level. -/
theorem sum_blocks_physVertex (b L : ℕ) (eps : ℝ) (j : Fin L) (v : Vertex (Coord b L)) :
    ∑ c, eps ^ failCount (support b L j c) v =
      (eps + (1 - eps) * vertexPoint v (Sum.inl j)) *
        ((blockCount b L j : ℝ) - blockCoverage b L eps j v) := by
  have hanchor : eps ^ anchorFail b L j v = eps + (1 - eps) * vertexPoint v (Sum.inl j) := by
    rw [anchorFail]
    cases hv : v (Sum.inl j) <;> simp [vertexPoint, hv]
  have hsplit : ∀ c : Fin (blockCount b L j), eps ^ failCount (support b L j c) v
      = eps ^ anchorFail b L j v * eps ^ blockFails b L j c v := by
    intro c
    rw [failCount_support, pow_add]
  rw [Finset.sum_congr rfl fun c _ => hsplit c, ← Finset.mul_sum, hanchor]
  congr 1
  rw [blockCoverage, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, mul_one]
  ring

/-- **PB36, the pointwise half.** At every binary assignment the family
polynomial on `[eps, 1]` and the coverage objective add up to an affine function
of the anchors. -/
theorem polynomial_add_coverage (b L : ℕ) (eps : ℝ) (v : Vertex (Coord b L)) :
    polynomial b L (boxPoint (epsLower b L eps) (epsUpper b L) (vertexPoint v))
        + coverage b L eps v =
      ∑ j : Fin L, (blockCount b L j : ℝ) * (eps + (1 - eps) * vertexPoint v (Sum.inl j)) := by
  rw [polynomial_physVertex, coverage_eq_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [sum_blocks_physVertex]
  ring

/-! ## The affine and concave totals -/

/-- The law-independent affine total `∑_j |P_j| (eps + (1-eps) u_j)` of the
pointwise identity, evaluated at the prescribed marginals. -/
def affineTotal (b L : ℕ) (eps : ℝ) : ℝ :=
  eps * ∑ j : Fin L, (blockCount b L j : ℝ) + (1 - eps) * (L : ℝ)

/-- The exact concave value of the whole family: the sum of the exact concave
values of its terms, which one law attains simultaneously. -/
def concaveTotal (b L : ℕ) (eps : ℝ) : ℝ :=
  ∑ j : Fin L, (blockCount b L j : ℝ) * termConcave b L eps j

/-- The level-`j` block count priced against the leaf count is the reciprocal
block size. -/
theorem blockCount_div_pow (b L : ℕ) (hb : 0 < b) (j : Fin L) :
    (blockCount b L j : ℝ) / (b : ℝ) ^ L = 1 / (blockSize b L j : ℝ) := by
  have hmul : (blockCount b L j : ℝ) * (blockSize b L j : ℝ) = (b : ℝ) ^ L := by
    exact_mod_cast congrArg (fun n : ℕ => (n : ℝ)) (blockCount_mul_blockSize b L j)
  have hc : (0 : ℝ) < (blockCount b L j : ℝ) := by
    exact_mod_cast pow_pos hb (j.val + 1)
  have hs : (0 : ℝ) < (blockSize b L j : ℝ) := by
    exact_mod_cast pow_pos hb (L - (j.val + 1))
  rw [← hmul]
  field_simp

/-- The affine total exceeds the concave total by exactly the source's
correction `D_L`. -/
theorem affineTotal_sub_concaveTotal (b L : ℕ) (hb : 0 < b) (eps : ℝ) :
    affineTotal b L eps - concaveTotal b L eps = dCorrection b L eps := by
  have hterm : ∀ j : Fin L, (blockCount b L j : ℝ) * termConcave b L eps j
      = eps * (blockCount b L j : ℝ) + (1 - eps)
        - eps * ((1 - eps ^ blockSize b L j) / (blockSize b L j : ℝ)) := by
    intro j
    have hc : (0 : ℝ) < (blockCount b L j : ℝ) := by
      exact_mod_cast pow_pos hb (j.val + 1)
    have hs : (0 : ℝ) < (blockSize b L j : ℝ) := by
      exact_mod_cast pow_pos hb (L - (j.val + 1))
    have hmul : (blockCount b L j : ℝ) * (blockSize b L j : ℝ) = (b : ℝ) ^ L := by
      exact_mod_cast congrArg (fun n : ℕ => (n : ℝ)) (blockCount_mul_blockSize b L j)
    rw [termConcave, ← hmul]
    field_simp
  rw [concaveTotal, Finset.sum_congr rfl fun j _ => hterm j, Finset.sum_sub_distrib,
    Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    nsmul_eq_mul, ← Finset.mul_sum, ← Finset.mul_sum, sum_blockSize_reflect,
    affineTotal, dCorrection]
  ring

/-! ## The exact concave value of the whole family -/

/-- The expectation of the family polynomial splits into its terms. -/
theorem expect_polynomial_eq (b L : ℕ) (eps : ℝ) (μ : Law (Vertex (Coord b L))) :
    μ.expect (fun v => polynomial b L
        (boxPoint (epsLower b L eps) (epsUpper b L) (vertexPoint v))) =
      ∑ j, ∑ c, μ.expect (fun v => eps ^ failCount (support b L j c) v) := by
  simp only [polynomial_physVertex]
  rw [Law.expect_sum]
  exact Finset.sum_congr rfl fun j _ => Law.expect_sum _ _

/-- The exact concave-envelope value of the whole family on `[eps, 1]`: common
threshold rounding attains every term's concave value simultaneously. -/
theorem family_concave_envelope (b L : ℕ) (hb : 2 ≤ b) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) :
    IsGreatest (boxEnvelopeValues (epsLower b L eps) (epsUpper b L) (polynomial b L)
      (physMeans b L eps)) (concaveTotal b L eps) := by
  have hb0 : 0 < b := by omega
  rw [physMeans, boxEnvelopeValues_eq_of_mem _ _ (epsLower_le_epsUpper b L h1) _ _
    (means_mem_cube b L hb0)]
  refine maximum_from_laws _ (polynomial_boxPoint_separatelyAffine b L hb0 eps) _ _ ?_ ?_
  · intro μ hμ
    rw [expect_polynomial_eq]
    refine le_trans (Finset.sum_le_sum fun j _ =>
      Finset.sum_le_sum fun c _ => expect_term_le b L hb0 eps h0 h1 μ hμ j c) ?_
    refine le_of_eq (Finset.sum_congr rfl fun j _ => ?_)
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  · refine ⟨thresholdRounding b L hb0, thresholdRounding_hasMeans b L hb0, ?_⟩
    rw [expect_polynomial_eq, concaveTotal]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [Finset.sum_congr rfl fun c _ =>
      thresholdRounding_expect b L hb0 eps j c (blockSize_succ_le b L hb j),
      Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]

/-! ## The hull gap of the whole family, and PB36 -/

/-- The exact hull gap `H_L` of the whole variable-radix family on `[eps, 1]` at
the prescribed physical means. -/
def hullTotal (b L : ℕ) (eps : ℝ) : ℝ :=
  boxHullGap (epsLower b L eps) (epsUpper b L) (polynomial b L) (physMeans b L eps)

/-- The feasible values of the maximization in equation (4): the coverage
expectations over all binary laws with the prescribed marginals. -/
def coverageValues (b L : ℕ) (eps : ℝ) : Set ℝ :=
  {y | ∃ μ : Law (Vertex (Coord b L)), HasMeans μ (means b L) ∧ y = μ.expect (coverage b L eps)}

/-- The expectation of the family polynomial is the affine total minus the
expected coverage. -/
theorem expect_polynomial_coverage (b L : ℕ) (hb : 0 < b) (eps : ℝ)
    (μ : Law (Vertex (Coord b L))) (hμ : HasMeans μ (means b L)) :
    μ.expect (fun v => polynomial b L
        (boxPoint (epsLower b L eps) (epsUpper b L) (vertexPoint v))) =
      affineTotal b L eps - μ.expect (coverage b L eps) := by
  have hpt : (fun v => polynomial b L
      (boxPoint (epsLower b L eps) (epsUpper b L) (vertexPoint v)))
      = fun v => (∑ j : Fin L, (blockCount b L j : ℝ)
          * (eps + (1 - eps) * vertexPoint v (Sum.inl j))) - coverage b L eps v := by
    funext v
    have := polynomial_add_coverage b L eps v
    linarith
  have haff : μ.expect (fun v => ∑ j : Fin L, (blockCount b L j : ℝ)
      * (eps + (1 - eps) * vertexPoint v (Sum.inl j))) = affineTotal b L eps := by
    rw [Law.expect_sum]
    have hj : ∀ j : Fin L, μ.expect (fun v => (blockCount b L j : ℝ)
        * (eps + (1 - eps) * vertexPoint v (Sum.inl j)))
        = eps * (blockCount b L j : ℝ) + (1 - eps) := by
      intro j
      have hc : (0 : ℝ) < (blockCount b L j : ℝ) := by
        exact_mod_cast pow_pos hb (j.val + 1)
      have hm : means b L (Sum.inl j) = 1 / (blockCount b L j : ℝ) := rfl
      rw [Law.expect_const_mul, Law.expect_add, Law.expect_const, Law.expect_const_mul,
        hμ (Sum.inl j), hm]
      field_simp
    rw [Finset.sum_congr rfl fun j _ => hj j, Finset.sum_add_distrib, Finset.sum_const,
      Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, ← Finset.mul_sum, affineTotal]
    ring
  rw [hpt, Law.expect_sub, haff]

/-- Membership in the envelope of the whole family is exactly a coverage value,
reflected in the affine total. -/
theorem mem_boxEnvelopeValues_iff (b L : ℕ) (hb : 0 < b) (eps : ℝ) (h1 : eps ≤ 1) (z : ℝ) :
    z ∈ boxEnvelopeValues (epsLower b L eps) (epsUpper b L) (polynomial b L)
        (physMeans b L eps) ↔
      ∃ μ : Law (Vertex (Coord b L)), HasMeans μ (means b L) ∧
        z = affineTotal b L eps - μ.expect (coverage b L eps) := by
  rw [physMeans, boxEnvelopeValues_eq_of_mem _ _ (epsLower_le_epsUpper b L h1) _ _
    (means_mem_cube b L hb)]
  constructor
  · intro hz
    obtain ⟨μ, hmean, hval⟩ := (mem_cubeGraph_hull_iff _
      (polynomial_boxPoint_separatelyAffine b L hb eps) (means b L) z).mp hz
    exact ⟨μ, hmean, by rw [← hval, expect_polynomial_coverage b L hb eps μ hmean]⟩
  · rintro ⟨μ, hmean, rfl⟩
    exact (mem_cubeGraph_hull_iff _ (polynomial_boxPoint_separatelyAffine b L hb eps)
      (means b L) _).mpr ⟨μ, hmean, expect_polynomial_coverage b L hb eps μ hmean⟩

/-- **PB36.** Equation (4): `H_L + D_L` is the exact **maximum** of the softened
coverage objective over all binary laws with the prescribed marginals. -/
theorem radix_hullGap_isGreatest (b L : ℕ) (hb : 2 ≤ b) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) :
    IsGreatest (coverageValues b L eps) (hullTotal b L eps + dCorrection b L eps) := by
  have hb0 : 0 < b := by omega
  set E := boxEnvelopeValues (epsLower b L eps) (epsUpper b L) (polynomial b L)
    (physMeans b L eps) with hE
  have hends := boxEnvelopeValues_endpoints (epsLower b L eps) (epsUpper b L)
    (epsLower_le_epsUpper b L h1) (polynomial b L) (polynomial_separatelyAffine b L)
    (physMeans b L eps) (physMeans_mem_box b L (by omega) h1)
  have hsup : sSup E = concaveTotal b L eps :=
    (family_concave_envelope b L hb eps h0 h1).csSup_eq
  have hgap : hullTotal b L eps = sSup E - sInf E := rfl
  have hval : affineTotal b L eps - sInf E = hullTotal b L eps + dCorrection b L eps := by
    rw [← affineTotal_sub_concaveTotal b L hb0 eps, hgap, hsup]
    ring
  constructor
  · obtain ⟨μ, hmean, hz⟩ := (mem_boxEnvelopeValues_iff b L hb0 eps h1 (sInf E)).mp hends.1.1
    exact ⟨μ, hmean, by rw [← hval, hz]; ring⟩
  · rintro y ⟨μ, hmean, rfl⟩
    have hmem : affineTotal b L eps - μ.expect (coverage b L eps) ∈ E :=
      (mem_boxEnvelopeValues_iff b L hb0 eps h1 _).mpr ⟨μ, hmean, rfl⟩
    have hle := hends.1.2 hmem
    linarith [hval]

/-! ## PB38: the hull-gap upper bound -/

/-- A block is hit exactly when it has a failed leaf. -/
theorem blockFails_pos_iff (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j))
    (v : Vertex (Coord b L)) :
    0 < blockFails b L j c v ↔ ∃ i ∈ block b L j c, v (Sum.inr i) = false := by
  rw [blockFails, Finset.card_pos]
  constructor
  · rintro ⟨i, hi⟩
    rw [Finset.mem_filter] at hi
    exact ⟨i, hi.1, hi.2⟩
  · rintro ⟨i, hi, hv⟩
    exact ⟨i, Finset.mem_filter.mpr ⟨hi, hv⟩⟩

/-- `N_j` counts the level-`j` blocks with a positive failed-leaf count. -/
theorem hitCount_eq_card_filter_pos (b L : ℕ) (j : Fin L) (v : Vertex (Coord b L)) :
    (Finset.univ.filter
        fun c : Fin (blockCount b L j) => 0 < blockFails b L j c v).card
      = hitCount b L j v := by
  rw [hitCount_eq_card_filter]
  congr 1
  exact Finset.filter_congr fun c _ => by simpa using blockFails_pos_iff b L j c v

/-- The blockwise bound `1 - eps ^ R_B ≤ 1[R_B > 0]` of the source, summed: the
level-`j` coverage never exceeds the incidence count `N_j`. -/
theorem blockCoverage_le_hitCount (b L : ℕ) (eps : ℝ) (h0 : 0 ≤ eps)
    (j : Fin L) (v : Vertex (Coord b L)) :
    blockCoverage b L eps j v ≤ (hitCount b L j v : ℝ) := by
  have hbound : ∀ c : Fin (blockCount b L j), (1 - eps ^ blockFails b L j c v)
      ≤ if 0 < blockFails b L j c v then (1 : ℝ) else 0 := by
    intro c
    by_cases hc : 0 < blockFails b L j c v
    · rw [if_pos hc]
      have : (0 : ℝ) ≤ eps ^ blockFails b L j c v := pow_nonneg h0 _
      linarith
    · rw [if_neg hc]
      have hz : blockFails b L j c v = 0 := by omega
      rw [hz, pow_zero]
      linarith
  calc blockCoverage b L eps j v
      ≤ ∑ c : Fin (blockCount b L j), if 0 < blockFails b L j c v then (1 : ℝ) else 0 :=
        Finset.sum_le_sum fun c _ => hbound c
    _ = (hitCount b L j v : ℝ) := by
        rw [Finset.sum_boole]
        exact_mod_cast congrArg (fun n : ℕ => (n : ℝ)) (hitCount_eq_card_filter_pos b L j v)

/-- The level-`j` blocks partition the leaves, so their failed-leaf counts add
up to the total failed-leaf count `R`. -/
theorem sum_blockFails (b L : ℕ) (j : Fin L) (v : Vertex (Coord b L)) :
    ∑ c, ((blockFails b L j c v : ℕ) : ℝ) = (failureCount b L v : ℝ) := by
  rw [Finset.sum_congr rfl fun c _ => blockFails_cast b L j c v,
    sum_blocks b L j (fun i => 1 - vertexPoint v (Sum.inr i)), ← failureCount_eq_sum]

/-- The blockwise bound `1 - eps ^ r ≤ (1-eps) r` of the source, summed. -/
theorem blockCoverage_le_failureCount (b L : ℕ) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1)
    (j : Fin L) (v : Vertex (Coord b L)) :
    blockCoverage b L eps j v ≤ (1 - eps) * (failureCount b L v : ℝ) := by
  calc blockCoverage b L eps j v
      ≤ ∑ c : Fin (blockCount b L j), (1 - eps) * ((blockFails b L j c v : ℕ) : ℝ) :=
        Finset.sum_le_sum fun c _ => one_sub_pow_le_mul eps h0 h1 _
    _ = (1 - eps) * (failureCount b L v : ℝ) := by rw [← Finset.mul_sum, sum_blockFails]

/-- The pointwise majorant of the coverage objective used in PB38. -/
theorem coverage_le (b L : ℕ) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1)
    (v : Vertex (Coord b L)) :
    coverage b L eps v
      ≤ (1 - eps) * (∑ j : Fin L, vertexPoint v (Sum.inl j) * (hitCount b L j v : ℝ))
        + eps * (1 - eps) * (L : ℝ) * (failureCount b L v : ℝ) := by
  have he : (0 : ℝ) ≤ 1 - eps := by linarith
  have hA : ∑ j : Fin L, vertexPoint v (Sum.inl j) * blockCoverage b L eps j v
      ≤ ∑ j : Fin L, vertexPoint v (Sum.inl j) * (hitCount b L j v : ℝ) :=
    Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_left
      (blockCoverage_le_hitCount b L eps h0 j v) (vertexPoint_nonneg v _)
  have hB : ∑ j : Fin L, blockCoverage b L eps j v
      ≤ (L : ℝ) * ((1 - eps) * (failureCount b L v : ℝ)) := by
    calc ∑ j : Fin L, blockCoverage b L eps j v
        ≤ ∑ _j : Fin L, (1 - eps) * (failureCount b L v : ℝ) :=
          Finset.sum_le_sum fun j _ => blockCoverage_le_failureCount b L eps h0 h1 j v
      _ = (L : ℝ) * ((1 - eps) * (failureCount b L v : ℝ)) := by
          rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  have h1' := mul_le_mul_of_nonneg_left hA he
  have h2' := mul_le_mul_of_nonneg_left hB h0
  rw [coverage]
  nlinarith [h1', h2']

/-- Every admissible law's coverage expectation obeys the source's estimate, by
the imported incidence bound (PB37) and `E R = 1`. -/
theorem expect_coverage_le (b L : ℕ) (hb : 1 ≤ b) (hL : 1 ≤ L) (eps : ℝ)
    (h0 : 0 ≤ eps) (h1 : eps ≤ 1) (μ : Law (Vertex (Coord b L)))
    (hμ : HasMeans μ (means b L)) :
    μ.expect (coverage b L eps)
      ≤ eps * (1 - eps) * (L : ℝ) + (1 - eps) * (1 + ((L : ℝ) - 1) / b) := by
  have he : (0 : ℝ) ≤ 1 - eps := by linarith
  have hR : μ.expect (fun v => (failureCount b L v : ℝ)) = 1 :=
    expect_failureCount_of_leafMeans b L hb μ (fun i => hμ (Sum.inr i))
  have hI := incidence_expect_le_of_means b L hb hL μ (fun j => hμ (Sum.inl j))
    (fun i => hμ (Sum.inr i))
  have hmono := μ.expect_mono (fun v => coverage_le b L eps h0 h1 v)
  rw [Law.expect_add, Law.expect_const_mul, Law.expect_const_mul, hR] at hmono
  nlinarith [mul_le_mul_of_nonneg_left hI he]

/-- **PB38.** Equation (5): the hull-gap upper bound. -/
theorem radix_hullGap_le (b L : ℕ) (hb : 2 ≤ b) (hL : 1 ≤ L) (eps : ℝ)
    (h0 : 0 ≤ eps) (h1 : eps ≤ 1) :
    hullTotal b L eps
      ≤ eps * (1 - eps) * (L : ℝ) + (1 - eps) * (1 + ((L : ℝ) - 1) / b)
        - dCorrection b L eps := by
  obtain ⟨μ, hmean, hz⟩ := (radix_hullGap_isGreatest b L hb eps h0 h1).1
  have hle := expect_coverage_le b L (by omega) hL eps h0 h1 μ hmean
  rw [← hz] at hle
  linarith

/-! ## PB39: the attaining-order hull-gap lower bound -/

/-- Under one-failure rounding every level-`j` block count is the indicator of
containing the failed leaf. -/
theorem blockFails_singleFailVertex (b L : ℕ) (j₀ : Fin L) (c₀ : Fin (blockCount b L j₀))
    (j : Fin L) (c : Fin (blockCount b L j)) (t : Fin (b ^ L)) :
    blockFails b L j c (singleFailVertex b L j₀ c₀ t) = if t ∈ block b L j c then 1 else 0 := by
  have hfilter : ((block b L j c).filter
      fun i => singleFailVertex b L j₀ c₀ t (Sum.inr i) = false)
      = (block b L j c).filter fun i => i = t := by
    apply Finset.filter_congr
    intro i _
    simp [singleFailVertex]
  rw [blockFails, hfilter, Finset.filter_eq']
  by_cases h : t ∈ block b L j c <;> simp [h]

/-- Exactly one level-`j` block contains a given leaf. -/
theorem filter_mem_block (b L : ℕ) (j : Fin L) (t : Fin (b ^ L)) :
    (Finset.univ.filter fun c : Fin (blockCount b L j) => t ∈ block b L j c)
      = {(blockEquiv b L j t).1} := by
  ext c
  simp [block_mem_iff, eq_comm]

/-- **PB39, the pointwise half.** Under the law that fails exactly one leaf,
every level contributes exactly `1 - eps`, deterministically. -/
theorem blockCoverage_singleFailVertex (b L : ℕ) (eps : ℝ) (j₀ : Fin L)
    (c₀ : Fin (blockCount b L j₀)) (j : Fin L) (t : Fin (b ^ L)) :
    blockCoverage b L eps j (singleFailVertex b L j₀ c₀ t) = 1 - eps := by
  have hterm : ∀ c : Fin (blockCount b L j),
      (1 - eps ^ blockFails b L j c (singleFailVertex b L j₀ c₀ t))
        = if t ∈ block b L j c then 1 - eps else 0 := by
    intro c
    rw [blockFails_singleFailVertex]
    by_cases h : t ∈ block b L j c <;> simp [h]
  rw [blockCoverage, Finset.sum_congr rfl fun c _ => hterm c, ← Finset.sum_filter,
    filter_mem_block, Finset.sum_const, Finset.card_singleton, one_smul]

/-- The coverage objective at a one-failure vertex, with the anchors free. -/
theorem coverage_singleFailVertex (b L : ℕ) (eps : ℝ) (j₀ : Fin L)
    (c₀ : Fin (blockCount b L j₀)) (t : Fin (b ^ L)) :
    coverage b L eps (singleFailVertex b L j₀ c₀ t)
      = (1 - eps) ^ 2 * (∑ j : Fin L, vertexPoint (singleFailVertex b L j₀ c₀ t) (Sum.inl j))
        + eps * (1 - eps) * (L : ℝ) := by
  simp only [coverage, blockCoverage_singleFailVertex]
  rw [← Finset.sum_mul, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  ring

/-- The exact coverage expectation of the one-failure law. -/
theorem expect_coverage_singleFail (b L : ℕ) (hb : 0 < b) (eps : ℝ) (j₀ : Fin L)
    (c₀ : Fin (blockCount b L j₀)) :
    (singleFailRounding b L hb j₀ c₀).expect (coverage b L eps)
      = eps * (1 - eps) * (L : ℝ)
        + (1 - eps) ^ 2 * ∑ j : Fin L, 1 / (blockCount b L j : ℝ) := by
  have hμ := singleFailRounding_hasMeans b L hb j₀ c₀
  have hpow : (0 : ℝ) < ((b ^ L : ℕ) : ℝ) := by exact_mod_cast pow_pos hb L
  have hanchor : ∀ j : Fin L,
      (∑ t : Fin (b ^ L), vertexPoint (singleFailVertex b L j₀ c₀ t) (Sum.inl j))
        = ((b ^ L : ℕ) : ℝ) * (1 / (blockCount b L j : ℝ)) := by
    intro j
    have h := hμ (Sum.inl j)
    rw [singleFailRounding, uniformImage_expect] at h
    have hm : means b L (Sum.inl j) = 1 / (blockCount b L j : ℝ) := rfl
    rw [hm, div_eq_iff hpow.ne'] at h
    rw [h, mul_comm]
  have hsum : (∑ t : Fin (b ^ L), coverage b L eps (singleFailVertex b L j₀ c₀ t))
      = ((b ^ L : ℕ) : ℝ) * (eps * (1 - eps) * (L : ℝ)
          + (1 - eps) ^ 2 * ∑ j : Fin L, 1 / (blockCount b L j : ℝ)) := by
    calc (∑ t : Fin (b ^ L), coverage b L eps (singleFailVertex b L j₀ c₀ t))
        = ∑ t : Fin (b ^ L), ((1 - eps) ^ 2
            * (∑ j : Fin L, vertexPoint (singleFailVertex b L j₀ c₀ t) (Sum.inl j))
            + eps * (1 - eps) * (L : ℝ)) :=
          Finset.sum_congr rfl fun t _ => coverage_singleFailVertex b L eps j₀ c₀ t
      _ = (1 - eps) ^ 2 * (∑ j : Fin L, ∑ t : Fin (b ^ L),
              vertexPoint (singleFailVertex b L j₀ c₀ t) (Sum.inl j))
            + ((b ^ L : ℕ) : ℝ) * (eps * (1 - eps) * (L : ℝ)) := by
          rw [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
            nsmul_eq_mul, ← Finset.mul_sum, Finset.sum_comm]
      _ = ((b ^ L : ℕ) : ℝ) * (eps * (1 - eps) * (L : ℝ)
            + (1 - eps) ^ 2 * ∑ j : Fin L, 1 / (blockCount b L j : ℝ)) := by
          rw [Finset.sum_congr rfl fun j (_ : j ∈ Finset.univ) => hanchor j, ← Finset.mul_sum]
          ring
  rw [singleFailRounding, uniformImage_expect, hsum]
  field_simp

/-- **PB39.** Equation (6): the hull-gap lower bound from the law that fails
exactly one uniformly random leaf. -/
theorem radix_hullGap_ge (b L : ℕ) (hb : 2 ≤ b) (hL : 0 < L) (eps : ℝ)
    (h0 : 0 ≤ eps) (h1 : eps ≤ 1) :
    eps * (1 - eps) * (L : ℝ) + (1 - eps) ^ 2 * (∑ j : Fin L, 1 / (blockCount b L j : ℝ))
        - dCorrection b L eps ≤ hullTotal b L eps := by
  have hb0 : 0 < b := by omega
  have j₀ : Fin L := ⟨0, hL⟩
  have c₀ : Fin (blockCount b L j₀) := ⟨0, pow_pos hb0 _⟩
  have hmem : (singleFailRounding b L hb0 j₀ c₀).expect (coverage b L eps)
      ∈ coverageValues b L eps :=
    ⟨_, singleFailRounding_hasMeans b L hb0 j₀ c₀, rfl⟩
  have hle := (radix_hullGap_isGreatest b L hb eps h0 h1).2 hmem
  rw [expect_coverage_singleFail b L hb0 eps j₀ c₀] at hle
  linarith

/-! ## PB40: finite positivity -/

/-- The sharper correction bound `D_L ≤ eps (1-eps) L` of the source, which is
what makes the hull gap positive at every finite `L`. -/
theorem dCorrection_le_mul (b L : ℕ) (hb : 0 < b) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) :
    dCorrection b L eps ≤ eps * (1 - eps) * (L : ℝ) := by
  have hbR : (0 : ℝ) < (b : ℝ) := by exact_mod_cast hb
  have hstep : ∀ t ∈ Finset.range L, (1 - eps ^ b ^ t) / (b : ℝ) ^ t ≤ 1 - eps := by
    intro t _
    have hp : (0 : ℝ) < (b : ℝ) ^ t := by positivity
    rw [div_le_iff₀ hp]
    have h := one_sub_pow_le_mul eps h0 h1 (b ^ t)
    have hcast : ((b ^ t : ℕ) : ℝ) = (b : ℝ) ^ t := by push_cast; ring
    rw [hcast] at h
    linarith
  calc dCorrection b L eps = eps * ∑ t ∈ Finset.range L, (1 - eps ^ b ^ t) / (b : ℝ) ^ t := rfl
    _ ≤ eps * ∑ _t ∈ Finset.range L, (1 - eps) :=
        mul_le_mul_of_nonneg_left (Finset.sum_le_sum hstep) h0
    _ = eps * (1 - eps) * (L : ℝ) := by
        rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul]
        ring

/-- **PB40.** The hull gap of the family is strictly positive at every finite
`L`. This precedes every division by a hull gap. -/
theorem hullTotal_pos (b L : ℕ) (hb : 2 ≤ b) (hL : 0 < L) (eps : ℝ)
    (h0 : 0 < eps) (h1 : eps < 1) : 0 < hullTotal b L eps := by
  have hb0 : 0 < b := by omega
  have hne : Nonempty (Fin L) := ⟨⟨0, hL⟩⟩
  have hsig : 0 < ∑ j : Fin L, 1 / (blockCount b L j : ℝ) := by
    refine Finset.sum_pos (fun j _ => ?_) Finset.univ_nonempty
    have hc : (0 : ℝ) < (blockCount b L j : ℝ) := by
      exact_mod_cast pow_pos hb0 (j.val + 1)
    positivity
  have hX : (0 : ℝ) < (1 - eps) ^ 2 * ∑ j : Fin L, 1 / (blockCount b L j : ℝ) :=
    mul_pos (pow_pos (by linarith) 2) hsig
  have hlb := radix_hullGap_ge b L hb hL eps h0.le h1.le
  have hD := dCorrection_le_mul b L hb0 eps h0.le h1.le
  linarith

/-! ## PB41: the two limits, at each fixed `rho` -/

/-- The uniform two-sided bracket of the hull gap at radix `b = L ^ 2`. -/
theorem hullTotal_sq_bounds (L : ℕ) (hL : 2 ≤ L) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) :
    eps * (1 - eps) * (L : ℝ) - 2 ≤ hullTotal (L ^ 2) L eps ∧
      hullTotal (L ^ 2) L eps ≤ eps * (1 - eps) * (L : ℝ) + 2 := by
  have hb : 2 ≤ L ^ 2 := two_le_sq L hL
  have hb0 : 0 < L ^ 2 := by omega
  have hLR : (2 : ℝ) ≤ (L : ℝ) := by exact_mod_cast hL
  have hcast : ((L ^ 2 : ℕ) : ℝ) = (L : ℝ) ^ 2 := by push_cast; ring
  have hbR : (4 : ℝ) ≤ ((L ^ 2 : ℕ) : ℝ) := by rw [hcast]; nlinarith
  have hD0 := dCorrection_nonneg (L ^ 2) L hb0 eps h0 h1
  have hD1 := dCorrection_le (L ^ 2) L hb eps h0
  have hD2 : dCorrection (L ^ 2) L eps ≤ 2 := by
    have hb1 : (0 : ℝ) < ((L ^ 2 : ℕ) : ℝ) - 1 := by linarith
    have hstep : eps * ((L ^ 2 : ℕ) : ℝ) / (((L ^ 2 : ℕ) : ℝ) - 1) ≤ 2 := by
      rw [div_le_iff₀ hb1]
      nlinarith
    linarith
  have hfrac0 : (0 : ℝ) ≤ ((L : ℝ) - 1) / ((L ^ 2 : ℕ) : ℝ) := by
    apply div_nonneg <;> linarith
  have hfrac1 : ((L : ℝ) - 1) / ((L ^ 2 : ℕ) : ℝ) ≤ 1 := by
    rw [div_le_one (by linarith)]
    rw [hcast]
    nlinarith
  have hsig : (0 : ℝ) ≤ ∑ j : Fin L, 1 / (blockCount (L ^ 2) L j : ℝ) := by
    refine Finset.sum_nonneg fun j _ => ?_
    have hc : (0 : ℝ) < (blockCount (L ^ 2) L j : ℝ) := by
      exact_mod_cast pow_pos hb0 (j.val + 1)
    positivity
  have hX : (0 : ℝ) ≤ (1 - eps) ^ 2 * ∑ j : Fin L, 1 / (blockCount (L ^ 2) L j : ℝ) :=
    mul_nonneg (sq_nonneg _) hsig
  have hup := radix_hullGap_le (L ^ 2) L hb (by omega) eps h0 h1
  have hlo := radix_hullGap_ge (L ^ 2) L hb (by omega) eps h0 h1
  have hprod : (1 - eps) * (1 + ((L : ℝ) - 1) / ((L ^ 2 : ℕ) : ℝ)) ≤ 2 := by
    have := mul_le_mul (show (1 : ℝ) - eps ≤ 1 by linarith)
      (show 1 + ((L : ℝ) - 1) / ((L ^ 2 : ℕ) : ℝ) ≤ 2 by linarith)
      (by linarith) (by norm_num : (0 : ℝ) ≤ 1)
    linarith
  exact ⟨by linarith, by linarith⟩

/-- The uniform two-sided bracket of the termwise gap at radix `b = L ^ 2`. -/
theorem termwiseTotal_sq_bounds (L : ℕ) (hL : 2 ≤ L) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) :
    (1 - eps) * (L : ℝ) - 2 ≤ termwiseTotal (L ^ 2) L eps ∧
      termwiseTotal (L ^ 2) L eps ≤ (1 - eps) * (L : ℝ) + 2 := by
  have hb : 2 ≤ L ^ 2 := two_le_sq L hL
  have hb0 : 0 < L ^ 2 := by omega
  have hLR : (2 : ℝ) ≤ (L : ℝ) := by exact_mod_cast hL
  have hcast : ((L ^ 2 : ℕ) : ℝ) = (L : ℝ) ^ 2 := by push_cast; ring
  have hbR : (4 : ℝ) ≤ ((L ^ 2 : ℕ) : ℝ) := by rw [hcast]; nlinarith
  have hD0 := dCorrection_nonneg (L ^ 2) L hb0 eps h0 h1
  have hD1 := dCorrection_le (L ^ 2) L hb eps h0
  have hD2 : dCorrection (L ^ 2) L eps ≤ 2 := by
    have hb1 : (0 : ℝ) < ((L ^ 2 : ℕ) : ℝ) - 1 := by linarith
    have hstep : eps * ((L ^ 2 : ℕ) : ℝ) / (((L ^ 2 : ℕ) : ℝ) - 1) ≤ 2 := by
      rw [div_le_iff₀ hb1]
      nlinarith
    linarith
  have hT : termwiseTotal (L ^ 2) L eps = (1 - eps) * (L : ℝ) - dCorrection (L ^ 2) L eps := rfl
  exact ⟨by rw [hT]; linarith, by rw [hT]; linarith⟩

/-- Squeeze: a sequence trapped within a constant of `A * L` has `f L / L → A`. -/
private theorem tendsto_div_of_bracket {A : ℝ} (f : ℕ → ℝ)
    (h : ∀ᶠ L : ℕ in atTop, A * (L : ℝ) - 2 ≤ f L ∧ f L ≤ A * (L : ℝ) + 2) :
    Tendsto (fun L : ℕ => f L / (L : ℝ)) atTop (𝓝 A) := by
  have h2 : Tendsto (fun L : ℕ => (2 : ℝ) / (L : ℝ)) atTop (𝓝 0) := by
    have h := (tendsto_one_div_atTop_nhds_zero_nat (𝕜 := ℝ)).const_mul (2 : ℝ)
    simpa [div_eq_mul_inv] using h
  have hlo : Tendsto (fun L : ℕ => A - 2 / (L : ℝ)) atTop (𝓝 A) := by
    simpa using h2.const_sub A
  have hhi : Tendsto (fun L : ℕ => A + 2 / (L : ℝ)) atTop (𝓝 A) := by
    simpa using h2.const_add A
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' hlo hhi ?_ ?_
  · filter_upwards [h, eventually_gt_atTop 0] with L hL hL0
    have hLR : (0 : ℝ) < (L : ℝ) := by exact_mod_cast hL0
    rw [le_div_iff₀ hLR]
    have hmul : (A - 2 / (L : ℝ)) * (L : ℝ) = A * (L : ℝ) - 2 := by field_simp
    rw [hmul]
    exact hL.1
  · filter_upwards [h, eventually_gt_atTop 0] with L hL hL0
    have hLR : (0 : ℝ) < (L : ℝ) := by exact_mod_cast hL0
    rw [div_le_iff₀ hLR]
    have hmul : (A + 2 / (L : ℝ)) * (L : ℝ) = A * (L : ℝ) + 2 := by field_simp
    rw [hmul]
    exact hL.2

/-- **PB41, first limit.** For each **fixed** `rho > 1` — so `eps = 1 / rho` and
the stage-`L` radix `b = L ^ 2` are determined before the limit is taken —
`H_L / L → eps (1 - eps)` as `L → ∞`. -/
theorem hullTotal_div_tendsto (rho : ℝ) (hrho : 1 < rho) :
    Tendsto (fun L : ℕ => hullTotal (L ^ 2) L (1 / rho) / (L : ℝ)) atTop
      (𝓝 (1 / rho * (1 - 1 / rho))) := by
  obtain ⟨h0, h1⟩ := eps_mem_Ioo rho hrho
  refine tendsto_div_of_bracket _ ?_
  filter_upwards [eventually_ge_atTop 2] with L hL
  exact hullTotal_sq_bounds L hL (1 / rho) h0.le h1.le

/-- The companion limit `T_L / L → 1 - eps` at the same fixed `rho`. -/
theorem termwiseTotal_div_tendsto (rho : ℝ) (hrho : 1 < rho) :
    Tendsto (fun L : ℕ => termwiseTotal (L ^ 2) L (1 / rho) / (L : ℝ)) atTop
      (𝓝 (1 - 1 / rho)) := by
  obtain ⟨h0, h1⟩ := eps_mem_Ioo rho hrho
  refine tendsto_div_of_bracket _ ?_
  filter_upwards [eventually_ge_atTop 2] with L hL
  exact termwiseTotal_sq_bounds L hL (1 / rho) h0.le h1.le

private theorem div_div_div_cancel (a b : ℝ) {c : ℝ} (hc : c ≠ 0) : a / c / (b / c) = a / b := by
  rcases eq_or_ne b 0 with rfl | hb
  · simp
  · field_simp

/-- **PB41, second limit.** For each **fixed** `rho > 1`, `T_L / H_L → rho` as
`L → ∞`. The quantifier order is `∀ rho, Tendsto (fun L => …)`: there is no
interchange of the `L` and `rho` limits. -/
theorem radix_ratio_tendsto (rho : ℝ) (hrho : 1 < rho) :
    Tendsto (fun L : ℕ => termwiseTotal (L ^ 2) L (1 / rho) / hullTotal (L ^ 2) L (1 / rho))
      atTop (𝓝 rho) := by
  obtain ⟨h0, h1⟩ := eps_mem_Ioo rho hrho
  have hne : (1 : ℝ) - 1 / rho ≠ 0 := by
    have : 1 / rho < 1 := h1
    intro hcon
    linarith
  have hden : 1 / rho * (1 - 1 / rho) ≠ 0 := mul_ne_zero h0.ne' hne
  have hlim : (1 - 1 / rho) / (1 / rho * (1 - 1 / rho)) = rho := by
    rw [mul_comm, ← div_div, div_self hne, one_div_one_div]
  have h := (termwiseTotal_div_tendsto rho hrho).div (hullTotal_div_tendsto rho hrho) hden
  rw [hlim] at h
  refine h.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with L hL
  have hLR : ((L : ℝ)) ≠ 0 := by
    have : (0 : ℝ) < (L : ℝ) := by exact_mod_cast hL
    exact this.ne'
  exact div_div_div_cancel _ _ hLR

/-! ## PB42 for this family: rescaling `[1/rho, 1]` to `[1, rho]` -/

/-- The rescaled coefficients on `[1, rho]`: a degree-`d` term of the family
acquires the positive coefficient `rho ^ -d = eps ^ d`. -/
def scaledCoeff (b L : ℕ) (eps : ℝ) (s : Finset (Coord b L)) : ℝ := eps ^ s.card

/-- **PB42 for this family.** Scaling every physical variable by `rho` carries
`[1/rho, 1]` onto `[1, rho]`, with the same cube parameters. -/
theorem boxPoint_eps_eq (b L : ℕ) (rho : ℝ) (hrho : 0 < rho) (q : Coord b L → ℝ)
    (i : Coord b L) :
    boxPoint (epsLower b L (1 / rho)) (epsUpper b L) q i
      = (1 / rho) * boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q i := by
  have hrho0 : rho ≠ 0 := hrho.ne'
  simp only [boxPoint, epsLower, epsUpper]
  field_simp

/-- A single monomial acquires exactly the factor `eps ^ d` under the rescaling. -/
theorem monomial_boxPoint_eps (b L : ℕ) (rho : ℝ) (hrho : 0 < rho) (s : Finset (Coord b L))
    (q : Coord b L → ℝ) :
    monomial s (boxPoint (epsLower b L (1 / rho)) (epsUpper b L) q)
      = (1 / rho) ^ s.card * monomial s (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q) := by
  rw [monomial, monomial, Finset.prod_congr rfl fun i _ => boxPoint_eps_eq b L rho hrho q i,
    Finset.prod_mul_distrib, Finset.prod_const]

/-- The whole family on `[1/rho, 1]` is *the same function of the cube
parameters* as the rescaled family on `[1, rho]`. -/
theorem supportPolynomial_boxPoint_eps (b L : ℕ) (rho : ℝ) (hrho : 0 < rho)
    (q : Coord b L → ℝ) :
    supportPolynomial (termSupports b L) (fun _ => 1)
        (boxPoint (epsLower b L (1 / rho)) (epsUpper b L) q)
      = supportPolynomial (termSupports b L) (scaledCoeff b L (1 / rho))
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q) := by
  rw [supportPolynomial, supportPolynomial]
  refine Finset.sum_congr rfl fun s _ => ?_
  rw [one_mul, monomial_boxPoint_eps b L rho hrho, scaledCoeff]

/-- The hull gap is preserved exactly by the rescaling. -/
theorem hullTotal_eq_boxHullGap (b L : ℕ) (hb : 0 < b) (rho : ℝ) (hrho : 1 < rho) :
    boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho)
        (supportPolynomial (termSupports b L) (scaledCoeff b L (1 / rho)))
        (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (means b L))
      = hullTotal b L (1 / rho) := by
  have hrho0 : (0 : ℝ) < rho := by linarith
  have h1 : (1 / rho) ≤ 1 := (eps_mem_Ioo rho hrho).2.le
  have hcube := means_mem_cube b L hb
  have hfun : (fun q => supportPolynomial (termSupports b L) (scaledCoeff b L (1 / rho))
      (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q))
      = fun q => polynomial b L (boxPoint (epsLower b L (1 / rho)) (epsUpper b L) q) := by
    funext q
    rw [← supportPolynomial_termSupports b L hb, supportPolynomial_boxPoint_eps b L rho hrho0]
  rw [boxHullGap_eq_of_mem (fun _ => (1 : ℝ)) (fun _ => rho) (fun _ => hrho.le) _ _ hcube,
    hullTotal, physMeans,
    boxHullGap_eq_of_mem _ _ (epsLower_le_epsUpper b L h1) _ _ hcube, hfun]

/-- The zero shift is mean exact, which is what turns a pure rescaling into a
gap rescaling. -/
theorem meanExact_zero {I : Type*} [Fintype I] [DecidableEq I] (x : I → ℝ) :
    MeanExact x (fun _ => (0 : ℝ)) := fun μ _ => μ.expect_const 0

/-- Each single term's gap is multiplied by the positive constant `eps ^ d`. -/
theorem boxHullGap_monomial_eps (b L : ℕ) (hb : 0 < b) (rho : ℝ) (hrho : 1 < rho)
    (s : Finset (Coord b L)) :
    boxHullGap (epsLower b L (1 / rho)) (epsUpper b L) (monomial s) (physMeans b L (1 / rho))
      = scaledCoeff b L (1 / rho) s * boxHullGap (fun _ => (1 : ℝ)) (fun _ => rho) (monomial s)
          (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (means b L)) := by
  have hrho0 : (0 : ℝ) < rho := by linarith
  have h1 : (1 / rho) ≤ 1 := (eps_mem_Ioo rho hrho).2.le
  have hcube := means_mem_cube b L hb
  rw [physMeans, boxHullGap_eq_of_mem _ _ (epsLower_le_epsUpper b L h1) _ _ hcube,
    boxHullGap_eq_of_mem (fun _ => (1 : ℝ)) (fun _ => rho) (fun _ => hrho.le) _ _ hcube]
  refine hullGap_of_meanExact_split
    (fun q => monomial s (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) q))
    (fun _ => 0)
    (fun q => monomial s (boxPoint (epsLower b L (1 / rho)) (epsUpper b L) q))
    (monomial_boxPoint_separatelyAffine _ _ s)
    (monomial_boxPoint_separatelyAffine _ _ s)
    (means b L) hcube (scaledCoeff b L (1 / rho) s) ?_ ?_ (meanExact_zero _)
  · rw [scaledCoeff]
    positivity
  · intro q
    rw [monomial_boxPoint_eps b L rho hrho0, scaledCoeff]
    ring

/-- The termwise gap is preserved exactly by the rescaling. -/
theorem boxTermwiseGap_eq_termwiseTotal (b L : ℕ) (hb : 2 ≤ b) (rho : ℝ) (hrho : 1 < rho) :
    boxTermwiseGap (termSupports b L) (scaledCoeff b L (1 / rho)) (fun _ => (1 : ℝ))
        (fun _ => rho) (boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (means b L))
      = termwiseTotal b L (1 / rho) := by
  obtain ⟨h0, h1⟩ := eps_mem_Ioo rho hrho
  rw [← radix_boxTermwiseGap b L hb (1 / rho) h0.le h1.le, boxTermwiseGap, boxTermwiseGap]
  refine Finset.sum_congr rfl fun s _ => ?_
  rw [one_mul, boxHullGap_monomial_eps b L (by omega) rho hrho s]

/-! ## PB43: `C_box(rho) ≥ rho` -/

/-- Every stage of the rescaled family is an admissible common-aspect witness on
`[1, rho]^n`, with its exact ratio `T_L / H_L`. -/
theorem radix_ratio_mem_commonAspectBoxRatios (L : ℕ) (hL : 2 ≤ L) (rho : ℝ) (hrho : 1 < rho) :
    termwiseTotal (L ^ 2) L (1 / rho) / hullTotal (L ^ 2) L (1 / rho)
      ∈ commonAspectBoxRatios rho := by
  have hb : 2 ≤ L ^ 2 := two_le_sq L hL
  have hb0 : 0 < L ^ 2 := by omega
  obtain ⟨h0, h1⟩ := eps_mem_Ioo rho hrho
  have hpos : 0 < hullTotal (L ^ 2) L (1 / rho) :=
    hullTotal_pos (L ^ 2) L hb (by omega) (1 / rho) h0 h1
  have hgap := hullTotal_eq_boxHullGap (L ^ 2) L hb0 rho hrho
  refine ⟨Coord (L ^ 2) L, inferInstance, inferInstance, termSupports (L ^ 2) L,
    scaledCoeff (L ^ 2) L (1 / rho),
    boxPoint (fun _ => (1 : ℝ)) (fun _ => rho) (means (L ^ 2) L), ?_, ?_, ?_, ?_⟩
  · intro s _
    rw [scaledCoeff]
    positivity
  · exact boxPoint_mem _ _ _ (fun _ => hrho.le) (means_mem_cube (L ^ 2) L hb0)
  · rw [hgap]
    exact hpos
  · rw [hgap, boxTermwiseGap_eq_termwiseTotal (L ^ 2) L hb rho hrho]

/-- **PB43** without any boundedness hypothesis: every upper bound of the
common-aspect ratio class on `[1, rho]^n` is at least `rho`. -/
theorem rho_le_of_forall_mem_commonAspectBoxRatios {rho U : ℝ} (hrho : 1 < rho)
    (hU : ∀ r ∈ commonAspectBoxRatios rho, r ≤ U) : rho ≤ U := by
  refine le_of_tendsto (radix_ratio_tendsto rho hrho) ?_
  filter_upwards [eventually_ge_atTop 2] with L hL
  exact hU _ (radix_ratio_mem_commonAspectBoxRatios L hL rho hrho)

/-- The same statement for the general strictly positive aspect-ratio class. -/
theorem rho_le_of_forall_mem_boxAspectRatios {rho U : ℝ} (hrho : 1 < rho)
    (hU : ∀ r ∈ boxAspectRatios rho, r ≤ U) : rho ≤ U :=
  rho_le_of_forall_mem_commonAspectBoxRatios hrho fun r hr =>
    hU r (commonAspectBoxRatios_subset_boxAspectRatios hrho.le hr)

/-- **PB43.** `C_box(rho) ≥ rho` for every `rho > 1`, under the explicit
boundedness hypothesis that the supremum needs. -/
theorem rho_le_boxAspectSupremum {rho : ℝ} (hrho : 1 < rho)
    (hbdd : BddAbove (boxAspectRatios rho)) : rho ≤ boxAspectSupremum rho :=
  rho_le_of_forall_mem_boxAspectRatios hrho fun _ hr => le_csSup hbdd hr

/-- The common-aspect supremum on `[1, rho]^n` is at least `rho` as well. -/
theorem rho_le_commonAspectBoxSupremum {rho : ℝ} (hrho : 1 < rho)
    (hbdd : BddAbove (commonAspectBoxRatios rho)) : rho ≤ commonAspectBoxSupremum rho :=
  rho_le_of_forall_mem_commonAspectBoxRatios hrho fun _ hr => le_csSup hbdd hr

end
end Radix
end MultilinearGap
