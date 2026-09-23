import Formal.MatroidSpectral.Boundaries
import Formal.MatroidSpectral.CoverCardinality
import Formal.MatroidSpectral.CoverPolynomialSize
import Formal.MatroidSpectral.CoverProducer
import Formal.MatroidSpectral.Criteria
import Formal.MatroidSpectral.CriteriaBitWork
import Formal.MatroidSpectral.CriteriaContrastExecution
import Formal.MatroidSpectral.CriteriaControl
import Formal.MatroidSpectral.CriteriaExecution
import Formal.MatroidSpectral.CriteriaSelection
import Formal.MatroidSpectral.DeterminantBits
import Formal.MatroidSpectral.DeterminantProfileBounds
import Formal.MatroidSpectral.DeterminantProfiles
import Formal.MatroidSpectral.Elimination
import Formal.MatroidSpectral.EliminationBitExecution
import Formal.MatroidSpectral.EliminationBits
import Formal.MatroidSpectral.EliminationExecution
import Formal.MatroidSpectral.ExecutionCandidate
import Formal.MatroidSpectral.ExecutionCollection
import Formal.MatroidSpectral.ExecutionCoordinates
import Formal.MatroidSpectral.ExecutionCostBounds
import Formal.MatroidSpectral.ExecutionCover
import Formal.MatroidSpectral.ExecutionMarked
import Formal.MatroidSpectral.ExecutionProfiles
import Formal.MatroidSpectral.ExecutionRecovery
import Formal.MatroidSpectral.ExecutionTrialLabels
import Formal.MatroidSpectral.ExecutionZero
import Formal.MatroidSpectral.GraphicRepresentation
import Formal.MatroidSpectral.GraphicRepresentationBasis
import Formal.MatroidSpectral.GraphicRepresentationFinite
import Formal.MatroidSpectral.GraphicRepresentationForest
import Formal.MatroidSpectral.GraphicRepresentationMultigraph
import Formal.MatroidSpectral.Headline
import Formal.MatroidSpectral.HeadlineCriteria
import Formal.MatroidSpectral.InputExecution
import Formal.MatroidSpectral.Interpolation
import Formal.MatroidSpectral.InterpolationBits
import Formal.MatroidSpectral.InterpolationExecution
import Formal.MatroidSpectral.InterpolationTrace
import Formal.MatroidSpectral.InterpolationTraceBits
import Formal.MatroidSpectral.NormalizationEnumeration
import Formal.MatroidSpectral.NormalizationExecution
import Formal.MatroidSpectral.NormalizationInputExecution
import Formal.MatroidSpectral.PartitionRepresentation
import Formal.MatroidSpectral.ProfileCardinality
import Formal.MatroidSpectral.ProfileGramExecution
import Formal.MatroidSpectral.ProfileLabels
import Formal.MatroidSpectral.ProfileOracleBounds
import Formal.MatroidSpectral.ProfileOracleEvaluation
import Formal.MatroidSpectral.ProfileOracleExecution
import Formal.MatroidSpectral.ProfileProducer
import Formal.MatroidSpectral.ProfileProducerBases
import Formal.MatroidSpectral.ProfileProducerOracle
import Formal.MatroidSpectral.Recovery
import Formal.MatroidSpectral.Representation
import Formal.MatroidSpectral.RepresentationBitCost
import Formal.MatroidSpectral.RepresentationCost
import Formal.MatroidSpectral.RepresentationExecution
import Formal.MatroidSpectral.RepresentationReduction
import Formal.MatroidSpectral.RepresentationScaling
import Formal.MatroidSpectral.SpectralApproximation
import Formal.MatroidSpectral.SpectralCover
import Formal.MatroidSpectral.SpectralRemainder
import Formal.MatroidSpectral.TrialLabels
import Formal.MatroidSpectral.UniformRepresentation
import Lean.Util.CollectAxioms

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.MatroidSpectral.Boundaries,
    `Formal.MatroidSpectral.CoverCardinality,
    `Formal.MatroidSpectral.CoverPolynomialSize,
    `Formal.MatroidSpectral.CoverProducer,
    `Formal.MatroidSpectral.Criteria,
    `Formal.MatroidSpectral.CriteriaBitWork,
    `Formal.MatroidSpectral.CriteriaContrastExecution,
    `Formal.MatroidSpectral.CriteriaControl,
    `Formal.MatroidSpectral.CriteriaExecution,
    `Formal.MatroidSpectral.CriteriaSelection,
    `Formal.MatroidSpectral.DeterminantBits,
    `Formal.MatroidSpectral.DeterminantProfileBounds,
    `Formal.MatroidSpectral.DeterminantProfiles,
    `Formal.MatroidSpectral.Elimination,
    `Formal.MatroidSpectral.EliminationBitExecution,
    `Formal.MatroidSpectral.EliminationBits,
    `Formal.MatroidSpectral.EliminationExecution,
    `Formal.MatroidSpectral.ExecutionCandidate,
    `Formal.MatroidSpectral.ExecutionCollection,
    `Formal.MatroidSpectral.ExecutionCoordinates,
    `Formal.MatroidSpectral.ExecutionCostBounds,
    `Formal.MatroidSpectral.ExecutionCover,
    `Formal.MatroidSpectral.ExecutionMarked,
    `Formal.MatroidSpectral.ExecutionProfiles,
    `Formal.MatroidSpectral.ExecutionRecovery,
    `Formal.MatroidSpectral.ExecutionTrialLabels,
    `Formal.MatroidSpectral.ExecutionZero,
    `Formal.MatroidSpectral.GraphicRepresentation,
    `Formal.MatroidSpectral.GraphicRepresentationBasis,
    `Formal.MatroidSpectral.GraphicRepresentationFinite,
    `Formal.MatroidSpectral.GraphicRepresentationForest,
    `Formal.MatroidSpectral.GraphicRepresentationMultigraph,
    `Formal.MatroidSpectral.Headline,
    `Formal.MatroidSpectral.HeadlineCriteria,
    `Formal.MatroidSpectral.InputExecution,
    `Formal.MatroidSpectral.Interpolation,
    `Formal.MatroidSpectral.InterpolationBits,
    `Formal.MatroidSpectral.InterpolationExecution,
    `Formal.MatroidSpectral.InterpolationTrace,
    `Formal.MatroidSpectral.InterpolationTraceBits,
    `Formal.MatroidSpectral.NormalizationEnumeration,
    `Formal.MatroidSpectral.NormalizationExecution,
    `Formal.MatroidSpectral.NormalizationInputExecution,
    `Formal.MatroidSpectral.PartitionRepresentation,
    `Formal.MatroidSpectral.ProfileCardinality,
    `Formal.MatroidSpectral.ProfileGramExecution,
    `Formal.MatroidSpectral.ProfileLabels,
    `Formal.MatroidSpectral.ProfileOracleBounds,
    `Formal.MatroidSpectral.ProfileOracleEvaluation,
    `Formal.MatroidSpectral.ProfileOracleExecution,
    `Formal.MatroidSpectral.ProfileProducer,
    `Formal.MatroidSpectral.ProfileProducerBases,
    `Formal.MatroidSpectral.ProfileProducerOracle,
    `Formal.MatroidSpectral.Recovery,
    `Formal.MatroidSpectral.Representation,
    `Formal.MatroidSpectral.RepresentationBitCost,
    `Formal.MatroidSpectral.RepresentationCost,
    `Formal.MatroidSpectral.RepresentationExecution,
    `Formal.MatroidSpectral.RepresentationReduction,
    `Formal.MatroidSpectral.RepresentationScaling,
    `Formal.MatroidSpectral.SpectralApproximation,
    `Formal.MatroidSpectral.SpectralCover,
    `Formal.MatroidSpectral.SpectralRemainder,
    `Formal.MatroidSpectral.TrialLabels,
    `Formal.MatroidSpectral.UniformRepresentation]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-22 declarations across {owners.size} modules."
