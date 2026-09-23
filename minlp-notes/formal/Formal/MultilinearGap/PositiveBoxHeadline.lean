import Formal.MultilinearGap.CommonAspectBound
import Formal.MultilinearGap.BilinearGraph
import Formal.MultilinearGap.RadixHullGap

/-!
# The positive-box headline bounds

This module assembles the two-sided bound on `C_box(rho)`, the supremum of the
termwise-to-hull gap ratio over strictly positive boxes of aspect ratio at most
`rho` (`boxAspectSupremum`, defined in `PositiveBox.lean`).

* PB45: `max 2 rho ≤ C_box rho ≤ rho + 2` for every `rho > 1`.
* PB46: `C_box rho = rho + O(1)`, in the explicit form `0 ≤ C_box rho - rho ≤ 2`,
  together with `C_box 2 ≤ 4`.

Every ingredient is proved elsewhere: the upper bound is
`positiveBoxAspectBound_add_two` (PB22/PB25), the `rho` branch of the lower bound
is `Radix.rho_le_boxAspectSupremum` (PB43) and the `2` branch is
`two_le_boxAspectSupremum` (PB44). Boundedness of the ratio class — required
before any supremum statement is meaningful, since `sSup` of an unbounded set is
junk — is supplied by `boxAspectRatios_bddAbove` applied to the upper bound, so
both lower bounds are used here in their unconditional form.

**Not claimed**, per the exclusions of the topic's obligation inventory: that
either endpoint is the exact value of `C_box rho` at any fixed `rho`.
-/

namespace MultilinearGap

/-- The ratio class is bounded above, from the `rho + 2` bound. This is what
makes every supremum statement below meaningful rather than junk. -/
theorem boxAspectRatios_bddAbove_of_lt {rho : ℝ} (hrho : 1 < rho) :
    BddAbove (boxAspectRatios rho) :=
  boxAspectRatios_bddAbove (positiveBoxAspectBound_add_two hrho)

/-- PB45, upper half: `C_box rho ≤ rho + 2`. -/
theorem boxAspectSupremum_le_add_two {rho : ℝ} (hrho : 1 < rho) :
    boxAspectSupremum rho ≤ rho + 2 :=
  boxAspectSupremum_le hrho (positiveBoxAspectBound_add_two hrho)

/-- PB45, lower half: `max 2 rho ≤ C_box rho`. -/
theorem le_boxAspectSupremum {rho : ℝ} (hrho : 1 < rho) :
    max 2 rho ≤ boxAspectSupremum rho :=
  max_le (two_le_boxAspectSupremum hrho (boxAspectRatios_bddAbove_of_lt hrho))
    (Radix.rho_le_boxAspectSupremum hrho (boxAspectRatios_bddAbove_of_lt hrho))

/-- **PB45.** `max {2, rho} ≤ C_box rho ≤ rho + 2` for every `rho > 1`. -/
theorem positiveBox_headline {rho : ℝ} (hrho : 1 < rho) :
    max 2 rho ≤ boxAspectSupremum rho ∧ boxAspectSupremum rho ≤ rho + 2 :=
  ⟨le_boxAspectSupremum hrho, boxAspectSupremum_le_add_two hrho⟩

/-- **PB46**, the asymptotic form: `C_box rho - rho` is trapped in `[0, 2]` for
every `rho > 1`, so `C_box rho = rho + O(1)` as `rho → ∞`. -/
theorem boxAspectSupremum_sub_mem {rho : ℝ} (hrho : 1 < rho) :
    0 ≤ boxAspectSupremum rho - rho ∧ boxAspectSupremum rho - rho ≤ 2 := by
  refine ⟨by linarith [le_max_right (2 : ℝ) rho, le_boxAspectSupremum hrho], ?_⟩
  linarith [boxAspectSupremum_le_add_two hrho]

/-- **PB46**, the numeric specialization: `C_box 2 ≤ 4`. -/
theorem boxAspectSupremum_two_le_four : boxAspectSupremum 2 ≤ 4 := by
  have := boxAspectSupremum_le_add_two (rho := 2) (by norm_num)
  linarith

/-- The common-aspect ratio class is bounded above too, by the inclusion of PB02.
Without this, `two_le_commonAspectBoxSupremum` and `rho_le_commonAspectBoxSupremum`
would remain permanently conditional. -/
theorem commonAspectBoxRatios_bddAbove_of_lt {rho : ℝ} (hrho : 1 < rho) :
    BddAbove (commonAspectBoxRatios rho) :=
  (boxAspectRatios_bddAbove_of_lt hrho).mono
    (commonAspectBoxRatios_subset_boxAspectRatios hrho.le)

/-- PB45 for the common-aspect class, unconditionally. -/
theorem le_commonAspectBoxSupremum {rho : ℝ} (hrho : 1 < rho) :
    max 2 rho ≤ commonAspectBoxSupremum rho :=
  max_le (two_le_commonAspectBoxSupremum hrho (commonAspectBoxRatios_bddAbove_of_lt hrho))
    (Radix.rho_le_commonAspectBoxSupremum hrho (commonAspectBoxRatios_bddAbove_of_lt hrho))

end MultilinearGap
