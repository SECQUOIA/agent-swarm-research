import Formal.NetworkSimplex.ThresholdUnreducedCircuits

/-!
Exhaustive support certificates for all 2^14 subsets of the full three-dimensional
signed-subset universe. `supportMask_bits` checks that the first masks encode the
41 displayed supports. `separatorMask_bits` checks that the second masks encode
the strictly positive evaluations of 32 explicit integer vectors.

Each of the 64 blocks checks 256 supports by kernel reduction. The Boolean test
accepts exactly a contained circuit support or an enclosing strict-positive set.
`ThresholdUnreducedSupport` converts this finite certificate into a completeness
proof for arbitrary nonnegative real cancellations. No weight or support bound
is assumed by the exhaustive check.
-/

namespace NetworkSimplex.Threshold.UnreducedCircuits
open scoped BigOperators

def supportMask : Fin 41 → ℕ :=
  ![129, 258, 516, 1032, 2064, 4128, 8256, 515, 2057, 8225, 4106, 8210,
    8204, 388, 1168, 1312, 4288, 2368, 1600, 8203, 2337, 1569, 2593, 2625,
    4242, 1554, 4626, 4674, 4236, 2316, 6156, 8244, 4244, 8340, 2340, 8484,
    6216, 1584, 9264, 1472, 6720]

def separatorMask : Fin 32 → ℕ :=
  ![16256, 15240, 11176, 16002, 10922, 11938, 2794, 9144, 762, 11430, 2286, 254,
    13208, 1016, 15494, 3302, 16129, 13081, 889, 15367, 127, 3175, 14097, 4953,
    15621, 381, 7239, 1143, 13589, 4445, 5461, 5207]

theorem supportMask_bits : ∀ c i, (supportMask c).testBit i.val = decide (weight c i ≠ 0) := by
  decide +kernel

theorem separatorMask_bits : ∀ s i, (separatorMask s).testBit i.val =
    decide (0 < ∑ j, normal i j * separator s j) := by
  decide +kernel

def coverMaskBool (mask : ℕ) : Bool :=
  (List.finRange 41).any (fun c => mask &&& supportMask c == supportMask c) ||
    (List.finRange 32).any (fun s => mask &&& separatorMask s == mask)

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Split the 16384 supports into 64 blocks to bound kernel-reduction memory.
private theorem cover_blocks : ∀ b : Fin 64, ∀ r : Fin 256,
    coverMaskBool (b.val * 256 + r.val) = true := by
  intro b
  fin_cases b <;> decide +kernel

theorem cover_mask (mask : Fin 16384) : coverMaskBool mask.val = true := by
  have hb : mask.val / 256 < 64 := by omega
  have hr : mask.val % 256 < 256 := Nat.mod_lt _ (by decide)
  have hc := cover_blocks ⟨mask.val / 256, hb⟩ ⟨mask.val % 256, hr⟩
  have he : mask.val / 256 * 256 + mask.val % 256 = mask.val := by
    simpa only [Nat.mul_comm] using Nat.div_add_mod mask.val 256
  exact he ▸ hc

end NetworkSimplex.Threshold.UnreducedCircuits
