import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Convex.Deriv
import Mathlib.NumberTheory.Real.Irrational
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# The zero set of the explicit integer quartic

This standalone file verifies the zero set and irrationality statements in
`research-20260927/convex-quartic-irrational-zero.md`, and a rational
sum-of-squares certificate for a lower bound on every second directional
derivative. The certificate gives the constant 4096; the note's stronger
constant 4124 is not formalized here.
-/

namespace ConvexQuarticIrrationalZero

def quadratic (x y : ℝ) : ℝ :=
  12599 * x ^ 2 - 10000 * x * y + 7937 * y ^ 2 - 15874 * x - 12599 * y + 20000

def quartic (x y : ℝ) : ℝ :=
  quadratic x y ^ 2 + 10000 * ((x ^ 2 - y) ^ 2 + (y ^ 2 - 2 * x) ^ 2)

theorem quartic_nonneg (x y : ℝ) : 0 ≤ quartic x y := by
  unfold quartic
  positivity

theorem quartic_eq_zero_iff (x y : ℝ) :
    quartic x y = 0 ↔ x ^ 3 = 2 ∧ y = x ^ 2 := by
  constructor
  · intro h
    change quadratic x y ^ 2 +
      10000 * ((x ^ 2 - y) ^ 2 + (y ^ 2 - 2 * x) ^ 2) = 0 at h
    have hA : quadratic x y = 0 := by
      have hs : quadratic x y ^ 2 = 0 := by
        nlinarith only [h, sq_nonneg (quadratic x y), sq_nonneg (x ^ 2 - y),
          sq_nonneg (y ^ 2 - 2 * x)]
      exact sq_eq_zero_iff.mp hs
    have h1 : x ^ 2 - y = 0 := by
      have hs : (x ^ 2 - y) ^ 2 = 0 := by
        nlinarith only [h, sq_nonneg (quadratic x y), sq_nonneg (x ^ 2 - y),
          sq_nonneg (y ^ 2 - 2 * x)]
      exact sq_eq_zero_iff.mp hs
    have h2 : y ^ 2 - 2 * x = 0 := by
      have hs : (y ^ 2 - 2 * x) ^ 2 = 0 := by
        nlinarith only [h, sq_nonneg (quadratic x y), sq_nonneg (x ^ 2 - y),
          sq_nonneg (y ^ 2 - 2 * x)]
      exact sq_eq_zero_iff.mp hs
    have hy : y = x ^ 2 := by linarith only [h1]
    have hx : x ≠ 0 := by
      intro hx
      have hy0 : y = 0 := by simpa [hx] using hy
      norm_num [quadratic, hx, hy0] at hA
    rw [hy] at h2
    have hf : x * (x ^ 3 - 2) = 0 := by nlinarith only [h2]
    have hc : x ^ 3 - 2 = 0 := (mul_eq_zero.mp hf).resolve_left hx
    exact ⟨by linarith only [hc], hy⟩
  · rintro ⟨hx, rfl⟩
    have h4 : x ^ 4 = 2 * x := by
      calc
        x ^ 4 = x * x ^ 3 := by ring
        _ = 2 * x := by rw [hx]; ring
    have hA : quadratic x (x ^ 2) = 0 := by
      unfold quadratic
      nlinarith only [hx, h4]
    have h2 : (x ^ 2) ^ 2 - 2 * x = 0 := by nlinarith only [h4]
    simp [quartic, hA, h2]

theorem quartic_le_zero_iff (x y : ℝ) :
    quartic x y ≤ 0 ↔ x ^ 3 = 2 ∧ y = x ^ 2 := by
  rw [← quartic_eq_zero_iff]
  exact ⟨fun h => le_antisymm h (quartic_nonneg x y), fun h => h.le⟩

theorem cube_two_bounds {x : ℝ} (hx : x ^ 3 = 2) : 1 < x ∧ x < 2 := by
  have hm : StrictMono (fun t : ℝ => t ^ 3) := (by decide : Odd 3).strictMono_pow
  constructor
  · exact hm.lt_iff_lt.mp (by norm_num [hx])
  · exact hm.lt_iff_lt.mp (by norm_num [hx])

theorem cube_two_irrational {x : ℝ} (hx : x ^ 3 = 2) : Irrational x := by
  refine irrational_nrt_of_notint_nrt 3 2 hx ?_ (by norm_num)
  rintro ⟨z, rfl⟩
  obtain ⟨hlo, hhi⟩ := cube_two_bounds hx
  have hzlo : (1 : ℤ) < z := by exact_mod_cast hlo
  have hzhi : z < (2 : ℤ) := by exact_mod_cast hhi
  omega

theorem quartic_pos_at_rationals (x y : ℚ) : 0 < quartic x y := by
  have hn : quartic (x : ℝ) (y : ℝ) ≠ 0 := by
    intro h
    have hi := cube_two_irrational ((quartic_eq_zero_iff _ _).mp h).1
    exact hi.ne_rat x rfl
  exact lt_of_le_of_ne (quartic_nonneg x y) (Ne.symm hn)

noncomputable def cubeRootTwo : ℝ := (2 : ℝ) ^ ((3 : ℝ)⁻¹)

theorem cubeRootTwo_cube : cubeRootTwo ^ 3 = 2 := by
  exact Real.rpow_inv_natCast_pow (by norm_num : (0 : ℝ) ≤ 2) (by norm_num : (3 : ℕ) ≠ 0)

theorem quartic_zero_unique (x y : ℝ) :
    quartic x y = 0 ↔ x = cubeRootTwo ∧ y = cubeRootTwo ^ 2 := by
  rw [quartic_eq_zero_iff]
  constructor
  · rintro ⟨hx, hy⟩
    have hm : StrictMono (fun t : ℝ => t ^ 3) := (by decide : Odd 3).strictMono_pow
    have he : x = cubeRootTwo := hm.injective (hx.trans cubeRootTwo_cube.symm)
    exact ⟨he, by simpa [he] using hy⟩
  · rintro ⟨rfl, rfl⟩
    exact ⟨cubeRootTwo_cube, rfl⟩

theorem quartic_has_zero : ∃ x y : ℝ, quartic x y = 0 := by
  exact ⟨cubeRootTwo, cubeRootTwo ^ 2, (quartic_zero_unique _ _).mpr ⟨rfl, rfl⟩⟩

theorem quartic_has_no_rational_nonpositive_point :
    ¬ ∃ x y : ℚ, quartic x y ≤ 0 := by
  rintro ⟨x, y, h⟩
  exact (not_le_of_gt (quartic_pos_at_rationals x y)) h

def quadraticFirst (x y a b : ℝ) : ℝ :=
  (25198 * x - 10000 * y - 15874) * a + (-10000 * x + 15874 * y - 12599) * b

def quadraticSecond (a b : ℝ) : ℝ :=
  25198 * a ^ 2 - 20000 * a * b + 15874 * b ^ 2

def quarticFirst (x y a b : ℝ) : ℝ :=
  2 * quadratic x y * quadraticFirst x y a b +
    20000 * ((x ^ 2 - y) * (2 * x * a - b) + (y ^ 2 - 2 * x) * (2 * y * b - 2 * a))

def hessianForm (x y a b : ℝ) : ℝ :=
  2 * quadraticFirst x y a b ^ 2 + 2 * quadratic x y * quadraticSecond a b +
    20000 * ((2 * x * a - b) ^ 2 + (x ^ 2 - y) * (2 * a ^ 2) +
      (2 * y * b - 2 * a) ^ 2 + (y ^ 2 - 2 * x) * (2 * b ^ 2))

theorem quadratic_line_deriv (x y a b t : ℝ) :
    HasDerivAt (fun s => quadratic (x + s * a) (y + s * b))
      (quadraticFirst (x + t * a) (y + t * b) a b) t := by
  have hx := ((hasDerivAt_id t).mul_const a).const_add x
  have hy := ((hasDerivAt_id t).mul_const b).const_add y
  have h := ((((((hx.pow 2).const_mul 12599).sub ((hx.mul hy).const_mul 10000)).add
    ((hy.pow 2).const_mul 7937)).sub (hx.const_mul 15874)).sub
    (hy.const_mul 12599)).add_const 20000
  have hd := h.congr_deriv (g' := quadraticFirst (x + t * a) (y + t * b) a b)
    (by simp [quadraticFirst]; ring)
  simpa [quadratic, mul_assoc] using! hd

theorem quadraticFirst_line_deriv (x y a b t : ℝ) :
    HasDerivAt (fun s => quadraticFirst (x + s * a) (y + s * b) a b)
      (quadraticSecond a b) t := by
  have hx := ((hasDerivAt_id t).mul_const a).const_add x
  have hy := ((hasDerivAt_id t).mul_const b).const_add y
  have h := ((((hx.const_mul 25198).sub (hy.const_mul 10000)).sub_const 15874).mul_const a).add
    ((((hx.const_mul (-10000)).add (hy.const_mul 15874)).sub_const 12599).mul_const b)
  have hd := h.congr_deriv (g' := quadraticSecond a b)
    (by simp [quadraticSecond]; ring)
  simpa [quadraticFirst] using! hd

theorem quartic_line_deriv (x y a b t : ℝ) :
    HasDerivAt (fun s => quartic (x + s * a) (y + s * b))
      (quarticFirst (x + t * a) (y + t * b) a b) t := by
  have hx := ((hasDerivAt_id t).mul_const a).const_add x
  have hy := ((hasDerivAt_id t).mul_const b).const_add y
  have hA := quadratic_line_deriv x y a b t
  have hq1 := (hx.pow 2).sub hy
  have hq2 := (hy.pow 2).sub (hx.const_mul 2)
  have h := (hA.pow 2).add (((hq1.pow 2).add (hq2.pow 2)).const_mul 10000)
  have hd := h.congr_deriv (g' := quarticFirst (x + t * a) (y + t * b) a b)
    (by simp [quarticFirst]; ring)
  simpa [quartic] using! hd

theorem quarticFirst_line_deriv (x y a b t : ℝ) :
    HasDerivAt (fun s => quarticFirst (x + s * a) (y + s * b) a b)
      (hessianForm (x + t * a) (y + t * b) a b) t := by
  have hx := ((hasDerivAt_id t).mul_const a).const_add x
  have hy := ((hasDerivAt_id t).mul_const b).const_add y
  have hA := quadratic_line_deriv x y a b t
  have hDA := quadraticFirst_line_deriv x y a b t
  have hq1 := (hx.pow 2).sub hy
  have hq2 := (hy.pow 2).sub (hx.const_mul 2)
  have hdq1 := ((hx.const_mul 2).mul_const a).sub_const b
  have hdq2 := ((hy.const_mul 2).mul_const b).sub_const (2 * a)
  have h := ((hA.mul hDA).const_mul 2).add
    (((hq1.mul hdq1).add (hq2.mul hdq2)).const_mul 20000)
  have hd := h.congr_deriv (g' := hessianForm (x + t * a) (y + t * b) a b)
    (by simp [hessianForm]; ring)
  simpa [quarticFirst, mul_assoc] using! hd

theorem quartic_line_second_deriv (x y a b : ℝ) :
    deriv (deriv (fun t => quartic (x + t * a) (y + t * b))) 0 = hessianForm x y a b := by
  have h : deriv (fun t => quartic (x + t * a) (y + t * b)) =
      fun t => quarticFirst (x + t * a) (y + t * b) a b := by
    funext t
    exact (quartic_line_deriv x y a b t).deriv
  rw [h]
  simpa using (quarticFirst_line_deriv x y a b 0).deriv

noncomputable def hessianGapSOS (x y a b : ℝ) : ℝ :=
  let X := 100 * x - 126
  let Y := 100 * y - 1587 / 10
  let v0 := 2 * a - 2 * b
  let v1 := 2 * b
  let v2 := 2 * X * a - X * b - Y * a + Y * b
  let v3 := 2 * X * b + Y * a - Y * b
  let v4 := 2 * Y * a - Y * b
  let v5 := 2 * Y * b
  668373469360 * v0 ^ 2 + 125940547168 * v1 ^ 2 + 596786912600 * v2 ^ 2 +
    1117644940 * v3 ^ 2 + 36051115250 * v4 ^ 2 + 87368345585 * v5 ^ 2 +
    102427849072 * (v0 + v1) ^ 2 + 22618204800 * (v0 + v2) ^ 2 +
    13093175680 * (v0 - v3) ^ 2 + 5654551200 * (v0 + v4) ^ 2 +
    130053040 * (v0 - v5) ^ 2 + 22618204800 * (v1 + v2) ^ 2 +
    5643994880 * (v1 - v3) ^ 2 + 1929960800 * (v1 + v4) ^ 2 +
    3911932400 * (v1 - v5) ^ 2 + 78611522400 * (v2 + v3) ^ 2 +
    39305761200 * (v2 + v4) ^ 2 + 2034439000 * (v2 - v5) ^ 2 +
    15939729800 * (v3 - v4) ^ 2 + 13708914300 * (v3 - v5) ^ 2 +
    13144848050 * (v4 + v5) ^ 2

theorem hessian_sos_identity (x y a b : ℝ) :
    16000000 * (hessianForm x y a b - 4096 * (a ^ 2 + b ^ 2)) = hessianGapSOS x y a b := by
  unfold hessianForm quadratic quadraticFirst quadraticSecond hessianGapSOS
  ring

theorem hessianGapSOS_nonneg (x y a b : ℝ) : 0 ≤ hessianGapSOS x y a b := by
  unfold hessianGapSOS
  positivity

theorem hessianForm_lower_bound (x y a b : ℝ) :
    4096 * (a ^ 2 + b ^ 2) ≤ hessianForm x y a b := by
  have h := hessianGapSOS_nonneg x y a b
  rw [← hessian_sos_identity] at h
  nlinarith only [h]

theorem quartic_second_deriv_lower_bound (x y a b : ℝ) :
    4096 * (a ^ 2 + b ^ 2) ≤
      deriv (deriv (fun t => quartic (x + t * a) (y + t * b))) 0 := by
  rw [quartic_line_second_deriv]
  exact hessianForm_lower_bound x y a b

theorem quartic_line_convex (x y a b : ℝ) :
    ConvexOn ℝ Set.univ (fun t => quartic (x + t * a) (y + t * b)) := by
  have hd : deriv (fun t => quartic (x + t * a) (y + t * b)) =
      fun t => quarticFirst (x + t * a) (y + t * b) a b := by
    funext t
    exact (quartic_line_deriv x y a b t).deriv
  apply convexOn_univ_of_deriv2_nonneg
  · intro t
    exact (quartic_line_deriv x y a b t).differentiableAt
  · rw [hd]
    intro t
    exact (quarticFirst_line_deriv x y a b t).differentiableAt
  · intro t
    change 0 ≤ deriv (deriv (fun s => quartic (x + s * a) (y + s * b))) t
    rw [hd, (quarticFirst_line_deriv x y a b t).deriv]
    exact (by positivity : (0 : ℝ) ≤ 4096 * (a ^ 2 + b ^ 2)).trans
      (hessianForm_lower_bound (x + t * a) (y + t * b) a b)

theorem quartic_convex :
    ConvexOn ℝ Set.univ (fun p : ℝ × ℝ => quartic p.1 p.2) := by
  refine ⟨convex_univ, ?_⟩
  intro p _ q _ a b ha hb hab
  have hc := quartic_line_convex p.1 p.2 (q.1 - p.1) (q.2 - p.2)
  have h := hc.2 (x := 0) (by trivial) (y := 1) (by trivial) ha hb hab
  have he : a = 1 - b := by linarith only [hab]
  simp only [smul_eq_mul, mul_zero, mul_one, one_mul, zero_add, zero_mul, add_zero] at h
  change quartic (a * p.1 + b * q.1) (a * p.2 + b * q.2) ≤
    a * quartic p.1 p.2 + b * quartic q.1 q.2
  have h1 : p.1 + b * (q.1 - p.1) = a * p.1 + b * q.1 := by rw [he]; ring
  have h2 : p.2 + b * (q.2 - p.2) = a * p.2 + b * q.2 := by rw [he]; ring
  have h3 : p.1 + (q.1 - p.1) = q.1 := by ring
  have h4 : p.2 + (q.2 - p.2) = q.2 := by ring
  simpa only [h1, h2, h3, h4] using h

end ConvexQuarticIrrationalZero

#print axioms ConvexQuarticIrrationalZero.quartic_eq_zero_iff
#print axioms ConvexQuarticIrrationalZero.quartic_zero_unique
#print axioms ConvexQuarticIrrationalZero.quartic_has_zero
#print axioms ConvexQuarticIrrationalZero.quartic_has_no_rational_nonpositive_point
#print axioms ConvexQuarticIrrationalZero.quartic_second_deriv_lower_bound
#print axioms ConvexQuarticIrrationalZero.quartic_convex
