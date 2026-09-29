import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# The ternary quartic: a zero and a global curvature certificate

This standalone file checks the polynomial in
`research-20260927/ternary-rational-sos-convex-counterexample.md`.
It proves its zero at `(a^4/2, a, a^2/2)` when `a^5 = 2`, and the
lower bound `a^2+b^2+c^2` on its actual second derivative along any
affine line with direction `(a,b,c)`. The rational weighted-square
identity is checked by Lean's ring tactic; its external generation is
not a trusted assumption. No field-theoretic SOS obstruction is proved.
-/

namespace TernarySOSDescent

set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

def r0 (x y _z : ℝ) : ℝ := 2 - 2 * x * y
def r1 (x y z : ℝ) : ℝ := 2 * x ^ 2 - 2 * y * z
def r2 (_x y z : ℝ) : ℝ := 2 * y ^ 2 - 4 * z
def r3 (x _y z : ℝ) : ℝ := 2 * z ^ 2 - x
def r4 (x y z : ℝ) : ℝ := 2 * x * z - y

def exposing (x y z : ℝ) : ℝ :=
  4 * r0 x y z + 5 * r1 x y z + 3 * r2 x y z + 9 * r3 x y z

def quartic (x y z : ℝ) : ℝ :=
  exposing x y z ^ 2 + r0 x y z ^ 2 + r1 x y z ^ 2 +
    r2 x y z ^ 2 + r3 x y z ^ 2 - r4 x y z ^ 2

theorem residuals_at_fifth_root {a : ℝ} (ha : a ^ 5 = 2) :
    r0 (a ^ 4 / 2) a (a ^ 2 / 2) = 0 ∧
    r1 (a ^ 4 / 2) a (a ^ 2 / 2) = 0 ∧
    r2 (a ^ 4 / 2) a (a ^ 2 / 2) = 0 ∧
    r3 (a ^ 4 / 2) a (a ^ 2 / 2) = 0 ∧
    r4 (a ^ 4 / 2) a (a ^ 2 / 2) = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · calc
      r0 (a ^ 4 / 2) a (a ^ 2 / 2) = 2 - a ^ 5 := by unfold r0; ring
      _ = 0 := by rw [ha]; ring
  · calc
      r1 (a ^ 4 / 2) a (a ^ 2 / 2) = (a ^ 5 - 2) * a ^ 3 / 2 := by unfold r1; ring
      _ = 0 := by rw [ha]; ring
  · unfold r2
    ring
  · unfold r3
    ring
  · calc
      r4 (a ^ 4 / 2) a (a ^ 2 / 2) = (a ^ 5 - 2) * a / 2 := by unfold r4; ring
      _ = 0 := by rw [ha]; ring

theorem quartic_zero_at_fifth_root {a : ℝ} (ha : a ^ 5 = 2) :
    quartic (a ^ 4 / 2) a (a ^ 2 / 2) = 0 := by
  obtain ⟨h0, h1, h2, h3, h4⟩ := residuals_at_fifth_root ha
  simp [quartic, exposing, h0, h1, h2, h3, h4]

def d0 (x y _z a b _c : ℝ) : ℝ := -2 * (a * y + x * b)
def d1 (x y z a b c : ℝ) : ℝ := 4 * x * a - 2 * (b * z + y * c)
def d2 (_x y _z _a b c : ℝ) : ℝ := 4 * y * b - 4 * c
def d3 (_x _y z a _b c : ℝ) : ℝ := 4 * z * c - a
def d4 (x _y z a b c : ℝ) : ℝ := 2 * (a * z + x * c) - b

def exposingFirst (x y z a b c : ℝ) : ℝ :=
  4 * d0 x y z a b c + 5 * d1 x y z a b c +
    3 * d2 x y z a b c + 9 * d3 x y z a b c

def exposingQuadratic (a b c : ℝ) : ℝ :=
  -8 * a * b + 10 * a ^ 2 - 10 * b * c + 6 * b ^ 2 + 18 * c ^ 2

def squareAlong (q d e t : ℝ) : ℝ := (q + t * d + t ^ 2 * e) ^ 2

def squareAlongFirst (q d e t : ℝ) : ℝ :=
  2 * (q + t * d + t ^ 2 * e) * (d + 2 * t * e)

def squareCurvature (q d e : ℝ) : ℝ := 2 * d ^ 2 + 4 * q * e

theorem squareAlong_hasDerivAt (q d e t : ℝ) :
    HasDerivAt (fun s => squareAlong q d e s) (squareAlongFirst q d e t) t := by
  have hi := hasDerivAt_id t
  have h := (((hi.mul_const d).const_add q).add ((hi.pow 2).mul_const e)).pow 2
  have hd := h.congr_deriv (g' := squareAlongFirst q d e t)
    (by simp [squareAlongFirst])
  simpa [squareAlong] using! hd

theorem squareAlongFirst_hasDerivAt_zero (q d e : ℝ) :
    HasDerivAt (fun s => squareAlongFirst q d e s) (squareCurvature q d e) 0 := by
  have hi := hasDerivAt_id (0 : ℝ)
  have hq := ((hi.mul_const d).const_add q).add ((hi.pow 2).mul_const e)
  have hd := (((hi.const_mul 2).mul_const e).const_add d)
  have h := (hq.mul hd).const_mul 2
  have h' := h.congr_deriv (g' := squareCurvature q d e)
    (by simp [squareCurvature]; ring)
  simpa [squareAlongFirst, mul_assoc] using! h'

def quarticLineFirst (x y z a b c t : ℝ) : ℝ :=
  squareAlongFirst (exposing x y z) (exposingFirst x y z a b c)
      (exposingQuadratic a b c) t +
    squareAlongFirst (r0 x y z) (d0 x y z a b c) (-2 * a * b) t +
    squareAlongFirst (r1 x y z) (d1 x y z a b c) (2 * a ^ 2 - 2 * b * c) t +
    squareAlongFirst (r2 x y z) (d2 x y z a b c) (2 * b ^ 2) t +
    squareAlongFirst (r3 x y z) (d3 x y z a b c) (2 * c ^ 2) t -
    squareAlongFirst (r4 x y z) (d4 x y z a b c) (2 * a * c) t

def hessianForm (x y z a b c : ℝ) : ℝ :=
  squareCurvature (exposing x y z) (exposingFirst x y z a b c)
      (exposingQuadratic a b c) +
    squareCurvature (r0 x y z) (d0 x y z a b c) (-2 * a * b) +
    squareCurvature (r1 x y z) (d1 x y z a b c) (2 * a ^ 2 - 2 * b * c) +
    squareCurvature (r2 x y z) (d2 x y z a b c) (2 * b ^ 2) +
    squareCurvature (r3 x y z) (d3 x y z a b c) (2 * c ^ 2) -
    squareCurvature (r4 x y z) (d4 x y z a b c) (2 * a * c)

theorem quartic_line_hasDerivAt (x y z a b c t : ℝ) :
    HasDerivAt (fun s => quartic (x + s * a) (y + s * b) (z + s * c))
      (quarticLineFirst x y z a b c t) t := by
  have h := (((((squareAlong_hasDerivAt (exposing x y z)
    (exposingFirst x y z a b c) (exposingQuadratic a b c) t).add
    (squareAlong_hasDerivAt (r0 x y z) (d0 x y z a b c) (-2 * a * b) t)).add
    (squareAlong_hasDerivAt (r1 x y z) (d1 x y z a b c) (2 * a ^ 2 - 2 * b * c) t)).add
    (squareAlong_hasDerivAt (r2 x y z) (d2 x y z a b c) (2 * b ^ 2) t)).add
    (squareAlong_hasDerivAt (r3 x y z) (d3 x y z a b c) (2 * c ^ 2) t)).sub
    (squareAlong_hasDerivAt (r4 x y z) (d4 x y z a b c) (2 * a * c) t)
  convert! h using 1
  · ext s
    simp only [Pi.add_apply, Pi.sub_apply]
    unfold quartic squareAlong exposing exposingFirst exposingQuadratic r0 r1 r2 r3 r4 d0 d1 d2 d3 d4
    ring

theorem quarticLineFirst_hasDerivAt_zero (x y z a b c : ℝ) :
    HasDerivAt (fun s => quarticLineFirst x y z a b c s) (hessianForm x y z a b c) 0 := by
  exact (((((squareAlongFirst_hasDerivAt_zero (exposing x y z)
    (exposingFirst x y z a b c) (exposingQuadratic a b c)).add
    (squareAlongFirst_hasDerivAt_zero (r0 x y z) (d0 x y z a b c) (-2 * a * b))).add
    (squareAlongFirst_hasDerivAt_zero (r1 x y z) (d1 x y z a b c) (2 * a ^ 2 - 2 * b * c))).add
    (squareAlongFirst_hasDerivAt_zero (r2 x y z) (d2 x y z a b c) (2 * b ^ 2))).add
    (squareAlongFirst_hasDerivAt_zero (r3 x y z) (d3 x y z a b c) (2 * c ^ 2))).sub
    (squareAlongFirst_hasDerivAt_zero (r4 x y z) (d4 x y z a b c) (2 * a * c))

theorem quartic_stationary_at_fifth_root {a : ℝ} (ha : a ^ 5 = 2) (b c d : ℝ) :
    deriv (fun t => quartic (a ^ 4 / 2 + t * b) (a + t * c) (a ^ 2 / 2 + t * d)) 0 = 0 := by
  rw [(quartic_line_hasDerivAt (a ^ 4 / 2) a (a ^ 2 / 2) b c d 0).deriv]
  obtain ⟨h0, h1, h2, h3, h4⟩ := residuals_at_fifth_root ha
  simp [quarticLineFirst, squareAlongFirst, exposing, h0, h1, h2, h3, h4]

theorem quartic_line_second_deriv (x y z a b c : ℝ) :
    deriv (deriv (fun t => quartic (x + t * a) (y + t * b) (z + t * c))) 0 =
      hessianForm x y z a b c := by
  have h : deriv (fun t => quartic (x + t * a) (y + t * b) (z + t * c)) =
      fun t => quarticLineFirst x y z a b c t := by
    funext t
    exact (quartic_line_hasDerivAt x y z a b c t).deriv
  rw [h]
  exact (quarticLineFirst_hasDerivAt_zero x y z a b c).deriv

noncomputable def hessianGapSOS (x y z a b c : ℝ) : ℝ :=
  let Z0 := a
  let Z1 := b
  let Z2 := c
  let Z3 := (x - 3 / 4) * a
  let Z4 := (x - 3 / 4) * b
  let Z5 := (x - 3 / 4) * c
  let Z6 := (y - 1) * a
  let Z7 := (y - 1) * b
  let Z8 := (y - 1) * c
  let Z9 := (z - 1 / 2) * a
  let Z10 := (z - 1 / 2) * b
  let Z11 := (z - 1 / 2) * c
  let W0 := 49 * Z0 - 10 * Z1 - 2 * Z2 - 84 * Z3 + 60 * Z4 - 6 * Z5 + 56 * Z6 - 53 * Z7 + 30 * Z8 - 92 * Z9 + 60 * Z10 - 155 * Z11
  let W1 := 4357 * Z1 - 4058 * Z2 + 3416 * Z3 - 2132 * Z4 + 1644 * Z5 - 350 * Z6 + 7172 * Z7 - 1752 * Z8 + 1688 * Z9 - 6640 * Z10 + 8268 * Z11
  let W2 := 530263 * Z2 - 1298068 * Z3 + 524468 * Z4 - 580532 * Z5 + 566056 * Z6 - 609996 * Z7 + 946112 * Z8 + 28646 * Z9 + 621688 * Z10 - 2925716 * Z11
  let W3 := 377023825 * Z3 - 112813848 * Z4 - 98906464 * Z5 - 117814520 * Z6 + 121113432 * Z7 - 44950168 * Z8 - 86523748 * Z9 - 45270752 * Z10 + 149659432 * Z11
  let W4 := 63225558167 * Z4 - 68755466744 * Z5 + 1112206080 * Z6 - 18742362628 * Z7 + 23286938872 * Z8 + 26016744492 * Z9 - 16111568992 * Z10 + 26998735172 * Z11
  let W5 := 24263050990949 * Z5 + 1532862818140 * Z6 - 1573246752514 * Z7 - 7194118258436 * Z8 + 383777028464 * Z9 + 2665067422760 * Z10 - 16848192623182 * Z11
  let W6 := 4133378376865537 * Z6 - 1771291768981972 * Z7 - 291438331563144 * Z8 - 3823100225067312 * Z9 + 1485796033865664 * Z10 + 1700900955055588 * Z11
  let W7 := 411989869164269610 * Z7 - 579534488163316986 * Z8 - 158470836678986192 * Z9 - 238774522080319484 * Z10 + 903404763509246445 * Z11
  let W8 := 10646884634267829927 * Z8 - 3482919609730315736 * Z9 + 4246495491274006828 * Z10 - 7654178283860930775 * Z11
  let W9 := 3070518842750230092439 * Z9 - 1075070384904935916856 * Z10 - 1635416472911750314176 * Z11
  let W10 := 2186318040815874179080883 * Z10 - 1791040772377325963641002 * Z11
  let W11 := Z11
  (1 / 49) * W0 ^ 2 +
  (1 / 426986) * W1 ^ 2 +
  (1 / 4620711782) * W2 ^ 2 +
  (1 / 199921784515975) * W3 ^ 2 +
  (1 / 23837541777882328775) * W4 ^ 2 +
  (1 / 1534044941737132990030483) * W5 ^ 2 +
  (1 / 100288370322774536684377024613) * W6 ^ 2 +
  (1 / 1702910016691253673194787785430570) * W7 ^ 2 +
  (1 / 731068101246512624854196436775769745) * W8 ^ 2 +
  (1 / 32691459886107263908659107287217140621953) * W9 ^ 2 +
  (1 / 20139392221709724916294440461543790279443230911) * W10 ^ 2 +
  (1202961604425506259443507567 / 4372636081631748358161766) * W11 ^ 2 +
  Z3 ^ 2 +
  Z4 ^ 2 +
  Z5 ^ 2 +
  Z6 ^ 2 +
  Z7 ^ 2 +
  Z8 ^ 2 +
  Z9 ^ 2 +
  Z10 ^ 2 +
  Z11 ^ 2

theorem hessian_sos_identity (x y z a b c : ℝ) :
    hessianForm x y z a b c - (a ^ 2 + b ^ 2 + c ^ 2) =
      hessianGapSOS x y z a b c := by
  unfold hessianForm squareCurvature exposing exposingFirst exposingQuadratic
    r0 r1 r2 r3 r4 d0 d1 d2 d3 d4 hessianGapSOS
  ring

theorem hessianGapSOS_nonneg (x y z a b c : ℝ) :
    0 ≤ hessianGapSOS x y z a b c := by
  unfold hessianGapSOS
  positivity

theorem hessianForm_lower_bound (x y z a b c : ℝ) :
    a ^ 2 + b ^ 2 + c ^ 2 ≤ hessianForm x y z a b c := by
  have h := hessianGapSOS_nonneg x y z a b c
  rw [← hessian_sos_identity] at h
  linarith only [h]

theorem quartic_second_deriv_lower_bound (x y z a b c : ℝ) :
    a ^ 2 + b ^ 2 + c ^ 2 ≤
      deriv (deriv (fun t => quartic (x + t * a) (y + t * b) (z + t * c))) 0 := by
  rw [quartic_line_second_deriv]
  exact hessianForm_lower_bound x y z a b c


end TernarySOSDescent

#print axioms TernarySOSDescent.quartic_zero_at_fifth_root
#print axioms TernarySOSDescent.quartic_stationary_at_fifth_root
#print axioms TernarySOSDescent.quartic_line_second_deriv
#print axioms TernarySOSDescent.hessian_sos_identity
#print axioms TernarySOSDescent.hessianGapSOS_nonneg
#print axioms TernarySOSDescent.quartic_second_deriv_lower_bound
