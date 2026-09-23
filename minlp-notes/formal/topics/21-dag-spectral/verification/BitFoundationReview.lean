import Formal.DAGSpectral.FactorBits
import Formal.DAGSpectral.NormalizationBits
import Formal.DAGSpectral.CharpolyBits
import Formal.DAGSpectral.EigenCompareBits

open DAGSpectral Matrix ReciprocalAnchor
open ReciprocalAnchor.ManyLeaf.BitCost
open scoped Matrix

#check rationalBits_finset_prod
#print axioms rationalLDLWithTrace_eq
#print axioms rationalLDL_bitWork_le
#print axioms ArithmeticExpr.run_eq
#print axioms ArithmeticExpr.eval_trace_bits
#print axioms determinantExpr_eval
#print axioms inverseEntryExpr_eval
#print axioms NormalizationBits.dyadicNormalization_bitWork_polynomial
#print axioms rationalCharpolyCoeff_eq
#print axioms rationalCharpolyCoeff_bits
#print axioms ratPolynomial_nonzero_root_bound
#print axioms coefficient_list_bisection_size

-- Extreme scales in both directions and the exact-window endpoint.
example : dyadicScale (1 / 64) 7 = 8 := by native_decide
example : dyadicScale 64 7 = 1 / 8 := by native_decide
example : dyadicScale 1 1 = 1 := by native_decide
example : (dyadicScaleTrace 1 1).length = 9 := by native_decide

-- The Schur trace includes the signed products and zero residual pivot.
example : rationalLDLTrace 2 !![(1 : ℚ), -2; -2, 4] =
    [(.compare,1,0), (.div,1,1), (.div,-2,1), (.mul,-2,-2),
      (.div,4,1), (.sub,4,4), (.compare,0,0)] := by native_decide
example : (rationalLDLTrace 2 !![(0 : ℚ), 0; 0, 3]).length = 3 := by native_decide

-- The expression interpreter uses the charged operands, including totalized division.
example : (ArithmeticExpr.op .div (.atom (-3 / 4)) (.atom 0)).run =
    (0, [(.div,-3/4,0)]) := by native_decide
example : (ArithmeticExpr.op .compare (.atom (-3 / 4)) (.atom 0)).run =
    (1, [(.compare,-3/4,0)]) := by native_decide
example : RationalBits ((-3 / 4 : ℚ) / 0) 3 := by
  unfold RationalBits
  native_decide
example : (determinantExpr (0 : Matrix (Fin 0) (Fin 0) ℚ)).run.1 = 1 := by native_decide
example : (determinantExpr !![(1 : ℚ), -2; -2, 4]).run.1 = 0 := by native_decide
example : (determinantExpr !![(1 : ℚ), -2; -2, 4]).run.2.length = 8 := by native_decide
example : (inverseEntryExpr !![(1 : ℚ), -2; -2, 4] 0 0).run.1 = 0 := by native_decide

-- Zero/repeated eigenvalue coefficients and out-of-degree coefficients.
example : (List.range 4).map (rationalCharpolyCoeff !![(0 : ℚ), 0; 0, 2]) =
    [0, -2, 1, 0] := by native_decide
example : (List.range 3).map (rationalCharpolyCoeff !![(2 : ℚ), 0; 0, 2]) =
    [4, -4, 1] := by native_decide

-- A zero constant coefficient and zero padding do not spoil the gap formula.
example : separationFromCoefficients [0, -1/2, 1] = 1/3 := by native_decide
example : separationFromCoefficients [0, -1/2, 1, 0, 0] = 1/3 := by native_decide
example : separationFromCoefficients [] = 1 := by native_decide
