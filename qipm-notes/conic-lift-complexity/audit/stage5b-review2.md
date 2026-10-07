# Stage 5B independent review 2

Reviewed 2026-09-20. Read the applicable repository `AGENTS.md` and all five
requested files, end to end: `12a-resource-ledgers.tex`,
`12b-work-contracts.tex`, `12c-newton-comparisons.tex`,
`12d-query-output.tex`, and `12e-active-compilers.tex`.

**Verdict: no valid major or minor issue found.** No manuscript correction is
requested by this review. This is an independent mathematical and scope audit,
not a claim of exhaustive specialist priority clearance.

I did not read the other Stage 5B reviewer reports, the author reports, or
`root-stage5b-checks`. I read the permitted source map and relevant original
workbench notes. I made no manuscript edits and used no delegation.

## Newton mathematics and access contracts

- **Centered marginal and right-hand side, 12c:31–90.** Hadamard's inequality
  removes auxiliary off-diagonal residuals, and sourcewise AM–GM gives
  `d_a = rho_a/h_a`. The stated marginal, Hessian, and exact parameter follow.
  The residual-coordinate calculation also proves equality of the Newton
  linear terms, so the proposition does not rely on equality of Hessians
  alone. Public zero padding creates no additional projected variables.
- **Exact off-center quotient, 12c:141–186.** The Riesz representatives of
  the allocation functionals are `D E_a D`; their Gram matrix is the stated
  `M(D)`, and it is positive definite because every source has a column.
  Minimum-norm allocation gives `4 z^T M(D)^{-1} z`, with the remaining
  term `2 tr(D^{-1} U^T U)`. I checked the factors of two against direct
  differentiation of the full log determinant.
- **First-power transfer, 12c:188–211.** This improvement is valid. The
  positive matrix in the trace-order argument is `E(theta) D E(theta)`,
  even when `E(theta)` is indefinite. Commutation of the two diagonal
  matrices and the exact allocation sums give the crucial identity
  `sum tr(D0 E D E) = sum theta_a^2 rho_a^2/h_a`. Consequently both terms
  in the quotient satisfy the same first-power bounds. The proof does not
  assume a false monotonicity rule for arbitrary matrix products. Tangent
  restriction and inverse congruence give the stated constrained and dual
  comparisons.
- **Reduced gradient, 12c:214–235.** Completing the square about `B=D`
  changes the allocation target to `-2z-rho`. Expanding the constrained
  minimum gives exactly `2 rho^T M(D)^{-1} z + eta<c,U>`. This is the
  eliminated gradient, and it reduces to the marginal gradient at the fiber
  center. The warning about additional terms for affine infeasibility is
  necessary and present.
- **Sharpness and approximate allocation, 12c:237–292.** The two-source
  feasible example attains both spectral endpoints and the condition
  factor `L/mu`. Its inverse action and both trace-distance formulas are
  correct. The approximate-allocation factors follow from the same trace
  identity with sourcewise error; exact spectral approximation alone is
  not silently treated as exact feasibility.
- **Oracle equivalence and recentering, 12c:104–137, 300–400.** Equality is
  claimed for complete matched interfaces, not arbitrary unitary
  completions. The projected-output scope correctly excludes reconstruction
  of the dense auxiliary Gram direction. Exact rational recentering has
  the stated arithmetic and bit-size bounds for common-denominator dyadic
  coordinates. The missing-scale search reductions, all-source adversary
  sum, promised exact upper bounds, margin version, and distinction between
  online evaluation and source-free compilation are valid. The
  normalization and inverse-access costs remain explicit.

## Sparse elimination and the classical comparison

- **One- and two-hub formulas, 12c:412–500.** Direct expansion confirms both
  Hessian identities and `v^T D^{-1} v = 2r/(t+r) < 1`. The positive and
  negative groups in the regularized augmentation are definite, so the
  quasidefinite conclusion is valid. The resolvent estimate uses the
  necessary small-regularization hypothesis. The text correctly limits
  pivot-free factorization to exact arithmetic and does not infer finite
  precision stability from quasidefiniteness.
- **Low-treewidth theorem, 12c:428–452.** I checked Corollary 3 of
  [Fürer, Hoppen, and Trevisan, ESA 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol351-esa2025/LIPIcs.ESA.2025.116/LIPIcs.ESA.2025.116.pdf).
  It supports a solution in quadratic-in-width, linear-in-matrix-size
  arithmetic from a supplied compact bipartite decomposition. Doubling
  each scalar vertex into row and column copies gives width at most
  `2 tau + 1` and preserves compactness. Full row rank and the positive
  barrier Hessian guarantee nonsingularity. The citation handles
  cancellations and arbitrary nonzero pivots, including the zero scalar
  diagonal present in the reduced grouped system.
- **Graph counts, 12c:502–570.** The incidence expansion, grouped raw and
  reduced counts, treewidth upper bags, cycle and subdivided-`K4` lower
  witnesses, direct-ball star, and binary-tree counts agree. The reduced
  graph avoids the unsupported zero-diagonal leaf-pivot shortcut.
- **Replacement and iterative comparator, 12c:586–647.** The full-output
  conclusion explicitly assumes accessible current coefficients, supplied
  decompositions, a residual-based outer guarantee, and width bounds along
  every admitted trajectory. It is an exact-arithmetic module comparison.
  The CGLS/LSQR estimate follows from the CG energy norm of the consistent
  normal equations; the dependence is on `kappa_2(K)`, with no free
  formation of an implicit matrix. The text correctly excludes the tall
  Hessian sampling setting of Apers–Gribling.

## Other mathematical checks

- **12a, resource ledgers.** The discrete-convex capacity argument gives
  the exact total-order formula. The dimension recurrence, order-four and
  order-five specializations, ratio bounds, grouped Schur counts, and
  small-order simultaneous frontiers are consistent. The larger-order
  integer minima are correctly distinguished from attainable lift optima.
  The balanced finite packing counts include padding and last-block
  effects. Projection onto the grouped domain has bounded fibers and
  relative Slater feasibility, so the newly stated intrinsic parameter
  `H` follows from the earlier projection lemma and matrix-epigraph upper
  bound. The free-coordinate optimum, Lorentz comparisons, truncated
  nullity envelope, Hölder constant and equality aspect, and width-four
  Schur proxy calculation are correct.
- **12b, work composition.** The mixed rank and movement theorem use the
  same aggregate dual rank `Q`. The fixed-factor budget and sequential
  refinement preserve the relevant contact quantifiers. The work bound
  uses an explicit fresh charge, not a barrier parameter substituted for
  exposed rank. The divisible construction, cached dense serialization,
  scalar schedule, speed bound, and endpoint estimate substantiate the
  claimed upper order in their specified output models. Preprocessing,
  scalar evaluation, projected state preparation, and final readout are
  not conflated.
- **12d, query and output.** The Fourier-span/information proof gives the
  required linear approximate-sign recovery bound. The public-magnitude
  constructions reduce to the stated mean-estimation or search promises;
  their precision scales, strict half-gap thresholds, condition bounds,
  and sign decoders agree with the displayed geometry. The EJA certificate
  normalization gives support-minor scale one. Unequal-magnitude state
  preparation is correctly heralded exact with constant expected queries,
  or bounded-error with constant worst-case queries. Direct-ball and
  product-body comparisons are explicitly different-body comparisons.
  One-factor packed and shared-cone movement claims retain their own
  barrier and primal–dual metric hypotheses.
- **12e, acquisition.** Search reductions identify the exact output
  contract. The radius, Pareto witness, adjacent-contact, growing-dimension
  decoder, and entropy aggregation calculations check out. The growing
  example distinguishes its decoding objective from its metric objective.
  The entropy comparison matches total gaps rather than multipliers, and
  preserves the closed perspective domain. The path and consensus KKT
  estimates do not become lower bounds against public elimination.
  Source-free compiled output, continued oracle access, and explicit-input
  loading are kept distinct.

## Coverage and attribution

I compared the Stage 5B source-map routing with original workbench material
on PSD order caps, packing Pareto and work ledgers, centered Newton forests,
reduced-oracle equivalence, off-center Schur elimination, implicit
recentering, latent Lorentz treewidth, symmetric-cone readout, product-disk
and direct-ball precision, joint search diagnostics, SOC compilation,
Pareto compilation, and blockwise entropy compilation. The retained core
claims are represented or subsumed. Deferred dynamic fresh-information
claims are not imported into the static snapshot model.

The Newton attribution is appropriately limited: low-rank augmentation,
quasidefinite factorization, sparse elimination, and Krylov estimates are
credited established tools; the formulation-specific identities and
allocation-aware transfer are separated from them. Local primary full text
for Chen–Goulart supports the augmentation comparison. Local primary full
text for Apers–Gribling supports the stated distinction between explicit
sparse solves and quantum Hessian/gradient acquisition.

I also checked BHMT's Theorems 4 and 16 in its local primary full text and
[Ambainis–Childs–Le Gall–Tani, Theorems 3–4](https://arxiv.org/pdf/0903.1291).
They support the known-cardinality exact-query upper bounds, promised
zero-versus-one search, and the adversary direct sums used here. Those
ingredients are not claimed as new query theorems.

## Independent numerical and build checks

Using `/workspace/local-home/miniconda3/envs/qipm/bin/python`, I ran direct full-matrix
Newton elimination for 40 independently generated two-source packed
instances with exact source allocations. Maximum discrepancies from the
stated quotient Hessian and reduced gradient were approximately
`4.69e-13` and `1.51e-14`. Every instance satisfied both first-power
semidefinite inequalities. These checks supplement the proof audit; they
are not evidence replacing the exact argument.

I independently computed dynamic programs for every `R=2,...,30` and
`N=1,...,500`. The total-order closed formula and the stated special
dimension formulas agreed throughout.

`conda run -n qipm --live-stream make` succeeded. Latexmk reported that all
targets were up to date. The existing log contained no undefined-reference,
undefined-citation, overfull-box, warning, or error matches. This was an
up-to-date build check, not a forced clean rebuild or a page-by-page PDF
inspection.
