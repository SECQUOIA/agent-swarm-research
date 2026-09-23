import Formal.QuadraticPrecision.AffineBoundary
import Formal.QuadraticPrecision.BinaryModel
import Formal.QuadraticPrecision.ContactNondegenerate
import Formal.QuadraticPrecision.ContactVolume
import Formal.QuadraticPrecision.CountMinimum
import Formal.QuadraticPrecision.Folding
import Formal.QuadraticPrecision.FoldingLift
import Formal.QuadraticPrecision.IntervalLower
import Formal.QuadraticPrecision.Isodiametric
import Formal.QuadraticPrecision.IsodiametricCompact
import Formal.QuadraticPrecision.IsodiametricDiameterClosed
import Formal.QuadraticPrecision.IsodiametricGeometry
import Formal.QuadraticPrecision.IsodiametricPolarizationMeasure
import Formal.QuadraticPrecision.IsodiametricReflection
import Formal.QuadraticPrecision.IsodiametricStrict
import Formal.QuadraticPrecision.IsodiametricSupport
import Formal.QuadraticPrecision.IsodiametricWeight
import Formal.QuadraticPrecision.LinearSystem
import Formal.QuadraticPrecision.LowerContact
import Formal.QuadraticPrecision.LowerCurvature
import Formal.QuadraticPrecision.LowerDeterminant
import Formal.QuadraticPrecision.LowerEuclidean
import Formal.QuadraticPrecision.LowerIsodiametric
import Formal.QuadraticPrecision.LowerNegativeSlice
import Formal.QuadraticPrecision.LowerPositiveSlice
import Formal.QuadraticPrecision.LowerPrincipal
import Formal.QuadraticPrecision.LowerPullback
import Formal.QuadraticPrecision.LowerVolume
import Formal.QuadraticPrecision.Model
import Formal.QuadraticPrecision.OutputReflection
import Formal.QuadraticPrecision.Parity
import Formal.QuadraticPrecision.Polyhedron
import Formal.QuadraticPrecision.PolyhedronAffine
import Formal.QuadraticPrecision.PrecisionArithmetic
import Formal.QuadraticPrecision.PrecisionUpper
import Formal.QuadraticPrecision.PrincipalMinor
import Formal.QuadraticPrecision.Product
import Formal.QuadraticPrecision.ProductExact
import Formal.QuadraticPrecision.ProductLinear
import Formal.QuadraticPrecision.ProductLower
import Formal.QuadraticPrecision.RowLower
import Formal.QuadraticPrecision.RowLowerContact
import Formal.QuadraticPrecision.RowLowerCounting
import Formal.QuadraticPrecision.ScalarHeadline
import Formal.QuadraticPrecision.Spectral
import Formal.QuadraticPrecision.SpectralConvex
import Formal.QuadraticPrecision.SpectralPositiveSlice
import Formal.QuadraticPrecision.SpectralSlice
import Formal.QuadraticPrecision.SpectralUpper
import Formal.QuadraticPrecision.SquareConstruction
import Formal.QuadraticPrecision.SquareLift
import Formal.QuadraticPrecision.SquareMinimum
import Formal.QuadraticPrecision.SquarePrefix
import Formal.QuadraticPrecision.SquareSystem
import Formal.QuadraticPrecision.UpperAssembly
import Formal.QuadraticPrecision.UpperBounds
import Formal.QuadraticPrecision.UpperSquares
import Lean.Util.CollectAxioms

/-! Audit every topic-owned declaration, including private and generated
helpers. No unrelated project modules are imported through the root. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let owners : Array Name := #[
    `Formal.QuadraticPrecision.AffineBoundary,
    `Formal.QuadraticPrecision.BinaryModel,
    `Formal.QuadraticPrecision.ContactNondegenerate,
    `Formal.QuadraticPrecision.ContactVolume,
    `Formal.QuadraticPrecision.CountMinimum,
    `Formal.QuadraticPrecision.Folding,
    `Formal.QuadraticPrecision.FoldingLift,
    `Formal.QuadraticPrecision.IntervalLower,
    `Formal.QuadraticPrecision.Isodiametric,
    `Formal.QuadraticPrecision.IsodiametricCompact,
    `Formal.QuadraticPrecision.IsodiametricDiameterClosed,
    `Formal.QuadraticPrecision.IsodiametricGeometry,
    `Formal.QuadraticPrecision.IsodiametricPolarizationMeasure,
    `Formal.QuadraticPrecision.IsodiametricReflection,
    `Formal.QuadraticPrecision.IsodiametricStrict,
    `Formal.QuadraticPrecision.IsodiametricSupport,
    `Formal.QuadraticPrecision.IsodiametricWeight,
    `Formal.QuadraticPrecision.LinearSystem,
    `Formal.QuadraticPrecision.LowerContact,
    `Formal.QuadraticPrecision.LowerCurvature,
    `Formal.QuadraticPrecision.LowerDeterminant,
    `Formal.QuadraticPrecision.LowerEuclidean,
    `Formal.QuadraticPrecision.LowerIsodiametric,
    `Formal.QuadraticPrecision.LowerNegativeSlice,
    `Formal.QuadraticPrecision.LowerPositiveSlice,
    `Formal.QuadraticPrecision.LowerPrincipal,
    `Formal.QuadraticPrecision.LowerPullback,
    `Formal.QuadraticPrecision.LowerVolume,
    `Formal.QuadraticPrecision.Model,
    `Formal.QuadraticPrecision.OutputReflection,
    `Formal.QuadraticPrecision.Parity,
    `Formal.QuadraticPrecision.Polyhedron,
    `Formal.QuadraticPrecision.PolyhedronAffine,
    `Formal.QuadraticPrecision.PrecisionArithmetic,
    `Formal.QuadraticPrecision.PrecisionUpper,
    `Formal.QuadraticPrecision.PrincipalMinor,
    `Formal.QuadraticPrecision.Product,
    `Formal.QuadraticPrecision.ProductExact,
    `Formal.QuadraticPrecision.ProductLinear,
    `Formal.QuadraticPrecision.ProductLower,
    `Formal.QuadraticPrecision.RowLower,
    `Formal.QuadraticPrecision.RowLowerContact,
    `Formal.QuadraticPrecision.RowLowerCounting,
    `Formal.QuadraticPrecision.ScalarHeadline,
    `Formal.QuadraticPrecision.Spectral,
    `Formal.QuadraticPrecision.SpectralConvex,
    `Formal.QuadraticPrecision.SpectralPositiveSlice,
    `Formal.QuadraticPrecision.SpectralSlice,
    `Formal.QuadraticPrecision.SpectralUpper,
    `Formal.QuadraticPrecision.SquareConstruction,
    `Formal.QuadraticPrecision.SquareLift,
    `Formal.QuadraticPrecision.SquareMinimum,
    `Formal.QuadraticPrecision.SquarePrefix,
    `Formal.QuadraticPrecision.SquareSystem,
    `Formal.QuadraticPrecision.UpperAssembly,
    `Formal.QuadraticPrecision.UpperBounds,
    `Formal.QuadraticPrecision.UpperSquares]
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    let owned := (env.getModuleIdxFor? name).any fun idx =>
      (env.header.modules[idx]?).any fun mod => owners.contains mod.module
    return if owned then names.push name else names
  if names.isEmpty then throwError "empty audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} topic-20 declarations across {owners.size} modules."
