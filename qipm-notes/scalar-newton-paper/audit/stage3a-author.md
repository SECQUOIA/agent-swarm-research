# Stage 3a author report

Authored `sections/06-coherent.tex` and `sections/07-scalar-realizations.tex`,
included them from main.tex, and added four primary-source bibliography
entries. All work is under `notes/scalar-newton-paper` as requested.

## Coverage and proof checks

- Section 6 states and attributes CGJ full-version Theorem 33, specializing
  c=1/2 and carefully squaring a relative norm estimate. The 3-dimensional
  completion lower bound is proved directly; it is expressly in the plain
  block-encoding interface, and its one-query sparse-entry bypass is stated.
  The coherent counting gap, fixed-transform error budget, polynomial and
  Laurent Bernstein obstruction, and lack of a rational/variable-time lower
  consequence are included. The source's q_* qualification is retained by
  cross-reference rather than replaced by an unjustified uniform claim.
- Section 7 proves the cyclic clock's exact condition, public inverse norm,
  plateau mass, and both matrix/Hessian full-SQ simulations. It incorporates
  the literal sparse accumulator, first Newton direction and public unperturbed
  decrement, objective-gap transfer, and fixed-k extension.
- The normalized objective tilt includes a full proof that G is public,
  its Θ(√K) size, the strengthened value/decrement scale, and its optimality
  within plateau-supported readouts. The earlier small tilt is retained as
  a clearly weaker fallback. Both box-LP and affine-slice LP consequences
  are proved, including central-subproblem accuracy, equality condition,
  barrier parameter one, and the norm-sensitive matching upper exponent.
- The norm-tree refinement is included with a full center calculation,
  c_D=2(D−1), direct Newton blocks and all scaling/barrier caveats.
  The separate global minimal-lift theorem is not imported; it belongs to
  the existing conic-lift manuscript and is unnecessary to these results.
- The original e^{-1/T} history instance is subsumed by the general damping
  formulas. A nonsymmetric cyclic M avoids an unnecessary symmetric
  dilation; its Newton Hessian is SPD, and a symmetric dilation could be
  added without changing parameters.

## Corrections and development beyond transcription

1. The fixed-k primary source has a positive high promise Φ≥2^(-5k), not
   an absolute high promise. The manuscript uses the original promise;
   magnitude outputs remain hard because they contain those instances.
2. A numerical estimate of an optimal coordinate is not an actual feasible
   optimizer representation. The quantum theorem asserts only the scalar
   numerical upper. The feasible-point-coordinate contract is a lower-bound
   transfer. No vacuous “representation” by restating Mx=e is used.
3. Sampling failure conventions are separated: fresh unflagged constant
   failure per sample can corrupt a rare plateau; one randomized reusable
   good-sampler setup does not accumulate that failure per draw. The latter
   reduction charges setup plus repeated sampling and can amplify setups.
4. The projected perturbation inequality proves the sufficient vector-error
   scale ε_v≤c√p, with Bernoulli event gap Θ(p). This retains the δ² repeat
   penalty on the scalar family and the source's p=Θ(ζ) lower. It also
   develops the stronger admissible p=Θ(ζ²) choice with its ζ² repeat factor.
   No ordinary unflagged sampler guarantee is silently upgraded.
5. Alase et al.'s tight α/ε comparator is specified for their normalized
   expectation-value subproblem; the manuscript does not drop the system
   conditioning parameters from their full unnormalized solution task.
6. The generic feasible-sample upper is proved via a residual for MP and
   angular normalization, and expressly supplies only the sample law rather
   than a free norm or explicit feasible coordinates.
7. Root identified that affine value accuracy can exceed the manuscript's
   default epsilon≤1/2 range. The norm-sensitive inverse-overlap theorem in
   Section 3 now explicitly permits 0<epsilon≤R_e/2: its unchanged proof
   uses eta=epsilon/(4R_e)≤1/8, and the sampling and degree estimates remain
   valid. The affine application states this range and its cost now uses
   multiplication, correcting a typographical comma.

## Literature verification

Primary local originals/full text checked: CGJ Theorem 33; Bansal–Sinha
Theorem 1.3 and Corollary 1.4; Alase et al. Theorem II.19, IV.13 and their
problem definitions; Apers–Gribling version 3 Lemma 8.5; Motlagh–Wiebe
boundedness characterization; Kerenidis–Prakash–Szilágyi output discussion.
Current primary arXiv records opened for 2111.10485, 2008.07003,
2308.01501, and 2311.03215. New bibliography entries use their verified
publication DOI/title metadata. The parent independently checked the norm
tree and Apers–Gribling comparison as well.

Novelty language is limited to the exact access/parameter/optimization
combinations. Neither classical optimization SQ hardness, Forrelation,
matrix-function clocks, norm trees, nor variable-time inverse-power norm
estimation is claimed as new.

## Validation

- `/home/sgusev/miniconda3/envs/qipm/bin/python scripts/verify_cyclic.py`
  passes: exact small cyclic spectrum, inverse series, public solution and
  tilt norms across different sign inputs, scalar and decrement identities,
  all row-norm metadata, tree center and Hessian blocks, completion distance.
- `conda run -n qipm --live-stream make -C notes/scalar-newton-paper` passes;
  current draft is 32 pages, with no undefined references/citations or
  overfull/underfull box warnings in main.log.
- Diagnostics supplement rather than prove the analytic results. The sole
  earlier-section change is the explicit inverse-overlap accuracy-range
  extension described in item 7. Other earlier-file changes are main
  inclusions, appended bibliography entries, and source-map dispositions.

Five independent reviews are still required before Stage 3a is complete.
