import Formal.ReciprocalAnchor.ManyActiveCount
import Formal.ReciprocalAnchor.ManyAlgorithm
import Formal.ReciprocalAnchor.ManyAlgorithmSize
import Formal.ReciprocalAnchor.ManyBitCost
import Formal.ReciprocalAnchor.ManyEnvelope
import Formal.ReciprocalAnchor.ManyEnvelopeBound
import Formal.ReciprocalAnchor.ManyEnvelopeLaw
import Formal.ReciprocalAnchor.ManyEuclidCost
import Formal.ReciprocalAnchor.ManyEvaluatorBitCost
import Formal.ReciprocalAnchor.ManyExamples
import Formal.ReciprocalAnchor.ManyFastAtoms
import Formal.ReciprocalAnchor.ManyFastConstruction
import Formal.ReciprocalAnchor.ManyFastCutSize
import Formal.ReciprocalAnchor.ManyFastDominance
import Formal.ReciprocalAnchor.ManyFastEnvelope
import Formal.ReciprocalAnchor.ManyFastEvaluation
import Formal.ReciprocalAnchor.ManyFastLaw
import Formal.ReciprocalAnchor.ManyFastLawGeometry
import Formal.ReciprocalAnchor.ManyFastLawSize
import Formal.ReciprocalAnchor.ManyFastOperandSize
import Formal.ReciprocalAnchor.ManyFastSegments
import Formal.ReciprocalAnchor.ManyFastSeparation
import Formal.ReciprocalAnchor.ManyFastSize
import Formal.ReciprocalAnchor.ManyFastWitness
import Formal.ReciprocalAnchor.ManyGeometry
import Formal.ReciprocalAnchor.ManyIntegrals
import Formal.ReciprocalAnchor.ManyLawCompress
import Formal.ReciprocalAnchor.ManyLaws
import Formal.ReciprocalAnchor.ManyLinearSeparation
import Formal.ReciprocalAnchor.ManyMembership
import Formal.ReciprocalAnchor.ManyMembershipExamples
import Formal.ReciprocalAnchor.ManyModel
import Formal.ReciprocalAnchor.ManyNormalization
import Formal.ReciprocalAnchor.ManyOneLeaf
import Formal.ReciprocalAnchor.ManyOracle
import Formal.ReciprocalAnchor.ManyOracleBitCost
import Formal.ReciprocalAnchor.ManyOracleExamples
import Formal.ReciprocalAnchor.ManyOracleSize
import Formal.ReciprocalAnchor.ManyParallelLines
import Formal.ReciprocalAnchor.ManyProbability
import Formal.ReciprocalAnchor.ManyProbabilityEndpoints
import Formal.ReciprocalAnchor.ManyProbabilityIntegral
import Formal.ReciprocalAnchor.ManyProbabilitySelection
import Formal.ReciprocalAnchor.ManyQuantile
import Formal.ReciprocalAnchor.ManyRationalBound
import Formal.ReciprocalAnchor.ManyRationalCandidate
import Formal.ReciprocalAnchor.ManyRationalEnvelope
import Formal.ReciprocalAnchor.ManyRationalExample
import Formal.ReciprocalAnchor.ManyRationalLaw
import Formal.ReciprocalAnchor.ManyRationalMix
import Formal.ReciprocalAnchor.ManyRationalMixCall
import Formal.ReciprocalAnchor.ManyRationalProducer
import Formal.ReciprocalAnchor.ManyRationalSelector
import Formal.ReciprocalAnchor.ManyRationalSize
import Formal.ReciprocalAnchor.ManyRationalThreshold
import Formal.ReciprocalAnchor.ManyRationalWitness
import Formal.ReciprocalAnchor.ManyResults
import Formal.ReciprocalAnchor.ManySelection
import Formal.ReciprocalAnchor.ManySeparation
import Formal.ReciprocalAnchor.ManySlopeJumps
import Formal.ReciprocalAnchor.ManySortCost
import Formal.ReciprocalAnchor.ManyStackGeometry
import Formal.ReciprocalAnchor.ManyThreshold
import Formal.ReciprocalAnchor.ManyWitnessBitCost
import Formal.ReciprocalAnchor.ManyWitnessExamples
import Formal.ReciprocalAnchor.ManyWitnessLists
import Formal.ReciprocalAnchor.ManyWitnessOperandSize
import Lean.Util.CollectAxioms

/-! Topic 13 only, including private and generated declarations. -/
open Lean Elab Command in
run_cmd do
  let selected : Array Name := #[`Formal.ReciprocalAnchor.ManyActiveCount,
    `Formal.ReciprocalAnchor.ManyAlgorithm,
    `Formal.ReciprocalAnchor.ManyAlgorithmSize,
    `Formal.ReciprocalAnchor.ManyBitCost,
    `Formal.ReciprocalAnchor.ManyEnvelope,
    `Formal.ReciprocalAnchor.ManyEnvelopeBound,
    `Formal.ReciprocalAnchor.ManyEnvelopeLaw,
    `Formal.ReciprocalAnchor.ManyEuclidCost,
    `Formal.ReciprocalAnchor.ManyEvaluatorBitCost,
    `Formal.ReciprocalAnchor.ManyExamples,
    `Formal.ReciprocalAnchor.ManyFastAtoms,
    `Formal.ReciprocalAnchor.ManyFastConstruction,
    `Formal.ReciprocalAnchor.ManyFastCutSize,
    `Formal.ReciprocalAnchor.ManyFastDominance,
    `Formal.ReciprocalAnchor.ManyFastEnvelope,
    `Formal.ReciprocalAnchor.ManyFastEvaluation,
    `Formal.ReciprocalAnchor.ManyFastLaw,
    `Formal.ReciprocalAnchor.ManyFastLawGeometry,
    `Formal.ReciprocalAnchor.ManyFastLawSize,
    `Formal.ReciprocalAnchor.ManyFastOperandSize,
    `Formal.ReciprocalAnchor.ManyFastSegments,
    `Formal.ReciprocalAnchor.ManyFastSeparation,
    `Formal.ReciprocalAnchor.ManyFastSize,
    `Formal.ReciprocalAnchor.ManyFastWitness,
    `Formal.ReciprocalAnchor.ManyGeometry,
    `Formal.ReciprocalAnchor.ManyIntegrals,
    `Formal.ReciprocalAnchor.ManyLawCompress,
    `Formal.ReciprocalAnchor.ManyLaws,
    `Formal.ReciprocalAnchor.ManyLinearSeparation,
    `Formal.ReciprocalAnchor.ManyMembership,
    `Formal.ReciprocalAnchor.ManyMembershipExamples,
    `Formal.ReciprocalAnchor.ManyModel,
    `Formal.ReciprocalAnchor.ManyNormalization,
    `Formal.ReciprocalAnchor.ManyOneLeaf,
    `Formal.ReciprocalAnchor.ManyOracle,
    `Formal.ReciprocalAnchor.ManyOracleBitCost,
    `Formal.ReciprocalAnchor.ManyOracleExamples,
    `Formal.ReciprocalAnchor.ManyOracleSize,
    `Formal.ReciprocalAnchor.ManyParallelLines,
    `Formal.ReciprocalAnchor.ManyProbability,
    `Formal.ReciprocalAnchor.ManyProbabilityEndpoints,
    `Formal.ReciprocalAnchor.ManyProbabilityIntegral,
    `Formal.ReciprocalAnchor.ManyProbabilitySelection,
    `Formal.ReciprocalAnchor.ManyQuantile,
    `Formal.ReciprocalAnchor.ManyRationalBound,
    `Formal.ReciprocalAnchor.ManyRationalCandidate,
    `Formal.ReciprocalAnchor.ManyRationalEnvelope,
    `Formal.ReciprocalAnchor.ManyRationalExample,
    `Formal.ReciprocalAnchor.ManyRationalLaw,
    `Formal.ReciprocalAnchor.ManyRationalMix,
    `Formal.ReciprocalAnchor.ManyRationalMixCall,
    `Formal.ReciprocalAnchor.ManyRationalProducer,
    `Formal.ReciprocalAnchor.ManyRationalSelector,
    `Formal.ReciprocalAnchor.ManyRationalSize,
    `Formal.ReciprocalAnchor.ManyRationalThreshold,
    `Formal.ReciprocalAnchor.ManyRationalWitness,
    `Formal.ReciprocalAnchor.ManyResults,
    `Formal.ReciprocalAnchor.ManySelection,
    `Formal.ReciprocalAnchor.ManySeparation,
    `Formal.ReciprocalAnchor.ManySlopeJumps,
    `Formal.ReciprocalAnchor.ManySortCost,
    `Formal.ReciprocalAnchor.ManyStackGeometry,
    `Formal.ReciprocalAnchor.ManyThreshold,
    `Formal.ReciprocalAnchor.ManyWitnessBitCost,
    `Formal.ReciprocalAnchor.ManyWitnessExamples,
    `Formal.ReciprocalAnchor.ManyWitnessLists,
    `Formal.ReciprocalAnchor.ManyWitnessOperandSize]
  let env ← getEnv
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => selected.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "Empty extension audit"
  for name in names do
    for axiomName in ← Lean.collectAxioms name do
      unless #[`propext, `Classical.choice, `Quot.sound].contains axiomName do
        throwError "{name} depends on disallowed axiom {axiomName}"
  logInfo m!"PASS: audited {names.size} declarations in {selected.size} extension modules; \
    only propext, Classical.choice, Quot.sound are allowed."
