import Formal.MultilinearGap.StructuralAveraging
import Formal.MultilinearGap.StructuralCamion
import Formal.MultilinearGap.StructuralCardinality
import Formal.MultilinearGap.StructuralCardinalityTU
import Formal.MultilinearGap.StructuralCardinalityUpper
import Formal.MultilinearGap.StructuralCommonAspect
import Formal.MultilinearGap.StructuralCycleParity
import Formal.MultilinearGap.StructuralCycleTU
import Formal.MultilinearGap.StructuralEvenCycleColoring
import Formal.MultilinearGap.StructuralFactorGaps
import Formal.MultilinearGap.StructuralFeedbackAssembly
import Formal.MultilinearGap.StructuralFeedbackBoxes
import Formal.MultilinearGap.StructuralFeedbackFlowerGraph
import Formal.MultilinearGap.StructuralFeedbackForest
import Formal.MultilinearGap.StructuralFeedbackLocal
import Formal.MultilinearGap.StructuralFeedbackOrder
import Formal.MultilinearGap.StructuralFeedbackPayoffSharpness
import Formal.MultilinearGap.StructuralFeedbackRepair
import Formal.MultilinearGap.StructuralFeedbackResults
import Formal.MultilinearGap.StructuralFeedbackUniversal
import Formal.MultilinearGap.StructuralFrequency
import Formal.MultilinearGap.StructuralFrequencyApplications
import Formal.MultilinearGap.StructuralFrequencyBipartite
import Formal.MultilinearGap.StructuralFrequencyBound
import Formal.MultilinearGap.StructuralFrequencyBox
import Formal.MultilinearGap.StructuralFrequencyComponents
import Formal.MultilinearGap.StructuralFrequencyCycle
import Formal.MultilinearGap.StructuralFrequencyCycleGirth
import Formal.MultilinearGap.StructuralFrequencyDual
import Formal.MultilinearGap.StructuralFrequencyLayout
import Formal.MultilinearGap.StructuralFrequencyLayoutAssembly
import Formal.MultilinearGap.StructuralFrequencyLocal
import Formal.MultilinearGap.StructuralFrequencyMonomial
import Formal.MultilinearGap.StructuralFrequencyOddCycle
import Formal.MultilinearGap.StructuralFrequencyProduct
import Formal.MultilinearGap.StructuralFrequencyRounding
import Formal.MultilinearGap.StructuralFrequencySharpness
import Formal.MultilinearGap.StructuralFrequencySharpnessBox
import Formal.MultilinearGap.StructuralFrequencySlab
import Formal.MultilinearGap.StructuralFrequencySupport
import Formal.MultilinearGap.StructuralFrequencyTheorem
import Formal.MultilinearGap.StructuralGHParity
import Formal.MultilinearGap.StructuralInterpolation
import Formal.MultilinearGap.StructuralPositiveFlower
import Formal.MultilinearGap.StructuralSharpness
import Formal.MultilinearGap.StructuralTreewidthArticulation
import Formal.MultilinearGap.StructuralTreewidthAssembly
import Formal.MultilinearGap.StructuralTreewidthClasses
import Formal.MultilinearGap.StructuralTreewidthColorAssembly
import Formal.MultilinearGap.StructuralTreewidthColoring
import Formal.MultilinearGap.StructuralTreewidthDecomposition
import Formal.MultilinearGap.StructuralTreewidthElimination
import Formal.MultilinearGap.StructuralTreewidthEmbedding
import Formal.MultilinearGap.StructuralTreewidthExpansion
import Formal.MultilinearGap.StructuralTreewidthGluing
import Formal.MultilinearGap.StructuralTreewidthGraph
import Formal.MultilinearGap.StructuralTreewidthIncidenceColoring
import Formal.MultilinearGap.StructuralTreewidthNetworkSound
import Formal.MultilinearGap.StructuralTreewidthNetworks
import Formal.MultilinearGap.StructuralTreewidthPieceColoring
import Formal.MultilinearGap.StructuralTreewidthPieces
import Formal.MultilinearGap.StructuralTreewidthReduction
import Formal.MultilinearGap.StructuralTreewidthStates
import Formal.MultilinearGap.StructuralTreewidthSuppression
import Formal.MultilinearGap.StructuralTreewidthTU
import Formal.MultilinearGap.StructuralTwoClasses
import Lean.Util.CollectAxioms

/-! Audit every declaration owned by the topic modules, including private
helpers and generated declarations. Transitive dependencies may use only the
three standard axioms below. This is not a project-wide audit. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.MultilinearGap.StructuralAveraging,
    `Formal.MultilinearGap.StructuralCamion,
    `Formal.MultilinearGap.StructuralCardinality,
    `Formal.MultilinearGap.StructuralCardinalityTU,
    `Formal.MultilinearGap.StructuralCardinalityUpper,
    `Formal.MultilinearGap.StructuralCommonAspect,
    `Formal.MultilinearGap.StructuralCycleParity,
    `Formal.MultilinearGap.StructuralCycleTU,
    `Formal.MultilinearGap.StructuralEvenCycleColoring,
    `Formal.MultilinearGap.StructuralFactorGaps,
    `Formal.MultilinearGap.StructuralFeedbackAssembly,
    `Formal.MultilinearGap.StructuralFeedbackBoxes,
    `Formal.MultilinearGap.StructuralFeedbackFlowerGraph,
    `Formal.MultilinearGap.StructuralFeedbackForest,
    `Formal.MultilinearGap.StructuralFeedbackLocal,
    `Formal.MultilinearGap.StructuralFeedbackOrder,
    `Formal.MultilinearGap.StructuralFeedbackPayoffSharpness,
    `Formal.MultilinearGap.StructuralFeedbackRepair,
    `Formal.MultilinearGap.StructuralFeedbackResults,
    `Formal.MultilinearGap.StructuralFeedbackUniversal,
    `Formal.MultilinearGap.StructuralFrequency,
    `Formal.MultilinearGap.StructuralFrequencyApplications,
    `Formal.MultilinearGap.StructuralFrequencyBipartite,
    `Formal.MultilinearGap.StructuralFrequencyBound,
    `Formal.MultilinearGap.StructuralFrequencyBox,
    `Formal.MultilinearGap.StructuralFrequencyComponents,
    `Formal.MultilinearGap.StructuralFrequencyCycle,
    `Formal.MultilinearGap.StructuralFrequencyCycleGirth,
    `Formal.MultilinearGap.StructuralFrequencyDual,
    `Formal.MultilinearGap.StructuralFrequencyLayout,
    `Formal.MultilinearGap.StructuralFrequencyLayoutAssembly,
    `Formal.MultilinearGap.StructuralFrequencyLocal,
    `Formal.MultilinearGap.StructuralFrequencyMonomial,
    `Formal.MultilinearGap.StructuralFrequencyOddCycle,
    `Formal.MultilinearGap.StructuralFrequencyProduct,
    `Formal.MultilinearGap.StructuralFrequencyRounding,
    `Formal.MultilinearGap.StructuralFrequencySharpness,
    `Formal.MultilinearGap.StructuralFrequencySharpnessBox,
    `Formal.MultilinearGap.StructuralFrequencySlab,
    `Formal.MultilinearGap.StructuralFrequencySupport,
    `Formal.MultilinearGap.StructuralFrequencyTheorem,
    `Formal.MultilinearGap.StructuralGHParity,
    `Formal.MultilinearGap.StructuralInterpolation,
    `Formal.MultilinearGap.StructuralPositiveFlower,
    `Formal.MultilinearGap.StructuralSharpness,
    `Formal.MultilinearGap.StructuralTreewidthArticulation,
    `Formal.MultilinearGap.StructuralTreewidthAssembly,
    `Formal.MultilinearGap.StructuralTreewidthClasses,
    `Formal.MultilinearGap.StructuralTreewidthColorAssembly,
    `Formal.MultilinearGap.StructuralTreewidthColoring,
    `Formal.MultilinearGap.StructuralTreewidthDecomposition,
    `Formal.MultilinearGap.StructuralTreewidthElimination,
    `Formal.MultilinearGap.StructuralTreewidthEmbedding,
    `Formal.MultilinearGap.StructuralTreewidthExpansion,
    `Formal.MultilinearGap.StructuralTreewidthGluing,
    `Formal.MultilinearGap.StructuralTreewidthGraph,
    `Formal.MultilinearGap.StructuralTreewidthIncidenceColoring,
    `Formal.MultilinearGap.StructuralTreewidthNetworkSound,
    `Formal.MultilinearGap.StructuralTreewidthNetworks,
    `Formal.MultilinearGap.StructuralTreewidthPieceColoring,
    `Formal.MultilinearGap.StructuralTreewidthPieces,
    `Formal.MultilinearGap.StructuralTreewidthReduction,
    `Formal.MultilinearGap.StructuralTreewidthStates,
    `Formal.MultilinearGap.StructuralTreewidthSuppression,
    `Formal.MultilinearGap.StructuralTreewidthTU,
    `Formal.MultilinearGap.StructuralTwoClasses]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-19 declarations across {owners.size} modules."
