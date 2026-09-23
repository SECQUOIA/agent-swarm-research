import Formal.DAGSpectral.EigenCompareExecutionCost
import Formal.DAGSpectral.PathInformationBits

open DAGSpectral Matrix
open scoped Matrix

def reviewIrrational : Matrix (Fin 2) (Fin 2) ℚ := !![2,1;1,1]
def reviewIrrationalPermuted : Matrix (Fin 2) (Fin 2) ℚ := !![1,1;1,2]
def reviewHalf : Matrix (Fin 2) (Fin 2) ℚ := !![1/2,0;0,2]
def reviewRepeated : Matrix (Fin 2) (Fin 2) ℚ := !![2,0;0,2]
def reviewSingularA : Matrix (Fin 2) (Fin 2) ℚ := !![1,0;0,0]
def reviewSingularB : Matrix (Fin 2) (Fin 2) ℚ := !![0,0;0,3]

#eval do
  unless rationalPSDTest !![(1 : ℚ),-1;-1,1] do
    throw (IO.userError "Singular PSD coefficient test failed")
  if rationalPSDTest !![(0 : ℚ),1;1,0] then
    throw (IO.userError "Indefinite symmetric matrix passed PSD test")
  unless eigenThresholdTest reviewRepeated 2 do
    throw (IO.userError "Threshold equality failed")
  if eigenThresholdTest reviewRepeated (2+1/1024) then
    throw (IO.userError "Threshold above the repeated minimum passed")
  unless decide (compareMinimumEigenvalues reviewIrrational reviewIrrationalPermuted = Ordering.eq) do
    throw (IO.userError "Equal irrational eigenvalues failed")
  unless decide (compareMinimumEigenvalues reviewIrrational reviewHalf = Ordering.lt) do
    throw (IO.userError "Irrational-versus-rational ordering failed")
  unless decide (compareMinimumEigenvalues reviewHalf reviewIrrational = Ordering.gt) do
    throw (IO.userError "Reverse ordering failed")
  unless decide (compareMinimumEigenvalues reviewSingularA reviewSingularB = Ordering.eq) do
    throw (IO.userError "Singular tie across different kernels failed")
  unless decide (compareMinimumEigenvalues !![(1 : ℚ)] !![1+(1/(2:ℚ)^80)] = Ordering.lt) do
    throw (IO.userError "Tiny positive gap failed")
  let run := compareMinimumEigenvaluesWithTrace reviewIrrational reviewIrrationalPermuted
  unless decide (run.1 = Ordering.eq ∧ run.2 = eigenComparisonExecutionTrace
      reviewIrrational reviewIrrationalPermuted) do
    throw (IO.userError "Instrumented equal-irrational run disagrees with full event trace")
  unless decide ((compareMinimumEigenvaluesWithTrace reviewHalf reviewIrrational).1 = Ordering.gt) do
    throw (IO.userError "Instrumented strict comparison failed")
  unless decide ((rationalSumRun [1/2,-1/3,5/6]).1 = 1 ∧
      (rationalSumRun [1/2,-1/3,5/6]).2.length = 3) do
    throw (IO.userError "Signed rational sum or addition count failed")
  let q0 : Matrix (Fin 2) (Fin 2) ℚ := 1
  let q : Fin 1 → Matrix (Fin 2) (Fin 2) ℚ := fun _ => !![1,-1;-1,1]
  let es : List (Fin 1) := List.replicate 10 0
  unless decide (rationalPathInformation q0 q es = !![11,-10;-10,11] ∧
      (rationalPathEntryRun q0 q es 0 1).1 = -10 ∧
      (rationalPathEntryRun q0 q es 0 1).2.length = 11) do
    throw (IO.userError "Longer signed matrix sum lost linear addition count")
  IO.println s!"Thirteen exact-criteria and path-sum checks passed; equal-irrational trace has {run.2.length} events."

#print axioms posSemidef_iff_charpoly_neg_coeff_nonneg
#print axioms rationalPSDTest_correct
#print axioms minimumEigenvalue_difference_root
#print axioms compareMinimumEigenvalues_correct
#print axioms compareMinimumEigenvaluesWithTrace_eq
#print axioms compareMinimumEigenvaluesWithTrace_correct
#print axioms eigenComparisonDepth_linear
#print axioms rationalPathInformation_bits
#print axioms rationalPathBitWork_le
#print axioms eigenComparisonExecutionTrace_bits
#print axioms eigenComparisonExecutionTrace_length
#print axioms compareMinimumEigenvalues_polynomial_bitWork
