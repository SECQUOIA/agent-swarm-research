import Formal.MultilinearGap.RadixFamily
import Formal.MultilinearGap.BoxTransfer
import Formal.CubicGap.Envelope

/-!
# Exact termwise envelopes of the variable-radix family on `[eps, 1]`

This module instantiates the radix-`b` anchor/leaf family of `RadixFamily.lean`
on the strictly positive box `[eps, 1]` and computes the two **exact** envelope
values of each of its terms, together with the exact total termwise gap.  These
are the obligations PB32-PB35 of `formal/topics/18-positive-box/CLAIMS.md`,
whose source is `results/positive-multilinear-positive-box-lower.md`.

Writing `eps = 1 / rho` with `rho > 1`, `L >= 2`, `b = L ^ 2` and `m = b ^ L`:

* **PB32** (`physMeans`, `physMeans_mem_box`, `physMeans_mem_interior`,
  `supportPolynomial_termSupports`).  Every variable ranges over `[eps, 1]`, the
  normalized endpoint-success means are `b ^ -(j+1)` for the anchor of level `j`
  and `1 - 1/m` for every leaf (`means` of `RadixFamily.lean`), and the
  corresponding physical point is strictly interior to `[eps, 1]`.
  In the source's notation `p(a, z) = ∑_j ∑_{B ∈ P_j} a_j ∏_{i ∈ B} z_i` the
  symbol `a_j` is the **anchor variable of level `j`**, not a coefficient: the
  family carries unit coefficients throughout ("The family above has unit
  coefficients on `[1/rho, 1]`").  Accordingly `termSupports` is used with the
  constant coefficient `1`.
* **PB33** (`term_convex_envelope`).  The exact convex-envelope value of every
  term is `eps`.  The lower bound is the integer form of Jensen's inequality
  (`pow_ge_support_line`, a Bernoulli estimate) applied to `E R = 1`, and the
  value is **attained** by `singleFailRounding`, the categorical law that fails
  exactly one coordinate of the term.
* **PB34** (`term_concave_envelope`).  The exact concave value of a level-`j`
  term is `termConcave = eps + (1-eps) u_j - (eps/m)(1 - eps ^ k)` with
  `u_j = 1 / blockCount b L j` and `k = blockSize b L j`, the number of leaves
  of the block.  The upper bound is a linear-programming dual certificate
  (`term_dual_pointwise`) whose only nonelementary ingredient is the chord bound
  `geom_chord`, and the value is **attained** by `thresholdRounding`, the
  common-threshold success coupling realized as a uniform law on `Fin m`.
* **PB35** (`radix_boxTermwiseGap`, `dCorrection_nonneg`, `dCorrection_le`).
  The exact termwise gap is `termwiseTotal = (1-eps) L - dCorrection` with
  `dCorrection = eps ∑_{t < L} (1 - eps ^ (b ^ t)) / b ^ t`, and
  `0 ≤ dCorrection ≤ eps * b / (b - 1)`.

All of this is stated with the existing box layer (`coordinateBox`, `boxPoint`,
`boxEnvelopeValues`, `boxHullGap`, `boxTermwiseGap` of `BoxTransfer.lean`), so
the hull-gap side of the lower bound can be built directly on top of it.

The general fact that common-threshold rounding maximizes every positive
physical monomial is PB05, proved in `PhysicalEnvelope.lean`; the proof here is
independent of it and produces the closed form for this family directly.
-/

namespace MultilinearGap
namespace Radix

noncomputable section
open scoped BigOperators
open CubicGap

/-! ## Two scalar inequalities -/

/-- The integer Jensen bound for the convex envelope: `n ↦ eps ^ n` lies above
its support line at `n = 1`.  This is Bernoulli's inequality after factoring out
one `eps`. -/
theorem pow_ge_support_line (eps : ℝ) (h0 : 0 ≤ eps) (n : ℕ) :
    eps - eps * (1 - eps) * ((n : ℝ) - 1) ≤ eps ^ n := by
  cases n with
  | zero =>
      simp only [Nat.cast_zero, pow_zero]
      nlinarith [sq_nonneg (1 - eps)]
  | succ p =>
      have hb : 1 + (p : ℝ) * (eps - 1) ≤ eps ^ p := by
        have h := one_add_mul_le_pow (a := eps - 1) (by linarith) p
        rwa [show (1 : ℝ) + (eps - 1) = eps by ring] at h
      have hmul : eps * (1 + (p : ℝ) * (eps - 1)) ≤ eps * eps ^ p :=
        mul_le_mul_of_nonneg_left hb h0
      calc eps - eps * (1 - eps) * (((p + 1 : ℕ) : ℝ) - 1)
          = eps * (1 + (p : ℝ) * (eps - 1)) := by push_cast; ring
        _ ≤ eps * eps ^ p := hmul
        _ = eps ^ (p + 1) := by ring

/-- The chord bound behind the concave envelope: for `s ≤ k` the point
`(s, eps ^ s)` lies below the chord of `n ↦ eps ^ n` through `(0, 1)` and
`(k, eps ^ k)`.  Equivalently `n ↦ (1 - eps ^ n) / n` is nonincreasing. -/
theorem geom_chord (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) {s k : ℕ} (hsk : s ≤ k) :
    (s : ℝ) * (1 - eps ^ k) ≤ (k : ℝ) * (1 - eps ^ s) := by
  have key : ∀ n : ℕ, (1 - eps) * (∑ i ∈ Finset.range n, eps ^ i) = 1 - eps ^ n := by
    intro n
    linear_combination -geom_sum_mul eps n
  have hsplit : (∑ i ∈ Finset.range s, eps ^ i) + (∑ i ∈ Finset.Ico s k, eps ^ i)
      = ∑ i ∈ Finset.range k, eps ^ i := Finset.sum_range_add_sum_Ico _ hsk
  have hks : ((k - s : ℕ) : ℝ) = (k : ℝ) - (s : ℝ) := by
    rw [Nat.cast_sub hsk]
  have hIco : (∑ i ∈ Finset.Ico s k, eps ^ i) ≤ ((k : ℝ) - (s : ℝ)) * eps ^ s := by
    calc (∑ i ∈ Finset.Ico s k, eps ^ i) ≤ ∑ _i ∈ Finset.Ico s k, eps ^ s :=
          Finset.sum_le_sum fun i hi =>
            pow_le_pow_of_le_one h0 h1 (Finset.mem_Ico.mp hi).1
      _ = ((k : ℝ) - (s : ℝ)) * eps ^ s := by
          rw [Finset.sum_const, Nat.card_Ico, nsmul_eq_mul, hks]
  have hrange : (s : ℝ) * eps ^ s ≤ ∑ i ∈ Finset.range s, eps ^ i := by
    calc (s : ℝ) * eps ^ s = ∑ _i ∈ Finset.range s, eps ^ s := by
          rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul]
      _ ≤ _ := Finset.sum_le_sum fun i hi =>
          pow_le_pow_of_le_one h0 h1 (le_of_lt (Finset.mem_range.mp hi))
  have hsub : (0 : ℝ) ≤ (k : ℝ) - (s : ℝ) := by
    have : (s : ℝ) ≤ (k : ℝ) := Nat.cast_le.mpr hsk
    linarith
  have hsum : (s : ℝ) * (∑ i ∈ Finset.range k, eps ^ i)
      ≤ (k : ℝ) * (∑ i ∈ Finset.range s, eps ^ i) := by
    calc (s : ℝ) * (∑ i ∈ Finset.range k, eps ^ i)
        = (s : ℝ) * (∑ i ∈ Finset.range s, eps ^ i)
            + (s : ℝ) * (∑ i ∈ Finset.Ico s k, eps ^ i) := by rw [← hsplit]; ring
      _ ≤ (s : ℝ) * (∑ i ∈ Finset.range s, eps ^ i)
            + (s : ℝ) * (((k : ℝ) - (s : ℝ)) * eps ^ s) := by
          linarith [mul_le_mul_of_nonneg_left hIco (Nat.cast_nonneg s)]
      _ = (s : ℝ) * (∑ i ∈ Finset.range s, eps ^ i)
            + ((k : ℝ) - (s : ℝ)) * ((s : ℝ) * eps ^ s) := by ring
      _ ≤ (s : ℝ) * (∑ i ∈ Finset.range s, eps ^ i)
            + ((k : ℝ) - (s : ℝ)) * (∑ i ∈ Finset.range s, eps ^ i) := by
          linarith [mul_le_mul_of_nonneg_left hrange hsub]
      _ = (k : ℝ) * (∑ i ∈ Finset.range s, eps ^ i) := by ring
  have hm := mul_le_mul_of_nonneg_left hsum (show (0 : ℝ) ≤ 1 - eps by linarith)
  calc (s : ℝ) * (1 - eps ^ k)
      = (1 - eps) * ((s : ℝ) * ∑ i ∈ Finset.range k, eps ^ i) := by
        linear_combination (-(s : ℝ)) * key k
    _ ≤ (1 - eps) * ((k : ℝ) * ∑ i ∈ Finset.range s, eps ^ i) := hm
    _ = (k : ℝ) * (1 - eps ^ s) := by linear_combination (k : ℝ) * key s

/-- The dual certificate of the concave envelope, as a pointwise inequality at
every binary assignment: `a` is the anchor failure indicator and `s` the number
of failed leaves of a block of `k` leaves. -/
theorem term_dual_pointwise (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) {a s k : ℕ}
    (ha : a ≤ 1) (hs : s ≤ k) :
    (k : ℝ) * eps ^ (a + s)
      ≤ (k : ℝ) * (1 + (eps - 1) * (a : ℝ)) + eps * (eps ^ k - 1) * (s : ℝ) := by
  have hchord := geom_chord eps h0 h1 hs
  have hbase : (k : ℝ) * eps ^ s ≤ (k : ℝ) + (s : ℝ) * (eps ^ k - 1) := by nlinarith [hchord]
  have hk1 : eps ^ k ≤ 1 := pow_le_one₀ h0 h1
  have hsnn : (0 : ℝ) ≤ (s : ℝ) := Nat.cast_nonneg s
  interval_cases a
  · have hcmp : (s : ℝ) * (eps ^ k - 1) ≤ eps * (eps ^ k - 1) * (s : ℝ) := by
      nlinarith [mul_nonneg (mul_nonneg hsnn (sub_nonneg.mpr hk1)) (sub_nonneg.mpr h1)]
    simpa using by linarith [hbase, hcmp]
  · have hmul : eps * ((k : ℝ) * eps ^ s) ≤ eps * ((k : ℝ) + (s : ℝ) * (eps ^ k - 1)) :=
      mul_le_mul_of_nonneg_left hbase h0
    have hpow : eps ^ (1 + s) = eps * eps ^ s := by rw [pow_add, pow_one]
    rw [hpow]
    push_cast
    nlinarith [hmul]

/-! ## The `[eps, 1]` box and its evaluation point -/

/-- The lower endpoints of the box `[eps, 1]` in every coordinate. -/
def epsLower (b L : ℕ) (eps : ℝ) : Coord b L → ℝ := fun _ => eps

/-- The upper endpoints of the box `[eps, 1]` in every coordinate. -/
def epsUpper (b L : ℕ) : Coord b L → ℝ := fun _ => 1

theorem epsLower_le_epsUpper (b L : ℕ) {eps : ℝ} (h1 : eps ≤ 1) (i : Coord b L) :
    epsLower b L eps i ≤ epsUpper b L i := h1

/-- The physical evaluation point of the family on `[eps, 1]`: the image of the
normalized means `means b L` under the affine parameterization of the box. -/
def physMeans (b L : ℕ) (eps : ℝ) : Coord b L → ℝ :=
  boxPoint (epsLower b L eps) (epsUpper b L) (means b L)

theorem physMeans_apply (b L : ℕ) (eps : ℝ) (i : Coord b L) :
    physMeans b L eps i = eps + (1 - eps) * means b L i := rfl

theorem physMeans_mem_box (b L : ℕ) {eps : ℝ} (hb : 1 ≤ b) (h1 : eps ≤ 1) :
    physMeans b L eps ∈ coordinateBox (epsLower b L eps) (epsUpper b L) :=
  boxPoint_mem _ _ _ (epsLower_le_epsUpper b L h1) (means_mem_cube b L hb)

/-- Every physical mean is strictly inside `[eps, 1]` (PB32). -/
theorem physMeans_mem_interior (b L : ℕ) {eps : ℝ} (hb : 2 ≤ b) (hL : 0 < L)
    (h1 : eps < 1) (i : Coord b L) :
    eps < physMeans b L eps i ∧ physMeans b L eps i < 1 := by
  obtain ⟨hlo, hhi⟩ := means_strict b L hb hL i
  rw [physMeans_apply]
  constructor <;> nlinarith

/-! ## Binary values of a term on the box -/

/-- The number of coordinates of `s` that fail at the binary point `v`. -/
def failCount {ι : Type*} (s : Finset ι) (v : Vertex ι) : ℕ :=
  (s.filter fun i => v i = false).card

/-- At a binary point the physical monomial is `eps` raised to the number of
failed coordinates. -/
theorem monomial_physVertex {ι : Type*} (s : Finset ι) (eps : ℝ) (v : Vertex ι) :
    monomial s (boxPoint (fun _ => eps) (fun _ => (1 : ℝ)) (vertexPoint v))
      = eps ^ failCount s v := by
  have h : ∀ i ∈ s, boxPoint (fun _ => eps) (fun _ => (1 : ℝ)) (vertexPoint v) i
      = if v i = false then eps else 1 := by
    intro i _
    cases hv : v i <;> simp [boxPoint, vertexPoint, hv]
  rw [monomial, Finset.prod_congr rfl h, Finset.prod_ite, Finset.prod_const,
    Finset.prod_const_one, mul_one, failCount]

/-- The anchor failure indicator of the level-`j` term. -/
def anchorFail (b L : ℕ) (j : Fin L) (v : Vertex (Coord b L)) : ℕ :=
  if v (Sum.inl j) = false then 1 else 0

/-- The number of failed leaves in the level-`j` block `c`. -/
def blockFails (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j))
    (v : Vertex (Coord b L)) : ℕ :=
  ((block b L j c).filter fun i => v (Sum.inr i) = false).card

theorem blockFails_le (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j))
    (v : Vertex (Coord b L)) : blockFails b L j c v ≤ blockSize b L j := by
  rw [blockFails, ← block_card b L j c]
  exact Finset.card_filter_le _ _

theorem anchorFail_le_one (b L : ℕ) (j : Fin L) (v : Vertex (Coord b L)) :
    anchorFail b L j v ≤ 1 := by
  rw [anchorFail]; split <;> omega

/-- A term's failure count splits into its anchor and its block. -/
theorem failCount_support (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j))
    (v : Vertex (Coord b L)) :
    failCount (support b L j c) v = anchorFail b L j v + blockFails b L j c v := by
  classical
  have hnot : Sum.inl j ∉ ((block b L j c).image Sum.inr) := by simp
  have himg : (((block b L j c).image Sum.inr).filter fun i => v i = false)
      = ((block b L j c).filter fun i => v (Sum.inr i) = false).image Sum.inr := by
    rw [Finset.filter_image]
  rw [failCount, support, Finset.filter_insert]
  rw [anchorFail, blockFails, himg]
  by_cases hv : v (Sum.inl j) = false
  · rw [if_pos hv, if_pos hv, Finset.card_insert_of_notMem, Finset.card_image_of_injective]
    · omega
    · exact Sum.inr_injective
    · simp
  · rw [if_neg hv, if_neg hv, Finset.card_image_of_injective _ Sum.inr_injective]
    omega

theorem anchorFail_cast (b L : ℕ) (j : Fin L) (v : Vertex (Coord b L)) :
    ((anchorFail b L j v : ℕ) : ℝ) = 1 - vertexPoint v (Sum.inl j) := by
  rw [anchorFail]
  cases hv : v (Sum.inl j) <;> simp [vertexPoint, hv]

theorem blockFails_cast (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j))
    (v : Vertex (Coord b L)) :
    ((blockFails b L j c v : ℕ) : ℝ)
      = ∑ i ∈ block b L j c, (1 - vertexPoint v (Sum.inr i)) := by
  rw [blockFails, Finset.card_filter]
  push_cast
  refine Finset.sum_congr rfl fun i _ => ?_
  cases hv : v (Sum.inr i) <;> simp [vertexPoint, hv]

/-! ## Expectations of the failure counts -/

private theorem expect_finset_sum {ι κ : Type*} [Fintype ι] (μ : Law ι) (s : Finset κ)
    (f : κ → ι → ℝ) : μ.expect (fun i => ∑ k ∈ s, f k i) = ∑ k ∈ s, μ.expect (f k) := by
  simp only [Law.expect, Finset.mul_sum]
  rw [Finset.sum_comm]

/-- The level-`j` anchor mean, in the form used throughout. -/
theorem blockSize_div_pow (b L : ℕ) (hb : 0 < b) (j : Fin L) :
    (blockSize b L j : ℝ) / (b : ℝ) ^ L = 1 / (blockCount b L j : ℝ) := by
  have hmul : (blockCount b L j : ℝ) * (blockSize b L j : ℝ) = (b : ℝ) ^ L := by
    have := blockCount_mul_blockSize b L j
    exact_mod_cast congrArg (fun n : ℕ => (n : ℝ)) this
  have hc : (0 : ℝ) < (blockCount b L j : ℝ) := by
    have : 0 < blockCount b L j := pow_pos hb _
    exact_mod_cast this
  have hs : (0 : ℝ) < (blockSize b L j : ℝ) := by
    have : 0 < blockSize b L j := pow_pos hb _
    exact_mod_cast this
  rw [← hmul]
  field_simp

/-- The expected anchor failure of a level-`j` term under any law with the
prescribed normalized means. -/
theorem expect_anchorFail (b L : ℕ) (μ : Law (Vertex (Coord b L)))
    (hμ : HasMeans μ (means b L)) (j : Fin L) :
    μ.expect (fun v => ((anchorFail b L j v : ℕ) : ℝ)) = 1 - 1 / (blockCount b L j : ℝ) := by
  have hfun : (fun v => ((anchorFail b L j v : ℕ) : ℝ))
      = fun v => 1 - vertexPoint v (Sum.inl j) := funext fun v => anchorFail_cast b L j v
  rw [hfun, Law.expect_sub, Law.expect_const, hμ (Sum.inl j)]
  rfl

/-- The expected number of failed leaves of a level-`j` block under any law with
the prescribed normalized means. -/
theorem expect_blockFails (b L : ℕ) (μ : Law (Vertex (Coord b L)))
    (hμ : HasMeans μ (means b L)) (j : Fin L) (c : Fin (blockCount b L j)) :
    μ.expect (fun v => ((blockFails b L j c v : ℕ) : ℝ))
      = (blockSize b L j : ℝ) / (b : ℝ) ^ L := by
  have hfun : (fun v => ((blockFails b L j c v : ℕ) : ℝ))
      = fun v => ∑ i ∈ block b L j c, (1 - vertexPoint v (Sum.inr i)) :=
    funext fun v => blockFails_cast b L j c v
  have hsum := expect_finset_sum μ (block b L j c)
    (fun i v => 1 - vertexPoint v (Sum.inr i))
  have hterm : ∀ i ∈ block b L j c,
      μ.expect (fun v => 1 - vertexPoint v (Sum.inr i)) = 1 / (b : ℝ) ^ L := by
    intro i _
    rw [Law.expect_sub, Law.expect_const, hμ (Sum.inr i)]
    change 1 - (1 - 1 / (b : ℝ) ^ L) = 1 / (b : ℝ) ^ L
    ring
  rw [hfun, hsum, Finset.sum_congr rfl hterm, Finset.sum_const, block_card, nsmul_eq_mul]
  ring

/-- Every term of the family has expected failure count exactly one: this is the
identity `(1 - u_j) + k/m = 1` of the source. -/
theorem expect_failCount (b L : ℕ) (hb : 0 < b) (μ : Law (Vertex (Coord b L)))
    (hμ : HasMeans μ (means b L)) (j : Fin L) (c : Fin (blockCount b L j)) :
    μ.expect (fun v => ((failCount (support b L j c) v : ℕ) : ℝ)) = 1 := by
  have hfun : (fun v => ((failCount (support b L j c) v : ℕ) : ℝ))
      = fun v => ((anchorFail b L j v : ℕ) : ℝ) + ((blockFails b L j c v : ℕ) : ℝ) := by
    funext v
    rw [failCount_support]
    push_cast
    ring
  rw [hfun, Law.expect_add, expect_anchorFail b L μ hμ j, expect_blockFails b L μ hμ j c,
    blockSize_div_pow b L hb j]
  ring

/-! ## Two uniform laws on `Fin (b ^ L)` -/

/-- The law of `f t` when the index `t` is uniform on `Fin n`. -/
def uniformImage {ι : Type*} [Fintype ι] {n : ℕ} (hn : 0 < n) (f : Fin n → ι) : Law ι :=
  haveI : Nonempty (Fin n) := ⟨⟨0, hn⟩⟩
  (Law.uniform (Fin n)).map f

theorem uniformImage_expect {ι : Type*} [Fintype ι] {n : ℕ} (hn : 0 < n) (f : Fin n → ι)
    (g : ι → ℝ) : (uniformImage hn f).expect g = (∑ t, g (f t)) / (n : ℝ) := by
  have : Nonempty (Fin n) := ⟨⟨0, hn⟩⟩
  rw [uniformImage, Law.expect_map, Law.expect_uniform]
  simp

theorem sum_fin_lt_indicator (n d : ℕ) (hd : d ≤ n) :
    ∑ t : Fin n, (if (t : ℕ) < d then (1 : ℝ) else 0) = (d : ℝ) := by
  rw [Fin.sum_univ_eq_sum_range (fun t => if t < d then (1 : ℝ) else 0) n]
  have h : (Finset.range n).filter (fun t => t < d) = Finset.range d := by
    ext t
    simp only [Finset.mem_filter, Finset.mem_range]
    omega
  rw [Finset.sum_boole, h, Finset.card_range]

/-- A block has at least one leaf less than the whole leaf set: this is the room
needed for the top atom of the common-threshold law. -/
theorem blockSize_succ_le (b L : ℕ) (hb : 2 ≤ b) (j : Fin L) :
    blockSize b L j + 1 ≤ b ^ L := by
  have hj : j.val < L := j.isLt
  have h1 : blockSize b L j ≤ b ^ (L - 1) :=
    Nat.pow_le_pow_right (by omega) (by omega)
  have h4 : 1 ≤ b ^ (L - 1) := Nat.one_le_pow _ _ (by omega)
  have h2 : b ^ (L - 1) * 2 ≤ b ^ (L - 1) * b := Nat.mul_le_mul_left _ hb
  have h3 : b ^ (L - 1) * b = b ^ L := by
    rw [← pow_succ]
    congr 1
    omega
  omega

/-! ## Common-threshold rounding and the concave envelope -/

/-- The binary point of common-threshold rounding at threshold index `t`: the
level-`j` anchor succeeds while `t < blockSize b L j`, and every leaf succeeds
while `t < b ^ L - 1`.  The thresholds are exactly the scaled normalized means,
so the uniform law on `Fin (b ^ L)` reproduces them. -/
def thresholdVertex (b L : ℕ) (t : Fin (b ^ L)) : Vertex (Coord b L) :=
  Sum.elim (fun j => decide ((t : ℕ) < blockSize b L j))
    (fun _ => decide ((t : ℕ) + 1 < b ^ L))

/-- Common-threshold rounding: the uniform law on the `b ^ L` thresholds. -/
def thresholdRounding (b L : ℕ) (hb : 0 < b) : Law (Vertex (Coord b L)) :=
  uniformImage (pow_pos hb L) (thresholdVertex b L)

theorem anchorFail_thresholdVertex (b L : ℕ) (j : Fin L) (t : Fin (b ^ L)) :
    anchorFail b L j (thresholdVertex b L t)
      = if (t : ℕ) < blockSize b L j then 0 else 1 := by
  by_cases h : (t : ℕ) < blockSize b L j <;> simp [anchorFail, thresholdVertex, h]

theorem blockFails_thresholdVertex (b L : ℕ) (j : Fin L) (c : Fin (blockCount b L j))
    (t : Fin (b ^ L)) :
    blockFails b L j c (thresholdVertex b L t)
      = if (t : ℕ) + 1 < b ^ L then 0 else blockSize b L j := by
  by_cases h : (t : ℕ) + 1 < b ^ L
  · simp [blockFails, thresholdVertex, h]
  · simp [blockFails, thresholdVertex, h, Finset.filter_true_of_mem, block_card]

/-- Common-threshold rounding has the prescribed normalized means. -/
theorem thresholdRounding_hasMeans (b L : ℕ) (hb : 0 < b) :
    HasMeans (thresholdRounding b L hb) (means b L) := by
  have hm : 1 ≤ b ^ L := Nat.one_le_pow _ _ hb
  intro i
  rw [thresholdRounding, uniformImage_expect]
  cases i with
  | inl j =>
      have hle : blockSize b L j ≤ b ^ L := by
        rw [blockSize]
        exact Nat.pow_le_pow_right hb (by omega)
      have hval : ∀ t : Fin (b ^ L), vertexPoint (thresholdVertex b L t) (Sum.inl j)
          = if (t : ℕ) < blockSize b L j then (1 : ℝ) else 0 := by
        intro t
        by_cases h : (t : ℕ) < blockSize b L j <;> simp [vertexPoint, thresholdVertex, h]
      rw [Finset.sum_congr rfl fun t _ => hval t, sum_fin_lt_indicator _ _ hle]
      change (blockSize b L j : ℝ) / ((b ^ L : ℕ) : ℝ) = 1 / (blockCount b L j : ℝ)
      rw [Nat.cast_pow]
      exact blockSize_div_pow b L hb j
  | inr i =>
      have hle : b ^ L - 1 ≤ b ^ L := by omega
      have hval : ∀ t : Fin (b ^ L), vertexPoint (thresholdVertex b L t) (Sum.inr i)
          = if (t : ℕ) < b ^ L - 1 then (1 : ℝ) else 0 := by
        intro t
        have ht : (t : ℕ) < b ^ L := t.isLt
        by_cases h : (t : ℕ) < b ^ L - 1
        · have h' : (t : ℕ) + 1 < b ^ L := by omega
          simp [vertexPoint, thresholdVertex, h, h']
        · have h' : ¬ ((t : ℕ) + 1 < b ^ L) := by omega
          simp [vertexPoint, thresholdVertex, h, h']
      rw [Finset.sum_congr rfl fun t _ => hval t, sum_fin_lt_indicator _ _ hle]
      change ((b ^ L - 1 : ℕ) : ℝ) / ((b ^ L : ℕ) : ℝ) = 1 - 1 / (b : ℝ) ^ L
      have hpos : (0 : ℝ) < (b : ℝ) ^ L := by
        have : (0 : ℝ) < (b : ℝ) := by exact_mod_cast hb
        positivity
      rw [Nat.cast_sub hm, Nat.cast_pow, Nat.cast_one]
      field_simp

theorem thresholdRounding_sum (b L : ℕ) (eps : ℝ) (j : Fin L) (c : Fin (blockCount b L j))
    {d : ℕ} (hd : b ^ L = blockSize b L j + d + 1) :
    ∑ t : Fin (b ^ L), eps ^ failCount (support b L j c) (thresholdVertex b L t)
      = (blockSize b L j : ℝ) + (d : ℝ) * eps + eps ^ (blockSize b L j + 1) := by
  have hval : ∀ t : Fin (b ^ L),
      eps ^ failCount (support b L j c) (thresholdVertex b L t)
        = (fun x : ℕ => if x < blockSize b L j then (1 : ℝ)
            else if x + 1 < b ^ L then eps else eps ^ (blockSize b L j + 1)) (t : ℕ) := by
    intro t
    rw [failCount_support, anchorFail_thresholdVertex, blockFails_thresholdVertex]
    by_cases h1 : (t : ℕ) < blockSize b L j
    · have h2 : (t : ℕ) + 1 < b ^ L := by omega
      simp [h1, h2]
    · by_cases h2 : (t : ℕ) + 1 < b ^ L
      · simp [h1, h2]
      · simp [h1, h2, Nat.add_comm]
  have hrange : ∑ t : Fin (b ^ L), eps ^ failCount (support b L j c) (thresholdVertex b L t)
      = ∑ x ∈ Finset.range (b ^ L), (if x < blockSize b L j then (1 : ℝ)
          else if x + 1 < b ^ L then eps else eps ^ (blockSize b L j + 1)) := by
    simp only [hval]
    exact Fin.sum_univ_eq_sum_range (fun x : ℕ => if x < blockSize b L j then (1 : ℝ)
      else if x + 1 < b ^ L then eps else eps ^ (blockSize b L j + 1)) (b ^ L)
  rw [hrange, hd, Finset.sum_range_succ,
    ← Finset.sum_range_add_sum_Ico _ (Nat.le_add_right (blockSize b L j) d)]
  have hlow : ∑ x ∈ Finset.range (blockSize b L j),
      (if x < blockSize b L j then (1 : ℝ)
        else if x + 1 < blockSize b L j + d + 1 then eps
        else eps ^ (blockSize b L j + 1)) = (blockSize b L j : ℝ) := by
    rw [Finset.sum_congr rfl fun x hx => if_pos (Finset.mem_range.mp hx),
      Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one]
  have hmid : ∑ x ∈ Finset.Ico (blockSize b L j) (blockSize b L j + d),
      (if x < blockSize b L j then (1 : ℝ)
        else if x + 1 < blockSize b L j + d + 1 then eps
        else eps ^ (blockSize b L j + 1)) = (d : ℝ) * eps := by
    have hcongr : ∀ x ∈ Finset.Ico (blockSize b L j) (blockSize b L j + d),
        (if x < blockSize b L j then (1 : ℝ)
          else if x + 1 < blockSize b L j + d + 1 then eps
          else eps ^ (blockSize b L j + 1)) = eps := by
      intro x hx
      obtain ⟨h1, h2⟩ := Finset.mem_Ico.mp hx
      rw [if_neg (by omega), if_pos (by omega)]
    rw [Finset.sum_congr rfl hcongr, Finset.sum_const, Nat.card_Ico,
      Nat.add_sub_cancel_left, nsmul_eq_mul]
  have htop : (if blockSize b L j + d < blockSize b L j then (1 : ℝ)
      else if blockSize b L j + d + 1 < blockSize b L j + d + 1 then eps
      else eps ^ (blockSize b L j + 1)) = eps ^ (blockSize b L j + 1) := by
    rw [if_neg (by omega), if_neg (by omega)]
  rw [hlow, hmid, htop]

/-- The exact concave-envelope value of a level-`j` term on `[eps, 1]` (PB34):
`eps + (1-eps) u_j - (eps/m)(1 - eps ^ k)` with `u_j = 1 / blockCount b L j`,
`k = blockSize b L j` and `m = b ^ L`. -/
def termConcave (b L : ℕ) (eps : ℝ) (j : Fin L) : ℝ :=
  eps + (1 - eps) / (blockCount b L j : ℝ)
    - eps * (1 - eps ^ blockSize b L j) / (b : ℝ) ^ L

/-- Common-threshold rounding attains `termConcave`. -/
theorem thresholdRounding_expect (b L : ℕ) (hb : 0 < b) (eps : ℝ) (j : Fin L)
    (c : Fin (blockCount b L j)) (hk : blockSize b L j + 1 ≤ b ^ L) :
    (thresholdRounding b L hb).expect (fun v => eps ^ failCount (support b L j c) v)
      = termConcave b L eps j := by
  obtain ⟨d, hd⟩ : ∃ d, b ^ L = blockSize b L j + d + 1 :=
    ⟨b ^ L - blockSize b L j - 1, by omega⟩
  have hbR : (0 : ℝ) < (b : ℝ) := by exact_mod_cast hb
  have hpow : (0 : ℝ) < (b : ℝ) ^ L := by positivity
  have hcast : (b : ℝ) ^ L = (blockSize b L j : ℝ) + (d : ℝ) + 1 := by
    have := congrArg (fun n : ℕ => (n : ℝ)) hd
    push_cast at this
    exact this
  have hK : (0 : ℝ) < (blockSize b L j : ℝ) := by
    have : 0 < blockSize b L j := pow_pos hb _
    exact_mod_cast this
  have hmul : (blockCount b L j : ℝ) * (blockSize b L j : ℝ) = (b : ℝ) ^ L := by
    have := blockCount_mul_blockSize b L j
    exact_mod_cast congrArg (fun n : ℕ => (n : ℝ)) this
  have hBC : (blockCount b L j : ℝ) = (b : ℝ) ^ L / (blockSize b L j : ℝ) := by
    rw [← hmul]
    field_simp
  rw [thresholdRounding, uniformImage_expect, thresholdRounding_sum b L eps j c hd,
    Nat.cast_pow, termConcave, hBC, hcast]
  have hden : (blockSize b L j : ℝ) + (d : ℝ) + 1 ≠ 0 := by
    have : (0 : ℝ) ≤ (d : ℝ) := Nat.cast_nonneg d
    positivity
  field_simp
  ring

/-- Every law with the prescribed normalized means gives at most `termConcave`
(the upper half of PB34), by the dual certificate `term_dual_pointwise`. -/
theorem expect_term_le (b L : ℕ) (hb : 0 < b) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1)
    (μ : Law (Vertex (Coord b L))) (hμ : HasMeans μ (means b L))
    (j : Fin L) (c : Fin (blockCount b L j)) :
    μ.expect (fun v => eps ^ failCount (support b L j c) v) ≤ termConcave b L eps j := by
  have hK : (0 : ℝ) < (blockSize b L j : ℝ) := by
    have : 0 < blockSize b L j := pow_pos hb _
    exact_mod_cast this
  have hpt : ∀ v, (blockSize b L j : ℝ) * eps ^ failCount (support b L j c) v
      ≤ (blockSize b L j : ℝ) * (1 + (eps - 1) * ((anchorFail b L j v : ℕ) : ℝ))
        + eps * (eps ^ blockSize b L j - 1) * ((blockFails b L j c v : ℕ) : ℝ) := by
    intro v
    rw [failCount_support]
    exact term_dual_pointwise eps h0 h1 (anchorFail_le_one b L j v) (blockFails_le b L j c v)
  have hmono := μ.expect_mono hpt
  have hlhs : μ.expect (fun v => (blockSize b L j : ℝ) * eps ^ failCount (support b L j c) v)
      = (blockSize b L j : ℝ) * μ.expect (fun v => eps ^ failCount (support b L j c) v) :=
    Law.expect_const_mul μ _ _
  have he : (fun v => (blockSize b L j : ℝ) * (1 + (eps - 1) * ((anchorFail b L j v : ℕ) : ℝ))
        + eps * (eps ^ blockSize b L j - 1) * ((blockFails b L j c v : ℕ) : ℝ))
      = fun v => ((blockSize b L j : ℝ)
          + ((blockSize b L j : ℝ) * (eps - 1)) * ((anchorFail b L j v : ℕ) : ℝ))
        + (eps * (eps ^ blockSize b L j - 1)) * ((blockFails b L j c v : ℕ) : ℝ) := by
    funext v
    ring
  rw [hlhs, he, Law.expect_add, Law.expect_add, Law.expect_const, Law.expect_const_mul,
    Law.expect_const_mul, expect_anchorFail b L μ hμ j, expect_blockFails b L μ hμ j c] at hmono
  have hgoal : (blockSize b L j : ℝ) * termConcave b L eps j
      = ((blockSize b L j : ℝ)
          + (blockSize b L j : ℝ) * (eps - 1) * (1 - 1 / (blockCount b L j : ℝ)))
        + eps * (eps ^ blockSize b L j - 1) * ((blockSize b L j : ℝ) / (b : ℝ) ^ L) := by
    rw [termConcave]
    ring
  exact le_of_mul_le_mul_left (by rw [hgoal]; exact hmono) hK

/-! ## One-failure rounding and the convex envelope -/

/-- The binary point that fails exactly the leaf `t`, together with the anchors
that a threshold rule fails.  For the term `(j₀, c₀)` this gives exactly one
failed coordinate: the anchor fails precisely when the failed leaf misses the
block. -/
def singleFailVertex (b L : ℕ) (j₀ : Fin L) (c₀ : Fin (blockCount b L j₀))
    (t : Fin (b ^ L)) : Vertex (Coord b L) :=
  Sum.elim (fun j => if j = j₀ then decide (t ∈ block b L j₀ c₀)
      else decide ((t : ℕ) < blockSize b L j)) (fun i => decide (i ≠ t))

/-- The categorical law that fails exactly one uniformly random leaf. -/
def singleFailRounding (b L : ℕ) (hb : 0 < b) (j₀ : Fin L)
    (c₀ : Fin (blockCount b L j₀)) : Law (Vertex (Coord b L)) :=
  uniformImage (pow_pos hb L) (singleFailVertex b L j₀ c₀)

private theorem sum_mem_indicator {n : ℕ} (B : Finset (Fin n)) :
    ∑ t : Fin n, (if t ∈ B then (1 : ℝ) else 0) = (B.card : ℝ) := by
  rw [Finset.sum_boole]
  congr 1
  rw [Finset.filter_mem_eq_inter, Finset.univ_inter]

private theorem sum_ne_indicator {n : ℕ} (i : Fin n) :
    ∑ t : Fin n, (if i ≠ t then (1 : ℝ) else 0) = ((n - 1 : ℕ) : ℝ) := by
  rw [Finset.sum_boole]
  congr 2
  rw [Finset.filter_ne, Finset.card_erase_of_mem (Finset.mem_univ i), Finset.card_univ,
    Fintype.card_fin]

/-- One-failure rounding has the prescribed normalized means. -/
theorem singleFailRounding_hasMeans (b L : ℕ) (hb : 0 < b) (j₀ : Fin L)
    (c₀ : Fin (blockCount b L j₀)) :
    HasMeans (singleFailRounding b L hb j₀ c₀) (means b L) := by
  have hm : 1 ≤ b ^ L := Nat.one_le_pow _ _ hb
  intro i
  rw [singleFailRounding, uniformImage_expect]
  cases i with
  | inl j =>
      by_cases hj : j = j₀
      · subst hj
        have hval : ∀ t : Fin (b ^ L),
            vertexPoint (singleFailVertex b L j c₀ t) (Sum.inl j)
              = if t ∈ block b L j c₀ then (1 : ℝ) else 0 := by
          intro t
          by_cases h : t ∈ block b L j c₀ <;>
            simp [vertexPoint, singleFailVertex, h]
        rw [Finset.sum_congr rfl fun t _ => hval t, sum_mem_indicator, block_card]
        change (blockSize b L j : ℝ) / ((b ^ L : ℕ) : ℝ) = 1 / (blockCount b L j : ℝ)
        rw [Nat.cast_pow]
        exact blockSize_div_pow b L hb j
      · have hle : blockSize b L j ≤ b ^ L := by
          rw [blockSize]
          exact Nat.pow_le_pow_right hb (by omega)
        have hval : ∀ t : Fin (b ^ L),
            vertexPoint (singleFailVertex b L j₀ c₀ t) (Sum.inl j)
              = if (t : ℕ) < blockSize b L j then (1 : ℝ) else 0 := by
          intro t
          by_cases h : (t : ℕ) < blockSize b L j <;>
            simp [vertexPoint, singleFailVertex, hj, h]
        rw [Finset.sum_congr rfl fun t _ => hval t, sum_fin_lt_indicator _ _ hle]
        change (blockSize b L j : ℝ) / ((b ^ L : ℕ) : ℝ) = 1 / (blockCount b L j : ℝ)
        rw [Nat.cast_pow]
        exact blockSize_div_pow b L hb j
  | inr i =>
      have hval : ∀ t : Fin (b ^ L),
          vertexPoint (singleFailVertex b L j₀ c₀ t) (Sum.inr i)
            = if i ≠ t then (1 : ℝ) else 0 := by
        intro t
        by_cases h : i = t <;> simp [vertexPoint, singleFailVertex, h]
      rw [Finset.sum_congr rfl fun t _ => hval t, sum_ne_indicator]
      change ((b ^ L - 1 : ℕ) : ℝ) / ((b ^ L : ℕ) : ℝ) = 1 - 1 / (b : ℝ) ^ L
      have hbR : (0 : ℝ) < (b : ℝ) := by exact_mod_cast hb
      have hpos : (0 : ℝ) < (b : ℝ) ^ L := by positivity
      rw [Nat.cast_sub hm, Nat.cast_pow, Nat.cast_one]
      field_simp

/-- Under one-failure rounding the term `(j₀, c₀)` has exactly one failed
coordinate at every threshold index. -/
theorem failCount_singleFailVertex (b L : ℕ) (j₀ : Fin L) (c₀ : Fin (blockCount b L j₀))
    (t : Fin (b ^ L)) :
    failCount (support b L j₀ c₀) (singleFailVertex b L j₀ c₀ t) = 1 := by
  have hanchor : anchorFail b L j₀ (singleFailVertex b L j₀ c₀ t)
      = if t ∈ block b L j₀ c₀ then 0 else 1 := by
    by_cases h : t ∈ block b L j₀ c₀ <;> simp [anchorFail, singleFailVertex, h]
  have hblock : blockFails b L j₀ c₀ (singleFailVertex b L j₀ c₀ t)
      = if t ∈ block b L j₀ c₀ then 1 else 0 := by
    have hfilter : ((block b L j₀ c₀).filter
        fun i => singleFailVertex b L j₀ c₀ t (Sum.inr i) = false)
        = (block b L j₀ c₀).filter fun i => i = t := by
      apply Finset.filter_congr
      intro i _
      simp [singleFailVertex]
    rw [blockFails, hfilter, Finset.filter_eq']
    by_cases h : t ∈ block b L j₀ c₀ <;> simp [h]
  rw [failCount_support, hanchor, hblock]
  by_cases h : t ∈ block b L j₀ c₀ <;> simp [h]

/-- One-failure rounding attains the value `eps`. -/
theorem singleFailRounding_expect (b L : ℕ) (hb : 0 < b) (eps : ℝ) (j₀ : Fin L)
    (c₀ : Fin (blockCount b L j₀)) :
    (singleFailRounding b L hb j₀ c₀).expect
      (fun v => eps ^ failCount (support b L j₀ c₀) v) = eps := by
  have hbR : (0 : ℝ) < (b : ℝ) := by exact_mod_cast hb
  have hpos : ((b ^ L : ℕ) : ℝ) ≠ 0 := by
    rw [Nat.cast_pow]
    positivity
  rw [singleFailRounding, uniformImage_expect,
    Finset.sum_congr rfl fun t (_ : t ∈ Finset.univ) => by
      rw [failCount_singleFailVertex, pow_one],
    Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  field_simp

/-- Every law with the prescribed normalized means gives at least `eps` (the
lower half of PB33): the integer Jensen bound at `E R = 1`. -/
theorem expect_term_ge (b L : ℕ) (hb : 0 < b) (eps : ℝ) (h0 : 0 ≤ eps)
    (μ : Law (Vertex (Coord b L))) (hμ : HasMeans μ (means b L))
    (j : Fin L) (c : Fin (blockCount b L j)) :
    eps ≤ μ.expect (fun v => eps ^ failCount (support b L j c) v) := by
  have hpt : ∀ v, eps - eps * (1 - eps) * (((failCount (support b L j c) v : ℕ) : ℝ) - 1)
      ≤ eps ^ failCount (support b L j c) v := fun v => pow_ge_support_line eps h0 _
  have hmono := μ.expect_mono hpt
  have he : (fun v => eps - eps * (1 - eps) * (((failCount (support b L j c) v : ℕ) : ℝ) - 1))
      = fun v => (eps + eps * (1 - eps))
        - (eps * (1 - eps)) * ((failCount (support b L j c) v : ℕ) : ℝ) := by
    funext v
    ring
  rw [he, Law.expect_sub, Law.expect_const, Law.expect_const_mul,
    expect_failCount b L hb μ hμ j c] at hmono
  linarith [hmono]

/-! ## The exact envelopes on the box `[eps, 1]` -/

/-- A monomial read in cube coordinates of a box is separately affine. -/
theorem monomial_boxPoint_separatelyAffine {ι : Type*} [Finite ι] [DecidableEq ι]
    (l u : ι → ℝ) (s : Finset ι) :
    SeparatelyAffine (fun q => monomial s (boxPoint l u q)) := by
  have he : (fun q => monomial s (boxPoint l u q))
      = supportPolynomial s.powerset (boxExpansionCoefficient l u s) :=
    funext fun q => monomial_box_expansion l u q s
  rw [he]
  intro x i t
  exact supportPolynomial_coordinate_affine _ _ _ _ _

/-- The binary value of a term of the family on `[eps, 1]`. -/
theorem monomial_physVertex' (b L : ℕ) (s : Finset (Coord b L)) (eps : ℝ)
    (v : Vertex (Coord b L)) :
    monomial s (boxPoint (epsLower b L eps) (epsUpper b L) (vertexPoint v))
      = eps ^ failCount s v :=
  monomial_physVertex s eps v

/-- **PB33.** The exact convex-envelope value of every term of the family on
`[eps, 1]` at the prescribed physical means is `eps`. -/
theorem term_convex_envelope (b L : ℕ) (hb : 0 < b) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1)
    (j : Fin L) (c : Fin (blockCount b L j)) :
    IsLeast (boxEnvelopeValues (epsLower b L eps) (epsUpper b L)
      (monomial (support b L j c)) (physMeans b L eps)) eps := by
  rw [physMeans, boxEnvelopeValues_eq_of_mem _ _ (epsLower_le_epsUpper b L h1) _ _
    (means_mem_cube b L hb)]
  refine minimum_from_laws _ (monomial_boxPoint_separatelyAffine _ _ _) _ _ ?_ ?_
  · intro μ hμ
    simp only [monomial_physVertex']
    exact expect_term_ge b L hb eps h0 μ hμ j c
  · refine ⟨singleFailRounding b L hb j c, singleFailRounding_hasMeans b L hb j c, ?_⟩
    simp only [monomial_physVertex']
    exact singleFailRounding_expect b L hb eps j c

/-- **PB34.** The exact concave-envelope value of the level-`j` term of the
family on `[eps, 1]` at the prescribed physical means is `termConcave`. -/
theorem term_concave_envelope (b L : ℕ) (hb : 2 ≤ b) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1)
    (j : Fin L) (c : Fin (blockCount b L j)) :
    IsGreatest (boxEnvelopeValues (epsLower b L eps) (epsUpper b L)
      (monomial (support b L j c)) (physMeans b L eps)) (termConcave b L eps j) := by
  have hb0 : 0 < b := by omega
  rw [physMeans, boxEnvelopeValues_eq_of_mem _ _ (epsLower_le_epsUpper b L h1) _ _
    (means_mem_cube b L hb0)]
  refine maximum_from_laws _ (monomial_boxPoint_separatelyAffine _ _ _) _ _ ?_ ?_
  · intro μ hμ
    simp only [monomial_physVertex']
    exact expect_term_le b L hb0 eps h0 h1 μ hμ j c
  · refine ⟨thresholdRounding b L hb0, thresholdRounding_hasMeans b L hb0, ?_⟩
    simp only [monomial_physVertex']
    exact thresholdRounding_expect b L hb0 eps j c (blockSize_succ_le b L hb j)

/-- The exact envelope gap of one level-`j` term on `[eps, 1]`. -/
def termGap (b L : ℕ) (eps : ℝ) (j : Fin L) : ℝ :=
  (1 - eps) / (blockCount b L j : ℝ) - eps * (1 - eps ^ blockSize b L j) / (b : ℝ) ^ L

theorem termGap_eq_sub (b L : ℕ) (eps : ℝ) (j : Fin L) :
    termGap b L eps j = termConcave b L eps j - eps := by
  rw [termGap, termConcave]
  ring

/-- The exact hull gap of one term of the family on `[eps, 1]`. -/
theorem term_boxHullGap (b L : ℕ) (hb : 2 ≤ b) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1)
    (j : Fin L) (c : Fin (blockCount b L j)) :
    boxHullGap (epsLower b L eps) (epsUpper b L) (monomial (support b L j c))
      (physMeans b L eps) = termGap b L eps j := by
  have hb0 : 0 < b := by omega
  rw [boxHullGap, (term_concave_envelope b L hb eps h0 h1 j c).csSup_eq,
    (term_convex_envelope b L hb0 eps h0 h1 j c).csInf_eq, termGap_eq_sub]

/-! ## The family as a support polynomial, and the total termwise gap -/

/-- The supports of the family, one for every level and every block. -/
def termSupports (b L : ℕ) : Finset (Finset (Coord b L)) :=
  Finset.univ.image fun p : (j : Fin L) × Fin (blockCount b L j) => support b L p.1 p.2

theorem sum_termSupports (b L : ℕ) (hb : 0 < b) (g : Finset (Coord b L) → ℝ) :
    ∑ s ∈ termSupports b L, g s = ∑ j, ∑ c, g (support b L j c) := by
  rw [termSupports, Finset.sum_image fun p _ q _ h => support_injective b L hb h,
    ← Finset.univ_sigma_univ, Finset.sum_sigma]

/-- **PB32.** The family polynomial of `RadixFamily.lean` is the support
polynomial of `termSupports` with all coefficients one. -/
theorem supportPolynomial_termSupports (b L : ℕ) (hb : 0 < b) (x : Coord b L → ℝ) :
    supportPolynomial (termSupports b L) (fun _ => 1) x = polynomial b L x := by
  rw [supportPolynomial, sum_termSupports b L hb (fun s => (1 : ℝ) * monomial s x), polynomial]
  exact Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun c _ => one_mul _

/-- The correction term `D_L` of the source's equation (2). -/
def dCorrection (b L : ℕ) (eps : ℝ) : ℝ :=
  eps * ∑ t ∈ Finset.range L, (1 - eps ^ b ^ t) / (b : ℝ) ^ t

/-- The exact total termwise gap `T_L = (1 - eps) L - D_L` of the source's
equation (2). -/
def termwiseTotal (b L : ℕ) (eps : ℝ) : ℝ := (1 - eps) * (L : ℝ) - dCorrection b L eps

theorem sum_blockSize_reflect (b L : ℕ) (eps : ℝ) :
    ∑ j : Fin L, (1 - eps ^ blockSize b L j) / (blockSize b L j : ℝ)
      = ∑ t ∈ Finset.range L, (1 - eps ^ b ^ t) / (b : ℝ) ^ t := by
  have h1 : ∀ j : Fin L, (1 - eps ^ blockSize b L j) / (blockSize b L j : ℝ)
      = (fun x : ℕ => (1 - eps ^ b ^ (L - 1 - x)) / (b : ℝ) ^ (L - 1 - x)) (j : ℕ) := by
    intro j
    have hj : j.val < L := j.isLt
    have he : L - (j.val + 1) = L - 1 - j.val := by omega
    simp only [blockSize, he, Nat.cast_pow]
  calc ∑ j : Fin L, (1 - eps ^ blockSize b L j) / (blockSize b L j : ℝ)
      = ∑ j : Fin L, (fun x : ℕ => (1 - eps ^ b ^ (L - 1 - x)) / (b : ℝ) ^ (L - 1 - x))
          (j : ℕ) := Finset.sum_congr rfl fun j _ => h1 j
    _ = ∑ x ∈ Finset.range L,
          (fun x : ℕ => (1 - eps ^ b ^ (L - 1 - x)) / (b : ℝ) ^ (L - 1 - x)) x :=
        Fin.sum_univ_eq_sum_range
          (fun x : ℕ => (1 - eps ^ b ^ (L - 1 - x)) / (b : ℝ) ^ (L - 1 - x)) L
    _ = ∑ t ∈ Finset.range L, (1 - eps ^ b ^ t) / (b : ℝ) ^ t :=
        Finset.sum_range_reflect (fun t => (1 - eps ^ b ^ t) / (b : ℝ) ^ t) L

/-- **PB35.** The exact termwise gap of the family on `[eps, 1]`. -/
theorem radix_boxTermwiseGap (b L : ℕ) (hb : 2 ≤ b) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) :
    boxTermwiseGap (termSupports b L) (fun _ => 1) (epsLower b L eps) (epsUpper b L)
      (physMeans b L eps) = termwiseTotal b L eps := by
  have hb0 : 0 < b := by omega
  have hinner : ∀ j : Fin L, ∑ _c : Fin (blockCount b L j),
      (1 : ℝ) * boxHullGap (epsLower b L eps) (epsUpper b L)
        (monomial (support b L j _c)) (physMeans b L eps)
      = (1 - eps) - eps * ((1 - eps ^ blockSize b L j) / (blockSize b L j : ℝ)) := by
    intro j
    have hK : (0 : ℝ) < (blockSize b L j : ℝ) := by
      have : 0 < blockSize b L j := pow_pos hb0 _
      exact_mod_cast this
    have hBC : (0 : ℝ) < (blockCount b L j : ℝ) := by
      have : 0 < blockCount b L j := pow_pos hb0 _
      exact_mod_cast this
    have hmul : (blockCount b L j : ℝ) * (blockSize b L j : ℝ) = (b : ℝ) ^ L := by
      have := blockCount_mul_blockSize b L j
      exact_mod_cast congrArg (fun n : ℕ => (n : ℝ)) this
    have hc : ∀ c : Fin (blockCount b L j), (1 : ℝ) * boxHullGap (epsLower b L eps)
        (epsUpper b L) (monomial (support b L j c)) (physMeans b L eps)
        = termGap b L eps j := by
      intro c
      rw [one_mul, term_boxHullGap b L hb eps h0 h1 j c]
    rw [Finset.sum_congr rfl fun c _ => hc c, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul, termGap, ← hmul]
    field_simp
  rw [boxTermwiseGap, sum_termSupports b L hb0
      (fun s => (1 : ℝ) * boxHullGap (epsLower b L eps) (epsUpper b L) (monomial s)
        (physMeans b L eps)),
    Finset.sum_congr rfl fun j _ => hinner j, Finset.sum_sub_distrib, Finset.sum_const,
    Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, ← Finset.mul_sum,
    sum_blockSize_reflect, termwiseTotal, dCorrection]
  ring

theorem dCorrection_nonneg (b L : ℕ) (hb : 0 < b) (eps : ℝ) (h0 : 0 ≤ eps) (h1 : eps ≤ 1) :
    0 ≤ dCorrection b L eps := by
  have hbR : (0 : ℝ) < (b : ℝ) := by exact_mod_cast hb
  refine mul_nonneg h0 (Finset.sum_nonneg fun t _ => ?_)
  have hnum : (0 : ℝ) ≤ 1 - eps ^ b ^ t := by
    have := pow_le_one₀ h0 h1 (n := b ^ t)
    linarith
  positivity

/-- **PB35.** The uniform upper bound `D_L ≤ eps * b / (b - 1)`. -/
theorem dCorrection_le (b L : ℕ) (hb : 2 ≤ b) (eps : ℝ) (h0 : 0 ≤ eps) :
    dCorrection b L eps ≤ eps * (b : ℝ) / ((b : ℝ) - 1) := by
  have hbR : (2 : ℝ) ≤ (b : ℝ) := by exact_mod_cast hb
  have hb0 : (0 : ℝ) < (b : ℝ) := by linarith
  have hr : (0 : ℝ) < 1 - 1 / (b : ℝ) := by
    rw [sub_pos, div_lt_one hb0]
    linarith
  have hstep : ∑ t ∈ Finset.range L, (1 - eps ^ b ^ t) / (b : ℝ) ^ t
      ≤ ∑ t ∈ Finset.range L, (1 / (b : ℝ)) ^ t := by
    refine Finset.sum_le_sum fun t _ => ?_
    have hp : (0 : ℝ) < (b : ℝ) ^ t := by positivity
    have hnum : 1 - eps ^ b ^ t ≤ 1 := by
      have : (0 : ℝ) ≤ eps ^ b ^ t := by positivity
      linarith
    calc (1 - eps ^ b ^ t) / (b : ℝ) ^ t ≤ 1 / (b : ℝ) ^ t := by gcongr
      _ = (1 / (b : ℝ)) ^ t := by rw [div_pow, one_pow]
  have hkey : (1 - 1 / (b : ℝ)) * (∑ t ∈ Finset.range L, (1 / (b : ℝ)) ^ t)
      = 1 - (1 / (b : ℝ)) ^ L := by
    linear_combination -geom_sum_mul (1 / (b : ℝ)) L
  have hgeom : ∑ t ∈ Finset.range L, (1 / (b : ℝ)) ^ t ≤ (b : ℝ) / ((b : ℝ) - 1) := by
    have hpos : (0 : ℝ) ≤ (1 / (b : ℝ)) ^ L := by positivity
    have hbound : ∑ t ∈ Finset.range L, (1 / (b : ℝ)) ^ t ≤ 1 / (1 - 1 / (b : ℝ)) := by
      rw [le_div_iff₀ hr]
      nlinarith [hkey]
    have heq : 1 / (1 - 1 / (b : ℝ)) = (b : ℝ) / ((b : ℝ) - 1) := by
      field_simp
    linarith [hbound, heq.le, heq.ge]
  calc dCorrection b L eps
      = eps * ∑ t ∈ Finset.range L, (1 - eps ^ b ^ t) / (b : ℝ) ^ t := rfl
    _ ≤ eps * ((b : ℝ) / ((b : ℝ) - 1)) :=
        mul_le_mul_of_nonneg_left (le_trans hstep hgeom) h0
    _ = eps * (b : ℝ) / ((b : ℝ) - 1) := by ring

/-! ## Interface for the hull-gap side -/

/-- The family polynomial on `[eps, 1]` at a binary point: every term
contributes `eps` raised to its number of failed coordinates. -/
theorem polynomial_physVertex (b L : ℕ) (eps : ℝ) (v : Vertex (Coord b L)) :
    polynomial b L (boxPoint (epsLower b L eps) (epsUpper b L) (vertexPoint v))
      = ∑ j, ∑ c, eps ^ failCount (support b L j c) v := by
  rw [polynomial]
  exact Finset.sum_congr rfl fun j _ =>
    Finset.sum_congr rfl fun c _ => monomial_physVertex' b L _ eps v

/-- The family polynomial read in cube coordinates of `[eps, 1]` is separately
affine, so its graph hull on the box is the hull of its binary graph. -/
theorem polynomial_boxPoint_separatelyAffine (b L : ℕ) (hb : 0 < b) (eps : ℝ) :
    SeparatelyAffine
      (fun q => polynomial b L (boxPoint (epsLower b L eps) (epsUpper b L) q)) := by
  have he : (fun q => polynomial b L (boxPoint (epsLower b L eps) (epsUpper b L) q))
      = supportPolynomial (boxExpansionSupports (termSupports b L))
        (boxPolynomialCoefficient (termSupports b L) (fun _ => 1)
          (epsLower b L eps) (epsUpper b L)) := by
    funext q
    rw [← supportPolynomial_termSupports b L hb, supportPolynomial_box_expansion]
  rw [he]
  intro x i t
  exact supportPolynomial_coordinate_affine _ _ _ _ _

/-- The source's radix `b = L ^ 2` satisfies the standing hypothesis `2 ≤ b`. -/
theorem two_le_sq (L : ℕ) (hL : 2 ≤ L) : 2 ≤ L ^ 2 := by nlinarith

/-- The source's `eps = 1 / rho` with `rho > 1` is strictly inside `(0, 1)`. -/
theorem eps_mem_Ioo (rho : ℝ) (hrho : 1 < rho) : 0 < 1 / rho ∧ 1 / rho < 1 := by
  have h : (0 : ℝ) < rho := by linarith
  exact ⟨by positivity, (div_lt_one h).mpr hrho⟩

end
end Radix
end MultilinearGap
