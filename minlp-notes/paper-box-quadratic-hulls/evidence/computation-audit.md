# Computational chapter and comparison tools audit

Scope: `sections/08-computation.tex`, `appendices/D-comparison-tools.tex`,
and the numerical companion. All optimization results come from the archived
October computation stream. No experiment, hull-depth solve, validity sampler,
or optimization-based checker was rerun.

## Mathematical reconstruction

1. **Fifteen-support family separator.** The proof now treats every feasible
   stationary solution of each bordered face system. It proves that singular
   systems with feasible stationary solutions have a common objective value.
   A smallest-support global minimizer has a nonsingular bordered system:
   a null direction leaves the objective constant and reaches a lower-dimensional
   face. This supplies the missing degeneracy contract and explains why exact
   omission of singular systems is sound, while numerical omission of nearly
   singular systems can miss a cut. All stationary candidates are feasible;
   neither positive definiteness of a face Hessian nor sufficiency of KKT
   conditions is assumed.
2. **Five-tetrahedron exact lift.** The tetrahedron vertices match the
   implementation. The central barycentric coordinates and four outer regions
   establish cube coverage. The CP4/DNN4 argument gives a complete primal proof
   of the exact normalized lift. Ten linking equations include normalization;
   no redundant eleventh equation is claimed.
3. **Normalized hull depth.** The dual description follows from COP4=PSD+N.
   The uniform mean is strictly positive for every nonzero nonnegative
   quadratic. A norm argument proves compactness of the mean-one coefficient
   slice, so the minimum is finite and attained. Separation of the compact
   moment hull proves the membership equivalence. Constant subtraction uses
   the explicit hypothesis M00=1. This avoids treating normalization or
   attainment as an implicit fact.
4. **Cut correction.** Adding at least minus the least tetrahedral simplex
   minimum yields a valid cube quadratic in exact arithmetic. Approximate
   stationary face calculations plus a small margin do not constitute interval
   certification. The manuscript states this distinction explicitly.
5. **Triple-local gain bound.** The hypotheses are exactly those used by the
   mixture proof: a convex baseline containing uniform moments, a feasible
   starting point, independently feasible auxiliaries per triple, and a
   one-sided bound on negative exact depths. It applies to clique patterns.
   Shared higher moments in the implemented K system are expressly excluded.
   A gain comparison from a reported lower baseline must add the primal-to-dual
   margin. The normalized matrix hull is called M3 throughout; the notation
   no longer collides with the paper's homogeneous moment cone.
6. **Dual-residual correction.** The weak-duality proof includes all variable
   intervals. Family auxiliary upper bounds of three follow from bounded
   b/B entries and the PSD Schur block, and DNN weights are bounded by their
   total normalization. The implementation's dual projection and rounding
   allowances remain floating-point estimates, not formal interval proofs.

No reconstructed mathematical statement was found to invalidate the
computational comparison. Completeness of the family is not inferred from
any finite sample.

## Numerical reporting decisions

- The main hard-three table uses corrected dual values throughout. The maximum
  F-primal shortfall below X's corrected reference is identified separately;
  the requested solver tolerance is not presented as an accuracy guarantee.
- Eight representative constructed rows identify seed 1 explicitly. Full
  records cover all 16 chains, eight cacti, and eight hard-tree instances.
  Heuristic U values are described as feasible references. Gurobi's optimal
  labels mean optimal within the requested tolerance, not exact certificates.
- X uses five tetrahedra, not the more familiar six-tetrahedron cube lift.
  F's selective size advantage is empirical; imposing all 24 orientations
  can exceed the exact lift's size.
- The hull-depth selection used by K/A/X is stronger than family selection
  and has a different cost. XF uses family selection, but its iterates need
  not select the exact same triples as F. Chain XF timings cross separate
  runs; cactus XF timings share a driver invocation. Neither design gives
  controlled hardware timings.
- The natural-instance outcomes are mostly negative. The AP-generator
  exception is retained, including its small relative gap and absence of
  additional family gain after KA. The manuscript expressly disclaims a
  reproduction of the published AP gap distribution and states the diagonal
  masking difference.
- The original BoxQP depths below -1e-6 are identified as baseline triangle
  residuals. Cap residuals can explain bulk numerical depths. A computed
  negative depth at an approximately feasible baseline point is not a proof
  of a valid triple gap.
- Only spar090-075-1 has a complete strict all-triple audit. Its computed
  minimum -8.10e-9 is not a certified one-sided depth. The 0.045% diagnostic
  and 0.60% sensitivity are separately identified; the latter assumes at
  most 1e-7 overestimation per computed depth. Their primal-to-dual adjusted
  figures are 0.54% and 1.10%. Exact baseline feasibility and the assumed
  depth-error bound remain uncertified.
- Hard objectives sharing edges produce little tested triple-level gain,
  rather than validating a general theorem about overlap. SCS comparisons
  support the F/X numerical tie where Clarabel's exact-lift dual estimates
  are less accurate.
- Wall-clock times come from a loaded shared 36-core machine. There is no
  branch-and-bound study, practical-class benefit claim, or generic solver
  speedup claim.

## Companion and provenance

The companion contains byte-identical source snapshots, sparse constructed
objective data, per-round comparison logs, feasible reference records,
benchmark summaries, and compact supplemental tables. It excludes the large
moment/depth arrays and external source papers. The source SHA256 manifest
identifies copied sources and the omitted small-dense campaign inputs behind
a compressed 30,000-instance summary.

`inspect_records.py` uses only the Python standard library; it does not import
the optimization implementation. It reconstructs all 334 method rows, the
109-objective closure table, and strict-audit sensitivities. It checks the
archived table values with their published rounding. The companion distinguishes
read-only record inspection from model reproduction, includes an executable
example of the original driver interface, and documents missing dependencies
of full-campaign reproduction and unrecorded NumPy/SciPy/Python versions.
The hard-objective dense-matrix-plus-constant format is distinguished from
the constructed instances' sparse upper-triangle format.

## Targeted commands actually run

From `/workspace/minlp-notes`:

```text
python paper-box-quadratic-hulls/companion/inspect_records.py --write
```

Result: exit 0. Reconstructed CSV exports, 386 initial copied-source hashes,
334 archived constructed-method table rows, and the hard-three/strict tables.
After removing redundant large baseline-triangle lists and the machine-specific
Gurobi wrapper from the companion:

```text
python paper-box-quadratic-hulls/companion/inspect_records.py
```

Result: exit 0. All 371 retained copied-source hashes verified; all 334
constructed-method rows reconstructed; the 109 hard-objective closures and
strict gain sensitivities reconstructed. No optimization code was imported,
no instance was generated, and no model was solved.

Additional work consisted of file reads, source copying, checksumming, and
standard-library aggregation of archived small-dense records. No project-wide
verification or CI inspection was performed.

## BoxQP objective convention

After the shared literature lead verified the official repository's
maximization convention, an additional read-only inspection confirmed the
conversion used by the archived computations. The loader in
`research-20261001/three-var-computation/code/relax.py`, lines 36–44,
reads the full symmetric matrix `Q`, checks symmetry, and returns
`H=-0.5*Q, g=-c`. Lines 122–131 use diagonal coefficients `H_ii` and
off-diagonal coefficients `2*H_ij`, exactly matching the manuscript's
`H:Y+g'm` convention. The reference-value readers in `spar_base.py`,
`spar_audit.py`, and `strict_spar_audit.py` negate the published
maximization optima. The benchmark paragraph now states this conversion.
This check read existing code; it did not run a model or an experiment.
The shared lead's supplied repository entry is undated. The internal key
`BurerBoxQPInstances2019` does not assert a publication year; the
typeset bibliography states that the repository is undated and records
the access date.
