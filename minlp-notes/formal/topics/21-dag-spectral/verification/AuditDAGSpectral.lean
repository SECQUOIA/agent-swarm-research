import Formal.DAGSpectral.AlgorithmBitCost
import Formal.DAGSpectral.BasisInputExecution
import Formal.DAGSpectral.BitComplexity
import Formal.DAGSpectral.CacheStorageExecution
import Formal.DAGSpectral.CharpolyBits
import Formal.DAGSpectral.CoverBitCost
import Formal.DAGSpectral.CoverCacheCost
import Formal.DAGSpectral.CoverCardinality
import Formal.DAGSpectral.CoverCorrectness
import Formal.DAGSpectral.CoverEnumerationCost
import Formal.DAGSpectral.CoverExecution
import Formal.DAGSpectral.CoverIndependenceExecution
import Formal.DAGSpectral.CoverInputExecution
import Formal.DAGSpectral.CoverLabelCost
import Formal.DAGSpectral.CoverLoopCost
import Formal.DAGSpectral.CoverNormalizationExecution
import Formal.DAGSpectral.CoverPolynomialCost
import Formal.DAGSpectral.CoverProducer
import Formal.DAGSpectral.CoverSizePolynomial
import Formal.DAGSpectral.CoverWholeExecution
import Formal.DAGSpectral.Criteria
import Formal.DAGSpectral.CriteriaBasic
import Formal.DAGSpectral.CriteriaCost
import Formal.DAGSpectral.CriteriaEigen
import Formal.DAGSpectral.CriterionSelect
import Formal.DAGSpectral.CriterionSelectContrast
import Formal.DAGSpectral.CriterionSelectContrastPath
import Formal.DAGSpectral.CriterionSelectContrastTrace
import Formal.DAGSpectral.CriterionSelectCostTrace
import Formal.DAGSpectral.CriterionSelectEigenTrace
import Formal.DAGSpectral.CriterionSelectHeadline
import Formal.DAGSpectral.CriterionSelectMatrix
import Formal.DAGSpectral.CriterionSelectMatrixTrace
import Formal.DAGSpectral.CriterionSelectPath
import Formal.DAGSpectral.CriterionSelectTrace
import Formal.DAGSpectral.CriterionSelectWeighted
import Formal.DAGSpectral.CriterionSelectWeightedPath
import Formal.DAGSpectral.CriterionSelectWeightedScan
import Formal.DAGSpectral.CriterionSelectWeightedTrace
import Formal.DAGSpectral.Determinant
import Formal.DAGSpectral.DyadicScale
import Formal.DAGSpectral.DyadicScaleBits
import Formal.DAGSpectral.EigenCompare
import Formal.DAGSpectral.EigenCompareBisection
import Formal.DAGSpectral.EigenCompareBits
import Formal.DAGSpectral.EigenCompareCoefficientTrace
import Formal.DAGSpectral.EigenCompareComplexity
import Formal.DAGSpectral.EigenCompareDifference
import Formal.DAGSpectral.EigenCompareDifferenceTrace
import Formal.DAGSpectral.EigenCompareExecution
import Formal.DAGSpectral.EigenCompareExecutionCost
import Formal.DAGSpectral.EigenCompareFinishTrace
import Formal.DAGSpectral.EigenComparePSD
import Formal.DAGSpectral.EigenComparePreprocessingTrace
import Formal.DAGSpectral.EigenCompareSeparation
import Formal.DAGSpectral.EigenCompareThresholdTrace
import Formal.DAGSpectral.EigenCompareTrace
import Formal.DAGSpectral.ExpressionMatrix
import Formal.DAGSpectral.FactorBits
import Formal.DAGSpectral.FactorInputData
import Formal.DAGSpectral.FactorInputExecution
import Formal.DAGSpectral.FactorRange
import Formal.DAGSpectral.FinRangeExecution
import Formal.DAGSpectral.Graph
import Formal.DAGSpectral.GraphInput
import Formal.DAGSpectral.Headline
import Formal.DAGSpectral.IndexedFactors
import Formal.DAGSpectral.Inverse
import Formal.DAGSpectral.LabeledFactors
import Formal.DAGSpectral.MatrixArithmeticTrace
import Formal.DAGSpectral.MaxVolume
import Formal.DAGSpectral.MaxVolumeTrials
import Formal.DAGSpectral.NormalizationAtoms
import Formal.DAGSpectral.NormalizationBits
import Formal.DAGSpectral.NormalizationComplete
import Formal.DAGSpectral.NormalizationData
import Formal.DAGSpectral.NormalizationEntries
import Formal.DAGSpectral.NormalizationFloor
import Formal.DAGSpectral.NormalizationInput
import Formal.DAGSpectral.NormalizationProducer
import Formal.DAGSpectral.NormalizationTrials
import Formal.DAGSpectral.PSDAlgebra
import Formal.DAGSpectral.PSDEntries
import Formal.DAGSpectral.PathInformation
import Formal.DAGSpectral.PathInformationBits
import Formal.DAGSpectral.PathMatrix
import Formal.DAGSpectral.Perturbation
import Formal.DAGSpectral.ProfileBitCost
import Formal.DAGSpectral.ProfileCount
import Formal.DAGSpectral.ProfileDP
import Formal.DAGSpectral.ProfileDPBitExecution
import Formal.DAGSpectral.ProfileDPBounds
import Formal.DAGSpectral.ProfileDPCacheExecution
import Formal.DAGSpectral.ProfileDPCost
import Formal.DAGSpectral.ProfileDPExecution
import Formal.DAGSpectral.ProfileSpectralDP
import Formal.DAGSpectral.Profiles
import Formal.DAGSpectral.Pseudoinverse
import Formal.DAGSpectral.PseudoinverseOrder
import Formal.DAGSpectral.RangeNormalization
import Formal.DAGSpectral.RangeObstruction
import Formal.DAGSpectral.RatMatrix
import Formal.DAGSpectral.RationalContrastTrace
import Formal.DAGSpectral.RationalFactorization
import Formal.DAGSpectral.RationalFactorizationCast
import Formal.DAGSpectral.RationalMatrixArithmetic
import Formal.DAGSpectral.RationalPseudoinverse
import Formal.DAGSpectral.RationalPseudoinverseTrace
import Formal.DAGSpectral.RationalSchur
import Formal.DAGSpectral.RationalStorage
import Formal.DAGSpectral.RawHeadline
import Formal.DAGSpectral.Rounding
import Formal.DAGSpectral.SortedTrial
import Formal.DAGSpectral.SpectralAlgorithmCost
import Formal.DAGSpectral.SubsetInputExecution
import Formal.DAGSpectral.TopologicalMaterializeCost
import Formal.DAGSpectral.TopologicalPath
import Formal.DAGSpectral.TopologicalSort
import Formal.DAGSpectral.TopologicalSortCost
import Formal.DAGSpectral.Transfer
import Formal.DAGSpectral.TrialApproximation
import Formal.DAGSpectral.TrialBitCostBound
import Formal.DAGSpectral.UpperTriangle
import Formal.DAGSpectral.ZeroBitCost
import Lean.Util.CollectAxioms

/-! Audit every topic-owned declaration, including private and generated
helpers. No unrelated project modules are imported through the root. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.DAGSpectral.AlgorithmBitCost,
    `Formal.DAGSpectral.BasisInputExecution,
    `Formal.DAGSpectral.BitComplexity,
    `Formal.DAGSpectral.CacheStorageExecution,
    `Formal.DAGSpectral.CharpolyBits,
    `Formal.DAGSpectral.CoverBitCost,
    `Formal.DAGSpectral.CoverCacheCost,
    `Formal.DAGSpectral.CoverCardinality,
    `Formal.DAGSpectral.CoverCorrectness,
    `Formal.DAGSpectral.CoverEnumerationCost,
    `Formal.DAGSpectral.CoverExecution,
    `Formal.DAGSpectral.CoverIndependenceExecution,
    `Formal.DAGSpectral.CoverInputExecution,
    `Formal.DAGSpectral.CoverLabelCost,
    `Formal.DAGSpectral.CoverLoopCost,
    `Formal.DAGSpectral.CoverNormalizationExecution,
    `Formal.DAGSpectral.CoverPolynomialCost,
    `Formal.DAGSpectral.CoverProducer,
    `Formal.DAGSpectral.CoverSizePolynomial,
    `Formal.DAGSpectral.CoverWholeExecution,
    `Formal.DAGSpectral.Criteria,
    `Formal.DAGSpectral.CriteriaBasic,
    `Formal.DAGSpectral.CriteriaCost,
    `Formal.DAGSpectral.CriteriaEigen,
    `Formal.DAGSpectral.CriterionSelect,
    `Formal.DAGSpectral.CriterionSelectContrast,
    `Formal.DAGSpectral.CriterionSelectContrastPath,
    `Formal.DAGSpectral.CriterionSelectContrastTrace,
    `Formal.DAGSpectral.CriterionSelectCostTrace,
    `Formal.DAGSpectral.CriterionSelectEigenTrace,
    `Formal.DAGSpectral.CriterionSelectHeadline,
    `Formal.DAGSpectral.CriterionSelectMatrix,
    `Formal.DAGSpectral.CriterionSelectMatrixTrace,
    `Formal.DAGSpectral.CriterionSelectPath,
    `Formal.DAGSpectral.CriterionSelectTrace,
    `Formal.DAGSpectral.CriterionSelectWeighted,
    `Formal.DAGSpectral.CriterionSelectWeightedPath,
    `Formal.DAGSpectral.CriterionSelectWeightedScan,
    `Formal.DAGSpectral.CriterionSelectWeightedTrace,
    `Formal.DAGSpectral.Determinant,
    `Formal.DAGSpectral.DyadicScale,
    `Formal.DAGSpectral.DyadicScaleBits,
    `Formal.DAGSpectral.EigenCompare,
    `Formal.DAGSpectral.EigenCompareBisection,
    `Formal.DAGSpectral.EigenCompareBits,
    `Formal.DAGSpectral.EigenCompareCoefficientTrace,
    `Formal.DAGSpectral.EigenCompareComplexity,
    `Formal.DAGSpectral.EigenCompareDifference,
    `Formal.DAGSpectral.EigenCompareDifferenceTrace,
    `Formal.DAGSpectral.EigenCompareExecution,
    `Formal.DAGSpectral.EigenCompareExecutionCost,
    `Formal.DAGSpectral.EigenCompareFinishTrace,
    `Formal.DAGSpectral.EigenComparePSD,
    `Formal.DAGSpectral.EigenComparePreprocessingTrace,
    `Formal.DAGSpectral.EigenCompareSeparation,
    `Formal.DAGSpectral.EigenCompareThresholdTrace,
    `Formal.DAGSpectral.EigenCompareTrace,
    `Formal.DAGSpectral.ExpressionMatrix,
    `Formal.DAGSpectral.FactorBits,
    `Formal.DAGSpectral.FactorInputData,
    `Formal.DAGSpectral.FactorInputExecution,
    `Formal.DAGSpectral.FactorRange,
    `Formal.DAGSpectral.FinRangeExecution,
    `Formal.DAGSpectral.Graph,
    `Formal.DAGSpectral.GraphInput,
    `Formal.DAGSpectral.Headline,
    `Formal.DAGSpectral.IndexedFactors,
    `Formal.DAGSpectral.Inverse,
    `Formal.DAGSpectral.LabeledFactors,
    `Formal.DAGSpectral.MatrixArithmeticTrace,
    `Formal.DAGSpectral.MaxVolume,
    `Formal.DAGSpectral.MaxVolumeTrials,
    `Formal.DAGSpectral.NormalizationAtoms,
    `Formal.DAGSpectral.NormalizationBits,
    `Formal.DAGSpectral.NormalizationComplete,
    `Formal.DAGSpectral.NormalizationData,
    `Formal.DAGSpectral.NormalizationEntries,
    `Formal.DAGSpectral.NormalizationFloor,
    `Formal.DAGSpectral.NormalizationInput,
    `Formal.DAGSpectral.NormalizationProducer,
    `Formal.DAGSpectral.NormalizationTrials,
    `Formal.DAGSpectral.PSDAlgebra,
    `Formal.DAGSpectral.PSDEntries,
    `Formal.DAGSpectral.PathInformation,
    `Formal.DAGSpectral.PathInformationBits,
    `Formal.DAGSpectral.PathMatrix,
    `Formal.DAGSpectral.Perturbation,
    `Formal.DAGSpectral.ProfileBitCost,
    `Formal.DAGSpectral.ProfileCount,
    `Formal.DAGSpectral.ProfileDP,
    `Formal.DAGSpectral.ProfileDPBitExecution,
    `Formal.DAGSpectral.ProfileDPBounds,
    `Formal.DAGSpectral.ProfileDPCacheExecution,
    `Formal.DAGSpectral.ProfileDPCost,
    `Formal.DAGSpectral.ProfileDPExecution,
    `Formal.DAGSpectral.ProfileSpectralDP,
    `Formal.DAGSpectral.Profiles,
    `Formal.DAGSpectral.Pseudoinverse,
    `Formal.DAGSpectral.PseudoinverseOrder,
    `Formal.DAGSpectral.RangeNormalization,
    `Formal.DAGSpectral.RangeObstruction,
    `Formal.DAGSpectral.RatMatrix,
    `Formal.DAGSpectral.RationalContrastTrace,
    `Formal.DAGSpectral.RationalFactorization,
    `Formal.DAGSpectral.RationalFactorizationCast,
    `Formal.DAGSpectral.RationalMatrixArithmetic,
    `Formal.DAGSpectral.RationalPseudoinverse,
    `Formal.DAGSpectral.RationalPseudoinverseTrace,
    `Formal.DAGSpectral.RationalSchur,
    `Formal.DAGSpectral.RationalStorage,
    `Formal.DAGSpectral.RawHeadline,
    `Formal.DAGSpectral.Rounding,
    `Formal.DAGSpectral.SortedTrial,
    `Formal.DAGSpectral.SpectralAlgorithmCost,
    `Formal.DAGSpectral.SubsetInputExecution,
    `Formal.DAGSpectral.TopologicalMaterializeCost,
    `Formal.DAGSpectral.TopologicalPath,
    `Formal.DAGSpectral.TopologicalSort,
    `Formal.DAGSpectral.TopologicalSortCost,
    `Formal.DAGSpectral.Transfer,
    `Formal.DAGSpectral.TrialApproximation,
    `Formal.DAGSpectral.TrialBitCostBound,
    `Formal.DAGSpectral.UpperTriangle,
    `Formal.DAGSpectral.ZeroBitCost]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-21 declarations across {owners.size} modules."
