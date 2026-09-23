import QipmFormal.ScalarCert.Inverse

/-!
# The scalar-dilation constant and the witness reduction

In the `v` coordinate the ratio `p⁻¹(y p'(y))/y` of `eq:cstar` is

  `ratio v = Y (W v) / Y v`,

because `p (Y u) = P u` and `P (W v) = Y v * A v`.  `cstar` is the supremum
of `ratio` over `(0,1)`.

The later module `Paper.lean` identifies this supremum with the manuscript's
definition using the inverse and derivative of `p` and the surjectivity of
`Y`. `Attainment.lean` supplies the attained maximum. Boundedness is proved
in `Final.lean` as `bddAbove_ratio`, so the final bounds carry no `BddAbove`
hypothesis; `lt_cstar_of_ratio` below takes one because it is used before
that proof is available.

`ratio_gt_of_witness` is the paper's lower-certificate argument: a pair
`(v, w)` with `a * Y v < Y w` and `P w < Y v * A v` forces `a < ratio v`.
It needs no boundedness hypothesis, hence no upper certificate.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-- The dilation ratio at `v`. -/
noncomputable def ratio (v : ℝ) : ℝ := Y (W v) / Y v

/-- The supremum of the dilation ratio, identified with the paper's `c⋆`
in `Paper.lean`. -/
noncomputable def cstar : ℝ := sSup (ratio '' Ioo 0 1)

/-- The lower-certificate reduction.  A strictly feasible witness `w` at `v`
forces the dilation ratio at `v` to exceed `a`. -/
theorem ratio_gt_of_witness {v w a : ℝ}
    (hv0 : 0 < v) (hv1 : v < 1) (hw0 : 0 < w) (hw1 : w < 1)
    (hY : a * Y v < Y w) (hP : P w < Y v * A v) :
    a < ratio v := by
  have hWmem : W v ∈ Ico (0:ℝ) 1 := W_mem hv0 hv1
  have hwmem : w ∈ Ico (0:ℝ) 1 := ⟨hw0.le, hw1⟩
  -- `P w < P (W v)` and `P` strictly monotone give `w < W v`
  have hPW : P (W v) = Y v * A v := P_W hv0 hv1
  have hlt : P w < P (W v) := by rw [hPW]; exact hP
  have hwW : w < W v := by
    rcases lt_trichotomy w (W v) with h | h | h
    · exact h
    · rw [h] at hlt; exact absurd hlt (lt_irrefl _)
    · exact absurd (P_strictMonoOn hWmem hwmem h) (not_lt.mpr hlt.le)
  -- `Y` strictly monotone
  have hYlt : Y w < Y (W v) := Y_strictMonoOn hwmem hWmem hwW
  have hYv : 0 < Y v := Y_pos hv0 hv1
  rw [ratio, lt_div_iff₀ hYv]
  linarith

/-- If the ratio family is bounded above, a witness bounds `cstar` from below. -/
theorem lt_cstar_of_ratio {v a : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (hbdd : BddAbove (ratio '' Ioo 0 1)) (h : a < ratio v) : a < cstar :=
  lt_of_lt_of_le h (le_csSup hbdd ⟨v, ⟨hv0, hv1⟩, rfl⟩)

end QipmFormal.ScalarCert
